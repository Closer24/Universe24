"""EM-D5 magnetism (MECHANISM: prescribed steady antiparallel line currents; pre-registered in NOTES_em.md).

Static driver gears S (u_S = D S.b: marginal, rounding-free, exactly static) feed the A_y source along two lines
(x = 8 and x = 24 at z = 16, all y) with opposite signs; A_y is prepared at its static profile (torus solution of
-(Q-1) Lap A_y = coupling * S); Phi stays 0 exactly (div A = d_y A_y = 0). The probe (sigma = 0: a test charge) moves
along +-y with k = +-0.4 at x = 14. Prediction a_x = <E''_xx> s q_A v_y <d_x A_y>, q_A = g_A / hop (S4-P PR-28 form;
the lattice factor 1/cos k_y of the k-shift is reported separately). A g = 0 control is subtracted.
"""
import time

import numpy as np

if __package__:
    from .emlib import Q0, accel, band_stats, save, stamp
else:
    from emlib import Q0, accel, band_stats, save, stamp
from universe24.core import Engine, compose
from universe24.layers.em import build_current_driver, build_em
from universe24.layers.matter import build_matter
from universe24.observe import em as oem
from universe24.prepare import vacuum_state
from universe24.prepare import em as pem

L, T, amp, width = 32, 60, 2 ** 14, 4.0
x1w, x2w, z0, xp = 8, 24, 16, 14
hop, mass = Q0, 3 * Q0
g_A = 1
S0, c_drv = 2 ** 20, 2 ** 29
t_start = stamp()
D = 6 * Q0
out = {}


def build(gA):
    m = build_matter(Q=Q0, hop=hop, mass=mass)
    e = build_em(Q=Q0, matter=m, g_phi=gA, g_A=gA, sigma=0)
    drv = build_current_driver(Q=Q0, em=e, axis=1, kappa=D, coupling=c_drv)
    Tn = compose(m, e, drv)
    return (m, e, drv), Tn, Engine(Tn, Q0)


S = np.zeros((L, L, L), np.int64)
S[x1w, :, z0] = S0
S[x2w, :, z0] = -S0
Ay = pem.torus_poisson(S.astype(float) * c_drv, float(Q0 - 1))
Ayf = Ay.astype(float)
dAy = 0.5 * (np.roll(Ayf, -1, 0) - np.roll(Ayf, 1, 0))
X = np.arange(L)
runs = (("part_+y", 1, 0.4), ("anti_+y", -1, 0.4), ("part_-y", 1, -0.4), ("anti_-y", -1, -0.4))
t0 = time.time()
for gA in (g_A, 0):
    blocks, Tn, eng = build(gA)
    m = blocks[0]
    vac = vacuum_state(Tn, Q0, L, *blocks)
    for label, sp, ky in runs:
        a0, b0, _ = pem.dirac_packet(m.params, L, +1, width, amp, kc=(0, ky, 0), center=(xp, L // 2, z0))
        if sp < 0:
            a0, b0 = pem.c_image(a0), pem.c_image(b0)
        s0 = pem.set_matter(vac, Tn, "matter", a0, b0)
        s0 = pem.set_field(s0, Tn, "em", "A_y", Ay, Ay)
        sv = {}
        A_s, B_s, R_s = s0.a.astype(object), s0.b.astype(object), s0.r.astype(object)
        gi = Tn.gear_index("drive.S")
        A_s[gi] = S.reshape(-1).astype(object)
        B_s[gi] = S.reshape(-1).astype(object)
        from universe24.core import State
        s0 = State(L, A_s, B_s, R_s)
        P = oem.species_projector(sp).astype(float)
        qsign = float(np.sign(np.asarray(oem.charge_density(s0, Tn, D), float).sum()))
        xs, ys, Fx = [], [], []
        phimax = 0
        s = s0
        for t in range(T + 1):
            w = oem.projected_density(s, Tn, P)
            w = w / w.sum()
            dxp = ((X - xp + L // 2) % L) - L // 2
            xs.append(float((w * dxp[:, None, None]).sum()))
            yc = (w * np.exp(2j * np.pi * X[None, :, None] / L)).sum()
            ys.append(float(np.angle(yc) * L / (2 * np.pi)))
            Fx.append(float((w * dAy).sum()))
            f = oem.field_view(s, Tn)
            phimax = max(phimax, int(np.abs(np.asarray(f["Phi"][1], dtype=object)).max()))
            if t < T:
                s = eng.step(s)
        rew = eng.rewind(s, T).same_as(s0)
        tt = np.arange(T + 1)
        vy = float(np.polyfit(tt, np.unwrap(np.array(ys) * 2 * np.pi / L) * L / (2 * np.pi), 1)[0])
        Exx, _, _ = band_stats(m.params, L, width / np.sqrt(2), kc=(0, ky, 0), axis=0)
        qA = g_A / hop
        pred = Exx * sp * qA * vy * float(np.mean(Fx))
        out[f"{label}_g{gA}"] = dict(a_x=accel(xs), v_y=vy, pred=pred, Phi_max=phimax, rewind_exact=rew, q_sign=qsign,
                                     lattice_factor_1_over_cos_ky=1 / np.cos(ky))
        print(label, gA, out[f"{label}_g{gA}"], flush=True)
res = {}
for label, sp, ky in runs:
    on, off = out[f"{label}_g{g_A}"], out[f"{label}_g0"]
    a = on["a_x"] - off["a_x"]
    res[label] = dict(a_x_minus_control=a, pred=on["pred"], ratio=a / on["pred"], v_y=on["v_y"], q_sign=on["q_sign"],
                      parallel_to_x8_wire=bool(on["q_sign"] * on["v_y"] > 0))
summary = dict(
    charge_odd=res["anti_+y"]["a_x_minus_control"] / res["part_+y"]["a_x_minus_control"],
    velocity_odd=res["part_-y"]["a_x_minus_control"] / res["part_+y"]["a_x_minus_control"],
    ratios={k: v["ratio"] for k, v in res.items()},
    # parallel currents attract: the probe current (particle moving +y) is parallel to the wire at x = 8 (+S): the
    # probe at x = 14 lies between the wires; attraction to the +S wire = motion toward smaller x.
    parallel_attract=bool(all((v["a_x_minus_control"] < 0) == v["parallel_to_x8_wire"] for v in res.values())),
    Phi_identically_zero=bool(all(v["Phi_max"] == 0 for v in out.values())),
    rewind_exact=bool(all(v["rewind_exact"] for v in out.values())), secs=time.time() - t0)
summary["charge_odd_ok"] = bool(-1.10 <= summary["charge_odd"] <= -0.90)
summary["velocity_odd_ok"] = bool(-1.10 <= summary["velocity_odd"] <= -0.90)
summary["ratio_ok"] = bool(all(0.85 <= v <= 1.15 for v in summary["ratios"].values()))
save("EM-D5_magnet", dict(out=out, res=res, summary=summary, L=L, T=T, amp=amp, width=width, Q=Q0, hop=hop, mass=mass,
                          g_A=g_A, S0=S0, c_drv=c_drv, started=t_start))
print(summary, flush=True)
