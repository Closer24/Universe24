"""The line's reading, live (the design verdict of 2026-10-19, section 5): the line's world is loaded and stepped by the engine's own step for its declared intervals with no look written, and per interval, from the electron's two lines z = now + i second, Q = SUM |z|^2, the dipole D(t) = SUM_i (x_i - c) |z_i|^2 / Q per axis in Nodes (x the 2p_x's axis, the line's), the peak Node and its level, the centre level, the electron's Wronskian SUM (now x im_before - im_now x before), and the electron's own row of the sign holder (the row it writes and never reads, `loader/derived.row_of`) at the centre and at the lobes named by the blind along +x and -x, its breathing. With `--reread <reading>.json` a saved reading's rows are read again against the blind with no stepping (the checks as the blind words them, the numbers untouched). The checks against the blind (`expectation.json`, the world's entry): the dipole's period from its zero crossings (twice the mean spacing) and from a least-squares cosine (the frequency scanned, the phase and the amplitude by the normal equations) within the tolerance of the blind's period, its amplitude from the fit within the tolerance of the blind's, Q within the walk's budget, the sign row's period at the lobe from its zero crossings about its mean or from a least-squares cosine within the tolerance of the blind's period (the blind's wording, either reading). Written to `<world>.reading.json`; every number the engine's, the script summing, fitting and comparing and inventing none.

PYTHONPATH=src python examples/events/atom/read_line.py examples/events/atom/atom_line.json [--expectation expectation.json] [--standing atom_line.standing.json] [--intervals N] [--out atom_line.reading.json]
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.lattice import Lattice
from event_universe.loader.derived import row_of
from event_universe.world_files import load_world

AXES = ("x", "y", "z")


def crossings(values: np.ndarray) -> list[float]:
    """The zero crossings of a series about 0, each the interval by linear interpolation."""
    found = []
    for k in range(len(values) - 1):
        a, b = float(values[k]), float(values[k + 1])
        if a == 0 and b != 0:
            found.append(float(k))
        elif a * b < 0:
            found.append(k + a / (a - b))
    return found


def period_from_crossings(values: np.ndarray) -> float | None:
    """The period from the zero crossings, twice their mean spacing; None below two crossings."""
    at = crossings(values)
    if len(at) < 2:
        return None
    return 2 * (at[-1] - at[0]) / (len(at) - 1)


def cosine_fit(values: np.ndarray, about: float, span: float) -> dict[str, float]:
    """A least-squares cosine a cos(w t) + b sin(w t) + c over the series, the frequency w scanned about 2 pi / about within the span of periods, then refined: the period, the amplitude sqrt(a^2 + b^2), the phase, the offset and the residual's root mean square."""
    t = np.arange(len(values), dtype=np.float64)
    best: dict[str, float] | None = None
    periods = np.linspace(about * (1 - span), about * (1 + span), 801)
    for step in (periods, None):
        if step is None:
            assert best is not None
            step = np.linspace(best["period"] * 0.995, best["period"] * 1.005, 401)
        for period in step:
            w = 2 * math.pi / period
            design = np.stack([np.cos(w * t), np.sin(w * t), np.ones_like(t)], axis=1)
            coefficients, *_rest = np.linalg.lstsq(design, values, rcond=None)
            residual = float(np.sqrt(np.mean((design @ coefficients - values) ** 2)))
            if best is None or residual < best["residual"]:
                a, b, c = (float(v) for v in coefficients)
                best = {
                    "period": float(period),
                    "amplitude": math.hypot(a, b),
                    "phase": math.atan2(-b, a),
                    "offset": c,
                    "residual": residual,
                }
    assert best is not None
    return best


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("world", type=Path, help="the line's world file, its mode file beside it")
    parser.add_argument(
        "--expectation", type=Path, default=Path(__file__).resolve().parent / "expectation.json"
    )
    parser.add_argument(
        "--standing",
        type=Path,
        default=None,
        help="the tool's readings beside the world (<world>.standing.json)",
    )
    parser.add_argument("--record", default="electron", help="the record's family")
    parser.add_argument(
        "--intervals", type=int, default=None, help="the intervals stepped (the world's own)"
    )
    parser.add_argument(
        "--out", type=Path, default=None, help="the reading's file (<world>.reading.json)"
    )
    parser.add_argument(
        "--reread",
        type=Path,
        default=None,
        help="a saved reading whose per-interval rows are read again against the blind, no stepping",
    )
    args = parser.parse_args(argv)
    stem = args.world.name.rsplit(".", 1)[0]
    expectation = (
        json.loads(args.expectation.read_text(encoding="utf-8")) if args.expectation.exists() else {}
    )
    blind = (expectation.get("worlds") or {}).get(stem, {})
    standing_path = args.standing or args.world.with_suffix(".standing.json")
    tool = json.loads(standing_path.read_text(encoding="utf-8")) if standing_path.exists() else {}
    board = Lattice(load_world(args.world), None)
    world = board.world
    families = board.families
    index = [f.name for f in families].index(args.record)
    holder = next(read.family for read in families[index].reads if families[read.family].wronskian)
    own = row_of(families, index, 0)
    width = families[holder].width
    assert own is not None
    shape = tuple(int(v) for v in world.shape)
    centre = tuple(int(v) for v in world.bodies[0].nodes[0])
    grids = [
        g.astype(np.float64)
        for g in np.meshgrid(
            *(np.arange(e) - c for e, c in zip(shape, centre, strict=True)), indexing="ij"
        )
    ]
    lobes = [int(v) for v in blind.get("sign_row_read_at", [3, -3])]
    at_lobes = [(centre[0] + d, centre[1], centre[2]) for d in lobes]
    intervals = world.intervals if args.intervals is None else args.intervals
    rows: list[dict[str, Any]] = []
    started = time.time()
    saved = json.loads(args.reread.read_text(encoding="utf-8")) if args.reread else None

    def read() -> dict[str, Any]:
        re, im = board.record(index)
        z = re.now.astype(np.float64) + 1j * im.now.astype(np.float64)
        q = np.abs(z) ** 2
        total = float(q.sum())
        peak = np.unravel_index(int(np.argmax(q)), shape)
        row = board.states[holder].lines[own * width].now
        free = board.states[holder].lines[0].now
        return {
            "interval": int(board.interval),
            "Q": total,
            "dipole_nodes": [float((g * q).sum()) / total for g in grids],
            "peak_node": [int(v) for v in peak],
            "peak_level": math.sqrt(float(q.max())),
            "peak_now": float(np.abs(re.now).max()),
            "centre_level": math.sqrt(float(q[centre])),
            "wronskian": float(
                (
                    re.now.astype(np.float64) * im.before.astype(np.float64)
                    - im.now.astype(np.float64) * re.before.astype(np.float64)
                ).sum()
            ),
            "own_row_at_centre": int(row[centre]),
            "own_row_at_lobes": [int(row[node]) for node in at_lobes],
            "free_row_at_lobes": [int(free[node]) for node in at_lobes],
            "share_over_wall": None
            if board.total_share(index)[0] is None
            else float(board.total_share(index)[0]),
        }

    if saved is not None:
        rows.extend(saved["per_interval"])  # the saved run's rows, read again
        intervals = 0
    else:
        rows.append(read())
    for _ in range(intervals):
        board.step()
        if board.ended is not None:
            break
        rows.append(read())
        if board.interval % 8 == 0:
            r = rows[-1]
            print(
                json.dumps(
                    {
                        "interval": r["interval"],
                        "D_x": round(r["dipole_nodes"][0], 4),
                        "Q_over_Q0": round(r["Q"] / rows[0]["Q"], 5),
                        "peak": r["peak_node"],
                        "own_row_at_lobes": r["own_row_at_lobes"],
                        "seconds": round(time.time() - started),
                    }
                ),
                flush=True,
            )
    axis = AXES.index(str(blind.get("dipole_axis", "x")))
    dipole = np.array([r["dipole_nodes"][axis] for r in rows])
    q0 = rows[0]["Q"]
    about = float(blind.get("period_intervals", 112))
    fit = cosine_fit(dipole, about, 0.5)
    from_crossings = period_from_crossings(dipole)
    checks: dict[str, Any] = {}
    if "period_intervals" in blind:
        tolerance = float(blind["period_tolerance"])
        checks["period"] = {
            "from_zero_crossings": from_crossings,
            "zero_crossings_at": [round(v, 2) for v in crossings(dipole)],
            "from_cosine_fit": fit["period"],
            "blind": about,
            "tolerance": tolerance,
            "pass": from_crossings is not None
            and abs(from_crossings - about) <= tolerance * about
            and abs(fit["period"] - about) <= tolerance * about,
        }
        checks["amplitude_nodes"] = {
            "from_cosine_fit": fit["amplitude"],
            "largest_abs_dipole": float(np.abs(dipole).max()),
            "fit": fit,
            "blind": blind["amplitude_nodes"],
            "tolerance": blind["amplitude_tolerance"],
            "pass": abs(fit["amplitude"] - float(blind["amplitude_nodes"]))
            <= float(blind["amplitude_tolerance"]) * float(blind["amplitude_nodes"]),
        }
    if "Q_budget" in blind:
        budget = blind["Q_budget"]
        one_signed = float(budget["one_signed_over_224"]) * (len(rows) - 1) / 224
        either = float(budget["either_sign"])
        at_end = rows[-1]["Q"] / q0
        checks["Q_within_the_walks_budget"] = {
            "Q_over_Q0_at_end": at_end,
            "least": 1 - either,
            "most": 1 + one_signed + either,
            "pass": 1 - either <= at_end <= 1 + one_signed + either,
        }
    if "sign_row" in blind:
        lobe_rows = {}
        for k, d in enumerate(lobes):
            series = np.array([r["own_row_at_lobes"][k] for r in rows], dtype=np.float64)
            about_mean = series - series.mean()
            row_fit = cosine_fit(about_mean, about, 0.5)
            lobe_rows[str(d)] = {
                "mean": float(series.mean()),
                "least": float(series.min()),
                "most": float(series.max()),
                "period_from_zero_crossings_about_the_mean": period_from_crossings(about_mean),
                "fit": row_fit,
            }
        tolerance = float(blind.get("period_tolerance", 0.05))

        def within(period: float | None) -> bool:
            return period is not None and abs(period - about) <= tolerance * about

        checks["sign_row_breathing_at_the_beat"] = {
            "at_x_from_the_centre": lobe_rows,
            "blind": about,
            "tolerance": tolerance,
            "pass_by_the_zero_crossings": all(
                within(v["period_from_zero_crossings_about_the_mean"]) for v in lobe_rows.values()
            ),
            "pass_by_the_cosine_fit": all(within(v["fit"]["period"]) for v in lobe_rows.values()),
            "pass": all(
                within(v["period_from_zero_crossings_about_the_mean"]) or within(v["fit"]["period"])
                for v in lobe_rows.values()
            ),  # the blind's wording: the zero crossings about the mean, or a least-squares cosine
        }
    if "wronskian_conserved_within" in blind:
        half = world.quantum_action / 2
        ws = [r["wronskian"] for r in rows]
        checks["wronskian"] = {
            "at_the_lay": ws[0],
            "at_the_lay_over_half_T": ws[0] / half,
            "blind_at_the_lay_over_half_T": blind.get("wronskian_at_the_lay_over_half_T"),
            "least": min(ws),
            "most": max(ws),
            "largest_relative_deviation_from_the_lay": max(abs(w - ws[0]) for w in ws) / ws[0],
            "tolerance": blind["wronskian_conserved_within"],
            "pass": max(abs(w - ws[0]) for w in ws) / ws[0]
            <= float(blind["wronskian_conserved_within"]),
        }
    if "A_at_the_lay" in blind and isinstance(tool.get("A"), dict):
        checks["A_at_the_lay"] = {"read": tool["A"], "blind": blind["A_at_the_lay"]}
    if "peak_level_at_the_lay" in blind:
        checks["peak_level_at_the_lay"] = {
            "read": rows[0]["peak_level"],
            "blind": blind["peak_level_at_the_lay"],
            "read_now_alone": rows[0]["peak_now"],
            "blind_now_alone": blind.get("peak_now_at_the_lay"),
            "least_over_the_run": min(r["peak_level"] for r in rows),
            "most_over_the_run": max(r["peak_level"] for r in rows),
            "peak_node_misses": [r["interval"] for r in rows if r["peak_node"] != list(centre)],
        }
    marks = sorted({0, 1, 28, 56, 84, 112, 140, 168, 196, 224} & {r["interval"] for r in rows})
    reading = {
        "label": "lattice reading",
        "world": args.world.name,
        "intervals": int(saved["intervals"]) if saved is not None else int(board.interval),
        "centre": list(centre),
        "dipole_axis": AXES[axis],
        "sign_row": {"own_row": own, "holder": families[holder].name, "lobes_x_from_the_centre": lobes},
        "tool": {k: tool.get(k) for k in ("level", "Omega", "A", "beats") if k in tool},
        "dipole_at": {str(t): [round(v, 4) for v in rows[t]["dipole_nodes"]] for t in marks},
        "Q_over_Q0_at": {str(t): rows[t]["Q"] / q0 for t in marks},
        "peak_at": {str(t): [rows[t]["peak_node"], round(rows[t]["peak_level"], 1)] for t in marks},
        "own_row_at_lobes_at": {str(t): rows[t]["own_row_at_lobes"] for t in marks},
        "checks": checks,
        "per_interval": rows,
        "seconds": int(saved["seconds"]) if saved is not None else round(time.time() - started),
    }
    target = args.out or args.world.with_suffix(".reading.json")
    target.write_text(json.dumps(reading, indent=1) + "\n", encoding="utf-8")
    summary = {
        k: reading[k]
        for k in ("world", "intervals", "dipole_at", "Q_over_Q0_at", "own_row_at_lobes_at", "seconds")
    }
    summary["checks"] = {k: (v.get("pass") if isinstance(v, dict) else v) for k, v in checks.items()}
    summary["period"] = {
        "from_zero_crossings": from_crossings,
        "from_cosine_fit": fit["period"],
        "amplitude": fit["amplitude"],
    }
    print(json.dumps(summary, default=str))


if __name__ == "__main__":
    main()
