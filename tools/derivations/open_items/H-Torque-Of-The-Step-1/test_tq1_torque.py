"""H-Torque-Of-The-Step-1: the identity of the step's torque on a small world, under 15 s.
The step's change of the board's 2 L across the riding lines' divisions equals the sum of the seven local terms
(ride, rounding, mass, link sym, link asym, curl, turn), exactly, at every interval; the identity per line
2 W (next - 2 now + before) = 2 (X F + rem - rem') + (Wb - W)(2 (now - before) - 1) holds at every Node."""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def test_identity_on_the_hole_six_intervals(tmp_path):
    sys.set_int_max_str_digits(0)
    world = json.load(open(os.path.join(ROOT, "tests", "worlds", "world_hole.json")))
    universe = json.load(open(os.path.join(ROOT, "tests", "worlds", world["universe"])))
    world["intervals"] = 6
    cache = tmp_path / "cache.json"
    json.dump({"world": world, "universe": universe}, open(cache, "w"))
    out = tmp_path / "out.json"
    env = dict(os.environ, PYTHONPATH=os.path.join(ROOT, "src"))
    subprocess.run([sys.executable, os.path.join(HERE, "tq1_torque.py"), str(cache), str(out)], check=True, env=env, capture_output=True)
    d = json.load(open(out))
    s = d["summary"]
    assert s["identity_misses"] == 0
    assert s["line_misses"] == 0
    assert len(d["per_interval"]) == 6
    assert all(r["identity"] for r in d["per_interval"])
    # the curl's torque is 0 on a plane row (a row with no axis matrices) and the lays move no record current
    for r in d["per_interval"]:
        assert all(x == "0/1" for x in r["terms"]["curl"])
