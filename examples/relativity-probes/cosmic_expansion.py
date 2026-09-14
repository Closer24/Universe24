"""A four-body universe under the computation-field coupling: recollapse or escape?

Four equal masses sit on the axes at distance R from the centre of an open slab,
each launched outward with the same speed v0 (momentum scale 120 = c). Every
mass emits the `computation` field and exchanges momentum with the delivered
flux of that field times its own mass (attractive sign supplied, as in the
lensing probe). No expansion term, pressure or cosmological constant exists in
the configuration: whatever happens is the coupling plus the initial motion.

For each v0 the probe reports the mean distance of the bodies from the centre
over time, whether the bodies turned around (recollapse) or left the slab
(escape), and the speed at which the two regimes separate.

usage: python examples/relativity-probes/cosmic_expansion.py [emission] [denominator] [R] [ticks]
"""

import sys

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state

EMISSION = int(sys.argv[1]) if len(sys.argv) > 1 else 24000
DENOMINATOR = int(sys.argv[2]) if len(sys.argv) > 2 else 80
R = int(sys.argv[3]) if len(sys.argv) > 3 else 5
TICKS = int(sys.argv[4]) if len(sys.argv) > 4 else 60
SHAPE = [29, 29, 3]
CENTER = (14, 14, 1)
AXES = ((1, 0), (-1, 0), (0, 1), (0, -1))


def op(name, *args):
    return {"op": name, "args": list(args)}


def document(v0, emission):
    seeds = []
    for tag, (ax, ay) in enumerate(AXES, start=1):
        seeds.append(
            {
                "position": [CENTER[0] + ax * R, CENTER[1] + ay * R, CENTER[2]],
                "type": "mass body",
                "values": {"tag": tag, "momentum": [ax * v0, ay * v0, 0]},
            }
        )
    return {
        "schema_version": 1,
        "model_id": f"four-body-universe-v0-{v0}-v1",
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
                "name": "tag",
                "components": 1,
                "units": "label",
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
                "fields": ["mass", "momentum", "tag"],
                "defaults": {"mass": 1, "momentum": [0, 0, 0], "tag": 0},
                "transport": {
                    "mode": "move",
                    "direction_field": "momentum",
                    "rate": op("min", 120, op("sum", op("abs", {"field": "momentum"}))),
                    "rate_denominator": 120,
                    "routing": "balanced",
                },
            }
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
                "name": "mass_times_flux",
                "type": "mass body",
                "field": "momentum",
                "mode": "exchange",
                "amount": op("mul", 1, op("mul", {"field": "mass"}, {"flux": "computation"})),
                "denominator": DENOMINATOR,
            }
        ],
        "seeds": seeds,
    }


def positions(world):
    found = {}
    snap = world.snapshot()
    for node in snap["nodes"]:
        for record in node["disturbances"]:
            tag = record["values"]["tag"][0]
            if tag:
                found[tag] = (tuple(node["position"]), tuple(record["values"]["momentum"]))
    for packet in snap["transfers"]:
        tag = packet["values"]["tag"][0]
        if tag:
            found[tag] = (tuple(packet["origin"]), tuple(packet["values"]["momentum"]))
    return found


def run(v0, emission):
    events = []
    world = Simulation(parse_initial_state(document(v0, emission)), observer=events.append)
    history = []
    escaped = {}
    for tick in range(1, TICKS + 1):
        world.step()
        for e in events:
            if e.get("event") == "escaped" and e["values"]["tag"][0] not in escaped:
                escaped[e["values"]["tag"][0]] = e["tick"]
        found = positions(world)
        if tick % 10 == 0 or tick == 1:
            distances = [abs(p[0] - CENTER[0]) + abs(p[1] - CENTER[1]) for p, _ in found.values()]
            radial = [(p[0] - CENTER[0]) * m[0] + (p[1] - CENTER[1]) * m[1] for p, m in found.values()]
            history.append(
                (
                    tick,
                    sum(distances) / len(distances) if distances else float("nan"),
                    sum(1 for r in radial if r > 0),
                    sum(1 for r in radial if r < 0),
                    len(found),
                )
            )
    return history, escaped


def label(history, escaped):
    if len(escaped) == 4:
        return f"ESCAPED (all four left the slab by tick {max(escaped.values())})"
    first = history[0][1]
    peak = max(h[1] for h in history)
    last = history[-1][1]
    if last < first:
        return f"RECOLLAPSED (mean distance {first:.1f} -> peak {peak:.1f} -> {last:.1f})"
    if any(h[3] and not h[2] for h in history[1:]):
        return f"TURNED AROUND (mean distance {first:.1f} -> peak {peak:.1f} -> {last:.1f}, all moving inward)"
    return f"still expanding at tick {history[-1][0]} (mean distance {first:.1f} -> {last:.1f}), {len(escaped)} escaped"


if __name__ == "__main__":
    print(f"emission {EMISSION}, denominator {DENOMINATOR}, R {R}, ticks {TICKS}")
    print("control without a field: v0 = 60 ->", label(*run(60, 0)))
    for v0 in (0, 15, 30, 45, 60, 90, 120):
        history, escaped = run(v0, EMISSION)
        print(f"\nv0 = {v0:>3}/120 c: {label(history, escaped)}")
        print("   tick | mean |r| | moving out | moving in | bodies")
        for tick, mean, out, inward, n in history:
            print(f"   {tick:>4} | {mean:>8.2f} | {out:>10} | {inward:>9} | {n}")
