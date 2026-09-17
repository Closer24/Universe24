"""The mean field's prediction for Run 2 of experiment A5s (docs/EXPERIMENTS.md,
"Run 2, to the steady state (dense mode)"): the same two bodies at rest, the
boundary 2r from both (the box [5r + 1, 4r + 1, 4r + 1], A at (2r, 2r, 2r), B at
(3r, 2r, 2r)), run for t90 + 32 ticks, t90 the first tick at which the push on B
reaches 90 % of the box's steady state; the engine reads F(r) as the mean push
over the last 32 ticks (`analyze.py`), so the prediction is the mean field's
push averaged over the same ticks in the same box, computed with the kernel of
`mean_field_gauss.py` (the table [6, 1, 1, 1, 1, 1] over 11 as the linear map it
is on average; the steady state by BiCGSTAB to 1e-10, the transient stepped from
the empty board). Written before the run into `predictions.json` beside the
worlds, which `make_worlds.py` reads for the ticks of the dense series and
`analyze_dense.py` for the criterion's numbers.

Per r: the box, t50, t90, the ticks (t90 + 32), the steady push F_inf, the
predicted F (the mean over ticks t90 + 1 .. t90 + 32), the mean over the window
before it, F / F_inf, the beam 4096 (6/11)^(r-1); then the log-log exponent of
the predicted F over r = 12, 16, 20 and over 12, 16, 20, 24 (the criterion's
reference), the same fits of F_inf, the local exponent of F_inf between
consecutive r including r = 32 (the asymptote), and the free-space r from which
the local exponent of the axis flux stays within -2.0 +- 0.2 and +- 0.1 (the
entry's computation after Run 1, cited, not recomputed here).

Run:  python examples/nature/a5_static/predict_dense.py [--out predictions.json]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import mean_field_gauss as mf  # noqa: E402

DISTANCES = (12, 16, 20, 24)
ASYMPTOTE_DISTANCES = (32,)
WINDOW = 32
EXTRA_TICKS = 32
BOUNDARY_FACTOR = 2
# The free-space computation of the entry ("Computed after the run", half-width
# 96): the local exponent of the axis flux stays within -2.0 +- 0.2 from r = 21
# on and within +- 0.1 from r = 26 on.
FREE_SPACE_WITHIN = {"0.2": 21, "0.1": 26}


def engine_box(r: int, boundary: int) -> dict:
    """The engine's world for the mean field's quarter board: the full box and
    the two bodies' Nodes (make_worlds.py, margin = boundary)."""
    return {
        "shape": [r + 2 * boundary + 1, 2 * boundary + 1, 2 * boundary + 1],
        "a": [boundary, boundary, boundary],
        "b": [boundary + r, boundary, boundary],
    }


def predict(r: int, boundary: int, tol: float = 1e-10) -> dict:
    board = mf.sink_board(r, boundary)
    started = time.time()
    f, iterations = board.steady_state(tol)
    steady = float(board.push(board.arrivals(f), board.sinks[1])[0])
    seconds_steady = time.time() - started
    started = time.time()
    f = board.empty()
    pushes = [0.0]  # index t: the push of tick t (tick 0 has none)
    reached = {0.5: None, 0.9: None}
    t = 0
    while True:
        t += 1
        f, ticks_pushes = board.step(f)
        push = float(ticks_pushes[1][0])
        pushes.append(push)
        for fraction in reached:
            if reached[fraction] is None and push >= fraction * steady:
                reached[fraction] = t
        if reached[0.9] is not None and t >= reached[0.9] + EXTRA_TICKS:
            break
        if t > 4 * r * r + 64:
            raise RuntimeError(f"no t90 within 4 r^2 + 64 ticks at r = {r}")
    t90 = reached[0.9]
    ticks = t90 + EXTRA_TICKS
    window = pushes[ticks - WINDOW + 1 : ticks + 1]
    previous = pushes[ticks - 2 * WINDOW + 1 : ticks - WINDOW + 1]
    predicted = sum(window) / WINDOW
    return {
        "r": r,
        "boundary": boundary,
        "box": engine_box(r, boundary),
        "mean_field_shape": list(board.shape),
        "t50": reached[0.5],
        "t90": t90,
        "ticks": ticks,
        "window": WINDOW,
        "steady_push": steady,
        "predicted_push": predicted,
        "previous_window_push": sum(previous) / WINDOW,
        "fraction_of_steady": predicted / steady,
        "beam": mf.beam(r),
        "first_push_tick": next((k for k, p in enumerate(pushes) if p > 0), None),
        "push_at_ticks": {str(k): pushes[k] for k in (t90, ticks)},
        "bicgstab_iterations": iterations,
        "seconds": {"steady": seconds_steady, "transient": time.time() - started},
    }


def fit(points):
    slope, error = mf.fit_exponent(points)
    return {"points": [[r, v] for r, v in points], "exponent": slope, "error": error}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "predictions.json")
    parser.add_argument("--distances", type=int, nargs="*", default=list(DISTANCES))
    args = parser.parse_args(argv)
    wall = time.time()
    rows = {}
    for r in args.distances:
        row = predict(r, BOUNDARY_FACTOR * r)
        rows[r] = row
        print(
            f"r = {r:>2}: box {row['box']['shape']} (mean field {row['mean_field_shape']}),"
            f" t50 {row['t50']}, t90 {row['t90']}, ticks {row['ticks']}, F_inf {row['steady_push']:.4f},"
            f" predicted F {row['predicted_push']:.4f} ({100 * row['fraction_of_steady']:.1f} % of F_inf,"
            f" the window before {row['previous_window_push']:.4f}), beam {row['beam']:.4f},"
            f" first push at tick {row['first_push_tick']}; BiCGSTAB {row['bicgstab_iterations']}"
            f" iterations {row['seconds']['steady']:.0f} s, transient {row['seconds']['transient']:.0f} s"
        )
    asymptote = {}
    for r in ASYMPTOTE_DISTANCES:
        s = mf.sink_steady(r, BOUNDARY_FACTOR * r)
        asymptote[r] = s["push"]
        print(f"r = {r:>2}: F_inf {s['push']:.4f} ({s['iterations']} iterations, {s['seconds']:.0f} s)")
    steadies = {r: rows[r]["steady_push"] for r in rows} | asymptote
    ordered = sorted(steadies)
    local = {
        f"{a}-{b}": mf.local_exponent(a, steadies[a], b, steadies[b])
        for a, b in zip(ordered, ordered[1:], strict=False)
    }
    fits = {}
    for label, subset in (("12-16-20", (12, 16, 20)), ("12-16-20-24", (12, 16, 20, 24))):
        if all(r in rows for r in subset):
            fits[label] = {
                "predicted": fit([(r, rows[r]["predicted_push"]) for r in subset]),
                "steady": fit([(r, rows[r]["steady_push"]) for r in subset]),
            }
            print(
                f"fit over r = {label}: predicted F {fits[label]['predicted']['exponent']:.3f}"
                f" +- {fits[label]['predicted']['error']:.3f}, F_inf"
                f" {fits[label]['steady']['exponent']:.3f} +- {fits[label]['steady']['error']:.3f}"
            )
    print("local exponent of F_inf: " + ", ".join(f"{k}: {v:.3f}" for k, v in local.items()))
    summary = {
        "boundary_factor": BOUNDARY_FACTOR,
        "window": WINDOW,
        "extra_ticks": EXTRA_TICKS,
        "rows": [rows[r] for r in args.distances],
        "fits": fits,
        "asymptote": {
            "steady_push": {str(r): v for r, v in steadies.items()},
            "local_exponent": local,
            "free_space_within_band_from": FREE_SPACE_WITHIN,
        },
        "wall_seconds": time.time() - wall,
    }
    args.out.write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {args.out} in {summary['wall_seconds']:.0f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
