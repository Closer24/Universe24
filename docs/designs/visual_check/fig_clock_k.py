"""Figure: the clock's k inside a shell of sources (series X, Poisson after a detector; DETECTOR).

The paper (the conversion table): "series X k = 0.9089 at r = 4 for the
pin 0.9108". Read from the detector's click lines of `shell_clock/age_4`
and its control `control_4`: the birth ordinal against the click's tick;
in the two windows 200 .. 350 and 350 .. 500, 1 + z the inverse slope, k = z.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from clock_reading import clicks, one_plus_z
from common import DETECTOR, INK, LIGHT, MID, arguments, cost, fingerprint, fmt, run_folder, save, style

WINDOWS = ((200, 350), (350, 500))
PIN = "0.910783 in [0.8197, 1.0019]"


def main() -> None:
    runs, out = arguments()
    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.8))
    for world, marker, colour in (("age_4", "o", INK), ("control_4", "s", MID)):
        folder = run_folder(runs, "shell_clock", world)
        found = clicks(folder)
        ks = []
        for window in WINDOWS:
            value, n = one_plus_z(found, window)
            ks.append(value - 1)
            print(
                f"{DETECTOR} shell_clock/{world} window {window}: {n} clicks, 1 + z = {fmt(value)}, k = {fmt(value - 1)}"
                + (f"; the pin k {PIN}, the paper's 0.9089" if world == "age_4" else "")
            )
        ages = sorted({a for _, _, a in found})
        print(
            f"{DETECTOR} shell_clock/{world}: {len(found)} clicks, ordinals {found[0][1]} .. {found[-1][1]}, the age at the click {ages[0]} .. {ages[-1]}; "
            f"fingerprint {fingerprint(folder)}; {cost(folder)}"
        )
        left.plot(
            [t for t, _, _ in found],
            [o for _, o, _ in found],
            marker,
            color=colour,
            ms=2,
            label=f"{world} (k = {float(ks[0]):.4f}, {float(ks[1]):.4f})",
        )
        right.bar(
            [
                0 + (0.4 if world.startswith("control") else 0),
                1 + (0.4 if world.startswith("control") else 0),
            ],
            [float(k) for k in ks],
            width=0.4,
            color=colour if world == "age_4" else LIGHT,
            edgecolor=INK,
            label=world,
        )
    for window in WINDOWS:
        left.axvline(window[0], color=LIGHT, lw=1)
    left.axvline(500, color=LIGHT, lw=1)
    left.set_xlabel("the click's tick")
    left.set_ylabel("birth ordinal of the record clicked (DETECTOR)")
    left.legend(fontsize=7, loc="upper left")
    left.set_title(
        "the lamp's records arriving at the detector; the slope's inverse is 1 + z", fontsize=9
    )
    style(left)
    right.axhline(0.910783, color=MID, ls="--", lw=1, label="the pin 0.9108")
    right.axhspan(0.8197, 1.0019, color=LIGHT, alpha=0.4, label="the pin's bracket")
    right.set_xticks([0.2, 1.2])
    right.set_xticklabels(["window 200 .. 350", "window 350 .. 500"])
    right.set_ylabel("k = z (DETECTOR)")
    right.legend(fontsize=7)
    right.set_title("k inside the shell at r = 4 against its control", fontsize=9)
    style(right)
    fig.suptitle("The clock's k after a detector (series X)", fontsize=10)
    save(fig, out, "fig_clock_k")


if __name__ == "__main__":
    main()
