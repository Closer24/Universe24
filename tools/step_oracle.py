"""The step's oracle, a host tool (the engine matches the law in its implementation, not only in its results): the law's first form of Rule3, SUM over the six Ports of R_ij m_ij + S a_now - w a_before + r, kept here and in no file of src/, with the one Node's interval around it (the six arrivals through the Ports, the planes two lines as one under the Link's pairs, the faces presented by the engine's own `presented`, the lattice's acts around the step the engine's own), run against the engine's step, Rule3's flux line (src/event_universe/flux.py, core/rule3.rule3), on one world: two boards from one load, one stepped by the oracle, the other by `Lattice.step`; after every interval every line's now, before and remainder of every family, every held line's write remainder, every phase line, the interval, the shape and the output lines are compared, the first difference named; then the engine's board is run back with the record the gate's way (tools/back_in_time.py: the faces from the `face` lines, each interval's lays crossed), `Lattice.step_inverse` at every interval against the forward state's digest, and the lay bit for bit at the end. The verdict EQUAL with the intervals run, or DIFFERS with the first interval, array and Node. tests/test_step_oracle.py runs it on two small worlds inside the suite's bound; every example world and the time paper's run are run by this tool (the 36 cases and their caps in tests/test_step_oracle.py's docstring).

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/step_oracle.py --intervals 40 <world>.json
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import board_readings, flux, node, swap
from event_universe.bookings import Bookings, booked_of
from event_universe.core.ports import AXES, Wrap, arrival
from event_universe.core.rule3 import Rule
from event_universe.lattice import Lattice
from event_universe.loader.derived import PLANE
from event_universe.readings import ports
from event_universe.records import Booking, Record, level_at, record_slice
from event_universe.world_files import load_world

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("back_in_time", ROOT / "tools" / "back_in_time.py")
BACK = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(BACK)  # type: ignore[union-attr]


def arrivals_rule3(reads, arrivals, self_coefficient, wall, now, other, carry, direction=1):  # type: ignore[no-untyped-def]
    """The law's first form of Rule3, by the six arrivals and the own weight: u = sigma (SUM over the Ports of R_ij arr_j + S a_now - w other) + carry, the quotient sigma (u div w) and the remainder u mod w; the engine steps by the flux line (core/rule3.rule3), the same integers by the identity S = 2 w - D - SUM R_ij."""
    total = self_coefficient * now
    total -= wall * other
    for read, arrived in zip(reads, arrivals, strict=True):
        total += read * arrived
    total = direction * total + carry
    quotient = total // wall
    return direction * quotient, total - wall * quotient


def oracle_step(record: Record, rule: Rule, wrap: Wrap, direction: int = 1) -> Record:
    """The first form's step on one line: the six arrivals of the level the step starts from, the first form."""
    reads, self_coefficient, wall, _mass = rule
    level, other = (record.now, record.before) if direction == 1 else (record.before, record.now)
    arrived = ports(level, wrap)
    found, remainder = arrivals_rule3(
        reads, arrived, self_coefficient, wall, level, other, record.remainder, direction
    )
    if direction == 1:
        return Record(np.asarray(found), record.now, np.asarray(remainder))
    return Record(record.before, np.asarray(found), np.asarray(remainder))


def oracle_step_plane(re, im, rule, wrap, direction, pairs):  # type: ignore[no-untyped-def]
    """The first form's step on a plane's two lines as one, every Link's pair on the two arrivals, the plain reads where no pair."""
    reads, self_coefficient, wall, _mass = rule
    now = (level_at(re, direction), level_at(im, direction))
    other = (re.before, im.before) if direction == 1 else (re.now, im.now)
    arrived = tuple(
        tuple(arrival(level, axis, side) for axis in range(AXES) for side in (1, -1)) for level in now
    )
    folded = (
        ((reads, arrived[0]), (reads, arrived[1]))
        if pairs is None
        else (
            (pairs[0] + tuple(-x for x in pairs[1]), arrived[0] + arrived[1]),
            (pairs[0] + pairs[1], arrived[1] + arrived[0]),
        )
    )
    stepped = [
        arrivals_rule3(
            read, at, self_coefficient, wall, now[part], other[part], record.remainder, direction
        )
        for part, (record, (read, at)) in enumerate(zip((re, im), folded, strict=True))
    ]
    levels, remainders = ([np.asarray(found[i]) for found in stepped] for i in (0, 1))
    u, v = (other, levels) if direction == 1 else (levels, other)
    lines = [
        Record(levels[part], record.now, remainders[part])
        if direction == 1
        else Record(record.before, levels[part], remainders[part])
        for part, record in enumerate((re, im))
    ]
    first = [Record(now[part], np.asarray(u[part]), remainders[part]) for part in range(PLANE)]
    second = [Record(np.asarray(v[part]), now[part], remainders[part]) for part in range(PLANE)]
    return lines, (first, second)


def oracle_step_family(index, families, states, rule, wrap, direction, record, pairs):  # type: ignore[no-untyped-def]
    """The first form's step on one record: line by line; a plane family plane by plane, the two lines as one under the Links' pairs where the record is turned or folded, two plain lines where it is not."""
    family, state = families[index], states[index]
    span = record_slice(family, record)
    own = state.lines[span]
    if not family.plane:
        traced = (
            family.axes and not family.wronskian
        )  # a holder of the content's tension lines: the shear's momentum, the lattice's step
        found = [
            oracle_step(line, rule, wrap, direction)
            if not (traced and 1 <= number - span.start <= AXES)
            else line
            for number, line in enumerate(own, span.start)
        ]
        return found, ((own, found) if direction == 1 else (found, own))
    lines: list[Record] = []
    first: list[Record] = []
    second: list[Record] = []
    for start in range(0, len(own), PLANE):
        pair = own[start], own[start + 1]
        found, (begun, left) = oracle_step_plane(*pair, rule, wrap, direction, pairs)
        lines, first, second = lines + found, first + begun, second + left
    return lines, (first, second)


def oracle_step_records(
    board: Lattice, index: int, direction: int
) -> tuple[list[Record], list[Booking]]:
    """The first form's step on every record of a family, with the engine's own read, rule and pairs (`flux.pairs_of` shares them) and the faces as `meeting.stepped` takes them."""
    families, states, wrap = board.families, board.states, board.wrap
    gamma, unit = board.world.node_clock, board.unit
    lines: list[Record] = []
    bookings: list[Booking] = []
    for record in range(families[index].records):
        content, factors = node.read(index, families, states, direction, wrap, gamma, unit, record)
        rule = node.rule_of(families[index], gamma, content, factors, unit)
        pairs = flux.pairs_of(
            index, families, states, direction, wrap, gamma, content, factors, record, board.amplitude
        )
        found, booking = oracle_step_family(
            index, families, states, rule, wrap, direction, record, pairs
        )
        lines, bookings = lines + found, bookings + [booking]
    return lines, bookings


def oracle_interval(board: Lattice) -> None:
    """The one Node's `Lattice.step` with the oracle's step in the place of the engine's; every other act the engine's own, in the engine's order: the fifth act (swap.kept before the phase act, swap.stepped after the held writes) and the densities' reading after it, the state at the interval's end (2026-10-23, The floor)."""
    board.interval, forms, turns = board.interval + 1, Bookings(), Bookings()
    kept_state = swap.kept(board)
    node.phase_act(board.held, board.families, board.states, 1, board.wrap, board.world.node_clock)
    senses, stresses = board_readings.sense_currents(board), board_readings.stresses(board)
    rulers, begun = board.rulers(1), [s.lines for s in board.states]
    found = {index: oracle_step_records(board, index, 1) for index in range(len(board.families))}
    for index, (lines, bookings) in found.items():
        family, state = board.families[index], board.states[index]
        for number, record in enumerate(lines):
            board.bounded(family.name, record, number == 0 and family.motion_volume)
        if family.quanta:
            booked = booked_of(board.families, index, bookings)
            for held, gained in zip((forms, turns), booked, strict=True):
                held.update(gained)
        state.lines = lines
    for index in board.held:
        board.held_write(index, forms, turns, 1, stresses, senses, rulers, begun)
    swap.stepped(board, kept_state)


def arrays(board: Lattice) -> list[tuple[str, np.ndarray]]:
    """Every array of every family with its name: the lines, the write remainders, the phase lines."""
    found: list[tuple[str, np.ndarray]] = []
    for family, state in zip(board.families, board.states, strict=True):
        for number, line in enumerate(state.lines):
            for key in ("now", "before", "remainder"):
                found.append((f"{family.name}[{number}].{key}", np.asarray(getattr(line, key))))
        for number, value in enumerate(state.write_remainders):
            found.append((f"{family.name}.write_remainders[{number}]", np.asarray(value)))
        for row, lines in enumerate(state.phases):
            for number, line in enumerate(lines):
                for key in ("now", "before", "remainder"):
                    found.append(
                        (f"{family.name}.phases[{row}][{number}].{key}", np.asarray(getattr(line, key)))
                    )
    return found


def digest(board: Lattice) -> str:
    """One digest of the board's state: the interval, the shape and every array."""
    h = hashlib.sha256()
    h.update(repr((board.interval, tuple(board.shape))).encode())
    for label, value in arrays(board):
        h.update(label.encode())
        h.update(
            repr(np.asarray(value, dtype=object).tolist()).encode()
        )  # the values, whatever the arrays' kind
    return h.hexdigest()


def first_difference(a: Lattice, b: Lattice) -> str | None:
    """The first array and Node at which two boards differ, with the two values, or None where they agree bit for bit."""
    if (a.interval, tuple(a.shape)) != (b.interval, tuple(b.shape)):
        return f"interval/shape: {a.interval, list(a.shape)} against {b.interval, list(b.shape)}"
    for (label, was), (_label, now) in zip(arrays(a), arrays(b), strict=True):
        if was.shape != now.shape:
            return f"{label}: the shape {list(was.shape)} against {list(now.shape)}"
        where = np.argwhere(was != now)
        if len(where):
            at = tuple(int(i) for i in where[0])
            return f"{label} at the Node {list(at)}: the oracle {was[at]} against the engine {now[at]}"
    return None


LINE_LABEL = re.compile(
    r"^(?P<family>[^.\[]+)\[(?P<line>\d+)\]\.(?P<key>now|before)$"
)  # a record line's levels


def verdict(board: Lattice, intervals: int | None) -> dict[str, Any]:
    """The oracle against the engine on a loaded board: two boards from the one load, `intervals` forward (fewer where the run ends or the world has fewer) compared at every interval, then the engine's board back with the record to the lay. Where a click wrote at the record's birth (the one meeting, 2026-10-20: the sides' draws run the record back to its birth and write the realised port's coefficients there), the frames the forward run recorded before the last click's close are the possibilities' run and the inverse from after the click returns the realised past (ALGEBRA.md, The click is the meeting of the future with the past), so the step back is held to the recorded frames at and after the last such click's close alone (a one-part record's click writes no birth and its world keeps the full comparison), and the lay is held recovered up to the write: each record line's two levels times the cumulative coefficient written on its part (`written_lay`), the remainders and every other array the lay's own; a world without a click is held at every frame and the lay itself, as before."""
    oracle, engine = board, copy.deepcopy(board)
    lines_oracle: list[dict[str, object]] = []
    lines_engine: list[dict[str, object]] = []
    oracle.output, engine.output = lines_oracle.append, lines_engine.append
    ticks = board.world.intervals if intervals is None else min(intervals, board.world.intervals)
    lay = [(label, value.copy()) for label, value in arrays(engine)]
    digests = {engine.interval: digest(engine)}
    run = 0
    for _ in range(ticks):
        oracle_interval(oracle)
        engine.step()
        run += 1
        digests[engine.interval] = digest(engine)
        difference = first_difference(oracle, engine)
        if difference is not None:
            return {"verdict": "DIFFERS", "interval": engine.interval, "what": difference}
        if lines_oracle != lines_engine:
            return {"verdict": "DIFFERS", "interval": engine.interval, "what": "the output lines differ"}
    clicks = [
        int(str(line["interval"]))
        for line in lines_engine
        if line["event"] == "credit" and line.get("order") is not None
    ]  # a click that wrote at the birth: a record of several parts' credit line carries `order`
    realised_from = max(
        clicks, default=0
    )  # below the last click's close the inverse returns the realised past
    for _ in range(run):
        BACK.crossed(engine, lines_engine)
        engine.step_inverse()
        if engine.interval >= realised_from and digest(engine) != digests[engine.interval]:
            return {
                "verdict": "DIFFERS",
                "interval": engine.interval,
                "what": "the step back misses the forward state",
            }
    for (label, was), (_label, now) in zip(lay, arrays(engine), strict=True):
        if was.shape != now.shape or not np.array_equal(was, now):
            return {
                "verdict": "DIFFERS",
                "interval": engine.interval,
                "what": f"the lay is not recovered on {label}"
                + (" up to the click's write" if clicks else ""),
            }
    return {
        "verdict": "EQUAL",
        "intervals": run,
        "back": run,
        "lines": len(lines_engine),
        "shape": list(engine.shape),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("world", type=Path, help="the world file, with its mode file beside it")
    parser.add_argument(
        "--intervals",
        type=int,
        default=None,
        help="the intervals to compare (the world's own without it)",
    )
    args = parser.parse_args(argv)
    print(json.dumps(verdict(Lattice(load_world(args.world)), args.intervals)))


if __name__ == "__main__":
    main()
