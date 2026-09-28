"""THE READER OF THE ONE-CLICK TRAIN (the fixture of the corrected giving, the Closer's word of 2026-09-28, 13:34 Israel time): the world of `lay_out_one_click_train.py` run headless through the engine's own functions with the event lines observed, then read against its expectation file, MATCH or MISS per line: THE TRAIN (GAMEBOARD), the window's length from the giving line, opened to closed, in intervals and in periods of the giver's clock (the mode's `period`), against `train_periods` within `train_band_periods`; THE WAVELENGTH (GAMEBOARD), twice the mean spacing of the sign changes of the light's level along the beam between the giver's far face and the window, the median over the intervals of the window, against `wavelength_links` within its band; THE GROUP VELOCITY (GAMEBOARD), the centroid of |level| along x over the intervals after the close until the record leaves, against `group_velocity_links_per_interval` within its band; THE CLICK (DETECTOR), the strip's first click in intervals after the close against the distance over the group velocity; THE REVERSAL (GAMEBOARD), the runner's reversible row over the whole run with `--reversible`, MATCH or MISS with the first deviation. Nothing here replays a rule; no number of a run enters a test. Run from the repository root: PYTHONPATH=src python examples/events/experiments/de_broglie/one_click_train.py <world.json> [--reversible]; the reading is written beside the world as `<name>.train.json`."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any

from one_click import centroid_and_extent, rows_of, run, wavelength_along

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
from reversible import reversible_row  # noqa: E402  (the runner's own row, tools/reversible.py)


def verdict(value: float | None, expected: float, band: float) -> str:
    """MATCH inside the band about the expected number, MISS outside or with no reading."""
    return "MISS" if value is None else ("MATCH" if abs(value - expected) <= band else "MISS")


def read(world_path: Path, reversible: bool) -> dict[str, Any]:
    """The five lines against the expectation file beside the world."""
    document = json.loads(world_path.read_text(encoding="utf-8"))
    blind = json.loads(world_path.with_suffix(".expectation.json").read_text(encoding="utf-8"))["blind"]
    mode = json.loads(world_path.with_suffix(".mode.json").read_text(encoding="utf-8"))
    period = int(mode["bodies"][0].get("period") or blind["period_intervals"])
    generator_train = mode["bodies"][0].get(
        "train"
    )  # the generator's reading of the train on the form, the algebra column
    output, lines, refusal = run(world_path)
    shape = document["shape"]
    strip = document["detectors"][0]["positions"]
    beam_y = strip[0][1] + len(strip) // 2 - 1
    giver_far = max(n["node"][0] for n in document["measured"][0]["nodes"])
    window_x = min(n["node"][0] for n in document["measured"][2]["nodes"])
    givings = [line for line in lines if line["event"] == "giving"]
    opened = givings[0].get("window") if givings else None
    closed = givings[0]["tick"] if givings else None
    train_intervals = None if opened is None or closed is None else closed - opened
    train_periods = None if train_intervals is None else round(train_intervals / period, 2)
    rows = rows_of(output, "light_rows")
    in_window = [r for r in rows if opened is not None and opened < r["interval"] <= (closed or 0)]
    wavelengths = [
        w
        for r in in_window
        if (w := wavelength_along(r["rows"], shape, beam_y, giver_far + 1, window_x - 1)) is not None
    ]
    wavelength = round(statistics.median(wavelengths), 2) if wavelengths else None
    path = []
    for r in rows:
        if closed is not None and r["interval"] >= closed:
            centre, largest, nodes = centroid_and_extent(r["rows"], shape)
            if centre is not None:
                path.append((r["interval"], centre, largest, nodes))
    velocity = None
    if len(path) >= 2 and path[-1][0] > path[0][0]:
        velocity = round((path[-1][1] - path[0][1]) / (path[-1][0] - path[0][0]), 4)
    clicks = sorted(c["interval"] for c in output["clicks"] if c["detector"] == "window_strip")
    distance = window_x - giver_far
    expected_click = (
        None
        if closed is None
        else round(closed + distance / blind["group_velocity_links_per_interval"], 1)
    )
    first_click = clicks[0] if clicks else None
    reversal: dict[str, Any] = {
        "label": "GAMEBOARD",
        "verdict": "NOT RUN",
        "row": "run with --reversible",
    }
    if reversible:
        row = reversible_row(
            lambda: DetectorLawSimulation(load_world(world_path)), int(document["ticks"])
        )
        reversal = {"label": "GAMEBOARD", **row}
    report = {
        "world": world_path.name,
        "kind": "THE ONE-CLICK TRAIN, the fixture of the corrected giving: every line MATCH or MISS against the expectation file",
        "verdict": output["verdict"],
        "refusal": refusal,
        "ticks_run": output["ticks_run"],
        "1_the_train": {
            "label": "GAMEBOARD",
            "opened": opened,
            "closed": closed,
            "train_intervals": train_intervals,
            "period_intervals": period,
            "train_periods": train_periods,
            "generator_train": generator_train,
            "generator_periods": None
            if not isinstance(generator_train, dict)
            else round(generator_train["intervals"] / period, 2),
            "expected_periods": blind["train_periods"],
            "band_periods": blind["train_band_periods"],
            "verdict": verdict(train_periods, blind["train_periods"], blind["train_band_periods"]),
        },
        "2_the_wavelength": {
            "label": "GAMEBOARD",
            "wavelengths_links_in_the_window": wavelengths,
            "wavelength_links": wavelength,
            "expected_links": blind["wavelength_links"],
            "band_links": blind["wavelength_band_links"],
            "verdict": verdict(wavelength, blind["wavelength_links"], blind["wavelength_band_links"]),
        },
        "3_the_group_velocity": {
            "label": "GAMEBOARD",
            "centroid_path": [(i, round(c, 2), largest, nodes) for i, c, largest, nodes in path],
            "links_per_interval": velocity,
            "expected": blind["group_velocity_links_per_interval"],
            "band": blind["group_velocity_band"],
            "verdict": verdict(
                velocity, blind["group_velocity_links_per_interval"], blind["group_velocity_band"]
            ),
        },
        "4_the_click": {
            "label": "DETECTOR",
            "strip_clicks": clicks,
            "distance_links": distance,
            "expected_interval": expected_click,
            "verdict": "MISS"
            if first_click is None or expected_click is None
            else verdict(first_click, expected_click, period),
        },
        "5_the_reversal": reversal,
    }
    world_path.with_name(f"{world_path.stem}.train.json").write_text(
        json.dumps(report, indent=1) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("world", type=Path, help="the world file")
    parser.add_argument(
        "--reversible", action="store_true", help="run the reversible row over the whole run"
    )
    args = parser.parse_args()
    report = read(args.world.resolve(), args.reversible)
    shown = {k: v for k, v in report.items() if k != "3_the_group_velocity"}
    shown["3_the_group_velocity"] = {
        k: v for k, v in report["3_the_group_velocity"].items() if k != "centroid_path"
    }
    print(json.dumps(shown, indent=1))


if __name__ == "__main__":
    main()
