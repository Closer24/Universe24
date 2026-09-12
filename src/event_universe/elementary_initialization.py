"""Compile a closed, formula-free JSON vocabulary into the shared runtime records."""

from .core.disturbance_state import (
    MAX_FIELDS,
    MAX_RULES,
    MAX_SLOTS,
    OPERATIONS,
    InitialState,
    OperationCosts,
    pack,
)
from .core.elementary_contract import validate_elementary
from .core.spatial_state import ElementaryExchange, SpatialFieldDefinition
from .initialization import (
    _address,
    _allowance,
    _array,
    _boolean,
    _decay,
    _disturbances,
    _emissions,
    _field_groups,
    _fields,
    _index,
    _integer,
    _names,
    _object,
    _payload,
    _seeds,
    _spatial_seeds,
    _text,
)
from .observer_configuration import ObserverDefinition


def parse_elementary(document: object) -> InitialState:
    required = {
        "schema_version",
        "model_id",
        "shape",
        "slots_per_cell",
        "link_ticks",
        "normal_budget",
        "ticks",
        "operation_costs",
        "fields",
        "disturbance_types",
        "seeds",
    }
    obj = _object(
        document,
        "elementary initialization",
        required
        | {
            "boundary",
            "spatial_fields",
            "spatial_seeds",
            "emissions",
            "exchanges",
            "field_groups",
            "observer",
        },
        required,
    )
    if _integer(obj["schema_version"], "schema_version") != 3:
        raise ValueError("ordinary initialization requires elementary schema_version 3")
    fields = _fields(obj["fields"])
    # Reject expression-bearing keys even when they are empty or renamed elsewhere.
    for raw in _array(obj["disturbance_types"], "disturbance_types", 16, 1):
        kind = _object(
            raw,
            "elementary disturbance",
            {"name", "fields", "defaults", "transport", "cost_field"},
            {"name", "fields", "transport"},
        )
        transport = _object(
            kind["transport"],
            "elementary transport",
            {"mode", "weights", "direction_field", "rate", "rate_denominator", "routing"},
            {"mode"},
        )
        if "rate" in transport:
            _integer(transport["rate"], "elementary transport rate", 0)
    disturbances = _disturbances(obj["disturbance_types"], fields)
    names = _names(fields)
    spatial: list[SpatialFieldDefinition] = []
    for raw in _array(obj.get("spatial_fields", []), "spatial_fields", MAX_FIELDS):
        field_obj = _object(
            raw,
            "elementary spatial field",
            {"field", "baseline", "routing_weights", "computation_delay", "decay"},
            {"field", "routing_weights", "computation_delay", "decay"},
        )
        index = _index(field_obj["field"], names, "spatial field")
        if any(d.field == index for d in spatial):
            raise ValueError("duplicate elementary spatial field")
        field = fields[index]
        spatial.append(
            SpatialFieldDefinition(
                field=index,
                baseline=_payload(field_obj["baseline"], field)
                if "baseline" in field_obj
                else pack((0,) * field.components),
                decay=_decay(field_obj["decay"]),
                transport="local",
                computation_delay=_boolean(field_obj["computation_delay"], "computation_delay"),
                routing_weights=tuple(
                    _integer(v, "routing weight", 0)
                    for v in _array(field_obj["routing_weights"], "routing_weights", 6, 6)
                ),
            )
        )
    exchanges = []
    for raw in _array(obj.get("exchanges", []), "exchanges", MAX_RULES):
        rule = _object(
            raw,
            "elementary exchange",
            {"name", "type", "field", "components", "budget"},
            {"name", "type", "field", "budget"},
        )
        index = _index(rule["field"], names, "exchange field")
        field = fields[index]
        exchanges.append(
            ElementaryExchange(
                _text(rule["name"], "exchange name"),
                _index(rule["type"], _names(disturbances), "exchange type"),
                index,
                tuple(
                    _integer(c, "exchange component", 0)
                    for c in _array(
                        rule.get("components", list(range(field.components))),
                        "components",
                        field.components,
                        1,
                    )
                ),
                _allowance(rule["budget"], field, "exchange budget"),
            )
        )
    # Emission amounts are leaves only; expressions cannot smuggle a response through a source.
    for raw in _array(obj.get("emissions", []), "emissions", MAX_RULES):
        emission = _object(
            raw,
            "elementary emission",
            {"type", "field", "amount", "source", "denominator", "budget"},
            {"type", "field", "amount", "source", "budget"},
        )
        amount = emission["amount"]
        if isinstance(amount, dict):
            _object(amount, "elementary emission amount", {"field"}, {"field"})
    spatial_fields = tuple(spatial)
    shape = _address(obj["shape"], "shape", 1)
    if "observer" in obj:
        ObserverDefinition.parse(obj["observer"], shape)
    capacity = _integer(obj["slots_per_cell"], "slots_per_cell", 1)
    if capacity > MAX_SLOTS:
        raise ValueError("elementary resident capacity exceeded")
    costs = _object(obj["operation_costs"], "operation_costs", set(OPERATIONS), set(OPERATIONS))
    initial = InitialState(
        model_id=_text(obj["model_id"], "model_id"),
        shape=shape,
        slots_per_cell=capacity,
        link_ticks=_integer(obj["link_ticks"], "link_ticks", 1),
        normal_budget=_integer(obj["normal_budget"], "normal_budget", 1),
        ticks=_integer(obj["ticks"], "ticks", 0),
        fields=fields,
        disturbances=disturbances,
        couplings=(),
        operation_costs=OperationCosts(
            tuple(_integer(costs[name], f"cost of {name}", 1) for name in OPERATIONS)
        ),
        seeds=_seeds(obj["seeds"], fields, disturbances, shape, capacity),
        spatial_fields=spatial_fields,
        emissions=_emissions(obj.get("emissions", []), fields, disturbances, spatial_fields, 2),
        spatial_seeds=_spatial_seeds(obj.get("spatial_seeds", []), fields, spatial_fields, shape),
        schema_version=3,
        boundary=_text(obj.get("boundary", "periodic"), "boundary"),
        field_groups=_field_groups(obj.get("field_groups", []), fields),
        elementary_exchanges=tuple(exchanges),
    )
    if initial.boundary not in ("periodic", "open"):
        raise ValueError("boundary must be periodic or open")
    validate_elementary(initial)
    return initial
