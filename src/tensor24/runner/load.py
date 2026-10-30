"""Clock: every Node-clock made alike: the 24's tables, each train's rows, every gear's teeth and every Mesh's grip, each train's click tooth at its birth, and the setting's gears laid.
Algebra: a channel's table is the primitive row u of its group sum c u u^T, its sign by Rule3's sign test; the teeth at rest 6 den Gamma^2, the grips den Gamma^2, s, T_k and T_d at 1; the key the universe file's CHOSEN integer, the click tooth born at (key - 1) div 2, the Spokes along one axis the divisor.
Board: the metric family found by its kinds' character: its 00 slot read into every other row's teeth, its own at rest (the acyclic cut), its ii slots into each axis's grips; each train's area the cross of its two parts through its kinds' tables onto A1, the kind found by its character.
Clicks: n/a: no number of the load reaches the clicks except through the act.
"""

# The engine's kinds come in as arguments, as main.py passes them: the runner imports no engine module.

from dataclasses import dataclass
from typing import Any, NamedTuple

import numpy as np

from tensor24.algebra.carry import Z, carry, lit
from tensor24.runner.board import board
from tensor24.runner.files import GEAR, entries, vocabulary


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


@dataclass(frozen=True, eq=False)
class Trains:
    """Every train's rows as arrays: per train its first row, its rows, its part, 1 where it is the four-vector's square and 1 where it is not (the matter), its first kind's entry and its kinds' count; per kind of a train, in the file's order, its index and dimension."""

    first: Z
    size: Z
    part: Z
    square: Z
    matter: Z  # 1 where the train's kinds' character is not the square's: the matter, which sources the metric's push
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


def first(x: Z) -> Z:
    """1 at the first 1 along the last axis of an array of 0s and 1s, 0 elsewhere: each entry times the zero test of the count of 1s before it."""
    before = np.cumsum(x, axis=-1) - x
    alone, _ = carry(1, before * before + 1, 0)
    return x * alone


def tables(held: Z, inverse: Z, weight: Z) -> Z:
    """C[i, k -> m] for every three kinds at once in the axes' cube, no seed chosen and no channel searched: the group sum S of rho_m(g) Psi_m x rho_i(g^-1)^T Phi_i x rho_k(g^-1)^T Phi_k, Psi and Phi the two forms each kind's matrices keep, is c u u^T on a channel and 0 off one; c is its diagonal's entry that divides every other, u its row there over c, times the sign of its first entry not 0 by Rule3's sign test."""
    kinds, side = len(held), held.shape[-1]
    cube = (kinds, kinds, kinds, -1)
    # each kind's two kept forms: Psi the sum of rho rho^T, the output's; Phi the sum of rho^T rho, an input's
    out = np.einsum("mgxy,myz->mgxz", held, np.einsum("g,mgxy,mgzy->mxz", weight, held, held))
    into = np.einsum("igpa,ipz->igaz", inverse, np.einsum("g,mgyx,mgyz->mxz", weight, held, held))
    outward, inward = np.einsum("mgxx->mgx", out), np.einsum("igaa->iga", into)
    diagonal = np.einsum("g,mgx,iga,kgb->ikmxab", weight, outward, inward, inward).reshape(cube)
    # the diagonal's entries not 0 are c times a square; c is the one that divides every other
    zero, _ = carry(1, diagonal * diagonal + 1, 0)
    _, rest = carry(diagonal[..., None, :], (diagonal + zero)[..., :, None], 0)
    whole, _ = carry(1, rest * rest + 1, 0)
    at = first(lit(diagonal) * np.prod(whole, axis=-1))
    c = (at * diagonal).sum(axis=-1)
    # S's row there, each factor's own row read at the entry's place
    place = at.reshape(kinds, kinds, kinds, side, side, side)
    outer = np.einsum("ikmx,mgxy->ikmgy", np.einsum("ikmxab->ikmx", place), out)
    middle = np.einsum("ikma,igap->ikmgp", np.einsum("ikmxab->ikma", place), into)
    inner = np.einsum("ikmb,kgbq->ikmgq", np.einsum("ikmxab->ikmb", place), into)
    row = np.einsum("g,ikmgy,ikmgp,ikmgq->ikmypq", weight, outer, middle, inner).reshape(cube)
    none, _ = carry(1, c * c + 1, 0)  # 1 where no channel stands: its row is 0
    u, _ = carry(row, (c + none)[..., None], 0)
    lead = (first(lit(u)) * u).sum(axis=-1)
    # the sign of the first entry not 0: the sign test of it less the sign test of its negative
    up, _ = carry(lead, lead * lead + 1, 0)
    down, _ = carry(-lead, lead * lead + 1, 0)
    return ((up - down)[..., None] * u).reshape(kinds, kinds, kinds, side, side, side)


def trains_of(kind: Z, of: Z, part: Z, dims: tuple[int, ...], reads: tuple[Z, Z, Z]) -> Trains:
    """Each train's rows from its kinds and part, and 1 where its kinds' character is the four-vector's square's: its rows that square's basis, its first 00."""
    traces, _, squared = reads
    member = np.eye(len(part), dtype=object)[of]  # each kind's train, one of each row
    dim = np.array(dims, dtype=object)[kind]
    size, count = part * (dim @ member), member.sum(axis=0)
    # Rule3's quotient of 1 by one more than the characters' squared gap: 1 where the gap is 0 on every turn, else 0
    gap = part[:, None] * (member.T @ traces[kind]) - squared
    away = (gap * gap).sum(axis=-1)
    square, _ = carry(1, away + 1, 0)
    return Trains(
        np.cumsum(size) - size, size, part, square, lit(away), np.cumsum(count) - count, count, kind, dim
    )


def lay(gears: list[list[int]], trains: Trains, sites: int, birth: Z) -> tuple[tuple[Z, ...], list[str]]:
    """The setting's gears laid on the trains' rows, every drive's fine tooth at 0 and every train's click tooth at its birth; a board past the machine's arrays, named."""
    rows = trains.size.sum()
    try:
        a = np.zeros((rows, sites), dtype=object)
        b, r, rd = a.copy(), a.copy(), a.copy()
        k = birth + np.zeros((len(trains), sites), dtype=object)
    except (ValueError, MemoryError) as error:
        return (), [
            f"piece.shape: {rows} rows at {sites} sites, more than the arrays of this machine hold ({error})"
        ]
    train, component, site, now, before, tooth = np.array(gears, dtype=object).reshape(-1, len(GEAR)).T
    at = (trains.first[train.astype(np.intp)] + component).astype(np.intp), site.astype(np.intp)
    a[at], b[at], r[at] = now, before, tooth
    return (a, b, r, rd, k), []


def clicking(trains: Trains, c: Z, traces: Z, key: Z) -> tuple[Z, Z, Z, Z, Z]:
    """Every train's whole click as the act reads it, with its key: its first part crossed with its second through each of its kinds' table with itself onto A1, the kind whose character is its own square on every turn, one term per entry of the table each way round (one part's now count with the other's kick, less the reverse), each into its train; a train of one part crosses its part with itself, so each term meets its opposite and no area moves."""
    # A1 is the one kind whose character is 1 on the 24 and 0 off them, its own square everywhere; each kind's form is
    # its table with itself onto A1, read over A1's one component
    gap = traces * traces - traces
    trivial = 1 - lit((gap * gap).sum(axis=-1))
    form = np.einsum("m,jjmyxi->jxi", trivial, c)
    # each kind entry's train, and the components before it, counted along the board's rows and within its own train
    kind, dim, part = trains.kind, trains.dim.astype(np.intp), trains.part
    of = np.repeat(np.arange(len(trains), dtype=np.intp), trains.count.astype(np.intp))
    before = np.cumsum(dim) - dim
    within = before - before[trains.start.astype(np.intp)][of]
    # one term per entry of each kind's form: the form's row x and column i at each
    pairs = dim * dim
    entry = np.repeat(np.arange(len(dim), dtype=np.intp), pairs)
    place = np.arange(pairs.sum(), dtype=np.intp) - np.repeat(np.cumsum(pairs) - pairs, pairs)
    x, i = carry(place, np.repeat(dim, pairs), 0)
    train = of[entry]
    first, p = trains.first[train], part[train]
    other = lit(p - 1)  # the second part, where the train has one
    one, two = first + (within[entry] + x) * p, first + (within[entry] + i) * p
    factor = form[kind[entry], x, i]
    return (
        np.concatenate((one, one + other)).astype(np.intp),
        np.concatenate((two + other, two)).astype(np.intp),
        np.concatenate((factor, -factor)),
        np.concatenate((train, train)),
        key,
    )


def pairs_of(trains: Trains, c: Z, traces: Z) -> tuple[Z, Z, Z, Z]:
    """Every pair of rows of each train through its kinds' table with itself onto A1, the kind whose character is its own square on every turn, one pair per entry of the table and part: (the first row, the second row, the entry, the train), the parts running fastest within a component as the load lays them."""
    gap = traces * traces - traces
    trivial = 1 - lit((gap * gap).sum(axis=-1))
    form = np.einsum("m,jjmyxi->jxi", trivial, c)
    kind, dim, part = trains.kind, trains.dim.astype(np.intp), trains.part.astype(np.intp)
    of = np.repeat(np.arange(len(trains), dtype=np.intp), trains.count.astype(np.intp))
    before = np.cumsum(dim) - dim
    within = before - before[trains.start.astype(np.intp)][of]
    squares = dim * dim
    entry = np.repeat(np.arange(len(dim), dtype=np.intp), squares)
    place = np.arange(squares.sum(), dtype=np.intp) - np.repeat(np.cumsum(squares) - squares, squares)
    x, i = carry(place, np.repeat(dim, squares), 0)
    train = of[entry]
    # each entry once per part of its train, the part's offset counted within the entry's run
    parts = part[train]
    each = np.repeat(np.arange(len(entry), dtype=np.intp), parts)
    offset = np.arange(parts.sum(), dtype=np.intp) - np.repeat(np.cumsum(parts) - parts, parts)
    first = (trains.first[train] + within[entry] * part[train])[each]
    one, two = first + x[each] * parts[each] + offset, first + i[each] * parts[each] + offset
    return one.astype(np.intp), two.astype(np.intp), form[kind[entry], x, i][each], train[each]


def spread(*parts: Z) -> Z:
    """Arrays broadcast together and flattened, one row each: a block of terms over the pairs and an axis or two."""
    return np.stack(np.broadcast_arrays(*parts)).reshape(len(parts), -1)


def pushing(trains: Trains, c: Z, traces: Z, spokes: Z, strength: Z) -> tuple[Z, Z, Z, Z, Z]:
    """Term 5, the metric's push, as a plan on the readings with the momenta in and out added before the unit: for every pair of a train not the square (the matter) and every square train, J = 2T - eta T from T00 = S (sigma_in sigma_in + sigma_out sigma_out), T_ij = D_i a D_j a and T_0i = (sigma_in + sigma_out) D_i a, S = Spokes x senses the slots' own ratio (c^2 = grip / rest at the loader's lay, two strides against two gradients); the 00 slot pushed by +S J00 (its unit the teeth), each ii, jk and 0i slot by -J (its unit the grips, at both ends of a Mesh), so gamma = 1 and the grips are lowered where matter is; the strength CHOSEN in the universe file; a train that is no square takes every term at the factor 0."""
    one, two, entry, train = pairs_of(trains, c, traces)
    n, d = spokes.shape
    senses, _ = carry(n, d, 0)
    scale, rows, trained = n * senses, trains.size.sum(), len(trains)
    unit = (
        d + senses * senses
    ) * rows  # the planes: the value, the d differences, the force, the momenta in and out
    sigma_in, sigma_out = d + senses, d + senses + 1
    axis = np.arange(d, dtype=np.intp)
    _, after = carry(axis + 1, d, 0)  # the other two axes of a shear slot, named by its third axis
    _, before = carry(axis + senses, d, 0)
    # every matter pair against every train: the factor carries the pair's entry, the strength, the matter's flag and
    # the target's square flag; the target's slot rows wrap at the rows, harmless at the factor 0
    f = np.outer(entry * trains.matter[train] * strength, trains.square).reshape(-1)
    o, w = np.repeat(one, trained), np.repeat(two, trained)
    q00 = np.tile(trains.first, len(one))
    _, q0i = carry(q00[:, None] + 1 + axis[None, :], rows, 0)
    _, qii = carry(q00[:, None] + 1 + d + axis[None, :], rows, 0)
    _, qjk = carry(q00[:, None] + 1 + senses * d + axis[None, :], rows, 0)
    # the readings each term enters: the momenta's planes at the pair's rows, and the differences' along each axis
    so, sw = sigma_in * rows + o, sigma_in * rows + w
    to, tw = sigma_out * rows + o, sigma_out * rows + w
    grad = 1 + axis[None, :]  # the difference along each axis, a plane per axis
    go, gw = grad * rows + o[:, None], grad * rows + w[:, None]
    ao, aw = (1 + after) * rows + o[:, None], (1 + after) * rows + w[:, None]
    bo, bw = (1 + before) * rows + o[:, None], (1 + before) * rows + w[:, None]
    goo, gww = grad[:, None, :] * rows + o[:, None, None], grad[:, None, :] * rows + w[:, None, None]
    # the factors: S S f on the 00 slot's momenta, S f on its differences, -S f and -f on the ii slots, f on the
    # other axes' differences there, -f on the shears and the 0i slots
    whole, half, less, back = scale * scale * f, scale * f[:, None], -scale * f[:, None], -f[:, None]
    other = f[:, None, None] * lit(
        axis[None, :, None] - axis[None, None, :]
    )  # 1 where the two axes differ
    blocks = np.concatenate(
        (
            spread(so, sw, whole, q00),
            spread(to, tw, whole, q00),
            spread(go, gw, half, q00[:, None]),
            spread(so[:, None], sw[:, None], less, qii),
            spread(to[:, None], tw[:, None], less, qii),
            spread(go, gw, back, qii),
            spread(goo, gww, other, qii[:, :, None]),
            spread(ao, bw, back, qjk),
            spread(bo, aw, back, qjk),
            spread(so[:, None], gw, back, q0i),
            spread(go, sw[:, None], back, q0i),
            spread(to[:, None], gw, back, q0i),
            spread(go, tw[:, None], back, q0i),
        ),
        axis=1,
    )
    first, second, factor, target = blocks
    third = unit + 0 * first
    return (
        first.astype(np.intp),
        second.astype(np.intp),
        third.astype(np.intp),
        factor,
        target.astype(np.intp),
    )


class Loaded(NamedTuple):
    """What the load makes of the universe and the setting: the trains' rows, J's potential, the state laid, the click's cross with its key, the metric's push."""

    trains: Trains
    potential: tuple[
        Z, tuple[Z, Z, Z, Z]
    ]  # J's potential: per monomial its factor and its four legs, the unit (-1) for a leg it lacks
    state: tuple[Z, ...]
    click: tuple[
        Z, Z, Z, Z, Z
    ]  # the whole click's cross: per term the row read, the row whose kick it crosses, its factor, its train; the keys
    push: tuple[
        Z, Z, Z, Z, Z
    ]  # term 5's plan: per term its three readings (the unit for a leg it lacks), its factor and the slot row it lands on


def load(
    universe: dict[str, Any], setting: dict[str, Any], sites: int, kinds: Any, c: Z, square: Z
) -> tuple[Loaded, list[str]]:
    """The held files loaded on the engine's kinds on the 24 and the four-vector's square, the lay's departures named; J's potential holds no monomial, as no file declares a coupling, until the coupling family's one plan reads the 24's tables c (G3); every train's key the universe file's one CHOSEN integer (its unit the train card's, G3), its click tooth born at (key - 1) div 2; the metric's push laid at the file's CHOSEN strength."""
    labels, dims, reads = vocabulary(kinds, square)
    trains = trains_of(*entries(universe["trains"], labels), dims, reads)
    none = np.empty(0, dtype=np.intp)
    traces, _, _ = reads
    side = c.shape[-1]  # the axes' cube the tables stand in: the board's axes
    senses, _ = carry(len(star(side)), side, 0)  # the Spokes along one axis, its + and its -
    key = np.full((len(trains), 1), universe["chosen"]["key"], dtype=object)  # one key for the board
    birth, _ = carry(key - 1, senses, 0)  # the one tooth the mirror leaves in place
    state, laid = lay(setting.get("gears", []), trains, sites, birth)
    potential = (none.astype(object), (none, none, none, none))
    push = pushing(trains, c, traces, star(side), universe["chosen"]["push"])
    return Loaded(trains, potential, state, clicking(trains, c, traces, key), push), laid


def geared(
    universe: dict[str, Any], trains: Trains, spokes: Z
) -> tuple[tuple[Z, ...], tuple[Z, Z, Z], tuple[Z, Z, Z], Z]:
    """Every gear's coefficients by one formula of the files' integers (David's table at rest, #2187 6488192915): the teeth at rest T = 6 den Gamma^2, the 6 the board's Spokes; every row but the slot's own reading the 00 slot of every train whose kinds are the four-vector's square, at the factor 1, the slot itself, the 00 row's teeth at rest; every Spoke's grip reading each square's ii slot of its axis at both ends of its Mesh; s = 1; the kick and the drive 1, the force's path, the one drive owed with the coupling family (G3); no spring, as no row holds a term of its own, so the swing's top is owed to the metric's law (G2); every grip den Gamma^2 per Mesh, one notch of a slot moving a grip by one count, so the Mesh unit is 1."""
    integers, first, rows = universe["integers"], trains.first, trains.size.sum()
    den, gamma = integers["den"], integers["full_rate"]
    grip = den * gamma * gamma
    ones = np.ones((rows, 1), dtype=object)
    # the square's 0i slots, the rows after its 00 slot, are odd under time's reversal (one time index): their parity
    # is 1 less the two senses of an axis, every other row's 1; a lone train's places wrap harmlessly at the factor 0
    n, d = spokes.shape
    senses, _ = carry(n, d, 0)
    axis = np.arange(d, dtype=np.intp)
    _, at = carry((first[:, None] + 1 + axis[None, :]).reshape(-1), rows, 0)
    odd = np.zeros((rows, 1), dtype=object)
    np.add.at(
        odd, (at.astype(np.intp), 0 * at.astype(np.intp)), np.repeat(trains.square, d).astype(object)
    )
    gearing = (
        len(spokes) * grip * ones,
        ones,
        ones.copy(),
        ones.copy(),
        1 - senses * odd,
    )  # main.py makes them the engine's records
    # every row reads every train's first row at the factor of its square flag, a square's 00 slot at 1 and the rest
    # at 0, less its own row: the zero test of the rows' difference cuts the 00 row's read of itself, so its teeth stand
    # at rest and the clocks' read is acyclic (a dial is never moved by its own quotient)
    trained, every = len(trains), np.arange(rows, dtype=np.intp)
    read, landed = np.repeat(first.astype(np.intp), rows), np.tile(every, trained)
    clock = (
        read,
        np.repeat(trains.square, rows).astype(object) * lit((read - landed).astype(object)),
        landed,
    )
    # every Spoke's grip reads a square's diagonal slot for its axis, after the 00 slot and the 0i slots, at the factor 1;
    # a train not the square reads its first row at the factor 0
    along = (spokes * spokes) @ axis
    diagonal = first[:, None] + trains.square[:, None] * (1 + d + along[None, :])
    stretch = (
        diagonal.reshape(-1).astype(np.intp),
        np.repeat(trains.square, n).astype(object),
        np.tile(np.arange(n, dtype=np.intp), trained),
    )
    return gearing, clock, stretch, grip


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
    """The board read once from the files as the layout's ten parts: the board and its Spokes from the piece's sides, every coefficient and grip from the universe's integers, J's potential, every gear's clock and the grips' read, the click's cross with its key, the metric's push; main.py, the one joint, makes them the engine's records."""
    sx, sy, sz = shape
    nb = board((sx, sy, sz))
    spokes, meshes = geometry(nb, len(shape))
    gearing, clock, stretch, grip = geared(universe, loaded.trains, spokes)
    grips = np.full((1, len(shape) * nb.shape[1]), grip, dtype=object)
    return (
        nb,
        spokes,
        meshes,
        grips,
        gearing,
        loaded.potential,
        clock,
        stretch,
        loaded.click,
        loaded.push,
    )
