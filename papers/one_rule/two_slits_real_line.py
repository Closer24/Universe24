"""The two slits' row by the law's real line, from the world's files and by no run of the engine.

The paper's Sections 9.1 and 9.2 and its Table 2 cite the numbers printed here (docs/ALGEBRA.md,
the rows against nature, row (g); the click formulas, item 1). The script reads the two slits'
world as the engine's loader reads it (examples/events/two_slits/two_slits.json with its mode file,
the universe file it names and the blind expectation file beside it) and steps Rule3's line for
light at the vacuum's paces in real arithmetic (floating point: no integer division and no
remainder) on the same declared world: the flat board with its third axis folded (the Node itself
through both z Ports), the wall's Nodes beyond the board read as 0, the y faces open (read as 0),
the x faces receding (zeros without end, by a padding no signal crosses within the run), the
emitter the law's packet lay now_i = b e_i cos(k x_i) under the raised-cosine envelope e_i and
before_i the exact before level, the packet now + i quadrature advanced mode by mode by its own band
phase (the generator's act at the frozen commit, tools/pixel_mode.advanced_real_part), and the screen's twelve regions read exactly as the engine
reports them: the net current through each region's front boundary Ports, F = num (now_i before_j
- before_i now_j) into the region's Node i from its neighbour j on the declared board outside the
instrument, at the pair the step starts from (the engine's click at the interval t reports the state
after t - 1 steps), summed over the window of the expectation file and divided by the count wall
W_c. Every number is printed with its definition: the total N over the window, the twelve regions'
quanta and shares, the visibility and the wings, the arrival of the screen's inflow (its peak, its
centroid and its half-maximum span, in the engine's labels and in the physical ones), the same
with the source face open as the meeting round's world had it, the same world scaled toward the
continuum (every extent and the run times s, the wave number over s, the result over s), the
Huygens blind row of the expectation file beside, the separation of the central maximum from the
first minima in the draw's scatter sqrt(N p (1 - p)), the arrival's spread sigma_t from the band's
group velocity and curvature with the lay's sigma_x and sigma_k, and the integer budget's bound on
the run's N (the walk sigma sqrt(n) of the integer step against the amplitude).

    PYTHONPATH=src python paper/two_slits_real_line.py [--scales 2 4 8] \\
        > paper/two_slits_real_line.txt

Needs numpy and the engine's loader. No number of the law is typed here: every coefficient is
Rule3's at the vacuum's paces (event_universe.core.rule3.coefficients), the count wall the
loader's, and every length, wave number, amplitude, region and window the files'. Nothing is read
from a run.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.core.rule3 import coefficients
from event_universe.loader.derived import count_wall
from event_universe.loader.world import World
from event_universe.world_files import load_world

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))

from click_counts import apportioned, extrema, nearest  # noqa: E402  # the NodeDetector's own rules
from pixel_mode import advanced_real_part  # noqa: E402  # the generator's exact before level

Node = tuple[int, int]
# the in-plane Ports of the flat board, (axis, side); the folded z axis returns the Node itself
PORTS: tuple[tuple[int, int], ...] = ((0, 1), (0, -1), (1, 1), (1, -1))


@dataclass(frozen=True)
class Packet:
    """The packet as the file lays it along x: its wave number k per Link, its amplitude b and the
    raised cosine's flat top and half-width on each axis of the plane."""

    wave_number: float
    amplitude: float
    top_x: tuple[int, int]
    edge_x: int
    top_y: tuple[int, int]
    edge_y: int


@dataclass(frozen=True)
class Board:
    """The flat board the real line steps: its declared extent, the Nodes beyond it (the wall), the
    declared regions with their Nodes, the names of the screen's regions in the expectation's order,
    the packet and the intervals."""

    length: int
    height: int
    beyond: frozenset[Node]
    regions: dict[str, tuple[Node, ...]]
    screen: tuple[str, ...]
    packet: Packet
    intervals: int

    def scaled(self, scale: int) -> Board:
        """The same world every extent times `scale` (a cell of one Node becomes scale x scale
        Nodes, so the regions, the gaps and the packet's cross-section keep their size in Links),
        the wall one Node thick at its scaled column and the packet's one-column top one column, so
        that the wavelength, the gaps, L and d grow alike and the Fresnel number stays."""
        wall_columns = {x for x, _y in self.beyond}
        gap_rows = {
            y for y in range(self.height) if any((x, y) not in self.beyond for x in wall_columns)
        }
        beyond = frozenset(
            (x * scale, y)
            for x in wall_columns
            for y in range(self.height * scale)
            if y // scale not in gap_rows
        )
        regions = {
            name: tuple((x, y) for nx, ny in nodes for x in cell(nx, scale) for y in cell(ny, scale))
            for name, nodes in self.regions.items()
        }
        p = self.packet
        top_x = (
            (p.top_x[0] * scale, p.top_x[0] * scale)
            if p.top_x[0] == p.top_x[1]
            else (
                p.top_x[0] * scale,
                (p.top_x[1] + 1) * scale - 1,
            )
        )
        packet = Packet(
            p.wave_number / scale,
            p.amplitude,
            top_x,
            p.edge_x * scale,
            (p.top_y[0] * scale, (p.top_y[1] + 1) * scale - 1),
            p.edge_y * scale,
        )
        return Board(
            self.length * scale,
            self.height * scale,
            beyond,
            regions,
            self.screen,
            packet,
            self.intervals * scale,
        )


def cell(at: int, scale: int) -> range:
    """The coordinates a Node at `at` covers once every extent is `scale` times as long."""
    return range(at * scale, (at + 1) * scale)


@dataclass(frozen=True)
class Line:
    """Rule3's line for the family at the vacuum's paces in real arithmetic: the read coefficient
    over the wall R / w on every axis, the self coefficient over the wall S / w, and the weight num
    of the current F = num (now_i before_j - before_i now_j)."""

    read: float
    self_over_wall: float
    weight: int
    pair: tuple[int, int]
    rule: tuple[
        tuple[Any, ...], Any, Any
    ]  # Rule3's integers (the six reads, S, w) as the lay tool takes them

    def cos_omega(self, *wave_numbers: float) -> float:
        """The band: a plane wave at the wave numbers k_a obeys 2 w cos omega = 2 SUM_a R_a cos k_a
        + S, with the axes not named at k = 0."""
        axes = list(wave_numbers) + [0.0] * (3 - len(wave_numbers))
        return self.read * sum(math.cos(k) for k in axes) + self.self_over_wall / 2

    def omega(self, k: float) -> float:
        """The rotation per interval along an axis at the wave number k."""
        return math.acos(self.cos_omega(k))

    def group_velocity(self, k: float) -> float:
        """d omega / dk along an axis, (R / w) sin k / sin omega, in Links per interval."""
        return self.read * math.sin(k) / math.sin(self.omega(k))

    def curvature(self, k: float) -> float:
        """d^2 omega / dk^2 along an axis, the band's curvature, from the derivative of the group
        velocity: (R / w) (cos k sin omega - sin k cos omega omega') / sin^2 omega."""
        omega, v = self.omega(k), self.group_velocity(k)
        return (
            self.read
            * (math.cos(k) * math.sin(omega) - math.sin(k) * math.cos(omega) * v)
            / math.sin(omega) ** 2
        )

    def light_speed(self) -> float:
        """Light's speed at long wavelength, the slope of omega at k = 0: sqrt(R / w) Links per
        interval, since 1 - cos omega = (R / w) (1 - cos k) there."""
        return math.sqrt(self.read)


def line_of(world: World, family: int) -> Line:
    """Rule3's coefficients for the family at the vacuum's paces (every content 0), as the engine
    derives them, over the wall."""
    num, den = world.families[family].pair
    reads, self_coefficient, wall = coefficients(
        num, den, world.node_clock, world.node_clock, world.node_clock
    )
    if len(set(reads)) != 1:
        raise ValueError(f"the vacuum's reads differ by axis: {reads}")
    return Line(
        reads[0] / wall, self_coefficient / wall, num, (num, den), (reads, self_coefficient, wall)
    )


def board_of(world: World, screen: list[str]) -> Board:
    """The flat board from the loaded world: refused by name where the world is not the two slits'
    kind of world (a flat lattice with z folded, one packet along x with no phase and no transverse
    wave, regions with declared Nodes)."""
    if world.shape[2] != 1 or not world.periodic[2] or world.periodic[0] or world.periodic[1]:
        raise ValueError(
            f"the board is {world.shape} with the axes periodic {world.periodic}; the real line steps a flat board, z folded, x and y open"
        )
    if len(world.packets) != 1:
        raise ValueError(f"the world lays {len(world.packets)} packets; the real line lays one")
    packet = world.packets[0]
    if packet.along != 0 or packet.phase != (0, 1) or any(t != (0, 1) for t in packet.transverse):
        raise ValueError(
            "the packet is not a plain wave along x: its phase or a transverse wave is declared"
        )
    turns, halves = packet.wave
    packet = Packet(
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
    missing = [name for name in screen if name not in regions]
    if missing:
        raise ValueError(
            f"the expectation names the regions {missing}, which the world does not declare"
        )
    return Board(
        world.shape[0],
        world.shape[1],
        frozenset((int(x), int(y)) for x, y, _z in world.beyond),
        regions,
        tuple(screen),
        packet,
        world.intervals,
    )


def raised_cosine(extent: int, top: tuple[int, int], edge: int) -> np.ndarray:
    """The envelope along one axis at every coordinate: 1 over the flat top [first, last],
    (1 + cos(pi j / edge)) / 2 at j Nodes beyond either end up to the half-width `edge`, 0 further
    (ALGEBRA.md, the generator (h))."""
    at = np.arange(extent)
    away = np.maximum(np.maximum(top[0] - at, at - top[1]), 0)
    taper = (1 + np.cos(np.pi * np.minimum(away, max(edge, 1)) / max(edge, 1))) / 2
    return np.where(away == 0, 1.0, np.where(away <= edge, taper, 0.0))


def law_lay(board: Board, line: Line) -> tuple[np.ndarray, np.ndarray]:
    """The packet lay in real arithmetic over the declared lattice, the law's (h) with the generator's exact
    before level (the law's line (c)): now_i = b e_i cos(k x_i), and before_i the real part of the packet
    b e_i (cos k x_i + i sin k x_i) advanced mode by mode by its own band phase omega(q) over the board's
    transform (`tools/pixel_mode.advanced_real_part`, the generator's own function), the plane record's
    level one interval earlier; e_i the product of the two axes' raised cosines; 0 at every Node beyond
    the lattice. The packet lay carries no uniform mode: the sums over the lattice of
    the levels now and of the levels before are each 0, the uniform component taken out of each level at
    the lay by the division act (the level's sum divided among the packet's Nodes in proportion to the
    envelope), here in real arithmetic and with no remainder."""
    p = board.packet
    x = np.arange(board.length)[:, None].astype(float)
    envelope = (
        raised_cosine(board.length, p.top_x, p.edge_x)[:, None]
        * raised_cosine(board.height, p.top_y, p.edge_y)[None, :]
    )
    now = p.amplitude * envelope * np.cos(p.wave_number * x)
    quadrature = p.amplitude * envelope * np.sin(p.wave_number * x)
    for x_wall, y_wall in board.beyond:
        now[x_wall, y_wall] = quadrature[x_wall, y_wall] = envelope[x_wall, y_wall] = 0.0
    # the exact before level, the generator's own act at the frozen commit (the law's line (c)): the packet
    # a + i s over the board's transform, every mode advanced by its own band phase omega(q) at the family's
    # pair (R370), the real part
    before = advanced_real_part(now[:, :, None], quadrature[:, :, None], line.rule)[:, :, 0]
    weight = envelope / envelope.sum()
    now -= weight * now.sum()
    before -= weight * before.sum()
    return now, before


def lay_count(now: np.ndarray, before: np.ndarray, line: Line, clock: int, wall: float) -> float:
    """The lay's count in quanta: the record's share summed over the lattice, Eq. (13) of the paper at the
    vacuum's paces (every pace the clock), e_i = [w (now_i^2 + before_i^2) - now_i (S before_i + sum_j R_ij
    before_j)] / (2 clock^2) per Node with the folded z axis reading the Node itself through both z Ports, the
    sum over W_c (the generator's count is this sum rounded at the lay)."""
    reads, self_coefficient, rule_wall = line.rule
    neighbours = 2 * before
    neighbours[1:] += before[:-1]
    neighbours[:-1] += before[1:]
    neighbours[:, 1:] += before[:, :-1]
    neighbours[:, :-1] += before[:, 1:]
    share = (
        rule_wall * (now**2 + before**2) - now * (self_coefficient * before + reads[0] * neighbours)
    ) / (2 * clock**2)
    return float(share.sum()) / wall


def mode_lay(world: World, board: Board) -> tuple[np.ndarray, np.ndarray]:
    """The generator's integer lay from the mode file, the levels the engine's run starts from, as
    real numbers over the declared board (the flat x-major index of the file unfolded)."""
    found = []
    for pairs in (world.packets[0].now, world.packets[0].before):
        levels = np.zeros((board.length, board.height))
        for flat, level in pairs:
            levels[flat // board.height, flat % board.height] = float(level)
        found.append(levels)
    return found[0], found[1]


def fronts(board: Board, offset: int) -> dict[str, tuple[np.ndarray, ...]]:
    """Per declared region, the front boundary Ports as index arrays (i_x, i_y, j_x, j_y) in the
    padded board's coordinates: a Port of a Node i of the region leading in from a Node j of the
    declared board outside the instrument (the union of the declared regions); a Port between two
    regions, toward a receding face's layers or beyond a face is no front (reports.front)."""
    instrument = {node for nodes in board.regions.values() for node in nodes}
    found = {}
    for name, nodes in board.regions.items():
        pairs = []
        for x, y in nodes:
            for axis, side in PORTS:
                jx, jy = (x + side, y) if axis == 0 else (x, y + side)
                if 0 <= jx < board.length and 0 <= jy < board.height and (jx, jy) not in instrument:
                    pairs.append((x + offset, y, jx + offset, jy))
        columns = tuple(np.array(column, dtype=int) for column in zip(*pairs, strict=True))
        found[name] = columns
    return found


def real_line(
    board: Board, line: Line, now: np.ndarray, before: np.ndarray, source_open: bool
) -> dict[str, np.ndarray]:
    """The law's line stepped `intervals` intervals; per declared region the net front inflow in the
    current's units at the pair after t steps, for t from 0 through intervals (the engine's click at the
    interval t reports the pair after t - 1 steps). The x faces recede: the lattice is padded with zeros
    farther than a signal travels in the run (one Link per interval), so nothing returns; with
    `source_open` the low x face is the open face instead, read as 0 (the meeting round's world)."""
    padding = board.intervals + 1
    low = 0 if source_open else padding
    shape = (low + board.length + padding, board.height)
    a_now, a_before = np.zeros(shape), np.zeros(shape)
    a_now[low : low + board.length], a_before[low : low + board.length] = now, before
    wall = np.zeros(shape, dtype=bool)
    for x, y in board.beyond:
        wall[low + x, y] = True
    front = fronts(board, low)
    inflow = {name: np.zeros(board.intervals + 1) for name in board.regions}
    for t in range(board.intervals + 1):
        for name, (ix, iy, jx, jy) in front.items():
            current = line.weight * (a_now[ix, iy] * a_before[jx, jy] - a_before[ix, iy] * a_now[jx, jy])
            inflow[name][t] = current.sum()
        if t == board.intervals:
            break
        arrivals = 2 * a_now  # the folded z axis: the Node itself through both z Ports
        arrivals[1:] += a_now[:-1]
        arrivals[:-1] += a_now[1:]
        arrivals[:, 1:] += a_now[:, :-1]
        arrivals[:, :-1] += a_now[:, 1:]
        a_next = line.read * arrivals + line.self_over_wall * a_now - a_before
        a_next[wall] = 0.0
        a_before, a_now = a_now, a_next
    return inflow


@dataclass(frozen=True)
class Reading:
    """What the screen's regions saw over a window, in quanta: per region, the arrival profile per
    interval (the regions summed) with its labels, and the labels' name."""

    regions: list[float]
    profile: dict[int, float]
    labels: str


def read_screen(
    inflow: dict[str, np.ndarray],
    screen: tuple[str, ...],
    wall: float,
    window: tuple[int, int],
    shift: int,
) -> Reading:
    """The screen read over the window [first, last] of labels, the label t naming the pair after
    t - shift steps (the engine's labels at shift 1, the physical ones at 0), each region's inflow
    summed over the window and divided by W_c, and the regions' sum per interval."""
    steps = [t - shift for t in range(window[0], window[1] + 1)]
    steps = [s for s in steps if 0 <= s < len(next(iter(inflow.values())))]
    regions = [float(sum(inflow[name][s] for s in steps)) / wall for name in screen]
    profile = {s + shift: float(sum(inflow[name][s] for name in screen)) / wall for s in steps}
    return Reading(regions, profile, "the engine's labels" if shift else "the physical labels")


def arrival(
    profile: dict[int, float], scale: float = 1.0
) -> tuple[float, float, tuple[float, float], float]:
    """The arrival of the screen's inflow over every interval of the window, the negative ones
    included: the peak (the first label at the largest inflow), the centroid, the half-maximum span
    (the first and the last label at or above half the peak) and the rms duration about the
    centroid, every label over `scale`."""
    largest = max(profile.values())
    peak = min(t for t, v in profile.items() if v == largest)
    total = sum(profile.values())
    centroid = sum(t * v for t, v in profile.items()) / total
    spread = math.sqrt(max(sum((t - centroid) ** 2 * v for t, v in profile.items()) / total, 0.0))
    high = [t for t, v in profile.items() if 2 * v >= largest]
    return peak / scale, centroid / scale, (min(high) / scale, max(high) / scale), spread / scale


def visibility(row: list[float], central: int, minima: list[int]) -> float:
    """The visibility at the blind central maximum against the blind first minima, (most x their
    count - their sum) over (most x their count + their sum)."""
    most, low = row[central] * len(minima), sum(row[at] for at in minima)
    return (most - low) / (most + low)


def deviation(row: list[float], blind: list[float]) -> float:
    """The summed absolute deviation of a row from the blind row's shares over the total, SUM_g
    |n_g B - T b_g| / (T B), T the row's total and B the blind's."""
    total, whole = sum(row), sum(blind)
    return sum(abs(n * whole - total * b) for n, b in zip(row, blind, strict=True)) / (total * whole)


def separations(row: list[float], total: float, central: int, minima: list[int]) -> dict[str, float]:
    """The central maximum against the two first minima in the draw's scatter sqrt(N p (1 - p)) per
    region, p a region's share of the total N: the central's count less the minima's mean over the
    central's own scatter; the same over the scatter of that difference under the draw (the draw
    multinomial, the covariance of two regions -N p_i p_j); and each minimum's scatter."""
    p = [v / total for v in row]
    scatter = [math.sqrt(total * q * (1 - q)) for q in p]
    mean_low = sum(row[at] for at in minima) / len(minima)
    difference = row[central] - mean_low
    weights = {central: 1.0}
    for at in minima:
        weights[at] = -1.0 / len(minima)
    variance = sum(
        wi * wj * total * ((p[i] * (1 - p[i])) if i == j else -p[i] * p[j])
        for i, wi in weights.items()
        for j, wj in weights.items()
    )
    found = {
        "central count": row[central],
        "central scatter": scatter[central],
        "minima mean": mean_low,
        "over the central's scatter": difference / scatter[central],
        "over the difference's scatter": difference / math.sqrt(variance),
    }
    for at in minima:
        found[f"minimum at the region {at}"] = row[at]
        found[f"its scatter at the region {at}"] = scatter[at]
    return found


def lay_widths(board: Board) -> tuple[float, float, float]:
    """The lay's widths along x: sigma_x, the rms half-width of the lay's intensity e_i^2 about its
    centroid over the Nodes; sigma_k, the rms half-width of the lay's spectrum |E(k)|^2 over the
    zone, E(k) = SUM_i e_i exp(-i k x_i); and the packet's centre."""
    p = board.packet
    x = np.arange(board.length).astype(float)
    e = raised_cosine(board.length, p.top_x, p.edge_x)
    weight = e * e
    centre = float((x * weight).sum() / weight.sum())
    sigma_x = math.sqrt(float((((x - centre) ** 2) * weight).sum() / weight.sum()))
    k = np.linspace(-math.pi, math.pi, 40001)
    spectrum = np.abs(np.exp(-1j * np.outer(k, x)) @ e) ** 2
    sigma_k = math.sqrt(float((k * k * spectrum).sum() / spectrum.sum()))
    return sigma_x, sigma_k, centre


def row_text(row: list[float], places: int = 2) -> str:
    """A row of numbers to `places` decimals, comma separated."""
    return ", ".join(f"{v:.{places}f}" for v in row)


def extrema_text(row: list[float], first: int, last: int) -> str:
    """The row's maxima and minima within the pattern's range by the NodeDetector's one rule."""
    maxima, minima = extrema(row, first, last)
    return f"maxima at the regions {maxima}, minima at {minima}"


def report_reading(
    title: str,
    reading: Reading,
    expected: dict[str, Any],
    wall: float,
    tail: tuple[float, float],
) -> None:
    """One reading of the screen printed: N, the regions, the shares, the extrema, the visibility,
    the deviation from the blind, the wings and the rounded shares by the NodeDetector's rules
    at N rounded, and the arrival."""
    central, minima = int(expected["central"]), [int(at) for at in expected["minima"]]
    wings = [int(at) for at in expected["wings"]["regions"]]
    first, last = int(expected["pattern"][0]), int(expected["pattern"][1])
    blind = [float(v) for v in expected["counts"]]
    total = sum(reading.regions)
    print(f"\n{title}")
    print(f"  N = {total:.2f} quanta: the screen's net front inflow summed over the window, over W_c")
    print(f"  the regions' quanta, from the row 0 across y: {row_text(reading.regions)}")
    print(
        f"  the shares, each region's quanta over N: {row_text([v / total for v in reading.regions], 4)}"
    )
    print(
        f"  {extrema_text(reading.regions, first, last)} (the NodeDetector's rule within the pattern {[first, last]})"
    )
    print(
        f"  the visibility at the blind first minima's regions {minima} against the blind central maximum,"
        f" the region {central}: {visibility(reading.regions, central, minima):.4f}"
    )
    print(
        f"  the deviation from the blind shares, SUM |n_g B - T b_g| / (T B): {deviation(reading.regions, blind):.4f}"
    )
    print(f"  the wings, the regions {wings}: {row_text([reading.regions[at] for at in wings], 2)}")
    units = [int(round(v * wall)) for v in reading.regions]
    quanta = nearest(sum(units), int(wall))
    rounded = apportioned(quanta, units)
    print(
        f"  N to the nearest whole {quanta}, apportioned by the largest remainders (the rounded shares): {rounded}"
    )
    peak, centroid, span, spread = arrival(reading.profile)
    print(
        f"  the arrival in {reading.labels}: the peak at {peak:.0f}, the centroid {centroid:.2f}, the"
        f" half-maximum span {span[0]:.0f} to {span[1]:.0f}, the rms duration {spread:.2f} intervals"
    )
    print(
        f"  arrived before the window {tail[0]:.2f} quanta, after it {tail[1]:.2f} (the labels' whole run)"
    )


def whole_run(
    inflow: dict[str, np.ndarray], screen: tuple[str, ...], wall: float, shift: int
) -> dict[int, float]:
    """The screen's inflow per label over the whole run in the labels of `shift`."""
    steps = range(len(next(iter(inflow.values()))))
    return {s + shift: float(sum(inflow[name][s] for name in screen)) / wall for s in steps}


def outside(profile: dict[int, float], window: tuple[int, int]) -> tuple[float, float]:
    """What the profile holds before and after the window."""
    before = sum(v for t, v in profile.items() if t < window[0])
    after = sum(v for t, v in profile.items() if t > window[1])
    return before, after


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--world",
        type=Path,
        default=ROOT / "examples" / "events" / "two_slits" / "two_slits.json",
        help="the two slits' world file, its mode file beside it",
    )
    parser.add_argument(
        "--expectation",
        type=Path,
        default=ROOT / "examples" / "events" / "two_slits" / "expectation.json",
        help="the blind expectation file: the screen's regions, the window, the seed, the Huygens row",
    )
    parser.add_argument(
        "--scales", type=int, nargs="*", default=[2, 4, 8], help="the scales of the continuum's worlds"
    )
    args = parser.parse_args(argv)
    world = load_world(args.world)
    expected = json.loads(args.expectation.read_text(encoding="utf-8"))
    screen = [str(name) for name in expected["node_detector"]]
    window = (int(expected["window"][0]), int(expected["window"][1]))
    board = board_of(world, screen)
    family = world.packets[0].family
    line = line_of(world, family)
    wall = float(count_wall(world.families[family], world.quantum_action))
    p = board.packet
    k = p.wave_number
    omega = line.omega(k)

    print(
        "The two slits by the law's real line (docs/ALGEBRA.md row (g); the paper's Sections 9.1 and 9.2)"
    )
    print(
        f"the world {args.world.relative_to(ROOT)}, the expectation {args.expectation.relative_to(ROOT)}"
    )
    print(
        f"the family {world.families[family].name!r} with the pair {list(world.families[family].pair)},"
        f" Gamma = {world.node_clock}, T = {world.quantum_action}, W_c = {int(wall)} (the count wall, 3 den T)"
    )
    print(
        f"Rule3 at the vacuum's paces: R / w = {line.read:.10f} on every axis, S / w = {line.self_over_wall:.10f},"
        f" the current's weight num = {line.weight}"
    )
    print(
        f"the board {board.length} x {board.height} x 1 (z folded), x and y open, both x faces receding;"
        f" the wall {len(board.beyond)} Nodes beyond the board at the column"
        f" {sorted({x for x, _y in board.beyond})}, its gaps the rows"
        f" {[y for y in range(board.height) if (next(iter({x for x, _y in board.beyond})), y) not in board.beyond]}"
    )
    print(
        f"the packet: k = pi x {world.packets[0].wave[0]} / {world.packets[0].wave[1]} = {k:.6f} per Link"
        f" (lambda = {2 * math.pi / k:.1f} Links), b = {p.amplitude:.0f}, the top x {list(p.top_x)} with the"
        f" half-width {p.edge_x}, the top y {list(p.top_y)} with the half-width {p.edge_y}"
    )
    print(
        f"the band at k: cos omega = {math.cos(omega):.6f}, omega = {omega:.6f}, the period {2 * math.pi / omega:.2f}"
        f" intervals, the group velocity {line.group_velocity(k):.4f} Links per interval, light's speed at long"
        f" wavelength {line.light_speed():.4f}"
    )
    print(
        f"the screen: {len(screen)} regions of {len(board.regions[screen[0]])} Nodes each at the column"
        f" {sorted({x for x, _y in board.regions[screen[0]]})}, read over the window {list(window)} of"
        f" {board.intervals} intervals; the bare regions beside: {[n for n in board.regions if n not in screen]}"
    )

    now, before = law_lay(board, line)
    mode_now, mode_before = mode_lay(world, board)
    print(
        f"the lay against the mode file's integers: the largest difference of a level {np.abs(now - mode_now).max():.2f}"
        f" (now) and {np.abs(before - mode_before).max():.2f} (before); the lay stands on"
        f" {int((mode_now != 0).sum())} Nodes now and {int((mode_before != 0).sum())} before;"
        f" the generator's count of the lay {expected['laid']} quanta"
    )

    inflow = real_line(board, line, now, before, source_open=False)
    engine = read_screen(inflow, board.screen, wall, window, 1)
    whole = whole_run(inflow, board.screen, wall, 1)
    report_reading(
        f"1. The world as declared, both x faces receding, the window {list(window)} in the engine's labels"
        " (the click at the interval t reports the pair after t - 1 steps)",
        engine,
        expected,
        wall,
        outside(whole, window),
    )
    for name in board.regions:
        if name not in screen:
            seen = sum(inflow[name][t - 1] for t in range(window[0], window[1] + 1)) / wall
            print(
                f"  the bare region {name!r} beside the screen saw {seen:.2f} quanta net over the window"
            )
    meeting = (window[0], 120)
    windowed = read_screen(inflow, board.screen, wall, meeting, 1)
    print(
        f"  over the meeting round's window {list(meeting)} (history): N = {sum(windowed.regions):.2f}, the"
        f" regions {row_text(windowed.regions, 1)}, the wings"
        f" {row_text([windowed.regions[at] for at in expected['wings']['regions']], 2)}"
    )
    physical = read_screen(inflow, board.screen, wall, window, 0)
    peak, centroid, span, spread = arrival(physical.profile)
    print(
        f"  in the physical labels (the pair after t steps labelled t), the window {list(window)}: N ="
        f" {sum(physical.regions):.2f}, the arrival's peak at {peak:.0f}, the centroid {centroid:.2f}, the span"
        f" {span[0]:.0f} to {span[1]:.0f}, the rms duration {spread:.2f}"
    )
    whole_physical = whole_run(inflow, board.screen, wall, 0)
    peak, centroid, span, _spread = arrival(whole_physical)
    print(
        f"  over the whole run in the physical labels: N = {sum(whole_physical.values()):.2f}, the peak at"
        f" {peak:.0f}, the centroid {centroid:.2f}, the span {span[0]:.0f} to {span[1]:.0f}"
    )

    mode_inflow = real_line(board, line, mode_now, mode_before, source_open=False)
    from_mode = read_screen(mode_inflow, board.screen, wall, window, 1)
    print(
        f"  the same from the mode file's integer lay: N = {sum(from_mode.regions):.2f}, the regions"
        f" {row_text(from_mode.regions, 2)}"
    )

    open_inflow = real_line(board, line, now, before, source_open=True)
    open_engine = read_screen(open_inflow, board.screen, wall, window, 1)
    open_whole = whole_run(open_inflow, board.screen, wall, 1)
    report_reading(
        f"2. The meeting round's world, the source face open (read as 0, reflecting), the window {list(window)}"
        " in the engine's labels",
        open_engine,
        expected,
        wall,
        outside(open_whole, window),
    )
    open_mode = real_line(board, line, mode_now, mode_before, source_open=True)
    print(
        f"  the same from the mode file's integer lay: N = {sum(read_screen(open_mode, board.screen, wall, window, 1).regions):.2f}"
    )
    open_meeting = read_screen(open_inflow, board.screen, wall, meeting, 1)
    open_physical = read_screen(open_inflow, board.screen, wall, meeting, 0)
    print(
        f"  over the window {list(meeting)}: N = {sum(open_meeting.regions):.2f} in the engine's labels,"
        f" {sum(open_physical.regions):.2f} in the physical labels (the engine's [{meeting[0] + 1}, {meeting[1] + 1}]),"
        f" the regions in the physical labels {row_text(open_physical.regions, 1)}"
    )
    print(
        f"  the second pass inside the window, the open face's N less the receding face's:"
        f" {sum(open_engine.regions) - sum(engine.regions):.2f} over {list(window)},"
        f" {sum(open_meeting.regions) - sum(windowed.regions):.2f} over {list(meeting)}"
    )

    blind = [float(v) for v in expected["counts"]]
    central, minima = int(expected["central"]), [int(at) for at in expected["minima"]]
    first, last = int(expected["pattern"][0]), int(expected["pattern"][1])
    print(
        "\n3. The Huygens blind of the expectation file (the advisor's per-Node row summed per region)"
    )
    print(
        f"  the blind row {row_text(blind, 1)}, its sum {sum(blind):.1f} by the per-Node rounding, N's blind"
        f" {float(expected['quanta']):.1f}"
    )
    print(
        f"  {extrema_text(blind, first, last)}; the visibility at {minima} against {central}:"
        f" {visibility(blind, central, minima):.4f}"
    )
    print(
        f"  the real line's row against the blind: the deviation {deviation(engine.regions, blind):.4f}"
        f" of the total; N {sum(engine.regions):.2f} against {float(expected['quanta']):.0f},"
        f" {100 * (sum(engine.regions) / float(expected['quanta']) - 1):.1f} percent over"
    )

    print(
        "\n4. The central maximum against the two first minima in the draw's scatter sqrt(N p (1 - p))"
    )
    for title, row, total in (
        (
            f"the Huygens blind row at N = {float(expected['quanta']):.0f}",
            blind,
            float(expected["quanta"]),
        ),
        (
            f"the real line's row, both faces receding, N = {sum(engine.regions):.2f}",
            engine.regions,
            sum(engine.regions),
        ),
        (
            f"the real line's row, the source face open, N = {sum(open_engine.regions):.2f}",
            open_engine.regions,
            sum(open_engine.regions),
        ),
    ):
        found = separations(row, total, central, minima)
        over_central = found["over the central's scatter"]
        over_difference = found["over the difference's scatter"]
        print(
            f"  {title}: the central region {central} {found['central count']:.2f} with the scatter"
            f" {found['central scatter']:.2f}; the minima at {minima}"
            f" {row_text([found[f'minimum at the region {at}'] for at in minima], 2)} with the scatters"
            f" {row_text([found[f'its scatter at the region {at}'] for at in minima], 2)}; the central less the"
            f" minima's mean {found['minima mean']:.2f} is {over_central:.2f} of the"
            f" central's scatter and {over_difference:.2f} of the difference's own"
        )

    sigma_x, sigma_k, centre = lay_widths(board)
    screen_column = min(x for x, _y in board.regions[screen[0]])
    distance = screen_column - centre
    v_g, omega2 = line.group_velocity(k), line.curvature(k)
    flight = distance / v_g
    width_at_screen = math.sqrt(sigma_x**2 + (omega2 * flight * sigma_k) ** 2)
    print(
        "\n5. The arrival's spread (the paper's Table 2): sigma_t = sqrt(sigma_x^2 + (omega'' L sigma_k / v_g)^2) / v_g"
    )
    print(
        f"  sigma_x = {sigma_x:.4f} Links, the rms half-width of the lay's intensity e_i^2 along x about its"
        f" centroid {centre:.1f}; sigma_k = {sigma_k:.4f} per Link, the rms half-width of the lay's spectrum"
        f" |E(k)|^2; their product {sigma_x * sigma_k:.4f}"
    )
    print(
        f"  v_g = {v_g:.4f} Links per interval at k = {k:.4f}; omega'' = {omega2:.4f}, the band's curvature there;"
        f" L = {distance:.0f} Links from the packet's centre to the screen's column {screen_column};"
        f" the flight t = L / v_g = {flight:.2f} intervals"
    )
    print(
        f"  the packet's width at the screen sqrt(sigma_x^2 + (omega'' t sigma_k)^2) = {width_at_screen:.4f} Links;"
        f" sigma_t = {width_at_screen / v_g:.2f} intervals"
    )
    own_peak, _own_centroid, own_span, own_spread = arrival(physical.profile)
    print(
        f"  beside it the real line's own screen inflow in the physical labels over the window: the rms duration"
        f" {own_spread:.2f} intervals (every row's path and both gaps summed), the peak at {own_peak:.0f} against"
        f" the flight's {flight:.1f}, the half-maximum span {own_span[0]:.0f} to {own_span[1]:.0f}"
    )

    print(
        f"\n6. The continuum: the same world scaled by s (every extent times s, lambda = {2 * math.pi / k:.0f} s, the"
        f" wall and the screen one Node thick, the packet's top one column), both x faces receding, the run"
        f" {board.intervals} s intervals, read in the physical labels over the window [{window[0]} s, {window[1]} s]"
        f" and the labels over s"
    )
    wings = [int(at) for at in expected["wings"]["regions"]]
    print(
        f"  s = 1 (the lattice itself, the physical labels): N = {sum(physical.regions):.2f}, the wings"
        f" {row_text([physical.regions[at] for at in wings], 2)}, the peak at {arrival(physical.profile)[0]:.1f},"
        f" the centroid {arrival(physical.profile)[1]:.2f}, the span {arrival(physical.profile)[2][0]:.1f} to"
        f" {arrival(physical.profile)[2][1]:.1f}, v_g {v_g:.4f}"
    )
    laid_one = lay_count(now, before, line, world.node_clock, wall)
    print(
        f"  the lay at s = 1: {laid_one:.1f} quanta by Eq. (13) over W_c (the generator's integer count"
        f" {expected['laid']}); the transmission per laid quantum N / lay = {sum(physical.regions) / laid_one:.4f}"
    )
    transmission: dict[int, float] = {1: sum(physical.regions) / laid_one}
    found: dict[int, tuple[float, float, float, float, float]] = {}
    for scale in args.scales:
        big = board.scaled(scale)
        big_now, big_before = law_lay(big, line)
        laid = lay_count(big_now, big_before, line, world.node_clock, wall)
        big_inflow = real_line(big, line, big_now, big_before, source_open=False)
        big_window = (window[0] * scale, window[1] * scale)
        big_reading = read_screen(big_inflow, big.screen, wall, big_window, 0)
        peak, centroid, span, _spread = arrival(big_reading.profile, scale)
        total = sum(big_reading.regions)
        found[scale] = (
            total,
            big_reading.regions[wings[0]],
            big_reading.regions[wings[1]],
            peak,
            centroid,
        )
        print(
            f"  s = {scale}: N = {total:.2f}, the regions {row_text(big_reading.regions, 1)}, the wings"
            f" {row_text([big_reading.regions[at] for at in wings], 2)}, the peak at {peak:.1f}, the centroid"
            f" {centroid:.2f}, the span {span[0]:.1f} to {span[1]:.1f}, v_g {line.group_velocity(k / scale):.4f}"
        )
        transmission[scale] = total / laid
        print(
            f"    the lay at s = {scale}: {laid:.1f} quanta; the transmission per laid quantum N / lay ="
            f" {total / laid:.4f}"
        )
    if len(found) >= 2:
        s1, s2 = sorted(found)[-2:]
        names = (
            "N",
            f"the wing at the region {wings[0]}",
            f"the wing at the region {wings[1]}",
            "the peak",
            "the centroid",
        )
        limits = [
            (s2 * s2 * b - s1 * s1 * a) / (s2 * s2 - s1 * s1)
            for a, b in zip(found[s1], found[s2], strict=True)
        ]
        print(
            f"  the limit by the corrections falling as 1 / s^2, from s = {s1} and {s2}: "
            + ", ".join(f"{name} {value:.2f}" for name, value in zip(names, limits, strict=True))
        )
    if len(transmission) >= 3:
        scales = sorted(transmission)
        fits = {
            (s1, s2): (s2 * transmission[s2] - s1 * transmission[s1]) / (s2 - s1)
            for s1, s2 in zip(scales[1:-1], scales[2:], strict=True)
        }
        print(
            "  the transmission per laid quantum, the lattice's own number: "
            + ", ".join(f"{transmission[s]:.4f} at s = {s}" for s in scales)
            + "; its limit by a correction falling as 1 / s: "
            + ", ".join(f"{value:.4f} from s = {s1} and {s2}" for (s1, s2), value in fits.items())
            + f" (the lattice at s = 1 is {100 * (transmission[1] / list(fits.values())[-1] - 1):.0f} percent above it)"
        )
    print(
        f"  the lattice against the continuum at the largest scale, the physical labels: the peak"
        f" {arrival(physical.profile)[0]:.1f} against {found[max(found)][3]:.1f}, the centroid"
        f" {arrival(physical.profile)[1]:.2f} against {found[max(found)][4]:.2f}, the wings"
        f" {row_text([physical.regions[at] for at in wings], 1)} against"
        f" {found[max(found)][1]:.1f}, {found[max(found)][2]:.1f}"
    )

    carrier_cos = line.cos_omega(k)
    per_mode = math.sqrt(board.intervals / (12 * (1 + carrier_cos)))
    cells = 192
    midpoints = [-math.pi + (cell + 0.5) * 2 * math.pi / cells for cell in range(cells)]
    zone_mean = sum(1 / (1 + line.cos_omega(kx, ky)) for kx in midpoints for ky in midpoints) / cells**2
    per_node = math.sqrt(zone_mean * board.intervals / 12)
    total = sum(physical.regions)
    print(
        "\n7. The integer budget's walk on the run (the law's clause): the integer step differs from the line"
        " applied to the integer levels by below one level per Node per interval, n levels over the run the hard"
        " bound; under the model of independent uniform remainders the deviation walks per band mode as"
        " sqrt(n / (12 (1 + cos omega_k))), the plane's per-Node figure the zone's mean of 1 / (1 + cos omega)"
        " over (k_x, k_y) with k_z folded (the midpoint rule on 192^2 cells)"
    )
    print(
        f"  at the carrier cos omega = {carrier_cos:.4f}: {per_mode:.2f} levels per mode over n = {board.intervals};"
        f" the zone's mean {zone_mean:.3f}, {per_node:.2f} levels per Node; against b = {p.amplitude:.0f}:"
        f" {200 * per_mode / p.amplitude:.2f} to {200 * per_node / p.amplitude:.2f} percent of the share,"
        f" {total * 2 * per_mode / p.amplitude:.2f} to {total * 2 * per_node / p.amplitude:.2f} units of"
        f" N = {total:.2f} (the physical labels); the run's integer N stands within this walk of the line's or"
        " the difference is named"
    )


if __name__ == "__main__":
    main()
