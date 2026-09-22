"""Figure: the Mach-Zehnder ports over the first 64 births (series L1, DETECTOR).

The paper (NATURE row 2b; "the seven confirmations"): `mz_equal` 64 / 0,
`mz_half` 0 / 64, `mz_quarter` 32 / 32 over 64 births. Read from the
gather lines: the set chosen per birth ordinal 1 .. 64.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from common import DETECTOR, INK, LIGHT, MID, arguments, cost, fingerprint, run_folder, save, style
from gathers import chosen_by_ordinal

BIRTHS = 64
WORLDS = (
    ("mz_equal", "equal arms", (64, 0)),
    ("mz_half", "half turn", (0, 64)),
    ("mz_quarter", "quarter turn", (32, 32)),
)


def main() -> None:
    runs, out = arguments()
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    for ax, (world, label, expected) in zip(axes, WORLDS, strict=True):
        folder = run_folder(runs, "amplitude", world)
        chosen = chosen_by_ordinal(folder, BIRTHS)
        d1 = sum(1 for c in chosen.values() if c[0][0] == "D1")
        d2 = sum(1 for c in chosen.values() if c[0][0] == "D2")
        print(
            f"{DETECTOR} {world}: D1 {d1}, D2 {d2} over {len(chosen)} births read; expected {expected}; "
            f"fingerprint {fingerprint(folder)}; {cost(folder)}"
        )
        bars = ax.bar(["D1", "D2"], [d1, d2], color=[INK, LIGHT], edgecolor=INK, width=0.6)
        for bar, value in zip(bars, (d1, d2), strict=True):
            ax.text(bar.get_x() + bar.get_width() / 2, value + 1, str(value), ha="center", color=INK)
        ax.plot([-0.3, 0.3], [expected[0]] * 2, ls="--", color=MID, lw=1)
        ax.plot([0.7, 1.3], [expected[1]] * 2, ls="--", color=MID, lw=1)
        ax.set_title(f"{world} ({label})", fontsize=10)
        ax.set_ylim(0, 72)
        style(ax)
    axes[0].set_ylabel("clicks over 64 births (DETECTOR)")
    fig.suptitle(
        "Mach-Zehnder: the port chosen per record, first 64 births; dashes the paper's 64/0, 0/64, 32/32",
        fontsize=10,
    )
    save(fig, out, "fig_mach_zehnder")


if __name__ == "__main__":
    main()
