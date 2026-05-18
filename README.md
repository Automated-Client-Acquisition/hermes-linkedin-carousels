# hermes-linkedin-carousels

A [Hermes](https://hermes-agent.nousresearch.com/) plugin that turns a
blog post URL, transcript, or research doc into a finished, ready-to-post
LinkedIn/Instagram carousel — slide-by-slide script, on-brand images via
OpenAI `gpt-image-2-2026-04-21`, correctly sized exports, and the post copy
that goes above the carousel.

Fully stateful: every step is resumable from a workspace JSON file inside
the run folder.

## Install

```bash
hermes plugins install seguelaCedric/hermes-linkedin-carousels --enable
```

This drops the plugin into `~/.hermes/plugins/hermes-linkedin-carousels/`
and enables it. You then need to:

1. **Install the Python deps into the same Python that runs Hermes.** If
   Hermes is in a venv at `~/venvs/hermes/`, that's
   `~/venvs/hermes/bin/pip install -r ~/.hermes/plugins/hermes-linkedin-carousels/data/requirements.txt`.
   In a Docker container it's `docker exec <cid> pip install -r ...`.

2. **Export your OpenAI key** for the user that runs Hermes:

   ```bash
   export OPENAI_API_KEY=sk-...
   ```

   Or drop it in a `.env` at your project root — the bundled `generate.py`
   reads `python-dotenv` when present. Image generation costs ~$0.08 per
   slide.

3. **Restart Hermes** so it discovers the new tools, then verify:

   ```bash
   hermes plugins list | grep carousel
   ```

## Update

```bash
hermes plugins update hermes-linkedin-carousels
```

## What the plugin exposes

Five tools under the `carousels` toolset, plus a bundled
`linkedin-carousels` skill (the orchestrator guide that lives in
`data/SKILL.md`).

| Tool | What it does |
|---|---|
| `carousel_list` | Inventory the available styles, voices, hooks, post-patterns, layout-systems. |
| `carousel_init` | Scaffold a new run folder under `<project_root>/runs/<slug>-<date>/`. STEP 0. |
| `carousel_state` | Read the workspace JSON for a run. Resume-safe. |
| `carousel_generate_slide` | Generate ONE slide image via `gpt-image-2-2026-04-21`. Idempotent. STEP 4. |
| `carousel_export` | Normalize + write `01.png..NN.png`, `carousel.pdf`, `post-copy.txt`, `CHECKLIST.md`. STEP 5. |

The orchestrator's job (write the script, pick the style, draft visual
notes) lives in `data/SKILL.md`. The agent reads that skill before
acting; the tools just do the deterministic work.

## How the filesystem is laid out

- **The plugin** lives at `~/.hermes/plugins/hermes-linkedin-carousels/`.
  Don't put project data here.
- **Your project** lives wherever you want — pass its absolute path as
  `project_root` to `carousel_init` and `carousel_list`. Brands and
  runs are created there:

  ```
  <project_root>/
    brands/<brand>/brand.md      # brand identity
    runs/<slug>-<date>/          # one carousel
      .working/                  # workspace JSON + scratch
      01.png..NN.png             # exported deliverables
      carousel.pdf
      post-copy.txt
      CHECKLIST.md
  ```

- **Project-local libraries** (your own styles, voices, etc.) go at
  `<project_root>/styles/<name>/`, etc. They shadow the plugin's
  defaults on name conflict.

## Typical flow

```text
1. carousel_list({project_root})              → see what's available
2. carousel_init({project_root, topic, brand, style, voice, hook,
                  pattern, layout, format, slides, new_brand?})
                                              → run folder scaffolded
3. (write source/insights.md, brief.md, script.md by hand —
    follow data/SKILL.md)
4. carousel_generate_slide({run_path, slide: 1, prompt: "..."})
   ... repeat for each slide ...              → ~$0.08 each, idempotent
5. carousel_export({run_path})                → deliverables at run root
```

`carousel_state({run_path})` returns the workspace JSON at any time so
the orchestrator can resume from the first step that isn't `done`.

## Plugin contract

Conforms to the
[build-a-Hermes-plugin guide](https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin):

- Schemas use JSONSchema style with the `parameters` key.
- Handlers are `(args: dict, **kwargs) -> str`, return JSON strings
  ALWAYS, and never raise (errors come back as `{"ok": false, "error":
  "..."}`).
- Tools are registered under the `carousels` toolset.
- `SKILL.md` is bundled and registered via `ctx.register_skill()`.

## What's worth piloting before trusting it

The plugin contract is mechanically correct and smoke-tested. What's
worth one $0.80 real run inside Hermes:

- Does Hermes' default model hold the **ask-before-generating** rule as
  faithfully as Claude does? That discipline lives in `SKILL.md` prose,
  not in code.
- Does the orchestrator write **content + mood** visual notes (vs.
  wireframe-style shape-and-position notes)? The discipline section of
  `SKILL.md` is where most regressions would show up.

## License

MIT.
