"""Clock: every Node-clock made alike: the 24's tables, each train's rows, every gear's teeth and every Mesh's grip, the held hand's spring and the ties of the coupling family, each train's click tooth at its birth, and the setting's gears laid.
Algebra: a channel's table is the primitive row u of its group sum c u u^T, its sign by Rule3's sign test; the teeth at rest 6 den Gamma^2, the grips den Gamma^2, s and T_k at 1, T_d senses on the square's 00 and ii rows and 1 elsewhere, the clock's read at Spokes x senses; the key the universe file's CHOSEN integer, the click tooth born at (key - 1) div 2, the Spokes along one axis the divisor.
Board: the metric family found by its kinds' character: its 00 slot read into every other row's teeth at k0 = Spokes x senses, its own at rest (the acyclic cut), its ii slots into each axis's grips, its 0i slots odd under the mirror, its 00 and ii rows driven at the dial senses; the held hand found by its character, the one-dimensional kinds together, its rows' grips 0 (a site-local oscillator), the tied trains by their character kept under the sign kind's twist; the plans (runner/plans.py) laid from the kinds' tables at the universe file's CHOSEN strengths: the momenta of every row on the force's path onto the square's 00 slot and every row's stretches onto its ii slots (the metric's push in the books' form), the monomials of the notch, the held hand's spring and tie and the hands' tie, the gradient vertex through the Mesh at the CHOSEN mesh, and each train's passing through its own form onto A1, the kind found by its character.
Clicks: n/a: no number of the load reaches the clicks except through the act.
"""

# The engine's kinds come in as arguments, as main.py passes them: the runner imports no engine module.

from dataclasses import dataclass
from typing import Any, NamedTuple

import numpy as np

from tensor24.algebra.carry import Z, carry, lit
from tensor24.runner.board import board
from tensor24.runner.files import GEAR, entries, star, vocabulary
from tensor24.runner.plans import holding, joined, meshing, notching, passing, pushing, tying


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
    """Every train's rows as arrays: per train its first row, its rows, its part, 1 where it is the four-vector's square and 1 where it is not (a clock train that sources the metric's push), its first kind's entry and its kinds' count; per kind of a train, in the file's order, its index and dimension."""

    first: Z
    size: Z
    part: Z
    square: Z
    sourcing: Z  # 1 where the kinds' character is not the square's: its rows source the metric's push
    held: Z  # 1 where the character is the held hand's, the one-dimensional kinds together at part 1: its own spring CHOSEN
    tied: Z  # 1 where the character is kept under the sign kind's twist and is not the held hand's: tied to the held hand
    gripped: Z  # 1 where the character is not the held hand's: its rows hold their Meshes' grips; the held hand holds none
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


def trains_of(kind: Z, of: Z, part: Z, dims: tuple[int, ...], reads: tuple[Z, Z, Z, Z, Z]) -> Trains:
    """Each train's rows from its kinds and part, and its character, its kinds' traces summed times its part, against the characters the files read off the kinds, 1 where the gap is 0 on every turn by Rule3's quotient of 1 by gap^2 + 1 and lit of the gap where it is not: the four-vector's square's (square: its rows that square's basis, its first 00; sourcing the rest), the held hand's, the one-dimensional kinds together (held, A1 + A2 at part 1; gripped the rest), and its own under the twist, the sign kind's character (tied where kept and not the held hand's: a train of the kinds K and the twist's K, the board's wave and the square untied)."""
    traces, _, squared, hand, twist = reads
    member = np.eye(len(part), dtype=object)[of]  # each kind's train, one of each row
    dim = np.array(dims, dtype=object)[kind]
    size, count = part * (dim @ member), member.sum(axis=0)
    character = part[:, None] * (member.T @ traces[kind])
    gap = character - squared
    away = (gap * gap).sum(axis=-1)
    square, _ = carry(1, away + 1, 0)
    off = character - hand
    apart = (off * off).sum(axis=-1)
    held, _ = carry(1, apart + 1, 0)
    twisted = character * twist[None, :] - character
    kept, _ = carry(1, (twisted * twisted).sum(axis=-1) + 1, 0)
    return Trains(
        np.cumsum(size) - size,
        size,
        part,
        square,
        lit(away),
        held,
        kept * lit(apart),
        lit(apart),
        np.cumsum(count) - count,
        count,
        kind,
        dim,
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
    # the format's fields head the gears' rows, so a setting of no gears lays every field empty
    train, component, site, now, before, tooth = np.array([GEAR, *gears], dtype=object)[1:].T
    at = (trains.first[train.astype(np.intp)] + component).astype(np.intp), site.astype(np.intp)
    a[at], b[at], r[at] = now, before, tooth
    return (a, b, r, rd, k), []


class Loaded(NamedTuple):
    """What the load makes of the universe and the setting: the trains' rows, J's potential, the state laid, the passing's pairs with their key, the metric's push, the gradient vertex's plan."""

    trains: Trains
    potential: tuple[
        Z, tuple[Z, Z, Z, Z]
    ]  # J's potential: per monomial its factor and its four legs, the unit (-1) for a leg it lacks
    state: tuple[Z, ...]
    click: tuple[
        Z, Z, Z, Z, Z
    ]  # the whole click's passing: per term a pair of a train's rows through its form onto A1, the entry, its train; the keys
    push: tuple[
        Z, Z, Z, Z, Z
    ]  # term 5's plan: per term its three readings (the unit for a leg it lacks), its factor and the slot row it lands on
    mesh: tuple[
        Z, Z, Z, Z, Z
    ]  # the gradient vertex: per term its readings on the plan's planes, its factor, its row


def load(
    universe: dict[str, Any], setting: dict[str, Any], sites: int, kinds: Any, c: Z, square: Z
) -> tuple[Loaded, list[str]]:
    """The held files loaded on the engine's kinds on the 24 and the four-vector's square, the lay's departures named; J's potential holds the notch's monomials, the held hand's own spring and tie and the hands' tie, laid from the 24's tables c and the file's CHOSEN strengths, as no file declares a coupling; every train's key the universe file's one CHOSEN integer, its click tooth born at (key - 1) div 2, its passing the pairs of its rows through its form; the metric's push and the notch laid at the file's CHOSEN strengths."""
    labels, dims, reads = vocabulary(kinds, square)
    trains = trains_of(*entries(universe["trains"], labels), dims, reads)
    traces, *_ = reads
    side = c.shape[-1]  # the axes' cube the tables stand in: the board's axes
    senses, _ = carry(len(star(side)), side, 0)  # the Spokes along one axis, its + and its -
    key = np.full((len(trains), 1), universe["chosen"]["key"], dtype=object)  # one key for the board
    birth, _ = carry(key - 1, senses, 0)  # the click tooth at its birth, a pair's two summing to key - 1
    state, laid = lay(setting.get("gears", []), trains, sites, birth)
    chosen, _, rest = universe["chosen"], *teeth(universe, star(side))
    potential = joined(
        notching(trains, star(side), chosen["notch"]),
        holding(
            trains, c, traces, rest, chosen["hold"], universe["integers"]["full_rate"], chosen["spring"]
        ),
        tying(trains, c, traces, chosen["tie"]),
    )
    push = pushing(trains, star(side), chosen["push"])
    mesh = meshing(trains, c, traces, square, chosen["mesh"])
    return Loaded(trains, potential, state, passing(trains, c, traces, key), push, mesh), laid


def teeth(universe: dict[str, Any], spokes: Z) -> tuple[Z, Z]:
    """The grip at rest and the teeth at rest from the files' integers: den Gamma^2 per Mesh, and Spokes times it, the 6 the board's Spokes (David's table at rest)."""
    integers = universe["integers"]
    grip = integers["den"] * integers["full_rate"] * integers["full_rate"]
    return grip, len(spokes) * grip


def geared(
    universe: dict[str, Any], trains: Trains, spokes: Z
) -> tuple[tuple[Z, ...], tuple[Z, Z, Z], tuple[Z, Z, Z], Z]:
    """Every gear's coefficients by one formula of the files' integers and the star's counts (David's table at rest, #2187 6488192915): the teeth at rest T = 6 den Gamma^2, the 6 the board's Spokes; every row but the slot's own reading the 00 slot of every train whose kinds are the four-vector's square at the factor k0 = Spokes x senses (one unit for all ten slots), the slot itself, the 00 row's teeth at rest; every Spoke's grip reading each square's ii slot of its axis at both ends of its Mesh at the factor 1; s = 1; the kick 1 and the drive 1, the force's path, on every row but the square's 00 and ii rows, whose dial is senses, term 5's push in the books' form halved with the remainder kept in the fine tooth; every grip den Gamma^2 per Mesh, one notch of a slot moving a grip by one count, so the Mesh unit is 1."""
    first, rows = trains.first, trains.size.sum()
    grip, rest = teeth(universe, spokes)
    ones = np.ones((rows, 1), dtype=object)
    # the square's 0i slots, the rows after its 00 slot, are odd under time's reversal (one time index): their parity
    # is 0, every other row's 1; a lone train's places wrap harmlessly at the factor 0
    n, d = spokes.shape
    senses, _ = carry(n, d, 0)
    axis = np.arange(d, dtype=np.intp)
    _, at = carry((first[:, None] + 1 + axis[None, :]).reshape(-1), rows, 0)
    even = np.ones((rows, 1), dtype=object)
    np.add.at(
        even, (at.astype(np.intp), 0 * at.astype(np.intp)), -np.repeat(trains.square, d).astype(object)
    )
    # the drive's dial on the square's pushed rows, its 00 and ii rows, is senses: term 5's push in the books' form is
    # the derivative of the act's energy halved by the two slots of an edge, and the carry keeps the half as the fine
    # tooth (the notch's monomials on those rows ride the same dial); every other row's dial is 1, the force's path
    scale = n * senses
    _, ii = carry((first[:, None] + 1 + d + axis[None, :]).reshape(-1), rows, 0)
    pushed = np.zeros((rows, 1), dtype=object)
    np.add.at(pushed, (first.astype(np.intp), 0 * first.astype(np.intp)), trains.square.astype(object))
    np.add.at(
        pushed, (ii.astype(np.intp), 0 * ii.astype(np.intp)), np.repeat(trains.square, d).astype(object)
    )
    gearing = (
        rest * ones,
        ones,
        ones.copy(),
        ones + pushed * (senses - 1),
        even,
    )  # main.py makes them the engine's records
    # every row reads every train's first row at the factor of its square flag times Spokes x senses, a square's 00
    # slot at k0 = 12 (one unit, the half grip, for all ten slots: the board's wave, its grip reading ii, needs it,
    # gamma owed to the click world, the Boss's frame, NOT_CLOSED 26) and the rest at 0, less its own row: the zero
    # test of the rows' difference cuts the 00 row's read of itself, so its teeth stand at rest and the clocks' read
    # is acyclic (a dial is never moved by its own quotient)
    trained, every = len(trains), np.arange(rows, dtype=np.intp)
    read, landed = np.repeat(first.astype(np.intp), rows), np.tile(every, trained)
    clock = (
        read,
        np.repeat(trains.square * scale, rows).astype(object) * lit((read - landed).astype(object)),
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


def geometry(nb: Z, axes: int) -> tuple[Z, Z]:
    """The board's Spokes as the act reads them: the star, and the Mesh each Spoke holds, each axis's Meshes after the earlier axes', the + Spoke's the site's own and the - Spoke's its - neighbour's."""
    _, n = nb.shape
    offsets = np.arange(axes, dtype=np.intp)[:, None] * n
    _, minus = np.moveaxis(nb.reshape(axes, -1, n), 1, 0)
    meshes = np.stack((offsets + np.arange(n, dtype=np.intp), offsets + minus), axis=1).reshape(-1, n)
    return star(axes), meshes


def laid_out(universe: dict[str, Any], shape: list[int], loaded: Loaded) -> tuple[Any, ...]:
    """The board read once from the files as the layout's eleven parts: the board and its Spokes from the piece's sides, every coefficient from the universe's integers, the grips per row, den Gamma^2 on every Mesh of a row whose train is not the held hand and 0 on the held hand's rows (a site-local oscillator: its turn at every Node-clock is its own whatever its neighbours do, and its stability at every wavevector the one Node-clock's; the ii slots' read still lands on its Spokes, so a world with the held hand keeps the push at 0 or its summed grips within the window, which the runner refuses by name otherwise), J's potential, every gear's clock and the grips' read, the passing's pairs with their key, the metric's push, the plan's terms with a Mesh leg (the gradient vertex, plans.meshing); main.py, the one joint, makes them the engine's records."""
    sx, sy, sz = shape
    nb = board((sx, sy, sz))
    spokes, meshes = geometry(nb, len(shape))
    gearing, clock, stretch, grip = geared(universe, loaded.trains, spokes)
    rows = np.repeat(
        loaded.trains.gripped, loaded.trains.size.astype(np.intp)
    )  # 1 but on the held hand's rows
    grips = np.outer(rows, np.full(len(shape) * nb.shape[1], grip, dtype=object))
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
        loaded.mesh,
    )
