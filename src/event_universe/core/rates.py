"""The composed rates, the law's two functions of the load (ALGEBRA.md #the-rates; PC-S1, the owner's approved sentence K-S4 in pc1's form, 2026-10-25): the rate p_0(c) = Gamma (1 - 1 / Gamma)^c to the unit, the exact power rounded half up once, by the law's carry at the resolution Gamma^2: N_0 = Gamma^3 with the fine tooth r_0 = Gamma div 2, N(c + 1) Gamma + r(c + 1) = N(c) (Gamma - 1) + r(c), one carry per load at the teeth Gamma, the rate rounded(N, Gamma^2) half up, bit for bit the exact power at every load to the edge; a hill (c < 0) by the inverse factors, N Gamma + r over Gamma - 1; the mesh rate the rate twice, p_a = p_0^2 div Gamma rounded once (h N = 1, the ruler goes with the rate), the rate the primary number and its square derived, so no act takes a root and every integer stays within the width (40 bits at Gamma 1,000; the former running fraction of 4.0, the one transient beyond the former width, kept by name and gone). The assembly certifies the margin once per Gamma, one pass to the stopped load, and refuses by name where the half lies within one of N (`certified`). The table per Gamma holds each load's rate once, two sides, the hollows (c >= 0) and the hills (c < 0); the vectorised entries look every clock's load up in the array's own kind. The one rounding of a coefficient (`rounded`, half up on the magnitude with the sign after, odd) and the integer sine of a ratio (`sine_rim`) stand beside. The mesh rate rounds to 0 first, where p_0^2 falls below Gamma div 2 (`stopped_load`, the standstill's load)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cache
from typing import Any

import numpy as np

from event_universe.core import acts
from event_universe.core.rule3 import half, largest_below


def rounded(numerator: Any, teeth: Any) -> Any:
    """The one rounding of a coefficient of the clock (the one rule of the remainder; the former plain half-up rounding, the same integers at a numerator of either sign but a negative odd one, struck 2026-10-26 under NL-S1, its one read, the tension's mean, spelt as the carry's carries in meshes.factors; the former odd_rounded kept by name): the numerator over the teeth rounded half up on the magnitude with the sign after, one carry from the half teeth at the doubled teeth, the carry flipped (acts.flip, the former rule3.mirrored kept by name) where the numerator is negative, odd at every integer, no fine tooth kept, a rate and a factor being coefficients of the tick and no notch; integers or arrays over the whole great clock alike, the flip in the numerator's own kind."""
    signed = np.asarray(numerator)
    kind, below = signed.dtype, signed < 0
    negative = below.astype(kind) if below.ndim else int(below)
    carry = teeth + negative * (acts.flip(teeth, teeth + teeth, 1) - teeth)
    return acts.carry(numerator + numerator, teeth + teeth, carry)[0]


def sine_rim(pinion: int, rim: int, scale: int = 1) -> int:
    """The integer sine of a ratio at a scale, scale rim sin omega to the unit: the largest x with x^2 <= scale^2 (rim^2 - pinion^2), one search on the whole product (`rule3.largest_below`), no root and no division before the search; 0 at |pinion| = rim, a ratio at the spring 0."""
    return largest_below(scale * scale * (rim * rim - pinion * pinion))


@dataclass
class Side:
    """One side of the rates' table at one Gamma, the hollows or the hills: the rates and the mesh rates found so far by the load's size |c|, and the carry's state at the next load, N at the resolution Gamma^2 with its fine tooth, the numerator's factor and the teeth."""

    factor: int
    teeth: int
    scaled: int
    carry: int
    rates: list[int] = field(default_factory=list)
    meshes: list[int] = field(default_factory=list)

    def fill_to(self, full_rate: int, size: int) -> None:
        """The side filled through the size |c|: the rate rounded(N, Gamma^2) half up, the mesh rate from it, p_0^2 over Gamma rounded once, then one carry per load."""
        while len(self.rates) <= size:
            clock_rate = int(rounded(self.scaled, full_rate * full_rate))
            self.rates.append(clock_rate)
            self.meshes.append(int(rounded(clock_rate * clock_rate, full_rate)))
            scaled, carry = acts.carry(self.scaled * self.factor, self.teeth, self.carry)
            self.scaled, self.carry = int(scaled), int(carry)

    def undecided(self, full_rate: int, size: int) -> list[int]:
        """The loads through the size where the half lies within one of N, rounded(N - 1) != rounded(N + 1) at the resolution Gamma^2: none at a certified Gamma."""
        self.fill_to(full_rate, size)
        found, scaled, carry = [], full_rate * full_rate * full_rate, int(half(self.teeth))
        for load in range(size + 1):
            if rounded(scaled - 1, full_rate * full_rate) != rounded(scaled + 1, full_rate * full_rate):
                found.append(load)
            scaled, carry = (int(x) for x in acts.carry(scaled * self.factor, self.teeth, carry))
        return found


@cache
def sides(full_rate: int) -> tuple[Side, Side]:
    """The table at one Gamma, the hollows' side and the hills', each starting at N_0 = Gamma^3 with its fine tooth at the half teeth, the hollows by Gamma - 1 over Gamma per load and the hills by Gamma over Gamma - 1."""
    return (
        Side(full_rate - 1, full_rate, full_rate * full_rate * full_rate, int(half(full_rate))),
        Side(full_rate, full_rate - 1, full_rate * full_rate * full_rate, int(half(full_rate - 1))),
    )


@cache
def certified(gamma: int) -> int:
    """The assembly's certificate once per Gamma: one pass to the stopped load on the hollows' side, refused by name where a load is undecided (the half within one of N); the stopped load returned."""
    stopped = stopped_load(gamma)
    undecided = sides(gamma)[0].undecided(gamma, stopped)
    if undecided:
        raise ValueError(
            f"the clock at Gamma {gamma} is undecided at the contents {undecided[0]}: the paces are refused"
        )
    return stopped


def side_of(full_rate: int, load: int) -> Side:
    """The side of the table the load falls on, the hollows' at or above 0 and the hills' below, filled through the load's size."""
    hollows, hills = sides(full_rate)
    side = hills if load < 0 else hollows
    side.fill_to(full_rate, abs(load))
    return side


def rate(full_rate: int, load: int) -> int:
    """The rate at a clock of load c, p_0 = Gamma (1 - 1 / Gamma)^c to the unit by the carry (`Side.fill_to`)."""
    return side_of(full_rate, load).rates[abs(load)]


def mesh_rate(full_rate: int, load: int) -> int:
    """The mesh rate at the load c, the rate twice: p_a = p_0^2 div Gamma rounded once from the rate's integer, Gamma at the vacuum; the rate of every mesh of a clock from the clock's own load, before the mesh's own tension enters."""
    return side_of(full_rate, load).meshes[abs(load)]


def stopped_load(full_rate: int) -> int:
    """The least load at which the mesh rate rounds to 0 at Gamma, p_0^2 below Gamma div 2 (the standstill's load, about (Gamma div 2) ln(2 Gamma)): the table walked from the vacuum to the first 0."""
    hollows = sides(full_rate)[0]
    load = 0
    while True:
        hollows.fill_to(full_rate, load)
        if hollows.meshes[load] == 0:
            return load
        load += 1


def looked_up(found: Callable[[Side], list[int]], full_rate: int, loads: Any) -> Any:
    """One of the table's two functions of the load at every clock (`found`, a side's rates or its mesh rates): a scalar load as it is; an empty array as it is; an array looked up through the table and spread back over the clocks in the array's own kind, on every value from its least to its largest where that range is narrower than the great clock and on its distinct values otherwise; the same integers either way."""
    values = np.asarray(loads)
    if values.ndim == 0:
        return found(side_of(full_rate, int(values)))[abs(int(values))]
    if values.size == 0:
        return values
    low, high = int(values.min()), int(values.max())
    if high - low < values.size:
        hollows, hills = sides(full_rate)
        hollows.fill_to(full_rate, max(high, 0))
        hills.fill_to(full_rate, max(-low, 0))
        below = found(hills)[-low : max(-high - 1, 0) : -1] if low < 0 else []
        table = below + found(hollows)[max(low, 0) : high + 1]
        return np.array(table, dtype=values.dtype)[(values - low).astype(int)]
    distinct, inverse = np.unique(values, return_inverse=True)
    table = [found(side_of(full_rate, int(c)))[abs(int(c))] for c in distinct.tolist()]
    return np.array(table, dtype=values.dtype)[np.asarray(inverse).reshape(values.shape)]


def rate_of(full_rate: int, loads: Any) -> Any:
    """The rate at every clock from the clock's load (`rate` through the table)."""
    return looked_up(lambda side: side.rates, full_rate, loads)


def mesh_rate_of(full_rate: int, loads: Any) -> Any:
    """The mesh rate at every clock from the load read on the mesh (`mesh_rate` through the table)."""
    return looked_up(lambda side: side.meshes, full_rate, loads)
