# Slide-type templates — aca (hand-drawn SaaS)

Per-slide-type composition rules for the `aca` style. The orchestrator
(Claude) reads this when writing each slide's Visual note in
`script.md` and the final prompt for `generate.py`.

## Hook slide (slide 1)

- TOP: small uppercase tracked sans kicker in Accent Blue
  (e.g. `AI SEARCH`, `COLD EMAIL`, `OUTBOUND`).
- Below: massive bold black sans headline, sentence case, two lines
  ideally, ~52-64px size.
- Below the headline: a one-line subtitle in subtle gray (#6B7280)
  that delivers the promise of the carousel in plain language.
- HERO: a single small hand-drawn marker illustration that anchors
  the topic visually — usually two or three sketched objects with
  arrows between them (e.g. two document icons with a curved arrow
  between them, a small chart, an icon pair). Generous margin.
- Bottom: page counter `01/10` centred in small black sans.
- **The word "SWIPE" written in marker handwriting with a curved
  arrow after it, in Accent Blue, sits just below the illustration**
  — this is the slide-1 swipe affordance and is unique to slide 1
  (does not appear on slides 2-N).

## Body slide (slides 2..N-1)

- TOP: kicker in Accent Blue, sentence-case headline, optional
  subtitle in gray.
- HERO: one hand-drawn marker diagram. Pick the diagram type that
  best explains the slide's lesson. Common diagram types:
  - **Comparison cards** — two sketched rectangular cards stacked
    vertically, one with a Blue "tape" label, one with an Orange
    "tape" label. Each card contains a short hand-drawn line of
    text. (Best for "wrong way vs right way" or "buried vs front".)
  - **Three-stage flow** — three boxes connected by curved hand-drawn
    arrows, blue-fill boxes on the left and orange-fill boxes on
    the right. (Best for cause-and-effect or process explainers.)
  - **Oversized number** — one giant marker-drawn number (`88%`,
    `3x`, `0.5%`) filling most of the hero zone, in Accent Blue
    marker fill with black outline, plus a hand-drawn underline in
    Accent Orange under the number. A short marker-handwriting line
    sits below the number. (Best for stat slides.)
  - **Annotated screenshot** — a sketched-frame "browser window"
    or "phone screen" with marker-drawn arrows and circles
    highlighting a specific element inside it. (Best for "look at
    this specific thing" slides.)
  - **Checklist with marker checkmarks** — a vertical stack of short
    items, each preceded by a hand-drawn Accent Blue checkbox or
    Accent Orange underline. (Best for "things to do" slides.)
- Bottom: page counter `NN/10`, centred, black sans.
- NO swipe arrow on body slides.

## CTA slide (slide N)

- TOP: kicker reading something like `THE OFFER`, `GET IT`, or
  `YOURS`, in Accent Blue.
- Headline: bold black sans, sentence case, names the deliverable
  ("The full pre-flight checklist. Yours.")
- Subtitle: short gray line explaining what the reader gets.
- HERO: a hand-drawn marker illustration of the lead magnet — a
  sketched document with a few lines drawn inside it, a curved
  Accent Blue arrow pointing toward the comment box (sketched as a
  small chat-bubble shape with the trigger word `CHECKLIST` written
  in marker handwriting inside it), and a small Accent Orange
  underline beneath the trigger word.
- Below the illustration: in larger marker handwriting, the
  instruction `Comment CHECKLIST` with a hand-drawn arrow pointing
  to a chat bubble — the same trigger word, repeated for clarity.
- Bottom: page counter `10/10`, centred.
- No inversion. The CTA slide is white like every other slide. The
  visual signal that this is the close is the lead-magnet illustration
  and the explicit "Comment X" instruction.
