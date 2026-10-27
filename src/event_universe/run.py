"""The record as one module, the writer run.py (NL-S1's third stroke, the Boss's 6411590757 under the owner's delegation; H-Readings-One-Reader-1's record_module.py the spec; the engine gate carries the writer's three marks under this name): the log's one spelling (`entry`: every event the engine logs, refused, birth, credit and lay, through it), the frame pushed at the close for the run back, the census and the hash of the state, and the writer (the reader's rows at the marks, the Node lines, the run back, the record and its command line, `python -m event_universe.run <world.json> <out.json> [back N]`); the acts write nothing here and read nothing from it but the frame."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import gram, readings
from event_universe.core import paces
from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, SIDES, port_of
from event_universe.decoder import THOUSAND
from event_universe.links import factors, link_current
from event_universe.loader.world import load_world
from event_universe.rows import CARRIER, POTENTIAL, Line, zeros

if TYPE_CHECKING:
    from event_universe.node import Node

MARKS = 12  # the reader's rows: one at every twelfth of the run
EARLY = (60, 24)  # and two early marks, at the sixtieth and the twenty-fourth


def entry(node: Node, event: str, at: Any, **fields: Any) -> dict[str, Any]:
    """The one spelling of a log entry: the event, the interval, the Node (None for a lay over the board), then the event's fields in the order given."""
    return {"event": event, "i": node.interval, "node": None if at is None else list(at), **fields}


def logged(node: Node, event: str, at: Any, **fields: Any) -> dict[str, Any]:
    """An entry appended to the log and returned."""
    node.log.append(entry(node, event, at, **fields))
    return node.log[-1]


def refused(node: Node, at: tuple[int, ...], cause: str, **numbers: Any) -> None:
    """A refusal by name, counted and logged."""
    node.counts["refused_" + cause] += 1
    logged(node, "refused", at, cause=cause, **numbers)


def birth(
    node: Node,
    at: Any,
    s: int,
    ends: Any,
    take: Any,
    rec: int,
    laid: Any,
    written: Any,
    kids: int,
    room: Any,
    exact: Any,
) -> None:
    """A birth's entry: the children's record, their ends, the take's numbers, the Node's proper time and content, the amplitude, the levels that stood, the lays' momentum per end with their bookings, the take's remainder and booking, and a merger's takes with its exact lays."""
    dp_lay, w_children, stood, dp_ends = laid
    logged(
        node,
        "birth",
        at,
        line_pair=s,
        senses=[-1, 1],
        W_children=w_children,
        minus=list(ends[0]),
        plus=list(ends[1]),
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
        room=room,
        dP_take=take["dP_take"],
        dP_lay=dp_lay,
        dP_lay_ends=dp_ends,
        **{key + "_ends": [w[key] for w in written] for key in written[0]},
        **{
            key: take[key]
            for key in ("remainder_was", "remainder", "owed", "clock", "recoil", "carry_was", "carry")
            if key in take
        },
        **({"takes": take["takes"], "exact_lay": exact} if "takes" in take else {}),
        **({"cross": take["cross"]} if "cross" in take else {}),
    )


def credit(
    node: Node,
    rec: int,
    at: tuple[int, ...],
    take: dict[str, Any],
    frame: dict[str, Any],
    start: list[Line],
) -> dict[str, Any]:
    """A body's credit with its frame (the plane's frame_of, the bodies' own readings of the record), its sense the sign of its charge at the Node read at the interval's start (`start`, the record's lines as the interval began, CL-S2; the former read on the board after the close's own writes kept by name), its beat, the take's numbers (the take act's dict), momentum and booking, the unit the close booked and what it owed; returned, not appended (the bodies append it after the lay-back)."""
    row = node.records()[rec]
    w = int(gram.charge(row.shape, start)[at])
    fall, levels, taken_was, line = (
        take["taken"],
        take["levels"],
        take["taken_now_was"],
        take["taken_line"],
    )
    taken_before, rem_was, rem = take["taker"][1], take["remainder_was"], take["remainder"]
    return entry(
        node,
        "credit",
        at,
        proper=int(node.proper[at]),
        closes=int(node.closes[at]),
        content=int(node.start_content[at]),
        line=rec,
        sense=1 if w > 0 else -1 if w < 0 else 0,
        beat=int(node.beats[rec][at]),
        frame=frame,
        taken=fall,
        booked=node.units[rec],
        levels=levels,
        taken_now_was=taken_was,
        remainder_was=rem_was,
        remainder=rem,
        owed=node.units[rec] - rem_was,
        taker=[taken_was, taken_before, levels],
        dP_take=node.last_dp,
        **node.last_recoil,
        taken_line=line,
        sign_level=int(node.row(POTENTIAL).lines[0].now[at]),
        turned=bool(node.turned[at]),
    )


def frame(node: Node, top: Any, log_from: int, frozen: Any, bookings: Any) -> dict[str, Any]:
    """The frame pushed at the close for the run back: the turned Nodes, the counters as they stood before the click (the swap changes none), the log's length, the frozen mask and the emission's bookings."""
    counters = (
        [a.copy() for a in node.standing],
        [a.copy() for a in node.crossed],
        [a.copy() for a in node.beats],
    )
    return {
        "turned": top,
        "counters": counters,
        "log_from": log_from,
        "frozen": frozen,
        "bookings": bookings,
    }


def bits_of(a: Any) -> int:
    """The largest bit length of an integer array's values."""
    return int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(a)))


def arrays(node: Node) -> list[Any]:
    """Every level and remainder of the state, the lines' arrays in the acts' order."""
    lines = node.all_lines()
    found = [a for line in lines for a in (line.now, line.before, line.rem)]
    return found + [line.wr for line in lines if line.wr is not None]


def state(node: Node) -> list[Any]:
    """Every integer array of the Node's state: the lines' levels and remainders, the records' standing, crossings and beats, the proper count, the closes and the take's remainder (the one list the census counts and the run back compares; the former comparison of the lines and the take's remainder alone, which left the five counters the bodies' closing reads unchecked, kept by name, the Boss's 6421253357 item 4, 2026-10-26)."""
    found = arrays(node) + node.standing + node.crossed + node.beats + [node.proper, node.closes]
    return [*found, node.take_rem]


def census(node: Node) -> tuple[int, int]:
    """The count of integer arrays the Node holds and the largest bit length among their values."""
    found = state(node)
    return len(found), max(bits_of(a) for a in found)


def state_text(node: Node) -> str:
    """Every integer of the state as text (`state`), the run back's comparison bit for bit."""
    return " ".join(str(int(v)) for a in state(node) for v in a.reshape(-1))


def state_hash(node: Node) -> str:
    """The state's hash with the interval."""
    return hashlib.sha256(state_text(node).encode() + str(node.interval).encode()).hexdigest()


def ints(a: Any) -> list[int]:
    """An array's values as Python integers."""
    return [int(x) for x in a.reshape(-1)]


def packets_of(node: Node) -> dict[str, Any]:
    """The reader's view of every plane with a gap: its weight's centroid in thousandths of a Link, its Nodes with levels, its energy's bits."""
    found = {}
    for rec, row in enumerate(node.records()):
        if row is node.emitter():
            continue
        nows = [line.now for line in row.lines]
        weight = gram.dot(nows, nows)
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


def reading(node: Node, maxbits: int) -> dict[str, Any]:
    """The reader's row at an interval: the board's numbers read from outside (no Node reads them)."""
    metric, potential, emitter = node.row(CARRIER), node.row(POTENTIAL), node.emitter().lines[0]
    records = node.records()
    cs, vs = ints(readings.content(node)), ints(metric.lines[0].now)
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
        "links at the wall": sum(1 for f in factors(node)[0::SIDES] for x in ints(f) if x == 0),
        "tension min/max": [min(tens), max(tens)],
        "odd max bits": odd_max.bit_length(),
        "link count max": node.count_max,
        "orbit table": len(node.orbit),
        "gap-0 W abs max": max(abs(x) for x in ints(charges[records.index(node.emitter())])),
        "W total": sum(ints(total)),
        "W abs sum": sum(abs(x) for w in charges for x in ints(w)),
        "gap-0 velocity max": emitter_v,
    }


def node_lines(node: Node) -> dict[str, Any]:
    """The record's Node and Link line at an interval, every Node by its index in the board's order: the carrier's level X, the content, the turned Nodes, the frozen Nodes (the Link pace 0), the Links held at the wall (the factor 0) as [Node, axis] pairs, and every Link's current of the gap-0 line, F_ij from the Node along each axis (the sign the direction, the size the flow); the page draws the board from these and nothing else."""
    carrier = node.row(CARRIER).lines[0]
    content = readings.content(node)
    pace = paces.link_pace_of(node.gamma, content)
    read = factors(node, None, readings.frozen_of(node, content))
    held = [
        [i, axis] for axis in range(AXES) for i, f in enumerate(ints(read[port_of(axis, 0)])) if f == 0
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


def run_back(node: Node, hashes: list[str]) -> dict[str, int]:
    """The run back: as many intervals back as states were kept, each compared with the kept state's hash."""
    exact = 0
    for k in range(len(hashes)):
        node.step(-1)
        exact += state_hash(node) == hashes[len(hashes) - 1 - k]
    return {"intervals": len(hashes), "exact": exact}


def forward(
    node: Node, intervals: int, back: int, out: Callable[[str], Any]
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
                dict(
                    reading(node, maxbits),
                    milliseconds=(time.monotonic_ns() - t0) // (THOUSAND * THOUSAND),
                )
            )
            out(json.dumps(rows[-1]))
    return rows, nodes, hashes


def record(
    universe: dict[str, Any],
    world: dict[str, Any],
    back: int = 0,
    out: Callable[[str], Any] = print,
    node_of: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    """The world's intervals run (`forward`), then `back` intervals run back and compared by the state's hash (`run_back`); the record returned; `node_of` the Node's class (the engine's unless a toy names its own)."""
    from event_universe.node import Node  # the writer stands below the Node, which reads the frame here

    node = (Node if node_of is None else node_of)(universe, world)
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
