import sys, copy, json
sys.set_int_max_str_digits(0)
import numpy as np
from event_universe.interval import Interval
from event_universe.rows import CARRIER
from tests.laws import node_of
node = node_of("world_hole.json")
found = {"shear numerator nonzero node-intervals per pair": [0, 0, 0], "flux numerator nonzero node-intervals per axis": [0, 0, 0], "shear wr moved off its half at 20 (nodes per pair)": [0, 0, 0], "largest |shear numerator| over the write wall, thousandths": [0, 0, 0], "write wall of the nine": None}
for _ in range(20):
    pre = copy.deepcopy(node); itv = Interval(pre, 1); itv.walled_act(); itv.forces(); itv.kicks()
    p02 = itv.p0 * itv.p0
    for a in range(3):
        found["shear numerator nonzero node-intervals per pair"][a] += int(sum(1 for x in (itv.shear[a] * p02).reshape(-1) if int(x) != 0))
        found["flux numerator nonzero node-intervals per axis"][a] += int(sum(1 for x in (itv.flux[a] * p02).reshape(-1) if int(x) != 0))
        ww = itv.carrier.lines[7].wwall
        found["largest |shear numerator| over the write wall, thousandths"][a] = max(found["largest |shear numerator| over the write wall, thousandths"][a], max(abs(int(x)) * 1000 // ww for x in (itv.shear[a] * p02).reshape(-1)))
    node.step()
lines = node.row(CARRIER).lines
found["write wall of the nine"] = int(lines[1].wwall)
for a in range(3):
    found["shear wr moved off its half at 20 (nodes per pair)"][a] = int(sum(1 for x in lines[7 + a].wr.reshape(-1) if int(x) != lines[7 + a].wwall // 2))
print(json.dumps(found)); json.dump(found, open(sys.argv[1], "w"), indent=1)
