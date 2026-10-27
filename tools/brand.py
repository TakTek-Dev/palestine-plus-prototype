"""The Palestine+ marks, drawn from the type and a plus built to the type's own stem.

python -I tools/brand.py  ->  assets/brand/*.svg, favicon.svg, tools/out/marks.json

The idea, «One more line»: a news line is a horizontal stroke; the plus is that line with a
second one standing across it, waiting to be laid down. Open a layer and the standing bar
falls flat beneath the first: one line deeper. So the plus is drawn, not typed, and it is
two-coloured: the lying bar is ink, the same stuff as the line you are reading; the standing
bar is green, the one more line still to come. Two colours also keep it from ever reading as
a pharmacy cross or a first-aid sign, which a solid green plus on a tile would.
Bars are equal, round-ended, as thick as the hairline-to-stem midpoint of Newsreader's l
(0.62 of the stem), and cross at the middle of the lowercase so the plus reads with the
letters, not above them like a footnote.
"""
import json
import os
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'research', 'font-src', 'Newsreader[opsz,wght].ttf')
BR = os.path.join(ROOT, 'assets', 'brand')
os.makedirs(BR, exist_ok=True)
os.makedirs(os.path.join(ROOT, 'tools', 'out'), exist_ok=True)

INK, PAPER, PLUS, PLUS_ON = '#0B1420', '#FFFFFF', '#0F9D58', '#35D48A'
WGHT = 600

font = instancer.instantiateVariableFont(TTFont(SRC), {'opsz': 72, 'wght': WGHT})
gs, cmap = font.getGlyphSet(), font.getBestCmap()
hmtx, kern = font['hmtx'], None


def bounds(ch):
    bp = BoundsPen(gs)
    gs[cmap[ord(ch)]].draw(bp)
    return bp.bounds


def stem():
    """Width of the l's stem, sampled at half the x-height by scanning its outline."""
    rec = DecomposingRecordingPen(gs)
    gs[cmap[ord('l')]].draw(rec)
    xh = bounds('x')[3]
    y = xh * .5
    xs = []
    pts = []
    for op, args in rec.value:
        if op == 'moveTo':
            pts = [args[0]]
        elif op in ('lineTo', 'qCurveTo', 'curveTo'):
            for p in args:
                if p is not None:
                    pts.append(p)
        elif op == 'closePath':
            for a, b in zip(pts, pts[1:] + pts[:1]):
                if (a[1] - y) * (b[1] - y) < 0:
                    xs.append(a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1]))
    xs.sort()
    return xs[-1] - xs[0], xh


STEM, XH = stem()


def text_path(s, x0=0.0):
    """Outline of s as one SVG path (y up in font units -> y down here, baseline at 0)."""
    pen = SVGPathPen(gs)
    x = x0
    for ch in s:
        g = cmap[ord(ch)]
        tp = TransformPen(pen, (1, 0, 0, -1, x, 0))
        gs[g].draw(tp)
        x += hmtx[g][0]
    return pen.getCommands(), x


def plus_bars(cx, cy, arm, w):
    """The two bars as round-ended rects: (x, y, width, height, r)."""
    h = (cx - arm / 2, cy - w / 2, arm, w, w / 2)
    v = (cx - w / 2, cy - arm / 2, w, arm, w / 2)
    return h, v


def rect(r, fill, extra=''):
    x, y, w, h, rr = r
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rr:.1f}" fill="{fill}"{extra}/>'


# ---- wordmark ---------------------------------------------------------------
word, adv = text_path('Palestine')
e_right = adv - hmtx[cmap[ord('e')]][0] + bounds('e')[2]
BAR = STEM * .62
ARM = XH * .98                       # a touch over the x-height so it holds its own beside the e
GAP = STEM * .62                      # one bar's width of air after the e
cx = e_right + GAP + ARM / 2
cy = -XH / 2                          # crosses at the middle of the lowercase
top = -bounds('l')[3] - 40
bottom = 60
right = cx + ARM / 2 + 30
VB = f'-10 {top:.0f} {right + 10:.0f} {bottom - top:.0f}'
H, Vb = plus_bars(cx, cy, ARM, BAR)


def wordmark_svg(ink, plus, label='Palestine+'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" role="img" aria-label="{label}">'
            f'<path d="{word}" fill="{ink}"/>{rect(Vb, plus)}{rect(H, ink)}</svg>')


# ---- the mark on its own: square tile ------------------------------------------------
def tile_svg(bg, line, plus, size=512, radius=.23, scale=.5):
    arm = size * scale
    w = arm * BAR / ARM
    h, v = plus_bars(size / 2, size / 2, arm, w)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
            f'<rect width="{size}" height="{size}" rx="{size * radius:.0f}" fill="{bg}"/>{rect(v, plus)}{rect(h, line)}</svg>')


def plus_svg(line, plus, size=100):
    w = size * BAR / ARM
    h, v = plus_bars(size / 2, size / 2, size, w)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{rect(v, plus)}{rect(h, line)}</svg>'


files = {
    'wordmark-ink.svg': wordmark_svg(INK, PLUS),
    'wordmark-white.svg': wordmark_svg(PAPER, PLUS_ON),
    'wordmark-mono.svg': wordmark_svg(INK, INK),
    'mark-ink.svg': tile_svg(INK, PAPER, PLUS_ON),
    'mark-white.svg': tile_svg(PAPER, INK, PLUS),
    'plus.svg': plus_svg(INK, PLUS),
    'plus-white.svg': plus_svg(PAPER, PLUS_ON),
}
for n, s in files.items():
    open(os.path.join(BR, n), 'w', encoding='utf-8').write(s)
open(os.path.join(ROOT, 'favicon.svg'), 'w', encoding='utf-8').write(tile_svg(INK, PAPER, PLUS_ON, 64, .25, .62))

ratio = BAR / ARM
json.dump({
    'word': word, 'viewBox': VB, 'H': H, 'V': Vb, 'stem': STEM, 'bar': BAR, 'xh': XH, 'arm': ARM, 'ratio': ratio,
    'colors': {'ink': INK, 'paper': PAPER, 'plus': PLUS, 'plus_on': PLUS_ON},
}, open(os.path.join(ROOT, 'tools', 'out', 'marks.json'), 'w'), indent=1)
print(f'stem {STEM:.1f}u  x-height {XH:.0f}u  arm {ARM:.0f}u  bar ratio {ratio:.3f}  viewBox {VB}')
