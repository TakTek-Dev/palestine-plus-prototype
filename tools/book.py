"""Build index.html, the Palestine+ identity book, and assets/palestine-plus-identity.zip.

python -I tools/book.py
"""
import os
import sys
import zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import C, E, S, BY, MARKS, ROOT, TODAY, esc, pl, badge, wordmark, head, foot, icon, long_day, write, V, depth
from parts import stack

C.R = ''
m = MARKS
INK, PLUS, PLUS_ON = m['colors']['ink'], m['colors']['plus'], m['colors']['plus_on']

# construction drawing: the wordmark at a known scale with its measures
x, y, w, h, r = m['V']
hx, hy, hw, hh, _ = m['H']
vb = [float(v) for v in m['viewBox'].split()]
xh = m['xh']
build = f'''<svg viewBox="{vb[0] - 200} {vb[1] - 260} {vb[2] + 600} {vb[3] + 620}" role="img" aria-label="Construction of the wordmark: the plus crosses at the middle of the x-height; its bars are 0.62 of the l's stem; its arms are 0.98 of the x-height.">
<g stroke="#9AA8B8" stroke-width="5" stroke-dasharray="22 16">
<path d="M{vb[0] - 160} 0H{vb[0] + vb[2] + 260}"/><path d="M{vb[0] - 160} {-xh}H{vb[0] + vb[2] + 260}"/><path d="M{vb[0] - 160} {-xh / 2}H{vb[0] + vb[2] + 260}"/>
</g>
<path d="{m['word']}" fill="{INK}" opacity=".16"/>
<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" fill="{PLUS}"/>
<rect x="{hx:.1f}" y="{hy:.1f}" width="{hw:.1f}" height="{hh:.1f}" rx="{r:.1f}" fill="{INK}"/>
<g font-family="Schibsted, sans-serif" font-size="120" font-weight="700" fill="#4F5D6E">
<text x="{vb[0] - 150}" y="-24">baseline</text><text x="{vb[0] - 150}" y="{-xh - 24}">x-height</text><text x="{vb[0] - 150}" y="{-xh / 2 - 24}">middle of the lowercase: the plus crosses here</text>
<text x="{hx}" y="{vb[1] + vb[3] + 150}">bar = 0.62 × stem of l · arm = 0.98 × x-height · round ends</text>
</g>
<path d="M{hx} {vb[1] + vb[3] + 50}H{hx + hw}" stroke="{INK}" stroke-width="6"/><path d="M{hx} {vb[1] + vb[3] + 30}v40M{hx + hw} {vb[1] + vb[3] + 30}v40" stroke="{INK}" stroke-width="6"/>
</svg>'''

lead = BY[E['lead']]
ramp = [('paper', '#FFFFFF', 'The fact. Line one sits on white.', 0), ('l1', '#F2F5F8', 'Context: one layer down.', 1),
        ('l2', '#E5EBF1', 'Numbers: two down.', 2), ('l3', '#D2DBE4', 'Voices: three down.', 3),
        ('ink', '#0B1420', 'What next, and the type itself.', 4)]
sw = ''.join(f'<li data-d="{d}" style="background:{hx_}"><b>{n}</b><code>{hx_}</code><span>{esc(t)}</span></li>' for n, hx_, t, d in ramp)
greens = [('plus', PLUS, 'The standing bar in marks and icons on light. Never text.'), ('plus-t', '#087A43', 'Green as text and badges on white: 5.4:1.'),
          ('plus-on', PLUS_ON, 'The standing bar and badges on ink: 9.6:1.'), ('mute', '#4F5D6E', 'Meta, sources and labels: 6.2:1 on white.')]
gr = ''.join(f'<li><i style="background:{c}"></i><b>{n}</b><code>{c}</code><span>{esc(t)}</span></li>' for n, c, t in greens)

dont = [
    ('A solid green plus on a tile', 'Reads as a pharmacy or first-aid sign. The plus is always two colours.',
     f'<svg viewBox="0 0 100 100"><rect width="100" height="100" rx="23" fill="{PLUS}"/><rect x="25" y="45" width="50" height="10" rx="5" fill="#fff"/><rect x="45" y="25" width="10" height="50" rx="5" fill="#fff"/></svg>'),
    ('A longer lower arm', 'Turns the plus into a Latin cross. The four arms are always equal.',
     f'<svg viewBox="0 0 100 100"><rect x="22" y="32" width="56" height="10" rx="5" fill="{INK}"/><rect x="45" y="14" width="10" height="76" rx="5" fill="{PLUS}"/></svg>'),
    ('Turned 45°', 'An × means close, delete, wrong. The plus never turns except to lie down.',
     f'<svg viewBox="0 0 100 100"><g transform="rotate(45 50 50)"><rect x="22" y="45" width="56" height="10" rx="5" fill="{INK}"/><rect x="45" y="22" width="10" height="56" rx="5" fill="{PLUS}"/></g></svg>'),
    ('Typed from a font', 'A typed + sits on the maths axis with square ends. The drawn plus crosses at the lowercase middle.',
     f'<svg viewBox="0 0 100 100"><text x="50" y="74" text-anchor="middle" font-family="Georgia" font-size="80" fill="{PLUS}">+</text></svg>'),
]
dn = ''.join(f'<li><div class="dn">{s_}</div><b>{esc(t)}</b><p>{esc(d)}</p></li>' for t, d, s_ in dont)

css = '''<style>
.bk-cover{min-height:min(88vh,860px);display:grid;align-content:center;gap:28px;padding-block:60px;position:relative}
.bk-cover .wm svg{width:min(100%,980px);height:auto}
.bk-cover .wm .wm-v rect{transform-box:fill-box;transform-origin:50% 100%;animation:bk-stand 1s .3s var(--ease) both}
@keyframes bk-stand{from{transform:scaleY(0)}}
.bk-cover .sub-t{display:flex;flex-wrap:wrap;gap:10px 28px;font:600 .9rem var(--sans);color:var(--mute)}
.bk-cover .sub-t b{color:var(--ink)}
.bk-nav{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.94);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-block:1px solid var(--rule)}
.bk-nav ol{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;padding-block:4px}
.bk-nav a{display:block;padding:10px 12px;font:600 .84rem var(--sans);white-space:nowrap;color:var(--mute);border-radius:var(--r1)}
.bk-nav a:hover{color:var(--ink);background:var(--l1)}
.ch{padding-block:clamp(56px,8vw,112px);border-bottom:1px solid var(--rule);scroll-margin-top:50px}
.ch-h{display:grid;grid-template-columns:90px minmax(0,1fr);gap:20px;margin-bottom:clamp(26px,4vw,48px)}
.ch-h .no{font:800 1rem var(--sans);color:var(--plus-t);font-variant-numeric:tabular-nums;padding-top:10px}
.ch-h p.dek{margin-top:14px;max-width:62ch}
@media (max-width:640px){.ch-h{grid-template-columns:1fr;gap:4px}}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(20px,4vw,56px);align-items:center}
@media (max-width:860px){.two{grid-template-columns:1fr}}
.pane{border-radius:var(--r3);background:var(--l1);padding:clamp(20px,4vw,48px);display:grid;place-items:center;min-height:280px;position:relative}
.pane.ink{background:var(--ink)}
.pane .cap{position:absolute;left:16px;bottom:12px;font:600 .74rem var(--sans);color:var(--mute)}
.pane.ink .cap{color:var(--mute-on)}
.demo{all:unset;cursor:pointer;display:grid;place-items:center;gap:18px;padding:20px;border-radius:var(--r2)}
.demo .pl{--s:120px}
.demo span.t{font:600 .9rem var(--sans);color:var(--mute)}
.demo:focus-visible{outline:2px solid var(--plus-t)}
.marks{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
@media (max-width:860px){.marks{grid-template-columns:1fr}}
.marks .pane{min-height:220px}
.marks .pane svg{width:min(80%,340px);height:auto}
.marks .pane img{width:120px;height:120px}
.sizes{display:flex;flex-wrap:wrap;gap:28px;align-items:flex-end;margin-top:22px}
.sizes div{display:grid;gap:8px;font:600 .74rem var(--sans);color:var(--mute)}
.gram{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
@media (max-width:900px){.gram{grid-template-columns:repeat(2,minmax(0,1fr))}}
.gram li{border-radius:var(--r2);border:1px solid var(--rule);padding:20px;display:grid;gap:10px;align-content:start}
.gram .ico{height:72px;display:flex;align-items:center}
.gram .ico .pl{--s:44px}
.gram b{font:700 1rem var(--sans)}
.gram .badge{font-size:2.4rem}.gram .badge .pl{--s:.62em}
.pl.leant .pl-v{transform:rotate(-9deg)}
.gram p{font:400 .98rem/1.45 var(--serif);color:var(--ink2)}
.ramp{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border-radius:var(--r3);overflow:hidden;border:1px solid var(--rule)}
@media (max-width:860px){.ramp{grid-template-columns:1fr}}
.ramp li{min-height:200px;padding:18px;display:grid;align-content:end;gap:4px}
.ramp li[data-d="4"]{color:#fff}
.ramp b{font:700 1.05rem var(--sans)}
.ramp code,.greens code{font:500 .8rem ui-monospace,Consolas,monospace;opacity:.8}
.ramp span{font:400 .95rem/1.35 var(--serif)}
.greens{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:14px}
@media (max-width:860px){.greens{grid-template-columns:1fr 1fr}}
.greens li{display:grid;gap:6px;align-content:start}
.greens i{height:70px;border-radius:var(--r2);display:block}
.greens span{font:400 .92rem/1.35 var(--serif);color:var(--ink2)}
.spec{display:grid;gap:22px}
.spec li{display:grid;grid-template-columns:200px minmax(0,1fr);gap:20px;align-items:baseline;border-top:1px solid var(--rule);padding-top:16px}
@media (max-width:700px){.spec li{grid-template-columns:1fr;gap:6px}}
.spec .k{font:600 .82rem/1.4 var(--sans);color:var(--mute)}
.motion{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
@media (max-width:900px){.motion{grid-template-columns:1fr}}
.motion li{border-radius:var(--r2);background:var(--l1);padding:20px;display:grid;gap:8px;align-content:start}
.motion b{font:700 1rem var(--sans)}
.motion code{font:500 .8rem ui-monospace,Consolas,monospace;color:var(--mute)}
.motion p{font:400 .98rem/1.45 var(--serif)}
.dont{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
@media (max-width:900px){.dont{grid-template-columns:repeat(2,minmax(0,1fr))}}
.dont li{display:grid;gap:8px;align-content:start}
.dont .dn{border-radius:var(--r2);background:var(--l1);aspect-ratio:1;display:grid;place-items:center;position:relative}
.dont .dn svg{width:46%}
.dont .dn::after{content:"";position:absolute;inset:14px;border-radius:8px;background:linear-gradient(to top right,transparent calc(50% - 1.5px),#B42318 calc(50% - 1.5px),#B42318 calc(50% + 1.5px),transparent calc(50% + 1.5px));opacity:.85}
.dont b{font:700 .95rem var(--sans)}
.dont p{font:400 .94rem/1.4 var(--serif);color:var(--ink2)}
.voice{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px}
@media (max-width:860px){.voice{grid-template-columns:1fr}}
.voice li{border-radius:var(--r2);padding:18px;display:grid;gap:8px}
.voice li.y{background:var(--plus-wash)}.voice li.n{background:var(--l1)}
.voice b{font:700 .8rem var(--sans);text-transform:uppercase;letter-spacing:.06em}
.voice p{font:500 1.08rem/1.4 var(--serif)}
.pages{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.pages a{border:1px solid var(--rule);border-radius:var(--r2);padding:14px 16px;display:flex;justify-content:space-between;align-items:center;font:600 .92rem var(--sans)}
.pages a:hover{border-color:var(--ink)}
</style>'''

chapters = [('idea', 'The idea'), ('mark', 'The mark'), ('wordmark', 'Wordmark'), ('grammar', 'The plus as grammar'),
            ('colour', 'Colour is depth'), ('type', 'Type'), ('layers', 'Layers'), ('motion', 'Motion'),
            ('photo', 'Photographs'), ('voice', 'Voice'), ('misuse', 'Misuse'), ('files', 'Pages and files')]
nav = ''.join(f'<li><a href="#{k}">{i:02d} {esc(t)}</a></li>' for i, (k, t) in enumerate(chapters, 1))


def ch(i, k, title, dek, body):
    return (f'<section class="ch" id="{k}" aria-labelledby="{k}-h"><div class="wrap"><div class="ch-h"><p class="no">{i:02d}</p>'
            f'<div><h2 class="h-l" id="{k}-h">{title}</h2><p class="dek">{dek}</p></div></div>{body}</div></section>')


body = f'''{css}
<header class="wrap bk-cover">
<p class="lbl">Identity · {esc(long_day(TODAY))}</p>
<div class="wm">{wordmark()}</div>
<p class="dek" style="max-width:52ch;font-size:clamp(1.15rem,1.8vw,1.45rem)">News from Palestine, one line at a time. The plus is one more line: standing across the one you read, waiting to be laid down beneath it.</p>
<p class="sub-t"><span><b>Concept</b> One more line</span><span><b>Type</b> Newsreader · Schibsted Grotesk</span><span><b>Colour</b> Ink, five depths, one green</span><a href="home.html" class="btn solid">See the site {icon("i-right")}</a></p>
</header>
<nav class="bk-nav" aria-label="Chapters"><div class="wrap"><ol>{nav}</ol></div></nav>
{ch(1, 'idea', 'One more line', 'The client’s name already holds the brief. “Palestine” is the news; “+” is what a reader gets for one more second of attention. The identity draws that literally.', f"""
<div class="two"><div class="prose" style="padding:0">
<p>A news line is a horizontal stroke: you read along it. The plus is that line with a second one standing across it. The standing line is not read yet; it is waiting.</p>
<p>Press it and it falls. It lies down beneath the first line, and you are one layer deeper: the context under the fact, the numbers under the context, the voices, then what happens next.</p>
<p>So the mark is not a decoration on the name. It is the button the whole site is built from. Every story is a line with standing lines across it, and the reader decides how many to lay down.</p>
</div>
<div class="pane"><button class="demo" type="button" data-lay aria-expanded="false" aria-controls="demo-p">{pl()}<span class="t">Press the plus</span></button><p class="cap" id="demo-p">Closed: there is more. Open: one line deeper.</p></div></div>""")}
{ch(2, 'mark', 'The mark is drawn from the type', 'The plus is not typed. A font’s + sits on the maths axis with square ends; ours is measured off Newsreader itself so it belongs to the letters beside it.', f"""
<div class="pane" style="background:#fff;border:1px solid var(--rule);padding:clamp(14px,3vw,40px)">{build}</div>
<ul class="spec" style="margin-top:28px">
<li><span class="k">Bars</span><p>Two equal bars with round ends, each 0.62 of the stem of Newsreader’s l at the wordmark’s weight (600, display size). Thin enough to read as a line, not a sign.</p></li>
<li><span class="k">Arms</span><p>0.98 of the x-height, so the plus stands exactly as tall as the lowercase it follows.</p></li>
<li><span class="k">Crossing</span><p>At the middle of the x-height: the lying bar continues the reading line of “Palestine”.</p></li>
<li><span class="k">Two colours</span><p>The lying bar is ink, the same matter as the line you are reading. The standing bar is green: the one more line. Drawn standing bar first, lying bar over it.</p></li>
</ul>""")}
{ch(3, 'wordmark', 'Wordmark and tile', 'Three versions of the wordmark and one tile for small spaces. The plus keeps its two colours in every one except the single-colour print version.', f"""
<div class="marks">
<div class="pane" style="background:#fff;border:1px solid var(--rule)">{wordmark()}<p class="cap">Ink on white · primary</p></div>
<div class="pane ink">{wordmark(ink='#fff', plus='var(--plus-on)')}<p class="cap">White on ink</p></div>
<div class="pane">{wordmark(ink=INK, plus=INK)}<p class="cap">One colour · print and stamps only</p></div>
</div>
<div class="marks" style="margin-top:14px">
<div class="pane"><img src="assets/brand/mark-ink.svg?v={V}" alt="The tile: a white lying bar and a green standing bar on ink." width="120" height="120"><p class="cap">Tile · app, avatar, favicon</p></div>
<div class="pane"><img src="assets/brand/mark-white.svg?v={V}" alt="The tile on white: an ink lying bar and a green standing bar." width="120" height="120" style="border-radius:28px;box-shadow:0 0 0 1px var(--rule)"><p class="cap">Tile on white</p></div>
<div class="pane"><div class="sizes"><div><img src="favicon.svg?v={V}" width="32" height="32" alt="">32 px</div><div><img src="favicon.svg?v={V}" width="16" height="16" alt="">16 px</div><div style="width:120px">{wordmark()}120 px</div></div><p class="cap">Smallest sizes</p></div>
</div>
<p class="dek" style="margin-top:22px;font-size:1rem">Clear space: one arm of the plus on every side. Minimum width of the wordmark: 96 px on screen, 22 mm in print.</p>""")}
{ch(4, 'grammar', 'The plus as grammar', 'The mark runs the interface. Every state of a story is a state of the plus.', f"""
<ul class="gram">
<li><div class="ico">{pl()}</div><b>Standing</b><p>There is more under this line. It is always a button, never decoration.</p></li>
<li><div class="ico">{pl('leant')}</div><b>Leaning</b><p>On hover the standing bar tips 9° towards the line, as if about to fall.</p></li>
<li><div class="ico">{pl('open')}</div><b>Laid down</b><p>The bar has fallen under the first line: this layer is open. Two lines, one under the other.</p></li>
<li><div class="ico">{badge(3)}</div><b>The count</b><p>Beside a headline, the number of layers under it. A reader sees the depth before going in.</p></li>
</ul>""")}
{ch(5, 'colour', 'Colour is depth', 'Every layer is one tint deeper than the one above it, cool greys tinted towards the ink, until the last layer is the ink itself. Nothing is beige; nothing is warm paper.', f"""
<ul class="ramp">{sw}</ul>
<ul class="greens">{gr}</ul>
<p class="dek" style="margin-top:22px;font-size:1rem">Green is the only colour, and it means one thing: one more line. The flag’s green, kept for the plus, the +n count and the ways in. No red, no alarm colour: the facts carry their own weight.</p>""")}
{ch(6, 'type', 'Type: a voice and an instrument', 'Newsreader writes; Schibsted Grotesk measures.', f"""
<ul class="spec">
<li><span class="k">Newsreader · display<br>opsz 72 · 640</span><p class="h-xl" style="font-size:clamp(2rem,4vw,3.4rem)">A year into the ceasefire, its first phase is still unfinished</p></li>
<li><span class="k">Newsreader · text<br>opsz 14–20 · 400</span><p class="dek" style="max-width:60ch">Production Type drew Newsreader for reading news on screens. Its optical sizes let one family carry a 64-pixel headline and a long story without a second serif.</p></li>
<li><span class="k">Newsreader · voices<br>italic 440</span><p style="font:italic 440 1.4rem/1.4 var(--serif)">“People quoted in their own words, short and exact.”</p></li>
<li><span class="k">Schibsted Grotesk<br>labels · 600–700</span><p style="font:700 1rem var(--sans)">GAZA · WEST BANK · JERUSALEM · DIASPORA &amp; WORLD — Updated {esc(E['updated'])} GMT · 4 layers</p></li>
<li><span class="k">Schibsted Grotesk<br>figures · 800, tabular</span><p class="num" style="font-size:clamp(2.6rem,6vw,4.6rem);line-height:1">1,431 · 27,830 · 0123456789</p></li>
</ul>
<p class="dek" style="margin-top:22px;font-size:1rem">Schibsted Grotesk was made by Bakken &amp; Bæck for the Schibsted newspapers: a working face for news, compact, with figures that line up in columns. Both faces are open source and self-hosted as subsets.</p>""")}
{ch(7, 'layers', 'Layers: the story, opened', 'The core component, live. This is today’s lead with its layers.', f"""
<div class="two" style="align-items:start"><div>{stack(lead, 'bk')}</div>
<ol class="howto" style="margin:0">
<li data-d="0"><b>The fact</b><p>One sentence, always visible, with its source.</p></li>
<li data-d="1"><b>{pl()}Context</b><p>Why now.</p></li><li data-d="2"><b>{pl()}Numbers</b><p>The measure, dated.</p></li>
<li data-d="3"><b>{pl()}Voices</b><p>In their own words.</p></li><li data-d="4"><b>{pl()}What next</b><p>The next date, or the fact that there is none.</p></li></ol></div>""")}
{ch(8, 'motion', 'Motion: laying the line', 'Movement follows the idea: lines are drawn left to right, standing bars fall, layers open downward. Nothing bounces for its own sake.', f"""
<ul class="motion">
<li><b>The loader</b><code>1.8 s · once per session</code><p>A line is drawn across the screen, a green bar stands up through it, then falls to lie beneath it, and the page opens along the line. <a href="home.html?loader" style="text-decoration:underline">Replay it</a>.</p></li>
<li><b>The fall</b><code>500 ms · cubic-bezier(.5,0,.25,1.25)</code><p>The standing bar rotates down about its foot and settles a hair past flat, like a ruler laid on a desk.</p></li>
<li><b>Opening a layer</b><code>550 ms · ease-out (.22,1,.36,1)</code><p>The layer’s height grows from nothing, its text arrives 120 ms later. “Open every layer” lays them one after another, 110 ms apart, top to bottom.</p></li>
<li><b>Lines on scroll</b><code>1 s · from the left</code><p>Each section rule is drawn from its left end as it enters the screen.</p></li>
<li><b>Headline hover</b><code>450 ms</code><p>A line is laid under the headline, from the first letter.</p></li>
<li><b>Reduced motion</b><code>prefers-reduced-motion</code><p>No loader, no drawing; layers open instantly. Everything still works.</p></li>
</ul>""")}
{ch(9, 'photo', 'Photographs: the real place', 'Most stories carry a photograph, and every one shows the place it names, captioned with where and when it was taken.', f"""
<div class="two"><div class="prose" style="padding:0">
<p>Photographs come from Wikimedia Commons under free licences, shown in their own colour, never tinted or filtered. A photograph of a different town is never used to stand in for the one in the story.</p>
<p>Where no honest photograph exists, the story gets a plate: the place name on ruled lines, the plus above it. It is better to show nothing than to show something false.</p>
</div><div class="plate r43" style="border-radius:var(--r3)">{pl()}<b>Masafer Yatta</b><span>West Bank</span></div></div>""")}
{ch(10, 'voice', 'Voice: write the line first', 'Every story must stand as one sentence before anything is laid under it.', f"""
<ul class="voice">
<li class="y"><b>Write</b><p>Settlers set fire to two homes in Duma overnight, the village council says.</p></li>
<li class="n"><b>Not</b><p>Horror in Duma as violence erupts once again.</p></li>
<li class="y"><b>Write</b><p>No date has been set for phase two to begin.</p></li>
<li class="n"><b>Not</b><p>The future remains uncertain.</p></li>
</ul>
<ul class="spec" style="margin-top:22px"><li><span class="k">Rules</span><p>Who, what, where, and who says so, in the first line. Numbers with a date and a counter. Quotes short and exact. British spelling. Sentence-case headlines. No adjectives the facts don’t need.</p></li></ul>""")}
{ch(11, 'misuse', 'Misuse', 'A plus is a common shape; these four mistakes turn it into something else.', f'<ul class="dont">{dn}</ul>')}
{ch(12, 'files', 'Pages and files', 'The whole site, and the files to take away.', f"""
<div class="pages">
<a href="home.html">Today (home) {icon("i-right")}</a><a href="story/{lead['id']}.html">A story, all layers {icon("i-right")}</a>
<a href="gaza.html">Gaza desk {icon("i-right")}</a><a href="westbank.html">West Bank desk {icon("i-right")}</a><a href="jerusalem.html">Jerusalem desk {icon("i-right")}</a><a href="world.html">Diaspora &amp; World {icon("i-right")}</a>
<a href="explainers.html">Explainers {icon("i-right")}</a><a href="numbers.html">Numbers {icon("i-right")}</a><a href="ahead.html">Dates ahead {icon("i-right")}</a><a href="archive.html">Every line {icon("i-right")}</a>
<a href="layers.html">How the layers work {icon("i-right")}</a><a href="daily.html">The daily +1 {icon("i-right")}</a><a href="search.html">Search {icon("i-right")}</a><a href="corrections.html">Corrections {icon("i-right")}</a><a href="credits.html">Credits {icon("i-right")}</a><a href="404.html">404 {icon("i-right")}</a>
</div>
<p style="margin-top:22px"><a class="btn solid" href="assets/palestine-plus-identity.zip" download>{pl()}Download the identity files (SVG, fonts)</a></p>""")}
'''

html = (head('Identity', 'The Palestine+ identity: one more line. Mark, wordmark, colour, type, layers and motion.') +
        f'<main id="main">{body}</main>' + foot() + f'<script src="assets/js/pp.js?v={V}" defer></script>\n</body>\n</html>\n')
write('index.html', html)

zp = os.path.join(ROOT, 'assets', 'palestine-plus-identity.zip')
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(os.path.join(ROOT, 'assets', 'brand'))):
        z.write(os.path.join(ROOT, 'assets', 'brand', f), f'brand/{f}')
    for f in sorted(os.listdir(os.path.join(ROOT, 'assets', 'fonts'))):
        z.write(os.path.join(ROOT, 'assets', 'fonts', f), f'fonts/{f}')
    z.write(os.path.join(ROOT, 'favicon.svg'), 'brand/favicon.svg')
print('index.html + zip', os.path.getsize(zp) // 1024, 'KB')
