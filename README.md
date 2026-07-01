# Content Creator Assets Dataset

A structured dataset of **50 content-creator broadcast graphics** — overlays, scene transitions, lower-thirds, alerts, panels, intro/outro stings, and font kits. Each entry includes style tags, target platforms, a color palette, animation type, recommended use case, and an illustrative "retention tier" annotation for exploring how visual/motion choices might relate to viewer attention on gaming channels.

Every preview thumbnail in this repo is an **original, procedurally-generated SVG** — no third-party overlay packs, fonts, or artwork are scraped, redistributed, or reproduced. See [Originality & License](#originality--license) below.

**[→ Browse the dataset](index.html)** &nbsp;·&nbsp; **[→ Database / API setup guide](setup.html)**

---

## What's inside

```
content-creator-assets-dataset/
├── index.html              # Browsable dataset UI (search, filters, category stats)
├── setup.html               # DB schema + API client snippets for 4 databases, 4 languages
├── data/
│   └── assets.json          # The 50-entry dataset
├── assets/
│   └── previews/*.svg       # 50 original generated preview thumbnails (1 per entry)
├── generate_data.py          # Regenerates data/assets.json
├── generate_previews.py      # Regenerates assets/previews/*.svg from the dataset
└── README.md
```

## Schema

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique record id (1–50) |
| `name` | string | Asset name |
| `category` | enum | `overlay`, `transition`, `lower-third`, `alert`, `panel`, `intro-outro`, `font` |
| `style_tags` | string[] | Aesthetic tags (e.g. `cyberpunk`, `retro-vhs`, `pastel-kawaii`) |
| `platforms` | string[] | Target platforms (`Twitch`, `YouTube`, `TikTok`, `Kick`) |
| `color_palette` | string[] | 4 hex codes: background → accent colors |
| `font_family` | string \| null | Typeface preset name, set for font/lower-third/alert entries |
| `effect_notes` | string | Shadow, glow, stroke, or animation treatment |
| `animation_type` | enum | `fade`, `slide`, `glitch`, `particle-burst`, `wipe`, `zoom-punch`, `static` |
| `use_case` | string | Recommended streaming context |
| `description` | string | Free-text description of the asset |
| `retention_tier` | enum | `High` / `Medium` / `Low` — **illustrative annotation only**, see below |
| `retention_rationale` | string | Reasoning behind the tier annotation |
| `preview_image` | string | Relative path to the generated SVG preview |

## About the "retention tier" field

This field is an **illustrative, author-annotated estimate** — not measured audience analytics. It's included to demonstrate how a dataset like this could support an insights/analytics layer (e.g. "do fast, high-contrast overlays correlate with lower drop-off during scene transitions?"), and each rationale explains the reasoning behind the tier. If you plug in real watch-time data from your own channel, this field is the natural place to replace estimates with measured values.

## Running locally

Because `index.html` fetches `data/assets.json` via `fetch()`, opening the file directly (`file://`) will be blocked by the browser's CORS policy. Serve the folder instead:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Or just push to GitHub and enable **GitHub Pages** on the repo — the site works as-is with zero build step.

## Regenerating the dataset

```bash
python3 generate_data.py       # rebuilds data/assets.json from ASSET_SEEDS
python3 generate_previews.py   # rebuilds assets/previews/*.svg from the current dataset
```

Add new entries by extending `ASSET_SEEDS` in `generate_data.py` (name, category, description, use case), then re-run both scripts.

## Originality & License

- **Dataset content** (names, descriptions, tags, palettes, use cases) is originally authored for this repo.
- **Preview thumbnails** are procedurally generated SVG graphics composed from each entry's own metadata — abstract shapes and category glyphs, not reproductions of any real overlay pack, font, or branded asset.
- **Fonts referenced by name** (e.g. "Bold Condensed Sans", "Purple Shadow Impact") describe *styles*, not licensed typefaces — no font files are bundled.
- This repo is released for educational/portfolio use. If you fork it to build a real product on top of real commercial assets, make sure you have the appropriate licenses for those assets — this dataset only models the *metadata layer*, deliberately, to avoid redistributing anyone else's IP.

## Credits

Built by [Jeeventhiran](https://github.com/Jvn1604) as a dataset + browsable UI project, structurally inspired by [hasaneyldrm/exercises-dataset](https://github.com/hasaneyldrm/exercises-dataset).
