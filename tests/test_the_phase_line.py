"""The standard as a standalone module (features/standard; ALGEBRA.md #the-four-acts (b), #the-direction; the two hands' item (i)): a Rule3 hand at the one fixed angle theta_0 = 1 / Gamma (K_0 = 2 Gamma^2 - 1 over D = 2 Gamma^2), set on the half teeth at a standard length a multiple of Gamma, iterated by a notch with the angle signed, read as the hop's two integers and folded into the mesh's one coefficient rounding. Integers throughout, the owner's word (no float anywhere in the system, the tests inside it): a magnitude within B notches of X is the inequality (X - B)^2 <= c^2 + s^2 <= (X + B)^2; the cosine is the exact rational K_0 / D by cross multiplication; the sine is the module's own integer sine (`core/rates.sine_rim`, the largest integer whose square is at most the product, no root); the angle is bracketed by the cosine's Taylor bounds as one integer inequality. The bound used throughout (item (i), both hands): the hand's magnitude within Gamma / 2 notches of X standing plus the walk's proved 1.42 N + 2.3 Gamma notches over the test's N acts, taken at the integer ceiling (`bound`), never a count. Every test under 15 seconds; each prints its numbers (the wall clock's seconds, a float, taken out 2026-10-25 by the owner's rule)."""

import numpy as np
import pytest

from event_universe import trains
from event_universe.assembly.piece import check_piece
from event_universe.clock import Clock
from event_universe.core.rates import rounded, sine_rim
from event_universe.core.rule3 import largest_below
from event_universe.features.standard import (
    act,
    carried,
    deviation,
    first_pair,
    shortest_hand,
    standard_mid,
    standard_pinion,
    standard_rate,
    standard_teeth,
)
from tests.laws import refused, world_of


def iterate(hand, count, full_rate, going=1):
    going, count = (going, count) if count >= 0 else (-going, -count)
    for _ in range(count):
        hand = tuple(act(gear, full_rate, going) for gear in hand)
    return hand


GAMMA = 6_000
WALL, COEFFICIENT, X175 = standard_teeth(GAMMA), standard_pinion(GAMMA), 175 * GAMMA
X35 = (2**35 // GAMMA) * GAMMA  # 2^35's size, the largest multiple of Gamma below it: 34,359,738,000
TENTH, ROOM = 10**10, 10**10 + 26  # the angle's relative unit, and (1 + 2.6 x 10^-9) 10^10


def bound(acts: int) -> int:
    """The hands' bound in notches after `acts` acts, at its integer ceiling: (Gamma + 1) div 2 standing (the mean fine tooth, a telescoping sum) plus the walk's proved 1.42 N + 2.3 Gamma (item (i), the mathematician's 2), (142 N + 230 Gamma + 99) div 100."""
    return (GAMMA + 1) // 2 + (142 * acts + 230 * GAMMA + 99) // 100


def within(hand, x: int, room: int, index: int = 0) -> bool:
    """The hand's (c, s) at the now (index 0) or at the before (index 1) within `room` notches of X in magnitude, as the integer inequality (X - room)^2 <= c^2 + s^2 <= (X + room)^2."""
    c, s = int(hand[0][index]), int(hand[1][index])
    return (x - room) ** 2 <= c * c + s * s <= (x + room) ** 2


def off(hand, x: int, index: int = 0) -> tuple[int, int]:
    """|c + i s| - X in notches as a quotient with its remainder: the largest integer whose square is at most c^2 + s^2 (`rule3.largest_below`, no root), less X, and the square's excess over that integer's square."""
    c, s = int(hand[0][index]), int(hand[1][index])
    floor = largest_below(c * c + s * s)
    return floor - x, c * c + s * s - floor * floor


def test_the_seed_stands_on_the_circle_at_the_half_wall_and_refuses_an_amplitude_off_gamma():
    """The fixed angle: D = 2 Gamma^2 = 72,000,000, K_0 = D - 1 = 71,999,999, 2 K_0 / D = 2 - 1 / Gamma^2 exactly by cross multiplication; theta_0 Gamma in [1, 1 + 2.6 x 10^-9]: cos x > 1 - x^2 / 2 at x = 1 / Gamma = cos theta_0, and cos x <= 1 - x^2 / 2 + x^4 / 24 at x = ROOM / (Gamma 10^10) is at most cos theta_0 by the integer inequality 12 Gamma^2 (ROOM^2 10^20 - 10^40) >= ROOM^4. The setting at X of 2^35's size and at X = 175 Gamma: the cosine gear (X, X cos theta_0 rounded half up, D div 2), the before within half a notch of X K_0 / D (2 |D before - X K_0| <= D), the sine gear (0, -(X div Gamma), D div 2), the sine setting within a notch of X sin theta_0 (the advisor's second, item 4) against the module's integer sine floor(X D sin theta_0); c^2 + s^2 within the bound of X^2 at the now and at the before, and after ten acts; 2^35 itself and 2^35 + 1 refused by name (neither a multiple of Gamma = 2^4 3 5^3)."""
    assert (WALL, COEFFICIENT) == (2 * GAMMA**2, WALL - 1) == (72_000_000, 71_999_999)
    assert 2 * COEFFICIENT * GAMMA**2 == (2 * GAMMA**2 - 1) * WALL  # 2 K_0 / D = 2 - 1 / Gamma^2
    margin = 12 * GAMMA**2 * (ROOM**2 * TENTH**2 - TENTH**4) - ROOM**4
    assert margin >= 0 and standard_mid(GAMMA) == GAMMA**2 == WALL // 2
    for x in (X35, X175):
        cosine, sine = hand = first_pair(x, GAMMA)
        assert cosine == (x, rounded(x * COEFFICIENT, WALL), WALL // 2)
        assert sine == (0, -(x // GAMMA), WALL // 2)
        assert 2 * abs(WALL * int(cosine[1]) - x * COEFFICIENT) <= WALL
        scaled = -int(sine[1]) * WALL  # (X div Gamma) D against floor(X D sin theta_0)
        assert scaled - WALL <= sine_rim(COEFFICIENT, WALL, x) < scaled + WALL
        assert within(hand, x, bound(0)) and within(hand, x, bound(0), 1)
        assert within(turned := iterate(hand, 10, GAMMA), x, bound(10))
        print(
            f"seed X = {x}: now off {off(hand, x)} levels (floor, the square's excess), before off {off(hand, x, 1)}, after 10 acts {off(turned, x)} (bound {bound(10)})"
        )
    refused("not a multiple of Gamma", first_pair, 2**35, GAMMA)
    refused("not a multiple of Gamma", first_pair, 2**35 + 1, GAMMA)
    refused("not a multiple", first_pair, np.array([X35, X35 + 1], dtype=np.int64), GAMMA)
    print(f"theta_0 Gamma - 1 <= {ROOM - TENTH} / 10^10, margin {margin}")


def test_the_reversal_is_bit_exact_over_ten_thousand_acts():
    """10^4 acts forward then 10^4 inverse acts (going -1): both gears, notches and fine teeth, bit for bit the setting; the same through `iterate` at going -1 and through the signed count."""
    hand = first_pair(X35, GAMMA)
    cosine, sine = hand
    acts = 10**4
    for _ in range(acts):
        cosine, sine = act(cosine, GAMMA), act(sine, GAMMA)
    forward = (cosine, sine)
    assert forward != hand
    for _ in range(acts):
        cosine, sine = act(cosine, GAMMA, -1), act(sine, GAMMA, -1)
    assert (cosine, sine) == hand
    assert iterate(forward, acts, GAMMA, -1) == hand and iterate(forward, -acts, GAMMA) == hand
    assert iterate(hand, acts, GAMMA) == forward
    refused("direction is 1 or -1", act, hand[0], GAMMA, 0)
    print(
        f"10^4 acts forward and back: bit for bit, remainders {forward[0][2]}, {forward[1][2]} on the way"
    )


def test_the_amplitude_is_the_universes_and_the_engine_refuses_a_scale_below_the_floor_from_gamma():
    """The standard length declared from outside (the owner's words of 2026-10-27, 04:0x and 04:4x UTC; THE-AMPLITUDE-SCALE.md): the calibre file names it beside rim, Gamma and T (288,230,376,000 in the shipped calibres, a multiple of 2 Gamma), the assembly refuses a file naming none, and the engine carries it above the shortest hand derived from Gamma alone, 23 Gamma at Gamma 1,000 (the circuit's departure 23 notches against the step 22 at k = 22, 20 against 23 at k = 23), refusing a scale below it by name as the engine's, never as nature's; no width and no room stands in the engine."""
    calibre, piece = world_of("world_hole.json")
    full, length = int(calibre["integers"]["node_clock"]), int(calibre["integers"]["amplitude"])
    least = shortest_hand(full)
    assert least == 23 * full and deviation(22 * full, full) >= 22 > deviation(least, full)
    assert length == 288_230_376_000 and length % standard_rate(full) == 0 and least < length
    assert carried(length, full) == length and Clock(calibre, piece).standard_length == length
    refused("engine cannot carry", carried, least - full, full)
    for words in ("nature", "law"):
        with pytest.raises(ValueError) as caught:
            carried(full, full)
        assert words not in str(caught.value)
    kept = {k: v for k, v in calibre["integers"].items() if k != "amplitude"}
    refused("names no amplitude", check_piece, piece, {**calibre, "integers": kept})
    assert not any(hasattr(trains, name) for name in ("WIDTH", "HALF_WIDTH", "ROOM"))
    print(
        f"the floor {least} = {least // full} Gamma at Gamma {full}; the universe's amplitude {length}"
    )
