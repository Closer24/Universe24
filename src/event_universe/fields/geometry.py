"""Reusable integer mapping from two scalar samples to a link length."""

from dataclasses import dataclass

from event_universe.core.state import checked, checked_work


@dataclass(frozen=True, slots=True)
class MeanStretch:
    base: int
    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        for value in (self.base, self.numerator, self.denominator):
            checked(value)
        if self.base < 1 or self.numerator < 0 or self.denominator < 1:
            raise ValueError("invalid stretch parameters")

    def __call__(self, local: int, received: int) -> int:
        checked(local)
        checked(received)
        if min(local, received) < 0:
            raise ValueError("nonnegative samples required")
        total = checked_work(local + received)
        scaled = checked_work(total * self.numerator)
        divisor = checked_work(2 * self.denominator)
        return checked(self.base + scaled // divisor)
