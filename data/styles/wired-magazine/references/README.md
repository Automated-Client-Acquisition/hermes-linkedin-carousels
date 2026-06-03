# References — wired-magazine

Place reference images here to anchor visual identity during generation.

## Recommended references

Reference images for this style should be clean, high-contrast tech
magazine spreads:

- WIRED feature spreads with bold sans headlines on white
- Fast Company covers with graphic overlays and accent colors
- Tech magazine interior spreads with photo + text layouts

## File naming

Name files descriptively: `wired-cover-ref.jpg`, `fastco-spread-ref.jpg`.

## Usage

```bash
python generate.py --run "runs/<slug>-<date>" --slide 1 \
  --reference "styles/wired-magazine/references/<file>.jpg"
```
