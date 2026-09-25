"""The margin rule of the massive record kind (`massive-record-v1`,
docs/designs/detector_law/MASSIVE_RECORD.md section 11 item 4, Reviewer 3's
two lines; the build's plan BUILD.md section 0, FINDING 1): a load-time
check of a world's blocks, made before the world runs, in a HOST module
outside the engine's integer path.

The block's bound mode in the massive medium: the rule of section 1 with
the kind's pair `[num, den]` on every Node and the block's lowered pair on
its Nodes has the characters `2 cos omega D a = (S_6 / 3) a`, D = den /
num per Node (the six-neighbour sum with the world's faces, the row itself
twice on an axis of one layer, as the engine reads it); the bound mode is
the largest eigenvalue `lambda = 2 cos omega_b` of the symmetric operator
`A = D^-1/2 (S_6 / 3) D^-1/2`, found by a Lanczos iteration (the largest
Ritz value of the three-term recurrence, converged to 1e-9). Then, with
D_out the kind's own ratio, `cosh kappa = 3 D_out cos omega_b - 2` and the
mode's extent in the medium is `1 / kappa` Links (the tail exp(-kappa x)),
its binding depth `eps = 1 - omega_b^2 / omega_0^2` with `cos omega_0 =
num / den`. A mode at or above the gap (lambda / 2 <= num / den) is not
bound and the block is refused. THE RULE: a CONTROL world's Nodes lie at
least ONE extent from any non-periodic face of the kind and a periodic
axis's side is at least the block's side plus TWO extents; a PIN world's
Nodes lie at least TWO extents from a non-periodic face and a periodic side
is at least the side plus FOUR extents (a hard face at distance d shifts
the mode by about eps e^(-2 kappa d)); a declaration below the margin is
refused naming the block, the axis, the extent and the distance. Every
number here is a COMPUTATION from the declaration, printed before the run
and written into the run's record; the state never reads it (the
transcendental of the pair is no verb of the law). This is the method of
the design's `massive_board_margin.py` on the world's own board and faces
(the design's table was computed on 96^3 and 128^3 boxes; a periodic image
shifts omega_b, so the world's own number is the pin's).
"""

from __future__ import annotations

import dataclasses
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh  # type: ignore[import-untyped]

from event_universe.events.world import BEAM_LAW, MARGIN_KINDS, NatureBeamWorld, body_node_indices

# The ramp of a pushed body at least this many relaxation times 1 / (omega_0
# - omega_b) of its own well (DECLARATIONS.md section 8, the rule for any
# pushed block; the layer pin world's ten).
RELAXATION_TIMES = 10

RITZ_TOLERANCE = 1e-9
MOST_ITERATIONS = 2000
# The margins per kind of world (extents): the distance to a non-periodic
# face, and the extents added to the side on a periodic axis.
FACE_EXTENTS = {MARGIN_KINDS[0]: 2.0, MARGIN_KINDS[1]: 1.0}
SIDE_EXTENTS = {MARGIN_KINDS[0]: 4.0, MARGIN_KINDS[1]: 2.0}


@dataclass(frozen=True)
class MarginReading:
    """One block's mode and margin: the frequencies, the binding depth, the
    decay rate and the extent (COMPUTATION), the margin's kind, and per
    axis the distance the rule compares (to the nearer non-periodic face,
    or the periodic side's room beyond the block) with what it needs."""

    number: int
    family: str
    side: int
    kind: str
    lambda_max: float
    omega_b: float
    omega_0: float
    eps: float
    kappa: float
    extent: float
    iterations: int
    axes: tuple[tuple[str, bool, float, float], ...]

    @property
    def bound(self) -> bool:
        return self.kappa > 0.0

    @property
    def runaway(self) -> bool:
        """The largest eigenvalue at or above 2: the well's mode is no
        oscillation (2 cos omega_b = lambda has no omega_b) but a level
        that grows by lambda / 2 + sqrt(lambda^2 / 4 - 1) per interval
        (a well too deep for its board: on a chain or a layer the folded
        axes' self-reads count fully, so a one-Node well runs away at a
        depth that binds on a cube; BUILD.md section 26)."""
        return self.lambda_max >= 2.0

    def lines(self) -> list[str]:
        """The reading printed, one line per fact, labelled COMPUTATION."""
        found = [
            f"margin (COMPUTATION): block {self.number} ({self.family}, side {self.side}, a "
            f"{self.kind} world): 2 cos omega_b = {self.lambda_max:.6f}, omega_b = {self.omega_b:.5f}, "
            f"omega_0 = {self.omega_0:.5f}, eps = {self.eps:.4f}, kappa = {self.kappa:.5f}, the extent "
            f"1 / kappa = {self.extent:.2f} Links ({self.iterations} Lanczos iterations)"
        ]
        for axis, periodic, have, need in self.axes:
            found.append(
                f"margin (COMPUTATION): block {self.number} axis {axis}: "
                + (
                    f"periodic, the side {have:.0f} against the block's side plus "
                    f"{SIDE_EXTENTS[self.kind]:.0f} extents = {need:.1f}"
                    if periodic
                    else f"a zero face at {have:.0f} Links against {FACE_EXTENTS[self.kind]:.0f} "
                    f"extents = {need:.1f}"
                )
            )
        return found

    def to_record(self) -> dict[str, object]:
        """The reading as `run.json` records it; a folded axis (a periodic
        extent below the block's side, a layer or a chain) has no row."""
        return {
            "measured": self.number,
            "family": self.family,
            "side": self.side,
            "margin": self.kind,
            "lambda_max": self.lambda_max,
            "omega_b": self.omega_b,
            "omega_0": self.omega_0,
            "eps": self.eps,
            "kappa": self.kappa,
            "extent": self.extent,
            "iterations": self.iterations,
            "axes": [
                {"axis": axis, "periodic": periodic, "have": have, "need": need}
                for axis, periodic, have, need in self.axes
            ],
            "kind": "COMPUTATION",
        }


def body_node_mask(
    shape: tuple[int, int, int],
    corner: tuple[int, int, int],
    side: int | tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
) -> np.ndarray:
    """The block's Nodes as a mask over the board: the array form of the
    loader's `body_node_indices` (the one copy of the box's rule; a cube's
    side or the box's extents)."""
    mask = np.zeros(shape, dtype=bool)
    mask.ravel()[body_node_indices(shape, corner, side, wrap)] = True
    return mask


def six_neighbours(a: np.ndarray, wrap: tuple[bool, bool, bool]) -> np.ndarray:
    """The six-neighbour sum as the engine reads it: the wrap on a periodic
    axis, 0 beyond a zero face, the row itself twice on an axis of one
    layer."""
    total = np.zeros_like(a)
    for axis in range(3):
        if a.shape[axis] == 1:
            total += 2 * a
            continue
        for sign in (1, -1):
            if wrap[axis]:
                total += np.roll(a, sign, axis=axis)
            else:
                shifted = np.zeros_like(a)
                lower = [slice(None)] * 3
                upper = [slice(None)] * 3
                if sign > 0:
                    lower[axis] = slice(1, None)
                    upper[axis] = slice(None, -1)
                else:
                    lower[axis] = slice(None, -1)
                    upper[axis] = slice(1, None)
                shifted[tuple(lower)] = a[tuple(upper)]
                total += shifted
    return total


def largest_eigenvalue(
    ratio: np.ndarray, wrap: tuple[bool, bool, bool], seed: np.ndarray
) -> tuple[float, int]:
    """The largest eigenvalue of A = D^-1/2 (S_6 / 3) D^-1/2 (D = `ratio`,
    den / num per Node) by the three-term Lanczos recurrence started from
    `seed`, the largest Ritz value converged to RITZ_TOLERANCE."""
    ritz, iterations, _ = lanczos(ratio, wrap, seed, vector=False)
    return ritz, iterations


def lanczos(
    ratio: np.ndarray, wrap: tuple[bool, bool, bool], seed: np.ndarray, vector: bool
) -> tuple[float, int, np.ndarray | None]:
    """The three-term Lanczos recurrence on A = D^-1/2 (S_6 / 3) D^-1/2 from
    `seed`: the largest Ritz value, the iterations, and with `vector` the
    Ritz vector of the mode (the bound mode's shape, D^-1/2 undone) by a
    second pass of the same recurrence accumulating the tridiagonal's
    eigenvector over the Lanczos basis (nothing of the basis is stored:
    the pass is deterministic and the memory one vector)."""
    scale = 1.0 / np.sqrt(ratio)

    def apply(vector_in: np.ndarray) -> np.ndarray:
        result: np.ndarray = scale * six_neighbours(scale * vector_in, wrap) / 3.0
        return result

    def recurrence(weights: np.ndarray | None) -> tuple[list[float], list[float], np.ndarray | None]:
        q = seed.astype(np.float64)
        q /= np.linalg.norm(q)
        previous = np.zeros_like(q)
        beta = 0.0
        alphas: list[float] = []
        betas: list[float] = []
        ritz_before = None
        total = np.zeros_like(q) if weights is not None else None
        for iteration in range(1, MOST_ITERATIONS + 1):
            if total is not None and weights is not None:
                if iteration > len(weights):
                    break
                total += weights[iteration - 1] * q
            w = apply(q) - beta * previous
            alpha = float(np.vdot(q, w))
            w -= alpha * q
            alphas.append(alpha)
            beta = float(np.linalg.norm(w))
            if weights is None and iteration >= 3:
                tridiagonal = np.diag(alphas) + np.diag(betas, 1) + np.diag(betas, -1)
                ritz = float(np.linalg.eigvalsh(tridiagonal)[-1])
                if ritz_before is not None and abs(ritz - ritz_before) < RITZ_TOLERANCE:
                    break
                ritz_before = ritz
            if beta < 1e-14:
                break
            betas.append(beta)
            previous, q = q, w / beta
        return alphas, betas, total

    alphas, betas, _ = recurrence(None)
    count = len(alphas)
    tridiagonal = np.diag(alphas) + np.diag(betas[: count - 1], 1) + np.diag(betas[: count - 1], -1)
    values, vectors = np.linalg.eigh(tridiagonal)
    ritz = float(values[-1])
    if not vector:
        return ritz, count, None
    _, _, total = recurrence(vectors[:, -1])
    assert total is not None
    # the mode of the rule's operator itself: A's vector scaled by D^-1/2
    mode: np.ndarray = scale * total
    mode /= np.max(np.abs(mode))
    if mode[np.unravel_index(int(np.argmax(np.abs(mode))), mode.shape)] < 0:
        mode = -mode
    return ritz, count, mode


def accurate_mode(world: NatureBeamWorld, number: int) -> tuple[float, np.ndarray]:
    """The bound mode of a block alone in its medium on the world's own
    board, to the host's floating precision: the largest eigenpair of the
    symmetric operator A = D^-1/2 (S_6 / 3) D^-1/2 (D = den / num per Node)
    by the implicitly restarted Lanczos method (ARPACK through scipy's
    `eigsh`, the tolerance the machine's, the start the Nodes' indicator
    plus a flat 10^-3), the eigenvalue 2 cos omega_b and the mode of the
    rule's operator (A's vector times D^-1/2, its largest entry 1). A HOST
    computation of the generator and of the diagnostics, never of the
    engine's run; the loader reads its rounded integers alone and checks
    them in integers (ALGEBRA.md 9.22 (7)). The three-term recurrence of
    `lanczos` (no reorthogonalisation) gave the mode to about 3 x 10^-4
    relative, hundreds of units at the amplitude 50 x 2^20, which the
    integer check refuses (BUILD.md section 26 item 20)."""
    entry = world.measured[number]
    definition = entry.block
    if definition is None:
        raise ValueError(f"{BEAM_LAW}: measured[{number}] is no block")
    family = world.families[entry.family]
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    wrap = world.kind_periodic(entry.family)
    corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
    nodes = body_node_mask(shape, corner, definition.extents, wrap)
    ratio = np.where(nodes, definition.pair[1] / definition.pair[0], family.pair[1] / family.pair[0])
    scale = 1.0 / np.sqrt(ratio)
    count = int(np.prod(shape))

    def apply(flat: np.ndarray) -> np.ndarray:
        result: np.ndarray = scale * six_neighbours(scale * flat.reshape(shape), wrap) / 3.0
        return result.ravel()

    operator = LinearOperator((count, count), matvec=apply, dtype=np.float64)
    start = (np.where(nodes, 1.0, 0.0) + 1e-3).ravel()
    values, vectors = eigsh(operator, k=1, which="LA", v0=start, tol=0, maxiter=100 * count)
    mode: np.ndarray = scale * vectors[:, 0].reshape(shape)
    mode /= np.max(np.abs(mode))
    if mode[np.unravel_index(int(np.argmax(np.abs(mode))), mode.shape)] < 0:
        mode = -mode
    return float(values[0]), mode


def _operator_step(
    levels: np.ndarray,
    remainder: np.ndarray,
    num: np.ndarray,
    den: np.ndarray,
    wrap: tuple[bool, bool, bool],
    amplitude: int,
) -> tuple[np.ndarray, np.ndarray]:
    """One step of the board's own operator in the law's integers, 3 den v' =
    num S_6(v) + 6 den v + r with the remainder r carried from step to step
    (the one copy of the generator's step; ALGEBRA.md 9.22 (7)): returns
    the levels and the remainder after the step. When the levels pass twice the amplitude they are renormalised by an
    exact shift by a power of two, the remainder shifted with them (the
    value v + r / wall halved k times is (v >> k) + ((v mod 2^k) wall + r)
    / (wall 2^k), whose remainder against the same wall is the floor of
    ((v mod 2^k) wall + r) / 2^k: nothing of the fraction is dropped but
    the last bits below the wall)."""
    wall = 3 * den.astype(np.int64)
    total = num.astype(np.int64) * six_neighbours(levels, wrap).astype(np.int64) + remainder
    total += 6 * den.astype(np.int64) * levels
    levels = np.floor_divide(total, wall)
    remainder = total - wall * levels
    largest = int(np.max(np.abs(levels)))
    if largest >= 2 * amplitude:
        shift = largest.bit_length() - int(amplitude).bit_length()
        shifted = np.right_shift(levels, shift)
        low = levels - np.left_shift(shifted, shift)
        remainder = np.right_shift(low * wall + remainder, shift)
        levels = shifted
    return levels, remainder


def integer_mode_iteration(
    start: np.ndarray,
    num: np.ndarray,
    den: np.ndarray,
    wrap: tuple[bool, bool, bool],
    amplitude: int,
    iterations: int,
) -> np.ndarray:
    """The board's own operator iterated a FIXED number of times from
    `start` (a diagnostic of the generator's convergence, `_operator_step`
    repeated; the generator itself stops by the rule of `iterated_mode`):
    from any start the power iteration v -> (M + 2 I) v converges to the
    bound mode (Perron-Frobenius on the nonnegative shifted operator) at
    the rate 1 - gap / (lambda + 2) per iteration. Reproducible bit for bit
    on every host; the cost one board step per iteration. Returns the
    levels after `iterations`, their largest magnitude in [amplitude, 2
    amplitude)."""
    levels = start.astype(np.int64).copy()
    remainder = np.zeros_like(levels)
    for _ in range(iterations):
        levels, remainder = _operator_step(levels, remainder, num, den, wrap, amplitude)
    return levels


WORKING_AMPLITUDE = (
    1 << 28
)  # the generator's least working amplitude (`iterated_mode`); 2^20 left the muon layer's well hovering at 1.5 times the loader's bound


def clock_denominator(amplitude: int) -> int:
    """The clock's denominator b for a profile at `amplitude` (ALGEBRA.md 9.22
    (7)): a power of two at least twice the amplitude and at least 2^20 (so
    that a shallow mode's binding above the band's top is resolved)."""
    return max(1 << (int(amplitude).bit_length() + 1), 1 << 20)


def iterated_mode(
    world: NatureBeamWorld, number: int, amplitude: int, limit: int = 1 << 20
) -> tuple[list[int], tuple[int, int], int]:
    """THE GENERATOR: THE BOARD'S OWN OPERATOR ITERATED IN INTEGERS, WITH THE
    STOP (the model owner's word of 2026-09-25, 04:10Z, closing record 1898:
    "the iterated operator becomes the generator itself, with the stop").
    The block alone in its medium on the world's own board (the family's
    pair everywhere, the block's pair on its Nodes), from the Nodes'
    indicator at `amplitude`: every iteration is one step of the operator
    (`_operator_step`), the levels are scaled to the amplitude at the peak,
    and the clock a / b is read from the scaled profile p as the operator's
    quotient over the whole board, a = round(b SUM_i p_i num_i (S_6 p)_i /
    SUM_i 3 den_i p_i^2) with b = `clock_denominator` (exact for the mode,
    second order in the rounding, every Node weighing in; the growth at the
    peak Node alone was READ AND REJECTED: its remainder's noise at a small
    amplitude, 4096, moves the read by more than a shallow well's binding
    above the band's top); THE STOP is the first iteration at which the
    scaled profile with that clock passes the loader's own residual bound
    (`mode_residual`: |b num_i (S_6 p)_i - 3 den_i a p_i| <= b (3 num_i + 6
    den_i) at every Node, ALGEBRA.md 9.22 (7)): the next step changes the
    board no more than the rounding floor, the board only rotating (a float
    reading of the residual filters the iterations first; the verdict is
    the loader's integer check alone). THE WORKING AMPLITUDE: the
    iteration runs at 2^28 or the declared amplitude, whichever is larger
    (`WORKING_AMPLITUDE`), and the profile checked and written is its
    rounding at the declared amplitude: the loader's bound is the bound
    for one rounding of an exact mode, while the iteration's own noise (a
    unit per Node per step through the six reads) must sit below it, which
    it does only when the working amplitude is large against the bound's
    1.5 / p relative width (a side-4 well of [850, 800] on the 24-cube at
    4096 hovered at 1.2 to 1.7 times the bound for ever and stopped at
    2^20; the muon layer's well [3200, 3227] of side 14 on the 200 x 200
    layer hovered at 1.5 times the bound at 2^20 for 2^20 iterations and
    stops at 36694 iterations at 2^28, the working amplitude
    since the names' regeneration of 2026-09-25, COMPUTATION). A HOST
    computation of the generator, reproducible bit for bit (the same
    integers in, the same out); the loader reads the written integers alone
    and checks them again. Returns the profile (x-major over the board),
    the clock [a, b] and the iterations taken; past `limit` iterations
    without the stop it raises, naming the last residual against the
    bound (a generator fault or the iteration's floor, never a bound
    moved)."""
    from event_universe.events.world import mode_residual

    entry = world.measured[number]
    definition = entry.block
    if definition is None:
        raise ValueError(f"{BEAM_LAW}: measured[{number}] is no block")
    family = world.families[entry.family]
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    wrap = world.kind_periodic(entry.family)
    corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
    nodes = body_node_mask(shape, corner, definition.extents, wrap)
    num = np.where(nodes, definition.pair[0], family.pair[0]).astype(np.int64)
    den = np.where(nodes, definition.pair[1], family.pair[1]).astype(np.int64)
    num_flat = [int(value) for value in num.ravel()]
    den_flat = [int(value) for value in den.ravel()]
    b = clock_denominator(amplitude)
    working = max(amplitude, WORKING_AMPLITUDE)
    levels = np.where(nodes, working, 0).astype(np.int64)
    remainder = np.zeros_like(levels)
    residual = bound = 0
    # the loader's bound per Node and the operator's integers as floats for the
    # quick filter below (a filter, never the verdict)
    num_float = num.astype(np.float64)
    den_float = den.astype(np.float64)
    bound_float = float(b) * (3.0 * num_float + 6.0 * den_float)
    for iteration in range(1, limit + 1):
        levels, remainder = _operator_step(levels, remainder, num, den, wrap, working)
        largest = int(np.max(np.abs(levels)))
        scaled = np.floor_divide(2 * levels * amplitude + largest, 2 * largest)
        six = six_neighbours(scaled, wrap)
        profile_float = scaled.astype(np.float64)
        six_float = six.astype(np.float64)
        quotient = float(np.sum(profile_float * num_float * six_float)) / float(
            np.sum(3.0 * den_float * profile_float * profile_float)
        )
        reading = np.abs(
            float(b) * num_float * six_float - 3.0 * den_float * (b * quotient) * profile_float
        )
        if not bool(np.all(reading <= bound_float * (1.0 + 1e-9))):
            continue
        # the exact integers: the clock as the quotient over the board, then the
        # loader's own check
        flat = [int(value) for value in scaled.ravel()]
        six_flat = [int(value) for value in six.ravel()]
        numerator = sum(p * n * s for p, n, s in zip(flat, num_flat, six_flat, strict=True))
        denominator = sum(3 * d * p * p for p, d in zip(flat, den_flat, strict=True))
        a = (2 * b * numerator + denominator) // (2 * denominator)
        residual, bound, _ = mode_residual(flat, num_flat, den_flat, (a, b), shape, wrap)
        if residual <= bound:
            return flat, (a, b), iteration
    raise ValueError(
        f"{BEAM_LAW}: the generator's iteration for measured[{number}] did not stop within "
        f"{limit} iterations: the last residual {residual} against the bound {bound} (the "
        f"amplitude {amplitude}; the iteration's floor or a generator fault; nothing written)"
    )


def bound_mode(world: NatureBeamWorld, number: int) -> np.ndarray:
    """The bound mode's shape of a block on the world's own board (its
    largest entry 1), over the whole board: the seed a pin world declares as
    integers at its amplitude (MASSIVE_RECORD.md section 11 item 7, the
    reader of record and the seed; a HOST computation of the generator,
    never of the engine's run); `accurate_mode`'s vector."""
    return accurate_mode(world, number)[1]


def profile_check(world: NatureBeamWorld, number: int) -> tuple[int, int] | None:
    """A GAMEBOARD diagnostic at load of a block seeded with an integer
    profile: the largest deviation, in units, of the file's integers from
    the eigensolver's mode at the file's amplitude, with that amplitude;
    None for a flat seed (a comparison printed, never read by the state;
    the generator's iterated profile sits within its floor, about 1 / gap
    units, of the eigensolver's; the law's check is the loader's residual
    bound)."""
    definition = world.measured[number].block
    if definition is None or definition.profile is None:
        return None
    profile = np.array(definition.profile, dtype=np.int64).reshape(world.shape)
    amplitude = int(np.max(np.abs(profile)))
    mode = bound_mode(world, number)
    expected = np.rint(mode * amplitude).astype(np.int64)
    deviation = int(np.max(np.abs(expected - profile)))
    return deviation, amplitude


def block_margin(world: NatureBeamWorld, number: int) -> MarginReading:
    """The reading of one block: its mode on the world's own board with its
    world's faces, alone in the medium (the other blocks' wells not carried:
    each block is checked on its own)."""
    entry = world.measured[number]
    definition = entry.block
    if definition is None:
        raise ValueError(f"{BEAM_LAW}: measured[{number}] is no block")
    family = world.families[entry.family]
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    wrap = world.kind_periodic(entry.family)
    corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
    nodes = body_node_mask(shape, corner, definition.extents, wrap)
    ratio_out = family.pair[1] / family.pair[0]
    ratio_in = definition.pair[1] / definition.pair[0]
    ratio = np.where(nodes, ratio_in, ratio_out)
    seed = np.where(nodes, 1.0, 0.0) + 1e-3 * np.random.default_rng(0).standard_normal(shape)
    lambda_max, iterations = largest_eigenvalue(ratio, wrap, seed)
    omega_0 = math.acos(min(1.0, family.pair[0] / family.pair[1]))
    cosine = lambda_max / 2.0
    omega_b = math.acos(max(-1.0, min(1.0, cosine)))
    eps = 1.0 - (omega_b / omega_0) ** 2 if omega_0 > 0 else 0.0
    argument = 3.0 * ratio_out * cosine - 2.0
    kappa = math.acosh(argument) if argument > 1.0 else 0.0
    extent = 1.0 / kappa if kappa > 0.0 else math.inf
    axes = []
    for axis, name in enumerate(("x", "y", "z")):
        side = definition.extents[axis]
        if wrap[axis] and shape[axis] <= side:
            # A FOLDED axis (a layer or a chain, MASSIVE_RECORD.md section 11
            # item 7: the block wraps onto itself and the rule reads the
            # Node itself across it, a_U = a_D = a_now): no face, no tail,
            # nothing for the rule to compare on that axis. A body whose side
            # equals the axis's extent spans it the same way (an emitter body
            # of side 1 on a chain or a layer, BUILD.md section 26).
            continue
        if wrap[axis]:
            have = float(shape[axis])
            need = side + SIDE_EXTENTS[definition.margin] * extent
        else:
            have = float(min(corner[axis], shape[axis] - corner[axis] - side))
            need = FACE_EXTENTS[definition.margin] * extent
        axes.append((name, wrap[axis], have, need))
    return MarginReading(
        number,
        family.name,
        definition.side,
        definition.margin,
        lambda_max,
        omega_b,
        omega_0,
        eps,
        kappa,
        extent,
        iterations,
        tuple(axes),
    )


def check_margins(world: NatureBeamWorld) -> list[MarginReading]:
    """Every block's reading; a block whose mode is not bound, or whose
    margin is below the rule, refuses the world naming the block, the axis,
    the extent and the distance. Called before a world runs."""
    found = []
    for number, entry in enumerate(world.measured):
        if entry.block is None or not world.families[entry.family].massive_kind:
            continue
        if entry.block.seed == 0:
            # A silent block (seed 0, no own record) holds nothing to bind: a
            # take line (an absorbing block with the kind's own pair, item 6b)
            # takes at its Nodes and carries no mode, so the threshold and
            # the extent have no record to read.
            continue
        kind = world.families[entry.family].pair
        if entry.block.pair[0] * kind[1] < entry.block.pair[1] * kind[0]:
            # A barrier (a raised pair, the matter wall of DECLARATIONS.md
            # section 15 M1-6) binds nothing: no mode, no margin.
            continue
        reading = block_margin(world, number)
        found.append(reading)
        if reading.runaway:
            raise ValueError(
                f"{BEAM_LAW}: measured[{number}]: the block's mode is a runaway (2 cos omega_b = "
                f"{reading.lambda_max:.6f} at or above 2: no oscillation, a level growing by "
                f"{reading.lambda_max / 2 + math.sqrt(reading.lambda_max**2 / 4 - 1):.4f} per "
                "interval; the well is too deep for its board, the folded axes' self-reads "
                "counting fully on a chain or a layer; BUILD.md section 26)"
            )
        if not reading.bound:
            raise ValueError(
                f"{BEAM_LAW}: measured[{number}]: the block's mode is not bound (2 cos omega_b = "
                f"{reading.lambda_max:.6f} at or below the gap's 2 num / den = "
                f"{2 * world.families[entry.family].pair[0] / world.families[entry.family].pair[1]:.6f}; "
                "the well is too shallow or the side too small for its pair, MASSIVE_RECORD.md "
                "section 4's threshold table)"
            )
        for axis, periodic, have, need in reading.axes:
            if have < need:
                raise ValueError(
                    f"{BEAM_LAW}: measured[{number}]: below the margin rule on {axis} for a "
                    f"{reading.kind} world (the mode's extent {reading.extent:.2f} Links): "
                    + (
                        f"the periodic side {have:.0f} is less than the block's side "
                        f"{reading.side} plus {SIDE_EXTENTS[reading.kind]:.0f} extents = {need:.1f}"
                        if periodic
                        else f"the Nodes lie {have:.0f} Links from a zero face, less than "
                        f"{FACE_EXTENTS[reading.kind]:.0f} extents = {need:.1f}"
                    )
                )
    return found


def relaxation_time(reading: MarginReading) -> float:
    """The mode's relaxation time 1 / (omega_0 - omega_b) in intervals
    (DECLARATIONS.md section 8; COMPUTATION)."""
    return 1.0 / (reading.omega_0 - reading.omega_b)


def period_of(reading: MarginReading) -> int:
    """The period P of the body's mode in intervals, the nearest integer to
    2 pi / omega_b (ALGEBRA.md 9.17 (5) item 1; COMPUTATION from the
    module's own omega_b); at least 1."""
    if reading.omega_b <= 0.0:
        return 1
    return max(1, int(round(2.0 * math.pi / reading.omega_b)))


def excitation_norm(world: NatureBeamWorld, number: int, period: int) -> int:
    """The excited record's norm T, one period's action P e_c (ALGEBRA.md
    9.17 (7) (e) and (f) in the flux's units of 9.19 (3)): the share e_c of
    the record's conserved form at the body's centre Node, summed over
    `period` intervals of its own mode advanced ALONE (the body on its board
    with no other measured event, no set and no emitter, the rule exact on
    integers; constant for the exact mode, wobbling with the seed's
    rounding transient), times the centre Node's pace (the body's own units,
    item 36). The generator writes it as the emitter's `norm`, under the
    input stamp (a HOST computation, not the law; the count of intervals
    reads no norm since item 33)."""
    from event_universe.events.detector_law import DetectorLawSimulation

    entry = world.measured[number]
    definition = entry.block
    if definition is None:
        raise ValueError(f"{BEAM_LAW}: measured[{number}] is no block")
    alone = dataclasses.replace(
        world,
        measured=(
            dataclasses.replace(
                entry, block=dataclasses.replace(definition, emitter=None, receiver=None)
            ),
        ),
        detectors=(),
    )
    simulation = DetectorLawSimulation(alone)
    block = simulation.blocks[0]
    total = Fraction(0)
    for _ in range(period):
        simulation.step()
        own = block.own
        assert own is not None
        total += simulation.form_share(own, simulation.centre_mask(block))
    # THE BODY'S OWN UNITS (ALGEBRA.md 9.50 (13); BUILD.md section 26 item 36):
    # the share at the centre Node is read in the world's time by the Node's
    # pace p = Gamma - c there (an exact rational); p times it is whole, the
    # norm as the body's own record carries it
    centre = tuple(int(axis[0]) for axis in np.nonzero(simulation.centre_mask(block)))
    pace = simulation.node_clock_pair(centre, block.family)[0]
    norm = total * pace
    assert norm.denominator == 1, (norm, pace)
    return int(norm)


def composed_largest_eigenvalues(world: NatureBeamWorld) -> dict[int, float]:
    """The largest eigenvalue of the COMPOSED operator of each massive family
    (ALGEBRA.md 9.19 (2)): every body's well of the family in one read
    matrix on the world's faces; the stability condition is read on it,
    below 2, refused at or above (a runaway mode of the whole board)."""
    found: dict[int, float] = {}
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    for index, family in enumerate(world.families):
        if not family.massive_kind:
            continue
        ratio = np.full(shape, family.pair[1] / family.pair[0])
        seed = 1e-3 * np.random.default_rng(0).standard_normal(shape)
        bodies = False
        for entry in world.measured:
            definition = entry.block
            if definition is None or entry.family != index or definition.seed == 0:
                continue
            corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
            nodes = body_node_mask(shape, corner, definition.extents, world.kind_periodic(index))
            ratio = np.where(nodes, definition.pair[1] / definition.pair[0], ratio)
            seed = seed + np.where(nodes, 1.0, 0.0)
            bodies = True
        if not bodies:
            continue
        found[index], _ = largest_eigenvalue(ratio, world.kind_periodic(index), seed)
    return found


def check_body_conditions(
    world: NatureBeamWorld, simulation: Any, readings: list[MarginReading]
) -> list[str]:
    """The body's algebraic conditions exact in the initial state, checked at
    load (the model owner's word of 2026-09-24, 16:48Z, through the Boss;
    SIMULATOR_DEFINITIONS.md, the four building blocks, the body's
    conditions 5 and 7; conditions 1, 2 and 6 are the loader's own refusals,
    3 and 4 `check_margins`): for every body the margin rule read (a bound
    body of a massive kind with its own record), (a) THE SEED ON THE MODE:
    the bound mode's integer profile over the whole board is recomputed
    from the declared pair, shape and amplitude (`bound_mode`, the module's
    own Lanczos vector, rounded at the largest magnitude of the declared
    seed) and compared with the simulation's initial state of the body's
    own record at both levels, `now` and `before`, bit for bit; the first
    Node that differs refuses the world, named with the two values
    (ALGEBRA.md 8.7, the standing start exact); (b) THE RAMP: a body with a
    momentum declares `ramp` at least RELAXATION_TIMES times 1 / (omega_0 -
    omega_b) of its own well, or is refused naming the ramp and the
    relaxation time. `simulation` is the world's `DetectorLawSimulation`
    before its first interval (its `block_by_number`); nothing here is read
    by the state: a HOST check at load, the lines returned are printed as
    COMPUTATION."""
    lines: list[str] = []
    blocks = simulation.block_by_number
    for index, largest in composed_largest_eigenvalues(world).items():
        if largest >= 2.0:
            raise ValueError(
                f"{BEAM_LAW}: the family {world.families[index].name!r}: the composed operator's "
                f"largest eigenvalue {largest:.6f} is at or above 2 (ALGEBRA.md 9.19 (2): a mode of "
                "the whole board grows without bound; the bodies' wells together are too deep for "
                "the board)"
            )
        lines.append(
            f"operator (COMPUTATION): the family {world.families[index].name!r}: the composed "
            f"operator's largest eigenvalue 2 cos omega = {largest:.6f}, below 2"
        )
    for reading in readings:
        number = reading.number
        entry = world.measured[number]
        definition = entry.block
        assert definition is not None
        own = blocks[number].own
        if own is None:
            raise ValueError(
                f"{BEAM_LAW}: measured[{number}]: a bound body without its own record at load"
            )
        amplitude = int(definition.seed)
        if definition.profile is None:
            raise ValueError(
                f"{BEAM_LAW}: measured[{number}]: a bound body declares its seed as the "
                "generator's profile (the operator iterated with the stop, `mode_profile` of the "
                "massive record generator); a flat scalar seed is no mode"
            )
        # the initial state is the file's profile at both levels, bit for bit; that
        # the profile IS the mode within the rounding is the loader's own residual
        # check (record 1886), made before this
        expected = np.array(definition.profile, dtype=np.int64).reshape(world.shape)
        for level_name, level in (("now", own.now), ("before", own.before)):
            found = np.asarray(level, dtype=np.int64)
            differing = np.nonzero(found != expected)
            if differing[0].size:
                x, y, z = (int(differing[axis][0]) for axis in range(3))
                raise ValueError(
                    f"{BEAM_LAW}: measured[{number}]: the body's initial state is not the file's "
                    f"profile at the amplitude {amplitude}: at the Node ({x}, {y}, {z}) the level "
                    f"`{level_name}` holds {int(found[x, y, z])} where the profile gives "
                    f"{int(expected[x, y, z])} ({int(differing[0].size)} Nodes differ; ALGEBRA.md "
                    "8.7: the standing start exact; the model owner's word of 2026-09-24, 16:48Z)"
                )
        lines.append(
            f"seed (COMPUTATION): block {number}: the initial state is the file's profile at the "
            f"amplitude {amplitude} at both levels, bit for bit "
            f"({int(np.count_nonzero(expected))} Nodes nonzero; the profile the mode within the "
            "loader's residual bound, record 1886)"
        )
        emitter = definition.emitter
        if emitter is not None:
            # (c) THE EXCITED RECORD'S NORM (ALGEBRA.md 9.17 (5) item 1, 9.19
            # (3)): the emitter's `period` and `norm` are the generator's
            # integers; the norm is recomputed here by advancing the seed
            # alone and a mismatch refuses the world; the period is printed
            # against the module's 2 pi / omega_b (COMPUTATION)
            if emitter.period is None or emitter.norm is None:
                raise ValueError(
                    f"{BEAM_LAW}: measured[{number}].emitter declares no `period` and `norm`: the "
                    "excited record's period P (the nearest integer to 2 pi / omega_b) and the "
                    "one-way flux into the body's centre Node over P intervals, the generator's "
                    "integers (ALGEBRA.md 9.17 (5) item 1; `excite_on_the_mode` of the massive "
                    "record generator)"
                )
            recomputed = excitation_norm(world, number, emitter.period)
            if recomputed != emitter.norm:
                raise ValueError(
                    f"{BEAM_LAW}: measured[{number}].emitter.norm {emitter.norm} is not the one-way "
                    f"flux into the body's centre Node over its period {emitter.period} advanced "
                    f"alone, {recomputed} (ALGEBRA.md 9.17 (5) item 1: the generator's integer, "
                    "recomputed at load)"
                )
            lines.append(
                f"norm (COMPUTATION): block {number}: the excited record's norm {emitter.norm} is the "
                f"one-way flux into its centre Node over the period {emitter.period} advanced alone, "
                "bit for bit; 2 pi / omega_b = "
                f"{2.0 * math.pi / reading.omega_b if reading.omega_b > 0 else math.inf:.2f} intervals"
            )
            if emitter.given is not None:
                lines.append(
                    f"given (COMPUTATION): block {number}: the given train of "
                    f"{len(emitter.given.now)} Nodes with the norm {emitter.given.norm} on the "
                    "vacuum (the generator's integers, ALGEBRA.md 9.17 (6a); no table in the engine)"
                )
        relaxation = relaxation_time(reading)
        if any(int(component) != 0 for component in entry.momentum):
            need = RELAXATION_TIMES * relaxation
            if definition.ramp < need:
                raise ValueError(
                    f"{BEAM_LAW}: measured[{number}]: the ramp {definition.ramp} is below "
                    f"{RELAXATION_TIMES} relaxation times of its own well (1 / (omega_0 - omega_b) = "
                    f"{relaxation:.1f} intervals, {RELAXATION_TIMES} times {need:.0f}; "
                    "DECLARATIONS.md section 8): a pushed body declares `ramp` at least that"
                )
            lines.append(
                f"ramp (COMPUTATION): block {number}: the ramp {definition.ramp} against the "
                f"relaxation time {relaxation:.1f} intervals, {definition.ramp / relaxation:.1f} times"
            )
    return lines
