"""THE READING OF THE TWO SLITS (g) and of de Broglie's fringes (j): one world run headless through the engine's own functions (`load_world` hands the mode file beside the world, `DetectorLawSimulation` steps it, the event lines observed), the runner's output written beside the world as `tools/run_inputs.py` writes it (`<name>.output.json`), and the reading: THE STRIPS' SHARES, a DETECTOR reading, the clicks per strip in the strips' order along the screen and each strip's share of the clicks that fell on the screen, compared with the expectation file's `strips` section where it carries one (inside or outside its band; the cosine and every closed form live only in the expectation, never here); THE BOOKS: the quanta given (the giver's giving lines), the clicks per detector, the records ended at a face, the records left on the GameBoard at the end (HOST); THE SENSITIVITY per strip by the ladder (GAMEBOARD: clicks over the click lines whose ladder reached the strip's Nodes); THE RECORD'S PATH from every `rows` reading (GAMEBOARD: the Nodes with a row, their box and centroid). Nothing here replays a rule and no number of a run enters a test. Run from the repository root: PYTHONPATH=src python examples/events/experiments/de_broglie/two_slits_strips.py <world.json> [--first-look]; a run before the blind expectation is a first look and is labelled so."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from event_universe.core.readings import Readings
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world

FACE_PREFIX = "face:"


def run(world_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    """One world run headless with the event lines observed; the runner's output, the lines and the records alive at the end."""
    world = load_world(world_path)
    lines: list[dict[str, Any]] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    readings = Readings(world.readings)
    readings.read(simulation)
    output: dict[str, Any] = {
        "format": "one-command-output-v1",
        "input": world_path.name,
        "name": world_path.stem,
        "verdict": "LAWFUL",
        "step": {"hash": world.step.digest},
        "ticks": world.ticks,
        "mode": world.start.mode if world.start is not None else None,
    }
    for _ in range(world.ticks):
        simulation.step()
        leaks = simulation.leaks()
        if leaks:
            output["verdict"] = "LEAK"
            output["reason"] = (
                f"the families {leaks} carry rows without a source at interval {simulation.tick}"
            )
            break
        readings.read(simulation)
    readings.clicks(simulation.layer.gathers, world.detectors)
    giver_of = {line["record"]: line["measured"] for line in lines if line["event"] == "giving"}
    output["clicks"] = [
        {
            "detector": g["chosen"][0][0] if isinstance(g["chosen"], list) and g["chosen"] else None,
            "interval": g["click"],
            "clock": g.get("clock"),
            "giving": g["giving"],
            "record": g["record"],
            "giver": giver_of.get(g["record"]),
        }
        for g in simulation.layer.gathers
    ]
    output["counts"] = {d.name: 0 for d in world.detectors}
    for click in output["clicks"]:
        if isinstance(click["detector"], str):
            output["counts"][click["detector"]] = output["counts"].get(click["detector"], 0) + 1
    output["readings"] = readings.output()
    output["records_alive"] = len(simulation.records)
    alive = [
        {"record": live.identity, "giving": live.giving_tick}
        for live in simulation.records.values()
        if live.identity in giver_of  # the given records alone; a body's own record is no quantum given
    ]
    return output, lines, alive


def strips_of(document: dict[str, Any]) -> list[dict[str, Any]]:
    """The strips: the detectors whose set lies on the screen, in the order of their lowest y (the screen's own face, one strip each)."""
    strips = [d for d in document["detectors"] if "positions" in d]
    return sorted(strips, key=lambda d: min(p[1] for p in d["positions"]))


def strip_shares(
    document: dict[str, Any], output: dict[str, Any], expectation: dict[str, Any]
) -> dict[str, Any]:
    """THE STRIPS' SHARES, a DETECTOR reading: the clicks per strip along the screen, each strip's share of the screen's clicks, against the expectation's `strips` where written (inside or outside the band)."""
    strips = strips_of(document)
    counts = output["counts"]
    on_screen = sum(counts.get(s["name"], 0) for s in strips)
    expected = {e["detector"]: e for e in expectation.get("strips", [])}
    rows = []
    for strip in strips:
        clicks = counts.get(strip["name"], 0)
        row: dict[str, Any] = {
            "detector": strip["name"],
            "y": [min(p[1] for p in strip["positions"]), max(p[1] for p in strip["positions"])],
            "clicks": clicks,
            "share": round(clicks / on_screen, 4) if on_screen else None,
        }
        if strip["name"] in expected:
            pin = expected[strip["name"]]
            row["expected_count"] = pin["count"]
            row["band"] = pin["band"]
            row["verdict"] = (
                "INSIDE" if abs(clicks - int(pin["count"])) <= int(pin["band"]) else "OUTSIDE"
            )
        rows.append(row)
    verdicts = [r["verdict"] for r in rows if "verdict" in r]
    return {
        "label": "DETECTOR",
        "row": "the clicks per strip along the screen and each strip's share of the screen's clicks; the expectation's count and band per strip where written before the run",
        "clicks_on_screen": on_screen,
        "strips": rows,
        "inside": verdicts.count("INSIDE"),
        "outside": verdicts.count("OUTSIDE"),
    }


def books(
    document: dict[str, Any],
    lines: list[dict[str, Any]],
    alive: list[dict[str, Any]],
    output: dict[str, Any],
) -> dict[str, Any]:
    """THE BOOKS: the quanta given, the clicks per detector, the records ended at a face, the records left on the GameBoard (HOST); the sensitivity per strip by the ladder and the record's path (GAMEBOARD)."""
    givings = [line for line in lines if line["event"] == "giving"]
    clicks = [line for line in lines if line["event"] == "gather"]
    by_detector: dict[str, int] = {}
    reached: dict[str, int] = {}
    faces: dict[str, int] = {}
    escaped = 0
    for click in clicks:
        chosen = click["chosen"]
        name = chosen[0][0] if isinstance(chosen, list) and chosen else None
        if name is None:
            escaped += 1
        elif name.startswith(FACE_PREFIX):
            faces[name] = faces.get(name, 0) + 1
        else:
            by_detector[name] = by_detector.get(name, 0) + 1
        for entry in click.get("detectors", []):
            set_name = entry[0][0][0]
            reached[set_name] = reached.get(set_name, 0) + 1
    strips = [s["name"] for s in strips_of(document)]
    sensitivity = {
        name: {
            "clicks": by_detector.get(name, 0),
            "reached": reached.get(name, 0),
            "share": round(by_detector.get(name, 0) / reached[name], 4) if reached.get(name) else None,
        }
        for name in strips
    }
    givers: dict[int, int] = {}
    for giving in givings:
        givers[giving["measured"]] = givers.get(giving["measured"], 0) + 1
    return {
        "quanta_given": len(givings),
        "givings_by_body": givers,
        "clicked_by_detector": dict(sorted(by_detector.items())),
        "clicks_on_screen": sum(by_detector.get(name, 0) for name in strips),
        "ended_at_faces": dict(sorted(faces.items())),
        "escaped_without_detector": escaped,
        "on_board_at_end": {"label": "HOST", "records": len(alive)},
        "balance": {
            "row": "the quanta given = the clicks at the strips + at the faces + escaped + the records on the GameBoard at the end",
            "given": len(givings),
            "accounted": sum(by_detector.values()) + sum(faces.values()) + escaped + len(alive),
        },
        "sensitivity": {
            "label": "GAMEBOARD",
            "row": "per strip: clicks over the click lines whose ladder reached the strip's Nodes",
            "by_strip": sensitivity,
        },
        "path": {"label": "GAMEBOARD", "rows": path(document, output)},
    }


def path(document: dict[str, Any], output: dict[str, Any]) -> list[dict[str, Any]]:
    """THE RECORD'S PATH from every `rows` reading (GAMEBOARD): per line the Nodes with a row, their bounding box and their centroid on the GameBoard's shape."""
    shape = document["shape"]
    found: list[dict[str, Any]] = []
    for reading in output.get("readings", []):
        if reading["kind"] != "rows":
            continue
        for line in reading["lines"]:
            occupied = [(i, v) for i, v in enumerate(line["rows"]) if v]
            if not occupied:
                found.append({"reading": reading["name"], "interval": line["interval"], "nodes": 0})
                continue
            nodes = [
                (i // (shape[1] * shape[2]), (i // shape[2]) % shape[1], i % shape[2])
                for i, _ in occupied
            ]
            weights = [abs(v) for _, v in occupied]
            total = sum(weights)
            found.append(
                {
                    "reading": reading["name"],
                    "interval": line["interval"],
                    "nodes": len(nodes),
                    "box": [[min(n[k] for n in nodes), max(n[k] for n in nodes)] for k in range(3)],
                    "centroid": [
                        round(sum(n[k] * w for n, w in zip(nodes, weights, strict=True)) / total, 2)
                        for k in range(3)
                    ],
                }
            )
    return found


def read(world_path: Path, first_look: bool) -> dict[str, Any]:
    """The whole reading of one world: the run, the output beside the world, the strips' shares, the books; the report returned."""
    document = json.loads(world_path.read_text(encoding="utf-8"))
    expectation_path = world_path.with_suffix(".expectation.json")
    expectation = (
        json.loads(expectation_path.read_text(encoding="utf-8")) if expectation_path.exists() else {}
    )
    output, lines, alive = run(world_path)
    stem = world_path.with_suffix("")
    Path(f"{stem}.output.json").write_text(
        json.dumps(output, indent=1, sort_keys=True) + "\n", encoding="utf-8"
    )
    Path(f"{stem}.lines.json").write_text(json.dumps(lines) + "\n", encoding="utf-8")
    report = {
        "world": world_path.name,
        "kind": "FIRST LOOK (before the blind expectation)"
        if first_look or not expectation.get("strips")
        else "the experiment against its blind expectation",
        "verdict": output["verdict"],
        "step": output["step"],
        "ticks": output["ticks"],
        "shares": strip_shares(document, output, expectation),
        "books": books(document, lines, alive, output),
    }
    Path(f"{stem}.books.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("worlds", nargs="+", type=Path, help="the world files")
    parser.add_argument(
        "--first-look",
        action="store_true",
        help="label the reading a first look: no blind expectation yet",
    )
    args = parser.parse_args()
    for world_path in args.worlds:
        report = read(world_path.resolve(), args.first_look)
        shown = dict(report)
        shown["books"] = {k: v for k, v in report["books"].items() if k != "path"}
        print(json.dumps(shown, indent=1))


if __name__ == "__main__":
    main()
