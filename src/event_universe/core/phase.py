"""The phase circle: scaled cosine and sine of every step, in bounded integers.

Every ray carries a phase that is a step of the world's one circle of N steps
(N a power of two from 2 through 65536; the bound was 4096 until 2026-09-20,
raised by the model owner so that a table at 2N exists for every N a world may
declare up to 32768). The tables give cos and sin of every
step scaled by PHASE_COSINE_SCALE = 256, rounded to the nearest integer, so that
equal phases give exactly one and opposite phases of equal amounts exactly
zero. They are immutable law data, computed once per N from fixed-point series;
no float enters a physical module.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from event_universe.core.integer import checked_work, integer_root

MAX_PHASE_STEPS = 65536
PHASE_COSINE_SCALE = 256
# The Gram matrix of the tables is stored (N^2 entries) for N up to this
# bound; beyond it an entry is formed from the tables where it is read.
GRAM_STORED_STEPS = 512
# pi in fixed point: integer arithmetic only, as every physical module requires.
_PI_FIXED = 3141592654
_FIXED = 1000000000


def _fixed_cosine(angle: int) -> int:
    """cos of a fixed-point angle in [0, pi/2], scaled by _FIXED, by its series."""
    if not 0 <= angle <= _PI_FIXED // 2:
        raise ValueError("phase table angle is outside the first quadrant")
    magnitude, total, sign = _FIXED, 0, 1
    for k in range(2, 66, 2):
        total = checked_work(total + sign * magnitude)
        magnitude = checked_work(magnitude * angle) // _FIXED
        magnitude = checked_work(magnitude * angle) // _FIXED // ((k - 1) * k)
        if not magnitude:
            return total
        sign = -sign
    raise OverflowError("phase table cosine did not converge within its fixed bound")


def _fixed_sine(angle: int) -> int:
    """sin of a fixed-point angle in [0, pi/2], scaled by _FIXED, by its series."""
    if not 0 <= angle <= _PI_FIXED // 2:
        raise ValueError("phase table angle is outside the first quadrant")
    magnitude, total, sign = angle, 0, 1
    for k in range(3, 67, 2):
        total = checked_work(total + sign * magnitude)
        magnitude = checked_work(magnitude * angle) // _FIXED
        magnitude = checked_work(magnitude * angle) // _FIXED // ((k - 1) * k)
        if not magnitude:
            return total
        sign = -sign
    raise OverflowError("phase table sine did not converge within its fixed bound")


@lru_cache(maxsize=4)
def phase_gram(phase_steps: int) -> tuple[tuple[int, ...], ...]:
    """The Gram matrix **G** = **E**^T **E** of the tables (the click without
    amplitudes, 2026-09-21, BEAM_LAW note 37 (xii); the derivations' section
    6.7): **E** is the 2 x N matrix whose rows are the tables C and S, and
    G_jk = C_j C_k + S_j S_k over those rounded entries themselves, never
    the cosine of j - k, so that f^T G f equals |E f|^2 for every integer
    vector **f** by the associativity of integer arithmetic. Symmetric,
    of rank 2, not circulant (the tables' rounding); immutable law data
    built once per N. Stored for N through GRAM_STORED_STEPS; beyond it
    `events.amplitude.Layer.gram_entry` forms an entry from the tables, the
    same integers."""
    if type(phase_steps) is not int or not 2 <= phase_steps <= GRAM_STORED_STEPS:
        raise ValueError(f"the Gram matrix is stored for phase_steps from 2 through {GRAM_STORED_STEPS}")
    cosines, sines = phase_cosines(phase_steps), phase_sines(phase_steps)
    return tuple(
        tuple(checked_work(cosines[j] * cosines[k] + sines[j] * sines[k]) for k in range(phase_steps))
        for j in range(phase_steps)
    )


@lru_cache(maxsize=16)
def phase_sines(phase_steps: int) -> tuple[int, ...]:
    """Scaled sine of every phase step, the companion of phase_cosines."""
    phase_cosines(phase_steps)
    entries = []
    for step in range(phase_steps):
        reduced = step if 2 * step <= phase_steps else phase_steps - step
        angle = checked_work(2 * _PI_FIXED * reduced) // phase_steps
        if 4 * reduced > phase_steps:
            angle = _PI_FIXED - angle
        scaled = checked_work(_fixed_sine(angle) * PHASE_COSINE_SCALE + _FIXED // 2) // _FIXED
        entries.append(scaled if 2 * step <= phase_steps else -scaled)
    return tuple(entries)


@lru_cache(maxsize=16)
def phase_cosines(phase_steps: int) -> tuple[int, ...]:
    """Scaled cosine of every phase difference; immutable law data, computed once.

    cos(2 pi d / P) x 256, rounded to the nearest integer. The only rational
    values on that circle are 0, +-1/2 and +-1, so no entry is a half-integer.
    """
    if type(phase_steps) is not int or not 2 <= phase_steps <= MAX_PHASE_STEPS:
        raise ValueError(f"phase_steps must be between 2 and {MAX_PHASE_STEPS}")
    entries = []
    for difference in range(phase_steps):
        reduced = min(difference, phase_steps - difference)
        angle = checked_work(2 * _PI_FIXED * reduced) // phase_steps
        flip = 4 * reduced > phase_steps
        if flip:
            angle = _PI_FIXED - angle
        cosine = _fixed_cosine(angle)
        scaled = checked_work(cosine * PHASE_COSINE_SCALE + _FIXED // 2) // _FIXED
        entries.append(-scaled if flip else scaled)
    return tuple(entries)


@dataclass(frozen=True)
class PhaseCircle:
    """The world's one circle of N steps, the cyclic group of the phase
    (the integers modulo N: a turn adds, a difference subtracts, the
    opposite phase is half a turn away) with its unit vectors at the scale
    256 (`vector`: (C[phase], S[phase])). Named on 2026-09-21 (the vector
    program, record 191); the operations are the ones every rule of the
    Beam Law performed on the phase, now in one place."""

    steps: int
    cosines: tuple[int, ...]
    sines: tuple[int, ...]

    @property
    def mask(self) -> int:
        """N - 1: the mask of a phase (N a power of two)."""
        return self.steps - 1

    @property
    def half(self) -> int:
        """N / 2: the half turn."""
        return self.steps // 2

    def turn(self, phase: int, by: int) -> int:
        """The phase after a turn of `by` steps (negative steps turn back)."""
        return (phase + by) % self.steps

    def difference(self, phase: int, from_phase: int) -> int:
        """The steps from `from_phase` to `phase` around the circle, 0 .. N - 1."""
        return (phase - from_phase) % self.steps

    def opposite(self, phase: int) -> int:
        """The phase half a turn away (the one that cancels this one)."""
        return (phase + self.half) % self.steps

    def vector(self, phase: int) -> tuple[int, int]:
        """The unit vector of a phase at the scale 256: (cosine, sine)."""
        return self.cosines[phase % self.steps], self.sines[phase % self.steps]


@lru_cache(maxsize=16)
def phase_circle(phase_steps: int) -> PhaseCircle:
    """The circle of N steps with its tables, cached per N."""
    return PhaseCircle(phase_steps, phase_cosines(phase_steps), phase_sines(phase_steps))


def nearest_phase(
    before: int, now: int, amplitude: int, clock: tuple[int, int], phase_steps: int
) -> tuple[int, int] | None:
    """The phase reading of a record at a Node (detector-law-v1, the TABLE
    form; docs/designs/detector_law/declarations/DECLARATIONS.md, the head):
    the angle phi on the circle Z_N nearest to the pair of levels
    (a_before, a_now) = A (cos(phi - k), cos phi) at the record's clock
    [n, d] (n / d steps of Z_N per interval; k the clock's whole step of
    the interval, floor(n / d) or one more as the clock's floor advances)
    and at the record's amplitude A (the third input the declaration
    names: the levels are A x C[phi] / 256 with C the phase table at load,
    so that the two phases sharing one direction of the pair, a small pair
    at a zero crossing and a large one at the peak, are told apart by A),
    read by the table: phi and k the entries minimising the integer
    residual abs(256 now - A C[phi]) + abs(256 before - A C[phi - k]), an
    integer comparison over 2 N entries, no root and no float. Returns
    (phi, the residual), the residual the reading's grain (0 for a pair the
    clock drove at that amplitude: the phase read back exactly), or None
    for the zero pair (no record at the Node)."""
    if before == 0 and now == 0:
        return None
    if phase_steps <= 0 or clock[0] <= 0 or clock[1] <= 0 or amplitude <= 0:
        raise ValueError("nearest_phase needs a positive circle, clock and amplitude")
    table = phase_cosines(phase_steps)
    whole = clock[0] // clock[1]
    steps = (whole % phase_steps, (whole + 1) % phase_steps)
    scaled_now = checked_work(PHASE_COSINE_SCALE * now)
    scaled_before = checked_work(PHASE_COSINE_SCALE * before)
    best: tuple[int, int] | None = None
    for phi in range(phase_steps):
        residual_now = abs(scaled_now - checked_work(amplitude * table[phi]))
        for step in steps:
            residual = residual_now + abs(
                scaled_before - checked_work(amplitude * table[(phi - step) % phase_steps])
            )
            if best is None or residual < best[1]:
                best = (phi, residual)
    return best


def remnant_intervals(
    extent: int, pair: tuple[int, int], clock: tuple[int, int], phase_steps: int
) -> int:
    """The intervals after its train before an emitter takes its own record's
    remnant (DECLARATIONS.md section 10 item 10, the rule): T = ceil(extent /
    v_g) + 2, the extent the emitter's span along its emission in Links and
    v_g the record's kind's band group pace at its declared clock. The band
    of the six-neighbour rule with the kind's pair [num, den] along an axis,
    cos omega = (num / den) (cos k + 2) / 3, gives v_g = d omega / d k =
    (num / den) sin k / (3 sin omega), so extent / v_g = 3 extent sin omega
    den / (num sin k). Computed once at load in the tables' fixed point (the
    series above, the integer root; no float), a declared rounding like the
    tables': 24 for a block of side 12 emitting light at the clock [77, 25]
    on N = 64, 4 for a one-Node lamp. A clock outside the kind's band, or
    beyond a quarter turn per interval, is refused."""
    num, den = pair
    clock_numerator, clock_denominator = clock
    if extent < 1 or num < 1 or den < 1 or clock_numerator < 1 or clock_denominator < 1:
        raise ValueError("remnant intervals need a positive extent, pair and clock")
    angle = checked_work(2 * _PI_FIXED * clock_numerator) // (clock_denominator * phase_steps)
    if not 0 < angle <= _PI_FIXED // 2:
        raise ValueError("the clock's step per interval lies outside (0, pi / 2]")
    cosine = _fixed_cosine(angle)
    sine = _fixed_sine(angle)
    band_cosine = checked_work(3 * den * cosine) // num - 2 * _FIXED
    if not -_FIXED < band_cosine < _FIXED:
        raise ValueError("the clock lies outside the kind's band (no group pace)")
    band_sine = integer_root(checked_work(_FIXED * _FIXED - band_cosine * band_cosine))
    numerator = checked_work(3 * extent * sine * den)
    denominator = checked_work(num * band_sine)
    return (numerator + denominator - 1) // denominator + 2
