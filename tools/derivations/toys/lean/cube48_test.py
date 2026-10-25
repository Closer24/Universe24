"""The 48 on the lean toy: the toy run from a seed and from each of its 48 images (the signed permutations of the axes about the origin), the births compared through the image (interval, the take's Node, the lift, the - child's Node, the + child's Node), the whole volume and light rows compared through the image at the last interval.
Usage: python cube48_test.py <den> <cube> <intervals> <mode> [extra]   mode: node | link | current;   extra: x,y,z of the one quantum more (the seed's asymmetry)."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_full import Lean


def signed_permutations():
    axes = range(3)
    return [np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes]) for pi in itertools.permutations(axes) for s in itertools.product((1, -1), repeat=3)]


def image(m, node, cube):
    v = m @ np.array(node, dtype=int)
    return tuple(int(x) % cube for x in v)


def events(b):
    return sorted((e['i'], tuple(e['node']), e['line_pair'], tuple(e['minus']), tuple(e['plus'])) for e in b.log if e['event'] == 'birth')


def mapped(evs, m, cube):
    return sorted((i, image(m, at, cube), s_, image(m, mi, cube), image(m, pl, cube)) for i, at, s_, mi, pl in evs)


def run(den, cube, n, mode, extra):
    link = True if mode == 'link' else ('current' if mode == 'current' else False)
    b = Lean(den, cube, link_birth=link, seed_extra=extra)
    for _ in range(n): b.step()
    return b


den, cube, n, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
extra = tuple(int(x) for x in sys.argv[5].split(',')) if len(sys.argv) > 5 else None
base = run(den, cube, n, mode, extra)
evs = events(base)
print({'mode': mode, 'extra': extra, 'intervals': n, 'births': len(evs), 'refused orientation': base.counts['refused_orientation'], 'refused lay': base.counts['refused_lay'], 'refused stop': base.counts['refused_stop'], 'turns': base.counts['turns']})
held = 0; apart = []
for m in signed_permutations():
    img_extra = None if extra is None else image(m, extra, cube)
    other = run(den, cube, n, mode, img_extra)
    same_events = events(other) == mapped(evs, m, cube)
    # the rows through the image: the volume's and the light's time lines at every Node
    same_rows = True
    for line_b, line_o in ((base.vol, other.vol), (base.light, other.light)):
        for at in np.ndindex(cube, cube, cube):
            if int(line_b.now[at]) != int(line_o.now[image(m, at, cube)]) or int(line_b.before[at]) != int(line_o.before[image(m, at, cube)]): same_rows = False; break
        if not same_rows: break
    if same_events and same_rows: held += 1
    else: apart.append((m.tolist(), 'events' if not same_events else 'rows'))
print({'images holding': held, 'of': 48, 'apart': apart[:6]})
