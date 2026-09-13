"""Bounded local source-envelope transitions and causally delivered inputs."""

from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from .disturbance_state import Address3, CostMeter, OperationCosts, bounded
from .integer import checked_work
from .source_envelope_state import EnvelopeAmplitude

if TYPE_CHECKING:
    from .node_services import NodeEvents

EnvelopeMatrix = tuple[tuple[tuple[int, int], ...], ...]
EnvelopePlanner = Callable[
    [EnvelopeMatrix, tuple[EnvelopeAmplitude, ...], int, CostMeter], EnvelopeAmplitude
]


def _nonnegative(value: int, name: str) -> int:
    if bounded(value) < 0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def _future(tick: int, *delays: int) -> int:
    value = _nonnegative(tick, "source clock")
    for delay in delays:
        value = bounded(checked_work(value + _nonnegative(delay, "source delay")))
    return value


def _ports(ports: tuple[int, ...]) -> None:
    if type(ports) is not tuple or len(ports) > 6 or len(set(ports)) != len(ports):
        raise ValueError("source propagation requires at most six distinct Ports")
    if any(type(port) is not int or not 0 <= port < 6 for port in ports):
        raise ValueError("source propagation requires Ports zero through five")


@dataclass(frozen=True, slots=True)
class EnvelopeGate:
    """An immutable definition index and this endpoint's local role."""

    matrix_index: int
    row: int
    port: int = -1

    def __post_init__(self) -> None:
        _nonnegative(self.matrix_index, "source matrix index")
        if type(self.row) is not int or self.row not in (0, 1):
            raise ValueError("source gate row must be zero or one")
        if type(self.port) is not int or not -1 <= self.port < 6:
            raise ValueError("source gate Port must be local or one of six neighbors")
        if self.port == -1 and self.row != 0:
            raise ValueError("a one-mode source gate has one output row")


@dataclass(frozen=True, slots=True)
class EnvelopePacket:
    """One frozen neighbor value or terminal notice; never a law or callback."""

    arrival_tick: int
    origin: Address3
    port: int
    source_id: int
    amplitude: EnvelopeAmplitude | None
    epoch: int = -1
    cause_id: int | None = None

    def __post_init__(self) -> None:
        _nonnegative(self.arrival_tick, "source arrival tick")
        _ports((self.port,))
        _nonnegative(self.source_id, "source identity")
        if type(self.origin) is not tuple or len(self.origin) != 3:
            raise ValueError("source packet requires three origin coordinates")
        for coordinate in self.origin:
            _nonnegative(coordinate, "source origin coordinate")
        if self.amplitude is None:
            if self.source_id == 0 or self.epoch != -1:
                raise ValueError("a terminal packet requires a positive source and no gate epoch")
        elif type(self.amplitude) is not EnvelopeAmplitude or bounded(self.epoch) < 0:
            raise ValueError("an amplitude packet requires a value and nonnegative gate epoch")
        if self.cause_id is not None:
            _nonnegative(self.cause_id, "source packet cause")


@dataclass(frozen=True, slots=True)
class PendingEnvelopeGate:
    epoch: int
    ready_tick: int
    source_id: int
    amplitude: EnvelopeAmplitude
    generation: int
    gate: EnvelopeGate


@dataclass(frozen=True, slots=True)
class PendingEnvelopeStop:
    ready_tick: int
    source_id: int
    cause_id: int | None


@dataclass(slots=True)
class SourceEnvelopeNode:
    """One domain's local mode; no world, remote origin or quantum-query access."""

    position: Address3
    source_id: int = 0
    amplitude: EnvelopeAmplitude = EnvelopeAmplitude()
    generation: int = 0
    retired: int = 0
    pending_gate: PendingEnvelopeGate | None = None
    incoming_gate: EnvelopePacket | None = None
    pending_stop: PendingEnvelopeStop | None = None
    output: tuple[EnvelopePacket | None, ...] = (None,) * 12
    cause_id: int | None = None

    def __post_init__(self) -> None:
        if type(self.position) is not tuple or len(self.position) != 3:
            raise ValueError("source Node requires three local coordinates")
        for coordinate in self.position:
            _nonnegative(coordinate, "source Node coordinate")
        for value in (self.source_id, self.generation, self.retired):
            _nonnegative(value, "source Node metadata")
        if type(self.amplitude) is not EnvelopeAmplitude:
            raise TypeError("source Node requires an immutable local amplitude")
        if self.retired and (
            self.source_id != self.retired or self.amplitude.real or self.amplitude.imag
        ):
            raise ValueError("a retired source Node must retain its identity and zero amplitude")
        if not self.source_id and (self.amplitude.real or self.amplitude.imag):
            raise ValueError("an unactivated source Node must retain vacuum")
        if type(self.output) is not tuple or len(self.output) != 12:
            raise ValueError("source output bank requires twelve fixed slots")
        if any(packet is not None and type(packet) is not EnvelopePacket for packet in self.output):
            raise TypeError("source output bank accepts only immutable packets")
        if self.cause_id is not None:
            _nonnegative(self.cause_id, "source Node cause")

    def _identity(self, source_id: int) -> None:
        _nonnegative(source_id, "source identity")
        identities: tuple[int, ...] = (self.source_id, self.retired)
        if self.pending_stop is not None:
            identities = (*identities, self.pending_stop.source_id)
        if self.pending_gate is not None:
            identities = (*identities, self.pending_gate.source_id)
        if self.incoming_gate is not None:
            identities = (*identities, self.incoming_gate.source_id)
        if source_id and any(value not in (0, source_id) for value in identities):
            raise ValueError("a local source envelope cannot mix different origins")

    def _record(
        self,
        kind: str,
        tick: int,
        events: NodeEvents,
        *,
        causes: tuple[int, ...] = (),
        cost: int = 0,
    ) -> tuple[int | None, dict[str, object]]:
        parents = tuple(dict.fromkeys(parent for parent in causes if parent != self.cause_id))
        return events.record(
            kind,
            tick,
            self.position,
            self.cause_id,
            causes=parents,
            event_cost=cost,
            owner="source-envelope",
        )

    def _terminal_outputs(
        self,
        source_id: int,
        tick: int,
        ports: tuple[int, ...],
        send_delay: int,
        link_ticks: int,
        cause_id: int | None,
    ) -> tuple[EnvelopePacket | None, ...]:
        _ports(ports)
        if bounded(link_ticks) < 1:
            raise ValueError("source Links require positive transit time")
        arrival = _future(tick, send_delay, link_ticks)
        if len(self.output) != 12:
            raise ValueError("source output bank requires twelve fixed slots")
        updated = list(self.output)
        for port in ports:
            if updated[6 + port] is not None:
                raise OverflowError("source terminal output Port is occupied")
            updated[6 + port] = EnvelopePacket(
                arrival, self.position, port, source_id, None, cause_id=cause_id
            )
        return tuple(updated)

    def start_gate(
        self,
        tick: int,
        epoch: int,
        gate: EnvelopeGate,
        send_delay: int,
        link_ticks: int,
        compute_delay: int,
        cost: int,
        events: NodeEvents,
    ) -> None:
        """Freeze a local input and reserve its one neighboring output Port."""
        _nonnegative(epoch, "source gate epoch")
        _nonnegative(cost, "source gate cost")
        if self.pending_gate is not None or self.incoming_gate is not None:
            raise ValueError("a source Node already owns an unfinished gate")
        if bounded(link_ticks) < 1:
            raise ValueError("source Links require positive transit time")
        if type(gate) is not EnvelopeGate or len(self.output) != 12:
            raise ValueError("a source gate requires its fixed local output bank")
        if gate.port >= 0 and self.output[gate.port] is not None:
            raise OverflowError("source amplitude output Port is occupied")
        arrival = _future(tick, send_delay, link_ticks if gate.port >= 0 else 0)
        ready = _future(arrival, compute_delay)
        pending = PendingEnvelopeGate(
            epoch, ready, self.source_id, self.amplitude, self.generation, gate
        )
        events.require_room(1)
        cause, message = self._record("source-gate-started", tick, events, cost=cost)
        updated = list(self.output)
        if gate.port >= 0:
            updated[gate.port] = EnvelopePacket(
                arrival, self.position, gate.port, self.source_id, self.amplitude, epoch, cause
            )
        self.output = tuple(updated)
        self.pending_gate = pending
        self.cause_id = cause
        events.publish(message)

    def receive(
        self,
        packet: EnvelopePacket,
        tick: int,
        link_ticks: int,
        control_delay: int,
        events: NodeEvents,
        *,
        costs: OperationCosts,
    ) -> None:
        """Accept an actual arrival; terminal knowledge waits for a local commit."""
        if type(packet) is not EnvelopePacket or packet.arrival_tick != tick:
            raise ValueError("source packet must arrive at its scheduled tick")
        if bounded(link_ticks) < 1:
            raise ValueError("source Links require positive transit time")
        self._identity(packet.source_id)
        duplicate = False
        if packet.amplitude is None:
            duplicate = self.retired == packet.source_id or self.pending_stop is not None
            pending = PendingEnvelopeStop(
                _future(tick, control_delay), packet.source_id, packet.cause_id
            )
        else:
            gate = self.pending_gate
            if (
                gate is None
                or gate.epoch != packet.epoch
                or gate.gate.port != packet.port ^ 1
                or gate.ready_tick < tick
            ):
                raise ValueError("source amplitude arrival does not match its frozen local gate")
            if self.incoming_gate is not None:
                raise OverflowError("a source gate accepts one neighboring amplitude")
        meter = CostMeter(costs)
        meter.charge("receive")
        meter.charge("read")
        events.require_room(1)
        kind = "source-amplitude-received"
        if packet.amplitude is None:
            kind = "source-terminal-ignored" if duplicate else "source-terminal-received"
        cause, message = self._record(
            kind,
            tick,
            events,
            causes=() if packet.cause_id is None else (packet.cause_id,),
            cost=meter.total,
        )
        if duplicate:
            events.publish(message)
            return
        if packet.amplitude is None:
            self.pending_stop = PendingEnvelopeStop(pending.ready_tick, pending.source_id, cause)
        else:
            self.incoming_gate = packet
        self.cause_id = cause
        events.publish(message)

    def complete(
        self,
        tick: int,
        local_output: EnvelopePlanner,
        matrices: tuple[EnvelopeMatrix, ...],
        costs: OperationCosts,
        neighbor_ports: tuple[int, ...],
        send_delay: int,
        link_ticks: int,
        events: NodeEvents,
    ) -> bool:
        """Commit only frozen local and delivered inputs, with terminal priority."""
        stopped = self._complete_stop(tick, costs, neighbor_ports, send_delay, link_ticks, events)
        pending = self.pending_gate
        if pending is None or pending.ready_tick > tick:
            return stopped
        if self.retired or pending.generation != self.generation:
            self.pending_gate = None
            self.incoming_gate = None
            return True
        if pending.gate.port >= 0 and self.incoming_gate is None:
            raise ValueError("source gate reached commit without its neighbor packet")
        source_id = pending.source_id
        inputs: tuple[EnvelopeAmplitude, ...] = (pending.amplitude,)
        if self.incoming_gate is not None:
            incoming = self.incoming_gate
            assert incoming.amplitude is not None
            self._identity(incoming.source_id)
            if source_id and incoming.source_id not in (0, source_id):
                raise ValueError("source gate cannot combine different origins")
            source_id = source_id or incoming.source_id
            inputs = (
                (pending.amplitude, incoming.amplitude)
                if pending.gate.row == 0
                else (incoming.amplitude, pending.amplitude)
            )
        if pending.gate.matrix_index >= len(matrices):
            raise ValueError("source gate refers to an unavailable immutable matrix")
        meter = CostMeter(costs)
        value = local_output(matrices[pending.gate.matrix_index], inputs, pending.gate.row, meter)
        if type(value) is not EnvelopeAmplitude:
            raise TypeError("source planner must return an immutable local amplitude")
        if source_id == 0 and (value.real or value.imag):
            raise ValueError("vacuum source gate cannot create a source envelope")
        meter.charge("update")
        meter.charge("commit")
        events.require_room(1)
        cause, message = self._record("source-gate-committed", tick, events, cost=meter.total)
        self.source_id, self.amplitude = source_id, value
        self.pending_gate = None
        self.incoming_gate = None
        self.cause_id = cause
        events.publish(message)
        return True

    def _complete_stop(
        self,
        tick: int,
        costs: OperationCosts,
        neighbor_ports: tuple[int, ...],
        send_delay: int,
        link_ticks: int,
        events: NodeEvents,
    ) -> bool:
        pending = self.pending_stop
        if pending is None or pending.ready_tick > tick:
            return False
        self._identity(pending.source_id)
        generation = bounded(checked_work(self.generation + 1))
        updated = self._terminal_outputs(
            pending.source_id, tick, neighbor_ports, send_delay, link_ticks, pending.cause_id
        )
        meter = CostMeter(costs)
        meter.charge("update", 3)
        meter.charge("send", len(neighbor_ports))
        meter.charge("commit")
        events.require_room(1)
        cause, message = self._record("source-terminal-committed", tick, events, cost=meter.total)
        updated = tuple(
            replace(packet, cause_id=cause)
            if packet is not None and slot - 6 in neighbor_ports
            else packet
            for slot, packet in enumerate(updated)
        )
        self.source_id = self.retired = pending.source_id
        self.amplitude = EnvelopeAmplitude()
        self.generation, self.output, self.cause_id = generation, updated, cause
        self.pending_stop = None
        events.publish(message)
        return True

    def activate(self, origin_id: int, tick: int, eventcause: int | None) -> None:
        """Activate only the local source at an already committed contact."""
        self.check_activation(tick)
        _nonnegative(tick, "source activation tick")
        if bounded(origin_id) < 1 or self.source_id or self.retired or self.pending_stop is not None:
            raise ValueError("source envelope activation requires a fresh positive origin")
        if eventcause is not None:
            _nonnegative(eventcause, "source activation cause")
        generation = bounded(checked_work(self.generation + 1))
        self.source_id, self.amplitude = origin_id, EnvelopeAmplitude(1)
        self.generation, self.cause_id = generation, eventcause

    def check_activation(self, tick: int) -> None:
        """Preflight the local transition before the quantum owner commits."""
        _nonnegative(tick, "source activation tick")
        if self.source_id or self.retired or self.pending_stop is not None:
            raise ValueError("source envelope activation requires a fresh origin")
        bounded(checked_work(self.generation + 1))

    def check_capture(
        self,
        originid: int,
        tick: int,
        neighbor_ports: tuple[int, ...],
        control_delay: int,
        link_ticks: int,
    ) -> None:
        self._identity(originid)
        if bounded(originid) < 1 or self.retired:
            raise ValueError("local source capture requires an unresolved positive origin")
        bounded(checked_work(self.generation + 1))
        self._terminal_outputs(originid, tick, neighbor_ports, control_delay, link_ticks, None)

    def check_null(self, tick: int) -> None:
        _nonnegative(tick, "source null tick")
        bounded(checked_work(self.generation + 1))

    def capture(
        self,
        originid: int,
        tick: int,
        eventcause: int | None,
        neighbor_ports: tuple[int, ...],
        control_delay: int,
        link_ticks: int,
        events: NodeEvents,
    ) -> None:
        """End this local source and send terminal knowledge through its Ports."""
        self.check_capture(originid, tick, neighbor_ports, control_delay, link_ticks)
        generation = bounded(checked_work(self.generation + 1))
        updated = self._terminal_outputs(
            originid, tick, neighbor_ports, control_delay, link_ticks, eventcause
        )
        events.require_room(1)
        cause, message = self._record(
            "source-localized", tick, events, causes=() if eventcause is None else (eventcause,)
        )
        self.source_id = self.retired = originid
        self.amplitude = EnvelopeAmplitude()
        self.generation, self.output, self.cause_id = generation, updated, cause
        self.pending_stop = None
        events.publish(message)

    def null(self, tick: int, cause: int | None) -> None:
        """A local null result removes only this amplitude; no remote normalization."""
        self.check_null(tick)
        if cause is not None:
            _nonnegative(cause, "source null cause")
        generation = bounded(checked_work(self.generation + 1))
        self.amplitude = EnvelopeAmplitude()
        self.generation, self.cause_id = generation, cause
        if self.pending_gate is not None:
            # Both gate inputs were frozen before this measurement. Retain that
            # complete snapshot: rewriting only one endpoint would break its
            # unitary normalization. This delayed source gate may repopulate
            # the Node; it is not the conditioned quantum probability.
            self.pending_gate = replace(self.pending_gate, generation=generation)

    def clear_output(self, slot: int, packet: EnvelopePacket) -> None:
        """Release one sender-owned packet only after the receiver accepted it."""
        if type(slot) is not int or not 0 <= slot < 12 or self.output[slot] is not packet:
            raise ValueError("source output acknowledgement does not match the retained packet")
        updated = list(self.output)
        updated[slot] = None
        self.output = tuple(updated)
