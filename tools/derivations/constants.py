"""The constants as readings of the lattice (ALGEBRA.md, The constants; the paper's Section 10.1 and 10.2, S.24 to S.27, S.44, S.53, S.54): from Rule3's band and the holder's rest line, with no number of nature but where the paper's mark itself rests on one, named below with its source. The chain: light's c^2 = 1 / 3 and the band's k^2 / 12 dispersion from rule3's band; the rest line's 3 at [1, 1] and the far kernel 3 / (4 pi r); G_clock / c^2 = 3 / (4 pi Gamma E_g) and Kepler's 2 cos omega_0 / (1 + cos omega_0) of it; the quantum one unit of the invariant, 2 A^2 sin omega = T, its Wronskian T / 2 for every family, so charge universality; alpha_law = (3 sqrt 3 / 8 pi) k / (Gamma E_s); the reciprocity; the energy line E_s T cos omega_s = k_w Gamma; the charge per record; the two forces' ratio between families; the Link's bound from MAGIC's dispersion limit; the dithered sub-unit level the clocks read; what the lattice fixes with no number; the calibration series; the masses from the click's structure. Roots in rule3.py; the lays' integer formulas are units.py's.

Usage: `python tools/derivations/constants.py` prints them.
"""

from __future__ import annotations

import math
from fractions import Fraction

try:
    import rule3
    import units
except ModuleNotFoundError:  # the gates load a module by its path, the folder not on sys.path
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import rule3
    import units

ACTION = 32768  # T = 2^15, the rule's universe (the paper's line 408)
MATTER = (2, 3)  # the rule's matter pair (line 170)
SHIPPED_MATTER = (4000, 6000)  # the shipped matter pair over Gamma = 6,000 (line 395)
SMALL_GAP = (999, 1000)  # a pair near the closing gap, the paper's second pair (moving_clock.py)
WIDE_GAP = (
    1,
    2,
)  # the pair of the paper's contact well, cosh kappa = 4 (families.py): with SMALL_GAP the two families a between-family check compares, their gaps a thousandfold apart
# the lay A^2 = isqrt(...) at T = 32,768 (units.py) floors by below one unit of 18,919 at [1, 2], a relative 5 x 10^-5 at most
# and 3.2 x 10^-5 as it falls: the tolerance of every between-family identity below that reads the lay
# the charged universe's integers and the turning file's, the energy line held exactly (line 571; S.26 (d'))
CHARGED = {"action": 36000, "gamma": 6000, "e_s": 1, "k_w": 4, "pair": (4000, 6000)}
TURNING = {"action": 36000, "gamma": 6000, "e_s": 100, "k_w": 400, "pair": (4000, 6000)}
RULE_FILE = {
    "action": 32768,
    "gamma": 6000,
    "k_w": 1,
    "pair": (2, 3),
}  # the file before the line (line 571)
CHARGED_RECORD_COUNT = 1  # every record reading the sign holder is one quantum of its family, count 1, writing its own held row (the law's line No record reads its own write of the sign, the hypotheses under their own names; S.60, line (1)); the loader's refusal of a higher count is that line's engine form and no ground
# nature's inputs the marks rest on, each named at the paper's line
FINE_STRUCTURE_INVERSE = 137.036  # 1 / alpha (line 571; S.26 (d))
MAGIC_QUANTUM_GRAVITY_GEV = (
    6.3e10  # MAGIC's subluminal quadratic bound E_QG,2 (Acciari et al. 2020; S.24)
)
MAGIC_PHOTON_GEV = 1.0e3  # the energy at which the bound is stated, 1 TeV (S.24)
WAVELENGTH_AT_ONE_TEV_M = 1.24e-18  # lambda of a 1 TeV photon (S.24)
REDUCED_COMPTON_M = 3.862e-13  # hbar / (m_e c), the electron's reduced Compton length (S.27)
ELECTRON_REST_MEV = 0.511  # m_e c^2 (S.27)
LHAASO_PHOTON_PEV = 1.4  # the highest photon observed (LHAASO; S.27)
PROTON_ELECTRON_MASS_RATIO = 1836.15  # m_p / m_e (line 571; S.44)
FORCE_RATIO_ELECTRON = 4.1656e42  # e^2 / (4 pi epsilon_0 G m_e^2) (line 571; S.44)
FORCE_RATIO_PROTON = 1.2356e36  # e^2 / (4 pi epsilon_0 G m_p^2) (line 571; S.44)
VACUUM_CONTENT = 0  # c_vac, declared 0 and read by no click (the calibration table, line 580)


def light_speed_squared() -> float:
    """c^2 = 1 / 3, light's band coefficient (cos omega_0 - cos omega(k)) / (1 - cos k) at [1, 1] on rule3's band (The lattice constants)."""
    k = math.pi / 2
    return (rule3.plane_wave_dispersion(0.0, 1, 1) - rule3.plane_wave_dispersion(k, 1, 1)) / (
        1 - math.cos(k)
    )


def rest_rotation(num: int, den: int) -> float:
    """omega_0 with cos omega_0 = num / den, rule3's band at k = 0."""
    return math.acos(rule3.plane_wave_dispersion(0.0, num, den))


def inertia(num: int, den: int) -> float:
    """m* = 3 tan omega_0, the band's curvature at rest (S.18): sin omega_0 omega''(0) = num / (3 den) from cos omega = cos omega_0 - (num / (3 den)) (1 - cos k)."""
    k = math.pi / 2
    coefficient = (
        rule3.plane_wave_dispersion(0.0, num, den) - rule3.plane_wave_dispersion(k, num, den)
    ) / (1 - math.cos(k))
    return math.sin(rest_rotation(num, den)) / coefficient


def source_coefficient() -> float:
    """The 3 of the holder's rest 3 G(r) s: at rest the line reads 2 w a = R S_6(a) + S a + w sigma, so Delta a = -(w / R) sigma, w / R = 3 den / num, 3 at [1, 1] (S.11, S.25)."""
    wall, reads, _ = rule3.coefficients(1, 1)
    return wall / reads[0]


def wronskian_per_quantum(num: int, den: int, action: int = ACTION) -> float:
    """A^2 sin omega / T, the Wronskian of one quantum laid by the count over the action, T / 2 for every family: the lay A^2 = isqrt(T^2 den^2 div (4 (den^2 - num^2))) of units.py (The conventions and the units, row 13) and sin omega from rule3's band."""
    return units.lay_squared(1, 1, num, den, action) * math.sin(rest_rotation(num, den)) / action


def link_dispersion_coefficient(k: float = 0.02) -> float:
    """1 / 12, the band's group speed along an axis (1 / sqrt 3) (1 - k^2 / 12) (S.1): (1 - v_g / c) / k^2 on rule3's band."""
    return (1 - rule3.group_velocity(k, 1, 1) / math.sqrt(light_speed_squared())) / (k * k)


def link_bound() -> list[float]:
    """The Link's bound from MAGIC's subluminal dispersion limit (line 571; S.24, S.27): |delta v / v| = (3 / 2) (E / E_QG,2)^2 at 1 TeV; the band's k^2 / 12 along an axis, from rule3, and its direction average: the band's k^4 term in omega^2 is -(k^4 / 36) (SUM_a n_a^4 - 1 / 3), -1 / 54 on an axis and -1 / 135 averaged with the sphere's SUM_a n_a^4 = 3 / 5, so the group speed's coefficient averaged is 1 / 12 times 2 / 5; k < sqrt(delta / coefficient), the Link k lambda / (2 pi) with lambda at 1 TeV, omega_e = the Link over the electron's unit sqrt 3 lambda_bar_e (S.27), gamma_K - 1 = omega_e^2 / 2; [omega_e along an axis in 10^-14, averaged in 10^-14, gamma_K - 1 along an axis in 10^-28, averaged in 10^-28, the orders by which LHAASO's bound on omega_e is slacker], 2.0, 3.1, 2.0, 4.9 and 4."""
    delta = 1.5 * (MAGIC_PHOTON_GEV / MAGIC_QUANTUM_GRAVITY_GEV) ** 2
    axis = link_dispersion_coefficient()
    sphere_fourth = Fraction(3, 5)  # the sphere's average of SUM_a n_a^4, three times <n_x^4> = 1 / 5
    averaged = axis * float((sphere_fourth - Fraction(1, 3)) / (1 - Fraction(1, 3)))
    unit = REDUCED_COMPTON_M / math.sqrt(
        light_speed_squared()
    )  # sqrt 3 lambda_bar_e, one Link per omega_e
    found = []
    for coefficient in (axis, averaged):
        wave_number = math.sqrt(delta / coefficient)
        link = wave_number * WAVELENGTH_AT_ONE_TEV_M / (2 * math.pi)
        found.append(link / unit)
    lhaaso = ELECTRON_REST_MEV / (LHAASO_PHOTON_PEV * 1e9)
    return [
        found[0] / 1e-14,
        found[1] / 1e-14,
        found[0] ** 2 / 2 / 1e-28,
        found[1] ** 2 / 2 / 1e-28,
        float(math.floor(math.log10(lhaaso / found[0]))),
    ]


def one_light_speed() -> list[float]:
    """A source and a reader of one family see one light speed, the band's own; in nature light's c is the same to 10^-28 at the MAGIC bound and 10^-20 at LHAASO's (line 534): [the difference of the band's c_s^2 = num / (3 den) for a source and a reader of the pair, 0; gamma_K - 1 = omega_e^2 / 2 at MAGIC's bound in 10^-28; at LHAASO's bound in 10^-20, the paragraph's 2.0 and 6.7]."""
    k = math.pi / 2
    coefficient = (
        rule3.plane_wave_dispersion(0.0, *MATTER) - rule3.plane_wave_dispersion(k, *MATTER)
    ) / (1 - math.cos(k))
    lhaaso = ELECTRON_REST_MEV / (LHAASO_PHOTON_PEV * 1e9)
    return [coefficient - coefficient, link_bound()[2], lhaaso * lhaaso / 2 / 1e-20]


def newton_constant() -> list[float]:
    """G_clock / c^2 = 3 / (4 pi Gamma E_g), that is G_clock = 1 / (4 pi Gamma E_g) (line 566; S.25): the holder's rest far from s quanta per interval is 3 s / (4 pi r) over E_g, the clock's share U = c / Gamma, nature's U = G M / (c^2 r) with M = s and c^2 = 1 / 3; [the rest line's 3 at [1, 1], the far kernel 3 / (4 pi), c^2, G_clock Gamma E_g = (3 / 4 pi) c^2 = 1 / (4 pi)]."""
    three = source_coefficient()
    far = three / (4 * math.pi)
    light = light_speed_squared()
    return [three, far, light, far * light]


def kepler_factor(num: int = 2, den: int = 3) -> list[float]:
    """Kepler's G, read from the orbits of matter as clicks, is [2 cos omega_0 / (1 + cos omega_0)] G_clock, 0.8 of it at [2, 3] (line 570; S.18): the fall a = (1 / m*) dk / dt with m* the band's inertia and dk / dt = -(d omega_0 / dU) |grad U| from the band at a pace with the clock Gamma e^(-U) and the Link Gamma e^(-2 U); nature's a = c^2 |grad U_K|, so U_K / U = a / (c^2 |grad U|); [a / |grad U|, 0.2667; U_K / U, 0.800]."""

    def rest(content: float) -> float:
        clock = math.exp(-content)
        return math.acos(
            rule3.dispersion_at_paces((0.0, 0.0, 0.0), num, den, 1, clock, (clock * clock,) * 3)
        )

    h = 1e-4
    slope = -(rest(h) - rest(-h)) / (2 * h)
    fall = slope / inertia(num, den)
    return [fall, fall / light_speed_squared()]


def charge_universality() -> list[float]:
    """Charge universality from two definitions, the quantum one unit of the invariant 2 A^2 sin omega = T and the sign holder's source the Wronskian A^2 sin omega = T / 2 for every family, so |q_p| = |q_e| by construction (line 571; S.26 (a)): [the Wronskian over T at [999, 1000], at [1, 2], their ratio], 1 / 2, 1 / 2 and 1 to the integer root's rounding, 3.2 x 10^-5 at [1, 2] (below one unit of A^2 = 18,919, 5 x 10^-5 at most), two families a thousandfold apart in their gaps, so the identity is tested across families and not by equal inputs."""
    first, second = wronskian_per_quantum(*SMALL_GAP), wronskian_per_quantum(*WIDE_GAP)
    return [first, second, second / first]


def alpha_law() -> list[float]:
    """alpha_law = (3 sqrt 3 / 8 pi) k / (Gamma E_s), independent of the family's gap (line 571; S.26 (a), (b)): one quantum writes s = W / (E_s T) = 1 / (2 E_s) per interval for every family, the angle at r is theta = 3 k s / (4 pi r Gamma) with the rest line's 3 and the far kernel, a reader's wave number changes by -grad theta = 3 k / (8 pi r^2 Gamma E_s), and Coulomb's dk / dt = alpha c / r^2 with c = 1 / sqrt 3 gives alpha = (3 sqrt 3 / 8 pi) k / (Gamma E_s); [the prefactor at k = Gamma E_s = 1, 0.20675; the write s at [999, 1000] over the write at [1, 2], 1 to the integer root's rounding 3.2 x 10^-5 at [1, 2], the gap cancelling across families]."""
    k, gamma, e_s, r = 1, 1, 1, 1.0
    source = 1 / (2 * e_s)  # W / (E_s T) with W = T / 2
    angle_slope = source_coefficient() * k * source / (4 * math.pi * r * r * gamma)  # -grad theta
    alpha = angle_slope * r * r / math.sqrt(light_speed_squared())
    return [alpha, wronskian_per_quantum(*SMALL_GAP) / wronskian_per_quantum(*WIDE_GAP)]


def reciprocal_pair(first: int = 3, second: int = 5) -> list[float]:
    """The reader sources the holder it reads at the same weight, so the pair is reciprocal (line 571; S.26 (c), S.43): a body of n quanta writes n / (2 E_s) per interval and feels n grad theta of the other's level, so the force on the first from the second's holder equals the force on the second from the first's; [their ratio], 1."""
    e_s, k, gamma, r = 1, 1, 1, 2.0

    def force(quanta_reading: int, quanta_writing: int) -> float:
        angle_slope = (
            source_coefficient() * k * (quanta_writing / (2 * e_s)) / (4 * math.pi * r * r * gamma)
        )
        return quanta_reading * angle_slope

    return [force(first, second) / force(second, first)]


def energy_line() -> list[float]:
    """A charged body and its light keep one energy by the line k_r E_s T cos omega_s = k_w Gamma (row 9 of the law's conventions and units table; the law's line What the lattice conserves, R316; line 571; S.26 (d')): the energy the body's clicks read and the holder's form move together under the turn and the write, both up for a body in its own level and both down for a pair of opposite senses, the sign the senses' product (a quantum of sense sigma in a level of source sense sigma_s goes from omega to omega + sigma sigma_s |theta| at its fixed Wronskian, theta = k_r Delta l / Gamma the turn, its energy T sin omega moving by sigma sigma_s T cos omega |theta|; the holder's form moving by k_w Delta l / E_s per quantum under the write), and the two agree to first order in the turn if and only if the line holds, one energy read twice; the ratio computed here is the magnitude, T (sin omega - sin(omega - theta)) / theta times E_s / (k_w Gamma) at k_r = 1 (T cos omega_s to first order), 1 under the line; [that ratio at the charged universe's integers, at the turning file's, T cos omega_s at the rule's file against its Gamma, 21,845 against 6,000]."""

    def clicks_over_form(action: int, gamma: int, e_s: int, k_w: int, pair: tuple[int, int]) -> float:
        omega = rest_rotation(*pair)
        theta = 1e-6  # the turn of one small level over Gamma, k_r = 1
        read = action * (math.sin(omega) - math.sin(omega - theta)) / theta  # the magnitude T cos omega
        return read * e_s / (k_w * gamma)

    charged = clicks_over_form(
        CHARGED["action"], CHARGED["gamma"], CHARGED["e_s"], CHARGED["k_w"], CHARGED["pair"]
    )
    turning = clicks_over_form(
        TURNING["action"], TURNING["gamma"], TURNING["e_s"], TURNING["k_w"], TURNING["pair"]
    )
    before = RULE_FILE["action"] * rule3.plane_wave_dispersion(0.0, *RULE_FILE["pair"])
    return [charged, turning, before, float(RULE_FILE["gamma"])]


def charge_per_record(records: int = 5) -> list[float]:
    """Many quanta of charge are that many records of count 1, the charge rows' derivations per record and additive over records (line 571; S.26; the law's line No record reads its own write of the sign, S.60 (1): every record reading the sign holder is one quantum of its family, count 1, writing its own held row): each record writes s = 1 / (2 E_s) per interval into its row, and the rest line is linear in its source, Delta a = -(w / R) sigma at the vacuum's paces (S.25; `source_coefficient`), so the rest of n records' writes is n times one record's and so is the angle it turns; [the count a charged record carries, the rest at n records' write over the rest at one's], 1 and n."""
    e_s = 1
    one = CHARGED_RECORD_COUNT / (2 * e_s)
    wall, reads, _ = rule3.coefficients(1, 1)

    def rest(source: float) -> float:
        return -wall / reads[0] * source  # Delta a = -(w / R) sigma, the rest line, linear in the source

    return [float(CHARGED_RECORD_COUNT), rest(records * one) / rest(one)]


def two_forces_ratio() -> list[float]:
    """(F_e / F_g)_e / (F_e / F_g)_p = (m_p / m_e)^2 with no number, an identity forced by charge universality and F_g proportional to m^2 (line 571; S.44): F_e / F_g = k E_g / (2 E_s sin^2 omega_s) at one family, the weights cancelling between two; [the identity's residual with the shipped weights k = 4, E_g = 1,000, E_s = 1 at [999, 1000] against [1, 2], two families a thousandfold apart in their gaps, exact in the rationals with sin^2 omega_0 = 1 - (num / den)^2, 0; (m_p / m_e)^2 in 10^6 from nature's ratio, 3.3714; nature's two force ratios' quotient in 10^6, 3.3713]."""
    k, e_g, e_s = 4, 1000, 1

    def sine_squared(num: int, den: int) -> Fraction:
        return (
            1 - Fraction(num, den) ** 2
        )  # sin^2 omega_0 at cos omega_0 = num / den, exact in the rationals

    def electric_over_gravity(num: int, den: int) -> Fraction:
        return Fraction(k * e_g, 2 * e_s) / sine_squared(num, den)

    between = electric_over_gravity(*SMALL_GAP) / electric_over_gravity(*WIDE_GAP)
    masses = sine_squared(*WIDE_GAP) / sine_squared(*SMALL_GAP)
    return [
        float(between - masses),
        PROTON_ELECTRON_MASS_RATIO**2 / 1e6,
        FORCE_RATIO_ELECTRON / FORCE_RATIO_PROTON / 1e6,
    ]


def dithered_level(gamma: int = 6000, source: Fraction = Fraction(1, 7)) -> list[float]:
    """Gamma reads nothing of omega_e or of alpha, and nothing of the clocks bounds it: the clocks read the mean of the write's dithered sub-unit level, the exact rest, and not Gamma (line 571; S.26 (e)): the write is the division act with the remainder kept, (numerator + r) div E, so a source s below one unit writes the level 1 once every 1 / s intervals and the clock p_0 = Gamma (1 - 1 / Gamma)^level reads the level 1 for that fraction of its intervals; [the mean level over a period less s, 0; the mean redshift 1 - p_0 / Gamma times Gamma, s, finer than the one unit 1 / Gamma]."""
    numerator, divisor = source.numerator, source.denominator
    remainder, levels = 0, []
    for _ in range(divisor):
        level, remainder = divmod(
            numerator + remainder, divisor
        )  # the division act, Euclid's with r kept
        levels.append(level)
    mean_level = Fraction(sum(levels), divisor)
    redshift = sum(1 - rule3.clock_pace(gamma, level) / gamma for level in levels) / divisor
    return [float(mean_level - source), float(redshift * gamma)]


def lattice_fixes() -> list[float]:
    """What the lattice fixes with no number (line 575; S.54): [the cube's group, the signed permutations of the three axes, 2^3 3! = 48; light's speed 1 / sqrt 3 from the band; the causal bound 1, the step's reach of one Link; the holders' far kernel 3 / (4 pi)]."""
    group = 2**rule3.AXES * math.factorial(rule3.AXES)
    count = 9
    reach = max(
        min(abs(j - i), count - abs(j - i))
        for i, ports in enumerate(rule3.chain_arrivals(count))
        for j in ports
    )
    return [
        float(group),
        math.sqrt(light_speed_squared()),
        float(reach),
        source_coefficient() / (4 * math.pi),
    ]


def calibration_series() -> list[float]:
    """The calibration series, each coefficient read by one click of nature in the form the lattice fixes (line 580; S.54): [Gamma E_s / k from Coulomb's force at nature's alpha, 1 / alpha times 3 sqrt 3 / (8 pi), 28.33; 4 pi Gamma E_g G_clock from Newton's G, 1; c_vac, declared 0]."""
    return [
        FINE_STRUCTURE_INVERSE * alpha_law()[0],
        4 * math.pi * newton_constant()[3],
        float(VACUUM_CONTENT),
    ]


def masses_from_the_click(num: int = 2, den: int = 3) -> list[float]:
    """What the click's structure derives of the masses (line 602; S.53, S.55): the rest energy m* c_m^2 = omega_0 exactly with m* the band's inertia and c_m^2 = omega_0 / m*; the ceiling m_p / m_e <= 1 / sin omega_e, the share T sin omega at most T; [m* c_m^2 / omega_0, 1; 1 / sin omega_0 in the rule's universe, 1.34; the ceiling at LHAASO's bound times m_e c^2 in PeV, 1.4, the photon's own energy]."""
    omega_0 = rest_rotation(num, den)
    kinetic_scale = omega_0 / inertia(num, den)
    lhaaso = ELECTRON_REST_MEV / (LHAASO_PHOTON_PEV * 1e9)
    return [
        inertia(num, den) * kinetic_scale / omega_0,
        1 / math.sin(omega_0),
        ELECTRON_REST_MEV / lhaaso / 1e9,
    ]


def universality_and_equivalence(gamma: int = 6000, content: int = 600) -> list[float]:
    """Charge universality and the equivalence between families follow from the writes (line 602): every family's quantum writes the Wronskian T / 2 into the sign holder, and every family's rest shifts by one factor at a Node, 1 - cos omega_b = (p_0 / Gamma)^2 (1 - cos omega_0) by the band at a pace (The clocks shift alike); [|q| at [1, 2] over |q| at [999, 1000], 1 to the integer root's rounding 3.2 x 10^-5 at [1, 2]; the clock's factor on 2 sin(omega_b / 2) at [1, 2] over the factor at [999, 1000], 1 exactly, each factor p_0 / Gamma], two families a thousandfold apart in their gaps."""
    clock = rule3.clock_pace(gamma, content)
    pace = rule3.node_pace(clock, gamma)

    def factor(num: int, den: int) -> float:
        shifted = math.acos(
            rule3.dispersion_at_paces((0.0, 0.0, 0.0), num, den, gamma, clock, (pace,) * 3)
        )
        return math.sin(shifted / 2) / math.sin(rest_rotation(num, den) / 2)

    return [
        wronskian_per_quantum(*WIDE_GAP) / wronskian_per_quantum(*SMALL_GAP),
        factor(*WIDE_GAP) / factor(*SMALL_GAP),
    ]


if __name__ == "__main__":
    print(
        "the Link's bound, omega_e (10^-14) axis and averaged, gamma_K - 1 (10^-28), orders:",
        link_bound(),
    )
    print("one light speed, the difference, gamma_K - 1 at MAGIC and LHAASO:", one_light_speed())
    print(
        "Newton's constant, 3, 3 / (4 pi), c^2, G_clock Gamma E_g:",
        [round(v, 4) for v in newton_constant()],
    )
    print("Kepler's factor, a / |grad U| and U_K / U:", [round(v, 4) for v in kepler_factor()])
    print(
        "charge universality, W / T twice and the ratio:", [round(v, 6) for v in charge_universality()]
    )
    print("alpha_law's prefactor and the gap's cancellation:", [round(v, 6) for v in alpha_law()])
    print("the reciprocal pair:", reciprocal_pair())
    print(
        "the energy line, charged, turning, the rule's T cos omega_s and Gamma:",
        [round(v, 3) for v in energy_line()],
    )
    print("the charge per record:", charge_per_record())
    print(
        "the two forces' ratio, residual, (m_p / m_e)^2, nature's (10^6):",
        [round(v, 5) for v in two_forces_ratio()],
    )
    print(
        "the dithered level, mean less s, the mean redshift times Gamma:",
        [round(v, 6) for v in dithered_level()],
    )
    print(
        "what the lattice fixes, 48, 1 / sqrt 3, 1, 3 / (4 pi):", [round(v, 4) for v in lattice_fixes()]
    )
    print("the calibration series, 28.33, 1, 0:", [round(v, 3) for v in calibration_series()])
    print(
        "the masses from the click, 1, 1 / sin omega_0, LHAASO's PeV:",
        [round(v, 4) for v in masses_from_the_click()],
    )
    print("universality and equivalence:", [round(v, 6) for v in universality_and_equivalence()])
