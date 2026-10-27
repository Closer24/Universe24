"""The phase line: a Rule3 pair at one fixed angle, iterated by a level (ALGEBRA.md #the-four-acts (b), the one-Node step, Chebyshev's recurrence; #the-direction; the mathematician's repaired form of item (g) and the two hands' item (i), the walk). A Link's phase is two lines of Rule3's rotation act at the one coefficient pair (K_0, D), D = 2 Gamma^2 and K_0 = D - 1, so that the doubled cosine of the angle per act is 2 K_0 / D = 2 - 1 / Gamma^2 and the angle theta_0 = arccos(1 - 1 / (2 Gamma^2)) is 1 / Gamma to the relative 2.6 x 10^-9 (the law's one rounding, the angle's own: no number of this module); the two lines (cos, sin) a quarter turn apart, each (now, before, remainder), the sin line seeded by one division X div Gamma and no root (the advisor's second, item 4), both born on the half wall D div 2 as every line of the engine is, at an amplitude X a multiple of Gamma (the mathematician's item (i) 4: the half-wall birth at a multiple of Gamma cancels the remainder's resonance at leading order). Each act is `core/rule3.rule3` with the reads 0 (as `features/click.rotated` steps it) and the self coefficient 2 K_0 on the wall D, forward or at direction -1 bit for bit; iterated per Link along the one orbit from the seed to the size |N| of the Link's count N, the signed sum of the levels n the acts added (n the turn factors' difference across the Link, node.phased; `orbit_moves`: |N'| - |N| acts, forward where the size grows and the inverse act where it shrinks), so the pair stands at X e^(i |N| theta_0) and is read with the count's sign on the sine line (`signed_read`): the pair at -n the conjugate of the pair at +n, so that the cube's 48 map the remainders as they map the levels; the inverse act exact as before; 2026-10-21 (before this date a negative count iterated the inverse act from the seed, Rule3's exact inverse and not the forward orbit's conjugate, the sine line exactly odd and the cosine line not exactly even, by up to 1,168 levels of X over 3,000 acts and one Link unit after the fold at 7 percent of the angles above the count 183, which parted the remainders of mirror-image worlds); read by the Port as the hop's two integers (c, s) = (X cos theta, X sin theta) to the walk's bound, and folded into the Link's one coefficient rounding with the fold's pair (X^c, X^s): (X^c c - X^s s) div X and (X^s c + X^c s) div X rounded half up on the magnitude (`core/paces.rounded`) with the direction's sign attached after, so that the pair read from the two ends is exact by direction (K_t = D M_t Hermitian, the count exact). Bounded and by how much (the two hands' item (i)): the magnitude stands within (Gamma + 1) / 2 levels of X by the mean remainder (a telescoping sum, proved) and drifts by at most 1.42 N + 2.3 Gamma levels over N acts (proved), the drift a resonance of the remainder's sawtooth with the line's own frequency, cancelled at leading order by the half-wall birth; a Link weight and never a count. Pure functions of integers, Python's or numpy's integer arrays alike (the loader's kind), no family's name and no number of the universe."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.acts import carry, mid
from event_universe.core.rates import rounded
from event_universe.core.rule3 import carries, rule3

# a line of the phase, (now, before, remainder), each an integer or an integer array over the Links
Gear = tuple[Any, Any, Any]
# the pair of lines, (the cosine line, the sine line)
Hand = tuple[Gear, Gear]


def standard_rate(gamma: Any) -> Any:
    """The phase line's Gamma under the centred count (ALGEBRA.md, The turn per proper interval, the owner's decision of 2026-10-23): the Link's count K_ij = K_i - K_j is twice the trapezoid sum of the clocked potential to the step's centre (node.phased), so one count is the half angle theta_0 / 2 and the line runs at the Gamma 2 Gamma, D = 2 (2 Gamma)^2 and K_0 = D - 1, the angle arccos(1 - 1 / (8 Gamma^2)) = 1 / (2 Gamma) to 6.5 x 10^-10 relative; the rest rotation's bisection (`rotation_unit`, struck 2026-10-24 as dead code and kept by name) kept the line at Gamma, the unit of the fold's angle."""
    return gamma + gamma


def standard_teeth(gamma: Any) -> Any:
    """The phase line's wall, D = 2 Gamma^2 (the mathematician's item (g): 72,000,000 at Gamma 6,000, 2^26.1), the unit of the doubled cosine 2 K_0 / D."""
    return (gamma + gamma) * gamma


def standard_pinion(gamma: Any) -> Any:
    """The phase line's coefficient, K_0 = D - 1: the fixed angle theta_0 with 2 cos theta_0 = 2 K_0 / D = 2 - 1 / Gamma^2 exactly, so theta_0 = arccos(1 - 1 / (2 Gamma^2)) = (1 / Gamma)(1 + 1 / (24 Gamma^2) + ...), 1 / Gamma to 2.6 x 10^-9 at Gamma 6,000: the angle's one rounding, fixed here and nowhere else."""
    return standard_teeth(gamma) - 1


def standard_mid(gamma: Any) -> Any:
    """The half wall D div 2 = Gamma^2, the remainder every line is born with (the engine's one birth, core/acts.born; item (i) 4, the resonance's leading term cancelled by it)."""
    return mid(standard_teeth(gamma))


def first_pair(amplitude: Any, gamma: Any) -> Hand:
    """The pair at the angle 0: the cosine line (X, X cos theta_0 rounded as the engine rounds, D div 2), the before X K_0 over D rounded half up once (`core/paces.rounded`, the (D) act at load), and the sine line a quarter turn behind, (0, -(X div Gamma), D div 2), X sin theta_0 the one exact division X div Gamma (the advisor's second, item 4: within 6 x 10^-4 of a level at 2^30, no root); X must be a multiple of Gamma (item (i) 4: the sum's extremum X Gamma then a multiple of D, the half-wall birth cancelling the resonance), refused by name otherwise (2^35 itself is none at Gamma 6,000 = 2^4 3 5^3: the amplitude of 2^35's size is (2^35 div Gamma) Gamma, as the mathematician's item (i) takes 178,956 Gamma for 2^30's size); width 63 holds X below 2^35.9 (2 K_0 X + D below 2^63)."""
    wall = standard_teeth(gamma)
    quotient_, remainder = carry(amplitude, gamma, 0)
    off = np.asarray(remainder) != 0
    if np.any(off):
        raise ValueError(
            f"the phase line's amplitude X = {np.asarray(amplitude)[off].ravel()[0]} is not a multiple "
            f"of Gamma = {gamma}: the seed is refused (the half-wall birth cancels the walk's resonance "
            "at a multiple of Gamma alone)"
        )
    fine = standard_mid(gamma) + 0 * amplitude  # the half wall in the amplitude's shape and kind
    cosine: Gear = (amplitude, rounded(amplitude * standard_pinion(gamma), wall), fine)
    sine: Gear = (0 * amplitude, -quotient_, fine)
    return cosine, sine


def act(line: Gear, gamma: Any, direction: int = 1) -> Gear:
    """One act of Rule3's rotation on a line at (K_0, D): forward, a_next = (2 K_0 a_now + r) div D - a_before with the remainder kept, the line (a_now, a_before, r) to (a_next, a_now, r'); at direction -1 the same act of `core/rule3.rule3` inverted, from (a_next, a_now, r') back to (a_now, a_before, r) bit for bit (ALGEBRA.md #the-direction), the reads 0 and the self coefficient 2 K_0 on the wall D, as `features/click.rotated` steps the rotation act."""
    if direction not in (1, -1):
        raise ValueError(f"the phase line's direction is 1 or -1, not {direction}")
    now, before, remainder = line
    wall = standard_teeth(gamma)
    mass = (
        wall + wall - standard_pinion(gamma) - standard_pinion(gamma)
    )  # the line's own term, 2 w - 2 K_0 = 2: Rule3's flux line with no Links
    if direction == 1:
        following, carried = rule3(0, mass, wall, now, before, remainder, 1)
        return following, now, carried
    previous, carried = rule3(0, mass, wall, before, now, remainder, -1)
    return before, previous, carried


def deviation(amplitude: Any, gamma: Any) -> int:
    """The orbit's own rounding over the half turn at the amplitude X: the pair built from the seed by the act until the cosine first rises above its lowest (the half turn, pi Gamma counts to the integer; readings.pair_angle builds the Node's orbit to the same turn), the magnitude's departure from X at every count in levels, |c^2 + s^2 - X^2| div 2 X, the largest of them (20 levels at X = 23,000 and 36,022 at the records' 288,230,376,000 at Gamma 1,000: the departure about X / D at a large X, the resonance's residue past the half-wall birth)."""
    cosine, sine = first_pair(amplitude, gamma)
    worst, lowest = 0, int(cosine[0])
    while True:
        cosine, sine = act(cosine, gamma), act(sine, gamma)
        c, s = int(cosine[0]), int(sine[0])
        if c > lowest:
            return worst
        lowest = c
        off = abs(c * c + s * s - amplitude * amplitude)
        worst = max(worst, int(carries(off, amplitude + amplitude)))


SHORTEST_HANDS: dict[int, int] = {}  # the floor once per Gamma


def shortest_hand(gamma: Any) -> int:
    """The floor of the phase line's amplitude, derived from Gamma alone the way G is (rule3.link_unit_of; the owner's word of 2026-10-27, 04:0x UTC): the least multiple of Gamma at which the orbit's rounding resolves one of its own steps over the half turn, `deviation(k Gamma)` below k, the orbit's one step X div Gamma, found by a search by comparisons from k = 1 (23 Gamma at Gamma 1,000: the departure 23 levels against the step 22 at k = 22, 20 against 23 at k = 23, and no k from 23 to 1,000 fails); below it the turn's rounding is coarser than the orbit's step and the engine refuses the scale (`carried`); a world's own floor for the state's invariance lies above it and is measured (THE-AMPLITUDE-SCALE.md: 1,000 Gamma on the bang's world, 100,000 Gamma on the chiral seed, the records' scale 288,230,376 Gamma)."""
    key = int(gamma)
    if key not in SHORTEST_HANDS:
        k = 1
        while deviation(k * key, key) >= k:
            k += 1
        SHORTEST_HANDS[key] = k * key
    return SHORTEST_HANDS[key]


def carried(amplitude: Any, gamma: Any) -> Any:
    """The engine's one refusal of a scale by name, never a verdict of the law and never a phenomenon (the owner's ruling of 2026-10-26, 22:1x UTC, and his words of 2026-10-27, 04:0x and 04:4x: the amplitude declared from outside in the universe file and read at the load, node.X, no width read by the physics; the former `amplitude` cut from the half width less one and the machine's width refusal struck, the value kept in the file): the amplitude below the floor, where the turn's rounding is coarser than the orbit's own step; the amplitude returned carried."""
    least = shortest_hand(gamma)
    if int(amplitude) < least:
        raise ValueError(
            f"the engine cannot carry the phase line at the amplitude {amplitude}: below the floor "
            f"{least} ({carries(least, gamma)} Gamma) at which the orbit's rounding resolves one step"
        )
    return amplitude
