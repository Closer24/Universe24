"""Write the register's `replay` blocks of series R from the engine as
shipped: every world run headless for the register's cap of intervals and
its record read by kind (`tools/quarks_readings.replay_block`), no number
typed by hand (the model owner, record 205: a run proves; the Boss's order
of 2026-09-21 after the crossing rule moved the fate readings). Run from
the repository root:

    python examples/events/quarks/replay_register.py [--cap 100]

`tests/test_quarks_expectations.py` (e) replays the same blocks bit-exact.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

from event_universe.events import parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REGISTER = HERE / "expectations.json"
DEFAULT_CAP = 100


def readings_tool():
    """The readings tool loaded by its path (a reader of the record)."""
    path = ROOT / "tools" / "quarks_readings.py"
    spec = importlib.util.spec_from_file_location("quarks_readings_tool", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["quarks_readings_tool"] = module
    spec.loader.exec_module(module)
    return module


def replay_of(name: str, cap: int) -> dict[str, object]:
    """Run one shipped world for `cap` intervals into a temporary folder and
    read its replay block."""
    tool = readings_tool()
    source = (HERE / f"{name}.json").read_bytes()
    world = parse_nature_beam_world(json.loads(source))
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "run"
        out.mkdir()
        execute_nature_beam_run(world, source, out, name, cap)
        block: dict[str, object] = tool.replay_block(out, cap)
    return block


def main() -> None:
    """Write every world's `replay` block and its engine first step."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cap", type=int, default=DEFAULT_CAP)
    args = parser.parse_args()
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    drive = str(register.get("drive", "per_axis"))
    for name, pinned in register["worlds"].items():
        # The former blocks (2026-09-21, read under the per-axis drive of
        # history) stand as history beside the law's, replayed under the
        # world key `per_axis_drive` by the test's (f); written once, when
        # the register's drive column first names the line drive.
        if "former" not in pinned and drive == "line":
            pinned["former"] = {
                "drive": "per_axis",
                "replay": pinned["replay"],
                "engine_first_step": pinned["fate"]["engine_first_step"],
            }
        block = replay_of(name, args.cap)
        pinned["replay"] = block
        steps = block["steps"]
        assert isinstance(steps, dict)
        first = min((ticks[0][0] for ticks in steps.values() if ticks), default=None)
        pinned["fate"]["engine_first_step"] = first
        pinned["fate"].pop("step_every_about", None)
        print(f"{name}: {sum(len(t) for t in steps.values())} steps, first at {first}", flush=True)
    REGISTER.write_text(json.dumps(register, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
