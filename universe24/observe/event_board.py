"""Passive physical-event decoder and self-contained board from retained state.

No function in this module advances, projects or supplies inputs to the Engine.
Physical snapshots have a declared coordinate chart and a register provenance.
Official integer clicks are exported separately by the runtime.
"""
from fractions import Fraction
import json
import math
from pathlib import Path


def encoded(value):
    return {'numerator_hex': format(value.numerator, 'x'),
            'denominator_hex': format(value.denominator, 'x')}


def export_event_board(program, state, parameters, out):
    out = Path(out)
    fields = parameters['fields']
    dt, dx = Fraction(parameters['dt']), Fraction(parameters['dx'])
    frames, provenance, charges = [], {}, []
    complex_matter = parameters.get('complex_matter', False)
    for step in range(parameters['steps'] + 1):
        outputs = {name: program.outputs[f'{step}.{name}'] for name in fields}
        ready = max((program.ready[t.wire] for value in outputs.values()
                     for t in (value.num, value.den) if t.wire is not None), default=0)
        provenance[str(step)] = {}
        for name, expression in outputs.items():
            provenance[str(step)][name] = {
                part: {'coefficient_hex': format(term.coefficient, 'x'),
                       'register': None if term.wire is None else program.names[term.wire],
                       'ready_microtick': 0 if term.wire is None else program.ready[term.wire]}
                for part, term in (('numerator', expression.num), ('denominator', expression.den))}
        events, exact = [], []
        total_charge, max_charge_defect = 0.0, 0.0
        for node in range(state.L ** 3):
            read = lambda suffix: program.read(state, f'{step}.{suffix}', node)
            values = {name: read(name) for name in fields}
            metric = [[read(f'metric.{min(i,j)}{max(i,j)}') for j in range(4)] for i in range(4)]
            stress = [[read(f'stress.{min(i,j)}{max(i,j)}') for j in range(4)] for i in range(4)]
            energy = {name: read(f'source.{name}') for name in ('rho', 'rho_scalar', 'rho_dark')}
            charge = read('matter.charge') if complex_matter else Fraction(0)
            current = [read(f'matter.current{i}') for i in range(4)] if complex_matter else [Fraction(0)] * 4
            if complex_matter:
                total_charge += float(charge) * math.sqrt(float(read('det_gamma'))) * float(dx) ** 3
                max_charge_defect = max(max_charge_defect, abs(float(read('matter.charge_spatial_defect'))))
            coordinates = list(state.lattice.coords(node))
            event_id = f'{step}:{node}'
            events.append({'id': event_id, 'node': node, 'grid': coordinates,
                           'coordinates': [float(step * dt)] + [float(v * dx) for v in coordinates],
                           'fields': {k: float(v) for k, v in values.items()},
                           'metric': [[float(v) for v in row] for row in metric],
                           'stress': [[float(v) for v in row] for row in stress],
                           'energy': {k: float(v) for k, v in energy.items()},
                           'charge': float(charge), 'current': list(map(float, current)),
                           'constraints': {k: float(read(f'constraint.{k}')) for k in ('H', 'M0', 'M1', 'M2')}})
            exact.append({'id': event_id, 'metric': [[encoded(v) for v in row] for row in metric],
                          'stress': [[encoded(v) for v in row] for row in stress],
                          'energy': {k: encoded(v) for k, v in energy.items()},
                          'charge': encoded(charge), 'current': list(map(encoded, current))})
        import gzip
        with gzip.open(out / f'event_tensors_{step}.json.gz', 'wt') as file:
            json.dump(exact, file, separators=(',', ':'))
        charges.append({'step': step, 'coordinate_volume_weighted_charge': total_charge,
                        'max_spatial_charge_balance_defect': max_charge_defect})
        frames.append({'step': step, 'time': str(step * dt), 'ready_microtick': ready, 'events': events})
    payload = {'format': 'Universe24-event-board-v1', 'L': state.L, 'dt': str(dt), 'dx': str(dx),
               'tensor_fingerprint': program.tensor.fingerprint, 'frames': frames,
               'charge_diagnostics': charges, 'provenance': provenance,
               'meaning': 'Metric, matter and stress decoded from one retained Engine state; physical snapshots use a declared coordinate chart.',
               'limits': 'Classical complex scalar and single-stream dark dust. No quantum particle count, electromagnetic interaction or annihilation model. Finite compiled horizon and numerical constraint errors.'}
    if hasattr(program,'assembly'):
        payload['channel_allocation']=program.assembly.manifest(include_channels=False)
        payload['channel_allocation']['physical_fields_per_event']=len(fields)
        payload['channel_allocation']['property_groups']=program.channel_manifest(include_channels=False)['property_groups']
    (out / 'event_board.json').write_text(json.dumps(payload, indent=2) + '\n')
    (out / 'board.html').write_text(HTML.replace('__PAYLOAD__', json.dumps(payload, separators=(',', ':')).replace('<', '\\u003c')))
    return {'file': 'board.html', 'data': 'event_board.json', 'physical_events': sum(len(f['events']) for f in frames),
            'official_clicks': 'official_events.jsonl.gz', 'register_provenance': 'event_board.json',
            'charge_diagnostics': charges,
            'charge_note': 'Volume-weighted charge uses floating-point quadrature of sqrt(det gamma); drift and spatial balance defects are numerical diagnostics.'}


HTML = r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Universe24 · Einstein event board</title>
<style>
:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#091018;color:#e3edf5}*{box-sizing:border-box}
body{max-width:1420px;margin:auto;padding:28px}h1{font-size:29px;letter-spacing:-1px;margin:0 0 8px}h2{font-size:16px;margin-top:0}
p{color:#a3b6c6;line-height:1.6}header{border-bottom:1px solid #263441;padding-bottom:18px;margin-bottom:22px}
.tag{font:12px monospace;color:#82ddd1;letter-spacing:2px}.grid{display:grid;grid-template-columns:1.3fr 1fr;gap:18px}
.card{background:#101d28;border:1px solid #273a48;border-radius:12px;padding:20px;min-width:0}.controls{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin:20px 0}
label{font-size:13px;color:#b9cbd9}select,button{background:#1d3342;color:#eef8ff;border:1px solid #476477;border-radius:6px;padding:9px}input{accent-color:#7eddd0}
canvas{display:block;width:100%;aspect-ratio:1.2;touch-action:none}.stats{display:flex;gap:24px;flex-wrap:wrap;font:13px monospace;margin:16px 0}.stats strong{display:block;font-size:19px;color:#e8f6ff;margin-top:6px}
.caption{font-size:12px;color:#9db2c3}.key{display:flex;justify-content:space-between;background:linear-gradient(90deg,#3586c6,#162736,#ed9951);padding:6px 10px;border-radius:5px;font:11px monospace}
pre{font:12px/1.5 monospace;overflow:auto;background:#0a141c;padding:12px;border-radius:6px;max-height:230px}table{width:100%;border-collapse:collapse;font:12px monospace}td,th{padding:6px;border-bottom:1px solid #233544;text-align:right}
details{margin-top:15px}summary{cursor:pointer;color:#8edbd1}.limit{border-left:3px solid #d8a455;padding-left:14px;font-size:13px;margin:22px 0}
@media(max-width:850px){.grid{grid-template-columns:1fr}body{padding:16px}}
</style>
<header><div class="tag">UNIVERSE24 / INTEGER RULE3</div><h1>Einstein event board</h1><p>Geometry, matter, antimatter charge and dark matter from the same evolving state.</p></header>
<div class="controls"><label>Physical step <input id="time" type="range" min="0" value="0"><span id="timeLabel"></span></label>
<label>z slice <select id="slice"></select></label><label>Color <select id="field"><option value="charge">Signed scalar charge</option><option value="rho_dark">Dark density</option><option value="rho">Total energy density</option><option value="g00">Spatial metric γxx</option><option value="H">Hamiltonian residual</option></select></label></div>
<div class="grid"><section class="card"><div class="stats"><span>COORDINATE TIME<strong id="clock"></strong></span><span>READY MICROTICK<strong id="tick"></strong></span><span>BOARD EVENTS<strong id="events"></strong></span></div><canvas id="board" width="780" height="650" aria-label="Event board slice"></canvas><div class="key"><span id="min"></span><span id="max"></span></div><p class="caption">Click a node to inspect its metric and source. Lines are shared spatial links; their lengths are computed from the metric, not this diagram's pixel spacing.</p></section>
<section class="card"><h2 id="nodeTitle">Event</h2><table id="values"></table><details open><summary>Spacetime metric gμν</summary><pre id="metric"></pre></details><details><summary>Independent source Tμν</summary><pre id="stress"></pre></details><details><summary>Einstein constraints</summary><pre id="constraints"></pre></details><details><summary>Retained register provenance</summary><pre id="registers"></pre></details></section></div>
<section class="card" style="margin-top:18px"><h2>Channel ownership</h2><p id="channelSummary"></p><table id="channels"></table><p class="caption">Each owner has a disjoint retained range. Communication and experimental probes are computational controls; they do not add a second metric or stress source to this physical board. Full allocation: channels.json.</p></section>
<p class="limit" id="limit"></p><p class="caption" id="fingerprint"></p>
<script type="application/json" id="data">__PAYLOAD__</script>
<script>
const data=JSON.parse(document.getElementById('data').textContent),$=id=>document.getElementById(id),ctx=$('board').getContext('2d');let selected=0,points=[];
$('time').max=data.frames.length-1;for(let z=0;z<data.L;z++)$('slice').add(new Option(z,z));$('limit').textContent=data.limits;
$('fingerprint').textContent='Fixed tensor '+data.tensor_fingerprint+' · Exact arrays: physical_N.json.gz / event_tensors_N.json.gz';
if(data.channel_allocation){const a=data.channel_allocation;$('channelSummary').textContent=`${a.physical_fields_per_event} physical fields · ${a.total_channels} channels per node · ${a.integer_registers_per_node} retained integers (a, b, r)`;for(const c of a.components){const row=$('channels').insertRow();for(const v of [c.owner,`${c.start}–${c.stop-1}`,c.channels,c.purpose])row.insertCell().textContent=v}}else{$('channelSummary').textContent='Standalone Einstein component; register provenance is shown per physical field.'}
const number=x=>Number(x).toPrecision(6),matrix=a=>a.map(row=>row.map(x=>number(x).padStart(13)).join(' ')).join('\n');
function value(e){let key=$('field').value;return key==='charge'?e.charge:key==='H'?e.constraints.H:key==='g00'?e.fields.g00:e.energy[key]}
function render(){const frame=data.frames[+$('time').value],z=+$('slice').value,events=frame.events.filter(e=>e.grid[2]===z),vals=events.map(value),lo=Math.min(...vals),hi=Math.max(...vals),span=Math.max(Math.abs(lo),Math.abs(hi),1e-30);$('clock').textContent=frame.time;$('tick').textContent=frame.ready_microtick;$('events').textContent=data.L**3;$('timeLabel').textContent=' '+frame.step;$('min').textContent=number(lo);$('max').textContent=number(hi);
ctx.clearRect(0,0,780,650);points=events.map(e=>({e,x:85+e.grid[0]*610/Math.max(data.L-1,1),y:560-e.grid[1]*470/Math.max(data.L-1,1)}));ctx.strokeStyle='#344e60';ctx.lineWidth=2;
for(const p of points)for(const q of points)if(Math.abs(p.e.grid[0]-q.e.grid[0])+Math.abs(p.e.grid[1]-q.e.grid[1])===1){ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke()}
for(const p of points){const v=value(p.e),t=($('field').value==='charge'||$('field').value==='H')?v/span:2*(v-lo)/(hi-lo||1)-1;ctx.beginPath();ctx.fillStyle=t<0?`hsl(205 65% ${25+35*Math.abs(t)}%)`:`hsl(29 80% ${25+35*t}%)`;ctx.arc(p.x,p.y,Math.min(32,160/data.L),0,Math.PI*2);ctx.fill();if(p.e.node===selected){ctx.strokeStyle='#fff';ctx.lineWidth=3;ctx.stroke();ctx.strokeStyle='#344e60'}ctx.fillStyle='#dae9f5';ctx.font='13px monospace';ctx.textAlign='center';ctx.fillText(p.e.id,p.x,p.y+47)}
if(!events.some(e=>e.node===selected))selected=events[0].node;const e=frame.events.find(e=>e.node===selected);$('nodeTitle').textContent=`Event ${e.id} · (${e.grid.join(', ')})`;
$('values').replaceChildren();for(const [k,v]of Object.entries({...e.energy,charge:e.charge,phi:e.fields.phi,chi:e.fields.chi??0})){const row=$('values').insertRow();row.insertCell().textContent=k;row.insertCell().textContent=number(v)}
$('metric').textContent=matrix(e.metric);$('stress').textContent=matrix(e.stress);$('constraints').textContent=JSON.stringify(e.constraints,null,2);$('registers').textContent=JSON.stringify(data.provenance[frame.step],null,2)}
for(const id of ['time','slice','field'])$(id).addEventListener('input',render);$('board').addEventListener('click',ev=>{const r=$('board').getBoundingClientRect(),x=(ev.clientX-r.left)*780/r.width,y=(ev.clientY-r.top)*650/r.height;let p=points.reduce((a,b)=>Math.hypot(a.x-x,a.y-y)<Math.hypot(b.x-x,b.y-y)?a:b);selected=p.e.node;render()});render();
</script></html>'''
