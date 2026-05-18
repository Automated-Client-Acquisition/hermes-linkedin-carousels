# linkedin-carousels — Hermes plugin

A port of the LinkedIn/Instagram carousel builder from a Claude Code skill
to a Hermes plugin. Same pipeline (init → source → script → style → art →
export), same `gpt-image-2-2026-04-21` art generation, same resumable
workspace JSON — exposed through five tools under the `carousels` toolset
plus the bundled `SKILL.md` orchestrator guide.

Follows the contract from
<https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin>:
JSONSchema-style schemas with `parameters`, handlers signed
`(args: dict, **kwargs) -> str` that always return JSON and never raise.

## Install

1. Copy the plugin folder into Hermes' user-plugins directory:

   ```bash
   cp -R hermes-plugin/linkedin-carousels ~/.hermes/plugins/linkedin-carousels
   ```

2. Install Python dependencies into the environment Hermes runs in:

   ```bash
   pip install -r ~/.hermes/plugins/linkedin-carousels/data/requirements.txt
   ```

3. Enable the plugin (Hermes plugins are opt-in):

   ```bash
   hermes plugins enable linkedin-carousels
   ```

4. Verify it loaded:

   ```bash
   hermes plugins list
   # Or, if discovery seems off:
   HERMES_PLUGINS_DEBUG=1 hermes plugins list
   ```

5. Export `OPENAI_API_KEY` (or drop it in a `.env` at your project root —
   the bundled `generate.py` reads dotenv when present).

The agent now has:

- **Tools** (toolset `carousels`): `carousel_init`, `carousel_list`,
  `carousel_state`, `carousel_generate_slide`, `carousel_export`.
- **Skill**: `linkedin-carousels` (the orchestrator guide). Access from
  inside Hermes with `skill_view("linkedin-carousels")`.

## How a real run looks

```text
1. carousel_list({project_root: "/path/to/project"})
   → see available styles/voices/hooks/patterns/layouts
2. carousel_init({project_root, topic, brand, new_brand, style, voice,
                  hook, pattern, layout, platform, format, slides})
   → run folder scaffolded under <project_root>/runs/<slug>-<date>/
3. (you write source/insights.md + brief.md + script.md by hand,
    following SKILL.md)
4. carousel_generate_slide({run_path, slide, prompt, reference?})
   → ~$0.08 per slide, idempotent. Confirm slide 1 with user first.
5. carousel_export({run_path})
   → 01.png..NN.png + carousel.pdf + post-copy.txt + CHECKLIST.md at run root
```

`carousel_state({run_path})` returns the workspace JSON at any time so
the orchestrator can resume from the first step that isn't `done`.

## How it differs from the Claude Code skill

- **Filesystem anchors are env-driven.** The skill computed
  `REPO_ROOT = SKILL_DIR.parent.parent.parent` from `__file__`. Inside a
  Hermes plugin the plugin lives in `~/.hermes/plugins/` but the user's
  project is elsewhere, so the handlers in `tools.py` set
  `CAROUSELS_PROJECT_ROOT` and `CAROUSELS_SKILL_DIR` per call. The
  scripts honor those overrides and fall back to `__file__`-relative
  paths when unset (so they still work standalone in the skill layout).
- **Tools, not slash commands.** `python scripts/init.py …` becomes
  `carousel_init({...})` — same args, JSONSchema contract.
- **Skill text is registered.** `SKILL.md` is bundled under `data/` and
  registered via `ctx.register_skill("linkedin-carousels", ...)`. The
  "ask before burning $0.08" discipline and visual-note rules live there
  — the orchestrator model still has to follow them.

## What was verified locally

A Python-level smoke test confirms (without Hermes installed):

- All five schemas use the required `parameters` key (not `input_schema`).
- Every handler returns a JSON string, including on error.
- Handlers never raise — bad args produce `{"ok": false, "error": ...}`.
- `carousel_list` reads the bundled library and prints the inventory.
- `carousel_init` scaffolds a brand + run folder in a `/tmp` project,
  copies the chosen style + layout files into `.working/style/`, and
  writes a valid workspace JSON.
- `carousel_state` round-trips the workspace JSON for an existing run
  and returns a clean error for a missing run.

## What to pilot before trusting it on a real carousel

The plugin contract is correct. What's worth one $0.80 test run inside
real Hermes:

- Does Hermes' default model hold the **ask-before-generating** rule as
  faithfully as Claude does? That discipline lives in `SKILL.md` prose,
  not in code.
- Does the orchestrator write **content + mood** visual notes (vs.
  wireframe-style shape-and-position notes)? The discipline section of
  `SKILL.md` is where most regressions would show up.
