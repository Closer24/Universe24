"""THE START, its own folder (ALGEBRA.md #the-generator, the (g) row's THE START): every held family's rest at the load by one folder found by its name, on a chain in one pass in integers, elsewhere the clamp iterated; the generator reads the clamp from the folder."""

from __future__ import annotations

import numpy as np

from event_universe.core.register import discover
from event_universe.features.start import chain_rest, field_at_rest, rest


def chain(extent: int = 40) -> np.ndarray:
    counts = np.zeros((extent, 1, 1), dtype=np.int64)
    counts[10:13, 0, 0] = 30
    counts[25, 0, 0] = 12
    return counts


def test_the_card_is_built_at_the_place_any_and_walked_by_nothing():
    """The folder's card: "the start", the place and the word any, the function the rest; the loop's walk calls it for no term of the files."""
    declaration = discover().declarations["the start"]
    assert (declaration.function, declaration.place, declaration.word) == (rest, "any", "any")


def test_the_chains_one_pass_is_the_clamps_fixed_point_on_every_face_kind_and_pair():
    """On a chain the one pass (the tridiagonal line in exact rationals, the levels by the division act) gives the clamp's fixed point: bit for bit on [1, 1] and [3, 4] between open and periodic faces, in one iteration against thousands."""
    for wrap, pair in (
        ((False, True, True), (1, 1)),
        ((True, True, True), (1, 1)),
        ((False, True, True), (1, 4)),
        ((True, True, True), (3, 4)),
    ):
        passed, clamped = chain_rest(chain(), pair, wrap), field_at_rest(chain(), pair, wrap)
        assert (passed.levels == clamped.levels).all() and passed.unit == clamped.unit
        assert passed.iterations == 1 and clamped.iterations > passed.iterations
        assert rest(chain(), pair, wrap).iterations == 1


def test_a_box_goes_through_the_clamp_and_a_chain_with_no_body_is_refused():
    """A box is no chain: `rest` iterates the clamp there (the tool's field at rest, the same object); counts without a body are refused by name."""
    box = np.zeros((5, 5, 5), dtype=np.int64)
    box[1:3, 1:3, 1:3] = 7
    found = rest(box, (1, 4), (True, True, True))
    assert found.iterations > 1 and (found.levels == field_at_rest(box, (1, 4)).levels).all()
    try:
        rest(np.zeros((9, 1, 1), dtype=np.int64), (1, 1), (True, True, True))
    except ValueError as refusal:
        assert "no body" in str(refusal)
    else:
        raise AssertionError("counts with no body were not refused")
