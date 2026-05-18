# Style Library

Six carousel visual styles, each fully specified. In STEP 3, pick ONE (or
inherit the brand default from `brands/<brand>/brand.md`), then write the run's
`02_style/style.md` using that style's **prompt fragment** as the base —
swapping in the brand's actual hex palette where noted.

The chosen style is **locked across every slide** so the carousel reads as a
set, not a collage. Aspect ratio is always **1080×1350 (4:5)**.

Every prompt fragment ends with the same negative list — keep it.

---

## 1. Clean SaaS

Flat vector illustration, generous whitespace, 2–3 brand colors, crisp
geometric shapes. Feels like a well-funded product's marketing site.

**Best for:** B2B software, technical explainers, data/process content.

**Prompt fragment:**
```
Flat vector illustration, clean and modern SaaS marketing style. Generous
whitespace, off-white background. Limited palette of <PRIMARY hex>, <SECONDARY
hex>, and <ACCENT hex>. Crisp geometric shapes, simple iconography, one clear
focal element per image. Soft, even lighting; no gradients heavier than a
subtle tint; no drop shadows. Confident and uncluttered. Negative: no
stock-photo clichés, no watermarks, no logos, no gibberish text, no busy
backgrounds.
```

## 2. Hand-drawn

Marker and ink sketch look, slightly imperfect linework, friendly and human.
Feels like a smart person explaining at a whiteboard.

**Best for:** founder voice, opinion pieces, "here's how I think about X".

**Prompt fragment:**
```
Hand-drawn marker and ink illustration, sketchbook style. Slightly imperfect,
energetic linework with visible strokes. Mostly monochrome ink on warm paper
white, with <ACCENT hex> used sparingly for emphasis. One clear hand-sketched
concept per image, plenty of breathing room. Friendly, human, a little raw.
Negative: no stock-photo clichés, no watermarks, no logos, no gibberish text,
no over-rendered 3D.
```

## 3. Craft paper

Textured paper background, cut-paper collage shapes, organic and tactile.
Feels handmade and warm.

**Best for:** sustainability, craft, lifestyle, wellness, education.

**Prompt fragment:**
```
Cut-paper collage illustration on a textured craft-paper background. Layered
construction-paper shapes with subtle torn edges and soft paper grain. Warm,
earthy palette built around <PRIMARY hex> and <SECONDARY hex>, with <ACCENT
hex> as a highlight. Soft natural shadows between paper layers. One tactile
focal composition per image. Organic, handmade, warm. Negative: no stock-photo
clichés, no watermarks, no logos, no gibberish text, no glossy digital
gradients.
```

## 4. Noir documentary

High-contrast black-and-white photographic feel, film grain, dramatic light.
Feels serious, cinematic, weighty.

**Best for:** finance, investigations, hard-hitting industry takes, history.

**Prompt fragment:**
```
High-contrast black-and-white documentary photography. Dramatic directional
lighting, deep blacks, bright highlights, visible 35mm film grain. Cinematic,
serious, slightly moody. Strong single subject per frame, shallow depth of
field. No color except true monochrome. Negative: no stock-photo clichés, no
watermarks, no logos, no gibberish text, no HDR over-processing, no cheerful
lighting.
```

## 5. Soft corporate

Muted gradients, rounded shapes, approachable and calm. Feels modern,
trustworthy, unthreatening.

**Best for:** HR, careers, coaching, services, "soft skills" topics.

**Prompt fragment:**
```
Modern soft-corporate illustration. Muted, desaturated gradients moving between
<PRIMARY hex> and <SECONDARY hex>, with <ACCENT hex> for small highlights.
Rounded, friendly shapes; smooth forms; gentle, even lighting. Calm,
approachable, trustworthy. One clear focal concept per image with soft
negative space. Negative: no stock-photo clichés, no watermarks, no logos, no
gibberish text, no harsh contrast, no sharp corners.
```

## 6. Photography

Realistic photographic scenes with consistent lighting and lens character
across all slides. Feels premium and editorial.

**Best for:** product, travel, food, real-world processes, premium brands.

**Prompt fragment:**
```
Realistic editorial photography. Consistent lighting setup across all images:
soft key light, natural fill, gentle falloff. Consistent lens character (~35mm
look, shallow but not extreme depth of field). Cohesive color grade with
<ACCENT hex> recurring as an environmental accent. One clear subject per frame,
clean composition, premium feel. Negative: no stock-photo clichés, no
watermarks, no logos, no gibberish text, no obvious compositing, no surreal
elements.
```

---

## Writing the run's style.md

The run's `02_style/style.md` should contain:
1. **Style name** — one of the six above (or a documented custom).
2. **Locked palette** — the actual hex codes used, pulled from the brand.
3. **Style prompt fragment** — the chosen fragment above with `<PRIMARY hex>`
   etc. replaced by real values. This paragraph is appended verbatim to every
   `generate.py` prompt.
4. **Typography note** — if any text is rendered inside images (keep minimal;
   prefer overlaying headlines at export when the style is clean/vector).
5. **Consistency note** — whether to pass slide 1 as a `--reference` anchor
   for later slides (recommended for Photography and Noir documentary).
