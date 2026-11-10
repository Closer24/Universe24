"""EM-D4 dipole radiation (MECHANISM: prescribed exactly conserved oscillating current on one link), pure field.

Pre-registered in NOTES_em.md. Usage: python demos/em/dipole.py [AXIS] [Q] [L] [T]   (AXIS z or y; default z 1025 48 70)
The driver gear S (u_S = kappa S.b, kappa = round(D cos 0.4): a linear clock) feeds the A source on the link
(c, c + e_axis). Readouts: E = -grad(phi) - (A(t) - A(t-1)), phi = Phi/3 (documented; the phi = Phi control is
reported); Lorenz C at every node and update; amplitudes along x; fronts along [100] and [111] (half-peak and 1/10 of
peak arrivals); strict taxicab causality of the field support.
"""
import sys
import time

import numpy as np

from emlib import save, stamp
from universe24.core import Engine, compose
from universe24.layers.em import A_NAMES, build_current_driver, build_em
from universe24.observe import em as oem
from universe24.prepare import vacuum_state, with_gears

axis_name = sys.argv[1] if len(sys.argv) > 1 else "z"
Q = int(sys.argv[2]) if len(sys.argv) > 2 else 1025
L = int(sys.argv[3]) if len(sys.argv) > 3 else 48
T = int(sys.argv[4]) if len(sys.argv) > 4 else 70
dax = {"x": 0, "y": 1, "z": 2}[axis_name]
D = 6 * Q
Om = 0.4
kappa = int(round(D * np.cos(Om)))
Om_eff = float(np.arccos(kappa / D))
P0 = 2 ** 40 if Q > 100 else 2 ** 30
t_start = stamp()
e = build_em(Q=Q, matter=None, g_phi=0, g_A=0, sigma=0)
drv = build_current_driver(Q=Q, em=e, axis=dax, kappa=kappa, coupling=1)
Tn = compose(e, drv)
eng = Engine(Tn, Q)
c = L // 2
vac = vacuum_state(Tn, Q, L, e, drv)
s0 = with_gears(vac, Tn, {("drive.S", (c, c, c)): (-int(round(P0 * np.sin(Om_eff))), 0, 3 * Q - 1)})
cQ = float(np.sqrt((Q - 1) / (3 * Q)))
xs = list(range(2, min(23, L // 2 - 1)))
diag = [k for k in range(1, L // 2 - 2)]
recE = {"par": [], "long": [], "other": [], "par_phi1": [], "long_phi1": [], "diag": []}
other_ax = [d for d in (1, 2) if d != dax][0] if dax != 0 else 1
Cfail = 0
causal_viol = 0
s = s0
t0 = time.time()
lat_x = np.arange(L)
dist1 = (np.abs(((lat_x - c + L // 2) % L) - L // 2)[:, None, None] + np.abs(((lat_x - c + L // 2) % L) - L // 2)[None, :, None]
         + np.abs(((lat_x - c + L // 2) % L) - L // 2)[None, None, :])
for t in range(1, T + 1):
    s = eng.step(s)
    Cfail += int(np.count_nonzero(np.asarray(oem.lorenz_C(s, Tn) != 0, bool)))
    E = oem.electric_field(s, Tn)
    E1 = oem.electric_field(s, Tn, phi_norm=1.0)
    recE["par"].append([E[dax][c + k, c, c] for k in xs])
    recE["long"].append([E[0][c + k, c, c] for k in xs])
    recE["other"].append([E[other_ax][c + k, c, c] for k in xs])
    recE["par_phi1"].append([E1[dax][c + k, c, c] for k in xs])
    recE["long_phi1"].append([E1[0][c + k, c, c] for k in xs])
    recE["diag"].append([float(np.sqrt(sum(E[d][c + k, c + k, c + k] ** 2 for d in range(3)))) for k in diag])
    # strict taxicab causality: every field gear is exactly 0 beyond |x - c|_1 > t + 1 (the driver link reaches c+e)
    f = oem.field_view(s, Tn)
    for n in A_NAMES + ("Phi",):
        nz = np.asarray(f[n][1] != 0, bool) | np.asarray(f[n][0] != 0, bool)
        causal_viol += int(np.count_nonzero(nz & (dist1 > t + 1)))
secs = time.time() - t0
R = np.array(xs, float)
par, lon, oth = (np.array(recE[k]) for k in ("par", "long", "other"))
amp = lambda Ea: np.abs(Ea[-20:]).max(0)
A_par, A_long, A_oth = amp(par), amp(lon), amp(oth)
sel = (R >= 10) & (R <= 18)
slope = float(np.polyfit(np.log(R[sel]), np.log(A_par[sel]), 1)[0]) if sel.any() else None
lt = {int(r): float(A_long[i] / A_par[i]) for i, r in enumerate(xs) if r in (4, 6, 8, 10, 12)}
lt1 = {int(r): float(amp(np.array(recE["long_phi1"]))[i] / amp(np.array(recE["par_phi1"]))[i])
       for i, r in enumerate(xs) if r in (4, 6, 8, 10, 12)}


def arrival(series, frac):
    s_ = np.abs(np.array(series))
    out = []
    for j in range(s_.shape[1]):
        mx = s_[:, j].max()
        idx = np.nonzero(s_[:, j] >= frac * mx)[0]
        if len(idx) == 0:
            out.append(np.nan)
            continue
        i = idx[0]
        if i == 0:
            out.append(1.0)
            continue
        y0, y1 = s_[i - 1, j], s_[i, j]
        out.append(float(i + (frac * mx - y0) / (y1 - y0)))   # interpolated (t index starts at update 1)
    return np.array(out)


fronts = {}
Rd = np.array([np.sqrt(3) * k for k in diag])
for frac in (0.5, 0.1):
    ax_ = arrival(par, frac)
    dg = arrival(recE["diag"], frac)
    m1 = (R >= 8) & (R <= 20) & np.isfinite(ax_)
    m2 = (Rd >= 8) & np.isfinite(dg)
    fronts[f"frac{frac}"] = dict(v100=float(np.polyfit(ax_[m1], R[m1], 1)[0]) if m1.sum() > 2 else None,
                                 v111=float(np.polyfit(dg[m2], Rd[m2], 1)[0]) if m2.sum() > 2 else None)
# POST-HOC readout (labelled; NOTES_em.md): each station's peak only BEFORE its first image wave can arrive
# (t < d_image / c_Q - 2, d_image = distance to the nearest periodic image of the source), and the fit only over
# stations reached well inside the window (r <= 0.8 c_Q T).


def arrival_pre_image(series, frac, dists, dimg):
    s_ = np.abs(np.array(series))
    out = []
    for j in range(s_.shape[1]):
        tmax = int(min(s_.shape[0], dimg[j] / cQ - 2))
        if tmax < 3 or dists[j] > 0.8 * cQ * T:
            out.append(np.nan)
            continue
        seg = s_[:tmax, j]
        mx = seg.max()
        idx = np.nonzero(seg >= frac * mx)[0]
        i = idx[0]
        if i == 0:
            out.append(np.nan)
            continue
        y0, y1 = seg[i - 1], seg[i]
        out.append(float(i + (frac * mx - y0) / (y1 - y0)))
    return np.array(out)


dimg_x = np.array([L - r for r in xs], float)
dimg_d = np.array([np.sqrt((L - k) ** 2 + 2 * k ** 2) for k in diag], float)
posthoc = {}
for frac in (0.5, 0.1):
    ax_ = arrival_pre_image(par, frac, R, dimg_x)
    dg = arrival_pre_image(recE["diag"], frac, Rd, dimg_d)
    m1 = (R >= 6) & np.isfinite(ax_)
    m2 = (Rd >= 6) & np.isfinite(dg)
    posthoc[f"frac{frac}"] = dict(v100=float(np.polyfit(ax_[m1], R[m1], 1)[0]) if m1.sum() > 2 else None,
                                  v111=float(np.polyfit(dg[m2], Rd[m2], 1)[0]) if m2.sum() > 2 else None,
                                  stations_100=int(m1.sum()), stations_111=int(m2.sum()))
res = dict(axis=axis_name, Q=Q, L=L, T=T, fronts_POSTHOC_pre_image_window=posthoc, Omega=Om_eff, kappa=kappa, c_Q=cQ, secs=secs, lorenz_C_failures=Cfail,
           node_updates=L ** 3 * T, taxicab_causality_violations=causal_viol, far_field_exponent=slope,
           A_par={int(r): float(v) for r, v in zip(xs, A_par)},
           other_transverse_over_par_r10_18=float((A_oth / A_par)[sel].max()) if sel.any() else None,
           long_over_par_phi_third=lt, long_over_par_phi_equals_Phi_control=lt1, fronts=fronts,
           rewind_exact=bool(eng.rewind(s, T).same_as(s0)), started=t_start)
save(f"EM-D4_dipole_{axis_name}_Q{Q}_L{L}", res)
print(res, flush=True)
