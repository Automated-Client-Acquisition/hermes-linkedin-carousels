# Styles

This folder is the carousel skill's **style library**. Each subfolder is one
named, self-contained visual style. A carousel run picks a style by name at
init time (`init.py --style <name>`), and every prompt for that run
inherits the style's locked rules and prompt fragment.

## Why a folder, not a single file

The previous version of this skill kept all styles in
`references/style-library.md` as paragraphs of prose. That worked for one
or two styles. It does not work once styles need:

- their own composition rules per slide-type,
- their own reference images for visual anchoring,
- their own prompt fragment that gets appended verbatim to every
  `generate.py` call,
- a way to be discovered programmatically by `init.py`.

A folder per style gives each one a stable home, makes the system
extensible, and keeps style assets co-located with the style definition.

## Folder layout (one style)

```
styles/
  README.md                # this file
  _index.md                # one-line registry of every available style
  <style-name>/
    style.md               # full human-readable spec
    prompt-fragment.txt    # the paragraph appended to every generate.py prompt
    slide-templates.md     # per-slide-type composition rules
    references/            # reference images for --reference anchoring (optional)
```

## How `init.py` uses this

When the user runs `init.py --style aca`, init.py:

1. Validates the style name against `styles/_index.md` (refuses unknown names).
2. Records the style in the run's workspace JSON (`style_name: "aca"`).
3. Copies the style's `style.md` and `prompt-fragment.txt` into the run's
   `02_style/` folder so they live next to the run for the life of the
   carousel. The run can override locally without touching the central
   style.

## How `generate.py` uses this

Each slide prompt has two parts: the slide's specific `Visual note` (from
`script.md`) and the run-locked style's `prompt-fragment.txt`. The user
(or Claude orchestrating) concatenates them and passes the whole thing to
`generate.py --prompt`.

If the style folder contains a reference image, `generate.py --reference
styles/<name>/references/<img>.png` can be used to anchor visual identity
across slides without first having to generate slide 1.

## Adding a new style

Five steps.

1. Pick a kebab-case name (e.g. `noir-documentary`, `clean-saas`,
   `craft-paper`).
2. Create `styles/<name>/`.
3. Write `styles/<name>/style.md` covering: when to use this style, palette
   (hex codes), typography, composition rules, per-slide-type guidance,
   what to avoid.
4. Write `styles/<name>/prompt-fragment.txt` — the paragraph appended
   verbatim to every prompt for this style. Keep it under ~500 words; it
   gets concatenated to every generate.py call so brevity counts.
5. Add a single line to `styles/_index.md` registering the style.

If the style needs reference images, add them to
`styles/<name>/references/` and document the file names + intended use in
`style.md`.

## Style naming conventions

- Names are kebab-case, no spaces, no underscores.
- Names describe the aesthetic, not the brand using it. `aca` is an
  exception because ACA's locked aesthetic is the first one built — but if
  the next brand wants the same look, they reference `aca` directly rather
  than forking a near-duplicate style.
- Avoid generic names like `default` or `standard`. Be specific
  (`hand-drawn-saas`, `editorial-dossier`, `noir-documentary`).
