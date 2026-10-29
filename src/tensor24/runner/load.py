"""The load: the 24's tables, the trains' rows with the clock's own time gear, the coupling rows' plan, the gears laid, and the layout: the board, every coefficient from the files' integers, and the ruler walked once."""

# The engine's kinds come in as arguments, as main.py passes them: the runner imports no engine module.

import itertools
from collections.abc import Callable, Sequence
from typing import Any, NamedTuple

import numpy as np

from tensor24.algebra.carry import Z, carry
from tensor24.runner.board import board
from tensor24.runner.files import OPERANDS


class Train(NamedTuple):
    """One train's rows: its first row, its kinds' indices and dimensions, and its part, which runs fastest."""

    first: int
    kinds: tuple[int, ...]
    dims: tuple[int, ...]
    part: int

    def rows(self) -> int:
        """Its rows: every component of every kind, times its part."""
        return sum(self.dims) * self.part

    def row(self, kind: int, component: int, part: int) -> int:
        """The row of one component of one of its kinds, at one part."""
        return self.first + (sum(self.dims[:kind]) + component) * self.part + part


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


def trains_of(
    trains: list[dict[str, Any]], labels: tuple[str, ...], dims: tuple[int, ...]
) -> tuple[list[Train], list[str]]:
    """Each train's rows from its kinds and part; a kind or a part that the 24's five kinds and the hands cannot hold, named."""
    held: list[Train] = []
    found = []
    for at, train in enumerate(trains):
        where = f"universe.trains[{at}]"
        for j, label in enumerate(train["kinds"]):
            if label not in labels:
                found.append(
                    f"{where}.kinds[{j}]: {label!r} is none of the 24's kinds {labels} (twin kinds wait on OPEN 3)"
                )
            elif label == "E":
                found.append(
                    f"{where}.kinds[{j}]: E has no whole basis the 24 permute; it stands beside A1 in the tensions (stage 7c)"
                )
        if train["part"] not in (1, 1 + 1):
            found.append(
                f"{where}.part: 1, one gear, or 2, a hand, not {train['part']} (twin hands wait on OPEN 3)"
            )
        kinds = tuple(labels.index(label) for label in train["kinds"] if label in labels)
        first = held[-1].first + held[-1].rows() if held else 0
        held.append(Train(first, kinds, tuple(dims[k] for k in kinds), train["part"]))
    # the clock's own time gear, one A1 gear after the file's trains, laid at every Node-clock and named by no file
    scalar = labels.index("A1")
    held.append(Train(held[-1].first + held[-1].rows() if held else 0, (scalar,), (dims[scalar],), 1))
    return held, found


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
    couplings: list[list[int]], trains: list[Train], c: dict[Any, Z], labels: tuple[str, ...], d: int
) -> tuple[tuple[Z, Z, Z, Z], list[str]]:
    """The coupling rows over the tables as index arrays; a row the 24 or the readings refuse is named and gives no term."""
    rows = sum(t.rows() for t in trains)
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


def lay(gears: list[list[int]], trains: list[Train], sites: int) -> tuple[tuple[Z, ...], list[str]]:
    """The setting's gears laid on the trains' rows, every going, drive's tooth, dial, count and time at 0; one off, named."""
    rows = sum(t.rows() for t in trains)
    try:
        a, b, r, go, rd = (np.zeros((rows, sites), dtype=object) for _ in ("a", "b", "r", "go", "rd"))
        ph, c, tn = (np.zeros((1, sites), dtype=object) for _ in ("ph", "c", "tn"))
    except (ValueError, MemoryError) as error:
        return (), [
            f"piece.shape: {rows} rows at {sites} sites, more than the arrays of this machine hold ({error})"
        ]
    found = []
    for at, (train, component, site, now, before, tooth) in enumerate(gears):
        if component >= trains[train].rows():
            found.append(
                f"setting.gears[{at}]: component {component} off train {train}'s {trains[train].rows()} rows"
            )
            continue
        row = trains[train].first + component
        a[row, site], b[row, site], r[row, site] = now, before, tooth
    return (a, b, r, go, rd, ph, c, tn), found


def promises(r: Z, w: Z, rate: Z, gamma: Z) -> list[str]:
    """The engine's two promises, each departure named where it stands: a fine tooth within [0, w), a rate within [0, Gamma]."""
    w = np.broadcast_to(w, r.shape)
    rate, gamma = (np.broadcast_to(x, (1, r.shape[-1])) for x in (rate, gamma))
    teeth = [
        f"row {g}, site {x}: the fine tooth {r[g, x]} not within [0, {w[g, x]})"
        for g, x in np.argwhere((r < 0) | (r >= w))
    ]
    rates = [
        f"site {x}: the rate {rate[0, x]} not within [0, the full rate {gamma[0, x]}]"
        for _, x in np.argwhere((rate < 0) | (rate > gamma))
    ]
    return teeth + rates


class Loaded(NamedTuple):
    """What the load makes of the universe and the setting: the trains' rows, the coupling rows' plan, the state laid."""

    trains: list[Train]
    plan: tuple[Z, Z, Z, Z]
    state: tuple[Z, ...]


def load(
    universe: dict[str, Any], setting: dict[str, Any], sites: int, kinds: Any, c: dict[Any, Z]
) -> tuple[Loaded | None, list[str]]:
    """The checked files loaded on the engine's kinds and their tables, every departure named; nothing loads past one."""
    labels, dims = tuple(name.upper() for name in kinds._fields), tuple(k.shape[-1] for k in kinds)
    trains, found = trains_of(universe["trains"], labels, dims)
    if found:
        return None, found
    planned, refused = plan(universe.get("couplings", []), trains, c, labels, kinds.t1.shape[-1])
    state, laid = lay(setting.get("gears", []), trains, sites)
    return (None if refused + laid else Loaded(trains, planned, state)), refused + laid


def mesh_unit(gamma: int) -> int:
    """G by K-S1, the least G at which one notch of tension at the vacuum resolves, 2 G^2 (2 Gamma - 1) > Gamma^2: 16 at Gamma 1,000, as the head's mesh_unit_of finds it."""
    return next(g for g in itertools.count(1) if (g + g) * g * (gamma + gamma - 1) > gamma * gamma)


def rounded(n: int, d: int) -> int:
    """n over d rounded half up, one carry at the doubled teeth from the half (the head's one rounding)."""
    return int(carry(n + n, d + d, d)[0])


def ruler_of(gamma: int) -> list[int]:
    """The ruler Y(c) = rate(-c) at every load from 0 to the clock's last rate (David, #2187 6488192915), the head's core/rates walked once: the hills' side from Gamma^3 at the resolution Gamma^2, one carry by Gamma over Gamma - 1 per load, each rounded once, as far as the hollows' side, by Gamma - 1 over Gamma, keeps the Mesh's rate p0^2 over Gamma from rounding to 0 (3,793 loads at Gamma 1,000)."""
    square = gamma * gamma
    hollow, hollow_tooth = square * gamma, carry(gamma, 1 + 1, 0)[0]
    hill, hill_tooth = square * gamma, carry(gamma - 1, 1 + 1, 0)[0]
    found = []
    while rounded(rounded(hollow, square) * rounded(hollow, square), gamma):
        found.append(rounded(hill, square))
        hollow, hollow_tooth = carry(hollow * (gamma - 1), gamma, hollow_tooth)
        hill, hill_tooth = carry(hill * gamma, gamma - 1, hill_tooth)
    return found


def geared(
    universe: dict[str, Any], trains: list[Train], spokes: int
) -> tuple[tuple[Z, ...], tuple[Z, ...], Z]:
    """Every gear's coefficients from the files' integers, David's table at rest (#2187 6488192915, 6488709540), T = 6 den Gamma^2 G^2 and every grip den Gamma^2 G^2 per Mesh: a file's train reads the ruler at W = W+ = 2 T, s = 2, its spring 12 (den - pinion) G^2 Gamma^2 on the force's path; the time gear stands on its own teeth, W = W+ = T, s = 1, its pinion den - den div Gamma, its kick T and its drive's teeth (T div 2) key; the 6 is the board's Spokes and the 12 its sides times the Spokes."""
    integers, rows = universe["integers"], sum(t.rows() for t in trains)
    den, gamma, key = integers["den"], integers["full_rate"], integers["key"]
    g = mesh_unit(gamma)
    teeth = spokes * den * gamma * gamma * g * g
    pinions = [train["pinion"] for train in universe["trains"]] + [den - carry(den, gamma, 0)[0]]
    rest = [p for train, pinion in zip(trains, pinions, strict=True) for p in [pinion] * train.rows()]
    time = trains[-1]
    reads = [1] * (rows - time.rows()) + [0] * time.rows()
    column = np.array(
        [
            [r * (teeth + teeth) + (1 - r) * teeth for r in reads],
            [r * (1 + 1) + (1 - r) for r in reads],
            [(spokes + spokes) * (den - p) * g * g for p in rest],
            [r + (1 - r) * teeth for r in reads],
            [r + (1 - r) * carry(teeth, 1 + 1, 0)[0] * key for r in reads],
        ],
        dtype=object,
    )[:, :, None]
    w, stretch, spring, kick, drive = column
    ruler = ruler_of(gamma)
    fourth = gamma * gamma * gamma * gamma
    tables = (
        np.array([carry(teeth * y * y * y * y, fourth, 0)[0] for y in ruler], dtype=object),
        np.array([y * y for y in ruler], dtype=object),
    )
    gearing = (
        w,
        w.copy(),
        stretch,
        spring * gamma * gamma,
        kick,
        drive,
    )  # main.py makes them the engine's records
    reading = np.array(reads, dtype=object)[:, None]
    held = (time.first, len(ruler) - 1, *tables, reading, spring * reading)
    return gearing, held, den * gamma * gamma * g * g


def sourced(plan: tuple[Z, Z, Z, Z], spring: Z, rows: int, time: int, axes: int) -> tuple[Z, Z, Z, Z]:
    """J's plan with the time gear's source, rho + 3p of every train through its own dot (David, #2187 6488709540): -2 value . force - D value . value over every row of the file's trains, D the row's spring at rest, light's 0."""
    first, second, factor, target = plan
    own = np.arange(time, dtype=np.intp)  # every row of the file's trains, before the time gear's
    force = (axes + 1) * rows + own  # the force's plane, after the value and the axes' differences
    return (
        np.concatenate((first, own, own)),
        np.concatenate((second, force, own)),
        np.concatenate((factor, np.full(time, -(1 + 1), dtype=object), -spring[:time, 0])),
        np.concatenate((target, np.full(time + time, time, dtype=np.intp))),
    )


def laid_out(universe: dict[str, Any], shape: list[int], loaded: Loaded) -> tuple[Any, ...]:
    """The board read once from the files as the layout's eight parts: the board from the piece's sides, every coefficient and grip from the universe's integers, J's plan with the time gear's source, every dial at the full rate and the clock's ruler; main.py, the one joint, makes them the engine's records."""
    sx, sy, sz = shape
    nb, meshes = board((sx, sy, sz))
    gearing, ruler, grip = geared(universe, loaded.trains, len(nb))
    _, _, _, spring, _, _ = gearing
    row, *_ = ruler
    gamma, sites, rows = (
        universe["integers"]["full_rate"],
        nb.shape[1],
        sum(t.rows() for t in loaded.trains),
    )
    return (
        nb,
        meshes,
        np.full((1, len(shape) * sites), grip, dtype=object),
        gearing,
        sourced(loaded.plan, spring, rows, row, len(shape)),
        np.full((1, sites), gamma, dtype=object),
        gamma,
        ruler,
    )
