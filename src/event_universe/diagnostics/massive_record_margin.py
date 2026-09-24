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

import dataclasses
import math
from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.events.world import BEAM_LAW, MARGIN_KINDS, NatureBeamWorld

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
        axes' self-reads count fully, so a one-cell well runs away at a
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


def bound_mode(world: NatureBeamWorld, number: int) -> np.ndarray:
    """The bound mode's shape of a block on the world's own board (the
    margin module's Lanczos vector, its largest entry 1), over the whole
    board: the seed a pin world declares as integers at its amplitude
    (MASSIVE_RECORD.md section 11 item 7, the reader of record and the
    seed; a HOST computation of the generator, never of the engine's run)."""
    entry = world.measured[number]
    definition = entry.block
    if definition is None:
        raise ValueError(f"{BEAM_LAW}: measured[{number}] is no block")
    family = world.families[entry.family]
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    wrap = world.kind_periodic(entry.family)
    corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
    cells = block_cells(shape, corner, definition.side, wrap)
    ratio = np.where(cells, definition.pair[1] / definition.pair[0], family.pair[1] / family.pair[0])
    seed = np.where(cells, 1.0, 0.0) + 1e-3 * np.random.default_rng(0).standard_normal(shape)
    _, _, mode = lanczos(ratio, wrap, seed, vector=True)
    assert mode is not None
    return mode


def profile_check(world: NatureBeamWorld, number: int) -> tuple[int, int] | None:
    """The GAMEBOARD check at load of a block seeded with an integer
    profile: the largest deviation, in units, of the file's integers from
    the module's mode at the file's amplitude, with that amplitude; None
    for a flat seed (a comparison printed, never read by the state)."""
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
        if wrap[axis] and shape[axis] <= definition.side:
            # A FOLDED axis (a layer or a chain, MASSIVE_RECORD.md section 11
            # item 7: the block wraps onto itself and the rule reads the
            # Node itself across it, a_U = a_D = a_now): no face, no tail,
            # nothing for the rule to compare on that axis. A body whose side
            # equals the axis's extent spans it the same way (an emitter body
            # of side 1 on a chain or a layer, BUILD.md section 26).
            continue
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
        if entry.block.seed == 0:
            # A silent block (seed 0, no own record) holds nothing to bind: a
            # take line (an absorbing block with the kind's own pair, item 6b)
            # takes at its cells and carries no mode, so the threshold and
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
                        else f"the cells lie {have:.0f} Links from a zero face, less than "
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
    """The excited record's norm T (ALGEBRA.md 9.17 (5) item 1 in the flux's
    units of 9.19 (3)): the one-way inward flux into the body's centre cell
    that its own mode books over `period` intervals, advanced ALONE (the
    body on its board with no other measured event, no set and no emitter,
    the rule exact on integers), the same sum `_excitation_rung` books to
    the offer. The generator writes it as the emitter's `norm`; the loader
    recomputes it here and refuses a mismatch (a load check, not the law)."""
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
    total = 0
    for _ in range(period):
        simulation.step()
        own = block.own
        assert own is not None
        total += simulation.inward_flux(own, simulation.centre_mask(block))
    return total


def composed_largest_eigenvalues(world: NatureBeamWorld) -> dict[int, float]:
    """The largest eigenvalue of the COMPOSED operator of each massive family
    (ALGEBRA.md 9.19 (2)): every body's well of the family in one read
    matrix on the family's faces; the stability condition is read on it,
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
            cells = block_cells(shape, corner, definition.side, world.kind_periodic(index))
            ratio = np.where(cells, definition.pair[1] / definition.pair[0], ratio)
            seed = seed + np.where(cells, 1.0, 0.0)
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
        expected = np.rint(bound_mode(world, number) * amplitude).astype(np.int64)
        for level_name, level in (("now", own.now), ("before", own.before)):
            found = np.asarray(level, dtype=np.int64)
            differing = np.nonzero(found != expected)
            if differing[0].size:
                x, y, z = (int(differing[axis][0]) for axis in range(3))
                raise ValueError(
                    f"{BEAM_LAW}: measured[{number}]: the body's initial state is not the bound "
                    f"mode's integer profile at the amplitude {amplitude}: at the Node ({x}, {y}, "
                    f"{z}) the level `{level_name}` holds {int(found[x, y, z])} where the mode gives "
                    f"{int(expected[x, y, z])} ({int(differing[0].size)} Nodes differ; the seed is "
                    "written as the margin module's own integers over the whole board, "
                    "`mode_profile` of the massive record generator, ALGEBRA.md 8.7: the standing "
                    "start exact; the model owner's word of 2026-09-24, 16:48Z)"
                )
        lines.append(
            f"seed (COMPUTATION): block {number}: the initial state is the bound mode's integer "
            f"profile at the amplitude {amplitude} at both levels, bit for bit "
            f"({int(np.count_nonzero(expected))} Nodes nonzero)"
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
                    "one-way flux into the body's centre cell over P intervals, the generator's "
                    "integers (ALGEBRA.md 9.17 (5) item 1; `excite_on_the_mode` of the massive "
                    "record generator)"
                )
            recomputed = excitation_norm(world, number, emitter.period)
            if recomputed != emitter.norm:
                raise ValueError(
                    f"{BEAM_LAW}: measured[{number}].emitter.norm {emitter.norm} is not the one-way "
                    f"flux into the body's centre cell over its period {emitter.period} advanced "
                    f"alone, {recomputed} (ALGEBRA.md 9.17 (5) item 1: the generator's integer, "
                    "recomputed at load)"
                )
            lines.append(
                f"norm (COMPUTATION): block {number}: the excited record's norm {emitter.norm} is the "
                f"one-way flux into its centre cell over the period {emitter.period} advanced alone, "
                "bit for bit; 2 pi / omega_b = "
                f"{2.0 * math.pi / reading.omega_b if reading.omega_b > 0 else math.inf:.2f} intervals"
            )
            if emitter.born is not None:
                now = np.array(emitter.born[0], dtype=np.int64)
                before = np.array(emitter.born[1], dtype=np.int64)
                motion = (now - before).astype(object)
                lines.append(
                    f"born (COMPUTATION): block {number}: the born profile on "
                    f"{int(np.count_nonzero(now | before))} Nodes, the motion it inserts "
                    f"{int(np.sum(motion * motion))}"
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
