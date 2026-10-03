"""The atom's gate reader, GameBoard readings labelled so and no measurement (docs/ENGINE.md section 4, the folder atom_gate; the mathematician's 172, the rotation read summed over the body and over a window of whole periods): a world of the nucleus and the electron is loaded as tools/run_inputs.py loads it and stepped by the engine's own step over the window, and at every interval the electron's record (its two lines, re and im, at every Node where it stands) gives the pair (SUM_i a_(i,t) (a_(i,t+1) + a_(i,t-1)), SUM_i a_(i,t)^2) over both lines, exact integers; their quotient over the whole window is 2 cos omega_read in the windowed summed form, which for one rotating mode has no singular interval (a plane crosses 0 at no Node), and over successive windows of one period each its drift; omega_read is set beside the free record's omega_0 (2 cos omega_0 = num / den twice) as the binding omega_0 - omega_read in radians per interval and in levels of the sign row (times Gamma). Beside it: the nucleus's share in quanta at its Node and over the board at every tenth interval (a declaration's reading, the one-Node record spreading), the sign row's time level at the nucleus's Node and at the electron's declared Node at the start, the electron's share over the board in quanta (the summed share over W_c), the cube's 48 images (per family the first interval at which one departs; the holder under the rotation departs at the lay, its odd lines' remainders at the origin and not complemented on the image side) (tools/body_standing.py's read, the interval through which they hold) and the books at the end. For the derived atom's run (ALGEBRA.md, the mathematician's 218 and 219 with the advisor's second; the folder's `blind_derived_run`): the sign holder's write weight k and its level weight E_s as the loader read them from the universe file with their ratio to Gamma E_s, the holder's rows at the start (per row its time level at the nucleus's Node and at the electron's declared Node, the row each record owns and the rows its turn reads, every row but its own), the content holders' time levels at the two Nodes against their rests (the self-read kept), the electron's rotation against the lay's own clock pair from the mode file, the electron's share deviation over the Nodes where the lay's share stands at the quarters of the window (tools/body_standing.py's read (2)) and the centroid of its share over the board at the window's ends with its drift (read (1)), and the declared region detector's click lines over the window (the owner's decision of 2026-10-03, 09:38 Israel, a detector beside the body: per family the net inflow summed, in quanta over W_c, the one measurement, labelled DETECTOR, beside its field lines). The tool compares nothing, holds no number of the law and writes nothing to the engine; with an expectation file the blind's rows are printed beside the readings.

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
from event_universe.loader.derived import count_wall, row_of
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


def electron_name(board: GameBoard, index: int) -> str:
    """A family's name by its index, the books' key."""
    return str(board.families[index].name)


def rows_read(
    board: GameBoard, sign: int, charged: tuple[int, int], at: tuple[tuple[int, ...], tuple[int, ...]]
) -> dict[str, Any]:
    """The sign holder's rows at the start (ALGEBRA.md, No record reads its own write of the sign): per row its time level at the two Nodes, and per charged record the row it owns (its Wronskian's) and the rows its read and its turn take, every row but its own; the row 0 the free row no record owns."""
    holder, lines = board.families[sign], board.states[sign].lines
    rows = {
        str(r): {
            "time_level_at_nucleus_node": int(lines[r * holder.width].now[at[0]]),
            "time_level_at_electron_declared_node": int(lines[r * holder.width].now[at[1]]),
        }
        for r in range(holder.records)
    }
    owned = {}
    for index in charged:
        own = row_of(board.families, index, 0)
        owned[board.families[index].name] = {
            "owns_row": own,
            "reads_rows": [r for r in range(holder.records) if r != own],
        }
    return {"rows": holder.records, "lines_per_row": holder.width, "levels": rows, "records": owned}


def lay_clock(path: Path, family: str) -> Fraction | None:
    """The lay's own clock pair of a family's body from the mode file beside the world, [next + before, now] at the largest level, as 2 cos omega of the lay, the one number taken from a file; None where no body of the family is laid."""
    bodies = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"]
    for body in bodies:
        if body["family"] == family and body.get("clock"):
            return Fraction(int(body["clock"][0]), int(body["clock"][1]))
    return None


def clicks(lines: list[dict[str, object]], board: GameBoard) -> dict[str, Any]:
    """The declared region detectors' lines over the run (ENGINE.md section 5): per detector and family the click lines' count, the net inflow summed over the window in the current's units and in quanta over W_c (the host's reading, the measurement), the first interval reported and the largest inflow in size with its interval; beside them the field lines' first and last readings, the family's share over the region, a GameBoard diagnostic. Empty where the world declares no region."""
    found: dict[str, Any] = {}
    walls = {f.name: count_wall(f, board.world.quantum_action) for f in board.families if f.quanta}
    for line in lines:
        detector, family, event = str(line["detector"]), str(line["family"]), str(line["event"])
        if detector == "face":
            continue
        entry = found.setdefault(detector, {}).setdefault(family, {"clicks": 0, "inflow": 0})
        tick = int(str(line["tick"]))
        if event == "click":
            inflow = int(str(line["inflow"]))
            entry["clicks"] += 1
            entry["inflow"] += inflow
            entry.setdefault("first_interval", tick)
            if abs(inflow) > abs(int(entry.get("largest", 0))):
                entry["largest"], entry["largest_at"] = inflow, tick
        elif event == "field":
            entry.setdefault("field_first", {"tick": tick, "reading": line["reading"]})
            entry["field_last"] = {"tick": tick, "reading": line["reading"]}
    for families in found.values():
        for family, entry in families.items():
            if family in walls:
                entry["inflow_over_W_c"] = pair(Fraction(int(entry["inflow"]), walls[family]))
    return found


def atom(path: Path, intervals: int | None) -> dict[str, Any]:
    """One world's readings over the window (the world's ticks, or `intervals`), every number exact but the arccosines, labelled."""
    lines: list[dict[str, object]] = []  # the run's click and field lines, the observer's
    board = GameBoard(load_world(path), lines.append)
    nucleus, electron = (board.world.bodies[i] for i in (0, 1))
    heavy, family = board.families[nucleus.family], board.families[electron.family]
    gamma, action = board.world.node_clock, board.world.quantum_action
    sign = next(i for i, f in enumerate(board.families) if f.held and f.wronskian)
    centre = tuple(int(v) for v in nucleus.nodes[0])
    declared = tuple(int(v) for v in electron.nodes[0])
    holder, row = board.families[sign], board.states[sign].lines
    light = sum((line.now for line in row[:: holder.width]), 0)
    start = {
        "sign_row_level_at_nucleus": int(np.asarray(light)[centre]),
        "sign_row_level_at_electron_declared_node": int(np.asarray(light)[declared]),
        "nucleus_quanta_at_node": int(board.quanta(nucleus.family)[0][centre]),
        "electron_record_nodes": int((board.record(electron.family)[0].now != 0).sum()),
        "sign_holder_as_loaded": {
            "family": holder.name,
            "write_weight_k": holder.write,
            "level_weight_E_s": holder.level_weight,
            "node_clock": gamma,
            "k_over_gamma_E_s": pair(Fraction(holder.write, gamma * int(holder.level_weight or 1))),
        },
        "sign_rows": rows_read(board, sign, (nucleus.family, electron.family), (centre, declared)),
        "content_holders": [
            {
                "family": f.name,
                "rest": f.rest,
                "time_level_at_nucleus_node": int(board.states[i].lines[0].now[centre]),
                "time_level_at_electron_declared_node": int(board.states[i].lines[0].now[declared]),
            }
            for i, f in enumerate(board.families)
            if f.held and not f.wronskian
        ],
        "least_pace": board.books()[electron_name(board, electron.family)]["pace"],
    }
    laid = board.share_of(electron.family)[0]
    stands = laid != 0  # the Nodes where the lay's share stands, the deviation's Nodes
    everywhere = np.ones(board.shape, dtype=bool)
    images_tool = body_standing()
    departed: dict[str, int] = {}  # per family the first interval at which one of its 48 images departs

    def imaged(tick: int) -> None:
        for name in images_tool.images_kept(board):
            departed.setdefault(name.split(" row ")[0], tick)

    imaged(0)
    steps = board.world.ticks if intervals is None else intervals
    quarters = sorted({steps * part // (2 * 2) for part in (1, 2, 3, 2 * 2)} - {0})
    centroid_start = images_tool.centroids(laid, everywhere)
    deviations: dict[str, Any] = {}
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
        if board.tick in quarters:
            square = images_tool.deviation(board.share_of(electron.family)[0], laid, stands)
            deviations[str(board.tick)] = {
                "squared": pair(square),
                "rho": images_tool.rooted(square, action),
            }
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
    centroid_end = images_tool.centroids(board.share_of(electron.family)[0], everywhere)
    clock = lay_clock(path, board.families[electron.family].name)
    return {
        "label": LABEL,
        "input": path.name,
        "intervals": board.tick,
        "ended": board.ended,
        "node_clock": gamma,
        "quantum_action": action,
        "amplitude_bound": board.world.amplitude_bound,
        "at_the_start": start,
        "standing": {
            "lay_clock_two_cos_omega": pair(clock),
            "accumulated_minus_lay_clock": pair(accumulated - clock)
            if accumulated is not None and clock is not None
            else None,
            "first_period_minus_lay_clock": pair(Fraction(*windows[0]) - clock)
            if windows and clock is not None
            else None,
            "share_deviation": deviations,
            "share_nodes_at_the_lay": int(stands.sum()),
            "centroid": {
                "start": [pair(c) for c in centroid_start],
                "end": [pair(c) for c in centroid_end],
                "drift": [
                    None if a is None or b is None else pair(b - a)
                    for a, b in zip(centroid_start, centroid_end, strict=True)
                ],
            },
        },
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
        "clicks": clicks(lines, board),
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
            key: expected.get(key)
            for key in ("blind_large", "numbers_large", "numbers_toy", "blind_derived_run")
        }
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
