# Example: a full run, start to finish

A worked example of the pipeline so you can see what "done" looks like at
each step. This uses the brand `aca` and the topic "On-page AEO".

---

## STEP 0 — init

```bash
python .claude/skills/linkedin-carousels/scripts/init.py \
  --topic "On-page AEO" --brand aca --platform both --slides 10
```

Creates `runs/on-page-aeo-2026-05-14/` with: `source/`, `02_style/`,
`middle-art/`, `slides/`, `export/`, plus `brief.md`, `README.md`, and
`.linkedin-carousels-workspace.json` (every step `pending` except `init`).

If `brands/aca/` didn't exist yet, you'd add `--new-brand` and fill in
`brands/aca/brand.md` from the template before STEP 3.

## STEP 1 — source

Source was a blog post URL. Fetched, stripped, saved to
`source/source.md`. Then:
- `source/insights.md` — 13 specific points pulled from the article.
- `brief.md` — summary + angle ("AEO is on-page work, not a separate
  channel") + which 8 insights become body slides.

Workspace updated: `steps.source = "done"`, `source_type = "url"`,
`insight_count = 13`.

## STEP 2 — script

Voice chosen for this run: **clean**. Wrote `script.md` in the template
format — 10 slides: hook, 8 body slides, payoff+CTA. CTA type `comment`,
trigger word `AEO`. Post copy written above the slides.

Workspace updated: `steps.script = "done"`, `slide_count = 10`,
`comment_trigger_word = "AEO"`.

## STEP 3 — style

Inherited the brand default from `brands/aca/brand.md`: **Clean SaaS**.
Wrote `02_style/style.md` with the locked palette and the style prompt
fragment (real hex codes substituted in).

Workspace updated: `steps.style = "done"`, `style_name = "Clean SaaS"`.

## STEP 4 — art

For each of the 10 slides, built the prompt (slide `Visual note` + locked
style fragment) and ran:

```bash
python .claude/skills/linkedin-carousels/scripts/generate.py \
  --run "runs/on-page-aeo-2026-05-14" --slide 1 \
  --prompt "<visual note + style fragment>"
# ... slides 2-10 ...
```

Each call writes `slides/slide-NN.png` and flips
`images.slide_NN = "done"`. Re-running a slide that already exists prints
`SKIP` — that's the resumability. When slide 10 landed, the script detected
all 10 present and set `steps.art = "done"` automatically.

## STEP 5 — export

```bash
python .claude/skills/linkedin-carousels/scripts/export.py \
  --run "runs/on-page-aeo-2026-05-14"
```

Confirmed all 10 slide images exist, normalized each to 1080×1350, wrote
`export/01.png … export/10.png`, `export/post-copy.txt`,
`export/CHECKLIST.md`, and the `alt-text.md` stub at the run root.

Workspace updated: `steps.export = "done"`, `status = "complete"`.

Final step: filled in `alt-text.md` with one descriptive line per slide.

---

## Resuming

Mid-run, "continue the AEO carousel" → find
`runs/on-page-aeo-2026-05-14/`, read the workspace file, see `art` is
`in_progress` with slides 1–6 done, continue from slide 7. No earlier step
is redone.
