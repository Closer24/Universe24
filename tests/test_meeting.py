"""The meeting under the Beam Law (docs/BEAM_LAW.md, section 3 step 3 and
section 10, note 35; the model owner's decision of 2026-09-20, Highlights
5.4, "DECIDED: the meeting, M-R"; `events/meeting.py`): at every Node of
free space, after the collision table, every paid unit reads the free units
of every number but its own by the one reading set (the vector moment V
with the labels as weights), the column sum kappa of its family against
theirs (gravity: -1), the target t = kappa V, and turns by k steps of the
arc permutation pi_t of the direction table toward t, k read off its phase
register (adv = (|t| + Q // 2) // Q, total = phase + adv, k = total // N,
phase' = total % N); the free units untouched; the books keep a `turned`
line. The expected integers of docs/TEST_EXPECTATIONS.md ("The meeting"),
written down before the first run:

(a) the arc permutation on the 296-entry direction table of series K (the
    two rest vectors, the six headings, the 288 primitive directions with
    |a| + |b| + |c| <= 6 beyond them and the lamp's (24, +-1, 0),
    (12, +-1, 0)): for 1034 fixed targets (the 342 integer vectors in
    [-3, 3]^3 but 0, the 294 unit labels of the moving directions and the
    first 398 nonzero sums of the label pairs (i, (37 i + 11) mod 294) for
    i from 0) pi_t is a permutation, the two rest directions are fixed, the
    cached inverse returns the identity and pi_t^3 = pi_t o pi_t o pi_t;
    (1, 0, 0) under t = (0, -1, 0) goes (24, -1, 0), (12, -1, 0),
    (5, -1, 0), (4, -1, 0), and under t = (0, -64, 0) (one crowd unit's
    flow) the same four; one cache entry per target (the sectors depend on
    |t|: the design's rule as flown offline); on the six headings alone +x
    under t = (0, -1, 0) is fixed (a sector of one) and the on-line pair
    +y, -y swaps;
(b) the register: a unit of phase 60 meeting one crowd unit (|t| = 64) per
    interval reads the phases 61, 62, 63, 0, 1, 2 with k = 1 at the fourth
    alone; meeting two units (|t| = 128, adv 2) it wraps at the second; the
    inverse (adv - phase' + 63) // 64 gives the same k and the phase before
    for every case; |t| = 31 advances by 0 and |t| = 32 by 1 (the nearest
    whole unit of Q); no crowd leaves the phase alone; on the GameBoard (the
    world of (c) with the phase 60) the same six phases and the turn at the
    fourth interval;
(c) the sign: a paid unit of `light` on +x at phase 63 at a Node of a
    4 x 1 x 2 GameBoard (x and y periodic, z open, the two measured events
    the numbers need parked on the unvisited plane z = 1, `release` [0, 1])
    with one free unit of `m` of another number on +y at every Node of the
    line (V = (0, 64, 0), kappa = -1, t = (0, -64, 0)) turns to (24, -1, 0)
    in the first interval on K's table, its label (64, 0, 0) -> (64, -3, 0),
    the `turned` line (0, -3, 0), the transit momentum line (64, 253, 0)
    (its label and the four crowd units' (0, 256, 0)), the running line
    equal to the recount; on the plane fan (the primitive (a, b, 0) with
    a >= 1 and a + |b| <= 13, whose finest step is (12, +-1, 0)) it turns to
    (12, -1, 0), the `turned` line (0, -5, 0); kappa of a paid family whose
    columns beyond gravity are 0 against a charged free family is (-1, 1),
    a reader whose charge column reads 2 against a crowd of charge 1 has
    kappa (1, 1) and its +x turns toward t = +V = (0, 64, 0) to (24, +1, 0),
    and the pair (1, 2) against (1, 3) reads (-5, 6); the record: the
    world's `hypotheses` ["meeting-v1"], `run.json` carrying `meeting` true
    and the `turned` line in its audit; without the key nothing turns, the
    phase stays 63 and the `turned` line is zero;
(d) untouched: the free rows of the world of (c) are equal at every one of
    six intervals to the free rows of the same world without the key
    (Node, direction, age, phase, number, amount, content); the paid unit's
    age, number, amount and content are unchanged by its turn; two paid
    units of two families (contents 1 and 2) at one Node with the crowd
    both turn to (24, -1, 0) (the same V; the `turned` line (0, -9, 0) =
    (0, -3, 0) + 2 x (0, -3, 0)), and at a Node without a free unit neither
    turns nor advances its phase (they never read each other); a free unit
    of the paid unit's own number on +y is not read (no turn, the phase 63
    kept) where one of another number turns it;
(e) the bijection: the periodic 8 x 8 x 4 world of the bijection test with
    its 300 fixed records split into 240 of the free family `m` (given the
    number 2 on the record: the GameBoard of rays alone names no emitter,
    and what the meeting reads is the number on the record) and 60 of the
    paid family `light` (every fifth, the number 1), `meeting: true`, 50
    forward then 50 inverse intervals: the sorted stores of both families
    bit-exact, the state at the turning point differing, the `turned` line
    nonzero at the turning point (at least one turn on the way) and zero
    again at the end, the running transit momentum line equal to the
    recount at every interval both ways; a phase-less paid family under
    the key is refused naming the register, and `meeting` that is not true
    or false is refused naming the key.
"""

from __future__ import annotations

import json
import math

import numpy as np
import pytest

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.meeting import (
    arc_shift,
    arc_table,
    column_sum,
    register,
    register_inverse,
)
from event_universe.events.nature_beam import direction_flight
from event_universe.events.run import execute_nature_beam_run
from tests.test_nature_beam_bijection import WORLD as BIJECTION_WORLD
from tests.test_nature_beam_bijection import fixed_beams

HEADINGS = {tuple(h) for h in PORT_HEADINGS}
REST = ((0, 0, 0), (0, 0, 0))
N = 64


def fan(manhattan: int) -> list[tuple[int, int, int]]:
    found = []
    for a in range(-manhattan, manhattan + 1):
        for b in range(-manhattan, manhattan + 1):
            for c in range(-manhattan, manhattan + 1):
                if (a or b or c) and abs(a) + abs(b) + abs(c) <= manhattan:
                    if math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1:
                        found.append((a, b, c))
    return sorted(found)


# The declared directions of series K's worlds beyond the six headings.
K_DECLARED = [v for v in fan(6) if v not in HEADINGS] + [
    (24, 1, 0),
    (24, -1, 0),
    (12, 1, 0),
    (12, -1, 0),
]
K_TABLE = (*REST, *PORT_HEADINGS, *K_DECLARED)
# A plane fan whose finest step off +x is (12, +-1, 0).
PLANE_DECLARED = [
    (a, b, 0)
    for a in range(1, 14)
    for b in range(-12, 13)
    if a + abs(b) <= 13 and math.gcd(a, abs(b)) == 1
]
PLANE_DECLARED = [v for v in PLANE_DECLARED if v not in HEADINGS]
COLUMNS = (("gravity", -1), ("charge", 1))


def test_the_arc_permutation_on_the_table_of_series_k():
    """(a)."""
    table = arc_table(direction_flight(K_TABLE).labels)
    assert table.units.shape == (296, 3) and not table.moving[0] and not table.moving[1]
    labels = [tuple(int(v) for v in table.units[i]) for i in range(2, 296)]
    targets: list[tuple[int, int, int]] = [
        (x, y, z)
        for x in range(-3, 4)
        for y in range(-3, 4)
        for z in range(-3, 4)
        if (x, y, z) != (0, 0, 0)
    ]
    targets += labels
    sums = []
    for i in range(400):
        first, second = labels[i % 294], labels[(37 * i + 11) % 294]
        total = tuple(first[k] + second[k] for k in range(3))
        if total != (0, 0, 0):
            sums.append((total[0], total[1], total[2]))
    targets += sums[:398]
    assert len(targets) == 1034
    identity = np.arange(296)
    for target in targets:
        one = arc_shift(table, target, 1)
        assert sorted(one.tolist()) == list(range(296)) and one[0] == 0 and one[1] == 1
        forward, inverse = table.permutation(target)
        assert (forward == one).all() and (inverse[forward] == identity).all()
        assert (one[one[one]] == arc_shift(table, target, 3)).all()
    chain = [K_TABLE.index((1, 0, 0))]
    forward, _ = table.permutation((0, -1, 0))
    for _ in range(4):
        chain.append(int(forward[chain[-1]]))
    assert [K_TABLE[i] for i in chain[1:]] == [(24, -1, 0), (12, -1, 0), (5, -1, 0), (4, -1, 0)]
    # One crowd unit's flow, the target (0, -64, 0) (the unit label of -y,
    # among the targets above): the same chain, its own cache entry beside
    # (0, -1, 0)'s (the sectors depend on |t|).
    unit_flow, _ = table.permutation((0, -64, 0))
    chain = [K_TABLE.index((1, 0, 0))]
    for _ in range(4):
        chain.append(int(unit_flow[chain[-1]]))
    assert [K_TABLE[i] for i in chain[1:]] == [(24, -1, 0), (12, -1, 0), (5, -1, 0), (4, -1, 0)]
    assert table.cache[(0, -64, 0)] is not table.cache[(0, -1, 0)]
    # On the six headings alone +x is a sector of one under t = -y, fixed;
    # the on-line pair +y, -y swaps; the rest directions stay.
    headings = arc_table(direction_flight((*REST, *PORT_HEADINGS)).labels)
    six = arc_shift(headings, (0, -1, 0), 1)
    assert six.tolist() == [0, 1, 2, 3, 5, 4, 6, 7]


def test_the_register_reads_the_crowd_into_the_phase():
    """(b)."""
    phases, ks = [], []
    phase = np.array([60])
    for _ in range(6):
        k, phase = register(phase, np.array([64]), N)
        ks.append(int(k[0]))
        phases.append(int(phase[0]))
    assert phases == [61, 62, 63, 0, 1, 2] and ks == [0, 0, 0, 1, 0, 0]
    k, phase = register(np.array([60]), np.array([128]), N)
    assert (int(k[0]), int(phase[0])) == (0, 62)
    k, phase = register(phase, np.array([128]), N)
    assert (int(k[0]), int(phase[0])) == (1, 0)
    for before, norm in ((60, 64), (63, 64), (0, 64), (60, 128), (62, 128), (5, 31), (5, 32), (7, 0)):
        k, after = register(np.array([before]), np.array([norm]), N)
        k_back, phase_back = register_inverse(after, np.array([norm]), N)
        assert int(k_back[0]) == int(k[0]) and int(phase_back[0]) == before
    assert register(np.array([5]), np.array([31]), N)[1].tolist() == [5]
    assert register(np.array([5]), np.array([32]), N)[1].tolist() == [6]
    assert register(np.array([7]), np.array([0]), N)[1].tolist() == [7]
    world = parse_nature_beam_world(sign_world(60))
    simulation = NatureBeamSimulation(world)
    light = simulation.stores[0]
    seen = []
    for _ in range(6):
        simulation.step()
        seen.append((int(light.phase[0]), world.directions[int(light.direction[0])]))
    assert seen == [
        (61, (1, 0, 0)),
        (62, (1, 0, 0)),
        (63, (1, 0, 0)),
        (0, (24, -1, 0)),
        (1, (24, -1, 0)),
        (2, (24, -1, 0)),
    ]


def sign_world(
    phase: int,
    meeting: bool = True,
    declared: list[tuple[int, int, int]] | None = None,
    crowd_number: int = 2,
    extra: list[dict[str, object]] | None = None,
    crowd: bool = True,
) -> dict[str, object]:
    """A paid unit on +x on the line y = 0, z = 0 of a 4 x 1 x 2 GameBoard
    (x and y periodic, so the free units on +y stay at their Nodes and the
    paid unit circles the line), one free unit on +y at every Node of the
    line; the two measured events the numbers name are parked on the plane
    z = 1, which nothing visits, and release nothing."""
    directions = K_DECLARED if declared is None else declared
    rows: list[dict[str, object]] = [
        {
            "position": [0, 0, 0],
            "family": "light",
            "number": 1,
            "direction": [1, 0, 0],
            "amount": 1,
            "phase": phase,
        }
    ]
    if crowd:
        rows += [
            {
                "position": [x, 0, 0],
                "family": "m",
                "number": crowd_number,
                "direction": [0, 1, 0],
                "amount": 1,
                "phase": 0,
            }
            for x in range(4)
        ]
    rows += extra or []
    return {
        "law": "beam",
        "model_id": "meeting-sign-test",
        "shape": [4, 1, 2],
        "boundary": {"x": "periodic", "y": "periodic"},
        "ticks": 8,
        "K": 1 << 20,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "age_bound": 64,
        "directions": [list(v) for v in directions],
        "families": [
            {"name": "light", "quantum": 1},
            {"name": "m", "quantum": 0, "charge": 3},
            {"name": "photon", "quantum": 2},
        ],
        "measured": [
            {"position": [0, 0, 1], "family": "light", "amount": 1, "fixed": True},
            {"position": [1, 0, 1], "family": "m", "amount": 1, "fixed": True},
        ],
        "in_transit": rows,
        "meeting": meeting,
    }


def test_the_sign_of_the_turn_and_the_turned_line(tmp_path):
    """(c)."""
    world = parse_nature_beam_world(sign_world(63))
    assert world.meeting and world.hypotheses == ["meeting-v1"]
    simulation = NatureBeamSimulation(world)
    light = simulation.stores[0]
    simulation.step()
    assert world.directions[int(light.direction[0])] == (24, -1, 0) and int(light.phase[0]) == 0
    books = simulation.books()
    assert books["momentum"]["turned"] == [0, -3, 0]
    assert books["families"]["light"]["turned"] == [0, -3, 0]
    assert books["families"]["m"]["turned"] == [0, 0, 0]
    assert books["momentum"]["transit"] == [64, 253, 0]
    assert simulation.books(recount=True)["momentum"]["transit"] == [64, 253, 0]
    plane = parse_nature_beam_world(sign_world(63, declared=PLANE_DECLARED))
    simulation = NatureBeamSimulation(plane)
    simulation.step()
    assert plane.directions[int(simulation.stores[0].direction[0])] == (12, -1, 0)
    assert simulation.books()["momentum"]["turned"] == [0, -5, 0]
    # kappa: the column sum of the paid family against the free one.
    paid = ((1, 1), (0, 1))
    assert column_sum(paid, ((1, 1), (3, 1)), COLUMNS) == (-1, 1)
    assert column_sum(((1, 1), (2, 1)), ((1, 1), (1, 1)), COLUMNS) == (1, 1)
    assert column_sum(((1, 1), (1, 2)), ((1, 1), (1, 3)), COLUMNS) == (-5, 6)
    table = arc_table(direction_flight(K_TABLE).labels)
    forward, _ = table.permutation((0, 64, 0))
    assert K_TABLE[int(forward[K_TABLE.index((1, 0, 0))])] == (24, 1, 0)
    # The record of a run.
    document = sign_world(63)
    folder = tmp_path / "meeting"
    folder.mkdir()
    execute_nature_beam_run(world, json.dumps(document).encode("utf-8"), folder, "test", 2)
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    assert record["meeting"] is True and record["hypotheses"] == ["meeting-v1"]
    assert record["audit"][0]["momentum"]["turned"] == [0, -3, 0]
    assert record["audit"][1]["families"]["light"]["turned"] == [0, -3, 0]
    # Without the key nothing turns.
    quiet = parse_nature_beam_world(sign_world(63, meeting=False))
    assert not quiet.meeting and quiet.hypotheses == []
    simulation = NatureBeamSimulation(quiet)
    simulation.step()
    assert quiet.directions[int(simulation.stores[0].direction[0])] == (1, 0, 0)
    assert int(simulation.stores[0].phase[0]) == 63
    assert simulation.books()["momentum"]["turned"] == [0, 0, 0]


def rows_of(simulation: NatureBeamSimulation, family: int) -> np.ndarray:
    store = simulation.stores[family]
    rows = np.stack(
        [store.node, store.direction, store.age, store.phase, store.number, store.amount, store.content],
        axis=1,
    )
    return rows[np.lexsort(rows.T[::-1])]


def test_the_crowd_and_the_record_are_untouched():
    """(d)."""
    with_key = NatureBeamSimulation(parse_nature_beam_world(sign_world(63)))
    without = NatureBeamSimulation(parse_nature_beam_world(sign_world(63, meeting=False)))
    before = rows_of(with_key, 0)[0]
    for _ in range(6):
        with_key.step()
        without.step()
        assert np.array_equal(rows_of(with_key, 1), rows_of(without, 1))
    after = rows_of(with_key, 0)[0]
    # The row: node, direction, age, phase, number, amount, content.
    assert after[1] != before[1] and after[3] != before[3]
    assert (after[2], after[4], after[5], after[6]) == (6, 1, 1, 1)
    # Two paid units of two families at one Node read the same V.
    second = {
        "position": [0, 0, 0],
        "family": "photon",
        "number": 1,
        "direction": [1, 0, 0],
        "amount": 1,
        "phase": 63,
    }
    world = parse_nature_beam_world(sign_world(63, extra=[second]))
    simulation = NatureBeamSimulation(world)
    simulation.step()
    assert world.directions[int(simulation.stores[0].direction[0])] == (24, -1, 0)
    assert world.directions[int(simulation.stores[2].direction[0])] == (24, -1, 0)
    assert simulation.books()["momentum"]["turned"] == [0, -9, 0]
    assert simulation.books()["families"]["photon"]["turned"] == [0, -6, 0]
    # Without a crowd they never read each other: no turn, no advance.
    world = parse_nature_beam_world(sign_world(63, extra=[second], crowd=False))
    simulation = NatureBeamSimulation(world)
    simulation.step()
    for family in (0, 2):
        store = simulation.stores[family]
        assert world.directions[int(store.direction[0])] == (1, 0, 0) and int(store.phase[0]) == 63
    # An own-number free row is not read.
    world = parse_nature_beam_world(sign_world(63, crowd_number=1))
    simulation = NatureBeamSimulation(world)
    simulation.step()
    store = simulation.stores[0]
    assert world.directions[int(store.direction[0])] == (1, 0, 0) and int(store.phase[0]) == 63
    assert simulation.books()["momentum"]["turned"] == [0, 0, 0]


def meeting_bijection_world() -> dict[str, object]:
    world = dict(BIJECTION_WORLD)
    world["model_id"] = "meeting-bijection-test"
    world["families"] = [
        {"name": "m", "quantum": 0},
        {"name": "light", "quantum": 1, "phase_per_link": 5},
    ]
    world["meeting"] = True
    rows = []
    for k, beam in enumerate(fixed_beams()):
        row = dict(beam)
        row["family"] = "light" if k % 5 == 0 else "m"
        rows.append(row)
    world["in_transit"] = rows
    return world


def test_fifty_intervals_forward_and_back_with_the_meeting_return_the_stores():
    """(e)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(meeting_bijection_world()))
    assert simulation.stores[1].size == 65 and simulation.stores[0].size == 259
    # The crowd's rows take the number 2 on the record: what the meeting
    # reads is the number on the record, and a GameBoard of rays alone
    # names no emitter.
    simulation.stores[0].number[:] = 2
    start = [rows_of(simulation, family) for family in (0, 1)]
    for _ in range(50):
        simulation.step()
        books = simulation.books()
        assert books["momentum"]["transit"] == simulation.books(recount=True)["momentum"]["transit"]
    middle = [rows_of(simulation, family) for family in (0, 1)]
    assert not np.array_equal(middle[1], start[1])
    assert simulation.ledger.turned_momentum[1] != [0, 0, 0]
    assert simulation.ledger.turned_momentum[0] == [0, 0, 0]
    for _ in range(50):
        simulation.inverse_step()
        books = simulation.books()
        assert books["momentum"]["transit"] == simulation.books(recount=True)["momentum"]["transit"]
    assert simulation.tick == 0
    for family in (0, 1):
        assert np.array_equal(rows_of(simulation, family), start[family])
    assert simulation.ledger.turned_momentum[1] == [0, 0, 0]


def test_the_refusals_under_the_key():
    """(e), the refusals."""
    world = sign_world(63)
    world["families"] = [{"name": "light", "quantum": 1, "phase": False}, {"name": "m", "quantum": 0}]
    world["in_transit"] = [row for row in world["in_transit"] if row["family"] != "photon"]
    for row in world["in_transit"]:
        if row["family"] == "light":
            row["phase"] = 0
    with pytest.raises(ValueError, match="phase register"):
        parse_nature_beam_world(world)
    world["meeting"] = False
    assert not parse_nature_beam_world(world).meeting
    world = sign_world(63)
    world["meeting"] = 1
    with pytest.raises(ValueError, match="meeting must be true or false"):
        parse_nature_beam_world(world)
