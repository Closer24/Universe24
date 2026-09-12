"""A fixed, data-only JSON codec for checkpoint records owned by this runtime.

Record names select only this explicit registry. They never name an import,
Python expression, callback or constructor outside the allowlist.
"""

import json
from annotationlib import Format
from dataclasses import fields, is_dataclass
from functools import cache
from types import UnionType
from typing import Any, get_args, get_origin, get_type_hints

from event_universe.core import disturbance_state as d
from event_universe.core import spatial_state as s
from event_universe.core import unit_state as u
from event_universe.core.event_space import CausalEvent
from event_universe.quantum import event_network as q
from event_universe.quantum import event_rules as r
from event_universe.quantum.mixed import DensityState
from event_universe.quantum.state import Amplitude

RECORDS: tuple[type[Any], ...] = (
    d.PortTopology,
    d.FieldDefinition,
    d.Expression,
    d.UpdateRule,
    d.TransportDefinition,
    d.DisturbanceDefinition,
    d.CouplingDefinition,
    d.Assignment,
    d.Invariant,
    d.InteractionDefinition,
    d.OperationCosts,
    d.DisturbanceRecord,
    d.Seed,
    d.InitialState,
    d.DirectionalDelayDefinition,
    d.Departure,
    d.LocalPlan,
    d.PendingCycle,
    d.Packet,
    d.DisturbanceCell,
    s.DecayDefinition,
    s.SpatialFieldDefinition,
    s.FieldGroupDefinition,
    s.FieldAssignment,
    s.NodeFieldRuleDefinition,
    s.SpatialInteractionDefinition,
    s.FieldInteractionGuard,
    s.EmissionDefinition,
    s.SpatialCouplingDefinition,
    s.SpatialSeed,
    s.SpatialState,
    s.SpatialCell,
    s.SpatialPacket,
    u.UnitDefinition,
    u.UnitSystem,
    CausalEvent,
    Amplitude,
    DensityState,
    q.QuantumPayload,
    q.EventDecision,
    q.NetworkRecord,
    r.LocalInstrument,
    r.GroupedInstrument,
)
REGISTRY = {record.__name__: record for record in RECORDS}
MAX_DEPTH = 256
MAX_ITEMS = 2_000_000
MAX_STRING = 8_000_000
MAX_INTEGER = (1 << 256) - 1


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _names(record: type[Any]) -> tuple[str, ...]:
    return (
        tuple(field.name for field in fields(record)) if is_dataclass(record) else tuple(record._fields)
    )


@cache
def _hints(name: str) -> dict[str, Any]:
    # Only trusted annotations from the fixed registry are resolved here.
    namespace = {**vars(d), **vars(s), **vars(u), **vars(r), **vars(q), "Amplitude": Amplitude}
    return get_type_hints(REGISTRY[name], globalns=namespace, format=Format.FORWARDREF)


def matches(value: Any, annotation: Any) -> bool:
    origin, args = get_origin(annotation), get_args(annotation)
    if annotation is Any:
        return True
    if origin is UnionType:
        return any(matches(value, item) for item in args)
    if origin is tuple:
        if type(value) is not tuple:
            return False
        if len(args) == 2 and args[1] is Ellipsis:
            return all(matches(item, args[0]) for item in value)
        return len(value) == len(args) and all(
            matches(item, kind) for item, kind in zip(value, args, strict=False)
        )
    if origin in (list, set, frozenset):
        return type(value) is origin and all(matches(item, args[0]) for item in value)
    if origin is dict:
        return type(value) is dict and all(
            matches(k, args[0]) and matches(v, args[1]) for k, v in value.items()
        )
    return type(value) is annotation


def encode(value: Any, depth: int = 0) -> Any:
    if depth > MAX_DEPTH:
        raise ValueError("checkpoint exceeds nesting limit")
    kind = type(value)
    if value is None or kind is bool:
        return value
    if kind is int:
        if abs(value) > MAX_INTEGER:
            raise ValueError("checkpoint integer exceeds host serialization bound")
        return value
    if kind is str:
        if len(value) > MAX_STRING:
            raise ValueError("checkpoint string exceeds capacity")
        return value
    if kind in RECORDS:
        names = _names(kind)
        if any(not matches(getattr(value, name), _hints(kind.__name__)[name]) for name in names):
            raise ValueError(f"checkpoint {kind.__name__} has invalid typed fields")
        return {
            "kind": "record",
            "type": kind.__name__,
            "values": [encode(getattr(value, name), depth + 1) for name in names],
        }
    if kind in (tuple, list, set, frozenset):
        if len(value) > MAX_ITEMS:
            raise ValueError("checkpoint container exceeds capacity")
        items = [encode(item, depth + 1) for item in value]
        if kind in (set, frozenset):
            items.sort(key=canonical)
        return {"kind": kind.__name__, "items": items}
    if kind is dict:
        if len(value) > MAX_ITEMS:
            raise ValueError("checkpoint mapping exceeds capacity")
        return {
            "kind": "dict",
            "items": [[encode(k, depth + 1), encode(v, depth + 1)] for k, v in value.items()],
        }
    raise ValueError(f"unsupported checkpoint value type: {kind.__name__}")


def decode(value: Any, depth: int = 0, budget: list[int] | None = None) -> Any:
    if budget is None:
        budget = [MAX_ITEMS]
    budget[0] -= 1
    if depth > MAX_DEPTH or budget[0] < 0:
        raise ValueError("checkpoint decoded structure exceeds capacity")
    if value is None or type(value) in (bool, int, str):
        return encode(value)
    if type(value) is not dict:
        raise ValueError("checkpoint container needs an explicit known kind")
    if value.get("kind") == "record":
        if set(value) != {"kind", "type", "values"} or type(value["type"]) is not str:
            raise ValueError("invalid checkpoint record envelope")
        record = REGISTRY.get(value["type"])
        if record is None:
            raise ValueError("unknown checkpoint record type")
        raw = value["values"]
        names = _names(record)
        if type(raw) is not list or len(raw) != len(names):
            raise ValueError("checkpoint record fields do not match this runtime")
        values = [decode(item, depth + 1, budget) for item in raw]
        if any(
            not matches(item, _hints(record.__name__)[name])
            for name, item in zip(names, values, strict=True)
        ):
            raise ValueError("checkpoint record has incompatible typed fields")
        return record(**dict(zip(names, values, strict=False)))
    if set(value) != {"kind", "items"} or type(value["items"]) is not list:
        raise ValueError("invalid checkpoint container envelope")
    items = value["items"]
    if value["kind"] == "dict":
        result: dict[Any, Any] = {}
        for pair in items:
            if type(pair) is not list or len(pair) != 2:
                raise ValueError("checkpoint mapping requires key/value pairs")
            key, item = (decode(entry, depth + 1, budget) for entry in pair)
            if key in result:
                raise ValueError("duplicate checkpoint mapping key")
            result[key] = item
        return result
    if type(value["kind"]) is not str:
        raise ValueError("checkpoint container kind must be a string")
    constructors = {"list": list, "tuple": tuple, "set": set, "frozenset": frozenset}
    constructor = constructors.get(value["kind"])
    if constructor is None:
        raise ValueError("unknown checkpoint container kind")
    sequence = constructor(decode(item, depth + 1, budget) for item in items)
    if len(sequence) != len(items):
        raise ValueError("duplicate checkpoint set item")
    return sequence
