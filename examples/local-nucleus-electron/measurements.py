"""Read canonical recorded evidence without reconstructing missing dynamics."""

import json
from pathlib import Path


def load_run(run_dir: Path) -> dict[str, object]:
    """Return decoded canonical sources; the raw trace is independent of display sampling."""
    return {
        "initialization": json.loads((run_dir / "initialization.json").read_text()),
        "metadata": json.loads((run_dir / "run.json").read_text()),
        "events": [json.loads(line) for line in (run_dir / "events.jsonl").read_text().splitlines()],
        "frames": [json.loads(line) for line in (run_dir / "states.jsonl").read_text().splitlines()],
        "final_state": json.loads((run_dir / "state.json").read_text()),
    }
