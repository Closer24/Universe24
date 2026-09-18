"""Write the worlds of experiment E11 (docs/EXPERIMENTS.md), the field's books.

(b) `point_source.json`: one external body at the centre of a 49 x 49 x 49 open
board (external-body-v1), amount 2^20 with `release` [1, 256], so 4096 quanta of
its `light` leave on every heading every interval; the light spreads by the
catalog's table [6, 1, 1, 1, 1, 1] with the Node-owned remainder
(field-spreading-v1, field-remainder-v1) and carries the body's source sign;
`dense_field: true` (dense-field-v1); no mark, no second body, no matter ray.
The body's table names its own light with sign +1, as the control of A5s did,
so its register must stay (0, 0, 0) by symmetry and the ledger shows it. One
unseeded lamp of light with `recoil_field` momentum binds the momentum field to
the light (the engine's one way to bind it) so that the ledger carries the
momentum line. `profile.py` reads the shells.

(a) `books.json`: a source body A of the proton family (amount 2^20, charge +3,
`release` [1, 4096], so 256 quanta per heading per interval, the same light
family with `spread`) at the centre of a 21 x 21 x 21 open board, and one free
`electron` ray of amount 64 (charge -3, no field of its own: nothing declares
`field_of` electron) emitted by a lamp at x = 0 on the line parallel to x at
impact parameter b = 4 from A (y = 14, z = 10), heading +X. The coupling
`electron_field_turn` in its momentum-table form, `{"light": -1}`: attraction,
the electron pushed toward the source of every light ray it meets, each light
ray returned reversed as the recoil. Whatever reaches A ends in its sink and A's
`momentum_table` `{"light": -1}` books the recoil. 2 x 10 + 16 = 36 ticks (ten
Links from the entry to the closest approach). `dense_field: true`.

(a') `books_axis.json`: the same world without `spread` (the engine alone, which
the dense mode does not admit without a spreading family): A's field lives on
its six axis lines, the electron's line crosses A's +Y line at (10, 14, 10), and
the one field ray met there returns whole along that line to A, four Links.
This is the picture Highlights 3.5 draws in words; the spread world is the
catalog's rule. `books.py` reads both.

Run:  python examples/nature/e11_field_books/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bit_law_migration import migrate  # noqa: E402

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
SPREAD = [6, 1, 1, 1, 1, 1]
# The phase is read nowhere in these worlds (every release at phase 0, the
# push reads no phase), so the width is the reference Born width, 8 steps.
PHASE_BITS = 3
BODY_AMOUNT = 1 << 20
PROTON_CHARGE = 3
ELECTRON_CHARGE = -3

# (b) The point source: 4096 quanta per heading per interval on the 49^3 board,
# the shells k = 1 to 22 two Links inside the open boundary. The plan says 600
# ticks or the shells steady to 1 % over 32 ticks; the dense engine costs 1.45 s
# per tick on this board (12 us per Node and tick, the whole arrays every tick,
# measured before the run on the shared machine), so the budget of five minutes
# per world allows 192 ticks, six windows of 32, and the run is fixed at that.
PROFILE_SHAPE = [49, 49, 49]
PROFILE_CENTRE = [24, 24, 24]
PROFILE_RELEASE = [1, 256]
PROFILE_TICKS = 192

# (a) The books: 256 quanta per heading per interval, the electron at b = 4.
BOOKS_SHAPE = [21, 21, 21]
BOOKS_CENTRE = [10, 10, 10]
BOOKS_RELEASE = [1, 4096]
IMPACT_PARAMETER = 4
ELECTRON_AMOUNT = 64
ELECTRON_START = [0, BOOKS_CENTRE[1] + IMPACT_PARAMETER, BOOKS_CENTRE[2]]
BOOKS_TICKS = 2 * BOOKS_CENTRE[0] + 16
ELECTRON_SIGN = -1


def family(name, charge, advance=0, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
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


MOMENTUM = {
    "name": "momentum",
    "components": 3,
    "units": "quantum times heading",
    "signed": True,
    "conserved": True,
    "extensive": True,
}


def idle_lamp(field_name):
    """One unseeded lamp of a light family with `recoil_field` momentum: it
    binds the momentum field to the light so the ledger carries its momentum
    (a5_static's deviation (v)); nothing is emitted."""
    kind = {
        "name": f"idle_{field_name}",
        "fields": [field_name, "momentum"],
        "defaults": {field_name: 1, "momentum": [0, 0, 0]},
        "transport": {"mode": "hold"},
    }
    emission = {
        "type": f"idle_{field_name}",
        "field": field_name,
        "amount": 1,
        "denominator": 1,
        "source": False,
        "heading": [1, 0, 0],
        "kerengonen_phase": 0,
        "recoil_field": "momentum",
    }
    return kind, emission


def turn_rule(sign):
    """The catalog's electron_field_turn in its momentum-table form
    (ray-momentum-turn-v2): the electron pushed by sign x amount x heading of
    every light ray it meets, the light returned reversed."""
    return {
        "name": "electron_field_turn",
        "participants": [{"type": "electron"}, {"type": "light"}],
        "momentum_table": {"light": sign},
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


def base(model_id, shape, ticks, *, dense):
    return {
        "schema_version": 1,
        "model_id": model_id,
        "shape": list(shape),
        "boundary": "open",
        **({"dense_field": True} if dense else {}),
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
    }


def profile_world():
    return migrate(_profile_world())


def _profile_world():
    kind, emission = idle_lamp("light")
    return base("e11-point-source", PROFILE_SHAPE, PROFILE_TICKS, dense=True) | {
        "fields": [scalar("proton"), scalar("light"), MOMENTUM],
        "disturbance_types": [kind],
        "spatial_fields": [
            family("proton", PROTON_CHARGE),
            family("light", 0, field_of="proton", release=PROFILE_RELEASE, spread=SPREAD),
        ],
        "emissions": [emission],
        "seeds": [],
        "ray_interactions": [],
        "external_bodies": [
            {
                "position": list(PROFILE_CENTRE),
                "family": "proton",
                "amount": BODY_AMOUNT,
                "charge": PROTON_CHARGE,
                "momentum_table": {"light": 1},
            }
        ],
    }


def books_world(*, spread=True):
    return migrate(_books_world(spread=spread))


def _books_world(*, spread=True):
    kind, emission = idle_lamp("light")
    light_extra = {"field_of": "proton", "release": BOOKS_RELEASE}
    if spread:
        light_extra["spread"] = SPREAD
    tag = "books" if spread else "books-axis"
    return base(f"e11-{tag}", BOOKS_SHAPE, BOOKS_TICKS, dense=spread) | {
        "fields": [scalar("electron"), scalar("proton"), scalar("light"), MOMENTUM],
        "disturbance_types": [
            {
                "name": "electron_lamp",
                "fields": ["electron", "momentum"],
                "defaults": {"electron": ELECTRON_AMOUNT, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            kind,
        ],
        "spatial_fields": [
            family("electron", ELECTRON_CHARGE, advance=1),
            family("proton", PROTON_CHARGE),
            family("light", 0, **light_extra),
        ],
        "emissions": [
            {
                "type": "electron_lamp",
                "field": "electron",
                "amount": ELECTRON_AMOUNT,
                "denominator": 1,
                "source": False,
                "heading": [1, 0, 0],
                "kerengonen_phase": 0,
                "recoil_field": "momentum",
            },
            emission,
        ],
        "seeds": [{"position": list(ELECTRON_START), "type": "electron_lamp"}],
        "ray_interactions": [turn_rule(ELECTRON_SIGN)],
        "external_bodies": [
            {
                "position": list(BOOKS_CENTRE),
                "family": "proton",
                "amount": BODY_AMOUNT,
                "charge": PROTON_CHARGE,
                "momentum_table": {"light": ELECTRON_SIGN},
            }
        ],
    }


def cases():
    yield "point_source", profile_world()
    yield "books", books_world(spread=True)
    yield "books_axis", books_world(spread=False)


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
