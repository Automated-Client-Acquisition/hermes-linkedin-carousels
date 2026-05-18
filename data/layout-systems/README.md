# Layout systems

This folder is the carousel skill's **layout-systems library**. Each
subfolder is one named compositional vocabulary that a run picks at
init time (`init.py --layout <name>`).

## What problem this solves

A **style** is the brand-locked aesthetic grammar (bone paper + italic
Instrument Serif + ACA Red for `aca`; white + bold sans + blue/orange
marker for `hand-drawn-saas`; etc.). The style is non-negotiable per
brand.

A **layout system** is the compositional vocabulary used INSIDE that
style on a given run. Same style + different layout system =
different deck. Same style + same layout system across two runs =
visually repetitive decks.

The principle: **design adapts to content per RUN, not just per slide.**
Every run picks a layout system that fits THIS post's narrative, and
that system supplies the compositional moves for every slide in the
run.

Layout systems supply:

- Which slide functions get content cards vs typography-only.
- Where the hero zone sits (centered / asymmetric / full-bleed).
- Whether kicker pills, page counters, ticker rows, drop caps, or
  column rules appear — and where.
- The vocabulary of recurring compositional moves the run favors
  (e.g. "every slide uses an oversized opening drop cap" vs "every
  slide has a hairline rule above the page counter").

Layout systems do NOT change:

- The style's color palette.
- The style's typography family.
- The style's spicy-element rules.
- The brand voice.
- The principles in `references/decoration-and-craft.md`.

## How `init.py` uses this

`init.py --layout <name>` validates the name against `_index.md` and
records the chosen layout in the run's workspace JSON
(`layout_system: "<name>"`). The layout's `prompt-fragment.txt` is
copied into the run's `02_style/layout-fragment.txt` and gets
concatenated into every `generate.py` prompt alongside the style's
fragment.

If `--layout` is omitted, the orchestrator picks one during STEP 3
based on the source content and confirms with the user.

## Adding a new layout system

1. Pick a kebab-case name describing the compositional vocabulary
   (e.g. `editorial-spread`, `newspaper-column`, `dossier-stack`).
2. Create `layout-systems/<name>/`.
3. Write `layout-systems/<name>/layout.md` covering: when to use this
   system, the four canonical hero-zone treatments per slide function
   (hook / capability / payoff / CTA), the recurring vocabulary moves,
   what to avoid.
4. Write `layout-systems/<name>/prompt-fragment.txt` — the paragraph
   appended verbatim to every prompt for this layout. Keep under
   ~400 words.
5. Add a single line to `_index.md` registering the layout.

## Naming conventions

- kebab-case, no spaces, no underscores.
- Names describe the compositional metaphor, not the topic.
  `dossier-stack` is good; `cold-email-layout` is bad.
- Avoid generic names like `default`, `standard`, `basic`.
