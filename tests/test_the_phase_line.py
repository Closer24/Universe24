"""The phase line as a standalone module (features/phase; ALGEBRA.md #the-four-acts (b), #the-direction; the two hands' item (i)): a Rule3 pair at the one fixed angle theta_0 = 1 / Gamma (K_0 = 2 Gamma^2 - 1 over D = 2 Gamma^2), seeded on the half wall at an amplitude a multiple of Gamma, iterated by a level with the angle signed, read as the hop's two integers and folded into the Link's one coefficient rounding; and the family's rest rotation to the unit found by a bisection on the act and no root. The bound used throughout (item (i), both hands): the pair's magnitude within Gamma / 2 levels of X standing plus the walk's proved 1.42 N + 2.3 Gamma levels over the test's N acts (`bound`), never a count. Every test under 30 seconds; each prints its numbers with its time."""

import math
import time

import numpy as np

from event_universe.core.paces import rounded
from event_universe.features.phase import K0, D, act, half_wall, seed
from tests.laws import refused


def read(pair):
    return pair[0][0], pair[1][0]


def iterate(pair, count, gamma, direction=1):
    direction, count = (direction, count) if count >= 0 else (-direction, -count)
    for _ in range(count):
        pair = tuple(act(line, gamma, direction) for line in pair)
    return pair


GAMMA = 6_000
WALL, COEFFICIENT = D(GAMMA), K0(GAMMA)
THETA = math.acos(COEFFICIENT / WALL)  # the angle per act, the integer pair's own
X35 = (2**35 // GAMMA) * GAMMA  # 2^35's size, the largest multiple of Gamma below it: 34,359,738,000
X175 = 175 * GAMMA
LINK_UNIT = 2_048_000  # the fold's unit X_ij of the hands' chains


def bound(acts: int) -> float:
    """The hands' bound in levels after `acts` acts: Gamma / 2 standing (the mean remainder, a telescoping sum) plus the walk's proved 1.42 N + 2.3 Gamma (item (i), the mathematician's 2)."""
    return GAMMA / 2 + 1.42 * acts + 2.3 * GAMMA


def magnitude_off(pair, amplitude) -> float:  # type: ignore[no-untyped-def]
    """|c + i s| - X in levels at the pair's now."""
    c, s = read(pair)
    return math.hypot(int(c), int(s)) - amplitude


def test_the_seed_stands_on_the_circle_at_the_half_wall_and_refuses_an_amplitude_off_gamma():
    """The fixed angle: D = 2 Gamma^2 = 72,000,000, K_0 = 71,999,999, 2 K_0 / D = 2 - 1 / Gamma^2 exactly, theta_0 within 2.6 x 10^-9 of 1 / Gamma relative. The seed at X of 2^35's size and at X = 175 Gamma: the cosine line (X, X cos theta_0 rounded half up, D div 2), the sine line (0, -(X div Gamma), D div 2), the sine seed within a level of X sin theta_0 (the advisor's second, item 4); c^2 + s^2 within the bound of X^2 at the now and at the before, and after ten acts; 2^35 itself and 2^35 + 1 refused by name (neither a multiple of Gamma = 2^4 3 5^3)."""
    started = time.perf_counter()
    assert (WALL, COEFFICIENT) == (72_000_000, 71_999_999)
    assert 2 * COEFFICIENT / WALL == 2 - 1 / GAMMA**2
    assert abs(THETA * GAMMA - 1) < 2.7e-9 and half_wall(GAMMA) == GAMMA**2 == WALL // 2
    for amplitude in (X35, X175):
        cosine, sine = pair = seed(amplitude, GAMMA)
        assert cosine == (amplitude, rounded(amplitude * COEFFICIENT, WALL), WALL // 2)
        assert sine == (0, -(amplitude // GAMMA), WALL // 2)
        assert abs(cosine[1] - amplitude * math.cos(THETA)) <= 0.5
        assert abs(-sine[1] - amplitude * math.sin(THETA)) <= 1
        assert abs(magnitude_off(pair, amplitude)) <= bound(0)
        before = math.hypot(cosine[1], sine[1]) - amplitude
        assert abs(before) <= bound(0)
        turned = iterate(pair, 10, GAMMA)
        assert abs(magnitude_off(turned, amplitude)) <= bound(10)
        print(
            f"seed X = {amplitude}: now off {magnitude_off(pair, amplitude):.3f} levels, before off {before:.3f}, after 10 acts {magnitude_off(turned, amplitude):.3f} (bound {bound(10):.0f})"
        )
    refused("not a multiple of Gamma", seed, 2**35, GAMMA)
    refused("not a multiple of Gamma", seed, 2**35 + 1, GAMMA)
    refused("not a multiple", seed, np.array([X35, X35 + 1], dtype=np.int64), GAMMA)
    print(f"theta_0 Gamma - 1 = {THETA * GAMMA - 1:.3e}; {time.perf_counter() - started:.2f} s")


def test_the_reversal_is_bit_exact_over_ten_thousand_acts():
    """10^4 acts forward then 10^4 inverse acts (direction -1): both lines, levels and remainders, bit for bit the seed; the same through `iterate` at direction -1 and through the signed count."""
    started = time.perf_counter()
    pair = seed(X35, GAMMA)
    cosine, sine = pair
    acts = 10**4
    for _ in range(acts):
        cosine, sine = act(cosine, GAMMA), act(sine, GAMMA)
    forward = (cosine, sine)
    assert forward != pair
    for _ in range(acts):
        cosine, sine = act(cosine, GAMMA, -1), act(sine, GAMMA, -1)
    assert (cosine, sine) == pair
    assert iterate(forward, acts, GAMMA, -1) == pair and iterate(forward, -acts, GAMMA) == pair
    assert iterate(pair, acts, GAMMA) == forward
    refused("direction is 1 or -1", act, pair[0], GAMMA, 0)
    print(
        f"10^4 acts forward and back: bit for bit, remainders {forward[0][2]}, {forward[1][2]} on the way; {time.perf_counter() - started:.2f} s"
    )
