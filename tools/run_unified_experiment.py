"""Reproducible candidate evidence using the existing application/HTML path.

The isolated-source runs deliberately measure a known open risk. Do not turn
observed self-force into a success claim about physical gravity.
"""

import json
from pathlib import Path

from event_universe import Config
from event_universe.diagnostics.frames import Slice
from event_universe.runner import run_scenario
from event_universe.scenarios import Scenario, get_scenario


def run(output: Path) -> None:
    cases = [
        Scenario(
            "isolated-slow",
            Config(nx=72, ny=72, nz=72, c_units=12, force_den=12),
            ((0, 36, 36, 36, 3, 0, 0),),
            24,
            Slice("XY", 36),
            unified=True,
        ),
        Scenario(
            "isolated-capacity",
            Config(nx=72, ny=72, nz=72, c_units=12, force_den=12),
            ((0, 36, 36, 36, 12, 0, 0),),
            24,
            Slice("XY", 36),
            unified=True,
        ),
        get_scenario("unified"),
        get_scenario("unified-links"),
    ]
    summaries = []
    for case in cases:
        directory = output / case.name
        path = run_scenario(case, directory, frame_stride=max(1, case.ticks // 12))
        metadata = json.loads((directory / "run.json").read_text())
        events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
        summaries.append(
            {"scenario": case.name, "html": str(path), "metadata": metadata, "events": len(events)}
        )
        print(
            case.name,
            metadata["status"],
            "momentum conserved:",
            metadata["momentum_equal_at_every_completed_tick"],
            flush=True,
        )
    (output / "summary.json").write_text(json.dumps(summaries, indent=2) + "\n")


if __name__ == "__main__":
    run(Path("artifacts/unified-action"))
