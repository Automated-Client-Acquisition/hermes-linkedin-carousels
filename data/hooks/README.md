# Hooks

This folder is the carousel skill's **hook library**. Each subfolder is one
named hook archetype — a structural template for the first 1-2 lines of
the LinkedIn post (the part above the "see more" fold).

The hook is the most important text in the post. If lines 1-2 don't stop
the scroll, the rest of the post is dead.

## Picking a hook

`init.py --hook <name>` locks an archetype for the run. The orchestrator
(Claude) reads the archetype's `hook.md` during STEP 2 (script) and
writes the post hook using that template, with the user's actual content
filled in.

If `--hook` is omitted, the orchestrator picks one during the script step
based on the source material and the chosen voice.

## Two tiers

- **Skill defaults** at `.claude/skills/linkedin-carousels/hooks/`
- **Project-local hooks** at `<project>/hooks/` (yours, optional)

Project-local entries shadow defaults on name conflict.

## Adding your own hook

```bash
cp -r .claude/skills/linkedin-carousels/hooks/stop hooks/my-hook
# edit hooks/my-hook/hook.md
echo "- my-hook: Description of my custom hook." >> hooks/_index.md
```

## What every hook.md must contain

In order:

1. 2-3 line description of what this hook does.
2. `## Formula` — structural template with placeholder brackets.
3. `## When to use` — 3-5 bullets.
4. `## Worked examples` — 2-3 short examples (line 1 + line 2 each).
5. `## Common failure modes` — 3-4 ways this hook misfires.
6. `## Pairs well with` — 1-2 sentences naming compatible
   post-patterns and CTAs.

## House rules every hook inherits

- Line 1 must be under 80 characters (ideally under 60).
- Line 1 and line 2 must create tension together.
- Never start with "I'm excited to share..." or "I've been thinking..."
- Never start with a hashtag.
- Never use "Let me explain" or "Here's why" as the second line.
- No fabricated stats, no fabricated client stories. If an example needs
  a number, use a clearly-placeholder format (`[N] replies from [N] sends`).
- No em dashes anywhere.

## Available archetypes

See `_index.md`. The 14 shipped archetypes come from the
linkedin-copywriter playbook (Russell Brunson plus the modern LinkedIn
operator canon). They split roughly into:

- **Command hooks:** stop, never, rip.
- **Claim hooks:** bold-claim, bold-number, specific-number, credibility.
- **Tension hooks:** contrarian-punch, curiosity-gap,
  curiosity-gap-misdirect, pattern-interrupt-question, contrast.
- **Vulnerability hooks:** confession.
- **FOMO hooks:** nobodys-talking.
