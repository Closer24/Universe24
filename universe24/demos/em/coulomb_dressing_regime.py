"""EM-D9: E1 Coulomb (+,-) in the integrator's dressing-compatible integer regime (NOTES_em.md §13).
Usage: python coulomb_dressing_regime.py AMP_LOG2   (e.g. 8 -> A_psi = 256)"""
import sys
import time

import numpy as np

if __package__:
    from .emlib import accel, em_system, phi_of, save, stamp, gx
else:
    from emlib import accel, em_system, phi_of, save, stamp, gx
from universe24.observe import em as oem
from universe24.prepare import vacuum_state
from universe24.prepare import em as pem

Q = (1 << 29) + 1
D = 6 * Q
hop, wilson, mass = 1 << 27, 1 << 26, 3 << 29
g_phi, g_A, sigma = 4, 1, 1 << 24
amp = 1 << int(sys.argv[1])
if len(sys.argv) > 2 and sys.argv[2] == "off":          # EM-D9c control: every EM coupling off
    g_phi, g_A, sigma = 0, 0, 0
L, T, width, r = 32, 150, 2.0, 8
blocks, Tn, eng = em_system(Q=Q, hop=hop, mass=mass, wilson=wilson, g_phi=g_phi, g_A=g_A, sigma=sigma)
m, e = blocks
c = L // 2
x1, x2 = (c - r // 2, c, c), (c - r // 2 + r, c, c)
vac = vacuum_state(Tn, Q, L, *blocks)
a1p, b1p, _ = pem.dirac_packet(m.params, L, +1, width, amp, center=x1)
a2p, b2p, _ = pem.dirac_packet(m.params, L, +1, width, amp, center=x2)
a2p, b2p = pem.c_image(a2p), pem.c_image(b2p)
st = pem.set_matter(vac, Tn, "matter", a1p + a2p, b1p + b2p)
Phi0 = pem.static_phi_for(oem.charge_density(st, Tn, D), e.params) if sigma else 0 * np.zeros((L, L, L), np.int64)
s0 = pem.set_field(st, Tn, "em", "Phi", Phi0, Phi0)
rho1 = np.asarray(oem.charge_density(pem.set_matter(vac, Tn, "matter", a1p, b1p), Tn, D), float)
rho2 = np.asarray(oem.charge_density(pem.set_matter(vac, Tn, "matter", a2p, b2p), Tn, D), float)
# band with the Wilson term: |beta(k)| = sqrt((mass + w sum(2 - 2cos k))^2 + 4 hop^2 sum sin^2 k), sin E = |beta|/D
K = pem.kgrid(L)
kk = ((K + np.pi) % (2 * np.pi)) - np.pi
Z2 = np.exp(-width ** 2 * (kk ** 2).sum(-1))


def Ek(k):
    mm = mass + wilson * (2 - 2 * np.cos(k)).sum(-1)
    return np.arcsin(np.sqrt(mm ** 2 + 4.0 * hop ** 2 * (np.sin(k) ** 2).sum(-1)) / D)


h = 1e-3
ex = np.array([h, 0, 0])
Epp = (Ek(kk + ex) - 2 * Ek(kk) + Ek(kk - ex)) / h ** 2
wgt = Z2 / Z2.sum()
Epp_m, Ecos = float((wgt * Epp).sum()), float((wgt * np.cos(Ek(kk))).sum())
F1 = -(2 * max(g_phi, 1) / (D * Ecos)) * float((np.abs(rho1) * gx(phi_of(rho2, dict(e.params, sigma=1 << 24)))).sum() / np.abs(rho1).sum())
pred = Epp_m * F1
X = np.arange(L)
dx = ((X - c + L // 2) % L) - L // 2
P1, P2 = oem.species_projector(1).astype(float), oem.species_projector(-1).astype(float)
o1, o2, q1 = [], [], []
s = s0
Cnz = 0
t0 = time.time()
for t in range(T + 1):
    w1, w2 = oem.projected_density(s, Tn, P1), oem.projected_density(s, Tn, P2)
    o1.append(float((w1 * dx[:, None, None]).sum() / w1.sum()))
    o2.append(float((w2 * dx[:, None, None]).sum() / w2.sum()))
    q1.append(float(w1.sum()))
    if t % 50 == 0:
        Cnz += int(np.count_nonzero(np.asarray(oem.lorenz_C(s, Tn) != 0, bool)))
    if t < T:
        s = eng.step(s)
a1, a2 = accel(o1), accel(o2)
res = dict(amp=amp, Q=Q, hop=hop, wilson=wilson, mass=mass, g=e.params["g"], hs=e.params["hs"], ws=e.params["ws"],
           sigma=sigma, g_phi=g_phi, g_A=g_A, alpha=g_phi * sigma / (e.params["g"] * (Q - 1)), control_off=(sigma == 0),
           G_equiv=2 ** 15 * g_phi * sigma / (e.params["g"] * (Q - 1)) * amp ** 2, a1=a1, a2=a2, pred=pred,
           ratio=a1 / pred, newton3=a2 / a1, Epp=Epp_m, Ecos=Ecos, species_charge_drift=q1[-1] / q1[0] - 1,
           lorenz_C_nonzero_sampled=Cnz, rewind_exact=bool(eng.rewind(s, T).same_as(s0)),
           max_abs=s.max_abs(), stats=dict(eng.stats), secs=time.time() - t0, started=stamp())
res["pass"] = bool(a1 > 0 and a2 < 0 and 0.85 <= res["ratio"] <= 1.15 and res["rewind_exact"] and Cnz == 0)
save(f"EM-D9_dressing_regime_amp{amp}" + ("_OFF" if sigma == 0 else ""), dict(res, obs1=o1, obs2=o2))
print({k: v for k, v in res.items()}, flush=True)
