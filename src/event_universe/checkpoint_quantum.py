"""Host-only checkpoint handling for the explicitly composed native quantum owner."""

from dataclasses import replace
from random import Random
from typing import TYPE_CHECKING, Any

from event_universe.core.event_space import CausalEvent, CausalEventSpace
from event_universe.integration.event_runtime import NativeEventResolver
from event_universe.quantum.event_network import EventDecision, NetworkRecord, QuantumPayload
from event_universe.quantum.event_rules import common_scale, matrix_shape, outcome_groups
from event_universe.quantum.mixed import DensityState, term_count, trace
from event_universe.quantum.state import checked_amp

if TYPE_CHECKING:
    from event_universe.disturbance_api import Simulation

NETWORK_FIELDS = (
    "_tick",
    "_revision",
    "_payloads",
    "_heads",
    "_constraints",
    "_prepared",
    "_records",
    "_queries",
    "_evaluated",
)
RESOLVER_FIELDS = ("draws", "host_plans", "overhead_cost")


def capture_events(world: Simulation) -> dict[str, Any] | None:
    events = world.event_space
    if events is None:
        return None
    if type(events) is not CausalEventSpace or set(vars(events)) != {
        "capacity",
        "shape",
        "boundary",
        "link_ticks",
        "_events",
        "_cost",
    }:
        raise ValueError("checkpoint requires the canonical event ledger")
    return {"events": events._events, "cost": events._cost}


def capture_quantum(world: Simulation, fresh: Simulation) -> dict[str, Any] | None:
    resolver, baseline = world._resolver, fresh._resolver
    if resolver is None:
        return None
    if type(resolver) is not NativeEventResolver or type(baseline) is not NativeEventResolver:
        raise ValueError("checkpoint cannot serialize a custom event resolver")
    if set(vars(resolver)) != set(vars(baseline)):
        raise ValueError("checkpoint resolver has unknown mutable attributes")
    for name in ("initial", "program", "layers", "bindings"):
        if getattr(resolver, name) != getattr(baseline, name):
            raise ValueError("checkpoint resolver configuration was changed")
    if (
        resolver.events is not world.event_space
        or resolver.space.event_space is not world.event_space
        or resolver.owner.event_network is not resolver.space
        or type(resolver.rng) is not Random
    ):
        raise ValueError("checkpoint resolver ownership is noncanonical")
    if set(vars(resolver.space)) != {*NETWORK_FIELDS, "_config", "event_space"}:
        raise ValueError("checkpoint quantum network has unknown state")
    if resolver.space.config != baseline.space.config:
        raise ValueError("checkpoint quantum network configuration changed")
    for name, value in vars(resolver.owner).items():
        if name != "_event_network" and value != vars(baseline.owner).get(name):
            raise ValueError("checkpoint only supports the selected native event quantum backend")
    if set(vars(resolver.owner)) != set(vars(baseline.owner)) or vars(resolver.rng) != vars(
        baseline.rng
    ):
        raise ValueError("checkpoint quantum owner contains unsupported state")
    state = resolver.rng.getstate()
    if state[2] is not None:
        raise ValueError("checkpoint native random generator contains an unsupported Gaussian cache")
    return {
        "network": {name: getattr(resolver.space, name) for name in NETWORK_FIELDS},
        "resolver": {name: getattr(resolver, name) for name in RESOLVER_FIELDS},
        "rng": state,
    }


def restore_events(world: Simulation, payload: Any) -> None:
    ledger = world.event_space
    if ledger is None:
        if payload is not None:
            raise ValueError("checkpoint includes an unconfigured event ledger")
        return
    if type(payload) is not dict or set(payload) != {"events", "cost"}:
        raise ValueError("checkpoint event ledger fields are incomplete")
    if type(payload["events"]) is not list or len(payload["events"]) > ledger.capacity:
        raise ValueError("checkpoint event ledger exceeds capacity")
    validated = CausalEventSpace(
        ledger.capacity, shape=ledger.shape, boundary=ledger.boundary, link_ticks=ledger.link_ticks
    )
    for entry in payload["events"]:
        if type(entry) is not CausalEvent or entry.tick > world.tick:
            raise ValueError("invalid checkpoint causal event")
        rebuilt = validated.append(
            tick=entry.tick,
            addresses=entry.addresses,
            owner=entry.owner,
            kind=entry.kind,
            parents=entry.parents,
            physical_parents=entry.physical_parents,
            payload_ref=entry.payload_ref,
            model_cost=entry.model_cost,
        )
        if rebuilt != entry:
            raise ValueError("checkpoint causal event order or parents are inconsistent")
    if type(payload["cost"]) is not int or validated.model_cost != payload["cost"]:
        raise ValueError("checkpoint causal cost ledger disagrees with events")
    ledger._events, ledger._cost = validated._events, validated._cost


def restore_quantum(world: Simulation, payload: Any) -> None:
    resolver = world._resolver
    if resolver is None:
        if payload is not None:
            raise ValueError("checkpoint includes an unconfigured quantum owner")
        return
    if type(resolver) is not NativeEventResolver:
        raise ValueError("checkpoint requires the canonical native resolver")
    if type(payload) is not dict or set(payload) != {"network", "resolver", "rng"}:
        raise ValueError("checkpoint quantum owner fields are incomplete")
    network, counters = payload["network"], payload["resolver"]
    if (
        type(network) is not dict
        or set(network) != set(NETWORK_FIELDS)
        or type(counters) is not dict
        or set(counters) != set(RESOLVER_FIELDS)
    ):
        raise ValueError("checkpoint quantum state schema mismatch")
    for name in ("_tick", "_revision", "_queries", "_evaluated"):
        if type(network[name]) is not int or network[name] < 0:
            raise ValueError("checkpoint quantum counters must be nonnegative integers")
    if network["_tick"] != world.tick:
        raise ValueError("checkpoint physical and quantum clocks disagree")
    if any(type(value) is not int or value < 0 for value in counters.values()):
        raise ValueError("checkpoint resolver counters are invalid")
    space, events = resolver.space, resolver.events
    for name in ("_payloads", "_heads", "_constraints", "_prepared", "_records"):
        if type(network[name]) is not dict or any(type(k) is not int for k in network[name]):
            raise ValueError("checkpoint quantum indices require integer-keyed dictionaries")
    quantum = network["_payloads"]
    if len(quantum) > space.config.max_nodes:
        raise ValueError("checkpoint quantum payload capacity exceeded")
    site_count = len(space.config.addresses)
    basis_size = 1
    for dimension in space.config.local_dimensions:
        basis_size *= dimension
    for identity, value in quantum.items():
        event = events.event(identity)
        if (
            type(value) is not QuantumPayload
            or event.owner != "quantum"
            or event.payload_ref != identity
        ):
            raise ValueError("checkpoint quantum payload has no matching causal owner")
        if (
            not value.sites
            or len(set(value.sites)) != len(value.sites)
            or any(not 0 <= site < site_count for site in value.sites)
        ):
            raise ValueError("checkpoint quantum payload support is invalid")
        if tuple(space.config.addresses[site] for site in value.sites) != event.addresses:
            raise ValueError("checkpoint quantum payload support disagrees with causal addresses")
        expected_kind = (
            "record"
            if value.outcome >= 0
            else "state"
            if value.state is not None
            else "channel"
            if value.channel
            else "operation"
        )
        if event.kind != expected_kind or value.outcome < -1:
            raise ValueError("checkpoint quantum payload kind disagrees with its causal event")
        if sum((value.matrix is not None, value.state is not None, bool(value.channel))) != 1:
            raise ValueError("checkpoint quantum payload has ambiguous physical ownership")
        local_dimension = 1
        for site in value.sites:
            local_dimension *= space.config.local_dimensions[site]
        if value.matrix is not None:
            if matrix_shape(value.matrix) != local_dimension:
                raise ValueError("checkpoint quantum operation dimension disagrees with its sites")
            if event.kind == "operation":
                common_scale((value.matrix,))
        for matrix in value.channel:
            if matrix_shape(matrix) != local_dimension:
                raise ValueError("checkpoint quantum channel dimension disagrees with its sites")
        if event.kind == "channel":
            common_scale(value.channel)
        if value.state is not None:
            if term_count(value.state) > space.config.max_terms or trace(value.state) <= 0:
                raise ValueError("checkpoint quantum state has invalid size or norm")
            entries = (
                value.state.entries
                if isinstance(value.state, DensityState)
                else tuple((i, i, a) for i, a in value.state)
            )
            if len({(i, j) for i, j, _ in entries}) != len(entries):
                raise ValueError("duplicate checkpoint quantum state index")
            for i, j, amplitude in entries:
                if not 0 <= i < basis_size or not 0 <= j < basis_size:
                    raise ValueError("checkpoint quantum basis index exceeds configuration")
                checked_amp(amplitude.real, amplitude.imag)
    if set(network["_heads"]) != set(range(site_count)) or any(
        type(i) is not int or i not in quantum for i in network["_heads"].values()
    ):
        raise ValueError("checkpoint quantum heads are incomplete or unknown")
    for identity, constraint in network["_constraints"].items():
        if identity not in quantum or type(constraint) is not tuple or len(constraint) != 2:
            raise ValueError("checkpoint quantum constraint is invalid")
        nodes, sites = constraint
        if (
            type(nodes) is not frozenset
            or type(sites) is not frozenset
            or any(type(i) is not int or i not in quantum for i in nodes)
            or any(type(i) is not int or not 0 <= i < site_count for i in sites)
        ):
            raise ValueError("checkpoint quantum constraint references missing state")
    prepared, records = network["_prepared"], network["_records"]
    if len(prepared) > space.config.max_records or len(records) > space.config.max_records:
        raise ValueError("checkpoint quantum record capacity exceeded")
    for identity, decision in prepared.items():
        if (
            type(decision) is not EventDecision
            or identity != decision.record_id
            or not 0 <= decision.site < site_count
            or not 0 <= decision.tick <= world.tick
            or not 0 <= decision.revision <= network["_revision"]
            or any(weight < 0 for weight in decision.weights)
            or decision.total_weight <= 0
            or len(decision.weights) != len(outcome_groups(decision.instrument))
        ):
            raise ValueError("checkpoint quantum decision is invalid")
        if decision.cause is not None:
            events.event(decision.cause)
        for group in outcome_groups(decision.instrument):
            for matrix in group:
                if matrix_shape(matrix) != space.config.local_dimensions[decision.site]:
                    raise ValueError("checkpoint quantum decision instrument dimension is inconsistent")
    for identity, record in records.items():
        if (
            type(record) is not NetworkRecord
            or identity not in prepared
            or record.decision != prepared[identity]
            or not 0 <= record.outcome < len(record.decision.weights)
            or record.decision.weights[record.outcome] == 0
        ):
            raise ValueError("checkpoint quantum recorded outcome is invalid")
        event = events.event(record.event_id)
        decision = record.decision
        if (
            event.owner != "quantum"
            or event.kind != "record"
            or event.addresses != (space.config.addresses[decision.site],)
            or event.tick != decision.tick
            or event.payload_ref != record.event_id
            or (decision.cause is not None and decision.cause not in event.parents)
        ):
            raise ValueError("checkpoint recorded outcome disagrees with the causal ledger")
        if record.event_id in quantum:
            value = quantum[record.event_id]
            group = outcome_groups(decision.instrument)[record.outcome]
            if (
                value.outcome != record.outcome
                or value.sites != (decision.site,)
                or value.matrix != (group[0] if len(group) == 1 else None)
                or value.channel != (group if len(group) > 1 else ())
                or value.state is not None
            ):
                raise ValueError("checkpoint quantum record and chosen outcome payload disagree")
        # The quantum owner requires this shared immutable identity on repeated commit.
        records[identity] = replace(record, decision=prepared[identity])
    rng = Random()
    if type(payload["rng"]) is not tuple or len(payload["rng"]) != 3 or payload["rng"][2] is not None:
        raise ValueError("checkpoint native random state is invalid")
    rng.setstate(payload["rng"])
    for name in NETWORK_FIELDS:
        setattr(space, name, network[name])
    for name in RESOLVER_FIELDS:
        setattr(resolver, name, counters[name])
    resolver.rng.setstate(rng.getstate())
