"""The load: the 24's tables from the engine's kinds, the trains' rows, the coupling rows' plan and the gears laid."""

# The engine's kinds come in as arguments, as main.py passes them: the runner imports no engine module.

import itertools
from collections.abc import Callable, Sequence
from typing import Any, NamedTuple

import numpy as np

from tensor24.algebra.carry import Z, carry
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
