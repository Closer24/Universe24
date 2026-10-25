"""pc2, item 3: the body's rotation per interval read at its centre Node from the plane's two levels (the law's own reading, a rational: cos omega = (z_now . z_before) / |z_before|^2 with z = (re, im)), against the standing law's rotation at the Node's content (1 - cos omega_c = (1 - num / den) (p_0 / Gamma)^2) and against the toy's crossing count (the credit's 'beat'); the neighbours' share of the arrivals (SUM R_j m_j against (2 w - D) a_now) at the centre, to see what rotates the body at depth.
Usage: PYTHONPATH=src python body_rotation.py <world.json> <intervals> <x,y,z> [rec]. Integers only; thousandths."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)
import numpy as np
from lean_carried import Lean, load_world
import pc2_paces as paces

universe, world = load_world(sys.argv[1]); n = int(sys.argv[2]); at = tuple(int(x) for x in sys.argv[3].split(',')); rec = int(sys.argv[4]) if len(sys.argv) > 4 else 2
MIL = 1000
b = Lean(universe, world)
r_ = b.records()[rec]; num, den = r_.pair
rows = []
for t in range(n):
    b.step()
    if b.interval % 4 == 0 or b.interval >= n - 6:
        re, im = r_.lines
        zn = (int(re.now[at]), int(im.now[at])); zb = (int(re.before[at]), int(im.before[at]))
        dot = zn[0] * zb[0] + zn[1] * zb[1]; nb = zb[0] ** 2 + zb[1] ** 2; nn = zn[0] ** 2 + zn[1] ** 2
        c = int(b.content()[at]); p0 = int(paces.clock(b.gamma, c))
        # the standing law: cos omega_c = 1 - (den - num) p0^2 / (den Gamma^2), in thousandths
        cos_law = MIL - (den - num) * p0 * p0 * MIL // (den * b.gamma * b.gamma)
        cos_read = dot * MIL // nb if nb else None
        # the neighbours' part: the mean of the six neighbours' re level over the centre's, thousandths
        neigh = [int(re.now[tuple((at[a] + (s if a == ax else 0)) % b.cube for a in range(3))]) for ax, s in ((0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1))]
        rows.append({'i': b.interval, 'content': c, 'p0': p0, 'cos omega read (thousandths)': cos_read, 'cos omega standing law (thousandths)': cos_law, '|z| now bits, before bits': [nn.bit_length() // 2, nb.bit_length() // 2], 're now, re before': [zn[0], zb[0]], 'neighbours re now / centre re now (thousandths)': [x * MIL // zn[0] if zn[0] else None for x in neigh], 'beat counted at the Node': int(b.beats[rec][at]), 'sign level': int(b.row(4).lines[0].now[at])})
for row in rows: print(json.dumps(row))
