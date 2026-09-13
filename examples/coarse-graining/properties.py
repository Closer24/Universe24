"""Bounded research readouts, never permission to replace physical records.

``sum`` and ``vector_sum`` add declared decoded properties. ``keep_equal``,
``phase_bins`` and ``interaction_state`` retain exact distinctions by partitioning;
``nonmergeable`` keeps every contributor separate. Law, channel, travel direction,
remaining delay and supplied state keys always partition bins. In particular,
opposite ports and different release times cannot cancel or release early.

A state key preserves only distinctions supplied by the caller. It does not prove
that those distinctions suffice for a selected law's future. Such a proof belongs
to a restricted closure experiment, not this readout or a property's sum metadata.
"""

from dataclasses import dataclass
from typing import Literal

from event_universe.core.disturbance_state import MAX_FIELDS, MAX_SLOTS, bounded
from event_universe.core.integer import checked_work

MAX_BLOCK_NODES = 64
MAX_CONTRIBUTIONS = MAX_BLOCK_NODES * MAX_SLOTS
MAX_IDENTITY_COMPONENTS = 4
MAX_STATE_COMPONENTS = 128
MAX_LABEL_LENGTH = 128
Aggregation = Literal[
    "sum", "vector_sum", "keep_equal", "phase_bins", "interaction_state", "nonmergeable"
]
Identity = tuple[int, ...]
PropertyValues = tuple[tuple[int, ...], ...]
_MODES = frozenset(
    ("sum", "vector_sum", "keep_equal", "phase_bins", "interaction_state", "nonmergeable")
)
_ADDITIVE = frozenset(("sum", "vector_sum"))


def _label(value: str, name: str) -> None:
    if type(value) is not str or not value or len(value) > MAX_LABEL_LENGTH:
        raise ValueError(f"{name} requires a nonempty bounded string")


def _integers(values: tuple[int, ...], limit: int, name: str, *, nonnegative: bool) -> None:
    if type(values) is not tuple or len(values) > limit:
        raise ValueError(f"{name} requires a bounded immutable tuple")
    for value in values:
        checked_work(value)
        if nonnegative and value < 0:
            raise ValueError(f"{name} requires nonnegative integers")


@dataclass(frozen=True, slots=True)
class PropertySpec:
    """One explicit aggregation choice; field names have no built-in meaning."""

    name: str
    aggregation: Aggregation
    components: int = 1

    def __post_init__(self) -> None:
        _label(self.name, "property name")
        if type(self.aggregation) is not str or self.aggregation not in _MODES:
            raise ValueError("unknown aggregation mode")
        if type(self.components) is not int or self.components not in (1, 3):
            raise ValueError("properties require one or three components")
        if self.aggregation in ("sum", "phase_bins") and self.components != 1:
            raise ValueError("sum and phase_bins require a scalar property")
        if self.aggregation == "vector_sum" and self.components != 3:
            raise ValueError("vector_sum requires a three-component property")


@dataclass(frozen=True, slots=True)
class Contribution:
    """One bounded local owner readout with explicitly supplied compatibility.

    ``law`` must identify the actual selected law and relevant parameters, not a
    cosmetic type name. ``channel`` identifies a declared field/channel index.
    ``direction`` is a travel port in [+X, -X, +Y, -Y, +Z, -Z] order. Identity is
    unique within a block; it is bookkeeping, never a selector for a physical law.
    Values are decoded single-record components, bounded by the existing schema.
    """

    identity: Identity
    law: str
    channel: int
    direction: int
    remaining_delay: int
    values: PropertyValues
    state_key: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        _integers(self.identity, MAX_IDENTITY_COMPONENTS, "identity", nonnegative=True)
        if not self.identity:
            raise ValueError("identity must not be empty")
        _label(self.law, "law")
        for name, value in (("channel", self.channel), ("remaining delay", self.remaining_delay)):
            checked_work(value)
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.direction) is not int or not 0 <= self.direction < 6:
            raise ValueError("direction must identify one of six travel ports")
        _integers(self.state_key, MAX_STATE_COMPONENTS, "state key", nonnegative=False)
        if type(self.values) is not tuple or not 1 <= len(self.values) <= MAX_FIELDS:
            raise ValueError("values require one to sixteen immutable properties")
        for payload in self.values:
            if type(payload) is not tuple or len(payload) not in (1, 3):
                raise ValueError("property values require one or three immutable components")
            for value in payload:
                bounded(value)


@dataclass(frozen=True, slots=True)
class AggregateBin:
    """One immutable compatible readout; sums use bounded working registers."""

    law: str
    channel: int
    direction: int
    remaining_delay: int
    values: PropertyValues
    state_key: tuple[int, ...]
    member_ids: tuple[Identity, ...]

    @property
    def count(self) -> int:
        return len(self.member_ids)


@dataclass(slots=True)
class _Accumulator:
    first: Contribution
    values: list[tuple[int, ...]]
    member_ids: list[Identity]


def aggregate_properties(
    schema: tuple[PropertySpec, ...],
    contributions: tuple[Contribution, ...],
    *,
    capacity: int,
) -> tuple[AggregateBin, ...]:
    """Validate the whole bounded input, then bin it in first-occurrence order.

    Capacity is an explicit local block bound, at most 64 Nodes times 32 slots.
    Inputs must already be tuples: this API never consumes an unbounded iterator.
    No records are mutated, discarded, or returned as replacement engine state.
    """
    if type(capacity) is not int or not 1 <= capacity <= MAX_CONTRIBUTIONS:
        raise ValueError("capacity must be between one and 2048 contributors")
    if type(schema) is not tuple or not 1 <= len(schema) <= MAX_FIELDS:
        raise ValueError("schema requires one to sixteen immutable property specs")
    if any(type(spec) is not PropertySpec for spec in schema):
        raise TypeError("schema entries must be PropertySpec values")
    if len({spec.name for spec in schema}) != len(schema):
        raise ValueError("property names must be unique")
    if type(contributions) is not tuple or len(contributions) > capacity:
        raise ValueError("contributions require an immutable tuple within block capacity")
    identities: set[Identity] = set()
    for item in contributions:
        if type(item) is not Contribution:
            raise TypeError("contributions must be Contribution values")
        if len(item.values) != len(schema) or any(
            len(payload) != spec.components for spec, payload in zip(schema, item.values, strict=True)
        ):
            raise ValueError("contribution properties do not match the complete schema")
        if item.identity in identities:
            raise ValueError("duplicate contribution identity")
        identities.add(item.identity)

    separate = any(spec.aggregation == "nonmergeable" for spec in schema)
    bins: dict[tuple[object, ...], _Accumulator] = {}
    for item in contributions:
        retained = tuple(
            payload
            for spec, payload in zip(schema, item.values, strict=True)
            if spec.aggregation not in _ADDITIVE
        )
        key = (
            item.law,
            item.channel,
            item.direction,
            item.remaining_delay,
            item.state_key,
            retained,
            item.identity if separate else (),
        )
        current = bins.get(key)
        if current is None:
            bins[key] = _Accumulator(item, list(item.values), [item.identity])
            continue
        for index, spec in enumerate(schema):
            if spec.aggregation in _ADDITIVE:
                current.values[index] = tuple(
                    checked_work(a + b)
                    for a, b in zip(current.values[index], item.values[index], strict=True)
                )
        current.member_ids.append(item.identity)
    return tuple(
        AggregateBin(
            item.first.law,
            item.first.channel,
            item.first.direction,
            item.first.remaining_delay,
            tuple(item.values),
            item.first.state_key,
            tuple(item.member_ids),
        )
        for item in bins.values()
    )
