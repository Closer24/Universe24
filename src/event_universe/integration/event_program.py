"""Strict initialization data for the opt-in native local event resolver.

The generic state carries an immutable serialized program, never executable
callbacks. This owner validates payloads; the physical scheduler stays neutral.
"""

import json
from dataclasses import dataclass

from event_universe.core.disturbance_state import Address3, InitialState
from event_universe.initialization import _address, _array, _index, _integer, _object, _text
from event_universe.quantum import Amplitude, EventNetworkConfig, LocalInstrument, LocalUnitary
from event_universe.quantum.event_rules import Matrix


@dataclass(frozen=True, slots=True)
class Binding:
    address: Address3
    site: int
    types: tuple[int, ...]
    field: int
    codes: tuple[int, ...]
    instrument: LocalInstrument


@dataclass(frozen=True, slots=True)
class Program:
    capacity: int
    network: EventNetworkConfig | None
    layers: tuple[tuple[int, tuple[tuple[LocalUnitary, tuple[int, ...]], ...]], ...]
    bindings: tuple[Binding, ...]
    seed: int
    tickets: tuple[int, ...] | None


def _matrix(value: object) -> Matrix:
    rows = _array(value, "matrix", 4, 2)
    if len(rows) not in (2, 4):
        raise ValueError("matrix must be two or four dimensional")
    result = []
    for row in rows:
        values = []
        for value in _array(row, "matrix row", len(rows), len(rows)):
            if type(value) is int:
                values.append(Amplitude(_integer(value, "coefficient"), 0))
            else:
                pair = _array(value, "complex integer pair", 2, 2)
                values.append(Amplitude(*(_integer(v, "coefficient") for v in pair)))
        result.append(tuple(values))
    return tuple(result)


def parse_event_program(initial: InitialState) -> Program:
    if initial.event_program is None or len(initial.event_program) > 1_000_000:
        raise ValueError("bounded event program required")
    obj = _object(
        json.loads(initial.event_program),
        "event program",
        {
            "model",
            "capacity",
            "addresses",
            "occupied",
            "layers",
            "bindings",
            "seed",
            "tickets",
            "bounds",
        },
        {"model", "capacity"},
    )
    model = _text(obj["model"], "event program model")
    capacity = _integer(obj["capacity"], "event capacity", 1)
    if initial.spatial_fields:
        raise ValueError("native event program v1 does not yet bind independent spatial-field clocks")
    if model == "causal-events-v1":
        _object(obj, "causal program", {"model", "capacity"}, {"model", "capacity"})
        return Program(capacity, None, (), (), 0, None)
    if model != "local-quantum-events-v1":
        raise ValueError("unknown event program model")
    addresses = tuple(
        _address(a, "quantum address", 0) for a in _array(obj.get("addresses"), "addresses", 30, 1)
    )
    for address in addresses:
        if any(v >= n for v, n in zip(address, initial.shape, strict=True)):
            raise ValueError("quantum address outside physical domain")
    occupied = tuple(
        _integer(q, "occupied site", 0) for q in _array(obj.get("occupied", []), "occupied", 30)
    )
    bounds = _object(
        obj.get("bounds", {}),
        "quantum bounds",
        {"max_nodes", "max_eval_nodes", "max_terms", "max_records"},
        set(),
    )
    network = EventNetworkConfig(
        addresses,
        occupied,
        max_nodes=_integer(bounds.get("max_nodes", 10000), "max_nodes", 1),
        max_eval_nodes=_integer(bounds.get("max_eval_nodes", 10000), "max_eval_nodes", 1),
        max_terms=_integer(bounds.get("max_terms", 4096), "max_terms", 1),
        max_records=_integer(bounds.get("max_records", 1024), "max_records", 1),
    )
    layers = []
    prior_tick = 0
    for raw in _array(obj.get("layers", []), "layers", 4096):
        layer = _object(raw, "layer", {"tick", "operations"}, {"tick", "operations"})
        tick = _integer(layer["tick"], "layer tick", 1)
        if tick <= prior_tick:
            raise ValueError("layers must have strictly increasing ticks")
        prior_tick = tick
        used: set[int] = set()
        operations = []
        for raw_op in _array(layer["operations"], "operations", 30, 1):
            op = _object(raw_op, "operation", {"sites", "matrix"}, {"sites", "matrix"})
            sites = tuple(
                _integer(q, "operation site", 0) for q in _array(op["sites"], "operation sites", 2, 1)
            )
            if any(q >= len(addresses) or q in used for q in sites) or len(set(sites)) != len(sites):
                raise ValueError("overlapping or invalid operation sites")
            used.update(sites)
            rule = LocalUnitary(_matrix(op["matrix"]))
            if len(rule.matrix) != 1 << len(sites):
                raise ValueError("matrix dimension disagrees with operation support")
            if (
                len(sites) == 2
                and sum(
                    abs(a - b) for a, b in zip(addresses[sites[0]], addresses[sites[1]], strict=True)
                )
                != 1
            ):
                raise ValueError("quantum operations require cardinal nearest neighbors")
            operations.append((rule, sites))
        layers.append((tick, tuple(operations)))
    names = {kind.name: q for q, kind in enumerate(initial.disturbances)}
    field_names = {field.name: q for q, field in enumerate(initial.fields)}
    bindings = []
    bound: set[Address3] = set()
    for raw in _array(obj.get("bindings", []), "bindings", 30):
        b = _object(
            raw,
            "binding",
            {"address", "types", "field", "codes", "instrument"},
            {"address", "types", "field", "codes", "instrument"},
        )
        address = _address(b["address"], "binding address", 0)
        if address not in addresses or address in bound:
            raise ValueError("one local binding per configured quantum address required")
        bound.add(address)
        types = tuple(
            _index(t, names, "binding type") for t in _array(b["types"], "binding types", 2, 1)
        )
        field = _index(b["field"], field_names, "binding field")
        definition = initial.fields[field]
        if definition.components != 1 or definition.conserved or definition.extensive:
            raise ValueError("outcome field must be a nonconserved nonextensive scalar")
        if any(
            field not in initial.disturbances[t].fields or initial.disturbances[t].cost_field == field
            for t in types
        ):
            raise ValueError("every participant must own a separate outcome field")
        instrument = LocalInstrument(
            tuple(_matrix(m) for m in _array(b["instrument"], "instrument", 4, 1))
        )
        codes = tuple(
            _integer(c, "outcome code")
            for c in _array(b["codes"], "codes", len(instrument.branches), len(instrument.branches))
        )
        if not definition.signed and any(c < 0 for c in codes):
            raise ValueError("negative code for unsigned outcome field")
        bindings.append(Binding(address, addresses.index(address), types, field, codes, instrument))
    tickets = (
        None
        if "tickets" not in obj
        else tuple(_integer(t, "ticket", 0) for t in _array(obj["tickets"], "tickets", 1024))
    )
    return Program(
        capacity,
        network,
        tuple(layers),
        tuple(bindings),
        _integer(obj.get("seed", 0), "seed", 0),
        tickets,
    )
