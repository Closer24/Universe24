"""The credits per interval of an eq1_run record and the levels per Node before each bottom against the bottom's shortfall from Gamma = 1000; the light's velocity at the origin at the bottoms."""
import json, sys
d = json.load(open(sys.argv[1]))
rows, s = d['rows'], d['summary']
print('bottoms', s['bottoms'], 'tops', s['tops'], 'credits', s['credits'])
nodes = 27 if 'pair_3' in s['world'] else 125
for r in rows:
    if r['credits']:
        print('  i', r['i'], 'credits', r['credits'], 'levels', r['credit levels'], 'beats', r['credit beats'], 'lines', r['credit lines'], 'X mean', r['X mean'], 'v light', r['v light at origin'])
for b_i, b_x in s['bottoms']:
    levels = sum(r['credits'] * r['credit levels'][0] for r in rows if r['i'] <= b_i and r['credits'] and len(r['credit levels']) == 1)
    print('bottom', b_i, 'X', b_x, 'shortfall', 1000 - b_x, 'credits before', sum(r['credits'] for r in rows if r['i'] <= b_i), 'levels per Node before', levels // nodes, 'v light at the bottom', [r['v light at origin'] for r in rows if r['i'] == b_i])
print('v light at the end', rows[-1]['v light at origin'], 'X mean at the end', rows[-1]['X mean'])
