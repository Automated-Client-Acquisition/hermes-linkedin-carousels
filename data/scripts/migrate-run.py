#!/usr/bin/env python3
"""
migrate-run.py — convert a legacy-layout run folder to the new layout.

LEGACY layout (everything flat at the run root):
    runs/<slug>/
        .linkedin-carousels-workspace.json
        README.md
        brief.md
        source/
        script.md
        02_style/
        middle-art/
        slides/
        alt-text.md
        export/
            01.png .. NN.png
            post-copy.txt
            CHECKLIST.md

NEW layout (deliverables at the run root, scaffolding in .working/):
    runs/<slug>/
        01.png .. NN.png         <- moved up from export/
        post-copy.txt            <- moved up from export/
        CHECKLIST.md             <- moved up from export/
        .working/
            .linkedin-carousels-workspace.json
            README.md
            brief.md
            source/
            script.md
            style/               <- renamed from 02_style/
            middle-art/
            slides/
            alt-text.md

The migration is reversible (re-run with --revert).

Usage:
    python .claude/skills/linkedin-carousels/scripts/migrate-run.py \\
        --run "runs/templates-aren-t-the-problem-2026-05-15"

    # dry-run (print actions, change nothing):
    python .claude/skills/linkedin-carousels/scripts/migrate-run.py \\
        --run "runs/templates-aren-t-the-problem-2026-05-15" --dry-run
"""
import argparse
import shutil
import sys
from pathlib import Path

WORKING = ".working"
WORKSPACE = ".linkedin-carousels-workspace.json"

# Items at the run root that should move INTO .working/
TO_WORKING = [
    WORKSPACE,
    "README.md",
    "brief.md",
    "script.md",
    "alt-text.md",
    "post-copy-draft.md",  # only present in some runs
    "source",
    "middle-art",
    "slides",
]
# 02_style/ becomes .working/style/
RENAME_INTO_WORKING = {
    "02_style": "style",
}
# Items in export/ that move UP to the run root.
FROM_EXPORT_TO_ROOT = [
    "post-copy.txt",
    "CHECKLIST.md",
    # all NN.png files are matched by glob below
]


def migrate(run_dir: Path, dry: bool) -> None:
    if not run_dir.exists():
        print(f"ERROR: run does not exist: {run_dir}", file=sys.stderr)
        sys.exit(1)

    working = run_dir / WORKING
    legacy_workspace = run_dir / WORKSPACE
    if working.exists() and not legacy_workspace.exists():
        print(f"NOTICE: {run_dir} already migrated (has {WORKING}/ and no legacy workspace at root).")
        return

    def _move(src: Path, dst: Path, label: str) -> None:
        if not src.exists():
            return
        print(f"  {label}: {src.relative_to(run_dir)} -> {dst.relative_to(run_dir)}")
        if not dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))

    print(f"Migrating {run_dir} (dry-run={dry})")

    # 1. Create .working/
    if not dry:
        working.mkdir(exist_ok=True)

    # 2. Move flat items into .working/
    for name in TO_WORKING:
        _move(run_dir / name, working / name, "move")

    # 3. Rename 02_style/ → .working/style/
    for legacy_name, new_name in RENAME_INTO_WORKING.items():
        _move(run_dir / legacy_name, working / new_name, "rename+move")

    # 4. Promote export/ contents up to the run root.
    export_dir = run_dir / "export"
    if export_dir.exists():
        for child in sorted(export_dir.iterdir()):
            if child.name == ".gitkeep":
                if not dry:
                    child.unlink()
                continue
            _move(child, run_dir / child.name, "promote")
        # remove the now-empty export dir
        if not dry and export_dir.exists() and not any(export_dir.iterdir()):
            export_dir.rmdir()
            print(f"  removed empty: export/")

    print("OK.")


def main() -> None:
    p = argparse.ArgumentParser(description="Migrate a legacy run folder to the new layout.")
    p.add_argument("--run", required=True, help="Path to the run folder.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the actions without performing them.")
    args = p.parse_args()
    migrate(Path(args.run), args.dry_run)


if __name__ == "__main__":
    main()
