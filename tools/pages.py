"""Build every page but home and the identity book.

python -I tools/pages.py
story/<id>.html for every story, the four desks, explainers, numbers, dates ahead, every line
(archive), how the layers work, corrections, the daily +1, search (+ assets/data/search.json),
credits and 404 (absolute paths, so it works at any depth).
"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell
from shell import (when, C, E, S, BY, DESKS, DESK, LAYERS, TODAY, PH, ROOT, esc, pl, badge, link, kick, ago, depth, minutes,
                   picture, caption, photo, day, long_day, D, page, write, icon, src_link)
from parts import layer_body, stack, deep_list

newest = sorted(S, key=lambda s: (s['date'], s.get('time') or '00:00'), reverse=True)
R_ARROW = lambda: icon('i-right')


def row(s):
    return f'''<article class="row"><div class="meta"><span>{esc(DESK[s['desk']][1])}</span><span>{esc(ago(s))}</span><span>{esc(s['place'])}</span></div>
<div><h2 class="h-s"><a href="{link(s['id'])}"><span class="hl">{esc(s['headline'])}</span></a></h2><p class="dek">{esc(s['fact'])}</p>
<p class="meta" style="margin-top:8px;display:flex;gap:12px">{badge(depth(s))}<span>{minutes(s)} min deep</span></p></div>
<a href="{link(s['id'])}" tabindex="-1" aria-hidden="true">{picture(s, cls='ph r32', sizes='220px')}</a></article>'''


def page_h(title, dek, tally=None, label=None, with_pl=False):
    t = f'<p class="tally"><b>{tally[0]}</b>{esc(tally[1])}</p>' if tally else ''
    lb = f'<p class="lbl" style="margin-bottom:10px">{esc(label)}</p>' if label else ''
    return (f'<header class="page-h"><div class="wrap"><div class="in"><div>{lb}<h1 class="h-xl">{pl() if with_pl else ""}{shell.plus1() if title == "The daily +1" else esc(title)}</h1>'
            f'<p class="dek">{esc(dek)}</p></div>{t}</div></div></header>')


# ---------------------------------------------------------------- stories
def story(s):
    C.R = '../'
    ls = [(k, lab, d, s['layers'][k]) for k, lab, d in LAYERS if s['layers'].get(k)]
    gauge = (f'<a href="#fact" aria-current="true"><i class="ln-mark"></i><span>The fact<span class="d">line one</span></span></a>' +
             ''.join(f'<a href="#{k}"><i class="ln-mark"></i><span>{lab}<span class="d">layer {i}</span></span></a>'
                     for i, (k, lab, d, v) in enumerate(ls, 1)))
    layers = ''.join(f'<section class="layer" data-d="{d}" id="{k}" aria-labelledby="{k}-h"><h2 class="lay-h" id="{k}-h">{pl("open")}{lab}'
                     f'<span class="n">layer {i}</span></h2>{layer_body(k, v)}</section>' for i, (k, lab, d, v) in enumerate(ls, 1))
    srcs = ''.join(f'<li><span><a href="{esc(x["url"])}" rel="noopener" target="_blank">{esc(x["name"])}</a>'
                   f'{", " + esc(day(x["date"], year=True)) if x.get("date") else ""}</span></li>' for x in s['sources'])
    same = [x for x in newest if x['desk'] == s['desk'] and x['id'] != s['id']][:4]
    side = ''.join(f'<li><a href="{x["id"]}.html"><span class="hl">{esc(x["headline"])}</span></a></li>' for x in same)
    others = [x for x in newest if x['desk'] != s['desk'] and x['id'] != s['id']]
    ranked = [x for x in others if x.get('photo')] + [x for x in others if not x.get('photo')]
    more = [next(x for x in ranked if x['desk'] == k_) for k_, *_ in DESKS if k_ != s['desk'] and any(x['desk'] == k_ for x in ranked)][:3]
    dl = [x for x in newest if x['desk'] == s['desk']]
    i_ = dl.index(s)
    prev_, next_ = (dl[i_ + 1] if i_ + 1 < len(dl) else None), (dl[i_ - 1] if i_ > 0 else None)
    pn = ''.join(f'<a class="pn {c}" href="{x["id"]}.html"><span class="lbl">{t}</span><span class="h-s">{esc(x["headline"])}</span></a>'
                 for c, t, x in (('prev', 'The line before', prev_), ('next', 'The line after', next_)) if x)
    cards = ''.join(f'<article class="card"><a href="{x["id"]}.html" style="display:grid;gap:10px">{picture(x, cls="ph r32", sizes="(max-width:560px) 100vw, 30vw")}'
                    f'{kick(x)}<h3 class="h-s"><span class="hl">{esc(x["headline"])}</span></h3></a></article>' for x in more)
    ph = s.get('photo')
    figure = (f'<div class="wrap"><figure class="story-fig">{photo(ph, cls="ph r169", sizes="(max-width:1320px) 100vw, 1260px", eager=True)}{caption(ph)}</figure></div>'
              if ph else '')
    body = f'''<article>
<header class="story-h"><div class="wrap"><div class="in">
<p class="crumbs"><a href="../{s['desk']}.html">{esc(DESK[s['desk']][1])}</a><span aria-hidden="true">/</span><span>{esc(s['place'])}</span>{'<span aria-hidden="true">/</span><a href="../explainers.html">Explainer</a>' if s.get('explainer') else ''}</p>
<h1 class="h-xl">{esc(s['headline'])}</h1>
<p class="dek">{esc(s['standfirst'])}</p>
<p class="meta"><span>{esc(long_day(s['date']))}{(", " + s['time'] + " GMT") if s.get('time') else ""}</span><span>{esc(s['place'])}{(", " + esc(s['region'])) if s['region'] and s['region'] not in s['place'] else ""}</span><span>{len(ls)} layers · {minutes(s)} min deep</span></p>
</div></div></header>
{figure}
<div class="wrap story">
<nav class="rail" aria-label="Layers of this story"><p class="lbl" style="margin-bottom:10px">Depth</p><div class="gauge">{gauge}</div>
<p class="depth">Each layer sits one line deeper than the last.</p></nav>
<div>
<p class="factline" id="fact">{esc(s['fact'])}</p>
<div class="body">{''.join(f'<p>{esc(p)}</p>' for p in s['body'])}</div>
<div class="layers">{layers}</div>
<nav class="pnav" aria-label="More from this desk">{pn}</nav>
<div class="sources"><p class="lbl">Sources</p><ol>{srcs}</ol>
<p class="src" style="margin-top:6px">Every figure and quote above links to where it was published. Something wrong? <a href="../corrections.html">Corrections</a>.</p></div>
</div>
<aside>
<div class="side-card"><p class="lbl">Share</p><div class="share"><button type="button" data-copy>Copy link</button></div></div>
<div class="side-card"><p class="lbl">More from {esc(DESK[s['desk']][1])}</p><ul>{side}</ul><a class="side-more" href="../{s['desk']}.html">The {esc(DESK[s['desk']][1])} desk {R_ARROW()}</a></div>
</aside>
</div>
</article>
<section class="next-up"><div class="wrap"><div class="sec-h" style="border:0;padding-top:0"><h2>One more line</h2><a class="more" href="../home.html">Today {R_ARROW()}</a></div><div class="cards">{cards}</div></div></section>'''
    og = f'assets/img/photo/{ph}.webp' if ph else None
    write(f'story/{s["id"]}.html', page(s['headline'], s['fact'], body, current=s['desk'], og=og))


for s in S:
    story(s)

# ---------------------------------------------------------------- desks
C.R = ''


def desk_figures(ds, n=4):
    """The first distinct numbers laid under this desk's stories, newest first."""
    out, seen = [], set()
    for s in ds:
        for f in s['layers'].get('numbers') or []:
            key = (f['figure'], f['label'][:40])
            if key in seen:
                continue
            seen.add(key)
            out.append((f, s))
            if len(out) == n:
                return out
    return out


def lines(n):
    return f'{n} line' if n == 1 else f'{n} lines'


def by_day(ds, ids=False):
    groups, cur = [], None
    for s in ds:
        if s['date'] != cur:
            cur = s['date']
            idattr = f' id="d-{cur}"' if ids else ''
            groups.append(f'<h2 class="day-h"{idattr}><span>{esc(long_day(cur))}</span><span>{lines(sum(1 for x in ds if x["date"] == cur))}</span></h2>')
        groups.append(row(s))
    return ''.join(groups)


for k, label, title, dek in DESKS:
    ds = [s for s in newest if s['desk'] == k]
    top = next((s for s in ds if s.get('photo') and depth(s) >= 3), None) or next((s for s in ds if s.get('photo')), ds[0])
    rest = [s for s in ds if s['id'] != top['id']]
    figs = desk_figures(ds)
    fg = ''.join(f'<li><span class="num">{esc(f["figure"])}</span><p>{esc(f["label"])}</p>'
                 f'<p class="src"><a href="{link(x["id"])}">{esc(x["headline"])}</a></p></li>' for f, x in figs)
    nexts = sorted([s for s in ds if (s['layers'].get('next') or {}).get('date')], key=lambda s: s['layers']['next']['date'])
    nx = ''.join(f'<li><a href="{link(s["id"])}#next"><b>{esc(day(s["layers"]["next"]["date"], wd=True, year=D(s["layers"]["next"]["date"]).year != TODAY.year))}</b>'
                 f'<span>{esc(s["layers"]["next"]["text"])}</span></a></li>' for s in nexts[:4])
    lead = f'''<section class="desk-lead"><div class="wrap"><div class="grid">
<figure>{picture(top, cls="ph r32", sizes="(max-width:900px) 100vw, 54vw", eager=True)}{caption(top["photo"]) if top.get("photo") else ""}</figure>
<div>{kick(top)}<h2 class="h-l" style="margin-top:10px"><a href="{link(top["id"])}"><span class="hl">{esc(top["headline"])}</span></a></h2>
<p class="dek" style="margin-top:12px">{esc(top["standfirst"])}</p>{stack(top, "dl-" + k, open_first=False)}</div>
</div></div></section>'''
    side = (f'<section class="desk-figs"><div class="wrap"><div class="sec-h"><h2>{pl()}The {esc(label)} desk in numbers</h2><a class="more" href="numbers.html#n-{k}">All its figures {R_ARROW()}</a></div>'
            f'<ul class="figrow">{fg}</ul>'
            + (f'<div class="desk-next"><p class="lbl">What next on this desk</p><ul>{nx}</ul></div>' if nx else '') +
            '</div></section>') if figs else ''
    body = (page_h(title, dek, (len(ds), f'lines, {sum(depth(s) for s in ds)} layers under them')) + lead + side +
            f'<div class="wrap list"><div class="sec-h"><h2>Every {esc(label)} line</h2><span class="meta">newest first</span></div>{by_day(rest)}</div>')
    write(f'{k}.html', page(title, dek, body, current=k))

# explainers: each one opened all the way down
xs = [s for s in newest if s.get('explainer')]
blocks = []
for i, s in enumerate(xs):
    blocks.append(f'''<section class="ex-full{" alt" if i % 2 else ""}"><div class="wrap"><div class="grid">
<figure>{picture(s, cls="ph r43", sizes="(max-width:900px) 100vw, 46vw", eager=i == 0)}{caption(s["photo"]) if s.get("photo") else ""}</figure>
<div><p class="lbl" style="margin-bottom:10px">Explainer {i + 1} of {len(xs)} · {esc(DESK[s["desk"]][1])}</p>
<h2 class="h-l"><a href="{link(s["id"])}"><span class="hl">{esc(s["headline"])}</span></a></h2>
<p class="dek" style="margin-top:12px">{esc(s["standfirst"])}</p>{deep_list(s)}
<p style="margin-top:18px"><a class="btn solid" href="{link(s["id"])}">Read it layer by layer {R_ARROW()}</a></p></div>
</div></div></section>''')
write('explainers.html', page('Explainers', 'The long matters under the daily lines, opened all the way down.',
      page_h('Explainers', 'The matters that sit under a week of daily lines: what they are, how they got here and what happens next, each one opened all the way down.', (len(xs), 'explainers')) +
      ''.join(blocks), current='explainers'))

# every line
days = sorted({x['date'] for x in S}, reverse=True)
dayidx = ''.join(f'<li><a href="#d-{d_}"><b>{D(d_).day}</b><span>{D(d_).strftime("%a %b")}</span><i>{lines(sum(1 for x in S if x["date"] == d_))}</i></a></li>' for d_ in days)
groups = [f'<nav class="days" aria-label="Jump to a day"><ul>{dayidx}</ul></nav>', by_day(newest, ids=True)]
write('archive.html', page('Every line', 'Every story on Palestine+, newest first, day by day.',
      page_h('Every line', 'Every story this edition carries, newest first, with the number of layers under each.', (len(S), f'lines since {day(newest[-1]["date"])}')) +
      f'<div class="wrap list">{"".join(groups)}</div>'))

# numbers
lis = []
for f in E['figures']:
    lis.append(f'<li><span class="num" style="font-size:clamp(2rem,3.4vw,2.8rem);line-height:1">{esc(f["figure"])}</span><i class="tick" aria-hidden="true"><i data-k="1"></i></i>'
               f'<p>{esc(f["label"])}</p><p class="src">As of {esc(day(f["as_of"], year=True))} · {src_link(f)}</p></li>')
ledger, total = [], 0
for k, label, *_ in DESKS:
    rows_, seen = [], set()
    for s in newest:
        if s['desk'] != k:
            continue
        for n in s['layers'].get('numbers') or []:
            key = (n['figure'], n['label'][:40])
            if key in seen:
                continue
            seen.add(key)
            rows_.append(f'<tr><td class="num">{esc(n["figure"])}</td><td>{esc(n["label"])}</td>'
                         f'<td><a href="{link(s["id"])}">{esc(s["headline"])}</a></td><td class="src">{src_link(n)}</td></tr>')
    total += len(rows_)
    ledger.append(f'<section class="ledger" id="n-{k}" aria-labelledby="n-{k}-h"><h3 id="n-{k}-h">{esc(label)} <span>{len(rows_)} figures</span></h3>'
                  f'<div class="tbl"><table><thead><tr><th scope="col">Figure</th><th scope="col">What it counts</th><th scope="col">Under the story</th><th scope="col">Source</th></tr></thead>'
                  f'<tbody>{"".join(rows_)}</tbody></table></div></section>')
write('numbers.html', page('Numbers', 'The running figures and every number under this week’s stories, each with its source and date.',
      page_h('Numbers', 'The running figures, then every number laid under this week’s lines, desk by desk. Each is the latest its source published, with the date it was true.', label='Layer two', with_pl=True) +
      f'<section class="numbers on-ink" style="margin-top:0"><div class="wrap"><ul class="nums n5">{"".join(lis)}</ul></div></section>'
      f'<section class="explain"><div class="wrap"><div class="sec-h"><h2>Under the stories</h2><span class="meta">{total} figures, repeats folded</span></div>'
      f'{"".join(ledger)}</div></section>', current='numbers'))

# dates ahead: a timeline, with today drawn as the line
ah = sorted(E['ahead'], key=lambda a: a['date'])
tl, today_done = [], False
for a in ah:
    d_ = D(a['date'])
    if not today_done and d_ > TODAY:
        tl.append(f'<li class="now"><span>Today · {esc(day(TODAY, wd=True))}</span></li>')
        today_done = True
    state = 'is-today' if d_ == TODAY and not a.get('approx') else ''
    tl.append(f'<li class="{state}"><p class="when">{when(a, True)}</p><div><p>{esc(a["what"])}</p><p class="src">{src_link(a)}</p></div></li>')
if not today_done:
    tl.append(f'<li class="now"><span>Today · {esc(day(TODAY, wd=True))}</span></li>')
nexts = sorted([s for s in newest if s['layers'].get('next')],
               key=lambda s: (0, s['layers']['next']['date']) if s['layers']['next'].get('date') else (1, s['date']))
nx = ''.join(f'<article class="row"><div class="meta"><span>{esc(DESK[s["desk"]][1])}</span>'
             f'<span>{esc(day(s["layers"]["next"]["date"], wd=True, year=True)) if s["layers"]["next"].get("date") else "No date set"}</span></div>'
             f'<div><h2 class="h-s"><a href="{link(s["id"])}#next"><span class="hl">{esc(s["layers"]["next"]["text"])}</span></a></h2>'
             f'<p class="dek">From: {esc(s["headline"])}</p></div><div></div></article>' for s in nexts)
write('ahead.html', page('Dates ahead', 'The dated events coming up, and the “what next” layer of every story.',
      page_h('Dates ahead', 'The dated events coming up, then the last layer of every story: what happens next, and when, if anyone has said.', (len(ah), 'dates')) +
      f'<section class="ahead" style="border:0"><div class="wrap"><ol class="tl">{"".join(tl)}</ol></div></section>'
      f'<div class="wrap list"><div class="sec-h"><h2>{pl()}What next, story by story</h2><span class="meta">dated first, then the rest</span></div>{nx}</div>', current='ahead'))

# how the layers work
ex = BY[E['lead']]
how = ''.join(f'<li data-d="{d}"><b>{pl()}{lab}</b><p>{t}</p></li>' for lab, d, t in [
    ('The fact', 0, 'One sentence: what happened, where, and who says so. If you read nothing else, read this.'),
    ('Context', 1, 'Why it matters now: what came before, and the rule, line or deal it touches.'),
    ('Numbers', 2, 'The figures that measure it, each with the date it was true and the body that counted.'),
    ('Voices', 3, 'People who were there or who decide, quoted in their own words, short and exact.'),
    ('What next', 4, 'The next date, vote, hearing or deadline, if anyone has set one. If not, we say so.'),
])
write('layers.html', page('How the layers work', 'Every Palestine+ story is a line with up to four layers under it.',
      page_h('How the layers work', 'Every story is one line with up to four layers under it. Each layer sits one line deeper, and one tint darker, than the last.', label='About Palestine+') +
      f'''<div class="wrap prose">
<p class="lead-p">News from Palestine comes fast and it comes heavy. Palestine+ is built so you can take as much as you have time for: the line for the skim, the layers for the rest.</p>
<ol class="howto">{how}</ol>
<h2>The plus</h2>
<p>A news line is a horizontal stroke. The plus is that line with one more standing across it, waiting to be laid down. Press it and the standing line falls flat beneath the first: you are one layer deeper. The badge beside a headline, {badge(3)}, counts the layers under it.</p>
<h2>Sources</h2>
<p>Every line and every layer carries the name of the body that published it and a link to where. We prefer the people closest to the event: health authorities, UN agencies, municipalities, rights groups that count, and reporters who were there. Where accounts differ we give both and say who says what.</p>
<h2>Corrections</h2>
<p>When we get something wrong we change it and say so at the foot of the story and on the <a href="corrections.html">corrections page</a>, with the date.</p>
<p>See it working on today’s lead: <a href="{link(ex['id'])}">{esc(ex['headline'])}</a>.</p>
</div>'''))

# corrections
write('corrections.html', page('Corrections', 'What we got wrong, what we changed and when.',
      page_h('Corrections', 'What we got wrong, what we changed and when. A correction is a line laid under the story, never a line taken away.') +
      f'''<div class="wrap prose">
<p>This is a design prototype, so there is no corrections log yet. When Palestine+ publishes, each correction will be listed here with the story, the date, what was wrong and what it says now, and the same note will sit at the foot of the story itself.</p>
<p>To report an error, write to the desk that ran the story. Tell us the line, the layer and the source that shows it is wrong.</p>
<p><a href="layers.html">How the layers work</a> · <a href="home.html">Back to today</a></p>
</div>'''))

# the daily +1
write('daily.html', page('The daily +1', 'The day’s lines each morning, and one story opened all the way down.',
      page_h('The daily +1', 'Every morning at 07:00 GMT: the day’s lines, and one of them opened all the way down. Five minutes if you skim, fifteen if you go deep.', label='Newsletter') +
      f'''<div class="wrap prose">
<form class="sub" action="#" method="post" data-proto style="max-width:520px"><label for="em-p">Email address</label><input id="em-p" name="email" type="email" placeholder="you@example.com" autocomplete="email" required><button type="submit">{pl()}Get the daily +1</button><p class="msg" role="status"></p></form>
<h2>What it looks like</h2>
<ol class="howto">
<li data-d="0"><b>The lines</b><p>Eight to twelve one-line facts from the four desks, each with its source.</p></li>
<li data-d="1"><b>{pl()}The +1</b><p>One of them opened all the way: context, numbers, voices and what next.</p></li>
<li data-d="2"><b>Dates ahead</b><p>What is set for the coming days: votes, hearings, deadlines, marches.</p></li>
</ol>
<p>No tracking pixels. Unsubscribe in one click from any issue.</p>
</div>'''))

# search
data = [{'u': link(s['id']), 'h': s['headline'], 'f': s['fact'], 'p': s['place'], 'desk': s['desk'],
         'dl': DESK[s['desk']][1], 'd': day(s['date']), 'n': depth(s)} for s in newest]
write('assets/data/search.json', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
chips = ''.join(f'<button type="button" aria-pressed="false" data-desk="{k}">{esc(l)}</button>' for k, l, *_ in DESKS)
write('search.html', page('Search', 'Search every line and layer on Palestine+.',
      page_h('Search', 'Every line this edition carries. Search a place, a name or a word, or narrow it to one desk.') +
      f'''<div class="wrap search"><form data-search="assets/data/search.json" role="search"><label class="vh" for="q">Search the news</label>
<input id="q" name="q" type="search" placeholder="Jenin, Al-Aqsa, ceasefire, olive…" autocomplete="off"><button class="btn solid" type="submit" style="min-height:52px">{icon("i-search")}Search</button></form>
<div class="chips" role="group" aria-label="Desk">{chips}</div><div class="results" aria-live="polite"></div></div>'''))

# credits
used = sorted({s['photo'] for s in S if s.get('photo')})
cr = ''.join(f'<li><a href="{esc(PH[p]["page_url"])}" rel="noopener" target="_blank">{esc(PH[p]["caption"])}</a> {esc(PH[p]["author"])}, {esc(PH[p]["license"])}.</li>' for p in used)
write('credits.html', page('Credits', 'Photographs, type and sources used in this prototype.',
      page_h('Credits', 'The photographs, the type and the method behind this prototype.') +
      f'''<div class="wrap prose">
<h2>Photographs</h2>
<p>All {len(used)} photographs come from Wikimedia Commons under free licences. Each shows the place named in its caption; where no honest photograph of a place exists, the story carries a plate with the place name instead of a stand-in picture.</p>
<ul class="dots">{cr}</ul>
<h2>Type</h2>
<p>Newsreader by Production Type and Schibsted Grotesk by Bakken &amp; Bæck, both under the SIL Open Font License, self-hosted as subsets.</p>
<h2>Stories</h2>
<p>Every story is drawn from published reporting, linked at its foot. The writing is ours; the facts are theirs.</p>
</div>'''))

# about
desk_lis = ''.join(f'<li data-d="{i}"><b>{esc(l)}</b><p>{esc(d_)} <a href="{k}.html">{sum(1 for x in S if x["desk"] == k)} lines</a></p></li>'
                   for i, (k, l, _t, d_) in enumerate(DESKS))
write('about.html', page('About', 'What Palestine+ is, what it covers and how it is made.',
      page_h('About Palestine+', 'English news from Palestine, one line at a time, with every layer under it sourced.', label='About') +
      f'''<div class="wrap prose">
<p class="lead-p">Palestine+ is a news site for readers who want the facts from Gaza, the West Bank and Jerusalem without wading through them: one line for the skim, and as many layers under it as they have time for.</p>
<h2>What we cover</h2>
<ol class="howto">{desk_lis}</ol>
<h2>How a story is made</h2>
<p>Every story starts as one sentence that must stand on its own: what happened, where, and who says so. Only then is anything laid under it, in the same order every time: context, numbers, voices, and what happens next. <a href="layers.html">How the layers work</a> explains each one.</p>
<p>We report from published sources and name them on every line and every layer: health authorities, UN agencies, municipalities, rights groups that count, and reporters who were there. Where they disagree we give both figures and say who gives which.</p>
<h2>Photographs</h2>
<p>A photograph on Palestine+ shows the place the story names, captioned with where and when it was taken. Where no honest photograph exists, the story carries the place name instead. See the <a href="credits.html">credits</a>.</p>
<h2>This prototype</h2>
<p>This is a design prototype built by TakTek for Palestine+. The stories are real and linked to their sources; the newsroom, its staff and its readership are not yet. Contact details will be published when the newsroom launches.</p>
<p><a href="corrections.html">Corrections</a> · <a href="privacy.html">Privacy</a> · <a href="index.html">The identity</a></p>
</div>'''))

# privacy
write('privacy.html', page('Privacy', 'What this site stores about you: almost nothing.',
      page_h('Privacy', 'What this site keeps about you, which is almost nothing.', label='About') +
      '''<div class="wrap prose">
<p class="lead-p">No cookies, no analytics, no advertising, no tracking pixels and no third-party scripts.</p>
<h2>What your browser keeps</h2>
<ul class="dots">
<li><code>pp-laid</code> in session storage, so the opening animation plays once per visit and not on every page.</li>
<li><code>pp-nav</code> in session storage for a fraction of a second, so the next page knows to open along the line.</li>
</ul>
<p>Both are deleted when you close the tab. Neither leaves your browser.</p>
<h2>What we load</h2>
<p>Every file this site uses, including its fonts and photographs, is served from the site itself. Links to sources take you to the publisher’s own site, under its own privacy terms.</p>
<h2>Forms</h2>
<p>The newsletter forms on this prototype send nothing and store nothing. When the newsletter launches, this page will say what it keeps, why, and how to remove it.</p>
</div>'''))

# 404 with absolute paths
C.R = '/palestine-plus-prototype/'
write('404.html', page('Not here', 'This page does not exist.',
      f'''<div class="wrap lost"><span class="pl big-pl" aria-hidden="true"><i class="pl-h"></i><i class="pl-v"></i></span>
<h1 class="h-l">There is no line here.</h1><p class="dek">The page may have moved, or the address has a typo. Every story is still one line away.</p>
<p class="row2"><a class="btn solid" href="{C.R}home.html">Today’s lines</a><a class="btn" href="{C.R}search.html">Search</a></p></div>'''))
print('pages built:', len(S), 'stories + desks and utility pages')
