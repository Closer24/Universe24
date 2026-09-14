"""Twin clocks seen by the local observer: a traveller goes out to a mirror and returns."""

import sys

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state

HOME, MIRROR = 20, 32
BUDGET = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
RATE = int(sys.argv[2]) if len(sys.argv) > 2 else 60  # momentum per 120 = speed in c


def op(name, *args, **kw):
    node = {"op": name, "args": list(args)}
    node.update(kw)
    return node


def body(name, momentum, hold=False):
    return {
        "name": name,
        "fields": ["mass", "momentum", "clock"],
        "defaults": {"mass": 1, "momentum": momentum, "clock": 0},
        "updates": [{"field": "clock", "expression": op("add", {"field": "clock"}, 1)}],
        "transport": {"mode": "hold"}
        if hold
        else {
            "mode": "move",
            "direction_field": "momentum",
            "rate": op("sum", op("abs", {"field": "momentum"})),
            "rate_denominator": 120,
        },
    }


doc = {
    "schema_version": 1,
    "model_id": "observer-twin-clocks-probe-v1",
    "boundary": "open",
    "shape": [41, 3, 3],
    "slots_per_node": 3,
    "link_ticks": 1,
    "normal_budget": BUDGET,
    "ticks": 400,
    "operation_costs": {name: 1 for name in OPERATIONS},
    "fields": [
        {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
        {
            "name": "momentum",
            "components": 3,
            "units": "c/120",
            "signed": True,
            "conserved": False,
            "scale": 120,
        },
        {
            "name": "clock",
            "components": 1,
            "units": "completed local cycles",
            "signed": False,
            "conserved": False,
            "extensive": False,
        },
    ],
    "disturbance_types": [
        body("stay-at-home", [0, 0, 0], hold=True),
        body("traveller", [RATE, 0, 0]),
        {"name": "mirror", "fields": ["mass"], "defaults": {"mass": 1}, "transport": {"mode": "hold"}},
    ],
    "interactions": [
        {
            "name": "reflect_at_mirror",
            "left_type": "traveller",
            "right_type": "mirror",
            "when": op("gt", op("component", {"field": "momentum", "side": "left"}, index=0), 0),
            "assignments": [
                {
                    "side": "left",
                    "field": "momentum",
                    "expression": op(
                        "transform",
                        {"field": "momentum", "side": "left"},
                        matrix=[[-1, 0, 0], [0, 1, 0], [0, 0, 1]],
                    ),
                }
            ],
            "invariants": [{"name": "left_mass", "expression": {"field": "mass", "side": "left"}}],
        }
    ],
    "seeds": [
        {"position": [HOME, 1, 1], "type": "stay-at-home"},
        {"position": [HOME, 1, 1], "type": "traveller"},
        {"position": [MIRROR, 1, 1], "type": "mirror"},
    ],
    "observer": {"position": [HOME, 1, 1], "max_receipts": 100000},
}

events = []
world = Simulation(parse_initial_state(doc), observer=events.append)
returned = None
for _tick in range(doc["ticks"]):
    world.step()
    arrival = next(
        (
            e
            for e in events
            if e.get("event") == "received"
            and tuple(e["position"]) == (HOME, 1, 1)
            and e.get("disturbance") == "traveller"
        ),
        None,
    )
    if arrival is not None:
        returned = arrival
        break

home_clock = next(
    world.record_values(r)["clock"][0]
    for n in world.nodes.values()
    for r in n.records
    if r is not None and doc["disturbance_types"][r.type_index]["name"] == "stay-at-home"
)
costs = sorted({e["cost"] for e in events if e.get("event") == "cycle_started"})
print(f"budget {BUDGET}, nominal speed {RATE}/120 c, cycle costs seen {costs}")
if returned is None:
    print("traveller did not return within the run")
else:
    traveller_clock = returned["values"]["clock"][0]
    print(f"traveller received back at home at audit tick {returned['tick']} (port {returned['port']})")
    print(
        f"  observer's own process clock: {home_clock} cycles; traveller's carried clock: {traveller_clock} cycles"
    )
    print(
        f"  ratio traveller/home = {traveller_clock / home_clock:.3f}; round trip {2 * (MIRROR - HOME)} links in {returned['tick']} ticks -> actual mean speed {2 * (MIRROR - HOME) / returned['tick']:.3f} c"
    )
