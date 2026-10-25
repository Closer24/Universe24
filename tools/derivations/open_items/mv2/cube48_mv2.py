"""The 48 on the moving lay (mv2's copy of David's cube48_test.py): the toy run from a seed and from each of its 48 images (the signed permutations of the
axes about the origin), the wave number carried as a vector (h' = m h: the sine of the half-angle is odd in k, so the image of the lay with k is the lay with
the image's k), the births compared through the image, and at the last interval EVERY row's lines compared through the image: the volume row, the light
row, and the planes (re and im, now and before). Usage: python cube48_mv2.py <world.json> <cube> <intervals>"""
import sys, os, itertools, copy, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_mv2 import Lean, load_world

sys.set_int_max_str_digits(0)


def signed_permutations():
    axes = range(3)
    return [np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes]) for pi in itertools.permutations(axes) for s in itertools.product((1, -1), repeat=3)]


def image(m, node, cube):
    v = m @ np.array(node, dtype=int)
    return tuple(int(x) % cube for x in v)


def vector_image(m, h):
    v = m @ np.array([int(x) for x in h], dtype=object)
    return [int(x) for x in v]


def events(b):
    return sorted((e['i'], tuple(e['node']), e['line_pair'], tuple(e['minus']), tuple(e['plus'])) for e in b.log if e['event'] == 'birth')


def mapped(evs, m, cube):
    return sorted((i, image(m, at, cube), s_, image(m, mi, cube), image(m, pl, cube)) for i, at, s_, mi, pl in evs)


def world_image(world, m, cube):
    w = copy.deepcopy(world); w['shape'] = [cube, cube, cube]
    for lay in w.get('seed', []):
        for key in ('at', 'centre'):
            if key in lay: lay[key] = list(image(m, tuple(lay[key]), cube))
        if 'wave' in lay: lay['wave'] = vector_image(m, lay['wave'])
    return w


def run(universe, world, n):
    b = Lean(universe, world)
    for _ in range(n): b.step()
    return b


def rows_equal(base, other, m, cube):
    """Every line of every row compared through the image at every Node, now and before, the lines turned as the row's shape turns them (the cube's 48 on a row): a row's first line a scalar; the three axis lines of the shape-10 row (the tensions, even) and of the shape-4 row (the odd lines, odd) a vector, line a of the base against line pi(a) of the image with the sign for the odd lines; the shape-10 row's six shear lines compared as they stand (zero on these boards); a plane's two lines scalars. Returns the unequal entries per row shape."""
    unequal = {}
    perm = [int(np.nonzero(m[:, a])[0][0]) for a in range(3)]  # the image axis of the base axis a
    sign = [int(m[perm[a], a]) for a in range(3)]
    for rb, ro in zip(base.rows_, other.rows_):
        key = 'shape %d%s' % (rb.shape, '' if rb.gap is None else ' gap %d' % min(rb.gap, 1))
        for k, lb in enumerate(rb.lines):
            if rb.shape in (10, 4) and 1 <= k <= 3:
                a = k - 1; lo = ro.lines[1 + perm[a]]; s = sign[a] if rb.shape == 4 else 1
            else:
                lo = ro.lines[k]; s = 1
            for at in np.ndindex(cube, cube, cube):
                im_ = image(m, at, cube)
                unequal[key] = unequal.get(key, 0) + (int(lb.now[at]) != s * int(lo.now[im_])) + (int(lb.before[at]) != s * int(lo.before[im_]))
    return {k: v for k, v in unequal.items() if v}


universe, world0 = load_world(sys.argv[1]); cube, n = int(sys.argv[2]), int(sys.argv[3])
identity = np.eye(3, dtype=int)
base = run(universe, world_image(world0, identity, cube), n)
evs = events(base)
print(json.dumps({'seed': world0.get('seed'), 'cube': cube, 'intervals': n, 'births': len(evs), 'credits': sum(1 for e in base.log if e['event'] == 'credit'), 'turns': base.counts['turns'], 'P base': None}))
held = 0; apart = []
for m in signed_permutations():
    other = run(universe, world_image(world0, m, cube), n)
    same_events = events(other) == mapped(evs, m, cube)
    unequal = rows_equal(base, other, m, cube)
    if same_events and not unequal: held += 1
    else: apart.append({'image': m.tolist(), 'events equal': same_events, 'unequal entries': unequal})
print(json.dumps({'images holding (births through the image, every line of every row through the image)': held, 'of': 48, 'apart': apart[:6]}))
