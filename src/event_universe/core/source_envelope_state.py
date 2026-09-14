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


@dataclass(frozen=True, slots=True)
class NullRecord:
    """This Node's own null: its unscaled weight and the scale it assumed at that tick.

    A notice ordered before that null that arrives afterwards changes the assumed
    scale; the record lets the Node issue the exact correction of its own factor.
    """

    tick: int
    weight_numerator: int
    weight_denominator: int
    scale_numerator: int = 1
    scale_denominator: int = 1

    def __post_init__(self) -> None:
        if bounded(self.tick) < 0:
            raise ValueError("null record tick must be nonnegative")
        if (
            bounded(self.weight_denominator) < 1
            or not 0 <= bounded(self.weight_numerator) <= self.weight_denominator
        ):
            raise ValueError("null record weight must be a probability")
        if bounded(self.scale_denominator) < 1 or bounded(self.scale_numerator) < self.scale_denominator:
            raise ValueError("null record scale must be a rational of at least one")


@dataclass(frozen=True, slots=True)
class EnvelopeScale:
    """A positive rational weight multiplier of at least one, applied to squared weights."""

    numerator: int = 1
    denominator: int = 1

    def __post_init__(self) -> None:
        if bounded(self.denominator) < 1 or bounded(self.numerator) < self.denominator:
            raise ValueError("source weight scale must be a rational of at least one")
