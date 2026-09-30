"""The look's page builder, a diagnostic (docs/ENGINE.md #6-how-to-run-a-world): one self-contained HTML page from a look file written by `tools/look/record.py` and, if the world's folder holds one, its blind expectation file, the look embedded gzip-compressed and base64-encoded and inflated by the browser's own DecompressionStream at load, so that a look of many frames fits one page with every number untouched. The page shows the GameBoard as cubes (a folded axis as a plane), one frame per interval with a slider and play and nothing between frames, the reading's window marked on the slider; whole quanta as dots sized by the square root of the count (a hole, a count below 0, a hollow dot), the wave as the glow of the Node's cube, a field as grey mist, the detectors' Nodes as rings that flash the interval their count rises; the detectors' report as a bar chart with the dashed blind curve behind it, labelled blind, the one measurement; graphs over the intervals beside the board (the total count per family, the count, the form, the field and the tension at a named Node, the pace's minimum), every one labelled "GameBoard reading" as the board is in its corner; the world's files' numbers listed beside frame 0, the world as laid. The family roles come from the file's rows and never from the look: a family that holds nothing is matter, the holder of the sign is light, a holder of the content is a field; a further family that holds nothing is drawn in the same colour, dashed. Every number on the page is the look's (the world's files' and the engine's arrays') or the blind file's; the page computes nothing but the totals its graphs draw, and draws no curve, surface or interpolation between Nodes. The page's own layout (every colour and size) stands in the one block at the top of the template's style and nowhere else.

The blind file, optional, `{"expected": {detector name: count, ...} or [one count per detector in the look's order], "family": the family the curve is of, "window": [first interval, last interval], "watch": {"detector": name, "count": the one number to watch}}`, every key optional.

    python tools/look/page.py <world>.look.json [--blind <world>.blind.json] [--out <world>.look.html]
"""

from __future__ import annotations

import argparse
import base64
import gzip
import json
from pathlib import Path
from typing import Any

from event_universe.loader.derived import CONTENT, SIGN

MATTER, LIGHT, FIELD = "matter", "light", "field"
CDN_THREE = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"


def roles(families: list[dict[str, Any]]) -> dict[str, dict[str, object]]:
    """The family roles from the file's rows: a family that holds nothing is matter, the holder of the sign is light, a holder of the content is a field; every further family that holds nothing is matter drawn dashed."""
    found: dict[str, dict[str, object]] = {}
    seen = False
    for family in families:
        held = family.get("held")
        role = LIGHT if held == SIGN else FIELD if held == CONTENT else MATTER
        found[str(family["name"])] = {"role": role, "dashed": role == MATTER and seen}
        seen = seen or role == MATTER
    return found


def embedded(value: object) -> str:
    """A value as compact JSON safe inside a script element."""
    return json.dumps(value, separators=(",", ":")).replace("</", "<\\/")


def packed(value: object) -> str:
    """A value as compact JSON, gzip-compressed (the same bytes for the same value) and base64-encoded, for the page to inflate at load: a look of many frames in one page."""
    data = json.dumps(value, separators=(",", ":")).encode("utf-8")
    return base64.b64encode(gzip.compress(data, compresslevel=9, mtime=0)).decode("ascii")


def page(look: dict[str, Any], blind: dict[str, Any] | None) -> str:
    """The page's HTML from the look and the blind expectation, if any."""
    if not isinstance(look, dict) or "frames" not in look or "families" not in look:
        raise ValueError("the look file must hold the frames and the families (tools/look/record.py)")
    if blind is not None and not isinstance(blind, dict):
        raise ValueError("the blind file must be an object of expected, family, window and watch")
    world = str(look.get("world", "world")).split(".")[0].replace("_", " ")
    title = f"{world[:1].upper()}{world[1:]} look"
    return (
        TEMPLATE.replace("{{TITLE}}", title)
        .replace("{{THREE}}", CDN_THREE)
        .replace("{{LOOK}}", packed(look))
        .replace("{{ROLES}}", embedded(roles(look["families"])))
        .replace("{{BLIND}}", embedded(blind))
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("look", type=Path, help="the look file (<world>.look.json)")
    parser.add_argument("--blind", type=Path, default=None, help="the blind expectation file")
    parser.add_argument("--out", type=Path, default=None, help="the page (<world>.look.html)")
    args = parser.parse_args(argv)
    look = json.loads(args.look.read_text(encoding="utf-8"))
    blind = json.loads(args.blind.read_text(encoding="utf-8")) if args.blind else None
    target: Path = args.out or args.look.with_suffix(".html")
    target.write_text(page(look, blind), encoding="utf-8")
    print(json.dumps({"look": args.look.name, "page": str(target), "bytes": target.stat().st_size}))


TEMPLATE = """<title>{{TITLE}}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* The page's own layout: every colour and size of the page stands in this one block and nowhere else. */
:root {
  --bg: #f6f5f0; --panel: #ffffff; --fg: #1e2027; --muted: #6a6e78; --line: #d8d6ce; --board: #ecebe5;
  --cube: #cfcdc5; --matter: #2f6fd0; --light: #c07f0a; --field: #7a7e87; --ring: #2c2f36; --flash: #000000;
  --blind: #6a6e78; --focus: #2f6fd0; --window: rgba(47, 111, 208, 0.16);
  --font-body: "IBM Plex Sans", system-ui, sans-serif; --font-mono: "IBM Plex Mono", ui-monospace, monospace;
  --text: 14px; --small: 12px; --title: 20px; --gap: 12px; --pad: 14px; --radius: 6px; --gutter: 16px;
  --side-min: 300px; --board-height: 520px; --graph-width: 360; --graph-height: 84; --graph-pad: 6;
  --cube-size: 0.78; --dot-radius: 0.38; --dot-floor: 0.08; --dot-offset: 0.22; --glow: 0.9;
  --mist-size: 1.02; --mist-opacity: 0.3; --mist-power: 0.5; --bar-length: 0.9; --bar-thickness: 0.07;
  --ring-radius: 0.6; --ring-tube: 0.05; --flash-scale: 1.4; --plane-opacity: 0.12;
  --camera-fov: 38; --camera-distance: 1.15; --camera-far: 12; --camera-tilt: 22; --camera-turn: -28;
  --orbit-rate: 0.006; --zoom-rate: 0.0012; --zoom-step: 0.85; --frames-per-second: 12; --line-width: 1.6;
  --label-size: 1.4;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #14161a; --panel: #1b1e24; --fg: #e9e7df; --muted: #9a9ea8; --line: #2e323a; --board: #0f1114;
  --cube: #2b2e35; --matter: #5f97ea; --light: #f0b445; --field: #a3a7ae; --ring: #d9d7d0; --flash: #ffffff;
  --blind: #9a9ea8; --focus: #5f97ea; --window: rgba(95, 151, 234, 0.2); color-scheme: dark;
} }
:root[data-theme="dark"] {
  --bg: #14161a; --panel: #1b1e24; --fg: #e9e7df; --muted: #9a9ea8; --line: #2e323a; --board: #0f1114;
  --cube: #2b2e35; --matter: #5f97ea; --light: #f0b445; --field: #a3a7ae; --ring: #d9d7d0; --flash: #ffffff;
  --blind: #9a9ea8; --focus: #5f97ea; --window: rgba(95, 151, 234, 0.2); color-scheme: dark;
}
* { box-sizing: border-box; }
body { margin: 0; padding-inline: var(--gutter); padding-block: var(--pad); background: var(--bg); color: var(--fg); font: var(--text)/1.45 var(--font-body); }
h1 { font-size: var(--title); margin: 0; font-weight: 600; text-wrap: balance; }
h2 { font-size: var(--text); margin: 0; font-weight: 600; }
header { display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--gap); margin-bottom: var(--gap); }
header .verdict { font-family: var(--font-mono); color: var(--muted); }
.page { display: grid; grid-template-columns: repeat(auto-fit, minmax(var(--side-min), 1fr)); gap: var(--gap); align-items: start; }
.wide { grid-column: 1 / -1; }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: var(--pad); min-width: 0; }
.stage { position: relative; height: var(--board-height); border-radius: var(--radius); overflow: hidden; background: var(--board); border: 1px solid var(--line); }
.stage canvas { display: block; width: 100%; height: 100%; touch-action: none; }
.corner { position: absolute; top: var(--gap); left: var(--gap); font: 500 var(--small)/1.2 var(--font-mono); color: var(--muted); pointer-events: none; }
.zoom { position: absolute; top: var(--gap); right: var(--gap); display: flex; gap: 4px; }
.hover { position: absolute; display: none; max-width: min(320px, 90%); padding: 8px 10px; background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); font: var(--small)/1.4 var(--font-mono); pointer-events: none; white-space: pre-line; }
.layers { display: flex; flex-wrap: wrap; gap: 6px var(--gap); margin-top: var(--gap); font-size: var(--small); }
.layers label { display: inline-flex; align-items: center; gap: 4px; }
.swatch { display: inline-block; width: 10px; height: 10px; border-radius: 50%; border: 2px solid var(--fg); }
.swatch.dashed { border-style: dashed; }
.time { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; align-items: center; gap: var(--gap); margin-top: var(--gap); }
.track { position: relative; min-width: 0; }
.track input { width: 100%; margin: 0; position: relative; z-index: 1; }
.track .window { position: absolute; top: 25%; height: 50%; background: var(--window); border-radius: var(--radius); }
.frame { font-family: var(--font-mono); font-variant-numeric: tabular-nums; min-width: 9ch; text-align: right; }
.lines { font: var(--small)/1.4 var(--font-mono); color: var(--muted); margin-top: 6px; min-height: 1.4em; }
button, select, input[type=number] { font: inherit; color: var(--fg); background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 4px 10px; }
button:focus-visible, select:focus-visible, input:focus-visible { outline: 2px solid var(--focus); outline-offset: 1px; }
.stack { display: grid; gap: var(--gap); }
.graph { display: grid; gap: 2px; }
.graph .caption { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px var(--gap); font-size: var(--small); color: var(--muted); }
.graph .caption b { color: var(--fg); font-weight: 600; }
.graph svg { width: 100%; height: auto; display: block; }
.legend { display: flex; flex-wrap: wrap; gap: 4px var(--gap); font-size: var(--small); }
.legend i { display: inline-block; width: 14px; height: 0; border-top: 2px solid; vertical-align: middle; margin-right: 4px; }
.legend i.dashed { border-top-style: dashed; }
.picker { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: var(--small); }
.picker input { width: 5ch; padding: 3px 6px; }
dl { display: grid; grid-template-columns: max-content minmax(0, 1fr); gap: 2px var(--gap); margin: 0; font-size: var(--small); }
dt { color: var(--muted); } dd { margin: 0; font-family: var(--font-mono); overflow-wrap: anywhere; }
table { border-collapse: collapse; width: 100%; font-size: var(--small); }
th, td { text-align: left; padding: 3px 6px; border-bottom: 1px solid var(--line); vertical-align: top; font-variant-numeric: tabular-nums; }
th { color: var(--muted); font-weight: 600; }
td.num { font-family: var(--font-mono); }
.scroll { overflow-x: auto; }
.measure { border-color: var(--fg); }
.watch { font-family: var(--font-mono); font-size: var(--small); margin-top: 6px; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
<script id="look" type="application/gzip+base64">{{LOOK}}</script>
<script id="roles" type="application/json">{{ROLES}}</script>
<script id="blind" type="application/json">{{BLIND}}</script>
<header>
  <h1 id="title"></h1>
  <span class="verdict" id="verdict"></span>
</header>
<div class="page">
  <section class="panel wide">
    <div class="stage" id="stage">
      <canvas id="board"></canvas>
      <div class="corner">GameBoard reading</div>
      <div class="zoom"><button type="button" id="zoom-in" aria-label="closer">+</button><button type="button" id="zoom-out" aria-label="farther">&minus;</button></div>
      <div class="hover" id="hover"></div>
    </div>
    <div class="layers" id="layers"></div>
    <div class="time">
      <button type="button" id="play">Play</button>
      <div class="track"><div class="window" id="window" hidden></div><input type="range" id="slider" min="0" value="0" step="1" aria-label="the interval"></div>
      <div class="frame" id="frame"></div>
    </div>
    <div class="lines" id="lines"></div>
  </section>
  <section class="panel measure">
    <h2>Measurement: the detectors' report</h2>
    <div class="picker" id="measure-picker"></div>
    <div class="graph" id="measure"></div>
    <div class="watch" id="watch"></div>
  </section>
  <section class="panel">
    <h2>The world's numbers</h2>
    <div id="numbers"></div>
  </section>
  <section class="panel">
    <h2>Over the intervals, at a Node</h2>
    <div class="picker" id="node-picker"></div>
    <div class="stack" id="graphs"></div>
  </section>
  <section class="panel wide">
    <h2>The books at the run's end</h2>
    <div class="scroll" id="books"></div>
  </section>
</div>
<script src="{{THREE}}"></script>
<script>
'use strict';
/* The look is embedded gzip-compressed and base64-encoded, so that a look of many frames fits one page; the browser's own DecompressionStream inflates it at load and the numbers are the look's, untouched. */
async function inflated(id) {
  const text = document.getElementById(id).textContent.trim();
  const bytes = Uint8Array.from(atob(text), c => c.charCodeAt(0));
  const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
  return JSON.parse(await new Response(stream).text());
}
(async () => {
const LOOK = await inflated('look');
const ROLES = JSON.parse(document.getElementById('roles').textContent);
const BLIND = JSON.parse(document.getElementById('blind').textContent) || {};
const root = document.documentElement;
const token = name => getComputedStyle(root).getPropertyValue(name).trim();
const size = name => parseFloat(token(name));
const byId = id => document.getElementById(id);
const [X, Y, Z] = LOOK.shape, N = X * Y * Z, T = LOOK.frames.length - 1;
const FAMILIES = LOOK.families, QUANTA = FAMILIES.filter(f => f.quanta), HELD = FAMILIES.filter(f => !f.quanta);
const AXES = ['x', 'y', 'z'], PARTS = ['x', 'y', 'z', 'xx', 'yy', 'zz', 'xy', 'xz', 'yz'];
const colourOf = name => token('--' + ROLES[name].role);
const esc = text => String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
const format = value => typeof value === 'number' ? value.toLocaleString('en-US') : String(value);

/* The arrays of a frame, dense nested lists or the nonzero Nodes alone, as flat x-major arrays. */
function arrayOf(value) {
  const out = new Float64Array(N);
  if (!value) return out;
  if (Array.isArray(value)) { let i = 0; for (const plane of value) for (const row of plane) for (const v of row) out[i++] = v; }
  else value.at.forEach((k, j) => { out[k] = value.values[j]; });
  return out;
}
const cache = new Map();
function frameOf(t) {
  if (cache.has(t)) return cache.get(t);
  const frame = LOOK.frames[t], out = {};
  for (const f of FAMILIES) {
    const row = frame.families[f.name] || {}, a = {};
    if (f.quanta) { for (const key of ['now', 'second', 'count', 'remainder', 'sense', 'form']) a[key] = arrayOf(row[key]); a.pace = row.pace; }
    else { a.level = arrayOf(row.level); a.parts = (row.parts || []).map(arrayOf); }
    out[f.name] = a;
  }
  cache.set(t, out);
  return out;
}
const peak = a => { let m = 0; for (let i = 0; i < a.length; i++) { const v = Math.abs(a[i]); if (v > m) m = v; } return m; };
const sum = a => { let s = 0; for (let i = 0; i < a.length; i++) s += a[i]; return s; };
const MOST = {}, TOTALS = {};
for (const f of FAMILIES) { MOST[f.name] = { now: 0, count: 0, level: 0, part: 0 }; if (f.quanta) TOTALS[f.name] = new Float64Array(T + 1); }
for (let t = 0; t <= T; t++) {
  const fr = frameOf(t);
  for (const f of FAMILIES) {
    const a = fr[f.name], m = MOST[f.name];
    if (f.quanta) { m.now = Math.max(m.now, peak(a.now), peak(a.second)); m.count = Math.max(m.count, peak(a.count)); TOTALS[f.name][t] = sum(a.count); }
    else { m.level = Math.max(m.level, peak(a.level)); for (const p of a.parts) m.part = Math.max(m.part, peak(p)); }
  }
}
const indexOf = (x, y, z) => (x * Y + y) * Z + z;
const nodeOf = i => [Math.floor(i / (Y * Z)), Math.floor(i / Z) % Y, i % Z];
const reportsAt = {};
for (const frame of LOOK.frames) for (const line of frame.lines) if (line.event === 'click') {
  const byFamily = reportsAt[line.detector] || (reportsAt[line.detector] = {});
  (byFamily[line.family] || (byFamily[line.family] = [])).push(line.tick);
}
const WINDOW = Array.isArray(BLIND.window) && BLIND.window.length === 2 ? BLIND.window : null;

/* The board: cubes, dots, glow, mist, bars, rings, the box's edges and a folded axis's plane. */
const stage = byId('stage'), canvas = byId('board');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(window.devicePixelRatio || 1);
const scene = new THREE.Scene();
const extent = Math.max(X, Y, Z);
const camera = new THREE.PerspectiveCamera(size('--camera-fov'), 1, size('--cube-size'), extent * size('--camera-far'));
const view = { turn: size('--camera-turn') * Math.PI / 180, tilt: size('--camera-tilt') * Math.PI / 180, distance: extent * size('--camera-distance') };
function placeCamera() {
  const { turn, tilt, distance } = view;
  camera.position.set(distance * Math.cos(tilt) * Math.sin(turn), distance * Math.sin(tilt), distance * Math.cos(tilt) * Math.cos(turn));
  camera.lookAt(0, 0, 0);
}
function fit() {
  view.distance = 1; placeCamera(); camera.updateMatrixWorld();
  const vertical = Math.tan(camera.fov * Math.PI / 360), horizontal = vertical * camera.aspect;
  let needed = 0;
  for (const sx of [-1, 1]) for (const sy of [-1, 1]) for (const sz of [-1, 1]) {
    const corner = new THREE.Vector3(sx * X / 2, sy * Y / 2, sz * Z / 2).applyMatrix4(camera.matrixWorldInverse), depth = corner.z + 1;
    needed = Math.max(needed, depth + Math.abs(corner.x) / horizontal, depth + Math.abs(corner.y) / vertical);
  }
  view.distance = needed * size('--camera-distance'); placeCamera();
}
const hemisphere = new THREE.HemisphereLight(0xffffff, 0x000000, 1), sun = new THREE.DirectionalLight(0xffffff, 0.5);
sun.position.set(1, 2, 3);
scene.add(hemisphere, sun);
const position = i => { const [x, y, z] = nodeOf(i); return new THREE.Vector3(x - (X - 1) / 2, y - (Y - 1) / 2, z - (Z - 1) / 2); };
const matrix = new THREE.Matrix4(), quaternion = new THREE.Quaternion(), scale = new THREE.Vector3(), colour = new THREE.Color(), tint = new THREE.Color();
const hidden = new THREE.Matrix4().makeScale(0, 0, 0);
const layers = {};
const cubeSide = size('--cube-size');
const cubes = new THREE.InstancedMesh(new THREE.BoxGeometry(cubeSide, cubeSide, cubeSide), new THREE.MeshLambertMaterial({ color: 0xffffff }), N);
for (let i = 0; i < N; i++) cubes.setMatrixAt(i, matrix.makeTranslation(...position(i).toArray()));
for (let i = 0; i < N; i++) cubes.setColorAt(i, colour.set(0xffffff));
scene.add(cubes);
function striped(hex) {
  const c = document.createElement('canvas'), bands = 8; c.width = c.height = 64;
  const g = c.getContext('2d'); g.fillStyle = hex;
  for (let b = 0; b < bands; b += 2) g.fillRect(0, b * c.height / bands, c.width, c.height / bands);
  const texture = new THREE.CanvasTexture(c); texture.needsUpdate = true; return texture;
}
const dots = {};
QUANTA.forEach((f, k) => {
  const hex = colourOf(f.name), dashed = ROLES[f.name].dashed;
  const full = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 16, 12), dashed ? new THREE.MeshLambertMaterial({ map: striped(hex), transparent: true, alphaTest: 0.5 }) : new THREE.MeshLambertMaterial({ color: hex }), N);
  const hollow = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), new THREE.MeshBasicMaterial({ color: hex, wireframe: true }), N);
  dots[f.name] = { full, hollow, offset: (k - (QUANTA.length - 1) / 2) * size('--dot-offset') };
  scene.add(full, hollow);
  layers[f.name + ' dots'] = { on: true, objects: [full, hollow] };
  layers[f.name + ' glow'] = { on: true, objects: [] };
});
const mists = {}, bars = {};
for (const f of HELD) {
  const mist = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({ color: colourOf(f.name), transparent: true, opacity: size('--mist-opacity'), depthWrite: false }), N);
  mists[f.name] = mist; scene.add(mist);
  layers[f.name + ' mist'] = { on: true, objects: [mist] };
  if (f.parts.length >= 3) {
    bars[f.name] = AXES.map(() => new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshLambertMaterial({ color: colourOf(f.name) }), N));
    scene.add(...bars[f.name]);
    layers[f.name + ' tension bars'] = { on: false, objects: bars[f.name] };
  }
}
const ringCapacity = LOOK.detectors.reduce((n, d) => n + (d.body === null ? d.nodes.length : Math.max(...LOOK.frames.map(fr => fr.bodies[d.body].length))), 0);
const rings = new THREE.InstancedMesh(new THREE.TorusGeometry(size('--ring-radius'), size('--ring-tube'), 8, 32), new THREE.MeshBasicMaterial({ color: 0xffffff }), Math.max(ringCapacity, 1));
scene.add(rings);
layers['detector rings'] = { on: true, objects: [rings] };
const box = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(X, Y, Z)), new THREE.LineBasicMaterial({ color: 0xffffff }));
const faces = new THREE.Group();
AXES.forEach((axis, a) => {
  if (LOOK.boundary[axis] !== 'open') return;
  for (const side of [-1, 1]) {
    const half = [X, Y, Z].map(e => e / 2), corners = [];
    for (const [u, v] of [[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]]) {
      const p = [0, 0, 0]; p[a] = side * half[a]; p[(a + 1) % 3] = u * half[(a + 1) % 3]; p[(a + 2) % 3] = v * half[(a + 2) % 3];
      corners.push(new THREE.Vector3(...p));
    }
    faces.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(corners), new THREE.LineBasicMaterial({ color: 0xffffff })));
  }
});
const plane = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: size('--plane-opacity'), side: THREE.DoubleSide, depthWrite: false }));
plane.visible = LOOK.folded.some(Boolean);
if (plane.visible) {
  const span = [X, Y, Z].map((e, a) => LOOK.folded[a] ? cubeSide : e), folded = LOOK.folded.indexOf(true);
  if (folded === 2) plane.scale.set(span[0], span[1], 1);
  else if (folded === 1) { plane.rotation.x = Math.PI / 2; plane.scale.set(span[0], span[2], 1); }
  else { plane.rotation.y = Math.PI / 2; plane.scale.set(span[2], span[1], 1); }
}
const labels = new THREE.Group(), labelSize = size('--label-size');
AXES.forEach((axis, a) => {
  const c = document.createElement('canvas'), px = 64; c.width = c.height = px;
  const g = c.getContext('2d'); g.font = `${px / 2}px ${token('--font-mono')}`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#ffffff'; g.fillText(axis, px / 2, px / 2);
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthTest: false }));
  const p = [0, 0, 0]; p[a] = [X, Y, Z][a] / 2 + labelSize;
  sprite.position.set(...p); sprite.scale.setScalar(labelSize); labels.add(sprite);
});
scene.add(box, faces, plane, labels);
layers['the box and its axes'] = { on: true, objects: [box, faces, plane, labels] };

function themed() {
  scene.background = new THREE.Color(token('--board'));
  box.material.color.set(token('--line')); plane.material.color.set(token('--muted'));
  faces.children.forEach(line => line.material.color.set(token('--fg')));
  labels.children.forEach(sprite => sprite.material.color.set(token('--muted')));
  hemisphere.color.set(token('--fg')); hemisphere.groundColor.set(token('--board'));
  for (const f of QUANTA) { const hex = colourOf(f.name); if (!ROLES[f.name].dashed) dots[f.name].full.material.color.set(hex); else dots[f.name].full.material.map = striped(hex); dots[f.name].hollow.material.color.set(hex); }
  for (const f of HELD) { mists[f.name].material.color.set(colourOf(f.name)); (bars[f.name] || []).forEach(b => b.material.color.set(colourOf(f.name))); }
}

/* One frame drawn: no state between frames, every mark from the frame's arrays alone. */
let t = 0, playing = null, named = null;
function draw() {
  const frame = LOOK.frames[t], fr = frameOf(t), glow = size('--glow');
  const base = new THREE.Color(token('--cube'));
  for (let i = 0; i < N; i++) {
    colour.copy(base);
    for (const f of QUANTA) {
      if (!layers[f.name + ' glow'].on || !MOST[f.name].now) continue;
      const a = fr[f.name], strength = glow * Math.max(Math.abs(a.now[i]), Math.abs(a.second[i])) / MOST[f.name].now;
      colour.add(tint.set(colourOf(f.name)).multiplyScalar(strength));
    }
    colour.r = Math.min(colour.r, 1); colour.g = Math.min(colour.g, 1); colour.b = Math.min(colour.b, 1);
    cubes.setColorAt(i, colour);
  }
  cubes.instanceColor.needsUpdate = true;
  const radius = size('--dot-radius'), floor = size('--dot-floor');
  for (const f of QUANTA) {
    const { full, hollow, offset } = dots[f.name], count = fr[f.name].count, most = Math.sqrt(MOST[f.name].count) || 1;
    for (let i = 0; i < N; i++) {
      const c = count[i], r = c ? Math.max(floor, radius * Math.sqrt(Math.abs(c)) / most) : 0;
      const p = position(i); p.y += offset;
      matrix.compose(p, quaternion, scale.setScalar(r));
      full.setMatrixAt(i, c > 0 ? matrix : hidden); hollow.setMatrixAt(i, c < 0 ? matrix : hidden);
    }
    full.instanceMatrix.needsUpdate = true; hollow.instanceMatrix.needsUpdate = true;
  }
  const mistSize = size('--mist-size'), power = size('--mist-power'), barLength = size('--bar-length'), thickness = size('--bar-thickness');
  for (const f of HELD) {
    const a = fr[f.name], mist = mists[f.name], most = MOST[f.name].level;
    for (let i = 0; i < N; i++) {
      const s = most ? mistSize * Math.pow(Math.abs(a.level[i]) / most, power) : 0;
      mist.setMatrixAt(i, s ? matrix.compose(position(i), quaternion, scale.setScalar(s)) : hidden);
    }
    mist.instanceMatrix.needsUpdate = true;
    if (bars[f.name]) bars[f.name].forEach((bar, axis) => {
      const part = a.parts[f.parts[1] + axis], most = MOST[f.name].part;
      for (let i = 0; i < N; i++) {
        const length = most && part ? barLength * Math.abs(part[i]) / most : 0;
        scale.set(thickness, thickness, thickness); if (length) scale.setComponent(axis, length);
        bar.setMatrixAt(i, length ? matrix.compose(position(i), quaternion, scale) : hidden);
      }
      bar.instanceMatrix.needsUpdate = true;
    });
  }
  let slot = 0;
  const ringColour = new THREE.Color(token('--ring')), flashColour = new THREE.Color(token('--flash')), flashScale = size('--flash-scale');
  for (const d of LOOK.detectors) {
    const nodes = d.body === null ? d.nodes : frame.bodies[d.body];
    const flashing = frame.lines.some(line => line.event === 'click' && line.detector === d.name);
    for (const [x, y, z] of nodes) {
      rings.setMatrixAt(slot, matrix.compose(position(indexOf(x, y, z)), quaternion, scale.setScalar(flashing ? flashScale : 1)));
      rings.setColorAt(slot, flashing ? flashColour : ringColour); slot++;
    }
  }
  for (; slot < rings.count; slot++) rings.setMatrixAt(slot, hidden);
  rings.instanceMatrix.needsUpdate = true; if (rings.instanceColor) rings.instanceColor.needsUpdate = true;
  for (const layer of Object.values(layers)) layer.objects.forEach(o => { o.visible = layer.on; });
  renderer.render(scene, camera);
  byId('slider').value = t;
  byId('frame').textContent = t === 0 ? 'laid, 0 / ' + T : 'interval ' + t + ' / ' + T;
  const counts = {};
  for (const line of frame.lines) counts[line.event] = (counts[line.event] || 0) + 1;
  const clicks = frame.lines.filter(line => line.event === 'click').map(line => line.detector + ': ' + line.family);
  byId('lines').textContent = t === 0 ? 'The world as laid: the bodies\\' declared counts, the levels of the mode file, every held row at its start.'
    : Object.entries(counts).map(([event, n]) => n + ' ' + event + (n === 1 ? '' : 's')).join(', ') + (clicks.length ? ' (' + [...new Set(clicks)].join(', ') + ')' : '') || 'no line this interval';
  drawMeasure();
  moveCursors();
}

/* The view: drag turns the board, the wheel and the two buttons bring it closer or farther. */
let dragging = null;
canvas.addEventListener('pointerdown', e => { dragging = { x: e.clientX, y: e.clientY }; canvas.setPointerCapture(e.pointerId); });
canvas.addEventListener('pointerup', e => { dragging = null; canvas.releasePointerCapture(e.pointerId); });
canvas.addEventListener('pointermove', e => {
  if (dragging) {
    const rate = size('--orbit-rate'), limit = Math.PI / 2 - rate;
    view.turn -= (e.clientX - dragging.x) * rate; view.tilt = Math.max(-limit, Math.min(limit, view.tilt + (e.clientY - dragging.y) * rate));
    dragging = { x: e.clientX, y: e.clientY }; placeCamera(); renderer.render(scene, camera); hover(null);
  } else hover(e);
});
canvas.addEventListener('pointerleave', () => hover(null));
canvas.addEventListener('wheel', e => { e.preventDefault(); zoom(Math.exp(e.deltaY * size('--zoom-rate'))); }, { passive: false });
function zoom(factor) { view.distance = Math.max(size('--cube-size'), view.distance * factor); placeCamera(); renderer.render(scene, camera); }
byId('zoom-in').addEventListener('click', () => zoom(size('--zoom-step')));
byId('zoom-out').addEventListener('click', () => zoom(1 / size('--zoom-step')));
canvas.addEventListener('click', e => { const i = pick(e); if (i !== null) { named = nodeOf(i); AXES.forEach((axis, a) => { byId('node-' + axis).value = named[a]; }); drawGraphs(); } });
new ResizeObserver(() => {
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); fit(); renderer.render(scene, camera);
}).observe(stage);

/* The hover: a Node's numbers as they are, the remainder as r / W_c, the sense as an arrow. */
const raycaster = new THREE.Raycaster(), pointer = new THREE.Vector2();
function pick(e) {
  const r = canvas.getBoundingClientRect();
  pointer.set((e.clientX - r.left) / r.width * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  raycaster.setFromCamera(pointer, camera);
  const hit = raycaster.intersectObject(cubes)[0];
  return hit ? hit.instanceId : null;
}
function hover(e) {
  const panel = byId('hover'), i = e ? pick(e) : null;
  if (i === null) { panel.style.display = 'none'; return; }
  const fr = frameOf(t), lines = ['Node [' + nodeOf(i).join(', ') + ']  (GameBoard reading)'];
  for (const f of FAMILIES) {
    const a = fr[f.name];
    if (f.quanta) {
      const parts = ['level ' + format(a.now[i])];
      if (MOST[f.name].now && a.second[i]) parts.push('second ' + format(a.second[i]));
      parts.push('count ' + format(a.count[i]));
      if (t > 0 && f.wall) parts.push('r / W_c = ' + (a.remainder[i] / f.wall).toFixed(2));
      if (a.sense[i]) parts.push('sense ' + (a.sense[i] > 0 ? '\\u21bb' : '\\u21ba') + ' ' + format(a.sense[i]));
      lines.push(f.name + ': ' + parts.join(', '));
    } else {
      const parts = a.parts.map((p, k) => PARTS[k] + ' ' + format(p[i]));
      lines.push(f.name + ': level ' + format(a.level[i]) + (parts.length ? '; ' + parts.join(', ') : ''));
    }
  }
  panel.textContent = lines.join('\\n');
  panel.style.display = 'block';
  const r = stage.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
  panel.style.left = Math.min(x + 12, r.width - panel.offsetWidth - 4) + 'px';
  panel.style.top = Math.min(y + 12, r.height - panel.offsetHeight - 4) + 'px';
}

/* The layers, one switch each. */
const layerBox = byId('layers');
for (const [name, layer] of Object.entries(layers)) {
  const family = FAMILIES.find(f => name.startsWith(f.name + ' '));
  const label = document.createElement('label'), input = document.createElement('input');
  input.type = 'checkbox'; input.checked = layer.on; input.id = 'layer-' + name.replace(/\\W+/g, '-');
  input.addEventListener('change', () => { layer.on = input.checked; draw(); });
  label.append(input);
  if (family) { const swatch = document.createElement('i'); swatch.className = 'swatch' + (ROLES[family.name].dashed ? ' dashed' : ''); swatch.style.borderColor = colourOf(family.name); swatch.style.background = name.endsWith(' dots') ? colourOf(family.name) : 'transparent'; label.append(swatch); }
  label.append(' ' + name + (family ? ' (' + ROLES[family.name].role + ')' : ''));
  layerBox.append(label);
}

/* The time: one frame per interval, a slider, play; the reading's window marked on the slider. */
const slider = byId('slider'); slider.max = T;
slider.addEventListener('input', () => { t = Number(slider.value); draw(); });
byId('play').addEventListener('click', () => {
  if (playing) { clearInterval(playing); playing = null; byId('play').textContent = 'Play'; return; }
  if (t >= T) t = 0;
  byId('play').textContent = 'Pause';
  playing = setInterval(() => { if (t >= T) { clearInterval(playing); playing = null; byId('play').textContent = 'Play'; return; } t++; draw(); }, 1000 / size('--frames-per-second'));
});
document.addEventListener('keydown', e => { if (e.target.tagName === 'INPUT' && e.target.type !== 'range') return; if (e.key === 'ArrowRight' && t < T) { t++; draw(); } if (e.key === 'ArrowLeft' && t > 0) { t--; draw(); } });
if (WINDOW && T) { const w = byId('window'); w.hidden = false; w.style.left = (WINDOW[0] / T * 100) + '%'; w.style.width = (Math.max(0, WINDOW[1] - WINDOW[0]) / T * 100) + '%'; w.title = 'the reading\\'s window: intervals ' + WINDOW[0] + ' to ' + WINDOW[1]; }

/* The graphs, inline SVG: polylines through the frames' values, nothing between frames. */
const svgText = (text, x, y, anchor) => `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size('--small') * 0.75}" font-family="${esc(token('--font-mono'))}" fill="${token('--muted')}">${esc(text)}</text>`;
function graph(container, title, series, kind) {
  const W = size('--graph-width'), H = size('--graph-height'), pad = size('--graph-pad'), left = pad * 8, frames = series[0] ? series[0].values.length : 0;
  let low = Infinity, high = -Infinity;
  for (const s of series) for (const v of s.values) { if (v < low) low = v; if (v > high) high = v; }
  if (!series.length || !isFinite(low)) { container.innerHTML = `<div class="caption"><b>${esc(title)}</b><span>nothing to draw</span></div>`; return; }
  if (low === high) { low -= 1; high += 1; }
  const px = i => left + (frames > 1 ? i / (frames - 1) : 0) * (W - left - pad), py = v => pad + (high - v) / (high - low) * (H - 2 * pad);
  let body = `<rect x="${left}" y="${pad}" width="${W - left - pad}" height="${H - 2 * pad}" fill="none" stroke="${token('--line')}"/>`;
  if (low < 0 && high > 0) body += `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}" stroke-dasharray="2 3"/>`;
  body += svgText(format(high), left - 3, pad + size('--small') * 0.3, 'end') + svgText(format(low), left - 3, H - pad, 'end');
  for (const s of series) body += `<polyline fill="none" stroke="${s.colour}" stroke-width="${size('--line-width')}" ${s.dashed ? 'stroke-dasharray="5 4"' : ''} stroke-linejoin="round" points="${Array.from(s.values, (v, i) => px(i).toFixed(1) + ',' + py(v).toFixed(1)).join(' ')}"/>`;
  body += `<line class="cursor" x1="${px(t)}" x2="${px(t)}" y1="${pad}" y2="${H - pad}" stroke="${token('--fg')}" stroke-width="1"/>`;
  const legend = series.map(s => `<span><i class="${s.dashed ? 'dashed' : ''}" style="border-color:${s.colour}"></i>${esc(s.name)}</span>`).join('');
  container.innerHTML = `<div class="caption"><b>${esc(title)}</b><span>${kind}</span></div><div class="legend">${legend}</div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(title)}">${body}</svg><div class="caption now"></div>`;
  container.dataset.px = JSON.stringify([left, W - pad, frames]);
  container.series = series;
}
function moveCursors() {
  document.querySelectorAll('.graph').forEach(g => {
    if (!g.series) return;
    const [left, right, frames] = JSON.parse(g.dataset.px), x = left + (frames > 1 ? t / (frames - 1) : 0) * (right - left);
    g.querySelectorAll('.cursor').forEach(c => { c.setAttribute('x1', x); c.setAttribute('x2', x); });
    const now = g.querySelector('.now'); if (now) now.innerHTML = g.series.map(s => `<span>${esc(s.name)} <b>${format(s.values[t])}</b></span>`).join('');
  });
}
const seriesOf = (family, name, values, dashed) => ({ name, values, colour: colourOf(family), dashed: !!dashed });
function drawGraphs() {
  const box = byId('graphs'); box.innerHTML = '';
  const at = named ? indexOf(...named) : null, reading = 'GameBoard reading';
  const add = (title, series) => { const g = document.createElement('div'); g.className = 'graph'; box.append(g); graph(g, title, series, reading); };
  add('The total count per family', QUANTA.map(f => seriesOf(f.name, f.name, TOTALS[f.name], ROLES[f.name].dashed)));
  if (at === null) return;
  const over = key => f => seriesOf(f.name, f.name, Float64Array.from({ length: T + 1 }, (_, k) => frameOf(k)[f.name][key][at]), ROLES[f.name].dashed);
  add('The count at the Node', QUANTA.map(over('count')));
  add('The form at the Node', QUANTA.map(over('form')));
  add('The field at the Node', HELD.map(f => seriesOf(f.name, f.name, Float64Array.from({ length: T + 1 }, (_, k) => frameOf(k)[f.name].level[at]))));
  add('The pace\\'s minimum', QUANTA.map(f => seriesOf(f.name, f.name, Float64Array.from({ length: T + 1 }, (_, k) => frameOf(k)[f.name].pace), ROLES[f.name].dashed)));
  const tension = [];
  for (const f of HELD) {
    const first = f.parts.length >= 3 ? f.parts[1] : 0, names = f.parts.length >= 3 ? PARTS.slice(3, 6) : PARTS.slice(0, 3);
    if (f.parts.length >= 2) names.forEach((part, k) => tension.push(seriesOf(f.name, f.name + ' ' + part, Float64Array.from({ length: T + 1 }, (_, i) => (frameOf(i)[f.name].parts[first + k] || [])[at] || 0), k > 0)));
  }
  if (tension.length) add('The tension at the Node', tension);
  moveCursors();
}
const picker = byId('node-picker');
picker.innerHTML = 'Node ' + AXES.map(axis => `<label>${axis} <input type="number" id="node-${axis}" min="0" max="${[X, Y, Z][AXES.indexOf(axis)] - 1}" value="0"></label>`).join(' ') + ' <span>(click a cube to pick it)</span>';
AXES.forEach(axis => byId('node-' + axis).addEventListener('change', () => { named = AXES.map(a => Math.max(0, Math.min([X, Y, Z][AXES.indexOf(a)] - 1, Number(byId('node-' + a).value) || 0))); drawGraphs(); }));
if (LOOK.bodies.length && LOOK.bodies[0].nodes.length) { named = LOOK.bodies[0].nodes[0].slice(); AXES.forEach((axis, a) => { byId('node-' + axis).value = named[a]; }); }

/* The measurement, drawn once: the detectors' reports as bars, the dashed blind curve behind them. */
const measurePicker = byId('measure-picker'), select = document.createElement('select'); select.id = 'measure-family';
for (const f of QUANTA) { const o = document.createElement('option'); o.value = f.name; o.textContent = f.name; select.append(o); }
const reporting = QUANTA.find(f => f.name === BLIND.family) || QUANTA.find(f => ROLES[f.name].role === 'light') || QUANTA[0];
if (reporting) select.value = reporting.name;
select.addEventListener('change', drawMeasure);
measurePicker.append('Family ', select, document.createTextNode(WINDOW ? ' within the window ' + WINDOW[0] + ' to ' + WINDOW[1] : ' over every interval'));
function reported(detector, family) {
  const ticks = (reportsAt[detector] || {})[family] || [];
  return ticks.filter(k => k <= t && (!WINDOW || (k >= WINDOW[0] && k <= WINDOW[1]))).length;
}
function drawMeasure() {
  const family = select.value, detectors = LOOK.detectors, box = byId('measure');
  const expected = detectors.map((d, k) => Array.isArray(BLIND.expected) ? BLIND.expected[k] : BLIND.expected && typeof BLIND.expected === 'object' ? BLIND.expected[d.name] : undefined);
  const counts = detectors.map(d => reported(d.name, family));
  const W = size('--graph-width'), H = size('--graph-height') * 1.5, pad = size('--graph-pad'), left = pad * 8, bottom = pad * 3;
  const high = Math.max(1, ...counts, ...expected.filter(v => typeof v === 'number'));
  const slot = (W - left - pad) / Math.max(detectors.length, 1), py = v => pad + (high - v) / high * (H - pad - bottom);
  let body = `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}"/>` + svgText(format(high), left - 3, pad + size('--small') * 0.3, 'end') + svgText('0', left - 3, py(0), 'end');
  if (expected.some(v => typeof v === 'number')) {
    const points = expected.map((v, k) => typeof v === 'number' ? (left + slot * (k + 0.5)).toFixed(1) + ',' + py(v).toFixed(1) : null).filter(Boolean).join(' ');
    body += `<polyline fill="none" stroke="${token('--blind')}" stroke-width="${size('--line-width')}" stroke-dasharray="5 4" points="${points}"/>` + svgText('blind', W - pad, pad + size('--small') * 0.3, 'end');
  }
  const every = Math.max(1, Math.ceil(detectors.length / 12));
  detectors.forEach((d, k) => {
    const x = left + slot * (k + 0.5), w = Math.max(1, slot * 0.6);
    body += `<rect x="${(x - w / 2).toFixed(1)}" y="${py(counts[k]).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(counts[k])).toFixed(1)}" fill="${colourOf(family)}"><title>${esc(d.name)}: ${counts[k]} reported</title></rect>`;
    if (k % every === 0) body += svgText(d.name, x, H - pad, 'middle');
  });
  box.innerHTML = `<div class="caption"><b>The reports of ${esc(family)}</b><span>measurement</span></div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="the detectors' report">${body}</svg>`;
  const watch = BLIND.watch && typeof BLIND.watch === 'object' ? BLIND.watch : null;
  byId('watch').textContent = watch ? `${watch.detector}: ${reported(watch.detector, family)} reported, the blind ${format(watch.count)}` : '';
}

/* The world's numbers as the files hold them, and the books at the end. */
function numbers() {
  const row = (k, v) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`;
  let html = '<dl>' + row('world', LOOK.world) + row('shape', LOOK.shape.join(' x ')) + row('faces', AXES.map(a => a + ' ' + LOOK.boundary[a]).join(', ')) + row('folded', AXES.filter((a, k) => LOOK.folded[k]).join(', ') || 'none') + row('face depth', LOOK.face_depth)
    + row('Gamma (the Node clock)', format(LOOK.node_clock)) + row('T (the quantum action)', format(LOOK.quantum_action)) + row('the largest integer', LOOK.largest_integer) + row('A (the amplitude bound)', format(LOOK.amplitude_bound))
    + row('intervals', format(LOOK.ticks) + ' recorded; the world declares ' + format(LOOK.declared_ticks)) + '</dl>';
  html += '<div class="scroll"><table><thead><tr><th>family</th><th>pair</th><th>holds</th><th>divisor</th><th>parts</th><th>reads</th><th>W_c</th><th>role</th></tr></thead><tbody>'
    + FAMILIES.map(f => `<tr><td>${esc(f.name)}</td><td class="num">[${f.pair.join(', ')}]</td><td>${f.held || 'nothing'}</td><td class="num">${f.divisor === null ? '' : f.divisor}</td><td class="num">${f.parts.join(' + ')}</td><td>${f.reads.join(', ')}</td><td class="num">${f.wall === null ? '' : format(f.wall)}</td><td><i class="swatch${ROLES[f.name].dashed ? ' dashed' : ''}" style="border-color:${colourOf(f.name)}"></i> ${ROLES[f.name].role}</td></tr>`).join('') + '</tbody></table></div>';
  html += '<div class="scroll"><table><thead><tr><th>body</th><th>family</th><th>Nodes</th><th>declared count</th><th>holds</th></tr></thead><tbody>'
    + LOOK.bodies.map(b => `<tr><td class="num">${b.number}</td><td>${esc(b.family)}</td><td class="num">${b.nodes.length}</td><td class="num">${format(b.declared)}</td><td>${Object.entries(b.holds).map(([k, v]) => k + ' ' + format(v.reduce((s, c) => s + c, 0))).join(', ')}</td></tr>`).join('') + '</tbody></table></div>';
  html += '<div class="scroll"><table><thead><tr><th>detector</th><th>Nodes</th><th>reads</th></tr></thead><tbody>'
    + LOOK.detectors.map(d => `<tr><td>${esc(d.name)}</td><td class="num">${d.body === null ? d.nodes.length : 'the body\\'s'}</td><td>${d.body === null ? 'its Nodes' : 'body ' + d.body}</td></tr>`).join('') + '</tbody></table></div>';
  if (Object.keys(BLIND).length) html += '<dl>' + row('blind expectation', JSON.stringify(BLIND)) + '</dl>';
  byId('numbers').innerHTML = html;
  const books = LOOK.books || {}, keys = Object.keys(Object.values(books)[0] || {});
  byId('books').innerHTML = keys.length ? '<div class="scroll"><table><thead><tr><th>family</th>' + keys.map(k => `<th>${esc(k.replace('_', ' '))}</th>`).join('') + '</tr></thead><tbody>'
    + Object.entries(books).map(([name, book]) => `<tr><td>${esc(name)}</td>` + keys.map(k => `<td class="num">${format(book[k])}</td>`).join('') + '</tr>').join('') + '</tbody></table></div>' : '<p>No interval was run.</p>';
}

/* The start: the title, the verdict, the theme, frame 0. */
byId('title').textContent = document.title;
byId('verdict').textContent = LOOK.verdict + (LOOK.reason ? ': ' + LOOK.reason : '') + ' (' + LOOK.label + ')';
function start() { themed(); fit(); numbers(); drawGraphs(); draw(); }
const scheme = window.matchMedia('(prefers-color-scheme: dark)');
scheme.addEventListener('change', start);
new MutationObserver(start).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
start();
})();
</script>
"""


if __name__ == "__main__":
    main()
