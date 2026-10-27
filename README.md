# Palestine+ — design prototype

English news from Palestine, one line at a time and one layer deeper. Identity and site prototype by TakTek.

- `index.html` — the identity book («One more line»: mark, wordmark, colour, type, layers, motion)
- `home.html` — today's front page; `story/*.html`, desks, explainers, numbers, dates ahead and utility pages

Built HTML is generated. Do not edit it by hand; change the tools and rebuild:

```
python -I tools/fonts.py      # WOFF2 subsets (sources in research/font-src, not committed)
python -I tools/brand.py      # marks and tools/out/marks.json
python -I tools/edition.py    # research/*.json + tools/picks.json -> tools/edition.json, tools/photos.json
python -I tools/photos.py     # Commons photos -> assets/img/photo/*.webp
python -I tools/build.py      # home.html
python -I tools/pages.py      # every other page + assets/data/search.json
python -I tools/book.py       # index.html + identity zip
python -I tools/og.py         # then: node --experimental-websocket tools/shot.mjs http://localhost:8303/tools/out/og.html assets/og.png 1200 630 view
python -I tools/links.py      # internal link check
```

Bump `V` in `tools/shell.py` after any CSS/JS change.

Type: Newsreader (Production Type) and Schibsted Grotesk (Bakken & Bæck), SIL OFL. Photographs: Wikimedia Commons, credited on `credits.html` and in `assets/img/photo/CREDITS.md`.
