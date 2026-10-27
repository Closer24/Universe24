"""The regulator's sources and the flow gears' skew, Y-S1 to Y-S3 (H-Six-Metric-Lines-3, 2026-10-26, the Boss's order under the owner's delegation): the stress tensor's diagonal parts and their trace (the tensions, the time gear's drive), its off-diagonal parts (the shears, T_2g) and the hands' count flow on each axis (the momentum density, T_1u: the hand's own velocities in and out against the centred gradient of its notches at the start, one mesh's reach, the same integers forward and backward), the nine axis gears' sources by the position of their reading; the read, the sprung hands turned at each mesh by the flow gears' odd part at the hand's rest rate K = omega_0 full_rate (`rest_rate_of`) as a second tangent triple multiplied into the odd gear's (meshes.skewed, the former fold_links kept by name), the unsprung train turned by nothing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from event_universe import hands
from event_universe.core.spokes import AXES, transverse
from event_universe.meshes import gradient

if TYPE_CHECKING:
    from event_universe.clock import Clock


def stress_of(notches: list[Any], velocity: list[Any]) -> list[Any]:
    """A hand's stress as one outer product (Y-S1 to Y-S3), Re(conj(d_mu z) d_nu z) of the Gaussian hand, the dot over its gears (hands.dot) of two of its changes, d_0 z its velocity and d_a z the centred gradient of its notches along the axis a at the tick's start: the nine axis gears' sources in the regulator's order, the diagonal (a, a) (the tensions before the trace is taken), the flows (0, a) (the momentum density, odd under the axis's inversion, T_1u) and the shears (a, a + 1) (xy, yz, zx, T_2g: the sign the product of the two axes' signs); one mesh's reach, no carry, the same act on every hand."""
    d = [[gradient(x, a) for x in notches] for a in range(AXES)]
    pairs = [(d[a], d[a]) for a in range(AXES)] + [(velocity, d[a]) for a in range(AXES)]
    return [hands.dot(x, y) for x, y in pairs + [(d[a], d[transverse(a)[0]]) for a in range(AXES)]]


def tensor_parts(parts: list[Any]) -> tuple[Any, list[Any]]:
    """A tensor's trace and its traceless diagonal parts: trace = SUM_a parts_a; traceless_a = 3 parts_a - trace (the stress's trace is the time gear's, the axis gears traceless)."""
    trace = sum(parts[:AXES])
    return trace, [AXES * part - trace for part in parts]


def rest_rate_of(clock: Clock, ratio: tuple[int, int]) -> int:
    """The hand's rest rate to the unit, K = omega_0 full_rate with cos omega_0 = pinion / rim (Y-S2, The clock train on the Ports): the count along the law's circuit at the step 1 / full_rate at which the circuit's cosine first falls to pinion / rim (hands.cosine_count, a search by comparisons and no root), found once per ratio and kept on the clock."""
    if ratio not in clock.rest_rates:
        clock.rest_rates[ratio] = hands.cosine_count(clock, ratio[0], ratio[1])
    return clock.rest_rates[ratio]
