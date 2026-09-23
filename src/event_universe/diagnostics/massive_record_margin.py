"""The margin rule of the massive record kind (`massive-record-v1`,
docs/designs/detector_law/MASSIVE_RECORD.md section 11 item 4, Reviewer 3's
two lines; the build's plan BUILD.md section 0, FINDING 1): a load-time
check of a world's blocks, made before the world runs, in a HOST module
outside the engine's integer path.

The block's bound mode in the massive medium: the rule of section 1 with
the kind's pair `[num, den]` on every Node and the block's lowered pair on
its cells has the characters `2 cos omega D a = (S_6 / 3) a`, D = den /
num per Node (the six-neighbour sum with the kind's faces, the row itself
twice on an axis of one layer, as the engine reads it); the bound mode is
the largest eigenvalue `lambda = 2 cos omega_b` of the symmetric operator
`A = D^-1/2 (S_6 / 3) D^-1/2`, found by a Lanczos iteration (the largest
Ritz value of the three-term recurrence, converged to 1e-9). Then, with
D_out the kind's own ratio, `cosh kappa = 3 D_out cos omega_b - 2` and the
mode's extent in the medium is `1 / kappa` Links (the tail exp(-kappa x)),
its binding depth `eps = 1 - omega_b^2 / omega_0^2` with `cos omega_0 =
num / den`. A mode at or above the gap (lambda / 2 <= num / den) is not
bound and the block is refused. THE RULE: a CONTROL world's cells lie at
least ONE extent from any non-periodic face of the kind and a periodic
axis's side is at least the block's side plus TWO extents; a PIN world's
cells lie at least TWO extents from a non-periodic face and a periodic side
is at least the side plus FOUR extents (a hard face at distance d shifts
the mode by about eps e^(-2 kappa d)); a declaration below the margin is
refused naming the block, the axis, the extent and the distance; a cavity
(form (I), its record held by its own faces) has no tail and is not
checked. Every
number here is a COMPUTATION from the declaration, printed before the run
and written into the run's record; the state never reads it (the
transcendental of the pair is no verb of the law). This is the method of
the design's `massive_board_margin.py` on the world's own board and faces
(the design's table was computed on 96^3 and 128^3 boxes; a periodic image
shifts omega_b, so the world's own number is the pin's).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from event_universe.events.world import BEAM_LAW, MARGIN_KINDS, NatureBeamWorld

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


def block_cells(
    shape: tuple[int, int, int], corner: tuple[int, int, int], side: int, wrap: tuple[bool, bool, bool]
) -> np.ndarray:
    """The block's cells as the engine forms them: the cube from its lower
    corner, wrapped on a periodic axis of the kind, cut on an open one."""
    mask = np.zeros(shape, dtype=bool)
    ranges = []
    for axis in range(3):
        indices = [corner[axis] + offset for offset in range(side)]
        if wrap[axis]:
            indices = [index % shape[axis] for index in indices]
        else:
            indices = [index for index in indices if 0 <= index < shape[axis]]
        ranges.append(sorted(set(indices)))
    if all(ranges):
        mask[np.ix_(ranges[0], ranges[1], ranges[2])] = True
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
    scale = 1.0 / np.sqrt(ratio)

    def apply(vector: np.ndarray) -> np.ndarray:
        result: np.ndarray = scale * six_neighbours(scale * vector, wrap) / 3.0
        return result

    q = seed.astype(np.float64)
    q /= np.linalg.norm(q)
    previous = np.zeros_like(q)
    beta = 0.0
    alphas: list[float] = []
    betas: list[float] = []
    ritz_before = None
    for iteration in range(1, MOST_ITERATIONS + 1):
        w = apply(q) - beta * previous
        alpha = float(np.vdot(q, w))
        w -= alpha * q
        alphas.append(alpha)
        beta = float(np.linalg.norm(w))
        if iteration >= 3:
            tridiagonal = np.diag(alphas) + np.diag(betas, 1) + np.diag(betas, -1)
            ritz = float(np.linalg.eigvalsh(tridiagonal)[-1])
            if ritz_before is not None and abs(ritz - ritz_before) < RITZ_TOLERANCE:
                return ritz, iteration
            ritz_before = ritz
        if beta < 1e-14:
            break
        betas.append(beta)
        previous, q = q, w / beta
    tridiagonal = (
        np.diag(alphas) + np.diag(betas[: len(alphas) - 1], 1) + np.diag(betas[: len(alphas) - 1], -1)
    )
    return float(np.linalg.eigvalsh(tridiagonal)[-1]), len(alphas)


def block_margin(world: NatureBeamWorld, number: int) -> MarginReading:
    """The reading of one block: its mode on the world's own board with its
    kind's faces, alone in the medium (the other blocks' wells not carried:
    each block is checked on its own)."""
    entry = world.measured[number]
    definition = entry.block
    if definition is None:
        raise ValueError(f"{BEAM_LAW}: measured[{number}] is no block")
    family = world.families[entry.family]
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    wrap = world.kind_periodic(entry.family)
    corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
    cells = block_cells(shape, corner, definition.side, wrap)
    ratio_out = family.pair[1] / family.pair[0]
    ratio_in = definition.pair[1] / definition.pair[0]
    ratio = np.where(cells, ratio_in, ratio_out)
    seed = np.where(cells, 1.0, 0.0) + 1e-3 * np.random.default_rng(0).standard_normal(shape)
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
        if wrap[axis]:
            have = float(shape[axis])
            need = definition.side + SIDE_EXTENTS[definition.margin] * extent
        else:
            have = float(min(corner[axis], shape[axis] - corner[axis] - definition.side))
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
        if entry.block.cavity:
            # A cavity (form (I)) binds its record by its mirror faces: its
            # mode has no tail in the medium and the rule has no extent to
            # compare; the control world of MASSIVE_RECORD.md section 4.
            continue
        reading = block_margin(world, number)
        found.append(reading)
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
                        else f"the cells lie {have:.0f} Links from a zero face, less than "
                        f"{FACE_EXTENTS[reading.kind]:.0f} extents = {need:.1f}"
                    )
                )
    return found
