"""tools/out/og.html: the 1200x630 sharing card (wordmark and the lead's line on the left, its photo right).

python -I tools/og.py
node --experimental-websocket tools/shot.mjs http://localhost:8303/tools/out/og.html assets/og.png 1200 630 view
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # python -I drops the script dir

import shell as sh
from shell import C, E, BY, esc, long_day, depth, pl

lead = BY[E['lead']]
C.R = '../../'
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>og</title>
<link rel="stylesheet" href="../../assets/css/pp.css?v={sh.V}">
<style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:var(--paper)}}
.og{{display:grid;grid-template-columns:660px 540px;height:630px}}
.l{{padding:50px 52px 44px;display:flex;flex-direction:column}}
.l .brand svg{{width:400px;height:auto}}
.l h1{{margin-top:auto;font:640 46px/1.04 var(--serif);font-variation-settings:"opsz" 72;letter-spacing:-.02em;text-wrap:balance}}
.l .f{{margin-top:22px;display:flex;align-items:center;gap:14px;font:700 17px var(--sans);color:var(--mute)}}
.l .f .pl{{--s:18px}}
.l .f b{{color:var(--plus-t)}}
.r{{position:relative;background:var(--l2)}}
.r img{{width:100%;height:100%;object-fit:cover}}
.ramp{{position:absolute;left:0;right:0;bottom:0;display:grid;grid-template-rows:repeat(4,12px)}}
.ramp i:nth-child(1){{background:var(--l1)}}.ramp i:nth-child(2){{background:var(--l2)}}.ramp i:nth-child(3){{background:var(--l3)}}.ramp i:nth-child(4){{background:var(--ink)}}
</style></head><body><div class="og"><div class="l"><div class="brand">{sh.wordmark()}</div>
<h1>{esc(lead["headline"])}</h1><p class="f">{pl()}<span><b>{depth(lead)} layers</b> under this line · {esc(long_day(E["date"]))}</span></p></div>
<div class="r">{f'<img src="../../assets/img/photo/{lead["photo"]}.webp" alt="">' if lead.get("photo") else ''}<div class="ramp"><i></i><i></i><i></i><i></i></div></div></div></body></html>'''
sh.write('tools/out/og.html', html)
print('tools/out/og.html')
