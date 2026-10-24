"""The click written on the lattice (ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision: after a click the paths are cancelled on the lattice, not in the clicks' books, Rule3 kept; the owner's word, the click the meeting of two quanta at one Node, the write their exchange there): the NodeDetectors' acts outside Rule3, taken by the engine's loop at the NodeDetectors' reports from outside the Node, as the lay and the receding face are; the Node knows nothing of them and no family of clicks exists. The draw: the click's read of the board (ALGEBRA.md, The click's read of the board; the owner's words), Rule3's kept remainders at the detector's Nodes read as the digits of one number (`read_number`, the digits in the order `digits.DIGIT_ORDER`), and each draw of the close one division act on it by the weights' total, the remainder the pick placed on the cumulative weights (the first whose cumulative weight exceeds it, the lower index on a tie) and the quotient the number left for the close's next draw (`drawn_from`); no generator and no seed: no number of the run is born outside the world file and Rule3, the same world read twice gives the same click, and the ensemble of worlds is the variety. The hole: the arriving record's levels at the one Node the credited quantum entered through set to 0, every line of the record there at the state of a Node with no level, exactly as the receding face removes a share (the advisor's second hand: for a spread record the form is quadratic, and subtracting one quantum's levels where less than a quantum stands would add form instead of removing it), which spreads by Rule3 alone as an event (no front is sent: a family has one level field, and an act ending a record's shares on arrival would end every other quantum's wave it reached); the record's count, not the levels, goes down by one. The lay of a record at one Node: the levels of `count` quanta of a pair standing at one Node at the pair's own rotation, the amplitude A from the count's measure, A^2 = count T den^2 div (2 (den^2 - num^2)) so that the share 6 den A^2 sin^2 omega reads the count (the count is the record's share), and for the massless pair the two levels alike, A^2 = count T div 2; a direction taken from the levels of the part the quantum leaves, so the phase passes with the quantum (the mathematician's hand, the arriving quantum's phase 0 on a real line of light); the level before the level now turned by the rest rotation, cos omega = num / den, in the record's own sense; the remainder at the lay's origin, the half wall. The face (the mathematician's hand, the advisor's second, two hands; the owner's word, the node_detector operates Rule3 on the families): the giver's write is no assignment but one value presented at one Port of the Node for two intervals, the least arrival that lifts Rule3's numerator at the Node into the target's window, arr_face = ceiling((w a* - SUM over the other Ports of R_j arr_j - S a_now + w a_before - r) / R_face) with the target a* = 0, so that Rule3 itself writes the level 0 and its own remainder, below one read coefficient; the second interval's face makes the new now 0 and the new before the 0 of the first, the record's lines at (0, 0) from then where every neighbour stands at 0, and the hole spreading by Rule3 alone elsewhere; the same value presented on the way back, Rule3's inverse crosses the click bit for bit, the Node knowing neither (the faces the books' log, `Face`). The undepleted beam (the two hands' line, the owner's word for the simple solution): a record of many quanta per Node is a beam, and the absorption of one of its quanta is read in the books and not written on the board, exact as the count per Node grows, so where the record's booked share at the Node, the share the credit reads there (`share.share`, the conserved form's density at the Node over 2 p_i^2 G^2), is above its own quantum W_rec, no face is booked and no front begins, the record's levels stand, its count in the books goes down by one and the board's share then exceeds the books' count by the quanta taken, the deficit, a tally per family printed in the books' line by name (`Lattice.books`); the hole to 0, both levels to 0, stands where the booked share at the Node is at most W_rec, the record there being local and whole, the front erasing what spread beyond it where the count reaches 0 (`take.faced`); the count goes down by one either way, the front erases only a record at count 0, and the inverse presents the kept value whatever the target."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import gcd
from typing import Any

import numpy as np

from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, PORTS, SIDES
from event_universe.core.rule3 import Rule, division_forward, flux_total, largest_below, rule3

SCALE_OF = (
    2  # the emission's reference scale, the count's wall times itself: its rounding below one level
)


def read_number(digits: Sequence[int], bases: Sequence[int]) -> int:
    """The click's read of the board as one integer (ALGEBRA.md, The click's read of the board): the digits `digits`, each Rule3's kept remainder at one of the detector's Nodes read as its index on the Node's lattice, r div F with F = gcd(w, D_i, R_ij) (`digits.read_of`, the order `loader/draw.DIGIT_ORDER`), each in [0, w div F), as one number with the first digit the most significant, x = ((d_1 b_2 + d_2) b_3 + d_3) ... in the mixed radix of the bases `bases`, each w div F + 1, one above its digit's count of values so that no total built of the wall's primes divides it (a digit carries log2(w div F) bits: 26.7 at the shipped universes' content 60, 11.9 for the atom [1, 1299], 1.6 for light at the exact vacuum paces), multiply and add in Python's integers, no division and no number of the run born here; the records' remainders are read and never written."""
    found = 0
    for digit, base in zip(digits, bases, strict=True):
        found = found * int(base) + int(digit)
    return found


def bias_bound(total: int, moduli: tuple[int, int]) -> list[int]:
    """The bound of a draw's bias by the read's base (the reader's F of 2026-10-20): the total's gcd with the read's bases less one (modulo it the residue is the distinct digits' sum), its gcd with the last base (modulo it the last digit alone) and the total, so that g / T, g the product of the two, bounds a port's move where the digits cycle; (1, 1, T) for a quotient's draw, which carries no moduli."""
    return [gcd(total, moduli[0]), gcd(total, moduli[1]), total]


def drawn_from(
    number: int, weights: Sequence[int], label: str, moduli: tuple[int, int] | None = None
) -> tuple[int, int]:
    """One draw from the number the click read (ALGEBRA.md, The click's read of the board; `read_number`): among the weights (each at or above 0, their total T above 0, refused by name otherwise) one division act of the number by T, the remainder the pick placed on the cumulative weights in their declared order, the first index whose cumulative weight exceeds it (the lower index on a tie, a weight of 0 never drawn), and the quotient the number left for the close's next draw (the credited Node, the piece's source), returned with the index; one weight above 0 (one weight, or one beside weights of 0) is a certain draw and consumes nothing, the number returned whole; a number below T is refused by name in two texts (the reader's G2 of 2026-10-20): the number read, the interval's read itself below the total (`moduli` given, the first draw: the board at the detector does not carry the draw and the world's declaration answers), and the number left, spent by the interval's earlier draws (a residue of a number below T is no residue of the whole). Derived: a residue uniform on [0, T) falls in the cell of the index i with probability w_i / T exactly, Born with no 2^-width term; the equidistribution of the digits' combination modulo T is measured on the ensembles and not derived (the law's honest clause). A total sharing a factor with the read's bases less one or with its last base (`moduli`, the read's first draw, `digits.read_of`; the quotient's draws after it carry none) reads its residue through the distinct digits' sum modulo the one gcd and the last digit modulo the other, exactly, and where the digits cycle a port's probability moves by at most g / T, g the product of the two gcds (`bias_bound`, booked on the click's line by the caller): a named bias, measured on the world's reads; the one draw refused by it is g = T with more than one weight above 0, the draw the digits' sum modulo the total alone (the reader's F of 2026-10-20, CHANGED the same day from the refusal where g reached the smallest weight, a model's worst case taken for a measure; the conversion's total 30 at the weight 1 was the draw refused, the conversion gone from the engine the same day)."""
    total = sum(int(weight) for weight in weights)
    if total <= 0:
        raise ValueError("the NodeDetector draws among weights whose total is above 0")
    live = [index for index, weight in enumerate(weights) if int(weight) > 0]
    if len(live) == 1:
        return live[0], int(number)  # a certain draw: one weight above 0 consumes nothing
    if number < total:
        if (
            moduli is not None
        ):  # the interval's read itself below the total: the board does not carry the draw
            raise RuntimeError(
                f"the click's read of the board at {label} has the number {number} read, below the draw's total "
                f"{total}: the digits read at this interval do not carry the draw (a residue of a number below the "
                "total is no residue of the whole); the world's declaration answers, the body's record over more "
                "Nodes, a well, a drive with a content, no key on the draw"
            )
        raise RuntimeError(
            f"the click's read of the board at {label} has the number {number} left, below the draw's total "
            f"{total}: the digits read are spent at this interval by its earlier draws (a residue of a number below "
            "the total is no residue of the whole); a shorter window, fewer draws per close or more Nodes read"
        )
    summed, last, _total = bias_bound(total, moduli or (1, 1))
    if summed * last == total and sum(1 for weight in weights if int(weight) > 0) > 1:
        raise RuntimeError(
            f"the click's read of the board at {label}: the draw's total {total} is the product of its gcd "
            f"{summed} with the read's bases less one and its gcd {last} with its last base, so the draw is the "
            "digits' sum modulo the total alone (and the last digit modulo the base's factor), no uniform part "
            "left to place: the draw is refused"
        )
    left, residue = division_forward(int(number), total, 0)
    reached = 0
    for index, weight in enumerate(weights):
        reached += int(weight)
        if residue < reached:
            return index, int(left)
    return len(weights) - 1, int(left)


@dataclass
class Face:
    """One presented value, the face: the record's family and line, the Node at the file's coordinates, the Ports presented at, a set of one to three Ports, a sided axis's one and a tied axis's two, within the wall's bound (`node_detector.face_ports`) (the hole's the Ports the quantum entered by, from the window's inflow booked per Port, `node_detector.arrival_ports`; a front shell Node's the Ports toward the inner shell, `front.faced`; the click's plan, C6: nature names no axis, so no Port order is read, the set maps to its image under the cube's symmetries and the one value presented on it is the same integer; a cut Port, its read 0, is dropped at the step and a set left without an open Port is refused by name), the interval at whose step it is presented, the value, None until the forward step computes it, the value the inverse presents again, and the frame's two flags (ALGEBRA.md, The booking is the frame's, the hole's clause, 2026-10-23): `framed`, whether the face's target is the level the record's frame holds at the Node (`target_of`: a plain massless record, one real line reading no holder of the sign, `take.faced`, `front.faced`; False for every other record, the target 0 as written, since a gapped row's mass and a turned plane's rotation read the level), and `inner`, which side the target is read from, over every open Port for the hole (False: the hole takes the record's wave and leaves the uniform level, to 0 where the neighbours stand at 0) and over the face's own Ports for a front shell (True; the front's faces are never framed, their target 0 as written, since the inner shell's Nodes stand mid-erasure at (0, the level before) and read as no frame, and the front runs at the count 0 alone), so that a uniform shift of a massless level moves every face's target with it."""

    family: int
    line: int
    at: tuple[int, int, int]
    ports: tuple[int, ...]
    interval: int
    value: int | None = None
    inner: bool = False
    framed: bool = False


def face_value(total: int, read: int) -> int:
    """The least arrival that lifts Rule3's numerator into the target's window [0, R_face), ceiling(-total / R_face), the division act's floor negated, with `total` the numerator with the face Ports' arrivals 0 less w a* (a* the target, 0 for the hole to 0) and `read` R_face the sum of the set's reaches: R_face x value + total in [0, R_face), within [0, w) since each reach is at most w / 3 at paces at most the vacuum's (L810's guard) and the set holds at most one Port per axis, so the level next is a* and the remainder Rule3's own, below one read coefficient."""
    return -int(division_forward(total, read, 0)[0])


def target_of(
    arrived: tuple[Any, ...],
    arrived_before: tuple[Any, ...] | None,
    at: tuple[int, int, int],
    reference: tuple[int, ...],
) -> int:
    """A face's target, the level the record's frame holds at the Node (ALGEBRA.md, The booking is the frame's, the hole's clause, 2026-10-23), read through the `reference` Ports from the neighbours' two levels and nothing beyond one Link: where the neighbours agree on their own next level, 2 now_j - before_j one number on every reference Port (a Node uniform with its neighbours, the level's own test: the massless row's free step is 2 L - a_before at any paces, exact in the integers on a drift), that level, so that after the hole's two faces the Node carries its neighbours' two levels, the record's wave alone taken and the uniform part untouched, and a uniform shift c of every level moves the target by c exactly; where they do not agree the frame is not readable at the Node by one Link's reach (a packet's edge: the neighbours' own next levels carry their Links' terms two Links from the Node, and the extrapolation overshoots them, the run refused at the amplitude bound where it was taken), and the target is 0, the written hole bit for bit, a write the shift is no symmetry of (named open in FURTHER_RESEARCH.md); 0 where the level before's arrivals are not given (a face presented with no frame), where the set is empty, and where the neighbours stand at 0."""
    if arrived_before is None or not reference:
        return 0
    own_next = {2 * int(arrived[p][at]) - int(arrived_before[p][at]) for p in reference}
    return own_next.pop() if len(own_next) == 1 else 0


def presented(
    arrived: tuple[Any, ...],
    rule: Rule,
    now: Any,
    other: Any,
    carry: Any,
    faces: list[Face],
    offset: tuple[int, int, int],
    direction: int,
    arrived_before: tuple[Any, ...] | None = None,
) -> tuple[Any, ...]:
    """The six arrivals of a line with the faces' values presented at their Ports and Nodes, every other arrival the neighbour's own: forward the value is computed at the Node from Rule3's flux line (`rule3.flux_total` with the face's arrival 0 among the six, the Node's two levels, its mass and its remainder as the step reads them; `face_value` at the target, the frame's level at the Node, `target_of` from the neighbours' two levels (`arrived`, `arrived_before`, the level before's six arrivals; 0 where none are given), on the sum of the reaches of the face's Ports, every cut Port, its reach 0 at the Node, dropped from the set and the set kept in the face; a set left with no open Port refused by name), backward the kept value is presented again, so the inverse runs through the click; the arrays copied once per Port touched."""
    found, copied = list(arrived), set()
    for face in faces:
        at = (face.at[0] + offset[0], face.at[1] + offset[1], face.at[2] + offset[2])
        here = [int(np.asarray(read)[at]) if np.ndim(read) else int(read) for read in rule.reaches]
        if face.value is None:
            assert direction == 1, "a face is computed forward and presented again backward"
            named, face.ports = face.ports, tuple(p for p in face.ports if here[p] != 0)
            if not face.ports:  # every Port of the set cut, or no Port named: the hole has no side
                raise ValueError(
                    f"the face at the Node {list(face.at)} has no open Port in its set {list(named)}"
                )
            reach = sum(here[p] for p in face.ports)
            level, wall = int(now[at]), int(rule.wall)
            own = int(np.asarray(rule.mass)[at] if np.ndim(rule.mass) else rule.mass)
            links = sum(
                here[p] * (int(found[p][at]) - level) for p in range(len(here)) if p not in face.ports
            )
            links -= reach * level  # the set's Links with their arrivals 0
            total = flux_total(links, own, wall, level, int(other[at])) + int(carry[at])
            reference = face.ports if face.inner else tuple(p for p in range(len(here)) if here[p] != 0)
            target = target_of(arrived, arrived_before, at, reference) if face.framed else 0
            face.value = face_value(
                total - wall * target, reach
            )  # the frame's level on a plain massless record, 0 on every other: every face's target
        for port in face.ports:
            if port not in copied:
                found[port] = np.array(found[port], copy=True)
                copied.add(port)
            found[port][at] = face.value
    return tuple(found)


def squared(count: int, action: int, pair: tuple[int, int], laid: int = 1) -> int:
    """A^2 of `count` quanta standing at one Node on `laid` lines alike (one, the taker's part): (the largest x with x^2 <= count^2 T^2 den^2 div (4 laid^2 (den^2 - num^2))), one search on the whole product by the search on the share reading (`rule3.largest_below`), the invariant 2 A^2 sin omega = T per quantum per line (ALGEBRA.md, the absorption's A^2 = (N + 1) T / (2 sin omega_part); the two hands' word on R8, #1793), count T div (2 laid) for the massless pair, the number `amplitude` takes the largest integer whose square is at most it of."""
    num, den = pair
    gap = den * den - num * num
    if gap:
        half = (
            count * action * den
        )  # 2 laid A^2 s = count T den with s^2 = gap: the search on the whole product
        return largest_below(int(division_forward(half * half, 2 * laid * 2 * laid * gap, 0)[0]))
    return int(division_forward(count * action, 2 * laid, 0)[0])


def spread(square: int, share: tuple[int, int]) -> int:
    """A region's Node's amplitude from the record's A^2 and the Node's share (weight, total) of the lay, (the largest x with x^2 <= A^2 weight div total): A_n^2 = A^2 / n over n Nodes in equal counts (ALGEBRA.md, The NodeDetector is one declaration kind for every world; the mathematician's hand)."""
    weight, total = share
    return largest_below(int(division_forward(square * weight, total, 0)[0]))


def amplitude(count: int, action: int, pair: tuple[int, int], laid: int = 1) -> int:
    """The amplitude A of `count` quanta standing at one Node on `laid` lines alike (one, the taker's part): A^2 = count T den^2 div (2 laid (den^2 - num^2)), the share 6 den A^2 sin^2 omega per line over W_c = 3 den T the count, by the search on the share reading (`rule3.largest_below`); for the massless pair, whose one-Node record has no rotation, A^2 = count T div (2 laid), the two levels alike (the lay by the count, `emission.laid_by_count`: every laid line of the record alike, the symmetric lay, the mathematician's hand)."""
    return largest_below(squared(count, action, pair, laid))


def two_squares(total: int) -> tuple[int, int] | None:
    """`total` as a sum of two squares, (a, b) with a >= b >= 0 and the largest a, by the search on the square (`rule3.largest_below`); None where no such pair exists: a plane's (re, im) at the quarter-turn lay carrying the Wronskian re^2 + im^2 = total exactly."""
    a = largest_below(total)
    while a * a * 2 >= total:
        b = largest_below(total - a * a)
        if a * a + b * b == total:
            return a, b
        a -= 1
    return None


def plane_squares(total: int, planes: int) -> list[tuple[int, int]] | None:
    """The tightest split of `total` over `planes` planes as sums of two squares, one (re, im) per plane with the planes' sums within the least spread about total div planes (the search widening the spread from 0, the sums nondecreasing), so that a record of several planes laid by the count at one Node carries its quantum's A^2 = T div 2 exactly in its Wronskian where the rounding per plane falls short (three planes at T div 6: 5450 + 5458 + 5476 = 16384 where 3 x 73^2 = 15987); None where no split exists (one plane whose total is no sum of two squares)."""
    if planes <= 1:
        squares = two_squares(total)
        return None if squares is None else [squares]
    target = int(division_forward(total, planes, 0)[0])

    def chain(left: int, lowest: int, top: int, planes_left: int) -> list[tuple[int, int]] | None:
        if planes_left == 0:
            return [] if left == 0 else None
        for one in range(lowest, min(top, left) + 1):
            squares = two_squares(one)
            if squares is None:
                continue
            rest = chain(left - one, one, top, planes_left - 1)
            if rest is not None:
                return [squares, *rest]
        return None

    for spread in range(target + 1):
        for first in range(max(target - spread, 0), target + 1):
            found = chain(total, first, first + spread, planes)
            if found is not None:
                return found
    return None


def direction(re: int, im: int, size: int) -> tuple[int, int]:
    """A level pair of the size `size` in the direction of (re, im) by the division act, (size, 0) where the pair is 0: the phase of the part the quantum leaves passed to the part it enters."""
    norm = largest_below(re * re + im * im)
    if norm == 0:
        return size, 0
    return int(division_forward(re * size, norm, 0)[0]), int(division_forward(im * size, norm, 0)[0])


def standing(
    count: int,
    action: int,
    pair: tuple[int, int],
    phase: tuple[int, int],
    sense: int,
    share: tuple[int, int] = (1, 1),
) -> tuple[tuple[int, int], tuple[int, int]]:
    """The levels of `count` quanta of a plane standing at one Node, ((re_now, im_now), (re_before, im_before)): the amplitude `amplitude` in the direction `phase`, the level before the level now turned by the rest rotation in the record's sense, re_b = (re num - sense im s) div den and im_b = (im num + sense re s) div den with s = the largest integer whose square is at most den^2 - num^2 (sin omega den, `paces.sine_den`), so the Wronskian re_now im_before - im_now re_before is sense x A^2 sin omega; both 0 at the count 0."""
    if count <= 0:
        return (0, 0), (0, 0)
    num, den = pair
    re, im = direction(phase[0], phase[1], spread(squared(count, action, pair), share))
    sine = sense * sine_den(num, den)
    re_before = int(division_forward(re * num - im * sine, den, 0)[0])
    im_before = int(division_forward(im * num + re * sine, den, 0)[0])
    return (re, im), (re_before, im_before)


def invariant(
    count: int, action: int, pair: tuple[int, int], laid: int, share: tuple[int, int] = (1, 1)
) -> int:
    """The amplitude of `count` whole quanta laid at one Node on a record of `laid` real lines or planes, every one alike, by the invariant (the two hands, the advisor's (b) and (c) and the mathematician's hand: one unit of the invariant 2 A^2 sin omega = T per quantum over the record's lines, A_l^2 = count T den div (2 s laid) with s the largest integer whose square is at most den^2 - num^2, sin omega den (`paces.sine_den`); the proton's three planes at T / 6 at [0, den], the electron's plane at 148, the antineutrino's real line at the excess rotation), the generator's one-Node declaration (tools/pixel_mode.py, `pixel_record`) in the engine for the lay of a record converted whole at the start, cut at its Node (`take.relaid`); the share form of `amplitude` beside it, the reader's parts' lay, and the lay by the count of `standing` at the massless pair for a whole quantum given at an open-Link Node (the two hands); 0 at the count 0 and on a pair with no rotation (a massless lay has no finite amplitude by the invariant)."""
    num, den = pair
    sine = sine_den(num, den)
    if count <= 0 or sine == 0:
        return 0
    return spread(int(division_forward(count * action * den, 2 * sine * laid, 0)[0]), share)


def line_total(action: int, resonance: tuple[int, int]) -> int:
    """The total of the squared amplitudes of one quantum of light on one real line, SUM a^2 = T / sin Omega, (the largest x with x^2 <= T^2 den^2 div (den^2 - num^2)) by the search on the share reading (`rule3.largest_below`), twice S (the mathematician's hand and the advisor's second, two hands): S = T / (2 sin Omega) is the SUM a^2 of one line of a plane record carrying one quantum, the taker's lay, the two lines together 2 A^2 sin Omega = T, and the packet is laid on the light record's first line alone, so the packet's root is T / sin Omega for a one-line packet (or S on each of two lines a quarter turn apart, the polarisation a world's choice by name; the branch lays one line); 43,962 at T = 32,768 and [2, 3]; one root at the lay, the NodeDetector's own act and no act of the interval. The source in time keeps S (`emission.laid_increment`): a source's increments are a drive and the field's energy is the response's."""
    num, den = resonance
    return largest_below(int(division_forward(action * action * den * den, den * den - num * num, 0)[0]))


def rotated(first: int, second: int, doubled: int, unit: int, count: int) -> list[int]:
    """Rule3's rotation act (ALGEBRA.md #the-four-acts (b)) from the levels `first` and `second`: a_next = (doubled a_now + r) div unit - a_before with the remainder kept, `count` levels in all; unit cos(n theta) from (unit, doubled div 2) and unit sin(n theta) from (0, unit sin theta) at 2 unit cos theta = doubled."""
    levels, carry = [first, second], 0
    mass = unit + unit - doubled  # the line's own term: Rule3's flux line with no Links
    while len(levels) < count:
        following, carry = rule3(0, mass, unit, levels[-1], levels[-2], carry)
        levels.append(int(following))
    return levels[:count]


def wave_cosine(turns: int, halves: int, unit: int) -> int:
    """unit cos(pi turns / halves) by the rotation act (the click's plan, C1: the cosine of a wave number pi p / q, as a packet's `wave` [p, q] declares it, by the integer search and no table; the quarter turn reads 0 exactly and an angle past it reads the negative of its mirror's, cos(pi - k) = -cos k, so one record has one unit at [1, 2] with den cos omega 4000 and not the search's 3999, the cold reader's line of 2026-10-19): the doubled cosine of the step pi / (2 halves) is the largest integer at which the rotation from the unit reaches 0 within `halves` steps (bisection on the integers, no root and no table, as the packet lay's generator finds its cosines), and 2 |turns| steps of it are the wave's cosine; at turns 1 and halves width + 1 the lowest mode of a top-hat of `width` Nodes with zero ends, cos(pi / (width + 1)) (`along_cosine`, `emission.holds_period`)."""
    turns = abs(turns)  # the cosine is even
    if 2 * turns == halves:
        return 0  # the quarter turn exactly: cos(pi / 2) = 0, the circle's two halves mirror about it
    if 2 * turns > halves:
        return -wave_cosine(halves - turns, halves, unit)  # cos(pi - k) = -cos k, the mirror's half
    lower, upper = 0, 2 * unit
    while upper - lower > 1:
        middle = int(division_forward(lower + upper, 2, 0)[0])
        if min(rotated(unit, int(division_forward(middle, 2, 0)[0]), middle, unit, halves + 1)) <= 0:
            lower = middle
        else:
            upper = middle
    steps = 2 * turns  # the recurrence's two seeds and the steps after them to the wave's angle
    return rotated(unit, int(division_forward(lower, 2, 0)[0]), lower, unit, steps + 1)[steps]


def below_the_band(num: int, den: int) -> bool:
    """Whether a resonance [num, den] lies below the width-one guide's band, no axis carrying the quantum: den cos k = (PORTS num - (PORTS - SIDES) den) div SIDES below -den, that is PORTS num below (PORTS - 2 SIDES) den (the guide of `emission.radiated_total`; the mathematician's hand)."""
    return PORTS * num < (PORTS - SIDES - SIDES) * den


def along_cosine(
    light: tuple[int, int], resonance: tuple[int, int], width: int, unit: int
) -> int | None:
    """The doubled cosine 2 unit cos k_z of a packet's wave number along its axis, from the light family's band with the transverse mode of its width (the mathematician's hand, the advisor's second, two hands): cos Omega = (num_l / (3 den_l)) (cos k_z + 2 cos k_perp) with k_perp = pi / (width + 1) the lowest mode of the top-hat across, so 2 unit cos k_z = (6 unit den_l num) div (num_l den) - 2 x (2 unit cos k_perp), the two transverse axes each at the doubled cosine, every cosine at the unit by the rotation act; None where the width cannot carry Omega, cos k_z not strictly inside (-1, 1) (the band's edge k_z = 0, a wave of no wave number, refused with the outside; the top-hat's spectrum spreads the frequency by about (num_l / (3 den_l)) k_perp^2 / sin Omega, the open board's tolerance)."""
    (num_l, den_l), (num, den) = light, resonance
    across = 2 * wave_cosine(1, width + 1, unit)  # 2 unit cos k_perp, one transverse axis
    doubled = int(division_forward(PORTS * unit * den_l * num, num_l * den, 0)[0]) - (AXES - 1) * across
    return doubled if -2 * unit < doubled < 2 * unit else None


def envelope(total: int, span: int, across: int) -> list[int]:
    """A packet's amplitude per Node slice by slice along its axis in the energy form (the mathematician's hand, on the advisor's derivation, step 5, two hands): the energy left R_0 the packet's root (`line_total`, T / sin Omega for the one-line packet), each slice's energy R_t div span over the `across` Nodes of its cross-section, the amplitude per Node a_t = (the largest x with x^2 <= (R_t div span) div across), the carry R_(t+1) = R_t - across a_t^2, so that the energy decays at 1 / span per slice and the amplitude at 1 / (2 span), the survival under the declared constant hazard, the premise named in ALGEBRA.md, The click writes on the lattice (5); nature's linewidth the click's number beside it; the lay ends where a_t falls below 1, the deficit left below span level squared per Node (47 of 43,962, the one-line root at T = 32,768 and [2, 3], span 48, one Node across, the mathematician's number); the length L = 2 span ln a_0 in the continuous line (326 at a_0 = 30) and longer in the integers, whose tail at a_t = 1 falls linearly (456 slices there, SUM a_t^2 = 43,915)."""
    found: list[int] = []
    left = total
    while True:
        energy = int(division_forward(left, span, 0)[0])
        amplitude = largest_below(int(division_forward(energy, across, 0)[0]))
        if amplitude == 0:
            return found
        found.append(amplitude)
        left -= across * amplitude * amplitude
