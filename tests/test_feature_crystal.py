"""THE CRYSTAL and THE PAIR RECORD (ALGEBRA.md #the-primitives, the row "the crystal"; #the-ladder, THE PAIR RECORD, THE LABELS' CLICKS and THE HALF QUANTUM): a body with the key `crystal` gives one record of rank 2 at the click of an arriving record on its set, at the arriving norm over twice its denominator with two identical labels, and each label clicks alone at its own side by its own ladder, the first click making the record rank 1 everywhere at once."""

from __future__ import annotations

import copy

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
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.worlds import emitter_world, receiver_cube

EMITTER, LEFT, CRYSTAL, RIGHT = 0, 4, 5, 6  # the bodies' numbers in the Bell world below


def bell_world(right: dict | None = None) -> dict:
    """Bell's world on the emitter's unit world (a chain of 80, x closed): the emitter's one giving of light aimed at the crystal's set; a polariser body in the law's form at 44 with its own set `left_own` and its far set `left_far` (a cube at 40), the crystal a block of two Nodes at 50 with its own set (its term set on the loop after the load: a block gives from its own record, which the law's form has only with a mode file), a polariser at 58 with `right_own` and `right_far` (a cube at 64); the crystal's term is set after the load."""
    document = emitter_world(stock=1, ticks=400)
    document["measured"][EMITTER]["emitter"]["receiver"] = ["crystal_set"]

    def polariser(x: int, card: dict) -> dict:
        nodes = [{"node": [x, 0, 0], "count": 1}]
        return {
            "family": "matter",
            "nodes": nodes,
            "momentum": [0, 0, 0],
            "momentum_before": [0, 0, 0],
            "polariser": card,
        }

    crystal = copy.deepcopy(document["measured"][EMITTER])
    crystal.pop("emitter")
    crystal.pop("clock", None)
    crystal.update(stocks={}, position=[50, 0, 0], extents=[2, 1, 1], seed=1 << 12)
    document["measured"].append(polariser(44, {"angle": [2, 1], "sets": ["left_far", "left_own"]}))
    document["measured"].append(crystal)
    document["measured"].append(
        polariser(58, right or {"angle": [1, 0], "sets": ["right_far", "right_own"]})
    )
    document["detectors"].extend(
        [
            {"name": "left_own", "positions": [[44, 0, 0]]},
            {"name": "crystal_set", "block": CRYSTAL},
            {"name": "right_own", "positions": [[58, 0, 0]]},
        ]
    )
    receiver_cube(document, "left_far", [40, 0, 0])
    receiver_cube(document, "right_far", [64, 0, 0])
    document["stamp"] = input_stamp(document)
    return document


def test_the_card_is_built_at_ii_and_the_pair_is_declared_at_the_half_quantum():
    """The card: "the crystal" at (ii) after the step, the function `apply`, the body's key `crystal` (an empty object, declaring nothing) through the cards, no write of its own (the giving's act writes for it); `apply` declares the pair's two labels, the arriving record's twice, its norm over twice the denominator (THE HALF QUANTUM) and its clock at half the arriving rotation ([p, 2 q]); a norm or a clock below 1 is refused by name; a body with no key gives nothing."""
    assert DECLARATION.name == "the crystal" and folder_of(DECLARATION.name) == "crystal"
    assert (DECLARATION.place, DECLARATION.word, DECLARATION.writes) == ("(ii)", "after the step", ())
    registered = discover().declarations["the crystal"]
    assert registered.built and registered.function is apply
    assert registered.schema is not None and "crystal" in registered.schema.places["a body"].keys
    writes = apply(CrystalTerm(), CrystalStart(7, 3, (0, 1), (512, 1)), CrystalOwn())
    assert (writes.labels, writes.norm, writes.denominator, writes.clock) == (
        ((0, 1), (0, 1)),
        7,
        6,
        (512, 2),
    )
    with pytest.raises(ValueError, match="clock is a pair of integers from 1"):
        apply(CrystalTerm(), CrystalStart(7, 3, (0, 1), (0, 1)), CrystalOwn())
    with pytest.raises(ValueError, match="norm is from 1"):
        apply(CrystalTerm(), CrystalStart(0, 3, (0, 1), (512, 1)), CrystalOwn())
    assert read_term({"family": "matter"}) is None and read_term({"crystal": {}}) == CrystalTerm()


def test_the_crystal_gives_the_pair_at_the_click_and_each_label_clicks_alone_at_its_side():
    """The loop on Bell's world, the main loop's audit admitting every act: the emitter's record clicks at the crystal's set and in the same interval the crystal gives the pair through the giving's open and window, named at the window's close (after the click, the intervals in this order and never the run's numbers) with the two identical labels, the arriving norm over twice its denominator and a residue of its own (the crystal's, read at its Node); the rows' label clicks alone at the left polariser's own set on the first row's line with the pair's one quantum, the columns' label alone at the right polariser's own set on the second row's line with the arriving record's residue (the second residue of the crystal's Node) and the content 0 (the half in the family's unit), whichever first; after the second click no row is alive. The refusals by name: a crystal on a body with an emitter, a world with one polariser body."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(bell_world()))
    simulation.crystals = {CRYSTAL: CrystalTerm()}
    assert ("measured[5].crystal", "the crystal") in simulation.family_terms()
    lines: list[dict] = []
    simulation.record = lines.append
    for _ in range(400):
        simulation.step()
    givings = [line for line in lines if line["event"] == "giving"]
    gathers = [line for line in lines if line["event"] == "gather"]
    arriving, pair = givings
    assert [(line["measured"], line["labels"]) for line in givings] == [
        (EMITTER, [[0, 1]]),
        (CRYSTAL, [[0, 1], [0, 1]]),
    ]
    assert (pair["norm"], pair["pace"]) == (arriving["norm"], 2 * arriving["pace"])
    assert pair["u"] != arriving["u"]  # the crystal's own residue, read at its Node
    assert [(g["record"], g["chosen"][0][0], g["u"], g["content"]) for g in gathers] == [
        (arriving["record"], "crystal_set", arriving["u"], 1),
        (pair["record"], "left_own", pair["u"], 1),
        (pair["record"] + 1, "right_own", arriving["u"], 0),
    ]
    ticks = [arriving["tick"], gathers[0]["tick"], pair["tick"], gathers[1]["tick"], gathers[2]["tick"]]
    assert (
        ticks == sorted(ticks) and ticks[0] < ticks[1] < ticks[2] < ticks[3]
    )  # the order, not the run's numbers
    assert not [live for live in simulation.records.values() if live.pair_record is not None]
    simulation.crystals = {EMITTER: CrystalTerm()}
    with pytest.raises(ValueError, match="declares nothing else"):
        simulation.family_terms()
    one_sided = bell_world()
    del one_sided["measured"][RIGHT]["polariser"]
    one_sided["stamp"] = input_stamp(one_sided)
    simulation = DetectorLawSimulation(parse_nature_beam_world(one_sided))
    simulation.crystals = {CRYSTAL: CrystalTerm()}
    with pytest.raises(ValueError, match="needs two polariser bodies"):
        simulation.family_terms()
