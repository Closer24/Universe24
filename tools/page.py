"""The page, the third tool of the standard (the owner's words of 2026-10-25 through the Boss, 6397241917 and 6397272516): it reads the record and the reading and writes one HTML, dark by its tokens and generic, with nothing of a universe or a world typed in it. The animation is the page: the torus from the record's Node lines (every Node by its X and content, each Node placed along every axis by the lengths of the Links before it on its line, so a line through matter bulges where its Links are longer, every Link's drawn length its stretch above the rest (e^U - 1, zero at X = Gamma, where the Nodes touch) up to the record's largest, so the board's return to its zero is seen as the Nodes closing on each other, and a Big Bang drawn as a burst with its label at the first interval and at every interval where the board stands at its zero and rises again, read from the Node lines' X alone, a turned Node filled in the turn's colour for its interval, the turned and the frozen Nodes marked, the Links from the world's shape alone, every Link's thickness and brightness its own length against the interval's shortest and longest, so the wells around matter are seen beside the whole board's rise, a Link held at the wall drawn thick, the passage through the Links as a directed mark along each Link from the gap-0 line's current, its size the flow and its direction the sign), the clicks as marks by row, matter at a Node as a halo in its row's colour from the clicks of the last intervals, a body bound at its Node as a steady ring where one line clicks there across a long span, the play holding two seconds on every new label, a legend line under the controls, the reading's event lines as labels at their interval and at their Node with a leader from the Node and a glyph per gate beside the label (a burst for the bang, a pair for the birth, rings for the click, a black disc for the horizon, a clock for the dilation, arrows for the lengthening and the contraction, and so on by the gate's number), a line with no Node at the click of its interval where one stands (the click the gate first showed at), else at the board's foot, and as ticks with their labels on the bar; one header line from the two files as they are, the seed's lays alike but for their centre folded with their count. The Node lines are carried in the page as words of base 36 (X and the content) and one letter per Link for the current's level and sign, so that a long record's page stays within the branch's file bound; where even so the lines pass the bound, every k-th interval is kept with the first, the last and the gates' own intervals, k named on the page. Usage: `python tools/page.py <record.json> <reading.jsonl> <out.html>`."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

BOUND = 4 * 1024 * 1024  # the Node lines' bytes on the page, under the branch's bound per file
LEVELS = 25  # the current's levels on a Link above zero, one letter each
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"

TOKENS = """
:root { --bg: #0f1114; --panel: #171a20; --fg: #e9e7df; --muted: #9a9ea8; --line: #2e323a; --board: #07080a;
  --wall: #d7dae0; --forward: #4ade80; --back: #f59e0b; --hole: #ffffff; --focus: #5f97ea; --label: #fde68a;
  --tones: #f472b6, #22d3ee, #a3e635, #fb923c, #c084fc, #facc15, #38bdf8, #f87171;
  --font: "IBM Plex Sans", system-ui, sans-serif; --mono: "IBM Plex Mono", ui-monospace, monospace; color-scheme: dark; }
html, body { margin: 0; background: var(--bg); color: var(--fg); font: 14px var(--font); }
#head { padding: 8px 16px 4px; color: var(--muted); font-family: var(--mono); font-size: 11px; white-space: pre-wrap; }
#stage { position: relative; }
#board { display: block; margin: 0 auto; background: var(--board); border: 1px solid var(--line); }
#bar { position: relative; height: 70px; margin: 8px 16px 4px; background: var(--panel); border: 1px solid var(--line); cursor: pointer; overflow: visible; }
#bar .tick { position: absolute; top: 0; bottom: 0; width: 2px; background: var(--label); }
#bar .name { position: absolute; font-size: 10px; color: var(--label); font-family: var(--mono); white-space: nowrap; padding-left: 4px; pointer-events: none; }
#bar .bang { position: absolute; bottom: 1px; font-size: 10px; color: var(--muted); font-family: var(--mono); }
#bar #cursor { position: absolute; top: 0; bottom: 0; width: 2px; background: var(--focus); }
#legend { margin: 0 16px 10px; color: var(--muted); font-family: var(--mono); font-size: 11px; }
#row { display: flex; gap: 12px; align-items: center; margin: 0 16px 8px; color: var(--muted); font-family: var(--mono); font-size: 12px; }
button { background: var(--panel); color: var(--fg); border: 1px solid var(--line); padding: 3px 10px; font: inherit; cursor: pointer; }
#labels { position: absolute; left: 0; top: 0; pointer-events: none; }
.label { position: absolute; color: var(--label); font-family: var(--mono); font-size: 15px; font-weight: 600; white-space: nowrap; background: rgba(7, 8, 10, 0.82); border: 1px solid var(--line); border-left: 3px solid var(--label); border-radius: 3px; padding: 3px 8px 4px 8px; max-width: 420px; overflow: hidden; text-overflow: ellipsis; }
.label small { display: block; color: var(--muted); font-size: 11px; font-weight: 400; overflow: hidden; text-overflow: ellipsis; }
a { color: var(--focus); }
"""

SCRIPT = """
const D = JSON.parse(document.getElementById("data").textContent);
const c = D.cube, G = D.gamma, N = D.intervals;
const canvas = document.getElementById("board"), ctx = canvas.getContext("2d");
const stage = document.getElementById("stage"), labels = document.getElementById("labels"), cursor = document.getElementById("cursor");
const bar = document.getElementById("bar"), where = document.getElementById("where");
const head = document.getElementById("head"), row = document.getElementById("row");
const size = Math.max(320, Math.min(window.innerWidth - 32, window.innerHeight - head.offsetHeight - bar.offsetHeight - row.offsetHeight - 40));
canvas.width = size; canvas.height = size;
function words(s) { return s.split(" ").map(w => parseInt(w, 36)); }
function levels(s) { return Array.from(s, ch => ch === "." ? 0 : (ch >= "a" ? ch.charCodeAt(0) - 96 : 64 - ch.charCodeAt(0))); }
const lines = D.nodes.map(l => ({i: l.i, X: words(l.X), content: words(l.content), turned: l.turned, frozen: l.frozen, held: l.held, current: l.current.map(levels)}));
const n = lines.length;
let t = 1, playing = true, speed = 6;
const yaw = 0.62, pitch = 0.42;
function place(x, y, z, grow) {
  const x1 = x * Math.cos(yaw) - y * Math.sin(yaw), y1 = x * Math.sin(yaw) + y * Math.cos(yaw);
  const y2 = y1 * Math.cos(pitch) - z * Math.sin(pitch), z2 = y1 * Math.sin(pitch) + z * Math.cos(pitch);
  const s = grow * canvas.width / (c + 1.5);
  return [canvas.width / 2 + x1 * s, canvas.height / 2 + y2 * s * 0.9, z2];
}
function length(X) { return Math.pow(Math.max(X, 1) / G, 0.25); }
function stretch(X) { return Math.max(length(X) - 1, 0); }
function meanStretch(line) { let sum = 0; for (const X of line.X) sum += stretch(X); return sum / line.X.length; }
const stretches = lines.map(meanStretch), most = Math.max(...stretches, 1e-9), full = canvas.width / (c + 1.5), touch = 5 / full, unit = (1 - touch) / most;
const bangs = [lines[0].i];
for (let k = 1; k + 1 < n; k++) if (stretches[k] <= stretches[k - 1] && stretches[k] < stretches[k + 1] && 10 * stretches[k] < most) bangs.push(lines[k].i);
let spots = [];
function lay(line) {
  const gaps = line.X.map(X => touch + unit * stretch(X));
  const at = (x, y, z) => x * c * c + y * c + z, pos = [[], [], []];
  for (let p = 0; p < c; p++) for (let q = 0; q < c; q++) {
    const linesOf = [k => at(k, p, q), k => at(p, k, q), k => at(p, q, k)];
    for (let a = 0; a < 3; a++) {
      let total = 0; for (let k = 0; k < c; k++) total += gaps[linesOf[a](k)];
      let cum = 0;
      for (let k = 0; k < c; k++) { pos[a][linesOf[a](k)] = cum + gaps[linesOf[a](k)] / 2 - total / 2; cum += gaps[linesOf[a](k)]; }
    }
  }
  spots = Array.from({length: c * c * c}, (_, i) => place(pos[0][i], pos[1][i], pos[2][i], 1));
}
const tones = getComputedStyle(document.documentElement).getPropertyValue("--tones").split(",").map(s => s.trim());
const wall = getComputedStyle(document.documentElement).getPropertyValue("--wall").trim();
function tone(line) { return tones[line % tones.length]; }
function neighbour(i, axis) {
  const q = [Math.floor(i / (c * c)), Math.floor(i / c) % c, i % c];
  if (q[axis] + 1 >= c) return -1;
  q[axis] += 1;
  return q[0] * c * c + q[1] * c + q[2];
}
function glyph(gate, x, y) {
  const g = parseInt(gate), r = 11, L = "#fde68a", M = "#9a9ea8";
  ctx.save(); ctx.translate(x, y); ctx.lineWidth = 2; ctx.strokeStyle = L; ctx.fillStyle = L; ctx.lineCap = "round";
  const dot = (cx, cy, rr, fill) => { ctx.beginPath(); ctx.arc(cx, cy, rr, 0, 2 * Math.PI); if (fill) ctx.fill(); else ctx.stroke(); };
  const arrow = (x1, y1, x2, y2) => { const a = Math.atan2(y2 - y1, x2 - x1); ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); ctx.beginPath(); ctx.moveTo(x2, y2); ctx.lineTo(x2 - 6 * Math.cos(a - 0.5), y2 - 6 * Math.sin(a - 0.5)); ctx.lineTo(x2 - 6 * Math.cos(a + 0.5), y2 - 6 * Math.sin(a + 0.5)); ctx.closePath(); ctx.fill(); };
  const text = (t, cx, cy) => { ctx.font = "bold 11px monospace"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(t, cx, cy); };
  if (g === 1 || g === 46) { for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4; ctx.beginPath(); ctx.moveTo(4 * Math.cos(a), 4 * Math.sin(a)); ctx.lineTo(r * Math.cos(a), r * Math.sin(a)); ctx.stroke(); } }
  else if (g === 17 || g === 21) { dot(-7, 0, 6, false); dot(7, 0, 6, false); text("+", -7, 0); text("-", 7, 0); }
  else if (g === 8) { dot(0, 0, 3, true); dot(0, 0, 7, false); dot(0, 0, 11, false); }
  else if (g === 9 || g === 13 || g === 22) { dot(-9, 0, 4, true); dot(9, 0, 4, true); arrow(-4, -8, 4, -8); arrow(4, 8, -4, 8); }
  else if (g === 14 || g === 34) { ctx.fillStyle = "#07080a"; dot(0, 0, 8, true); ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3; dot(0, 0, 9, false); }
  else if (g === 4) { dot(-7, 4, 4, true); dot(7, 4, 4, true); dot(0, -6, 4, true); }
  else if (g === 10 || g === 30) { dot(0, 0, r, false); ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, -7); ctx.moveTo(0, 0); ctx.lineTo(5, 3); ctx.stroke(); }
  else if (g === 2 || g === 5) { arrow(-2, 0, r + 2, 0); arrow(2, 0, -r - 2, 0); if (g === 5) { ctx.beginPath(); ctx.moveTo(-6, -7); ctx.lineTo(6, -7); ctx.stroke(); } }
  else if (g === 3 || g === 6) { arrow(-r - 2, 0, -3, 0); arrow(r + 2, 0, 3, 0); }
  else if (g === 7) { ctx.beginPath(); for (let k = -12; k <= 2; k++) ctx.lineTo(k, 4 * Math.sin(k * 0.9)); ctx.stroke(); dot(8, 0, 4, true); }
  else if (g === 18) { ctx.beginPath(); ctx.arc(0, 0, 8, -0.5 * Math.PI, 1.1 * Math.PI); ctx.stroke(); arrow(-3, 7, -9, 3); }
  else if (g === 16) { dot(0, -4, 4, true); ctx.beginPath(); ctx.moveTo(-r, 6); ctx.lineTo(r, 6); ctx.stroke(); }
  else if (g === 19 || g === 26) { dot(-7, 2, 3, true); dot(4, 0, 6, true); }
  else if (g === 25) { ctx.beginPath(); ctx.moveTo(-10, 8); ctx.lineTo(-4, 8); ctx.lineTo(-4, 2); ctx.lineTo(2, 2); ctx.lineTo(2, -4); ctx.lineTo(8, -4); ctx.lineTo(8, -10); ctx.stroke(); }
  else if (g === 27) { dot(-7, 5, 3, true); dot(7, 5, 3, true); dot(0, -6, 3, true); ctx.beginPath(); ctx.moveTo(-7, 5); ctx.lineTo(0, -6); ctx.lineTo(7, 5); ctx.closePath(); ctx.stroke(); }
  else if (g === 37) { dot(-9, 0, 3, true); dot(9, 0, 3, true); arrow(-5, 0, 5, 0); }
  else if (g === 43) { dot(0, 0, 6, false); ctx.beginPath(); ctx.moveTo(-9, -9); ctx.lineTo(9, 9); ctx.moveTo(9, -9); ctx.lineTo(-9, 9); ctx.stroke(); }
  else if (g === 45) { ctx.beginPath(); ctx.moveTo(-9, -8); ctx.lineTo(-9, 4); ctx.quadraticCurveTo(0, 12, 9, 4); ctx.lineTo(9, -8); ctx.stroke(); dot(0, 3, 3, true); }
  else if (g === 49) { ctx.beginPath(); ctx.moveTo(-10, -8); ctx.quadraticCurveTo(-6, 8, 10, 8); ctx.stroke(); }
  else { ctx.beginPath(); ctx.moveTo(0, -r); ctx.lineTo(r, 0); ctx.lineTo(0, r); ctx.lineTo(-r, 0); ctx.closePath(); ctx.stroke(); }
  ctx.restore();
}
function seek(i) { let k = 0; while (k + 1 < n && lines[k].i < i) k++; return k + 1; }
function draw() {
  const line = lines[t - 1], before = lines[Math.max(t - 2, 0)], step = Math.max(1, line.i - before.i);
  const held = new Set(line.held.map(h => h[0] + ":" + h[1]));
  const frozen = new Set(line.frozen), turned = new Set(line.turned);
  const lens = line.X.map(length), lenMin = Math.min(...lens), lenSpan = Math.max(Math.max(...lens) - lenMin, 1e-9);
  lay(line);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.lineCap = "round";
  for (let i = 0; i < spots.length; i++) for (let a = 0; a < 3; a++) {
    const j = neighbour(i, a);
    if (j < 0) continue;
    const isHeld = held.has(i + ":" + a), rel = ((lens[i] + lens[j]) / 2 - lenMin) / lenSpan;
    ctx.strokeStyle = isHeld ? wall : "rgba(154,158,168," + (0.2 + 0.7 * rel) + ")";
    ctx.lineWidth = isHeld ? 5 : 1 + 5 * rel;
    ctx.beginPath(); ctx.moveTo(spots[i][0], spots[i][1]); ctx.lineTo(spots[j][0], spots[j][1]); ctx.stroke();
    const flow = line.current[a][i];
    if (flow !== 0) {
      const size = Math.abs(flow) / D.levels, dir = flow > 0 ? 1 : -1;
      const mx = (spots[i][0] + spots[j][0]) / 2, my = (spots[i][1] + spots[j][1]) / 2;
      const dx = (spots[j][0] - spots[i][0]) * dir, dy = (spots[j][1] - spots[i][1]) * dir, len = Math.hypot(dx, dy) || 1;
      const ux = dx / len, uy = dy / len, h = 4 + 10 * size;
      ctx.fillStyle = "rgba(95,151,234," + (0.35 + 0.65 * size) + ")";
      ctx.beginPath(); ctx.moveTo(mx + ux * h, my + uy * h); ctx.lineTo(mx - uy * h * 0.5, my + ux * h * 0.5); ctx.lineTo(mx + uy * h * 0.5, my - ux * h * 0.5); ctx.closePath(); ctx.fill();
    }
  }
  const order = spots.map((s, i) => i).sort((p, q) => spots[p][2] - spots[q][2]);
  const cmin = Math.min(...line.content), cmax = Math.max(...line.content);
  for (const i of order) {
    const r = 3 + 9 * (line.content[i] - cmin) / Math.max(cmax - cmin, 1);
    ctx.fillStyle = turned.has(i) ? "#f59e0b" : "#4ade80";
    ctx.beginPath(); ctx.arc(spots[i][0], spots[i][1], r, 0, 2 * Math.PI); ctx.fill();
    if (frozen.has(i)) { ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(spots[i][0], spots[i][1], r + 3, 0, 2 * Math.PI); ctx.stroke(); }
    if (turned.has(i)) { ctx.strokeStyle = "#f59e0b"; ctx.lineWidth = 1.5; ctx.strokeRect(spots[i][0] - r - 2, spots[i][1] - r - 2, 2 * r + 4, 2 * r + 4); }
  }
  const recent = new Map(), span = new Map();
  for (const k of D.clicks) {
    if (k.i > line.i) break;
    const id = k.node[0] * c * c + k.node[1] * c + k.node[2], key = id + ":" + k.line;
    if (k.i > line.i - 24 * step) { const m = recent.get(id) || new Map(); m.set(k.line, (m.get(k.line) || 0) + 1); recent.set(id, m); }
    const sp = span.get(key); if (!sp) span.set(key, [k.i, k.i, 1]); else { sp[1] = k.i; sp[2]++; }
  }
  for (const [id, m] of recent) {
    let best = -1, count = 0, total = 0; for (const [l, n] of m) { total += n; if (n > count) { count = n; best = l; } }
    const sp = spots[id], r = 8 + Math.min(10, total);
    ctx.fillStyle = tone(best); ctx.globalAlpha = 0.18 + 0.03 * Math.min(10, total); ctx.beginPath(); ctx.arc(sp[0], sp[1], r, 0, 2 * Math.PI); ctx.fill(); ctx.globalAlpha = 1;
  }
  for (const [key, sp] of span) if (sp[1] > line.i - 24 * step && sp[1] - sp[0] >= 60 * step && sp[2] >= 4) {
    const id = parseInt(key), s = spots[id]; ctx.strokeStyle = tone(parseInt(key.split(":")[1])); ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(s[0], s[1], 14, 0, 2 * Math.PI); ctx.stroke();
  }
  for (const k of D.clicks) if (k.i <= line.i && k.i > line.i - 4 * step) {
    const i = k.node[0] * c * c + k.node[1] * c + k.node[2], s = spots[i], age = (line.i - k.i) / step, fade = 1 - age / 4;
    ctx.strokeStyle = tone(k.line); ctx.globalAlpha = fade; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.arc(s[0], s[1], 10 + 4 * age, 0, 2 * Math.PI); ctx.stroke(); ctx.globalAlpha = 1;
  }
  for (const b of bangs) if (line.i >= b && line.i < b + 12 * step) {
    const age = (line.i - b) / step, reach = (0.08 + 0.05 * age) * canvas.width, cx = canvas.width / 2, cy = canvas.height / 2;
    ctx.strokeStyle = "#fde68a"; ctx.globalAlpha = Math.max(0, 1 - age / 12); ctx.lineWidth = 2;
    for (let r = 0; r < 24; r++) { const ang = r * Math.PI / 12 + age * 0.1, inner = reach * (0.35 + 0.15 * (r % 2)); ctx.beginPath(); ctx.moveTo(cx + Math.cos(ang) * inner, cy + Math.sin(ang) * inner); ctx.lineTo(cx + Math.cos(ang) * reach, cy + Math.sin(ang) * reach); ctx.stroke(); }
    ctx.globalAlpha = 1;
  }
  labels.innerHTML = "";
  let free = 0;
  const placed = [];
  function settle(x, y) {
    for (let moved = true; moved;) { moved = false; for (const q of placed) if (Math.abs(q[0] - x) < 220 && Math.abs(q[1] - y) < 42 && q[1] + 42 > y) { y = q[1] + 42; moved = true; } }
    placed.push([x, y]); return y;
  }
  for (const b of bangs) if (line.i >= b && line.i < b + 12 * step) {
    const div = document.createElement("div"); div.className = "label"; div.style.fontSize = "20px";
    div.innerHTML = "Big Bang<small>the board at its zero and rising, interval " + b + "</small>";
    div.style.left = (canvas.offsetLeft + canvas.width / 2 + 0.14 * canvas.width) + "px"; div.style.top = (canvas.offsetTop + canvas.height / 2 - 0.16 * canvas.width) + "px";
    labels.appendChild(div);
  }
  for (const e of D.events) if (e.i !== null && e.i <= line.i && e.i > line.i - 30 * step) {
    const div = document.createElement("div"); div.className = "label";
    div.innerHTML = e.label + "<small>" + e.numbers + "</small>";
    const click = e.node ? null : D.clicks.find(k => k.i === e.i), node = e.node || (click ? click.node : null);
    if (node) {
      const s = spots[node[0] * c * c + node[1] * c + node[2]];
      ctx.strokeStyle = "#fde68a"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(s[0], s[1]); ctx.lineTo(s[0] + 26, s[1] - 26); ctx.stroke();
      ctx.fillStyle = "#fde68a"; ctx.beginPath(); ctx.arc(s[0], s[1], 4, 0, 2 * Math.PI); ctx.fill();
      const y = settle(s[0] + 28, s[1] - 44);
      ctx.beginPath(); ctx.moveTo(s[0] + 26, s[1] - 26); ctx.lineTo(s[0] + 28, y + 18); ctx.stroke();
      glyph(e.gate, s[0] + 44, y + 18);
      div.style.left = (canvas.offsetLeft + s[0] + 60) + "px"; div.style.top = (canvas.offsetTop + y) + "px";
    } else { const fy = canvas.height - 48 - 40 * free++; glyph(e.gate, canvas.width / 2 - 96, fy + 18); div.style.left = (canvas.offsetLeft + canvas.width / 2 - 80) + "px"; div.style.top = (canvas.offsetTop + fy) + "px"; }
    labels.appendChild(div);
  }
  cursor.style.left = (100 * (line.i - 1) / Math.max(N - 1, 1)) + "%";
  where.textContent = "interval " + line.i + " of " + N + (D.stride > 1 ? " (1 of every " + D.stride + " intervals kept)" : "");
}
let hold = 0;
function tick() {
  if (playing && hold > 0) hold--;
  else if (playing) { t = t % n + 1; draw(); const now = lines[t - 1].i, before = t > 1 ? lines[t - 2].i : 0; if (D.events.some(e => e.i !== null && e.i > before && e.i <= now) || bangs.some(b => b > before && b <= now)) hold = 2 * speed; }
  setTimeout(tick, 1000 / speed);
}
const rowEnds = [-100, -100, -100, -100, -100, -100];
for (const e of D.events) if (e.i !== null) {
  const pct = 100 * (e.i - 1) / Math.max(N - 1, 1), at = pct + "%";
  const d = document.createElement("div"); d.className = "tick"; d.style.left = at; d.title = e.label + ": " + e.numbers; bar.appendChild(d);
  let row = rowEnds.findIndex(end => pct - end > 11); if (row < 0) continue; rowEnds[row] = pct;
  const m = document.createElement("div"); m.className = "name"; m.style.top = (2 + 11 * row) + "px"; m.textContent = e.label;
  if (4 * (e.i - 1) > 3 * Math.max(N - 1, 1)) { m.style.right = "calc(100% - " + at + ")"; m.style.paddingRight = "4px"; } else m.style.left = at;
  bar.appendChild(m);
}
for (const b of bangs) { const d = document.createElement("div"); d.className = "tick"; d.style.left = (100 * (b - 1) / Math.max(N - 1, 1)) + "%"; d.style.background = "#f59e0b"; d.title = "Big Bang at " + b; bar.appendChild(d); }
D.bangs.forEach((i, k) => { const d = document.createElement("div"); d.className = "bang"; d.style.left = (100 * (i - 1) / Math.max(N - 1, 1)) + "%"; d.textContent = (k + 1); bar.appendChild(d); });
bar.addEventListener("click", ev => { const r = bar.getBoundingClientRect(); t = seek(1 + Math.round((N - 1) * (ev.clientX - r.left) / r.width)); playing = false; draw(); });
document.getElementById("play").addEventListener("click", () => { playing = !playing; });
document.getElementById("faster").addEventListener("click", () => { speed = Math.min(speed * 2, 48); });
document.getElementById("slower").addEventListener("click", () => { speed = Math.max(speed / 2, 1); });
draw(); tick();
"""


def header_of(record: dict[str, Any]) -> str:
    """One header line from the two files as they are: the universe's integers and rows, the world's shape, intervals and seed."""
    universe, world = record["universe"], record["world"]
    integers = ", ".join(f"{k} {v}" for k, v in universe["integers"].items())
    rows = "; ".join(
        f"shape {r['shape']} "
        + (f"pair {r['pair'][0]}/{r['pair'][1]}" if r.get("pair") is not None else f"wall {r['wall']}")
        for r in universe["rows"]
    )
    seed = "; ".join(lays_of(world.get("seed", [])))
    return f"universe {world['universe']}: {integers}\nrows: {rows}\nworld: shape {world['shape']}, {world['intervals']} intervals, seed {seed}"


def lays_of(seed: list[dict[str, Any]]) -> list[str]:
    """The seed's lays as they are, the lays alike in everything but their centre folded into one with their count, so a seed laid at every Node reads as one line."""
    found: dict[str, int] = {}
    for lay in seed:
        key = json.dumps({k: v for k, v in lay.items() if k != "centre"})
        found[key] = found.get(key, 0) + 1
    return [key if n == 1 else f"{key} at {n} centres" for key, n in found.items()]


def word(n: int) -> str:
    """An integer as a word of base 36, a minus sign before a negative one."""
    found, rest = "", abs(n)
    while True:
        rest, digit = divmod(rest, len(DIGITS))
        found = DIGITS[digit] + found
        if rest == 0:
            return ("-" if n < 0 else "") + found


def letters(current: list[Any]) -> str:
    """A Link's current on every Link of one axis as one letter each: its level above zero in LEVELS steps of the axis's largest size, a small letter forward, a capital backward, a dot at zero."""
    values = [int(x) for x in current]
    largest = max((abs(x) for x in values), default=0)
    found = []
    for x in values:
        if x == 0:
            found.append(".")
            continue
        level = abs(x) * (LEVELS - 1) // largest
        found.append(chr((97 if x > 0 else 65) + level))
    return "".join(found)


def line_of(line: dict[str, Any]) -> dict[str, Any]:
    """A Node line as the page carries it: X and the content as words of base 36, the current as letters, the turned, the frozen and the held as they are."""
    return {
        "i": int(line["i"]),
        "X": " ".join(word(int(x)) for x in line["X"]),
        "content": " ".join(word(int(x)) for x in line["content"]),
        "turned": line["turned"],
        "frozen": line["frozen"],
        "held": line["held"],
        "current": [letters(axis) for axis in line["current"]],
    }


def kept(lines: list[dict[str, Any]], named: set[int]) -> tuple[list[dict[str, Any]], int]:
    """The Node lines within the bound: all of them where they fit, else every k-th with the first, the last and the named intervals, k the least that fits."""
    total = sum(len(json.dumps(line)) for line in lines)
    stride = max(1, -(-total // BOUND))
    if stride == 1:
        return lines, 1
    last = lines[-1]["i"]
    return [
        line for line in lines if line["i"] % stride == 1 or line["i"] in named or line["i"] == last
    ], stride


def data_of(record: dict[str, Any], reading: list[dict[str, Any]]) -> dict[str, Any]:
    """The page's data from the record and the reading: the Node lines, the clicks (every birth and credit with its Node and row), the bangs (the births' intervals), the reading's event lines."""
    events = next((line["events"] for line in reading if "events" in line), [])
    clicks = [
        {"i": e["i"], "node": e["node"], "line": e.get("line", e.get("line_pair", 0))}
        for e in record["log"]
        if e["event"] in ("birth", "credit")
    ]
    bangs = sorted({e["i"] for e in record["log"] if e["event"] == "birth"})
    named = {int(e["i"]) for e in events if e["i"] is not None} | {int(k["i"]) for k in clicks}
    held = next((int(line["i"]) for line in record["nodes"] if line["held"] or line["frozen"]), None)
    if held is not None:
        named.add(held)
    lines, stride = kept([line_of(line) for line in record["nodes"]], named)
    return {
        "cube": int(record["cube"]),
        "gamma": int(record["gamma"]),
        "intervals": int(record["intervals"]),
        "levels": LEVELS,
        "stride": stride,
        "nodes": lines,
        "clicks": clicks,
        "bangs": bangs,
        "events": events,
    }


def page_of(record: dict[str, Any], reading: list[dict[str, Any]]) -> str:
    """The one HTML: the header line, the board, the bar and the controls, the data embedded, the script."""
    title = f"{record['world'].get('universe', 'universe')} on {record['cube']}^3 for {record['intervals']} intervals"
    return (
        '<!doctype html>\n<html><head><meta charset="utf-8"><title>'
        + title
        + "</title><style>"
        + TOKENS
        + "</style></head>\n<body>\n"
        '<div id="head">' + header_of(record) + "</div>\n"
        '<div id="stage"><canvas id="board" width="320" height="320"></canvas><div id="labels"></div></div>\n'
        '<div id="bar"><div id="cursor"></div></div>\n'
        '<div id="row"><button id="play">play / pause</button><button id="slower">slower</button><button id="faster">faster</button><span id="where"></span>'
        "<span>the reading: the verdicts in the reading file beside the record</span></div>\n"
        '<div id="legend">green dot: a Node, its size the content; blue arrow: the gap-0 current along the Link (the gap-0 row); coloured halo: matter clicking at the Node, the colour its row; coloured ring: a body bound at its Node; orange: the Node turned; white ring: the Node frozen; thick white Link: at the wall; yellow: a gate as it first shows</div>\n'
        '<script id="data" type="application/json">'
        + json.dumps(data_of(record, reading))
        + "</script>\n"
        "<script>" + SCRIPT + "</script>\n</body></html>\n"
    )


def write_page(record_path: str | Path, reading_path: str | Path, out_path: str | Path) -> None:
    """The page written from the record file and the reading file (one JSON per line, the gates' output)."""
    record = json.loads(Path(record_path).read_text(encoding="utf-8"))
    reading = [
        json.loads(line)
        for line in Path(reading_path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    Path(out_path).write_text(page_of(record, reading), encoding="utf-8")


if __name__ == "__main__":
    write_page(sys.argv[1], sys.argv[2], sys.argv[3])
