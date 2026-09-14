"""Gathered gravity: does claim-and-gather focus a source's pull on whoever catches a piece?

A source emits, every tick, a train of negative quanta, one per ray over 512
mirrored headings, each tick's train with its own label. A single body at
distance r absorbs with a claiming rule: taking one ray of a train, it opens a
claim and gathers every ray of that train the flood can still reach, with its
amount x heading. Without the claim the body takes only the rays whose lines
cross its Node, the inverse-square pull of the signed-quanta gravity probe.
The pull per tick is read on the lattice axis and off it, at link speed, and
once at half pace, where the flood overtakes the whole train. The question is
the dark-matter one: does gathering make the pull fall slower than the inverse
square? Every number is a read-only world/event audit at host lattice
coordinates; no constant is identified.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

ROOT = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "gravity_probe", ROOT / "examples/gravity-probe/run_experiments.py"
)
assert _SPEC is not None and _SPEC.loader is not None
GRAVITY = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(GRAVITY)

SIZE = 21
CENTER = SIZE // 2
HEADINGS = 512
HEADING_SCALE = 24
TICKS = 60
WINDOW = 12
DISTANCES = (3, 5, 7, 9)
OFF_AXIS = (2, 1)  # the off-axis body sits at (r, 2, 1) from the source
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}


def document(
    distance: int,
    claim: bool,
    ticks: int = TICKS,
    off_axis: bool = False,
    pace: tuple[int, int] = (1, 1),
    headings: int = HEADINGS,
    size: int = SIZE,
) -> dict:
    center = size // 2
    offset = (distance, *OFF_AXIS) if off_axis else (distance, 0, 0)
    return {
        "schema_version": 1,
        "model_id": "gathered-gravity-probe-v1",
        "shape": [size] * 3,
        "boundary": "open",
        "slots_per_node": 1,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": [
            {
                "name": "quanta",
                "components": 1,
                "units": "quantum",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "train",
                "components": 1,
                "units": "label",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "source",
                "fields": ["quanta", "momentum", "train"],
                "defaults": {"quanta": 0, "momentum": [0, 0, 0], "train": 1},
                "transport": {"mode": "hold"},
                # Every tick's train carries its own label.
                "updates": [
                    {"field": "train", "expression": {"op": "add", "args": [{"field": "train"}, 1]}}
                ],
            },
            {
                "name": "body",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 10**6, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": GRAVITY.mirrored_headings(headings, HEADING_SCALE),
                "rays_per_tick": headings,
                "ray_slots": 4096,
                "pace": list(pace),
                "claim": {"ticks": 3 * ticks, "slots": 64},
            }
        ],
        "emissions": [
            {
                "type": "source",
                "field": "quanta",
                "amount": -headings,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "train_field": "train",
            }
        ],
        "spatial_couplings": [
            {
                "name": "body_absorbs",
                "type": "body",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
                "claim": claim,
            }
        ],
        "seeds": [
            {"position": [center] * 3, "type": "source"},
            {"position": [center + o for o in offset], "type": "body"},
        ],
    }


def pull(raw: dict) -> dict:
    """The body's momentum gain toward the source per tick, averaged over the last WINDOW ticks."""
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    gains = []
    previous = (0, 0, 0)
    body: dict[str, tuple[int, ...]] = {}
    for _ in range(raw["ticks"]):
        world.step()
        body = next(
            world.record_values(record)
            for node in world.nodes.values()
            for record in node.records
            if record is not None and record.type_index == 1
        )
        momentum = body["momentum"]
        gains.append(tuple(momentum[i] - previous[i] for i in range(3)))
        previous = tuple(momentum)
    seed = raw["seeds"][1]["position"]
    center = raw["shape"][0] // 2
    offset = [p - center for p in seed]
    length = math.sqrt(sum(o * o for o in offset))
    window = gains[-WINDOW:]
    toward = [-sum(g[i] * offset[i] for i in range(3)) / length for g in window]
    return {
        "offset": offset,
        "distance": round(length, 3),
        "claim": raw["spatial_couplings"][0]["claim"],
        "pace": raw["spatial_fields"][0]["pace"],
        "pull_per_tick": round(sum(toward) / WINDOW, 2),
        "last_gains": [round(t, 1) for t in toward],
        "paid": 10**6 - body["quanta"][0],
        "quanta_closed": world.totals()["quanta"][0] + world.escaped_totals()["quanta"][0] == initial,
    }


def slope(rows: list[dict]) -> float | None:
    return GRAVITY.fit_exponent([(row["distance"], row["pull_per_tick"]) for row in rows])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    tables = {}
    for name, off_axis in (("axis", False), ("off_axis", True)):
        for claim in (False, True):
            rows = [pull(document(d, claim, off_axis=off_axis)) for d in DISTANCES]
            key = f"{name}_{'claim' if claim else 'plain'}"
            tables[key] = {"rows": rows, "slope": slope(rows)}
            print(key, "slope", tables[key]["slope"])
            for row in rows:
                print(
                    "  r",
                    row["distance"],
                    "pull",
                    row["pull_per_tick"],
                    "paid",
                    row["paid"],
                    "closed",
                    row["quanta_closed"],
                    row["last_gains"][-4:],
                )
    half = pull(document(DISTANCES[1], True, pace=(1, 2)))
    print(
        "half pace, claim, r",
        half["distance"],
        "pull",
        half["pull_per_tick"],
        "paid",
        half["paid"],
        half["last_gains"][-4:],
    )
    report = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "headings": HEADINGS,
        "ticks": TICKS,
        "tables": tables,
        "half_pace_claim": half,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
