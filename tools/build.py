"""Build home.html, the front page, from tools/edition.json.

python -I tools/build.py
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import (when, plus1, C, E, S, BY, DESKS, DESK, TODAY, esc, pl, badge, link, kick, ago, depth, minutes,
                   picture, caption, photo, day, D, page, write, icon, src_link, long_day)
from parts import stack, skim, deep_list

C.R = ''
lead = BY[E['lead']]
feature = BY[E['feature']]
used = {lead['id'], feature['id']}
newest = sorted(S, key=lambda s: (s['date'], s.get('time') or '00:00'), reverse=True)


def lead_block():
    s = lead
    ph = s.get('photo')
    fig = (f'<figure>{photo(ph, cls="ph r43", sizes="(max-width:900px) 100vw, 46vw", eager=True)}{caption(ph)}</figure>'
           if ph else f'<figure>{picture(s, cls="ph r43")}</figure>')
    return f'''<section class="lead" aria-labelledby="lead-h"><div class="wrap"><div class="grid">
<div>
{kick(s)}
<h1 class="h-xl" id="lead-h"><a href="{link(s['id'])}"><span class="hl">{esc(s['headline'])}</span></a></h1>
<p class="fact">{esc(s['standfirst'])}</p>
<p class="meta"><span>{esc(s['place'])}</span><span>{depth(s)} layers</span><span>{minutes(s)} min all the way down</span></p>
{stack(s, 'lead')}
</div>
{fig}
</div></div></section>'''


def lines_block():
    pick = [s for s in newest if s['id'] not in used and not s.get('explainer')][:12]
    used.update(s['id'] for s in pick)
    half = (len(pick) + 1) // 2
    col = lambda xs, o: '<ul>' + ''.join(skim(s, f'ln{o + i}') for i, s in enumerate(xs)) + '</ul>'
    return f'''<section class="lines" aria-labelledby="lines-h"><div class="wrap">
<div class="sec-h rv"><h2 id="lines-h">Line one</h2><p class="how">{pl()}Skim the lines. Press any of them for the layers underneath.</p></div>
<div class="grid">{col(pick[:half], 0)}{col(pick[half:], half)}</div>
</div></section>'''


def desks_block():
    cols = []
    for k, label, title, _ in DESKS:
        ds = [s for s in newest if s['desk'] == k and not s.get('explainer')]
        top = next((s for s in ds if s.get('photo') and s['id'] not in used), None) or next((s for s in ds if s['id'] not in used), ds[0])
        rest = [s for s in ds if s['id'] != top['id']][:3]
        lis = ''.join(f'<li><a href="{link(s["id"])}"><span class="hl">{esc(s["headline"])}</span>{badge(depth(s))}</a></li>' for s in rest)
        cols.append(f'''<div class="desk rv"><div class="desk-h"><a href="{k}.html">{esc(label)} {icon("i-right")}</a><span class="meta">{len(ds)} lines</span></div>
<div class="top"><a href="{link(top['id'])}">{picture(top, cls="ph r32", sizes="(max-width:600px) 100vw, (max-width:1100px) 50vw, 25vw")}
<span class="meta">{esc(top['place'])} · {esc(ago(top))}</span><h3 class="h-s"><span class="hl">{esc(top['headline'])}</span></h3></a></div>
<ul>{lis}</ul></div>''')
    return f'''<section class="desks" aria-labelledby="desks-h"><div class="wrap">
<div class="sec-h rv"><h2 id="desks-h">The four desks</h2><a class="more" href="archive.html">Every line {icon("i-right")}</a></div>
<div class="grid">{''.join(cols)}</div>
</div></section>'''


def feature_block():
    s = feature
    return f'''<section class="feature" aria-labelledby="ft-h"><div class="wrap"><div class="grid">
<div class="rv">
<p class="lbl" style="margin-bottom:12px">Opened all the way down</p>
{kick(s)}
<h2 class="h-l" id="ft-h" style="margin-top:10px"><a href="{link(s['id'])}"><span class="hl">{esc(s['headline'])}</span></a></h2>
<p class="dek">{esc(s['standfirst'])}</p>
{deep_list(s)}
<p style="margin-top:18px"><a class="btn solid" href="{link(s['id'])}">Read it layer by layer {icon("i-right")}</a></p>
</div>
<figure class="rv">{picture(s, cls="ph r54", sizes="(max-width:900px) 100vw, 44vw")}{caption(s['photo']) if s.get('photo') else ''}</figure>
</div></div></section>'''


def numbers_block():
    figs = E['figures'][:8]
    lis = []
    for f in figs:
        raw = f['figure']
        mt = re.match(r'^([\d][\d,.]*)(.*)$', raw)
        lead_n, rest = (mt.group(1), mt.group(2)) if mt else (raw, '')
        countable = mt and not rest.startswith(('–', '-'))
        num = lead_n.replace(',', '')
        val = (f'<span class="num" data-count="{num}">{esc(lead_n)}<span class="u">{esc(rest)}</span></span>' if countable
               else f'<span class="num">{esc(raw)}</span>')
        lis.append(f'<li>{val}<i class="tick" aria-hidden="true"><i data-k="1"></i></i><p>{esc(f["label"])}</p>'
                   f'<p class="src">As of {esc(day(f["as_of"]))} · {src_link(f)}</p></li>')
    return f'''<section class="numbers on-ink" aria-labelledby="num-h"><div class="wrap">
<div class="sec-h rv"><h2 id="num-h">{pl("on")}Numbers</h2><a class="more" href="numbers.html">Every figure and its source {icon("i-right")}</a></div>
<p class="lede">The running figures under this week’s lines. Each is the latest the named source has published, with the date it was true.</p>
<ul class="nums">{''.join(lis)}</ul>
</div></section>'''


def explain_block():
    xs = [s for s in S if s.get('explainer')][:3]
    if not xs:
        return ''
    cards = []
    for s in xs:
        steps = ''.join(f'<li>{label}</li>' for k, label, d in [('fact', 'The fact', 0)] + [(k, l, d) for k, l, d in
                        __import__('shell').LAYERS if s['layers'].get(k)])
        cards.append(f'''<article class="ex rv"><a href="{link(s['id'])}" style="display:grid;gap:12px">{picture(s, cls="ph r169", sizes="(max-width:960px) 100vw, 30vw")}
{kick(s, with_date=False)}<h3 class="h-m"><span class="hl">{esc(s['headline'])}</span></h3></a><p class="dek" style="font-size:1rem">{esc(s['standfirst'])}</p><ol class="steps">{steps}</ol></article>''')
    return f'''<section class="explain" aria-labelledby="ex-h"><div class="wrap">
<div class="sec-h rv"><h2 id="ex-h">Explainers</h2><a class="more" href="explainers.html">All explainers {icon("i-right")}</a></div>
<div class="ex-grid">{''.join(cards)}</div>
</div></section>'''


def ahead_block():
    items = [a for a in E['ahead'] if a['date'] >= E['date']][:5]
    lis = ''.join(f'''<li class="rv"><p class="when">{when(a)}</p>
<p>{esc(a['what'])}</p><p class="src">{src_link(a)}</p></li>''' for a in items)
    return f'''<section class="ahead" aria-labelledby="ah-h"><div class="wrap">
<div class="sec-h rv"><h2 id="ah-h">Dates ahead</h2><a class="more" href="ahead.html">The calendar {icon("i-right")}</a></div>
<ol>{lis}</ol>
</div></section>'''


def daily_block():
    return f'''<section class="daily" aria-labelledby="dl-h"><div class="wrap"><div class="box rv">
<div><p class="lbl">Newsletter</p><h2 class="h-l" id="dl-h" style="margin-top:8px">{plus1()}</h2>
<p class="dek" style="margin-top:10px">Every morning at 07:00 GMT: the day’s lines, and one of them opened all the way down. Five minutes if you skim, fifteen if you go deep.</p></div>
<form class="sub" action="#" method="post" data-proto><label for="em-h">Email address</label><input id="em-h" name="email" type="email" placeholder="you@example.com" autocomplete="email" required><button type="submit">{pl()}Get the daily +1</button><p class="msg" role="status"></p></form>
</div></div></section>'''


body = lead_block() + lines_block() + desks_block() + feature_block() + numbers_block() + explain_block() + ahead_block() + daily_block()
write('home.html', page('Today', f'Palestine+ for {long_day(TODAY)}: the news from Gaza, the West Bank, Jerusalem and the world, one line at a time and one layer deeper.',
                        body, current='home', with_loader=True))
print('home.html', len(S), 'stories; lead', lead['id'])
