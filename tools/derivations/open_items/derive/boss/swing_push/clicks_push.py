"""Do the clicks push the contraction away? The great clock's swing with a source the clicks raise, in exact fractions.

usage: python3 -I clicks_push.py

A toy of the logic, not the act. The time gear's load x swings on its spring, x'' = -w2 x + j, the leapfrog
x(n+1) = 2 x(n) - x(n-1) - w2 x(n) + j(n), with w2 = 2 / Gamma (the time gear's D / W, stage 7b), Gamma = 1000, so
the swing's period is 2 pi sqrt(Gamma / 2) = 140.5 ticks. The bang is the kick: x(0) = 0, x(1) = v0. The source
is rho + 3p: matter pushes once with its share m and light twice with its share l, j = m + 2 l (the picture, 4).
A click that turns matter into light (a giver's emission) moves a share from m to l. The top is the first tick
where the load stops rising: the contraction starts there. Every rate below is the toy's, typed, and the forms
are the toy's; what the act gives is stage 9's count.
"""

from fractions import Fraction
from math import atan, pi, sqrt

GAMMA = 1000
W2 = Fraction(2, GAMMA)
V0 = Fraction(1)
OMEGA = sqrt(2 / GAMMA)
LIMIT = 400


def swing(source) -> tuple[int, Fraction]:
    """Run from the bang to the top; source(n, x) gives j(n). Returns the top's tick and its height."""
    before, now = Fraction(0), V0
    for n in range(1, LIMIT):
        after = 2 * now - before - W2 * now + source(n, now)
        if after <= now:
            return n, now
        before, now = now, after
    return LIMIT, now  # no top within the run


def steady(push: Fraction):
    return lambda n, x: push


def converting(matter: Fraction, rate: Fraction):
    """Matter at share m turned into light at `rate` per tick by the clicks: j = m + 2 l, m + l kept."""
    state = {"m": matter, "l": Fraction(0)}

    def j(n, x):
        moved = rate * state["m"]
        state["m"] -= moved
        state["l"] += moved
        return state["m"] + 2 * state["l"]

    return j


def fading(light: Fraction, rate: Fraction):
    """Light alone, reddening and thinning at `rate` per tick, no clicks renewing it: j = 2 l."""
    state = {"l": light}

    def j(n, x):
        state["l"] -= rate * state["l"]
        return 2 * state["l"]

    return j


def main() -> None:
    unit = V0 * Fraction(OMEGA).limit_denominator(
        10**9
    )  # the push that equals the kick's v0 w, as a fraction
    lines = [
        "Do the clicks push the contraction away? The time gear's swing, exact fractions (the Boss, 2026-10-29)",
        "",
    ]
    lines.append(
        f"Gamma = {GAMMA}: the swing's period {2 * pi / OMEGA:.1f} ticks, a quarter of it {pi / (2 * OMEGA):.1f}"
    )
    top, height = swing(steady(Fraction(0)))
    lines.append(
        f"1. no source after the bang (the control): the top at tick {top}, height {float(height):.2f}"
    )
    lines.append(
        "2. a steady push j0 = kappa v0 w (the formula for a smooth swing: w t_top = pi - atan(1 / kappa)):"
    )
    for kappa in (Fraction(1, 2), Fraction(1), Fraction(3), Fraction(10)):
        top, height = swing(steady(kappa * unit))
        formula = (pi - atan(1 / float(kappa))) / OMEGA
        lines.append(
            f"   kappa {str(kappa):>4}: the top at tick {top} (smooth {formula:.1f}), height {float(height):.2f}"
        )
    lines.append(
        "3. matter at kappa = 1, the clicks turning it into light at a rate per tick (light pushes twice):"
    )
    for rate in (Fraction(0), Fraction(1, 100), Fraction(1, 30), Fraction(1, 10)):
        top, height = swing(converting(unit, rate))
        lines.append(f"   rate {str(rate):>5}: the top at tick {top}, height {float(height):.2f}")
    lines.append(
        "4. light alone at kappa = 1, fading with no clicks to renew it (the redshift's thinning):"
    )
    for rate in (Fraction(0), Fraction(1, 100), Fraction(1, 30), Fraction(1, 10)):
        top, height = swing(fading(unit / 2, rate))
        lines.append(f"   fade {str(rate):>5}: the top at tick {top}, height {float(height):.2f}")
    lines.append(
        "5. a source that grows with the load as fast as the spring pulls (j = w2 x), the door of section 12:"
    )
    top, height = swing(lambda n, x: W2 * x)
    lines.append(
        f"   the top at tick {top} of {LIMIT} ({'none within the run' if top == LIMIT else 'reached'}), height {float(height):.2f}"
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
