"""Admission boundaries for canonical Detector ownership and historical research."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .spatial_state import SpatialFieldDefinition

DETECTOR_ONLY = "detector-only-v1"
HISTORICAL_AUTONOMOUS = "historical-autonomous-v1"


def validate_sampling_profile(profile: str) -> None:
    if profile not in (DETECTOR_ONLY, HISTORICAL_AUTONOMOUS):
        raise ValueError("sampling_profile must be detector-only-v1 or historical-autonomous-v1")


def require_historical_sampling(profile: str, mechanism: str) -> None:
    """Reject an unbound sampler instead of pretending a local contact is a Detector."""
    validate_sampling_profile(profile)
    if profile != HISTORICAL_AUTONOMOUS:
        raise ValueError(
            f"{mechanism} requires an actual external Detector; this sampling composition "
            "is unsupported under detector-only-v1. historical-autonomous-v1 retains "
            "the separate research candidate and does not satisfy Detector-only ownership"
        )


def validate_spatial_sampling(profile: str, definitions: tuple[SpatialFieldDefinition, ...]) -> None:
    validate_sampling_profile(profile)
    if any(definition.capture == "lottery" or definition.bonded for definition in definitions):
        require_historical_sampling(profile, "ordinary ray lottery or bond sampling")
