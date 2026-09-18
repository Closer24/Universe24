"""Write the worlds of A5s repeated under the law of the bit (docs/EXPERIMENTS.md,
"A5s repeated under the law of the bit (2026-09-18)"): two things at rest,
each reading the other's shadows by its charge, the push per interval on
each, its scaling with the distance, the product law and the recoil through
the field.

Every world is written on the law as the engine of 2026-09-18 states it (see
`examples/nature/e11_law/make_worlds.py` for the settings shared with E11:
N = 64, K 1, `wait_per_quantum` 1, the dense mode, no retired key, the fill
12 the largest the prefill admits, the release [1, 512]). The two things are
external bodies of the catalog's `proton` family (charge +3 per quantum, the
whole charge 3 x amount declared on the body), each with the momentum table
`{"proton": 1}` read by charge (`reads` "charge", Highlights 5.4 point 16:
sign x amount x heading x (the owner's charge / the owner's content) x the
charge per quantum of what is pushed, 3 x 3 = 9 per shadow quantum here,
repulsion), each the home of its own shadows (a shadow of its own owner is
never a push) and each reading the other's. Their shadow sets are given with
the board by `initial_field` `{"fill": 12}`: a body of 2^28 releases 2^19 per
heading per interval of the fill, a set of 37748736; a body of 2^27 releases
2^18, a set of 18874368 (a body of 2^26, the first choice, is refused by the
prefill at fill 12, "a third phase on one Port of a source", so the second
content is 2^27). The body's momentum accumulates the pushes and steps a
Link when a whole amount has accumulated on an axis: at 2^28 and 2^27 no
body steps within 40 ticks at these pushes (of order 10^5 per interval,
measured before the run), so both stay at rest for the whole run.

The worlds (`ticks` 40 each, open boundary, a margin of 12 empty Nodes
beyond each body on every side; the fill's train reaches about 7 Links, so
nothing escapes during the fill):

- `pp_d{4,6,8,12}.json`: A and B of 2^28 on the x axis at distance d, B at
  (d, 0, 0) from A, the board [d + 25, 25, 25];
- `pp_d8_110.json`, `pp_d8_111.json`: B at (8, 8, 0) (r = 11.31) and at
  (8, 8, 8) (r = 13.86) from A, for the lattice's anisotropy;
- `pq_d8.json`, `qq_d8.json`: the product law at d = 8 on the axis, A of 2^28
  with B of 2^27, and both of 2^27, beside `pp_d8.json` (2^28 with 2^28):
  three pairs of contents, and of whole charges, 3 x 2^28 and 3 x 2^27;
- `pp_d{4,6,8,12}_closed.json`, `pp_d8_{110,111}_closed.json`, `pq_d8_closed.json`,
  `qq_d8_closed.json`: the eight worlds again on a closed board
  (`boundary` periodic, the same shape), the model owner's decision of
  2026-09-18 that the confrontation runs are made on a closed board, so
  that a thing's shadows circulate and its field at rest is a steady
  circulation and not a passing wave; 120 ticks with `standing_field` on,
  so the runner reports the shadow layer's fixed point or period, or the
  residual when there is none, and the pushes are read once the field has
  settled. The open-board worlds above are the control.

Run:  python examples/nature/a5s_law/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bit_law_migration import migrate  # noqa: E402

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
COSTS = ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
N = 64  # the one phase width of the world (Highlights 5.4, definitions; cleanup-law-v1)
K = 1
WAIT_PER_QUANTUM = 1
TICKS = 40
P = 1 << 28
Q = 1 << 27
PROTON_CHARGE = 3
ELECTRON_CHARGE = -3
RELEASE = [1, 512]
FILL = 12
MARGIN = 12
AXIS_DISTANCES = (4, 6, 8, 12)
# The proton family's slot budget: on a closed board the outgoing and the
# returning shares of two owners on six headings in two phases meet at one
# Node, more than the 24 of E11 (no rule couples the family here, so the
# layer cap of 32 does not apply).
SLOTS = 64
# The closed board (the model owner's decision of 2026-09-18, landing during
# these runs): `boundary` periodic, the same board, the shadows circulating,
# run three times as long with `standing_field` on so that the runner reports
# the layer's fixed point or period, or its residual.
CLOSED_TICKS = 120
OFF_AXIS = {"110": (8, 8, 0), "111": (8, 8, 8)}
PAIRS = {"pq": (P, Q), "qq": (Q, Q)}


def field(name, components=1):
    return {
        "name": name,
        "components": components,
        "units": "quantum" if components == 1 else "quantum times heading",
        "signed": components == 3,
        "conserved": True,
        "extensive": True,
    }


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
        "charge": charge,
    } | extra


def body(position, amount):
    return {
        "position": list(position),
        "family": "proton",
        "amount": amount,
        "charge": PROTON_CHARGE * amount,
        "momentum_table": {"proton": 1},
        "reads": "charge",
    }


def world(model_id, offset, amount_a, amount_b, *, closed=False):
    a = (MARGIN, MARGIN, MARGIN)
    b = tuple(a[k] + offset[k] for k in range(3))
    shape = [max(a[k], b[k]) + MARGIN + 1 for k in range(3)]
    return {
        "schema_version": 1,
        "model_id": model_id,
        "shape": shape,
        "boundary": "periodic" if closed else "open",
        "dense_field": True,
        **({"standing_field": True} if closed else {}),
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": CLOSED_TICKS if closed else TICKS,
        "operation_costs": dict.fromkeys(COSTS, 1),
        "N": N,
        "K": K,
        "wait_per_quantum": WAIT_PER_QUANTUM,
        "fields": [field("proton"), field("electron"), field("momentum", 3)],
        # No matter rays: one unseeded type of the electron family, never
        # emitted, since a world declares at least one type.
        "disturbance_types": [
            {
                "name": "idle",
                "fields": ["electron", "momentum"],
                "defaults": {"electron": 1, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            family("proton", PROTON_CHARGE, SLOTS, release=RELEASE),
            family("electron", ELECTRON_CHARGE, 8, clock=True),
        ],
        "emissions": [],
        "seeds": [],
        "ray_interactions": [],
        "external_bodies": [body(a, amount_a), body(b, amount_b)],
        "detectors": [],
        "initial_field": {"proton": {"fill": FILL}},
    }


def cases():
    for d in AXIS_DISTANCES:
        yield f"pp_d{d}", world(f"a5s-law-pp-d{d}", (d, 0, 0), P, P)
    for direction, offset in OFF_AXIS.items():
        yield f"pp_d8_{direction}", world(f"a5s-law-pp-d8-{direction}", offset, P, P)
    for tag, (amount_a, amount_b) in PAIRS.items():
        yield f"{tag}_d8", world(f"a5s-law-{tag}-d8", (8, 0, 0), amount_a, amount_b)
    for d in AXIS_DISTANCES:
        yield f"pp_d{d}_closed", world(f"a5s-law-pp-d{d}-closed", (d, 0, 0), P, P, closed=True)
    for direction, offset in OFF_AXIS.items():
        yield f"pp_d8_{direction}_closed", world(f"a5s-law-pp-d8-{direction}-closed", offset, P, P, closed=True)
    for tag, (amount_a, amount_b) in PAIRS.items():
        yield f"{tag}_d8_closed", world(f"a5s-law-{tag}-d8-closed", (8, 0, 0), amount_a, amount_b, closed=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in cases():
        assert migrate(json.loads(json.dumps(document))) == document
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path, document["shape"], document["ticks"], document["model_id"])


if __name__ == "__main__":
    main()
