"""Bounded local source-envelope transitions and causally delivered inputs."""

from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from .disturbance_state import Address3, CostMeter, OperationCosts, bounded
from .integer import checked_work
from .source_envelope_state import EnvelopeAmplitude, EnvelopeScale, NullRecord
from .state import reduced_ratio

if TYPE_CHECKING:
    from .node_services import NodeEvents

EnvelopeMatrix = tuple[tuple[tuple[int, int], ...], ...]
EnvelopePlanner = Callable[
    [EnvelopeMatrix, tuple[EnvelopeAmplitude, ...], int, CostMeter], EnvelopeAmplitude
]
NullFactor = Callable[[EnvelopeAmplitude, EnvelopeScale, CostMeter], tuple[int, int] | None]
WeightOf = Callable[[EnvelopeAmplitude, CostMeter], tuple[int, int]]
NullCorrection = Callable[
    [NullRecord, tuple[int, int], CostMeter], tuple[tuple[int, int], tuple[int, int]] | None
]
# Six amplitude, six terminal, six null-notice and six correction Port slots.
OUTPUT_SLOTS = 24
NOTICE_BANK = 6
CORRECTION_QUEUE = 6


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
    scale: tuple[int, int] | None = None
    notice_id: int = -1
    null_tick: int = -1
    null_origin: Address3 | None = None

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
        if self.scale is None:
            if self.notice_id != -1:
                raise ValueError("a notice identity requires a scale factor")
        else:
            if self.amplitude is not None or bounded(self.notice_id) < 0:
                raise ValueError("a null notice carries a scale factor and an event identity")
            if (
                type(self.scale) is not tuple
                or len(self.scale) != 2
                or bounded(self.scale[1]) < 1
                or bounded(self.scale[0]) < self.scale[1]
            ):
                raise ValueError("a null notice factor must be a rational of at least one")
        if self.null_origin is None:
            if self.null_tick != -1:
                raise ValueError("a null ordering key requires the deciding Node's position")
        else:
            if self.scale is None or bounded(self.null_tick) < 0:
                raise ValueError("a null ordering key belongs to a notice with a null tick")
            if type(self.null_origin) is not tuple or len(self.null_origin) != 3:
                raise ValueError("a null ordering key requires three coordinates")
            for coordinate in self.null_origin:
                _nonnegative(coordinate, "null ordering coordinate")

    @property
    def is_notice(self) -> bool:
        return self.scale is not None

    @property
    def order_key(self) -> tuple[int, Address3] | None:
        """The (tick, position) of the null this notice reports, if it carries one."""
        return None if self.null_origin is None else (self.null_tick, self.null_origin)


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


@dataclass(frozen=True, slots=True)
class PendingEnvelopeScale:
    """One delivered null notice waiting for this Node's local control delay."""

    ready_tick: int
    source_id: int
    numerator: int
    denominator: int
    notice_id: int
    port: int
    cause_id: int | None
    null_tick: int = -1
    null_origin: Address3 | None = None

    @property
    def order_key(self) -> tuple[int, Address3] | None:
        return None if self.null_origin is None else (self.null_tick, self.null_origin)


@dataclass(frozen=True, slots=True)
class PendingEnvelopeCorrection:
    """One computed correction of this Node's own null factor, waiting for free Ports."""

    numerator: int
    denominator: int
    notice_id: int
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
    output: tuple[EnvelopePacket | None, ...] = (None,) * OUTPUT_SLOTS
    cause_id: int | None = None
    scale: EnvelopeScale = EnvelopeScale()
    pending_scales: tuple[PendingEnvelopeScale | None, ...] = (None,) * 6
    applied_notices: tuple[int, ...] = (-1,) * NOTICE_BANK
    null_record: NullRecord | None = None
    pending_corrections: tuple[PendingEnvelopeCorrection, ...] = ()
    corrections: int = 0

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
        if type(self.output) is not tuple or len(self.output) != OUTPUT_SLOTS:
            raise ValueError("source output bank requires twenty-four fixed slots")
        if any(packet is not None and type(packet) is not EnvelopePacket for packet in self.output):
            raise TypeError("source output bank accepts only immutable packets")
        if self.cause_id is not None:
            _nonnegative(self.cause_id, "source Node cause")
        if type(self.scale) is not EnvelopeScale:
            raise TypeError("source Node requires an immutable weight scale")
        if type(self.pending_scales) is not tuple or len(self.pending_scales) != 6:
            raise ValueError("source Node holds one pending notice per Port")
        if type(self.applied_notices) is not tuple or len(self.applied_notices) != NOTICE_BANK:
            raise ValueError("source Node retains a fixed bank of applied notices")
        if self.null_record is not None and type(self.null_record) is not NullRecord:
            raise TypeError("source Node retains at most one immutable null record")
        if (
            type(self.pending_corrections) is not tuple
            or len(self.pending_corrections) > CORRECTION_QUEUE
        ):
            raise ValueError("source Node queues at most six pending corrections")
        _nonnegative(self.corrections, "source correction count")

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
        if len(self.output) != OUTPUT_SLOTS:
            raise ValueError("source output bank requires twenty-four fixed slots")
        updated = list(self.output)
        for port in ports:
            if updated[6 + port] is not None:
                raise OverflowError("source terminal output Port is occupied")
            updated[6 + port] = EnvelopePacket(
                arrival, self.position, port, source_id, None, cause_id=cause_id
            )
        return tuple(updated)

    def _notice_outputs(
        self,
        source_id: int,
        tick: int,
        ports: tuple[int, ...],
        send_delay: int,
        link_ticks: int,
        factor: tuple[int, int],
        notice_id: int,
        cause_id: int | None,
        *,
        base: int = 12,
        null_tick: int = -1,
        null_origin: Address3 | None = None,
    ) -> tuple[EnvelopePacket | None, ...]:
        _ports(ports)
        if bounded(link_ticks) < 1:
            raise ValueError("source Links require positive transit time")
        if base not in (12, 18):
            raise ValueError("source notices leave through the notice or correction bank")
        arrival = _future(tick, send_delay, link_ticks)
        updated = list(self.output)
        for port in ports:
            if updated[base + port] is not None:
                raise OverflowError("source notice output Port is occupied")
            updated[base + port] = EnvelopePacket(
                arrival,
                self.position,
                port,
                source_id,
                None,
                cause_id=cause_id,
                scale=factor,
                notice_id=notice_id,
                null_tick=null_tick,
                null_origin=null_origin,
            )
        return tuple(updated)

    def _known_notice(self, notice_id: int) -> bool:
        if notice_id in self.applied_notices:
            return True
        return any(p is not None and p.notice_id == notice_id for p in self.pending_scales)

    def _apply_factor(self, numerator: int, denominator: int, notice_id: int) -> None:
        old = self.scale
        top, bottom = reduced_ratio(
            checked_work(old.numerator * numerator), checked_work(old.denominator * denominator)
        )
        self.scale = EnvelopeScale(bounded(top), bounded(bottom))
        self.applied_notices = (*self.applied_notices[1:], notice_id)

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
        if type(gate) is not EnvelopeGate or len(self.output) != OUTPUT_SLOTS:
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
        if packet.scale is not None:
            duplicate = bool(self.retired) or self._known_notice(packet.notice_id)
            if not duplicate and self.pending_scales[packet.port ^ 1] is not None:
                raise OverflowError("a source Node holds one pending notice per Port")
        elif packet.amplitude is None:
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
        if packet.scale is not None:
            kind = "source-notice-ignored" if duplicate else "source-notice-received"
        elif packet.amplitude is None:
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
        if packet.scale is not None:
            # The notice entered through this Node's opposite Port; it is not
            # forwarded back through it.
            slots = list(self.pending_scales)
            slots[packet.port ^ 1] = PendingEnvelopeScale(
                _future(tick, control_delay),
                packet.source_id,
                packet.scale[0],
                packet.scale[1],
                packet.notice_id,
                packet.port ^ 1,
                cause,
                packet.null_tick,
                packet.null_origin,
            )
            self.pending_scales = tuple(slots)
        elif packet.amplitude is None:
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
        correction: NullCorrection | None = None,
    ) -> bool:
        """Commit only frozen local and delivered inputs, with terminal priority."""
        stopped = self._complete_stop(tick, costs, neighbor_ports, send_delay, link_ticks, events)
        stopped = (
            self._complete_scales(
                tick, costs, neighbor_ports, send_delay, link_ticks, events, correction
            )
            or stopped
        )
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

    def _complete_scales(
        self,
        tick: int,
        costs: OperationCosts,
        neighbor_ports: tuple[int, ...],
        send_delay: int,
        link_ticks: int,
        events: NodeEvents,
        correction: NullCorrection | None = None,
    ) -> bool:
        """Apply delivered null factors after the local control delay, then forward them.

        A delivered notice ordered before this Node's own null, by (tick, position),
        arrived after that null's factor was sent from a stale scale. With a
        correction law the Node then computes the exact quotient from its own null
        record, applies it, and queues it for its correction Ports under its own
        null's ordering key. Ordering is total, so of two crossing nulls exactly
        one corrects, and a chain of corrections telescopes to the conditional scale.
        """
        changed = self._flush_corrections(tick, costs, neighbor_ports, send_delay, link_ticks, events)
        for port, pending in enumerate(self.pending_scales):
            if pending is None or pending.ready_tick > tick:
                continue
            slots = list(self.pending_scales)
            slots[port] = None
            self.pending_scales = tuple(slots)
            changed = True
            if self.retired or self._known_notice(pending.notice_id):
                continue
            self._identity(pending.source_id)
            forward = tuple(p for p in neighbor_ports if p != pending.port)
            factor = (pending.numerator, pending.denominator)
            updated = self._notice_outputs(
                pending.source_id,
                tick,
                forward,
                send_delay,
                link_ticks,
                factor,
                pending.notice_id,
                pending.cause_id,
                null_tick=pending.null_tick,
                null_origin=pending.null_origin,
            )
            meter = CostMeter(costs)
            meter.charge("update", 3)
            meter.charge("send", len(forward))
            meter.charge("commit")
            events.require_room(1)
            cause, message = self._record(
                "source-scale-committed",
                tick,
                events,
                causes=() if pending.cause_id is None else (pending.cause_id,),
                cost=meter.total,
            )
            updated = tuple(
                replace(packet, cause_id=cause)
                if packet is not None and 12 <= slot < 18 and slot - 12 in forward
                else packet
                for slot, packet in enumerate(updated)
            )
            self._apply_factor(pending.numerator, pending.denominator, pending.notice_id)
            self.output, self.cause_id = updated, cause
            events.publish(message)
            self._correct_own_null(pending, factor, tick, costs, events, correction)
        changed = (
            self._flush_corrections(tick, costs, neighbor_ports, send_delay, link_ticks, events)
            or changed
        )
        return changed

    def _correct_own_null(
        self,
        pending: PendingEnvelopeScale,
        factor: tuple[int, int],
        tick: int,
        costs: OperationCosts,
        events: NodeEvents,
        correction: NullCorrection | None,
    ) -> None:
        record, key = self.null_record, pending.order_key
        if correction is None or record is None or key is None or self.retired:
            return
        if key >= (record.tick, self.position):
            return
        meter = CostMeter(costs)
        result = correction(record, factor, meter)
        if result is None:
            return
        (numerator, denominator), (scale_numerator, scale_denominator) = result
        self.null_record = replace(
            record, scale_numerator=scale_numerator, scale_denominator=scale_denominator
        )
        if numerator == denominator:
            return
        if len(self.pending_corrections) >= CORRECTION_QUEUE:
            raise OverflowError("source correction queue is full")
        meter.charge("update", 3)
        meter.charge("commit")
        events.require_room(1)
        corrected, message = self._record(
            "source-scale-corrected",
            tick,
            events,
            causes=() if pending.cause_id is None else (pending.cause_id,),
            cost=meter.total,
        )
        if corrected is None:
            raise ValueError("null corrections require a recording event owner")
        self._apply_factor(numerator, denominator, corrected)
        self.pending_corrections = (
            *self.pending_corrections,
            PendingEnvelopeCorrection(numerator, denominator, corrected, corrected),
        )
        self.corrections = bounded(checked_work(self.corrections + 1))
        self.cause_id = corrected
        events.publish(message)

    def _flush_corrections(
        self,
        tick: int,
        costs: OperationCosts,
        neighbor_ports: tuple[int, ...],
        send_delay: int,
        link_ticks: int,
        events: NodeEvents,
    ) -> bool:
        """Send the oldest queued correction through every Port once the bank is free."""
        if not self.pending_corrections:
            return False
        if self.retired or self.null_record is None:
            self.pending_corrections = ()
            return True
        if any(self.output[18 + port] is not None for port in neighbor_ports):
            return False
        first, *rest = self.pending_corrections
        meter = CostMeter(costs)
        meter.charge("send", len(neighbor_ports))
        events.require_room(1)
        cause, message = self._record(
            "source-correction-sent",
            tick,
            events,
            causes=() if first.cause_id is None else (first.cause_id,),
            cost=meter.total,
        )
        self.output = self._notice_outputs(
            self.source_id,
            tick,
            neighbor_ports,
            send_delay,
            link_ticks,
            (first.numerator, first.denominator),
            first.notice_id,
            cause,
            base=18,
            null_tick=self.null_record.tick,
            null_origin=self.position,
        )
        self.pending_corrections = tuple(rest)
        self.cause_id = cause
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
        self.null_record, self.pending_corrections = None, ()

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

    def null(
        self,
        tick: int,
        cause: int | None,
        *,
        null_factor: NullFactor | None = None,
        neighbor_ports: tuple[int, ...] = (),
        send_delay: int = 0,
        link_ticks: int = 1,
        costs: OperationCosts | None = None,
        events: NodeEvents | None = None,
        null_weight: WeightOf | None = None,
    ) -> None:
        """A local null result removes this amplitude; optional notices carry its factor.

        Without ``null_factor`` no remote normalization occurs. With it, the
        factor ``1 / (1 - p)`` computed from this Node's own scaled weight is
        applied locally and sent through the given Ports as a null notice. With
        ``null_weight`` the Node also keeps its own null record, the unscaled
        weight and the scale it assumed, so that a notice ordered before this
        null can later be answered with the exact correction.
        """
        self.check_null(tick)
        if cause is not None:
            _nonnegative(cause, "source null cause")
        factor: tuple[int, int] | None = None
        if null_factor is not None and self.source_id:
            if costs is None or events is None:
                raise ValueError("null notices require the local tariff and event owner")
            meter = CostMeter(costs)
            factor = null_factor(self.amplitude, self.scale, meter)
            if factor is not None and factor[0] == factor[1]:
                # A vacuum null carries no information; no notice is sent.
                factor = None
        record: NullRecord | None = None
        if factor is not None and null_weight is not None:
            weight = null_weight(self.amplitude, meter)
            record = NullRecord(tick, weight[0], weight[1], self.scale.numerator, self.scale.denominator)
        self.null_record, self.pending_corrections = record, ()
        generation = bounded(checked_work(self.generation + 1))
        self.amplitude = EnvelopeAmplitude()
        self.generation, self.cause_id = generation, cause
        if self.pending_gate is not None:
            # Both gate inputs were frozen before this measurement. Retain that
            # complete snapshot: rewriting only one endpoint would break its
            # unitary normalization. This delayed source gate may repopulate
            # the Node; it is not the conditioned quantum probability.
            self.pending_gate = replace(self.pending_gate, generation=generation)
        if factor is None or events is None or costs is None:
            return
        meter.charge("update", 3)
        meter.charge("send", len(neighbor_ports))
        meter.charge("commit")
        events.require_room(1)
        notice, message = self._record(
            "source-null-notice",
            tick,
            events,
            causes=() if cause is None else (cause,),
            cost=meter.total,
        )
        if notice is None:
            raise ValueError("null notices require a recording event owner")
        self.output = self._notice_outputs(
            self.source_id,
            tick,
            neighbor_ports,
            send_delay,
            link_ticks,
            factor,
            notice,
            notice,
            null_tick=tick if record is not None else -1,
            null_origin=self.position if record is not None else None,
        )
        self._apply_factor(factor[0], factor[1], notice)
        self.cause_id = notice
        events.publish(message)

    def clear_output(self, slot: int, packet: EnvelopePacket) -> None:
        """Release one sender-owned packet only after the receiver accepted it."""
        if type(slot) is not int or not 0 <= slot < OUTPUT_SLOTS or self.output[slot] is not packet:
            raise ValueError("source output acknowledgement does not match the retained packet")
        updated = list(self.output)
        updated[slot] = None
        self.output = tuple(updated)
