"""Build an opt-in transverse population reflection and one-link streaming world.

This module creates ordinary initialization data. It is not a physical runtime,
and it never measures neighboring values or supplies derivatives to the engine.
The candidate has six transverse vector populations and no physical carriers.
Their locally summed vector and direction-cross-vector sum are the two measured
field moments. Reflection preserves those moments and the population norm.

All runs use the same amplitude scale. The initial projection divides by four;
each subsequent reflection can consume one additional binary factor. The
eighteen-step limit is a finite exact-arithmetic budget, not a general solution
for bounded integer evolution at arbitrarily late times. The existing engine
also checks every intermediate and payload bound while a run evolves.
"""

from collections.abc import Iterable
from functools import reduce

from event_universe.core.disturbance_state import OPERATIONS, bounded
from event_universe.core.integer import checked_work

type Vector = tuple[int, int, int]
type MomentSeed = tuple[Vector, Vector, Vector]
type Expression = int | list[int] | dict[str, object]

DIRECTIONS: tuple[Vector, ...] = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)
NAMES = (
    "amplitude_positive_x",
    "amplitude_negative_x",
    "amplitude_positive_y",
    "amplitude_negative_y",
    "amplitude_positive_z",
    "amplitude_negative_z",
)
AMPLITUDE_SCALE = 1 << 20
MAX_EXACT_TICKS = 18


def _operation(name: str, *arguments: Expression) -> dict[str, object]:
    return {"op": name, "args": list(arguments)}


def _sum(expressions: Iterable[Expression]) -> Expression:
    return reduce(lambda left, right: _operation("add", left, right), expressions)


def _retained(name: str) -> dict[str, object]:
    return {"field": name, "side": "right"}


def _owned(name: str, port: int) -> Expression:
    # Only this port is ever written for this field. Every other output is zero.
    return _operation("add", _retained(name), {"outgoing": name, "port": port})


def _invariants(*, include_outgoing: bool) -> list[dict[str, object]]:
    populations = [
        _owned(name, port) if include_outgoing else _retained(name) for port, name in enumerate(NAMES)
    ]
    norm_terms = []
    for port, name in enumerate(NAMES):
        retained = _retained(name)
        squared = _operation("dot", retained, retained)
        if include_outgoing:
            outgoing = {"outgoing": name, "port": port}
            squared = _operation("add", squared, _operation("dot", outgoing, outgoing))
        norm_terms.append(squared)
    return [
        {"name": "electric_moment", "expression": _sum(populations)},
        {
            "name": "magnetic_moment",
            "expression": _sum(
                _operation("cross", list(direction), population)
                for direction, population in zip(DIRECTIONS, populations, strict=True)
            ),
        },
        {
            "name": "population_squared_amplitude",
            "expression": _sum(norm_terms),
        },
        *[
            {
                "name": f"transverse_{name}",
                "expression": _operation("dot", list(direction), population),
            }
            for name, direction, population in zip(NAMES, DIRECTIONS, populations, strict=True)
        ],
    ]


def _reflection_rule() -> dict[str, object]:
    electric = _sum(_retained(name) for name in NAMES)
    magnetic = _sum(
        _operation("cross", list(direction), _retained(name))
        for name, direction in zip(NAMES, DIRECTIONS, strict=True)
    )
    assignments = []
    for name, direction in zip(NAMES, DIRECTIONS, strict=True):
        normal = list(direction)
        transverse = _operation(
            "neg", _operation("cross", normal, _operation("cross", normal, electric))
        )
        reflected = _operation(
            "sub",
            _operation(
                "exact_div",
                _operation("sub", transverse, _operation("cross", normal, magnetic)),
                2,
            ),
            _retained(name),
        )
        assignments.append({"field": name, "expression": reflected})
    return {
        "name": "reflect_about_local_moment_projection",
        "assignments": assignments,
        "invariants": _invariants(include_outgoing=False),
    }


def _streaming_rule() -> dict[str, object]:
    assignments = []
    for port, name in enumerate(NAMES):
        assignments.extend(
            [
                {"field": name, "expression": [0, 0, 0]},
                {"field": name, "port": port, "expression": _retained(name)},
            ]
        )
    return {
        "name": "transfer_each_population_to_its_directional_link",
        "assignments": assignments,
        "invariants": _invariants(include_outgoing=True),
    }


def _cross(left: Vector, right: Vector) -> Vector:
    return (
        checked_work(left[1] * right[2] - left[2] * right[1]),
        checked_work(left[2] * right[0] - left[0] * right[2]),
        checked_work(left[0] * right[1] - left[1] * right[0]),
    )


def _vector(value: Vector, label: str) -> Vector:
    if len(value) != 3 or any(type(component) is not int for component in value):
        raise ValueError(f"{label} must contain exactly three integers")
    return tuple(bounded(component) for component in value)


def project_moments(electric: Vector, magnetic: Vector) -> tuple[Vector, ...]:
    """Initialize equilibrium populations from unscaled integer moment coefficients.

    No rounding is permitted. Scaling and the orthogonal projection happen only
    while constructing initial data; no macroscopic measurements feed back into
    an evolving run. The returned populations contain raw fixed-scale integers.
    """
    electric = tuple(bounded(value * AMPLITUDE_SCALE) for value in _vector(electric, "electric"))
    magnetic = tuple(bounded(value * AMPLITUDE_SCALE) for value in _vector(magnetic, "magnetic"))
    populations = []
    squared_amplitude = 0
    for normal in DIRECTIONS:
        transverse = tuple(-value for value in _cross(normal, _cross(normal, electric)))
        magnetic_cross = _cross(normal, magnetic)
        numerator = tuple(
            checked_work(first - second)
            for first, second in zip(transverse, magnetic_cross, strict=True)
        )
        if any(value % 4 for value in numerator):
            raise ValueError("initial moment projection requires exact division by four")
        population = tuple(bounded(value // 4) for value in numerator)
        squared_amplitude = checked_work(
            squared_amplitude + sum(checked_work(value * value) for value in population)
        )
        populations.append(population)
    return tuple(populations)


def build_configuration(
    shape: Vector,
    ticks: int,
    moments: Iterable[MomentSeed],
    *,
    scatter_enabled: bool = True,
    boundary: str = "periodic",
) -> dict[str, object]:
    """Build six-field local JSON data with fixed precision and no runtime callbacks.

    Each moment seed is ``(position, electric, magnetic)``. The two field vectors
    are integer coefficients before multiplication by ``AMPLITUDE_SCALE``.
    Positions are unique and inside the supplied three-dimensional shape.
    The negative control omits reflection and preserves the same seed and scale.
    """
    shape = _vector(shape, "shape")
    if any(length < 1 for length in shape):
        raise ValueError("shape must contain positive extents")
    if type(ticks) is not int or not 0 <= ticks <= MAX_EXACT_TICKS:
        raise ValueError(f"ticks must be an integer from zero through {MAX_EXACT_TICKS}")
    if type(scatter_enabled) is not bool:
        raise ValueError("scatter_enabled must be a boolean")
    if boundary not in ("periodic", "open"):
        raise ValueError("boundary must be periodic or open")
    seeds = []
    positions: set[Vector] = set()
    for position, electric, magnetic in moments:
        position = _vector(position, "position")
        if any(not 0 <= value < extent for value, extent in zip(position, shape, strict=True)):
            raise ValueError("moment seed position is outside the shape")
        if position in positions:
            raise ValueError("moment seed positions must be unique")
        positions.add(position)
        for name, population in zip(NAMES, project_moments(electric, magnetic), strict=True):
            if any(population):
                seeds.append(
                    {
                        "position": list(position),
                        "field": name,
                        "populations": [list(population), *[[0, 0, 0] for _ in range(7)]],
                    }
                )
    mode = "reflection" if scatter_enabled else "streaming-control"
    return {
        "schema_version": 1,
        "model_id": f"transverse-six-port-{mode}-v1",
        "shape": list(shape),
        "boundary": boundary,
        "slots_per_node": 1,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "fields": [
            {
                "name": name,
                "components": 3,
                "units": "normalized vector amplitude",
                "signed": True,
                "conserved": False,
                "scale": AMPLITUDE_SCALE,
            }
            for name in NAMES
        ],
        "field_groups": [{"name": "transverse_population_field", "fields": list(NAMES)}],
        "disturbance_types": [
            {"name": "unused_held_carrier", "fields": list(NAMES), "transport": {"mode": "hold"}}
        ],
        "seeds": [],
        "spatial_fields": [
            {"field": name, "baseline": [0, 0, 0], "transport": "local"} for name in NAMES
        ],
        "spatial_seeds": seeds,
        "field_rules": ([_reflection_rule()] if scatter_enabled else []) + [_streaming_rule()],
    }
