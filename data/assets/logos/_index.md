# Brand logo library

Real brand wordmarks / icons used when a carousel slide mentions a
named product, platform, or company. Passing the actual logo as a
reference image to gpt-image-2-2026-04-21 (via `generate.py --reference`) is
the difference between "the slide says LINKEDIN in monospace" and
"the slide carries the actual LinkedIn-blue wordmark."

## How the orchestrator uses this

When writing a slide's `Visual note` that names a brand, the
orchestrator:

1. Looks up the brand in the **Brand index** below, finding either a
   matching SVG file in this folder or a fallback typographic
   instruction.
2. Passes the matched logo as the reference image to `generate.py`:
   ```bash
   python scripts/generate.py --run <run> --slide N \
     --prompt "..." \
     --reference .claude/skills/linkedin-carousels/assets/logos/<brand>.svg
   ```
3. In the visual note, references the logo by name and intended
   position ("the LINKEDIN wordmark in its official blue, top-right
   corner of the card, ~80px wide"), NOT by re-describing the visual
   style of the brand.

If a brand is in the index but its file is `NOT INCLUDED`, the
orchestrator uses the fallback typographic treatment specified in
the entry, and does NOT pass a reference image.

If a brand is NOT in the index at all, the orchestrator either (a)
falls back to plain typographic rendering OR (b) asks the user to
add the logo to this folder before proceeding.

## Licensing

All SVG files in this folder are sourced from
[SimpleIcons.org](https://simpleicons.org), released under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) (public
domain).

**The icons themselves are CC0. The trademarks they represent are
NOT.** Use the marks only in a descriptive / nominative-fair-use
context — i.e. referring to the actual product or company in good
faith, not implying endorsement or affiliation. For a carousel that
says "we tested GPT, Gemini, Grok, Llama, Claude on real outbound,"
that's fine. For a carousel that says "Claude approves this method"
or "official LinkedIn partner," that's not fine — that's
misrepresentation, and the relevant trademark holders can object
regardless of the logo file's licensing.

The orchestrator MUST check the slide's voice before deciding to
include a logo. If the slide implies any kind of endorsement,
affiliation, or partnership with the brand, switch to typographic
rendering and remove the reference image.

## Brand index

Format: `<lookup-key>` (case-insensitive) → `<file>` (in this folder)
+ `<aliases>` + `<recommended sizing>` + `<voice note>`.

The lookup key is what appears on the carousel slide (or in the
visual note). Aliases let the orchestrator match "Twitter", "X",
"X / Twitter", "twitter.com" all to the same file.

### Platforms

- **LinkedIn** — file: `NOT INCLUDED` (trademark holder removed from
  SimpleIcons CDN). Fallback: render the wordmark typographically as
  "Linked" in deep ink + "in" in white inside a small saturated
  blue (#0A66C2) sharp-corner square. Aliases: `linked-in`,
  `linkedin.com`, `LI`.
- **X / Twitter** — file: `x.svg`. Aliases: `Twitter`, `X.com`,
  `twitter.com`. Use this for both pre-rebrand "Twitter" mentions
  and post-rebrand "X" mentions; the file is the current X mark.
  Recommended size on a slide: 48-72px square.
- **Instagram** — file: `instagram.svg`. Aliases: `IG`, `Insta`,
  `instagram.com`. Recommended size: 48-72px square.
- **Facebook** — file: `facebook.svg`. Aliases: `FB`,
  `facebook.com`, `Meta Facebook`. Recommended size: 48-72px square.
- **TikTok** — file: `tiktok.svg`. Aliases: `tiktok.com`.
  Recommended size: 48-72px square.
- **YouTube** — file: `youtube.svg`. Aliases: `YT`, `youtube.com`.
  Recommended size: 48-72px square.

### Messaging and DM channels

- **Telegram** — file: `telegram.svg`. Aliases: `telegram.org`,
  `TG`. Recommended size: 48-72px square.
- **Discord** — file: `discord.svg`. Aliases: `discord.com`.
  Recommended size: 48-72px square.
- **WhatsApp** — file: `whatsapp.svg`. Aliases: `WA`,
  `whatsapp.com`. Recommended size: 48-72px square.
- **Slack** — file: `NOT INCLUDED` (removed from SimpleIcons at
  Salesforce/Slack request). Fallback: render the wordmark
  typographically as "slack" in a chunky sans with the four-color
  Slack hashtag glyph approximated by four small dots in red /
  yellow / green / blue. Aliases: `slack.com`. If using this on a
  slide where exactness matters, drop the actual Slack logo into
  this folder manually.
- **Gmail** — file: `gmail.svg`. Aliases: `Google Mail`,
  `mail.google.com`. Recommended size: 48-72px square. Note: this
  is the multicolor M-envelope icon, not the Gmail wordmark.

### AI models and labs

- **Anthropic** — file: `anthropic.svg`. Aliases: `Claude`,
  `Anthropic AI`, `anthropic.com`. The current Anthropic mark is
  used for both "Anthropic the company" and "Claude the model" —
  Anthropic does not ship a separate Claude wordmark logo on
  SimpleIcons. Recommended size: 48-64px square.
- **OpenAI / ChatGPT** — file: `NOT INCLUDED` (removed from
  SimpleIcons). Fallback: render the wordmark typographically as
  "OpenAI" in heavy bold sans, deep ink, with the petal-spiral
  glyph approximated by a small abstract circular form to its left.
  For "ChatGPT" specifically, use the same fallback. Aliases:
  `GPT`, `ChatGPT`, `gpt-4`, `gpt-5`, `openai.com`. If exactness
  matters, drop the actual OpenAI logo into this folder.
- **Google Gemini** — file: `googlegemini.svg`. Aliases: `Gemini`,
  `Bard`, `Google AI`, `gemini.google.com`. Recommended size:
  48-64px square.
- **Meta** — file: `meta.svg`. Aliases: `Llama`, `Meta AI`,
  `meta.com`. Meta's mark is used for both "Meta the company" and
  "Llama the model" — Llama doesn't ship a distinct logo.
  Recommended size: 48-72px square.
- **Mistral AI** — file: `mistralai.svg`. Aliases: `Mistral`,
  `mistral.ai`. Recommended size: 48-64px square.
- **xAI / Grok** — file: `x.svg`. Aliases: `Grok`, `xAI`, `x.ai`.
  The X mark is used because xAI / Grok ride on the X parent brand.
  Recommended size: 48-64px square.
- **Nous Research** — file: `NOT INCLUDED` (not on SimpleIcons).
  Fallback: render typographically as "Nous Research" in italic
  display serif, deep ink. For "Hermes" (the agent from Nous
  Research), use the same fallback. If exactness matters, drop a
  Nous logo into this folder manually.

### Productivity and SaaS

- **Stripe** — file: `stripe.svg`. Aliases: `stripe.com`.
  Recommended size: 48-80px wide.
- **Notion** — file: `notion.svg`. Aliases: `notion.so`,
  `Notion AI`. Recommended size: 48-72px square.
- **Linear** — file: `linear.svg`. Aliases: `linear.app`.
  Recommended size: 48-72px square.
- **HubSpot** — file: `hubspot.svg`. Aliases: `hubspot.com`.
  Recommended size: 48-80px wide.
- **Salesforce** — file: `NOT INCLUDED` (removed from SimpleIcons
  at Salesforce request). Fallback: render typographically as
  "salesforce" in lowercase chunky sans with a small cloud-shape
  glyph approximated to its left. Aliases: `SFDC`,
  `salesforce.com`. If exactness matters, drop the actual logo into
  this folder.

## Adding a new logo

1. Drop the SVG (or PNG, but SVG is preferred) into this folder.
   Filename should be kebab-case, lowercase, no spaces.
2. Add an entry to the relevant section above with:
   - The lookup key (the brand name as it appears on slides).
   - The file name.
   - All known aliases the orchestrator might encounter on a script.
   - Recommended sizing on a slide.
   - Any voice / endorsement note (when to use vs not use).
3. Confirm licensing — if not from SimpleIcons CC0, document the
   source and any usage restrictions in the entry.

## When NOT to use a logo

- The slide implies endorsement / partnership with the brand → use
  typographic fallback or omit the brand mention entirely.
- The slide is satire or critique that the brand owner could object
  to → use typographic fallback.
- The brand is mentioned as a competitor being outperformed → use
  typographic fallback to avoid trademark-disparagement risk.
- The brand owner has publicly requested no third-party use → use
  typographic fallback or remove the mention.

The default is: real logo IF the slide is neutral, descriptive, or
positive about the brand AND the file is in this folder. Otherwise,
typographic fallback.
