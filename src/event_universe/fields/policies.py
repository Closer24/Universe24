"""Reusable scalar source, range and activity policies, selected by a model."""

from collections.abc import Callable

from event_universe.core.state import checked, checked_work
from event_universe.fields.scalar import ScalarSample

ScalarActivity = Callable[[ScalarSample, ScalarSample, int], bool]


def uniform_source(count: int, strength: int) -> int:
    """Map a nonnegative local count to a bounded source; retain no emission history."""
    checked(count)
    checked(strength)
    if count < 0 or strength < 0:
        raise ValueError("source count and strength must be non-negative")
    return checked_work(count * strength)


def nonnegative_sample(sample: ScalarSample) -> ScalarSample:
    """Clear a negative scalar value and its residue; preserve other samples exactly."""
    return ScalarSample() if sample.value < 0 else sample


def value_changed_or_source(previous: ScalarSample, current: ScalarSample, sources: int) -> bool:
    """Value-based activity used by the existing v10 model."""
    return previous.value != current.value or sources != 0


def sample_changed_or_source(previous: ScalarSample, current: ScalarSample, sources: int) -> bool:
    """Include remainder-only evolution when deciding whether a scalar law is quiescent."""
    return previous != current or sources != 0
