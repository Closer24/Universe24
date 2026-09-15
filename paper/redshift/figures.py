"""Figures for the redshift paper, drawn only from recorded summary files.

Usage: python figures.py --sweep summary.json --hubble hubble.json --output figures
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def figure_law(sweep: dict, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    runs = sweep["runs"]
    rows = [r for r in runs if r["label"].startswith("row") and r.get("z") is not None]
    ax.plot(
        [r["distance"] for r in rows],
        [math.log(1 + r["z"]) for r in rows],
        "o",
        label="rows 16 to 96, emission 16 per Node per tick",
    )
    reference = next((r for r in rows if r["length"] == 48), None)
    if reference and reference.get("alpha_from_schedule"):
        alpha = reference["alpha_from_schedule"]
        grid = [0, max(r["distance"] for r in rows) * 1.05]
        ax.plot(
            grid,
            [alpha * d for d in grid],
            "-",
            color="gray",
            linewidth=1,
            label=f"slope from the hop schedule, alpha = {alpha:.4f} per link",
        )
        # The ceiling's launch offset: k_e = 8 while the load stands at 7.02 budgets, so the
        # continuum integral runs from 7.5 and ln(1 + z) = alpha D - ln(8 / 7.5).
        offset = math.log(
            reference["hop_time_at_launch"] / (reference["baseline"] / reference["budget"] + 0.5)
        )
        ax.plot(
            grid,
            [alpha * d - offset for d in grid],
            "--",
            color="gray",
            linewidth=1,
            label=f"the same slope with the launch offset, ln(8/7.5) = {offset:.3f}",
        )
    for label, marker in (("half the emission", "v"), ("double the emission", "^")):
        run = next((r for r in runs if r["label"] == label and r.get("z") is not None), None)
        if run:
            ax.plot(
                [run["distance"]],
                [math.log(1 + run["z"])],
                marker,
                label=f"{label} (row 48)",
            )
    for label, marker in (("launch at k = 1", "x"), ("launch at k = 4", "+"), ("launch at k = 16", "*")):
        run = next((r for r in runs if r["label"] == label and r.get("z") is not None), None)
        if run:
            ax.plot(
                [run["distance"]],
                [math.log(1 + run["z"])],
                marker,
                color="black",
                label=f"{label} (row 48)",
            )
    ax.set_xlabel("distance from the lamps to the eye, D (links)")
    ax.set_ylabel("ln(1 + z) on the eye's clock")
    ax.set_title("The stretch against the distance on closed rows")
    ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    fig.savefig(output / "redshift_law.pdf")
    plt.close(fig)


def figure_residuals(hubble: dict, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    picks = (
        ("linear load (n = 1), rate and amount loss (B)", "linear load, reading B", "s--"),
        ("quadratic load (n = 2), rate and amount loss (B)", "quadratic load, reading B", "^--"),
        ("flat LambdaCDM, Omega_m 0.334", "flat LambdaCDM", "o-"),
        ("linear load (n = 1), rate loss only (A)", "linear load, reading A", "x:"),
    )
    for key, label, style in picks:
        rows = hubble["fits"][key]["binned_residuals_model_minus_data"]
        centers = [math.sqrt(r["z_low"] * r["z_high"]) for r in rows]
        ax.errorbar(
            centers,
            [r["mean_residual_mag"] for r in rows],
            yerr=[r["error_of_mean_mag"] for r in rows],
            fmt=style,
            capsize=3,
            label=label,
        )
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xscale("log")
    ax.set_xlabel("redshift z (bin centre)")
    ax.set_ylabel("model - data (mag), one free offset each")
    ax.set_title("Binned residuals against the Pantheon+ Hubble-flow sample")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(output / "hubble_residuals.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sweep", type=Path, required=True)
    parser.add_argument("--hubble", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    figure_law(json.loads(args.sweep.read_text(encoding="utf-8")), args.output)
    figure_residuals(json.loads(args.hubble.read_text(encoding="utf-8")), args.output)
    print("Wrote figures to " + str(args.output))


if __name__ == "__main__":
    main()
