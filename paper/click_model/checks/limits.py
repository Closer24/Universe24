"""The continuum limits of the click model: what returns as the resolution
grows (the owner's direction of 2026-09-20: "take the computation on our
Nodes to infinity and you should get the known formulas, as Fourier gives
pi"). Three computations from the design's formulas, not engine runs:

1. The Bell value S(N, Q) at the CHSH labels with the phase resolution N
   and the tables' scale Q (the engine's Q is 256): the bound of
   Theorem 4, |E - cos| <= 2/N + 4 arcsin(sqrt 2 / (2 Q)), goes to zero
   as both grow, so S -> 2 sqrt 2, Tsirelson's value, as a limit.
2. Young's fringes under the flight table's rounding: the exact cosine
   pattern against the pattern whose per-path phase is read at whole
   intervals, for wavelengths of 8 (the registered two-slit world), 32,
   64 and 256 intervals: the residual of the limit shrinks with lambda.
3. The plane wave: the pair form turns n / d steps per interval and the
   flight moves 1 / sqrt 3 Links per interval, so the phase along the
   line is k x - omega t with omega = c k exactly (no dispersion) up to
   the floor of the count; the floor's error per interval is 1 / d steps.

    python paper/click_model/checks/limits.py
"""

from __future__ import annotations

import math
from fractions import Fraction
from functools import cache

TSIRELSON = 2 * math.sqrt(2)


@cache
def tables(n: int, scale: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """The half-angle tables of 2N at the scale Q: C[p] = round(Q cos(2 pi p / 2N)),
    S[p] = C[p - N/2] (the quarter turn exact on the tables)."""
    c = tuple(round(scale * math.cos(2 * math.pi * p / (2 * n))) for p in range(2 * n))
    s = tuple(c[(p - n // 2) % (2 * n)] for p in range(2 * n))
    return c, s


def cells(n: int, scale: int, a: int, b: int) -> tuple[dict[tuple[int, int], int], Fraction]:
    c, s = tables(n, scale)
    ua = ((c[a], s[a]), (-s[a], c[a]))
    ub = ((c[b], s[b]), (-s[b], c[b]))
    w = {}
    for oa in (0, 1):
        for ob in (0, 1):
            j = ua[oa][0] * ub[ob][0] + ua[oa][1] * ub[ob][1]
            w[(oa, ob)] = j * j
    total = sum(w.values())

    def rung(cumulative: int) -> int:
        return (2 * n * cumulative + total) // (2 * total)

    coarse = rung(w[(0, 0)] + w[(0, 1)])
    fine_plus = rung(w[(0, 0)])
    fine_minus = rung(w[(0, 0)] + w[(0, 1)] + w[(1, 0)])
    found = {
        (0, 0): fine_plus,
        (0, 1): coarse - fine_plus,
        (1, 0): fine_minus - coarse,
        (1, 1): n - fine_minus,
    }
    e = Fraction(found[(0, 0)] + found[(1, 1)] - found[(0, 1)] - found[(1, 0)], n)
    return found, e


def chsh(n: int, scale: int) -> Fraction:
    q = n // 8
    settings = ((0, q), (0, 3 * q), (2 * q, q), (2 * q, 3 * q))
    signs = (1, -1, 1, 1)
    return sum(
        (sign * cells(n, scale, a, b)[1] for (a, b), sign in zip(settings, signs, strict=True)),
        Fraction(0),
    )


def tsirelson_limit() -> None:
    print(
        "== 1. S(N, Q) at the CHSH labels: the resolution N and the tables' scale Q; the engine's Q = 256"
    )
    print("   N      Q          S(N, Q)      S - 2 sqrt 2    the bound 8/N + 16 arcsin(sqrt 2 / 2Q)")
    for n in (64, 256, 1024, 4096):
        for scale in (256, 4096, 65536, 1 << 20):
            s = chsh(n, scale)
            bound = 8 / n + 16 * math.asin(math.sqrt(2) / (2 * scale))
            print(f"  {n:5d}  {scale:8d}  {float(s):.7f}  {float(s) - TSIRELSON:+.7f}   {bound:.5f}")
    print(
        "  the bound goes to zero as N and Q grow: S(N, Q) -> 2 sqrt 2, the Tsirelson value, as a limit;"
    )
    print(
        "  at Q = 256 the tables' term stays whatever N does: 16 arcsin(sqrt 2 / 512) = 0.0442 at the nominal"
        " length 256, 0.0443 at the least table length sqrt 65185 = 255.3 (the proof's value)"
    )


def pearson(a: list[float], b: list[float]) -> float:
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b, strict=True))
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    return cov / math.sqrt(va * vb)


def young_limit() -> None:
    """Two slits at y = +-s/2 on the wall, a screen at distance D (Links),
    every pixel reached from each slit along the straight line; the phase
    of a path is 2 pi t / lambda with t its flight time in intervals
    (Euclidean length x sqrt 3), exact or floored to whole intervals."""
    print("\n== 2. Young's fringes under the rounding of the flight to whole intervals")
    s, distance, pixels = 10, 44, 121
    print("   lambda (intervals)   Pearson(rounded, exact)   visibility exact   visibility rounded")
    for wavelength in (8, 32, 64, 256):
        exact, rounded = [], []
        for y in range(pixels):
            paths = [math.hypot(distance, y - 60 - sign * s / 2) * math.sqrt(3) for sign in (1, -1)]
            exact.append(abs(sum(math.e ** (2j * math.pi * t / wavelength) for t in paths)) ** 2)
            rounded.append(
                abs(sum(math.e ** (2j * math.pi * math.floor(t) / wavelength) for t in paths)) ** 2
            )
        visibility = lambda p: (max(p) - min(p)) / (max(p) + min(p))  # noqa: E731
        print(
            f"  {wavelength:8d}              {pearson(rounded, exact):.3f}                  "
            f"{visibility(exact):.3f}              {visibility(rounded):.3f}"
        )
    print(
        "  the registered two-slit world has lambda = 8 intervals: the rounding is an eighth of a wavelength per path;"
    )
    print(
        "  the limit lambda -> infinity (a -> 0 at fixed light) returns Young's pattern; the register's 0.368 is the finite-lambda residual"
    )


def fan_limit() -> None:
    """Two openings each re-emitting along K equally spaced directions
    (the registered world: 91); a pixel of the screen receives a row from
    an opening only where one of its rays lands (nearest pixel). The
    per-pixel W = |sum e^{i phi}|^2 over the rows that reach it (the phase
    from the exact flight time at lambda = 8 intervals): with few
    directions most pixels see one opening or none and the pattern is
    the incoherent sum; as K grows every pixel sees both and Young's
    pattern returns."""
    print(
        "\n== 2b. Young's fringes under the fan's discreteness: K directions per opening (the register's 91)"
    )
    s, distance, pixels, wavelength = 10, 44, 121, 8.0
    openings = (60 - s / 2, 60 + s / 2)
    print(
        "        K   pixels reached   pixels with both openings   Pearson(W, cosine)   Pearson(W, incoherent)"
    )
    for k in (91, 181, 361, 721, 1441, 5761):
        rows: dict[int, list[complex]] = {}
        seen: dict[int, set[int]] = {}
        for index, y0 in enumerate(openings):
            for j in range(k):
                angle = -math.pi / 2 + math.pi * (j + 0.5) / k  # the half-plane toward the screen
                y = y0 + distance * math.tan(angle)
                pixel = round(y)
                if not 0 <= pixel < pixels:
                    continue
                t = math.hypot(distance, pixel - y0) * math.sqrt(3)
                rows.setdefault(pixel, []).append(math.e ** (2j * math.pi * t / wavelength))
                seen.setdefault(pixel, set()).add(index)
        w = [abs(sum(rows.get(y, []))) ** 2 for y in range(pixels)]
        incoherent = [float(len(rows.get(y, []))) for y in range(pixels)]
        cosine = [
            1
            + math.cos(
                2
                * math.pi
                * (math.hypot(distance, y - openings[0]) - math.hypot(distance, y - openings[1]))
                * math.sqrt(3)
                / wavelength
            )
            for y in range(pixels)
        ]
        both = sum(1 for y in seen.values() if len(y) == 2)
        print(
            f"  {k:7d}   {len(rows):6d}           {both:6d}                     "
            f"{pearson(w, cosine):.3f}                {pearson(w, incoherent):.3f}"
        )
    print(
        "  the register's reading: 75 pixels with rows, 27 with both openings, Pearson 0.368 with the cosine, 0.744 with the incoherent sum;"
    )
    print(
        "  the limit K -> infinity (Huygens' every direction) returns Young; the discreteness of the fan, not the rounding, is the residual"
    )


def plane_wave() -> None:
    print(
        "\n== 3. The plane wave: the pair form n / d steps per interval at the flight's 1 / sqrt 3 Links per interval"
    )
    for n_steps, n, d in ((64, 8, 1), (64, 1, 4), (4096, 1, 1)):
        omega = 2 * math.pi * n / (d * n_steps)  # radians per interval
        k = omega * math.sqrt(3)  # radians per Link along the line (c = 1 / sqrt 3)
        print(
            f"  N = {n_steps}, rate {n}/{d}: omega = {omega:.5f} rad/interval, k = {k:.5f} rad/Link, omega / k = {omega / k:.5f} = c;"
            f" the floor's error per interval < 1/{d} step = {2 * math.pi / (d * n_steps):.5f} rad"
        )
    print(
        "  dispersionless: omega = c k for every rate; the limit N, d -> infinity is the massless wave equation's plane wave"
    )


if __name__ == "__main__":
    tsirelson_limit()
    young_limit()
    fan_limit()
    plane_wave()
