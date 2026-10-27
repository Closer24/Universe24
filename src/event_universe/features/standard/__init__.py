"""The standard: a Rule3 pair at one fixed angle, iterated by a notch (ALGEBRA.md #the-four-acts (b), the one-clock tick, Chebyshev's recurrence; #the-direction; the mathematician's repaired form of item (g) and the two hands' item (i), the walk). A mesh's offset is two gears of Rule3's rotation act at the one ratio (K_0, D), D = 2 Gamma^2 and K_0 = D - 1, so that the doubled cosine of the angle per act is 2 K_0 / D = 2 - 1 / Gamma^2 and the angle theta_0 = arccos(1 - 1 / (2 Gamma^2)) is 1 / Gamma to the relative 2.6 x 10^-9 (the law's one rounding, the angle's own: no number of this module); the two gears (cos, sin) a quarter turn apart, each (now, before, fine), the sin gear set by one division X div Gamma and no root (the advisor's second, item 4), both set at the mid tooth D div 2 as every gear of the engine is, at a standard length X a multiple of Gamma (the mathematician's item (i) 4: the mid-tooth start at a multiple of Gamma cancels the fine tooth's resonance at leading order). Each act is `core/rule3.rule3` with the grips 0 (as `features/click.rotated` steps it) and the hold 2 K_0 on the teeth D, forward or at the going -1 bit for bit; iterated per mesh along the one circuit from the first pair to the size |N| of the mesh's count N, the signed sum of the notches n the acts added (n the turn factors' difference across the mesh, node.phased; `orbit_moves`: |N'| - |N| acts, forward where the size grows and the inverse act where it shrinks), so the pair stands at X e^(i |N| theta_0) and is read with the count's sign on the sine gear (`signed_read`): the pair at -n the conjugate of the pair at +n, so that the cube's 48 map the fine teeth as they map the notches; the inverse act exact as before; 2026-10-21 (before this date a negative count iterated the inverse act from the first pair, Rule3's exact inverse and not the forward circuit's conjugate, the sine gear exactly odd and the cosine gear not exactly even, by up to 1,168 notches of X over 3,000 acts and one mesh unit after the fold at 7 percent of the angles above the count 183, which parted the fine teeth of mirror-image pieces); read by the spoke as the hop's two integers (c, s) = (X cos theta, X sin theta) to the walk's bound, and folded into the mesh's one coefficient rounding with the fold's pair (X^c, X^s): (X^c c - X^s s) div X and (X^s c + X^c s) div X rounded half up on the magnitude (`core/rates.rounded`) with the direction's sign attached after, so that the pair read from the two ends is exact by direction (K_t = D M_t Hermitian, the count exact). Bounded and by how much (the two hands' item (i)): the magnitude stands within (Gamma + 1) / 2 notches of X by the mean fine tooth (a telescoping sum, proved) and drifts by at most 1.42 N + 2.3 Gamma notches over N acts (proved), the drift a resonance of the fine tooth's sawtooth with the gear's own frequency, cancelled at leading order by the mid-tooth start; a mesh weight and never a count. Pure functions of integers, Python's or numpy's integer arrays alike (the assembly's kind), no train's name and no number of the calibre."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.acts import carry, mid
from event_universe.core.rates import rounded
from event_universe.core.rule3 import carries, rule3

# a gear of the standard, (now, before, fine), each an integer or an integer array over the meshes
Gear = tuple[Any, Any, Any]
# the pair of gears, (the cosine gear, the sine gear)
Hand = tuple[Gear, Gear]


def standard_rate(gamma: Any) -> Any:
    """The standard's Gamma under the centred count (ALGEBRA.md, The turn per proper tick, the owner's decision of 2026-10-23): the mesh's count K_ij = K_i - K_j is twice the trapezoid sum of the clocked offset to the tick's centre (node.phased), so one count is the half angle theta_0 / 2 and the gear runs at the Gamma 2 Gamma, D = 2 (2 Gamma)^2 and K_0 = D - 1, the angle arccos(1 - 1 / (8 Gamma^2)) = 1 / (2 Gamma) to 6.5 x 10^-10 relative; the rest rotation's bisection (`rotation_unit`, struck 2026-10-24 as dead code and kept by name) kept the gear at Gamma, the unit of the fold's angle."""
    return gamma + gamma


def standard_teeth(gamma: Any) -> Any:
    """The standard's teeth, D = 2 Gamma^2 (the mathematician's item (g): 72,000,000 at Gamma 6,000, 2^26.1), the unit of the doubled cosine 2 K_0 / D."""
    return (gamma + gamma) * gamma


def standard_pinion(gamma: Any) -> Any:
    """The standard's pinion, K_0 = D - 1: the fixed angle theta_0 with 2 cos theta_0 = 2 K_0 / D = 2 - 1 / Gamma^2 exactly, so theta_0 = arccos(1 - 1 / (2 Gamma^2)) = (1 / Gamma)(1 + 1 / (24 Gamma^2) + ...), 1 / Gamma to 2.6 x 10^-9 at Gamma 6,000: the angle's one rounding, fixed here and nowhere else."""
    return standard_teeth(gamma) - 1


def standard_mid(gamma: Any) -> Any:
    """The mid tooth D div 2 = Gamma^2, the fine tooth every gear starts at (the engine's one start, core/acts.mid; item (i) 4, the resonance's leading term cancelled by it)."""
    return mid(standard_teeth(gamma))


def first_pair(length: Any, gamma: Any) -> Hand:
    """The pair at the angle 0: the cosine gear (X, X cos theta_0 rounded as the engine rounds, D div 2), the before X K_0 over D rounded half up once (`core/rates.rounded`, the (D) act at the assembly), and the sine gear a quarter turn behind, (0, -(X div Gamma), D div 2), X sin theta_0 the one exact division X div Gamma (the advisor's second, item 4: within 6 x 10^-4 of a notch at 2^30, no root); X must be a multiple of Gamma (item (i) 4: the sum's extremum X Gamma then a multiple of D, the mid-tooth start cancelling the resonance), refused by name otherwise (2^35 itself is none at Gamma 6,000 = 2^4 3 5^3: the standard length of 2^35's size is (2^35 div Gamma) Gamma, as the mathematician's item (i) takes 178,956 Gamma for 2^30's size); width 63 holds X below 2^35.9 (2 K_0 X + D below 2^63)."""
    teeth = standard_teeth(gamma)
    carries_, fine_x = carry(length, gamma, 0)
    off = np.asarray(fine_x) != 0
    if np.any(off):
        raise ValueError(
            f"the phase line's amplitude X = {np.asarray(length)[off].ravel()[0]} is not a multiple "
            f"of Gamma = {gamma}: the seed is refused (the half-wall birth cancels the walk's resonance "
            "at a multiple of Gamma alone)"
        )
    fine = standard_mid(gamma) + 0 * length  # the mid tooth in the standard length's shape and kind
    cosine: Gear = (length, rounded(length * standard_pinion(gamma), teeth), fine)
    sine: Gear = (0 * length, -carries_, fine)
    return cosine, sine


def act(gear: Gear, gamma: Any, going: int = 1) -> Gear:
    """One act of Rule3's rotation on a gear at (K_0, D): forward, a_next = (2 K_0 a_now + r) div D - a_before with the fine tooth kept, the gear (a_now, a_before, r) to (a_next, a_now, r'); at the going -1 the same act of `core/rule3.rule3` inverted, from (a_next, a_now, r') back to (a_now, a_before, r) bit for bit (ALGEBRA.md #the-direction), the grips 0 and the hold 2 K_0 on the teeth D, as `features/click.rotated` steps the rotation act."""
    if going not in (1, -1):
        raise ValueError(f"the phase line's direction is 1 or -1, not {going}")
    now, before, fine = gear
    teeth = standard_teeth(gamma)
    spring = (
        teeth + teeth - standard_pinion(gamma) - standard_pinion(gamma)
    )  # the gear's own term, 2 w - 2 K_0 = 2: Rule3's gear in its pull form with no meshes
    if going == 1:
        following, carried = rule3(0, spring, teeth, now, before, fine, 1)
        return following, now, carried
    previous, carried = rule3(0, spring, teeth, before, now, fine, -1)
    return before, previous, carried


def deviation(length: Any, gamma: Any) -> int:
    """The circuit's own rounding over the half turn at the standard length X: the pair built from the first pair by the act until the cosine first rises above its lowest (the half turn, pi Gamma counts to the integer; readings.standard_angle builds the clock's circuit to the same turn), the magnitude's departure from X at every count in notches, |c^2 + s^2 - X^2| div 2 X, the largest of them (20 notches at X = 23,000 and 36,022 at the charts' 288,230,376,000 at Gamma 1,000: the departure about X / D at a large X, the resonance's residue past the mid-tooth start)."""
    cosine, sine = first_pair(length, gamma)
    worst, lowest = 0, int(cosine[0])
    while True:
        cosine, sine = act(cosine, gamma), act(sine, gamma)
        c, s = int(cosine[0]), int(sine[0])
        if c > lowest:
            return worst
        lowest = c
        off = abs(c * c + s * s - length * length)
        worst = max(worst, int(carries(off, length + length)))


SHORTEST_HANDS: dict[int, int] = {}  # the shortest hand once per Gamma


def shortest_hand(gamma: Any) -> int:
    """The shortest hand, the floor of the standard length, derived from Gamma alone the way G is (rule3.mesh_unit_of; the owner's word of 2026-10-27, 04:0x UTC): the least multiple of Gamma at which the circuit's rounding resolves one of its own steps over the half turn, `deviation(k Gamma)` below k, the circuit's one step X div Gamma, found by a search by comparisons from k = 1 (23 Gamma at Gamma 1,000: the departure 23 notches against the step 22 at k = 22, 20 against 23 at k = 23, and no k from 23 to 1,000 fails); below it the turn's rounding is coarser than the circuit's step and the engine refuses the scale (`carried`); a piece's own floor for the state's invariance lies above it and is measured (THE-AMPLITUDE-SCALE.md: 1,000 Gamma on the swing's piece, 100,000 Gamma on the chiral setting, the charts' scale 288,230,376 Gamma)."""
    key = int(gamma)
    if key not in SHORTEST_HANDS:
        k = 1
        while deviation(k * key, key) >= k:
            k += 1
        SHORTEST_HANDS[key] = k * key
    return SHORTEST_HANDS[key]


def carried(length: Any, gamma: Any) -> Any:
    """The engine's one refusal of a scale by name, never a verdict of the law and never a phenomenon (the owner's ruling of 2026-10-26, 22:1x UTC, and his words of 2026-10-27, 04:0x and 04:4x: the standard length derived from the rim at the clock, X = Gamma rim, clock.standard_length (DAVID-AMPLITUDES.md section 4; the length declared from outside before it), no width read by the physics; the former `amplitude` cut from the half width less one and the machine's width refusal struck, the value kept in the file): the standard length below the floor, where the turn's rounding is coarser than the circuit's own step; the standard length returned carried."""
    least = shortest_hand(gamma)
    if int(length) < least:
        raise ValueError(
            f"the engine cannot carry the phase line at the amplitude {length}: below the floor "
            f"{least} ({carries(least, gamma)} Gamma) at which the orbit's rounding resolves one step"
        )
    return length
