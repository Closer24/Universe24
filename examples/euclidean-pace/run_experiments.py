"""Euclidean pace: rays that wait at a Node so every heading covers equal distance per tick.

On the links metric a ray hops one link every tick, so a wave front reaches
Manhattan distance `t` in every heading after `t` ticks: an octahedron whose
Euclidean radius is `t` along an axis and `t / sqrt 3` along a body diagonal.
With `"metric": "euclidean"` a ray hops only when its wait passes its heading's
pace, the slowest heading hopping every tick, so every heading covers the same
Euclidean distance per tick and the front is round. Two probes: one lamp on
the 26 neighbor headings measures the front's radius per heading class; two
lamps in phase behind a line of readers measure where the fringe minima fall,
which on the links metric follow Manhattan path difference (constant beyond the
lamps' separation) and on the Euclidean metric follow the Euclidean one.
Every number is a read-only world/event audit at host lattice coordinates; no
length unit or constant is identified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from itertools import product
from math import gcd
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

FRONT_SIZE = 29
FRONT_CENTER = FRONT_SIZE // 2
FRONT_TICKS = 12
PLANE_WIDTH = 41
PLANE_CENTER = PLANE_WIDTH // 2
SCREEN_OFFSET = 12
HALF_SEPARATION = 2
SCREEN_HALF = 12
PHASE_STEPS = 64
ADVANCE = 16
PER_RAY = 4
FRINGE_TICKS = 40
WINDOW = 8
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}
NEIGHBOR_HEADINGS = [list(h) for h in product((-1, 0, 1), repeat=3) if any(h)]


def screen_headings() -> list[list[int]]:
    """One primitive heading from each lamp to every reader on the screen line."""
    result: list[list[int]] = []
    for n in range(-SCREEN_HALF - HALF_SEPARATION, SCREEN_HALF + HALF_SEPARATION + 1):
        g = gcd(abs(n), SCREEN_OFFSET)
        heading = [n // g, SCREEN_OFFSET // g, 0]
        if heading not in result:
            result.append(heading)
    return result


def _fields() -> list[dict]:
    return [
        {
            "name": "quanta",
            "components": 1,
            "units": "quantum",
            "signed": False,
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
    ]


def front_document(metric: str, ticks: int = FRONT_TICKS) -> dict:
    per_tick = len(NEIGHBOR_HEADINGS)
    return {
        "schema_version": 1,
        "model_id": "euclidean-pace-front-probe-v1",
        "shape": [FRONT_SIZE, FRONT_SIZE, FRONT_SIZE],
        "boundary": "open",
        "slots_per_node": 1,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": _fields(),
        "disturbance_types": [
            {
                "name": "lamp",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": per_tick * ticks, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": NEIGHBOR_HEADINGS,
                "rays_per_tick": per_tick,
                "ray_slots": 32,
                "metric": metric,
            }
        ],
        "emissions": [
            {
                "type": "lamp",
                "field": "quanta",
                "amount": per_tick,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            }
        ],
        "seeds": [{"position": [FRONT_CENTER] * 3, "type": "lamp"}],
    }


def front(raw: dict) -> dict:
    """The farthest Node holding a ray of each heading class after the run."""
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    for _ in range(raw["ticks"]):
        world.step()
    headings = raw["spatial_fields"][0]["headings"]
    farthest: dict[int, tuple[int, int]] = {}
    for node in world.inventory_view().nodes:
        for ray in node.rays[0] if node.rays else ():
            offset = [p - FRONT_CENTER for p in node.position]
            manhattan = sum(abs(o) for o in offset)
            squared = sum(o * o for o in offset)
            if manhattan > farthest.get(ray.heading, (0, 0))[0]:
                farthest[ray.heading] = (manhattan, squared)
    classes: dict[str, list[float]] = {"axis": [], "face": [], "body": []}
    links: dict[str, list[int]] = {"axis": [], "face": [], "body": []}
    for index, heading in enumerate(headings):
        name = ("axis", "face", "body")[sum(abs(c) for c in heading) - 1]
        manhattan, squared = farthest[index]
        classes[name].append(math.sqrt(squared))
        links[name].append(manhattan)
    radii = {name: sorted(set(values)) for name, values in classes.items()}
    every = [r for values in classes.values() for r in values]
    return {
        "metric": raw["spatial_fields"][0]["metric"],
        "ticks": raw["ticks"],
        "links": {name: sorted(set(values)) for name, values in links.items()},
        "radius": {name: [round(v, 2) for v in values] for name, values in radii.items()},
        "spread": round(max(every) / min(every), 3),
        "quanta_closed": world.totals()["quanta"][0] + world.escaped_totals()["quanta"][0] == initial,
    }


def fringe_document(metric: str, ticks: int = FRINGE_TICKS, phased: bool = True) -> dict:
    headings = screen_headings()
    per_tick = len(headings) * PER_RAY
    field = {
        "field": "quanta",
        "baseline": 0,
        "transport": "ray",
        "headings": headings,
        "rays_per_tick": len(headings),
        "ray_slots": 32,
        "metric": metric,
    }
    if phased:
        field["kerengonen"] = {"phase_steps": PHASE_STEPS, "phase_advance": ADVANCE}
    return {
        "schema_version": 1,
        "model_id": "euclidean-pace-fringe-probe-v1",
        "shape": [PLANE_WIDTH, SCREEN_OFFSET + 4, 3],
        "boundary": "open",
        "slots_per_node": 1,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": _fields(),
        "disturbance_types": [
            {
                "name": "lamp",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": per_tick * ticks, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [field],
        "emissions": [
            {
                "type": "lamp",
                "field": "quanta",
                "amount": per_tick,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            }
        ],
        "seeds": [
            {"position": [PLANE_CENTER - HALF_SEPARATION, 1, 1], "type": "lamp"},
            {"position": [PLANE_CENTER + HALF_SEPARATION, 1, 1], "type": "lamp"},
        ],
    }


def predicted_minima(metric: str) -> list[int]:
    """Screen positions where the two lamps' phases differ by a half turn."""
    result = []
    for x in range(-SCREEN_HALF, SCREEN_HALF + 1):
        a = (x + HALF_SEPARATION, SCREEN_OFFSET)
        b = (x - HALF_SEPARATION, SCREEN_OFFSET)
        if metric == "links":
            difference = float(abs(a[0]) + a[1] - abs(b[0]) - b[1])
        else:
            # Every heading moves at the slowest heading's Euclidean speed, sqrt 2 / 2
            # link-lengths per tick for this set, so ticks are sqrt 2 x distance.
            difference = math.sqrt(2) * (math.hypot(*a) - math.hypot(*b))
        steps = (ADVANCE * difference) % PHASE_STEPS
        if abs(steps - PHASE_STEPS / 2) <= ADVANCE / 2:
            result.append(x)
    return result


def fringe(raw: dict) -> dict:
    """Readings along the screen line summed over the last WINDOW ticks."""
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    y = 1 + SCREEN_OFFSET
    readings = {x: 0 for x in range(-SCREEN_HALF, SCREEN_HALF + 1)}
    for tick in range(raw["ticks"]):
        world.step()
        if tick >= raw["ticks"] - WINDOW:
            for x in readings:
                readings[x] += world.spatial_values((PLANE_CENTER + x, y, 1))["quanta"]["value"][0]
    darkest = min(readings.values())
    return {
        "metric": raw["spatial_fields"][0]["metric"],
        "phased": "kerengonen" in raw["spatial_fields"][0],
        "readings": readings,
        "darkest": [x for x, value in readings.items() if value == darkest],
        "quanta_closed": world.totals()["quanta"][0] + world.escaped_totals()["quanta"][0] == initial,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    fronts = [front(front_document(metric)) for metric in ("links", "euclidean")]
    fringes = [fringe(fringe_document(metric)) for metric in ("links", "euclidean")]
    plain = fringe(fringe_document("euclidean", phased=False))
    report = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "screen_headings": len(screen_headings()),
        "phase_steps": PHASE_STEPS,
        "advance": ADVANCE,
        "fronts": fronts,
        "fringes": fringes,
        "plain": plain,
        "predicted_minima": {metric: predicted_minima(metric) for metric in ("links", "euclidean")},
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    for result in fronts:
        print("front", result["metric"], "links", result["links"], "radius", result["radius"])
        print("  spread", result["spread"], "closed", result["quanta_closed"])
    for result in fringes:
        print(
            "fringe",
            result["metric"],
            "darkest",
            result["darkest"],
            "predicted minima",
            predicted_minima(result["metric"]),
        )
        print("  readings", list(result["readings"].values()), "closed", result["quanta_closed"])
    print("plain", list(plain["readings"].values()), "closed", plain["quanta_closed"])
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
