"""Figures for the manuscript, drawn only from recorded summary files.

Usage: python paper/figures.py --interference DIR --bell FILE --crossing FILE \
    --bond-sequence FILE --bond-uniform FILE --bond-biased FILE --bond-sweep FILE \
    --output paper/figures
Every input is a summary written by an experiment harness; nothing is computed
from the engine here. Needs matplotlib (the `render` extra).
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

PHASES = {"0": 0.0, "pi/2": math.pi / 2, "pi": math.pi, "3pi/2": 3 * math.pi / 2}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def largest_lattice_level(sweep: dict) -> dict:
    """The sweep level with the most lattice pairs per correlation."""
    return max(
        (lvl for lvl in sweep["levels"] if lvl["lattice"]), key=lambda lvl: lvl["pairs_per_correlation"]
    )


def figure_bell(bell: dict, sweep: dict, output: Path) -> None:
    labels = ["share", "lottery", "threshold", "plain", "bonded", "quantum owner"]
    bonded = largest_lattice_level(sweep)
    values = [
        bell["share"]["S"]["value"],
        bell["lottery"]["S"]["value"],
        2.0,
        2.0,
        bonded["S_mean"],
        2.8,
    ]
    # Statistical errors where a value is a count: the lottery's pairs and the bonded sweep.
    lottery_pairs = bell["lottery"].get("pairs_per_setting")
    errors = [0, 0, 0, 0, bonded["S_error_of_mean"], 0]
    if lottery_pairs:
        errors[1] = 2 * math.sqrt((1 - (values[1] / 4) ** 2) / lottery_pairs)
    colors = ["#4c72b0"] * 4 + ["#c44e52"] * 2
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.bar(labels, values, color=colors, yerr=errors, capsize=3, ecolor="black")
    ax.axhline(2, color="black", linestyle="--", linewidth=1)
    ax.axhline(2 * math.sqrt(2), color="gray", linestyle=":", linewidth=1)
    ax.text(5.4, 2.03, "local bound 2", ha="right", fontsize=8)
    ax.text(5.4, 2 * math.sqrt(2) + 0.03, "2 sqrt 2", ha="right", fontsize=8, color="gray")
    ax.set_ylabel("CHSH S")
    ax.set_ylim(0, 3.2)
    ax.set_title("Bell's test five times on one lattice")
    fig.tight_layout()
    fig.savefig(output / "bell_candidates.pdf")
    plt.close(fig)


def figure_convergence(sweep: dict, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for lattice, style, label in (
        (True, "o-", "lattice runs, 4 replicas"),
        (False, "s--", "registry alone, 4 replicas"),
    ):
        rows = [lvl for lvl in sweep["levels"] if lvl["lattice"] == lattice]
        ax.errorbar(
            [lvl["pairs_per_correlation"] for lvl in rows],
            [lvl["S_mean"] for lvl in rows],
            yerr=[lvl["sigma_S_predicted"] / math.sqrt(lvl["replicas"]) for lvl in rows],
            fmt=style,
            capsize=3,
            label=label,
        )
    ax.axhline(sweep["expected_S"], color="black", linestyle=":", linewidth=1)
    ax.axhline(2 * math.sqrt(2), color="gray", linestyle="-.", linewidth=1)
    ax.axhline(2, color="black", linestyle="--", linewidth=1)
    at = ax.get_yaxis_transform()
    ax.text(
        0.98,
        sweep["expected_S"] - 0.06,
        "registry expectation 724/256",
        ha="right",
        fontsize=8,
        transform=at,
    )
    ax.text(
        0.98, 2 * math.sqrt(2) + 0.03, "2 sqrt 2", ha="right", fontsize=8, color="gray", transform=at
    )
    ax.text(0.98, 2.03, "local bound 2", ha="right", fontsize=8, transform=at)
    ax.set_xscale("log")
    ax.set_xlabel("bonded pairs per correlation")
    ax.set_ylabel("CHSH S (mean of replicas, binomial error)")
    ax.set_title("The bonded value against the number of pairs")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(output / "bond_convergence.pdf")
    plt.close(fig)


def figure_interference(summary: dict, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    phi = [PHASES[row["phase"]] for row in summary["interference"]]
    measured = []
    for row in summary["interference"]:
        weights = row["measured_output_weights"]
        measured.append(weights[1] / sum(weights))
    balanced = [float(Fraction(row["measured_capture_probability"])) for row in summary["balanced"]]
    grid = [i * 2 * math.pi / 200 for i in range(201)]
    ax.plot(
        grid,
        [288 * (1 - math.cos(x)) / 625 for x in grid],
        color="#4c72b0",
        label="3:4 mixer, 288(1 - cos phi)/625",
    )
    ax.plot(
        grid,
        [(1 - math.cos(x)) / 2 for x in grid],
        color="#dd8452",
        label="balanced splitter, (1 - cos phi)/2",
    )
    ax.plot(phi, measured, "o", color="#4c72b0", label="recorded, 3:4")
    ax.plot(phi, balanced, "s", color="#dd8452", label="recorded, balanced")
    ax.set_xlabel("phase gate on the arm, phi")
    ax.set_ylabel("capture probability at D")
    ax.set_xticks([0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi])
    ax.set_xticklabels(["0", "pi/2", "pi", "3pi/2", "2pi"])
    ax.legend(fontsize=8)
    ax.set_title("Two-arm interference on the canonical runner")
    fig.tight_layout()
    fig.savefig(output / "interference.pdf")
    plt.close(fig)


def figure_null_notices(summary: dict, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    rows = {(row["variant"], row["phase"]): row for row in summary["null_notices"]}
    default = next(r for r in summary["which_path"] if r["arm_ticket"] == "null")
    for label, case, style in (
        ("default rule after an arm null", default["case"], "s--"),
        ("with null notices", rows[("arm_null", "pi")]["case"], "o-"),
    ):
        table = case["emission_by_tick"]
        ticks = sorted(int(t) for t in table)
        ax.plot(ticks, [table[str(t)].get("1", 0) for t in ticks], style, label=label)
    ax.set_xlabel("tick")
    ax.set_ylabel("classical emission at S per tick")
    ax.set_title("A null on the arm at tick 1: the source's emission")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output / "null_notices.pdf")
    plt.close(fig)


def figure_scale(summary: dict, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for phase, marker in (("pi/2", "o"), ("pi", "s")):
        rows = [r for r in summary["scale"] if r["phase"] == phase]
        amounts = [r["amount"] for r in rows]
        deviation = [max(float(Fraction(r["max_deviation_per_tick"])), 1e-3) for r in rows]
        ax.plot(amounts, deviation, marker + "-", label=f"largest departure per tick, phi = {phase}")
    ax.axhline(1, color="black", linestyle="--", linewidth=1)
    ax.text(30, 1.08, "one unit", fontsize=8)
    ax.text(700, 1.25e-3, "exact (0) at multiples of 625, drawn at the floor", fontsize=8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("full emission per tick (amount)")
    ax.set_ylabel("|emission - amount x |a_S|^2| (units)")
    ax.set_title("Emission-scale limit: the integer field follows |psi|^2 within one unit")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output / "scale.pdf")
    plt.close(fig)


def figure_crossing(summary: dict, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for name, style in (("offset_0", "o-"), ("offset_1", "s--")):
        rows = summary["runs"][name]["scales"]
        ticks = list(range(1, len(rows) + 1))
        scale = [r["(1, 1, 1)"][2] / r["(1, 1, 1)"][3] for r in rows]
        label = (
            "crossing nulls (same tick)" if name == "offset_0" else "sequential nulls (one tick apart)"
        )
        ax.plot(ticks, scale, style, label=label)
    ax.axhline(25 / 9, color="black", linestyle=":", linewidth=1)
    ax.text(12, 25 / 9 + 0.04, "conditional scale 25/9", ha="right", fontsize=8)
    ax.set_xlabel("tick")
    ax.set_ylabel("weight scale at the source S")
    ax.set_title("Two nulls before either notice arrives, and the correction")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output / "crossing_nulls.pdf")
    plt.close(fig)


def figure_outside(sequence: dict, uniform: dict, biased: dict, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    pairs = ["a,b", "a,b2", "a2,b", "a2,b2"]
    x = range(len(pairs))
    width = 0.27
    for offset, (label, data) in enumerate(
        (
            ("world's sequence", sequence),
            ("uniform outside source", uniform),
            ("biased outside source", biased),
        )
    ):
        rates = [data["correlations"][p]["bob_plus_rate"] for p in pairs]
        ax.bar([i + (offset - 1) * width for i in x], rates, width, label=label)
    ax.set_xticks(list(x))
    ax.set_xticklabels(["(a, b)", "(a, b')", "(a', b)", "(a', b')"])
    ax.set_ylabel("Bob's plus rate")
    ax.set_ylim(0, 1)
    ax.set_title("Bob's marginal against the setting pair: a biased source is a signal")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output / "outside_source.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--interference", type=Path, required=True, help="causal_interference summary.json"
    )
    parser.add_argument("--bell", type=Path, required=True, help="kerengonen-bell summary.json")
    parser.add_argument("--crossing", type=Path, required=True, help="crossing_nulls summary.json")
    parser.add_argument("--bond-sequence", type=Path, required=True)
    parser.add_argument("--bond-uniform", type=Path, required=True)
    parser.add_argument("--bond-biased", type=Path, required=True)
    parser.add_argument("--bond-sweep", type=Path, required=True, help="summary-bond-sweep.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    interference = load(args.interference)
    bond = load(args.bond_sequence)
    sweep = load(args.bond_sweep)
    figure_bell(load(args.bell), sweep, args.output)
    figure_convergence(sweep, args.output)
    figure_interference(interference, args.output)
    figure_null_notices(interference, args.output)
    figure_scale(interference, args.output)
    figure_crossing(load(args.crossing), args.output)
    figure_outside(bond, load(args.bond_uniform), load(args.bond_biased), args.output)
    print("Wrote figures to " + str(args.output))


if __name__ == "__main__":
    main()
