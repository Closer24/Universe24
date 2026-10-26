"""The one test of the hand bc2 (under 15 s): the hole world at 60 run forward and back with the state's hash at every interval (the run back exact 60 of 60, every act its own inverse); every born pair's two clicks within the cone of the birth's Link (the Link distance at most the intervals back); the root's integers read from the birth line; at every pair the identity A(a) B(b) - A(a) B(b') + A(a') B(b) + A(a') B(b') in {-2, 2} by the clicks and by the root, so |S| <= 2 by every reading and S^2 > 8 is not read; the senses' S = -2 exactly."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORLD = os.path.join(HERE, "..", "..", "..", "..", "tests", "worlds", "world_hole.json")


def test_bell_through_the_root_on_the_hole_60(tmp_path):
    out = tmp_path / "root_hole_60.json"
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.join(HERE, "..", "..", "..", "..", "src")
    subprocess.run([sys.executable, os.path.join(HERE, "root_read.py"), WORLD, str(out)], check=True, env=env, capture_output=True)
    with open(out, encoding="utf-8") as f:
        r = json.load(f)
    assert r["run back exact, intervals"] == r["run back intervals"] == 60
    assert r["births"] >= 10 and r["pairs clicked at both ends"] >= 10
    assert r["every pair's clicks within the cone"] is True
    assert r["every pair's run back exact to its birth"] is True
    for p in r["pairs"]:
        assert all(dist <= d for dist, d in zip(p["Link distance click to the birth's Link"], p["intervals back to the birth"]))
        assert p["identity at the clicks, the frame"] in (-2, 0, 2)
        assert p["identity at the root, the frame"] in (-2, 2)
        assert p["identity at the clicks, the sense"] == -2
        assert p["root"]["senses"] == [-1, 1]
    for key in (
        "S at the clicks by the frame",
        "S at the clicks by the sense",
        "S through the root by the frame (the lay's levels)",
        "S through the root by the sense",
    ):
        num, den = r[key]["S as a rational"]
        assert abs(num) <= 2 * den
        assert not (num * num > 8 * den * den)
    num, den = r["S at the clicks by the sense"]["S as a rational"]
    assert num == -2 * den
