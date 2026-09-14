"""Does a localized quantum domain feel the computation field's clock like a carrier does?

A charge is converted into a one-excitation quantum domain at x=1 and hopped
register by register to a detector at x=7 by configured swap gates (one Link per
tick). A mass beside the chain emits the `computation` field, which delays carrier
departures along its direction (`delay_direction`; contact programs reject the
shared clock). A classical carrier runs the same distance on a parallel row. Compare the classical arrival tick and the quantum
capture tick with and without the mass.
"""

import json
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

BASE = json.loads(Path("examples/quantum/localized_charge.json").read_text(encoding="utf-8"))
LENGTH = 7
BUDGET = 40
SWAP = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]


def op(name, *args):
    return {"op": name, "args": list(args)}


def document(emission):
    doc = json.loads(json.dumps(BASE))
    doc["model_id"] = "quantum-chain-under-computation-clock-v1"
    doc["schema_version"] = 1
    doc["shape"] = [LENGTH + 2, 3, 3]
    doc["ticks"] = 40
    doc["normal_budget"] = BUDGET
    # Contact programs require the fixed spatial clock, so the field delays carrier
    # departures directionally (default clock) instead of the whole node cycle.
    doc["delay_direction"] = "along"
    doc["computation_field"] = "computation"
    doc["fields"] = [f for f in doc["fields"] if f["name"] != "electric_signal"] + [
        {
            "name": "computation",
            "components": 1,
            "units": "load unit",
            "signed": False,
            "conserved": True,
            "extensive": True,
        },
        {
            "name": "momentum",
            "components": 3,
            "units": "c/120",
            "signed": True,
            "conserved": False,
            "extensive": False,
            "scale": 120,
        },
    ]
    doc["disturbance_types"] += [
        {
            "name": "mass body",
            "fields": ["mass"],
            "defaults": {"mass": 1},
            "transport": {"mode": "hold"},
        },
        {
            "name": "runner",
            "fields": ["mass", "momentum"],
            "defaults": {"mass": 1, "momentum": [120, 0, 0]},
            "transport": {
                "mode": "move",
                "direction_field": "momentum",
                "rate": 120,
                "rate_denominator": 120,
            },
        },
    ]
    doc["spatial_fields"] = [{"field": "computation", "baseline": 0, "transport": "outward"}]
    doc["emissions"] = [
        {
            "type": "mass body",
            "field": "computation",
            "amount": emission,
            "denominator": 1,
            "source": True,
        }
    ]
    doc["seeds"] = [
        {"position": [1, 1, 1], "type": "incoming_charge"},
        {"position": [1, 1, 1], "type": "contact_probe"},
        {"position": [LENGTH, 1, 1], "type": "contact_probe"},
        {"position": [1, 0, 1], "type": "runner"},
        {"position": [(LENGTH + 1) // 2, 2, 1], "type": "mass body"},
    ]
    program = doc["event_program"]
    program["addresses"] = [[x, 1, 1] for x in range(1, LENGTH + 1)]
    program["tickets"] = [0] * 64
    program["capacity"] = 2_000_000  # the emitting mass appends many spatial events
    domain = program["domains"][0]
    domain["register_indices"] = list(range(LENGTH))
    domain["capture"]["register_indices"] = [LENGTH - 1]
    domain["phases"] = [
        [{"register_indices": [k, k + 1], "matrix": SWAP}] for k in range(LENGTH - 1)
    ] + [[]] * 20
    return doc


def run(emission):
    events = []
    world = Simulation(parse_initial_state(document(emission)), observer=events.append)
    for _ in range(40):
        world.step()
    report = world._resolver.report()
    captures = [t["tick"] for t in report.get("contact_transfers", [])]
    runner_arrival = next(
        (
            e["tick"]
            for e in events
            if e.get("event") == "received"
            and e.get("disturbance") == "runner"
            and tuple(e["position"]) == (LENGTH, 0, 1)
        ),
        None,
    )
    delays = {
        tuple(n["position"]): max(n["delay_counts"])
        for n in world.snapshot()["nodes"]
        if n["delay_counts"] and max(n["delay_counts"])
    }
    localized = [
        (tuple(n["position"]), r["type"])
        for n in world.snapshot()["nodes"]
        for r in n["disturbances"]
        if r["type"] == "localized_charge"
    ]
    print(f"\n=== mass emission {emission}, budget {BUDGET} ===")
    print(f"  contact transfers (source conversion, capture) at ticks: {captures}")
    print(f"  localized output: {localized}")
    print(f"  classical runner over the same {LENGTH - 1} links arrived at tick {runner_arrival}")
    print(f"  delayed carrier nodes (max delay count): {delays}")
    print(
        f"  quantum inventory charge: {report['quantum_inventory']['charge']}, draws {world._resolver.draws}"
    )


for emission in (0, 6000):
    run(emission)
