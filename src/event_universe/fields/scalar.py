"""Integer scalar-field primitives. No particle, occupancy, world or Config knowledge."""

from dataclasses import dataclass
from typing import NamedTuple, Protocol

from event_universe.core.state import Neighbors, Vector, checked, checked_work, signed_divrem


class ScalarSample(NamedTuple):
    value: int = 0
    remainder: int = 0


def validate_sample(sample: ScalarSample, denominator: int) -> None:
    checked(sample.value)
    checked(sample.remainder)
    checked(denominator)
    if denominator <= 0 or abs(sample.remainder) >= denominator:
        raise ValueError("field law returned an invalid remainder or denominator")


class ScalarFieldRule(Protocol):
    """A local scalar law; source meaning and denominator are chosen by the caller.

    Return a bounded value and a remainder with absolute value below denominator.
    """

    def advance(
        self, sample: ScalarSample, neighbors: Neighbors, *, source: int, denominator: int
    ) -> ScalarSample: ...


@dataclass(frozen=True, slots=True)
class ScalarField:
    """Weighted six-neighbor stencil with optional local retention and exact residue.

    Weights are immutable policy, not per-node state. Signed values are supported;
    a nonnegative-field policy belongs to the consuming model.
    """

    neighbor_weights: Neighbors
    self_weight: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.neighbor_weights, tuple) or len(self.neighbor_weights) != 6:
            raise ValueError("exactly six immutable neighbor weights are required")
        for weight in self.neighbor_weights:
            checked(weight)
        checked(self.self_weight)

    def advance(
        self, sample: ScalarSample, neighbors: Neighbors, *, source: int, denominator: int
    ) -> ScalarSample:
        validate_sample(sample, denominator)
        if len(neighbors) != 6:
            raise ValueError("exactly six neighbor values are required")
        raw = checked_work(source)
        raw = checked_work(raw + sample.remainder)
        raw = checked_work(raw + self.self_weight * sample.value)
        for weight, value in zip(self.neighbor_weights, neighbors, strict=True):
            checked(value)
            raw = checked_work(raw + checked_work(weight * value))
        value, remainder = signed_divrem(raw, denominator)
        return ScalarSample(checked(value), checked(remainder))


def gradient(neighbors: Neighbors) -> Vector:
    """Unscaled integer central difference on the three coordinate axes."""
    if len(neighbors) != 6:
        raise ValueError("exactly six neighbor values are required")
    for value in neighbors:
        checked(value)
    return (
        checked_work(neighbors[0] - neighbors[1]),
        checked_work(neighbors[2] - neighbors[3]),
        checked_work(neighbors[4] - neighbors[5]),
    )
