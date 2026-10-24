"""The board's readings, each one loop over the lattice's records and no act (ALGEBRA.md #the-interval: the currents, the turned records' sign currents and the tensions' parts read from every record at the pair the step starts from; `Lattice.step`, `Lattice.booked_back`): every family of quanta's currents through the Ports (`currents`; a turned record's with the Link pairs its step reads, `turned_read`, `turned_currents`), every record's tension's part per axis with the count's flux and, where a held row declares the shear, the shear's part per axis pair (`stresses`), every turned record's sign current, or under its holder's Lorentz form its step's own flux through each +a Link (`sense_currents`, `sense_fluxes`), the families' densities over the declared regions written as the output's field lines (`densities_read`, a lattice reading labelled so), a held family's uniform mode, the time line's mean level now and before (`uniform_mode`, `UniformMode`), and a held row of the content's eras as the board reads them under the volume form (`eras`, `Eras`: the families' writes, the hill's weight over the Nodes, the mix's exponent and the constraint's residual as integers, the seed Node's level against the other Nodes'); readings alone, no level written, each the lattice's loop over the readings of one record (readings.py, features/currents)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

import numpy as np

import event_universe.readings as readings
import event_universe.records as records
from event_universe import registry
from event_universe.bookings import Bookings, sources_of
from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.features import volume
from event_universe.frames import frames_of
from event_universe.loader.derived import weight_of

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Stresses = dict[
    records.Sourcing, tuple[Any, ...]
]  # per record of quanta its tension, its flux per axis, its shear per axis pair where declared


class UniformMode(NamedTuple):
    """A held family's uniform mode as a lattice reading (`uniform_mode`): the time line's level now and level before, each the sum over the Nodes divided once by their count, with the two remainders and the Nodes' count."""

    level: int
    level_remainder: int
    before: int
    before_remainder: int
    nodes: int


def horizon_ports(board: Lattice, index: int) -> tuple[Any, ...] | None:
    """Per Port the mask of a family's Links at the wall, the horizon (ALGEBRA.md, The horizon, 2026-10-23): the Links whose factor the read gives at 0 (features/read.link_tensions, the tension at or past Gamma read at the wall); None where no Link stands at the wall."""
    factors = board.read(index)[1]
    found = []
    for factor in factors:
        at = np.asarray(np.asarray(factor) == 0)
        found.append(at)
    return tuple(found) if any(bool(np.any(at)) for at in found) else None


def stresses(board: Lattice) -> Stresses:
    """Every record of quanta's tension's part on each axis at every Node, read from its lines as they stand, the pair the step starts from (`readings.stresses_of`), the count's flux along each axis beside it (`readings.axis_sources_of`, the flux holder's odd lines' source) and, where a held row of the world declares the shear (`off_diagonals`), the shear's part on each axis pair, the product of the Node's own two axis differences D_a D_b at the same Node and interval (`readings.off_diagonals_of`, the shear lines' source): the Node's own part h_a(i) the content's axis lines take in their one write, the Link's tension being the sum of its two ends' parts, read through the Ports at the next interval (ALGEBRA.md #the-primitives, The tension); a world without the word runs as before bit for bit, the shear's readings not made."""
    return {
        s: readings.axis_sources_of(
            board.families[s[0]].pair[0],
            board.lines_of(*s),
            board.wrap,
            frames_of(s[0], board.families, board.states, board.wrap, s[1]),
        )
        for s in sources_of(board.families, board.states, board.order)
    }


def sense_currents(board: Lattice) -> Stresses:
    """Every turned record's sign current on each axis at every Node, the Node's two a-Links' Wronskian currents summed unhalved, J_a = Im(conj(z_i) (z_(+a) - z_(-a))), read from its lines as they stand at the interval's start (`readings.sense_current_of`): the source the odd lines of the record's own row take in their one write under the rotation at the doubled wall 2 E_s T (`loader.derived.held_write_of`; the two hands' lines of 2026-10-09); where the record's holder of the sign declares the Lorentz form, the record's step's own flux through each of the Node's three +a Links instead (`sense_fluxes`, covector.link_fluxes), read after the interval's phase act with the Link pairs the step reads."""
    return {
        s: sense_fluxes(board, s, board.lines_of(*s), 1)
        for s in sources_of(board.families, board.states, board.order)
        if s[0] in board.turning
    }


def sense_fluxes(
    board: Lattice, source: records.Sourcing, lines: list[records.Record], direction: int
) -> Any:
    """One turned record's source of its own row's odd lines at the interval's start in `direction`: the plain sign current (`readings.sense_current_of`) where its holder books each line its own, and under the holder's Lorentz form the flux of its step through each +a Link in the Link unit (covector.link_fluxes), from the Link pairs its step reads (`flux.pairs_of` at its own read, `read`, the same integers the step takes, divided by the pace squared they carry) and the levels the step starts from, the same numbers forward and back."""
    index, record = source
    frames = frames_of(index, board.families, board.states, board.wrap, record)
    return readings.sense_current_of(lines, board.wrap, frames)


def uniform_mode(board: Lattice, index: int) -> UniformMode:
    """The uniform mode of a held family's time line as the board holds it, a lattice reading and no act (ALGEBRA.md, The closed lattice has no rest; The board's interval is no observable): the level now and the level before summed over the Nodes in Python's integers, each divided once by the Nodes' count with its remainder kept beside (`UniformMode`: `level`, `level_remainder`, `before`, `before_remainder`, `nodes`), so that N x level + remainder is the sum exactly; the k = 0 component Rule3's own line carries at every Node (`held_write`), read here as one integer per held family, every family alike."""
    line, nodes = board.states[index].lines[0], int(np.prod(board.shape))
    found = []
    for levels in (row_level(board, index, line.now), row_level(board, index, line.before)):
        total = int(np.asarray(levels, dtype=object).sum())
        level, remainder = division_forward(total, nodes, 0)
        found += [int(level), int(remainder)]
    return UniformMode(found[0], found[1], found[2], found[3], nodes)


class Eras(NamedTuple):
    """A held row of the content's eras as the board reads them under the volume form (`eras`), integers alone (the host's floats from them, tools/eras.py): the time line's mean level now and before with their remainders over the Nodes' count (`uniform_mode`, the level reading of the volume where the row carries it); per sourcing family its write into the row's time line summed over the Nodes (the rounded booking at the row's power, the read weight and the write weight, in units of the wall E_s T); the mix's exponent n_eff as a pair of integers, P SUM_f S_f over SUM_f (P / n_f) S_f (`paces.exponent_products`, no division); the trace's own residual as a pair, 3 E_s T V^2 over 2 Gamma N SUM_f S_f (`nature`: V the mean's velocity times the Nodes' count with the remainders, so the fraction less 1 is (Gamma / 2) U'^2 / (SUM_f s_f / 3) - 1, the surface the trace's weight preserves, -1 at rest, 0 on nature's constraint; ALGEBRA.md, The stress's trace is the time line's); the seed Node's level with the other Nodes' sum and count (`seed`, (0, 0, 0) where the world lays no whole packet); and the three tension lines' sums over the Nodes now and before (`tensions`, `tensions_before`, 0 where the row has no axis lines): the tension's reading, the k = 0 mode of the axis lines whose growth under a lay's mean stress froze every Link in the smokes of 2026-10-22."""

    level: int
    level_remainder: int
    before: int
    before_remainder: int
    nodes: int
    writes: tuple[tuple[str, int], ...]
    mix: tuple[int, int]
    nature: tuple[int, int]
    seed: tuple[int, int, int]
    tensions: tuple[int, int, int]
    tensions_before: tuple[int, int, int]
    volume: tuple[int, int]


def volume_sums(line: records.Record, carried: bool) -> tuple[int, int]:
    """The volume's record summed over the Nodes, now and before, where the row carries its volume (features/volume; the host reads the volume form's own constraint from three of these, X'^2 over 2 X X'' less 1, tools/eras.py), (0, 0) for a row at its level."""
    if not carried:
        return 0, 0
    return int(np.asarray(line.now, dtype=object).sum()), int(
        np.asarray(line.before, dtype=object).sum()
    )


def eras(
    board: Lattice, index: int, forms: Bookings, rulers: dict[records.Sourcing, records.Rulers]
) -> Eras:
    """The eras of a held row of the content as the board reads them (`Eras`), a reading over the Nodes and no act (readings may sum over the board, acts may not: the owner's locality decision of 2026-10-22): from the interval's bookings and rulers (`forms` the records' forms about the step, `records.form` on the lines before and after; `rulers` the write's rulers at the interval's start, `Lattice.rulers`, the same numbers read at -1 after the step from the held rows' `before`), each sourcing family's write into the row's time line at every Node by the engine's own functions (`records.rulers_write_factor` at the row's booking power, the read weight, the row's write weight), the mix's exponent, the trace's residual, the seed's level and the tension lines' sums."""
    family, gamma, shape = board.families[index], board.world.node_clock, board.shape
    read, wall = uniform_mode(board, index), board.writes[index].walls[0]
    terms: list[Any] = []
    exponents: list[int] = []
    writes: list[tuple[str, int]] = []
    for source in registry.sourcing(board.families, board.states, index)[0]:
        other = board.families[source[0]]
        scaled = records.rulers_write_factor(forms.get(source, 0), rulers[source], gamma, family.power)
        weighed = weight_of(index, other) * np.asarray(scaled, dtype=object) + np.zeros(
            shape, dtype=object
        )
        terms.append(weighed)
        exponents.append(other.exponent(family.power))
        writes.append((other.name, int(family.write * weighed.sum())))
    product, others = paces.exponent_products(exponents)
    sums = [int(term.sum()) for term in terms]
    potential = sum(s * o for s, o in zip(sums, others, strict=True))  # P x SUM_f S_f / n_f
    velocity = read.nodes * (read.level - read.before) + (read.level_remainder - read.before_remainder)
    nature = (3 * wall * velocity * velocity, 2 * gamma * read.nodes * sum(write for _, write in writes))
    lines = board.states[index].lines
    tensions = tuple(
        int(np.asarray(lines[1 + a].now, dtype=object).sum()) if family.axes else 0 for a in range(3)
    )
    before = tuple(
        int(np.asarray(lines[1 + a].before, dtype=object).sum()) if family.axes else 0 for a in range(3)
    )
    seed = (0, 0, 0)
    return Eras(
        read.level,
        read.level_remainder,
        read.before,
        read.before_remainder,
        read.nodes,
        tuple(writes),
        (product * sum(sums), potential),
        nature,
        seed,
        (tensions[0], tensions[1], tensions[2]),
        (before[0], before[1], before[2]),
        volume_sums(lines[0], family.motion_volume),
    )


def row_level(board: Lattice, index: int, levels: Any) -> Any:
    """A held row's time line array as a level at every Node for the readings: the array itself, or the level reading of the volume where the row carries it (features/volume)."""
    return volume.levels_read(board.world.node_clock, levels, board.families[index].motion_volume)
