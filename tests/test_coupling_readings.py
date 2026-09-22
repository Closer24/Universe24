"""The coupling readings tool reads the engine's own functions (Highlights
5.4, the architecture review of 2026-09-20: the tools replayed three rules
of the engine, a second owner; `tools/coupling_readings.py` now reads
`engine.by_clock`, `nature_beam.direction_flight` with its `manhattan_steps`,
`nature_beam.unit_label`, `world.LABEL_SCALE` and the parsed world). Each
reading of the tool is checked against the engine on a minimal GameBoard; the
expected integers of docs/TEST_EXPECTATIONS.md ("The tools read the
engine"), written down first:

(a) the front: the tool's first arrivals of a heading ray at m = 1 .. 11
    Links are the intervals 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19
    (`test_nature_beam_flight` (a)) and equal, at every m, the first interval at
    which one unit declared on +x at (0, 0, 0) of an open 14 x 1 x 1 bar
    stands m Links out;
(b) the step rule under the law's line drive (since 2026-09-22, record
    972): a free probe of content 1 pushed once by (64, 0, 0) (one unit's
    label) steps by the tool's rule at the ticks 3, 6, 9 on x at width 1
    (the accumulator p Q = 4096 per interval against the wall Q^2 S m +
    |p|_1 T_h = 4096 + 7040 = 11136, the overflow kept) and at 5, 10 at
    width 3 (the wall 19328); pushed by (64, 64, 0) at (5, x), (6, y), (9,
    x), (10, y) (the wall 4096 + 128 x 110 = 18176 for both axes, x first
    on the tie at 5 with y keeping its overflow and stepping at 6, then
    x again on the tie at 9: the line of the momentum, no fire lost);
    under the per-axis drive of history (a
    bar declaring `per_axis_drive`, the tool's `drive` "per_axis") the same
    probe steps at 2, 4, 6, 8, 10 on x at width 1, at 4, 8 at width 3, and
    at 2, 4, 6, 8, 10 on x alone under (64, 64, 0) (x before y, the y fires
    lost); on the GameBoard a free measured event of content 1 with that
    declared momentum makes the same `step` records (tick, axis), width by
    width and drive by drive (the declared momentum a read at tick 0: since
    the crossing rule, BEAM_LAW note 48, a push read at tick t drives from
    tick t + 1, as the tool's rule has it);
(c) the release: `RELEASE_PER_HEADING` = by_clock(0, 2^24, 128) = 131072
    and q = 6 x 131072 = 786432; a source of 2^24 on the six headings at
    `release` [1, 128] has released 786432 units after its first
    self-creation (the books' transit line);
(d) the push: `label_push((1, 0, 0), 5, 3)` = (-960, 0, 0); a fixed reader
    of content 3 met by 5 units of another number arriving on +x is pushed
    (-960, 0, 0), and its `read` record says so;
(e) the declared charges: the engine's `Measured.charge`, the family's
    charge per unit of content times the content as a reduced pair, read
    as an integer where whole: [1, 2] on content 2^24 reads 2^23, [2, 1] on
    1 reads 2, [1, 2] on 4 reads 2, an integer -3 (as [-3, 1]) on 5 reads
    -15, no charge reads 0 and [1, 3] on 2 reads the fraction 2/3.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "coupling_readings_tool", ROOT / "tools" / "coupling_readings.py"
)
TOOL = importlib.util.module_from_spec(SPEC)
sys.modules["coupling_readings_tool"] = TOOL
SPEC.loader.exec_module(TOOL)

FIRST_ARRIVALS = [1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19]
UNIT = 64


def bar(shape: list[int], measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "coupling-readings-test",
        "shape": shape,
        "boundary": "open",
        "ticks": 10,
        "K": 1024,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        # The law's line drive with nothing declared (since 2026-09-22); the
        # per-axis drive of history under the key, passed by (b).
        "families": [{"name": "m", "quantum": 0, "phase": False}],
        "measured": measured,
    }
    world.update(keys)
    return world


def test_the_front_is_the_flight_tables_first_arrival_as_the_engine_walks_it():
    """(a)."""
    arrivals = TOOL.first_arrivals(5)
    assert [arrivals[m] for m in range(1, 12)] == FIRST_ARRIVALS
    beam = {"position": [0, 0, 0], "family": "m", "number": 1, "direction": [1, 0, 0], "amount": 1}
    simulation = NatureBeamSimulation(parse_nature_beam_world(bar([14, 1, 1], [], in_transit=[beam])))
    store = simulation.stores[0]
    walked: dict[int, int] = {}
    for tick in range(1, 21):
        simulation.step()
        assert store.size == 1, tick
        x = int(store.coordinates(store.node)[0][0])
        walked.setdefault(x, tick)
    assert [walked[m] for m in range(1, 12)] == [arrivals[m] for m in range(1, 12)]


def engine_steps(momentum: list[int], width: int, per_axis: bool = False) -> list[tuple[int, int]]:
    """The (tick, axis) of the `step` records of a free measured event of
    content 1 at (2, 2, 0) of an open 20 x 5 x 1 GameBoard (room for two
    steps on y) with the declared momentum, over ten intervals at the
    world's `width`, under the law's drive or, with `per_axis`, the drive
    of history under its key."""
    records: list[dict[str, object]] = []
    probe = {"position": [2, 2, 0], "family": "m", "amount": 1, "momentum": momentum}
    keys: dict[str, object] = {"width": width}
    if per_axis:
        keys["per_axis_drive"] = True
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar([20, 5, 1], [probe], **keys)), records.append
    )
    for _ in range(10):
        simulation.step()
        assert simulation.books()["balanced"]
    return [(int(e["tick"]), TOOL.step_axis(e)) for e in records if e["event"] == "step"]


def test_the_step_rule_is_the_engines_step_off_the_clock():
    """(b)."""
    # The law's line drive: the integers written first (the docstring).
    assert TOOL.steps_by_rule({0: (0, (UNIT, 0, 0))}, 1, 0, 10) == [(3, 0), (6, 0), (9, 0)]
    assert TOOL.steps_by_rule({0: (0, (UNIT, 0, 0))}, 1, 0, 10, 3) == [(5, 0), (10, 0)]
    assert TOOL.steps_by_rule({0: (0, (UNIT, UNIT, 0))}, 1, 0, 10, 1) == [
        (5, 0),
        (6, 1),
        (9, 0),
        (10, 1),
    ]
    for momentum, width in (([UNIT, 0, 0], 1), ([UNIT, 0, 0], 3), ([UNIT, UNIT, 0], 1)):
        reads = {0: (0, (momentum[0], momentum[1], momentum[2]))}
        assert engine_steps(momentum, width) == TOOL.steps_by_rule(reads, 1, 0, 10, width), (
            momentum,
            width,
        )
    # The per-axis drive of history under its key.
    x_only = [(t, 0) for t in (2, 4, 6, 8, 10)]
    axis = TOOL.AXIS_DRIVE
    assert TOOL.steps_by_rule({0: (0, (UNIT, 0, 0))}, 1, 0, 10, 1, axis) == x_only
    assert TOOL.steps_by_rule({0: (0, (UNIT, 0, 0))}, 1, 0, 10, 3, axis) == [(4, 0), (8, 0)]
    assert TOOL.steps_by_rule({0: (0, (UNIT, UNIT, 0))}, 1, 0, 10, 1, axis) == x_only
    for momentum, width in (([UNIT, 0, 0], 1), ([UNIT, 0, 0], 3), ([UNIT, UNIT, 0], 1)):
        reads = {0: (0, (momentum[0], momentum[1], momentum[2]))}
        assert engine_steps(momentum, width, per_axis=True) == TOOL.steps_by_rule(
            reads, 1, 0, 10, width, axis
        ), (momentum, width)


def test_the_release_per_heading_is_the_engines_clock():
    """(c)."""
    assert TOOL.RELEASE_PER_HEADING == 131072 and TOOL.Q == 6 * 131072
    source = {"position": [2, 2, 2], "family": "m", "amount": 1 << 24, "fixed": True}
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar([5, 5, 5], [source], release=[1, 128]))
    )
    simulation.step()
    assert simulation.ledger.transit_released[0] == TOOL.Q
    assert simulation.books()["balanced"]


def test_the_expected_push_is_the_engines_label_flow():
    """(d)."""
    assert TOOL.label_push((1, 0, 0), 5, 3) == (-960, 0, 0)
    assert TOOL.label_push((0, -1, 0), 2, 1) == (0, 128, 0)
    reader = {"position": [2, 0, 0], "family": "m", "amount": 3, "fixed": True}
    other = {"position": [6, 0, 0], "family": "m", "amount": 1, "fixed": True}
    beam = {"position": [1, 0, 0], "family": "m", "number": 2, "direction": [1, 0, 0], "amount": 5}
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(bar([8, 1, 1], [reader, other], in_transit=[beam])), records.append
    )
    simulation.step()
    assert simulation.measured[1].pushed == list(TOOL.label_push((1, 0, 0), 5, 3))
    reads = [e for e in records if e["event"] == "read" and e["measured"] == 1]
    assert [TOOL.vector(e["push"]) for e in reads] == [TOOL.label_push((1, 0, 0), 5, 3)]


def test_the_declared_charges_are_the_engines_charge_per_unit_of_content():
    """(e)."""
    families = [
        {"name": "q", "quantum": 0, "charge": [1, 2], "phase": False},
        {"name": "p", "quantum": 0, "charge": [2, 1], "phase": False},
        {"name": "h", "quantum": 0, "charge": [1, 2], "phase": False},
        {"name": "n", "quantum": 0, "charge": -3, "phase": False},
        {"name": "z", "quantum": 0, "phase": False},
        {"name": "t", "quantum": 0, "charge": [1, 3], "phase": False},
    ]
    measured = [
        {"position": [0, 0, 0], "family": "q", "amount": 1 << 24, "fixed": True},
        {"position": [1, 0, 0], "family": "p", "amount": 1, "fixed": True},
        {"position": [2, 0, 0], "family": "h", "amount": 4, "fixed": True},
        {"position": [3, 0, 0], "family": "n", "amount": 5, "fixed": True},
        {"position": [4, 0, 0], "family": "z", "amount": 9, "fixed": True},
        {"position": [5, 0, 0], "family": "t", "amount": 2, "fixed": True},
    ]
    world = parse_nature_beam_world(bar([6, 1, 1], measured, families=families))
    charges = TOOL.declared_charges(world)
    assert charges == [1 << 23, 2, 2, -15, 0, Fraction(2, 3)]
    assert [type(charge) for charge in charges[:5]] == [int] * 5
    assert charges == [
        entry.charge[0] if entry.charge[1] == 1 else Fraction(*entry.charge)
        for entry in NatureBeamSimulation(world).measured.values()
    ]


def test_a_gameboard_diagnostic_is_printed_and_never_counted():
    """Item 5's ring means, the cube flux and item 6's identity with the
    replay are GameBoard numbers (records 562 and 564; the audit of record
    567, F3 and F4): `Checks.diagnostic` keeps the number beside its
    expectation, names the detector reading behind it and leaves `failed`,
    `outside`, the rows and the readings untouched."""
    checks = TOOL.Checks()
    checks.diagnostic("5: flow x 2 pi r / q at r = 5", 0.97, 0.90, 1.10, TOOL.BEHIND_ITEM_5)
    checks.diagnostic("5: slope of the count", -1.3, -1.10, -0.90, TOOL.BEHIND_ITEM_5)
    checks.diagnostic_equal("6: (age, waited, owed)", (1, 2, 3), (1, 2, 4), "the probe's own record")
    assert [ok for _, ok, _ in checks.diagnostics] == [True, False, False]
    assert all("not yet read" in detail for _, _, detail in checks.diagnostics)
    assert checks.rows == [] and checks.readings == [] and checks.failed == 0 and checks.outside == 0
