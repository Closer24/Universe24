"""The split, the birth of a record and the phase per interval of age under
the amplitude law (`amplitude-v1`, the model owner, 2026-09-20; the design,
docs/designs/amplitude-v1/DESIGN.md sections 2.1, 2.3, 3.1 and 3.4; the owner's
unifications (1) and (2); docs/BEAM_LAW.md note 37), on the Mach-Zehnder
world of series L (`examples/events/amplitude/make_worlds.py`, the one
builder). The expected integers of docs/TEST_EXPECTATIONS.md ("The
amplitude law: the split"), written down before the first run:

(a) the birth: the source of `mz_equal` (content 2^20 at K 2^20, one row
    per self-creation on +x and +y, the turn 16 on +y) births at tick 1 one
    record, 2^32 + 1, of two rows at (0, 0): (+x, age 0, phase 0, amount 1,
    content 1, branch 0, multiplicity 2) and (+y, phase 16); at tick 3 the
    record 2^32 + 2 with the phases 1 and 17 (u the clock's phase; no
    birth at tick 2, where the exact clock of the content 2^20 - 2 turns
    0, the fraction-free law of 2026-09-20; the whole part off the clock
    put it at tick 2 until then); the lamp's `births` 2; the same lamp without the key (its `turns` dropped,
    which the key alone admits) births rows of record 0, multiplicity 1
    and phase 0 on both directions;
(b) the split: on `mz_equal` (the (20, 21) splitter) the store at tick 11
    holds at (3, 3) the record's two rows (+x, age 0, phase 16, amount 41,
    multiplicity 1682) and (+y, phase 32, amount 1, 1682): arm 1 arriving
    along +y (phase 0) transmitted 20 on +y at 0 and reflected 21 on +x at
    16, arm 2 arriving along +x (phase 16) transmitted 20 on +x at 16 and
    reflected 21 on +y at 32; the two +x rows merge in phase (41), the two
    +y rows cancel to 1 at 32 (the design's mz.txt: the offers 1681/1682
    and 1/1682); the ledger's `cancelled` lines 40 units, 40 content, the
    labels (0, 2560, 0); on `mz_balanced` ((1, 1)) the store holds (+x,
    16, amount 2, multiplicity 4) alone, 2 units cancelled, the books
    balanced at every tick with the `cancelled` line; the multiplicity is
    read in the rows (`state.json`); a row arriving at the splitter on a
    direction its `inputs` do not name refuses the run naming the Node;
(c) the phase per interval of age (the pair form of `phase_per_link`,
    refused without the key and on a family without a phase circle): a
    declared ray on +x of a 9 x 1 x 1 bar reads after 5 intervals the
    phase 40 at [8, 1] (every interval its age advances), 26 at [16, 3]
    (floor(5 x 16 / 3)) and 24 at the integer 8 (3 Links crossed: the
    integer form turns per Link, the two forms are not the same number on
    the flight table); a rest row turns nothing under the pair; `run.json`
    carries the pair as declared; on a periodic bar without measured
    events 5 forward and 5 inverse intervals return the phases bit-exact;
(d) the refusals of the split: `weights` without the key, on `measure`, on
    a free family's entry, of a wrong length, all zero, a turn beyond
    N - 1, `inputs` naming a direction the world does not declare, a
    lamp's `turns` without the key, a rate other than [1, 1] under it;
    a split whose multiplicity would pass 2^62 - 1 refuses the run naming
    the Node (a pending row of multiplicity 2^61 split by (20, 21), A = 841).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.measured import PendingRow
from event_universe.events.run import execute_nature_beam_run

ROOT = Path(__file__).resolve().parents[1]
N = 64


def load_generator():
    path = ROOT / "examples" / "events" / "amplitude" / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("amplitude_make_worlds", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["amplitude_make_worlds"] = module
    spec.loader.exec_module(module)
    return module


EXPECTATIONS = json.loads(
    (ROOT / "examples" / "events" / "amplitude" / "expectations.json").read_text("utf-8")
)


def registered_rows(rows: list[list[object]]) -> list[tuple[object, ...]]:
    """The register's rows (node, direction index, age, phase, amount,
    content, branch, multiplicity) in `rows_at`'s form."""
    return [(tuple(row[0]), *row[1:]) for row in rows]  # type: ignore[misc]


GENERATOR = load_generator()


def rows_at(simulation: NatureBeamSimulation, record: int) -> list[tuple[object, ...]]:
    return sorted(
        (r.node, r.direction, r.age, r.phase, r.amount, r.content, r.branch, r.multiplicity)
        for r in simulation.stores[0].rows()
        if r.record == record
    )


def test_the_birth_of_a_record_by_a_lamp():
    """(a)."""
    world = GENERATOR.mach_zehnder("mz_equal")
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    simulation.step()
    first = (1 << 32) + 1
    registered = EXPECTATIONS["mach_zehnder"]["mz_equal"]["birth"]
    assert rows_at(simulation, first) == registered_rows(registered["rows"])
    # The lamp's turn is the count of its accumulator (the fraction-free
    # law, 2026-09-20): the content 2^20 - 2 gives 0 at tick 2 (no birth)
    # and 2^21 - 4 gives 1 at tick 3, the second record born there (at
    # tick 2 under the whole part off the clock until then); the
    # register's `second`.
    second_registered = registered["second"]
    for _ in range(1, second_registered["tick"] - 1):
        simulation.step()
    second = (1 << 32) + 2
    assert rows_at(simulation, second) == [] and simulation.measured[1].births == 1
    assert simulation.measured[1].acc_turn == second_registered["accumulator_after_tick_2"]
    simulation.step()
    assert [r[3] for r in rows_at(simulation, second)] == second_registered["phases"]
    assert simulation.measured[1].births == 2


def test_the_split_at_the_splitter_and_the_cancel_on_the_game_board(tmp_path: Path):
    """(b)."""
    registered = EXPECTATIONS["mach_zehnder"]["mz_equal"]["split"]
    tick = int(registered["tick"])
    world = GENERATOR.mach_zehnder("mz_equal", ticks=tick)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    for _ in range(tick):
        simulation.step()
        assert simulation.books(recount=True)["balanced"]
    first = (1 << 32) + 1
    assert rows_at(simulation, first) == registered_rows(registered["rows"])
    ledger = simulation.ledger
    assert ledger.cancelled_amount[0] == registered["cancelled_amount"]
    assert ledger.cancelled_content[0] == registered["cancelled_content"]
    assert ledger.cancelled_momentum[0] == registered["cancelled_momentum"]
    books = simulation.books()
    assert books["families"]["light"]["transit"]["cancelled"] == registered["cancelled_amount"]
    assert books["momentum"]["cancelled"] == registered["cancelled_momentum"]
    balanced_registered = EXPECTATIONS["mach_zehnder"]["mz_balanced"]["split"]
    tick = int(balanced_registered["tick"])
    balanced = GENERATOR.mach_zehnder("mz_balanced", splitter=(1, 1), ticks=tick)
    out = tmp_path / "balanced"
    out.mkdir()
    execute_nature_beam_run(parse_nature_beam_world(balanced), b"{}", out, "test", tick)
    state = json.loads((out / "state.json").read_text())
    rows = [
        (
            tuple(node["position"]),
            tuple(ray["direction"]),
            ray["phase"],
            ray["amount"],
            ray["multiplicity"],
        )
        for node in state["nodes"]
        for f in node["families"]
        for ray in f["rays"]
        if ray["record"] == first
    ]
    assert rows == [(tuple(row[0]), tuple(row[1]), *row[2:]) for row in balanced_registered["rows"]]
    record = json.loads((out / "run.json").read_text())
    assert record["conserved_at_every_completed_tick"]
    cancelled = record["audit"][-1]["families"]["light"]["transit"]["cancelled"]
    assert cancelled == balanced_registered["cancelled"]
    # A row from a side the splitter's inputs do not name.
    one_sided = GENERATOR.mach_zehnder("one_sided", ticks=11)
    one_sided["measured"][3]["table"]["light"]["inputs"] = [[0, 1, 0]]
    one_sided["measured"][3]["table"]["light"]["weights"] = [[21, 20]]
    one_sided["measured"][3]["table"]["light"]["turns"] = [[16, 0]]
    lopsided = NatureBeamSimulation(parse_nature_beam_world(one_sided))
    with pytest.raises(ValueError, match=r"at \[3, 3, 0\] on the direction \[1, 0, 0\]"):
        for _ in range(11):
            lopsided.step()


def bar(frequency: object, periodic: bool = False, rest: bool = False) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "amplitude-phase-per-age",
        "shape": [9, 1, 1],
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"} if periodic else "open",
        "ticks": 5,
        "K": 1,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "age_bound": 100,
        "families": [{"name": "light", "quantum": 1, "phase_per_link": frequency}],
        "measured": [],
        "in_transit": [
            {
                "position": [0, 0, 0],
                "family": "light",
                "number": 1,
                "direction": 0 if rest else [1, 0, 0],
                "amount": 1,
                "phase": 0,
            }
        ],
    }


def test_the_phase_per_interval_of_age(tmp_path: Path):
    """(c)."""
    for frequency, expected in (([8, 1], 40), ([16, 3], 26), (8, 24)):
        simulation = NatureBeamSimulation(parse_nature_beam_world(bar(frequency)))
        for _ in range(5):
            simulation.step()
        (row,) = simulation.stores[0].rows()
        assert (row.phase, row.age) == (expected, 5), frequency
    resting = NatureBeamSimulation(parse_nature_beam_world(bar([8, 1], rest=True)))
    for _ in range(5):
        resting.step()
    assert resting.stores[0].rows()[0].phase == 0
    out = tmp_path / "pair"
    out.mkdir()
    execute_nature_beam_run(parse_nature_beam_world(bar([16, 3])), b"{}", out, "test", 1)
    record = json.loads((out / "run.json").read_text())
    assert record["families"][0]["phase_per_link"] == [16, 3]
    # The inverse on a periodic bar: 5 forward, 5 back, bit-exact.
    both = NatureBeamSimulation(parse_nature_beam_world(bar([16, 3], periodic=True)))
    before = both.stores[0].rows()
    for _ in range(5):
        both.step()
    assert both.stores[0].rows()[0].phase == 26
    for _ in range(5):
        both.inverse_step()
    assert both.stores[0].rows() == before
    phaseless = bar([8, 1])
    phaseless["families"][0]["phase"] = False
    with pytest.raises(ValueError, match="refused for a family without a phase circle"):
        parse_nature_beam_world(phaseless)


def test_the_refusals_of_the_split():
    """(d)."""
    base = GENERATOR.mach_zehnder("refusals")
    splitter = base["measured"][3]["table"]["light"]

    def variant(**changes: object) -> dict[str, object]:
        world = json.loads(json.dumps(base))
        world.update(changes)
        return world

    cases = [
        ({"rule": "measure", "weights": [1, 1]}, "on the rule 'measure'"),
        ({**splitter, "weights": [[1, 1, 1], [1, 1]]}, "one integer per declared direction"),
        ({**splitter, "weights": [[0, 0], [1, 1]]}, "at least one positive weight"),
        ({**splitter, "turns": [[64, 0], [0, 0]]}, "turns must be an integer from 0 through 63"),
        ({**splitter, "inputs": [[0, 1, 0], [2, 3, 0]]}, "names a direction the world does not declare"),
    ]
    for entry, message in cases:
        world = variant()
        world["measured"][3]["table"]["light"] = entry
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(world)
    free = variant()
    free["families"].append({"name": "m", "quantum": 0})
    free["measured"][3]["table"]["m"] = {"rule": "rerelease", "weights": [1, 1]}
    with pytest.raises(ValueError, match="free families never branch"):
        parse_nature_beam_world(free)
    # The multiplicity beyond the bound at the split, refused naming the Node.
    simulation = NatureBeamSimulation(parse_nature_beam_world(base))
    splitter_event = simulation.measured[4]
    assert splitter_event.position == (3, 3, 0)
    splitter_event.pending[0].append(
        PendingRow(1, 1, 0, record=(1 << 32) + 9, multiplicity=1 << 61, split=True, arrival=4)
    )
    with pytest.raises(OverflowError, match=r"multiplicity 2305843009213693952 x 841 .* at \[3, 3, 0\]"):
        simulation.step()
    assert np.all(simulation.stores[0].multiplicity <= (1 << 62) - 1)
