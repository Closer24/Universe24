"""Verifier's independent check of the draft's gauge and its three A1 equations (C), (V), (R), by numbers and not by
its algebra: GR's flat-or-curved Friedmann universe integrated in proper time tau (H^2 = kappa rho / 3 - k / a^2,
a''/a = -(kappa / 6)(rho + 3 p), each component's rho ~ a^(-3 (1 + w))), then the clock's tick t with dt = a dtau
(lapse 1 / a), X = Gamma a^4, F = 2 rho / a^2, S = 6 p / a^2; X(t) is sampled on a grid of t and differenced, and
the residuals of (C) X'^2 = (8 kappa / 3) X^2 F - 16 Gamma k X, (V) X'' = kappa X (F - S/3) - 8 Gamma k and
(R) X'' - X'^2 / (2 X) = -(kappa / 3) X (F + S) are read relative to their largest term. Floats (a check of the
continuum's algebra, not an engine probe). Also the mutations: (V) with (F - S/2) or the push X (F) of the head."""
import math
G, kappa = 1000.0, 3.0 / (1000.0 * 36000.0)

def run(comps, k, a0, adot0_sign, tau_end, n=200000):
    # comps: list of (w, rho0 at a0). Proper-time RK4 on (a, adot) with the constraint giving adot0.
    def rho_p(a):
        rho = sum(r0 * (a0 / a) ** (3 * (1 + w)) for w, r0 in comps)
        p = sum(w * r0 * (a0 / a) ** (3 * (1 + w)) for w, r0 in comps)
        return rho, p
    rho, p = rho_p(a0)
    h2 = kappa * rho / 3 - k / a0 ** 2
    adot = adot0_sign * math.sqrt(max(h2, 0.0)) * a0
    a, tau, t = a0, 0.0, 0.0
    dt_tau = tau_end / n
    samples = []
    def f(a, ad):
        r, pp = rho_p(a)
        return ad, -(kappa / 6) * (r + 3 * pp) * a
    peak = a
    for i in range(n):
        samples.append((t, a))
        peak = max(peak, a)
        if a < 0.6 * peak:      # stop well before a crunch
            break
        k1 = f(a, adot); k2 = f(a + 0.5 * dt_tau * k1[0], adot + 0.5 * dt_tau * k1[1])
        k3 = f(a + 0.5 * dt_tau * k2[0], adot + 0.5 * dt_tau * k2[1]); k4 = f(a + dt_tau * k3[0], adot + dt_tau * k3[1])
        a_new = a + dt_tau / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        ad_new = adot + dt_tau / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        t += 0.5 * dt_tau * (a + a_new)   # dt = a dtau (trapezoid)
        a, adot = a_new, ad_new
    return samples, rho_p

def check(name, comps, k, a0=1.0, tau_end=2000.0):
    samples, rho_p = run(comps, k, a0, +1, tau_end)
    worst = {"C": 0.0, "V": 0.0, "R": 0.0, "V_half": 0.0, "V_head": 0.0}
    for i in range(1000, len(samples) - 1000, 997):
        (t0, am), (t1, a1), (t2, ap) = samples[i - 1], samples[i], samples[i + 1]
        # differences on the nonuniform t grid
        Xm, X1, Xp = G * am ** 4, G * a1 ** 4, G * ap ** 4
        h1, h2 = t1 - t0, t2 - t1
        Xd = (Xp - Xm) / (h1 + h2)
        Xdd = 2 * ((Xp - X1) / h2 - (X1 - Xm) / h1) / (h1 + h2)
        rho, p = rho_p(a1)
        F, S = 2 * rho / a1 ** 2, 6 * p / a1 ** 2
        C_l, C_r = Xd ** 2, (8 * kappa / 3) * X1 ** 2 * F - 16 * G * k * X1
        V_r = kappa * X1 * (F - S / 3) - 8 * G * k
        R_l, R_r = Xdd - Xd ** 2 / (2 * X1), -(kappa / 3) * X1 * (F + S)
        scale_C = max(abs(C_l), abs(C_r), 1e-300)
        scale_V = max(abs(Xdd), abs(kappa * X1 * F), 1e-300)
        worst["C"] = max(worst["C"], abs(C_l - C_r) / scale_C)
        worst["V"] = max(worst["V"], abs(Xdd - V_r) / scale_V)
        worst["R"] = max(worst["R"], abs(R_l - R_r) / max(abs(R_l), abs(R_r), abs(Xd ** 2 / (2 * X1)), 1e-300))
        worst["V_half"] = max(worst["V_half"], abs(Xdd - (kappa * X1 * (F - S / 2) - 8 * G * k)) / scale_V)
        worst["V_head"] = max(worst["V_head"], abs(Xdd - (kappa * (4 / 3) * X1 * F - 8 * G * k)) / scale_V)
    print(f"{name:52s} worst relative residuals: (C) {worst['C']:.1e} (V) {worst['V']:.1e} (R) {worst['R']:.1e}"
          f" | mutated (V) with S/2: {worst['V_half']:.1e}, with (4/3) F: {worst['V_head']:.1e}")

rho0 = 1.0e7   # in units where kappa rho / 3 ~ 0.28
check("radiation (w = 1/3), flat", [(1 / 3, rho0)], 0.0)
check("dust (w = 0), flat", [(0.0, rho0)], 0.0)
check("stiff (w = 1), flat", [(1.0, rho0)], 0.0)
check("w = -1/3 (the quarter turn's rho + 3p = 0), flat", [(-1 / 3, rho0)], 0.0)
check("radiation + dust + curvature k > 0 (closed, through its top)", [(1 / 3, rho0), (0.0, 0.3 * rho0)], 0.05)
check("dust + Lambda < 0 (w = -1, rho < 0), flat, through its top", [(0.0, rho0), (-1.0, -0.02 * rho0)], 0.0, tau_end=200.0)
