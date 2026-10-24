"""The volume form of the massless row's time line under the volume form (every board's interval unobservable) (the momentum hand's derivation M12a, 2026-10-22, read cold by the reader: the hypothesis The carried momentum beside The board's interval is no observable, the body of The motion of gravity's row, the symmetric hill its first form kept by name as superseded by derivation): the row carries its time line as the volume's level X = Gamma (Gamma / p_0)^(d + 1) in place of the level a = Gamma U (Gamma at the vacuum's paces, as the clock is), the Node's proper volume (Gamma / p_0)^d per proper interval Gamma / p_0 in its own paces (The paces compose; The write per proper volume and per proper interval), the variable in which the reader's Lagrangian is a constant force, L = (Gamma / (2 (d + 1)^2)) X'^2 + (s_0 / (d + 1)) X, so that Rule3's own line steps X with its double root kept and the one write ((d + 1) X_now c + r) div (Gamma E_s T) at the one fixed wall is the chain rule between the level and the volume (X'' = (d + 1) X s / Gamma is Gamma U'' = s - (d + 1) Gamma U'^2 exactly: the hill is no act), the inertia e^(2 (d + 1) U) carried by the record's own size (the count of integer states (X, X') per unit of (U, U') is (d + 1)^2 X^2, so no two states collide and the constraint is reached from rest as -e^(-(d + 1) U)), the inverse the same functions at -1, exact at every Node and every interval (the reversibility hand's Theorem 1: every numerator and wall a function of the post-state at the fixed wall; The wall is one kept, no fifth act, no pole). The exponent d + 1 = 4 is the trace's (the hill's one weight for every mix and the exponent one number by the chain rule, K = n E_s T / Gamma), derived and not declared: the loader refuses the key without the stress's trace and under the carried factor, whose wall per Node moves with the clock and folds the run back (loader/interval.volume_rows; the reader's (d) and W5). The level the clocks and the Links' factors read is a reading of the record, the largest a with Gamma^(d + 2) <= X p_0(a)^(d + 1), a search by comparisons on the paces the Node holds over [-Gamma, the clock's last pace) (kind S, as `rule3.largest_below`), no logarithm and no root; the volume of a level the least X whose reading is a, ceil(Gamma^(d + 2) / p_0(a)^(d + 1)), one division (kind D) at the start's conversion alone. Costs named: the Links read volumes (a well e^((d + 1) u) - 1 deep in X, the law's u to first order), the width (X at the clock's last pace Gamma^(d + 2), 7.8 x 10^18 at Gamma 6,000, inside 2^63 for X itself and not for the write's products (d + 1) X c, so the width 92 is the run's, Python's integers), the amplitude bound read against X as against every record, the write's numerator the row's own volume times its sources; the record never stops, X growing while the clock's reading rests at its last pace."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from functools import cache
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import AXES
from event_universe.core.rule3 import division_forward

EXPONENT = (
    AXES + 1
)  # d + 1: the proper volume (Gamma / p_0)^d per proper interval Gamma / p_0, the trace's one weight
LOW = (
    -1
)  # the level reading's search begins at -Gamma, a hill one Gamma deep; its top the clock's last pace

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


@cache
def clock_zero(gamma: int) -> int:
    """The least content at which the clock's pace rounds to 0 at Gamma, about Gamma ln(2 Gamma) (56,352 at 6,000; paces.frozen_content finds the Link's zero before it): the top of the level reading's search, the clock's last pace, found by doubling and halving on the clock's own power (`paces.clock_alone`), the memo untouched, and kept per Gamma (the one search per run, as the loader's constants are)."""
    low, high = 0, 1
    while paces.clock_alone(gamma, high) > 0:
        high += high
    while high - low > 1:
        middle = int(division_forward(low + high, 2, 0)[0])
        if paces.clock_alone(gamma, middle) > 0:
            low = middle
        else:
            high = middle
    return high


def volume_of(gamma: int, levels: Any) -> Any:
    """The volume's level of a level at every Node, X(a) = ceil(Gamma^(d + 2) / p_0(a)^(d + 1)), the least X whose level reading is a (one division per Node, the start's conversion; Gamma at the vacuum's content)."""
    found = np.asarray(levels)
    clocks = np.asarray(paces.clock_of(gamma, found), dtype=object).reshape(-1)
    target = gamma ** (EXPONENT + 1)
    volumes = [
        division_forward(target + int(p) ** EXPONENT - 1, int(p) ** EXPONENT, 0)[0] for p in clocks
    ]
    return np.array([int(x) for x in volumes], dtype=object).reshape(found.shape)


@cache
def bounds_of(gamma: int, amplitude: int) -> tuple[int, int]:
    """The volume's two walls at the amplitude bound A, X(-A) and X(A), the volumes of the deepest and the highest level (the guard `Lattice.bounded` reads the upper alone: downward the carried line ends at the crunch, X at most 0, refused by `level_of`): a row carrying its volume is inside the bound where its X lies between them, the level reading being monotone in X; the lower wall at -Gamma where A passes the hill's depth, the upper at the clock's last pace where A passes it (the level reading's own top, `clock_zero`)."""
    low = int(volume_of(gamma, np.array([max(-amplitude, -gamma)], dtype=object)).reshape(-1)[0])
    top = min(amplitude, clock_zero(gamma) - 1)
    return low, int(volume_of(gamma, np.array([top], dtype=object)).reshape(-1)[0])


@cache
def fill_of(gamma: int, rest: int) -> int:
    """The time line's value beyond a face under the volume form, the rest's volume X(rest) (`volume_of` at the one level): on a board with a sink the rest beyond the face fixes the clock's unit (ALGEBRA.md, The board's interval is no observable), so the Link to the fill reads the vacuum's volume at the declared rest, Gamma at the rest 0; the one Node's fill on every faced board and every grown layer (flux.step_family, growth.resized)."""
    return int(volume_of(gamma, np.array([rest], dtype=object)).reshape(-1)[0])


LEVELS: dict[
    int, dict[int, int]
] = {}  # the level reading's memo per Gamma, the level a found at each volume X so far (`level_of`), cleared at a run's start with the paces' (resonance.clear_memo)


def level_of(gamma: int, volume: Any) -> Any:
    """The level a of the volume X at every Node, the largest a with Gamma^(d + 2) <= X p_0(a)^(d + 1), found by a search by comparisons on the paces the Node holds (kind S), no logarithm and no root (`searched_levels`); the level is one function of the one volume, so the search runs once per distinct volume of the run (the memo `LEVELS`, filled on the volumes the memo lacks and read back at every Node that holds a read volume): the same integers Node by Node as the search at every Node gave (the architect's round of 2026-10-24: the reading re-read many times per interval, the vacuum's one volume on most Nodes of a large board), refused by name where X is at most 0 at a Node."""
    volumes = np.asarray(volume, dtype=object).reshape(-1)
    if (volumes <= 0).any():
        raise ValueError(
            "the volume X is at most 0 at a Node: the level has no reading, refused by name"
        )
    found = LEVELS.setdefault(gamma, {})
    distinct, inverse = np.unique(volumes, return_inverse=True)
    unread = [int(x) for x in distinct.tolist() if int(x) not in found]
    if unread:
        levels = searched_levels(gamma, np.array(unread, dtype=object))
        found.update(zip(unread, (int(a) for a in levels.reshape(-1)), strict=True))
    table = np.array([found[int(x)] for x in distinct.tolist()], dtype=object)
    return table[np.asarray(inverse).reshape(-1)].reshape(np.asarray(volume).shape)


def searched_levels(gamma: int, volumes: Any) -> Any:
    """The level a of each volume X of `volumes` (every X above 0), the largest a with Gamma^(d + 2) <= X p_0(a)^(d + 1), found by a search by comparisons on the paces the Node holds (kind S), no logarithm and no root: from the deepest hill -Gamma upward by doubling steps while the volume is reached (the probes within twice the level's distance from -Gamma, so the clocks' memo fills only as deep as the records stand and never to the clock's last pace for a shallow board), then halving between the last probe reached and the first not (the halving the division act on a count as `rule3.largest_below` has it), never beyond the clock's last pace, each volume's search its own (the probes per volume the same whatever the other volumes beside it); refused by name where X lies below the deepest hill's volume; at the clock's last pace the reading rests while the record grows (the pole never reached by a finite record)."""
    target = gamma ** (EXPONENT + 1)

    def reached(levels: Any) -> Any:
        clocks = np.asarray(paces.clock_of(gamma, levels), dtype=object).reshape(-1)
        return np.array(
            [int(x) * int(p) ** EXPONENT >= target for x, p in zip(volumes, clocks, strict=True)]
        )

    low = np.full(volumes.shape, LOW * gamma, dtype=object)
    top = np.full(volumes.shape, clock_zero(gamma), dtype=object)
    if not reached(low).all():
        raise ValueError(
            f"a volume's level lies below {LOW * gamma}: the level reading is refused by name"
        )
    step = np.full(volumes.shape, 1, dtype=object)
    while True:  # the doubling steps upward, each Node's own, until its probe is not reached
        probe = np.minimum(low + step, top)
        good = reached(probe) & (probe < top)
        if not good.any():
            break
        low, step = np.where(good, probe, low), np.where(good, step + step, step)
    high = np.minimum(low + step, top)
    while (high - low > 1).any():
        middle = np.array(
            [division_forward(a + b, 2, 0)[0] for a, b in zip(low, high, strict=True)], dtype=object
        )
        good = reached(middle)
        low, high = np.where(good, middle, low), np.where(good, high, middle)
    return np.array([int(a) for a in low], dtype=object)


def at_start[Row: DataclassInstance](families: tuple[Row, ...]) -> tuple[Row, ...]:
    """The families as the start reads them, every row at its level: the volume's flag off until the start's rests are solved in the level and converted once (`started`; Lattice.start restores the loader's families after)."""
    return tuple(replace(family, motion_volume=False) for family in families)


def resting(held: Sequence[int], families: Any, loaded: Any) -> list[tuple[int, int]]:
    """The held rows whose rests the start solves, the holders of the content as (index, 0) (`Lattice.start`): every held row that is not the sign's holder and not the gapped row carrying its volume, which the start lays at the vacuum instead, its two levels the empty state's 0 converted once to the volume Gamma with the remainder at the half wall, the seed at rest the design's initial condition (ALGEBRA.md, The carried momentum, the clause of 2026-10-23 on the return hand's derivation read cold by the reader; The closed lattice has no rest: the vacuum is no rest state of a gapped uniform mode, so no rest of its line is solved); `families` the start's rows with the volume's flag off (`at_start`), `loaded` the loader's with it set."""
    return [
        (i, 0)
        for i in held
        if not families[i].wronskian
        and not (loaded[i].motion_volume and loaded[i].pair[0] != loaded[i].pair[1])
    ]


def started(gamma: int, family: Any, line: Any) -> Any:
    """A held row's time line at the end of the start, the record in its own variable: the levels now and before converted once to the volume's levels where the row carries its volume (Rule3's remainder kept), the line itself otherwise."""
    if not family.motion_volume:
        return line
    return line.__class__(volume_of(gamma, line.now), volume_of(gamma, line.before), line.remainder)


def levels_read(gamma: int, lines: Any, carried: bool) -> Any:
    """The level of a held row's time line array as the readings and the paces take it: the array itself where the row carries its level, the level reading where it carries its volume (`carried`, the row's flag `motion_volume`)."""
    return level_of(gamma, lines) if carried else lines
