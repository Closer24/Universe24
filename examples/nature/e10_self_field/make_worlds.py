"""Write the worlds of experiment E10 (docs/EXPERIMENTS.md), the ring meets its
own field: the unit-square electron of E5 (`examples/nature/ring.json`) with
the rays of E9 (amount 4, 8 or 16 per ray, content 32, 64 or 128, the
catalog's rest rate 1) on a 12^3 open board, its field `light` declared as in
`screen_loop.json` (`field_of` electron, `release` [1, 4], `spread`
[6, 1, 1, 1, 1, 1], the source sign set by the engine), no Detector mark, and
the catalog's `electron_field_turn` in its momentum-table form (`{"light": 1}`,
like charges repel: a ring ray is pushed away from the source of every light
ray it meets and the light returns reversed) declared beside the corner
table.

Three worlds per content:

- `control`: the corner table alone, E9's form (no rule names `light`).
- `corner_first`: the corner table declared first, the coupling second.
- `turn_first`: the coupling declared first, the corner table second.

The two orders exist because the engine meets a Node's rays in declared order
and a ray one rule took is not available to a later rule in the same cycle
(`ray-meeting-conversion-v1`, `ray-momentum-turn-v2`; `_meet` in
`src/event_universe/fields/ray_interactions.py`); on the unit square every
ring Node is a corner, so which rule meets a ring ray in a cycle is the
declared order, and the run registers both.

Run:  python examples/nature/e10_self_field/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bit_law_migration import migrate  # noqa: E402

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# The unit square of ring.json in the plane z = 5, centred on the 12^3 board.
P0, P1, P2, P3 = (5, 5, 5), (6, 5, 5), (6, 6, 5), (5, 6, 5)
CORNERS = (P0, P1, P2, P3)
# The R sense P0 -> P1 -> P2 -> P3 -> P0 (+X, +Y, -X, -Y) and the L sense
# P0 -> P3 -> P2 -> P1 -> P0 (+Y, -X, -Y, +X): the Port each sense leaves each
# corner through, ring.json's lamps.
R_PORTS = (0, 2, 1, 3)
L_PORTS = (2, 1, 3, 0)
# The amount per ray: at the release ratio [1, 4] a ray of amount a releases
# a / 4 per heading, so 4, 8 and 16 release 1, 2 and 4; content 8 x amount.
AMOUNTS = (4, 8, 16)
RELEASE = [1, 4]
SPREAD = [6, 1, 1, 1, 1, 1]
SHAPE = [12, 12, 12]
TICKS = 96
PHASE_BITS = 3
RATE = 1
CHARGE = -3
VARIANTS = ("control", "corner_first", "turn_first")


def lamps():
    """The corner lamps: (position, name, Port), one per sense per corner."""
    result = []
    for k in range(4):
        result.append((CORNERS[k], f"corner_{k}_r", R_PORTS[k]))
        result.append((CORNERS[k], f"corner_{k}_l", L_PORTS[k]))
    return result


def ray_family(name, slots, rate, charge, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": slots,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": PHASE_BITS,
        "charge": charge,
        "kerengonen": {"phase_advance": rate},
        **extra,
    }


def scalar(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


def corner_rule():
    """The Port form of the corner table (loop-binding-v1): each input's amount
    and phase leave through the Port the other input came in by."""
    return {
        "name": "corner",
        "participants": [{"type": "electron"}, {"type": "electron"}],
        "outputs": [
            {
                "field": "electron",
                "amount": {"of": 0},
                "heading": "reversed",
                "input": 1,
                "phase": {"of": 0},
            },
            {
                "field": "electron",
                "amount": {"of": 1},
                "heading": "reversed",
                "input": 0,
                "phase": {"of": 1},
            },
        ],
        "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
    }


def turn_rule():
    """The catalog's electron_field_turn in its momentum-table form
    (ray-momentum-turn-v2): the electron pushed by sign x amount x heading of
    every light ray it meets, +1 for repulsion, the light returned reversed."""
    return {
        "name": "electron_field_turn",
        "participants": [{"type": "electron"}, {"type": "light"}],
        "momentum_table": {"light": 1},
        "invariants": [
            {
                "name": "energy",
                "expression": {
                    "op": "add",
                    "args": [
                        {"field": "amount", "participant": 0},
                        {"field": "amount", "participant": 1},
                    ],
                },
            }
        ],
    }


def rules(variant):
    if variant == "control":
        return [corner_rule()]
    if variant == "corner_first":
        return [corner_rule(), turn_rule()]
    if variant == "turn_first":
        return [turn_rule(), corner_rule()]
    raise ValueError(variant)


def world(amount, variant, *, ticks=TICKS):
    return migrate(_world(amount, variant, ticks=ticks))


def _world(amount, variant, *, ticks=TICKS):
    content = 8 * amount
    return {
        "schema_version": 1,
        "model_id": f"e10-self-field-c{content}-{variant.replace('_', '-')}",
        "shape": list(SHAPE),
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            scalar("electron"),
            scalar("light"),
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
                "fields": ["electron", "momentum"],
                "defaults": {"electron": amount, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for _, name, _ in lamps()
        ],
        "spatial_fields": [
            ray_family("electron", 8, RATE, CHARGE),
            ray_family("light", 24, 0, 0, field_of="electron", release=RELEASE, spread=SPREAD),
        ],
        "emissions": [
            {
                "type": name,
                "field": "electron",
                "amount": amount,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": HEADINGS[port],
                "kerengonen_phase": 0,
            }
            for _, name, port in lamps()
        ],
        "seeds": [{"position": list(position), "type": name} for position, name, _ in lamps()],
        "ray_interactions": rules(variant),
    }


def cases():
    for amount in AMOUNTS:
        for variant in VARIANTS:
            yield f"c{8 * amount}_{variant}", world(amount, variant)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in cases():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path, document["shape"], document["ticks"], document["model_id"])


if __name__ == "__main__":
    main()
