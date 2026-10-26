"""The one test of the hand bc1 (under 15 s): the hole world at 60 intervals run forward and back by the reader; the run back exact at every step from the last interval to the first birth (the arrow, the law's inverse), every birth's root recovered to the integer at both ends (the shared root), every click within its cone (one Link per interval), and the reading through the root bounded: the per-pair identity in {-2, 2}, |S| <= 2, S through the root equal to S by the frame (the root carries no setting), S by the senses -2 exactly."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from bell_root_bc1 import main  # noqa: E402


def test_bell_through_the_root_hole_60(tmp_path):
    out = main(os.path.join(HERE, "worlds", "world_hole_60.json"), str(tmp_path / "hole60.json"))
    rb = out["run_back"]
    assert rb["steps"] > 0 and rb["exact"] == rb["steps"]
    assert rb["roots_captured"] == out["births"] > 0
    assert rb["roots_recovered_equal_every_integer"] == out["births"]
    assert out["cone"]["within_cone"] == out["cone"]["clicks"] > 0
    assert set(out["per-pair identity"]) <= {-2, 2}
    assert out["|S| <= 2 through the root"] is True
    assert out["S^2 > 8 through the root"] is False
    assert out["S through the root equals S by the frame"] is True
    num, den = (int(x) for x in out["S by the senses"].split(" / "))
    assert num == -2 * den
