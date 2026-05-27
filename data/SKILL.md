---
name: linkedin-carousels
description: >
  Turn a blog post URL, a transcript, or a research doc into a finished,
  ready-to-post LinkedIn/Instagram carousel — slide-by-slide script, on-brand
  images generated with OpenAI gpt-image-2-2026-04-21, correctly sized exports, and the
  post copy that goes above the carousel. Fully stateful: the first call
  scaffolds a run folder + workspace file, and every later call resumes from
  the first step that isn't done.
built_with: [Hermes Agent, OpenAI gpt-image-2-2026-04-21]
trigger: >
  Use when the user wants a LinkedIn or Instagram carousel, wants to turn an
  article/transcript/research doc into slides, says "make a carousel",
  "carousel from this post", "slide deck for social", or asks to resume/continue
  a carousel run.
---

# LinkedIn & Instagram Carousels

You are the **orchestrator**. The Python scripts in `scripts/`
do the deterministic work — folder scaffolding, OpenAI image calls, image
resizing/export. You do the judgement work — reading the source, writing the
script, locking the style, writing image prompts.

This skill is built as ONE orchestrator but the SCRIPT stage and the ART
stage are self-contained (own scripts, own references) so they can be split
into sub-skills later without a rewrite.

---

## The golden rule: the workspace file is the source of truth

Every carousel lives in a run folder: `runs/<slug>-<YYYY-MM-DD>/`.
Its state lives in `.linkedin-carousels-workspace.json` inside that run folder
— which steps are done, the slide count, the chosen brand and style, the
comment trigger word, and per-slide image status.

**Before doing anything: read the workspace file. After finishing any step:
update it.** This is what lets a run resume instead of redoing work or
clobbering finished slides. A step may only run if every step before it is
marked `done`.

---

## The second golden rule: ask before generating

This skill spends real money every time it calls `gpt-image-2-2026-04-21`. Around
$0.08 per slide. A 10-slide carousel in the wrong style is $0.80 of
direct waste plus user trust. The cost of pausing to ask the user a
question is zero.

**Rule: when there's a creative choice the orchestrator could make
multiple reasonable ways, ASK FIRST. Do not guess and burn the API
budget.** A confirmed prompt that takes 30 seconds longer to draft is
always better than three regen rounds at $0.08 each.

Explicit ask-points, by step:

- **STEP 0 (init):** if the user invokes the carousel without `--format`,
  `--style`, `--voice`, `--hook`, `--pattern`, or `--layout`, ask them which to pick
  before scaffolding the run. Show them the relevant `list.py` output for
  each kind they haven't specified. Format choices come from
  `state.py / FORMAT_PRESETS` (portrait, square, landscape). The format
  is LOCKED at init time and cannot change mid-run.
- **STEP 1 (source):** if the source material is ambiguous (multiple
  reasonable angles, multiple possible audiences), ask before writing
  `brief.md`.
- **STEP 2 (script):** before writing `script.md`, confirm:
  - the hook archetype (if not locked at init),
  - the post body pattern (if not locked at init),
  - the CTA trigger word.
- **STEP 3 (style + layout):** if `--style` or `--layout` were not locked at init, ask which
  style to pick. Show `list.py styles` output.
- **STEP 4 (art):** **before generating slide 1, print the full prompt
  and confirm it with the user.** Slide 1 is the anchor for slides
  2-N. Getting it right matters more than speed. Once slide 1 is
  approved, slides 2-N can run without per-slide confirmation UNLESS
  the user asked for it.
- **STEP 5 (export):** before posting (the user's job, not the
  skill's), the orchestrator must surface the post copy, the trigger
  word, and any TODO items in `brand.md`/`lead-magnets.md` that need
  to be resolved before publication.

When you ask, ask precisely. "Want this in the hype voice or the
senior-operator voice?" beats "what voice do you want?" — the user can
always say "other" but the named options anchor the question.

### When NOT to ask

- When the user has explicitly told you to keep going ("don't stop
  asking", "just do it", "ship it").
- When the question would be answered by reading `brands/<brand>/` —
  read the brand sub-files first, then ask only if a choice is left
  open.
- When the workspace file says a previous step locked the choice —
  trust the lock unless the user is rerunning from scratch.

---

## Brands vs runs vs libraries

- `brands/<brand>/` — a brand's locked identity. Each brand is a folder
  with `brand.md` as the index plus four sub-files: `voice.md`,
  `audience.md`, `design.md`, `lead-magnets.md`. The brand is the WHO,
  WHAT, WHERE.
- `runs/<slug>-<date>/` — one carousel. Inherits the brand's defaults
  and the locked libraries; the per-run `02_style/` holds the specific
  style for that run.
- **Libraries** at `<skill>/<kind>/` and `<project>/<kind>/` — reusable
  modules for `styles`, `voices`, `hooks`, `post-patterns`, `layout-systems`.
  A run picks one entry from each library at init time. Libraries are
  the HOW.

The skill discovers libraries in two tiers: skill-shipped defaults
inside `data/<kind>/`, and project-local
entries at `<project-root>/<kind>/`. Project-local entries shadow skill
defaults on name conflict, so users can override without forking the
skill.

To discover what's available:

```bash
python data/scripts/list.py
```

If the user names a brand that has no `brand.md` yet, run `init.py` with
`--new-brand` and help them fill in `brands/<brand>/brand.md` (plus the
four sub-files) from the patterns in `brands/aca/`.

---

## Pipeline overview

| # | Step    | Who                  | Reads                    | Writes                                   |
|---|---------|----------------------|--------------------------|------------------------------------------|
| 0 | init    | `scripts/init.py`    | user args                | run folder tree + workspace json         |
| 1 | source  | you                  | the input                | `brief.md`, `source/insights.md`         |
| 2 | script  | you (+script refs)   | `brief.md`, insights     | `script.md`                              |
| 3 | style   | you (+style library) | brand.md + user choice   | `02_style/style.md`                      |
| 4 | art     | you + `generate.py`  | `script.md`, `style.md`  | `slides/slide-NN.png`, `middle-art/`      |
| 5 | export  | `scripts/export.py`  | `slides/`                | `export/` sized images + copy + alt-text |

Run-folder layout created by init (mirrors the demo screenshot):

```
runs/<slug>-<date>/
  .linkedin-carousels-workspace.json   <- STATE. read first, write last.
  brief.md                             <- step 1: source summary + angle
  source/                              <- step 1: raw input + insights.md
  script.md                            <- step 2: slide-by-slide script + post copy
  02_style/                            <- step 3: locked style for this run
  middle-art/                          <- step 4: working/iteration images, refs
  slides/                              <- step 4: final per-slide images
  alt-text.md                          <- step 5: accessibility alt text per slide
  export/                              <- step 5: 1080x1350 exports + post-copy.txt
```

---

## STEP 0 — init (ALWAYS the first call)

Creates the run folder structure + workspace file so the skill knows what has
been done.

```bash
python data/scripts/init.py \
  --topic "On-page AEO" \
  --brand aca \
  --style aca \
  --voice senior-operator \
  --hook stop \
  --pattern fascination-bullets \
  --platform both --slides 10
```

Args:
- `--topic` (required) — short title; used to build the run slug.
- `--brand` (required) — brand key. Folder created under `brands/` if new
  (pass `--new-brand` to confirm creating it).
- `--style` (recommended) — visual style name from `styles/_index.md`
  (skill or project-local). Locks the aesthetic at init time, copies the
  style's files into the run's `02_style/`, and marks STEP 3 done. If
  omitted, STEP 3 stays pending and the orchestrator picks a style
  during that step.
- `--voice` (recommended) — voice name from `voices/_index.md`. Locks
  the tone of the post and slide copy at init time. If omitted, the
  brand's default voice is used (from `brands/<brand>/voice.md`).
- `--hook` (optional) — hook archetype name from `hooks/_index.md`.
  Suggests the slide-1 / post-line-1 structure for STEP 2. If omitted,
  the orchestrator picks one based on the source material.
- `--pattern` (optional) — post-body pattern name from
  `post-patterns/_index.md`. Suggests the post body structure for STEP
  2. If omitted, the orchestrator picks one.
- `--platform` — `linkedin` | `instagram` | `both`. Default `both`.
- `--slides` — target slide count hint, 8–12. Default `10`.

It prints the run path + the fresh workspace JSON. If the run folder already
exists, it refuses to overwrite and prints the existing state so you resume.

**After init: read the printed workspace JSON before continuing.**

### Library discovery (`list.py`)

To see every available style, voice, hook, post-pattern, and layout-system:

```bash
python data/scripts/list.py
# or:
python data/scripts/list.py <kind>
python data/scripts/list.py <kind> <name>
```

This is the first command a new user should run after installing the
skill. It distinguishes skill-shipped defaults `[skill]` from
project-local additions `[project]`.

### Library kinds and their READMEs

- `styles/` — brand-consistency layer (palette, typography, voice,
  realism rules, continuity chrome). See `styles/README.md`.
- `voices/` — tone-of-voice for post copy and in-image text. See
  `voices/README.md`.
- `hooks/` — first-line / first-slide copywriting templates. See
  `hooks/README.md`.
- `post-patterns/` — structural templates for the post body. See
  `post-patterns/README.md`.
- `layout-systems/` — compositional vibe per run (editorial-spread,
  dossier-stack, newspaper-column, dispatch-bulletin). The vibe sets
  the overall compositional mood; specific layout per slide is
  decided contextually by the model based on slide content. See
  `layout-systems/README.md`.

The `diagrams/` library was removed — it prescribed specific
visualization templates (timeline, funnel, three-stage-flow,
oversized-number, etc.) per slide. The new architecture is content-
driven: the model composes the visual for each slide based on its
content, within the style's aesthetic world. No prescribed
visualization templates per slide.

Every library follows the same shape: `_index.md` registers the entries,
each entry is a folder with a markdown spec (and a `prompt-fragment.txt`
where applicable). Adding a new entry is copy-and-edit; see each
library's README for the recipe.

To list available styles from a terminal:

```bash
cat data/styles/_index.md
```

---

## STEP 1 — source

Get raw material into the run folder.

- **URL given** → fetch, strip nav/boilerplate, save clean text to
  `source/source.md` (URL on line 1 as `# Source: <url>`).
- **Transcript / research doc given** → copy verbatim into `source/source.md`.
- **Nothing given** → stop and ask. Never invent a source.

Then read it fully and write:
- `source/insights.md` — 10–15 of the strongest, most specific,
  most counterintuitive points. Be ruthless; vague points get cut.
- `brief.md` — the run brief: one-paragraph summary, the chosen angle for
  this carousel, target audience, and which insights become slides.

Update workspace: `steps.source = "done"`, set `source_type`, `insight_count`.

---

## STEP 2 — script

Write `script.md`. The most important creative step. The orchestrator
reads THREE references before writing visual notes:

1. `references/copywriting-patterns.md` — hook formulas, post patterns,
   CTA formats. Drives the WORDS on each slide.
2. `references/decoration-and-craft.md` — the eight principles that
   make a slide scroll-stopping (decoration, texture, annotation, one
   spicy element, color discipline, asymmetry, continuity, short
   confident headline). Drives the visual ENERGY of each slide.
3. `references/designer-moves.md` — the QUALITY-FLOOR RULES for
   avatars, mockups, charts, and brand logos. NOT a catalog of named
   moves to pick from; only realism gates. Avatars have faces.
   Mockups carry plausible content. Charts are real or absent.
   Brand logos are real.

A slide whose visual note is just "headline + diagram + page counter"
is rejected. So is a visual note that overspecifies shape and
position — see the discipline below.

### Visual-note discipline (the most important rule in STEP 2)

The orchestrator's job when writing a `Visual note` is to describe
**WHAT THE SLIDE IS ABOUT and HOW IT SHOULD FEEL**, not to choreograph
shape and position. The skill has been stripped of element catalogs
precisely so the model can compose contextually. The orchestrator
must not re-introduce those catalogs by writing visual notes in
shape-and-position language.

**Write visual notes in CONTENT + MOOD language. Forbidden in visual notes:**

- "INSIDE THE CARD, render a 2x2 grid of mini-cards..."
- "1px Ink border, sharp 0px corners, rounded ~16-20px corners..."
- "TOP-LEFT mini-card carries an uppercase tracked-monospace header..."
- "Connect them with thin ACA-Red routing lines and small straight red arrow glyphs at each turn..."
- "Position the headline at the upper-left at approximately 60-80px..."

That language micromanages the layout. The model dutifully delivers
exactly that — a wireframe-flavored 2x2 grid of monospace-labelled
boxes. The result reads as a Figma frame, not an editorial slide.

**Allowed in visual notes:**

- What the slide is ABOUT (its narrative function, the argument it
  makes).
- The KEY COPY (headline, body line, kicker copy, attribution).
- The EMOTIONAL REGISTER and physical-artifact METAPHOR ("this
  slide is a magazine front cover", "this slide is a desk that just
  got photographed", "this slide is a paper-clipped field note",
  "this slide is a torn newspaper clipping under glass").
- The QUALITY BAR ("the slide should stop the scroll in under one
  second", "visible craft on the page", "real artifact density,
  not minimalist-empty").
- Specific COPY that must appear inside any mockup ("the email
  preview's subject line should read 'subject: re: our chat last
  week'"), but NOT the mockup's frame, border weight, or position.
- Hard CONTENT bans ("no fake charts on this slide because we don't
  have a real number to anchor", "no brand mentions that imply
  endorsement").

### Two examples — same content, two different visual notes

**BAD** (shape-language micromanagement; produces wireframes):

> Editorial-spread asymmetric-card slide. Kicker pill at top-LEFT.
> Italic-serif headline left-aligned. One white content card pushed
> right (~60% width). Inside the card, a 2x2 grid of four mini-cards
> with 1px Ink borders and sharp 0px corners. Top-left mini-card
> labelled "EMAIL" with placeholder subject text. Top-right
> labelled "LINKEDIN". Bottom-left "DMS". Bottom-right "PHONE".
> Connect with red routing line and small straight arrows at turns.

**GOOD** (content + mood; lets the model compose):

> This slide is about how ACA executes the operator's outreach
> across four channels: email, LinkedIn, DMs, and phone. It should
> feel like an outbound operator's desk got photographed from above
> — visible artifacts proving the system is alive in the world:
> a real-looking email composer, a phone with a LinkedIn DM open,
> a sticky note tracking a call-log, papers with handwritten
> notations. Real artifacts, not wireframe diagram boxes. The body
> line "Multi-channel infrastructure. Email, LinkedIn, DMs,
> phone." sits underneath the artifact composition. Headline
> reads "aca executes the outreach." with "executes" in red.

The difference: the GOOD note tells the model WHAT THE SLIDE IS
ABOUT and WHAT IT SHOULD FEEL LIKE. The model then composes the
actual artifact layout (which is exactly the kind of judgment-call
work the model is good at when not micromanaged).

### Before generating, audit your visual note

Re-read each visual note before passing it to `generate.py`. Search
for these red flags:

- Any mention of borders, corners, pixel weights, grid arrangements,
  positions in percentages, "1px", "0px", "rounded", "sharp 0px".
- Any description of an internal mini-card / mini-element structure
  ("inside the card, a 2x2 grid", "stack of three rows", "vertical
  list of items").
- Any "INSIDE THE CARD" or "INSIDE THIS FRAME" language at all —
  this almost always means you're micromanaging.
- Any mention of "tracked-monospace label header" / "header sits in
  the top-left" / element-positioning chrome.

If you find any of those, rewrite the note in content + mood
language before generating. The model produces editorial composition
when given an editorial brief. It produces wireframes when given
wireframe specs.

One clear point per slide — never two:
- **Slide 1 — Hook.** A scroll-stopper. Bold claim, number, sharp question,
  or "most people get this wrong" framing. No throat-clearing.
- **Slides 2..N-1 — Body.** Each = one insight, as a 3–7 word headline + one
  supporting line. A narrative thread runs through them.
- **Slide N — Payoff + CTA.** Takeaway lands, then a call to action: **save**,
  **follow**, or **comment a specific word**. When it's a comment CTA, pick
  ONE clean trigger word — that's what plugs into ManyChat-style auto-DM.

Also write the **post copy** — the caption above the carousel: 3–6 short
lines, hook-first, ending with a soft nudge to swipe.

### Voice — ask the user per run
1. **Brand default** — use the voice locked in `brands/<brand>/brand.md`.
2. **Hype** — high-energy B2B founder voice.
3. **Clean** — neutral, calm, authoritative.
4. **Custom** — user describes it.

Write `script.md` in the exact format in `templates/script.md` so
`generate.py` can parse it. Every slide MUST have a `Visual note`.

Update workspace: `steps.script = "done"`, set `slide_count`,
`comment_trigger_word`.

---

## STEP 3 — style AND layout system

This step picks TWO things, both of which sit inside the run's
`02_style/` folder:

1. **The style** — the brand-locked aesthetic grammar (palette, type
   family, spicy-element rules). Picked from `styles/_index.md`.
2. **The layout system** — the run-level compositional vocabulary
   that shapes how each slide's hero zone varies by function. Picked
   from `layout-systems/_index.md`. See principle 9 in
   `references/decoration-and-craft.md` for why this matters: a
   confession deck and a teardown deck inside the same style should
   NOT look the same. The layout system is what makes them different.

### If the style was locked at init (--style passed)

Skip the style sub-step. The style's `style.md`, `prompt-fragment.txt`,
and `slide-templates.md` are already in `02_style/`, and
`steps.style` is already `done`.

### If the style was NOT locked at init

1. Read `styles/_index.md` for the registered list.
2. Read each candidate's `styles/<name>/style.md` for "when to use" guidance.
3. Pick the style that best fits this carousel's content type. Confirm
   with the user if there's any ambiguity.
4. Copy the chosen style's `style.md`, `prompt-fragment.txt`, and
   `slide-templates.md` into the run's `02_style/`.
5. Update workspace: `steps.style = "done"`, set `style_name`.

### Layout system — ALWAYS picked at STEP 3 (init lock or here)

If the layout system was locked at init (`--layout` passed), the
layout's `layout.md` and `layout-fragment.txt` are already in
`02_style/`, and `steps.layout` is already `done`. Skip ahead.

If the layout was NOT locked at init, pick one now:

1. Read `layout-systems/_index.md` for the registered list.
2. Read each candidate's `layout-systems/<name>/layout.md` for "when
   to use" guidance.
3. Pick the layout that best fits THIS RUN's content — not the style's
   most-common layout. A confessional narrative wants
   `editorial-spread`. A capability teardown wants `dossier-stack`.
   Breaking news wants `newspaper-column`. A terse operational update
   wants `dispatch-bulletin`.
4. Confirm with the user before locking — this choice shapes every
   slide. The cost of asking is zero; the cost of regenerating 12
   slides under the wrong layout is ~$0.96.
5. Copy the chosen layout's `layout.md` and `prompt-fragment.txt`
   (the latter as `layout-fragment.txt` to avoid colliding with the
   style's prompt-fragment.txt) into the run's `02_style/`.
6. Update workspace: `steps.layout = "done"`, set `layout_system`.

### What if none of the layout systems fit?

Propose a new one to the user before scaffolding the run. Add the
layout's folder under `layout-systems/<new-name>/`, register it in
`_index.md`, then proceed. Do not freelance a layout inside the run
folder only — layout systems are meant to be reusable.

Aspect ratio is always **1080×1350 (4:5)** for both platforms — handled
by `export.py`, not the style.

Older style definitions (Clean SaaS, Hand-drawn, Craft paper, Noir
documentary, Soft corporate, Photography) used to live in
`references/style-library.md` as paragraphs of prose. That file is kept
for backwards compatibility / inspiration, but the canonical style
source is now `styles/<name>/`.

---

## STEP 4 — art

For each slide in `script.md`, generate one image into `slides/`.

Before generating ANY slide, the orchestrator locks the run's
**continuity guardrails** — the small set of elements that stay
consistent across every slide so the deck reads as ONE artifact:

- The palette (locked by the chosen style).
- The typography family (locked by the chosen style).
- The kicker-pill format (if the style uses one).
- The page-counter format and corner position.
- The brand wordmark treatment.

These guardrails are recorded in the run's
`02_style/continuity-guardrails.md` (one short file — what stays
locked, nothing else). The orchestrator does NOT pre-pick a fixed
list of "decoration elements" for the run. Decoration is composed
per-slide by gpt-image-2-2026-04-21 based on each slide's content, within the
style's aesthetic register. The orchestrator's job is to (a) lock
continuity guardrails, then (b) write visual notes that describe
WHAT THE SLIDE IS ABOUT, leaving the decoration composition to the
model.

This is a deliberate shift from earlier versions of this skill,
which locked a prescriptive "kit" of decoration elements per run.
That approach produced repetitive, mechanical slides. The current
approach gives the model a rich aesthetic world (via the style's
prompt fragment) and content-specific direction (via the visual
note) — and trusts the model to compose decoration that fits.

Per slide:
1. Build the prompt = slide `Visual note` + the locked **layout
   fragment** (from `02_style/layout-fragment.txt`, the layout system
   locked at STEP 3) + the locked **style fragment** (from
   `02_style/prompt-fragment.txt`). Concatenation order: visual note
   FIRST (the slide-specific content wins), then layout fragment
   (run-level compositional shape), then style fragment (brand-level
   aesthetic world).

   The **visual note** describes WHAT THE SLIDE IS ABOUT — its
   narrative function (hook / setup / capability / payoff / CTA),
   the headline + body copy, and the kind of content the slide is
   built around (a capability list, a stat reveal, a system diagram,
   a pull-quote, a CTA). The visual note MAY suggest specific
   decoration elements that fit the content — but it does NOT
   dictate them from a fixed checklist. The model is given a rich
   aesthetic world (via the style fragment) and trusted to compose
   decoration that fits.

   `references/designer-moves.md` contains the QUALITY-FLOOR RULES
   the orchestrator confirms before generating: avatars must show
   real faces, mockups must carry plausible content, charts are
   real or absent, brand marks use real logos. These are quality
   gates, not creative suggestions. The 32-move catalog that used
   to live in that file was removed — it produced mechanical decks
   because the orchestrator kept reaching for the same fixed
   elements.

   Per-slide quality bar (the orchestrator confirms before
   generating):
   - The visual note describes the slide's CONTENT and FUNCTION
     clearly — what the slide is ABOUT, not just "headline +
     diagram + page counter."
   - Headline is 1-6 words (gpt-image-2-2026-04-21 misspells
     anything longer).
   - Body copy is short (one line max on the slide; longer body
     lives in the post caption).
   - The realism rules in `references/designer-moves.md` are
     honored: avatars have faces, mockups have plausible content,
     charts are real or absent, brand logos are passed as
     `--reference` when a brand is named.
   - The principles in `references/decoration-and-craft.md` are
     honored (decoration, texture, annotation, one spicy element,
     color discipline, asymmetry, continuity, short headlines) —
     but as FORCES, not as a checklist.

   The orchestrator does NOT require: a fixed list of decoration
   elements per slide, a prescribed hero-zone treatment per slide
   function, a specific diagram type per content type, named moves
   from a catalog. Those constraints produced wireframes. Trust the
   style's prompt fragment to deliver the aesthetic world, the
   layout system's vibe to deliver the compositional mood, and
   the visual note to deliver the content. The model composes the
   actual slide.
2. Generate:
   ```bash
   python data/scripts/generate.py \
     --run "runs/<slug>-<date>" --slide 3 --prompt "<full prompt>"
   ```
3. `generate.py` is **idempotent** — if `slides/slide-03.png` exists it skips
   unless `--force`. This is what makes the step resumable.
4. Optionally anchor style drift by passing slide 1 as a reference:
   `--reference "slides/slide-01.png"`. Working/iteration images go in
   `middle-art/`. Reference anchoring is especially important for any
   style that uses a recurring character / protagonist.

5. **If the slide mentions a named brand or product** (LinkedIn,
   Telegram, Discord, Claude, GPT, Gemini, Stripe, Notion, etc.),
   pass the actual logo as the reference image instead of slide-01:
   `--reference "data/assets/logos/<brand>.svg"`.
   Look up the brand in `assets/logos/_index.md` first to find the
   correct file + the alias mapping + any voice / endorsement
   guardrails. In the visual note, reference the logo by name and
   intended position ("the LINKEDIN wordmark in its official blue,
   top-right corner of the card, ~80px wide") — never re-describe
   the logo's visual style. If the brand is in the index but its
   file is `NOT INCLUDED` (some trademark holders removed their
   marks from SimpleIcons), use the typographic fallback specified
   in the entry instead of passing a reference image. If the slide
   mentions multiple brands at once (e.g. a "we tested GPT, Gemini,
   Grok, Llama, Claude" bake-off), generate one slide per brand
   round-robin OR pass the most-prominent brand as the reference
   and describe the others typographically — gpt-image-2-2026-04-21 can only
   anchor on one reference per call.
5. After each slide, run the per-slide checklist from
   `references/decoration-and-craft.md`. If the visual note fails any
   of the eight checks, fix the visual note before generating —
   regenerating after the fact costs ~$0.08 per slide.
6. After each slide, update workspace `images.slide_NN = "done"`.

When all slides exist: `steps.art = "done"`.

---

## STEP 5 — export

```bash
python data/scripts/export.py --run "runs/<slug>-<date>"
```

This: confirms every scripted slide image exists (errors loudly if not);
normalizes each to exactly 1080×1350 sRGB no-alpha; writes them to `export/`
as `01.png … NN.png`; writes `export/post-copy.txt` (the caption) and
`alt-text.md` (accessibility alt text per slide); writes `export/CHECKLIST.md`
(which slide has the CTA, the trigger word, per-platform posting notes).

Update workspace: `steps.export = "done"`, `status = "complete"`. Then tell
the user the export folder path and the comment trigger word.

---

## Resuming a run

If the user says "continue the AEO carousel":
1. Find the run folder under `runs/`.
2. Read its `.linkedin-carousels-workspace.json`.
3. Announce what's done and what's next, then continue from the first step
   that isn't `done`. Never redo a `done` step unless explicitly asked.

## Setup

Requires `OPENAI_API_KEY` in the environment.
`pip install -r data/requirements.txt`
