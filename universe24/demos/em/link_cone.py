"""LINK WAVES ON THE SHARED CONE (NOTES_em.md §12): exact linear dispersion of the compact link dynamics.

In deviation form the degree-1 monomials of the link (U*) and 2-path (P*) gears are the Hessian H of the potential;
linearised about the vacuum every gear obeys D (xi(t+1) + xi(t-1)) = 2 (H xi)(t), so for the Bloch matrix
H(k)[t, f] = sum coeff exp(i k . offset) every eigenvalue h gives cos(omega) = h / D (|h| <= D: stable).
Usage:  python link_cone.py lc1        (dispersion of the given regimes, formula check)
        python link_cone.py lc2        (cone-regime search)
"""
import sys
import time

import numpy as np

from emlib import save, stamp
from universe24.core import compose
from universe24.layers.gauge import build_default, build_gauge
from universe24.layers.em_compact import build_u1_links


def sel_links(tensor, ns):
    return [i for i, n in enumerate(tensor.names) if n.startswith(f"{ns}.U") or n.startswith(f"{ns}.P")]


def bloch_data(tensor, sel):
    pos = {g: j for j, g in enumerate(sel)}
    rows, cols, coefs, offs = [], [], [], []
    for m in tensor.monomials:
        if m.degree != 1 or m.target not in pos:
            continue
        f = m.factors[0]
        if f.field != "b" or f.gear not in pos:
            continue
        rows.append(pos[m.target])
        cols.append(pos[f.gear])
        coefs.append(float(m.coeff))
        offs.append(f.offset)
    return len(sel), np.array(rows), np.array(cols), np.array(coefs), np.array(offs, float)


def bloch(bd, k):
    n, rows, cols, coefs, offs = bd
    H = np.zeros((n, n), complex)
    np.add.at(H, (rows, cols), coefs * np.exp(1j * offs @ np.asarray(k, float)))
    return H


def omegas(bd, D, k):
    h = np.linalg.eigvalsh(0.5 * (bloch(bd, k) + bloch(bd, k).conj().T))
    return h / D


def photon(bd, D, direction, kabs, n_gauge):
    """Transverse photon speeds at |k| = kabs along ``direction``: skip the n_gauge pure-gauge modes (h = D) and
    return omega/k of the next 2 n_gauge modes (two polarisations per generator)."""
    d = np.asarray(direction, float)
    d = d / np.linalg.norm(d)
    hD = omegas(bd, D, kabs * d)
    w = np.sort(np.arccos(np.clip(hD, -1.0, 1.0)))
    nz = w[n_gauge:n_gauge + 2 * n_gauge]
    return float(nz.min() / kabs), float(nz.max() / kabs), float(w[:n_gauge].max())


def stability(bd, D, nk=16):
    """max |h|/D and min h/D over an nk^3 Bloch grid (incl. the zone boundary)."""
    ks = 2 * np.pi * np.arange(nk) / nk
    hmax, hmin = -np.inf, np.inf
    for kx in ks:
        for ky in ks:
            for kz in ks:
                hD = omegas(bd, D, (kx, ky, kz))
                hmax, hmin = max(hmax, hD.max()), min(hmin, hD.min())
    return float(hmax), float(hmin)


def stiff_formula(Q, A, kappa_P, P0, beta):
    D = 6 * Q
    K = kappa_P * P0 * A * A
    B = beta * P0 * P0
    Keff = K * B / (K + 2 * B)
    return float(np.sqrt(2 * Keff / (D * A * A)))


def analyse(tensor, ns, Q, n_gauge, label, params=None, nk=16):
    sel = sel_links(tensor, ns)
    bd = bloch_data(tensor, sel)
    D = 6 * Q
    out = {"label": label, "gears": len(sel)}
    for name, dvec in (("100", (1, 0, 0)), ("110", (1, 1, 0)), ("111", (1, 1, 1))):
        out[name] = {f"k={kk}": photon(bd, D, dvec, kk, n_gauge) for kk in (0.05, 0.1, 0.2)}
    out["hmax_over_D"], out["hmin_over_D"] = stability(bd, D, nk)
    out["stable_linear"] = bool(out["hmax_over_D"] <= 1 + 1e-12 and out["hmin_over_D"] >= -1 - 1e-12)
    if params is not None:
        out["c_stiff_formula"] = stiff_formula(Q, params["A"], params["kappa_P"], params["P0"], params["beta"])
        out["c_bloch_100_k0.05"] = out["100"]["k=0.05"][0]
        out["formula_ratio"] = out["c_bloch_100_k0.05"] / out["c_stiff_formula"]
    out["c_Q"] = float(np.sqrt((Q - 1) / (3 * Q)))
    return out


def lc1():
    res = {}
    Q = (1 << 29) + 1
    A = 1 << 14
    for kP in (256, 1 << 13, 1 << 15):
        blk = build_u1_links(Q=Q, A=A, lam=4, kappa_P=kP, c_P=0, beta=6 * Q - (1 << 29))
        T = compose(blk)
        r = analyse(T, "u1", Q, 1, f"u1 kappa_P={kP}", dict(blk.params, A=A, kappa_P=kP), nk=12)
        res[r["label"]] = r
        print(r["label"], {k: r[k] for k in ("c_stiff_formula", "c_bloch_100_k0.05", "formula_ratio", "hmax_over_D",
                                             "hmin_over_D")}, r["111"]["k=0.05"], flush=True)
    for Qd in ((1 << 25) + 1, (1 << 29) + 1):
        for grp, ng in (("u1", 1), ("su2", 3), ("su3", 8)):
            blk = build_default(grp, Q=Qd)
            T = compose(blk)
            p = blk.params
            r = analyse(T, grp, Qd, ng, f"default {grp} Q={Qd}", dict(p), nk=8)
            res[r["label"]] = r
            print(r["label"], {k: r.get(k) for k in ("c_stiff_formula", "c_bloch_100_k0.05", "formula_ratio",
                                                     "hmax_over_D", "hmin_over_D")}, r["111"]["k=0.05"], flush=True)
    save("LC1_link_dispersion", dict(res, started=stamp()))


if __name__ == "__main__":
    t0 = time.time()
    if sys.argv[1] == "lc1":
        lc1()
    print("secs", time.time() - t0)


def lc2():
    """Scan kappa_P, d_P, lam (c_P = 0, beta = D - d_P) at Q = 2^29+1, A = 2^14 for the fastest linearly stable photon."""
    Q = (1 << 29) + 1
    A = 1 << 14
    D = 6 * Q
    rows = []
    for e_k in range(10, 17):
        kP = 1 << e_k
        for e_d in range(26, 30):
            dP = 1 << e_d
            if (kP * A * A) % dP:
                continue
            P0 = kP * A * A // dP
            cU = 4 * kP * P0
            edge = cU / (A * A)
            for f in (1.05, 1.5, 2.0, 3.0):
                lam = max(1, int(np.ceil(edge * f)))
                blk = build_u1_links(Q=Q, A=A, lam=lam, kappa_P=kP, c_P=0, beta=D - dP)
                T = compose(blk)
                bd = bloch_data(T, sel_links(T, "u1"))
                hmax, hmin = stability(bd, D, nk=8)
                cs = [photon(bd, D, v, 0.05, 1) for v in ((1, 0, 0), (1, 1, 0), (1, 1, 1))]
                row = dict(kappa_P=kP, d_P=dP, P0=P0, c_U_over_D=cU / D, lam=lam, lam_over_edge=lam / edge,
                           radial_diag_over_D=(cU + 2 * lam * A * A) / D, hmax=hmax, hmin=hmin,
                           stable=bool(hmax <= 1 + 1e-12 and hmin >= -1 - 1e-12),
                           c_min=min(x[0] for x in cs), c_max=max(x[1] for x in cs),
                           c_formula=stiff_formula(Q, A, kP, P0, D - dP))
                rows.append(row)
    stable = [r for r in rows if r["stable"]]
    best = max(stable, key=lambda r: r["c_min"]) if stable else None
    unstable_fast = sorted([r for r in rows if not r["stable"]], key=lambda r: -r["c_U_over_D"])[:5]
    out = dict(rows=rows, n=len(rows), n_stable=len(stable), best_stable=best, c_Q=float(np.sqrt((Q - 1) / (3 * Q))),
               max_stable_c_U_over_D=max((r["c_U_over_D"] for r in stable), default=None), started=stamp())
    save("LC2_cone_scan", out)
    print("n", len(rows), "stable", len(stable), "best", best, flush=True)
    for r in sorted(stable, key=lambda r: -r["c_min"])[:6]:
        print("  stable", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
    for r in unstable_fast[:4]:
        print("  unstable", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)


if __name__ == "__main__" and sys.argv[1] == "lc2":
    lc2()
