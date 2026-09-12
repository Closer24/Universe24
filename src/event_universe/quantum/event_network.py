"""Demand-driven joint-state backend owned by DeferredQuantum.

Acyclic per-cell heads describe the wave; pure queries never select old paths.
Recorded constraints close the conservative backward cone. Only an explicitly
supplied local instrument can commit an outcome. This is an opt-in finite
quantum candidate, not a field law or an Engine-native event producer.
"""

from copy import copy
from dataclasses import dataclass

from event_universe.core.event_space import CausalEventSpace
from event_universe.core.lattice import PeriodicLattice
from event_universe.core.state import Address, checked, checked_work

from .event_rules import (
    LocalInstrument,
    LocalUnitary,
    Matrix,
    State,
    apply_matrix,
    multiply,
    reduce_state,
    squared_norm,
)
from .state import Amplitude, checked_address

EVENT_NETWORK_MODEL_ID = "deferred-event-network-v1"


@dataclass(frozen=True, slots=True)
class EventNetworkConfig:
    addresses: tuple[Address, ...]
    occupied: tuple[int, ...] = ()
    max_nodes: int = 10_000
    max_eval_nodes: int = 10_000
    max_terms: int = 4_096
    max_records: int = 1_024
    modes_per_cell: int = 1
    shape: Address | None = None
    boundary: str = "open"
    initial_state: State | None = None

    def __post_init__(self) -> None:
        if type(self.addresses) is not tuple or not 1 <= len(self.addresses) <= 30:
            raise ValueError("one to thirty immutable addresses are supported")
        for address in self.addresses:
            checked_address(address)
        if not 1 <= checked(self.modes_per_cell) <= 8:
            raise ValueError("one to eight modes per cell are supported")
        if any(self.addresses.count(a) > self.modes_per_cell for a in self.addresses):
            raise ValueError("cell addresses must be distinct unless local modes are selected")
        if self.boundary not in ("open", "periodic"):
            raise ValueError("unknown quantum boundary policy")
        if self.boundary == "periodic" and self.shape is None:
            raise ValueError("periodic modes require an explicit shape")
        if self.shape is not None:
            lattice = PeriodicLattice(self.shape)
            if any(lattice.wrap(a) != a for a in self.addresses):
                raise ValueError("mode address outside declared shape")
        if type(self.occupied) is not tuple:
            raise TypeError("occupied cells must be immutable")
        for site in self.occupied:
            checked(site)
            if not 0 <= site < len(self.addresses):
                raise ValueError("occupied cell outside network")
        if len(set(self.occupied)) != len(self.occupied):
            raise ValueError("duplicate initial occupation")
        for value in (self.max_nodes, self.max_eval_nodes, self.max_terms, self.max_records):
            if checked(value) <= 0:
                raise ValueError("positive quantum resource budgets required")
        if self.max_nodes < len(self.addresses):
            raise ValueError("node budget cannot hold initial sources")
        if self.initial_state is not None:
            if self.occupied or type(self.initial_state) is not tuple:
                raise ValueError("supply either occupations or an immutable joint initial state")
            if not 1 <= len(self.initial_state) <= self.max_terms:
                raise ValueError("initial state exceeds the term capacity")
            seen: set[int] = set()
            for bits, amp in self.initial_state:
                if not 0 <= checked(bits) < 1 << len(self.addresses) or bits in seen:
                    raise ValueError("invalid or duplicate initial occupation mask")
                seen.add(bits)
                if type(amp) is not Amplitude or amp == (0, 0):
                    raise ValueError("nonzero bounded initial amplitude required")
                checked(amp.real)
                checked(amp.imag)
            if squared_norm(self.initial_state) <= 0:
                raise ValueError("nonzero initial state required")


@dataclass(frozen=True, slots=True)
class NetworkEvent:
    id: int
    tick: int
    sites: tuple[int, ...]
    parents: tuple[int, ...] = ()
    matrix: Matrix | None = None
    state: State | None = None
    outcome: int = -1


@dataclass(frozen=True, slots=True)
class NetworkQuery:
    weights: tuple[int, int]
    evaluated_nodes: int
    peak_terms: int
    model_cost: int = 1
    world_ticks: int = 0


@dataclass(frozen=True, slots=True)
class EventDecision:
    record_id: int
    tick: int
    revision: int
    site: int
    instrument: LocalInstrument
    weights: tuple[int, ...]
    evaluated_nodes: int
    model_cost: int = 1
    world_ticks: int = 0
    address: Address = (0, 0, 0)
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
    sites: tuple[int, ...]
    matrix: Matrix | None
    state: State | None
    outcome: int


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
        self._addresses = config.addresses
        self._tick = 0
        self._revision = 0
        self.event_space = (
            event_space
            if event_space is not None
            else CausalEventSpace(shape=config.shape, boundary=config.boundary)
        )
        self.event_space.require_room(1 if config.initial_state is not None else len(config.addresses))
        self._payloads: dict[int, QuantumPayload] = {}
        self._heads: dict[int, int] = {}
        if config.initial_state is not None:
            node = NetworkEvent(
                self.event_space.next_id,
                0,
                tuple(range(len(config.addresses))),
                state=reduce_state(config.initial_state),
            )
            self._store(node)
            self._heads = dict.fromkeys(node.sites, node.id)
        else:
            for q in range(len(config.addresses)):
                node = NetworkEvent(
                    self.event_space.next_id,
                    0,
                    (q,),
                    state=(((1 << q) if q in config.occupied else 0, Amplitude(1, 0)),),
                )
                self._store(node)
                self._heads[q] = node.id
        self._support_heads = self._heads.copy()
        self._constraints: dict[int, tuple[frozenset[int], frozenset[int]]] = {}
        self._prepared: dict[int, EventDecision] = {}
        self._records: dict[int, NetworkRecord] = {}
        self._queries = 0
        self._evaluated = 0

    def _store(
        self, node: NetworkEvent, cause: int | None = None, *, physical_parents: tuple[int, ...] = ()
    ) -> None:
        parents = node.parents if cause is None else (*node.parents, cause)
        event = self.event_space.append(
            tick=node.tick,
            addresses=tuple(self.addresses[q] for q in node.sites),
            owner="quantum",
            kind="record" if node.outcome >= 0 else "state" if node.state is not None else "operation",
            parents=parents,
            physical_parents=physical_parents,
            payload_ref=node.id,
        )
        if event.id != node.id:
            raise ValueError("event identity changed during insertion")
        self._payloads[event.id] = QuantumPayload(node.sites, node.matrix, node.state, node.outcome)

    def _event(self, identity: int) -> NetworkEvent:
        payload = self._payloads[identity]
        event = self.event_space.event(identity)
        return NetworkEvent(
            identity,
            event.tick,
            payload.sites,
            tuple(i for i in event.parents if i in self._payloads),
            payload.matrix,
            payload.state,
            payload.outcome,
        )

    @property
    def config(self) -> EventNetworkConfig:
        return self._config

    @property
    def addresses(self) -> tuple[Address, ...]:
        return self._addresses

    @property
    def node_count(self) -> int:
        return len(self._payloads)

    @property
    def tick(self) -> int:
        return self._tick

    @property
    def heads(self) -> tuple[int, ...]:
        return tuple(self._heads[q] for q in range(len(self.config.addresses)))

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

    def _site(self, site: int) -> None:
        checked(site)
        if not 0 <= site < len(self.config.addresses):
            raise ValueError("site outside network")

    def _room(self, count: int) -> None:
        self.event_space.require_room(count)
        checked(self.event_space.next_id + count)
        if len(self._payloads) + count > self.config.max_nodes:
            raise OverflowError("quantum node budget exceeded")

    def step(self, operations: tuple[tuple[LocalUnitary, tuple[int, ...]], ...]) -> None:
        """One tick of disjoint local operations, validated before any mutation."""
        if type(operations) is not tuple:
            raise TypeError("immutable operation layer required")
        tick = checked(self.tick + 1)
        revision = checked(self._revision + 1)
        self._room(len(operations))
        used: set[int] = set()
        nodes: list[NetworkEvent] = []
        for rule, sites in operations:
            if type(rule) is not LocalUnitary or type(sites) is not tuple:
                raise TypeError("local coherent rule and immutable sites required")
            limit = 4 if self.config.modes_per_cell > 1 else 2
            if not 1 <= len(sites) <= limit or len(rule.matrix) != 1 << len(sites):
                raise ValueError("rule dimension and sites disagree")
            for site in sites:
                self._site(site)
                if site in used:
                    raise ValueError("a site cannot occur twice in a physical tick")
                used.add(site)
            addresses = tuple(self.addresses[q] for q in sites)
            if len(sites) > 2 and len(set(addresses)) != 1:
                raise ValueError("multi-mode interactions must be in one cell")
            if len(sites) == 2:
                a, b = (self.addresses[q] for q in sites)
                distance = sum(abs(checked_work(x - y)) for x, y in zip(a, b, strict=True))
                local = a == b and self.config.modes_per_cell > 1
                if self.config.shape is not None and self.config.boundary == "periodic":
                    distance = 1 if b in PeriodicLattice(self.config.shape).neighbors(a) else distance
                if not local and distance != 1:
                    raise ValueError("only cardinal nearest-neighbor operations are allowed")
            parents = tuple(dict.fromkeys(self._heads[q] for q in sites))
            nodes.append(
                NetworkEvent(self.event_space.next_id + len(nodes), tick, sites, parents, rule.matrix)
            )
        for node in nodes:
            self._store(node)
            for site in node.sites:
                self._heads[site] = node.id
                self._support_heads[site] = node.id
        self._tick, self._revision = tick, revision

    def advance(
        self,
        operations: tuple[tuple[LocalUnitary, tuple[int, ...]], ...],
        observations: tuple[tuple[int, int, LocalInstrument, int | None], ...] = (),
        transfers: tuple[tuple[int, Address], ...] = (),
    ) -> None:
        """Atomically install one tick and explicit records in this quantum owner.

        Staging copies host graph containers, not another physical world. Failed
        tickets, arithmetic or capacity checks leave all committed state unchanged.
        Callers must reserve local modes before supplying the disjoint batch.
        """
        staged = copy(self)
        staged.event_space = self.event_space.stage()
        staged._payloads = self._payloads.copy()
        staged._heads = self._heads.copy()
        staged._support_heads = self._support_heads.copy()
        staged._constraints = self._constraints.copy()
        staged._prepared = self._prepared.copy()
        staged._records = self._records.copy()
        used = {site for _, sites in operations for site in sites}
        destinations = list(self.addresses)
        moving: set[int] = set()
        for site, destination in transfers:
            self._site(site)
            checked_address(destination)
            if site in used or site in moving:
                raise ValueError("a transferred mode cannot interact in the same tick")
            moving.add(site)
            origin = self.addresses[site]
            if self.config.shape is not None and self.config.boundary == "periodic":
                valid = destination in PeriodicLattice(self.config.shape).neighbors(origin)
            else:
                valid = (
                    sum(abs(checked_work(a - b)) for a, b in zip(origin, destination, strict=True)) == 1
                )
                if self.config.shape is not None:
                    valid = valid and PeriodicLattice(self.config.shape).wrap(destination) == destination
            if not valid or destination == origin:
                raise ValueError("a mode transfer must cross one declared neighbor link")
            support = self.event_space.event(self._support_heads[site])
            if checked(self.tick + 1) - support.tick < self.event_space.link_ticks:
                raise ValueError("a mode transfer requires a completed local link")
            destinations[site] = destination
        if any(destinations.count(a) > self.config.modes_per_cell for a in destinations):
            raise OverflowError("arrival exceeds the local mode capacity")
        observed: set[int] = set()
        for _, site, _, _ in observations:
            if site in used or site in observed or site in moving:
                raise ValueError("observation overlaps another operation in this tick")
            observed.add(site)
        from .mode_rules import IDENTITY

        staged._room(len(operations) + len(moving) + len(observations))
        staged.step(operations)
        staged._addresses = tuple(destinations)
        for site, _ in transfers:
            parents = (staged._heads[site],)
            node = NetworkEvent(staged.event_space.next_id, staged.tick, (site,), parents, IDENTITY)
            staged._store(node, physical_parents=(staged._support_heads[site],))
            staged._heads[site] = node.id
            staged._support_heads[site] = node.id
        for record_id, site, instrument, ticket in observations:
            staged.commit(staged.prepare(record_id, site, instrument), ticket)
        self.event_space.adopt(staged.event_space)
        staged.event_space = self.event_space
        self.__dict__.update(staged.__dict__)

    def _ancestors(self, roots: tuple[int, ...]) -> tuple[set[int], set[int]]:
        found: set[int] = set()
        sites: set[int] = set()
        stack = list(roots)
        while stack:
            i = stack.pop()
            if i in found:
                continue
            if len(found) >= self.config.max_eval_nodes:
                raise OverflowError("backward dependency budget exceeded")
            node = self._event(i)
            found.add(i)
            sites.update(node.sites)
            stack.extend(node.parents)
        return found, sites

    def _plan(self, targets: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
        for site in targets:
            self._site(site)
        ids, sites = self._ancestors(tuple(self._heads[q] for q in targets))
        while True:
            grew = False
            for i, (record_ids, record_sites) in self._constraints.items():
                if i not in ids and sites.intersection(record_sites):
                    if len(ids | record_ids) > self.config.max_eval_nodes:
                        raise OverflowError("conditional dependency budget exceeded")
                    ids.update(record_ids)
                    sites.update(record_sites)
                    grew = True
            if not grew:
                return tuple(sorted(ids)), tuple(sorted(sites))

    def _evaluate(self, ids: tuple[int, ...]) -> tuple[State, int]:
        value: State = ((0, Amplitude(1, 0)),)
        initialized: set[int] = set()
        peak = 1
        for i in ids:
            node = self._event(i)
            if node.state is not None:
                if initialized.intersection(node.sites):
                    raise ArithmeticError("overlapping checkpoint sources")
                initialized.update(node.sites)
                if len(value) * len(node.state) > self.config.max_terms:
                    raise OverflowError("quantum tensor-product budget exceeded")
                value = tuple(sorted((a | b, multiply(x, y)) for a, x in value for b, y in node.state))
        peak = max(peak, len(value))
        for i in ids:
            node = self._event(i)
            if node.matrix is not None:
                value = apply_matrix(value, node.matrix, node.sites, self.config.max_terms)
                value = reduce_state(value)
                peak = max(peak, len(value))
        return value, peak

    def _count_query(self, nodes: int) -> None:
        queries = checked_work(self._queries + 1)
        evaluated = checked_work(self._evaluated + nodes)
        self._queries, self._evaluated = queries, evaluated

    def query(self, site: int) -> NetworkQuery:
        """Compute a local marginal; never sample or alter a physical record."""
        ids, _ = self._plan((site,))
        state, peak = self._evaluate(ids)
        weights = [0, 0]
        for bits, amp in state:
            outcome = (bits >> site) & 1
            weights[outcome] = checked(weights[outcome] + squared_norm(((bits, amp),)))
        checked(weights[0] + weights[1])
        reply = NetworkQuery((weights[0], weights[1]), len(ids), peak)
        self._count_query(len(ids))
        return reply

    def joint_state(self) -> State:
        """Read-only host diagnostic, not a fixed-size physical cell reply."""
        ids, _ = self._plan(tuple(range(len(self.config.addresses))))
        return self._evaluate(ids)[0]

    def prepare(
        self, record_id: int, site: int, instrument: LocalInstrument, *, cause: int | None = None
    ) -> EventDecision:
        """Resolve branches before asking the external sampler for a ticket.

        A record identity binds one instrument at one site. Calling prepare is
        an explicit request from a configured rule, not proof an event occurred.
        No occupancy precondition or guessed uncomputed path is required.
        """
        if checked(record_id) < 0 or type(instrument) is not LocalInstrument:
            raise ValueError("non-negative record id and local instrument required")
        self._site(site)
        if cause is not None:
            causal = self.event_space.event(cause)
            if causal.tick != self.tick or self.addresses[site] not in causal.addresses:
                raise ValueError("instrument trigger must be local and current")
        old = self._prepared.get(record_id)
        if old is not None:
            if old.site != site or old.instrument != instrument or old.cause != cause:
                raise ValueError("record identity cannot be rebound")
            if record_id not in self._records and old.revision != self._revision:
                raise ValueError("pending decision is stale; use a new record identity")
            return old
        if len(self._prepared) >= self.config.max_records:
            raise OverflowError("quantum decision budget exceeded")
        self._room(1)
        ids, _ = self._plan((site,))
        state, _ = self._evaluate(ids)
        weights = tuple(
            squared_norm(apply_matrix(state, matrix, (site,), self.config.max_terms))
            for matrix in instrument.branches
        )
        decision = EventDecision(
            record_id,
            self.tick,
            self._revision,
            site,
            instrument,
            weights,
            len(ids),
            address=self.addresses[site],
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
        parents = (self._heads[decision.site],)
        ids, sites = self._ancestors(parents)
        if len(ids) + 1 > self.config.max_eval_nodes:
            raise OverflowError("record dependency budget exceeded")
        i = self.event_space.next_id
        node = NetworkEvent(
            i,
            self.tick,
            (decision.site,),
            parents,
            decision.instrument.branches[outcome],
            outcome=outcome,
        )
        record = NetworkRecord(decision, outcome, i)
        self._store(node, decision.cause)
        self._heads[decision.site] = i
        self._support_heads[decision.site] = i
        self._constraints[i] = (frozenset(ids | {i}), frozenset(sites))
        self._records[decision.record_id] = record
        self._revision = revision
        return record

    def checkpoint(self, site: int) -> int:
        """Replace a full live connected component, preserving residual coherence.

        This is host compaction, never a local physical event or a lottery.
        Records remain in the audit ledger; stale prepared decisions are rejected.
        An omitted branch is not deleted until its complete replacement is saved.
        """
        self._site(site)
        sites: tuple[int, ...] = (site,)
        while True:
            ids, grown = self._plan(sites)
            if grown == sites:
                break
            sites = grown
        state, _ = self._evaluate(ids)
        revision = checked(self._revision + 1)
        self.event_space.require_room(1)
        new = NetworkEvent(self.event_space.next_id, self.tick, sites, state=state)
        events = {**{i: self._event(i) for i in self._payloads}, new.id: new}
        heads = {**self._heads, **dict.fromkeys(sites, new.id)}
        constraints = {i: cone for i, cone in self._constraints.items() if i not in ids}
        live: set[int] = set()
        stack = list(heads.values()) + list(constraints)
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
        self._store(new)
        self._payloads = {i: payload for i, payload in self._payloads.items() if i in live}
        self._heads, self._constraints = heads, constraints
        self._revision = revision
        return new.id
