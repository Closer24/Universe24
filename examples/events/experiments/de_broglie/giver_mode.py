"""THE GIVER'S MODE ALONE: the mode file of a world written by the generator's own functions (tools/body_generator.py, ALGEBRA.md #the-generator) for the giving bodies only, the wall, the screen and the tube loading as content alone (docs/ENGINE.md, the mode file: a body without a profile in its entry loads as content alone; only a giving body and a moving body need one). The generator computes a bound mode for every body whose family reads a held field plainly, and a thin body of hundreds of Nodes at the mirror's count takes hundreds of thousands of iterations to its first repeat (40 minutes on the two slits' board); so this driver hands the generator the same world with the still bodies under a copy of their family's row that reads no held field plainly, which the generator itself skips as content alone, while every body's count still enters the world's well (the giver's clock in the world's well is unchanged). The written entries carry the bodies' real family names, the profile at the generator's unit and the world's own digest, exactly as the generator's own command writes them; no number of the driver's own. Run from the repository root: PYTHONPATH=src python examples/events/experiments/de_broglie/giver_mode.py <world.json>; the mode file is written beside the world."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "tools"))

import body_generator  # noqa: E402  (the generator's module, found by its path under tools/)

from event_universe.world_files import input_digest  # noqa: E402

STILL = "_still"  # the suffix of the temporary row a still body is generated under
SCRATCH = (
    ROOT / "artifacts" / "giver_mode"
)  # the temporary files (an ignored folder inside the repository)


def still_universe(universe_path: str, families: set[str]) -> str:
    """The universe file with one extra row per family of a still body: the row's copy that reads no held field plainly (its `reads` empty), which the generator treats as content alone; the repository path of the copy."""
    document = json.loads((ROOT / universe_path).read_text(encoding="utf-8"))
    rows = {row["name"]: row for row in document["families"]}
    for name in sorted(families):
        copy = json.loads(json.dumps(rows[name]))
        copy["name"] = name + STILL
        copy["reads"] = []
        document["families"].append(copy)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    path = SCRATCH / Path(universe_path).name
    path.write_text(json.dumps(document), encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def giver_modes(world_path: Path) -> dict[str, Any]:
    """The generator's reading of the world with the still bodies under their still rows, the entries' families restored."""
    document = json.loads(world_path.read_text(encoding="utf-8"))
    handed = json.loads(json.dumps(document))
    still = {
        body["family"]
        for body in handed["measured"]
        if "emitter" not in body and not any(body.get("momentum", [0, 0, 0]))
    }
    handed["universe"] = still_universe(document["universe"], still)
    for body in handed["measured"]:
        if (
            body["family"] in still
            and "emitter" not in body
            and not any(body.get("momentum", [0, 0, 0]))
        ):
            body["family"] = body["family"] + STILL
    sys.set_int_max_str_digits(0)
    reading = body_generator.generate(handed)
    for entry, body in zip(reading["bodies"], document["measured"], strict=True):
        entry["family"] = body["family"]
    reading["world_digest"] = input_digest(document)
    return reading


def write_mode_file(world_path: Path) -> Path:
    """The mode file beside the world, in the form the generator's own command writes: the profile as a flat list, the content and the moving levels left out."""
    reading = giver_modes(world_path)
    for body in reading["bodies"]:
        profile = body.pop("profile", None)
        body.pop("content", None)
        if "moving" in body:
            body["moving"].pop("now", None)
            body["moving"].pop("before", None)
        if profile is not None:
            body["profile"] = profile.ravel().tolist()
    out = world_path.with_suffix(".mode.json")
    out.write_text(json.dumps(reading), encoding="utf-8")
    return out


def main() -> None:
    for argument in sys.argv[1:]:
        out = write_mode_file(Path(argument).resolve())
        reading = json.loads(out.read_text(encoding="utf-8"))
        summary = [
            {
                k: v
                for k, v in body.items()
                if k in ("family", "clock", "period", "iterations", "mode", "refused")
            }
            for body in reading["bodies"]
        ]
        print(json.dumps({"mode_file": str(out), "bodies": summary}))


if __name__ == "__main__":
    main()
