"""eq2's one-board test of EQ-S1 (under 15 s; pytest or a script): the pair of the heavy row laid at every Node of the 3-cube at one
quantum (tests/worlds/world_pair_3.json) run 175 intervals under the flagged copy src_eq2 in three processes, the flag absent
(David's path), EQ2_CLICK=a (the click refused where nothing arrives) and EQ2_CLICK=b (the equilibrium: the take laid back in the
same close), and read: the flag absent bottoms at 171 at 953 with 135 credits in the rise (the head's pinned numbers, the light taken);
under a and b the board returns to Gamma EXACTLY at every Node at 168 and 169 (ma1's 168 / 169), the top at 85 with 27 turning; under
b 81 credits, every one laid back, under a none; the state hash at 169 equal under a and b (the light's state untouched by the laid-back
click); the run back exact 10 of 10 through the credit intervals under b; 98 integers, the bits within 128; the emission's count laid 0
on every run (EM-S1 lays nothing on a uniform board)."""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
WORLD = os.path.join(WORKTREE, "tests", "worlds", "world_pair_3.json")
CODE = r'''
import json, sys
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER
universe, world = load_world(sys.argv[1])
node = Node(universe, dict(world, intervals=175))
means, exact, tops, hashes = [], [], [], {}
kept = []
for _ in range(175):
    if node.interval >= 165:
        kept.append(node.state_hash())
    node.step()
    x = [int(v) for v in node.row(CARRIER).lines[0].now.reshape(-1)]
    means.append(sum(x) // len(x))
    exact.append(min(x) == max(x) == node.gamma)
    if node.turned.any():
        tops.append((node.interval, int(node.turned.sum())))
    if node.interval in (168, 169):
        hashes[node.interval] = node.state_hash()
bottoms = [(k + 1, means[k]) for k in range(1, 174) if means[k] <= means[k - 1] and means[k] < means[k + 1]]
credits = [e for e in node.log if e["event"] == "credit"]
back = 0
for k in range(10):
    node.step_back()
    back += node.state_hash() == kept[9 - k]
n, bits = node.census()
print(json.dumps({"bottoms": bottoms, "exact at 168 and 169": [exact[167], exact[168]], "tops": tops,
    "credits": len(credits), "laid back": sum(1 for c in credits if "laid_back" in c),
    "credits in the rise": sum(1 for c in credits if c["i"] < 85), "hash 169": hashes[169], "run back": back,
    "integers": n, "bits": bits, "laid": node.counts["laid"], "births": node.counts["births"]}))
'''


def run_flag(flag):
    env = dict(os.environ, PYTHONPATH=os.path.join(HERE, "src_eq2"), TMPDIR="/dev/shm/tmp")
    env.pop("EQ2_CLICK", None)
    env.pop("EQ2_CROSS", None)
    if flag:
        env["EQ2_CLICK"] = flag
    return subprocess.Popen([sys.executable, "-c", CODE, WORLD], env=env, stdout=subprocess.PIPE, text=True)


def readings():
    procs = {flag: run_flag(flag) for flag in (None, "a", "b")}
    return {flag: json.loads(p.communicate()[0]) for flag, p in procs.items()}


def test_the_body_at_rest_lays_back_and_the_uniform_board_returns_to_gamma_exactly_eq():
    found = readings()
    head, a, b = found[None], found["a"], found["b"]
    assert head["bottoms"] == [[171, 953]] and head["credits in the rise"] == 135 and head["laid back"] == 0
    for r in (a, b):
        assert r["bottoms"] == [[169, 1000]] and r["exact at 168 and 169"] == [True, True]
        assert r["tops"] == [[85, 27]] and r["births"] == 0
    assert a["credits"] == 0
    assert b["credits in the rise"] == 81 and b["laid back"] == b["credits"] > 81
    assert a["hash 169"] == b["hash 169"] and a["hash 169"] != head["hash 169"]
    assert b["run back"] == 10 and head["run back"] == 10
    for r in (head, a, b):
        assert r["integers"] == 98 and r["bits"] <= 128 and r["laid"] == 0
    return found


if __name__ == "__main__":
    t0 = time.monotonic_ns()
    found = test_the_body_at_rest_lays_back_and_the_uniform_board_returns_to_gamma_exactly_eq()
    for flag, r in found.items():
        print(flag or "absent", json.dumps(r))
    print("PASS in", (time.monotonic_ns() - t0) // 1000000, "ms")
