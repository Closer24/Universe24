"""The page, the third tool of the standard (the owner's words of 2026-10-25 through the Boss, 6397241917 and 6397272516): it reads the record and the reading and writes one HTML, dark by its tokens and generic, with nothing of a universe or a world typed in it. The animation is the page: the torus from the record's Node lines (every Node by its X and content, each Node placed along every axis by the lengths of the Links before it on its line, so a line through matter bulges where its Links are longer, every Link's drawn length its stretch above the rest (e^U - 1, zero at X = Gamma, where the Nodes stand a hand apart as a tight lattice), the board's size a quarter and three quarters of the square root of the interval's mean stretch against the record's largest so that a run whose late lengths dwarf its early ones stays in view and its Nodes stay apart, every Link at its own length within the interval, so the board's return to its zero is seen as the Nodes closing on each other, and a Big Bang drawn as a burst with its label at the first interval and at every exact return the reading's row 1c names, the Nodes small and sharp, a turned Node filled in the turn's colour for its interval, the turned Nodes marked and a frozen Node drawn as a black disc in a white ring with a dark halo (the horizon, the label at the first frozen Node), the Links from the world's shape alone, every Link's thickness and brightness its own length against the interval's shortest and longest, so the wells around matter are seen beside the whole board's rise, a Link held at the wall drawn thick, the passage through the Links as a directed mark along each Link from the gap-0 line's current, its size the flow and its direction the sign), the clicks as marks by row with the take's source inside (the levels taken, blue from the gap-0 row, else the taken row's colour) and a birth's two children joined to the take's Node with their signs, a turned Node marked by an arc with an arrowhead fading over eight intervals (its clock reversed at the top), a turn of the whole board at once as one dashed ring with its label, the bar banded by the eras the reading's eras row names (each bang, the era of matter, the acceleration), the bangs and the tops read from that row too and the readout naming how many clocks' volumes rise and fall at the interval, matter at a Node as a halo in its row's colour from the clicks of the last intervals, a body bound at its Node as a steady ring where one line clicks there across a long span, the play holding a second on every new label and then running at a quarter pace for four seconds, a big round play button at the centre under the bar (the space key too) and the page's look its tokens' (the board a card at the left, the controls pills, the labels glass), the list of the gates of the phenomena beside the board (every row of the reading in two groups, the rows read from the Node lines (the board's view) and the rows read from the log (the clicks' view), as the decoder's line names them, each row with the gate's glyph as its icon, its verdict's kind, the SHOWN rows with the interval they first show at, each lit as the play passes its interval and brightest for the intervals after it, the count of the numbered rows SHOWN at its head), a strip under the bar naming the bang and the latest labels, the bar carrying the ticks of the gates and the births and the bands of the eras with no names on it, the two files' lines and the legend out of the viewer's sight behind one info button at the top right, the reading's event lines (the gates of the phenomena, one per gate at its first SHOWN) as labels at their interval and at their Node set outside the lattice's edge with a dashed leader to the Node and a glyph per gate beside the label in its family's colour (the cosmos amber, matter pink, the gap-0 row's gates cyan, gravity and time orange, the conservations green, the quantum violet, the constants blue; a burst for the bang, a pair for the birth, rings for the click, a black disc for the horizon, a clock for the dilation, arrows for the lengthening and the contraction, and so on by the gate's number), a line with no Node at the click of its interval where one stands (the click the gate first showed at), else at the board's foot, and as ticks with their labels on the bar; one header line from the two files as they are, the seed's lays alike but for their centre folded with their count. The Node lines are carried in the page as words of base 36 (X and the content) and one letter per Link for the current's level and sign, so that a long record's page stays within the branch's file bound; where even so the lines pass the bound, every k-th interval is kept with the first, the last and the gates' own intervals, k named on the page. Usage: `python tools/page.py <record.json> <reading.jsonl> <out.html>`."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

MEBIBYTE = 1024 * 1024  # a mebibyte, the unit of the branch's bound per file
BOUND = 4 * MEBIBYTE  # the Node lines' bytes on the page, under the branch's bound of 5 per file
LEVELS = 25  # the current's levels on a Link above zero, one letter each
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"

TOKENS = """
:root { --bg: #0b0d11; --panel: #14171d; --card: #10131a; --fg: #ecebe4; --muted: #8e939e; --dim: #5b606b; --line: #262b34; --board: #06070a;
  --wall: #d7dae0; --forward: #4ade80; --back: #f59e0b; --hole: #ffffff; --focus: #5f97ea; --label: #fde68a; --shown: #fde68a; --part: #fbbf24; --not: #6b7280;
  --tones: #f472b6, #22d3ee, #a3e635, #fb923c, #c084fc, #facc15, #38bdf8, #f87171;
  --font: "Inter", "IBM Plex Sans", system-ui, sans-serif; --mono: "JetBrains Mono", "IBM Plex Mono", ui-monospace, monospace; color-scheme: dark; }
* { box-sizing: border-box; }
html, body { margin: 0; background: radial-gradient(1400px 600px at 30% -20%, #161b26 0%, var(--bg) 60%); color: var(--fg); font: 14px var(--font); overflow: auto; }
#top { display: flex; align-items: center; gap: 14px; padding: 12px 20px 10px; }
#title { font-size: 20px; font-weight: 700; letter-spacing: 0.2px; white-space: nowrap; }
#title small { margin-left: 10px; color: var(--muted); font-size: 12px; font-weight: 400; }
#top button#info { margin-left: auto; width: 30px; height: 30px; padding: 0; border-radius: 50%; font-family: var(--mono); font-weight: 700; color: var(--muted); }
#card { display: none; position: absolute; right: 20px; top: 52px; width: 560px; max-height: 70vh; overflow: auto; background: rgba(20, 23, 29, 0.96); backdrop-filter: blur(10px); border: 1px solid var(--line); border-radius: 14px; padding: 14px 16px; z-index: 9; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6); color: var(--muted); font-family: var(--mono); font-size: 10px; line-height: 1.55; }
body.info #card { display: block; }
#card h3 { margin: 0 0 6px; font: 600 11px var(--font); letter-spacing: 0.4px; text-transform: uppercase; color: var(--fg); }
#card pre { margin: 0 0 12px; white-space: pre-wrap; font: inherit; }
#main { display: flex; gap: 16px; padding: 0 20px; align-items: stretch; }
#stage { position: relative; flex: none; }
#board { display: block; background: radial-gradient(circle at 50% 45%, #0c0f15 0%, var(--board) 72%); border: 1px solid var(--line); border-radius: 20px; box-shadow: 0 24px 70px rgba(0, 0, 0, 0.6), inset 0 0 90px rgba(95, 151, 234, 0.05); }
#side { flex: 1; min-width: 0; display: flex; flex-direction: column; background: var(--card); border: 1px solid var(--line); border-radius: 20px; padding: 12px 14px 10px; }
#side h2 { margin: 0 0 6px; font-size: 13px; font-weight: 600; letter-spacing: 0.4px; text-transform: uppercase; color: var(--muted); display: flex; justify-content: space-between; }
#side h2 b { color: var(--shown); font-family: var(--mono); font-weight: 600; text-transform: none; letter-spacing: 0; }
#gates { flex: 1; display: grid; grid-auto-flow: column; grid-template-rows: repeat(var(--rows), minmax(0, 1fr)); column-gap: 18px; min-height: 0; font-family: var(--mono); font-size: 11px; }
.gate { display: flex; align-items: center; gap: 6px; min-width: 0; padding: 0 6px; border-radius: 6px; color: var(--dim); white-space: nowrap; transition: background 0.2s, color 0.2s; }
.gate .n { width: 18px; text-align: right; flex: none; opacity: 0.8; }
.gate .i { width: 20px; height: 20px; flex: none; opacity: 0.35; }
.gate.shown .i, .gate.part .i { opacity: 0.7; } .gate.lit .i { opacity: 1; }
.group { font: 600 10px var(--font); letter-spacing: 0.6px; text-transform: uppercase; color: var(--focus); padding: 0 6px; display: flex; align-items: center; border-bottom: 1px solid var(--line); }
.gate .d { width: 8px; height: 8px; border-radius: 50%; flex: none; background: #2a2f39; }
.gate .t { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; }
.gate .k { flex: none; font-size: 9px; letter-spacing: 0.3px; opacity: 0.7; }
.gate.shown { color: var(--muted); } .gate.shown .d { background: color-mix(in srgb, var(--c) 35%, transparent); border: 1px solid var(--c); }
.gate.part { color: var(--muted); } .gate.part .d { background: rgba(251, 191, 36, 0.3); border: 1px solid var(--part); }
.gate.lit { color: var(--fg); background: color-mix(in srgb, var(--c) 9%, transparent); } .gate.lit .d { background: var(--c); box-shadow: 0 0 8px var(--c); border: none; }
.gate.now { background: color-mix(in srgb, var(--c) 22%, transparent); color: var(--c); }
.gate.not .d { background: #1d2027; border: 1px solid #343944; }
#bar { position: relative; height: 34px; margin: 10px 20px 0; background: linear-gradient(180deg, #1a1e26, var(--panel)); border: 1px solid var(--line); border-radius: 10px; cursor: pointer; }
#bar .era { position: absolute; top: 0; bottom: 0; pointer-events: none; border-radius: 10px; }
#bar .tick { position: absolute; top: 6px; bottom: 6px; width: 2px; background: var(--label); opacity: 0.8; border-radius: 1px; }
#bar .birth { position: absolute; bottom: 3px; width: 2px; height: 8px; background: var(--forward); opacity: 0.8; border-radius: 1px; }
#bar #cursor { position: absolute; top: -5px; bottom: -5px; width: 3px; background: var(--focus); border-radius: 2px; box-shadow: 0 0 12px var(--focus), 0 0 24px rgba(95, 151, 234, 0.6); }
#now { display: flex; gap: 8px; margin: 6px 20px 0; min-height: 22px; overflow: hidden; }
#now span { font-family: var(--mono); font-size: 11px; color: var(--c, var(--label)); background: color-mix(in srgb, var(--c, var(--label)) 10%, transparent); border: 1px solid color-mix(in srgb, var(--c, var(--label)) 35%, transparent); border-radius: 999px; padding: 2px 10px; white-space: nowrap; }
#now span.era { color: var(--focus); background: rgba(95, 151, 234, 0.1); border-color: rgba(95, 151, 234, 0.35); }
#row { display: flex; gap: 14px; align-items: center; justify-content: center; margin: 8px 20px 12px; color: var(--muted); font-family: var(--mono); font-size: 12px; }
button { background: var(--panel); color: var(--fg); border: 1px solid var(--line); padding: 7px 14px; font: inherit; cursor: pointer; border-radius: 999px; transition: background 0.15s, transform 0.1s; }
button:hover { background: #222733; } button:active { transform: scale(0.97); }
#play { width: 60px; height: 60px; padding: 0; border: none; border-radius: 50%; background: linear-gradient(135deg, var(--focus), #22d3ee); box-shadow: 0 8px 28px rgba(95, 151, 234, 0.45); display: inline-flex; align-items: center; justify-content: center; }
#play .tri { width: 0; height: 0; border-left: 22px solid var(--board); border-top: 13px solid transparent; border-bottom: 13px solid transparent; margin-left: 5px; }
#play .bars { display: none; width: 7px; height: 24px; background: var(--board); box-shadow: 12px 0 0 var(--board); margin-right: 12px; }
body.playing #play .tri { display: none; } body.playing #play .bars { display: block; }
#where { font-size: 12px; color: var(--fg); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 260px; }
#labels { position: absolute; left: 0; top: 0; pointer-events: none; }
.label { position: absolute; color: var(--label); font-family: var(--mono); font-size: 14px; font-weight: 600; white-space: nowrap; background: rgba(10, 12, 16, 0.78); backdrop-filter: blur(8px); border: 1px solid rgba(253, 230, 138, 0.22); border-left: 3px solid var(--label); border-radius: 8px; padding: 4px 10px 5px 10px; max-width: 330px; overflow: hidden; text-overflow: ellipsis; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45); }
.label small { display: block; color: var(--muted); font-size: 10px; font-weight: 400; overflow: hidden; text-overflow: ellipsis; }
.label.bang { font-size: 22px; letter-spacing: 1px; border-left-color: #f59e0b; color: #fde68a; background: rgba(245, 158, 11, 0.12); }
a { color: var(--focus); }
"""

SCRIPT = """
const D = JSON.parse(document.getElementById("data").textContent);
const MS = 1000, BASE = 36;  // a second in milliseconds (the ticks' pace); the base of the Node lines' words
const FAMILIES = [  // the gates' families and their colours: the cosmos, matter, the gap-0 row, gravity and time, the conservations, the quantum, the constants
  [[1, 3, 5, 6, 46, 58, 59, 60], "#fbbf24"], [[4, 8, 9, 13, 19, 26, 33, 45], "#f472b6"], [[7, 11, 12, 29, 31, 48, 50, 55], "#22d3ee"],
  [[10, 14, 30, 32, 34, 35, 36], "#fb923c"], [[15, 16, 17, 18, 21, 22, 23, 25, 27, 43, 47], "#a3e635"], [[2, 37, 20, 24, 28, 38, 39, 40, 41, 42, 44, 49, 51, 52, 53, 54, 56, 57], "#c084fc"]];
function colour(gate) { const g = parseInt(gate); for (const [gs, c] of FAMILIES) if (gs.includes(g)) return c; return "#38bdf8"; }
const c = D.cube, G = D.gamma, N = D.intervals;
const canvas = document.getElementById("board"), ctx = canvas.getContext("2d");
const stage = document.getElementById("stage"), labels = document.getElementById("labels"), cursor = document.getElementById("cursor");
const bar = document.getElementById("bar"), where = document.getElementById("where");
const row = document.getElementById("row"), topBox = document.getElementById("top");
const now = document.getElementById("now"), gatesBox = document.getElementById("gates"), side = document.getElementById("side");
const size = Math.max(320, Math.min(Math.floor(window.innerWidth * 0.48), window.innerHeight - topBox.offsetHeight - bar.offsetHeight - now.offsetHeight - row.offsetHeight - 64));
canvas.width = size; canvas.height = size; side.style.height = size + "px";
function words(s) { return s.split(" ").map(w => parseInt(w, BASE)); }
function levels(s) { return Array.from(s, ch => ch === "." ? 0 : (ch >= "a" ? ch.charCodeAt(0) - 96 : 64 - ch.charCodeAt(0))); }
const unravel = i => [Math.floor(i / (c * c)), Math.floor(i / c) % c, i % c];
D.clicks = D.clicks.map(k => ({i: k[0], at: k[1], node: unravel(k[1]), line: k[2], levels: k[3], from: k[4] < 0 ? null : k[4], children: k[5] ? k[5] : null}));
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
const stretches = lines.map(meanStretch), most = Math.max(...stretches, 1e-9), full = canvas.width / (c + 1.5), touch = 16 / full;
const bangs = D.eras.bangs || [lines[0].i], tops = D.eras.tops || [], spans = D.eras["spans (from, to, the gate, its label)"] || [];  // the reading's eras row: the bangs, the tops, the spans
let spots = [];
const firstAt = new Map(); for (const e of D.events) if (e.i !== null) firstAt.set(e.gate, e.i);
const boardRows = new Set(D.board);
const grouped = [["the board, from the Node lines", D.gates.filter(g => boardRows.has(g[0]))], ["the clicks, from the log", D.gates.filter(g => !boardRows.has(g[0]))]];
const gateRows = [];
for (const [name, rows] of grouped) {
  const h = document.createElement("div"); h.className = "group"; h.textContent = name; gatesBox.appendChild(h);
  for (const g of rows) { const div = document.createElement("div"); div.className = "gate " + g[2]; const at = firstAt.get(g[0]);
    const icon = document.createElement("canvas"); icon.width = 26; icon.height = 26; icon.className = "i"; glyph(g[0], 13, 13, icon.getContext("2d"), 0.85);
    div.innerHTML = '<span class="n"></span><span class="d"></span><span class="t"></span><span class="k"></span>'; div.insertBefore(icon, div.children[1]);
    div.style.setProperty("--c", colour(g[0])); div.querySelector(".n").textContent = g[0].split(" ")[0]; div.querySelector(".t").textContent = g[0].split(" ").slice(1).join(" "); div.querySelector(".k").textContent = at ? "at " + at : g[1]; div.title = g[0] + ": " + g[3]; gatesBox.appendChild(div); gateRows.push([div, at]); }
}
gatesBox.style.setProperty("--rows", Math.ceil((D.gates.length + grouped.length) / 2));
const numbered = D.gates.filter(g => /^[0-9]+ /.test(g[0]));
document.getElementById("count").textContent = numbered.filter(g => g[2] === "shown").length + " of " + numbered.length + " shown";
function panel(i) { for (const [div, at] of gateRows) { div.classList.toggle("lit", at !== undefined && at <= i); div.classList.toggle("now", at !== undefined && at <= i && at > i - 24); } }
function lay(line) {
  const mean = meanStretch(line), grow = Math.min(1, 0.25 + 0.75 * Math.sqrt(mean / most)), gaps = line.X.map(X => touch + (1 - touch) * grow * (mean > 0 ? stretch(X) / mean : 0));
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
function glyph(gate, x, y, on, scale) {
  const cx2 = on || ctx, g = parseInt(gate), r = 11, L = colour(gate);
  cx2.save(); cx2.translate(x, y); if (scale) cx2.scale(scale, scale); cx2.lineWidth = 2.4; cx2.strokeStyle = L; cx2.fillStyle = L; cx2.lineCap = "round"; cx2.lineJoin = "round"; cx2.shadowColor = L; cx2.shadowBlur = 6;
  const dot = (cx, cy, rr, fill) => { cx2.beginPath(); cx2.arc(cx, cy, rr, 0, 2 * Math.PI); if (fill) cx2.fill(); else cx2.stroke(); };
  const line = (x1, y1, x2, y2) => { cx2.beginPath(); cx2.moveTo(x1, y1); cx2.lineTo(x2, y2); cx2.stroke(); };
  const arrow = (x1, y1, x2, y2) => { const a = Math.atan2(y2 - y1, x2 - x1); line(x1, y1, x2, y2); cx2.beginPath(); cx2.moveTo(x2, y2); cx2.lineTo(x2 - 6 * Math.cos(a - 0.5), y2 - 6 * Math.sin(a - 0.5)); cx2.lineTo(x2 - 6 * Math.cos(a + 0.5), y2 - 6 * Math.sin(a + 0.5)); cx2.closePath(); cx2.fill(); };
  const wave = (x1, x2, yy, amp, k) => { cx2.beginPath(); for (let q = x1; q <= x2; q++) cx2.lineTo(q, yy + amp * Math.sin(q * k)); cx2.stroke(); };
  const text = (s, cx, cy) => { cx2.font = "bold 11px monospace"; cx2.textAlign = "center"; cx2.textBaseline = "middle"; cx2.fillText(s, cx, cy); };
  if (g === 1 || g === 46) { for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4; line(4 * Math.cos(a), 4 * Math.sin(a), r * Math.cos(a), r * Math.sin(a)); } }
  else if (g === 17 || g === 21) { dot(-7, 0, 6, false); dot(7, 0, 6, false); text("+", -7, 0); text("-", 7, 0); }
  else if (g === 8) { dot(0, 0, 3, true); dot(0, 0, 7, false); dot(0, 0, 11, false); }
  else if (g === 9 || g === 13 || g === 22 || g === 33) { dot(-9, 0, 4, true); dot(9, 0, 4, true); arrow(-4, -8, 4, -8); arrow(4, 8, -4, 8); }
  else if (g === 14 || g === 34) { cx2.fillStyle = "#07080a"; dot(0, 0, 8, true); cx2.strokeStyle = "#ffffff"; cx2.lineWidth = 3; dot(0, 0, 9, false); if (g === 34) { cx2.strokeStyle = L; cx2.lineWidth = 2; line(0, 0, 0, -5); } }
  else if (g === 4) { dot(-7, 4, 4, true); dot(7, 4, 4, true); dot(0, -6, 4, true); }
  else if (g === 10 || g === 30) { dot(0, 0, r, false); line(0, 0, 0, -7); line(0, 0, 5, 3); }
  else if (g === 2 || g === 5) { arrow(-2, 0, r + 2, 0); arrow(2, 0, -r - 2, 0); if (g === 5) line(-6, -7, 6, -7); }
  else if (g === 3 || g === 6) { arrow(-r - 2, 0, -3, 0); arrow(r + 2, 0, 3, 0); }
  else if (g === 7) { wave(-12, 2, 0, 4, 0.9); dot(8, 0, 4, true); }
  else if (g === 11 || g === 29) { wave(-12, -1, 0, 3, 1.4); wave(0, 12, 0, 3, 0.7); }
  else if (g === 12 || g === 31) { cx2.beginPath(); cx2.moveTo(-12, -6); cx2.quadraticCurveTo(0, 8, 12, -6); cx2.stroke(); dot(0, 6, 3, true); }
  else if (g === 18) { cx2.beginPath(); cx2.arc(0, 0, 8, -0.5 * Math.PI, 1.1 * Math.PI); cx2.stroke(); arrow(-3, 7, -9, 3); }
  else if (g === 15 || g === 47) { line(-10, 6, 10, 6); line(0, 6, 0, -6); line(-8, -4, 8, -4); dot(-8, -4, 2, true); dot(8, -4, 2, true); }
  else if (g === 16) { dot(0, -4, 4, true); line(-r, 6, r, 6); }
  else if (g === 19 || g === 26) { dot(-7, 2, 3, true); dot(4, 0, 6, true); }
  else if (g === 20) { line(0, -10, 0, 10); dot(-6, 0, 3, true); dot(6, 0, 3, false); }
  else if (g === 23) { dot(0, 0, 3, true); arrow(-3, -3, -11, -9); arrow(3, 3, 11, 9); }
  else if (g === 24) { dot(-8, -4, 3, true); dot(-8, 4, 3, true); wave(-3, 12, 0, 3, 1.2); }
  else if (g === 25) { cx2.beginPath(); cx2.moveTo(-10, 8); cx2.lineTo(-4, 8); cx2.lineTo(-4, 2); cx2.lineTo(2, 2); cx2.lineTo(2, -4); cx2.lineTo(8, -4); cx2.lineTo(8, -10); cx2.stroke(); }
  else if (g === 27) { dot(-7, 5, 3, true); dot(7, 5, 3, true); dot(0, -6, 3, true); cx2.beginPath(); cx2.moveTo(-7, 5); cx2.lineTo(0, -6); cx2.lineTo(7, 5); cx2.closePath(); cx2.stroke(); }
  else if (g === 28 || g === 52) { line(0, 10, 0, 0); line(0, 0, -8, -8); line(0, 0, 8, -8); dot(-8, -8, 2, true); dot(8, -8, 2, true); if (g === 52) dot(0, -10, 2, false); }
  else if (g === 32) { cx2.beginPath(); cx2.ellipse(0, 0, 11, 6, 0.5, 0, 2 * Math.PI); cx2.stroke(); dot(-3, -1, 3, true); }
  else if (g === 35) { cx2.beginPath(); for (let a = 0; a < 4.5; a += 0.2) cx2.lineTo(a * 2.4 * Math.cos(a), a * 2.4 * Math.sin(a)); cx2.stroke(); dot(0, 0, 2, true); }
  else if (g === 36) { wave(-12, 12, -4, 3, 0.8); wave(-12, 12, 5, 3, 0.8); }
  else if (g === 37) { dot(-9, 0, 3, true); dot(9, 0, 3, true); arrow(-5, 0, 5, 0); }
  else if (g === 38) { dot(0, 0, 9, false); dot(0, 0, 2, true); }
  else if (g === 39) { line(-10, -6, 10, -6); line(-10, 2, 10, 2); line(-10, 7, 10, 7); }
  else if (g === 40) { wave(-12, -2, 0, 3, 1.2); dot(2, 0, 4, true); arrow(5, -3, 12, -10); }
  else if (g === 41) { cx2.beginPath(); cx2.arc(-5, 0, 6, 0.5 * Math.PI, 1.5 * Math.PI); cx2.stroke(); cx2.beginPath(); cx2.arc(5, 0, 6, -0.5 * Math.PI, 0.5 * Math.PI); cx2.stroke(); }
  else if (g === 42) { line(-12, 0, -2, 0); arrow(-2, 0, 10, -7); arrow(-2, 0, 10, 7); }
  else if (g === 43) { dot(0, 0, 6, false); line(-9, -9, 9, 9); line(9, -9, -9, 9); }
  else if (g === 44 || g === 53) { dot(-4, 0, 4, true); if (g === 44) arrow(1, 0, 12, 0); else { cx2.beginPath(); cx2.moveTo(-11, -8); cx2.lineTo(-11, 4); cx2.quadraticCurveTo(-4, 11, 3, 4); cx2.lineTo(3, -8); cx2.stroke(); } }
  else if (g === 45) { cx2.beginPath(); cx2.moveTo(-9, -8); cx2.lineTo(-9, 4); cx2.quadraticCurveTo(0, 12, 9, 4); cx2.lineTo(9, -8); cx2.stroke(); dot(0, 3, 3, true); }
  else if (g === 48) { cx2.beginPath(); cx2.moveTo(-12, 8); cx2.quadraticCurveTo(-6, -14, 0, -4); cx2.quadraticCurveTo(6, 6, 12, 8); cx2.stroke(); }
  else if (g === 49) { cx2.beginPath(); cx2.moveTo(-10, -8); cx2.quadraticCurveTo(-6, 8, 10, 8); cx2.stroke(); }
  else if (g === 50) { wave(-12, 12, -3, 3, 0.9); wave(-12, 12, 3, 3, -0.9); }
  else if (g === 51) { line(-7, -10, -7, 10); line(7, -10, 7, 10); arrow(-5, 0, -1, 0); arrow(5, 0, 1, 0); }
  else if (g === 54) { arrow(-12, -5, 12, 5); arrow(12, -5, -12, 5); }
  else if (g === 55) { line(-2, -11, -2, -4); line(-2, -1, -2, 1); line(-2, 4, -2, 11); wave(-12, -4, 0, 2, 1.5); for (let k = -8; k <= 8; k += 4) dot(9, k, 1.5, true); }
  else if (g === 56) { dot(-8, 0, 4, false); dot(8, 0, 4, false); line(-4, 0, 4, 0); line(-8, -4, -8, -9); line(8, 4, 8, 9); }
  else if (g === 58) { for (const a of [0, 2, 4]) arrow(0, 0, 11 * Math.cos(a * Math.PI / 3 - Math.PI / 2), 11 * Math.sin(a * Math.PI / 3 - Math.PI / 2)); dot(0, 0, 2, true); }
  else if (g === 59) { arrow(-11, 0, 4, 0); line(8, -7, 8, 7); }
  else if (g === 60) { arrow(-11, 4, 2, 4); arrow(-11, -4, 11, -4); }
  else if (g === 57) { dot(0, 7, 2, true); for (const dx of [-8, 0, 8]) { line(0, 7, dx, -6); dot(dx, -6, 3, false); } }
  else { cx2.beginPath(); cx2.moveTo(0, -r); cx2.lineTo(r, 0); cx2.lineTo(0, r); cx2.lineTo(-r, 0); cx2.closePath(); cx2.stroke(); }
  cx2.restore();
}
function seek(i) { let k = 0; while (k + 1 < n && lines[k].i < i) k++; return k + 1; }
function draw() {
  const line = lines[t - 1], before = lines[Math.max(t - 2, 0)], step = Math.max(1, line.i - before.i);
  const held = new Set(line.held.map(h => h[0] + ":" + h[1]));
  const frozen = new Set(line.frozen), turned = new Map();
  for (let back = 0; back < 8 && t - 1 - back >= 0; back++) for (const i of lines[t - 1 - back].turned) if (!turned.has(i)) turned.set(i, back);
  let wholeTurn = null; for (const top of tops) if (line.i >= top && line.i < top + 12 * step) wholeTurn = (line.i - top) / step;
  const lens = line.X.map(length), lenMin = Math.min(...lens), lenSpan = Math.max(Math.max(...lens) - lenMin, 1e-9);
  lay(line);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (const b of bangs) if (line.i >= b && line.i < b + 12 * step) {
    const age = (line.i - b) / step, reach = (0.08 + 0.05 * age) * canvas.width, cx = canvas.width / 2, cy = canvas.height / 2;
    ctx.strokeStyle = "#fde68a"; ctx.globalAlpha = Math.max(0, 1 - age / 12); ctx.lineWidth = 2;
    for (let r = 0; r < 24; r++) { const ang = r * Math.PI / 12 + age * 0.1, inner = reach * (0.35 + 0.15 * (r % 2)); ctx.beginPath(); ctx.moveTo(cx + Math.cos(ang) * inner, cy + Math.sin(ang) * inner); ctx.lineTo(cx + Math.cos(ang) * reach, cy + Math.sin(ang) * reach); ctx.stroke(); }
    ctx.globalAlpha = 1;
  }
  ctx.lineCap = "round";
  for (let i = 0; i < spots.length; i++) for (let a = 0; a < 3; a++) {
    const j = neighbour(i, a);
    if (j < 0) continue;
    const isHeld = held.has(i + ":" + a), rel = ((lens[i] + lens[j]) / 2 - lenMin) / lenSpan;
    ctx.strokeStyle = isHeld ? wall : "rgba(154,158,168," + (0.2 + 0.7 * rel) + ")";
    ctx.lineWidth = isHeld ? 4 : 0.8 + 3 * rel;
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
    const r = 2.5 + 5 * (line.content[i] - cmin) / Math.max(cmax - cmin, 1);
    ctx.fillStyle = turned.has(i) && turned.get(i) === 0 ? "#f59e0b" : "#4ade80";
    ctx.beginPath(); ctx.arc(spots[i][0], spots[i][1], r, 0, 2 * Math.PI); ctx.fill();
    if (frozen.has(i)) { ctx.fillStyle = "rgba(0,0,0,0.55)"; ctx.beginPath(); ctx.arc(spots[i][0], spots[i][1], r + 14, 0, 2 * Math.PI); ctx.fill(); ctx.fillStyle = "#000000"; ctx.beginPath(); ctx.arc(spots[i][0], spots[i][1], r + 2, 0, 2 * Math.PI); ctx.fill(); ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(spots[i][0], spots[i][1], r + 4, 0, 2 * Math.PI); ctx.stroke(); }
    if (turned.has(i)) { ctx.globalAlpha = 1 - turned.get(i) / 8; ctx.strokeStyle = "#f59e0b"; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(spots[i][0], spots[i][1], r + 5, 0.2 * Math.PI, 1.7 * Math.PI); ctx.stroke(); ctx.fillStyle = "#f59e0b"; ctx.beginPath(); const ax = spots[i][0] + (r + 5) * Math.cos(0.2 * Math.PI), ay = spots[i][1] + (r + 5) * Math.sin(0.2 * Math.PI); ctx.moveTo(ax, ay); ctx.lineTo(ax - 5, ay - 5); ctx.lineTo(ax + 3, ay - 6); ctx.closePath(); ctx.fill(); ctx.globalAlpha = 1; }
  }
  const recent = new Map(), span = new Map();
  for (const k of D.clicks) {
    if (k.i > line.i) break;
    const id = k.at, key = id + ":" + k.line;
    if (k.i > line.i - 24 * step) { const m = recent.get(id) || new Map(); m.set(k.line, (m.get(k.line) || 0) + 1); recent.set(id, m); }
    const sp = span.get(key); if (!sp) span.set(key, [k.i, k.i, 1]); else { sp[1] = k.i; sp[2]++; }
  }
  for (const [id, m] of recent) {
    let best = -1, count = 0, total = 0; for (const [l, n] of m) { total += n; if (n > count) { count = n; best = l; } }
    const sp = spots[id], r = 6 + Math.min(6, total);
    ctx.fillStyle = tone(best); ctx.globalAlpha = 0.18 + 0.03 * Math.min(10, total); ctx.beginPath(); ctx.arc(sp[0], sp[1], r, 0, 2 * Math.PI); ctx.fill(); ctx.globalAlpha = 1;
  }
  for (const [key, sp] of span) if (sp[1] > line.i - 24 * step && sp[1] - sp[0] >= 60 * step && sp[2] >= 4) {
    const id = parseInt(key), s = spots[id]; ctx.strokeStyle = tone(parseInt(key.split(":")[1])); ctx.lineWidth = 1.8; ctx.beginPath(); ctx.arc(s[0], s[1], 10, 0, 2 * Math.PI); ctx.stroke();
  }
  for (const k of D.clicks) if (k.i <= line.i && k.i > line.i - 4 * step) {
    const s = spots[k.at], age = (line.i - k.i) / step, fade = 1 - age / 4;
    ctx.globalAlpha = fade;
    ctx.fillStyle = k.from === null ? "#5f97ea" : tone(k.from);
    ctx.beginPath(); ctx.arc(s[0], s[1], 2 + Math.min(5, k.levels / 3), 0, 2 * Math.PI); ctx.fill();
    ctx.strokeStyle = tone(k.line); ctx.lineWidth = 1.8;
    ctx.beginPath(); ctx.arc(s[0], s[1], 7 + 3 * age, 0, 2 * Math.PI); ctx.stroke();
    if (k.children) for (let h = 0; h < 2; h++) {
      const sq = spots[k.children[h]];
      ctx.beginPath(); ctx.moveTo(s[0], s[1]); ctx.lineTo(sq[0], sq[1]); ctx.stroke();
      ctx.fillStyle = "#07080a"; ctx.beginPath(); ctx.arc(sq[0], sq[1], 7, 0, 2 * Math.PI); ctx.fill();
      ctx.beginPath(); ctx.arc(sq[0], sq[1], 7, 0, 2 * Math.PI); ctx.stroke();
      ctx.fillStyle = tone(k.line); ctx.font = "bold 11px monospace"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(h === 0 ? "-" : "+", sq[0], sq[1]);
    }
    ctx.globalAlpha = 1;
  }
  if (wholeTurn !== null) {
    const reach = (0.22 + 0.02 * wholeTurn) * canvas.width; ctx.strokeStyle = "#f59e0b"; ctx.globalAlpha = 1 - wholeTurn / 12; ctx.lineWidth = 6; ctx.setLineDash([14, 10]);
    ctx.beginPath(); ctx.arc(canvas.width / 2, canvas.height / 2, reach, 0, 2 * Math.PI); ctx.stroke(); ctx.setLineDash([]); ctx.globalAlpha = 1;
  }
  labels.innerHTML = "";
  let free = 0;
  const edge = [Math.min(...spots.map(p => p[0])), Math.max(...spots.map(p => p[0]))];
  if (wholeTurn !== null) {
    const div = document.createElement("div"); div.className = "label"; div.style.fontSize = "16px"; div.style.borderLeftColor = "#f59e0b"; div.style.color = "#f59e0b";
    div.innerHTML = "every Node turns at once<small>the clocks reversed at the top, interval " + (line.i - wholeTurn * step) + "</small>";
    div.style.right = "16px"; div.style.top = "16px";
    labels.appendChild(div);
  }
  const placed = [];
  function settle(x, y) {
    for (let moved = true; moved;) { moved = false; for (const q of placed) if (Math.abs(q[0] - x) < 220 && Math.abs(q[1] - y) < 42 && q[1] + 42 > y) { y = q[1] + 42; moved = true; } }
    placed.push([x, y]); return y;
  }
  for (const b of bangs) if (line.i >= b && line.i < b + 12 * step) {
    const div = document.createElement("div"); div.className = "label bang";
    div.innerHTML = "Big Bang<small>the board at its zero and rising, interval " + b + "</small>";
    div.style.left = "16px"; div.style.top = "16px";
    labels.appendChild(div);
  }
  const fresh = D.events.filter(e => e.i !== null && e.i <= line.i && e.i > line.i - 60 * step).slice(-4);
  for (const e of fresh) {
    const div = document.createElement("div"); div.className = "label"; div.style.borderLeftColor = colour(e.gate); div.style.color = colour(e.gate);
    div.innerHTML = e.label + "<small>" + e.numbers + "</small>";
    const click = e.node ? null : D.clicks.find(k => k.i === e.i), node = e.node || (click ? click.node : null);
    if (node) {
      const s = spots[node[0] * c * c + node[1] * c + node[2]], L = colour(e.gate);
      const right = edge[1] + 24 + 360 <= canvas.width, x0 = right ? edge[1] + 24 : Math.max(8, edge[0] - 24 - 360);
      const y = settle(x0, Math.max(8, Math.min(s[1] - 18, canvas.height - 44)));
      ctx.strokeStyle = L; ctx.lineWidth = 1.2; ctx.setLineDash([3, 4]); ctx.beginPath(); ctx.moveTo(s[0], s[1]); ctx.lineTo(right ? x0 + 12 : x0 + 348, y + 18); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = L; ctx.beginPath(); ctx.arc(s[0], s[1], 3, 0, 2 * Math.PI); ctx.fill();
      glyph(e.gate, right ? x0 + 14 : x0 + 346, y + 18);
      div.style.left = (right ? x0 + 30 : x0) + "px"; div.style.top = y + "px";
    } else { const fy = canvas.height - 48 - 40 * free++; glyph(e.gate, 24, fy + 18); div.style.left = "40px"; div.style.top = fy + "px"; }
    labels.appendChild(div);
  }
  cursor.style.left = (100 * (line.i - 1) / Math.max(N - 1, 1)) + "%";
  panel(line.i);
  now.innerHTML = "";
  for (const b of bangs) if (line.i >= b && line.i < b + 12 * step) { const s = document.createElement("span"); s.className = "era"; s.textContent = "Big Bang at " + b; now.appendChild(s); }
  for (const e of D.events.filter(e => e.i !== null && e.i <= line.i && e.i > line.i - 60 * step).slice(-5)) { const s = document.createElement("span"); s.style.setProperty("--c", colour(e.gate)); s.textContent = e.label + " (" + e.i + ")"; now.appendChild(s); }
  let up = 0, down = 0; for (let i = 0; i < line.X.length; i++) { if (line.X[i] > before.X[i]) up++; else if (line.X[i] < before.X[i]) down++; }
  const course = t === 1 ? "the seed" : up === line.X.length ? "every clock's volume rising" : down === line.X.length ? "every clock's volume falling" : up + " rising, " + down + " falling, " + (line.X.length - up - down) + " at rest";
  where.textContent = "interval " + line.i + " of " + N + (D.stride > 1 ? " (1 of every " + D.stride + " intervals kept)" : "") + "; " + course;
}
let hold = 0, slow = 0, beat = 0;
function tick() {
  document.body.classList.toggle("playing", playing);
  if (playing && hold > 0) hold--;
  else if (playing && slow > 0 && (++beat % 4) !== 0) slow--;
  else if (playing) { if (slow > 0) slow--; t = t % n + 1; draw(); const now = lines[t - 1].i, before = t > 1 ? lines[t - 2].i : 0; if (D.events.some(e => e.i !== null && e.i > before && e.i <= now) || bangs.some(b => b > before && b <= now)) { hold = speed; slow = 4 * speed; } }
  setTimeout(tick, MS / speed);
}
for (const [from, to, g, label] of spans) {
  const d = document.createElement("div"); d.className = "era"; d.style.left = (100 * (from - 1) / Math.max(N - 1, 1)) + "%"; d.style.width = (100 * (to - from) / Math.max(N - 1, 1)) + "%";
  d.style.background = g === "4" ? "rgba(244,114,182,0.18)" : g === "5" ? "rgba(253,230,138,0.14)" : "rgba(95,151,234,0.16)"; d.title = label + " from " + from; bar.appendChild(d);
}
for (const e of D.events) if (e.i !== null) {
  const d = document.createElement("div"); d.className = "tick"; d.style.left = (100 * (e.i - 1) / Math.max(N - 1, 1)) + "%"; d.title = e.label + " at " + e.i + ": " + e.numbers; bar.appendChild(d);
}
for (const b of bangs) { const d = document.createElement("div"); d.className = "tick"; d.style.left = (100 * (b - 1) / Math.max(N - 1, 1)) + "%"; d.style.background = "#f59e0b"; d.title = "Big Bang at " + b; bar.appendChild(d); }
for (const i of D.births) { const d = document.createElement("div"); d.className = "birth"; d.style.left = (100 * (i - 1) / Math.max(N - 1, 1)) + "%"; d.title = "a birth at " + i; bar.appendChild(d); }
bar.addEventListener("click", ev => { const r = bar.getBoundingClientRect(); t = seek(1 + Math.round((N - 1) * (ev.clientX - r.left) / r.width)); playing = false; draw(); });
document.getElementById("play").addEventListener("click", () => { playing = !playing; });
document.addEventListener("keydown", ev => { if (ev.key === " ") { ev.preventDefault(); playing = !playing; } });
document.getElementById("info").addEventListener("click", () => { document.body.classList.toggle("info"); });
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
    """The seed's lays as they are: a lone lay whole with its centre; lays alike in everything but their centre folded into one line with their count, so a seed laid at every Node reads as one line."""
    found: dict[str, list[Any]] = {}
    for lay in seed:
        key = json.dumps({k: v for k, v in lay.items() if k != "centre"})
        found.setdefault(key, [lay, 0])[1] += 1
    return [json.dumps(lay) if n == 1 else f"{key} at {n} centres" for key, (lay, n) in found.items()]


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


CLASSES = {
    "SHOWN": "shown",
    "SHOWN in part": "part",
}  # the list's style per kind the decoder writes; every other kind "not"


def data_of(record: dict[str, Any], reading: list[dict[str, Any]]) -> dict[str, Any]:
    """The page's data from the record and the reading: the Node lines, the clicks (every birth and credit as one short list: the interval, the Node's index, the row, the levels taken, the taken row or -1, a birth's two children's indices or 0), the births' intervals (numbered on the bar), the reading's event lines."""
    events = next((line["events"] for line in reading if "events" in line), [])
    gates = [
        [key, row["kind"], CLASSES.get(row["kind"], "not"), row["verdict"], row["label"]]
        for line in reading
        for key, row in line.items()
        if isinstance(row, dict) and "verdict" in row and key[:1].isdigit()
    ]
    eras = next((line["the eras"] for line in reading if "the eras" in line), {})
    decoder = next((line["the decoder"] for line in reading if "the decoder" in line), {})
    board = next((v for k, v in decoder.items() if k.startswith("rows read from the Node lines")), [])
    cube = int(record["cube"])

    def index(node: list[int]) -> int:
        return int(node[0]) * cube * cube + int(node[1]) * cube + int(node[2])

    clicks = [
        [
            e["i"],
            index(e["node"]),
            e.get("line", e.get("line_pair", 0)),
            int(e.get("levels", 0)),
            e.get("taken_row", -1),
            [index(e["minus"]), index(e["plus"])] if e["event"] == "birth" else 0,
        ]
        for e in record["log"]
        if e["event"] in ("birth", "credit")
    ]
    births = sorted({e["i"] for e in record["log"] if e["event"] == "birth"})
    named = {int(e["i"]) for e in events if e["i"] is not None} | {int(k[0]) for k in clicks}
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
        "births": births,
        "events": events,
        "gates": gates,
        "board": board,
        "eras": eras,
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
        '<div id="top"><div id="title">'
        + title
        + '<small>the record and its reading, from the seed alone</small></div><button id="info" title="the two files and the marks">i</button></div>\n'
        '<div id="card"><h3>the two files</h3><pre>' + header_of(record) + "</pre><h3>the marks</h3>"
        "green dot: a Node, its size the content; blue arrow: the gap-0 current along the Link (the gap-0 row); coloured halo: matter clicking at the Node, the colour its row; coloured ring: a body bound at its Node; a click: the ring in the colour of its row, the dot inside the levels taken, blue from the gap-0 row, else in the colour of the taken row; a birth: the Node of the take joined to its two children, - and +; orange arc with an arrowhead: the Node turned, its clock reversed at the top; a black disc in a white ring with a dark halo: the Node frozen, the horizon; thick white Link: at the wall; yellow: a gate of the phenomena as it first shows, lit in the list at its interval; the bands of the bar: the spans from each bang, from the era of matter and from the acceleration, as the reading names them; the verdicts in the reading file beside the record</div>\n"
        '<div id="main"><div id="stage"><canvas id="board" width="320" height="320"></canvas><div id="labels"></div></div>\n'
        '<div id="side"><h2><span>the gates of the phenomena</span><b id="count"></b></h2><div id="gates"></div></div></div>\n'
        '<div id="bar"><div id="cursor"></div></div>\n<div id="now"></div>\n'
        '<div id="row"><button id="play" title="play / pause"><span class="tri"></span><span class="bars"></span></button><button id="slower">slower</button><button id="faster">faster</button><span id="where"></span>'
        "</div>\n"
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
