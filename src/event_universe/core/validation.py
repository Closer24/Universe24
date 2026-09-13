"""Passive validation evaluates bounded expressions without pricing physical work."""

from .disturbance_state import CostMeter


class ValidationMeter(CostMeter):
    """Keep validation separate from the model's local computation clock."""

    def charge(self, operation: str, count: int = 1) -> None:
        pass
