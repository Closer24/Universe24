"""Private one-input, one-output units for the identity transport experiment.

This is a separate, deliberately minimal execution profile. It does not invoke
the existing whole-Node interaction planner or define universal physical routing.
Addresses belong to the host. The pure transition receives no address, clock,
neighbor reference, shared snapshot or callback.
"""

from dataclasses import dataclass, field
from typing import Literal

from .disturbance_state import MAX_COMPONENTS, Address3, bounded, decode

PRIVATE_PORT_PAIRS: tuple[tuple[int, int], ...] = tuple(
    (source, target) for source in range(6) for target in range(6) if source // 2 != target // 2
)
CUBIC_PORT_PAIRS: tuple[tuple[int, int], ...] = tuple(
    (source, target) for source in range(6) for target in range(6)
)


def _pair(source: int, target: int) -> None:
    if any(type(port) is not int or not 0 <= port < 6 for port in (source, target)):
        raise ValueError("a private Register requires two of the six external Ports")


def validate_private_pairs(pairs: tuple[tuple[int, int], ...]) -> None:
    """Validate a fixed immutable set of distinct configured Register endpoints."""
    if type(pairs) is not tuple or not 1 <= len(pairs) <= 36:
        raise ValueError("private Port pairs require a bounded immutable tuple")
    for pair in pairs:
        if type(pair) is not tuple or len(pair) != 2:
            raise ValueError("a private Port pair requires two Port indices")
        _pair(*pair)
    if len(set(pairs)) != len(pairs):
        raise ValueError("configured private Port pairs must be distinct")


def _codes(codes: tuple[int, ...], *, empty: bool) -> None:
    if type(codes) is not tuple or not (0 if empty else 1) <= len(codes) <= MAX_COMPONENTS:
        raise ValueError("private components require a fixed bounded integer tuple")
    for code in codes:
        decode(code)


@dataclass(frozen=True, slots=True, order=True)
class PrivateKey:
    """Host identity only; this key is never a physical transition argument."""

    node: Address3
    from_port: int
    to_port: int

    def __post_init__(self) -> None:
        if type(self.node) is not tuple or len(self.node) != 3:
            raise ValueError("a private Register address requires three Node coordinates")
        for value in self.node:
            if bounded(value) < 0:
                raise ValueError("Node coordinates must be nonnegative")
        _pair(self.from_port, self.to_port)


@dataclass(frozen=True, slots=True)
class RegisterDatum:
    """One actually received datum on one channel, with no embedded routing law.

    Components use the existing positive integer coding. Code 1 represents numerical
    zero and remains a present datum; only None means no received input. Components
    are opaque to identity transport and are not several independent input channels.
    """

    codes: tuple[int, ...]

    def __post_init__(self) -> None:
        _codes(self.codes, empty=False)


@dataclass(frozen=True, slots=True)
class PrivateState:
    """Only this unit's retained components; identity transport preserves them.

    The transport fixture initializes empty private memory. Nonempty bounded memory
    is supported for isolation tests; it does not introduce an evolution or mass law.
    """

    codes: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        _codes(self.codes, empty=True)


@dataclass(frozen=True, slots=True)
class IdentityLaw:
    """The sole law supported by this explicit transport-only profile."""

    operation: Literal["identity"] = "identity"

    def __post_init__(self) -> None:
        if type(self.operation) is not str or self.operation != "identity":
            raise ValueError("the private transport profile supports only the identity law")


@dataclass(frozen=True, slots=True)
class PrivateResult:
    """One new private state and at most one output on the unit's single channel."""

    state: PrivateState
    output: RegisterDatum | None

    def __post_init__(self) -> None:
        if type(self.state) is not PrivateState:
            raise ValueError("a private result requires immutable own state")
        if self.output is not None and type(self.output) is not RegisterDatum:
            raise ValueError("a private Register supplies one output datum, not a batch")


def private_transition(
    state: PrivateState, received: RegisterDatum | None, law: IdentityLaw
) -> PrivateResult:
    """Apply the same pure identity rule to own state and one received input.

    The result is a proposal until its owner commits it. Returning the immutable
    input object does not create a second inventory owner. Admission, capacity and
    causal transfer belong to the external runtime, which moves that ownership once.
    """
    if type(state) is not PrivateState or type(law) is not IdentityLaw:
        raise ValueError("private transition requires immutable own state and an identity law")
    if received is not None and type(received) is not RegisterDatum:
        raise ValueError("a private Register accepts one received datum, not a batch")
    return PrivateResult(state, received)


@dataclass(slots=True)
class PrivateUnit:
    """One independent state owner; no peer or Node reference is retained."""

    state: PrivateState = field(default_factory=PrivateState)
    law: IdentityLaw = field(default_factory=IdentityLaw)

    def __post_init__(self) -> None:
        private_transition(self.state, None, self.law)

    def advance(self, received: RegisterDatum | None) -> RegisterDatum | None:
        result = private_transition(self.state, received, self.law)
        self.state = result.state
        return result.output


class PrivateNode:
    """A container of configured private units; it has no physical mixer."""

    __slots__ = ("pairs", "units")

    def __init__(
        self,
        law: IdentityLaw | None = None,
        *,
        pairs: tuple[tuple[int, int], ...] = PRIVATE_PORT_PAIRS,
    ) -> None:
        validate_private_pairs(pairs)
        self.pairs = pairs
        configured = IdentityLaw() if law is None else law
        self.units: tuple[PrivateUnit, ...] = tuple(PrivateUnit(law=configured) for _ in pairs)

    def unit(self, from_port: int, to_port: int) -> PrivateUnit:
        """Resolve a configured host endpoint without exposing it to the law."""
        _pair(from_port, to_port)
        if (from_port, to_port) not in self.pairs:
            raise ValueError("private Register is not in the configured Port pairs")
        return self.units[self.pairs.index((from_port, to_port))]
