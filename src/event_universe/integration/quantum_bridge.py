"""Sole adapter between spacetime records and the shared quantum-history owner.

No Engine reference, write callback, automatic polling, or physical commit is
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

    def query_cell(self, root: int, address: Address, tick: int) -> QuantumReply:
        """Explicit fixed-size call; does not turn every cell into a detector."""
        return self._quantum.query(QuantumQuery(root, address, tick))

    def focus_event(self, request: FocusRequest) -> FocusReply:
        """Ask the single quantum owner to refine one region into event/no-event."""
        return self._quantum.focus_event(request)

    def measure(self, event_id: int, root: int) -> QuantumMeasurement:
        """Compatibility adapter through the same oracle; no second evaluator."""
        checked(event_id)
        if event_id < 0:
            raise ValueError("event id must be non-negative")
        node = self._quantum.node(root)
        reply = self.query_cell(root, (node.x, node.y, node.z), node.tick)
        return QuantumMeasurement(event_id, reply.amplitude, reply.weight, reply.evaluation_nodes)

    def bind_terminal_trial(self, setup: TerminalSetup) -> None:
        """Explicit test-only binding; state belongs to the quantum owner."""
        self._quantum.bind_terminal_trial(setup)

    def read_terminal_trial(self, tick: int, ticket: int) -> TerminalReply:
        """Return trial result, never write a physical detector or Engine event."""
        return self._quantum.read_terminal_trial(tick, ticket)
