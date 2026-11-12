"""Passive, standalone visualization of a saved Universe24 run.

This module never prepares or advances an Engine. Its only input is the report
produced from a saved run. Floating point is confined to drawing.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any



def validate_report(data: dict[str, Any]) -> None:
    """Reject inconsistent display reports, without claiming trace verification.

    Self-consistent JSON is not proof of a historical Engine execution. The
    full saved bundle/trace must still be checked with the unified verifier.
    """
    if not isinstance(data, dict) or data.get("schema") != "universe24/geodesic-board/1":
        raise ValueError("Unsupported saved-run report schema")
    try:
        metadata, provenance, runtime = data["metadata"], data["provenance"], data["runtime_validation"]
        snapshots, gates = data["snapshots"], data["acceptance_gates"]
        if runtime["schema"] != "universe24/system/run/1":
            raise ValueError("Unsupported runtime report schema")
        identities = (
            (metadata["tensor_sha256"], provenance["tensor_sha256"], runtime["tensor_hash"]),
            (provenance["run_id"], runtime["run_id"]),
            (provenance["bundle_id"], runtime["bundle_id"]),
            (provenance["trace_sha256"], runtime["files"]["full_trace.jsonl.gz"]),
        )
        for values in identities:
            if any(not isinstance(v, str) or not re.fullmatch(r"[0-9a-f]{64}", v) for v in values) or len(set(values)) != 1:
                raise ValueError("Mismatched or malformed saved-run identity")
        steps, channels, nodes = metadata["steps"], metadata["channels"], metadata["nodes"]
        if any(type(v) is not int for v in (steps, channels, nodes)) or not (1 <= steps <= 8 and 1 <= channels <= 48 and nodes > 0):
            raise ValueError("Invalid saved-run dimensions")
        if (runtime["steps"], runtime["channels_per_node"], runtime["nodes"]) != (steps, channels, nodes):
            raise ValueError("Metadata/runtime dimensions disagree")
        if runtime["retained_integers_per_node"] != 3*channels or len(snapshots) != steps+1:
            raise ValueError("Retained-state or snapshot count disagrees")
        if metadata["max_bits"] != max(runtime["maximum_integer_bits_by_step"]) or len(runtime["maximum_integer_bits_by_step"]) != steps+1:
            raise ValueError("Integer cost evidence disagrees")
        for i, snapshot in enumerate(snapshots):
            if snapshot["step"] != i or len(snapshot["nodes"]) != nodes:
                raise ValueError("Incomplete saved snapshot")
            if [row["node"] for row in snapshot["nodes"]] != list(range(nodes)):
                raise ValueError("Saved node identities disagree")
            first = snapshot["nodes"][0]
            for alias, source in (("gamma", "gamma"), ("energy_density", "rho"), ("dust_density", "dust_density"), ("charge", "electric_charge")):
                if snapshot[alias] != first[source]:
                    raise ValueError("Display aliases disagree with saved diagnostics")
            if snapshot["hamiltonian_constraint"] != first["constraints"]["H"]:
                raise ValueError("Constraint display disagrees with saved diagnostics")
        required = {"integer_local_reversible_execution": "passed",
                    "same_tensor_massive_source_and_metric": "passed",
                    "independent_scalar_oracle": "passed",
                    "metric_positive_on_saved_run": "passed",
                    "exact_discrete_Einstein_constraints": "failed",
                    "general_Einstein_convergence": "not_tested",
                    "retained_geodesic_probe": "not_implemented",
                    "operational_material_clock": "not_implemented",
                    "Born_Bell_quantum_dynamics": "not_implemented"}
        if gates != required:
            raise ValueError("Unreviewed physical acceptance status")
        checks = runtime["checks"]
        for name in ("bundle_contract", "complete_state_forward_replay", "complete_state_step_inverse", "complete_state_rewind_to_seed", "canonical_click_parity"):
            if checks[name] != "passed":
                raise ValueError("Runtime report lacks required execution checks")
        from .geodesics import build_geodesics
        expected = build_geodesics(snapshots)
        if data["geodesics"] != expected:
            raise ValueError("Geodesics do not match this saved metric report")
        json.dumps(data, allow_nan=False)
    except (KeyError, TypeError, IndexError) as exc:
        raise ValueError("Incomplete or malformed saved-run report") from exc


def render_board(data: dict[str, Any], output_path: str | Path) -> Path:
    """Write a self-contained board; preserve report provenance verbatim."""
    validate_report(data)
    # Script data cannot close its enclosing element, including user labels.
    payload = json.dumps(data, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c").replace("&", "\\u0026")
    title = html.escape(str(data.get("title", "Universe24 · לוח אירועים")))
    document = _HTML.replace("__TITLE__", title).replace("__DATA__", payload)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document, encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    data = json.loads(args.report.read_text(encoding="utf-8"))
    print(render_board(data, args.out or args.report.with_name("board.html")))


_HTML = r'''<!doctype html>
<html lang="he"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>__TITLE__</title>
<style>
:root{color-scheme:dark;--bg:#091019;--panel:#101b28;--line:#263749;--muted:#93a8bd;--fg:#eaf2fa;--cyan:#64dded;--gold:#ffc67b;--green:#91dfb3;--pink:#f797b2}*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 75% -25%,#183a4d 0,transparent 60%),var(--bg);color:var(--fg);font:14px/1.55 system-ui,sans-serif}main{max-width:1440px;margin:auto;padding:30px 34px 40px}header{display:flex;justify-content:space-between;align-items:start;gap:24px;margin-bottom:22px}.eyebrow{font-size:11px;letter-spacing:.19em;color:var(--cyan);font-weight:700}h1{font-size:34px;letter-spacing:-1px;margin:5px 0 4px;font-weight:650}h1 span{font-size:22px;font-weight:400;color:#b9cbdc}.sub{color:var(--muted);max-width:790px;margin:0}.status{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.tag{font-size:11px;padding:5px 9px;border:1px solid var(--line);border-radius:5px;background:#13202c;color:#bdd0e1}.tag.amber{color:var(--gold);border-color:#654e32;background:#282319}.tag.green{color:var(--green)}.layout{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:18px}.panel{background:linear-gradient(140deg,#132130,#0e1925);border:1px solid var(--line);border-radius:12px;overflow:hidden}.panelhead{padding:19px 22px 12px;display:flex;justify-content:space-between;gap:14px;align-items:start}.panelhead h2{font-size:17px;margin:0;font-weight:580}.small{font-size:12px;color:var(--muted)}.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:11px;color:#c8d7e6}.legend i{display:inline-block;width:15px;height:3px;border-radius:5px;vertical-align:middle;margin-right:5px}.canvaswrap{height:430px;padding:0 12px}canvas{display:block;width:100%;height:100%}.controls{padding:15px 22px 18px;display:flex;gap:15px;align-items:center;border-top:1px solid var(--line)}button{background:#203849;color:var(--fg);border:1px solid #3e5b6c;border-radius:6px;padding:8px 15px;font:inherit;cursor:pointer;min-width:84px}button:hover{background:#2a4b61}input[type=range]{width:100%;accent-color:var(--cyan);cursor:pointer}.step{font-variant-numeric:tabular-nums;white-space:nowrap;color:var(--cyan)}.note{margin:0;padding:0 22px 18px;font-size:12px;color:var(--muted)}aside{display:flex;flex-direction:column;gap:14px}.metric{padding:17px 19px}.metric h3{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}.hero-value{font-size:28px;line-height:1.2;letter-spacing:-.8px;font-variant-numeric:tabular-nums}.unit{font-size:12px;color:var(--muted);margin-top:6px}.pair{display:flex;justify-content:space-between;align-items:center;margin-top:8px;font-size:12px}.pair strong{font-variant-numeric:tabular-nums;font-weight:500}.matrix{font-family:ui-monospace,monospace;color:#cfe2f2;font-size:12px;white-space:pre;line-height:1.6;margin:10px 0 0}.chart{height:182px;padding:4px 12px 12px}.lower{display:grid;grid-template-columns:1.05fr 1fr;gap:18px;margin-top:18px}.gatebox{padding:18px 22px}.gatebox h2{font-size:15px;margin:0 0 10px}.gate{display:flex;justify-content:space-between;gap:14px;padding:7px 0;border-bottom:1px solid #21303f;font-size:12px}.gate:last-child{border:0}.gate em{font-style:normal;color:var(--gold)}.gate em.pass{color:var(--green)}details{margin-top:18px;border-top:1px solid var(--line);padding-top:15px}summary{cursor:pointer;color:#b0c4d7;font-size:12px}pre{background:#08111b;padding:15px;border-radius:8px;white-space:pre-wrap;overflow-wrap:anywhere;color:#9db6cc;font-size:11px;max-height:260px;overflow:auto}footer{display:flex;justify-content:space-between;gap:20px;color:#7891a7;font-size:11px;margin-top:20px}.rtl{direction:rtl;text-align:right}.warning{color:var(--gold)}@media(max-width:960px){main{padding:20px}.layout{grid-template-columns:1fr}aside{display:grid;grid-template-columns:1fr 1fr}.lower{grid-template-columns:1fr}header{display:block}.canvaswrap{height:380px}}@media(max-width:560px){h1{font-size:28px}h1 span{display:block;font-size:20px}aside{grid-template-columns:1fr}.panelhead{display:block}.legend{margin-top:10px}.canvaswrap{height:340px}.controls{padding:12px;gap:9px}.step{font-size:11px}footer{display:block}}
</style></head><body><main>
<header><div><div class="eyebrow">ONE ENGINE · ONE SAVED RUN · ONE METRIC</div><h1>Universe24 <span>לוח אירועים וגאודזיות</span></h1><p class="sub rtl">מסלולי אור וחלקיקי מבחן המחושבים מתוך המטריקה של אותה ריצה. הלוח קורא תוצאות שמורות; הוא אינו משנה את הדינמיקה.</p><div class="status"><span class="tag" id="channelTag">Retained channels</span><span class="tag">Exact integer Rule3</span><span class="tag">Face-local tensor</span><span class="tag amber">GR & quantum acceptance remain open</span></div></div><div class="small" style="padding-top:9px">SAVED-RUN OBSERVATORY<br><span id="hashShort"></span></div></header>
<div class="layout"><section class="panel"><div class="panelhead"><div><h2>מרחב האירועים · Spacetime section</h2><div class="small">Physical x-distance versus coordinate time · y = z = 0 node slice</div></div><div class="legend"><span><i style="background:var(--cyan)"></i>Null</span><span><i style="background:var(--gold)"></i>Timelike</span><span><i style="background:#778ea5"></i>Saved node event</span></div></div><div class="canvaswrap"><canvas id="spacetime" aria-label="Saved spacetime node events and passive null and timelike trajectories"></canvas></div><div class="controls"><button id="play" type="button">▶ Play</button><input id="time" type="range" min="0" step="1" aria-label="Saved time slice"><span class="step" id="step"></span></div><p class="note">Dots are saved computational node events. Curves are passive test paths in the reconstructed metric, not retained particles or detector clicks. The time slider selects saved slices; animation does not evolve the Engine. This offline page checks report consistency, not the authenticity of an independently supplied trace.</p></section>
<aside><section class="panel metric"><h3>Selected metric · מטריקה</h3><div class="hero-value" id="scale"></div><div class="unit">x-axis scale √γₓₓ · lapse 1 · shift 0</div><div class="matrix" id="matrix"></div></section><section class="panel metric"><h3>Matter on the same slice · חומר</h3><div class="hero-value" id="energy"></div><div class="unit">total energy density ρ</div><div class="pair"><span>Dust density</span><strong id="dust"></strong></div><div class="pair"><span>Scalar energy</span><strong id="scalar"></strong></div><div class="pair"><span>Charge density</span><strong id="charge"></strong></div></section><section class="panel metric"><h3>Einstein constraint · אילוץ</h3><div class="hero-value warning" id="constraint"></div><div class="unit">Hamiltonian residual H · zero is the target</div><div class="pair"><span>Max retained integer size</span><strong id="bits"></strong></div></section></aside></div>
<div class="lower"><section class="panel"><div class="panelhead"><div><h2>Constraint history · שגיאת האילוץ</h2><div class="small">Signed residual from the saved metric and matter. A growing error is not hidden.</div></div></div><div class="chart"><canvas id="history" aria-label="Hamiltonian constraint residual over saved time"></canvas></div></section><section class="panel gatebox"><h2>What this run establishes · גבולות התוצאה</h2><div id="gates"></div><p class="small" style="margin:12px 0 0">Geodesic quadrature accuracy is a readout check. It does not establish convergence of the underlying Einstein evolution, physical clocks, Born probabilities or Bell correlations.</p></section></div>
<details><summary>Run identity, methods and acceptance evidence</summary><pre id="provenance"></pre></details><footer><span>Universe24 · reversible state, passive observation</span><span>Report consistency checked; replay the full trace to verify its origin.</span></footer>
</main><script id="report" type="application/json">__DATA__</script><script>
'use strict';
const D=JSON.parse(document.getElementById('report').textContent), S=D.snapshots, M=D.metadata||{}, G=D.geodesics||{}, paths=(G.paths||[]).filter(p=>(p.points||[]).every(q=>Array.isArray(q.x)&&Math.abs(Number(q.x[1]))<1e-12&&Math.abs(Number(q.x[2]))<1e-12));
const $=id=>document.getElementById(id), n=v=>typeof v==='number'?v:(typeof v==='string'&&v.includes('/')?v.split('/').map(Number).reduce((a,b)=>a/b):Number(v)), fmt=v=>Number.isFinite(n(v))?(Math.abs(n(v))<1e-6&&n(v)!==0?n(v).toExponential(3):n(v).toLocaleString('en-US',{maximumSignificantDigits:6})):'not reported';
function node(s){return(s.nodes||[])[0]||{};}function gamma(s){return s.gamma||node(s).gamma;}function val(s,k,nk){return s[k]??node(s)[nk||k];}function H(s){return s.hamiltonian_constraint??node(s).constraints?.H;}function time(s){return n(s.time);}function a(s){return Math.sqrt(n(gamma(s)[0][0]));}
let selected=S.length-1, timer=null; const slider=$('time');slider.max=S.length-1;slider.value=selected;
$('channelTag').textContent=(M.channels??D.channels??'—')+' / 48 retained channels';$('hashShort').textContent=(M.tensor_sha256||D.provenance?.tensor_sha256||'').slice(0,16);
$('bits').textContent=(M.max_bits??D.max_bits??'—')+' bits';
const gateRows=[['Exact replay',D.acceptance_gates?.integer_local_reversible_execution],['Shared saved metric',D.acceptance_gates?.same_tensor_massive_source_and_metric],['Retained physical probe',D.acceptance_gates?.retained_geodesic_probe],['Einstein constraint preservation',D.acceptance_gates?.exact_discrete_Einstein_constraints],['General GR convergence',D.acceptance_gates?.general_Einstein_convergence],['Quantum Born / Bell',D.acceptance_gates?.Born_Bell_quantum_dynamics]];
for(const [label,status] of gateRows){const row=document.createElement('div');row.className='gate';const left=document.createElement('span');left.textContent=label;const right=document.createElement('em');right.textContent=status===true?'passed':typeof status==='string'?status:'see evidence';if(status===true||status==='passed')right.className='pass';row.append(left,right);$('gates').append(row);}
$('provenance').textContent=JSON.stringify({metadata:M,provenance:D.provenance,runtime_validation:D.runtime_validation,acceptance_gates:D.acceptance_gates,geodesic_method:G.method,geodesic_quadrature:G.quadrature_refinement,geodesic_scope:G.scope,quantum:D.quantum},null,2);
function canvas(id){const el=$(id),rect=el.getBoundingClientRect(),ratio=window.devicePixelRatio||1;el.width=Math.round(rect.width*ratio);el.height=Math.round(rect.height*ratio);const c=el.getContext('2d');c.scale(ratio,ratio);return[c,rect.width,rect.height];}
function metricAt(t){if(t<=time(S[0]))return a(S[0]);for(let i=1;i<S.length;i++)if(t<=time(S[i])){const f=(t-time(S[i-1]))/(time(S[i])-time(S[i-1]));return Math.sqrt((1-f)*n(gamma(S[i-1])[0][0])+f*n(gamma(S[i])[0][0]));}return a(S[S.length-1]);}
function pointX(p){const x=Array.isArray(p.x)?n(p.x[0]):n(p.x);return metricAt(n(p.t))*x;}
function sliceNodes(s){const ns=(s.nodes||[]).filter(v=>Array.isArray(v.position)&&n(v.position[1])===0&&n(v.position[2])===0);const dx=n(M.dx??1);return ns.map(v=>n(v.position[0])*(M.position_units==='physical_coordinates'?1:dx)*a(s));}
function drawBoard(){const[c,w,h]=canvas('spacetime'),pad={l:64,r:30,t:30,b:44},ts=S.map(time),t0=Math.min(...ts),t1=Math.max(...ts),xs=[0,...S.flatMap(sliceNodes),...paths.flatMap(p=>(p.points||[]).map(pointX))];let lo=Math.min(...xs),hi=Math.max(...xs),span=hi-lo||1;lo-=span*.16;hi+=span*.16;const X=x=>pad.l+(x-lo)/(hi-lo)*(w-pad.l-pad.r),Y=t=>h-pad.b-(t-t0)/(t1-t0||1)*(h-pad.t-pad.b);c.clearRect(0,0,w,h);c.font='11px system-ui';c.textAlign='right';
for(let i=0;i<=4;i++){let t=t0+(t1-t0)*i/4,y=Y(t);c.strokeStyle='#223344';c.beginPath();c.moveTo(pad.l,y);c.lineTo(w-pad.r,y);c.stroke();c.fillStyle='#8098ae';c.fillText(fmt(t),pad.l-11,y+4);}c.textAlign='center';for(let i=0;i<=4;i++){let x=lo+(hi-lo)*i/4;c.fillStyle='#8098ae';c.fillText(fmt(x),X(x),h-20);}c.save();c.translate(15,h/2);c.rotate(-Math.PI/2);c.fillStyle='#a9bfd2';c.fillText('Coordinate time t',0,0);c.restore();c.textAlign='right';c.fillStyle='#a9bfd2';c.fillText('Physical distance √γₓₓ x',w-pad.r,h-2);
for(let si=0;si<S.length;si++){const s=S[si],y=Y(time(s));c.strokeStyle=si===selected?'#406b80':'#253c4e';c.setLineDash([3,6]);c.beginPath();c.moveTo(pad.l,y);c.lineTo(w-pad.r,y);c.stroke();c.setLineDash([]);for(const x of sliceNodes(s)){c.beginPath();c.arc(X(x),y,si===selected?4:3,0,Math.PI*2);c.fillStyle=si===selected?'#c4dced':'#526f86';c.fill();}}
for(const p of paths){const pts=p.points||[],color=p.kind==='null'?'#64dded':'#ffc67b';c.lineWidth=p.kind==='null'?2:2.5;c.strokeStyle=color;c.globalAlpha=.18;c.beginPath();pts.forEach((pt,i)=>i?c.lineTo(X(pointX(pt)),Y(n(pt.t))):c.moveTo(X(pointX(pt)),Y(n(pt.t))));c.stroke();c.globalAlpha=1;c.beginPath();let last=null;for(const pt of pts){if(n(pt.t)>time(S[selected])+1e-12)break;if(last)c.lineTo(X(pointX(pt)),Y(n(pt.t)));else c.moveTo(X(pointX(pt)),Y(n(pt.t)));last=pt;}c.stroke();if(last){c.beginPath();c.arc(X(pointX(last)),Y(n(last.t)),4,0,Math.PI*2);c.fillStyle=color;c.fill();}}c.lineWidth=1;c.globalAlpha=1;
if(!paths.length){c.fillStyle='#ffc67b';c.textAlign='center';c.fillText('No reconstructed paths in this report',w/2,h/2);}}
function drawHistory(){const[c,w,h]=canvas('history'),p={l:66,r:22,t:15,b:30},vs=S.map(s=>n(H(s))),ts=S.map(time);let mn=Math.min(0,...vs.filter(Number.isFinite)),mx=Math.max(0,...vs.filter(Number.isFinite));if(mx===mn){mn-=1;mx+=1;}const r=mx-mn;mn-=r*.1;mx+=r*.1;const X=t=>p.l+(t-ts[0])/(ts.at(-1)-ts[0]||1)*(w-p.l-p.r),Y=v=>h-p.b-(v-mn)/(mx-mn)*(h-p.t-p.b);c.font='10px system-ui';c.strokeStyle='#304453';c.beginPath();c.moveTo(p.l,Y(0));c.lineTo(w-p.r,Y(0));c.stroke();c.fillStyle='#8ba4b9';c.textAlign='right';for(let i=0;i<3;i++){let v=mn+(mx-mn)*i/2;c.fillText(fmt(v),p.l-8,Y(v)+3);}c.strokeStyle='#f797b2';c.lineWidth=2;c.beginPath();vs.forEach((v,i)=>{if(Number.isFinite(v)){if(i)c.lineTo(X(ts[i]),Y(v));else c.moveTo(X(ts[i]),Y(v));}});c.stroke();vs.forEach((v,i)=>{if(!Number.isFinite(v))return;c.fillStyle=i===selected?'#ffe2eb':'#f797b2';c.beginPath();c.arc(X(ts[i]),Y(v),i===selected?4:2.5,0,Math.PI*2);c.fill();});c.fillStyle='#8ba4b9';c.textAlign='left';c.fillText('t = '+fmt(ts[0]),p.l,h-8);c.textAlign='right';c.fillText(fmt(ts.at(-1)),w-p.r,h-8);}
function update(){const s=S[selected];$('step').textContent='t '+fmt(time(s))+' · '+selected+'/'+(S.length-1);$('scale').textContent=fmt(a(s));$('energy').textContent=fmt(val(s,'energy_density','rho'));$('dust').textContent=fmt(val(s,'dust_density'));$('scalar').textContent=fmt(val(s,'scalar_energy'));$('charge').textContent=fmt(val(s,'charge','electric_charge'));$('constraint').textContent=fmt(H(s));$('matrix').textContent=gamma(s).map(row=>'[ '+row.map(v=>fmt(v).padStart(8)).join('  ')+' ]').join('\n');drawBoard();drawHistory();}
slider.addEventListener('input',()=>{selected=Number(slider.value);update();});$('play').addEventListener('click',()=>{if(timer){clearInterval(timer);timer=null;$('play').textContent='▶ Play';}else{if(selected===S.length-1)selected=-1;$('play').textContent='Ⅱ Pause';timer=setInterval(()=>{selected++;slider.value=selected;update();if(selected>=S.length-1){clearInterval(timer);timer=null;$('play').textContent='▶ Play';}},850);}});window.addEventListener('resize',update);update();
</script></body></html>'''

if __name__ == "__main__":
    main()
