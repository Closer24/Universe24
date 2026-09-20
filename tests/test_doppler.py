"""The reading's weight at the relative speed, `doppler-v1` (2026-09-20;
docs/BEAM_LAW.md section 3 step 4 and note 38; the model owner's record
119, "a body TAKES a message at the rate at which it and the message meet";
the mathematician's admissible form, docs/designs/push_relative_speed/
FORM.md section 6, record 110, and its grain and flux form, GRAIN.md
sections 1 and 2 on branch `claude/series-m-masses`, after the physics-rule
review of e916e115). Under the world key `doppler` a free measured event
reads the rows that ARRIVED at its Node for the push with each direction's
label flow V_d weighted by the flux of its rows through the body, one
scalar per (direction, body), (|G Q |v|^2 - T_d sum_a s_a w_a v_a|,
G Q |v|^2), with w_a = G |p_a| // D_a the body's speed at the grain G =
2^12 (`SPEED_GRAIN`), D_a = Q S M + |p_a| the step rule's divisor, v the
direction's vector and T_d its resolution from the flight table; the
weighted flow V'_d = sign(V_d) x by_clock(age_A, |V_d| x num_d, G Q |v|^2)
per component, summed over the directions, then the columns as today. The
expected integers of docs/TEST_EXPECTATIONS.md ("The reading's weight at
the relative speed"), written down before the first run:

(a) a fixed body reads byte-identically with and without the key: on the
    bar below with the body held in place (`fixed`), 200 intervals, the
    same records line by line and the same books; a free body at rest
    (p = 0, its push cancelled by the charge column) the same;
(b) the bar of the finding (RULES.md section 2, FORM.md section 4): a fixed
    source at x = 0 releasing one row per interval on +x, the steady beam
    declared in transit (the row of age tau at the Node m(tau)), a free
    body of content 2^20 whose width S and momentum p make its speed
    |p| / D exact, reading the beam with a third column `probe` whose
    product is exact (the body's value [1, 2^20], the beam's 1, the divisor
    1: the push IS the weighted flow, in label units, 64 per row): over
    200 intervals the body reads 200 rows in every case (the finding: the
    arrivals do not Doppler) and the push under the key, the sum of the
    reads' pushes, is at rest 12800 (200 rows); receding at 0.30 (S 7, p
    3 x 2^26, D 10 x 2^26; w 1228, the pair 127064 / 262144) 6204 (96.94
    rows); receding at 0.45 (S 11, p 9 x 2^26; w 1843, 59414 / 262144)
    2901 (45.33); approaching at 0.30 (S 7, p -3 x 2^26; 397224 / 262144)
    19395 (303.05); co-moving at c = 32 / 55 (S 23, p 2^31; w 2383,
    14 / 262144, below one label unit per row: 0) 0; outrunning at 0.75
    (S 1, p 3 x 2^26; w 3072, 75776 / 262144, taken from behind at
    |c - v|) 3700 (57.81), against FORM.md's map 200, 97, 45, 303, 0, 58
    and its exact rates 96.9, 45.3, 303.1, 0, 57.8: the flux times the
    arrivals to the label unit (the speed's grain below 1 / G, the flow's
    floor off the clock); without the key 12800 in every case. The bar as
    the finding posed it, rows of amount 64, runs under the key (the pair
    of the first build refused it) and reads receding at 0.30 within a
    row of the amount-1 line (396673 of 4096 per row: 96.84);
(c) the third law on two fixed bodies (series C item 2's mirror world of
    `test_columns.py` (b)) unchanged: equal and opposite pushes at every
    tick, the same integers as without the key;
(d) the refusals: the key that is not true or false, naming it; the
    weighted flow's product |V_d| x num tested by division before it is
    formed (`weighted_flow` on one label of 64 at the outrunning pair
    75776 / 262144 gives 18; on a label of 2^50 it is refused naming the
    body and the direction); the static budget of the
    columns under the key takes the weight's largest factor on the table
    (`weighted_flow_factor`: 3 on the headings, 4 with (1, 1, 1));
(e) the grain and the pair: `quantised_speed` (1365, 1) at p / D = 1 / 3,
    (1183, 1) at 26 / 90 (the G2 star's 0.28889), (0, 0) at rest, the
    sign -1 on a negative momentum; `flux_pair` on a heading (|G Q - T_d
    s w|, G Q): (262144, 262144) at rest, (111994, 262144) at 1 / 3
    (0.4272), (0, 262144) at w = G x 32 / 55 (2383 gives 14, the grain),
    exactly 1 for a transverse motion; on (1, 1, 0) at 1 / 3 (311348,
    524288) = 0.5938 (the flux, GRAIN.md section 2, against the per-axis
    form's 0.1875), on (1, 2, 0) at the star's speed (1018519, 1310720) =
    0.7771, on (1, 3, 2) (3180254, 3670016) = 0.8666; the record
    (`run.json` carrying `doppler` and the identity under `hypotheses`);
    every world of the gate set parsing without the key;
(f) the fan, pinned as integers over three intervals (a free reader of
    content 2^20 at (4, 6, 4) of a 9 x 12 x 9 open GameBoard, the push the
    weighted flow as in (b), one row of amount 64 of the direction
    arriving at each of the ticks 1, 2, 3 from number 2, the reader's
    clock ages 0, 1, 2, its first step after the third reading at 1 / 3
    and after the fourth at 26 / 90): on
    (1, 1, 0) at v = 1 / 3 (p 2^25, D 3 x 2^25) the sum (5130, 5130, 0)
    of (8640, 8640, 0), 0.594 of the rate on both components; on
    (1, 2, 0) at v = 26 / 90 (p 26 x 2^20, D 90 x 2^20) (4326, 8504, 0)
    of (5568, 10944, 0), 0.777; on (1, 3, 2) at the same speed (2828,
    8485, 5656) of (3264, 9792, 6528), 0.866; on the heading +x at 1 / 3
    (5249, 0, 0) of (12288, 0, 0), 0.427; on the transverse +y at 1 / 3
    exactly (0, 12288, 0); the three fan directions arriving together in
    one interval at 1 / 3 the sum of their weighted flows, (5130 + 4135 +
    2761, 5130 + 8128 + 8284, 5522) ((1, 2, 0) at 973565 / 1310720 =
    0.743, (1, 3, 2) at 3104906 / 3670016 = 0.846); the same fan
    reader at rest with rows of amount 1 byte-identical with and without
    the key (the same records over the three intervals, the pushes the
    flows (273, 459, 102), its momentum below D / G = 16384), and with
    rows of 64 identical for two reads and apart at the third, its
    momentum then past D / G on y (w_y = 1, the grain: (5821, 9788,
    2175) against the flow (5824, 9792, 2176));
(g) a body on a set (`span` [1, 1, 3], content 1, the momentum (32, 0,
    0), D = 96, w = 1365) met in one interval by one +x row at two of its
    Nodes from two numbers: two groups, each weighted from the one frame
    snapshot, each pushing -27 (by_clock(0, 64 x 111994, 262144); the
    live momentum after the first group, 5, would give 56), the momentum
    after the interval -22; without the key -64 each;
(h) a registered star world of series G2 (`examples/events/hubble_stars/
    gravity_scalar.json`, the example's own path since series G2's merge
    of doppler-v1 replaced the reviewer's temporary copy: 24 stars of
    content 2^22 + 4096 at width 2^20, rows of amount 64) parses under the
    key with the identity and runs 20 intervals without a refusal, its
    books balanced: the stars fit as registered. Its table is the eight
    headings, where the flux equals the heading pair; the fan's integers
    rest on (f).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import (
    flight_table,
    flux_pair,
    quantised_speed,
    unit_label,
    weighted_flow,
)
from event_universe.events.world import (
    COLUMNS_RULE,
    DOPPLER_RULE,
    LABEL_SCALE,
    SPEED_GRAIN,
    step_divisor,
    weighted_flow_factor,
)
from event_universe.runner import run_initialization
from event_universe.world_loading import load_world

Q = LABEL_SCALE
G = SPEED_GRAIN
T_HEADING = 110
PLUS_X = [1, 0, 0]
PLUS_Y = [0, 1, 0]
DIAGONAL = [1, 1, 0]
SLANTED = [1, 2, 0]
OBLIQUE = [1, 3, 2]
ROOT = Path(__file__).resolve().parents[1]
CONTENT = 1 << 20


def m_heading(tau: int) -> int:
    """Links made by age tau on a heading, (2 tau Q + T) // (2 T)."""
    return (2 * tau * Q + T_HEADING) // (2 * T_HEADING)


def families(probe: bool) -> list[dict[str, object]]:
    """The beam and the body, rho 1 on both (gravity and charge cancel);
    with `probe` a third column whose product on the body of content 2^20
    is exact: the push is the weighted flow itself."""
    beam: dict[str, object] = {"name": "beam", "quantum": 0, "charge": 1, "phase": False}
    body: dict[str, object] = {"name": "body", "quantum": 0, "charge": 1, "phase": False}
    if probe:
        beam["columns"] = {"probe": {"value": 1, "sign": 1}}
        body["columns"] = {"probe": {"value": [1, CONTENT], "sign": 1}}
    return [beam, body]


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
    body of content 2^20 at `start`."""
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
        "families": families(probe),
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
                "amount": CONTENT,
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


def push_sum(records: list[dict[str, object]], number: int) -> list[int]:
    reads = reads_of(records, number)
    return [sum(int(r["push"][axis]) for r in reads) for axis in range(3)]  # type: ignore[index]


class _entry:
    number = 2
    position = (40, 0, 0)
    frame_momentum = [0, 0, 0]
    frame_content = 1


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
    assert run(bar(0, 1, 40, doppler=True, fixed=True))[0].measured[2].pushed == [12800, 0, 0]
    assert run(bar(0, 1, 40, doppler=True, probe=False))[0].measured[2].pushed == [0, 0, 0]


# -- (b) ---------------------------------------------------------------------------

BAR = {
    "at rest": (0, 1, 40, 0, 12800),
    "receding at 0.30": (3 << 26, 7, 40, 1228, 6204),
    "receding at 0.45": (9 << 26, 11, 40, 1843, 2901),
    "approaching at 0.30": (-(3 << 26), 7, 200, 1228, 19395),
    "co-moving at c": (1 << 31, 23, 40, 2383, 0),
    "outrunning at 0.75": (3 << 26, 1, 40, 3072, 3700),
}


@pytest.mark.parametrize("case", sorted(BAR))
def test_the_bar_of_the_finding(case):
    """(b)."""
    momentum, width, start, w, expected = BAR[case]
    divisor = step_divisor(momentum, CONTENT, width)
    assert divisor == Q * width * CONTENT + abs(momentum)
    speeds = quantised_speed([momentum, 0, 0], CONTENT, width)
    assert speeds[0] == (w, (momentum > 0) - (momentum < 0)) and speeds[1:] == ((0, 0), (0, 0))
    numerator, denominator = flux_pair((1, 0, 0), T_HEADING, speeds)
    assert (numerator, denominator) == (abs(G * Q - T_HEADING * speeds[0][1] * w), G * Q)
    simulation, records = run(bar(momentum, width, start, doppler=True))
    reads = reads_of(records, 2)
    assert len(reads) == 200 and sum(int(str(r["amount"])) for r in reads) == 200, case
    assert push_sum(records, 2) == [expected, 0, 0], case
    assert simulation.measured[2].pushed == [expected, 0, 0]
    if momentum:
        assert simulation.measured[2].position[0] != start
    plain, records = run(bar(momentum, width, start, doppler=False))
    assert push_sum(records, 2) == [12800, 0, 0] and len(reads_of(records, 2)) == 200


def test_the_bar_as_posed_with_rows_of_64_runs_under_the_key():
    """(b), the register: rows of amount 64 on the body of content 2^20."""
    simulation, records = run(bar(3 << 26, 7, 40, doppler=True, amount=64))
    assert len(reads_of(records, 2)) == 200
    assert push_sum(records, 2) == [396673, 0, 0]
    assert abs(396673 / 4096 - 6204 / 64) < 1


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


def test_the_refusals_and_the_budget():
    """(d)."""
    base = bar(0, 1, 4, doppler=False, length=8)
    for value in (1, "true", None, [True]):
        with pytest.raises(ValueError, match="doppler must be true or false"):
            parse_nature_beam_world({**base, "doppler": value})
    table = flight_table(((0, 0, 0), (0, 0, 0), (1, 0, 0)))
    entry = _entry()
    entry.frame_momentum = [3 << 26, 0, 0]
    entry.frame_content = CONTENT
    assert weighted_flow(table, [2], [[64, 0, 0]], entry, 1, 0) == [18, 0, 0]  # type: ignore[arg-type]
    with pytest.raises(
        OverflowError, match=r"weighted flow of measured event 2 .* direction 2 under doppler"
    ):
        weighted_flow(table, [2], [[1 << 50, 0, 0]], entry, 1, 0)  # type: ignore[arg-type]
    # The speed's register intermediate G x |p_a| is tested before it is
    # formed: a momentum of 2^50 + 1 on the y axis (above bound / G) is
    # refused naming the body, its Node and the axis; 2^50 - 1 is not.
    entry.frame_momentum = [0, (1 << 50) + 1, 0]
    with pytest.raises(OverflowError, match=r"speed of measured event 2 .* on axis 1 under doppler"):
        weighted_flow(table, [2], [[64, 0, 0]], entry, 1, 0)  # type: ignore[arg-type]
    entry.frame_momentum = [0, (1 << 50) - 1, 0]
    weighted_flow(table, [2], [[64, 0, 0]], entry, 1, 0)  # type: ignore[arg-type]
    headings = (
        (0, 0, 0),
        (0, 0, 0),
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    )
    assert weighted_flow_factor(headings) == 3 and weighted_flow_factor(((0, 0, 0),)) == 1
    assert weighted_flow_factor((*headings, (1, 1, 1))) == 4
    # The static budget under the key takes the factor: a reader whose
    # budget fits without the key at 2^61 is refused with it at 3 x 2^61.
    tight = {
        **bar(0, 1, 4, doppler=False, length=8, probe=False),
        "families": [
            {"name": "beam", "quantum": 0, "charge": 0, "phase": False},
            {"name": "body", "quantum": 0, "charge": 0, "phase": False},
        ],
    }
    tight["measured"][0]["amount"] = 1 << 25  # type: ignore[index]
    tight["measured"][1]["amount"] = 1 << 30  # type: ignore[index]
    tight["measured"][1]["directions"] = [[-1, 0, 0]]  # type: ignore[index]
    tight["in_transit"] = []
    parse_nature_beam_world(tight)
    with pytest.raises(
        ValueError, match=r"x 3 the largest label flow .* times the largest weight of doppler"
    ):
        parse_nature_beam_world({**tight, "doppler": True})


# -- (e) ---------------------------------------------------------------------------


def test_the_grain_the_pair_and_the_record(tmp_path: Path):
    """(e)."""
    third = quantised_speed([1 << 25, 0, 0], CONTENT, 1)
    star = quantised_speed([26 << 20, 0, 0], CONTENT, 1)
    assert third == ((1365, 1), (0, 0), (0, 0)) and star == ((1183, 1), (0, 0), (0, 0))
    assert quantised_speed([0, -(1 << 25), 0], CONTENT, 1) == ((0, 0), (1365, -1), (0, 0))
    assert quantised_speed([32, 0, 0], 1, 1) == ((1365, 1), (0, 0), (0, 0))
    rest = ((0, 0), (0, 0), (0, 0))
    assert flux_pair((1, 0, 0), T_HEADING, rest) == (262144, 262144)
    assert flux_pair((1, 0, 0), T_HEADING, third) == (111994, 262144)
    assert flux_pair((-1, 0, 0), T_HEADING, third) == (262144 + 110 * 1365, 262144)
    assert flux_pair((0, 1, 0), T_HEADING, third) == (262144, 262144)
    co_moving = quantised_speed([1 << 31, 0, 0], CONTENT, 23)
    assert co_moving[0] == (2383, 1) and flux_pair((1, 0, 0), T_HEADING, co_moving) == (14, 262144)
    assert flux_pair((1, 1, 0), 156, third) == (311348, 524288)
    assert flux_pair((1, 2, 0), 247, star) == (1018519, 1310720)
    assert flux_pair((1, 3, 2), 414, star) == (3180254, 3670016)
    assert abs(311348 / 524288 - 0.5938) < 1e-4 and abs(1018519 / 1310720 - 0.7770) < 1e-4
    assert abs(3180254 / 3670016 - 0.8665) < 1e-4
    table = flight_table(((0, 0, 0), (0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 2)))
    assert table.resolution.tolist() == [1, 1, 110, 156, 247, 414]
    # The record.
    world = bar(1 << 25, 1, 4, doppler=True, length=8, ticks=1)
    path = tmp_path / "world.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert record["doppler"] is True and record["hypotheses"] == [COLUMNS_RULE, DOPPLER_RULE]
    assert record["status"] == "completed"
    # The gate set declares the key nowhere: every shipped world reads as it did.
    listing = json.loads((ROOT / "examples/events/gate_set.json").read_text(encoding="utf-8"))
    assert len(listing["worlds"]) == 15
    for item in listing["worlds"]:
        path = ROOT / "examples/events" / item["path"]
        parsed = load_world(path.read_bytes(), base_dir=path.parent).world
        assert parsed.doppler is False and DOPPLER_RULE not in parsed.hypotheses, item["path"]


# -- (f) ---------------------------------------------------------------------------

READER = (4, 6, 4)
FAN_TABLE = flight_table(
    (
        (0, 0, 0),
        (0, 0, 0),
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
        (1, 1, 0),
        (1, 2, 0),
        (1, 3, 2),
    )
)
FAN_INDEX = {
    tuple(PLUS_X): 2,
    tuple(PLUS_Y): 4,
    tuple(DIAGONAL): 8,
    tuple(SLANTED): 9,
    tuple(OBLIQUE): 10,
}


def placed(direction: list[int], tick: int, amount: int = 64) -> dict[str, object]:
    """A row of the direction placed on its line so that it
    steps into the reader's Node at `tick`: the position is the reader
    less the steps of the flight table from an age whose step at tick - 1
    is a move."""
    index = FAN_INDEX[tuple(direction)]
    period = int(FAN_TABLE.period[index])
    for age in range(period):
        steps = [FAN_TABLE.steps[index][(age + k) % period].tolist() for k in range(tick)]
        if any(steps[-1]):
            position = [READER[a] - sum(int(s[a]) for s in steps) for a in range(3)]
            return {
                "position": position,
                "family": "beam",
                "number": 2,
                "direction": direction,
                "amount": amount,
                "phase": 0,
                "age": age,
            }
    raise AssertionError(direction)


def fan(
    momentum: int, directions: list[list[int]], doppler: bool, amount: int = 64
) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "doppler-fan-test",
        "shape": [9, 12, 9],
        "boundary": "open",
        "ticks": 3,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "doppler": doppler,
        "directions": [DIAGONAL, SLANTED, OBLIQUE],
        "families": families(True),
        "measured": [
            {
                "position": list(READER),
                "family": "body",
                "amount": CONTENT,
                "momentum": [momentum, 0, 0],
                "table": {"beam": "read"},
            },
            {"position": [0, 0, 0], "family": "beam", "amount": 1, "fixed": True},
        ],
        "in_transit": [
            placed(direction, tick, amount) for direction in directions for tick in (1, 2, 3)
        ],
    }


THIRD = 1 << 25
STAR = 26 << 20
FAN = {
    "diagonal at 1/3": (THIRD, DIAGONAL, [5130, 5130, 0], [8640, 8640, 0]),
    "slanted at the star's speed": (STAR, SLANTED, [4326, 8504, 0], [5568, 10944, 0]),
    "oblique at the star's speed": (STAR, OBLIQUE, [2828, 8485, 5656], [3264, 9792, 6528]),
    "heading at 1/3": (THIRD, PLUS_X, [5249, 0, 0], [12288, 0, 0]),
    "transverse at 1/3": (THIRD, PLUS_Y, [0, 12288, 0], [0, 12288, 0]),
}


@pytest.mark.parametrize("case", sorted(FAN))
def test_the_fan_over_three_intervals(case):
    """(f)."""
    momentum, direction, expected, flow = FAN[case]
    assert [64 * c for c in unit_label(tuple(direction))] == [f // 3 for f in flow]  # type: ignore[arg-type]
    simulation, records = run(fan(momentum, [direction], True))
    reads = reads_of(records, 1)
    assert [r["tick"] for r in reads] == [1, 2, 3] and all(r["amount"] == 64 for r in reads)
    assert push_sum(records, 1) == expected, case
    # The first step after the third reading: at 1 / 3 the drive fires at
    # the third self-creation, at 26 / 90 at the fourth.
    assert simulation.measured[1].position == (READER[0] + (momentum == THIRD), READER[1], READER[2])
    plain, records = run(fan(momentum, [direction], False))
    assert push_sum(records, 1) == flow


def test_the_fan_directions_together_and_the_fan_reader_at_rest():
    """(f), the three fan directions in one group, and the reader at rest."""
    speeds = quantised_speed([THIRD, 0, 0], CONTENT, 1)
    expected = [0, 0, 0]
    for direction in (DIAGONAL, SLANTED, OBLIQUE):
        index = FAN_INDEX[tuple(direction)]
        numerator, denominator = flux_pair(tuple(direction), int(FAN_TABLE.resolution[index]), speeds)  # type: ignore[arg-type]
        for axis, component in enumerate(unit_label(tuple(direction))):  # type: ignore[arg-type]
            expected[axis] += sum(
                by_clock(age, 64 * component * numerator, denominator) for age in range(3)
            )
    simulation, records = run(fan(THIRD, [DIAGONAL, SLANTED, OBLIQUE], True))
    reads = reads_of(records, 1)
    assert [r["tick"] for r in reads] == [1, 2, 3] and all(r["amount"] == 192 for r in reads)
    assert push_sum(records, 1) == expected == [5130 + 4135 + 2761, 5130 + 8128 + 8284, 5522]
    # The reader at rest, rows of amount 1: the pushes the flows, the unit
    # labels (45, 45, 0) + (29, 57, 0) + (17, 51, 34) per read, its momentum
    # after the three reads below D / G = 16384 (it still reads as at rest).
    under, records = run(fan(0, [DIAGONAL, SLANTED, OBLIQUE], True, amount=1))
    plain, plain_records = run(fan(0, [DIAGONAL, SLANTED, OBLIQUE], False, amount=1))
    assert records == plain_records and push_sum(records, 1) == [3 * 91, 3 * 153, 3 * 34]
    assert under.measured[1].momentum == plain.measured[1].momentum == [273, 459, 102]
    assert G * max(under.measured[1].momentum) < step_divisor(0, CONTENT, 1)
    # With rows of amount 64 the third read differs: the momentum after two
    # reads, (11648, 19584, 4352), passes D / G on y (w_y = 1, the grain).
    under, records = run(fan(0, [DIAGONAL, SLANTED, OBLIQUE], True))
    plain, plain_records = run(fan(0, [DIAGONAL, SLANTED, OBLIQUE], False))
    pushes, plain_pushes = (
        [r["push"] for r in reads_of(records, 1)],
        [r["push"] for r in reads_of(plain_records, 1)],
    )
    assert pushes[:2] == plain_pushes[:2] == [[5824, 9792, 2176]] * 2
    assert pushes[2] == [5821, 9788, 2175] and plain_pushes[2] == [5824, 9792, 2176]
    assert quantised_speed([11648, 19584, 4352], CONTENT, 1) == ((0, 1), (1, 1), (0, 1))


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
    assert by_clock(0, 64 * 111994, 262144) == 27
    # The live momentum after the first group, 5 (w = G x 5 // 69 = 296),
    # would have weighted the second at (262144 - 110 x 296, 262144): 56.
    assert by_clock(0, 64 * (262144 - 110 * (G * 5 // 69)), 262144) == 56
    assert simulation.measured[1].momentum == [32 - 54, 0, 0]
    assert simulation.measured[1].nodes == ((4, 0, 0), (4, 0, 1), (4, 0, 2))
    plain, records = run(world(False))
    assert [r["push"] for r in reads_of(records, 1)] == [[-64, 0, 0], [-64, 0, 0]]


# -- (h) ---------------------------------------------------------------------------


def test_a_registered_star_world_of_series_g2_runs_under_the_key():
    """(h)."""
    path = ROOT / "examples/events/hubble_stars/gravity_scalar.json"
    # The shipped world references the definition `hubble_stars` (record
    # 113); the loader expands it to its inline form.
    document = json.loads(
        load_world(path.read_bytes(), base_dir=path.parent, root=path.parents[1]).expanded_source
    )
    assert document["width"] == 1 << 20 and "doppler" not in document
    world = parse_nature_beam_world({**document, "doppler": True, "ticks": 20})
    assert world.doppler is True and DOPPLER_RULE in world.hypotheses
    stars = [entry for entry in world.measured if not entry.fixed]
    assert len(stars) == 24 and all(sum(entry.held) == (1 << 22) + 4096 for entry in stars)
    simulation = NatureBeamSimulation(world)
    for _ in range(20):
        simulation.step()
    assert simulation.books()["balanced"]
    assert any(entry.pushed != [0, 0, 0] for entry in simulation.measured.values() if not entry.fixed)
