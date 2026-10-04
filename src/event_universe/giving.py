"""The giving as a source in time (the mathematician's hand with the advisor's second, two hands; the owner's word, everything in a generic form; ALGEBRA.md, The click writes on the GameBoard (j), the giving): a quantum given to a spread record is laid at the one Node over the giving's declared lifetime tau, one interval at a time, the pair (now, before) of the source advanced by the transition's declared resonance Omega each interval, so that the Node oscillates at Omega for tau intervals and Rule3 radiates it as a wave at Omega, the frequency's width 1 / tau; the total one quantum by the form the source radiates on the width-one guide, SUM_t A_t^2 = (2 / 3) T sin k with cos k = (3 num - 2 den) / den (`radiated_total`, the mathematician's hand with the advisor's second, two hands; the invariant's 2 SUM_t A_t^2 sin Omega = T before it, the two alike at [2, 3]), flat over tau, integers by the division act; the write at the one Node kept literally, no direction drawn, nothing declared beyond the transition's resonance and the giving's lifetime; one `lay` line per interval for the host's tool to cross. The mathematician's hand (at the owner's word): on the integer board a single quantum laid at one Node cannot travel as a spherical wave beyond about 0.28 A_source Links (the spreading wave falls below one level per Node and Rule3 propagates no sub-level wave, the remainder staying at home), so the source in time stands inside a guide (a chain, a tube), where its far Node reads the frequency, and a quantum in the open board travels as a beam, as every shipped world's light does; the beam from the body's Node along a drawn axis, tried in the chain as a head moving one Link per interval with the on-shell phase k - Omega (now alone and the travelling pair), laid 0.34 and 0.68 of a quantum's share and read 0.76 to 0.98 for cos Omega = 0.667 along the beam (the head outruns the wave's phase pace Omega / k = 0.535); the advisor's second: a source in time at one Node cannot feed a beam in the open, Rule3 spreading a one-Node write spherically, a beam of width w holds its amplitude only to the Rayleigh length pi w^2 / lambda, and the one-level floor caps a quantum carried as a wave at T / (2 sin Omega) Nodes, so the open board's giving is by name and not built until the hands converge; a giving at a resonance above the axis band's top (cos Omega below 1 / 3, k = arccos(3 cos Omega - 2) not real) is refused by name at the loader (no axis carries it). The sources stand in the credit's books and at no Node; the engine holds no number and no family name, the resonance and the lifetime the file's. The one lay function of a spread record given whole quanta (`given_quantum`) holds the two lays of the one act's lists: the conversion's records out, laid by the count at one Node at the pair the item names, their family's massless pair [den, den], A^2 = count T div 2 (the two hands: a one-Node lay of an open-Link record is a delta over the band and carries no frequency, its share 1 per quantum; `laid_by_count`), and the giving's, the source in time at the item's resonance and span (`laid_increment`); both hands' lines stand as they are."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from event_universe import node
from event_universe.core.ports import PORTS, SIDES
from event_universe.core.rule3 import division_fixed_point, division_forward
from event_universe.features.click import (
    SCALE_OF,
    along_cosine,
    amplitude,
    envelope,
    line_total,
    rotated,
    transverse_cosine,
)
from event_universe.lay import division_act_in_time, uniform_removed
from event_universe.loader.derived import FamilyRule, count_wall
from event_universe.loader.keys import Node
from event_universe.reports import lay

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard
    from event_universe.meeting import Item


@dataclass
class Source:
    """A quantum given as a source in time at one Node (the mathematician's hand with the advisor's second, two hands): the record's family, the Node at the file's coordinates, the resonance (num, den) with cos Omega = num / den, the total S = SUM_t A_t^2 of the span (the exact root), the span tau, the intervals laid so far, the span's increments computed whole at the source's start (`increments_of`: A_t with the carry times the reference phasor's value at the scale R, advanced by Omega each interval by the recurrence r_(t+1) = (2 num r_t) div den - r_(t-1)) and, where the span holds a period of the resonance (`holds_period`), corrected by the division act in time so that they lay no uniform mode (`uniform_removed_in_time`), one laid per interval, and the interval the source was begun at (its first increment laid by the click's write step, the rest by `sourced`, one per interval after)."""

    family: int
    at: Node
    resonance: tuple[int, int]
    total: int
    span: int
    laid: int
    increments: list[int]
    begun: int


def line_levels_at(board: GameBoard, index: int, line: int, at: Node) -> list[int]:
    """One line's [now, before, remainder] at a Node named at the file's coordinates, read from its arrays."""
    record, here = board.states[index].lines[line], tuple(np.add(at, board.offset))
    return [int(record.now[here]), int(record.before[here]), int(record.remainder[here])]


def given_quantum(board: GameBoard, item: Item) -> None:
    """A spread record given `delta` whole quanta at the Nodes named, the one lay of the act's lists: by the count at the pair the item names (`laid_by_count`, the conversion's records out at their massless pair) or, where it names none, each a source in time (the mathematician's hand with the advisor's second, two hands; ALGEBRA.md, The click writes on the GameBoard (j), the giving): the quantum is laid at the one Node over the span tau the item carries (the giving's declared lifetime, the frequency's width 1 / tau), the source's level A_t r_t div R added to the record's level now each interval, the reference phasor r advanced by the declared resonance Omega (the pair at the Node then (A_t r_t, A_(t-1) r_(t-1)) by Rule3's own step), the total of the squared amplitudes S = (2 / 3) T sin k, the form the source radiates on the width-one guide, one quantum (`radiated_total`, the mathematician's hand with the advisor's second, two hands, in place of the invariant's S = T / (2 sin Omega), which laid 1.36 and 2.41 quanta at [4, 5] and [9, 10]), laid with the carry, A_t = isqrt((S t) div tau - SUM_(u < t) A_u^2), so that the cumulative sum tracks S t / tau within one level squared and the amplitudes differ by one level now and then; the first interval's level added to the record's first line at once, the following by `sourced` at each interval with their own lay lines; the record's count in the books up by the change at once; a record that held no count at the books' origin gets its unit here, at its first source-in-time lay, the giving's own W_c sin Omega (`born_unit`, the advisor's word), and holds it from there (a lay by the count returns before this and keeps W_c, right for a massless lay, the record staying among the empty; no shipped world lays both on one family)."""
    if item.pair is not None:
        laid_by_count(board, item)
        return
    if item.direction is not None:
        laid_packet(board, item)
        return
    assert item.resonance is not None and item.span > 0  # a lay names its resonance and its span
    action = board.world.quantum_action
    if (
        item.family in board.credit.empty
    ):  # a record empty at the books' origin: its unit the first lay's own
        board.credit.units[item.family] = born_unit(board, item.family, item.resonance)
        board.credit.empty.discard(item.family)
    total = radiated_total(action, item.resonance)
    scale = count_wall(board.families[item.family], action) ** SCALE_OF
    increments, amplitudes = increments_of(total, item.span, item.resonance, scale)
    if holds_period(
        item.span, item.resonance, scale
    ):  # a shorter span is laid as built, its uniform mode named
        increments = uniform_removed_in_time(increments, amplitudes)
    for at in item.nodes:
        for _ in range(item.delta):
            where = (int(at[0]), int(at[1]), int(at[2]))
            source = Source(
                item.family, where, item.resonance, total, item.span, 0, increments, board.tick
            )
            laid_increment(board, source)
            if source.laid < source.span:
                board.credit.sources.append(source)
    board.credit.counts[item.family] += item.delta


def radiated_total(action: int, resonance: tuple[int, int]) -> int:
    """The total of the squared amplitudes S = SUM_t A_t^2 of a source in time laying one quantum (ALGEBRA.md, The giving: one quantum is laid at SUM A_t^2 = (2 / 3) T sin k, the law's line this function reads, closed; the mathematician's hand with the advisor's second, two hands; the integers written from the Ports' names: on the width-one guide the four folded reads fall on the Node itself and two Ports stay open, so den cos k = (6 num - 4 den) / 2 = 3 num - 2 den and the two outgoing waves carry 2 T over Rule3's 3 den): the source in time puts into the record the form it radiates, not its increments' squares; on a guide of width one a point source at Omega radiates two outgoing waves of amplitude 3 A / (2 sin k), the form (3 / 2) S sin Omega / sin k, so one quantum is laid at S = (2 / 3) T sin k, k the guide's wave number at the resonance for massless light in a width-one guide, cos k = (3 num - 2 den) / den; in integers the root on the large number, isqrt((2 T div 3)^2 (den^2 - (3 num - 2 den)^2) div den^2), the fixed point of the division act, (2 / 3) T exactly at [2, 3] (where the invariant's S = T / (2 sin Omega) = 0.671 T already read one quantum within the rounding), 0.611 T at [4, 5] and 0.476 T at [9, 10], where the invariant's S read 1.36 and 2.41 quanta on the chain; on a guide of width w the sum over its transverse modes with their k and weights at the Node, and on the open board the packet lay, both by name and not built."""
    num, den = resonance
    guide = division_forward(PORTS * num - (PORTS - SIDES) * den, SIDES, 0)[0]  # den cos k on the guide
    third = division_forward(SIDES * action, 3, 0)[0]  # 2 T div 3: the two open Ports over Rule3's 3 den
    return division_fixed_point(
        int(division_forward(third * third * (den * den - guide * guide), den * den, 0)[0])
    )


def born_unit(board: GameBoard, index: int, resonance: tuple[int, int]) -> int:
    """The unit of one quantum of a record empty at the books' origin, set at its first lay and held from there (the advisor's word, on the generic node_reader's entry "read once from the books' origin"): the giving's own share, W_c sin Omega, the exact root isqrt((W_c^2 (den^2 - num^2)) div den^2) as the source's total is taken (the root on the large number, within one of the share's unit, where the fixed point of den^2 - num^2 alone would read 4 div 10 for the 0.436 of [9, 10]), the count's line Q(z) = count x W_c sin Omega at the count 1 (the mathematician's hand), so that a born quantum below the half-top energy (sin Omega below 1 / 2) is credited 1 and not 0 by `record_unit`'s default W_c."""
    num, den = resonance
    wall = count_wall(board.families[index], board.world.quantum_action)
    return division_fixed_point(
        int(division_forward(wall * wall * (den * den - num * num), den * den, 0)[0])
    )


def given_lines(family: FamilyRule) -> list[int]:
    """The lines a spread record's given quantum is laid on at the Node by the count (`laid_by_count`): every line of one part of its first record, each real line, or each plane's two lines, laid alike; a holder of the sign's time line alone, its record, light (the giving's source in time writes that first line alone)."""
    return list(range(1 if family.held else family.width))


def laid_by_count(board: GameBoard, item: Item) -> None:
    """A spread record given `delta` whole quanta at the Nodes named by the count (features/click, `amplitude`), at the pair the item names, the conversion's records out at their family's massless pair [den, den] (the two hands: a one-Node lay of an open-Link record is a delta over the band and carries no frequency, its share 1 per quantum), every laid line of the record alike, the symmetric lay (`given_lines`; the mathematician's hand: the law's form names no line of a record), A_l^2 = count T div (2 laid) with `laid` the record's real lines or its planes (128 on one line or one plane; 73 on each of three planes, the fixed point of the division act on 5,461, the share then 0.976 of a quantum at T = 32,768, the file's rounding and not the form's, read beside the count: no three squares sum to 2^14, so no exact equal split exists at a power-of-two T, and the alike lay at the fixed point is laid rather than the unequal (74, 74, 73), the record's own unit absorbing the rounding in the count, the advisor's second): a real line at the two levels alike, (A_l, A_l), the level before the level now turned by the pair's rest rotation, none at the massless pair; a plane on its two lines with the sense the item carries from the conversion's table (`Item.sense`, +1 or -1), the real line (A_l, 0) and the sense line (0, sense A_l), the level before the level now turned a quarter in the record's sense as `laid_pairs` lays a plane at the quarter turn [0, den], the one lay at which the count's unit and the charge's unit coincide: the share per plane 3 den (A_l^2 + A_l^2) and the Wronskian re_now im_before - im_now re_before = sense A_l^2, over the planes count W_c and sense count T div 2 to the root's rounding (|W| is at most (|z_now|^2 + |z_before|^2) / 2, so no other lay has both), so that the sign row is written at the Node from the lay on (ALGEBRA.md #the-paces, The sign is the rotation sense; round F of the board, the neutron reading's row 2; the worker's four points to both hands and the mathematician's hand); every laid line's remainder at the lay's origin, the half wall; the record's count in the books up by the change."""
    assert item.pair is not None
    family, state = board.families[item.family], board.states[item.family]
    gamma, unit, at = board.world.node_clock, board.unit, board.mask(item.nodes)
    num, den = item.pair
    laid = 1 if family.held else family.laid  # a holder of the sign: its time line alone, not its rows
    size = amplitude(item.delta, board.world.quantum_action, item.pair, laid)
    if family.plane:  # the loader admits a plane given by the count with the table's sense alone
        assert item.sense != 0
        pairs = [pair for _ in range(laid) for pair in ((size, 0), (0, item.sense * size))]
    else:
        pairs = [(size, int(division_forward(size * num, den, 0)[0]))] * laid
    origin = division_forward(node.rule_of(family, gamma, 0, None, unit)[2], 2, 0)[0]
    for number, (now, was) in zip(given_lines(family), pairs, strict=True):
        line = state.lines[number]
        state.lines[number] = node.Record(
            line.now + np.where(at, now, 0),
            line.before + np.where(at, was, 0),
            np.where(at, origin, line.remainder),
        )
    board.credit.counts[item.family] += item.delta


def laid_packet(board: GameBoard, item: Item) -> None:
    """The open board's giving (the mathematician's hand; the advisor's seconds, his derivation and his precisions; the owner's word, "a new emitter node_reader also needs to enter"): the given quantum laid from the body's Node as a packet along the drawn direction at one instant, the lay (A) in the message lay's form (ALGEBRA.md, The message lay) with the carry, in place of the source in time where the body stands in the open board (the loader decides by the board's shape against the width, `loader/node_reader_declaration.packet_form`). The direction, an assumption by name, the price of the floor: drawn by the giver among the cube's equivalent directions the board holds with its own generator in the click's one draw (`meeting.gave`), nature's dipole pattern not in it. The shape: `width` Nodes across on each transverse axis, the top-hat around the body's Node (the offsets -(w div 2) through w - 1 - (w div 2)), the one declared number; L slices along, derived from the lifetime and T by the envelope in the energy form (`features/click.envelope`: the energy left R_0 the one-line packet's root T / sin Omega, `features/click.line_total`, the slice's a_t = isqrt((R_t div tau) div w^2), the carry R_(t+1) = R_t - w^2 a_t^2, the lay ending where a_t falls below 1, the deficit below tau level squared per Node), the slice at the distance z from the body carrying the envelope's interval t = z, so the body's Node holds a_0 and the train falls away from it along the drawn direction and travels outward; the invariant SUM over the Nodes of a^2 sin Omega = T within the deficit, one real line carrying the one quantum, its root T / sin Omega twice S, the plane's share per line (`line_total`, one root at the lay, the NodeReader's own act; the mathematician's hand and the advisor's second, two hands). The wave along the axis at the reference scale R = W_c^SCALE_OF (the phasor's scale, the register): 2 R cos k_z = (6 R den_l num) div (num_l den) - 4 R cos(pi / (w + 1)) by the band's line with the transverse mode (`along_cosine`, the loader having refused a width that cannot carry Omega), R cos(k_z z) and R sin(k_z z) by the rotation act (`rotated`, the sine's first level isqrt(R^2 - (R cos k_z)^2), one root at the lay, named), the level now a_t cos(k_z z) and the level before a_t cos(k_z z + Omega) = a_t (R cos(k_z z) num R - R sin(k_z z) s_R) div (den R^2) with s_R = isqrt(R^2 (den^2 - num^2)), the sine's root on the large number at the reference scale, isqrt(R^2 (den^2 - num^2)), one carried rounding, the carrier's phase exact (the floor root isqrt(den^2 - num^2) = 2 for 2.236 at [2, 3] had laid the before level at 0.943 a_t cos(k z + pi / 4), its mean square 8 / 9 of now's, the form short by 0.075 of the top's unit at the one-line root: Worker PACKET-DIAG's reading of the branch), the wave one interval earlier so that the Node oscillates at the transition's resonance and the packet travels outward, the top-hat flat across; the two levels then taken through the message lay's division act over the packet's Nodes where the span holds a period of the resonance (`holds_period`; `features/start.uniform_removed`, in proportion to the envelope's amplitudes, the leftover one unit each at the heaviest), so that now and before each sum to 0 over the packet and the lay carries no uniform mode (on the shipped packet world before's sum -80 over 4,992 Nodes taken out, the share +0.17 percent; a train from a span below the period is steep, 16 slices from 49 at tau = 2, and the act would move its levels by a fifth, so it is laid as built) (ALGEBRA.md, The click writes on the GameBoard (5), the giving lays no uniform mode: the energy-form envelope under the carrier has E(k_z) = SUM e_z e^(i k_z z) other than 0 at every top, the two slits' bump of +24,442 in before the same defect; the mathematician's hand); added to the light record's first line at every Node of the packet, the remainder as it stands; one `lay` line per Node changed for the host's tool to cross (written here, the write step's lines for the body's Node alone standing aside); the record's count in the books up by the change."""
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
            levels, earliers = [], []
            for size, wave, quadrature in zip(amplitudes, waves, quadratures, strict=True):
                levels.append(int(division_forward(size * wave, scale, half_scale)[0]))
                earliers.append(
                    int(
                        division_forward(
                            size * (wave * num * scale - quadrature * sine),
                            scale * scale * den,
                            half_wall,
                        )[0]
                    )
                )
            # the message lay's division act over the packet's Nodes: each level's sum over the train and
            # the cross-section to 0 exactly, in proportion to the envelope (the uniform mode laid none)
            nows = np.array([[lv] * len(section) for lv in levels], dtype=object)
            befores = np.array([[e] * len(section) for e in earliers], dtype=object)
            if holds_period(item.span, item.resonance, scale):  # a shorter span laid as built, named
                weights = np.array([[size] * len(section) for size in amplitudes], dtype=object)
                nows, befores = uniform_removed(nows, weights), uniform_removed(befores, weights)
            for distance in range(len(amplitudes)):
                for across, node_at in enumerate(section):
                    level, earlier = int(nows[distance][across]), int(befores[distance][across])
                    there = list(node_at)
                    there[axis] += sign * distance
                    here = tuple(np.add(there, board.offset))
                    was = [int(now[here]), int(before[here]), int(line.remainder[here])]
                    now[here] += level
                    before[here] += earlier
                    if board.output is not None and (level or earlier):
                        board.output(
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
    half = int(division_forward(width, 2, 0)[0])  # w div 2 by the division act, an index
    span = range(-half, width - half)
    found: list[tuple[int, int, int]] = []
    for first in span:
        for second in span:
            offset = [0, 0, 0]
            across = [a for a in range(3) if a != axis]
            offset[across[0]], offset[across[1]] = first, second
            if all(0 <= int(at[a]) + offset[a] < shape[a] for a in range(3)):
                found.append((offset[0], offset[1], offset[2]))
    return found


def increments_of(
    total: int, span: int, resonance: tuple[int, int], scale: int
) -> tuple[list[int], list[int]]:
    """The span's increments and amplitudes of a source in time, computed whole at its start as the interval-by-interval lay held them: the amplitude A_t = isqrt((S (t + 1)) div tau - the carry) with the carry gaining A_t^2, so that the cumulative sum of the squares tracks S t / tau within one level squared and the amplitudes differ by one level now and then; the reference phasor at the scale R, R cos(Omega t), advanced by the resonance (`advanced`) from r_0 = R and r_(-1) = R cos Omega; the increment A_t r_t div R, rounded half up; one list of each, so that the division act in time reads the whole span before the first interval is laid."""
    num, den = resonance
    phasor = scale
    previous = int(division_forward(scale * num, den, division_forward(den, 2, 0)[0])[0])
    half_scale = division_forward(scale, 2, 0)[0]
    carried, increments, amplitudes = 0, [], []
    for laid in range(span):
        aimed = division_forward(total * (laid + 1), span, 0)[0]
        amplitude = division_fixed_point(int(aimed) - carried)
        increments.append(int(division_forward(amplitude * phasor, scale, half_scale)[0]))
        amplitudes.append(amplitude)
        phasor, previous = advanced(phasor, previous, resonance)
        carried += amplitude * amplitude
    return increments, amplitudes


def holds_period(span: int, resonance: tuple[int, int], unit: int) -> bool:
    """Whether a source's span holds one period of its resonance, tau Omega >= 2 pi, that is cos Omega <= cos(2 pi / tau), with cos(2 pi / tau) = 2 cos^2(pi / tau) - 1 from the rotation act's cos(pi / tau) at the unit (`features/click.transverse_cosine` at the width tau - 1, the message lay's own act; no table and no number of the engine), a span of one interval holding none: the division act in time is exact for any span but takes out most of a span shorter than its period (two constraints on a half-period burst, which is mostly uniform content: 0.005 and 0.15 of the form left at tau = 4 and 6 at [2, 3], 0.98 from tau = 8, the period 7.5; 0.98 from tau = 16 at [5414, 6000], the period 14.1), and nature has no source whose lifetime is below its period; so the correction applies where the span holds a period and a shorter span is laid as built, its uniform mode named here and in the law (the owner's word pending on refusing it at the loader; the mathematician's hand, #1793 comment 5975925032)."""
    if span < 2:
        return False
    num, den = resonance
    cosine = transverse_cosine(span - 1, unit)  # unit cos(pi / tau)
    doubled = int(division_forward(2 * cosine * cosine, unit, 0)[0]) - unit  # unit cos(2 pi / tau)
    return num * unit <= den * doubled


uniform_removed_in_time = division_act_in_time  # the act's name here, kept while its callers read it


def laid_increment(board: GameBoard, source: Source) -> None:
    """One interval of a source: its increment of the interval (`increments_of`, corrected by `uniform_removed_in_time`) added to its record's first line's level now at its Node, the level before and the remainder as they stand (the previous interval's increment, stepped by Rule3, is the pair's own before: adding the phasor's previous value to the level before as well doubled the action, the share reading 1.63 quanta against sin Omega = 0.745, a check made before the lay entered); the interval counted."""
    state, at = board.states[source.family], board.mask((source.at,))
    level = source.increments[source.laid]
    line = state.lines[0]
    state.lines[0] = node.Record(line.now + np.where(at, int(level), 0), line.before, line.remainder)
    source.laid += 1


def advanced(phasor: int, previous: int, resonance: tuple[int, int]) -> tuple[int, int]:
    """One interval of a reference phasor at the resonance (num, den), cos Omega = num / den, Chebyshev's recurrence r_(t+1) = 2 cos Omega r_t - r_(t-1), an identity of the cosine: the turn 2 num r_t div den rounded half up without a carry (one stated choice, the phase error below W / (2 R) over a window of W intervals at the scale R either way; the hands), then the turn minus r_(t-1); returns (r_(t+1), r_t). The giving's phasor and the taker's two reference records (`meeting.gathered`) advance by this one recurrence."""
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
        was = line_levels_at(board, source.family, 0, source.at)
        laid_increment(board, source)
        if board.output is not None:
            name, now = (
                board.families[source.family].name,
                line_levels_at(board, source.family, 0, source.at),
            )
            board.output(lay(board.tick, name, 0, list(source.at), was, now))
        if source.laid < source.span:
            kept.append(source)
    board.credit.sources = kept
