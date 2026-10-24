"""The Node's acts on every family's NodeState over the lattice (records.py: a flat list of lines of dimension one and the law's numbers and nothing else), each a pure function of whole-board arrays with every neighbour read through a Port (core/ports.py), one Link's reach for every act (ALGEBRA.md #the-interval, the dependency radius): the read, the content at the Node into the composed clock and the Node's pace, the clock twice, with each Link's own factor from its tension (#the-paces; the guard once at load), the rule's integers of that read for the step (`rule_of`, core/rule3.rule_integers; the step itself is flux.py, Rule3 in flux form on every line, #the-line, #the-direction), the sign's levels a turned record reads, the phase act on the holder's phase lines (features/phase) and the one write per held line (#the-primitives, the row "the held write"). The step knows no family, no dimension and no name: it receives lines with their rule, their sources and their readers (the loader's grouping, loader/derived.py)."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import AXES, PORTS, Wrap, arrival
from event_universe.core.rule3 import Rule, division_back, division_forward, rule_integers
from event_universe.features import phase, volume
from event_universe.features.held_write import held_write
from event_universe.features.read import (
    READS,
    axis_paces,
    content_of,
    link_factors,
    link_tensions,
    paces_guard,
    plain,
    read_again,
)
from event_universe.loader.derived import FamilyRule, row_of, turns, weight_of
from event_universe.plane import (
    Angles,
    fold_guard,
    frame_signs,
    link_guard,
    link_levels,
    link_wall,
    odd_links,
)
from event_universe.records import Families, Record, Rulers, States, level_at, phase_lines, row_levels

if TYPE_CHECKING:
    from event_universe.lattice import Lattice
    from event_universe.loader.world import World

Factors = tuple[Any, ...]  # the factor Q_ij of a Node's six Links in Port order, in the unit G^2


def read_key(
    name: Callable[..., Any],
    index: int,
    families: Families,
    states: States,
    direction: int,
    gamma: int,
    record: int,
) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """The read memo's key for one reading (`name`: the reading's own function, read_lines, read or rulers, no word of its own) of one record of a family in a direction (features/read READS; one entry per key, so the memo holds one board's records and grows with no interval), and the objects the reading takes, compared by identity: the families, the states and every record of the rows the family reads (every record the same object means every integer the same, a record never written in place)."""
    reads = [r for r in families[index].reads if not families[r.family].rotation]
    key = (name, index, record, direction, gamma)
    return key, (families, states, *(line for r in reads for line in states[r.family].lines))


def read_lines(
    index: int, families: Families, states: States, direction: int, gamma: int, record: int = 0
) -> tuple[Any, list[Any]]:
    """The lines a record's read takes at the interval's start in `direction` (ALGEBRA.md #the-paces, Every row reads the content): the content c = SUM over its reads of the holders acting on the pace of (weight x the read family's time line at the level the step in `direction` starts from, `level_at`), a held row of the content reading its own level among them and a holder of the sign read as the sum of every row but the record's own (`row_levels`, `derived.row_of`), and per read row carrying axis lines its weight and its three axis lines at the same level; the integer 0 and no axis lines where it reads nothing (the plain rule at Gamma); a holder declaring the rotation enters no pace (`turning`); the read made once per interval on the same records and given again to every act that reads them (features/read READS, the architect's second round of 2026-10-24: the same integers, read once)."""
    reads = [r for r in families[index].reads if not families[r.family].rotation]
    key, taken = read_key(read_lines, index, families, states, direction, gamma, record)
    if (kept := read_again(key, taken)) is not None:
        return kept  # the same records read again: the read made before (features/read READS)
    own = row_of(families, index, record)
    levels = [
        plain(
            volume.levels_read(
                gamma,
                row_levels(families[r.family], states[r.family].lines, 0, direction, own),
                families[r.family].motion_volume,
            ),
            families[r.family].wronskian,
        )
        for r in reads
    ]  # a holder of the sign's level, every row but the reader's own, as the plain read takes it: its size
    content = content_of([(r.weight, level) for r, level in zip(reads, levels, strict=True)])
    rows = [r for r in reads if families[r.family].axes]
    found = (
        content,
        [
            (r.weight, [level_at(states[r.family].lines[1 + a], direction) for a in range(3)])
            for r in rows
        ],
    )
    READS[key] = (taken, found)
    return found


def read(
    index: int,
    families: Families,
    states: States,
    direction: int,
    wrap: Wrap,
    gamma: int,
    unit: int,
    record: int = 0,
) -> tuple[Any, Factors]:
    """The read of a record of a family at the interval's start (ALGEBRA.md #the-paces, Every row reads the content; The clock is the Node's, the tension is the Link's; #the-interval, the dependency radius): the content at every Node (`read_lines`, every sign row but the record's own) and the factor of each of its six Links, Q_ij from the Link's tension, the read rows' axis lines at its two ends, (weight x (aa_i + aa_j) + 1) div 2, the neighbour's line read through the Port the arrival is read through, one number per Link read the same from both ends, booked once per Link in the unit G^2 (features/read, `link_tensions`, `link_factors`); the integer 0 at the Node and G^2 on every Link where it reads nothing (the plain rule at Gamma); no floor, no clamp and no guard in the interval; the same levels read back, so the inverse reads the same paces."""
    if not any(not families[r.family].rotation for r in families[index].reads):
        factors: Factors = (unit * unit,) * PORTS
        content: Any = 0
    else:
        key, taken = read_key(read, index, families, states, direction, gamma, record)
        if (kept := read_again(key, taken)) is None:
            content, axes = read_lines(index, families, states, direction, gamma, record)
            factors = link_factors(gamma, unit, link_tensions(axes, wrap, gamma))
            READS[key] = (taken, (content, list(factors)))
        else:
            content, factors = kept[0], tuple(kept[1])
    return content, factors


def rulers(
    index: int,
    families: Families,
    states: States,
    direction: int,
    wrap: Wrap,
    gamma: int,
    record: int = 0,
) -> Rulers:
    """The paces a record's read gives it at every Node for the write's factor (ALGEBRA.md, The write per proper volume and per proper interval; The paces compose): the clock p_0 from its content and its pace along each axis, p_a = p_i (q_(+a) + q_(-a)) / (2 Gamma), the Node's pace p_i = p_0^2 / Gamma times the mean of its two a-Links' factors from their tensions, one reading per axis through its two Ports (`features/read`, `axis_paces`), the ruler h_a = p_0 / p_a; Gamma on the clock and on every axis where the family reads nothing (every factor 1 at the vacuum's paces); read at the level the step in `direction` starts from, the same numbers read back."""
    if not any(not families[r.family].rotation for r in families[index].reads):
        return gamma, (gamma, gamma, gamma)
    key, taken = read_key(rulers, index, families, states, direction, gamma, record)
    if (kept := read_again(key, taken)) is not None:
        return kept[0], tuple(kept[1])
    content, axes = read_lines(index, families, states, direction, gamma, record)
    clock, pace = paces.node_paces(gamma, content)
    found = clock, axis_paces(gamma, pace, link_tensions(axes, wrap, gamma))
    READS[key] = (taken, (found[0], list(found[1])))
    return found


def rulers_of(
    board: Lattice, sources: Iterable[tuple[int, int]], direction: int
) -> dict[tuple[int, int], Rulers]:
    """Every record of quanta's paces at the interval's start in `direction`, keyed by its sourcing (the family's index and the record), and beside them every held row's own paces keyed (held, row), the wall of a row that reads the content (`records.wall_rulers`; ALGEBRA.md, The one Node, the clause of 2026-10-23): a held row's index is no quanta family's, so the keys never meet."""
    families, states, wrap, gamma = board.families, board.states, board.wrap, board.world.node_clock
    found = {s: rulers(s[0], families, states, direction, wrap, gamma, s[1]) for s in sources}
    for index in board.held:
        for row in range(families[index].records):
            found[(index, row)] = rulers(index, families, states, direction, wrap, gamma, row)
    return found


def turning(
    index: int, families: Families, states: States, direction: int, record: int = 0
) -> Angles | None:
    """The sign's levels a turned record reads (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; features/phase): from every holder it reads that declares the rotation, the time level SUM of (weight x the holder's time line summed over every row but the record's own, `row_levels`), the potential whose difference across each Link iterates the Link's phase pair (`phased`, n_ij = rounded(L(i) p_0(i), Gamma) - rounded(L(j) p_0(j), Gamma), each end's level at its own clock, L(i) - L(j) at the vacuum's clock, Part H, MUST 3: the angle per act is theta_0 = 1 / Gamma and the field the count of acts, the mathematician's item (g)), and each axis's SUM of (weight x the holder's odd line a over the same rows) as it is, at every Node, at the level the step in `direction` starts from (the same number read back, so the inverse is explicit); None where the family's record is not turned (`derived.turns`: a one-part family, or every holder acting on the pace)."""
    if not turns(families, index):
        return None
    reads = [r for r in families[index].reads if families[r.family].rotation]
    own = row_of(families, index, record)
    levels = [
        content_of(
            [
                (r.weight, row_levels(families[r.family], states[r.family].lines, line, direction, own))
                for r in reads
            ]
        )
        for line in range(1 + AXES)  # the time line and the three axis lines
    ]
    return levels[0], (levels[1], levels[2], levels[3])


def sign_holder(index: int, families: Families) -> int:
    """The one holder of the sign under the rotation a turned family reads, whose phase lines its records read (`phased`, `step_records`); the energy line's holder (`derived.energy_line`); refused by name where a family reads more than one (the Link's phase is one pair per Link, one holder's)."""
    holders = [r.family for r in families[index].reads if families[r.family].rotation]
    if len(holders) != 1:
        raise ValueError(
            f"{families[index].name!r} reads {len(holders)} holders under the rotation, and the Link's phase "
            "is one pair per Link, one holder's: a plane reads one holder of the sign under the rotation"
        )
    return holders[0]


PHI = (
    2 * AXES + AXES
)  # the Node's phase row among a row's phase lines, after the six pair lines and the three count lines


def clocked_potentials(
    index: int, families: Families, states: States, direction: int, wrap: Wrap, gamma: int
) -> dict[int, Any]:
    """The clocked potential of every row of the sign beyond the free row at every Node, c = rounded(L p_0 / Gamma) (`paces.turn_factor`, kind D; ALGEBRA.md, The turn per proper interval): L the holder's time level summed over every row but the row's own reader's (`row_levels`, at the weight the reader reads with, `weight_of`; No record reads its own write of the sign) and p_0 the reader's clock at that Node (`rulers`), both at the level `direction` names, 1 the level now and -1 the level before, the Node's own levels and nothing of the board; the write of the Node's phase row (`phased`)."""
    family, state = families[index], states[index]
    readers = {
        row_of(families, reader, record): (reader, record)
        for reader, other in enumerate(families)
        if turns(families, reader) and weight_of(index, other)
        for record in range(other.records)
    }
    found: dict[int, Any] = {}
    for row, lines in enumerate(state.phases):
        if row == 0 or row not in readers or not lines:
            continue
        reader_index, reader_record = readers[row]
        potential = weight_of(index, families[reader_index]) * row_levels(
            family, state.lines, 0, direction, row
        )
        clock = rulers(reader_index, families, states, direction, wrap, gamma, reader_record)[0]
        found[row] = np.asarray(paces.turn_factor(potential, clock, gamma), dtype=object)
    return found


def phase_counts(
    index: int, families: Families, states: States, direction: int, wrap: Wrap, gamma: int
) -> dict[int, list[Any]]:
    """The count every Link of the holder's rows stands at in the state the Node holds (ALGEBRA.md, The turn per proper interval, the centred count): per row, the Node's K = 2 (Phi_now - Phi_before) - c, c the row's clocked potential at the level `direction` names (`clocked_potentials`), which is Phi_next - Phi_before of the Rule3 triple whose write is c, twice the trapezoid sum of the clocked potential to the triple's centre (at the end of an interval, c at the level before, the write the act just took: K(m + 1); at a turned Node after the swap at the top the same reading gives -K(m + 1); after the inverse of the act, c at the level now: K(m)); per axis the Link's count K_i - s K_(i + a), the two ends' difference read in one frame (`frame_signs`: s = +1 where the two ends' phase rows carry one remainder at the wall 2 and -1 where one end is time-reversed by the swap and the other not, the neighbour's K negated into the Node's frame), 0 beyond a face (`arrival`), the pair at -K the conjugate of the pair at +K (features/phase `signed_read`). In the frame every record was born in the swap exchanges a plane's two levels like every plain line's (conj(conj z) = z, -(-K) = K), so the pair the two ends read is one and the same whichever end turned, and the inverse of a split top is exact at the unturned neighbours (M25; the former reading of a mixed Link, -K_i - K_j, carried the pair by about 2 |K| acts at the fire and the inverse read it where the forward step read K_i - K_j)."""
    found: dict[int, list[Any]] = {}
    for row, c in clocked_potentials(index, families, states, direction, wrap, gamma).items():
        phi = states[index].phases[row][PHI]
        k = 2 * (np.asarray(phi.now, dtype=object) - np.asarray(phi.before, dtype=object)) - c
        signs = frame_signs(phi.remainder, wrap)
        counts = []
        for axis in range(AXES):
            counts.append(k - signs[2 * axis] * arrival(k, axis, 1))
        found[row] = counts
    return found


def phase_carried(
    index: int, states: States, counts: dict[int, list[Any]], gamma: int
) -> list[list[Record]]:
    """The holder's phase lines with every row's pairs carried along the one orbit from the seed from the count standing (the row's count lines, the cache the planes read, plane.phase_links) to the count `counts` names (features/phase `Orbit.pairs_at`: the pair at the count |K'| along the one orbit from the seed, the checkpoint at or below it carried by the rest, the same integers as `iterate` at the line's unit 2 Gamma over |K'| - |K| acts, forward where the size grows, the inverse act where it shrinks, bit for bit in either direction; a state the lattice did not seed carried by `iterate` itself), the count lines then at `counts`, the Node's phase row as it is; the state untouched."""
    found: list[list[Record]] = []
    for row, lines in enumerate(states[index].phases):
        if row not in counts:
            found.append(list(lines))
            continue
        phased_lines: list[Record] = []
        count_lines: list[Record] = []
        orbit = phase.orbit_of(states[index])
        for axis in range(AXES):
            cosine, sine, standing = lines[2 * axis], lines[2 * axis + 1], lines[2 * AXES + axis]
            reached = np.asarray(counts[row][axis])
            if orbit is not None:  # the pairs at |K'| along the one orbit, the same integers
                lines_standing = (
                    (cosine.now, cosine.before, cosine.remainder),
                    (sine.now, sine.before, sine.remainder),
                )
                pair = orbit.pairs_at(
                    np.abs(reached), np.abs(standing.now), lines_standing, cosine.now.dtype
                )
            else:
                moved = np.abs(reached) - np.abs(np.asarray(standing.now, dtype=object))
                pair = phase.iterate(
                    (
                        (cosine.now, cosine.before, cosine.remainder),
                        (sine.now, sine.before, sine.remainder),
                    ),
                    moved,
                    phase.unit(gamma),
                )
            phased_lines += [Record(*(np.asarray(a) for a in line)) for line in pair]
            count_lines.append(Record(reached, np.asarray(0 * reached), np.asarray(0 * reached)))
        found.append(phased_lines + count_lines + [lines[PHI]])
    return found


def phase_rows(index: int, states: States, potentials: dict[int, Any], direction: int) -> None:
    """The Node's phase row of every row of the sign stepped by Rule3 with the write c = `potentials` (the clocked potential at the level now, the interval's start in either direction; `clocked_potentials`), mass 0, no Links, the wall 2 with the write 2 c by the carried division (the clocked potential is the law's one rounding, so (2 c + r) div 2 = c and the remainder r stands, 0 from the start; the remainder is the record's frame, complemented at the swap at the top like every remainder, 1 at a record time-reversed an odd number of times, `frame_signs`): forward Phi_next = 2 Phi_now - Phi_before + c, the row then (Phi_next, Phi_now); backward Phi_prev = 2 Phi_before - Phi_now + c, the row then (Phi_before, Phi_prev), bit for bit (ALGEBRA.md #the-direction)."""
    for row, c in potentials.items():
        lines = list(states[index].phases[row])
        phi = lines[PHI]
        now, before = np.asarray(phi.now, dtype=object), np.asarray(phi.before, dtype=object)
        act = division_forward if direction == 1 else division_back
        write, kept = act(2 * c, 2, np.asarray(phi.remainder, dtype=object))
        kind = phi.now.dtype  # the board's kind, the loader's choice by the width
        remainder = np.asarray(kept, dtype=kind)
        if direction == 1:
            lines[PHI] = Record(np.asarray(2 * now - before + write, dtype=kind), phi.now, remainder)
        else:
            lines[PHI] = Record(phi.before, np.asarray(2 * before - now + write, dtype=kind), remainder)
        states[index].phases[row] = lines


def phased(
    index: int, families: Families, states: States, direction: int, wrap: Wrap, gamma: int
) -> list[list[Record]]:
    """The phase act of one interval on a holder of the sign under the rotation (features/phase; the mathematician's item (g) and the two hands' item (i); ALGEBRA.md, The sign holder rotates the two-part record, The turn per proper interval; the centred count, the owner's decision of 2026-10-23, the phase hand's derivation M23): for every row of the sign beyond the free row the Node carries its phase row Phi, a Rule3 record whose write per interval is the row's clocked potential c = rounded(L p_0 / Gamma) at the level now, the interval's start in either direction (`clocked_potentials`, `phase_rows`: Phi_next = 2 Phi_now - Phi_before + c), and the Link's count is the two ends' difference of the Node's K = Phi_next - Phi_before = 2 (Phi_now - Phi_before) + c, twice the trapezoid sum of the clocked potential to the triple's centre, K_ij = K_i - K_(i + a) (`phase_counts`; the former reading, to 2026-10-23, the left sum N_ij moved by c_i - c_j per interval, read at the step's start), by which each axis's Link's cosine and sine lines take the acts that carry the pair along the one orbit from the seed to the size of the count reached (`phase_carried`; the pair at X e^(i |K| theta_0 / 2), read with the count's sign, the pair at -K the conjugate of the pair at +K, so that the cube's 48 map the remainders as they map the levels and the Node's time reversal, the swap at the top, is the pair's conjugate exactly, swap.py); forward, and at `direction` -1 the row stepped back and the pairs carried back to K(m), bit for bit, once every line stands at the interval's start again (`Lattice.step_inverse`); one Link's reach, the two ends; no count line of its own, the row's three count lines the cache of the Link's count the planes read (plane.phase_links). Returns the rows' phase lines after the act, the state's phase rows stepped."""
    potentials = clocked_potentials(index, families, states, 1, wrap, gamma)
    phase_rows(index, states, potentials, direction)
    counts = phase_counts(index, families, states, direction, wrap, gamma)
    return phase_carried(index, states, counts, gamma)


def guarded(index: int, families: Families, states: States, gamma: int, wrap: Wrap, unit: int) -> None:
    """The guard once at load (ALGEBRA.md #the-paces, The guard): every record's read of the initial state checked as squares, the content below the Link's zero (the lower side, a frozen clock refused by name) and p^2 (den + num) <= 2 den Gamma^2 at every Node on the clock, on the Node's pace and on each Link's pace p_i^2 Q_ij / G^2, refused by name outside; a family that reads nothing stands at Gamma, inside; no act of the interval reads it (features/read). A turned record's Links alike (`plane.link_guard`): each Link's two ends' sum n_ij of the sign's odd lines within 4 Gamma, a tangent half-angle at most 1, the guard on n the fold's Link keeps (`plane.sign_pairs`); the time level is guarded by nothing, the phase line's circle wrapping (features/phase); one holder of the sign under the rotation per turned family (`sign_holder`)."""
    for record in range(families[index].records):
        if families[index].reads:
            content, factors = read(index, families, states, 1, wrap, gamma, unit, record)
            paces_guard(families[index].pair, gamma, unit, content, factors, families[index].name)
        links = odd_links(index, families, states, 1, wrap)
        if links is not None:  # a folded record's fold at every Link within the tangent 1
            fold_guard(families[index].pair, gamma, links, families[index].name)
        angles = turning(index, families, states, 1, record)
        if angles is not None:  # a turned record's Links at both ends, read as the holder declares
            ends = families[sign_holder(index, families)].link_read
            for a, link in zip((0, 0, 1, 1, 2, 2), link_levels(angles[1], wrap, ends), strict=True):
                link_guard(link, link_wall(gamma), families[index].name, a)


def least_pace(index: int, families: Families, states: States, gamma: int, wrap: Wrap, unit: int) -> int:
    """The least Node pace p_i = p_0^2 / Gamma of a family's records over the lattice as it is, 0 at a frozen Node, a lattice diagnostic for the report and no act of the law (the Links' factors beside it are read by no report)."""
    return min(
        int(
            np.min(
                paces.link_pace_of(gamma, read(index, families, states, 1, wrap, gamma, unit, record)[0])
            )
        )
        for record in range(families[index].records)
    )


def rule_of(
    family: FamilyRule, gamma: int, content: Any, factors: Factors | None = None, unit: int = 1
) -> Rule:
    """The rule every line of a family steps by, Rule3's integers at every Node from its pair and the paces of its read, (the six reaches R_ij, the own weight S_i, the wall w, the mass D_i), the clock and the Node's pace from the Node's content (`paces.node_paces`, The paces compose) and each Link's factor (ALGEBRA.md #the-line, the flux form; #the-interval): a family of quanta's (the holder of the sign included, its line its record) and a held row's alike, the row's own level among the content it reads (Every row reads the content); None no tension, G^2 on every Link; the step's module takes it (flux.py)."""
    num, den = family.pair
    clock, pace = paces.node_paces(gamma, content)
    return rule_integers(num, den, gamma, clock, pace, factors, unit)


def held_write_at(
    lines: Sequence[Record],
    numerators: Sequence[Any],
    walls: Sequence[Any],
    remainders: Sequence[np.ndarray],
    direction: int = 1,
) -> tuple[list[Record], list[np.ndarray]]:
    """A held family's one write per line (ALGEBRA.md #the-primitives, the row "the held write"), its lines already stepped by Rule3 in the interval's second act, with or without a gap: each line's level gains (numerator + r) div wall by the write's carried division (features/held_write) with the one remainder kept at the Node; backward the increments taken off and the remainders stepped back, exact; returns the lines and the remainders after."""
    found, after = [], []
    for line, numerator, wall, remainder in zip(lines, numerators, walls, remainders, strict=True):
        level, kept = held_write(line.now, numerator, wall, remainder, direction)
        kind = line.now.dtype  # the lines keep the lattice's kind under any wall
        found.append(replace(line, now=np.asarray(level, dtype=kind)))
        kind = np.asarray(
            wall
        ).dtype  # the remainder's kind its wall's, Python's integers under the carry
        after.append(np.asarray(kept, dtype=kind))
    return found, after


def seed_phases(board: Lattice, world: World) -> int:
    """The phase lines of every holder of the sign under the rotation seeded at the angle 0 before the first interval (`phase_lines`) and carried to the count the laid state stands at (`phase_counts` at the level before, the Node's phase row born at rest; `phase_carried`), the lines' amplitude X returned (features/phase `amplitude` at the line's unit 2 Gamma, the width's, never written); the board's families, states, shape, kind and wrap read and nothing else of it."""
    bits, gamma, families, states = (
        world.width.bit_length(),
        world.node_clock,
        board.families,
        board.states,
    )
    for index, family in enumerate(families):
        states[index].phases = phase_lines(family, board.shape, board.kind, gamma, bits)
        if family.rotation:  # the state's pairs stand on the one orbit from this seed (phase.Orbit)
            phase.seeded(states[index], phase.unit(gamma), phase.amplitude(phase.unit(gamma), bits))
    for index, family in enumerate(families):
        if family.rotation and any(turns(families, i) for i in range(len(families))):
            counts = phase_counts(index, families, states, -1, board.wrap, gamma)
            states[index].phases = phase_carried(index, states, counts, gamma)
    return phase.amplitude(phase.unit(gamma), bits)


def phase_act(
    held: Sequence[int], families: Families, states: States, direction: int, wrap: Wrap, gamma: int
) -> None:
    """The phase act of one interval on every held holder of the sign under the rotation (`phased`), by the potentials at the interval's start: forward at `direction` 1 before the lines' step, back at -1 after them."""
    for index in held:
        if families[index].rotation:
            states[index].phases = phased(index, families, states, direction, wrap, gamma)
