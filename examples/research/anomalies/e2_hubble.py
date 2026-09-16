"""E2: redshift-distance relation on the closed row for a linear and a quadratic load.

Reuses the redshift sweep's closed row (examples/relativity-probes/redshift_sweep.py)
unchanged for the linear load, and for the quadratic load gives every mass body a
bare-rate counter and makes its emission proportional to that counter
(amount = clock / denominator), so the load per Node grows as t^2 / (2 d) once
it dominates the baseline. The eye's counter reads z at each row length; the hop
schedule read off the rays gives k(t) directly; the FRW-correspondence family
D = (1/H) n [(1+z)^((n-1)/n) - 1] / (n - 1) is fitted to (D, z) as a cosmologist
would, with a launch-offset nuisance, to extract n and q0 = -(n-1)/n; and the
kinematic q = -k k'' / k'^2 is read off the schedule at the observation epoch.

usage: PYTHONPATH=src python examples/research/anomalies/e2_hubble.py --output DIR --load linear|quadratic [--rows 16 24 32 48 64 96]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "examples" / "relativity-probes"))
from redshift_sweep import (  # noqa: E402
    BUDGET,
    TRAIN,
    observe,
    op,  # noqa: E402
)
from redshift_sweep import document as row_document  # noqa: E402

from event_universe.runner import source_fingerprint  # noqa: E402

BASELINE = 7000
LINEAR_EMISSION = 16
QUADRATIC_DENOMINATOR = 50  # emission per cycle = clock / 50: load = 7000 + t^2 / 100
QUADRATIC_LAUNCH = 1500  # the lamps fire when their bare counter reads this, in the t^2 regime
QUADRATIC_TICKS = {16: 2200, 24: 2700, 32: 3300, 48: 5200, 64: 12500}
ROW_TICKS = {16: 500, 24: 600, 32: 800, 48: 1100, 64: 1700, 96: 2700}


def quadratic_document(length: int, ticks: int) -> dict:
    raw = row_document(length, LINEAR_EMISSION, BUDGET, BASELINE, ticks)
    raw["model_id"] = "redshift-closed-row-quadratic-load-v1"
    mass = next(k for k in raw["disturbance_types"] if k["name"] == "mass body")
    mass["fields"] = ["mass", "clock"]
    mass["defaults"] = {"mass": 1, "clock": 0}
    mass["updates"] = [{"field": "clock", "expression": op("add", {"field": "clock"}, 1)}]
    rule = next(r for r in raw["emissions"] if r["type"] == "mass body")
    rule["amount"] = {"field": "clock"}
    rule["denominator"] = QUADRATIC_DENOMINATOR
    # Late launch: every lamp carries a bare-rate counter and fires when it reads the
    # launch tick, so the train leaves when the quadratic term dominates the baseline.
    lamp = next(k for k in raw["disturbance_types"] if k["name"] == "lamp")
    lamp["fields"] = ["light", "train", "clock"]
    lamp["defaults"] = {"light": 1, "train": 0, "clock": 0}
    lamp["updates"] = [{"field": "clock", "expression": op("add", {"field": "clock"}, 1)}]
    lamp_rule = next(r for r in raw["emissions"] if r["type"] == "lamp")
    lamp_rule["amount"] = op("eq", {"field": "clock"}, QUADRATIC_LAUNCH)
    return raw


def measure_row(raw: dict, label: str) -> dict:
    t0 = time.time()
    seen = observe(raw)
    length = raw["shape"][0]
    schedule: list[tuple[int, int]] = []
    for train in range(1, TRAIN + 1):
        track = sorted((tick, x) for (t, x), tick in seen["first_seen"].items() if t == train)
        schedule.extend((a[0], b[0] - a[0]) for a, b in zip(track, track[1:], strict=False))
    schedule.sort()
    leading = sorted((tick, x) for (t, x), tick in seen["first_seen"].items() if t == 1)
    k_launch = leading[1][0] - leading[0][0] if len(leading) > 1 else None
    last_hops = []
    for train in range(1, TRAIN + 1):
        track = sorted((tick, x) for (t, x), tick in seen["first_seen"].items() if t == train)
        if len(track) > 1 and track[-1][1] == length - 1:
            last_hops.append(track[-1][0] - track[-2][0])
    absorbed = seen["absorptions"]
    gaps_clock = [b[1] - a[1] for a, b in zip(absorbed, absorbed[1:], strict=False)]
    distance = sum(length - 1 - i for i in range(TRAIN)) / TRAIN
    result = {
        "label": label,
        "length": length,
        "ticks": raw["ticks"],
        "distance": distance,
        "hop_time_at_launch": k_launch,
        "absorbed": len(absorbed),
        "first_absorption_tick": absorbed[0][0] if absorbed else None,
        "last_absorption_tick": absorbed[-1][0] if absorbed else None,
        "gaps_on_the_eye_clock": gaps_clock,
        "eye_clock_equals_ticks": all(a[0] == a[1] for a in absorbed),
        "last_hops_into_the_eye": last_hops,
        "schedule": schedule,
        "closure": seen["closure"],
        "host_seconds": round(time.time() - t0, 1),
    }
    if len(absorbed) == TRAIN and k_launch:
        mean_gap = sum(gaps_clock) / len(gaps_clock)
        z = mean_gap / k_launch - 1
        # Resolution: each gap is an integer; the mean of 11 gaps over k_launch.
        sd = math.sqrt(sum((g - mean_gap) ** 2 for g in gaps_clock) / (len(gaps_clock) - 1))
        result.update(
            {
                "z": round(z, 4),
                "z_err_gap_scatter": round(sd / math.sqrt(len(gaps_clock)) / k_launch, 4),
                "z_resolution_per_gap": round(1 / k_launch, 4),
                "k_o_over_k_e": round(sum(last_hops) / len(last_hops) / k_launch, 4),
                "duration_ratio": round(
                    (absorbed[-1][1] - absorbed[0][1]) / (k_launch * (TRAIN - 1)), 4
                ),
                "t_e": leading[0][0],
                "t_o": absorbed[TRAIN // 2][0],
            }
        )
    return result


def family_distance(z: float, n: float) -> float:
    """H D for a flat FRW scale factor a ~ t^n (n -> 1: ln(1+z))."""
    if abs(n - 1) < 1e-6:
        return math.log(1 + z)
    return n * ((1 + z) ** ((n - 1) / n) - 1) / (n - 1)


def _solve(points, n, inv_h_guess=None):
    xs = [family_distance(z, n) for _, z, _ in points]
    ds = [d for d, _, _ in points]
    ws = []
    for (_, z, sz), _x in zip(points, xs, strict=True):
        dz = 1e-4
        slope = (family_distance(z + dz, n) - family_distance(z - dz, n)) / (2 * dz)
        sigma_d = sz * slope * (inv_h_guess if inv_h_guess else 1.0)
        ws.append(1.0 / max(1e-12, sigma_d**2))
    sw = sum(ws)
    mx = sum(w * x for w, x in zip(ws, xs, strict=True)) / sw
    md = sum(w * d for w, d in zip(ws, ds, strict=True)) / sw
    sxx = sum(w * (x - mx) ** 2 for w, x in zip(ws, xs, strict=True))
    if sxx <= 0:
        return None
    inv_h = sum(w * (x - mx) * (d - md) for w, x, d in zip(ws, xs, ds, strict=True)) / sxx
    d0 = md - inv_h * mx
    chi2 = sum(w * (d - (inv_h * x + d0)) ** 2 for w, x, d in zip(ws, xs, ds, strict=True))
    return inv_h, d0, chi2


def fit_family(points: list[tuple[float, float, float]]) -> dict:
    """Fit D = F_n(z) / H + D0 to (D, z, sigma_z) over a grid of n (0.5..4); sigma_D = sigma_z dF/dz / H
    (two passes: H from an unweighted solve, then weighted). Returns n, H, D0, chi2 and the
    Delta chi2 <= 1 interval on n with H and D0 profiled."""
    grid = [0.5 + 0.01 * i for i in range(0, 351)]
    results = {}
    for n in grid:
        first = _solve(points, n)
        if first is None:
            continue
        second = _solve(points, n, first[0])
        if second is None:
            continue
        results[n] = second
    best_n = min(results, key=lambda n: results[n][2])
    inv_h, d0, chi2 = results[best_n]
    inside = [n for n, (_, _, c) in results.items() if c <= chi2 + 1]
    lo, hi = min(inside), max(inside)
    return {
        "n": best_n,
        "H_lattice": 1 / inv_h,
        "D0": d0,
        "chi2": chi2,
        "dof": len(points) - 3,
        "n_interval_1sigma": [lo, hi],
        "q0": -(best_n - 1) / best_n,
        "q0_interval": [-(hi - 1) / hi, -(lo - 1) / lo],
        "points": len(points),
        "grid": "n = 0.50..4.00 step 0.01, H and D0 profiled",
    }


def schedule_kinematics(schedule: list[tuple[int, int]], t_o: int, budget: int, load: str) -> dict:
    """H = k'/k and q = -k k''/k'^2 at the observation epoch from the configured load law,
    after checking that law against every measured hop (k = ceil(load / budget))."""
    if load == "linear":

        def law(t: float) -> float:
            return (BASELINE + LINEAR_EMISSION * t) / budget

        def d1(t: float) -> float:
            return LINEAR_EMISSION / budget

        def d2(t: float) -> float:
            return 0.0
    else:
        # emission per cycle = floor(clock / d) with residue: the load is the baseline plus
        # the running sum of clock / d, i.e. t^2 / (2 d) up to the integer residue.
        def law(t: float) -> float:
            return (BASELINE + t * t / (2 * QUADRATIC_DENOMINATOR)) / budget

        def d1(t: float) -> float:
            return t / QUADRATIC_DENOMINATOR / budget

        def d2(t: float) -> float:
            return 1 / QUADRATIC_DENOMINATOR / budget

    deviations = [d - math.ceil(law(s)) for s, d in schedule]
    k, kd, kdd = law(t_o), d1(t_o), d2(t_o)
    t_e = min(s for s, _ in schedule)
    return {
        "law_checked_against_hops": {
            "n_hops": len(schedule),
            "max_abs_deviation_ticks": max(abs(v) for v in deviations),
            "mean_deviation_ticks": sum(deviations) / len(deviations),
        },
        "H_at_observation": kd / k,
        "q_at_observation": -(k * kdd) / (kd * kd) if kd else None,
        "H_at_launch": d1(t_e) / law(t_e),
        "t_e": t_e,
        "t_o": t_o,
        "H_decreases_with_age": d1(t_e) / law(t_e) > kd / k,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--load", choices=["linear", "quadratic"], required=True)
    parser.add_argument("--rows", type=int, nargs="*", default=None)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    runs = []
    rows = args.rows or ([16, 24, 32, 48, 64, 96] if args.load == "linear" else [16, 24, 32, 48, 64])
    for length in rows:
        ticks = ROW_TICKS[length] if args.load == "linear" else QUADRATIC_TICKS[length]
        if args.load == "linear":
            raw = row_document(length, LINEAR_EMISSION, BUDGET, BASELINE, ticks)
        else:
            raw = quadratic_document(length, ticks)
        run = measure_row(raw, f"{args.load} load, row {length}")
        runs.append(run)
        print(
            f"{run['label']}: D {run['distance']}, k_e {run['hop_time_at_launch']}, absorbed {run['absorbed']},"
            f" z {run.get('z')} +/- {run.get('z_err_gap_scatter')}, k_o/k_e {run.get('k_o_over_k_e')},"
            f" gaps {run['gaps_on_the_eye_clock']}, field linear {run['closure']['linear_in_age']},"
            f" light conserved {run['closure']['light_conserved']}, {run['host_seconds']} s",
            flush=True,
        )
    points = [
        (r["distance"], r["z"], max(r["z_err_gap_scatter"], r["z_resolution_per_gap"] / math.sqrt(11)))
        for r in runs
        if "z" in r and r["z"] > 0
    ]
    fit = fit_family(points) if len(points) >= 3 else None
    kin = {
        r["label"]: schedule_kinematics(r["schedule"], r["t_o"], BUDGET, args.load)
        for r in runs
        if "t_o" in r
    }
    report = {
        "source_sha256": source_fingerprint(),
        "load": args.load,
        "runs": runs,
        "fit_points_D_z_sigma": points,
        "frw_family_fit": fit,
        "schedule_kinematics": kin,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print("fit:", json.dumps(fit))
    for label, k in kin.items():
        print(
            label,
            "H_obs",
            round(k["H_at_observation"], 6),
            "q_obs",
            k["q_at_observation"],
            "H_launch",
            round(k["H_at_launch"], 6),
            "H decreases with age",
            k["H_decreases_with_age"],
            "law vs hops",
            k["law_checked_against_hops"],
        )


if __name__ == "__main__":
    main()
