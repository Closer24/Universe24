"""The exact return of the uniform board (the sentences BB-S1, then MA-S1, then CS6-S1): the state at the return (X = Gamma at every Node) against the seed's state, line by line at the Node (0, 0, 0): which integers return (now, before, the rotation remainder, the write remainder) and which do not; the whole state's hash equal or not; the next cycle's return compared with the first. A reader, no act; integers only."""
import json
import sys

from event_universe.rows import CARRIER
from tests.laws import node_of

sys.set_int_max_str_digits(0)
AT = (0, 0, 0)


def snapshot(node):
    found = []
    for k, r in enumerate(node.rows_):
        for j, line in enumerate(r.lines):
            found.append((k, j, int(line.now[AT]), int(line.before[AT]), int(line.rem[AT]), None if line.wr is None else int(line.wr[AT])))
    return found


for name, returns in (("world_sea_3.json", (114, 115, 229, 230)), ("world_pair_3.json", (168, 169, 333, 334)), ("world_universe_3.json", (200, 201, 399, 400))):
    node = node_of(name)
    seed = snapshot(node)
    seed_hash = node.state_hash()
    shots = {}
    for t in range(1, max(returns) + 1):
        node.step()
        if t in returns:
            shots[t] = (snapshot(node), node.state_hash(), int(node.row(CARRIER).lines[0].now[AT]))
    out = {"world": name}
    for t in returns:
        shot, h, x = shots[t]
        same = [(k, j) for (k, j, *a), (_k, _j, *b) in zip(seed, shot) if a == b]
        differ = [(k, j, a, b) for (k, j, *a), (_k, _j, *b) in zip(seed, shot) if a != b]
        out[str(t)] = {"X": x, "lines equal to the seed": len(same), "of": len(seed), "lines differing (row index, line, seed (now, before, rem, wr), at the return)": differ[:6]}
    a, b = shots[returns[1]][0], shots[returns[3]][0]
    out["second return against the first (lines equal)"] = sum(1 for p, q in zip(a, b) if p[2:] == q[2:])
    out["levels now equal first/second return"] = sum(1 for p, q in zip(a, b) if p[2] == q[2])
    print(json.dumps(out))
