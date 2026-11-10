"""EM-C6: link-wave front of the COMPACT-U(1) candidate vs the shared cone c_Q (NOTES_em.md §4).

B1-GAUGE's u1 link block alone (no matter needed: the matter stays at its vacuum), a transverse pulse W_im on the
z-links of a 3x3x3 patch at the centre, at rest. Arrival of |W_im(z-links)| at half and 1/10 of each station's peak
(interpolated) along x (transverse to the link axis) and along [111]; strict taxicab causality checked.
"""
import time

import numpy as np

from emlib import save, stamp
from research.metric_variant_v1.core import Engine, compose
from research.metric_variant_v1.layers.em_compact import default_compact
from research.metric_variant_v1.prepare import vacuum_state
from research.metric_variant_v1.prepare import em_compact as pc

L, T, amp = 40, 30, 2 ** 8
Q = (1 << 29) + 1
cQ = float(np.sqrt((Q - 1) / (3 * Q)))
t_start = stamp()
import sys
from research.metric_variant_v1.layers.em_compact import build_u1_links
kP = int(sys.argv[1]) if len(sys.argv) > 1 else 256          # EM-C6b exploratory: kappa_P = 2^15
if kP == 256:
    m, links, c = default_compact(Q)
else:
    links = build_u1_links(Q=Q, A=1 << 14, lam=4, kappa_P=kP, c_P=0, beta=6 * Q - (1 << 29))
Tn = compose(links)
eng = Engine(Tn, Q)
cc = L // 2
s0 = pc.link_pulse(vacuum_state(Tn, Q, L, links), Tn, 2, (cc, cc, cc), 1, amp)
g = Tn.gear_index("u1.Uz_im")
xs = list(range(3, 18))
diag = list(range(2, 9))
rec_x, rec_d = [], []
s = s0
viol = 0
X = np.arange(L)
d1 = np.abs(((X - cc + L // 2) % L) - L // 2)
dist1 = d1[:, None, None] + d1[None, :, None] + d1[None, None, :]
init_support = 3                     # the patch reaches |x - c|_1 <= 3
t0 = time.time()
for t in range(1, T + 1):
    s = eng.step(s)
    f = np.abs(s.b[g].astype(float)).reshape(L, L, L)
    rec_x.append([f[cc + k, cc, cc] for k in xs])
    rec_d.append([f[cc + k, cc + k, cc + k] for k in diag])
    nz = np.zeros((L, L, L), bool)
    for gg in range(Tn.G):
        nz |= (s.b[gg].reshape(L, L, L) != 0) | (s.a[gg].reshape(L, L, L) != 0)
    viol += int(np.count_nonzero(nz & (dist1 > t + init_support + 2)))   # +2: 2-path / link reach per update
secs = time.time() - t0


def arrival(series, frac):
    s_ = np.array(series)
    out = []
    for j in range(s_.shape[1]):
        mx = s_[:, j].max()
        if mx <= 0:
            out.append(np.nan)
            continue
        idx = np.nonzero(s_[:, j] >= frac * mx)[0]
        i = idx[0]
        if i == 0:
            out.append(np.nan)
            continue
        y0, y1 = s_[i - 1, j], s_[i, j]
        out.append(float(i + 1 + (frac * mx - y0) / (y1 - y0) - 1))
    return np.array(out)


R = np.array(xs, float)
Rd = np.array([np.sqrt(3) * k for k in diag])
fronts = {}
for frac in (0.5, 0.1):
    ax_ = arrival(rec_x, frac)
    dg = arrival(rec_d, frac)
    m1 = np.isfinite(ax_) & (R <= 0.8 * cQ * T + 3)
    m2 = np.isfinite(dg) & (Rd <= 0.8 * cQ * T + 3)
    fronts[f"frac{frac}"] = dict(v100=float(np.polyfit(ax_[m1], R[m1], 1)[0]) if m1.sum() > 2 else None,
                                 v111=float(np.polyfit(dg[m2], Rd[m2], 1)[0]) if m2.sum() > 2 else None,
                                 stations=(int(m1.sum()), int(m2.sum())))
peak_x = np.array(rec_x).max(0)
res = dict(L=L, T=T, amp=amp, Q=Q, c_Q=cQ, fronts=fronts, peak_along_x={int(k): float(v) for k, v in zip(xs, peak_x)},
           taxicab_violations=viol, rewind_exact=bool(eng.rewind(s, T).same_as(s0)), secs=secs, started=t_start,
           v111_half_over_cQ=(fronts["frac0.5"]["v111"] / cQ) if fronts["frac0.5"]["v111"] else None)
res["pass_111_within_3pct"] = bool(res["v111_half_over_cQ"] is not None and abs(res["v111_half_over_cQ"] - 1) <= 0.03)
res["kappa_P"] = kP
res["P0"], res["c_U"] = links.params["P0"], links.params["c_U"]
save("EM-C6_compact_wave" + ("" if kP == 256 else f"b_kP{kP}"), res)
print(res, flush=True)
