"""The torus view, a page tool beside tools/look/eras_page.py in its dark tokens (the owner's word of 2026-10-23: let every Node be shown in three dimensions and the Link's length between them, so one sees how the bang starts, reaches the top and contracts, the time's direction at the Nodes by colour, and the Nodes' content): one self-contained HTML page from the Nodes' log tools/eras.py writes with `--nodes` (`<world>.nodes.jsonl`, one JSON line per interval: X at every Node of the first held row, the Link's length e^U = (X / Gamma)^(1 / (d + 1)) at every Node, the Nodes the fifth act turned this interval, every Node's direction of time and every family's quanta per Node) with the eras log beside it (the header's shape, the volume's course), the clicks log where the run kept one (the instrument bodies' credits, the clicks written) and the world file (the bodies' Nodes and families, the markers). The page places the Nodes of any three-dimensional torus on their lattice with every Link drawn at its own length, the mean of its two Nodes' e^U, the lattice stretching toward the top and shrinking back, each Node coloured by its time's direction (forward or turned, the log's own reading), each Node's marker sized by its content (the quanta of every family at the Node, the numbers on hover), played from the seed by itself on load (a play/pause control, the slider beside it), a stage strip under the view with the bang, the first turns, every top, the contraction, every return and the cut marked at their intervals as the tool read them from the logs, the births and the written clicks ticked on it, and, for every instrument body, one chart of the click rate (the clicks written at its Node per 100 intervals in a running window, counted here from the credits), 1 / e^U at its Node (the clock p_0 / Gamma, the Link's length's inverse) and the light's quanta read at its Node, interval by interval, the ratio the one number the page forms. Plain HTML and inline JS, no library; every number the log's.

python tools/look/torus_page.py <world>.nodes.jsonl --eras <world>.eras.jsonl [--clicks <world>.clicks.jsonl] [--world <world>.json] [--notes notes.md] [--out <world>.torus.html]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

PAGE = Path(__file__).with_name("page.py")
TOKENS = re.search(r":root \{.*?\n\}\n", PAGE.read_text(encoding="utf-8"), re.S)
assert TOKENS is not None, (
    "tools/look/page.py holds the page's tokens, the one block the torus page shares"
)

TEMPLATE = """<meta charset="utf-8">
<title>{{TITLE}}</title>
<style>
{{TOKENS}}
* { box-sizing: border-box; }
body { margin: 0; padding-inline: var(--gutter); padding-block: var(--pad); background: var(--bg); color: var(--fg); font: var(--text)/1.45 var(--font-body); }
h1 { font-size: var(--title); margin: 0; font-weight: 600; }
h2 { font-size: var(--text); margin: 0 0 6px; font-weight: 600; }
header { display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--gap); margin-bottom: var(--gap); }
.verdict { font-family: var(--font-mono); color: var(--muted); }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: var(--pad); margin-bottom: var(--gap); min-width: 0; }
.row { display: flex; flex-wrap: wrap; align-items: center; gap: var(--gap); font-size: var(--small); }
.row input[type=range] { flex: 1 1 240px; }
.row button { font: inherit; color: var(--fg); background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 3px 10px; cursor: pointer; }
.words { font-size: var(--small); color: var(--muted); }
.words b { color: var(--fg); font-weight: 600; }
svg { width: 100%; height: auto; display: block; }
.legend { display: flex; flex-wrap: wrap; gap: 4px var(--gap); font-size: var(--small); }
.legend i { display: inline-block; width: 12px; height: 12px; border-radius: 50%; vertical-align: middle; margin-right: 4px; }
.legend i.line { border-radius: 0; height: 0; border-top: 2px solid; width: 14px; }
.prose { max-width: 90ch; }
summary { cursor: pointer; font-weight: 600; }
.prose p, .prose ul { margin: 0 0 var(--gap); }
.prose h3 { font-size: var(--text); font-weight: 600; margin: var(--gap) 0 6px; }
.prose code { font-family: var(--font-mono); font-size: var(--small); }
</style>
<script id="nodes" type="application/json">{{NODES}}</script>
<script id="course" type="application/json">{{COURSE}}</script>
<script id="bodies" type="application/json">{{BODIES}}</script>
<script id="charts" type="application/json">{{CHARTS}}</script>
<script id="notes" type="application/json">{{NOTES}}</script>
<script id="stages" type="application/json">{{STAGES}}</script>
<header><h1 id="title"></h1><span class="verdict" id="verdict"></span></header>
<section class="panel" id="notes-box" hidden><h2 id="notes-heading">Notes</h2><div class="prose" id="notes-lead"></div></section>
<section class="panel">
  <h2>The torus: every Node, every Link at its own length e^U, the time's direction by colour, the content by size</h2>
  <div class="row"><button id="play">play</button><input type="range" id="at" min="0" value="0"><span class="verdict" id="where"></span></div>
  <div class="row"><label>turn <input type="range" id="yaw" min="0" max="360" value="35"></label><label>tilt <input type="range" id="pitch" min="-90" max="90" value="25"></label></div>
  <div id="legend" class="legend"></div>
  <svg id="torus" viewBox="0 0 1000 760" role="img" aria-label="the torus"></svg>
  <svg id="strip" viewBox="0 0 1000 118" role="img" aria-label="the stages of the run"></svg>
  <div class="words" id="strip-words"></div>
  <div class="words" id="torus-words"></div>
</section>
<section class="panel" id="notes-rest" hidden><details><summary>The notes in full, stage by stage</summary><div class="prose" id="notes-prose"></div></details></section>
<section class="panel" id="charts-box" hidden><h2>At the instrument's Node: the click rate, 1 / e^U and the light's quanta, interval by interval</h2><div id="charts-drawn"></div><div class="words" id="charts-words"></div></section>
<script>
const NODES = JSON.parse(document.getElementById('nodes').textContent);
const COURSE = JSON.parse(document.getElementById('course').textContent);
const BODIES = JSON.parse(document.getElementById('bodies').textContent);
const CHARTS = JSON.parse(document.getElementById('charts').textContent);
const NOTES = JSON.parse(document.getElementById('notes').textContent);
const STAGES = JSON.parse(document.getElementById('stages').textContent);
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const token = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
const [nx, ny, nz] = COURSE.shape, N = nx * ny * nz;
const index = (x, y, z) => (x * ny + y) * nz + z;
const FAMILIES = NODES.length ? Object.keys(NODES[0].quanta) : [];
const FORWARD = token('--field'), TURNED = token('--flash'), LINK = token('--muted'), MARK = token('--light');
const tones = token('--click-tones').split(',').map(s => s.trim());
const familyColour = name => tones[(FAMILIES.indexOf(name) + 1) % tones.length];
document.getElementById('title').textContent = `${COURSE.world.replace('.json', '').replace(/_/g, ' ')}: the torus, interval by interval`;
document.getElementById('verdict').textContent = `${NODES.length} intervals logged, ${N} Nodes on ${nx} x ${ny} x ${nz}, Gamma ${COURSE.gamma}` + (COURSE.refused ? `; REFUSED at ${COURSE.refused.interval}` : '');
const slider = document.getElementById('at'); slider.max = Math.max(0, NODES.length - 1);
function positions(line) {  // every Node placed by the cumulative Link lengths along its three axes from the origin, each Link the mean of its two Nodes' e^U (the log's)
  const L = line.length, pos = new Array(N);
  for (let x = 0; x < nx; x++) for (let y = 0; y < ny; y++) for (let z = 0; z < nz; z++) {
    let px = 0, py = 0, pz = 0;
    for (let k = 0; k < x; k++) px += (L[index(k, y, z)] + L[index(k + 1, y, z)]) / 2;
    for (let k = 0; k < y; k++) py += (L[index(x, k, z)] + L[index(x, k + 1, z)]) / 2;
    for (let k = 0; k < z; k++) pz += (L[index(x, y, k)] + L[index(x, y, k + 1)]) / 2;
    pos[index(x, y, z)] = [px, py, pz];
  }
  return pos;
}
function project(p, yaw, pitch) {
  const a = yaw * Math.PI / 180, b = pitch * Math.PI / 180;
  const x1 = p[0] * Math.cos(a) - p[2] * Math.sin(a), z1 = p[0] * Math.sin(a) + p[2] * Math.cos(a);
  const y2 = p[1] * Math.cos(b) - z1 * Math.sin(b), z2 = p[1] * Math.sin(b) + z1 * Math.cos(b);
  return [x1, y2, z2];
}
const bodyAt = {}; for (const b of BODIES) if (b.nodes.length <= 8) for (const n of b.nodes) bodyAt[index(...n)] = b.family;  // a ring for the bodies of a few Nodes, the clumps and the instruments; a family laid over the board is no marker
function draw() {
  const t = parseInt(slider.value, 10), line = NODES[t]; if (!line) return;
  const yaw = parseFloat(document.getElementById('yaw').value), pitch = parseFloat(document.getElementById('pitch').value);
  const pos = positions(line).map(p => project(p, yaw, pitch));
  const extent = (Math.max(nx, ny, nz) - 1) * Math.max(...NODES.map(l => l.length.reduce((a, b) => a + b, 0) / N)) * 1.3 || 1;  // the run's largest mean Link sets the frame, the lattice filling it at the highest top and small at the seed, so the stretch is seen
  const scale = 620 / extent, cx = 500, cy = 380;
  const mx = pos.reduce((a, p) => a + p[0], 0) / N, my = pos.reduce((a, p) => a + p[1], 0) / N;  // the lattice centred on its own mean, the frame the run's largest
  const sx = p => cx + (p[0] - mx) * scale * 0.9, sy = p => cy - (p[1] - my) * scale * 0.9;
  let body = '';
  const meanL = line.length.reduce((a, b) => a + b, 0) / N;
  for (let x = 0; x < nx; x++) for (let y = 0; y < ny; y++) for (let z = 0; z < nz; z++) {
    const i = index(x, y, z);
    for (const j of [x + 1 < nx ? index(x + 1, y, z) : -1, y + 1 < ny ? index(x, y + 1, z) : -1, z + 1 < nz ? index(x, y, z + 1) : -1]) {
      if (j < 0) continue;
      const len = (line.length[i] + line.length[j]) / 2, w = Math.max(0.4, 1.6 * len / meanL);
      body += `<line x1="${sx(pos[i]).toFixed(1)}" y1="${sy(pos[i]).toFixed(1)}" x2="${sx(pos[j]).toFixed(1)}" y2="${sy(pos[j]).toFixed(1)}" stroke="${LINK}" stroke-width="${w.toFixed(2)}" opacity="0.55"><title>Link length e^U ${len.toFixed(3)}</title></line>`;
    }
  }
  const order = [...Array(N).keys()].sort((a, b) => pos[a][2] - pos[b][2]);
  for (const i of order) {
    const content = FAMILIES.reduce((s, f) => s + Math.abs(line.quanta[f][i]), 0);
    const r = 3 + Math.min(18, Math.sqrt(content) / 12);
    const fill = line.direction[i] > 0 ? FORWARD : TURNED, ring = bodyAt[i] ? `stroke="${familyColour(bodyAt[i])}" stroke-width="2.5"` : `stroke="${token('--bg')}" stroke-width="0.8"`;
    const words = `Node [${Math.floor(i / (ny * nz))}, ${Math.floor(i / nz) % ny}, ${i % nz}]: X ${line.X[i].toLocaleString()}, e^U ${line.length[i].toFixed(3)}, time ${line.direction[i] > 0 ? 'forward' : 'turned'}${line.turned.includes(i) ? ' (turned this interval)' : ''}; ` + FAMILIES.map(f => `${f} ${line.quanta[f][i].toLocaleString()}`).join(', ') + (bodyAt[i] ? `; a body of ${bodyAt[i]}` : '');
    body += `<circle cx="${sx(pos[i]).toFixed(1)}" cy="${sy(pos[i]).toFixed(1)}" r="${r.toFixed(1)}" fill="${fill}" ${ring}><title>${esc(words)}</title></circle>`;
  }
  document.getElementById('torus').innerHTML = body;
  const cursor = document.getElementById('cursor'); if (cursor) { const first = NODES[0].interval, last = NODES[NODES.length - 1].interval, x = 12 + (line.interval - first) / Math.max(1, last - first) * 976; cursor.setAttribute('x1', x.toFixed(1)); cursor.setAttribute('x2', x.toFixed(1)); }
  const row = COURSE.rows[t] || {};
  document.getElementById('where').textContent = `interval ${line.interval}: U ${row.U === undefined ? '' : row.U.toFixed(4)}, the mean Link e^U ${meanL.toFixed(3)}, ${line.turned.length} Nodes turned this interval, ${line.direction.filter(d => d < 0).length} with time turned`;
}
function legend() {
  const marks = [`<span><i style="background:${FORWARD}"></i>time forward</span>`, `<span><i style="background:${TURNED}"></i>time turned (the swap at the top)</span>`, `<span><i class="line" style="border-color:${LINK}"></i>a Link drawn at its length e^U = (X / Gamma)^(1 / 4), the frame the run's largest lattice, so the stretch to the top and the shrink back are seen; its width the length against the mean</span>`];
  for (const f of [...new Set(BODIES.filter(b => b.nodes.length <= 8).map(b => b.family))]) marks.push(`<span><i style="background:transparent;border:2.5px solid ${familyColour(f)}"></i>a body of ${esc(f)}</span>`);
  document.getElementById('legend').innerHTML = marks.join('');
  const tops = COURSE.bangs.map(b => `${b.kind} at ${b.at} (U ${b.U.toFixed(3)})`).join(', ');
  document.getElementById('torus-words').innerHTML = `<b>Read from the log, drawn here</b>: every Node at its place by the cumulative Link lengths from the origin, each Link the mean of its two Nodes' e^U = (X / Gamma)^(1 / 4), the lattice stretching to the top and shrinking back; the Node's colour its direction of time as the eras tool read it (flipped at each of its turns under the fifth act); the marker's size the content, the quanta of every family at the Node (hover for the numbers); a ring the body declared there. ${tops ? 'The volume\\'s course: ' + esc(tops) + '.' : ''}`;
}
let playing = null;
function play() {  // the run plays from the seed by itself on load, one logged interval per frame where the log is short, a few where it is long, back to the seed at the cut
  document.getElementById('play').textContent = 'pause';
  playing = setInterval(() => { let v = parseInt(slider.value, 10) + Math.max(1, Math.round(NODES.length / 600)); if (v > NODES.length - 1) v = 0; slider.value = v; draw(); }, 50);
}
function pause() { clearInterval(playing); playing = null; document.getElementById('play').textContent = 'play'; }
document.getElementById('play').addEventListener('click', () => playing ? pause() : play());
for (const id of ['at', 'yaw', 'pitch']) document.getElementById(id).addEventListener('input', draw);
document.getElementById('at').addEventListener('pointerdown', pause);
function strip() {  // the stage strip: every mark read from the logs by the tool, none typed; the births and the clicks ticked at their intervals; the cursor the frame shown
  if (!NODES.length) return;
  const left = 12, right = 988, first = NODES[0].interval, last = NODES[NODES.length - 1].interval, Y = 56;
  const px = at => left + (at - first) / Math.max(1, last - first) * (right - left);
  let body = `<line x1="${left}" x2="${right}" y1="${Y}" y2="${Y}" stroke="${LINK}" stroke-width="2"/>`;
  const text = (t, x, y, anchor, fill) => `<text x="${x.toFixed(1)}" y="${y}" fill="${fill}" font-size="11" font-family="${token('--font-mono')}" text-anchor="${anchor}">${esc(t)}</text>`;
  for (const b of STAGES.births) body += `<line x1="${px(b).toFixed(1)}" x2="${px(b).toFixed(1)}" y1="${Y}" y2="${Y + 10}" stroke="${familyColour('electron')}" stroke-width="1.5"><title>a birth at ${b}</title></line>`;
  for (const c of STAGES.clicks) body += `<line x1="${px(c).toFixed(1)}" x2="${px(c).toFixed(1)}" y1="${Y - 10}" y2="${Y}" stroke="${MARK}" stroke-width="1.2"><title>a click written at ${c}</title></line>`;
  const rows = [[10, 20], [80, 90], [32, 42], [102, 112]];  // the words above and below the line on two levels each, so neighbouring marks keep apart
  STAGES.marks.forEach((m, k) => { const x = px(m.at), [wy, ny] = rows[k % 4], anchor = k === 0 ? 'start' : k === STAGES.marks.length - 1 ? 'end' : 'middle'; body += `<circle cx="${x.toFixed(1)}" cy="${Y}" r="4" fill="${m.word === 'top' || m.word === 'bang' ? TURNED : FORWARD}"/>` + text(m.word, x, wy, anchor, token('--fg')) + text(m.at, x, ny, anchor, token('--muted')); });
  const now = NODES[parseInt(slider.value, 10)].interval;
  body += `<line id="cursor" x1="${px(now).toFixed(1)}" x2="${px(now).toFixed(1)}" y1="4" y2="114" stroke="${token('--fg')}" stroke-width="1" stroke-dasharray="3 2"/>`;
  document.getElementById('strip').innerHTML = body;
  document.getElementById('strip-words').innerHTML = `<b>The stages, read from the log</b>: ${STAGES.marks.map(m => `${esc(m.word)} at ${m.at}`).join(', ')}; ${STAGES.births.length} births (the ticks below the line, at ${STAGES.births.join(', ') || 'none'}) and ${STAGES.clicks.length} clicks written (the ticks above, at ${STAGES.clicks.join(', ') || 'none'}); the dashed cursor the frame shown. Click the strip to go to an interval.`;
}
document.getElementById('strip').addEventListener('click', e => {
  const box = e.currentTarget.getBoundingClientRect(), f = (e.clientX - box.left) / box.width * 1000, first = NODES[0].interval, last = NODES[NODES.length - 1].interval;
  const at = Math.round(first + (f - 12) / 976 * (last - first)); let k = NODES.findIndex(l => l.interval >= at); if (k < 0) k = NODES.length - 1;
  pause(); slider.value = Math.max(0, k); draw();
});
function chart(box, title, series, xs, options = {}) {
  const W = 1000, H = 300, pad = 16, left = 70;
  let low = Infinity, high = -Infinity;
  for (const s of series) for (const v of s.values) if (v !== null && isFinite(v)) { low = Math.min(low, v); high = Math.max(high, v); }
  if (!isFinite(low)) return;
  if (low === high) { low -= 1; high += 1; }
  const px = i => left + i / Math.max(1, xs.length - 1) * (W - left - pad), py = v => pad + (high - v) / (high - low) * (H - 2 * pad);
  let body = `<rect x="${left}" y="${pad}" width="${W - left - pad}" height="${H - 2 * pad}" fill="none" stroke="${token('--line')}"/>`;
  const label = (text, x, y, anchor) => `<text x="${x}" y="${y}" fill="${token('--muted')}" font-size="11" font-family="${token('--font-mono')}" text-anchor="${anchor}">${esc(text)}</text>`;
  body += label(high.toPrecision(3), left - 4, pad + 5, 'end') + label(low.toPrecision(3), left - 4, H - pad, 'end') + label(xs[0], left, H - 2, 'start') + label(xs[xs.length - 1], W - pad, H - 2, 'end');
  for (const m of options.marks || []) { const i = xs.indexOf(m.at); if (i >= 0) body += `<line x1="${px(i).toFixed(1)}" x2="${px(i).toFixed(1)}" y1="${pad}" y2="${H - pad}" stroke="${token('--fg')}" stroke-dasharray="2 3"/>` + label(m.kind, px(i) + 3, pad + 12, 'start'); }
  for (const s of series) {
    const points = s.values.map((v, i) => v === null || !isFinite(v) ? null : `${px(i).toFixed(1)},${py(v).toFixed(1)}`).filter(Boolean);
    body += `<polyline points="${points.join(' ')}" fill="none" stroke="${s.colour}" stroke-width="1.6" ${s.dashed ? 'stroke-dasharray="4 3"' : ''}/>`;
  }
  const legend = series.map(s => `<span><i class="line ${s.dashed ? 'dashed' : ''}" style="border-color:${s.colour}"></i>${esc(s.name)}</span>`).join('');
  box.innerHTML += `<h2>${esc(title)}</h2><div class="legend">${legend}</div><svg viewBox="0 0 ${W} ${H}">${body}</svg>`;
}
function charts() {
  if (!CHARTS.length) return;
  document.getElementById('charts-box').hidden = false;
  const box = document.getElementById('charts-drawn');  // its own id: 'charts' is the embedded data's script element
  const norm = a => { const m = Math.max(...a.filter(v => v !== null && isFinite(v)).map(Math.abs)) || 1; return a.map(v => v === null ? null : v / m); };
  const words = [];
  for (const c of CHARTS) {
    chart(box, `${c.body} at [${c.node.join(', ')}]: the click rate per 100 intervals, 1 / e^U and the light's quanta, each against its own largest`, [
      {name: `clicks per 100 intervals (largest ${Math.max(...c.rate)})`, values: norm(c.rate), colour: MARK},
      {name: `1 / e^U at the Node (largest ${Math.max(...c.inverse).toFixed(3)}, least ${Math.min(...c.inverse).toFixed(3)})`, values: norm(c.inverse), colour: FORWARD},
      {name: `light's quanta at the Node (largest ${Math.max(...c.light).toLocaleString()})`, values: norm(c.light), colour: TURNED, dashed: true},
    ], c.intervals, {marks: COURSE.bangs});
    words.push(`<b>${esc(c.body)}</b>: ${c.clicks.length} clicks written at ${c.clicks.join(', ')}; by the volume's stages, the rate per 100 intervals ${c.stages.map(s => `${s.name} ${s.rate.toFixed(1)}`).join(', ')}; e^U at the Node ${c.e_top.toFixed(3)} at the top against 1 at the seed, so 1 / e^U falls to ${(1 / c.e_top).toFixed(3)} there; the light's quanta at the Node ${c.light_top.toLocaleString()} at the top against ${c.light_first.toLocaleString()} at the first click.`);
  }
  document.getElementById('charts-words').innerHTML = `<b>What the clock reads</b>: nothing but the light's quanta at its own Node, through the draw; the Link's length enters through the Node's time line (the clock p_0 = Gamma / e^U, the window its own beat in its own intervals). ${words.join(' ')}`;
}
function renderNotes(text) {
  const box = document.getElementById('notes-prose'); box.innerHTML = ''; document.getElementById('notes-box').hidden = false;
  const inline = s => esc(s).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\\*\\*([^*]+)\\*\\*/g, '<b>$1</b>');
  let heading = null, list = false, html = '';
  for (const raw of text.split('\\n')) {
    const line = raw.trim(), head = line.match(/^(#+)\\s+(.*)$/), item = line.match(/^[-*]\\s+(.*)$/);
    if (head) { if (list) { html += '</ul>'; list = false; } if (head[1].length === 1 && heading === null) { heading = head[2]; document.getElementById('notes-heading').innerHTML = inline(heading); continue; } html += `<h3>${inline(head[2])}</h3>`; continue; }
    if (item) { if (!list) { html += '<ul>'; list = true; } html += `<li>${inline(item[1])}</li>`; continue; }
    if (list) { html += '</ul>'; list = false; }
    if (line) html += `<p>${inline(line)}</p>`;
  }
  if (list) html += '</ul>';
  const lead = html.match(/^<p>.*?<\\/p>/);  // the leading paragraph above the view, the rest in full under the view
  document.getElementById('notes-lead').innerHTML = lead ? lead[0] : '';
  box.innerHTML = lead ? html.slice(lead[0].length) : html; document.getElementById('notes-rest').hidden = !box.innerHTML;
}
legend(); draw(); strip(); charts(); if (NOTES) renderNotes(NOTES); if (NODES.length > 1) play();
</script>
"""


def read_log(path: Path) -> list[dict[str, Any]]:
    """The log's lines, one JSON object per line."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def bangs_of(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The volume's tops and returns from the eras log's rows (the weak extrema of the board's volume, the larger top or the deeper return kept where two of a kind follow each other), as tools/look/eras_page.py marks them."""
    found: list[dict[str, Any]] = []
    volumes = [(r["interval"], r["volume"], r["U"]) for r in rows if "volume" in r]
    for i in range(1, len(volumes) - 1):
        p, q, r = volumes[i - 1][1], volumes[i][1], volumes[i + 1][1]
        kind = (
            "top"
            if q >= p and q >= r and (q > p or q > r)
            else "return"
            if q <= p and q <= r and (q < p or q < r)
            else None
        )
        if kind is None:
            continue
        entry = {"kind": kind, "at": volumes[i][0], "volume": q, "U": volumes[i][2]}
        if found and found[-1]["kind"] == kind:
            if (kind == "top" and q > found[-1]["volume"]) or (
                kind == "return" and q < found[-1]["volume"]
            ):
                found[-1] = entry
        else:
            found.append(entry)
    return found


def course_of(eras: list[dict[str, Any]], world: dict[str, Any] | None) -> dict[str, Any]:
    """The course the page marks: the header's world, shape and Gamma, per interval the first held row's U and volume, the tops and returns, the refusal where one stands."""
    head = eras[0]
    row = head["held"][0]
    rows = [
        {
            "interval": line["interval"],
            "U": line["rows"][row]["U"],
            "volume": line["rows"][row].get("volume"),
        }
        for line in eras[1:]
        if "rows" in line
    ]
    refused = next((line for line in eras[1:] if "refused" in line), None)
    return {
        "world": head["world"],
        "shape": head["shape"] if world is None else world["shape"],
        "gamma": head["node_clock"],
        "rows": rows,
        "bangs": bangs_of(rows),
        "refused": refused,
    }


def bodies_of(world: dict[str, Any] | None) -> list[dict[str, Any]]:
    """The bodies the world declares, each its family and its Nodes, the page's rings."""
    if world is None:
        return []
    return [
        {"family": body["family"], "nodes": [entry["node"] for entry in body["nodes"]]}
        for body in world.get("bodies", [])
    ]


def charts_of(
    nodes: list[dict[str, Any]],
    clicks: list[dict[str, Any]],
    world: dict[str, Any] | None,
    course: dict[str, Any],
) -> list[dict[str, Any]]:
    """One chart per instrument body (a body whose credits the clicks log carries): the clicks written at its Node (the credit lines whose part changed), their count per 100 intervals in a running window ending at each logged interval, 1 / e^U at its Node and the light's quanta there from the Nodes' log, the rate by the volume's stages, and the readings at the top and at the first click."""
    if world is None or not clicks:
        return []
    shape = course["shape"]
    index = lambda n: (n[0] * shape[1] + n[1]) * shape[2] + n[2]  # noqa: E731
    light = next((name for name in nodes[0]["quanta"] if name == "light"), None) if nodes else None
    intervals = [line["interval"] for line in nodes]
    found = []
    for number, body in enumerate(world.get("bodies", [])):
        name = f"body {number}"
        written = sorted(
            int(c["interval"])
            for c in clicks
            if c.get("event") == "credit"
            and c.get("node_detector") == name
            and c.get("before") != c.get("realised")
        )
        if not written:
            continue
        at = index(body["nodes"][0]["node"])
        rate = [sum(1 for w in written if t - 99 <= w <= t) for t in intervals]
        inverse = [1 / line["length"][at] if line["length"][at] else None for line in nodes]
        lit = [line["quanta"][light][at] if light else 0 for line in nodes]
        edges = [b["at"] for b in course["bangs"]] + [intervals[-1]]
        stages, start = [], intervals[0]
        for edge in edges:
            n = sum(1 for w in written if start <= w <= edge)
            stages.append(
                {"name": f"{start} to {edge}", "clicks": n, "rate": 100 * n / max(1, edge - start + 1)}
            )
            start = edge + 1
        top = next((b["at"] for b in course["bangs"] if b["kind"] == "top"), intervals[-1])
        at_top = intervals.index(top) if top in intervals else len(intervals) - 1
        first = intervals.index(written[0]) if written[0] in intervals else 0
        found.append(
            {
                "body": f"{body['family']} ({name})",
                "node": body["nodes"][0]["node"],
                "intervals": intervals,
                "clicks": written,
                "rate": rate,
                "inverse": inverse,
                "light": lit,
                "stages": stages,
                "e_top": nodes[at_top]["length"][at],
                "light_top": lit[at_top],
                "light_first": lit[first],
            }
        )
    return found


def stages_of(
    nodes: list[dict[str, Any]], course: dict[str, Any], clicks: list[dict[str, Any]]
) -> dict[str, Any]:
    """The stage strip's marks, each read from the logs and none typed: the bang (the seed, the first logged interval), the first turns (the first interval the fifth act turned a Node), every top and return of the board's volume (`bangs_of`), the contraction (the first interval after a top with the volume below the top's), the cut (the last logged interval, or the refusal's), with the births' and the written clicks' intervals ticked."""
    marks: list[dict[str, Any]] = []
    if not nodes:
        return {"marks": marks, "births": [], "clicks": []}
    marks.append({"word": "bang", "at": nodes[0]["interval"]})
    turned = next((line["interval"] for line in nodes if line.get("turned")), None)
    if turned is not None:
        marks.append({"word": "turns", "at": turned})
    rows = course["rows"]
    for bang in course["bangs"]:
        marks.append({"word": bang["kind"], "at": bang["at"]})
        if bang["kind"] == "top":
            after = next(
                (
                    r["interval"]
                    for r in rows
                    if r["interval"] > bang["at"]
                    and r["volume"] is not None
                    and r["volume"] < bang["volume"]
                ),
                None,
            )
            if after is not None:
                marks.append({"word": "contraction", "at": after})
    cut = course["refused"]["interval"] if course["refused"] else nodes[-1]["interval"]
    marks.append({"word": "cut", "at": cut})
    marks.sort(key=lambda m: m["at"])
    births = sorted(int(c["interval"]) for c in clicks if c.get("event") == "birth")
    written = sorted(
        int(c["interval"])
        for c in clicks
        if c.get("event") == "credit" and c.get("before") != c.get("realised")
    )
    return {"marks": marks, "births": births, "clicks": written}


def page(
    nodes: list[dict[str, Any]],
    eras: list[dict[str, Any]],
    clicks: list[dict[str, Any]] | None,
    world: dict[str, Any] | None,
    notes: str | None,
) -> str:
    """The page's HTML from the Nodes' log, the eras log, the clicks log and the world file; everything the page shows embedded as data."""
    if not nodes or "length" not in nodes[0] or "direction" not in nodes[0]:
        raise ValueError(
            "the Nodes' log is tools/eras.py's --nodes file, one line per interval with X, length, turned, direction and quanta"
        )
    course = course_of(eras, world)
    title = f"{str(course['world']).split('.')[0].replace('_', ' ')} torus"
    embed = lambda value: json.dumps(value, separators=(",", ":")).replace("</", "<\\/")  # noqa: E731
    return (
        TEMPLATE.replace("{{TITLE}}", f"{title[:1].upper()}{title[1:]}")
        .replace("{{TOKENS}}", TOKENS.group(0).rstrip("\n"))
        .replace("{{NODES}}", embed(nodes))
        .replace("{{COURSE}}", embed(course))
        .replace("{{BODIES}}", embed(bodies_of(world)))
        .replace("{{CHARTS}}", embed(charts_of(nodes, clicks or [], world, course)))
        .replace("{{NOTES}}", embed(notes))
        .replace("{{STAGES}}", embed(stages_of(nodes, course, clicks or [])))
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "nodes", type=Path, help="the Nodes' log (<world>.nodes.jsonl, tools/eras.py --nodes)"
    )
    parser.add_argument(
        "--eras", type=Path, required=True, help="the eras log of the same run (<world>.eras.jsonl)"
    )
    parser.add_argument(
        "--clicks", type=Path, default=None, help="the clicks log of the same run (<world>.clicks.jsonl)"
    )
    parser.add_argument(
        "--world", type=Path, default=None, help="the world file (the bodies' Nodes and families)"
    )
    parser.add_argument(
        "--notes", type=Path, default=None, help="a Markdown file rendered as the leading prose"
    )
    parser.add_argument("--out", type=Path, default=None, help="the page (<world>.torus.html)")
    args = parser.parse_args(argv)
    nodes, eras = read_log(args.nodes), read_log(args.eras)
    clicks = read_log(args.clicks) if args.clicks else None
    world = json.loads(args.world.read_text(encoding="utf-8")) if args.world else None
    notes = args.notes.read_text(encoding="utf-8") if args.notes else None
    stem = args.nodes.name.removesuffix(".nodes.jsonl")
    target = args.out or args.nodes.with_name(f"{stem}.torus.html")
    target.write_text(page(nodes, eras, clicks, world, notes), encoding="utf-8")
    print(
        json.dumps(
            {
                "nodes": args.nodes.name,
                "page": str(target),
                "bytes": target.stat().st_size,
                "intervals": len(nodes),
            }
        )
    )


if __name__ == "__main__":
    main()
