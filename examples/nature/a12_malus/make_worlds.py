"""Write the worlds of experiment A12 (docs/EXPERIMENTS.md), Malus's law and the
three-polarizer chain: a marked source of light polarized along +Y sends a beam
of pulses along +X through one polarizer, or a chain of them, to a marked Node
behind the last one, every polarizer an external body under the polarizer
coupling (external-body-v1 with ray-polarization-v1, Highlights 3.19 and 3.26):
the arriving content is split by the declared table at the difference between
the body's angle and the ray's polarization, the pass share leaving on +X with
the body's angle as its polarization, the rest ending in the body's sink and the
shares below one quantum owned by the body's registers until they reach one.

The table is cos^2(theta) in N-ths, rounded, at N = 2^8 = 256 steps per half
turn (the catalog's `phase_bits` default, and the polarization circle of light
by default): entry d is round(256 cos^2(d x 180 / 256 degrees)); 22.5, 45, 67.5
and 90 degrees are the steps 32, 64, 96 and 128 exactly. The source declares
`polarization` 0, the first transverse lattice axis of +X, which is +Y.

Eight worlds: `single_{0,22,45,67,90}` (one polarizer at 0, 22.5, 45, 67.5 and
90 degrees), `chain_90` (y, 90), `chain_45_90` (y, 45, 90) and
`chain_22_45_67_90` (y, 22.5, 45, 67.5, 90). Light declares no `spread`: a
polarizer confrontation needs a beam, and this run's deviation from "the field
spreads" is stated in the register's entry.

Run:  python examples/nature/a12_malus/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# The phase width and, by default, the polarization circle: 256 steps per half
# turn, the catalog's default (`phase_bits` 8); the table is in 256-ths.
PHASE_BITS = 8
STEPS = 1 << PHASE_BITS
# The source: one pulse of AMOUNT quanta per interval for PULSES intervals, at
# phase 0, polarized along +Y (step 0), on +X from the marked Node at x = 2.
AMOUNT = 256
PULSES = 8
SOURCE_X = 2
# The polarizers, in beam order, ten Links apart; the marked Node behind the last
# one at x = 52; the open boundary at x = 64 lets the passed content escape.
POLARIZER_X = (12, 22, 32, 42)
MARK_X = 52
SHAPE = [65, 9, 9]
AXIS = 4
# Ticks: the last pulse leaves the source in the cycle of tick 7 and escapes
# through the open face at x = 64 at tick 69; 72 ticks end the run with every
# quantum clicked, sunk, held or escaped.
TICKS = 72
ANGLES = {"0": 0, "22": 32, "45": 64, "67": 96, "90": 128}


def polarizer_table(steps: int = STEPS) -> list[int]:
    """cos^2 of d half-turns over `steps`, in steps-ths, rounded to the nearest
    integer (no entry is a half-integer: cos^2 of a rational multiple of pi is
    rational only at 0, 1/4, 1/2, 3/4 and 1)."""
    return [round(steps * math.cos(math.pi * d / steps) ** 2) for d in range(steps)]


def scalar(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


def family(name):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": PHASE_BITS,
        "charge": 0,
        "kerengonen": {"phase_advance": 0},
    }


def polarizer(x, angle, table):
    return {
        "position": [x, AXIS, AXIS],
        "family": "apparatus",
        "amount": 1,
        "coupling": "polarizer",
        "polarizer": {"family": "light", "angle": angle, "pass": [1, 0, 0], "table": table},
    }


def world(tag, angles):
    table = polarizer_table()
    return {
        "schema_version": 1,
        "model_id": f"a12-malus-{tag.replace('_', '-')}",
        "shape": SHAPE,
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": TICKS,
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
        "fields": [scalar("light"), scalar("apparatus")],
        # The source: a lamp holding PULSES x AMOUNT that emits AMOUNT per interval,
        # funded from its own stock, on a marked Node (a source is a Detector).
        "disturbance_types": [
            {
                "name": "source",
                "fields": ["light"],
                "defaults": {"light": AMOUNT * PULSES},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [family("light"), family("apparatus")],
        "emissions": [
            {
                "type": "source",
                "field": "light",
                "amount": AMOUNT,
                "denominator": 1,
                "source": False,
                "heading": [1, 0, 0],
                "kerengonen_phase": 0,
                "polarization": 0,
            }
        ],
        "seeds": [{"position": [SOURCE_X, AXIS, AXIS], "type": "source"}],
        "detectors": [
            {"position": [SOURCE_X, AXIS, AXIS], "setting": [1, 1], "seed": 0},
            {"position": [MARK_X, AXIS, AXIS], "setting": [1, 1], "seed": 0},
        ],
        "ray_interactions": [],
        "external_bodies": [
            polarizer(x, angle, table) for x, angle in zip(POLARIZER_X, angles, strict=False)
        ],
    }


def cases():
    for name, angle in ANGLES.items():
        yield f"single_{name}", world(f"single_{name}", [angle])
    yield "chain_90", world("chain_90", [ANGLES["90"]])
    yield "chain_45_90", world("chain_45_90", [ANGLES["45"], ANGLES["90"]])
    yield (
        "chain_22_45_67_90",
        world("chain_22_45_67_90", [ANGLES["22"], ANGLES["45"], ANGLES["67"], ANGLES["90"]]),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in cases():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path, [body["polarizer"]["angle"] for body in document["external_bodies"]])


if __name__ == "__main__":
    main()
