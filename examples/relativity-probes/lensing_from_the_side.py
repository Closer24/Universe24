"""Lensing seen by local observers: a row of eyes behind the mass reports only what lands on it.

Light bodies leave a lamp column at x=2 (one per row y), pass the mass and reach a
column of held eyes at x=34. Each eye is a local observer: it sees the arrival
tick, the entry port and the arriving momentum of whatever reaches its own node,
nothing else. From the arrival direction an eye infers where the lamp appears to
be (tracing the ray back along -p). With the mass present the apparent lamp is
displaced away from the mass, as in gravitational lensing; without it every eye
sees its own row.

usage: python examples/relativity-probes/lensing_from_the_side.py [emission] [denominator]
"""

import sys

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state

SHAPE = [37, 17, 17]
MASS = (18, 8, 8)
LAMP_X, EYE_X = 2, 34
EMISSION = int(sys.argv[1]) if len(sys.argv) > 1 else 24000
DENOMINATOR = int(sys.argv[2]) if len(sys.argv) > 2 else 80
TICKS = 40
PORT = {0: "+x", 1: "-x", 2: "+y", 3: "-y", 4: "+z", 5: "-z"}


def op(name, *args):
    return {"op": name, "args": list(args)}


def document(emission):
    doc = {
        "schema_version": 1,
        "model_id": "lensing-from-the-side-v1",
        "boundary": "open",
        "shape": SHAPE,
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": 1_000_000,
        "ticks": TICKS,
        "computation_field": "computation",
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
            {
                "name": "row",
                "components": 1,
                "units": "lamp row",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "c/120",
                "signed": True,
                "conserved": True,
                "extensive": True,
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
                "fields": ["mass"],
                "defaults": {"mass": 1},
                "transport": {"mode": "hold"},
            },
            {"name": "eye", "fields": ["mass"], "defaults": {"mass": 1}, "transport": {"mode": "hold"}},
            {
                "name": "light",
                "fields": ["mass", "momentum", "row"],
                "defaults": {"mass": 1, "momentum": [120, 0, 0], "row": 0},
                "transport": {
                    "mode": "move",
                    "direction_field": "momentum",
                    "rate": op("min", 120, op("sum", op("abs", {"field": "momentum"}))),
                    "rate_denominator": 120,
                },
            },
        ],
        "spatial_fields": [
            {"field": "computation", "baseline": 0, "transport": "outward"},
            {"field": "momentum", "baseline": [0, 0, 0], "transport": "outward"},
        ],
        "emissions": [
            {
                "type": "mass body",
                "field": "computation",
                "amount": emission,
                "denominator": 1,
                "source": True,
            }
        ],
        "spatial_couplings": [
            {
                "name": "light_mass_times_flux",
                "type": "light",
                "field": "momentum",
                "mode": "exchange",
                "amount": op("mul", 1, op("mul", {"field": "mass"}, {"flux": "computation"})),
                "denominator": DENOMINATOR,
            }
        ],
        "seeds": [{"position": list(MASS), "type": "mass body"}]
        + [
            {"position": [LAMP_X, y, MASS[2]], "type": "light", "values": {"row": y}}
            for y in range(1, 16)
            if y != MASS[1]
        ]
        + [{"position": [EYE_X, y, MASS[2]], "type": "eye"} for y in range(0, 17)],
    }
    return doc


def observe(emission):
    events = []
    world = Simulation(parse_initial_state(document(emission)), observer=events.append)
    for _ in range(TICKS):
        world.step()
    seen = {}
    for e in events:
        if (
            e.get("event") == "received"
            and e.get("disturbance") == "light"
            and e["position"][0] == EYE_X
        ):
            y = e["position"][1]
            seen.setdefault(y, []).append(
                (e["tick"], PORT[e["port"]], tuple(e["values"]["momentum"]), e["values"]["row"][0])
            )
    return seen


for emission in (0, EMISSION):
    seen = observe(emission)
    print(f"\n=== eyes at x={EYE_X}, mass emission {emission} (what each eye receives) ===")
    print(
        "  eye y | tick | via | arriving p        | lamp row | apparent lamp y (ray traced back along -p)"
    )
    for y in sorted(seen):
        for tick, port, p, row in seen[y]:
            apparent = y - (EYE_X - LAMP_X) * p[1] / p[0]
            print(f"  {y:>5} | {tick:>4} | {port:>3} | {str(p):<17} | {row:>8} | {apparent:.1f}")
    rows_seen = {row for arrivals in seen.values() for _, _, _, row in arrivals}
    print(f"  rows not seen by any eye: {sorted(set(range(1, 16)) - {MASS[1]} - rows_seen)}")
