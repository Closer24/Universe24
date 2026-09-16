"""Explicit causal channels for the private Register transport experiment."""

from dataclasses import dataclass

from .disturbance_state import Address3, bounded
from .private_register import (
    CUBIC_PORT_PAIRS,
    PRIVATE_PORT_PAIRS,
    PrivateKey,
    RegisterDatum,
    validate_private_pairs,
)
from .state import DIRECTIONS


@dataclass(frozen=True)
class RouteTemplate:
    """One repeated directed channel, supplied by initialization data."""

    source: tuple[int, int]
    offset: Address3
    target: tuple[int, int]
    transit_ticks: int = 1

    def __post_init__(self) -> None:
        for pair in (self.source, self.target):
            validate_private_pairs((pair,))
        if (
            type(self.offset) is not tuple
            or len(self.offset) != 3
            or any(type(value) is not int for value in self.offset)
            or sum(abs(value) for value in self.offset) != 1
        ):
            raise ValueError("a channel must span exactly one cardinal lattice unit")
        if type(self.transit_ticks) is not int or self.transit_ticks != 1:
            raise ValueError("this transport profile requires one model tick per Link")


@dataclass(frozen=True)
class Channel:
    target: PrivateKey
    transit_ticks: int
    offset: Address3


class PeriodicWiring:
    """Expand supplied templates outside every private physical evaluator."""

    def __init__(
        self,
        shape: Address3,
        templates: tuple[RouteTemplate, ...],
        *,
        pairs: tuple[tuple[int, int], ...] = PRIVATE_PORT_PAIRS,
    ) -> None:
        validate_private_pairs(pairs)
        if (
            type(shape) is not tuple
            or len(shape) != 3
            or any(type(size) is not int or not 1 <= size <= 32 for size in shape)
        ):
            raise ValueError("periodic shape requires three integer extents from 1 to 32")
        if type(templates) is not tuple or any(type(item) is not RouteTemplate for item in templates):
            raise ValueError("wiring requires immutable explicit channel templates")
        if len(templates) != len(pairs) or {item.source for item in templates} != set(pairs):
            raise ValueError("wiring requires exactly one channel for each configured Register")
        if any(item.target not in pairs for item in templates):
            raise ValueError("a channel target is not in the configured Port pairs")
        if frozenset(pairs) == frozenset(CUBIC_PORT_PAIRS):
            for item in templates:
                if item.offset != DIRECTIONS[item.source[1]] or item.target[0] != item.source[1] ^ 1:
                    raise ValueError("cubic channels must connect matching external Ports")
        self.pairs = pairs
        self.shape = shape
        self.nodes: tuple[Address3, ...] = tuple(
            (x, y, z) for x in range(shape[0]) for y in range(shape[1]) for z in range(shape[2])
        )
        self.channels: dict[PrivateKey, Channel] = {}
        for node in self.nodes:
            for item in templates:
                target_node = tuple((node[axis] + item.offset[axis]) % shape[axis] for axis in range(3))
                target_address: Address3 = (target_node[0], target_node[1], target_node[2])
                source = PrivateKey(node, *item.source)
                self.channels[source] = Channel(
                    PrivateKey(target_address, *item.target), item.transit_ticks, item.offset
                )
        if {channel.target for channel in self.channels.values()} != set(self.channels):
            raise ValueError("this transport profile requires bijective single-input wiring")


@dataclass(frozen=True)
class ChannelPacket:
    """The one owned datum in a source Register's output channel."""

    target: PrivateKey
    datum: RegisterDatum
    due_tick: int


class CausalTransport:
    """Fixed-capacity channel owners; the due index stores source handles only."""

    def __init__(
        self, wiring: PeriodicWiring, seeds: tuple[tuple[PrivateKey, RegisterDatum], ...]
    ) -> None:
        self.wiring = wiring
        self.inputs: dict[PrivateKey, RegisterDatum] = {}
        self.channels: dict[PrivateKey, ChannelPacket] = {}
        self._due: dict[int, set[PrivateKey]] = {}
        self.peak_channels = 0
        for key, datum in seeds:
            self.admit(key, datum)

    def admit(self, key: PrivateKey, datum: RegisterDatum) -> None:
        """Admit one real external input, rejecting capacity before mutation."""
        if key not in self.wiring.channels:
            raise ValueError("input Register is outside the configured world")
        if type(datum) is not RegisterDatum:
            raise ValueError("input requires one bounded immutable datum")
        if key in self.inputs:
            raise ValueError("a Register input has fixed capacity one")
        self.inputs[key] = datum

    def pending_inputs(self, tick: int) -> frozenset[PrivateKey]:
        """Preflight the full due cohort without consuming any actual owner."""
        return frozenset(self.preview_inputs(tick))

    def preview_inputs(self, tick: int) -> dict[PrivateKey, RegisterDatum]:
        """Read validated due input objects without transferring their ownership."""
        if bounded(tick) < 0:
            raise ValueError("transport tick must be nonnegative")
        bounded(tick + 1)
        due_sources = self._due.get(tick, set())
        targets = dict(self.inputs)
        for source in due_sources:
            packet = self.channels[source]
            if packet.due_tick != tick:
                raise ValueError("channel deadline and owned packet disagree")
            if packet.target in targets:
                raise ValueError("a Register input has fixed capacity one")
            targets[packet.target] = packet.datum
        for target in targets:
            if target in self.channels and target not in due_sources:
                raise ValueError("a Register output channel has fixed capacity one")
        return targets

    def receive(self, tick: int) -> tuple[tuple[PrivateKey, ChannelPacket], ...]:
        """Transfer ownership only after pending_inputs has validated the cohort."""
        self.pending_inputs(tick)
        receipts = tuple((source, self.channels[source]) for source in sorted(self._due.get(tick, ())))
        for source, packet in receipts:
            self.inputs[packet.target] = packet.datum
            del self.channels[source]
        self._due.pop(tick, None)
        return receipts

    def emit(self, source: PrivateKey, datum: RegisterDatum, tick: int) -> ChannelPacket:
        """Move one actual input into its single causal output channel."""
        if source in self.channels:
            raise ValueError("a Register output channel has fixed capacity one")
        if type(datum) is not RegisterDatum or self.inputs.get(source) is not datum:
            raise ValueError("identity transport requires the actual received datum owner")
        channel = self.wiring.channels[source]
        arrival = bounded(tick + channel.transit_ticks)
        packet = ChannelPacket(channel.target, datum, arrival)
        self.channels[source] = packet
        del self.inputs[source]
        self._due.setdefault(arrival, set()).add(source)
        self.peak_channels = max(self.peak_channels, len(self.channels))
        return packet

    def retain(self, source: PrivateKey, datum: RegisterDatum) -> None:
        """Consume an actual input after its sole owner becomes private state."""
        if type(datum) is not RegisterDatum or self.inputs.get(source) is not datum:
            raise ValueError("retention requires the actual received datum owner")
        del self.inputs[source]

    def queue_report(self) -> dict[str, int]:
        return {
            "arrival_handles": sum(len(keys) for keys in self._due.values()),
            "arrival_epochs": len(self._due),
            "owned_channels": len(self.channels),
            "peak_channels": self.peak_channels,
        }
