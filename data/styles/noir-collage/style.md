# Style: noir-collage

Investigative documentary aesthetic. Near-black canvas. Halftone
B&W photographic cutouts of buildings, hands, phones, documents
treated as evidence on a corkboard. Red rubber stamps, red dot
bullets, red underlines, red arrows. ALL-CAPS distressed
condensed-serif headlines that feel like wood-type mastheads.
Ticker rows, public-records vocabulary. Journalism-as-theatre.

This file defines ONLY the brand-consistency layer. Composition,
hero treatment, and decoration on each slide are decided
contextually by the model based on the slide's content.

## When to use

- Breaking-news / market / policy commentary.
- Investigative-feel teardowns.
- Money / regulation / "they don't want you to know this" reveals.
- Posts where the format itself implies authority.

DO NOT use for: soft lifestyle posts, friendly explainers
(`hand-drawn-saas`), confessional narratives (`editorial-spread` +
`aca`), single-quote manifestos (`bold-poster`).

## Palette

| Token        | Hex        | Role                                                  |
|--------------|------------|-------------------------------------------------------|
| Noir         | `#0A0A0A`  | Page background. Near-black, slightly warm.           |
| Red          | `#E63322`  | Stamps, dot bullets, underlines, arrows.              |
| Red-deep     | `#9A2014`  | Weathered stamp interior gradient.                    |
| Mute-gray    | `#807A70`  | Kicker labels, ticker numbers, page counter.          |
| Soft-white   | `#EDE9DF`  | Headline text, subtitle bright variant.               |
| Paper-white  | `#F2EDE4`  | Halftone cutout highlights.                           |
| Ink          | `#0A0A0A`  | Dark side of halftone cutouts.                        |

Color discipline: noir background always. NEVER pure black
(#000000) — always slightly warm #0A0A0A. Red is the only chromatic
accent. Everything else is black / white / gray. NEVER red
backgrounds. Total red coverage stays moderate (one stamp + dot
bullets + headline emphasis + arrows per slide).

## Typography

| Element        | Treatment                                                       |
|----------------|-----------------------------------------------------------------|
| Headline       | DISTRESSED CONDENSED SERIF, ALL CAPS, large (60-80px), soft-white. ONE phrase per headline in red. Slight paper-print roughness — NEVER clean digital edges. |
| Subtitle       | ALL CAPS sans, smaller (~18-22px), letter-spaced, soft-white at ~70%. Source attribution feel. |
| Kicker label   | Tracked-monospace uppercase, muted gray. Small (~12-14px).      |
| List item      | Bold condensed sans, ALL CAPS, soft-white. Red underline beneath one keyword. |
| Stamp text     | Slab-serif or condensed sans, ALL CAPS, red. Tilted 8-12°, weathered/distressed edges. |
| Ticker         | Tracked monospace, ~10-12px, muted gray. Numbers and dashes.   |
| Page counter   | Monospace small-caps, muted gray, format "NN/NN".              |

## Voice and bans

- NEVER pure black (#000000) backgrounds.
- NEVER clean digital edges on headlines (must feel printed on rough paper).
- NEVER italic serif headlines (that's aca).
- NEVER hand-drawn marker fills (that's hand-drawn-saas).
- NEVER more than one rubber stamp per slide.
- NEVER more than 4 halftone cutouts per slide.
- NEVER curved or twisted arrows (straight or single-bend only).
- NEVER Title Case headlines.
- NEVER friendly emoji.
- NEVER cream / warm / beige backgrounds (that's bloomberg-feature / aca).

Voice register: cold journalism. Authority through restraint. The
slide should feel like evidence pinned to a corkboard, not like a
press release.

## Realism

The universal realism rules in `references/designer-moves.md` apply.
For noir-collage specifically:

- Avatars render as halftone B&W photographic portraits with
  visible halftone dot pattern. Often side-profile or three-quarter
  angle, NEVER frontal headshots.
- Mockups (document cutouts, screen mockups) carry plausible content
  rendered in the halftone B&W treatment. Real-looking journalism
  headlines, real-looking data, real-looking dates.
- Charts are real (axis labels, real data) or absent. Never fake
  ascending-arrow decorations.
- Brand marks are real logos when a brand is named.

## Continuity chrome

- Subtle film-grain overlay on the noir background, consistent across
  every slide.
- Page counter format and position locked from slide 1.
- Ticker row format consistent across slides that carry one.
