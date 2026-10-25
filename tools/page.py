"""The page, the third tool of the standard (the owner's words of 2026-10-25 through the Boss, 6397241917 and 6397272516): it reads the record and the reading and writes one HTML, dark by its tokens and generic, with nothing of a universe or a world typed in it. The animation is the page: the torus from the record's Node lines (every Node by its X and content, each Node placed along every axis by the lengths of the Links before it on its line, so a line through matter bulges where its Links are longer, every Link's drawn length its stretch above the rest (e^U - 1, zero at X = Gamma, where the Nodes touch) up to the record's largest, so the board's return to its zero is seen as the Nodes closing on each other, and a Big Bang drawn as a burst with its label at the first interval and at every interval where the board stands at its zero and rises again, read from the Node lines' X alone, a turned Node filled in the turn's colour for its interval, the turned and the frozen Nodes marked, the Links from the world's shape alone, every Link's thickness and brightness its own length against the interval's shortest and longest, so the wells around matter are seen beside the whole board's rise, a Link held at the wall drawn thick, the passage through the Links as a directed mark along each Link from the gap-0 line's current, its size the flow and its direction the sign), the clicks as marks by row, the reading's event lines as labels at their interval and at their Node with a leader from the Node, a line with no Node at the board's foot, and as ticks with their labels on the bar; one header line from the two files as they are. The Node lines are carried in the page as words of base 36 (X and the content) and one letter per Link for the current's level and sign, so that a long record's page stays within the branch's file bound; where even so the lines pass the bound, every k-th interval is kept with the first, the last and the gates' own intervals, k named on the page. Usage: `python tools/page.py <record.json> <reading.jsonl> <out.html>`."""

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
#bar { position: relative; height: 44px; margin: 8px 16px 4px; background: var(--panel); border: 1px solid var(--line); cursor: pointer; overflow: visible; }
#bar .tick { position: absolute; top: 0; bottom: 0; width: 2px; background: var(--label); }
#bar .name { position: absolute; font-size: 10px; color: var(--label); font-family: var(--mono); white-space: nowrap; padding-left: 4px; pointer-events: none; }
#bar .bang { position: absolute; bottom: 1px; font-size: 10px; color: var(--muted); font-family: var(--mono); }
#bar #cursor { position: absolute; top: 0; bottom: 0; width: 2px; background: var(--focus); }
#row { display: flex; gap: 12px; align-items: center; margin: 0 16px 8px; color: var(--muted); font-family: var(--mono); font-size: 12px; }
button { background: var(--panel); color: var(--fg); border: 1px solid var(--line); padding: 3px 10px; font: inherit; cursor: pointer; }
#labels { position: absolute; left: 0; top: 0; pointer-events: none; }
.label { position: absolute; color: var(--label); font-family: var(--mono); font-size: 13px; text-shadow: 0 0 4px #000, 0 0 4px #000; white-space: nowrap; }
.label small { display: block; color: var(--muted); font-size: 11px; }
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
  function settle(x, y) { for (const q of placed) if (Math.abs(q[0] - x) < 220 && Math.abs(q[1] - y) < 36) return settle(x, q[1] + 36); placed.push([x, y]); return y; }
  for (const b of bangs) if (line.i >= b && line.i < b + 12 * step) {
    const div = document.createElement("div"); div.className = "label"; div.style.fontSize = "20px";
    div.innerHTML = "Big Bang<small>the board at its zero and rising, interval " + b + "</small>";
    div.style.left = (canvas.offsetLeft + canvas.width / 2 + 0.14 * canvas.width) + "px"; div.style.top = (canvas.offsetTop + canvas.height / 2 - 0.16 * canvas.width) + "px";
    labels.appendChild(div);
  }
  for (const e of D.events) if (e.i !== null && e.i <= line.i && e.i > line.i - 6 * step) {
    const div = document.createElement("div"); div.className = "label";
    div.innerHTML = e.label + "<small>" + e.numbers + "</small>";
    if (e.node) {
      const s = spots[e.node[0] * c * c + e.node[1] * c + e.node[2]];
      ctx.strokeStyle = "#fde68a"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(s[0], s[1]); ctx.lineTo(s[0] + 26, s[1] - 26); ctx.stroke();
      ctx.fillStyle = "#fde68a"; ctx.beginPath(); ctx.arc(s[0], s[1], 4, 0, 2 * Math.PI); ctx.fill();
      const y = settle(s[0] + 28, s[1] - 40);
      ctx.beginPath(); ctx.moveTo(s[0] + 26, s[1] - 26); ctx.lineTo(s[0] + 28, y + 14); ctx.stroke();
      div.style.left = (canvas.offsetLeft + s[0] + 28) + "px"; div.style.top = (canvas.offsetTop + y) + "px";
    } else { div.style.left = (canvas.offsetLeft + canvas.width / 2 - 80) + "px"; div.style.top = (canvas.offsetTop + canvas.height - 44 - 34 * free++) + "px"; }
    labels.appendChild(div);
  }
  cursor.style.left = (100 * (line.i - 1) / Math.max(N - 1, 1)) + "%";
  where.textContent = "interval " + line.i + " of " + N + (D.stride > 1 ? " (1 of every " + D.stride + " intervals kept)" : "");
}
function tick() { if (playing) { t = t % n + 1; draw(); } setTimeout(tick, 1000 / speed); }
let named = 0;
for (const e of D.events) if (e.i !== null) {
  const at = (100 * (e.i - 1) / Math.max(N - 1, 1)) + "%";
  const d = document.createElement("div"); d.className = "tick"; d.style.left = at; d.title = e.label + ": " + e.numbers; bar.appendChild(d);
  const m = document.createElement("div"); m.className = "name"; m.style.top = (2 + 11 * (named++ % 3)) + "px"; m.textContent = e.label;
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
    seed = "; ".join(json.dumps(lay) for lay in world.get("seed", []))
    return f"universe {world['universe']}: {integers}\nrows: {rows}\nworld: shape {world['shape']}, {world['intervals']} intervals, seed {seed}"


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
