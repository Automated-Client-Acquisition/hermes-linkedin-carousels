#!/usr/bin/env python3
"""
export.py — STEP 5 of the linkedin-carousels pipeline.

Takes the generated slide images, normalizes each to exactly 1080x1350
(4:5, sRGB, no alpha — the format LinkedIn and Instagram both accept), and
writes the ready-to-post bundle into the run's export/ folder along with the
post copy and a pre-post checklist.

Usage:
    python data/scripts/export.py \
        --run "runs/on-page-aeo-2026-05-14"

Requires Pillow (see requirements.txt).
"""
import argparse
import re
import sys
from pathlib import Path

import state as state_mod

TARGET_W, TARGET_H = 1080, 1350


def fail(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def hex_to_rgb(s: str) -> tuple[int, int, int]:
    """Parse '#RRGGBB' or 'RRGGBB' into (r, g, b)."""
    s = s.strip().lstrip("#")
    if len(s) != 6:
        raise ValueError(f"bad hex: {s!r}")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def detect_dominant_bg(img, sample_size: int = 32) -> tuple[int, int, int]:
    """Sample the four corners of the image and return the mean RGB.

    gpt-image-2-2026-04-21 keeps the background uniform near the edges even when the
    middle has type and accents. Averaging the four corner regions gives
    the dominant page color without picking up any foreground content.
    """
    w, h = img.size
    boxes = [
        (0, 0, sample_size, sample_size),
        (w - sample_size, 0, w, sample_size),
        (0, h - sample_size, sample_size, h),
        (w - sample_size, h - sample_size, w, h),
    ]
    rs, gs, bs = [], [], []
    for box in boxes:
        region = img.crop(box).convert("RGB").getdata()
        for r, g, b in region:
            rs.append(r); gs.append(g); bs.append(b)
    return sum(rs) // len(rs), sum(gs) // len(gs), sum(bs) // len(bs)


def _first_content_col_left_to_right(img, target_rgb, tolerance: int):
    """First column (left→right) containing any non-bg pixel. None if all bg."""
    w, h = img.size
    px = img.load()
    for x in range(w):
        for y in range(h):
            r, g, b = px[x, y][:3]
            if (abs(r - target_rgb[0]) > tolerance
                    or abs(g - target_rgb[1]) > tolerance
                    or abs(b - target_rgb[2]) > tolerance):
                return x
    return None


def _last_content_col_right_to_left(img, target_rgb, tolerance: int):
    """Last column (right→left) containing any non-bg pixel. None if all bg."""
    w, h = img.size
    px = img.load()
    for x in range(w - 1, -1, -1):
        for y in range(h):
            r, g, b = px[x, y][:3]
            if (abs(r - target_rgb[0]) > tolerance
                    or abs(g - target_rgb[1]) > tolerance
                    or abs(b - target_rgb[2]) > tolerance):
                return x
    return None


def smart_zoom_content(img, target_hex: str,
                       target_content_fraction: float = 0.82,
                       min_zoom_trigger_fraction: float = 0.78,
                       max_zoom: float = 1.4,
                       min_top_margin_px: int = 90,
                       min_bottom_margin_px: int = 75,
                       tolerance: int = 10):
    """If the content's vertical extent is well below the target fraction
    of canvas height, scale the content up to fill that fraction.

    Only triggers when content_h < min_zoom_trigger_fraction × TARGET_H —
    avoids zooming slides that already fill the canvas.

    After zoom: content is centered horizontally and placed at
    min_top_margin_px from the top. Bg around the content is the canonical
    bg hex.

    Args:
        target_content_fraction: aim to have content occupy this fraction of
            canvas height.
        min_zoom_trigger_fraction: only zoom when current content is below
            this fraction. Stops the pass from messing with already-good
            slides.
        max_zoom: cap on the scale factor. 1.4× = max 40% upscale.
        min_top_margin_px: where to land the top of the zoomed content.
    """
    from PIL import Image
    target_rgb = hex_to_rgb(target_hex)
    w, h = img.size

    top = _first_content_row_top_down(img, target_rgb, tolerance)
    bot = _last_content_row_bottom_up(img, target_rgb, tolerance)
    if top is None or bot is None:
        return img, 1.0

    # Determine left/right bounds for the horizontal extent.
    left = _first_content_col_left_to_right(img, target_rgb, tolerance)
    right = _last_content_col_right_to_left(img, target_rgb, tolerance)
    if left is None or right is None:
        return img, 1.0

    content_h = bot - top + 1
    content_w = right - left + 1
    v_fraction = content_h / h
    h_fraction = content_w / w

    # Trigger zoom when EITHER dimension is below the threshold. gpt-image-2-2026-04-21
    # sometimes renders content that fills vertically but is narrow
    # horizontally (small card + wide bg gutters), or vice versa. Either
    # case reads as a too-small slide.
    if v_fraction >= min_zoom_trigger_fraction and h_fraction >= min_zoom_trigger_fraction:
        return img, 1.0  # already fills enough of the canvas in both dims

    target_h = int(h * target_content_fraction)
    target_w = int(w * target_content_fraction)
    zoom_by_h = target_h / content_h
    zoom_by_w = target_w / content_w
    # Pick the LARGER zoom (favoring horizontal fill, since gpt-image-2-2026-04-21
    # frequently renders narrow content with wide bg gutters).
    zoom = min(max(zoom_by_h, zoom_by_w), max_zoom)
    # HARD caps so the zoomed content respects BOTH safe-areas:
    #   - vertical: content must fit between min_top_margin_px and
    #     (h - min_bottom_margin_px). Available height = h - top - bottom.
    #   - horizontal: leave 5% margin on each side.
    max_zoom_by_v_safe = (h - min_top_margin_px - min_bottom_margin_px) / content_h
    max_zoom_by_h_safe = w * 0.90 / content_w  # 5% margin each side
    zoom = min(zoom, max_zoom_by_v_safe, max_zoom_by_h_safe)
    if zoom <= 1.01:
        return img, 1.0  # not worth a sub-1% rescale

    # Crop the content bbox, scale it, center it horizontally, place it at
    # min_top_margin_px from the top.
    content = img.crop((left, top, right + 1, bot + 1))
    new_w = int(content_w * zoom)
    new_h = int(content_h * zoom)
    scaled = content.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), target_rgb)
    paste_x = (w - new_w) // 2
    paste_y = min_top_margin_px
    canvas.paste(scaled, (paste_x, paste_y))
    return canvas, zoom


def _first_content_row_top_down(img, target_rgb, tolerance: int):
    """First row (top→bottom) containing any non-bg pixel. None if all bg."""
    w, h = img.size
    px = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][:3]
            if (abs(r - target_rgb[0]) > tolerance
                    or abs(g - target_rgb[1]) > tolerance
                    or abs(b - target_rgb[2]) > tolerance):
                return y
    return None


def _last_content_row_bottom_up(img, target_rgb, tolerance: int):
    """Last row (bottom→top) containing any non-bg pixel. None if all bg."""
    w, h = img.size
    px = img.load()
    for y in range(h - 1, -1, -1):
        for x in range(w):
            r, g, b = px[x, y][:3]
            if (abs(r - target_rgb[0]) > tolerance
                    or abs(g - target_rgb[1]) > tolerance
                    or abs(b - target_rgb[2]) > tolerance):
                return y
    return None


def ensure_top_safe_area(img, target_hex: str,
                         min_top_margin_px: int = 90,
                         min_bottom_margin_px: int = 75,
                         tolerance: int = 10):
    """Enforce the top safe-area by shifting content down. Uses available
    bottom margin first; if that's not enough, scales the content
    proportionally to make room without clipping bottom-edge elements.

    Strategy:
    1. Detect topmost and bottommost non-bg rows.
    2. If top margin already >= min_top_margin_px: no-op.
    3. Else compute the shift needed and the slack available at the bottom.
       Slack = (bottom_margin - min_bottom_margin_px).
    4. If slack covers the shift: pure translate down. No distortion.
    5. Else: translate by the slack amount, then scale the content box
       slightly to fit the remaining shift. Tiny distortion, no clipping.

    This handles gpt-image-2's tendency to push the kicker pill against
    the top edge while keeping page-counter and bottom elements intact.

    Args:
        min_top_margin_px: hard floor for top empty bg. 90px / 1350 ≈ 6.7%.
        min_bottom_margin_px: hard floor for bottom empty bg. 75px / 1350 ≈ 5.5%.
        tolerance: bg-color tolerance for the row scan. Keep TIGHT (~10):
            the white pill body (#FFFFFF) is only ~13 RGB units from the
            Bone bg (#F2EEE6). A wider tolerance lets the detector skip
            over the pill body and find content only at the pill's dark
            outline, mis-computing the shift.
    """
    from PIL import Image
    target_rgb = hex_to_rgb(target_hex)
    w, h = img.size

    top_content = _first_content_row_top_down(img, target_rgb, tolerance)
    if top_content is None or top_content >= min_top_margin_px:
        return img, 0  # all bg or already safe

    bottom_content = _last_content_row_bottom_up(img, target_rgb, tolerance)
    if bottom_content is None:
        return img, 0

    needed_shift = min_top_margin_px - top_content

    # Strategy: extend the canvas at the top with `needed_shift` rows of
    # bg-colored pixels, then resize the entire (taller) canvas back to
    # the target dimensions. Result: top margin is exactly correct, no
    # bottom content is lost, and the vertical distortion is needed_shift/h
    # (typically ~1-5%, imperceptible).
    #
    # NEVER simple-translate: that requires cropping at the bottom, which
    # erases the page counter on the (common) slides where gpt-image-2-2026-04-21
    # jammed it against the canvas edge.
    #
    # NEVER scale-down without canvas extension: that sub-pixel-aliases
    # small mono text and the bg-lock pass then erases the anti-aliased
    # edges.
    extended = Image.new("RGB", (w, h + needed_shift), target_rgb)
    extended.paste(img, (0, needed_shift))
    # Now extended is (w, h + needed_shift); resize back to (w, h) so the
    # final output matches the canvas dimensions exactly.
    final = extended.resize((w, h), Image.LANCZOS)
    return final, needed_shift


def lock_background(img, target_hex: str, tolerance: int = 8):
    """Replace pixels close to the detected dominant background with the
    target hex color. Conservative: only pixels within +/- tolerance RGB
    units of the detected bg get rewritten.

    Tolerance is intentionally TIGHT (8). Wider tolerance (e.g. 15) erases
    anti-aliased edges of small Muted-ink text (page counter, kicker pill
    labels) because those edge pixels sit only a few RGB units off the bg.
    Card surfaces (#FFFFFF, ~13 units from #F2EEE6) and accent colors are
    untouched at any reasonable tolerance.
    """
    from PIL import Image
    target_rgb = hex_to_rgb(target_hex)
    detected = detect_dominant_bg(img)

    # If the detected bg is already within tolerance of the target, the lock
    # is a no-op visually. Still run it so the output is bit-deterministic.
    px = img.load()
    w, h = img.size
    dr, dg, db = detected
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][:3]
            if (abs(r - dr) <= tolerance
                    and abs(g - dg) <= tolerance
                    and abs(b - db) <= tolerance):
                px[x, y] = target_rgb
    return img, detected


def normalize_image(src: Path, dst: Path, bg_hex: str | None = None,
                    target_w: int = 1080, target_h: int = 1350):
    """Resize+center-crop to exactly 1080x1350, optionally lock the
    background to bg_hex, flatten to sRGB RGB, save PNG.
    """
    try:
        from PIL import Image, ImageOps
    except ImportError:
        fail("Pillow not installed. Run: pip install -r "
             "data/requirements.txt")

    img = Image.open(src)
    # flatten transparency onto white first; the bg lock pass (if any) runs
    # after resize so it operates on the final pixel grid.
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img).convert("RGB")
    else:
        img = img.convert("RGB")

    # CONTAIN-AND-PAD to the target canvas, NOT center-crop.
    #
    # gpt-image-2-2026-04-21 generates at 1024x1536 (aspect 0.667). Target is 1080x1350
    # (aspect 0.800). With ImageOps.fit (center-crop), the source gets
    # scaled UP to match width then 135px gets cropped from top AND bottom.
    # That crops off page counter rows on slides where the model put the
    # counter near the bottom edge of its render. Page counter goes ghost.
    #
    # Contain-and-pad instead: scale the source to fit INSIDE the target
    # without losing pixels, then pad the leftover width with the canonical
    # bg color. The vertical content is preserved; we lose only a small
    # amount of side margin (which was empty bg anyway).
    src_w, src_h = img.size
    scale = min(target_w / src_w, target_h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    scaled = img.resize((new_w, new_h), Image.LANCZOS)
    # Pad to target dims; if bg_hex is set, pad with that; else white.
    pad_rgb = hex_to_rgb(bg_hex) if bg_hex else (255, 255, 255)
    canvas = Image.new("RGB", (target_w, target_h), pad_rgb)
    offset = ((target_w - new_w) // 2, (target_h - new_h) // 2)
    canvas.paste(scaled, offset)
    img = canvas
    detected = None
    shift_applied = 0
    zoom_applied = 1.0
    if bg_hex:
        # Step 1: lock the bg first. This rewrites every near-bg pixel to
        # exactly bg_hex, so the smart-zoom and safe-area detectors see a
        # clean canvas and can use a tight tolerance to find true content
        # edges.
        img, detected = lock_background(img, bg_hex)
        # Step 2: smart-zoom — if the content occupies less than ~78% of
        # the canvas height (because gpt-image-2-2026-04-21 rendered it small with
        # extra bg around it, and our contain-and-pad fit preserved that
        # margin), scale the content up to fill ~82% of canvas height. The
        # content is centered horizontally and placed at min_top_margin_px
        # from the top. Slides that already fill the canvas are untouched.
        img, zoom_applied = smart_zoom_content(img, bg_hex)
        # Step 3: enforce the top safe-area. After smart-zoom the top
        # margin is already correct on the zoomed slides; this pass only
        # acts on slides that weren't zoomed (zoom_applied == 1.0).
        img, shift_applied = ensure_top_safe_area(img, bg_hex)
    img.save(dst, format="PNG")
    return detected, shift_applied, zoom_applied


def parse_script(script_path: Path):
    """Pull post copy and slide count from script.md. Tolerant parser."""
    text = script_path.read_text()
    post_copy = ""
    m = re.search(r"##\s*Post Copy\s*\n(.+?)(?:\n---|\n##\s*Slide)", text, re.S | re.I)
    if m:
        post_copy = m.group(1).strip()
    slide_nums = [int(n) for n in re.findall(r"##\s*Slide\s+(\d+)", text, re.I)]
    return post_copy, (max(slide_nums) if slide_nums else 0)


def main():
    p = argparse.ArgumentParser(description="Export a finished carousel.")
    p.add_argument("--run", required=True, help="Path to the run folder.")
    args = p.parse_args()

    run_dir = Path(args.run)
    if not run_dir.exists():
        fail(f"run folder does not exist: {run_dir}")

    try:
        ws = state_mod.load(run_dir)
        state_mod.require_step_done(ws, "script")
        state_mod.require_step_done(ws, "style")
        state_mod.require_step_done(ws, "art")
    except state_mod.StateError as e:
        fail(str(e))

    # Resolve format. New runs store it in workspace.format; legacy runs
    # don't have it and fall back to the portrait default.
    fmt = state_mod.format_spec((ws.get("format") or {}).get("name"))
    target_w = fmt["width"]
    target_h = fmt["height"]
    print(f"  format: {fmt['name']} ({target_w}x{target_h}, aspect {fmt['aspect']})")

    # Resolve scaffolding paths. Prefer the new .working/ layout; fall back
    # to the legacy flat layout for runs that haven't been migrated yet.
    working_dir = run_dir / ".working"
    def _pick(new_rel: str, legacy_rel: str) -> Path:
        new = working_dir / new_rel
        legacy = run_dir / legacy_rel
        if new.exists():
            return new
        if legacy.exists():
            return legacy
        return new  # default to new for writes

    script_path = _pick("script.md", "script.md")
    if not script_path.exists():
        fail("script.md not found — STEP 2 must be complete.")

    post_copy, scripted_count = parse_script(script_path)
    slide_count = ws.get("slide_count") or scripted_count
    if not slide_count:
        fail("could not determine slide count from workspace or script.md.")

    # Raw slide PNGs live in .working/slides/ (or legacy slides/).
    if (working_dir / "slides").exists():
        slides_dir = working_dir / "slides"
    elif (run_dir / "slides").exists():
        slides_dir = run_dir / "slides"
    else:
        fail(f"no slides folder found at {working_dir / 'slides'} or "
             f"{run_dir / 'slides'}.")

    # Final exports land at the run root (the product surface). The PNGs,
    # post-copy.txt, and CHECKLIST.md sit next to each other at the top of
    # the run folder so a non-technical operator opens the run folder and
    # immediately sees what to post.
    export_dst = run_dir

    # confirm every scripted slide image exists BEFORE writing anything
    missing = [
        n for n in range(1, slide_count + 1)
        if not (slides_dir / f"slide-{n:02d}.png").exists()
    ]
    if missing:
        fail(f"missing slide images for slides: {missing}. "
             "Run generate.py for those slides before exporting.")

    # Read the canonical background hex from .working/style/canonical-bg.txt
    # (or legacy 02_style/canonical-bg.txt). When set, the normalize pass
    # locks every slide's background to that exact color.
    bg_lock_path = _pick("style/canonical-bg.txt", "02_style/canonical-bg.txt")
    bg_hex = bg_lock_path.read_text().strip() if bg_lock_path.exists() else None
    if bg_hex:
        print(f"  bg-lock: every slide background locked to {bg_hex}")

    # normalize each slide into the export destination (= run root in the
    # new layout; legacy runs used run_dir/export/ which is no longer the
    # case).
    for n in range(1, slide_count + 1):
        src = slides_dir / f"slide-{n:02d}.png"
        dst = export_dst / f"{n:02d}.png"
        result = normalize_image(src, dst, bg_hex=bg_hex,
                                 target_w=target_w, target_h=target_h)
        # normalize_image now returns (detected_bg, shift_px, zoom_factor).
        # Accept older 2-tuple shape for backwards compat.
        if isinstance(result, tuple) and len(result) == 3:
            detected, shift_applied, zoom_applied = result
        elif isinstance(result, tuple) and len(result) == 2:
            detected, shift_applied = result
            zoom_applied = 1.0
        else:
            detected, shift_applied, zoom_applied = result, 0, 1.0
        notes = []
        if detected and bg_hex:
            target = hex_to_rgb(bg_hex)
            d = max(abs(detected[i] - target[i]) for i in range(3))
            notes.append(f"bg drift {d}")
        if zoom_applied and abs(zoom_applied - 1.0) > 0.01:
            notes.append(f"zoom x{zoom_applied:.2f}")
        if shift_applied:
            notes.append(f"safe-area shift +{shift_applied}px")
        note = f"  ({', '.join(notes)})" if notes else ""
        print(f"  exported {dst.name}  ({target_w}x{target_h}){note}")

    # Build the LinkedIn-ready multi-page PDF from the just-exported PNGs.
    # 10 pages, each page sized exactly to the slide aspect (no letterbox,
    # no distortion). LinkedIn's document carousel preserves source aspect,
    # so portrait slides give portrait pages.
    #
    # PNGs in PDFs are heavy. We re-encode each page as JPEG (quality 92)
    # inside the PDF to keep file size sane while staying visually clean.
    from PIL import Image as _Image
    pdf_path = export_dst / "carousel.pdf"
    pages = []
    for n in range(1, slide_count + 1):
        png = export_dst / f"{n:02d}.png"
        img = _Image.open(png).convert("RGB")
        pages.append(img)
    if pages:
        first, rest = pages[0], pages[1:]
        first.save(
            pdf_path,
            "PDF",
            resolution=72.0,
            save_all=True,
            append_images=rest,
            quality=92,
        )
        pdf_size_mb = pdf_path.stat().st_size / (1024 * 1024)
        print(f"  exported carousel.pdf  ({slide_count} pages at "
              f"{target_w}x{target_h}, {pdf_size_mb:.1f} MB)")

    # post copy (lands at the run root next to the PNGs — the product surface)
    (export_dst / "post-copy.txt").write_text(
        (post_copy or "[No post copy found in script.md]") + "\n"
    )

    # alt-text stub lives in .working/ (it's a checklist for the operator
    # to fill in, not a deliverable). New runs put it in .working/; legacy
    # runs kept it at the run root.
    if working_dir.exists():
        alt_path = working_dir / "alt-text.md"
    else:
        alt_path = run_dir / "alt-text.md"
    if not alt_path.exists():
        alt_lines = ["# Alt text per slide\n",
                     "_One concise, descriptive line per slide for accessibility._\n"]
        for n in range(1, slide_count + 1):
            alt_lines.append(f"- Slide {n:02d}: ")
        alt_path.write_text("\n".join(alt_lines) + "\n")

    # pre-post checklist (also lands at the run root — operator-facing)
    trigger = ws.get("comment_trigger_word") or "[set in script step]"
    platform = ws.get("platform", "both")
    checklist = f"""# Pre-post checklist — {ws.get('topic', '')}

- [ ] `carousel.pdf` is in this folder ({slide_count} pages at {target_w}x{target_h})
- [ ] `01.png` ... `{slide_count:02d}.png` are in this folder ({slide_count} slides at {target_w}x{target_h})
- [ ] Post copy reviewed (`post-copy.txt`)
- [ ] Alt text written for every slide (`.working/alt-text.md`)
- [ ] CTA slide is slide {slide_count} — verify the call to action reads cleanly
- [ ] Comment trigger word: **{trigger}**
- [ ] If using ManyChat-style auto-DM, the trigger word is wired up

## Platform notes
"""
    if platform in ("linkedin", "both"):
        checklist += ("- LinkedIn: upload `carousel.pdf` as a document post "
                      "(better reach than image carousels). Paste `post-copy.txt` "
                      "into the post body.\n")
    if platform in ("instagram", "both"):
        checklist += ("- Instagram: upload `01.png` through "
                      f"`{slide_count:02d}.png` in order as a carousel post. "
                      "Paste `post-copy.txt` into the caption.\n")
    (export_dst / "CHECKLIST.md").write_text(checklist)

    # finalize state
    ws["steps"]["export"] = "done"
    ws["status"] = "complete"
    state_mod.log(ws, "export", f"exported {slide_count} slides to run root")
    state_mod.save(run_dir, ws)

    print(f"\nOK: carousel exported to {export_dst}")
    print(f"  - {slide_count} PNG slides at {target_w}x{target_h} (01.png .. {slide_count:02d}.png) — for Instagram")
    print(f"  - carousel.pdf ({slide_count} pages at {target_w}x{target_h}) — for LinkedIn")
    print(f"  - post copy: {export_dst / 'post-copy.txt'}")
    print(f"  - checklist: {export_dst / 'CHECKLIST.md'}")
    print(f"  - comment trigger word: {trigger}")
    print("  - remember to fill in alt-text.md before posting")


if __name__ == "__main__":
    main()
