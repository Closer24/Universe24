"""Small, explicit candidates; physical equations never generate their updates."""

import copy
import json
from pathlib import Path

from event_universe.entities import compile_entities

ROOT = Path(__file__).resolve().parents[2]


def read(relative):
    return json.loads((ROOT / relative).read_text())


def op(name, *args):
    return {"op": name, "args": list(args)}


def local(name, side="right"):
    return {"field": name, "side": side}


def relocate(raw, size):
    """Translate a finite experiment without changing any local rule or unit."""
    raw = copy.deepcopy(raw)
    shift = size // 2 - raw["shape"][0] // 2
    raw["shape"] = [size] * 3
    for seed in raw.get("seeds", []) + raw.get("spatial_seeds", []):
        seed["position"] = [value + shift for value in seed["position"]]
    return raw


def candidates():
    catalog = read("examples/known-entities/catalog.json")
    cases = {}
    for identity in ("electron", "proton", "photon"):
        cases[identity + "-free"] = compile_entities(catalog, [identity])
    raw = copy.deepcopy(cases["photon-free"])
    raw["model_id"] = "one-link-per-tick-ray-candidate-v1"
    raw["disturbance_types"][0]["transport"]["rate_denominator"] = 1
    cases["photon-speed-candidate"] = raw
    raw = copy.deepcopy(cases["electron-free"])
    raw["seeds"][0]["values"]["momentum"] = [0, 0, 0]
    cases["electron-rest"] = raw
    raw = copy.deepcopy(cases["electron-free"])
    raw["seeds"][0]["values"]["momentum"] = [2, 0, 0]
    cases["electron-double-momentum"] = raw

    for identity in ("electromagnetic_field", "higgs_field", "strong_field", "computational_field"):
        cases[identity] = compile_entities(catalog, [identity])
    raw = copy.deepcopy(cases["electromagnetic_field"])
    raw["spatial_seeds"][1]["populations"] = [[0, 0, 0]] * 8
    cases["electric-only-pulse"] = raw

    raw = compile_entities(catalog, ["electron", "positron", "neutron", "electromagnetic_field"])
    raw["spatial_seeds"] = []
    raw["field_rules"] = []
    raw["spatial_fields"][0]["baseline"] = [1, 0, 0]
    for index, (kind, seed) in enumerate(zip(raw["disturbance_types"], raw["seeds"], strict=True)):
        kind["transport"] = {"mode": "hold"}
        seed["position"] = [3 + index, 4, 4]
        seed["values"]["momentum"] = [0, 0, 0]
    cases["charges-in-electric-background"] = raw

    pair = read("examples/known-entities/discrete-pair.json")
    pair["ticks"] = 12
    cases["equal-contact-9"] = pair
    cases["equal-contact-15"] = relocate(pair, 15)
    raw = copy.deepcopy(pair)
    raw["disturbance_types"][1]["defaults"]["mass"] = 2
    names = {
        raw["disturbance_types"][0]["name"]: "synthetic light body",
        raw["disturbance_types"][1]["name"]: "synthetic heavy body",
    }
    for kind in raw["disturbance_types"]:
        kind["name"] = names[kind["name"]]
    for seed in raw["seeds"]:
        seed["type"] = names[seed["type"]]
    for rule in raw["interactions"]:
        rule["left_type"] = names[rule["left_type"]]
        rule["right_type"] = names[rule["right_type"]]
    raw["model_id"] = "synthetic-unequal-pair-under-equal-mass-rule-v1"
    cases["unequal-contact-current"] = raw
    raw = copy.deepcopy(raw)
    raw["ticks"] = 8
    raw["model_id"] = "zero-total-momentum-permutation-candidate-v1"
    raw["fields"][0]["units"] = "synthetic mass unit"
    raw["fields"][2]["units"] = "synthetic mass unit times link speed"
    raw["fields"][2]["scale"] = 2
    raw["seeds"][0]["position"] = [2, 4, 4]
    raw["disturbance_types"][0]["transport"]["rate_denominator"] = 2
    momentum_sum = op("add", local("momentum", "left"), local("momentum", "right"))
    zero_total = op("sub", 1, op("gt", op("dot", momentum_sum, momentum_sum), 0))
    raw["interactions"][0]["when"]["args"][0] = zero_total
    cases["unequal-zero-total-candidate"] = raw

    source = read("examples/small-space/source-pulse.json")
    cases["source-emission"] = source
    pulse = copy.deepcopy(source)
    pulse["model_id"] = "outward-pulse-shell-diagnostic-v1"
    pulse["ticks"] = 5
    pulse["emissions"] = []
    pulse["seeds"] = []
    pulse["spatial_seeds"] = [{"position": [4, 4, 4], "field": "radiation", "populations": [27] * 8}]
    cases["outward-pulse-9"] = pulse
    cases["outward-pulse-15"] = relocate(pulse, 15)

    response = read("examples/small-space/source-response.json")
    cases["source-response-9"] = response
    cases["source-response-15"] = relocate(response, 15)
    negative = copy.deepcopy(response)
    negative["disturbance_types"][1]["defaults"]["polarity"] = -1
    cases["source-response-negative"] = negative
    control = copy.deepcopy(response)
    control["seeds"] = control["seeds"][1:]
    cases["receiver-without-source"] = control

    # An explicitly separate candidate transfers finite stock to a field.
    # Stock is abstract inventory, not an assumed physical energy variable.
    raw = compile_entities(catalog, ["computational_field"])
    name = raw["fields"][0]["name"]
    raw["fields"][0]["conserved"] = True
    raw["model_id"] = "closed-reservoir-transfer-candidate-v1"
    raw["spatial_seeds"] = []
    raw["disturbance_types"] = [
        {"name": "reservoir", "fields": [name], "defaults": {name: 3}, "transport": {"mode": "hold"}}
    ]
    raw["seeds"] = [{"position": [4, 4, 4], "type": "reservoir"}]
    raw["spatial_interactions"] = [
        {
            "name": "one owned unit per local cycle",
            "type": "reservoir",
            "when": op("gt", local(name, "left"), 0),
            "assignments": [
                {"side": "left", "field": name, "expression": op("sub", local(name, "left"), 1)},
                {"side": "right", "field": name, "expression": op("add", local(name), 1)},
            ],
            "invariants": [
                {"name": "combined stock", "expression": op("add", local(name, "left"), local(name))}
            ],
        }
    ]
    cases["closed-reservoir"] = raw
    return cases
