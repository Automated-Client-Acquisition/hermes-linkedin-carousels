# Voices

This folder is the carousel skill's **voice library**. Each subfolder is one
named tone-of-voice module. A carousel run picks a voice at init time
(`init.py --voice <name>`), and every script written for that run inherits
the voice's rules.

## What a voice is, and what it isn't

A voice is the **tone, casing, rhythm, and vocabulary** of the post copy
and any in-image text. It is NOT:

- The visual aesthetic (that's a [style](../styles/README.md)).
- The brand's audience or lead magnet (those live in
  [brands/](../../../brands/)).
- The structural pattern of the post body (that's a
  [post pattern](../post-patterns/README.md)).
- The first-line attention grab (that's a [hook](../hooks/README.md)).

A voice can be inherited by many brands. ACA's senior-operator voice could
be the right fit for any anti-hype B2B consultancy.

## Folder layout

```
voices/
  README.md       # this file
  _index.md       # registry of available voices
  <name>/
    voice.md      # the full spec for one voice
```

## How `init.py` uses this

When the user runs `init.py --voice senior-operator`, init.py validates the
name against `_index.md`, records it in the run's workspace JSON, and the
orchestrator (Claude) reads the voice's `voice.md` when writing
`script.md` during STEP 2.

If `--voice` is omitted at init time, the brand's default voice (from
`brands/<brand>/brand.md` or `brands/<brand>/voice.md`) is used.

## Two tiers of voices

Like every library in this skill, voices are discovered in two locations:

1. **Skill defaults** at `.claude/skills/linkedin-carousels/voices/`
   (this folder). Ships with the skill. Don't edit if you want to track
   upstream updates cleanly.
2. **Project-local voices** at `<project>/voices/`. Your own additions.
   These shadow the skill defaults on name conflict.

`scripts/list.py` shows both. `init.py --voice` accepts entries from
either.

## Adding your own voice

Copy an existing voice folder, rename, edit, register.

```bash
cp -r .claude/skills/linkedin-carousels/voices/clean voices/my-brand-voice
# edit voices/my-brand-voice/voice.md
# add a line to voices/_index.md
echo "- my-brand-voice: Description of my brand voice." >> voices/_index.md
```

Then `init.py --voice my-brand-voice` works.

## What every voice.md must contain

These sections, in this order, so the orchestrator can rely on them:

1. A 2-3 line description of who this voice sounds like.
2. `## When to use` — 3-5 bullet points.
3. `## Words and phrases to USE` — 5-10 specific examples.
4. `## Words and phrases to AVOID` — 5-10 specific examples.
5. `## Sentence rhythm` — 2-3 lines on length and cadence.
6. `## Casing rules` — explicit rules on lowercase vs sentence case vs
   UPPERCASE.
7. `## Punctuation` — rules for em dashes (the project default is "never
   use them"), exclamation marks, periods, and profanity.
8. `## Three example one-liners in this voice` — for the orchestrator to
   sanity-check generated copy against.
9. `## What NOT to do` — 4-6 specific don'ts.

Keep each voice.md tight (40-80 lines). It gets read by the orchestrator
every time a carousel uses this voice; brevity matters.

## House rules every voice inherits

- No em dashes anywhere. Periods or line breaks instead.
- No fabricated stats, no fabricated client stories. If example copy in a
  voice.md needs a number, use a clearly-placeholder format like
  `[your specific result]`.
- No hashtags.
- Emoji discipline depends on the voice — `clean` and `senior-operator`
  use zero, `hype` allows 1-2 per post.
