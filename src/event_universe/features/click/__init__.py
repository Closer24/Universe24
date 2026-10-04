"""The click written on the lattice (ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision: after a click the paths are cancelled on the lattice, not in the clicks' books, Rule3 kept; the owner's word, the click the meeting of two quanta at one Node, the write their exchange there): the NodeDetectors' acts outside Rule3, taken by the engine's loop at the NodeDetectors' reports from outside the Node, as the lay and the receding face are; the Node knows nothing of them and no family of clicks exists. The draw: the draw's generator, declared in the world file with its seed, x <- (multiplier x + increment) mod modulus by the division act, the pick the state's fraction of the weights' total, (x times total) div modulus by the same act, and one index among integer weights, the first whose cumulative weight exceeds the pick (the lower index on a tie), the state's low bits entering no pick; the run is deterministic per seed. The hole: the arriving record's levels at the one Node the credited quantum entered through set to 0, every line of the record there at the state of a Node with no level, exactly as the receding face removes a share (the advisor's second hand: for a spread record the form is quadratic, and subtracting one quantum's levels where less than a quantum stands would add form instead of removing it), which spreads by Rule3 alone as an event (no front is sent: a family has one level field, and an act ending a record's shares on arrival would end every other quantum's wave it reached); the record's count, not the levels, goes down by one. The lay of a record at one Node: the levels of `count` quanta of a pair standing at one Node at the pair's own rotation, the amplitude A from the count's measure, A^2 = count T den^2 div (2 (den^2 - num^2)) so that the share 6 den A^2 sin^2 omega reads the count (the count is the record's share), and for the massless pair the two levels alike, A^2 = count T div 2; a direction taken from the levels of the part the quantum leaves, so the phase passes with the quantum (the mathematician's hand, the arriving quantum's phase 0 on a real line of light); the level before the level now turned by the rest rotation, cos omega = num / den, in the record's own sense; the remainder at the lay's origin, the half wall. The face (the mathematician's hand, the advisor's second, two hands; the owner's word, the node_detector operates Rule3 on the families): the giver's write is no assignment but one value presented at one Port of the Node for two intervals, the least arrival that lifts Rule3's numerator at the Node into the target's window, arr_face = ceiling((w a* - SUM over the other Ports of R_j arr_j - S a_now + w a_before - r) / R_face) with the target a* = 0, so that Rule3 itself writes the level 0 and its own remainder, below one read coefficient; the second interval's face makes the new now 0 and the new before the 0 of the first, the record's lines at (0, 0) from then where every neighbour stands at 0, and the hole spreading by Rule3 alone elsewhere; the same value presented on the way back, Rule3's inverse crosses the click bit for bit, the Node knowing neither (the faces the books' log, `Face`). The undepleted beam (the two hands' line, the owner's word for the simple solution): a record of many quanta per Node is a beam, and the absorption of one of its quanta is read in the books and not written on the board, exact as the count per Node grows, so where the record's booked share at the Node, the share the credit reads there (`share.share`, the conserved form's density at the Node over 2 p_i^2 G^2), is above its own quantum W_rec, no face is booked and no front begins, the record's levels stand, its count in the books goes down by one and the board's share then exceeds the books' count by the quanta taken, the deficit, a tally per family printed in the books' line by name (`Lattice.books`); the hole to 0, both levels to 0, stands where the booked share at the Node is at most W_rec, the record there being local and whole, the front erasing what spread beyond it where the count reaches 0 (`meeting.faced`); the count goes down by one either way, the front erases only a record at count 0, and the inverse presents the kept value whatever the target."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.ports import AXES, PORTS, SIDES
from event_universe.core.rule3 import NO_READ, division_fixed_point, division_forward, rule3

SCALE_OF = (
    2  # the emission's reference scale, the count's wall times itself: its rounding below one level
)


def drawn(
    state: int, multiplier: int, increment: int, modulus: int, weights: list[int]
) -> tuple[int, int]:
    """One draw of the NodeDetector (ALGEBRA.md, The click is the meeting, How it chooses; the mathematician's line #1793 comment 5981866600 K1, the advisor's breaker 5981736108, two hands): the generator's next state x = (multiplier x + increment) mod modulus by the division act, the state kept in the books and advanced once per draw; the pick the state's fraction of the weights' total, (x times total) div modulus by the same act (the product above 2^width at any total above 1, so the state, the total and the generator's integers are taken as Python's integers, never a hardware integer that wraps; the reviewer's #1793 comment 5982079576 D), and among the weights (each at or above 0, their total above 0) the index drawn the first whose cumulative weight exceeds the pick, the lower index on a tie, a weight of 0 never drawn; returns the index and the state after. The index i is drawn at ceiling(c_(i+1) modulus / total) - ceiling(c_i modulus / total) states of the modulus, c_i the cumulative weight below it, within one of w_i modulus / total, so P(i) = w_i / total to within 2^-width over the generator's full period whatever the seed and whatever the total; a total at or above the modulus is admitted by the pick and drawn at every index to within 2^-width, so no refusal of a total enters (K2); the state's low bits, each with the period of its own count, enter no pick (until the clean main of 2026-10-04 the pick was the state modulo the total, so a power-of-two total was a cycle of the low bits, [1, 1] alternating and [1, 7] hitting once in eight, and an even total alternated the lowest index's possible intervals)."""
    state, modulus = int(state), int(modulus)  # Python's integers: the product below is above 2^width
    state = int(division_forward(int(multiplier) * state + int(increment), modulus, 0)[1])
    total = sum(int(weight) for weight in weights)
    if total <= 0:
        raise ValueError("the NodeDetector draws among weights whose total is above 0")
    pick = int(division_forward(state * total, modulus, 0)[0])
    reached = 0
    for index, weight in enumerate(weights):
        reached += int(weight)
        if pick < reached:
            return index, state
    return len(weights) - 1, state


@dataclass
class Face:
    """One presented value, the face: the record's family and line, the Node at the file's coordinates, the Port preferred (the first in Port order whose read is not 0 at the step is taken and kept), the interval at whose step it is presented, the value, None until the forward step computes it, the value the inverse presents again, and the front's taper (`fraction`, (p, q): the target the fraction p / q of Rule3's own level by the division act on its size, toward 0, so that a level of size 1 falls to 0 at any fraction below 1 and no leading edge of ones rides the band; None the target 0, the hole to 0; src/event_universe/front.py)."""

    family: int
    line: int
    at: tuple[int, int, int]
    port: int
    interval: int
    value: int | None = None
    fraction: tuple[int, int] | None = None


def face_value(total: int, read: int) -> int:
    """The least arrival that lifts Rule3's numerator into the target's window [0, R_face), ceiling(-total / R_face), the division act's floor negated, with `total` the numerator without the face Port's term less w a* (a* the target, 0 for the hole to 0): R_face x value + total in [0, R_face), within [0, w) since R_face <= w, so the level next is a* and the remainder Rule3's own."""
    return -int(division_forward(total, read, 0)[0])


def presented(
    arrived: tuple[Any, ...],
    reads: tuple[Any, ...],
    self_coefficient: Any,
    wall: Any,
    now: Any,
    other: Any,
    carry: Any,
    faces: list[Face],
    offset: tuple[int, int, int],
    direction: int,
) -> tuple[Any, ...]:
    """The six arrivals of a line with the faces' values presented at their Ports and Nodes, every other arrival the neighbour's own: forward the value is computed from the arrivals, the Node's two levels and its remainder as the step reads them (`face_value` at the target, 0, the hole to 0, or the taper's fraction of Rule3's own level, the first Port from the preferred one whose read is not 0 at the Node, kept in the face; a Node with every read 0 refused by name), backward the kept value is presented again, so the inverse runs through the click; the arrays copied once per Port touched."""
    found, copied = list(arrived), set()
    for face in faces:
        at = (face.at[0] + offset[0], face.at[1] + offset[1], face.at[2] + offset[2])
        here = [int(np.asarray(read)[at]) if np.ndim(read) else int(read) for read in reads]
        if face.value is None:
            assert direction == 1, "a face is computed forward and presented again backward"
            ports = [p for p in [*range(face.port, len(here)), *range(face.port)] if here[p] != 0]
            if not ports:
                raise ValueError(
                    f"the face at the Node {list(face.at)} finds every read 0: no open Link"
                )
            face.port = ports[0]
            coefficient = int(
                np.asarray(self_coefficient)[at] if np.ndim(self_coefficient) else self_coefficient
            )
            self_term = coefficient * int(now[at])
            rest = -int(wall) * int(other[at]) + int(carry[at])
            rest += sum(here[p] * int(found[p][at]) for p in range(len(here)) if p != face.port)
            target = 0  # the hole to 0, every face's target but the taper's
            if (
                face.fraction is not None
            ):  # the front's taper: the fraction of Rule3's own level, toward 0
                own = here[face.port] * int(found[face.port][at])  # the face Port's arrival untouched
                own_level = int(division_forward(self_term + rest + own, int(wall), 0)[0])
                scaled = int(division_forward(face.fraction[0] * abs(own_level), face.fraction[1], 0)[0])
                target = (
                    scaled if own_level >= 0 else -scaled
                )  # a level of size 1 goes to 0 at any fraction
            face.value = face_value(self_term + rest - int(wall) * target, here[face.port])
        if face.port not in copied:
            found[face.port] = np.array(found[face.port], copy=True)
            copied.add(face.port)
        found[face.port][at] = face.value
    return tuple(found)


def squared(count: int, action: int, pair: tuple[int, int], laid: int = 1) -> int:
    """A^2 of `count` quanta standing at one Node on `laid` lines alike (one, the taker's part): isqrt(count^2 T^2 den^2 div (4 laid^2 (den^2 - num^2))), one root on the whole product by the fixed point of the division act, the invariant 2 A^2 sin omega = T per quantum per line (ALGEBRA.md, the absorption's A^2 = (N + 1) T / (2 sin omega_part); the two hands' word on R8, #1793), count T div (2 laid) for the massless pair, the number `amplitude` takes the root of."""
    num, den = pair
    gap = den * den - num * num
    if gap:
        half = count * action * den  # 2 laid A^2 sqrt(gap) = count T den: the root of the whole product
        return division_fixed_point(int(division_forward(half * half, 2 * laid * 2 * laid * gap, 0)[0]))
    return int(division_forward(count * action, 2 * laid, 0)[0])


def spread(square: int, share: tuple[int, int]) -> int:
    """A region's Node's amplitude from the record's A^2 and the Node's share (weight, total) of the lay, isqrt(A^2 weight div total): A_n^2 = A^2 / n over n Nodes in equal counts (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment; the mathematician's hand)."""
    weight, total = share
    return division_fixed_point(int(division_forward(square * weight, total, 0)[0]))


def amplitude(count: int, action: int, pair: tuple[int, int], laid: int = 1) -> int:
    """The amplitude A of `count` quanta standing at one Node on `laid` lines alike (one, the taker's part): A^2 = count T den^2 div (2 laid (den^2 - num^2)), the share 6 den A^2 sin^2 omega per line over W_c = 3 den T the count, by the fixed point of the division act; for the massless pair, whose one-Node record has no rotation, A^2 = count T div (2 laid), the two levels alike (the lay by the count, `emission.laid_by_count`: every laid line of the record alike, the symmetric lay, the mathematician's hand)."""
    return division_fixed_point(squared(count, action, pair, laid))


def direction(re: int, im: int, size: int) -> tuple[int, int]:
    """A level pair of the size `size` in the direction of (re, im) by the division act, (size, 0) where the pair is 0: the phase of the part the quantum leaves passed to the part it enters."""
    norm = division_fixed_point(re * re + im * im)
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
    """The levels of `count` quanta of a plane standing at one Node, ((re_now, im_now), (re_before, im_before)): the amplitude `amplitude` in the direction `phase`, the level before the level now turned by the rest rotation in the record's sense, re_b = (re num - sense im s) div den and im_b = (im num + sense re s) div den with s = the fixed point of den^2 - num^2 (sin omega den), so the Wronskian re_now im_before - im_now re_before is sense x A^2 sin omega; both 0 at the count 0."""
    if count <= 0:
        return (0, 0), (0, 0)
    num, den = pair
    re, im = direction(phase[0], phase[1], spread(squared(count, action, pair), share))
    sine = sense * division_fixed_point(den * den - num * num)
    re_before = int(division_forward(re * num - im * sine, den, 0)[0])
    im_before = int(division_forward(im * num + re * sine, den, 0)[0])
    return (re, im), (re_before, im_before)


def invariant(
    count: int, action: int, pair: tuple[int, int], laid: int, share: tuple[int, int] = (1, 1)
) -> int:
    """The amplitude of `count` whole quanta laid at one Node on a record of `laid` real lines or planes, every one alike, by the invariant (the two hands, the advisor's (b) and (c) and the mathematician's hand: one unit of the invariant 2 A^2 sin omega = T per quantum over the record's lines, A_l^2 = count T den div (2 s laid) with s the fixed point of den^2 - num^2, sin omega den; the proton's three planes at T / 6 at [0, den], the electron's plane at 148, the antineutrino's real line at the excess rotation), the generator's one-Node declaration (tools/pixel_mode.py, `pixel_record`) in the engine for the lay of a record converted whole at the start, cut at its Node (`meeting.relaid`); the share form of `amplitude` beside it, the reader's parts' lay, and the lay by the count of `standing` at the massless pair for a whole quantum given at an open-Link Node (the two hands); 0 at the count 0 and on a pair with no rotation (a massless lay has no finite amplitude by the invariant)."""
    num, den = pair
    sine = division_fixed_point(den * den - num * num)
    if count <= 0 or sine == 0:
        return 0
    return spread(int(division_forward(count * action * den, 2 * sine * laid, 0)[0]), share)


def laid_pairs(
    count: int,
    action: int,
    pair: tuple[int, int],
    sense: int,
    plane: bool,
    laid: int,
    share: tuple[int, int] = (1, 1),
) -> list[tuple[int, int]]:
    """The level pairs (now, before) of `count` whole quanta on every line of a record at one Node, the lay of a record converted whole at the start (the two hands; the generator's one-Node declaration, equal phases): per real line or plane the amplitude `invariant` on the level now and the level before turned by the pair's rest rotation, (A, A num div den), and for a plane its second line's pair, the sense, (0, sense A s div den) with s the fixed point of den^2 - num^2, so that its Wronskian is sense x A^2 sin omega; `laid` pairs for real lines, 2 `laid` for planes, every one alike; every level 0 at the count 0."""
    num, den = pair
    size, sine = invariant(count, action, pair, laid, share), division_fixed_point(den * den - num * num)
    real = (size, int(division_forward(size * num, den, 0)[0]))
    turned = (0, sense * int(division_forward(size * sine, den, 0)[0]))
    return [pair for _ in range(laid) for pair in ((real, turned) if plane else (real,))]


def exact_total(action: int, resonance: tuple[int, int]) -> int:
    """The total of the squared amplitudes of one quantum of light at the resonance, S = SUM A^2 with 2 S sin Omega = T, the exact root isqrt((T den div 2)^2 div (den^2 - num^2)) by the fixed point of the division act (the advisor's form and the mathematician's hand, two hands), one root of the whole product; one line's share of a plane's quantum, the two lines together (the taker's lay), the source in time's total (`emission.laid_increment`, `emission.emitted_quantum`); the one-line packet's root is `line_total`; the NodeDetector's own act at the lay and no act of the interval."""
    num, den = resonance
    half = int(
        division_forward(action * den, 2, 0)[0]
    )  # T den div 2, exact for the file's T, a power of two
    return division_fixed_point(int(division_forward(half * half, den * den - num * num, 0)[0]))


def line_total(action: int, resonance: tuple[int, int]) -> int:
    """The total of the squared amplitudes of one quantum of light on one real line, SUM a^2 = T / sin Omega, the exact root isqrt(T^2 den^2 div (den^2 - num^2)) by the fixed point of the division act, twice S (the mathematician's hand and the advisor's second, two hands): S = T / (2 sin Omega) (`exact_total`) is the SUM a^2 of one line of a plane record carrying one quantum, the taker's lay, the two lines together 2 A^2 sin Omega = T, and the packet is laid on the light record's first line alone, so the packet's root is T / sin Omega for a one-line packet (or S on each of two lines a quarter turn apart, the polarisation a world's choice by name; the branch lays one line); 43,962 at T = 32,768 and [2, 3]; one root at the lay, the NodeDetector's own act and no act of the interval. The source in time keeps S (`emission.laid_increment`): a source's increments are a drive and the field's energy is the response's."""
    num, den = resonance
    return division_fixed_point(
        int(division_forward(action * action * den * den, den * den - num * num, 0)[0])
    )


def rotated(first: int, second: int, doubled: int, unit: int, count: int) -> list[int]:
    """Rule3's rotation act (ALGEBRA.md #the-four-acts (b)) from the levels `first` and `second`: a_next = (doubled a_now + r) div unit - a_before with the remainder kept, `count` levels in all; unit cos(n theta) from (unit, doubled div 2) and unit sin(n theta) from (0, unit sin theta) at 2 unit cos theta = doubled."""
    levels, carry = [first, second], 0
    while len(levels) < count:
        following, carry = rule3(NO_READ, NO_READ, doubled, unit, levels[-1], levels[-2], carry)
        levels.append(int(following))
    return levels[:count]


def transverse_cosine(width: int, unit: int) -> int:
    """unit cos(pi / (width + 1)), the lowest mode of a top-hat of `width` Nodes with zero ends, by the rotation act: the doubled cosine of the step pi / (2 (width + 1)) is the largest integer at which the rotation from the unit reaches 0 within width + 1 steps (bisection on the integers, no root and no table, as the packet lay's generator finds its cosines), and two steps of it are the mode's cosine."""
    lower, upper = 0, 2 * unit
    while upper - lower > 1:
        middle = int(division_forward(lower + upper, 2, 0)[0])
        if min(rotated(unit, int(division_forward(middle, 2, 0)[0]), middle, unit, width + 2)) <= 0:
            lower = middle
        else:
            upper = middle
    seeds = 2  # the recurrence's two seeds; the level after them is the cosine's
    return rotated(unit, int(division_forward(lower, 2, 0)[0]), lower, unit, seeds + 1)[seeds]


def below_the_band(num: int, den: int) -> bool:
    """Whether a resonance [num, den] lies below the width-one guide's band, no axis carrying the quantum: den cos k = (PORTS num - (PORTS - SIDES) den) div SIDES below -den, that is PORTS num below (PORTS - 2 SIDES) den (the guide of `emission.radiated_total`; the mathematician's hand)."""
    return PORTS * num < (PORTS - SIDES - SIDES) * den


def along_cosine(
    light: tuple[int, int], resonance: tuple[int, int], width: int, unit: int
) -> int | None:
    """The doubled cosine 2 unit cos k_z of a packet's wave number along its axis, from the light family's band with the transverse mode of its width (the mathematician's hand, the advisor's second, two hands): cos Omega = (num_l / (3 den_l)) (cos k_z + 2 cos k_perp) with k_perp = pi / (width + 1) the lowest mode of the top-hat across, so 2 unit cos k_z = (6 unit den_l num) div (num_l den) - 2 x (2 unit cos k_perp), the two transverse axes each at the doubled cosine, every cosine at the unit by the rotation act; None where the width cannot carry Omega, cos k_z not strictly inside (-1, 1) (the band's edge k_z = 0, a wave of no wave number, refused with the outside; the top-hat's spectrum spreads the frequency by about (num_l / (3 den_l)) k_perp^2 / sin Omega, the open board's tolerance)."""
    (num_l, den_l), (num, den) = light, resonance
    across = 2 * transverse_cosine(width, unit)  # 2 unit cos k_perp, one transverse axis
    doubled = int(division_forward(PORTS * unit * den_l * num, num_l * den, 0)[0]) - (AXES - 1) * across
    return doubled if -2 * unit < doubled < 2 * unit else None


def envelope(total: int, span: int, across: int) -> list[int]:
    """A packet's amplitude per Node slice by slice along its axis in the energy form (the mathematician's hand, on the advisor's derivation, step 5, two hands): the energy left R_0 the packet's root (`line_total`, T / sin Omega for the one-line packet), each slice's energy R_t div span over the `across` Nodes of its cross-section, the amplitude per Node a_t = isqrt((R_t div span) div across), the carry R_(t+1) = R_t - across a_t^2, so that the energy decays at 1 / span per slice and the amplitude at 1 / (2 span), the body's survival under the constant hazard and nature's natural linewidth, the Lorentzian of full width 1 / span; the lay ends where a_t falls below 1, the deficit left below span level squared per Node (47 of 43,962, the one-line root at T = 32,768 and [2, 3], span 48, one Node across, the mathematician's number); the length L = 2 span ln a_0 in the continuous line (326 at a_0 = 30) and longer in the integers, whose tail at a_t = 1 falls linearly (456 slices there, SUM a_t^2 = 43,915)."""
    found: list[int] = []
    left = total
    while True:
        energy = int(division_forward(left, span, 0)[0])
        amplitude = division_fixed_point(int(division_forward(energy, across, 0)[0]))
        if amplitude == 0:
            return found
        found.append(amplitude)
        left -= across * amplitude * amplitude
