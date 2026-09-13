"""Particle interaction probes composed from existing rules only.

1. Two like-charged bodies approach head-on through a signed straight-ray field
   they both emit; two opposite charges and two neutral bodies are the controls.
2. A light charged body beside a heavy one: attraction or repulsion by the sign
   of the charge product, and the recoil ratio set by the masses.
3. A bound pair converts, after a local timer, into a free "proton" leaving at
   speed and a heavier residual recoiling the other way: momentum and mass are
   conserved by the declared invariants.

Every number is a read-only world/event audit. Labels such as proton, electron
and charge are configuration data; the engine dispatches no law by name, and
no physical constant or unit is identified.
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

SIZE = 21
CENTER = SIZE // 2
HEADINGS = 512
HEADING_SCALE = 16
RAYS_PER_TICK = 512  # every heading fires every tick: no sweep, a dense field
EMISSION_PER_CHARGE = 512  # ray units per tick per unit of charge: 3 units per ray for charge 3
SPEED_SCALE = 16  # hops per tick = |p| / (SPEED_SCALE * mass), capped at one

COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}


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


def charged_transport() -> dict:
    """Move along the momentum at min(1, |p| / (SPEED_SCALE * mass)) hops per tick."""
    return {
        "mode": "move",
        "direction_field": "momentum",
        "rate": {
            "op": "min",
            "args": [
                {"op": "mul", "args": [{"field": "mass"}, SPEED_SCALE]},
                {"op": "sum", "args": [{"op": "abs", "args": [{"field": "momentum"}]}]},
            ],
        },
        "rate_denominator": SPEED_SCALE,
        "rate_divisor": {"field": "mass"},
    }


def charged_document(bodies: list[dict], ticks: int, shared_field: bool = True) -> dict:
    """Bodies: {"name", "mass", "charge", "momentum", "position"}; each is one type.

    With ``shared_field`` every charged body emits into one signed ray field with
    ``self_exclusion``: a departing record subtracts its own one-link-old rays from
    the flux it samples at the next Node, using only its own bookkeeping. Without
    it each body gets a field of its own and reads only the others' fields.
    """
    raw = {
        "schema_version": 1,
        "model_id": "signed-ray-charge-interaction-probe-v1",
        "shape": [SIZE, SIZE, SIZE],
        "boundary": "open",
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": [
            {
                "name": "mass",
                "components": 1,
                "units": "mass unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "charge",
                "components": 1,
                "units": "charge unit",
                "signed": True,
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
        "disturbance_types": [],
        "spatial_fields": [
            {"field": "momentum", "baseline": [0, 0, 0], "transport": "local"},
        ],
        "emissions": [],
        "spatial_couplings": [],
        "seeds": [],
    }
    charged = [body for body in bodies if body["charge"]]

    def ray_field(name: str, exclude: bool) -> None:
        raw["fields"].append(
            {
                "name": name,
                "components": 1,
                "units": "signed ray unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
            }
        )
        raw["spatial_fields"].append(
            {
                "field": name,
                "baseline": 0,
                "transport": "ray",
                "headings": golden_headings(HEADINGS, HEADING_SCALE),
                "rays_per_tick": RAYS_PER_TICK,
                "ray_slots": 2048,
                "self_exclusion": exclude,
            }
        )

    if shared_field and charged:
        ray_field("charge_field", True)
    elif not shared_field:
        for body in charged:
            ray_field(f"field_of_{body['name']}", False)
    for body in bodies:
        raw["disturbance_types"].append(
            {
                "name": body["name"],
                "fields": ["mass", "charge", "momentum"],
                "defaults": {
                    "mass": body["mass"],
                    "charge": body["charge"],
                    "momentum": body["momentum"],
                },
                "transport": charged_transport(),
            }
        )
        if body["charge"]:
            own = "charge_field" if shared_field else f"field_of_{body['name']}"
            raw["emissions"].append(
                {
                    "type": body["name"],
                    "field": own,
                    "amount": {"op": "mul", "args": [{"field": "charge"}, EMISSION_PER_CHARGE]},
                    "denominator": 1,
                    "source": True,
                }
            )
            read = (
                ["charge_field"]
                if shared_field
                else [f"field_of_{other['name']}" for other in charged if other["name"] != body["name"]]
            )
            for field_name in read:
                # Momentum change is +charge x flux: like charges push apart, unlike attract.
                raw["spatial_couplings"].append(
                    {
                        "name": f"{body['name']}_in_{field_name}",
                        "type": body["name"],
                        "field": "momentum",
                        "mode": "exchange",
                        "amount": {
                            "op": "neg",
                            "args": [{"op": "mul", "args": [{"field": "charge"}, {"flux": field_name}]}],
                        },
                        "denominator": 1,
                    }
                )
        raw["seeds"].append({"position": [CENTER + v for v in body["position"]], "type": body["name"]})
    return raw


def track(raw: dict) -> tuple[Simulation, dict[str, list[dict]]]:
    world = Simulation(parse_initial_state(raw))
    names = [kind["name"] for kind in raw["disturbance_types"]]
    history: dict[str, list[dict]] = {name: [] for name in names}
    for tick in range(1, raw["ticks"] + 1):
        world.step()
        seen = set()
        for position, node in world.nodes.items():
            for record in node.records:
                if record is None:
                    continue
                name = names[record.type_index]
                seen.add(name)
                values = world.record_values(record)
                history[name].append(
                    {
                        "tick": tick,
                        "offset": [v - CENTER for v in position],
                        "momentum": list(values["momentum"]),
                    }
                )
        for packets in world.links.values():
            for packet in packets:
                if packet is not None and getattr(packet, "record", None) is not None:
                    name = names[packet.record.type_index]
                    seen.add(name)
                    history[name].append(
                        {
                            "tick": tick,
                            "offset": None,
                            "momentum": list(world.record_values(packet.record)["momentum"]),
                        }
                    )
        for name in names:
            if name not in seen:
                history[name].append({"tick": tick, "offset": None, "momentum": None, "gone": True})
    return world, history


def separation(history: dict[str, list[dict]], a: str, b: str) -> list[tuple[int, float | None]]:
    by_tick = {}
    for name in (a, b):
        for entry in history[name]:
            if entry.get("offset") is not None:
                by_tick.setdefault(entry["tick"], {})[name] = entry["offset"]
    result = []
    for tick in sorted(by_tick):
        pair = by_tick[tick]
        if a in pair and b in pair:
            result.append((tick, math.dist(pair[a], pair[b])))
        else:
            result.append((tick, None))
    return result


def head_on(charge_a: int, charge_b: int, ticks: int = 40) -> dict:
    bodies = [
        {
            "name": "left",
            "mass": 16,
            "charge": charge_a,
            "momentum": [128, 0, 0],
            "position": [-7, 0, 0],
        },
        {
            "name": "right",
            "mass": 16,
            "charge": charge_b,
            "momentum": [-128, 0, 0],
            "position": [7, 0, 0],
        },
    ]
    world, history = track(charged_document(bodies, ticks))
    seps = separation(history, "left", "right")
    finite = [(t, d) for t, d in seps if d is not None]
    closest = min(finite, key=lambda item: item[1]) if finite else None
    final = {name: history[name][-1] for name in ("left", "right")}
    return {
        "charges": [charge_a, charge_b],
        "closest_approach": None
        if closest is None
        else {"tick": closest[0], "distance": round(closest[1], 3)},
        "final": final,
        "momentum_total": list(world.totals()["momentum"]),
        "trajectory_left_x": [(e["tick"], e["offset"][0]) for e in history["left"] if e.get("offset")][
            ::4
        ],
        "trajectory_right_x": [(e["tick"], e["offset"][0]) for e in history["right"] if e.get("offset")][
            ::4
        ],
    }


def light_beside_heavy(light_charge: int, ticks: int = 32) -> dict:
    bodies = [
        {"name": "heavy", "mass": 64, "charge": 3, "momentum": [0, 0, 0], "position": [0, 0, 0]},
        {
            "name": "light",
            "mass": 1,
            "charge": light_charge,
            "momentum": [0, 0, 0],
            "position": [5, 0, 0],
        },
    ]
    world, history = track(charged_document(bodies, ticks))
    light = [e for e in history["light"] if e.get("offset")]
    heavy = [e for e in history["heavy"] if e.get("offset")]
    return {
        "light_charge": light_charge,
        "light_x": [(e["tick"], e["offset"][0], e["momentum"][0]) for e in light][::3],
        "heavy_x": [(e["tick"], e["offset"][0], e["momentum"][0]) for e in heavy][::6],
        "light_final": light[-1] if light else history["light"][-1],
        "heavy_final": heavy[-1] if heavy else history["heavy"][-1],
        "momentum_total": list(world.totals()["momentum"]),
    }


def emission_document(ticks: int, delay: int, proton_momentum: int, residual_mass: int) -> dict:
    fields = ["mass", "momentum", "excitation"]

    def kind(name, mass, momentum, transport):
        return {
            "name": name,
            "fields": fields,
            "defaults": {"mass": mass, "momentum": momentum, "excitation": 0},
            "transport": transport,
        }

    move = {
        "mode": "move",
        "direction_field": "momentum",
        "rate": {
            "op": "min",
            "args": [
                {"op": "mul", "args": [{"field": "mass"}, SPEED_SCALE]},
                {"op": "sum", "args": [{"op": "abs", "args": [{"field": "momentum"}]}]},
            ],
        },
        "rate_denominator": SPEED_SCALE,
        "rate_divisor": {"field": "mass"},
    }
    bound_proton = kind("bound_proton", 1, [0, 0, 0], {"mode": "hold"})
    bound_proton["updates"] = [
        {"field": "excitation", "expression": {"op": "add", "args": [{"field": "excitation"}, 1]}}
    ]
    return {
        "schema_version": 1,
        "model_id": "timed-two-body-proton-emission-probe-v1",
        "shape": [SIZE, SIZE, SIZE],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": [
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
            {
                "name": "excitation",
                "components": 1,
                "units": "tick count",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            bound_proton,
            kind("residual_core", residual_mass, [0, 0, 0], {"mode": "hold"}),
            kind("free_proton", 1, [0, 0, 0], move),
            kind("recoiling_core", residual_mass, [0, 0, 0], move),
        ],
        "interactions": [
            {
                "name": "proton_emission",
                "left_type": "bound_proton",
                "right_type": "residual_core",
                "output_types": {"left": "free_proton", "right": "recoiling_core"},
                "when": {"op": "gt", "args": [{"field": "excitation", "side": "left"}, delay]},
                "assignments": [
                    {"side": "left", "field": "mass", "expression": {"field": "mass", "side": "left"}},
                    {
                        "side": "left",
                        "field": "momentum",
                        "expression": {"op": "vector", "args": [proton_momentum, 0, 0]},
                    },
                    {"side": "left", "field": "excitation", "expression": 0},
                    {"side": "right", "field": "mass", "expression": {"field": "mass", "side": "right"}},
                    {
                        "side": "right",
                        "field": "momentum",
                        "expression": {"op": "vector", "args": [-proton_momentum, 0, 0]},
                    },
                    {"side": "right", "field": "excitation", "expression": 0},
                ],
                "invariants": [
                    {
                        "name": "total_momentum",
                        "expression": {
                            "op": "add",
                            "args": [
                                {"field": "momentum", "side": "left"},
                                {"field": "momentum", "side": "right"},
                            ],
                        },
                    },
                    {
                        "name": "total_mass",
                        "expression": {
                            "op": "add",
                            "args": [
                                {"field": "mass", "side": "left"},
                                {"field": "mass", "side": "right"},
                            ],
                        },
                    },
                ],
            }
        ],
        "seeds": [
            {"position": [CENTER] * 3, "type": "bound_proton"},
            {"position": [CENTER] * 3, "type": "residual_core"},
        ],
    }


def proton_emission(
    ticks: int = 40, delay: int = 8, proton_momentum: int = 24, residual_mass: int = 3
) -> dict:
    raw = emission_document(ticks, delay, proton_momentum, residual_mass)
    world, history = track(raw)

    def path(name):
        return [(e["tick"], e["offset"][0], e["momentum"][0]) for e in history[name] if e.get("offset")]

    emitted_tick = next((e["tick"] for e in history["free_proton"] if e.get("offset")), None)
    return {
        "delay": delay,
        "proton_momentum": proton_momentum,
        "residual_mass": residual_mass,
        "emission_tick": emitted_tick,
        "free_proton_x": path("free_proton")[::2],
        "recoiling_core_x": path("recoiling_core")[::4],
        "totals": {name: list(values) for name, values in world.totals().items()},
        "initial_totals": {"mass": [1 + residual_mass], "momentum": [0, 0, 0]},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    result: dict[str, object] = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "head_on": {
            "like_charges": head_on(3, 3),
            "opposite_charges": head_on(3, -3),
            "neutral": head_on(0, 0),
        },
        "light_beside_heavy": {
            "opposite": light_beside_heavy(-3),
            "like": light_beside_heavy(3),
        },
        "proton_emission": proton_emission(),
        "radiation_pressure": radiation_pressure(),
    }
    (args.output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    for name, run in result["head_on"].items():  # type: ignore[union-attr]
        print(
            name,
            "closest",
            run["closest_approach"],
            "final momenta",
            run["final"]["left"]["momentum"],
            run["final"]["right"]["momentum"],
        )
    for name, run in result["light_beside_heavy"].items():  # type: ignore[union-attr]
        print(
            name,
            "light",
            run["light_final"].get("offset"),
            run["light_final"].get("momentum"),
            "heavy",
            run["heavy_final"].get("offset"),
            run["heavy_final"].get("momentum"),
        )
    pressure = result["radiation_pressure"]
    print(
        "radiation pressure audit",
        pressure["audit"]["status"],
        "sail",
        pressure["sail_final"],  # type: ignore[index]
        "lamp",
        pressure["lamp_final"],
    )  # type: ignore[index]
    emission = result["proton_emission"]
    print("emission tick", emission["emission_tick"], "totals", emission["totals"])  # type: ignore[index]
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()


def radiation_pressure_document(ticks: int, headings: list[list[int]], rays_per_tick: int) -> dict:
    """Energy-closed push: a funded emitter, an absorbing body, and the conservation audit.

    Rays are quanta: energy is their amount and momentum is amount x heading. The
    emitter pays every quantum from its own stock and recoils; the absorber banks
    each quantum it swallows and takes its momentum. Nothing else changes energy.
    """
    move = {
        "mode": "move",
        "direction_field": "momentum",
        "rate": {
            "op": "min",
            "args": [
                {"op": "mul", "args": [{"field": "mass"}, SPEED_SCALE]},
                {"op": "sum", "args": [{"op": "abs", "args": [{"field": "momentum"}]}]},
            ],
        },
        "rate_denominator": SPEED_SCALE,
        "rate_divisor": {"field": "mass"},
    }
    return {
        "schema_version": 1,
        "model_id": "funded-ray-radiation-pressure-probe-v1",
        "shape": [SIZE, SIZE, SIZE],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": [
            {
                "name": "mass",
                "components": 1,
                "units": "mass unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
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
        ],
        "disturbance_types": [
            {
                "name": "lamp",
                "fields": ["mass", "quanta", "momentum"],
                "defaults": {"mass": 4096, "quanta": 200000, "momentum": [0, 0, 0]},
                "transport": move,
            },
            {
                "name": "sail",
                "fields": ["mass", "quanta", "momentum"],
                "defaults": {"mass": 64, "quanta": 0, "momentum": [0, 0, 0]},
                "transport": move,
            },
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": headings,
                "rays_per_tick": rays_per_tick,
                "ray_slots": 4096,
                "self_exclusion": True,
            },
        ],
        "emissions": [
            {
                "type": "lamp",
                "field": "quanta",
                "amount": 2048,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            }
        ],
        "spatial_couplings": [
            {
                "name": "sail_absorbs",
                "type": "sail",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
        ],
        "seeds": [
            {"position": [CENTER] * 3, "type": "lamp"},
            {"position": [CENTER + 4, CENTER, CENTER], "type": "sail"},
        ],
        "conservation": {
            "name": "ray quanta",
            "energy_units": "quantum",
            "momentum_units": "quantum times heading",
            "carriers": [
                {
                    "requires": ["quanta", "momentum"],
                    "energy": {"field": "quanta"},
                    "momentum": {"field": "momentum"},
                }
            ],
            "spatial": {
                "energy": {"field": "quanta", "side": "right"},
                "momentum": {"op": "vector", "args": [0, 0, 0]},
            },
        },
    }


def radiation_pressure(ticks: int = 40) -> dict:
    raw = radiation_pressure_document(ticks, golden_headings(HEADINGS, HEADING_SCALE), RAYS_PER_TICK)
    world, history = track(raw)

    def path(name):
        return [(e["tick"], e["offset"][0], e["momentum"][0]) for e in history[name] if e.get("offset")]

    report = world.conservation_report()
    sail = [e for e in history["sail"] if e.get("offset")]
    lamp = [e for e in history["lamp"] if e.get("offset")]
    return {
        "audit": {
            k: report[k] for k in ("status", "checked_node_events", "initial", "current", "escaped")
        },
        "sail_x": path("sail")[::4],
        "lamp_x": path("lamp")[::8],
        "sail_final": sail[-1] if sail else history["sail"][-1],
        "lamp_final": lamp[-1] if lamp else history["lamp"][-1],
        "totals": {name: list(values) for name, values in world.totals().items()},
    }
