"""Tool schemas for the linkedin-carousels Hermes plugin.

Each schema is the LLM-visible contract for one tool. The handlers in
tools.py do the actual work by shelling into the bundled scripts under
data/scripts/. Keep schemas tight: every parameter listed here is one the
orchestrator must be able to reason about, and every parameter NOT listed
is one the orchestrator should not have to know.
"""

CAROUSEL_INIT = {
    "name": "carousel_init",
    "description": (
        "STEP 0 of the carousel pipeline. Scaffold a new run folder under "
        "`<project_root>/runs/<slug>-<date>/` and seed its workspace JSON. "
        "Must be the FIRST tool called for any new carousel. Refuses to "
        "overwrite an existing run — if the run already exists, returns the "
        "existing workspace state so the orchestrator can resume."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "project_root": {
                "type": "string",
                "description": (
                    "Absolute path to the user's project root. Brands, runs, "
                    "and project-local libraries live HERE, not inside the "
                    "plugin. Required."
                ),
            },
            "topic": {
                "type": "string",
                "description": "Short title; used to build the run slug.",
            },
            "brand": {
                "type": "string",
                "description": "Brand key (folder under `<project_root>/brands/`).",
            },
            "new_brand": {
                "type": "boolean",
                "default": False,
                "description": (
                    "Allow creating the brand folder if it does not exist. "
                    "Pass true the first time you use a new brand."
                ),
            },
            "platform": {
                "type": "string",
                "enum": ["linkedin", "instagram", "both"],
                "default": "both",
            },
            "format": {
                "type": "string",
                "enum": ["portrait", "square", "landscape"],
                "default": "portrait",
                "description": (
                    "Output format preset. Locked at init time and cannot "
                    "change mid-run. Ask the user before defaulting."
                ),
            },
            "slides": {
                "type": "integer",
                "minimum": 3,
                "maximum": 20,
                "default": 10,
            },
            "style": {
                "type": "string",
                "description": (
                    "Style name from `styles/_index.md`. Omit to pick later "
                    "in STEP 3."
                ),
            },
            "voice": {"type": "string"},
            "hook": {"type": "string"},
            "pattern": {"type": "string"},
            "layout": {
                "type": "string",
                "description": (
                    "Layout-system name (editorial-spread, dossier-stack, "
                    "newspaper-column, dispatch-bulletin, etc.). Omit to "
                    "pick during STEP 3 based on the source content."
                ),
            },
        },
        "required": ["project_root", "topic", "brand"],
    },
}

CAROUSEL_LIST = {
    "name": "carousel_list",
    "description": (
        "Library discovery. Lists every available style, voice, hook, "
        "post-pattern, and layout-system, merging plugin defaults with "
        "project-local entries (project entries shadow defaults on name "
        "conflict). Call this BEFORE asking the user to pick a style/voice/"
        "hook/pattern/layout so you can present real options."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "project_root": {"type": "string"},
            "kind": {
                "type": "string",
                "enum": ["styles", "voices", "hooks", "post-patterns",
                         "layout-systems"],
                "description": "Optional. Filter to one library kind.",
            },
            "name": {
                "type": "string",
                "description": (
                    "Optional. With `kind`, returns the full spec for one "
                    "entry (the markdown file)."
                ),
            },
        },
        "required": ["project_root"],
    },
}

CAROUSEL_STATE = {
    "name": "carousel_state",
    "description": (
        "Read the workspace JSON for a run. Returns which steps are done, "
        "which slides have been generated, the chosen brand/style/voice/"
        "hook/pattern/layout, the comment trigger word, and history. ALWAYS "
        "call this before doing any work on an existing run."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "run_path": {
                "type": "string",
                "description": (
                    "Path to the run folder, e.g. "
                    "`<project_root>/runs/on-page-aeo-2026-05-14`."
                ),
            },
        },
        "required": ["run_path"],
    },
}

CAROUSEL_GENERATE_SLIDE = {
    "name": "carousel_generate_slide",
    "description": (
        "STEP 4. Generate ONE slide image with gpt-image-2-2026-04-21 and save "
        "it into the run's slides folder. Idempotent: if the slide already "
        "exists it is skipped unless `force=true`. Costs ~$0.08 per call — "
        "confirm the prompt with the user before generating slide 1."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "run_path": {"type": "string"},
            "slide": {
                "type": "integer",
                "minimum": 1,
                "description": "Slide number (1-based).",
            },
            "prompt": {
                "type": "string",
                "description": (
                    "Full image prompt: visual note FIRST, then layout "
                    "fragment, then style fragment."
                ),
            },
            "reference": {
                "type": "string",
                "description": (
                    "Optional path (relative to run_path or absolute) to an "
                    "anchor image. Pass slide-01 for style continuity, or a "
                    "brand logo SVG when the slide mentions a named brand."
                ),
            },
            "previous_response_id": {
                "type": "string",
                "description": (
                    "Optional. Explicit Responses-API id to chain off. If "
                    "omitted, the script auto-chains off the previous slide."
                ),
            },
            "no_chain": {
                "type": "boolean",
                "default": False,
                "description": "Disable auto-chaining. Use for a deliberate fresh generation.",
            },
            "size": {
                "type": "string",
                "description": (
                    "Optional image size (e.g. '1024x1536'). Defaults to "
                    "the format.source_size locked at init."
                ),
            },
            "force": {
                "type": "boolean",
                "default": False,
                "description": "Regenerate even if the slide image exists.",
            },
        },
        "required": ["run_path", "slide", "prompt"],
    },
}

CAROUSEL_EXPORT = {
    "name": "carousel_export",
    "description": (
        "STEP 5. Normalize every slide image to the locked format, lock the "
        "background, write `01.png..NN.png` + `carousel.pdf` + "
        "`post-copy.txt` + `CHECKLIST.md` into the run root. Marks the run "
        "complete."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "run_path": {"type": "string"},
        },
        "required": ["run_path"],
    },
}

ALL_SCHEMAS = [
    CAROUSEL_INIT,
    CAROUSEL_LIST,
    CAROUSEL_STATE,
    CAROUSEL_GENERATE_SLIDE,
    CAROUSEL_EXPORT,
]
