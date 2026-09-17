"""Admission boundary for Detector-owned sampling: the only draw is at a marked Node."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .spatial_state import SpatialFieldDefinition

DETECTOR_ONLY = "detector-only-v1"


def validate_sampling_profile(profile: str) -> None:
    """Only the Detector-only contract exists; the historical autonomous profile was deleted."""
    if profile != DETECTOR_ONLY:
        raise ValueError(
            "sampling_profile must be detector-only-v1: the historical-autonomous-v1 research "
            "profile was deleted on 2026-09-17 and only a Node whose Detector bit is set may draw"
        )


def validate_spatial_sampling(profile: str, definitions: tuple[SpatialFieldDefinition, ...]) -> None:
    """Reject any ordinary lottery: no absorber, ticket or registry draws outside a Detector."""
    validate_sampling_profile(profile)
    if any(definition.capture == "lottery" for definition in definitions):
        raise ValueError(
            "the lottery capture was deleted on 2026-09-17: an ordinary absorber does not draw, "
            "only a Node whose Detector bit is set (detector-only-v1)"
        )
