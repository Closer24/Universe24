"""Write the worlds of experiment A5s (docs/EXPERIMENTS.md): two external bodies at
rest (external-body-v1), each radiating its light (field_of, release) which spreads
by the catalog's table [6, 1, 1, 1, 1, 1] with the Node-owned remainder
(field-spreading-v1, field-remainder-v1), each absorbing the other's light in its
sink with a `momentum_table` whose sign is the charge product: +1 (repulsion) for
like charges, -1 (attraction) for opposite charges. The force is the change of each
body's momentum register per interval, read from the `external_body_absorbed`
records; no matter rays, no Detector.

The engine names one light family per releaser (catalog, `light`), so each body's
family is its own (`proton_a`, `proton_b` or `electron_b`) and its light is its own
family (`light_a`, `light_b`); the sign of the source travels on the ray as
`source_sign`, set by the engine from the body's declared charge, and a body's
`momentum_table` reads no sign, so the table names the other body's light with the
sign of the charge product, written before the run.

Run 2 (the entry's "Run 2, to the steady state (dense mode)"): the same bodies
under the dense mode (`dense_field: true`, dense-field-v1, the pure-field Nodes
cycled as one vectorized step with the same integers) with the boundary 2r from
both, the box [5r + 1, 4r + 1, 4r + 1], run to the steady state, t90 + 32 ticks
by the mean field's t90 in that box (predict_dense.py, its numbers in
predictions.json beside the worlds): like charges at r = 12, 16, 20 and 24,
opposite charges at r = 16, and the control alone in the cube of r = 16's margin
for r = 16's ticks (`pp_r{r}d`, `pe_r16d`, `p_alone_16d`).

Run:  python examples/nature/a5_static/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bit_law_migration import migrate  # noqa: E402

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
AXIS_DISTANCES = (4, 6, 8, 12, 16)
DIAGONAL_DISTANCES = (3, 4, 6, 8)
# The body's amount and its light's release: 2^28 x 1 / 65536 = 4096 quanta per
# heading per interval. The amount enters no sum but the body's motion: its axis
# accumulator adds the momentum register every interval and steps a Link at a
# whole amount, so at a push of order 750 per interval (r = 4) an amount of 2^20
# would step the body after about 53 intervals (F t^2 / 2 > 2^20); 2^28 keeps both
# bodies at rest for the whole run.
AMOUNT = 1 << 28
RELEASE = [1, 65536]
SPREAD = [6, 1, 1, 1, 1, 1]
# The phase is read nowhere in these worlds (no meeting, every release at phase 0),
# and the coherent sum of a spread costs one pass over the circle per register, so
# the width is the reference Born width, 8 steps.
PHASE_BITS = 3
# The margin of empty Nodes beyond each body on every side (open boundary): the
# entry plans at least 8; the engine's cost, 2.3 ms per Node cycle with every Node
# of the board cycling once the field fills it, allows 5 within about eight
# minutes per world (the mean-field estimate of what the box costs is in the
# entry).
MARGIN = 5
# Ticks: 2r + 32, r the Manhattan distance (the entry plans 2r + 64; the same
# cost); the push is read as the mean per interval over the last 32 ticks, and
# the per-tick series shows the transient.
EXTRA_TICKS = 32
CONTROL_TICKS = 64
CHARGES = {"proton": 3, "electron": -3}
# Run 2, the dense mode: the boundary 2r from both bodies (the mean-field entry's
# box) and t90 + 32 ticks, t90 the first tick at which the mean field's push in
# that box reaches 90 % of its steady state (predict_dense.py; predictions.json
# holds the computation, and the test checks these against it): 164, 354, 590
# and 866 at r = 12, 16, 20, 24. The control alone sits in the cube of r = 16's
# margin for r = 16's ticks.
DENSE_DISTANCES = (12, 16, 20, 24)
DENSE_TICKS = {12: 196, 16: 386, 20: 622, 24: 898}
DENSE_OPPOSITE_DISTANCE = 16
DENSE_CONTROL_DISTANCE = 16


def family(name, charge, slots, **extra):
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
        "kerengonen": {"phase_advance": 0},
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


def body(position, name, charge, table):
    return {
        "position": list(position),
        "family": name,
        "amount": AMOUNT,
        "charge": charge,
        "momentum_table": table,
    }


def world(case, offset, *, margin=MARGIN, ticks=None, dense=False):
    tag, document = _world(case, offset, margin=margin, ticks=ticks, dense=dense)
    return tag, migrate(document)


def _world(case, offset, *, margin=MARGIN, ticks=None, dense=False):
    """`case`: pp (proton, proton), pe (proton, electron) or p (the control, one
    body); `offset`: the position of B relative to A, (r, 0, 0) on the axis or
    (d, d, 0) on the diagonal; (0, 0, 0) for the control. `dense`: the world of
    Run 2, `dense_field: true` and the tag with a `d` (the control's tag names
    the r whose margin it takes, `p_alone_16d`)."""
    kinds = {"pp": ("proton", "proton"), "pe": ("proton", "electron"), "p": ("proton", None)}[case]
    manhattan = sum(abs(c) for c in offset)
    if ticks is None:
        ticks = 2 * manhattan + EXTRA_TICKS if manhattan else CONTROL_TICKS
    a = (margin, margin, margin)
    b = tuple(a[k] + offset[k] for k in range(3))
    shape = [max(a[k], b[k]) + margin + 1 for k in range(3)]
    name_a = f"{kinds[0]}_a"
    charge_a = CHARGES[kinds[0]]
    matter = [name_a]
    fields = ["light_a"]
    bodies = []
    spatial = [family(name_a, charge_a, 2)]
    if kinds[1] is None:
        # The control: one body alone, its table naming its own light, whose
        # backward spread returns to it from all sides.
        bodies.append(body(a, name_a, charge_a, {"light_a": 1}))
        tag = f"p_alone_{margin // 2}d" if dense else "p_alone"
    else:
        name_b = f"{kinds[1]}_b"
        charge_b = CHARGES[kinds[1]]
        matter.append(name_b)
        fields.append("light_b")
        spatial.append(family(name_b, charge_b, 2))
        sign = 1 if charge_a * charge_b > 0 else -1
        bodies.append(body(a, name_a, charge_a, {"light_b": sign}))
        bodies.append(body(b, name_b, charge_b, {"light_a": sign}))
        axis = offset[1] == 0
        tag = f"{case}_{'r' if axis else 'd'}{offset[0]}{'d' if dense else ''}"
    for matter_name, field_name in zip(matter, fields, strict=True):
        spatial.append(family(field_name, 0, 8, field_of=matter_name, release=RELEASE, spread=SPREAD))
    return tag, {
        "schema_version": 1,
        "model_id": f"a5-static-{tag.replace('_', '-')}",
        "shape": shape,
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
        # No matter rays: one unseeded lamp per light family binds the momentum
        # field to the light (an emission's recoil_field is the engine's one way to
        # bind it), so that the ledger carries the momentum line; nothing is emitted.
        "disturbance_types": [
            {
                "name": f"idle_{field_name}",
                "fields": [field_name, "momentum"],
                "defaults": {field_name: 1, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for field_name in fields
        ],
        "spatial_fields": spatial,
        "emissions": [
            {
                "type": f"idle_{field_name}",
                "field": field_name,
                "amount": 1,
                "denominator": 1,
                "source": False,
                "heading": [1, 0, 0],
                "kerengonen_phase": 0,
                "recoil_field": "momentum",
            }
            for field_name in fields
        ],
        "seeds": [],
        "ray_interactions": [],
        "external_bodies": bodies,
    }


def cases():
    for case in ("pp", "pe"):
        for r in AXIS_DISTANCES:
            yield world(case, (r, 0, 0))
    for d in DIAGONAL_DISTANCES:
        yield world("pp", (d, d, 0))
    yield world("p", (0, 0, 0))


def dense_cases():
    """The worlds of Run 2: like charges at every dense r, opposite charges at
    r = 16, the control in r = 16's cube for r = 16's ticks."""
    for r in DENSE_DISTANCES:
        yield world("pp", (r, 0, 0), margin=2 * r, ticks=DENSE_TICKS[r], dense=True)
    r = DENSE_OPPOSITE_DISTANCE
    yield world("pe", (r, 0, 0), margin=2 * r, ticks=DENSE_TICKS[r], dense=True)
    r = DENSE_CONTROL_DISTANCE
    yield world("p", (0, 0, 0), margin=2 * r, ticks=DENSE_TICKS[r], dense=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in (*cases(), *dense_cases()):
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path, document["shape"], document["ticks"])


if __name__ == "__main__":
    main()
