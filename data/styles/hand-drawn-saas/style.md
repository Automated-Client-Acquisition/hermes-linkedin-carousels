# Style: hand-drawn-saas

Whiteboard-explainer aesthetic. Bold black sans-serif headlines on
white, with hand-drawn marker illustrations and annotations as the
visual texture. Reads as "smart consultant explaining at a
whiteboard."

This file defines ONLY the brand-consistency layer (palette,
typography, voice, realism, continuity chrome, when-to-use).
Composition, hero shape, and decoration on each slide are decided
contextually by the model based on the slide's content.

## When to use

- Educational explainers, step-by-step content, frameworks.
- B2B / SaaS / agency content where a well-drawn diagram trusts
  better than a stock photo.
- Posts where the value of the slide is **explaining something
  clearly**, not establishing mood.

DO NOT use for: investigative / breaking-news content
(`noir-collage`), premium magazine features (`bloomberg-feature`),
manifesto carousels (`bold-poster`).

## Palette

| Token         | Hex        | Role                                            |
|---------------|------------|-------------------------------------------------|
| Background    | `#FFFFFF`  | Pure white page background.                     |
| Ink           | `#0A0A0A`  | Headline + body type + diagram outlines.        |
| Subtle ink    | `#6B7280`  | Subtitle + small footer text.                   |
| Accent blue   | `#2563EB`  | Marker fill A, kicker label color.              |
| Accent orange | `#F97316`  | Marker fill B, keyword underlines.              |

Color discipline: pure white page, two-color marker scheme only (blue
+ orange + black + white). NEVER red. NEVER green / purple / pink.
NEVER beige / cream / off-white backgrounds.

## Typography

| Element        | Family                       | Treatment                                       |
|----------------|------------------------------|-------------------------------------------------|
| Headline       | Sans-serif (Inter / Helvetica) | Weight 700-800, sentence case, tight leading, ~44-56px. Black. |
| Subtitle       | Sans-serif (Inter)           | Regular weight, subtle ink color, ~18-22px.    |
| Kicker label   | Sans-serif (Inter)           | UPPERCASE, tracked +0.1em, Accent Blue, small. |
| Inside-diagram labels | Hand-drawn marker handwriting | Looks like real handwriting, not typeset. |
| Page counter   | Sans-serif (Inter)           | Small, black, format "NN/NN" centered at bottom. |

Headlines are bold black sans, sentence case, never italic, never
serif. The contrast between clean typeset headlines and hand-drawn
diagrams IS the look.

## Voice and bans

- NEVER italic type anywhere.
- NEVER serif type anywhere.
- NEVER beige / cream / off-white backgrounds (pure white only).
- NEVER red (the accent palette is blue + orange).
- NEVER Title Case headlines.
- NEVER rubber stamps (FILED / MEMO / DOSSIER) — that's noir-collage.
- NEVER halftone B&W photo cutouts — that's noir-collage.
- NEVER vector-perfect shapes (every diagram element should look
  hand-drawn).

## Realism

The universal realism rules in `references/designer-moves.md` apply.
For hand-drawn-saas specifically:

- Avatars render as hand-drawn marker portraits — simple but
  clearly human faces with marker outlines and soft fills in the
  locked blue or orange palette. NEVER empty circles or monogram
  initials.
- Mockups carry plausible marker-handwritten content. The sketch
  vocabulary allows wobbly placeholder hairlines on body type
  inside sketched cards (this is the one style where placeholder
  hairlines read as deliberate sketch).
- Charts are real (axis labels, real data line, real numbers) or
  absent.
- Brand marks are real logos when a brand is named — passed via
  `--reference assets/logos/<brand>.svg`.

## Continuity chrome

- Page counter format and position locked from slide 1 (typically
  centered at the bottom).
- No kicker pill — hand-drawn-saas uses a plain Accent-Blue uppercase
  kicker label at the top instead.
- The "SWIPE →" affordance in marker handwriting appears ONLY on
  slide 1, in Accent Blue.

Everything else (hero composition, decoration, diagram type per
slide) is content-driven and composed by the model.
