"""The joint-gather readings of the Bell and Malus rows under the local detector law.

Reads the run folders of the GO worlds `bell_a0b0`, `bell_a0b1`, `bell_a1b0`,
`bell_a1b1` (DECLARATIONS.md sections 1 and 2, rows 1a to 1d) and
`malus_<angle>` (sections 5 and 6, row 9) written by the runner (`run.json`,
`initialization.json`, `events.jsonl`) and prints, per run, the counts of
the joint cells of the pair's ONE gather (section 1 item 3: the chosen joint
cell [[alice, o_A, "0"], [bob, o_B, "0"]] on every gather line, o = 0 the +
channel and 1 the - channel of the table body of two cells, section 14 item
6), the correlation E = (n++ + n-- - n+- - n-+) / n and the marginals of
each side (the + channel's share), and, over the four runs, the CHSH sum S
= E(a, b) - E(a, b') + E(a', b) + E(a', b') with the settings read from the
worlds (a = the smaller of Alice's two, b the smaller of Bob's); for a
Malus run (one table body) the + channel's count and share. Every number
is on integers and `fractions.Fraction`, no float. The clicks are
DETECTOR readings; E, the marginals and S are COMPUTATION; the pins are the
series' `expectations.json` (the generator's `bell.py`), which this reader
does not move: it prints the readings for the comparison.

    PYTHONPATH=src python tools/click_readings/detector_law_bell.py artifacts/bell_a0b0 ...
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.world_loading import world_of_run  # noqa: E402

PLUS = 0
MINUS = 1


@dataclass
class Reading:
    """One run's reading: the tables' names and settings in the sets' order,
    the counts per joint cell (the channels in that order), the gathers."""

    folder: str
    names: list[str]
    settings: list[int]
    counts: dict[tuple[int, ...], int]
    gathers: int
    escaped: int

    @property
    def total(self) -> int:
        return sum(self.counts.values())

    def marginal(self, side: int) -> Fraction:
        """The + channel's share on one side (0 the first table)."""
        plus = sum(count for cell, count in self.counts.items() if cell[side] == PLUS)
        return Fraction(plus, self.total) if self.total else Fraction(0)

    @property
    def correlation(self) -> Fraction:
        """E over two tables: the same channels less the different ones."""
        same = self.counts.get((PLUS, PLUS), 0) + self.counts.get((MINUS, MINUS), 0)
        different = self.counts.get((PLUS, MINUS), 0) + self.counts.get((MINUS, PLUS), 0)
        return Fraction(same - different, self.total) if self.total else Fraction(0)


def settings_of(world: dict[str, Any]) -> dict[str, int]:
    """The setting of each table body named by a detector set of one Node."""
    tables = {tuple(entry["position"]): entry.get("table", {}) for entry in world["measured"]}
    found: dict[str, int] = {}
    for detector in world["detectors"]:
        if len(detector.get("positions", [])) != 1:
            continue
        (position,) = detector["positions"]
        for entry in tables.get(tuple(position), {}).values():
            if isinstance(entry, dict) and isinstance(entry.get("phase_window"), int):
                found[str(detector["name"])] = int(entry["phase_window"])
    return found


def counts_of(gathers: list[dict[str, Any]], names: list[str]) -> tuple[dict[tuple[int, ...], int], int]:
    """The counts per joint cell from the gather lines' chosen cells (the
    channels in the tables' order) and the gathers with no cell (escaped)."""
    found: dict[tuple[int, ...], int] = {}
    escaped = 0
    for gather in gathers:
        chosen = gather.get("chosen")
        if not chosen:
            escaped += 1
            continue
        by_name = {str(cell[0]): int(cell[1]) for cell in chosen}
        if set(by_name) != set(names):
            escaped += 1
            continue
        key = tuple(by_name[name] for name in names)
        found[key] = found.get(key, 0) + 1
    return found, escaped


def read_run(folder: Path) -> Reading:
    world = world_of_run(folder)
    setting_of = settings_of(world)
    names = [str(detector["name"]) for detector in world["detectors"] if detector["name"] in setting_of]
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        gathers = [
            line
            for line in (json.loads(text) for text in stream if text.strip())
            if line["event"] == "gather"
        ]
    counts, escaped = counts_of(gathers, names)
    return Reading(
        folder.name, names, [setting_of[name] for name in names], counts, len(gathers), escaped
    )


def chsh(readings: list[Reading]) -> Fraction | None:
    """S over four two-table runs: E(a, b) - E(a, b') + E(a', b) + E(a', b')
    with a < a' and b < b' the two settings of each side."""
    pairs = [reading for reading in readings if len(reading.settings) == 2]
    if len(pairs) != 4:
        return None
    firsts = sorted({reading.settings[0] for reading in pairs})
    seconds = sorted({reading.settings[1] for reading in pairs})
    if len(firsts) != 2 or len(seconds) != 2:
        return None
    by_setting = {(reading.settings[0], reading.settings[1]): reading for reading in pairs}
    a, a_prime = firsts
    b, b_prime = seconds
    try:
        return (
            by_setting[(a, b)].correlation
            - by_setting[(a, b_prime)].correlation
            + by_setting[(a_prime, b)].correlation
            + by_setting[(a_prime, b_prime)].correlation
        )
    except KeyError:
        return None


def report(readings: list[Reading]) -> list[str]:
    lines = []
    for reading in readings:
        cells = ", ".join(
            "".join("+" if channel == PLUS else "-" for channel in cell) + f" {count}"
            for cell, count in sorted(reading.counts.items())
        )
        lines.append(
            f"{reading.folder}: DETECTOR {reading.gathers} gathers, the cells {cells}"
            + (f", {reading.escaped} with no cell" if reading.escaped else "")
            + "; settings "
            + ", ".join(f"{n} {s}" for n, s in zip(reading.names, reading.settings, strict=True))
        )
        if len(reading.names) == 2:
            lines.append(
                f"{reading.folder}: COMPUTATION E = {reading.correlation} = {float(reading.correlation):.5f}; "
                f"the marginals {reading.marginal(0)} and {reading.marginal(1)}"
            )
        elif len(reading.names) == 1:
            lines.append(
                f"{reading.folder}: COMPUTATION the + share {reading.marginal(0)} = {float(reading.marginal(0)):.5f}"
            )
    value = chsh(readings)
    if value is not None:
        lines.append(f"COMPUTATION S = {value} = {float(value):.6f}")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("runs", nargs="+", type=Path, help="run folders of the GO worlds")
    arguments = parser.parse_args(argv)
    readings = [read_run(folder) for folder in arguments.runs]
    for line in report(readings):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
