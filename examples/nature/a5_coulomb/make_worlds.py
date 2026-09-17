"""Write the worlds of experiment A5 (docs/EXPERIMENTS.md): two charged rays on
antiparallel lines along x at impact parameter b, each releasing its field
`light` (field_of, release [1, 4]) which spreads by the catalog's table
[6, 1, 1, 1, 1, 1], and the coupling `electron_field_turn` as a momentum table
(ray-momentum-turn-v1): +1 (repulsion) for a field ray whose source has the
ray's own sign, -1 (attraction) for the opposite sign.

The engine names one light family per releaser (catalog, `light`), so each ray's
field is its own family, `light_a` and `light_b`, and the sign of the source
reaches the coupling through the family: the engine sets `source_sign` on every
released ray from the releaser's charge (-1 for the electron, +1 for the
positron), and no `when` guard can read it today (RAY_PROPERTIES holds amount,
heading, phase, advance, delay, family, charge and detector), so the table names
the family that carries the sign, never the phase. A role takes one family, so
each coupling names the other ray's field alone; whether a ray ever shares a
Node with its own field (the self-meeting clause) is read from the record, the
`spatial_received` line of the Node the ray arrives at.

Run:  python examples/nature/a5_coulomb/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
IMPACT_PARAMETERS = (4, 6, 8, 12, 16)
# The electron amount: 64 quanta, so the release [1, 4] gives 16 per heading and
# the momentum register resolves a transfer of one quantum in 64.
AMOUNT = 64
RELEASE = [1, 4]
SPREAD = [6, 1, 1, 1, 1, 1]
PHASE_BITS = 12
# The board: A5 names 49 x 49 x 49; the x extent is 97 so that both rays are on
# the board 3b past closest approach for b = 16 (closest approach at x = 48,
# tick 48; read-off at tick 48 + 3b).
SHAPE = [97, 49, 49]
CENTER_Y, CENTER_Z = 24, 24
START_A, START_B = 0, 96
CLOSEST = (START_B - START_A) // 2
# Extra ticks after the read-off, to see whether the transfer is complete.
TAIL = 8
CHARGES = {"electron": -3, "positron": 3, "neutral": 0}


def family(name, charge, advance, slots, **extra):
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
        "kerengonen": {"phase_advance": advance},
    } | extra


def scalar(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


def coupling(name, receiver, other, sign_other):
    """The momentum table of `receiver` over the other ray's field: +1 repulsion
    when the field's source has the receiver's sign, -1 attraction otherwise."""
    return {
        "name": name,
        "participants": [{"type": receiver}, {"type": other}],
        "momentum_table": {other: sign_other},
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


def world(case, b, *, spread=True, shape=SHAPE, ticks=None):
    kinds = {
        "ee": ("electron", "electron"),
        "ep": ("electron", "positron"),
        "nn": ("neutral", "neutral"),
    }[case]
    charge_a, charge_b = CHARGES[kinds[0]], CHARGES[kinds[1]]
    ya, yb = CENTER_Y - b // 2, CENTER_Y + b // 2
    read_off = CLOSEST + 3 * b
    if ticks is None:
        ticks = min(read_off + TAIL, shape[0] - 1 - START_A)
    matter = ["electron_a", "electron_b"] if case != "nn" else ["neutral_a", "neutral_b"]
    fields = ["light_a", "light_b"]
    spread_key = {"spread": SPREAD} if spread else {}
    spatial = [
        family(matter[0], charge_a, 1, 2),
        family(matter[1], charge_b, 1, 2),
        family(fields[0], 0, 0, 30, field_of=matter[0], release=RELEASE, **spread_key),
        family(fields[1], 0, 0, 30, field_of=matter[1], release=RELEASE, **spread_key),
    ]
    rules = []
    if case != "nn":
        # Like signs repel (+1), opposite signs attract (-1): the sign the field ray
        # carries is its family's releaser's charge sign.
        sign = 1 if charge_a * charge_b > 0 else -1
        rules = [
            coupling("electron_field_turn_a", matter[0], fields[1], sign),
            coupling("electron_field_turn_b", matter[1], fields[0], sign),
        ]
    return {
        "schema_version": 1,
        "model_id": f"a5-coulomb-{case}-b{b}" + ("" if spread else "-nospread"),
        "shape": list(shape),
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
        "fields": [scalar(n) for n in matter + fields]
        + [
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            }
        ],
        "disturbance_types": [
            {
                "name": f"lamp_{tag}",
                "fields": [name, "momentum"],
                "defaults": {name: AMOUNT, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for tag, name in zip("ab", matter, strict=True)
        ],
        "spatial_fields": spatial,
        "emissions": [
            {
                "type": f"lamp_{tag}",
                "field": name,
                "amount": AMOUNT,
                "denominator": 1,
                "source": False,
                "heading": heading,
                "kerengonen_phase": 0,
                "recoil_field": "momentum",
            }
            for tag, name, heading in zip("ab", matter, ([1, 0, 0], [-1, 0, 0]), strict=True)
        ],
        "seeds": [
            {"position": [START_A, ya, CENTER_Z], "type": "lamp_a"},
            {"position": [START_B, yb, CENTER_Z], "type": "lamp_b"},
        ],
        "ray_interactions": rules,
    }


def cases():
    for case in ("ee", "ep"):
        for b in IMPACT_PARAMETERS:
            yield f"{case}_b{b}", world(case, b)
    yield "nn_b4", world("nn", 4)
    # The no-spread check (E6): without `spread` the field runs on the six axis
    # lines of its source and the transfer is one whole meeting, independent of b.
    for b in (4, 16):
        yield f"ee_b{b}_nospread", world("ee", b, spread=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in cases():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path, document["shape"], document["ticks"])


if __name__ == "__main__":
    main()
