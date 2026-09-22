"""Figure: Malus's law after the click (A12 under the click; NATURE row 9; DETECTOR).

The paper: 128 of 256 at 45 degrees (`malus_a`), 0 of 256 at 90 degrees
(`malus_b`), 219 of 256 at 22.5 degrees (`malus_22_5`). Read from the
gather lines: the second polariser's outcome per birth ordinal 1 .. 256.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from common import DETECTOR, INK, LIGHT, MID, arguments, cost, fingerprint, run_folder, save, style
from gathers import chosen_by_ordinal

BIRTHS = 256
WORLDS = (
    ("malus_a", "45 degrees (window 64)", 128),
    ("malus_b", "90 degrees (window 128)", 0),
    ("malus_22_5", "22.5 degrees (window 32)", 219),
)


def main() -> None:
    runs, out = arguments()
    fig, ax = plt.subplots(figsize=(7, 3.4))
    for i, (world, _label, expected) in enumerate(WORLDS):
        folder = run_folder(runs, "amplitude", world)
        chosen = chosen_by_ordinal(folder, BIRTHS)
        outcome = {n: [c[2] for c in ch if c[0] == "second"][0] for n, ch in chosen.items()}
        plus = sum(1 for o in outcome.values() if o == "+")
        minus = sum(1 for o in outcome.values() if o == "-")
        print(
            f"{DETECTOR} {world}: transmitted (+) {plus}, absorbed (-) {minus} of {len(outcome)} births; "
            f"the paper's {expected} of 256; fingerprint {fingerprint(folder)}; {cost(folder)}"
        )
        ax.bar(
            i - 0.2,
            plus,
            width=0.4,
            color=INK,
            edgecolor=INK,
            label="transmitted (+)" if i == 0 else None,
        )
        ax.bar(
            i + 0.2,
            minus,
            width=0.4,
            color=LIGHT,
            edgecolor=INK,
            label="absorbed (-)" if i == 0 else None,
        )
        ax.text(i - 0.2, plus + 4, str(plus), ha="center", fontsize=9)
        ax.text(i + 0.2, minus + 4, str(minus), ha="center", fontsize=9)
        ax.plot([i - 0.4, i], [expected] * 2, ls="--", color=MID, lw=1)
    ax.set_xticks(range(len(WORLDS)))
    ax.set_xticklabels([f"{w}\n{angle}" for w, angle, _ in WORLDS], fontsize=8)
    ax.set_ylim(0, 280)
    ax.set_ylabel("clicks over 256 births (DETECTOR)")
    ax.legend(fontsize=8, loc="upper center")
    ax.set_title(
        "Malus after the click: the second polariser's outcome per birth; dashes the paper's 128, 0, 219 of 256",
        fontsize=9,
    )
    style(ax)
    save(fig, out, "fig_malus")


if __name__ == "__main__":
    main()
