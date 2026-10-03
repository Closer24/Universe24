"""The look's page builder, a diagnostic (docs/ENGINE.md #6-how-to-run-a-world): one self-contained HTML page from a look file written by `tools/look/record.py` and, if the world's folder holds one, its blind expectation file, the look embedded gzip-compressed and base64-encoded and inflated by the browser's own DecompressionStream at load, so that a look of many frames fits one page with every number untouched. The page shows the GameBoard as cubes (a folded axis as a plane of thin slabs; the inner faces the world declares as dark cubes with their gaps open, "the faces (declared)" in the legend; a board with a receding face at the shape of each frame, its box drawn per frame and every Node at the file's coordinates), one frame per interval with a slider and play and nothing between frames, the reading's window marked on the slider; the view fixed, the board seen along one axis and never turned (a folded axis is the one seen along, the board the plane it is; a board of three axes is seen along z one layer at a time, the layer picked beside the board, the first body's layer or the middle one first), the declared board alone in the frame and never the layers a receding face grew, the wheel and two buttons bringing it closer or farther; whole quanta as dots sized by the square root of the count (a hole, a count below 0, a hollow dot), resting on the slabs' face where an axis is folded, the wave as the glow of the Node's cube, a field as grey mist, the declared node_readers' Nodes as rings (the open faces' layer reports but is drawn as no ring), seen at rest and brighter and larger the interval they click; the node_readers' report as a bar chart with the dashed blind curve behind it, labelled blind, the one measurement; graphs over the intervals beside the board (the total count per family, the count, the form, the field and the tension at a named Node, the pace's minimum), every one labelled "GameBoard reading" as the board is in its corner; the world's files' numbers listed beside frame 0, the world as laid. The family roles come from the file's rows and never from the look: a family that holds nothing is matter, the holder of the sign is light, a holder of the content is a field; a further family that holds nothing is drawn in the same colour, dashed. Every number on the page is the look's (the world's files' and the engine's arrays') or the blind file's; the page computes nothing but the totals its graphs draw and the sums its bars draw, and draws no curve, surface or interpolation between Nodes. The blind's numbers stand in a table of their own (every number and short list of the expectation file a row, a nested object's rows named key.subkey, its words under a fold) and never as a raw dump; with an expectation across an axis the NodeReaders' arrival over the intervals is drawn beside the bars, the reporters' inflow per interval in quanta over the family's wall and the quanta gathered within the window up to each interval, the blind's peak, centroid, span and total marked where the blind names them. With `--output <world>.output.json` (tools/run_inputs.py's file, the run's own output) the page's measurement is the output file's: its `click` lines feed the bars and the arrival, its `credit` lines the clicks credited up to each interval, its `density` lines the GameBoard density over the reporters' regions, and the header says whether the look's click lines are the output's (they are the same engine lines; a difference is named); with `--reading <reading>.json` (tools/click_counts.py's file, the output file read against the blind) the bars are the reading's rounded shares beside the clicks the draw credited and the blind curve, and one table holds every row the reader compares, read against blind with the difference. The page is dark, one theme and no switch; the moving quanta of light are green; a cube glows by the record's form D at its Node where the look holds it, the wave's own intensity, else by its level. The page's own layout (every colour and size) stands in the one block at the top of the template's style and nowhere else.

The blind file, optional, in one of two formats. The expectation `tools/click_counts.py` reads, `{"node_reader": name or a list, "family": name, "window": [first interval, last interval], "across": the axis across the node_reader, "counts": [the blind count per reporter in that order], "pattern": [first, last] (the range of bars), "through": the blind total, "watch": {coordinate on the across axis: the blind number, ...}}`: the chart draws one bar per reporter ordered by its coordinate on that axis, the rounded shares as click_counts.py reads them (what it saw within the window summed from the look's click lines, floored at 0, N the screen's total over the family's wall W_c to the nearest whole, N apportioned by the shares: the expectation, the clicks being the tool's draw), the blind counts as the dashed curve, the pattern's range, the totals line and one watch line per key. Or the node_readers' totals, `{"expected": {node_reader name: count, ...} or [one count per node_reader in the look's order], "family": the family the curve is of, "window": [first interval, last interval], "watch": {"node_reader": name, "count": the one number to watch}}`, every key optional, one bar per node_reader, what it saw over W_c up to the frame shown.

A gate's reading, optional: with `--gate <reading>.json`, the joint-share reader's file (`tools/bell_gate.py`'s output over the gate's worlds, the look's world among them), and the gate's blind as `--blind` (the expectation of the gate's form: `family`, `sides`, `order`, `runs`, `combination`, `blind`), the page adds the gate's panels, inserted at three markers of the template and absent without a reading (a page without one holds none of them): the board seen from above at the frame shown (frame 0 the input as laid, the record's counts at its Nodes and each side's region with its declared setting and pattern as the reader read them; the beams leaving the record and meeting the regions over the intervals; a region brighter the interval it clicks), labelled a GameBoard reading; the gate's family's `parts` lines per region over the intervals (the parts overlaid, one curve where they are equal) with the region's `click` lines marked, the NodeReader's read; and the reader's credit beside the blind: the 2^n joint shares as bars, the run filled and the blind outlined, the drawn combination (the click) named, E_n, the marginals, the sub-correlations and the three local credits of the look's world in one table against the blind, the combination over the gate's worlds (its formula from the blind's order and signs, the run's value beside the blind's) on a ruler from minus to plus the number of its terms (the algebraic maximum, one per term) with the fence the blind's theorem lines name ("at most") shaded and the local credits marked on it. `--beside <other>.json` adds one line with another gate's blind combination, read from that file and typed nowhere. Every number of the panels is the reader's file's, the blind's or the look's; the page compares them and sums nothing new.

    python tools/look/page.py <world>.look.json [--blind <world>.blind.json] [--output <world>.output.json] [--reading <reading>.json] [--gate <reading>.json] [--beside <other>.json] [--out <world>.look.html]
"""

from __future__ import annotations

import argparse
import base64
import gzip
import json
from pathlib import Path
from typing import Any

MATTER, LIGHT, HELD = "matter", "light", "held"
AXES = ("x", "y", "z")
CDN_THREE = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"


def shown(value: object) -> str:
    """A number as the page prints it: an integer with its thousands separated, any other value as written."""
    return f"{value:,}" if isinstance(value, int) and not isinstance(value, bool) else str(value)


Reporter = tuple[int, str]  # its coordinate on the axis (the least of its Nodes'), its node_reader


def inflows(
    look: dict[str, Any], node_readers: list[str], family: str, window: tuple[int, int]
) -> dict[str, int]:
    """What each named node_reader saw of one family within the window [first, last] of intervals, its click lines' net front inflows summed from the look's frames' lines as tools/click_counts.py sums them (a click reports its region and never a Node)."""
    found = {name: 0 for name in node_readers}
    for frame in look["frames"]:
        for line in frame["lines"]:
            if line.get("event") != "click" or line.get("node_reader") not in found:
                continue
            if line.get("family") != family or not window[0] <= int(line["tick"]) <= window[1]:
                continue
            found[str(line["node_reader"])] += int(line["inflow"])
    return found


def apportioned(quanta: int, shares: list[int]) -> list[int]:
    """N apportioned by the shares to whole numbers, the largest remainders first, the rounded shares as tools/click_counts.py reads them, the expectation and no sample (0 everywhere where nothing was seen)."""
    total = sum(shares)
    if not total or quanta <= 0:
        return [0] * len(shares)
    floors = [quanta * share // total for share in shares]
    rests = sorted(range(len(shares)), key=lambda i: (-(quanta * shares[i] % total), i))
    for index in rests[: quanta - sum(floors)]:
        floors[index] += 1
    return floors


def reporters(node_readers: list[dict[str, Any]], axis: int) -> list[Reporter]:
    """The reporters across `axis` as tools/click_counts.py places them, one per node_reader, ordered by their coordinate on it, the least of the node_reader's Nodes' (a region across the beam at its first row)."""
    return sorted((min(int(node[axis]) for node in d["nodes"]), str(d["name"])) for d in node_readers)


def measurement(look: dict[str, Any], blind: dict[str, Any] | None) -> dict[str, Any] | None:
    """The one measurement from an expectation in tools/click_counts.py's format (`node_reader`, one name or a list, or none for every declared region but the faces' layer, `family`, `window`, or none for the whole look, `across`, `counts`), None from any other: the reporters ordered by their coordinate on the across axis (`reporters`), what each one saw within the window, floored at 0, N over the family's wall to the nearest whole and the rounded shares (`apportioned`, as the tool reads them), the blind counts, the pattern's range, the totals line and the watch lines, each key of `watch` named as the coordinate on the across axis; the page draws these and computes nothing more."""
    if blind is None or "across" not in blind:
        return None
    if blind["across"] not in AXES:
        raise ValueError(f"the blind file's across is one of {list(AXES)}, got {blind['across']!r}")
    axis = AXES.index(blind["across"])
    named = blind.get("node_reader")
    if named is None:  # every declared region, over the whole look (the faces' layer is drawn, not read)
        node_readers = [d for d in look["node_readers"] if d["body"] is None and d["name"] != "face"]
        names = [str(d["name"]) for d in node_readers]
    else:
        names = [str(name) for name in named] if isinstance(named, list) else [str(named)]
        node_readers = [d for d in look["node_readers"] if d["name"] in names]
    if len(node_readers) != len(names):
        raise ValueError(f"the blind file's node_readers {names} are not all in the look")
    spanned = blind.get("window", [0, len(look["frames"]) - 1])
    window = (int(spanned[0]), int(spanned[1]))
    saw = inflows(look, names, str(blind["family"]), window)
    placed = reporters(node_readers, axis)
    seen = [saw[node_reader] for _at, node_reader in placed]
    wall = next(int(f["wall"]) for f in look["families"] if f["name"] == blind["family"])
    shares = [max(value, 0) for value in seen]  # the credit's floor, the NodeReader's declaration
    quanta = (sum(shares) + wall // 2) // wall
    rounded = apportioned(quanta, shares)
    watch = blind.get("watch") if isinstance(blind.get("watch"), dict) else {}
    lines = [
        f"{blind['across']} = {key}: {shown(sum(c for (at, _n), c in zip(placed, rounded, strict=True) if at == int(key)))} by the shares, the blind {shown(value)}"
        for key, value in watch.items()
    ]
    return {
        "node_reader": named if named is not None else names,
        "family": blind["family"],
        "window": list(window),
        "across": blind["across"],
        "axis": axis,
        "at": [at for at, _name in placed],
        "labels": [name for _at, name in placed],
        "seen": seen,
        "quanta": quanta,
        "rounded_shares": rounded,
        "blind": list(blind.get("counts", [])),
        "pattern": blind.get("pattern"),
        "totals": f"N {shown(quanta)} by the shares (the blind {shown(blind.get('quanta', blind.get('through')))})",
        "watch": lines,
        "recorded": len(look["frames"]) - 1,
    }


def roles(families: list[dict[str, Any]]) -> dict[str, dict[str, object]]:
    """The family roles from the file's rows: a family that holds nothing is matter, the holder of the sign is light, a holder of the content is a field; every further family that holds nothing is matter drawn dashed."""
    found: dict[str, dict[str, object]] = {}
    seen = False
    for family in families:
        role = LIGHT if family.get("sign") else HELD if family.get("held") else MATTER
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


GATE_FORM = ("family", "sides", "order", "runs", "combination", "blind")  # the keys of a gate's blind


def gate(look: dict[str, Any], blind: dict[str, Any] | None, reading: dict[str, Any]) -> dict[str, Any]:
    """The gate's reading for the page: the look's world named by its stem, its key in the blind's order (the combination of settings whose run it is) and the reader's file (tools/bell_gate.py's output over the gate's worlds) untouched; refused by name where the blind is not of the gate's form or the look's world is not among the reading's worlds and the blind's runs."""
    world = str(look.get("world", "")).rsplit(".", 1)[0]
    if blind is None or not all(key in blind for key in GATE_FORM):
        raise ValueError(
            f"a gate's reading needs the gate's blind beside it, with the keys {list(GATE_FORM)}"
        )
    keys = [key for key, run in blind["runs"].items() if run == world]
    if not isinstance(reading, dict) or world not in reading.get("worlds", {}) or not keys:
        raise ValueError(
            f"the look's world {world!r} is not among the reading's worlds "
            f"{sorted(reading.get('worlds', {})) if isinstance(reading, dict) else reading} and the blind's runs"
        )
    return {"world": world, "key": keys[0], "reading": reading}


OUTPUT_LINES = ("click", "credit", "density")  # the output file's lines the page draws


def trimmed(output: dict[str, Any]) -> dict[str, Any]:
    """The run's output file as the page embeds it: its verdict, intervals, end and books, and its click, credit and density lines alone, untouched; refused by name where it is not a run's output."""
    if not isinstance(output, dict) or not isinstance(output.get("lines"), list):
        raise ValueError("the output file must be tools/run_inputs.py's, with its lines")
    kept = {key: output.get(key) for key in ("input", "verdict", "ticks", "ended", "books")}
    kept["lines"] = [line for line in output["lines"] if line.get("event") in OUTPUT_LINES]
    return kept


def checked_reading(read: dict[str, Any]) -> dict[str, Any]:
    """tools/click_counts.py's reading as the page embeds it, untouched; refused by name where it is not of that format."""
    if not isinstance(read, dict) or "rounded_shares" not in read or "quanta" not in read:
        raise ValueError(
            "the reading file must be tools/click_counts.py's, with its rounded shares and quanta"
        )
    return read


def beside(path: Path) -> dict[str, Any]:
    """Another gate's blind for the one line beside the reading: the file's content with its path, its combination's name and value read there and typed nowhere."""
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or "combination" not in document or "blind" not in document:
        raise ValueError(f"{path} is not a gate's blind: it holds no combination and blind")
    return {"file": path.as_posix(), **document}


def page(
    look: dict[str, Any],
    blind: dict[str, Any] | None,
    reading: dict[str, Any] | None = None,
    other: dict[str, Any] | None = None,
    output: dict[str, Any] | None = None,
    read: dict[str, Any] | None = None,
) -> str:
    """The page's HTML from the look and the blind expectation, if any; with a gate's reading, the gate's panels inserted at the template's three markers (`other` the line of another gate's blind); with the run's output file and tools/click_counts.py's reading of it, the measurement from them."""
    if not isinstance(look, dict) or "frames" not in look or "families" not in look:
        raise ValueError("the look file must hold the frames and the families (tools/look/record.py)")
    if blind is not None and not isinstance(blind, dict):
        raise ValueError(
            "the blind file must be an object (tools/click_counts.py's format, or expected, family, window and watch)"
        )
    world = str(look.get("world", "world")).split(".")[0].replace("_", " ")
    title = f"{world[:1].upper()}{world[1:]} look"
    gated = gate(look, blind, reading) if reading is not None else None
    template = TEMPLATE
    for marker, text in GATE_MARKERS.items():
        template = template.replace(marker, text if gated else "")
    return (
        template.replace("{{TITLE}}", title)
        .replace("{{THREE}}", CDN_THREE)
        .replace("{{LOOK}}", packed(look))
        .replace("{{ROLES}}", embedded(roles(look["families"])))
        .replace("{{BLIND}}", embedded(blind))
        .replace("{{MEASURE}}", embedded(measurement(look, blind)))
        .replace("{{OUTPUT}}", embedded(trimmed(output) if output is not None else None))
        .replace("{{READ}}", embedded(checked_reading(read) if read is not None else None))
        .replace("{{GATE}}", embedded(gated))
        .replace("{{BESIDE}}", embedded(other))
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("look", type=Path, help="the look file (<world>.look.json)")
    parser.add_argument("--blind", type=Path, default=None, help="the blind expectation file")
    parser.add_argument("--gate", type=Path, default=None, help="a gate's reading (tools/bell_gate.py)")
    parser.add_argument("--beside", type=Path, default=None, help="another gate's blind, for one line")
    parser.add_argument(
        "--output", type=Path, default=None, help="the run's output file (tools/run_inputs.py)"
    )
    parser.add_argument(
        "--reading",
        type=Path,
        default=None,
        help="the output read against the blind (tools/click_counts.py)",
    )
    parser.add_argument("--out", type=Path, default=None, help="the page (<world>.look.html)")
    args = parser.parse_args(argv)
    look = json.loads(args.look.read_text(encoding="utf-8"))
    blind = json.loads(args.blind.read_text(encoding="utf-8")) if args.blind else None
    reading = json.loads(args.gate.read_text(encoding="utf-8")) if args.gate else None
    target: Path = args.out or args.look.with_suffix(".html")
    target.write_text(
        page(
            look,
            blind,
            reading,
            beside(args.beside) if args.beside else None,
            output=json.loads(args.output.read_text(encoding="utf-8")) if args.output else None,
            read=json.loads(args.reading.read_text(encoding="utf-8")) if args.reading else None,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"look": args.look.name, "page": str(target), "bytes": target.stat().st_size}))


TEMPLATE = """<meta charset="utf-8">
<title>{{TITLE}}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* The page's own layout: every colour and size of the page stands in this one block and nowhere else. */
:root {
  --bg: #0f1114; --panel: #171a20; --fg: #e9e7df; --muted: #9a9ea8; --line: #2e323a; --board: #07080a;
  --cube: #1a1d24; --matter: #6ea1f0; --light: #4ade80; --field: #a3a7ae; --wall: #d7dae0; --ring: #c9c7c0;
  --flash: #ff5a1f; --blind: #b4b8c0; --focus: #5f97ea; --window: rgba(95, 151, 234, 0.2);
  --font-body: "IBM Plex Sans", system-ui, sans-serif; --font-mono: "IBM Plex Mono", ui-monospace, monospace;
  --text: 14px; --small: 12px; --title: 20px; --gap: 12px; --pad: 14px; --radius: 6px; --gutter: 16px;
  --sky: #ffffff; --ground: #5a5a5a; --sun: 0.3;
  --side-min: 300px; --board-height: min(76vh, 900px); --graph-width: 360; --graph-height: 84; --graph-pad: 6;
  --bar-slot: 12; --measure-width: 960px; --blind-words: 100; --blind-list: 48; --blind-rows: 24; --arrival-width: 2.6; --arrival-height: 1.6;
  --cube-size: 0.92; --cube-depth: 0.2; --dot-radius: 0.5; --dot-floor: 0.12; --dot-offset: 0.22; --glow: 1; --glow-power: 0.75; --glow-tint: 0;
  --mist-size: 1.02; --mist-opacity: 0.3; --mist-power: 0.5; --bar-length: 0.9; --bar-thickness: 0.07;
  --wall-size: 1; --wall-depth: 0.6; --ring-radius: 0.6; --ring-tube: 0.09; --flash-scale: 1.2; --plane-opacity: 0.12;
  --view-margin: 1; --board-least: 180; --board-most: 900; --camera-far: 4; --zoom-rate: 0.0012; --zoom-step: 0.85; --zoom-most: 8; --frames-per-second: 12; --line-width: 1.6;
  --label-size: 1.4;
  color-scheme: dark;
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
.measure svg, #arrival svg { max-width: var(--measure-width); }
.totals, .watch { font-family: var(--font-mono); font-size: var(--small); margin-top: 6px; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
<script id="look" type="application/gzip+base64">{{LOOK}}</script>
<script id="roles" type="application/json">{{ROLES}}</script>
<script id="blind" type="application/json">{{BLIND}}</script>
<script id="measurement" type="application/json">{{MEASURE}}</script>
<script id="output" type="application/json">{{OUTPUT}}</script>
<script id="reading" type="application/json">{{READ}}</script>
<header>
  <h1 id="title"></h1>
  <span class="verdict" id="verdict"></span>
  <span class="verdict" id="source"></span>
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
    <div class="picker" id="view-picker"></div>
    <div class="time">
      <button type="button" id="play">Play</button>
      <div class="track"><div class="window" id="window" hidden></div><input type="range" id="slider" min="0" value="0" step="1" aria-label="the interval"></div>
      <div class="frame" id="frame"></div>
    </div>
    <div class="lines" id="lines"></div>
  </section>{{GATE_PANELS}}
  <section class="panel measure" id="measure-box">
    <h2>Measurement: the node_readers' report</h2>
    <div class="picker" id="measure-picker"></div>
    <div class="graph" id="measure"></div>
    <div class="totals" id="totals"></div>
    <div class="watch" id="watch"></div>
  </section>
  <section class="panel wide" id="arrival-box" hidden>
    <h2>The arrival at the NodeReaders over the intervals</h2>
    <div class="stack" id="arrival"></div>
  </section>
  <section class="panel">
    <h2>The blind, written before the run</h2>
    <div id="blind-box"></div>
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
const MEASURE = JSON.parse(document.getElementById('measurement').textContent);
const OUTPUT = JSON.parse(document.getElementById('output').textContent);
const READ = JSON.parse(document.getElementById('reading').textContent);
const root = document.documentElement;
const token = name => getComputedStyle(root).getPropertyValue(name).trim();
const size = name => parseFloat(token(name));
const byId = id => document.getElementById(id);
/* The frames' shapes: a board with a receding face grows, so the page's box is the union of the frames' shapes at the file's coordinates (a frame's origin is minus its offset, the layers grown before the origin); an older look without them has the world's shape. */
const shapeOf = fr => fr.shape || LOOK.shape, originOf = fr => (fr.offset || [0, 0, 0]).map(o => -o);
const LOW = [0, 1, 2].map(a => Math.min(...LOOK.frames.map(fr => originOf(fr)[a])));
const HIGH = [0, 1, 2].map(a => Math.max(...LOOK.frames.map(fr => originOf(fr)[a] + shapeOf(fr)[a])));
const [X, Y, Z] = HIGH.map((h, a) => h - LOW[a]), N = X * Y * Z, T = LOOK.frames.length - 1;
/* The view is fixed: the board is seen along one axis, VIEW, and never turned; a folded axis is the one seen along (the board the plane it is), a board of three axes is seen along z one layer at a time, LAYER. The eye stands on the side of the axis from which its two other axes read right and up (ACROSS), and the declared board (the file's own Nodes, from the origin) alone is in the frame. */
const VIEW = LOOK.folded.indexOf(true) >= 0 ? LOOK.folded.indexOf(true) : 2, SIDE = VIEW === 2 ? 1 : -1;
const ACROSS = [0, 1, 2].filter(a => a !== VIEW);
const CENTRE = LOOK.shape.map((e, a) => (e - 1) / 2 - LOW[a] - ([X, Y, Z][a] - 1) / 2);
let LAYER = LOOK.folded[VIEW] ? 0 : LOOK.bodies.length && LOOK.bodies[0].nodes.length ? LOOK.bodies[0].nodes[0][VIEW] : Math.floor(LOOK.shape[VIEW] / 2);
const FAMILIES = LOOK.families, QUANTA = FAMILIES.filter(f => f.quanta), HELD = FAMILIES.filter(f => !f.quanta);
const AXES = ['x', 'y', 'z'], PARTS = ['x', 'y', 'z', 'xx', 'yy', 'zz', 'xy', 'xz', 'yz'];
const colourOf = name => token('--' + ROLES[name].role);
const esc = text => String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
const format = value => typeof value === 'number' ? value.toLocaleString('en-US') : String(value);

/* The arrays of a frame, dense nested lists or the nonzero Nodes alone over the frame's own shape, as flat x-major arrays over the page's box, the frame's Nodes at their file coordinates. */
function arrayOf(value, fr) {
  const out = new Float64Array(N);
  if (!value) return out;
  const [fy, fz] = shapeOf(fr).slice(1), [ox, oy, oz] = originOf(fr).map((o, a) => o - LOW[a]);
  const put = (x, y, z, v) => { out[((x + ox) * Y + (y + oy)) * Z + (z + oz)] = v; };
  if (Array.isArray(value)) value.forEach((plane, x) => plane.forEach((row, y) => row.forEach((v, z) => put(x, y, z, v))));
  else value.at.forEach((k, j) => put(Math.floor(k / (fy * fz)), Math.floor(k / fz) % fy, k % fz, value.values[j]));
  return out;
}
const inside = i => { const n = nodeOf(i); return n.every((c, a) => c >= 0 && c < LOOK.shape[a]) && (LOOK.folded[VIEW] || n[VIEW] === LAYER); };  // the declared board, the layer seen
const cache = new Map();
function frameOf(t) {
  if (cache.has(t)) return cache.get(t);
  const frame = LOOK.frames[t], out = {};
  for (const f of FAMILIES) {
    const row = frame.families[f.name] || {}, a = {};
    if (f.quanta) { for (const key of ['now', 'second', 'count', 'form']) if (row[key] !== undefined) a[key] = arrayOf(row[key], frame); a.pace = row.pace; a.peakForm = a.form ? peak(a.form) : 0; a.peakNow = Math.max(peak(a.now), a.second ? peak(a.second) : 0); }
    else { a.level = arrayOf(row.level, frame); a.parts = (row.parts || []).map(part => arrayOf(part, frame)); }
    out[f.name] = a;
  }
  cache.set(t, out);
  return out;
}
const peak = a => { let m = 0; for (let i = 0; i < a.length; i++) { const v = Math.abs(a[i]); if (v > m) m = v; } return m; };
const sum = a => { let s = 0; for (let i = 0; i < a.length; i++) s += a[i]; return s; };
const MOST = {}, TOTALS = {};
for (const f of FAMILIES) { MOST[f.name] = { now: 0, count: 0, level: 0, part: 0, form: 0 }; if (f.quanta) TOTALS[f.name] = new Float64Array(T + 1); }
for (let t = 0; t <= T; t++) {
  const fr = frameOf(t);
  for (const f of FAMILIES) {
    const a = fr[f.name], m = MOST[f.name];
    if (f.quanta) { m.now = Math.max(m.now, peak(a.now), a.second ? peak(a.second) : 0); m.count = Math.max(m.count, peak(a.count)); m.form = Math.max(m.form, a.form ? peak(a.form) : 0); TOTALS[f.name][t] = sum(a.count); }
    else { m.level = Math.max(m.level, peak(a.level)); for (const p of a.parts) m.part = Math.max(m.part, peak(p)); }
  }
}
const indexOf = (x, y, z) => ((x - LOW[0]) * Y + (y - LOW[1])) * Z + (z - LOW[2]);
const nodeOf = i => [Math.floor(i / (Y * Z)) + LOW[0], Math.floor(i / Z) % Y + LOW[1], i % Z + LOW[2]];
/* The click lines the measurement is drawn from: the output file's where it is given (the run's own output), the look's otherwise; the two are the same engine lines, and the header says so or names the difference. The output file's credit lines (the clicks the draw credited) and density lines (a GameBoard reading per declared region) beside them. */
const LOOK_CLICKS = [], reportsAt = {}, CREDITS_AT = {}, DENSITY_AT = {};
for (const frame of LOOK.frames) for (const line of frame.lines) if (line.event === 'click') LOOK_CLICKS.push(line);
const CLICKS = OUTPUT ? OUTPUT.lines.filter(line => line.event === 'click') : LOOK_CLICKS;
for (const line of CLICKS) {
  const byFamily = reportsAt[line.node_reader] || (reportsAt[line.node_reader] = {});
  (byFamily[line.family] || (byFamily[line.family] = [])).push([line.tick, line.inflow]);
}
if (OUTPUT) for (const line of OUTPUT.lines) {
  if (line.event === 'credit') (CREDITS_AT[line.node_reader] || (CREDITS_AT[line.node_reader] = [])).push([line.tick, line.count || 0]);
  if (line.event === 'density') ((DENSITY_AT[line.family] || (DENSITY_AT[line.family] = {}))[line.node_reader] || (DENSITY_AT[line.family][line.node_reader] = [])).push([line.tick, line.reading]);
}
const key = line => [line.tick, line.node_reader, line.family, line.inflow].join('|');
const SAME_LINES = OUTPUT ? CLICKS.length === LOOK_CLICKS.length && CLICKS.map(key).sort().join(';') === LOOK_CLICKS.map(key).sort().join(';') : null;
const WALL = {};
for (const f of FAMILIES) if (f.quanta) WALL[f.name] = f.wall;
const WINDOW = Array.isArray(BLIND.window) && BLIND.window.length === 2 ? BLIND.window : null;

/* The board: cubes, dots, glow, mist, bars, rings, the box's edges and a folded axis's plane. */
const stage = byId('stage'), canvas = byId('board');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(window.devicePixelRatio || 1);
const scene = new THREE.Scene();
const EXTENT = Math.max(X, Y, Z);
const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, EXTENT * size('--camera-far'));
/* The frame: the declared board's two axes across the view with a margin of Links, fitted to the stage; the eye along VIEW at the board's centre, looking at it, the up axis the second of ACROSS. */
function fit() {
  const w = stage.clientWidth || 1, margin = size('--view-margin');
  let halfW = (LOOK.shape[ACROSS[0]] + 2 * margin) / 2, halfH = (LOOK.shape[ACROSS[1]] + 2 * margin) / 2;
  stage.style.height = Math.round(Math.max(size('--board-least'), Math.min(size('--board-most'), w * halfH / halfW))) + 'px';  // the stage the board's own shape, within bounds
  const h = stage.clientHeight || 1;
  if (halfW / halfH > w / h) halfH = halfW * h / w; else halfW = halfH * w / h;
  camera.left = -halfW; camera.right = halfW; camera.top = halfH; camera.bottom = -halfH; camera.updateProjectionMatrix();
  const centre = new THREE.Vector3(...CENTRE), eye = centre.clone(), up = new THREE.Vector3();
  eye.setComponent(VIEW, CENTRE[VIEW] + SIDE * EXTENT * size('--camera-far') / 2); up.setComponent(ACROSS[1], 1);
  camera.position.copy(eye); camera.up.copy(up); camera.lookAt(centre);
}
const hemisphere = new THREE.HemisphereLight(0xffffff, 0x000000, 1), sun = new THREE.DirectionalLight(0xffffff, size('--sun'));
sun.position.set(1, 2, 3);
scene.add(hemisphere, sun);
const position = i => { const [x, y, z] = nodeOf(i); return new THREE.Vector3(x - LOW[0] - (X - 1) / 2, y - LOW[1] - (Y - 1) / 2, z - LOW[2] - (Z - 1) / 2); };  // the Node at its file coordinates within the box, the layers grown before the origin counted
const matrix = new THREE.Matrix4(), quaternion = new THREE.Quaternion(), scale = new THREE.Vector3(), colour = new THREE.Color(), tint = new THREE.Color();
const hidden = new THREE.Matrix4().makeScale(0, 0, 0);
const layers = {};
/* A cube is thin along a folded axis (the board a plane of slabs) and the dots rest on the slab's face, so a dot of any count is seen; along an axis of many Nodes a cube keeps its size. */
const cubeSide = size('--cube-size'), cubeDepth = size('--cube-depth');
const extentAlong = (side, depth) => [0, 1, 2].map(a => LOOK.folded[a] ? depth : side);
const lift = [0, 1, 2].map(a => LOOK.folded[a] ? SIDE * cubeDepth / 2 : 0);  // toward the eye
const cubes = new THREE.InstancedMesh(new THREE.BoxGeometry(...extentAlong(cubeSide, cubeDepth)), new THREE.MeshLambertMaterial({ color: 0xffffff }), N);
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
const ringCapacity = LOOK.node_readers.reduce((n, d) => n + (d.body === null ? d.nodes.length : Math.max(...LOOK.frames.map(fr => fr.bodies[d.body].length))), 0);
const rings = new THREE.InstancedMesh(new THREE.TorusGeometry(size('--ring-radius'), size('--ring-tube'), 8, 32), new THREE.MeshBasicMaterial({ color: 0xffffff }), Math.max(ringCapacity, 1));
scene.add(rings);
layers['node_reader rings (the declared regions)'] = { on: true, objects: [rings] };
/* The inner faces the world declares: the plane's Nodes across the axis at the coordinate, its gaps left open, drawn as cubes within the declared board alone (the layers a receding face grew are not in the frame); the Nodes are the file's declaration and nothing is read there. */
const beyond = new Set();
for (const face of LOOK.faces || []) {
  const a = AXES.indexOf(face.axis), others = [0, 1, 2].filter(k => k !== a), extents = LOOK.shape;
  for (let u = 0; u < extents[others[0]]; u++) for (let v = 0; v < extents[others[1]]; v++) {
    const open = face.gaps.some(gap => { const [p, q] = gap[AXES[others[0]]], [r, s] = gap[AXES[others[1]]]; return p <= u && u <= q && r <= v && v <= s; });
    if (open) continue;
    const at = [0, 0, 0]; at[a] = face.at; at[others[0]] = u; at[others[1]] = v;
    beyond.add(indexOf(...at));
  }
}
const wall = new THREE.InstancedMesh(new THREE.BoxGeometry(...extentAlong(size('--wall-size'), size('--wall-depth'))), new THREE.MeshLambertMaterial({ color: 0xffffff }), Math.max(beyond.size, 1));
wall.setMatrixAt(0, hidden);
[...beyond].forEach((i, k) => wall.setMatrixAt(k, matrix.makeTranslation(...position(i).toArray())));
wall.visible = beyond.size > 0;
scene.add(wall);
if (beyond.size) layers['the faces (declared)'] = { on: true, objects: [wall] };
const box = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(...LOOK.shape)), new THREE.LineBasicMaterial({ color: 0xffffff }));
/* The box is the declared board's, drawn once at its place; the cubes outside the declared board, and outside the layer seen, are hidden. */
let boxKey = null;
function boxAt() {
  if (boxKey === LAYER) return;
  boxKey = LAYER;
  for (let i = 0; i < N; i++) cubes.setMatrixAt(i, inside(i) ? matrix.makeTranslation(...position(i).toArray()) : hidden);
  cubes.instanceMatrix.needsUpdate = true;
}
const faces = new THREE.Group();
AXES.forEach((axis, a) => {
  if (LOOK.boundary[axis] !== 'open') return;
  for (const side of [-1, 1]) {
    const half = LOOK.shape.map(e => e / 2), corners = [];
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
  const span = LOOK.shape.map((e, a) => LOOK.folded[a] ? cubeSide : e), folded = LOOK.folded.indexOf(true);
  if (folded === 2) plane.scale.set(span[0], span[1], 1);
  else if (folded === 1) { plane.rotation.x = Math.PI / 2; plane.scale.set(span[0], span[2], 1); }
  else { plane.rotation.y = Math.PI / 2; plane.scale.set(span[2], span[1], 1); }
}
const labels = new THREE.Group(), labelSize = size('--label-size');
AXES.forEach((axis, a) => {
  const c = document.createElement('canvas'), px = 64; c.width = c.height = px;
  const g = c.getContext('2d'); g.font = `${px / 2}px ${token('--font-mono')}`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#ffffff'; g.fillText(axis, px / 2, px / 2);
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthTest: false }));
  const p = [0, 0, 0]; p[a] = LOOK.shape[a] / 2 + labelSize;
  sprite.position.set(...p); sprite.scale.setScalar(labelSize); labels.add(sprite);
});
const frameGroup = new THREE.Group();
frameGroup.position.set(...CENTRE); frameGroup.add(box, faces, plane, labels); scene.add(frameGroup);
layers['the box and its axes'] = { on: true, objects: [box, faces, plane, labels] };

function themed() {
  scene.background = new THREE.Color(token('--board'));
  box.material.color.set(token('--line')); plane.material.color.set(token('--muted')); wall.material.color.set(token('--wall'));
  faces.children.forEach(line => line.material.color.set(token('--fg')));
  labels.children.forEach(sprite => sprite.material.color.set(token('--muted')));
  hemisphere.color.set(token('--sky')); hemisphere.groundColor.set(token('--ground'));
  for (const f of QUANTA) { const hex = colourOf(f.name); if (!ROLES[f.name].dashed) dots[f.name].full.material.color.set(hex); else dots[f.name].full.material.map = striped(hex); dots[f.name].hollow.material.color.set(hex); }
  for (const f of HELD) { mists[f.name].material.color.set(colourOf(f.name)); (bars[f.name] || []).forEach(b => b.material.color.set(colourOf(f.name))); }
}

/* One frame drawn: no state between frames, every mark from the frame's arrays alone. */
let t = 0, playing = null, named = null;
function draw() {
  const frame = LOOK.frames[t], fr = frameOf(t), glow = size('--glow'), glowPower = size('--glow-power'), glowTint = size('--glow-tint');
  const base = new THREE.Color(token('--cube'));
  boxAt(frame);
  for (let i = 0; i < N; i++) {
    colour.copy(base);
    for (const f of QUANTA) {
      if (!layers[f.name + ' glow'].on || !MOST[f.name].now) continue;
      const a = fr[f.name];  // the glow by the form D at the Node (the wave's intensity, phase-free) against the frame's own largest, where the look holds it, else by the level against the frame's own largest; the dots carry the absolute count
      if (!(a.peakForm || a.peakNow)) continue;
      const strength = glow * Math.pow(a.peakForm && a.form ? Math.abs(a.form[i]) / a.peakForm : Math.max(Math.abs(a.now[i]), a.second ? Math.abs(a.second[i]) : 0) / a.peakNow, glowPower);
      colour.lerp(tint.set(colourOf(f.name)).lerp(base, glowTint), Math.min(1, strength));  // the glow a tint of the family's colour, the dots the colour itself
    }
    cubes.setColorAt(i, colour);
  }
  cubes.instanceColor.needsUpdate = true;
  const radius = size('--dot-radius'), floor = size('--dot-floor');
  for (const f of QUANTA) {
    const { full, hollow, offset } = dots[f.name], count = fr[f.name].count, most = Math.sqrt(MOST[f.name].count) || 1;
    for (let i = 0; i < N; i++) {
      const c = inside(i) ? count[i] : 0, r = c ? Math.max(floor, radius * Math.sqrt(Math.abs(c)) / most) : 0;
      const p = position(i); p.y += offset; p.x += lift[0]; p.y += lift[1]; p.z += lift[2];
      matrix.compose(p, quaternion, scale.setScalar(r));
      full.setMatrixAt(i, c > 0 ? matrix : hidden); hollow.setMatrixAt(i, c < 0 ? matrix : hidden);
    }
    full.instanceMatrix.needsUpdate = true; hollow.instanceMatrix.needsUpdate = true;
  }
  const mistSize = size('--mist-size'), power = size('--mist-power'), barLength = size('--bar-length'), thickness = size('--bar-thickness');
  for (const f of HELD) {
    const a = fr[f.name], mist = mists[f.name], most = MOST[f.name].level;
    for (let i = 0; i < N; i++) {
      const s = most && inside(i) ? mistSize * Math.pow(Math.abs(a.level[i]) / most, power) : 0;
      mist.setMatrixAt(i, s ? matrix.compose(position(i), quaternion, scale.setScalar(s)) : hidden);
    }
    mist.instanceMatrix.needsUpdate = true;
    if (bars[f.name]) bars[f.name].forEach((bar, axis) => {
      const part = a.parts[f.parts[1] + axis], most = MOST[f.name].part;
      for (let i = 0; i < N; i++) {
        const length = most && part && inside(i) ? barLength * Math.abs(part[i]) / most : 0;
        scale.set(thickness, thickness, thickness); if (length) scale.setComponent(axis, length);
        bar.setMatrixAt(i, length ? matrix.compose(position(i), quaternion, scale) : hidden);
      }
      bar.instanceMatrix.needsUpdate = true;
    });
  }
  let slot = 0;
  const ringColour = new THREE.Color(token('--ring')), flashColour = new THREE.Color(token('--flash')), flashScale = size('--flash-scale');
  for (const d of LOOK.node_readers) {
    if (d.name === 'face') continue;  // the open faces' layer reports, but is no declared region: not drawn
    const nodes = d.body === null ? d.nodes : frame.bodies[d.body];
    const flashing = frame.lines.some(line => line.event === 'click' && line.node_reader === d.name);
    for (const [x, y, z] of nodes) {
      rings.setMatrixAt(slot, inside(indexOf(x, y, z)) ? matrix.compose(position(indexOf(x, y, z)), quaternion, scale.setScalar(flashing ? flashScale : 1)) : hidden);
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
  const clicks = frame.lines.filter(line => line.event === 'click').map(line => line.node_reader + ': ' + line.family);
  byId('lines').textContent = t === 0 ? 'The world as laid: the bodies\\' declared counts, the levels of the mode file, every held row at its start.'
    : Object.entries(counts).map(([event, n]) => n + ' ' + event + (n === 1 ? '' : 's')).join(', ') + (clicks.length ? ' (' + [...new Set(clicks)].join(', ') + ')' : '') || 'no line this interval';
  if (!MEASURE) drawMeasure();
  moveCursors();{{GATE_DRAW}}
}

/* The view is fixed: no turning; the wheel and the two buttons bring the board closer or farther, within a bound; a board of three axes has its layer picked. */
canvas.addEventListener('pointermove', hover);
canvas.addEventListener('pointerleave', () => hover(null));
canvas.addEventListener('wheel', e => { e.preventDefault(); zoom(Math.exp(e.deltaY * size('--zoom-rate'))); }, { passive: false });
function zoom(factor) { camera.zoom = Math.min(size('--zoom-most'), Math.max(1 / size('--zoom-most'), camera.zoom / factor)); camera.updateProjectionMatrix(); renderer.render(scene, camera); }
byId('zoom-in').addEventListener('click', () => zoom(size('--zoom-step')));
byId('zoom-out').addEventListener('click', () => zoom(1 / size('--zoom-step')));
const viewPicker = byId('view-picker');
if (LOOK.folded[VIEW]) viewPicker.textContent = `Seen along ${AXES[VIEW]}, the board the plane it is: ${AXES[ACROSS[0]]} to the right, ${AXES[ACROSS[1]]} up; the declared board alone, ${LOOK.shape[ACROSS[0]]} x ${LOOK.shape[ACROSS[1]]} Nodes; no turning.`;
else {
  viewPicker.innerHTML = `Seen along ${AXES[VIEW]}, one layer at a time: ${AXES[VIEW]} = <label><input type="number" id="layer" min="0" max="${LOOK.shape[VIEW] - 1}" value="${LAYER}" aria-label="the layer seen"></label> of 0 to ${LOOK.shape[VIEW] - 1}; ${AXES[ACROSS[0]]} to the right, ${AXES[ACROSS[1]]} up; the declared board alone; no turning.`;
  byId('layer').addEventListener('change', () => { LAYER = Math.max(0, Math.min(LOOK.shape[VIEW] - 1, Number(byId('layer').value) || 0)); draw(); });
}
canvas.addEventListener('click', e => { const i = pick(e); if (i !== null) { named = nodeOf(i); AXES.forEach((axis, a) => { byId('node-' + axis).value = named[a]; }); drawGraphs(); } });
new ResizeObserver(() => {
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(w, h, false); fit(); renderer.render(scene, camera);
}).observe(stage);

/* The hover: a Node's numbers as they are, the count the record's share in quanta. */
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
  const fr = frameOf(t), lines = ['Node [' + nodeOf(i).join(', ') + ']  (GameBoard reading)' + (beyond.has(i) ? ', beyond the board: a declared face' : '')];
  for (const f of FAMILIES) {
    const a = fr[f.name];
    if (f.quanta) {
      const parts = ['level ' + format(a.now[i])];
      if (MOST[f.name].now && a.second && a.second[i]) parts.push('second ' + format(a.second[i]));
      parts.push('count ' + format(a.count[i]));
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
  label.append(' ' + name + (family ? ' (' + ROLES[family.name].role + (name.endsWith(' glow') ? ', the form D against the frame\\'s own largest' : name.endsWith(' dots') ? ', the count' : '') + ')' : ''));
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
function graph(container, title, series, kind, marks, shape) {
  const W = size('--graph-width') * (shape ? shape[0] : 1), H = size('--graph-height') * (shape ? shape[1] : 1), pad = size('--graph-pad'), left = pad * 8, frames = series[0] ? series[0].values.length : 0;
  let low = Infinity, high = -Infinity;
  for (const s of series) for (const v of s.values) { if (v < low) low = v; if (v > high) high = v; }
  if (!series.length || !isFinite(low)) { container.innerHTML = `<div class="caption"><b>${esc(title)}</b><span>nothing to draw</span></div>`; return; }
  if (low === high) { low -= 1; high += 1; }
  const px = i => left + (frames > 1 ? i / (frames - 1) : 0) * (W - left - pad), py = v => pad + (high - v) / (high - low) * (H - 2 * pad);
  let body = `<rect x="${left}" y="${pad}" width="${W - left - pad}" height="${H - 2 * pad}" fill="none" stroke="${token('--line')}"/>`;
  if (low < 0 && high > 0) body += `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}" stroke-dasharray="2 3"/>`;
  body += svgText(format(high), left - 3, pad + size('--small') * 0.3, 'end') + svgText(format(low), left - 3, H - pad, 'end');
  for (const s of series) body += `<polyline fill="none" stroke="${s.colour}" stroke-width="${size('--line-width')}" ${s.dashed ? 'stroke-dasharray="5 4"' : ''} stroke-linejoin="round" points="${Array.from(s.values, (v, i) => px(i).toFixed(1) + ',' + py(v).toFixed(1)).join(' ')}"/>`;
  if (marks) body += marks(px, py, low, high);
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
picker.innerHTML = 'Node ' + AXES.map((axis, a) => `<label>${axis} <input type="number" id="node-${axis}" min="${LOW[a]}" max="${HIGH[a] - 1}" value="0"></label>`).join(' ') + ' <span>(click a cube to pick it)</span>';
AXES.forEach(axis => byId('node-' + axis).addEventListener('change', () => { named = AXES.map((a, k) => Math.max(LOW[k], Math.min(HIGH[k] - 1, Number(byId('node-' + a).value) || 0))); drawGraphs(); }));
if (LOOK.bodies.length && LOOK.bodies[0].nodes.length) { named = LOOK.bodies[0].nodes[0].slice(); AXES.forEach((axis, a) => { byId('node-' + axis).value = named[a]; }); }

/* The measurement: with an expectation across an axis, one bar per reporter ordered along it, the rounded shares of what the reporters saw within the window, the expectation (the file's numbers embedded, the sums the page's), the dashed blind curve behind them, the pattern's range, the totals and the watch lines; otherwise the node_readers' reports as bars, one each, what each saw over W_c up to the frame shown, the dashed blind curve behind them. */
const measurePicker = byId('measure-picker'), select = document.createElement('select'); select.id = 'measure-family';
function drawNodeMeasure() {
  const m = MEASURE, n = m.rounded_shares.length, family = m.family, box = byId('measure'), hex = ROLES[family] ? colourOf(family) : token('--fg');
  byId('measure-box').classList.add('wide');
  measurePicker.textContent = `${m.node_reader}, ${family}, within the window ${m.window[0]} to ${m.window[1]}: one bar per reporter across ${m.across} (a group at the coordinate its Nodes share, else a Node)`
    + (m.recorded < m.window[1] ? ` (the look holds intervals 0 to ${m.recorded})` : '');
  const slot = size('--bar-slot'), pad = size('--graph-pad'), left = pad * 8, bottom = pad * 3, H = size('--graph-height') * 2;
  const W = Math.max(size('--graph-width'), left + slot * n + pad), blind = m.blind.map(v => typeof v === 'number' ? v : null);
  const high = Math.max(1, ...m.rounded_shares, ...blind.filter(v => v !== null));
  const px = k => left + slot * (k + 0.5), py = v => pad + (high - v) / high * (H - pad - bottom);
  const coordinate = k => m.at[k];
  let body = '';
  if (Array.isArray(m.pattern) && m.pattern.length === 2 && n) {
    const [first, last] = m.pattern.map(v => Math.max(0, Math.min(n - 1, v)));
    body += `<rect x="${(px(first) - slot / 2).toFixed(1)}" y="${pad}" width="${(slot * (last - first + 1)).toFixed(1)}" height="${(H - pad - bottom).toFixed(1)}" fill="${token('--window')}"><title>the pattern's range: ${m.across} ${coordinate(first)} to ${coordinate(last)}</title></rect>`;
  }
  body += `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}"/>` + svgText(format(high), left - 3, pad + size('--small') * 0.3, 'end') + svgText('0', left - 3, py(0), 'end');
  const every = Math.max(1, Math.ceil(n / 16)), w = Math.max(1, slot * 0.6);
  m.rounded_shares.forEach((v, k) => {
    body += `<rect x="${(px(k) - w / 2).toFixed(1)}" y="${py(v).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(v)).toFixed(1)}" fill="${hex}"><title>${esc(m.labels[k])}: ${format(v)} by the shares, saw ${format(m.seen[k])}${blind[k] === null ? '' : ', the blind ' + format(blind[k])}</title></rect>`;
    if (k % every === 0 || k === n - 1) body += svgText(coordinate(k), px(k), H - pad, 'middle');
  });
  if (blind.some(v => v !== null)) {
    const points = blind.map((v, k) => v === null ? null : px(k).toFixed(1) + ',' + py(v).toFixed(1)).filter(Boolean).join(' ');
    body += `<polyline fill="none" stroke="${token('--blind')}" stroke-width="${size('--line-width')}" stroke-dasharray="5 4" points="${points}"/>` + svgText('blind', W - pad, pad + size('--small') * 0.3, 'end');
  }
  const legend = `<span><i style="border-color:${hex};border-top-width:6px"></i>${esc(family)} the rounded shares per reporter (N by the shares of the look's click lines, the expectation)</span><span><i class="dashed" style="border-color:${token('--blind')}"></i>blind</span>` + (Array.isArray(m.pattern) ? `<span><i style="border-color:${token('--window')};border-top-width:6px"></i>the pattern's range</span>` : '');
  box.innerHTML = `<div class="caption"><b>The credit of ${esc(family)} at ${esc(String(m.node_reader))} across ${esc(m.across)}</b><span>measurement</span></div><div class="legend">${legend}</div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="the node_readers' credit per reporter">${body}</svg>`;
  byId('totals').textContent = m.totals;
  byId('watch').innerHTML = m.watch.map(esc).join('<br>');
}
if (!MEASURE) {
  for (const f of QUANTA) { const o = document.createElement('option'); o.value = f.name; o.textContent = f.name; select.append(o); }
  const reporting = QUANTA.find(f => f.name === BLIND.family) || QUANTA.find(f => ROLES[f.name].role === 'light') || QUANTA[0];
  if (reporting) select.value = reporting.name;
  select.addEventListener('change', drawMeasure);
  measurePicker.append('Family ', select, document.createTextNode(WINDOW ? ' within the window ' + WINDOW[0] + ' to ' + WINDOW[1] : ' over every interval'));
}
function reported(node_reader, family) {
  const lines = (reportsAt[node_reader] || {})[family] || [];
  const saw = lines.filter(([k]) => k <= t && (!WINDOW || (k >= WINDOW[0] && k <= WINDOW[1]))).reduce((s, [, inflow]) => s + inflow, 0);
  return WALL[family] ? saw / WALL[family] : saw;
}
function drawMeasure() {
  const family = select.value, node_readers = LOOK.node_readers, box = byId('measure');
  const expected = node_readers.map((d, k) => Array.isArray(BLIND.expected) ? BLIND.expected[k] : BLIND.expected && typeof BLIND.expected === 'object' ? BLIND.expected[d.name] : undefined);
  const counts = node_readers.map(d => reported(d.name, family));
  const W = size('--graph-width'), H = size('--graph-height') * 1.5, pad = size('--graph-pad'), left = pad * 8, bottom = pad * 3;
  const high = Math.max(1, ...counts, ...expected.filter(v => typeof v === 'number'));
  const slot = (W - left - pad) / Math.max(node_readers.length, 1), py = v => pad + (high - v) / high * (H - pad - bottom);
  let body = `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}"/>` + svgText(format(high), left - 3, pad + size('--small') * 0.3, 'end') + svgText('0', left - 3, py(0), 'end');
  if (expected.some(v => typeof v === 'number')) {
    const points = expected.map((v, k) => typeof v === 'number' ? (left + slot * (k + 0.5)).toFixed(1) + ',' + py(v).toFixed(1) : null).filter(Boolean).join(' ');
    body += `<polyline fill="none" stroke="${token('--blind')}" stroke-width="${size('--line-width')}" stroke-dasharray="5 4" points="${points}"/>` + svgText('blind', W - pad, pad + size('--small') * 0.3, 'end');
  }
  const every = Math.max(1, Math.ceil(node_readers.length / 12));
  node_readers.forEach((d, k) => {
    const x = left + slot * (k + 0.5), w = Math.max(1, slot * 0.6);
    body += `<rect x="${(x - w / 2).toFixed(1)}" y="${py(counts[k]).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(counts[k])).toFixed(1)}" fill="${colourOf(family)}"><title>${esc(d.name)}: ${counts[k].toFixed(2)} quanta seen</title></rect>`;
    if (k % every === 0) body += svgText(d.name, x, H - pad, 'middle');
  });
  box.innerHTML = `<div class="caption"><b>The reports of ${esc(family)} (what each node_reader saw over W_c)</b><span>measurement</span></div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="the node_readers' report">${body}</svg>`;
  const watch = BLIND.watch && typeof BLIND.watch === 'object' ? BLIND.watch : null;
  byId('watch').textContent = watch ? `${watch.node_reader}: ${reported(watch.node_reader, family).toFixed(2)} quanta seen, the blind ${format(watch.count)}` : '';
}

/* The world's numbers as the files hold them, and the books at the end. */
function numbers() {
  const row = (k, v) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`;
  const inner = (LOOK.faces || []).map(f => `${f.axis} at ${f.at}, gaps ${f.gaps.map(g => Object.entries(g).map(([k, v]) => k + ' [' + v.join(', ') + ']').join(' ')).join('; ') || 'none'}`).join(' | ') || 'none';
  const receding = Object.entries(LOOK.receding || {}).map(([a, f]) => `${a} ${f.sides.join(' and ')}, the largest ${format(f.largest)}, ${format(f.layers)} layers per growth`).join('; ') || 'none';
  const ended = LOOK.ended ? `at interval ${format(LOOK.ended.interval)}: the front at the ${LOOK.ended.side} face of ${LOOK.ended.axis} at the largest size ${format(LOOK.ended.largest)}` : 'no';
  let html = '<dl>' + row('world', LOOK.world) + row('shape', LOOK.shape.join(' x ') + (X * Y * Z > LOOK.shape[0] * LOOK.shape[1] * LOOK.shape[2] ? ', grown to ' + [X, Y, Z].join(' x ') : '')) + row('boundary', AXES.map(a => a + ' ' + LOOK.boundary[a]).join(', ')) + row('inner faces', inner) + row('receding faces', receding) + row('ended', ended) + row('folded', AXES.filter((a, k) => LOOK.folded[k]).join(', ') || 'none') + row('face depth', LOOK.face_depth)
    + row('Gamma (the Node clock)', format(LOOK.node_clock)) + row('T (the quantum action)', format(LOOK.quantum_action)) + row('the largest integer', LOOK.largest_integer) + row('A (the amplitude bound)', format(LOOK.amplitude_bound))
    + row('intervals', format(LOOK.ticks) + ' recorded; the world declares ' + format(LOOK.declared_ticks)) + '</dl>';
  html += '<div class="scroll"><table><thead><tr><th>family</th><th>pair</th><th>holds</th><th>level weight</th><th>parts</th><th>reads</th><th>W_c</th><th>role</th></tr></thead><tbody>'
    + FAMILIES.map(f => `<tr><td>${esc(f.name)}</td><td class="num">[${f.pair.join(', ')}]</td><td>${f.held ? (f.sign ? 'the sign' : 'the content') : 'nothing'}</td><td class="num">${f.level_weight === null ? '' : f.level_weight}</td><td class="num">${f.parts.join(' + ')}</td><td>${f.reads.join(', ')}</td><td class="num">${f.wall === null ? '' : format(f.wall)}</td><td><i class="swatch${ROLES[f.name].dashed ? ' dashed' : ''}" style="border-color:${colourOf(f.name)}"></i> ${ROLES[f.name].role}</td></tr>`).join('') + '</tbody></table></div>';
  html += '<div class="scroll"><table><thead><tr><th>body</th><th>family</th><th>Nodes</th><th>declared count</th></tr></thead><tbody>'
    + LOOK.bodies.map(b => `<tr><td class="num">${b.number}</td><td>${esc(b.family)}</td><td class="num">${b.nodes.length}</td><td class="num">${format(b.declared)}</td></tr>`).join('') + '</tbody></table></div>';
  html += '<div class="scroll"><table><thead><tr><th>node_reader</th><th>Nodes</th><th>reads</th></tr></thead><tbody>'
    + LOOK.node_readers.map(d => `<tr><td>${esc(d.name)}</td><td class="num">${d.body === null ? d.nodes.length : 'the body\\'s'}</td><td>${d.body === null ? 'its Nodes' : 'body ' + d.body}</td></tr>`).join('') + '</tbody></table></div>';
  byId('numbers').innerHTML = html;
  const books = LOOK.books || {}, keys = Object.keys(Object.values(books)[0] || {});
  byId('books').innerHTML = keys.length ? '<div class="scroll"><table><thead><tr><th>family</th>' + keys.map(k => `<th>${esc(k.replace('_', ' '))}</th>`).join('') + '</tr></thead><tbody>'
    + Object.entries(books).map(([name, book]) => `<tr><td>${esc(name)}</td>` + keys.map(k => `<td class="num">${format(book[k])}</td>`).join('') + '</tr>').join('') + '</tbody></table></div>' : '<p>No interval was run.</p>';
}

/* The blind as a table: every number and short list of the expectation file a row, a nested object's rows named key.subkey, a list of lists or of objects as it is written, and its words (comments, statuses) under a fold; nothing of the page's own. */
function blindTable() {
  const box = byId('blind-box');
  if (!Object.keys(BLIND).length) { box.innerHTML = '<p>No blind file was given.</p>'; return; }
  const rows = [], words = [], most = size('--blind-words'), many = size('--blind-list');
  const plain = v => Array.isArray(v) ? (v.some(x => x && typeof x === 'object') ? JSON.stringify(v) : v.map(plain).join(', ')) : v === null ? 'none' : format(v);
  const walk = (name, v) => {
    if (typeof v === 'string' && v.length > most) words.push([name, v]);
    else if (Array.isArray(v)) rows.push([name, v.length > many ? plain(v.slice(0, many)) + ', ... (' + format(v.length) + ' in all)' : plain(v)]);
    else if (v && typeof v === 'object') Object.entries(v).forEach(([k, w]) => walk(name + '.' + k, w));
    else rows.push([name, plain(v)]);
  };
  Object.entries(BLIND).forEach(([k, v]) => walk(k, v));
  const row = ([k, v]) => `<tr><td>${esc(k)}</td><td class="num">${esc(v)}</td></tr>`, head = '<table><thead><tr><th>the blind file, key</th><th>value</th></tr></thead><tbody>', first = size('--blind-rows');
  box.innerHTML = '<div class="scroll">' + head + rows.slice(0, first).map(row).join('') + '</tbody></table></div>'
    + (rows.length > first ? '<details><summary>the blind file, ' + format(rows.length - first) + ' more rows</summary><div class="scroll">' + head + rows.slice(first).map(row).join('') + '</tbody></table></div></details>' : '')
    + (words.length ? '<details><summary>the blind file, its words: ' + esc(words.map(([k]) => k).join(', ')) + '</summary>' + words.map(([k, v]) => `<p><b>${esc(k)}</b> ${esc(v)}</p>`).join('') + '</details>' : '');
}

/* The reading of the output file against the blind (tools/click_counts.py's file): one bar per reporter for the rounded shares (N by the shares, the expectation), one beside it for the clicks the draw credited (the measurement), the dashed blind curve, the totals, and one table of every row the reader compares, read against blind with the difference. */
function drawReading() {
  const r = READ, rs = r.rounded_shares, n = rs.row.length, family = r.family, box = byId('measure'), hex = ROLES[family] ? colourOf(family) : token('--fg'), flash = token('--flash');
  byId('measure-box').classList.add('wide');
  measurePicker.textContent = `${r.node_reader.join(', ')}, ${family}, within the window ${r.window[0]} to ${r.window[1]}, the seed ${format(r.seed)}: the output file read by tools/click_counts.py, one bar per reporter across ${r.across}`;
  const slot = size('--bar-slot') * 1.8, pad = size('--graph-pad'), left = pad * 8, bottom = pad * 3, H = size('--graph-height') * 2;
  const clicks = r.clicks ? r.clicks.row : null, blind = (r.blind.counts || []).map(v => typeof v === 'number' ? v : null);
  const W = Math.max(size('--graph-width'), left + slot * n + pad), high = Math.max(1, ...rs.row, ...(clicks || []), ...blind.filter(v => v !== null));
  const px = k => left + slot * (k + 0.5), py = v => pad + (high - v) / high * (H - pad - bottom), w = Math.max(1, slot * 0.3);
  let body = '';
  if (Array.isArray(BLIND.pattern) && BLIND.pattern.length === 2 && n) {
    const [first, last] = BLIND.pattern.map(v => Math.max(0, Math.min(n - 1, v)));
    body += `<rect x="${(px(first) - slot / 2).toFixed(1)}" y="${pad}" width="${(slot * (last - first + 1)).toFixed(1)}" height="${(H - pad - bottom).toFixed(1)}" fill="${token('--window')}"><title>the pattern's range: ${r.across} ${r.at[first]} to ${r.at[last]}</title></rect>`;
  }
  body += `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}"/>` + svgText(format(high), left - 3, pad + size('--small') * 0.3, 'end') + svgText('0', left - 3, py(0), 'end');
  const every = Math.max(1, Math.ceil(n / 16));
  rs.row.forEach((v, k) => {
    body += `<rect x="${(px(k) - w).toFixed(1)}" y="${py(v).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(v)).toFixed(1)}" fill="${hex}"><title>${esc(r.node_reader[k])}: ${format(v)} by the shares, saw ${format(r.seen[k])}${blind[k] === null ? '' : ', the blind ' + format(blind[k])}</title></rect>`;
    if (clicks) body += `<rect x="${px(k).toFixed(1)}" y="${py(clicks[k]).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(clicks[k])).toFixed(1)}" fill="${flash}"><title>${esc(r.node_reader[k])}: ${format(clicks[k])} clicks credited by the draw</title></rect>`;
    if (k % every === 0 || k === n - 1) body += svgText(r.at[k], px(k), H - pad, 'middle');
  });
  if (blind.some(v => v !== null)) {
    const points = blind.map((v, k) => v === null ? null : px(k).toFixed(1) + ',' + py(v).toFixed(1)).filter(Boolean).join(' ');
    body += `<polyline fill="none" stroke="${token('--blind')}" stroke-width="${size('--line-width')}" stroke-dasharray="5 4" points="${points}"/>` + svgText('blind', W - pad, pad + size('--small') * 0.3, 'end');
  }
  const legend = `<span><i style="border-color:${hex};border-top-width:6px"></i>${esc(family)}, the rounded shares per reporter (N by the shares of the output file's click lines, the expectation)</span>` + (clicks ? `<span><i style="border-color:${flash};border-top-width:6px"></i>the clicks the draw credited (the credit lines, the measurement)</span>` : '') + `<span><i class="dashed" style="border-color:${token('--blind')}"></i>blind</span>` + (Array.isArray(BLIND.pattern) ? `<span><i style="border-color:${token('--window')};border-top-width:6px"></i>the pattern's range</span>` : '');
  box.innerHTML = `<div class="caption"><b>The output file's credit of ${esc(family)} at ${format(n)} reporters across ${esc(r.across)}, beside the blind</b><span>measurement</span></div><div class="legend">${legend}</div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="the reading's bars beside the blind">${body}</svg>`;
  const credited = clicks ? clicks.reduce((a, b) => a + b, 0) : null;
  byId('totals').textContent = `N ${format(r.quanta)} by the shares (the blind ${format(r.blind_quanta)}); ` + (clicks ? `${format(credited)} clicks credited by the draw with the seed ${format(r.seed)}` : 'no draw declared, no click credited') + `; laid ${format(r.laid)}, elsewhere ${format(r.elsewhere)}` + (r.floored ? '; a region floored at 0' : '');
  byId('watch').innerHTML = readingTable();
}
function readingTable() {
  const r = READ, rs = r.rounded_shares, b = r.blind || {}, a = r.arrival || {}, ba = r.blind_arrival || {}, rows = [];
  const text = v => v === null || v === undefined ? 'none' : Array.isArray(v) ? (v.some(x => x && typeof x === 'object') ? JSON.stringify(v) : v.map(text).join(', ')) : typeof v === 'object' ? JSON.stringify(v) : format(v);
  const signed = v => (v > 0 ? '+' : '') + format(Math.round(v * 100) / 100);
  const numbers = v => Array.isArray(v) && v.length && v.every(x => typeof x === 'number');
  const diff = (x, y) => typeof x === 'number' && typeof y === 'number' ? (x - y === 0 ? 'the same' : signed(x - y)) : numbers(x) && numbers(y) && x.length === y.length ? (x.every((v, k) => v === y[k]) ? 'the same' : x.map((v, k) => signed(v - y[k])).join(', ')) : x === null || x === undefined || y === null || y === undefined ? '' : JSON.stringify(x) === JSON.stringify(y) ? 'the same' : 'differs';
  const put = (what, x, y) => rows.push([what, text(x), text(y), diff(x, y)]);
  put('N, the screen\u2019s inflow over W_c, to the nearest whole', r.quanta, r.blind_quanta);
  put('laid by the generator; elsewhere, laid less N', [r.laid, r.elsewhere], [r.laid, 0]);
  put('maxima within the pattern, by the shares', rs.maxima, b.maxima);
  put('minima, by the shares (the blind its first minima)', rs.minima, b.minima);
  put('visibility at the central maximum, by the shares [most - least, most + least]', rs.visibility, b.visibility);
  put('wings, by the shares (the blind the lattice\u2019s; the continuum\u2019s beside)', rs.wings, b.wings && b.wings.lattice ? b.wings.lattice : b.wings);
  if (b.wings && b.wings.continuum) put('wings, the continuum\u2019s number', rs.wings, b.wings.continuum);
  put('deviation from the blind row\u2019s shares, [numerator, denominator]', rs.deviation, [0, rs.deviation ? rs.deviation[1] : 1]);
  if (r.clicks) { put('maxima, the clicks the draw credited', r.clicks.maxima, b.maxima); put('minima, the clicks', r.clicks.minima, b.minima); put('visibility, the clicks', r.clicks.visibility, b.visibility); put('deviation, the clicks', r.clicks.deviation, [0, r.clicks.deviation ? r.clicks.deviation[1] : 1]); }
  if (a.peak !== undefined) put('arrival: the peak interval', a.peak, ba.peak);
  if (Array.isArray(a.centroid)) put('arrival: the centroid interval', Math.round(a.centroid[0] / a.centroid[1] * 100) / 100, ba.centroid);
  if (a.span) put('arrival: the half-maximum span', a.span, ba.span);
  for (const [name, seen] of Object.entries(r.aside || {})) put(`the bare region ${name}: seen, quanta`, [seen.seen, seen.quanta], 'nothing');
  return '<div class="scroll"><table><thead><tr><th>what tools/click_counts.py compares</th><th>read from the output file</th><th>the blind, written first</th><th>the difference</th></tr></thead><tbody>' + rows.map(cells => '<tr>' + cells.map((c, k) => `<td${k ? ' class="num"' : ''}>${esc(c)}</td>`).join('') + '</tr>').join('') + '</tbody></table></div>';
}

/* The arrival: with an expectation across an axis, the reporters' inflow per interval (their click lines summed, the negative ones included, in quanta over the family's wall) and the quanta gathered within the window up to each interval; the blind's peak, centroid and span marked where the blind names an arrival, the blind's total where it names one; the measurement over the intervals. */
function drawArrival() {
  const m = READ ? { labels: READ.node_reader, family: READ.family, window: READ.window } : MEASURE, box = byId('arrival'); box.innerHTML = ''; byId('arrival-box').hidden = false;
  const wall = WALL[m.family] || 1, per = new Float64Array(T + 1), gathered = new Float64Array(T + 1), hex = ROLES[m.family] ? colourOf(m.family) : token('--fg');
  for (const name of m.labels) for (const [tick, inflow] of (reportsAt[name] || {})[m.family] || []) if (tick <= T) per[tick] += inflow / wall;
  let sum = 0;
  for (let k = 0; k <= T; k++) { if (k >= m.window[0] && k <= m.window[1]) sum += per[k]; gathered[k] = sum; }
  const arrival = BLIND.arrival && typeof BLIND.arrival === 'object' ? BLIND.arrival : null, total = Number(BLIND.quanta !== undefined ? BLIND.quanta : BLIND.through);
  const marks = (px, py, low, high) => {
    let body = '';
    if (!arrival) return body;
    if (Array.isArray(arrival.span) && arrival.span.length === 2) body += `<rect x="${px(arrival.span[0]).toFixed(1)}" y="${py(high).toFixed(1)}" width="${(px(arrival.span[1]) - px(arrival.span[0])).toFixed(1)}" height="${(py(low) - py(high)).toFixed(1)}" fill="${token('--window')}"><title>the blind span, intervals ${arrival.span[0]} to ${arrival.span[1]}</title></rect>`;
    [['peak', '5 4'], ['centroid', '2 3']].forEach(([key, dash], k) => { if (typeof arrival[key] !== 'number') return; body += `<line x1="${px(arrival[key]).toFixed(1)}" x2="${px(arrival[key]).toFixed(1)}" y1="${py(high).toFixed(1)}" y2="${py(low).toFixed(1)}" stroke="${token('--blind')}" stroke-dasharray="${dash}"><title>the blind ${key}, interval ${arrival[key]}</title></line>` + svgText('blind ' + key + ' ' + format(arrival[key]), px(arrival[key]) + 2, py(high) + size('--small') * (0.75 + 0.85 * k), 'start'); });
    return body;
  };
  const line = (px, py, low, high) => isFinite(total) && total >= low && total <= high ? `<line x1="${px(0).toFixed(1)}" x2="${px(T).toFixed(1)}" y1="${py(total).toFixed(1)}" y2="${py(total).toFixed(1)}" stroke="${token('--blind')}" stroke-dasharray="5 4"><title>the blind total ${format(total)}</title></line>` + svgText('blind ' + format(total), px(T), py(total) - 2, 'end') : '';
  const add = (title, name, values, extra) => { const g = document.createElement('div'); g.className = 'graph'; box.append(g); graph(g, title, [{ name, values, colour: hex, dashed: false }], 'measurement', extra, [size('--arrival-width'), size('--arrival-height')]); };
  add(`The inflow of ${m.family} at the ${m.labels.length} reporters per interval, in quanta over W_c ${format(wall)}`, "the reporters' click lines summed", per, marks);
  add(`The quanta gathered within the window ${m.window[0]} to ${m.window[1]}, up to each interval`, 'N so far, the inflow over W_c', gathered, line);
  if (OUTPUT) {
    const credited = new Float64Array(T + 1);
    for (const name of m.labels) for (const [tick, count] of CREDITS_AT[name] || []) if (tick <= T) credited[tick] += count;
    for (let k = 1; k <= T; k++) credited[k] += credited[k - 1];
    if (credited[T]) add(`The clicks the draw credited at the ${m.labels.length} reporters, up to each interval (the credit lines)`, 'clicks credited so far', credited, line);
    const density = new Float64Array(T + 1), at = DENSITY_AT[m.family] || {};
    for (const name of m.labels) { let last = 0, next = 0; const changes = at[name] || []; for (let k = 0; k <= T; k++) { while (next < changes.length && changes[next][0] <= k) { last = changes[next][1] === null ? last : changes[next][1]; next++; } density[k] += last; } }
    const g = document.createElement('div'); g.className = 'graph'; box.append(g);
    graph(g, `The density of ${m.family} over the ${m.labels.length} reporters\u2019 Nodes per interval, in quanta (the density lines)`, [{ name: 'GAMEBOARD, the share at the regions, a diagnostic and no click', values: density, colour: token('--field'), dashed: true }], 'GameBoard reading', null, [size('--arrival-width'), size('--arrival-height')]);
  }
  moveCursors();
}

{{GATE_SCRIPT}}/* The start: the title, the verdict, frame 0. */
byId('title').textContent = document.title;
byId('verdict').textContent = LOOK.verdict + (LOOK.reason ? ': ' + LOOK.reason : '') + ' (' + LOOK.label + ')';
byId('source').textContent = OUTPUT ? `the output file: ${OUTPUT.verdict}, ${format(OUTPUT.ticks)} intervals, ${format(CLICKS.length)} click lines` + (SAME_LINES ? ', the look\u2019s click lines the same' : `, the look\u2019s ${format(LOOK_CLICKS.length)} click lines DIFFER`) : 'no output file given: the measurement from the look\u2019s own lines';
function start() { themed(); fit(); numbers(); blindTable(); drawGraphs(); if (READ) { drawReading(); drawArrival(); } else if (MEASURE) { drawNodeMeasure(); drawArrival(); } draw(); }
start();
})();
</script>
"""

# The gate's panels, inserted at the template's three markers with a reading and absent without one.
GATE_PANELS = """
<script id="gate" type="application/json">{{GATE}}</script>
<script id="beside" type="application/json">{{BESIDE}}</script>
  <section class="panel">
    <h2>The gate's input and run, seen from above</h2>
    <div class="graph" id="gate-above"></div>
    <div id="gate-sides"></div>
  </section>
  <section class="panel">
    <h2>The parts lines per region</h2>
    <div class="stack" id="gate-parts"></div>
  </section>
  <section class="panel wide">
    <h2>The gate's reading beside the blind</h2>
    <div class="stack" id="gate-reading"></div>
  </section>"""

GATE_SCRIPT = r"""/* The gate's panels (the joint-share reader's file over the gate's worlds and the blind of the gate's form): the board from above at the frame shown, the parts lines per region and the reader's credit beside the blind; every number the look's, the reader's or the blind's, the page comparing them and summing nothing new. */
const GATE = JSON.parse(byId('gate').textContent), BESIDE = JSON.parse(byId('beside').textContent);
const READING = GATE.reading, WORLD = READING.worlds[GATE.world], KEY = GATE.key, EXPECTED = BLIND.blind || {};
const SIDES = Object.keys(BLIND.sides), NAME = String(BLIND.combination.name), GATE_FAMILY = String(BLIND.family);
const SIDE_TONES = ['--matter', '--light', '--field', '--flash', '--ring'], CREDITS = ['by_the_parts_shares', 'by_the_local_sums', 'by_the_sign'];
const sideColour = k => token(SIDE_TONES[k % SIDE_TONES.length]), gateHex = () => ROLES[GATE_FAMILY] ? colourOf(GATE_FAMILY) : token('--fg');
const frac = v => v === null || v === undefined ? 'none' : v[1] === 1 ? format(v[0]) : format(v[0]) + ' / ' + format(v[1]);
const ratio = v => v === null || v === undefined ? NaN : v[0] / v[1];
const same = (u, v) => u !== null && u !== undefined && v !== null && v !== undefined && u[0] === v[0] && u[1] === v[1];
const verdictOf = (u, v) => same(u, v) ? 'MATCH' : 'differs';
const port = key => String(key).split(' ').map(p => p === 'plus' ? '+' : p === 'minus' ? '\u2212' : p).join(' ');
const regionOf = label => LOOK.node_readers.find(d => d.name === BLIND.sides[label]) || { name: String(BLIND.sides[label]), nodes: [], body: null };
const clickedAt = (frame, name) => frame.lines.some(line => line.event === 'click' && line.node_reader === name && line.family === GATE_FAMILY);
const AT_MOST = /at most (\d+)/, boundOf = text => { const m = AT_MOST.exec(String(text || '')); return m ? Number(m[1]) : null; };
const FENCE = CREDITS.map(f => boundOf((EXPECTED[f] || {}).status)).find(b => b !== null) ?? null;

/* From above: the two unfolded axes (a chain with its folded neighbour), the third summed; the view the frame's own box, growing with it. */
const UNFOLDED = [0, 1, 2].filter(a => !LOOK.folded[a]), U = UNFOLDED[0] ?? 0, V = UNFOLDED[1] ?? [0, 1, 2].find(a => a !== U);
function drawAbove() {
  const frame = LOOK.frames[t], row = frameOf(t)[GATE_FAMILY] || {}, count = row.count, cells = new Map();
  const o = originOf(frame), s = shapeOf(frame), left = o[U], top = o[V] + s[V];
  const px = u => u - left, py = v => top - 1 - v;
  if (count) for (let i = 0; i < N; i++) if (count[i]) { const n = nodeOf(i), k = px(n[U]) * s[V] + py(n[V]); cells.set(k, (cells.get(k) || 0) + count[i]); }
  const most = Math.sqrt(Math.max(0, ...Array.from(cells.values(), Math.abs))) || 1;
  let body = `<rect x="0" y="0" width="${s[U]}" height="${s[V]}" fill="${token('--board')}" stroke="${token('--line')}" stroke-width="0.3"/>`;
  for (const [k, c] of cells) {
    const x = Math.floor(k / s[V]), y = k % s[V], strength = Math.min(1, Math.sqrt(Math.abs(c)) / most);
    body += c > 0 ? `<rect x="${x}" y="${y}" width="1" height="1" fill="${gateHex()}" fill-opacity="${strength.toFixed(3)}"/>` : `<rect x="${x + 0.15}" y="${y + 0.15}" width="0.7" height="0.7" fill="none" stroke="${gateHex()}" stroke-width="0.2"/>`;
  }
  const letter = Math.max(2, Math.min(s[U], s[V]) / 16);
  SIDES.forEach((label, k) => {
    const region = regionOf(label), nodes = region.body === null ? region.nodes : frame.bodies[region.body], flashing = clickedAt(frame, region.name);
    const stroke = flashing ? token('--flash') : sideColour(k);
    for (const n of nodes) body += `<rect x="${px(n[U]) + 0.1}" y="${py(n[V]) + 0.1}" width="0.8" height="0.8" fill="none" stroke="${stroke}" stroke-width="${flashing ? 0.3 : 0.15}"/>`;
    if (nodes.length) {
      const cx = nodes.reduce((a, n) => a + px(n[U]) + 0.5, 0) / nodes.length, cy = nodes.reduce((a, n) => a + py(n[V]) + 0.5, 0) / nodes.length;
      body += `<text x="${cx.toFixed(1)}" y="${(cy + letter * 0.35).toFixed(1)}" text-anchor="middle" font-size="${letter}" font-family="${esc(token('--font-mono'))}" font-weight="600" fill="${stroke}">${esc(label)}</text>`;
    }
  });
  body += `<text x="${s[U] - 0.3}" y="${s[V] - 0.5}" text-anchor="end" font-size="${letter}" font-family="${esc(token('--font-mono'))}" fill="${token('--muted')}">${AXES[U]}</text><text x="0.3" y="${letter}" font-size="${letter}" font-family="${esc(token('--font-mono'))}" fill="${token('--muted')}">${AXES[V]}</text>`;
  const title = t === 0 ? `The input as laid: ${esc(GATE_FAMILY)}'s record at its Nodes and the ${SIDES.length} regions` : `Interval ${t}: the beams of ${esc(GATE_FAMILY)} and the ${SIDES.length} regions`;
  byId('gate-above').innerHTML = `<div class="caption"><b>${title}</b><span>GameBoard reading, a diagnostic</span></div><svg viewBox="0 0 ${s[U]} ${s[V]}" role="img" aria-label="the board from above" shape-rendering="crispEdges" style="max-height: var(--board-height)">${body}</svg><div class="caption"><span>${AXES[U]} across, ${AXES[V]} up; a Node's count of ${esc(GATE_FAMILY)} as the cell's depth against the frame's largest (a hollow cell a count below 0); the box the frame's own, ${s[U]} x ${s[V]} at the file's coordinates from (${left}, ${o[V]})</span></div>`;
}
function sidesList() {
  const family = FAMILIES.find(f => f.name === GATE_FAMILY), rows = SIDES.map((label, k) => {
    const region = regionOf(label), basis = WORLD.bases[label] || [], pattern = WORLD.patterns[label] || [];
    return `<dt style="color:${sideColour(k)}">${esc(label)}</dt><dd>${esc(region.name)}, ${format(region.nodes.length)} Nodes: the setting (p, q) = (${basis.map(format).join(', ')}), the pattern ${pattern.map(part => '[' + part.map(format).join(', ') + ']').join(' ')}</dd>`;
  });
  byId('gate-sides').innerHTML = `<dl>${rows.join('')}<dt>record</dt><dd>${esc(GATE_FAMILY)}, ${family ? format(family.lines) + ' parts laid alike' : 'not in the look'}; frame 0 the world as laid</dd><dt>declared</dt><dd>the settings and the patterns are the world file's, read by the reader (${esc(WORLD.world)}) and by nothing in the engine; the regions' Nodes are the file's</dd></dl>`;
}

/* The parts lines: per region the parts' signed level sums (now) over the intervals, the parts overlaid, and a strip of its click lines. */
const PARTS_AT = {};
for (const frame of LOOK.frames) for (const line of frame.lines) if (line.event === 'parts' && line.family === GATE_FAMILY) (PARTS_AT[line.node_reader] || (PARTS_AT[line.node_reader] = {}))[line.tick] = line.levels;
function drawParts() {
  const box = byId('gate-parts'); box.innerHTML = '';
  SIDES.forEach((label, k) => {
    const region = regionOf(label), at = PARTS_AT[region.name] || {}, parts = Math.max(0, ...Object.values(at).map(levels => levels.length));
    const series = Array.from({ length: parts }, (_, p) => ({ name: label + ' part ' + (p + 1), colour: sideColour(k), dashed: p > 0, values: Float64Array.from({ length: T + 1 }, (_, i) => at[i] && at[i][p] ? at[i][p][0] : 0) }));
    const g = document.createElement('div'); g.className = 'graph'; box.append(g);
    graph(g, `The parts at ${region.name} (${label}): ${parts} parts overlaid, the sums now`, series, "the parts lines, the NodeReader's read");
    const clicks = (reportsAt[region.name] || {})[GATE_FAMILY] || [];
    if (!g.dataset.px) return;
    const [left, right, frames] = JSON.parse(g.dataset.px), W = size('--graph-width'), h = size('--graph-pad') * 3, px = i => left + (frames > 1 ? i / (frames - 1) : 0) * (right - left);
    const marks = clicks.map(([tick, inflow]) => `<line x1="${px(tick).toFixed(1)}" x2="${px(tick).toFixed(1)}" y1="0" y2="${h - size('--small')}" stroke="${token('--flash')}" stroke-width="1"><title>click at interval ${tick}: the inflow ${format(inflow)}</title></line>`).join('');
    g.insertAdjacentHTML('beforeend', `<svg viewBox="0 0 ${W} ${h}" role="img" aria-label="the click lines of ${esc(region.name)}">${marks}${svgText(format(clicks.length) + ' click lines of ' + region.name + ' (the measurement)', right, h - 1, 'end')}</svg>`);
  });
  moveCursors();
}

/* The reading: the joint shares as shareBars beside the blind, the world's numbers in one table, the combination over the gate's worlds on its ruler, the otherGate gate's line. */
function shareBars() {
  const keys = Object.keys(WORLD.shares || {}), n = keys.length, blind = (EXPECTED.shares || {})[KEY] || {}, drawn = WORLD.drawn ? WORLD.drawn.join(' ') : null;
  const W = size('--graph-width') * 1.5, H = size('--graph-height') * 2, pad = size('--graph-pad'), left = pad * 6, bottom = pad * 9, small = size('--small') * 0.75;
  const slot = (W - left - pad) / Math.max(n, 1), py = v => pad + (1 - v) * (H - pad - bottom), w = Math.max(1, slot * 0.3);
  let body = `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}"/>` + svgText('1', left - 3, pad + small * 0.4, 'end') + svgText('0', left - 3, py(0), 'end');
  keys.forEach((key, k) => {
    const x = left + slot * (k + 0.5), run = WORLD.shares[key], expected = blind[key], rv = run ? ratio(run) : 0;
    body += `<rect x="${(x - w).toFixed(1)}" y="${py(rv).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(rv)).toFixed(1)}" fill="${gateHex()}"><title>${port(key)}: the run's share ${frac(run)}, J = ${frac(WORLD.joint[key])}</title></rect>`;
    if (expected) body += `<rect x="${x.toFixed(1)}" y="${py(ratio(expected)).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(ratio(expected))).toFixed(1)}" fill="none" stroke="${token('--blind')}" stroke-dasharray="3 2"><title>${port(key)}: the blind's share ${frac(expected)}</title></rect>`;
    body += svgText(port(key), x, H - bottom + small * 1.2, 'middle') + svgText(frac(run), x, H - bottom + small * 2.4, 'middle') + (expected ? svgText('blind ' + frac(expected), x, H - bottom + small * 3.6, 'middle') : '') + (key === drawn ? svgText('drawn: the click', x, H - bottom + small * 4.8, 'middle') : '');
  });
  const identical = n > 0 && keys.every(key => same(WORLD.shares[key], blind[key]));
  const legend = `<span><i style="border-color:${gateHex()};border-top-width:6px"></i>the run's shares J over their sum (the reader's credit over the parts lines)</span><span><i class="dashed" style="border-color:${token('--blind')}"></i>the blind's shares</span><span>drawn: the combination of ports drawn by the shares with the declared seed, the click</span>`;
  return `<div class="graph"><div class="caption"><b>The ${n} joint shares at (${esc(KEY)}): ${identical ? 'the blind\u2019s exactly' : 'the run beside the blind'}</b><span>the reader's credit over the parts lines</span></div><div class="legend">${legend}</div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="the joint shares beside the blind" style="max-width: var(--measure-width)">${body}</svg></div>`;
}
function worldTable() {
  const rows = [[`E_${SIDES.length}, the correlation over the ${SIDES.length} sides`, WORLD.correlation, (EXPECTED.correlation || {})[KEY]]];
  for (const label of SIDES) rows.push([`the marginal P(+) of ${label} (${regionOf(label).name})`, (WORLD.marginals || {})[label], ((EXPECTED.marginals || {})[KEY] || {})[label]]);
  for (const [subset, e] of Object.entries(WORLD.sub_correlations || {})) rows.push([`E over ${subset} alone`, e, ((EXPECTED.sub_correlations || {})[KEY] || {})[subset]]);
  for (const f of CREDITS) rows.push([`E ${f.replace(/_/g, ' ')}, a local credit (the fence)`, WORLD[f], ((EXPECTED[f] || {}).correlation || {})[KEY]]);
  const cells = rows.map(([what, run, expected]) => `<tr><td>${esc(what)}</td><td class="num">${frac(run)}</td><td class="num">${frac(expected)}</td><td>${verdictOf(run, expected)}</td></tr>`).join('');
  const quanta = Object.entries(WORLD.quanta || {}).map(([label, [inflow, wall]]) => `${label} ${format(inflow)} over W_c ${format(wall)}, about ${format(Math.round(inflow / wall))} quanta`).join('; ');
  const mismatch = WORLD.mismatch || {}, ratios = (mismatch.ratios || []).map(frac).join(', ');
  return `<div class="scroll"><table><thead><tr><th>${esc(GATE_FAMILY)} at (${esc(KEY)}), the world ${esc(WORLD.world)}</th><th>the run (the reader's credit)</th><th>the blind</th><th></th></tr></thead><tbody>${cells}</tbody></table></div>`
    + `<div class="totals">drawn ${WORLD.drawn ? port(WORLD.drawn.join(' ')) : 'nothing'} (the click, one combination by the shares with the seed ${format(BLIND.seed)}); ${format(WORLD.intervals_reported)} intervals reported within the window ${(BLIND.window || []).join(' to ')}; the sides' inflow: ${quanta}</div>`
    + `<div class="watch">${esc(mismatch.label || 'GAMEBOARD')}, a diagnostic and no credit: the parts' cross-side products' ratios to the first part's ${ratios || 'none'}, rho ${frac(mismatch.rho)}</div>`;
}
function rulerOf(most) {
  const run = READING[NAME], expected = EXPECTED[NAME], W = size('--graph-width') * 1.5, H = size('--graph-height'), pad = size('--graph-pad'), left = pad * 5, right = W - pad * 5, mid = H / 2, small = size('--small') * 0.75;
  const px = v => left + (v + most) / (2 * most) * (right - left);
  let body = FENCE === null ? '' : `<rect x="${px(-FENCE).toFixed(1)}" y="${pad}" width="${(px(FENCE) - px(-FENCE)).toFixed(1)}" height="${H - 2 * pad}" fill="${token('--window')}"><title>the fence: |${NAME}| at most ${FENCE}, the blind's theorem lines</title></rect>`;
  body += `<line x1="${left}" x2="${right}" y1="${mid}" y2="${mid}" stroke="${token('--line')}"/>`;
  for (let v = -most; v <= most; v++) body += `<line x1="${px(v)}" x2="${px(v)}" y1="${mid - 4}" y2="${mid + 4}" stroke="${token('--line')}"/>` + svgText(format(v), px(v), H - pad, 'middle');
  CREDITS.forEach((f, k) => { const own = READING[NAME + '_' + f]; if (own) body += `<path d="M ${px(ratio(own)).toFixed(1)} ${mid - 2} l -5 -8 h 10 z" fill="${token('--muted')}"><title>the local credit ${f.replace(/_/g, ' ')}: ${NAME} = ${frac(own)} (the blind ${frac((EXPECTED[f] || {})[NAME])})</title></path>` + (k === 0 ? svgText('the local credits, the fence', px(ratio(own)), mid - 12, 'middle') : ''); });
  if (expected) body += `<circle cx="${px(ratio(expected)).toFixed(1)}" cy="${mid}" r="8" fill="none" stroke="${token('--blind')}" stroke-dasharray="3 2"><title>the blind's ${NAME} = ${frac(expected)}</title></circle>`;
  if (run) body += `<circle cx="${px(ratio(run)).toFixed(1)}" cy="${mid}" r="4.5" fill="${gateHex()}"><title>the run's ${NAME} = ${frac(run)}</title></circle>` + svgText(NAME + ' = ' + frac(run), px(ratio(run)), mid + 16 + small, 'middle');
  body += svgText('the algebraic maximum, one per term', right, pad + small, 'end') + (FENCE === null ? '' : svgText('|' + NAME + '| at most ' + FENCE + ', local realism', px(0), pad + small, 'middle'));
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(NAME)} on its ruler" style="max-width: var(--measure-width)">${body}</svg>`;
}
function combinationBox() {
  const order = BLIND.order, signs = BLIND.combination.signs.map(Number), most = signs.reduce((s, v) => s + Math.abs(v), 0);
  const formula = NAME + ' = ' + order.map((key, i) => (signs[i] < 0 ? (i ? ' \u2212 ' : '\u2212 ') : (i ? ' + ' : '')) + 'E(' + key + ')').join('');
  const rows = order.map(key => `<tr><td>${esc(key)}${key === KEY ? ' (this page)' : ''}</td><td>${esc(String(BLIND.runs[key]))}</td><td class="num">${frac((READING.correlation || {})[key])}</td><td class="num">${frac((EXPECTED.correlation || {})[key])}</td><td>${verdictOf((READING.correlation || {})[key], (EXPECTED.correlation || {})[key])}</td></tr>`).join('');
  const credits = CREDITS.map(f => `${f.replace(/_/g, ' ')} ${frac(READING[NAME + '_' + f])} (the blind ${frac((EXPECTED[f] || {})[NAME])})`).join('; ');
  const statuses = CREDITS.map(f => (EXPECTED[f] || {}).status).filter(Boolean).map(text => `<div class="watch">${esc(text)}</div>`).join('');
  return `<div class="graph"><div class="caption"><b>${esc(formula)}</b><span>over the gate's ${format(order.length)} worlds, the reader's file beside the blind</span></div>`
    + `<div class="scroll"><table><thead><tr><th>settings</th><th>world</th><th>E, the run</th><th>E, the blind</th><th></th></tr></thead><tbody>${rows}</tbody></table></div>${rulerOf(most)}`
    + `<div class="totals">${esc(NAME)} = ${frac(READING[NAME])} by the meeting, the run; the blind ${frac(EXPECTED[NAME])}, ${verdictOf(READING[NAME], EXPECTED[NAME])}; the algebraic maximum ${format(most)}, one per term; the local credits as the fence: ${esc(credits)}</div>${statuses}</div>`;
}
function otherGate() {
  if (!BESIDE) return '';
  const name = String(BESIDE.combination.name), fence = CREDITS.map(f => boundOf(((BESIDE.blind || {})[f] || {}).status)).find(b => b !== null);
  return `<div class="totals">Beside it, the other gate's blind, ${esc(BESIDE.file)}: ${esc(name)} = ${frac((BESIDE.blind || {})[name])} for ${esc(String(BESIDE.family))} over ${format(Object.keys(BESIDE.sides || {}).length)} sides at the settings ${esc(JSON.stringify(BESIDE.settings || {}))}${fence === null || fence === undefined ? '' : ', its fence |' + esc(name) + '| at most ' + format(fence)}</div>`;
}
function drawReading() { byId('gate-reading').innerHTML = shareBars() + worldTable() + combinationBox() + otherGate(); }
let gateTheme = '';
function drawGate() {
  drawAbove();
  const frame = LOOK.frames[t], counts = {}, clicked = frame.lines.filter(line => line.event === 'click').map(line => line.node_reader + ': ' + line.family);
  for (const line of frame.lines) counts[line.event] = (counts[line.event] || 0) + 1;
  if (t) byId('lines').textContent = Object.entries(counts).map(([event, n]) => n + ' ' + event + (n === 1 ? ' line' : ' lines')).join(', ') + (clicked.length ? ' (' + [...new Set(clicked)].join(', ') + ')' : '') || 'no line this interval';
  const theme = token('--fg') + token('--matter');
  if (theme !== gateTheme) { gateTheme = theme; sidesList(); drawParts(); drawReading(); }
}

"""

GATE_MARKERS = {
    "{{GATE_PANELS}}": GATE_PANELS,
    "{{GATE_SCRIPT}}": GATE_SCRIPT,
    "{{GATE_DRAW}}": " drawGate();",
}


if __name__ == "__main__":
    main()
