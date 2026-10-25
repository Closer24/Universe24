"""Hand w1's shared helpers (2026-10-25, engine-5.0-test at 8aa19393b): a bare torus world at a chosen den written beside a universe file of the three integers (den, Gamma, T), loaded through the engine's own loader; the point families of den's circle with their gaps g = (den - num) / den; a body laid by the engine's own lay by the count (`emission.laid_by_count`, the click's lay) on a record of a point family at one Node; the per-Node readings used by the measuring scripts (a record's share in its own unit, the volume holder's U at every Node). Nothing of src/ is changed; every reading is a lattice diagnostic beside the clicks."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from event_universe import emission, share, world_files
from event_universe.features import volume
from event_universe.lattice import Lattice
from event_universe.take import Item
from event_universe.world_files import load_world

GAMMA, ACTION = 1000, 36000  # the one universe's clock and quantum action (tests/laws_universe.SMALL)
DEN54 = 15162856759112389  # the candidate den, 54 bits, 617 x 196613 x 124992409
DEN_TOP = 1166991900949580266237  # the top tier's den, 70 bits
DEN_TOY = 1021  # the toy den


def bare_world(folder: Path, den: int, cube: int, intervals: int) -> Path:
    """The folded world's three keys on a bare torus of `cube` Nodes a side at the den `den`, the universe file beside it; the loader's root pointed at `folder`."""
    folder.mkdir(parents=True, exist_ok=True)
    universe = {"integers": {"den": den, "node_clock": GAMMA, "quantum_action": ACTION}}
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    world = {"universe": "u.json", "shape": [cube] * 3, "intervals": intervals}
    path = folder / "bare.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    world_files.REPOSITORY_ROOT = folder
    return path


def board_of(folder: Path, den: int, cube: int, intervals: int, lines: list | None = None) -> Lattice:
    """A Lattice on the bare world, its output lines appended to `lines` where given."""
    return Lattice(load_world(bare_world(folder, den, cube, intervals)), output=None if lines is None else lines.append)


def point_families(board: Lattice) -> list[tuple[int, str, int, int, float]]:
    """Every point family of the board (a plane row of den's circle): (index, name, num, den, g)."""
    found = []
    for index, family in enumerate(board.families):
        if family.plane and family.quanta:
            num, den = family.pair
            found.append((index, family.name, num, den, (den - num) / den))
    return found


def family_with_gap(board: Lattice, target: float) -> tuple[int, str, int, int, float]:
    """The point family whose g lies nearest to `target`."""
    return min(point_families(board), key=lambda row: abs(row[4] - target))


def light_emptied(board: Lattice) -> None:
    """The light's record emptied at every Node (tests/laws_universe.light_emptied)."""
    from event_universe import records

    light = board.world.seed
    state = board.states[light]
    zeros = records.zeros(board.shape, board.kind)
    state.lines[0] = records.Record(zeros, zeros.copy(), state.lines[0].remainder)


def lay_body(board: Lattice, index: int, at: tuple[int, int, int], record: int, sense: int = 1, count: int = 1) -> None:
    """One body: `count` quanta of the point family `index` laid at the Node `at` on its record `record` by the engine's own lay by the count (the click's lay, the quarter-turn plane (A, 0), (0, sense A), A^2 = count T div 2); the point's records and sign rows born at the first lay."""
    den = board.families[index].pair[1]
    emission.laid_by_count(board, Item(index, count, (at,), (den, den), sense=sense, record=record))


def record_share(board: Lattice, index: int, record: int) -> np.ndarray:
    """A record's share at every Node in its own unit W_rec (quanta, as a float array), read as `bound_body.bodies_closing` reads it."""
    gamma, unit = board.world.node_clock, board.unit
    content, factors = board.read(index, 1, record)
    own = share.family_share(board.families[index], board.lines_of(index, record), gamma, content, factors, unit)
    return np.asarray(own, dtype=object).astype(float) / float(board.credit.units[index])


def content_u(board: Lattice) -> np.ndarray:
    """The volume holder's U at every Node: the content c read from the volume's level (features/volume.level_of), U = -c ln(1 - 1 / Gamma)."""
    held = board.held[0]
    gamma = board.world.node_clock
    level = volume.level_of(gamma, board.states[held].lines[0].now)
    c = np.asarray(level, dtype=object).astype(float)
    return -c * math.log(1 - 1 / gamma)


def centroid(weights: np.ndarray, axis: int, cube: int) -> float:
    """The share-weighted position along `axis` on the torus, by the circular mean (the angle's mean unwrapped to [0, cube))."""
    total = float(weights.sum())
    if total <= 0:
        return float("nan")
    coords = np.indices(weights.shape)[axis]
    angle = 2 * math.pi * coords / cube
    s = float((weights * np.sin(angle)).sum()) / total
    c = float((weights * np.cos(angle)).sum()) / total
    mean = math.atan2(s, c) / (2 * math.pi) * cube
    return mean % cube


def torus_distance(a: float, b: float, cube: int) -> float:
    """The shorter distance between two positions along one wrapped axis."""
    d = abs(a - b) % cube
    return min(d, cube - d)


def slope(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Least-squares slope and intercept of ys over xs."""
    x, y = np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)
    ok = np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 2:
        return float("nan"), float("nan")
    a, b = np.polyfit(x, y, 1)
    return float(a), float(b)


def record_share_int(board: Lattice, index: int, record: int) -> np.ndarray:
    """A record's share at every Node in the current's units, Python's integers (the integer reading; `record_share` divides it by W_rec as a float check)."""
    gamma, unit = board.world.node_clock, board.unit
    content, factors = board.read(index, 1, record)
    own = share.family_share(board.families[index], board.lines_of(index, record), gamma, content, factors, unit)
    return np.asarray(own, dtype=object)


def position_int(weights: np.ndarray, axis: int, origin: int, cube: int) -> tuple[int, int, int]:
    """The share-weighted position along `axis` as an integer reading: the coordinates counted from `origin` on the torus (the shorter way, in (-cube div 2, cube div 2]), the sum of share x coordinate over the sum of the shares by one division with its remainder: (quotient, remainder, divisor), the position origin + quotient + remainder / divisor Links; the divisor 0 where no share stands."""
    coords = np.indices(weights.shape)[axis]
    rel = ((coords - origin + cube // 2) % cube) - cube // 2
    total = int(sum(int(w) for w in weights.reshape(-1) if int(w) > 0))
    if total == 0:
        return 0, 0, 0
    moment = int(sum(int(w) * int(z) for w, z in zip(weights.reshape(-1), rel.reshape(-1)) if int(w) > 0))
    quotient, remainder = divmod(moment, total)
    return int(quotient), int(remainder), total
