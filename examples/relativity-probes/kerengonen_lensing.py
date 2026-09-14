"""Lensing on Kerengonen signed quanta: the pulled body pays for its pull.

The mass is a funded source of negative `quanta` rays over mirrored golden
headings (docs/SPATIAL_FIELDS.md, funded emission and absorption): it is
credited with what it emits and every ray's momentum points back at it. A
passing body absorbs the share mass / 256 of every ray crossing its Node, pays
that share from its own quanta stock and gains the share's momentum toward the
source. No exchange reservoir, no engine gravity: the ledger of quanta and
momentum closes by construction.

Light bodies (momentum 65536 = one hop per tick) and slow bodies (32768, half
a hop per tick) pass at impact parameters 3, 5 and 7 on both sides. Newton:
angle ~ 1/(b v^2); the slow body deflects four times more, b = 3/7 gives 2.33.

usage: python examples/relativity-probes/kerengonen_lensing.py [per_ray] [rays_per_tick] [ticks]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
ARGS, sys.argv = sys.argv, sys.argv[:1]
from gravity_lensing import RAY_HEADINGS, RAY_SCALE, golden_headings  # noqa: E402

sys.argv = ARGS

from event_universe import Simulation  # noqa: E402
from event_universe.core.disturbance_state import OPERATIONS  # noqa: E402
from event_universe.initialization import parse_initial_state  # noqa: E402

SHAPE = [37, 17, 17]
MASS = (18, 8, 8)
PER_RAY = int(sys.argv[1]) if len(sys.argv) > 1 else 4096
RAYS_PER_TICK = int(sys.argv[2]) if len(sys.argv) > 2 else 512
TICKS = int(sys.argv[3]) if len(sys.argv) > 3 else 30
SCALE = 65536  # momentum of one hop per tick for unit mass
DENOMINATOR = 256  # absorbed share of each crossing ray is mass / 256
STOCK = 65536 * 4  # quanta a body can pay for its pull
BODIES = {"light": SCALE, "slow": SCALE // 2}


def op(name, *args):
    return {"op": name, "args": list(args)}


def mirrored_headings(count, scale):
    result = []
    for heading in golden_headings(count // 2, scale):
        mirror = [-c for c in heading]
        if heading not in result and mirror not in result:
            result.extend([heading, mirror])
    return result


def body(name, momentum):
    return {
        "name": name,
        "fields": ["quanta", "mass", "momentum", "tag"],
        "defaults": {"quanta": STOCK, "mass": 1, "momentum": [momentum, 0, 0], "tag": 0},
        "transport": {
            "mode": "move",
            "direction_field": "momentum",
            "rate": op("min", SCALE, op("sum", op("abs", {"field": "momentum"}))),
            "rate_denominator": SCALE,
            "routing": "balanced",
        },
    }


def document():
    seeds = [{"position": list(MASS), "type": "source"}]
    tags = {}
    tag = 0
    for kind, momentum in BODIES.items():
        start_x = MASS[0] - 16 * momentum // SCALE
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
        "model_id": "kerengonen-signed-quanta-lensing-v1",
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
                "name": "source",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            *(body(kind, momentum) for kind, momentum in BODIES.items()),
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
                "type": "source",
                "field": "quanta",
                "amount": -PER_RAY * RAYS_PER_TICK,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            }
        ],
        "spatial_couplings": [
            {
                "name": f"pull_{kind}",
                "type": kind,
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
                "fraction": {"field": "mass"},
                "fraction_denominator": DENOMINATOR,
            }
            for kind in BODIES
        ],
        "seeds": seeds,
    }
    return doc, tags


def run():
    doc, tags = document()
    world = Simulation(parse_initial_state(doc))
    for _ in range(TICKS):
        world.step()
    snap = world.snapshot()
    final = {}
    for node in snap["nodes"]:
        for record in node["disturbances"]:
            if "tag" in record["values"] and record["values"]["tag"][0]:
                values = record["values"]
                final[values["tag"][0]] = (node["position"], values["momentum"], values["quanta"][0])
    for packet in snap["transfers"]:
        if "tag" in packet["values"] and packet["values"]["tag"][0]:
            values = packet["values"]
            final[values["tag"][0]] = (packet["origin"], values["momentum"], values["quanta"][0])
    totals, escaped = world.totals(), world.escaped_totals()
    print(
        f"=== Kerengonen signed quanta: {PER_RAY} per ray, {RAYS_PER_TICK} rays per tick, "
        f"share 1/{DENOMINATOR}, {TICKS} ticks ==="
    )
    print(
        f"quanta in the world {totals['quanta'][0]} + escaped {escaped['quanta'][0]} "
        f"(initial stock {12 * STOCK}); momentum in the world {totals['momentum']} "
        f"+ escaped {escaped['momentum']}"
    )
    angles = {}
    for tag, (kind, b, side) in tags.items():
        if tag not in final:
            print(f"  {kind:<5} b={b} side={side:+d}: lost (escaped)")
            continue
        position, p, quanta = final[tag]
        toward = -side * p[1]
        angles[(kind, b, side)] = toward / p[0] if p[0] else float("nan")
        print(
            f"  {kind:<5} b={b} side={side:+d}: at {position} p={tuple(p)} paid {STOCK - quanta} quanta  "
            f"angle toward mass {angles[(kind, b, side)]:+.4f}"
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


if __name__ == "__main__":
    run()
