"""C. The average trajectories as the streamlines of the conserved form's own current (README.md, section
C; docs/ALGEBRA.md, The click writes on the lattice (2): the current the credit books, num (now_i before_j
- before_i now_j) per Link) of the shipped two slits' record, a lattice reading and no click: the law's
real line stepped on the shipped world from the mode file's lay (fields.py), the Link currents and the Node
shares summed over the whole run, the velocity field v = J / rho on the Nodes, the streamlines integrated
from the gaps to the screen at equal flux, their crossings of the midline counted and their arrival rows
binned against the screen's row; a PNG beside the README. With --engine the same from the engine's integer
board (the shipped world stepped with no draw, the currents Lattice.currents and the shares
Lattice.share_of), the lattice reading proper.

    PYTHONPATH=src python papers/one_rule/variants/scripts/c_streamlines.py [--engine]
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
import zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import fields  # noqa: E402

OUT = HERE.parent / "out"
PICTURES = HERE.parent
SCALE = 10  # pixels per Node in the pictures
PER_GAP = 22  # streamlines per gap, seeded at equal flux
STEP = 0.1  # the integration's step along the unit tangent, in Nodes
# the pictures' colours on the dark ground (the site shows one colour scheme, dark; 2026-10-21)
GROUND = (15, 17, 20)  # the look pages' background
SHARE = (110, 161, 240)  # the summed share's glow at its largest, the look pages' blue
WALL = (215, 218, 224)  # the wall's Nodes, the look pages' light grey
SCREEN = (120, 112, 72)  # the screen's regions, a dim yellow
LOWER_LINE = (255, 96, 96)  # the lower gap's streamlines, red
UPPER_LINE = (96, 224, 112)  # the upper gap's streamlines, green
MIDLINE = (150, 150, 150)  # the midline, grey


def png(path: Path, rgb: np.ndarray) -> None:
    """A PNG of an (H, W, 3) uint8 array, written with zlib alone."""
    height, width, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[row].tobytes() for row in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def line_to(
    img: np.ndarray, x0: float, y0: float, x1: float, y1: float, colour: tuple[int, int, int]
) -> None:
    """A thin line drawn by sampling (the image indexed [row, column])."""
    steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
    for s in range(steps + 1):
        t = s / steps
        c, r = int(round(x0 + t * (x1 - x0))), int(round(y0 + t * (y1 - y0)))
        if 0 <= r < img.shape[0] and 0 <= c < img.shape[1]:
            img[r, c] = colour


def flow_from_real_line(window: tuple[int, int]):  # type: ignore[no-untyped-def]
    """The Link currents and the Node shares summed over the window from the law's real line."""
    world, expected, board, line, wall, both, _lower, _upper = fields.three_fields()
    clock = world.node_clock
    jx = np.zeros((board.length - 1, board.height))
    jy = np.zeros((board.length, board.height - 1))
    rho = np.zeros((board.length, board.height))
    for t in range(window[0] - 1, min(window[1], both.now.shape[0])):  # the pair after t steps
        fx, fy = fields.link_currents(line, both.now[t], both.before[t])
        jx += fx
        jy += fy
        rho += fields.share(line, clock, both.now[t], both.before[t])
    return board, jx, jy, rho, wall


def flow_from_engine(window: tuple[int, int]):  # type: ignore[no-untyped-def]
    """The engine's integer board stepped with no draw (the world's `draw` removed: the regions report and
    nothing is credited, no hole and no front), the plain currents and the shares read at every interval of
    the window; the flow along +x across the Link (x, x + 1) is the current into x + 1 from its -x Port."""
    from event_universe import world_files
    from event_universe.lattice import Lattice
    from event_universe.loader.world import parse_world
    from event_universe.world_files import input_digest

    document = json.loads(fields.WORLD.read_text(encoding="utf-8"))
    document.pop("engine", None)
    files, digest = world_files.world_files(document), input_digest(document)
    mode = fields.WORLD.with_suffix(".mode.json")
    files[mode.name] = json.loads(mode.read_text(encoding="utf-8"))
    document.pop("draw", None)
    world = parse_world(document, files, digest)
    board = Lattice(world)
    index = [f.name for f in board.families].index("charge")
    length, height = world.shape[0], world.shape[1]
    jx = np.zeros((length - 1, height))
    jy = np.zeros((length, height - 1))
    rho = np.zeros((length, height))
    for t in range(window[1]):
        if t + 1 >= window[0]:
            currents = board.currents()[index]
            ox = board.offset[0]
            from_minus_x = np.asarray(currents[1], dtype=float)[ox : ox + length, :, 0]  # Port 1: -x
            from_minus_y = np.asarray(currents[3], dtype=float)[ox : ox + length, :, 0]  # Port 3: -y
            jx += from_minus_x[1:, :]
            jy += from_minus_y[:, 1:]
            rho += np.asarray(board.share_of(index)[0], dtype=float)[ox : ox + length, :, 0]
        board.step()
    return jx, jy, rho


def velocity(jx: np.ndarray, jy: np.ndarray, rho: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """v = J / rho on the Nodes: J per Node the mean of its two Links' flows per axis, rho the Node's share;
    NaN where the share is below 10^-9 of its largest."""
    vx = np.zeros_like(rho)
    vy = np.zeros_like(rho)
    vx[1:-1] = 0.5 * (jx[1:] + jx[:-1])
    vx[0], vx[-1] = jx[0], jx[-1]
    vy[:, 1:-1] = 0.5 * (jy[:, 1:] + jy[:, :-1])
    vy[:, 0], vy[:, -1] = jy[:, 0], jy[:, -1]
    safe = np.where(rho > 1e-9 * rho.max(), rho, np.nan)
    return vx / safe, vy / safe


def interpolated(field: np.ndarray, x: float, y: float) -> float:
    """The field's bilinear value at (x, y), NaN where a corner is NaN."""
    length, height = field.shape
    x = min(max(x, 0.0), length - 1.001)
    y = min(max(y, 0.0), height - 1.001)
    i, j = int(x), int(y)
    fx, fy = x - i, y - j
    values = field[i : i + 2, j : j + 2]
    if np.isnan(values).any():
        return float("nan")
    return float(
        values[0, 0] * (1 - fx) * (1 - fy)
        + values[1, 0] * fx * (1 - fy)
        + values[0, 1] * (1 - fx) * fy
        + values[1, 1] * fx * fy
    )


def streamlines(vx, vy, starts, x_end: float) -> list[np.ndarray]:  # type: ignore[no-untyped-def]
    """The streamlines from `starts` (x, y) to the column `x_end`: the Euler-midpoint step along the unit
    tangent of v, bilinear interpolation; a line ends where the share is below the floor or at the board's
    edge."""
    height = vx.shape[1]
    found = []
    for x0, y0 in starts:
        path = [(x0, y0)]
        x, y = x0, y0
        for _ in range(100000):
            ux, uy = interpolated(vx, x, y), interpolated(vy, x, y)
            if np.isnan(ux) or (ux == 0 and uy == 0):
                break
            norm = (ux * ux + uy * uy) ** 0.5
            mx, my = x + 0.5 * STEP * ux / norm, y + 0.5 * STEP * uy / norm
            ux2, uy2 = interpolated(vx, mx, my), interpolated(vy, mx, my)
            if np.isnan(ux2):
                break
            norm2 = (ux2 * ux2 + uy2 * uy2) ** 0.5
            x, y = x + STEP * ux2 / norm2, y + STEP * uy2 / norm2
            path.append((x, y))
            if x >= x_end or x < 0 or y < 0 or y > height - 1:
                break
        found.append(np.array(path))
    return found


def seeds_of(jx: np.ndarray, wall_x: int) -> tuple[list[tuple[float, float]], dict[str, list[float]]]:
    """The streamlines' seeds at equal flux across each gap: the flux through the Links from the wall's
    column to the next per row of the gap, its cumulative profile across the gap (the Node's flux spread
    over its row), cut at the quantiles; PER_GAP lines per gap, started one column behind the wall."""
    starts: list[tuple[float, float]] = []
    seeds: dict[str, list[float]] = {}
    for gap in (fields.LOWER, fields.UPPER):
        rows = list(range(gap[0], gap[1] + 1))
        flux = np.array([max(jx[wall_x, y], 0.0) for y in rows])
        cumulative = np.concatenate([[0.0], np.cumsum(flux)]) / flux.sum()
        edges = np.append(np.array(rows, dtype=float) - 0.5, rows[-1] + 0.5)
        quantiles = (np.arange(PER_GAP) + 0.5) / PER_GAP
        ys = np.interp(quantiles, cumulative, edges)
        seeds[str(gap)] = [round(float(y), 3) for y in ys]
        starts += [(wall_x + 1.0, float(y)) for y in ys]
    return starts, seeds


def picture(board, rho, lines, mid: float, target: Path) -> None:  # type: ignore[no-untyped-def]
    """The board on the site's dark ground (rgb(15, 17, 20), the look pages' background; the figure dark
    since 2026-10-21, the site's one colour scheme), the summed share as a blue glow, the wall light grey,
    the screen's column a dim yellow, the lower gap's lines red, the upper's green, the midline grey;
    SCALE pixels per Node."""
    img = np.zeros((board.height * SCALE, board.length * SCALE, 3), dtype=np.uint8)
    img[:, :] = GROUND
    dens = rho / rho.max()
    for x in range(board.length):
        for y in range(board.height):
            a = min(dens[x, y] ** 0.5, 1.0)
            img[y * SCALE : (y + 1) * SCALE, x * SCALE : (x + 1) * SCALE] = tuple(
                int(round(g + a * (s - g))) for g, s in zip(GROUND, SHARE, strict=True)
            )
    for x, y in board.beyond:
        img[y * SCALE : (y + 1) * SCALE, x * SCALE : (x + 1) * SCALE] = WALL
    for name in board.screen:
        for x, y in board.regions[name]:
            img[y * SCALE : (y + 1) * SCALE, x * SCALE : (x + 1) * SCALE] = SCREEN
    half = SCALE / 2
    for k, path in enumerate(lines):
        colour = LOWER_LINE if k < PER_GAP else UPPER_LINE
        for (x0, y0), (x1, y1) in zip(path[:-1], path[1:], strict=True):
            line_to(
                img, x0 * SCALE + half, y0 * SCALE + half, x1 * SCALE + half, y1 * SCALE + half, colour
            )
    line_to(img, 0, mid * SCALE + half, board.length * SCALE, mid * SCALE + half, MIDLINE)
    png(target, img)


def reading(board, jx, jy, rho, wall: float) -> dict[str, object]:  # type: ignore[no-untyped-def]
    """One flow's streamlines and their statistics: the seeds, the arrivals, the midline's crossings and the
    deepest excursion across it, the arrivals per region against the screen's flux shares, the flux
    conservation (the screen's flux over the gaps', the summed divergence behind the wall)."""
    wall_x = next(iter({x for x, _y in board.beyond}))
    screen_x = min(x for x, _y in board.regions[board.screen[0]])
    rows_per_region = len({y for _x, y in board.regions[board.screen[0]]})
    starts, seeds = seeds_of(jx, wall_x)
    vx, vy = velocity(jx, jy, rho)
    lines = streamlines(vx, vy, starts, float(screen_x))
    mid = (board.height - 1) / 2  # the board's centre row, 23.5 at the height 48; the gaps' axis is 24
    crossings = 0
    arrived = []
    for path in lines:
        side = np.sign(path[:, 1] - mid)
        crossings += int((np.diff(side[side != 0]) != 0).sum())
        if path[-1, 0] >= screen_x - 0.5:
            arrived.append(float(path[-1, 1]))
    bins = [0] * len(board.screen)
    for e in arrived:
        bins[min(int(e // rows_per_region), len(bins) - 1)] += 1
    screen_row = [
        float(sum(jx[screen_x - 1, y] for y in range(rows_per_region * r, rows_per_region * (r + 1))))
        for r in range(len(board.screen))
    ]
    total = sum(screen_row)
    gap_flux = float(
        sum(max(jx[wall_x, y], 0.0) for g in (fields.LOWER, fields.UPPER) for y in range(g[0], g[1] + 1))
    )
    xs_in = np.arange(wall_x + 1, board.length - 1)
    ys_in = np.arange(1, board.height - 1)
    divergence = float(
        np.abs(
            jx[np.ix_(xs_in, ys_in)]
            - jx[np.ix_(xs_in - 1, ys_in)]
            + jy[np.ix_(xs_in, ys_in)]
            - jy[np.ix_(xs_in, ys_in - 1)]
        ).sum()
    )
    lower_lines, upper_lines = lines[:PER_GAP], lines[PER_GAP:]
    excursion = max(
        [float(max(p[:, 1].max() - mid, 0.0)) for p in lower_lines]
        + [float(max(mid - p[:, 1].min(), 0.0)) for p in upper_lines]
    )
    return {
        "streamlines": len(lines),
        "seeds": seeds,
        "midline_row": mid,
        "arrived_at_the_screen": len(arrived),
        "midline_crossings": crossings,
        "deepest_excursion_across_the_midline_nodes": round(excursion, 3),
        "lower_gap_lines_ending_below_midline": sum(1 for p in lower_lines if p[-1, 1] < mid),
        "upper_gap_lines_ending_above_midline": sum(1 for p in upper_lines if p[-1, 1] > mid),
        "arrival_rows": [round(e, 2) for e in arrived],
        "arrivals_per_region": bins,
        "screen_flow_per_region_share": [round(v / total, 4) for v in screen_row],
        "expected_arrivals_per_region": [round(len(lines) * v / total, 1) for v in screen_row],
        "flux_through_the_gaps_over_W_c": round(gap_flux / wall, 2),
        "screen_flux_over_gap_flux": round(total / gap_flux, 4),
        "summed_divergence_behind_the_wall_over_gap_flux": round(divergence / gap_flux, 4),
        "lines": lines,
        "mid": mid,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--engine", action="store_true", help="also the engine's integer board")
    args = parser.parse_args(argv)
    # the flow summed over the whole run, so that the summed current's divergence is the share's change
    # over the run, 0 behind the wall at the start and the tail at the end (the share's change is the
    # currents), and streamlines seeded at equal flux arrive at equal flux
    window = (1, 130)
    board, jx, jy, rho, wall = flow_from_real_line(window)
    flows = {"real line": (jx, jy, rho)}
    if args.engine:
        flows["engine"] = flow_from_engine(window)
    report: dict[str, object] = {}
    for label, (jx, jy, rho) in flows.items():
        found = reading(board, jx, jy, rho, wall)
        lines, mid = found.pop("lines"), found.pop("mid")
        picture(board, rho, lines, mid, PICTURES / f"c_streamlines_{label.replace(' ', '_')}.png")
        report[label] = found
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "c_streamlines.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
