"""Four masses on Kerengonen signed quanta: escape speed against radius, ledger closed.

Every mass is a funded source of negative quanta rays (mirrored golden headings)
and absorbs the share mass / 256 of every ray from the others, paying from its
own stock and gaining momentum toward the emitter. The four sit on the axes at
distance R from the centre of an open slab and are launched outward at a common
speed v0 (momentum scale 65536 = one hop per tick). Newton: v_esc ~ 1/sqrt(R).

usage: python examples/relativity-probes/kerengonen_universe.py [R] [per_ray] [rays_per_tick] [ticks] [side]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
ARGS, sys.argv = sys.argv, sys.argv[:1]
from gravity_lensing import RAY_HEADINGS, RAY_SCALE  # noqa: E402
from kerengonen_lensing import mirrored_headings  # noqa: E402

sys.argv = ARGS

from event_universe import Simulation  # noqa: E402
from event_universe.core.disturbance_state import OPERATIONS  # noqa: E402
from event_universe.initialization import parse_initial_state  # noqa: E402

R = int(sys.argv[1]) if len(sys.argv) > 1 else 5
PER_RAY = int(sys.argv[2]) if len(sys.argv) > 2 else 16384
RAYS_PER_TICK = int(sys.argv[3]) if len(sys.argv) > 3 else 128
TICKS = int(sys.argv[4]) if len(sys.argv) > 4 else 60
SIDE = int(sys.argv[5]) if len(sys.argv) > 5 else 41
SHAPE = [SIDE, SIDE, 3]
CENTER = (SIDE // 2, SIDE // 2, 1)
SCALE = 65536
DENOMINATOR = 256
STOCK = 65536 * 8
AXES = ((1, 0), (-1, 0), (0, 1), (0, -1))


def op(name, *args):
    return {"op": name, "args": list(args)}


def document(v0):
    momentum = v0 * SCALE // 120
    seeds = [
        {
            "position": [CENTER[0] + ax * R, CENTER[1] + ay * R, CENTER[2]],
            "type": "mass body",
            "values": {"tag": tag, "momentum": [ax * momentum, ay * momentum, 0]},
        }
        for tag, (ax, ay) in enumerate(AXES, start=1)
    ]
    return {
        "schema_version": 1,
        "model_id": f"kerengonen-four-body-universe-v0-{v0}-v1",
        "boundary": "open",
        "shape": SHAPE,
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": 1_000_000,
        "ticks": TICKS,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {
                "name": "quanta",
                "components": 1,
                "units": "quantum",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "tag",
                "components": 1,
                "units": "label",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "mass body",
                "fields": ["quanta", "mass", "momentum", "tag"],
                "defaults": {"quanta": STOCK, "mass": 1, "momentum": [0, 0, 0], "tag": 0},
                "transport": {
                    "mode": "move",
                    "direction_field": "momentum",
                    "rate": op("min", SCALE, op("sum", op("abs", {"field": "momentum"}))),
                    "rate_denominator": SCALE,
                    "routing": "balanced",
                },
            }
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": mirrored_headings(RAY_HEADINGS, RAY_SCALE),
                "rays_per_tick": RAYS_PER_TICK,
                "ray_slots": 4096,
            }
        ],
        "emissions": [
            {
                "type": "mass body",
                "field": "quanta",
                "amount": -PER_RAY * RAYS_PER_TICK,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            }
        ],
        "spatial_couplings": [
            {
                "name": "pull",
                "type": "mass body",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
                "fraction": {"field": "mass"},
                "fraction_denominator": DENOMINATOR,
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


def run(v0):
    events = []
    world = Simulation(parse_initial_state(document(v0)), observer=events.append)
    history, escaped = [], {}
    for tick in range(1, TICKS + 1):
        world.step()
        for e in events:
            if e.get("event") == "escaped" and e["values"]["tag"][0] not in escaped:
                escaped[e["values"]["tag"][0]] = e["tick"]
        if tick % 10 == 0:
            found = positions(world)
            distances = [abs(p[0] - CENTER[0]) + abs(p[1] - CENTER[1]) for p, _ in found.values()]
            radial = [(p[0] - CENTER[0]) * m[0] + (p[1] - CENTER[1]) * m[1] for p, m in found.values()]
            history.append(
                (
                    tick,
                    sum(distances) / len(distances) if distances else float("nan"),
                    sum(r > 0 for r in radial),
                    sum(r < 0 for r in radial),
                )
            )
    return history, escaped


def label(history, escaped):
    if len(escaped) == 4:
        return f"ESCAPED (all four left by tick {max(escaped.values())})"
    first, last = R, history[-1][1]
    if last < first:
        return f"RECOLLAPSED (mean distance {first} -> {last:.1f})"
    if history[-1][3] and not history[-1][2]:
        return f"TURNED AROUND (mean distance {first} -> {last:.1f}, all moving inward)"
    return f"still expanding at tick {history[-1][0]} (mean distance {first} -> {last:.1f}), {len(escaped)} escaped"


if __name__ == "__main__":
    print(
        f"Kerengonen four-body universe: R {R}, {PER_RAY} per ray, {RAYS_PER_TICK} rays per tick per mass, {TICKS} ticks, side {SIDE}"
    )
    for v0 in (0, 15, 30, 45, 60, 90):
        history, escaped = run(v0)
        print(
            f"v0 = {v0:>3}/120 c: {label(history, escaped)}   "
            + " ".join(f"t{t}:{d:.1f}" for t, d, _, _ in history)
        )
