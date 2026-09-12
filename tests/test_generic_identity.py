"""Names and declaration indices cannot select generic simulation behavior."""

import json
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
FIELD_LABELS = ("__proto__", "constructor", "toString", "prototype", "add", "hold", "field")
TYPE_LABELS = ("constructor", "__proto__", "hold")
FIELD_MAPS = {
    "values",
    "fields",
    "spatial_baselines",
    "escaped_totals",
    "source_delta",
    "reaction",
    "dissipated",
    "escaped",
    "totals",
    "sources",
    "losses",
    "escapes",
    "accounting",
}


def configured_example(case):
    name = "spatial_turning" if case in {"rotation", "flux"} else case
    raw = json.loads((EXAMPLES / f"{name}.json").read_text(encoding="utf-8"))
    raw["normal_budget"] = {"basic": 10, "exchange": 5, "rotation": 150}.get(case, 100000)
    if case == "basic":
        raw["disturbance_types"][0]["updates"] = [
            {
                "field": "mass",
                "source": True,
                "expression": {"op": "add", "args": [{"field": "mass"}, 1]},
            }
        ]
    if case == "finite_fields":
        raw["emissions"][0]["budget"] = 144
        raw["spatial_fields"][0]["baseline"] = 3
    if case in {"rotation", "flux"}:
        raw["schema_version"] = 2
        for field in raw["spatial_fields"]:
            field["decay"] = {"retain_numerator": 1, "retain_denominator": 2}
        raw["spatial_couplings"][0]["budget"] = [20, 20, 20]
    if case == "flux":
        raw["fields"][1]["components"] = 1
        raw["spatial_fields"][1].update(baseline=1, axis_weights=[0, 1, 0])
        raw["spatial_couplings"][0].update(rotation={"flux": "control"}, denominator=12)
        raw["spatial_seeds"] = [
            {"position": [16, 14, 15], "field": "control", "populations": [24] + [0] * 7}
        ]
    return raw


def renamed_document(raw):
    """Rename only semantic labels/references; leave operators and law order intact."""
    result = deepcopy(raw)
    fields = {field["name"]: FIELD_LABELS[i] for i, field in enumerate(raw["fields"])}
    types = {kind["name"]: TYPE_LABELS[i] for i, kind in enumerate(raw["disturbance_types"])}

    def expression(value):
        if not isinstance(value, dict):
            return
        for key in ("field", "flux"):
            if key in value:
                value[key] = fields[value[key]]
        for argument in value.get("args", []):
            expression(argument)

    def values(mapping):
        return {fields[name]: value for name, value in mapping.items()}

    result["model_id"] = "hold"
    for index, field in enumerate(result["fields"]):
        field.update(name=fields[field["name"]], units=f"unrelated unit label {index}")
    for kind in result["disturbance_types"]:
        kind["name"] = types[kind["name"]]
        kind["fields"] = [fields[name] for name in kind["fields"]]
        kind["defaults"] = values(kind.get("defaults", {}))
        if "cost_field" in kind:
            kind["cost_field"] = fields[kind["cost_field"]]
        transport = kind["transport"]
        if "direction_field" in transport:
            transport["direction_field"] = fields[transport["direction_field"]]
        expression(transport.get("rate"))
        for update in kind.get("updates", []):
            update["field"] = fields[update["field"]]
            expression(update["expression"])
    for group in ("couplings", "spatial_couplings", "emissions"):
        for index, rule in enumerate(result.get(group, [])):
            if "name" in rule:
                rule["name"] = f"rule label {index}"
            for key in ("type", "left_type", "right_type"):
                if key in rule:
                    rule[key] = types[rule[key]]
            rule["field"] = fields[rule["field"]]
            for key in ("amount", "rotation"):
                expression(rule.get(key))
    for group in ("spatial_fields", "spatial_seeds"):
        for item in result.get(group, []):
            item["field"] = fields[item["field"]]
    for seed in result["seeds"]:
        seed["type"] = types[seed["type"]]
        if "values" in seed:
            seed["values"] = values(seed["values"])
    return result, {new: old for old, new in fields.items()}, {new: old for old, new in types.items()}


def reorder_declarations(raw):
    for key in ("fields", "disturbance_types", "spatial_fields"):
        if key in raw:
            raw[key].reverse()
    for kind in raw["disturbance_types"]:
        kind["fields"].reverse()
        kind["defaults"] = dict(reversed(list(kind.get("defaults", {}).items())))


def normalize(value, fields, types, context=None):
    """Decode semantic output labels without rewriting event or operator keywords."""
    if isinstance(value, dict):
        if context in FIELD_MAPS:
            return {fields.get(key, key): normalize(item, fields, types) for key, item in value.items()}
        return {key: normalize(item, fields, types, key) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return tuple(normalize(item, fields, types) for item in value)
    if context in {"type", "disturbance"}:
        return types.get(value, value)
    return value


def observation(world, events):
    return {
        "snapshot": world.snapshot(),
        "events": events,
        "totals": world.totals(),
        "sources": world.source_totals(),
        "losses": world.dissipation_totals(),
        "escapes": world.escaped_totals(),
        "accounting": world.spatial_accounting(),
    }


def assert_exercised(case, world, events):
    assert any(event["event"] == "cycle_committed" for event in events)
    if case in {"basic", "exchange", "rotation"}:
        assert any(
            event["event"] == "cycle_started" and event["ready_tick"] > event["tick"] for event in events
        )
    if case == "basic":
        assert any(event["event"] == "sent" and event["disturbance"] == "pulse" for event in events)
        reporter = next(
            record
            for cell in world.snapshot()["cells"]
            for record in cell["disturbances"]
            if record["type"] == "local_work"
        )
        assert reporter["values"]["computation"][0] > 0
        assert world.source_totals()["mass"][0] > 0
    elif case == "exchange":
        records = world.snapshot()["cells"][0]["disturbances"]
        assert [record["values"]["balance"] for record in records] == [(6,), (2,)]
    elif case == "finite_fields":
        assert world.source_totals()["radiation"] == (144,)
        assert world.dissipation_totals()["radiation"][0] > 0
        assert world.snapshot()["spatial_baselines"]["radiation"] == (3,)
    elif case == "open_world":
        assert world.escaped_totals() == {"strength": (72,), "radiation": (20,)}
    elif case in {"rotation", "flux"}:
        assert any(
            event["event"] == "spatial_coupled" and any(event["reaction"].get("inventory", ()))
            for event in events
        )
        records = [
            record for cell in world.snapshot()["cells"] for record in cell["disturbances"]
        ] + world.snapshot()["transfers"]
        assert records and all(sum(v * v for v in r["values"]["inventory"]) == 25 for r in records)


@pytest.mark.parametrize(
    "case", ["basic", "exchange", "finite_fields", "open_world", "rotation", "flux"]
)
@pytest.mark.parametrize("change", ["rename", "reorder", "both"])
def test_generic_runtime_uses_references_instead_of_names_or_declaration_indices(case, change):
    original = configured_example(case)
    unchanged = deepcopy(original)
    changed, fields, types = renamed_document(original)
    if change == "reorder":
        changed, fields, types = deepcopy(original), {}, {}
    if change != "rename":
        reorder_declarations(changed)
    events = [[], []]
    worlds = [
        Simulation(parse_initial_state(raw), observer=sink.append)
        for raw, sink in zip((original, changed), events, strict=True)
    ]
    initial = worlds[0].totals()
    for tick in range(7):
        assert normalize(observation(worlds[0], events[0]), {}, {}) == normalize(
            observation(worlds[1], events[1]), fields, types
        ), (case, change, tick)
        for name, total in worlds[0].totals().items():
            assert tuple(
                value + loss + escaped
                for value, loss, escaped in zip(
                    total,
                    worlds[0].dissipation_totals()[name],
                    worlds[0].escaped_totals()[name],
                    strict=True,
                )
            ) == tuple(
                a + b for a, b in zip(initial[name], worlds[0].source_totals()[name], strict=True)
            )
        assert all(item["balanced"] for item in worlds[0].spatial_accounting().values())
        if tick < 6:
            for world in worlds:
                world.step()
    assert_exercised(case, worlds[0], events[0])
    assert original == unchanged
