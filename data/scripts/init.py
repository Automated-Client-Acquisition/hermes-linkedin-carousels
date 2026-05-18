#!/usr/bin/env python3
"""
init.py — STEP 0 of the linkedin-carousels pipeline.

The FIRST call. Creates the run folder structure and the workspace JSON so
the rest of the pipeline knows what has been done. Also creates the brand
folder if it does not exist yet.

Usage:
    python .claude/skills/linkedin-carousels/scripts/init.py \
        --topic "On-page AEO" --brand aca --platform both --slides 10

    # first time using a brand:
    python .claude/skills/linkedin-carousels/scripts/init.py \
        --topic "Crew retention" --brand lighthouse --new-brand
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys
from pathlib import Path

# Path model for a distributable Claude Code skill.
# The skill folder is dropped into any project at:
#     <project>/.claude/skills/linkedin-carousels/
# Brands, runs, and the user's own libraries live in the PROJECT, not the skill:
#     <project>/brands/<brand>/
#     <project>/runs/<slug-date>/
#     <project>/styles/<name>/           (user-added, optional)
#     <project>/voices/<name>/           (user-added, optional)
#     <project>/hooks/<name>/            (user-added, optional)
#     <project>/post-patterns/<name>/    (user-added, optional)
#
# Library discovery merges two tiers:
#   1. Skill-shipped defaults at <skill>/styles, <skill>/voices, etc.
#   2. Project-local entries at <project>/styles, <project>/voices, etc.
# On name conflict the project-local entry wins (so users can shadow defaults
# without forking the skill).
SKILL_DIR = Path(os.environ.get("CAROUSELS_SKILL_DIR")
                 or Path(__file__).resolve().parent.parent)
REPO_ROOT = Path(os.environ.get("CAROUSELS_PROJECT_ROOT")
                 or SKILL_DIR.parent.parent.parent)
BRANDS_DIR = REPO_ROOT / "brands"
RUNS_DIR = REPO_ROOT / "runs"
BRAND_TEMPLATE = SKILL_DIR / "templates" / "brand.md"

# The five library kinds. Each has a folder of the same name inside both
# the skill (defaults) and the project root (user-added).
# (The diagrams/ library was removed — it was a prescriptive checklist of
# named visualization templates; the new architecture trusts the model to
# compose visuals contextually per slide.)
LIBRARY_KINDS = ("styles", "voices", "hooks", "post-patterns",
                 "layout-systems")

# State + scaffolding paths inside a run folder.
#
# The run folder is shaped for end users, not for pipeline scaffolding:
#   runs/<slug>/
#     01.png .. 10.png       <- final deliverables, at the root
#     post-copy.txt          <- caption for the post
#     CHECKLIST.md           <- pre-post checks
#     .working/              <- everything pipeline-internal (hidden)
#       .linkedin-carousels-workspace.json
#       source/
#       brief.md
#       script.md
#       alt-text.md
#       style/               <- copied from styles/<chosen>/ at init
#       slides/              <- raw gpt-image-2-2026-04-21 PNGs (pre-export)
#       middle-art/          <- iteration / scratch images
#
# The .working/ dot prefix hides the folder in Finder by default so a
# non-technical operator opening the run sees only the deliverables.
WORKING_SUBDIR = ".working"
WORKSPACE_FILENAME = ".linkedin-carousels-workspace.json"

# Subdirectories INSIDE the run's .working/ folder.
WORKING_SUBDIRS = ["source", "style", "middle-art", "slides"]


def library_search_paths(kind: str) -> list[Path]:
    """Skill-default path first, project-local path second. Project wins on conflict."""
    return [SKILL_DIR / kind, REPO_ROOT / kind]


def parse_index(index_path: Path) -> dict[str, str]:
    """Parse a library's _index.md. Returns {name: description}.

    Line format: '- <name><separator><description>' where separator is one
    of ': ', ' - ', or ' — '. The first match wins. Empty descriptions are
    allowed.
    """
    if not index_path.exists():
        return {}
    entries: dict[str, str] = {}
    # First-match separator: colon-space, space-hyphen-space, space-em-dash-space.
    # Keeps em-dash compatibility for legacy files without making it the project standard.
    sep_re = re.compile(r":\s+|\s+-\s+|\s+—\s+")
    for line in index_path.read_text().splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        rest = line[2:].strip()
        match = sep_re.search(rest)
        if match:
            name = rest[:match.start()].strip()
            desc = rest[match.end():].strip()
        else:
            name = rest.strip()
            desc = ""
        if name:
            entries[name] = desc
    return entries


def list_library(kind: str) -> dict[str, tuple[str, Path]]:
    """Return {name: (description, source_dir)} for one library kind,
    merging skill-defaults and project-local entries. Project wins on conflict."""
    merged: dict[str, tuple[str, Path]] = {}
    for base in library_search_paths(kind):
        for name, desc in parse_index(base / "_index.md").items():
            merged[name] = (desc, base / name)
    return merged


def resolve_library_entry(kind: str, name: str) -> Path | None:
    """Return the directory for a library entry, project-local preferred. None if not found."""
    for base in reversed(library_search_paths(kind)):  # project first
        candidate = base / name
        if candidate.is_dir():
            return candidate
    return None


# Backwards-compatible thin wrapper used by older code paths in this script.
def list_available_styles() -> list[str]:
    return list(list_library("styles").keys())


def install_style_into_run(style_name: str, run_dir: Path) -> None:
    """Copy the chosen style's spec + prompt fragment into the run's
    .working/style/ folder."""
    style_src = resolve_library_entry("styles", style_name)
    if style_src is None:
        print(f"ERROR: style '{style_name}' has no folder under styles/ "
              f"(searched {' and '.join(str(p) for p in library_search_paths('styles'))}).",
              file=sys.stderr)
        sys.exit(1)
    style_dst = run_dir / WORKING_SUBDIR / "style"
    style_dst.mkdir(parents=True, exist_ok=True)
    for fname in ("style.md", "prompt-fragment.txt", "slide-templates.md",
                  "canonical-bg.txt"):
        src = style_src / fname
        if src.exists():
            shutil.copy(src, style_dst / fname)


def install_layout_into_run(layout_name: str, run_dir: Path) -> None:
    """Copy the chosen layout system's spec + prompt fragment into the run's
    .working/style/ folder. The layout's prompt-fragment.txt lands as
    layout-fragment.txt to avoid colliding with the style's prompt fragment."""
    layout_src = resolve_library_entry("layout-systems", layout_name)
    if layout_src is None:
        print(f"ERROR: layout-system '{layout_name}' has no folder under layout-systems/ "
              f"(searched {' and '.join(str(p) for p in library_search_paths('layout-systems'))}).",
              file=sys.stderr)
        sys.exit(1)
    layout_dst = run_dir / WORKING_SUBDIR / "style"
    layout_dst.mkdir(parents=True, exist_ok=True)
    spec_src = layout_src / "layout.md"
    if spec_src.exists():
        shutil.copy(spec_src, layout_dst / "layout.md")
    frag_src = layout_src / "prompt-fragment.txt"
    if frag_src.exists():
        shutil.copy(frag_src, layout_dst / "layout-fragment.txt")


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:50]


def ensure_brand(brand_key: str, allow_create: bool) -> Path:
    """Return the brand dir, creating it from template if --new-brand given."""
    brand_slug = slugify(brand_key)
    if not brand_slug:
        print("ERROR: --brand produced an empty slug.", file=sys.stderr)
        sys.exit(1)
    brand_dir = BRANDS_DIR / brand_slug
    brand_md = brand_dir / "brand.md"

    if brand_dir.exists() and brand_md.exists():
        return brand_dir

    if not allow_create:
        print(
            f"ERROR: brand '{brand_slug}' has no brand.md yet.\n"
            f"Re-run with --new-brand to create brands/{brand_slug}/ from the "
            "template, then fill in the brand voice + style before the style step.",
            file=sys.stderr,
        )
        sys.exit(1)

    # create it
    brand_dir.mkdir(parents=True, exist_ok=True)
    (brand_dir / "runs-index.md").write_text(
        f"# {brand_key} — carousel runs\n\nRuns for this brand live in the "
        "top-level `runs/` folder. This file is just a human index.\n"
    )
    if BRAND_TEMPLATE.exists():
        content = BRAND_TEMPLATE.read_text().replace("{{BRAND_NAME}}", brand_key)
        brand_md.write_text(content)
    else:
        brand_md.write_text(f"# Brand: {brand_key}\n\nTODO: define voice + style.\n")
    print(f"NEW BRAND: created brands/{brand_slug}/ — fill in brand.md before step 3.")
    return brand_dir


def build_workspace(topic, slug, brand_slug, platform, slides, run_rel,
                    style, voice, hook, pattern, layout, format_spec):
    now = datetime.datetime.now().isoformat(timespec="seconds")
    history_note = (
        f"run scaffolded for '{topic}' (brand: {brand_slug}"
        + (f", style: {style}" if style else "")
        + (f", voice: {voice}" if voice else "")
        + (f", hook: {hook}" if hook else "")
        + (f", pattern: {pattern}" if pattern else "")
        + (f", layout: {layout}" if layout else "")
        + f", format: {format_spec['name']} ({format_spec['width']}x{format_spec['height']})"
        + ")"
    )
    return {
        "topic": topic,
        "slug": slug,
        "brand": brand_slug,
        "run_path": run_rel,
        "platform": platform,
        "format": format_spec,
        "target_slides": slides,
        "status": "in_progress",
        "created_at": now,
        "updated_at": now,
        "source_type": None,
        "insight_count": None,
        "slide_count": None,
        "style_name": style,
        "voice_name": voice,
        "hook_name": hook,
        "pattern_name": pattern,
        "layout_system": layout,
        "comment_trigger_word": None,
        "steps": {
            "init": "done",
            "source": "pending",
            "script": "pending",
            "style": "done" if style else "pending",
            "layout": "done" if layout else "pending",
            "art": "pending",
            "export": "pending",
        },
        "images": {},
        "history": [{"step": "init", "at": now, "note": history_note}],
    }


def main():
    p = argparse.ArgumentParser(description="Initialize a carousel run.")
    p.add_argument("--topic", required=True, help="Short title for the carousel.")
    p.add_argument("--brand", required=True, help="Brand key (folder under brands/).")
    p.add_argument("--new-brand", action="store_true",
                   help="Allow creating the brand folder if it does not exist.")
    p.add_argument("--platform", choices=["linkedin", "instagram", "both"],
                   default="both")
    p.add_argument("--format", default=None, dest="format_name",
                   choices=list(__import__("state").FORMAT_PRESETS.keys()),
                   help="Output format preset: portrait (1080x1350, default), "
                        "square (1080x1080), landscape (1920x1080). Locked at "
                        "init time. If omitted, the orchestrator should ASK "
                        "the user (per the ask-first rule in SKILL.md) "
                        "before passing this flag.")
    p.add_argument("--slides", type=int, default=10,
                   help="Target slide count hint (8-12 recommended).")
    p.add_argument("--style", default=None,
                   help="Style name from styles/_index.md (or your project-local "
                        "styles/). Locks the visual style at init. Omit to pick "
                        "later in STEP 3.")
    p.add_argument("--voice", default=None,
                   help="Voice name from voices/_index.md (or your project-local "
                        "voices/). Locks the tone of the post + slide copy at init. "
                        "Omit to inherit the brand's default voice.")
    p.add_argument("--hook", default=None,
                   help="Hook archetype name from hooks/_index.md. Suggests the "
                        "slide-1/post-line-1 structure for STEP 2 (script). "
                        "Omit to pick during the script step.")
    p.add_argument("--pattern", default=None,
                   help="Post-body pattern name from post-patterns/_index.md. "
                        "Suggests the post body structure for STEP 2. Omit to "
                        "pick during the script step.")
    p.add_argument("--layout", default=None,
                   help="Layout-system name from layout-systems/_index.md. "
                        "Locks the compositional vocabulary for the run "
                        "(editorial-spread, dossier-stack, newspaper-column, "
                        "dispatch-bulletin, etc.). The layout system is the "
                        "RUN-LEVEL design grammar that sits inside the style "
                        "and tells the orchestrator how each slide's hero "
                        "zone should vary by function. Omit to pick during "
                        "STEP 3 based on the source content.")
    args = p.parse_args()

    if not 3 <= args.slides <= 20:
        print(f"ERROR: --slides must be 3-20 (got {args.slides}).", file=sys.stderr)
        sys.exit(1)

    # validate every library-backed flag against its registry.
    # Each flag is optional. Unknown values fail loudly with the available list.
    # Map library-kind names to the CLI flag they came from, so error
    # messages reference the right flag.
    kind_to_flag = {
        "styles": "--style",
        "voices": "--voice",
        "hooks": "--hook",
        "post-patterns": "--pattern",
        "layout-systems": "--layout",
    }

    def validate_flag(value: str | None, kind: str) -> str | None:
        if value is None:
            return None
        available = list_library(kind)
        if value not in available:
            flag = kind_to_flag.get(kind, f"--{kind}")
            print(f"ERROR: {flag} '{value}' is not registered.\n"
                  f"Available {kind}: "
                  f"{', '.join(available) or '(none)'}", file=sys.stderr)
            sys.exit(1)
        return value

    chosen_style = validate_flag(args.style, "styles")
    chosen_voice = validate_flag(args.voice, "voices")
    chosen_hook = validate_flag(args.hook, "hooks")
    chosen_pattern = validate_flag(args.pattern, "post-patterns")
    chosen_layout = validate_flag(args.layout, "layout-systems")

    # Resolve the format. If --format was passed, use it; else default to
    # portrait. The ask-first rule in SKILL.md says the orchestrator should
    # ask the user before relying on the default — but init.py itself stays
    # CLI-only and accepts the default without prompting.
    import state as state_mod
    chosen_format = state_mod.format_spec(args.format_name)

    brand_dir = ensure_brand(args.brand, args.new_brand)
    brand_slug = brand_dir.name

    slug = slugify(args.topic)
    if not slug:
        print("ERROR: --topic produced an empty slug.", file=sys.stderr)
        sys.exit(1)

    date_str = datetime.date.today().isoformat()
    run_name = f"{slug}-{date_str}"
    run_dir = RUNS_DIR / run_name
    run_rel = f"runs/{run_name}"
    working_dir = run_dir / WORKING_SUBDIR
    workspace_file = working_dir / WORKSPACE_FILENAME

    # resume-safety: never clobber an existing run
    if run_dir.exists():
        if workspace_file.exists():
            print(f"NOTICE: run already exists at {run_rel}")
            print("Do NOT re-init. Read its workspace JSON and resume from the")
            print("first step that is not 'done'.")
            print("--- workspace ---")
            print(workspace_file.read_text())
            sys.exit(0)
        # Backwards-compat: legacy runs kept the workspace JSON at the run root.
        legacy_workspace = run_dir / WORKSPACE_FILENAME
        if legacy_workspace.exists():
            print(f"NOTICE: run already exists at {run_rel} in LEGACY layout.")
            print("Migrate it with: python scripts/migrate-run.py --run "
                  f"{run_rel}")
            sys.exit(0)
        print(f"ERROR: {run_rel} exists but has no workspace JSON. Inspect manually.",
              file=sys.stderr)
        sys.exit(1)

    # Build the tree. Root stays empty (deliverables land there at export
    # time); everything pipeline-internal goes into .working/.
    run_dir.mkdir(parents=True)
    working_dir.mkdir()
    for sub in WORKING_SUBDIRS:
        d = working_dir / sub
        d.mkdir()
        (d / ".gitkeep").touch()

    workspace = build_workspace(args.topic, slug, brand_slug, args.platform,
                                args.slides, run_rel,
                                chosen_style, chosen_voice, chosen_hook, chosen_pattern,
                                chosen_layout, chosen_format)
    workspace_file.write_text(json.dumps(workspace, indent=2))

    # if a style was chosen, copy its files into .working/style/
    if chosen_style:
        install_style_into_run(chosen_style, run_dir)

    # if a layout system was chosen, copy its files into .working/style/ too
    # (the layout fragment lands as layout-fragment.txt alongside the style's
    # prompt-fragment.txt — generate.py callers concatenate both)
    if chosen_layout:
        install_layout_into_run(chosen_layout, run_dir)

    # human-readable breadcrumbs INSIDE .working/ (not at the run root,
    # because the run root is reserved for end-user deliverables).
    (working_dir / "brief.md").write_text(
        f"# Brief: {args.topic}\n\n_Filled in during STEP 1 (source)._\n"
    )
    (working_dir / "README.md").write_text(
        f"# Carousel run: {args.topic}\n\n"
        f"- Brand: `{brand_slug}`\n- Slug: `{slug}`\n"
        f"- Platform: {args.platform}\n- Target slides: {args.slides}\n"
        f"- Style: `{chosen_style or '(not yet chosen)'}`\n"
        f"- Voice: `{chosen_voice or '(brand default)'}`\n"
        f"- Hook: `{chosen_hook or '(pick during script step)'}`\n"
        f"- Pattern: `{chosen_pattern or '(pick during script step)'}`\n"
        f"- Layout: `{chosen_layout or '(pick during STEP 3)'}`\n"
        f"- Created: {date_str}\n\n"
        f"State lives in `{WORKSPACE_FILENAME}` inside this folder. The run "
        f"root (one level up) is reserved for the final deliverables that "
        f"land there at export time.\n"
    )

    print(f"OK: run initialized at {run_rel}")
    print(f"Brand: brands/{brand_slug}/")
    print(f"Format: {chosen_format['name']} "
          f"({chosen_format['width']}x{chosen_format['height']}, "
          f"source {chosen_format['source_size']})")
    for label, picked, kind in (
        ("Style", chosen_style, "styles"),
        ("Voice", chosen_voice, "voices"),
        ("Hook", chosen_hook, "hooks"),
        ("Pattern", chosen_pattern, "post-patterns"),
        ("Layout", chosen_layout, "layout-systems"),
    ):
        if picked:
            print(f"{label}: {picked} (locked)")
        else:
            avail = ", ".join(list_library(kind).keys()) or "(none registered)"
            print(f"{label}: (not chosen — available: {avail})")
    print(f".working/ subfolders: {', '.join(WORKING_SUBDIRS)}")
    print(f"(deliverables land at the run root at export time)")
    print(f"--- {WORKSPACE_FILENAME} ---")
    print(workspace_file.read_text())
    print("--- NEXT ---")
    print("STEP 1 (source): put source material in source/source.md, then write "
          "source/insights.md and brief.md. Update the workspace file when done.")


if __name__ == "__main__":
    main()
