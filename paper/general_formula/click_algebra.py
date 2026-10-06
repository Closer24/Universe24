"""The click's algebra beyond the law, S.55's witnesses (Section 2.5.2): the identities and the numbers of the
derivation checked in floating point, one Node and one Link, no run. Lemma A (the Wronskian of a
plane configuration is A^2 sin omega at every Node and free of the wave vector; the Link current of a real line
along an axis is -num A^2 sin omega sin k), the one-Node quadratic Q = x_t^2 + x_{t-1}^2 - 2 cos omega x_t x_{t-1}
with the norm factor 2 (a real line of amplitude 2A carries the two plane quanta's Q exactly), the matter band's
inertia m* = 3 tan omega_0 and kinetic scale c_m^2 = c^2 omega_0 / tan omega_0 at [2, 3] (c_m / c = 0.867),
Compton's factor omega_0 / tan omega_0 = 0.752 at [2, 3] against the exact quadratic of the two bands in the
Klein-Gordon form, absorption alone forbidden for c_m <= c, and the single-quantum pair threshold outside the
zone at [2, 3]; the twist's division on the magnitude with the sign carried, odd under an axis's inversion (the
accumulation of (i) at k_a = +-3 and at the boundary +-7 against M = 7), and the two recoils of (e), in rotation and
in the click's unit, their ratio cos omega_0, with the two Compton factors they give, 0.752 under the beat and 0.501
under the energy, distinct at [2, 3] and one at the closing gap. Every number here is the formula's; nothing is read
from a run.

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


def symmetric_divmod(k: int, count: int) -> tuple[int, int]:
    """The proposition's twist and remainder, the magnitude's floor division with the sign carried: delta k =
    sgn(k) (|k| div M) and r = sgn(k) (|k| mod M), so that k = M delta k + r with |r| < M and r of k's sign."""
    sign = (k > 0) - (k < 0)
    return sign * (abs(k) // count), sign * (abs(k) % count)


def kicks(k: int, count: int, clicks: int) -> list[int]:
    """The twist written at each of the first clicks, the accumulated remainder carried: the whole part of the
    accumulated wave number after each click less the one before."""
    whole = [symmetric_divmod(step * k, count)[0] for step in range(clicks + 1)]
    return [whole[step] - whole[step - 1] for step in range(1, clicks + 1)]


def booked_kicks(arrivals: list[int], count: int) -> tuple[list[int], int]:
    """The proposition's books for a sequence of arriving wave numbers of one axis, mixed in sign and size: the
    taker's books hold a signed remainder r with |r| < M; at a click with the arrival k the sum s = r + k gives the
    kick delta k = sgn(s) (|s| div M) and the new remainder r' = s - M delta k, so that r + k = M delta k + r' at
    every click (the identity asserted here) and M (sum of the kicks) + r = sum of the arrivals over any run."""
    books = 0
    kicked: list[int] = []
    for arrival in arrivals:
        total = books + arrival
        kick, rest = symmetric_divmod(total, count)
        assert books + arrival == count * kick + rest and abs(rest) < count, (books, arrival, kick, rest)
        assert rest == 0 or (rest > 0) == (total > 0), (total, rest)
        kicked.append(kick)
        books = rest
    assert count * sum(kicked) + books == sum(arrivals), (kicked, books, arrivals)
    return kicked, books


def band_omega(k: float, num: int, den: int) -> float:
    """The band along one axis, cos omega = (num / den)(1 - (1 - cos k) / 3)."""
    return math.acos((num / den) * (1 - (1 - math.cos(k)) / 3))


def compton_factors(num: int, den: int) -> tuple[float, float]:
    """Compton's non-relativistic factor under the beat rule, omega_0 / tan omega_0, and under a balance of the
    click's energy T sin omega, omega_0 cos^2 omega_0 / sin omega_0."""
    omega_0 = math.acos(num / den)
    return omega_0 / math.tan(omega_0), omega_0 * math.cos(omega_0) ** 2 / math.sin(omega_0)


def compton_out(omega_in: float, theta: float, beta: float, omega_0: float) -> float:
    """The outgoing rotation from the two bands in the Klein-Gordon form, the ratio c_m^2 / c^2, named beta here (1 at nature's gap)."""
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
        f"Compton at theta = pi/2, omega_L,in = {omega_in}: the shift at the finite gap over the shift at nature's gap "
        f"= {shift_gap / shift_nature:.3f} (the factor {beta:.3f}; the rest the relativistic term); "
        f"2 pi / (m* c) = {2 * math.pi / (3 * math.tan(omega_0) * C):.3f} Links against 2 pi / (sqrt 3 omega_0) = {2 * math.pi * C / omega_0:.3f}"
    )
    k_q, count = 3, 7
    for k_signed in (k_q, -k_q):
        kicked = kicks(k_signed, count, 7)
        at = [i + 1 for i, kick in enumerate(kicked) if kick]
        assert at == [3, 5, 7] and all(kick == (1 if k_signed > 0 else -1) for kick in kicked if kick), (
            k_signed,
            kicked,
        )
        print(
            f"the integer recoilless condition: k_a = {k_signed:+d}, M = {count}, the twist sgn(k_a) (|k_a| div M) = "
            f"{symmetric_divmod(k_signed, count)[0]}; the accumulated remainder gives one whole kick of {kicked[2]:+d} "
            f"per Link at the clicks {at} of seven"
        )
    assert kicks(count, count, 3) == [1, 1, 1] and kicks(-count, count, 3) == [-1, -1, -1], (
        "the boundary |k_a| = M"
    )
    for k_same in (3, -3, 7, 10):
        assert booked_kicks([k_same] * 7, count)[0] == kicks(k_same, count, 7), k_same
    mixed = [3, -5, 10, 3, 3, -7, 2]
    kicked_mixed, books = booked_kicks(mixed, count)
    assert (
        kicked_mixed == [0, 0, 1, 0, 1, -1, 0] and books == 2 and count * sum(kicked_mixed) + books == 9
    )
    print(
        f"the books with mixed arrivals {mixed} against M = {count}: the kicks {kicked_mixed}, the books {books}, "
        f"M (sum of the kicks) + the books = {count * sum(kicked_mixed) + books} = the arrivals' sum {sum(mixed)}; "
        f"one arrival repeated gives kicks() exactly"
    )
    for k_odd in (3, 7, 10):
        twist, rest = symmetric_divmod(k_odd, count)
        assert (
            symmetric_divmod(-k_odd, count) == (-twist, -rest)
            and k_odd == count * twist + rest
            and abs(rest) < count
        )
    print(
        f"the rule odd under k_a -> -k_a at +-3, +-7 and +-10 against M = {count}: "
        f"{[symmetric_divmod(k_odd, count) for k_odd in (3, -3, 7, -7, 10, -10)]}; the law's floor division would give "
        f"divmod(-3, 7) = {divmod(-3, 7)} against divmod(3, 7) = {divmod(3, 7)}"
    )
    k_small, count_large = 0.03, 1000
    recoil_rotation = count_large * (band_omega(k_small / count_large, num, den) - omega_0)
    recoil_energy = count_large * (
        math.sin(band_omega(k_small / count_large, num, den)) - math.sin(omega_0)
    )
    printed = k_small**2 / (2 * count_large * 3 * math.tan(omega_0))
    assert (
        abs(recoil_rotation / printed - 1) < 1e-5
        and abs(recoil_energy / recoil_rotation - math.cos(omega_0)) < 1e-6
    )
    beat_factor, energy_factor = compton_factors(num, den)
    closing = compton_factors(999_999, 1_000_000)
    assert abs(beat_factor - energy_factor) > 0.2 and abs(closing[0] - closing[1]) < 1e-5, (
        beat_factor,
        energy_factor,
        closing,
    )
    print(
        f"the two recoils at k = {k_small}, M = {count_large}: in rotation M [omega(k / M) - omega_0] = {recoil_rotation:.5e} "
        f"against k^2 / (2 M m*) = {printed:.5e}; in the click's unit M [sin omega(k / M) - sin omega_0] = {recoil_energy:.4e} "
        f"at T = 1, the ratio {recoil_energy / recoil_rotation:.6f} = cos omega_0 = {math.cos(omega_0):.6f}; the factors "
        f"{beat_factor:.4f} under the beat and {energy_factor:.4f} under the energy at [{num}, {den}], "
        f"{closing[0]:.6f} and {closing[1]:.6f} at [999999, 1000000]"
    )
    print(
        f"absorption alone: k_L (c^2 - c_m^2) = -2 c omega_0 gives k_L = {-2 * C * omega_0 / (C * C - c_m * c_m):.2f} < 0, forbidden; "
        f"the pair threshold k_L = 2 omega_0 / sqrt(c^2 - c_m^2) = {2 * omega_0 / math.sqrt(C * C - c_m * c_m):.2f} "
        f"against the zone's pi sqrt 3 = {math.pi * math.sqrt(3):.2f}"
    )


if __name__ == "__main__":
    main()
