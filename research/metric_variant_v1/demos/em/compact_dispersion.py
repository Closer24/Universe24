"""EM-C9 (exploratory): long-wavelength transverse link-wave speed of B1-GAUGE's u1 links (2-path gears) vs the
stiff-limit formula c^2 = 2 K_eff/(D A^2), K_eff = K B/(K + 2B), K = kappa_P P0 A^2, B = beta P0^2 (NOTES_em.md §10)."""
import sys

import numpy as np

from emlib import save, stamp
from research.metric_variant_v1.core import Engine, State, compose
from research.metric_variant_v1.core.engine import OBJ
from research.metric_variant_v1.layers.em_compact import build_u1_links
from research.metric_variant_v1.prepare import vacuum_state

L, T, eps = 32, 300, 0.01
Q = (1 << 29) + 1
D = 6 * Q
A = 1 << 14
beta = 6 * Q - (1 << 29)
out = {}
for kP in [int(x) for x in (sys.argv[1:] or ["32768", "8192"])]:
    links = build_u1_links(Q=Q, A=A, lam=4, kappa_P=kP, c_P=0, beta=beta)
    Tn = compose(links)
    eng = Engine(Tn, Q)
    P0 = links.params["P0"]
    K = kP * P0 * A * A
    B = beta * P0 * P0
    Keff = K * B / (K + 2 * B)
    c_stiff = float(np.sqrt(2 * Keff / (D * A * A)))
    k = 2 * np.pi / L
    v_pred = c_stiff * 2 * np.sin(k / 2) / k
    s = vacuum_state(Tn, Q, L, links)
    g = Tn.gear_index("u1.Uz_im")
    gr = Tn.gear_index("u1.Uz_re")
    X = np.arange(L)
    th = eps * np.sin(k * X)[:, None, None] * np.ones((1, L, L))
    wim = np.rint(A * np.sin(th)).astype(np.int64)
    wre = np.rint(A * np.cos(th)).astype(np.int64) - A
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    for arr in (a, b):
        arr[g] = wim.reshape(-1).astype(object)
        arr[gr] = wre.reshape(-1).astype(object)
    s0 = State(L, a, b, r)
    proj = np.sin(k * X)
    amp = []
    st = s0
    blow = None
    mx = []
    for t in range(T + 1):
        m_ = st.max_abs()
        mx.append(m_)
        if m_ > 2 ** 40:                       # runaway guard (exploratory): stop and report the time
            blow = t
            break
        f = st.b[g].astype(float).reshape(L, L, L).mean(axis=(1, 2))
        amp.append(float((f * proj).sum() / (proj * proj).sum()))
        if t < T:
            st = eng.step(st)
    Tdone = len(amp) - 1
    amp = np.array(amp)
    zc = np.nonzero(np.diff(np.sign(amp)) != 0)[0]
    if len(zc) >= 2:
        # interpolated zero crossings; half-period = mean spacing
        zz = [i + amp[i] / (amp[i] - amp[i + 1]) for i in zc]
        half = float(np.mean(np.diff(zz))) if len(zz) > 1 else float("nan")
        omega = np.pi / half
    else:
        omega = float("nan")
    out[f"kappa_P={kP}"] = dict(P0=P0, c_U=links.params["c_U"], c_U_over_D=links.params["c_U"] / D, c_stiff=c_stiff,
                                v_pred_lattice=v_pred, omega=omega, v_measured=omega / k if omega == omega else None,
                                ratio=(omega / k) / v_pred if omega == omega else None, zero_crossings=len(zc),
                                blowup_at=blow, max_abs_every_25=[int(v).bit_length() for v in mx[::25]],
                                rewind_exact=bool(eng.rewind(st, (blow if blow is not None else T)).same_as(s0)))
    print(kP, out[f"kappa_P={kP}"], flush=True)
save("EM-C9_compact_dispersion", dict(out, started=stamp(), L=L, T=T, eps=eps, label="EXPLORATORY"))
