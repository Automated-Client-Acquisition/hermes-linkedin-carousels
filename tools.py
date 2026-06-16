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


def _profile_dir(profile_name: str) -> Path:
    return Path.home() / ".hermes" / "profiles" / profile_name


def _config_has_plugin(profile_name: str, plugin_name: str) -> bool:
    cfg = _profile_dir(profile_name) / "config.yaml"
    return cfg.exists() and plugin_name in cfg.read_text(errors="ignore")


def _run_hermes(cmd: list[str], timeout: int = 30) -> dict[str, Any]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    except Exception as e:
        return {"returncode": -1, "stdout": "", "stderr": str(e)}


def _enable_profile_plugin(profile_name: str, plugin_name: str) -> list[str]:
    results = []
    create = _run_hermes(["hermes", "profile", "create", profile_name])
    msg = (create.get("stdout", "") + create.get("stderr", "")).lower()
    if create["returncode"] == 0:
        results.append(f"created profile: {profile_name}")
    elif "already exists" in msg:
        results.append(f"profile already exists: {profile_name}")
    else:
        results.append(f"profile create warning: {(create['stderr'] or create['stdout'])[:160]}")
    pdir = _profile_dir(profile_name)
    pdir.mkdir(parents=True, exist_ok=True)
    enable = _run_hermes(["hermes", "-p", profile_name, "plugins", "enable", plugin_name])
    if enable["returncode"] == 0 or _config_has_plugin(profile_name, plugin_name):
        results.append(f"enabled root-level plugin on profile: {plugin_name}")
    else:
        shared = Path.home()/'.hermes'/'plugins'/plugin_name
        local = pdir/'plugins'
        local.mkdir(parents=True, exist_ok=True)
        link = local/plugin_name
        try:
            if shared.exists() and not link.exists():
                link.symlink_to(shared, target_is_directory=True)
                results.append("profile-local symlink created for plugin discovery")
            enable2 = _run_hermes(["hermes", "-p", profile_name, "plugins", "enable", plugin_name])
            results.append("enabled after symlink" if enable2["returncode"] == 0 else f"enable warning: {(enable2['stderr'] or enable2['stdout'])[:160]}")
        except Exception as e:
            results.append(f"enable fallback warning: {e}")
    return results


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
    """Load the workspace JSON for a run."""
    run = Path(run_path)
    for candidate in (run / ".working" / ".linkedin-carousels-workspace.json",
                      run / ".linkedin-carousels-workspace.json"):
        if candidate.exists():
            try:
                return json.loads(candidate.read_text())
            except json.JSONDecodeError:
                return None
    return None


def carousel_setup_profile(args: dict, **_kwargs) -> str:
    try:
        profile_name = args.get("profile_name", "carousel-bot")
        project_root = Path(args.get("project_root") or (Path.home()/"carousel-projects"/"default")).expanduser()
        brand = args.get("brand", "default")
        for d in [project_root, project_root/"brands"/brand, project_root/"runs", project_root/"styles", project_root/"voices"]:
            d.mkdir(parents=True, exist_ok=True)
        results = _enable_profile_plugin(profile_name, "linkedin-carousels")
        pdir = _profile_dir(profile_name)
        soul = f"""# Carousel Operator

## Identity
You are the dedicated carousel production operator. The linkedin-carousels plugin code lives at root level in `~/.hermes/plugins/linkedin-carousels`; this profile only enables and uses it.

## Defaults
- Project root: {project_root}
- Brand: {brand}

## Operating Rules
- Ask before generating slide 1 because image generation costs money.
- Always run carousel_list before asking style questions.
- Save every run under the project root.
- Deliver PDF, PNGs, post-copy.txt, and CHECKLIST.md.

## First Live Commands
- `Run carousel_status`
- `Run carousel_smoke_test`
- `Make a carousel from this URL and ask before generating slide 1`
"""
        (pdir/"SOUL.md").write_text(soul)
        results.append("SOUL.md written")
        return json.dumps({"ok": True, "profile_name": profile_name, "project_root": str(project_root), "brand": brand, "setup_summary": results, "next_action": "Run carousel_status, then carousel_smoke_test before paid image generation."})
    except Exception as e:
        return _err(f"carousel_setup_profile failed: {e}", traceback=traceback.format_exc())


def carousel_status(args: dict, **_kwargs) -> str:
    try:
        profile_name = args.get("profile_name", "carousel-bot")
        project_root = Path(args.get("project_root") or (Path.home()/"carousel-projects"/"default")).expanduser()
        pdir = _profile_dir(profile_name)
        checks = {
            "root_level_plugin_exists": (Path.home()/'.hermes'/'plugins'/'linkedin-carousels').exists(),
            "profile_exists": pdir.exists(),
            "plugin_enabled_on_profile": _config_has_plugin(profile_name, "linkedin-carousels"),
            "soul_exists": (pdir/'SOUL.md').exists(),
            "project_root_exists": project_root.exists(),
            "brands_dir_exists": (project_root/'brands').exists(),
            "runs_dir_exists": (project_root/'runs').exists(),
        }
        missing = [k for k,v in checks.items() if not v]
        return json.dumps({"ok": True, "profile_name": profile_name, "project_root": str(project_root), "checks": checks, "ready": not missing, "missing": missing, "next_action": "Run carousel_setup_profile" if missing else "Run carousel_smoke_test, then initialize one carousel run."})
    except Exception as e:
        return _err(f"carousel_status failed: {e}", traceback=traceback.format_exc())


def carousel_smoke_test(args: dict, **_kwargs) -> str:
    try:
        project_root = Path(args.get("project_root") or (Path.home()/"carousel-projects"/"default")).expanduser()
        reports = project_root/"reports"
        reports.mkdir(parents=True, exist_ok=True)
        status_payload = json.loads(carousel_status(args))
        report = reports/"smoke-test.json"
        report.write_text(json.dumps(status_payload, indent=2))
        return json.dumps({"ok": True, "paid_calls": False, "side_effects": ["created/updated local smoke-test report only"], "saved_to": str(report), "ready": status_payload.get("ready", False), "next_action": status_payload.get("next_action")})
    except Exception as e:
        return _err(f"carousel_smoke_test failed: {e}", traceback=traceback.format_exc())


def carousel_init(args: dict, **_kwargs) -> str:
    try:
        if not args.get("project_root"):
            return _err("Missing required parameter: project_root")
        if not args.get("topic"):
            return _err("Missing required parameter: topic")
        if not args.get("brand"):
            return _err("Missing required parameter: brand")

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

        result = _run_script("init.py", cli_args, args["project_root"])
        run_path = None
        for line in result["stdout"].splitlines():
            if line.startswith("OK: run initialized at "):
                run_path = str(Path(args["project_root"]) / line[len("OK: run initialized at "):].strip())
                break
            if line.startswith("NOTICE: run already exists at "):
                run_path = str(Path(args["project_root"]) / line[len("NOTICE: run already exists at "):].strip())
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
        return json.dumps(_run_script("list.py", cli_args, args.get("project_root")))
    except Exception as e:
        return _err(f"carousel_list failed: {e}", traceback=traceback.format_exc())


def carousel_state(args: dict, **_kwargs) -> str:
    try:
        if not args.get("run_path"):
            return _err("Missing required parameter: run_path")
        workspace = _read_workspace(args["run_path"])
        if workspace is None:
            return _err("Workspace not found for this run_path")
        return json.dumps({"ok": True, "workspace": workspace})
    except Exception as e:
        return _err(f"carousel_state failed: {e}", traceback=traceback.format_exc())


def carousel_generate_slide(args: dict, **_kwargs) -> str:
    try:
        # Input validation
        if not args.get("run_path"):
            return _err("Missing required parameter: run_path")
        if args.get("slide") is None:
            return _err("Missing required parameter: slide")
        if not args.get("prompt"):
            return _err("Missing required parameter: prompt")

        # Cost warning - require explicit confirmation
        if not args.get("force"):
            return json.dumps({
                "ok": False,
                "warning": "Image generation costs ~$0.08 per slide. Set force=true to proceed.",
                "cost_estimate": 0.08
            })

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
        if not args.get("run_path"):
            return _err("Missing required parameter: run_path")

        cli_args = ["--run", args["run_path"]]
        project_root = str(Path(args["run_path"]).resolve().parents[1])
        result = _run_script("export.py", cli_args, project_root)
        result["workspace"] = _read_workspace(args["run_path"])
        return json.dumps(result)
    except Exception as e:
        return _err(f"carousel_export failed: {e}", traceback=traceback.format_exc())


HANDLERS = {
    "carousel_setup_profile": carousel_setup_profile,
    "carousel_status": carousel_status,
    "carousel_smoke_test": carousel_smoke_test,
    "carousel_init": carousel_init,
    "carousel_list": carousel_list,
    "carousel_state": carousel_state,
    "carousel_generate_slide": carousel_generate_slide,
    "carousel_export": carousel_export,
}