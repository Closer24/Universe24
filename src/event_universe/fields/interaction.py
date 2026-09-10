"""Bounded local variations of a single interaction term S_int = g * n * phi.

This is an interaction action, not a full action-derived time integrator.
Source and force use the same immutable coefficient and the same term.
"""

from dataclasses import dataclass

from event_universe.core.state import Neighbors, Vector, checked, checked_work


@dataclass(frozen=True, slots=True)
class ScalarInteraction:
    """One nonnegative integer coupling in declared action/field units.

    No world, source identity, history, or mutable private state. Six samples
    must already be delivered locally; this calculation performs no transport.
    """

    coupling: int = 64

    def __post_init__(self) -> None:
        checked(self.coupling)
        if self.coupling < 0:
            raise ValueError("nonnegative scalar coupling required")

    def term(self, sources: int, phi: int) -> int:
        """S_int at one location; bound each product before any cancellation."""
        checked(sources)
        checked(phi)
        if sources < 0:
            raise ValueError("source count cannot be negative")
        return checked_work(checked_work(self.coupling * sources) * phi)

    def source(self, sources: int, coefficient: int) -> int:
        """Exact variation S(n,1)-S(n,0); reject a mismatching source knob."""
        checked(coefficient)
        if coefficient != self.coupling:
            raise ValueError("source coefficient must equal the shared coupling")
        return checked_work(self.term(sources, 1) - self.term(sources, 0))

    def force_numerator(self, neighbors: Neighbors) -> Vector:
        """Central spatial action difference for one particle, BEFORE division by 2.

        Use the same term at each +/- neighbor. No dominant-axis suppression.
        A downstream integer accumulator divides by 2 * impulse_units.
        """
        if len(neighbors) != 6:
            raise ValueError("exactly six delivered samples required")
        values = tuple(self.term(1, phi) for phi in neighbors)
        return (
            checked_work(values[0] - values[1]),
            checked_work(values[2] - values[3]),
            checked_work(values[4] - values[5]),
        )

    @staticmethod
    def response_denominator(impulse_units: int) -> int:
        """Two is the +/- stencil separation; impulse_units is an explicit scale."""
        checked(impulse_units)
        if impulse_units < 1:
            raise ValueError("positive integer impulse scale required")
        return checked(2 * impulse_units)

    def local_energy_twice(self, phi: int, neighbors: Neighbors, sources: int, denominator: int) -> int:
        """Local spatial functional with neighbors held fixed, NOT global energy.

        (D-6)*phi**2 + sum6((phi-neighbor)**2) - 2*S_int.
        Its centered phi variation / 4 equals D*phi - sum6 - g*n.
        This identifies the stationary stencil, not the relaxation dynamics as
        a variational time integrator. Summing this would double-count edges.
        """
        checked(phi)
        checked(denominator)
        if denominator < 6 or len(neighbors) != 6:
            raise ValueError("six neighbors and nonnegative screening required")
        total = checked_work((denominator - 6) * checked_work(phi * phi))
        for neighbor in neighbors:
            checked(neighbor)
            difference = checked_work(phi - neighbor)
            total = checked_work(total + checked_work(difference * difference))
        return checked_work(total - checked_work(2 * self.term(sources, phi)))
