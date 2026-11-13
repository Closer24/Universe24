"""Passive, self-contained replay board reconstructed from arithmetic clicks.

The initial sealed bundle is explicitly disclosed as public calibration. This
module never opens the full transition trace or advances Engine. It validates
the initial public history against the inverse gate oracle; subsequent frames
come only from clicks. Browser controls select recorded frames and do not
evolve another universe. A checksum is not proof of stream completeness.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from .core import State, exact_json
from .observer import read_clicks, _reconstruct_channel_records
from .system.bundle import load_bundle, read_json, canonical_bytes

BOARD_SCHEMA = 'universe24/click-board/1'


def _sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def board_data(run_dir):
    """Read initial calibration plus clicks and return passive display frames.

    The saved report supplies the declared complete horizon. Its identifiers
    and click checksum are checked, but no hidden trace replay is performed.
    Initial public calibration must belong to the forward Boolean sector.
    Its inverse-oracle check does not generate any subsequent displayed frame.
    Actual stream completeness must be established separately with ``verify``.
    """
    from .load import face_load_profile, integer_work_profile
    from .model import coupling_tensor, decode_occupation, sector_map

    directory = Path(run_dir)
    report = read_json(directory / 'validation.json')
    if not isinstance(report, dict) or report.get('schema') != 'universe24/system/run/1':
        raise ValueError('unsupported run report for board')
    steps = report.get('steps')
    if type(steps) is not int or steps < 0:
        raise ValueError('board horizon must be an exact nonnegative integer')
    bundle = load_bundle(directory / 'bundle')
    if bundle.tensor.fingerprint != coupling_tensor().fingerprint:
        raise ValueError('board requires the calibrated capacity-scatter coupling')
    seed = bundle.seed
    decode_occupation(seed.a, seed.L)
    decode_occupation(seed.b, seed.L)
    if np.any((seed.r < 1) | (seed.r > 5)):
        raise ValueError('board calibration requires positive carries in 1..5')
    if not np.array_equal(seed.a, sector_map(seed.b, seed.L, inverse=True)):
        raise ValueError('board calibration is outside the forward Boolean history sector')
    expected_run = hashlib.sha256(canonical_bytes({
        'schema': 'universe24/system/run/1', 'bundle_id': bundle.bundle_id,
        'steps': steps})).hexdigest()
    if (report.get('bundle_id') != bundle.bundle_id or
            report.get('tensor_hash') != bundle.tensor.fingerprint or
            report.get('run_id') != expected_run or report.get('nodes') != seed.N):
        raise ValueError('board run and public calibration do not match')
    click_path = directory / 'clicks.jsonl.gz'
    click_hash = _sha(click_path)
    files = report.get('files')
    if not isinstance(files, dict) or files.get('clicks.jsonl.gz') != click_hash:
        raise ValueError('board click checksum mismatch')
    records = read_clicks(click_path)
    if any(event['run_id'] != expected_run for event in records):
        raise ValueError('board click provenance does not match calibration')
    if report.get('click_count') != len(records):
        raise ValueError('board click count does not match saved report')
    channels = []
    for channel in range(48):
        channels.append(_reconstruct_channel_records(
            records, channel=channel, node_count=seed.N, steps=steps,
            initial_a=list(map(int, seed.a[channel])),
            initial_b=list(map(int, seed.b[channel])))['values_by_step'])
    counts = [[0] * seed.N for _ in range(steps + 1)]
    for event in records:
        counts[event['step']][event['node']] += 1
    frames = []
    old, current = seed.a.copy(), seed.b.copy()
    for tick in range(steps + 1):
        if tick:
            old, current = current, np.asarray([
                [exact_json.loads(v) for v in channels[channel][tick - 1]]
                for channel in range(48)], dtype=object)
        # Constructing a calibrated snapshot is readout, not a state transition.
        snapshot = State(seed.L, old, current, seed.r.copy())
        profile = face_load_profile(current, seed.L)
        work = integer_work_profile(snapshot, bundle.tensor)
        frames.append({'step': tick, 'load': profile, 'work': work,
                       'clicks_by_node': counts[tick], 'clicks': sum(counts[tick])})
    return {
        'schema': BOARD_SCHEMA, 'run_id': expected_run, 'bundle_id': bundle.bundle_id,
        'tensor_hash': bundle.tensor.fingerprint, 'click_sha256': click_hash,
        'L': seed.L, 'nodes': seed.N, 'steps': steps, 'click_count': len(records),
        'model_id': bundle.model['id'], 'preparation': bundle.model,
        'calibration': 'Complete initial a,b,r are public calibration. Exact coupling, Boolean values, positive carries and the inverse-history sector are checked; no species labels are used.',
        'calibration_sector_verified': True,
        'initial_inverse_oracle_checked': True,
        'observation': 'Subsequent frames are reconstructed only from canonical arithmetic clicks and that calibration.',
        'integrity': 'Click checksum and provenance checked; full trace is not opened. Completeness requires separate verify.',
        'physics': {'light': 'Isolated vacuum transport only',
                    'ordinary_matter': 'Not established', 'dark_matter': 'Not established',
                    'einstein_geometry': 'Not established', 'gravitational_waves': 'Not established'},
        'frames': frames,
    }


def _script_json(value):
    """JSON in a script element must not be able to terminate that element."""
    return exact_json.dumps(value, separators=(',', ':'), ensure_ascii=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')


def build_board(run_dir, out_path):
    """Write a new standalone HTML board and return a concise creation report."""
    destination = Path(out_path)
    if destination.exists():
        raise ValueError('board output must be a new file')
    data = board_data(run_dir)
    html = _HTML.replace('__BOARD_DATA__', _script_json(data))
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x', encoding='utf-8') as stream:
        stream.write(html)
    return {'board': str(destination), 'schema': BOARD_SCHEMA, 'run_id': data['run_id'],
            'steps': data['steps'], 'nodes': data['nodes'], 'clicks': data['click_count'],
            'source': 'canonical clicks + explicitly disclosed and validated initial calibration',
            'calibration_sector_verified': True,
            'full_trace_opened': False, 'browser_evolution': False,
            'physics_acceptance': 'blocked'}


_HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Universe24 · Clock and load replay</title>
<style>
:root{color-scheme:dark;--bg:#08111d;--panel:#101d2d;--line:#263b50;--muted:#9fb2c5;--ink:#edf6ff;--blue:#57c7ff;--amber:#ffc16c;--mint:#8ce5b7}
*{box-sizing:border-box}body{margin:0;background:var(--bg);font:14px/1.5 system-ui,sans-serif;color:var(--ink)}button,input,select{font:inherit}button,select{background:#192b40;color:var(--ink);border:1px solid #36516a;border-radius:7px;padding:7px 11px}button{cursor:pointer}button:hover{background:#24425c}button:focus-visible,select:focus-visible,input:focus-visible{outline:2px solid var(--blue);outline-offset:3px}main{max-width:1460px;margin:auto;padding:30px 28px}header{display:flex;justify-content:space-between;gap:20px;align-items:center;margin-bottom:24px}.eyebrow{color:var(--mint);font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase}h1{font-size:30px;line-height:1.2;letter-spacing:-.8px;margin:7px 0}p{margin:7px 0}.muted{color:var(--muted)}.pill{display:inline-block;border:1px solid #395366;border-radius:99px;padding:5px 10px;font-size:12px;white-space:nowrap}.grid{display:grid;grid-template-columns:minmax(0,1.8fr) minmax(290px,1fr);gap:18px}.panel{border:1px solid var(--line);border-radius:13px;background:var(--panel);padding:19px}.controls{display:flex;flex-wrap:wrap;gap:13px;align-items:center}.controls label{display:flex;align-items:center;gap:8px;color:var(--muted)}input[type=range]{accent-color:var(--blue);min-width:140px}.timeline{display:flex;align-items:center;gap:14px;margin:18px 0 10px}.timeline input{flex:1}.step{font-variant-numeric:tabular-nums;font-weight:700;min-width:100px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:16px 0}.stat{border:1px solid var(--line);border-radius:9px;padding:11px}.stat strong{font-size:23px;display:block;font-variant-numeric:tabular-nums}.stat span{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.8px}h2{font-size:16px;margin:0 0 10px}h3{font-size:13px;margin:18px 0 7px;color:var(--muted)}canvas{display:block;width:100%;border-radius:9px;background:#0b1725}#space{aspect-ratio:1.25;cursor:crosshair}#chart{height:170px}.legend{display:flex;gap:15px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin:11px 0}.dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:5px}.faces{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.face{border:1px solid var(--line);padding:10px;border-radius:9px}.face-title{display:flex;justify-content:space-between;color:var(--blue);font-weight:700}.face small{color:var(--muted);display:block}.track{height:6px;background:#071320;border-radius:5px;margin:7px 0;overflow:hidden}.fill{height:100%;background:var(--amber)}.status{display:flex;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);font-size:12px}.status:last-child{border:0}.status span:last-child{color:var(--amber)}details{margin-top:18px;padding-top:12px;border-top:1px solid var(--line)}summary{cursor:pointer;color:var(--muted)}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;color:var(--muted)}code{overflow-wrap:anywhere;color:#bed8ef;font-size:11px}.note{border-left:3px solid #446d88;padding-left:11px;font-size:12px;color:var(--muted);margin-top:14px}.bottom{margin-top:18px}.chart-label{display:flex;justify-content:space-between;color:var(--muted);font-size:11px}.mono{font-variant-numeric:tabular-nums}@media(max-width:850px){main{padding:19px 14px}.grid{grid-template-columns:1fr}header{align-items:flex-start}h1{font-size:25px}.stats{grid-template-columns:repeat(2,1fr)}.pill{max-width:150px;white-space:normal;text-align:center}}
</style></head><body><main>
<header><div><div class="eyebrow">Universe24 / observation board</div><h1>Clocks, traffic and redistribution</h1><p class="muted">Recorded integer dynamics. Every displayed update comes from saved clicks.</p><p class="muted" id="preparation-summary"></p></div><span class="pill">PASSIVE CLICK REPLAY</span></header>
<div class="panel"><div class="controls"><button id="play" type="button">Play records</button><label>Playback <select id="speed"><option value="600">Slow</option><option value="220" selected>Normal</option><option value="80">Fast</option></select></label><label>Layer <select id="layer"><option value="occupation">Occupied slots</option><option value="moving_occupation">Transferable occupation</option><option value="held_occupation">Occupation held at capacity</option><option value="available_capacity">Available capacity</option><option value="clicks">Arithmetic clicks</option></select></label><label>Slice z <input id="slice" type="range" min="0" value="0"><span id="slice-label">0</span></label></div><div class="timeline"><span class="step" id="step-label"></span><input id="timeline" type="range" min="0" value="0" aria-label="Recorded update"></div><div class="note">The lattice is an address map. Distances, metric deformation and proper time have not been inferred.</div></div>
<div class="stats"><div class="stat"><span>Occupied slots</span><strong id="free"></strong></div><div class="stat"><span>Held at capacity</span><strong id="stored"></strong></div><div class="stat"><span>Occupied nodes</span><strong id="support"></strong></div><div class="stat"><span>Concentration · uniform = 1</span><strong id="concentration"></strong></div></div>
<div class="grid"><section class="panel"><h2>Node activity <span class="muted" id="slice-title"></span></h2><canvas id="space" aria-label="Node activity on the selected lattice slice"></canvas><div class="legend"><span><i class="dot" style="background:#173148"></i>Zero</span><span><i class="dot" style="background:var(--blue)"></i>Lower layer value</span><span><i class="dot" style="background:var(--amber)"></i>Higher layer value</span><span>Color scale is fixed across the recording · click a node for its six faces</span></div><h3>Distribution through the recorded history</h3><canvas id="chart" aria-label="Occupied-node fraction and concentration divided by node count through recorded history"></canvas><div class="legend"><span><i class="dot" style="background:var(--mint)"></i>Occupied-node fraction</span><span><i class="dot" style="background:var(--amber)"></i>Concentration / node count</span></div><div class="chart-label"><span>Initial calibration</span><span id="horizon"></span></div></section>
<aside class="panel"><h2 id="node-title">Node</h2><p class="muted" id="node-summary"></p><div class="faces" id="faces"></div><h3>What is identified</h3><div class="status"><span>Light-like transport</span><span>Isolated vacuum transport</span></div><div class="status"><span>Ordinary matter</span><span>Not established</span></div><div class="status"><span>Dark matter</span><span>Not established</span></div><div class="status"><span>Einstein geometry</span><span>Not established</span></div><div class="status"><span>Gravitational waves</span><span>Not established</span></div><div class="note">A held or optically quiet value is not automatically matter or dark matter. Color denotes occupation, not particle identity. Transferable/held classification is a passive gate-capacity diagnostic of the reconstructed state.</div><h3>Computation and observation</h3><p class="muted" id="work"></p><p class="muted" id="clicks"></p><details><summary>Calibration, provenance and limits</summary><p id="calibration"></p><p id="observation"></p><p id="integrity"></p><p>Click counts are not photon counts. Concentration can increase or decrease; replay does not establish monotonic balancing or gravity.</p><p>Initial preparation</p><pre id="preparation"></pre><p>Model <code id="model-id"></code></p><p>Run <code id="run-id"></code></p><p>Tensor <code id="tensor-hash"></code></p><p>Clicks <code id="click-hash"></code></p></details></aside></div>
</main><script type="application/json" id="board-data">__BOARD_DATA__</script><script>
'use strict';
const data=JSON.parse(document.getElementById('board-data').textContent);
const el=id=>document.getElementById(id), timeline=el('timeline'), slice=el('slice');
let step=0,z=Math.floor(data.L/2),selected=0,timer=null;
const names=['+x','−x','+y','−y','+z','−z'];
const ratio=v=>v&&Number(v.den)!==0?Number(v.num)/Number(v.den):0;
const display=v=>Number(v).toLocaleString('en-US');
const layerMax={};for(const key of ['occupation','moving_occupation','held_occupation','available_capacity','clicks']){let peak=1;for(const f of data.frames){const values=key==='clicks'?f.clicks_by_node:f.load.per_node[key];for(const value of values)peak=Math.max(peak,value)}layerMax[key]=peak}
function coordinates(n){return [Math.floor(n/(data.L*data.L)),Math.floor(n/data.L)%data.L,n%data.L]}
function nodeIndex(x,y){return x*data.L*data.L+y*data.L+z}
function fit(canvas){const r=canvas.getBoundingClientRect(),d=devicePixelRatio||1;canvas.width=Math.round(r.width*d);canvas.height=Math.round(r.height*d);const c=canvas.getContext('2d');c.scale(d,d);return [c,r.width,r.height]}
function palette(v,max){const t=max?Math.min(1,v/max):0;if(!t)return '#173148';return t<.6?`rgb(${Math.round(45+45*t)},${Math.round(105+130*t)},${Math.round(155+95*t)})`:`rgb(${Math.round(100+155*t)},${Math.round(180+13*t)},${Math.round(150-42*t)})`}
function spatial(){const [c,w,h]=fit(el('space')),f=data.frames[step],a=el('layer').value==='clicks'?f.clicks_by_node:f.load.per_node[el('layer').value];c.clearRect(0,0,w,h);const pad=30,unit=Math.min((w-pad*2)/data.L,(h-pad*2)/data.L),ox=(w-unit*data.L)/2,oy=(h-unit*data.L)/2,max=layerMax[el('layer').value];for(let x=0;x<data.L;x++)for(let y=0;y<data.L;y++){const n=nodeIndex(x,y),px=ox+x*unit,py=oy+(data.L-1-y)*unit;c.fillStyle=palette(a[n],max);c.fillRect(px+2,py+2,unit-4,unit-4);if(n===selected){c.strokeStyle='#fff';c.lineWidth=2;c.strokeRect(px+3,py+3,unit-6,unit-6)}if(unit>35){c.fillStyle='#f0f8ff';c.textAlign='center';c.font='12px system-ui';c.fillText(a[n],px+unit/2,py+unit/2+4)}}c.fillStyle='#9fb2c5';c.font='11px system-ui';c.textAlign='center';c.fillText('x →',w/2,h-8);c.save();c.translate(12,h/2);c.rotate(-Math.PI/2);c.fillText('y →',0,0);c.restore();el('space')._grid={ox,oy,unit};}
function chart(){const[c,w,h]=fit(el('chart')),pad=18;c.clearRect(0,0,w,h);c.strokeStyle='#294057';c.lineWidth=1;for(let k=0;k<=4;k++){const y=pad+(h-2*pad)*k/4;c.beginPath();c.moveTo(pad,y);c.lineTo(w-pad,y);c.stroke()}function line(get,color){c.strokeStyle=color;c.lineWidth=2;c.beginPath();data.frames.forEach((f,i)=>{let value=Math.max(0,Math.min(1,get(f))),x=pad+(w-2*pad)*i/Math.max(1,data.steps),y=h-pad-(h-2*pad)*value;i?c.lineTo(x,y):c.moveTo(x,y)});c.stroke()}line(f=>f.load.distribution.support_nodes/data.nodes,'#8ce5b7');line(f=>ratio(f.load.distribution.normalized_concentration)/data.nodes,'#ffc16c');const x=pad+(w-2*pad)*step/Math.max(1,data.steps);c.strokeStyle='#ecf6ff';c.setLineDash([3,4]);c.beginPath();c.moveTo(x,pad);c.lineTo(x,h-pad);c.stroke();c.setLineDash([]);}
function render(){const f=data.frames[step],p=f.load.per_node,d=f.load.distribution;timeline.value=step;slice.value=z;el('slice-label').textContent=z;el('step-label').textContent=`Update ${step} / ${data.steps}`;el('slice-title').textContent=`· z = ${z}`;el('free').textContent=display(f.load.totals.occupation);el('stored').textContent=display(f.load.totals.held_occupation);el('support').textContent=`${display(d.support_nodes)} / ${display(data.nodes)}`;el('concentration').textContent=ratio(d.normalized_concentration).toFixed(3);const xyz=coordinates(selected);el('node-title').textContent=`Node ${selected} · (${xyz.join(', ')})`;el('node-summary').textContent=`${p.occupation[selected]} / 48 occupied · ${p.held_occupation[selected]} held at current gate capacity · ${f.clicks_by_node[selected]} arithmetic clicks`;const faces=el('faces');faces.replaceChildren();f.load.per_face.forEach((face,i)=>{const card=document.createElement('div');card.className='face';const title=document.createElement('div');title.className='face-title';title.textContent=`${names[i]}  /  ${face.occupation[selected]} of 8 slots`;const track=document.createElement('div');track.className='track';const fill=document.createElement('div');fill.className='fill';fill.style.width=`${Math.min(100,100*face.occupation[selected]/8)}%`;track.append(fill);const detail=document.createElement('small');detail.textContent=`${face.moving_occupation[selected]} transferable · ${face.held_occupation[selected]} held · ${face.available_capacity[selected]} empty`;card.append(title,track,detail);faces.append(card)});const work=f.work,schedule=work.canonical_scalar_schedule_per_node;el('work').textContent=`${display(schedule.monomial_evaluations)} monomial evaluations per node per update. Selected node: ${display(work.magnitude_bits_sum_by_node[selected])} retained magnitude bits; largest integer ${work.magnitude_bits_max_by_node[selected]} bits. Representation size is not calibrated energy or CPU time.`;el('clicks').textContent=`${display(f.clicks)} arithmetic clicks in this update. ${display(f.load.blocked_quartets)} edge quartets at 3/4 capacity; ${display(f.load.saturated_quartets)} fully occupied. These are gate states, not particle waiting times.`;spatial();chart()}
function stop(){if(timer){clearInterval(timer);timer=null}el('play').textContent='Play records'}
function play(){if(timer){stop();return}if(step===data.steps)step=0;el('play').textContent='Pause replay';timer=setInterval(()=>{if(step>=data.steps){stop();return}step++;render()},Number(el('speed').value));render()}
timeline.max=data.steps;slice.max=data.L-1;selected=nodeIndex(Math.floor(data.L/2),Math.floor(data.L/2));
el('horizon').textContent=`Update ${data.steps}`;el('preparation').textContent=JSON.stringify(data.preparation,null,2);const prep=data.preparation.preparation||{};el('preparation-summary').textContent=`Initial ${prep.pattern||'sealed input'} · radius ${prep.radius??'—'} · ${prep.total_occupation??'—'} occupied slots · seeded halo ${prep.halo?'enabled':'disabled'} (${prep.halo_occupation??0} slots).`;for(const [id,key]of [['calibration','calibration'],['observation','observation'],['integrity','integrity'],['model-id','model_id'],['run-id','run_id'],['tensor-hash','tensor_hash'],['click-hash','click_sha256']])el(id).textContent=data[key];
timeline.addEventListener('input',()=>{stop();step=Number(timeline.value);render()});slice.addEventListener('input',()=>{z=Number(slice.value);const xyz=coordinates(selected);selected=nodeIndex(xyz[0],xyz[1]);render()});el('layer').addEventListener('change',render);el('play').addEventListener('click',play);el('speed').addEventListener('change',()=>{if(timer){stop();play()}});el('space').addEventListener('click',event=>{const r=el('space').getBoundingClientRect(),g=el('space')._grid,x=Math.floor((event.clientX-r.left-g.ox)/g.unit),y=data.L-1-Math.floor((event.clientY-r.top-g.oy)/g.unit);if(x>=0&&x<data.L&&y>=0&&y<data.L){selected=nodeIndex(x,y);render()}});window.addEventListener('resize',render);render();
</script></body></html>'''
