"""Render saved 44-channel diagnostics; no Engine updates or reference solver.

python -m validation.team48_board --observables runs/observables.json \
    --out runs/one-system-board.html
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from universe24.core import exact_json


HTML = r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Universe24 · one recorded system</title>
<style>
:root{color-scheme:dark;--bg:#0b1119;--panel:#121d29;--line:#293747;--text:#e6edf4;--muted:#93a8bc;--accent:#80ddc8;--amber:#f2bf72}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 system-ui,-apple-system,sans-serif}main{max-width:1440px;padding:30px 28px 60px;margin:auto}header{display:flex;justify-content:space-between;align-items:flex-start;gap:24px}h1{font-weight:580;letter-spacing:-1px;font-size:32px;margin:4px 0 8px}h2{font-size:16px;margin:0 0 16px;font-weight:600}h3{font-size:12px;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin:20px 0 8px}p{margin:6px 0}.eyebrow{color:var(--accent);font-size:11px;letter-spacing:.16em;text-transform:uppercase}.subtle{color:var(--muted);font-size:12px}.status{border:1px solid #675036;color:var(--amber);background:#2a241c;border-radius:8px;padding:12px 16px;margin:22px 0}.status strong{font-weight:580}.chips{display:flex;gap:8px;flex-wrap:wrap}.chip{border:1px solid var(--line);border-radius:6px;padding:5px 9px;font-size:12px;color:var(--muted)}.chip strong{color:var(--text);font-weight:600}.layout{display:grid;grid-template-columns:minmax(350px,.9fr) minmax(420px,1.3fr);gap:18px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px;min-width:0}.controls{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:18px}.control{display:flex;gap:8px;align-items:center;font-size:12px;color:var(--muted)}select,button{font:inherit}select{color:var(--text);background:#0e1721;border:1px solid var(--line);padding:7px;border-radius:6px}input[type=range]{accent-color:var(--accent);width:180px}#stepLabel{min-width:25px;color:var(--text);font-variant-numeric:tabular-nums}.grid{display:grid;gap:8px;margin:18px 0}.node{min-width:0;min-height:105px;color:var(--text);border:1px solid #526377;background:#1c3447;border-radius:8px;padding:12px 8px;text-align:left;cursor:pointer;overflow:hidden}.node:hover{filter:brightness(1.2)}.node.selected{outline:2px solid var(--accent);outline-offset:2px}.node .coord{display:block;color:#d2e1ee;font-size:11px;margin-bottom:8px}.node .value{display:block;font-family:ui-monospace,monospace;font-size:13px;overflow-wrap:anywhere}.legend{display:flex;justify-content:space-between;gap:12px;font-size:11px;color:var(--muted)}.legend i{display:inline-block;width:44px;height:6px;background:linear-gradient(90deg,#263a53,#6a4c55,#bc724f);margin-right:5px}.stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:16px}.stat{border:1px solid var(--line);border-radius:8px;padding:12px}.stat label{display:block;color:var(--muted);font-size:11px;margin-bottom:6px}.exact{font-family:ui-monospace,SFMono-Regular,monospace;overflow-wrap:anywhere;font-size:12px}.large{font-size:18px;font-variant-numeric:tabular-nums}.matrix{border-collapse:collapse;table-layout:fixed;width:100%;font-family:ui-monospace,monospace;font-size:12px}.matrix td{border:1px solid var(--line);padding:9px;text-align:center;overflow-wrap:anywhere}.twocol{display:grid;grid-template-columns:1fr 1fr;gap:14px}.row{display:flex;gap:16px;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line)}.row span:first-child{color:var(--muted);font-size:12px}.row span:last-child{text-align:right;max-width:65%}.long{font-size:10px;overflow-wrap:anywhere}details{margin-top:18px}summary{cursor:pointer;color:var(--muted)}#provenance{padding:12px 0}.empty{color:var(--muted)}.dot{width:7px;height:7px;display:inline-block;border-radius:50%;background:var(--accent);margin-right:8px}.note{padding-top:14px;color:var(--muted);font-size:12px}.full{grid-column:1/-1}footer{padding-top:18px;color:var(--muted);font-size:11px}@media(max-width:950px){.layout{grid-template-columns:1fr}header{display:block}.chips{margin-top:14px}.full{grid-column:auto}}@media(max-width:520px){main{padding:20px 14px}.panel{padding:14px}.twocol{grid-template-columns:1fr}h1{font-size:27px}.node{min-height:92px}.controls{gap:10px}input[type=range]{width:130px}}
</style>
<main>
<header><div><div class="eyebrow">Universe24 / saved-state diagnostics</div><h1>One recorded system</h1><p class="subtle">Geometry, matter, energy and opposite charge from the same retained state.</p></div><div class="chips"><span class="chip"><strong id="channels">44</strong> channels / node</span><span class="chip">one immutable tensor</span><span class="chip">exact integer replay</span></div></header>
<div class="status"><strong>Diagnostic readout · Einstein constraints and refinement are not established.</strong><br><span class="subtle">This view does not certify physical clocks, quantum particles or a Born/Bell law. Charge signs denote classical charge-conjugate sectors.</span></div>
<div class="layout">
<section class="panel"><h2>Event-board slice</h2><div class="controls"><label class="control">Update <input id="step" type="range" min="0" value="0"><span id="stepLabel"></span></label><label class="control">z <select id="slice"></select></label><label class="control">Color <select id="color"><option value="energy">Energy density</option><option value="charge">Signed U(1) charge</option><option value="constraint">Hamiltonian defect</option></select></label></div><p class="subtle">Computational updates, not proper time. Select a node to inspect exact values.</p><div id="grid" class="grid" aria-label="Spatial node selection"></div><div class="legend"><span><i></i>relative diagnostic magnitude</span><span id="colorLabel">exact values on cells</span></div><p class="note">The square layout shows node addresses. Pixel spacing and cell shape do not represent physical distances or angles.</p><div id="frameSummary"></div></section>
<section class="panel"><h2 id="nodeTitle">Node</h2><div class="stats"><div class="stat"><label>Total energy density</label><div class="exact large" id="totalEnergy"></div></div><div class="stat"><label>Signed U(1) charge density</label><div class="exact large" id="charge"></div><span id="chargeSector" class="subtle"></span></div></div><div id="energies"></div><div class="twocol"><div><h3>Metric γ</h3><div id="metric"></div></div><div><h3>Inverse metric γ⁻¹</h3><div id="inverseMetric"></div></div></div><h3>Momentum & stress · orthonormal frame</h3><div id="momentum"></div><div id="stress"></div></section>
<section class="panel"><h2>Links and local angles</h2><p class="subtle">Exact values from this node's metric; angle data is retained as inner products, without rounded arccos.</p><div id="links"></div><h3>Angle inner products</h3><div id="angles"></div></section>
<section class="panel"><h2>Constraint diagnostics</h2><p class="subtle">H uses the retained frame connection; it is not an independent reconstruction of metric curvature. Nonzero defects are shown without projection or repair.</p><div id="constraints"></div></section>
<section class="panel full"><h2><span class="dot"></span>Same run, same tensor, passive readout</h2><p class="subtle">Every panel is computed from saved snapshots of one run. This page contains no evolution law or alternate simulator.</p><details><summary>Source identity and exact-value format</summary><div id="provenance"></div><p class="subtle">All exact integers and rational numerators/denominators are displayed as decimal strings. Only cell colors use an approximate scale.</p></details></section>
</div><footer>Universe24 · one-system research record. Open physical acceptance gates remain visible.</footer>
</main>
<script id="data" type="application/json">__PAYLOAD__</script>
<script>
'use strict';
const D=JSON.parse(document.getElementById('data').textContent),$=id=>document.getElementById(id);
// ADAPTER
const frames=D.snapshots.map(f=>({step:f.step,nodes:f.nodes.map(n=>({node:n.node,coordinates:n.xyz,
geometry:{gamma:n.geometry.gamma,gamma_inverse:n.geometry.gamma_inv,
link_squared_lengths:Object.fromEntries(['+x','+y','+z'].map((a,i)=>[a,n.geometry.face_link_squared_lengths?.[i]??null])),
angle_inner_products:Object.fromEntries(['01','02','12'].map(k=>[k,{inner_product:n.geometry.gamma?.[Number(k[0])]?.[Number(k[1])]??null,cosine_squared:n.geometry.face_angle_cosine_squared?.[k]??null,cosine_sign:n.geometry.face_angle_cosine_sign?.[k]??null}]))},
matter:{total_energy:n.matter.rho_total,u1_charge:n.matter.electric_charge,scalar_energy:n.matter.rho_scalar,dust_energy:n.matter.rho_dust,em_energy:n.matter.rho_maxwell,momentum:n.matter.momentum_frame,stress:n.matter.stress_frame},
constraints:{hamiltonian:n.constraints.H,...Object.fromEntries(Object.entries(n.constraints).filter(([k])=>k!=='H').map(([k,v])=>[/^C[0-9]+$/.test(k)?'torsion '+k:k,v]))}}))})), L=Number(D.L), ids={run_id:D.run_id,bundle_id:D.bundle_id,tensor_hash:D.tensor_hash,source_commit:D.source_commit,units:D.units};
let selected=0;
function exact(v){if(v===null||v===undefined)return 'not available';if(Array.isArray(v))return '['+v.map(exact).join(', ')+']';if(typeof v==='object'){let n=v.numerator??v.num??v.n, d=v.denominator??v.den??v.d;if(n!==undefined&&d!==undefined)return String(d)==='1'?String(n):String(n)+' / '+String(d);return Object.entries(v).map(([k,x])=>k+': '+exact(x)).join(' · ')}return String(v)}
function sign(v){const s=exact(v).trim();if(s==='0'||s.startsWith('0 /'))return 0;return s.startsWith('-')?-1:1}
function magnitude(v){const s=exact(v),parts=s.split('/');function lg(t){const a=t.trim().replace(/^[-+]/,'').replace(/^0+/,'');if(!a)return -100;return a.length-1+Math.log10(Number(a.slice(0,12))/10**(Math.min(a.length,12)-1))}return lg(parts[0])-(parts.length>1?lg(parts[1]):0)}
function clear(id){$(id).replaceChildren();return $(id)}
function row(parent,label,value){const el=document.createElement('div');el.className='row';const a=document.createElement('span'),b=document.createElement('span');a.textContent=label;b.textContent=exact(value);b.className='exact';el.append(a,b);parent.append(el)}
function matrix(id,value){const parent=clear(id);if(!Array.isArray(value)||!Array.isArray(value[0])){parent.textContent=exact(value);parent.classList.add('exact');return}const table=document.createElement('table');table.className='matrix';value.forEach(values=>{const tr=document.createElement('tr');values.forEach(v=>{const td=document.createElement('td');td.textContent=exact(v);tr.append(td)});table.append(tr)});parent.append(table)}
function entries(id,value){const el=clear(id);if(Array.isArray(value))value.forEach((v,i)=>row(el,String(i),v));else if(value&&typeof value==='object')Object.entries(value).forEach(([k,v])=>row(el,k.replaceAll('_',' '),v));else el.textContent=exact(value)}
function nodeCoords(n){return n.coordinates??[Number(n.node)%L,Math.floor(Number(n.node)/L)%L,Math.floor(Number(n.node)/(L*L))]}
function colorValue(n){return $('color').value==='charge'?n.matter.u1_charge:$('color').value==='constraint'?n.constraints.hamiltonian:n.matter.total_energy}
function render(){const frame=frames[Number($('step').value)];$('stepLabel').textContent=String(frame.step);const z=Number($('slice').value),nodes=frame.nodes.filter(n=>Number(nodeCoords(n)[2])===z).sort((a,b)=>{const ca=nodeCoords(a),cb=nodeCoords(b);return Number(ca[1])-Number(cb[1])||Number(ca[0])-Number(cb[0])});if(!nodes.some(n=>Number(n.node)===selected))selected=Number(nodes[0]?.node??0);const grid=clear('grid');grid.style.gridTemplateColumns=`repeat(${L},minmax(0,1fr))`;const mags=nodes.map(n=>magnitude(colorValue(n))).filter(Number.isFinite);const max=Math.max(...mags),min=Math.min(...mags);nodes.forEach(n=>{const value=colorValue(n),button=document.createElement('button');button.type='button';button.className='node'+(Number(n.node)===selected?' selected':'');button.setAttribute('aria-pressed',String(Number(n.node)===selected));button.setAttribute('aria-label','Node '+nodeCoords(n).join(', '));const coord=document.createElement('span'),val=document.createElement('span');coord.className='coord';coord.textContent='('+nodeCoords(n).join(', ')+')';val.className='value';val.textContent=exact(value);button.append(coord,val);const intensity=max===min?.4:Math.max(0,Math.min(1,(magnitude(value)-min)/(max-min)));button.style.background=sign(value)<0?`hsl(208 35% ${20+intensity*22}%)`:`hsl(${28-intensity*14} ${15+intensity*25}% ${18+intensity*19}%)`;button.onclick=()=>{selected=Number(n.node);render()};grid.append(button)});const n=frame.nodes.find(n=>Number(n.node)===selected);if(!n)return;$('nodeTitle').textContent='Node ('+nodeCoords(n).join(', ')+') · update '+frame.step;$('totalEnergy').textContent=exact(n.matter.total_energy);$('charge').textContent=exact(n.matter.u1_charge);$('chargeSector').textContent=sign(n.matter.u1_charge)===0?'zero classical charge':sign(n.matter.u1_charge)<0?'negative classical charge sector':'positive classical charge sector';const e=clear('energies');row(e,'Scalar energy',n.matter.scalar_energy);row(e,'Dust energy',n.matter.dust_energy);row(e,'Electromagnetic energy',n.matter.em_energy);matrix('metric',n.geometry.gamma);matrix('inverseMetric',n.geometry.gamma_inverse);const m=clear('momentum');row(m,'Momentum density',n.matter.momentum);matrix('stress',n.matter.stress);entries('links',n.geometry.link_squared_lengths);entries('angles',n.geometry.angle_inner_products);entries('constraints',n.constraints);entries('frameSummary',frame.summary??{});}
$('channels').textContent=exact(D.channels_per_node??44);$('step').max=String(frames.length-1);for(let z=0;z<L;z++){const option=document.createElement('option');option.value=String(z);option.textContent=String(z);$('slice').append(option)}for(const id of ['step','slice','color'])$(id).addEventListener('input',render);Object.entries(ids).forEach(([k,v])=>row($('provenance'),k.replaceAll('_',' '),v));render();
</script></html>'''


def _stringify_integers(value):
    """Prevent JSON.parse from silently rounding retained integers in the page."""
    if type(value) is int:
        return exact_json.dumps(value)
    if isinstance(value, list):
        return [_stringify_integers(v) for v in value]
    if isinstance(value, dict):
        return {k: _stringify_integers(v) for k, v in value.items()}
    return value


def render(observables: dict, out: str | Path) -> Path:
    if observables.get('schema') != 'universe24/validation/team48-observables/1':
        raise ValueError('unsupported observables schema')
    if not isinstance(observables.get('snapshots'), list) or not observables['snapshots']:
        raise ValueError('observables require saved snapshots')
    payload = json.dumps(_stringify_integers(observables), ensure_ascii=True, separators=(',', ':'))
    # Never allow data strings to terminate the inert JSON script element.
    payload = payload.replace('<', r'\u003c').replace('>', r'\u003e').replace('&', r'\u0026')
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HTML.replace('__PAYLOAD__', payload), encoding='utf-8')
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--observables', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args(argv)
    report = exact_json.loads(args.observables.read_text(encoding='utf-8'))
    output = render(report, args.out)
    print(json.dumps({'board': str(output), 'run_id': report.get('run_id')}))


if __name__ == '__main__':
    main()
