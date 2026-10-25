"""The reach of the Link birth's orientation on the lean toy (ALGEBRA.md, Only local; the owner's locality law of 2026-10-25): two boards run alike to an interval in the mode named, one Node's light level changed on one of them, both run one interval; the births of that interval compared Link by Link, each Link named by the least torus L1 distance of its two ends from the changed Node; the births on Links with both ends at distance 2 or more must be equal bit for bit (the current reads the two ends; the twist reads the two ends and their transverse neighbours, one Link from each end; the shares read the ends' frames), and the lines' differences by distance as David's reach_test reports them.
Usage: python pa2_reach.py <world.json> <cube> <intervals before the change> <x,y,z> <mode> <levels added> <out.json>"""
import sys, os, json, copy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'toy'))
import numpy as np
from lean_pa2 import LeanPa2
from lean_full import load_world

sys.set_int_max_str_digits(0)


def distance(node, origin, cube):
    return sum(min(abs(node[k] - origin[k]), cube - abs(node[k] - origin[k])) for k in range(3))


def births_of(b, interval):
    found = {}
    for e in b.log:
        if e['event'] == 'birth' and e['i'] == interval:
            key = (tuple(e['minus']), tuple(e['plus'])) if tuple(e['minus']) < tuple(e['plus']) else (tuple(e['plus']), tuple(e['minus']))
            found[key] = (e['line_pair'], tuple(e['minus']), tuple(e['plus']), e['taken'], e['booked'], e['levels'], e['amplitude'])
    refused = {}
    for e in b.log:
        if e['event'] == 'refused' and e['i'] == interval and 'link' in e:
            key = tuple(sorted((tuple(e['node']), tuple(e['link']))))
            refused[key] = e['cause']
    return found, refused


def main():
    world_path, cube, n, p, mode, added, out_path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), tuple(int(x) for x in sys.argv[4].split(',')), sys.argv[5], int(sys.argv[6]), sys.argv[7]
    universe, world = load_world(world_path); world = copy.deepcopy(world); world['shape'] = [cube, cube, cube]
    a = LeanPa2(universe, world, mode)
    for _ in range(n): a.step()
    b = copy.deepcopy(a)
    b.light.now[p] = b.light.now[p] + added
    a.step(); b.step()
    fa, ra = births_of(a, a.interval); fb, rb = births_of(b, b.interval)
    links = set(fa) | set(fb) | set(ra) | set(rb)
    by = {}
    for link in links:
        d = min(distance(link[0], p, cube), distance(link[1], p, cube))
        same = fa.get(link) == fb.get(link) and ra.get(link) == rb.get(link)
        row = by.setdefault(d, {'links': 0, 'equal': 0, 'apart': 0, 'births a': 0, 'births b': 0})
        row['links'] += 1; row['equal' if same else 'apart'] += 1; row['births a'] += link in fa; row['births b'] += link in fb
    far_apart = max([d for d, r in by.items() if r['apart']], default=None)
    # the lines' differences by distance (David's reading)
    diffs = {}
    for r, (ra_, rb_) in enumerate(zip(a.rows(), b.rows())):
        for k, (la, lb) in enumerate(zip(ra_, rb_)):
            for slot in ('now', 'before', 'rem', 'wr'):
                xa, xb = getattr(la, slot), getattr(lb, slot)
                if xa is None: continue
                for node in zip(*np.nonzero(np.asarray(xa != xb))):
                    node = tuple(int(x) for x in node); d = distance(node, p, cube)
                    diffs[d] = diffs.get(d, 0) + 1
    result = {'world': world_path, 'cube': cube, 'mode': mode, 'changed node': list(p), 'levels added': added, 'interval of the change': a.interval,
              'births this interval a/b': [len(fa), len(fb)], 'links compared by distance of the nearer end': {str(d): r for d, r in sorted(by.items())},
              'farthest distance with a birth apart': far_apart, 'links at distance >= 2 equal / of': [sum(r['equal'] for d, r in by.items() if d >= 2), sum(r['links'] for d, r in by.items() if d >= 2)],
              'lines differing by distance (the step reaches one Link, the lays the Link ends)': {str(d): c for d, c in sorted(diffs.items())}}
    json.dump(result, open(out_path, 'w'), indent=1); print(json.dumps(result, indent=1))


if __name__ == '__main__':
    main()
