# Designer moves — quality floor

This file used to be a catalog of 32 named visual moves with
paste-ready prompt snippets. The catalog was removed because it
turned the orchestrator into a vending machine: pick element 4 from
column A, render it. Slides came out mechanical and repetitive.

The new architecture is content-driven. **The orchestrator describes
WHAT THE SLIDE IS ABOUT. The model (gpt-image-2-2026-04-21) decides
WHAT TO RENDER based on that content, within the locked style's
aesthetic world** (palette + typography + voice + brand consistency
chrome).

This file now contains only **quality-floor rules** — the visual
standards every slide must meet regardless of style or content.
These are not creative suggestions; they are quality gates.

---

## AVATARS AND MOCKUPS — THE REALISM RULE

The most common failure mode in AI-generated carousels: empty
avatar circles, screen mockups with lorem ipsum, profile cards with
three horizontal gray lines pretending to be a name + title + bio.
These slides look unfinished. The reader sees "the designer didn't
bother to fill this in" and the trust dies.

**Avatars must have faces. Mockups must have plausible content.**

### When the slide includes a human avatar

Every avatar — circular or rectangular, primary subject or
background deck — MUST be rendered as a recognizably human portrait.
NEVER:

- An empty Ink-outlined circle.
- A flat solid colored circle.
- A monogram letter (e.g. "S" inside a circle) standing in for a
  face.
- A silhouette / dark featureless head shape.
- A gray rectangle where the face would be.

The portrait treatment is contextual to the slide's style — an ACA
slide renders avatars as editorial illustration (Le Monde / The New
Yorker portrait feel); a noir-collage slide renders them as halftone
B&W photographic portraits; a hand-drawn-saas slide renders them as
sketched marker portraits; a bloomberg-feature slide uses photoreal
with one saturated accent detail; a risograph-zine slide uses
two-ink halftone with deliberate misregistration. The model picks
the treatment to match the locked style.

When the carousel calls for multiple avatars on one slide (e.g. a
multi-account deck), each avatar must be a DIFFERENT person —
varied gender, age, ethnicity, hair, attire — so the slide reads as
a real distribution of humans, not three copies of the same
template.

### When the slide includes a screen / UI / document mockup

Every mockup — phone screen, laptop screen, browser window,
document, chat interface, email preview, profile card — MUST carry
plausible content. NEVER:

- Lorem ipsum text.
- Generic gray horizontal bars where readable text should be (the
  one exception: hand-drawn sketched diagram lines in marker styles,
  where wobbly placeholder hairlines clearly read as deliberate
  sketch, not unfinished mockup).
- Empty rectangles with no internal content.
- Made-up brand logos that look like fake stock-photo brand names.
- Random unrelated content (a screenshot of a weather app inside a
  carousel about cold email).

Plausible content means:

- **Email mockup:** real-feeling subject line, sender name, one or
  two preview lines that match the carousel's topic.
- **LinkedIn / social profile mockup:** plausible first name + last
  initial, realistic-sounding title, plausible company name. Avoid
  naming real people unless explicitly authorized.
- **Dashboard / chart mockup:** real numbers that match the
  carousel's argument. If the slide claims "<60s", the dashboard
  shows a time of 47s or 52s. If the slide claims "47 replies", a
  number near 47 appears on the chart.
- **Chat / DM mockup:** a plausible message that the topic would
  generate, with a realistic-sounding sender name.
- **Document / dossier mockup:** a plausible header, plausible body
  lines that match the topic, plausible page numbers.

---

## DATA AND CHARTS — THE NO-FAKE-CHART RULE

If a slide carries a chart, it must be a real chart with real-looking
data. If it carries a stat, the operator must be able to stand
behind the number. If neither, don't invent chart-shaped decoration
to fill space.

Specifically forbidden:

- "N ascending arrows on a baseline forming an implied slope."
  This is not a chart. It is decoration pretending to be data.
- A chart frame with no axis labels and no data line / bars — just
  an empty rectangle with arrows or shapes inside.
- A percentage stat ("+47%") as a callout on a slide where the
  operator has not verified that number. Made-up stats destroy
  trust faster than fake charts do.

If the slide is about growth, compounding, improvement, or any
data-shaped concept and the operator does NOT have a real number to
anchor it, the slide should be a typographic moment instead — a
pull-quote, a single declarative line, an oversized italic word.
Let the words do the work. Don't reach for chart-shaped decoration
because the slide "needs to look dense."

---

## BRAND MARKS — THE REAL-LOGO RULE

When a slide names a brand or product (LinkedIn, Telegram, Discord,
Claude, GPT, Gemini, Stripe, Notion, etc.), pass the actual logo as
the reference image to generate.py via
`--reference assets/logos/<brand>.svg`. The model uses the
reference to render the real mark at the position the visual note
specifies.

See `assets/logos/_index.md` for the full lookup table, aliases,
and typographic fallbacks for brands whose owners removed their
logos from SimpleIcons (LinkedIn, Slack, OpenAI/ChatGPT,
Salesforce).

Endorsement guardrails: if the slide implies endorsement,
partnership, or affiliation with the brand — or if the slide
disparages the brand — DO NOT use the real logo. Use a typographic
fallback. Trademark fair use covers neutral / descriptive /
positive references only.

---

## How the orchestrator uses this file

At STEP 4 (art), the orchestrator confirms each slide's visual
note meets these three rules before generating:

1. **Avatars and mockups carry real faces / real content** — no
   empty placeholders, no lorem ipsum, no monogram circles.
2. **Charts are real or absent** — no fake ascending-arrow
   decorations pretending to be data, no made-up stats.
3. **Brand marks pass the real logo** when a brand is named (and
   the endorsement guardrails allow it).

These are quality gates, not creative suggestions. Everything ELSE
the slide carries — composition, decoration, hero element, paper
artifacts, annotations, layout — is decided contextually by the
model based on the slide's content and the locked style's
aesthetic world. The orchestrator does NOT pick decoration from a
catalog.

The realism rules above prevent AI-slop. The style's prompt
fragment provides the aesthetic world. The visual note provides the
content. That's the entire art-step contract.
