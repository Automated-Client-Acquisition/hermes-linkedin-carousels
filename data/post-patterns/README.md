# Post Patterns

This folder is the carousel skill's **post-body pattern library**. Each
subfolder is one named structural template for the body of the LinkedIn
post (the lines after the hook, before the CTA).

A post pattern is the **shape** of the body. Distinct from:

- The **hook** (first 1-2 lines) — picked from `hooks/`.
- The **voice** (tone) — picked from `voices/`.
- The **CTA** (last 2-3 lines) — picked by the orchestrator during STEP 2.

## Picking a pattern

`init.py --pattern <name>` locks a pattern for the run. Orchestrator reads
the pattern's `pattern.md` when writing the post body in STEP 2.

If `--pattern` is omitted, the orchestrator picks based on the source
material, the chosen hook, and the voice.

## Two tiers

- Skill defaults at `.claude/skills/linkedin-carousels/post-patterns/`
- Project-local at `<project>/post-patterns/`

Project entries shadow defaults on name conflict.

## Adding your own pattern

```bash
cp -r .claude/skills/linkedin-carousels/post-patterns/breakdown post-patterns/my-pattern
# edit
echo "- my-pattern: Description." >> post-patterns/_index.md
```

## What every pattern.md must contain

In order:

1. 2-3 line description.
2. `## When to use` — 3-5 bullets.
3. `## Structure` — concrete shape (setup → arrows → punchline, etc).
4. `## Worked example` — one example post body, 10-20 lines.
5. `## Rules` — 4-6 bullets on requirements.
6. `## What NOT to do` — 3-5 don'ts.
7. `## Pairs well with` — which hooks and CTAs combine well.

## House rules every pattern inherits

- No em dashes anywhere.
- No fabricated stats, no fabricated client stories.
- Generous whitespace; one idea per line; max 2 sentences per paragraph.
- Write for mobile.

## Available patterns

See `_index.md`. Seven shipped patterns derived from the
linkedin-copywriter playbook (Patterns A through G).
