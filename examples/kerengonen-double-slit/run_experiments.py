"""Kerengonen double slit: two lamps in phase, a line of absorbers, a fringe in path difference.

Configuration only on the `kerengonen-ray-field-v1` candidate. Two funded lamps
fire the same planar heading set every tick; each ray carries a phase that
advances one step per link. A line of absorbers eight links downstream takes
the rays that reach it, gated by the coherence of what meets at each Node.
The same world without the key is the plain ray field: amounts add and the
line is lit evenly. Every number is a read-only world/event audit at host
lattice coordinates; no physical constant, wavelength or species is identified.
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

SIZE = 31
CENTER = SIZE // 2
LAMP_X = CENTER - 8
SCREEN_X = CENTER + 8
SLIT_HALF = 3  # lamps at y = CENTER +- 3
SCREEN_HALF = 12
HEADINGS = 128
HEADING_SCALE = 16
PER_RAY = 16
PHASE_STEPS = 8
TICKS = 48
SINGLE_QUANTA_TICKS = 96  # one quantum per ray: twice the ticks for the counts
SOURCE_X = CENTER - 12  # the single lamp of the wall experiment
WALL_X = CENTER - 4  # an absorbing wall with two re-emitting slits at y = +-3
SOURCE_PER_RAY = 64
SOURCE_TICKS = 64
WALL_HEADINGS = 256  # a forward cone within 45 degrees of +x at scale 64: 117 distinct
WALL_HEADING_SCALE = 64
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}


def planar_headings(count: int, scale: int) -> list[list[int]]:
    """Distinct integer headings on the half circle facing +x, in the lamp plane."""
    result: list[list[int]] = []
    for i in range(count):
        angle = -math.pi / 2 + math.pi * (i + 0.5) / count
        heading = [round(scale * math.cos(angle)), round(scale * math.sin(angle)), 0]
        if heading[0] > 0 and heading not in result:
            result.append(heading)
    return result


def cone_headings(count: int, scale: int) -> list[list[int]]:
    """Distinct integer headings within 45 degrees of +x: nothing crawls along a wall."""
    result: list[list[int]] = []
    for i in range(count):
        angle = -math.pi / 4 + math.pi / 2 * (i + 0.5) / count
        heading = [round(scale * math.cos(angle)), round(scale * math.sin(angle)), 0]
        if heading[0] > 0 and heading not in result:
            result.append(heading)
    return result


def document(
    ticks: int,
    headings: list[list[int]],
    per_ray: int = PER_RAY,
    phase_steps: int = PHASE_STEPS,
    phase_b: int = 0,
    audit: bool = False,
    screen_half: int = SCREEN_HALF,
    layers: int = 1,
) -> dict:
    count = len(headings)
    stock = per_ray * count * ticks
    field = {
        "field": "quanta",
        "baseline": 0,
        "transport": "ray",
        "headings": headings,
        "rays_per_tick": count,
        "ray_slots": 2048,
    }
    if phase_steps:
        field["kerengonen"] = {"phase_steps": phase_steps, "phase_advance": 1}
    emission_b: dict = {
        "type": "lamp_b",
        "field": "quanta",
        "amount": per_ray * count,
        "denominator": 1,
        "source": False,
        "recoil_field": "momentum",
    }
    if phase_b:
        emission_b["kerengonen_phase"] = phase_b
    raw: dict = {
        "schema_version": 1,
        "model_id": "kerengonen-double-slit-probe-v1",
        "sampling_profile": "detector-only-v1",
        "shape": [SIZE, SIZE, 3],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": [
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
                "name": name,
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": stock, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for name in ("lamp_a", "lamp_b")
        ]
        + [
            {
                "name": "screen",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [field],
        "emissions": [
            {
                "type": "lamp_a",
                "field": "quanta",
                "amount": per_ray * count,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            },
            emission_b,
        ],
        "spatial_couplings": [
            {
                "name": "screen_absorbs",
                "type": "screen",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
        ],
        "seeds": [
            {"position": [LAMP_X, CENTER - SLIT_HALF, 1], "type": "lamp_a"},
            {"position": [LAMP_X, CENTER + SLIT_HALF, 1], "type": "lamp_b"},
        ]
        + [
            {"position": [SCREEN_X + layer, CENTER + y, 1], "type": "screen"}
            for layer in range(layers)
            for y in range(-screen_half, screen_half + 1)
        ],
    }
    if audit:
        raw["conservation"] = {
            "name": "quanta",
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
        }
    return raw


def wall_document(
    ticks: int,
    headings: list[list[int]],
    slits: tuple[int, ...] = (-SLIT_HALF, SLIT_HALF),
    phase_steps: int = PHASE_STEPS,
) -> dict:
    """One lamp, an absorbing wall whose slits re-emit what they absorb, and the screen.

    A slit is a Huygens source: it absorbs the rays that reach it and next cycle
    re-emits its whole stock over the field's headings at the phase it absorbed,
    one advance on. The wall keeps what it absorbs. The plain field has no phase,
    so its slits re-emit without one.
    """
    raw = document(ticks, headings, per_ray=SOURCE_PER_RAY, phase_steps=phase_steps)
    raw["model_id"] = "kerengonen-single-source-wall-probe-v1"
    raw["disturbance_types"] = [
        {
            "name": "lamp",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": SOURCE_PER_RAY * len(headings) * ticks, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        },
        {
            "name": "wall",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        },
        {
            "name": "slit",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        },
        {
            "name": "screen",
            "fields": ["quanta", "momentum"],
            "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        },
    ]
    slit_emission: dict = {
        "type": "slit",
        "field": "quanta",
        "amount": {"field": "quanta"},
        "denominator": 1,
        "source": False,
        "recoil_field": "momentum",
    }
    if phase_steps:
        slit_emission["kerengonen_phase"] = "carried"
    raw["emissions"] = [
        {
            "type": "lamp",
            "field": "quanta",
            "amount": SOURCE_PER_RAY * len(headings),
            "denominator": 1,
            "source": False,
            "recoil_field": "momentum",
        },
        slit_emission,
    ]
    raw["spatial_couplings"] = [
        {
            "name": f"{name}_absorbs",
            "type": name,
            "field": "quanta",
            "mode": "absorb",
            "momentum_field": "momentum",
        }
        for name in ("wall", "slit", "screen")
    ]
    raw["seeds"] = (
        [{"position": [SOURCE_X, CENTER, 1], "type": "lamp"}]
        + [
            {"position": [WALL_X, CENTER + y, 1], "type": "slit" if y in slits else "wall"}
            for y in range(-(SIZE // 2), SIZE // 2 + 1)
        ]
        + [
            {"position": [SCREEN_X, CENTER + y, 1], "type": "screen"}
            for y in range(-SCREEN_HALF, SCREEN_HALF + 1)
        ]
    )
    return raw


def run_wall(raw: dict) -> dict:
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    for _ in range(raw["ticks"]):
        world.step()
    totals, escaped = world.totals(), world.escaped_totals()
    profile = {}
    kept = {"wall": 0, "slit": 0}
    names = [kind["name"] for kind in raw["disturbance_types"]]
    for position, node in world.nodes.items():
        for record in node.records:
            if record is None:
                continue
            name = names[record.type_index]
            quanta = world.record_values(record)["quanta"][0]
            if name == "screen":
                profile[position[1] - CENTER] = quanta
            elif name in kept:
                kept[name] += quanta
    return {
        "profile": dict(sorted(profile.items())),
        "absorbed_total": sum(profile.values()),
        "wall_kept": kept["wall"],
        "slit_stock": kept["slit"],
        "quanta_closed": totals["quanta"][0] + escaped["quanta"][0] == initial,
        "escaped": escaped["quanta"][0],
    }


def screen_profile(world: Simulation, layer: int = 0) -> dict[int, int]:
    """The absorbed quanta per screen Node of one layer (0 is the first the wave meets)."""
    profile = {}
    for position, node in world.nodes.items():
        for record in node.records:
            if record is not None and record.type_index == 2 and position[0] == SCREEN_X + layer:
                profile[position[1] - CENTER] = world.record_values(record)["quanta"][0]
    return dict(sorted(profile.items()))


def layer_totals(world: Simulation, layers: int) -> list[int]:
    return [sum(screen_profile(world, layer).values()) for layer in range(layers)]


def run(raw: dict) -> dict:
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    for _ in range(raw["ticks"]):
        world.step()
    totals, escaped = world.totals(), world.escaped_totals()
    profile = screen_profile(world)
    layers = len(
        {
            p[0]
            for p, node in world.nodes.items()
            if any(r is not None and r.type_index == 2 for r in node.records)
        }
    )
    lamps = [
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index in (0, 1)
    ]
    return {
        "profile": profile,
        "absorbed_total": sum(layer_totals(world, layers)),
        "layer_totals": layer_totals(world, layers),
        "lamp_stock": [lamp["quanta"][0] for lamp in lamps],
        "lamp_momentum": [list(lamp["momentum"]) for lamp in lamps],
        "quanta_closed": totals["quanta"][0] + escaped["quanta"][0] == initial,
        "escaped": escaped["quanta"][0],
        **({"audit": world.conservation_report()} if "conservation" in raw else {}),
    }


def path_difference(y: int) -> int:
    """Manhattan path difference between the two lamps and a screen Node at offset y."""
    return abs(y + SLIT_HALF) - abs(y - SLIT_HALF)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    headings = planar_headings(HEADINGS, HEADING_SCALE)
    runs = {
        "kerengonen": run(document(TICKS, headings)),
        "kerengonen_lamp_b_half_turn": run(document(TICKS, headings, phase_b=PHASE_STEPS // 2)),
        "plain": run(document(TICKS, headings, phase_steps=0)),
    }
    # A thick screen: the quanta a dark Node lets pass are absorbed in the layers
    # behind it, where the path difference, and so the phase, is different.
    thick = {
        f"layers_{layers}": {
            "phased": run(document(TICKS, headings, layers=layers)),
            "plain": run(document(TICKS, headings, phase_steps=0, layers=layers)),
        }
        for layers in (1, 2, 4, 8)
    }
    # Single quanta under the share rule: a lone quantum's half share truncates to
    # nothing, so only the fully coherent Nodes take it. (The whole-or-nothing
    # lottery capture that once built the fringe click by click was deleted on
    # 2026-09-17: an ordinary absorber does not draw.)
    single_quanta = {"share_single_quanta": run(document(SINGLE_QUANTA_TICKS, headings, per_ray=1))}
    # One source behind a wall: the two slits are Huygens sources of the same wave.
    # A forward cone of headings keeps re-emitted rays off the wall plane.
    cone = cone_headings(WALL_HEADINGS, WALL_HEADING_SCALE)
    wall = {
        "two_slits": run_wall(wall_document(SOURCE_TICKS, cone)),
        "slit_a_only": run_wall(wall_document(SOURCE_TICKS, cone, slits=(-SLIT_HALF,))),
        "slit_b_only": run_wall(wall_document(SOURCE_TICKS, cone, slits=(SLIT_HALF,))),
        "two_slits_plain": run_wall(wall_document(SOURCE_TICKS, cone, phase_steps=0)),
    }
    # Eight headings, 24 ticks, a five-Node screen: the (16, +-3) headings of both
    # lamps meet at y = 0 after 19 links each, in phase, under the event audit.
    audited = run(document(24, planar_headings(8, HEADING_SCALE), audit=True, screen_half=2))
    fringe = [
        {
            "y": y,
            "path_difference": path_difference(y),
            "phase_difference": path_difference(y) % PHASE_STEPS,
            "kerengonen": runs["kerengonen"]["profile"].get(y, 0),
            "half_turn": runs["kerengonen_lamp_b_half_turn"]["profile"].get(y, 0),
            "plain": runs["plain"]["profile"].get(y, 0),
            **{name: world["profile"].get(y, 0) for name, world in single_quanta.items()},
            **{f"wall_{name}": world["profile"].get(y, 0) for name, world in wall.items()},
        }
        for y in range(-SCREEN_HALF, SCREEN_HALF + 1)
    ]
    result = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "headings": len(headings),
        "per_ray": PER_RAY,
        "phase_steps": PHASE_STEPS,
        "ticks": TICKS,
        "fringe": fringe,
        "runs": {name: {k: v for k, v in run_.items() if k != "profile"} for name, run_ in runs.items()},
        "single_quanta": {
            name: {k: v for k, v in world.items() if k != "profile"}
            for name, world in single_quanta.items()
        },
        "single_quanta_ticks": SINGLE_QUANTA_TICKS,
        "wall": {
            name: {k: v for k, v in world.items() if k != "profile"} for name, world in wall.items()
        },
        "wall_ticks": SOURCE_TICKS,
        "wall_headings": len(cone),
        "thick_screen": {
            name: {
                kind: {k: v for k, v in world.items() if k != "profile"}
                | {"first_layer": world["profile"]}
                for kind, world in pair.items()
            }
            for name, pair in thick.items()
        },
        "audited": {k: v for k, v in audited.items() if k != "profile"}
        | {"profile": audited["profile"]},
    }
    (args.output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    for row in fringe:
        print(
            row["y"],
            row["path_difference"],
            row["kerengonen"],
            row["half_turn"],
            row["plain"],
            "single quanta",
            row["share_single_quanta"],
            "wall",
            [row[f"wall_{name}"] for name in wall],
        )
    print("single quanta", result["single_quanta"])
    for name, pair in thick.items():
        print(
            name,
            "phased absorbed",
            pair["phased"]["absorbed_total"],
            pair["phased"]["layer_totals"],
            "plain",
            pair["plain"]["absorbed_total"],
            "escaped",
            pair["phased"]["escaped"],
            pair["plain"]["escaped"],
            "first layer center and half turn",
            pair["phased"]["profile"].get(0),
            pair["phased"]["profile"].get(2),
        )
    print("wall", result["wall"])
    print("runs", result["runs"])
    print("audited", result["audited"]["audit"]["status"], result["audited"]["quanta_closed"])
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
