"""Configuration-only signed displacement and frozen, open electric-ray pilot.

Numerical authority: PROTON_NEUTRON_ELECTRON_CANDIDATE.md; source preparation
was published in 742eb3d9 before calibration. No host trajectory feeds this law.
"""

from __future__ import annotations

import json
from copy import deepcopy
from hashlib import sha256

from event_universe.initialization import parse_initial_state

MODEL_ID = "contact-bound-ray-electron-pilot-v1"
SOURCE_HASH = "551f46ab5e5a05916c85ccf5328918dd0ec45f95d7e7f23758a5d3eaaee1bb70"
SOURCE_RATE = 293
NORMAL_BUDGET = 536870912


def op(name: str, *args: object) -> dict[str, object]:
    return {"op": name, "args": list(args)}


def field(name: str) -> dict[str, str]:
    return {"field": name}


def component(name: str, index: int) -> dict[str, object]:
    return {"op": "component", "args": [field(name)], "index": index}


def definition(
    name: str,
    components: int,
    units: str,
    *,
    signed: bool = True,
    conserved: bool = False,
    extensive: bool = False,
) -> dict[str, object]:
    return {
        "name": name,
        "components": components,
        "units": units,
        "signed": signed,
        "conserved": conserved,
        "extensive": extensive,
    }


def source_headings() -> list[list[int]]:
    """Frozen bounded integer geometry; never selected from an orbital result."""
    headings = [
        [x, y, z]
        for x in range(-16, 17)
        for y in range(-16, 17)
        for z in range(-16, 17)
        if 225 < x * x + y * y + z * z <= 256
    ]
    encoded = (json.dumps(headings, separators=(",", ":")) + "\n").encode()
    if len(headings) != 2930 or sha256(encoded).hexdigest() != SOURCE_HASH:
        raise ValueError("source table differs from the published preparation")
    return headings


def electric_field() -> dict[str, object]:
    return {
        "field": "charge_field",
        "transport": "ray",
        "baseline": 0,
        "headings": source_headings(),
        "rays_per_tick": SOURCE_RATE,
        "ray_slots": 4096,
        "metric": "links",
    }


def electric_emission(enabled: int = 1) -> dict[str, object]:
    return {
        "requires": ["charge", "bound"],
        "field": "charge_field",
        "source": True,
        "amount": op(
            "mul", SOURCE_RATE * enabled, op("mul", op("gt", field("charge"), 0), field("bound"))
        ),
    }


def motion_updates(denominator: int, launch_age: int) -> list[dict[str, object]]:
    """Author the published local AST; evaluation belongs to the shared engine."""
    trial = [component("motion_trial", i) for i in range(3)]
    choice = [component("motion_choice", i) for i in range(3)]
    a, b, c = choice
    mask = op(
        "vector",
        op("mul", op("sub", 1, a), op("sub", 1, b)),
        op("mul", a, op("sub", 1, c)),
        op("mul", b, c),
    )
    signs = op("vector", *(op("exact_div", value, op("max", 1, op("abs", value))) for value in trial))
    largest = op("max", op("max", op("abs", trial[0]), op("abs", trial[1])), op("abs", trial[2]))
    due = op("gt", largest, denominator - 1)
    expressions = [
        (
            "motion_trial",
            op(
                "add",
                field("motion_remainder"),
                op("mul", op("gt", field("age"), launch_age - 1), field("momentum")),
            ),
        ),
        (
            "motion_choice",
            op(
                "vector",
                op("gt", op("abs", trial[1]), op("abs", trial[0])),
                op("gt", op("abs", trial[2]), op("abs", trial[0])),
                op("gt", op("abs", trial[2]), op("abs", trial[1])),
            ),
        ),
        ("hop_direction", op("mul", op("mul", mask, signs), due)),
        (
            "motion_remainder",
            op("sub", field("motion_trial"), op("mul", denominator, field("hop_direction"))),
        ),
        ("age", op("min", op("add", field("age"), 1), launch_age + 1)),
    ]
    return [{"field": name, "expression": expression} for name, expression in expressions]


def _integer_parameters(parameters: dict[str, int]) -> dict[str, int]:
    defaults = {
        "mass": 512,
        "speed_scale": 16,
        "launch_age": 64,
        "radius": 8,
        "px": 0,
        "py": 2048,
        "pz": 0,
        "source_enabled": 1,
    }
    required = {"force_numerator", "force_denominator"}
    if required - parameters.keys() or parameters.keys() - defaults.keys() - required:
        raise ValueError("supply an explicit calibrated force fraction and known parameters")
    if any(type(value) is not int for value in parameters.values()):
        raise ValueError("candidate parameters must be integers")
    defaults.update(parameters)
    if (
        min(defaults[key] for key in ("mass", "speed_scale", "force_denominator")) <= 0
        or defaults["force_numerator"] < 0
        or defaults["launch_age"] < 0
        or defaults["source_enabled"] not in (0, 1)
    ):
        raise ValueError("invalid candidate scale, preparation or response")
    if defaults["mass"] * defaults["speed_scale"] > 100000000:
        raise ValueError("candidate scale would overflow bounded helper state")
    return defaults


def add_electron(document: dict[str, object], *, parameters: dict[str, int]) -> dict[str, object]:
    """Deep-copy extension; reject shared-schema conflicts and preserve strong rules."""
    p = _integer_parameters(parameters)
    result = deepcopy(document)
    if (
        result.get("schema_version") != 1
        or result.get("link_ticks") != 1
        or result.get("boundary") != "open"
        or result.get("node_execution", False)
        or result.get("normal_budget", 0) < NORMAL_BUDGET
    ):
        raise ValueError("pilot requires schema 1, open H=1 and declared zero-wait budget")
    fields = result["fields"]
    names = {item["name"]: item for item in fields}
    for expected in (
        definition("mass", 1, "mass code", signed=False, conserved=True, extensive=True),
        definition("charge", 1, "charge code", conserved=True, extensive=True),
        definition("momentum", 3, "momentum code", conserved=True, extensive=True),
    ):
        actual = names.get(expected["name"], {})
        if (
            any(
                actual.get(key, True if key == "extensive" else None) != value
                for key, value in expected.items()
            )
            or actual.get("scale", 1) != 1
        ):
            raise ValueError(f"incompatible shared field {expected['name']}")
    if "bound" not in names:
        raise ValueError("electric source requires the published local binding property")
    additions = [
        definition(name, 3, "displacement numerator")
        for name in ("motion_remainder", "hop_direction", "motion_trial", "motion_choice")
    ]
    additions += [
        definition("age", 1, "local preparation cycles", signed=False),
        definition("charge_field", 1, "unit ray stock", conserved=True, extensive=True),
    ]
    if any(item["name"] in names for item in additions) or len(fields) + len(additions) > 16:
        raise ValueError("electron fields conflict or exceed the fixed 16-field capacity")
    fields.extend(additions)
    denominator = p["mass"] * p["speed_scale"]
    if sum(abs(p[name]) for name in ("px", "py", "pz")) > denominator:
        raise ValueError("electron momentum exceeds the one-hop local speed bound")
    owned = [
        "mass",
        "charge",
        "momentum",
        "motion_remainder",
        "hop_direction",
        "motion_trial",
        "motion_choice",
        "age",
    ]
    remainder = field("motion_remainder")
    max_remainder = op(
        "max",
        op(
            "max",
            op("abs", component("motion_remainder", 0)),
            op("abs", component("motion_remainder", 1)),
        ),
        op("abs", component("motion_remainder", 2)),
    )
    electron = {
        "name": "electron",
        "fields": owned,
        "defaults": {"mass": p["mass"], "charge": -1, "momentum": [p["px"], p["py"], p["pz"]]},
        "transport": {"mode": "move", "direction_field": "hop_direction"},
        "updates": motion_updates(denominator, p["launch_age"]),
        "checks": [
            {
                "name": "admissible_one_hop_momentum",
                "expression": op("gt", denominator + 1, op("sum", op("abs", field("momentum")))),
            },
            {
                "name": "bounded_total_remainder",
                "expression": op("gt", 3 * denominator, op("sum", op("abs", remainder))),
            },
            {
                "name": "bounded_component_remainder",
                "expression": op("gt", 2 * denominator, max_remainder),
            },
        ],
    }
    if any(kind["name"] == "electron" for kind in result["disturbance_types"]):
        raise ValueError("electron type already exists")
    result["disturbance_types"].append(electron)
    position = [size // 2 for size in result["shape"]]
    position[0] += p["radius"]
    result["seeds"].append({"position": position, "type": "electron"})
    spatial = result.setdefault("spatial_fields", [])
    if any(item["field"] in ("momentum", "charge_field") for item in spatial):
        raise ValueError("electron spatial owners must be unambiguous")
    spatial.extend(
        [electric_field(), {"field": "momentum", "transport": "local", "baseline": [0, 0, 0]}]
    )
    result.setdefault("emissions", []).append(electric_emission(p["source_enabled"]))
    # Exchange removes the request from the material owner and deposits its opposite locally.
    amount = op(
        "neg",
        op(
            "mul",
            p["force_numerator"],
            op(
                "mul",
                field("charge"),
                op("mul", op("gt", field("age"), p["launch_age"] - 1), {"flux": "charge_field"}),
            ),
        ),
    )
    result.setdefault("spatial_couplings", []).append(
        {
            "name": "electron_arrived_port_response_v1",
            "requires": ["charge", "momentum", "age", "motion_remainder"],
            "field": "momentum",
            "mode": "exchange",
            "amount": amount,
            "denominator": p["force_denominator"],
        }
    )
    # The standalone nuclear audit is closed-system-only; its pair invariants remain intact.
    result.pop("conservation", None)
    result["model_id"] = MODEL_ID
    parse_initial_state(result)
    return result
