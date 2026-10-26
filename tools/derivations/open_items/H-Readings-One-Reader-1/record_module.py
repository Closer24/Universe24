"""The record as one module (H-Readings-One-Reader-1, the Node pair's stroke 3): the log's one spelling `entry` (every event the engine logs: refused, birth, credit, lay), the frame pushed for the run back, the census of the state, and the writer (the reader's row, the Node line, the run back, the record). Nothing here moves the state; every integer is read from the Node. The acts stay the engine's: `children` and `credit` are the engine's own with their dict spelt through `entry`, rebound for the proof."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from collections.abc import Callable
from typing import Any

import numpy as np

from event_universe import gram, readings
from event_universe.close import Kid, child_laid
from event_universe.core import paces
from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, SIDES, port_of
from event_universe.core.ports import PORT_SIDES
from event_universe.decoder import THOUSAND
from event_universe.links import link_current
from event_universe.merger import light_children
from event_universe.rows import CARRIER, Line, zeros
from event_universe.rows import PLANE, POTENTIAL
from event_universe.take import frame_nodes

MARKS = 12
EARLY = (60, 24)


# --- the log, spelt once ---


def entry(node: Any, event: str, at: tuple[int, ...], **fields: Any) -> dict[str, Any]:
    """The one spelling of a log entry: the event, the interval, the Node, then the event's fields in the order given."""
    return {"event": event, "i": node.interval, "node": list(at), **fields}


def logged(node: Any, event: str, at: tuple[int, ...], **fields: Any) -> dict[str, Any]:
    """An entry appended to the log and returned."""
    node.log.append(entry(node, event, at, **fields))
    return node.log[-1]


def refused(node: Any, at: tuple[int, ...], cause: str, **numbers: Any) -> None:
    """A refusal by name, counted and logged (close.refused's form)."""
    node.counts["refused_" + cause] += 1
    logged(node, "refused", at, cause=cause, **numbers)


def birth(node: Any, at: tuple[int, ...], s: int, take: dict[str, Any], rec: int, dp_lay: Any, w_children: Any, stood: Any, ends: Any, kids: int, room: Any, exact: Any) -> None:
    """A birth's entry (close.children's dict), through `entry`."""
    logged(
        node, "birth", at, line_pair=s, senses=[-1, 1], W_children=w_children, minus=list(take["_minus"]), plus=list(take["_plus"]),
        taken=take["taken"], booked=take["booked"], levels=take["levels"], taken_now_was=take["taken_now_was"], taker=take["taker"], taken_row=rec,
        taken_line=take["taken_line"], proper=int(node.proper[at]), content=int(node.start_content[at]), amplitude=[node.A, node.B], stood=stood,
        children_at_node=kids, room=room, dP_take=take["dP_take"], dP_lay=dp_lay, dP_lay_ends=ends,
        **{key: take[key] for key in ("remainder_was", "remainder", "owed") if key in take},
        **({"takes": take["takes"], "exact_lay": exact} if "takes" in take else {}),
    )


def children(node: Any, at: tuple[int, ...], kids: list[Kid], take: dict[str, Any], rec: int, c: Any, factors: tuple[Any, ...]) -> set[tuple[int, ...]]:
    """close.children with its dict spelt through `birth` (the acts untouched: child_laid, light_children)."""
    touched = {at}
    for s, minus, plus, room in kids:
        exact: list[list[int] | None] = []
        if "takes" in take:
            row = node.records()[s]
            walls = [t["booked"] for t in take["takes"]]
            rule = node.rule(row.pair, c, factors)
            dp_lay, w_children, stood, exact, ends = light_children(node, s, minus, plus, walls, rule)
        else:
            dp_lay, w_children, stood, ends = child_laid(node, s, minus, plus)
        touched |= {minus, plus}
        node.counts["births"] += 1
        node.closes[at] += 1
        birth(node, at, s, {**take, "_minus": minus, "_plus": plus}, rec, dp_lay, w_children, stood, ends, len(kids), room, exact)
    return touched


def frame_of(node: Any, rec: int, at: tuple[int, ...], plane_starts: list[list[Line]]) -> dict[str, Any]:
    """A plane's credit frame (bodies.frame_of)."""
    re, im = node.records()[rec].lines
    re0, im0 = plane_starts[rec]
    nodes = frame_nodes(node, at)[1:]
    sre, sim = node.stepped[rec]
    return {
        "re_now": int(re.now[at]), "im_now": int(im.now[at]), "re_before": int(re.before[at]), "im_before": int(im.before[at]),
        "re_stepped": int(sre.now[at]), "im_stepped": int(sim.now[at]),
        "re_start_now": int(re0.now[at]), "re_start_before": int(re0.before[at]), "im_start_now": int(im0.now[at]), "im_start_before": int(im0.before[at]),
        "re_neighbours_start": [int(re0.now[n]) for n in nodes], "im_neighbours_start": [int(im0.now[n]) for n in nodes],
        "phases": [[int(c[at]), int(sn[at])] for c, sn in node.start_phases],
        "frames": [int(f[at]) for f in node.start_frames],
        "odd": [int(side * (node.start_odd[axis][at] + node.start_odd[axis][n])) for (axis, side), n in zip(PORT_SIDES, nodes, strict=True)],
        "X": node.X,
        "factors": [int(f[at]) for f in node.start_factors],
    }


def bilinears_of(node: Any, rec: int, at: tuple[int, ...]) -> dict[str, Any]:
    """A quartet's credit frame (bodies.bilinears_of)."""
    row = node.records()[rec]
    nows, befores = [line.now for line in row.lines], [line.before for line in row.lines]
    gj = gram.matmul(gram.gram(row.shape), gram.rotation(row.shape))
    axial = [int(s[at]) for s in gram.density(row.shape, nows)]
    return {
        "levels_now": [int(n[at]) for n in nows], "levels_before": [int(b[at]) for b in befores],
        "W": int(gram.charge(row.shape, row.lines)[at]), "axial": axial, "axial_sign": [(s > 0) - (s < 0) for s in axial],
        "axial_wronskian": [int(gram.form(gj, befores, gram.matvec(ga, nows))[at]) for ga in gram.axes(row.shape)],
    }


def credit(node: Any, rec: int, at: tuple[int, ...], plane_starts: list[list[Line]], fall: int, levels: int, taken_was: int, taken_before: int, line: int, rem_was: int, rem: int) -> dict[str, Any]:
    """A body's credit entry (bodies.credit), through `entry`; returned, not appended (bodies.bodies appends it)."""
    row = node.records()[rec]
    w = int(gram.charge(row.shape, row.lines)[at])
    return entry(
        node, "credit", at, proper=int(node.proper[at]), closes=int(node.closes[at]), content=int(node.start_content[at]), line=rec,
        sense=1 if w > 0 else -1 if w < 0 else 0, beat=int(node.beats[rec][at]),
        frame=frame_of(node, rec, at, plane_starts) if row.shape == PLANE else bilinears_of(node, rec, at),
        taken=fall, booked=node.units[rec], levels=levels, taken_now_was=taken_was, remainder_was=rem_was, remainder=rem, owed=node.units[rec] - rem_was,
        taker=[taken_was, taken_before, levels], dP_take=node.last_dp, taken_line=line,
        sign_level=int(node.row(POTENTIAL).lines[0].now[at]), turned=bool(node.turned[at]),
    )


# --- the frame and the census ---


def frame(top: Any, counters: Any, log_from: int, frozen: Any) -> dict[str, Any]:
    """The frame pushed at the close for the run back (interval.close's dict)."""
    return {"turned": top, "counters": counters, "log_from": log_from, "frozen": frozen}


def bits_of(a: Any) -> int:
    """The largest bit length of an array's values."""
    return int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(a)))


def arrays(node: Any) -> list[Any]:
    """Every level and remainder of the state in the acts' order."""
    lines = node.all_lines()
    return [a for line in lines for a in (line.now, line.before, line.rem)] + [line.wr for line in lines if line.wr is not None]


def census(node: Any) -> tuple[int, int]:
    """The count of the Node's integer arrays and the largest bit length among them."""
    found = arrays(node) + node.standing + node.crossed + node.beats + [node.proper, node.closes, node.take_rem]
    return len(found), max(bits_of(a) for a in found)


def state_hash(node: Any) -> str:
    """The state's hash with the interval, the run back's comparison."""
    text = " ".join(str(int(v)) for a in [*arrays(node), node.take_rem] for v in a.reshape(-1))
    return hashlib.sha256(text.encode() + str(node.interval).encode()).hexdigest()


# --- the writer ---


def ints(a: Any) -> list[int]:
    return [int(x) for x in a.reshape(-1)]


def packets_of(node: Any) -> dict[str, Any]:
    """Every plane with a gap: its weight's centroid in thousandths, its Nodes with levels, its energy's bits."""
    found = {}
    for rec, row in enumerate(node.records()):
        if row is node.emitter():
            continue
        nows = [line.now for line in row.lines]
        weight = ints(gram.form(gram.gram(row.shape), nows, nows))
        total = sum(weight)
        if total == 0:
            continue
        idx = np.indices(node.shape)
        centre = [sum(w * x for w, x in zip(weight, ints(idx[a]), strict=True)) * THOUSAND // total for a in range(AXES)]
        found[f"plane {rec}"] = {"centroid (thousandths of a Link)": centre, "nodes with levels": sum(1 for x in weight if x > 0), "energy bits": total.bit_length()}
    return found


def reading(node: Any, maxbits: int) -> dict[str, Any]:
    """The reader's row at an interval."""
    metric, potential, emitter = node.row(CARRIER), node.row(POTENTIAL), node.emitter().lines[0]
    records = node.records()
    cs, vs = ints(node.content()), ints(metric.lines[0].now)
    charges = [gram.charge(r.shape, r.lines) for r in records]
    tens = [x for line in metric.lines[1:] for x in ints(line.now)]
    counts = node.counts
    return {
        "i": node.interval,
        "packets (reader)": packets_of(node),
        "content min/mean/max": [min(cs), sum(cs) // len(cs), max(cs)],
        "volume mean": sum(vs) // len(vs),
        "births": counts["births"],
        "body_clicks": counts["body_clicks"],
        "refused": sum(v for k, v in counts.items() if k.startswith("refused_")),
        "refused_lay": counts["refused_lay"],
        "refused_orientation": counts["refused_orientation"],
        "turns": counts["turns"],
        "integers": census(node)[0],
        "max bits": maxbits,
        "max transient bits": node.max_transient,
        "sign level max": max(abs(x) for x in ints(potential.lines[0].now)),
        "planes energy bits": sum(x * x for r in records for line in r.lines for x in ints(line.now)).bit_length(),
        "links at the wall": sum(1 for f in node.link_factors()[0::SIDES] for x in ints(f) if x == 0),
        "tension min/max": [min(tens), max(tens)],
        "odd max bits": max(abs(x) for line in potential.lines[1:] for x in ints(line.now)).bit_length(),
        "link count max": node.count_max,
        "orbit table": len(node.orbit),
        "gap-0 W abs max": max(abs(x) for x in ints(charges[records.index(node.emitter())])),
        "W total": sum(sum(ints(w)) for w in charges),
        "W abs sum": sum(abs(x) for w in charges for x in ints(w)),
        "gap-0 velocity max": max(abs(a - b) for a, b in zip(ints(emitter.now), ints(emitter.before), strict=True)),
    }


def node_lines(node: Any) -> dict[str, Any]:
    """The Node and Link line at an interval."""
    content = node.content()
    pace = paces.link_pace_of(node.gamma, content)
    factors = node.link_factors(None, readings.frozen_of(node, content))
    emitter = node.emitter().lines[0]
    return {
        "i": node.interval,
        "X": ints(node.row(CARRIER).lines[0].now),
        "content": ints(content),
        "turned": [i for i, t in enumerate(node.turned.reshape(-1).tolist()) if t],
        "frozen": [i for i, p in enumerate(ints(pace)) if p == 0],
        "held": [[i, axis] for axis in range(AXES) for i, f in enumerate(ints(factors[port_of(axis, 0)])) if f == 0],
        "current": [ints(link_current(emitter, port_of(axis, 0))) for axis in range(AXES)],
    }


def run_back(node: Any, hashes: list[str]) -> dict[str, int]:
    """As many intervals back as states were kept, each compared with the kept hash."""
    exact = 0
    for k in range(len(hashes)):
        node.step(-1)
        exact += state_hash(node) == hashes[len(hashes) - 1 - k]
    return {"intervals": len(hashes), "exact": exact}


def forward(node: Any, intervals: int, back: int, out: Callable[[str], Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """The intervals forward: the reader's rows at the marks, a Node line per interval, the last `back` hashes kept."""
    t0 = time.monotonic_ns()
    marks = {1, intervals} | {(k * intervals) // MARKS for k in range(1, MARKS)} | {intervals // e for e in EARLY}
    rows, nodes, hashes, maxbits = [], [], [], 0
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(state_hash(node))
        node.step()
        maxbits = max(maxbits, census(node)[1])
        nodes.append(node_lines(node))
        if node.interval in marks:
            rows.append(dict(reading(node, maxbits), milliseconds=(time.monotonic_ns() - t0) // (THOUSAND * THOUSAND)))
            out(json.dumps(rows[-1]))
    return rows, nodes, hashes


def record(node_of: Callable[..., Any], universe: dict[str, Any], world: dict[str, Any], back: int = 0, out: Callable[[str], Any] = print) -> dict[str, Any]:
    """The record of a world: forward, back, the counts; `node_of` the Node's constructor (run.py's Node), passed so this module imports no act."""
    node = node_of(universe, world)
    intervals = int(world["intervals"])
    rows, nodes, hashes = forward(node, intervals, back, out)
    kept_log = list(node.log)
    returned = run_back(node, hashes) if back else None
    if returned:
        out(json.dumps({"run back": returned}))
    counts = {k: str(v) for k, v in node.counts.items()}
    out(json.dumps({"counts": counts}))
    return {
        "world": world, "universe": universe, "den": node.den, "cube": node.cube, "intervals": intervals,
        "gapped": [(str(r.pair[0]), str(sine_den(r.pair[0], node.den))) for r in node.gapped if r.pair],
        "planes": [str(r.pair[0]) for r in node.records() if r.pair],
        "T": node.T, "gamma": node.gamma, "G": node.G, "counts": counts, "turns": node.turns, "rows": rows, "nodes": nodes, "run_back": returned, "log": kept_log,
    }
