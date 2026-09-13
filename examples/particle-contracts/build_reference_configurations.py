"""Produce runtime JSON candidates; all physical formulas remain outside the engine."""

import json
from pathlib import Path

HERE = Path(__file__).parent


def op(name, *args):
    return {"op": name, "args": list(args)}


def field(name, side="left"):
    return {"field": name, "side": side}


def momentum(side="left"):
    return op(
        "add", field("whole", side), op("ratio", field("remainder", side), field("denominator", side))
    )


def kinetic(side="left"):
    return op("ratio", op("dot", momentum(side), momentum(side)), op("mul", 2, field("mass", side)))


def projected(name, expression):
    return op("rational_" + name, expression)


def base():
    fields = [
        ("mass", 1, False, True),
        ("charge", 1, True, True),
        ("whole", 3, True, False),
        ("remainder", 3, True, False),
        ("denominator", 1, False, False),
    ]
    return {
        "schema_version": 1,
        "model_id": "bounded-rational-particle-candidate-v1",
        "shape": [17, 17, 17],
        "boundary": "periodic",
        "slots_per_node": 4,
        "link_ticks": 1,
        "ticks": 180,
        "normal_budget": 100000000,
        "operation_costs": dict.fromkeys(
            ["receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit"], 1
        ),
        "fields": [
            {
                "name": n,
                "components": c,
                "units": "configured unit",
                "signed": s,
                "conserved": conserved,
                "extensive": conserved,
            }
            for n, c, s, conserved in fields
        ],
        "disturbance_types": [],
        "seeds": [],
    }


def entity(name, spec, p):
    rate = op("ratio", op("sum", op("abs", momentum())), field("mass"))
    return {
        "name": name,
        "fields": ["mass", "charge", "whole", "remainder", "denominator"],
        "defaults": {**spec, "whole": p, "remainder": [0, 0, 0], "denominator": 1},
        "transport": {
            "mode": "move",
            "routing": "balanced",
            "direction": projected("direction", momentum()),
            "rate": projected("numerator", rate),
            "rate_divisor": projected("denominator", rate),
            "rate_denominator": 12,
        },
    }


def pair(left, right, entities):
    raw = base()
    raw["model_id"] = "bounded-rational-elastic-" + left + "-" + right + "-v1"
    for name, sign in [(left, 1), (right, -1)]:
        spec = entities[name]
        raw["disturbance_types"].append(entity(name, spec, [sign * spec["mass"], 0, 0]))
        raw["seeds"].append({"position": [8, 8, 8], "type": name})
    ml, mr, pl, pr = field("mass"), field("mass", "right"), momentum(), momentum("right")
    total = op("add", ml, mr)
    results = [
        op("ratio", op("add", op("mul", op("sub", ml, mr), pl), op("mul", op("mul", 2, ml), pr)), total),
        op("ratio", op("add", op("mul", op("sub", mr, ml), pr), op("mul", op("mul", 2, mr), pl)), total),
    ]
    raw["interactions"] = [
        {
            "name": "configured_elastic_backscatter",
            "left_type": left,
            "right_type": right,
            "when": projected(
                "floor",
                op(
                    "gt",
                    {
                        "op": "component",
                        "args": [op("sub", op("ratio", pl, ml), op("ratio", pr, mr))],
                        "index": 0,
                    },
                    0,
                ),
            ),
            "assignments": [
                {"side": side, "field": name, "expression": projected(projection, value)}
                for side, value in zip(["left", "right"], results, strict=True)
                for name, projection in [
                    ("whole", "whole"),
                    ("remainder", "remainder"),
                    ("denominator", "denominator"),
                ]
            ],
            "invariants": [
                {"name": "decoded_momentum", "expression": projected("key", op("add", pl, pr))},
                {
                    "name": "decoded_kinetic_energy",
                    "expression": projected("key", op("add", kinetic(), kinetic("right"))),
                },
            ],
        }
    ]
    return raw


def massless(direction, energy):
    raw = base()
    raw["model_id"] = "configured-massless-half-speed-v1"
    raw["fields"].append(
        {
            "name": "energy",
            "components": 1,
            "units": "configured energy",
            "signed": False,
            "conserved": True,
        }
    )
    kind = entity("massless", {"mass": 0, "charge": 0}, direction)
    kind["fields"].append("energy")
    kind["defaults"]["energy"] = energy
    kind["checks"] = [
        {
            "name": "configured_mass_shell",
            "expression": projected(
                "floor",
                op(
                    "eq",
                    op("mul", 4, op("mul", field("energy"), field("energy"))),
                    op("dot", momentum(), momentum()),
                ),
            ),
        }
    ]
    # c=1/2, E=c*|p|. Hop rate c*||p||1/|p| = ||p||1/(4E).
    rate = op("ratio", op("sum", op("abs", momentum())), op("mul", 4, field("energy")))
    kind["transport"].update(
        rate=projected("numerator", rate),
        rate_divisor=projected("denominator", rate),
        rate_denominator=1,
    )
    raw["disturbance_types"] = [kind]
    raw["seeds"] = [{"type": "massless", "position": [8, 8, 8]}]
    return raw


def reservoir():
    raw = base()
    raw["model_id"] = "configured-local-kinetic-reservoir-v1"
    raw["ticks"] = 12
    raw["fields"].append(
        {
            "name": "reservoir",
            "components": 1,
            "units": "kinetic energy unit",
            "signed": False,
            "conserved": False,
        }
    )
    raw["fields"].append(
        {
            "name": "reaction",
            "components": 3,
            "units": "momentum unit",
            "signed": True,
            "conserved": False,
        }
    )
    kind = entity("probe", {"mass": 2, "charge": 1}, [4, 0, 0])
    kind["transport"] = {
        "mode": "move",
        "routing": "balanced",
        "direction": projected("direction", momentum()),
        "rate": 1,
    }
    raw["disturbance_types"] = [kind]
    raw["seeds"] = [{"type": "probe", "position": [8, 8, 8]}]
    raw["spatial_fields"] = [
        {"field": "reservoir", "baseline": 0, "transport": "local"},
        {"field": "reaction", "baseline": [0, 0, 0], "transport": "local"},
    ]
    raw["spatial_seeds"] = [
        {"field": "reservoir", "position": [8, 8, 8], "populations": [10, 0, 0, 0, 0, 0, 0, 0]}
    ]
    after = op("add", momentum(), [2, 0, 0])
    new_energy = op(
        "sub",
        op("add", field("reservoir", "right"), kinetic()),
        op("ratio", op("dot", after, after), op("mul", 2, field("mass"))),
    )
    raw["spatial_interactions"] = [
        {
            "name": "configured_energy_exchange",
            "type": "probe",
            "assignments": [
                {"side": "left", "field": n, "expression": projected(p, after)}
                for n, p in [
                    ("whole", "whole"),
                    ("remainder", "remainder"),
                    ("denominator", "denominator"),
                ]
            ]
            + [
                {
                    "side": "right",
                    "field": "reservoir",
                    "expression": projected("numerator", new_energy),
                },
                {
                    "side": "right",
                    "field": "reaction",
                    "expression": op("sub", field("reaction", "right"), [2, 0, 0]),
                },
            ],
            "when": {"op": "gt", "args": [field("reservoir", "right"), 0]},
            "invariants": [
                {
                    "name": "joint_energy",
                    "expression": projected("key", op("add", kinetic(), field("reservoir", "right"))),
                },
                {
                    "name": "joint_momentum",
                    "expression": projected("key", op("add", momentum(), field("reaction", "right"))),
                },
            ],
        }
    ]
    return raw


def main():
    entities = json.loads((HERE / "entities.json").read_text(encoding="utf-8"))["entities"]
    for left, right in [("electron", "positron"), ("electron", "proton"), ("proton", "neutron")]:
        (HERE / f"{left}-{right}.json").write_text(
            json.dumps(pair(left, right, entities), indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    for name, direction, energy in [("axis", [10, 0, 0], 5), ("oblique", [6, 8, 0], 5)]:
        (HERE / f"massless-{name}.json").write_text(
            json.dumps(massless(direction, energy), indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    (HERE / "energy-reservoir.json").write_text(
        json.dumps(reservoir(), indent=2) + "\n", encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    main()
