"""The flux lines' read (Y-S2) measured with a hand-set flux line, as Y2 measured it: the world named (the plasma of the 3-cube, a gapped plane at every Node) to 8, g_0x set to V at every Node (now and before), one interval from the same state with V = 0 and with V = 50: the entries that differ per row (the gap-0 row turned by nothing, a gapped plane turned where it stands), the run back through the fed state 6 of 6, and the rest rotations K per gapped pair."""
import sys, copy, json
sys.set_int_max_str_digits(0)
from event_universe.rows import CARRIER, PLANE
from tests.laws import node_of, state_of
node = node_of(sys.argv[2] if len(sys.argv) > 2 else "world_hole.json")
for _ in range(8):
    node.step()
out = {"rotation K per record pair (omega_0 Gamma to the unit)": {str(r.pair): node.rotation_of(r.pair) for r in node.records() if r.pair}}
fed = copy.deepcopy(node)
for a in (fed.row(CARRIER).lines[4].now, fed.row(CARRIER).lines[4].before):
    a[:] = 50
kept = copy.deepcopy(fed)
node.step(); fed.step()
diff = {}
for r0, r1 in zip(node.rows_, fed.rows_, strict=True):
    n = sum(1 for l0, l1 in zip(r0.lines, r1.lines, strict=True) for a0, a1 in ((l0.now, l1.now), (l0.before, l1.before), (l0.rem, l1.rem)) for x, y in zip(a0.reshape(-1), a1.reshape(-1), strict=True) if int(x) != int(y))
    diff[f"shape {r0.shape} gap {r0.gap}"] = n
out["entries differing after one interval, V = 50 against V = 0, per row"] = diff
states = []
for _ in range(6):
    states.append(state_of(kept)); kept.step()
out["run back through the fed state"] = sum(state_of(kept) == states[5 - k] for k in range(6) if not kept.step_back())
print(json.dumps(out)); json.dump(out, open(sys.argv[1], "w"), indent=1)
