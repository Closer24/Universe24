"""Passive visualization of checked integer records; requires Matplotlib.

Floating arithmetic is used here only to display the exact decoded ratios.
This script never constructs or advances an engine state.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def plot(source, destination):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    report = json.loads(source.read_text())
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
    fig.patch.set_facecolor("#f8fafc")
    for ax in axes:
        ax.set_facecolor("#f8fafc")
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#dbe3eb", linewidth=.7)
        ax.set_xlabel("Rule3 update / prepared affine counter")
    for case, color, label in zip(report["cases"][:2], ("#64748b", "#007f86"),
                                   ("Flat rest preparation", "Curved geodesic preparation")):
        samples = case["decoded"]
        n = [row["n"] for row in samples]
        x = [row["transverse_position_numerator"]/row["transverse_position_denominator"] for row in samples]
        rate = [row["coordinate_time_derivative_denominator"]/row["coordinate_time_derivative_numerator"] for row in samples]
        axes[0].plot(n, x, ".-", color=color, label=label, linewidth=1.6)
        axes[1].plot(n, rate, ".-", color=color, linewidth=1.6)
    axes[0].set_ylabel("Decoded transverse coordinate X")
    axes[1].set_ylabel("Decoded proper / coordinate time rate")
    axes[1].set_ylim(.65, 1.03)
    axes[0].legend(loc="upper left", fontsize=8, frameon=False)
    fig.suptitle("One geodesic encoded by integer Rule3", x=.09, ha="left", fontsize=16, weight="bold")
    fig.text(.09, .885, "Actual official records + prepared decoder; 48 registers, divisor 6", fontsize=10, color="#475569")
    fig.text(.09, .035, "Coordinates remain inside one computational node. The rate uses the proved continuum calibration;\n"
             "this is neither a spatial packet nor a stationary redshift measurement.", fontsize=9, color="#475569")
    fig.subplots_adjust(left=.09, right=.98, bottom=.22, top=.79, wspace=.34)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT/"docs/evidence/ppwave_geodesic_clock.json")
    parser.add_argument("--out", type=Path, default=ROOT/"runs/ppwave-geodesic/summary.png")
    args = parser.parse_args()
    plot(args.source, args.out)
