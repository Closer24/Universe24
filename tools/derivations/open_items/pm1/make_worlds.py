"""pm1's world copies: the engine's worlds with the key pm1_weight (link / vacuum / clock) and the intervals named; the default copies carry no key."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, 'worlds')
def write(src, name, intervals, weight=None, shape=None):
    w = json.loads(open(os.path.join(W, src)).read())
    w['intervals'] = intervals
    if shape: w['shape'] = shape
    if weight: w['pm1_weight'] = weight
    json.dump(w, open(os.path.join(W, name), 'w'))
for wt in (None, 'link', 'vacuum', 'clock'):
    tag = wt or 'default'
    write('world_node.json', f'node100_{tag}.json', 100, wt)
    write('world_chiral.json', f'chiral300_{tag}.json', 300, wt)
    write('world_bodies.json', f'bodies120_{tag}.json', 120, wt)
    write('world_hole.json', f'hole60_{tag}.json', 60, wt)
write('world_node.json', 'node20_default.json', 20)
write('world_chiral.json', 'chiral2400_default.json', 2400)
write('world_chiral.json', 'chiral2400_link.json', 2400, 'link')
write('world_collapse_800.json', 'collapse800_400_default.json', 400)
write('world_collapse_800.json', 'collapse800_400_link.json', 400, 'link')
print('written')
