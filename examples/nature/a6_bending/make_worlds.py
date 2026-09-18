"""Write the worlds of experiment A6 (docs/EXPERIMENTS.md, "Light bending by a bound
group and G_eff N^2 over N = 2^8 to 2^16"): a star, an external body at rest
(external-body-v1) of the catalog's neutron family, radiating its mass field
(`mass_field`, `field_of` neutron, `release`), which spreads by the catalog's table
[6, 1, 1, 1, 1, 1] with the Node-owned remainder (field-spreading-v1,
field-remainder-v1) and fills the board under the dense mode (dense-field-v1);
one light ray launched along +x at impact parameter b past the star; the coupling
of the light with the mass field in one form, its own series of worlds:

- `turn`: the form A6's status names for the deflection "measured as a momentum
  register" (ray-momentum-turn-v2, feature 8b): a `momentum_table` rule pushing
  the light's momentum register by -amount x heading of every mass-field ray it
  meets, each returned reversed.

The `delay` form (the catalog's `mass_field_delay` of ray-binding-v1, a lag of
the light's face clock by a declared table) was deleted with the lag in the
cleanup of 2026-09-18 (Highlights 5.4, points 16, 21 and 22); its records stay
as dated evidence in docs/EXPERIMENTS.md.

The launch: the light waits at a launcher body at the start of its line (a
declared coupling of the body, the light's output on Port +X with an integer
`delay`, LAUNCH_DELAY intervals) so that it passes the star in a field that has
filled the board; the lamp one Node below the launcher emits it at tick 0 on +Y.

The series (one world per case and form, `{form}_{case}.json`): the axis series
b = 4, 6, 8, 12, 16 at N = 2^12 (`b4` .. `b16`), the control without the star
(`control`), the star at twice the amount (`2m`), the slow massive ray, an
electron of rest rate 1 with the light's content (`slow`), the N scan at b = 8
(`n8`, `n10`, the world's `N`; `n14` and `n16` deleted with the bound N <= 4096), the other side of the star
(`m4` .. `m16`, b = -4 .. -16), all on the register's board of 65 x 65 x 9 Nodes;
and, on a cube of 49 x 33 x 33 that holds the (0, 1, 1) diagonal passes, the axis
passes b = 4, 6, 8 (`c_b4`, `c_b6`, `c_b8`) and the diagonal passes at (0, d, d),
d = 3, 4, 6 (`c_d3`, `c_d4`, `c_d6`; Euclidean b = 4.24, 5.66, 8.49).
`small_world` is the 25 x 25 x 9 board of the isolated test.

Run:  python examples/nature/a6_bending/make_worlds.py [--out DIR]
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
FORMS = ("turn",)
# The register's board: 65 x 65 x 9, the star at its center, open boundary; the
# cube for the diagonal passes, the star at its center.
SLAB = [65, 65, 9]
SLAB_STAR = (32, 32, 4)
CUBE = [49, 33, 33]
CUBE_STAR = (24, 16, 16)
AXIS_B = (4, 6, 8, 12, 16)
SCAN_B = 8
BASE_BITS = 12
# The N scan stops at N = 4096 (12 bits, the base): N is one for the world and a
# power of two up to 4096 since the cleanup of 2026-09-18 (the definitions of the
# law); the n14 and n16 worlds of the first series are deleted.
SCAN_BITS = (8, 10)
CUBE_AXIS_B = (4, 6, 8)
CUBE_DIAGONAL_D = (3, 4, 6)
# The light's amount (its momentum register's scale, 2^18: the register reads the
# deflection to one part in 2^18 and the DDA completes no transverse Link over the
# pass), the star's amount and its field's release: 2^28 x 1 / 2^15 = 8192 quanta
# per heading per interval (the amount enters no sum but the body's motion, an
# accumulator that steps a Link at a whole amount: with 2^28 the star stays for
# the whole run under the recoils of the pass); 2M is 2^29 at the same release.
LIGHT = 1 << 18
AMOUNT = 1 << 28
RELEASE = [1, 1 << 15]
# The spreading family's phase width (read nowhere in these worlds: every release
# at phase 0, the coherent sum of a spread costs one pass over the circle per
# register), the reference Born width; the light's width is the case's N.
FIELD_BITS = 3
# The launch: the light leaves the launcher at tick LAUNCH_DELAY + 1 and is at
# x = k at tick LAUNCH_DELAY + 1 + k; it escapes the 65-board at tick
# LAUNCH_DELAY + 66 and the world runs two ticks more.
LAUNCH_DELAY = 192
EXTRA_TICKS = 68
SLOW_RATE = 1
SLOW_CHARGE = -3


def family(name, rate, bits, slots, charge=0, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": slots,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": bits,
        "charge": charge,
        "kerengonen": {"phase_advance": rate},
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


def launch_rule(ray, delay):
    """The launcher body's coupling: the arriving ray leaves on Port +X after
    `delay` intervals at the launcher's Node; the body is returned unchanged."""
    return {
        "name": "launch",
        "participants": [{"type": ray}, {"type": "launcher"}],
        "outputs": [
            {
                "field": ray,
                "amount": {"of": 0},
                "heading": 0,
                "phase": "same",
                "delay": delay,
                "input": 0,
            },
            {"field": "launcher", "amount": {"of": 1}, "heading": "same", "phase": "same", "input": 1},
        ],
        "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
    }


def gravity_rule(form, ray):
    if form == "turn":
        return {
            "name": "mass_field_turn",
            "participants": [{"type": ray}, {"type": "mass_field"}],
            "momentum_table": {"mass_field": -1},
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
    raise ValueError(form)


def world(*args, **kwargs):
    return migrate(_world(*args, **kwargs))


def _world(
    form,
    name,
    *,
    shape=SLAB,
    star=SLAB_STAR,
    offset=(0, 0, 0),
    bits=BASE_BITS,
    amount=AMOUNT,
    star_on=True,
    ray="light",
    launch_delay=LAUNCH_DELAY,
    ticks=None,
):
    """One world: the star at `star` (absent when `star_on` is false), the ray's line
    parallel to x through star + offset (offset (0, b, 0) on the axis, (0, d, d) on
    the diagonal), the launcher at x = 0 on that line and the lamp one Node below
    it; `ray` is `light` or `electron` (the slow ray); `bits` the ray's phase
    width, N = 2^bits."""
    if ticks is None:
        ticks = launch_delay + EXTRA_TICKS
    y, z = star[1] + offset[1], star[2] + offset[2]
    launcher = [0, y, z]
    lamp = [0, y - 1, z]
    fields = [scalar("neutron"), scalar("mass_field"), scalar("light"), scalar("launcher")]
    spatial = [
        family("neutron", 1, FIELD_BITS, 2),
        family(
            "mass_field", 0, FIELD_BITS, 16, field_of="neutron", release=list(RELEASE), spread=SPREAD
        ),
        family("light", 0, bits, 8),
        family("launcher", 0, FIELD_BITS, 2),
    ]
    if ray == "electron":
        fields.append(scalar("electron"))
        spatial.append(family("electron", SLOW_RATE, bits, 8, charge=SLOW_CHARGE))
    fields.append(
        {
            "name": "momentum",
            "components": 3,
            "units": "quantum times heading",
            "signed": True,
            "conserved": True,
            "extensive": True,
        }
    )
    bodies = [{"position": launcher, "family": "launcher", "amount": 1, "coupling": "launch"}]
    if star_on:
        bodies.insert(
            0,
            {
                "position": list(star),
                "family": "neutron",
                "amount": amount,
                "momentum_table": {"mass_field": -1},
            },
        )
    return {
        "schema_version": 1,
        "model_id": f"a6-bending-{name.replace('_', '-')}",
        "shape": list(shape),
        "boundary": "open",
        "dense_field": True,
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {
            name_: 1
            for name_ in (
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
        "fields": fields,
        # The lamp holds the ray's content and emits it at tick 0 on +Y toward the
        # launcher; the unseeded lamp of the mass field binds the momentum field to
        # it (an emission's recoil_field is the engine's one way to bind it), so
        # that the ledger carries the momentum line for both families.
        "disturbance_types": [
            {
                "name": "lamp",
                "fields": [ray, "momentum"],
                "defaults": {ray: LIGHT, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "idle_mass_field",
                "fields": ["mass_field", "momentum"],
                "defaults": {"mass_field": 1, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": spatial,
        "emissions": [
            {
                "type": "lamp",
                "field": ray,
                "amount": LIGHT,
                "denominator": 1,
                "source": False,
                "heading": [0, 1, 0],
                "kerengonen_phase": 0,
                "recoil_field": "momentum",
            },
            {
                "type": "idle_mass_field",
                "field": "mass_field",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "heading": [1, 0, 0],
                "kerengonen_phase": 0,
                "recoil_field": "momentum",
            },
        ],
        "seeds": [{"position": lamp, "type": "lamp"}],
        "ray_interactions": [launch_rule(ray, launch_delay), gravity_rule(form, ray)],
        "external_bodies": bodies,
    }


def cases(form):
    """The worlds of one form, in the order they are run."""
    for b in AXIS_B:
        yield f"{form}_b{b}", world(form, f"{form}_b{b}", offset=(0, b, 0))
    yield f"{form}_control", world(form, f"{form}_control", offset=(0, SCAN_B, 0), star_on=False)
    yield f"{form}_2m", world(form, f"{form}_2m", offset=(0, SCAN_B, 0), amount=2 * AMOUNT)
    yield f"{form}_slow", world(form, f"{form}_slow", offset=(0, SCAN_B, 0), ray="electron")
    for bits in SCAN_BITS:
        yield f"{form}_n{bits}", world(form, f"{form}_n{bits}", offset=(0, SCAN_B, 0), bits=bits)
    for b in AXIS_B:
        yield f"{form}_m{b}", world(form, f"{form}_m{b}", offset=(0, -b, 0))
    for b in CUBE_AXIS_B:
        yield (
            f"{form}_c_b{b}",
            world(form, f"{form}_c_b{b}", shape=CUBE, star=CUBE_STAR, offset=(0, b, 0)),
        )
    for d in CUBE_DIAGONAL_D:
        yield (
            f"{form}_c_d{d}",
            world(form, f"{form}_c_d{d}", shape=CUBE, star=CUBE_STAR, offset=(0, d, d)),
        )


def all_cases():
    for form in FORMS:
        yield from cases(form)


def small_world(form):
    """The isolated test's world: a 25 x 25 x 9 board, the star at (12, 12, 4), b = 4,
    the launch after 10 intervals, 40 ticks; everything else the series'."""
    return world(
        form,
        f"small_{form}",
        shape=[25, 25, 9],
        star=(12, 12, 4),
        offset=(0, 4, 0),
        launch_delay=10,
        ticks=40,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in all_cases():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path, document["shape"], document["ticks"])


if __name__ == "__main__":
    main()
