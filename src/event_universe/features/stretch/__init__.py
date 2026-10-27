"""The volume form of the gap-0 row's time line under the volume form (every board's interval unobservable) (the momentum hand's derivation M12a, 2026-10-22, read cold by the reader: the hypothesis The carried momentum beside The board's interval is no observable, the body of The motion of gravity's row, the symmetric hill its first form kept by name as superseded by derivation): the row carries its time line as the volume's level X = Gamma (Gamma / p_0)^(d + 1) in place of the level a = Gamma U (Gamma at the vacuum's paces, as the clock is), the Node's proper volume (Gamma / p_0)^d per proper interval Gamma / p_0 in its own paces (The paces compose; The write per proper volume and per proper interval), the variable in which the reader's Lagrangian is a constant force, L = (Gamma / (2 (d + 1)^2)) X'^2 + (s_0 / (d + 1)) X, so that Rule3's own line steps X with its double root kept and the one write ((d + 1) X_now c + r) div (Gamma E_s T) at the one fixed wall is the chain rule between the level and the volume (X'' = (d + 1) X s / Gamma is Gamma U'' = s - (d + 1) Gamma U'^2 exactly: the hill is no act), the inertia e^(2 (d + 1) U) carried by the record's own size (the count of integer states (X, X') per unit of (U, U') is (d + 1)^2 X^2, so no two states collide and the constraint is reached from rest as -e^(-(d + 1) U)), the inverse the same functions at -1, exact at every Node and every interval (the reversibility hand's Theorem 1: every numerator and wall a function of the post-state at the fixed wall; The wall is one kept, no fifth act, no pole). The exponent d + 1 = 4 is the trace's (the hill's one weight for every mix and the exponent one number by the chain rule, K = n E_s T / Gamma), derived and not declared: the loader refuses the key without the stress's trace and under the carried factor, whose wall per Node moves with the clock and folds the run back (loader/interval.volume_rows; the reader's (d) and W5). The level the clocks and the Links' factors read is a reading of the record, the largest a with Gamma^(d + 2) <= X p_0(a)^(d + 1), a search by comparisons on the paces the Node holds over [-Gamma, the clock's last pace) (kind S, as `rule3.largest_below`), no logarithm and no root; the volume of a level the least X whose reading is a, ceil(Gamma^(d + 2) / p_0(a)^(d + 1)), one division (kind D) at the start's conversion alone. Costs named: the Links read volumes (a well e^((d + 1) u) - 1 deep in X, the law's u to first order), the width (X at the clock's last pace Gamma^(d + 2), 7.8 x 10^18 at Gamma 6,000, inside 2^63 for X itself and not for the write's products (d + 1) X c, so the width 92 is the run's, Python's integers), the amplitude bound read against X as against every record, the write's numerator the row's own volume times its sources; the record never stops, X growing while the clock's reading rests at its last pace."""

from __future__ import annotations

from functools import cache
from typing import Any

import numpy as np

from event_universe.core import rates
from event_universe.core.rule3 import carries, half
from event_universe.core.spokes import AXES

EXPONENT = (
    AXES + 1
)  # d + 1: the proper volume (Gamma / p_0)^d per proper interval Gamma / p_0, the trace's one weight
LOW = (
    -1
)  # the level reading's search begins at -Gamma, a hill one Gamma deep; its top the clock's last pace


@cache
def rate_zero(gamma: int) -> int:
    """The least content at which the clock's pace rounds to 0 at Gamma, about Gamma ln(2 Gamma) (56,352 at 6,000; paces.frozen_content finds the Link's zero before it): the top of the level reading's search, the clock's last pace, found by doubling and halving on the carried clock (`paces.clock`), and kept per Gamma (the one search per run, as the loader's constants are)."""
    low, high = 0, 1
    while rates.rate(gamma, high) > 0:
        high += high
    while high - low > 1:
        middle = int(half(low + high))
        if rates.rate(gamma, middle) > 0:
            low = middle
        else:
            high = middle
    return high


def stretch_of(gamma: int, levels: Any) -> Any:
    """The volume's level of a level at every Node, X(a) = ceil(Gamma^(d + 2) / p_0(a)^(d + 1)), the least X whose level reading is a (one division per Node, the start's conversion; Gamma at the vacuum's content)."""
    found = np.asarray(levels)
    clocks = np.asarray(rates.rate_of(gamma, found), dtype=object).reshape(-1)
    target = gamma ** (EXPONENT + 1)
    volumes = [carries(target + int(p) ** EXPONENT - 1, int(p) ** EXPONENT) for p in clocks]
    return np.array([int(x) for x in volumes], dtype=object).reshape(found.shape)


LOADS: dict[
    int, dict[int, int]
] = {}  # the level reading's memo per Gamma, the level a found at each volume X so far (`level_of`), a pure function of (Gamma, X), kept for the run


def load_of(gamma: int, volume: Any) -> Any:
    """The level a of the volume X at every Node, the largest a with Gamma^(d + 2) <= X p_0(a)^(d + 1), found by a search by comparisons on the paces the Node holds (kind S), no logarithm and no root (`searched_levels`); the level is one function of the one volume, so the search runs once per distinct volume of the run (the memo `LEVELS`, filled on the volumes the memo lacks and read back at every Node that holds a read volume): the same integers Node by Node as the search at every Node gave (the architect's round of 2026-10-24: the reading re-read many times per interval, the vacuum's one volume on most Nodes of a large board), refused by name where X is at most 0 at a Node."""
    volumes = np.asarray(volume, dtype=object).reshape(-1)
    if (volumes <= 0).any():
        raise ValueError(
            "the volume X is at most 0 at a Node: the level has no reading, refused by name"
        )
    found = LOADS.setdefault(gamma, {})
    distinct, inverse = np.unique(volumes, return_inverse=True)
    unread = [int(x) for x in distinct.tolist() if int(x) not in found]
    if unread:
        levels = searched_loads(gamma, np.array(unread, dtype=object))
        found.update(zip(unread, (int(a) for a in levels.reshape(-1)), strict=True))
    table = np.array([found[int(x)] for x in distinct.tolist()], dtype=object)
    return table[np.asarray(inverse).reshape(-1)].reshape(np.asarray(volume).shape)


def searched_loads(gamma: int, volumes: Any) -> Any:
    """The level a of each volume X of `volumes` (every X above 0), the largest a with Gamma^(d + 2) <= X p_0(a)^(d + 1), found by a search by comparisons on the paces the Node holds (kind S), no logarithm and no root: from the deepest hill -Gamma upward by doubling steps while the volume is reached (the probes within twice the level's distance from -Gamma, so the clocks' memo fills only as deep as the records stand and never to the clock's last pace for a shallow board), then halving between the last probe reached and the first not (the halving the division act on a count as `rule3.largest_below` has it), never beyond the clock's last pace, each volume's search its own (the probes per volume the same whatever the other volumes beside it); refused by name where X lies below the deepest hill's volume; at the clock's last pace the reading rests while the record grows (the pole never reached by a finite record)."""
    target = gamma ** (EXPONENT + 1)

    def reached(levels: Any) -> Any:
        clocks = np.asarray(rates.rate_of(gamma, levels), dtype=object).reshape(-1)
        return np.array(
            [int(x) * int(p) ** EXPONENT >= target for x, p in zip(volumes, clocks, strict=True)]
        )

    low = np.full(volumes.shape, LOW * gamma, dtype=object)
    top = np.full(volumes.shape, rate_zero(gamma), dtype=object)
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
        middle = np.array([half(a + b) for a, b in zip(low, high, strict=True)], dtype=object)
        good = reached(middle)
        low, high = np.where(good, middle, low), np.where(good, high, middle)
    return np.array([int(a) for a in low], dtype=object)
