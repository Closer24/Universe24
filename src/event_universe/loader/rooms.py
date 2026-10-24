"""The rooms of a held family's one write per part at the amplitude A, the numerator's size over A^2 at the largest level (ALGEBRA.md #the-bound; The write per proper volume and per proper interval; The guard): one source's booking's room (`booking_room`), the write's factor's room at a source's hill's edge (`hill_scale`) and under a negative tension (`factor_bound`, `tension_room`, `source_room`), and the row's rooms line by line (`write_rooms`), read by the amplitude bound of loader/derived.py (`bound_under_rooms`), which this module reads for the families and the walls."""

from __future__ import annotations

from event_universe.core.ports import AXES, SIDES
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.features.currents import PRODUCTS
from event_universe.features.read import edge_of
from event_universe.loader.derived import FamilyRule, HeldWrite, readers_of, weight_of


def booking_room(families: tuple[FamilyRule, ...], index: int, wronskian: bool) -> int:
    """The room of one source's booking at the amplitude A, its size over A^2: the Wronskian's two products per plane of the part (three planes thrice), or the form's two per line of its record (now^2 and next x before); a turned record's bookings are read from its plain levels too (under the temporal gauge the time Link carries no phase, plane.step_plane), so no turned level enters a booking."""
    if wronskian:
        return PRODUCTS * (families[index].planes or 1)  # every plane of the part its two products
    return families[index].record * PRODUCTS


def hill_scale(pair: tuple[int, int], gamma: int) -> int:
    """The write's factor's room at a source's hill's edge (ALGEBRA.md, The write per proper volume and per proper interval; The guard): P the edge's pace of the source's pair, the largest the guard admits (`features/read`, `edge_of`), where the factor N^k p_x p_y p_z / p_0^3, one rounding of the count times the three paces over the one wall (`paces.write_factor`, the product exact beyond the width), is at most (P / Gamma)^3 (1 at most in a hollow, every pace at or below Gamma): P^3 div Gamma^3 rounded up, which multiplies the booking's room in the write's numerator, the one place the factor meets the width."""
    edge = edge_of(pair, gamma)
    cube = gamma * gamma * gamma
    return int(division_forward(edge * edge * edge, cube, cube - 1)[0])


def factor_bound(families: tuple[FamilyRule, ...], index: int, gamma: int, bound: int) -> int:
    """The largest Link factor q_max the axis lines within the level `bound` admit on a Link of the family `index`'s record (ALGEBRA.md, The write per proper volume and per proper interval): the Link's factor is q = Gamma - t (`paces.axis_pace`), t the Link's tension, SUM over the held rows with axis lines the family reads of W_a times the mean of the row's axis line at the Link's two ends (`read.link_tension`), each end within the bound, so q_max = Gamma + SUM W_a x bound over those rows (the mathematician's hand with the advisor's precision: Gamma + W A on the one axis line a Link carries, the sum where more than one held row's axis lines are read on a Link); Gamma where the family reads no axis line, the odd lines of a holder under the rotation entering no Link's factor (`node.read_lines`)."""
    weights = sum(
        abs(read.weight)
        for read in families[index].reads
        if families[read.family].axes and not families[read.family].rotation
    )
    return gamma + weights * bound


def tension_room(pair: tuple[int, int], gamma: int, q_max: int, wronskian: bool) -> int:
    """The write's factor's room at a source's hill's edge under a negative tension (ALGEBRA.md, The write per proper volume and per proper interval; the mathematician's hand and the advisor's second, two hands): the guard bounds p_i^2 Q_ij and not the Link's factor q itself, so under a negative tension q exceeds Gamma, up to q_max, the largest Link factor the axis lines within the bound admit (`factor_bound`), and in a hollow the factor reaches (P / Gamma)^3 (q_max / P)^(1/2) on a count and (P / Gamma)^3 q_max / P on a Wronskian, P the edge's pace of the source's pair (`edge_of`), beyond the hill's room (`hill_scale`); the room is the ceiling of P^2 ((the largest x with x^2 <= q_max P) + 1) / Gamma^3 on a count and of P^2 q_max / Gamma^3 on a Wronskian, the ceiling by the division act with the carry Gamma^3 - 1 and the root's integer the largest whose square is at most the product, plus one, so that the floor never under-bounds (at the rule's universe, Gamma 6,000 and q_max 15,266: 3 and 4 on matter's pair against the hill's 2, 2 and 3 on the massless pairs against 1)."""
    edge = edge_of(pair, gamma)
    cube = gamma * gamma * gamma
    factor = q_max if wronskian else largest_below(q_max * edge) + 1
    return int(division_forward(edge * edge * factor, cube, cube - 1)[0])


def source_room(
    families: tuple[FamilyRule, ...], index: int, gamma: int, wronskian: bool, hill: int | None
) -> int:
    """The room of the write's factor of the source `index` in a row's write (ALGEBRA.md, The write per proper volume and per proper interval): the hill's room alone (`hill_scale`) where `hill` is None, the first pass of `amplitude_bound`, which finds the hill's own bound A_1; else the larger of the hill's room and the tension's room at the largest Link factor the axis lines within A_1 = `hill` admit (`tension_room`, `factor_bound`), one pass and no fixed point, since the bound found is at most A_1 and q_max(A_1) bounds q_max(A)."""
    room = hill_scale(families[index].pair, gamma)
    if hill is None:
        return room
    q_max = factor_bound(families, index, gamma, hill)
    return max(room, tension_room(families[index].pair, gamma, q_max, wronskian))


def write_rooms(
    families: tuple[FamilyRule, ...],
    index: int,
    write: HeldWrite,
    gamma: int,
    hill: int | None,
    unit: int,
) -> list[int]:
    """The room of a held family's one write per part at the amplitude A, the numerator's size over A^2 at the largest level, each part's times the size of the row's write weight: for the time part SUM over the sourcing families of w x the room of the booking the row takes, the form or the Wronskian (`booking_room`), times the write's factor's room at the source's hill's edge (`source_room`: the hill's, `hill_scale`, 1 in a hollow under tensions at or above 0, where `hill` is None, and the larger of it and the tension's room at the hill's own bound `hill`, `tension_room`, where it is given; the Wronskian's room on a count too where the row declares the form's own clock, one proper-interval power); for each axis part SUM over the sources of w x factor x lines x 2 x 2 |num| for a tension line (the tension's part per line of the source's record, the centred difference squared, the difference of two levels within the bound squared, |num| on it; The stress is the Links', 2026-10-23) and w x factor x lines x 2 x 2 for an odd line (the sign's current across the axis's two Ports, two products each: the room of the two Links' currents, within which their mean, the source, stays), and w x factor x lines x 2 x 2 x |num| for a shear line (one product of the Node's two axis differences, each the difference of two levels within the bound, |num| on it)."""
    family = families[index]
    sources = readers_of(families, index)
    time = sum(
        abs(weight_of(index, families[other]))
        * (
            write.factors[other] if family.wronskian else 1
        )  # the sign holder's charge factor on its time line (The constants, 2026-10-24)
        * booking_room(families, other, family.wronskian)
        * source_room(families, other, gamma, True, hill)
        for other in sources
    )
    axis = sum(
        abs(weight_of(index, families[other]))
        * write.factors[other]
        * families[other].record
        * PRODUCTS
        * (SIDES if family.rotation else abs(families[other].pair[0]))
        for other in sources
    )
    rooms = [time] + [axis] * (family.width - 1)
    if (
        family.axes and not family.rotation
    ):  # a tension line: the centred difference squared, (2 A)^2 at the bound, |num| on it (The stress is the Links', 2026-10-23)
        rooms[1 : 1 + AXES] = [SIDES * axis] * AXES
    if (
        family.flux
    ):  # an odd line: the flux through the axis's two Ports, two products each, |num| on each
        rooms[1 + AXES :] = [SIDES * axis] * AXES
    return [abs(family.write) * room for room in rooms * family.records]


def held_room(
    family: FamilyRule,
    write: HeldWrite,
    rooms: list[int],
    found: int,
    largest: int,
    gamma: int,
    action: int,
    width: int,
) -> int:
    """The bound a held family's one write leaves inside the width, folded into the board's bound `found` for a holder of the content and gated apart for the holder of the sign (the Boss's word of 2026-10-24: the register's scale and the lay's amplitude bound are the loader's tool and no line of the law, and a record laid at W = 0 writes nothing, so a sign holder's write room never lowers the bound for the others; refused by name where it leaves no level inside the width; the former rule, the min over every family's rooms with the sign holder's among them, kept by name, 2026-10-23): per line (largest - wall) div room, the least over the lines, 0 where a wall passes the width."""
    own = largest
    for wall, room in zip(write.walls, rooms, strict=True):
        if wall > largest:
            own = 0
        elif room:
            own = min(own, largest_below(int(division_forward(largest - wall, room, 0)[0])))
    if not family.wronskian:
        return min(found, own)
    if own < 1:
        raise ValueError(
            f"the holder of the sign {family.name!r} at the Node clock Gamma = {gamma} and T = {action}: "
            f"its one write's room, the walls {list(write.walls)[:2]} and the numerators' rooms "
            f"{[int(room) for room in rooms][:2]} per level, leaves no level inside the width of "
            f"{width} bits (ALGEBRA.md #the-bound; the room gated apart from the register's bound)"
        )
    return found
