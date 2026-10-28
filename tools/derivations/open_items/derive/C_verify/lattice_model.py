"""Verifier's float model of the engine's A1 equations with no rounding (to separate the lattice's own frequency from
the integers' granularity): one complex mode a on the time gear X,
  matter:  p = W (a - a-), p+ = p - X (OmG^2 + OmM^2) a, W = (X- + X)/2, a+ = a + p+ / W+, W+ = (X + X+)/2,
           OmG^2 = (lam/3) Gamma / X (a Mesh's term: the mesh rate squared), OmM^2 = 2 (s/rim) (Gamma / X)^(1/2) (a spring),
  push:    X+ = 2 X - X- + k X (cG G + cV V),  G = OmG^2 |a|^2, V = OmM^2 |a|^2 (the draft: cG = 4, cV = 6),
  forms:   F = K + G + V, K = Re(conj(u_in) u_out), u_in = p / X, u_out = p+ / X.
E = X'^2/16 - (k/2) X^2 F is (V)'s first integral with continuity (k = kappa/3). Prints E on the seed's scale (k/2) X0^2 F0
early and late, and E's drift against the late (k/2) X^2 F, for several cV (cG) at a lattice frequency w0."""
import math
GAMMA = 1000.0

def course(cos0, lam, cG, cV, k, ticks, amp=1.0):
    s_rim = 1.0 - cos0
    X_b = X = GAMMA
    a = complex(amp, 0.0)
    om2 = (lam / 3) + 2 * s_rim            # at the vacuum
    w = math.acos(1 - om2 / 2) if om2 < 4 else math.pi
    a_b = a * complex(math.cos(-w), math.sin(-w))
    out = []
    Xs = [X]
    F_list = []
    for n in range(ticks):
        OG, OM = (lam / 3) * GAMMA / X, 2 * s_rim * math.sqrt(GAMMA / X)
        G, V = OG * abs(a) ** 2, OM * abs(a) ** 2
        W = (X_b + X) / 2
        p = W * (a - a_b)
        X_n = 2 * X - X_b + k * X * (cG * G + cV * V)
        p_n = p - X * (OG + OM) * a
        W_n = (X + X_n) / 2
        a_n = a + p_n / W_n
        K = ((p / X).conjugate() * (p_n / X)).real
        F_list.append(K + G + V)
        X_b, X, a_b, a = X, X_n, a, a_n
        Xs.append(X)
    res = []
    norm = (k / 2) * Xs[0] ** 2 * F_list[0]
    for n in range(1, ticks - 1):
        Xd = (Xs[n + 1] - Xs[n - 1]) / 2
        e = Xd * Xd / 16 - (k / 2) * Xs[n] ** 2 * F_list[n]
        res.append((n, Xs[n], e / norm, (k / 2) * Xs[n] ** 2 * F_list[n] / norm))
    return res

def report(label, cos0, lam, cGs_cVs, k, ticks):
    print(label)
    for cG, cV in cGs_cVs:
        r = course(cos0, lam, cG, cV, k, ticks)
        e0 = sum(x[2] for x in r[20:60]) / 40
        e1 = sum(x[2] for x in r[-40:]) / 40
        g1 = sum(x[3] for x in r[-40:]) / 40
        print(f"   cG {cG} cV {cV:.3f}: X {r[0][1]:.0f} -> {r[-1][1]:.3g};  E / E_seed-scale: early {e0:+.4f}, late {e1:+.4f}"
              f" (late (k/2) X^2 F on the same scale {g1:.3f}; E's drift / that {(e1 - e0) / g1:+.4f})")

k = 2e-6
report("a spring alone at cos w0 = 0.162 (the bang's heavy row), lam = 0:", 0.162, 0.0,
       [(4, 6.0), (4, 2 * (2 + 0.162)), (4, 3.0), (4, 9.0)], k, 3000)
report("a spring alone at cos w0 = 0.9:", 0.9, 0.0, [(4, 6.0), (4, 2 * (2 + 0.9)), (4, 3.0)], k, 3000)
report("a spring alone at cos w0 = 0.999 (near the continuum):", 0.999, 0.0, [(4, 6.0), (4, 2 * (2 + 0.999)), (4, 3.0)], 3e-8, 6000)
report("a Mesh's term alone (light) at lam = 6 (the quarter turn), cos w0 = 1:", 1.0, 6.0, [(4, 6.0), (3, 6.0), (5, 6.0)], k, 3000)
report("a Mesh's term alone (light) at lam = 1:", 1.0, 1.0, [(4, 6.0), (3, 6.0), (5, 6.0)], k, 3000)

print("slow courses (X moves a few per cent, the lattice frequency nearly fixed): which cV keeps E")
for cos0 in (0.162, 0.5, 0.9):
    best = None
    for cV in [x / 4 for x in range(8, 33)]:
        r = course(cos0, 0.0, 4, cV, 2e-8, 4000)
        e0 = sum(x[2] for x in r[20:120]) / 100
        e1 = sum(x[2] for x in r[-100:]) / 100
        g0 = sum(x[3] for x in r[20:120]) / 100
        g1 = sum(x[3] for x in r[-100:]) / 100
        d = (e1 - e0) / (g1 - g0)
        if best is None or abs(d) < abs(best[1]):
            best = (cV, d, r[-1][1])
    print(f"   cos w0 {cos0}: the cV with the least drift {best[0]} (drift / rise of (k/2) X^2 F {best[1]:+.4f}; X -> {best[2]:.0f});"
          f" the verifier's adiabatic formula 2 (2 + cos w0) = {2 * (2 + cos0):.3f}; the draft 6")
