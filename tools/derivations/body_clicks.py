"""A body's clicks from Rule3's one-Node line (ALGEBRA.md, What a body does, in the words of the clicks; The two-mode line; the paper's Section 7.4, S.14, S.16, S.42 and S.43): the resonance's envelope, the uniformly moving body that writes no travelling light in the long-wavelength band, the steady rotation that writes none, the adiabatic invariant A^2 sin omega with the count's drift of Eq. (13), Planck's relation on the lattice, Rabi's rate checked on a two-Node body, the one-mode line's absence under the rotation, and Millikan's slope T.

Every rotation is the band's at a pace, `rule3.dispersion_at_paces`, and every speed the band's; the one-Node line a_next + a_before = 2 cos omega a_now is the line at k = 0.

Usage: `python tools/derivations/body_clicks.py` prints them.
"""

from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # the folder's root, rule3.py, by its file
import rule3  # noqa: E402
import units  # noqa: E402

LIGHT_PAIR = (1, 1)
MATTER_PAIR = (2, 3)  # the paper's computed pair, cos omega_0 = 2 / 3, omega_0 = 0.841
ACTION = 32768  # T of the examples (units.py)
GAMMA = 6000  # the law's Gamma in its examples (The frozen Node has no share, "4.70 at Gamma = 6,000")
WELL_CONTENT = 600  # the content c of the moving well's example, U = c / Gamma = 0.1
# S.14's check: the rotation lowered from 0.841 to 0.600 over 20,000 intervals
INVARIANT_START, INVARIANT_END, INVARIANT_INTERVALS = 0.841, 0.600, 20_000
# S.16's check: 2 cos omega_b = 1.4317 and epsilon = 0.013 at the one-mode line 2 omega_b
ONE_MODE_COSINE, ONE_MODE_EPSILON = 1.4317 / 2, 0.013
# the modulation of the two-Node body's Node 0 for the Rabi check, first order
RABI_EPSILON = 0.02
# the breathing body's radiated factor 3 sqrt 3 / (4 pi) (S.42 (c))
UNIFORM_PACES = (1, 1, 1)


def rotation_at_rest(num: int, den: int, clock: float = 1.0) -> float:
    """omega_b at k = 0 at the clock's pace p_0 / Gamma = clock: cos omega_b = 1 - (1 - num / den) clock^2 (The band at a pace)."""
    return math.acos(rule3.dispersion_at_paces((0.0, 0.0, 0.0), num, den, 1, clock, UNIFORM_PACES))


def resonance_envelope() -> list[float]:
    """[the transferred share at the detuning 0, at the detuning 2 Omega_R, the full width at half transfer in units of Omega_R]: 1, 1 / 2 and 4; Rabi's law P = [g^2 / (g^2 + Delta^2 / 4)] sin^2(sqrt(g^2 + Delta^2 / 4) t) oscillates at every detuning with that envelope (S.43 (d)), the meeting of a quantum with the body's own transition."""

    def envelope(delta: float) -> float:
        return 1 / (1 + delta * delta / 4)

    low, high = 0.0, 10.0
    for _ in range(100):
        middle = (low + high) / 2
        if envelope(middle) > 0.5:
            low = middle
        else:
            high = middle
    return [envelope(0.0), envelope(2.0), 2 * (low + high) / 2]


def uniform_motion_writes_no_light() -> list[float]:
    """[light's phase speed omega / k at the zone's edge along an axis, matter's largest group speed along the diagonal at the computed pair]: 0.392 and 0.385 Links per interval; a uniformly moving source is phase-matched to travelling light only where its speed reaches light's phase speed, which falls to 0.392 at the zone's edge, and no body of the computed pair reaches it (S.42 (b))."""
    edge = math.acos(rule3.plane_wave_dispersion(math.pi, *LIGHT_PAIR)) / math.pi
    num, den = MATTER_PAIR
    best, h = 0.0, 1e-6
    for i in range(1, 1000):
        kappa = math.pi * i / 1000
        omega = [
            math.acos(rule3.dispersion_at_paces((x, x, x), num, den, 1, 1, UNIFORM_PACES))
            for x in (kappa - h, kappa + h)
        ]
        best = max(best, (omega[1] - omega[0]) / (2 * h * math.sqrt(3)))
    return [edge, best]


def one_node_line(start_now: float, start_before: float, cosines: list[float]) -> list[float]:
    """The one-Node line a_next = 2 cos omega_t a_now - a_before stepped over the cosines, returning every level from a_before on (Rule3's line at k = 0)."""
    levels = [start_before, start_now]
    for cosine in cosines:
        levels.append(2 * cosine * levels[-1] - levels[-2])
    return levels


def steady_rotation_writes_no_light() -> list[float]:
    """[the spread of W over 1,000 intervals of a body's plane record re = A cos omega_b t, im = e A sin omega_b t stepped by the one-Node line, the breathing body's radiated factor 3 sqrt 3 / (4 pi)]: 0 and 0.4135; W = -e A^2 sin omega_b at every interval, so the sign holder's source is constant and no travelling event is born; a breathing body writes at its beat with the second moment's factor (S.42 (a), (c))."""
    num, den = MATTER_PAIR
    omega = rotation_at_rest(num, den)
    amplitude, ellipticity, intervals = 1000.0, 0.5, 1000
    cosines = [math.cos(omega)] * intervals
    re = one_node_line(amplitude, amplitude * math.cos(-omega), cosines)
    im = one_node_line(0.0, ellipticity * amplitude * math.sin(-omega), cosines)
    wronskians = [re[t] * im[t - 1] - im[t] * re[t - 1] for t in range(1, len(re))]
    spread = (max(wronskians) - min(wronskians)) / abs(ellipticity * amplitude**2 * math.sin(omega))
    return [spread, 3 * math.sqrt(3) / (4 * math.pi)]


def invariant_and_drift() -> list[float]:
    """[the largest relative change of D / sin omega over S.14's run, D's final over initial, sin omega_end / sin omega_start]: 0 to 4 x 10^-5, 0.76 and 0.76; with omega lowered slowly from 0.841 to 0.600 the form D = a_t^2 - a_(t+1) a_(t-1) falls as sin omega while A^2 sin omega = D / sin omega is kept, the discrete adiabatic invariant, the first factor of Eq. (13) (S.14)."""
    cosines = [
        math.cos(INVARIANT_START + (INVARIANT_END - INVARIANT_START) * t / INVARIANT_INTERVALS)
        for t in range(INVARIANT_INTERVALS + 1)
    ]
    levels = one_node_line(1000.0, 1000.0 * math.cos(-INVARIANT_START), cosines)
    forms = [levels[t] ** 2 - levels[t + 1] * levels[t - 1] for t in range(1, len(levels) - 1)]
    invariants = [d / math.sin(math.acos(c)) for d, c in zip(forms, cosines, strict=True)]
    deviation = (max(invariants) - min(invariants)) / invariants[0]
    return [deviation, forms[-1] / forms[0], math.sin(INVARIANT_END) / math.sin(INVARIANT_START)]


def drift_under_a_moving_well() -> list[float]:
    """Eq. (13) between the vacuum and a well of content c = 600 at Gamma = 6,000 for the computed pair: [sin omega_b(c) / sin omega_b(0), p_i^2(0) / p_i^2(c), their product N(c) / N(0)]; the clock p_0 = Gamma (1 - 1 / Gamma)^c, the Node's pace p_i = p_0^2 / Gamma, the rotation at the pace (The paces; The band at a pace)."""
    num, den = MATTER_PAIR
    clock = rule3.clock_pace(GAMMA, WELL_CONTENT)
    pace = rule3.node_pace(clock, GAMMA)
    first = math.sin(rotation_at_rest(num, den, float(clock) / GAMMA)) / math.sin(
        rotation_at_rest(num, den)
    )
    second = float(rule3.node_pace(GAMMA, GAMMA)) ** 2 / float(pace) ** 2
    return [first, second, first * second]


def planck_on_the_lattice() -> list[float]:
    """[2 A^2 sin omega / T, the share 2 A^2 sin^2 omega / T] for one quantum laid by the count at the computed pair: 1 and sin omega_0 = 0.745; the share is the invariant I = A^2 sin omega / T times sin omega, E = hbar omega with T for hbar and sin omega for omega (S.14, "Planck's relation")."""
    num, den = MATTER_PAIR
    sine = math.sin(rotation_at_rest(num, den))
    squared = units.lay_squared(1, 1, num, den, ACTION)
    return [2 * squared * sine / ACTION, 2 * squared * sine * sine / ACTION]


def rabi_rate(epsilon_ij: float, omega_i: float, omega_j: float) -> float:
    """Omega_R = epsilon_ij / (4 sqrt(sin omega_i sin omega_j)), the two-mode line's transfer rate (The two-mode line; S.16)."""
    return epsilon_ij / (4 * math.sqrt(math.sin(omega_i) * math.sin(omega_j)))


def parametric_growth() -> list[float]:
    """[mu = epsilon / (4 sin omega_b), the growth per interval of the one-Node record modulated at 2 omega_b over 10,000 intervals]: 0.0047 and 0.0047 at S.16's 2 cos omega_b = 1.4317 and epsilon = 0.013, the one-mode line of the pace read."""
    omega = math.acos(ONE_MODE_COSINE)
    intervals = 10_000
    cosines = [
        ONE_MODE_COSINE + ONE_MODE_EPSILON / 2 * math.cos(2 * omega * t) for t in range(intervals)
    ]
    levels = one_node_line(1.0, math.cos(-omega), cosines)
    forms = [levels[t] ** 2 - levels[t + 1] * levels[t - 1] for t in range(1, len(levels) - 1)]
    tail, head = max(forms[-200:]), max(forms[:200])
    return [ONE_MODE_EPSILON / (4 * math.sin(omega)), math.log(tail / head) / (2 * (len(forms) - 200))]


def two_node_modes() -> tuple[float, float]:
    """(omega_s, omega_a) of a two-Node body of the computed pair, the x Ports joining the two Nodes and the other axes folded: 2 w cos omega_s = 6 R, 2 w cos omega_a = 2 R, so cos omega_s = num / den and cos omega_a = num / (3 den) (The line)."""
    num, den = MATTER_PAIR
    wall, reads, self_coefficient = rule3.coefficients(num, den)
    symmetric = (self_coefficient + 6 * reads[0]) / (2 * wall)
    antisymmetric = (self_coefficient + 2 * reads[0]) / (2 * wall)
    return math.acos(symmetric), math.acos(antisymmetric)


def rabi_transfer() -> list[float]:
    """[T_pi / the measured time of the first full transfer] on the two-Node body with Node 0's rotation modulated by epsilon cos(omega_L t) at omega_L = omega_a - omega_s: 1.0; the modes (1, 1) / sqrt 2 and (1, -1) / sqrt 2 give epsilon_ij = epsilon / 2, Omega_R = epsilon_ij / (4 sqrt(sin omega_s sin omega_a)) and T_pi = pi / (2 Omega_R) (S.16, "the two-mode line"; S.43 (d))."""
    num, den = MATTER_PAIR
    wall, reads, self_coefficient = rule3.coefficients(num, den)
    omega_s, omega_a = two_node_modes()
    rate = rabi_rate(RABI_EPSILON / 2, omega_s, omega_a)
    t_pi = math.pi / (2 * rate)
    line = omega_a - omega_s
    before = [math.cos(-omega_s), math.cos(-omega_s)]
    now = [1.0, 1.0]
    best_t, best = 0, 0.0
    for t in range(int(3 * t_pi)):
        # the line's right side over w at each Node: (4 R a_i + 2 R a_other + S a_i) / w, plus the modulation at Node 0
        drive = RABI_EPSILON * math.cos(line * t)
        nxt = [
            (4 * reads[0] * now[0] + 2 * reads[0] * now[1] + self_coefficient * now[0]) / wall
            + drive * now[0]
            - before[0],
            (4 * reads[0] * now[1] + 2 * reads[0] * now[0] + self_coefficient * now[1]) / wall
            - before[1],
        ]
        # the antisymmetric mode's form D = c^2 - c_next c_before with c = (a_0 - a_1) / sqrt 2
        c_before, c_now, c_next = (
            (before[0] - before[1]) / math.sqrt(2),
            (now[0] - now[1]) / math.sqrt(2),
            (nxt[0] - nxt[1]) / math.sqrt(2),
        )
        share = c_now * c_now - c_next * c_before
        if share > best:
            best, best_t = share, t
        before, now = now, nxt
    return [t_pi / best_t]


def one_mode_line_under_the_rotation() -> list[float]:
    """[the growth per interval of a one-Node plane record under the time turn theta_t = theta_L cos(2 omega_b t) at the one-mode line, the growth under the pace read at the same line]: 0 and 0.0047; the uniform turn is a gauge, z_t = e^(-i Phi_t) u_t with u on the plain line, so the moduli never change and no resonance is driven (S.43 (a)), where the pace read grows at mu (S.16)."""
    omega = math.acos(ONE_MODE_COSINE)
    intervals = 10_000
    z_before, z_now = cmath.exp(1j * omega), 1 + 0j
    turn_before = cmath.exp(-1j * ONE_MODE_EPSILON / 2 * math.cos(-2 * omega))
    moduli = []
    for t in range(intervals):
        turn = cmath.exp(-1j * ONE_MODE_EPSILON / 2 * math.cos(2 * omega * t))
        z_next = turn * (2 * ONE_MODE_COSINE * z_now - turn_before * z_before)
        moduli.append(abs(z_next))
        z_before, z_now, turn_before = z_now, z_next, turn
    growth = math.log(max(moduli[-200:]) / max(moduli[:200])) / (intervals - 200)
    return [growth, parametric_growth()[1]]


def millikan_slope() -> list[float]:
    """[the residual of sin omega_j - sin omega_i = 2 cos((omega_i + omega_j) / 2) sin((omega_j - omega_i) / 2) at the two-Node body's modes, T (sin omega_j - sin omega_i) over T sin(omega_j - omega_i) at small modes 10^-3 and 2 x 10^-3]: 0 and 1 to 10^-6; one transition takes T (sin omega_j - sin omega_i) = T sin omega_L [1 - omega_i omega_j / 2 + O(omega^4)], one photon's share at the line, so a body reads hbar omega per click with the slope T (S.14, "the body's click")."""
    omega_s, omega_a = two_node_modes()
    residual = abs(
        math.sin(omega_a)
        - math.sin(omega_s)
        - 2 * math.cos((omega_s + omega_a) / 2) * math.sin((omega_a - omega_s) / 2)
    )
    small_i, small_j = 1e-3, 2e-3
    return [residual, (math.sin(small_j) - math.sin(small_i)) / math.sin(small_j - small_i)]


if __name__ == "__main__":
    print("the resonance's envelope:", [round(v, 4) for v in resonance_envelope()])
    print("uniform motion, the two speeds:", [round(v, 3) for v in uniform_motion_writes_no_light()])
    print("the steady rotation:", [round(v, 4) for v in steady_rotation_writes_no_light()])
    print("the invariant and the drift:", [round(v, 5) for v in invariant_and_drift()])
    print("the drift under a moving well:", [round(v, 4) for v in drift_under_a_moving_well()])
    print("Planck on the lattice:", [round(v, 4) for v in planck_on_the_lattice()])
    print("the parametric growth:", [round(v, 6) for v in parametric_growth()])
    print("the two-Node modes:", [round(v, 4) for v in two_node_modes()])
    print("the Rabi transfer:", [round(v, 3) for v in rabi_transfer()])
    print(
        "the one-mode line under the rotation:",
        [round(v, 6) for v in one_mode_line_under_the_rotation()],
    )
    print("Millikan's slope:", [round(v, 6) for v in millikan_slope()])
