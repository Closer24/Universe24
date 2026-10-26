"""The click reader's arithmetic (bk1): nature's singlet at the exact cosines is -14/5 and sits in the band 4 < S^2 <= 8; the per-pair identity of four signs is in {-2, 0, 2}; the four readings written under out/ keep |S| <= 2 and the twin one Link away. Under one second; the readings themselves are bk1_click_read.py's runs."""
import json
import os
from itertools import product

from bk1_click_read import EXACT_A, EXACT_B, nature_singlet

HERE = os.path.dirname(os.path.abspath(__file__))


def test_nature_singlet_exact_cosines():
    es, s = nature_singlet(EXACT_A, EXACT_B)
    assert es[(0, 0)] == (-3, 5) and es[(0, 1)] == (4, 5) and es[(1, 0)] == (-4, 5) and es[(1, 1)] == (-3, 5)
    assert s == (-14, 5)
    n, d = s
    assert 4 * d * d < n * n <= 8 * d * d


def test_identity_of_four_signs_is_bounded():
    for a0, a1, b0, b1 in product((-1, 0, 1), repeat=4):
        assert a0 * b0 - a0 * b1 + a1 * b0 + a1 * b1 in (-2, -1, 0, 1, 2)
    for a0, a1, b0, b1 in product((-1, 1), repeat=4):
        assert a0 * b0 - a0 * b1 + a1 * b0 + a1 * b1 in (-2, 2)


def test_readings_bounded_and_twin_one_link():
    for w in ("hole_60", "chiral_60", "chiral_300", "two_slits_AB"):
        path = os.path.join(HERE, "out", w + ".json")
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        assert d["twin_links_at_birth"] == {"1": d["pairs_both_clicked"]}
        assert d["run_back"]["exact"] == d["run_back"]["steps"]
        for key in ("law by the frame at the exact cosines: S", "law by the frame at row 56's settings: S", "law by the senses: S"):
            n, den = (int(x) for x in d[key].split(" / "))
            assert n * n <= 4 * den * den
