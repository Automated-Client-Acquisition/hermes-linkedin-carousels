# Style: wired-magazine

Design-forward magazine aesthetic that feels like a creative director's
marked-up proof. Clean white backgrounds, bold condensed sans-serif
display headlines, saturated accent — but with HANDWRITTEN energy.
Marker annotations, scribbled circles around key words, margin notes,
hand-drawn arrows, underlines. The slide looks like a WIRED or Fast
Company spread that a designer attacked with a sharpie — stylish,
human, opinionated. Not sterile. Not corporate. A magazine that
someone actually touched.

This file defines ONLY the brand-consistency layer. Composition,
hero treatment, and decoration on each slide are decided
contextually by the model based on the slide's content.

## When to use

- Product launches, feature reveals, announcements — big energy, one
  hero idea per carousel.
- Industry takes, opinion pieces, trend analysis — authoritative
  voice, bold claims, handwritten emphasis.
- Comparison/review carousels — multiple products with marker
  annotations calling out key differences.
- Any tech/startup content where the visual register should say
  "this is important and a real human made this."

DO NOT use for: quiet/meditative content, breaking news (use
noir-collage), friendly B2B whiteboard explainers (use
hand-drawn-saas), premium warm-toned features (use bloomberg-feature),
manifesto/poster-only content (use bold-poster).

## Palette

One accent color per carousel. Pick ONE at run-init.

### electric-blue (canonical)

| Token       | Hex        | Role                                          |
|-------------|------------|-----------------------------------------------|
| Paper       | `#FAFAFA`  | Clean white page background. Never cream.      |
| Ink         | `#0D0D0D`  | Default text. Near-black, not pure #000.       |
| Accent      | `#0055FF`  | Electric blue. Emphasis words, marker strokes, graphic blocks, rules. |
| Muted       | `#707070`  | Captions, labels.                             |
| Rule        | `#E0E0E0`  | Subtle dividing lines.                        |

### Alt accents (one per run)

| Accent      | Hex        | Role                                          |
|-------------|------------|-----------------------------------------------|
| Neon Green  | `#00DD55`  | High-energy tech, startup, growth content.     |
| Hot Pink    | `#FF3366`  | Opinion pieces, bold takes, culture content.   |
| Yellow      | `#FFCC00`  | Product launches, optimistic announcements.    |

Color discipline:

- Paper is clean white (#FAFAFA). NEVER cream, bone, or warm paper.
- ONE accent color per carousel. The accent appears as emphasis
  words inside headlines, solid-color background blocks behind
  white text, thin rules, AND handwritten marker annotations.
- Handwritten marks (circles, arrows, underlines, margin notes,
  strike-throughs) are drawn in the accent color using a marker-like
  stroke — visible ink texture, not a perfect vector line. 1.5-2px
  stroke weight, slightly imperfect, like a real sharpie on paper.
- Flat solid color blocks ONLY. NO gradients.
- NO drop shadows on type or cards.
- The accent is bold and saturated — this is a loud magazine, not a
  restrained one.

## Typography

| Element              | Treatment                                                   |
|----------------------|-------------------------------------------------------------|
| Headline             | Bold condensed or wide sans-serif display (Druk Wide / Akzidenz-Grotesk Condensed / Helvetica Now Display feel), 60-100px, sentence case, tight tracking (-0.02em). ONE emphasis word per headline in the accent color. |
| Emphasis word        | Same family/weight/size as headline, in the accent color. MAX one per headline. Optionally circled with a hand-drawn accent marker ring. |
| Pull-quote           | Italic editorial serif (Tiempos Text feel), 28-40px, either near-black or accent-colored. Often underlined with a hand-drawn accent stroke. Used sparingly — one per carousel max. |
| Body copy            | Clean geometric sans-serif (Inter / Graphik feel), 18-24px, near-black. Short blocks, never paragraphs. |
| Kicker label         | Tracked uppercase sans-serif or mono, 12-14px, small. Can appear as a simple label in muted or as white text inside a solid-accent pill. Sometimes accompanied by a handwritten checkmark or star in the accent color. |
| Page counter         | Two styles: (a) hand-drawn marker-style number in accent color, slightly tilted, lower corner — "1 / 10" written as if with a marker. OR (b) tracked mono muted with accent dot for current page. Pick one per carousel and lock it. |
| Wordmark             | Brand wordmark, small, bottom corner opposite the page counter. |
| Handwritten annotations | Accent-color marker strokes: circles around key words, underlines, margin arrows, checkmarks, stars, scribbled notes. 1.5-2px lines with visible marker texture — slightly imperfect, like a real human drew them. Used on 2-3 slides per carousel, not every slide. |

Typography rules:

- Headlines are ALWAYS sans-serif display. NEVER serif headlines.
- NEVER Title Case headlines (sentence case only).
- Tight tracking on headlines (-0.02em) — the compression IS the
  magazine look.
- Body copy is short — one line per slide max.
- The type hierarchy is: BIG SANS HEADLINE → small body line →
  tiny page counter. No middle weights.
- Handwritten annotations should feel ORGANIC, not templated. Vary
  the annotation type slide to slide: marker circle on slide 2,
  margin arrow on slide 4, underlined key phrase on slide 7.

## Voice and bans

- NEVER gradients — flat solid color blocks only.
- NEVER drop shadows on anything.
- NEVER serif headlines (sans-serif display ONLY).
- NEVER warm/cream/off-white backgrounds — clean white (#FAFAFA)
  only.
- NEVER more than one accent color per carousel.
- NEVER centered everything — use asymmetric, kinetic layouts.
- NEVER emoji on slides.
- NEVER fluorescent neon overkill (one accent is bold; three is
  a rave).
- NEVER halftone or risograph misregistration — this is NOT
  risograph-zine. The aesthetic is design-magazine + sharpie, not
  indie print shop.
- NEVER empty, sterile "corporate deck" energy. Every slide should
  feel like a human designer touched it. At least one hand-drawn
  element per slide: a circle, an underline, an arrow, a margin note.

Voice register: confident, kinetic, opinionated — but with a human
hand visible on every spread. The slide should feel like a WIRED
feature that got marked up by the art director at 2 AM with a blue
sharpie. Stylish, not sterile.

## Realism

The universal realism rules in `references/designer-moves.md` apply.
For wired-magazine specifically:

- Avatars: High-contrast editorial photography with graphic accent-
  color overlays. Clean, modern, recognizable faces. Optionally
  circled or annotated with a hand-drawn accent marker ring. NEVER
  empty circles, monogram initials, or silhouettes.
- Mockups: Clean UI screenshots on device frames or flat white
  cards. Plausible content, no lorem ipsum. Annotated with hand-
  drawn accent arrows pointing to key features.
- Charts: Clean vector-style charts with accent-color data lines.
  Real axis labels, real data. Key data points annotated with hand-
  drawn marker circles. NEVER fake ascending-arrow decorations.
- Brand marks: Real logos, clean placement on white. When a brand
  is named on a slide, pass the actual logo as a reference image.
  NEVER typographic approximations.

## Continuity chrome

- Clean white (#FAFAFA) background on every slide.
- Page counter format and corner position locked across the deck.
- The single accent color locked across every slide.
- Brand wordmark position consistent slide-to-slide.
- Graphic overlay vocabulary (solid color blocks, thin rules,
  geometric shapes) consistent across the deck.
- Handwritten annotation style (marker stroke weight, imperfection
  level) consistent across the deck.
