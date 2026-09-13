"""Fixed integer records for locally retained source envelopes."""

from dataclasses import dataclass

from .disturbance_state import bounded


@dataclass(frozen=True, slots=True)
class EnvelopeAmplitude:
    """A complex numerator and one positive local denominator."""

    real: int = 0
    imag: int = 0
    denominator: int = 1

    def __post_init__(self) -> None:
        bounded(self.real)
        bounded(self.imag)
        if bounded(self.denominator) < 1:
            raise ValueError("source amplitude denominator must be positive")


@dataclass(frozen=True, slots=True)
class EnvelopeRemainder:
    """A signed subunit source remainder, independent of the latest weight."""

    numerator: int = 0
    denominator: int = 1

    def __post_init__(self) -> None:
        bounded(self.numerator)
        if bounded(self.denominator) < 1 or abs(self.numerator) >= self.denominator:
            raise ValueError("source remainder must have magnitude below its positive denominator")
