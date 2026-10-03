"""The atom's gate reader, GameBoard readings labelled so and no measurement (docs/ENGINE.md section 4, the folder atom_gate; the mathematician's 172, the rotation read summed over the body and over a window of whole periods): a world of the nucleus and the electron is loaded as tools/run_inputs.py loads it and stepped by the engine's own step over the window, and at every interval the electron's record (its two lines, re and im, at every Node where it stands) gives the pair (SUM_i a_(i,t) (a_(i,t+1) + a_(i,t-1)), SUM_i a_(i,t)^2) over both lines, exact integers; their quotient over the whole window is 2 cos omega_read in the windowed summed form, which for one rotating mode has no singular interval (a plane crosses 0 at no Node), and over successive windows of one period each its drift; omega_read is set beside the free record's omega_0 (2 cos omega_0 = num / den twice) as the binding omega_0 - omega_read in radians per interval and in levels of the sign row (times Gamma). Beside it: the nucleus's share in quanta at its Node and over the board at every tenth interval (a declaration's reading, the one-Node record spreading), the sign row's time level at the nucleus's Node and at the electron's declared Node at the start, the electron's share over the board in quanta (the summed share over W_c), the cube's 48 images (per family the first interval at which one departs; the holder under the rotation departs at the lay, its odd lines' remainders at the origin and not complemented on the image side) (tools/body_standing.py's read, the interval through which they hold) and the books at the end. The tool compares nothing, holds no number of the law and writes nothing to the engine; with an expectation file the blind's rows are printed beside the readings.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/atom_gate/read_atom.py [--intervals N] [--expectation <expectation>.json] <world>.json ...
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.game_board import GameBoard
from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LABEL = "GAMEBOARD"


def body_standing() -> Any:
    """tools/body_standing.py loaded by its path (tools/ is no package): its read of the cube's 48 images."""
    spec = importlib.util.spec_from_file_location("body_standing", ROOT / "tools" / "body_standing.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pair(value: Fraction | None) -> list[int] | None:
    """A fraction as [numerator, denominator] for the output, None where there is none."""
    return None if value is None else [value.numerator, value.denominator]


def summed(before: list[np.ndarray], now: list[np.ndarray], after: list[np.ndarray]) -> tuple[int, int]:
    """The rotation's pair at one interval over the record's lines and every Node: (SUM a_t (a_(t+1) + a_(t-1)), SUM a_t^2), exact integers (172's windowed form sums these over the window; for a plane the first is Re(conj(z_t) (z_(t+1) + z_(t-1))) and the second |z_t|^2 summed)."""
    numerator = weight = 0
    for b, n, a in zip(before, now, after, strict=True):
        z = n.astype(object)
        numerator += int((z * (a.astype(object) + b.astype(object))).sum())
        weight += int((z * z).sum())
    return numerator, weight


def binding(two_cos: Fraction, pair_of: tuple[int, int], gamma: int) -> dict[str, Any]:
    """omega_read from 2 cos omega_read beside the free record's omega_0 = acos(num / den): the binding omega_0 - omega_read in radians per interval and in levels of the sign row (the angle per level 1 / Gamma), the one place the reader leaves the integers for the reader's own arccosine, labelled so."""
    num, den = pair_of
    omega_read = math.acos(float(two_cos) / 2)
    omega_0 = math.acos(num / den)
    return {
        "two_cos_omega_read": pair(two_cos),
        "two_cos_omega_read_float": float(two_cos),
        "omega_read": omega_read,
        "omega_0": omega_0,
        "omega_0_minus_omega_read": omega_0 - omega_read,
        "in_levels_of_the_row": (omega_0 - omega_read) * gamma,
        "above_the_band_top": two_cos > Fraction(2 * num, den),
    }


def atom(path: Path, intervals: int | None) -> dict[str, Any]:
    """One world's readings over the window (the world's ticks, or `intervals`), every number exact but the arccosines, labelled."""
    board = GameBoard(load_world(path))
    nucleus, electron = (board.world.bodies[i] for i in (0, 1))
    heavy, family = board.families[nucleus.family], board.families[electron.family]
    gamma, action = board.world.node_clock, board.world.quantum_action
    sign = next(i for i, f in enumerate(board.families) if f.held and f.wronskian)
    centre = tuple(int(v) for v in nucleus.nodes[0])
    declared = tuple(int(v) for v in electron.nodes[0])
    row = board.states[sign].lines
    light = sum((line.now for line in row[:: board.families[sign].width]), 0)
    start = {
        "sign_row_level_at_nucleus": int(np.asarray(light)[centre]),
        "sign_row_level_at_electron_declared_node": int(np.asarray(light)[declared]),
        "nucleus_quanta_at_node": int(board.quanta(nucleus.family)[0][centre]),
        "electron_record_nodes": int((board.record(electron.family)[0].now != 0).sum()),
    }
    images_tool = body_standing()
    departed: dict[str, int] = {}  # per family the first interval at which one of its 48 images departs

    def imaged(tick: int) -> None:
        for name in images_tool.images_kept(board):
            departed.setdefault(name.split(" row ")[0], tick)

    imaged(0)
    steps = board.world.ticks if intervals is None else intervals
    every = 2 * (2 + 3)  # every tenth interval
    series: list[tuple[int, int, int]] = []
    nucleus_series: dict[str, Any] = {}
    electron_quanta: dict[str, Any] = {}
    for _ in range(steps):
        record = board.record(electron.family)
        before, now = [r.before.copy() for r in record], [r.now.copy() for r in record]
        board.step()
        if board.ended is not None:
            break
        after = [r.now for r in board.record(electron.family)]
        numerator, weight = summed(before, now, after)
        series.append((numerator, weight, board.tick))
        if len(departed) < len(board.families):
            imaged(board.tick)
        if board.tick % every == 0 or board.tick == 1:
            quanta = board.quanta(nucleus.family)[0]
            nucleus_series[str(board.tick)] = {
                "at_node": int(quanta[centre]),
                "over_the_board": int(quanta.sum()),
                "share_at_node_over_W_c": pair(
                    Fraction(int(board.share_of(nucleus.family)[0][centre]), count_wall(heavy, action))
                ),
            }
            total, frozen = board.total_share(electron.family)
            electron_quanta[str(board.tick)] = (
                None if total is None else pair(Fraction(total, count_wall(family, action)))
            )
    total_numerator = sum(n for n, _w, _t in series)
    total_weight = sum(w for _n, w, _t in series)
    accumulated = Fraction(total_numerator, total_weight) if total_weight else None
    per_interval = [Fraction(n, w) for n, w, _t in series if w]
    period = max(1, round(2 * math.pi / math.acos(float(accumulated or 0) / 2))) if accumulated else 1
    windows = []
    for first in range(0, len(series) - period + 1, period):
        block = series[first : first + period]
        windows.append(pair(Fraction(sum(n for n, _w, _t in block), sum(w for _n, w, _t in block))))
    return {
        "label": LABEL,
        "input": path.name,
        "intervals": board.tick,
        "ended": board.ended,
        "node_clock": gamma,
        "quantum_action": action,
        "amplitude_bound": board.world.amplitude_bound,
        "at_the_start": start,
        "rotation": {
            "accumulated_two_cos_omega": pair(accumulated),
            "least_per_interval": pair(min(per_interval)) if per_interval else None,
            "largest_per_interval": pair(max(per_interval)) if per_interval else None,
            "period_in_intervals": period,
            "two_cos_over_successive_periods": windows,
            "binding": binding(accumulated, family.pair, gamma) if accumulated else None,
        },
        "nucleus": nucleus_series,
        "electron_share_over_the_board_in_quanta": electron_quanta,
        "images": {
            "first_departure_per_family": departed,
            "kept_to_the_bit_through_the_run": sorted(
                f.name for f in board.families if f.name not in departed
            ),
        },
        "books": board.books(),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "worlds", type=Path, nargs="+", help="the world files, each with its mode file beside it"
    )
    parser.add_argument(
        "--intervals", type=int, default=None, help="the intervals read (the world's ticks)"
    )
    parser.add_argument("--expectation", type=Path, default=None, help="the blind expectation file")
    args = parser.parse_args(argv)
    found: dict[str, Any] = {"label": LABEL}
    found["worlds"] = {path.stem: atom(path, args.intervals) for path in args.worlds}
    if args.expectation is not None:
        expected = json.loads(args.expectation.read_text(encoding="utf-8"))
        found["blind"] = {
            key: expected.get(key) for key in ("blind_large", "numbers_large", "numbers_toy")
        }
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
