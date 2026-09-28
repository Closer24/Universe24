"""The families a world touches, computed from the world file and its universe file, never by hand (the owner's word, 21:47Z): the bodies' own families; the families they hold (a held row whose count word is `content` is held by every body, one whose count word is `sign` by the bodies of a signed family); the families they give (the emitters') and take (the given family at every set); then the closure over the universe rows' `reads` (a family read by a touched family is touched). The list is written into the world's `.expectation.json` as `families`, and a GAMEBOARD check per untouched family says its levels stay 0 at every Node (a nonzero level there is a finding that names the family). Run from the repository root: python examples/events/experiments/families_touched.py <world.json> [...]."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]


def touched_families(world: dict[str, Any], universe: dict[str, Any]) -> dict[str, list[str]]:
    """The touched families by the way each is touched, and the untouched rest of the universe's rows."""
    rows = {row["name"]: row for row in universe["families"]}
    own = sorted({body["family"] for body in world["measured"]})
    signed = {name for name in own if rows[name].get("sign", 0) != 0}
    held = sorted(
        name
        for name, row in rows.items()
        if "held" in row
        and (row["held"].get("count") == "content" or (row["held"].get("count") == "sign" and signed))
    )
    given = sorted({body["emitter"]["family"] for body in world["measured"] if "emitter" in body})
    taken = given if world.get("detectors") else []
    touched = set(own) | set(held) | set(given) | set(taken)
    read: set[str] = set()
    frontier = set(touched)
    while frontier:
        name = frontier.pop()
        for entry in rows[name].get("reads", []):
            if entry["family"] not in touched:
                touched.add(entry["family"])
                read.add(entry["family"])
                frontier.add(entry["family"])
    return {
        "own": own,
        "held": held,
        "given": given,
        "taken": taken,
        "read": sorted(read),
        "touched": sorted(touched),
        "untouched": sorted(name for name in rows if name not in touched),
    }


def write_into_expectation(world_path: Path) -> dict[str, list[str]]:
    """Compute the families of the world at the path and write them into its expectation file, with the untouched families' GAMEBOARD checks."""
    world = json.loads(world_path.read_text(encoding="utf-8"))
    universe = json.loads((ROOT / world["universe"]).read_text(encoding="utf-8"))
    families = touched_families(world, universe)
    expectation_path = world_path.with_suffix(".expectation.json")
    expectation = json.loads(expectation_path.read_text(encoding="utf-8"))
    expectation["families"] = families
    checks = [
        check for check in expectation.get("GAMEBOARD_checks", []) if "untouched family" not in check
    ]
    for name in families["untouched"]:
        checks.append(
            f"the untouched family `{name}`: its levels stay 0 at every Node over the run (a `total` reading of "
            f"the family reads 0 at every stride); a nonzero level there is a finding that names the family"
        )
    if not families["untouched"]:
        checks.append(
            "no untouched family: every row of the universe file is touched (own, held, given, taken or read), "
            "so a difference in the DETECTOR numbers on the full universe comes from a touched family by construction"
        )
    expectation["GAMEBOARD_checks"] = checks
    expectation_path.write_text(json.dumps(expectation, indent=1) + "\n", encoding="utf-8")
    return families


def main() -> None:
    for argument in sys.argv[1:]:
        path = Path(argument).resolve()
        families = write_into_expectation(path)
        print(
            f"{path.relative_to(ROOT).as_posix()}: touched {families['touched']}, untouched {families['untouched']}"
        )


if __name__ == "__main__":
    main()
