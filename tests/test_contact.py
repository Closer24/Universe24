"""The contact through the table (the Beam Law, docs/BEAM_LAW.md, section 3
step 5 and the implementation note on the columns, part (ix); the model
owner, 2026-09-20, on the physicist's design of the strong force, section
4.4): a body whose step on an axis is refused because the destination holds
another measured event has arrived at that occupant, and the occupant's
table entry for the body's family decides as it decides for a ray:
`measure` hands the body's momentum component on that axis to the occupant
(the body's 0, the occupant's raised by it), `rerelease` returns it (the
body's component reversed, the occupant's raised by twice it), `read` and
`pass` leave the step refused and the labels as they are (the rule as it
was: the component accumulating under every push). Where the entry is the
keys' own rule for the body's family, declared or not (an entry equal to
the default changes nothing), the contact is `measure`: a body arriving at
a body is a paid arrival, its momentum its own label, kappa = 1, and the
keys' rule for a paid arrival is `measure`; so `read` accumulates only
where it is declared against the keys, on a paid family. A body on a set
of Nodes hands
the component apportioned whole over the occupants of its destination set
by their contents. The expected integers of docs/TEST_EXPECTATIONS.md ("The
contact through the table"), written down before the first run (the
physicist's DESIGN.md, test (f), and the integers of its section 4.4); K
2^20, N 64, `suspension` 0, `width` 1, every family without a phase circle:

(a) the pair on the six headings (DESIGN test (f)): two protons of the
    family `p` (amount 4, charge 3) holding one unit of `g` (strong 11 with
    the sign minus, lifetime 3), the charges Q 12, G 11 and the content
    M 5, at one Link on an open 9^3 GameBoard, `release` [1, 1]: from tick 2
    each reads per interval the `p` row of amount 4 as -7936 (gravity
    +1280, electric -9216) and the `g` row as +8064 (gravity +320, strong
    +7744), the push +128 toward the other, `(Q^2 - G^2 - M^2) x (-64)`;
    under the contact (no rule declared: `measure`) the momentum of p1
    over ticks 2 .. 8 reads 128, 0, 0, 128, 256, 384, 512 (the mirror on
    p2), the hand-overs at ticks 3 (256), 4 (128), 9 (640), 13 (512), 14
    (128), 16 (256) and 18 (256), each a `contact` record (p1 to p2, the
    family `p`, the rule `measure`, the axis 0, the component), p2 never
    handing (its label is 0 when its turn comes), no step in 30 intervals,
    the largest label 640 (handed at tick 9; after a tick no label is
    beyond 512), the sum of the two momenta 0 after every tick,
    the books balanced; with `read` declared for `p` on both, the keys'
    own rule, the same hand-overs; with `pass` declared the `p` rows are
    passed too and the `g` rows alone push, 8064 x (tick - 1). At three
    Links (x 2 and x 5) no `g` row reaches either body (the border takes
    it at the age 3), the `p` row's -7936 is read at tick 6, and at tick
    6 p1 steps to x 1 with (-7936, 0, 0) and p2 to x 6 with (7936, 0, 0):
    the pair separates, no contact;
(b) the isolated hand-over (`release` [0, 1], no rays): p1 of `p`, content
    5, momentum (256, 0, 0) at (1, 2, 2) and p2 of `q`, content 5, fixed,
    at (2, 2, 2) on an open 5^3 GameBoard: the step rule fires at tick 3
    (`by_clock(2, 256, 576)` = 1) and is refused; under `measure` (the
    default) p1 reads (0, 0, 0) and p2 (256, 0, 0), one `contact` record
    {tick 3, number 1, node (1, 2, 2), to (2, 2, 2), occupant 2, family
    `p`, rule `measure`, axis 0, component 256, momentum (0, 0, 0)}, p2's
    `contacts` [1, 0], the books' measured momentum line (256, 0, 0)
    before and after; under `rerelease` p1 (-256, 0, 0) and p2 (512, 0, 0),
    the component 512; under `pass` both unchanged, no record, the step
    counted (p1's `steps` 1); an entry that declares no rule (`{"reads":
    "scalar"}`) or the keys' own rule (`{"p": "read"}`) leaves the
    default; a body of the paid family `h` (quantum 1, content 5, the same
    momentum) hands 256 by the keys (`measure`) and keeps it under `read`
    declared against the keys and under `pass`; the parser derives
    `contact` ("measure", "measure", "measure") from an empty table,
    ("measure", "measure", "read") from `{"h": "read"}` and ("pass",
    "measure", "measure") from `{"p": "pass"}`;
(c) the apportioning: a body of span [1, 3, 1] (content 5, momentum
    (300, 0, 0) at (1, 2, 2)) whose destination set holds q1 (content 1) at
    (2, 1, 2) and q2 (content 3) at (2, 3, 2): 75 to q1 and 225 to q2, the
    body 0, two records; with 301, 75 and 226 (the unit left to the
    largest remainder); with q1 declaring `pass` for the body's family,
    q1 takes nothing and the body keeps its 75; a body of span [1, 3, 1]
    against one occupant hands it the whole component;
(d) the register's pair, a proton (1836 of `p`, charge 4, holding one
    unit of `nuclear`, strong 10000 with the sign minus, lifetime 3) and a
    neutron (1839 of `n` holding one unit of `nuclear`) at one Link on an
    open 5^3 GameBoard, both releasing on the 290 primitive directions
    with |a| + |b| + |c| <= 6, `release` [1, 1]: the pushes on the proton
    per interval 10 161 754 944 from the neutron's `n` rows (1837 x 1839 x
    3008, the x components of the 57 unit vectors whose first step is -x
    summing to 3008) and 300 805 525 696 from its `nuclear` rows (10000 x
    10000 x 3008 + 1837 x 3008), the sum 310 967 280 640 (on the neutron
    10 161 745 920 = 1840 x 1836 x 3008 and 300 805 534 720 = 300 800 000 000
    + 1840 x 3008, the same sum: the mirror); under the contact the labels after 1000 intervals (0, 0, 0)
    and (0, 0, 0), 999 hand-overs, the largest component 310 967 280 640
    (one interval's push), no step, the books balanced at every tick;
    with `pass` declared on each for the other's family (the rows of that
    family passed too, the `nuclear` rows alone read) the labels after 40
    intervals 39 x 300 805 525 696 = 11 731 415 502 144 on the proton and
    -39 x 300 805 534 720 = -11 731 415 854 080 on the neutron, no record.
"""

from __future__ import annotations

import itertools
import math

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
FAN = [
    list(v)
    for v in itertools.product(range(-6, 7), repeat=3)
    if 1 < sum(abs(c) for c in v) <= 6 and math.gcd(*[abs(c) for c in v]) == 1
]
PUSH_P = 10_161_754_944
PUSH_NUCLEAR = 300_805_525_696
PUSH_PAIR = PUSH_P + PUSH_NUCLEAR
# The mirror on the neutron: 1840 x 1836 x 3008 and 10000 x 10000 x 3008 +
# 1840 x 3008, the same sum.
PUSH_N = 10_161_745_920
PUSH_NUCLEAR_ON_N = 300_805_534_720
assert PUSH_N + PUSH_NUCLEAR_ON_N == PUSH_PAIR


def run(document: dict[str, object], ticks: int) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), records.append)
    for tick in range(1, ticks + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
    return simulation, records


def contacts(records: list[dict[str, object]]) -> list[dict[str, object]]:
    return [r for r in records if r["event"] == "contact"]


# -- (a) ---------------------------------------------------------------------------


def pair_world(gap: int, rule: str | None = None) -> dict[str, object]:
    table = {} if rule is None else {"p": rule}
    left = 4 - (gap + 1) // 2
    return {
        "law": "beam",
        "model_id": "contact-pair",
        "shape": [9, 9, 9],
        "boundary": "open",
        "ticks": 30,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "width": 1,
        "families": [
            {"name": "p", "quantum": 0, "phase": False, "charge": 3},
            {
                "name": "g",
                "quantum": 0,
                "phase": False,
                "columns": {"strong": {"value": 11, "sign": -1}},
                "lifetime": 3,
            },
        ],
        "measured": [
            {"position": [left, 4, 4], "family": "p", "amount": 4, "held": {"g": 1}, "table": table},
            {
                "position": [left + gap, 4, 4],
                "family": "p",
                "amount": 4,
                "held": {"g": 1},
                "table": table,
            },
        ],
    }


def test_the_pair_on_the_six_headings():
    """(a)."""
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(pair_world(1)), records.append)
    p1, p2 = simulation.measured[1], simulation.measured[2]
    assert p1.charges() == [(5, 1), (12, 1), (11, 1)] and p1.contact == ("measure", "measure")
    momenta = {}
    for tick in range(1, 31):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert p1.position == (3, 4, 4) and p2.position == (4, 4, 4)
        assert [a + b for a, b in zip(p1.momentum, p2.momentum, strict=True)] == [0, 0, 0]
        assert p2.momentum == [-p1.momentum[0], 0, 0]
        momenta[tick] = p1.momentum[0]
        reads = [
            (r["measured"], r["family"], r["push"][0])
            for r in records
            if r["event"] == "read" and r["tick"] == tick
        ]
        expected = (
            [] if tick == 1 else [(1, "p", -7936), (1, "g", 8064), (2, "p", 7936), (2, "g", -8064)]
        )
        assert reads == expected, tick
    assert [momenta[t] for t in range(2, 9)] == [128, 0, 0, 128, 256, 384, 512]
    handed = [(r["tick"], r["component"]) for r in contacts(records)]
    assert handed == [
        (3, 256),
        (4, 128),
        (9, 640),
        (13, 512),
        (14, 128),
        (16, 256),
        (18, 256),
        (21, 384),
        (23, 256),
        (25, 256),
        (27, 256),
        (28, 128),
        (30, 256),
    ]
    assert all(
        (r["number"], r["occupant"], r["family"], r["rule"], r["axis"], r["node"], r["to"])
        == (1, 2, "p", "measure", 0, [3, 4, 4], [4, 4, 4])
        for r in contacts(records)
    )
    # The largest label held is the 640 handed at tick 9 (512 + 128 within
    # the tick); after a tick no label is beyond 512.
    assert max(abs(int(str(r["component"]))) for r in contacts(records)) == 640
    assert max(abs(v) for v in momenta.values()) == 512
    assert not [r for r in records if r["event"] == "step"]
    assert p2.contacts == [13, 0] and p1.contacts == [0, 0]
    assert p1.state()["contacts"] == [0, 0]
    # `read` declared for `p` is the keys' own rule: it declares nothing,
    # and the hand-overs are the same.
    simulation, records = run(pair_world(1, "read"), 4)
    assert simulation.measured[1].contact == ("measure", "measure")
    assert [(r["tick"], r["component"]) for r in contacts(records)] == [(3, 256), (4, 128)]
    # `pass` passes the `p` rays too: the `g` rows alone push.
    simulation, records = run(pair_world(1, "pass"), 4)
    assert simulation.measured[1].momentum == [8064 * 3, 0, 0] and not contacts(records)
    # Three Links: the border takes the `g` rows, the pair separates.
    simulation, records = run(pair_world(3), 7)
    reads = [
        (r["tick"], r["measured"], r["family"], r["push"][0]) for r in records if r["event"] == "read"
    ]
    assert reads == [(6, 1, "p", -7936), (6, 2, "p", 7936)]
    steps = [(r["tick"], r["number"], r["to"], r["momentum"]) for r in records if r["event"] == "step"]
    assert steps[:2] == [(6, 1, [1, 4, 4], [-7936, 0, 0]), (6, 2, [6, 4, 4], [7936, 0, 0])]
    assert not contacts(records)


# -- (b) ---------------------------------------------------------------------------


def isolated(
    table: dict[str, object] | None = None, family: str = "p", **keys: object
) -> dict[str, object]:
    occupant: dict[str, object] = {"position": [2, 2, 2], "family": "q", "amount": 5, "fixed": True}
    if table is not None:
        occupant["table"] = table
    base: dict[str, object] = {
        "law": "beam",
        "model_id": "contact-isolated",
        "shape": [5, 5, 5],
        "boundary": "open",
        "ticks": 3,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "width": 1,
        "families": [
            {"name": "p", "quantum": 0, "phase": False},
            {"name": "q", "quantum": 0, "phase": False},
            {"name": "h", "quantum": 1, "phase": False},
        ],
        "measured": [
            {"position": [1, 2, 2], "family": family, "amount": 5, "momentum": [256, 0, 0]},
            occupant,
        ],
    }
    base.update(keys)
    return base


def test_the_isolated_hand_over_under_every_rule():
    """(b)."""
    world = parse_nature_beam_world(isolated())
    assert world.measured[1].contact == ("measure", "measure", "measure")
    assert parse_nature_beam_world(isolated({"p": "read"})).measured[1].contact == (
        "measure",
        "measure",
        "measure",
    )
    assert parse_nature_beam_world(isolated({"h": "read"})).measured[1].contact == (
        "measure",
        "measure",
        "read",
    )
    assert parse_nature_beam_world(isolated({"p": "pass"})).measured[1].contact == (
        "pass",
        "measure",
        "measure",
    )
    simulation, records = run(isolated(), 3)
    body, occupant = simulation.measured[1], simulation.measured[2]
    assert body.position == (1, 2, 2) and body.momentum == [0, 0, 0] and occupant.momentum == [256, 0, 0]
    assert records == [
        {
            "event": "contact",
            "tick": 3,
            "number": 1,
            "node": [1, 2, 2],
            "to": [2, 2, 2],
            "occupant": 2,
            "family": "p",
            "rule": "measure",
            "axis": 0,
            "component": 256,
            "momentum": [0, 0, 0],
        }
    ]
    assert occupant.contacts == [1, 0, 0] and body.steps == 1
    assert simulation.books()["momentum"]["measured"] == [256, 0, 0]
    simulation, records = run(isolated({"p": "rerelease"}), 3)
    assert simulation.measured[1].momentum == [-256, 0, 0]
    assert simulation.measured[2].momentum == [512, 0, 0]
    assert [(r["rule"], r["component"]) for r in records] == [("rerelease", 512)]
    assert simulation.books()["momentum"]["measured"] == [256, 0, 0]
    for table, family in (({"p": "pass"}, "p"), ({"h": "read"}, "h"), ({"h": "pass"}, "h")):
        simulation, records = run(isolated(table, family), 3)
        assert simulation.measured[1].momentum == [256, 0, 0]
        assert simulation.measured[2].momentum == [0, 0, 0]
        assert records == [] and simulation.measured[1].steps == 1
    # The paid body by the keys: `measure`, the hand-over.
    simulation, records = run(isolated(None, "h"), 3)
    assert simulation.measured[2].momentum == [256, 0, 0] and simulation.measured[2].contacts == [
        0,
        0,
        1,
    ]
    assert [(r["family"], r["rule"], r["component"]) for r in records] == [("h", "measure", 256)]
    simulation, records = run(isolated({"p": "read"}), 3)
    assert simulation.measured[2].momentum == [256, 0, 0] and len(records) == 1
    simulation, records = run(isolated({"p": {"reads": "scalar"}}), 3)
    assert simulation.measured[2].momentum == [256, 0, 0] and len(records) == 1


# -- (c) ---------------------------------------------------------------------------


def wide(momentum: int, occupants: list[dict[str, object]]) -> dict[str, object]:
    body = {
        "position": [1, 2, 2],
        "family": "p",
        "amount": 5,
        "momentum": [momentum, 0, 0],
        "span": [1, 3, 1],
    }
    return isolated(measured=[body, *occupants])


def test_the_apportioning_over_the_occupants():
    """(c)."""
    q1: dict[str, object] = {"position": [2, 1, 2], "family": "q", "amount": 1, "fixed": True}
    q2: dict[str, object] = {"position": [2, 3, 2], "family": "q", "amount": 3, "fixed": True}
    simulation, records = run(wide(300, [q1, q2]), 3)
    assert simulation.measured[1].momentum == [0, 0, 0]
    assert simulation.measured[2].momentum == [75, 0, 0]
    assert simulation.measured[3].momentum == [225, 0, 0]
    assert [(r["occupant"], r["component"]) for r in records] == [(2, 75), (3, 225)]
    simulation, records = run(wide(301, [q1, q2]), 3)
    assert [(r["occupant"], r["component"]) for r in records] == [(2, 75), (3, 226)]
    assert simulation.measured[1].momentum == [0, 0, 0]
    simulation, records = run(wide(300, [{**q1, "table": {"p": "pass"}}, q2]), 3)
    assert simulation.measured[1].momentum == [75, 0, 0]
    assert simulation.measured[2].momentum == [0, 0, 0]
    assert simulation.measured[3].momentum == [225, 0, 0]
    assert [(r["occupant"], r["component"]) for r in records] == [(3, 225)]
    one: dict[str, object] = {"position": [2, 2, 2], "family": "q", "amount": 4, "fixed": True}
    simulation, records = run(wide(300, [one]), 3)
    assert simulation.measured[1].momentum == [0, 0, 0]
    assert simulation.measured[2].momentum == [300, 0, 0]
    assert [(r["occupant"], r["component"]) for r in records] == [(2, 300)]


# -- (d) ---------------------------------------------------------------------------


def nucleon_pair(ticks: int, accumulate: bool = False) -> dict[str, object]:
    directions = HEADINGS + FAN
    proton: dict[str, object] = {
        "position": [2, 2, 2],
        "family": "p",
        "amount": 1836,
        "held": {"nuclear": 1},
        "directions": directions,
    }
    neutron: dict[str, object] = {
        "position": [3, 2, 2],
        "family": "n",
        "amount": 1839,
        "held": {"nuclear": 1},
        "directions": directions,
    }
    if accumulate:
        proton["table"] = {"n": "pass"}
        neutron["table"] = {"p": "pass"}
    return {
        "law": "beam",
        "model_id": "contact-nucleons",
        "shape": [5, 5, 5],
        "boundary": "open",
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "width": 1,
        "directions": FAN,
        "families": [
            {"name": "p", "quantum": 0, "phase": False, "charge": 4},
            {"name": "n", "quantum": 0, "phase": False},
            {
                "name": "nuclear",
                "quantum": 0,
                "phase": False,
                "columns": {"strong": {"value": 10000, "sign": -1}},
                "lifetime": 3,
            },
        ],
        "measured": [proton, neutron],
    }


def test_the_register_pair_over_a_thousand_intervals():
    """(d)."""
    assert len(FAN) == 284
    simulation, records = run(nucleon_pair(1000), 1000)
    proton, neutron = simulation.measured[1], simulation.measured[2]
    assert proton.momentum == [0, 0, 0] and neutron.momentum == [0, 0, 0]
    assert proton.position == (2, 2, 2) and neutron.position == (3, 2, 2)
    handed = contacts(records)
    assert len(handed) == 999 and max(abs(int(str(r["component"]))) for r in handed) == PUSH_PAIR
    assert not [r for r in records if r["event"] == "step"]
    pushes = {
        (r["family"], r["push"][0])  # type: ignore[index]
        for r in records
        if r["event"] == "read" and r["measured"] == 1
    }
    assert pushes == {("n", PUSH_P), ("nuclear", PUSH_NUCLEAR)}
    mirror = {
        (r["family"], r["push"][0])  # type: ignore[index]
        for r in records
        if r["event"] == "read" and r["measured"] == 2
    }
    assert mirror == {("p", -PUSH_N), ("nuclear", -PUSH_NUCLEAR_ON_N)}
    simulation, records = run(nucleon_pair(40, accumulate=True), 40)
    assert simulation.measured[1].momentum == [39 * PUSH_NUCLEAR, 0, 0]
    assert simulation.measured[2].momentum == [-39 * PUSH_NUCLEAR_ON_N, 0, 0]
    assert 39 * PUSH_NUCLEAR == 11_731_415_502_144 and 39 * PUSH_NUCLEAR_ON_N == 11_731_415_854_080
    assert not contacts(records)
