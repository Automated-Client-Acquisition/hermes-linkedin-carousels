"""Tool handlers for the linkedin-carousels Hermes plugin.

Per the Hermes build-a-plugin guide, every handler:
  - Has signature `(args: dict, **kwargs) -> str`.
  - Returns a JSON-serialized string ALWAYS, including on error.
  - Never raises — exceptions are caught and returned as error JSON.

Handlers wrap the bundled scripts in `data/scripts/` by shelling out with
the right env vars. The scripts already encode the pipeline logic,
idempotency, and workspace-JSON discipline.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any

PLUGIN_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = PLUGIN_DIR / "data" / "scripts"


def _err(message: str, **extra: Any) -> str:
    """Serialize a structured error response."""
    payload = {"ok": False, "error": message}
    payload.update(extra)
    return json.dumps(payload)


def _run_script(script_name: str, args: list[str], project_root: str | None,
                cwd: str | None = None) -> dict[str, Any]:
    """Invoke one of the bundled scripts and capture its output as a dict."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        return {
            "ok": False,
            "stdout": "",
            "stderr": f"script not found: {script_path}",
            "returncode": -1,
        }
    env = os.environ.copy()
    if project_root:
        env["CAROUSELS_PROJECT_ROOT"] = project_root
        env["CAROUSELS_SKILL_DIR"] = str(PLUGIN_DIR / "data")
    proc = subprocess.run(
        [sys.executable, str(script_path), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd or project_root or os.getcwd(),
    )
    return {
        "ok": proc.returncode == 0,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "returncode": proc.returncode,
    }


def _read_workspace(run_path: str) -> dict[str, Any] | None:
    """Load the workspace JSON for a run. Honors new .working/ + legacy layouts."""
    run = Path(run_path)
    for candidate in (run / ".working" / ".linkedin-carousels-workspace.json",
                      run / ".linkedin-carousels-workspace.json"):
        if candidate.exists():
            try:
                return json.loads(candidate.read_text())
            except json.JSONDecodeError:
                return None
    return None


def carousel_init(args: dict, **_kwargs) -> str:
    try:
        project_root = args["project_root"]
        cli_args = ["--topic", args["topic"], "--brand", args["brand"]]
        if args.get("new_brand"):
            cli_args.append("--new-brand")
        if args.get("platform"):
            cli_args += ["--platform", args["platform"]]
        if args.get("format"):
            cli_args += ["--format", args["format"]]
        if args.get("slides") is not None:
            cli_args += ["--slides", str(args["slides"])]
        for flag in ("style", "voice", "hook", "pattern", "layout"):
            if args.get(flag):
                cli_args += [f"--{flag}", args[flag]]

        result = _run_script("init.py", cli_args, project_root)
        run_path = None
        for line in result["stdout"].splitlines():
            if line.startswith("OK: run initialized at "):
                run_path = str(Path(project_root) / line[len("OK: run initialized at "):].strip())
                break
            if line.startswith("NOTICE: run already exists at "):
                run_path = str(Path(project_root) / line[len("NOTICE: run already exists at "):].strip())
                break
        workspace = _read_workspace(run_path) if run_path else None
        return json.dumps({**result, "run_path": run_path, "workspace": workspace})
    except Exception as e:
        return _err(f"carousel_init failed: {e}", traceback=traceback.format_exc())


def carousel_list(args: dict, **_kwargs) -> str:
    try:
        cli_args = []
        if args.get("kind"):
            cli_args.append(args["kind"])
        if args.get("name"):
            cli_args.append(args["name"])
        return json.dumps(_run_script("list.py", cli_args, args["project_root"]))
    except Exception as e:
        return _err(f"carousel_list failed: {e}", traceback=traceback.format_exc())


def carousel_state(args: dict, **_kwargs) -> str:
    try:
        ws = _read_workspace(args["run_path"])
        if ws is None:
            return _err(f"no workspace JSON found under {args['run_path']}")
        return json.dumps({"ok": True, "workspace": ws})
    except Exception as e:
        return _err(f"carousel_state failed: {e}", traceback=traceback.format_exc())


def carousel_generate_slide(args: dict, **_kwargs) -> str:
    try:
        cli_args = [
            "--run", args["run_path"],
            "--slide", str(args["slide"]),
            "--prompt", args["prompt"],
        ]
        if args.get("reference"):
            cli_args += ["--reference", args["reference"]]
        if args.get("previous_response_id"):
            cli_args += ["--previous-response-id", args["previous_response_id"]]
        if args.get("no_chain"):
            cli_args.append("--no-chain")
        if args.get("size"):
            cli_args += ["--size", args["size"]]
        if args.get("force"):
            cli_args.append("--force")
        project_root = str(Path(args["run_path"]).resolve().parents[1])
        return json.dumps(_run_script("generate.py", cli_args, project_root))
    except Exception as e:
        return _err(f"carousel_generate_slide failed: {e}", traceback=traceback.format_exc())


def carousel_export(args: dict, **_kwargs) -> str:
    try:
        cli_args = ["--run", args["run_path"]]
        project_root = str(Path(args["run_path"]).resolve().parents[1])
        result = _run_script("export.py", cli_args, project_root)
        result["workspace"] = _read_workspace(args["run_path"])
        return json.dumps(result)
    except Exception as e:
        return _err(f"carousel_export failed: {e}", traceback=traceback.format_exc())


HANDLERS = {
    "carousel_init": carousel_init,
    "carousel_list": carousel_list,
    "carousel_state": carousel_state,
    "carousel_generate_slide": carousel_generate_slide,
    "carousel_export": carousel_export,
}
