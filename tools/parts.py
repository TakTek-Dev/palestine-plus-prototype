"""Layer components shared by the home page and the story pages.

A story is a fact line and up to four layers under it (context, numbers, voices, what next),
each one tint deeper than the last. The same data renders three ways: the stack (a button per
layer, home lead and feature), the skim line (one button opening every layer at once) and the
story page (all layers laid out, with the depth gauge beside them).
"""
from shell import C, DESK, LAYERS, E, esc, pl, badge, link, ago, depth, src_link, minutes, day, D


def layer_body(k, v, compact=False):
    """Inner HTML of one layer."""
    if k in ('context', 'next'):
        when = ''
        if k == 'next' and v.get('date') and not compact:
            dd = D(v['date'])
            when = f'<p class="when">{esc(day(dd, wd=True, year=dd.year != D(E["date"]).year))}</p>'
        return f'{when}<p>{esc(v["text"])}</p><p class="src">Source: {src_link(v)}</p>'
    if k == 'numbers':
        if compact:
            n = v[0]
            return (f'<p><span class="num">{esc(n["figure"])}</span>{esc(n["label"])}</p>'
                    f'<p class="src">Source: {src_link(n)}</p>')
        if len(v) == 1:
            n = v[0]
            return (f'<div class="big"><span class="num">{esc(n["figure"])}</span><span>{esc(n["label"])}</span></div>'
                    f'<p class="src">Source: {src_link(n)}</p>')
        cells = ''.join(f'<div><span class="num">{esc(n["figure"])}</span><p>{esc(n["label"])}</p>'
                        f'<p class="src">Source: {src_link(n)}</p></div>' for n in v)
        return f'<div class="nrow">{cells}</div>'
    if k == 'voices':
        vs = v[:1] if compact else v
        return ''.join(f'<div class="q"><blockquote>{esc(q["quote"])}</blockquote>'
                       f'<cite>{esc(q["who"])}<span>{", " + esc(q["role"]) if q.get("role") else ""} · {src_link(q)}</span></cite></div>'
                       for q in vs)
    return ''


def stack(s, uid, open_first=True):
    """The lead's stack: a button per layer; the first one laid open."""
    rows = []
    i = 0
    for k, label, d in LAYERS:
        v = s['layers'].get(k)
        if not v:
            continue
        i += 1
        op = 'true' if (open_first and i == 1) else 'false'
        pid = f'{uid}-{k}'
        rows.append(
            f'<div class="lay" data-d="{d}"><button class="lay-b" type="button" data-lay aria-expanded="{op}" aria-controls="{pid}">'
            f'{pl()}<span class="lay-h">{label}<span class="n">layer {i}</span></span></button>'
            f'<div class="lay-p" id="{pid}" role="region" aria-label="{label}"><div><div class="lay-c">{layer_body(k, v)}</div></div></div></div>')
    n = len(rows)
    first = s['sources'][0] if s.get('sources') else None
    return (f'<div class="stack" data-stack>'
            f'<div class="lay" data-d="0"><div class="lay-b" style="cursor:default"><span class="lay-h">The fact<span class="n">line one</span></span></div>'
            f'<div class="lay-c" style="opacity:1;transform:none;padding-top:0"><p>{esc(s["fact"])}</p>'
            f'{f"<p class=src>Source: {src_link(first)}</p>" if first else ""}</div></div>'
            + ''.join(rows) +
            f'<div class="stack-f"><button type="button" data-all>Open every layer</button>'
            f'<a class="go" href="{link(s["id"])}">Read the full story <svg class="ic" aria-hidden="true"><use href="#i-right"/></svg></a></div></div>')


def skim(s, uid):
    """One line of the skim: a button that lays every layer under it at once."""
    n = depth(s)
    rows = []
    for k, label, d in LAYERS:
        v = s['layers'].get(k)
        if v:
            rows.append(f'<div data-d="{d}"><p class="lbl">{pl("open")}{label}</p>{layer_body(k, v, compact=True)}</div>')
    pid = f'{uid}-p'
    return (f'<li class="ln"><button class="ln-b" type="button" data-lay aria-expanded="false" aria-controls="{pid}">'
            f'<span class="meta">{esc(DESK[s["desk"]][1])}<br>{esc(ago(s))}</span><span class="t">{esc(s["headline"])}</span>{badge(n)}</button>'
            f'<div class="ln-p" id="{pid}" role="region" aria-label="Layers under: {esc(s["headline"])}"><div><div class="ln-c">{"".join(rows)}'
            f'<a class="go" href="{link(s["id"])}">The full story, {minutes(s)} min <svg class="ic" aria-hidden="true"><use href="#i-right"/></svg></a></div></div></div></li>')


def deep_list(s):
    """Static, no buttons: the layers as tinted lines (feature block on home)."""
    out = []
    for k, label, d in LAYERS:
        v = s['layers'].get(k)
        if not v:
            continue
        if k == 'numbers':
            t = f'<b class="num" style="font-size:1.25rem;margin-right:6px">{esc(v[0]["figure"])}</b>{esc(v[0]["label"])}'
        elif k == 'voices':
            t = f'“{esc(v[0]["quote"])}” <span class="src">{esc(v[0]["who"])}</span>'
        else:
            t = esc(v['text'])
        out.append(f'<li data-d="{d}"><span class="lbl">{label}</span><span>{t}</span></li>')
    return '<ul class="deep">' + ''.join(out) + '</ul>'
