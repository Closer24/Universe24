"""The coincidence count of BELL from the clicks' own times (the owner's decision, 22:26Z): no shared click, each detector clicks alone at its own interval, and the pairs are counted twice, by the pair record's identity (every click line carries its record) and within the coincidence window the expectation file declares (`coincidence_window`, intervals, as Aspect's window), a left click and a right click matched when their intervals differ by at most the window, each click in one pair at most, the nearest first. Per cell of settings (the polarisers' angles of the world, or the setting a click line carries when the polarisers switch in flight) E = (same - different) / pairs, the outcome plus at the far set and minus at the polariser's own set; S = E(a, b) - E(a, b2) + E(a2, b) + E(a2, b2) over the four cells where all four exist, from one switching run or from four fixed-angle runs read together. Nothing here is compared with nature: the report is the run's numbers beside the expectation file's forms. Run from the repository root: python examples/events/experiments/coincidences.py <world.json> <world.output.json> [<world.json> <world.output.json> ...]; the report is printed and written beside the first output as <name>.coincidences.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SIDES = {"left": ("left_plus", "left_minus"), "right": ("right_plus", "right_minus")}
CELLS = (("a", "b"), ("a", "b2"), ("a2", "b"), ("a2", "b2"))


def settings_of(world: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Each side's polariser: its fixed angle, or its two angles and the period when it switches (the card of #1315: `angles` and `every`)."""
    found: dict[str, dict[str, Any]] = {}
    for body in world["measured"]:
        card = body.get("polariser")
        if card is None:
            continue
        side = "left" if card["sets"][0].startswith("left") else "right"
        found[side] = card
    return found


def setting_at(card: dict[str, Any], interval: int) -> list[int]:
    """The exact pair the polariser held at the interval (no angle, no cosine: the pair as the file writes it): the fixed one, or the first for `every` intervals and the second for the next, by the body's own clock from interval 0."""
    if "angles" in card:
        first, second = card["angles"]
        return list(first if (interval // int(card["every"])) % 2 == 0 else second)
    return list(card["angle"])


def clicks_by_side(
    output: dict[str, Any], pair_givers: set[int] | None = None
) -> dict[str, list[dict[str, Any]]]:
    """The clicks per side with their outcome: plus at the far set, minus at the polariser's own set; sorted by interval; a click that names its `giver` counts only when the giver is a crystal (the pump's own clicks at the polarisers are no pair's)."""
    sides: dict[str, list[dict[str, Any]]] = {"left": [], "right": []}
    for click in output["clicks"]:
        if pair_givers and "giver" in click and click["giver"] not in pair_givers:
            continue
        for side, (plus, minus) in SIDES.items():
            if click["detector"] in (plus, minus):
                sides[side].append(
                    {
                        "interval": int(click["interval"]),
                        "clock": int(click.get("clock", click["interval"])),
                        "record": click["record"],
                        "outcome": 1 if click["detector"] == plus else -1,
                    }
                )
    for side in sides:
        sides[side].sort(key=lambda c: c["interval"])
    return sides


def pairs_by_record(
    sides: dict[str, list[dict[str, Any]]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """The pairs by the pair record's identity: one left click and one right click of the same record."""
    right = {c["record"]: c for c in sides["right"]}
    return [(left, right[left["record"]]) for left in sides["left"] if left["record"] in right]


def pairs_by_window(
    sides: dict[str, list[dict[str, Any]]], window: int, time: str = "interval"
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """The pairs within the window: each left click with the nearest unmatched right click at most `window` away on the time named, `interval` (the loop's step, the laboratory clock as Aspect's) or `clock` (the detector's own count)."""
    free = list(sides["right"])
    pairs = []
    for left in sides["left"]:
        best = None
        for right in free:
            gap = abs(right[time] - left[time])
            if gap <= window and (best is None or gap < abs(best[time] - left[time])):
                best = right
        if best is not None:
            free.remove(best)
            pairs.append((left, best))
    return pairs


def cell_of(
    cards: dict[str, dict[str, Any]],
    names: dict[str, dict[str, list[int]]],
    left: dict[str, Any],
    right: dict[str, Any],
) -> str:
    """The cell's name from the two exact pairs held at the two clicks' intervals, each equal to one of the expectation file's named pairs (a, a2, b, b2); a pair named nowhere is refused."""

    def name(side: str, click: dict[str, Any]) -> str:
        pair = setting_at(cards[side], click["interval"])
        matches = [n for n, named in names[side].items() if list(named) == pair]
        if len(matches) != 1:
            raise ValueError(
                f"the {side} pair {pair} at interval {click['interval']} is named by {matches}"
            )
        return matches[0]

    return f"{name('left', left)}_{name('right', right)}"


def report(worlds: list[Path], outputs: list[Path]) -> dict[str, Any]:
    """The report over the runs given: the four fixed-angle runs together, or one switching run."""
    names: dict[str, dict[str, list[int]]] = {"left": {}, "right": {}}
    window = None
    by_record: list[tuple[dict[str, Any], dict[str, Any]]] = []
    by_window: list[tuple[dict[str, Any], dict[str, Any]]] = []
    by_clock: list[tuple[dict[str, Any], dict[str, Any]]] = []
    disagreeing = 0
    cards_of_run: list[dict[str, dict[str, Any]]] = []
    for world_path, output_path in zip(worlds, outputs, strict=True):
        world = json.loads(world_path.read_text(encoding="utf-8"))
        expectation = json.loads(world_path.with_suffix(".expectation.json").read_text(encoding="utf-8"))
        window = int(expectation["coincidence_window"])
        for side, name_to_pair in expectation["settings"].items():
            for setting, pair in name_to_pair.items():
                names[side][setting] = list(pair)
        output = json.loads(output_path.read_text(encoding="utf-8"))
        crystals = {n for n, body in enumerate(world["measured"]) if "crystal" in body}
        sides = clicks_by_side(output, crystals)
        cards = settings_of(world)
        cards_of_run.append(cards)
        by_record += [
            (dict(one, run=len(cards_of_run) - 1), other) for one, other in pairs_by_record(sides)
        ]
        by_window += [
            (dict(one, run=len(cards_of_run) - 1), other)
            for one, other in pairs_by_window(sides, window)
        ]
        by_clock += [
            (dict(one, run=len(cards_of_run) - 1), other)
            for one, other in pairs_by_window(sides, window, "clock")
        ]
        disagreeing += sum(c["clock"] != c["interval"] for side in sides.values() for c in side)

    def tally(pairs: list[tuple[dict[str, Any], dict[str, Any]]]) -> dict[str, Any]:
        cells: dict[str, dict[str, int]] = {}
        for left, right in pairs:
            cell = cells.setdefault(
                cell_of(cards_of_run[left["run"]], names, left, right), {"same": 0, "different": 0}
            )
            cell["same" if left["outcome"] == right["outcome"] else "different"] += 1
        e = {
            cell: (c["same"] - c["different"]) / (c["same"] + c["different"])
            for cell, c in cells.items()
        }
        s = (
            e["a_b"] - e["a_b2"] + e["a2_b"] + e["a2_b2"]
            if all(f"{one}_{other}" in e for one, other in CELLS)
            else None
        )
        return {
            "pairs": len(pairs),
            "cells": cells,
            "E": {k: round(v, 4) for k, v in e.items()},
            "S": None if s is None else round(s, 4),
        }

    return {
        "window": window,
        "by_record": tally(by_record),
        "within_window": tally(by_window),
        "within_window_by_detector_clock": tally(by_clock),
        "clicks_whose_two_times_differ": disagreeing,
        "note": "S twice: over every pair matched by the pair record's identity, and over the pairs matched within the window from the clicks' own intervals (the owner's 22:26Z); and once more with the window on the detector's own count (`clock` on the click line; the owner's 23:12Z): in Bell the detectors are at rest and read no level, so the two times agree and `clicks_whose_two_times_differ` is 0, else it is said; the expectation file's blind expectation decides nothing here; no angle and no cosine enter: the settings are the files' exact pairs and the outcomes the clicks' detectors",
    }


def main() -> None:
    arguments = [Path(a).resolve() for a in sys.argv[1:]]
    worlds, outputs = arguments[0::2], arguments[1::2]
    found = report(worlds, outputs)
    text = json.dumps(found, indent=1)
    print(text)
    outputs[0].with_suffix(".coincidences.json").write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
