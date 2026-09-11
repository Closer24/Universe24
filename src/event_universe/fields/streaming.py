"""Bounded outward field streaming through six nearest-neighbor links.

Eight fixed octant populations preserve the sign of outward propagation without
storing source identity or history. Every nonzero population is split across the
three cardinal directions belonging to its octant and moves exactly one link in
one tick. The split phase only assigns indivisible integer units; it does not
change total field amount.
"""

from dataclasses import dataclass
from typing import Protocol, cast

from event_universe.core.state import checked, checked_work
from event_universe.fields.faces import face_imbalance

Octants = tuple[int, int, int, int, int, int, int, int]
Outgoing = tuple[Octants, Octants, Octants, Octants, Octants, Octants]
ZERO_OCTANTS: Octants = (0, 0, 0, 0, 0, 0, 0, 0)
OCTANT_SIGNS: tuple[tuple[int, int, int], ...] = (
    (1, 1, 1),
    (1, 1, -1),
    (1, -1, 1),
    (1, -1, -1),
    (-1, 1, 1),
    (-1, 1, -1),
    (-1, -1, 1),
    (-1, -1, -1),
)


class OctantFieldRule(Protocol):
    """Replaceable pure law over a fixed eight-channel directional state.

    Inputs are one cell's old populations, bounded resident source count,
    immutable source strength and supplied tick phase. Return six fixed packets
    of eight nonnegative integers. The engine owns neighbor delivery and commits.
    Implementations must retain no private evolving state or source histories.
    Passing this interface alone does not establish a law's causal or self-force
    properties; those also depend on its routing and the engine's tick order.
    """

    def emit(
        self, populations: Octants, sources: int, source_per_octant: int, phase: int
    ) -> Outgoing: ...


def _direction(axis: int, sign: int) -> int:
    return checked(2 * axis + (0 if sign > 0 else 1))


def _split_three(value: int, phase: int) -> tuple[int, int, int]:
    """Conserve a nonnegative integer exactly while rotating indivisible units."""
    checked(value)
    checked(phase)
    if value < 0 or phase < 0:
        raise ValueError("stream amount and phase must be non-negative")
    quotient, remainder = divmod(value, 3)
    shares = [quotient, quotient, quotient]
    start = phase % 3
    for offset in range(remainder):
        shares[(start + offset) % 3] = checked(shares[(start + offset) % 3] + 1)
    return shares[0], shares[1], shares[2]


@dataclass(frozen=True, slots=True)
class CausalOctantStream:
    """Local stream law with no remote reads and no evolving private state."""

    def emit(self, populations: Octants, sources: int, source_per_octant: int, phase: int) -> Outgoing:
        if len(populations) != 8:
            raise ValueError("exactly eight octant populations are required")
        for value in (*populations, sources, source_per_octant, phase):
            checked(value)
        if any(value < 0 for value in populations):
            raise ValueError("stream populations must be non-negative before source emission")
        if sources < 0 or source_per_octant < 0 or phase < 0:
            raise ValueError("sources, stream strength and phase must be non-negative")
        source = checked_work(sources * source_per_octant)
        buckets = [[0] * 8 for _ in range(6)]
        for octant, old in enumerate(populations):
            amount = checked(checked_work(old + source))
            shares = _split_three(amount, phase)
            signs = OCTANT_SIGNS[octant]
            for axis, share in enumerate(shares):
                direction = _direction(axis, signs[axis])
                buckets[direction][octant] = checked(checked_work(buckets[direction][octant] + share))
        return cast(Outgoing, tuple(tuple(bucket) for bucket in buckets))


def flux_vector(flux: tuple[int, int, int, int, int, int]) -> tuple[int, int, int]:
    """Compatibility difference of six travel-oriented directional amounts.

    This delegates the arithmetic only; it does not reverse packet orientation.
    New source-facing response code calls face_imbalance on its delivered inbox.
    """
    return face_imbalance(flux)


def attractive_samples(flux: tuple[int, int, int, int, int, int]) -> tuple[int, int, int, int, int, int]:
    """Present incoming propagation as an attractive central-difference sample."""
    if len(flux) != 6:
        raise ValueError("exactly six directional flux values are required")
    for value in flux:
        checked(value)
    return flux[1], flux[0], flux[3], flux[2], flux[5], flux[4]
