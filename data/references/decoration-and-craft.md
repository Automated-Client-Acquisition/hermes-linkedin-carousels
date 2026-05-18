# Decoration and craft — the principles

The single source of truth for the visual ENERGY of every carousel,
regardless of style.

This file used to also catalog specific decoration elements ("torn
paper insert", "rubber stamp", "halftone cutout") and prescribe
decoration kits per style. Those catalogs were removed. They
produced wireframes that all looked alike because the orchestrator
kept reaching for the same fixed elements regardless of slide
content.

The new architecture: the orchestrator describes the slide's
CONTENT (what the slide is ABOUT, what narrative beat it serves);
the style file describes the AESTHETIC WORLD (palette, typography,
voice, brand-consistency chrome); the model composes decoration
contextually based on both. This file describes the FORCES that
make a slide scroll-stop — the principles the orchestrator and the
model should honor — but it does NOT prescribe specific elements.

The realism rules (faces must look like faces; mockups must carry
plausible content; charts are real or absent; brand marks use real
logos) are quality gates documented in
`references/designer-moves.md`. Read both files together.

---

## The eight principles

### 1. Decoration IS the hook

A slide that is JUST `headline + diagram + page counter` loses to
the next post in the feed. What stops the scroll is layered,
intentional decoration on the slide — physical-craft elements that
prove a human composed the page.

What "decoration" means here is contextual to the slide's content
AND the locked style's aesthetic world. An ACA editorial slide
might decorate with a torn newspaper clipping, a paper-clipped
note, a hand-circled phrase in red ink. A noir-collage slide might
decorate with halftone B&W photo cutouts, red rubber stamps,
ticker rows. A hand-drawn-saas slide might decorate with marker
arrows, taped labels, marker handwriting.

The orchestrator does NOT pre-pick decoration elements. The model
composes them based on what the slide is about, in the register the
locked style allows. The principle is: **a finished slide carries
visible craft, layered intentionally, not just typesetting on
empty paper.**

### 2. Texture beats flatness

Pure digital cleanliness reads as corporate-deck boring. Real-
feeling carousels have visible material qualities — paper grain,
ink imperfection, halftone dots, marker stroke wobble, distressed
edges, slight rotation on layered elements. The texture should be
barely perceptible at full resolution but the slide should feel
printed, not exported.

The exact texture vocabulary is style-specific (paper grain for
editorial; film grain for noir; marker imperfection for hand-drawn-
saas). The principle: **flatness is the default failure mode;
adding material texture is what differentiates the slide from a
Figma frame.**

### 3. Annotation beats explanation

The slide should look like someone marked it up — like a print-out
someone circled, arrowed, or underlined. The annotation carries
the argument. A hand-drawn circle around the one number that
matters does more work than three sentences of body copy.

The specific annotation form depends on the style (a red ink
circle for editorial; a marker scribble for hand-drawn-saas; a red
underline + leader-line for noir). The principle: **show that a
human looked at this and made a point. Don't just arrange shapes.**

### 4. One spicy element per slide

Every slide has ONE moment — the eye-magnet that earns the swipe.
Two spicy elements compete. Three is chaos. One is a hook.

The spicy element changes per slide so the deck isn't 12 versions
of the same gesture. It should match the slide's content (a
strike-through on a "kill the old way" slide; an oversized
quotation mark on a manifesto slide; a wax seal on a verdict
slide). The orchestrator and the model choose the element together
based on content.

### 5. Color discipline

Almost every great carousel runs on TWO colors: a background
neutral and ONE accent. The accent appears sparingly — on
emphasis words, on annotations, on the brand chrome. The instant a
slide has three competing accent colors, the energy collapses.

Each style locks its palette. The principle: **color screams the
loudest when it's used the least. Hold the accent for the moments
that matter.**

### 6. Asymmetry and tension

Perfect grids read as institutional and dead. Real carousels have
elements rotated 1-4° off-axis, headlines pushed slightly
off-center, weight balanced on one side with intentional negative
space on the other, occasional overlap between elements.

This does NOT mean random — every off-axis rotation is
deliberate. The principle: **lean against the grid, don't worship
it.**

### 7. Continuity is the second hook

Slide 1 makes someone start swiping. Continuity makes them finish.
The carousel must feel like ONE artifact, not 12 disconnected
slides.

The continuity-locked elements are: the palette, the typography
family, the kicker treatment (if the style uses one), the page
counter format and position, the brand wordmark treatment. These
stay consistent across every slide in a run.

Everything ELSE (hero composition, decoration, spicy element)
varies per slide based on content. The continuity lives in the
locked chrome. The variety lives in the contextual decoration.

### 8. The headline is short, confident, and styled

Long headlines kill carousels. Long headlines also break
gpt-image-2-2026-04-21 (the model misspells anything past ~5
words). The fix is the same in both cases: cut.

- **1-6 words.** No exceptions for body slides. Hook and CTA can
  flex to 7-8 if the rhythm demands.
- **Styled, not plain.** The headline is rendered per the locked
  style — italic Instrument Serif for ACA, ALL-CAPS distressed for
  noir-collage, bold sans for hand-drawn-saas, etc. Never a plain
  default sans-serif headline.
- **One emphasis element.** ONE word or phrase carries the visual
  stress (a color shift, an underline, a strike-through, a
  highlighter swipe). Two emphases dilute each other.
- **Sentence case OR ALL CAPS, never Title Case.** Title Case reads
  as a press release.

Long body explanation lives in the post caption, never on the
slide.

---

## How the orchestrator uses these principles

These are forces, not checklists. The orchestrator reads them
before writing visual notes for a deck, and confirms each visual
note honors them — but the orchestrator does NOT translate the
principles into "the slide must have X element from list Y."

For each visual note the orchestrator writes:

- Is the slide more than just `headline + diagram + page counter`?
  (Principle 1)
- Does the slide carry visible texture / material quality?
  (Principle 2)
- Is there a clear annotation — something marked up — pointing at
  the slide's argument? (Principle 3)
- Is there ONE clear focal point, not three? (Principle 4)
- Is the color discipline held — accent used sparingly? (Principle 5)
- Is there intentional asymmetry / tension somewhere? (Principle 6)
- Do the continuity-locked elements (chrome) match the rest of
  the deck? (Principle 7)
- Is the headline 1-6 words, styled, with one emphasis? (Principle 8)

When the answer to any of these is "no", fix the visual note. When
all eight are honored, generate. The model composes the actual
decoration based on the slide's content and the locked style's
aesthetic world.
