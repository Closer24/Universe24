# pc2: David's test on the flagged copy lean_carried.py (the import the one change)
"""The one-Link reach on the lean toy, forward and backward (the owner's locality law of 2026-10-25): two boards run alike to an interval, one Node's level changed on one of them, both run one interval in the direction, every line compared at every Node; the Nodes that differ are reported by their lattice distance from the changed Node (the torus's L1 distance), the farthest first, the lines named by their row and the acts that reach them (the step: the rotate and the writes read the six Ports; the close: a Link's meeting reads both ends' shares, each a one-Link read, and lays at both ends).
Usage: python reach_test.py <world.json> <intervals before the change> <x,y,z> [levels added to the light at the Node, default 1]"""
import sys, os, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_carried import Lean, load_world

universe, world = load_world(sys.argv[1]); n = int(sys.argv[2])
p = tuple(int(x) for x in sys.argv[3].split(',')); added = int(sys.argv[4]) if len(sys.argv) > 4 else 1
a = Lean(universe, world)
for _ in range(n): a.step()
b = copy.deepcopy(a)


def distance(node, origin, cube):
    return sum(min(abs(node[k] - origin[k]), cube - abs(node[k] - origin[k])) for k in range(3))


def differences(a, b):
    """Every (row, line, slot, Node) where the two boards differ, with the Node's distance from the changed Node."""
    found = []
    for r, (ra, rb) in enumerate(zip(a.rows(), b.rows())):
        for k, (la, lb) in enumerate(zip(ra, rb)):
            for slot in ('now', 'before', 'rem', 'wr'):
                xa, xb = getattr(la, slot), getattr(lb, slot)
                if xa is None: continue
                for node in zip(*np.nonzero(np.asarray(xa != xb))):
                    node = tuple(int(x) for x in node)
                    found.append((distance(node, p, a.cube), r, k, slot, node))
    return found


def report(label, found, boards):
    by = {}
    for d, r, k, slot, node in found: by.setdefault(d, set()).add((r, k, slot))
    far = max(by) if by else None
    print({label: {'differing lines': len(found), 'farthest distance': far, 'by distance': {d: sorted(v) for d, v in sorted(by.items())},
                   'turns a/b': [int(x.turned.sum()) for x in boards], 'births a/b': [x.counts['births'] for x in boards], 'log lines this interval a/b': [len(x.log) - x.stack[-1]['log_from'] for x in boards]}})


z = b.row(2, gap=0).lines[0]; z.now[p] = z.now[p] + added
assert len(differences(a, b)) == 1
a.step(); b.step()
report('forward one interval', differences(a, b), (a, b))
# backward: from one post-state, the same change at the Node, both run back one interval
a2 = copy.deepcopy(a); b2 = copy.deepcopy(a)
z2 = b2.row(2, gap=0).lines[0]; z2.now[p] = z2.now[p] + added
a2.step_back(); b2.step_back()
found = differences(a2, b2)
by = {}
for d, r, k, slot, node in found: by.setdefault(d, set()).add((r, k, slot))
print({'backward one interval': {'differing lines': len(found), 'farthest distance': max(by) if by else None, 'by distance': {d: sorted(v) for d, v in sorted(by.items())}}})
print({'rows': 'row 0 the phase row; rows 1..%d the planes (line 0 re, 1 im); row %d the massless row; row %d the sign row (0 time line, 1..3 odd lines); row %d the volume row (0 time line, 1..3 axis lines)' % (2 * a.nl, 2 * a.nl + 1, 2 * a.nl + 2, 2 * a.nl + 3)})
