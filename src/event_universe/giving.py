"""The giving as a source in time (the mathematician's 213 (B) and 214 with the advisor's second, two hands; the owner's word of 2026-10-03, 03:24 Israel, everything in a generic form; ALGEBRA.md, The click writes on the GameBoard (j), the giving): a quantum given to a spread record is laid at the one Node over the giving's declared lifetime tau, one interval at a time, the pair (now, before) of the source advanced by the transition's declared resonance Omega each interval, so that the Node oscillates at Omega for tau intervals and Rule3 radiates it as a wave at Omega, the frequency's width 1 / tau; the total one quantum by the invariant 2 SUM_t A_t^2 sin Omega = T, flat over tau at A_t^2 = (T den) div (2 tau s) with s the fixed point of den^2 - num^2 (sin Omega den), integers by the division act; the write at the one Node kept literally, no direction drawn, nothing declared beyond the transition's resonance and the giving's lifetime; one `lay` line per interval for the host's tool to cross. The mathematician's 221 (#1572 comment 5965498522, at the owner's word of 2026-10-03, 06:15 Israel): on the integer board a single quantum laid at one Node cannot travel as a spherical wave beyond about 0.28 A_source Links (the spreading wave falls below one level per Node and Rule3 propagates no sub-level wave, the remainder staying at home), so the source in time stands inside a guide (a chain, a tube), where its far Node reads the frequency, and a quantum in the open board travels as a beam, as every shipped world's light does; the beam from the body's Node along a drawn axis, tried in the chain as a head moving one Link per interval with the on-shell phase k - Omega (now alone and the travelling pair), laid 0.34 and 0.68 of a quantum's share and read 0.76 to 0.98 for cos Omega = 0.667 along the beam (the head outruns the wave's phase pace Omega / k = 0.535); the advisor's second (#1572 comment 5965700585): a source in time at one Node cannot feed a beam in the open, Rule3 spreading a one-Node write spherically, a beam of width w holds its amplitude only to the Rayleigh length pi w^2 / lambda, and the one-level floor caps a quantum carried as a wave at T / (2 sin Omega) Nodes, so the open board's giving is by name and not built until the hands converge; a giving at a resonance above the axis band's top (cos Omega below 1 / 3, k = arccos(3 cos Omega - 2) not real) is refused by name at the loader (221 (2a): no axis carries it). The sources stand in the credit's books and at no Node; the engine holds no number and no family name, the resonance and the lifetime the file's. The one lay function of a spread record given whole quanta (`given_quantum`) holds the two lays of the one act's lists: the conversion's records out, laid by the count at one Node at the pair the item names, their family's massless pair [den, den], A^2 = count T div 2 (the two hands of 2026-10-03, #1572 comments 5964520368 and 5964754600: a one-Node lay of an open-Link record is a delta over the band and carries no frequency, its share 1 per quantum; `laid_by_count`), and the giving's, the source in time at the item's resonance and span (`laid_increment`); both hands' lines stand as they are."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from event_universe import node
from event_universe.core.rule3 import division_fixed_point, division_forward
from event_universe.features.click import (
    SCALE_OF,
    along_cosine,
    envelope,
    exact_total,
    line_total,
    rotated,
    standing,
)
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


def levels_of(board: GameBoard, index: int, line: int, at: Node) -> list[int]:
    """One line's [now, before, remainder] at a Node named at the file's coordinates, read from its arrays."""
    record, here = board.states[index].lines[line], tuple(np.add(at, board.offset))
    return [int(record.now[here]), int(record.before[here]), int(record.remainder[here])]


def given_quantum(board: GameBoard, item: Item) -> None:
    """A spread record given `delta` whole quanta at the Nodes named, the one lay of the act's lists: by the count at the pair the item names (`laid_by_count`, the conversion's records out at their massless pair) or, where it names none, each a source in time (the mathematician's 213 (B), #1572 comment 5965054791, and 220, 5965303134, with the advisor's second, #1563 comment 5965316267, two hands; ALGEBRA.md, The click writes on the GameBoard (j), the giving): the quantum is laid at the one Node over the span tau the item carries (the giving's declared lifetime, the frequency's width 1 / tau), the source's level A_t r_t div R added to the record's level now each interval, the reference phasor r advanced by the declared resonance Omega (the pair at the Node then (A_t r_t, A_(t-1) r_(t-1)) by Rule3's own step), the total of the squared amplitudes S = isqrt(T^2 den^2 div (4 (den^2 - num^2))), the exact root of the invariant 2 S sin Omega = T, one quantum's action (computed as isqrt((T den div 2)^2 div (den^2 - num^2)), the same number for the file's T, a power of two), laid with the carry, A_t = isqrt((S t) div tau - SUM_(u < t) A_u^2), so that the cumulative sum tracks S t / tau within one level squared and the amplitudes differ by one level now and then; the first interval's level added to the record's first line at once, the following by `sourced` at each interval with their own lay lines; the record's count in the books up by the change at once; a record that held no count at the books' origin gets its unit here, at its first source-in-time lay, the giving's own W_c sin Omega (`born_unit`, the advisor's word of 2026-10-03), and holds it from there (a lay by the count returns before this and keeps W_c, right for a massless lay, the record staying among the empty; no shipped world lays both on one family)."""
    if item.pair is not None:
        laid_by_count(board, item)
        return
    if item.direction is not None:
        laid_packet(board, item)
        return
    assert item.resonance is not None and item.span > 0  # a lay names its resonance and its span
    num, den = item.resonance
    action = board.world.quantum_action
    if (
        item.family in board.credit.empty
    ):  # a record empty at the books' origin: its unit the first lay's own
        board.credit.units[item.family] = born_unit(board, item.family, item.resonance)
        board.credit.empty.discard(item.family)
    total = exact_total(action, item.resonance)
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


def born_unit(board: GameBoard, index: int, resonance: tuple[int, int]) -> int:
    """The unit of one quantum of a record empty at the books' origin, set at its first lay and held from there (the advisor's word of 2026-10-03, #1572 comment 5967247080, on the generic detector's entry "read once from the books' origin"): the giving's own share, W_c sin Omega, the exact root isqrt((W_c^2 (den^2 - num^2)) div den^2) as the source's total is taken (the root on the large number, within one of the share's unit, where the fixed point of den^2 - num^2 alone would read 4 div 10 for the 0.436 of [9, 10]), the count's line Q(z) = count x W_c sin Omega at the count 1 (the mathematician's 235, line 2), so that a born quantum below the half-top energy (sin Omega below 1 / 2) is credited 1 and not 0 by `record_unit`'s default W_c."""
    num, den = resonance
    wall = count_wall(board.families[index], board.world.quantum_action)
    return division_fixed_point(
        int(division_forward(wall * wall * (den * den - num * num), den * den, 0)[0])
    )


def laid_by_count(board: GameBoard, item: Item) -> None:
    """A spread record given `delta` whole quanta at the Nodes named by the count (features/click, `standing`), at the pair the item names: the conversion's records out at their family's massless pair [den, den], the two levels alike, A^2 = count T div 2 whatever the family, added to the record's first line, the free row, its remainder at the lay's origin, the half wall; the record's count in the books up by the change (the two hands of 2026-10-03, #1572 comments 5964520368 and 5964754600: a one-Node lay of an open-Link record is a delta over the band and carries no frequency, its share 1 per quantum)."""
    assert item.pair is not None
    family, state = board.families[item.family], board.states[item.family]
    gamma, unit, at = board.world.node_clock, board.unit, board.mask(item.nodes)
    (level, _im), (before, _im_before) = standing(
        item.delta, board.world.quantum_action, item.pair, (1, 0), 1
    )
    origin = division_forward(node.rule_of(family, gamma, 0, None, unit)[2], 2, 0)[0]
    line = state.lines[0]
    now, was = line.now + np.where(at, level, 0), line.before + np.where(at, before, 0)
    state.lines[0] = node.Record(now, was, np.where(at, origin, line.remainder))
    board.credit.counts[item.family] += item.delta


def laid_packet(board: GameBoard, item: Item) -> None:
    """The open board's giving (the mathematician's 224 (1), #1572 comment 5966081562, and 229, 5966424405; the advisor's seconds, 5966129376 with #1563 comment 5966129628, his derivation 5966387795 step 5 and his precisions 5966338551 step 5; the owner's word of 2026-10-03, 09:46 Israel, "a new emitter detector also needs to enter"): the given quantum laid from the body's Node as a packet along the drawn direction at one instant, the lay (A) in the message lay's form (ALGEBRA.md, The message lay) with the carry, in place of the source in time where the body stands in the open board (the loader decides by the board's shape against the width, `loader/instrument.packet_form`). The direction, an assumption by name, the price of the floor: drawn by the giver among the cube's equivalent directions the board holds with its own generator in the click's one draw (`meeting.gave`), nature's dipole pattern not in it. The shape: `width` Nodes across on each transverse axis, the top-hat around the body's Node (the offsets -(w div 2) through w - 1 - (w div 2)), the one declared number; L slices along, derived from the lifetime and T by the envelope in the energy form (`features/click.envelope`: the energy left R_0 the one-line packet's root T / sin Omega, `features/click.line_total`, the slice's a_t = isqrt((R_t div tau) div w^2), the carry R_(t+1) = R_t - w^2 a_t^2, the lay ending where a_t falls below 1, the deficit below tau level squared per Node), the slice at the distance z from the body carrying the envelope's interval t = z, so the body's Node holds a_0 and the train falls away from it along the drawn direction and travels outward; the invariant SUM over the Nodes of a^2 sin Omega = T within the deficit, one real line carrying the one quantum, its root T / sin Omega twice S, the plane's share per line (`line_total`, one root at the lay, the instrument's own act; the mathematician's 242 section 1, #1572 comment 5967687794, and the advisor's second, 5967838095 section 1, two hands). The wave along the axis at the reference scale R = W_c^SCALE_OF (the phasor's scale, the register): 2 R cos k_z = (6 R den_l num) div (num_l den) - 4 R cos(pi / (w + 1)) by the band's line with the transverse mode (`along_cosine`, the loader having refused a width that cannot carry Omega), R cos(k_z z) and R sin(k_z z) by the rotation act (`rotated`, the sine's first level isqrt(R^2 - (R cos k_z)^2), one root at the lay, named), the level now a_t cos(k_z z) and the level before a_t cos(k_z z + Omega) = a_t (R cos(k_z z) num R - R sin(k_z z) s_R) div (den R^2) with s_R = isqrt(R^2 (den^2 - num^2)), the sine's root on the large number at the reference scale, isqrt(R^2 (den^2 - num^2)), one carried rounding, the carrier's phase exact (the floor root isqrt(den^2 - num^2) = 2 for 2.236 at [2, 3] had laid the before level at 0.943 a_t cos(k z + pi / 4), its mean square 8 / 9 of now's, the form short by 0.075 of the top's unit at the one-line root: Worker PACKET-DIAG's reading of the branch), the wave one interval earlier so that the Node oscillates at the transition's resonance and the packet travels outward, the top-hat flat across; added to the light record's first line at every Node of the packet, the remainder as it stands; one `lay` line per Node changed for the host's tool to cross (written here, the write step's lines for the body's Node alone standing aside); the record's count in the books up by the change."""
    assert item.resonance is not None and item.span > 0 and item.width and item.direction is not None
    num, den = item.resonance
    family, state, action = (
        board.families[item.family],
        board.states[item.family],
        board.world.quantum_action,
    )
    scale = count_wall(family, action) ** SCALE_OF
    doubled = along_cosine(family.pair, item.resonance, item.width, scale)
    assert doubled is not None  # the loader refused a width that cannot carry Omega
    axis, sign = item.direction
    width, shape = item.width, board.world.shape
    sine = division_fixed_point(scale * scale * (den * den - num * num))  # R sin Omega den, at the scale
    half_scale = division_forward(scale, 2, 0)[0]
    half_wall = division_forward(scale * scale * den, 2, 0)[0]
    for at in item.nodes:
        for _ in range(item.delta):
            section = [
                tuple(
                    int(at[a]) + (offset[k] if a != axis else 0)
                    for a, k in zip(range(3), (0, 1, 2), strict=True)
                )
                for offset in _offsets(axis, width, at, shape)
            ]
            amplitudes = envelope(line_total(action, item.resonance), item.span, len(section))
            cosine = int(division_forward(doubled, 2, 0)[0])
            waves = rotated(scale, cosine, doubled, scale, len(amplitudes))
            quadratures = rotated(
                0, division_fixed_point(scale * scale - cosine * cosine), doubled, scale, len(amplitudes)
            )
            line = state.lines[0]
            now, before = line.now.copy(), line.before.copy()
            for distance, (amplitude, wave, quadrature) in enumerate(
                zip(amplitudes, waves, quadratures, strict=True)
            ):
                level = int(division_forward(amplitude * wave, scale, half_scale)[0])
                earlier = int(
                    division_forward(
                        amplitude * (wave * num * scale - quadrature * sine),
                        scale * scale * den,
                        half_wall,
                    )[0]
                )
                for node_at in section:
                    there = list(node_at)
                    there[axis] += sign * distance
                    here = tuple(np.add(there, board.offset))
                    was = [int(now[here]), int(before[here]), int(line.remainder[here])]
                    now[here] += level
                    before[here] += earlier
                    if board.observer is not None and (level or earlier):
                        board.observer(
                            lay(
                                board.tick,
                                family.name,
                                0,
                                there,
                                was,
                                [int(now[here]), int(before[here]), was[2]],
                            )
                        )
            state.lines[0] = node.Record(now, before, line.remainder)
    board.credit.counts[item.family] += item.delta


def _offsets(axis: int, width: int, at: Node, shape: Node) -> list[tuple[int, int, int]]:
    """The cross-section's offsets from the body's Node on the two axes across the packet's axis, the top-hat of `width` Nodes around the Node, -(w div 2) through w - 1 - (w div 2) on each, kept where the Node stands on the board (the loader admitted the whole section, so every one is)."""
    span = range(-(width // 2), width - width // 2)
    found: list[tuple[int, int, int]] = []
    for first in span:
        for second in span:
            offset = [0, 0, 0]
            across = [a for a in range(3) if a != axis]
            offset[across[0]], offset[across[1]] = first, second
            if all(0 <= int(at[a]) + offset[a] < shape[a] for a in range(3)):
                found.append((offset[0], offset[1], offset[2]))
    return found


def laid_increment(board: GameBoard, source: Source) -> None:
    """One interval of a source: its amplitude A_t = isqrt((S t) div tau - the carry) times the reference phasor's value, A_t r_t div R, added to its record's first line's level now at its Node, the level before and the remainder as they stand (the previous interval's increment, stepped by Rule3, is the pair's own before: adding the phasor's previous value to the level before as well doubled the action, the share reading 1.63 quanta against sin Omega = 0.745, a check made before the lay entered); the carry gains A_t^2, the phasor advances by the resonance and the interval is counted."""
    state, at = board.states[source.family], board.mask((source.at,))
    aimed = division_forward(source.total * (source.laid + 1), source.span, 0)[0]
    amplitude = division_fixed_point(int(aimed) - source.carried)
    scale = count_wall(board.families[source.family], board.world.quantum_action) ** SCALE_OF
    level = division_forward(amplitude * source.phasor, scale, division_forward(scale, 2, 0)[0])[0]
    line = state.lines[0]
    state.lines[0] = node.Record(line.now + np.where(at, int(level), 0), line.before, line.remainder)
    source.phasor, source.previous = advanced(source.phasor, source.previous, source.resonance)
    source.carried, source.laid = source.carried + amplitude * amplitude, source.laid + 1


def advanced(phasor: int, previous: int, resonance: tuple[int, int]) -> tuple[int, int]:
    """One interval of a reference phasor at the resonance (num, den), cos Omega = num / den, Chebyshev's recurrence r_(t+1) = 2 cos Omega r_t - r_(t-1), an identity of the cosine: the turn 2 num r_t div den rounded half up without a carry (one stated choice, the phase error below W / (2 R) over a window of W intervals at the scale R either way; the hands of 2026-10-03, #1572 comments 5966338551 and 5966387795), then the turn minus r_(t-1); returns (r_(t+1), r_t). The giving's phasor and the taker's two reference records (`meeting.gathered`) advance by this one recurrence."""
    num, den = resonance
    turned = division_forward(2 * num * phasor, den, division_forward(den, 2, 0)[0])[0]
    return int(turned) - previous, phasor


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
