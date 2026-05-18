# Style: bold-poster

Pure typographic poster. The TYPE is the slide. Negative space
carries the weight. No diagrams, no illustrations, no content
cards, no photographic elements. The carousel is a sequence of
posters that read together as a manifesto.

Think Helmut Schmid, Jan Tschichold, Wolfgang Weingart — Swiss /
Dutch poster tradition adapted for a feed. Or the closing slide of
an Apple keynote when one line of italic serif fills the screen.

This file defines ONLY the brand-consistency layer. The hero shape
(which typographic treatment, which alignment, how much negative
space, how the type bleeds or breathes) is decided contextually
per slide.

## When to use

- Manifesto carousels — 8-10 declarations the brand believes.
- Single-quote per-slide carousels.
- Reflection / philosophy / values posts.
- Anytime the audience is supposed to FEEL a line, not learn one.

DO NOT use for: explainers, step-by-step content, capability lists,
anything where a diagram would teach better.

## Palette

Two background options. Pick ONE at run-init.

### Off-white background

| Token        | Hex        | Role                                       |
|--------------|------------|--------------------------------------------|
| Off-white    | `#F4EFE5`  | Page background.                           |
| Ink          | `#0C0C0C`  | Default type.                              |
| Accent       | `#C8332B`  | (Or yellow #F2C744 or electric blue #2752E6.) |
| Mute         | `#7A746A`  | Page counter, small captions.              |

### Deep-ink background

| Token        | Hex        | Role                                       |
|--------------|------------|--------------------------------------------|
| Ink          | `#0C0C0C`  | Page background.                           |
| Cream        | `#F4EFE5`  | Default type.                              |
| Accent       | `#F2C744`  | (Or red #E63322 or electric blue #4F7CFF.) |
| Mute         | `#86807A`  | Page counter, small captions.              |

Color discipline: ONE accent per carousel. The accent appears only
as one emphasis word per slide, optionally one underline, and the
page-counter dot. NEVER as a background fill.

## Typography

| Element        | Treatment                                                          |
|----------------|--------------------------------------------------------------------|
| Hero type      | Either: oversized italic display serif (Tiempos Display Italic feel) at 90-140px, OR oversized condensed display sans (Druk Wide / Compressa feel, weight 800-900) at 100-160px, OR knockout type (solid accent block with one word knocked out). |
| Emphasis word  | Same family / weight / size as the headline, in the accent color. ONE per slide. |
| Single underline | Heavy slightly-irregular stroke beneath one keyword. Used in tandem with OR instead of the accent color shift. NEVER both on the same word. |
| Page marker    | Tracked monospace "NN / NN" in mute color with a tiny accent dot. Bottom-left or bottom-right (NOT centered). |
| Wordmark       | Brand wordmark in the opposite bottom corner, small, mute.        |

## Voice and bans

- NEVER diagrams of any kind.
- NEVER illustrations, photographic cutouts, sketched objects.
- NEVER kicker pills, content cards, ticker rows, paperclips,
  stamps, post-its.
- NEVER multiple accent colors in one run.
- NEVER centered everything (vary alignment across the deck).
- NEVER subtitles (the headline IS the entire message).
- NEVER drop shadows on type.
- NEVER Title Case.

Voice register: typographic confidence. Restraint is the look.
Discipline IS the style.

## Realism

The universal realism rules in `references/designer-moves.md` apply.
For bold-poster specifically:

- Avatars are almost always OMITTED — bold-poster is type-only by
  design. The one exception: a single oversized italic-serif
  initial inside a circular block as a typographic stand-in. NEVER
  an empty circle.
- Mockups are not used. If the slide needs a mockup, switch styles.
- Charts are not used. If the slide needs a chart, switch styles.

## Continuity chrome

- Page-marker format ("NN / NN" + accent dot) and corner position
  locked across the deck.
- Brand wordmark position consistent slide-to-slide if present.
