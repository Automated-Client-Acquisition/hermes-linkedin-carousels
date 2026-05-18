#!/usr/bin/env python3
"""
list.py — discovery command. Prints every available library entry across
styles, voices, hooks, post-patterns, and layout-systems.

This is the first command a new user should run after installing the
skill into their project. It shows them what they can pick from when
calling init.py, and where each entry came from (skill default vs
project-local).

Usage:
    python .claude/skills/linkedin-carousels/scripts/list.py

    # Filter to one kind
    python .claude/skills/linkedin-carousels/scripts/list.py styles

    # Show details for one entry
    python .claude/skills/linkedin-carousels/scripts/list.py styles aca
"""
import sys
from pathlib import Path

# import the shared library helpers from init.py to avoid duplicating logic.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from init import LIBRARY_KINDS, library_search_paths, parse_index, SKILL_DIR, REPO_ROOT


def fmt_source(source_dir: Path) -> str:
    """Return 'skill' or 'project' depending on which tier the entry came from."""
    try:
        source_dir.relative_to(SKILL_DIR)
        return "skill"
    except ValueError:
        pass
    try:
        source_dir.relative_to(REPO_ROOT)
        return "project"
    except ValueError:
        return "unknown"


def list_kind(kind: str) -> None:
    """Print all entries for one library kind, with source tier and description."""
    print(f"\n## {kind}")
    skill_path, project_path = library_search_paths(kind)
    merged: dict[str, tuple[str, str]] = {}
    for base, tier in ((skill_path, "skill"), (project_path, "project")):
        for name, desc in parse_index(base / "_index.md").items():
            # project-local entries shadow skill defaults on name conflict
            merged[name] = (desc, tier)
    if not merged:
        print(f"  (no entries registered. Check {skill_path}/_index.md or "
              f"add to {project_path}/_index.md.)")
        return
    name_w = max(len(n) for n in merged) + 2
    for name in sorted(merged):
        desc, tier = merged[name]
        tier_tag = f"[{tier}]"
        print(f"  {name:<{name_w}} {tier_tag:<10} {desc}")


def show_entry(kind: str, name: str) -> None:
    """Print the spec file for one entry."""
    for base in library_search_paths(kind):
        entry_dir = base / name
        if entry_dir.is_dir():
            # Find the main spec file. Convention varies by kind.
            for candidate in (f"{kind.rstrip('s')}.md", "style.md", "voice.md",
                              "hook.md", "pattern.md", "diagram.md"):
                spec = entry_dir / candidate
                if spec.exists():
                    print(f"# {kind}/{name} (from {fmt_source(entry_dir)})")
                    print(f"# Source: {spec}")
                    print()
                    print(spec.read_text())
                    return
            print(f"ERROR: entry exists but no spec file found in {entry_dir}",
                  file=sys.stderr)
            sys.exit(1)
    print(f"ERROR: no entry '{name}' in {kind}/. "
          f"Run `list.py {kind}` to see what's available.", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    args = sys.argv[1:]

    if not args:
        # No args: print everything.
        print("# linkedin-carousels library inventory")
        print(f"# Skill defaults: {SKILL_DIR}")
        print(f"# Project root:   {REPO_ROOT}")
        print(f"# Entries marked [project] come from your project root and "
              f"shadow skill defaults on name conflict.")
        for kind in LIBRARY_KINDS:
            list_kind(kind)
        print()
        return

    kind = args[0]
    if kind not in LIBRARY_KINDS:
        print(f"ERROR: '{kind}' is not a library kind. "
              f"Available: {', '.join(LIBRARY_KINDS)}", file=sys.stderr)
        sys.exit(1)

    if len(args) == 1:
        list_kind(kind)
        return

    if len(args) == 2:
        show_entry(kind, args[1])
        return

    print(f"Usage: {sys.argv[0]} [<kind>] [<name>]", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
