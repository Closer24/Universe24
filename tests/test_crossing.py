"""The crossing rule (2026-09-21; the model owner's record 158 of
2026-09-20, "the step reads the crossed Link"; the physicist's design
docs/designs/crossing/DESIGN.md; docs/BEAM_LAW.md section 3 step 4 and note
48): a row and a body meet ONCE, at the crossing of their world lines. The
body's step precedes the law (`_move` before `nature_beam`), so the reading
of an interval finds the body at its destination; a body reads every
arrival at its Nodes as before, and in the interval of a step it also
reads the rows that crossed its Link the other way (C1, the swap) and the
rows resident at the Node it entered whose motion is against the step
(C2), never a row that came over its Link behind it, in that interval
(C3', with the step) or the next after a rest at the origin (C3'', the
leapfrog), nor a resident row moving with it (C2'). The body's own two
last Links (`Measured.step_port`, `last_step_port`) and the rows' own last
two steps off the flight rule are the only inputs; nothing is kept at a
Node. The world key `doppler` and the grain G of `doppler-v1` are deleted
with it (MIGRATION): a moving reader's Doppler is the COUNT of the rows it
crosses. The expected integers of docs/TEST_EXPECTATIONS.md ("The crossing
rule"), written down before the first run:

(a) the experimenter's streams (record 151's test, the design's section
    2): a lamp at x = 0 of a bar of 64 releasing one row of amount 1 per
    interval on +x, the stream pre-filled (the row of age tau at m(tau) =
    (2 tau Q + T) // (2 T), Q 64, T 110: 32 Links per 55 intervals), a
    reader of content M = 21 x 2^16 at x = 40 whose momentum makes it
    step one Link per k intervals exactly (|p| = Q S M / 3 at k = 4, Q S M
    / 7 at k = 8; the sign minus toward the lamp), `read` on the beam, the
    charges cancelling the push: toward at k = 4 the reader reads 45 rows
    in 32 intervals, the windows of k intervals ending at each step [5, 6,
    6, 5, 6, 6, 6, 5]; toward at k = 8 58 in 48, [9, 10, 10, 9, 10, 10];
    away at k = 4 19 in 32, [3, 2, 2, 2, 3, 2, 2, 3]; away at k = 8 38 in
    48, [7, 6, 6, 6, 7, 6]; at rest 48 in 48 (one per interval); every
    `read` line's amount 1, 2 or 3; the steps at the ticks 4, 8, ... (8,
    16, ...); no row read twice: the same worlds with `measure` (a row
    absorbed at its first meeting cannot be met again) click exactly the
    same counts; the books balanced, the momentum constant. The
    comparison pair: `toward_k4_probe_off` (a third column `probe`, the
    value 1 on the beam and [1, M] on the reader, the sign minus on both:
    the push is the flow read, 64 label units per row, toward the lamp)
    reads 45 rows and pushes 64 x 45 = 2880 toward the lamp, -2880 on x,
    with the steps at the same ticks; `toward_k4_probe_on` (the same with
    `"doppler": true`) is refused at parsing as an unknown key;
(b) a reader at rest is unchanged: the control at rest above reads one
    row per interval, as the rule as built read it; the gate set replayed
    byte-identical in its records is the research replay of VALIDATION;
(c) beyond the axis, on a GameBoard [64, 64, 1] with every Node on
    exactly one digital line of the stream's direction (one lamp per
    line, one row per interval per line, the lines pre-filled; the reader
    at (40, 40, 0) stepping +x at k = 4 for 32 intervals), the counts
    written down from the rule transcribed on the lines' geometry
    (docs/designs/crossing/crossing_2d.py, no engine code): a transverse
    stream (rows +y, one lamp per column) is read at exactly the rest
    rate, 32 in 32, one at every interval (C2 with u . e = 0: the entered
    Node's rows are not met; every arrival met); a stream on the face
    diagonal (1, 1, 0) moving with the step (the lamps at (x, 0) for even
    x and (0, y) for even y from 2) is read 24 in 32, in the pattern 1, 1,
    1, 0, 0, 1, 1, 1 per four intervals, twice: at the steps whose Link
    the line takes along +x the arrival came over the body's Link with it
    (C3') and the next interval's arrival rested at the origin during the
    step (C3''), at the steps whose Link the line takes along +y the
    arrival is met (the design's "at exactly the rest rate" for this
    stream is not what the rule gives on the lattice: 24, not 32); a
    stream on (-1, 1, 0) against the step (the lamps at (x, 0) for odd x
    and (63, y) for even y from 2) is read 36 in 32, one per interval and
    2 at the steps at the ticks 4, 12, 20, 28, where a row crossed the
    body's Link the other way (C1); no resident row against the step at
    any entered Node in these 32 intervals (the design's "2 or 3 at every
    step" is a density the lines do not have); no row twice in any of
    the three (the `measure` counts equal);
(d) one row met once: a single row of amount 1 in transit on +x at age 0
    (its Node at tick t the start x_0 + m(t), m(0 .. 13) = 0, 1, 1, 2, 2,
    3, 3, 4, 5, 5, 6, 6, 7, 8) and the experimenter's reader at k = 4, no
    stream: toward, the row at x_0 = 30 and the reader at 40 stepping -x
    (39, 38, 37 after the ticks 4, 8, 12): at tick 12 the row moves 36 ->
    37 as the reader enters 37 from 38, C3 with both arrived: ONE `read`
    line, at tick 12, amount 1, nothing at 13 when the row moves on to
    38; away with the leapfrog after a rest (C3''), the row at x_0 = 30
    and the reader at 32 stepping +x (33 after tick 4): the row arrives
    at 32 at tick 3, the reader at rest, `read` at tick 3; at tick 4 the
    reader steps 32 -> 33 while the row rests at 32; at tick 5 the row
    moves 32 -> 33 into the reader's Node with e' = +x and s_2 = 0, NOT
    met; at tick 8 the reader steps 33 -> 34 as the row moves 34 -> 35,
    nothing: exactly one `read` line, at tick 3; away with the entered
    Node's resident row moving with the step (C2'), the row at x_0 = 31:
    the row arrives at 32 at tick 1, `read` at tick 1; it rests at 32 at
    tick 2, moves to 33 at tick 3, rests there at tick 4 as the reader
    enters 33, u . e > 0, NOT met: exactly one `read` line, at tick 1;
    each world's books balanced;
(e) the sum over a period: the stream pre-filled over a bar of 512, the
    reader at x = 400 crossing 32 Links = 32 k intervals (the stream 55
    rows per 32 Links exactly): toward 128 + 55 = 183 reads at k = 4 and
    256 + 55 = 311 at k = 8, exactly; away 128 - 55 + 1 = 74 and 256 - 55
    + 1 = 202, the one extra the row co-located with the reader at the
    first interval (a boundary of the window, not of the rule): the rate
    1 + v / c toward and 1 - v / c away with v = 1 / k and c = 32 / 55,
    as a count;
(f) the report of the fast steps (the design's section 2, "not proved"):
    a body faster than one Link per two intervals, |p| > Q S M, can cross
    a Link in the interval right after another; the engine counts those
    Links (`NatureBeamSimulation.fast_steps`, `run.json`'s `fast_steps`),
    no refusal. Content 1, width 1 (Q S M = 64), no rows: at the momentum
    96 (D = 160, the drive 96 per self-creation) the Links fall at the
    self-creations 2, 4, 5, 7, 9, 10, ..., every fifth one right after
    another: 18 Links in 30 intervals and 6 fast; at 128 (D = 192) at 2,
    3, 5, 6, ...: 20 Links and 10 fast; at 64 (D = 128, one Link per two
    intervals exactly) 15 Links and 0 fast; at 32 (D = 96) 10 and 0; the
    runner's record carries the count.
"""

from __future__ import annotations

import copy
import json

import numpy as np
import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight
from event_universe.events.world import LABEL_SCALE, step_divisor
from event_universe.runner import run_initialization

Q = LABEL_SCALE
T_HEADING = 110
PLUS_X = [1, 0, 0]
PLUS_Y = [0, 1, 0]
M = 21 << 16
QSM = Q * 1 * M
MOMENTUM = {4: QSM // 3, 8: QSM // 7}
LAMP, READER = 1, 2


def m_heading(tau: int) -> int:
    """Links made by age tau on a heading, (2 tau Q + T) // (2 T)."""
    return (2 * tau * Q + T_HEADING) // (2 * T_HEADING)


def stream(length: int) -> list[dict[str, object]]:
    """The steady beam of the lamp at x = 0: the row of age tau at m(tau)."""
    rows = []
    tau = 0
    while m_heading(tau) < length:
        rows.append(
            {
                "position": [m_heading(tau), 0, 0],
                "family": "beam",
                "number": LAMP,
                "direction": PLUS_X,
                "amount": 1,
                "phase": 0,
                "age": tau,
            }
        )
        tau += 1
    return rows


def bar(
    momentum: int,
    ticks: int,
    *,
    length: int = 64,
    start: int = 40,
    rule: str = "read",
    probe: bool = False,
    rows: list[dict[str, object]] | None = None,
    release: list[int] | None = None,
) -> dict[str, object]:
    """The experimenter's bar (record 151): the lamp at x = 0, the reader
    of content M at `start` with the momentum on x, the stream pre-filled
    (or the declared `rows`)."""
    beam: dict[str, object] = {"name": "beam", "quantum": 0, "charge": 1, "phase": False}
    body: dict[str, object] = {"name": "body", "quantum": 0, "charge": 1, "phase": False}
    if probe:
        beam["columns"] = {"probe": {"value": 1, "sign": -1}}
        body["columns"] = {"probe": {"value": [1, M], "sign": -1}}
    return {
        "law": "beam",
        "model_id": "crossing-bar-test",
        "shape": [length, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1] if release is None else release,
        "suspension": 0,
        "width": 1,
        "age_bound": 4096,
        "families": [beam, body],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "beam",
                "amount": 1,
                "fixed": True,
                "directions": [PLUS_X],
            },
            {
                "position": [start, 0, 0],
                "family": "body",
                "amount": M,
                "momentum": [momentum, 0, 0],
                "table": {"beam": rule},
            },
        ],
        "in_transit": stream(length) if rows is None else rows,
    }


def run(world: dict[str, object]) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(copy.deepcopy(world)), records.append)
    for _ in range(int(str(world["ticks"]))):
        simulation.step()
    assert simulation.books()["balanced"]
    return simulation, records


def met(records: list[dict[str, object]], number: int, event: str = "read") -> list[dict[str, object]]:
    return [r for r in records if r["event"] == event and r["measured"] == number]


def per_tick(
    records: list[dict[str, object]], number: int, ticks: int, event: str = "read"
) -> list[int]:
    found = [0] * (ticks + 1)
    for line in met(records, number, event):
        found[int(str(line["tick"]))] += int(str(line["amount"]))
    return found[1:]


def windows(counts: list[int], k: int) -> list[int]:
    return [sum(counts[lo : lo + k]) for lo in range(0, len(counts) - len(counts) % k, k)]


def steps_of(records: list[dict[str, object]], number: int) -> list[int]:
    return [int(str(r["tick"])) for r in records if r["event"] == "step" and r["number"] == number]


# -- (a), (b) ----------------------------------------------------------------------

STREAMS = {
    "toward_k4": (4, -1, 32, 45, [5, 6, 6, 5, 6, 6, 6, 5]),
    "toward_k8": (8, -1, 48, 58, [9, 10, 10, 9, 10, 10]),
    "away_k4": (4, 1, 32, 19, [3, 2, 2, 2, 3, 2, 2, 3]),
    "away_k8": (8, 1, 48, 38, [7, 6, 6, 6, 7, 6]),
    "rest": (None, 0, 48, 48, [48]),
}


@pytest.mark.parametrize("case", sorted(STREAMS))
def test_the_experimenters_streams_are_read_at_the_crossing_rate(case):
    """(a), (b)."""
    k, sense, ticks, expected, expected_windows = STREAMS[case]
    momentum = 0 if k is None else sense * MOMENTUM[k]
    if k is not None:
        assert (QSM + abs(momentum)) // abs(momentum) == k
        assert step_divisor(momentum, M, 1) == QSM + abs(momentum)
    simulation, records = run(bar(momentum, ticks))
    reader = simulation.measured[READER]
    counts = per_tick(records, READER, ticks)
    assert sum(counts) == expected, case
    assert windows(counts, ticks if k is None else k) == expected_windows, case
    assert set(counts) <= {0, 1, 2, 3}
    assert all(int(str(r["amount"])) in (1, 2, 3) for r in met(records, READER))
    assert steps_of(records, READER) == ([] if k is None else list(range(k, ticks + 1, k)))
    assert reader.momentum == [momentum, 0, 0] and reader.position[0] == 40 + (
        0 if k is None else sense * ticks // k
    )
    # No row twice: absorbed at its first meeting, every row is met once,
    # and the counts are the same.
    clicked, records_m = run(bar(momentum, ticks, rule="measure"))
    assert per_tick(records_m, READER, ticks, "click") == counts, case
    assert clicked.measured[READER].momentum == [momentum, 0, 0]
    assert clicked.measured[READER].clicks[0] == expected


def test_the_comparison_pair_of_the_probe():
    """(a), the probe column: the push is the count in label units; the
    key `doppler` is refused."""
    simulation, records = run(bar(-MOMENTUM[4], 32, probe=True))
    reads = met(records, READER)
    assert sum(int(str(r["amount"])) for r in reads) == 45
    assert sum(int(str(r["push"][0])) for r in reads) == -64 * 45 == -2880  # type: ignore[index]
    assert all(r["push"][1:] == [0, 0] for r in reads)  # type: ignore[index]
    assert simulation.measured[READER].pushed == [-2880, 0, 0]
    assert steps_of(records, READER) == [4, 8, 12, 16, 20, 24, 28, 32]
    with pytest.raises(ValueError, match="unknown keys: doppler"):
        parse_nature_beam_world({**bar(-MOMENTUM[4], 32, probe=True), "doppler": True})


# -- (c) ---------------------------------------------------------------------------

SIDE = 64
PLANE_TABLE = (
    (0, 0, 0),
    (0, 0, 0),
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)


def lamps_for(vector: tuple[int, int, int]) -> list[tuple[int, int]]:
    """The lamps' Nodes so that every Node of the plane (but one corner)
    lies on exactly one digital line of the direction."""
    if vector == (0, 1, 0):
        return [(x, 0) for x in range(SIDE)]
    if vector == (1, 1, 0):
        return [(x, 0) for x in range(0, SIDE, 2)] + [(0, y) for y in range(2, SIDE, 2)]
    if vector == (-1, 1, 0):
        return [(x, 0) for x in range(SIDE - 1, -1, -2)] + [(SIDE - 1, y) for y in range(2, SIDE, 2)]
    raise ValueError(vector)


def plane(
    vector: tuple[int, int, int], momentum: int, ticks: int, rule: str = "read"
) -> dict[str, object]:
    """A plane of parallel lines of one direction, one lamp per line,
    pre-filled: the row of age tau at the lamp plus the line's point
    m(tau) (the flight's own rule), and the reader at (40, 40, 0)."""
    flight = direction_flight((*PLANE_TABLE, vector))
    index = len(PLANE_TABLE)
    ages = np.arange(400)
    made = flight.manhattan_steps(np.full(ages.shape[0], index), ages)
    s1 = int(flight.manhattan[index])
    line = flight.lines[index, :s1]
    lamps = lamps_for(vector)
    measured: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []
    for number, (lx, ly) in enumerate(lamps, start=1):
        measured.append(
            {
                "position": [lx, ly, 0],
                "family": "beam",
                "amount": 1,
                "fixed": True,
                "directions": [list(vector)],
                "table": {"beam": "pass"},
            }
        )
        for age, count in enumerate(made.tolist()):
            whole, part = divmod(count, s1)
            point = whole * flight.vectors[index] + line[:part].sum(axis=0)
            x, y = lx + int(point[0]), ly + int(point[1])
            if 0 <= x < SIDE and 0 <= y < SIDE:
                rows.append(
                    {
                        "position": [x, y, 0],
                        "family": "beam",
                        "number": number,
                        "direction": list(vector),
                        "amount": 1,
                        "phase": 0,
                        "age": age,
                    }
                )
    measured.append(
        {
            "position": [40, 40, 0],
            "family": "body",
            "amount": M,
            "momentum": [momentum, 0, 0],
            "table": {"beam": rule},
        }
    )
    return {
        "law": "beam",
        "model_id": "crossing-plane-test",
        "shape": [SIDE, SIDE, 1],
        "boundary": {"z": "periodic"},
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "width": 1,
        "age_bound": 4096,
        "directions": [list(vector)] if vector != (0, 1, 0) else [],
        "families": [
            {"name": "beam", "quantum": 0, "charge": 1, "phase": False},
            {"name": "body", "quantum": 0, "charge": 1, "phase": False},
        ],
        "measured": measured,
        "in_transit": rows,
    }


PLANES = {
    "transverse +y": ((0, 1, 0), 32, [1] * 32),
    "diagonal (1, 1, 0) with the step": ((1, 1, 0), 24, [1, 1, 1, 0, 0, 1, 1, 1] * 4),
    "diagonal (-1, 1, 0) against the step": ((-1, 1, 0), 36, [1, 1, 1, 2, 1, 1, 1, 1] * 4),
}


@pytest.mark.parametrize("case", sorted(PLANES))
def test_the_streams_beyond_the_axis(case):
    """(c)."""
    vector, expected, pattern = PLANES[case]
    world = plane(vector, MOMENTUM[4], 32)
    reader = len(lamps_for(vector)) + 1
    simulation, records = run(world)
    counts = per_tick(records, reader, 32)
    assert counts == pattern and sum(counts) == expected, case
    assert steps_of(records, reader) == [4, 8, 12, 16, 20, 24, 28, 32]
    assert simulation.measured[reader].position == (48, 40, 0)
    clicked, records_m = run(plane(vector, MOMENTUM[4], 32, rule="measure"))
    assert per_tick(records_m, reader, 32, "click") == pattern, case


# -- (d) ---------------------------------------------------------------------------


def one_row(x_0: int, start: int, sense: int, ticks: int) -> dict[str, object]:
    row = {
        "position": [x_0, 0, 0],
        "family": "beam",
        "number": LAMP,
        "direction": PLUS_X,
        "amount": 1,
        "phase": 0,
        "age": 0,
    }
    return bar(sense * MOMENTUM[4], ticks, start=start, rows=[row], release=[0, 1])


def test_one_row_is_met_once():
    """(d)."""
    assert [m_heading(t) for t in range(14)] == [0, 1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8]
    # Toward: C3 with both arrived at 37 at tick 12.
    simulation, records = run(one_row(30, 40, -1, 14))
    assert [(r["tick"], r["amount"], r["node"]) for r in met(records, READER)] == [(12, 1, [37, 0, 0])]
    assert steps_of(records, READER) == [4, 8, 12]
    # Away, the leapfrog after a rest (C3''): met at tick 3 only.
    simulation, records = run(one_row(30, 32, 1, 10))
    assert [(r["tick"], r["amount"], r["node"]) for r in met(records, READER)] == [(3, 1, [32, 0, 0])]
    assert steps_of(records, READER) == [4, 8]
    # Away, the entered Node's row moving with the step (C2'): tick 1 only.
    simulation, records = run(one_row(31, 32, 1, 10))
    assert [(r["tick"], r["amount"], r["node"]) for r in met(records, READER)] == [(1, 1, [32, 0, 0])]
    assert steps_of(records, READER) == [4, 8]


# -- (e) ---------------------------------------------------------------------------

PERIODS = {
    "toward k = 4": (4, -1, 183),
    "toward k = 8": (8, -1, 311),
    "away k = 4": (4, 1, 74),
    "away k = 8": (8, 1, 202),
}


@pytest.mark.parametrize("case", sorted(PERIODS))
def test_the_sum_over_a_period(case):
    """(e)."""
    k, sense, expected = PERIODS[case]
    ticks = 32 * k
    simulation, records = run(bar(sense * MOMENTUM[k], ticks, length=512, start=400))
    counts = per_tick(records, READER, ticks)
    assert sum(counts) == expected, case
    assert len(steps_of(records, READER)) == 32
    assert simulation.measured[READER].position[0] == 400 + 32 * sense
    if sense < 0:
        assert expected == ticks + 55
    else:
        assert expected == ticks - 55 + 1


# -- (f) ---------------------------------------------------------------------------


def lone(momentum: int, ticks: int) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "crossing-fast-steps-test",
        "shape": [64, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "width": 1,
        "families": [{"name": "body", "quantum": 0, "charge": 0, "phase": False}],
        "measured": [
            {"position": [4, 0, 0], "family": "body", "amount": 1, "momentum": [momentum, 0, 0]}
        ],
    }


@pytest.mark.parametrize(
    ("momentum", "links", "fast"), [(96, 18, 6), (128, 20, 10), (64, 15, 0), (32, 10, 0)]
)
def test_the_fast_steps_are_reported(momentum, links, fast, tmp_path):
    """(f)."""
    simulation, records = run(lone(momentum, 30))
    ticks = steps_of(records, 1)
    assert len(ticks) == links and simulation.measured[1].steps == links
    assert sum(1 for a, b in zip(ticks, ticks[1:], strict=False) if b == a + 1) == fast
    assert simulation.fast_steps == fast
    if momentum == 96:
        assert ticks[:8] == [2, 4, 5, 7, 9, 10, 12, 14]
    path = tmp_path / "world.json"
    path.write_text(json.dumps(lone(momentum, 30)), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert record["fast_steps"] == fast and record["status"] == "completed"
