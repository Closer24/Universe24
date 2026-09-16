"""E1 (rows): the rate and energy exponents of the lattice's dimming law.

Runs the redshift sweep's closed row with the light carrying a Kerengonen phase
(examples/relativity-probes/redshift_sweep.py, `wave = "link"` and `"interval"`)
at three distances, and reads two exponents against the stretch 1 + z on the
eye's counter: a for the count rate (arrival gaps) and b for the per-photon
energy read as the phase rate. The Tolman exponent of the lattice is then
n = a + b, the geometric factors (1/D^2 dilution, s/D angular size) being
measured separately in e1_geometry.py and shown to be load-independent.

usage: PYTHONPATH=src python examples/research/anomalies/e1_rows.py --output DIR [--rule link|interval]
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
from redshift_sweep import BASELINE, BUDGET, EMISSION, measure  # noqa: E402

from event_universe.runner import source_fingerprint  # noqa: E402

ROWS = ((24, 600), (48, 1100), (96, 2700))


def fit_slope(points: list[tuple[float, float]]) -> tuple[float, float]:
    """Slope and its standard error of y against x through the origin-free line."""
    n = len(points)
    mx = sum(x for x, _ in points) / n
    my = sum(y for _, y in points) / n
    sxx = sum((x - mx) ** 2 for x, _ in points)
    slope = sum((x - mx) * (y - my) for x, y in points) / sxx
    resid = [y - (my + slope * (x - mx)) for x, y in points]
    se = math.sqrt(sum(r * r for r in resid) / max(1, n - 2) / sxx) if n > 2 else float("nan")
    return slope, se


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rule", choices=["link", "interval"], default="link")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    runs = []
    for length, ticks in ROWS:
        t0 = time.time()
        run = measure(
            f"wave, phase per {args.rule}, row {length}",
            length,
            EMISSION,
            BUDGET,
            BASELINE,
            ticks,
            args.rule,
        )
        run["host_seconds"] = round(time.time() - t0, 1)
        runs.append(run)
        print(
            f"{run['label']}: D {run['distance']}, z {run.get('z')}, span stretch {run.get('gap_ratio_over_the_frequency_span')},"
            f" freq {run.get('frequency_at_the_source')} -> {run.get('frequency_at_the_eye')}, ratio {run.get('frequency_ratio')}"
            f" (predicted {run.get('frequency_ratio_predicted')}), gaps {run['gaps_on_the_eye_clock']}, {run['host_seconds']} s",
            flush=True,
        )
    # Control at zero emission, row 48.
    t0 = time.time()
    control = measure(
        f"wave, phase per {args.rule}, no emission, row 48", 48, 0, BUDGET, BASELINE, 600, args.rule
    )
    control["host_seconds"] = round(time.time() - t0, 1)
    print(
        f"{control['label']}: z {control.get('z')}, frequency ratio {control.get('frequency_ratio')}",
        flush=True,
    )
    # Exponents: the rate ratio over the frequency span is 1 / (gap ratio) by construction of the
    # gaps; the phase-rate ratio is measured. Fit ln(ratio) = -a ln(1 + z_span) etc.
    pts_rate = []
    pts_energy = []
    for run in runs:
        s = run.get("gap_ratio_over_the_frequency_span")
        f = run.get("frequency_ratio")
        if s and f:
            pts_rate.append((math.log(s), math.log(1 / s)))  # rate falls as 1/stretch, by the gaps
            pts_energy.append((math.log(s), math.log(abs(f))))
    a, a_se = fit_slope(pts_rate)
    b, b_se = fit_slope(pts_energy)
    report = {
        "source_sha256": source_fingerprint(),
        "rule": args.rule,
        "runs": runs,
        "control": control,
        "exponents_vs_span_stretch": {
            "a_rate": round(-a, 4),
            "a_se": round(a_se, 4),
            "b_energy_phase_rate": round(-b, 4),
            "b_se": round(b_se, 4),
            "n_tolman_lattice": round(-a - b, 4),
            "n_se": round(math.sqrt(a_se**2 + b_se**2), 4),
            "stretch_range": [
                round(min(math.exp(x) for x, _ in pts_rate), 3),
                round(max(math.exp(x) for x, _ in pts_rate), 3),
            ],
            "points": len(pts_rate),
        },
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print("exponents:", json.dumps(report["exponents_vs_span_stretch"]))


if __name__ == "__main__":
    main()
