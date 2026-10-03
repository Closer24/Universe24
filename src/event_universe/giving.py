"""The giving as a source in time (the mathematician's 213 (B) and 214 with the advisor's second, two hands; the owner's word of 2026-10-03, 03:24 Israel, everything in a generic form; ALGEBRA.md, The click writes on the GameBoard (j), the giving): a quantum given to a spread record is laid at the one Node over the giving's declared lifetime tau, one interval at a time, the pair (now, before) of the source advanced by the transition's declared resonance Omega each interval, so that the Node oscillates at Omega for tau intervals and Rule3 radiates it as a wave at Omega, the frequency's width 1 / tau; the total one quantum by the invariant 2 SUM_t A_t^2 sin Omega = T, flat over tau at A_t^2 = (T den) div (2 tau s) with s the fixed point of den^2 - num^2 (sin Omega den), integers by the division act; the write at the one Node kept literally, no direction drawn, nothing declared beyond the transition's resonance and the giving's lifetime; one `lay` line per interval for the host's tool to cross. The sources stand in the credit's books and at no Node; the engine holds no number and no family name, the resonance and the lifetime the file's."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from event_universe import node
from event_universe.core.rule3 import division_fixed_point, division_forward
from event_universe.loader.derived import count_wall
from event_universe.loader.keys import Node
from event_universe.reports import lay

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard
    from event_universe.meeting import Item


@dataclass
class Source:
    """A quantum given as a source in time at one Node (the mathematician's 213 (B), #1572 comment 5965054791, and his 220 (c), 5965303134, with the advisor's second, #1563 comment 5965316267, two hands): the record's family, the Node at the file's coordinates, the resonance (num, den) with cos Omega = num / den, the total S = SUM_t A_t^2 of the span (the exact root), the span tau, the intervals laid so far with the sum of their A_t^2 (the carry), and the reference phasor's two values, advanced by Omega each interval by the recurrence r_(t+1) = (2 num r_t) div den - r_(t-1) at the scale R, and the interval the source was begun at (its first increment laid by the click's write step, the rest by `sourced`, one per interval after)."""

    family: int
    at: Node
    resonance: tuple[int, int]
    total: int
    span: int
    laid: int
    carried: int
    phasor: int
    previous: int
    begun: int


SCALE_OF = 2  # the reference phasor's scale, the count's wall times itself: its rounding below one level


def levels_of(board: GameBoard, index: int, line: int, at: Node) -> list[int]:
    """One line's [now, before, remainder] at a Node named at the file's coordinates, read from its arrays."""
    record, here = board.states[index].lines[line], tuple(np.add(at, board.offset))
    return [int(record.now[here]), int(record.before[here]), int(record.remainder[here])]


def given_quantum(board: GameBoard, item: Item) -> None:
    """A spread record given `delta` whole quanta at the Nodes named, each a source in time (the mathematician's 213 (B), #1572 comment 5965054791, and 220, 5965303134, with the advisor's second, #1563 comment 5965316267, two hands; ALGEBRA.md, The click writes on the GameBoard (j), the giving): the quantum is laid at the one Node over the span tau the item carries (the giving's declared lifetime, the frequency's width 1 / tau), the source's level A_t r_t div R added to the record's level now each interval, the reference phasor r advanced by the declared resonance Omega (the pair at the Node then (A_t r_t, A_(t-1) r_(t-1)) by Rule3's own step), the total of the squared amplitudes S = isqrt(T^2 den^2 div (4 (den^2 - num^2))), the exact root of the invariant 2 S sin Omega = T, one quantum's action, laid with the carry, A_t = isqrt((S t) div tau - SUM_(u < t) A_u^2), so that the cumulative sum tracks S t / tau within one level squared and the amplitudes differ by one level now and then; the first interval's level added to the record's first line at once, the following by `sourced` at each interval with their own lay lines; the record's count in the books up by the change at once."""
    assert item.resonance is not None and item.span > 0  # a lay names its resonance and its span
    num, den = item.resonance
    action = board.world.quantum_action
    total = division_fixed_point(
        division_forward(action * action * den * den, 4 * (den * den - num * num), 0)[0]
    )
    scale = count_wall(board.families[item.family], action) ** SCALE_OF
    previous = int(division_forward(scale * num, den, division_forward(den, 2, 0)[0])[0])
    for at in item.nodes:
        for _ in range(item.delta):
            where = (int(at[0]), int(at[1]), int(at[2]))
            source = Source(
                item.family, where, item.resonance, total, item.span, 0, 0, scale, previous, board.tick
            )
            laid_increment(board, source)
            if source.laid < source.span:
                board.credit.sources.append(source)
    board.credit.counts[item.family] += item.delta


def laid_increment(board: GameBoard, source: Source) -> None:
    """One interval of a source: its amplitude A_t = isqrt((S t) div tau - the carry) times the reference phasor's value, A_t r_t div R, added to its record's first line's level now at its Node, the level before and the remainder as they stand (the previous interval's increment, stepped by Rule3, is the pair's own before: adding the phasor's previous value to the level before as well doubled the action, the share reading 1.63 quanta against sin Omega = 0.745, a check made before the lay entered); the carry gains A_t^2, the phasor advances by the resonance and the interval is counted."""
    state, at = board.states[source.family], board.mask((source.at,))
    aimed = division_forward(source.total * (source.laid + 1), source.span, 0)[0]
    amplitude = division_fixed_point(int(aimed) - source.carried)
    scale = count_wall(board.families[source.family], board.world.quantum_action) ** SCALE_OF
    level = division_forward(amplitude * source.phasor, scale, division_forward(scale, 2, 0)[0])[0]
    line = state.lines[0]
    state.lines[0] = node.Record(line.now + np.where(at, int(level), 0), line.before, line.remainder)
    num, den = source.resonance
    turned = division_forward(2 * num * source.phasor, den, division_forward(den, 2, 0)[0])[0]
    source.phasor, source.previous = int(turned) - source.previous, source.phasor
    source.carried, source.laid = source.carried + amplitude * amplitude, source.laid + 1


def sourced(board: GameBoard) -> None:
    """The sources' act at the end of an interval, after the credit and the records' clicks: every source with intervals left lays its interval's pair at its Node (`laid_increment`), one `lay` line each with the line's levels before and after (the host's tool crosses it), and a source whose span is spent leaves the books."""
    kept = []
    for source in board.credit.sources:
        if source.begun == board.tick:  # begun by this interval's click: its first increment laid there
            kept.append(source)
            continue
        was = levels_of(board, source.family, 0, source.at)
        laid_increment(board, source)
        if board.observer is not None:
            name, now = board.families[source.family].name, levels_of(board, source.family, 0, source.at)
            board.observer(lay(board.tick, name, 0, list(source.at), was, now))
        if source.laid < source.span:
            kept.append(source)
    board.credit.sources = kept
