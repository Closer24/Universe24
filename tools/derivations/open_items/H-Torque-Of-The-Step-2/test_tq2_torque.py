"""H-Torque-Of-The-Step-2: the step's torque identity closes to the integer on the hole (3 intervals, REST 0, the terms' sum the measured change), and the one-end pace's asymmetric part is present where the paces differ."""
import json, os, subprocess, sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

def fr(x):
    n, _, d = x.partition("/")
    return Fr(int(n), int(d or 1))

def test_the_identity_closes_on_the_hole(tmp_path):
    out = tmp_path / "hole.json"
    env = dict(os.environ, PYTHONPATH=os.path.join(ROOT, "src"))
    subprocess.run([sys.executable, os.path.join(HERE, "tq2_torque.py"), os.path.join(ROOT, "tests", "worlds", "world_hole.json"), str(out), "3"], check=True, env=env, capture_output=True)
    o = json.load(open(out))
    assert o["intervals_with_REST_not_0"] == 0
    seen_asym = False
    for r in o["per_interval"]:
        total = [Fr(0)] * 3
        for k, v in r["terms"].items():
            if k != "REST":
                total = [t + fr(x) for t, x in zip(total, v)]
        assert [int(t) for t in total] == r["dL2_step"] and all(t.denominator == 1 for t in total)
        seen_asym |= any(fr(x) != 0 for x in r["terms"]["LINKS_ASYM"])
        assert all(fr(x) == 0 for x in r["terms"]["TURN"]) and all(fr(x) == 0 for x in r["terms"]["CURL"])
    assert seen_asym
