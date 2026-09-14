"""Does a growing computation load along a light path stretch a pulse train (redshift)?

A train of twelve light bodies one link apart runs at c along a row past a
mass whose emission of the `computation` field grows every cycle (a universe
still filling with field). Under `delay_direction: "along"` each departure is
delayed by the load delivered through its port, so a body that passes the mass
later meets more load and waits longer. An eye at the end of the row is a local
observer: it records only the arrival tick of each body. Spacing above one link
per tick is a redshift z = spacing - 1 produced by delay growth, with no
recession and no expansion term. The control keeps the emission at zero.

usage: python examples/relativity-probes/redshift_without_expansion.py [growth] [budget]
"""

import sys

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state

GROWTH = int(sys.argv[1]) if len(sys.argv) > 1 else 600  # emission added per mass cycle
BUDGET = int(sys.argv[2]) if len(sys.argv) > 2 else 40
SHAPE = [37, 9, 5]
MASS = (18, 6, 2)
ROW, EYE_X, TRAIN = 2, 34, 12
TICKS = 60


def op(name, *args):
    return {"op": name, "args": list(args)}


def document(growth):
    return {
        "schema_version": 1,
        "model_id": "redshift-from-delay-growth-v1",
        "boundary": "open",
        "shape": SHAPE,
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": BUDGET,
        "ticks": TICKS,
        "computation_field": "computation",
        "delay_direction": "along",
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
            {
                "name": "age",
                "components": 1,
                "units": "completed cycles",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
            {
                "name": "tag",
                "components": 1,
                "units": "train index",
                "signed": False,
                "conserved": False,
                "extensive": False,
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
            {
                "name": "computation",
                "components": 1,
                "units": "load unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "mass body",
                "fields": ["mass", "age"],
                "defaults": {"mass": 1, "age": 0},
                "updates": [{"field": "age", "expression": op("add", {"field": "age"}, 1)}],
                "transport": {"mode": "hold"},
            },
            {"name": "eye", "fields": ["mass"], "defaults": {"mass": 1}, "transport": {"mode": "hold"}},
            {
                "name": "light",
                "fields": ["mass", "momentum", "tag"],
                "defaults": {"mass": 1, "momentum": [120, 0, 0], "tag": 0},
                "transport": {
                    "mode": "move",
                    "direction_field": "momentum",
                    "rate": 120,
                    "rate_denominator": 120,
                    # Cyclic routing: the train only moves +x, and balanced routing
                    # prices 512 route operations per cycle, which would exceed the
                    # small budget on its own and delay every hop uniformly.
                },
            },
        ],
        "spatial_fields": [{"field": "computation", "baseline": 0, "transport": "outward"}],
        "emissions": [
            {
                "type": "mass body",
                "field": "computation",
                "amount": op("mul", {"field": "age"}, growth),
                "denominator": 1,
                "source": True,
            }
        ],
        "seeds": [{"position": list(MASS), "type": "mass body"}]
        + [
            {"position": [2 + i, ROW, MASS[2]], "type": "light", "values": {"tag": TRAIN - i}}
            for i in range(TRAIN)
        ]
        + [{"position": [EYE_X, ROW, MASS[2]], "type": "eye"}],
    }


def observe(growth):
    events = []
    world = Simulation(parse_initial_state(document(growth)), observer=events.append)
    for _ in range(TICKS):
        world.step()
    arrivals = {}
    for e in events:
        if (
            e.get("event") == "received"
            and e.get("disturbance") == "light"
            and tuple(e["position"]) == (EYE_X, ROW, MASS[2])
        ):
            arrivals[e["values"]["tag"][0]] = e["tick"]
    return arrivals


for growth in (0, GROWTH):
    arrivals = observe(growth)
    order = sorted(arrivals)
    ticks = [arrivals[t] for t in order]
    gaps = [b - a for a, b in zip(ticks, ticks[1:])]
    print(f"\n=== emission growth {growth} per mass cycle, budget {BUDGET}: what the eye records ===")
    print("  body (1 = first to pass the mass) -> arrival tick:", dict(zip(order, ticks)))
    print("  gaps between successive arrivals:", gaps)
    if gaps:
        early, late = gaps[: len(gaps) // 2], gaps[len(gaps) // 2 :]
        print(
            f"  z = spacing - 1: early pairs {sum(early) / len(early) - 1:+.2f}, "
            f"late pairs {sum(late) / len(late) - 1:+.2f}"
        )
    print(f"  bodies not received within {TICKS} ticks: {TRAIN - len(arrivals)}")
