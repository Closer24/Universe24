"""The generator makes a body (ALGEBRA.md #the-generator, the generator is Rule3; the model owner's word of 2026-09-28, 22:05 Israel: no body is reduced to one Node, the generator generates a whole body): the mode file of a world of bodies and the bodies themselves. A body is its quanta, M, about a centre; the world declares it with one Node carrying M (a new body) or with its Nodes and their counts (a body laid before, laid anew here). The generator finds the body's fixed point in whole integers: the counts at its Nodes source every held row of the universe file at the row's level weight, the rest of each row by the start (features/start: the division act iterated from nothing until the levels repeat) is the level every record reads, the body's record is the standing record Rule3 makes in those paces, the held rows then rest under that record by the engine's own start (`start_content`, one act with `GameBoard.start`: the form of the record as the hold books it over the write's wall, the lay and the rest iterated to the fixed point; the count is the seed of the first pass alone), and the counts are that record's share in quanta at the paces of its read in those rests (ALGEBRA.md #the-count-is-the-records-share) at every Node of the body's region, until the counts return themselves within the rounding, each round taking the half step from the counts toward the share (the deep well overshoots under the whole step); the body's Nodes are then the Nodes carrying a quantum, its region those Nodes and a Link around them (widened a Link a round while the share reaches a quantum there, narrowed where it falls below one; the region names the body's Nodes and where its counts are read, not where its record is iterated), and the record written is the top mode of the read act on the board as declared (`on_the_board`: a mode cut at the region is no mode of the board's and relaxes when laid), the content it stands in the board's. The counts the world declares are the engine's own reading at the start, the record's share in quanta at the paces of its read, the held rows at the rests the engine's start lays under the laid records (`read_at_the_start` calls the same act), so one body's declaration is the gate's reading within the rounding. A body of a plane turned by a holder of the sign (ALGEBRA.md, The sign holder rotates the two-part record; The atom is a bound body of the holder of the sign) is laid as the turned top mode (`turned_mode`): the power iteration of Rule3's read with the arrivals turned by the Link angles and the Node by the time angle, in the content holders' paces, the holder under the rotation entering no pace; its region is the board as kept, where its record stands, and where no Node carries a whole quantum of it (the law's count 1 over the Nodes of its mode) its count stands at its declared Node, which the gate admits within its rounding. A body named by `--pixel` is laid as the one-Node record of its quanta at its declared Node, a declaration by name and no fixed point (the frozen proton, examples/events/frozen_proton/build_world.py). The arrays are of the kind the universe's width chooses, as the loader's are (`loader.world.kind_of`)."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass, replace
from fractions import Fraction
from functools import cache
from math import lcm
from pathlib import Path
from typing import Any, cast

import numpy as np

from event_universe import node
from event_universe.bookings import booked_sources
from event_universe.core import paces
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import (
    NO_READ,
    coefficients,
    division_fixed_point,
    division_forward,
    rule3,
)
from event_universe.features import rotation
from event_universe.features.start import (
    RestCollapses,
    Sourced,
    held_rests,
    returned,
    settled_rows,
)
from event_universe.loader.derived import FamilyRule, held_write, turns, with_records
from event_universe.loader.faces import faces_of
from event_universe.loader.keys import AXES, weights_of
from event_universe.loader.lay import COMPACT, FIXED_POINT, Lay, lay_of
from event_universe.loader.universe import universe_of
from event_universe.loader.world import kind_of
from event_universe.node import Record, empty_state, ports, record_slice, wronskian
from event_universe.node import read as content_read
from event_universe.share import quanta_of, share
from event_universe.world_files import input_digest, world_files

Axis = tuple[int, int, int]
type Angles = (
    node.Angles | None
)  # a turned record's angles at every Node (the time's numerators, the three odd lines), None for a record no holder turns


@dataclass(frozen=True)
class Board:
    """The world's board as Rule3 sees it: its shape, its face rule (which axes wrap, the Nodes beyond it), the universe's Gamma and T, a record's pair [num, den] as the file writes it, the width's largest integer, the Link's unit and the kind of the arrays the width chooses."""

    shape: Axis
    wrap: Wrap
    gamma: int
    action: int
    pair: tuple[int, int]
    width: int  # the largest integer of the universe's width, 2^width - 1
    unit: int  # the Link's unit G, the run's declaration like Gamma (ALGEBRA.md #the-paces)
    kind: type = np.int64  # the arrays' kind by the width, the loader's one choice (`kind_of`)

    @property
    def room(self) -> int:
        """The largest integer a read of the generator may reach: the host's where the arrays are the hardware's integers, the file's width where they are Python's (exact at any width)."""
        return self.width if self.kind is object else min(self.width, MAX_WORK_INT)


def board_of(
    shape: Axis, wrap: Wrap, gamma: int, integers: dict[str, Any], pair: tuple[int, int]
) -> Board:
    """The board of a record's pair from the world's shape and face rule and the universe's integers (Gamma, T, the width and the Link unit), the arrays' kind by the width."""
    width = int(integers["width"])
    return Board(
        shape,
        wrap,
        gamma,
        int(integers["quantum_action"]),
        pair,
        int(2**width - 1),
        int(integers["link_unit"]),
        kind_of(width),
    )


@dataclass(frozen=True)
class Standing:
    """A body's standing record over its window: the share in quanta its record carries over the region at the vacuum's paces (`carried`, the summed share rounded once to whole quanta, and `share` the sum itself in the current's units), the window's length (the period is [window, 2]), the amplitude b, the clock pair [next + before, now] at the largest level at the centre, the two levels over the board at that moment with the next level after it, and for a plane turned by a holder of the sign its second line's three levels (`second`: im now, im before, im next), None on a real record."""

    carried: int
    window: int
    amplitude: int
    clock: tuple[int, int]
    now: np.ndarray
    before: np.ndarray
    next: np.ndarray
    share: int = 0
    second: tuple[np.ndarray, np.ndarray, np.ndarray] | None = None


def step(
    board: Board, content: np.ndarray, now: np.ndarray, before: np.ndarray, remainder: np.ndarray
) -> np.ndarray:
    """One interval of Rule3 on the whole board, the engine's own form: the six arrivals through the Ports (0 beyond a face, the wrap on a periodic one, `node.ports`), the coefficients from the composed paces of the content at every Node with no tension (core.rule3, core.paces, ALGEBRA.md #the-paces), the division by the wall with the remainder kept at the Node."""
    reads, self_coefficient, wall = coefficients(
        board.pair[0],
        board.pair[1],
        board.gamma,
        *paces.node_paces(board.gamma, content),
        None,
        board.unit,
    )
    arrivals = ports(now, board.wrap)
    nxt, remainder[...] = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
    return np.asarray(nxt, dtype=board.kind)


def rule_of(board: Board, content: np.ndarray) -> node.Rule:
    """Rule3's integers at every Node of the board from the composed paces of the content, no tension (`core.rule3.coefficients`)."""
    return coefficients(
        board.pair[0],
        board.pair[1],
        board.gamma,
        *paces.node_paces(board.gamma, content),
        None,
        board.unit,
    )


def turned_arrivals(
    board: Board, re: np.ndarray, im: np.ndarray, links: tuple[Any, Any, Any]
) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """A plane's six arrivals under the Link angles as the engine reads them (`node.turned_ports`, the pair through the +a Port turned by the Link's odd level over the wall 4 Gamma and through the -a Port by its opposite): the plain arrivals where no odd line stands (the shear by 0 being the identity), the turned ones otherwise."""
    if not any(bool(np.asarray(level).any()) for level in links):
        return ports(re, board.wrap), ports(im, board.wrap)
    turned_re, turned_im = node.turned_ports((re, im), links, 2 * 2 * board.gamma, board.wrap)
    return tuple(turned_re), tuple(turned_im)


def turned_step(
    board: Board,
    content: np.ndarray,
    angles: node.Angles,
    re: Record,
    im: Record,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """One interval of Rule3 on a plane under the rotation, the engine's own act (`node.step_plane` after `node.turned_before`'s turn of the level before, u = e^(-i theta) z_before by the time angle; the arrivals turned by the Link angles; the stepped pair turned back by the time angle), the remainders returned beside the two levels next; a reading of a laid plane as the engine steps it, every number the engine's."""
    time = angles[0]
    u = rotation.turned(re.before, im.before, -time, 2 * board.gamma)
    planes = (replace(re, before=np.asarray(u[0])), replace(im, before=np.asarray(u[1])))
    lines, _booking = node.step_plane(*planes, rule_of(board, content), board.wrap, angles, board.gamma)
    return (
        np.asarray(lines[0].now, dtype=board.kind),
        np.asarray(lines[1].now, dtype=board.kind),
        np.asarray(lines[0].remainder, dtype=board.kind),
        np.asarray(lines[1].remainder, dtype=board.kind),
    )


def share_of(board: Board, content: np.ndarray | int, now: np.ndarray, before: np.ndarray) -> np.ndarray:
    """The record's weighted share at every Node in the current's units, the engine's own `share.share` at the paces of the content (ALGEBRA.md #the-count-is-the-records-share): the conserved form's Node term over the Link's pace squared less the plain Link term."""
    zero: np.ndarray = np.zeros(board.shape, dtype=board.kind)
    record = Record(now.astype(board.kind), before.astype(board.kind), zero)
    found = share(board.pair, record, board.wrap, board.gamma, content, None, board.unit)
    return np.asarray(found, dtype=board.kind)


def read_quanta(share_now: np.ndarray | int, den: int, action: int, kind: type = np.int64) -> np.ndarray:
    """A share read in quanta at every Node, the engine's own reading (`share.quanta_of`): (share + W_c div 2) div W_c with W_c = 3 den T by Rule3's division act (ALGEBRA.md #the-count-is-the-records-share), in the arrays' kind."""
    return np.asarray(quanta_of(share_now, 3 * den * action, kind))


def period_reading(
    board: Board, content: np.ndarray, node: Axis, state: list[np.ndarray]
) -> tuple[int, int, tuple[int, int], np.ndarray, np.ndarray, np.ndarray] | None:
    """One whole period of the record at the centre, from the interval its level returns upward through 0 to the next such return: the period's length, the largest |now| at the centre and the pair [next + before, now] with the three levels over the board at that moment; None when the whole state repeats before the level returns twice (a cloud, no record). `state` is [now, before, remainder], stepped in place."""
    now, before, remainder = state
    sign = 1 if now[node] > 0 else -1 if now[node] < 0 else 0
    length, largest, best, returned = 0, -1, None, False
    seen: set[bytes] = set()
    while (key := digest(now, before, remainder)) not in seen:
        seen.add(key)
        nxt = step(board, content, now, before, remainder)
        here = int(now[node])
        if here > 0 and sign <= 0:
            if returned and best is not None:
                state[:] = [now, before, remainder]
                return (length, largest, best[0], best[1], best[2], best[3])
            returned = True
        if here:
            sign = 1 if here > 0 else -1
        if returned:
            length += 1
            if abs(here) > largest:
                largest = abs(here)
                best = (
                    (int(nxt[node]) + int(before[node]), here),
                    now.copy(),
                    before.copy(),
                    nxt.copy(),
                )
        now, before = nxt, now
    return None


def digest(*arrays: np.ndarray) -> bytes:
    """A state's digest for the repeat searches, the arrays' bytes hashed so that the memory of a search is bounded on a large board (a repeat is read exactly on the digest, the tool's own bookkeeping and no number of the law); an array of Python's integers (the width above the host's) is hashed by its values' text, its bytes being the objects' addresses."""
    found = hashlib.sha256()
    for array in arrays:
        found.update(repr(array.tolist()).encode() if array.dtype == object else array.tobytes())
    return found.digest()


def agree(first: int, second: int) -> bool:
    """Two readings of a count within the rounding of its amplitude, ((|a - b| - 1) div 2)^2 at most the larger, as integer squares."""
    return bool(within(np.array(first - second), np.array(max(first, second))))


def within(off: np.ndarray, largest: np.ndarray) -> np.ndarray:
    """The law's gate at every Node, ((|a - b| - 1) div 2)^2 <= c by Rule3's division act, the root's inequality written as a square."""
    half = np.asarray(division_forward(np.abs(off) - 1, 2, 0)[0])
    return (np.abs(off) <= 1) | (half * half <= largest)


def on_the_board(board: Board) -> np.ndarray:
    """The Nodes of the board as declared, every Node but those beyond an inner face (nothing stands there): the region the top mode is iterated on and the record is written over. The standing state the engine steps is the top mode of the read act on the board as declared, its faces read as the engine reads them (0 beyond an open or a closed face, the wrap on a periodic one), and not on the body's region with 0 beyond: a mode of the cut operator is no mode of the board's (the Boss's word of 2026-10-02 on the fourth finding, the region's cut compressing the mode: in the pixel's start the mode cut a Link beyond the body's Nodes rotated at 1.3774 against the board's 1.3810 and carried 21 percent less share at the same amplitude, and released on the board it relaxed by a third at the centre)."""
    return np.ones(board.shape, dtype=bool) if board.wrap.beyond is None else ~board.wrap.beyond


def own_board(board: Board, others: np.ndarray) -> np.ndarray:
    """The board as declared less the other bodies' regions (their Nodes carrying a quantum and a Link around them, `others` their counts): the region a body's top mode is iterated on and its record written over. The power iteration finds the top mode of the read in the whole content, which sits in the deepest well; a second body laid in the first's sources needs its own mode, the top mode outside the first's region (laid on the whole board the second body's scale ran away to carry its quanta within its own region, its form collapsing the rest; the look's chain of two bodies, 2026-10-02); the bodies' regions never share a Node, and a body's mode is small at the other's region, so the cut costs it little."""
    return np.asarray(on_the_board(board) & ~dilated(others > 0, board.wrap), dtype=bool)


def dilated(mask: np.ndarray, wrap: Wrap) -> np.ndarray:
    """The mask and its six-neighbour surroundings (the wrap on a periodic axis, nothing beyond a face)."""
    grown = mask.copy()
    for axis in range(3):
        for sense in (1, -1):
            grown |= np.asarray(arrival(mask.astype(np.int64), axis, sense, wrap, 0)) > 0
    return grown


frozen_content = cache(
    paces.frozen_content
)  # the Link's zero at Gamma once per run of the tool (`paces.frozen_content` searches the clock's own power, minutes at a large Gamma)

ACTS_OF_A_HELD_ROW = 1 + 1  # the acts `held_rests` composes per held row: its rest's and its booking's
ROUNDINGS_OF_A_STEP = (
    1 + 1 + 1 + 1
)  # the acts composed in next + before - clock x now: now, before, next, the clock's level
SHEARS_OF_A_TURNED_STEP = (
    2 * (1 + 1 + 1)
)  # the two turns of a plane's step, the level before by the previous angle and the stepped pair by this interval's, three shears each, each a floor (features/rotation)


def rotation_spread(
    now: np.ndarray,
    before: np.ndarray,
    nxt: np.ndarray,
    where: np.ndarray,
    clock: tuple[int, int] | None = None,
) -> tuple[Fraction, int, Fraction]:
    """The one-step reading of a record in a content: the rotation (next + before) / now at every Node of `where` carrying a level, its median (the mode's clock as the body reads it), the number of Nodes read and the largest departure from the median in units of the Node's rounding 1 / |now|: next + before - clock x now is made of integers each rounded once, the two laid levels by the generator's scale act, next by the step's own act and the clock's level at the median's Node, so a record standing in the content departs at most one unit per act composed, `ROUNDINGS_OF_A_STEP`, at every Node (the power iteration's own integer fixed point at the pixel's amplitude departs up to 4.6 units in the rule's seed well, a GameBoard reading of 2026-10-02), and a record departing further is no mode of the step in that content; with `clock` the lay's own pair [next + before, now] stands in the median's place (a record of the law's count 1 stands on thousands of Nodes of a few levels, where the ratio is the rounding's and the median says nothing)."""
    read = where & (now != 0)
    sums, levels = (nxt + before)[read].tolist(), now[read].tolist()
    ratios = sorted(Fraction(int(s), int(level)) for s, level in zip(sums, levels, strict=True))
    if not ratios:
        return Fraction(0), 0, Fraction(0)
    median = ratios[len(ratios) // 2] if clock is None else Fraction(clock[0], clock[1])
    worst = max(
        abs(Fraction(int(s), int(level)) - median) * abs(int(level))
        for s, level in zip(sums, levels, strict=True)
    )
    return median, len(ratios), worst


Modes = dict[int, Any]  # the fine modes found in one content, by the fine unit they were iterated at


def scaled(board: Board, total: np.ndarray, to: int, largest: int | None = None) -> np.ndarray:
    """The division act to a unit: the level times the unit over its largest size (`largest`, the array's own where None), the array as it is where it is 0 everywhere."""
    largest = int(np.abs(total).max()) if largest is None else largest
    if largest == 0:
        return total
    return np.asarray(division_forward(total * to, largest, 0)[0], dtype=board.kind)


def reach_of(rule: node.Rule) -> int:
    """The largest sum of the rule's coefficients at a Node, |S| + SUM over the six Ports of R_ij, the room one level of the read takes."""
    reads, self_coefficient, _wall = rule
    return int((np.abs(np.asarray(self_coefficient)) + sum(np.asarray(read) for read in reads)).max())


def fine_mode(
    board: Board, content: np.ndarray, keep: np.ndarray, seed: np.ndarray, fine: int
) -> np.ndarray:
    """The iteration of the generator at the fine unit (ALGEBRA.md #the-generator (b)): Rule3's read act with the before-coefficient 0, a <- (SUM over the Ports of R_ij arr_j + S a) div w within `keep` (the board as declared, `on_the_board`) and 0 outside it, then the division act to the fine unit (the level times the unit over its largest size): the power iteration of the symmetric form's top mode, the body's bound mode; the stop is the first repeat of the integer vector, exact, no tolerance."""
    reads, self_coefficient, wall = rule_of(board, content)

    def read_of(a: np.ndarray) -> np.ndarray:
        total = np.asarray(rule3(reads, ports(a, board.wrap), self_coefficient, wall, a, 0, 0)[0])
        return np.where(keep, total, 0).astype(board.kind)

    a = scaled(board, np.where(keep, seed, 0).astype(board.kind), fine)
    seen: set[bytes] = set()
    while True:
        total = read_of(a)
        if not total.any():
            break
        a = scaled(board, total, fine)
        key = digest(a)
        if key in seen:
            break
        seen.add(key)
    return a


def top_mode(
    board: Board, content: np.ndarray, keep: np.ndarray, seed: np.ndarray, unit: int, modes: Modes
) -> tuple[np.ndarray, np.ndarray]:
    """The top mode at the amplitude `unit` and its read (`fine_mode` once per fine unit in one content, `modes`, the iteration not depending on the amplitude it is read at). The fine unit is derived from the width and never written, the largest at which the read of a level stays inside the room (`Board.room`, the host's width or the file's, over twice the sum of the coefficients at a Node, as the start derives its own, `features.start.unit_of`), so that the rounding trap of the iteration is far below the amplitude's rounding; the mode is then rounded once to the amplitude `unit` by the division act and read once more: returns the mode at the amplitude and its read, (SUM over the Ports of R_ij arr_j + S a) div w, the mode times its rotation 2 cos omega within the step's one act."""
    reads, self_coefficient, wall = rule = rule_of(board, content)
    fine = max(unit, int(division_forward(board.room, 2 * reach_of(rule), 0)[0]))
    if fine not in modes:
        modes[fine] = fine_mode(board, content, keep, seed, fine)
    a = scaled(board, modes[fine], unit)
    total = np.asarray(rule3(reads, ports(a, board.wrap), self_coefficient, wall, a, 0, 0)[0])
    return a, np.where(keep, total, 0).astype(board.kind)


ROUNDINGS_OF_THE_TURNED_READ = (
    1 + 1 + 1
)  # the acts composed in one turned iteration: the read div w, the time factor's division, the scale


def time_factor(time: Any, cosine: int, sine: int, fine: int, gamma: int) -> tuple[Any, Any]:
    """The standing condition of a turned plane at every Node as one fraction, 2 cos(Omega - theta_i) = numerator_i / wall_i (ALGEBRA.md, The sign holder rotates the two-part record, the engine's convention: e^(i theta) z_next + e^(-i theta) z_before = M z, so a record z = phi e^(-i Omega t) stands where (M phi)_i = 2 cos(Omega - theta_i) phi_i): with tan(theta_i / 2) = n_i / h the turn's own rationals, h = 2 Gamma (the time turn's wall, `node.step_plane`), cos theta_i = (h^2 - n_i^2) / (h^2 + n_i^2) and sin theta_i = 2 n_i h / (h^2 + n_i^2) (features/rotation), and the clock pair cos Omega = cosine / fine, sin Omega = sine / fine, 2 cos(Omega - theta_i) = 2 (cosine (h^2 - n_i^2) + sine 2 n_i h) / (fine (h^2 + n_i^2)); the wall above 0 while |Omega - theta| is below a quarter turn."""
    h = 2 * gamma
    square = h * h
    return 2 * (cosine * (square - time * time) + 2 * sine * time * h), fine * (square + time * time)


def turned_mode(
    board: Board, content: np.ndarray, angles: node.Angles, keep: np.ndarray, seed: np.ndarray, fine: int
) -> tuple[np.ndarray, np.ndarray, tuple[int, int]]:
    """The turned top mode at the fine unit (ALGEBRA.md, The atom is a bound body of the holder of the sign, step (4); The sign holder rotates the two-part record): the power iteration of Rule3's read with the arrivals turned by the Link angles (`turned_arrivals`, the odd lines' numerators as `node.turned_ports` turns them) and the Node by the time angle, z <- F(z) with F(z)_i = (M z)_i wall_i div numerator_i, M z = (S z + SUM over the Ports of R_ij e^(+-i theta_a) z_j) div w the turned read and numerator_i / wall_i = 2 cos(Omega - theta_i) the standing condition at the clock pair (`time_factor`), shifted by the unit, z <- F(z) + z, so that the band's bottom modes, whose eigenvalue under F has nearly the top's size with the opposite sign, fall near 0 while the top stands near 2 (the real top mode needs no shift, a hollow's S above 0 lifting its whole spectrum), then the division act to the fine unit by one factor on both lines (the mode's own scale; the rotation's phase free): the top mode of the standing condition in the content holders' paces, the holder under the rotation entering no pace, an unlike sign binding it below the free rest rotation; the inner stop the first repeat of the integer pair or a return within the roundings of one iteration at every Node (`ROUNDINGS_OF_THE_TURNED_READ`, the start's own rule of the repeat, one unit per division act composed), the clock then re-read from the mode's own ratio, cosine <- cosine x (the largest of F(z) + z less fine) div fine (F(z) = z exactly at the clock the mode stands at), the outer pass repeated until the clock pair returns itself; the first clock the free rest's, cos omega_0 = num / den. Returns the two lines at the fine unit and the clock pair (cosine, fine), cos Omega = cosine / fine."""
    reads, self_coefficient, wall = rule_of(board, content)
    time, links = angles
    cosine = int(division_forward(board.pair[0] * fine, board.pair[1], 0)[0])
    re = scaled(board, np.where(keep, seed, 0).astype(board.kind), fine)
    im: np.ndarray = np.zeros(board.shape, dtype=board.kind)

    def read_of(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        arrived = turned_arrivals(board, x, y, links)
        found = [
            np.where(keep, np.asarray(rule3(reads, at, self_coefficient, wall, a, 0, 0)[0]), 0)
            for a, at in zip((x, y), arrived, strict=True)
        ]
        return np.asarray(found[0]), np.asarray(found[1])

    while True:  # the outer pass: the clock re-read from the mode's own ratio
        sine = division_fixed_point(fine * fine - cosine * cosine)
        numerator, denominator = time_factor(time, cosine, sine, fine, board.gamma)
        seen: set[bytes] = set()
        largest = fine
        while True:
            total = read_of(re, im)
            found = [
                np.asarray(rule3(NO_READ, NO_READ, t * denominator, numerator, 1, 0, 0)[0]) + z
                for t, z in zip(total, (re, im), strict=True)
            ]  # F(z) + z: the shift by one unit, the band's bottom modes near 0 and the top near 2
            largest = max(int(np.abs(found[0]).max()), int(np.abs(found[1]).max()))
            if largest == 0:
                break
            turned = [scaled(board, f.astype(board.kind), fine, largest) for f in found]
            close = max(int(np.abs(turned[0] - re).max()), int(np.abs(turned[1] - im).max()))
            re, im = turned[0], turned[1]
            key = digest(re, im)
            if key in seen or close <= ROUNDINGS_OF_THE_TURNED_READ:
                break
            seen.add(key)
        read = int(division_forward(cosine * (largest - fine), fine, 0)[0])
        if abs(read - cosine) <= 1:
            return re, im, (cosine, fine)
        cosine = read


def turned_top_mode(
    board: Board,
    content: np.ndarray,
    angles: node.Angles,
    keep: np.ndarray,
    seed: np.ndarray,
    unit: int,
    modes: Modes,
) -> tuple[tuple[np.ndarray, np.ndarray], tuple[int, int]]:
    """The turned top mode at the amplitude `unit` with its clock pair (cosine, fine), cos Omega = cosine / fine (`turned_mode` once per fine unit in one content, `modes`). The fine unit is derived from the width and never written: the largest at which the turned read of a level stays inside the room (`Board.room` over twice the sum of the coefficients at a Node) and the time factor's product, twice the read times the fine unit times the wall's 2 h^2, h = 2 Gamma, does too (the fixed point of the division act on the room over 4 h^2), at least the amplitude; the mode is then rounded once to the amplitude by one factor on both lines."""
    h = 2 * board.gamma
    fine = max(
        unit,
        min(
            int(division_forward(board.room, 2 * reach_of(rule_of(board, content)), 0)[0]),
            division_fixed_point(int(division_forward(board.room, 2 * 2 * h * h, 0)[0])),
        ),
    )
    if fine not in modes:
        modes[fine] = turned_mode(board, content, angles, keep, seed, fine)
    re, im, clock = modes[fine]
    largest = max(int(np.abs(re).max()), int(np.abs(im).max()))
    return (scaled(board, re, unit, largest), scaled(board, im, unit, largest)), clock


def turned_spread(
    board: Board,
    content: np.ndarray,
    angles: node.Angles,
    clock: tuple[int, int],
    re: np.ndarray,
    im: np.ndarray,
    where: np.ndarray,
) -> int:
    """The standing condition's largest departure over `where` in levels, on either line: |(M z)_i wall_i - numerator_i z_i| div wall_i, the turned read against 2 cos(Omega - theta_i) z_i at the clock pair (`time_factor`), a record standing in the content and the angles departing at most the roundings of a step at a Node (`ROUNDINGS_OF_A_STEP`)."""
    reads, self_coefficient, wall = rule_of(board, content)
    cosine, fine = clock
    sine = division_fixed_point(fine * fine - cosine * cosine)
    numerator, denominator = time_factor(angles[0], cosine, sine, fine, board.gamma)
    arrived = turned_arrivals(board, re, im, angles[1])
    worst = 0
    for a, at in zip((re, im), arrived, strict=True):
        total = np.asarray(rule3(reads, at, self_coefficient, wall, a, 0, 0)[0])
        off = np.abs(total * denominator - numerator * a)
        departure = np.asarray(rule3(NO_READ, NO_READ, off, denominator, 1, 0, 0)[0])
        worst = max(worst, int(np.where(where, departure, 0).max()))
    return worst


def turned_period(
    board: Board, content: np.ndarray, angles: node.Angles, pairs: Pairs, at: Axis
) -> int | None:
    """One whole period of a turned plane at a Node by the engine's own turned step (`turned_step`): the intervals from the real line's return upward through 0 at `at` to the next such return; None where the state repeats before the level returns twice."""
    (re_now, re_before), (im_now, im_before) = pairs
    remainders: list[np.ndarray] = [np.zeros(board.shape, dtype=board.kind) for _ in range(2)]
    sign = 1 if re_now[at] > 0 else -1 if re_now[at] < 0 else 0
    length, returned_once = 0, False
    seen: set[bytes] = set()
    while (key := digest(re_now, re_before, im_now, im_before)) not in seen:
        seen.add(key)
        re_next, im_next, remainders[0], remainders[1] = turned_step(
            board,
            content,
            angles,
            Record(re_now, re_before, remainders[0]),
            Record(im_now, im_before, remainders[1]),
        )
        here = int(re_now[at])
        if here > 0 and sign <= 0:
            if returned_once:
                return length
            returned_once = True
        if here:
            sign = 1 if here > 0 else -1
        if returned_once:
            length += 1
        re_now, re_before, im_now, im_before = re_next, re_now, im_next, im_now
    return None


def quarter_turned(
    re: np.ndarray, im: np.ndarray, clock: tuple[int, int], sense: int, direction: int
) -> tuple[np.ndarray, np.ndarray]:
    """A plane's level pair turned by its own rotation Omega in the record's sense (ALGEBRA.md #the-paces, The sign is the rotation sense: the record of positive Wronskian has z_before = z_now e^(i Omega)): the turn by the tangent half-angle sin Omega / (1 + cos Omega) = sine / (fine + cosine), the three exact shears (features/rotation), `direction` 1 the level before (e^(i sense Omega) z) and -1 the level next (e^(-i sense Omega) z)."""
    cosine, fine = clock
    sine = division_fixed_point(fine * fine - cosine * cosine)
    x, y = rotation.turned(re, im, direction * sense * sine, fine + cosine)
    return np.asarray(x), np.asarray(y)


def standing(
    board: Board,
    content: np.ndarray,
    angles: Angles,
    node_at: Axis,
    shape_seed: np.ndarray,
    scale: int,
    region: np.ndarray,
    keep: np.ndarray,
    modes: Modes,
    sense: int = 0,
) -> Standing | None:
    """The standing record of the body in a content: the top mode of Rule3's read act over `keep`, the board as declared outside the other bodies' regions (`own_board`; the power iteration from the body's shape, scaled to `scale` at its largest level; a bound mode's eigenvalue stands above the band's top, so the iteration on the board finds it, and the other bodies' regions are left out so that it is this body's mode and not the deeper well's), laid at its peak, the level before and the level next alike at half the mode's read (next + before = 2 cos omega x now at every Node of a standing record, so before = next = the read div 2 at the peak), the clock pair [the read, now] at the centre, the period read by Rule3 from that record (`period_reading`, the length from the centre's return upward through 0 to the next, the window twice it) and the share the record carries over the region at the paces of the content, the sum in the current's units and once rounded to quanta; None, no record, where the mode departs from one rotation across the region by more than the roundings of a step at a Node (`rotation_spread`, `ROUNDINGS_OF_A_STEP`: the mode is no eigenvector of the read in this content within the integers' rounding, a cloud's or a trapped iteration's), where the mode is 0 at the centre or where the centre's level never returns (a cloud, no period). The read act with the before-coefficient 0 is Rule3's own and the step a <- read - before keeps the record: a record stepped from this lay rotates at the mode's clock within the rounding. Where a holder of the sign turns the record (`angles`, the time numerators and the odd lines of every sign row but the body's own) the record is the turned top mode (`turned_top_mode`), the two lines laid rotating in the body's sense at the mode's own clock, z_before = e^(i sense Omega) z and z_next = e^(-i sense Omega) z (`quarter_turned`), the clock pair [2 cosine, fine] = 2 cos Omega, the period by the engine's turned step (`turned_period`) and the departure of the standing condition at a Node (`turned_spread`) within the roundings of a step, else None."""
    if angles is None:
        now, total = top_mode(board, content, keep, shape_seed, scale, modes)
        if not now[node_at]:
            return None
        if now[node_at] < 0:
            now, total = -now, -total
        if rotation_spread(now, np.zeros_like(now), total, region)[2] > ROUNDINGS_OF_A_STEP:
            return None
        before = np.asarray(division_forward(total, 2, 0)[0], dtype=board.kind)
        pairs: Pairs = [(now, before)]
        nxt, clock, second = total - before, (int(total[node_at]), int(now[node_at])), None
        reading = period_reading(
            board, content, node_at, [now.copy(), before.copy(), np.zeros(board.shape, dtype=board.kind)]
        )
        window = None if reading is None else 2 * reading[0]
    else:
        (now, im), turned_clock = turned_top_mode(board, content, angles, keep, shape_seed, scale, modes)
        if not now[node_at] and not im[node_at]:
            return None
        if now[node_at] < 0:
            now, im = -now, -im
        if turned_spread(board, content, angles, turned_clock, now, im, region) > ROUNDINGS_OF_A_STEP:
            return None
        before, im_before = quarter_turned(now, im, turned_clock, sense, 1)
        nxt, im_next = quarter_turned(now, im, turned_clock, sense, -1)
        pairs, second, clock = (
            [(now, before), (im, im_before)],
            (im, im_before, im_next),
            (2 * turned_clock[0], turned_clock[1]),
        )
        period = turned_period(board, content, angles, pairs, node_at)
        window = (
            None if period is None else 2 * period
        )  # the period is [window, 2], as the real record's
    if window is None:
        return None
    total_share = sum(
        (share_of(board, content, a, b) for a, b in pairs), np.zeros(board.shape, dtype=board.kind)
    )
    summed = int(np.where(region, total_share, 0).sum(dtype=object))
    if angles is None:  # the quanta at the Nodes, each rounded, summed: the body's counts as laid
        quanta = read_quanta(total_share, board.pair[1], board.action, board.kind)
        carried = int(np.where(region, quanta, 0).sum())
    else:  # the law's count 1 over the mode's Nodes: the summed share rounded once
        carried = int(read_quanta(summed, board.pair[1], board.action, object))
    amplitude = max(int(np.abs(a).max()) for a, _b in pairs)
    return Standing(carried, window, amplitude, clock, now, before, nxt, summed, second)


def rows_read(universe: dict[str, Any], family: str, sign: bool) -> list[tuple[int, FamilyRule]]:
    """The held rows a body's family reads into its paces that hold the sign (`sign`, sourced by the Wronskian) or the content (sourced by the form), each by its position among the universe's families with its rule, as the loader reads the family's declaration (ALGEBRA.md #the-paces); a holder of the sign that declares the rotation is read by the turn of the record and not into the pace, so it is none of these (its turn leaves the record's share as it is)."""
    families = universe_of(universe)[1]
    reader = families[[row.name for row in families].index(family)]
    found = []
    for read in reader.reads:
        row = families[read.family]
        if row.wronskian == sign and not row.rotation:
            found.append((read.family, row))
    return found


Rows = list[tuple[int, FamilyRule]]  # the held rows of the content a body's family reads, by position


def held_rows(universe: dict[str, Any], family: str) -> Rows:
    """The held rows holding the content a body's family reads: the rows whose levels are the content its record reads, sourced by the plain share of its record; refused by name where there is none, a body needing a row to bind in."""
    found = rows_read(universe, family, False)
    if not found:
        raise ValueError(
            f"the family {family!r} reads no held row of the content: a body needs a row to bind in "
            "(ALGEBRA.md #the-generator)"
        )
    return found


def family_of(universe: dict[str, Any], name: str) -> FamilyRule:
    """A family of the universe file as the loader derives it, by its name."""
    families = universe_of(universe)[1]
    return families[[row.name for row in families].index(name)]


def rests(rows: Rows, counts: np.ndarray, board: Board) -> np.ndarray:
    """Every held row's level under counts in quanta at the row's level weight times its write weight, the seed of a lay and no result (the engine's start sources the form, `start_content`): every holder of the content at the rest of its own line, reading the holders among these rows its declaration names at their weights, its own level among them where it names itself (features/start, `settled_rows`: the division act iterated from nothing until it repeats, at the row's pair and level weight, with or without a gap), with its vacuum content added (the massless row's `rest`), summed into the content every record reads: the first lay's well, the shape a body's first record is seeded with."""
    positions = [position for position, _row in rows]
    sourced = [
        (
            row.write * counts,
            row.pair,
            int(row.level_weight or 0),
            row.rest,
            tuple((positions.index(r.family), r.weight) for r in row.reads if r.family in positions),
        )
        for _position, row in rows
    ]
    fields = settled_rows(sourced, board.wrap, board.width, board.gamma, board.unit)
    return sum(
        (
            np.asarray(field.levels, dtype=board.kind) + row[3]
            for field, row in zip(fields, sourced, strict=True)
        ),
        np.zeros(counts.shape, dtype=board.kind),
    )


Pairs = list[tuple[np.ndarray, np.ndarray]]  # a body's level pairs as laid, (now, before) per line pair
Laid = list[
    tuple[int, int, Pairs]
]  # laid records: each its family, its record number and its level pairs
Others = tuple[np.ndarray, Laid]  # the other bodies' counts (the seed's) and the other records as laid


def start_content(
    board: Board, families: tuple[FamilyRule, ...], index: int, slot: int, pairs: Pairs, others: Laid
) -> tuple[np.ndarray, Angles]:
    """The content a body's record reads at the engine's own start, by the engine's own act and no copy of it (`GameBoard.start`; `booked_sources` and `held_rests` are the one act, so the generator and the engine compute one fixed point and agree by construction): the body's level pairs laid on its record's lines and the other bodies' and the messages' on theirs (`others`, each its family and its record, `node.record_slice`; the symmetric lay over a record's parts, the plane's second pair on its second line), every held row at the rest the lay and the rest return together from nothing, the holders of the content and every row of the holders of the sign a laid plane sources (the form of every record and its Wronskian as the hold books them, the Wronskian into the record's own row, over the write's wall E_s T, the fine form and no whole quanta), and the record's read of those rests (every holder of the content, and for a plane every row of the holders of the sign but its own, plainly), the content the engine steps its record in (ALGEBRA.md, No record reads its own write of the sign); beside it the angles the record is turned by where a holder declares the rotation (`node.turning`: the time angle's numerators from every sign row but the record's own at the record's own clock, and the odd lines), None where no holder turns it."""
    walls = {
        number: held_write(families, number, board.action).walls
        for number, f in enumerate(families)
        if f.held
    }
    states = [
        empty_state(f, board.shape, walls.get(number, ()), board.kind)
        for number, f in enumerate(families)
    ]
    for number, own, laid in [(index, slot, pairs), *others]:
        family, lines = families[number], states[number].lines
        span = record_slice(family, own)
        for first in range(span.start, span.stop, family.width):
            for part, (now, before) in enumerate(laid):
                line = lines[first + part]
                lines[first + part] = Record(line.now + now, line.before + before, line.remainder)
    holders = [(number, 0) for number, f in enumerate(families) if f.held and not f.wronskian]
    signs = [
        (number, row)
        for number, f in enumerate(families)
        if f.held
        and f.wronskian
        and any(
            bool(np.asarray(wronskian(states[reader].lines, families[reader].plane)).any())
            for reader, family in enumerate(families)
            if family.quanta and any(taken.family == number for taken in family.reads)
        )
        for row in range(f.records)
    ]
    rows = holders + signs
    time_walls = {row: walls[row[0]][0] for row in rows}
    messages = {row: states[row[0]].lines[record_slice(families[row[0]], row[1]).start] for row in rows}

    def booked(levels: Sequence[np.ndarray]) -> tuple[list[Sourced], list[Sourced]]:
        return booked_sources(
            families,
            states,
            rows,
            holders,
            time_walls,
            messages,
            levels,
            board.wrap,
            board.gamma,
            board.unit,
        )

    fields = held_rests(
        booked,
        [np.zeros(board.shape, dtype=board.kind) for _ in rows],
        board.wrap,
        board.width,
        board.gamma,
        board.unit,
    )
    booked([field.levels for field in fields])  # the rests as found laid into the rows for the read
    content = np.asarray(
        content_read(index, families, states, 1, board.wrap, board.gamma, board.unit, slot)[0],
        dtype=board.kind,
    )
    return content, node.turning(index, families, states, 1, board.gamma, slot)


def region_of(counts: np.ndarray, well: np.ndarray, centre: Axis, wrap: Wrap) -> np.ndarray:
    """A body's region: the Nodes carrying a quantum of it and one Link around them, where its form may reach next round (the body's width is its own: the iteration widens it a Link a round while its form reaches a quantum there, and narrows it where the form falls below one)."""
    if int(well[centre]) <= 0:
        raise ValueError(
            f"the body about the Node {list(centre)} has no well: its binding level there is {int(well[centre])}"
        )
    return dilated(counts > 0, wrap)


def spread(
    first: np.ndarray,
    centre: Axis,
    board: Board,
    rows: Rows,
    others: np.ndarray,
) -> np.ndarray:
    """The first lay: a body declared on one Node is laid over the cube about its centre, its quanta shared alike, the cube widened one Link at a time until every pace is positive, the content below the Link's zero (no value of the law: the iteration moves it to the fixed point); a body declared on its Nodes is laid as declared."""
    if int(np.count_nonzero(first)) > 1:
        return first.copy()
    quanta = int(first.sum())
    for half in range(1, max(board.shape)):
        idx = np.indices(board.shape).reshape(3, -1).T
        cube = (np.abs(idx - np.array(centre)).max(axis=1) <= half).reshape(board.shape)
        for axis in range(3):  # a cube beyond a face stays on the board
            if not board.wrap[axis]:
                cube &= np.abs(idx[:, axis] - centre[axis]).reshape(board.shape) <= half
        nodes = int(cube.sum())
        counts = np.where(cube, int(division_forward(quanta, nodes, 0)[0]), 0).astype(np.int64)
        counts[centre] += quanta - int(counts.sum())
        try:  # the body alone: the others are spread in their turn
            content = rests(rows, counts, board)
        except RestCollapses:
            continue  # the rows' own rests reach the pace 0 under this cube: the next
        if int(content.max()) < frozen_content(board.gamma):  # the Node's pace above 0 (#the-paces)
            return counts
    raise ValueError(
        f"the body of {quanta} quanta about the Node {list(centre)} fits no cube on this board with a positive pace"
    )


def compact_seed(
    quanta: int, centre: Axis, shape: Axis, wrap: Wrap, profile: tuple[int, int]
) -> np.ndarray:
    """The first lay of the compact seed (the world's `lay.seed` `compact`, loader/lay.py; ALGEBRA.md, The compact pixel under the composed paces): the body's quanta at its seed Node and at the Nodes of its six Ports in the proportion the world's `profile` [centre, neighbour] declares, each Port's Node read through the Port as the engine reads it (`ports.arrival`: the Node itself on a folded axis, nothing beyond a face), every Node's count the parts' quotient of the quanta by the division act and the remainder at the centre: the compact branch's shape as the law's line names it, the seed of the first pass alone and no result (the iteration moves it to the fixed point, or away from the branch)."""
    parts, one = np.zeros(shape, dtype=np.int64), np.zeros(shape, dtype=np.int64)
    parts[centre], one[centre] = profile
    for axis in range(3):
        for sense in (1, -1):
            parts += np.asarray(arrival(one, axis, sense, wrap, 0))
    counts = np.asarray(division_forward(parts * quanta, int(parts.sum()), 0)[0], dtype=np.int64)
    counts[centre] += quanta - int(counts.sum())
    return counts


def scaled_record(
    board: Board,
    content: np.ndarray,
    angles: Angles,
    centre: Axis,
    own: np.ndarray,
    region: np.ndarray,
    quanta: int,
    centre_count: int,
    keep: np.ndarray,
    sense: int = 0,
    squares: int = 1,
) -> Standing:
    """The standing record scaled so its form over the region carries the body's quanta: the scale bracketed from the centre's own count (the form there is its count times T) by halving and doubling, a scale too large to stand halved back toward the last that stood, then bisected on the quanta carried at the Nodes (each Node's share rounded, summed, the counts as laid) or, for a record a holder turns, on the summed share against the quanta's wall W_c = 3 den T (the share itself and not its rounding to whole quanta, so that a record of count 1, whose share at every Node is below a quantum, is scaled to one quantum over its region); the reading closest to the quanta; refused by name when no reading stands. The mode is iterated once per fine unit in this content and scaled to each trial amplitude (`Modes`)."""
    readings: dict[int, Standing] = {}
    modes: Modes = {}
    target = quanta if angles is None else quanta * 3 * board.pair[1] * board.action

    def measure(found: Standing) -> int:  # the share over the lines the pair is laid on at their weights
        return found.carried * squares if angles is None else found.share

    def read(scale: int) -> Standing | None:
        if scale not in readings:
            record = standing(board, content, angles, centre, own, scale, region, keep, modes, sense)
            if record is None:
                return None
            readings[scale] = record
        return readings[scale]

    def stands(scale: int) -> Standing:
        record = read(scale)
        if record is None:
            raise ValueError(
                f"the record of the body of {quanta} quanta about the Node {list(centre)} scaled at {scale} "
                "does not stand: the top mode of the read in this content is no one rotation across the region "
                "within the roundings of a step, or its centre's level never returns (the generator is Rule3)"
            )
        return record

    low = max(1, division_fixed_point(max(1, centre_count) * board.action))
    while low > 1 and ((found := read(low)) is None or measure(found) > target):
        low = max(1, low // 2)
    high = low
    while (found := read(high)) is not None and measure(found) < target:
        low, high = high, 2 * high
        while read(high) is None and high > low + 1:
            high = (low + high) // 2
    stands(low), stands(high)
    while high - low > 1:
        middle = (low + high) // 2
        if measure(stands(middle)) < target:
            low = middle
        else:
            high = middle
    return readings[min(readings, key=lambda found: (abs(measure(readings[found]) - target), found))]


def pixel_record(
    board: Board, counts: np.ndarray, centre: Axis, sense: int, planes: int = 1
) -> tuple[Standing, Pairs]:
    """The one-Node record of a body's quanta at its declared Node, a declaration by name and no fixed point (examples/events/frozen_proton/design.json, the proton; ALGEBRA.md, The law's alpha is a coefficient of the file, the quantum of a family: one unit of the invariant, 2 A^2 sin omega_s = T per quantum, its Wronskian sense x T / 2): the level now (A, 0) with A the fixed point of the division act on quanta x T den div (2 sin omega_s den) and the level before the band's rest rotation in the body's sense, (A cos omega_s, sense A sin omega_s) with cos omega_s = num / den and sin omega_s = the fixed point of den^2 - num^2 over den; on a pair whose num is not 0 the record is no exact rotating pixel and spreads from the first interval at the band's group velocity (the folder's blind, row 2); its share at the Node reads 1 / sin omega_s of its quanta, which the gate admits within its rounding. Returns the record and its level pairs; `planes` the planes of the record's part, every plane laid alike at A_l^2 = count T den / (2 sin omega_0 x planes), the planes summing to the invariant (the two hands of 2026-10-03, the proton's row of three planes at A_l^2 = T / 6 at [0, den])."""
    num, den = board.pair
    sine = division_fixed_point(den * den - num * num)
    quanta = int(counts.sum())
    amplitude = division_fixed_point(
        int(division_forward(quanta * board.action * den, 2 * sine * planes, 0)[0])
    )
    zero: np.ndarray = np.zeros(board.shape, dtype=board.kind)
    re_now, re_before, im_before = zero.copy(), zero.copy(), zero.copy()
    re_now[centre] = amplitude
    re_before[centre] = int(division_forward(amplitude * num, den, 0)[0])
    im_before[centre] = sense * int(division_forward(amplitude * sine, den, 0)[0])
    pairs: Pairs = [(re_now, re_before), (zero.copy(), im_before)] * planes
    total = sum((share_of(board, 0, a, b) for a, b in pairs), zero.copy())
    summed = int(total.sum(dtype=object))
    record = Standing(
        int(read_quanta(summed, den, board.action, object)),
        0,
        amplitude,
        (2 * num, den),
        re_now,
        re_before,
        re_before,
        summed,
        (zero.copy(), im_before, -im_before),
    )
    return record, pairs


def body_fixed_point(
    board: Board,
    families: tuple[FamilyRule, ...],
    index: int,
    slot: int,
    rows: Rows,
    others: Others,
    centre: Axis,
    quanta: int,
    first: np.ndarray,
    sense: int = 0,
    weights: tuple[int, ...] = (1,),
) -> tuple[np.ndarray, Standing, np.ndarray, np.ndarray, Pairs]:
    """The body is the joint fixed point of its record and its content: from a first lay of its quanta the count's rest, the seed of the first pass alone (the other bodies' counts among it), the body's region from its well, its standing record seeded with the well's shape and scaled until its weighted share over the region carries its quanta, the record laid as the engine lays it (its level pair over the board as declared outside the other bodies' regions, `own_board`; with a sense its second pair the record a quarter period on, `rotating`, so that the holder of the sign rests inside the iteration and not after it), then the engine's own start on that lay (`start_content`: every held row at the rest its form and Wronskian return, the fine form over the write's wall as the hold books it, the other bodies' laid records among the sources), the content the record stands in next, and the counts the record's share in quanta at that content over the region; repeated until the content returns itself by the start's own rule (`returned`: the fixed point, or an earlier content one unit per division act composed at most, a rounding tie; the acts composed in the content are the record's scale, one, and per held row the family's declaration reads into its content, the content holders and the holders of the sign where a sense is laid, the acts the engine's own `held_rests` composes for that row, its rest's and its booking's, `ACTS_OF_A_HELD_ROW`, so 1 + 2 x 2 = 5 for matter reading the binding and gravity and 1 + 2 x 3 = 7 for a charged plane reading the charge too, counted from the family's reads at the call; a return further off a cycle, refused by name, the law's own answer at this count and sense and no defect) and the counts return within the rounding at every Node, each round taking the half step from the counts toward the share (the deep well overshoots under the whole step); returns the counts over the region, the record standing in the content returned, the region, the content and the laid level pairs, all of one round; refused by name as a cloud (the rotation not above the band's top) or a collapse (a pace not positive). The seed is the count and the fixed point is the form's and the content's together."""
    counts = first.copy()
    seen: dict[bytes, int] = {}
    name = f"the lay and the rest of the body of {quanta} quanta about the Node {list(centre)}"
    read_rows = [  # the held rows the family's declaration reads into its content at this lay
        r
        for r in families[index].reads
        if not families[r.family].rotation and (sense or not families[r.family].wronskian)
    ]
    acts = 1 + ACTS_OF_A_HELD_ROW * len(
        read_rows
    )  # the record's scale, then every row's rest and booking
    content, angles = seed_content(board, families, index, slot, rows, others, counts)
    keep = own_board(board, others[0])
    round_number = 0
    while True:
        round_number += 1
        record, pairs, found, turned = one_pass(
            board,
            families,
            index,
            slot,
            others,
            centre,
            quanta,
            counts,
            content,
            angles,
            keep,
            sense,
            weights,
        )
        region = keep if angles is not None else region_of(counts, content, centre, board.wrap)
        a, level = record.clock
        zero: np.ndarray = np.zeros(board.shape, dtype=board.kind)
        total = sum((share_of(board, found, now, before) for now, before in pairs), zero)
        laid = np.where(region, read_quanta(total, board.pair[1], board.action, board.kind), 0)
        agreed = bool(np.all(within(laid - counts, np.maximum(laid, counts))))
        print(
            f"GAMEBOARD the body about {list(centre)}, round {round_number}: the content at the centre "
            f"{int(content[centre])} -> {int(found[centre])}, the count {int(counts[centre])} -> {int(laid[centre])} "
            f"of {int(laid.sum())}, the clock [{a}, {level}] = {a / level:.4f}",
            file=sys.stderr,
            flush=True,
        )
        if returned(angled(found, turned), angled(content, angles), seen, name, acts) and agreed:
            return laid, record, region, found, pairs
        counts = (counts + laid) // 2  # the half step: the deep well overshoots under the whole step
        content, angles = found, turned


def angled(content: np.ndarray, angles: Angles) -> list[np.ndarray]:
    """A pass's paces as the repeat reads them: the content, and where a holder turns the record the time angle's numerators beside it (the record stands in both)."""
    return [content] if angles is None else [content, np.asarray(angles[0])]


def seed_content(
    board: Board,
    families: tuple[FamilyRule, ...],
    index: int,
    slot: int,
    rows: Rows,
    others: Others,
    counts: np.ndarray,
) -> tuple[np.ndarray, Angles]:
    """The seed of the first pass alone: the content holders' rests under the counts in quanta (`rests`) and no angle for a record no holder turns; for a record a holder of the sign turns, the engine's own start under the other bodies' laid records with this body's lines empty (`start_content`), whose sign rows give the first pass its angles (the turned body binds in the angle and not in the content, its own count below the content's rounding where it is the law's count 1)."""
    if not turns(families, index):
        return rests(rows, others[0] + counts, board), None
    zero: np.ndarray = np.zeros(board.shape, dtype=board.kind)
    return start_content(board, families, index, slot, [(zero, zero), (zero, zero)], others[1])


def one_pass(
    board: Board,
    families: tuple[FamilyRule, ...],
    index: int,
    slot: int,
    others: Others,
    centre: Axis,
    quanta: int,
    counts: np.ndarray,
    content: np.ndarray,
    angles: Angles,
    keep: np.ndarray,
    sense: int,
    weights: tuple[int, ...] = (1,),
) -> tuple[Standing, Pairs, np.ndarray, Angles]:
    """One pass of the lay-and-rest map, the act both lays share: refused by name where the content reaches the Link's zero (a collapse, a frozen clock); the body's region from its counts (the board as kept for a record a holder turns, which binds in the angle over every Node where it stands), its standing record in the content and the angles scaled to carry its quanta (`scaled_record`), refused by name as a cloud where its rotation is not above the band's top and below 2; the record's level pairs over the board as declared outside the other bodies' regions (with a sense its second pair, `rotating`; a turned record's two lines the turned mode's own, laid with a sense, refused by name without one); and the content and the angles the engine's own start returns under that lay (`start_content`), the paces the record stands in next."""
    num, den = board.pair
    if int(content.max()) >= frozen_content(board.gamma):
        raise ValueError(
            f"the body of {quanta} quanta about the Node {list(centre)} collapses: its wells reach the pace 0 "
            f"(the content {int(content.max())} at or beyond the Link's zero {frozen_content(board.gamma)}, "
            "where the Node's pace p_0^2 / Gamma rounds to 0, a frozen clock; ALGEBRA.md #the-paces, "
            "The paces compose)"
        )
    if angles is not None and not sense:
        raise ValueError(
            f"the body of {quanta} quanta about the Node {list(centre)} is turned by a holder of the sign and is "
            "laid with no sense: a turned record rotates in its own sense (ALGEBRA.md, The sign holder rotates "
            "the two-part record)"
        )
    region = keep if angles is not None else region_of(counts, content, centre, board.wrap)
    own = np.where(region, content, 0)  # the shape of the seed: the well over the body's region
    if angles is not None:  # the seed the angle's well too, the sign row's size about its source
        own = own + np.where(region, np.abs(np.asarray(angles[0])), 0)
    laid = weights  # one per real line at its weight, one per plane at 1 (`laid_weights`)
    squares = sum(weight * weight for weight in laid)  # the share's multiplier over the laid lines
    record = scaled_record(
        board, content, angles, centre, own, region, quanta, int(counts[centre]), keep, sense, squares
    )
    a, level = record.clock
    if not (2 * num * level < a * den < 2 * level * den):
        raise ValueError(
            f"the body of {quanta} quanta about the Node {list(centre)} is a cloud: its standing reading rotates at "
            f"[{a}, {level}], not above the band's top 2 x {num} / {den} and below 2; its quanta are below its "
            "binding row's window of mass (ALGEBRA.md #the-generator)"
        )
    pairs: Pairs = [
        (np.where(keep, w * record.now, 0), np.where(keep, w * record.before, 0)) for w in laid
    ]
    if families[index].plane:  # every plane alike: its first pair, and its sense where there is one
        first, second = pairs[0], None
        if record.second is not None:
            second = (np.where(keep, record.second[0], 0), np.where(keep, record.second[1], 0))
        elif sense:
            levels = rotating(board, content, record, keep, sense)
            first, second = (levels[0], levels[1]), (levels[2], levels[3])
        zero = (np.zeros_like(record.now), np.zeros_like(record.before))
        pairs = [pair for _ in laid for pair in (first, second if second is not None else zero)]
        pairs = pairs if second is not None else pairs[:-1]  # the last sense unlaid where there is none
    found, turned = start_content(board, families, index, slot, pairs, others[1])
    return record, pairs, found, turned


Trajectory = list[
    list[int | None]
]  # per pass: its number, the content's largest change, the record's, the count laid


def unit_fixed_point(
    board: Board,
    families: tuple[FamilyRule, ...],
    index: int,
    slot: int,
    rows: Rows,
    others: Others,
    centre: Axis,
    quanta: int,
    first: np.ndarray,
    sense: int,
    lay: Lay,
    weights: tuple[int, ...] = (1,),
) -> tuple[np.ndarray, Standing, np.ndarray, np.ndarray, Pairs, Trajectory]:
    """The lay at the integer fixed point under the body's own paces (the world's `lay` of the kind `fixed_point`, loader/lay.py; HIGHLIGHTS.md, the mathematician's 162 (3) and 168 item 2 (1), the owner's word of 2026-10-02, 17:40): the same map as `body_fixed_point`, one pass the standing record in the content and the engine's own start under that record (`one_pass`), iterated with the design's count the input of every pass and no half step on the counts, until the record's two levels and the content repeat the pass before within the declared `stop` units at every Node (0 the exact repeat), inside the declared `passes`; the record of the last pass is laid in the content it returned to within the stop, so the start the engine lays under the mode file's record gives the paces the record was laid in to the unit declared, the body standing exact by construction and the reads' walk alone remaining; the trajectory, per pass the content's largest change, the record's and the count laid, printed as a GameBoard reading and written to the mode file; where the passes run out the body is refused by name with its trajectory, the law's own answer at this count and no defect. Returns the counts, the record, the region, the content and the laid level pairs of the last pass, and the trajectory."""
    counts = first.copy()
    content, angles = seed_content(board, families, index, slot, rows, others, counts)
    keep = own_board(board, others[0])
    previous: Standing | None = None
    trajectory: Trajectory = []
    for number in range(1, lay.passes + 1):
        record, pairs, found, turned_by = one_pass(
            board,
            families,
            index,
            slot,
            others,
            centre,
            quanta,
            counts,
            content,
            angles,
            keep,
            sense,
            weights,
        )
        region = keep if angles is not None else region_of(counts, content, centre, board.wrap)
        zero: np.ndarray = np.zeros(board.shape, dtype=board.kind)
        total = sum((share_of(board, found, now, before) for now, before in pairs), zero)
        laid = np.where(region, read_quanta(total, board.pair[1], board.action, board.kind), 0)
        moved = max(
            int(np.abs(a - b).max())
            for a, b in zip(angled(found, turned_by), angled(content, angles), strict=True)
        )
        turned = None
        if previous is not None:
            turned = max(
                int(np.abs(record.now - previous.now).max()),
                int(np.abs(record.before - previous.before).max()),
            )
        trajectory.append([number, moved, turned, int(laid.sum())])
        a, level = record.clock
        print(
            f"GAMEBOARD the fixed-point lay about {list(centre)}, pass {number}: the content's largest change "
            f"{moved} ({int(content[centre])} -> {int(found[centre])} at the centre), the record's {turned}, the "
            f"count {int(laid.sum())} ({int(laid[centre])} at the centre), the clock [{a}, {level}] = {a / level:.4f}",
            file=sys.stderr,
            flush=True,
        )
        if turned is not None and max(moved, turned) <= lay.stop:
            return laid, record, region, found, pairs, trajectory
        counts, content, angles, previous = laid, found, turned_by, record
    raise ValueError(
        f"the body of {quanta} quanta about the Node {list(centre)} finds no fixed point to {lay.stop} unit(s) in "
        f"{lay.passes} passes: the trajectory, per pass [the pass, the content's largest change, the record's, the "
        f"count laid], {trajectory} (the world's declared stop and passes, loader/lay.py)"
    )


def declared(
    body: dict[str, Any], shape: Axis, quanta: int | None = None
) -> tuple[np.ndarray, Axis, int]:
    """A body's first lay from the world: its counts at its declared Nodes, its centre (the Node of its largest count) and its quanta: the sum of the declared counts for a new body, one Node carrying its quanta, and for a body laid before (declared on its Nodes) the design's count where it is given (`quanta`, the input of every re-lay: the declared Nodes' counts are the engine's reading of the lay before, the output, and never the input)."""
    counts = np.zeros(shape, dtype=np.int64)
    for entry in cast(list[dict[str, Any]], body["nodes"]):
        node = (int(entry["node"][0]), int(entry["node"][1]), int(entry["node"][2]))
        counts[node] += int(entry["count"])
    centre = tuple(int(index) for index in np.unravel_index(int(counts.argmax()), shape))
    return (
        counts,
        (centre[0], centre[1], centre[2]),
        int(counts.sum()) if quanta is None or int(np.count_nonzero(counts)) <= 1 else int(quanta),
    )


def designed_quanta(world: Path, bodies: int) -> list[int | None]:
    """The design's count of every body of a world file, the input of a re-lay: the folder's design file (`design.json` beside the world, its world's entry `quanta` or the design's own `quanta`, one count for every body of the world), else the mode file beside the world (`<world>.mode.json`, each body's `count`, the first lay's design), else none (the world's declared counts sum to a new body's quanta)."""
    design = world.with_name("design.json")
    if design.exists():
        document = json.loads(design.read_text(encoding="utf-8"))
        worlds = cast(dict[str, Any], document.get("worlds", {}))
        entry = worlds.get(world.stem, {})  # a design may name its world in prose alone
        quanta = (entry if isinstance(entry, dict) else {}).get("quanta", document.get("quanta"))
        if quanta is not None:
            return [int(quanta)] * bodies
    mode = world.with_suffix(".mode.json")
    if mode.exists():
        laid = cast(list[dict[str, Any]], json.loads(mode.read_text(encoding="utf-8")).get("bodies", []))
        if len(laid) == bodies:
            return [int(body["count"]) for body in laid]
    return [None] * bodies


def body_entry(
    record: Standing,
    board: Board,
    region: np.ndarray,
    body: dict[str, Any],
    quanta: int,
    scale: int,
) -> dict[str, Any]:
    """One body's mode entry: its standing record over the board as declared, its clock pair, amplitude and period."""
    keep = on_the_board(board)
    now, before = np.where(keep, record.now, 0), np.where(keep, record.before, 0)
    entry: dict[str, Any] = {
        "family": body["family"],
        "pair": list(board.pair),
        "count": quanta,
        "seed": scale,
        "carried": record.carried,
        "period": [record.window, 2],
        "amplitude": int(np.abs(now).max()),
        "clock": list(record.clock),
        "profile": now.ravel().tolist(),
        "moving": {"now": now.ravel().tolist(), "before": before.ravel().tolist()},
    }
    return entry


def rotating(
    board: Board, content: np.ndarray, record: Standing, keep: np.ndarray, sense: int
) -> list[np.ndarray]:
    """A body laid with a sense (ALGEBRA.md #the-paces, the sign is the rotation sense): its record and its second level pair, sense x the standing record a quarter period on by Rule3 (the mode's own rotation, the period [window, 2]), both within the kept region and scaled by one factor so the two pairs' plain form at the written moment is the record's own (the start's sources, and so the well, unchanged); returns [re_now, re_before, im_now, im_before]."""
    now, before = record.now.copy(), record.before.copy()
    remainder: np.ndarray = np.zeros(board.shape, dtype=board.kind)
    quarter = (
        record.window
    )  # the period is [window, 2]: a quarter period is window div 8, three halvings
    for _ in range(3):
        quarter = int(division_forward(quarter, 2, 0)[0])
    for _ in range(quarter):
        now, before = step(board, content, now, before, remainder), now
    pairs = [np.where(keep, level, 0) for level in (record.now, record.before, now, before)]
    own = int(share_of(board, 0, pairs[0], pairs[1]).sum())
    both = own + int(share_of(board, 0, pairs[2], pairs[3]).sum())
    amplitude = max(int(np.abs(level).max()) for level in pairs)
    scale = division_fixed_point(int(division_forward(amplitude * amplitude * own, both, 0)[0]))
    found = [
        np.asarray(division_forward(level * scale, amplitude, 0)[0], dtype=board.kind) for level in pairs
    ]
    found[2], found[3] = sense * found[2], sense * found[3]
    return found


def read_at_the_start(
    board: Board,
    families: tuple[FamilyRule, ...],
    index: int,
    slot: int,
    others: Laid,
    region: np.ndarray,
    pairs: Pairs,
) -> tuple[np.ndarray, np.ndarray, Angles]:
    """The count the engine's gate reads at the start (ALGEBRA.md #the-count-is-the-records-share; `GameBoard.gate`): the record's share in quanta at the paces of its read at the engine's own start (`start_content`, the one act with `GameBoard.start`: every held row at the rest the laid records' forms and Wronskians return, the other bodies' laid records among them), over the body's region, with the content and the angles of that start (the one-step standing check reads them); the body's Nodes are where that share stands in quanta."""
    content, angles = start_content(board, families, index, slot, pairs, others)
    zero: np.ndarray = np.zeros(board.shape, dtype=board.kind)
    total = sum((share_of(board, content, now, before) for now, before in pairs), zero)
    weighted = np.where(region, read_quanta(total, board.pair[1], board.action, board.kind), 0)
    return weighted, content, angles


def standing_check(
    board: Board,
    content: np.ndarray,
    angles: Angles,
    pairs: Pairs,
    nodes: np.ndarray,
    centre: Axis,
    clock: tuple[int, int],
) -> None:
    """The generator's one-step standing check of a lay (the advisor's hand, 5944220853 and 5944611538 section 3): the laid world stepped once by Rule3 in its own start's content (`read_at_the_start` builds it as `GameBoard.start` does; a turned record by the engine's turned step under the start's angles, `turned_step`), the rotation (next + before) / now read over the body's Nodes (`nodes`, the Nodes where its share stands in quanta, or where its record stands for the law's count 1) on every level pair of the lay alike, a real record's one and a plane's re and im; a lay standing in its content reads one rotation within the rounding 1 / |now| per act composed at every Node (`rotation_spread`, `ROUNDINGS_OF_A_STEP`; a turned record against the lay's own clock, the median over thousands of Nodes of a few levels being the rounding's, with the two turns' six shears allowed beside, `SHEARS_OF_A_TURNED_STEP`), and a lay reading a spread beyond it is no mode of the step in the well the engine lays and is refused by name, printing the centre's rotation, the median read and the mode file's clock."""
    zero: np.ndarray = np.zeros(board.shape, dtype=board.kind)
    stepped = [step(board, content, now, before, zero.copy()) for now, before in pairs]
    allowed = ROUNDINGS_OF_A_STEP
    if angles is not None:  # a turned record against its own clock, the two turns' floors allowed
        re, im = (Record(now, before, zero.copy()) for now, before in pairs)
        stepped = list(turned_step(board, content, angles, re, im)[:2])
        allowed += SHEARS_OF_A_TURNED_STEP
    for part, ((now, before), nxt) in enumerate(zip(pairs, stepped, strict=True)):
        median, read, worst = rotation_spread(now, before, nxt, nodes, clock if angles else None)
        at_centre = (
            f"{float(Fraction(int(nxt[centre]) + int(before[centre]), int(now[centre]))):.4f}"
            if now[centre]
            else "no level"
        )
        print(
            f"GAMEBOARD the lay about {list(centre)}, level pair {part}: stepped once in its start's content the "
            f"rotation (next + before) / now reads {float(median):.4f} (the median over {read} Nodes), at the centre "
            f"{at_centre}, the largest departure {float(worst):.2f} of the "
            f"rounding 1 / |now|; the mode file's clock [{clock[0]}, {clock[1]}] = {clock[0] / clock[1]:.4f}",
            file=sys.stderr,
            flush=True,
        )
        if worst > allowed:
            raise ValueError(
                f"the lay of the body about the Node {list(centre)} does not stand in its own start: stepped once, "
                f"its level pair {part} rotates at {float(median):.4f} in the median over {read} Nodes and at the "
                f"centre at {at_centre}, a Node departing {float(worst):.2f} "
                f"roundings 1 / |now| where at most {allowed}, one per act composed, is a standing record's (the mode file's "
                f"clock [{clock[0]}, {clock[1]}]; ALGEBRA.md #the-generator)"
            )


def turned(doubled: int, unit: int, steps: int) -> list[int]:
    """Rule3's rotation act (ALGEBRA.md #the-four-acts (b)) from the level `unit` and the level `doubled` div 2 after it: a_next = (doubled x a_now + r) div unit - a_before with the remainder kept, `steps` turns; the levels unit x cos(n theta) at 2 unit cos theta = doubled."""
    levels, carry = [unit, int(division_forward(doubled, 2, 0)[0])], 0
    for _ in range(steps - 1):
        nxt, carry = rule3(NO_READ, NO_READ, doubled, unit, levels[-1], levels[-2], carry)
        levels.append(int(nxt))
    return levels


def half_turn(halves: int, unit: int) -> list[int]:
    """The cosines of a half turn in `halves` x 2 steps at the unit, unit x cos(n pi / (2 halves)) for n from 0 through 2 halves, by the rotation act: its doubled cosine is the largest integer at which the rotation from the unit reaches 0 or below within `halves` turns (bisection on the integers, the first zero of the cosine at the quarter turn), no root and no table."""
    lower, upper = 0, 2 * unit
    while upper - lower > 1:
        middle = int(division_forward(lower + upper, 2, 0)[0])
        if min(turned(middle, unit, halves)) <= 0:
            lower = middle
        else:
            upper = middle
    return turned(lower, unit, 2 * halves)


def cosine_at(turns: list[int], index: int) -> int:
    """The cosine at a step of the full turn from a half turn's cosines, cos(2 pi - a) = cos a."""
    whole = 2 * (len(turns) - 1)
    index %= whole
    return turns[whole - index] if index > len(turns) - 1 else turns[index]


def envelope(extent: int, top: tuple[int, int], edge: int, unit: int) -> list[int]:
    """A raised cosine along one axis at the unit: the unit over the flat top [first, last], (unit + unit cos(pi j / edge)) div 2 at j Nodes beyond either end up to the half-width `edge`, 0 further; the unit at every Node where the edge is 0 within the top and 0 beyond it."""
    taper = half_turn(edge, unit) if edge else []
    found = []
    for at in range(extent):
        away = max(top[0] - at, at - top[1], 0)
        if away == 0:
            found.append(unit)
        elif away <= edge:
            found.append(int(division_forward(unit + taper[2 * away], 2, 0)[0]))
        else:
            found.append(0)
    return found


def message_levels(
    board: Board, message: dict[str, Any], beyond: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """The message's two levels (ALGEBRA.md #the-generator, the message lay): now_i = b e_i cos(k x_i + phi) and before_i = b e_i cos(k x_i + phi + omega), the wave one interval earlier, k = pi p / q per Link along its axis (`wave`, p below 0 the packet toward the axis's lower side) with a wave number per axis across the beam (`transverse`, 0 without the key; k x_i then stands for the wave vector's product with the Node's coordinates), phi = 2 pi r / s its phase (`phase`, 0 without the key), b the amplitude, e_i the envelope (the product of the three axes' raised cosines, `top` and `edge`), cos omega the vacuum's band, the mean over the three axes of cos k_a, sin omega the fixed point of the division act; every cosine by the rotation act at a unit derived from the width, the turn cut into the least steps that hold every fraction (a multiple of 2 x 2 q on each axis and of s); 0 beyond the board."""
    along, (turns, halves) = AXES.index(str(message["along"])), message["wave"]
    turned, whole_turn = message.get("phase", [0, 1])
    sideways = {
        AXES.index(str(name)): (int(r), int(s)) for name, (r, s) in message.get("transverse", {}).items()
    }
    numbers = [
        (int(turns), int(halves)) if axis == along else sideways.get(axis, (0, 1)) for axis in range(3)
    ]
    amplitude = int(message["amplitude"])
    unit = division_fixed_point(int(division_forward(board.width, amplitude, 0)[0]))
    steps = lcm(*(2 * 2 * q for _p, q in numbers), int(whole_turn))
    quarter = int(division_forward(steps, 2 * 2, 0)[0])
    cosines = half_turn(quarter, unit)  # cos(2 pi j / steps) for j from 0 through the half turn
    per_link = [
        int(division_forward(p * steps, 2 * q, 0)[0]) for p, q in numbers
    ]  # k's steps per Link per axis
    shift = int(division_forward(int(turned) * steps, int(whole_turn), 0)[0])  # the phase's steps
    axes = [
        envelope(
            board.shape[axis],
            (int(message["top"][name][0]), int(message["top"][name][1])),
            int(message["edge"][name]),
            unit,
        )
        for axis, name in enumerate(AXES)
    ]
    coordinates = np.indices(board.shape)
    index = sum(per_link[axis] * coordinates[axis] for axis in range(3)) + shift
    wave = np.vectorize(lambda i: cosine_at(cosines, int(i)), otypes=[object])(index)
    quadrature = np.vectorize(lambda i: cosine_at(cosines, int(i) - quarter), otypes=[object])(index)
    cosine = int(division_forward(sum(cosine_at(cosines, per_link[axis]) for axis in range(3)), 3, 0)[0])
    sine = division_fixed_point(unit * unit - cosine * cosine)
    shaped = [
        np.array(levels, dtype=object).reshape([-1 if a == axis else 1 for a in range(3)])
        for axis, levels in enumerate(axes)
    ]
    envelope_here = amplitude * shaped[0] * shaped[1] * shaped[2]
    now = envelope_here * wave * unit
    before = envelope_here * (wave * cosine - quadrature * sine)
    scale = unit * unit * unit * unit * unit
    half = int(division_forward(scale, 2, 0)[0])
    found = []
    for numerator in (now, before):
        levels = np.asarray(rule3(NO_READ, NO_READ, 1, scale, 0, 0, numerator + half)[0])
        found.append(np.where(beyond, 0, levels.astype(board.kind)))
    return found[0], found[1]


def laid_weights(row: dict[str, Any], label: str, family: FamilyRule) -> tuple[int, ...]:
    """The weights a body's or a message's laid pair takes on the lines of its record, the world file's key `weights` as the loader reads it (`keys.weights_of`): 1 on every line without the key, a plane's two lines its real pair and its sense."""
    return weights_of(row.get("weights"), f"{label}.weights", family.laid, family.plane)


def message_entry(
    board: Board, message: dict[str, Any], beyond: np.ndarray, family: FamilyRule, label: str
) -> dict[str, Any]:
    """One message's mode entry: its family and pair, its amplitude, the count its record reads over the board at the vacuum's paces (its share in quanta, a reading, over every part of the family and over the lines of a part as the engine lays them, the one event laid on each part alike and on each real line at its weight, `laid_weights`, the share summed over the lines before it is read in quanta, as the engine's books read it) and its two levels as their nonzero Nodes."""
    now, before = message_levels(board, message, beyond)
    weights = (1,) if family.plane else laid_weights(message, label, family)
    total = sum(share_of(board, 0, w * now, w * before) for w in weights)
    laid = read_quanta(total, board.pair[1], board.action)
    return {
        "family": message["family"],
        "pair": list(board.pair),
        "amplitude": int(np.abs(now).max()),
        "count": int(laid.sum()) * family.parts,
        "moving": {"now": nonzero(now), "before": nonzero(before)},
    }


def nonzero(levels: np.ndarray) -> dict[str, list[int]]:
    """A level over the board as its nonzero Nodes alone, the mode file's sparse form: their flat x-major indexes and their levels (a packet stands on few Nodes of a long board)."""
    flat = levels.ravel()
    at = np.flatnonzero(flat)
    return {"at": at.tolist(), "values": flat[at].tolist()}


DECLARATION = (
    "declaration"  # the lay of a body named by --pixel, the one-Node record by name (`pixel_record`)
)


def pixel_mode(
    document: dict[str, Any],
    senses: list[int] | None = None,
    designed: list[int | None] | None = None,
    pixels: Sequence[int] = (),
) -> dict[str, Any]:
    """The mode document of a world of bodies and messages: `world_digest`, `bodies`, one entry per declared event in the world's order, each the standing record of the whole body, rotating in the sense `senses` names for it (+1 or -1; 0 or none a real record), laid at the design's count `designed` where given (the input of every re-lay, `designed_quanta`; the declared counts' sum otherwise), its first pass seeded by the world's `lay.seed` by name (`compact_seed` for the compact profile, else the declared count spread over its cube), or, for a body numbered in `pixels`, the one-Node record of its quanta at its declared Node, a declaration by name (`pixel_record`, laid with a sense, no fixed point, no standing check, its Nodes no other body's cut and no sharing check: it stands inside the body it binds), and `messages`, one entry per message, its packet laid; the document's bodies are rewritten in place to the fixed point's Nodes and counts (the digest is the rewritten world's); a body no Node of which carries a whole quantum (the law's count 1 over its mode's Nodes) keeps its declared Node and count, which the gate admits within its rounding."""
    universe = cast(dict[str, Any], world_files(document)[document["universe"]])
    integers = universe["integers"]
    if "quantum_action" not in integers:
        raise ValueError(
            "the universe file declares no quantum_action T: the count c = D div T needs it"
        )
    pairs = {
        family["name"]: (int(family["pair"][0]), int(family["pair"][1]))
        for family in universe["families"]
    }
    shape = (int(document["shape"][0]), int(document["shape"][1]), int(document["shape"][2]))
    beyond = np.zeros(shape, dtype=bool)
    outside = faces_of(document["faces"], shape) if "faces" in document else ()
    for at in outside:
        beyond[at] = True
    wrap = Wrap(
        *(document["boundary"][axis] == "periodic" for axis in AXES), beyond if outside else None
    )
    gamma = int(document.get("node_clock", integers["node_clock"]))
    rows = cast(list[dict[str, Any]], document.get("bodies", []))
    # a body declaring its parts, or converted whole, is laid by the engine at its one Node (loader/instrument.py)
    kept = [n for n, body in enumerate(rows) if not any(k in body for k in ("parts", "conversion"))]
    bodies = [rows[number] for number in kept]
    lay = lay_of(document["lay"], "lay") if "lay" in document else None  # the lay by name
    lays: list[tuple[np.ndarray, Pairs, Axis, int]] = []
    zero = np.zeros(shape, dtype=np.int64)
    for number, body in enumerate(bodies):
        counts, centre, quanta = declared(body, shape, (designed or [None] * len(rows))[kept[number]])
        if bool(counts[beyond].any()):
            raise ValueError(
                f"bodies[{number}] declares a Node beyond the board's inner face: nothing stands there"
            )
        board = board_of(shape, wrap, gamma, integers, pairs[body["family"]])
        rows = held_rows(universe, str(body["family"]))
        if number in pixels:  # the one-Node record's declaration, its own seed
            first = counts
        elif lay is not None and lay.seed == COMPACT and lay.profile is not None:
            first = compact_seed(quanta, centre, shape, wrap, lay.profile)
        else:  # the declared count's cube
            first = spread(counts, centre, board, rows, zero)
        lays.append((first, [], centre, quanta))
    all_counts = sum(
        (
            counts
            for number, (counts, _pairs, _centre, _quanta) in enumerate(lays)
            if number not in pixels
        ),
        zero,
    )
    names = [family.name for family in universe_of(universe)[1]]
    document_messages = [  # the start's messages: one laid whole at a tick of the run takes no mode entry
        message
        for message in cast(list[dict[str, Any]], document.get("messages", []))
        if "tick" not in message
    ]
    events = [names.index(str(row["family"])) for row in bodies]
    families = with_records(universe_of(universe)[1], [events.count(i) for i in range(len(names))])
    records = []  # each body's record number within its family; a message lays on the first record, 0
    for number, family_index in enumerate(events):
        records.append(min(events[:number].count(family_index), families[family_index].records - 1))
    records += [0] * len(document_messages)
    laid_messages: Laid = []  # every message's record on its family, as the engine lays it
    for number, message in enumerate(document_messages):
        family = str(message["family"])
        board = board_of(shape, wrap, gamma, integers, pairs[family])
        slot = records[len(bodies) + number]
        laid_messages.append((names.index(family), slot, [message_levels(board, message, beyond)]))
    entries: list[dict[str, Any]] = []
    # two passes where there are two bodies or more: the second lays each body in the others' sources
    # as the first laid them (a body not yet laid stands at its first lay, its quanta, not its share);
    # one body's declaration is the engine's reading exactly, several bodies' within the gate's rounding
    for _round in range(2 if len(bodies) > 1 else 1):
        entries = []
        regions: list[np.ndarray] = []
        for number, body in enumerate(bodies):
            counts, _pairs, centre, quanta = lays[number]
            index = names.index(str(body["family"]))
            others = list(laid_messages)  # the messages, then the other bodies as laid
            for other, (_counts, laid_pairs, _centre, _quanta) in enumerate(lays):
                if other != number and laid_pairs:
                    others.append(
                        (names.index(str(bodies[other]["family"])), records[other], laid_pairs)
                    )
            board = board_of(shape, wrap, gamma, integers, pairs[body["family"]])
            rows = held_rows(universe, str(body["family"]))
            sense = (senses or [])[number] if number < len(senses or []) else 0
            if sense not in (-1, 0, 1):
                raise ValueError(f"bodies[{number}]: a sense is +1 or -1 (0: none), got {sense}")
            if sense and not family_of(universe, str(body["family"])).plane:
                raise ValueError(
                    f"bodies[{number}]: a body of {body['family']!r}, a family of dimension one, is laid with "
                    "no sense: a rotating record is a plane, dimension two (ALGEBRA.md #a-familys-declaration)"
                )
            if number in pixels:
                if not sense:
                    raise ValueError(
                        f"bodies[{number}] is laid as a one-Node record with no sense: the declaration is one "
                        "quantum of a plane, its Wronskian sense x T / 2 (ALGEBRA.md, the quantum of a family)"
                    )
                record, pairs_kept = pixel_record(board, counts, centre, sense, families[index].planes)
                region, laid = dilated(counts > 0, wrap), counts
                lays[number] = (laid, pairs_kept, centre, quanta)
                entry = body_entry(record, board, region, body, quanta, record.amplitude)
                entry["lay"] = {"kind": DECLARATION, "declaration": pixel_record.__doc__}
                entry["nodes"] = [
                    {"node": [int(x), int(y), int(z)], "count": int(counts[x, y, z])}
                    for x, y, z in zip(*np.nonzero(counts), strict=True)
                ]
                print(
                    f"GAMEBOARD bodies[{number}] is laid as the one-Node record of {quanta} quanta at the Node "
                    f"{list(centre)}, a declaration: the amplitude {record.amplitude}, its share {record.carried} "
                    "quanta at the Node, no fixed point and no standing check",
                    file=sys.stderr,
                    flush=True,
                )
                levels = [level for pair in pairs_kept[: len(("now", "before"))] for level in pair]
                words = ("now", "before", "im_now", "im_before")
                entry["moving"] = {
                    word: level.ravel().tolist() for word, level in zip(words, levels, strict=True)
                }
                entries.append(entry)
                continue
            arguments = (board, families, index, records[number], rows, (all_counts - counts, others))
            weights = laid_weights(body, f"bodies[{number}]", families[index])  # the lines' weights
            trajectory: Trajectory = []
            try:
                if lay is not None and lay.kind == FIXED_POINT:
                    laid, record, region, _content, pairs_kept, trajectory = unit_fixed_point(
                        *arguments, centre, quanta, counts, sense, lay, weights
                    )
                else:
                    laid, record, region, _content, pairs_kept = body_fixed_point(
                        *arguments, centre, quanta, counts, sense, weights
                    )
            except RestCollapses as refusal:
                raise ValueError(
                    f"the body of {quanta} quanta about the Node {list(centre)} collapses: its wells reach the "
                    f"pace 0 ({refusal}; the rows reading their own levels, ALGEBRA.md #the-paces, Every row "
                    "reads the content; a frozen clock, The paces compose)"
                ) from refusal
            levels = [level for pair in pairs_kept[:2] for level in pair] if sense else []  # one plane
            try:
                weighted, content, angles = read_at_the_start(
                    board, families, index, records[number], others, region, pairs_kept
                )
            except RestCollapses as refusal:
                raise ValueError(
                    f"the body of {quanta} quanta about the Node {list(centre)} collapses at the start's read: "
                    f"{refusal} (a frozen clock; ALGEBRA.md #the-paces, The paces compose)"
                ) from refusal
            stands = weighted > 0
            if not stands.any():  # the law's count 1 over the mode's Nodes: the declaration stands
                weighted, stands = declared(body, shape)[0], region & (pairs_kept[0][0] != 0)
                print(
                    f"GAMEBOARD no Node carries a whole quantum of the body of {quanta} quanta about the Node "
                    f"{list(centre)}: its count stands at its declared Node, which the gate admits within its "
                    f"rounding; its record stands on {int(stands.sum())} Nodes",
                    file=sys.stderr,
                    flush=True,
                )
            standing_check(board, content, angles, pairs_kept, stands, centre, record.clock)
            for other, taken in enumerate(regions):
                if other not in pixels and bool(np.any(taken & region)):
                    raise ValueError(
                        f"bodies[{number}] and bodies[{other}] share a Node in their regions: two bodies stand apart or are one body"
                    )
            regions.append(region)
            all_counts = all_counts - counts + laid
            lays[number] = (laid, pairs_kept, centre, quanta)
            entry = body_entry(record, board, region, body, quanta, int(record.clock[1]))
            if lay is not None:  # the lay as declared, its seed by name, the fixed-point trajectory
                entry["lay"] = {"kind": lay.kind, "seed": lay.seed}
                if trajectory:
                    entry["lay"].update(stop=lay.stop, trajectory=trajectory)
            entry["nodes"] = [
                {"node": [int(x), int(y), int(z)], "count": int(weighted[x, y, z])}
                for x, y, z in zip(*np.nonzero(weighted), strict=True)
            ]
            if levels:
                words = ("now", "before", "im_now", "im_before")
                entry["moving"] = {
                    word: level.ravel().tolist() for word, level in zip(words, levels, strict=True)
                }
            entries.append(entry)
    for body, entry in zip(bodies, entries, strict=True):
        body["nodes"] = entry.pop("nodes")
    messages = [
        message_entry(
            board_of(shape, wrap, gamma, integers, pairs[str(message["family"])]),
            message,
            beyond,
            family_of(universe, str(message["family"])),
            f"messages[{number}]",
        )
        for number, message in enumerate(document_messages)
    ]
    return {"world_digest": input_digest(document), "bodies": entries, "messages": messages}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="the world file of bodies, rewritten with their Nodes and counts",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="the mode file to write; beside the world as <world>.mode.json when omitted",
    )
    parser.add_argument(
        "--sense",
        type=int,
        nargs="*",
        default=[],
        help="the rotation sense of each body in the world's order, +1 or -1 (0: a real record, neutral)",
    )
    parser.add_argument(
        "--pixel",
        type=int,
        nargs="*",
        default=[],
        help="the numbers of the bodies laid as the one-Node record of their quanta at their declared Node, a declaration by name (the atom's nucleus)",
    )
    args = parser.parse_args(argv)
    document = json.loads(args.input.read_text(encoding="utf-8"))
    designed = designed_quanta(args.input, len(cast(list[Any], document.get("bodies", []))))
    mode = pixel_mode(document, list(args.sense), designed, tuple(args.pixel))
    args.input.write_text(json.dumps(document) + "\n", encoding="utf-8")
    out = args.out if args.out is not None else args.input.with_suffix(".mode.json")
    out.write_text(json.dumps(mode, separators=(",", ":")) + "\n", encoding="utf-8")
    for body in mode["bodies"]:
        reading = {key: value for key, value in body.items() if key not in ("profile", "moving")}
        reading["nodes"] = sum(1 for level in body["profile"] if level)
        print(json.dumps(reading))
    for message in mode["messages"]:
        reading = {key: value for key, value in message.items() if key != "moving"}
        reading["nodes"] = sum(1 for level in message["moving"]["now"]["values"] if level)
        print(json.dumps(reading))


if __name__ == "__main__":
    main()
