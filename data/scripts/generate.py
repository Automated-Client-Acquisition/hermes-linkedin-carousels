#!/usr/bin/env python3
"""
generate.py — STEP 4 of the linkedin-carousels pipeline.

Generates ONE slide image with OpenAI's gpt-image-2-2026-04-21 model and saves it into
the run's slides/ folder. Idempotent: if the slide image already exists it is
skipped unless --force is passed. That idempotency is what makes the art step
resumable after an interruption — a crashed run just continues from the
missing slide.

Usage:
    python .claude/skills/linkedin-carousels/scripts/generate.py \
        --run "runs/on-page-aeo-2026-05-14" \
        --slide 3 \
        --prompt "<visual note + locked style fragment>"

Optional:
    --reference "slides/slide-01.png"   anchor style on an earlier slide
    --force                             regenerate even if the image exists
    --size 1024x1536                    gpt-image-2-2026-04-21 size (default 1024x1536, ~4:5)

Requires OPENAI_API_KEY in the environment.
"""
import argparse
import base64
import sys
from pathlib import Path

import state as state_mod  # local module, same folder

# Multi-turn image generation via the Responses API.
# gpt-5.5 (and newer) supports tools=[{"type": "image_generation"}] with
# previous_response_id chaining. Chaining preserves visual context across
# slides — paper color, type rendering, accent intensity, composition
# language — so the deck reads as one set instead of ten lookalikes.
# Reference: https://developers.openai.com/api/docs/guides/image-generation
#
# The legacy direct-image-endpoint approach (client.images.generate /
# images.edit with model=gpt-image-2-2026-04-21) is still viable but lacks the
# automatic visual context propagation that makes a carousel coherent.
DEFAULT_SIZE = "1024x1536"
MODEL = "gpt-5.5"


def fail(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def get_client():
    try:
        from openai import OpenAI
    except ImportError:
        fail("openai package not installed. Run: pip install -r "
             ".claude/skills/linkedin-carousels/requirements.txt")
    import os
    # Load OPENAI_API_KEY from .env at the repo root if present. Real env
    # vars always win — the file is just a convenience so the key doesn't
    # have to be re-exported every session.
    try:
        from dotenv import load_dotenv
        repo_root = Path(__file__).resolve().parents[4]
        load_dotenv(repo_root / ".env", override=False)
    except ImportError:
        pass  # dotenv optional — exporting the var manually still works
    if not os.environ.get("OPENAI_API_KEY"):
        fail("OPENAI_API_KEY not set. Either `export OPENAI_API_KEY=sk-...` "
             "or add it to the .env file at the repo root.")
    return OpenAI()


def _extract_image_from_response(response) -> bytes:
    """Pull the b64 image payload out of a Responses API response.

    The response.output is a list of items; the image lives in an item of
    type 'image_generation_call' with a base64 result on its .result field.
    """
    items = getattr(response, "output", None) or []
    for item in items:
        item_type = getattr(item, "type", None)
        if item_type == "image_generation_call":
            b64 = getattr(item, "result", None)
            if b64:
                return base64.b64decode(b64)
    fail("OpenAI response contained no image_generation_call output. "
         "Inspect the run's workspace history for the response id.")


def generate_image(client, prompt: str, size: str,
                   previous_response_id: str | None,
                   reference: Path | None) -> tuple[bytes, str]:
    """Generate one slide via the Responses API.

    Three modes, in priority order:
    1. If previous_response_id is set, chain off it (multi-turn).
    2. Else if reference is set, pass the reference image as input alongside
       the prompt (single-turn anchored on a literal image).
    3. Else generate from prompt only (cold start, no visual anchor).

    Returns (image_bytes, response_id). Caller persists the response_id so
    the next slide can chain off this one.
    """
    tools = [{"type": "image_generation", "size": size}]

    if previous_response_id:
        response = client.responses.create(
            model=MODEL,
            previous_response_id=previous_response_id,
            input=prompt,
            tools=tools,
        )
    elif reference is not None:
        if not reference.exists():
            fail(f"reference image not found: {reference}")
        with open(reference, "rb") as ref_fh:
            ref_b64 = base64.b64encode(ref_fh.read()).decode("ascii")
        response = client.responses.create(
            model=MODEL,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{ref_b64}",
                        },
                    ],
                }
            ],
            tools=tools,
        )
    else:
        response = client.responses.create(
            model=MODEL,
            input=prompt,
            tools=tools,
        )

    img_bytes = _extract_image_from_response(response)
    response_id = getattr(response, "id", None)
    if not response_id:
        fail("OpenAI response had no .id; cannot chain subsequent slides.")
    return img_bytes, response_id


def main():
    p = argparse.ArgumentParser(description="Generate one carousel slide image.")
    p.add_argument("--run", required=True, help="Path to the run folder.")
    p.add_argument("--slide", type=int, required=True, help="Slide number (1-based).")
    p.add_argument("--prompt", required=True, help="Full image prompt.")
    p.add_argument("--reference", help="Optional earlier slide image to anchor style. "
                   "Ignored when --previous-response-id is set or auto-chaining picks one up.")
    p.add_argument("--previous-response-id", default=None,
                   help="Explicit Responses-API response id to chain off. "
                   "If omitted, auto-chains off the previous slide's stored id.")
    p.add_argument("--no-chain", action="store_true",
                   help="Disable auto-chaining off the previous slide's response id. "
                   "Use when you intentionally want a fresh generation.")
    p.add_argument("--size", default=None,
                   help="Image size for gpt-image-2-2026-04-21 (e.g. 1024x1536). "
                        "If omitted, reads format.source_size from the run's "
                        "workspace JSON. Falls back to 1024x1536.")
    p.add_argument("--force", action="store_true", help="Regenerate even if it exists.")
    args = p.parse_args()

    run_dir = Path(args.run)
    if not run_dir.exists():
        fail(f"run folder does not exist: {run_dir}")

    # load + guard state
    try:
        ws = state_mod.load(run_dir)
        state_mod.require_step_done(ws, "script")
        state_mod.require_step_done(ws, "style")
    except state_mod.StateError as e:
        fail(str(e))

    if args.slide < 1:
        fail("--slide must be >= 1")

    # Raw slide PNGs live inside .working/slides/ in the new layout. Legacy
    # runs kept them at runs/<slug>/slides/ — fall back to that if .working/
    # doesn't exist yet (e.g. mid-migration).
    working_slides = run_dir / ".working" / "slides"
    legacy_slides = run_dir / "slides"
    if working_slides.exists() or (run_dir / ".working").exists():
        slides_dir = working_slides
    elif legacy_slides.exists():
        slides_dir = legacy_slides
    else:
        slides_dir = working_slides  # default: write into new layout
    slides_dir.mkdir(parents=True, exist_ok=True)
    out_path = slides_dir / f"slide-{args.slide:02d}.png"

    # idempotency — this is what makes the step resumable
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} already exists (pass --force to regenerate).")
        ws["images"][f"slide_{args.slide:02d}"] = "done"
        state_mod.save(run_dir, ws)
        return

    reference = None
    if args.reference:
        reference = Path(args.reference)
        if not reference.is_absolute():
            # Try the new layout first (run_dir/.working/<arg>), then fall
            # back to the legacy layout (run_dir/<arg>). Users typing
            # `--reference slides/slide-01.png` should hit either without
            # caring about the migration.
            candidate_new = run_dir / ".working" / args.reference
            candidate_legacy = run_dir / args.reference
            if candidate_new.exists():
                reference = candidate_new
            elif candidate_legacy.exists():
                reference = candidate_legacy
            else:
                reference = candidate_new  # let the existence check below fail clearly

    # Resolve which response_id (if any) to chain off. Priority:
    # 1. Explicit --previous-response-id from the CLI.
    # 2. Auto-chain: the previous slide's stored response_id (unless --no-chain).
    # 3. None: cold start; reference image (if any) is used instead.
    previous_response_id = args.previous_response_id
    if not previous_response_id and not args.no_chain and args.slide > 1:
        prev_key = f"slide_{args.slide - 1:02d}_response_id"
        previous_response_id = ws.get("images", {}).get(prev_key)

    chain_note = ""
    if previous_response_id:
        chain_note = f", chained off response {previous_response_id[:12]}..."
    elif reference:
        chain_note = f", anchored on {reference.name}"
    # Resolve image size: --size CLI arg wins; else workspace format.source_size;
    # else DEFAULT_SIZE. Workspace lookup tolerates older runs that have no
    # format field.
    if args.size:
        size = args.size
    else:
        fmt = ws.get("format") or {}
        size = fmt.get("source_size", DEFAULT_SIZE)

    print(f"Generating slide {args.slide} -> {out_path} (size {size}){chain_note}")

    client = get_client()
    try:
        img_bytes, response_id = generate_image(
            client, args.prompt, size, previous_response_id, reference
        )
    except Exception as e:  # noqa: BLE001 - surface any API failure cleanly
        fail(f"image generation failed: {e}")

    out_path.write_bytes(img_bytes)

    # update workspace
    ws["images"][f"slide_{args.slide:02d}"] = "done"
    ws["images"][f"slide_{args.slide:02d}_response_id"] = response_id
    state_mod.log(ws, "art",
                  f"generated slide {args.slide:02d} (response {response_id[:12]}...)")

    # if every scripted slide is now present, mark the art step done
    expected = ws.get("slide_count")
    if expected:
        have = sum(
            1 for n in range(1, expected + 1)
            if (slides_dir / f"slide-{n:02d}.png").exists()
        )
        if have == expected:
            ws["steps"]["art"] = "done"
            state_mod.log(ws, "art", f"all {expected} slides generated")
            print(f"ALL {expected} SLIDES DONE — art step complete.")
    state_mod.save(run_dir, ws)

    print(f"OK: wrote {out_path}")


if __name__ == "__main__":
    main()
