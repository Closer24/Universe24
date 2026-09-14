"""Host-side test of whether an inverse-square law follows from outward field transport.

Every measurement here is a read-only world/event audit of node state after
the run, compared against host Euclidean distance from the source. This is not
an operational local observer measurement. No detector is planted; the
optional held receivers only check that the in-world flux coupling agrees with
the host projection. Schema 1 conservative transport and schema 2 localizing
attenuation are compared. No physical law is inferred from names.
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

ROOT = Path(__file__).resolve().parents[2]
SIZE = 41
CENTER = SIZE // 2
TICKS = 18
# 8 * 3**12: exact integer octant/axis splitting for the first twelve links.
STRENGTH = 8 * 3**12


def configure(size: int, ticks: int, strength: int) -> None:
    """Select a smaller world for fast acceptance tests; defaults reproduce the README."""
    global SIZE, CENTER, TICKS, STRENGTH
    SIZE, CENTER, TICKS, STRENGTH = size, size // 2, ticks, strength


PORTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
DIRECTIONS = {"axis": (1, 0, 0), "face_diagonal": (1, 1, 0), "body_diagonal": (1, 1, 1)}


def base_document() -> dict:
    return {
        "schema_version": 1,
        "model_id": "inverse-square-host-probe-v1",
        "shape": [SIZE, SIZE, SIZE],
        "boundary": "periodic",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": TICKS,
        # This probe documents the node-owned allocation phase (axis rays fall
        # geometrically); carried phases are compared in docs/SPATIAL_FIELDS.md.
        "allocation_phase": "node",
        "operation_costs": {
            "receive": 1,
            "read": 1,
            "evaluate": 1,
            "update": 1,
            "couple": 1,
            "route": 1,
            "split": 1,
            "send": 1,
            "commit": 1,
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
                "units": "transported scalar unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "abstract vector stock unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "polarity",
                "components": 1,
                "units": "signed response multiplier",
                "signed": True,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "stationary_source",
                "fields": ["strength"],
                "defaults": {"strength": STRENGTH},
                "transport": {"mode": "hold"},
            },
            {
                "name": "held_receiver",
                "fields": ["momentum", "polarity"],
                "defaults": {"momentum": [0, 0, 0], "polarity": 1},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "radiation",
                "baseline": 0,
                "transport": "outward",
                "axis_weights": [1, 1, 1],
                "octant_weights": [1] * 8,
            },
            {"field": "momentum", "baseline": [0, 0, 0], "transport": "local"},
        ],
        "emissions": [
            {
                "type": "stationary_source",
                "field": "radiation",
                "amount": {"field": "strength"},
                "denominator": 1,
                "source": True,
            }
        ],
        "spatial_couplings": [
            {
                "name": "delivered_scalar_flux_exchange",
                "type": "held_receiver",
                "field": "momentum",
                "mode": "exchange",
                "amount": {
                    "op": "neg",
                    "args": [{"op": "mul", "args": [{"field": "polarity"}, {"flux": "radiation"}]}],
                },
                "denominator": 1,
            }
        ],
        "seeds": [{"position": [CENTER] * 3, "type": "stationary_source"}],
    }


def receiver_positions() -> dict[str, list[tuple[int, int, int]]]:
    return {
        name: [tuple(CENTER + k * d for d in direction) for k in range(1, 7)]
        for name, direction in DIRECTIONS.items()
    }


def conservative_document(with_receivers: bool) -> dict:
    raw = base_document()
    if with_receivers:
        raw["model_id"] = "inverse-square-receiver-probe-v1"
        for positions in receiver_positions().values():
            raw["seeds"].extend({"position": list(p), "type": "held_receiver"} for p in positions)
    return raw


def localizing_document() -> dict:
    raw = base_document()
    raw.update(schema_version=2, model_id="inverse-square-localizing-probe-v1")
    raw["spatial_fields"][1] = {
        "field": "momentum",
        "baseline": [0, 0, 0],
        "transport": "outward",
        "decay": {"retain_numerator": 2, "retain_denominator": 3},
    }
    raw["spatial_fields"][0]["decay"] = {"retain_numerator": 2, "retain_denominator": 3}
    raw["emissions"][0]["budget"] = STRENGTH * TICKS
    raw["spatial_couplings"] = []
    return raw


def run(raw: dict) -> Simulation:
    world = Simulation(parse_initial_state(raw))
    for _ in range(raw["ticks"]):
        world.step()
    return world


RAY_HEADINGS = 4096
RAY_SCALE = 24
RAYS_PER_TICK = 64


def golden_headings(count: int, scale: int) -> list[list[int]]:
    """Integer headings spread evenly over the observer's sphere by a golden spiral."""
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


def ray_document() -> dict:
    """Straight rays through an open boundary; one full sweep of the heading sequence."""
    raw = base_document()
    raw.update(model_id="isotropic-ray-host-probe-v1", boundary="open")
    raw["spatial_fields"][0] = {
        "field": "radiation",
        "baseline": 0,
        "transport": "ray",
        "headings": golden_headings(RAY_HEADINGS, RAY_SCALE),
        "rays_per_tick": RAYS_PER_TICK,
        "ray_slots": 512,
    }
    raw["spatial_couplings"] = []
    raw["ticks"] = 2 * (RAY_HEADINGS // RAYS_PER_TICK)
    return raw


def solid_angle(o) -> float:
    """Projected area of one lattice node on the Manhattan shell face, seen from the source."""
    r2 = sum(v * v for v in o)
    manhattan_radius = manhattan(o)
    cos_theta = manhattan_radius / (math.sqrt(3) * math.sqrt(r2))
    return cos_theta * math.sqrt(3) / r2


def isotropy_table(arrived: dict, ticks: int, radii: tuple[int, ...]) -> list[dict]:
    """Observer's test: share of flux per node against the solid angle the node subtends."""
    rows = []
    for radius in radii:
        nodes = []
        for a in range(-radius, radius + 1):
            for b in range(-radius + abs(a), radius - abs(a) + 1):
                for c in {radius - abs(a) - abs(b), -(radius - abs(a) - abs(b))}:
                    o = (a, b, c)
                    r = euclid(o)
                    theta, phi = math.acos(c / r), math.atan2(b, a) % (2 * math.pi)
                    nodes.append((arrived.get(o, 0) / ticks, solid_angle(o), theta, phi))
        flux_total = sum(n[0] for n in nodes)
        omega_total = sum(n[1] for n in nodes)
        rho = [(f / flux_total) / (om / omega_total) for f, om, _, _ in nodes]
        patches: dict[tuple[int, int], list[float]] = {}
        for f, om, theta, phi in nodes:
            key = (min(int(theta / math.pi * 6), 5), min(int(phi / (2 * math.pi) * 12), 11))
            patches.setdefault(key, [0.0, 0.0])
            patches[key][0] += f
            patches[key][1] += om
        patch_rho = [(f / flux_total) / (om / omega_total) for f, om in patches.values()]

        def cv(values: list[float]) -> float:
            mean = sum(values) / len(values)
            return math.sqrt(sum((v - mean) ** 2 for v in values) / len(values)) / mean

        rows.append(
            {
                "manhattan_radius": radius,
                "shell_nodes": len(nodes),
                "mean_flux_times_r2_over_emission": sum(
                    f * (r2)
                    for (f, _, _, _), r2 in zip(
                        nodes,
                        [
                            euclid((a, b, c)) ** 2
                            for a in range(-radius, radius + 1)
                            for b in range(-radius + abs(a), radius - abs(a) + 1)
                            for c in {radius - abs(a) - abs(b), -(radius - abs(a) - abs(b))}
                        ],
                        strict=True,
                    )
                )
                / len(nodes)
                / STRENGTH,
                "cv_rho_nodes": round(cv(rho), 4),
                "cv_rho_72_patches": round(cv(patch_rho), 4),
                "min_patch_rho": round(min(patch_rho), 3),
                "max_patch_rho": round(max(patch_rho), 3),
                "empty_nodes": sum(1 for n in nodes if n[0] == 0),
            }
        )
    return rows


def run_rays(raw: dict) -> tuple[Simulation, dict, int]:
    """Step the ray world; after one sweep, accumulate host-read node values per tick."""
    world = Simulation(parse_initial_state(raw))
    warm = RAY_HEADINGS // RAYS_PER_TICK
    arrived: dict[tuple[int, int, int], int] = {}
    radii = tuple(range(1, TICKS))
    for tick in range(raw["ticks"]):
        world.step()
        if tick < warm:
            continue
        for radius in radii:
            for a in range(-radius, radius + 1):
                for b in range(-radius + abs(a), radius - abs(a) + 1):
                    for c in {radius - abs(a) - abs(b), -(radius - abs(a) - abs(b))}:
                        value = world.spatial_values((CENTER + a, CENTER + b, CENTER + c))["radiation"][
                            "value"
                        ][0]
                        if value:
                            arrived[(a, b, c)] = arrived.get((a, b, c), 0) + value
    return world, arrived, raw["ticks"] - warm


def offset(position) -> tuple[int, int, int]:
    return tuple(v - CENTER for v in position)


def euclid(o) -> float:
    return math.sqrt(sum(v * v for v in o))


def manhattan(o) -> int:
    return sum(abs(v) for v in o)


def sample(world: Simulation, position) -> dict:
    fields = world.spatial_values(tuple(position))["radiation"]
    delivered = fields["directions"]
    flux = tuple(delivered[2 * axis][0] - delivered[2 * axis + 1][0] for axis in range(3))
    return {"value": fields["value"][0], "flux": flux, "localized": fields.get("localized", (0,))[0]}


def shell_table(world: Simulation, max_radius: int) -> list[dict]:
    """Total moving stock on each Manhattan shell, not oriented surface flux."""
    rows = []
    for radius in range(1, max_radius + 1):
        stock, nodes, values = 0, 0, []
        for a in range(-radius, radius + 1):
            for b in range(-radius + abs(a), radius - abs(a) + 1):
                for c in {radius - abs(a) - abs(b), -(radius - abs(a) - abs(b))}:
                    value = sample(world, (CENTER + a, CENTER + b, CENTER + c))["value"]
                    stock += value
                    nodes += 1
                    values.append(value)
        rows.append(
            {
                "manhattan_radius": radius,
                "shell_nodes": nodes,
                "shell_stock": stock,
                "shell_stock_over_emission": stock / STRENGTH,
                "mean_node_value": stock / nodes,
                "mean_times_4R2_plus_2_over_emission": stock
                / nodes
                * (4 * radius * radius + 2)
                / STRENGTH,
                "max_node_value": max(values),
                "min_node_value": min(values),
            }
        )
    return rows


def direction_table(world: Simulation, max_steps: int) -> list[dict]:
    """The observer's Euclidean distance against host-read node values along three rays."""
    rows = []
    for name, direction in DIRECTIONS.items():
        for k in range(1, max_steps + 1):
            o = tuple(k * d for d in direction)
            reading = sample(world, tuple(CENTER + v for v in o))
            r = euclid(o)
            rows.append(
                {
                    "direction": name,
                    "steps": k,
                    "manhattan_radius": manhattan(o),
                    "euclidean_r": round(r, 4),
                    "value": reading["value"],
                    "value_times_r2_over_emission": reading["value"] * r * r / STRENGTH,
                    "flux_vector": reading["flux"],
                    "radial_flux": sum(f * d for f, d in zip(reading["flux"], direction, strict=True))
                    / euclid(direction),
                    "localized": reading["localized"],
                }
            )
    return rows


def fit_exponent(points: list[tuple[float, float]]) -> float | None:
    """Least-squares slope over positive samples; report their support separately."""
    usable = [(math.log(r), math.log(v)) for r, v in points if v > 0 and r > 0]
    if len(usable) < 2:
        return None
    n = len(usable)
    mx = sum(x for x, _ in usable) / n
    my = sum(y for _, y in usable) / n
    sxx = sum((x - mx) ** 2 for x, _ in usable)
    sxy = sum((x - mx) * (y - my) for x, y in usable)
    return sxy / sxx if sxx else None


def receiver_table(world: Simulation) -> list[dict]:
    rows = []
    for name, positions in receiver_positions().items():
        direction = DIRECTIONS[name]
        for position in positions:
            node = world.nodes[position]
            record = next(r for r in node.records if r is not None and r.type_index == 1)
            momentum = world.record_values(record)["momentum"]
            host = sample(world, position)
            rows.append(
                {
                    "direction": name,
                    "steps": manhattan(offset(position)) // manhattan(direction),
                    "euclidean_r": round(euclid(offset(position)), 4),
                    "momentum": momentum,
                    "host_flux_now": host["flux"],
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    result: dict[str, object] = {
        "size": SIZE,
        "ticks": TICKS,
        "emission_per_tick": STRENGTH,
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
    }

    world = run(conservative_document(with_receivers=False))
    shells = shell_table(world, TICKS - 1)
    rays = direction_table(world, TICKS - 1)
    fits = {
        name: fit_exponent(
            [
                (row["euclidean_r"], row["value"])
                for row in rays
                if row["direction"] == name and 1 <= row["steps"] <= 12
            ]
        )
        for name in DIRECTIONS
    }
    fits["shell_mean_vs_R"] = fit_exponent(
        [
            (row["manhattan_radius"], row["mean_node_value"])
            for row in shells
            if row["manhattan_radius"] <= 12
        ]
    )
    result["conservative"] = {
        "totals": world.totals(),
        "sources": world.source_totals(),
        "shells": shells,
        "rays": rays,
        "log_log_slopes_steps_1_to_12": fits,
        "fit_support": {
            name: {
                "positive_sample_steps": [
                    row["steps"]
                    for row in rays
                    if row["direction"] == name and 1 <= row["steps"] <= 12 and row["value"] > 0
                ],
                "selection": "positive samples only; unreached zero values are excluded",
            }
            for name in DIRECTIONS
        },
    }

    world = run(conservative_document(with_receivers=True))
    result["receivers"] = receiver_table(world)

    world = run(localizing_document())
    rays = direction_table(world, TICKS - 1)
    result["localizing"] = {
        "totals": world.totals(),
        "sources": world.source_totals(),
        "dissipation": world.dissipation_totals(),
        "localized": world.localized_totals(),
        "rays": rays,
        "moving_value_ratio_per_diagonal_step_body_diagonal": [
            round(b["value"] / a["value"], 4) if a["value"] else None
            for a, b in zip(rays, rays[1:], strict=False)
            if a["direction"] == b["direction"] == "body_diagonal"
        ],
    }
    world, arrived, measured = run_rays(ray_document())
    ray_rays = []
    for name, direction in DIRECTIONS.items():
        for k in range(1, TICKS):
            o = tuple(k * d for d in direction)
            r = euclid(o)
            value = arrived.get(o, 0) / measured
            ray_rays.append(
                {
                    "direction": name,
                    "steps": k,
                    "manhattan_radius": manhattan(o),
                    "euclidean_r": round(r, 4),
                    "mean_value": round(value, 2),
                    "value_times_r2_over_emission": round(value * r * r / STRENGTH, 5),
                }
            )
    ray_fits = {
        name: fit_exponent(
            [
                (row["euclidean_r"], row["mean_value"])
                for row in ray_rays
                if row["direction"] == name and row["manhattan_radius"] <= 16
            ]
        )
        for name in DIRECTIONS
    }
    result["rays"] = {
        "headings": RAY_HEADINGS,
        "heading_scale": RAY_SCALE,
        "rays_per_tick": RAYS_PER_TICK,
        "measured_ticks": measured,
        "totals": world.totals(),
        "sources": world.source_totals(),
        "escaped": world.escaped_totals(),
        "rays": ray_rays,
        "log_log_slopes_R_1_to_16": ray_fits,
        "fit_support": {
            name: {
                "positive_sample_steps": [
                    row["steps"]
                    for row in ray_rays
                    if row["direction"] == name
                    and row["manhattan_radius"] <= 16
                    and row["mean_value"] > 0
                ],
                "selection": "positive samples only; unreached zero values are excluded",
            }
            for name in DIRECTIONS
        },
        "isotropy": isotropy_table(arrived, measured, (4, 8, 12, 16)),
    }
    print(json.dumps({"ray_slopes": ray_fits, "isotropy": result["rays"]["isotropy"]}))
    (args.output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"slopes": fits, "localized_totals": result["localizing"]["localized"]}))
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
