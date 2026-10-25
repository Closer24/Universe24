import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_full import Lean
b = Lean(15162856759112389, 5)
at = (2, 2, 2); at2 = (0, 0, 0)
for t in range(660):
    vb, vn = int(b.vol.before[at]), int(b.vol.now[at])
    b.step()
    if b.interval >= 648 or b.interval in (100, 200, 300, 400, 500):
        print(b.interval, 'turned', int(b.turned.sum()), 'node', at, 'vol before/now (start)', vb, vn, '-> now/before after', int(b.vol.now[at]), int(b.vol.before[at]), 'light', int(b.light.now[at]), int(b.light.before[at]), 'vol_wr0', int(b.vol_wr[0][at]), 'planes re0', int(b.planes[0][0].now[at]), int(b.planes[0][0].before[at]), 'light share quanta', int(b.share(b.light, b.rule((b.den, b.den), b.content(), b.link_factors()))[at]) // b.unit_light)
