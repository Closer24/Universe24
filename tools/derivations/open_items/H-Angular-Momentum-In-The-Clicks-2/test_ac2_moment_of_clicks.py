"""The clicks' moment reader (H-Angular-Momentum-In-The-Clicks-2): the identities on a small synthetic log and on a shipped record where present. Under a second."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from ac2_moment_of_clicks import cross, moment_of_clicks, shift_identity  # noqa: E402

RECORDS = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", "records", "2ab32b518")


def synthetic() -> dict:
    """Two credits mirrored about the centre of a 3-cube (the mirror keeps dP_y and flips the arm, so the moments cancel), one laid-back credit (dP 0), one birth onto nothing (dP_lay 0, senses opposite)."""
    return {"cube": 3, "log": [
        {"event": "credit", "i": 1, "node": [0, 1, 1], "dP_take": [0, 5, 0], "sense": 1},
        {"event": "credit", "i": 1, "node": [2, 1, 1], "dP_take": [0, 5, 0], "sense": -1},
        {"event": "credit", "i": 2, "node": [1, 1, 1], "dP_take": [0, 0, 0], "sense": 1, "laid_back": 3},
        {"event": "birth", "i": 3, "node": [1, 2, 1], "minus": [1, 1, 1], "plus": [1, 2, 1], "senses": [-1, 1],
         "W_children": [-18000, 18000], "dP_take": [7, 0, 0], "dP_lay": [0, 0, 0]},
    ]}


def test_mirrored_credits_cancel_and_laid_back_books_zero() -> None:
    r = moment_of_clicks(synthetic(), [2, 2, 2])
    assert r["J2 of the credits"] == [0, 0, 0]
    assert r["laid back with dP_take 0"] == 1 and r["credits laid back"] == 1
    assert r["births with dP_lay 0"] == 1 and r["births with senses summing to 0"] == 1
    # the birth's take at node [1,2,1]: arm 2r-2c = [0, 2, 0], dP [7,0,0]: the moment [0, 0, -14]
    assert r["J2 of the births' takes"] == cross([0, 2, 0], [7, 0, 0]) == [0, 0, -14]
    assert r["J2 clicks"] == [0, 0, -14] and r["P clicks"] == [7, 10, 0]


def test_centre_law_exact() -> None:
    assert shift_identity(synthetic(), [2, 2, 2], [0, 0, 0])
    assert shift_identity(synthetic(), [2, 2, 2], [4, 0, 2])


def test_the_take_moment_is_link_position_free() -> None:
    """A Link's momentum is along its own axis, so the moment about any point on the Link's line is one: t a x (p a) = 0 for every t."""
    for a, p in (([1, 0, 0], [3, 0, 0]), ([0, 1, 0], [0, -9, 0]), ([0, 0, 1], [0, 0, 11])):
        for t in (-3, -1, 0, 1, 2):
            assert cross([t * x for x in a], p) == [0, 0, 0]


def test_shipped_records_where_present() -> None:
    sys.set_int_max_str_digits(0)
    for name, laid_back_all in (("world_universe_400.json", True), ("world_hole_60.json", False)):
        path = os.path.join(RECORDS, name)
        if not os.path.exists(path):
            continue
        rec = json.load(open(path))
        r = moment_of_clicks(rec, [rec["cube"] - 1] * 3)
        assert r["laid back with dP_take not 0"] == 0
        assert r["births with dP_lay 0"] == r["births"]  # every birth onto nothing on these two
        if laid_back_all:
            assert r["credits laid back"] == r["credits"] and r["J2 clicks"] == [0, 0, 0]
        else:
            assert r["J2 clicks"][1] == -r["J2 clicks"][2] and r["P clicks"][1:] == [0, 0]
        assert shift_identity(rec, [rec["cube"] - 1] * 3, [0, 0, 0])
