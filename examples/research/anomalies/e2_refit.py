"""Refit the FRW family to a sweep's (D, z) with a wider redshift error.

Reads a summary.json written by e2_hubble.py and refits the family with
sigma_z = gap scatter + ceiling half-step (0.5 / k_e) in quadrature, then once more
with the sigma rescaled so that chi2/dof = 1 at the best fit (the gap-scatter sigma is
conservative because the gaps drift with k along the train rather than scatter).

usage: PYTHONPATH=src python examples/research/anomalies/e2_refit.py SUMMARY_JSON [--output DIR]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e2_hubble import fit_family  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path, help="summary.json of one e2_hubble.py run")
    parser.add_argument("--output", type=Path, help="optional directory for refit.json")
    args = parser.parse_args()
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    pts = []
    for r in summary["runs"]:
        if "z" not in r:
            continue
        sig = math.sqrt(r["z_err_gap_scatter"] ** 2 + (0.5 / r["hop_time_at_launch"]) ** 2)
        pts.append((r["distance"], r["z"], sig))
    fit = fit_family(pts)
    fit["chi2_per_dof"] = fit["chi2"] / max(1, len(pts) - 3)
    first = {"load": summary["load"], "points": pts, "fit": fit}
    print(json.dumps(first, indent=1))
    scale = math.sqrt(max(fit["chi2"] / max(1, fit["dof"]), 1e-12))
    fit2 = fit_family([(d, z, s * scale) for d, z, s in pts])
    second = {
        "residual_scaled": {
            "sigma_scale": scale,
            "n": fit2["n"],
            "n_interval_1sigma": fit2["n_interval_1sigma"],
            "q0": fit2["q0"],
            "q0_interval": fit2["q0_interval"],
        }
    }
    print(json.dumps(second, indent=1))
    if args.output is not None:
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "refit.json").write_text(json.dumps({**first, **second}, indent=1) + "\n")


if __name__ == "__main__":
    main()
