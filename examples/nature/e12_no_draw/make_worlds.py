"""Write the worlds of experiment E12 (docs/EXPERIMENTS.md), the screen without a
draw: does a Detector need its draw at all, or is a mark at setting [1, 1] a
counter whose counts are the intensity?

Part 1, a counter against a drawn mark: the E9 world (`screen_loop.json`, the
ring of content 32 radiating on seven marks at x = 7, 240 ticks) with the marks
at setting [1, 1] (every arriving field quantum drawn 1: a counter), [1, 2] and
[1, 4] (a draw per arrival, the refused quanta returned on their lines), and the
counter again with another ticket seed (a draw at setting [1, 1] reads nothing
of its ticket, so the record must not change).

Part 2, interference in counts without a draw: two point sources of light, two
external bodies of one `proton` family at x = 1, 8 Links apart on the y axis,
radiating one `light` family (`field_of` proton, `release` [1, 4], `spread`,
the source sign +1 set by the engine from the charge), in phase (both at phase
0) and in antiphase (the second at phase 4, half the circle of N = 8), on a
line of 15 counters at x = 12; and the same two worlds with the catalog's
`born_steering` declared over `[light, light]`, so that light meets light in
one layer and the table steers the shared content between +Y and -Y by the
phase difference. Board 16 x 17 x 9, open; the marks at y = 1 to 15 and the
sources at y = 4 and 12, z = 4, so that the world is symmetric under
y -> 16 - y and no mark lies on a face (the plan's y = 0 to 14 shifted by one).
The two worlds without the coupling run 240 ticks; the two with it run 96,
because a coupling on field rays is not admitted by the dense mode and the
engine costs about 1.3 s per tick once the field fills this board (measured
on a 48-tick probe before the runs), so 240 ticks would take the engine
beyond the run budget; their counts are read against the first 96 ticks of
the plain worlds' records.

Run:  python examples/nature/e12_no_draw/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
OPERATIONS = ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
PHASE_BITS = 3
RELEASE = [1, 4]
SPREAD = [6, 1, 1, 1, 1, 1]
TICKS = 240
STEER_TICKS = 96

# ---- Part 1: E9's board (examples/nature/screen_loop.json) -------------------
SCREEN_SHAPE = [12, 11, 11]
# The unit square in the plane y = 5, edge-on to the screen (ring.json's lamps
# with Y read as Z): the R sense P0 -> P1 -> P2 -> P3 -> P0 (+X, +Z, -X, -Z) and
# the L sense P0 -> P3 -> P2 -> P1 -> P0 (+Z, +X, -Z, -X).
P0, P1, P2, P3 = (1, 5, 5), (2, 5, 5), (2, 5, 6), (1, 5, 6)
CORNERS = (P0, P1, P2, P3)
R_PORTS = (0, 4, 1, 5)
L_PORTS = (4, 1, 5, 0)
RING_AMOUNT = 4
RING_RATE = 1
ELECTRON_CHARGE = -3
MARKS = tuple((7, y, 5) for y in range(2, 9))
SCREEN_SETTINGS = {"d1": [1, 1], "d2": [1, 2], "d4": [1, 4]}
OTHER_SEED = 7

# ---- Part 2: two point sources on a line of counters --------------------------
FRINGE_SHAPE = [16, 17, 9]
SOURCE_X, SCREEN_X, PLANE_Z = 1, 12, 4
SOURCES = ((SOURCE_X, 4, PLANE_Z), (SOURCE_X, 12, PLANE_Z))
FRINGE_MARKS = tuple((SCREEN_X, y, PLANE_Z) for y in range(1, 16))
# The body's amount: floor(amount x 1 / 4) = 64 quanta per heading per interval.
SOURCE_AMOUNT = 256
SOURCE_CHARGE = 3
ANTIPHASE = 4

# bit-law-v1 (2026-09-18): the worlds are written in the law's form, migrated
# textually from the declaration below (see examples/nature/bit_law_migration.py).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bit_law_migration import migrate  # noqa: E402


def scalar(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


def ray_family(name, rate, charge, **extra):
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
        "kerengonen": {"phase_advance": rate},
        **extra,
    }


def frame(model_id, shape, ticks=TICKS):
    return {
        "schema_version": 1,
        "model_id": model_id,
        "shape": list(shape),
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {name: 1 for name in OPERATIONS},
    }


# ---- Part 1 -------------------------------------------------------------------


def lamps():
    """The corner lamps of E9: (position, name, Port), one per sense per corner."""
    result = []
    for k in range(4):
        result.append((CORNERS[k], f"corner_{k}_r", R_PORTS[k]))
        result.append((CORNERS[k], f"corner_{k}_l", L_PORTS[k]))
    return result


def corner_rule():
    """The Port form of the corner table (loop-binding-v1)."""
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


def screen_world(setting, seed, *, ticks=TICKS):
    """E9's world with the marks at `setting` and ticket seed `seed`."""
    n, d = setting
    return {
        **frame(f"e12-screen-d{d}" + (f"-seed{seed}" if seed else ""), SCREEN_SHAPE, ticks),
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
                "defaults": {"electron": RING_AMOUNT, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for _, name, _ in lamps()
        ],
        "spatial_fields": [
            ray_family("electron", RING_RATE, ELECTRON_CHARGE),
            ray_family("light", 0, 0, field_of="electron", release=RELEASE, spread=SPREAD),
        ],
        "emissions": [
            {
                "type": name,
                "field": "electron",
                "amount": RING_AMOUNT,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": HEADINGS[port],
                "kerengonen_phase": 0,
            }
            for _, name, port in lamps()
        ],
        "seeds": [{"position": list(position), "type": name} for position, name, _ in lamps()],
        "detectors": [{"position": list(mark), "setting": [n, d], "seed": seed} for mark in MARKS],
        "ray_interactions": [corner_rule()],
    }


# ---- Part 2 -------------------------------------------------------------------


def born_steering():
    """The catalog's `born_steering` (catalog/nature.json): two light rays of one
    layer, the shared content split between +Y (Port 2) and -Y (Port 3) in the
    ratio table[d] : 8 - table[d] for d their phase difference."""
    return {
        "name": "born_steering",
        "participants": [{"type": "light"}, {"type": "light"}],
        "outputs": [
            {
                "field": "light",
                "amount": {"of": "sum", "index": "phase_difference"},
                "heading": 2,
            },
            {"field": "light", "amount": {"rest_of": 0}, "heading": 3, "phase": {"of": 1}},
        ],
        "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
    }


def fringe_world(second_phase, steer, *, ticks=TICKS, amount=SOURCE_AMOUNT):
    """Two bodies of one `proton` family radiating one `light` family, the first at
    phase 0 and the second at `second_phase`, on fifteen counters; with `steer`
    the catalog's born_steering over [light, light]."""
    name = "antiphase" if second_phase else "inphase"
    return {
        **frame(f"e12-two-{name}" + ("-steer" if steer else ""), FRINGE_SHAPE, ticks),
        "fields": [scalar("proton"), scalar("light")],
        # One idle type so that the document declares an emission of the field
        # (as the A5s worlds do); nothing is seeded, the bodies alone radiate.
        "disturbance_types": [
            {
                "name": "idle_light",
                "fields": ["light"],
                "defaults": {"light": 1},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            ray_family("proton", 0, SOURCE_CHARGE),
            ray_family("light", 0, 0, field_of="proton", release=RELEASE, spread=SPREAD),
        ],
        "emissions": [
            {
                "type": "idle_light",
                "field": "light",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "heading": [1, 0, 0],
                "kerengonen_phase": 0,
            }
        ],
        "seeds": [],
        "detectors": [{"position": list(mark), "setting": [1, 1], "seed": 0} for mark in FRINGE_MARKS],
        "ray_interactions": [born_steering()] if steer else [],
        "external_bodies": [
            {
                "position": list(position),
                "family": "proton",
                "amount": amount,
                "charge": SOURCE_CHARGE,
                "phase": phase,
            }
            for position, phase in zip(SOURCES, (0, second_phase), strict=True)
        ],
    }


# ---- The isolated test's board ---------------------------------------------
TEST_SHAPE = [10, 9, 9]
TEST_SOURCE = (1, 4, 4)
TEST_MARKS = tuple((7, y, 4) for y in range(2, 7))
TEST_AMOUNT = 64
TEST_TICKS = 24


def counter_world(seed=0, *, ticks=TEST_TICKS):
    """The smallest world of the question, for `tests/test_screen_no_draw.py` and
    not written to disk: one body of the `proton` family (16 quanta per heading
    per interval) on a 10 x 9 x 9 open board, five counters at distance 6 on the
    line x = 7, the marks' ticket seed `seed`."""
    world = fringe_world(0, False, ticks=ticks, amount=TEST_AMOUNT)
    world["model_id"] = "e12-counter-test" + (f"-seed{seed}" if seed else "")
    world["shape"] = list(TEST_SHAPE)
    world["detectors"] = [
        {"position": list(mark), "setting": [1, 1], "seed": seed} for mark in TEST_MARKS
    ]
    world["external_bodies"] = world["external_bodies"][:1]
    world["external_bodies"][0]["position"] = list(TEST_SOURCE)
    return world


def cases():
    for name, document in _cases():
        yield name, migrate(document)


def _cases():
    for key, setting in SCREEN_SETTINGS.items():
        yield f"screen_{key}", screen_world(setting, 0)
    yield f"screen_d1_seed{OTHER_SEED}", screen_world([1, 1], OTHER_SEED)
    for steer in (False, True):
        for second_phase in (0, ANTIPHASE):
            name = "antiphase" if second_phase else "inphase"
            yield (
                f"two_{name}" + ("_steer" if steer else ""),
                fringe_world(second_phase, steer, ticks=STEER_TICKS if steer else TICKS),
            )


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
