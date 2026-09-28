"""The books of a BELL run (the owner's word, 23:08Z): how the photon goes on the GameBoard, since some records wander and never reach a detector. This tool runs one world headless with the engine's event lines observed (the runner `tools/run_inputs.py` passes no observer, and parses the document without the mode file beside it, so it refuses every giver in the law's form; this tool loads through `load_world`, which hands the mode file), writes the runner's output beside the world as the runner does (`<name>.output.json`: the clicks, each with its `giver` (the body whose giving line wrote the record: the pump's clicks are the emitter's, the pair's the crystal's) and its two times as the click line carries them, `interval` the loop's step over the whole GameBoard and `clock` the detector's own count with `clock_source`, the owner's question of 23:12Z; the readings, the counts, the records alive), the event lines (`<name>.lines.json`) and the books (`<name>.books.json`): the pairs given by the crystal (the giving lines of a body with the key `crystal`), the labels that clicked at each detector, the labels that ended at a face or escaped, the labels left on the GameBoard at the end (HOST); THE DETECTOR'S SENSITIVITY, a GAMEBOARD reading labelled so: its clicks over the labels whose ladder reached its Nodes (a click line lists under `detectors` every set whose pointer the record filled); the losses per side, to be compared across the runs of the series: a loss that moves with the polariser's angle is Bell's detection loophole, so `losses_by_setting` is written per run with the side's setting (a fixed-angle chain has one setting per side; on a switching chain the setting of a lost label is not known to the tool, since a lost label has no click interval, and the run's losses are reported whole); and THE RECORD'S PATH (GAMEBOARD, a small run's diagnostic): per line of a `rows` reading the count of Nodes with a row, their bounding box and their centroid on the GameBoard, so the path of the record is read without the DETECTOR. Until the engine writes one click per label, a click line is a record's; every count here is per click line and says so. Run from the repository root: python examples/events/experiments/bell_books.py <world.json> [<world.json> ...]; nothing runs without the owner's word."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from event_universe.core.readings import Readings
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world

SIDES = {"left": ("left_plus", "left_minus"), "right": ("right_plus", "right_minus")}


def run(world_path: Path) -> dict[str, Any]:
    """One world run headless with the event lines observed; the runner's output, the lines and the books written beside the world; the books returned."""
    document = json.loads(world_path.read_text(encoding="utf-8"))
    world = load_world(
        world_path
    )  # the mode file beside the world handed with the files, as the host does
    lines: list[dict[str, Any]] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    readings = Readings(world.readings)
    readings.read(simulation)
    output: dict[str, Any] = {
        "format": "run-output-v1",
        "input": world_path.name,
        "name": world_path.stem,
        "verdict": "LAWFUL",
        "ticks": world.ticks,
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
            "clock": g["clock"],
            "clock_source": g["clock_source"],
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
        {
            "record": live.identity,
            "labels": [list(label) for label in live.labels],
            "giving": live.giving_tick,
        }
        for live in simulation.records.values()
    ]
    found = books(document, lines, alive, output)
    stem = world_path.with_suffix("")
    Path(f"{stem}.output.json").write_text(
        json.dumps(output, indent=1, sort_keys=True) + "\n", encoding="utf-8"
    )
    Path(f"{stem}.lines.json").write_text(json.dumps(lines) + "\n", encoding="utf-8")
    Path(f"{stem}.books.json").write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
    return found


def crystal_bodies(document: dict[str, Any]) -> set[int]:
    """The numbers of the bodies with the key `crystal`."""
    return {n for n, body in enumerate(document["measured"]) if "crystal" in body}


def settings_of(document: dict[str, Any]) -> dict[str, Any]:
    """Each side's polariser card as the file writes it (the exact pairs; no angle)."""
    found: dict[str, Any] = {}
    for body in document["measured"]:
        card = body.get("polariser")
        if card is not None:
            side = "left" if card["sets"][0].startswith("left") else "right"
            found[side] = {k: card[k] for k in ("angle", "angles", "every") if k in card}
    return found


def books(
    document: dict[str, Any],
    lines: list[dict[str, Any]],
    alive: list[dict[str, Any]],
    output: dict[str, Any],
) -> dict[str, Any]:
    """The books from the event lines: the givings and the pairs, the click lines per detector, the faces and the escapes, the records alive at the end, the sensitivity per detector (GAMEBOARD), the losses per side with the side's setting, and the record's path from the `rows` readings (GAMEBOARD)."""
    crystals = crystal_bodies(document)
    givings = [line for line in lines if line["event"] == "giving"]
    pairs = [g for g in givings if g["measured"] in crystals]
    pair_records = {g["record"] for g in pairs}
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
        elif name.startswith("face:"):
            faces[name] = faces.get(name, 0) + 1
        else:
            by_detector[name] = by_detector.get(name, 0) + 1
        for entry in click.get("detectors", []):
            set_name = entry[0][0][0]
            reached[set_name] = reached.get(set_name, 0) + 1
    sensitivity = {
        name: {
            "clicks": by_detector.get(name, 0),
            "reached": reached[name],
            "share": round(by_detector.get(name, 0) / reached[name], 4),
        }
        for name in sorted(reached)
        if not name.startswith("face:")
    }
    pair_clicks = [c for c in clicks if c["record"] in pair_records]
    losses: dict[str, Any] = {}
    cards = settings_of(document)
    for side, sets in SIDES.items():
        clicked = sum(
            1
            for c in pair_clicks
            if isinstance(c["chosen"], list) and c["chosen"] and c["chosen"][0][0] in sets
        )
        losses[side] = {
            "setting": cards.get(side),
            "pairs": len(pairs),
            "clicked": clicked,
            "lost": len(pairs) - clicked,
            "share_lost": round((len(pairs) - clicked) / len(pairs), 4) if pairs else None,
        }
    return {
        "label_note": "per click line; one click line per record until the engine writes one per label (then per label, the pair's record identity on both)",
        "givings": len(givings),
        "pairs_given": len(pairs),
        "clicked_by_detector": dict(sorted(by_detector.items())),
        "ended_at_faces": dict(sorted(faces.items())),
        "escaped_without_detector": escaped,
        "on_board_at_end": {
            "label": "HOST",
            "records": len(alive),
            "pair_records": sum(1 for a in alive if a["record"] in pair_records),
        },
        "sensitivity": {
            "label": "GAMEBOARD",
            "row": "clicks over the click lines whose ladder reached the set's Nodes (the pointer filled), per set",
            "by_detector": sensitivity,
        },
        "losses_by_setting": {
            "label": "GAMEBOARD",
            "row": "per side: the pairs whose click line fell on neither of the side's sets; compare across the series' runs: a loss that moves with the setting is the detection loophole",
            "sides": losses,
        },
        "path": {"label": "GAMEBOARD", "rows": path(document, output)},
    }


def path(document: dict[str, Any], output: dict[str, Any]) -> list[dict[str, Any]]:
    """The record's path from every `rows` reading: per line the Nodes with a row, their bounding box and centroid on the GameBoard's shape."""
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


def main() -> None:
    for argument in sys.argv[1:]:
        found = run(Path(argument).resolve())
        print(json.dumps({k: v for k, v in found.items() if k != "path"}, indent=1))


if __name__ == "__main__":
    main()
