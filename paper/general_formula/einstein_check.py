"""The Einstein rows from Rule3's coefficients themselves (COMPUTED, no run of the engine): a record's packet moves by the
geometric optics of its band, x' = d omega / d k, k' = - d omega / d x, with omega(k, U) the rotation Rule3's coefficients give
at the paces of a static well U(r) = U_1 / r (the held level over the Node clock). Measured, not assumed: light's deflection
past the well against Newton's 2 U_1 / b and Einstein's 4 U_1 / b, and a massive orbit's periapsis advance against
Einstein's 6 pi U_1 / (a (1 - e^2)). Two forms of the self coefficient: the law's line (S = 12 den G^2 - 12 (den - num) p_0^2
- 4 num SUM p_a^2, the conformal pace) and the engine on main (S = 12 den G^2 - 6 (den - num)(p_0^2 + G^2) - 4 num SUM p_a^2);
two readings of the Link's pace: once (p_a = p_0) and twice (p_a = Gamma - 2 c). The band taken isotropic at small k
(SUM cos k_a = 3 - k^2 / 2) so that the lattice's cubic anisotropy adds no precession of its own."""

import numpy as np
from scipy.integrate import solve_ivp

MATTER = (4000, 6000)
LIGHT = (6000, 6000)


def make(pair, variant, link_twice):
    num, den = pair

    def AB(U):
        P0 = 1 - U
        Pa = 1 - 2 * U if link_twice else P0
        if variant == "law":
            S = 2 - 2 * (den - num) / den * P0**2 - (2 * num / (3 * den)) * 3 * Pa**2
        else:
            S = 2 - (den - num) / den * (P0**2 + 1) - (2 * num / (3 * den)) * 3 * Pa**2
        B = (2 * num / (3 * den)) * Pa**2  # times SUM cos k_a
        return S, B

    def dAB(U, h=1e-6):
        S1, B1 = AB(U + h)
        S0, B0 = AB(U - h)
        return (S1 - S0) / (2 * h), (B1 - B0) / (2 * h)

    def rhs(t, y, U1):
        x, yy, kx, ky = y
        r = np.hypot(x, yy)
        U = U1 / r
        S, B = AB(U)
        k2 = kx * kx + ky * ky
        C = S + B * (3 - k2 / 2)  # 2 cos omega
        c = C / 2
        dw_dC = -1 / (2 * np.sqrt(max(1e-300, 1 - c * c)))  # d omega / d(2 cos omega)
        dSdU, dBdU = dAB(U)
        dC_dU = dSdU + dBdU * (3 - k2 / 2)
        dU_dx, dU_dy = -U1 * x / r**3, -U1 * yy / r**3
        vx, vy = dw_dC * (-B * kx), dw_dC * (-B * ky)
        fx, fy = -dw_dC * dC_dU * dU_dx, -dw_dC * dC_dU * dU_dy
        return [vx, vy, fx, fy]

    return rhs, AB


def bending(variant, link_twice, U1=0.05, b=20.0, L=4000.0):
    rhs, AB = make(LIGHT, variant, link_twice)
    k0 = 0.05
    sol = solve_ivp(
        rhs, (0, 2 * L / 0.55), [-L, b, k0, 0.0], args=(U1,), rtol=1e-11, atol=1e-13, method="DOP853"
    )
    kx, ky = sol.y[2, -1], sol.y[3, -1]
    return -np.arctan2(ky, kx)


def perihelion(variant, link_twice, U1=0.05, r0=120.0, k_tangential=None, orbits=6):
    rhs, AB = make(MATTER, variant, link_twice)
    # a first orbit to read the circular wave number at r0, then the tangential k lowered for an eccentric orbit
    if k_tangential is None:
        # v_circ from the force at rest: k' = -dw/dx; choose k so that centripetal balance holds by bisection on r_min
        def rmin_of(k):
            s = solve_ivp(
                rhs,
                (0, 4e5),
                [r0, 0, 0, k],
                args=(U1,),
                rtol=1e-10,
                atol=1e-12,
                method="DOP853",
                dense_output=False,
                max_step=50,
            )
            r = np.hypot(s.y[0], s.y[1])
            return r.min()

        lo, hi = 0.005, 0.2
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if rmin_of(mid) < 0.6 * r0:
                lo = mid
            else:
                hi = mid
        k_tangential = hi
    peri_angles = []

    def event(t, y, U1):
        x, yy, kx, ky = y
        return x * (rhs(t, y, U1)[0]) + yy * (rhs(t, y, U1)[1])  # d(r^2)/dt / 2

    event.direction = 1  # r decreasing -> increasing: the periapsis
    sol = solve_ivp(
        rhs,
        (0, 2e6),
        [r0, 0, 0, k_tangential],
        args=(U1,),
        rtol=1e-11,
        atol=1e-13,
        method="DOP853",
        events=event,
        max_step=20,
    )
    r = np.hypot(sol.y[0], sol.y[1])
    for ev in sol.y_events[0][: orbits + 1]:
        peri_angles.append(np.arctan2(ev[1], ev[0]))
    a = 0.5 * (r.min() + r.max())
    e = (r.max() - r.min()) / (r.max() + r.min())
    adv = np.diff(np.unwrap(peri_angles))
    adv = adv - 2 * np.pi * np.round(adv / (2 * np.pi))
    return a, e, adv.mean(), len(adv)


print(
    "LIGHT'S BENDING at U_1 = 0.05, the impact parameter b = 20: Newton's 2 U_1 / b = 0.0050, Einstein's 4 U_1 / b = 0.0100"
)
for variant in ("law", "main"):
    for twice in (False, True):
        d = bending(variant, twice)
        print(
            f"   S of {variant:4}, the Link {'twice' if twice else 'once '}: deflection {d:.5f} rad = {d / 0.005:.2f} x Newton's"
        )
print(
    "A MASSIVE ORBIT (the matter pair): the periapsis advance per orbit against Einstein's 6 pi U_1 / (a (1 - e^2))"
)
for variant in ("law", "main"):
    for twice in (False, True):
        a, e, adv, n = perihelion(variant, twice)
        gr = 6 * np.pi * 0.05 / (a * (1 - e * e))
        print(
            f"   S of {variant:4}, the Link {'twice' if twice else 'once '}: a {a:6.1f}, e {e:.3f}, the advance {adv:+.5f} rad per orbit over {n} orbits = {adv / gr:+.2f} x Einstein's ({gr:.5f})"
        )
