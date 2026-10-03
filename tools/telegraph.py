"""The telegraph's reader (examples/events/shelved_ion; ALGEBRA.md, The click writes on the GameBoard (j), the shelved ion's telegraph as three clicks): a run's output file read against the blind expectation file, every number from the `credit` lines of the counter (the clicks) and the `credit` lines of the record declared an instrument (its clicks, the lines naming `taken` or `given`), nothing from the arrays. The counts per bin: the counter's `credit` lines of the blind's family within the window, one count each, summed per window of `bin` intervals; a bin with 0 counts is dark and a bin with 1 or more bright (the blind's rule); the bright bins' mean and variance (Poisson: the variance the mean); the bright and the dark periods, runs of bins of one kind, the first and the last period dropped as cut by the window, their lengths in intervals, their means and the standard deviation over the mean (1 for an exponential); the dark fraction; the histogram of the counts per bin; the switches, the periods of each kind; the returns, the counter's `credit` lines of the family the design names as the return's row; the record's clicks per kind from its `credit` lines labelled DETECTOR (the part realised, the family taken from or given to; the null window's GAMEBOARD-labelled lines left out), the fluorescence givings' spacing; the intervals the run reached (a run refused inside names its interval). The tool holds no number of the law and compares nothing: the blind is printed beside each reading.

Run with the checkout's root as the working directory:

    python tools/telegraph.py --output runs/shelved_ion.output.json --expectation examples/events/shelved_ion/expectation.json
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import Counter
from pathlib import Path


def bins(
    lines: list[dict[str, object]],
    detectors: list[str],
    family: str,
    window: tuple[int, int],
    width: int,
) -> list[int]:
    """The counts per bin: the counter's credit lines of the family within the window, summed per window of `width` intervals (the bin of the credit at the tick t is (t - first) div width)."""
    first, last = window
    found = [0] * ((last - first) // width + 1)
    for line in lines:
        if (
            line.get("event") != "credit"
            or line.get("family") != family
            or line.get("detector") not in detectors
        ):
            continue
        tick = int(str(line["tick"]))
        if first <= tick <= last:
            found[(tick - first) // width] += int(str(line["count"]))
    return found


def periods(counts: list[int], bright: bool) -> list[int]:
    """The runs of bright (count above 0) or dark (count 0) bins, in bins, the first and the last run of the window dropped as cut."""
    kinds = [c > 0 for c in counts]
    runs: list[tuple[bool, int]] = []
    for kind in kinds:
        if runs and runs[-1][0] == kind:
            runs[-1] = (kind, runs[-1][1] + 1)
        else:
            runs.append((kind, 1))
    inner = runs[1:-1]
    return [length for kind, length in inner if kind == bright]


def shape(values: list[float]) -> dict[str, float | int | None]:
    """A sample's size, mean, standard deviation over the mean (1 for an exponential) and variance over the mean (1 for a Poisson)."""
    if not values:
        return {"n": 0, "mean": None, "sd_over_mean": None, "variance_over_mean": None}
    mean = statistics.mean(values)
    sd = statistics.pstdev(values) if len(values) > 1 else 0.0
    return {
        "n": len(values),
        "mean": round(mean, 3),
        "sd_over_mean": round(sd / mean, 3) if mean else None,
        "variance_over_mean": round(sd * sd / mean, 3) if mean else None,
    }


def reading(output: Path, expectation: Path) -> dict[str, object]:
    """The telegraph read from the output's lines against the blind (`expectation.json`): the rows 1 to 7 and 9's click half, each beside the blind's sentence."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    document = json.loads(output.read_text(encoding="utf-8"))
    lines = document["lines"]
    detectors = [str(d) for d in expected["detector"]]
    family, width = str(expected["family"]), int(expected["bin"])
    reached = int(document.get("ticks") or 0)
    reason = str(document.get("reason", ""))
    if not reached and (found := re.search(r"interval (\d+)", reason)):
        reached = int(found.group(1))
    window = (int(expected["window"][0]), min(int(expected["window"][1]), reached))
    counts = bins(lines, detectors, family, window, width)
    bright = [c for c in counts if c > 0]
    bright_periods = [p * width for p in periods(counts, True)]
    dark_periods = [p * width for p in periods(counts, False)]
    clicks = [
        line
        for line in lines
        if line.get("event") == "credit"
        and line.get("label") == "DETECTOR"
        and (line.get("taken") or line.get("given"))
    ]  # the record's own clicks: the takings and the givings
    kinds = Counter((str(j["realised"]), str(j.get("taken") or j.get("given"))) for j in clicks)
    givings = [int(str(j["tick"])) for j in clicks if j.get("given") == family]
    gaps = [b - a for a, b in zip(givings, givings[1:], strict=False)]
    returns = [
        line
        for line in lines
        if line.get("event") == "credit"
        and line.get("family") != family
        and line.get("detector") in detectors
    ]
    blind = expected["blind"]
    return {
        "verdict": document["verdict"],
        "reason": reason or None,
        "intervals_reached": reached,
        "window_read": list(window),
        "bins": len(counts),
        "counts_per_bin": counts,
        "1_bright_bins": {
            "reading": shape([float(c) for c in bright]),
            "blind": blind["1_bright_bins_poisson"]["blind"],
        },
        "2_bright_periods": {
            "reading": shape([float(p) for p in bright_periods]),
            "blind": blind["2_bright_periods_exponential"]["blind"],
        },
        "3_dark_periods": {
            "reading": shape([float(p) for p in dark_periods]),
            "blind": blind["3_dark_periods_exponential"]["blind"],
        },
        "4_dark_fraction": {
            "reading": round(sum(1 for c in counts if c == 0) / len(counts), 4) if counts else None,
            "blind": blind["4_dark_fraction"]["blind"],
        },
        "5_histogram": {
            "reading": dict(sorted(Counter(counts).items())),
            "blind": blind["5_bimodal"]["blind"],
        },
        "6_switches": {
            "reading": {"bright": len(bright_periods), "dark": len(dark_periods)},
            "blind": blind["6_switches"]["blind"],
        },
        "7_returns": {
            "reading": Counter(str(r["family"]) for r in returns),
            "blind": blind["7_returns"]["blind"],
        },
        "record_clicks": {f"{realised} by {family}": n for (realised, family), n in kinds.items()},
        "givings_of_the_family": {"n": len(givings), "spacing": shape([float(g) for g in gaps])},
        "label": "DETECTOR",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, required=True, help="the run's output file")
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    args = parser.parse_args(argv)
    print(json.dumps(reading(args.output, args.expectation), indent=1))


if __name__ == "__main__":
    main()
