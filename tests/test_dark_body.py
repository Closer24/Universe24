"""The dark body row, built and not run against its pins: the dark body of content M beside a beam's
line and its bright control, their files the generator's and their pins declared blind."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "examples/events/dark_body"
DARK_NUMBER = 1  # the body's measured index in both worlds


def load(name: str) -> dict:
    return json.loads((FOLDER / f"{name}.json").read_text(encoding="utf-8"))


def test_the_files_are_the_generators_and_the_pins_are_declared_blind():
    """(i) Both worlds load under their input stamp (the generator's, the loader's check); the expectations file declares every pin with its kind (DETECTOR) and the bend's band from the ray's COMPUTATION, positive toward the body, before any run."""
    for name in ("dark", "bright"):
        document = load(name)
        assert document["universe"] == "examples/events/universe.json"  # item 59
        world = parse_nature_beam_world(document)
        assert world.node_clock == 10_000
        # the three families of ALGEBRA.md #the-primitives (the one stroke, commit 1)
        assert [family.name for family in world.families] == ["gravity", "charge", "matter"]
        assert [family.parts for family in world.families] == [(1, 3, 6), (1, 3), (1,)]
        assert all(family.charge == (0, 1) for family in world.families)
    pins = json.loads((FOLDER / "expectations.json").read_text(encoding="utf-8"))
    assert "before any run" in pins["declared"]
    for pin in pins["pins"].values():
        assert pin["kind"] == "DETECTOR"
    bend = pins["pins"]["bend_links"]
    assert 5.0 < bend["value"] < 120.0 and bend["band"][0] < bend["value"] < bend["band"][1]
    assert pins["pins"]["dark_far_count_equals_stock"]["value"] == 30


def test_the_dark_body_is_dark_by_declaration_and_the_bright_one_is_not():
    """The dark body has charge 0, no emitter and no detector set; the bright one gives light and is read."""
    dark, bright = load("dark"), load("bright")
    for document in (dark, bright):
        body = document["measured"][DARK_NUMBER]
        assert body["position"] == [184, 143, 0] and body["extents"] == [32, 5, 1]
    # the level 4812 at both bodies' Nodes; the bright body's split into its own quanta and
    # its stock of light held (item 47)
    assert dark["measured"][DARK_NUMBER]["amount"] == 4812
    assert bright["measured"][DARK_NUMBER]["amount"] == 4812 - 128
    # light is the charge family's wave (ALGEBRA.md #the-primitives): the stock and the giving are its
    assert bright["measured"][DARK_NUMBER]["stocks"] == {"charge": 128}
    # the dark body is dark by declaration, one family of matter (ALGEBRA.md #the-primitives), no emitter
    assert dark["measured"][DARK_NUMBER]["family"] == "matter"
    assert dark["measured"][DARK_NUMBER]["kind"] == [800, 809]
    assert "emitter" not in dark["measured"][DARK_NUMBER]
    assert all("block" not in detector for detector in dark["detectors"])
    assert bright["measured"][DARK_NUMBER]["family"] == "matter"
    assert bright["measured"][DARK_NUMBER]["emitter"]["family"] == "charge"
    assert {"name": "at_body", "block": DARK_NUMBER} in bright["detectors"]
    assert bright["measured"][0]["emitter"]["receiver"][0] == "at_body"
    assert "at_body" not in dark["measured"][0]["emitter"]["receiver"]


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_both_worlds_run_balanced_and_the_dark_body_never_clicks():
    """80 intervals each: books balanced, the sign family exactly zero, and no click of the dark world names the dark body."""
    lines: dict[str, list[dict]] = {}
    for name in ("dark", "bright"):
        lines[name] = []
        simulation = DetectorLawSimulation(
            parse_nature_beam_world(load(name)), observer=lines[name].append
        )
        for interval in range(80):
            simulation.step()
            if interval % 20 == 19:
                assert simulation.books()["balanced"], (name, simulation.tick)
        assert (
            not simulation.held_record("sign").now.any()
            and not simulation.held_record("sign").remainder.any()
        )
    # the dark body's own rotation cycles on (its `click` and `block` lines are the GameBoard's
    # count of its own record, ALGEBRA.md #the-postulates); no giving click and no taking click name it
    assert not [
        line
        for line in lines["dark"]
        if line.get("measured") == DARK_NUMBER and line["event"] in ("giving", "gather")
    ]
    assert not [
        line
        for line in lines["dark"]
        if line["event"] == "gather" and line["chosen"] and line["chosen"][0][0] == "at_body"
    ]
    for name in ("dark", "bright"):
        givings = [line for line in lines[name] if line["event"] == "giving" and line["measured"] == 0]
        assert givings, name
