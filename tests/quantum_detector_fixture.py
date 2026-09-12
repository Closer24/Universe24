"""Test-only controller. Detector records are NOT ScalarEngine-native physical events."""

from dataclasses import dataclass

from event_universe.core.scalar_engine import ScalarEngine
from event_universe.core.state import Address
from event_universe.integration.quantum_bridge import QuantumBridge
from event_universe.quantum import DeferredQuantum, QuantumConfig
from event_universe.quantum.terminal import TerminalRecord, TerminalSetup

SOURCE: Address = (3, 3, 3)
PORT_A: Address = (6, 5, 5)
PORT_B: Address = (5, 6, 5)
READOUT_TICK = 8


@dataclass(slots=True)
class DetectorController:
    world: ScalarEngine
    bridge: QuantumBridge
    event: TerminalRecord | None = None
    detector_bits: tuple[int, int] = (0, 0)

    def commit(self, ticket: int) -> TerminalRecord:
        record = self.bridge.read_terminal_trial(self.world.tick, ticket).record
        if record.address not in (PORT_A, PORT_B):
            raise ValueError("result is not at a registered detector")
        if self.event is not None:
            if record != self.event:
                raise ValueError("cannot rewrite a detector record")
            return self.event
        self.detector_bits = (1, 0) if record.detector == 0 else (0, 1)
        self.event = record
        return record


def prepare(turns: int, config: QuantumConfig | None = None):
    """H diag(1,i**turns) H with common output denominator 2 (not evaluated).

    Both outputs are evaluated coherently. Their integer weights sum to 4.
    Spatial paths are explicit 3D six-neighbor hops. This is a prescribed
    interferometer circuit, not emergent field dynamics or arbitrary unitarity.
    """
    q = DeferredQuantum(config)
    bridge = QuantumBridge(q)
    source = bridge.prepare(0, SOURCE, 0, 1).quantum_node
    left, right = source, source
    left_path = [(4, 3, 3), (5, 3, 3), (5, 4, 3), (5, 5, 3), (5, 5, 4), (5, 5, 5)]
    right_path = [(3, 3, 4), (3, 3, 5), (3, 4, 5), (3, 5, 5), (4, 5, 5), (5, 5, 5)]
    for tick, position in enumerate(left_path, 1):
        left = q.phase(left, position, tick, 0)
    for tick, position in enumerate(right_path, 1):
        right = q.phase(right, position, tick, turns if tick == 1 else 0)
    bright = bridge.interfere(left, right, (5, 5, 5), 6)
    minus_right = q.phase(right, (5, 5, 5), 6, 2)
    dark = bridge.interfere(left, minus_right, (5, 5, 5), 6)
    out_a = q.phase(bright, PORT_A, 7, 0)
    out_b = q.phase(dark, PORT_B, 7, 0)
    bridge.bind_terminal_trial(TerminalSetup(out_a, out_b, READOUT_TICK))
    return q, bridge
