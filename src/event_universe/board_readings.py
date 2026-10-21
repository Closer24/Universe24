"""The board's readings, each one loop over the lattice's records and no act (ALGEBRA.md #the-interval: the currents, the turned records' sign currents and the tensions' parts read from every record at the pair the step starts from; `Lattice.step`, `Lattice.booked_back`): every family of quanta's currents through the Ports (`currents`), every record's tension's part per axis with the count's flux and, where a held row declares the shear, the shear's part per axis pair (`stresses`), every turned record's sign current, or under its holder's Lorentz form its step's own flux through each +a Link (`sense_currents`, `sense_fluxes`), and a held family's uniform mode, the time line's mean level now and before (`uniform_mode`, `UniformMode`); readings alone, no level written, each the lattice's loop over the readings of one record (readings.py, features/currents)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

import numpy as np

import event_universe.readings as readings
import event_universe.records as records
from event_universe import covector, flux, node
from event_universe.bookings import sources_of
from event_universe.core import paces
from event_universe.core.rule3 import division_forward

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

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


def currents(board: Lattice) -> Currents:
    """Every family of quanta's plain current through each Port at every Node, read from its record (`readings.currents_of`) before Rule3 acts, the pair the step starts from, so that the share's change over the step is exactly their sum where no tension stands (ALGEBRA.md #the-count-is-the-records-share); a charged family's records' currents added, light's the current of its rows' sum; a turned record's from its plain pair as its share reads it (`record`); the click line's number and every diagnostic's, the credit booking the weighted current (`node_detector.weighed_currents`)."""
    return {
        index: readings.currents_of(
            board.families[index].pair[0],
            board.record(index),
            board.wrap,
            covector.weights(board.families[index]),
        )
        for index in board.order
    }


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
    gamma = board.world.node_clock
    content, factors = board.read(index, direction, record)
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
    return covector.link_fluxes(lines, pairs, pace * pace, board.wrap)


def uniform_mode(board: Lattice, index: int) -> UniformMode:
    """The uniform mode of a held family's time line as the board holds it, a lattice reading and no act (ALGEBRA.md, The closed lattice has no rest; the world's `uniform: carried`): the level now and the level before summed over the Nodes in Python's integers, each divided once by the Nodes' count with its remainder kept beside (`UniformMode`: `level`, `level_remainder`, `before`, `before_remainder`, `nodes`), so that N x level + remainder is the sum exactly; the k = 0 component Rule3's own line carries at every Node (`held_write`), read here as one integer per held family, every family alike."""
    line, nodes = board.states[index].lines[0], int(np.prod(board.shape))
    found = []
    for levels in (line.now, line.before):
        total = int(np.asarray(levels, dtype=object).sum())
        level, remainder = division_forward(total, nodes, 0)
        found += [int(level), int(remainder)]
    return UniformMode(found[0], found[1], found[2], found[3], nodes)
