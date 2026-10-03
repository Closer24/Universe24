"""The click written on the GameBoard (ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision of 2026-10-02: after a click the paths are cancelled on the GameBoard, not in the clicks' books, Rule3 kept; the owner's word of 2026-10-03, the click the meeting of two quanta at one Node, the write their exchange there): the instruments' acts outside Rule3, taken by the engine's loop at the instruments' reports from outside the Node, as the lay and the receding face are; the Node knows nothing of them and no family of clicks exists. The draw: the instrument's generator, declared in the world file with its seed, x <- (multiplier x + increment) mod modulus by the division act, and one index among integer weights, the first whose cumulative weight exceeds x mod total (the lower index on a tie); the run is deterministic per seed. The hole: the arriving record's levels at the one Node the credited quantum entered through set to 0, every line of the record there at the state of a Node with no level, exactly as the receding face removes a share (the advisor's second hand: for a spread record the form is quadratic, and subtracting one quantum's levels where less than a quantum stands would add form instead of removing it), which spreads by Rule3 alone as an event (no front is sent: a family has one level field, and an act ending a record's shares on arrival would end every other quantum's wave it reached); the record's count, not the levels, goes down by one. The lay of a record at one Node: the levels of `count` quanta of a pair standing at one Node at the pair's own rotation, the amplitude A from the count's measure, A^2 = count T den^2 div (2 (den^2 - num^2)) so that the share 6 den A^2 sin^2 omega reads the count (the count is the record's share), and for the massless pair the two levels alike, A^2 = count T div 2; a direction taken from the levels of the part the quantum leaves, so the phase passes with the quantum (the mathematician's 174 (a), the arriving quantum's phase 0 on a real line of light); the level before the level now turned by the rest rotation, cos omega = num / den, in the record's own sense; the remainder at the lay's origin, the half wall (174 (b)). The face (the mathematician's 193, 195 and 197, the advisor's second, #1572 comment 5963391333, two hands; the owner's word of 2026-10-03, 03:22 Israel, the detector operates Rule3 on the families): the giver's write is no assignment but one value presented at one Port of the Node for two intervals, the least arrival that lifts Rule3's numerator at the Node into the target's window, arr_face = ceiling((w a* - SUM over the other Ports of R_j arr_j - S a_now + w a_before - r) / R_face) with the target a* = 0, so that Rule3 itself writes the level 0 and its own remainder, below one read coefficient; the second interval's face makes the new now 0 and the new before the 0 of the first, the record's lines at (0, 0) from then where every neighbour stands at 0, and the hole spreading by Rule3 alone elsewhere; the same value presented on the way back, Rule3's inverse crosses the click bit for bit, the Node knowing neither (the faces the books' log, `Face`)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.rule3 import division_fixed_point, division_forward


def drawn(
    state: int, multiplier: int, increment: int, modulus: int, weights: list[int]
) -> tuple[int, int]:
    """One draw of the instrument: the generator's next state x = (multiplier x + increment) mod modulus, and among the weights (each at or above 0, their total above 0) the first index whose cumulative weight exceeds x mod total, the lower index on a tie; returns the index and the state after."""
    state = int(division_forward(multiplier * state + increment, modulus, 0)[1])
    total = sum(weights)
    if total <= 0:
        raise ValueError("the instrument draws among weights whose total is above 0")
    pick = int(division_forward(state, total, 0)[1])
    reached = 0
    for index, weight in enumerate(weights):
        reached += weight
        if pick < reached:
            return index, state
    return len(weights) - 1, state


@dataclass
class Face:
    """One presented value, the face: the record's family and line, the Node at the file's coordinates, the Port preferred (the first in Port order whose read is not 0 at the step is taken and kept), the interval at whose step it is presented, and the value, None until the forward step computes it, the value the inverse presents again."""

    family: int
    line: int
    at: tuple[int, int, int]
    port: int
    tick: int
    value: int | None = None


def face_value(total: int, read: int) -> int:
    """The least arrival that lifts Rule3's numerator into the target's window [0, R_face), ceiling(-total / R_face), the division act's floor negated, with `total` the numerator without the face Port's term: R_face x value + total in [0, R_face), within [0, w) since R_face <= w, so the level next is 0 and the remainder Rule3's own."""
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
    """The six arrivals of a line with the faces' values presented at their Ports and Nodes, every other arrival the neighbour's own: forward the value is computed from the arrivals, the Node's two levels and its remainder as the step reads them (`face_value`, the first Port from the preferred one whose read is not 0 at the Node, kept in the face; a Node with every read 0 refused by name), backward the kept value is presented again, so the inverse runs through the click; the arrays copied once per Port touched."""
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
            total = int(
                np.asarray(self_coefficient)[at] if np.ndim(self_coefficient) else self_coefficient
            )
            total = total * int(now[at]) - int(wall) * int(other[at]) + int(carry[at])
            total += sum(here[p] * int(found[p][at]) for p in range(len(here)) if p != face.port)
            face.value = face_value(total, here[face.port])
        if face.port not in copied:
            found[face.port] = np.array(found[face.port], copy=True)
            copied.add(face.port)
        found[face.port][at] = face.value
    return tuple(found)


def amplitude(count: int, action: int, pair: tuple[int, int]) -> int:
    """The amplitude A of `count` quanta standing at one Node: A^2 = count T den^2 div (2 (den^2 - num^2)), the share 6 den A^2 sin^2 omega over W_c = 3 den T the count, by the fixed point of the division act; for the massless pair, whose one-Node record has no rotation, A^2 = count T div 2, the two levels alike."""
    num, den = pair
    gap = den * den - num * num
    square = division_forward(count * action * den * den, 2 * gap, 0)[0] if gap else None
    return division_fixed_point(
        int(square if square is not None else division_forward(count * action, 2, 0)[0])
    )


def direction(re: int, im: int, size: int) -> tuple[int, int]:
    """A level pair of the size `size` in the direction of (re, im) by the division act, (size, 0) where the pair is 0: the phase of the part the quantum leaves passed to the part it enters."""
    norm = division_fixed_point(re * re + im * im)
    if norm == 0:
        return size, 0
    return int(division_forward(re * size, norm, 0)[0]), int(division_forward(im * size, norm, 0)[0])


def standing(
    count: int, action: int, pair: tuple[int, int], phase: tuple[int, int], sense: int
) -> tuple[tuple[int, int], tuple[int, int]]:
    """The levels of `count` quanta of a plane standing at one Node, ((re_now, im_now), (re_before, im_before)): the amplitude `amplitude` in the direction `phase`, the level before the level now turned by the rest rotation in the record's sense, re_b = (re num - sense im s) div den and im_b = (im num + sense re s) div den with s = the fixed point of den^2 - num^2 (sin omega den), so the Wronskian re_now im_before - im_now re_before is sense x A^2 sin omega; both 0 at the count 0."""
    if count <= 0:
        return (0, 0), (0, 0)
    num, den = pair
    re, im = direction(phase[0], phase[1], amplitude(count, action, pair))
    sine = sense * division_fixed_point(den * den - num * num)
    re_before = int(division_forward(re * num - im * sine, den, 0)[0])
    im_before = int(division_forward(im * num + re * sine, den, 0)[0])
    return (re, im), (re_before, im_before)


def born(upper: tuple[int, int], lower: tuple[int, int]) -> tuple[int, int]:
    """The pair of the born quantum's rotation, the resonance omega_L = omega_e - omega_g (the mathematician's 174 (c), the advisor's second; the one place of the choice between the resonance and the share's rotation sin omega_L = sin omega_e - sin omega_g): cos omega_L = cos omega_e cos omega_g + sin omega_e sin omega_g as [num_e num_g + s_e s_g, den_e den_g] with s the fixed point of den^2 - num^2 (sin omega den); the massless pair for parts of one pair, whose transition has no rotation, so the quantum is laid by its count alone; the giving's lay (`meeting.given_quantum`) calls it with light's own pair and lays at light's own pair, the two levels alike: the giving's frequency (T4) waits on the packet lay; a one-Node lay carries no frequency (the mathematician's 205, #1572 comment 5964520368)."""
    (n_e, d_e), (n_g, d_g) = upper, lower
    s_e, s_g = division_fixed_point(d_e * d_e - n_e * n_e), division_fixed_point(d_g * d_g - n_g * n_g)
    num, den = n_e * n_g + s_e * s_g, d_e * d_g
    return (den, den) if num >= den else (num, den)
