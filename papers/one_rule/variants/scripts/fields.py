"""The two slits' fields by the law's real line (docs/ALGEBRA.md, the rows against nature (g); the paper's
script papers/one_rule/two_slits_real_line.py imported for its line and its regions): the shipped world
examples/events/two_slits/two_slits.json stepped in real arithmetic from its mode file's integer lay with
both gaps open, with the lower gap alone open and with the upper gap alone open, every interval's levels
kept on the declared board, with the conserved form's current per Link and the share per Node as the law
books them at the vacuum's paces. No number of the law is typed here; every coefficient is Rule3's, every
length the files'. Imported by the scripts beside it; run from the repository root with PYTHONPATH=src."""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # papers/one_rule/variants/scripts: the repository root three folders up
for folder in ("src", "tools", "papers/one_rule"):
    sys.path.insert(0, str(ROOT / folder))

import two_slits_real_line as tsl  # noqa: E402  # the law's own script, the two slits by the real line

from event_universe import world_files  # noqa: E402
from event_universe.loader.derived import count_wall  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402

world_files.REPOSITORY_ROOT = ROOT
WORLD = ROOT / "examples" / "events" / "two_slits" / "two_slits.json"
EXPECTATION = ROOT / "examples" / "events" / "two_slits" / "expectation.json"
LOWER, UPPER = (17, 19), (29, 31)  # the two gaps' rows, the design's


@dataclass(frozen=True)
class Fields:
    """The levels per interval on the declared board: now[t], before[t] of shape (length, height), t = 0
    the lay, t = 1 after one step, ... (the engine's click at the interval t reports the pair after t - 1
    steps)."""

    now: np.ndarray  # (intervals + 1, length, height)
    before: np.ndarray
    line: tsl.Line
    board: tsl.Board


def board_of(world, screen: list[str]) -> tsl.Board:  # type: ignore[no-untyped-def]
    """tsl.board_of as the loader names a packet's fields at this head (no `phase` on PacketRow; the
    shipped packet is the plain wave along x the real line lays): the flat board, the wall's Nodes beyond
    it, the declared regions with their Nodes, the screen's names in the expectation's order, the packet
    and the intervals."""
    packet = world.packets[0]
    turns, halves = packet.wave
    found = tsl.Packet(
        math.pi * turns / halves,
        float(packet.amplitude),
        (int(packet.top[0][0]), int(packet.top[0][1])),
        int(packet.edge[0]),
        (int(packet.top[1][0]), int(packet.top[1][1])),
        int(packet.edge[1]),
    )
    regions = {
        d.name: tuple((int(x), int(y)) for x, y, _z in d.positions)
        for d in world.node_detectors
        if d.declared
    }
    return tsl.Board(
        world.shape[0],
        world.shape[1],
        frozenset((int(x), int(y)) for x, y, _z in world.beyond),
        regions,
        tuple(screen),
        found,
        world.intervals,
    )


def loaded():  # type: ignore[no-untyped-def]
    """The shipped world, its blind expectation, the flat board, the line and the count wall W_c."""
    world = load_world(WORLD)
    expected = json.loads(EXPECTATION.read_text(encoding="utf-8"))
    screen = [str(name) for name in expected["node_detector"]]
    board = board_of(world, screen)
    family = world.packets[0].family
    line = tsl.line_of(world, family)
    wall = float(count_wall(world.families[family], world.quantum_action))
    return world, expected, board, line, wall


def closed(board: tsl.Board, gap_rows: tuple[int, int]) -> tsl.Board:
    """The board with the gap at `gap_rows` closed: its Nodes added to the wall (the wall's own face rule)."""
    wall_x = next(iter({x for x, _y in board.beyond}))
    beyond = set(board.beyond) | {(wall_x, y) for y in range(gap_rows[0], gap_rows[1] + 1)}
    return tsl.Board(
        board.length,
        board.height,
        frozenset(beyond),
        board.regions,
        board.screen,
        board.packet,
        board.intervals,
    )


def stepped(
    board: tsl.Board, line: tsl.Line, now0: np.ndarray, before0: np.ndarray, intervals: int
) -> Fields:
    """The law's line stepped on the declared board with both x faces receding (zeros without end, by a
    padding no signal crosses within the run), every interval's levels kept on the declared board's Nodes
    (tsl.real_line's step, the fields kept)."""
    padding = intervals + 1
    low = padding
    shape = (low + board.length + padding, board.height)
    a_now, a_before = np.zeros(shape), np.zeros(shape)
    a_now[low : low + board.length], a_before[low : low + board.length] = now0, before0
    wall = np.zeros(shape, dtype=bool)
    for x, y in board.beyond:
        wall[low + x, y] = True
    nows, befores = [], []
    for t in range(intervals + 1):
        nows.append(a_now[low : low + board.length].copy())
        befores.append(a_before[low : low + board.length].copy())
        if t == intervals:
            break
        arrivals = 2 * a_now  # the folded z axis: the Node itself through both z Ports
        arrivals[1:] += a_now[:-1]
        arrivals[:-1] += a_now[1:]
        arrivals[:, 1:] += a_now[:, :-1]
        arrivals[:, :-1] += a_now[:, 1:]
        a_next = line.read * arrivals + line.self_over_wall * a_now - a_before
        a_next[wall] = 0.0
        a_before, a_now = a_now, a_next
    return Fields(np.array(nows), np.array(befores), line, board)


def three_fields(intervals: int | None = None):  # type: ignore[no-untyped-def]
    """The fields with both gaps open, with the lower gap alone and with the upper gap alone, from the mode
    file's integer lay (the generator's exact before level), as the paper's script also reports it; the
    script's own law_lay calls the generator with a signature that moved at this head and is not used."""
    world, expected, board, line, wall = loaded()
    intervals = board.intervals if intervals is None else intervals
    now0, before0 = tsl.mode_lay(world, board)
    both = stepped(board, line, now0, before0, intervals)
    lower = stepped(closed(board, UPPER), line, now0, before0, intervals)  # the lower gap alone open
    upper = stepped(closed(board, LOWER), line, now0, before0, intervals)  # the upper gap alone open
    return world, expected, board, line, wall, both, lower, upper


def link_currents(line: tsl.Line, now: np.ndarray, before: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The conserved form's current along +x and +y per Link at the vacuum's paces, F = num (now_j before_i
    - before_j now_i) for the Link from i to j = i + a (the flow from i to j, positive toward +a): fx of
    shape (length - 1, height), fy of shape (length, height - 1)."""
    fx = line.weight * (now[1:, :] * before[:-1, :] - before[1:, :] * now[:-1, :])
    fy = line.weight * (now[:, 1:] * before[:, :-1] - before[:, 1:] * now[:, :-1])
    return fx, fy


def share(line: tsl.Line, clock: int, now: np.ndarray, before: np.ndarray) -> np.ndarray:
    """The share per Node at the vacuum's paces in the current's units (row 14 of The conventions and the
    units; tsl.lay_count's form): [w (now^2 + before^2) - now (S before + R SUM_6 before)] / (2 Gamma^2),
    the folded z axis reading the Node itself through both z Ports, the faces beyond the board reading 0."""
    reads, self_coefficient, rule_wall = line.rule
    neighbours = 2 * before
    neighbours[1:] += before[:-1]
    neighbours[:-1] += before[1:]
    neighbours[:, 1:] += before[:, :-1]
    neighbours[:, :-1] += before[:, 1:]
    return (
        rule_wall * (now**2 + before**2) - now * (self_coefficient * before + reads[0] * neighbours)
    ) / (2 * clock**2)


def region_inflow(board: tsl.Board, line: tsl.Line, fields: Fields, name: str) -> np.ndarray:
    """A declared region's net front inflow per interval (tsl.fronts: the Ports of the region's Nodes
    leading in from the declared board outside the instrument), in the current's units, at the pair after
    t steps."""
    (ix, iy, jx, jy) = tsl.fronts(board, 0)[name]
    found = np.zeros(fields.now.shape[0])
    for t in range(fields.now.shape[0]):
        n, b = fields.now[t], fields.before[t]
        found[t] = (line.weight * (n[ix, iy] * b[jx, jy] - b[ix, iy] * n[jx, jy])).sum()
    return found


def region_cross_inflow(board: tsl.Board, line: tsl.Line, a: Fields, b: Fields, name: str) -> np.ndarray:
    """The symmetrised cross inflow of two fields through a region's front, per interval: F[a, b] with
    F[a + b] = F[a] + F[b] + 2 F[a, b] (the current is bilinear in the levels)."""
    (ix, iy, jx, jy) = tsl.fronts(board, 0)[name]
    found = np.zeros(a.now.shape[0])
    for t in range(a.now.shape[0]):
        na, ba, nb, bb = a.now[t], a.before[t], b.now[t], b.before[t]
        found[t] = (
            0.5
            * line.weight
            * (
                na[ix, iy] * bb[jx, jy]
                - ba[ix, iy] * nb[jx, jy]
                + nb[ix, iy] * ba[jx, jy]
                - bb[ix, iy] * na[jx, jy]
            )
        ).sum()
    return found


def windowed(profile: np.ndarray, window: tuple[int, int]) -> float:
    """The sum over the window [first, last] in the engine's labels (the label t the pair after t - 1
    steps)."""
    return float(
        sum(profile[t - 1] for t in range(window[0], window[1] + 1) if 0 <= t - 1 < len(profile))
    )
