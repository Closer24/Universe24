"""A shared, bounded deferred-history owner with unit-model-cost queries.

The oracle postulate is implemented by query methods, not by pretending host DAG
traversal is constant-time. Queries do not mutate source facts, advance world
time, or commit native physical events. Host evaluation has explicit budgets.
"""

from event_universe.core.state import Address, checked, checked_work

from .focus import FocusReply, FocusRequest, WeightedFocusCandidate, select_focused_event
from .query import QuantumQuery, QuantumQueryStats, QuantumReply
from .state import (
    EMPTY_NODE,
    Q_PHASE,
    Q_SOURCE,
    Q_SUM2,
    Amplitude,
    QuantumConfig,
    QuantumNode,
    add_amp,
    amplitude_weight,
    checked_address,
    checked_amp,
    phase_quarter_turns,
)
from .terminal import TerminalRecord, TerminalReply, TerminalSetup, choose_output


class DeferredQuantum:
    """Single owner of history, query cache and accounting for one quantum space."""

    def __init__(self, config: QuantumConfig | None = None) -> None:
        self._config = config if config is not None else QuantumConfig()
        self._nodes: list[QuantumNode] = []
        self._query_cache: dict[int, tuple[Amplitude, int]] = {}
        self._query_stats = QuantumQueryStats()
        self._terminal_setup: TerminalSetup | None = None
        self._terminal_record: TerminalRecord | None = None
        self._terminal_calls = 0
        self._terminal_work = 0

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def cached_result_count(self) -> int:
        return len(self._query_cache)

    @property
    def query_stats(self) -> QuantumQueryStats:
        return self._query_stats

    def _append(self, node: QuantumNode) -> int:
        if len(self._nodes) >= self._config.max_nodes:
            raise OverflowError("quantum node budget exceeded")
        self._nodes.append(node)
        return len(self._nodes) - 1

    def _where(self, address: Address, tick: int) -> tuple[int, int, int, int]:
        x, y, z = checked_address(address)
        checked(tick)
        if tick < 0:
            raise ValueError("quantum world tick must be non-negative")
        return x, y, z, tick

    def source(self, address: Address, tick: int, real: int, imag: int = 0) -> int:
        amp = checked_amp(real, imag)
        x, y, z, tick = self._where(address, tick)
        return self._append(
            QuantumNode(Q_SOURCE, EMPTY_NODE, EMPTY_NODE, amp.real, amp.imag, 0, x, y, z, tick)
        )

    def phase(self, parent: int, address: Address, tick: int, quarter_turns: int) -> int:
        x, y, z, tick = self._where(address, tick)
        self._require_local_parent(parent, address, tick)
        return self._append(
            QuantumNode(Q_PHASE, parent, EMPTY_NODE, 0, 0, checked(quarter_turns) % 4, x, y, z, tick)
        )

    def sum2(self, left: int, right: int, address: Address, tick: int) -> int:
        x, y, z, tick = self._where(address, tick)
        self._require_local_parent(left, address, tick)
        self._require_local_parent(right, address, tick)
        return self._append(QuantumNode(Q_SUM2, left, right, 0, 0, 0, x, y, z, tick))

    def _require_node(self, node_id: int) -> None:
        checked(node_id)
        if node_id < 0 or node_id >= len(self._nodes):
            raise IndexError("unknown quantum node")

    def node(self, node_id: int) -> QuantumNode:
        """Return an immutable record, never an alias to mutable state."""
        self._require_node(node_id)
        return self._nodes[node_id]

    def _require_local_parent(self, parent: int, address: Address, tick: int) -> None:
        """Validate recorded physical edges; oracle evaluation is not such an edge."""
        node = self.node(parent)
        dx = abs(checked_work(address[0] - node.x))
        dy = abs(checked_work(address[1] - node.y))
        dz = abs(checked_work(address[2] - node.z))
        distance = checked_work(dx + dy + dz)
        if tick < node.tick:
            raise ValueError("quantum operation cannot precede a parent event")
        if distance > 1:
            raise ValueError("quantum history edge must stay local to six cardinal neighbors")
        if tick - node.tick < distance:
            raise ValueError("quantum history edge arrives before its causal tick")

    def resolve(self, root: int, *, node_budget: int | None = None) -> tuple[Amplitude, int]:
        """Evaluate reachable ancestors only; return amplitude and evaluated-node count."""
        self._require_node(root)
        budget = self._config.max_eval_nodes
        if node_budget is not None:
            checked(node_budget)
            if node_budget < 0:
                raise ValueError("evaluation budget must be non-negative")
            budget = min(budget, node_budget)
        memo: dict[int, Amplitude] = {}
        discovered: set[int] = set()
        stack: list[tuple[int, int]] = [(root, 0)]
        work = 0
        while stack:
            node_id, expanded = stack.pop()
            if node_id in memo:
                continue
            node = self._nodes[node_id]
            if not expanded:
                if node_id not in discovered:
                    if len(discovered) >= budget:
                        raise OverflowError("quantum evaluation budget exceeded")
                    discovered.add(node_id)
                stack.append((node_id, 1))
                if node.kind == Q_PHASE:
                    if node.parent_a not in memo:
                        stack.append((node.parent_a, 0))
                elif node.kind == Q_SUM2:
                    if node.parent_b not in memo:
                        stack.append((node.parent_b, 0))
                    if node.parent_a not in memo:
                        stack.append((node.parent_a, 0))
                elif node.kind != Q_SOURCE:
                    raise ValueError("unknown quantum node kind")
                continue

            work = checked(work + 1)
            if node.kind == Q_SOURCE:
                value = checked_amp(node.value_a, node.value_b)
            elif node.kind == Q_PHASE:
                value = phase_quarter_turns(memo[node.parent_a], node.param)
            else:
                value = add_amp(memo[node.parent_a], memo[node.parent_b])
            memo[node_id] = value
        return memo[root], work

    def query(self, request: QuantumQuery) -> QuantumReply:
        """One model operation, zero simulated ticks, separately bounded host work."""
        if type(request) is not QuantumQuery:
            raise TypeError("query requires an immutable QuantumQuery")
        root = self.node(request.root)
        if request.address != (root.x, root.y, root.z):
            raise ValueError("query must address its local quantum history node")
        if request.tick < root.tick:
            raise ValueError("query cannot read a future quantum history node")

        cached = self._query_cache.get(request.root)
        if cached is None:
            if len(self._query_cache) >= self._config.max_cached_results:
                raise OverflowError("quantum query cache budget exceeded")
            amplitude, work = self.resolve(request.root)
            weight = amplitude_weight(amplitude)
            cache_hit = 0
        else:
            amplitude, weight = cached
            work = 0
            cache_hit = 1

        previous = self._query_stats
        updated = QuantumQueryStats(
            successful_queries=checked_work(previous.successful_queries + 1),
            host_evaluated_nodes=checked_work(previous.host_evaluated_nodes + work),
            cache_hits=checked_work(previous.cache_hits + cache_hit),
        )
        reply = QuantumReply(request, amplitude, weight, work, cache_hit)
        if cached is None:
            self._query_cache[request.root] = (amplitude, weight)
        self._query_stats = updated
        return reply

    def focus_event(self, request: FocusRequest) -> FocusReply:
        """Resolve one spatial event/no-event decision by hierarchical refinement.

        The whole call costs one model oracle operation and zero world ticks. The
        recursive region work and every history evaluation remain host work. The
        same global ticket is narrowed through all levels; focus never resamples.
        """
        if type(request) is not FocusRequest:
            raise TypeError("focus_event requires an immutable FocusRequest")
        weighted: list[WeightedFocusCandidate] = []
        work = 0
        for candidate in request.candidates:
            node = self.node(candidate.root)
            if candidate.address != (node.x, node.y, node.z):
                raise ValueError("focus candidate address must match its quantum root")
            if request.tick < node.tick:
                raise ValueError("focus cannot read a future quantum history node")
            remaining = checked(self._config.max_eval_nodes - work)
            amplitude, used = self.resolve(candidate.root, node_budget=remaining)
            work = checked(work + used)
            weighted.append(
                WeightedFocusCandidate(
                    candidate.root,
                    candidate.address,
                    candidate.outcome,
                    amplitude_weight(amplitude),
                )
            )
        return select_focused_event(request, tuple(weighted), work)

    @property
    def terminal_record(self) -> TerminalRecord | None:
        return self._terminal_record

    @property
    def terminal_calls(self) -> int:
        return self._terminal_calls

    @property
    def terminal_evaluated_nodes(self) -> int:
        return self._terminal_work

    def bind_terminal_trial(self, setup: TerminalSetup) -> None:
        """Bind once; cannot consume the same excitation under a second identity."""
        if type(setup) is not TerminalSetup:
            raise TypeError("terminal setup must be immutable TerminalSetup")
        if self._terminal_setup is not None:
            if self._terminal_setup != setup:
                raise ValueError("terminal trial is already bound")
            return
        for root in (setup.root_a, setup.root_b):
            if self.node(root).tick > setup.tick:
                raise ValueError("terminal setup cannot precede output history")
        self._terminal_setup = setup

    def read_terminal_trial(self, tick: int, ticket: int) -> TerminalReply:
        """Absorbing trial. First ticket must be uniform; repeats reuse the result."""
        checked(tick)
        checked(ticket)
        if tick < 0 or ticket < 0:
            raise ValueError("tick and ticket must be non-negative")
        setup = self._terminal_setup
        if setup is None:
            raise RuntimeError("bind a terminal trial before readout")
        if tick < setup.tick:
            raise ValueError("terminal readout is not causally ready")
        calls = checked_work(self._terminal_calls + 1)
        if self._terminal_record is not None:
            self._terminal_calls = calls
            return TerminalReply(self._terminal_record, 0, 1)
        if tick != setup.tick:
            raise ValueError("first readout must be at its scheduled world tick")
        amp_a, work_a = self.resolve(setup.root_a)
        amp_b, work_b = self.resolve(
            setup.root_b, node_budget=checked(self._config.max_eval_nodes - work_a)
        )
        weight_a, weight_b = amplitude_weight(amp_a), amplitude_weight(amp_b)
        selected = choose_output(weight_a, weight_b, ticket)
        work = checked(work_a + work_b)
        if work > self._config.max_eval_nodes:
            raise OverflowError("combined terminal evaluation budget exceeded")
        total_work = checked_work(self._terminal_work + work)
        root = setup.root_a if selected == 0 else setup.root_b
        node = self.node(root)
        record = TerminalRecord(
            tick, selected, (node.x, node.y, node.z), root, weight_a, weight_b, ticket
        )
        self._terminal_record = record
        self._terminal_calls = calls
        self._terminal_work = total_work
        return TerminalReply(record, work, 0)
