"""The 48 on the clicks for fd2's copy against David's (the kit's rule 5, pa2's reading without LeanPa2's extra fields): the world
run from its seed and from each of its 48 images (the signed permutations about the origin) with both classes; per image the two
classes' records (births: interval, the take's Node, the lift, the two children's Nodes, taken, booked, levels; credits: interval,
Node, line, sense, beat, taken, levels) must be equal (David against fd2), and the image's record is compared through the image to
the base record: equal, equal with the senses exchanged, or apart.
Usage: python fd2_48.py <world.json> <cube> <intervals> <out.json>"""
import sys, os, json, copy, itertools, importlib.util, time
HERE = os.path.dirname(os.path.abspath(__file__))
import numpy as np
sys.set_int_max_str_digits(0)


def load(name, folder):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, folder, 'lean_full.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def signed_permutations():
    axes = range(3)
    return [np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes]) for pi in itertools.permutations(axes) for s in itertools.product((1, -1), repeat=3)]


def image(m, node, cube):
    v = m @ np.array(node, dtype=int)
    return tuple(int(x) % cube for x in v)


def det3(m):
    """The determinant of a 3 x 3 integer matrix in integers (the signed permutations' +1 or -1), no float."""
    a = [[int(x) for x in row] for row in m]
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0]) + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def world_image(world, m, cube):
    w = copy.deepcopy(world); w['shape'] = [cube, cube, cube]
    for lay in w.get('seed', []):
        for key in ('at', 'centre'):
            if key in lay: lay[key] = list(image(m, tuple(lay[key]), cube))
    return w


def records(b, m, cube, conj):
    births = []; credits = []
    for e in b.log:
        if e['event'] == 'birth':
            mi, pl = image(m, tuple(e['minus']), cube), image(m, tuple(e['plus']), cube)
            if conj: mi, pl = pl, mi
            births.append((e['i'], image(m, tuple(e['node']), cube), e['line_pair'], mi, pl, e['taken'], e['booked'], e['levels']))
        elif e['event'] == 'credit':
            sense = -e['sense'] if conj else e['sense']
            credits.append((e['i'], image(m, tuple(e['node']), cube), e['line'], sense, e['beat'], e['taken'], e['levels']))
    return sorted(births), sorted(credits)


def main():
    world_path, cube, n, out_path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    david = load('lean_david', 'toy_david'); fd2 = load('lean_fd2', 'toy_fd2')
    universe, world0 = david.load_world(world_path)
    t0 = time.monotonic_ns()
    identity = np.eye(3, dtype=int)
    def run(mod, m):
        b = mod.Lean(universe, world_image(world0, m, cube))
        for _ in range(n): b.step()
        return b
    base_d = run(david, identity); base_f = run(fd2, identity)
    same_base = records(base_d, identity, cube, False) == records(base_f, identity, cube, False) and base_d.state_hash() == base_f.state_hash()
    def tally():
        return {'equal': 0, 'equal rotations': 0, 'equal reflections': 0, 'senses exchanged': 0, 'exchanged rotations': 0, 'exchanged reflections': 0, 'apart': 0}
    def classify(t, ob, mb, xb, det):
        if ob == mb: t['equal'] += 1; t['equal rotations' if det == 1 else 'equal reflections'] += 1
        elif ob == xb: t['senses exchanged'] += 1; t['exchanged rotations' if det == 1 else 'exchanged reflections'] += 1
        else: t['apart'] += 1
    def takes_multiset(b, m):  # pa2's reading of the credits: the takes per (interval, Node) as a multiset (two records closing at one Node take in the records' index order, a label), the births whole
        births, credits = records(b, m, cube, False)
        return births, sorted((i, node, taken, levels) for (i, node, _line, _sense, _beat, taken, levels) in credits)
    full = tally(); births_only = tally(); multiset = tally(); classes_equal = 0
    for m in signed_permutations():
        od = run(david, m); of = run(fd2, m)
        classes_equal += (records(od, identity, cube, False) == records(of, identity, cube, False) and od.state_hash() == of.state_hash())
        ob = records(od, identity, cube, False); mb = records(base_d, m, cube, False); xb = records(base_d, m, cube, True)
        det = det3(m)
        classify(full, ob, mb, xb, det)
        classify(births_only, ob[0], mb[0], xb[0], det)
        classify(multiset, takes_multiset(od, identity), takes_multiset(base_d, m), (xb[0], takes_multiset(base_d, m)[1]), det)
    result = {'world': os.path.basename(world_path), 'cube': cube, 'intervals': n, 'base: births, credits': [len(records(base_d, identity, cube, False)[0]), len(records(base_d, identity, cube, False)[1])],
              'base record and state equal (David against fd2)': same_base, 'images with David and fd2 equal (records and state hash)': [classes_equal, 48],
              'the 48 on the clicks (David): births and credits with line, sense, beat, take': full,
              'the 48 on the births alone': births_only,
              'the 48 on the births and the takes as a multiset per (interval, Node) (pa2\'s reading)': multiset,
              'seconds': (time.monotonic_ns() - t0) // 10 ** 9}
    json.dump(result, open(out_path, 'w'), indent=1); print(json.dumps(result, indent=1))


if __name__ == '__main__':
    main()
