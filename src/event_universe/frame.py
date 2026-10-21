"""The frame of a bound record as the engine holds it, integers alone (the sprint of 2026-10-21, builder L; the frame out of the engine on the owner's rule, only integers and Rule3 at the step, every number chosen outside the engine at the start; ALGEBRA.md, The static frame and the two gauges; The emission of a bound record is the click's act of the taker): the host's tool tools/frame_of.py reads the standing line's modes in doubles once at the lay and writes into the body's mode entry the integers the taker needs (loader/mode.py `frame_of`, the key `frame`, a declared layer the Node never sees): its levels as rotation pairs (den cos Omega, den) with their sines den sin Omega by the one search and their degenerate counts, its transition (the upper the level of its largest share, the lower the lowest, the next above where the two are one), its unit W_rec = W_c sin(Omega_upper - Omega_lower) in thirds under the Lorentz form, its period, its standing region (the Nodes of its largest shares holding half its record's share), its shares per level at the lay in parts of the unit and per level one compiled profile, the level's standing form at one quantum over the board. The engine reads them (`frame_of`), keeps the gauge, the acts the phase act applied at every Node this interval and since the lay (`turns_of`, `advanced`: L p_0 / Gamma rounded once, `node.turning`, the same integers the phase act applies on each Link), and writes a record into a level at one quantum through the one lay act (`relaid`): the compiled profile turned at every Node by the one act's pair (cos theta_0, sin theta_0) raised to the acts since the lay (`act_pair`, `powered`: the pair's integer powers by repeated squaring, each product of two pairs rounded once by the engine's signed rounding at the pair's amplitude, the count's halving the division act, no function of an angle), the level before at the level's own pair one interval earlier, the shares after the write the written level whole; the write carries the lay's phase (the arriving record's fitted phase is the tool's reading and not the engine's, named). No float, no root, no fit and no number of the law here; the Node knows none of it."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from event_universe import node
from event_universe.core import paces
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.features.phase import signed_rounded
from event_universe.lay import laid
from event_universe.loader.derived import FamilyRule
from event_universe.loader.mode import FrameEntry, Levels
from event_universe.records import Record, record_slice

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


@dataclass
class Level:
    """One level of the frame as the mode file holds it: its rotation as the integer pair (den cos Omega, den), its sine den sin Omega and the count of its degenerate modes."""

    pair: tuple[int, int]
    sine: int
    modes: int


@dataclass
class Frame:
    """A record's frame: its family and record, the holder it reads, its levels in energy order, the two of its transition (`lower`, `upper`), the unit W_rec, the period, its standing region as a mask over the board, its shares per level in parts of the unit (the lay's, then the writes': the written level whole), per level its compiled profile at one quantum (the mode file's nonzero Nodes), the one act's pair at its amplitude (`act_pair`), the acts the phase act applied at every Node this interval (`turns`) and since the lay (`acts`, the gauge a write is turned by)."""

    index: int
    record: int
    holder: int
    levels: list[Level]
    lower: int
    upper: int
    unit: int
    period: int
    region: np.ndarray
    shares: list[int]
    profiles: tuple[Levels, ...]
    act: tuple[int, int, int]
    turns: np.ndarray
    acts: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=object))


def act_pair(amplitude: int, gamma: int) -> tuple[int, int, int]:
    """The phase line's one act as an integer pair at the amplitude X 2 Gamma^2: (X (2 Gamma^2 - 1), the sine by the one search, the amplitude), 2 cos theta_0 = 2 - 1 / Gamma^2 (features/phase, K_0 over D); no function of an angle."""
    scale = amplitude * 2 * gamma * gamma
    cosine = scale - amplitude  # X 2 Gamma^2 cos theta_0 = X (2 Gamma^2 - 1)
    return cosine, largest_below(scale * scale - cosine * cosine), scale


def turns_of(board: Lattice, index: int, record: int) -> np.ndarray:
    """The count of phase acts per interval the record's turn reads at every Node, L p_0 / Gamma rounded once (`node.turning`, `paces.turn_factor`, the same integers the phase act applies on each Link as the two ends' difference): the well's angle U_i = -count theta_0 (the lay's convention, tools/standing_lay.py: the well positive at the centre)."""
    angles = node.turning(index, board.families, board.states, 1, record)
    assert angles is not None  # a frame is read for a turned record alone
    clock = node.rulers(
        index, board.families, board.states, 1, board.wrap, board.world.node_clock, record
    )
    counts = paces.turn_factor(angles[0], clock[0], board.world.node_clock)
    return np.asarray(np.broadcast_to(np.asarray(counts, dtype=object), board.shape), dtype=object)


def frame_of(board: Lattice, index: int, record: int, entry: FrameEntry) -> Frame:
    """A turned record's frame from its mode entry at the lay (loader/mode.py `frame_of`): the levels, the transition, the unit, the period, the region's mask from its flat indexes, the shares and the profiles the tool wrote, the act's pair at the board's amplitude, and the gauge at the lay, the first interval's acts (`turns_of`)."""
    region = np.zeros(board.shape, dtype=bool).reshape(-1)
    region[list(entry.region)] = True
    turns = turns_of(board, index, record)
    levels = [
        Level(pair, sine, modes)
        for pair, sine, modes in zip(entry.levels, entry.sines, entry.modes, strict=True)
    ]
    return Frame(
        index,
        record,
        node.sign_holder(index, board.families),
        levels,
        entry.lower,
        entry.upper,
        entry.unit,
        entry.period,
        region.reshape(board.shape),
        list(entry.shares),
        entry.profiles,
        act_pair(board.amplitude, board.world.node_clock),
        turns,
        turns.copy(),
    )


def advanced(board: Lattice, frame: Frame) -> None:
    """The frame's gauge advanced by one interval: the acts the phase act applied at every Node this interval (`turns_of`, read from the rows as they stand at the interval's end, the potential the next step reads) added to the acts accumulated since the lay."""
    frame.turns = turns_of(board, frame.index, frame.record)
    frame.acts = frame.acts + frame.turns


def powered(act: tuple[int, int, int], count: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The act's pair raised to the signed count at every Node, (X cos(n theta_0), X sin(n theta_0)) at the pair's amplitude X: by repeated squaring on the count's size, each product of two pairs rounded once by the engine's signed rounding (features/phase `signed_rounded`), the count's halving one division act, the sine's sign the count's (the pair at -n the conjugate of the pair at +n)."""
    cosine, sine, scale = act
    signed = np.asarray(count, dtype=object)
    remaining = np.abs(signed)
    found_cosine = np.full(remaining.shape, scale, dtype=object)
    found_sine = np.zeros(remaining.shape, dtype=object)
    base_cosine = np.full(remaining.shape, cosine, dtype=object)
    base_sine = np.full(remaining.shape, sine, dtype=object)
    while np.any(remaining > 0):
        remaining, odd = division_forward(remaining, 2, 0)
        taken = odd == 1
        real = signed_rounded(found_cosine * base_cosine - found_sine * base_sine, scale)
        imaginary = signed_rounded(found_cosine * base_sine + found_sine * base_cosine, scale)
        found_cosine = np.where(taken, real, found_cosine)
        found_sine = np.where(taken, imaginary, found_sine)
        base_cosine, base_sine = (
            signed_rounded(base_cosine * base_cosine - base_sine * base_sine, scale),
            signed_rounded(base_cosine * base_sine + base_sine * base_cosine, scale),
        )
    return found_cosine, np.where(signed < 0, -found_sine, found_sine)


def relaid(board: Lattice, frame: Frame, level: int, region: np.ndarray | None) -> None:
    """The record re-laid in one level at one quantum through the one lay act (`lay.laid`), the shortcut of the write-back at the click's interval (the run back to the birth is the law's path, open): the level's compiled profile A phi (the mode file's, one quantum by the invariant 2 A^2 sin omega_0 SUM phi^2 = T) turned at every Node by the act's pair raised to the acts accumulated since the lay (`powered`), the level now P A phi and the level before P' A phi (cos Omega, sin Omega), P' the pair one interval earlier, in the engine's gauge (lattice.step applies the phase act before Rule3), each product rounded once by the engine's signed rounding, every Node of the board (or of `region`) at the lay's origin; the shares after it the written level whole."""
    found = frame.levels[level]
    scale = frame.act[2]
    profile = board.board_array(frame.profiles[level]).astype(object)
    now_cosine, now_sine = powered(frame.act, frame.acts)
    before_cosine, before_sine = powered(frame.act, frame.acts - frame.turns)
    (num, den), turned_sine = found.pair, found.sine
    real, imaginary = signed_rounded(profile * num, den), signed_rounded(profile * turned_sine, den)
    now = (signed_rounded(profile * now_cosine, scale), signed_rounded(profile * now_sine, scale))
    before = (
        signed_rounded(real * before_cosine - imaginary * before_sine, scale),
        signed_rounded(real * before_sine + imaginary * before_cosine, scale),
    )
    first = record_slice(board.families[frame.index], frame.record).start
    at = np.ones(board.shape, dtype=bool) if region is None else region
    origin = board.half_wall(frame.index)
    for number, (new_now, new_before) in enumerate(zip(now, before, strict=True)):
        line: Record = board.states[frame.index].lines[first + number]
        changes = (
            np.asarray(np.where(at, new_now - np.asarray(line.now, dtype=object), 0), dtype=int),
            np.asarray(np.where(at, new_before - np.asarray(line.before, dtype=object), 0), dtype=int),
        )
        laid(board, frame.index, first + number, changes, None, origin, at)
    frame.shares = [frame.unit if k == level else 0 for k in range(len(frame.levels))]


def level_kind(family: FamilyRule, level: Level) -> str:
    """A level's word in the reader's lines: its rotation pair and the count of its degenerate modes, no letter of the spectroscopist's."""
    return f"level [{level.pair[0]}, {level.pair[1]}] x{level.modes} of {family.name!r}"
