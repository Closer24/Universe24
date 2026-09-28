"""The centroid of a beam at a screen, read from the strips' clicks alone (ALGEBRA.md #the-rows-against-nature (b) THE BENDING): the screen carries one detector per strip across the beam (the world file's `detectors` whose names share the expectation file's `CENTROID.strips` prefix), each click is the strip's (the engine's `counts` per detector, a DETECTOR reading), and the centroid is the click-weighted mean of the strips' coordinate along the one axis on which the strips differ, an exact fraction in Nodes; with a twin input (the same beam and screen, no heavy body) the shift is this centroid minus the twin's, compared with the expectation's `shift` within its `band` when the expectation names one (MATCH or MISS), else reported as a first look. The books beside it: the clicks in the strips, at the face and elsewhere, the records alive. Nothing here replays a rule and nothing is compared with nature. Run from the repository root: python tools/beam_centroid.py <world.json> <world.output.json> [<twin.json> <twin.output.json>]; the report is printed and written beside the first output as <name>.centroid.json."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


def strips_of(world: dict[str, Any], prefix: str) -> dict[str, list[int]]:
    """The strips: each detector whose name starts with the prefix, with the one Node its positions name (a strip of several Nodes takes their mean, exact only when written as a list of one)."""
    found: dict[str, list[int]] = {}
    for detector in world["detectors"]:
        name = str(detector["name"])
        if name.startswith(prefix):
            positions = detector["positions"]
            found[name] = [sum(int(p[axis]) for p in positions) for axis in range(3)]
            found[name] = [part // len(positions) for part in found[name]]
    if not found:
        raise ValueError(f"no detector of the world is named with the prefix {prefix!r}")
    return found


def strip_axis(strips: dict[str, list[int]]) -> int:
    """The one axis on which the strips' Nodes differ; refused where they differ on none or on more than one."""
    axes = [axis for axis in range(3) if len({node[axis] for node in strips.values()}) > 1]
    if len(axes) != 1:
        raise ValueError(f"the strips differ on the axes {axes}; the centroid needs exactly one")
    return axes[0]


def centroid(world: dict[str, Any], output: dict[str, Any], prefix: str) -> dict[str, Any]:
    """The click-weighted centroid of the strips along their axis (an exact fraction, None with no click), with the run's books: the clicks in the strips, at the face, elsewhere, and the records alive."""
    strips = strips_of(world, prefix)
    axis = strip_axis(strips)
    counts = {str(name): int(count) for name, count in output.get("counts", {}).items()}
    in_strips = sum(counts.get(name, 0) for name in strips)
    weighted = sum(counts.get(name, 0) * node[axis] for name, node in strips.items())
    mean = Fraction(weighted, in_strips) if in_strips else None
    face = sum(count for name, count in counts.items() if name == "face")
    return {
        "axis": "xyz"[axis],
        "centroid": None if mean is None else [mean.numerator, mean.denominator],
        "clicks_in_strips": in_strips,
        "clicks_at_the_face": face,
        "clicks_elsewhere": sum(counts.values()) - in_strips - face,
        "records_alive": output.get("records_alive"),
    }


def report(pairs: list[tuple[Path, Path]]) -> dict[str, Any]:
    """The report of the first world against its expectation's `CENTROID` section, the twin's centroid from the second pair where given: the shift (first minus twin, exact) and its verdict within the band, or a first look where the expectation's `shift` is None."""
    world_path, output_path = pairs[0]
    world = json.loads(world_path.read_text(encoding="utf-8"))
    output = json.loads(output_path.read_text(encoding="utf-8"))
    expectation_path = world_path.with_suffix(".expectation.json")
    expectation = json.loads(expectation_path.read_text(encoding="utf-8")).get("CENTROID", {})
    prefix = str(expectation.get("strips", "screen_"))
    found: dict[str, Any] = {
        "input": world_path.stem,
        "kind": "DETECTOR",
        "this": centroid(world, output, prefix),
    }
    if len(pairs) > 1:
        twin_world = json.loads(pairs[1][0].read_text(encoding="utf-8"))
        twin_output = json.loads(pairs[1][1].read_text(encoding="utf-8"))
        found["twin"] = {"input": pairs[1][0].stem, **centroid(twin_world, twin_output, prefix)}
        here, there = found["this"]["centroid"], found["twin"]["centroid"]
        if here is not None and there is not None:
            shift = Fraction(*here) - Fraction(*there)
            found["shift"] = [shift.numerator, shift.denominator]
            expected = expectation.get("shift")
            if expected is None:
                found["verdict"] = "FIRST LOOK: no shift expected yet"
            else:
                within = abs(shift - Fraction(expected)) <= Fraction(expectation.get("band", 1))
                found["expected"], found["band"] = expected, expectation.get("band", 1)
                found["verdict"] = "MATCH" if within else "MISS"
    return found


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 4):
        print(__doc__.splitlines()[-1])
        return 2
    pairs = [(Path(argv[i]), Path(argv[i + 1])) for i in range(0, len(argv), 2)]
    found = report(pairs)
    text = json.dumps(found, indent=1)
    print(text)
    pairs[0][1].with_name(f"{pairs[0][0].stem}.centroid.json").write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
