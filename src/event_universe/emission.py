"""The emission as a source in time (the mathematician's hand with the advisor's second, two hands; the owner's word, everything in a generic form; ALGEBRA.md, The click writes on the lattice (j), the emission): a quantum given to a spread record is laid at the one Node over the emission's declared lifetime tau, one interval at a time, the pair (now, before) of the source advanced by the transition's declared resonance Omega each interval, so that the Node oscillates at Omega for tau intervals and Rule3 radiates it as a wave at Omega, the frequency's width 1 / tau; the total one quantum by the form the source radiates on the width-one guide, SUM_t A_t^2 = (2 / 3) T sin k with cos k = (3 num - 2 den) / den (`radiated_total`, the mathematician's hand with the advisor's second, two hands; the invariant's 2 SUM_t A_t^2 sin Omega = T before it, the two alike at [2, 3]), flat over tau, integers by the division act; the write at the one Node kept literally, no direction drawn, nothing declared beyond the transition's resonance and the emission's lifetime; one `lay` line per interval for the host's tool to cross. The mathematician's hand (at the owner's word): on the integer board a single quantum laid at one Node cannot travel as a spherical wave beyond about 0.28 A_source Links (the spreading wave falls below one level per Node and Rule3 propagates no sub-level wave, the remainder staying at home), so the source in time stands inside a guide (a chain, a tube), where its far Node reads the frequency, and a quantum in the open board travels as a beam, as every shipped world's light does; the beam from the body's Node along a drawn axis, tried in the chain as a head moving one Link per interval with the on-shell phase k - Omega (now alone and the travelling pair), laid 0.34 and 0.68 of a quantum's share and read 0.76 to 0.98 for cos Omega = 0.667 along the beam (the head outruns the wave's phase pace Omega / k = 0.535); the advisor's second: a source in time at one Node cannot feed a beam in the open, Rule3 spreading a one-Node write spherically, a beam of width w holds its amplitude only to the Rayleigh length pi w^2 / lambda, and the one-level floor caps a quantum carried as a wave at T / (2 sin Omega) Nodes, so the open board's emission is by name and not built until the hands converge; an emission at a resonance above the axis band's top (cos Omega below 1 / 3, k = arccos(3 cos Omega - 2) not real) is refused by name at the loader (no axis carries it). The sources stand in the credit's books and at no Node; the engine holds no number and no family name, the resonance and the lifetime the file's. The one lay function of a spread record given whole quanta (`emitted_quantum`) holds the two lays of the one act's lists: the conversion's records out, laid by the count at one Node at the pair the item names, their family's massless pair [den, den], A^2 = count T div 2 (the two hands: a one-Node lay of an open-Link record is a delta over the band and carries no frequency, its share 1 per quantum; `laid_by_count`), and the emission's, the source in time at the item's resonance and span (`laid_increment`); both hands' lines stand as they are."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe import records, registry
from event_universe.core.rule3 import division_forward
from event_universe.features.click import amplitude
from event_universe.lay import laid
from event_universe.loader.derived import FamilyRule, charged
from event_universe.records import record_slice

if TYPE_CHECKING:
    from event_universe.lattice import Lattice
    from event_universe.take import Item


def emitted_lines(family: FamilyRule, record: int = 0) -> list[int]:
    """The lines a quantum born during the run is laid on (`laid_by_count`; ALGEBRA.md, The lay across parts, the owner's word of 2026-10-20): every line of every part of the family's record `record` alike, the symmetric lay, each real line or each plane's two lines of each part, as the file's lay lays one event on every part of the record alike; a born child's own record, its position among its family's children in the meeting's list (`take.Item.record`, `act.born_items`; the clause of 2026-10-24 under Matter's birth from light), the first record otherwise; a holder of the sign's one line, its time line (`records.record_slice`)."""
    if family.held:
        return [0]
    first = record_slice(family, record).start
    return [first + line for line in range(family.parts * family.width)]


def laid_by_count(board: Lattice, item: Item) -> None:
    """A spread record given `delta` whole quanta at the Nodes named by the count (features/click, `amplitude`, the amplitude from the quantum's share over every part's lines laid alike, ALGEBRA.md, The lay across parts), at the pair the item names, a record laid whole at its declared interval at its family's massless pair [den, den], a born child on its own record (`Item.record`: N records of the write step, one per child of the list, ALGEBRA.md, Matter's birth from light, 2026-10-24) (`meeting.laid_whole`; the conversion's records out until 2026-10-20; the two hands: a one-Node lay of an open-Link record is a delta over the band and carries no frequency, its share 1 per quantum), every laid line of the record alike, the symmetric lay (`emitted_lines`; the mathematician's hand: the law's form names no line of a record), A_l^2 = count T div (2 laid) with `laid` the record's real lines or its planes (128 on one line or one plane; 73 on each of three planes, the largest integer whose square is at most 5,461, the share then 0.976 of a quantum at T = 32,768, the file's rounding and not the form's, read beside the count: no three squares sum to 2^14, so no exact equal split exists at a power-of-two T, and the alike lay at that largest integer is laid rather than the unequal (74, 74, 73), the record's own unit absorbing the rounding in the count, the advisor's second): a real line at the two levels alike, (A_l, A_l), the level before the level now turned by the pair's rest rotation, none at the massless pair; a plane on its two lines with the sense the item carries (`Item.sense`, +1 or -1; the conversion's table declared it until 2026-10-20), the real line (A_l, 0) and the sense line (0, sense A_l), the level before the level now turned a quarter in the record's sense as `laid_pairs` lays a plane at the quarter turn [0, den], the one lay at which the count's unit and the charge's unit coincide: the share per plane 3 den (A_l^2 + A_l^2) and the Wronskian re_now im_before - im_now re_before = sense A_l^2, over the planes count W_c and sense count T div 2 to the root's rounding (|W| is at most (|z_now|^2 + |z_before|^2) / 2, so no other lay has both), so that the sign row is written at the Node from the lay on (ALGEBRA.md #the-paces, The sign is the rotation sense; round F of the board, the neutral record's reading, row 2; the worker's four points to both hands and the mathematician's hand); every laid line's remainder at the lay's origin, the half wall, through the one act with no weights (`lay.laid`, a one-Node lay laid as built, its lay lines the write step's); the record's count in the books up by the change."""
    assert item.pair is not None
    born_point(
        board, item.family
    )  # a point's records and rows of the sign born at its first lay (2026-10-24, `Lattice.born_point`)
    family, at = board.families[item.family], board.mask(item.nodes)
    num, den = item.pair
    lines = 1 if family.held else family.laid  # a holder of the sign: its time line alone, not its rows
    parts = 1 if family.held else family.parts  # every part alike, each one n-th of the quantum's share
    size = amplitude(item.delta, board.world.quantum_action, item.pair, lines * parts)
    if family.plane:  # the loader admits a plane given by the count with the table's sense alone
        assert item.sense != 0
        squares = (
            [(size, 0)] * lines
        )  # one plane per record since the family-less file: the rounding is exact where the total is a square
        pairs = [pair for re, im in squares for pair in ((re, -item.sense * im), (im, item.sense * re))]
    else:
        pairs = [(size, int(division_forward(size * num, den, 0)[0]))] * lines
    origin = board.half_wall(item.family)  # a fresh lay by the count: the Node's remainder at the origin
    lines_laid = emitted_lines(family, item.record)  # a born child's own record (2026-10-24)
    for number, (now, was) in zip(lines_laid, pairs * parts, strict=True):
        # the one act with no weights: a one-Node lay's uniform part is the lay itself, laid as built, named
        laid(board, item.family, number, (np.where(at, now, 0), np.where(at, was, 0)), None, origin, at)
    board.credit.counts[item.family] += item.delta


def born_point(board: Lattice, index: int) -> None:
    """A point's records and rows of the sign born at the first birth of the point (2026-10-24, the architect's field view (c), the Boss's order: the lattice's arrays grow per point and not per child, nothing at the Node naming a body): where the family holds no line yet, the loader's count of records (`FamilyRule.records`, the longest list's children of the point, 2), each its lines at the half wall (`records.born_lines`), and for each its own row of the sign at the registry's place (`registry.row_of`): the row's lines at the holder's half wall, its write remainders at half the row's divided wall (`Lattice.row_walls`, `records.divided_walls`, `records.write_origins`), its phase row seeded on the orbit (`records.phase_row`, the amplitude of the start) and its fixed walls, every number the row had at the start to that day, so every state the law reads and every output line are the same as before where no empty record entered a number: an empty record enters every sum as 0, its row's write divides 0 and keeps its remainder, and its phase row is read by no level (the theorem of the zero rows); the two numbers that did depend on the empty records, the draw's digits and the phase frame of a row born into a standing field, named in CHANGELOG.md. Nothing where the point stands already; the interval booked in `Lattice.born_at` for the step back (`unborn_point`) and the replay (`Lattice.step` with no act)."""
    family, state = board.families[index], board.states[index]
    if state.lines or not charged(board.families, index):
        return
    sign = next(r.family for r in family.reads if board.families[r.family].wronskian)
    holder, width, gamma = board.states[sign], board.families[sign].width, board.world.node_clock
    divided = records.divided_walls(board.families[sign], board.row_walls[index], gamma)
    for record in range(family.records):
        state.lines = state.lines + records.born_lines(
            family, board.shape, board.kind, board.half_wall(index)
        )
        place = registry.row_of(board.families, board.states, index, record)
        assert place is not None
        at = place * width
        empty = [
            records.empty_record(board.shape, board.kind, board.half_wall(sign)) for _ in range(width)
        ]
        holder.lines = holder.lines[:at] + empty + holder.lines[at:]
        origins = records.write_origins(divided, board.shape, object)
        holder.write_remainders = holder.write_remainders[:at] + origins + holder.write_remainders[at:]
        seeded = records.phase_row(board.shape, board.kind, gamma, board.amplitude)
        holder.phases = holder.phases[:place] + [seeded] + holder.phases[place:]
        walls = board.fixed_walls[sign]
        board.fixed_walls[sign] = walls[:at] + list(board.row_walls[index]) + walls[at:]
    born = board.born_at.setdefault(board.interval, [])
    if index not in born:
        born.append(index)


def unborn_point(board: Lattice, index: int) -> None:
    """The inverse of `born_point` for the step back: the point's records and their rows of the sign gone, the board the one the interval began with (the records born at a close enter no act of that interval, so the step back runs without them as the step ran)."""
    family, state = board.families[index], board.states[index]
    if not state.lines:
        return
    sign = next(r.family for r in family.reads if board.families[r.family].wronskian)
    holder, width = board.states[sign], board.families[sign].width
    first = registry.row_of(board.families, board.states, index, 0)
    assert first is not None
    count = registry.records_of(family, state.lines)
    at, to = first * width, (first + count) * width
    holder.lines = holder.lines[:at] + holder.lines[to:]
    holder.write_remainders = holder.write_remainders[:at] + holder.write_remainders[to:]
    holder.phases = holder.phases[:first] + holder.phases[first + count :]
    board.fixed_walls[sign] = board.fixed_walls[sign][:at] + board.fixed_walls[sign][to:]
    state.lines = []
