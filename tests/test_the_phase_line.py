"""The phase line as a standalone module (features/phase; ALGEBRA.md #the-four-acts (b), #the-direction; the two hands' item (i)): a Rule3 pair at the one fixed angle theta_0 = 1 / Gamma (K_0 = 2 Gamma^2 - 1 over D = 2 Gamma^2), seeded on the half wall at an amplitude a multiple of Gamma, iterated by a level with the angle signed, read as the hop's two integers and folded into the Link's one coefficient rounding. Integers throughout, the owner's word (no float anywhere in the system, the tests inside it): a magnitude within B levels of X is the inequality (X - B)^2 <= c^2 + s^2 <= (X + B)^2; the cosine is the exact rational K_0 / D by cross multiplication; the sine is the module's own integer sine (`core/paces.sine_den`, the largest integer whose square is at most the product, no root); the angle is bracketed by the cosine's Taylor bounds as one integer inequality. The bound used throughout (item (i), both hands): the pair's magnitude within Gamma / 2 levels of X standing plus the walk's proved 1.42 N + 2.3 Gamma levels over the test's N acts, taken at the integer ceiling (`bound`), never a count. Every test under 15 seconds; each prints its numbers (the clock's seconds, a float, taken out 2026-10-25 by the owner's rule)."""

import numpy as np
import pytest

from event_universe import rows
from event_universe.core.paces import rounded, sine_den
from event_universe.core.rule3 import largest_below
from event_universe.features.phase import (
    K0,
    D,
    act,
    carried,
    deviation,
    floor,
    half_wall,
    seed,
    unit,
)
from event_universe.loader.world import read_world
from event_universe.node import Node
from tests.laws import refused, world_of


def iterate(pair, count, gamma, direction=1):
    direction, count = (direction, count) if count >= 0 else (-direction, -count)
    for _ in range(count):
        pair = tuple(act(line, gamma, direction) for line in pair)
    return pair


GAMMA = 6_000
WALL, COEFFICIENT, X175 = D(GAMMA), K0(GAMMA), 175 * GAMMA
X35 = (2**35 // GAMMA) * GAMMA  # 2^35's size, the largest multiple of Gamma below it: 34,359,738,000
TENTH, ROOM = 10**10, 10**10 + 26  # the angle's relative unit, and (1 + 2.6 x 10^-9) 10^10


def bound(acts: int) -> int:
    """The hands' bound in levels after `acts` acts, at its integer ceiling: (Gamma + 1) div 2 standing (the mean remainder, a telescoping sum) plus the walk's proved 1.42 N + 2.3 Gamma (item (i), the mathematician's 2), (142 N + 230 Gamma + 99) div 100."""
    return (GAMMA + 1) // 2 + (142 * acts + 230 * GAMMA + 99) // 100


def within(pair, x: int, room: int, index: int = 0) -> bool:
    """The pair's (c, s) at the now (index 0) or at the before (index 1) within `room` levels of X in magnitude, as the integer inequality (X - room)^2 <= c^2 + s^2 <= (X + room)^2."""
    c, s = int(pair[0][index]), int(pair[1][index])
    return (x - room) ** 2 <= c * c + s * s <= (x + room) ** 2


def off(pair, x: int, index: int = 0) -> tuple[int, int]:
    """|c + i s| - X in levels as a quotient with its remainder: the largest integer whose square is at most c^2 + s^2 (`rule3.largest_below`, no root), less X, and the square's excess over that integer's square."""
    c, s = int(pair[0][index]), int(pair[1][index])
    floor = largest_below(c * c + s * s)
    return floor - x, c * c + s * s - floor * floor


def test_the_seed_stands_on_the_circle_at_the_half_wall_and_refuses_an_amplitude_off_gamma():
    """The fixed angle: D = 2 Gamma^2 = 72,000,000, K_0 = D - 1 = 71,999,999, 2 K_0 / D = 2 - 1 / Gamma^2 exactly by cross multiplication; theta_0 Gamma in [1, 1 + 2.6 x 10^-9]: cos x > 1 - x^2 / 2 at x = 1 / Gamma = cos theta_0, and cos x <= 1 - x^2 / 2 + x^4 / 24 at x = ROOM / (Gamma 10^10) is at most cos theta_0 by the integer inequality 12 Gamma^2 (ROOM^2 10^20 - 10^40) >= ROOM^4. The seed at X of 2^35's size and at X = 175 Gamma: the cosine line (X, X cos theta_0 rounded half up, D div 2), the before within half a level of X K_0 / D (2 |D before - X K_0| <= D), the sine line (0, -(X div Gamma), D div 2), the sine seed within a level of X sin theta_0 (the advisor's second, item 4) against the module's integer sine floor(X D sin theta_0); c^2 + s^2 within the bound of X^2 at the now and at the before, and after ten acts; 2^35 itself and 2^35 + 1 refused by name (neither a multiple of Gamma = 2^4 3 5^3)."""
    assert (WALL, COEFFICIENT) == (2 * GAMMA**2, WALL - 1) == (72_000_000, 71_999_999)
    assert 2 * COEFFICIENT * GAMMA**2 == (2 * GAMMA**2 - 1) * WALL  # 2 K_0 / D = 2 - 1 / Gamma^2
    margin = 12 * GAMMA**2 * (ROOM**2 * TENTH**2 - TENTH**4) - ROOM**4
    assert margin >= 0 and half_wall(GAMMA) == GAMMA**2 == WALL // 2
    for x in (X35, X175):
        cosine, sine = pair = seed(x, GAMMA)
        assert cosine == (x, rounded(x * COEFFICIENT, WALL), WALL // 2)
        assert sine == (0, -(x // GAMMA), WALL // 2)
        assert 2 * abs(WALL * int(cosine[1]) - x * COEFFICIENT) <= WALL
        scaled = -int(sine[1]) * WALL  # (X div Gamma) D against floor(X D sin theta_0)
        assert scaled - WALL <= sine_den(COEFFICIENT, WALL, x) < scaled + WALL
        assert within(pair, x, bound(0)) and within(pair, x, bound(0), 1)
        assert within(turned := iterate(pair, 10, GAMMA), x, bound(10))
        print(
            f"seed X = {x}: now off {off(pair, x)} levels (floor, the square's excess), before off {off(pair, x, 1)}, after 10 acts {off(turned, x)} (bound {bound(10)})"
        )
    refused("not a multiple of Gamma", seed, 2**35, GAMMA)
    refused("not a multiple of Gamma", seed, 2**35 + 1, GAMMA)
    refused("not a multiple", seed, np.array([X35, X35 + 1], dtype=np.int64), GAMMA)
    print(f"theta_0 Gamma - 1 <= {ROOM - TENTH} / 10^10, margin {margin}")


def test_the_reversal_is_bit_exact_over_ten_thousand_acts():
    """10^4 acts forward then 10^4 inverse acts (direction -1): both lines, levels and remainders, bit for bit the seed; the same through `iterate` at direction -1 and through the signed count."""
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
        f"10^4 acts forward and back: bit for bit, remainders {forward[0][2]}, {forward[1][2]} on the way"
    )


def test_the_amplitude_is_the_universes_and_the_engine_refuses_a_scale_below_the_floor_from_gamma():
    """The amplitude declared from outside (the owner's words of 2026-10-27, 04:0x and 04:4x UTC; THE-AMPLITUDE-SCALE.md): the universe file names it beside den, Gamma and T (288,230,376,000 in the shipped universes, a multiple of 2 Gamma), the loader refuses a file naming none, and the engine carries it above the floor derived from Gamma alone, 23 Gamma at Gamma 1,000 (the orbit's departure 23 levels against the step 22 at k = 22, 20 against 23 at k = 23), refusing a scale below it by name as the engine's, never as nature's; no width and no room stands in the engine."""
    universe, world = world_of("world_hole.json")
    gamma, scale = int(universe["integers"]["node_clock"]), int(universe["integers"]["amplitude"])
    least = floor(gamma)
    assert least == 23 * gamma and deviation(22 * gamma, gamma) >= 22 > deviation(least, gamma)
    assert scale == 288_230_376_000 and scale % unit(gamma) == 0 and least < scale
    assert carried(scale, gamma) == scale and Node(universe, world).X == scale
    refused("engine cannot carry", carried, least - gamma, gamma)
    for words in ("nature", "law"):
        with pytest.raises(ValueError) as caught:
            carried(gamma, gamma)
        assert words not in str(caught.value)
    kept = {k: v for k, v in universe["integers"].items() if k != "amplitude"}
    refused("names no amplitude", read_world, world, {**universe, "integers": kept})
    assert not any(hasattr(rows, name) for name in ("WIDTH", "HALF_WIDTH", "ROOM"))
    print(
        f"the floor {least} = {least // gamma} Gamma at Gamma {gamma}; the universe's amplitude {scale}"
    )
