"""THE ONE COMMAND (the model owner's record 1887 of 2026-09-25; ALGEBRA.md #a-familys-declaration): a list of input files in, one output file per experiment out, in parallel.

Every input file is run in its own process (the runs share nothing), at most
`--jobs` at once (the machine's cores by default). Each run first loads its
input and says LAWFUL or REFUSED with the reason (the loader's integer checks
of record 1886: the input stamp, the profiles against the eigen-equation, the
clocks, the bodies, the families); a lawful input is then run under the law
for its declared ticks, headless, and ONE output file `<name>.output.json` is
written into `--out`: the input's name, its stamp (the law and the hash), the
verdict, the ticks, the clicks (the detector's name and the interval of each
click line, DETECTOR), the count per detector, and, where `--pins` registers a
blind pin for the input (`{"<name>": [{"detector": ..., "count": ..., "band":
...}]}` on the count of clicks, `{"detector": ..., "first_click": ..., "band":
...}` on the detector's first click (the least interval since the record's giving
among its clicks), or `{"detector": ...,
"mean_interval": ..., "band": ...}` on the mean over the detector's clicks of the
interval since the record's giving (the passage rows, ALGEBRA.md #the-ladder),
written before the run), the comparison per pin: MATCH within the band or MISS, with the
value read. Nothing else is compared; a GameBoard
reading is not written. The output carries no time, so two inputs run
together give the same files as each alone (the test of record 1887); the
wall seconds go to the summary printed.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/run_inputs.py --out runs/inputs --jobs 4 \\
        <world>.json ...
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path
from typing import Any

from event_universe.core.readings import Readings
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world

OUTPUT_FORMAT = "one-command-output-v1"


def input_mode(path: Path) -> str:
    """The run's mode of one input as its engine start file declares it
    (`load_world` reads the file with the generator's mode file beside it and
    refuses a missing key by name); an input the loader refuses is reported by the run itself."""
    try:
        world = load_world(path)
    except ValueError, OSError:
        return "refused"
    return world.start.mode if world.start is not None else "refused"


def load_pins(path: Path | None) -> dict[str, list[dict[str, Any]]]:
    if path is None:
        return {}
    pins = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(pins, dict):
        raise ValueError("the pins file is an object: input name to its list of pins")
    return pins


def run_input(path: str, out_dir: str, pins: list[dict[str, Any]]) -> dict[str, object]:
    """One input file in this process: the verdict at load, the run, the output
    file; the summary row returned (the seconds are the summary's alone)."""
    source = Path(path)
    name = source.stem
    started = time.monotonic()
    output: dict[str, object] = {"format": OUTPUT_FORMAT, "input": source.name, "name": name}
    document = json.loads(source.read_text(encoding="utf-8"))
    stamp = document.get("stamp") if isinstance(document, dict) else None
    output["stamp"] = stamp if isinstance(stamp, dict) else None
    try:
        world = load_world(source)  # the mode file beside the world handed with its files
        simulation = DetectorLawSimulation(world)
    except Exception as error:  # noqa: BLE001 - every refusal is written, none hidden
        output["verdict"] = "REFUSED"
        output["reason"] = f"{type(error).__name__}: {error}"
        write_output(Path(out_dir), name, output)
        return {"name": name, "verdict": "REFUSED", "seconds": time.monotonic() - started}
    output["verdict"] = "LAWFUL"
    output["step"] = {"hash": world.step.digest}
    output["ticks"] = world.ticks
    readings = Readings(world.readings)
    readings.read(simulation)
    output["mode"] = world.start.mode if world.start is not None else None
    clicks: list[dict[str, object]] = []
    for _ in range(world.ticks):
        simulation.step()
        # THE LEAK TEST IN EVERY RUN (the model owner's record 2075 (3); BUILD.md
        # section 26 item 55): a family with no source stays exactly zero at
        # every interval, or the run is refused naming the family
        leaks = simulation.leaks()
        if leaks:
            output["verdict"] = "LEAK"
            output["reason"] = (
                f"the families {leaks} carry rows without a source at interval {simulation.tick} "
                "(the model owner's record 2075 (3): a family with no source stays exactly zero)"
            )
            write_output(Path(out_dir), name, output)
            return {"name": name, "verdict": "LEAK", "seconds": time.monotonic() - started}
        readings.read(simulation)
    readings.clicks(simulation.layer.gathers, world.detectors)
    for gather in simulation.layer.gathers:
        chosen = gather["chosen"]
        detector = chosen[0][0] if isinstance(chosen, list) and chosen else None
        clicks.append(
            {
                "detector": detector,
                "interval": gather["click"],
                "giving": gather["giving"],
                "record": gather["record"],
            }
        )
    counts: dict[str, int] = {detector.name: 0 for detector in world.detectors}
    for click in clicks:
        detector = click["detector"]
        if isinstance(detector, str):
            counts[detector] = counts.get(detector, 0) + 1
    output["clicks"] = clicks
    output["readings"] = readings.output()
    output["counts"] = counts
    output["records_alive"] = len(simulation.records)
    verdicts = []
    # the expectation file beside the world (<world>.expectation.json), written before the run: its
    # DETECTOR section joins the pins, its GAMEBOARD section is compared below
    expectation_path = Path(path).with_suffix(".expectation.json")
    expectation = (
        json.loads(expectation_path.read_text(encoding="utf-8")) if expectation_path.exists() else {}
    )
    for pin in [*pins, *expectation.get("DETECTOR", [])]:
        # a pin on the COUNT of clicks at the detector, on its FIRST click (the
        # least interval since the record's giving among its clicks: the stock's
        # fastest passage; for one record given at interval 0 the interval of the
        # click itself), or on the MEAN INTERVAL over its clicks since the
        # record's giving (the passage rows, ALGEBRA.md #the-ladder: the pin the
        # mean click interval over the stock), rounded to the nearest integer
        detector, band = str(pin["detector"]), int(pin["band"])
        at_detector = [c for c in clicks if c["detector"] == detector]
        waits = [int(c["interval"]) - int(c["giving"]) for c in at_detector]
        if "first_click" in pin:
            kind, expected = "first_click", int(pin["first_click"])
            read: int | None = min(waits) if waits else None
        elif "mean_interval" in pin:
            kind, expected = "mean_interval", int(pin["mean_interval"])
            read = (2 * sum(waits) + len(waits)) // (2 * len(waits)) if waits else None
        else:
            kind, expected = "count", int(pin["count"])
            read = counts.get(detector, 0)
        verdicts.append(
            {
                "detector": detector,
                "kind": kind,
                "pin": expected,
                "band": band,
                "read": read,
                "verdict": "MATCH" if read is not None and abs(read - expected) <= band else "MISS",
            }
        )
    for pin in expectation.get("GAMEBOARD", []):
        # a pin of the expectation file's GAMEBOARD section (a diagnostic, never a measurement): a
        # body's momentum or centre at a named interval, read from the declared readings, each
        # component within the band
        kind = "momentum" if "momentum" in pin else "centre"
        expected_parts = [int(part) for part in pin[kind]]
        found = None
        for line in readings.output():
            if line["kind"] == kind and line.get("body") == int(pin["body"]):
                for entry in line["lines"]:
                    if entry["interval"] == int(pin["interval"]):
                        found = entry["momentum" if kind == "momentum" else "node"]
        verdicts.append(
            {
                "body": int(pin["body"]),
                "interval": int(pin["interval"]),
                "kind": kind,
                "pin": expected_parts,
                "band": int(pin["band"]),
                "read": found,
                "verdict": (
                    "MATCH"
                    if found is not None
                    and all(
                        abs(int(r) - e) <= int(pin["band"])
                        for r, e in zip(found, expected_parts, strict=True)
                    )
                    else "MISS"
                ),
            }
        )
    output["pins"] = verdicts
    write_output(Path(out_dir), name, output)
    return {
        "name": name,
        "verdict": "LAWFUL",
        "clicks": len(clicks),
        "pins": [v["verdict"] for v in verdicts],
        "seconds": time.monotonic() - started,
    }


def write_output(out_dir: Path, name: str, output: dict[str, object]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.output.json"
    path.write_text(json.dumps(output, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="the input files (world files)")
    parser.add_argument("--out", type=Path, required=True, help="the directory of the output files")
    parser.add_argument(
        "--jobs", type=int, required=True, help="processes at once (required, no default)"
    )
    parser.add_argument(
        "--pins",
        type=Path,
        default=None,
        help="the blind pins per input, written before the run; refused under the mode check",
    )
    arguments = parser.parse_args(argv)
    names = [path.stem for path in arguments.inputs]
    if len(set(names)) != len(names):
        parser.error("two inputs of one name")
    if arguments.jobs < 1:
        parser.error("--jobs must be 1 or more")
    # THE RUN'S MODE (the engine start file, record 2092 (2); BUILD.md section 26
    # item 57): every input names the one start file; under "check" no pin is
    # compared (the pins file refused), under "pin" the pins file is required
    modes = {path.stem: input_mode(path) for path in arguments.inputs}
    if any(mode == "check" for mode in modes.values()) and arguments.pins is not None:
        parser.error(
            "--pins is refused under the mode check (the engine start file: every measured event "
            "is read beside its blind expectation, no pin compared; records 2050, 2054, 2092)"
        )
    if any(mode == "pin" for mode in modes.values()) and arguments.pins is None:
        parser.error("--pins is required under the mode pin (the engine start file)")
    pins = load_pins(arguments.pins)
    rows: list[dict[str, object]] = []
    with ProcessPoolExecutor(max_workers=arguments.jobs, mp_context=get_context("spawn")) as pool:
        futures = [
            pool.submit(run_input, str(path), str(arguments.out), pins.get(path.stem, []))
            for path in arguments.inputs
        ]
        for future in futures:
            rows.append(future.result())
    for row in rows:
        print(json.dumps(row, sort_keys=True))
    return 0 if all(row["verdict"] == "LAWFUL" for row in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
