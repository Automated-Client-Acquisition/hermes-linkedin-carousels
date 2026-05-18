# Slide-type templates — aca (editorial)

Per-slide-type composition rules for the `aca` style.

## Safe areas (applies to every slide)

The 1024x1536 canvas has inviolable margins. Nothing — pill, headline,
diagram, page counter — may touch or clip the canvas edges.

- **Top safe-area: 6-8% of canvas height (~90-120px).** The kicker pill
  sits BELOW this margin, never inside it. gpt-image-2-2026-04-21 tends to push
  pills against the top edge unless told otherwise; the prompt and
  this template both lock the pill below the safe-area.
- **Bottom safe-area: 5-7% of canvas height (~75-100px).** The page
  counter and arrow sit above this margin.
- **Left/right safe-area: 5% of canvas width (~50px).** Headlines and
  cards never extend into these gutters.

## Hook slide (slide 1)

- TOP (after the safe-area): kicker pill — white rounded pill, small
  green dot, uppercase tracked mono label (e.g. `OUTBOUND`, `THE HOOK`).
  Pill is centered horizontally and has at least 90px of empty Bone
  above it.
- HERO: massive italic Instrument Serif headline, broken across two
  or three lines, with ONE or TWO emphasis phrases switched to ACA
  Red. The headline takes 50-60% of the canvas height.
- BELOW HEADLINE: a short italic-serif subtitle line in black, ~28px,
  named the supporting claim from the post.
- BOTTOM:
  - Page counter `01/10` centered in JetBrains Mono.
  - To the right of the page counter, a small straight ACA-Red `→`
    arrow glyph. NO curved arrow, NO twisted shape. Just a clean
    horizontal arrowhead.
- No content card on the hook slide. The headline floats on Bone.

## Body slide (slides 2..N-1)

- TOP (after the safe-area): kicker pill, centered horizontally with at
  least 90px of empty Bone above it (same safe-area as slide 1).
- HEADLINE: italic Instrument Serif, large but smaller than the hook
  (~44-52px), with red emphasis where the headline calls for it.
- DIAGRAM ZONE: the slide's diagram, chosen per-slide from the
  `diagrams/` library (`comparison-cards`, `oversized-number`,
  `three-stage-flow`, `marker-checklist`, `timeline`, `funnel`,
  `icon-grid`, `annotated-screenshot`). The diagram sits inside a
  white rounded card (16-20px radius) when the diagram is a list,
  comparison, or grid. Number-led diagrams (oversized-number,
  timeline, funnel) sit on Bone directly without a card.
- For numbered checklists / marker-checklist: each item is preceded by
  a small red-outlined `NN` number box (sharp corners, 1.5pt outline,
  red mono number inside).
- BOTTOM:
  - Page counter `NN/10` centered.
  - To the right of the page counter, a small straight ACA-Red `→`
    arrow glyph. Same as slide 1.

## CTA slide (slide N)

- TOP (after the safe-area): kicker pill, label `THE OFFER` or similar,
  centered horizontally with at least 90px of empty Bone above it.
- HEADLINE: italic Instrument Serif, with the trigger word rendered
  in ACA Red as the emphasis phrase. Example: "Want this in your
  pipeline? Comment **CLAUDE**." (where CLAUDE is red).
- BELOW HEADLINE: subtitle in italic serif, smaller, naming the
  deliverable.
- CTA BUTTON: a pill-shaped ACA-Red filled button with white
  sans-serif text "Comment CLAUDE →" (or whatever the trigger word
  is). Centered. This mirrors the "Start For Free →" button from the
  live site.
- BOTTOM:
  - Page counter `10/10` centered.
  - NO swipe arrow on the final slide.
