# LinkedIn Carousels — Community Guide

Turn any blog post, transcript, or research doc into a finished LinkedIn/Instagram carousel — slide-by-slide script, on-brand AI-generated images, correctly sized exports, and post copy. All through Hermes Agent.

---

## What You Need

| Item | Cost | Setup Time |
|---|---|---|
| Hermes Agent installed | Free | 10 min (if not already) |
| OpenAI API key | ~$0.08 per slide | 2 min |
| GitHub account (member of Automated-Client-Acquisition org) | Free | Already done via Skool |

---

## Step 1: Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. Give it a name like `hermes-carousels`
4. Copy the key (it starts with `sk-proj-` or `sk-`)
5. Save it somewhere safe — you'll need it in Step 2

---

## Step 2: Install the Plugin

If you're already a member of the Automated-Client-Acquisition GitHub org, run this ONE command:

```bash
hermes plugins install Automated-Client-Acquisition/hermes-linkedin-carousels --enable
```

Hermes will prompt you for the OpenAI key. Paste it when asked.

Then install the Python dependencies:

```bash
pip install -r ~/.hermes/plugins/linkedin-carousels/data/requirements.txt
```

Restart Hermes and verify:

```bash
hermes plugins list | grep carousel
```

You should see `linkedin-carousels` listed.

---

## Step 3: Create Your Project Folder

Pick a folder on your machine where your carousel projects will live. This is where brands, styles, and runs are stored. For example:

```bash
mkdir ~/carousels
```

That's it. Pass this path as `project_root` whenever you use the carousel tools.

---

## Step 4: Your First Carousel

Open Hermes and type:

```
Make a LinkedIn carousel from this URL: https://example.com/my-blog-post
```

Hermes will:

1. Ask you which style/voice/hook/layout to use (shows you the available options)
2. Scaffold a run folder under `~/carousels/runs/<topic>-<date>/`
3. Write the script and visual notes
4. Ask you to confirm before generating slide images (each costs ~$0.08)
5. Generate all slides
6. Export final PNGs + PDF + post copy

The final deliverables land at:
```
~/carousels/runs/<topic>-<date>/
  01.png ... 10.png    ← ready to post
  carousel.pdf          ← LinkedIn document carousel
  post-copy.txt         ← caption text
  CHECKLIST.md          ← pre-post checks
```

---

## The Five Tools

These are what Hermes uses under the hood. You can also call them directly:

| Tool | What it does |
|---|---|
| `carousel_list` | Show available styles, voices, hooks, patterns, layouts |
| `carousel_init` | Scaffold a new run folder (STEP 0) |
| `carousel_state` | Check the progress of a run |
| `carousel_generate_slide` | Generate ONE slide image (~$0.08) |
| `carousel_export` | Export final PNGs + PDF + copy (STEP 5) |

---

## Available Styles (built-in)

- **aca** — Automated Client Acquisition brand style (red, dark, editorial)
- **bold-poster** — High-contrast poster aesthetic
- **bloomberg-feature** — Financial/tech editorial, data-heavy
- **hand-drawn-saas** — Sketch-style SaaS illustrations
- **noir-collage** — Dark, textured, collage aesthetic
- **risograph-zine** — Print-zine texture, limited palette

To see them all: `carousel_list({project_root: "~/carousels", kind: "styles"})`

---

## Costs

| Operation | Cost |
|---|---|
| `carousel_list` | Free |
| `carousel_init` | Free |
| `carousel_state` | Free |
| `carousel_generate_slide` | ~$0.08 per slide (OpenAI API) |
| `carousel_export` | Free (local processing) |

A typical 10-slide carousel costs ~$0.80.

---

## Troubleshooting

### "OPENAI_API_KEY not found"
The plugin needs your OpenAI key. Run:
```bash
hermes plugins disable linkedin-carousels
hermes plugins enable linkedin-carousels
```
It will prompt you for the key again. Or add it to `~/.hermes/.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

### "openai package not installed"
Run: `pip install -r ~/.hermes/plugins/linkedin-carousels/data/requirements.txt`

### "Pillow not installed"
Run: `pip install Pillow`

### "script not found: .../generate.py"
The plugin wasn't installed correctly. Re-install:
```bash
hermes plugins remove linkedin-carousels
hermes plugins install Automated-Client-Acquisition/hermes-linkedin-carousels --enable
```

### Generated images look wrong or off-brand
- The `force=true` parameter on `carousel_generate_slide` regenerates a slide
- Try a different style with `carousel_init({..., style: "bold-poster"})`
- The first slide sets the visual anchor — confirm the prompt before generating

### "Workspace not found"
You may be pointing to a wrong `run_path`. Use `carousel_list` to find available runs, or check your project root's `runs/` folder.

---

## Still Stuck?

- Ask in the Skool community
- Message the admin agent (@ACAHermesAdminBot on Telegram)
- Check the full README at: https://github.com/Automated-Client-Acquisition/hermes-linkedin-carousels
