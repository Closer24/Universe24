"""The click written on the lattice (ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision: after a click the paths are cancelled on the lattice, not in the clicks' books, Rule3 kept; the owner's word, the click the meeting of two quanta at one Node, the write their exchange there): the NodeDetectors' acts outside Rule3, taken by the engine's loop at the NodeDetectors' reports from outside the Node, as the lay and the receding face are; the Node knows nothing of them and no family of clicks exists. The draw: the click's read of the board (ALGEBRA.md, The click's read of the board; the owner's words), Rule3's kept remainders at the detector's Nodes read as the digits of one number (`read_number`, the digits in the order `digits.DIGIT_ORDER`), and each draw of the close one division act on it by the weights' total, the remainder the pick placed on the cumulative weights (the first whose cumulative weight exceeds it, the lower index on a tie) and the quotient the number left for the close's next draw (`drawn_from`); no generator and no seed: no number of the run is born outside the world file and Rule3, the same world read twice gives the same click, and the ensemble of worlds is the variety. The hole: the arriving record's levels at the one Node the credited quantum entered through set to 0, every line of the record there at the state of a Node with no level, exactly as the receding face removes a share (the advisor's second hand: for a spread record the form is quadratic, and subtracting one quantum's levels where less than a quantum stands would add form instead of removing it), which spreads by Rule3 alone as an event (no front is sent: a family has one level field, and an act ending a record's shares on arrival would end every other quantum's wave it reached); the record's count, not the levels, goes down by one. The lay of a record at one Node: the levels of `count` quanta of a pair standing at one Node at the pair's own rotation, the amplitude A from the count's measure, A^2 = count T den^2 div (2 (den^2 - num^2)) so that the share 6 den A^2 sin^2 omega reads the count (the count is the record's share), and for the massless pair the two levels alike, A^2 = count T div 2; a direction taken from the levels of the part the quantum leaves, so the phase passes with the quantum (the mathematician's hand, the arriving quantum's phase 0 on a real line of light); the level before the level now turned by the rest rotation, cos omega = num / den, in the record's own sense; the remainder at the lay's origin, the half wall. The face (the mathematician's hand, the advisor's second, two hands; the owner's word, the node_detector operates Rule3 on the families): the giver's write is no assignment but one value presented at one Port of the Node for two intervals, the least arrival that lifts Rule3's numerator at the Node into the target's window, arr_face = ceiling((w a* - SUM over the other Ports of R_j arr_j - S a_now + w a_before - r) / R_face) with the target a* = 0, so that Rule3 itself writes the level 0 and its own remainder, below one read coefficient; the second interval's face makes the new now 0 and the new before the 0 of the first, the record's lines at (0, 0) from then where every neighbour stands at 0, and the hole spreading by Rule3 alone elsewhere; the same value presented on the way back, Rule3's inverse crosses the click bit for bit, the Node knowing neither (the faces the books' log, `Face`). The undepleted beam (the two hands' line, the owner's word for the simple solution): a record of many quanta per Node is a beam, and the absorption of one of its quanta is read in the books and not written on the board, exact as the count per Node grows, so where the record's booked share at the Node, the share the credit reads there (`share.share`, the conserved form's density at the Node over 2 p_i^2 G^2), is above its own quantum W_rec, no face is booked and no front begins, the record's levels stand, its count in the books goes down by one and the board's share then exceeds the books' count by the quanta taken, the deficit, a tally per family printed in the books' line by name (`Lattice.books`); the hole to 0, both levels to 0, stands where the booked share at the Node is at most W_rec, the record there being local and whole, the front erasing what spread beyond it where the count reaches 0 (`take.faced`); the count goes down by one either way, the front erases only a record at count 0, and the inverse presents the kept value whatever the target."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import gcd
from typing import Any

import numpy as np

from event_universe.core.rule3 import Rule, division_forward, flux_total, largest_below


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
    """One presented value, the face: the record's family and line, the Node at the file's coordinates, the Ports presented at, a set of one to three Ports, a sided axis's one and a tied axis's two, within the wall's bound (`node_detector.face_ports`) (the hole's the Ports the quantum entered by, from the window's inflow booked per Port, `node_detector.arrival_ports`; a front shell Node's the Ports toward the inner shell, `front.faced`; the click's plan, C6: nature names no axis, so no Port order is read, the set maps to its image under the cube's symmetries and the one value presented on it is the same integer; a cut Port, its read 0, is dropped at the step and a set left without an open Port is refused by name), the interval at whose step it is presented, the value, None until the forward step computes it, the value the inverse presents again, and the front's taper (`fraction`, (p, q): the target the fraction p / q of Rule3's own level by the division act on its size, toward 0, so that a level of size 1 falls to 0 at any fraction below 1 and no leading edge of ones rides the band; None the target 0, the hole to 0; src/event_universe/front.py)."""

    family: int
    line: int
    at: tuple[int, int, int]
    ports: tuple[int, ...]
    interval: int
    value: int | None = None


def face_value(total: int, read: int) -> int:
    """The least arrival that lifts Rule3's numerator into the target's window [0, R_face), ceiling(-total / R_face), the division act's floor negated, with `total` the numerator with the face Ports' arrivals 0 less w a* (a* the target, 0 for the hole to 0) and `read` R_face the sum of the set's reaches: R_face x value + total in [0, R_face), within [0, w) since each reach is at most w / 3 at paces at most the vacuum's (L810's guard) and the set holds at most one Port per axis, so the level next is a* and the remainder Rule3's own, below one read coefficient."""
    return -int(division_forward(total, read, 0)[0])


def presented(
    arrived: tuple[Any, ...],
    rule: Rule,
    now: Any,
    other: Any,
    carry: Any,
    faces: list[Face],
    direction: int,
) -> tuple[Any, ...]:
    """The six arrivals of a line with the faces' values presented at their Ports and Nodes, every other arrival the neighbour's own: forward the value is computed at the Node from Rule3's flux line (`rule3.flux_total` with the face's arrival 0 among the six, the Node's two levels, its mass and its remainder as the step reads them; `face_value` at the target, 0, the hole to 0, or the taper's fraction of Rule3's own level, on the sum of the reaches of the face's Ports, every cut Port, its reach 0 at the Node, dropped from the set and the set kept in the face; a set left with no open Port refused by name), backward the kept value is presented again, so the inverse runs through the click; the arrays copied once per Port touched."""
    found, copied = list(arrived), set()
    for face in faces:
        at = face.at
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
            face.value = face_value(total, reach)  # the hole to 0, every face's target
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
