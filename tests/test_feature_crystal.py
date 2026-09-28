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


def test_the_crystal_with_a_flat_seed_is_refused_by_name_and_the_terms_refusals_hold():
    """Bell's world at the load: the crystal is a block of two Nodes whose seed is the flat scalar 2^12 and no mode record, refused by name (the old seed fallback left; a block gives from its own record, which comes from its mode record alone). Bell's run, the emitter's click at the crystal's set and the pair's two labels clicking alone at the polarisers' own sets, returns with the crystal's mode from the generator in the law's form. The term's refusals by name hold on a silent crystal (the seed 0, no own record): a crystal on a body with an emitter, a world with one polariser body."""
    with pytest.raises(
        ValueError, match=r"measured\[5\] needs its `seed` as its composed mode's profile"
    ):
        DetectorLawSimulation(parse_nature_beam_world(bell_world()))
    silent = bell_world()
    silent["measured"][CRYSTAL]["seed"] = 0
    silent["stamp"] = input_stamp(silent)
    simulation = DetectorLawSimulation(parse_nature_beam_world(silent))
    simulation.crystals = {CRYSTAL: CrystalTerm()}
    assert ("measured[5].crystal", "the crystal") in simulation.family_terms()
    simulation.crystals = {EMITTER: CrystalTerm()}
    with pytest.raises(ValueError, match="declares nothing else"):
        simulation.family_terms()
    one_sided = bell_world()
    one_sided["measured"][CRYSTAL]["seed"] = 0
    del one_sided["measured"][RIGHT]["polariser"]
    one_sided["stamp"] = input_stamp(one_sided)
    simulation = DetectorLawSimulation(parse_nature_beam_world(one_sided))
    simulation.crystals = {CRYSTAL: CrystalTerm()}
    with pytest.raises(ValueError, match="needs two polariser bodies"):
        simulation.family_terms()
