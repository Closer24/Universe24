"""Figure: one opening, the reference `slits_one` (series L2's control; DETECTOR).

The register: `slits_one` is the two-slit geometry with one opening, one
birth of the lamp, its rows declared as rays of amount 91 per fan
direction, the screen reading the age: "the record without the
two-source term", the reference of `slits_low`. Read from the click lines
of the screen's pixels: the clicks per pixel and the age each carries.
The paper's row 10 (the single-opening spread against 0.886) has no
completed registered run under the click (NATURE row 10, NOT YET); this
figure is the two-slit reference, not row 10.
"""

from __future__ import annotations

from collections import Counter

import matplotlib.pyplot as plt
from common import (
    DETECTOR,
    INK,
    arguments,
    cost,
    events,
    fingerprint,
    fmt,
    mean,
    run_folder,
    save,
    style,
)

from event_universe.trimmed_record import refuse_trimmed_record


def main() -> None:
    runs, out = arguments()
    folder = run_folder(runs, "amplitude", "slits_one")
    counts: Counter = Counter()
    ages: dict[int, list[int]] = {}
    refuse_trimmed_record(folder)
    for line in events(folder, {"click"}):
        detector = line.get("detector") or ""
        if detector.startswith("screen_"):
            y = int(detector.split("_")[1])
            counts[y] += 1
            ages.setdefault(y, []).append(int(line["reading"]))
    print(
        f"{DETECTOR} slits_one: {sum(counts.values())} screen clicks on {len(counts)} pixels, y from {min(counts)} to {max(counts)}; "
        f"the counts y = 40 .. 80: " + " ".join(str(counts[y]) for y in range(40, 81))
    )
    all_ages = [a for v in ages.values() for a in v]
    print(
        f"{DETECTOR} slits_one: the age read at the click from {min(all_ages)} to {max(all_ages)} intervals, mean {fmt(mean(all_ages))}; "
        f"fingerprint {fingerprint(folder)}; {cost(folder)}"
    )
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(11, 5), sharex=True)
    top.bar(list(counts), [counts[y] for y in counts], color=INK, width=0.8)
    top.set_ylabel("clicks per pixel (DETECTOR)")
    top.set_title(
        "slits_one: one opening, one birth, the rows' clicks per screen pixel (the register's reference)",
        fontsize=9,
    )
    style(top)
    ys = sorted(ages)
    bottom.plot(ys, [float(mean(ages[y])) for y in ys], "o", color=INK, ms=3)
    bottom.set_ylabel("mean age at the click (DETECTOR)")
    bottom.set_xlabel("screen pixel y")
    bottom.set_xlim(-1, 121)
    style(bottom)
    save(fig, out, "fig_one_slit")


if __name__ == "__main__":
    main()
