"""The lifetime's folder (ALGEBRA.md #the-primitives, the row "the lifetime"): the record's age against L, the click first, the refusals by name."""

from __future__ import annotations

from dataclasses import replace

import pytest

from event_universe.core.register import discover, folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.lifetime import DECLARATION, THE_WORD, LifetimeStart, LifetimeTerm, apply
from event_universe.world_files import parse_nature_beam_world
from tests.running import stamped
from tests.worlds import emitter_world


def test_the_declaration_is_the_ledgers_row_and_the_register_finds_it_built():
    assert DECLARATION.name == "the lifetime" and folder_of(DECLARATION.name) == "lifetime"
    assert DECLARATION.place == "(ii)" and DECLARATION.word == "after the step"
    assert DECLARATION.reads == ("the record's age", "L") and DECLARATION.writes == (
        "the record's tally",
    )
    assert THE_WORD in DECLARATION.section and DECLARATION.function is apply
    registered = discover().declarations["the lifetime"]
    assert registered.built and registered.function is apply


def test_a_record_ends_at_age_l_unless_the_ladder_clicked_it_first():
    """Below L the record lives; at L (and beyond, should a step be missed) it ends; a record the ladder clicked this interval is the click's, not the lifetime's; L = 0 and a negative age are refused by name."""
    term = LifetimeTerm(lifetime=3)
    assert [apply(term, LifetimeStart(age, False)).ends for age in (0, 1, 2, 3, 4)] == [
        False,
        False,
        False,
        True,
        True,
    ]
    assert not apply(term, LifetimeStart(3, True)).ends
    assert apply(LifetimeTerm(1), LifetimeStart(1, False)).ends
    with pytest.raises(ValueError, match="lifetime L = 0 is refused"):
        apply(LifetimeTerm(0), LifetimeStart(0, False))
    with pytest.raises(ValueError, match="age -1 is refused"):
        apply(term, LifetimeStart(-1, False))


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_a_records_of_a_family_with_a_lifetime_end_on_the_border_at_age_l_through_the_loop():
    """The emitter's unit world with the light family's lifetime L = 10 (set on the parsed world until the loader reads the key): the two records given end on the border `lifetime` at their giving's interval + L, each a click line there with its giving named, the record deleted whole; no record reaches the screen; without a lifetime the border is not made."""
    document = emitter_world(stock=2, ticks=120)
    stamped(document)
    world, lifetime = parse_nature_beam_world(document), 10
    world = replace(world, families=(replace(world.families[0], lifetime=lifetime), *world.families[1:]))
    simulation = DetectorLawSimulation(world)
    assert simulation.detector_names[simulation.lifetime_detector] == "lifetime"
    lines: list[dict] = []
    simulation.record = lines.append
    for _ in range(120):
        simulation.step()
    gathers = [line for line in lines if line["event"] == "gather"]
    ages = [(line["tick"] - line["giving"], line["chosen"]) for line in gathers]  # each at its age L
    assert ages == [(lifetime, [["lifetime", 0, "0"]])] * 2
    assert all(line["record"] not in simulation.records for line in gathers)
    assert DetectorLawSimulation(parse_nature_beam_world(document)).lifetime_detector is None
