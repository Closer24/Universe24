"""Immutable host scheduling handles and bounded Node-local readiness messages.

Handles and readiness messages are views, never additional physical inventory.
Actual records remain in NodeState or its existing fixed outgoing PortBank.
"""

from dataclasses import dataclass
from typing import Literal

from .disturbance_state import Address3, Packet, bounded

WorkKind = Literal["arrival", "compute", "commit"]


def _port(value: int) -> None:
    if type(value) is not int or not 0 <= value < 6:
        raise ValueError("Register port must be an integer from zero through five")


@dataclass(frozen=True, slots=True)
class PortEndpointKey:
    """Host-only endpoint identity; local rule inputs never contain this key."""

    node: Address3
    port: int

    def __post_init__(self) -> None:
        _port(self.port)
        if type(self.node) is not tuple or len(self.node) != 3:
            raise ValueError("Register key requires a three-component Node address")
        if any(type(value) is not int or bounded(value) < 0 for value in self.node):
            raise ValueError("Register key address must contain bounded nonnegative integers")


@dataclass(frozen=True, slots=True)
class ReadyBatch:
    """One ready external Port; packet views belong to Node-level admission.

    This aggregate host interface is not an individual internal Register input.
    """

    port: int
    kind: WorkKind
    packets: tuple[Packet, ...] = ()

    def __post_init__(self) -> None:
        _port(self.port)
        if self.kind not in ("arrival", "compute", "commit"):
            raise ValueError("unsupported Register work kind")
        if type(self.packets) is not tuple or len(self.packets) > 32:
            raise ValueError("Register arrival batch exceeds fixed record capacity")
        if self.kind != "arrival" and self.packets:
            raise ValueError("only arrival readiness may carry packet views")
        if any(type(packet) is not Packet for packet in self.packets):
            raise ValueError("Register arrivals require immutable Packets")
        if any(packet.port ^ 1 != self.port for packet in self.packets):
            raise ValueError("arrival packet uses a different receiving Register")


@dataclass(frozen=True, slots=True)
class OutgoingIntent:
    """Reference to a packet owned by this Node's fixed output bank."""

    slot: int
    port: int
    arrival_tick: int

    def __post_init__(self) -> None:
        _port(self.port)
        if type(self.slot) is not int or not 0 <= self.slot < 192:
            raise ValueError("outgoing slot exceeds the six-Port capacity bound")
        if type(self.arrival_tick) is not int or bounded(self.arrival_tick) < 0:
            raise ValueError("arrival tick must be a bounded nonnegative integer")


@dataclass(frozen=True, slots=True)
class WakeIntent:
    """Absolute admission time in the existing execution profile's clock."""

    port: int
    kind: Literal["compute", "commit"]
    due_tick: int

    def __post_init__(self) -> None:
        _port(self.port)
        if self.kind not in ("compute", "commit"):
            raise ValueError("wake kind must be compute or commit")
        if type(self.due_tick) is not int or bounded(self.due_tick) < 0:
            raise ValueError("wake time must be a bounded nonnegative integer")


@dataclass(frozen=True, slots=True)
class RegisterEffects:
    """Aggregate Node output handles and the replacement set of future wakes.

    The host replaces this Node's prior compute/commit wake set with ``wakes``.
    Outgoing packets stay in their PortBank until a later successful receipt.
    Existing Node event publication remains the canonical physical event trace.
    This is a Node coordination result, not a one-Register output interface.
    """

    outgoing: tuple[OutgoingIntent, ...] = ()
    wakes: tuple[WakeIntent, ...] = ()
    committed: bool = False

    def __post_init__(self) -> None:
        if type(self.outgoing) is not tuple or len(self.outgoing) > 192:
            raise ValueError("Register outgoing effects exceed fixed PortBank capacity")
        if any(type(intent) is not OutgoingIntent for intent in self.outgoing):
            raise ValueError("Register outgoing effects require OutgoingIntent handles")
        if len({intent.slot for intent in self.outgoing}) != len(self.outgoing):
            raise ValueError("an outgoing packet slot may appear only once")
        if type(self.wakes) is not tuple or len(self.wakes) > 12:
            raise ValueError("Register wakes exceed fixed endpoint capacity")
        if any(type(intent) is not WakeIntent for intent in self.wakes):
            raise ValueError("Register wake effects require WakeIntent values")
        if len({(intent.port, intent.kind) for intent in self.wakes}) != len(self.wakes):
            raise ValueError("a Register wake key may appear only once")
        if type(self.committed) is not bool:
            raise ValueError("Register commit report must be boolean")


@dataclass(frozen=True, slots=True)
class PortState:
    """One of six external Port views; this is not an internal Register."""

    port: int
    slots: tuple[int, ...] = ()
    locked_slots: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        _port(self.port)
        if type(self.slots) is not tuple or len(self.slots) > 32:
            raise ValueError("Register slot ownership must be a fixed bounded tuple")
        if any(type(slot) is not int or not 0 <= slot < 32 for slot in self.slots):
            raise ValueError("Register slot exceeds fixed Node capacity")
        if len(set(self.slots)) != len(self.slots):
            raise ValueError("Register slot ownership must be unique and bounded")
        if type(self.locked_slots) is not tuple or len(self.locked_slots) > 32:
            raise ValueError("Register locks must be a fixed bounded tuple")
        if any(type(slot) is not int or not 0 <= slot < 32 for slot in self.locked_slots):
            raise ValueError("Register lock exceeds fixed Node capacity")
        if len(set(self.locked_slots)) != len(self.locked_slots):
            raise ValueError("Register locks must be unique")
        if not set(self.locked_slots).issubset(self.slots):
            raise ValueError("Register locks must refer to its own slots")


INTERNAL_PORT_PAIRS: tuple[tuple[int, int], ...] = tuple(
    (source, target) for source in range(6) for target in range(6) if source // 2 != target // 2
)


def _internal_pair(source: int, target: int) -> None:
    _port(source)
    _port(target)
    if source // 2 == target // 2:
        raise ValueError("an internal Register must connect two orthogonal Ports")


@dataclass(frozen=True, slots=True)
class InternalRegisterKey:
    """Host identity for one of 24 directed internal computational units."""

    node: Address3
    from_port: int
    to_port: int

    def __post_init__(self) -> None:
        PortEndpointKey(self.node, self.from_port)
        _internal_pair(self.from_port, self.to_port)


@dataclass(frozen=True, slots=True)
class RegisterInput:
    """One input channel's reference to one vector-bearing NodeState slot.

    The referenced datum has one provenance. Combining distinct incoming channels
    is a separate Node transaction and cannot be hidden in this interface.
    """

    slot: int

    def __post_init__(self) -> None:
        if type(self.slot) is not int or not 0 <= self.slot < 32:
            raise ValueError("Register input requires one bounded NodeState slot")


@dataclass(frozen=True, slots=True)
class RegisterOutput:
    """One output channel's reference to one Node-local proposal slot.

    The proposal is not inventory until the separate atomic Node commit accepts it.
    """

    slot: int

    def __post_init__(self) -> None:
        if type(self.slot) is not int or not 0 <= self.slot < 32:
            raise ValueError("Register output requires one bounded proposal slot")


@dataclass(frozen=True, slots=True)
class InternalRegisterState:
    """One local unit with exactly one input and one output interface.

    The interface alone does not define routing through this graph. Straight and
    returning physical signals need a separately agreed mapping; no additional
    physical hop, direct same-axis edge or inventory copy is implied here.
    """

    from_port: int
    to_port: int
    input: RegisterInput | None = None
    output: RegisterOutput | None = None

    def __post_init__(self) -> None:
        _internal_pair(self.from_port, self.to_port)
        if self.input is not None and type(self.input) is not RegisterInput:
            raise ValueError("an internal Register accepts exactly one input channel")
        if self.output is not None and type(self.output) is not RegisterOutput:
            raise ValueError("an internal Register supplies exactly one output channel")
