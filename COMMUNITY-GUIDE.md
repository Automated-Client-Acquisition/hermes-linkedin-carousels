# Hermes Cracked: LinkedIn & Instagram Carousels

Turn any blog post, transcript, or topic into a finished, ready-to-post carousel.
AI generates the slides. You get the PDF + PNGs + post copy. Fully automated.

---

## What You Need (3 Things)

| Thing | Cost | Time |
|-------|------|------|
| Hermes Agent (free) | $0 | 5 min |
| OpenAI API key | ~$0.08/slide | 2 min |
| The carousel plugin (provided) | Included | 1 min |

**Total: 10 minutes setup, then $0.80 for a 10-slide carousel.**

---

## Step 1: Install Hermes Agent

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Or with pip:
```bash
pip install hermes-agent
```

Verify:
```bash
hermes --version
```

---

## Step 2: Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy it (starts with `sk-...`)
4. Fund your account with $10 (lasts ~125 slides)

---

## Step 3: Install the Carousel Plugin

We provide the plugin as a folder. Copy it into Hermes:

```bash
# From the zip we gave you:
cp -r linkedin-carousels ~/.hermes/plugins/linkedin-carousels

# Enable it
hermes plugins enable linkedin-carousels

# Verify
hermes plugins list | grep linkedin
```

Install the Python dependencies:
```bash
pip install openai Pillow python-dotenv
```

---

## Step 4: Set Your OpenAI Key

```bash
echo "OPENAI_API_KEY=sk-your-key-here" > ~/.hermes/.env
```

---

## Step 5: Create Your First Carousel

Open Hermes and type:

```
make a carousel about 5 LinkedIn growth hacks that work in 2026
```

The agent will:
1. Ask which style, voice, and layout you want
2. Draft the slide script
3. Ask you to confirm before generating (costs $0.08/slide)
4. Generate all slide images
5. Export to PDF + PNGs + post copy

Your carousel lands in `~/carousels/runs/<topic>-<date>/`.

---

## Advanced: Telegram Bot (Auto-Delivery)

Want carousels delivered straight to Telegram? Set up the bot:

### 1. Create a Telegram bot
- DM @BotFather on Telegram
- Send `/newbot`
- Name it, get the token

### 2. Create a Hermes profile
```bash
hermes profile create carousel-bot
```

### 3. Configure it
```bash
echo "OPENAI_API_KEY=sk-..." >> ~/.hermes/profiles/carousel-bot/.env
echo "TELEGRAM_BOT_TOKEN=123:abc..." >> ~/.hermes/profiles/carousel-bot/.env
echo "DEEPSEEK_API_KEY=sk-..." >> ~/.hermes/profiles/carousel-bot/.env

# Copy the plugin
cp -r ~/.hermes/plugins/linkedin-carousels ~/.hermes/profiles/carousel-bot/plugins/
hermes -p carousel-bot plugins enable linkedin-carousels
```

### 4. Start the bot
```bash
hermes -p carousel-bot gateway run
```

DM your bot on Telegram. Send "make a carousel about AI agents for B2B" and it delivers the PDF.

---

## Costs

| Item | Price |
|------|-------|
| Hermes Agent | Free |
| DeepSeek API (the brain) | ~$0.01/carousel |
| OpenAI gpt-5.5 (image gen) | $0.08/slide |
| **10-slide carousel** | **~$0.81** |

---

## Styles Available

| Style | Vibe |
|-------|------|
| `aca` | Editorial Bone-paper + Ink + Red. Warm, authoritative |
| `hand-drawn-saas` | Whiteboard explainer, marker-style diagrams |
| `noir-collage` | Dark, halftone B&W, investigative energy |
| `bloomberg-feature` | Magazine-feature, cream paper, premium |
| `bold-poster` | Single oversized typographic statement |
| `risograph-zine` | Two-ink spot-print, art-school energy |

---

## Troubleshooting

**"OPENAI_API_KEY not found"**
→ Your key isn't set. Run `echo "OPENAI_API_KEY=sk-..." >> ~/.hermes/.env`

**"Module not found: PIL"**
→ Run `pip install Pillow`

**"Provider deepseek has no API key"**
→ Add `DEEPSEEK_API_KEY` to your `.env` file

**Image looks wrong?**
→ The agent asks before generating slide 1. Approve the prompt before it burns credits.

---

## Files You Get Per Carousel

```
runs/<your-topic>-<date>/
  01.png              ← slide 1, 1080×1350
  02.png              ← slide 2
  ...
  carousel.pdf        ← all slides, for LinkedIn document carousel
  post-copy.txt       ← the caption to paste above the carousel
  CHECKLIST.md        ← pre-post verification
```
