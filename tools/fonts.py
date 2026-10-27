"""Self-hosted WOFF2 subsets of the two brand faces.

python -I tools/fonts.py   (from the project root; sources in research/font-src, gitignored)

Newsreader (Production Type, OFL) is the voice: headlines at its display optical size,
reading text at its text size, the wordmark. Schibsted Grotesk (Bakken & Baeck for
Schibsted, OFL) is the instrument: desk labels, layer names, times, the +n badges and
every figure. Both keep their layout features (tnum, lnum, onum, case, ss01).
"""
import io
import os
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'research', 'font-src')
OUT = os.path.join(ROOT, 'assets', 'fonts')
os.makedirs(OUT, exist_ok=True)

# Basic Latin, Latin-1, Latin Extended-A, the transliteration letters Arabic names use
# (ḥ ṣ ḍ ṭ ẓ ʿ ʾ), typographic punctuation, arrows, the shekel and maths signs.
UNICODES = (
    list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) +
    [0x1E0C, 0x1E0D, 0x1E24, 0x1E25, 0x1E62, 0x1E63, 0x1E6C, 0x1E6D, 0x1E92, 0x1E93, 0x02BE, 0x02BF, 0x02BC,
     0x2009, 0x200A, 0x2010, 0x2011, 0x2012, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026,
     0x2032, 0x2033, 0x2039, 0x203A, 0x2044, 0x20AC, 0x20AA, 0x2116, 0x2190, 0x2191, 0x2192, 0x2193,
     0x2197, 0x2198, 0x2212, 0x2248, 0x2264, 0x2265, 0x00D7, 0x00B0, 0x00B7, 0x00B2, 0x2153, 0x00BD, 0x00BC]
)

JOBS = [
    ('Newsreader[opsz,wght].ttf', 'newsreader.woff2', {'opsz': (6, 72), 'wght': (400, 680)}),
    ('Newsreader-Italic[opsz,wght].ttf', 'newsreader-italic.woff2', {'opsz': (12, 36), 'wght': (400, 500)}),
    ('SchibstedGrotesk[wght].ttf', 'schibsted.woff2', {'wght': (500, 800)}),
]


def options():
    o = subset.Options()
    o.flavor = 'woff2'
    o.layout_features = ['*']
    o.name_IDs = ['*']
    o.name_languages = ['*']
    o.notdef_outline = True
    o.glyph_names = False
    o.hinting = False
    o.desubroutinize = True
    return o


for src, out, limits in JOBS:
    font = instancer.instantiateVariableFont(TTFont(os.path.join(SRC, src)), limits)
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    font = TTFont(buf)
    sub = subset.Subsetter(options())
    sub.populate(unicodes=UNICODES)
    sub.subset(font)
    font.flavor = 'woff2'
    font.save(os.path.join(OUT, out))
    print(out, os.path.getsize(os.path.join(OUT, out)) // 1024, 'KB')
