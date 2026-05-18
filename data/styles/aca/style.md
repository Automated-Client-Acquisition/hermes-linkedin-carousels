# Style: aca (editorial, real ACA brand)

The aesthetic world of the live automatedclientacquisition.com site.
Carousels in this style look like extensions of the site, not
separate marketing artifacts.

This file defines ONLY the brand-consistency layer:

- **Palette** — the locked hex codes.
- **Typography** — the locked type families and treatment rules.
- **Voice** — banned vocabulary and brand voice anchors.
- **Realism** — how avatars and mockups render in this style.
- **Continuity chrome** — the elements that stay consistent across
  every slide in a run.

Everything else — composition, decoration, hero treatment, layout
shape per slide — is decided contextually by the model based on
each slide's content and the locked layout system's vibe. The
style does NOT prescribe a decoration kit, a composition recipe,
or per-slide hero-zone treatments.

## When to use

- ACA-branded carousels. This is the default for the brand.
- Editorial, explanatory, or "serious operator" content.
- Any post where the brand wants to feel like a peer publication
  to a business magazine, not a SaaS marketing deck.

If the post is breaking news / policy / market commentary, consider
`noir-collage` instead. If the post is a friendly explainer with
sketched diagrams, consider `hand-drawn-saas`. If the post is a
premium magazine feature, consider `bloomberg-feature`.

## Palette

| Token       | Hex        | Role                                          |
|-------------|------------|-----------------------------------------------|
| Bone        | `#F2EEE6`  | Page background. Warm paper. Never white.     |
| Card        | `#FFFFFF`  | White content cards on the Bone background.   |
| Ink         | `#15140F`  | Default text and outlines.                    |
| ACA Red     | `#D4361A`  | The only chromatic accent.                    |
| Muted       | `#6B6759`  | Captions, meta, small mono labels.            |
| Rule        | `#C9C2AE`  | Hairline rules on Bone.                       |
| Green dot   | `#2EA66F`  | Small status dot inside kicker pills only.    |

Color discipline:

- Bone is the page background. NEVER pure white outside of content
  cards.
- ACA Red is the only chromatic accent. Used as text color for
  emphasis phrases inside black headlines, as the outline of any
  red-outlined chrome elements, as the color of accent annotations
  and the page-counter arrow. Never as a background fill (except
  inside knockout-type blocks, where red is the field and type
  knocks through).
- No gradients. No drop shadows on type.

## Typography

| Element                | Family                            | Treatment                                       |
|------------------------|-----------------------------------|-------------------------------------------------|
| Headline               | Instrument Serif (or close serif) | ITALIC, large display, lowercase or sentence case. Mixed deep Ink + ACA Red emphasis phrases. |
| Emphasis phrase in headline | Instrument Serif             | ITALIC, same size as the rest of the headline, in ACA Red. |
| Pull-quote             | Instrument Serif                  | ITALIC, smaller than headline, often with one red emphasis word. |
| Body copy              | Sans-serif (Inter feel)           | Black on white card or black on bone. Plain weight. |
| Kicker label           | JetBrains Mono                    | UPPERCASE, tracked +0.1em, small. Black inside a small white rounded pill with a tiny green dot bullet. |
| Page counter           | JetBrains Mono                    | small-caps, black on bone, format "NN/NN" with a small straight ACA-Red right-arrow glyph (→) on body slides. |
| Brand wordmark `aca.`  | Bricolage Grotesque feel          | Italic display sans, lowercase, black letters with the trailing period in ACA Red. |

Typography rules:

- The headline is the visual hero. Set it big, set it italic serif,
  use the red emphasis trick deliberately — one or two phrases per
  headline maximum.
- NEVER sans-serif headlines (italic serif only).
- NEVER em dashes anywhere in body copy.
- NEVER exclamation marks anywhere.
- NEVER Title Case headlines (sentence case OR lowercase only).
- NEVER curved or twisted swipe arrows. The page-counter arrow is a
  straight ACA-Red → glyph.

## Voice and banned vocabulary

ACA inherits from the `senior-operator` voice library entry (see
`voices/senior-operator/voice.md`). Anti-hype, declarative, lowercase
italic moments allowed. The brand-specific bans on top of the
senior-operator baseline:

- NEVER "leads" as a noun for prospects. Use "meetings", "buyers",
  "pipeline", "prospects".
- NEVER "AI-powered". The brand USES AI; the brand doesn't sell it.
- NEVER "ambitious founders" framing.
- NEVER "we'll help you grow." The brand replaces cold outreach; it
  doesn't help.
- NEVER emoji on slides (rare emoji in post copy only, restrained).
- NEVER FILED / MEMO / DOSSIER stamps (the editorial-dossier
  vocabulary was explicitly removed from the brand).
- NEVER halftone B&W photographic cutouts (that's noir-collage; for
  ACA, photographic mode uses warm sepia tones on cream paper).
- NEVER hand-drawn marker fills (that's hand-drawn-saas).
- Total red coverage stays moderate. Red is the typographic stress
  voice, used sparingly.

Stock phrases (use sparingly, max one per deck): "meetings, not
leads." / "booked, not browsed." / "we replace your cold outreach."
/ "pipeline as a system."

## Realism (inherited)

The universal realism rules in `references/designer-moves.md` apply.
For ACA specifically:

- Avatars are rendered as editorial illustration in Le Monde / The
  New Yorker portrait style — soft tonal washes, simplified facial
  features, gentle line work. NEVER empty Ink-outlined circles,
  monogram initials, gray rectangles, or silhouettes.
- Mockups (email previews, profile cards, document mockups, dashboards)
  carry plausible italic-serif body content. NEVER lorem ipsum.
  NEVER empty gray hairlines pretending to be readable text.
- Charts are real (axis labels, real-looking data line, anchor stats
  the operator can stand behind) or absent. NEVER fake ascending-arrow
  decorations pretending to be data.
- When a brand or product is named on a slide, pass the actual logo
  as `--reference assets/logos/<brand>.svg`. See
  `assets/logos/_index.md` for the lookup table.

## Continuity chrome (locked across every slide in a run)

These elements stay consistent slide-to-slide so the deck reads as
ONE artifact:

- The kicker pill (when used) — small white rounded pill with a
  tiny green status dot and uppercase tracked-monospace black
  label. Same format across the deck.
- The page counter — JetBrains Mono small-caps "NN/NN" + straight
  ACA-Red right-arrow glyph on body slides, no arrow on the closing
  slide. Same position across the deck (corner-locked from slide 1).
- The brand wordmark "aca." — italic display sans with red period.
  Appears once, on the closing CTA slide.

EVERYTHING ELSE — what hero shape each slide takes, what decoration
goes on it, what physical-craft elements appear — is decided
contextually based on the slide's content. The style does not
prescribe. The model composes within this aesthetic world.
