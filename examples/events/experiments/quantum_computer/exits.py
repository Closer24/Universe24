"""The reading of the phase of a one-qubit world of (k) from its two exits' clicks (ALGEBRA.md #the-rows-against-nature (l) and (k)): the runner's output beside the world (`<world>.output.json`, tools/run_inputs.py) carries every click with its detector; this tool counts the clicks per exit, the share at the cross exit, and the phase the row's form gives for that share, cos^2 (Delta / 2) = share / (4 s (1 - s)) with s the expectation file's splitter share, beside the expectation's blind shares at each reading of the level; the books it can read from the output alone: the clicks per detector and the records alive at the end (the labels left on the GameBoard); the quanta given and the labels ended at a face are the event lines' (examples/events/experiments/bell_books.py). Nothing here is compared with nature, and no rule is replayed: the cosine lives in the expectation's form alone. Run from the repository root: python examples/events/experiments/quantum_computer/exits.py <world.json> <world.output.json>; the report is printed and written beside the output as <name>.exits.json."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

EXITS = ("cross_exit", "straight_exit")
SPLITTER_SHARE = 0.5  # s of the row's form, the expectation's: one half at Cheshbon's count by bisection


def clicks_per_exit(output: dict[str, Any]) -> dict[str, int]:
    """The clicks per detector from the output's click lines, the measurement."""
    counts = dict.fromkeys(EXITS, 0)
    for click in output.get("clicks", []):
        name = click.get("detector")
        if name in counts:
            counts[name] += 1
    return counts


def phase_of(share: float, splitter_share: float = SPLITTER_SHARE) -> float | None:
    """Delta from the cross exit's share by the row's form, 4 s (1 - s) cos^2 (Delta / 2); None where the share exceeds the form's top."""
    top = 4 * splitter_share * (1 - splitter_share)
    if top <= 0 or share > top:
        return None
    return 2 * math.acos(math.sqrt(share / top))


def report(world: dict[str, Any], output: dict[str, Any], expectation: dict[str, Any]) -> dict[str, Any]:
    """The run's numbers beside the expectation's forms: the clicks per exit (DETECTOR), the cross share with its draw's band, the phase by the form, the records alive at the end (GAMEBOARD), and the giver's stock as the quanta the run could give."""
    counts = clicks_per_exit(output)
    total = sum(counts.values())
    share = counts["cross_exit"] / total if total else None
    band = math.sqrt(share * (1 - share) / total) if total and share is not None else None
    phase = None if share is None else phase_of(share)
    giver = world["measured"][0]
    return {
        "verdict": output.get("verdict"),
        "DETECTOR": {
            "clicks_per_exit": counts,
            "clicks": total,
            "cross_share": None if share is None else round(share, 4),
            "cross_share_band": None if band is None else round(band, 4),
            "phase_by_the_form": None if phase is None else round(phase, 4),
        },
        "GAMEBOARD": {
            "records_alive_at_the_end": output.get("records_alive"),
            "quanta_the_giver_could_give": giver.get("stocks", {}).get("charge"),
        },
        "expected": expectation.get("blind_expectation", {}),
        "row": "the clicks per exit are the measurement; the share's band is the draw's, sqrt(p (1 - p) / n); the phase is the row's form read backward and no reading of the GameBoard; the quanta given and the labels ended at a face are read from the event lines, not from this output",
    }


def main(argv: list[str]) -> None:
    world_path, output_path = Path(argv[1]), Path(argv[2])
    world = json.loads(world_path.read_text(encoding="utf-8"))
    output = json.loads(output_path.read_text(encoding="utf-8"))
    expectation = json.loads(world_path.with_suffix(".expectation.json").read_text(encoding="utf-8"))
    result = report(world, output, expectation)
    text = json.dumps(result, indent=1)
    print(text)
    output_path.with_suffix(".exits.json").write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
