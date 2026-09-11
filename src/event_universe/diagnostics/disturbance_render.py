"""Optional data-only inspection for arbitrary disturbance names and values."""

import html
import json
from pathlib import Path


def render_disturbances(
    frames: list[dict[str, object]], output: Path, metadata: dict[str, object]
) -> Path:
    data = json.dumps(frames).replace("<", "\\u003c")
    title = html.escape(str(metadata["model"]))
    document = """<!doctype html><html lang="en"><meta charset="utf-8">
<title>Disturbance simulation</title><style>
body{font:16px system-ui;margin:2rem;background:#101827;color:#e6edf3}
table{border-collapse:collapse;width:100%}td,th{text-align:left;border-bottom:1px solid #334155;padding:.6rem}
input{width:70%}pre{white-space:pre-wrap}small{color:#aab8cc}
</style><h1>__TITLE__</h1><p><input id="seek" type="range" min="0" value="0"><b id="tick"></b></p>
<small>Read-only sampled state. Positions are lattice addresses. Waiting values remain cell-owned.</small>
<h2>Local disturbances</h2><table><thead><tr><th>Position</th><th>Type</th><th>Fields</th><th>Local timing</th></tr></thead><tbody id="cells"></tbody></table>
<h2>Transfers in links</h2><pre id="links"></pre>
<script>const frames=__DATA__;const seek=document.querySelector('#seek');seek.max=frames.length-1;
function draw(){const f=frames[Number(seek.value)];document.querySelector('#tick').textContent='Tick '+f.tick;
const body=document.querySelector('#cells');body.replaceChildren();
for(const c of f.cells)for(const d of c.disturbances){const row=document.createElement('tr');
const timing=c.waiting_until===null?'next cycle '+c.available_tick:'waiting until '+c.waiting_until;
for(const value of [c.position.join(', '),d.type,JSON.stringify(d.values),'Cost '+c.cost+'; '+timing]){
const td=document.createElement('td');td.textContent=value;row.append(td)}body.append(row)}
document.querySelector('#links').textContent=JSON.stringify(f.transfers,null,2)}seek.oninput=draw;draw();</script></html>"""
    output.write_text(document.replace("__TITLE__", title).replace("__DATA__", data), encoding="utf-8")
    return output
