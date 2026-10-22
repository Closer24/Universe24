"""The board's readings, each one loop over the lattice's records and no act (ALGEBRA.md #the-interval: the currents, the turned records' sign currents and the tensions' parts read from every record at the pair the step starts from; `Lattice.step`, `Lattice.booked_back`): every family of quanta's currents through the Ports (`currents`; a turned record's with the Link pairs its step reads, `turned_read`, `turned_currents`), every record's tension's part per axis with the count's flux and, where a held row declares the shear, the shear's part per axis pair (`stresses`), every turned record's sign current, or under its holder's Lorentz form its step's own flux through each +a Link (`sense_currents`, `sense_fluxes`), the families' densities over the declared regions written as the output's field lines (`densities_read`, a lattice reading labelled so), a held family's uniform mode, the time line's mean level now and before (`uniform_mode`, `UniformMode`), and a held row of the content's eras as the board reads them under `interval: unobservable` (`eras`, `Eras`: the families' writes, the hill's weight over the Nodes, the mix's exponent and the constraint's residual as integers, the seed Node's level against the other Nodes'); readings alone, no level written, each the lattice's loop over the readings of one record (readings.py, features/currents)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

import numpy as np

import event_universe.readings as readings
import event_universe.records as records
from event_universe import covector, flux, node, reports
from event_universe.bookings import Bookings, sources_of
from event_universe.core import paces
from event_universe.core.ports import PORTS
from event_universe.core.rule3 import division_forward
from event_universe.loader.derived import count_wall, quanta_records, row_sources, weight_of

if TYPE_CHECKING:
    from event_universe.lattice import Lattice
    from event_universe.node_detector import Weighed

Currents = dict[int, tuple[np.ndarray, ...]]  # per family of quanta its current through each Port
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


def currents(board: Lattice, weighed: Weighed | None = None) -> Currents:
    """Every family of quanta's current through each Port at every Node, read from its record (`readings.currents_of`) before Rule3 acts, the pair the step starts from, so that the share's change over the step is exactly their sum where no tension stands (ALGEBRA.md #the-count-is-the-records-share); light's the current of its rows' sum; a turned record's the flux line's own with the Link pairs its step reads, per record and the records added (`turned_currents`; ALGEBRA.md, The share's change is the currents, the clause of 2026-10-21), every plain record's the plain bilinear bit for bit; the click line's number and every diagnostic's, the credit booking the weighted current (`node_detector.weighed_currents`); `weighed`, the bookings' read of the same interval where the step holds it, whose per-record currents of a turned family are the same integers and are added instead of read again."""
    return {
        index: turned_currents(board, index, weighed)
        if index in board.turning
        else readings.currents_of(
            board.families[index].pair[0],
            board.record(index),
            board.wrap,
            covector.weights(board.families[index]),
        )
        for index in board.order
    }


def turned_read(
    board: Lattice,
    index: int,
    record: int,
    direction: int = 1,
    read: tuple[Any, node.Factors] | None = None,
) -> readings.Turned:
    """What the books read of one turned record beside its lines (`readings.Turned`): the Link pairs its step reads in `direction` (`flux.pairs_of` at its own read, the same integers the step takes, read after the interval's phase act as the step reads them), the pace squared they carry, the six Links' factors of the read (`read`, the record's content and factors where the caller holds them, `Lattice.read` otherwise), the family's quantum W_rec (loader/derived.count_wall) and the quantum's measure of a current W_c = 3 den T."""
    gamma, action, family = board.world.node_clock, board.world.quantum_action, board.families[index]
    content, factors = board.read(index, direction, record) if read is None else read
    pairs = flux.pairs_of(
        index,
        board.families,
        board.states,
        direction,
        board.wrap,
        gamma,
        content,
        factors,
        record,
        board.amplitude,
    )
    assert pairs is not None  # a turned record reads its holder's pairs
    pace = paces.link_pace_of(gamma, content)
    return readings.Turned(
        pairs, pace * pace, factors, count_wall(family, action), 3 * family.pair[1] * action
    )


def turned_currents(
    board: Lattice, index: int, weighed: Weighed | None = None
) -> tuple[np.ndarray, ...]:
    """A turned family's currents through each Port at every Node, every record's read with the Link pairs its own step reads (`turned_read`, `readings.currents_of`), the records added; where the bookings' read of the interval is given (`weighed`, node_detector.weighed_currents, the same call per record), its records' currents added and the lines not read twice."""
    found: list[Any] = [0] * PORTS
    if weighed is not None and index in weighed:
        for through, _factors, _shares in weighed[index]:
            found = [a + b for a, b in zip(found, through, strict=True)]
        return tuple(np.asarray(value) for value in found)
    for record in quanta_records(board.families, index):
        through = readings.currents_of(
            board.families[index].pair[0],
            board.lines_of(index, record),
            board.wrap,
            None,
            turned_read(board, index, record),
        )
        found = [a + b for a, b in zip(found, through, strict=True)]
    return tuple(np.asarray(value) for value in found)


def stresses(board: Lattice) -> Stresses:
    """Every record of quanta's tension's part on each axis at every Node, read from its lines as they stand, the pair the step starts from (`readings.stresses_of`), the count's flux along each axis beside it (`readings.axis_sources_of`, the flux holder's odd lines' source) and, where a held row of the world declares the shear (`off_diagonals`), the shear's part on each axis pair, the product of the Node's own two axis differences D_a D_b at the same Node and interval (`readings.off_diagonals_of`, the shear lines' source): the Node's own part h_a(i) the content's axis lines take in their one write, the Link's tension being the sum of its two ends' parts, read through the Ports at the next interval (ALGEBRA.md #the-primitives, The tension); a world without the word runs as before bit for bit, the shear's readings not made."""
    return {
        s: readings.axis_sources_of(
            board.families[s[0]].pair[0], board.lines_of(*s), board.wrap, board.off_diagonals
        )
        for s in sources_of(board.families, board.order)
    }


def sense_currents(board: Lattice) -> Stresses:
    """Every turned record's sign current on each axis at every Node, the Node's two a-Links' Wronskian currents summed unhalved, J_a = Im(conj(z_i) (z_(+a) - z_(-a))), read from its lines as they stand at the interval's start (`readings.sense_current_of`): the source the odd lines of the record's own row take in their one write under the rotation at the doubled wall 2 E_s T (`loader.derived.held_write_of`; the two hands' lines of 2026-10-09); where the record's holder of the sign declares the Lorentz form, the record's step's own flux through each of the Node's three +a Links instead (`sense_fluxes`, covector.link_fluxes), read after the interval's phase act with the Link pairs the step reads."""
    return {
        s: sense_fluxes(board, s, board.lines_of(*s), 1)
        for s in sources_of(board.families, board.order)
        if s[0] in board.turning
    }


def sense_fluxes(
    board: Lattice, source: records.Sourcing, lines: list[records.Record], direction: int
) -> Any:
    """One turned record's source of its own row's odd lines at the interval's start in `direction`: the plain sign current (`readings.sense_current_of`) where its holder books each line its own, and under the holder's Lorentz form the flux of its step through each +a Link in the Link unit (covector.link_fluxes), from the Link pairs its step reads (`flux.pairs_of` at its own read, `read`, the same integers the step takes, divided by the pace squared they carry) and the levels the step starts from, the same numbers forward and back."""
    index, record = source
    holder = board.families[node.sign_holder(index, board.families)]
    if not holder.lorentz:
        return readings.sense_current_of(lines, board.wrap)
    read = turned_read(board, index, record, direction)
    return covector.link_fluxes(lines, read.pairs, read.square, board.wrap)


def uniform_mode(board: Lattice, index: int) -> UniformMode:
    """The uniform mode of a held family's time line as the board holds it, a lattice reading and no act (ALGEBRA.md, The closed lattice has no rest; the world's `uniform: carried`): the level now and the level before summed over the Nodes in Python's integers, each divided once by the Nodes' count with its remainder kept beside (`UniformMode`: `level`, `level_remainder`, `before`, `before_remainder`, `nodes`), so that N x level + remainder is the sum exactly; the k = 0 component Rule3's own line carries at every Node (`held_write`), read here as one integer per held family, every family alike."""
    line, nodes = board.states[index].lines[0], int(np.prod(board.shape))
    found = []
    for levels in (line.now, line.before):
        total = int(np.asarray(levels, dtype=object).sum())
        level, remainder = division_forward(total, nodes, 0)
        found += [int(level), int(remainder)]
    return UniformMode(found[0], found[1], found[2], found[3], nodes)


def densities_read(board: Lattice, forms: Bookings, at: np.ndarray) -> None:
    """A lattice reading, no measurement, labelled so (`reports.density`; `Lattice.report` calls it after the clicks): per family and declared region, the family's density over the region this interval (its share read at the declared regions' Nodes alone, `at`, the union of the declared NodeDetectors' Nodes), one `field` line where it differs from the last interval's (`Lattice.densities`, the last readings): for a family of quanta its share in quanta summed over the region (the packet's passage), None over a region holding a frozen Node, every Link pace 0 (its share is not read and no number is invented; ALGEBRA.md #the-count-is-the-records-share, the frozen Node), with the frozen Nodes' wells D div T of the interval summed beside as their content reading (`records.well`); for a holder of the content the square of its time line's deviation from the row's rest summed over the region (a row with no count, its travelling events' passage; the advisor's reading of a kick's arrival); a reading over the declared regions and no act."""
    for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
        frozen, well = np.zeros(board.shape, dtype=bool), None
        if family.quanta:
            found, frozen = board.quanta(index, at)
            form = sum(forms[(index, record)] for record in quanta_records(board.families, index))
            well = records.well(form, board.world.quantum_action)
        else:
            deviation = state.lines[0].now - family.rest
            found = deviation * deviation
        for detector in board.node_detectors:
            if not detector.declared or detector.nodes is None:
                continue
            name, cold = detector.name, detector.nodes & frozen
            reading = None if cold.any() else int(found[detector.nodes].sum(dtype=object))
            content = int(well[cold].sum(dtype=object)) if well is not None and cold.any() else None
            if board.densities.get((index, name)) == (reading, content):
                continue
            board.densities[(index, name)] = (reading, content)
            if board.output is not None:
                board.output(reports.density(board.interval, family.name, name, reading, content))


class Eras(NamedTuple):
    """A held row of the content's eras as the board reads them under `interval: unobservable` (`eras`), integers alone (the host's floats from them, tools/eras.py): the time line's mean level now and before with their remainders over the Nodes' count (`uniform_mode`); per sourcing family its write into the row's time line summed over the Nodes this interval, k_w w_f D_f f_f (`writes`, by the family's name: the family whose sum is largest sources the era, the crossing of two sums the transition); the hill's weight's least, largest and sum over the Nodes (`weight_low`, `weight_high`, `weight_sum`, the Node-mean the sum over the count, the coefficient the mean's line carries where the mix differs between Nodes, the reader's line L1 on the design); the mix's exponent n_eff = SUM_f s_f / SUM_f (s_f / n_f) over the Nodes as a pair of integers (`mix`, numerator and denominator); the constraint's residual R + 1 = Gamma v^2 / (2 Phi) as a pair of integers (`residual`: E_s T V^2 P over 2 Gamma N SUM_f (P / n_f) S_f, V the Nodes' count times the mean velocity's integer part plus the remainders' difference, S_f the family's write summed, P the exponents' product; the tracker's residual 2 (n_eff - c) / (2 c - n_eff) the host's from `mix` and the Node-mean weight); and the seed Node's level against the other Nodes' (`seed`: the time line's level at the first whole packet's Node, the sum of the other Nodes' levels and their count; (0, 0, 0) where the world lays no whole packet), the clock's contrast e^(-(U_seed - U_void)) the host's; below one level per interval the hill is quantised and the velocity pulses 0 -> 1 -> 0 at the mean rate s Gamma / n, the crawl (the floor, the crawl and the pulses one phenomenon, the history hand's and the reversal hand's), read by the host from the velocity's course and named once."""

    level: int
    level_remainder: int
    before: int
    before_remainder: int
    nodes: int
    writes: tuple[tuple[str, int], ...]
    weight_low: int
    weight_high: int
    weight_sum: int
    mix: tuple[int, int]
    residual: tuple[int, int]
    seed: tuple[int, int, int]


def eras(
    board: Lattice, index: int, forms: Bookings, rulers: dict[records.Sourcing, records.Rulers]
) -> Eras:
    """The eras of a held row of the content as the board reads them (`Eras`), a reading over the Nodes and no act (readings may sum over the board, acts may not: the owner's locality decision of 2026-10-22): from the interval's bookings and rulers (`forms` the records' forms about the step, `records.form` on the lines before and after; `rulers` the write's rulers at the interval's start, `Lattice.rulers`, the same numbers read at -1 after the step from the held rows' `before`), each sourcing family's write into the row's time line at every Node by the engine's own functions (`records.rulers_write_factor` at the row's booking power, the read weight, the row's write weight), the hill's weight at every Node by the one function the write reads (`records.hill_weight`), the mix's exponent and the constraint's residual as fractions of integers over the exponents' products (`paces.exponent_products`), and the uniform mode (`uniform_mode`)."""
    family, gamma, shape = board.families[index], board.world.node_clock, board.shape
    read, wall = uniform_mode(board, index), board.writes[index].walls[0]
    terms: list[Any] = []
    exponents: list[int] = []
    writes: list[tuple[str, int]] = []
    for source in row_sources(board.families, index, 0):
        other = board.families[source[0]]
        scaled = records.rulers_write_factor(forms.get(source, 0), rulers[source], gamma, family.power)
        weighed = weight_of(index, other) * np.asarray(scaled, dtype=object) + np.zeros(
            shape, dtype=object
        )
        terms.append(weighed)
        exponents.append(other.exponent(family.power))
        writes.append((other.name, int(family.write * weighed.sum())))
    weight = np.asarray(records.hill_weight(family, terms, exponents, wall, gamma), dtype=object)
    weight = weight + np.zeros(shape, dtype=object)
    product, others = paces.exponent_products(exponents)
    sums = [int(term.sum()) for term in terms]
    potential = sum(s * o for s, o in zip(sums, others, strict=True))  # P x SUM_f S_f / n_f
    velocity = read.nodes * (read.level - read.before) + (read.level_remainder - read.before_remainder)
    residual = (wall * velocity * velocity * product, 2 * gamma * read.nodes * family.write * potential)
    line, seed = board.states[index].lines[0], (0, 0, 0)
    if board.world.wholes:
        at = tuple(a + o for a, o in zip(board.world.wholes[0].at, board.offset, strict=True))
        level = int(line.now[at])
        seed = (level, int(np.asarray(line.now, dtype=object).sum()) - level, read.nodes - 1)
    return Eras(
        read.level,
        read.level_remainder,
        read.before,
        read.before_remainder,
        read.nodes,
        tuple(writes),
        int(weight.min()),
        int(weight.max()),
        int(weight.sum()),
        (product * sum(sums), potential),
        residual,
        seed,
    )
