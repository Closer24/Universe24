"""sr2: the one-Link reach of the spinor row's step (the Pauli term's Phi read), forward and backward: two boards run alike,
one odd line (A_x of the shape-4 row, the field) changed at one Node by one level on one of them, both run one
interval; every line of every row compared at every Node; the differing Nodes by their torus distance from the changed
Node (1 expected: the six neighbours read the odd line through their Links, the Node itself through its own level; a
Node two Links away bit for bit). The same with the light's level changed (the toy's test).
Usage: python sr2_reach.py <world.json> <intervals before the change> <x,y,z>
"""
import sys, os, copy, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_sr2 import Lean, load_world


def distance(node, origin, cube): return sum(min(abs(node[k] - origin[k]), cube - abs(node[k] - origin[k])) for k in range(3))


def differences(a, b, p):
    found = []
    for r, (ra, rb) in enumerate(zip(a.rows(), b.rows())):
        for k, (la, lb) in enumerate(zip(ra, rb)):
            for slot in ('now', 'before', 'rem', 'wr'):
                xa, xb = getattr(la, slot), getattr(lb, slot)
                if xa is None: continue
                for node in zip(*np.nonzero(np.asarray(xa != xb))):
                    node = tuple(int(x) for x in node); found.append((distance(node, p, a.cube), r, k, slot, node))
    return found


def by_distance(found):
    by = {}
    for d, r, k, slot, node in found: by.setdefault(d, set()).add((r, k, slot))
    return {str(d): sorted(v) for d, v in sorted(by.items())}, (max(by) if by else None)


def main():
    universe, world = load_world(sys.argv[1]); n = int(sys.argv[2]); p = tuple(int(x) for x in sys.argv[3].split(','))
    out = {'rows (index: shape)': None}
    a = Lean(universe, world)
    for _ in range(n): a.step()
    out['rows (index: shape)'] = {k: (r.shape, 'wall' if r.wall is not None else r.gap) for k, r in enumerate(a.rows_)}
    for label, change in (('odd line A_x + 1 at the Node', lambda bd: setattr(bd.row(4).lines[1], 'now', bd.row(4).lines[1].now) or bd.row(4).lines[1].now.__setitem__(p, bd.row(4).lines[1].now[p] + 1)), ('light + 1 at the Node', lambda bd: bd.row(2, gap=0).lines[0].now.__setitem__(p, bd.row(2, gap=0).lines[0].now[p] + 1))):
        b = copy.deepcopy(a); change(b)
        assert len(differences(a, b, p)) == 1
        a2, b2 = copy.deepcopy(a), b
        a2.step(); b2.step()
        by, far = by_distance(differences(a2, b2, p))
        out[label + ': forward one interval'] = {'farthest distance': far, 'by distance': by, 'turns a/b': [int(a2.turned.sum()), int(b2.turned.sum())], 'births a/b': [a2.counts['births'], b2.counts['births']]}
        # backward: from one post-state, the same change, both run back one interval
        a3 = copy.deepcopy(a2); b3 = copy.deepcopy(a2); change(b3)
        a3.step_back(); b3.step_back()
        by, far = by_distance(differences(a3, b3, p))
        out[label + ': backward one interval'] = {'farthest distance': far, 'by distance': by}
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
