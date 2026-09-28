"""THE START, its own folder (ALGEBRA.md #the-generator, the (g) row's THE START): every held family's rest at the load by one folder found by its name, on a chain in one pass in integers, elsewhere the clamp iterated; the generator reads the clamp from the folder."""

from __future__ import annotations

import numpy as np

from event_universe.core.register import discover
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.start import arrivals, chain_rest, field_at_rest, rest
from event_universe.world_files import parse_nature_beam_world
from tests.running import stamped
from tests.worlds import emitter_world


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


def test_a_box_takes_the_certified_rest_the_clamps_levels_and_a_half_rounded_up_and_no_body_is_refused():
    """A box is no chain: `rest` takes the line's certified rest there, in a few rounds against the clamp's steps, the clamp's levels bit for bit where no value sits at a half; at a half (the two columns fixed under the torus's reflection that swaps two bodies of counts 1 and 4 read 2.5 exactly) the division act rounds up where the clamp's fixed point, below the line by the floors' deficit, rounds down; counts without a body are refused by name."""
    box = np.zeros((5, 5, 5), dtype=np.int64)
    box[1:3, 1:3, 1:3] = 7
    found, clamped = rest(box, (1, 4), (True, True, True)), field_at_rest(box, (1, 4))
    assert 1 <= found.iterations < clamped.iterations and (found.levels == clamped.levels).all()
    torus = np.zeros((20, 10, 1), dtype=np.int64)
    torus[5, 0, 0], torus[15, 0, 0] = 1, 4
    found, clamped = rest(torus, (1, 1), (True, True, True)), field_at_rest(torus, (1, 1))
    halves = np.zeros(torus.shape, dtype=bool)
    halves[0], halves[10] = True, True
    assert (found.levels[halves] == 3).all() and (clamped.levels[halves] == 2).all()
    assert (found.levels[~halves] == clamped.levels[~halves]).all()
    try:
        rest(np.zeros((9, 1, 1), dtype=np.int64), (1, 1), (True, True, True))
    except ValueError as refusal:
        assert "no body" in str(refusal)
    else:
        raise AssertionError("counts with no body were not refused")


def test_the_loop_starts_every_held_family_at_its_rest_at_the_load():
    """THE START in the loop (ALGEBRA.md #the-generator, THE START): at the load, after the held records and the hold's first write, every held family's time part is the folder's rest on the counts the hold wrote at the bodies' Nodes, at both levels with the remainder 0, before the first interval; a family no body holds stays at 0."""
    document = emitter_world(stock=1, ticks=2)
    for entry in document["universe"]:
        if "held" in entry:
            entry["held"] = {**entry["held"], "divisor": 1}  # a copy: the sources' loads are the counts
    simulation = DetectorLawSimulation(parse_nature_beam_world(stamped(document)))
    started = 0
    for family, record in simulation.held_records.items():
        definition = simulation.families[family]
        counts = np.zeros(simulation.shape, dtype=np.int64)
        for number in range(len(simulation.held)):  # every body's Nodes, a block's or a span's
            block = simulation.block_by_number.get(number)
            mask = block.mask if block is not None else simulation.span_masks[number]
            counts[mask] = simulation.body_source(number, definition.held) // definition.held_divisor
        if not counts.any():
            assert not record.now.any() and not record.before.any()
            continue
        expected = rest(counts, definition.pair, simulation.kind_wrap[family]).levels
        assert np.array_equal(record.now, expected) and np.array_equal(record.before, expected)
        assert not record.remainder.any() and simulation.node_level[family] is record.now
        assert (expected != 0).sum() > (counts != 0).sum()  # the field reaches beyond the bodies
        started += 1
    assert started >= 1


def test_the_sources_rest_solves_the_sums_line_on_a_chain_and_on_a_box_alike():
    """THE START ON THE SUM'S SOURCES (ALGEBRA.md #the-generator, THE START; the hold's row as a sum): the rest solves 6 den a - num S_6(a) = 3 den sigma, sigma the weighted count over the divisor at the bodies' Nodes, 0 beyond an open face, no Node clamped; the certified values' exact residual stays below one fine unit, on a chain and on a box alike; a board periodic on its every axis at [1, 1] has no rest and is refused by name; a divisor below 1 is refused."""
    numerators, divisor, wrap = chain(), 7, (False, True, True)
    box = np.zeros((6, 5, 4), dtype=np.int64)
    box[1:3, 1:3, 1] = 9
    for counts, faces, pair in (
        (numerators, wrap, (1, 1)),
        (numerators, wrap, (1, 4)),
        (box, (False, True, True), (1, 1)),
        (box, (True, True, True), (3, 4)),
    ):
        num, den = pair
        found = rest(counts, pair, faces, divisor)
        fine = found.fine.astype(object)
        neighbours = sum(arrivals(fine, faces))  # the six Ports' reads, 0 beyond an open face
        side = counts.astype(object) * (3 * den * found.unit) // divisor
        left = 6 * den * fine - num * neighbours - side
        assert (np.abs(left) < found.unit).all(), (pair, faces)
        assert (found.levels[counts > 0] > 0).all() and (found.levels >= 0).all()
    for bad, message in (
        ((numerators, (True, True, True), 7), "no sink"),
        ((numerators, wrap, 0), "divisor from 1"),
    ):
        try:
            rest(bad[0], (1, 1), bad[1], bad[2])
        except ValueError as refusal:
            assert message in str(refusal)
        else:
            raise AssertionError(f"not refused: {message}")


def test_the_falls_tent_is_the_sums_rest_on_the_open_chain():
    """The fall's chain (400 open on x) with the heavy body alone, 30 Nodes of 3,600 at x = 185..214 over the divisor 40,000 at [1, 1]: the rest is a tent, linear outside the body with the slope half the source total 3 sigma x 30 / 2 (the body centred, the two sides equal), the second difference -3 sigma inside; the closed form a_i = (i + 1) s up to the body's edge and a_i = a_185 + s m - (3 sigma / 2) m (m + 1) inside (m = i - 185) gives 753.3 at the edge and 781.65 at the centre, and the levels are its nearest integers (the certificate's claim); the tent is symmetric about the body."""
    from fractions import Fraction

    numerators = np.zeros((400, 1, 1), dtype=np.int64)
    numerators[185:215, 0, 0] = 3600
    divisor = 40000
    found = rest(numerators, (1, 1), (False, True, True), divisor)
    sigma = Fraction(3600, divisor)
    slope = 3 * 30 * sigma / 2

    def exact(i: int) -> Fraction:
        if i <= 185:
            return (i + 1) * slope
        if i >= 214:
            return (400 - i) * slope
        m = i - 185
        return 186 * slope + slope * m - (3 * sigma / 2) * m * (m + 1)

    assert exact(185) == Fraction(7533, 10) and exact(199) == Fraction(78165, 100)
    levels = found.levels[:, 0, 0]
    for i in (0, 100, 184, 185, 186, 199, 200, 214, 215, 286, 399):
        assert exact(i) - int(exact(i)) != Fraction(1, 2) and int(levels[i]) == round(exact(i)), i
    assert int(levels[185]) == 753 and int(levels[199]) == 782 and int(levels[199]) == int(levels[200])
    assert (levels == levels[::-1]).all() and int(levels[0]) == 4
