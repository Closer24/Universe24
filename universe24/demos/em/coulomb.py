"""EM-D1 (and EM-D8 control): fully dynamical two-body Coulomb force on the E1 board (pre-registered in NOTES_em.md).

Usage: python demos/em/coulomb.py CFG R [T] [BLIND] [WIDTH2]     CFG in {+-, ++, --}
WIDTH2 (EM-D1b, amendment A3): packet 2 gets another width, so the (+,-) state is not C-P symmetric; Newton III is then
read on forces, F_i = a_i / <E''>_i.
Both packets source the field and feel it; the field is prepared as the static E1 potential of the total charge
(A = 0, C = 0). Observables (window-free, as S4-P run5/run6): (+,-) species projection Pi+-, like charges the spin
projection of spin-separated packets. Prediction a1 = <E''> F1, F1 = -s1 (2 g_phi/(D <cos E>)) <|rho1| d_x Phi_2>.
"""
import sys
import time

import numpy as np

from emlib import (MASS0, HOP0, Q0, accel, band_stats, em_system, gx, phi_of, save, spin_projectors, stamp)
from universe24.observe import em as oem
from universe24.prepare import vacuum_state
from universe24.prepare import em as pem
from universe24.layers.matter import algebra

cfg = sys.argv[1]
r = int(sys.argv[2])
T = int(sys.argv[3]) if len(sys.argv) > 3 else 150
blind = int(sys.argv[4]) if len(sys.argv) > 4 else 0
L, amp, width = 32, 2 ** 14, 2.0
width2 = float(sys.argv[5]) if len(sys.argv) > 5 else width
rem_mode = sys.argv[6] if len(sys.argv) > 6 else "vac"     # "vac": 3Q-1 (R'-fixed); "even": 3Q+1 (EM-D1c diagnostic)
g_phi, g_A, sigma = 4, 1, 2 ** 14
t_start = stamp()
blocks, Tn, eng = em_system(g_phi=g_phi, g_A=g_A, sigma=sigma, blind=blind)
m, e = blocks
D = 6 * Q0
c = L // 2
x1 = (c - r // 2, c, c)
x2 = (c - r // 2 + r, c, c)
sg = {"+": 1, "-": -1}
s1, s2 = sg[cfg[0]], sg[cfg[1]]
like = s1 == s2
spin1, spin2 = (0, 1) if like else (0, 0)
a1p, b1p, _ = pem.dirac_packet(m.params, L, +1, width, amp, spin=spin1, center=x1)
a2p, b2p, _ = pem.dirac_packet(m.params, L, +1, width2, amp, spin=spin2, center=x2)
if s1 < 0:
    a1p, b1p = pem.c_image(a1p), pem.c_image(b1p)
if s2 < 0:
    a2p, b2p = pem.c_image(a2p), pem.c_image(b2p)
vac = vacuum_state(Tn, Q0, L, *blocks)
st = pem.set_matter(vac, Tn, "matter", a1p + a2p, b1p + b2p)
if rem_mode == "even":       # matter remainders 3Q + 1 (even, NOT fixed by R'): the C-image is no longer exact (as S4)
    st = pem.set_matter(st, Tn, "matter", a1p + a2p, b1p + b2p, np.full((L, L, L, 16), 3 * Q0 + 1, dtype=object))
rho_tot = oem.charge_density(st, Tn, D)
Phi0 = pem.static_phi_for(rho_tot, e.params)
st = pem.set_field(st, Tn, "em", "Phi", Phi0, Phi0)
s0 = st
# prediction
st1 = pem.set_matter(vac, Tn, "matter", a1p, b1p)
st2 = pem.set_matter(vac, Tn, "matter", a2p, b2p)
rho1 = np.asarray(oem.charge_density(st1, Tn, D), float)
rho2 = np.asarray(oem.charge_density(st2, Tn, D), float)
Epp, Ecos, _ = band_stats(m.params, L, width)
Epp2, Ecos2, _ = band_stats(m.params, L, width2)
F1 = -s1 * (2 * g_phi / (D * Ecos)) * float((np.abs(rho1) * gx(phi_of(rho2, e.params))).sum() / np.abs(rho1).sum())
F2 = -s2 * (2 * g_phi / (D * Ecos2)) * float((np.abs(rho2) * gx(phi_of(rho1, e.params))).sum() / np.abs(rho2).sum())
pred_a1, pred_a2 = Epp * F1, Epp2 * F2
# observables
X = np.arange(L)
dx = ((X - c + L // 2) % L) - L // 2
alg = algebra("pair")
Jp = alg["Jp"].astype(float)
if like:
    Ps = spin_projectors(m.params)
    Cm = alg["C"].astype(float)
    P1 = Ps[0] if s1 > 0 else Cm @ Ps[0] @ Cm
    P2 = Ps[1] if s2 > 0 else Cm @ Ps[1] @ Cm
else:
    P1 = oem.species_projector(s1).astype(float)
    P2 = oem.species_projector(s2).astype(float)


def cent(w):
    return float((w * dx[:, None, None]).sum() / w.sum())


o1, o2, q1, q2 = [], [], [], []
t0 = time.time()
s = s0
Cnz = 0
for t in range(T + 1):
    w1 = oem.projected_density(s, Tn, P1)
    w2 = oem.projected_density(s, Tn, P2)
    o1.append(cent(w1))
    o2.append(cent(w2))
    q1.append(float(w1.sum()))
    q2.append(float(w2.sum()))
    if t % 25 == 0:
        Cnz += int(np.count_nonzero(np.asarray(oem.lorenz_C(s, Tn) != 0, bool)))
    if t < T:
        s = eng.step(s)
secs = time.time() - t0
a1, a2 = accel(o1), accel(o2)
rew = eng.rewind(s, T).same_as(s0)
res = dict(cfg=cfg, r=r, T=T, L=L, amp=amp, width=width, Q=Q0, hop=HOP0, mass=MASS0, g_phi=g_phi, g_A=g_A,
           sigma=sigma, blind=blind, width2=width2, rem_mode=rem_mode, Epp2=Epp2, force_ratio_F2_over_F1=(a2 / Epp2) / (a1 / Epp),
           pred_a1=pred_a1, pred_a2=pred_a2, a1=a1, a2=a2, ratio=a1 / pred_a1,
           ratio2=a2 / pred_a2, newton3=a2 / a1, Epp=Epp, Ecos=Ecos, dx1=o1[-1] - o1[0], dx2=o2[-1] - o2[0],
           lorenz_C_nonzero_sampled=Cnz, rewind_exact=rew, secs=secs, engine_stats=dict(eng.stats),
           max_abs_final=s.max_abs(), started=t_start, obs1=o1, obs2=o2,
           species_charge_drift=[q1[-1] / q1[0] - 1, q2[-1] / q2[0] - 1])
want = 1 if s1 != s2 else -1
res["sign_ok"] = bool(np.sign(a1) == want and np.sign(a2) == -want)
res["ratio_ok"] = bool(0.90 <= res["ratio"] <= 1.05)
res["newton3_ok"] = bool(-1.025 <= res["newton3"] <= -0.975)
res["force_newton3_ok"] = bool(-1.025 <= res["force_ratio_F2_over_F1"] <= -0.975)
res["symmetric_state_note"] = ("(+,-) with equal packets is exactly C-P symmetric (exact C-image incl. remainders): "
                               "a2/a1 = -1 by symmetry" if (s1 != s2 and width2 == width) else "")
name = f"EM-D1_coulomb_{cfg}_r{r}_T{T}" + (f"_blind{blind}" if blind else "") + (f"_w2_{width2}" if width2 != width else "") + ("" if rem_mode == "vac" else f"_rem_{rem_mode}")
save(name, res)
print({k: v for k, v in res.items() if k not in ("obs1", "obs2")}, flush=True)
