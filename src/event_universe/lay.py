"""The one lay act (ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode; The packet lay (h); The click writes on the lattice (5), the emission lays no uniform mode): every act that writes a record's levels from outside Rule3 is one call of `laid`, the act's change of the level now and of the level before at every Node of the lattice with the lay's weights per Node (the envelope, the amplitudes or the standing levels), or of `laid_in_time`, the source in time's increments over its span. (a) For a massless family (num = den) the uniform part of each level's change is taken out by the one division act (`division_act`): the change's sum over the written Nodes divided back among them in proportion to the weights, the leftover one unit each at the heaviest Nodes in x-major order; in time (`division_act_in_time`) the velocity's sum among the increments in proportion to the amplitudes and the moment among the running sums in proportion to the parabola (t + 1) (span - 1 - t); a gapped family takes no correction. (b) The guard (`guarded`): after the correction the act's change of SUM now and of SUM before over the board (in time, of the sum and of the first moment over the span) is 0, else the act refuses by name with the family and the two changes; the guard compares the act's change of the two sums and never the sums themselves, which Rule3's own floors walk. (c) The write (`written`): the changes added at the Nodes, the remainder of every written Node born at the division's origin where the door names one (the half wall, `node.empty_record`). (d) One `lay` report line per written Node and line (`reports.lay`), the host's tool crossing them back in time. A massless lay handed no weights is laid as built and named by its door: the lay by the count (`emission.laid_by_count`, a one-Node lay whose uniform part is the lay itself) and the absorption's lay of a record declared a NodeDetector (`meeting.relaid`)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import node
from event_universe.core.rule3 import division_forward
from event_universe.reports import lay

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Changes = tuple[Any, Any]  # the act's change of the level now and of the level before over the lattice


def shares_of(total: int, weights: Sequence[int]) -> list[int]:
    """`total` divided among the weights in proportion by the division act, floor by floor, the division's leftover one unit each at the heaviest in their order, so that the shares sum to `total` exactly (the one act of the packet lay's correction, the packet's and the source in time's alike); every share 0 where the total is 0 or the weights are all 0, and 0 at a weight of 0."""
    mass = sum(int(weight) for weight in weights)
    if total == 0 or mass == 0:
        return [0] * len(weights)
    found = [int(division_forward(total * int(w), mass, 0)[0]) if w else 0 for w in weights]
    leftover = total - sum(found)  # the floors fall short by less than one unit per weighted entry
    for i in sorted((i for i, w in enumerate(weights) if w), key=lambda i: -int(weights[i]))[:leftover]:
        found[i] += 1
    return found


def division_act(levels: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """A laid level of a massless record with the uniform mode's content taken out (ALGEBRA.md, The packet lay: the massless row's double root at wave number 0 carries neither level nor velocity, so a laid packet's two levels each sum to 0 over the board): the level's sum over the board divided among the laid Nodes in proportion to the envelope's weights by the division act, floor by floor, the division's leftover one unit each at the heaviest Nodes in x-major order (`shares_of`), so that the sum is exactly 0 and the packet keeps the envelope's taper; a level whose sum is 0 as it stands, or whose weights are all 0, is returned as it is."""
    flat, heavy = (
        np.asarray(levels, dtype=object).ravel().copy(),
        np.asarray(weights, dtype=object).ravel(),
    )
    total = int(flat.sum())
    if total == 0 or int(heavy.sum()) == 0:
        return levels
    for i, change in enumerate(shares_of(-total, [int(w) for w in heavy])):
        flat[i] += change
    return flat.reshape(np.shape(levels))


def division_act_in_time(increments: list[int], amplitudes: list[int]) -> list[int]:
    """The source in time's increments with the uniform mode's content taken out (ALGEBRA.md, The click writes on the lattice (5), the emission lays no uniform mode; the mathematician's hand): on the massless row a level delta added at the one Node at the interval t puts into the double root at wave number 0 the velocity delta and, by the interval s, the level (s - t + 1) delta, so a span of increments leaves the board a uniform velocity SUM delta_t and, once that is 0, a uniform level -SUM t delta_t, growing with no bound in the first case and standing for ever in the second; both are taken out by the division act, exact in the integers: the velocity's sum divided among the increments in proportion to the amplitudes (`shares_of`), then the moment SUM t delta_t divided among the running sums s_0 .. s_(tau - 2) in proportion to the parabola (t + 1) (tau - 1 - t), the increments corrected by the running sums' differences s_t - s_(t - 1) with s_(-1) = s_(tau - 1) = 0, which leave the sum at 0 and move the moment by -SUM s_t exactly; the correction a slope over the span below one level per interval at the shipped lifetimes, where the second difference of the moment, nature's dipole, would have amplified the onset's transient by the band's top over the resonance, 2 (1 - cos pi) / (2 (1 - cos Omega)); increments summing to 0 with the moment 0, or a span of one interval, are returned as they are."""
    found = list(increments)
    velocity = sum(found)
    if velocity:
        found = [d + c for d, c in zip(found, shares_of(-velocity, amplitudes), strict=True)]
    span, moment = len(found), sum(t * d for t, d in enumerate(found))
    if moment and span > 1:
        running = [0, *shares_of(moment, [(t + 1) * (span - 1 - t) for t in range(span - 1)]), 0]
        found = [d + (running[t + 1] - running[t]) for t, d in enumerate(found)]
    return found


def guarded(name: str, kept: bool, first: int, second: int, in_time: bool) -> None:
    """The guard of the act: where the two sums are kept (a massless family under the correction) the act's change of each is 0, else the act refuses by name with the family and the two changes, SUM now and SUM before over the board, or in time the sum and the first moment over the span. The guard reads the act's change and never the sums themselves, which Rule3's own floors walk."""
    if kept and (first or second):
        raise ValueError(
            f"the lay on the massless family {name!r} wakes the zero mode: the act changes "
            + (
                f"the sum over the span by {first} and the first moment over the span by {second}"
                if in_time
                else f"SUM now by {first} and SUM before by {second}"
            )
            + ", and both must be 0 (ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode)"
        )


def corrected(name: str, massless: bool, changes: Changes, weights: Any | None) -> Changes:
    """The act in space before its write: for a massless family with weights the uniform part of each level's change taken out by the one division act (`division_act`), then the guard on the change of SUM now and of SUM before; a gapped family, or a lay handed no weights, as given."""
    now, before = changes
    kept = massless and weights is not None
    if massless and weights is not None:
        now, before = division_act(now, weights), division_act(before, weights)
    sums = (int(np.asarray(now, dtype=object).sum()), int(np.asarray(before, dtype=object).sum()))
    guarded(name, kept, sums[0], sums[1], False)
    return now, before


def laid_in_time(name: str, massless: bool, increments: list[int], amplitudes: list[int]) -> list[int]:
    """The one lay act in time, the source in time's increments over its span as one lay (ALGEBRA.md, The click writes on the lattice (5)): for a massless family the division act in time (`division_act_in_time`, in proportion to the amplitudes) and the guard on the change of the sum and of the first moment over the span; a gapped family's increments as given; each increment then written at its interval by the write step (`written`)."""
    found = division_act_in_time(increments, amplitudes) if massless else list(increments)
    guarded(name, massless, sum(found), sum(t * d for t, d in enumerate(found)), True)
    return found


def written(
    board: Lattice,
    index: int,
    line: int,
    changes: Changes,
    origin: int | None,
    nodes: Any | None = None,
    faced: Any | None = None,
) -> None:
    """The write step of the act, the one place a level is written from outside Rule3: the changes added to the line's two levels at the Nodes `nodes` (the lay's declared Nodes; where none are named, every Node whose change is not 0) but the Nodes `faced`, which the faces write at the step; the remainder at `origin` at the written Nodes where one is given, the division's origin, as it stands otherwise; one `lay` line per written Node whose [now, before, remainder] moved."""
    record = board.states[index].lines[line]
    now, before = (np.asarray(c, dtype=object) for c in changes)
    at = np.asarray((now != 0) | (before != 0) if nodes is None else nodes, dtype=bool)
    if faced is not None:
        at &= ~np.asarray(faced, dtype=bool)
    now, before = np.where(at, now, 0), np.where(at, before, 0)
    kind = record.now.dtype
    laid_line = node.Record(
        np.asarray(record.now + now).astype(kind),
        np.asarray(record.before + before).astype(kind),
        record.remainder if origin is None else np.where(at, origin, record.remainder),
    )
    board.states[index].lines[line] = laid_line
    if board.output is not None:
        name = board.families[index].name
        for here in np.argwhere(at):
            where = tuple(here)
            was = [int(r[where]) for r in (record.now, record.before, record.remainder)]
            after = [int(r[where]) for r in (laid_line.now, laid_line.before, laid_line.remainder)]
            if was != after:
                board.output(
                    lay(
                        board.interval,
                        name,
                        line,
                        [int(a - o) for a, o in zip(here, board.offset, strict=True)],
                        was,
                        after,
                    )
                )


def laid(
    board: Lattice,
    index: int,
    line: int,
    changes: Changes,
    weights: Any | None,
    origin: int | None,
    nodes: Any | None = None,
    faced: Any | None = None,
) -> None:
    """The one lay act on one line of a family's record: the changes corrected for a massless family (`corrected`, the uniform part of each level out in proportion to `weights`), guarded, and written (`written`) at the lay's Nodes with the remainder at `origin`, the Nodes `faced` left to the faces."""
    family = board.families[index]
    num, den = family.pair
    written(
        board, index, line, corrected(family.name, num == den, changes, weights), origin, nodes, faced
    )
