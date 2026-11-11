"""EM-D2: Coulomb 1/r^2 with a PREPARED STATIC field and a SHORT window (pre-registered in NOTES_em.md).

A ball (radius 2) of charge at the box centre is represented by its prepared torus potential Phi (the static E1
Gauss law -2 g (Q-1) Lap Phi = sigma_ref rho_ball, k = 0 removed = a neutralising background), A = 0. The EM block has
sigma = 0, so the probe is a TEST charge and Phi is an exact fixed point (bit-static; checked every update).
ONE probe per board (particle or antiparticle) at r = 8, 10, 12, 14 on +x; window T = 40; a no-field control gives
the spreading and the drift. Prediction a = <E''> F, F = -s (2 g_phi/(D <cos E>)) <|rho| d_x Phi>.
"""
import sys
import time

import numpy as np

if __package__:
    from .emlib import MASS0, HOP0, Q0, accel, band_stats, em_system, gx, save, stamp
else:
    from emlib import MASS0, HOP0, Q0, accel, band_stats, em_system, gx, save, stamp
from universe24.observe import em as oem
from universe24.prepare import vacuum_state
from universe24.prepare import em as pem

L, T, amp, width = 40, 40, 2 ** 14, 2.5
if len(sys.argv) > 1:                      # POST-HOC variant (labelled in NOTES_em.md): longer window, still short
    T = int(sys.argv[1])                   # against the spreading time 2 sigma0^2 / E'' ~ 500 updates
if len(sys.argv) > 2:                      # EM-D2c POST-HOC #2: larger box (stations far from the torus midpoint)
    L = int(sys.argv[2])
g_phi, g_A, sigma_ref = 4, 1, 2 ** 14
stations = [8, 10, 12, 14]
t_start = stamp()
blocks, Tn, eng = em_system(g_phi=g_phi, g_A=g_A, sigma=0)
m, e = blocks
D = 6 * Q0
c = L // 2
vac = vacuum_state(Tn, Q0, L, *blocks)
# the ball's charge: the same total charge as one probe packet
a0, b0, _ = pem.dirac_packet(m.params, L, +1, width, amp, center=(c, c, c))
q_packet = float(np.asarray(oem.charge_density(pem.set_matter(vac, Tn, "matter", a0, b0), Tn, D), float).sum())
X, Y, Z = np.meshgrid(np.arange(L), np.arange(L), np.arange(L), indexing="ij")
ball = ((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2 <= 4).astype(float)
rho_ball = ball * q_packet / ball.sum()
g = (m.params["hop"] if m.params["wilson"] == 0 else np.gcd(m.params["hop"], m.params["wilson"]))
Phi = pem.torus_poisson(rho_ball * sigma_ref, 2.0 * g * (Q0 - 1))
PhiF = Phi.astype(float)
Epp, Ecos, _ = band_stats(m.params, L, width)
coef = 2 * g_phi / (D * Ecos)
dxs = ((np.arange(L) - c + L // 2) % L) - L // 2


def run(sp, r, field=True):
    pos = (c + r, c, c)
    a, b, _ = pem.dirac_packet(m.params, L, +1, width, amp, center=pos)
    if sp < 0:
        a, b = pem.c_image(a), pem.c_image(b)
    s0 = pem.set_matter(vac, Tn, "matter", a, b)
    if field:
        s0 = pem.set_field(s0, Tn, "em", "Phi", Phi, Phi)
    P = oem.species_projector(sp).astype(float)
    xs, sig2 = [], []
    rel = ((np.arange(L) - pos[0] + L // 2) % L) - L // 2
    s = s0
    static = True
    pidx = Tn.gear_index("em.Phi")
    rho0 = None
    for t in range(T + 1):
        w = oem.projected_density(s, Tn, P)
        if rho0 is None:
            rho0 = w
        xs.append(float((w * rel[:, None, None]).sum() / w.sum()))
        sig2.append(float((w * (rel ** 2)[:, None, None]).sum() / w.sum()))
        if field:
            static &= bool(np.array_equal(np.asarray(s.b[pidx], dtype=object).reshape(L, L, L), Phi.astype(object)))
        if t < T:
            s = eng.step(s)
    rew = eng.rewind(s, T).same_as(s0)
    grad = float((np.abs(rho0) * gx(PhiF)).sum() / np.abs(rho0).sum()) if field else 0.0
    F = -sp * coef * grad
    return dict(a=accel(xs), pred=Epp * F, grad=grad, sigma0=np.sqrt(sig2[0]), sigmaT=np.sqrt(sig2[-1]),
                phi_bit_static=static, rewind_exact=rew)


t0 = time.time()
ctrl = run(+1, stations[0], field=False)
out = {"control_no_field": ctrl}
for r in stations:
    for sp in (1, -1):
        res = run(sp, r)
        res["a_minus_control"] = res["a"] - ctrl["a"]
        res["ratio"] = res["a_minus_control"] / res["pred"]
        out[f"r={r},s={sp}"] = res
        print(r, sp, {k: (round(v, 6) if isinstance(v, float) else v) for k, v in res.items()}, flush=True)
R = np.array(stations, float)
ap = np.array([out[f"r={r},s=1"]["a_minus_control"] for r in stations])
am = np.array([out[f"r={r},s=-1"]["a_minus_control"] for r in stations])
gr = np.array([out[f"r={r},s=1"]["grad"] for r in stations])
slope_a = float(np.polyfit(np.log(R), np.log(np.abs(0.5 * (ap - am))), 1)[0])
slope_g = float(np.polyfit(np.log(R), np.log(np.abs(gr)), 1)[0])
kappa = np.abs(0.5 * (ap - am)) / np.abs(gr)
summary = dict(
    signs_ok=bool(all(ap > 0) and all(am < 0)),           # positive ball: particle repelled (+x), antiparticle attracted
    charge_symmetry=[float(x) for x in am / ap + 1], charge_symmetry_ok=bool(np.all(np.abs(am / ap + 1) <= 0.03)),
    ratios=[out[k]["ratio"] for k in out if k.startswith("r=")],
    ratio_ok=bool(all(0.85 <= out[k]["ratio"] <= 1.15 for k in out if k.startswith("r="))),
    slope_a=slope_a, slope_grad_torus=slope_g, slope_ok=bool(abs(slope_a - slope_g) <= 0.15),
    kappa_max_over_min=float(kappa.max() / kappa.min()),
    phi_bit_static=bool(all(out[k]["phi_bit_static"] for k in out if k.startswith("r="))),
    rewind_exact=bool(all(out[k]["rewind_exact"] for k in out)),
    spreading_sigmaT_over_sigma0=ctrl["sigmaT"] / ctrl["sigma0"], secs=time.time() - t0)
save("EM-D2_slope" + ("" if T == 40 and L == 40 else f"_POSTHOC_T{T}_L{L}"), dict(out, summary=summary, L=L, T=T, amp=amp, width=width, Q=Q0, g_phi=g_phi, sigma_ref=sigma_ref,
                         stations=stations, started=t_start))
print(summary, flush=True)
