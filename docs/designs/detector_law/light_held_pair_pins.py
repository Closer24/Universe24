"""The light-held pair in motion, member (iii) of PUSH_BALANCE.md section 5 on the lattice's
own band (COMPUTATION, before any run; derivation (a) of the Boss's order of 02:00Z on the owner's
question; DECLARATIONS.md section 10 item 8).

The standing condition of DESIGN.md 8b (iv) with the law's own frequency f = f_0 / gamma_m
(ALGEBRA.md 8.1 and 8.4, the massive kind's bound clock) on a chain: the rear body, moving at
v = 1 / k, emits forward at omega_1 with omega_1 - k(omega_1) v = omega_obj, the front body emits
backward at omega_2 with omega_2 + k(omega_2) v = omega_obj, k(omega) the chain's band cos omega =
(cos k + 2) / 3 (light's kind [1, 1]); nodes at both bodies give L (k_1 + k_2) = 2 pi m, so the
separation is L / L_0 = 2 k(omega_0) / (k_1 + k_2); the round trip is t_+ + t_- with the group
paces, L / (v_g(omega_1) - v) + L / (v_g(omega_2) + v); five's along ratio is that round trip in
the pair's OWN count over the rest count, (t_+ + t_-) / (gamma_m N_0). In the continuum (c
constant, gamma_m = gamma) the member gives L / L_0 = 1 / gamma and five's ratio 1 exactly
(PUSH_BALANCE.md section 4, the wave equation's covariance), printed as the check; on the band the
forward wave is Doppler-compressed into the lattice's dispersive range (5.8 Links at lambda_0 =
12 and k = 3), and five's ratio reads 1 + O((a / lambda)^2 beta^2), the lattice's own term,
tending to 1 as the wavelength grows or the speed falls. The rigid pair's ratio (the declared
separation, section 10 item 7) is printed beside. gamma_m by the one formula, the same expression
as coupled_mode_pins.py (c).

    PYTHONPATH=src python docs/designs/detector_law/light_held_pair_pins.py
"""

import math


def band_k(om):
    return math.acos(3 * math.cos(om) - 2)


def band_vg(om):
    # d omega / dk from cos omega = (cos k + 2) / 3: sin omega d omega = (sin k / 3) dk
    k = band_k(om)
    return math.sin(k) / (3 * math.sin(om))


def solve(f, lo, hi, tol=1e-13):
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def member_iii(lam0, k_step, num=800, den=809, continuum=False):
    c = 1 / math.sqrt(3)
    v = 1 / k_step
    k0 = 2 * math.pi / lam0
    om0 = c * k0 if continuum else math.acos((math.cos(k0) + 2) / 3)
    gamma = 1 / math.sqrt(1 - v * v / (c * c))
    w0 = math.acos(num / den)
    ceff2 = math.cos(w0) * (w0 / math.sin(w0)) * c * c
    gamma_m = gamma if continuum else 1 / math.sqrt(1 - v * v / ceff2)
    om_obj = om0 / gamma_m
    if continuum:

        def kf(om):
            return om / c

        def vg(om):
            return c

    else:
        kf, vg = band_k, band_vg
    top = (math.pi - 1e-9) if continuum else (math.acos(1 / 3) - 1e-9)
    om1 = solve(lambda om: om - kf(om) * v - om_obj, om_obj, top)
    om2 = solve(lambda om: om + kf(om) * v - om_obj, 1e-9, om_obj)
    k1, k2 = kf(om1), kf(om2)
    L_ratio = 2 * kf(om0) / (k1 + k2)
    L0 = 60.0  # L_0 = 60 as declared (section 13); the ratios do not depend on it
    L = L0 * L_ratio
    tp = L / (vg(om1) - v)
    tm = L / (vg(om2) + v)
    N0 = 2 * L0 / vg(om0)
    five_along = (tp + tm) / (gamma_m * N0)
    rigid_along = (L0 / (vg(om1) - v) + L0 / (vg(om2) + v)) / (gamma_m * N0)
    return dict(
        om0=om0,
        gamma=gamma,
        gamma_m=gamma_m,
        om1=om1,
        om2=om2,
        k1=k1,
        k2=k2,
        L_ratio=L_ratio,
        inv_gamma=1 / gamma,
        tp=tp,
        tm=tm,
        N0=N0,
        five_along=five_along,
        rigid_along=rigid_along,
        lam1=2 * math.pi / k1,
        lam2=2 * math.pi / k2,
    )


if __name__ == "__main__":
    for cont in (True, False):
        print(
            "CONTINUUM (c constant, gamma_m = gamma)"
            if cont
            else "THE CHAIN'S BAND, the massive kind [800, 809]"
        )
        for k_step in (3, 4):
            for lam0 in (12, 16, 24):
                r = member_iii(lam0, k_step, continuum=cont)
                print(
                    f"  k = {k_step}, lambda_0 = {lam0}: omega_0 {r['om0']:.5f}, gamma {r['gamma']:.5f}, gamma_m {r['gamma_m']:.5f};"
                    f" the two waves omega_1 {r['om1']:.4f} (lambda {r['lam1']:.2f}), omega_2 {r['om2']:.4f} (lambda {r['lam2']:.2f});"
                    f" L_along / L_0 = {r['L_ratio']:.4f} against 1 / gamma = {r['inv_gamma']:.4f};"
                    f" five's along ratio {r['five_along']:.4f} (the rigid pair's {r['rigid_along']:.4f})"
                )
