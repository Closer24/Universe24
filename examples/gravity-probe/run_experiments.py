"""Gravity probe: mass-proportional attraction toward a straight-ray source.

Configuration only; no engine law is added. A stationary source emits the
straight-ray field `radiation`. A held test body of mass m responds through an
`exchange` coupling whose amount is `m * flux(radiation) / D`, so its momentum
moves toward the source (the flux points away from it) by m times the delivered
flux. The equal-and-opposite reaction lands in the local momentum field at the
body's Node. Every number reported here is a read-only world/event audit at host
Euclidean distance; no operational observer is modeled.

Measured: momentum gained per tick per unit mass (the host's "acceleration")
against distance and direction, its independence from the mass, and a moving
body that falls inward under the same rule.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

SIZE = 41
CENTER = SIZE // 2
STRENGTH = 4096
HEADINGS = 4096
HEADING_SCALE = 24
RAYS_PER_TICK = 64
DENOMINATOR = 16
MASSES = (1, 2, 4)
FALL_SCALE = 64
FALL_TICKS = 256
DIRECTIONS = {"axis": (1, 0, 0), "face_diagonal": (1, 1, 0), "body_diagonal": (1, 1, 1)}
STEPS = {"axis": (2, 4, 6, 8, 12), "face_diagonal": (2, 4, 6, 8), "body_diagonal": (2, 3, 4, 5)}


def golden_headings(count: int, scale: int) -> list[list[int]]:
    ratio = (1 + 5**0.5) / 2
    result = []
    for i in range(count):
        z = 1 - 2 * (i + 0.5) / count
        radius = math.sqrt(1 - z * z)
        angle = 2 * math.pi * i / ratio
        heading = [
            round(scale * radius * math.cos(angle)),
            round(scale * radius * math.sin(angle)),
            round(scale * z),
        ]
        result.append(heading if any(heading) else [scale, 0, 0])
    return result


def base_document(ticks: int) -> dict:
    return {
        "schema_version": 1,
        "model_id": "ray-gravity-host-probe-v1",
        "shape": [SIZE, SIZE, SIZE],
        "boundary": "open",
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {
                "name": "strength",
                "components": 1,
                "units": "source units per tick",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "radiation",
                "components": 1,
                "units": "ray unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "mass",
                "components": 1,
                "units": "mass unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "momentum unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "source",
                "fields": ["strength"],
                "defaults": {"strength": STRENGTH},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "radiation",
                "baseline": 0,
                "transport": "ray",
                "headings": golden_headings(HEADINGS, HEADING_SCALE),
                "rays_per_tick": RAYS_PER_TICK,
                "ray_slots": 512,
            },
            {"field": "momentum", "baseline": [0, 0, 0], "transport": "local"},
        ],
        "emissions": [
            {
                "type": "source",
                "field": "radiation",
                "amount": {"field": "strength"},
                "denominator": 1,
                "source": True,
            }
        ],
        "spatial_couplings": [],
        "seeds": [{"position": [CENTER] * 3, "type": "source"}],
    }


def attraction(type_name: str) -> dict:
    """Momentum change is -(mass * flux) / D: toward the source, proportional to mass."""
    return {
        "name": f"attract_{type_name}",
        "type": type_name,
        "field": "momentum",
        "mode": "exchange",
        "amount": {"op": "mul", "args": [{"field": "mass"}, {"flux": "radiation"}]},
        "denominator": DENOMINATOR,
    }


def held_document(ticks: int) -> dict:
    raw = base_document(ticks)
    raw["disturbance_types"].append(
        {
            "name": "held_body",
            "fields": ["mass", "momentum"],
            "defaults": {"mass": 1, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        }
    )
    raw["spatial_couplings"].append(attraction("held_body"))
    for name, direction in DIRECTIONS.items():
        for k in STEPS[name]:
            position = [CENTER + k * d for d in direction]
            for mass in MASSES:
                raw["seeds"].append(
                    {"position": position, "type": "held_body", "values": {"mass": mass}}
                )
    return raw


def falling_document(ticks: int, mass: int, start: int) -> dict:
    """One moving body: rate min(1, |p| / (mass * FALL_SCALE)) hops per tick along its momentum.

    The scale keeps the body well below one hop per tick, so rays can still
    reach it on the way out; a body moving at link speed outruns the field.
    """
    raw = base_document(ticks)
    raw["disturbance_types"].append(
        {
            "name": "falling_body",
            "fields": ["mass", "momentum"],
            "defaults": {"mass": mass, "momentum": [0, 0, 0]},
            "transport": {
                "mode": "move",
                "direction_field": "momentum",
                "rate": {
                    "op": "min",
                    "args": [
                        mass * FALL_SCALE,
                        {"op": "sum", "args": [{"op": "abs", "args": [{"field": "momentum"}]}]},
                    ],
                },
                "rate_denominator": mass * FALL_SCALE,
            },
        }
    )
    raw["spatial_couplings"].append(attraction("falling_body"))
    raw["seeds"].append({"position": [CENTER + start, CENTER, CENTER], "type": "falling_body"})
    return raw


def euclid(o) -> float:
    return math.sqrt(sum(v * v for v in o))


def bodies(world: Simulation, type_index: int) -> list[tuple[tuple[int, int, int], dict]]:
    found = []
    for position, node in world.nodes.items():
        for record in node.records:
            if record is not None and record.type_index == type_index:
                found.append((position, world.record_values(record)))
    for packets in world.links.values():
        for packet in packets:
            if packet is not None and packet.record.type_index == type_index:
                found.append((None, world.record_values(packet.record)))
    return found


def held_table(ticks_measured: int) -> tuple[list[dict], dict]:
    warm = HEADINGS // RAYS_PER_TICK
    raw = held_document(warm + ticks_measured)
    world = Simulation(parse_initial_state(raw))
    for _ in range(warm):
        world.step()
    baseline_masses = {}
    for position, node in world.nodes.items():
        for record in node.records:
            if record is not None and record.type_index == 1:
                baseline_masses[(position, world.record_values(record)["mass"][0])] = (
                    world.record_values(record)["momentum"]
                )
    for _ in range(ticks_measured):
        world.step()
    rows = []
    for position, node in world.nodes.items():
        for record in node.records:
            if record is None or record.type_index != 1:
                continue
            values = world.record_values(record)
            mass = values["mass"][0]
            before = baseline_masses[(position, mass)]
            gained = tuple(a - b for a, b in zip(values["momentum"], before, strict=True))
            offset = tuple(v - CENTER for v in position)
            r = euclid(offset)
            radial = sum(g * o for g, o in zip(gained, offset, strict=True)) / r
            name = next(
                n
                for n, d in DIRECTIONS.items()
                if all(o * d[0] == offset[0] * dd for o, dd in zip(offset, d, strict=True))
                and offset != (0, 0, 0)
            )
            rows.append(
                {
                    "direction": name,
                    "euclidean_r": round(r, 4),
                    "mass": mass,
                    "momentum_gained": gained,
                    "radial_momentum_per_tick": round(radial / ticks_measured, 4),
                    "acceleration": round(radial / ticks_measured / mass, 5),
                    "acceleration_times_r2_times_D_over_emission": round(
                        -radial / ticks_measured / mass * r * r * DENOMINATOR / STRENGTH, 5
                    ),
                }
            )
    rows.sort(key=lambda row: (row["direction"], row["euclidean_r"], row["mass"]))
    totals = {
        "momentum_total": world.totals()["momentum"],
        "conserved": world.totals()["momentum"] == (0, 0, 0),
    }
    return rows, totals


def fit_exponent(points: list[tuple[float, float]]) -> float | None:
    usable = [(math.log(r), math.log(v)) for r, v in points if v > 0 and r > 0]
    if len(usable) < 2:
        return None
    n = len(usable)
    mx = sum(x for x, _ in usable) / n
    my = sum(y for _, y in usable) / n
    sxx = sum((x - mx) ** 2 for x, _ in usable)
    sxy = sum((x - mx) * (y - my) for x, y in usable)
    return sxy / sxx if sxx else None


def fall_trajectory(mass: int, start: int, ticks: int) -> list[dict]:
    raw = falling_document(ticks, mass, start)
    world = Simulation(parse_initial_state(raw))
    trajectory = []
    for tick in range(1, ticks + 1):
        world.step()
        found = bodies(world, 1)
        if not found:
            trajectory.append({"tick": tick, "escaped": True})
            break
        position, values = found[0]
        trajectory.append(
            {
                "tick": tick,
                "x_offset": None if position is None else position[0] - CENTER,
                "momentum": values["momentum"],
            }
        )
    return trajectory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    measured = HEADINGS // RAYS_PER_TICK
    rows, totals = held_table(measured)
    fits = {
        name: fit_exponent(
            [
                (row["euclidean_r"], -row["acceleration"])
                for row in rows
                if row["direction"] == name and row["mass"] == 1
            ]
        )
        for name in DIRECTIONS
    }
    mass_ratios = {}
    for row in rows:
        key = (row["direction"], row["euclidean_r"])
        mass_ratios.setdefault(key, {})[row["mass"]] = row["acceleration"]
    equivalence = [
        {
            "direction": d,
            "euclidean_r": r,
            "acceleration_by_mass": {str(m): a for m, a in sorted(values.items())},
        }
        for (d, r), values in sorted(mass_ratios.items())
    ]
    falls = {f"mass_{m}": fall_trajectory(m, 8, FALL_TICKS) for m in (1, 2)}
    result = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "size": SIZE,
        "emission_per_tick": STRENGTH,
        "denominator": DENOMINATOR,
        "measured_ticks": measured,
        "held": rows,
        "held_totals": totals,
        "log_log_slopes_of_acceleration_mass_1": fits,
        "equivalence": equivalence,
        "falls": falls,
    }
    (args.output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"slopes": fits, "totals": totals}))
    for name, trajectory in falls.items():
        arrival = next((t["tick"] for t in trajectory if t.get("x_offset") == 0), None)
        print(name, "arrival_tick", arrival, "final", trajectory[-1])
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
