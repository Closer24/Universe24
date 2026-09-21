"""The figures of the click-model paper, drawn from the runs' summary and the
plan's exact computation only.

    PYTHONPATH=src python paper/click_model/figures.py \
        --summary paper/click_model/figures/summary.json --output paper/click_model/figures

The summary is written by `summarize_runs.py` from the runs of series L
(`examples/events/amplitude/`); the exact curve of S(N) and of E over the
setting difference is the computation of `checks/s_of_n.py` from the design's
formulas with the repository's tables, labelled as a computation wherever it
is drawn. Needs matplotlib (the `render` extra).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
# Black and white only (the model owner, 2026-09-21): every series is told apart by
# its fill (black, white with a hatch, grey), its marker or its line style, never by hue.
INK, DARK, MID, LIGHT, PALE = "#000000", "#404040", "#808080", "#c8c8c8", "#e4e4e4"
MUTED = DARK
WHITE = "#ffffff"
TSIRELSON = 2 * math.sqrt(2)
POH_S, POH_SIGMA = 2.82759, 0.00051


def load_checks():
    spec = importlib.util.spec_from_file_location("s_of_n", HERE / "checks" / "s_of_n.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def style(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelcolor=INK)
    ax.grid(axis="y", color=PALE, linewidth=0.6)
    ax.set_axisbelow(True)


def figure_mach_zehnder(summary: dict, output: Path) -> None:
    worlds = list(summary["mach_zehnder"].keys())
    labels = {
        "mz_equal": "equal arms",
        "mz_half": "half turn",
        "mz_quarter": "quarter turn",
        "mz_balanced": "(1, 1) split",
        "mz_345": "(3, 4) split",
        "mz_unequal_f0": "unequal, f = 0",
        "mz_unequal_f8": "unequal, f = 8",
        "mz_unequal_f16": "unequal, f = 16",
        "ev_29": "EV (20, 21)",
        "ev_169": "EV (119, 120)",
    }
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    x = range(len(worlds))
    width = 0.27
    series = ((-width, "D1", INK, None), (0, "D2", WHITE, "////"), (width, "absorber", LIGHT, None))
    for offset, channel, fill, hatch in series:
        values = [summary["mach_zehnder"][w]["clicks"].get(channel, 0) for w in worlds]
        ax.bar(
            [i + offset for i in x],
            values,
            width=width * 0.92,
            color=fill,
            edgecolor=INK,
            linewidth=0.6,
            hatch=hatch,
            label=channel,
        )
    ax.set_xticks(list(x), [labels[w] for w in worlds], rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("clicks over 64 births")
    ax.set_ylim(0, 66)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper right")
    style(ax)
    fig.tight_layout()
    fig.savefig(output / "mach_zehnder.pdf")
    plt.close(fig)


def figure_two_slits(summary: dict, output: Path) -> None:
    slits = summary["two_slits"]
    ys = sorted(int(k.split("_")[1]) for k in slits["weights"] if k.startswith("screen_"))
    weights = [float(Fraction(slits["weights"][f"screen_{y}"])) for y in ys]
    total = sum(weights)
    clicks = [slits["clicks"].get(f"screen_{y}", 0) for y in ys]
    alone = [slits["screen_alone"].get(f"screen_{y}", 0) for y in ys]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 4.2), sharex=True)
    ax1.bar(ys, [w / total for w in weights], width=1.0, color=LIGHT, edgecolor=INK, linewidth=0.4)
    ax1.set_ylabel("record's weight\n(share of the screen)")
    ax2.bar(
        [y - 0.22 for y in ys],
        clicks,
        width=0.44,
        color=INK,
        edgecolor=INK,
        linewidth=0.4,
        label="clicks, 64 births",
    )
    ax2.bar(
        [y + 0.22 for y in ys],
        alone,
        width=0.44,
        color=WHITE,
        edgecolor=INK,
        linewidth=0.6,
        hatch="////",
        label="screen-conditioned histogram",
    )
    ax2.set_ylabel("clicks")
    ax2.set_xlabel("pixel y")
    ax2.legend(frameon=False, fontsize=8)
    for ax in (ax1, ax2):
        style(ax)
    fig.tight_layout()
    fig.savefig(output / "two_slits.pdf")
    plt.close(fig)


def figure_pair(summary: dict, checks, output: Path) -> None:
    n = 64
    c_n = checks.phase_cosines(n)
    diffs = list(range(n))
    computed = [float(checks.counts(n, d, 0)[1]) for d in diffs]
    table = [c_n[d] / 256 for d in diffs]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.plot(diffs, table, color=MID, linewidth=1.2, linestyle="--", label="table cosine C[a - b] / 256")
    ax.step(
        diffs,
        computed,
        where="mid",
        color=INK,
        linewidth=1.4,
        label="E computed from the rule (all a - b)",
    )
    measured = []
    for world, entry in summary["pair"]["64"]["worlds"].items():
        a, b = (int(part) for part in world.split("_")[1:3])
        measured.append(((a - b) % n, float(Fraction(entry["E"]))))
    ax.scatter(
        [d for d, _ in measured],
        [e for _, e in measured],
        s=46,
        color=INK,
        marker="o",
        zorder=3,
        label="CHSH worlds, registered",
    )
    chooser = []
    for key, entry in summary["choosers"].items():
        if entry["E"] is None:
            continue
        a, b = (int(part) for part in key.split("_"))
        chooser.append(((a - b) % n, float(Fraction(entry["E"]))))
    ax.scatter(
        [d for d, _ in chooser],
        [e for _, e in chooser],
        s=30,
        facecolors=WHITE,
        edgecolors=INK,
        linewidths=1.0,
        marker="s",
        zorder=4,
        label="choosers' bins, registered",
    )
    ax.set_xlabel("a - b (steps of the circle, N = 64)")
    ax.set_ylabel("E(a, b)")
    ax.set_xlim(0, n - 1)
    ax.legend(frameon=False, fontsize=8, loc="upper center")
    style(ax)
    fig.tight_layout()
    fig.savefig(output / "pair_64.pdf")
    plt.close(fig)


def figure_s_of_n(summary: dict, checks, output: Path) -> None:
    ns = [64, 256, 512, 1024, 2048, 4096, 8192]  # the registered and computed powers of two only
    values = [float(checks.chsh(n)[0]) for n in ns]
    runs = [(int(n), entry["S_float"]) for n, entry in summary["pair"].items()]
    fig, (ax, zoom) = plt.subplots(1, 2, figsize=(7.2, 3.2), gridspec_kw={"width_ratios": [1.15, 1]})
    for axis, lo, hi, ylim in ((ax, 64, 8192, (2.70, 2.86)), (zoom, 512, 8192, (2.820, 2.837))):
        axis.axhline(TSIRELSON, color=INK, linewidth=1.0, linestyle="--", label="2 sqrt 2")
        axis.axhspan(
            POH_S - 3 * POH_SIGMA,
            POH_S + 3 * POH_SIGMA,
            color=PALE,
            linewidth=0,
            label="Poh et al. 2015, 3 sigma",
        )
        pts = [(n, s) for n, s in zip(ns, values, strict=True) if lo <= n <= hi]
        axis.scatter(
            [n for n, _ in pts],
            [s for _, s in pts],
            s=7,
            color=DARK,
            linewidth=0,
            label="S(N) computed from the rule",
        )
        rp = [(n, s) for n, s in runs if lo <= n <= hi]
        axis.scatter(
            [n for n, _ in rp],
            [s for _, s in rp],
            s=70,
            facecolors="none",
            edgecolors=INK,
            linewidths=1.6,
            zorder=4,
            label="engine runs",
        )
        axis.set_xscale("log", base=2)
        axis.set_ylim(*ylim)
        axis.set_xlabel("N (the circle's steps)")
        style(axis)
    ax.set_ylabel("S at the CHSH labels")
    ax.legend(frameon=False, fontsize=7, loc="lower right")
    zoom.set_title("N from 512 to 8192", fontsize=9, color=INK)
    fig.tight_layout()
    fig.savefig(output / "s_of_n.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--summary", type=Path, default=HERE / "figures" / "summary.json")
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    parser.add_argument("--png", type=Path, default=None, help="also write PNG previews here")
    args = parser.parse_args()
    if args.png is not None:
        args.png.mkdir(parents=True, exist_ok=True)
        original = plt.Figure.savefig

        def save_both(fig, path, *rest, **options):
            original(fig, path, *rest, **options)
            original(fig, args.png / (Path(path).stem + ".png"), dpi=150)

        plt.Figure.savefig = save_both  # type: ignore[method-assign]
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    checks = load_checks()
    args.output.mkdir(parents=True, exist_ok=True)
    figure_mach_zehnder(summary, args.output)
    figure_two_slits(summary, args.output)
    figure_pair(summary, checks, args.output)
    figure_s_of_n(summary, checks, args.output)
    print("wrote", sorted(p.name for p in args.output.glob("*.pdf")))


if __name__ == "__main__":
    main()
