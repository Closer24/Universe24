"""EM-C8 (POST-HOC diagnostic): early-window force of the compact-U(1) candidate vs the Gauss-prepared field."""
import numpy as np

from emlib import accel, band_stats, save, stamp
from universe24.core import Engine, compose
from universe24.layers.em_compact import default_compact
from universe24.observe import em as oem
from universe24.observe import em_compact as oc
from universe24.prepare import vacuum_state
from universe24.prepare import em as pem
from universe24.prepare import em_compact as pc

L, T, amp, w = 24, 20, 2 ** 11, 2.0
Q = (1 << 29) + 1
D = 6 * Q
m, links, c = default_compact(Q)
Tn = compose(m, links, c)
eng = Engine(Tn, Q)
cc = L // 2
X = np.arange(L)
dx = ((X - cc + L // 2) % L) - L // 2
E2, _, _ = band_stats(m.params, L, w)
out = {}
for r in (6, 8, 10):
    x1, x2 = (cc - r // 2, cc, cc), (cc - r // 2 + r, cc, cc)
    vac = vacuum_state(Tn, Q, L, m, links, c)
    a1p, b1p, _ = pem.dirac_packet(m.params, L, +1, w, amp, center=x1)
    a2p, b2p, _ = pem.dirac_packet(m.params, L, +1, w, amp, center=x2)
    a2p, b2p = pem.c_image(a2p), pem.c_image(b2p)
    st = pem.set_matter(vac, Tn, "matter", a1p + a2p, b1p + b2p)
    s0 = pc.gauss_links(st, Tn, oem.charge_density(st, Tn, D), links.params["A"], D)
    rho1 = np.abs(np.asarray(oem.charge_density(pem.set_matter(vac, Tn, "matter", a1p, b1p), Tn, D), float))
    dth = oc.link_phase_advance(s0, Tn, links.params, 0)
    dth_node = 0.5 * (dth + np.roll(dth, 1, axis=0))
    mean_dth = float((rho1 * dth_node).sum() / rho1.sum())
    P1 = oem.species_projector(1).astype(float)
    xs = []
    s = s0
    for t in range(T + 1):
        wgt = oem.projected_density(s, Tn, P1)
        xs.append(float((wgt * dx[:, None, None]).sum() / wgt.sum()))
        if t < T:
            s = eng.step(s)
    a1 = accel(xs)
    out[f"r={r}"] = dict(a1=a1, mean_dtheta=mean_dth, pred_abs=abs(E2 * mean_dth), ratio_abs=abs(a1) / abs(E2 * mean_dth),
                         sign_a1=float(np.sign(a1)), sign_dtheta=float(np.sign(mean_dth)))
    print(r, out[f"r={r}"], flush=True)
R = np.array([6, 8, 10], float)
A1 = np.array([abs(out[f"r={int(r)}"]["a1"]) for r in R])
Pd = np.array([out[f"r={int(r)}"]["pred_abs"] for r in R])
summary = dict(slope_a=float(np.polyfit(np.log(R), np.log(A1), 1)[0]),
               slope_pred=float(np.polyfit(np.log(R), np.log(Pd), 1)[0]), label="POST-HOC diagnostic")
save("EM-C8_compact_force_POSTHOC", dict(out, summary=summary, started=stamp()))
print(summary, flush=True)
