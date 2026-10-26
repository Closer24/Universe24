"""cm2's one test (under 15 s): on the chiral 3-cube to 12 intervals under CM2_FORM=1, every birth's children keep the charge (W summing 0 where the plane stood at nothing), the pair's lay momentum lies along the Link alone where laid onto nothing, the along-Link recoil is reduced to a remainder below the pair's gain per unit a, the relative L about the midpoint is 0, the run back exact; and the letter's theorem: the alike (symmetric) re_before of the two children carries no momentum, the opposite (antisymmetric) carries it along the Link alone. Run: CM2_FORM=1 PYTHONPATH=/dev/shm/tmp/cm2/src_cm2 python tests_cm2.py"""
import json
import os
import sys

sys.set_int_max_str_digits(0)
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("CM2_SRC", "/dev/shm/tmp/cm2/src_cm2"))
os.environ["CM2_FORM"] = "1"
from event_universe import close  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.run import record  # noqa: E402

u, w = load_world(os.path.join(here, "worlds", "world_chiral_3_30.json"))
found = record(u, dict(w, intervals=12), 4, lambda line: None)
births = [e for e in found["log"] if e["event"] == "birth"]
assert births, "no birth to read"
assert found["run_back"]["exact"] == found["run_back"]["intervals"] == 4, found["run_back"]
for e in births:
    minus, plus = e["minus"], e["plus"]
    axis = next(b for b in range(3) if minus[b] != plus[b])
    ends = e["dP_lay_ends"]
    p = [int(e["dP_take"][b]) + int(ends[0][b]) + int(ends[1][b]) for b in range(3)]
    a = int(e["moving"][1])
    assert e["moving"] == [-a, a], e["moving"]
    if all(v == 0 for s in e["stood"] for v in s):
        assert sum(int(x) for x in e["W_children"]) == 0 and abs(int(e["W_children"][0])) == found["T"] // 2
        lay = [int(ends[0][b]) + int(ends[1][b]) for b in range(3)]
        onto_nothing = all(int(ends[k][b]) == 0 for k in range(2) for b in range(3) if b != axis)
        if a:
            gain = abs(lay[axis]) // abs(a)
            assert abs(p[axis]) < gain or abs(p[axis]) < abs(int(e["dP_take"][axis])), (p, gain)
        arm = [[2 * minus[b] - minus[b] - plus[b] for b in range(3)], [2 * plus[b] - minus[b] - plus[b] for b in range(3)]]
        l2 = [sum(arm[k][(b + 1) % 3] * int(ends[k][(b + 2) % 3]) - arm[k][(b + 2) % 3] * int(ends[k][(b + 1) % 3]) for k in range(2)) for b in range(3)]
        assert l2 == [0, 0, 0] or not onto_nothing, l2
# the theorem on a fresh board: the symmetric part carries nothing, the antisymmetric part along the Link alone
node = Node(u, dict(w, intervals=1, seed=[]))
s = next(k for k, r in enumerate(node.records()) if r.shape == 2 and r is not node.emitter())
minus, plus = (0, 0, 0), (1, 0, 0)
alike = [0, 0, 0]
for where, sense in ((minus, -1), (plus, 1)):
    alike = [x + y for x, y in zip(alike, close.child_at(node, s, where, sense, moving=7))]
for where, sense in ((plus, 1), (minus, -1)):
    close.child_at(node, s, where, sense, -1, moving=7)
assert alike == [0, 0, 0], alike
dp0, gain = close.pair_gain(node, s, minus, plus)
assert dp0 == [0, 0, 0] and gain[1] == 0 and gain[2] == 0 and gain[0] != 0, (dp0, gain)
num = node.records()[s].pair[0]
assert abs(gain[0]) == 4 * num * node.A, (gain, num, node.A)
print(json.dumps({"births": len(births), "run_back": found["run_back"], "gain_per_unit_a": gain, "four_num_A": 4 * num * node.A, "alike_momentum": alike}))
