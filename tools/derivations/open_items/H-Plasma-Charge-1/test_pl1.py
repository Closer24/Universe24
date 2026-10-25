"""pl1's one-board test (under 15 s; pytest or a script): nature's plasma on the 3-cube (the heavy row 2 at +1 and the light row 1 at
-1 at every Node, ma1's lay: amplitudes 136 and 5,690, the Node's charge +1,154) run 170 intervals under the flagged copy src_pl1 in
three processes: EQ2_CLICK=a (the clicks refused: the head's sign row), EQ2_CLICK=a with PL1_SIGN=kick, and EQ2_CLICK=b with
PL1_SIGN=kick (nature's: the clicks laid back, the charge as a kick). Read: under the head's sign row the board bottoms at 939 at
167 and the carrier's retrace X(top + k) = X(top - 2 - k) parts at k = 9 by one level; under the kick the board returns to Gamma
EXACTLY at every Node at 166 and 167 with the retrace equal at every k, the top at 84 with 27 turning, births 0, the run back exact
10 of 10 through the top, 98 integers, the bits within 128, the emission laid 0; under b every credit laid back (81 in 170)."""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WORLD = os.path.join(HERE, "worlds", "h3.json")
CODE = r'''
import json, sys
sys.set_int_max_str_digits(0)
from pathlib import Path
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.rows import CARRIER
sys.path.insert(0, sys.argv[2])
import pl1_run
where = Path(sys.argv[1])
world = json.loads(where.read_text()); universe = json.loads(where.parent.joinpath(world["universe"]).read_text())
plasma = [l for l in world["seed"] if l["lay"] == "plasma"]
universe, stripped = read_world(dict(world, seed=[l for l in world["seed"] if l["lay"] != "plasma"], intervals=170), universe)
node = Node(universe, stripped)
laid = [pl1_run.lay_plasma(node, l) for l in plasma]
means, exact, tops, kept = [], [], [], []
for _ in range(170):
    if 78 <= node.interval < 88:
        kept.append(node.state_hash())
    node.step()
    x = [int(v) for v in node.row(CARRIER).lines[0].now.reshape(-1)]
    means.append(sum(x) // len(x)); exact.append(min(x) == max(x) == node.gamma)
    if node.turned.any():
        tops.append((node.interval, int(node.turned.sum())))
top = tops[0][0]
X = {k + 1: m for k, m in enumerate(means)}; X[0] = node.gamma
parting = next((k for k in range(1, top - 2) if X[top + k] != X[top - 2 - k]), None)
bottoms = [(k + 1, means[k]) for k in range(1, 169) if means[k] <= means[k - 1] and means[k] < means[k + 1]]
credits = [e for e in node.log if e["event"] == "credit"]
state_end = node.state_hash()
back = 0
for _ in range(170 - 88):
    node.step_back()
for k in range(10):
    node.step_back(); back += node.state_hash() == kept[9 - k]
n, bits = node.census()
print(json.dumps({"laid W": [l["W of the Node after"] for l in laid], "bottoms": bottoms, "exact at 166 and 167": [exact[165], exact[166]],
    "tops": tops, "retrace first parting k": parting, "credits": len(credits), "laid back": sum(1 for c in credits if "laid_back" in c),
    "run back through the top": back, "integers": n, "bits": bits, "laid": node.counts["laid"], "births": node.counts["births"]}))
'''


def run_flag(click, sign):
    env = dict(os.environ, PYTHONPATH=os.path.join(HERE, "src_pl1"), TMPDIR="/dev/shm/tmp")
    env.pop("EQ2_CLICK", None)
    env.pop("PL1_SIGN", None)
    env["EQ2_CLICK"] = click
    if sign:
        env["PL1_SIGN"] = sign
    return subprocess.Popen([sys.executable, "-c", CODE, WORLD, HERE], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def readings():
    procs = {name: run_flag(*flags) for name, flags in (("a", ("a", None)), ("a kick", ("a", "kick")), ("b kick", ("b", "kick")))}
    found = {}
    for name, p in procs.items():
        out, err = p.communicate()
        assert p.returncode == 0, err[-2000:]
        found[name] = json.loads(out)
    return found


def test_the_plasma_returns_to_gamma_exactly_under_the_charge_as_a_kick_pl1():
    found = readings()
    head, kick, nature = found["a"], found["a kick"], found["b kick"]
    assert head["laid W"] == [18224, 1154]
    assert head["bottoms"] == [[167, 939]] and head["retrace first parting k"] == 9 and head["credits"] == 0
    for r in (kick, nature):
        assert r["bottoms"] == [[167, 1000]] and r["exact at 166 and 167"] == [True, True]
        assert r["retrace first parting k"] is None and r["tops"] == [[84, 27]] and r["births"] == 0
    assert kick["credits"] == 0
    assert nature["credits"] == 81 and nature["laid back"] == 81
    for r in (head, kick, nature):
        assert r["run back through the top"] == 10 and r["integers"] == 98 and r["bits"] <= 128 and r["laid"] == 0
    return found


if __name__ == "__main__":
    t0 = time.monotonic_ns()
    found = test_the_plasma_returns_to_gamma_exactly_under_the_charge_as_a_kick_pl1()
    for name, r in found.items():
        print(name, json.dumps(r))
    print("PASS in", (time.monotonic_ns() - t0) // 1000000, "ms")
