#!/usr/bin/env python3
"""
state.py — shared workspace-file helpers used by generate.py and export.py.

The workspace file (.linkedin-carousels-workspace.json) lives inside each
run's .working/ subfolder. It is the single source of truth for what has
been done. Always load it before acting, always save it after.

Legacy runs kept the workspace file at the run root. The loader checks
the new location first, then falls back to the root location, so existing
runs continue to work until they're migrated.
"""
import datetime
import json
from pathlib import Path

WORKSPACE_FILENAME = ".linkedin-carousels-workspace.json"
WORKING_SUBDIR = ".working"

# Format presets. Each preset names the final export dimensions and the
# best matching gpt-image-2-2026-04-21 source size (the model only supports three:
# 1024x1024, 1024x1536, 1536x1024).
#
# Locked at init time via --format. Stored in the workspace JSON under
# 'format' so generate.py and export.py read from one source of truth.
# Adding a new preset = add a key here.
FORMAT_PRESETS = {
    "portrait": {
        "width": 1080,
        "height": 1350,
        "source_size": "1024x1536",
        "aspect": "4:5",
        "note": "LinkedIn + Instagram carousel default. Works on both.",
    },
    "square": {
        "width": 1080,
        "height": 1080,
        "source_size": "1024x1024",
        "aspect": "1:1",
        "note": "Square. Works on Instagram and LinkedIn. Older feed standard.",
    },
    "landscape": {
        "width": 1920,
        "height": 1080,
        "source_size": "1536x1024",
        "aspect": "16:9",
        "note": "LinkedIn landscape carousels and presentation-style slides.",
    },
}
DEFAULT_FORMAT = "portrait"


def format_spec(name: str | None) -> dict:
    """Return the format spec for a preset name. Falls back to DEFAULT_FORMAT
    when name is None or unknown — keeps legacy runs working."""
    if name and name in FORMAT_PRESETS:
        return {"name": name, **FORMAT_PRESETS[name]}
    return {"name": DEFAULT_FORMAT, **FORMAT_PRESETS[DEFAULT_FORMAT]}


class StateError(Exception):
    pass


def _workspace_path(run_dir) -> Path:
    """Resolve the workspace file. New layout first, legacy fallback second."""
    run = Path(run_dir)
    new = run / WORKING_SUBDIR / WORKSPACE_FILENAME
    if new.exists():
        return new
    legacy = run / WORKSPACE_FILENAME
    if legacy.exists():
        return legacy
    # Default to the new path so future writes land in the right place.
    return new


def load(run_dir) -> dict:
    """Load the workspace file for a run. Raises StateError if missing/corrupt."""
    wp = _workspace_path(run_dir)
    if not wp.exists():
        raise StateError(
            f"No workspace file at {wp}. Run init.py first — the pipeline "
            "cannot proceed without run state."
        )
    try:
        return json.loads(wp.read_text())
    except json.JSONDecodeError as e:
        raise StateError(f"Workspace file at {wp} is corrupt: {e}")


def save(run_dir, state: dict) -> None:
    """Write the workspace file back, refreshing updated_at."""
    state["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    wp = _workspace_path(run_dir)
    wp.parent.mkdir(parents=True, exist_ok=True)
    wp.write_text(json.dumps(state, indent=2))


def log(state: dict, step: str, note: str) -> None:
    """Append a history breadcrumb (does not save)."""
    state.setdefault("history", []).append(
        {
            "step": step,
            "at": datetime.datetime.now().isoformat(timespec="seconds"),
            "note": note,
        }
    )


def require_step_done(state: dict, step: str) -> None:
    """Guard: ensure a prerequisite step is complete before proceeding."""
    status = state.get("steps", {}).get(step)
    if status != "done":
        raise StateError(
            f"Prerequisite step '{step}' is '{status}', not 'done'. "
            "Complete earlier pipeline steps first."
        )
