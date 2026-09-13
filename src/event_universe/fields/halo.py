"""Fixed local scalar-halo transformations."""

from event_universe.fields.scalar import ScalarSample


def cancel_scalar_sample(sample: ScalarSample) -> ScalarSample:
    """Return the quiescent scalar sample for one locally selected node."""
    return ScalarSample()
