"""The masses in the Beam Law, read in integers (the mathematician, 2026-09-20).

Standalone: the only thing imported from the engine is the collision
table's own class function (`nature_beam.class_key`), so that section A
reads the engine's rule and not a copy of it. Everything else is exact
integer arithmetic on the rules as BEAM_LAW states them (the clock
`by_clock`, the lamp's cost h x s, the flight table's pace) and a few
measured numbers of nature (CODATA 2018, PDG 2022) with their uncertainties.
Run from the checkout with `PYTHONPATH=src`; the output beside this file
(`ladder.out`) is what it printed.

Sections:
  A. the collision table: its cycles are content-blind (the only "loop" of
     free space);
  B. the bounds on a measured event's content (bounds, not rungs);
  C. the exchange of light between two lamps, the one dynamics of content in
     the law: every equal split of every total is a fixed point (a continuum,
     no ladder); checked against the engine's run of `examples/events/masses`;
  D. representability of nature's mass ratios on one integer grid (A10's
     test) and what it does and does not say;
  E. the harmonic ladder a self-referential window would give (NOT the law;
     the smallest rule named in DESIGN.md) against nature's spectrum;
  F. what the law does say about composites (no mass defect) against nature.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

from event_universe.events.nature_beam import class_key

Q = 64  # the label's scale, BEAM_LAW section 2


def by_clock(age: int, numerator: int, denominator: int) -> int:
    """core/integer.by_clock, restated: the whole part gained at one self-creation."""
    return ((age + 1) * numerator) // denominator - (age * numerator) // denominator


def flight_age(distance: int) -> int:
    """The age at which a ray on a heading has made `distance` Links
    (BEAM_LAW section 3: T_d = isqrt(3 Q^2) = 110 on a heading, m(tau) =
    (2 tau Q + T_d) // (2 T_d))."""
    t_d = math.isqrt(3 * Q * Q)
    tau = 0
    while (2 * tau * Q + t_d) // (2 * t_d) < distance:
        tau += 1
    return tau


def section(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# --------------------------------------------------------------------------
section("A. The collision table's cycles are content-blind")

classes: dict[object, list[tuple[int, ...]]] = {}
for state in itertools.product(range(3), repeat=8):
    classes.setdefault(class_key(state), []).append(state)
sizes = sorted(len(members) for members in classes.values())
histogram: dict[int, int] = {}
for size in sizes:
    histogram[size] = histogram.get(size, 0) + 1
print("slot states 3^8 =", 3**8, "; classes:", len(classes))
print("cycle length -> number of classes:", histogram)
fixed = sum(1 for members in classes.values() if len(members) == 1)
moving = sum(len(m) for m in classes.values() if len(m) > 1)
print("fixed states (a class of one):", fixed, "; states that move:", moving)
# The states whose occupied slots are the two rest slots alone: nothing
# leaves the Node, whatever the amount and the content of the rows.
rest_only = [
    s for s in itertools.product(range(3), repeat=8) if all(v == 0 for v in s[:6]) and any(s[6:])
]
print("states occupied on the rest slots alone:", len(rest_only), "->", rest_only)
for s in rest_only:
    members = classes[class_key(s)]
    print("   ", s, "class size", len(members), "members", members)
print(
    "class_key reads the slot codes (0 empty, 1 single, 2 crowd) and nothing else:\n"
    "    the amount enters only as single (1) or crowd (2), the content not at all;\n"
    "    a crowd slot is a wall the pattern never enters or leaves (BEAM_LAW section 4),\n"
    "    so a rest row of ANY amount above 1 and ANY content stays at its Node forever,\n"
    "    and a single at rest alternates ha <-> hb with period 2 for ANY content."
)

# --------------------------------------------------------------------------
section("B. The bounds on a measured event's content (bounds, not rungs)")

for K, N in ((2**20, 64), (4096, 64), (2**30, 64), (2**20, 4096)):
    # The frame refuses a turn of half the circle or more: 2 x by_clock(age, M, K) >= N.
    # by_clock takes the values floor(M / K) and ceil(M / K) over the ages, so
    # the largest admitted M is the largest with ceil(M / K) < N / 2.
    m_max = K * (N // 2 - 1)

    def largest_turn(m: int, K: int = K) -> int:
        # ceil(m / K), reached at some age unless K divides m (then m / K at every age).
        return -(-m // K)

    assert largest_turn(m_max) * 2 < N <= largest_turn(m_max + 1) * 2
    if K <= 4096:  # the scan over every age, where it is cheap, confirms the formula
        assert max(by_clock(a, m_max, K) for a in range(K)) == largest_turn(m_max)
        assert max(by_clock(a, m_max + 1, K) for a in range(K)) == largest_turn(m_max + 1)
    print(f"K = {K}, N = {N}: 1 <= M <= K (N/2 - 1) = {m_max}; the label bound Q M amount <= 2^62 - 1")
print("every integer M in the range is admitted: nothing between the bounds is refused.")

# --------------------------------------------------------------------------
section("C. The exchange of light between two lamps: every equal split is a fixed point")


def exchange(
    m_a: int, m_b: int, K: int, ticks: int, distance: int = 7, h: int = 1
) -> tuple[int, int, list[tuple[int, int, int]]]:
    """Two fixed lamps of one paid family (`quantum` h) facing each other
    `distance` Links apart, `suspension` 0, `release` irrelevant (paid), the
    lamp `rate` [1, 1], one direction each; each measures the other's units
    by the keys' rule (a paid arrival is measured). Per interval, in the
    engine's order: the frame reads the content M and the turn s =
    by_clock(age, M, K); the arrivals of this interval click and their
    content joins; then the self-creation releases one unit of content h s
    (cost h x s, BEAM_LAW step 5) when s > 0 and the content covers it. A
    unit born at interval t clicks at t + tau, tau the flight age of the
    distance. Returns the two contents after `ticks` and the trace."""
    tau = flight_age(distance)
    inbox_a: dict[int, int] = {}
    inbox_b: dict[int, int] = {}
    trace = []
    for t in range(1, ticks + 1):
        age = t - 1
        s_a, s_b = by_clock(age, m_a, K), by_clock(age, m_b, K)
        m_a += inbox_a.pop(t, 0)
        m_b += inbox_b.pop(t, 0)
        if s_a > 0 and m_a >= h * s_a:
            m_a -= h * s_a
            inbox_b[t + tau] = inbox_b.get(t + tau, 0) + h * s_a
        if s_b > 0 and m_b >= h * s_b:
            m_b -= h * s_b
            inbox_a[t + tau] = inbox_a.get(t + tau, 0) + h * s_b
        trace.append((t, m_a, m_b))
    return m_a, m_b, trace


print(
    "flight age of 7 Links on a heading:",
    flight_age(7),
    "intervals (the engine's first click at tick 13 for a birth at tick 1)",
)
K = 4096
a, b, trace = exchange(32768, 8192, K, 600)
print(f"unequal (32768, 8192), K = {K}, 600 intervals -> ({a}, {b}); the engine's run: (29634, 11209)")
assert (a, b) == (29634, 11209), "the standalone map must reproduce the engine integer by integer"
a, b, trace = exchange(32768, 8192, K, 6000)
print(f"unequal (32768, 8192), 6000 intervals -> ({a}, {b}); the engine's run at 6000: see cavity.out")
for t, x, y in trace:
    if t in (1, 100, 500, 1000, 2000, 3000, 4000, 5000, 6000):
        print(f"    t = {t:5d}: A {x:6d}  B {y:6d}  A - B {x - y:6d}  total on the lamps {x + y}")
a, b, trace = exchange(20480, 20480, K, 6000)
print(f"equal (20480, 20480), 6000 intervals -> ({a}, {b}); the engine's run at 600: (20420, 20420)")
print("the fixed points of the map (the content in transit, tau x s each way, held constant):")
for total in (2, 64, 4096, 8192, 40960, 65536, 2**18, 2**20 + 6):
    half = total // 2
    a, b, trace = exchange(half, total - half, K, 3000)
    tau = flight_age(7)
    s = by_clock(0, half, K)
    print(
        f"    total {total:8d}: split ({half}, {total - half}) after 3000 -> ({a}, {b});"
        f" {'FIXED' if a == b and abs(half - a) <= tau * (s + 1) else 'moved'}"
        f" (steady transit each way {tau} x s, s = M / K = {Fraction(half, K)})"
    )
print(
    "the map is linear in the contents (the cost per unit is the turn, M / K per self-creation;\n"
    "    the click joins what was paid), so the total is conserved and any two contents relax to\n"
    "    the equal split of their total: the set of fixed points is one per total, a continuum\n"
    "    of every integer within the bounds of B. Nothing selects a content."
)

# --------------------------------------------------------------------------
section("D. Representability of nature's ratios on one integer grid (A10's test)")

# CODATA 2018 (relative standard uncertainties in parentheses as given) and PDG 2022 for the pions.
RATIOS = {
    "m_mu / m_e": (Fraction("206.7682830"), Fraction("0.0000046")),
    "m_p / m_e": (Fraction("1836.15267343"), Fraction("0.00000011")),
    "m_n / m_e": (Fraction("1838.68366173"), Fraction("0.00000089")),
    "m_tau / m_e": (Fraction("3477.23"), Fraction("0.23")),
}
M_E_MEV = Fraction("0.51099895000")
PION = {
    "m_pi+ / m_e": (Fraction("139.57039") / M_E_MEV, Fraction("0.00018") / M_E_MEV),
    "m_pi0 / m_e": (Fraction("134.9768") / M_E_MEV, Fraction("0.0005") / M_E_MEV),
}
for name, (value, error) in {**RATIOS, **PION}.items():
    print(f"    {name:12s} = {float(value):.7f} +- {float(error):.2e}")
print(
    "m_n / m_p =", float(RATIOS["m_n / m_e"][0] / RATIOS["m_p / m_e"][0]), "(CODATA: 1.00137841931(49))"
)


def fits(k: int, value: Fraction, error: Fraction) -> bool:
    """Exact: |k r - round(k r)| <= k u in rational arithmetic."""
    x = k * value
    nearest = round(x)
    return abs(x - nearest) <= k * error


def fits_float(k: int, value: float, error: float) -> bool:
    """The same test in floating point, to scan quickly; every k it reports
    is confirmed by `fits` (exact) before it is printed."""
    x = k * value
    return abs(x - round(x)) <= k * error


def smallest_k(names: list[str], limit: int) -> int | None:
    items = [({**RATIOS, **PION})[n] for n in names]
    floats = [(float(v), float(e)) for v, e in items]
    for k in range(1, limit + 1):
        if all(fits_float(k, v, e) for v, e in floats) and all(fits(k, v, e) for v, e in items):
            return k
    return None


for names in (
    ["m_mu / m_e", "m_p / m_e"],
    ["m_mu / m_e", "m_p / m_e", "m_n / m_e"],
    ["m_mu / m_e", "m_p / m_e", "m_n / m_e", "m_tau / m_e"],
    ["m_mu / m_e", "m_p / m_e", "m_pi+ / m_e", "m_pi0 / m_e"],
):
    k = smallest_k(names, 3_000_000)
    rungs = {n: (round(k * ({**RATIOS, **PION})[n][0]) if k else None) for n in names}
    print(f"    smallest k (the electron's rung) fitting {names}: {k}; the rungs {rungs}")
mu, pr = (float(v) for v in RATIOS["m_mu / m_e"]), (float(v) for v in RATIOS["m_p / m_e"])
mu_v, mu_e = mu
pr_v, pr_e = pr
count = sum(1 for k in range(1, 3_000_001) if fits_float(k, mu_v, mu_e) and fits_float(k, pr_v, pr_e))
print(f"    number of k below 3 000 000 fitting the muon and the proton: {count}")
print(
    "what this says: a grid fine enough (k of a few thousand) carries the measured ratios, as a\n"
    "    fine grid carries any number; the test has no power unless a rule fixes k, and the law\n"
    "    has none (section C). A10 was written for the superseded loop law and stays planned."
)

# --------------------------------------------------------------------------
section("E. The harmonic ladder a self-referential window would give (NOT the law) against nature")

# The rule (DESIGN.md, the smallest rule): a reader's window centred on its
# own clock phase. A body of content M whose light returns after tau
# intervals re-absorbs it iff (2 l p_l - turn over tau) mod N is inside the
# window, and its turn over tau is tau M / K to the floor: contents in bands
# of width w K / tau spaced K N / tau, a ladder equally spaced in M.
for K, N, tau in ((2**20, 64, 24), (2**20, 64, 240), (2**30, 64, 24)):
    print(
        f"    K = {K}, N = {N}, round trip tau = {tau}: rung spacing K N / tau = {Fraction(K * N, tau)}"
    )
# Whatever the spacing, an equally spaced ladder with an offset puts nature's
# masses at m = a (j + c): three masses fix (m_p - m_e) / (m_mu - m_e) as a
# ratio of two rung differences, an integer ratio p / q within the measured
# uncertainty. The smallest q is the number of rungs from the electron to the
# muon, and every rung between is a lepton nature does not show.
value_r = (RATIOS["m_p / m_e"][0] - 1) / (RATIOS["m_mu / m_e"][0] - 1)
error_r = value_r * (
    RATIOS["m_mu / m_e"][1] / (RATIOS["m_mu / m_e"][0] - 1)
    + RATIOS["m_p / m_e"][1] / (RATIOS["m_p / m_e"][0] - 1)
)
print(f"    R = (m_p - m_e) / (m_mu - m_e) = {float(value_r):.9f} +- {float(error_r):.1e}")
best = None
for q in range(1, 200_001):
    p = round(q * value_r)
    if abs(Fraction(p, q) - value_r) <= error_r:
        best = (p, q)
        break
print(
    f"    smallest p / q within the uncertainty: {best}; rungs from the electron to the muon: {best[1] if best else None}"
)
print(
    "    leptons nature shows between the electron and the muon: 0 (the next charged lepton is the tau, at 3477)"
)
print(
    "verdict of E: the only ladder a clock resonance can give is harmonic (equally spaced in the\n"
    "    content), and a harmonic ladder that carries the electron, the muon and the proton has\n"
    f"    {best[1] - 1 if best else '?'} unseen rungs between the electron and the muon; refuted by the spectrum."
)

# --------------------------------------------------------------------------
section("F. What the law says about composites (no mass defect) against nature")

m_p, m_n = RATIOS["m_p / m_e"][0], RATIOS["m_n / m_e"][0]
NATURE = {
    "deuteron": (Fraction("3670.48296788"), m_p + m_n),
    "alpha": (Fraction("7294.29954142"), 2 * m_p + 2 * m_n),
}
for name, (nature, law) in NATURE.items():
    print(
        f"    {name}: the law's content m_p + ... = {float(law):.5f} m_e exactly (a free ray carries no content);"
        f" nature {float(nature):.5f} m_e; the law is above by {float(law - nature):.3f} m_e = {float((law - nature) * M_E_MEV):.3f} MeV"
        f" ({float((law - nature) / nature) * 100:.3f} %)"
    )
print(
    "    the register's integers 1836 and 1839 (series I, H): m_n / m_p = 1839 / 1836 ="
    f" {float(Fraction(1839, 1836)):.7f} against nature's 1.0013784: an input, and rounded"
)
print(
    "    the muon (207), the tau (3477), the pions: catalog values; the law has no rung for any of them."
)
