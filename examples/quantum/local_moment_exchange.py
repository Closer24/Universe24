"""Author a local exchange of coarse momentum moments after quantum capture.

The finite quantum contact profile supplies the localization event. A separate
configured equal-mass response swaps the local records' mean momentum and trace
of covariance. Zero mean with nonzero spread is not a definite zero momentum.
This candidate closes its declared moments; it does not derive their values from
the spatial quantum amplitudes or establish full quantum/classical dynamics.
"""

import json
from copy import deepcopy
from pathlib import Path

EXAMPLE = Path(__file__).resolve().with_name("localized_charge.json")


def _field(name, side):
    return {"field": name, "side": side}


def _operation(name, *arguments):
    return {"op": name, "args": list(arguments)}


def _second_moment(side):
    mean = _field("coarse_momentum", side)
    return _operation("add", _operation("dot", mean, mean), _field("momentum_spread", side))


def _exchange_rule(fields):
    assignments = []
    exchanged = {"coarse_momentum", "momentum_spread", "momentum_known"}
    for side, other in (("left", "right"), ("right", "left")):
        for name in fields:
            assignments.append(
                {
                    "side": side,
                    "field": name,
                    "expression": _field(name, other if name in exchanged else side),
                }
            )
    return {
        "name": "equal_mass_moment_exchange",
        "left_type": "localized_charge",
        "right_type": "arriving_reservoir",
        "output_types": {"left": "moving_output", "right": "spent_reservoir"},
        "assignments": assignments,
        "invariants": [
            {
                "name": "total_second_moment",
                "expression": _operation("add", _second_moment("left"), _second_moment("right")),
            }
        ],
    }


def _retire_probe_rule(fields):
    return {
        "name": "record_completed_contact",
        "left_type": "spent_reservoir",
        "right_type": "contact_probe",
        "output_types": {"left": "stored_recoil", "right": "retired_probe"},
        "assignments": [
            {"side": side, "field": name, "expression": _field(name, side)}
            for side in ("left", "right")
            for name in fields
        ],
        "invariants": [
            {
                "name": "retained_second_moment",
                "expression": _operation("add", _second_moment("left"), _second_moment("right")),
            }
        ],
    }


def configuration(axis=0, sign=1, reservoir=True, normal_budget=10000, link_ticks=1):
    """Return the same finite candidate oriented along any signed lattice axis.

    Mean momentum has 300 units per unit mass times c, so the incoming mean of
    three advances at c/100 before computation delay. The unit spread remains
    independent local payload. The swap moves uncertainty to the other equal-mass
    record instead of deleting it. The same local cycle retires the one-shot
    detector, preserving its complete payload alongside the stored recoil.
    This first conversion contract excludes spatial emission and field response.
    """
    if type(axis) is not int or axis not in (0, 1, 2):
        raise ValueError("axis must be 0, 1 or 2")
    if type(sign) is not int or sign not in (-1, 1):
        raise ValueError("sign must be -1 or 1")
    if type(reservoir) is not bool:
        raise ValueError("reservoir must be a boolean")
    if type(normal_budget) is not int or normal_budget < 1:
        raise ValueError("normal_budget must be a positive integer")
    if type(link_ticks) is not int or not 1 <= link_ticks <= 16:
        raise ValueError("link_ticks must be between 1 and 16 for the bounded phase schedule")

    raw = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    raw["schema_version"] = 1
    raw["model_id"] = "localized-equal-mass-moment-exchange-candidate-v1"
    raw["normal_budget"] = normal_budget
    raw["link_ticks"] = link_ticks
    raw["ticks"] = 800 * link_ticks
    raw.pop("spatial_fields")
    raw.pop("emissions")
    raw["fields"] = [field for field in raw["fields"] if field["name"] != "electric_signal"]
    for domain in raw["event_program"]["domains"]:
        domain["phases"] = [
            operation
            for phase in domain["phases"]
            for operation in [*[[] for _ in range(link_ticks - 1)], phase]
        ]
    raw["fields"].extend(
        [
            {
                "name": "coarse_momentum",
                "components": 3,
                "units": "mean momentum; 300 units = one mass unit times c",
                "signed": True,
                "conserved": True,
            },
            {
                "name": "momentum_spread",
                "components": 1,
                "units": "trace of momentum covariance in squared momentum units",
                "signed": False,
                "conserved": True,
            },
        ]
    )
    for kind in raw["disturbance_types"][:2]:
        kind["fields"].extend(["coarse_momentum", "momentum_spread"])
        kind["defaults"].update(coarse_momentum=[0, 0, 0], momentum_spread=1)
    raw["disturbance_types"][2]["fields"] = list(raw["disturbance_types"][1]["fields"])

    incoming = deepcopy(raw["disturbance_types"][1])
    incoming["name"] = "arriving_reservoir"
    incoming["defaults"].update(
        charge=0, momentum_known=1, coarse_momentum=[3 * sign, 0, 0], momentum_spread=0
    )
    incoming["transport"] = {
        "mode": "move",
        "direction_field": "coarse_momentum",
        "rate": _operation("sum", _operation("abs", {"field": "coarse_momentum"})),
        "rate_denominator": 300,
    }
    raw["disturbance_types"].append(incoming)
    for name in ("moving_output", "spent_reservoir"):
        kind = deepcopy(incoming)
        kind["name"] = name
        raw["disturbance_types"].append(kind)
    stored = deepcopy(incoming)
    stored["name"] = "stored_recoil"
    stored["transport"] = {"mode": "hold"}
    retired = deepcopy(raw["disturbance_types"][2])
    retired["name"] = "retired_probe"
    raw["disturbance_types"].extend([stored, retired])
    raw["interactions"] = [
        _exchange_rule(incoming["fields"]),
        _retire_probe_rule(incoming["fields"]),
    ]
    if reservoir:
        raw["seeds"].append({"position": [0 if sign > 0 else 6, 1, 1], "type": "arriving_reservoir"})

    # Both signs travel three Links to the same capture Node. Three arrivals
    # complete the existing cyclic routing phase for a direction of magnitude 3.
    # Permutation changes the geometry and vector data, not the local law.
    raw["shape"][0], raw["shape"][axis] = raw["shape"][axis], raw["shape"][0]
    positions = [seed["position"] for seed in raw["seeds"]]
    positions.extend(raw["event_program"]["addresses"])
    for position in positions:
        position[0], position[axis] = position[axis], position[0]
    for kind in raw["disturbance_types"]:
        mean = kind["defaults"].get("coarse_momentum")
        if mean is not None:
            mean[0], mean[axis] = mean[axis], mean[0]
        expected_mass = 0 if kind["name"] in ("contact_probe", "retired_probe") else 1
        kind["checks"] = [
            {
                "name": "candidate_mass_scope",
                "expression": _operation(
                    "sub", 1, _operation("abs", _operation("sub", {"field": "mass"}, expected_mass))
                ),
            }
        ]
        if expected_mass:
            kind["checks"].append(
                {
                    "name": "momentum_validity_matches_spread",
                    "expression": _operation(
                        "sub",
                        1,
                        _operation(
                            "abs",
                            _operation(
                                "sub",
                                {"field": "momentum_known"},
                                _operation("sub", 1, _operation("gt", {"field": "momentum_spread"}, 0)),
                            ),
                        ),
                    ),
                }
            )
        else:
            kind["checks"].append(
                {
                    "name": "probe_has_no_kinetic_moments",
                    "expression": _operation("sub", 1, _second_moment("left")),
                }
            )
    return raw
