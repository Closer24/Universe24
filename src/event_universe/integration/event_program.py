"""Strict initialization data for the opt-in native local event resolver.

The generic state carries an immutable serialized program, never executable
callbacks. This owner validates payloads; the physical scheduler stays neutral.
"""

import json
from dataclasses import dataclass

from event_universe.core.disturbance_state import Address3, InitialState
from event_universe.initialization import _address, _array, _index, _integer, _object, _text
from event_universe.quantum import Amplitude, EventNetworkConfig, LocalInstrument, LocalUnitary
from event_universe.quantum.event_network import Instrument, LocalOperation
from event_universe.quantum.event_rules import GroupedInstrument, LocalChannel, Matrix, outcome_groups


@dataclass(frozen=True, slots=True)
class Binding:
    address: Address3
    register_index: int
    types: tuple[int, ...]
    field: int
    codes: tuple[int, ...]
    instrument: Instrument


@dataclass(frozen=True, slots=True)
class Program:
    capacity: int
    network: EventNetworkConfig | None
    layers: tuple[tuple[int, tuple[tuple[LocalOperation, tuple[int, ...]], ...]], ...]
    bindings: tuple[Binding, ...]
    seed: int
    tickets: tuple[int, ...] | None


def _matrix(value: object) -> Matrix:
    rows = _array(value, "matrix", 16, 2)
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


def _require_initial_capacity(initial: InitialState, capacity: int, quantum_sources: int = 0) -> None:
    """Check the deterministic startup requirement without allocating event state."""
    # Carrier and field owners each record one source per seeded node.
    required = (
        len({seed.position for seed in initial.seeds})
        + len({seed.position for seed in initial.spatial_seeds})
        + quantum_sources
    )
    if required > capacity:
        raise ValueError(f"initial sources require {required} events but event capacity is {capacity}")


def parse_event_program(initial: InitialState) -> Program:
    if initial.event_program is None or len(initial.event_program) > 1_000_000:
        raise ValueError("bounded event program required")
    if initial.conservation is not None:
        raise ValueError("conservation audit does not support native event programs")
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
            "dimensions",
            "initial_levels",
            "register_names",
        },
        {"model", "capacity"},
    )
    model = _text(obj["model"], "event program model")
    capacity = _integer(obj["capacity"], "event capacity", 1)
    if model == "causal-events-v1":
        _object(obj, "causal program", {"model", "capacity"}, {"model", "capacity"})
        _require_initial_capacity(initial, capacity)
        return Program(capacity, None, (), (), 0, None)
    if initial.spatial_fields:
        raise ValueError("native quantum program does not yet bind independent spatial-field clocks")
    if model not in ("local-quantum-events-v1", "local-quantum-events-v2"):
        raise ValueError("unknown event program model")
    v2 = model == "local-quantum-events-v2"
    if not v2 and {"dimensions", "initial_levels", "register_names"} & obj.keys():
        raise ValueError("register definitions require local-quantum-events-v2")
    addresses = tuple(
        _address(a, "quantum address", 0) for a in _array(obj.get("addresses"), "addresses", 30, 1)
    )
    for address in addresses:
        if any(v >= n for v, n in zip(address, initial.shape, strict=True)):
            raise ValueError("quantum address outside physical domain")
    occupied = tuple(
        _integer(q, "occupied register_index", 0)
        for q in _array(obj.get("occupied", []), "occupied", 30)
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
        dimensions=tuple(
            _integer(d, "dimension", 2) for d in _array(obj.get("dimensions", []), "dimensions", 30)
        ),
        initial_levels=tuple(
            _integer(d, "initial level", 0)
            for d in _array(obj.get("initial_levels", []), "initial_levels", 30)
        ),
        register_names=tuple(
            _text(n, "register name")
            for n in _array(obj.get("register_names", []), "register_names", 30)
        ),
    )
    _require_initial_capacity(initial, capacity, len(network.addresses))
    layers = []
    prior_tick = 0
    for raw in _array(obj.get("layers", []), "layers", 4096):
        layer = _object(raw, "layer", {"tick", "operations"}, {"tick", "operations"})
        tick = _integer(layer["tick"], "layer tick", 1)
        if tick <= prior_tick:
            raise ValueError("layers must have strictly increasing ticks")
        prior_tick = tick
        used: set[int] = set()
        operations: list[tuple[LocalOperation, tuple[int, ...]]] = []
        for raw_op in _array(layer["operations"], "operations", 30, 1):
            op = _object(
                raw_op,
                "operation",
                {"register_indices", "matrix", "channel"} if v2 else {"register_indices", "matrix"},
                {"register_indices"},
            )
            if ("matrix" in op) == ("channel" in op):
                raise ValueError("operation must supply exactly one matrix or channel")
            register_indices = tuple(
                _integer(q, "operation register_index", 0)
                for q in _array(op["register_indices"], "operation register_indices", 2, 1)
            )
            if any(q >= len(addresses) or q in used for q in register_indices) or len(
                set(register_indices)
            ) != len(register_indices):
                raise ValueError("overlapping or invalid operation register_indices")
            used.update(register_indices)
            rule: LocalOperation
            if "matrix" in op:
                rule = LocalUnitary(_matrix(op["matrix"]))
                size = len(rule.matrix)
            else:
                rule = LocalChannel(tuple(_matrix(m) for m in _array(op["channel"], "channel", 4, 1)))
                if len(register_indices) != 1:
                    raise ValueError("a local channel acts on one register")
                size = len(rule.kraus[0])
            dimension = 1
            for register_index in register_indices:
                dimension *= network.local_dimensions[register_index]
            if size != dimension:
                raise ValueError("matrix dimension disagrees with operation support")
            if len(register_indices) == 2 and sum(
                abs(a - b)
                for a, b in zip(
                    addresses[register_indices[0]], addresses[register_indices[1]], strict=True
                )
            ) not in ((0, 1) if v2 else (1,)):
                raise ValueError("quantum operations require cardinal nearest neighbors")
            operations.append((rule, register_indices))
        layers.append((tick, tuple(operations)))
    names = {kind.name: q for q, kind in enumerate(initial.disturbances)}
    field_names = {field.name: q for q, field in enumerate(initial.fields)}
    bindings = []
    bound: set[Address3] = set()
    for raw in _array(obj.get("bindings", []), "bindings", 30):
        b = _object(
            raw,
            "binding",
            {"address", "types", "field", "codes", "instrument", "grouped_instrument", "register_index"}
            if v2
            else {"address", "types", "field", "codes", "instrument"},
            {"address", "types", "field", "codes"},
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
        if ("instrument" in b) == ("grouped_instrument" in b):
            raise ValueError("binding requires exactly one instrument definition")
        instrument: Instrument
        if "instrument" in b:
            instrument = LocalInstrument(
                tuple(_matrix(m) for m in _array(b["instrument"], "instrument", 4, 1))
            )
        else:
            instrument = GroupedInstrument(
                tuple(
                    tuple(_matrix(m) for m in _array(group, "unobserved Kraus terms", 4, 1))
                    for group in _array(b["grouped_instrument"], "grouped instrument", 4, 1)
                )
            )
        if "register_index" in b:
            register_index = _integer(b["register_index"], "binding register_index", 0)
            if register_index >= len(addresses) or addresses[register_index] != address:
                raise ValueError("binding register must be at its physical address")
        else:
            if addresses.count(address) != 1:
                raise ValueError("colocated registers require an explicit binding register_index")
            register_index = addresses.index(address)
        groups = outcome_groups(instrument)
        if len(groups[0][0]) != network.local_dimensions[register_index]:
            raise ValueError("instrument dimension disagrees with binding register")
        codes = tuple(
            _integer(c, "outcome code") for c in _array(b["codes"], "codes", len(groups), len(groups))
        )
        if not definition.signed and any(c < 0 for c in codes):
            raise ValueError("negative code for unsigned outcome field")
        bindings.append(Binding(address, register_index, types, field, codes, instrument))
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
