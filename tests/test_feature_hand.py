"""The hand's folder (ALGEBRA.md #the-primitives, the row "the hand"): S . n as a booking, its sign against the declared hand, the refusal by name."""

from __future__ import annotations

import copy
import json
from dataclasses import replace

import pytest

from event_universe.core.register import discover, folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.hand import DECLARATION, THE_WORD, HandStart, HandTerm, apply, booking
from event_universe.world_files import parse_nature_beam_world
from tests.running import ROOT

LIGHT_CLOCK = ROOT / "examples" / "events" / "massive_record" / "light_clock.json"


def test_the_declaration_is_the_ledgers_row_and_the_register_finds_it_built():
    assert DECLARATION.name == "the hand" and folder_of(DECLARATION.name) == "hand"
    assert DECLARATION.place == "(ii)" and DECLARATION.word == "after the step"
    assert DECLARATION.reads == ("a body's spin S", "a body's momentum n", "the declared hand")
    assert DECLARATION.writes == ()  # a check writes nothing
    assert THE_WORD in DECLARATION.section and DECLARATION.function is apply
    registered = discover().declarations["the hand"]
    assert registered.built and registered.function is apply


def test_the_booking_is_s_dot_n_and_the_opposite_sign_alone_refuses():
    """S . n over the three axes exactly; the click is refused where its sign is opposite to the declared hand, admitted where it agrees or is 0 (a body with no spin or no momentum); a hand of 0 or 2 is refused by name."""
    spin, momentum = (2, -3, 4), (5, 1, -2)
    assert booking(spin, momentum) == 10 - 3 - 8 == -1
    right, left = HandTerm(1), HandTerm(-1)
    assert (
        not apply(right, HandStart(spin, momentum)).admitted
        and apply(left, HandStart(spin, momentum)).admitted
    )
    assert apply(right, HandStart(spin, momentum)).booking == -1
    assert (
        apply(right, HandStart((0, 0, 0), momentum)).admitted
        and apply(left, HandStart(spin, (0, 0, 0))).admitted
    )
    assert (
        apply(right, HandStart((1, 0, 0), (7, 0, 0))).admitted
        and not apply(left, HandStart((1, 0, 0), (7, 0, 0))).admitted
    )
    for hand in (0, 2):
        with pytest.raises(ValueError, match=f"declared hand {hand} is refused"):
            apply(HandTerm(hand), HandStart(spin, momentum))


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_the_hand_refuses_a_click_at_the_giver_and_the_ladder_walks_on_to_the_face():
    """The shipped light clock over 700 intervals with A's spin S = (1, 0, 0) and the charge family's hand set on the parsed world: the booking S . n is read from the run itself as each click is booked (S and n of A at the click, the row of the hand, ALGEBRA.md #the-primitives), and every click at A's own set is one the declared hand admits (sign(S . n) x hand never -1); a click the hand refuses walks the ladder on to the face, so every record ends at `at_well` or at the face, and the two hands part the run's clicks: the records clicking at `at_well` under -1 and under +1 are not the same set."""
    document = json.loads(LIGHT_CLOCK.read_bytes())
    at_well: dict[int, set[int]] = {}
    for hand in (-1, 1):
        world = parse_nature_beam_world(copy.deepcopy(document))
        families = list(world.families)
        families[1] = replace(families[1], hand=hand)
        simulation = DetectorLawSimulation(replace(world, families=tuple(families)))
        body = simulation.blocks[0]
        body.spin, body.spin_before = [1, 0, 0], [1, 0, 0]
        lines: list[dict] = []
        simulation.record = lambda line, b=body, out=lines: out.append(
            {**line, "booking": (tuple(b.spin), tuple(b.momentum))}
        )
        for _ in range(700):
            simulation.step()
        gathers = [line for line in lines if line["event"] == "gather"]
        assert gathers and {line["chosen"][0][0] for line in gathers} <= {"at_well", "face"}
        for line in gathers:
            admitted = apply(HandTerm(hand), HandStart(*line["booking"])).admitted
            assert line["chosen"][0][0] == "face" or admitted
        at_well[hand] = {line["record"] for line in gathers if line["chosen"][0][0] == "at_well"}
    assert at_well[-1] != at_well[1]
