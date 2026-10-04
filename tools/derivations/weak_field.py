"""The weak field's forms from Rule3's band at the composed paces (docs/ALGEBRA.md, The paces, "The paces compose" and "The Link is twice"; The rows against nature, rows (a), (a2), (b), (c), (d), (i), (j), (p) and (p2); the paper's Section 8 rows and S.15, S.18, S.19, S.20, S.30, S.41, S.47, S.58): the clock's share U = -ln(1 - 1 / Gamma) c, the clock N = e^(-U) and the Link pace N^2 under the one assumption p_a = p_0^2 / Gamma, read into rule3's band at a pace; from them the redshift's factor f(omega_0) and the Kepler column's gamma_K, beta_K and alpha_K, light's index e^(2U) and the light clock's 2U, the bending's 4 U_b and the push on a moving record, Shapiro's gamma = 1, the perihelion's 6 pi mu / (a (1 - e^2)) and Mercury's 43 arcseconds, the fall's coefficient and the equivalence between families, Newton's powers, the lens's chromatic 1 / 24, the shadow's 2e m and the clock in two places' 0.989. Every physical number is a named constant with its source; the numbers of nature stand where the paper's own mark rests on them, named so.

Usage: `python tools/derivations/weak_field.py` prints them.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent)
)  # the folder's root, rule3.py, beside this module
import rule3  # noqa: E402

COMPUTED_PAIR = (2, 3)  # the rule's own matter pair, the paper's computed pair (Section 8)
SMALL_GAP_PAIR = (999, 1000)  # the paper's small-gap illustration (Fig. 3, S.58)
GAMMA = 6000  # the engine's Gamma of the paper's worlds (Section 3.4)
LIGHT_SPEED_SQUARED = 1 / 3  # c^2 = 1 / 3 Link^2 per interval^2 (The lattice constants)
# the Kepler column's inputs of nature (row (d), a comparison at nature's pair)
SUN_GM = 1.32712440018e20  # m^3 / s^2, the Sun's gravitational parameter
LIGHT_SPEED = 299_792_458.0  # m / s
MERCURY_SEMI_MAJOR_AXIS = 5.7909e10  # m
MERCURY_ECCENTRICITY = 0.205630
MERCURY_ORBITS_PER_CENTURY = 36525 / 87.9691  # days per century over Mercury's period in days
ARCSECONDS_PER_RADIAN = 180 * 3600 / math.pi
# the equivalence between families (row (i), S.47): nature's inputs the estimate rests on
NEUTRON_OVER_ELECTRON = 1838.68  # the neutron's mass in electron masses
PROTON_OVER_ELECTRON = 1836.15  # the proton's mass in electron masses
BERYLLIUM_NEUTRON_FRACTION = 5 / 9  # beryllium-9's neutrons over its nucleons
TITANIUM_NEUTRON_FRACTION = 26 / 48  # titanium-48's neutrons over its nucleons
OMEGA_E_LHAASO = 3.7e-10  # the law's rounded bound on the electron's gap, row (i) (The constants)
OMEGA_E_MAGIC_AXIS = 2.0e-14  # the electron's gap at the MAGIC bound along an axis (S.24)
MAGIC_E_QG_2_GEV = 6.3e10  # MAGIC's quadratic bound E_QG,2, a number of nature (S.24)
EOT_WASH_BOUND = 1e-13  # nature's Be-Ti Eotvos bound (Will)
MICROSCOPE_BOUND = 1e-15  # nature's Ti-Pt bound (MICROSCOPE)
# the clock in two places (row (a2), S.41): a strontium clock at one metre for one second
STRONTIUM_LINE_HZ = 429.228e12
EARTH_GRAVITY = 9.807  # m / s^2
HEIGHT_M, DURATION_S = 1.0, 1.0


def rest_rotation(num: int, den: int) -> float:
    """omega_0 = arccos(num / den), the gap of the pair, from the band at k = 0 (rule3, cos omega = (num / (3 den)) (2 + cos k))."""
    return math.acos(rule3.plane_wave_dispersion(0.0, num, den))


def composed_paces(gamma: int, content: float) -> tuple[float, float, float]:
    """(U, p_0, p_a) at a content level: U = -c ln(1 - 1 / Gamma), the clock p_0 = Gamma e^(-U) (rule3.clock_pace at an integer c) and the Link pace p_a = p_0^2 / Gamma (rule3.node_pace), the one assumption h N = 1 (The paces)."""
    share = -content * math.log(1 - 1 / gamma)
    clock = gamma * math.exp(-share)
    return share, clock, float(rule3.node_pace(clock, gamma))


def rotation_at_content(k: float, num: int, den: int, gamma: int, content: float) -> float:
    """omega(k, U) along an axis at the composed paces, rule3.dispersion_at_paces with the clock and the three Link paces of `composed_paces`."""
    _, clock, link = composed_paces(gamma, content)
    return math.acos(rule3.dispersion_at_paces((k, 0.0, 0.0), num, den, gamma, clock, (link,) * 3))


def redshift_factors(num: int = 2, den: int = 3) -> list[float]:
    """Row (a): [f(omega_0) = 2 (1 - cos omega_0) / (omega_0 sin omega_0), the bound record's shift per U (S.15); 1 + alpha_K = tan omega_0 / omega_0, the shift per U_K (S.19)]: 1.063 and 1.329 at [2, 3], both 1 as the gap closes."""
    omega = rest_rotation(num, den)
    return [2 * (1 - math.cos(omega)) / (omega * math.sin(omega)), math.tan(omega) / omega]


def kepler_column(num: int = 2, den: int = 3) -> list[float]:
    """The two columns (S.18, S.19): [gamma_K = den / num, beta_K = (den + num) / (2 num), 1 + alpha_K = tan omega_0 / omega_0, alpha_U = f(omega_0) - 1]: 1.5, 1.25, 1.329 and 0.063 at [2, 3]; U_K = [2 cos omega_0 / (1 + cos omega_0)] U is the potential the orbits measure."""
    f, one_plus_alpha = redshift_factors(num, den)
    return [den / num, (den + num) / (2 * num), one_plus_alpha, f - 1]


def source_through_the_pace(gamma: int = GAMMA, content: int = 300) -> list[float]:
    """Inside matter the source is read through the pace, gravity gravitates (the paper's Section 6.5; S.34 (d)): a count source written at a Node of the clock p_0 and the Link paces p_a carries the factor p_x p_y p_z / (p_0 Gamma^2) in Rule3's bookkeeping, which at the composed paces of rule3 (clock_pace, node_pace) is N^5 = e^(-5U): [the exponent of N in that factor, ln(factor) / ln N, 5]."""
    clock = rule3.clock_pace(gamma, content)
    link = rule3.node_pace(clock, gamma)
    factor = link**3 / (clock * gamma * gamma)
    return [math.log(float(factor)) / math.log(float(clock) / gamma)]


def light_index_exponent(gamma: int = GAMMA, content: float = 300.0, k: float = 1e-3) -> list[float]:
    """Row (b), S.2: [ln n / U, the exponent of light's index n = c(0) / c(U) from the group velocity of light's band at the composed paces; d ln(rate) / dU of a light clock between two faces, S.15, whose round trip is 2 L / v_g]: 2 and -2, the Link's pace reading the content twice, the light clock falling by 2U."""
    share, _, _ = composed_paces(gamma, content)
    speed_vacuum = rotation_at_content(k, 1, 1, gamma, 0.0) / k
    speed_content = rotation_at_content(k, 1, 1, gamma, content) / k
    index_exponent = math.log(speed_vacuum / speed_content) / share
    return [index_exponent, -index_exponent]


def bending(num: int = 2, den: int = 3) -> list[float]:
    """Row (b), S.20 and S.58: [the bending's coefficient of U_b, 2 (the index's n - 1 = 2U) times the integral of b dl / (b^2 + l^2)^(3 / 2), which is 2 / b; gamma_K = den / num; the exact pull at rest -d omega / dU = 2 tan(omega_0 / 2); E = omega_0; the coefficient of beta^2 in the push, gamma_K - alpha_K / 2; the same coefficient against beta_v = v / c_m, times c_m^2 / c^2 = omega_0 / tan omega_0]: 4, 1.5, 0.8944, 0.8411, 1.335 and 1.0045 at [2, 3]."""
    omega = rest_rotation(num, den)
    integral = sum(
        1 / (1 + along * along) ** 1.5 * 1e-3 for along in (i * 1e-3 for i in range(-200_000, 200_000))
    )
    turn = 2 * integral  # b = 1: INTEGRAL b dl / (b^2 + l^2)^(3 / 2) = 2 / b
    gamma_k, _, one_plus_alpha, _ = kepler_column(num, den)
    coefficient = gamma_k - (one_plus_alpha - 1) / 2
    return [
        turn,
        gamma_k,
        2 * math.tan(omega / 2),
        omega,
        coefficient,
        coefficient * omega / math.tan(omega),
    ]


def push_on_a_moving_record(
    pairs: tuple[tuple[int, int], ...] = (COMPUTED_PAIR, SMALL_GAP_PAIR),
    gamma: int = GAMMA,
    k_over_gap: float = 1 / 100,
) -> list[float]:
    """S.58's check on the exact band: per pair [the rest push over E, -(d omega / dU) / omega at k = 0, the redshift's f(omega_0); the coefficient of beta^2 = (v / c)^2 in the push over its rest value, read at the wave number k = omega_0 / 100]; -(d omega / dU) at fixed k is the derivative of rule3's band at a pace through N = e^(-U), [2 (1 - nu) N^2 + (4 nu / 3) N^4 (1 - cos k)] / sin omega, at the vacuum N = 1: 1.0634 and 1.3354 at [2, 3], 1.00017 and 1.00067 at [999, 1000], both to 1 as the gap closes; the bending at beta = 1 is twice the rest push for every pair, the 4 U_b of row (b)."""
    out: list[float] = []
    for num, den in pairs:
        k = rest_rotation(num, den) * k_over_gap
        nu = num / den

        def push_over_energy(wave: float, num: int = num, den: int = den, nu: float = nu) -> float:
            omega = math.acos(
                rule3.dispersion_at_paces((wave, 0.0, 0.0), num, den, gamma, gamma, (gamma,) * 3)
            )
            pull = (2 * (1 - nu) + 4 * nu / 3 * (1 - math.cos(wave))) / math.sin(omega)
            return pull / omega

        rest = push_over_energy(0.0)
        velocity = rule3.group_velocity(k, num, den)
        beta_squared = velocity * velocity / LIGHT_SPEED_SQUARED
        out += [rest, (push_over_energy(k) / rest - 1) / beta_squared]
    return out


def shapiro_gamma(mu: float = 1.0, b: float = 1.0, x_1: float = 1e6, x_2: float = 1e6) -> list[float]:
    """Row (c), S.20: [1 + gamma from the delay, the integral of (n - 1) dl / c with n - 1 = 2 mu / r along the path, 2 sqrt 3 mu [arsinh(x_2 / b) + arsinh(x_1 / b)], over sqrt 3 mu ln(4 x_1 x_2 / b^2), nature's (1 + gamma) G M / c^3 form; gamma]: 2 and 1, Shapiro's delay at gamma = 1."""
    exponent, _ = light_index_exponent()
    delay = exponent * mu * math.sqrt(3) * (math.asinh(x_2 / b) + math.asinh(x_1 / b))
    one_plus_gamma = delay / (math.sqrt(3) * mu * math.log(4 * x_1 * x_2 / (b * b)))
    return [one_plus_gamma, one_plus_gamma - 1]


def perihelion(num: int = 2, den: int = 3) -> list[float]:
    """Row (d), S.19: [Mercury's advance per century in arcseconds from 6 pi mu / (a (1 - e^2)) at nature's inputs, a comparison; the Kepler column's factor (2 - beta_K + 2 gamma_K) / 3 of Einstein's, beta_K itself]: 43, 1.25 and 1.25 at [2, 3]."""
    mu = SUN_GM / LIGHT_SPEED**2
    per_orbit = 6 * math.pi * mu / (MERCURY_SEMI_MAJOR_AXIS * (1 - MERCURY_ECCENTRICITY**2))
    gamma_k, beta_k, _, _ = kepler_column(num, den)
    return [
        per_orbit * MERCURY_ORBITS_PER_CENTURY * ARCSECONDS_PER_RADIAN,
        (2 - beta_k + 2 * gamma_k) / 3,
        beta_k,
    ]


def fall_coefficient(num: int = 2, den: int = 3) -> list[float]:
    """Row (i), S.18: [a / |grad U| = 2 cos omega_0 / (3 (1 + cos omega_0)) from the band's curvature 1 / m* and d omega_0 / dU; the same as c^2 (1 - tan^2(omega_0 / 2)) (S.47); U_K / U = 2 cos omega_0 / (1 + cos omega_0)]: 0.2667, 0.2667 and 0.800 at [2, 3], 1 / 3, 1 / 3 and 1 as the gap closes."""
    omega = rest_rotation(num, den)
    nu = math.cos(omega)
    coefficient = 2 * nu / (3 * (1 + nu))
    return [coefficient, LIGHT_SPEED_SQUARED * (1 - math.tan(omega / 2) ** 2), 2 * nu / (1 + nu)]


def equivalence_between_families(omega_e_lhaaso: float = OMEGA_E_LHAASO) -> list[float]:
    """Row (i), S.47: [eta / omega_e^2 = (neutron fraction difference) (omega_n^2 - omega_p^2) / (4 omega_e^2); eta at the MAGIC bound; eta at the LHAASO bound; the electron against the proton, omega_p^2 / 4 at LHAASO]: 32.3, 1.3 x 10^-26, 4.4 x 10^-18 and 1.15 x 10^-13; the fall of a free packet is c^2 (1 - tan^2(omega_s / 2)) grad U, two families apart by (omega_n^2 - omega_p^2) / 4 at small gaps."""
    fraction = BERYLLIUM_NEUTRON_FRACTION - TITANIUM_NEUTRON_FRACTION
    gap_difference = NEUTRON_OVER_ELECTRON**2 - PROTON_OVER_ELECTRON**2
    per_omega_e_squared = fraction * gap_difference / 4
    return [
        per_omega_e_squared,
        per_omega_e_squared * OMEGA_E_MAGIC_AXIS**2,
        per_omega_e_squared * omega_e_lhaaso**2,
        (PROTON_OVER_ELECTRON * omega_e_lhaaso) ** 2 / 4,
    ]


def newton_powers(source: float = 1.0, radius: float = 50.0, step: float = 1e-3) -> list[float]:
    """Row (j): the massless holder's rest outside a body, l(r) = 3 s / (4 pi r) (the lattice's far kernel, ALGEBRA.md The lattice constants), gives [the power of r in the acceleration dl / dr, 2; the power in a circular orbit's v^2 = r dl / dr, 1], the log-slopes at r Links: Newton's pull and Kepler's fall-off."""

    def level(r: float) -> float:
        return 3 * source / (4 * math.pi * r)

    def pull(r: float) -> float:
        return -(level(r + step) - level(r - step)) / (2 * step)

    acceleration_power = -(math.log(pull(radius * 2)) - math.log(pull(radius))) / math.log(2)
    speed_power = -(
        math.log(2 * radius * pull(2 * radius)) - math.log(radius * pull(radius))
    ) / math.log(2)
    return [acceleration_power, speed_power]


def lens(num: int = 1, den: int = 1, content_share: float = 0.1, k: float = 0.3) -> list[float]:
    """Row (p), S.28: a stationary boundary conserves the rotation, so 1 - cos k_in = [1 - cos k + 3 (den - num) (1 - N^2) / num] / N^4 with N = e^(-U); [the residual of that k_in against rule3's band at the composed paces (0); light's long-wavelength index k_in / k over e^(2U) (1); the chromatic term's divisor, k^2 (e^(6U) - e^(2U)) over (k_in / k - e^(2U)) as k -> 0 (24)]."""
    n_factor = math.exp(-content_share)
    outside = rule3.plane_wave_dispersion(k, num, den)
    one_minus_cos = (1 - math.cos(k) + 3 * (den - num) * (1 - n_factor**2) / num) / n_factor**4
    k_in = math.acos(1 - one_minus_cos)
    clock, link = GAMMA * n_factor, GAMMA * n_factor**2
    inside = rule3.dispersion_at_paces((k_in, 0.0, 0.0), num, den, GAMMA, clock, (link,) * 3)
    small = 1e-3
    k_in_small = 2 * math.asin(math.sin(small / 2) / n_factor**2)
    index = k_in_small / small
    medium = 0.02  # the chromatic term read where k^4 is below the digits, k = 0.02
    chromatic = 2 * math.asin(math.sin(medium / 2) / n_factor**2) / medium - math.exp(2 * content_share)
    divisor = medium**2 * (math.exp(6 * content_share) - math.exp(2 * content_share)) / chromatic
    return [inside - outside, index / math.exp(2 * content_share), divisor]


def shadow(mass: float = 1.0) -> list[float]:
    """S.30: light's index n = e^(2U) with U = m / r; the photon sphere is where n r is least, found on a grid, and the capture radius b = n(r) r there: [r / m (2), b / m = 2e (5.44), Schwarzschild's 3 sqrt 3 (5.20), the excess in percent (4.6)]."""
    radii = [mass * (1 + i * 1e-4) for i in range(1, 40_000)]
    best = min(radii, key=lambda r: math.exp(2 * mass / r) * r)
    capture = math.exp(2 * mass / best) * best
    schwarzschild = 3 * math.sqrt(3) * mass
    return [best / mass, capture / mass, schwarzschild / mass, (capture / schwarzschild - 1) * 100]


def gravity_of_light(k: float = math.pi / 4, nodes: int = 24, intervals: int = 50) -> list[float]:
    """S.41 (2), row (p2): the one write, a holder of the content gains the form D = now^2 - next x before of every record over its wall (Section 3.5), and S.5's identity, D = A^2 sin^2 omega at every Node for a travelling wave as for a standing one, so a travelling light record's form summed over its Nodes is its share, its count n; a light packet of count n therefore writes n quanta per interval into the massless row as a static body of count n does, its clock's well is G_clock n / r^2 and a static body falls toward it at [1] x E / c^2; general relativity's pencil pulls at rho + 3 p / c^2 with p = rho c^2 / 3 along the beam, [2] x E / c^2 (Tolman). Computed from the three levels: a one-quantum light record a = A cos(k x - Omega t) travelling at rule3's Omega and a one-quantum matter record a = A cos(omega_0 t) resting at [2, 3], each on two lines (re and im, The conventions and the units, row 9) laid by the count over `nodes` Nodes, 2 A^2 sin omega = T per line (row 13), D summed over the lines, the Nodes and `intervals` intervals, per interval, against one quantum's form T sin omega (row 17); [the travelling record's quanta over the resting record's, the law's factor; general relativity's]: 1 and 2."""
    action = 32768  # T, the unit of action (row 10); the quanta below are ratios in which T cancels

    def quanta(wave_number: float, omega: float) -> float:
        amplitude_squared = action / (2 * math.sin(omega) * nodes)  # the lay per Node per line
        form = 0.0
        for t in range(intervals):
            for x in range(nodes):
                for line in (0.0, math.pi / 2):  # the two lines, re and im
                    phase = wave_number * x + line
                    now = math.cos(phase - omega * t)
                    nxt = math.cos(phase - omega * (t + 1))
                    before = math.cos(phase - omega * (t - 1))
                    form += amplitude_squared * (now * now - nxt * before)
        return form / intervals / (action * math.sin(omega))

    travelling = quanta(k, math.acos(rule3.plane_wave_dispersion(k, 1, 1)))
    resting = quanta(0.0, rest_rotation(*COMPUTED_PAIR))
    return [travelling / resting, 1 + 3 * (1 / 3)]


def clock_in_two_places() -> list[float]:
    """S.41 (1), row (a2): a bound body's beat Omega on two paths at the contents U_1 and U_2 for T accumulates the phase Omega Delta U T, Delta U = g h / c^2, and the fringes' visibility is |cos(Omega Delta U T / 2)|: [Delta U (1.09 x 10^-16), the phase (0.294 rad), the visibility (0.989)] for a strontium clock at one metre for one second."""
    beat = 2 * math.pi * STRONTIUM_LINE_HZ
    delta_u = EARTH_GRAVITY * HEIGHT_M / LIGHT_SPEED**2
    phase = beat * delta_u * DURATION_S
    return [delta_u, phase, abs(math.cos(phase / 2))]


if __name__ == "__main__":
    print("f(omega_0), 1 + alpha_K at [2, 3]:", [round(v, 3) for v in redshift_factors()])
    print("gamma_K, beta_K, 1 + alpha_K, alpha_U:", [round(v, 3) for v in kepler_column()])
    print("light's index exponent, the light clock's:", [round(v, 4) for v in light_index_exponent()])
    print(
        "the bending's 4, gamma_K, 2 tan(omega_0 / 2), omega_0, 1.335, 1.0045:",
        [round(v, 4) for v in bending()],
    )
    print("the push at [2, 3] and [999, 1000]:", [round(v, 5) for v in push_on_a_moving_record()])
    print("Shapiro's 1 + gamma, gamma:", [round(v, 4) for v in shapiro_gamma()])
    print("Mercury's arcseconds, the Kepler factor, beta_K:", [round(v, 3) for v in perihelion()])
    print("the fall's coefficient, S.47's form, U_K / U:", [round(v, 4) for v in fall_coefficient()])
    print("eta / omega_e^2, eta at MAGIC, at LHAASO, e against p:", equivalence_between_families())
    print("Newton's powers:", [round(v, 4) for v in newton_powers()])
    print("the lens's residual, index ratio, chromatic divisor:", lens())
    print("the shadow's r / m, 2e, 3 sqrt 3, percent:", [round(v, 3) for v in shadow()])
    print("the gravity of light, the law's and general relativity's:", gravity_of_light())
    print("the clock in two places: Delta U, phase, visibility:", clock_in_two_places())
