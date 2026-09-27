"""The hand's folder (ALGEBRA.md #the-primitives, the row "the hand"): S . n as a booking, its sign against the declared hand, the refusal by name."""

from __future__ import annotations

import pytest

from event_universe.core.register import discover, folder_of
from event_universe.features.hand import DECLARATION, THE_WORD, HandStart, HandTerm, apply, booking


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
