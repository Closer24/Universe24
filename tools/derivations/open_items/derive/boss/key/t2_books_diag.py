"""Probe 2's diagnostic: the light's and the time gear's leapfrog forms tick by tick, against lam = ell key / 2.

usage: python3 -I t2_books_diag.py > t2_books_diag.txt

One light train, the standing wave (1, 0, -1, 0) at amplitude 600 along the fastest axis of the 4 x 4 x 4 board
(rig.standing), at rest, run 70 ticks on the committed act at the keys 36,000 and 288,000.  Every 5 ticks: the board's
mean count c; the light's form H_m (rig.forms, row 0) over its start; its fall over the time gear's form H_c (the last
row); the same fall over the uniform swing's own form N [(1/2) T (cbar - cbar_b)^2 + (1/2) D_c cbar cbar_b]; and
E / H_m0 with E = H_m + lam H_c, lam = ln(1000/999) key / 2 (lam_pred).
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # this folder's rig.py

import rig

shape = (4, 4, 4)
T = rig.teeth()


def diag(train, laid, key, ticks, every=5):
    L, s = rig.built([train], laid, shape, rig.integers(key=key))
    lam = math.log(1000 / 999) * key / 2
    row = L.ruler.row
    rows = []
    for n in range(ticks + 1):
        h = rig.forms(L, s)
        hm, hc = float(h[0]) / 2, float(h[-1]) / 2
        cb = float(rig.count(L, s))
        c = [int(x) for x in s.a[row].tolist()]
        cbv = [int(x) for x in s.b[row].tolist()]
        # the uniform swing's own form: N [ (1/2) T (cbar - cbar_b)^2 + (1/2) D_c cbar cbar_b ]
        cm = sum(c) / len(c)
        cmb = sum(cbv) / len(cbv)
        dc = int(L.gearing.spring[row, 0])
        hcu = len(c) * (0.5 * T * (cm - cmb) ** 2 + 0.5 * dc * cm * cmb)
        rows.append((n, hm, hc, hcu, cb))
        s = rig.tick(L, s)
    hm0 = rows[0][1]
    print(f"key {key}, lam_pred {lam:.3f}")
    for n, hm, hc, hcu, cb in rows[::every]:
        print(
            f" t {n:3d} c {cb:8.1f}  H_m/H_m0 {hm / hm0:.4f}  (H_m0-H_m)/H_c {((hm0 - hm) / hc if hc else 0):8.3f}  (H_m0-H_m)/H_c,uniform {((hm0 - hm) / hcu if hcu else 0):8.3f}  E/H_m0 {(hm + lam * hc) / hm0:.4f}"
        )


diag(rig.light(), rig.standing(shape, 600), 36000, 70)
diag(rig.light(), rig.standing(shape, 600), 288000, 70)
