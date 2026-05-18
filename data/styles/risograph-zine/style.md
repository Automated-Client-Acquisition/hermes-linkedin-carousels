# Style: risograph-zine

DIY two-color risograph / screen-print aesthetic. Slightly off-white
paper. Halftone-textured everything. Two saturated spot inks
deliberately MISREGISTERED by 2-4px — the misalignment IS the look.
Hand-drawn illustrations. Indie-zine / art-school / late-90s
shareware energy.

This file defines ONLY the brand-consistency layer. Composition,
hero treatment, and decoration on each slide are decided
contextually by the model based on the slide's content.

## When to use

- Irreverent founder posts.
- Indie-tech, design-aware audience content.
- Hackathon recaps, demo-day artifacts, conference highlights.
- Self-deprecating brand-voice posts where polish would feel wrong.
- Audiences that recognize and reward the risograph aesthetic.

DO NOT use for: serious B2B pitches, breaking news (`noir-collage`),
C-suite audiences who value polish, premium-magazine register
(`bloomberg-feature`).

## Palette

Two-ink combinations. Pick ONE combo at run-init.

### fluoro-pink + electric-blue (canonical)

| Token        | Hex        | Role                                       |
|--------------|------------|--------------------------------------------|
| Paper        | `#F2EBDB`  | Page background.                           |
| Pink         | `#FF6699`  | Spot ink A — fluorescent magenta.          |
| Blue         | `#2552B8`  | Spot ink B — electric blue.                |
| Ink          | `#1A1A1A`  | Sparingly, for type or small marks.        |

### sun-yellow + black

| Token        | Hex        | Role                                       |
|--------------|------------|--------------------------------------------|
| Paper        | `#EEE6CC`  | Page background.                           |
| Yellow       | `#FFD23F`  | Spot ink A.                                |
| Black-ink    | `#0F0F0F`  | Spot ink B.                                |

### teal + coral

| Token        | Hex        | Role                                       |
|--------------|------------|--------------------------------------------|
| Paper        | `#F2EBDB`  | Page background.                           |
| Teal         | `#0E7B7E`  | Spot ink A.                                |
| Coral        | `#F26A52`  | Spot ink B.                                |

Color discipline: TWO inks per carousel, never three. Both inks
always carry visible halftone dot texture in fills. Every two-color
element is deliberately misregistered 2-4px. Paper background is
NEVER a third color — it's the absence of ink.

## Typography

| Element        | Treatment                                                          |
|----------------|--------------------------------------------------------------------|
| Kicker         | Tracked-monospace ALL CAPS or chunky condensed sans, in the darker ink, ~14-18px, with slight halftone texture. |
| Headline       | Varied per slide — chunky display sans (Cooper Black / Goudy Heavyface feel), bouncy display, distressed condensed serif, or marker-handwritten. 50-80px. |
| Pull-quote     | Oversized italic display in ink A, with misregistered shadow in ink B. |
| Body           | Sans-serif typewriter feel (Courier / Pitch feel) in the darker ink, ~18-22px. |
| Page marker    | Hand-written marker "PG NN" or "NN" in the darker ink, lower-corner, slightly tilted. |

## Voice and bans

- NEVER three or more colors (paper is not a color).
- NEVER perfectly aligned two-color elements (misregistration is
  the point).
- NEVER solid flat fills (halftone dots always visible).
- NEVER clean Helvetica / Inter as the only typography.
- NEVER glassmorphism, modern UI drop shadows, gradients (except
  halftone).
- NEVER Pixar / 3D illustrations.
- NEVER photoreal photography (photos get polaroid + halftone
  treatment).
- NEVER pure white backgrounds.
- NEVER vector-perfect shapes.

Voice register: irreverent, DIY, charming-clumsy. The slide should
feel printed by someone who is OK with smudges.

## Realism

The universal realism rules in `references/designer-moves.md` apply.
For risograph-zine specifically:

- Avatars render as two-ink halftone portraits with deliberate
  2-4px misregistration. Charming-clumsy faces, recognizably human,
  printed-paper feel. NEVER empty circles.
- Mockups render in halftone with both inks misregistered. Plausible
  content visible.
- Charts are real (axis labels, real data) rendered in two-ink
  halftone, OR absent.
- Brand marks are real logos when a brand is named.

## Continuity chrome

- The two locked spot inks across every slide.
- Heavy paper grain texture across every slide.
- Page-marker format and position consistent slide-to-slide.
- Optional zine decoration (staple-mark glyph, perforation line) if
  used, locked across the deck.
