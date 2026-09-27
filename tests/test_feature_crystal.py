"""THE CRYSTAL's draft folder and hook (docs/HIGHLIGHTS.md "Where a tensor enters"; the law's row to come): a body with the key `crystal` gives one record of rank 2 with two identical labels at the click of an arriving record on its set, its norm the taken quantum's by conservation and its clock the crystal's; the joint click at the two ends waits on the row."""

from __future__ import annotations

import copy
import json

import pytest

from event_universe.core.register import discover, folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.crystal import (
    DECLARATION,
    CrystalOwn,
    CrystalStart,
    CrystalTerm,
    apply,
    read_term,
)
from event_universe.world_files import parse_nature_beam_world
from tests.worlds import ROOT

LIGHT_CLOCK = ROOT / "examples" / "events" / "massive_record" / "light_clock.json"


def test_the_card_is_built_at_ii_and_the_pair_is_declared_from_the_taken_quantum():
    """The card: "the crystal" at (ii) after the step, the function `apply`, the body's key `crystal` with its label through the cards, no write of its own (the giving's act writes for it); `apply` declares the pair's two identical labels, the taken norm whole and the crystal's clock; a clock or a norm below 1 is refused by name; a body with no key gives nothing and a crystal with no clock is refused."""
    assert DECLARATION.name == "the crystal" and folder_of(DECLARATION.name) == "crystal"
    assert (DECLARATION.place, DECLARATION.word, DECLARATION.writes) == ("(ii)", "after the step", ())
    registered = discover().declarations["the crystal"]
    assert registered.built and registered.function is apply
    assert registered.schema is not None and "crystal" in registered.schema.places["a body"].keys
    writes = apply(CrystalTerm((0, 1), (512, 1)), CrystalStart(7, 3), CrystalOwn())
    assert (writes.labels, writes.norm, writes.denominator, writes.clock) == (
        ((0, 1), (0, 1)),
        7,
        3,
        (512, 1),
    )
    with pytest.raises(ValueError, match="clock is a pair of integers from 1"):
        apply(CrystalTerm((0, 1), (0, 1)), CrystalStart(7, 3), CrystalOwn())
    with pytest.raises(ValueError, match="norm is from 1"):
        apply(CrystalTerm((0, 1), (512, 1)), CrystalStart(0, 3), CrystalOwn())
    assert read_term({"family": "matter"}, (512, 1)) is None
    assert read_term({"crystal": {"label": [0, 1]}}, (512, 1)) == CrystalTerm((0, 1), (512, 1))
    with pytest.raises(ValueError, match="declares its clock"):
        read_term({"crystal": {"label": [0, 1]}}, None)


def test_a_click_at_the_crystals_set_gives_one_pair_record_through_the_giving():
    """The hook on the shipped light clock with A as the crystal (the term set on the loop; the key through the loader needs a giving body in the law's form, the mode file's row): over 700 intervals every click at `at_well` is followed by one giving of a record whose two labels are the crystal's, its norm the clicked record's and its clock the crystal's [512, 1] (read on the pair records alive at the end), through the giving's own open (one quantum of the given family from A's stock), the loop's audit admitting the act; the run without the term gives no such record; measured once on this tree: 19 clicks and 12 pairs (the pairs given late in the run click after it ends, the plain run 15 clicks and none)."""
    document = json.loads(LIGHT_CLOCK.read_bytes())
    seen: dict[bool, tuple[int, int, set[tuple[int, int]]]] = {}
    for with_crystal in (False, True):
        simulation = DetectorLawSimulation(parse_nature_beam_world(copy.deepcopy(document)))
        if with_crystal:
            simulation.crystals = {0: CrystalTerm((0, 1), (512, 1))}
            assert ("measured[0].crystal", "the crystal") in simulation.family_terms()
        lines: list[dict] = []
        simulation.record = lines.append
        for _ in range(700):
            simulation.step()
        clicks = [
            line for line in lines if line["event"] == "gather" and line["chosen"][0][0] == "at_well"
        ]
        pairs = [
            line for line in lines if line["event"] == "giving" and line["labels"] == [[0, 1], [0, 1]]
        ]
        alive = {
            (live.period_numerator, live.period_denominator, live.lamp)
            for live in simulation.records.values()
            if live.labels == ((0, 1), (0, 1))
        }
        seen[with_crystal] = (len(clicks), len(pairs), alive)
    assert seen[False] == (15, 0, set()) and seen[True] == (19, 12, {(512, 1, 0)})
