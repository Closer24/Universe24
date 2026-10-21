"""The step's oracle, a host tool (the engine matches the law in its implementation, not only in its results, and this tool holds the step to the 2.0.0 step it replaced): the law's first form of Rule3, SUM over the six Ports of R_ij m_ij + S a_now - w a_before + r, kept here and in no file of src/, with the 2.0.0 step around it (the six arrivals through the Ports, the planes two lines as one under the Link's pairs, the faces presented by the engine's own `presented`, the lattice's acts around the step the engine's own), run against the engine's step, Rule3's flux line (src/event_universe/flux.py, core/rule3.rule3), on one world: two boards from one load, one stepped by the oracle, the other by `Lattice.step`; after every interval every line's now, before and remainder of every family, every held line's write remainder, every phase line, the interval, the shape and the output lines are compared, the first difference named; then the engine's board is run back with the record the gate's way (tools/back_in_time.py: the faces from the `face` lines, each interval's lays crossed), `Lattice.step_inverse` at every interval against the forward state's digest, and the lay bit for bit at the end. The verdict EQUAL with the intervals run, or DIFFERS with the first interval, array and Node. tests/test_step_oracle.py runs it on two small worlds inside the suite's bound; every example world and the time paper's run are run by this tool (the 36 cases and their caps in tests/test_step_oracle.py's docstring).

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
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import board_readings, credit, emission, flux, front, growth, meeting, node
from event_universe.bookings import Bookings, booked_of
from event_universe.core.ports import AXES, Wrap, arrival
from event_universe.core.rule3 import Rule
from event_universe.features.click import presented
from event_universe.lattice import Lattice
from event_universe.loader.derived import PLANE
from event_universe.node_detector import weighed_currents
from event_universe.plane import NO_FACE, Faces
from event_universe.readings import ports
from event_universe.records import Booking, Record, level_at, record_slice
from event_universe.take import faces_presented
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


def oracle_step(
    record: Record, rule: Rule, wrap: Wrap, direction: int = 1, fill: int = 0, faces: Faces = NO_FACE
) -> Record:
    """The 2.0.0 step on one line: the six arrivals of the level the step starts from, the faces presented, the first form."""
    reads, self_coefficient, wall, _mass = rule
    level, other = (record.now, record.before) if direction == 1 else (record.before, record.now)
    arrived = ports(level, wrap, fill)
    if faces[0]:
        arrived = presented(arrived, rule, level, other, record.remainder, *faces, direction)
    found, remainder = arrivals_rule3(
        reads, arrived, self_coefficient, wall, level, other, record.remainder, direction
    )
    if direction == 1:
        return Record(np.asarray(found), record.now, np.asarray(remainder))
    return Record(record.before, np.asarray(found), np.asarray(remainder))


def oracle_step_plane(re, im, rule, wrap, direction, faces, pairs):  # type: ignore[no-untyped-def]
    """The 2.0.0 step on a plane's two lines as one, every Link's pair on the two arrivals, the plain reads where no pair."""
    reads, self_coefficient, wall, _mass = rule
    now = (level_at(re, direction), level_at(im, direction))
    other = (re.before, im.before) if direction == 1 else (re.now, im.now)
    arrived = tuple(
        tuple(arrival(level, axis, side, wrap) for axis in range(AXES) for side in (1, -1))
        for level in now
    )
    if faces[0][0] or faces[1][0]:
        faced = [
            presented(at, rule, now[k], other[k], (re, im)[k].remainder, *faces[k], direction)
            if faces[k][0]
            else at
            for k, at in enumerate(arrived)
        ]
        arrived = (faced[0], faced[1])
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


def oracle_step_family(index, families, states, rule, wrap, direction, record, faces, pairs):  # type: ignore[no-untyped-def]
    """The 2.0.0 step on one record: line by line; a plane family plane by plane, the two lines as one under the Links' pairs where the record is turned or folded, two plain lines where it is not."""
    family, state = families[index], states[index]
    span = record_slice(family, record)
    own = state.lines[span]
    faced: Mapping[int, Faces] = dict(faces or {})
    if not family.plane:
        found = [
            oracle_step(
                line,
                rule,
                wrap,
                direction,
                family.rest if number == 0 else 0,
                faced.get(number, NO_FACE),
            )
            for number, line in enumerate(own, span.start)
        ]
        return found, ((own, found) if direction == 1 else (found, own))
    lines: list[Record] = []
    first: list[Record] = []
    second: list[Record] = []
    for start in range(0, len(own), PLANE):
        pair = own[start], own[start + 1]
        at = faced.get(span.start + start, NO_FACE), faced.get(span.start + start + 1, NO_FACE)
        found, (begun, left) = oracle_step_plane(*pair, rule, wrap, direction, at, pairs)
        lines, first, second = lines + found, first + begun, second + left
    return lines, (first, second)


def oracle_step_records(
    board: Lattice, index: int, direction: int
) -> tuple[list[Record], list[Booking]]:
    """The 2.0.0 step on every record of a family, with the engine's own read, rule and pairs (`flux.pairs_of` shares them), the cuts and the faces as `meeting.stepped` takes them."""
    families, states, wrap = board.families, board.states, board.wrap
    gamma, unit, cut = board.world.node_clock, board.unit, meeting.cut(board, index)
    faces = faces_presented(board, index)
    lines: list[Record] = []
    bookings: list[Booking] = []
    for record in range(families[index].records):
        content, factors = node.read(index, families, states, direction, wrap, gamma, unit, record, cut)
        rule = node.rule_of(families[index], gamma, content, factors, unit)
        pairs = flux.pairs_of(
            index, families, states, direction, wrap, gamma, content, factors, record, board.amplitude
        )
        found, booking = oracle_step_family(
            index, families, states, rule, wrap, direction, record, faces, pairs
        )
        lines, bookings = lines + found, bookings + [booking]
    return lines, bookings


def oracle_interval(board: Lattice) -> None:
    """The 2.0.0 `Lattice.step` with the oracle's step in the place of the engine's; every other act the engine's own."""
    if board.ended is not None:
        raise RuntimeError(f"the run ended at interval {board.interval}: {board.ended}")
    if not growth.grow(board):
        return
    board.interval, forms, turns = board.interval + 1, Bookings(), Bookings()
    node.phase_act(board.held, board.families, board.states, 1, board.wrap, board.world.node_clock)
    currents, senses, stresses = (
        board_readings.currents(board),
        board_readings.sense_currents(board),
        board_readings.stresses(board),
    )
    rulers, begun, weighed = board.rulers(1), [s.lines for s in board.states], weighed_currents(board)
    found = {index: oracle_step_records(board, index, 1) for index in range(len(board.families))}
    for index, (lines, bookings) in found.items():
        family, state = board.families[index], board.states[index]
        for record in lines:
            board.bounded(family.name, record)
        if family.quanta:
            booked = booked_of(board.families, index, bookings)
            for held, gained in zip((forms, turns), booked, strict=True):
                held.update(gained)
        state.lines = lines
    board.report(currents, weighed, forms, begun)
    for index in board.held:
        board.held_write(index, forms, turns, 1, stresses, senses, rulers)
    if credit.counted_windows(board):
        meeting.closed(board)
    meeting.jumped(board)
    emission.sourced(board)
    front.advanced_fronts(board)


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
    """One digest of the board's state: the interval, the shape, the offset and every array."""
    h = hashlib.sha256()
    h.update(repr((board.interval, tuple(board.shape), tuple(board.offset))).encode())
    for label, value in arrays(board):
        h.update(label.encode())
        h.update(
            repr(value.tolist()).encode()
            if value.dtype == object
            else np.ascontiguousarray(value).tobytes()
        )
    return h.hexdigest()


def first_difference(a: Lattice, b: Lattice) -> str | None:
    """The first array and Node at which two boards differ, with the two values, or None where they agree bit for bit."""
    if (a.interval, tuple(a.shape), a.ended is None) != (b.interval, tuple(b.shape), b.ended is None):
        return f"interval/shape/ended: {a.interval, list(a.shape), a.ended} against {b.interval, list(b.shape), b.ended}"
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


def written_lay(board: Lattice, label: str, laid: np.ndarray) -> np.ndarray:
    """The lay's array as the click's write at the birth left it (ALGEBRA.md, The click is the meeting of the future with the past: the lay is not taken back, the written birth stands): a record line's two levels times the cumulative coefficient written on its part (`credit.Books.written`, `meeting_back.parts_of`), the remainders, the write remainders, the phase lines and every unwritten family the lay's own."""
    found = LINE_LABEL.match(label)
    if found is None:
        return laid
    index = [family.name for family in board.families].index(found["family"])
    written = board.credit.written.get(index)
    if written is None:
        return laid
    part = credit.parts_of(board.families[index], len(board.states[index].lines))[int(found["line"])]
    re, im = written[part]  # the pair written on the part: the oracle's arithmetic is the real ports'
    assert im == 0, "the oracle reads real-port worlds; a turned side's write is the two-term test's"
    return np.asarray(laid * re)


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
        if oracle.ended is not None or engine.ended is not None:
            if str(oracle.ended) != str(engine.ended):
                return {
                    "verdict": "DIFFERS",
                    "interval": engine.interval,
                    "what": f"ended: {oracle.ended} against {engine.ended}",
                }
            break
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
    BACK.faces_from(engine, lines_engine)
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
        if was.shape != now.shape or not np.array_equal(written_lay(engine, label, was), now):
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
