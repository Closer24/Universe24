"""Directional radiation quanta scattered by a charged carrier, entirely in initialization JSON.

Six scalar local fields carry integer quanta, one per cardinal travel direction;
each quantum carries one momentum unit along its direction. A carrier emits a
`presence` marker proportional to charge squared. The field phase holds up to
`presence * cross_section` of the +X stream at that node and streams the rest;
in the next carrier phase a joint transaction turns the held quanta into the
-X stream and gives the carrier twice their momentum. Quanta and momentum are
declared invariants of every rule. The engine sees only generic operations.

    python examples/radiation-scattering/build.py --output artifacts/radiation-scattering
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

DIRECTIONS = ("px", "mx", "py", "my", "pz", "mz")
UNIT = {
    "px": [1, 0, 0],
    "mx": [-1, 0, 0],
    "py": [0, 1, 0],
    "my": [0, -1, 0],
    "pz": [0, 0, 1],
    "mz": [0, 0, -1],
}
CROSS_SECTION = 2
SHAPE = [17, 5, 5]
CENTER = 2
CARRIER_X, SOURCE_X = 8, 2


def op(name: str, *args: object) -> dict:
    return {"op": name, "args": list(args)}


def right(name: str) -> dict:
    return {"field": name, "side": "right"}


def quanta_expression(extra_outgoing: bool = False) -> dict:
    terms: list[object] = [right(f"rad_{d}") for d in DIRECTIONS] + [right("held_px")]
    if extra_outgoing:
        terms += [{"outgoing": f"rad_{d}", "port": i} for i, d in enumerate(DIRECTIONS)]
    total = terms[0]
    for term in terms[1:]:
        total = op("add", total, term)
    return total


def wave_momentum_expression() -> dict:
    total = op("mul", right("rad_px"), [1, 0, 0])
    for d in DIRECTIONS[1:]:
        total = op("add", total, op("mul", right(f"rad_{d}"), UNIT[d]))
    return op("add", total, op("mul", right("held_px"), [1, 0, 0]))


def configuration(
    charge: int,
    *,
    ticks: int = 14,
    quanta_per_tick: int = 10,
    pulses: int = 6,
) -> dict:
    fields = [
        {"name": "mass", "components": 1, "units": "mass unit", "signed": False, "conserved": True},
        {"name": "charge", "components": 1, "units": "charge unit", "signed": True, "conserved": True},
        # Carrier momentum is conserved only jointly with the radiation quanta; the named
        # total_momentum invariant enforces that per transaction, so the per-field flag is off.
        {
            "name": "momentum",
            "components": 3,
            "units": "quantum momentum unit",
            "signed": True,
            "conserved": False,
            "extensive": True,
        },
        {
            "name": "presence",
            "components": 1,
            "units": "charge squared",
            "signed": False,
            "conserved": False,
        },
        {
            "name": "held_px",
            "components": 1,
            "units": "radiation quantum",
            "signed": False,
            "conserved": False,
        },
    ] + [
        {
            "name": f"rad_{d}",
            "components": 1,
            "units": "radiation quantum",
            "signed": False,
            "conserved": False,
        }
        for d in DIRECTIONS
    ]
    held = op("min", right("rad_px"), op("mul", right("presence"), CROSS_SECTION))
    field_rules = [
        {
            "name": "hold_scattered_quanta",
            "when": op("gt", op("mul", right("presence"), right("rad_px")), 0),
            "assignments": [
                {"field": "held_px", "expression": op("add", right("held_px"), held)},
                {"field": "rad_px", "expression": op("sub", right("rad_px"), held)},
            ],
            "invariants": [{"name": "quanta", "expression": quanta_expression()}],
        },
        {
            "name": "stream_quanta",
            "assignments": [
                item
                for i, d in enumerate(DIRECTIONS)
                for item in (
                    {"field": f"rad_{d}", "expression": 0},
                    {"field": f"rad_{d}", "port": i, "expression": right(f"rad_{d}")},
                )
            ],
            "invariants": [{"name": "quanta", "expression": quanta_expression(extra_outgoing=True)}],
        },
        {
            "name": "clear_presence",
            "assignments": [{"field": "presence", "expression": 0}],
            "invariants": [{"name": "quanta", "expression": quanta_expression()}],
        },
    ]
    scatter = {
        "name": "scatter_held_quanta",
        "type": "scatterer",
        "when": op("gt", right("held_px"), 0),
        "assignments": [
            {"side": "right", "field": "held_px", "expression": 0},
            {
                "side": "right",
                "field": "rad_mx",
                "expression": op("add", right("rad_mx"), right("held_px")),
            },
            {
                "side": "left",
                "field": "momentum",
                "expression": op(
                    "add", {"field": "momentum"}, op("mul", op("mul", right("held_px"), 2), [1, 0, 0])
                ),
            },
        ],
        "invariants": [
            {"name": "quanta", "expression": quanta_expression()},
            {
                "name": "total_momentum",
                "expression": op("add", {"field": "momentum"}, wave_momentum_expression()),
            },
        ],
    }
    # The marker is emitted in every field interval; a held carrier cycles only when it
    # has work, so a carrier-phase assignment would mark only every other interval.
    emissions = [
        {
            "type": "scatterer",
            "field": "presence",
            "amount": op("mul", {"field": "charge"}, {"field": "charge"}),
            "denominator": 1,
            "source": True,
        }
    ]
    return {
        "schema_version": 1,
        "model_id": "directional-quanta-charge-scattering-v1",
        "boundary": "open",
        "shape": SHAPE,
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 1_000_000,
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
        "fields": fields,
        "disturbance_types": [
            {
                "name": "scatterer",
                "fields": ["mass", "charge", "momentum"],
                "defaults": {"mass": 1, "charge": charge, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            {"field": name, "baseline": 0, "transport": "local"}
            for name in ("presence", "held_px", *(f"rad_{d}" for d in DIRECTIONS))
        ],
        "emissions": emissions,
        "spatial_seeds": [
            {
                "position": [SOURCE_X + i, CENTER, CENTER],
                "field": "rad_px",
                "populations": [quanta_per_tick] + [0] * 7,
            }
            for i in range(pulses)
        ],
        "field_rules": field_rules,
        "spatial_interactions": [scatter],
        "seeds": [{"position": [CARRIER_X, CENTER, CENTER], "type": "scatterer"}],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", default="artifacts/radiation-scattering")
    parser.add_argument("--charge", type=int, default=-1)
    args = parser.parse_args()
    config = configuration(args.charge)
    path = HERE / f"scattering-charge-{args.charge}.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    output = (ROOT / args.output).resolve()
    shutil.rmtree(output, ignore_errors=True)
    subprocess.run(
        [sys.executable, "-m", "event_universe", "--init", str(path), "--output", str(output)],
        cwd=ROOT,
        check=True,
    )
    print(path, "->", output)


if __name__ == "__main__":
    main()
