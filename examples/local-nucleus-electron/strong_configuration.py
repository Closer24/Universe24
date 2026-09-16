"""Initialization for the published contact-bound nucleus candidate.

The dictionaries below declare operators for the existing integer evaluator.
They neither execute a second simulator nor supply an electron force law.
"""

from __future__ import annotations

from copy import deepcopy

MODEL_ID = "contact-bound-ray-electron-pilot-v1"
NUCLEON_MASS = 940032
BINDING_GAP = 669889164
HALF_GAP = 334944582
SPEED_SCALE = 16
NORMAL_BUDGET = 536870912
NUCLEAR_FIELDS = (
    "mass",
    "charge",
    "momentum",
    "baryon",
    "sector",
    "bound",
    "gap",
    "radiation",
    "excitation",
    "internal_direction",
)
AXIAL_HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]


def field(name: str, side: str | None = None) -> dict:
    return {"field": name, **({"side": side} if side is not None else {})}


def operation(name: str, *arguments: object) -> dict:
    return {"op": name, "args": list(arguments)}


def equal(left: object, right: object) -> dict:
    return operation("sub", 1, operation("min", 1, operation("abs", operation("sub", left, right))))


def both(*conditions: object) -> object:
    result = conditions[0]
    for condition in conditions[1:]:
        result = operation("mul", result, condition)
    return result


def energy(side: str | None = None) -> dict:
    """Nuclear readout, with fixed admitted mass so an empty owner has zero energy."""
    momentum = field("momentum", side)
    return operation(
        "sub",
        operation(
            "add",
            operation("exact_div", operation("dot", momentum, momentum), 2 * NUCLEON_MASS),
            operation("add", field("radiation", side), field("excitation", side)),
        ),
        operation("mul", field("gap", side), field("bound", side)),
    )


def shared_fields() -> list[dict]:
    return [
        {
            "name": name,
            "components": components,
            "units": units,
            "signed": signed,
            "conserved": conserved,
            "extensive": extensive,
        }
        for name, components, units, signed, conserved, extensive in (
            ("mass", 1, "mass code", False, True, True),
            ("charge", 1, "charge code", True, True, True),
            ("momentum", 3, "momentum code", True, True, True),
            ("baryon", 1, "baryon count", False, True, True),
            ("sector", 1, "reaction lifecycle", False, False, False),
            ("bound", 1, "binding flag", False, False, False),
            ("gap", 1, "energy code", False, False, False),
            ("radiation", 1, "energy code", False, False, True),
            ("excitation", 1, "energy code", False, False, True),
            ("internal_direction", 3, "unit release axis", True, False, False),
        )
    ]


def build_strong_document(
    *, parameters: dict[str, int], shape: tuple[int, int, int], ticks: int
) -> dict[str, object]:
    """Build pair-only capture or explicitly funded breakup controls.

    Parameters select coupling/emission (0 or 1), axis (0..2), boost (0 or 1),
    initial_bound (0 or 1), release_kick (0 or M), and each excitation owner.
    Prepared carriers always begin co-resident with zero transport histories.
    """
    allowed = {
        "coupling",
        "emission",
        "axis",
        "boost",
        "initial_bound",
        "release_kick",
        "excitation_left",
        "excitation_right",
    }
    if set(parameters) - allowed or any(type(value) is not int for value in parameters.values()):
        raise ValueError("unsupported strong parameter or noninteger value")
    if len(shape) != 3 or any(type(size) is not int or size < 5 for size in shape):
        raise ValueError("the strong world needs three dimensions of at least five Nodes")
    if type(ticks) is not int or ticks < 0:
        raise ValueError("ticks must be a nonnegative integer")
    coupling, emission = parameters.get("coupling", 1), parameters.get("emission", 1)
    boost, initially_bound = parameters.get("boost", 0), parameters.get("initial_bound", 0)
    axis, kick = parameters.get("axis", 0), parameters.get("release_kick", 0)
    if any(value not in (0, 1) for value in (coupling, emission, boost, initially_bound)):
        raise ValueError("coupling, emission, boost and initial_bound are binary")
    if axis not in (0, 1, 2) or kick not in (0, NUCLEON_MASS):
        raise ValueError("only axial exact zero or nucleon-mass breakup kicks are admitted")
    if boost and (emission or initially_bound):
        raise ValueError("the fresh boosted control must retain radiation without emission")
    excitation = [parameters.get("excitation_left", 0), parameters.get("excitation_right", 0)]
    if any(value < 0 or value > (1 << 30) - 1 for value in excitation):
        raise ValueError("excitation owners must fit the nonnegative payload domain")
    momentum = operation("add", field("momentum", "left"), field("momentum", "right"))
    common = operation("exact_div", momentum, 2)
    kinetic = operation(
        "exact_div",
        operation(
            "add",
            operation("dot", field("momentum", "left"), field("momentum", "left")),
            operation("dot", field("momentum", "right"), field("momentum", "right")),
        ),
        2 * NUCLEON_MASS,
    )
    center_kinetic = operation("exact_div", operation("dot", momentum, momentum), 4 * NUCLEON_MASS)
    capture_share = operation(
        "exact_div", operation("add", operation("sub", kinetic, center_kinetic), BINDING_GAP), 2
    )
    required_share = (BINDING_GAP + kick * kick // NUCLEON_MASS) // 2
    invariants = [
        {"name": "pair energy", "expression": operation("add", energy("left"), energy("right"))},
        {"name": "pair momentum", "expression": momentum},
    ]
    fresh = both(
        coupling,
        equal(field("sector", "left"), 0),
        equal(field("sector", "right"), 0),
        equal(operation("add", field("charge", "left"), field("charge", "right")), 1),
        equal(
            operation("dot", field("internal_direction", "left"), field("internal_direction", "right")),
            -1,
        ),
    )
    funded = both(
        equal(field("sector", "left"), 1),
        equal(field("sector", "right"), 1),
        operation("gt", field("excitation", "left"), required_share - 1),
        operation("gt", field("excitation", "right"), required_share - 1),
    )
    capture, release = [], []
    for side in ("left", "right"):
        for name, expression in (
            ("momentum", common),
            ("bound", 1),
            ("sector", 1),
            ("radiation", operation("add", field("radiation", side), capture_share)),
        ):
            capture.append({"side": side, "field": name, "expression": expression})
        for name, expression in (
            (
                "momentum",
                operation("add", common, operation("mul", kick, field("internal_direction", side))),
            ),
            ("bound", 0),
            ("sector", 2),
            ("excitation", operation("sub", field("excitation", side), required_share)),
        ):
            release.append({"side": side, "field": name, "expression": expression})
    transport = {
        "mode": "move",
        "routing": "balanced",
        "direction_field": "momentum",
        "rate": operation("sum", operation("abs", field("momentum"))),
        "rate_denominator": SPEED_SCALE,
        "rate_divisor": field("mass"),
    }
    kinds = []
    for index, (name, charge, sign) in enumerate((("proton", 1, 1), ("neutron", 0, -1))):
        direction = [0, 0, 0]
        direction[axis] = sign
        initial_momentum = [0, 0, 0]
        initial_momentum[axis] = 0 if initially_bound else (sign + boost) * NUCLEON_MASS
        defaults = {
            "mass": NUCLEON_MASS,
            "charge": charge,
            "momentum": initial_momentum,
            "baryon": 1,
            "sector": initially_bound,
            "bound": initially_bound,
            "gap": HALF_GAP,
            "radiation": 0,
            "excitation": excitation[index],
            "internal_direction": direction,
        }
        checks = [
            ("fixed mass", equal(field("mass"), NUCLEON_MASS)),
            ("one baryon", equal(field("baryon"), 1)),
            ("fixed gap", equal(field("gap"), HALF_GAP)),
            ("lifecycle range", operation("gt", 3, field("sector"))),
            ("binding matches lifecycle", equal(field("bound"), equal(field("sector"), 1))),
            (
                "unit release direction",
                equal(operation("dot", field("internal_direction"), field("internal_direction")), 1),
            ),
        ]
        kinds.append(
            {
                "name": name,
                "fields": list(NUCLEAR_FIELDS),
                "defaults": defaults,
                "transport": deepcopy(transport),
                "checks": [{"name": label, "expression": value} for label, value in checks],
            }
        )
    document = {
        "schema_version": 1,
        "model_id": MODEL_ID,
        "shape": list(shape),
        "boundary": "open",
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": NORMAL_BUDGET,
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
        "fields": shared_fields(),
        "disturbance_types": kinds,
        "interactions": [
            {
                "name": "contact capture",
                "left_requires": list(NUCLEAR_FIELDS),
                "right_requires": list(NUCLEAR_FIELDS),
                "when": fresh,
                "assignments": capture,
                "invariants": deepcopy(invariants),
            },
            {
                "name": "funded dissociation",
                "left_requires": list(NUCLEAR_FIELDS),
                "right_requires": list(NUCLEAR_FIELDS),
                "when": funded,
                "assignments": release,
                "invariants": deepcopy(invariants),
            },
        ],
        "seeds": [
            {"position": [size // 2 for size in shape], "type": name} for name in ("proton", "neutron")
        ],
        "conservation": {
            "name": "closed contact gap and radiation",
            "energy_units": "energy code",
            "momentum_units": "momentum code",
            "carriers": [
                {"requires": list(NUCLEAR_FIELDS), "energy": energy(), "momentum": field("momentum")}
            ],
        },
    }
    if emission:
        document["spatial_fields"] = [
            {
                "field": "radiation",
                "baseline": 0,
                "transport": "ray",
                "headings": deepcopy(AXIAL_HEADINGS),
                "rays_per_tick": 6,
                "ray_slots": 64,
            }
        ]
        document["emissions"] = [
            {
                "requires": list(NUCLEAR_FIELDS),
                "field": "radiation",
                "amount": field("radiation"),
                "denominator": 1,
                "source": False,
            }
        ]
        document["conservation"]["spatial"] = {
            "energy": field("radiation", "right"),
            "momentum": operation("vector", 0, 0, 0),
        }
    return document
