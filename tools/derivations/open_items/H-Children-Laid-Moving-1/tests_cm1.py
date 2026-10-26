"""cm1's one test (under 15 s): the chiral 3-cube world run 8 intervals on the flagged copy. Flag off: the state hash equals the head's own src bit for bit. Flag on: at every birth W sums 0, the children's Q is an integer with the P balance along the pair's Link within half the lay's quantum (the carried division's remainder), the pair's relative L is 0 (the one-Link couple theorem), the transverse recoil is the remainder in full, and the run back is exact. Usage: tests_cm1.py <copy src> <head src>"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORLD = os.path.join(HERE, "worlds", "world_chiral_3_30.json")
RUNNER = f"""
import json, sys
sys.path.insert(0, sys.argv[1]); sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
u, w = load_world({WORLD!r}); w = dict(w, intervals=8)
node = Node(u, w); hashes = []
for _ in range(8):
    node.step(); hashes.append(node.state_hash())
births = [e for e in node.log if e["event"] == "birth" and "takes" not in e]
back = 0
for k in range(3):
    node.run(-1); back += node.state_hash() == hashes[-2 - k]
print(json.dumps({{"hash": hashes[-1], "births": births, "back": back, "cube": int(w["shape"][0])}}, default=str))
"""


def run(src, flag):
    env = dict(os.environ, CM1_FORM=flag, TMPDIR="/dev/shm/tmp")
    out = subprocess.run([sys.executable, "-c", RUNNER, src], capture_output=True, text=True, env=env, check=True)
    import json

    return json.loads(out.stdout.strip().splitlines()[-1])


def test_cm1(copy_src, head_src):
    off, head = run(copy_src, ""), run(head_src, "")
    assert off["hash"] == head["hash"], "the flag off is not the head bit for bit"
    on = run(copy_src, "1")
    assert on["back"] == 3, "the run back is not exact"
    cube = on["cube"]
    assert on["births"], "no birth to read"
    for e in on["births"]:
        assert sum(int(x) for x in e["W_children"]) == 0
        d = [((p - m) % cube) for p, m in zip(e["plus"], e["minus"])]
        d = [x - cube if x > cube // 2 else x for x in d]
        ax = [a for a in range(3) if d[a]][0]
        dpt, dpl = [int(x) for x in e["dP_take"]], [int(x) for x in e["dP_lay"]]
        q = int(e["cm1_q"][1])
        assert isinstance(q, int)
        bal = [a + b for a, b in zip(dpt, dpl)]
        if q:
            assert 2 * abs(bal[ax]) <= abs(dpl[ax] // q), "the along-Link balance beyond half the quantum"
        ends = e["dP_lay_ends"]
        nothing = all(int(x) == 0 for x in ends[0]) and not any(int(x) for row in e["stood"] for x in row)
        if nothing:  # onto nothing at the - end: the pair's lay momentum is along its own Link and its relative L is 0
            assert all(dpl[b] == 0 for b in range(3) if b != ax), "a transverse lay momentum onto nothing"
            rel = [int(a) - int(b) for a, b in zip(ends[1], ends[0])]
            lr = [d[1] * rel[2] - d[2] * rel[1], d[2] * rel[0] - d[0] * rel[2], d[0] * rel[1] - d[1] * rel[0]]
            assert lr == [0, 0, 0], "a relative L onto nothing"
    return {"births": len(on["births"]), "back": on["back"], "flag_off_equals_head": True}


if __name__ == "__main__":
    print(test_cm1(sys.argv[1], sys.argv[2]))
