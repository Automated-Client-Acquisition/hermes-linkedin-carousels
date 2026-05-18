# Slide-type templates — noir-collage

Per-slide-type composition rules for noir-collage. The orchestrator
reads this when writing each slide's Visual note.

## Hook slide (slide 1)

- TOP: tracked-mono kicker label in muted gray ("EVIDENCE", "ON
  RECORD", "BREAKING").
- HEADLINE: ALL-CAPS distressed condensed serif, white with ONE red
  phrase, 1-2 lines, ~60-80px.
- SUBTITLE: ALL-CAPS sans, source attribution ("FILED MAY 17, 2026.
  TREASURY ON RECORD.").
- HERO: a single anchor cutout (a building, a document, a closed
  envelope) with a red rubber stamp slammed across it. NO arrows on
  slide 1 — the collage is one element, the focal stamp is the spicy
  element.
- FOOTER: ticker row, page counter `01/NN`.

## Body slide (slides 2..N-1)

- TOP: kicker.
- HEADLINE: distressed serif ALL CAPS with one red phrase.
- SUBTITLE: optional, source attribution or one-line context.
- HERO: pick the diagram type:
  - **Mechanism** — 2-4 halftone cutouts with red straight arrows
    showing flow (issuer → buys bond → mints token).
  - **Comparison** — 2 halftone cutouts side by side under "OLD PATH"
    and "NEW PATH" labels, with red dot bullets under each.
  - **Exhibit** — one large halftone cutout (a document, a screen)
    with a red stamp slammed across it and a small handwritten note
    paper-clipped beside it.
  - **List** — 3-5 list items, each prefixed by a red dot bullet,
    each with a red underline beneath one keyword.
  - **Number** — one oversized halftone-cutout numeral filling 50% of
    the hero zone, with a red underline beneath and a short ALL-CAPS
    caption.
- FOOTER: ticker row, page counter `NN/NN`.

## CTA slide (slide N)

- TOP: kicker "ACCESS" or "EVIDENCE".
- HEADLINE: ALL-CAPS distressed serif, "COMMENT TO RECEIVE." or
  "WANT THE FILE?" with one word in red.
- SUBTITLE: ALL-CAPS sans, "DM AUTO-DELIVERY ON."
- HERO: one halftone cutout of a folder / dossier / envelope, with
  the trigger word stamped in red across it (functional rubber
  stamp), and a single straight red arrow pointing down to a
  sketched chat-bubble icon containing the trigger word in white
  ALL-CAPS condensed sans.
- FOOTER: ticker row, page counter `NN/NN` (no swipe affordance on
  CTA).
