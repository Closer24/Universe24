"""Strict finite contact domains; physical names and local recipes are data."""

from dataclasses import dataclass

from event_universe.core.coupling_selectors import selected_types
from event_universe.core.disturbance_state import DisturbanceRecord, InitialState, unpack
from event_universe.core.topology import neighbor_address
from event_universe.initialization import _address, _array, _index, _integer, _object, _seeds, _text
from event_universe.quantum import EventNetworkConfig, LocalInstrument, LocalUnitary
from event_universe.quantum.contact_rules import (
    preserves_occupation,
    validates_capture,
    validates_preparation,
)
from event_universe.quantum.wave_origins import WaveDefinition

from .event_program import Program, _matrix, _require_initial_capacity


@dataclass(frozen=True, slots=True)
class ContactDomain:
    name: str
    registers: tuple[int, ...]
    source_register: int
    source_type: int
    partner_type: int
    validity_field: int
    unknown_value: int
    preparation: LocalUnitary
    output: DisturbanceRecord
    detector_type: int
    captures: tuple[int, ...]
    instrument: LocalInstrument
    phases: tuple[tuple[tuple[LocalUnitary, tuple[int, ...]], ...], ...]


@dataclass(frozen=True, slots=True)
class ContactConfiguration:
    domains: tuple[ContactDomain, ...]
    causal_sources: bool = False
    null_notices: bool = False


def parse_contact_program(initial: InitialState, raw: object) -> Program:
    if initial.node_execution or initial.spatial_computation_delay or initial.conservation_contract:
        raise ValueError("localized contacts require the fixed spatial clock and ordinary local cycles")
    if initial.slots_per_node < 2:
        raise ValueError("localized contacts require two resident slots")
    obj = _object(
        raw,
        "localized contact program",
        {"model", "capacity", "addresses", "domains", "bounds", "seed", "tickets", "null_notices"},
        {"model", "capacity", "addresses", "domains"},
    )
    causal_sources = obj["model"] == "causal-contact-fields-v1"
    null_notices = obj.get("null_notices", False)
    if type(null_notices) is not bool:
        raise ValueError("null_notices must be true or false")
    if null_notices and not causal_sources:
        raise ValueError("null notices require the causal contact field model")
    if causal_sources and (not initial.spatial_fields or not initial.emissions):
        raise ValueError("causal contact fields require configured spatial sources")
    if causal_sources and any(definition.rays for definition in initial.spatial_fields):
        raise ValueError("causal contact fields currently require octant transport")
    addresses = tuple(
        _address(a, "contact address", 0) for a in _array(obj["addresses"], "contact addresses", 30, 1)
    )
    if len(set(addresses)) != len(addresses) or any(
        any(v >= n for v, n in zip(a, initial.shape, strict=True)) for a in addresses
    ):
        raise ValueError("contact mode addresses must be distinct and inside the domain")
    types = {definition.name: i for i, definition in enumerate(initial.disturbances)}
    fields = {definition.name: i for i, definition in enumerate(initial.fields)}
    domains = []
    used: set[int] = set()
    for raw_domain in _array(obj["domains"], "contact domains", 30, 1):
        d = _object(
            raw_domain,
            "contact domain",
            {"name", "register_indices", "source", "capture", "phases"},
            {"name", "register_indices", "source", "capture", "phases"},
        )
        registers = tuple(
            _integer(q, "domain register", 0)
            for q in _array(d["register_indices"], "domain registers", 30, 1)
        )
        if len(set(registers)) != len(registers) or any(
            q >= len(addresses) or q in used for q in registers
        ):
            raise ValueError("contact domains require disjoint valid registers")
        used.update(registers)
        s = _object(
            d["source"],
            "contact source",
            {"register_index", "type", "partner_type", "validity_field", "unknown_value", "preparation"},
            {"register_index", "type", "partner_type", "validity_field", "unknown_value", "preparation"},
        )
        register = _integer(s["register_index"], "source register", 0)
        if register not in registers:
            raise ValueError("source register must belong to its domain")
        source_type = _index(s["type"], types, "source type")
        partner_type = _index(s["partner_type"], types, "contact partner type")
        validity = _index(s["validity_field"], fields, "validity field")
        f = initial.fields[validity]
        if (
            f.components != 1
            or f.conserved
            or f.extensive
            or validity not in initial.disturbances[source_type].fields
            or validity == initial.disturbances[source_type].cost_field
        ):
            raise ValueError("validity requires a separate owned nonextensive nonconserved scalar")
        unknown = _integer(s["unknown_value"], "unknown marker")
        if not f.signed and unknown < 0:
            raise ValueError("negative marker for unsigned validity field")
        preparation = LocalUnitary(_matrix(s["preparation"]))
        validates_preparation(preparation)
        c = _object(
            d["capture"],
            "contact capture",
            {"register_indices", "detector_type", "output", "instrument"},
            {"register_indices", "detector_type", "output", "instrument"},
        )
        captures = tuple(
            _integer(q, "capture register", 0)
            for q in _array(c["register_indices"], "capture registers", 30)
        )
        if len(set(captures)) != len(captures) or any(q not in registers for q in captures):
            raise ValueError("distinct capture registers must belong to their domain")
        detector = _index(c["detector_type"], types, "detector type")
        output = _object(c["output"], "localized output", {"type", "values"}, {"type"})
        record = _seeds(
            [{**output, "position": list(addresses[register])}],
            initial.fields,
            initial.disturbances,
            initial.shape,
            initial.slots_per_node,
        )[0].record
        kind = initial.disturbances[record.type_index]
        if (
            validity not in kind.fields
            or unpack(record.values[validity]) != (unknown,)
            or kind.transport.mode != "hold"
        ):
            raise ValueError(
                "localized capture must retain undefined momentum and hold until a local rule acts"
            )
        source = initial.disturbances[source_type]
        if any(
            f.conserved and source.defaults[i] != record.values[i] for i, f in enumerate(initial.fields)
        ):
            raise ValueError("source and capture templates must agree on conserved inventory")
        instrument = LocalInstrument(
            tuple(_matrix(m) for m in _array(c["instrument"], "capture instrument", 2, 2))
        )
        validates_capture(instrument)
        phases = []
        for raw_phase in _array(d["phases"], "propagation phases", 32, 1):
            phase = []
            phase_used: set[int] = set()
            for raw_op in _array(raw_phase, "phase operations", 30):
                op = _object(
                    raw_op,
                    "contact propagation",
                    {"register_indices", "matrix"},
                    {"register_indices", "matrix"},
                )
                qs = tuple(
                    _integer(q, "propagation register", 0)
                    for q in _array(op["register_indices"], "propagation registers", 2, 1)
                )
                if len(set(qs)) != len(qs) or any(q not in registers or q in phase_used for q in qs):
                    raise ValueError("propagation phase requires disjoint local domain registers")
                phase_used.update(qs)
                if len(qs) == 2 and not any(
                    neighbor_address(addresses[qs[0]], p, initial.shape, initial.boundary)
                    == addresses[qs[1]]
                    for p in range(6)
                ):
                    raise ValueError("contact propagation requires one physical Link")
                rule = LocalUnitary(_matrix(op["matrix"]))
                if len(rule.matrix) != 2 ** len(qs):
                    raise ValueError("propagation matrix dimension differs from support")
                preserves_occupation(rule)
                phase.append((rule, qs))
            phases.append(tuple(phase))
        domains.append(
            ContactDomain(
                _text(d["name"], "domain name"),
                registers,
                register,
                source_type,
                partner_type,
                validity,
                unknown,
                preparation,
                record,
                detector,
                captures,
                instrument,
                tuple(phases),
            )
        )
    if used != set(range(len(addresses))):
        raise ValueError("every quantum mode must belong to one contact domain")
    if causal_sources:
        for domain in domains:
            remaining = set(domain.registers)
            reached = {remaining.pop()}
            while remaining:
                adjacent = {
                    q
                    for q in remaining
                    if any(
                        neighbor_address(addresses[p], port, initial.shape, initial.boundary)
                        == addresses[q]
                        for p in reached
                        for port in range(6)
                    )
                }
                if not adjacent:
                    raise ValueError("causal source domains must be connected through physical Links")
                reached.update(adjacent)
                remaining.difference_update(adjacent)
    localized_types = {kind for d in domains for kind in (d.source_type, d.output.type_index)}
    if any(
        emission.budget is None and localized_types.intersection(selected_types(emission))
        for emission in initial.emissions
    ):
        raise ValueError("localized contact sources require a finite emission budget")
    bounds = _object(
        obj.get("bounds", {}),
        "contact quantum bounds",
        {"max_nodes", "max_eval_nodes", "max_terms", "max_records"},
        set(),
    )
    network = EventNetworkConfig(
        addresses,
        max_nodes=_integer(bounds.get("max_nodes", 10000), "max_nodes", 1),
        max_eval_nodes=_integer(bounds.get("max_eval_nodes", 10000), "max_eval_nodes", 1),
        max_terms=_integer(bounds.get("max_terms", 4096), "max_terms", 1),
        max_records=_integer(bounds.get("max_records", 1024), "max_records", 1),
        waves=tuple(WaveDefinition(d.name, d.source_register, True) for d in domains),
        local_contacts=True,
        occupation_domains=tuple(d.registers for d in domains),
    )
    capacity = _integer(obj["capacity"], "event capacity", 1)
    _require_initial_capacity(initial, capacity, len(addresses))
    tickets = (
        None
        if "tickets" not in obj
        else tuple(_integer(t, "ticket", 0) for t in _array(obj["tickets"], "tickets", 1024))
    )
    return Program(
        capacity,
        network,
        (),
        (),
        _integer(obj.get("seed", 0), "seed", 0),
        tickets,
        contacts=ContactConfiguration(tuple(domains), causal_sources, null_notices),
    )
