"""The guide clause of the emission (ALGEBRA.md, The click writes on the lattice (5), BUILT 2026-10-22; src/event_universe/guide.py): a source in time lays S on the guide of width one, and on a wider cross-section the clause lays S over R, the share of S the guide's travelling transverse modes carry, so that one quantum travels. The numbers are the box's (examples/events/clicks/clicks_box.json, 61 x 7 x 7 closed, the body at (51, 3, 3), the resonance [5414, 6000]): the mode (1, 1) alone travels, its weight 1 / 16 at the centre, R = (1 / 16)(sin k / sin k_mn) with sin k 0.7071 and sin k_mn 0.5117, the factor 11.58 (the reader's 16 sin k_z / sin k = 11.6); on the chain's cross-section of 1 x 1 R is 1 exactly and S stands bit for bit; where no mode travels the lay is refused by name; a width whose cosines the table's acts do not reach (w + 1 no power of two) keeps the width-one line."""

import pytest

from event_universe import guide

DEN = 6000
BOX, CHAIN = (61, 7, 7), (101, 1, 1)
CLOSED, CHAIN_FACES = (False, False, False), (False, True, True)
RESONANCE = (5414, 6000)


def test_the_half_angle_chain_reads_the_cosines_of_pi_over_four_and_eight():
    quarter = guide.half_angle(DEN, 0)
    assert (
        quarter == 4242 and guide.half_angle(DEN, quarter) == 5543
    )  # den cos(pi / 4), den cos(pi / 8), floored
    assert (
        guide.base_cosine(DEN, 7) == 5543 and guide.base_cosine(DEN, 5) is None
    )  # 8 a power of two, 6 not


def test_the_box_has_one_travelling_mode_and_the_factor_of_the_reader():
    modes, numerator, denominator = guide.travelling(BOX, CLOSED, (51, 3, 3), RESONANCE)
    assert modes == [(1, 1)]
    assert 11.5 < denominator / numerator < 11.7  # 16 sin k_z / sin k = 11.6
    assert guide.guide_total(1000000, BOX, CLOSED, (51, 3, 3), RESONANCE) == 11576888


def test_the_width_one_guide_keeps_the_line_bit_for_bit():
    modes, numerator, denominator = guide.travelling(CHAIN, CHAIN_FACES, (62, 0, 0), RESONANCE)
    assert modes == [(0, 0)] and numerator == denominator
    assert guide.guide_total(123456789, CHAIN, CHAIN_FACES, (62, 0, 0), RESONANCE) == 123456789


def test_no_travelling_mode_is_refused_by_name_and_an_unreached_width_keeps_the_line():
    with pytest.raises(ValueError, match="no mode of the guide travels"):
        guide.guide_total(1000000, BOX, CLOSED, (51, 3, 3), (5999, 6000))
    assert guide.travelling((7, 5, 5), CLOSED, (3, 2, 2), RESONANCE) is None
    assert guide.guide_total(1000000, (7, 5, 5), CLOSED, (3, 2, 2), RESONANCE) == 1000000
