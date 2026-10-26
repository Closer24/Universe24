"""The record as one module (H-Readings-One-Reader-2, the Node pair's stroke 3): what the Node writes down and nothing it acts on. The log's three lines spelt once each (`entry` the head every line carries, `refused`, `birth`, `credit`), the frame the close pushes for the run back (`frame`), the run's counts (COUNTS), the census of the state (`arrays`, `census`, `state_bytes`, `state_hash`, `bits_of`) and the writer (`packets_of`, `reading`, `node_lines`, `forward`, `run_back`, `record`, `main`: run.py's, moved whole). Imports through run.py's own imports (gram, readings, paces, the loader, the decoder's THOUSAND, links.link_current) and the engine's Node through run."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from collections.abc import Callable
from typing import Any

import numpy as np

from event_universe import gram, readings
from event_universe.core import paces
from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, SIDES, port_of
from event_universe.decoder import THOUSAND
from event_universe.links import link_current
from event_universe.loader.world import load_world
from event_universe.rows import CARRIER, POTENTIAL, zeros
from event_universe.run import Node

MARKS = 12  # the reader's rows: one at every twelfth of the run
EARLY = (60, 24)  # and two early marks, at the sixtieth and the twenty-fourth

COUNTS = {  # the run's counts, every one 0 at the start
    "births": 0,
    "taken": 0,
    "booked": 0,
    "body_clicks": 0,
    "laid_back": 0,
    "refused_stop": 0,
    "refused_origin": 0,
    "refused_lay": 0,
    "refused_orientation": 0,
    "refused_twist": 0,
    "refused_sense": 0,
    "turns": 0,
    "met": 0,
    "laid": 0,
    "laid_nodes": 0,
}


def entry(event: str, node: Any, at: tuple[int, ...], **fields: Any) -> dict[str, Any]:
    """The head of every log line, the event, the interval and the Node, then the line's own fields."""
    return {"event": event, "i": node.interval, "node": list(at), **fields}


def refused(node: Any, at: tuple[int, ...], cause: str, count: int = 1, **numbers: Any) -> None:
    """A refusal by name, counted (`count` times: a birth's refusal counts its children) and logged."""
    node.counts["refused_" + cause] += count
    node.log.append(entry("refused", node, at, cause=cause, **numbers))


def birth(
    node: Any,
    at: tuple[int, ...],
    kid: Any,
    take: dict[str, Any],
    rec: int,
    dp_lay: list[int],
    w_children: list[int],
    stood: list[list[int]],
    ends: list[list[int]],
    kids: int,
    exact: list[Any],
) -> dict[str, Any]:
    """A birth's log line: the children's record and Nodes, the take's numbers, the lays' momentum and senses, the exact take's remainders where the take carries them, a merger's two ends under `takes`."""
    return entry(
        "birth",
        node,
        at,
        line_pair=kid.line_pair,
        senses=[-1, 1],
        W_children=w_children,
        minus=list(kid.minus),
        plus=list(kid.plus),
        taken=take["taken"],
        booked=take["booked"],
        levels=take["levels"],
        taken_now_was=take["taken_now_was"],
        taker=take["taker"],
        taken_row=rec,
        taken_line=take["taken_line"],
        proper=int(node.proper[at]),
        content=int(node.start_content[at]),
        amplitude=[node.A, node.B],
        stood=stood,
        children_at_node=kids,
        room=kid.room,
        dP_take=take["dP_take"],
        dP_lay=dp_lay,
        dP_lay_ends=ends,
        **{key: take[key] for key in ("remainder_was", "remainder", "owed") if key in take},
        **({"takes": take["takes"], "exact_lay": exact} if "takes" in take else {}),
    )


def credit(
    node: Any,
    rec: int,
    at: tuple[int, ...],
    frame_read: dict[str, Any],
    fall: int,
    levels: int,
    taken_was: int,
    taken_before: int,
    line: int,
    rem_was: int,
    rem: int,
) -> dict[str, Any]:
    """A body's credit: its frame as read by the close (`frame_read`), its sense the sign of its charge, its beat, the take's numbers and momentum, the remainders (EX-S1), the taker's three levels, the line taken, the sign level and whether the Node turned."""
    row = node.records()[rec]
    w = int(gram.charge(row.shape, row.lines)[at])
    return entry(
        "credit",
        node,
        at,
        proper=int(node.proper[at]),
        closes=int(node.closes[at]),
        content=int(node.start_content[at]),
        line=rec,
        sense=1 if w > 0 else -1 if w < 0 else 0,
        beat=int(node.beats[rec][at]),
        frame=frame_read,
        taken=fall,
        booked=node.units[rec],
        levels=levels,
        taken_now_was=taken_was,
        remainder_was=rem_was,
        remainder=rem,
        owed=node.units[rec] - rem_was,
        taker=[taken_was, taken_before, levels],
        dP_take=node.last_dp,
        taken_line=line,
        sign_level=int(node.row(POTENTIAL).lines[0].now[at]),
        turned=bool(node.turned[at]),
    )


def frame(node: Any, top: Any, log_from: int, frozen: Any) -> dict[str, Any]:
    """The frame pushed at the close for the run back: the turned Nodes, the counters as they stood before the click, the log's length and the frozen mask."""
    counters = (
        [a.copy() for a in node.standing],
        [a.copy() for a in node.crossed],
        [a.copy() for a in node.beats],
    )
    return {"turned": top, "counters": counters, "log_from": log_from, "frozen": frozen}


def bits_of(a: Any) -> int:
    """The largest bit length of an integer array's values."""
    return int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(a)))


def arrays(node: Any) -> list[Any]:
    """Every level and remainder of the state, the lines' arrays in the acts' order."""
    lines = node.all_lines()
    found = [a for line in lines for a in (line.now, line.before, line.rem)]
    return found + [line.wr for line in lines if line.wr is not None]


def census(node: Any) -> tuple[int, int]:
    """The count of integer arrays the Node holds and the largest bit length among their values."""
    found = arrays(node) + node.standing + node.crossed + node.beats + [node.proper, node.closes]
    found.append(node.take_rem)
    return len(found), max(bits_of(a) for a in found)


def state_bytes(node: Any) -> bytes:
    """Every level and remainder of the state as text bytes, the run back's comparison bit for bit."""
    found = [*arrays(node), node.take_rem]
    return " ".join(str(int(v)) for a in found for v in a.reshape(-1)).encode()


def state_hash(node: Any) -> str:
    """The state's hash with the interval."""
    return hashlib.sha256(state_bytes(node) + str(node.interval).encode()).hexdigest()


def ints(a: Any) -> list[int]:
    """An array's values as Python integers."""
    return [int(x) for x in a.reshape(-1)]


def packets_of(node: Any) -> dict[str, Any]:
    """The reader's view of every plane with a gap: its weight's centroid in thousandths of a Link, its Nodes with levels, its energy's bits."""
    found = {}
    for rec, row in enumerate(node.records()):
        if row is node.emitter():
            continue
        nows = [line.now for line in row.lines]
        weight = gram.form(gram.gram(row.shape), nows, nows)
        total = sum(ints(weight))
        if total == 0:
            continue
        idx = np.indices(node.shape)
        centre = [
            sum(w * x for w, x in zip(ints(weight), ints(idx[a]), strict=True)) * THOUSAND // total
            for a in range(len(node.shape))
        ]
        found[f"plane {rec}"] = {
            "centroid (thousandths of a Link)": centre,
            "nodes with levels": sum(1 for x in ints(weight) if x > 0),
            "energy bits": total.bit_length(),
        }
    return found


def reading(node: Any, maxbits: int) -> dict[str, Any]:
    """The reader's row at an interval: the board's numbers read from outside (no Node reads them)."""
    metric, potential, emitter = node.row(CARRIER), node.row(POTENTIAL), node.emitter().lines[0]
    records = node.records()
    cs, vs = ints(node.content()), ints(metric.lines[0].now)
    energy = sum(x * x for r in records for line in r.lines for x in ints(line.now))
    odd_max = max(abs(x) for line in potential.lines[1:] for x in ints(line.now))
    emitter_v = max(abs(a - b) for a, b in zip(ints(emitter.now), ints(emitter.before), strict=True))
    total = zeros(node.shape)
    charges = [gram.charge(r.shape, r.lines) for r in records]
    for w in charges:
        total = total + w
    n, _bits = census(node)
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
        "integers": n,
        "max bits": maxbits,
        "max transient bits": node.max_transient,
        "sign level max": max(abs(x) for x in ints(potential.lines[0].now)),
        "planes energy bits": energy.bit_length(),
        "links at the wall": sum(1 for f in node.link_factors()[0::SIDES] for x in ints(f) if x == 0),
        "tension min/max": [min(tens), max(tens)],
        "odd max bits": odd_max.bit_length(),
        "link count max": node.count_max,
        "orbit table": len(node.orbit),
        "gap-0 W abs max": max(abs(x) for x in ints(charges[records.index(node.emitter())])),
        "W total": sum(ints(total)),
        "W abs sum": sum(abs(x) for w in charges for x in ints(w)),
        "gap-0 velocity max": emitter_v,
    }


def node_lines(node: Any) -> dict[str, Any]:
    """The record's Node and Link line at an interval: X, the content, the turned and frozen Nodes, the Links held at the wall and every Link's current of the gap-0 line."""
    carrier = node.row(CARRIER).lines[0]
    content = node.content()
    pace = paces.link_pace_of(node.gamma, content)
    factors = node.link_factors(None, readings.frozen_of(node, content))
    held = [
        [i, axis]
        for axis in range(AXES)
        for i, f in enumerate(ints(factors[port_of(axis, 0)]))
        if f == 0
    ]
    emitter = node.emitter().lines[0]
    return {
        "i": node.interval,
        "X": ints(carrier.now),
        "content": ints(content),
        "turned": [i for i, t in enumerate(node.turned.reshape(-1).tolist()) if t],
        "frozen": [i for i, p in enumerate(ints(pace)) if p == 0],
        "held": held,
        "current": [ints(link_current(emitter, port_of(axis, 0))) for axis in range(AXES)],
    }


def run_back(node: Any, hashes: list[str]) -> dict[str, int]:
    """The run back: as many intervals back as states were kept, each compared with the kept state's hash."""
    exact = 0
    for k in range(len(hashes)):
        node.step(-1)
        exact += state_hash(node) == hashes[len(hashes) - 1 - k]
    return {"intervals": len(hashes), "exact": exact}


def forward(
    node: Any, intervals: int, back: int, out: Callable[[str], Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """The intervals run forward: the reader's rows at the marks written as they come, a Node line at every interval, the last `back` states' hashes kept for the run back."""
    t0 = time.monotonic_ns()
    marks = (
        {1, intervals}
        | {(k * intervals) // MARKS for k in range(1, MARKS)}
        | {intervals // e for e in EARLY}
    )
    rows: list[dict[str, Any]] = []
    nodes: list[dict[str, Any]] = []
    hashes = []
    maxbits = 0
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(state_hash(node))
        node.step()
        maxbits = max(maxbits, census(node)[1])
        nodes.append(node_lines(node))
        if node.interval in marks:
            rows.append(
                dict(reading(node, maxbits), milliseconds=(time.monotonic_ns() - t0) // (THOUSAND * THOUSAND))
            )
            out(json.dumps(rows[-1]))
    return rows, nodes, hashes


def record(
    universe: dict[str, Any], world: dict[str, Any], back: int = 0, out: Callable[[str], Any] = print
) -> dict[str, Any]:
    """The world's intervals run (`forward`), then `back` intervals run back and compared by the state's hash (`run_back`); the record returned."""
    node = Node(universe, world)
    intervals = int(world["intervals"])
    rows, nodes, hashes = forward(node, intervals, back, out)
    kept_log = list(node.log)
    returned = run_back(node, hashes) if back else None
    if returned:
        out(json.dumps({"run back": returned}))
    counts = {k: str(v) for k, v in node.counts.items()}
    out(json.dumps({"counts": counts}))
    return {
        "world": world,
        "universe": universe,
        "den": node.den,
        "cube": node.cube,
        "intervals": intervals,
        "gapped": [(str(r.pair[0]), str(sine_den(r.pair[0], node.den))) for r in node.gapped if r.pair],
        "planes": [str(r.pair[0]) for r in node.records() if r.pair],
        "T": node.T,
        "gamma": node.gamma,
        "G": node.G,
        "counts": counts,
        "turns": node.turns,
        "rows": rows,
        "nodes": nodes,
        "run_back": returned,
        "log": kept_log,
    }


def main(argv: list[str]) -> None:
    """The writer from the command line: the world file, the output file, `back N` for the run back."""
    sys.set_int_max_str_digits(0)
    _, world_path, out_path, *_rest = argv
    universe, world = load_world(world_path)
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    found = record(universe, world, back, lambda line: print(line, flush=True))
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(found, out)


if __name__ == "__main__":
    main(sys.argv)
