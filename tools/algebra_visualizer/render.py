"""The algebra visualizer: one page in three layers (the geometry that is the
algebra; how it produces the physics; the clicks), every panel read from a
run's record alone (docs/designs/algebra_visualizer/DESIGN.md; the model
owner's word of 2026-09-23 through the Boss, record 1435).

Headless by default: the tool reads the two runs, builds the panels and
prints every number with its kind and its source, and writes nothing.
`--render OUT.html` writes the one static page (inline SVG and CSS, a few
lines of plain script for the sliders) and nothing else. The tool never
runs the engine: a missing run folder is refused with the line that makes
it (`tools/run_series.py`). Standard library only; nothing of
`event_universe` is imported.

    PYTHONPATH=src python tools/algebra_visualizer/render.py RUNS_DIR [--render OUT.html]
        [--light c_measured] [--detector slits_low]
    PYTHONPATH=src python tools/algebra_visualizer/render.py RUN_FOLDER [--render OUT.html]

`RUNS_DIR` holds one folder per world, `<name>/run` (the runner's output
through `tools/run_series.py`) or `<name>`: the first page, two runs in
three layers (DESIGN.md). `RUN_FOLDER` holds one run's `run.json`: the 3-D
page of docs/designs/algebra_visualizer/DESIGN_3D.md, any registered run of
either engine (the Beam Law on main, or the detector law told from
`run.json`'s `hypotheses`) in the owner's three layers, the algebra, the
GameBoard as the Inside in 3-D with a step control over the intervals, and
the clicks as the Outside. The registers are read from `examples/events/`
by the world's name (`REGISTERS`); a world without a register prints no PIN.
An EXPLORATORY run (the word in its folder's path or its model identity)
carries EXPLORATORY in the page's title and on every panel, never a result.
"""

from __future__ import annotations

import argparse
import sys
from html import escape
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import json  # noqa: E402

from board3d import build_layer  # noqa: E402
from panels import (  # noqa: E402
    KIND_WORDS,
    KINDS,
    Panel,
    as_rows,
    build_panels,
    build_run_panels,
    head_numbers,
    head_numbers_run,
)
from record import MissingRun, RunRecord, load_run  # noqa: E402
from svg import figure  # noqa: E402

# The register of a registered world, by the world's name: the file beside
# the world and, where the register keeps one block per world, its block.
REGISTERS: dict[str, tuple[str, str | None]] = {
    "c_measured": ("examples/events/c_measured/expectations.json", None),
    "slits_low": ("examples/events/amplitude/expectations.json", "two_slits"),
}

LAYERS = {
    1: (
        "The geometry that is the algebra",
        "Everything generic, no physical name: the torus, a Node with its six Ports, a record's state vector, each of the six verbs on one Node with its integers, the light rule as one picture.",
    ),
    2: (
        "How it produces the physics",
        "The same verbs over many Nodes and many intervals: a record propagating and read at the faces, the pace c, a foreign object as a declared block with its own pair, a detector-emitter as a declared object, and a GameBoard view labelled a diagnostic.",
    ),
    3: (
        "The clicks",
        "How a click is born on the board, beside how it looks in our world: one record's birth, offers, gather and deletion; the screen as the experimenter sees it, the counts against the detector's clock, the interval between clicks. Every click a DETECTOR reading; nothing pinned or compared.",
    ),
}

LAYERS_RUN = {
    1: (
        "The algebra",
        "The run's declared objects as objects of ALGEBRA.md: the families with their pairs, the blocks with their pairs and sides, the detectors and the emitters, the board's extents and faces, the verbs that act per interval. Every integer DECLARATION, read from run.json and the world file beside it.",
    ),
    2: (
        "The GameBoard, the Inside: a diagnostic, never a measurement",
        "The board in 3-D: the Nodes' extents as a box, a layer or a chain; the records' presence over the intervals where the record shows it; the blocks as cubes at their recorded positions; the detectors as faces or cells; a step control over the intervals. GAMEBOARD, the host's view of the board.",
    ),
    3: (
        "The Outside: the clicks",
        "The clicks as the detectors' own records in their own counts: per detector its clicks, the count against the detector's own count where the run stamps it, the intervals between clicks, the pattern an experimenter sees. Every number DETECTOR; nothing pinned or compared.",
    ),
}

WIDE = {
    "light_rule",
    "fan",
    "pace",
    "life",
    "screen",
    "clock",
    "objects",
    "gameboard",
    "block",
    "board",
    "alg_blocks",
    "alg_instruments",
    "out_records",
    "out_clock",
}

CSS = """
:root{--ground:#f5f6f8;--surface:#ffffff;--ink:#14181d;--muted:#5c6470;--rule:#d9dde3;--soft:#eceff3;
--detector:#1f3f9a;--gameboard:#6a707a;--computation:#0b7a6e;--host:#7a5b12;--conversion:#5a7a1f;--declaration:#7a2f74;--pin:#b0641c;
--c-axes:#2f5bd1;--c-face:#c9622a;--c-body:#2e8b57;--c-rest:#7b6fb0;--band:#e9edf3;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;--ground:#14171b;--surface:#1c2026;--ink:#e6e4df;--muted:#a3a9b3;--rule:#2e343c;--soft:#252a31;
--detector:#8fa8ff;--gameboard:#9aa1ab;--computation:#5fcfc2;--host:#d9b25b;--conversion:#b6d16a;--declaration:#d78bd0;--pin:#f0a45c;
--c-axes:#7f9bff;--c-face:#f0925a;--c-body:#66c48f;--c-rest:#b3a7f0;--band:#1a1e24;}}
:root[data-theme="dark"]{color-scheme:dark;--ground:#14171b;--surface:#1c2026;--ink:#e6e4df;--muted:#a3a9b3;--rule:#2e343c;--soft:#252a31;
--detector:#8fa8ff;--gameboard:#9aa1ab;--computation:#5fcfc2;--host:#d9b25b;--conversion:#b6d16a;--declaration:#d78bd0;--pin:#f0a45c;
--c-axes:#7f9bff;--c-face:#f0925a;--c-body:#66c48f;--c-rest:#b3a7f0;--band:#1a1e24;}
body{background:var(--ground);color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5;margin:0;padding-block:24px 64px;padding-inline:16px;}
.wrap{max-width:1160px;margin:0 auto;}
h1,h2,h3{font-family:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;text-wrap:balance;font-weight:600;}
h1{font-size:2rem;margin:0 0 .4rem;} h2{font-size:1.5rem;margin:0;} h3{font-size:1.1rem;margin:0 0 .5rem;}
p{max-width:72ch;} .lede{color:var(--muted);max-width:80ch;margin:.2rem 0 1rem;}
.head{border-bottom:1px solid var(--rule);padding-bottom:1rem;margin-bottom:1.5rem;}
.runs{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;margin:1rem 0;}
.run{background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:12px 14px;}
.run h3{margin-bottom:.3rem;}
.legend{display:flex;flex-wrap:wrap;gap:8px 14px;margin:.6rem 0 0;padding:0;list-style:none;font-size:.85rem;color:var(--muted);}
.legend li{display:flex;align-items:center;gap:6px;}
.badge{display:inline-block;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.68rem;letter-spacing:.06em;padding:1px 6px;border-radius:3px;border:1px solid currentColor;line-height:1.4;white-space:nowrap;}
.k-DETECTOR{color:var(--detector);background:color-mix(in srgb,var(--detector) 12%,transparent);}
.k-GAMEBOARD{color:var(--gameboard);border-style:dashed;}
.k-COMPUTATION{color:var(--computation);}
.k-HOST{color:var(--host);}
.k-CONVERSION{color:var(--conversion);}
.k-DECLARATION{color:var(--declaration);}
.k-PIN{color:var(--pin);border-style:dashed;}
.layer{margin:2.2rem 0 0;padding-top:1.2rem;border-top:3px solid var(--rule);}
.layer-head{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:baseline;margin-bottom:1rem;}
.layer-n{font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;font-size:2.6rem;line-height:1;color:var(--muted);}
.panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr));gap:18px;}
.panel{background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:14px 16px 12px;display:flex;flex-direction:column;gap:10px;min-width:0;}
.panel.wide{grid-column:1 / -1;}
.panel.diag{background:var(--band);border-style:dashed;}
.panel .eyebrow{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}
.alg{margin:0;padding:0 0 0 12px;border-left:2px solid var(--rule);font-size:.92rem;}
.alg p{margin:0 0 .4rem;} .alg .ref{color:var(--muted);font-size:.8rem;}
.fig{overflow-x:auto;} .figure{width:100%;height:auto;max-width:100%;display:block;}
.figure text{font-family:system-ui,sans-serif;fill:var(--ink);font-size:12px;}
.figure .t-small{font-size:11px;fill:var(--muted);} .figure .t-tiny{font-size:9px;fill:var(--muted);}
.figure .t-mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;}
.figure .t-label{font-weight:600;} .figure .t-on-node{fill:var(--surface);font-size:11px;}
.figure .line{stroke:var(--ink);stroke-width:1.2;fill:none;} .figure .line-strong{stroke:var(--ink);stroke-width:2;}
.figure .line-faint{stroke:var(--muted);stroke-width:.8;opacity:.6;} .figure .grid{stroke:var(--rule);stroke-width:1;fill:none;}
.figure .line-inference{stroke:var(--muted);stroke-width:.6;opacity:.14;}
.figure .line-c{stroke:var(--computation);stroke-width:2;stroke-dasharray:6 4;}
.figure .arrow{stroke:var(--detector);stroke-width:2;}
.figure .node{fill:var(--ink);} .figure .node-far{fill:var(--soft);stroke:var(--ink);stroke-width:1.2;}
.figure .box{fill:var(--soft);stroke:var(--rule);} .figure .face{fill:var(--soft);stroke:var(--rule);}
.figure .mark-detector{fill:var(--detector);} .figure .bar{fill:var(--detector);}
.figure .stair{fill:none;stroke:var(--detector);stroke-width:2;}
.figure .rung{stroke:var(--muted);stroke-width:1.5;} .figure .rung-chosen{stroke:var(--detector);stroke-width:3;}
.figure .mark{stroke:var(--surface);stroke-width:1;} .figure .m-axes{fill:var(--c-axes);} .figure .m-face{fill:var(--c-face);}
.figure .m-body{fill:var(--c-body);} .figure .m-rest{fill:var(--c-rest);}
.figure .cell-medium{fill:var(--soft);stroke:var(--rule);} .figure .cell-well{fill:var(--declaration);opacity:.75;}
.figure .obj-lamp{fill:var(--host);} .figure .obj-reemit{fill:var(--declaration);} .figure .obj-detector{fill:var(--detector);} .figure .obj-wall{fill:var(--muted);}
.figure .store-node{fill:var(--gameboard);}
dl.nums{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:4px 12px;margin:0;font-size:.88rem;}
dl.nums dt{color:var(--muted);} dl.nums dd{margin:0;font-family:ui-monospace,Menlo,Consolas,monospace;font-variant-numeric:tabular-nums;word-break:break-all;display:flex;gap:6px;align-items:baseline;flex-wrap:wrap;}
.note{font-size:.85rem;color:var(--muted);margin:0;}
.missing{font-size:.9rem;padding:8px 10px;border:1px dashed var(--rule);border-radius:4px;color:var(--muted);}
.sources{font-size:.75rem;color:var(--muted);border-top:1px solid var(--rule);padding-top:6px;margin-top:auto;}
.control{display:flex;gap:10px;align-items:center;font-size:.85rem;flex-wrap:wrap;}
.control input[type=range]{flex:1;min-width:160px;}
.control select{font:inherit;}
.stages{list-style:none;padding:0;margin:0;display:grid;gap:8px;counter-reset:s;}
.stage{border:1px solid var(--rule);border-radius:4px;padding:8px 10px;font-size:.9rem;}
.stage.on{border-color:var(--detector);background:color-mix(in srgb,var(--detector) 8%,transparent);}
.stage .st{font-weight:600;} .stage .sl{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.82rem;margin:.2rem 0 0;word-break:break-word;}
.foot{margin-top:2rem;font-size:.85rem;color:var(--muted);border-top:1px solid var(--rule);padding-top:1rem;}
:focus-visible{outline:2px solid var(--detector);outline-offset:2px;}
@media (prefers-reduced-motion: no-preference){.stage{transition:border-color .15s;}}
.figure .b-edge{stroke:var(--ink);stroke-width:1.1;fill:none;} .figure .b-edge-periodic{stroke:var(--muted);stroke-width:1;stroke-dasharray:5 4;fill:none;}
.figure .b-face{fill:var(--detector);opacity:.07;stroke:var(--detector);stroke-width:.6;}
.figure .b-cube{fill:var(--declaration);opacity:.55;stroke:var(--ink);stroke-width:.8;}
.figure .b-cell{fill:var(--gameboard);} .figure .b-cell-neg{fill:var(--host);}
.figure .b-det{fill:var(--detector);} .figure .b-lamp{fill:var(--host);} .figure .b-body{fill:var(--muted);} .figure .b-blockcell{fill:var(--declaration);}
.figure .b-mark{fill:var(--gameboard);} .figure .b-mark-det{fill:var(--detector);}
.board-wrap{touch-action:none;cursor:grab;user-select:none;} .board-wrap:active{cursor:grabbing;}
.strip{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:.85rem;font-family:ui-monospace,Menlo,Consolas,monospace;}
details.tbl summary{cursor:pointer;font-size:.85rem;color:var(--muted);}
.tbl-scroll{overflow:auto;max-height:320px;border:1px solid var(--rule);border-radius:4px;}
table.rec{border-collapse:collapse;font-size:.8rem;font-family:ui-monospace,Menlo,Consolas,monospace;font-variant-numeric:tabular-nums;width:100%;}
table.rec th,table.rec td{padding:2px 8px;text-align:left;border-bottom:1px solid var(--rule);white-space:nowrap;}
table.rec th{position:sticky;top:0;background:var(--surface);font-weight:600;}
.explor{display:inline-block;padding:2px 8px;border:2px solid var(--pin);color:var(--pin);border-radius:4px;font-weight:700;letter-spacing:.08em;font-size:.8rem;}
"""

SCRIPT_3D = """
(function(){
  var holder=document.querySelector('[data-board-json]'); if(!holder) return;
  var B=JSON.parse(holder.textContent);
  var box=document.querySelector('[data-board]'), svg=box.querySelector('svg'), g=svg.querySelector('[data-board-drawn]');
  var range=box.querySelector('input[data-t]'), out=box.querySelector('[data-t-out]'), strip=box.querySelector('[data-strip]');
  var yawIn=box.querySelector('input[data-yaw]'), pitchIn=box.querySelector('input[data-pitch]');
  var X=Math.max(B.shape[0],1), Y=Math.max(B.shape[1],1), Z=Math.max(B.shape[2],1);
  var W=760, H=460, PAD=36, yaw=0.62, pitch=0.42, t=B.ticks;
  function proj(x,y,z){var cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
    var x1=x*cy-y*sy, y1=x*sy+y*cy; return [x1, -(y1*sp+z*cp), y1*cp-z*sp];}
  var at, scale;
  function fit(){var cs=[],i,j,k; for(i=0;i<2;i++)for(j=0;j<2;j++)for(k=0;k<2;k++) cs.push(proj(i?X:0,j?Y:0,k?Z:0));
    var u0=Math.min.apply(null,cs.map(function(c){return c[0]})), u1=Math.max.apply(null,cs.map(function(c){return c[0]}));
    var v0=Math.min.apply(null,cs.map(function(c){return c[1]})), v1=Math.max.apply(null,cs.map(function(c){return c[1]}));
    scale=Math.min((W-2*PAD)/Math.max(u1-u0,1e-9),(H-2*PAD)/Math.max(v1-v0,1e-9));
    at=function(x,y,z){var p=proj(x,y,z); return [PAD+(p[0]-u0)*scale, PAD+(p[1]-v0)*scale, p[2]];};}
  function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
  function posAt(obj){var p=obj.positions[0][1]; for(var i=0;i<obj.positions.length;i++){if(obj.positions[i][0]<=t) p=obj.positions[i][1];} return p;}
  function countAt(name){var s=B.counts[name]||[], c=0; for(var i=0;i<s.length;i++){if(s[i][0]<=t) c=s[i][1];} return c;}
  function draw(){fit(); var items=[]; var ext=[X,Y,Z];
    B.faces.forEach(function(f){var ax='xyz'.indexOf(f.axis); var others=[0,1,2].filter(function(i){return i!==ax}); var fixed=f.positive?ext[ax]:0;
      var q=[[0,0],[ext[others[0]],0],[ext[others[0]],ext[others[1]]],[0,ext[others[1]]]].map(function(ab){var pt=[0,0,0]; pt[ax]=fixed; pt[others[0]]=ab[0]; pt[others[1]]=ab[1]; return at(pt[0],pt[1],pt[2]);});
      var d=(q[0][2]+q[1][2]+q[2][2]+q[3][2])/4;
      items.push([d-0.5,'<polygon points="'+q.map(function(p){return p[0].toFixed(1)+','+p[1].toFixed(1)}).join(' ')+'" class="b-face"><title>'+esc(f.name)+', an open face, a detector</title></polygon>']);});
    var E=[[[0,0,0],[X,0,0]],[[0,Y,0],[X,Y,0]],[[0,0,Z],[X,0,Z]],[[0,Y,Z],[X,Y,Z]],[[0,0,0],[0,Y,0]],[[X,0,0],[X,Y,0]],[[0,0,Z],[0,Y,Z]],[[X,0,Z],[X,Y,Z]],[[0,0,0],[0,0,Z]],[[X,0,0],[X,0,Z]],[[0,Y,0],[0,Y,Z]],[[X,Y,0],[X,Y,Z]]];
    E.forEach(function(e){var a=at(e[0][0],e[0][1],e[0][2]), b=at(e[1][0],e[1][1],e[1][2]); var axis=[0,1,2].filter(function(i){return e[0][i]!==e[1][i]})[0];
      items.push([(a[2]+b[2])/2-1,'<line x1="'+a[0].toFixed(1)+'" y1="'+a[1].toFixed(1)+'" x2="'+b[0].toFixed(1)+'" y2="'+b[1].toFixed(1)+'" class="'+(B.axes[axis].periodic?'b-edge-periodic':'b-edge')+'"/>']);});
    if(t===B.ticks && B.snapshot.cells.length){var top=1; B.snapshot.cells.forEach(function(c){top=Math.max(top,Math.abs(c[3]))});
      B.snapshot.cells.forEach(function(c){var p=at(c[0]+0.5,c[1]+0.5,c[2]+0.5); var f=Math.min(Math.abs(c[3])/top,1);
        items.push([p[2],'<circle cx="'+p[0].toFixed(1)+'" cy="'+p[1].toFixed(1)+'" r="'+Math.max(1.2+2.2*f,1.2).toFixed(1)+'" class="'+(c[3]<0?'b-cell-neg':'b-cell')+'" opacity="'+(0.25+0.7*f).toFixed(2)+'"><title>('+c[0]+', '+c[1]+', '+c[2]+'): '+c[3]+', GAMEBOARD</title></circle>']);});}
    if(B.probes){var row=null; B.probes.values.forEach(function(v){if(v[0]<=t) row=v;}); if(row){var top2=1; row[1].forEach(function(v){top2=Math.max(top2,Math.abs(v))});
      B.probes.nodes.forEach(function(n,i){var p=at(n[0]+0.5,n[1]+0.5,n[2]+0.5); var v=row[1][i]||0; var f=Math.min(Math.abs(v)/top2,1);
        items.push([p[2],'<circle cx="'+p[0].toFixed(1)+'" cy="'+p[1].toFixed(1)+'" r="'+(2+3*f).toFixed(1)+'" class="'+(v<0?'b-cell-neg':'b-cell')+'" opacity="'+(0.3+0.6*f).toFixed(2)+'"><title>probe ('+n.join(', ')+') at t = '+row[0]+': '+v+', GAMEBOARD</title></circle>']);});}}
    B.cells.forEach(function(c){var cls={detector:'b-det',emitter:'b-lamp',block:'b-blockcell',body:'b-body'}[c.role]||'b-body'; var n0=c.nodes[0]; var cnt=countAt(c.name);
      c.nodes.forEach(function(n){var p=at(n[0]+0.5,n[1]+0.5,n[2]+0.5);
        items.push([p[2],'<rect x="'+(p[0]-3).toFixed(1)+'" y="'+(p[1]-3).toFixed(1)+'" width="6" height="6" class="'+cls+'"><title>'+esc(c.name)+', '+esc(c.role)+' at ('+n.join(', ')+'), DECLARATION; clicks so far '+cnt+', DETECTOR</title></rect>']);});
      if(cnt>0 && n0){var p0=at(n0[0]+0.5,n0[1]+0.5,n0[2]+0.5); items.push([p0[2]-0.02,'<text x="'+(p0[0]+5).toFixed(1)+'" y="'+(p0[1]-4).toFixed(1)+'" class="t-tiny" data-kind="DETECTOR">'+cnt+'</text>']);}});
    B.faces.forEach(function(f){var cnt=countAt(f.name); if(!cnt) return; var ax='xyz'.indexOf(f.axis); var pt=[X/2,Y/2,Z/2]; pt[ax]=f.positive?ext[ax]:0; var p=at(pt[0],pt[1],pt[2]);
      items.push([p[2]-0.6,'<text x="'+p[0].toFixed(1)+'" y="'+(p[1]+(f.positive?14:-14)).toFixed(1)+'" class="t-small" text-anchor="middle" data-kind="DETECTOR">'+esc(f.name)+' '+cnt+'</text>']);});
    B.objects.forEach(function(o){var n=posAt(o); var size=o.side?[o.side,o.side,o.side]:o.span; var org=o.side?n.slice():[n[0]-((size[0]-1)>>1),n[1]-((size[1]-1)>>1),n[2]-((size[2]-1)>>1)];
      var c=[]; [0,size[0]].forEach(function(dx){[0,size[1]].forEach(function(dy){[0,size[2]].forEach(function(dz){c.push(at(org[0]+dx,org[1]+dy,org[2]+dz));});});});
      [[0,1,3,2],[4,5,7,6],[0,1,5,4],[2,3,7,6],[0,2,6,4],[1,3,7,5]].forEach(function(f){var q=f.map(function(i){return c[i]}); var d=(q[0][2]+q[1][2]+q[2][2]+q[3][2])/4;
        items.push([d,'<polygon points="'+q.map(function(p){return p[0].toFixed(1)+','+p[1].toFixed(1)}).join(' ')+'" class="b-cube"><title>'+esc(o.name)+' at ('+n.join(', ')+') from its line, GAMEBOARD</title></polygon>']);});});
    B.marks.forEach(function(m){if(m[0]>t) return; var p=at(m[2]+0.5,m[3]+0.5,m[4]+0.5); var age=Math.max(0,Math.min(t-m[0],40));
      items.push([p[2]+0.01,'<circle cx="'+p[0].toFixed(1)+'" cy="'+p[1].toFixed(1)+'" r="2.6" class="'+(m[5]==='DETECTOR'?'b-mark-det':'b-mark')+'" opacity="'+(0.9-0.02*age).toFixed(2)+'"><title>'+esc(m[1])+' at ('+m[2]+', '+m[3]+', '+m[4]+'), t = '+m[0]+', '+m[5]+'</title></circle>']);});
    items.sort(function(a,b){return b[0]-a[0]}); g.innerHTML=items.map(function(i){return i[1]}).join('');
    if(out) out.textContent=String(t);
    if(strip){var parts=[]; var bk=B.books; if(bk.transit.length&&t>=1){var r=Math.min(t,bk.transit.length)-1; bk.families.forEach(function(f,i){parts.push('<span><span class="n" data-kind="GAMEBOARD" data-source="run.json: transit_content">'+esc(f)+' in transit '+bk.transit[r][i]+'</span>'+(bk.measured[r]?', <span class="n" data-kind="GAMEBOARD" data-source="run.json: measured_content">measured '+bk.measured[r][i]+'</span>':'')+'</span>');});}
      strip.innerHTML=parts.join('');}}
  if(range){range.addEventListener('input',function(){t=parseInt(range.value,10); draw();});}
  box.querySelectorAll('[data-step]').forEach(function(b){b.addEventListener('click',function(){t=Math.max(0,Math.min(B.ticks,t+parseInt(b.getAttribute('data-step'),10))); if(range) range.value=String(t); draw();});});
  if(yawIn){yawIn.addEventListener('input',function(){yaw=parseFloat(yawIn.value); draw();});}
  if(pitchIn){pitchIn.addEventListener('input',function(){pitch=parseFloat(pitchIn.value); draw();});}
  var drag=null; svg.addEventListener('pointerdown',function(e){drag=[e.clientX,e.clientY,yaw,pitch]; svg.setPointerCapture(e.pointerId);});
  svg.addEventListener('pointermove',function(e){if(!drag) return; yaw=drag[2]+(e.clientX-drag[0])*0.01; pitch=Math.max(-1.5,Math.min(1.5,drag[3]+(e.clientY-drag[1])*0.01)); if(yawIn) yawIn.value=yaw.toFixed(2); if(pitchIn) pitchIn.value=pitch.toFixed(2); draw();});
  svg.addEventListener('pointerup',function(){drag=null;}); svg.addEventListener('pointercancel',function(){drag=null;});
  draw();
})();
"""

SCRIPT = """
(function(){
  document.querySelectorAll('[data-net]').forEach(function(box){
    var range=box.querySelector('input[type=range]'), out=box.querySelector('[data-out]'), svg=box.querySelector('svg');
    if(!range||!svg) return;
    function apply(){var t=parseInt(range.value,10); if(out) out.textContent=String(t);
      svg.querySelectorAll('[data-tick]').forEach(function(el){el.style.visibility=(parseInt(el.getAttribute('data-tick'),10)>t)?'hidden':'visible';});}
    range.addEventListener('input',apply); apply();
  });
  document.querySelectorAll('[data-stairs]').forEach(function(box){
    var sel=box.querySelector('select'); if(!sel) return;
    function apply(){box.querySelectorAll('.stair-series').forEach(function(el){el.hidden=(el.getAttribute('data-series')!==sel.value);});}
    sel.addEventListener('change',apply); apply();
  });
  document.querySelectorAll('[data-stepper]').forEach(function(box){
    var range=box.querySelector('input[type=range]'), stages=box.querySelectorAll('.stage'); if(!range) return;
    function apply(){var k=parseInt(range.value,10); stages.forEach(function(el,i){el.classList.toggle('on',i===k); el.style.opacity=(i<=k)?'1':'.45';});}
    range.addEventListener('input',apply); apply();
  });
})();
"""


def badge(kind: str) -> str:
    return f'<span class="badge k-{kind}">{kind}</span>'


def number_row(label: str, value: str, kind: str, source: str) -> str:
    return (
        f'<dt data-ref="label">{escape(label)}</dt>'
        f'<dd><span class="n" data-kind="{kind}" data-source="{escape(source, quote=True)}">{escape(value)}</span>{badge(kind)}</dd>'
    )


def run_card(run: RunRecord, role: str) -> str:
    rows = "".join(number_row(n.label, n.value, n.kind, n.source) for n in head_numbers(run))
    return (
        f'<section class="run"><h3 data-ref="run">{escape(role)}: <span class="ref">{escape(run.name)}</span></h3>'
        f'<p class="note" data-ref="folder">read from <span class="ref">{escape(str(run.folder))}</span></p><dl class="nums">{rows}</dl></section>'
    )


def legend() -> str:
    items = "".join(f"<li>{badge(kind)}<span>{escape(KIND_WORDS[kind])}</span></li>" for kind in KINDS)
    return f'<ul class="legend">{items}</ul>'


def table_html(fig: dict[str, Any], key: str) -> str:
    """A panel's table: every cell one labelled number (DESIGN_3D.md 6.3)."""
    rows = fig.get("rows", [])
    if not rows:
        return ""
    head = "".join(f"<th>{escape(h)}</th>" for h in fig.get("head", []))
    body = []
    for row in rows:
        body.append(
            "<tr>"
            + "".join(
                f'<td><span class="n" data-kind="{kind}" data-source="{escape(source, quote=True)}">{escape(value)}</span></td>'
                for value, kind, source in row
            )
            + "</tr>"
        )
    return (
        f'<details class="tbl" id="tbl-{key}"><summary>the lines, as a table (<span class="n" data-kind="HOST" data-source="the count of rows">{len(rows)}</span> rows)</summary>'
        f'<div class="tbl-scroll"><table class="rec"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div></details>'
    )


def board_html(panel: Panel) -> str:
    """The 3-D board: the step control, the view's two angles, the pre-rendered
    picture, the books' strip and the board's data as one JSON element."""
    board = panel.figure["board"]
    ticks = int(board["ticks"])
    data = json.dumps(board, separators=(",", ":"))
    return (
        "<div data-board>"
        f'<div class="control"><label for="t-{panel.key}">the interval t</label>'
        f'<button type="button" data-step="-1" aria-label="one interval back" data-ref="control">-1</button>'
        f'<input id="t-{panel.key}" type="range" min="0" max="{ticks}" value="{ticks}" step="1" data-t>'
        f'<button type="button" data-step="1" aria-label="one interval forward" data-ref="control">+1</button>'
        f'<span>t = <span class="n" data-kind="GAMEBOARD" data-source="run.json: completed_ticks (the record\'s ordering)" data-t-out>{ticks}</span>{badge("GAMEBOARD")}</span></div>'
        f'<div class="control"><label for="yaw-{panel.key}">turn</label><input id="yaw-{panel.key}" type="range" min="-3.2" max="3.2" value="0.62" step="0.02" data-yaw>'
        f'<label for="pitch-{panel.key}">tilt</label><input id="pitch-{panel.key}" type="range" min="-1.5" max="1.5" value="0.42" step="0.02" data-pitch><span class="note">or drag the board</span></div>'
        f'<div class="fig board-wrap">{figure(panel.figure)}</div>'
        '<div class="strip" data-strip data-ref="books"></div>'
        f'<script type="application/json" data-board-json>{data.replace("</", "<\\/")}</script>'
        "</div>"
    )


def panel_html(panel: Panel, exploratory: bool = False) -> str:
    classes = ["panel"]
    if panel.key in WIDE:
        classes.append("wide")
    if (
        panel.key == "gameboard"
        or panel.key.startswith("board")
        or (panel.numbers and all(n.kind == "GAMEBOARD" for n in panel.numbers))
    ):
        classes.append("diag")
    parts = [f'<article class="{" ".join(classes)}" id="p-{panel.key}">']
    eyebrow = "GAMEBOARD, a diagnostic" if "diag" in classes else f"Layer {panel.layer}"
    if exploratory:
        eyebrow = "EXPLORATORY, never a result; " + eyebrow
    parts.append(f'<div class="eyebrow" data-ref="layer">{escape(eyebrow)}</div>')
    parts.append(f'<h3 data-ref="title">{escape(panel.title)}</h3>')
    if panel.algebra:
        parts.append('<blockquote class="alg">')
        for sentence, ref in panel.algebra:
            parts.append(
                f'<p data-ref="algebra">{escape(sentence)} <span class="ref" data-ref="{escape(ref, quote=True)}">({escape(ref)})</span></p>'
            )
        parts.append("</blockquote>")
    if panel.missing:
        parts.append(
            f'<div class="missing" data-ref="missing">Not recorded by these two runs: {escape(panel.missing)}.</div>'
        )
    else:
        fig = panel.figure
        kind = fig.get("kind")
        if kind == "cube_net":
            ticks = fig["ticks"]
            parts.append(
                f'<div data-net><div class="control"><label for="net-{panel.key}">the clicks up to the tick</label>'
                f'<input id="net-{panel.key}" type="range" min="{ticks[0]}" max="{ticks[-1]}" value="{ticks[-1]}" step="1">'
                f'<span class="n" data-kind="DETECTOR" data-source="events.jsonl: click.tick" data-out>{ticks[-1]}</span>{badge("DETECTOR")}</div>'
                f'<div class="fig">{figure(fig)}</div></div>'
            )
        elif kind == "staircase":
            options = "".join(
                f'<option value="{escape(s["name"], quote=True)}">{escape(s["name"])}</option>'
                for s in fig["series"]
            )
            parts.append(
                f'<div data-stairs><div class="control"><label for="stairs-{panel.key}">the set</label><select id="stairs-{panel.key}" data-ref="set">{options}</select></div>'
                f'<div class="fig">{figure(fig)}</div></div>'
            )
        elif kind == "stages":
            stages = fig["stages"]
            items = []
            for stage in stages:
                lines = "".join(
                    f'<p class="sl"><span class="n" data-kind="{stage["kind"]}" data-source="{escape(stage["source"], quote=True)}">{escape(line)}</span></p>'
                    for line in stage["lines"]
                )
                items.append(
                    f'<li class="stage"><div class="st">{escape(stage["title"])} {badge(stage["kind"])}</div>{lines}</li>'
                )
            parts.append(
                f'<div data-stepper><div class="control"><label for="step-{panel.key}">the record\'s life, step by step</label>'
                f'<input id="step-{panel.key}" type="range" min="0" max="{len(stages) - 1}" value="{len(stages) - 1}" step="1"></div>'
                f'<ol class="stages">{"".join(items)}</ol></div>'
            )
        elif kind == "board3d":
            parts.append(board_html(panel))
        elif kind == "table":
            parts.append(table_html(fig, panel.key))
        elif fig:
            drawn = figure(fig)
            if drawn:
                parts.append(f'<div class="fig">{drawn}</div>')
        if panel.numbers:
            parts.append(
                '<dl class="nums">'
                + "".join(number_row(n.label, n.value, n.kind, n.source) for n in panel.numbers)
                + "</dl>"
            )
    if panel.note:
        parts.append(f'<p class="note" data-ref="note">{escape(panel.note)}</p>')
    sources = sorted({n.source for n in panel.numbers})
    if sources:
        parts.append(
            '<div class="sources">read from: '
            + "; ".join(f'<span class="ref" data-ref="src">{escape(s)}</span>' for s in sources)
            + "</div>"
        )
    parts.append("</article>")
    return "".join(parts)


def page_html(light: RunRecord, detector: RunRecord, panels: list[Panel]) -> str:
    parts = [
        "<title>The Algebra Visualizer</title>",
        f"<style>{CSS}</style>",
        '<div class="wrap">',
        '<header class="head">',
        "<h1>The Algebra Visualizer</h1>",
        '<p class="lede">One page in three layers, read from two runs\' records alone: the geometry that is the algebra, how it produces the physics, and the clicks. '
        "Every number carries its kind; nothing here is computed by the page, pinned, or compared with nature. "
        '<span class="ref" data-ref="design">docs/designs/algebra_visualizer/DESIGN.md</span>; the algebra quoted from <span class="ref" data-ref="algebra">docs/ALGEBRA.md</span>.</p>',
        legend(),
        '<div class="runs">',
        run_card(light, "Run 1, a light world"),
        run_card(detector, "Run 2, a world with a detector and clicks"),
        "</div></header>",
    ]
    for layer, (title, lede) in LAYERS.items():
        own = [p for p in panels if p.layer == layer]
        parts.append(
            f'<section class="layer" id="layer-{layer}"><div class="layer-head"><div class="layer-n" data-ref="layer">{layer}</div><div><h2>{escape(title)}</h2><p class="lede">{escape(lede)}</p></div></div>'
        )
        parts.append(legend())
        parts.append('<div class="panels">' + "".join(panel_html(p) for p in own) + "</div></section>")
    parts.append(
        '<footer class="foot"><p>A picture here is a diagnostic in every case; it is never compared with nature. Only a detector\'s reading is a measurement: a click, '
        "a count between clicks on the detector's own record, a ratio of such counts. A GameBoard reading is the host's view of the board. "
        "The page reads the record and computes no physics: no rule of the law is evaluated, no table of the engine is loaded, no record is stepped again; "
        "the only arithmetic is an exact difference or ratio of two recorded integers, labelled CONVERSION.</p></footer>"
    )
    parts.append("</div>")
    parts.append(f"<script>{SCRIPT}</script>")
    return "\n".join(parts)


def page_html_run(run: RunRecord, panels: list[Panel]) -> str:
    """The 3-D page of one run in the owner's three layers (DESIGN_3D.md)."""
    explor = run.exploratory
    title = ("EXPLORATORY: " if explor else "") + f"Algebra 3-D, {run.name}"
    heading = ("EXPLORATORY: " if explor else "") + f"The Algebra Visualizer in 3-D: {run.name}"
    rows = "".join(number_row(n.label, n.value, n.kind, n.source) for n in head_numbers_run(run))
    parts = [
        f"<title>{escape(title)}</title>",
        f"<style>{CSS}</style>",
        '<div class="wrap">',
        '<header class="head">',
        (
            '<p><span class="explor" data-ref="exploratory">EXPLORATORY</span> <span class="note">an exploratory run: its page is a reading of its record and never a result</span></p>'
            if explor
            else ""
        ),
        f'<h1 data-ref="title">{escape(heading)}</h1>',
        '<p class="lede" data-ref="lede">One run in the owner\'s three layers, read from its record alone: the algebra, the GameBoard as the Inside in 3-D, and the clicks as the Outside. '
        "Every number carries its kind and its source; nothing here is computed by the page beyond a sum, a difference or a ratio of recorded integers, nothing is pinned, nothing is compared with nature. "
        "Neither engine records the board's state per Node per interval: the board draws only what the record writes and says so on its face. "
        '<span class="ref" data-ref="design">docs/designs/algebra_visualizer/DESIGN_3D.md</span>; the algebra quoted from <span class="ref" data-ref="algebra">docs/ALGEBRA.md</span>.</p>',
        legend(),
        '<div class="runs">',
        f'<section class="run"><h3 data-ref="run">The run: <span class="ref">{escape(run.name)}</span></h3>'
        f'<p class="note" data-ref="folder">read from <span class="ref">{escape(str(run.folder))}</span></p><dl class="nums">{rows}</dl></section>',
        "</div></header>",
    ]
    for layer, (ltitle, lede) in LAYERS_RUN.items():
        own = [p for p in panels if p.layer == layer]
        parts.append(
            f'<section class="layer" id="layer-{layer}"><div class="layer-head"><div class="layer-n" data-ref="layer">{layer}</div><div><h2>{escape(ltitle)}</h2><p class="lede" data-ref="lede">{escape(lede)}</p></div></div>'
        )
        parts.append(legend())
        parts.append(
            '<div class="panels">' + "".join(panel_html(p, explor) for p in own) + "</div></section>"
        )
    parts.append(
        '<footer class="foot"><p>A picture of the board is a diagnostic in every case; it is never compared with nature. Only a detector\'s reading is a measurement: a click, '
        "a count between clicks on the detector's own record, a ratio of such counts. A GameBoard reading is the host's view of the board. "
        "The page reads the record and computes no physics: no rule of the law is evaluated, no table of the engine is loaded, no record is stepped again, no block is interpolated between two of its lines; "
        "the only arithmetic is a sum, a difference or a ratio of recorded integers, labelled as its inputs are.</p></footer>"
    )
    parts.append("</div>")
    parts.append(f"<script>{SCRIPT}</script>")
    parts.append(f"<script>{SCRIPT_3D}</script>")
    return "\n".join(parts)


def load_one(folder: Path) -> RunRecord:
    """One run folder (`run.json` in it, or in its `run/`), with the register
    of its world where `REGISTERS` names one by the folder's name."""
    if not (folder / "run.json").exists() and (folder / "run" / "run.json").exists():
        folder = folder / "run"
    name = folder.parent.name if folder.name == "run" else folder.name
    register, block = register_of(name)
    return load_run(folder, register, block)


def build_run(run: RunRecord) -> list[Panel]:
    _board, board_panels = build_layer(run)
    return build_run_panels(run, board_panels)


def is_run_folder(path: Path) -> bool:
    return (path / "run.json").exists() or (path / "run" / "run.json").exists()


def run_folder(runs: Path, name: str) -> Path:
    nested = runs / name / "run"
    return nested if nested.exists() else runs / name


def register_of(name: str) -> tuple[Path | None, str | None]:
    entry = REGISTERS.get(name)
    if entry is None:
        return None, None
    return ROOT / entry[0], entry[1]


def load_pair(runs: Path, light_name: str, detector_name: str) -> tuple[RunRecord, RunRecord]:
    light_register, light_block = register_of(light_name)
    detector_register, detector_block = register_of(detector_name)
    light = load_run(run_folder(runs, light_name), light_register, light_block)
    detector = load_run(run_folder(runs, detector_name), detector_register, detector_block)
    return light, detector


def print_rows(panels: list[Panel]) -> None:
    for key, label, value, kind, source in as_rows(panels):
        print(f"{kind:<11} {key:<10} {label}: {value}  [{source}]")
    for panel in panels:
        if panel.missing:
            print(f"{'(none)':<11} {panel.key:<10} not recorded: {panel.missing}")
        rows = panel.figure.get("rows") if panel.figure.get("kind") == "table" else None
        if rows:
            print(
                f"{'(table)':<11} {panel.key:<10} {len(rows)} rows of labelled cells (the page's table)"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "runs",
        type=Path,
        help="a run folder (one run.json: the 3-D page of one run) or the runs directory of the first page (one folder per world, <name>/run)",
    )
    parser.add_argument("--light", default="c_measured", help="the light world's folder name")
    parser.add_argument("--detector", default="slits_low", help="the detector world's folder name")
    parser.add_argument(
        "--render", type=Path, default=None, help="write the page to this file (headless without it)"
    )
    args = parser.parse_args(argv)
    try:
        if is_run_folder(args.runs):
            run = load_one(args.runs)
            print(
                f"{'(engine)':<11} {run.name:<10} {run.engine}"
                + ("  EXPLORATORY" if run.exploratory else "")
            )
            panels = build_run(run)
            page = None if args.render is None else page_html_run(run, panels)
        else:
            light, detector = load_pair(args.runs, args.light, args.detector)
            panels = build_panels(light, detector)
            page = None if args.render is None else page_html(light, detector, panels)
    except MissingRun as refused:
        print(str(refused), file=sys.stderr)
        return 2
    if page is None:
        print_rows(panels)
        return 0
    args.render.write_text(page, encoding="utf-8")
    print(f"wrote {args.render} ({args.render.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
