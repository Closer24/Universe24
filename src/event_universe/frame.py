"""The frame of a bound record, a lattice reading made once at the lay and never typed (the sprint of 2026-10-21, builder L; ALGEBRA.md, The static frame and the two gauges; the cold reader's recipes in tools/standing_lay.py, the same standing line read here by the engine for the taker's unit and window): a turned record standing in the well of the holder of the sign it reads has the modes of Rule3's own standing line, 2 cos(Omega + U_i) phi_i = SUM_j (R_ij / w) phi_j + (S_i / w) phi_i, U_i the well's angle at the Node (the count of phase acts per interval the record's turn reads there, `turns_of`, times the phase line's angle theta_0 = 1 / Gamma), read as the symmetric eigenproblem B chi = 2 cos Omega chi with B_ij = (R_ij / w) (p_j / p_i) / sqrt(cos U_i cos U_j), B_ii = S_i / w + 2 sin Omega sin U_i / cos U_i and phi_i = p_i chi_i / sqrt(cos U_i), each level's Omega at its own fixed point, every root by the one search on the integers (`rule3.largest_below` at the phase line's amplitude), every angle a pair (cosine, sine) and never a function of an angle, the lowest six levels kept and labelled by their energy order alone (the degenerate ones one level); the record's share in each level by the least-squares fit of its gauge-flat levels on the modes (`shares_of`); the transition the record carries (`transition_of`: the upper the level of its largest share, the lower the lowest level, the next level above where the two are one), its unit W_rec = W_c sin(Omega_upper - Omega_lower) by the angle difference of the two pairs (in thirds under the Lorentz form, as `credit.record_unit` reads a unit) and its period, the count of turns of the transition's pair that closes the circle, the taker's window; and the re-lay of a level at a count whole at any interval in the engine's own gauge (`relaid`), the one lay act with no level written by hand. Nothing here is a number of the law or a name; the Node knows none of it."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from event_universe import node
from event_universe.core import paces
from event_universe.core.ports import PORT_SIDES, PORTS, arrival
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.covector import THIRDS
from event_universe.lay import laid
from event_universe.loader.derived import FamilyRule
from event_universe.records import Record, record_slice

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

SETTLED = PORTS  # a level's fixed point: at most six solves, the secant on the integer pair, stopped at the pair's own grain


@dataclass
class Level:
    """One level of the frame: its rotation as the integer pair (den cos Omega, den), its sine den sin Omega by the one search, its modes' profiles over the board as columns (one for a simple level, several for a degenerate one, orthonormal in the weight cos U) and its weight SUM phi^2 sin(Omega + U) per column."""

    pair: tuple[int, int]
    sine: int
    profiles: np.ndarray
    weights: np.ndarray


@dataclass
class Frame:
    """A record's frame: its family and record, the holder it reads, the well's count of acts per Node at the lay (`turns`), cos U and sin U per Node, the phase pair of one act (cos theta_0, sin theta_0) as floats of the engine's integers, its levels in energy order, the two of its transition (`lower`, `upper`), the unit W_rec and the period, and the acts accumulated since the lay per Node (`acts`, the gauge the shares are read in, advanced once per interval by the taker)."""

    index: int
    record: int
    holder: int
    turns: np.ndarray
    cosine: np.ndarray
    sine: np.ndarray
    act: complex
    levels: list[Level]
    lower: int
    upper: int
    unit: int
    period: int
    acts: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=object))


def act_pair(amplitude: int, gamma: int) -> complex:
    """The phase line's one act as a complex number of modulus 1, (cos theta_0, sin theta_0) with 2 cos theta_0 = 2 - 1 / Gamma^2 (features/phase, K_0 over D), the sine by the one search at the amplitude X: no function of an angle."""
    scale = amplitude * 2 * gamma * gamma
    cosine = scale - amplitude  # X 2 Gamma^2 cos theta_0 = X (2 Gamma^2 - 1)
    sine = largest_below(scale * scale - cosine * cosine)
    return complex(cosine / scale, sine / scale)


def turns_of(board: Lattice, index: int, record: int) -> np.ndarray:
    """The count of phase acts per interval the record's turn reads at every Node, L p_0 / Gamma rounded once (`node.turning`, `paces.turn_factor`, the same integers the phase act applies on each Link as the two ends' difference): the well's angle U_i = -count theta_0 (the lay's convention, tools/standing_lay.py: the well positive at the centre)."""
    angles = node.turning(index, board.families, board.states, 1, record)
    assert angles is not None  # a frame is read for a turned record alone
    clock = node.rulers(
        index, board.families, board.states, 1, board.wrap, board.world.node_clock, record
    )
    counts = paces.turn_factor(angles[0], clock[0], board.world.node_clock)
    return np.asarray(np.broadcast_to(np.asarray(counts, dtype=object), board.shape), dtype=object)


def well_pair(turns: np.ndarray, act: complex) -> tuple[np.ndarray, np.ndarray]:
    """cos U_i and sin U_i at every Node from the count of acts, the act's power by complex multiplication, U_i = -count theta_0."""
    phasor = np.power(act, -turns.astype(int))
    return np.asarray(phasor.real, dtype=float), np.asarray(phasor.imag, dtype=float)


def rooted(values: np.ndarray, amplitude: int) -> np.ndarray:
    """The square roots of positive floats by the one search on the integers at the phase line's amplitude: sqrt(v) = largest_below(X X v) / X."""
    flat = [
        largest_below(int(round(float(value) * amplitude * amplitude))) / amplitude
        for value in values.ravel()
    ]
    return np.asarray(flat, dtype=float).reshape(values.shape)


def operator(board: Lattice, frame: Frame, sine_omega: float) -> np.ndarray:
    """The symmetric operator of the standing line at the angle whose sine is `sine_omega` (tools/standing_lay.py's `operator` on the engine's own rule integers of the record's read, `node.rule_of`, in doubles): B_ij = (R_ij / w) (p_j / p_i) / sqrt(cos U_i cos U_j) over each Link whose far Node stands on the board (the fill beyond a face, the wrap on a periodic axis, the reach back on the diagonal on an axis of one layer), B_ii = S_i / w + 2 sin Omega sin U_i / cos U_i, symmetrised as the mean with its transpose."""
    content, factors = board.read(frame.index, 1, frame.record)
    rule = node.rule_of(
        board.families[frame.index], board.world.node_clock, content, factors, board.unit
    )
    pace = np.broadcast_to(
        np.asarray(paces.link_pace_of(board.world.node_clock, content), dtype=float), board.shape
    )
    wall = float(rule.wall)
    size = int(np.prod(board.shape))
    index = np.arange(size).reshape(board.shape)
    scale = 1 / rooted(frame.cosine, board.amplitude)
    relative = (pace / pace.max()).ravel()
    own = np.broadcast_to(np.asarray(rule.self_coefficient, dtype=float), board.shape).ravel() / wall
    diagonal = own + 2 * sine_omega * frame.sine.ravel() / frame.cosine.ravel()
    found = np.zeros((size, size), dtype=float)
    flat_scale = scale.ravel()
    for port, (axis, side) in enumerate(PORT_SIDES):
        reach = np.broadcast_to(np.asarray(rule.reaches[port], dtype=float), board.shape).ravel() / wall
        if board.shape[axis] == 1:
            diagonal = diagonal + reach
            continue
        far = arrival(index, axis, side, board.wrap, -1).ravel()
        near = np.nonzero(far >= 0)[0]
        there = far[near]
        found[near, there] += (
            reach[near] * flat_scale[near] * flat_scale[there] * relative[there] / relative[near]
        )
    found = (found + found.T) / 2
    found[np.arange(size), np.arange(size)] += diagonal
    return found


def integer_pair(cosine: float, den: int) -> tuple[tuple[int, int], int]:
    """A rotation's integer pair from its cosine, (den cos Omega rounded, den) with den sin Omega by the one search; the cosine clipped to the circle."""
    num = max(-den, min(den, int(round(cosine * den))))
    return (num, den), largest_below(den * den - num * num)


def levels_of(board: Lattice, frame: Frame, kept: int) -> list[Level]:
    """The frame's lowest `kept` levels, each at its own fixed point (`SETTLED` iterations from the record's rest rotation, the eigenvector followed by its overlap, one solve per distinct sine), in energy order, the modes of one rotation pair gathered into one degenerate level with orthonormal columns (`Level`), their weights SUM phi^2 sin(Omega + U) per column."""
    den = board.families[frame.index].pair[1]
    scale = rooted(
        frame.cosine, board.amplitude
    ).ravel()  # sqrt(cos U): phi = chi / sqrt(cos U) at uniform paces
    solved: dict[int, tuple[np.ndarray, np.ndarray]] = {}

    def solve(sine: int) -> tuple[np.ndarray, np.ndarray]:
        if sine not in solved:
            found = np.linalg.eigh(operator(board, frame, sine / den))
            solved[sine] = (np.asarray(found[0]), np.asarray(found[1]))
        return solved[sine]

    values, vectors = solve(largest_below(den * den - board.families[frame.index].pair[0] ** 2))
    found: list[tuple[tuple[int, int], int, np.ndarray]] = []
    for first in np.argsort(-values)[:kept]:
        vector, (pair, sine) = vectors[:, first], integer_pair(values[first] / 2, den)
        guesses: list[tuple[int, int]] = []  # (the sine put in, the cosine's numerator read out)
        for _step in range(SETTLED):
            own_values, own_vectors = solve(sine)
            rank = int(np.argmax(np.abs(own_vectors.T @ vector)))
            vector, (read, _sine) = own_vectors[:, rank], integer_pair(own_values[rank] / 2, den)
            guesses.append((sine, read[0]))
            put = largest_below(den * den - read[0] * read[0])  # the sine the read cosine asks for
            if put == sine:
                pair = read
                break
            if len(guesses) > 1 and guesses[-1][1] != guesses[-2][1]:  # the secant on the fixed point
                (s_1, c_1), (s_2, _c_2) = guesses[-2], guesses[-1]
                f_1, f_2 = largest_below(den * den - c_1 * c_1) - s_1, put - s_2
                if f_2 != f_1:
                    put = int(round(s_2 - f_2 * (s_2 - s_1) / (f_2 - f_1)))
            pair, sine = read, max(0, min(den, put))
        found.append((pair, sine, vector / scale))
    found.sort(key=lambda level: -level[0][0])
    levels: list[Level] = []
    for pair, sine, profile in found:
        if levels and levels[-1].pair == pair:
            levels[-1].profiles = np.column_stack([levels[-1].profiles, profile])
            continue
        levels.append(Level(pair, sine, profile.reshape(-1, 1), np.zeros(0)))
    for level in levels:
        columns, _ = np.linalg.qr(level.profiles * scale[:, None])  # orthonormal in the weight cos U
        level.profiles = columns / scale[:, None]
        sine_up = level.sine / den * frame.cosine.ravel() + level.pair[0] / den * frame.sine.ravel()
        level.weights = np.asarray(
            [float((column * column * sine_up).sum()) for column in level.profiles.T]
        )
    return levels


def gauge_flat(board: Lattice, frame: Frame) -> tuple[np.ndarray, np.ndarray]:
    """The record's level pair in the static frame at this interval, u = z conj(P) with P = act^acts the phasor of the acts accumulated at the Node since the lay (now) and one interval fewer (before): complex arrays over the Nodes."""
    lines = board.lines_of(frame.index, frame.record)
    now = np.asarray(lines[0].now, dtype=float) + complex(0, 1) * np.asarray(lines[1].now, dtype=float)
    before = np.asarray(lines[0].before, dtype=float) + complex(0, 1) * np.asarray(
        lines[1].before, dtype=float
    )
    acts = frame.acts.astype(int)
    phasor = np.power(frame.act, acts).ravel()
    earlier = np.power(frame.act, acts - frame.turns.astype(int)).ravel()
    return now.ravel() * np.conj(phasor), before.ravel() * np.conj(earlier)


def shares_of(board: Lattice, frame: Frame) -> tuple[list[float], list[np.ndarray]]:
    """The record's share in each level at this interval: the gauge-flat level now fitted on every level's columns by least squares, the level's energy SUM over its columns of |a|^2 weight, as fractions of their total, with the coefficients per level (the phase the re-lay carries)."""
    flat, _before = gauge_flat(board, frame)
    basis = np.column_stack([level.profiles for level in frame.levels])
    coefficients, *_ = np.linalg.lstsq(basis, flat, rcond=None)
    energies, found, at = [], [], 0
    for level in frame.levels:
        width = level.profiles.shape[1]
        own = coefficients[at : at + width]
        energies.append(float((np.abs(own) ** 2 * level.weights).sum()))
        found.append(own)
        at += width
    total = sum(energies)
    return [e / total if total > 0 else 0 / 1 for e in energies], found


def transition_of(fractions: list[float]) -> tuple[int, int]:
    """The transition a record carries from its shares: the upper level the one of its largest share, the lower the lowest level; where the two are one the lower level and the one above it (the gap to the next level)."""
    upper = max(range(len(fractions)), key=lambda k: fractions[k])
    return (0, 1) if upper == 0 else (0, upper)


def transition_unit(board: Lattice, frame: Frame) -> int:
    """W_rec of the frame's transition, W_c sin(Omega_upper - Omega_lower) by the angle difference of the two pairs, W_c = 3 den T of the holder the record reads (its light's wall), in thirds under the Lorentz form (`covector.THIRDS`, as `credit.record_unit` reads the holder's unit): one division act on the integers."""
    low, high = frame.levels[frame.lower], frame.levels[frame.upper]
    den = low.pair[1]
    sine = high.sine * low.pair[0] - high.pair[0] * low.sine  # den^2 sin(Omega_u - Omega_l)
    holder = board.families[frame.holder]
    wall = 3 * holder.pair[1] * board.world.quantum_action * (THIRDS if holder.lorentz else 1)
    return int(division_forward(wall * sine, den * den, 0)[0])


def period_of(frame: Frame) -> int:
    """The transition's period in intervals: the count of turns of the pair (cos Omega, sin Omega), Omega = Omega_upper - Omega_lower, that brings the unit back across the start, 2 pi / Omega rounded up, counted by complex multiplication alone; 0 where the transition has no angle."""
    low, high = frame.levels[frame.lower], frame.levels[frame.upper]
    den = low.pair[1]
    turn = complex(
        (high.pair[0] * low.pair[0] + high.sine * low.sine) / (den * den),
        (high.sine * low.pair[0] - high.pair[0] * low.sine) / (den * den),
    )
    if turn.imag <= 0:
        return 0
    pointer, count, passed = turn, 1, False
    while not (passed and pointer.imag >= 0):
        pointer, count, passed = pointer * turn, count + 1, passed or pointer.imag < 0
    return count


def frame_of(board: Lattice, index: int, record: int) -> Frame | None:
    """A turned record's frame at the lay (`turns_of`, `levels_of`, `shares_of`, `transition_of`, `transition_unit`, `period_of`), None where it carries no transition with an angle (a frozen record, every level at one rotation)."""
    holder = node.sign_holder(index, board.families)
    act = act_pair(board.amplitude, board.world.node_clock)
    turns = turns_of(board, index, record)
    cosine, sine = well_pair(turns, act)
    frame = Frame(index, record, holder, turns, cosine, sine, act, [], 0, 0, 0, 0, turns.copy())
    frame.levels = levels_of(board, frame, PORTS)
    if len(frame.levels) < 2:  # a frozen record: every level at one rotation, no transition
        return None
    fractions, _coefficients = shares_of(board, frame)
    frame.lower, frame.upper = transition_of(fractions)
    frame.unit, frame.period = transition_unit(board, frame), period_of(frame)
    return frame if frame.unit > 0 and frame.period > 0 else None


def advanced(board: Lattice, frame: Frame) -> None:
    """The frame's gauge advanced by one interval: the acts the phase act applied at every Node this interval (`turns_of`, read from the rows as they stand at the interval's end, the potential the next step reads) added to the acts accumulated since the lay."""
    frame.turns = turns_of(board, frame.index, frame.record)
    frame.acts = frame.acts + frame.turns


def relaid(
    board: Lattice,
    frame: Frame,
    level: int,
    coefficients: np.ndarray,
    count: int,
    region: np.ndarray | None,
) -> None:
    """The record re-laid in one level at `count` whole quanta through the one lay act (`lay.laid`), the shortcut of the write-back at the click's interval (the run back to the birth is the law's path, open): the level's profile in the direction of `coefficients` within the level (its columns' combination turned to the real axis at its largest component, the first column where none stands, the combination's imaginary part dropped and named), the amplitude by the invariant 2 A^2 sin omega_0 SUM phi^2 = count T per quantum (`features/click.standing`'s rule over a spread profile, the root by the one search at the phase line's amplitude), the phase the coefficients' own, the level now P A phi e^(i theta) and the level before P' A phi e^(i (theta + Omega)) in the engine's gauge (P the acts' phasor now, P' one interval earlier), rounded to the integers, every Node of the board (or of `region`) at the lay's origin."""
    found = frame.levels[level]
    weights = coefficients if np.abs(coefficients).sum() > 0 else np.eye(found.profiles.shape[1])[0]
    pivot = weights[int(np.argmax(np.abs(weights)))]
    unit = pivot / abs(pivot)
    profile = np.real(
        found.profiles @ (weights / unit)
    )  # the standing profile, its phase kept in `unit`
    profile = profile / np.abs(profile).max()  # 1 at its largest, the root's precision at the peak
    num, den = board.families[frame.index].pair
    scale = board.amplitude
    grains = [int(round(float(value) * scale)) for value in profile]
    norm = sum(grain * grain for grain in grains)
    sine_free = largest_below(den * den - num * num)
    square = division_forward(
        count * board.world.quantum_action * den * scale * scale, 2 * sine_free * norm, 0
    )
    amplitude = largest_below(
        int(square[0])
    )  # A at the profile's peak: 2 A^2 sin omega_0 SUM phi^2 = count T
    turn = complex(found.pair[0] / den, found.sine / den)
    acts = frame.acts.astype(int)
    now = np.power(frame.act, acts).ravel() * amplitude * profile * unit
    before = (
        np.power(frame.act, acts - frame.turns.astype(int)).ravel() * amplitude * profile * unit * turn
    )
    first = record_slice(board.families[frame.index], frame.record).start
    at = np.ones(board.shape, dtype=bool) if region is None else region
    origin = board.half_wall(frame.index)
    for number, (new_now, new_before) in enumerate(((now.real, before.real), (now.imag, before.imag))):
        line: Record = board.states[frame.index].lines[first + number]
        target_now = np.rint(new_now).astype(int).reshape(board.shape)
        target_before = np.rint(new_before).astype(int).reshape(board.shape)
        changes = (
            np.where(at, target_now - np.asarray(line.now), 0),
            np.where(at, target_before - np.asarray(line.before), 0),
        )
        laid(board, frame.index, first + number, changes, None, origin, at)


def level_kind(family: FamilyRule, level: Level) -> str:
    """A level's word in the reader's lines: its rotation pair and the count of its degenerate modes, no letter of the spectroscopist's."""
    return f"level [{level.pair[0]}, {level.pair[1]}] x{level.profiles.shape[1]} of {family.name!r}"
