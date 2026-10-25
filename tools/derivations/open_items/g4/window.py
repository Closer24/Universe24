"""Hand g4, brief m, part (a) and (d): the window of g for the heavy lift, derived from the gapped line's
dispersion at the vacuum's paces (ALGEBRA.md, The line; The clock once and the Link twice; The paces compose;
What a body is, the Compton length; The two branches; The velocity; The four lines of the body (d) The fall; The
well, the one-Node threshold). Every algebraic number is an exact fraction printed as an integer quotient with
its remainder at the scale named; the transcendental ones (omega_0, pi) are floats marked CHECK, each beside an
integer reading: the period of the one-Node rotation counted on the exact integer recurrence
a_next = (2 num' a_now) div den' - a_before (the beat), and the beat's redshift factor as the quotient of two
such counts at two contents against the clock's own integer slowing.

    python tools/derivations/g4/window.py            (the table and the window's edges)
"""

from __future__ import annotations

from fractions import Fraction
from math import acos, isqrt, pi, sin, sqrt

GAMMA = 1000
WATSON_MICRO = 1516386  # Watson's integral for the simple cubic lattice, W_3 = 1.516386 x 10^-6 scaled: the one-Node well binds where its depth passes the band's half-width over W_3 (W2's threshold; ALGEBRA.md, The well: one Node at y = 0.25 is bound, the Node's threshold)
SPAN = 100  # intervals of the fall's and the width's predicate
SIGMAS = (Fraction(1), Fraction(3, 2), Fraction(2))  # the laid packet's rms half-width in Links (the width 2 sigma: 2, 3, 4 Links)
GRADIENTS = (10, 30, 100)  # the well's gradient in content levels per Link (U per Link = G / Gamma)
FRACTIONS = (Fraction(1, 100), Fraction(5, 100), Fraction(1, 10), Fraction(2, 10), Fraction(1, 4))  # the named fractions of the clock's 1


def quot(x: Fraction, scale: int = 1000) -> str:
    """An exact fraction as the integer quotient of scale x with its remainder over the denominator."""
    n = x.numerator * scale
    q, r = divmod(n, x.denominator)
    return f"{q} rem {r}/{x.denominator}" if r else f"{q}"


def clock(gamma: int, c: int) -> int:
    """p_0(c) = Gamma (1 - 1 / Gamma)^c rounded half up (core/paces.clock_alone's fraction)."""
    if c == 0:
        return gamma
    num, den = gamma * (gamma - 1) ** c, gamma**c
    return (2 * num + den) // (2 * den)


def period_count(num: int, den: int, c: int, gamma: int, intervals: int = 20000, amplitude: int = 10**12) -> tuple[int, int]:
    """The one-Node rotation counted on the exact integer recurrence at the content c: 2 cos omega = 2 (den Gamma^2 - (den - num) p_0^2) / (den Gamma^2), a_next = (2 K a_now) div W - a_before with K = den Gamma^2 - (den - num) p_0^2 and W = den Gamma^2 (the rotation act of features/click `rotated`); returns (upward zero crossings, intervals): the beat is crossings per interval, an integer reading of omega / 2 pi."""
    p0 = clock(gamma, c)
    k = den * gamma * gamma - (den - num) * p0 * p0
    w = den * gamma * gamma
    before, now = 0, amplitude  # the lay (A, 0): the before level 0, the now level A
    crossings = 0
    for _ in range(intervals):
        nxt = (2 * k * now) // w - before
        if now < 0 <= nxt:
            crossings += 1
        before, now = now, nxt
    return crossings, intervals


def table_row(g: Fraction, label: str) -> dict:
    """Every derived quantity at one g (exact fractions, and the floats marked CHECK)."""
    cos0 = 1 - g
    sin2 = g * (2 - g)  # sin^2 omega_0 = 1 - (1 - g)^2
    t = (1 - g) / 3  # the hopping num / (3 den)
    delta2 = t * t / sin2  # Delta^2, Delta = (num / (3 den)) / sin omega_0 the band's curvature at k = 0 (Links^2 per interval)
    fall_coefficient = Fraction(2, 3) * (1 - g) / (2 - g)  # a / (dU / dx) = 2 g t / sin^2 omega_0 = (2 / 3)(1 - g) / (2 - g), light's 1 / 3 at g -> 0
    threshold_u = (1 - g) * 10**6 / (WATSON_MICRO * (4 - 2 * g))  # U_c = Delta_c / (8 - 4 g), Delta_c = 2 (1 - g) / W_3 in 2 cos omega (W2 (e); The well)
    doubling2 = {s: 12 * s**4 / delta2 for s in SIGMAS}  # T_d^2 = 12 sigma_0^4 / Delta^2: sigma(T_d) = 2 sigma_0 for a free Gaussian packet, sigma(t)^2 = sigma_0^2 + Delta^2 t^2 / (4 sigma_0^2)
    width2_at_span = {s: s * s + delta2 * SPAN * SPAN / (4 * s * s) for s in SIGMAS}  # sigma(SPAN)^2
    falls = {G: Fraction(SPAN * SPAN, 2) * fall_coefficient * Fraction(G, GAMMA) for G in GRADIENTS}  # s = a T^2 / 2 in Links at the gradient G levels per Link
    omega0 = acos(float(cos0))  # CHECK (transcendental)
    row = {
        "label": label,
        "g": g,
        "cos0": cos0,
        "sin2": sin2,
        "sin0_milli": isqrt(sin2.numerator * 10**6 // sin2.denominator),
        "t": t,
        "delta2": delta2,
        "delta_micro": isqrt(delta2.numerator * 10**12 // delta2.denominator),
        "fall_coefficient": fall_coefficient,
        "threshold_u": threshold_u,
        "threshold_levels": threshold_u * GAMMA,
        "doubling": {s: isqrt(doubling2[s].numerator // doubling2[s].denominator) for s in SIGMAS},
        "width_at_span_milli": {s: isqrt(width2_at_span[s].numerator * 10**6 // width2_at_span[s].denominator) for s in SIGMAS},
        "falls_milli": falls,
        "omega0_check": omega0,
        "compton_check": 1 / (sqrt(3) * omega0),
        "factor_check": 2 * float(g) / (omega0 * sin(omega0)),
    }
    return row


def window_edges() -> dict[str, Fraction | float]:
    """The window's edges in g, each solved exactly where the condition is algebraic: the doubling time T_d(sigma_0) = SPAN gives q g (2 - g) = (1 - g)^2 with q = 108 sigma_0^4 / SPAN^2, so g = 1 - sqrt(q / (1 + q)); the fall of one Link within SPAN intervals at the gradient G gives (1 - g) / (2 - g) >= 3 Gamma / (SPAN^2 G); the beat's factor within the fraction f is solved by bisection on the float check."""
    found: dict[str, Fraction | float] = {}
    for s in SIGMAS:
        q = 108 * s**4 / SPAN**2
        found[f"g_low_localised_sigma_{s}"] = 1 - sqrt(float(q / (1 + q)))
    for G in GRADIENTS:
        ratio = Fraction(3 * GAMMA, SPAN * SPAN * G)  # (1 - g) / (2 - g) >= ratio  <=>  g <= (1 - 2 ratio) / (1 - ratio)
        found[f"g_high_fall_one_link_G_{G}"] = (1 - 2 * ratio) / (1 - ratio)
    for f in FRACTIONS:
        lo, hi = 1e-6, 0.999
        for _ in range(60):
            mid = (lo + hi) / 2
            w0 = acos(1 - mid)
            if 2 * mid / (w0 * sin(w0)) <= 1 + float(f):
                lo = mid
            else:
                hi = mid
        found[f"g_high_beat_within_{f}"] = lo
    return found


def beat_factor_integer(num: int, den: int, c: int, gamma: int = GAMMA) -> tuple[int, int, int, int, str]:
    """The beat's redshift factor as an integer reading: the one-Node rotation's crossings n_0 at the vacuum and n_c at the content c over the same span, the clock p_0(c); the beat's fractional slowing over the clock's, 1000 (n_0 - n_c) p_0 div (n_c (Gamma - p_0)), the proper clock's own value being 1000."""
    n0, span = period_count(num, den, 0, gamma)
    nc, _ = period_count(num, den, c, gamma)
    p0 = clock(gamma, c)
    q, r = divmod(1000 * (n0 - nc) * p0, nc * (gamma - p0))
    return n0, nc, p0, span, f"{q} rem {r}"


def main() -> None:
    print(f"# the window of g (hand g4), Gamma {GAMMA}, span {SPAN} intervals, Watson W_3 = {WATSON_MICRO} x 10^-6")
    print("# columns: g | sin omega_0 (milli) | t = (1-g)/3 | Delta (micro Links^2/interval) | a/(dU/dx) (milli) | U_c (milli) c_c (levels) | T_double at sigma_0 1, 1.5, 2 (intervals) | sigma at 100 intervals from sigma_0 1, 1.5, 2 (milli Links) | fall in 100 intervals at G = 10, 30, 100 levels/Link (milli Links) | omega_0 CHECK | Compton 1/(sqrt3 omega_0) CHECK | beat factor 2g/(omega sin omega) CHECK")
    gs = [Fraction(n, 1000) for n in (10, 20, 41, 100, 150, 200, 300, 400, 500, 600, 616, 700, 772, 800, 830, 840, 880, 897, 920, 950, 970, 990)]
    for g in gs:
        r = table_row(g, f"g={g}")
        print(
            f"g {quot(g)} | sin {r['sin0_milli']} | t {quot(r['t'])} | Delta {r['delta_micro']} | a/G {quot(r['fall_coefficient'])} | U_c {quot(r['threshold_u'])} c_c {quot(r['threshold_levels'], 1)} | T_d "
            + " ".join(str(r["doubling"][s]) for s in SIGMAS)
            + " | sigma100 "
            + " ".join(str(r["width_at_span_milli"][s]) for s in SIGMAS)
            + " | fall "
            + " ".join(quot(r["falls_milli"][G]) for G in GRADIENTS)
            + f" | omega0 {r['omega0_check']:.4f} | Compton {r['compton_check']:.3f} | F {r['factor_check']:.4f}"
        )
    print("# the window's edges (g):")
    for key, value in window_edges().items():
        print(f"  {key}: {value if isinstance(value, Fraction) else round(value, 4)}" + (f" = {quot(value)} milli" if isinstance(value, Fraction) else ""))
    print("# the beat's factor as an integer reading on the exact recurrence (20,000 intervals, amplitude 10^12): lifts (num, den) at contents c")
    for label, num, den in (
        ("617 lift (19,16): g 512/617", 617 - 512, 617),
        ("196613 lift (338,287)", 196613 - 2 * 287 * 287, 196613),
        ("1013 lift (23,22)", 1013 - 2 * 22 * 22, 1013),
        ("421 lift (15,14)", 421 - 2 * 14 * 14, 421),
        ("181 lift (10,9)", 181 - 2 * 81, 181),
        ("89 lift (8,5)", 89 - 50, 89),
        ("13 lift (3,2)", 13 - 8, 13),
        ("5 lift (2,1)", 5 - 2, 5),
        ("1297 lift (36,1)", 1297 - 2, 1297),
        ("37 lift (6,1)", 37 - 2, 37),
    ):
        for c in (50, 300):
            n0, nc, p0, span, factor = beat_factor_integer(num, den, c)
            g = Fraction(den - num, den)
            w0 = acos(float(1 - g))
            print(f"  {label}: g {quot(g)} milli; c {c}: crossings n_0 {n0} n_c {nc} over {span}, p_0(c) {p0}; factor x1000 = {factor} (CHECK 2g/(omega sin omega) at U=0: {1000 * 2 * float(g) / (w0 * sin(w0)):.0f}; the clock's 1000)")


if __name__ == "__main__":
    main()
