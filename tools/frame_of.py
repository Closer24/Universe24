"""The frame of a bound record, the host's reading of the lattice at the lay, typed into the mode file as a bound body's declaration as an instrument body, integers alone (2026-10-21, the frame out of the engine on the owner's rule: only integers and Rule3 at the step, every number chosen outside the engine at the start; the owner's word of 2026-10-21, "the builder builds it all in code"; the reader's design of the conserving click, (b): the parts, the transition and the resonance written into the mode file by this tool as a derived declaration, "declaring what the law derives until the body runs", ALGEBRA.md, The click writes on the lattice (3) and (4); The emission of a bound record is the click's act of the taker; tools/standing_lay.py lays the same standing line, this tool reads it for the body's instrument): a turned record standing in the well of the holder of the sign it reads has the modes of Rule3's own standing line, 2 cos(Omega + U_i) phi_i = SUM_j (R_ij / w) phi_j + (S_i / w) phi_i, U_i the well's angle at the Node (the count of phase acts per interval the record's turn reads there, `turns_of`, times the phase line's angle theta_0 = 1 / Gamma), read as the symmetric eigenproblem B chi = 2 cos Omega chi with B_ij = (R_ij / w) (p_j / p_i) / sqrt(cos U_i cos U_j), B_ii = S_i / w + 2 sin Omega sin U_i / cos U_i and phi_i = p_i chi_i / sqrt(cos U_i), in doubles, each level's Omega at its own fixed point, every root by the one search on the integers (`rule3.largest_below` at the phase line's amplitude), every angle a pair (cosine, sine) and never a function of an angle, the lowest six levels kept and labelled by their energy order alone (the degenerate ones one level); the record's share in each level by the least-squares fit of its gauge-flat levels on the modes (`shares_of`); the transition the record carries (`transition_of`: the upper the level of its largest share, the lower the lowest level, the next level above where the two are one), its resonance the pair [den cos(Omega_upper - Omega_lower), den] by the two levels' pairs, its unit W_rec = W_c sin(Omega_upper - Omega_lower) (in thirds under the Lorentz form, as `credit.record_unit` reads a unit) and its period, the count of turns of the transition's pair that closes the circle, the taker's window where no rate is declared; its standing region, the Nodes of its largest shares holding half its record's share, the count's own rounding as the floor, with the record's share at each as the lay's weight (`standing_region`). All of it is typed into the body's entry of the mode file beside the world under the key `instrument` (loader/mode.instrument_of reads and checks it; loader/world.instrument_body builds the declaration the engine reads for every detector body) in the form the world file declares a detector body in: `nodes` (the standing region with its weights), `parts` (the two levels of the transition by name, the count in the level the record stands in), `transitions` (the lower to the upper by the light family `--light`, at the weight `--weight`, the record's read weight of its holder where none is given, at the transition's resonance), `rates` (the upper to the lower at the lifetime `--lifetime`, the declared constant of The click writes on the lattice (5) and the lay's span, giving to the light family, as a packet `--width` Nodes across where given; none where no lifetime is given, the constant 0) and `node_detector` (the empty object where a rate is declared, the window then derived at load as the lifetime, else the transition's period, the steady beat's declared window); so that the engine's instrument-body click runs on the bound record with no new act and no body-wide re-lay: the frame's derivation is this tool's, a declared layer the Node never sees; the sources' bodies, the frozen pair and a record with no transition (every level at one rotation) get no declaration and are said so. The tool holds no number of the law: every integer is the files' and the engine's own.

Run with PYTHONPATH set to the checkout's src, after the mode file is written (tools/standing_lay.py or tools/pixel_mode.py):

    PYTHONPATH=src python tools/frame_of.py --input <world>.json --light <family> [--lifetime N] [--width w] [--weight k] [--region half|whole] [--root <folder>]
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import node, share, world_files
from event_universe.core import paces
from event_universe.core.ports import PORT_SIDES, PORTS, arrival
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.covector import THIRDS
from event_universe.lattice import Lattice
from event_universe.loader.derived import turns, weight_of
from event_universe.loader.faces import connected
from event_universe.loader.mode import INSTRUMENT
from event_universe.loader.world import BodyRow
from event_universe.world_files import load_world

LABEL = "lattice reading"
SETTLED = PORTS  # a level's fixed point: at most six solves, the secant on the integer pair, stopped at the pair's own grain


@dataclass
class Level:
    """One level of the frame: its rotation as the integer pair (den cos Omega, den), its sine den sin Omega by the one search, its modes' profiles over the board as columns (one for a simple level, several for a degenerate one, orthonormal in the weight cos U) and its weight SUM phi^2 sin(Omega + U) per column."""

    pair: tuple[int, int]
    sine: int
    profiles: np.ndarray
    weights: np.ndarray


@dataclass
class Reading:
    """A record's frame as the tool reads it: its family and record, the holder it reads, the well's count of acts per Node at the lay (`turns`), cos U and sin U per Node, the phase pair of one act (cos theta_0, sin theta_0) as a complex number of the engine's integers, its levels in energy order, the two of its transition (`lower`, `upper`), the unit W_rec and the period, and the acts accumulated at the lay per Node (`acts`, the gauge the shares are read in)."""

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
    """The square roots of positive floats by the one search on the integers at the phase line's amplitude: the root of v is largest_below(X X v) / X."""
    flat = [
        largest_below(int(round(float(value) * amplitude * amplitude))) / amplitude
        for value in values.ravel()
    ]
    return np.asarray(flat, dtype=float).reshape(values.shape)


def operator(board: Lattice, reading: Reading, sine_omega: float) -> np.ndarray:
    """The symmetric operator of the standing line at the angle whose sine is `sine_omega` (tools/standing_lay.py's `operator` on the engine's own rule integers of the record's read, `node.rule_of`, in doubles): B_ij = (R_ij / w) (p_j / p_i) / sqrt(cos U_i cos U_j) over each Link whose far Node stands on the board (the fill beyond a face, the wrap on a periodic axis, the reach back on the diagonal on an axis of one layer), B_ii = S_i / w + 2 sin Omega sin U_i / cos U_i, symmetrised as the mean with its transpose."""
    content, factors = board.read(reading.index, 1, reading.record)
    rule = node.rule_of(
        board.families[reading.index], board.world.node_clock, content, factors, board.unit
    )
    pace = np.broadcast_to(
        np.asarray(paces.link_pace_of(board.world.node_clock, content), dtype=float), board.shape
    )
    wall = float(rule.wall)
    size = int(np.prod(board.shape))
    index = np.arange(size).reshape(board.shape)
    scale = 1 / rooted(reading.cosine, board.amplitude)
    relative = (pace / pace.max()).ravel()
    own = np.broadcast_to(np.asarray(rule.self_coefficient, dtype=float), board.shape).ravel() / wall
    diagonal = own + 2 * sine_omega * reading.sine.ravel() / reading.cosine.ravel()
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


def levels_of(board: Lattice, reading: Reading, kept: int) -> list[Level]:
    """The frame's lowest `kept` levels, each at its own fixed point (`SETTLED` iterations from the record's rest rotation, the eigenvector followed by its overlap, one solve per distinct sine), in energy order, the modes of one rotation pair gathered into one degenerate level with orthonormal columns (`Level`), their weights SUM phi^2 sin(Omega + U) per column."""
    den = board.families[reading.index].pair[1]
    scale = rooted(reading.cosine, board.amplitude).ravel()  # sqrt(cos U): phi = chi / sqrt(cos U)
    solved: dict[int, tuple[np.ndarray, np.ndarray]] = {}

    def solve(sine: int) -> tuple[np.ndarray, np.ndarray]:
        if sine not in solved:
            found = np.linalg.eigh(operator(board, reading, sine / den))
            solved[sine] = (np.asarray(found[0]), np.asarray(found[1]))
        return solved[sine]

    values, vectors = solve(largest_below(den * den - board.families[reading.index].pair[0] ** 2))
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
        sine_up = level.sine / den * reading.cosine.ravel() + level.pair[0] / den * reading.sine.ravel()
        level.weights = np.asarray(
            [float((column * column * sine_up).sum()) for column in level.profiles.T]
        )
    return levels


def gauge_flat(board: Lattice, reading: Reading) -> tuple[np.ndarray, np.ndarray]:
    """The record's level pair in the static frame at the lay, u = z conj(P) with P = act^acts the phasor of the acts accumulated at the Node (now) and one interval fewer (before): complex arrays over the Nodes."""
    lines = board.lines_of(reading.index, reading.record)
    now = np.asarray(lines[0].now, dtype=float) + complex(0, 1) * np.asarray(lines[1].now, dtype=float)
    before = np.asarray(lines[0].before, dtype=float) + complex(0, 1) * np.asarray(
        lines[1].before, dtype=float
    )
    acts = reading.acts.astype(int)
    phasor = np.power(reading.act, acts).ravel()
    earlier = np.power(reading.act, acts - reading.turns.astype(int)).ravel()
    return now.ravel() * np.conj(phasor), before.ravel() * np.conj(earlier)


def shares_of(board: Lattice, reading: Reading) -> tuple[list[float], list[np.ndarray]]:
    """The record's share in each level at the lay: the gauge-flat level now fitted on every level's columns by least squares, the level's energy SUM over its columns of |a|^2 weight, as fractions of their total, with the coefficients per level (the direction a degenerate level's profile is compiled in)."""
    flat, _before = gauge_flat(board, reading)
    basis = np.column_stack([level.profiles for level in reading.levels])
    coefficients, *_ = np.linalg.lstsq(basis, flat, rcond=None)
    energies, found, at = [], [], 0
    for level in reading.levels:
        width = level.profiles.shape[1]
        own = coefficients[at : at + width]
        energies.append(float((np.abs(own) ** 2 * level.weights).sum()))
        found.append(own)
        at += width
    total = sum(energies)
    return [e / total if total > 0 else 0 for e in energies], found


def transition_of(fractions: list[float], unit: int) -> tuple[int, int]:
    """The transition a record carries from its shares: the two levels of its largest shares in energy order, the record standing in the larger's (the beat between its two laid levels; a record laid in one level has no second: the lowest level and the one above it then, the gap to the next level); a share counts where it stands above 0 in the unit's integers, as the mode file writes it."""
    order = sorted(range(len(fractions)), key=lambda k: -fractions[k])
    first, second = order[0], order[1]
    if int(round(fractions[second] * unit)) <= 0:
        return (0, 1) if first == 0 else (0, first)
    return min(first, second), max(first, second)


def transition_unit(board: Lattice, reading: Reading) -> int:
    """W_rec of the frame's transition, W_c sin(Omega_upper - Omega_lower) by the angle difference of the two pairs, W_c = 3 den T of the holder the record reads (its light's wall), in thirds under the Lorentz form (`covector.THIRDS`, as `credit.record_unit` reads the holder's unit): one division act on the integers."""
    low, high = reading.levels[reading.lower], reading.levels[reading.upper]
    den = low.pair[1]
    sine = high.sine * low.pair[0] - high.pair[0] * low.sine  # den^2 sin(Omega_u - Omega_l)
    holder = board.families[reading.holder]
    wall = 3 * holder.pair[1] * board.world.quantum_action * (THIRDS if holder.lorentz else 1)
    return int(division_forward(wall * sine, den * den, 0)[0])


def period_of(reading: Reading) -> int:
    """The transition's period in intervals: the count of turns of the pair (cos Omega, sin Omega), Omega = Omega_upper - Omega_lower, that brings the unit back across the start, 2 pi / Omega rounded up, counted by complex multiplication alone; 0 where the transition has no angle."""
    low, high = reading.levels[reading.lower], reading.levels[reading.upper]
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


def reading_of(board: Lattice, index: int, record: int) -> Reading | None:
    """A turned record's frame at the lay (`turns_of`, `levels_of`, `shares_of`, `transition_of`, `transition_unit`, `period_of`), None where it carries no transition with an angle (a frozen record, every level at one rotation)."""
    holder = node.sign_holder(index, board.families)
    act = act_pair(board.amplitude, board.world.node_clock)
    turns_now = turns_of(board, index, record)
    cosine, sine = well_pair(turns_now, act)
    reading = Reading(
        index, record, holder, turns_now, cosine, sine, act, [], 0, 0, 0, 0, turns_now.copy()
    )
    reading.levels = levels_of(board, reading, PORTS)
    if len(reading.levels) < 2:  # a frozen record: every level at one rotation, no transition
        return None
    fractions, _coefficients = shares_of(board, reading)
    reading.lower, reading.upper = transition_of(fractions, board.world.quantum_action)
    reading.unit, reading.period = transition_unit(board, reading), period_of(reading)
    return reading if reading.unit > 0 and reading.period > 0 else None


def standing_region(
    board: Lattice,
    index: int,
    record: int,
    declared: tuple[tuple[int, int, int], ...],
    whole: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    """A body's standing region at the lay: its record's share at every Node (share.family_share at the record's own read), the Nodes taken in the order of their shares until they hold half the record's share, the count's own rounding as the floor (`--region half`), or every Node where the share stands above 0, the record's whole support (`--region whole`, `whole`: the exchange's write then moves the board's share by the lay's rounding alone, where the half region leaves the tail outside it standing, the remainder the conservation table names), the body's declared Nodes among them, and the pieces joined into one region through the six Ports along the shortest Link paths between them (the loader's rule for every NodeDetector, loader/faces.connected; a level odd about a plane holds half its share in two lobes, its nodal plane carrying none, so the joining Nodes stand at the weight 1, the least, where their share is 0); the declared Node alone where the share is nowhere above 0; returned as the region's mask with the record's share at every Node, at least 1, the lay's weights the region's Nodes carry."""
    family, gamma = board.families[index], board.world.node_clock
    content, factors = board.read(index, 1, record)
    shares = share.family_share(
        family, board.lines_of(index, record), board.wrap, gamma, content, factors, board.unit
    )
    shape, periodic = board.shape, board.world.periodic
    flat = np.asarray(shares, dtype=object).ravel()
    order = sorted(range(flat.size), key=lambda k: -int(flat[k]))
    total, taken, found = int(sum(int(v) for v in flat)), 0, np.zeros(flat.size, dtype=bool)
    for at in declared:
        found[int(np.ravel_multi_index(tuple(int(v) for v in at), shape))] = True
    for place in order:
        if (2 * taken >= total and not whole) or int(flat[place]) <= 0:
            break
        if not found[place]:
            found[place], taken = True, taken + int(flat[place])
    region = found.reshape(shape)
    while not connected(tuple(tuple(int(v) for v in at) for at in np.argwhere(region)), shape, periodic):
        region |= joining_path(region, shape, periodic)
    weights = np.where(np.asarray(shares, dtype=object) > 0, np.asarray(shares, dtype=object), 1)
    return region, weights


def joining_path(
    region: np.ndarray, shape: tuple[int, int, int], periodic: tuple[bool, bool, bool]
) -> np.ndarray:
    """The Nodes of the shortest Link path from the region's first piece (the piece holding its first Node in x-major order) to any Node of another piece, by a breadth-first walk over the six Ports (the wrap on a periodic axis), the path's Nodes outside the region as a mask: the join of two pieces, added until the region is one."""
    nodes = [tuple(int(v) for v in at) for at in np.argwhere(region)]
    piece, front = {nodes[0]}, [nodes[0]]
    while front:  # the first piece
        node = front.pop()
        for axis in range(3):
            for side in (1, -1):
                there = list(node)
                there[axis] += side
                if periodic[axis]:
                    there[axis] %= shape[axis]
                at = (there[0], there[1], there[2])
                if region[at] and at not in piece and all(0 <= at[a] < shape[a] for a in range(3)):
                    piece.add(at)
                    front.append(at)
    came: dict[tuple[int, int, int], tuple[int, int, int] | None] = dict.fromkeys(piece, None)
    queue = list(piece)
    found = np.zeros(shape, dtype=bool)
    while queue:
        node = queue.pop(0)
        for axis in range(3):
            for side in (1, -1):
                there = list(node)
                there[axis] += side
                if periodic[axis]:
                    there[axis] %= shape[axis]
                if not all(0 <= there[a] < shape[a] for a in range(3)):
                    continue
                at = (there[0], there[1], there[2])
                if at in came:
                    continue
                came[at] = node
                if region[at]:  # another piece reached: the path back to the first piece
                    back: tuple[int, int, int] | None = node
                    while back is not None and not region[back]:
                        found[back] = True
                        back = came[back]
                    return found
                queue.append(at)
    return found


def compiled(board: Lattice, reading: Reading, level: int, coefficients: np.ndarray) -> list[int]:
    """A level's compiled profile at one quantum, the integers the engine lays a record in that level with: the level's profile in the direction of `coefficients` within the level (its columns' combination turned to the real axis at its largest component, the first column where none stands, the combination's imaginary part dropped and named), 1 at its largest, the amplitude by the invariant 2 A^2 sin omega_0 SUM phi^2 = T per quantum (`features/click.standing`'s rule over a spread profile, the root by the one search at the phase line's amplitude), A phi rounded to the integers at every Node in x-major order."""
    found = reading.levels[level]
    weights = coefficients if np.abs(coefficients).sum() > 0 else np.eye(found.profiles.shape[1])[0]
    pivot = weights[int(np.argmax(np.abs(weights)))]
    profile = np.real(found.profiles @ (weights / (pivot / abs(pivot))))
    profile = profile / np.abs(profile).max()  # 1 at its largest, the root's precision at the peak
    num, den = board.families[reading.index].pair
    scale = board.amplitude
    grains = [int(round(float(value) * scale)) for value in profile]
    norm = sum(grain * grain for grain in grains)
    sine_free = largest_below(den * den - num * num)
    square = division_forward(board.world.quantum_action * den * scale * scale, 2 * sine_free * norm, 0)
    amplitude = largest_below(int(square[0]))  # A at the profile's peak: 2 A^2 sin omega_0 SUM phi^2 = T
    return [int(v) for v in np.rint(amplitude * profile)]


def level_name(level: Level) -> str:
    """A level's name as the declaration's part, its rotation pair and the count of its degenerate modes, no letter of the spectroscopist's."""
    return f"level [{level.pair[0]}, {level.pair[1]}] x{level.profiles.shape[1]}"


def instrument_entry(
    board: Lattice,
    index: int,
    record: int,
    light: str,
    weight: int | None,
    lifetime: int | None,
    width: int | None,
    declared: tuple[tuple[int, int, int], ...] = (),
    whole: bool = False,
) -> dict[str, Any] | None:
    """The mode file's `instrument` of one bound body, the detector body's declaration in the world file's own form (loader/world.BODY_KEYS, loader/node_detector_declaration.READER_RECORD_KEYS): `nodes`, the standing region's Nodes at the file's coordinates (`standing_region`, the body's declared Nodes `declared` among them) with the record's share at each as the lay's weight; `parts`, the transition's two levels by name in energy order with the count 1 in the level the record stands in and 0 in the other (the upper where two levels carry share, the beating record the giver of (5), which emits from its upper part; the one level laid otherwise); `transitions`, the lower to the upper by the light family at the weight (the record's read weight of its holder where none is given) and the resonance [den cos(Omega_upper - Omega_lower), den], the cosine of the difference by the two pairs' cosines and sines over den, one rounding; `rates`, the upper to the lower at the lifetime giving to the light family, with the packet's width where given, none where no lifetime is given; `node_detector`, the empty object where a rate is declared and the transition's period as the window otherwise; None for a record with no transition."""
    reading = reading_of(board, index, record)
    if reading is None:
        return None
    fractions, _coefficients = shares_of(board, reading)
    region, shares = standing_region(board, index, record, declared, whole)
    low, high = reading.levels[reading.lower], reading.levels[reading.upper]
    den = low.pair[1]
    cosine = int(
        paces.rounded(high.pair[0] * low.pair[0] + high.sine * low.sine, den)
    )  # den cos(Omega_u - Omega_l)
    second = sorted(fractions, reverse=True)[1]  # the second level's share: a beating record
    stands = reading.upper if int(round(second * reading.unit)) > 0 else reading.lower
    names = [level_name(low), level_name(high)]
    parts = [
        {"part": 0, "name": names[0], "count": 1 if stands == reading.lower else 0},
        {"part": 1, "name": names[1], "count": 1 if stands == reading.upper else 0},
    ]
    coupling = weight_of(reading.holder, board.families[index]) if weight is None else weight
    transitions = [
        {
            "from": names[0],
            "to": names[1],
            "drive": light,
            "weight": coupling,
            "resonance": [cosine, den],
        }
    ]
    rates: list[dict[str, Any]] = []
    if lifetime is not None:
        rate: dict[str, Any] = {
            "from": names[1],
            "to": names[0],
            "lifetime": lifetime,
            "gives_to": light,
        }
        if width is not None:
            rate["width"] = width
        rates.append(rate)
    nodes = [
        {"node": [int(v) for v in at], "weight": int(shares[tuple(at)])} for at in np.argwhere(region)
    ]
    return {
        "nodes": nodes,
        "parts": parts,
        "transitions": transitions,
        "rates": rates,
        "node_detector": {} if lifetime is not None else {"window": reading.period},
    }


def readings_of(board: Lattice, index: int, record: int) -> dict[str, Any] | None:
    """The tool's own readings of a bound record beside its declaration: its levels as pairs [den cos Omega, den] with their sines and degenerate counts, the two of its transition, its unit W_rec and its period, its shares at the lay in parts of the unit; None for a record with no transition."""
    reading = reading_of(board, index, record)
    if reading is None:
        return None
    fractions, _coefficients = shares_of(board, reading)
    return {
        "levels": [[level.pair[0], level.pair[1]] for level in reading.levels],
        "sines": [level.sine for level in reading.levels],
        "modes": [int(level.profiles.shape[1]) for level in reading.levels],
        "transition": [reading.lower, reading.upper],
        "unit": reading.unit,
        "period": reading.period,
        "shares": [int(round(f * reading.unit)) for f in fractions],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--input", type=Path, required=True, help="the world file; its mode file beside it is rewritten"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="the repository root the world's universe path is read against (the checkout's by default)",
    )
    parser.add_argument(
        "--light", required=True, help="the family of light the body takes its quantum from and gives to"
    )
    parser.add_argument(
        "--lifetime",
        type=int,
        default=None,
        help="the rate's declared constant and the lay's span (The click writes on the lattice (5)); none, the constant 0",
    )
    parser.add_argument(
        "--width", type=int, default=None, help="the emitted packet's Nodes across on the open board"
    )
    parser.add_argument(
        "--weight",
        type=int,
        default=None,
        help="the transition's coupling; the record's read weight of its holder where none is given",
    )
    parser.add_argument(
        "--region",
        default="half",
        choices=("half", "whole"),
        help="the standing region: the Nodes of the largest shares holding half the record's share, or its whole support",
    )
    args = parser.parse_args(argv)
    path: Path = args.input
    if args.root is not None:
        world_files.REPOSITORY_ROOT = args.root
    world = load_world(path)
    board = Lattice(world, None)
    mode_path = path.with_suffix(".mode.json")
    mode = json.loads(mode_path.read_text(encoding="utf-8"))
    entries = mode["bodies"]
    summary: dict[str, Any] = {"label": LABEL, "world": path.name, "bodies": {}}
    placed = 0
    for number, (record, row) in enumerate(board.laid_rows()):
        if not isinstance(row, BodyRow) or (row.detector is not None and not row.region):
            continue  # a body laid in its parts by the engine has no mode entry; a declared bound body is typed again
        entry, placed = entries[placed], placed + 1
        entry.pop("frame", None)  # the engine's frame of the removed taker, read by nothing
        family = board.families[row.family]
        if not turns(board.families, row.family) or family.pair[0] == 0:
            entry.pop(INSTRUMENT, None)
            summary["bodies"][number] = (
                "no instrument: the record is not turned or stands at the frozen pair"
            )
            continue
        found = instrument_entry(
            board,
            row.family,
            record,
            args.light,
            args.weight,
            args.lifetime,
            args.width,
            row.nodes,
            args.region == "whole",
        )
        if found is None:
            entry.pop(INSTRUMENT, None)
            summary["bodies"][number] = "no instrument: no transition, every level at one rotation"
            continue
        entry[INSTRUMENT] = found
        summary["bodies"][number] = {
            "declaration": {
                key: found[key] for key in ("parts", "transitions", "rates", "node_detector")
            },
            "region": len(found["nodes"]),
            "readings": readings_of(board, row.family, record),
        }
    mode_path.write_text(json.dumps(mode) + "\n", encoding="utf-8")
    load_world(path)  # the loader admits the mode file beside the world
    summary["mode"] = str(mode_path)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
