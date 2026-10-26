"""bk2's one test (under 10 s): the hole 60 read by bk2_read.py: the run back exact 60 of 60, 16 pairs clicked at both ends, the twin one Link away at every first click, no first click laid back, the law's S by the frame -16/16 and by the sense -32/16 with every identity in {-2, 2}, nature's S -14/5 within the band 4 den^2 < num^2 <= 8 den^2 and the law's outside it."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORLD = os.path.join(HERE, "..", "H-Bell-Through-The-Cone-1", "worlds", "world_hole_60.json")


def test_hole_60(tmp_path):
    out = tmp_path / "hole_60.json"
    subprocess.run([sys.executable, os.path.join(HERE, "bk2_read.py"), WORLD, str(out)], check=True, capture_output=True)
    d = json.loads(out.read_text())
    assert d["run back exact, intervals"] == 60
    assert d["pairs clicked at both ends"] == 16
    assert d["twin Link distance at the first click: per pair"] == [1] * 16
    assert d["first clicks laid back (EQ-S1)"] == 0
    assert d["the law's S at the clicks by the frame"]["S as a rational"] == [-16, 16]
    assert d["the law's S at the clicks by the sense"]["S as a rational"] == [-32, 16]
    assert set(d["the law's S at the clicks by the frame"]["identity per pair"]) <= {"-2", "2"}
    nat = d["nature's singlet on these settings"]
    assert nat["S as a rational"] == [-14, 5] and nat["4 den^2 < S^2 <= 8 den^2"] is True
    assert d["the law's S at the clicks by the frame"]["4 den^2 < S^2 <= 8 den^2 (nature's band)"] is False
