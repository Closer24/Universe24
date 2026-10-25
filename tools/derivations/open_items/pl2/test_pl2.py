"""pl2's one-board test of PL-S1 (under 15 s; pytest or a script): nature's plasma on the 3-cube (tests/worlds/world_plasma_3.json, the
heavy row at +1 and the light massive row at -1 at every Node under the sea) run 170 intervals on the flagged copy src_pl2b in three
processes: (1) CS7_EQ=n alone (the clicks laid back where the net current is 0, David's write 2 W after the step): the top at 84
with 27 turning, the fall parting from the mirror of the rise at k = 1 in ONE line, the sign row's time line's write remainder, by
2 (W(83) - W(82)) = 32 with every level equal, the bottom 939 at 167 (ma1's number), no exact return; (2) CS7_EQ=n PL2_WRITE=kick
(PL-S1: the charge read at the kick in and out and written as a momentum kick): no line parts at any k of the fall (the state at
top + k the exchange of the state at top - 1 - k, bit for bit, 83 of 83), X = Gamma at every Node at 166 and 167, 135 credits in the
rise and 162 to 170, every one laid back; (3) the same to 90 intervals with the run back of 10 THROUGH the top: 10 of 10; 98 integers, the bits
within 128, births 0, the emission's count laid 0."""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
WORLD = os.path.join(WORKTREE, "tests", "worlds", "world_plasma_3.json")
CODE = r'''
import json, sys
sys.set_int_max_str_digits(0)
sys.path.insert(0, sys.argv[3])
from retrace import exchanged, names_of, state_of
from event_universe import gram
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER
universe, world = load_world(sys.argv[1])
n = int(sys.argv[2])
back = int(sys.argv[4])
node = Node(universe, dict(world, intervals=n))
names = names_of(node)
states, exact, means, tops, charges, kept = {0: state_of(node)}, {}, {}, [], {}, []
for _ in range(n):
    if back and node.interval >= n - back:
        kept.append(node.state_hash())
    node.step()
    i = node.interval
    states[i] = state_of(node)
    x = [int(v) for v in node.row(CARRIER).lines[0].now.reshape(-1)]
    means[i], exact[i] = sum(x) // len(x), min(x) == max(x) == node.gamma
    charges[i] = sum(int(gram.charge(r.shape, r.lines).reshape(-1)[0]) for r in node.gapped)
    if node.turned.any():
        tops.append((i, int(node.turned.sum())))
top = tops[0][0]
first, same = None, 0
for k in range(1, top):
    if top + k > n:
        break
    mirror = exchanged(node, states[top - 1 - k])
    if states[top + k] == mirror:
        same += 1
        continue
    first = {"k": k, "lines": [(nm, a, b) for nm, a, b in zip(names, states[top + k], mirror) if a != b]}
    break
credits = [e for e in node.log if e["event"] == "credit"]
exact_back = 0
for k in range(len(kept)):
    node.step_back()
    exact_back += node.state_hash() == kept[len(kept) - 1 - k]
ints, bits = node.census()
bottoms = [(k, means[k]) for k in range(2, n) if means[k] <= means[k - 1] and means[k] < means[k + 1]] if n > 100 else []
print(json.dumps({"tops": tops, "equal k": same, "first parting": first, "W(82), W(83)": [charges.get(82), charges.get(83)],
    "exact at 166 and 167": [exact.get(166), exact.get(167)], "bottoms": bottoms, "credits": len(credits),
    "laid back": sum(1 for c in credits if "laid_back" in c), "credits in the rise": sum(1 for c in credits if c["i"] < top),
    "run back": [exact_back, len(kept)], "integers": ints, "bits": bits, "births": node.counts["births"], "laid": node.counts["laid"]}))
'''


def start(flags, intervals, back):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("PL2_", "CS7_"))}
    env.update(PYTHONPATH=os.path.join(HERE, "src_pl2b"), TMPDIR="/dev/shm/tmp", **flags)
    return subprocess.Popen([sys.executable, "-c", CODE, WORLD, str(intervals), HERE, str(back)], env=env, stdout=subprocess.PIPE, text=True)


def test_the_plasma_retraces_bit_for_bit_and_returns_to_gamma_under_the_charge_at_the_kick() -> None:
    t0 = time.monotonic_ns()
    runs = {
        "n": start({"CS7_EQ": "n"}, 170, 0),
        "kick": start({"CS7_EQ": "n", "PL2_WRITE": "kick"}, 170, 0),
        "kick through the top": start({"CS7_EQ": "n", "PL2_WRITE": "kick"}, 90, 10),
    }
    found = {k: json.loads(p.communicate()[0]) for k, p in runs.items()}
    seconds = (time.monotonic_ns() - t0) // 10**9
    print(json.dumps({"seconds (whole, from the monotonic clock in nanoseconds)": seconds, **found}))
    a, b, c = found["n"], found["kick"], found["kick through the top"]
    assert a["tops"][0] == [84, 27] and b["tops"][0] == [84, 27] and c["tops"][0] == [84, 27]
    # (1) David's write: one line parts at k = 1, the sign row's time line's write remainder, by 2 (W(83) - W(82)) = 32
    assert a["equal k"] == 0 and a["first parting"]["k"] == 1 and len(a["first parting"]["lines"]) == 1
    name, fall, mirror = a["first parting"]["lines"][0]
    assert name == "shape 4 gap 0 line 0" and fall[:4] == mirror[:4] and fall[4] - mirror[4] == -2 * (a["W(82), W(83)"][1] - a["W(82), W(83)"][0]) == -32
    assert a["bottoms"][0] == [167, 939] and a["exact at 166 and 167"] == [False, False]
    # (2) PL-S1: no line parts, the exact return at every Node, every credit laid back
    assert b["equal k"] == 83 and b["first parting"] is None
    assert b["exact at 166 and 167"] == [True, True] and b["bottoms"][0] == [167, 1000]
    assert b["credits"] == b["laid back"] == 162 and b["credits in the rise"] == 135 and a["credits"] == a["laid back"] == 135
    # (3) the run back through the top
    assert c["run back"] == [10, 10] and c["first parting"] is None
    for r in (a, b, c):
        assert r["integers"] == 98 and r["bits"] <= 128 and r["births"] == 0 and r["laid"] == 0
    assert seconds < 15


if __name__ == "__main__":
    test_the_plasma_retraces_bit_for_bit_and_returns_to_gamma_under_the_charge_at_the_kick()
    print("PASS")
