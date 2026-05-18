# assets/

Static assets the skill itself uses — NOT per-run output.

Put here things that are reused across every run, e.g.:
- a logo PNG to optionally composite onto the final slide
- a font file, if you overlay headline text at export time
- a watermark or brand frame

Per-run images live in each run folder (`runs/<slug>-<date>/slides/`,
`/middle-art/`, `/export/`), never here.

This folder is intentionally kept in version control even when empty.
