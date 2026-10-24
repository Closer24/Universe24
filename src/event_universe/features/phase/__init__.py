"""The phase line: a Rule3 pair at one fixed angle, iterated by a level (ALGEBRA.md #the-four-acts (b), the one-Node step, Chebyshev's recurrence; #the-direction; the mathematician's repaired form of item (g) and the two hands' item (i), the walk). A Link's phase is two lines of Rule3's rotation act at the one coefficient pair (K_0, D), D = 2 Gamma^2 and K_0 = D - 1, so that the doubled cosine of the angle per act is 2 K_0 / D = 2 - 1 / Gamma^2 and the angle theta_0 = arccos(1 - 1 / (2 Gamma^2)) is 1 / Gamma to the relative 2.6 x 10^-9 (the law's one rounding, the angle's own: no number of this module); the two lines (cos, sin) a quarter turn apart, each (now, before, remainder), the sin line seeded by one division X div Gamma and no root (the advisor's second, item 4), both born on the half wall D div 2 as every line of the engine is, at an amplitude X a multiple of Gamma (the mathematician's item (i) 4: the half-wall birth at a multiple of Gamma cancels the remainder's resonance at leading order). Each act is `core/rule3.rule3` with the reads 0 (as `features/click.rotated` steps it) and the self coefficient 2 K_0 on the wall D, forward or at direction -1 bit for bit; iterated per Link along the one orbit from the seed to the size |N| of the Link's count N, the signed sum of the levels n the acts added (n the turn factors' difference across the Link, node.phased; `orbit_moves`: |N'| - |N| acts, forward where the size grows and the inverse act where it shrinks), so the pair stands at X e^(i |N| theta_0) and is read with the count's sign on the sine line (`signed_read`): the pair at -n the conjugate of the pair at +n, so that the cube's 48 map the remainders as they map the levels; the inverse act exact as before; 2026-10-21 (before this date a negative count iterated the inverse act from the seed, Rule3's exact inverse and not the forward orbit's conjugate, the sine line exactly odd and the cosine line not exactly even, by up to 1,168 levels of X over 3,000 acts and one Link unit after the fold at 7 percent of the angles above the count 183, which parted the remainders of mirror-image worlds); read by the Port as the hop's two integers (c, s) = (X cos theta, X sin theta) to the walk's bound, and folded into the Link's one coefficient rounding with the fold's pair (X^c, X^s): (X^c c - X^s s) div X and (X^s c + X^c s) div X rounded half up on the magnitude (`core/paces.rounded`) with the direction's sign attached after, so that the pair read from the two ends is exact by direction (K_t = D M_t Hermitian, the count exact). Bounded and by how much (the two hands' item (i)): the magnitude stands within (Gamma + 1) / 2 levels of X by the mean remainder (a telescoping sum, proved) and drifts by at most 1.42 N + 2.3 Gamma levels over N acts (proved), the drift a resonance of the remainder's sawtooth with the line's own frequency, cancelled at leading order by the half-wall birth; a Link weight and never a count. Pure functions of integers, Python's or numpy's integer arrays alike (the loader's kind), no family's name and no number of the universe."""

from __future__ import annotations

import weakref
from functools import cache
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.paces import rounded
from event_universe.core.rule3 import division_forward, rule3

# a line of the phase, (now, before, remainder), each an integer or an integer array over the Links
Line = tuple[Any, Any, Any]
# the pair of lines, (the cosine line, the sine line)
Pair = tuple[Line, Line]


def unit(gamma: Any) -> Any:
    """The phase line's Gamma under the centred count (ALGEBRA.md, The turn per proper interval, the owner's decision of 2026-10-23): the Link's count K_ij = K_i - K_j is twice the trapezoid sum of the clocked potential to the step's centre (node.phased), so one count is the half angle theta_0 / 2 and the line runs at the Gamma 2 Gamma, D = 2 (2 Gamma)^2 and K_0 = D - 1, the angle arccos(1 - 1 / (8 Gamma^2)) = 1 / (2 Gamma) to 6.5 x 10^-10 relative; the rest rotation's bisection (`rotation_unit`) keeps the line at Gamma, the unit of the fold's angle."""
    return 2 * gamma


def D(gamma: Any) -> Any:
    """The phase line's wall, D = 2 Gamma^2 (the mathematician's item (g): 72,000,000 at Gamma 6,000, 2^26.1), the unit of the doubled cosine 2 K_0 / D."""
    return 2 * gamma * gamma


def K0(gamma: Any) -> Any:
    """The phase line's coefficient, K_0 = D - 1: the fixed angle theta_0 with 2 cos theta_0 = 2 K_0 / D = 2 - 1 / Gamma^2 exactly, so theta_0 = arccos(1 - 1 / (2 Gamma^2)) = (1 / Gamma)(1 + 1 / (24 Gamma^2) + ...), 1 / Gamma to 2.6 x 10^-9 at Gamma 6,000: the angle's one rounding, fixed here and nowhere else."""
    return D(gamma) - 1


def half_wall(gamma: Any) -> Any:
    """The half wall D div 2 = Gamma^2, the remainder every line is born with (the engine's birth; item (i) 4, the resonance's leading term cancelled by it)."""
    return division_forward(D(gamma), 2, 0)[0]


def seed(amplitude: Any, gamma: Any) -> Pair:
    """The pair at the angle 0: the cosine line (X, X cos theta_0 rounded as the engine rounds, D div 2), the before X K_0 over D rounded half up once (`core/paces.rounded`, the (D) act at load), and the sine line a quarter turn behind, (0, -(X div Gamma), D div 2), X sin theta_0 the one exact division X div Gamma (the advisor's second, item 4: within 6 x 10^-4 of a level at 2^30, no root); X must be a multiple of Gamma (item (i) 4: the sum's extremum X Gamma then a multiple of D, the half-wall birth cancelling the resonance), refused by name otherwise (2^35 itself is none at Gamma 6,000 = 2^4 3 5^3: the amplitude of 2^35's size is (2^35 div Gamma) Gamma, as the mathematician's item (i) takes 178,956 Gamma for 2^30's size); width 63 holds X below 2^35.9 (2 K_0 X + D below 2^63)."""
    wall = D(gamma)
    quotient, remainder = division_forward(amplitude, gamma, 0)
    off = np.asarray(remainder) != 0
    if np.any(off):
        raise ValueError(
            f"the phase line's amplitude X = {np.asarray(amplitude)[off].ravel()[0]} is not a multiple "
            f"of Gamma = {gamma}: the seed is refused (the half-wall birth cancels the walk's resonance "
            "at a multiple of Gamma alone)"
        )
    half = half_wall(gamma) + 0 * amplitude  # the half wall in the amplitude's shape and kind
    cosine: Line = (amplitude, rounded(amplitude * K0(gamma), wall), half)
    sine: Line = (0 * amplitude, -quotient, half)
    return cosine, sine


def act(line: Line, gamma: Any, direction: int = 1) -> Line:
    """One act of Rule3's rotation on a line at (K_0, D): forward, a_next = (2 K_0 a_now + r) div D - a_before with the remainder kept, the line (a_now, a_before, r) to (a_next, a_now, r'); at direction -1 the same act of `core/rule3.rule3` inverted, from (a_next, a_now, r') back to (a_now, a_before, r) bit for bit (ALGEBRA.md #the-direction), the reads 0 and the self coefficient 2 K_0 on the wall D, as `features/click.rotated` steps the rotation act."""
    if direction not in (1, -1):
        raise ValueError(f"the phase line's direction is 1 or -1, not {direction}")
    now, before, remainder = line
    wall = D(gamma)
    mass = (
        wall + wall - 2 * K0(gamma)
    )  # the line's own term, 2 w - 2 K_0 = 2: Rule3's flux line with no Links
    if direction == 1:
        following, carried = rule3(0, mass, wall, now, before, remainder, 1)
        return following, now, carried
    previous, carried = rule3(0, mass, wall, before, now, remainder, -1)
    return before, previous, carried


def chosen(mask: Any, taken: Line, kept: Line) -> Line:
    """A line's three integers from `taken` where the mask holds and from `kept` elsewhere, over the Links; the mask over the whole board or one truth."""
    now, before, remainder = (np.where(mask, a, b) for a, b in zip(taken, kept, strict=True))
    return now, before, remainder


def iterate(pair: Pair, count: Any, gamma: Any, direction: int = 1) -> Pair:
    """The act applied |n| times to both lines, n = `count` a level (one integer, or an integer array per Link), in the sense of n's sign: n < 0 applies the inverse act, so that the angle is signed, n theta_0; `direction` -1 is the back-step of the same n (the inverse of every act in the reverse order, |n| acts in the opposite sense), so iterate(iterate(pair, n), n, -1) is the pair bit for bit. Over arrays, each Link takes its own count: the k-th round applies the act where |n| >= k, forward where n is positive and inverse where negative, through the largest |n| on the board; a Link at n = 0 is untouched."""
    if direction not in (1, -1):
        raise ValueError(f"the phase line's direction is 1 or -1, not {direction}")
    levels = np.asarray(count)
    if levels.ndim == 0:
        sense = direction * (1 if int(levels) >= 0 else -1)
        cosine, sine = pair
        for _ in range(abs(int(levels))):
            cosine, sine = act(cosine, gamma, sense), act(sine, gamma, sense)
        return cosine, sine
    cosine, sine = pair
    if levels.size == 0:
        return cosine, sine
    signed = direction * levels
    for round_ in range(1, int(np.abs(levels).max()) + 1):
        forward, backward = signed >= round_, signed <= -round_
        cosine = chosen(forward, act(cosine, gamma, 1), chosen(backward, act(cosine, gamma, -1), cosine))
        sine = chosen(forward, act(sine, gamma, 1), chosen(backward, act(sine, gamma, -1), sine))
    return cosine, sine


SPACING = (
    1 << (MAX_WORK_INT.bit_length() >> 3)
)  # the orbit's checkpoints, one pair kept every so many acts along the orbit from the seed: 2^7 = 128 at the hardware's 63 bits, a size of the table and no number of the law


class Orbit:
    """The one orbit of the phase pair from its seed at one amplitude and one Gamma (node.phase_carried: every Link's pair stands at the orbit's count |K|, the acts from the seed one by one, forward and inverse exact; the acts compose in sequence and in no closed form, every act rounding at its wall, so the pair at a count is reached by that many acts and no fewer): the pair at every SPACING-th count kept (`checkpoints`) with the farthest pair reached (`reached`, `pair`), so that the pair at any count is the checkpoint at or below it carried by fewer than SPACING acts (`pairs_at`), the same integers as the acts one by one from the seed, and the acts of an interval over the board number the farthest count's advance and not the Links' sum (the architect's round of 2026-10-24)."""

    def __init__(self, gamma: int, amplitude: int) -> None:
        self.gamma, self.reached, self.pair = gamma, 0, seed(amplitude, gamma)
        self.checkpoints: dict[int, Pair] = {0: self.pair}

    def carried_to(self, count: int) -> None:
        """The orbit carried forward act by act to `count` where it stands short of it, the checkpoints laid on the way."""
        while self.reached < count:
            self.pair = (act(self.pair[0], self.gamma, 1), act(self.pair[1], self.gamma, 1))
            self.reached += 1
            if division_forward(self.reached, SPACING, 0)[1] == 0:
                self.checkpoints[self.reached] = self.pair

    def pairs_at(self, counts: Any, standing: Any, pair: Pair, kind: Any) -> Pair:
        """The pairs at the counts `counts` (an array of sizes |K'| over the Links, every one at or above 0) in the arrays' `kind`, from the pairs `pair` standing at the sizes `standing`: each Link carried from its own pair by |K'| - |K| acts (forward where the size grows, the inverse act where it shrinks) where that is the shorter way, and from the checkpoint at or below |K'| by the rest otherwise, both the orbit's own integers; the Links together in one iteration of as many rounds as the longest way, fewer than SPACING (`iterate`, each Link its own count)."""
        sizes = np.asarray(counts, dtype=object)
        flat = [int(x) for x in sizes.reshape(-1).tolist()]
        self.carried_to(max(flat, default=0))
        places = [division_forward(m, SPACING, 0) for m in flat]
        bases = [self.checkpoints[int(q) * SPACING] for q, _rest in places]
        rest = np.array([r for _q, r in places], dtype=object).reshape(sizes.shape)
        moved = sizes - np.asarray(standing, dtype=object)
        own = np.abs(moved) < rest  # the shorter way from the pair standing

        def line_at(line: int) -> Line:
            now, before, remainder = (
                np.where(
                    own,
                    np.asarray(pair[line][part], dtype=object),
                    np.array([base[line][part] for base in bases], dtype=object).reshape(sizes.shape),
                )
                for part in range(3)
            )
            return now, before, remainder

        def in_kind(line: Line) -> Line:
            now, before, remainder = (np.asarray(a, dtype=kind) for a in line)
            return now, before, remainder

        cosine, sine = iterate((line_at(0), line_at(1)), np.where(own, moved, rest), self.gamma)
        return in_kind(cosine), in_kind(sine)


ORBITS: dict[
    tuple[int, int], Orbit
] = {}  # the orbits by (Gamma, amplitude), cleared at a run's start (resonance.clear_memo)
SEEDED: dict[
    int, tuple[Any, Orbit]
] = {}  # per seeded NodeState (by id, with a weak reference that tells a reused id apart) the orbit its Links' pairs stand on (node.seed_phases)


def seeded(state: Any, gamma: int, amplitude: int) -> None:
    """A holder's NodeState seeded at the angle 0 registered with the orbit its pairs stand on, the orbit made once per (Gamma, amplitude)."""
    orbit = ORBITS.setdefault((gamma, amplitude), Orbit(gamma, amplitude))
    SEEDED[id(state)] = (weakref.ref(state), orbit)


def orbit_of(state: Any) -> Orbit | None:
    """The orbit a NodeState's pairs stand on, None where the state was not seeded by the lattice (a state built by hand; its pairs then carried act by act)."""
    kept = SEEDED.get(id(state))
    return kept[1] if kept is not None and kept[0]() is state else None


def read(pair: Pair) -> tuple[Any, Any]:
    """The hop's two integers at the amplitude X, (c, s) = (cosine now, sine now) = (X cos theta, X sin theta) at the pair's angle theta = n theta_0, to the walk's bound (item (i): within (Gamma + 1) / 2 levels standing and 1.42 N + 2.3 Gamma levels over N acts, proved); the Port at the -a end reads the same pair conjugated, (c, -s)."""
    cosine, sine = pair
    return cosine[0], sine[0]


def orbit_moves(standing: Any, count: Any, direction: int = 1) -> tuple[Any, Any]:
    """The Link's count after an act and the acts that carry its pair there along the one orbit from the seed (`iterate`; 2026-10-21): the count standing at N (the signed sum of the levels the acts added, the Link's angle in the unit theta_0, one integer per Link), the interval's level n, the count reached N + n forward (`direction` 1) and N - n back (-1); the pair stands at the count's size |N| on the forward orbit from the seed and is carried by |N'| - |N| acts, forward where the size grows and by the inverse act where it shrinks, the two acts each other's inverse on every state (ALGEBRA.md #the-direction), so that the back-step's acts undo the forward's act for act and a count below 0 stands at the pair of its size, read conjugated (`signed_read`): the pair at -n the conjugate of the pair at +n, so that the cube's 48 map the remainders as they map the levels; the inverse act exact as before. Returns (the count reached, the acts, signed)."""
    reached = standing + direction * count
    return reached, np.abs(reached) - np.abs(standing)


def signed_read(pair: Pair, count: Any) -> tuple[Any, Any]:
    """The hop's two integers at a signed count (`read`): (c, s) at a count at or above 0 and (c, -s) below it, the pair at -n the conjugate of the pair at +n, so that the cube's 48 map the remainders as they map the levels (2026-10-21; `orbit_moves`); at the count 0 the sine line stands at 0 and the sign is nothing."""
    cosine, sine = read(pair)
    return cosine, np.where(np.asarray(count) < 0, -sine, sine)


def signed_rounded(numerator: Any, wall: Any) -> Any:
    """The numerator over the wall rounded half up on the magnitude (`core/paces.rounded` on |numerator|) with the sign attached after, the engine's one signed rounding, so that the rounding is odd: signed_rounded(-v, X) = -signed_rounded(v, X) exactly, the fold's pair exact by direction (ALGEBRA.md, The clock family on the Ports and The sign holder rotates the two-part record: one rounding on the magnitude with the direction's sign attached after, the mathematician's item (g)); a scalar in its own integers, Python's exact beyond the width, as the piece's momentum, the reader's projected level and the momentum reading in T's unit take it (`node_detector.piece_momentum`, `node_detector.arriving`, `take.scaled`), a whole-board array in the array's kind (`fold`; the Link pairs, plane.py)."""
    if np.ndim(numerator) == 0:
        size = rounded(abs(numerator), wall)
        return -size if numerator < 0 else size
    sign = np.where(np.asarray(numerator) < 0, -1, 1)
    return sign * rounded(np.abs(numerator), wall)


def fold(fold_cosine: Any, fold_sine: Any, cosine: Any, sine: Any, amplitude: Any) -> tuple[Any, Any]:
    """The product pair of the fold's (X^c, X^s) with the phase pair (c, s) at the amplitude X, rounded once into the Link's unit: ((X^c c - X^s s) div X, (X^s c + X^c s) div X), each the engine's one rounding half up on the magnitude with the direction's sign attached after (`signed_rounded`), so that the Link read from its other end, (X^c, -X^s) with (c, -s), gives the conjugate pair exactly, X^s_ji = -X^s_ij (the count exact by Hermiticity, Theorem 3's K_ji = conj K_ij)."""
    real = fold_cosine * cosine - fold_sine * sine
    imaginary = fold_sine * cosine + fold_cosine * sine
    return signed_rounded(real, amplitude), signed_rounded(imaginary, amplitude)


def amplitude(gamma: Any, width: int) -> int:
    """The phase line's amplitude X, derived from the width and never written (the two hands' item (i): X of 2^35's size at width 63, 2 K_0 X + D below 2^width): half of the act's room, (2^width - 1) div (2 D) div 2, the half the walk's room (the pair's magnitude within 1.42 N + 2.3 Gamma levels of X over N acts), rounded down to a multiple of Gamma (the half-wall birth cancels the resonance at a multiple of Gamma alone, `seed`): 32,025,594,000 at Gamma 6,000 and width 63 (2^34.9; the hands' 2^35 div Gamma times Gamma is 34,359,738,000, 35 being no literal of the law); refused by name where the width leaves no multiple of Gamma."""
    largest = 2**width - 1
    room = division_forward(largest, 2 * D(gamma), 0)[0]
    half = division_forward(room, 2, 0)[0]
    found = division_forward(half, gamma, 0)[0] * gamma
    if int(found) < int(gamma):
        raise ValueError(
            f"the width {width} leaves no multiple of Gamma = {gamma} inside the phase act's room "
            f"2 K_0 X + D < 2^{width}: the phase line's amplitude is refused"
        )
    return int(found)


def quarter_turn(amplitude: int, gamma: int) -> int:
    """The count of acts to the quarter turn, the largest n with the cosine line at or above 0, found by bisection on the phase line seeded at the amplitude X as `rotation_unit` finds the rest rotation (kind S), the pair carried along the probe: pi Gamma / 2 to the walk's bound, 9,424 at Gamma 6,000; the exclusivity bound reads it (`resonance.unit_weight`)."""
    low, high, pair = 0, 2 * gamma, seed(amplitude, gamma)
    while high - low > 1:
        middle = int(division_forward(low + high, 2, 0)[0])
        probe = iterate(pair, middle - low, gamma)
        if int(read(probe)[0]) >= 0:
            low, pair = middle, probe
        else:
            high = middle
    return low


# the rotation unit's seed: the phase line's amplitude of the hardware's width's size, 2^63 (the largest
# multiple of Gamma below it, features/phase.seed asking a multiple of Gamma), in Python's integers at load;
# the cosine line then resolves an angle to 2^-63 and the walk's standing Gamma / 2 levels lie far below one
# act's step X theta_0 sin omega_0 at every rest rotation; the hardware's bound the one integer, no number of the law
SEED_SIZE = MAX_WORK_INT + 1


@cache
def rotation_unit(num: int, den: int, gamma: int) -> int:
    """The family's rest rotation to the unit Gamma, K = omega_0 Gamma with cos omega_0 = num / den, computed once from the pair with one rounding as the clock's pace is computed from the content (ALGEBRA.md, The clock family on the Ports: omega_0 Gamma_theta the family's rotation to the unit, Gamma_theta = Gamma), the odd Link part's angle 12 V omega_0 then an integer product with the law's one rounding at the read: found by a bisection on the rotation act and no root (the two hands' word of 2026-10-09, the advisor's (d) and the mathematician's (d): the loader checks an angle by the rotation act's bisection as features/click reads a cosine, no formula in the run and no table): the phase line's pair (features/phase) at the fixed angle theta_0 = 1 / Gamma (D = 2 Gamma^2, K_0 = D - 1, theta_0 within 2.6 x 10^-9 of 1 / Gamma relative) seeded at the amplitude X of the width's size (`SEED_SIZE`, 2^63), a multiple of Gamma, and acted on K times, the cosine line standing at X cos(K theta_0) to the walk's bound; K the largest count in [0, 2 Gamma] at which the cosine line's level is still at or above the pair's cosine, c_K den >= X num (the cosine falling over the half turn, the bisection carrying the pair and acting (middle - low) times per probe, at most 2 Gamma acts in all), then rounded half up to the nearer of K and K + 1 by the two levels' distances to X num, c_K den - X num against X num - c_(K + 1) den; 0 for a massless pair (no rest rotation, no odd part), 5,046 at [4000, 6000] and Gamma 6,000 (arccos(2 / 3) = 0.84107, 5,046.4 to the unit)."""
    amplitude = int(division_forward(SEED_SIZE, gamma, 0)[0]) * gamma
    target = amplitude * num  # c_K den compared against X num, the pair's cosine at the amplitude
    low, high = 0, 2 * gamma  # cos(2) < 0 <= num / den: the crossing lies inside
    pair = seed(amplitude, gamma)
    while high - low > 1:
        middle = int(division_forward(low + high, 2, 0)[0])
        probe = iterate(pair, middle - low, gamma)
        if int(read(probe)[0]) * den >= target:
            low, pair = middle, probe
        else:
            high = middle
    at, following = int(read(pair)[0]), int(read(iterate(pair, 1, gamma))[0])
    return low + int(at * den - target >= target - following * den)
