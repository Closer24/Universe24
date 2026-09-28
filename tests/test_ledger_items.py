"""The ledger's items, each with its small test written before the build and marked xfail strict until its support lands; every test speaks the run's files alone."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.running import lines_of, run_world, stamped
from tests.worlds import emitter_world, family_entry

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

STEPS = 120
READING_KINDS = {"DETECTOR", "GAMEBOARD", "HOST"}


def families_of(document: dict) -> list[dict]:
    entries = document["universe"]
    assert isinstance(entries, list)
    return entries


# (1) THE OUTPUT DECLARED IN ONE FORMAT (records 2191, 2199; the ledger's run declarations)


def test_1_the_output_holds_exactly_the_declared_readings_each_labelled_by_kind(tmp_path):
    """Every line the run writes is a reading the world file declared, labelled by its kind (DETECTOR, GAMEBOARD or HOST); one format for every experiment; the clicks of a declared detector are its DETECTOR reading."""
    document = emitter_world(stock=2, ticks=STEPS)
    document["readings"] = [
        {"name": "screen_clicks", "kind": "clicks", "detector": "screen"},
        {"name": "emitter_centre", "kind": "centre", "body": 0, "every": 40},
    ]
    stamped(document)
    output = run_world(document, tmp_path)
    readings = output["readings"]
    assert isinstance(readings, list) and {r["name"] for r in readings} == {
        "screen_clicks",
        "emitter_centre",
    }
    assert all(r["label"] in READING_KINDS for r in readings)
    clicks = next(r for r in readings if r["name"] == "screen_clicks")
    centre = next(r for r in readings if r["name"] == "emitter_centre")
    assert clicks["label"] == "DETECTOR" and centre["label"] == "GAMEBOARD"
    assert all({"interval", "node"} <= set(line) for line in clicks["lines"])
    assert [line["interval"] for line in centre["lines"]] == list(range(0, STEPS + 1, 40))


# (2) THE LOADER READS EVERY DECLARATION AS A GENERIC TERM (ALGEBRA.md #the-primitives; record 2186)


def test_2c_a_one_sided_send_is_refused_by_the_loader():
    """The send declaration admits a symmetric set of Ports alone: an axis on or off; a one-sided send (five Ports) is refused by name (the rule alone's record, section 13: a one-sided send is a gain, the rule's step amplifies without bound)."""
    document = emitter_world(stock=1, ticks=10)
    document["step"] = {
        "send": ["level", "pair", "accumulator"],
        "ports": ["-x", "+y", "-y", "+z", "-z"],
        "receive": "rotated",
        "wait": 1,
        "operation": "rule",
    }
    stamped(document)
    with pytest.raises(ValueError, match="step|ports|unknown keys"):
        parse_nature_beam_world(document)


# (3) THE SOURCE VERB AND THE TWO-SIDED GUARD (ALGEBRA.md #rule3, #the-paces)


def test_3a_a_sourced_family_is_written_where_its_records_are_and_nowhere_else():
    """A field family sourced by the matter records: after the first intervals its level is nonzero (the source's act through the folder, the count D_i of the body's own record); the same family sourced by a family with no record stays exactly zero everywhere (the leak test)."""
    document = emitter_world(stock=2, ticks=STEPS)
    well = {
        **family_entry(
            "well", [52, 53], [], clock=[512, 1]
        ),  # the depth of [1000, 1019] at a numerator the walls admit under the bound 2^24
        "sourced": {"of": "matter", "weight": 1, "scale": 1000},
    }
    null = {**well, "name": "null", "sourced": {**well["sourced"], "of": "charge"}}
    families_of(document).extend([well, null])
    stamped(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    for _ in range(20):
        simulation.step()
    names = [family.name for family in simulation.families]
    well_index, null_index = names.index("well"), names.index("null")
    assert int(np.abs(simulation.sourced_records[well_index].now).sum()) > 0
    assert int(np.abs(simulation.sourced_records[null_index].now).sum()) == 0


# (4) THE CLICK THAT KEEPS THE MOMENTUM: n A READING (ALGEBRA.md #the-primitives, the recoil's row)


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_4_the_bodys_momentum_is_the_reading_of_its_records_current_through_the_givings():
    """No click writes a body's momentum (the law's row "the recoil": the momentum a reading, no level): the emitter of the older form keeps its declared 0 at every interval through two windows' closes, both levels alike, and a giver whose mode carries no wave number (the fixture off the mode) takes no turn, its recoil book empty (ALGEBRA.md #the-interval, #the-primitives)."""
    lines: list[dict] = []
    document = stamped(emitter_world(stock=2, ticks=STEPS))
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    while len(lines_of(lines, "giving")) < 2:
        simulation.step()
        block = simulation.blocks[0]
        assert block.momentum == [0, 0, 0] == block.momentum_before and simulation.tick <= 2 * STEPS
    givings = [line["momentum"] for line in lines if line.get("event") == "giving"]
    assert all(momentum[1:] == [0, 0] for momentum in givings) and lines_of(lines, "recoil") == []
    assert simulation.recoil_turns == {} and not hasattr(simulation, "recoil_wall")


# (5) A CLICK'S CHANGE AFTER ALL ADVANCES; A RUN-TIME OVERFLOW BOUND (record 2185)


def test_5b_the_loads_bound_holds_at_run_time_no_level_leaves_the_integer_range():
    """A run-time overflow bound: on a shipped world every level and remainder the run writes stays within 2^62 in magnitude at every interval, so no int64 wrap can pass unseen (record 2185; the load's bound of world.py checks the start alone)."""
    document = emitter_world(stock=2, ticks=STEPS)
    stamped(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    bound = 1 << 62
    for _ in range(STEPS):
        simulation.step()
        for live in simulation.records.values():
            assert int(np.abs(live.now).max(initial=0)) < bound
            assert int(np.abs(live.remainder).max(initial=0)) < bound
