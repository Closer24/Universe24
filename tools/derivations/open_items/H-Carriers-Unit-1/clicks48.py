"""pm1's 48 on the clicks under the flagged copy (re-based from the kit's clicks_48_example.py, pa2's, onto the engine): the world run
from its seed and from each of its 48 images (the signed permutations about the origin, on the torus); every credit line (a birth: the
interval, the plane, the two children's Nodes; a body's credit: the interval, the Node, the row, the sense) pulled back through the image
and compared with the seed's: equal / the senses exchanged (every sense flipped) / apart. Usage: python clicks48.py <world.json> <intervals> <out.json>"""
import copy, itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'src_pm1'))
import numpy as np
from event_universe import readings
from event_universe.loader.world import read_world
from event_universe.node import Node

sys.set_int_max_str_digits(0)
where, n, out_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
world0 = json.loads(open(where).read())
readings.WEIGHT = world0.pop('pm1_weight', 'default')
universe = json.loads(open(os.path.join(os.path.dirname(where), world0['universe'])).read())
world0['intervals'] = n
cube = int(world0['shape'][0])
mats = [np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)]) for pi in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]

def image(m, node):
    return tuple(int(x) % cube for x in (m @ np.array(node, dtype=int)))

def record(world):
    read_world(dict(world), universe)
    node = Node(universe, world)
    for _ in range(n):
        node.step()
    found = []
    for e in node.log:
        if e['event'] == 'birth':
            found.append(('birth', e['i'], e['line_pair'], tuple(e['minus']), tuple(e['plus'])))
        elif e['event'] == 'credit':
            found.append(('credit', e['i'], e['line'], tuple(e['node']), e['sense']))
    return found, dict(node.counts)

base, counts0 = record(copy.deepcopy(world0))
print(json.dumps({'seed': counts0, 'lines': len(base)}), flush=True)
results = {'equal': 0, 'senses_exchanged': 0, 'apart': 0, 'per_image': []}
chosen = [int(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else list(range(48))
for k, m in enumerate(mats):
    if k not in chosen:
        continue
    w = copy.deepcopy(world0)
    for lay in w.get('seed', []):
        for key in ('at', 'centre'):
            if key in lay:
                lay[key] = list(image(m, tuple(lay[key])))
    found, counts = record(w)
    inv = np.round(np.linalg.inv(m)).astype(int)
    back = []
    for e in found:
        if e[0] == 'birth':
            back.append((e[0], e[1], e[2], image(inv, e[3]), image(inv, e[4])))
        else:
            back.append((e[0], e[1], e[2], image(inv, e[3]), e[4]))
    det = int(round(np.linalg.det(m)))
    if sorted(back) == sorted(base):
        verdict = 'equal'
    else:
        flipped = [(e[0], e[1], e[2], e[4], e[3]) if e[0] == 'birth' else (e[0], e[1], e[2], e[3], -e[4]) for e in back]
        verdict = 'senses_exchanged' if sorted(flipped) == sorted(base) else 'apart'
    results[verdict] += 1
    results['per_image'].append({'k': k, 'det': det, 'verdict': verdict, 'births': counts['births'], 'body_clicks': counts['body_clicks']})
    print(json.dumps(results['per_image'][-1]), flush=True)
results['seed_counts'] = counts0
json.dump(results, open(out_path, 'w'))
print(json.dumps({k: v for k, v in results.items() if k != 'per_image'}))
