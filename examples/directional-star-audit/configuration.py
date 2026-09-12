"""Prepare timing-only star encounters without a force or a steering rule."""

import json
from copy import deepcopy
from itertools import product
from pathlib import Path

from event_universe.experiment import load_experiment
from event_universe.initialization import parse_initial_state

HERE = Path(__file__).parent


def configurations():
    raw = json.loads(load_experiment(HERE.parent / "computational-star/experiment.json").runtime_json)
    raw.update(
        model_id="directional-star-orbit-audit-v1",
        shape=[128] * 3,
        ticks=256,
        normal_budget=1000000,
        directional_delay={
            "model_id": "positive-projection-origin-wait-v1",
            "field": "computational_load",
            "divisor": 16,
        },
    )
    raw["fields"].append(
        {
            "name": "charge",
            "components": 1,
            "signed": True,
            "conserved": True,
            "extensive": True,
            "units": "test charge unit",
        }
    )
    prototypes = json.loads((HERE / "entities.json").read_text())
    raw["disturbance_types"] = [raw["disturbance_types"][0], *prototypes["types"]]
    raw["seeds"] = [
        {
            "position": [64 + x, 64 + y, 64 + z],
            "type": "star_constituent",
            "values": {"mass": 1000000 if (x, y, z) == (0, 0, 0) else 10000},
        }
        for x, y, z in product((-1, 0, 1), repeat=3)
    ]
    raw["seeds"] += [{"position": [56, 68, 64], "type": p["name"]} for p in prototypes["types"]]
    cases = {}
    for name in (
        "active",
        "no_directional_wait",
        "no_field",
        "small_star",
        "reverse_vector",
        "mirrored_approach",
        "oblique",
        "radial",
        "symmetric_source_axes",
    ):
        cases[name] = deepcopy(raw)
    cases["no_directional_wait"].pop("directional_delay")
    cases["no_field"]["emissions"] = []
    for seed in cases["small_star"]["seeds"][:27]:
        seed["values"]["mass"] = 4
    cases["reverse_vector"]["disturbance_types"][0]["defaults"]["load_axis"] = [-1, -1, -1]
    for seed in cases["mirrored_approach"]["seeds"][27:]:
        seed["position"] = [72, 68, 64]
    for kind in cases["mirrored_approach"]["disturbance_types"][1:]:
        kind["defaults"]["momentum"][0] *= -1
    for kind in cases["oblique"]["disturbance_types"][1:]:
        unit = kind["defaults"]["momentum"][0]
        kind["defaults"]["momentum"] = [unit, unit, 0]
    for seed in cases["oblique"]["seeds"][27:]:
        seed["position"] = [56, 60, 64]
    for seed in cases["radial"]["seeds"][27:]:
        seed["position"] = [56, 64, 64]
    for seed in cases["symmetric_source_axes"]["seeds"][:27]:
        seed["values"]["load_axis"] = [x - 64 for x in seed["position"]]
    for case in cases.values():
        parse_initial_state(case)
    return cases
