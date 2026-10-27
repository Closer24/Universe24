"""The file's one reader (R6 of the readings' map, 2026-10-26, under the owner's word of 12:2x UTC): what the clock reads of the two files at its load before it adds, each a function of the clock's state at every clock alike: the load (the regulator's notch), the two rates, the stopped mask, the (cos, sin) pair at a count along the one circuit, the turnover's bottom, Rule3's integers at a ratio and at a train (the former node.rule, node.rule_of and node.content kept by name) and the mean teeth of the regulator's two notches (the former Interval.mean_wall); the mesh's readings are meshes.py's and the hands' wind is hands.wind."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import rates, rule3
from event_universe.core.rule3 import remainder
from event_universe.core.spokes import SPOKES
from event_universe.features import standard, stretch
from event_universe.trains import REGULATOR, Gear, Train

if TYPE_CHECKING:
    from event_universe.clock import Clock


def rates_of(clock: Clock, c: Any) -> tuple[Any, Any]:
    """The clock's two rates from its load, the rate p_0 and the mesh rate p_i (X2: rates(load)), one reading; a load below 0 (a hill) read at 0, so no clock runs faster than the full rate, the great clock's (the owner's word of 2026-10-27, 18:5x UTC: the whole system one great clock that runs the small clocks)."""
    held = np.maximum(np.asarray(c, dtype=object), 0)
    return rates.rate_of(clock.full_rate, held), rates.mesh_rate_of(clock.full_rate, held)


def stopped_of(clock: Clock, c: Any) -> Any:
    """The stopped mask from the load (BH-S1): the clocks whose mesh rate reads 0 at the tick's start, one reading for the tick, the striking and the writer."""
    mesh_rate = np.asarray(rates_of(clock, c)[1], dtype=object)
    return mesh_rate == 0 if np.ndim(mesh_rate) else np.zeros(clock.size, dtype=bool)


def load(clk: Clock) -> Any:
    """The load at every clock, the notch of the regulator's time gear."""
    return np.asarray(stretch.load_of(clk.full_rate, clk.train(REGULATOR).gears[0].now), dtype=object)


def standard_angle(clock: Clock, n: Any) -> tuple[int, int]:
    """The integer (cos, sin) pair at the count n along the one circuit from the first pair (features/standard): the circuit a table built as far as the counts reach and stored to the half turn H alone, the first count where the cosine rises, the floor's one tie rule (standard.deviation's; the former rule where it stops falling struck, DAVID-CLOSE-LAW item 6) (3,142 at the full rate 1,000, pi times the full rate to the integer; 254,469, the deepest cosine over 400,000 counts, the former docstring's number, H-Confirm-Build-25), every count beyond read by the circuit's own symmetry, the pair at 2 H - n with the sine negated, modulo the full turn 2 H (the Boss's word of 2026-10-26, 11:33 UTC, 6414995372, under the owner's delegation of 08:3x: the table of the heavy quartet legs' beat reached 12,581,080 pairs and killed the run; the walked circuit beyond H kept by name, the symmetry's read differing from it by the rounding of each step alone)."""
    n = int(n)
    s = 1 if n >= 0 else -1
    n = abs(n)
    while clock.circuit_half is None and len(clock.circuit) <= n:
        c, sn = clock.circuit_gears[-1]
        c, sn = standard.act(c, clock.full_rate, 1), standard.act(sn, clock.full_rate, 1)
        if int(c[0]) > clock.circuit[-1][0] and len(clock.circuit) > 1:
            clock.circuit_half = len(clock.circuit) - 1
            break
        clock.circuit_gears = [(c, sn)]
        clock.circuit.append((int(c[0]), int(sn[0])))
    if clock.circuit_half is not None and n > clock.circuit_half:
        n = remainder(n, clock.circuit_half + clock.circuit_half)
        if n > clock.circuit_half:
            n, s = clock.circuit_half + clock.circuit_half - n, -s
    c_, sn_ = clock.circuit[n]
    return c_, s * sn_


def gearing(
    clock: Clock, ratio: tuple[int, int], c: Any, factors: tuple[Any, ...], held: Any = None
) -> rule3.Gearing:
    """Rule3's integers of a ratio at the clock's rates from the load, in the regulator's unit (PM-S1); the spring's rate read at the held load (the load with the held fields' notches at their weights, the tick's start reading clock.start_held unless given: a held field moves the mass and not the meshes, the step and the strike reading one spring)."""
    mesh_rate = rates_of(clock, c)[1]
    spring_rate = rates_of(clock, clock.start_held if held is None else held)[0]
    return rule3.gearing(ratio[0], ratio[1], clock.full_rate, spring_rate, mesh_rate, factors, clock.G)


def gearing_of(
    clock: Clock, r: Train, c: Any, factors: tuple[Any, ...], held: Any = None
) -> rule3.Gearing:
    """A train's gearing: Rule3's integers at its ratio and the clock's rates, or, for the train with its own teeth, no meshes and the own hold 2 teeth (next = 2 now - before + the drive inside the carry)."""
    if r.teeth is not None:
        return rule3.Gearing(tuple(0 for _ in range(SPOKES)), r.teeth + r.teeth, r.teeth, 0)
    assert r.ratio is not None
    return gearing(clock, r.ratio, c, factors, held)


def mean_teeth(clock: Clock, gear: Gear) -> Any:
    """The mean teeth (teeth div 2)(stretch_before + stretch_now) of the regulator's time gear as given: the trains' own before the regulator's act for the impulse and the advances, the act's at its end for the driven gears' carries."""
    return rule3.mean_teeth_of(clock.teeth, gear.before, gear.now)


def bottom(clock: Clock) -> int:
    """The regulator's notch at the load -full_rate, the turnover's bottom."""
    return int(
        np.asarray(
            stretch.stretch_of(clock.full_rate, np.array([-clock.full_rate], dtype=object)), dtype=object
        ).reshape(-1)[0]
    )
