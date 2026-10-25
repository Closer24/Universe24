"""ol1's one-board test of OL-S1 beside PL-S1 (under 15 s; pytest or a script): the BEAM, nature's heavy row laid at every Node of
the 4-cube as a quarter-turn plane wave along x over the sea (a uniform board with a current: J_x about 36,000 per Node per
interval, the odd line x written every interval), run 100 intervals on the flagged copy src_ol1 in three processes:
(1) the head's path (no flag): the top at 87 with 64 turning, the fall parting from the mirror of the rise at k = 1 in the odd
line x's write remainder (and the heavy plane's levels by 1 through the Link's odd part), no exact return; (2) OL1_PL=kick
OL1_ODD=exchkick (PL-S1 and OL-S1: the odd lines negated at the exchange, the current landing as a momentum kick before the
division): the top at 87, the state at top + k the exchange of the state at top - 1 - k in every level and every odd line's
integer at every Node, the one integer apart the gap-0 plane's write remainder at k = 10 by 2 (the emission's write); (3) the same with the run back of 20 THROUGH the top: 20 of 20; 98 integers, the bits within 128,
births 0, every credit laid back, the emission's count laid 0."""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WORLD = os.path.join(HERE, "worlds", "beam4.json")
LAY = os.path.join(HERE, "worlds", "beam_wave.json")
CODE = r'''
import json, sys
sys.set_int_max_str_digits(0)
sys.path.insert(0, sys.argv[3])
from ol1_run import exchanged, lay_beam, line_equal, names_of, state_of, first_node_off
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER
universe, world = load_world(sys.argv[1])
n, back = int(sys.argv[2]), int(sys.argv[4])
node = Node(universe, dict(world, intervals=n))
lay = lay_beam(node, json.load(open(sys.argv[5]))["beam"])
names = names_of(node)
states, exact, tops, kept = {0: state_of(node)}, {}, [], []
for _ in range(n):
    if back and node.interval >= n - back:
        kept.append(node.state_hash())
    node.step()
    i = node.interval
    states[i] = state_of(node)
    x = [int(v) for v in node.row(CARRIER).lines[0].now.reshape(-1)]
    exact[i] = min(x) == max(x) == node.gamma
    if node.turned.any():
        tops.append((i, int(node.turned.sum())))
top = tops[0][0]
first, same = None, 0
for k in range(1, top):
    if top + k > n:
        break
    mirror = exchanged(node, states[top - 1 - k])
    parted = [(nm, first_node_off(a, b)) for nm, a, b in zip(names, states[top + k], mirror) if not line_equal(a, b)]
    if not parted:
        same += 1
        continue
    first = {"k": k, "lines": parted}
    break
credits = [e for e in node.log if e["event"] == "credit"]
exact_back = 0
for k in range(len(kept)):
    node.step_back()
    exact_back += node.state_hash() == kept[len(kept) - 1 - k]
ints, bits = node.census()
print(json.dumps({"lay": {k: lay[k] for k in ("amplitude", "J_at_origin", "W_at_origin")}, "tops": tops, "equal k": same, "first parting": first,
    "credits": len(credits), "laid back": sum(1 for c in credits if "laid_back" in c), "run back": [exact_back, len(kept)],
    "integers": ints, "bits": bits, "births": node.counts["births"], "laid": node.counts["laid"]}))
'''


def start(flags, intervals, back):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("OL1_", "CS7_", "CS4_"))}
    env.update(PYTHONPATH=os.path.join(HERE, "src_ol1"), TMPDIR="/dev/shm/tmp", **flags)
    return subprocess.Popen([sys.executable, "-c", CODE, WORLD, str(intervals), HERE, str(back), LAY], env=env, stdout=subprocess.PIPE, text=True)


def test_the_beam_retraces_bit_for_bit_under_the_odd_lines_negated_and_kicked() -> None:
    t0 = time.monotonic_ns()
    runs = {
        "head": start({}, 100, 0),
        "ol": start({"OL1_PL": "kick", "OL1_ODD": "exchkick"}, 100, 0),
        "ol through the top": start({"OL1_PL": "kick", "OL1_ODD": "exchkick"}, 100, 20),
    }
    found = {k: json.loads(p.communicate()[0]) for k, p in runs.items()}
    seconds = (time.monotonic_ns() - t0) // 10**9
    print(json.dumps({"seconds (whole, from the monotonic clock in nanoseconds)": seconds, **found}))
    a, b, c = found["head"], found["ol"], found["ol through the top"]
    assert a["lay"]["J_at_origin"][0] != 0 and a["lay"]["J_at_origin"][1:] == [0, 0]
    assert a["tops"][0] == [87, 64] and b["tops"][0] == [87, 64] and c["tops"][0] == [87, 64]
    # (1) the head: the odd line x's write remainder parts at k = 1 (with the heavy plane's levels through the Link's odd part)
    assert a["equal k"] == 0 and a["first parting"]["k"] == 1
    parted = {nm: off for nm, off in a["first parting"]["lines"]}
    assert parted["shape 4 gap 0 line 1"]["field"] == "wr" and parted["shape 4 gap 0 line 1"]["difference"] != 0
    assert "shape 4 gap 0 line 2" not in parted and "shape 4 gap 0 line 3" not in parted
    # (2) OL-S1 with PL-S1: no odd line and no level parts at any k; the one integer apart is the gap-0 plane's re line's write
    # remainder at k = 10, by 2 (the emission's write, EM-S1's odd quotient at the start written after the division: named missing)
    assert b["equal k"] == 9 and b["first parting"]["k"] == 10 and len(b["first parting"]["lines"]) == 1
    name, off = b["first parting"]["lines"][0]
    assert name == "shape 2 gap 0 line 0" and off["field"] == "wr" and abs(off["difference"]) == 2
    # (3) the run back through the top
    assert c["run back"] == [20, 20] and c["first parting"]["k"] == 10
    for r in (a, b, c):
        assert r["integers"] == 98 and r["bits"] <= 128 and r["births"] == 0 and r["laid"] == 0
        assert r["credits"] == r["laid back"]
    assert seconds < 15


if __name__ == "__main__":
    test_the_beam_retraces_bit_for_bit_under_the_odd_lines_negated_and_kicked()
    print("PASS")
