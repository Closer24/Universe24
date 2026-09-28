"""The self-source's folder: each difference Rule3's read act, its square a booking, the sum divided by P_2; on the shipped moving Lorentz world the folder's line is the loop's arithmetic at every interval, forward and backward, bit for bit."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.register import folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.self_source import (
    DECLARATION,
    OwnLevel,
    SelfSourceStart,
    SelfSourceTerm,
    apply,
    difference,
)
from event_universe.world_files import input_digest, parse_world_document, world_files

ROOT = Path(__file__).resolve().parents[1]
TOWARD = (
    ROOT / "tests"
)  # the rule tests' own small worlds (the shipped worlds left with the worlds' replay)


def moving_world_with_the_self_source(family_name: str) -> tuple[DetectorLawSimulation, int, int]:
    """The moving Lorentz world with the named family's self-source unit set to 24 A in its universe file, A lowered to 2^16 so that the well's edge reaches the unit; the loop's simulation, the family's index and the unit."""
    document = json.loads((TOWARD / "lorentz_moving.json").read_text(encoding="utf-8"))
    files = world_files(document)
    universe = copy.deepcopy(files[document["universe"]])
    universe["integers"]["amplitude_bound"] = (
        1 << 16
    )  # the records stay within it over the test; the unit then reachable
    unit = 24 * int(universe["integers"]["amplitude_bound"])
    index = next(i for i, entry in enumerate(universe["families"]) if entry["name"] == family_name)
    universe["families"][index]["self_source"] = {"unit": unit}  # the file derives it as 0; set here
    files[document["universe"]] = universe
    world = parse_world_document(document, files, input_digest(document))
    return DetectorLawSimulation(world), index, unit


def test_the_shipped_universe_has_the_line_off_and_the_difference_is_the_read_act():
    document = json.loads((TOWARD / "lorentz_moving.json").read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(
        parse_world_document(document, world_files(document), input_digest(document))
    )
    live = next(iter(simulation.records.values()))
    assert (
        simulation.families[live.family].self_unit == 0 and simulation._self_source(live, False) is None
    )
    here, arrived = np.array([5, -3, 0]), np.array([-2, 7, 4])
    assert np.array_equal(difference(here, arrived), arrived - here)


def test_the_refusals_name_the_unit_the_links_and_the_bound():
    level = np.zeros((1, 1, 1), dtype=np.int64)
    own = OwnLevel(level, (level,) * 6)
    with pytest.raises(ValueError, match="P_2 is 0"):
        apply(SelfSourceTerm(0, 1), SelfSourceStart((own,)))
    with pytest.raises(ValueError, match="carries 5 Links"):
        apply(SelfSourceTerm(24, 1), SelfSourceStart((OwnLevel(level, (level,) * 5),)))
    with pytest.raises(ValueError, match="beyond int64"):
        apply(SelfSourceTerm(1 << 40, 1 << 30), SelfSourceStart((own,)))
    assert apply(SelfSourceTerm(1 << 40, 1 << 20), SelfSourceStart((own,)), None).total == 0


def test_the_declaration_is_the_registers_row():
    assert DECLARATION.name == "the self-source" and folder_of(DECLARATION.name) == "self_source"
    assert DECLARATION.place == "(i)" and DECLARATION.word == "the right side"
    assert DECLARATION.function is apply and DECLARATION.writes == ("a family's level at a Node",)
    simulation, family, _ = moving_world_with_the_self_source("charge")
    registered = simulation.register.declarations["the self-source"]
    assert registered.binder is None and registered.function is apply
