"""The guide clause of the emission (ALGEBRA.md, The click writes on the lattice (5), BUILT 2026-10-22; src/event_universe/guide.py): a source in time lays S on the guide of width one, and on a wider cross-section the clause lays S / R, R the share of S that travels in the guide's transverse modes at the Node, every cosine the engine's own (`features/click.wave_cosine`), so one quantum travels; the box's numbers of the reader's derivation, the chain's identity bit for bit, and the width-one line standing where no mode travels, the near zone's lay."""

from event_universe import guide
from event_universe.features.click import wave_cosine

DEN = 6000
BOX, CHAIN = (61, 7, 7), (101, 1, 1)
CLOSED, CHAIN_FACES = (False, False, False), (False, True, True)
RESONANCE = (5414, 6000)


def test_every_cosine_is_the_engines_own_and_the_centres_weight_is_exact():
    assert [c for _, c, _, _ in guide.modes_of(DEN, 7, False, 3)] == [
        wave_cosine(m, 8, DEN) for m in range(1, 8)
    ]
    assert (
        wave_cosine(4, 8, DEN) == 0 and wave_cosine(8, 8, DEN) == -DEN
    )  # the quarter turn and pi, exact
    assert guide.modes_of(DEN, 7, False, 3)[0] == (
        1,
        5541,
        2 * DEN * DEN,
        8 * DEN * DEN,
    )  # c_1 and the weight 1 / 4 at the centre exactly
    assert guide.modes_of(DEN, 1, False, 0) == [(0, DEN, 1, 1)]  # one layer, the uniform mode


def test_the_box_has_one_travelling_mode_and_the_factor_of_the_reader():
    modes, numerator, denominator = guide.travelling(BOX, CLOSED, (51, 3, 3), RESONANCE)
    assert modes == [(1, 1)]
    assert 11.5 < denominator / numerator < 11.7  # 16 sin k_z / sin k = 11.6
    assert guide.guide_total(1000000, BOX, CLOSED, (51, 3, 3), RESONANCE) == 11542776


def test_the_width_one_guide_keeps_the_line_bit_for_bit():
    modes, numerator, denominator = guide.travelling(CHAIN, CHAIN_FACES, (62, 0, 0), RESONANCE)
    assert modes == [(0, 0)] and numerator == denominator
    assert guide.guide_total(123456789, CHAIN, CHAIN_FACES, (62, 0, 0), RESONANCE) == 123456789


def test_where_no_mode_travels_the_width_one_line_stands_and_every_width_is_reached():
    modes, numerator, denominator = guide.travelling(BOX, CLOSED, (51, 3, 3), (5999, 6000))
    assert modes == [] and numerator == 0  # 17997 - 2 x 5541 = 6915, nothing travels
    assert (
        guide.guide_total(1000000, BOX, CLOSED, (51, 3, 3), (5999, 6000)) == 1000000
    )  # S stands, the near zone's lay
    assert (
        guide.travelling((5, 5, 5), CLOSED, (2, 2, 2), (5751, 6000))[0] == []
    )  # the conserve giver: den cos k_11 = 6865
    assert guide.guide_total(777, (5, 5, 5), CLOSED, (2, 2, 2), (5751, 6000)) == 777
    modes, numerator, denominator = guide.travelling((7, 5, 5), CLOSED, (3, 2, 2), RESONANCE)
    assert modes == [(1, 1)] and 0 < numerator < denominator  # a 5 x 5 cross-section, reached
    assert guide.modes_of(DEN, 4, True, 0) == [
        (0, DEN, 1, 4),
        (1, 0, 1, 4),
        (2, -DEN, 1, 4),
        (3, 0, 1, 4),
    ]
