"""mv1 (3d): the collision. Two electron packets (row 1) 4 Links apart laid toward each other (+k and -k along x, k = pi/2) on the 9-cube, 60 intervals, at the held vacuum and with the sea alone: the share's profile along x (summed over y and z, in quanta div and the two peaks' positions), the row's lattice momentum P_x before, through and after, the births and body credits with the toy's dP bookings (the momentum in the clicks), the run back. Usage: python collision_mv1.py <hold|sea> <out.json>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)
import numpy as np
import lean_mv1
from lean_mv1 import Lean
from measure_mv1 import shares, momentum
HERE = os.path.dirname(os.path.abspath(__file__))
UNI = json.load(open(os.path.join(HERE, 'toy', 'universe_middle.json')))
mode = sys.argv[1]
world = {"universe": "universe_middle.json", "shape": [9, 9, 9], "intervals": 60, "seed": [{"lay": "sea", "row": 0}, {"lay": "at", "row": 1, "centre": [2, 4, 4], "width": 2, "quanta": 125, "wave": [1571, 0, 0]}, {"lay": "at", "row": 1, "centre": [6, 4, 4], "width": 2, "quanta": 125, "wave": [-1571, 0, 0]}]}
if mode == 'hold': world['control'] = {"well": {"at": [0, 0, 0], "levels": 0, "radius": 1, "held": True}}
b = Lean(UNI, world); r = b.records()[0]; unit = b.units[0]
rows = []; hashes = []
def reading():
    sh = shares(b, r); prof = [int(sum(int(x) for x in sh[i].reshape(-1))) for i in range(b.cube)]
    total = sum(prof); peaks = sorted(range(b.cube), key=lambda i: -prof[i])[:2]
    light = b.row(2, gap=0)
    return {'i': b.interval, 'profile x (share in thousandths of the unit)': [(1000 * p) // unit for p in prof], 'count': total // unit, 'two peaks x': sorted(peaks), 'P row': momentum(b, r), 'P light': momentum(b, light), 'births': b.counts['births'], 'body clicks': b.counts['body_clicks']}
rows.append(reading())
for t in range(60):
    if t >= 50: hashes.append(b.state_hash())
    b.step(); rows.append(reading())
births = [e for e in b.log if e['event'] == 'birth']; credits = [e for e in b.log if e['event'] == 'credit']
sum_dp_take = [sum(int(e['dP_take'][a]) for e in births + credits) for a in range(3)]; sum_dp_lay = [sum(int(e['dP_lay'][a]) for e in births) for a in range(3)]
exact = 0
for k in range(10):
    b.step_back(); exact += (b.state_hash() == hashes[9 - k])
out = {'world': world, 'rows': rows, 'births': len(births), 'credits': len(credits), 'sum dP_take over clicks': sum_dp_take, 'sum dP_lay over births': sum_dp_lay, 'run back': {'intervals': 10, 'exact': exact}, 'lays': [e for e in b.log if e['event'] == 'lay'], 'first births': births[:5], 'first credits': credits[:3]}
json.dump(out, open(sys.argv[2], 'w'), default=str)
brief = {'mode': mode, 'run back': out['run back'], 'births': len(births), 'credits': len(credits), 'sum dP_take': sum_dp_take, 'sum dP_lay': sum_dp_lay, 'lays': [(l['amplitude'], l['share'] // l['unit'], l['wave']) for l in out['lays']]}
brief['profiles'] = [(row['i'], row['profile x (share in thousandths of the unit)'], row['two peaks x'], row['count'], row['P row'][0], row['P light'][0]) for row in rows if row['i'] in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 40, 50, 60)]
print(json.dumps(brief, default=str))
