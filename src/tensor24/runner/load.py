"""The load: the 24's tables, the trains' rows and the metric family found by its kinds, the coupling rows' plan, the gears laid, and the layout: the board, and every coefficient by one formula of the files' integers."""

# The engine's kinds come in as arguments, as main.py passes them: the runner imports no engine module.

import itertools
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, NamedTuple

import numpy as np

from tensor24.algebra.carry import Z, carry
from tensor24.runner.board import board
from tensor24.runner.files import GEAR, OPERANDS, entries, vocabulary


class Train(NamedTuple):
    """One train's rows: its first row, its kinds' indices and dimensions, its part, which runs fastest, and whether its kinds are the four-vector's square."""

    first: int
    kinds: tuple[int, ...]
    dims: tuple[int, ...]
    part: int
    square: int  # 1 where its kinds' character is the four-vector's square's: its rows that square's basis, its first 00

    def rows(self) -> int:
        """Its rows: every component of every kind, times its part."""
        return sum(self.dims) * self.part

    def row(self, kind: int, component: int, part: int) -> int:
        """The row of one component of one of its kinds, at one part."""
        return self.first + (sum(self.dims[:kind]) + component) * self.part + part


@dataclass(frozen=True, eq=False)
class Trains:
    """Every train's rows as arrays: per train its first row, its rows, its part, 1 where it is the four-vector's square, its first kind's entry and its kinds' count; per kind of a train, in the file's order, its index and dimension."""

    first: Z
    size: Z
    part: Z
    square: Z
    start: Z
    count: Z
    kind: Z
    dim: Z

    def __len__(self) -> int:
        return len(self.first)

    def __getitem__(self, t: int) -> Train:
        """One train as a record, read off the arrays."""
        at = slice(self.start[t], self.start[t] + self.count[t])
        kinds, dims = tuple(self.kind[at].tolist()), tuple(self.dim[at].tolist())
        return Train(int(self.first[t]), kinds, dims, int(self.part[t]), int(self.square[t]))


def common(values: Any) -> int:
    """The greatest common divisor of whole numbers, by Euclid's carries; 0 where all are 0."""
    g = 0
    for value in values:
        a, b = abs(value), g
        while b:
            a, b = b, carry(a, b, 0)[1]
        g = a
    return g


def primitive(c: Z) -> Z:
    """A table over its entries' greatest common divisor, its first entry that is not 0 positive: the strength its one scale."""
    g = common(c)
    if not g:
        return c
    q, _ = carry(c, g, 0)
    return q if next(x for x in q if x) > 0 else -q


def tables(
    kinds: Sequence[Z], inverse: Sequence[Z], weight: Z, projector: Callable[..., Z]
) -> dict[Any, Z]:
    """C[i, k -> m] for every three kinds: the group sum of each elementary seed in turn, the first not 0, made primitive."""
    found = {}
    every = range(len(kinds))
    for i, k, m in itertools.product(every, every, every):
        shape = tuple(kinds[n].shape[-1] for n in (m, i, k))
        seeds = projector(weight, kinds[m], inverse[i], inverse[k]).reshape(int(np.prod(shape)), -1).T
        found[(i, k, m)] = primitive(next((seed for seed in seeds if seed.any()), seeds[0])).reshape(
            shape
        )
    return found


def trains_of(kind: Z, of: Z, part: Z, dims: tuple[int, ...], reads: tuple[Z, Z, Z]) -> Trains:
    """Each train's rows from its kinds and part, and 1 where its kinds' character is the four-vector's square's: its rows that square's basis, its first 00."""
    traces, _, squared = reads
    member = np.eye(len(part), dtype=object)[of]  # each kind's train, one of each row
    dim = np.array(dims, dtype=object)[kind]
    size, count = part * (dim @ member), member.sum(axis=0)
    square = (part[:, None] * (member.T @ traces[kind]) == squared).all(axis=-1).astype(int)
    return Trains(np.cumsum(size) - size, size, part, square, np.cumsum(count) - count, count, kind, dim)


def side(
    train: Train, kind: int, part: int, operand: int, rows: int, labels: tuple[str, ...], d: int
) -> tuple[int, list[int]]:
    """One side of a coupling row: the kind it enters as and its readings' rows; a gradient is a T1 reading of an A1 train."""
    gradient = OPERANDS.index("gradient")
    if operand == gradient:
        return labels.index("T1"), [
            (gradient + axis) * rows + train.row(kind, 0, part) for axis in range(d)
        ]
    plane = operand if operand < gradient else operand + d - 1
    return train.kinds[kind], [plane * rows + train.row(kind, x, part) for x in range(train.dims[kind])]


def plan(
    couplings: list[list[int]], trains: Trains, c: dict[Any, Z], labels: tuple[str, ...], d: int
) -> tuple[tuple[Z, Z, Z, Z], list[str]]:
    """The coupling rows over the tables as index arrays; a row the 24 or the readings refuse is named and gives no term."""
    rows = trains.size.sum()
    first: list[int] = []
    second: list[int] = []
    factor: list[int] = []
    landing: list[int] = []
    found = []
    for at, row in enumerate(couplings):
        (
            train,
            kind,
            part,
            operand,
            with_train,
            with_kind,
            with_part,
            with_operand,
            target,
            target_kind,
            target_part,
            strength,
        ) = row
        where = f"universe.couplings[{at}]"
        if {OPERANDS[operand], OPERANDS[with_operand]} & {"before", "after"}:
            found.append(
                f"{where}: before and after enter at stage 7c, with the trains that step between an impulse and its carry"
            )
            continue
        sides = ((train, kind, part, operand), (with_train, with_kind, with_part, with_operand))
        if any(OPERANDS[o] == "gradient" and labels[trains[t].kinds[k]] != "A1" for t, k, _, o in sides):
            found.append(f"{where}: a gradient of a train not of A1, whose channel with T1 is unnamed")
            continue
        (a, ones), (b, twos) = (side(trains[t], k, p, o, rows, labels, d) for t, k, p, o in sides)
        landed = trains[target].kinds[target_kind]
        table = c[(a, b, landed)]
        if not table.any():
            found.append(f"{where}: the 24 hold no {labels[a]} x {labels[b]} -> {labels[landed]}")
        for x, y, z in np.argwhere(table):
            first.append(ones[y])
            second.append(twos[z])
            factor.append(strength * table[x, y, z])
            landing.append(trains[target].row(target_kind, x, target_part))
    first_, second_, landing_ = (np.array(column, dtype=np.intp) for column in (first, second, landing))
    return (first_, second_, np.array(factor, dtype=object), landing_), found


def lay(gears: list[list[int]], trains: Trains, sites: int) -> tuple[tuple[Z, ...], list[str]]:
    """The setting's gears laid on the trains' rows, every drive's fine tooth at 0; a board past the machine's arrays, named."""
    rows = trains.size.sum()
    try:
        a = np.zeros((rows, sites), dtype=object)
        b, r, rd = a.copy(), a.copy(), a.copy()
    except (ValueError, MemoryError) as error:
        return (), [
            f"piece.shape: {rows} rows at {sites} sites, more than the arrays of this machine hold ({error})"
        ]
    train, component, site, now, before, tooth = np.array(gears, dtype=object).reshape(-1, len(GEAR)).T
    at = (trains.first[train.astype(np.intp)] + component).astype(np.intp), site.astype(np.intp)
    a[at], b[at], r[at] = now, before, tooth
    return (a, b, r, rd), []


def promises(r: Z, w: Z) -> list[str]:
    """The engine's promise, each departure named where it stands: every fine tooth within [0, w), its teeth."""
    w = np.broadcast_to(w, r.shape)
    return [
        f"row {g}, site {x}: the fine tooth {r[g, x]} not within [0, {w[g, x]})"
        for g, x in np.argwhere((r < 0) | (r >= w))
    ]


class Loaded(NamedTuple):
    """What the load makes of the universe and the setting: the trains' rows, the coupling rows' plan, the state laid."""

    trains: Trains
    plan: tuple[Z, Z, Z, Z]
    state: tuple[Z, ...]


def load(
    universe: dict[str, Any], setting: dict[str, Any], sites: int, kinds: Any, c: dict[Any, Z], square: Z
) -> tuple[Loaded, list[str]]:
    """The held files loaded on the engine's kinds on the 24, their tables and the four-vector's square, the plan's and the lay's departures named; nothing is read of a load past one."""
    labels, dims, reads = vocabulary(kinds, square)
    trains = trains_of(*entries(universe["trains"], labels), dims, reads)
    planned, refused = plan(universe.get("couplings", []), trains, c, labels, kinds.t1.shape[-1])
    state, laid = lay(setting.get("gears", []), trains, sites)
    return Loaded(trains, planned, state), refused + laid


def mesh_unit(gamma: int) -> int:
    """G by K-S1, the least G at which one notch of tension at the vacuum resolves, 2 G^2 (2 Gamma - 1) > Gamma^2: 16 at Gamma 1,000, as the head's mesh_unit_of finds it."""
    return next(g for g in itertools.count(1) if (g + g) * g * (gamma + gamma - 1) > gamma * gamma)


def geared(
    universe: dict[str, Any], trains: Trains, spokes: int
) -> tuple[tuple[Z, ...], tuple[Z, Z, Z], Z]:
    """Every gear's coefficients by one formula of the files' integers (David's table at rest, #2187 6488192915): the teeth at rest T = 6 den Gamma^2 G^2, the 6 the board's Spokes; every row reading the 00 slot of every train whose kinds are the four-vector's square, at the factor 1, the slot itself; s = 1; the kick and the drive 1, the force's path, the one drive owed with the coupling family (G3); no spring, as no row holds a term of its own, so the swing's top is owed to the metric's law (G2); every grip den Gamma^2 G^2 per Mesh."""
    integers, first, rows = universe["integers"], trains.first, trains.size.sum()
    den, gamma = integers["den"], integers["full_rate"]
    g = mesh_unit(gamma)
    grip = den * gamma * gamma * g * g
    ones = np.ones((rows, 1), dtype=object)
    gearing = (
        spokes * grip * ones,
        ones,
        ones.copy(),
        ones.copy(),
    )  # main.py makes them the engine's records
    # every row reads each square's 00 slot, its first row, one term each
    squares, every = np.flatnonzero(trains.square), np.arange(rows, dtype=np.intp)
    clock = (
        np.repeat(first[squares].astype(np.intp), rows),
        np.ones(len(squares) * rows, dtype=object),
        np.tile(every, len(squares)),
    )
    return gearing, clock, grip


def star(axes: int) -> Z:
    """The Node-clock's star as the files lay it at the initialization: each Spoke's direction, the + and the - of every axis in turn, the neighbours' order."""
    unit = np.eye(axes, dtype=object)
    return np.stack((unit, -unit), axis=1).reshape(-1, axes)


def geometry(nb: Z, axes: int) -> tuple[Z, Z]:
    """The board's Spokes as the act reads them: the star, and the Mesh each Spoke holds, each axis's Meshes after the earlier axes', the + Spoke's the site's own and the - Spoke's its - neighbour's."""
    _, n = nb.shape
    offsets = np.arange(axes, dtype=np.intp)[:, None] * n
    _, minus = np.moveaxis(nb.reshape(axes, -1, n), 1, 0)
    meshes = np.stack((offsets + np.arange(n, dtype=np.intp), offsets + minus), axis=1).reshape(-1, n)
    return star(axes), meshes


def laid_out(universe: dict[str, Any], shape: list[int], loaded: Loaded) -> tuple[Any, ...]:
    """The board read once from the files as the layout's seven parts: the board and its Spokes from the piece's sides, every coefficient and grip from the universe's integers, J's plan and every gear's clock; main.py, the one joint, makes them the engine's records."""
    sx, sy, sz = shape
    nb = board((sx, sy, sz))
    spokes, meshes = geometry(nb, len(shape))
    gearing, clock, grip = geared(universe, loaded.trains, len(nb))
    grips = np.full((1, len(shape) * nb.shape[1]), grip, dtype=object)
    return nb, spokes, meshes, grips, gearing, loaded.plan, clock
