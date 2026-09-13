"""Demand-driven joint-state backend owned by DeferredQuantum.

Acyclic per-node heads describe the wave; read-only queries never select old paths.
Recorded constraints close the conservative backward cone. Only an explicitly
supplied local instrument can commit an outcome. This is an opt-in finite
quantum candidate, not a derived field law; native integration shares the causal metadata owner.
"""

from dataclasses import dataclass

from event_universe.core.event_space import CausalEventSpace
from event_universe.core.state import Address, checked, checked_work

from .event_rules import (
    BasisLayout,
    GroupedInstrument,
    LocalChannel,
    LocalInstrument,
    LocalUnitary,
    Matrix,
    State,
    outcome_groups,
)
from .mixed import (
    DensityState,
    QuantumState,
    density,
    evolve,
    marginal,
    partial_trace,
    reduce_quantum,
    tensor,
    term_count,
    trace,
)
from .state import Amplitude, checked_address

LocalOperation = LocalUnitary | LocalChannel
Instrument = LocalInstrument | GroupedInstrument

EVENT_NETWORK_MODEL_ID = "deferred-event-network-v1"
# The original constant remains for legacy binary callers. Native v2 is explicit.
REGISTER_NETWORK_MODEL_ID = "deferred-register-network-v2"


@dataclass(frozen=True, slots=True)
class EventNetworkConfig:
    addresses: tuple[Address, ...]
    occupied: tuple[int, ...] = ()
    max_nodes: int = 10_000
    max_eval_nodes: int = 10_000
    max_terms: int = 4_096
    max_records: int = 1_024
    dimensions: tuple[int, ...] = ()
    initial_levels: tuple[int, ...] = ()
    register_names: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if type(self.addresses) is not tuple or not 1 <= len(self.addresses) <= 30:
            raise ValueError("one to thirty immutable addresses are supported")
        for address in self.addresses:
            checked_address(address)
        if type(self.register_names) is not tuple:
            raise ValueError("register names must be immutable")
        if self.register_names:
            if (
                type(self.register_names) is not tuple
                or len(self.register_names) != len(self.addresses)
                or len(set(self.register_names)) != len(self.register_names)
                or any(type(n) is not str or not n or len(n) > 128 for n in self.register_names)
            ):
                raise ValueError("register names must be distinct bounded strings")
        elif len(set(self.addresses)) != len(self.addresses):
            raise ValueError("node addresses must be distinct without explicit register names")
        if type(self.dimensions) is not tuple or (
            self.dimensions and len(self.dimensions) != len(self.addresses)
        ):
            raise ValueError("one dimension per register required")
        BasisLayout(self.local_dimensions)
        if type(self.initial_levels) is not tuple or (
            self.initial_levels and len(self.initial_levels) != len(self.addresses)
        ):
            raise ValueError("one initial level per register required")
        if self.initial_levels and self.occupied:
            raise ValueError("initial_levels and occupied are mutually exclusive")
        if self.initial_levels:
            for level, dimension in zip(self.initial_levels, self.local_dimensions, strict=True):
                if not 0 <= checked(level) < dimension:
                    raise ValueError("initial level outside register basis")
        if type(self.occupied) is not tuple:
            raise TypeError("occupied nodes must be immutable")
        for register_index in self.occupied:
            checked(register_index)
            if not 0 <= register_index < len(self.addresses):
                raise ValueError("occupied node outside network")
        if len(set(self.occupied)) != len(self.occupied):
            raise ValueError("duplicate initial occupation")
        for value in (self.max_nodes, self.max_eval_nodes, self.max_terms, self.max_records):
            if checked(value) <= 0:
                raise ValueError("positive quantum resource budgets required")
        if self.max_nodes < len(self.addresses):
            raise ValueError("node budget cannot hold initial sources")

    @property
    def local_dimensions(self) -> tuple[int, ...]:
        return self.dimensions or (2,) * len(self.addresses)

    @property
    def levels(self) -> tuple[int, ...]:
        return self.initial_levels or tuple(int(q in self.occupied) for q in range(len(self.addresses)))


@dataclass(frozen=True, slots=True)
class NetworkEvent:
    id: int
    tick: int
    register_indices: tuple[int, ...]
    parents: tuple[int, ...] = ()
    matrix: Matrix | None = None
    state: QuantumState | None = None
    outcome: int = -1
    channel: tuple[Matrix, ...] = ()


@dataclass(frozen=True, slots=True)
class NetworkQuery:
    weights: tuple[int, ...]
    evaluated_nodes: int
    peak_terms: int
    model_cost: int = 1
    world_ticks: int = 0


@dataclass(frozen=True, slots=True)
class EventDecision:
    record_id: int
    tick: int
    revision: int
    register_index: int
    instrument: Instrument
    weights: tuple[int, ...]
    evaluated_nodes: int
    model_cost: int = 1
    world_ticks: int = 0
    cause: int | None = None

    @property
    def total_weight(self) -> int:
        total = 0
        for value in self.weights:
            total = checked(total + value)
        return total


@dataclass(frozen=True, slots=True)
class NetworkRecord:
    decision: EventDecision
    outcome: int
    event_id: int


@dataclass(frozen=True, slots=True)
class QuantumPayload:
    register_indices: tuple[int, ...]
    matrix: Matrix | None
    state: QuantumState | None
    outcome: int
    channel: tuple[Matrix, ...] = ()


class EventNetwork:
    """Internal backend; instantiate through DeferredQuantum.bind_event_network.

    State/configuration snapshots are immutable. Physical steps only append local
    recipes. Query results and full checkpoints belong to the host quantum owner,
    never to ordinary field, movement or self-field rules.
    """

    def __init__(self, config: EventNetworkConfig, event_space: CausalEventSpace | None = None) -> None:
        if type(config) is not EventNetworkConfig:
            raise TypeError("immutable EventNetworkConfig required")
        self._config = config
        self._tick = 0
        self._revision = 0
        self.event_space = event_space if event_space is not None else CausalEventSpace()
        self.event_space.require_room(len(config.addresses))
        self._payloads: dict[int, QuantumPayload] = {}
        self._cursors = self.event_space.bind_streams("quantum", config.addresses)
        layout = BasisLayout(config.local_dimensions)
        for q in range(len(config.addresses)):
            node = NetworkEvent(
                self.event_space.next_id,
                0,
                (q,),
                state=((layout.stride(q) * config.levels[q], Amplitude(1, 0)),),
            )
            self._store(node)
        self._constraints: dict[int, tuple[frozenset[int], frozenset[int]]] = {}
        self._prepared: dict[int, EventDecision] = {}
        self._records: dict[int, NetworkRecord] = {}
        self._queries = 0
        self._evaluated = 0

    def _store(self, node: NetworkEvent, cause: int | None = None, *, checkpoint: bool = False) -> None:
        parents = node.parents if cause is None else (*node.parents, cause)
        event = self.event_space.append(
            tick=node.tick,
            addresses=tuple(self.config.addresses[q] for q in node.register_indices),
            owner="quantum",
            kind="checkpoint"
            if checkpoint
            else "record"
            if node.outcome >= 0
            else "state"
            if node.state is not None
            else "channel"
            if node.channel
            else "operation",
            parents=parents,
            payload_ref=node.id,
            cursors=tuple(self._cursors[q] for q in node.register_indices),
            advance_stream_time=not checkpoint,
        )
        if event.id != node.id:
            raise ValueError("event identity changed during insertion")
        self._payloads[event.id] = QuantumPayload(
            node.register_indices, node.matrix, node.state, node.outcome, node.channel
        )

    def _event(self, identity: int) -> NetworkEvent:
        payload = self._payloads[identity]
        event = self.event_space.event(identity)
        return NetworkEvent(
            identity,
            event.tick,
            payload.register_indices,
            tuple(i for i in event.parents if i in self._payloads),
            payload.matrix,
            payload.state,
            payload.outcome,
            payload.channel,
        )

    @property
    def config(self) -> EventNetworkConfig:
        return self._config

    @property
    def node_count(self) -> int:
        return len(self._payloads)

    @property
    def tick(self) -> int:
        return self._tick

    @property
    def heads(self) -> tuple[int, ...]:
        return tuple(self._head(q) for q in range(len(self._cursors)))

    def _head(self, register_index: int) -> int:
        head = self._cursors[register_index].head
        if head is None:
            raise RuntimeError("quantum stream lacks its initial state")
        return head

    @property
    def physical_ticks(self) -> tuple[int, ...]:
        """Last modeled change per register, unaffected by host checkpoints."""
        return tuple(cursor.physical_tick for cursor in self._cursors)

    def history(self, register_index: int) -> tuple[int, ...]:
        """Read the local linked audit sequence, including compacted records."""
        self._validate_register_index(register_index)
        return self.event_space.history(self._cursors[register_index])

    @property
    def events(self) -> tuple[NetworkEvent, ...]:
        return tuple(self._event(i) for i in self._payloads)

    @property
    def records(self) -> tuple[NetworkRecord, ...]:
        return tuple(self._records.values())

    @property
    def host_evaluated_nodes(self) -> int:
        return self._evaluated

    @property
    def successful_queries(self) -> int:
        return self._queries

    def _validate_register_index(self, register_index: int) -> None:
        checked(register_index)
        if not 0 <= register_index < len(self.config.addresses):
            raise ValueError("register_index outside network")

    def _room(self, count: int) -> None:
        self.event_space.require_room(count)
        checked(self.event_space.next_id + count)
        if len(self._payloads) + count > self.config.max_nodes:
            raise OverflowError("quantum node budget exceeded")

    def step(self, operations: tuple[tuple[LocalOperation, tuple[int, ...]], ...]) -> None:
        """One tick of disjoint local operations, validated before any mutation."""
        if type(operations) is not tuple:
            raise TypeError("immutable operation layer required")
        tick = checked(self.tick + 1)
        revision = checked(self._revision + 1)
        self._room(len(operations))
        used: set[int] = set()
        nodes: list[NetworkEvent] = []
        for rule, register_indices in operations:
            if type(rule) not in (LocalUnitary, LocalChannel) or type(register_indices) is not tuple:
                raise TypeError("local coherent rule and immutable register_indices required")
            if len(register_indices) not in (1, 2):
                raise ValueError("rule dimension and register_indices disagree")
            if isinstance(rule, LocalChannel) and len(register_indices) != 1:
                raise ValueError("unobserved channels act on one register")
            size = 1
            for register_index in register_indices:
                self._validate_register_index(register_index)
                size *= self.config.local_dimensions[register_index]
            matrix = rule.matrix if isinstance(rule, LocalUnitary) else rule.kraus[0]
            if len(matrix) != size:
                raise ValueError("rule dimension and register_indices disagree")
            for register_index in register_indices:
                self._validate_register_index(register_index)
                if register_index in used:
                    raise ValueError("a register_index cannot occur twice in a physical tick")
                used.add(register_index)
            if len(register_indices) == 2:
                a, b = (self.config.addresses[q] for q in register_indices)
                distance = sum(abs(checked_work(x - y)) for x, y in zip(a, b, strict=True))
                if distance not in (0, 1):
                    raise ValueError("only cardinal nearest-neighbor operations are allowed")
            parents = tuple(dict.fromkeys(self._head(q) for q in register_indices))
            nodes.append(
                NetworkEvent(
                    self.event_space.next_id + len(nodes),
                    tick,
                    register_indices,
                    parents,
                    rule.matrix if isinstance(rule, LocalUnitary) else None,
                    channel=rule.kraus if isinstance(rule, LocalChannel) else (),
                )
            )
        for node in nodes:
            self._store(node)
        self._tick, self._revision = tick, revision

    def _ancestors(self, roots: tuple[int, ...]) -> tuple[set[int], set[int]]:
        found: set[int] = set()
        register_indices: set[int] = set()
        stack = list(roots)
        while stack:
            i = stack.pop()
            if i in found:
                continue
            if len(found) >= self.config.max_eval_nodes:
                raise OverflowError("backward dependency budget exceeded")
            node = self._event(i)
            found.add(i)
            register_indices.update(node.register_indices)
            stack.extend(node.parents)
        return found, register_indices

    def _plan(self, targets: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
        for register_index in targets:
            self._validate_register_index(register_index)
        ids, register_indices = self._ancestors(tuple(self._head(q) for q in targets))
        while True:
            grew = False
            for i, (record_ids, record_register_indices) in self._constraints.items():
                if i not in ids and register_indices.intersection(record_register_indices):
                    if len(ids | record_ids) > self.config.max_eval_nodes:
                        raise OverflowError("conditional dependency budget exceeded")
                    ids.update(record_ids)
                    register_indices.update(record_register_indices)
                    grew = True
            if not grew:
                return tuple(sorted(ids)), tuple(sorted(register_indices))

    def _evaluate(self, ids: tuple[int, ...]) -> tuple[QuantumState, int]:
        value: QuantumState = ((0, Amplitude(1, 0)),)
        initialized: set[int] = set()
        peak = 1
        for i in ids:
            node = self._event(i)
            if node.state is not None:
                if initialized.intersection(node.register_indices):
                    raise ArithmeticError("overlapping checkpoint sources")
                initialized.update(node.register_indices)
                value = tensor(value, node.state, self.config.max_terms)
        peak = max(peak, term_count(value))
        for i in ids:
            node = self._event(i)
            matrices = (node.matrix,) if node.matrix is not None else node.channel
            if matrices:
                value = evolve(
                    value,
                    matrices,
                    node.register_indices,
                    self.config.max_terms,
                    self.config.local_dimensions,
                )
                value = reduce_quantum(value)
                peak = max(peak, term_count(value))
        return value, peak

    def _count_query(self, nodes: int) -> None:
        queries = checked_work(self._queries + 1)
        evaluated = checked_work(self._evaluated + nodes)
        self._queries, self._evaluated = queries, evaluated

    def query(self, register_index: int) -> NetworkQuery:
        """Compute a local marginal; never sample or alter a physical record."""
        ids, _ = self._plan((register_index,))
        state, peak = self._evaluate(ids)
        weights = marginal(state, register_index, self.config.local_dimensions)
        reply = NetworkQuery(weights, len(ids), peak)
        self._count_query(len(ids))
        return reply

    def joint_state(self) -> State:
        """Read-only host diagnostic, not a fixed-size physical node reply."""
        ids, _ = self._plan(tuple(range(len(self.config.addresses))))
        state = self._evaluate(ids)[0]
        if isinstance(state, DensityState):
            raise ValueError("mixed state has no single wavefunction; use joint_density")
        return state

    def joint_density(self, register_indices: tuple[int, ...] | None = None) -> DensityState:
        """Read-only host state, with exact partial trace when register_indices are supplied."""
        targets = (
            tuple(range(len(self.config.addresses))) if register_indices is None else register_indices
        )
        if type(targets) is not tuple or not targets or len(set(targets)) != len(targets):
            raise ValueError("distinct immutable diagnostic registers required")
        ids, _ = self._plan(targets)
        state, _ = self._evaluate(ids)
        if register_indices is None:
            result = reduce_quantum(density(state, self.config.max_terms))
            assert isinstance(result, DensityState)
            return result
        return partial_trace(state, targets, self.config.local_dimensions, self.config.max_terms)

    def prepare(
        self, record_id: int, register_index: int, instrument: Instrument, *, cause: int | None = None
    ) -> EventDecision:
        """Resolve branches before asking the external sampler for a ticket.

        A record identity binds one instrument at one register_index. Calling prepare is
        an explicit request from a configured rule, not proof an event occurred.
        No occupancy precondition or guessed uncomputed path is required.
        """
        if checked(record_id) < 0 or type(instrument) not in (LocalInstrument, GroupedInstrument):
            raise ValueError("non-negative record id and local instrument required")
        self._validate_register_index(register_index)
        groups = outcome_groups(instrument)
        if len(groups[0][0]) != self.config.local_dimensions[register_index]:
            raise ValueError("instrument dimension and register disagree")
        if cause is not None:
            causal = self.event_space.event(cause)
            if causal.tick != self.tick or self.config.addresses[register_index] not in causal.addresses:
                raise ValueError("instrument trigger must be local and current")
        old = self._prepared.get(record_id)
        if old is not None:
            if (
                old.register_index != register_index
                or old.instrument != instrument
                or old.cause != cause
            ):
                raise ValueError("record identity cannot be rebound")
            if record_id not in self._records and old.revision != self._revision:
                raise ValueError("pending decision is stale; use a new record identity")
            return old
        if len(self._prepared) >= self.config.max_records:
            raise OverflowError("quantum decision budget exceeded")
        self._room(1)
        ids, _ = self._plan((register_index,))
        state, _ = self._evaluate(ids)
        weights = tuple(
            trace(
                evolve(
                    state, group, (register_index,), self.config.max_terms, self.config.local_dimensions
                )
            )
            for group in groups
        )
        decision = EventDecision(
            record_id,
            self.tick,
            self._revision,
            register_index,
            instrument,
            weights,
            len(ids),
            cause=cause,
        )
        if decision.total_weight == 0:
            raise ArithmeticError("zero total branch weight")
        self._count_query(len(ids))
        self._prepared[record_id] = decision
        return decision

    def commit(self, decision: EventDecision, ticket: int | None = None) -> NetworkRecord:
        """Commit one result, with no clock advance or new hidden values.

        Supply a uniform integer in [0,total_weight) only for nondeterministic
        decisions. A certain result needs no random number. Repeated commits
        return the immutable original record without interpreting a new ticket.
        """
        if type(decision) is not EventDecision or self._prepared.get(decision.record_id) is not decision:
            raise ValueError("decision was not prepared by this quantum owner")
        previous = self._records.get(decision.record_id)
        if previous is not None:
            return previous
        if decision.revision != self._revision:
            raise ValueError("network changed after branch preparation")
        positive = [i for i, weight in enumerate(decision.weights) if weight]
        if len(positive) == 1 and ticket is None:
            outcome = positive[0]
        else:
            if ticket is None or not 0 <= checked(ticket) < decision.total_weight:
                raise ValueError("uniform integer ticket outside branch weights")
            outcome, running = -1, 0
            for i, weight in enumerate(decision.weights):
                running = checked(running + weight)
                if ticket < running:
                    outcome = i
                    break
        self._room(1)
        revision = checked(self._revision + 1)
        parents = (self._head(decision.register_index),)
        ids, register_indices = self._ancestors(parents)
        if len(ids) + 1 > self.config.max_eval_nodes:
            raise OverflowError("record dependency budget exceeded")
        i = self.event_space.next_id
        group = outcome_groups(decision.instrument)[outcome]
        node = NetworkEvent(
            i,
            self.tick,
            (decision.register_index,),
            parents,
            group[0] if len(group) == 1 else None,
            outcome=outcome,
            channel=group if len(group) > 1 else (),
        )
        record = NetworkRecord(decision, outcome, i)
        self._store(node, decision.cause)
        self._constraints[i] = (frozenset(ids | {i}), frozenset(register_indices))
        self._records[decision.record_id] = record
        self._revision = revision
        return record

    def checkpoint(self, register_index: int) -> int:
        """Replace a full live connected component, preserving residual coherence.

        This is host compaction, never a local physical event or a lottery.
        Records remain in the audit ledger; stale prepared decisions are rejected.
        An omitted branch is not deleted until its complete replacement is saved.
        """
        self._validate_register_index(register_index)
        register_indices: tuple[int, ...] = (register_index,)
        while True:
            ids, grown = self._plan(register_indices)
            if grown == register_indices:
                break
            register_indices = grown
        state, _ = self._evaluate(ids)
        revision = checked(self._revision + 1)
        self.event_space.require_room(1)
        new = NetworkEvent(self.event_space.next_id, self.tick, register_indices, state=state)
        events = {**{i: self._event(i) for i in self._payloads}, new.id: new}
        heads = tuple(new.id if q in register_indices else head for q, head in enumerate(self.heads))
        constraints = {i: cone for i, cone in self._constraints.items() if i not in ids}
        live: set[int] = set()
        stack = list(heads) + list(constraints)
        while stack:
            i = stack.pop()
            if i in live:
                continue
            if len(live) >= self.config.max_eval_nodes:
                raise OverflowError("checkpoint reachability budget exceeded")
            live.add(i)
            stack.extend(events[i].parents)
        if len(live) > self.config.max_nodes:
            raise OverflowError("checkpoint node budget exceeded")
        self._store(new, checkpoint=True)
        self._payloads = {i: payload for i, payload in self._payloads.items() if i in live}
        self._constraints = constraints
        self._revision = revision
        return new.id
