"""Figure: Bell's cells at N = 64 and the plateau of S(N) (series L3, L6, 24.4; DETECTOR).

The paper (NATURE row 1a; Theorem on CHSH; Figure S(N)): the cells 27, 5,
5, 27 per setting pair over 64 births, S = 2.75 = 176 / 64 at N = 64; the
plateau S = 181 / 64 at N = 512, 2048, 4096, 8192 and 5793 / 2048 at 16384.
Read from the gather lines of the four worlds per N: the two outcomes per
birth ordinal 1 .. N; E in counts per pair; S N = E(a, b) - E(a, b') +
E(a', b) + E(a', b') (the register's `chsh_S`, `S_times_N`).
"""

from __future__ import annotations

from fractions import Fraction

import matplotlib.pyplot as plt
from common import (
    DETECTOR,
    INK,
    LIGHT,
    MID,
    PALE,
    arguments,
    cost,
    fingerprint,
    fmt,
    run_folder,
    save,
    style,
)
from gathers import correlation, outcome_counts

PARTIES = ("alice_plus", "bob_plus")
# (N, the four worlds in the order a b, a b', a' b, a' b'), the register's names.
LADDER = (
    (64, ("bell_0_8", "bell_0_24", "bell_16_8", "bell_16_24")),
    (512, ("bell_n512_0_64", "bell_n512_0_192", "bell_n512_128_64", "bell_n512_128_192")),
    (2048, ("bell_n2048_0_256", "bell_n2048_0_768", "bell_n2048_512_256", "bell_n2048_512_768")),
    (4096, ("bell_n4096_0_512", "bell_n4096_0_1536", "bell_n4096_1024_512", "bell_n4096_1024_1536")),
    (8192, ("bell_n8192_0_1024", "bell_n8192_0_3072", "bell_n8192_2048_1024", "bell_n8192_2048_3072")),
    (
        16384,
        ("bell_n16384_0_2048", "bell_n16384_0_6144", "bell_n16384_4096_2048", "bell_n16384_4096_6144"),
    ),
)
PAPER = {
    64: Fraction(176, 64),
    512: Fraction(181, 64),
    2048: Fraction(181, 64),
    4096: Fraction(181, 64),
    8192: Fraction(181, 64),
    16384: Fraction(5793, 2048),
}
CELLS = ("++", "+-", "-+", "--")


def main() -> None:
    runs, out = arguments()
    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw={"width_ratios": [1.3, 1]})
    s_of_n: dict[int, Fraction] = {}
    for n, worlds in LADDER:
        signs = (1, -1, 1, 1)
        total = 0
        counts_all = []
        for world, sign in zip(worlds, signs, strict=True):
            try:
                folder = run_folder(runs, "amplitude", world)
            except SystemExit as missing:
                print(f"missing {missing}")
                counts_all = []
                break
            counts = outcome_counts(folder, n, PARTIES)
            counts_all.append((world, counts, fingerprint(folder), cost(folder)))
            total += sign * correlation(counts)
        if not counts_all:
            continue
        s_of_n[n] = Fraction(total, n)
        for world, counts, fp, host in counts_all:
            print(
                f"{DETECTOR} N = {n} {world}: "
                + ", ".join(f"{c} {counts[c]}" for c in CELLS)
                + f"; E {correlation(counts)}; fingerprint {fp}; {host}"
            )
        print(f"{DETECTOR} N = {n}: S = {fmt(s_of_n[n])}; the paper's {fmt(PAPER[n])}")
        if n == 64:
            x = 0
            for world, counts, _, _ in counts_all:
                values = [counts[c] for c in CELLS]
                left.bar(
                    [x + i for i in range(4)], values, color=[INK, LIGHT, LIGHT, INK], edgecolor=INK
                )
                for i, v in enumerate(values):
                    left.text(x + i, v + 0.6, str(v), ha="center", fontsize=8)
                left.text(x + 1.5, -9, world.replace("bell_", ""), ha="center", fontsize=8)
                x += 5
            left.set_xticks([i + 5 * j for j in range(4) for i in range(4)])
            left.set_xticklabels(CELLS * 4, fontsize=7)
            left.set_ylim(0, 36)
            left.set_ylabel("clicks per cell over 64 births (DETECTOR)")
            left.set_title(
                "N = 64: the four cells per setting pair (a, b); S = 176/64 pinned", fontsize=9
            )
            style(left)
    ns = sorted(s_of_n)
    right.axhline(2 * 2**0.5, color=MID, ls=":", lw=1, label="2 sqrt 2 (drawn, not read)")
    right.axhline(float(Fraction(181, 64)), color=PALE, lw=6, label="181/64, the paper's plateau")
    right.plot(ns, [float(s_of_n[n]) for n in ns], "o", color=INK, label="S read (DETECTOR)")
    right.plot(
        ns, [float(PAPER[n]) for n in ns], "s", mfc="none", mec=INK, ms=10, label="the paper's value"
    )
    for n in ns:
        right.annotate(
            f"{s_of_n[n].numerator}/{s_of_n[n].denominator}",
            (n, float(s_of_n[n])),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=7,
        )
    right.set_xscale("log", base=2)
    right.set_xticks(ns)
    right.set_xticklabels([str(n) for n in ns], fontsize=8)
    right.set_xlabel("N (the phase circle)")
    right.set_ylabel("S")
    right.set_ylim(2.7, 2.9)
    right.legend(fontsize=7, loc="lower right")
    right.set_title("S(N) from the four worlds' cells", fontsize=9)
    style(right)
    fig.suptitle("Bell: the cells and the plateau (DETECTOR: the gather lines' outcomes)", fontsize=10)
    save(fig, out, "fig_bell_cells")


if __name__ == "__main__":
    main()
