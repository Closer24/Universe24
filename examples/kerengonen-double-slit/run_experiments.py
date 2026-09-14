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
LOTTERY_TICKS = 96  # single quanta, whole or nothing: twice the ticks for the counts
LOTTERY_SEEDS = (1, 2)
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


def document(
    ticks: int,
    headings: list[list[int]],
    per_ray: int = PER_RAY,
    phase_steps: int = PHASE_STEPS,
    phase_b: int = 0,
    audit: bool = False,
    screen_half: int = SCREEN_HALF,
    capture_seed: int | None = None,
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
        if capture_seed is not None:
            field["kerengonen"].update({"capture": "lottery", "capture_seed": capture_seed})
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
            {"position": [SCREEN_X, CENTER + y, 1], "type": "screen"}
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


def screen_profile(world: Simulation) -> dict[int, int]:
    profile = {}
    for position, node in world.nodes.items():
        for record in node.records:
            if record is not None and record.type_index == 2:
                profile[position[1] - CENTER] = world.record_values(record)["quanta"][0]
    return dict(sorted(profile.items()))


def run(raw: dict) -> dict:
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    for _ in range(raw["ticks"]):
        world.step()
    totals, escaped = world.totals(), world.escaped_totals()
    profile = screen_profile(world)
    lamps = [
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index in (0, 1)
    ]
    return {
        "profile": profile,
        "absorbed_total": sum(profile.values()),
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
    # Single quanta, whole or nothing: the lottery capture builds the fringe click by
    # click. The share rule would truncate a lone quantum's half share to nothing.
    lottery = {
        f"seed_{seed}": run(document(LOTTERY_TICKS, headings, per_ray=1, capture_seed=seed))
        for seed in LOTTERY_SEEDS
    }
    lottery["share_single_quanta"] = run(document(LOTTERY_TICKS, headings, per_ray=1))
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
            **{name: world["profile"].get(y, 0) for name, world in lottery.items()},
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
        "lottery": {
            name: {k: v for k, v in world.items() if k != "profile"} for name, world in lottery.items()
        },
        "lottery_ticks": LOTTERY_TICKS,
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
            "lottery",
            [row[f"seed_{seed}"] for seed in LOTTERY_SEEDS],
            row["share_single_quanta"],
        )
    print("lottery", result["lottery"])
    print("runs", result["runs"])
    print("audited", result["audited"]["audit"]["status"], result["audited"]["quanta_closed"])
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
