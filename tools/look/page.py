"""The look's page builder, a diagnostic (docs/ENGINE.md #6-how-to-run-a-world): one self-contained HTML page from a look file written by `tools/look/record.py` and, if the world's folder holds one, its blind expectation file, the look embedded gzip-compressed and base64-encoded and inflated by the browser's own DecompressionStream at load, so that a look of many frames fits one page with every number untouched. The page shows the lattice as cubes (a folded axis as a plane of thin slabs; the inner faces the world declares as dark cubes with their gaps open, "the faces (declared)" in the legend; a board with a receding face at the shape of each frame, its box drawn per frame and every Node at the file's coordinates), one frame per interval with a slider and play and nothing between frames (a strided look, record.py's `--every K`, one frame per kept interval, every sum up to the frame shown, every mark at an interval and the window's marker reading the frame's own interval and never its position), the reading's window marked on the slider; a look of several passes (record.py's frames from the lattice's observers on a world of a record read at declared sides, each frame carrying its `pass`, 1 the run to the first close, then per side a run back to the record's birth with its intervals decreasing and a run forward to the next close, and its `direction`, +1 or -1) runs the slider over the frames in the look's order, labels the frame with its own interval, its pass and its direction, marks the direction beside the slider and the passes' bounds on the slider and on every graph over the frames, counts every sum up to the frame shown over the lines of the frames up to it, a click line belonging to the pass it was written in, and places every line of the run's output at the frame of its pass, a look of one pass (no `pass` key) rendering as before; a look whose header carries the run back's reach (`reach` cone, the record's light cone; `cone_support`, the birth's Nodes at the file's coordinates (the lay's for a record laid at the start); `cone_volume`, the cone's Nodes per interval) and whose frames of the run back and forward carry `cone_radius` (t + 1 at the interval t) shades the Nodes within that many Links of the support in a tone of their own, on the board and on the gate's view from above, the Link metric with the wrap as the engine's front counts its shells (per axis |d|, on a periodic axis the lesser of |d| and the extent less |d|, summed over the three axes), a geometry from the two recorded numbers and nothing of the engine's, draws the radius over the frames as a graph, names the radius and the support in the frame's label, says under the board that the click is where the past met the future, the record's own light cone running back after the click, the realised term written at the record's birth and the cone running forward with it, the rest of the board neither read nor written (the frames' arrays are the engine's as they stand, one ring beyond the cone read from the board and asserted equal to the record's reference, the board at its birth, the lay's frame 0 for a record laid at the start) and reads its own count of the cone's Nodes beside the look's, and where the header carries `cone_stepped` (the Node-steps per interval of the cone stepped alone, the box with its ring) says so with the sum, drawing the ball alone and never the box; a frame carrying the board's `tick` (the loop's forward steps, standing at the close while the record is read back and forward) is labelled by its tick and the interval the record is read at; the view fixed, the board seen along one axis and never turned (a folded axis is the one seen along, the board the plane it is; a board of three axes is seen along z one layer at a time, the layer picked beside the board, the first body's layer or the middle one first), the declared board alone in the frame, the layers a receding face grew on the board's own switch, off by default, the frame's label counting the Nodes with a count out there (2026-10-21), the wheel and two buttons bringing it closer or farther; whole quanta as dots sized by the square root of the count (a hole, a count below 0, a hollow dot), resting on the slabs' face where an axis is folded, the wave as the glow of the Node's cube, a field as grey mist, the declared node_detectors' Nodes as rings (the open faces' layer reports but is drawn as no ring), seen at rest and brighter and larger the interval they click; the node_detectors' report as a bar chart with the dashed blind curve behind it, labelled blind, the one measurement; graphs over the intervals beside the board (the total count per family, the count, the form, the field and the tension at a named Node, the pace's minimum, and where the blind names a line or levels (`line_per_interval`, `levels`) the transform of the form at the Node over the frames with the blind's line as a dashed mark and the levels named), every one labelled "lattice reading" as the board is in its corner; the world's files' numbers listed beside frame 0, the world as laid. The family roles come from the file's rows and never from the look: a family that holds nothing is matter, the holder of the sign is light, a holder of the content is a field; a further family that holds nothing is drawn in the same colour, dashed. Every number on the page is the look's (the world's files' and the engine's arrays') or the blind file's; the page computes nothing but the totals its graphs draw, the sums its bars draw and the transform of one Node's form where the blind names a line, and draws no curve, surface or interpolation between Nodes. The blind's numbers stand in a table of their own (every number and short list of the expectation file a row, a nested object's rows named key.subkey, its words under a fold) and never as a raw dump; with an expectation across an axis the NodeDetectors' arrival over the intervals is drawn beside the bars, the reporters' inflow per interval in quanta over the family's wall and the quanta gathered within the window up to each interval, the blind's peak, centroid, span and total marked where the blind names them. With `--output <world>.output.json` (tools/run_inputs.py's file, the run's own output) the page's measurement is the output file's: its `click` lines feed the bars and the arrival, its `credit` lines the clicks credited up to each interval and, where the file carries credit lines at the reporters, the clicks the draw credited per reporter as a second bar beside the shares' (one quantum, one click, where the family's unit rounds every share to 0; 2026-10-21), its `density` lines the lattice density over the reporters' regions, and the header says whether the look's click lines are the output's (they are the same engine lines; a difference is named); with `--reading <reading>.json` (tools/click_counts.py's file, the output file read against the blind) the bars are the reading's rounded shares beside the clicks the draw credited and the blind curve, and one table holds every row the reader compares, read against blind with the difference. The output file's click act is drawn too, the meeting of the future with the past (ENGINE.md section 3, act 6): the hole, the Nodes the `lay` lines write at their interval, marked as wire cubes; the faces the act presents, the `face` lines' Nodes at their interval (the hole's over two intervals, then the front's shells), marked as small cubes, what is erased behind the front seen in the record's own glow and dots going out; the `erasure` lines' distance and the sizes taken per interval as a graph; a record declared a NodeDetector (a body with `credit` lines) ringed at its standing Nodes and flashing at its absorption; and one panel of the records' clicks, the part each record stands in over the intervals from its `credit` lines (before and realised), the fronts' erasure per front (the `erasure` lines' take over the record's unit, in quanta, and the distance, one line per front in its click's tone) and the lines themselves in a table. Every credit line of the output is drawn with its light cone (2026-10-22, the owner's word, "let them show in the experiment's run all the clicks with their cone and everything"): the credit line is the click proper and names no Node, so the Nodes it wrote are read from the `lay` lines contiguous with it at its interval (the absorption's, the emission's and the null window's lays at the body's Nodes, light's quantum laid, the conversion's records out at the front Node) and from the hole's `face` lines at the interval after (the erasure line's origin the check; where two clicks of one family fall at one interval the page gives their lines to the first, the one reading of the lines that can misattribute, named), and the cone at the frame of interval t is the Nodes within t - t_c + 1 Links of them in the Link metric with the wrap, the run back's cone's geometry with one support per click (ALGEBRA.md, The interval's dependency radius is one Link; the pace of light on the board 1 / sqrt 3 Links per interval named in the legend), each click's cone in a tone of the style block's list, the latest click's cone painted last and brightest, with a legend under the board naming each click's kind (the region's credit with the conversion's records out and senses, the absorption, the emission, the own-light click, the null window's no-click), interval, Node, count and credit, the cones' radii over the frames as one graph and a layer switch; a bound body's light front (the look's `shell` and `radius` on its row, the loader's own numbers) as a ring of Nodes in the shell's tone, each ring scaled by the light booked at its shell Node at the frame (the frames' `own_light`, the window's running sum, begun again at the close), the book's sum and the carry graphed in the records' panel and the own light's words of the credit line in its table where the close writes them. The page is dark, one theme and no switch; the moving quanta of light are green; a cube glows by the record's form D at its Node where the look holds it, the wave's own intensity, else by its level. The page's own layout (every colour and size) stands in the one block at the top of the template's style and nowhere else.

The blind file, optional, in one of two formats (a third, the which-way folder's, holds `rows`, the screen's counts per region by world, and `quanta` by world; the page draws its row at the screen reporters and prints its total in words). The expectation `tools/click_counts.py` reads, `{"node_detector": name or a list, "family": name, "window": [first interval, last interval], "across": the axis across the node_detector, "counts": [the blind count per reporter in that order], "pattern": [first, last] (the range of bars), "through": the blind total, "watch": {coordinate on the across axis: the blind number, ...}}`: the chart draws one bar per reporter ordered by its coordinate on that axis, the rounded shares as click_counts.py reads them (what it saw within the window summed from the look's click lines, floored at 0, N the screen's total over the family's wall W_c to the nearest whole, N apportioned by the shares: the expectation, the clicks being the tool's draw), the blind counts as the dashed curve, the pattern's range, the totals line and one watch line per key. Or the node_detectors' totals, `{"expected": {node_detector name: count, ...} or [one count per node_detector in the look's order], "family": the family the curve is of, "window": [first interval, last interval], "watch": {"node_detector": name, "count": the one number to watch}}`, every key optional, one bar per node_detector, what it saw over W_c up to the frame shown.

A gate's reading, optional: with `--gate <reading>.json`, the gate's reader's file (`tools/bell_gate.py`'s or `tools/spin_gate.py`'s output over the gate's worlds, the look's world among them), and the gate's blind as `--blind` (the expectation of the gate's form: `family`, `sides`, `order`, `runs`, `combination`, `blind`), the page adds the gate's panels, inserted at three markers of the template and absent without a reading (a page without one holds none of them): the board seen from above at the frame shown (frame 0 the input as laid, the record's counts at its Nodes and each side's region with its declared setting and pattern as the reader read them; the beams leaving the record and meeting the regions over the intervals; a region brighter the interval it clicks), labelled a lattice reading; the gate's family's `parts` lines per region over the intervals (the parts overlaid, one curve where they are equal) with the region's `click` lines marked, the NodeDetector's read; and the reader's credit beside the blind: the 2^n joint shares as bars, the run filled and the blind outlined, the drawn combination (the click) named, E_n, the marginals, the sub-correlations and the three local credits of the look's world in one table against the blind, the combination over the gate's worlds (its formula from the blind's order and signs, the run's value beside the blind's) on a ruler from minus to plus the number of its terms (the algebraic maximum, one per term) with the fence the blind's theorem lines name ("at most") shaded and the local credits marked on it. `--beside <other>.json` adds one line with another gate's blind combination, read from that file and typed nowhere. `--notes <file.md>` (2026-10-21) embeds a Markdown text and renders it as one prose section in the page's tokens, its first heading the section's, then headings, paragraphs and numbered or bulleted lists: what one sees in the run and why it is like nature, stated beside the look, deciding nothing and computing nothing. Every number of the panels is the reader's file's, the blind's or the look's; the page compares them and sums nothing new.

    python tools/look/page.py <world>.look.json [--blind <world>.blind.json] [--output <world>.output.json] [--reading <reading>.json] [--gate <reading>.json] [--beside <other>.json] [--out <world>.look.html]
"""

from __future__ import annotations

import argparse
import base64
import gzip
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any

MATTER, LIGHT, HELD = "matter", "light", "held"
AXES = ("x", "y", "z")
CDN_THREE = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"


def shown(value: object) -> str:
    """A number as the page prints it: an integer with its thousands separated (a whole float the same), a blind's nested object or list as JSON, any other value as written."""
    if isinstance(value, int) and not isinstance(value, bool):
        return f"{value:,}"
    if isinstance(value, float) and value.is_integer():
        return f"{int(value):,}"
    return json.dumps(value) if isinstance(value, dict | list) else str(value)


def blind_words(value: object) -> str:
    """A blind's total as the totals line prints it: one number as written, an object by its keys in words ("316.5 at the channel, 316.5 at the screen")."""
    if isinstance(value, dict):
        return ", ".join(f"{shown(v)} at the {k}" for k, v in value.items())
    return shown(value)


def bias_words(output: dict[str, Any] | None) -> str:
    """The totals' bias bound as the output's credit lines carry it (`bias_bound`, g and the total; ALGEBRA.md, The digits' base and a total's factors): the worst g / T over the credits, reduced, or nothing where no line carries one."""
    if not isinstance(output, dict) or not isinstance(output.get("lines"), list):
        return ""
    bounds = [
        (int(line["bias_bound"]["g"]), int(line["bias_bound"]["total"]))
        for line in output["lines"]
        if line.get("event") == "credit"
        and isinstance(line.get("bias_bound"), dict)
        and line["bias_bound"].get("g")
        and line["bias_bound"].get("total")
    ]
    if not bounds:
        return ""
    g, total = max(bounds, key=lambda pair: Fraction(pair[0], pair[1]))
    worst = Fraction(g, total)
    return f"; the bias bound {worst.numerator} / {worst.denominator} on the click's line, the worst over the {len(bounds)} credits carrying one (g {g:,} against T {total:,})"


Reporter = tuple[int, str]  # its coordinate on the axis (the least of its Nodes'), its node_detector


def inflows(
    look: dict[str, Any], node_detectors: list[str], family: str, window: tuple[int, int]
) -> dict[str, int]:
    """What each named node_detector saw of one family within the window [first, last] of intervals, its click lines' net front inflows summed from the look's frames' lines as tools/click_counts.py sums them (a click reports its region and never a Node)."""
    found, seen = {name: 0 for name in node_detectors}, set()
    for frame in look["frames"]:
        for line in frame["lines"]:
            if line.get("event") != "click" or line.get("node_detector") not in found:
                continue
            if line.get("family") != family or not window[0] <= int(line["interval"]) <= window[1]:
                continue
            key = (int(line["interval"]), str(line["node_detector"]), int(line["inflow"]))
            if "pass" in frame and key in seen:
                continue  # a run forward again reports the same click line at the same interval: one click, counted once
            seen.add(key)
            found[str(line["node_detector"])] += int(line["inflow"])
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


def credited(
    output: dict[str, Any] | None, labels: list[str], family: str, window: tuple[int, int]
) -> list[int] | None:
    """The clicks the draw credited per reporter within the window, in the record's own unit: the run's output file's credit lines at the reporters, their `count` summed (the engine's division act N = (SUM s + W_rec div 2) div W_rec in the record's own unit W_rec and its draw among the regions, ALGEBRA.md R101 and B2; a record's own credit lines, `body n`, are no reporter's); None without an output file or where no credit line of the family stands at a reporter within the window (no draw declared: the clicks are in no unit)."""
    if not isinstance(output, dict) or not isinstance(output.get("lines"), list):
        return None
    found, seen = dict.fromkeys(labels, 0), False
    for line in output["lines"]:
        if line.get("event") != "credit" or line.get("node_detector") not in found:
            continue
        if line.get("family") != family or not window[0] <= int(line["interval"]) <= window[1]:
            continue
        found[str(line["node_detector"])] += int(line.get("count") or 0)
        seen = True
    return [found[label] for label in labels] if seen else None


def reporters(node_detectors: list[dict[str, Any]], axis: int) -> list[Reporter]:
    """The reporters across `axis` as tools/click_counts.py places them, one per node_detector, ordered by their coordinate on it, the least of the node_detector's Nodes' (a region across the beam at its first row)."""
    return sorted((min(int(node[axis]) for node in d["nodes"]), str(d["name"])) for d in node_detectors)


def last_interval(look: dict[str, Any]) -> int:
    """The last interval the look holds, the largest of its frames' own (a strided look, tools/look/record.py --every K, keeps frame 0, every K-th interval's frame and the last, so a frame's position is not its interval; a look of several passes runs back and forward again, so its last frame's interval is not its largest; on a full look of one pass the last frame's interval, the frames' count less one)."""
    frames = look["frames"]
    return max(int(frame["interval"]) for frame in frames) if frames else 0


def passes(look: dict[str, Any]) -> int:
    """The passes of a look: 1 for a look without the `pass` key on its frames (every shipped look), else the largest `pass` written (3 for the click that runs back: the run to the first close, the run back to the birth, the run forward to the partner's close)."""
    return max(int(frame.get("pass", 1)) for frame in look["frames"]) if look["frames"] else 1


def measurement(
    look: dict[str, Any], blind: dict[str, Any] | None, output: dict[str, Any] | None = None
) -> dict[str, Any] | None:
    """The one measurement from an expectation in tools/click_counts.py's format (`node_detector`, one name or a list, or none for every declared region but the faces' layer, `family`, `window`, or none for the whole look, `across`, `counts`), None from any other: the reporters ordered by their coordinate on the across axis (`reporters`), what each one saw within the window, floored at 0, N over the family's wall to the nearest whole and the rounded shares (`apportioned`, as the tool reads them), the blind counts, the pattern's range, the totals line and the watch lines, each key of `watch` named as the coordinate on the across axis; the page draws these and computes nothing more. With the run's output file carrying credit lines at the reporters (2026-10-21), the bars stand in the record's own unit, the unit a credit stands in: `clicks`, the clicks the draw credited within the window (the engine's N in W_rec, `credited`), apportioned by the same shares as `record_shares`, the expectation in that unit, with `credited` per reporter, where the draw fell; the totals line names both units, and the watch lines read the bars drawn (one quantum's click no longer reads 0 where the family's unit W_c rounds every share to 0)."""
    if blind is None or "across" not in blind:
        return None
    if blind["across"] not in AXES:
        raise ValueError(f"the blind file's across is one of {list(AXES)}, got {blind['across']!r}")
    axis = AXES.index(blind["across"])
    named = blind.get("node_detector")
    if named is None:  # every declared region, over the whole look (the faces' layer is drawn, not read)
        node_detectors = [d for d in look["node_detectors"] if d["body"] is None and d["name"] != "face"]
        names = [str(d["name"]) for d in node_detectors]
    else:
        names = [str(name) for name in named] if isinstance(named, list) else [str(named)]
        node_detectors = [d for d in look["node_detectors"] if d["name"] in names]
    if len(node_detectors) != len(names):
        raise ValueError(f"the blind file's node_detectors {names} are not all in the look")
    spanned = blind.get("window", [0, last_interval(look)])
    window = (int(spanned[0]), int(spanned[1]))
    saw = inflows(look, names, str(blind["family"]), window)
    placed = reporters(node_detectors, axis)
    seen = [saw[node_detector] for _at, node_detector in placed]
    wall = next(int(f["wall"]) for f in look["families"] if f["name"] == blind["family"])
    shares = [max(value, 0) for value in seen]  # the credit's floor, the NodeDetector's declaration
    quanta = (sum(shares) + wall // 2) // wall
    rounded = apportioned(quanta, shares)
    watch: dict[str, Any] = blind["watch"] if isinstance(blind.get("watch"), dict) else {}
    stem = str(look.get("world", "")).rsplit(".", 1)[0]
    labels = [name for _at, name in placed]
    if isinstance(blind.get("counts"), list):
        per_bar: list[Any] = list(blind["counts"])
    elif isinstance(blind.get("rows"), dict) and isinstance(
        blind["rows"].get(stem), list
    ):  # the which-way folder's blind: the screen's counts per region by world, none at a channel
        row = blind["rows"][stem]
        per_bar = [
            row[k] if k < len(row) and str(label).startswith("screen") else None
            for k, label in enumerate(labels)
        ]
    else:
        per_bar = []
    total_blind = blind.get("quanta", blind.get("through"))
    if isinstance(total_blind, dict) and stem in total_blind:
        total_blind = total_blind[stem]
    clicks = credited(output, labels, str(blind["family"]), window)
    record_shares = apportioned(sum(clicks), shares) if clicks is not None else None
    bars = rounded if record_shares is None else record_shares
    lines = [
        f"{blind['across']} = {key}: {shown(sum(c for (at, _n), c in zip(placed, bars, strict=True) if at == int(key)))} by the shares, the blind {shown(value)}"
        for key, value in watch.items()
    ]
    totals = (
        f"N {shown(quanta)} by the shares (the blind {blind_words(total_blind)}){bias_words(output)}"
        if clicks is None
        else f"N {shown(sum(clicks))} by the shares in the record's own unit, the clicks the draw credited within the window apportioned by the shares of the click lines (the blind {blind_words(total_blind)}); N {shown(quanta)} over the family's wall W_c in T's unit{bias_words(output)}"
    )
    return {
        "node_detector": named if named is not None else names,
        "family": blind["family"],
        "window": list(window),
        "across": blind["across"],
        "axis": axis,
        "at": [at for at, _name in placed],
        "labels": labels,
        "seen": seen,
        "quanta": quanta,
        "rounded_shares": rounded,
        "credited": clicks,
        "clicks": None if clicks is None else sum(clicks),
        "record_shares": record_shares,
        "blind": per_bar,
        "pattern": blind.get("pattern"),
        "totals": totals,
        "watch": lines,
        "recorded": last_interval(look),
    }


def roles(families: list[dict[str, Any]]) -> dict[str, dict[str, object]]:
    """The family roles from the file's rows: a family of quanta with a gap (den above |num|) is matter, a massless family of quanta (num = den, light's own pair) and the holder of the sign are light, a holder of the content is a field; every further family of matter is drawn dashed."""
    found: dict[str, dict[str, object]] = {}
    seen = False
    for family in families:
        pair = family.get("pair") or [0, 1]
        massless = family.get("quanta", not family.get("held")) and pair[0] == pair[1]
        role = LIGHT if family.get("sign") or massless else HELD if family.get("held") else MATTER
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


OUTPUT_LINES = (
    "click",
    "credit",
    "density",
    "lay",
    "face",
    "erasure",
    "conversion",
)  # the output file's lines the page draws


def trimmed(output: dict[str, Any]) -> dict[str, Any]:
    """The run's output file as the page embeds it: its verdict, intervals, end and books, and its click, credit and density lines alone, untouched; refused by name where it is not a run's output."""
    if not isinstance(output, dict) or not isinstance(output.get("lines"), list):
        raise ValueError("the output file must be tools/run_inputs.py's, with its lines")
    kept = {key: output.get(key) for key in ("input", "verdict", "intervals", "ended", "books")}
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
    notes: str | None = None,
) -> str:
    """The page's HTML from the look and the blind expectation, if any; with a gate's reading, the gate's panels inserted at the template's three markers (`other` the line of another gate's blind); with the run's output file and tools/click_counts.py's reading of it, the measurement from them; with `notes`, a Markdown text (`--notes`, 2026-10-21), its headings, paragraphs and lists rendered by the page as one prose section in the page's own tokens, what one sees and why it is like nature, stated beside the look and deciding nothing."""
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
        .replace("{{MEASURE}}", embedded(measurement(look, blind, output)))
        .replace("{{OUTPUT}}", embedded(trimmed(output) if output is not None else None))
        .replace("{{READ}}", embedded(checked_reading(read) if read is not None else None))
        .replace("{{GATE}}", embedded(gated))
        .replace("{{BESIDE}}", embedded(other))
        .replace("{{NOTES}}", embedded(notes))
    )


BLOCKS = (
    "look",
    "roles",
    "blind",
    "measurement",
    "output",
    "reading",
    "gate",
    "beside",
    "notes",
)  # the page's embedded blocks, by their script ids (`notes` the Markdown text of `--notes`, a string)
BLOCK = re.compile(r'<script id="([a-z]+)" type="application/[a-z0-9+]+">(.*?)</script>', re.S)


def recorded(html: str) -> dict[str, Any]:
    """A recorded page's embedded data read back (2026-10-21): the look inflated from its gzip+base64 block, the other blocks' JSON by their ids (None where the page holds no such block: a gate's two stand on a gate's page alone); refused by name where the page holds no look."""
    blocks = dict(BLOCK.findall(html))
    if "look" not in blocks:
        raise ValueError("the page holds no embedded look (tools/look/page.py's block `look`)")
    look = json.loads(gzip.decompress(base64.b64decode(blocks["look"])))
    return {
        "look": look,
        **{key: json.loads(blocks[key]) if key in blocks else None for key in BLOCKS[1:]},
    }


def retemplated(html: str) -> str:
    """A recorded page written again from its own embedded data with the current template and nothing else changed (`--retemplate`, 2026-10-21): the look, the blind, the output file's lines, tools/click_counts.py's reading, a gate's reading and the other gate's blind as the page recorded them, the measurement computed from them again as at the first build; the way a template fix reaches every shipped page without the engine run again, the frames and every number theirs byte for byte."""
    data = recorded(html)
    gated = data["gate"]
    return page(
        data["look"],
        data["blind"],
        gated["reading"] if isinstance(gated, dict) else None,
        data["beside"],
        output=data["output"],
        read=data["reading"],
        notes=data["notes"] if isinstance(data["notes"], str) else None,
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "look",
        type=Path,
        help="the look file (<world>.look.json); with --retemplate, a recorded page (<world>.html)",
    )
    parser.add_argument(
        "--retemplate",
        action="store_true",
        help="read the page's embedded data and write the page again with the current template",
    )
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
    parser.add_argument(
        "--notes",
        type=Path,
        default=None,
        help="a Markdown file rendered as one prose section: what one sees and why it is like nature",
    )
    parser.add_argument("--out", type=Path, default=None, help="the page (<world>.look.html)")
    args = parser.parse_args(argv)
    if args.retemplate:
        target: Path = args.out or args.look
        target.write_text(retemplated(args.look.read_text(encoding="utf-8")), encoding="utf-8")
        print(json.dumps({"page": str(target), "bytes": target.stat().st_size, "retemplated": True}))
        return
    look = json.loads(args.look.read_text(encoding="utf-8"))
    blind = json.loads(args.blind.read_text(encoding="utf-8")) if args.blind else None
    reading = json.loads(args.gate.read_text(encoding="utf-8")) if args.gate else None
    target = args.out or args.look.with_suffix(".html")
    target.write_text(
        page(
            look,
            blind,
            reading,
            beside(args.beside) if args.beside else None,
            output=json.loads(args.output.read_text(encoding="utf-8")) if args.output else None,
            read=json.loads(args.reading.read_text(encoding="utf-8")) if args.reading else None,
            notes=args.notes.read_text(encoding="utf-8") if args.notes else None,
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
  --flash: #ff5a1f; --blind: #b4b8c0; --focus: #5f97ea; --window: rgba(95, 151, 234, 0.2); --hole: #ffffff; --front: #c084fc;
  --forward: #4ade80; --back: #f59e0b; --bound: #9a9ea8; --cone: #f59e0b; --cone-tint: 0.62; --cone-above: 0.3;
  --click-tones: #f472b6, #22d3ee, #a3e635, #fb923c, #c084fc, #facc15, #38bdf8, #f87171; --click-tint: 0.6; --click-fade: 0.55; --shell: #fde68a; --shell-scale: 0.6;
  --font-body: "IBM Plex Sans", system-ui, sans-serif; --font-mono: "IBM Plex Mono", ui-monospace, monospace;
  --text: 14px; --small: 12px; --title: 20px; --gap: 12px; --pad: 14px; --radius: 6px; --gutter: 16px;
  --sky: #ffffff; --ground: #5a5a5a; --sun: 0.3;
  --side-min: 300px; --board-height: min(76vh, 900px); --graph-width: 360; --graph-height: 84; --graph-pad: 6;
  --bar-slot: 12; --measure-width: 960px; --blind-words: 100; --blind-list: 48; --blind-rows: 24; --arrival-width: 2.6; --arrival-height: 1.6;
  --cube-size: 0.92; --cube-depth: 0.2; --dot-radius: 0.5; --dot-floor: 0.12; --dot-least: 3; --dot-offset: 0.22; --glow: 1; --glow-power: 0.5; --glow-tint: 0;
  --mist-size: 1.02; --mist-opacity: 0.3; --mist-power: 0.5; --bar-length: 0.9; --bar-thickness: 0.07;
  --wall-size: 1; --wall-depth: 0.6; --ring-radius: 0.6; --ring-tube: 0.09; --flash-scale: 1.2; --plane-opacity: 0.12; --hole-size: 1.08; --front-size: 0.5;
  --view-margin: 1; --node-least: 6; --node-fit-least: 3; --node-most: 24; --board-least: 180; --board-most: 900; --camera-far: 4; --zoom-rate: 0.0012; --zoom-step: 0.85; --zoom-most: 8; --frames-per-second: 12; --line-width: 1.6;
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
.time { display: grid; grid-template-columns: auto minmax(12rem, 1fr) minmax(0, auto); align-items: center; gap: var(--gap); margin-top: var(--gap); }  /* the track keeps 12rem at least; the frame's status wraps beside it, never wider than the row leaves it (2026-10-21) */
@media (max-width: 600px) { .time { grid-template-columns: auto minmax(0, 1fr); } .frame { grid-column: 1 / -1; max-width: none; text-align: left; } }  /* at the phone width the frame's status on its own row under the track */
.track { position: relative; min-width: 0; }
.track input { width: 100%; margin: 0; position: relative; z-index: 1; }
.track .window { position: absolute; top: 25%; height: 50%; background: var(--window); border-radius: var(--radius); }
.track .bounds span { position: absolute; top: 10%; height: 80%; width: 0; border-left: 2px dashed var(--bound); }
.frame svg { width: 1em; height: 1em; vertical-align: -0.15em; margin-left: 6px; }
.frame { font-family: var(--font-mono); font-variant-numeric: tabular-nums; min-width: 9ch; max-width: 52ch; text-align: right; }
.lines { font: var(--small)/1.4 var(--font-mono); color: var(--muted); margin-top: 6px; min-height: 1.4em; }
.cone { font: var(--small)/1.4 var(--font-mono); color: var(--muted); margin-top: 4px; }
.cone:empty { display: none; }
.cone b { color: var(--cone); font-weight: 600; }
.clicks { display: grid; grid-template-columns: minmax(0, 1fr); gap: 4px; margin-top: var(--gap); font-size: var(--small); }  /* the clicks' legend under the board: one row per click line of the output with the swatch of its cone's tone (2026-10-22) */
.clicks:empty { display: none; }
.clicks .row { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 8px; overflow-wrap: anywhere; }
.clicks .row b { font-weight: 600; }
.clicks .row .now { color: var(--muted); font-family: var(--font-mono); }
.clicks .heading { color: var(--muted); }
button, select, input[type=number] { font: inherit; color: var(--fg); background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 4px 10px; }
button:focus-visible, select:focus-visible, input:focus-visible { outline: 2px solid var(--focus); outline-offset: 1px; }
.stack { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--gap); }
.graph { display: grid; grid-template-columns: minmax(0, 1fr); gap: 2px; min-width: 0; }  /* a graph's column never wider than its panel: a long caption wraps and the chart scales to the panel, no overflow at the phone width (2026-10-21) */
.graph .caption { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px var(--gap); font-size: var(--small); color: var(--muted); overflow-wrap: anywhere; }
.graph .caption b { color: var(--fg); font-weight: 600; }
.graph svg { width: 100%; height: auto; display: block; }
.legend { display: flex; flex-wrap: wrap; gap: 4px var(--gap); font-size: var(--small); }
.prose { max-width: 90ch; }  /* the notes: one prose section in the page's tokens (--notes, 2026-10-21) */
.prose p, .prose ol, .prose ul { margin: 0 0 var(--gap); }
.prose ol, .prose ul { padding-left: 1.6em; }
.prose li { margin-bottom: 6px; }
.prose h3 { font-size: var(--text); font-weight: 600; margin: var(--gap) 0 6px; }
.prose h4 { font-size: var(--small); font-weight: 600; color: var(--muted); margin: var(--gap) 0 4px; }
.prose code { font-family: var(--font-mono); font-size: var(--small); }
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
.measure svg, #arrival svg { width: 100%; max-width: min(var(--measure-width), 100%); }  /* the chart bound by its panel and so by the viewport, --measure-width its widest (2026-10-21) */
.totals, .watch { font-family: var(--font-mono); font-size: var(--small); margin-top: 6px; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
<script id="look" type="application/gzip+base64">{{LOOK}}</script>
<script id="roles" type="application/json">{{ROLES}}</script>
<script id="blind" type="application/json">{{BLIND}}</script>
<script id="measurement" type="application/json">{{MEASURE}}</script>
<script id="output" type="application/json">{{OUTPUT}}</script>
<script id="reading" type="application/json">{{READ}}</script>
<script id="notes" type="application/json">{{NOTES}}</script>
<header>
  <h1 id="title"></h1>
  <span class="verdict" id="verdict"></span>
  <span class="verdict" id="source"></span>
</header>
<div class="page">
  <section class="panel wide">
    <div class="stage" id="stage">
      <canvas id="board"></canvas>
      <div class="corner">lattice reading</div>
      <div class="zoom"><button type="button" id="zoom-in" aria-label="closer">+</button><button type="button" id="zoom-out" aria-label="farther">&minus;</button></div>
      <div class="hover" id="hover"></div>
    </div>
    <div class="layers" id="layers"></div>
    <div class="picker" id="view-picker"></div>
    <div class="time">
      <button type="button" id="play">Play</button>
      <div class="track"><div class="window" id="window" hidden></div><div class="bounds" id="bounds"></div><input type="range" id="slider" min="0" value="0" step="1" aria-label="the interval"></div>
      <div class="frame"><span id="frame"></span><span id="direction"></span></div>
    </div>
    <div class="lines" id="lines"></div>
    <div class="cone" id="cone"></div>
    <div class="clicks" id="clicks"></div>
  </section>{{GATE_PANELS}}
  <section class="panel measure" id="measure-box">
    <h2>Measurement: the node_detectors' report</h2>
    <div class="picker" id="measure-picker"></div>
    <div class="graph" id="measure"></div>
    <div class="totals" id="totals"></div>
    <div class="watch" id="watch"></div>
  </section>
  <section class="panel wide" id="arrival-box" hidden>
    <h2>The arrival at the NodeDetectors over the intervals</h2>
    <div class="stack" id="arrival"></div>
  </section>
  <section class="panel wide" id="records-box" hidden>
    <h2>The records' clicks: the meeting written on the lattice</h2>
    <div class="stack" id="records"></div>
    <div class="scroll" id="credits"></div>
  </section>
  <section class="panel wide" id="notes-box" hidden>
    <h2 id="notes-heading">Notes</h2>
    <div class="prose" id="notes"></div>
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
const NOTES = JSON.parse(document.getElementById('notes').textContent);  // the Markdown text of --notes, or null
const root = document.documentElement;
const token = name => getComputedStyle(root).getPropertyValue(name).trim();
const size = name => parseFloat(token(name));
const byId = id => document.getElementById(id);
/* The frames' shapes: a board with a receding face grows, so the page's box is the union of the frames' shapes at the file's coordinates (a frame's origin is minus its offset, the layers grown before the origin); an older look without them has the world's shape. */
const shapeOf = fr => fr.shape || LOOK.shape, originOf = fr => (fr.offset || [0, 0, 0]).map(o => -o);
const LOW = [0, 1, 2].map(a => Math.min(...LOOK.frames.map(fr => originOf(fr)[a])));
const HIGH = [0, 1, 2].map(a => Math.max(...LOOK.frames.map(fr => originOf(fr)[a] + shapeOf(fr)[a])));
const [X, Y, Z] = HIGH.map((h, a) => h - LOW[a]), N = X * Y * Z, T = LOOK.frames.length - 1;
/* A strided look (tools/look/record.py --every K) keeps frame 0, every K-th interval's frame and the last, so a frame's position on the slider is not its interval: every sum "up to the frame shown", every mark at an interval and the window's marker read the frame's own interval, INTERVAL(k), and place an interval at the position of the frame holding it or the first after it, positionOf(interval), the full look's rule (one position per interval) beyond the last frame; on a full look both are the identity. */
const INTERVAL = k => Number(LOOK.frames[k].interval), LAST = Math.max(...LOOK.frames.map((_, k) => INTERVAL(k)));
/* The passes (a look recorded from the lattice's observers on a world of a record read at declared sides: every frame carries its `pass`, 1 the run to the first close, 2 the run back to the record's birth with its intervals decreasing, 3 the run forward to the partner's close, and its `direction`, +1 or -1): the slider runs over the frames in the look's order, every label reads the frame's own interval with its pass, every sum "up to the frame shown" counts the lines of the frames up to it (a click line belongs to the pass it was written in), and a mark at an interval stands at the frame holding it in its pass, or the first after it in the pass's direction; a look of one pass (no `pass` key) reads PASS 1 and DIRECTION +1 everywhere and renders as before. */
const PASS = k => Number(LOOK.frames[k].pass || 1), DIRECTION = k => Number(LOOK.frames[k].direction || 1);
const PASSES = Math.max(1, ...LOOK.frames.map((_, k) => PASS(k))), BOUNDS = LOOK.frames.map((_, k) => k).filter(k => k > 0 && PASS(k) !== PASS(k - 1));
const positionOf = (interval, pass = 1) => { let last = -1; for (let k = 0; k <= T; k++) { if (PASS(k) !== pass) continue; if (DIRECTION(k) > 0 ? INTERVAL(k) >= interval : INTERVAL(k) <= interval) return k; last = k; } return last < 0 ? (pass === 1 ? T + Math.max(0, interval - LAST) : positionOf(interval, 1)) : last + Math.abs(interval - INTERVAL(last)); };
const passLabel = k => 'pass ' + PASS(k) + ' of ' + PASSES + (DIRECTION(k) < 0 ? ', back' : ', forward');
/* The board's tick (the loop's forward steps, `tick` on a frame of a look of several passes): it stands at the close while the record is read back and forward, so a frame of the run back is labelled by the tick and by the interval the record is read at; a frame without the key is labelled by its interval as before. */
const TICK = k => LOOK.frames[k].tick === undefined || LOOK.frames[k].tick === null ? null : Number(LOOK.frames[k].tick);
const LAST_TICK = Math.max(LAST, ...LOOK.frames.map((_, k) => TICK(k) === null ? LAST : TICK(k)));
/* The run back's reach (ALGEBRA.md, The meeting's reading, the run back's reach): a look whose header carries `reach` cone has the cone's support, `cone_support` (the birth's Nodes at the file's coordinates, the lay's for a record laid at the start), the cone's Nodes per interval, `cone_volume`, and on every frame of the run back and forward `cone_radius`, t + 1 at the frame's interval t; the page shades the Nodes within that many Links of the support in the Link metric with the wrap as the engine's front counts its shells (per axis |d|, on a periodic axis the lesser of |d| and the extent less |d|, summed over the three axes; features/front.shell), a geometry from the two recorded numbers and nothing of the engine's. The frames' arrays are the engine's as they stand: outside the cone neither read nor written, one ring beyond it read from the board and asserted equal to the record's reference, the board at its birth (the lay's frame 0 for a record laid at the start), by the engine at every step back and forward; at the birth frame of a run back the realised port's coefficients are written into the record's parts (the frame's lay lines), the run forward carrying the realised term. The page's count of the cone's Nodes within the frame's own box stands beside the look's `cone_volume` at the frame's interval. A look without the words draws no cone. */
const REACH = typeof LOOK.reach === 'string' ? LOOK.reach : null, SUPPORT = Array.isArray(LOOK.cone_support) ? LOOK.cone_support : [], VOLUME = Array.isArray(LOOK.cone_volume) ? LOOK.cone_volume : null;
const STEPPED = Array.isArray(LOOK.cone_stepped) ? LOOK.cone_stepped : null;  // the Node-steps per interval of the cone stepped alone (the box with its ring), the header's; the page draws the ball alone and never the box
const CONE_RADIUS = k => LOOK.frames[k].cone_radius === undefined || LOOK.frames[k].cone_radius === null ? null : Number(LOOK.frames[k].cone_radius);
const CONED = SUPPORT.length > 0 && LOOK.frames.some((_, k) => CONE_RADIUS(k) !== null);
const supportSpan = () => CONED ? ' (' + [0, 1, 2].filter(a => LOOK.shape[a] > 1).map(a => AXES[a] + ' ' + format(Math.min(...SUPPORT.map(n => n[a]))) + ' to ' + format(Math.max(...SUPPORT.map(n => n[a])))).join(', ') + ')' : '';  // the support's extent along the unfolded axes, from the header's Nodes
const linkDistanceTo = (support, node) => { let least = Infinity; for (const at of support) { let d = 0; for (let a = 0; a < 3; a++) { let along = Math.abs(node[a] - at[a]); if (LOOK.boundary[AXES[a]] === 'periodic') along = Math.min(along, LOOK.shape[a] - along); d += along; } if (d < least) least = d; } return least; };  // the least Link distance to a support of Nodes, the front's metric with the wrap; a periodic axis never grows, so its extent is the file's
const linkDistance = node => linkDistanceTo(SUPPORT, node);  // to the run back's cone's support
const inBox = (node, fr) => { const o = originOf(fr), s = shapeOf(fr); return node.every((c, a) => c >= o[a] && c < o[a] + s[a]); };  // within the frame's own box
const inCone = (i, k) => { const radius = CONE_RADIUS(k); return radius !== null && DISTANCE[i] <= radius && inBox(nodeOf(i), LOOK.frames[k]); };
/* The view is fixed: the board is seen along one axis, VIEW, and never turned; a folded axis is the one seen along (the board the plane it is), a board of three axes is seen along z one layer at a time, LAYER. The eye stands on the side of the axis from which its two other axes read right and up (ACROSS), and the declared board (the file's own Nodes, from the origin) alone is in the frame. */
const VIEW = LOOK.folded.indexOf(true) >= 0 ? LOOK.folded.indexOf(true) : 2, SIDE = VIEW === 2 ? 1 : -1;
const ACROSS = [0, 1, 2].filter(a => a !== VIEW);
const CENTRE = LOOK.shape.map((e, a) => (e - 1) / 2 - LOW[a] - ([X, Y, Z][a] - 1) / 2);
let LAYER = LOOK.folded[VIEW] ? 0 : LOOK.bodies.length && LOOK.bodies[0].nodes.length ? LOOK.bodies[0].nodes[0][VIEW] : Math.floor(LOOK.shape[VIEW] / 2);
const FAMILIES = LOOK.families, QUANTA = FAMILIES.filter(f => f.quanta), HELD = FAMILIES.filter(f => !f.quanta);
const AXES = ['x', 'y', 'z'], PARTS = ['x', 'y', 'z', 'xx', 'yy', 'zz', 'xy', 'xz', 'yz'];
const colourOf = name => token('--' + ROLES[name].role);
const esc = text => String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
const format = value => typeof value === 'number' ? (value === 0 ? 0 : value).toLocaleString('en-US') : String(value);  // -0 printed as 0
const ordinal = n => { const tens = n % 100, ones = n % 10; return format(n) + (tens >= 11 && tens <= 13 ? 'th' : ones === 1 ? 'st' : ones === 2 ? 'nd' : ones === 3 ? 'rd' : 'th'); };  // 1st, 2nd, 3rd, 11th, 12th, 13th, 21st
const nodesWord = n => format(n) + (n === 1 ? ' Node' : ' Nodes'), linksWord = n => format(n) + (n === 1 ? ' Link' : ' Links');

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
/* The declared board alone is in the frame; the layers a receding face grew stand on the board's own switch, off by default (2026-10-21: a record that has left the declared board, the GHZ close, is otherwise an emptied board), the frame's label counting the Nodes with a count out there. */
const GROWN = { on: false, objects: [] }, GROWS = N > LOOK.shape[0] * LOOK.shape[1] * LOOK.shape[2];
const declared = n => n.every((c, a) => c >= 0 && c < LOOK.shape[a]);
const inside = i => { const n = nodeOf(i); return (GROWN.on || declared(n)) && (LOOK.folded[VIEW] || n[VIEW] === LAYER); };  // the declared board (the grown layers with it where switched on), the layer seen
const cache = new Map();
function frameOf(t) {
  if (cache.has(t)) return cache.get(t);
  const frame = LOOK.frames[t], out = {};
  for (const f of FAMILIES) {
    const row = frame.families[f.name] || {}, a = {};
    if (f.quanta) { for (const key of ['now', 'second', 'count', 'form']) if (row[key] !== undefined) a[key] = arrayOf(row[key], frame); a.pace = row.pace; a.share = row.share; a.peakForm = a.form ? peak(a.form) : 0; a.peakNow = Math.max(peak(a.now), a.second ? peak(a.second) : 0); }
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
    if (f.quanta) { m.now = Math.max(m.now, peak(a.now), a.second ? peak(a.second) : 0); m.count = Math.max(m.count, peak(a.count)); m.form = Math.max(m.form, a.form ? peak(a.form) : 0); TOTALS[f.name][t] = a.share == null ? sum(a.count) : a.share / f.wall; }
    else { m.level = Math.max(m.level, peak(a.level)); for (const p of a.parts) m.part = Math.max(m.part, peak(p)); }
  }
}
const indexOf = (x, y, z) => ((x - LOW[0]) * Y + (y - LOW[1])) * Z + (z - LOW[2]);
const nodeOf = i => [Math.floor(i / (Y * Z)) + LOW[0], Math.floor(i / Z) % Y + LOW[1], i % Z + LOW[2]];
const DISTANCE = CONED ? Float64Array.from({ length: N }, (_, i) => linkDistance(nodeOf(i))) : null;  // every Node's Link distance to the cone's support, once
const coneCount = k => { if (!CONED || CONE_RADIUS(k) === null) return null; let n = 0; for (let i = 0; i < N; i++) if (inCone(i, k)) n++; return n; };
const coneLabel = k => CONE_RADIUS(k) === null ? '' : ', cone ' + linksWord(CONE_RADIUS(k)) + ' about the birth\\'s ' + nodesWord(SUPPORT.length) + supportSpan();
/* The interval from which the cone holds a box whole: the largest Link distance of the box's Nodes from the support, less one (G(t) holds the Nodes within t + 1 Links); the declared board's box and the last frame's, the board as grown. */
const filledFrom = fr => { if (!CONED) return null; let far = 0; for (let i = 0; i < N; i++) if (inBox(nodeOf(i), fr) && DISTANCE[i] > far) far = DISTANCE[i]; return far - 1; };
const DECLARED_BOX = { shape: LOOK.shape, offset: [0, 0, 0] }, FILLED = CONED ? { declared: filledFrom(DECLARED_BOX), grown: filledFrom(LOOK.frames[T]) } : null;
/* The click lines the measurement is drawn from: the output file's where it is given (the run's own output), the look's otherwise; the two are the same engine lines, and the header says so or names the difference. The output file's credit lines (the clicks the draw credited) and density lines (a lattice reading per declared region) beside them. */
const LOOK_CLICKS = [], reportsAt = {}, CREDITS_AT = {}, DENSITY_AT = {};
for (const frame of LOOK.frames) for (const line of frame.lines) if (line.event === 'click') LOOK_CLICKS.push(line);
/* Every line's position, the frame it belongs to: a look line's the frame holding it; an output line's by the look's order (the output's lines and the look's are the same engine lines in the same order): a click, parts, credit or lay line takes the position of its twin in the look, the next of the look's lines with its interval, region, family and inflow (a lay line's twin by its content too: its line, Node and levels, so that the write's lines at the birth and a source's lines at the same interval are told apart), and a line with no twin is placed from the cursor, the frame of the line before it in the output: within the cursor's pass where its interval lies at or ahead of the line before it in the pass's direction, at the frame of its interval or the next frame kept in the pass (the lines of an interval between the kept frames shown at the next frame kept), else (an interval behind the line before it, a line of a later pass) at the first frame from the cursor whose interval is its own, else at the next frame kept of the following pass, else at the position the full look's rule gives its interval in the cursor's pass; on a look of one pass every position is the frame holding the line's interval, or the first after it. */
const POSITIONS = new Map(), TWINS = new Map(), keyOf = line => [line.event, line.interval, line.node_detector, line.family, line.inflow].concat(line.event === 'lay' ? [line.line, JSON.stringify(line.node && line.node.at), JSON.stringify(line.before), JSON.stringify(line.after)] : []).join('|');
const placed = (interval, cursor, last) => {
  const c = Math.min(cursor, T), within = (from, pass) => { const d = DIRECTION(from); for (let k = from; k <= T && PASS(k) === pass; k++) if (d * (INTERVAL(k) - interval) >= 0) return k; return null; };
  if (DIRECTION(c) * (interval - last) >= 0) { const k = within(c, PASS(c)); if (k !== null) return k; }
  let k = c; while (k <= T && INTERVAL(k) !== interval) k++;
  if (k <= T) return k;
  let next = c; while (next <= T && PASS(next) === PASS(c)) next++;
  if (next <= T) { const k2 = within(next, PASS(next)); if (k2 !== null) return k2; }
  return positionOf(interval, PASS(c));
};
LOOK.frames.forEach((frame, k) => frame.lines.forEach(line => { POSITIONS.set(line, k); const key = keyOf(line); if (!TWINS.has(key)) TWINS.set(key, []); TWINS.get(key).push(k); }));
if (OUTPUT) { let cursor = 0, last = 0; for (const line of OUTPUT.lines) { const twins = TWINS.get(keyOf(line)); const k = twins && twins.length ? twins.shift() : placed(Number(line.interval), cursor, last); POSITIONS.set(line, k); cursor = Math.max(cursor, Math.min(k, T)); last = Number(line.interval); } }
const positionOfLine = line => POSITIONS.get(line);
const CLICKS = OUTPUT ? OUTPUT.lines.filter(line => line.event === 'click') : LOOK_CLICKS;
for (const line of CLICKS) {
  const byFamily = reportsAt[line.node_detector] || (reportsAt[line.node_detector] = {});
  (byFamily[line.family] || (byFamily[line.family] = [])).push([line.interval, line.inflow, positionOfLine(line)]);
}
if (OUTPUT) for (const line of OUTPUT.lines) {
  if (line.event === 'credit') (CREDITS_AT[line.node_detector] || (CREDITS_AT[line.node_detector] = [])).push([line.interval, line.count || 0, positionOfLine(line)]);
  if (line.event === 'density') ((DENSITY_AT[line.family] || (DENSITY_AT[line.family] = {}))[line.node_detector] || (DENSITY_AT[line.family][line.node_detector] = [])).push([line.interval, line.reading, positionOfLine(line)]);
}
/* The click act's lines from the output file: the hole (the lay lines' Nodes per interval), the faces presented (the face lines' Nodes per interval: the hole's faces, then the front's shells), the front's erasure lines (the origin, the distance and the sizes taken per interval) and the records' credits (a record declared a NodeDetector, `body n`), the meeting of the future with the past drawn where the engine wrote it. */
/* The write at the birth (ALGEBRA.md, The meeting's reading: the realised port's integer coefficients, reduced by their greatest common divisor over the record's surviving parts, scaled into the record's parts at its birth; a scaling alone writes nothing): the output's lay lines of a record of several parts whose levels after the lay are a whole multiple of the levels before on both levels of the line, now and before (a source's lay moves the level now alone and is no scaling), grouped by the frame the line's position names and the family: the coefficient per part (1 where no line was written, the engine writing the lines whose coefficient is not 1), the Nodes written; a group holding a line that is no scaling is a lay, an emission's or a packet's, drawn as the hole and never labelled the write; the last frame of a run back with no write's lines is the birth where nothing was written. */
const PARTS_OF = {}, WIDTH_OF = {};
for (const f of FAMILIES) { WIDTH_OF[f.name] = f.plane ? 2 : 1; if (f.quanta && f.lines > WIDTH_OF[f.name]) PARTS_OF[f.name] = f.lines / WIDTH_OF[f.name]; }
const scaleOf = line => { const before = Array.isArray(line.before) ? line.before : [], after = Array.isArray(line.after) ? line.after : []; let c = null; for (let i = 0; i < 2; i++) { const x = Number(before[i]), y = Number(after[i]); if (!Number.isFinite(x) || !Number.isFinite(y)) return null; if (x !== 0) { const r = y / x; if (!Number.isInteger(r) || (c !== null && r !== c)) return null; c = r === 0 ? 0 : r; } else if (y !== 0) return null; } return c; };
const GROUPS = {};  // per frame and family the lay lines of a record of several parts
if (OUTPUT) for (const line of OUTPUT.lines) if (line.event === 'lay' && PARTS_OF[line.family] !== undefined) { const g = positionOfLine(line) + '|' + line.family; (GROUPS[g] || (GROUPS[g] = [])).push(line); }
const WRITTEN = new Set(), WRITES_AT = {};
for (const g in GROUPS) { const lines = GROUPS[g]; if (lines.some(line => scaleOf(line) === null)) continue; const k = positionOfLine(lines[0]), family = lines[0].family, w = { family, coefficients: Array(PARTS_OF[family]).fill(1), nodes: new Set() }; for (const line of lines) { const part = Math.floor(Number(line.line) / WIDTH_OF[family]); if (part >= 0 && part < w.coefficients.length) w.coefficients[part] = scaleOf(line); if (line.node && Array.isArray(line.node.at)) w.nodes.add(line.node.at.join(',')); WRITTEN.add(line); } if (w.coefficients.some(c => c !== 1)) (WRITES_AT[k] || (WRITES_AT[k] = [])).push(w); }
const isWrite = line => WRITTEN.has(line);
const BIRTHS = new Set(LOOK.frames.map((_, k) => k).filter(k => DIRECTION(k) < 0 && (k === T || PASS(k + 1) !== PASS(k))));  // the run backs' last frames, the record's birth
const scaledWords = (w, html) => (Object.keys(PARTS_OF).length > 1 ? (html ? esc(w.family) : w.family) + "'s parts" : 'the parts') + ' scaled by (' + w.coefficients.map(format).join(', ') + ')';
const NOTHING_WRITTEN = "nothing written, the realised port's coefficients a scaling of the parts alone (the port realised all the same)";
const writeLabel = k => WRITES_AT[k] ? ", the click's write at the birth: " + WRITES_AT[k].map(w => scaledWords(w, false)).join('; ') : OUTPUT && BIRTHS.has(k) ? ", the click's write at the birth: " + NOTHING_WRITTEN : '';
/* The count on the board (ALGEBRA.md, The count on the board, 2026-10-20): the frame's `board_count` per family where the look carries it, the record's count read from the board (the families holding a record, their count other than 0; the family named where the look reads the count of more than one family), and the credit line's `board_count` at the close, read before the write. */
const outsideLabel = k => { if (!GROWS) return ''; const fr = frameOf(k), found = []; for (const f of QUANTA) { const count = fr[f.name].count; let n = 0; for (let i = 0; i < N; i++) if (count[i] && !declared(nodeOf(i))) n++; if (n) found.push(nodesWord(n) + ' of ' + f.name); } return found.length ? ', with a count on the layers the receding faces grew, outside the declared board: ' + found.join(', ') + (GROWN.on ? '' : ' (the layers\\' switch under the board)') : ''; };  // the Nodes with a count beyond the declared board, the frame's own arrays
const countLabel = k => { const found = []; let carrying = 0; for (const f of FAMILIES) { const row = (LOOK.frames[k].families || {})[f.name]; if (row && row.board_count !== undefined && row.board_count !== null) { carrying++; if (row.board_count !== 0) found.push([f.name, row.board_count]); } } return found.length ? ', the count on the board ' + found.map(([name, n]) => carrying > 1 ? format(n) + ' of ' + name : format(n)).join(', ') : ''; };  // the look's own row (frameOf keeps the arrays alone)
const HOLES_AT = {}, FACES_AT = {}, FRONTS_AT = {}, RECORD_CREDITS = {}, REGION_CREDITS = [];  // the holes and the faces by the frame they belong to; the regions' credit lines (a side's credit line carries its `order`, `scale` and `board_count`)
if (OUTPUT) for (const line of OUTPUT.lines) {
  if (line.event === 'lay' && !isWrite(line) && line.node && Array.isArray(line.node.at)) (HOLES_AT[positionOfLine(line)] || (HOLES_AT[positionOfLine(line)] = new Set())).add(line.node.at.join(','));
  if (line.event === 'face' && line.node && Array.isArray(line.node.at)) (FACES_AT[positionOfLine(line)] || (FACES_AT[positionOfLine(line)] = new Set())).add(line.node.at.join(','));
  if (line.event === 'erasure') (FRONTS_AT[line.interval] || (FRONTS_AT[line.interval] = [])).push(line);
  if (line.event === 'credit' && /^body \\d+$/.test(String(line.node_detector))) (RECORD_CREDITS[line.node_detector] || (RECORD_CREDITS[line.node_detector] = [])).push(line);
  if ((line.event === 'credit' || line.event === 'conversion') && !/^body \\d+$/.test(String(line.node_detector))) REGION_CREDITS.push(line);  // the conversion line beside a region's credit, a row of the table (2026-10-21)
}
const DETECTOR_BODIES = LOOK.bodies.filter(b => b.reader || b.detector || RECORD_CREDITS['body ' + b.number]).map(b => b.number);  // the records declared readers (the look's flag; the credits of an older look)
/* The clicks' light cones (the owner's word of 2026-10-22, "let them show in the experiment's run all the clicks with their cone and everything"): every credit line of the output file is a click, the one act at the window's close (reports.credit, the one click line kind of every reader: a region's credit, with the conversion's records out where a conversion line stands beside it, a record's absorption, its emission at a rate or by its own light, the null window's re-lay at the count 0), and the line names no Node, so the Nodes the click wrote are read from the LATTICE lines beside it in the output: the lay lines contiguous with the credit line at its interval that are no scaling write and are of the click's families (the credited record's, the one it absorbed from or emitted to, or the conversion's records out), the conversion line between them; and the hole, the face lines at the interval after of the family whose quantum the click took (the credited record's, or the absorbed one's), the erasure line of that family beginning there at the distance 1 naming it as its origin, else the Node faced at both of the two intervals after (the hole's faces stand two intervals, a front's shell passes a Node once); a click with no written Node in the output (a beam's quantum passing in the books alone) has no cone and says so; where two clicks of one family fall at one interval the page gives their lines to the first (the law's No click names a Node keeps the Node off the line, so the inference from the lines beside it is the source, with this limit named). The cone at the frame of interval t is the Nodes within t - t_c + 1 Links of the click's Nodes in the Link metric with the wrap, the run back's cone's own geometry with one support per click (linkDistanceTo; ALGEBRA.md, The interval's dependency radius is one Link: every act one Link's reach, so the cone grows one Link per interval and the pace of light on the board, 1 / sqrt 3 Links per interval, lies inside it), from the click's frame on; each click's cone in a tone of its own from the style block's list, the cones painted from the earliest click to the latest so that the latest lies on top at the full tint and each older one fades by --click-fade. Every number is the output's; nothing is drawn between Nodes or between frames. */
const TONES = token('--click-tones').split(',').map(tone => tone.trim()).filter(Boolean);
const nodeAt = line => line && line.node && Array.isArray(line.node.at) ? line.node.at.join(',') : null;
const CONVERSIONS_BESIDE = new Map();  // a region's credit line and the conversion line beside it: the same interval, region and family
if (OUTPUT) for (const line of OUTPUT.lines) if (line.event === 'conversion') { const credit = OUTPUT.lines.find(c => c.event === 'credit' && c.interval === line.interval && c.node_detector === line.node_detector && c.family === line.family); if (credit) CONVERSIONS_BESIDE.set(credit, line); }
function writtenBeside(index) {  // the lay lines contiguous with the credit line at `index` at its interval (the conversion line between them): the quantum laid (light's at the emission, the conversion's records out) and the exchange over the credited record's own Nodes (its parts moved, the null window's re-lay), with the Nodes each wrote
  const credit = OUTPUT.lines[index], conversion = CONVERSIONS_BESIDE.get(credit) || null;
  const laidOf = new Set(conversion && Array.isArray(conversion.into) ? conversion.into : [credit.emitted].filter(f => f !== null && f !== undefined));
  const own = line => line === conversion || (line.event === 'lay' && line.interval === credit.interval && (laidOf.has(line.family) || line.family === credit.family) && !isWrite(line) && nodeAt(line) !== null);
  const lays = [];
  for (let k = index - 1; k >= 0 && own(OUTPUT.lines[k]); k--) if (OUTPUT.lines[k].event === 'lay') lays.unshift(OUTPUT.lines[k]);
  for (let k = index + 1; k < OUTPUT.lines.length && own(OUTPUT.lines[k]); k++) if (OUTPUT.lines[k].event === 'lay') lays.push(OUTPUT.lines[k]);
  const laid = lays.filter(line => laidOf.has(line.family)), exchange = lays.filter(line => !laidOf.has(line.family));
  return { conversion, laid, exchange, laidNodes: new Set(laid.map(nodeAt)), exchangeNodes: new Set(exchange.map(nodeAt)) };
}
function holeBeside(credit) {  // the hole's Nodes: the erasure's origin of the taken family beginning at the interval after, else the Node faced at both intervals after, else any Node faced at the interval after; where two clicks take one family at one interval the lines go to the first
  const family = credit.absorbed || credit.family, next = Number(credit.interval) + 1, lines = OUTPUT.lines;
  const origins = new Set(lines.filter(line => line.event === 'erasure' && line.family === family && line.interval === next && line.distance === 1 && Array.isArray(line.origin)).map(line => line.origin.join(',')));
  const faced = at => new Set(lines.filter(line => line.event === 'face' && line.family === family && line.interval === at && nodeAt(line) !== null).map(nodeAt));
  const first = faced(next), second = faced(next + 1), twice = [...first].filter(at => second.has(at));
  const found = origins.size ? { nodes: origins, from: "the erasure line's origin at " + next } : twice.length ? { nodes: new Set(twice), from: 'the face lines at ' + next + ' and ' + (next + 1) } : { nodes: first, from: first.size ? 'the face lines at ' + next : '' };
  if (found.nodes.size && lines.find(line => line.event === 'credit' && line.interval === credit.interval && (line.absorbed || line.family) === family) !== credit) return { nodes: new Set(), from: "the hole's lines of the interval after given to the first click of " + family + ' at this interval' };
  return found;
}
/* The light's front of a bound body (2026-10-22): the look's body row `shell`, the Nodes of the shell at r = 1 / k about the declared Node (the loader's own numbers, recorded; the page computes no radius), drawn as a ring of Nodes in the shell's tone, each ring scaled by the light booked at its Node at the frame shown (the frame's `own_light`, the window's running sum per shell Node as the books hold it after the interval, empty right after the close) against the largest booked over the run; the book's sum and the carry graphed in the records' panel. */
const SHELLED = LOOK.bodies.filter(b => Array.isArray(b.shell) && b.shell.length);
const SHELL_INDEX = new Map(); for (const b of SHELLED) b.shell.forEach((at, j) => SHELL_INDEX.set(at.join(','), [b.number, j]));
const lightOf = (k, number) => { const own = LOOK.frames[k].own_light, row = own && own[String(number)]; return row && Array.isArray(row.light) ? row.light : []; };
const carryOf = (k, number) => { const own = LOOK.frames[k].own_light, row = own && own[String(number)]; return row && typeof row.carry === 'number' ? row.carry : null; };
const LIGHT_MOST = {}; for (const b of SHELLED) { let most = 0; for (let k = 0; k <= T; k++) for (const v of lightOf(k, b.number)) most = Math.max(most, Math.abs(v)); LIGHT_MOST[b.number] = most; }
function laidInFrames(credit) {  // a bound body's emission whose light the output lays on no line of its own: the shell Node where the emitted light's count first stands at the click's frame against the frame before (the only new level of the light inside the ring), the frames' word
  const body = SHELLED.find(b => 'body ' + b.number === String(credit.node_detector)), family = credit.emitted, k = Math.min(positionOfLine(credit), T);
  if (!body || !family || !FAMILIES.some(f => f.name === family && f.quanta) || k < 1) return [];
  const now = frameOf(k)[family].count, before = frameOf(k - 1)[family].count;
  return body.shell.filter(at => { const i = indexOf(...at); return i >= 0 && i < N && now[i] > before[i]; });
}
const CLICK_CONES = [];
if (OUTPUT) OUTPUT.lines.forEach((line, index) => {
  if (line.event !== 'credit') return;
  const written = writtenBeside(index), hole = holeBeside(line), from = [];  // the click's Node: where the quantum was taken (the hole) or laid; the exchange over the record's own Nodes where the click wrote nothing else (the null window's re-lay)
  if (hole.nodes.size || hole.from) from.push(hole.from);
  if (written.laidNodes.size) from.push(written.laid.length + (written.laid.length === 1 ? ' lay line' : ' lay lines') + ' of the quantum laid beside it');
  const support = new Set([...hole.nodes, ...written.laidNodes]);
  if (!support.size) { for (const at of written.exchangeNodes) support.add(at); if (support.size) from.push(written.exchange.length + (written.exchange.length === 1 ? ' lay line' : ' lay lines') + ' of the record itself beside it'); }
  const nodes = [...support].map(at => at.split(',').map(Number));
  if (!nodes.length) { const laid = laidInFrames(line); if (laid.length) { nodes.push(...laid); from.push('the frames: the light first standing at the shell Node at this frame'); } }
  const tone = TONES.length ? TONES[CLICK_CONES.length % TONES.length] : token('--cone');
  CLICK_CONES.push({ line, conversion: written.conversion, exchange: written.exchange, exchangeNodes: [...written.exchangeNodes].map(at => at.split(',').map(Number)), nodes, from, interval: Number(line.interval), position: positionOfLine(line), tone, colour: new THREE.Color(tone), distance: nodes.length ? Float64Array.from({ length: N }, (_, i) => linkDistanceTo(nodes, nodeOf(i))) : null });
});
CLICK_CONES.sort((a, b) => a.position - b.position || a.interval - b.interval);
const CONE_LAYER = "the clicks' cones";
const coneRadiusAt = (c, k) => c.distance && k >= c.position && INTERVAL(k) >= c.interval ? INTERVAL(k) - c.interval + 1 : null;  // t - t_c + 1 at the frame of interval t, from the click's frame on
function conesAt(k) {  // the cones present at the frame, the earliest first: the latest at the full tint, each older one faded by --click-fade
  const found = CLICK_CONES.map(c => ({ cone: c, radius: coneRadiusAt(c, k) })).filter(x => x.radius !== null), tint = size('--click-tint'), fade = size('--click-fade');
  found.forEach((x, j) => { x.tint = tint * Math.pow(fade, found.length - 1 - j); });
  return found;
}
const clickCount = (c, k) => { const radius = coneRadiusAt(c, k); if (radius === null) return null; let n = 0; for (let i = 0; i < N; i++) if (c.distance[i] <= radius && inBox(nodeOf(i), LOOK.frames[k])) n++; return n; };
const OWN_LIGHT_WORDS = ['light', 'outflow', 'carry'];  // the words a bound body's close may carry on its credit line for its own light (the window's booked outflow, its carry), read where present
const ownLightOf = line => OWN_LIGHT_WORDS.filter(word => line[word] !== undefined && line[word] !== null);
const bodyLine = line => /^body \\d+$/.test(String(line.node_detector));
const closedShare = row => row && Array.isArray(row.closed_share) && Number(row.closed_share[1]) > 0;  // a close of the body's own light stands in the row: the share's unit is set there (0 until the first own-light close, and on a body emitting at its declared rate)
const closedAt = c => { const body = SHELLED.find(b => 'body ' + b.number === String(c.line.node_detector)), own = body && LOOK.frames[Math.min(c.position, T)].own_light, row = own && own[String(body.number)]; return closedShare(row) ? row : null; };  // the frame's own_light row at the click where it carries the close's share: the draw of the body's own light was made there
function kindOf(c) {  // the click's kind named from the line's own words (and the frames' close words for a bound body's own light)
  const l = c.line, closed = closedAt(c);
  if (!l.count) return 'the null window: no click, the record laid again whole (' + l.node_detector + ', ' + l.family + ', the LATTICE line)';
  if (bodyLine(l) && l.absorbed) return 'the absorption: ' + l.node_detector + ' (' + l.family + ') took one quantum of ' + l.absorbed + ', ' + l.before + ' to ' + l.realised;
  if (bodyLine(l) && l.emitted) return 'the emission: ' + l.node_detector + ' (' + l.family + ') gave one quantum to ' + l.emitted + ', ' + l.before + ' to ' + l.realised + (ownLightOf(l).length || closed ? ' by its own light at the close' + (closed ? " (the frames' closed_share [" + closed.closed_share.map(format).join(', ') + '] and closed_light ' + format(closed.closed_light) + ' at its frame)' : '') : '');
  const words = "the region's credit: " + l.node_detector + ' credited ' + (l.count === 1 ? 'one quantum' : format(l.count) + ' quanta') + ' of ' + l.family;
  return c.conversion ? words + ', converted into ' + [].concat(c.conversion.into || []).join(' + ') + (Array.isArray(c.conversion.senses) ? ' at the senses ' + c.conversion.senses.join(', ') : '') : words;
}
const key = line => [line.interval, line.node_detector, line.family, line.inflow].join('|');
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
/* The frame: the declared board's two axes across the view with a margin of Links, fitted to the stage; the eye along VIEW at the board's centre, looking at it, the up axis the second of ACROSS.
   The default camera (2026-10-20, the lit box 2026-10-21): the board's own fit where a Node then spans --node-least pixels or more; else the lit extent, the Nodes any family of quanta lights with the bodies' Nodes and the regions' (a region a node_detector of Nodes alone other than the declared faces' `face`, and one spanning half the board or more frames nothing): the union of the frames' lit boxes over the run framed whole wherever it fits at --node-fit-least pixels per Node or more (the pixels per Node the whole number the stage allows, at most --node-most), and where it does not, a window of --node-least pixels per Node along the long axis following the frame's lit Nodes within that extent; either way one scale over the run, held frame to frame where the lit box grows (the frame's own box moved the zoom with it, 2026-10-21); the whole board one zoom step out (the buttons step between the two frames). The camera is presentation: it frames and computes no number but the box it frames. */
const litNodes = fr => { const found = [], [fy, fz] = shapeOf(fr).slice(1), o = originOf(fr); for (const f of QUANTA) { const now = ((fr.families || {})[f.name] || {}).now; if (!now) continue; if (Array.isArray(now)) now.forEach((plane, x) => plane.forEach((row, y) => row.forEach((v, z) => { if (v) found.push([x + o[0], y + o[1], z + o[2]]); }))); else now.at.forEach((k, j) => { if (now.values[j]) found.push([Math.floor(k / (fy * fz)) + o[0], Math.floor(k / fz) % fy + o[1], k % fz + o[2]]); }); } return found; };
const emptyBox = () => [0, 1, 2].map(() => [Infinity, -Infinity]);
const grow = (box, nodes) => { for (const n of nodes) for (let a = 0; a < 3; a++) { if (box[a][0] > n[a]) box[a][0] = n[a]; if (box[a][1] < n[a]) box[a][1] = n[a]; } return box; };
const merge = (box, other) => { for (let a = 0; a < 3; a++) { box[a][0] = Math.min(box[a][0], other[a][0]); box[a][1] = Math.max(box[a][1], other[a][1]); } return box; };
const REGION_NODES = LOOK.node_detectors.filter(d => d.body === null && d.name !== 'face' && d.nodes.length * 2 < LOOK.shape[0] * LOOK.shape[1] * LOOK.shape[2]).flatMap(d => d.nodes);
const FIXED_BOX = grow(emptyBox(), [...LOOK.bodies.flatMap(b => b.nodes), ...REGION_NODES]);  // the bodies' and the regions' Nodes, lit or not
const LIT_AT = LOOK.frames.map(fr => grow(emptyBox(), litNodes(fr)));  // per frame, the box of the Nodes lit in it
const LIT = LIT_AT.reduce(merge, merge(emptyBox(), FIXED_BOX));  // over the run
const LIT_SEEN = LIT.every(([lo, hi]) => Number.isFinite(lo) && Number.isFinite(hi));
const LONG = LIT_SEEN ? ACROSS.reduce((best, a) => LIT[a][1] - LIT[a][0] > LIT[best][1] - LIT[best][0] ? a : best, ACROSS[0]) : ACROSS[0];  // the across axis of the longer lit extent
const sceneOf = (c, a) => c - LOW[a] - ([X, Y, Z][a] - 1) / 2;  // a file coordinate in the scene, as position() places the Nodes
let FRAMING = null, LIT_DEFAULT = false, shown = 0, PIXELS_PER_NODE = 1;  // the frame in force, 'board' or 'lit', decided at the first fit with a stage; whether the lit frame is the page's default; the frame drawn; the fit's pixels per Node
const litCentre = k => { const b = merge(merge(emptyBox(), LIT_AT[k] || emptyBox()), FIXED_BOX)[LONG]; return Number.isFinite(b[0]) ? (b[0] + b[1]) / 2 : (LIT[LONG][0] + LIT[LONG][1]) / 2; };
const aimed = (half, margin) => { const [lo, hi] = LIT[LONG]; if (hi - lo + 1 + 2 * margin <= 2 * half) return (lo + hi) / 2; return Math.min(hi + 0.5 + margin - half, Math.max(lo - 0.5 - margin + half, litCentre(shown))); };  // the view's centre along the long axis: the extent's where it fits, else the frame's lit Nodes within the extent
function fit() {
  const w = stage.clientWidth || 1, margin = size('--view-margin');
  let halfW = (LOOK.shape[ACROSS[0]] + 2 * margin) / 2, halfH = (LOOK.shape[ACROSS[1]] + 2 * margin) / 2;
  stage.style.height = Math.round(Math.max(size('--board-least'), Math.min(size('--board-most'), w * halfH / halfW))) + 'px';  // the stage the board's own shape, within bounds
  const h = stage.clientHeight || 1;
  if (FRAMING === null && w > 1) { LIT_DEFAULT = LIT_SEEN && w / (2 * halfW) < size('--node-least'); FRAMING = LIT_DEFAULT ? 'lit' : 'board'; }
  const centre = new THREE.Vector3(...CENTRE);
  if (FRAMING === 'lit') {
    const box = LIT;  // the union of the frames' lit boxes over the run with the bodies' and the regions' Nodes: one box, one scale, held frame to frame
    const along = LONG === ACROSS[0] ? w : h, whole = Math.min(size('--node-most'), Math.floor(along / (box[LONG][1] - box[LONG][0] + 1 + 2 * margin)));  // the pixels per Node at which the run's box fits whole
    const fits = whole >= size('--node-fit-least'), px = fits ? whole : size('--node-least');
    halfW = w / (2 * px); halfH = h / (2 * px);
    for (const a of ACROSS) centre.setComponent(a, sceneOf((box[a][0] + box[a][1]) / 2, a));
    if (!fits) centre.setComponent(LONG, sceneOf(aimed(LONG === ACROSS[0] ? halfW : halfH, margin), LONG));  // the scale held, the window following the frame's lit Nodes
  } else if (halfW / halfH > w / h) halfH = halfW * h / w; else halfW = halfH * w / h;
  PIXELS_PER_NODE = w / (2 * halfW);  // the fit's scale, for the dots' least size in pixels
  camera.left = -halfW; camera.right = halfW; camera.top = halfH; camera.bottom = -halfH; camera.updateProjectionMatrix();
  const eye = centre.clone(), up = new THREE.Vector3();
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
const cubes = new THREE.InstancedMesh(new THREE.BoxGeometry(...extentAlong(cubeSide, cubeDepth)), new THREE.MeshBasicMaterial({ color: 0xffffff }), N);  // unlit, so that a Node's glow is drawn in the tone the frame gives it and no light dims it (the owner's word of 2026-10-04: the tones stand out)
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
if (CONED) layers['the cone'] = { on: true, objects: [] };  // the run back's reach, shaded on the cubes of the frames that carry a radius
if (CLICK_CONES.some(c => c.nodes.length)) layers[CONE_LAYER] = { on: true, objects: [] };  // the clicks' light cones, shaded on the cubes from each click's frame on
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
const bodyExtent = n => Math.max(1, ...LOOK.frames.map(fr => fr.bodies[n].length));
const ringCapacity = LOOK.node_detectors.reduce((n, d) => n + (d.body === null ? d.nodes.length : bodyExtent(d.body)), 0) + DETECTOR_BODIES.reduce((n, b) => n + bodyExtent(b), 0);
const ringGeometry = new THREE.TorusGeometry(size('--ring-radius'), size('--ring-tube'), 8, 32);  // the ring faces the eye: it lies across the axis seen along
if (VIEW === 1) ringGeometry.rotateX(Math.PI / 2); else if (VIEW === 0) ringGeometry.rotateY(Math.PI / 2);
const rings = new THREE.InstancedMesh(ringGeometry, new THREE.MeshBasicMaterial({ color: 0xffffff }), Math.max(ringCapacity, 1));
scene.add(rings);
layers['node_detector rings (the declared regions and the records declared readers)'] = { on: true, objects: [rings] };
const shells = new THREE.InstancedMesh(ringGeometry, new THREE.MeshBasicMaterial({ color: 0xffffff }), Math.max(1, SHELLED.reduce((n, b) => n + b.shell.length, 0)));
shells.setMatrixAt(0, hidden); shells.visible = SHELLED.length > 0; scene.add(shells);
if (SHELLED.length) layers["the light's front (a bound body's shell at r = 1 / k about its Node, each ring scaled by the light booked at its shell Node)"] = { on: true, objects: [shells] };
/* The hole and the front, from the output file: a wire cube at each Node the lay and face lines write at the interval shown, and a small cube at each Node of the erasure lines' shells at that interval. */
const holeCapacity = Math.max(1, ...Object.values(HOLES_AT).map(set => set.size)), frontCapacity = Math.max(1, ...Object.values(FACES_AT).map(set => set.size));
const holes = new THREE.InstancedMesh(new THREE.BoxGeometry(...extentAlong(size('--hole-size'), size('--hole-size'))), new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true }), holeCapacity);
const fronts = new THREE.InstancedMesh(new THREE.BoxGeometry(...extentAlong(size('--front-size'), size('--front-size'))), new THREE.MeshBasicMaterial({ color: 0xffffff }), frontCapacity);
holes.setMatrixAt(0, hidden); fronts.setMatrixAt(0, hidden);
scene.add(holes, fronts);
if (Object.keys(HOLES_AT).length) layers['the hole (the lay lines)'] = { on: true, objects: [holes] };
if (Object.keys(FACES_AT).length) layers['the faces presented (the face lines: the hole, then the front)'] = { on: true, objects: [fronts] };
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
  if (boxKey === LAYER + '|' + GROWN.on) return;
  boxKey = LAYER + '|' + GROWN.on;
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
if (GROWS) layers['the layers the receding faces grew (' + [X, Y, Z].join(' x ') + ' as grown; zoom out to see them)'] = GROWN;

function themed() {
  scene.background = new THREE.Color(token('--board'));
  box.material.color.set(token('--line')); plane.material.color.set(token('--muted')); wall.material.color.set(token('--wall'));
  holes.material.color.set(token('--hole')); fronts.material.color.set(token('--front')); shells.material.color.set(token('--shell'));
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
  const base = new THREE.Color(token('--cube')), coneTone = new THREE.Color(token('--cone')), cones = layers[CONE_LAYER] && layers[CONE_LAYER].on ? conesAt(t) : [];
  boxAt(frame);
  for (let i = 0; i < N; i++) {
    colour.copy(base);
    if (CONED && layers['the cone'].on && inCone(i, t)) colour.lerp(coneTone, size('--cone-tint'));  // the cone's Nodes in the cone's tone, the floor the record's glow stands on
    for (const x of cones) if (x.cone.distance[i] <= x.radius) colour.lerp(x.cone.colour, x.tint);  // the clicks' cones, the latest painted last and brightest
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
  const radius = size('--dot-radius'), floor = Math.max(size('--dot-floor'), size('--dot-least') / (PIXELS_PER_NODE * camera.zoom));  // a dot's least radius in Links, and --dot-least pixels at the fit's scale, so that a Node with quanta is seen at the board's own fit (2026-10-21)
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
  for (const d of LOOK.node_detectors) {
    if (d.name === 'face') continue;  // the open faces' layer reports, but is no declared region: not drawn
    const nodes = d.body === null ? d.nodes : frame.bodies[d.body];
    const flashing = frame.lines.some(line => line.event === 'click' && line.node_detector === d.name);
    for (const [x, y, z] of nodes) {
      rings.setMatrixAt(slot, inside(indexOf(x, y, z)) ? matrix.compose(position(indexOf(x, y, z)), quaternion, scale.setScalar(flashing ? flashScale : 1)) : hidden);
      rings.setColorAt(slot, flashing ? flashColour : ringColour); slot++;
    }
  }
  for (const n of DETECTOR_BODIES) {
    const flashing = (RECORD_CREDITS['body ' + n] || []).some(line => line.interval === INTERVAL(t) && positionOfLine(line) === t && line.count);
    for (const [x, y, z] of frame.bodies[n]) {
      rings.setMatrixAt(slot, inside(indexOf(x, y, z)) ? matrix.compose(position(indexOf(x, y, z)), quaternion, scale.setScalar(flashing ? flashScale : 1)) : hidden);
      rings.setColorAt(slot, flashing ? flashColour : ringColour); slot++;
    }
  }
  for (; slot < rings.count; slot++) rings.setMatrixAt(slot, hidden);
  rings.instanceMatrix.needsUpdate = true; if (rings.instanceColor) rings.instanceColor.needsUpdate = true;
  let shellSlot = 0;
  const shellScale = size('--shell-scale'), shellMost = size('--flash-scale');
  for (const b of SHELLED) { const light = lightOf(t, b.number), most = LIGHT_MOST[b.number]; for (const [j, at] of b.shell.entries()) { const i = indexOf(...at), v = light[j] || 0, s = shellScale + (most ? Math.abs(v) / most : 0) * (shellMost - shellScale); shells.setMatrixAt(shellSlot++, i >= 0 && i < N && inside(i) ? matrix.compose(position(i), quaternion, scale.setScalar(s)) : hidden); } }
  for (; shellSlot < shells.count; shellSlot++) shells.setMatrixAt(shellSlot, hidden);
  shells.instanceMatrix.needsUpdate = true;
  let hole = 0;
  for (const at of HOLES_AT[t] || []) { const [x, y, z] = at.split(',').map(Number), i = indexOf(x, y, z); if (i >= 0 && i < N && inside(i)) holes.setMatrixAt(hole++, matrix.makeTranslation(...position(i).toArray())); }
  for (; hole < holes.count; hole++) holes.setMatrixAt(hole, hidden);
  holes.instanceMatrix.needsUpdate = true;
  let front = 0;
  for (const at of FACES_AT[t] || []) { const [x, y, z] = at.split(',').map(Number), i = indexOf(x, y, z); if (i >= 0 && i < N && inside(i)) fronts.setMatrixAt(front++, matrix.makeTranslation(...position(i).toArray())); }
  for (; front < fronts.count; front++) fronts.setMatrixAt(front, hidden);
  fronts.instanceMatrix.needsUpdate = true;
  for (const layer of Object.values(layers)) layer.objects.forEach(o => { o.visible = layer.on; });
  shown = t; if (FRAMING === 'lit') fit();  // the view along the long axis follows the frame's lit Nodes where the extent does not fit
  renderer.render(scene, camera);
  byId('slider').value = t;
  byId('frame').textContent = (t === 0 ? 'laid, 0 / ' + LAST : TICK(t) !== null ? 'tick ' + TICK(t) + ' / ' + LAST_TICK + (TICK(t) === INTERVAL(t) ? ', the record at interval ' : ', the record read at interval ') + INTERVAL(t) : 'interval ' + INTERVAL(t) + ' / ' + LAST) + (PASSES > 1 ? ', ' + passLabel(t) : '') + (CONED ? coneLabel(t) : '') + writeLabel(t) + countLabel(t) + outsideLabel(t);
  byId('direction').innerHTML = PASSES > 1 ? `<svg viewBox="0 0 12 12" role="img" aria-label="${DIRECTION(t) < 0 ? 'the run back' : 'the run forward'}"><path d="${DIRECTION(t) < 0 ? 'M 11 1 L 1 6 L 11 11 z' : 'M 1 1 L 11 6 L 1 11 z'}" fill="${DIRECTION(t) < 0 ? token('--back') : token('--forward')}"/></svg>` : '';
  const counts = {};
  for (const line of frame.lines) counts[line.event] = (counts[line.event] || 0) + 1;
  const clicks = frame.lines.filter(line => line.event === 'click').map(line => line.node_detector + ': ' + line.family);
  byId('lines').textContent = t === 0 ? 'The world as laid: the bodies\\' declared counts, the levels of the mode file, every held row at its start.'
    : Object.entries(counts).map(([event, n]) => n + ' ' + event + (n === 1 ? '' : 's')).join(', ') + (clicks.length ? ' (' + [...new Set(clicks)].join(', ') + ')' : '') || 'no line this interval';
  clicksNow();
  if (REACH) {
    const radius = CONE_RADIUS(t), count = coneCount(t), volume = VOLUME && VOLUME[INTERVAL(t)] !== undefined && VOLUME[INTERVAL(t)] !== null ? Number(VOLUME[INTERVAL(t)]) : null, cells = shapeOf(LOOK.frames[t]).reduce((p, e) => p * e, 1);
    const grownShape = shapeOf(LOOK.frames[T]).join(' x '), grownCells = shapeOf(LOOK.frames[T]).reduce((p, e) => p * e, 1), closing = VOLUME && VOLUME[LAST] !== undefined ? Number(VOLUME[LAST]) : null;
    const fills = CONED ? ` The cone holds the declared board of ${LOOK.shape.join(' x ')} Nodes whole from the interval ${format(FILLED.declared)} on (its farthest Node ${format(FILLED.declared + 1)} Links from the birth\\'s Nodes)` + (FILLED.grown <= LAST ? ` and the board as grown, ${grownShape}, whole from the interval ${format(FILLED.grown)} on` : ` and at the close ${closing === null ? '' : format(closing) + ' of '}the grown board\\'s ${format(grownCells)} Nodes (${grownShape}), inside it`) + ': the shading shows the record\\'s own region shrinking back to the birth\\'s Nodes and growing from it.' : '';
    const stepped = STEPPED ? STEPPED.reduce((s, v) => s + (Number(v) || 0), 0) : null;
    const alone = stepped === null ? '' : ` Only the record\\'s cone is stepped on the run back and forward (${format(stepped)} Node-steps in all, the box with its ring, the header\\'s cone_stepped); the rest of the board is neither read nor written.`;
    const legend = CONED ? '<b>The click is where the past met the future: the record\\'s own light cone runs back after the click, the realised term is written at the record\\'s birth, and the cone runs forward with it; the rest of the board neither read nor written</b> (one ring beyond the cone read from the board and asserted equal to the record\\'s reference, the board at its birth, the lay\\'s frame 0 for a record laid at the start, by the engine at every step): at the Nodes Rule3 at -1 and +1 inside the record\\'s cone, the draws, the write at the birth and the count\\'s write the only acts of the click, the board\\'s tick standing at the close while the record is read back and forward, the detectors\\' proper clocks the Nodes\\' own; the shading a geometry from the frames\\' cone_radius and the header\\'s cone_support in the front\\'s Link metric with the wrap, every number the look\\'s.' + alone + fills : REACH === 'board' ? "<b>The click is where the past met the future: the whole board runs back to the record's birth after the click, the realised term is written there, and the board runs forward with it</b> (the reach board, the whole board stepped by Rule3 at -1 and +1: the record's cone not stepped alone, a check of the cone's reach, the two equal bit for bit; the draws, the write at the birth and the count's write the only acts of the click, the board's tick standing at the close while the record is read back and forward" + (stepped === null ? '' : ', ' + format(stepped) + " Node-steps in all, the header's cone_stepped") + ').' : 'the run back\\'s reach: ' + esc(REACH) + ' (the run back and forward by Rule3 at -1 and +1, the draws and the count\\'s write the only acts of the click).';
    const now = radius === null ? (CONED ? 'This frame: the run to the first close; the cone on the frames of the run back and forward.' : '') : `This frame: the cone ${linksWord(radius)} about the birth's ${nodesWord(SUPPORT.length)}${esc(supportSpan())}, ${format(count)} Nodes of the frame's ${format(cells)} inside it` + (volume === null ? '' : `, the look's |G| ${format(volume)}${volume === count ? ', the same' : ', differs'}`) + '; outside the cone the board as the engine left it, neither read nor written.';
    const written = WRITES_AT[t], writeNow = written ? written.map(w => "This frame: the click's write at the record's birth, " + scaledWords(w, true) + ' at ' + nodesWord(w.nodes.size) + " (the output's lay lines, the levels after the write a whole multiple of the levels before); the run forward carries the realised term.").join('<br>') : OUTPUT && BIRTHS.has(t) ? "This frame: the record's birth at the end of the run back, " + NOTHING_WRITTEN + '; the run forward carries the realised term.' : '';
    const closedHere = OUTPUT ? OUTPUT.lines.filter(line => line.event === 'credit' && positionOfLine(line) === t && line.board_count !== undefined && line.board_count !== null) : [];
    const countNow = closedHere.map(line => "This frame: the record's count read from the board at the close of " + esc(String(line.node_detector)) + ', ' + format(line.board_count) + ", before the write (the credit line's board_count: the record's share in its unit over the written coefficients' norm)").join('<br>');
    byId('cone').innerHTML = legend + (now ? '<br>' + now : '') + (writeNow ? '<br>' + writeNow : '') + (countNow ? '<br>' + countNow : '');
  }
  if (!MEASURE) drawMeasure();
  moveCursors();{{GATE_DRAW}}
}

/* The view is fixed: no turning; the wheel and the two buttons bring the board closer or farther, within a bound; a board of three axes has its layer picked. */
canvas.addEventListener('pointermove', hover);
canvas.addEventListener('pointerleave', () => hover(null));
canvas.addEventListener('wheel', e => { e.preventDefault(); zoom(Math.exp(e.deltaY * size('--zoom-rate'))); }, { passive: false });
function zoom(factor) { camera.zoom = Math.min(size('--zoom-most'), Math.max(1 / size('--zoom-most'), camera.zoom / factor)); camera.updateProjectionMatrix(); renderer.render(scene, camera); }
byId('zoom-in').addEventListener('click', () => { if (FRAMING === 'board' && LIT_DEFAULT && camera.zoom >= 1) { FRAMING = 'lit'; camera.zoom = 1; fit(); renderer.render(scene, camera); } else zoom(size('--zoom-step')); });  // one step in from the whole board: the lit extent
byId('zoom-out').addEventListener('click', () => { if (FRAMING === 'lit' && camera.zoom <= 1) { FRAMING = 'board'; camera.zoom = 1; fit(); renderer.render(scene, camera); } else zoom(1 / size('--zoom-step')); });  // one step out from the lit extent: the whole board
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
  const fr = frameOf(t), lines = ['Node [' + nodeOf(i).join(', ') + ']  (lattice reading)' + (beyond.has(i) ? ', beyond the board: a declared face' : '')];
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
  const shellAt = SHELL_INDEX.get(nodeOf(i).join(','));
  if (shellAt) { const v = lightOf(t, shellAt[0])[shellAt[1]]; lines.push("the light's front of body " + shellAt[0] + ': its own light booked at this shell Node ' + (v === undefined ? 'none in the window at this frame' : format(v))); }
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
  if (name === 'the cone') { const swatch = document.createElement('i'); swatch.className = 'swatch'; swatch.style.borderColor = token('--cone'); swatch.style.background = token('--cone'); label.append(swatch); }
  if (name === CONE_LAYER) for (const c of CLICK_CONES) { if (!c.nodes.length) continue; const swatch = document.createElement('i'); swatch.className = 'swatch'; swatch.style.borderColor = c.tone; swatch.style.background = c.tone; label.append(swatch); }
  label.append(' ' + name + (family ? ' (' + ROLES[family.name].role + (name.endsWith(' glow') ? ', the form D against the frame\\'s own largest' : name.endsWith(' dots') ? ', the count' : '') + ')' : name === 'the cone' ? ' (the run back\\'s reach: the birth\\'s Nodes within the frame\\'s radius of Links, the front\\'s metric with the wrap)' : name === CONE_LAYER ? " (every click's light cone running forward from the Nodes it wrote: within t - t_c + 1 Links at the frame of interval t, the front's metric with the wrap; the legend under the board)" : ''));
  layerBox.append(label);
}

/* The time: one frame per interval, a slider, play; the reading's window marked on the slider. */
const slider = byId('slider'); slider.max = T;
for (const k of BOUNDS) { const mark = document.createElement('span'); mark.style.left = (k / T * 100) + '%'; mark.title = passLabel(k) + ', from the frame at interval ' + INTERVAL(k); byId('bounds').append(mark); }
slider.addEventListener('input', () => { t = Number(slider.value); draw(); });
byId('play').addEventListener('click', () => {
  if (playing) { clearInterval(playing); playing = null; byId('play').textContent = 'Play'; return; }
  if (t >= T) t = 0;
  byId('play').textContent = 'Pause';
  playing = setInterval(() => { if (t >= T) { clearInterval(playing); playing = null; byId('play').textContent = 'Play'; return; } t++; draw(); }, 1000 / size('--frames-per-second'));
});
document.addEventListener('keydown', e => { if (e.target.tagName === 'INPUT' && e.target.type !== 'range') return; if (e.key === 'ArrowRight' && t < T) { t++; draw(); } if (e.key === 'ArrowLeft' && t > 0) { t--; draw(); } });
if (WINDOW && T) { const w = byId('window'); w.hidden = false; w.style.left = (positionOf(WINDOW[0]) / T * 100) + '%'; w.style.width = (Math.max(0, positionOf(WINDOW[1]) - positionOf(WINDOW[0])) / T * 100) + '%'; w.title = 'the reading\\'s window: intervals ' + WINDOW[0] + ' to ' + WINDOW[1]; }

/* The graphs, inline SVG: polylines through the frames' values, nothing between frames. */
const axisLeft = (pad, ...values) => Math.max(pad * 8, pad + Math.max(...values.map(v => format(v).length)) * size('--small') * 0.5);  // the axis's left margin, wide enough for the longest label (2026-10-21: a high of 1,811.855 was clipped at the edge)
const svgText = (text, x, y, anchor) => `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size('--small') * 0.75}" font-family="${esc(token('--font-mono'))}" fill="${token('--muted')}">${esc(text)}</text>`;
function graph(container, title, series, kind, marks, shape) {
  const W = size('--graph-width') * (shape ? shape[0] : 1), H = size('--graph-height') * (shape ? shape[1] : 1), pad = size('--graph-pad'), frames = series[0] ? series[0].values.length : 0;
  let low = Infinity, high = -Infinity;
  for (const s of series) for (const v of s.values) { if (v === null || Number.isNaN(v)) continue; if (v < low) low = v; if (v > high) high = v; }  // a frame without a value is a gap
  if (!series.length || !isFinite(low)) { container.innerHTML = `<div class="caption"><b>${esc(title)}</b><span>nothing to draw</span></div>`; return; }
  if (low === high) { low -= 1; high += 1; }
  const left = axisLeft(pad, low, high);
  const px = i => left + (frames > 1 ? i / (frames - 1) : 0) * (W - left - pad), py = v => pad + (high - v) / (high - low) * (H - 2 * pad);
  let body = `<rect x="${left}" y="${pad}" width="${W - left - pad}" height="${H - 2 * pad}" fill="none" stroke="${token('--line')}"/>`;
  if (low < 0 && high > 0) body += `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}" stroke-dasharray="2 3"/>`;
  body += svgText(format(high), left - 3, pad + size('--small') * 0.3, 'end') + svgText(format(low), left - 3, H - pad, 'end');
  for (const s of series) { const runs = [[]]; Array.from(s.values).forEach((v, i) => { if (v === null || Number.isNaN(v)) { if (runs[runs.length - 1].length) runs.push([]); } else runs[runs.length - 1].push(px(i).toFixed(1) + ',' + py(v).toFixed(1)); }); for (const points of runs) if (points.length) body += `<polyline fill="none" stroke="${s.colour}" stroke-width="${size('--line-width')}" ${s.dashed ? 'stroke-dasharray="5 4"' : ''} stroke-linejoin="round" points="${points.join(' ')}"/>`; }
  if (BOUNDS.length && frames === T + 1) body += BOUNDS.map(k => `<line x1="${px(k).toFixed(1)}" x2="${px(k).toFixed(1)}" y1="${pad}" y2="${H - pad}" stroke="${token('--bound')}" stroke-dasharray="2 3"><title>${passLabel(k)}, from the frame at interval ${INTERVAL(k)}</title></line>`).join('');
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
    const now = g.querySelector('.now'); if (now) now.innerHTML = g.series.map(s => `<span>${esc(s.name)} <b>${s.values[t] === null || Number.isNaN(s.values[t]) ? 'none' : format(s.values[t])}</b></span>`).join('');
  });
}
const seriesOf = (family, name, values, dashed) => ({ name, values, colour: colourOf(family), dashed: !!dashed });
function drawGraphs() {
  const box = byId('graphs'); box.innerHTML = '';
  const at = named ? indexOf(...named) : null, reading = 'lattice reading';
  const add = (title, series) => { const g = document.createElement('div'); g.className = 'graph'; box.append(g); graph(g, title, series, reading); };
  add('The share per family over the lattice, in quanta (the books per interval, LATTICE; the counts per Node summed where the look holds no share)', QUANTA.map(f => seriesOf(f.name, f.name, TOTALS[f.name], ROLES[f.name].dashed)));
  if (CONED) { const g = document.createElement('div'); g.className = 'graph'; box.append(g); graph(g, 'The cone\\'s radius in Links over the frames: down Link by Link on the run back to the birth\\'s Nodes, up on the run forward (the frames\\' cone_radius; none on the run to the first close)', [{ name: 'cone_radius', values: Float64Array.from({ length: T + 1 }, (_, k) => CONE_RADIUS(k) === null ? NaN : CONE_RADIUS(k)), colour: token('--cone'), dashed: false }], 'the run back\\'s reach, the frames\\' word'); }
  if (CLICK_CONES.some(c => c.nodes.length)) { const g = document.createElement('div'); g.className = 'graph'; box.append(g); graph(g, "The clicks' light cones' radius in Links over the frames: t - t_c + 1 from each click's frame on, one Link per interval (the credit lines' intervals; none before the click)", CLICK_CONES.filter(c => c.nodes.length).map(c => ({ name: 'interval ' + format(c.interval) + ', ' + c.line.node_detector + ', ' + c.line.family, values: Float64Array.from({ length: T + 1 }, (_, k) => { const r = coneRadiusAt(c, k); return r === null ? NaN : r; }), colour: c.tone, dashed: false })), "the clicks' light cones, a geometry from the output's lines"); }
  if (at === null) return;
  const over = key => f => seriesOf(f.name, f.name, Float64Array.from({ length: T + 1 }, (_, k) => (frameOf(k)[f.name][key] || [])[at] || 0), ROLES[f.name].dashed);  // frame 0 holds no form
  add('The count at the Node', QUANTA.map(over('count')));
  add('The form at the Node', QUANTA.map(over('form')));
  const entry = BLIND.worlds && typeof BLIND.worlds === 'object' ? BLIND.worlds[String(LOOK.world).replace(/\\.json$/, '')] || BLIND : BLIND;
  const line = typeof entry.line_per_interval === 'number' ? entry.line_per_interval : null, levels = entry.levels && typeof entry.levels === 'object' && !Array.isArray(entry.levels) ? entry.levels : null;
  if (line !== null || levels) addSpectrum(line, levels, QUANTA.map(over('form')));
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
/* The line at the Node (where the blind names a line, `line_per_interval`, or levels, `levels`, in the world's entry or at its root): the discrete transform of the picked Node's form over the frames after the first (frame 0 holds no form) about its mean, the bins 2 pi m / (N every) per interval with every the look's stride and N the frames used, the amplitudes 2 |X_m| / N, one series per family of quanta; the blind's line a dashed mark at its bin, the levels named from the blind, the peak bin of every family above half a level in the caption; no cursor, the graph being over the bins and not the frames. Every number is the look's or the blind's; the page names no world. */
function addSpectrum(line, levels, formSeries) {
  const every = Number(LOOK.every) || 1, used = formSeries.map(s => Array.from(s.values).slice(1));
  const N = used[0] ? used[0].length : 0;
  if (N < 4) return;
  const step = 2 * Math.PI / (N * every), bins = Math.floor(N / 2), four = v => Number(v).toFixed(4);
  const series = formSeries.map((s, j) => {
    const v = used[j], mean = v.reduce((a, b) => a + b, 0) / N, amps = new Float64Array(bins + 1);
    for (let m = 1; m <= bins; m++) { let re = 0, im = 0; for (let k = 0; k < N; k++) { const a = 2 * Math.PI * m * k / N, d = v[k] - mean; re += d * Math.cos(a); im -= d * Math.sin(a); } amps[m] = 2 * Math.hypot(re, im) / N; }
    return { name: s.name, values: amps, colour: s.colour, dashed: s.dashed };
  });
  const marks = (px, py, low, high) => line === null ? '' : `<line x1="${px(line / step).toFixed(1)}" x2="${px(line / step).toFixed(1)}" y1="${py(high).toFixed(1)}" y2="${py(low).toFixed(1)}" stroke="${token('--blind')}" stroke-width="${size('--line-width')}" stroke-dasharray="5 4"><title>the blind\\'s line, ${four(line)} per interval</title></line>`;
  const g = document.createElement('div'); g.className = 'graph'; byId('graphs').append(g);
  graph(g, `The line at the Node: the transform of the form over the frames, the bins ${four(step)} per interval (the blind\\'s line dashed)`, series, 'lattice reading', marks);
  g.querySelectorAll('.cursor').forEach(c => c.remove()); delete g.series;
  const peaks = series.filter(s => Math.max(...s.values) > 0.5).map(s => { let best = 1; for (let m = 2; m < s.values.length; m++) if (s.values[m] > s.values[best]) best = m; return `${esc(s.name)} peaks at ${four(best * step)} per interval (${format(Math.round(s.values[best]))})`; }).join('; ');
  const named = levels ? Object.entries(levels).filter(([, v]) => typeof v === 'number').map(([k, v]) => `${esc(k)} ${four(v)}`).join(', ') : '';
  g.querySelector('.now').innerHTML = (named ? `the blind\\'s levels ${named}; ` : '') + (line !== null ? `the line ${four(line)} per interval, dashed; ` : '') + peaks;
}
const picker = byId('node-picker');
picker.innerHTML = 'Node ' + AXES.map((axis, a) => `<label>${axis} <input type="number" id="node-${axis}" min="${LOW[a]}" max="${HIGH[a] - 1}" value="0"></label>`).join(' ') + ' <span>(click a cube to pick it)</span>';
AXES.forEach(axis => byId('node-' + axis).addEventListener('change', () => { named = AXES.map((a, k) => Math.max(LOW[k], Math.min(HIGH[k] - 1, Number(byId('node-' + a).value) || 0))); drawGraphs(); }));
if (LOOK.bodies.length && LOOK.bodies[0].nodes.length) { named = LOOK.bodies[0].nodes[0].slice(); AXES.forEach((axis, a) => { byId('node-' + axis).value = named[a]; }); }

/* The measurement: with an expectation across an axis, one bar per reporter ordered along it, the rounded shares of what the reporters saw within the window, the expectation (the file's numbers embedded, the sums the page's), the dashed blind curve behind them, the pattern's range, the totals and the watch lines; otherwise the node_detectors' reports as bars, one each, what each saw over W_c up to the frame shown, the dashed blind curve behind them. */
const measurePicker = byId('measure-picker'), select = document.createElement('select'); select.id = 'measure-family';
function drawNodeMeasure() {
  const m = MEASURE, n = m.rounded_shares.length, family = m.family, box = byId('measure'), hex = ROLES[family] ? colourOf(family) : token('--fg');
  byId('measure-box').classList.add('wide');
  measurePicker.textContent = `${[].concat(m.node_detector).join(', ')}, ${family}, within the window ${m.window[0]} to ${m.window[1]}: one bar per reporter across ${m.across} (a group at the coordinate its Nodes share, else a Node)`
    + (m.recorded < m.window[1] ? ` (the look holds intervals 0 to ${m.recorded})` : '');
  const pad = size('--graph-pad'), bottom = pad * 3, H = size('--graph-height') * 2, blind = m.blind.map(v => typeof v === 'number' ? v : null);
  /* The bars' unit (2026-10-21): where the output file carries credit lines at the reporters the bars stand in the record's own unit W_rec, the unit a credit stands in, m.record_shares (the clicks the draw credited within the window, the engine's N in that unit, apportioned by the shares of the click lines: the expectation), and the clicks credited per reporter, m.credited, stand beside them as a second bar, where the draw fell (the sample against the expectation); without credit lines the bars are the rounded shares over the family's wall W_c, N in T's unit, as tools/click_counts.py reads them. */
  const shares = m.record_shares || m.rounded_shares, clicks = m.credited || [], credited = clicks.length > 0, unit = m.record_shares ? "in the record's own unit" : "over W_c, in T's unit";
  const high = Math.max(1, ...shares, ...clicks, ...blind.filter(v => v !== null)), left = axisLeft(pad, high);
  const W = Math.max(size('--graph-width'), left + size('--bar-slot') * n + pad), slot = Math.max(size('--bar-slot'), (W - left - pad) / n);  // the bars fill the chart's width
  const px = k => left + slot * (k + 0.5), py = v => pad + (high - v) / high * (H - pad - bottom);
  const coordinate = k => m.at[k];
  let body = '';
  if (Array.isArray(m.pattern) && m.pattern.length === 2 && n) {
    const [first, last] = m.pattern.map(v => Math.max(0, Math.min(n - 1, v)));
    body += `<rect x="${(px(first) - slot / 2).toFixed(1)}" y="${pad}" width="${(slot * (last - first + 1)).toFixed(1)}" height="${(H - pad - bottom).toFixed(1)}" fill="${token('--window')}"><title>the pattern's range: ${m.across} ${coordinate(first)} to ${coordinate(last)}</title></rect>`;
  }
  body += `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}"/>` + svgText(format(high), left - 3, pad + size('--small') * 0.3, 'end') + svgText('0', left - 3, py(0), 'end');
  const every = Math.max(1, Math.ceil(n / 16)), w = Math.max(1, slot * 0.6);
  shares.forEach((v, k) => {
    const bw = credited ? w / 2 : w;
    body += `<rect x="${(px(k) - w / 2).toFixed(1)}" y="${py(Math.max(0, v)).toFixed(1)}" width="${bw.toFixed(1)}" height="${(py(0) - py(Math.max(0, v))).toFixed(1)}" fill="${hex}"><title>${esc(m.labels[k])}: ${format(v)} by the shares ${unit}, saw ${format(m.seen[k])} of ${format(m.seen.reduce((a, b) => a + Math.max(0, b), 0))}${m.record_shares ? ' (' + format(m.rounded_shares[k]) + ' over W_c)' : ''}${blind[k] === null ? '' : ', the blind ' + format(blind[k])}</title></rect>`;
    if (credited) body += `<rect x="${px(k).toFixed(1)}" y="${py(Math.max(0, clicks[k])).toFixed(1)}" width="${bw.toFixed(1)}" height="${(py(0) - py(Math.max(0, clicks[k]))).toFixed(1)}" fill="${token('--flash')}"><title>${esc(m.labels[k])}: ${format(clicks[k])} clicks credited by the draw</title></rect>`;
    if (k % every === 0 || k === n - 1) body += svgText(coordinate(k), px(k), H - pad, 'middle');
  });
  const hasBlind = blind.some(v => v !== null);
  if (hasBlind && blind.every(v => v !== null)) {
    const points = blind.map((v, k) => px(k).toFixed(1) + ',' + py(v).toFixed(1)).join(' ');
    body += `<polyline fill="none" stroke="${token('--blind')}" stroke-width="${size('--line-width')}" stroke-dasharray="5 4" points="${points}"/>` + svgText('blind', W - pad, pad + size('--small') * 0.3, 'end');
  } else if (hasBlind) {  // a blind with gaps (the which-way folder's rows: none at the channel): one dashed mark per bar where the row carries a count
    blind.forEach((v, k) => { if (v !== null) body += `<line x1="${(px(k) - slot * 0.4).toFixed(1)}" x2="${(px(k) + slot * 0.4).toFixed(1)}" y1="${py(v).toFixed(1)}" y2="${py(v).toFixed(1)}" stroke="${token('--blind')}" stroke-width="${size('--line-width')}" stroke-dasharray="4 3"><title>the blind ${format(v)} at ${esc(m.labels[k])}</title></line>`; });
    body += svgText('blind', W - pad, pad + size('--small') * 0.3, 'end');
  }
  const legend = `<span><i style="border-color:${hex};border-top-width:6px"></i>${esc(family)} the rounded shares per reporter ${unit} (${m.record_shares ? "N the clicks the draw credited within the window, the engine's division act in the record's unit W_rec, apportioned by the shares of the click lines" : "N over the family's wall by the shares of the click lines"}: the expectation)</span>` + (credited ? `<span><i style="border-color:${token('--flash')};border-top-width:6px"></i>the clicks the draw credited per reporter (the output file's credit lines: where the draw fell, the measurement)</span>` : '') + (hasBlind ? `<span><i class="dashed" style="border-color:${token('--blind')}"></i>blind, the expectation file's counts as written</span>` : '') + (Array.isArray(m.pattern) ? `<span><i style="border-color:${token('--window')};border-top-width:6px"></i>the pattern's range</span>` : '');
  box.innerHTML = `<div class="caption"><b>The credit of ${esc(family)} at ${esc([].concat(m.node_detector).join(', '))} across ${esc(m.across)}</b><span>measurement</span></div><div class="legend">${legend}</div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="the node_detectors' credit per reporter">${body}</svg>`;
  byId('totals').textContent = m.totals + (credited ? `; ${format(clicks.reduce((a, b) => a + b, 0))} clicks credited by the draw (the credit lines)` : '');
  byId('watch').innerHTML = m.watch.map(esc).join('<br>');
}
if (!MEASURE) {
  for (const f of QUANTA) { const o = document.createElement('option'); o.value = f.name; o.textContent = f.name; select.append(o); }
  const reporting = QUANTA.find(f => f.name === BLIND.family) || QUANTA.find(f => ROLES[f.name].role === 'light') || QUANTA[0];
  if (reporting) select.value = reporting.name;
  select.addEventListener('change', drawMeasure);
  measurePicker.append('Family ', select, document.createTextNode(WINDOW ? ' within the window ' + WINDOW[0] + ' to ' + WINDOW[1] : ' over every interval'));
}
function reported(node_detector, family) {
  const lines = (reportsAt[node_detector] || {})[family] || [];
  const saw = lines.filter(([k, , p]) => p <= t && (!WINDOW || (k >= WINDOW[0] && k <= WINDOW[1]))).reduce((s, [, inflow]) => s + inflow, 0);
  return WALL[family] ? saw / WALL[family] : saw;
}
function drawMeasure() {
  const family = select.value, node_detectors = LOOK.node_detectors, box = byId('measure');
  const expected = node_detectors.map((d, k) => Array.isArray(BLIND.expected) ? BLIND.expected[k] : BLIND.expected && typeof BLIND.expected === 'object' ? BLIND.expected[d.name] : undefined);
  const counts = node_detectors.map(d => reported(d.name, family));
  const W = size('--graph-width'), H = size('--graph-height') * 1.5, pad = size('--graph-pad'), bottom = pad * 3;
  const high = Math.max(1, ...counts, ...expected.filter(v => typeof v === 'number')), left = axisLeft(pad, high);
  const slot = (W - left - pad) / Math.max(node_detectors.length, 1), py = v => pad + (high - v) / high * (H - pad - bottom);
  let body = `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}"/>` + svgText(format(high), left - 3, pad + size('--small') * 0.3, 'end') + svgText('0', left - 3, py(0), 'end');
  if (expected.some(v => typeof v === 'number')) {
    const points = expected.map((v, k) => typeof v === 'number' ? (left + slot * (k + 0.5)).toFixed(1) + ',' + py(v).toFixed(1) : null).filter(Boolean).join(' ');
    body += `<polyline fill="none" stroke="${token('--blind')}" stroke-width="${size('--line-width')}" stroke-dasharray="5 4" points="${points}"/>` + svgText('blind', W - pad, pad + size('--small') * 0.3, 'end');
  }
  const every = Math.max(1, Math.ceil(node_detectors.length / 12));
  node_detectors.forEach((d, k) => {
    const x = left + slot * (k + 0.5), w = Math.max(1, slot * 0.6);
    body += `<rect x="${(x - w / 2).toFixed(1)}" y="${py(Math.max(0, counts[k])).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(Math.max(0, counts[k]))).toFixed(1)}" fill="${colourOf(family)}"><title>${esc(d.name)}: ${counts[k].toFixed(2)} quanta seen</title></rect>`;  // the bar the region's credit, max(s_R, 0) (ALGEBRA.md, The share's sign and the credit's floor), the saw as it is in the title
    if (k % every === 0) body += svgText(d.name, x, H - pad, 'middle');
  });
  box.innerHTML = `<div class="caption"><b>The reports of ${esc(family)} (what each node_detector saw over W_c)</b><span>measurement</span></div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="the node_detectors' report">${body}</svg>`;
  const watch = BLIND.watch && typeof BLIND.watch === 'object' ? BLIND.watch : null;
  byId('watch').textContent = watch ? `${watch.node_detector}: ${reported(watch.node_detector, family).toFixed(2)} quanta seen, the blind ${format(watch.count)}` : '';
}

/* The world's numbers as the files hold them, and the books at the end. */
function numbers() {
  const row = (k, v) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`;
  const inner = (LOOK.faces || []).map(f => `${f.axis} at ${f.at}, gaps ${f.gaps.map(g => Object.entries(g).map(([k, v]) => k + ' [' + v.join(', ') + ']').join(' ')).join('; ') || 'none'}`).join(' | ') || 'none';
  const receding = Object.entries(LOOK.receding || {}).map(([a, f]) => `${a} ${f.sides.join(' and ')}, the largest ${format(f.largest)}, ${format(f.layers)} layers per growth`).join('; ') || 'none';
  const ended = LOOK.ended ? `at interval ${format(LOOK.ended.interval)}: the front at the ${LOOK.ended.side} face of ${LOOK.ended.axis} at the largest size ${format(LOOK.ended.largest)}` : 'no';
  let html = '<dl>' + row('world', LOOK.world) + row('shape', LOOK.shape.join(' x ') + (X * Y * Z > LOOK.shape[0] * LOOK.shape[1] * LOOK.shape[2] ? ', grown to ' + [X, Y, Z].join(' x ') : '')) + row('boundary', AXES.map(a => a + ' ' + LOOK.boundary[a]).join(', ')) + row('inner faces', inner) + row('receding faces', receding) + row('ended', ended) + row('folded', AXES.filter((a, k) => LOOK.folded[k]).join(', ') || 'none') + row('face depth', LOOK.face_depth)
    + row('Gamma (the Node clock)', format(LOOK.node_clock)) + row('T (the quantum action)', format(LOOK.quantum_action)) + row('the largest integer', LOOK.largest_integer) + row('A (the amplitude bound)', format(LOOK.amplitude_bound))
    + row('intervals', format(LOOK.intervals) + ' recorded; the world declares ' + format(LOOK.declared_intervals))
    + (REACH ? row('the run back\\'s reach', REACH + (SUPPORT.length ? ', the record\\'s light cone about the birth\\'s ' + nodesWord(SUPPORT.length) + supportSpan() : '')) : '') + '</dl>';
  html += '<div class="scroll"><table><thead><tr><th>family</th><th>pair</th><th>holds</th><th>level weight</th><th>parts</th><th>reads</th><th>W_c</th><th>role</th></tr></thead><tbody>'
    + FAMILIES.map(f => `<tr><td>${esc(f.name)}</td><td class="num">[${f.pair.join(', ')}]</td><td>${f.held ? (f.sign ? 'the sign' : 'the content') : 'nothing'}</td><td class="num">${f.level_weight === null ? '' : f.level_weight}</td><td class="num">${f.parts.join(' + ')}</td><td>${f.reads.join(', ')}</td><td class="num">${f.wall === null ? '' : format(f.wall)}</td><td><i class="swatch${ROLES[f.name].dashed ? ' dashed' : ''}" style="border-color:${colourOf(f.name)}"></i> ${ROLES[f.name].role}</td></tr>`).join('') + '</tbody></table></div>';
  html += '<div class="scroll"><table><thead><tr><th>body</th><th>family</th><th>Nodes</th><th>declared count</th>' + (SHELLED.length ? "<th>the light's front</th>" : '') + '</tr></thead><tbody>'
    + LOOK.bodies.map(b => `<tr><td class="num">${b.number}</td><td>${esc(b.family)}</td><td class="num">${b.nodes.length}</td><td class="num">${format(b.declared)}</td>` + (SHELLED.length ? `<td class="num">${Array.isArray(b.shell) && b.shell.length ? nodesWord(b.shell.length) + ' at r = ' + format(b.radius) + ' Links' : ''}</td>` : '') + '</tr>').join('') + '</tbody></table></div>';
  html += '<div class="scroll"><table><thead><tr><th>node_detector</th><th>Nodes</th><th>reads</th></tr></thead><tbody>'
    + LOOK.node_detectors.map(d => `<tr><td>${esc(d.name)}</td><td class="num">${d.body === null ? d.nodes.length : 'the body\\'s'}</td><td>${d.body === null ? 'its Nodes' : 'body ' + d.body}</td></tr>`).join('') + '</tbody></table></div>';
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
  measurePicker.textContent = `${r.node_detector.join(', ')}, ${family}, within the window ${r.window[0]} to ${r.window[1]}: the output file read by tools/click_counts.py, one bar per reporter across ${r.across}`;
  const pad = size('--graph-pad'), bottom = pad * 3, H = size('--graph-height') * 2;
  const clicks = r.clicks ? r.clicks.row : null, blind = (r.blind.counts || []).map(v => typeof v === 'number' ? v : null);
  const high = Math.max(1, ...rs.row, ...(clicks || []), ...blind.filter(v => v !== null)), left = axisLeft(pad, high);
  const W = Math.max(size('--graph-width'), left + size('--bar-slot') * 1.8 * n + pad), slot = Math.max(size('--bar-slot') * 1.8, (W - left - pad) / n);
  const px = k => left + slot * (k + 0.5), py = v => pad + (high - v) / high * (H - pad - bottom), w = Math.max(1, slot * 0.3);
  let body = '';
  if (Array.isArray(BLIND.pattern) && BLIND.pattern.length === 2 && n) {
    const [first, last] = BLIND.pattern.map(v => Math.max(0, Math.min(n - 1, v)));
    body += `<rect x="${(px(first) - slot / 2).toFixed(1)}" y="${pad}" width="${(slot * (last - first + 1)).toFixed(1)}" height="${(H - pad - bottom).toFixed(1)}" fill="${token('--window')}"><title>the pattern's range: ${r.across} ${r.at[first]} to ${r.at[last]}</title></rect>`;
  }
  body += `<line x1="${left}" x2="${W - pad}" y1="${py(0)}" y2="${py(0)}" stroke="${token('--line')}"/>` + svgText(format(high), left - 3, pad + size('--small') * 0.3, 'end') + svgText('0', left - 3, py(0), 'end');
  const every = Math.max(1, Math.ceil(n / 16));
  rs.row.forEach((v, k) => {
    body += `<rect x="${(px(k) - w).toFixed(1)}" y="${py(Math.max(0, v)).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(Math.max(0, v))).toFixed(1)}" fill="${hex}"><title>${esc(r.node_detector[k])}: ${format(v)} by the shares, saw ${format(r.seen[k])}${blind[k] === null ? '' : ', the blind ' + format(blind[k])}</title></rect>`;
    if (clicks) body += `<rect x="${px(k).toFixed(1)}" y="${py(Math.max(0, clicks[k])).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(Math.max(0, clicks[k]))).toFixed(1)}" fill="${flash}"><title>${esc(r.node_detector[k])}: ${format(clicks[k])} clicks credited by the draw</title></rect>`;
    if (k % every === 0 || k === n - 1) body += svgText(r.at[k], px(k), H - pad, 'middle');
  });
  if (blind.some(v => v !== null)) {
    const points = blind.map((v, k) => v === null ? null : px(k).toFixed(1) + ',' + py(v).toFixed(1)).filter(Boolean).join(' ');
    body += `<polyline fill="none" stroke="${token('--blind')}" stroke-width="${size('--line-width')}" stroke-dasharray="5 4" points="${points}"/>` + svgText('blind', W - pad, pad + size('--small') * 0.3, 'end');
  }
  const legend = `<span><i style="border-color:${hex};border-top-width:6px"></i>${esc(family)}, the rounded shares per reporter (N by the shares of the output file's click lines, the expectation)</span>` + (clicks ? `<span><i style="border-color:${flash};border-top-width:6px"></i>the clicks the draw credited (the credit lines, the measurement)</span>` : '') + `<span><i class="dashed" style="border-color:${token('--blind')}"></i>blind</span>` + (Array.isArray(BLIND.pattern) ? `<span><i style="border-color:${token('--window')};border-top-width:6px"></i>the pattern's range</span>` : '');
  box.innerHTML = `<div class="caption"><b>The output file's credit of ${esc(family)} at ${format(n)} reporters across ${esc(r.across)}, beside the blind</b><span>measurement</span></div><div class="legend">${legend}</div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="the reading's bars beside the blind">${body}</svg>`;
  const credited = clicks ? clicks.reduce((a, b) => a + b, 0) : null;
  byId('totals').textContent = `N ${format(r.quanta)} by the shares (the blind ${format(r.blind_quanta)}); ` + (clicks ? `${format(credited)} clicks credited by the draw` : 'no draw declared, no click credited') + `; laid ${format(r.laid)}, elsewhere ${format(r.elsewhere)}` + (r.floored ? '; a region floored at 0' : '');
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

/* The records' clicks: for each record declared a NodeDetector (a body with credit lines in the output file) the part it stands in over the intervals, from its credit lines (the part before and the part realised at each absorption, the first line's `before` the part it started in), one step series per record, and the credit lines themselves in one table; the measurement, the engine's own lines. */
function drawRecords() {
  if (!DETECTOR_BODIES.length && !REGION_CREDITS.length) return;
  const box = byId('records'); box.innerHTML = ''; byId('records-box').hidden = false;
  const names = [], rows = [], byPosition = (a, b) => positionOfLine(a) - positionOfLine(b) || a.interval - b.interval;
  const WORDS = ['order', 'scale', 'board_count', 'into', 'senses', ...OWN_LIGHT_WORDS].filter(word => OUTPUT.lines.some(line => (line.event === 'credit' || line.event === 'conversion') && line[word] !== undefined));  // `into` and `senses` the conversion line's two words (2026-10-21); the own light's words where a bound body's close writes them (2026-10-22)  // a side of a record of several parts names its order, the record's scale after its write and the count read from the board on the line
  const bookOf = line => {  // the frames' word on a bound body's own light at the close (2026-10-22): the close's own words of the frame's own_light row at the line's frame where the books carry them, else the running book's sum at the last frame before the close holding one (the close's own interval is booked and begun again inside the act)
    if (!bodyLine(line) || !SHELLED.some(b => 'body ' + b.number === line.node_detector)) return '';
    const number = Number(String(line.node_detector).slice(5)), k = Math.min(positionOfLine(line), T), own = LOOK.frames[k].own_light, at = own && own[String(number)];
    const words = closedShare(at) ? Object.entries(at).filter(([key, v]) => key !== 'light' && key !== 'carry' && v !== null && (typeof v !== 'object' || Array.isArray(v))).map(([key, v]) => key + ' ' + (Array.isArray(v) ? '[' + v.map(format).join(', ') + ']' : format(v))) : [];
    if (words.length) return words.join(', ');
    for (let j = k; j >= 0; j--) { const light = lightOf(j, number); if (light.length) return 'the book ' + format(light.reduce((a, v) => a + v, 0)) + ' at the frame of interval ' + format(INTERVAL(j)); }
    return '';
  };
  const row = (line, record) => [line.interval, ...(PASSES > 1 ? [passLabel(positionOfLine(line))] : []), record, line.family, line.window ? line.window.join(' to ') : '', line.proper, line.before, line.realised, line.count, line.left, line.taken, line.given, ...WORDS.map(word => Array.isArray(line[word]) ? line[word].join(' ') : line[word]), ...(SHELLED.length ? [bookOf(line)] : []), line.label];
  for (const n of DETECTOR_BODIES) {
    const lines = (RECORD_CREDITS['body ' + n] || []).slice().sort(byPosition), body = LOOK.bodies[n];
    const parts = []; for (const line of lines) for (const part of [line.before, line.realised]) if (part !== null && part !== undefined && !parts.includes(part)) parts.push(part);
    let part = lines.length ? lines[0].before : null, next = 0;
    const values = new Float64Array(T + 1), labels = [];
    for (let k = 0; k <= T; k++) { while (next < lines.length && positionOfLine(lines[next]) <= k) { if (lines[next].count && lines[next].realised !== null) part = lines[next].realised; next++; } values[k] = part === null ? 0 : parts.indexOf(part); }
    const g = document.createElement('div'); g.className = 'graph'; box.append(g);
    graph(g, `body ${n} (${esc(body.family)} at the Nodes ${body.nodes.map(node => '[' + node.join(', ') + ']').join(' ')}): ${lines.length ? 'the part it stands in, ' + parts.map((p, k) => k + ' = ' + p).join(', ') : 'no click: it stands in the part it was laid in'}`, [{ name: 'the part, from the credit lines', values, colour: colourOf(body.family), dashed: false }], 'measurement, the credit lines', (px, py, low, high) => lines.filter(line => line.count).map(line => `<line x1="${px(positionOfLine(line)).toFixed(1)}" x2="${px(positionOfLine(line)).toFixed(1)}" y1="${py(high).toFixed(1)}" y2="${py(low).toFixed(1)}" stroke="${token('--flash')}" stroke-dasharray="3 2"><title>interval ${line.interval}: ${line.before} to ${line.realised}</title></line>`).join(''), [size('--arrival-width'), 1]);
    for (const line of lines) rows.push(row(line, 'body ' + n));
  }
  for (const line of REGION_CREDITS.slice().sort(byPosition)) rows.push(row(line, line.node_detector));
  for (const b of SHELLED) {  // a bound body's own light through its light's front: the book's sum over the shell and the carry per frame
    const sums = Float64Array.from({ length: T + 1 }, (_, k) => { const light = lightOf(k, b.number); return light.length ? light.reduce((a, v) => a + v, 0) : NaN; }), carries = Float64Array.from({ length: T + 1 }, (_, k) => { const c = carryOf(k, b.number); return c === null ? NaN : c; });
    const closes = Float64Array.from({ length: T + 1 }, (_, k) => { const own = LOOK.frames[k].own_light, row = own && own[String(b.number)]; return row && typeof row.closed_light === 'number' ? row.closed_light : NaN; });
    if (![...sums, ...carries, ...closes].some(v => !Number.isNaN(v))) continue;
    const g = document.createElement('div'); g.className = 'graph'; box.append(g);
    graph(g, `body ${b.number} (${esc(b.family)}): its own light through the light's front, the book's sum over the ${format(b.shell.length)} shell Nodes at r = ${format(b.radius)} Links per frame (the frames' own_light, the window's running sum outward positive in G^2, begun again at each close: a gap at the close's frame), the carry below one quantum and the window's total at the last close`, [{ name: "the book's sum over the shell", values: sums, colour: token('--shell'), dashed: false }, { name: 'the carry', values: carries, colour: token('--shell'), dashed: true }, { name: "the window's total at the last close (closed_light)", values: closes, colour: token('--flash'), dashed: true }], 'lattice reading, the books', null, [size('--arrival-width'), 1]);
  }
  const fronts = {};  // the erasure lines per front, its family and its origin (the click's Node), each front one line in the tone of its click
  for (const shells of Object.values(FRONTS_AT)) for (const line of shells) { const key = line.family + '|' + (line.origin || []).join(','); (fronts[key] || (fronts[key] = [])).push(line); }
  if (Object.keys(fronts).length) {
    const series = Object.entries(fronts).map(([key, lines]) => {
      const [family, origin] = key.split('|'), first = Math.min(...lines.map(line => Number(line.interval))), click = CLICK_CONES.find(c => c.interval + 1 === first && c.nodes.some(at => at.join(',') === origin));
      const take = new Float64Array(T + 1).fill(NaN), distance = new Float64Array(T + 1).fill(NaN);
      for (const line of lines) { const k = positionOfLine(line); if (k > T) continue; take[k] = (Number.isNaN(take[k]) ? 0 : take[k]) + (line.unit ? (line.take || 0) / line.unit : line.take || 0); distance[k] = Math.max(Number.isNaN(distance[k]) ? 0 : distance[k], line.distance || 0); }
      return { name: `from [${origin.split(',').join(', ')}], ${family}, since interval ${format(first)}` + (click ? ` (the click at ${format(click.interval)})` : ''), colour: click ? click.tone : token('--front'), take, distance };
    });
    for (const [title, key] of [["The fronts' erasure: the record's share standing on the shell as the front reaches it, per interval and per front, in quanta (the erasure lines' take over the record's unit)", 'take'], ["The fronts' distance from their origin per interval, in Links (the erasure lines), one Link per interval", 'distance']]) {
      const g = document.createElement('div'); g.className = 'graph'; box.append(g);
      graph(g, title, series.map(s => ({ name: s.name, values: s[key], colour: s.colour, dashed: false })), "lattice reading, the fronts' shells", null, [size('--arrival-width'), 1]);
    }
  }
  byId('credits').innerHTML = (SHELLED.length ? '<p class="lines">The own light column (a bound body, the frames): the close\\'s own words of the frame\\'s own_light row at the line\\'s frame where the books carry them, else the running book\\'s sum at the last frame before the close holding one (the close\\'s own interval is booked and begun again inside the act, so the exact outflow at the close is the credit line\\'s word where it carries one).</p>' : '') + '<table><thead><tr>' + ['interval', ...(PASSES > 1 ? ['pass'] : []), 'record', 'family', 'window', 'proper time', 'before', 'realised', 'count moved', 'count left', 'taken from', 'given to', ...WORDS, ...(SHELLED.length ? ['own light (the frames)'] : []), 'label'].map(h => `<th>${h}</th>`).join('') + '</tr></thead><tbody>' + rows.sort((a, b) => a[0] - b[0]).map(cells => '<tr>' + cells.map(c => `<td class="num">${esc(c === null || c === undefined ? '' : c)}</td>`).join('') + '</tr>').join('') + '</tbody></table>';
}
/* The clicks' legend under the board (2026-10-22): one row per click line of the output with the swatch of its cone's tone, its kind (named from the line's own words), its interval and pass, the Nodes it wrote and the lines they are read from, the count moved and left, the window and the proper time, the credit's words (momentum, source, recoil, lost, the count on the board, the own light's words where the close writes them) and, at the frame shown, its cone's radius in Links with the Nodes inside it; every number the output's. */
function drawClicks() {
  const box = byId('clicks'); box.innerHTML = '';
  if (!CLICK_CONES.length) return;
  const heading = document.createElement('div'); heading.className = 'heading';
  heading.innerHTML = "<b>The clicks and their light cones</b>: every credit line of the output a click (the one act at the window's close), its cone the Nodes within t - t_c + 1 Links of the Nodes it wrote at the frame of interval t, the Link metric with the wrap as the run back's cone is shaded (the dependency radius one Link per interval, the pace of light on the board 1 / sqrt 3 Links per interval inside it), a geometry from the click line's Node and interval and nothing of the engine's, the latest click's cone brightest; the Nodes read from the lay and face lines beside the line, which itself names none (the law's No click names a Node), and where two clicks of one family fall at one interval the page gives their lines to the first.";
  box.append(heading);
  const span = nodes => [0, 1, 2].filter(a => LOOK.shape[a] > 1).map(a => AXES[a] + ' ' + format(Math.min(...nodes.map(n => n[a]))) + ' to ' + format(Math.max(...nodes.map(n => n[a])))).join(', ');
  for (const c of CLICK_CONES) {
    const l = c.line, row = document.createElement('div'); row.className = 'row';
    const where = (c.nodes.length ? 'at ' + (c.nodes.length === 1 ? 'the Node [' + c.nodes[0].join(', ') + ']' : nodesWord(c.nodes.length) + ' (' + span(c.nodes) + ')') + ' (' + c.from.join('; ') + ')' : "no Node written beside the line in the output (the quantum passed in the books, or the write stands at the birth as the run back's cone draws it): no cone") + (c.exchange.length && c.nodes.length && c.from.every(f => !f.includes('of the record itself')) ? '; the exchange written over the record at ' + (c.exchangeNodes.length === 1 ? 'the Node [' + c.exchangeNodes[0].join(', ') + ']' : nodesWord(c.exchangeNodes.length) + ' (' + span(c.exchangeNodes) + ')') + ' (' + c.exchange.length + ' lay lines)' : '');
    const words = [
      'count moved ' + format(l.count) + (l.left === null || l.left === undefined ? '' : ', left ' + format(l.left)),
      Array.isArray(l.window) ? 'window ' + l.window.join(' to ') + (l.proper === undefined || l.proper === null ? '' : ', proper time ' + format(l.proper)) + (l.windows ? ', the ' + ordinal(l.windows) + ' window' : '') : '',
      Array.isArray(l.momentum) ? 'momentum [' + l.momentum.map(format).join(', ') + ']' : '',
      l.source ? 'source ' + l.source : '',
      l.recoil !== null && l.recoil !== undefined ? 'recoil ' + (Array.isArray(l.recoil) ? '[' + l.recoil.map(format).join(', ') + ']' : l.recoil) : '',
      Array.isArray(l.lost) && l.lost.length ? 'lost: ' + l.lost.join('; ') : '',
      l.board_count !== undefined && l.board_count !== null ? 'the count on the board ' + format(l.board_count) : '',
      ...ownLightOf(l).map(word => word + ' ' + (Array.isArray(l[word]) ? '[' + l[word].map(format).join(', ') + ']' : format(l[word]))),
    ].filter(Boolean).join('; ');
    row.innerHTML = `<i class="swatch" style="border-color:${c.tone};background:${c.nodes.length ? c.tone : 'transparent'}"></i> <b>interval ${format(l.interval)}</b>` + (PASSES > 1 ? ' (' + esc(passLabel(c.position)) + ')' : '') + ' ' + esc(kindOf(c)) + ' ' + esc(where) + '; ' + esc(words) + '. <span class="now"></span>';
    c.now = row.querySelector('.now');
    box.append(row);
  }
}
function clicksNow() {  // the frame's word on each click's cone
  for (const c of CLICK_CONES) { if (!c.now) continue; const radius = coneRadiusAt(c, t); c.now.textContent = radius === null ? (c.nodes.length ? 'no cone at this frame (before its click)' : '') : 'its cone ' + linksWord(radius) + ' at this frame, ' + nodesWord(clickCount(c, t)) + ' inside it'; }
}

/* The arrival: with an expectation across an axis, the reporters' inflow per interval (their click lines summed, the negative ones included, in quanta over the family's wall) and the quanta gathered within the window up to each interval; the blind's peak, centroid and span marked where the blind names an arrival, the blind's total where it names one; the measurement over the intervals. */
function drawArrival() {
  const m = READ ? { labels: READ.node_detector, family: READ.family, window: READ.window } : MEASURE, box = byId('arrival'); box.innerHTML = ''; byId('arrival-box').hidden = false;
  const wall = WALL[m.family] || 1, per = new Float64Array(T + 1), gathered = new Float64Array(T + 1), hex = ROLES[m.family] ? colourOf(m.family) : token('--fg');
  for (const name of m.labels) for (const [, inflow, p] of (reportsAt[name] || {})[m.family] || []) if (p <= T) per[p] += inflow / wall;
  let sum = 0;
  for (let k = 0; k <= T; k++) { if (INTERVAL(k) >= m.window[0] && INTERVAL(k) <= m.window[1]) sum += per[k]; gathered[k] = sum; }
  const arrival = BLIND.arrival && typeof BLIND.arrival === 'object' ? BLIND.arrival : null, total = Number(BLIND.quanta !== undefined ? BLIND.quanta : BLIND.through);
  const marks = (px, py, low, high) => {
    let body = '';
    if (!arrival) return body;
    if (Array.isArray(arrival.span) && arrival.span.length === 2) body += `<rect x="${px(positionOf(arrival.span[0])).toFixed(1)}" y="${py(high).toFixed(1)}" width="${(px(positionOf(arrival.span[1])) - px(positionOf(arrival.span[0]))).toFixed(1)}" height="${(py(low) - py(high)).toFixed(1)}" fill="${token('--window')}"><title>the blind span, intervals ${arrival.span[0]} to ${arrival.span[1]}</title></rect>`;
    [['peak', '5 4'], ['centroid', '2 3']].forEach(([key, dash], k) => { if (typeof arrival[key] !== 'number') return; body += `<line x1="${px(positionOf(arrival[key])).toFixed(1)}" x2="${px(positionOf(arrival[key])).toFixed(1)}" y1="${py(high).toFixed(1)}" y2="${py(low).toFixed(1)}" stroke="${token('--blind')}" stroke-dasharray="${dash}"><title>the blind ${key}, interval ${arrival[key]}</title></line>` + svgText('blind ' + key + ' ' + format(arrival[key]), px(positionOf(arrival[key])) + 2, py(high) + size('--small') * (0.75 + 0.85 * k), 'start'); });
    return body;
  };
  const line = (px, py, low, high) => isFinite(total) && total >= low && total <= high ? `<line x1="${px(0).toFixed(1)}" x2="${px(T).toFixed(1)}" y1="${py(total).toFixed(1)}" y2="${py(total).toFixed(1)}" stroke="${token('--blind')}" stroke-dasharray="5 4"><title>the blind total ${format(total)}</title></line>` + svgText('blind ' + format(total), px(T), py(total) - 2 < size('--small') ? py(total) + size('--small') : py(total) - 2, 'end') : '';  // the label under the line where the line stands at the top, inside the chart (2026-10-21)
  const add = (title, name, values, extra) => { const g = document.createElement('div'); g.className = 'graph'; box.append(g); graph(g, title, [{ name, values, colour: hex, dashed: false }], 'measurement', extra, [size('--arrival-width'), size('--arrival-height')]); };
  add(`The inflow of ${m.family} at the ${m.labels.length} reporters per interval, in quanta over W_c ${format(wall)}`, "the reporters' click lines summed", per, marks);
  add(`The quanta gathered within the window ${m.window[0]} to ${m.window[1]}, up to each interval`, 'N so far, the inflow over W_c', gathered, line);
  if (OUTPUT) {
    const credited = new Float64Array(T + 1);
    for (const name of m.labels) for (const [, count, p] of CREDITS_AT[name] || []) if (p <= T) credited[p] += count;
    for (let k = 1; k <= T; k++) credited[k] += credited[k - 1];
    if (credited[T]) add(`The clicks the draw credited at the ${m.labels.length} reporters, up to each interval (the credit lines)`, 'clicks credited so far', credited, line);
    const density = new Float64Array(T + 1), at = DENSITY_AT[m.family] || {};
    for (const name of m.labels) { let last = 0, next = 0; const changes = at[name] || []; for (let k = 0; k <= T; k++) { while (next < changes.length && changes[next][2] <= k) { last = changes[next][1] === null ? last : changes[next][1]; next++; } density[k] += last; } }
    const g = document.createElement('div'); g.className = 'graph'; box.append(g);
    graph(g, `The density of ${m.family} over the ${m.labels.length} reporters\u2019 Nodes per interval, in quanta (the density lines)`, [{ name: 'LATTICE, the share at the regions, a diagnostic and no click', values: density, colour: token('--field'), dashed: true }], 'lattice reading', null, [size('--arrival-width'), size('--arrival-height')]);
  }
  moveCursors();
}

/* The notes (--notes, 2026-10-21): a Markdown text rendered as one prose section, its first heading the section's, its other headings, paragraphs, numbered and bulleted lists, `code` and **bold**; escaped, nothing computed, nothing decided. */
function drawNotes() {
  if (typeof NOTES !== 'string' || !NOTES.trim()) return;
  const inline = text => esc(text).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\\*\\*([^*]+)\\*\\*/g, '<b>$1</b>');
  const box = byId('notes'); box.innerHTML = ''; byId('notes-box').hidden = false;
  let heading = null, paragraph = [], list = null, listKind = null;
  const flushParagraph = () => { if (paragraph.length) { const p = document.createElement('p'); p.innerHTML = inline(paragraph.join(' ')); box.append(p); paragraph = []; } };
  const flushList = () => { if (list) { box.append(list); list = null; listKind = null; } };
  for (const raw of NOTES.split(/\\r?\\n/)) {
    const line = raw.trim();
    const head = /^(#{1,3})\\s+(.*)$/.exec(line), item = /^(\\d+)\\.\\s+(.*)$/.exec(line), bullet = /^[-*]\\s+(.*)$/.exec(line);
    if (!line) { flushParagraph(); flushList(); continue; }
    if (head) {
      flushParagraph(); flushList();
      if (head[1].length === 1 && heading === null) { heading = head[2]; byId('notes-heading').innerHTML = inline(heading); continue; }
      const h = document.createElement(head[1].length <= 2 ? 'h3' : 'h4'); h.innerHTML = inline(head[2]); box.append(h); continue;
    }
    if (item || bullet) {
      flushParagraph();
      const kind = item ? 'ol' : 'ul';
      if (!list || listKind !== kind) { flushList(); list = document.createElement(kind); listKind = kind; }
      const li = document.createElement('li'); li.innerHTML = inline(item ? item[2] : bullet[1]); list.append(li); continue;
    }
    if (list && /^\\s/.test(raw) && list.lastElementChild) { list.lastElementChild.innerHTML += ' ' + inline(line); continue; }
    flushList(); paragraph.push(line);
  }
  flushParagraph(); flushList();
}
{{GATE_SCRIPT}}/* The start: the title, the verdict, frame 0. */
byId('title').textContent = document.title;
byId('verdict').textContent = LOOK.verdict + (LOOK.reason ? ': ' + LOOK.reason : '') + ' (' + LOOK.label + ')';
const biasBound = () => { const pairs = OUTPUT ? OUTPUT.lines.filter(l => l.event === 'credit' && l.bias_bound && l.bias_bound.g && l.bias_bound.total).map(l => [Number(l.bias_bound.g), Number(l.bias_bound.total)]) : []; if (!pairs.length) return ''; const [g, T] = pairs.reduce((a, b) => a[0] * b[1] >= b[0] * a[1] ? a : b); const gcd = (x, y) => y ? gcd(y, x % y) : x, d = gcd(g, T); return `, the bias bound ${format(g / d)} / ${format(T / d)} on the click's line (the worst over the ${format(pairs.length)} credits carrying one)`; };  // the totals' bias as the credit lines carry it (ALGEBRA.md, The digits' base and a total's factors)
byId('source').textContent = OUTPUT ? `the output file: ${OUTPUT.verdict}, ${format(OUTPUT.intervals)} intervals, ${format(CLICKS.length)} click lines, ${format(OUTPUT.lines.filter(l => l.event === 'credit').length)} credit, ${format(Object.keys(HOLES_AT).length)} hole, ${format(Object.keys(FACES_AT).length)} face and ${format(Object.keys(FRONTS_AT).length)} front intervals` + (MEASURE ? '' : biasBound()) + (SAME_LINES ? ', the look\u2019s click lines the same' : LOOK.every > 1 && LOOK_CLICKS.every(line => CLICKS.some(other => key(other) === key(line))) ? `, the look strided to every ${ordinal(LOOK.every)} interval holding ${format(LOOK_CLICKS.length)} of them` : `, the look\u2019s ${format(LOOK_CLICKS.length)} click lines DIFFER`) : 'no output file given: the measurement from the look\u2019s own lines';
if (!MEASURE && !READ && !LOOK.node_detectors.some(d => d.body === null && d.name !== 'face')) byId('measure-box').hidden = true;  // no declared region reports: nothing to bar
function start() { themed(); fit(); numbers(); blindTable(); drawGraphs(); drawRecords(); drawClicks(); drawNotes(); if (READ) { drawReading(); drawArrival(); } else if (MEASURE) { drawNodeMeasure(); drawArrival(); } draw(); }
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
const SIDES = Object.keys(BLIND.sides), NAME = String(BLIND.combination.name), GATE_FAMILY = String(BLIND.family), PLANE_FAMILY = FAMILIES.some(f => f.name === GATE_FAMILY && f.plane);
const SIDE_TONES = ['--matter', '--light', '--field', '--flash', '--ring'], CREDITS = ['by_the_parts_shares', 'by_the_local_sums', 'by_the_sign'];
const sideColour = k => token(SIDE_TONES[k % SIDE_TONES.length]), gateHex = () => ROLES[GATE_FAMILY] ? colourOf(GATE_FAMILY) : token('--fg');
const frac = v => v === null || v === undefined ? 'none' : v[1] === 1 ? format(v[0]) : format(v[0]) + ' / ' + format(v[1]);
const ratio = v => v === null || v === undefined ? NaN : v[0] / v[1];
const same = (u, v) => u !== null && u !== undefined && v !== null && v !== undefined && u[0] === v[0] && u[1] === v[1];
const verdictOf = (u, v) => u === null || u === undefined || v === null || v === undefined ? 'none' : same(u, v) ? 'MATCH' : 'differs';  // none where the run read nothing (the joint form's rows where the sides read in different windows) or the blind predicts nothing (a row not read)
const port = key => String(key).split(' ').map(p => p === 'plus' ? '+' : p === 'minus' ? '\u2212' : p).join(' ');
const regionOf = label => LOOK.node_detectors.find(d => d.name === BLIND.sides[label]) || { name: String(BLIND.sides[label]), nodes: [], body: null };
const clickedAt = (frame, name) => frame.lines.some(line => line.event === 'click' && line.node_detector === name && line.family === GATE_FAMILY);
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
  if (CONED && layers['the cone'].on && CONE_RADIUS(t) !== null) for (let i = 0; i < N; i++) if (inCone(i, t)) { const n = nodeOf(i); body += `<rect x="${px(n[U])}" y="${py(n[V])}" width="1" height="1" fill="${token('--cone')}" fill-opacity="${size('--cone-above')}"/>`; }  // the record's cone, the run back's reach
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
  body += `<text x="${s[U] - 0.3}" y="${s[V] - letter * 0.4}" text-anchor="end" font-size="${letter}" font-family="${esc(token('--font-mono'))}" fill="${token('--muted')}">${AXES[U]}</text><text x="0.3" y="${letter}" font-size="${letter}" font-family="${esc(token('--font-mono'))}" fill="${token('--muted')}">${AXES[V]}</text>`;
  const title = t === 0 ? `The input as laid: ${esc(GATE_FAMILY)}'s record at its Nodes and the ${SIDES.length} regions` : `Interval ${INTERVAL(t)}: the beams of ${esc(GATE_FAMILY)} and the ${SIDES.length} regions` + (CONED && CONE_RADIUS(t) !== null ? `, the record's cone of ${format(CONE_RADIUS(t))} Links shaded` : '');
  byId('gate-above').innerHTML = `<div class="caption"><b>${title}</b><span>Lattice reading, a diagnostic</span></div><svg viewBox="0 0 ${s[U]} ${s[V]}" role="img" aria-label="the board from above" shape-rendering="crispEdges" style="max-height: var(--board-height)">${body}</svg><div class="caption"><span>${AXES[U]} across, ${AXES[V]} up; a Node's count of ${esc(GATE_FAMILY)} as the cell's depth against the frame's largest (a hollow cell a count below 0); the box the frame's own, ${s[U]} x ${s[V]} at the file's coordinates from (${left}, ${o[V]})</span></div>`;
}
function sidesList() {
  const family = FAMILIES.find(f => f.name === GATE_FAMILY), rows = SIDES.map((label, k) => {
    const region = regionOf(label), basis = WORLD.bases[label] || [], pattern = WORLD.patterns[label] || [];
    return `<dt style="color:${sideColour(k)}">${esc(label)}</dt><dd>${esc(region.name)}, ${format(region.nodes.length)} Nodes: the setting (p, q) = (${basis.map(format).join(', ')}), the pattern ${pattern.map(part => '[' + part.map(format).join(', ') + ']').join(' ')}</dd>`;
  });
  byId('gate-sides').innerHTML = `<dl>${rows.join('')}<dt>record</dt><dd>${esc(GATE_FAMILY)}, ${family ? format(family.lines / (family.plane ? 2 : 1)) + ' parts' + (family.plane ? ' of a plane each' : '') + ' laid alike' : 'not in the look'}; frame 0 the world as laid</dd><dt>declared</dt><dd>the settings and the patterns are the world file's, read by the reader (${esc(WORLD.world)}) and by nothing in the engine; the regions' Nodes are the file's</dd></dl>`;
}

/* The parts lines: per region the parts' signed level sums (now) over the intervals, the parts overlaid, and a strip of its click lines. */
const PARTS_AT = {};
for (const frame of LOOK.frames) for (const line of frame.lines) if (line.event === 'parts' && line.family === GATE_FAMILY) (PARTS_AT[line.node_detector] || (PARTS_AT[line.node_detector] = {}))[line.interval] = line.levels;
function drawParts() {
  const box = byId('gate-parts'); box.innerHTML = '';
  SIDES.forEach((label, k) => {
    const region = regionOf(label), at = PARTS_AT[region.name] || {}, rows = Math.max(0, ...Object.values(at).map(levels => levels.length)), width = PLANE_FAMILY ? 2 : 1, parts = Math.floor(rows / width);
    const series = Array.from({ length: rows }, (_, p) => ({ name: label + ' part ' + (Math.floor(p / width) + 1) + (width > 1 ? (p % 2 ? ' im' : ' re') : ''), colour: sideColour(k), dashed: p > 0, values: Float64Array.from({ length: T + 1 }, (_, i) => at[INTERVAL(i)] && at[INTERVAL(i)][p] ? at[INTERVAL(i)][p][0] : 0) }));
    const g = document.createElement('div'); g.className = 'graph'; box.append(g);
    graph(g, `The parts at ${region.name} (${label}): ${parts} parts${width > 1 ? ' of a plane, re and im,' : ''} overlaid, the sums now`, series, "the parts lines, the NodeDetector's read");
    const clicks = (reportsAt[region.name] || {})[GATE_FAMILY] || [];
    if (!g.dataset.px) return;
    const [left, right, frames] = JSON.parse(g.dataset.px), W = size('--graph-width'), h = size('--graph-pad') * 4, px = i => left + (frames > 1 ? i / (frames - 1) : 0) * (right - left);
    const marks = clicks.map(([interval, inflow, p]) => `<line x1="${px(p).toFixed(1)}" x2="${px(p).toFixed(1)}" y1="0" y2="${h - size('--small')}" stroke="${token('--flash')}" stroke-width="1"><title>click at interval ${interval}: the inflow ${format(inflow)}</title></line>`).join('');
    g.insertAdjacentHTML('beforeend', `<svg viewBox="0 0 ${W} ${h}" role="img" aria-label="the click lines of ${esc(region.name)}">${marks}${svgText(format(clicks.length) + ' click lines of ' + region.name + ' (the measurement)', right, h - size('--graph-pad'), 'end')}</svg>`);
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
    body += `<rect x="${(x - w).toFixed(1)}" y="${py(Math.max(0, rv)).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(Math.max(0, rv))).toFixed(1)}" fill="${gateHex()}"><title>${port(key)}: the run's share ${frac(run)}, J = ${frac(WORLD.joint[key])}</title></rect>`;
    if (expected) body += `<rect x="${x.toFixed(1)}" y="${py(Math.max(0, ratio(expected))).toFixed(1)}" width="${w.toFixed(1)}" height="${(py(0) - py(Math.max(0, ratio(expected)))).toFixed(1)}" fill="none" stroke="${token('--blind')}" stroke-dasharray="3 2"><title>${port(key)}: the blind's share ${frac(expected)}</title></rect>`;
    body += svgText(port(key), x, H - bottom + small * 1.2, 'middle') + svgText(frac(run), x, H - bottom + small * 2.4, 'middle') + (expected ? svgText('blind ' + frac(expected), x, H - bottom + small * 3.6, 'middle') : '') + (key === drawn ? svgText('drawn: the click', x, H - bottom + small * 4.8, 'middle') : '');
  });
  const identical = n > 0 && keys.every(key => same(WORLD.shares[key], blind[key]));
  const legend = `<span><i style="border-color:${gateHex()};border-top-width:6px"></i>the joint form's shares J over their sum (the gate's arithmetic over both sides' lines; none where the sides read in different windows)</span><span><i class="dashed" style="border-color:${token('--blind')}"></i>the blind's shares</span><span>drawn: the ports the sides' clicks realised, one after another</span>`;
  return `<div class="graph"><div class="caption"><b>The ${n} joint shares at (${esc(KEY)}): ${identical ? 'the blind\u2019s exactly' : 'the run beside the blind'}</b><span>the joint form's shares, the gate's arithmetic over the parts lines</span></div><div class="legend">${legend}</div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="the joint shares beside the blind" style="max-width: var(--measure-width)">${body}</svg></div>`;
}
function worldTable() {
  const branch = WORLD.branch || null, realised = branch && branch.realised ? Object.entries(branch.realised).map(([label, p]) => label + ' = ' + port(p)).join(', ') : '';
  const rows = [[branch ? `E_${SIDES.length} on the realised branch (${realised}; the gate's E, the last side ${branch.last} read where the record stands)` : `E_${SIDES.length}, the correlation over the ${SIDES.length} sides`, WORLD.correlation, (EXPECTED.correlation || {})[KEY]]];
  if (branch && branch.shares) for (const p of Object.keys(branch.shares)) rows.push([`the share of ${branch.last} at ${port(p)} on the branch (its local read, the realised term where it stands)`, branch.shares[p], null]);
  if (WORLD.correlation_by_the_joint_shares !== undefined) rows.push([`E_${SIDES.length} by the joint form over both sides' lines (the gate's arithmetic, a diagnostic; none where the sides read in different windows)`, WORLD.correlation_by_the_joint_shares, (EXPECTED.correlation || {})[KEY]]);
  for (const label of SIDES) rows.push([`the marginal P(+) of ${label} (${regionOf(label).name})`, (WORLD.marginals || {})[label], ((EXPECTED.marginals || {})[KEY] || {})[label]]);
  for (const [subset, e] of Object.entries(WORLD.sub_correlations || {})) rows.push([`E over ${subset} alone`, e, ((EXPECTED.sub_correlations || {})[KEY] || {})[subset]]);
  for (const f of CREDITS) rows.push([`E ${f.replace(/_/g, ' ')}, a local credit (the fence)`, WORLD[f], ((EXPECTED[f] || {}).correlation || {})[KEY]]);
  const cells = rows.map(([what, run, expected]) => `<tr><td>${esc(what)}</td><td class="num">${frac(run)}</td><td class="num">${frac(expected)}</td><td>${verdictOf(run, expected)}</td></tr>`).join('');
  const quanta = Object.entries(WORLD.quanta || {}).map(([label, [inflow, wall]]) => `${label} ${format(inflow)} over W_c ${format(wall)}, about ${format(Math.round(inflow / wall))} quanta`).join('; ');
  const mismatch = WORLD.mismatch || {}, ratios = (mismatch.ratios || []).map(frac).join(', ');
  return `<div class="scroll"><table><thead><tr><th>${esc(GATE_FAMILY)} at (${esc(KEY)}), the world ${esc(WORLD.world)}</th><th>the run (the gate's reading)</th><th>the blind</th><th></th></tr></thead><tbody>${cells}</tbody></table></div>`
    + `<div class="totals">drawn ${WORLD.drawn ? port(WORLD.drawn.join(' ')) : 'nothing'} (the sides' clicks, one port each, drawn one after another on their own reads of the board, the write at the birth between them); ${format(WORLD.intervals_reported)} intervals reported within the window ${(BLIND.window || []).join(' to ')}; the sides' inflow: ${quanta}</div>`
    + `<div class="watch">${esc(mismatch.label || 'LATTICE')}, a diagnostic and no credit: the parts' cross-side products' ratios to the first part's ${ratios || 'none'}, rho ${frac(mismatch.rho)}</div>`;
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
  body += svgText('the algebraic maximum, one per term', right, pad + small, 'end') + (FENCE === null ? '' : svgText('|' + NAME + '| at most ' + FENCE + ', local realism', px(0), H - pad - small * 1.4, 'middle'));  // the fence's label at the foot of its band, the maximum's at the top right, the credits' over their marks
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
  const frame = LOOK.frames[t], counts = {}, clicked = frame.lines.filter(line => line.event === 'click').map(line => line.node_detector + ': ' + line.family);
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
