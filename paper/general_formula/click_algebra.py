"""The click's algebra beyond the law, S.57's witnesses (Section 2.5.2): the identities and the numbers of the
derivation checked in floating point, one Node and one Link, no run. Lemma A (the Wronskian of a
plane configuration is A^2 sin omega at every Node and free of the wave vector; the Link current of a real line
along an axis is -num A^2 sin omega sin k), the one-Node quadratic Q = x_t^2 + x_{t-1}^2 - 2 cos omega x_t x_{t-1}
with the norm factor 2 (a real line of amplitude 2A carries the two plane quanta's Q exactly), the matter band's
inertia m* = 3 tan omega_0 and kinetic scale c_m^2 = c^2 omega_0 / tan omega_0 at [2, 3] (c_m / c = 0.867),
Compton's factor omega_0 / tan omega_0 = 0.752 at [2, 3] against the exact quadratic of the two bands in the
Klein-Gordon form, absorption alone forbidden for c_m <= c, and the single-quantum pair threshold outside the
zone at [2, 3]. Every number here is the formula's; nothing is read from a run.

    python paper/general_formula/click_algebra.py
"""

from __future__ import annotations

import cmath
import math

C = 1 / math.sqrt(3)  # light's speed in Links per interval


def lemma_a(amplitude: float, omega: float, k: float, phase: float) -> tuple[float, float]:
    """The Wronskian's departure from A^2 sin omega and the Link current's from -A^2 sin omega sin k (num = 1)."""
    now = amplitude * cmath.exp(1j * phase)
    before = amplitude * cmath.exp(1j * (phase + omega))  # one interval earlier
    wronskian = now.real * before.imag - now.imag * before.real
    n_i, b_i = amplitude * math.cos(phase), amplitude * math.cos(phase + omega)
    n_j, b_j = amplitude * math.cos(phase + k), amplitude * math.cos(phase + k + omega)
    current = n_i * b_j - b_i * n_j
    return wronskian - amplitude**2 * math.sin(omega), current + amplitude**2 * math.sin(
        omega
    ) * math.sin(k)


def quadratic_real(amplitude: float, omega: float, phase: float) -> float:
    """Q of a real line B cos(phi - omega t) at one Node, B^2 sin^2 omega."""
    x, y = amplitude * math.cos(phase), amplitude * math.cos(phase + omega)
    return x * x + y * y - 2 * math.cos(omega) * x * y


def quadratic_plane(amplitude: float, omega: float, phase: float) -> float:
    """Q of a plane configuration A e^{i phi} at one Node, 2 A^2 sin^2 omega."""
    z, zb = amplitude * cmath.exp(1j * phase), amplitude * cmath.exp(1j * (phase + omega))
    return abs(z) ** 2 + abs(zb) ** 2 - 2 * math.cos(omega) * (z * zb.conjugate()).real


def compton_out(omega_in: float, theta: float, beta: float, omega_0: float) -> float:
    """The outgoing rotation from the two bands in the Klein-Gordon form, beta = c_m^2 / c^2 (1 at nature's gap)."""
    a = 1 - beta
    b = -2 * omega_in * (1 - beta * math.cos(theta)) - 2 * omega_0
    c = (1 - beta) * omega_in**2 + 2 * omega_0 * omega_in
    if a < 1e-15:
        return -c / b
    roots = [(-b - s * math.sqrt(b * b - 4 * a * c)) / (2 * a) for s in (1, -1)]
    return min((r for r in roots if r > 0), key=lambda r: abs(r - omega_in))


def main() -> None:
    worst = max(abs(v) for pars in ((1.3, 0.7, 0.4, 0.37), (0.8, 1.9, 2.2, 5.1)) for v in lemma_a(*pars))
    print(f"Lemma A: the two identities hold to {worst:.1e}")
    amplitude, omega = 1.3, 0.7
    real_two = quadratic_real(2 * amplitude, omega, 0.37)
    plane_two = 2 * quadratic_plane(amplitude, omega, 0.37)
    print(
        f"the norm factor: Q of the real line 2A cos phi = {real_two:.12f}, two plane quanta = {plane_two:.12f}, "
        f"one plane quantum = {quadratic_plane(amplitude, omega, 0.37):.12f}; B_q^2 = 2 A_q^2"
    )
    num, den = 2, 3
    omega_0 = math.acos(num / den)
    beta = omega_0 / math.tan(omega_0)
    c_m = C * math.sqrt(beta)
    k = 0.05
    omega_k = math.acos((num / den) * (1 - (1 - math.cos(k)) / 3))
    print(
        f"[{num}, {den}]: omega_0 = {omega_0:.4f}, m* = 3 tan omega_0 = {3 * math.tan(omega_0):.4f}, "
        f"omega(k) - omega_0 = {omega_k - omega_0:.3e} against k^2 / (2 m*) = {k * k / (6 * math.tan(omega_0)):.3e}; "
        f"c_m / c = {math.sqrt(beta):.3f}, the factor omega_0 / tan omega_0 = {beta:.3f}, "
        f"its first order 1 - (2/3)(1 - num/den) = {1 - (2 / 3) * (1 - num / den):.3f}"
    )
    omega_in, theta = 0.02, math.pi / 2
    shift_nature = omega_in - compton_out(omega_in, theta, 1.0, omega_0)
    shift_gap = omega_in - compton_out(omega_in, theta, beta, omega_0)
    print(
        f"Compton at theta = pi/2, Omega_in = {omega_in}: the shift at the finite gap over the shift at nature's gap "
        f"= {shift_gap / shift_nature:.3f} (the factor {beta:.3f}; the rest the relativistic term); "
        f"2 pi / (m* c) = {2 * math.pi / (3 * math.tan(omega_0) * C):.3f} Links against 2 pi / (sqrt 3 omega_0) = {2 * math.pi * C / omega_0:.3f}"
    )
    k_q, count = 3, 7
    kicks = [(step * k_q) // count - ((step - 1) * k_q) // count for step in range(1, 8)]
    print(
        f"the integer recoilless condition: k_q = {k_q} < M = {count}, k_q div M = {k_q // count}; the accumulated remainder "
        f"gives one whole kick per Link at the clicks {[i + 1 for i, kick in enumerate(kicks) if kick]} of seven"
    )
    print(
        f"absorption alone: K (c^2 - c_m^2) = -2 c omega_0 gives K = {-2 * C * omega_0 / (C * C - c_m * c_m):.2f} < 0, forbidden; "
        f"the pair threshold K = 2 omega_0 / sqrt(c^2 - c_m^2) = {2 * omega_0 / math.sqrt(C * C - c_m * c_m):.2f} "
        f"against the zone's pi sqrt 3 = {math.pi * math.sqrt(3):.2f}"
    )


if __name__ == "__main__":
    main()
