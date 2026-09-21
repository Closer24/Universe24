"""Open problem (3), the moving laboratory's anisotropy without a contraction:
the numbers of the read-only note (the G2 session, 2026-09-21; the Boss's
order of 15:00Z under record 396). A host derivation on the engine's own
flight rule (`direction_flight`, the one import; the Manhattan accumulator
of BEAM_LAW section 3 step 1 transcribed as `made_by`); no run, no fit, no
build.

(A) Nature's pins: Michelson and Morley 1887, the resonators of 2009 and
    2015, Kennedy and Thorndike 1932, Ives and Stilwell 1938, and the
    three coefficients of the Robertson-Mansouri-Sexl test theory.
(B) The continuum's ether clock at the register's speeds v = 1 / k Links
    per interval on a heading: the round trip along the motion gamma^2
    times the rest one, across gamma; the anisotropy gamma - 1.
(C) The GameBoard: a laboratory of the law (a lamp, a mirror d Links
    ahead on the heading, a mirror d Links across, all stepping one Link
    every k intervals), the two round trips in whole intervals from the
    flight rule, the difference in intervals and in fringes of the
    register's lamp (the turn 8: one fringe per 8 intervals).
(D) Nature's scale: the Earth's beta = 10^-4; the 1887 arm; the bound.
(E) The candidates: the Robertson-Mansouri-Sexl coefficients of each, the
    residual anisotropy of an arm that is the law's bond (DERIVATIONS
    12b.2's factors), the exact 1 / gamma of Lorentz's 1904 argument under
    the named identity source-velocity-v1, and the whole-Link grain of any
    contraction: the residual anisotropy of an arm of d Links contracted
    to the nearest whole Link, and the arm a null at 10^-17 needs.

Run from the repository root:

    PYTHONPATH=src python docs/designs/open_problems/moving_laboratory/moving_laboratory_map.py > docs/designs/open_problems/moving_laboratory/moving_laboratory_map.out
"""

from __future__ import annotations

import math

from event_universe.events.nature_beam import Q, direction_flight

HEADING_PACE = 32 / 55  # Links per interval on a heading: 2 Q / (2 T_D) with T_D = 110
FRINGE_INTERVALS = 8  # the register's lamp (series K): the turn 8, one fringe per 8 intervals
SPEEDS = (2, 4, 8, 16, 32)  # v = 1 / k Links per interval
ARMS = (6, 12, 24, 48)


def flight_of(vector: tuple[int, int, int]):
    """The flight constants of one direction vector: (S_1, T_D)."""
    flight = direction_flight((vector,))
    return int(flight.manhattan[0]), int(flight.resolution[0])


def made_by(age: int, s1: int, t_d: int) -> int:
    """Manhattan steps made by the age (BEAM_LAW section 3 step 1: the
    accumulator started at T_D, 2 S_1 Q per interval, a step per 2 T_D)."""
    return (2 * age * s1 * Q + t_d) // (2 * t_d)


def age_of(made: int, s1: int, t_d: int) -> int:
    """The first age at which the count reaches `made` Links."""
    age = 0
    while made_by(age, s1, t_d) < made:
        age += 1
    return age


def gamma(beta: float) -> float:
    return 1 / math.sqrt(1 - beta * beta)


def beta_of(k: int) -> float:
    return (1 / k) / HEADING_PACE


S1_H, TD_H = flight_of((1, 0, 0))


def along_round_trip(d: int, k: int) -> tuple[int, int, int]:
    """A row from the lamp at x = 0 at tick 0 on the heading +x; the mirror
    at x = d, both bodies stepping one Link at every tick that is a
    multiple of k (position d + tick // k). The mirror re-emits on -x in
    the interval of the click. Returns (forward transit, backward transit,
    round trip) in whole intervals."""
    tick = 0
    while made_by(tick, S1_H, TD_H) < d + tick // k:
        tick += 1
    forward = tick
    mirror_x = d + forward // k
    while mirror_x - made_by(tick - forward, S1_H, TD_H) > tick // k:
        tick += 1
    return forward, tick - forward, tick


def transverse_transit(d: int, k: int):
    """The row aimed at the mirror d Links across: on the direction (a, d)
    it reaches the point (a, d) at its Manhattan step a + d; the mirror is
    there when a == transit // k. Returns the exact hits (a, transit) and,
    if none, the nearest miss."""
    hits, nearest = [], None
    for a in range(0, d + 1):
        s1, t_d = flight_of((a, d, 0))
        transit = age_of(a + d, s1, t_d)
        miss = abs(a - transit / k)
        if a == transit // k:
            hits.append((a, transit))
        if nearest is None or miss < nearest[0]:
            nearest = (miss, a, transit)
    return hits, nearest


print("A. NATURE'S PINS")
print(
    "   Michelson and Morley 1887 (Am. J. Sci. 34, 333): the arm 11 m (multiplied by reflection), the expected shift on a 90-degree"
    " rotation 2 d beta^2 / lambda = 0.40 fringe at beta = 10^-4 (the Earth's orbital 30 km/s), observed below 0.01 (they wrote: less"
    " than one twentieth, probably less than one fortieth, of the expected)"
)
print(
    "   the resonators: delta c / c below about 10^-17 (Herrmann et al. 2009, Phys. Rev. D 80, 105011), 9.2 +- 10.7 x 10^-19 (Nagel"
    " et al. 2015, Nature Communications 6, 8174); the Kennedy-Thorndike form (unequal arms, the Earth's changing speed): Tobar et al."
    " 2010 at 10^-8 on the coefficient; Ives and Stilwell 1938 (the transverse Doppler) and Botermann et al. 2014 at 2.3 x 10^-9"
)
print(
    "   the Robertson-Mansouri-Sexl test theory (Robertson 1949; Mansouri and Sexl 1977): a moving laboratory's clock at 1 + alpha beta^2,"
    " its arm along the motion 1 + beta_L beta^2, across 1 + delta beta^2; Michelson-Morley reads beta_L - delta + 1 / 2, Kennedy-Thorndike"
    " alpha - beta_L + 1, Ives-Stilwell alpha + 1 / 2; relativity alpha = -1 / 2, beta_L = -1 / 2, delta = 0, the three coefficients 0;"
    " the ether at rest in the lattice alpha = beta_L = delta = 0: 1 / 2, 1, 1 / 2"
)
print()

print(
    "B. THE CONTINUUM'S ETHER CLOCK AT THE REGISTER'S SPEEDS (closed forms on the heading's pace c_h = 32 / 55 Links per interval)"
)
print(
    "   k | v = 1 / k | beta = v / c_h | round trip along, over 2 d / c_h (= gamma^2) | across (= gamma) | along / across = gamma | the anisotropy gamma - 1 | beta^2 / 2"
)
for k in SPEEDS:
    b = beta_of(k)
    g = gamma(b)
    print(
        f"   {k:2d} | {1 / k:.4f} | {b:.4f} | {g * g:.4f} | {g:.4f} | {g:.4f} | {g - 1:.4f} | {b * b / 2:.4f}"
    )
print(
    "   the forward leg d / (c_h - v), the backward d / (c_h + v), the transverse leg gamma d / c_h each way (the retarded distance);"
    " two arms of one length at right angles differ by gamma; Lorentz and FitzGerald closed the gap by contracting the arm along the motion"
    " by 1 / gamma; the law has no verb that contracts a Link (DERIVATIONS 12.1, 12.5 (iii))"
)
print()

print(
    "C. THE GAMEBOARD: THE LAW'S LABORATORY, THE TWO ROUND TRIPS IN WHOLE INTERVALS (the flight rule; the bodies step one Link per k intervals)"
)
print(
    "   d | k | beta | rest round trip 2 age_of(d) | along: forward, back, round trip | along / rest | gamma^2 | across: the direction (a, d) that"
    " the mirror meets, its transit, round trip | across / rest | gamma | along / across | gamma | the difference in intervals | in fringes of the turn 8"
)
lattice_rows = []
for d in ARMS:
    rest = 2 * age_of(d, S1_H, TD_H)
    for k in (4, 8, 16):
        b = beta_of(k)
        g = gamma(b)
        fwd, back, along = along_round_trip(d, k)
        hits, nearest = transverse_transit(d, k)
        if hits:
            a, transit = hits[0]
            tag = f"({a}, {d}) exact"
        else:
            _, a, transit = nearest
            tag = f"({a}, {d}) nearest (a - transit / k = {a - transit / k:+.2f})"
        across = 2 * transit
        diff = along - across
        lattice_rows.append((d, k, along, across))
        print(
            f"   {d:2d} | {k:2d} | {b:.4f} | {rest:3d} | {fwd:3d}, {back:3d}, {along:3d} | {along / rest:.3f} | {g * g:.3f} |"
            f" {tag}, {transit}, {across} | {across / rest:.3f} | {g:.3f} | {along / across:.3f} | {g:.3f} | {diff:+d} | {diff / FRINGE_INTERVALS:+.3f}"
        )
print(
    "   the along arm on the lattice: the forward leg chases a mirror that steps away, the backward leg meets a lamp that steps toward it;"
    " the whole intervals of the accumulator and the bodies' whole steps put the lattice above or below gamma^2 by a few percent (12.3's 1.375"
    " against 1.226 at k = 4 with one Link; here the arm is d Links and the ratio approaches the closed form as d grows)"
)
print(
    "   the across arm: the only rows that reach the co-moving mirror are the ones aimed at (a, d) with a the mirror's advance during the"
    " transit; their transit is the direction's own age at a + d, Pythagoras in the flight table's T_D (the lorentz note's Theorem 2)"
)
print(
    "   the fringe: the two arms' rows arriving together at the detector were born, or re-emitted, that many intervals apart; the wheel gives"
    " them phases that many eighths of a turn apart (the register's lamp, the turn 8); a rotation of the laboratory by 90 degrees swaps the"
    " arms and shifts the fringe by twice the difference"
)
print()

print("D. NATURE'S SCALE")
beta_earth = 1e-4
g_earth = gamma(beta_earth)
print(
    f"   the Earth's beta = 10^-4 (30 km/s): gamma - 1 = {g_earth - 1:.3e}; against the cosmic background 370 km/s: {gamma(370 / 299792.458) - 1:.3e}"
)
print(
    f"   the 1887 arm, 11 m at lambda = 5.5 x 10^-7 m: the shift on a 90-degree rotation 2 d beta^2 / lambda = {2 * 11 * beta_earth**2 / 5.5e-7:.2f} fringe; observed below 0.01"
)
print(
    f"   the resonators' 10^-17 against the law's {g_earth - 1:.1e}: {math.log10((g_earth - 1) / 1e-17):.1f} orders of magnitude (NATURE row 5b: FAIL by eight to nine)"
)
print()

print("E. THE CANDIDATES")
print(
    "   E1. The Robertson-Mansouri-Sexl coefficients of each candidate (0 is nature's; the value is the fraction of the ether's full effect)"
)
print(
    "   candidate | alpha (the clock) | beta_L (the arm along) | delta (the arm across) | Michelson-Morley beta_L - delta + 1 / 2 | Kennedy-Thorndike alpha - beta_L + 1 | Ives-Stilwell alpha + 1 / 2"
)
candidates = [
    ("(A) the law as built: the counter unslowed, the Links uncontracted", 0.0, 0.0, 0.0),
    (
        "(A') the law under covariant-readings-v1: the counter at 1 / gamma, the Links uncontracted (17.6 M4, M5)",
        -0.5,
        0.0,
        0.0,
    ),
    (
        "(B) the arm as the law's bond under the six (12b.2): the dispersion's factor s, here s = 0.87",
        -0.5,
        (0.87 - 1) / (beta_of(8) ** 2),
        0.0,
    ),
    ("(B) the same at s = 0.96", -0.5, (0.96 - 1) / (beta_of(8) ** 2), 0.0),
    (
        "(B) the same at the pins' elongation 1.2 (the retarded flux, no aberration)",
        -0.5,
        (1.2 - 1) / (beta_of(8) ** 2),
        0.0,
    ),
    (
        "(C) source-velocity-v1 (named, not designed): the magnetic part of the push, Lorentz's 1904 pair contracted by 1 / gamma exactly",
        -0.5,
        -0.5,
        0.0,
    ),
]
for name, al, bl, de in candidates:
    print(
        f"   {name} | {al:+.3f} | {bl:+.3f} | {de:+.3f} | {bl - de + 0.5:+.3f} | {al - bl + 1:+.3f} | {al + 0.5:+.3f}"
    )
print(
    "   (B)'s beta_L is the factor s written as 1 + beta_L beta^2 at 12b.2's beta = 0.2148 (k = 8), where relativity's s is 1 / gamma = 0.977:"
    " the six give a contraction of the wrong size (0.87 to 0.96 by the dispersion) or an elongation (1.2 by the retarded flux without the"
    " aberration), unstable (the bond unbound within 2200 intervals); a Michelson-Morley coefficient far from 0 either way"
)
print()
print(
    "   E2. The residual anisotropy of an arm along the motion that is s times its rest length: s gamma - 1 (0 at s = 1 / gamma)"
)
print(
    "   k | beta | gamma | 1 / gamma | s = 1 (no contraction) | s = 0.87 | s = 0.96 | s = 1.2 | s = 1 / gamma"
)
for k in (4, 8, 16):
    b = beta_of(k)
    g = gamma(b)
    print(
        f"   {k:2d} | {b:.4f} | {g:.4f} | {1 / g:.4f} | {g - 1:+.4f} | {0.87 * g - 1:+.4f} | {0.96 * g - 1:+.4f} | {1.2 * g - 1:+.4f} | {g / g - 1:+.4f}"
    )
print()
print(
    "   E3. The whole-Link grain of any contraction: an arm of d Links contracted to the nearest whole number of Links d' = round(d / gamma), the residual anisotropy d' gamma / d - 1"
)
print("   d | k | beta | d / gamma | d' | residual anisotropy | without the contraction gamma - 1")
for d in ARMS:
    for k in (4, 8, 16):
        b = beta_of(k)
        g = gamma(b)
        d_prime = round(d / g)
        print(
            f"   {d:2d} | {k:2d} | {b:.4f} | {d / g:.3f} | {d_prime:2d} | {d_prime * g / d - 1:+.4f} | {g - 1:+.4f}"
        )
need = 1 / (2 * 1e-17)
print(
    f"   the residual is at most gamma / (2 d): a null at 10^-17 with a contraction quantised to one Link needs an arm of at least {need:.1e} Links"
    f" ({math.log2(need):.1f} bits), the order of NATURE row 5a's bound on Q (5.8 x 10^16 for the one-way anisotropy); at the Earth's beta the"
    f" contraction of a 10^8-Link arm is {1e8 * (1 - 1 / g_earth):.2f} Link, below one: such an arm does not contract at all and reads the full"
    f" gamma - 1 = {g_earth - 1:.1e}"
)
