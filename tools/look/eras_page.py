"""The eras' page, a page tool beside tools/look/page.py in its dark tokens (docs/ENGINE.md section 6; DESIGN section 4 (g)): one self-contained HTML page from the log tools/eras.py writes (`<world>.eras.jsonl`, one JSON line per interval after the header) and, where the folder holds them, the blind (`--blind <world>.blind.json`, its rows in a table and, under its optional key `course` as rows of `interval`, `U` and `velocity`, the model's course dashed beside the board's) and the notes (`--notes notes.md`, a Markdown text rendered as one prose section, the page's leading panel), and the clicks log the same run kept (`--clicks <world>.clicks.jsonl`, tools/eras.py's second file: the detector's clicks drawn as their magnitude on a log axis, the quanta at the detector's Nodes with its time line, and the fifth act's fires where the eras log carries them; history kept one way, nothing run back). The page draws, against the interval, U = level / Gamma and H = v / Gamma of the first held row of the content with the eras shaded as the board reads them (the family whose write's sum is largest at the interval sources the era, the crossing of two writes the transition); q_p from the slope of 1 / v over spans and nothing else (the estimator on the integers' staircase, d(1 / v) / dt = n_eff / (2 Gamma), q_board = n_eff / 2 - 1, q_p = q_board - 1, the span picked on the page) with the blind's bands where the blind names them; the families' writes on a log axis; the constraint's residual R beside the tracker's 2 (n_eff - c) / (2 c - n_eff) at the Node-mean weight; the hill's weight's least, largest and Node-mean; the seed Node's share within one Link per family, the well's depth, the seed's contrast U_seed - U_void and the clock ratio e^(-(U_seed - U_void)) (the wall observer's clock against the void's, a reading); the rulers at the far Node. The legend names what is an input (the pairs, the four integers, the seed's counts, light's amplitude) and what the board reads by itself (every curve), the hypotheses under which the course is nature's by name, the crawl once as the integers' end where the velocity falls below one level per interval (the floor, the crawl and the pulses one phenomenon), the coast as the reals' mean, the stop as the other booking's end under the rounded factor (named, not shown) and nature's late acceleration as MISSING. Every number on the page is the log's or the blind's; the page computes the floats named above and nothing of the law; the board's own frames are the look page's (`<world>.look.html` by tools/look/record.py and page.py), linked where it stands beside the page.

The bangs (the owner's word of 2026-10-23): every bang is marked and numbered, the seed at the first interval bang 1 and each later bang the interval the board's volume velocity turns from falling to rising after the fifth act fired since the last bang (the return), the tops numbered beside, the horizon's spans shaded with the count of Links held at the wall (the black hole, in the owner's words), and with `--nodes <world>.nodes.jsonl` (tools/eras.py's Nodes' log, X at every Node) the least X over the board per interval drawn on a log axis against the floor X_f = volume_of(Gamma, -Gamma) by the engine's own `swap.floor_of`, so the distance to X = 0 is seen; readings of the logs, nothing computed of the law.

python tools/look/eras_page.py <world>.eras.jsonl [--blind <world>.blind.json] [--notes notes.md] [--clicks <world>.clicks.jsonl] [--nodes <world>.nodes.jsonl] [--span 50] [--out <world>.html]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from captions import (  # noqa: E402  (the look's own module, beside this tool)
    captions_of,
    ledger_of,
    legend_html,
    legend_of,
    parse_log,
)

PAGE = Path(__file__).with_name("page.py")
TOKENS = re.search(r":root \{.*?\n\}\n", PAGE.read_text(encoding="utf-8"), re.S)
assert TOKENS is not None, (
    "tools/look/page.py holds the page's tokens, the one block the eras page shares"
)

TEMPLATE = """<meta charset="utf-8">
<title>{{TITLE}}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* The page's tokens are tools/look/page.py's one block, shared bit for bit; the layout below is this page's own. */
{{TOKENS}}
* { box-sizing: border-box; }
body { margin: 0; padding-inline: var(--gutter); padding-block: var(--pad); background: var(--bg); color: var(--fg); font: var(--text)/1.45 var(--font-body); }
h1 { font-size: var(--title); margin: 0; font-weight: 600; text-wrap: balance; }
h2 { font-size: var(--text); margin: 0 0 6px; font-weight: 600; }
header { display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--gap); margin-bottom: var(--gap); }
header .verdict { font-family: var(--font-mono); color: var(--muted); }
.page { display: grid; grid-template-columns: repeat(auto-fit, minmax(var(--side-min), 1fr)); gap: var(--gap); align-items: start; }
.wide { grid-column: 1 / -1; }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: var(--pad); min-width: 0; }
.graph { display: grid; grid-template-columns: minmax(0, 1fr); gap: 2px; min-width: 0; margin-bottom: var(--gap); }
.graph .caption { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px var(--gap); font-size: var(--small); color: var(--muted); overflow-wrap: anywhere; }
.graph .caption b { color: var(--fg); font-weight: 600; }
.graph svg { width: 100%; height: auto; display: block; }
.legend { display: flex; flex-wrap: wrap; gap: 4px var(--gap); font-size: var(--small); }
.legend i { display: inline-block; width: 14px; height: 0; border-top: 2px solid; vertical-align: middle; margin-right: 4px; }
.legend i.dashed { border-top-style: dashed; }
.legend i.band { height: 10px; border: 0; opacity: 0.35; }
.picker { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: var(--small); margin-bottom: var(--gap); }
.picker input { width: 6ch; padding: 3px 6px; font: inherit; color: var(--fg); background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); }
.words { font-size: var(--small); color: var(--muted); }
.words b { color: var(--fg); font-weight: 600; }
.prose { max-width: 90ch; }
.prose p, .prose ol, .prose ul { margin: 0 0 var(--gap); }
.prose ol, .prose ul { padding-left: 1.6em; }
.prose h3 { font-size: var(--text); font-weight: 600; margin: var(--gap) 0 6px; }
.prose code { font-family: var(--font-mono); font-size: var(--small); }
table { border-collapse: collapse; width: 100%; font-size: var(--small); }
th, td { text-align: left; padding: 3px 6px; border-bottom: 1px solid var(--line); vertical-align: top; font-variant-numeric: tabular-nums; }
th { color: var(--muted); font-weight: 600; }
td.num { font-family: var(--font-mono); }
.scroll { overflow-x: auto; }
</style>
<script id="log" type="application/json">{{LOG}}</script>
<script id="blind" type="application/json">{{BLIND}}</script>
<script id="notes" type="application/json">{{NOTES}}</script>
<script id="clicks" type="application/json">{{CLICKS}}</script>
<script id="span" type="application/json">{{SPAN}}</script>
<script id="least" type="application/json">{{LEAST}}</script>
<script id="captions" type="application/json">{{CAPTIONS}}</script>
<header>
  <h1 id="title"></h1>
  <span class="verdict">lattice reading</span>
  <span class="verdict" id="verdict"></span>
  <a class="verdict" id="look" href="{{LOOK}}" hidden>the board's frames (the look page)</a>
</header>
<div class="page">
  <section class="panel wide" id="notes-box" hidden><h2 id="notes-heading">Notes</h2><div class="prose" id="notes-prose"></div></section>
  <section class="panel wide" id="captions-box" hidden><h2>The events, in the viewer's words (every caption read from the logs; the interval first)</h2><div class="prose scroll" id="captions-list"></div></section>
{{LEGEND}}
  <section class="panel wide">
    <div class="picker"><label>the estimator's span <input type="number" id="span-input" min="2" step="1"></label><span class="words">intervals: d(1 / v) / dt = n_eff / (2 Gamma), q_board = n_eff / 2 - 1, q_p = q_board - 1, the second difference over short spans failing on the integers' staircase</span></div>
    <div class="graph" id="course"></div>
    <div class="graph" id="deceleration"></div>
    <div class="words" id="eras-words"></div>
  </section>
  <section class="panel wide"><h2>The least X over the board against the floor X_f, the distance to X = 0 (a log axis)</h2><div class="graph" id="least-x"></div><div class="words" id="least-words"></div></section>
  <section class="panel"><h2>The writes per family, summed over the Nodes (a log axis)</h2><div class="graph" id="writes"></div></section>
  <section class="panel"><h2>The constraint's residual</h2><div class="graph" id="residual"></div></section>
  <section class="panel"><h2>The mix's exponent</h2><div class="graph" id="exponent"></div></section>
  <section class="panel"><h2>The seed: its share within one Link and its well</h2><div class="graph" id="seed"></div><div class="graph" id="well"></div></section>
  <section class="panel"><h2>The clocks: the seed Node against the void</h2><div class="graph" id="contrast"></div><div class="graph" id="clock"></div></section>
  <section class="panel"><h2>The rulers at the far Node</h2><div class="graph" id="rulers"></div></section>
  <section class="panel"><h2>The tension lines' means and the Links' factors</h2><div class="graph" id="tensions"></div><div class="graph" id="links"></div></section>
  <section class="panel"><h2>The quanta over the board, per family (a log axis)</h2><div class="graph" id="quanta"></div></section>
  <section class="panel wide" id="legend-box"><h2>What is an input and what the board reads by itself</h2><div class="words" id="legend-words"></div></section>
  <section class="panel wide" id="blind-box" hidden><h2>The blind, written before the run</h2><div class="scroll" id="blind-table"></div></section>
  <section class="panel wide" id="clicks-box" hidden><h2>The detector's clicks, history kept one way (the clicks log beside the eras log)</h2><div class="graph" id="detector-quanta"></div><div class="graph" id="detector-clicks"></div><div class="graph" id="fires"></div><div class="words" id="clicks-words"></div></section>
</div>
<script>
const LOG = JSON.parse(document.getElementById('log').textContent);
const BLIND = JSON.parse(document.getElementById('blind').textContent);
const NOTES = JSON.parse(document.getElementById('notes').textContent);
const CLICKS = JSON.parse(document.getElementById('clicks').textContent);
let SPAN = JSON.parse(document.getElementById('span').textContent);
const LEAST = JSON.parse(document.getElementById('least').textContent);
const CAPTIONS = JSON.parse(document.getElementById('captions').textContent) || [];
const HEAD = LOG[0], LINES = LOG.slice(1).filter(l => l.rows), REFUSED = LOG.slice(1).find(l => l.refused);
const GAMMA = HEAD.node_clock, ROW = HEAD.held[0];
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const token = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
const size = name => parseFloat(token(name));
const TONES = token('--click-tones').split(',').map(s => s.trim());
const format = v => v === null || v === undefined || Number.isNaN(v) ? 'none' : Math.abs(v) >= 1000 ? Math.round(v).toLocaleString() : Math.abs(v) >= 10 ? v.toFixed(1) : Math.abs(v) >= 1 ? v.toFixed(3) : v.toPrecision(3);
const intervals = LINES.map(l => l.interval);
const rows = LINES.map(l => l.rows[ROW]);
const families = Object.keys(rows[0].writes);
const SEED = HEAD.seed || 'light';  // the seed row's name from the header (the massless point; 'light' the former files' row)
const colour = name => name === SEED || name === 'light' || name === 'photon' ? token('--light') : name === 'dust' ? token('--matter') : TONES[(families.indexOf(name) + 2) % TONES.length];
function era(i) {  // the family whose write is largest at the interval sources the era
  const writes = rows[i].writes; let best = null;
  for (const name of families) if (best === null || writes[name] > writes[best]) best = name;
  return best;
}
function spans(span) {  // the estimator on the staircase: the slope of 1 / v over spans, where v is above 0 at both ends
  const found = [];
  for (let s = 0; s + span < rows.length; s += span) {
    const a = rows[s].velocity, b = rows[s + span].velocity;
    if (a <= 0 || b <= 0) { found.push({t: s, q_p: null, n_eff: null}); continue; }
    const n_eff = 2 * GAMMA * ((1 / b - 1 / a) / span);
    found.push({t: s, n_eff, q_p: n_eff / 2 - 2});
  }
  return found;
}
function graph(box, title, series, options = {}) {
  const W = size('--graph-width') * 2, H = size('--graph-height') * 2, pad = size('--graph-pad') * 2, left = pad + 48;
  const xs = options.xs || intervals, xmax = Math.max(...xs), xmin = Math.min(...xs);
  const log = !!options.log, tr = v => log ? Math.log10(v) : v;
  let low = Infinity, high = -Infinity;
  for (const s of series) for (const v of s.values) { if (v === null || v === undefined || Number.isNaN(v) || (log && v <= 0)) continue; if (tr(v) < low) low = tr(v); if (tr(v) > high) high = tr(v); }
  for (const b of options.bands || []) { low = Math.min(low, b.low); high = Math.max(high, b.high); }
  if (!isFinite(low)) { box.innerHTML = `<div class="caption"><b>${esc(title)}</b><span>nothing to draw</span></div>`; return; }
  if (low === high) { low -= 1; high += 1; }
  const px = x => left + (xmax > xmin ? (x - xmin) / (xmax - xmin) : 0) * (W - left - pad), py = v => pad + (high - tr(v)) / (high - low) * (H - 2 * pad);
  let body = '';
  for (const shade of options.shades || []) body += `<rect x="${px(shade.from).toFixed(1)}" y="${pad}" width="${Math.max(0, px(shade.to) - px(shade.from)).toFixed(1)}" height="${H - 2 * pad}" fill="${shade.colour}" opacity="0.14"/>`;
  for (const b of options.bands || []) body += `<rect x="${left}" y="${py(log ? Math.pow(10, b.high) : b.high).toFixed(1)}" width="${W - left - pad}" height="${Math.max(0, py(log ? Math.pow(10, b.low) : b.low) - py(log ? Math.pow(10, b.high) : b.high)).toFixed(1)}" fill="${token('--blind')}" opacity="0.18"/>`;
  body += `<rect x="${left}" y="${pad}" width="${W - left - pad}" height="${H - 2 * pad}" fill="none" stroke="${token('--line')}"/>`;
  if (!log && low < 0 && high > 0) body += `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}" stroke-dasharray="2 3"/>`;
  const label = (text, x, y, anchor) => `<text x="${x}" y="${y}" fill="${token('--muted')}" font-size="${size('--small')}" font-family="${token('--font-mono')}" text-anchor="${anchor}">${esc(text)}</text>`;
  body += label(log ? format(Math.pow(10, high)) : format(high), left - 4, pad + size('--small') * 0.4, 'end') + label(log ? format(Math.pow(10, low)) : format(low), left - 4, H - pad, 'end');
  body += label(xmin, left, H - 1, 'start') + label(xmax, W - pad, H - 1, 'end');
  for (const s of series) {
    const xx = s.xs || xs, runs = [[]];
    s.values.forEach((v, i) => { if (v === null || v === undefined || Number.isNaN(v) || (log && v <= 0)) { if (runs[runs.length - 1].length) runs.push([]); } else runs[runs.length - 1].push(`${px(xx[i]).toFixed(1)},${py(v).toFixed(1)}`); });
    for (const run of runs) if (run.length) body += `<polyline points="${run.join(' ')}" fill="none" stroke="${s.colour}" stroke-width="1.6" ${s.dashed ? 'stroke-dasharray="4 3"' : ''}/>`;
  }
  for (const mark of options.marks || []) body += `<line x1="${px(mark.at).toFixed(1)}" x2="${px(mark.at).toFixed(1)}" y1="${pad}" y2="${H - pad}" stroke="${mark.colour || token('--bound')}" stroke-dasharray="2 3"/>` + label(mark.name, px(mark.at) + 3, pad + size('--small'), 'start');
  const legend = series.map(s => `<span><i class="${s.dashed ? 'dashed' : ''}" style="border-color:${s.colour}"></i>${esc(s.name)}</span>`).join('') + (options.shades || []).filter((s, i, all) => all.findIndex(o => o.name === s.name) === i).map(s => `<span><i class="band" style="background:${s.colour}"></i>${esc(s.name)}</span>`).join('');
  box.innerHTML = `<div class="caption"><b>${esc(title)}</b><span>${esc(options.kind || 'lattice reading')}</span></div><div class="legend">${legend}</div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(title)}">${body}</svg>`;
}
function shades() {  // the eras as the board reads them: runs of one sourcing family
  const found = []; let from = 0;
  for (let i = 1; i <= rows.length; i++) if (i === rows.length || era(i) !== era(from)) { found.push({from: intervals[from], to: intervals[i - 1], name: `${era(from)}'s era`, colour: colour(era(from))}); from = i; }
  return found;
}
function bangs() {  // the volume's tops and returns where the row carries its volume: a weak extremum of the board's volume, the larger top or the deeper return kept where two of a kind follow each other
  if (!rows[0] || rows[0].volume === undefined) return [];
  const found = [];
  for (let i = 1; i < rows.length - 1; i++) {
    const p = rows[i - 1].volume, q = rows[i].volume, r = rows[i + 1].volume;
    let kind = null;
    if (q >= p && q >= r && (q > p || q > r)) kind = 'top'; else if (q <= p && q <= r && (q < p || q < r)) kind = 'return';
    if (!kind) continue;
    const e = {kind, at: intervals[i], volume: q, U: rows[i].U};
    if (found.length && found[found.length - 1].kind === kind) { if ((kind === 'top' && q > found[found.length - 1].volume) || (kind === 'return' && q < found[found.length - 1].volume)) found[found.length - 1] = e; }
    else found.push(e);
  }
  return found;
}
function returns() {  // the bangs as the owner reads them: the seed at the first interval is bang 1; each later bang the interval the volume's velocity turns from falling to rising after the fifth act fired since the last bang (the return); the fires counted from the eras log
  if (!rows[0] || rows[0].volume === undefined) return [];
  const found = [{at: intervals[0], volume: rows[0].volume, fires: LINES[0].fires || 0}];
  let fired = 0;
  for (let i = 2; i < rows.length; i++) {
    fired += LINES[i - 1].fires || 0;
    const fall = rows[i - 1].volume - rows[i - 2].volume, rise = rows[i].volume - rows[i - 1].volume;
    if (fall < 0 && rise > 0 && fired > 0) { found.push({at: intervals[i - 1], volume: rows[i - 1].volume, fires: fired}); fired = 0; }
  }
  return found;
}
function horizons() {  // the horizon's spans: runs of intervals with Links held at the wall, each with its largest count (the black hole, in the owner's words; ALGEBRA.md, The horizon)
  const found = []; let from = -1, most = 0;
  for (let i = 0; i <= LINES.length; i++) {
    const n = i < LINES.length ? (LINES[i].horizon || 0) : 0;
    if (n > 0) { if (from < 0) from = i; most = Math.max(most, n); }
    else if (from >= 0) { found.push({from: LINES[from].interval, to: LINES[i - 1].interval, most, name: `the horizon: ${most} Links at the wall (the black hole)`, colour: token('--flash')}); from = -1; most = 0; }
  }
  return found;
}
function marks() {
  const found = [];
  returns().forEach((b, n) => found.push({at: b.at, name: `bang ${n + 1}`, colour: token('--fg')}));
  let tops = 0;
  for (const b of bangs()) if (b.kind === 'top') found.push({at: b.at, name: `top ${++tops}`, colour: token('--fg')});
  for (let i = 1; i < rows.length; i++) if (era(i) !== era(i - 1)) found.push({at: intervals[i], name: 'the crossing', colour: token('--fg')});
  for (const h of horizons()) found.push({at: h.from, name: `the horizon (${h.most} Links)`, colour: token('--flash')});
  const crawl = rows.findIndex(r => r.velocity < 1);
  if (crawl >= 0) found.push({at: intervals[crawl], name: 'the crawl', colour: token('--flash')});
  if (REFUSED) found.push({at: REFUSED.interval, name: 'refused', colour: token('--flash')});
  return found;
}
function draw() {
  document.getElementById('title').textContent = `${HEAD.world.replace('.json', '').replace(/_/g, ' ')}: the eras as the board reads them`;
  document.getElementById('verdict').textContent = REFUSED ? `REFUSED at ${REFUSED.interval}: ${REFUSED.refused.slice(0, 160)}` : `${LINES.length} intervals of ${HEAD.intervals}, the width ${HEAD.width}`;
  const course = BLIND && Array.isArray(BLIND.course) ? BLIND.course : null;
  const U = rows.map(r => r.U), H = rows.map(r => r.H);
  const series = [{name: 'U = level / Gamma', values: U, colour: token('--field')}, {name: 'H = v / Gamma', values: H.map(h => h * 100), colour: token('--focus')}];
  if (course) series.push({name: 'the blind\\'s U (the model, dashed)', values: course.map(c => c.U), xs: course.map(c => c.interval), colour: token('--blind'), dashed: true}, {name: 'the blind\\'s H x 100', values: course.map(c => c.velocity / GAMMA * 100), xs: course.map(c => c.interval), colour: token('--blind'), dashed: true});
  graph(document.getElementById('course'), 'U and H x 100 against the interval, the eras shaded, the horizon shaded in the flash colour', series, {shades: shades().concat(horizons()), marks: marks()});
  const q = spans(SPAN), bands = (BLIND && BLIND.q_p_bands) || [];
  graph(document.getElementById('deceleration'), `q_p from the slope of 1 / v over spans of ${SPAN} intervals`, [{name: 'q_p (the board)', values: q.map(s => s.q_p), xs: q.map(s => intervals[s.t]), colour: token('--fg')}, {name: 'n_eff (the board)', values: q.map(s => s.n_eff), xs: q.map(s => intervals[s.t]), colour: token('--muted'), dashed: true}], {xs: q.map(s => intervals[s.t]), shades: shades(), marks: marks(), bands: bands.map(b => ({low: b.low, high: b.high}))});
  const crawl = rows.findIndex(r => r.velocity < 1);
  const words = [`the eras by the largest write: ${shades().map(s => `${s.name} from ${s.from} to ${s.to}`).join('; ')}.`];
  const bangList = returns(), topList = bangs().filter(b => b.kind === 'top');
  words.push(`<b>The bangs</b>, ${bangList.length} over the run: ${bangList.map((b, n) => n === 0 ? `bang 1 at ${b.at} (the seed, ${b.fires} Nodes turned)` : `bang ${n + 1} at ${b.at} (the return after ${b.fires} Nodes turned by the fifth act since bang ${n})`).join('; ')}; the tops at ${topList.map(b => b.at).join(', ') || 'none'}; a bang is the interval the volume's velocity turns from falling to rising after the fifth act fired, read from the log.`);
  const spansOfWall = horizons();
  words.push(spansOfWall.length ? `<b>The horizon</b> (the black hole, in the owner's words): ${spansOfWall.map(h => `from ${h.from} to ${h.to}, up to ${h.most} Links held at the wall`).join('; ')}; the span shaded in the flash colour.` : 'No horizon within the run: no Link held at the wall.');
  words.push(crawl >= 0 ? `<b>The crawl</b> from the interval ${intervals[crawl]} (the velocity below one level per interval; the floor, the crawl and the pulses 0 to 1 to 0 at the mean rate s Gamma / n one phenomenon): the integers' end; the coast is the reals' mean.` : 'No crawl within the run: the velocity stayed at or above one level per interval.');
  words.push('The stop, the write\\'s death under the rounded factor (`factor: rounded`), is the other booking\\'s end, named and not shown; the end is never a cycle. Nature\\'s late acceleration is <b>MISSING</b> under the Node\\'s own hill (the remainders hand\\'s and the structures hand\\'s negatives); q_p never below 0 after the crossing is the blind\\'s clause.');
  document.getElementById('eras-words').innerHTML = words.join(' ');
  if (LEAST && LEAST.least_x.length) {
    graph(document.getElementById('least-x'), 'the least X over the board per interval against the floor X_f = volume_of(Gamma, -Gamma), the horizon shaded (log)', [{name: 'the least X over the board', values: LEAST.least_x, xs: LEAST.intervals, colour: token('--field')}, {name: `the floor X_f = ${LEAST.floor}`, values: LEAST.intervals.map(() => LEAST.floor), xs: LEAST.intervals, colour: token('--flash'), dashed: true}], {log: true, xs: LEAST.intervals, shades: horizons(), marks: marks()});
    const least = Math.min(...LEAST.least_x), at = LEAST.intervals[LEAST.least_x.indexOf(least)];
    document.getElementById('least-words').innerHTML = `<b>The least X over the board</b>, read from the Nodes log: ${format(least)} at the interval ${at}, ${(least / LEAST.floor).toFixed(1)} times the floor X_f = ${LEAST.floor} (ALGEBRA.md, The floor: a Node whose time line would fall below X_f turns as at the top); X = 0 lies below the floor and off the log axis, the distance to it the gap under the curve.`;
  } else document.getElementById('least-x').innerHTML = '<div class="caption"><b>the least X over the board</b><span>the Nodes log not given (--nodes)</span></div>';
  graph(document.getElementById('writes'), 'the writes per family into the row\\'s time line (log)', families.map(f => ({name: f, values: rows.map(r => r.writes[f]), colour: colour(f)})), {log: true, shades: shades(), marks: marks()});
  graph(document.getElementById('residual'), 'R_nat = (Gamma / 2) U\\'^2 / (SUM s_f / 3) - 1, the trace\\'s surface, and R_vol = X\\'^2 / (2 X X\\'\\') - 1, the volume form\\'s own constraint (E = 0 of its Lagrangian, reached from rest as -X_0 / X)', [{name: 'R_nat', values: rows.map(r => r.nature_residual === undefined ? null : r.nature_residual), colour: token('--fg')}, {name: 'R_vol', values: rows.map(r => r.volume_residual === undefined ? null : r.volume_residual), colour: token('--field')}], {marks: marks()});
  graph(document.getElementById('exponent'), 'n_eff, the mix\\'s exponent from the writes (the readings\\' pair P SUM S_f over SUM (P / n_f) S_f)', [{name: 'n_eff', values: rows.map(r => r.n_eff), colour: token('--fg')}], {marks: marks()});
  const quanta = Object.keys(LINES[0].quanta || {});
  graph(document.getElementById('seed'), 'the share within one Link of the seed Node, per family', quanta.map(f => ({name: f, values: LINES.map(l => l.quanta[f].share_within_one_link), colour: colour(f)})), {marks: marks()});
  graph(document.getElementById('well'), 'the well: the time line at the seed Node less the far Node\\'s (levels)', [{name: 'the well\\'s depth', values: rows.map(r => r.well), colour: token('--field')}], {marks: marks()});
  graph(document.getElementById('contrast'), 'U_seed - U_void: the seed Node\\'s level against the other Nodes\\' mean', [{name: 'the contrast', values: rows.map(r => r.contrast), colour: token('--field')}], {marks: marks()});
  graph(document.getElementById('clock'), 'N_seed / N_void = e^(-(U_seed - U_void)), the wall observer\\'s clock against the void\\'s', [{name: 'the clock ratio', values: rows.map(r => r.clock_ratio), colour: token('--focus')}], {marks: marks()});
  graph(document.getElementById('tensions'), 'the three tension lines\\' means over the Nodes (levels; the k = 0 mode of the axis lines)', ['x', 'y', 'z'].map((axis, a) => ({name: `the ${axis} tension line\\'s mean`, values: rows.map(r => r.tension_means ? r.tension_means[a] : null), colour: TONES[a]})), {marks: marks()});
  const linked = quanta.length && LINES[0].quanta[quanta[0]].links_far;
  graph(document.getElementById('links'), `the Links\\' factors (q_+ + q_-) / (2 Gamma) per axis at the far Node and the seed (${quanta[0] || ''}\\'s read)`, linked ? ['x', 'y', 'z'].flatMap((axis, a) => [{name: `${axis} at the far Node`, values: LINES.map(l => l.quanta[quanta[0]].links_far[a]), colour: TONES[a]}, {name: `${axis} at the seed`, values: LINES.map(l => l.quanta[quanta[0]].links_seed[a]), colour: TONES[a], dashed: true}]) : [], {marks: marks()});
  graph(document.getElementById('quanta'), 'the quanta over the board per family (the share read in the free unit; a wave pumped as the paces fall under it grows here)', quanta.map(f => ({name: f, values: LINES.map(l => l.quanta[f].quanta), colour: colour(f)})), {log: true, marks: marks()});
  const rulers = quanta.length && LINES[0].quanta[quanta[0]].rulers_far ? ['x', 'y', 'z'].map((axis, a) => ({name: `h_${axis} at the far Node`, values: LINES.map(l => l.quanta[quanta[0]].rulers_far ? l.quanta[quanta[0]].rulers_far[0] / l.quanta[quanta[0]].rulers_far[1][a] : null), colour: TONES[a]})) : [];
  graph(document.getElementById('rulers'), `the three rulers h_a = p_0 / p_a at the far Node (${quanta[0] || ''}'s read)`, rulers, {marks: marks()});
  const legend = [`<b>The inputs</b> (as in nature): the pairs of the universe file (the masses), the four integers Gamma ${GAMMA}, T ${HEAD.quantum_action}, the width ${HEAD.width} and the Link's unit, the seed's content (the whole packets' counts at one Node at the interval 1) and light's amplitude (the one number of the mix, the radiation-to-matter ratio at the seed).`,
    `<b>What the board reads by itself</b>: every curve on this page, from the engine's own integers (the mean level and its remainders, the writes, the mix's exponent, the two residuals' fractions, the shares, the seed Node's level); this page computes U, H, the slope of 1 / v over spans and the ratios named and nothing else.`,
    `<b>The hypotheses under their own names</b> (ALGEBRA.md): The board's interval is no observable; The mean's velocity is the content's; the carried momentum of the volume form (the massless row carrying X = Gamma (Gamma / p_0)^(d + 1), its write ((d + 1) X c + r) div (Gamma E_s T) at a wall that never moves, the level a reading of the record; the exponent ${HEAD.keys && HEAD.keys[ROW] && HEAD.keys[ROW].pressure === 'trace' ? 'the trace\\'s d + 1 = 4 under The stress\\'s trace is the time line\\'s' : 'd + 1 = 4'}); The form's own clock (the held row's key booking: form); The factor carried (the key factor: carried at the wall fixed per Node, the coast) against the law's rounding (the stop). The course is nature's sequence of q (radiation 1, dust 1 / 2) under them, with the toy's integers.`];
  document.getElementById('legend-words').innerHTML = legend.map(p => `<p>${p}</p>`).join('');
  const look = document.getElementById('look'); if (look.getAttribute('href')) look.hidden = false;
  if (BLIND) {
    document.getElementById('blind-box').hidden = false;
    const rowsOf = Array.isArray(BLIND.rows) ? BLIND.rows : Object.entries(BLIND).filter(([k, v]) => k !== 'course' && k !== 'q_p_bands').map(([k, v]) => ({reading: k, blind: typeof v === 'object' ? JSON.stringify(v) : v}));
    document.getElementById('blind-table').innerHTML = `<table><tr><th>reading</th><th>blind</th><th>status</th><th>fence</th><th>outcome</th></tr>${rowsOf.map(r => `<tr><td>${esc(r.reading || '')}</td><td class="num">${esc(typeof r.blind === 'object' ? JSON.stringify(r.blind) : (r.blind ?? ''))}</td><td>${esc(r.status || '')}</td><td>${esc(r.fence || '')}</td><td>${esc(r.outcome || '')}</td></tr>`).join('')}</table>`;
  }
  if (NOTES) renderNotes(NOTES);
  if (CAPTIONS.length) { document.getElementById('captions-box').hidden = false; document.getElementById('captions-list').innerHTML = `<ol>${CAPTIONS.map(c => `<li><b>${c.at}</b>: ${esc(c.words)}</li>`).join('')}</ol>`; }
  if (CLICKS) drawClicks();
}
function drawClicks() {  // the clicks log's lines: the clicks per family (the net current into the region, its magnitude on a log axis), the detector lines (the quanta at its Nodes, the time line there) and the fires the eras log carries; nothing computed but the sums
  document.getElementById('clicks-box').hidden = false;
  const detectors = [...new Set(CLICKS.map(l => l.node_detector).filter(Boolean))];
  const quantaOf = CLICKS.filter(l => l.event === 'detector');
  const names = quantaOf.length ? Object.keys(quantaOf[0].quanta) : [];
  const sum = a => Array.isArray(a) ? a.reduce((x, y) => x + y, 0) : null;
  const perInterval = (lines, at) => { const m = new Map(lines.map(l => [l.interval, l])); return intervals.map(t => m.has(t) ? at(m.get(t)) : null); };
  const quantaSeries = detectors.flatMap(d => names.map(f => ({name: `${f}'s quanta at ${d}'s Nodes`, values: perInterval(quantaOf.filter(l => l.node_detector === d), l => sum(l.quanta[f])), colour: colour(f)})));
  graph(document.getElementById('detector-quanta'), 'the quanta at the detector\\'s Nodes per family (the record\\'s share there), with the detector\\'s own time line X / Gamma', quantaSeries.concat(detectors.map(d => ({name: `X / Gamma at ${d}, the mean of its Nodes`, values: perInterval(quantaOf.filter(l => l.node_detector === d), l => l.X ? sum(l.X) / l.X.length / GAMMA : null), colour: token('--field'), dashed: true}))), {marks: marks(), kind: 'the clicks log'});
  const written = CLICKS.filter(l => l.event === 'credit' && l.before !== l.realised).map(l => ({at: l.interval, name: `click written (${l.realised || ''})`, colour: token('--flash')}));
  const clicks = CLICKS.filter(l => l.event === 'click');
  const clickSeries = detectors.flatMap(d => [...new Set(clicks.filter(l => l.node_detector === d).map(l => l.family))].map(f => ({name: `|click| of ${f} into ${d}`, values: perInterval(clicks.filter(l => l.node_detector === d && l.family === f), l => Math.abs(l.inflow)), colour: colour(f)})));
  graph(document.getElementById('detector-clicks'), 'the clicks: the net current of each family into the detector through its front Ports each interval, its magnitude (log); the clicks written on the lattice by an instrument body marked', clickSeries, {log: true, marks: marks().concat(written), kind: 'NODEDETECTOR'});
  const fires = LINES.map(l => l.fires === undefined ? null : l.fires);
  if (fires.some(f => f)) graph(document.getElementById('fires'), 'the fifth act: the Nodes turned at their own top each interval (the swap at the top)', [{name: 'Nodes turned', values: fires, colour: token('--flash')}], {marks: marks()});
  if (written.length) {
    const bins = []; for (let a = intervals[0]; a <= intervals[intervals.length - 1]; a += 100) bins.push({at: a, n: written.filter(w => w.at >= a && w.at < a + 100).length});
    graph(document.getElementById('fires'), 'the clicks written on the lattice per 100 intervals (every instrument body), beside the fifth act\\'s turned Nodes', [{name: 'clicks written per 100 intervals', values: bins.map(b => b.n), xs: bins.map(b => b.at), colour: token('--light')}].concat(fires.some(f => f) ? [{name: 'Nodes turned (the swap at the top)', values: fires, colour: token('--flash'), dashed: true}] : []), {marks: marks(), kind: 'the clicks log'});
  }
  const edges = bangs().map(b => b.at), stages = [];
  if (written.length && edges.length) {
    let from = intervals[0];
    for (const at of edges.concat([intervals[intervals.length - 1]])) { const n = written.filter(w => w.at >= from && w.at <= at).length; stages.push(`${from} to ${at}: ${n} clicks, ${(100 * n / (at - from + 1)).toFixed(1)} per 100 intervals`); from = at + 1; }
  }
  const counts = (stages.length ? [`the rate by stage, between the volume\\'s tops and returns: ${stages.join('; ')}`] : []).concat(detectors.filter(d => clicks.some(l => l.node_detector === d)).map(d => `${d}: ${clicks.filter(l => l.node_detector === d).length} clicks over ${intervals.length} intervals, the first at ${clicks.filter(l => l.node_detector === d).map(l => l.interval)[0]}`)).concat(written.length ? [`the clicks written on the lattice (the instrument bodies\\' credits): ${written.length}${written.length <= 40 ? ', at ' + written.map(w => w.at).join(', ') : ''}`] : []);
  document.getElementById('clicks-words').innerHTML = `<b>History kept</b>: every click here was written as the run went and none is run back; the fires are the eras log's own reading of the fifth act. ${esc(counts.join('; '))}.`;
}
function renderNotes(text) {  // the notes: headings, paragraphs and lists, escaped, nothing computed
  const box = document.getElementById('notes-prose'); box.innerHTML = ''; document.getElementById('notes-box').hidden = false;  // the prose box's own id, not the embedded text's script element 'notes'
  const inline = s => esc(s).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\\*\\*([^*]+)\\*\\*/g, '<b>$1</b>');
  let heading = null, list = null, html = '';
  for (const raw of text.split('\\n')) {
    const line = raw.trim(), head = line.match(/^(#+)\\s+(.*)$/), item = line.match(/^(?:[-*]|\\d+\\.)\\s+(.*)$/);
    if (head) { if (list) { html += `</${list}>`; list = null; } if (head[1].length === 1 && heading === null) { heading = head[2]; document.getElementById('notes-heading').innerHTML = inline(heading); continue; } html += `<h3>${inline(head[2])}</h3>`; continue; }
    if (item) { const kind = /^\\d/.test(line) ? 'ol' : 'ul'; if (list !== kind) { if (list) html += `</${list}>`; html += `<${kind}>`; list = kind; } html += `<li>${inline(item[1])}</li>`; continue; }
    if (list) { html += `</${list}>`; list = null; }
    if (line) html += `<p>${inline(line)}</p>`;
  }
  if (list) html += `</${list}>`;
  box.innerHTML = html;
}
const input = document.getElementById('span-input'); input.value = SPAN;
input.addEventListener('change', () => { const v = parseInt(input.value, 10); if (v >= 2) { SPAN = v; draw(); } });
draw();
</script>
"""


def page(
    log: list[dict[str, Any]],
    blind: dict[str, Any] | None,
    notes: str | None,
    span: int,
    look: str,
    clicks: list[dict[str, Any]] | None = None,
    least: dict[str, Any] | None = None,
    captions: list[dict[str, Any]] | None = None,
    legend: str = "",
) -> str:
    """The page's HTML from the log's lines (the header first), the blind and the notes, the estimator's span, the look page's link (empty where none stands) and, where the run kept one, the clicks log's lines (tools/eras.py --clicks), drawn as one panel: the quanta at the detector's Nodes, the clicks' magnitude and the fifth act's fires; `legend` the legend of kinds and the per-bang ledger as captions.legend_html renders them (empty where none)."""
    if not log or not isinstance(log[0], dict) or "held" not in log[0] or not log[0]["held"]:
        raise ValueError(
            "the log's first line is tools/eras.py's header naming the held rows of the content"
        )
    if span < 2:
        raise ValueError(f"--span takes an integer from 2, got {span}")
    title = f"{str(log[0].get('world', 'world')).split('.')[0].replace('_', ' ')} eras"
    embed = lambda value: json.dumps(value, separators=(",", ":")).replace("</", "<\\/")  # noqa: E731
    return (
        TEMPLATE.replace("{{TITLE}}", f"{title[:1].upper()}{title[1:]}")
        .replace("{{TOKENS}}", TOKENS.group(0).rstrip("\n"))
        .replace("{{LOG}}", embed(log))
        .replace("{{BLIND}}", embed(blind))
        .replace("{{NOTES}}", embed(notes))
        .replace("{{CLICKS}}", embed(clicks))
        .replace("{{SPAN}}", embed(span))
        .replace("{{LEAST}}", embed(least))
        .replace("{{CAPTIONS}}", embed(captions or []))
        .replace("{{LOOK}}", look)
        .replace("{{LEGEND}}", legend)
    )


def read_log(path: Path) -> list[dict[str, Any]]:
    """The log's lines, one JSON object per line, the header first; a last line cut mid-write (a log read while its run goes on) left out."""
    return parse_log(path.read_text(encoding="utf-8"))


def least_of(nodes: list[dict[str, Any]], gamma: int) -> dict[str, Any]:
    """The least X over the board per interval, read from the Nodes' log (tools/eras.py --nodes, X at every Node), with the floor X_f = volume_of(Gamma, -Gamma) by the engine's own `swap.floor_of`, so the page draws the distance to X = 0 against the floor; nothing computed of the law."""
    from event_universe.swap import floor_of

    lines = [line for line in nodes if "X" in line]
    return {
        "intervals": [int(line["interval"]) for line in lines],
        "least_x": [min(line["X"]) for line in lines],
        "floor": floor_of(gamma),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("log", type=Path, help="the eras' log (<world>.eras.jsonl, tools/eras.py)")
    parser.add_argument("--blind", type=Path, default=None, help="the blind expectation file")
    parser.add_argument(
        "--notes", type=Path, default=None, help="a Markdown file rendered as one prose section"
    )
    parser.add_argument(
        "--span",
        type=int,
        default=50,
        help="the estimator's span in intervals (the page's picker changes it)",
    )
    parser.add_argument(
        "--look",
        type=Path,
        default=None,
        help="the look's file (<world>.look.json), its page linked beside",
    )
    parser.add_argument(
        "--clicks",
        type=Path,
        default=None,
        help="the clicks log of the same run (<world>.clicks.jsonl), drawn as one panel",
    )
    parser.add_argument(
        "--nodes",
        type=Path,
        default=None,
        help="the Nodes' log of the same run (<world>.nodes.jsonl), the least X over the board drawn against the floor",
    )
    parser.add_argument("--out", type=Path, default=None, help="the page (<world>.html)")
    args = parser.parse_args(argv)
    log = read_log(args.log)
    clicks = read_log(args.clicks) if args.clicks else None
    least = least_of(read_log(args.nodes), int(log[0]["node_clock"])) if args.nodes else None
    nodes = read_log(args.nodes) if args.nodes else []
    floor = least["floor"] if least else None
    captions = captions_of(log, nodes, clicks or [], None, floor)
    legend = legend_html(legend_of(log, nodes, clicks or [], floor), ledger_of(log, nodes, clicks or []))
    blind = json.loads(args.blind.read_text(encoding="utf-8")) if args.blind else None
    notes = args.notes.read_text(encoding="utf-8") if args.notes else None
    stem = args.log.name.removesuffix(".eras.jsonl")
    target = args.out or args.log.with_name(f"{stem}.html")
    look = (
        args.look.with_suffix(".html").name
        if args.look is not None
        else f"{stem}.look.html"
        if args.log.with_name(f"{stem}.look.html").exists()
        else ""
    )
    target.write_text(
        page(log, blind, notes, args.span, look, clicks, least, captions, legend), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "log": args.log.name,
                "page": str(target),
                "bytes": target.stat().st_size,
                "intervals": len(log) - 1,
            }
        )
    )


if __name__ == "__main__":
    main()
