#!/usr/bin/env python3
"""
generate.py — STEP 4 of the linkedin-carousels pipeline.

Generates ONE slide image via OpenAI Responses API (gpt-5.5 + image_generation tool)
and saves it into the run's .working/slides/ folder. Idempotent: skips existing
slides unless --force.

Usage:
    python scripts/generate.py \
        --run "runs/on-page-aeo-2026-05-14" --slide 1 \
        --prompt "The full prompt: visual note + layout fragment + style fragment"

    # With a reference image for style anchoring:
    python scripts/generate.py \
        --run "runs/on-page-aeo-2026-05-14" --slide 2 \
        --prompt "..." --reference ".working/slides/slide-01.png"

    # Force regenerate an existing slide:
    python scripts/generate.py \
        --run "runs/on-page-aeo-2026-05-14" --slide 1 \
        --prompt "..." --force

Auto-chaining: by default, reads the workspace to find the previous slide's
response_id and chains via `previous_response_id` for visual consistency.
Use --no-chain to disable, or --previous-response-id to chain off a specific id.
"""
import argparse
import base64
import datetime
import json
import os
import re
import sys
import time
from pathlib import Path

# Path model consistent with init.py / list.py / state.py.
SKILL_DIR = Path(os.environ.get("CAROUSELS_SKILL_DIR")
                 or Path(__file__).resolve().parent.parent)
REPO_ROOT = Path(os.environ.get("CAROUSELS_PROJECT_ROOT")
                 or SKILL_DIR.parent.parent.parent)

# Import shared state helpers from the same directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import state as state_mod

WORKING_SUBDIR = ".working"


# ---- OpenAI client ----

def get_client():
    """Return an OpenAI client, reading OPENAI_API_KEY from env or .env."""
    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("openai package not installed. Run: pip install openai")

    import os as _os
    api_key = _os.getenv("OPENAI_API_KEY")

    if not api_key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = _os.getenv("OPENAI_API_KEY")
        except ImportError:
            pass

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in environment or .env file")

    return OpenAI(api_key=api_key)


# ---- Helpers ----

def _resolve_slide_path(run_dir: Path, slide_num: int) -> Path:
    """Return path to .working/slides/slide-NN.png for the run."""
    return run_dir / WORKING_SUBDIR / "slides" / f"slide-{slide_num:02d}.png"


def _resolve_reference(ref_spec: str, run_dir: Path) -> Path | None:
    """Resolve a --reference value. Absolute paths used directly;
    relative paths resolved against the run_dir."""
    if not ref_spec:
        return None
    p = Path(ref_spec)
    if p.is_absolute():
        return p if p.exists() else None
    return (run_dir / p) if (run_dir / p).exists() else None


def _upload_reference(client, ref_path: Path) -> str | None:
    """Upload a reference image via the Files API and return the file ID.
    Returns None if upload fails."""
    try:
        with open(ref_path, "rb") as f:
            file_obj = client.files.create(file=f, purpose="vision")
        return file_obj.id
    except Exception as exc:
        print(f"WARNING: could not upload reference {ref_path}: {exc}",
              file=sys.stderr)
        return None


def _extract_image(response) -> str | None:
    """Extract base64 image data from a Responses API response output."""
    for output in response.output:
        if getattr(output, "type", None) == "image_generation_call":
            return output.result
    return None


def _save_image(b64_data: str, dst: Path) -> None:
    """Decode base64 image and save to dst. Creates parent dirs if needed."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Remove data URL prefix if present
    if b64_data.startswith("data:"):
        # data:image/png;base64,iVBOR...
        b64_data = b64_data.split(",", 1)[1]
    dst.write_bytes(base64.b64decode(b64_data))


def _get_previous_response_id(ws: dict, slide_num: int) -> str | None:
    """Find the response_id of the previous slide in the workspace."""
    images = ws.get("images", {})
    # Try slide-{N-1:02d} then raw integers 0-(N-1)
    prev_key = f"slide_{(slide_num - 1):02d}"
    prev = images.get(prev_key, {})
    if isinstance(prev, dict):
        return prev.get("response_id")
    # Backward compat: check if images values may be strings "done"
    return None


# ---- Main generation ----

def generate_slide(
    run_dir: Path,
    slide_num: int,
    prompt: str,
    *,
    reference: str | None = None,
    previous_response_id: str | None = None,
    no_chain: bool = False,
    size: str | None = None,
    force: bool = False,
    client=None,
) -> dict:
    """
    Generate one slide image. Returns a result dict:
        {ok, path, response_id, cached}
    """
    ws = state_mod.load(run_dir)

    # Resolve size from workspace format if not explicit
    if not size:
        fmt = ws.get("format", {})
        size = fmt.get("source_size", "1024x1536")
        # Validate size is one of the three allowed
        if size not in ("1024x1024", "1024x1536", "1536x1024"):
            size = "1024x1536"

    # Idempotency check
    slide_path = _resolve_slide_path(run_dir, slide_num)
    if slide_path.exists() and not force:
        print(f"  slide-{slide_num:02d}.png already exists — skipping (use --force to regenerate)",
              file=sys.stderr)
        return {
            "ok": True,
            "path": str(slide_path),
            "response_id": None,
            "cached": True,
        }

    # Client
    if client is None:
        client = get_client()

    # Reference image
    ref_file_id = None
    if reference:
        ref_path = _resolve_reference(reference, run_dir)
        if ref_path and ref_path.exists():
            ref_file_id = _upload_reference(client, ref_path)
            print(f"  reference: {ref_path} (file_id={ref_file_id})", file=sys.stderr)
        else:
            print(f"WARNING: reference image not found: {reference}", file=sys.stderr)

    # Chaining: resolve previous_response_id
    chain_id = previous_response_id
    if not chain_id and not no_chain:
        chain_id = _get_previous_response_id(ws, slide_num)
    if chain_id:
        print(f"  chaining from response_id: {chain_id}", file=sys.stderr)

    # Build Responses API call
    kwargs = {
        "model": "gpt-5.5",
        "input": prompt,
        "tools": [{"type": "image_generation", "size": size}],
    }
    if chain_id:
        kwargs["previous_response_id"] = chain_id

    # If we have a reference but can't pass file_id directly in input for image_generation,
    # prepend a vision message with the reference
    if ref_file_id:
        kwargs["input"] = [
            {
                "role": "user",
                "content": [
                    {"type": "input_image", "file_id": ref_file_id, "detail": "high"},
                ],
            },
            {
                "role": "user",
                "content": f"Using the style reference above, generate: {prompt}",
            },
        ]

    # Generate
    print(f"  generating slide {slide_num} ({size})...", file=sys.stderr)
    try:
        response = client.responses.create(**kwargs)
    except Exception as exc:
        return {
            "ok": False,
            "error": f"API call failed: {exc}",
            "response_id": None,
        }

    # Extract image
    b64_data = _extract_image(response)
    if not b64_data:
        return {
            "ok": False,
            "error": "Response did not contain an image_generation_call output",
            "response_id": response.id,
        }

    # Save
    _save_image(b64_data, slide_path)
    print(f"  saved: {slide_path} ({slide_path.stat().st_size} bytes)", file=sys.stderr)

    # Update workspace
    now = datetime.datetime.now().isoformat(timespec="seconds")
    ws.setdefault("images", {})[f"slide_{slide_num:02d}"] = {
        "status": "done",
        "response_id": response.id,
        "generated_at": now,
        "path": str(slide_path),
    }
    state_mod.save(run_dir, ws)

    return {
        "ok": True,
        "path": str(slide_path),
        "response_id": response.id,
        "cached": False,
        "size": size,
    }


# ---- CLI ----

def main():
    p = argparse.ArgumentParser(description="Generate one carousel slide image.")
    p.add_argument("--run", required=True, help="Path to the run folder.")
    p.add_argument("--slide", type=int, required=True, help="Slide number (1-based).")
    p.add_argument("--prompt", required=True, help="Full image prompt (visual note + layout + style fragments).")
    p.add_argument("--reference", default=None, help="Path to an anchor image for style continuity.")
    p.add_argument("--previous-response-id", default=None, help="Explicit Responses API id to chain off.")
    p.add_argument("--no-chain", action="store_true", help="Disable auto-chaining.")
    p.add_argument("--size", default=None, help="Image size (1024x1536, 1024x1024, 1536x1024).")
    p.add_argument("--force", action="store_true", help="Regenerate even if the slide image exists.")
    args = p.parse_args()

    run_dir = Path(args.run)
    if not run_dir.exists():
        print(f"ERROR: run folder does not exist: {run_dir}", file=sys.stderr)
        sys.exit(1)

    # Verify prerequisites
    try:
        ws = state_mod.load(run_dir)
        state_mod.require_step_done(ws, "script")
        state_mod.require_step_done(ws, "style")
    except state_mod.StateError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    result = generate_slide(
        run_dir=run_dir,
        slide_num=args.slide,
        prompt=args.prompt,
        reference=args.reference,
        previous_response_id=args.previous_response_id,
        no_chain=args.no_chain,
        size=args.size,
        force=args.force,
    )

    print(json.dumps(result, indent=2))
    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
