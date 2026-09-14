"""Bodies passing a mass whose computation field is coupled to their momentum.

Everything physical is supplied in JSON: the mass emits the `computation` field,
every body exchanges momentum with that field's delivered flux times its own mass
(the sign is a supplied convention, exactly as in examples/charged-pair), and the
same field optionally sets the shared node clock (`spatial_computation_delay`).
The engine only splits, routes and prices integer work.

Newtonian expectation for the momentum-only coupling: impulse ~ m/(b v), so the
deflection angle ~ 1/(b v^2). A slow body at c/2 should deflect four times more
than light at the same impact parameter; halving b doubles the angle.
Relativity check: under the shared clock a body near the mass spends more
intervals per cycle inside the strong field, so light should bend more than the
momentum coupling alone predicts (the time-dilation half of the GR deflection).

usage: python examples/relativity-probes/gravity_lensing.py [emission] [denominator] [budget]
"""

import sys
from collections import defaultdict

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state

SHAPE = [37, 17, 17]
MASS = (18, 8, 8)
EMISSION = int(sys.argv[1]) if len(sys.argv) > 1 else 24000
DENOMINATOR = int(sys.argv[2]) if len(sys.argv) > 2 else 40
BUDGET = int(sys.argv[3]) if len(sys.argv) > 3 else 60
# +1 pulls a body toward the source under the delivered-flux sign convention (the
# first run with -1 pushed every body away); the sign is supplied, not derived.
SIGN = int(sys.argv[4]) if len(sys.argv) > 4 else 1
TICKS = int(sys.argv[6]) if len(sys.argv) > 6 else 30
# "rays": the mass emits straight rays (isotropic-ray-field-v1) instead of octant
# populations, so the far field is not concentrated on the lattice axes.
RAYS = len(sys.argv) > 7 and sys.argv[7] == "rays"
BODIES = {"light": 120, "slow": 60}  # momentum along x; mass 1, so speed = p/120 c
# 512 headings at 64 rays per tick gave 375 units per ray: a body at b = 7 met no
# ray in 30 ticks and b = 5 outscored b = 3. Finer quanta (47 units per ray, 512
# rays per tick over 4096 headings) sample the sphere densely enough per node.
RAY_HEADINGS, RAY_SCALE, RAYS_PER_TICK, RAY_SLOTS = 4096, 24, 512, 4096


def op(name, *args, **kw):
    node = {"op": name, "args": list(args)}
    node.update(kw)
    return node


def golden_headings(count, scale):
    """Integer headings spread evenly over the sphere (configuration data only)."""
    import math

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
    # The spiral index runs from the north pole to the south pole, so consecutive
    # rays_per_tick headings would form one latitude band per tick and the
    # equatorial plane would see rays only in bursts. A stride coprime to the
    # count spreads every tick's rays over the whole sphere (still a fixed,
    # deterministic sequence).
    stride = 1597
    return [result[(i * stride) % count] for i in range(count)]


def computation_definition():
    if RAYS:
        return {
            "field": "computation",
            "baseline": 0,
            "transport": "ray",
            "headings": golden_headings(RAY_HEADINGS, RAY_SCALE),
            "rays_per_tick": RAYS_PER_TICK,
            "ray_slots": RAY_SLOTS,
        }
    return {"field": "computation", "baseline": 0, "transport": "outward"}


def body(name, momentum):
    return {
        "name": name,
        "fields": ["mass", "momentum", "tag"],
        "defaults": {"mass": 1, "momentum": [momentum, 0, 0], "tag": 0},
        "transport": {
            "mode": "move",
            "direction_field": "momentum",
            "rate": op("min", 120, op("sum", op("abs", {"field": "momentum"}))),
            "rate_denominator": 120,
            # Balanced routing interleaves lanes by the reduced weight ratio;
            # the default cyclic walk would spend 120 moves on x first.
            "routing": "balanced",
        },
    }


def document(clock, emission=EMISSION):
    seeds = [{"position": list(MASS), "type": "mass body"}]
    tags = {}
    tag = 0
    for kind, momentum in BODIES.items():
        start_x = MASS[0] - 16 * momentum // 120  # every body passes the mass near tick 16
        for b in (3, 5, 7):
            for side in (1, -1):
                tag += 1
                tags[tag] = (kind, b, side)
                seeds.append(
                    {
                        "position": [start_x, MASS[1] + side * b, MASS[2]],
                        "type": kind,
                        "values": {"tag": tag},
                    }
                )
    doc = {
        "schema_version": 1,
        "model_id": f"gravity-lensing-{clock}-v1",
        "boundary": "open",
        "shape": SHAPE,
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": BUDGET if clock == "shared" else 1_000_000,
        "ticks": TICKS,
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
                "fields": ["mass"],
                "defaults": {"mass": 1},
                "transport": {"mode": "hold"},
            },
            *(body(kind, momentum) for kind, momentum in BODIES.items()),
        ],
        "spatial_fields": [
            computation_definition(),
            {"field": "momentum", "baseline": [0, 0, 0], "transport": "outward"},
        ],
        "emissions": [
            {
                "type": "mass body",
                "field": "computation",
                "amount": emission,
                "denominator": 1,
                "source": True,
            },
        ],
        "spatial_couplings": [
            {
                "name": f"{kind}_mass_times_flux",
                "type": kind,
                "field": "momentum",
                "mode": "exchange",
                "amount": op("mul", SIGN, op("mul", {"field": "mass"}, {"flux": "computation"})),
                "denominator": DENOMINATOR,
            }
            for kind in BODIES
        ],
        "seeds": seeds,
    }
    if clock != "default":
        # Only the delay modes read the field as computation load (outward only).
        doc["computation_field"] = "computation"
    if clock == "shared":
        doc["spatial_computation_delay"] = True
    elif clock in ("along", "against"):
        # Default clock; each departure is delayed by the load delivered through
        # (or against) its port, so the source node does not throttle itself.
        doc["delay_direction"] = clock
        doc["normal_budget"] = BUDGET
    return doc, tags


def run(clock, emission=EMISSION):
    doc, tags = document(clock, emission)
    world = Simulation(parse_initial_state(doc))
    for _ in range(TICKS):
        world.step()
    snap = world.snapshot()
    final = {}
    for node in snap["nodes"]:
        for record in node["disturbances"]:
            if "tag" in record["values"] and record["values"]["tag"][0]:
                final[record["values"]["tag"][0]] = (node["position"], record["values"]["momentum"])
    for packet in snap["transfers"]:
        if "tag" in packet["values"] and packet["values"]["tag"][0]:
            final[packet["values"]["tag"][0]] = (packet["origin"], packet["values"]["momentum"])
    delays = defaultdict(int)
    for node in snap["nodes"]:
        if node["delay_counts"] and max(node["delay_counts"]):
            delays[max(node["delay_counts"])] += 1
    return tags, final, world.totals()["momentum"], dict(sorted(delays.items()))


def report(clock, emission=EMISSION):
    tags, final, total, delays = run(clock, emission)
    print(
        f"\n=== clock {clock}, field {'rays' if RAYS else 'octants'}, emission {emission}, "
        f"denominator {DENOMINATOR}, budget {BUDGET} ==="
    )
    print(f"momentum total (carriers + field): {total}; carrier nodes by delay count: {delays}")
    angles = {}
    for tag, (kind, b, side) in tags.items():
        if tag not in final:
            print(f"  {kind:<5} b={b} side={side:+d}: lost (escaped)")
            continue
        position, p = final[tag]
        toward = -side * p[1]  # positive when the transverse momentum points at the mass
        angles[(kind, b, side)] = toward / p[0] if p[0] else float("nan")
        print(
            f"  {kind:<5} b={b} side={side:+d}: at {position} p={p}  angle toward mass {angles[(kind, b, side)]:+.4f}"
        )
    mean = {}
    for kind in BODIES:
        for b in (3, 5, 7):
            pair = [angles[k] for k in angles if k[0] == kind and k[1] == b]
            if pair:
                mean[(kind, b)] = sum(pair) / len(pair)
    if (
        all((k, b) in mean for k in BODIES for b in (3, 5, 7))
        and mean[("light", 7)]
        and mean[("light", 5)]
    ):
        print(
            f"  angle ratios: b3/b7 light {mean[('light', 3)] / mean[('light', 7)]:.2f} (Newton 2.33), "
            f"slow/light at b5 {mean[('slow', 5)] / mean[('light', 5)]:.2f} (Newton 4.00)"
        )
    return mean


if __name__ == "__main__":
    which = sys.argv[5] if len(sys.argv) > 5 else "all"
    if which in ("default", "all"):
        report("default")
    if which in ("shared", "all"):
        report("shared")
    if which in ("along", "against"):
        report(which)
    if which in ("control", "all"):
        report("default", emission=0)
