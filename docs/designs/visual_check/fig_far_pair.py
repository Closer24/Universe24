"""Figure: the far pair, the cells 27, 5, 5, 27 with Bob's counters 116 Links farther (series L3; DETECTOR).

The paper ("the seven confirmations": "the far pair's cells 27, 5, 5, 27";
the far world `bell_16_24_far`, 300 intervals, "no maintenance"). Read
from the gather lines of `bell_16_24` and `bell_16_24_far`: the cells over
birth ordinals 1 .. 64 and the tick of each record's completion.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from common import DETECTOR, INK, LIGHT, MID, arguments, cost, fingerprint, run_folder, save, style
from gathers import gather_ticks, outcome_counts

BIRTHS = 64
PARTIES = ("alice_plus", "bob_plus")
CELLS = ("++", "+-", "-+", "--")


def main() -> None:
    runs, out = arguments()
    fig, (left, right) = plt.subplots(1, 2, figsize=(10, 3.4))
    for i, (world, label) in enumerate(
        (("bell_16_24", "near: Bob at 17, 18"), ("bell_16_24_far", "far: Bob at 133, 134"))
    ):
        folder = run_folder(runs, "amplitude", world)
        counts = outcome_counts(folder, BIRTHS, PARTIES)
        ticks = gather_ticks(folder, BIRTHS)
        print(
            f"{DETECTOR} {world}: "
            + ", ".join(f"{c} {counts[c]}" for c in CELLS)
            + f"; completions from tick {min(ticks.values())} to {max(ticks.values())}; "
            f"fingerprint {fingerprint(folder)}; {cost(folder)}"
        )
        values = [counts[c] for c in CELLS]
        left.bar([j + 5 * i for j in range(4)], values, color=[INK, LIGHT, LIGHT, INK], edgecolor=INK)
        for j, v in enumerate(values):
            left.text(j + 5 * i, v + 0.6, str(v), ha="center", fontsize=8)
        left.text(1.5 + 5 * i, -5, label, ha="center", fontsize=8)
        right.plot(
            sorted(ticks),
            [ticks[n] for n in sorted(ticks)],
            "o" if i == 0 else "s",
            mfc=INK if i == 0 else "none",
            mec=INK,
            ms=4,
            label=label,
        )
    left.plot([-0.4, 8.4], [27, 27], ls="--", color=MID, lw=1)
    left.plot([-0.4, 8.4], [5, 5], ls="--", color=MID, lw=1)
    left.set_xticks([j + 5 * i for i in range(2) for j in range(4)])
    left.set_xticklabels(CELLS * 2)
    left.set_ylim(0, 33)
    left.set_ylabel("clicks per cell over 64 births (DETECTOR)")
    left.set_title("the cells at the setting pair (16, 24); dashes the paper's 27, 5, 5, 27", fontsize=9)
    style(left)
    right.set_xlabel("birth ordinal")
    right.set_ylabel("the completion's tick (DETECTOR)")
    right.legend(fontsize=8)
    right.set_title("the record's one click completes at the far arm's arrival", fontsize=9)
    style(right)
    save(fig, out, "fig_far_pair")


if __name__ == "__main__":
    main()
