# Style: bloomberg-feature

Magazine-feature aesthetic in the visual language of a Bloomberg
Businessweek long-read or a Monocle profile spread. Warm cream
paper. Oversized condensed display type. Photoreal cutouts in a
desaturated palette with ONE saturated accent (yellow OR red,
locked per run). Premium B2B trust energy.

This file defines ONLY the brand-consistency layer. Composition,
hero treatment, and decoration on each slide are decided
contextually by the model based on the slide's content.

## When to use

- B2B thought-leadership and feature-piece content.
- Industry-analysis posts, market commentary, founder interviews,
  case studies.
- Posts where the audience expects gravitas without coldness.

DO NOT use for: friendly explainers (`hand-drawn-saas`), breaking
news (`noir-collage`), single-line manifestos (`bold-poster`).

## Palette

Two palette options. Pick ONE at run-init and lock for the entire
carousel.

### Yellow-accent (calm authority)

| Token        | Hex        | Role                                       |
|--------------|------------|--------------------------------------------|
| Cream        | `#F5F0E6`  | Page background. Warm magazine paper.      |
| Ink          | `#0F0E0B`  | Default text, headlines.                   |
| Yellow       | `#F2C744`  | The single accent.                         |
| Mute         | `#6F695A`  | Captions, meta.                            |
| Sepia        | `#9C8466`  | Desaturated cutout tones.                  |

### Red-accent (urgent feature)

| Token        | Hex        | Role                                       |
|--------------|------------|--------------------------------------------|
| Cream        | `#F5F0E6`  | Page background.                           |
| Ink          | `#0F0E0B`  | Default text.                              |
| Red          | `#C8332B`  | The single accent.                         |
| Mute         | `#6F695A`  | Captions, meta.                            |
| Sepia        | `#9C8466`  | Desaturated cutout tones.                  |

Color discipline: cream is the page, NEVER pure white. ONE accent
color per run. Photographic cutouts are desaturated to sepia / B&W
with ONLY ONE small detail in the locked accent. NEVER two accents
in the same run.

## Typography

| Element        | Treatment                                                          |
|----------------|--------------------------------------------------------------------|
| Section number | Tracked-mono "No. NN" in ink, ~14px.                              |
| Headline       | Heavy condensed display sans (Druk / Compressa feel, weight 800-900) OR condensed serif (Caslon Condensed). 60-90px, 1-2 lines, sentence case OR ALL CAPS. ONE phrase in the accent color. |
| Pull-quote     | Oversized italic serif (Tiempos / Caslon Italic), 36-48px, often with an oversized opening quotation mark in the accent. |
| Body           | Sans-serif (Söhne / Inter feel), 18-22px, generous line height.   |
| Attribution    | Tracked monospace, ~12-14px, mute color.                          |
| Page counter   | Tracked mono "No. NN" in ink, with a tiny accent-color dot beside. |

## Voice and bans

- NEVER pure white backgrounds (only cream).
- NEVER two accent colors in one run.
- NEVER saturated color photography (everything desaturated except
  one accent detail).
- NEVER italic serif as the entire headline (italic serif is for
  pull-quotes only; headlines are condensed display).
- NEVER multiple stamps per slide.
- NEVER hand-drawn marker fills (that's hand-drawn-saas).
- NEVER black backgrounds (that's noir-collage).
- NEVER Title Case across multi-word headlines.
- NEVER curved or twisted swipe arrows.
- NEVER drop shadows on type.

Voice register: editorial gravitas. Premium magazine feel.
Restrained.

## Realism

The universal realism rules in `references/designer-moves.md` apply.
For bloomberg-feature specifically:

- Avatars render as photoreal-feeling portraits in desaturated
  sepia / B&W tones with ONE small detail in the locked saturated
  accent (a yellow tie, a red collar, a yellow pen in the hand).
- Mockups (document mockups, dashboards, product cutouts) carry
  plausible content rendered in desaturated tones. Real-looking
  data, real-looking headlines.
- Charts are real (axis labels, real data, real-looking trend
  lines) or absent. Never fake decoration.
- Brand marks are real logos when a brand is named.

## Continuity chrome

- Section number format and position locked across the deck.
- Page counter format ("No. NN" + accent dot) consistent slide-to-slide.
- Hairline rules in the muted color when present.
