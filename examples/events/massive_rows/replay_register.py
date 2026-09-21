"""The register of the small massive two-slit world's replay
(`slits_matter_small`, `tests/test_massive_rows.py` (f)): the world run
through the runner as shipped and its record written into
`expectations.json` under `slits_matter_small.replay` (no number typed by
hand): the gathers of the records 1 .. 8 (the tick, the chosen set, the
Node, the content q_F and the one label), the books of the massive family
at the end, the layer's line and the sha256 of `state.json`, of the books
(the audit of `run.json`, JSON-encoded) and of `events.jsonl`. A law
change re-registers it by this script; the test replays it bit-exact.

    PYTHONPATH=src python examples/events/massive_rows/replay_register.py
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.events.run import execute_nature_beam_run  # noqa: E402
from event_universe.world_loading import load_world  # noqa: E402

WORLD = HERE / "slits_matter_small.json"
FAMILY = "matter"
BASE = 1 << 32


def replay(births: int) -> dict[str, object]:
    """The world's record through the runner, as the register keeps it."""
    source = WORLD.read_bytes()
    loaded = load_world(source, base_dir=WORLD.parent)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "run"
        out.mkdir()
        execute_nature_beam_run(loaded.world, source, out, "register", loaded.world.ticks)
        record = json.loads((out / "run.json").read_text(encoding="utf-8"))
        digests = {
            "state_sha256": hashlib.sha256((out / "state.json").read_bytes()).hexdigest(),
            "audit_sha256": hashlib.sha256(json.dumps(record["audit"]).encode("utf-8")).hexdigest(),
            "events_sha256": hashlib.sha256((out / "events.jsonl").read_bytes()).hexdigest(),
        }
    gathers = [
        {
            "record": int(g["record"]) - BASE,
            "tick": g["tick"],
            "u": g["u"],
            "chosen": None if g["chosen"] is None else g["chosen"][0][0],
            "node": g["node"],
            "content": g["content"],
            "momentum": g["momentum"],
        }
        for g in record["world"]
        if BASE + 1 <= int(g["record"]) <= BASE + births
    ]
    books = record["audit"][-1]["families"][FAMILY]
    return {
        "date": "2026-09-21",
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "intervals": record["completed_ticks"],
        "conserved": record["conserved_at_every_completed_tick"],
        "hypotheses": record["hypotheses"],
        "layer": record["layer"],
        "gathers": gathers,
        "books_at_end": books,
        "momentum_at_end": record["audit"][-1]["momentum"],
        "digests": digests,
    }


def main() -> None:
    path = HERE / "expectations.json"
    register = json.loads(path.read_text(encoding="utf-8"))
    block = register["slits_matter_small"]
    block["replay"] = replay(int(block["births"]))
    path.write_text(json.dumps(register, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(block["replay"]["digests"], indent=1))


if __name__ == "__main__":
    main()
