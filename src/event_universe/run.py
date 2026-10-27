"""The chart as one module, the writer run.py (NL-S1's third stroke, the Boss's 6411590757 under the owner's delegation; H-Readings-One-Reader-1's record_module.py the spec; the engine gate carries the writer's three marks under this name): the log's one spelling (`entry`: every event the engine logs, jammed, fitting, chime and set, through it), the rewind note pushed at the striking for the rewind, the census and the hash of the state, and the writer (the reader's rows at the marks, the clock lines, the rewind, the chart and its command line, `python -m event_universe.run <piece.json> <out.json> [back N]`); the acts write nothing here and read nothing from it but the rewind note."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import hands, readings
from event_universe.assembly.piece import read_piece
from event_universe.core import rates
from event_universe.core.rates import sine_rim
from event_universe.core.spokes import AXES, SIDES, spoke_of
from event_universe.meshes import factors, mesh_lead
from event_universe.reckoner import THOUSAND
from event_universe.trains import OFFSET, REGULATOR, Gear, zeros

if TYPE_CHECKING:
    from event_universe.clock import Clock

MARKS = 12  # the reader's rows: one at every twelfth of the run
EARLY = (60, 24)  # and two early marks, at the sixtieth and the twenty-fourth


def entry(node: Clock, event: str, at: Any, **fields: Any) -> dict[str, Any]:
    """The one spelling of a log entry: the event, the tick, the clock (None for a setting over the great clock), then the event's fields in the order given."""
    return {"event": event, "i": node.ticks, "node": None if at is None else list(at), **fields}


def logged(node: Clock, event: str, at: Any, **fields: Any) -> dict[str, Any]:
    """An entry appended to the log and returned."""
    node.log.append(entry(node, event, at, **fields))
    return node.log[-1]


def jammed(clock: Clock, at: tuple[int, ...], cause: str, **numbers: Any) -> None:
    """A jam by name, counted and logged."""
    clock.counts["refused_" + cause] += 1
    logged(clock, "refused", at, cause=cause, **numbers)


def fitting(
    node: Clock,
    at: Any,
    s: int,
    ends: Any,
    unwind: Any,
    rec: int,
    advanced: Any,
    drives: Any,
    fitted: int,
    room: Any,
    exact: Any,
) -> None:
    """A fitting's entry: the fitted hands' train, their ends, the unwind's numbers, the clock's dial and load, the hand length, the notches that stood, the advances' push per end with their tallies, the unwind's slack and tally, and an unspringing's unwinds with its exact advances."""
    dp_advance, w_fitted, stood, dp_ends = advanced
    logged(
        node,
        "birth",
        at,
        line_pair=s,
        **({} if hands.twin_of(node.hands(), s) == s else {"plus_hand": hands.twin_of(node.hands(), s)}),
        senses=[-1, 1],
        W_children=w_fitted,
        minus=list(ends[0]),
        plus=list(ends[1]),
        taken=unwind["taken"],
        booked=unwind["booked"],
        levels=unwind["levels"],
        taken_now_was=unwind["taken_now_was"],
        taker=unwind["taker"],
        taken_row=rec,
        taken_line=unwind["taken_line"],
        proper=int(node.dial[at]),
        content=int(node.start_load[at]),
        amplitude=[node.A, node.B],
        stood=stood,
        children_at_node=fitted,
        room=room,
        dP_take=unwind["dP_take"],
        dP_lay=dp_advance,
        dP_lay_ends=dp_ends,
        **{key + "_ends": [w[key] for w in drives] for key in drives[0]},
        **{
            key: unwind[key]
            for key in ("remainder_was", "remainder", "owed", "clock", "recoil", "carry_was", "carry")
            if key in unwind
        },
        **({"takes": unwind["takes"], "exact_lay": exact} if "takes" in unwind else {}),
        **({"cross": unwind["cross"]} if "cross" in unwind else {}),
    )


def chime(
    clock: Clock,
    rec: int,
    at: tuple[int, ...],
    unwind: dict[str, Any],
    face: dict[str, Any],
    start: list[Gear],
) -> dict[str, Any]:
    """A bob's chime with its face (the hand's face_of, the bobs' own readings of the hand), its sense the sign of its sweep at the clock read at the tick's start (`start`, the hand's gears as the tick began, CL-S2; the former read on the great clock after the striking's own drives kept by name), its beat, the unwind's numbers (the unwind act's dict), push and tally, the winding the striking tallied and what is due; returned, not appended (the bobs append it after the return)."""
    w = int(hands.sweep(start)[at])
    fall, notches, unwound_was, gear = (
        unwind["taken"],
        unwind["levels"],
        unwind["taken_now_was"],
        unwind["taken_line"],
    )
    unwound_before, slack_was, slack = unwind["taker"][1], unwind["remainder_was"], unwind["remainder"]
    return entry(
        clock,
        "credit",
        at,
        proper=int(clock.dial[at]),
        closes=int(clock.strikes[at]),
        content=int(clock.start_load[at]),
        line=rec,
        sense=1 if w > 0 else -1 if w < 0 else 0,
        beat=int(clock.beats[rec][at]),
        frame=face,
        taken=fall,
        booked=clock.windings[rec],
        levels=notches,
        taken_now_was=unwound_was,
        remainder_was=slack_was,
        remainder=slack,
        owed=clock.windings[rec] - slack_was,
        taker=[unwound_was, unwound_before, notches],
        dP_take=clock.last_push,
        **clock.last_recoil,
        taken_line=gear,
        sign_level=int(clock.train(OFFSET).gears[0].now[at]),
        turned=bool(clock.turned_over[at]),
    )


def rewind_note(clock: Clock, top: Any, log_from: int, stopped: Any, tallies: Any) -> dict[str, Any]:
    """The rewind note pushed at the striking for the rewind: the turned-over clocks, the counters as they stood before the strike (the turnover changes none), the log's length, the stopped mask and the release's tallies."""
    counters = (
        [a.copy() for a in clock.wound],
        [a.copy() for a in clock.crossed],
        [a.copy() for a in clock.beats],
    )
    return {
        "turned": top,
        "counters": counters,
        "log_from": log_from,
        "frozen": stopped,
        "bookings": tallies,
    }


def bits_of(a: Any) -> int:
    """The largest bit length of an integer array's values."""
    return int(np.max(np.abs(a))).bit_length()


def arrays(clock: Clock) -> list[Any]:
    """Every notch and fine tooth of the state, the gears' arrays in the acts' order."""
    gears = clock.all_gears()
    found = [a for gear in gears for a in (gear.now, gear.before, gear.fine)]
    return found + [gear.dfine for gear in gears if gear.dfine is not None]


def state(clock: Clock) -> list[Any]:
    """Every integer array of the clock's state: the gears' notches and fine teeth, the hands' wound ticks, crossings and beats, the dial, the strikes and the slack (the one list the census counts and the rewind compares; the former comparison of the gears and the slack alone, which left the five counters the bobs' striking reads unchecked, kept by name, the Boss's 6421253357 item 4, 2026-10-26)."""
    found = arrays(clock) + clock.wound + clock.crossed + clock.beats + [clock.dial, clock.strikes]
    return [*found, clock.slack]


def census(clock: Clock) -> tuple[int, int]:
    """The count of integer arrays the clock holds and the largest bit length among their values."""
    found = state(clock)
    return len(found), max(bits_of(a) for a in found)


def state_text(clock: Clock) -> str:
    """Every integer of the state as text (`state`), the rewind's comparison bit for bit."""
    return " ".join(str(int(v)) for a in state(clock) for v in a.reshape(-1))


def state_hash(clock: Clock) -> str:
    """The state's hash with the tick."""
    return hashlib.sha256(state_text(clock).encode() + str(clock.ticks).encode()).hexdigest()


def ints(a: Any) -> list[int]:
    """An array's values as Python integers."""
    return [int(x) for x in a.reshape(-1)]


def packets_of(clock: Clock) -> dict[str, Any]:
    """The reader's view of every sprung hand: its weight's centroid in thousandths of a mesh, its clocks with notches, its wind's bits."""
    found = {}
    for rec, train in enumerate(clock.hands()):
        if train is clock.unsprung():
            continue
        nows = [gear.now for gear in train.gears]
        weight = hands.dot(nows, nows)
        total = sum(ints(weight))
        if total == 0:
            continue
        idx = np.indices(clock.size)
        centre = [
            sum(w * x for w, x in zip(ints(weight), ints(idx[a]), strict=True)) * THOUSAND // total
            for a in range(len(clock.size))
        ]
        found[f"plane {rec}"] = {
            "centroid (thousandths of a Link)": centre,
            "nodes with levels": sum(1 for x in ints(weight) if x > 0),
            "energy bits": total.bit_length(),
        }
    return found


def reading(clock: Clock, maxbits: int) -> dict[str, Any]:
    """The reader's row at a tick: the great clock's numbers read from outside (no clock reads them)."""
    regulator, offset, unsprung = clock.train(REGULATOR), clock.train(OFFSET), clock.unsprung().gears[0]
    hand_trains = clock.hands()
    cs, vs = ints(readings.load(clock)), ints(regulator.gears[0].now)
    wind = sum(x * x for r in hand_trains for gear in r.gears for x in ints(gear.now))
    odd_max = max(abs(x) for gear in offset.gears[1:] for x in ints(gear.now))
    unsprung_v = max(abs(a - b) for a, b in zip(ints(unsprung.now), ints(unsprung.before), strict=True))
    total = zeros(clock.size)
    sweeps = [hands.sweep(r.gears) for r in hand_trains]
    for w in sweeps:
        total = total + w
    n, _bits = census(clock)
    tens = [x for gear in regulator.gears[1:] for x in ints(gear.now)]
    counts = clock.counts
    return {
        "i": clock.ticks,
        "packets (reader)": packets_of(clock),
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
        "max transient bits": clock.max_transient,
        "sign level max": max(abs(x) for x in ints(offset.gears[0].now)),
        "planes energy bits": wind.bit_length(),
        "links at the wall": sum(1 for f in factors(clock)[0::SIDES] for x in ints(f) if x == 0),
        "tension min/max": [min(tens), max(tens)],
        "odd max bits": odd_max.bit_length(),
        "link count max": clock.count_max,
        "orbit table": len(clock.circuit),
        "gap-0 W abs max": max(abs(x) for x in ints(sweeps[hand_trains.index(clock.unsprung())])),
        "W total": sum(ints(total)),
        "W abs sum": sum(abs(x) for w in sweeps for x in ints(w)),
        "gap-0 velocity max": unsprung_v,
    }


def clock_lines(clock: Clock) -> dict[str, Any]:
    """The chart's clock and mesh line at a tick, every clock by its index in the great clock's order: the regulator's notch (the stretch), the load, the turned-over clocks, the stopped clocks (the mesh rate 0), the meshes held disengaged (the factor 0) as [clock, axis] pairs, and every mesh's lead of the unsprung gear, F_ij from the clock along each axis (the sign the direction, the size the flow); the page draws the great clock from these and nothing else."""
    regulator = clock.train(REGULATOR).gears[0]
    load = readings.load(clock)
    mesh_rate = rates.mesh_rate_of(clock.full_rate, load)
    read = factors(clock, None, readings.stopped_of(clock, load))
    held = [
        [i, axis] for axis in range(AXES) for i, f in enumerate(ints(read[spoke_of(axis, 0)])) if f == 0
    ]
    unsprung = clock.unsprung().gears[0]
    return {
        "i": clock.ticks,
        "X": ints(regulator.now),
        "content": ints(load),
        "turned": [i for i, t in enumerate(clock.turned_over.reshape(-1).tolist()) if t],
        "frozen": [i for i, p in enumerate(ints(mesh_rate)) if p == 0],
        "held": held,
        "current": [ints(mesh_lead(unsprung, spoke_of(axis, 0))) for axis in range(AXES)],
    }


def rewind(clock: Clock, hashes: list[str]) -> dict[str, int]:
    """The rewind: as many ticks back as states were kept, each compared with the kept state's hash."""
    exact = 0
    for k in range(len(hashes)):
        clock.tick(-1)
        exact += state_hash(clock) == hashes[len(hashes) - 1 - k]
    return {"intervals": len(hashes), "exact": exact}


def forward(
    clock: Clock, tick_count: int, back: int, out: Callable[[str], Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """The ticks run forward: the reader's rows at the marks written as they come, a clock line at every tick, the last `back` states' hashes kept for the rewind."""
    t0 = time.monotonic_ns()
    marks = (
        {1, tick_count}
        | {(k * tick_count) // MARKS for k in range(1, MARKS)}
        | {tick_count // e for e in EARLY}
    )
    rows: list[dict[str, Any]] = []
    clocks: list[dict[str, Any]] = []
    hashes = []
    maxbits = 0
    for t in range(tick_count):
        if back and t >= tick_count - back:
            hashes.append(state_hash(clock))
        clock.tick()
        maxbits = max(maxbits, census(clock)[1])
        clocks.append(clock_lines(clock))
        if clock.ticks in marks:
            rows.append(
                dict(
                    reading(clock, maxbits),
                    milliseconds=(time.monotonic_ns() - t0) // (THOUSAND * THOUSAND),
                )
            )
            out(json.dumps(rows[-1]))
    return rows, clocks, hashes


def chart(
    calibre: dict[str, Any],
    piece: dict[str, Any],
    back: int = 0,
    out: Callable[[str], Any] = print,
    clock_of: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    """The piece's ticks run (`forward`), then `back` ticks rewound and compared by the state's hash (`rewind`); the chart returned; `clock_of` the clock's class (the engine's unless a toy names its own)."""
    from event_universe.clock import (
        Clock,  # the writer stands below the Clock, which reads the rewind note here
    )

    clock = (Clock if clock_of is None else clock_of)(calibre, piece)
    tick_count = int(piece["intervals"])
    rows, clocks, hashes = forward(clock, tick_count, back, out)
    kept_log = list(clock.log)
    returned = rewind(clock, hashes) if back else None
    if returned:
        out(json.dumps({"run back": returned}))
    counts = {k: str(v) for k, v in clock.counts.items()}
    out(json.dumps({"counts": counts}))
    return {
        "world": piece,
        "universe": calibre,
        "den": clock.rim,
        "cube": clock.cube,
        "intervals": tick_count,
        "gapped": [
            (str(r.ratio[0]), str(sine_rim(r.ratio[0], clock.rim))) for r in clock.sprung if r.ratio
        ],
        "planes": [str(r.ratio[0]) for r in clock.hands() if r.ratio],
        "T": clock.key,
        "gamma": clock.full_rate,
        "G": clock.G,
        "counts": counts,
        "turns": clock.turnovers,
        "rows": rows,
        "nodes": clocks,
        "run_back": returned,
        "log": kept_log,
    }


def main(argv: list[str]) -> None:
    """The writer from the command line: the piece file, the output file, `back N` for the rewind."""
    sys.set_int_max_str_digits(0)
    _, piece_path, out_path, *_rest = argv
    calibre, piece = read_piece(piece_path)
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    found = chart(calibre, piece, back, lambda line: print(line, flush=True))
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(found, out)


if __name__ == "__main__":
    main(sys.argv)
