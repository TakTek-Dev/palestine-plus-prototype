"""Compose tools/edition.json and tools/photos.json from the research.

python -I tools/edition.py
Reads research/news.json (sourced items), research/photos.json (Commons candidates) and
tools/picks.json (hand choices: lead, feature, which photo goes with which story, items to
drop). Only photos a story actually uses are copied to tools/photos.json.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: json.load(open(os.path.join(ROOT, p), encoding='utf-8'))
news, cand, picks = rd('research/news.json'), rd('research/photos.json')['photos'], rd('tools/picks.json')

drop = set(picks.get('drop', []))
stories = []
for it in news['items']:
    if it['id'] in drop:
        continue
    s = {k: it.get(k) for k in ('id', 'desk', 'explainer', 'date', 'time', 'place', 'region', 'headline', 'fact',
                                 'standfirst', 'body', 'layers', 'sources')}
    s['explainer'] = bool(s['explainer'])
    s['layers'] = {k: v for k, v in (s['layers'] or {}).items() if v}
    for k in ('numbers', 'voices'):
        if k in s['layers'] and isinstance(s['layers'][k], dict):
            s['layers'][k] = [s['layers'][k]]
    for k, v in picks.get('edit', {}).get(it['id'], {}).items():
        s[k] = v
    ph = picks['photo'].get(it['id'])
    if ph:
        if ph not in cand:
            raise SystemExit(f'{it["id"]}: no candidate photo {ph}')
        s['photo'] = ph
    stories.append(s)

used = {s['photo'] for s in stories if s.get('photo')}
photos = {}
for k in sorted(used):
    c = cand[k]
    photos[k] = {f: c[f] for f in ('file', 'page_url', 'author', 'license', 'date', 'alt', 'caption')}
    if picks.get('focus', {}).get(k):
        photos[k]['focus'] = picks['focus'][k]

ahead = []
for a in news.get('dates_ahead', []):
    a = dict(a)
    if len(a['date']) == 7:           # month only: sort at the month's start, print as the month
        a['date'], a['approx'] = a['date'] + '-01', True
    ahead.append(a)

ids = {s['id'] for s in stories}
for k in ('lead', 'feature'):
    assert picks[k] in ids, (k, picks[k])
edition = {
    'date': picks['date'], 'updated': picks['updated'], 'lead': picks['lead'], 'feature': picks['feature'],
    'stories': stories, 'figures': news.get('figures', []), 'ahead': ahead,
}
json.dump(edition, open(os.path.join(ROOT, 'tools', 'edition.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(photos, open(os.path.join(ROOT, 'tools', 'photos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(stories), 'stories,', len(photos), 'photos,', sum(1 for s in stories if s.get('photo')), 'with a photo')
