"""EM-C4 / EM-C5: Coulomb sign and NON-symmetric Newton III on the COMPACT-U(1) candidate (NOTES_em.md §4, A5).

Usage: python demos/em/compact_coulomb.py CFG R [W2]     CFG in {+-, ++}
Matter (16-ch pair) hops through B1-GAUGE's u1 links (temporal gauge: the link phase advance per update is E). The
links are prepared Gauss-consistent for the total charge (prepare/em_compact.gauss_links). (+,-): species projection
centroids; (+,+): half-space minimum-image centroids (packets separated in space). Newton III read on MOMENTUM:
(Q2 a2/<E''>_2)/(Q1 a1/<E''>_1), Q_i = |sum rho| of packet i alone.
"""
import sys
import time

import numpy as np

from emlib import accel, band_stats, save, stamp
from research.metric_variant_v1.core import Engine, compose
from research.metric_variant_v1.layers.em_compact import default_compact
from research.metric_variant_v1.observe import em as oem
from research.metric_variant_v1.observe import em_compact as oc
from research.metric_variant_v1.prepare import vacuum_state
from research.metric_variant_v1.prepare import em as pem
from research.metric_variant_v1.prepare import em_compact as pc

cfg = sys.argv[1]
r = int(sys.argv[2])
w2 = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
sym = len(sys.argv) > 4 and sys.argv[4] == "sym"          # EM-C4b POST-HOC: symmetric half-spaces
L, T, amp, w1 = 24, 60, 2 ** 11, 2.0
Q = (1 << 29) + 1
D = 6 * Q
t_start = stamp()
m, links, c = default_compact(Q)
Tn = compose(m, links, c)
eng = Engine(Tn, Q)
cc = L // 2
x1 = (cc - r // 2, cc, cc)
x2 = (cc - r // 2 + r, cc, cc)
sg = {"+": 1, "-": -1}
s1, s2 = sg[cfg[0]], sg[cfg[1]]
vac = vacuum_state(Tn, Q, L, m, links, c)
a1p, b1p, _ = pem.dirac_packet(m.params, L, +1, w1, amp, center=x1)
a2p, b2p, _ = pem.dirac_packet(m.params, L, +1, w2, amp, center=x2)
if s1 < 0:
    a1p, b1p = pem.c_image(a1p), pem.c_image(b1p)
if s2 < 0:
    a2p, b2p = pem.c_image(a2p), pem.c_image(b2p)
st = pem.set_matter(vac, Tn, "matter", a1p + a2p, b1p + b2p)
rho = oem.charge_density(st, Tn, D)
s0 = pc.gauss_links(st, Tn, rho, links.params["A"], D)
Q1 = abs(float(np.asarray(oem.charge_density(pem.set_matter(vac, Tn, "matter", a1p, b1p), Tn, D), float).sum()))
Q2 = abs(float(np.asarray(oem.charge_density(pem.set_matter(vac, Tn, "matter", a2p, b2p), Tn, D), float).sum()))
G0 = oc.gauss_G(s0, Tn, links.params, D)
X = np.arange(L)
dx = ((X - cc + L // 2) % L) - L // 2
like = s1 == s2
if like:
    P1 = P2 = oem.species_projector(s1).astype(float)
    mask1 = (dx < 0)[:, None, None] * np.ones((1, L, L))
    mask2 = (dx >= 0)[:, None, None] * np.ones((1, L, L))
    if sym:
        mask1 = ((dx <= -1) & (dx >= -(L // 2 - 1)))[:, None, None] * np.ones((1, L, L))
        mask2 = ((dx >= 1) & (dx <= L // 2 - 1))[:, None, None] * np.ones((1, L, L))
else:
    P1, P2 = oem.species_projector(s1).astype(float), oem.species_projector(s2).astype(float)
    mask1 = mask2 = np.ones((L, L, L))


def cent(w, mask):
    w = w * mask
    return float((w * dx[:, None, None]).sum() / w.sum())


o1, o2, devs, adv = [], [], [], []
s = s0
gfail = 0
t0 = time.time()
for t in range(T + 1):
    o1.append(cent(oem.projected_density(s, Tn, P1), mask1))
    o2.append(cent(oem.projected_density(s, Tn, P2), mask2))
    if t % 10 == 0:
        devs.append(oc.link_norm_dev(s, Tn, links.params))
        th = oc.link_phase_advance(s, Tn, links.params, 0)
        adv.append(float(th[cc, cc, cc]))
    if t < T:
        s2_ = eng.step(s)
        if t % 10 == 0:
            gfail += int(np.count_nonzero(np.asarray(oc.gauss_step_residual(s, s2_, Tn, links.params, D) != 0, bool)))
        s = s2_
secs = time.time() - t0
a1, a2 = accel(o1), accel(o2)
a1e, a2e = accel(o1[:21]), accel(o2[:21])                 # EM-C5b POST-HOC early window t = 0..20
E1, _, _ = band_stats(m.params, L, w1)
E2, _, _ = band_stats(m.params, L, w2)
mom = (Q2 * a2 / E2) / (Q1 * a1 / E1)
mom_early = (Q2 * a2e / E2) / (Q1 * a1e / E1)
rew = eng.rewind(s, T).same_as(s0)
want = 1 if s1 != s2 else -1          # +1: packet 1 (left) moves toward packet 2 (attraction)
res = dict(cfg=cfg, r=r, T=T, L=L, amp=amp, widths=(w1, w2), Q=Q, A=links.params["A"], a1=a1, a2=a2,
           newton3_accel=a2 / a1, momentum_ratio=mom, POSTHOC_early_a1=a1e, POSTHOC_early_a2=a2e,
           POSTHOC_early_momentum_ratio=mom_early, symmetric_masks=sym, Q1=Q1, Q2=Q2, Epp1=E1, Epp2=E2,
           sign_ok=bool(np.sign(a1) == want and np.sign(a2) == -want),
           momentum_ok=bool(-1.025 <= mom <= -0.975), gauss_step_failures_sampled=gfail,
           initial_gauss_residual_rel=float(np.abs(np.asarray(G0, float)).max() / np.abs(np.asarray(rho, float)).max()),
           link_norm_dev=devs, centre_link_phase_advance=adv, rewind_exact=rew, secs=secs,
           engine_stats=dict(eng.stats), started=t_start, obs1=o1, obs2=o2)
save(f"EM-C4_compact_coulomb_{cfg}_r{r}_w2_{w2}" + ("_symPOSTHOC" if sym else ""), res)
print({k: v for k, v in res.items() if k not in ("obs1", "obs2")}, flush=True)
