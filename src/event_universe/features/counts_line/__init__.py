"""The count's line: W_c c_next + r' = W_c c_now + SUM over the six Ports of F_ij + r, Rule3 for the family of clicks at every Node with the family's current as its read and the count's wall W_c = 3 den T as its wall, F_ij = num (now_i before_j - before_i now_j) the current into Node i from its neighbour j, the booking of the family's two levels at the Link's two ends; the click is the division's carry of one whole quantum, the inverse the same line with the current reversed (ALGEBRA.md #the-counts-line). The count is the family's, one array per family over the GameBoard; a count may stand below 0 at a Node (a hole the line conserves), and the line keeps no block and no clamp (a clamp at 0 would create quanta). Beside the count the line books the tension on each axis, T_aa(i) = num (G_aa(i) + G_aa(i - a)) div 2 with G_aa(i) = now_i (now_(i+2a) - now_i) - now_(i+a) (now_(i+a) - now_(i-a)) the flux of the a-momentum through the a-Link at one time, Rule3's own conservation of the current per axis, read and never written (ALGEBRA.md #the-primitives, the row "the hold")."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import NO_READ, rule3

Vector = tuple[Any, Any, Any]
PORTS = 6  # a Node's six Ports, the lattice's own integer (Rule3's 6)
PRODUCTS = 2  # the current's two products, now_i before_j and before_i now_j
LEVELS = (
    2  # a record's two level pairs, the real and the second (the rotation sense), whose currents add
)


@dataclass(frozen=True)
class Levels:
    """A family's two levels at one Node or across one Port: now and before."""

    now: Any
    before: Any


@dataclass(frozen=True)
class Differences:
    """The level now at the Node and its difference across one axis's two Ports, D_a = the +a arrival minus the -a arrival: at the Node (`here`) and the neighbours' own differences brought through the +a Port (`plus`) and the -a Port (`minus`)."""

    now: Any
    here: Any
    plus: Any
    minus: Any


@dataclass(frozen=True)
class CountTerm:
    """The family of clicks' declaration: the count's wall W_c = 3 den T; the current's weight (the pair's num); the amplitude bound A of the levels; the largest count."""

    norm: int
    weight: int
    amplitude: int
    most: int


@dataclass(frozen=True)
class CountStart:
    """The interval's reading after the step: the count c and its remainder r at every Node, the family's levels here and across the six Ports in the order +x, -x, +y, -y, +z, -z, the direction +1 forward, -1 backward, the second level pair's here and across the Ports (None: a real record), whose current adds, and per level pair the three axes' differences for the tension (none: no tension booked)."""

    count: Any
    remainder: Any
    here: Levels
    links: tuple[Levels, ...]
    direction: int
    second: tuple[Levels, tuple[Levels, ...]] | None = None
    differences: tuple[tuple[Differences, Differences, Differences], ...] = ()


@dataclass(frozen=True)
class CountWrites:
    """The line's writes: the count and its remainder after the act; the inflow per axis it read, the current into the Node through the axis's two Ports; the current into the Node through each of the six Ports; and the tension per axis, T_xx, T_yy, T_zz, the stresses Rule3 reads into the Link's paces."""

    count: Any
    remainder: Any
    net: Vector
    through: tuple[Any, ...]
    stress: Vector


def current(weight: int, here: Levels, there: Levels) -> Any:
    """The current into the Node here from the Node there through their Link, weight (now_i before_j - before_i now_j), positive inward (ALGEBRA.md #the-booking)."""
    return weight * (here.now * there.before - here.before * there.now)


def tension(weight: int, d: Differences) -> Any:
    """The tension on one axis at the Node, T_aa(i) = weight x (G_aa(i) + G_aa(i - a)) div 2, the mean of the a-momentum's flux through the Node's two a-Links at one time, G_aa(i) = now_i (now_(i+2a) - now_i) - now_(i+a) (now_(i+a) - now_(i-a)): with the differences D it is weight x (now_i (D_(i+a) - D_(i-a)) - D_i^2) div 2, a plane wave's -2 b^2 sin^2 k_a and a uniform record's 0 (ALGEBRA.md #the-primitives, the row "the hold", the tension)."""
    return rule3(NO_READ, NO_READ, weight, 2, d.now * (d.plus - d.minus) - d.here * d.here, 0, 0)[0]


def stress(weight: int, differences: tuple[Differences, Differences, Differences]) -> Vector:
    """The tension on each axis at every Node from one level pair's differences."""
    x, y, z = (tension(weight, d) for d in differences)
    return x, y, z


def bound(term: CountTerm) -> int:
    """The largest total the line reaches at a Node whose levels stand at A: one current per Port, the weight times the two products of two levels at A, W_c (most + 1) and the remainder below W_c (ALGEBRA.md #the-counts-line, the bound)."""
    current_bound = abs(term.weight) * PRODUCTS * LEVELS * term.amplitude * term.amplitude
    return PORTS * current_bound + term.norm * (term.most + 1) + term.norm


def check(term: CountTerm, start: CountStart) -> None:
    """The refusals by name: W_c from 1, the direction +1 or -1, six Links, the total within int64."""
    if term.norm < 1:
        raise ValueError(f"the count's line needs W_c = {term.norm} from 1")
    if start.direction not in (1, -1):
        raise ValueError(f"the count's line runs in the direction +1 or -1, got {start.direction}")
    if len(start.links) != PORTS:
        raise ValueError(f"the count's line reads six Links, one per Port, got {len(start.links)}")
    if bound(term) > MAX_WORK_INT:
        raise ValueError(
            f"the count's line at A = {term.amplitude}, the weight {term.weight}, W_c = {term.norm} and "
            f"the count up to {term.most} reaches the total {bound(term)}, beyond int64: the run is refused"
        )


def apply(term: CountTerm, start: CountStart) -> CountWrites:
    """The line at every Node: the current through each Port (the second level pair's added where the record has one), the inflow per axis through its +a and -a Ports, read by Rule3 with the coefficient sigma on each axis and W_c on the count over the wall W_c; the tension per axis beside it, summed over the level pairs whose differences are given (ALGEBRA.md #the-counts-line)."""
    check(term, start)
    through = [current(term.weight, start.here, start.links[port]) for port in range(PORTS)]
    if start.second is not None:
        here, links = start.second
        through = [through[port] + current(term.weight, here, links[port]) for port in range(PORTS)]
    tensions: Vector = (0, 0, 0)
    for differences in start.differences:
        found = stress(term.weight, differences)
        tensions = (tensions[0] + found[0], tensions[1] + found[1], tensions[2] + found[2])
    x, y, z = (through[2 * axis] + through[2 * axis + 1] for axis in range(3))
    net = (x, y, z)
    sigma = start.direction
    count, remainder = rule3(
        (sigma, sigma, sigma), net, term.norm, term.norm, start.count, 0, start.remainder
    )
    return CountWrites(count, remainder, net, tuple(through), tensions)
