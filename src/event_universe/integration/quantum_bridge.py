"""Sole adapter between spacetime records and the shared quantum-history owner.

No ScalarEngine reference, write callback, automatic polling, or physical commit is
allowed here. The caller supplies current world time and explicit quantum input.
"""

from dataclasses import dataclass

from event_universe.core.state import Address, checked
from event_universe.quantum import (
    ORACLE_COST,
    Amplitude,
    DeferredQuantum,
    FocusReply,
    FocusRequest,
    FocusSet,
    OracleCost,
    QuantumQuery,
    QuantumReply,
)
from event_universe.quantum.state import checked_address
from event_universe.quantum.terminal import TerminalReply, TerminalSetup


@dataclass(frozen=True, slots=True)
class QuantumEventRef:
    event_id: int
    address: Address
    tick: int
    quantum_node: int

    def __post_init__(self) -> None:
        checked(self.event_id)
        checked(self.tick)
        checked(self.quantum_node)
        checked_address(self.address)
        if min(self.event_id, self.tick, self.quantum_node) < 0:
            raise ValueError("event reference identifiers and tick must be non-negative")


@dataclass(frozen=True, slots=True)
class QuantumMeasurement:
    """Legacy name: an amplitude query, not an outcome or physical collapse."""

    event_id: int
    amplitude: Amplitude
    weight: int
    evaluation_nodes: int

    @property
    def cost(self) -> OracleCost:
        return ORACLE_COST


class QuantumBridge:
    """Application adapter; all quantum state/cache belongs to DeferredQuantum."""

    def __init__(self, quantum: DeferredQuantum) -> None:
        self._quantum = quantum

    def prepare(
        self, event_id: int, address: Address, tick: int, real: int, imag: int = 0
    ) -> QuantumEventRef:
        checked(event_id)
        if event_id < 0:
            raise ValueError("event id must be non-negative")
        node = self._quantum.source(address, tick, real, imag)
        return QuantumEventRef(event_id, address, tick, node)

    def phase(self, source: QuantumEventRef, address: Address, tick: int, quarter_turns: int) -> int:
        return self._quantum.phase(source.quantum_node, address, tick, quarter_turns)

    def interfere(self, left: int, right: int, address: Address, tick: int) -> int:
        return self._quantum.sum2(left, right, address, tick)

    def query_node(self, root: int, address: Address, tick: int) -> QuantumReply:
        """Explicit fixed-size call; does not turn every node into a detector.

        One invocation is one model unit. Repeated host probes are allowed and
        remain read-only; the physical scheduler, if added later, must bound its
        invocations per local update. This bridge never polls the world itself.
        """
        return self._quantum.query(QuantumQuery(root, address, tick))

    def bind_focus_set(self, focus_set_id: int, focus_set: FocusSet) -> None:
        """Configure a bounded candidate set in the quantum owner, not in a node."""
        self._quantum.bind_focus_set(focus_set_id, focus_set)

    def focus_event(self, request: FocusRequest) -> FocusReply:
        """Send one fixed-size request for one event/no-event focus decision."""
        return self._quantum.focus_event(request)

    def measure(self, event_id: int, root: int) -> QuantumMeasurement:
        """Compatibility adapter through the same oracle; no second evaluator.

        With no world timestamp argument, this historical API queries at the
        root's recorded time. Use query_node for an explicitly stamped node call.
        """
        checked(event_id)
        if event_id < 0:
            raise ValueError("event id must be non-negative")
        node = self._quantum.node(root)
        reply = self.query_node(root, (node.x, node.y, node.z), node.tick)
        return QuantumMeasurement(event_id, reply.amplitude, reply.weight, reply.evaluation_nodes)

    def bind_terminal_trial(self, setup: TerminalSetup) -> None:
        """Explicit test-only binding; state belongs to the quantum owner."""
        self._quantum.bind_terminal_trial(setup)

    def read_terminal_trial(self, tick: int, ticket: int) -> TerminalReply:
        """Return trial result, never write a physical detector or ScalarEngine event."""
        return self._quantum.read_terminal_trial(tick, ticket)
