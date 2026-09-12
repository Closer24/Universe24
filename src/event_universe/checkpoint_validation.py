"""Read-only structural and ownership checks for a restored checkpoint candidate."""

from typing import TYPE_CHECKING, Any

from event_universe.core.disturbance_state import (
    MAX_VALUE,
    DisturbanceCell,
    DisturbanceRecord,
    LocalPlan,
    Packet,
    bounded,
    decode,
)
from event_universe.core.spatial_state import SpatialCell, SpatialPacket
from event_universe.core.topology import site_count, validate_position

if TYPE_CHECKING:
    from event_universe.disturbance_api import Simulation

WORLD_FIELDS = (
    "tick",
    "faulted",
    "_model_work",
    "_local_cycles",
    "_cells",
    "_links",
    "_source_totals",
    "_escaped_totals",
)
SPATIAL_FIELDS = (
    "cells",
    "links",
    "_active",
    "_field_tick",
    "sources",
    "dissipation",
    "reactions",
    "transformations",
    "escaped",
    "_initial_totals",
)


def _integer(value: Any, minimum: int = 0, maximum: int = MAX_VALUE) -> None:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError("checkpoint integer is outside its state bound")


def _payload(value: Any, components: int, *, encoded: bool = True) -> None:
    if type(value) is not tuple or len(value) != components:
        raise ValueError("checkpoint payload width is inconsistent")
    for component in value:
        decode(component) if encoded else bounded(component)


def _values(world: Simulation, values: Any, *, encoded: bool = False, optional: bool = False) -> None:
    if optional and values == ():
        return
    if type(values) is not tuple or len(values) != len(world.initial.fields):
        raise ValueError("checkpoint named field schema is inconsistent")
    for definition, payload in zip(world.initial.fields, values, strict=False):
        _payload(payload, definition.components, encoded=encoded)


def _record(world: Simulation, record: Any) -> None:
    if type(record) is not DisturbanceRecord:
        raise ValueError("checkpoint contains an invalid disturbance record")
    initial = world.initial
    _integer(record.type_index, 0, len(initial.disturbances) - 1)
    _values(world, record.values, encoded=True)
    _values(world, record.phase_codes, encoded=True)
    for index, definition in enumerate(initial.fields):
        definition.validate(record.values[index])
        if index not in initial.disturbances[record.type_index].fields and any(
            decode(c) for c in record.values[index]
        ):
            raise ValueError("checkpoint disturbance carries an unowned field")
        for code in record.phase_codes[index]:
            _integer(code, 1, MAX_VALUE + 1)
    for code in (record.route_phase_code, record.rate_remainder_code):
        _integer(code, 1, MAX_VALUE + 1)
    _integer(record.channel_code, 1, initial.topology.degree + 1)
    _integer(record.rate_credit_denominator, 1)
    transport = initial.disturbances[record.type_index].transport
    if transport.rate_divisor is not None:
        if record.rate_remainder_code - 1 >= record.rate_credit_denominator:
            raise ValueError("checkpoint fractional movement credit exceeds its denominator")
    elif (
        record.rate_credit_denominator != 1
        or record.rate_remainder_code - 1 >= transport.rate_denominator
    ):
        raise ValueError("checkpoint fixed movement credit exceeds its configured denominator")
    for codes in (record.route_count_codes, record.route_weight_codes):
        if len(codes) != initial.topology.degree:
            raise ValueError("checkpoint route state does not match topology")
        for code in codes:
            _integer(code, 1, MAX_VALUE + 1)
    if any(
        count > weight
        for count, weight in zip(record.route_count_codes, record.route_weight_codes, strict=True)
    ):
        raise ValueError("checkpoint balanced routing count exceeds its saved weight")
    layouts = (
        (
            record.emission_remainders,
            tuple(initial.spatial_fields[d.spatial_field].field for d in initial.emissions),
        ),
        (
            record.emission_phases,
            tuple(initial.spatial_fields[d.spatial_field].field for d in initial.emissions),
        ),
        (
            record.emission_remaining,
            tuple(initial.spatial_fields[d.spatial_field].field for d in initial.emissions),
        ),
        (record.exchange_remainders, tuple(d.field for d in initial.couplings)),
        (record.spatial_remainders, tuple(d.field for d in initial.spatial_couplings)),
        (record.spatial_remaining, tuple(d.field for d in initial.spatial_couplings)),
    )
    for values, field_indices in layouts:
        if not values:
            continue
        if len(values) != len(field_indices):
            raise ValueError("checkpoint carried remainder schema is inconsistent")
        for value, field in zip(values, field_indices, strict=False):
            _payload(value, initial.fields[field].components)


def _remainders(world: Simulation, values: tuple[int, ...]) -> None:
    expected = len(world.initial.couplings) * world.initial.slots_per_cell**2 * 3
    if len(values) != expected:
        raise ValueError("checkpoint pair remainder capacity is inconsistent")
    for value in values:
        decode(value)


def _cause(world: Simulation, value: int | None) -> None:
    if value is not None:
        if world.event_space is None:
            raise ValueError("checkpoint causal reference has no configured ledger")
        world.event_space.event(value)


def _plan(world: Simulation, plan: LocalPlan) -> None:
    capacity, degree = world.initial.slots_per_cell, world.initial.topology.degree
    if len(plan.replacements) > capacity or len({slot for slot, _ in plan.replacements}) != len(
        plan.replacements
    ):
        raise ValueError("checkpoint pending replacement slots are inconsistent")
    for slot, record in plan.replacements:
        _integer(slot, 0, capacity - 1)
        if record is not None:
            _record(world, record)
    if len(plan.departures) > capacity * degree:
        raise ValueError("checkpoint pending departure capacity exceeded")
    for departure in plan.departures:
        _integer(departure.port, 0, degree - 1)
        _integer(departure.origin_slot, -1, capacity - 1)
        _record(world, departure.record)
    _remainders(world, plan.coupling_remainders)
    _values(world, plan.source_delta)
    _values(world, plan.spatial_reaction, optional=True)
    _integer(plan.cost)
    _cause(world, plan.cause_id)
    for guard in plan.spatial_guards:
        _integer(guard.rule_index, 0, len(world.initial.spatial_interactions) - 1)
        _integer(guard.slot, 0, capacity - 1)
        for values in (guard.before, guard.after):
            _values(world, values, encoded=True)
        _values(world, guard.delta)


def _ledger(world: Simulation, ledger: Any) -> None:
    if type(ledger) is not list or len(ledger) != len(world.initial.fields):
        raise ValueError("checkpoint cumulative ledger schema is inconsistent")
    for definition, values in zip(world.initial.fields, ledger, strict=False):
        if (
            type(values) is not list
            or len(values) != definition.components
            or any(type(v) is not int for v in values)
        ):
            raise ValueError("checkpoint cumulative ledger components are invalid")
        for value in values:
            _integer(value, -(1 << 63) + 1, (1 << 63) - 1)


def _pending_balance(world: Simulation, cell: DisturbanceCell) -> None:
    if cell.pending is None:
        return
    plan = cell.pending.plan
    before = [cell.records[slot] for slot, _ in plan.replacements]
    after = [record for _, record in plan.replacements]
    after.extend(departure.record for departure in plan.departures)
    for index, field in enumerate(world.initial.fields):
        if not field.conserved:
            continue
        for component in range(field.components):
            incoming = sum(
                decode(record.values[index][component]) for record in before if record is not None
            )
            outgoing = sum(
                decode(record.values[index][component]) for record in after if record is not None
            )
            reaction = plan.spatial_reaction[index][component] if plan.spatial_reaction else 0
            if outgoing + reaction - incoming != plan.source_delta[index][component]:
                raise ValueError("checkpoint frozen pending plan violates its conserved balance")


def validate_world(world: Simulation) -> None:
    initial = world.initial
    _integer(world.tick)
    if type(world.faulted) is not bool:
        raise ValueError("checkpoint failure flag is invalid")
    for counter in (world._model_work, world._local_cycles):
        _integer(counter, maximum=(1 << 63) - 1)
    for ledger in (world._source_totals, world._escaped_totals):
        _ledger(world, ledger)
    if type(world._cells) is not dict or type(world._links) is not dict:
        raise ValueError("checkpoint carrier indices are invalid")
    for position, cell in world._cells.items():
        validate_position(position, initial.shape, initial.topology)
        if type(cell) is not DisturbanceCell or len(cell.records) != initial.slots_per_cell:
            raise ValueError("checkpoint cell has invalid resident capacity")
        for record in cell.records:
            if record is not None:
                _record(world, record)
        _remainders(world, cell.coupling_remainders)
        for value in (cell.available_tick, cell.received_count, cell.last_cost):
            _integer(value)
        _cause(world, cell.cause_id)
        if cell.pending is not None:
            pending = cell.pending
            _integer(pending.ready_tick)
            _integer(pending.next_tick)
            if pending.next_tick - pending.ready_tick != initial.link_ticks:
                raise ValueError("checkpoint pending cycle timing is inconsistent")
            if not world.faulted and pending.ready_tick < world.tick:
                raise ValueError("checkpoint contains an overdue pending cycle")
            _plan(world, pending.plan)
            _cause(world, pending.cause_id)
            _pending_balance(world, cell)
    for origin, packets in world._links.items():
        if (
            origin not in world._cells
            or type(packets) is not tuple
            or len(packets) != initial.slots_per_cell * initial.topology.degree
        ):
            raise ValueError("checkpoint carrier link ownership or capacity is invalid")
        for packet in packets:
            if packet is None:
                continue
            if type(packet) is not Packet or packet.origin != origin:
                raise ValueError("checkpoint carrier packet ownership is invalid")
            _integer(packet.port, 0, initial.topology.degree - 1)
            _integer(packet.arrival_tick)
            if not world.faulted and packet.arrival_tick <= world.tick:
                raise ValueError("checkpoint contains an overdue carrier packet")
            _record(world, packet.record)
            _cause(world, packet.cause_id)
    _validate_spatial(world)


def _validate_spatial(world: Simulation) -> None:
    initial, spatial = world.initial, world._spatial
    if spatial is None:
        return
    for name in ("sources", "dissipation", "reactions", "transformations", "escaped"):
        _ledger(world, getattr(spatial, name))
    _integer(spatial._field_tick, -1, world.tick)
    if (
        type(spatial.cells) is not dict
        or type(spatial.links) is not dict
        or type(spatial._active) is not set
    ):
        raise ValueError("checkpoint spatial indices are invalid")
    if not spatial._active <= spatial.cells.keys():
        raise ValueError("checkpoint active spatial index contains unknown cells")
    for position, cell in spatial.cells.items():
        validate_position(position, initial.shape, initial.topology)
        if type(cell) is not SpatialCell or len(cell.states) != len(initial.spatial_fields):
            raise ValueError("checkpoint spatial cell schema is invalid")
        if position not in spatial._active and (
            cell.received_count
            or any(
                decode(code)
                for state in cell.states
                for payload in state.populations
                for code in payload
            )
        ):
            raise ValueError("checkpoint spatial scheduling hides an active physical owner")
        for definition, state in zip(initial.spatial_fields, cell.states, strict=False):
            state.validate(initial.fields[definition.field].components, initial.topology.degree)
            for payload in (*state.populations, *state.delivered):
                initial.fields[definition.field].validate(payload)
        for value in (cell.last_cost, cell.received_count, cell.received_decay_cost):
            _integer(value)
        _integer(cell.last_begin_tick, -1, world.tick)
        if cell.reaction_phases:
            if len(cell.reaction_phases) != len(initial.spatial_fields):
                raise ValueError("checkpoint spatial reaction phases have the wrong width")
            for definition, phase in zip(initial.spatial_fields, cell.reaction_phases, strict=False):
                _payload(phase, initial.fields[definition.field].components)
                if any(not 0 <= decode(code) < sum(definition.octant_weights) for code in phase):
                    raise ValueError("checkpoint spatial reaction phase exceeds its allocation cycle")
        _values(world, cell.sample_values, encoded=True, optional=True)
        if cell.sample_values:
            for field, payload in zip(initial.fields, cell.sample_values, strict=True):
                field.validate(payload)
        if cell.sample_fluxes:
            if len(cell.sample_fluxes) != len(initial.fields):
                raise ValueError("checkpoint sampled flux fields have the wrong width")
            for flux in cell.sample_fluxes:
                _payload(flux, 3)
        if cell.sample_ports:
            if len(cell.sample_ports) != initial.topology.degree:
                raise ValueError("checkpoint sampled port count is invalid")
            for values in cell.sample_ports:
                _values(world, values, encoded=True)
                for field, payload in zip(initial.fields, values, strict=True):
                    field.validate(payload)
    for origin, packets in spatial.links.items():
        if (
            origin not in spatial.cells
            or type(packets) is not tuple
            or len(packets) != initial.topology.degree
        ):
            raise ValueError("checkpoint spatial link ownership or capacity is invalid")
        for packet in packets:
            if packet is None:
                continue
            if (
                type(packet) is not SpatialPacket
                or packet.origin != origin
                or len(packet.fields) != len(initial.spatial_fields)
            ):
                raise ValueError("checkpoint spatial packet ownership is invalid")
            _integer(packet.port, 0, initial.topology.degree - 1)
            _integer(packet.arrival_tick)
            if not world.faulted and packet.arrival_tick <= world.tick:
                raise ValueError("checkpoint contains an overdue spatial packet")
            for definition, populations in zip(initial.spatial_fields, packet.fields, strict=False):
                if len(populations) != 8:
                    raise ValueError("checkpoint spatial packet requires eight populations")
                for payload in populations:
                    initial.fields[definition.field].validate(payload)


def validate_balance(world: Simulation, fresh: Simulation) -> None:
    """Reconcile actual owners, without trusting the optimized active index."""
    totals = [[0] * field.components for field in world.initial.fields]
    records = [r for cell in world._cells.values() for r in cell.records if r is not None]
    records.extend(p.record for packets in world._links.values() for p in packets if p is not None)
    for record in records:
        for index, payload in enumerate(record.values):
            for component, code in enumerate(payload):
                totals[index][component] += decode(code)
    spatial = world._spatial
    if spatial is not None:
        volume = site_count(world.initial.shape, world.initial.topology)
        for index, definition in enumerate(world.initial.spatial_fields):
            target = totals[definition.field]
            for component, code in enumerate(definition.baseline):
                target[component] += volume * decode(code)
            inventories = [cell.states[index].populations for cell in spatial.cells.values()]
            inventories.extend(
                packet.fields[index]
                for packets in spatial.links.values()
                for packet in packets
                if packet is not None
            )
            for populations in inventories:
                for payload in populations:
                    for component, code in enumerate(payload):
                        target[component] += decode(code)
    initial = fresh.totals()
    sources, losses, escaped = world.source_totals(), world.dissipation_totals(), world.escaped_totals()
    for index, field in enumerate(world.initial.fields):
        if field.conserved:
            for component, current in enumerate(totals[index]):
                if (
                    current + losses[field.name][component] + escaped[field.name][component]
                    != initial[field.name][component] + sources[field.name][component]
                ):
                    raise ValueError(
                        "checkpoint conserved stock disagrees with initial state and ledgers"
                    )
