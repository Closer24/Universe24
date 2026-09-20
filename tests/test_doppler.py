"""The reading's weight at the relative speed, `doppler-v1` (2026-09-20;
docs/BEAM_LAW.md section 3 step 4 and note 38; the model owner's record
119, "a body TAKES a message at the rate at which it and the message meet";
the mathematician's admissible form, docs/designs/push_relative_speed/
FORM.md section 6 on branch `claude/series-m-masses`, record 110). Under
the world key `doppler` a free measured event reads the rows that ARRIVED
at its Node for the push with each row of direction d weighted, on every
axis a where its own momentum p_a is nonzero, by the pair
(N_d D_a - T_d s p_a, N_d D_a): (N_d, T_d) the direction's pace along the
axis from the flight table ((32, 55) on a heading), s the sign of u_{d,a},
D_a = Q S M + |p_a| the step rule's divisor; one floor per (direction,
column) off the reader's clock. The expected integers of
docs/TEST_EXPECTATIONS.md ("The reading's weight at the relative speed"),
written down before the first run:

(a) a fixed body reads byte-identically with and without the key: on the
    bar below with the body held in place (`fixed`), 200 intervals, the
    same records line by line and the same books; a free body at rest
    (p = 0, its push cancelled by the charge column) the same;
(b) the bar of the finding (RULES.md section 2, FORM.md section 4): a fixed
    source at x = 0 releasing one row per interval on +x, the steady beam
    declared in transit (the row of age tau at the Node m(tau)), a free
    body of content 2^20 whose width S and momentum p make its speed
    |p| / D exact, reading the beam with a third column `probe` that
    normalises its push to one unit per row read (gravity and charge
    cancelling exactly, rho 1 on both families): over 200 intervals the
    body reads 200 rows in every case (the finding: the arrivals do not
    Doppler) and the push under the key, the sum of the reads' pushes, is
    at rest 200, receding at 0.30 (S 7, p 3 x 2^26, D 10 x 2^26) 96,
    receding at 0.45 (S 11, p 9 x 2^26, D 20 x 2^26) 45, approaching at
    0.30 (S 7, p -3 x 2^26) 303, co-moving at c = 32 / 55 (S 23, p 2^31,
    D 55 x 2^26) 0, outrunning at 0.75 (S 1, p 3 x 2^26, D 4 x 2^26) 57
    (taken from behind at |c - v|, the absolute value of the pair, the
    push keeping the flow's sign), against FORM.md's map 200, 97, 45,
    303, 0, 58: the two that differ do so by the floor's grain (the
    exact values 96.875 and 57.8, the map's clock ages from 1 and the
    engine's from 0); without the key 200 in every case. The bar as the
    finding posed it, rows of amount 64 on the body of content 2^20, runs
    without the key and is refused at the first weighted push under it,
    the gravity column's product |V E n| x |N D - T s p| = 2^32 x
    155 x 2^26 leaving the register (the mathematician's R1), naming
    the body, the column and the direction;
(c) the third law on two fixed bodies (series C item 2's mirror world of
    `test_columns.py` (b)) unchanged: equal and opposite pushes at every
    tick, the same integers as without the key;
(d) the refusals: the key that is not true or false, naming it; at load
    under the key a free body whose pair cannot fit, content 2^40 at width
    2^10 (D = 2^56, 87 x D beyond 2^62 - 1) and content 1 with the
    momentum 2^56, refused naming the axis, the direction, the pace and
    the largest D admitted; the same worlds parse without the key, and a
    fixed body of that content parses under it (the weight 1);
(e) the pace table and the pair: (32, 55) on every heading, (16, 39) on
    (1, 1, 0) along x and y, (128, 247) and (64, 247) on (2, 1, 0), (0, 1)
    where the direction has no component and on the rest directions; the
    pair 1 at p = 0, 0 at the direction's own speed, negative beyond it;
    on a free reader of content 1 with the momentum (32, 0, 0) (D = 96)
    met by one row on +x and one on (1, 1, 0) in one interval, gravity
    alone: the x push -(27 + 8) (by_clock(0, 64 x 1312, 3072) and
    by_clock(0, 45 x 288, 1536), one floor per direction), the y push -45
    (the reader at rest on y: the group's product as today); the record
    (`run.json` carrying `doppler` and the identity under `hypotheses`);
    every world of the gate set parsing without the key; `column_term`
    refusing the denominator D_c d_c x N D by division before it is formed
    and giving 0 at a weight of numerator 0;
(f) the implementer's rule on a fan with a column denominator above 1
    (the reader `a` of charge [1, 3] met by a `b` row of charge 1 on +x
    and one on (1, 1, 0)): a free reader at rest reads (-73, -30, 0)
    (gravity -(109, 45), charge by_clock(0, 109, 3) = 36 and by_clock(0,
    45, 3) = 15) byte-identically with and without the key, the same
    records, and `push_form` with the terms at rest equals `push_form`
    without them on that nonzero push; the same reader with the momentum
    (1, 0, 0) (D = 65, the pairs (2025, 2080) on the heading and (1001,
    1040) on the diagonal) reads x per direction, gravity -(62 + 43) and
    charge 20 + 14, the push (-71, -30, 0), y at rest as before;
(g) a body on a set (`span` [1, 1, 3], content 1, the momentum (32, 0,
    0), D = 96) met in one interval by one +x row at two of its Nodes
    from two numbers: two groups, each weighted from the one frame
    snapshot p = 32, each pushing -27 (by_clock(0, 64 x 1312, 3072); the
    live momentum after the first group, 5, would give 56), the momentum
    after the interval -22; without the key -64 each.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import (
    DopplerTerms,
    column_term,
    flight_table,
    push_form,
    relative_speed_pair,
)
from event_universe.events.world import (
    COLUMNS_RULE,
    DOPPLER_RULE,
    LABEL_SCALE,
    MOMENTUM_BOUND,
    axis_pace,
    step_divisor,
)
from event_universe.runner import run_initialization
from event_universe.world_loading import load_world

Q = LABEL_SCALE
T_HEADING = 110
PLUS_X = [1, 0, 0]
DIAGONAL = [1, 1, 0]
ROOT = Path(__file__).resolve().parents[1]


def m_heading(tau: int) -> int:
    """Links made by age tau on a heading, (2 tau Q + T) // (2 T)."""
    return (2 * tau * Q + T_HEADING) // (2 * T_HEADING)


def bar(
    momentum: int,
    width: int,
    start: int,
    *,
    doppler: bool,
    amount: int = 1,
    fixed: bool = False,
    probe: bool = True,
    ticks: int = 200,
    length: int = 400,
) -> dict[str, object]:
    """The bar of the finding: the steady beam of the fixed source at x = 0
    (one row per interval on +x, the row of age tau at the Node m(tau)), the
    body of content 2^20 at `start`. With `probe` the third column makes
    the push one unit per row read: |V E n| / (D_c d_c) = (64 x amount) x
    (2^20 / 2^16) / (1024 x amount) = 1."""
    rows = []
    tau = 0
    while m_heading(tau) < length:
        rows.append(
            {
                "position": [m_heading(tau), 0, 0],
                "family": "beam",
                "number": 1,
                "direction": PLUS_X,
                "amount": amount,
                "phase": 0,
                "age": tau,
            }
        )
        tau += 1
    beam: dict[str, object] = {"name": "beam", "quantum": 0, "charge": 1, "phase": False}
    body: dict[str, object] = {"name": "body", "quantum": 0, "charge": 1, "phase": False}
    if probe:
        beam["columns"] = {"probe": {"value": [1, 1024 * amount], "sign": 1}}
        body["columns"] = {"probe": {"value": [1, 1 << 16], "sign": 1}}
    return {
        "law": "beam",
        "model_id": "doppler-bar-test",
        "shape": [length, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "width": width,
        "doppler": doppler,
        "families": [beam, body],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "beam",
                "amount": amount,
                "fixed": True,
                "directions": [PLUS_X],
            },
            {
                "position": [start, 0, 0],
                "family": "body",
                "amount": 1 << 20,
                "momentum": [momentum, 0, 0],
                "fixed": fixed,
                "table": {"beam": "read"},
            },
        ],
        "in_transit": rows,
    }


def run(world: dict[str, object]) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), records.append)
    for _ in range(int(str(world["ticks"]))):
        simulation.step()
    assert simulation.books()["balanced"]
    return simulation, records


def reads_of(records: list[dict[str, object]], number: int) -> list[dict[str, object]]:
    return [r for r in records if r["event"] == "read" and r["measured"] == number]


# -- (a) ---------------------------------------------------------------------------


def test_a_fixed_body_and_a_free_body_at_rest_read_byte_identically():
    """(a)."""
    for keys in ({"fixed": True}, {"probe": False}):
        without = run(bar(0, 1, 40, doppler=False, **keys))  # type: ignore[arg-type]
        under = run(bar(0, 1, 40, doppler=True, **keys))  # type: ignore[arg-type]
        assert under[1] == without[1] and len(reads_of(under[1], 2)) == 200
        assert under[0].books() == without[0].books()
        assert under[0].measured[2].momentum == without[0].measured[2].momentum
        assert under[0].measured[2].pushed == without[0].measured[2].pushed
    # The fixed body's momentum books the push it takes (its record), a
    # free body at rest under the cancelled push keeps 0: neither moves.
    assert run(bar(0, 1, 40, doppler=True, fixed=True))[0].measured[2].pushed == [200, 0, 0]
    assert run(bar(0, 1, 40, doppler=True, probe=False))[0].measured[2].pushed == [0, 0, 0]


# -- (b) ---------------------------------------------------------------------------

BAR = {
    "at rest": (0, 1, 40, 200),
    "receding at 0.30": (3 << 26, 7, 40, 96),
    "receding at 0.45": (9 << 26, 11, 40, 45),
    "approaching at 0.30": (-(3 << 26), 7, 200, 303),
    "co-moving at c": (1 << 31, 23, 40, 0),
    "outrunning at 0.75": (3 << 26, 1, 40, 57),
}


@pytest.mark.parametrize("case", sorted(BAR))
def test_the_bar_of_the_finding(case):
    """(b)."""
    momentum, width, start, expected = BAR[case]
    divisor = step_divisor(momentum, 1 << 20, width)
    assert divisor == Q * width * (1 << 20) + abs(momentum)
    # The pair on the heading: 1 at rest, 0 co-moving, |c - v| / c outrunning.
    numerator, denominator = relative_speed_pair((32, 55), 1, momentum, divisor, _entry(), 2)
    assert denominator == 32 * divisor and numerator == abs(32 * divisor - 55 * momentum)
    simulation, records = run(bar(momentum, width, start, doppler=True))
    reads = reads_of(records, 2)
    assert len(reads) == 200 and sum(int(str(r["amount"])) for r in reads) == 200, case
    assert sum(int(r["push"][0]) for r in reads) == expected, case  # type: ignore[index]
    assert simulation.measured[2].pushed[0] == expected
    if momentum:
        assert simulation.measured[2].position[0] != start
    # Without the key the same bar reads 200 whatever the motion (the finding).
    plain, records = run(bar(momentum, width, start, doppler=False))
    assert sum(int(r["push"][0]) for r in reads_of(records, 2)) == 200  # type: ignore[index]
    assert len(reads_of(records, 2)) == 200


def test_the_bar_as_posed_with_rows_of_64_is_refused_at_the_first_weighted_push():
    """(b), the register: rows of amount 64 on the body of content 2^20."""
    simulation, records = run(bar(3 << 26, 7, 40, doppler=False, amount=64))
    assert len(reads_of(records, 2)) == 200
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar(3 << 26, 7, 40, doppler=True, amount=64))
    )
    with pytest.raises(OverflowError) as refusal:
        for _ in range(200):
            simulation.step()
    text = str(refusal.value)
    assert "measured event 2 at [40, 0, 0]" in text and "column 'gravity'" in text
    assert "against the direction 2 under doppler" in text
    assert "|V E n| x |N D - T s p| = 4294967296 x 10401873920" in text  # 2^32 x 155 x 2^26


# -- (c) ---------------------------------------------------------------------------


def mirror(doppler: bool) -> dict[str, object]:
    column = {"strong": {"value": [2, 3], "sign": -1}}
    return {
        "law": "beam",
        "model_id": "doppler-mirror-test",
        "shape": [4, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": 12,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "doppler": doppler,
        "families": [
            {"name": "p", "quantum": 0, "phase": False, "charge": [1, 3], "columns": column},
            {"name": "q", "quantum": 0, "phase": False, "charge": [1, 3], "columns": column},
        ],
        "measured": [
            {"position": [0, 0, 0], "family": "p", "amount": 3, "fixed": True, "directions": [PLUS_X]},
            {
                "position": [3, 0, 0],
                "family": "q",
                "amount": 5,
                "fixed": True,
                "directions": [[-1, 0, 0]],
            },
        ],
    }


def test_the_third_law_on_two_fixed_bodies_is_unchanged():
    """(c)."""
    simulation, records = run(mirror(True))
    plain, plain_records = run(mirror(False))
    assert records == plain_records
    on_p = {r["tick"]: r["push"] for r in reads_of(records, 1)}
    on_q = {r["tick"]: r["push"] for r in reads_of(records, 2)}
    assert sorted(on_p) == sorted(on_q) == list(range(6, 13))
    for tick in on_p:
        push = on_p[tick]
        assert push == [-v for v in on_q[tick]] and push[0] > 0  # type: ignore[union-attr]
        assert push[0] == 960 - by_clock(tick - 1, 320, 3) + by_clock(tick - 1, 1280, 3)  # type: ignore[index]
    assert simulation.measured[1].pushed == [-v for v in simulation.measured[2].pushed]
    assert simulation.measured[1].pushed == plain.measured[1].pushed
    assert simulation.world.hypotheses == [COLUMNS_RULE, DOPPLER_RULE]


# -- (d) ---------------------------------------------------------------------------


def refused(document: dict[str, object], text: str) -> None:
    with pytest.raises(ValueError, match=text):
        parse_nature_beam_world(document)


def test_the_refusals_at_load():
    """(d)."""
    base = bar(0, 1, 4, doppler=False, length=8)
    for value in (1, "true", None, [True]):
        refused({**base, "doppler": value}, "doppler must be true or false")
    heavy = copy.deepcopy(base)
    heavy["width"] = 1 << 10
    heavy["measured"][1]["amount"] = 1 << 40  # type: ignore[index]
    parse_nature_beam_world(heavy)
    reach = MOMENTUM_BOUND // 87
    refused(
        {**heavy, "doppler": True},
        rf"doppler is refused: measured\[1\] on the axis x against the direction \[1, 0, 0\] of "
        rf"pace \[32, 55\] needs the relative-speed pair \(N \+ T\) x D = 87 x {1 << 56} beyond "
        rf"the integer bound {MOMENTUM_BOUND}: D = 64 x 1024 x {1 << 40} \+ 0 .* at most {reach}",
    )
    held = copy.deepcopy(heavy)
    held["doppler"] = True
    held["measured"][1]["fixed"] = True  # type: ignore[index]
    assert parse_nature_beam_world(held).doppler is True
    fast = copy.deepcopy(base)
    fast["measured"][1]["amount"] = 1  # type: ignore[index]
    fast["measured"][1]["momentum"] = [0, 0, -(1 << 56)]  # type: ignore[index]
    parse_nature_beam_world(fast)
    refused(
        {**fast, "doppler": True},
        rf"measured\[1\] on the axis z against the direction \[0, 0, 1\] .* 87 x {64 + (1 << 56)} .* "
        rf"D = 64 x 1 x 1 \+ {1 << 56}",
    )


# -- (e) ---------------------------------------------------------------------------


class _entry:
    number = 2
    position = (40, 0, 0)


def test_the_pace_table_the_pair_the_fan_and_the_record(tmp_path: Path):
    """(e)."""
    for heading in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
        pace = axis_pace(heading)
        assert pace[[abs(c) for c in heading].index(1)] == (32, 55)
        assert [p for p in pace if p != (32, 55)] == [(0, 1), (0, 1)]
    assert axis_pace((0, 0, 0)) == ((0, 1), (0, 1), (0, 1))
    assert axis_pace((1, 1, 0)) == ((16, 39), (16, 39), (0, 1))
    assert axis_pace((2, 1, 0)) == ((128, 247), (64, 247), (0, 1))
    table = flight_table(((0, 0, 0), (0, 0, 0), (1, 0, 0), (-1, 0, 0), (2, 1, 0)))
    assert table.pace.shape == (5, 3, 2)
    assert table.pace[2].tolist() == [[32, 55], [0, 1], [0, 1]]
    assert table.pace[4].tolist() == [[128, 247], [64, 247], [0, 1]]
    # The pair: 1 at rest, 0 at the direction's own speed, negative beyond.
    assert relative_speed_pair((32, 55), 1, 0, 96, _entry(), 2) == (3072, 3072)
    assert relative_speed_pair((32, 55), 1, 32, 55, _entry(), 2) == (0, 32 * 55)
    assert relative_speed_pair((32, 55), 1, 40, 55, _entry(), 2) == (55 * 40 - 32 * 55, 32 * 55)
    assert relative_speed_pair((32, 55), -1, 40, 55, _entry(), 2) == (32 * 55 + 55 * 40, 32 * 55)
    with pytest.raises(OverflowError, match=r"\(N \+ T\) x D = 87 x"):
        relative_speed_pair((32, 55), 1, 0, MOMENTUM_BOUND // 87 + 1, _entry(), 2)
    # The column term under a weight: the denominator tested by division
    # before it is formed, the product with the numerator likewise, a
    # numerator of 0 forming nothing.
    assert column_term(64, 1, 1, 1, 0, "gravity", _entry(), (1312, 3072), 2) == 27
    assert column_term(-64, 1, 1, 1, 0, "gravity", _entry(), (1312, 3072), 2) == -27
    assert column_term(64, 1, 1, 3, 0, "charge", _entry(), (0, 3072), 2) == 0
    with pytest.raises(OverflowError, match=r"the denominator D_c d_c x N D = 1073741824 x"):
        column_term(1, 1, 1, 1 << 30, 0, "charge", _entry(), (1, 1 << 40), 2)
    with pytest.raises(OverflowError, match=r"\|V E n\| x \|N D - T s p\| = 4294967296 x"):
        column_term(1 << 32, 1, 1, 1, 0, "gravity", _entry(), (1 << 31, 1 << 31), 2)
    # The fan: one row on +x and one on (1, 1, 0) at the free reader of
    # content 1 with the momentum (32, 0, 0), D = 96, gravity alone.
    fan = {
        "law": "beam",
        "model_id": "doppler-fan-test",
        "shape": [5, 5, 1],
        "boundary": {"z": "periodic"},
        "ticks": 1,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "doppler": True,
        "directions": [DIAGONAL],
        "families": [
            {"name": "a", "quantum": 0, "phase": False},
            {"name": "b", "quantum": 0, "phase": False},
        ],
        "measured": [
            {"position": [2, 2, 0], "family": "a", "amount": 1, "momentum": [32, 0, 0]},
            {"position": [0, 4, 0], "family": "b", "amount": 1, "fixed": True},
        ],
        "in_transit": [
            {
                "position": [1, 2, 0],
                "family": "b",
                "number": 2,
                "direction": PLUS_X,
                "amount": 1,
                "phase": 0,
                "age": 0,
            },
            {
                "position": [2, 1, 0],
                "family": "b",
                "number": 2,
                "direction": DIAGONAL,
                "amount": 1,
                "phase": 0,
                "age": 1,
            },
        ],
    }
    simulation, records = run(fan)
    reads = reads_of(records, 1)
    assert len(reads) == 1 and reads[0]["amount"] == 2
    x_heading = by_clock(0, 64 * (32 * 96 - 55 * 32), 32 * 96)
    x_diagonal = by_clock(0, 45 * (16 * 96 - 39 * 32), 16 * 96)
    assert (x_heading, x_diagonal) == (27, 8)
    assert reads[0]["push"] == [-(27 + 8), -45, 0]
    plain, records = run({**fan, "doppler": False})
    assert reads_of(records, 1)[0]["push"] == [-(64 + 45), -45, 0]
    held, records = run({**fan, "measured": [{**fan["measured"][0], "fixed": True}, fan["measured"][1]]})  # type: ignore[index, list-item]
    assert reads_of(records, 1)[0]["push"] == [-(64 + 45), -45, 0]
    # The record.
    path = tmp_path / "world.json"
    path.write_text(json.dumps(fan), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert record["doppler"] is True and record["hypotheses"] == [DOPPLER_RULE]
    assert record["status"] == "completed"
    # The gate set declares the key nowhere: every shipped world reads as it did.
    listing = json.loads((ROOT / "examples/events/gate_set.json").read_text(encoding="utf-8"))
    assert len(listing["worlds"]) == 15
    for item in listing["worlds"]:
        path = ROOT / "examples/events" / item["path"]
        world = load_world(path.read_bytes(), base_dir=path.parent).world
        assert world.doppler is False and DOPPLER_RULE not in world.hypotheses, item["path"]


# -- (f) ---------------------------------------------------------------------------


def charged_fan(momentum: list[int], doppler: bool) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "doppler-charged-fan-test",
        "shape": [5, 5, 1],
        "boundary": {"z": "periodic"},
        "ticks": 1,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "doppler": doppler,
        "directions": [DIAGONAL],
        "families": [
            {"name": "a", "quantum": 0, "phase": False, "charge": [1, 3]},
            {"name": "b", "quantum": 0, "phase": False, "charge": 1},
        ],
        "measured": [
            {"position": [2, 2, 0], "family": "a", "amount": 1, "momentum": momentum},
            {"position": [0, 4, 0], "family": "b", "amount": 1, "fixed": True},
        ],
        "in_transit": [
            {
                "position": [1, 2, 0],
                "family": "b",
                "number": 2,
                "direction": PLUS_X,
                "amount": 1,
                "phase": 0,
                "age": 0,
            },
            {
                "position": [2, 1, 0],
                "family": "b",
                "number": 2,
                "direction": DIAGONAL,
                "amount": 1,
                "phase": 0,
                "age": 1,
            },
        ],
    }


def test_the_rule_on_a_fan_with_a_column_denominator_above_one():
    """(f)."""
    at_rest = (-(109 - by_clock(0, 109, 3)), -(45 - by_clock(0, 45, 3)), 0)
    assert at_rest == (-73, -30, 0)
    under, records = run(charged_fan([0, 0, 0], True))
    plain, plain_records = run(charged_fan([0, 0, 0], False))
    assert records == plain_records and reads_of(records, 1)[0]["push"] == list(at_rest)
    assert under.measured[1].momentum == plain.measured[1].momentum == list(at_rest)
    columns = (("gravity", -1), ("charge", 1))
    charges = [(1, 1), (1, 3)]
    values = ((1, 1), (1, 1))
    terms = DopplerTerms(
        (False, False, False),
        ((2, (64, 0, 0), ((1, 1), (1, 1), (1, 1))), (8, (45, 45, 0), ((1, 1), (1, 1), (1, 1)))),
    )
    assert push_form(True, [109, 45, 0], charges, values, columns, 0, _entry(), terms) == list(at_rest)  # type: ignore[arg-type]
    assert push_form(True, [109, 45, 0], charges, values, columns, 0, _entry(), None) == list(at_rest)  # type: ignore[arg-type]
    # Moving on x at p = 1: D = 65, one floor per (direction, column) on x.
    heading, diagonal = (abs(32 * 65 - 55), 32 * 65), (abs(16 * 65 - 39), 16 * 65)
    assert (heading, diagonal) == ((2025, 2080), (1001, 1040))
    gravity = by_clock(0, 64 * 2025, 2080) + by_clock(0, 45 * 1001, 1040)
    charge = by_clock(0, 64 * 2025, 3 * 2080) + by_clock(0, 45 * 1001, 3 * 1040)
    assert (gravity, charge) == (62 + 43, 20 + 14)
    moving, records = run(charged_fan([1, 0, 0], True))
    assert reads_of(records, 1)[0]["push"] == [-gravity + charge, -30, 0] == [-71, -30, 0]
    plain, records = run(charged_fan([1, 0, 0], False))
    assert reads_of(records, 1)[0]["push"] == [-73, -30, 0]


# -- (g) ---------------------------------------------------------------------------


def test_a_body_on_a_set_reads_every_group_from_the_one_frame_snapshot():
    """(g)."""

    def world(doppler: bool) -> dict[str, object]:
        return {
            "law": "beam",
            "model_id": "doppler-set-body-test",
            "shape": [8, 1, 3],
            "boundary": {"y": "periodic", "z": "periodic"},
            "ticks": 1,
            "K": 1 << 20,
            "N": 64,
            "release": [0, 1],
            "suspension": 0,
            "doppler": doppler,
            "families": [
                {"name": "a", "quantum": 0, "phase": False},
                {"name": "b", "quantum": 0, "phase": False},
            ],
            "measured": [
                {
                    "position": [4, 0, 1],
                    "family": "a",
                    "amount": 1,
                    "momentum": [32, 0, 0],
                    "span": [1, 1, 3],
                },
                {"position": [0, 0, 0], "family": "b", "amount": 1, "fixed": True},
                {"position": [0, 0, 2], "family": "b", "amount": 1, "fixed": True},
            ],
            "in_transit": [
                {
                    "position": [3, 0, 0],
                    "family": "b",
                    "number": 2,
                    "direction": PLUS_X,
                    "amount": 1,
                    "phase": 0,
                    "age": 0,
                },
                {
                    "position": [3, 0, 2],
                    "family": "b",
                    "number": 3,
                    "direction": PLUS_X,
                    "amount": 1,
                    "phase": 0,
                    "age": 0,
                },
            ],
        }

    simulation, records = run(world(True))
    reads = reads_of(records, 1)
    assert [(r["number"], r["push"]) for r in reads] == [(2, [-27, 0, 0]), (3, [-27, 0, 0])]
    assert by_clock(0, 64 * abs(32 * 96 - 55 * 32), 32 * 96) == 27
    # The live momentum after the first group, 5, would have weighted the
    # second at (32 x 69 - 55 x 5, 32 x 69): 56, not 27.
    assert by_clock(0, 64 * abs(32 * 69 - 55 * 5), 32 * 69) == 56
    assert simulation.measured[1].momentum == [32 - 54, 0, 0]
    assert simulation.measured[1].nodes == ((4, 0, 0), (4, 0, 1), (4, 0, 2))
    plain, records = run(world(False))
    assert [r["push"] for r in reads_of(records, 1)] == [[-64, 0, 0], [-64, 0, 0]]
