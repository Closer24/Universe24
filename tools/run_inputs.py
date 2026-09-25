"""THE ONE COMMAND (the model owner's record 1887 of 2026-09-25; ALGEBRA.md 9.22
(7)): a list of input files in, one output file per experiment out, in parallel.

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
...}]}` on the count of clicks, or `{"detector": ..., "first_click": ...,
"band": ...}` on the interval of the detector's first click, written before
the run), the comparison per pin: MATCH within the band or MISS, with the
value read. Nothing else is compared; a GameBoard
reading is not written. The output carries no time, so two inputs run
together give the same files as each alone (the test of record 1887); the
wall seconds go to the summary printed.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/run_inputs.py --out runs/inputs --jobs 4 \\
        examples/events/massive_record/light_clock_60.json ...
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

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import parse_nature_beam_world

OUTPUT_FORMAT = "one-command-output-v1"


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
    stamp = document.get("input") if isinstance(document, dict) else None
    output["stamp"] = stamp if isinstance(stamp, dict) else None
    try:
        world = parse_nature_beam_world(document)
        if not world.detector_law:
            raise ValueError("the one command runs the worlds of the detector law alone")
        simulation = DetectorLawSimulation(world)
    except Exception as error:  # noqa: BLE001 - every refusal is written, none hidden
        output["verdict"] = "REFUSED"
        output["reason"] = f"{type(error).__name__}: {error}"
        write_output(Path(out_dir), name, output)
        return {"name": name, "verdict": "REFUSED", "seconds": time.monotonic() - started}
    output["verdict"] = "LAWFUL"
    output["ticks"] = world.ticks
    clicks: list[dict[str, object]] = []
    for _ in range(world.ticks):
        simulation.step()
    for gather in simulation.layer.gathers:
        chosen = gather["chosen"]
        detector = chosen[0][0] if isinstance(chosen, list) and chosen else None
        clicks.append({"detector": detector, "interval": gather["click"], "record": gather["record"]})
    counts: dict[str, int] = {detector.name: 0 for detector in world.detectors}
    for click in clicks:
        detector = click["detector"]
        if isinstance(detector, str):
            counts[detector] = counts.get(detector, 0) + 1
    output["clicks"] = clicks
    output["counts"] = counts
    output["records_alive"] = len(simulation.records)
    verdicts = []
    for pin in pins:
        # a pin on the COUNT of clicks at the detector, or on the interval of
        # its FIRST click (the light clock's and Sagnac's first rungs)
        detector, band = str(pin["detector"]), int(pin["band"])
        if "first_click" in pin:
            kind, expected = "first_click", int(pin["first_click"])
            firsts = [int(c["interval"]) for c in clicks if c["detector"] == detector]
            read: int | None = min(firsts) if firsts else None
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
        "--jobs", type=int, default=None, help="processes at once (the cores by default)"
    )
    parser.add_argument(
        "--pins", type=Path, default=None, help="the blind pins per input, written before the run"
    )
    arguments = parser.parse_args(argv)
    names = [path.stem for path in arguments.inputs]
    if len(set(names)) != len(names):
        parser.error("two inputs of one name")
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
