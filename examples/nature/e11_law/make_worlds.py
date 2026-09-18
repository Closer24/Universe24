"""Write the worlds of E11 repeated under the law of the bit (docs/EXPERIMENTS.md,
"E11 repeated under the law of the bit (2026-09-18)"): one thing at rest and its
field, given with the board and read shell by shell, with test things that read
it at three radii on an axis, on (110) and on (111).

Every world is written on the law as the engine of 2026-09-18 states it
(bit-law-v1, node-mixing-v1, clock-readings-v1, node-is-ports-v1, lanes-v1,
return-field-v1, cleanup-law-v1): N = 64 declared once for the world (the
per-family `phase_bits` is retired), one K for the world (1: a thing of one quantum
advances one step per interval), `wait_per_quantum` 1, the dense mode, no
`spread`, `steering`, `mass_field` or `seed` key, no `field_of`, no release
during the run. The thing at rest is an external body of the catalog's
`proton` family (charge +3 per quantum, so the body of 2^28 declares the whole
charge 3 x 2^28 = 805306368, the largest such charge below the bounded
integer's 2^30 - 1 at a power of two), whose shadows are given with the board
by `initial_field` `{"fill": 12}` with `release` [1, 512]: the body releases
2^19 = 524288 quanta per Port heading per interval of the fill, so its shadow
set is 6 x 2^19 x 12 = 37748736 quanta (nothing escapes during the fill: the
train reaches about 12 / sqrt 3 = 7 Links). The fill is 12 because the prefill
admits no longer one: at 13 intervals a third phase arrives back at the source
on one Port and the prefill's two phase layers per Port refuse it
(`event_universe/prefill.py`), at every release amount tried (4096 to 2^18
per heading); 12 is the largest lawful fill. The release amount 2^19 is chosen
so that every Node of the board holds far more than 256 quanta of the body's
shadows through the run (the receiver's condition of DERIVATIONS.md section
30): about 20000 per Node at r = 4 to 8 while the train passes and a haze of
about 700 per Node at tick 30, measured before the run on a 25^3 board at
half the amount.

The worlds (`ticks` 40 each, open boundary):

- `pulse.json`: the body at the centre of a 41^3 board with `fill` 1, that is
  one release of 2^19 on each of the six headings and nothing else, X =
  3145728: the front's arrival tick per direction and the fraction of the
  release off the coordinate planes at t = 30 (DERIVATIONS.md section 27
  (ii) and (iii)); the board is wider so that the front, at t / sqrt 3 =
  17.3 at t = 30, is still on it.
- `standing.json`: the body at the centre of a 33^3 board (r = 16) with
  `fill` 12 and no test thing: the field read shell by shell per interval by
  `analyze.py` in-process (the content per Node, the signed radial flux J_r
  per shell, the content and J at the nine Nodes of the test things below),
  and the books per bit.
- `standing_closed.json`: the standing world on a closed board (`boundary`
  periodic, the model owner's decision of 2026-09-18 that the confrontation
  runs are made on a closed board, the shadows circulating), 120 ticks with
  `standing_field` on so that the runner reports the layer's fixed point or
  period, or its residual; the shells are read at the settled state, the
  open board above being the control.
- `probe_axis_r{4,8,12}.json`, `probe_110_m{3,6,9}.json` (the Node (m, m, 0)
  from the body, r = 4.24, 8.49, 12.73), `probe_111_m{2,5,7}.json` ((m, m, m),
  r = 3.46, 8.66, 12.12): the standing world with one test thing each, a real
  ray of the catalog's `electron` family (charge -3, `clock`) of content 1,
  emitted by a lamp that holds exactly that one quantum, one Link outward of
  the read Node and heading inward, so that it stands at the read Node after
  tick 1 and reads the field there from the cycle of tick 2. Its coupling
  `read` over [electron, proton] is a momentum table `{"proton": 1}` with
  `reads` "content": the push is +1 x amount x heading x 1 per shadow, the
  signed flux J of the body's shadows at its Node in quanta, so the test
  thing's momentum line is the pushed amount itself (the electricity reading
  would multiply every push by (3 x 2^28 / 2^28) x (-3) = -9 and change
  nothing else). A thing pays a tick per whole quantum it reads (point 23),
  so a test thing that reads thousands of quanta never moves again: it is a
  probe at rest at its Node, and its momentum line per tick is the field's
  push per interval. It heads inward because the engine takes a share that
  arrives through the Port the thing arrived by as riding with it (one
  meeting, one push, return-field-v1): a probe heading inward ignores the
  inward-moving arrivals on its own lane, the wave's small backward share,
  and reads the outgoing wave whole; `analyze.py` reports the inventory's J
  at the same Node in `standing.json` beside every probe's reading.
  One probe per world, because every push returns as field (point 3) and a
  probe's returns would pollute another probe's reading on the same line.
- `probe_*_closed.json`: the nine probe worlds again on the closed board
  (`boundary` periodic, 120 ticks, `standing_field` on, as `standing_closed`):
  the pushed amount per interval at the test thing's Node once the field has
  settled, and the amplitude at its Node (the size of the coherent sum of the
  arriving shadows, `arrival_amplitude` of wait-reads-v1, formed by
  `analyze.py` from the arrivals of the replay exactly as the engine forms it;
  no world declares `wait_reads`, so the closed probes differ from the open
  ones by the boundary, the ticks and the standing-set search alone).

Run:  python examples/nature/e11_law/make_worlds.py [--out DIR]
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
BODY_AMOUNT = 1 << 28
PROTON_CHARGE = 3
ELECTRON_CHARGE = -3
RELEASE = [1, 512]
FILL = 12
HALF = 16  # the board 33^3
PULSE_HALF = 20  # the pulse board 41^3
# The closed board (the model owner's decision of 2026-09-18, landing during
# these runs): the standing world again with `boundary` periodic and
# `standing_field` on, three times as long, the shells read at the settled state.
CLOSED_TICKS = 120
PROBE_CONTENT = 1
# The read Nodes relative to the body and the probe's inward heading.
PROBES = {
    "axis": ([(4, 0, 0), (8, 0, 0), (12, 0, 0)], (-1, 0, 0), "r"),
    "110": ([(3, 3, 0), (6, 6, 0), (9, 9, 0)], (-1, 0, 0), "m"),
    "111": ([(2, 2, 2), (5, 5, 5), (7, 7, 7)], (0, 0, -1), "m"),
}


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


def body(position, amount=BODY_AMOUNT):
    return {
        "position": list(position),
        "family": "proton",
        "amount": amount,
        "charge": PROTON_CHARGE * amount,
    }


READ_RULE = {
    "name": "read",
    "participants": [{"type": "electron"}, {"type": "proton"}],
    "momentum_table": {"proton": 1},
    "reads": "content",
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


def world(model_id, half, fill, probe=None, *, closed=False):
    """The body at the centre of the (2 half + 1)^3 board; `probe` = (offset,
    heading): one test thing standing at centre + offset; `closed`: the
    periodic board with the standing-set search on, for CLOSED_TICKS."""
    shape = [2 * half + 1] * 3
    centre = (half, half, half)
    types = [
        {
            "name": "idle",
            "fields": ["electron", "momentum"],
            "defaults": {"electron": PROBE_CONTENT, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        }
    ]
    emissions, seeds, rules = [], [], []
    if probe is not None:
        offset, heading = probe
        types.append(
            {
                "name": "probe",
                "fields": ["electron", "momentum"],
                "defaults": {"electron": PROBE_CONTENT, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        )
        emissions.append(
            {
                "type": "probe",
                "field": "electron",
                "amount": PROBE_CONTENT,
                "denominator": 1,
                "heading": list(heading),
                "kerengonen_phase": 0,
            }
        )
        seeds.append(
            {
                "position": [centre[k] + offset[k] - heading[k] for k in range(3)],
                "type": "probe",
            }
        )
        rules.append(json.loads(json.dumps(READ_RULE)))
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
        "disturbance_types": types,
        "spatial_fields": [
            family("proton", PROTON_CHARGE, 24, release=RELEASE),
            family("electron", ELECTRON_CHARGE, 8, clock=True),
        ],
        "emissions": emissions,
        "seeds": seeds,
        "ray_interactions": rules,
        "external_bodies": [body(centre)],
        "detectors": [],
        "initial_field": {"proton": {"fill": fill}},
    }


def cases():
    yield "pulse", world("e11-law-pulse", PULSE_HALF, 1)
    yield "standing", world("e11-law-standing", HALF, FILL)
    yield "standing_closed", world("e11-law-standing-closed", HALF, FILL, closed=True)
    for direction, (offsets, heading, letter) in PROBES.items():
        for offset in offsets:
            name = f"probe_{direction}_{letter}{offset[0]}"
            yield name, world(f"e11-law-{name.replace('_', '-')}", HALF, FILL, (offset, heading))
    for direction, (offsets, heading, letter) in PROBES.items():
        for offset in offsets:
            name = f"probe_{direction}_{letter}{offset[0]}_closed"
            yield name, world(f"e11-law-{name.replace('_', '-')}", HALF, FILL, (offset, heading), closed=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in cases():
        # Written on the law: the migration of the old worlds is a no-op here.
        assert migrate(json.loads(json.dumps(document))) == document
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path, document["shape"], document["ticks"], document["model_id"])


if __name__ == "__main__":
    main()
