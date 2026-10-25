"""The 48 on the lean toy: the toy run from a seed and from each of its 48 images (the signed permutations of the axes about the origin), the births compared through the image (interval, the take's Node, the lift, the - child's Node, the + child's Node), the whole volume and light rows compared through the image at the last interval.
Usage: python cube48_test.py <world.json> <cube> <intervals> <mode: current|link|node>   (the world's shape replaced by the cube; the seed's 'at' entries carried through each image)"""
import sys, os, itertools, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_full import Lean, load_world


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


def world_image(world, m, cube):
    w = copy.deepcopy(world); w['shape'] = [cube, cube, cube]
    for lay in w.get('seed', []):
        if 'at' in lay: lay['at'] = list(image(m, tuple(lay['at']), cube))
        if 'hole' in lay: lay['hole'] = list(image(m, tuple(lay['hole']), cube))
    return w


def run(universe, world, n, link):
    b = Lean(universe, world, link_birth=link)
    for _ in range(n): b.step()
    return b


universe, world0 = load_world(sys.argv[1]); cube, n, mode = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
link = {'current': 'current', 'link': True, 'node': False}[mode]
identity = np.eye(3, dtype=int)
base = run(universe, world_image(world0, identity, cube), n, link)
evs = events(base)
print({'mode': mode, 'seed': world0.get('seed'), 'cube': cube, 'intervals': n, 'births': len(evs), 'refused orientation': base.counts['refused_orientation'], 'refused lay': base.counts['refused_lay'], 'refused stop': base.counts['refused_stop'], 'turns': base.counts['turns']})
held = 0; apart = []
for m in signed_permutations():
    other = run(universe, world_image(world0, m, cube), n, link)
    same_events = events(other) == mapped(evs, m, cube)
    same_rows = True
    for line_b, line_o in ((base.vol, other.vol), (base.light, other.light)):
        for at in np.ndindex(cube, cube, cube):
            if int(line_b.now[at]) != int(line_o.now[image(m, at, cube)]) or int(line_b.before[at]) != int(line_o.before[image(m, at, cube)]): same_rows = False; break
        if not same_rows: break
    if same_events and same_rows: held += 1
    else: apart.append((m.tolist(), 'events' if not same_events else 'rows'))
print({'images holding': held, 'of': 48, 'apart': apart[:6]})
