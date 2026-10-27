"""The page shell every built page shares: head, strip, masthead, desks, footer, loader, the plus.

Imported by build.py (home) and pages.py (everything else). C.R is the path back to the site
root; pages in folders set it to '../', the 404 page to the absolute site path.
"""
import datetime as dt
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = '4'                                       # bump on any asset change (Chrome caches hard)
SITE = 'Palestine+'
BASE_URL = 'https://taktek-dev.github.io/palestine-plus-prototype/'
E = json.load(open(os.path.join(ROOT, 'tools', 'edition.json'), encoding='utf-8'))
MARKS = json.load(open(os.path.join(ROOT, 'tools', 'out', 'marks.json'), encoding='utf-8'))
PH = json.load(open(os.path.join(ROOT, 'tools', 'photos.json'), encoding='utf-8'))
DIM_P = os.path.join(ROOT, 'tools', 'out', 'photos.json')
DIM = json.load(open(DIM_P, encoding='utf-8')) if os.path.exists(DIM_P) else {}
esc = html.escape
D = dt.date.fromisoformat
TODAY = D(E['date'])
S = E['stories']
BY = {s['id']: s for s in S}


class Ctx:
    R = ''


C = Ctx()

DESKS = [  # slug, tab label, page title, standfirst
    ('gaza', 'Gaza', 'Gaza', 'The Strip under the ceasefire: strikes and the dead, aid at the crossings, the yellow line and the families on either side of it.'),
    ('westbank', 'West Bank', 'West Bank', 'Raids, settlers and demolitions, the camps of the north and the olive harvest, village by village.'),
    ('jerusalem', 'Jerusalem', 'Jerusalem', 'Al-Aqsa and its gates, Silwan and Sheikh Jarrah, the orders, the demolitions and the people who stay.'),
    ('world', 'Diaspora & World', 'Diaspora & World', 'Courts, councils and capitals, the marches, and Palestinians abroad asking for a say.'),
]
DESK = {d[0]: d for d in DESKS}
LAYERS = [  # key, label, depth
    ('context', 'Context', 1),
    ('numbers', 'Numbers', 2),
    ('voices', 'Voices', 3),
    ('next', 'What next', 4),
]


def day(d, year=False, wd=False):
    d = D(d) if isinstance(d, str) else d
    s = f"{d.day} {d.strftime('%b')}" + (f" {d.year}" if year else '')
    return (d.strftime('%a') + ' ' + s) if wd else s


def long_day(d):
    d = D(d) if isinstance(d, str) else d
    return f"{d.strftime('%A')} {d.day} {d.strftime('%B')} {d.year}"


def ago(s):
    """'Today 09:40', 'Yesterday', 'Sat 24 Oct' — the way the desk would say it."""
    d = D(s['date'])
    n = (TODAY - d).days
    if n == 0:
        return f"Today {s['time']}" if s.get('time') else 'Today'
    if n == 1:
        return 'Yesterday'
    if n < 6:
        return d.strftime('%a') + (f" {s['time']}" if s.get('time') else '')
    return day(d)


def when(a, long=False):
    d = D(a['date'])
    if a.get('approx'):
        return f"<b>{d.strftime('%b')}</b><span>{d.year} · date not set</span>"
    return f"<b>{d.day}</b><span>{d.strftime('%B' if long else '%b')} · {d.strftime('%A' if long else '%a')}{' ' + str(d.year) if d.year != TODAY.year else ''}</span>"


def depth(s):
    """How many layers sit under the line."""
    return sum(1 for k, *_ in LAYERS if s['layers'].get(k))


def minutes(s):
    words = sum(len(p.split()) for p in s['body']) + len(s['fact'].split())
    for k, *_ in LAYERS:
        v = s['layers'].get(k)
        if isinstance(v, dict):
            words += len(v.get('text', '').split())
        elif isinstance(v, list):
            words += sum(len(json.dumps(x).split()) for x in v)
    return max(1, round(words / 220))


# ---------------------------------------------------------------- icons and marks
SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="i-right" viewBox="0 0 16 16"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-search" viewBox="0 0 16 16"><path d="M7 2.5a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9zM10.4 10.4 14 14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></symbol>
<symbol id="i-out" viewBox="0 0 16 16"><path d="M6 3.5H3.5v9h9V10M9 3h4v4M13 3 7.5 8.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-cal" viewBox="0 0 16 16"><path d="M3 4.5h10v8.5H3zM3 7.5h10M6 3v3M10 3v3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</defs></svg>'''


def icon(name, cls='ic'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{name}"/></svg>'


def pl(cls=''):
    """The plus as a live element: a lying bar in the text colour, a standing bar in green."""
    return f'<span class="pl{(" " + cls) if cls else ""}" aria-hidden="true"><i class="pl-h"></i><i class="pl-v"></i></span>'


def plus1(text='The daily'):
    """'The daily +1' with the drawn plus, for headings where a typed + would sit on the maths axis."""
    return f'{text} <span class="p1">{pl()}1</span>'


def badge(n):
    return f'<span class="badge" title="{n} more {"layer" if n == 1 else "layers"} under this line">{pl()}{n}</span>'


def wordmark(ink='currentColor', plus='var(--plus)', label=SITE):
    m = MARKS
    def r(b, fill):
        x, y, w, h, rr = b
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rr:.1f}" style="fill:{fill}"/>'
    return (f'<svg viewBox="{m["viewBox"]}" role="img" aria-label="{esc(label)}">'
            f'<path d="{m["word"]}" style="fill:{ink}"/><g class="wm-v">{r(m["V"], plus)}</g>{r(m["H"], ink)}</svg>')


# ---------------------------------------------------------------- photographs
def photo(slug, sizes='100vw', cls='ph', eager=False):
    if not slug or slug not in PH:
        return ''
    p = PH[slug]
    dm = DIM.get(slug, {'w': 1000, 'h': 667})
    pos = f' style="object-position:{p["focus"]}"' if p.get('focus') else ''
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<div class="{cls}"><img src="{C.R}assets/img/photo/{slug}.webp?v={V}" width="{dm["w"]}" height="{dm["h"]}" '
            f'alt="{esc(p["alt"])}" sizes="{sizes}" {load}{pos}></div>')


def plate(s, cls='plate r32'):
    return f'<div class="{cls}">{pl()}<b>{esc(s["place"])}</b><span>{esc(DESK[s["desk"]][1])}</span></div>'


def picture(s, cls='ph r32', sizes='100vw', eager=False, fallback=True):
    img = photo(s.get('photo'), sizes=sizes, cls=cls, eager=eager)
    if img:
        return img
    return plate(s, cls.replace('ph', 'plate')) if fallback else ''


def caption(slug):
    p = PH[slug]
    return f'<figcaption>{esc(p["caption"])} Photo: {esc(p["author"])}, {esc(p["license"])}, via Wikimedia Commons.</figcaption>'


def fig(slug, cls='ph r169', **kw):
    img = photo(slug, cls=cls, **kw)
    return f'<figure>{img}{caption(slug)}</figure>' if img else ''


def link(sid):
    return f'{C.R}story/{sid}.html'


def kick(s, with_date=True):
    dd = f'<span class="d">{esc(ago(s))}</span>' if with_date else ''
    return f'<p class="kick"><span>{esc(DESK[s["desk"]][1])}</span>{dd}</p>'


def src_link(o):
    if not o:
        return ''
    name = esc(o.get('source') or o.get('name') or '')
    u = o.get('url')
    return f'<a href="{esc(u)}" rel="noopener" target="_blank">{name}</a>' if u else name


# ---------------------------------------------------------------- the shell
# Runs in <head> before the first paint, so neither curtain flashes the page first:
# first page of the session -> the full loader (js-load); arriving from another page of the
# site -> the page starts closed along the line (pp-arrive) and pp.js opens it.
EARLY = ("(function(){var d=document.documentElement,s;try{s=sessionStorage}catch(e){return}"
         "if(matchMedia('(prefers-reduced-motion: reduce)').matches){s.setItem('pp-laid','1');s.removeItem('pp-nav');return}"
         "if(location.search.indexOf('loader')>-1||s.getItem('pp-laid')!=='1')d.classList.add('js-load');"
         "else if(s.getItem('pp-nav')==='1')d.classList.add('pp-arrive');s.removeItem('pp-nav')})()")


def curtain():
    """Page-to-page: the two halves close on a line, the next page opens along it."""
    return '<div class="nav-ldr" aria-hidden="true"><i class="half t"></i><i class="half b"></i><i class="line"></i></div>'


def head(title, desc, og=None, canonical=''):
    t = esc(title if title == SITE else f'{title} · {SITE}')
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0B1420">
<link rel="icon" href="{C.R}favicon.svg?v={V}" type="image/svg+xml">
<link rel="preload" href="{C.R}assets/fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{C.R}assets/fonts/schibsted.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{C.R}assets/css/pp.css?v={V}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{BASE_URL}{og or 'assets/og.png'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="noindex">
<script>{EARLY}</script>
</head>
<body>
{loader()}{curtain()}<a class="skip" href="#main">Skip to the news</a>
{SPRITE}'''


def strip():
    n = sum(1 for s in S if s['date'] == E['date'])
    lines = f'{n} new {"line" if n == 1 else "lines"} today' if n else 'The day’s lines'
    return (f'<div class="strip"><div class="wrap"><span><b>{long_day(TODAY)}</b></span>'
            f'<span class="lv">Updated {E["updated"]} GMT</span><span class="hide-s">{lines}</span>'
            f'<span class="sp"></span><a class="hide-s" href="{C.R}layers.html">How the layers work</a>'
            f'<a class="hide-s" href="{C.R}corrections.html">Corrections</a></div></div>')


def mast(current=''):
    tabs = ([('home', 'Today', f'{C.R}home.html')] + [(k, l, f'{C.R}{k}.html') for k, l, *_ in DESKS] +
            [('explainers', 'Explainers', f'{C.R}explainers.html'), ('numbers', 'Numbers', f'{C.R}numbers.html'),
             ('ahead', 'Dates ahead', f'{C.R}ahead.html')])
    lis = ''.join(
        f'<li><a href="{u}"{" aria-current=\"page\"" if k == current else ""}>'
        f'{pl() if k == "numbers" else ""}{esc(l)}</a></li>' for k, l, u in tabs)
    return f'''<header class="mast">
<div class="wrap">
<div class="top">
<p class="motto">News from Palestine. One line for the skim, one more for every layer under it.</p>
<a class="brand" href="{C.R}home.html" aria-label="{SITE}, today">{wordmark()}</a>
<div class="tools"><a class="btn icon" href="{C.R}search.html" aria-label="Search the news">{icon("i-search")}</a><a class="btn" href="{C.R}daily.html">{plus1()}</a></div>
</div>
<nav class="tabs" aria-label="Desks"><ul>{lis}</ul></nav>
</div>
</header>'''


def loader():
    return (f'<div class="ldr" aria-hidden="true"><div class="half t"></div><div class="half b"></div>'
            f'<p class="say say2">One line at a time.</p><i class="line"></i><i class="stand"></i>'
            f'<p class="say"><b>{long_day(TODAY)}</b> · {len(S)} lines, {sum(depth(s) for s in S)} layers under them</p></div>')


def foot():
    desks = ''.join(f'<li><a href="{C.R}{k}.html">{esc(l)}</a></li>' for k, l, *_ in DESKS)
    return f'''<footer class="foot on-ink">
<div class="wrap">
<div><a class="brand" href="{C.R}home.html" aria-label="{SITE}, today">{wordmark(ink="#fff", plus="var(--plus-on)")}</a>
<p style="margin-top:16px;max-width:42ch">News from Gaza, the West Bank, Jerusalem and the world, told one line at a time. Every line has a source. Every layer under it has one too.</p></div>
<div><p class="lbl">The daily +1</p><p style="margin-top:6px">The day’s lines each morning at 07:00 GMT, and one story opened all the way down.</p>
<form class="sub" action="#" method="post" data-proto><label for="em-f">Email address</label><input id="em-f" name="email" type="email" placeholder="you@example.com" autocomplete="email" required><button type="submit">{pl()}Subscribe</button><p class="msg" role="status"></p></form></div>
<div><p class="lbl">Desks</p><ul>{desks}<li><a href="{C.R}explainers.html">Explainers</a></li><li><a href="{C.R}numbers.html">Numbers</a></li></ul></div>
<div><p class="lbl">Palestine+</p><ul><li><a href="{C.R}ahead.html">Dates ahead</a></li><li><a href="{C.R}archive.html">Every line</a></li><li><a href="{C.R}layers.html">How the layers work</a></li><li><a href="{C.R}corrections.html">Corrections</a></li><li><a href="{C.R}search.html">Search</a></li><li><a href="{C.R}index.html">Identity</a></li></ul></div>
</div>
<div class="credits"><div class="wrap"><span>Design prototype by TakTek. Not a live newsroom: the stories are real and sourced, the publication is not yet.</span><span>Type: Newsreader and Schibsted Grotesk (OFL). Photographs: Wikimedia Commons, <a href="{C.R}credits.html">credited here</a>.</span></div></div>
</footer>'''


def page(title, desc, body, current='', og=None):
    return (head(title, desc, og=og) + strip() + mast(current) +
            f'<main id="main">{body}</main>' + foot() +
            f'<script src="{C.R}assets/js/pp.js?v={V}" defer></script>\n</body>\n</html>\n')


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
