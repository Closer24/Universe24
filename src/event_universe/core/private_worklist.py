"""Sparse and dense scheduling of one shared private Register transport law."""

from dataclasses import dataclass
from typing import Literal, Protocol

from .private_reference import DenseSelector
from .private_register import PRIVATE_PORT_PAIRS, PrivateKey, PrivateNode, RegisterDatum
from .private_transport import CausalTransport, PeriodicWiring


class Selector(Protocol):
    checks: int

    def select(self, due: frozenset[PrivateKey]) -> tuple[PrivateKey, ...]: ...


class SparseSelector:
    """Visit only actual received-input handles; no dormant Register scan."""

    def __init__(self) -> None:
        self.checks = 0

    def select(self, due: frozenset[PrivateKey]) -> tuple[PrivateKey, ...]:
        self.checks += len(due)
        return tuple(sorted(due))


@dataclass(frozen=True)
class TransferEvent:
    tick: int
    kind: Literal["receive", "send"]
    source: PrivateKey
    target: PrivateKey
    codes: tuple[int, ...]
    due_tick: int


class PrivateSimulation:
    """Explicit identity transport profile, separate from whole-Node physics.

    Nodes only contain 24 private units. Routing, due handles, history and global
    time belong to this host adapter and are never arguments of the local law.
    """

    def __init__(
        self,
        wiring: PeriodicWiring,
        seeds: tuple[tuple[PrivateKey, RegisterDatum], ...],
        *,
        strategy: Literal["dense", "sparse"] = "sparse",
    ) -> None:
        if strategy not in ("dense", "sparse"):
            raise ValueError("private execution strategy must be dense or sparse")
        self.wiring = wiring
        self.nodes = {address: PrivateNode() for address in wiring.nodes}
        self.transport = CausalTransport(wiring, seeds)
        self.selector: Selector = (
            DenseSelector(wiring.nodes) if strategy == "dense" else SparseSelector()
        )
        self.tick = 0
        self.transitions = 0
        self.events: list[TransferEvent] = []

    def step(self) -> None:
        due = self.transport.pending_inputs(self.tick)
        selected = self.selector.select(due)
        if len(selected) != len(due) or frozenset(selected) != due:
            raise ValueError("scheduler must dispatch exactly the actual due Register cohort")
        receipts = self.transport.receive(self.tick)
        for source, packet in receipts:
            self.events.append(
                TransferEvent(
                    self.tick, "receive", source, packet.target, packet.datum.codes, packet.due_tick
                )
            )
        for key in selected:
            received = self.transport.inputs[key]
            output = self.nodes[key.node].unit(key.from_port, key.to_port).advance(received)
            if output is None:
                raise ValueError("the identity profile must emit its actual received datum")
            packet = self.transport.emit(key, output, self.tick)
            self.events.append(
                TransferEvent(self.tick, "send", key, packet.target, output.codes, packet.due_tick)
            )
            self.transitions += 1
        self.tick += 1

    def work_report(self) -> dict[str, int]:
        return {
            "register_checks": self.selector.checks,
            "nonempty_transitions": self.transitions,
            **self.transport.queue_report(),
        }

    def canonical_state(self) -> tuple[object, ...]:
        """Read all private owners, causal deadlines and events for comparison.

        This complete observation may scan the world. It never runs within the
        measured step or supplies input to a private physical calculation.
        """
        private_states = tuple(
            (PrivateKey(address, *pair), unit.state.codes)
            for address, node in sorted(self.nodes.items())
            for pair, unit in zip(PRIVATE_PORT_PAIRS, node.units, strict=True)
        )
        inputs = tuple((key, datum.codes) for key, datum in sorted(self.transport.inputs.items()))
        channels = tuple(
            (source, packet.target, packet.datum.codes, packet.due_tick)
            for source, packet in sorted(self.transport.channels.items())
        )
        return self.tick, private_states, inputs, channels, tuple(self.events)
