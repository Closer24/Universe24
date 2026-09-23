"""Figure: GHZ, the four allowed triples 16 each and the products (series L4; DETECTOR).

The paper ("the seven confirmations"): the four allowed triples 16 each,
the products +1 (xxx) and -1 (xyy, yxy, yyx), the other triples 0; yyy
every triple 8. Read from the gather lines: the three outcomes per birth
ordinal 1 .. 64.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from common import DETECTOR, INK, LIGHT, arguments, cost, fingerprint, run_folder, save, style
from gathers import outcome_counts

BIRTHS = 64
WORLDS = ("ghz_xxx", "ghz_xyy", "ghz_yxy", "ghz_yyx", "ghz_yyy")
TRIPLES = ("+++", "++-", "+-+", "+--", "-++", "-+-", "--+", "---")


def product(triple: str) -> int:
    return (-1) ** triple.count("-")


def main() -> None:
    runs, out = arguments()
    fig, axes = plt.subplots(1, 5, figsize=(13, 3), sharey=True)
    for ax, world in zip(axes, WORLDS, strict=True):
        folder = run_folder(runs, "amplitude", world)
        counts = outcome_counts(folder, BIRTHS, ("a", "b", "c"))
        products = sorted({product(t) for t in TRIPLES if counts[t] > 0})
        print(
            f"{DETECTOR} {world}: "
            + ", ".join(f"{t} {counts[t]}" for t in TRIPLES)
            + f"; products seen {products}; fingerprint {fingerprint(folder)}; {cost(folder)}"
        )
        values = [counts[t] for t in TRIPLES]
        ax.bar(
            range(8), values, color=[INK if product(t) == 1 else LIGHT for t in TRIPLES], edgecolor=INK
        )
        for i, v in enumerate(values):
            if v:
                ax.text(i, v + 0.5, str(v), ha="center", fontsize=7)
        ax.set_xticks(range(8))
        ax.set_xticklabels(TRIPLES, fontsize=6, rotation=60)
        ax.set_title(f"{world}: products {products}", fontsize=9)
        ax.set_ylim(0, 20)
        style(ax)
    axes[0].set_ylabel("clicks over 64 births (DETECTOR)")
    fig.suptitle("GHZ: the triple chosen per birth (black: product +1; grey: product -1)", fontsize=10)
    save(fig, out, "fig_ghz")


if __name__ == "__main__":
    main()
