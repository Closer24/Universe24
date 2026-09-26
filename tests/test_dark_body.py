"""THE DARK BODY ROW, BUILT AND NOT RUN AGAINST ITS PINS (ALGEBRA.md 9.54 (4); the model owner's
word of 2026-09-25 through the Boss, record 2015: "yes" to building it now, the run only after
he says the engine is stable; BUILD.md section 26 item 39). The two worlds of
examples/events/dark_body (the dark body of content M standing 45 Links beside a beam's line,
and the bright control of the same M in a body of the light clock's family with its giving and
taking clicks) and their expectations, declared blind from the algebra. The suite reads what
needs no run against the pins: (i) the files are the generator's under the stamp and the pins
are declared with their kinds; (ii) the dark body is dark by declaration: every family's charge
0, no emitter on it, no detector set names its Nodes; the bright body has both; (iii) over 80
intervals of each world the books balance, the family of charge is 0 everywhere, the family
of clicks' level beside the two bodies is the same in both worlds within the rounding, no giving click
    and no taking click of the dark world names the dark body, and the emitter's giving clicks have begun (GAMEBOARD
readings, COMPUTATION; no pin read)."""

from __future__ import annotations

import json
from pathlib import Path

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "examples/events/dark_body"
DARK_NUMBER = 1  # the body's measured index in both worlds
BEAM_Y = 100
BODY_CENTRE = (200, 145, 0)


def load(name: str) -> dict:
    return json.loads((FOLDER / f"{name}.json").read_text(encoding="utf-8"))


def test_the_files_are_the_generators_and_the_pins_are_declared_blind():
    """(i) Both worlds load under their input stamp (the generator's, the loader's check); the
    expectations file declares every pin with its kind (DETECTOR) and the bend's band from the
    ray's COMPUTATION, positive toward the body, before any run."""
    for name in ("dark", "bright"):
        document = load(name)
        assert document["universe"] == "examples/events/universe.json"  # item 59
        world = parse_nature_beam_world(document)
        assert world.node_clock == 10_000 and world.body_record is False
        # the three families of ALGEBRA.md 9.86 (2) (the one stroke, commit 1)
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
    """(ii) The dark body: a block of the family `dark` (charge 0), no emitter, on no detector
    set; the bright body: the same place and content in the family `matter`, an emitter of
    light and the set `at_body` bound to its Nodes; the emitter's ladder names the body's set
    first in the bright world and not at all in the dark one."""
    dark, bright = load("dark"), load("bright")
    for document in (dark, bright):
        body = document["measured"][DARK_NUMBER]
        assert body["position"] == [184, 143, 0] and body["extents"] == [32, 5, 1]
    # the level 4812 at both bodies' Nodes; the bright body's split into its own quanta and
    # its stock of light held (item 47)
    assert dark["measured"][DARK_NUMBER]["amount"] == 4812
    assert bright["measured"][DARK_NUMBER]["amount"] == 4812 - 128
    # light is the charge family's wave (9.86 (2) (b)): the stock and the giving are its
    assert bright["measured"][DARK_NUMBER]["stocks"] == {"charge": 128}
    # the dark body is dark by declaration, one family of matter (9.86 (2) (c)), no emitter
    assert dark["measured"][DARK_NUMBER]["family"] == "matter"
    assert dark["measured"][DARK_NUMBER]["kind"] == [800, 809]
    assert "emitter" not in dark["measured"][DARK_NUMBER]
    assert all("block" not in detector for detector in dark["detectors"])
    assert bright["measured"][DARK_NUMBER]["family"] == "matter"
    assert bright["measured"][DARK_NUMBER]["emitter"]["family"] == "charge"
    assert {"name": "at_body", "block": DARK_NUMBER} in bright["detectors"]
    assert bright["measured"][0]["emitter"]["receiver"][0] == "at_body"
    assert "at_body" not in dark["measured"][0]["emitter"]["receiver"]


def test_both_worlds_run_with_the_same_field_beside_the_body_and_the_dark_body_never_clicks():
    """(iii) 80 intervals of each world: the books balanced every 20 intervals; the family of
    charge 0 everywhere (every family's charge 0); the family of clicks' level at the Nodes 10
    Links outside the body's four faces equal in the two worlds within one percent (the same
    held content at the same Nodes, the bright body's lower by its giving clicks so far); no giving click and no taking click of the dark world
    names the dark body (its own rotation's cycle lines are the GameBoard's); the emitter's first giving click has happened in both."""
    simulations = {}
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
        simulations[name] = simulation
    # ten Links outside the slab's four faces (the slab [184, 216) x [143, 148)) and beside
    # the beam's line; the bright body's content is lower by its giving clicks so far (a few
    # quanta of 100000), so the levels agree within one percent
    beside = [(226, 145, 0), (173, 145, 0), (200, 158, 0), (200, 132, 0), (200, 125, 0)]
    for node in beside:
        dark_level = int(simulations["dark"].level_of("content")[node])
        bright_level = int(simulations["bright"].level_of("content")[node])
        assert abs(dark_level - bright_level) <= max(10, abs(dark_level) // 100), (
            node,
            dark_level,
            bright_level,
        )
    assert int(simulations["dark"].level_of("content")[BODY_CENTRE]) == 4812
    # the dark body's own rotation cycles on (its `click` and `block` lines are the GameBoard's
    # count of its own record, 9.54 (3)); no giving click and no taking click name it
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
