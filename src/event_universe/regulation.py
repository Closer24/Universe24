"""The regulator's sources and the flow gears' skew, Y-S1 to Y-S3 (H-Six-Metric-Lines-3, 2026-10-26, the Boss's order under the owner's delegation): the stress tensor's diagonal parts and their trace (the tensions, the time gear's drive), its off-diagonal parts (the shears, T_2g) and the hands' count flow on each axis (the momentum density, T_1u: the hand's own velocities in and out against the centred gradient of its notches at the start, one mesh's reach, the same integers forward and backward), the nine axis gears' sources by the position of their reading; the read, the sprung hands turned at each mesh by the flow gears' odd part at the hand's rest rate K = omega_0 full_rate (`rest_rate_of`) as a second tangent triple multiplied into the odd gear's (meshes.skewed, the former fold_links kept by name), the unsprung train turned by nothing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from event_universe import hands
from event_universe.core.spokes import AXES, transverse
from event_universe.meshes import gradient
from event_universe.trains import zeros

if TYPE_CHECKING:
    from event_universe.clock import Clock

Sources = list[tuple[list[Any], int]]


def stress_parts(trains: Sources, size: tuple[int, ...]) -> list[Any]:
    """The stress tensor's three diagonal parts from the hands' notches, one act on every hand alike: SUM over hands of pinion x d.d with d the gradient of the gears along the axis (the sum of the gears' squared gradients); `trains` holds (notches, pinion) pairs."""
    parts = [zeros(size) for _ in range(AXES)]
    for notches, pinion in trains:
        for a in range(AXES):
            d = [gradient(x, a) for x in notches]
            parts[a] = parts[a] + pinion * hands.dot(d, d)
    return parts


def shear_parts(trains: Sources, size: tuple[int, ...]) -> list[Any]:
    """The stress tensor's three off-diagonal parts on the axis pairs (a, a + 1): xy, yz, zx, the shears' source (Y-S1): SUM over hands of pinion x d_a.d_b, the clock's product of its two centred gradients, T_2g under the cube's 48 (the sign the product of the two axes' signs), one mesh's reach, the same act on every hand as the diagonal parts; 0 at a clock where one bob stands alone, the two-bob tidal term between two."""
    parts = [zeros(size) for _ in range(AXES)]
    for notches, pinion in trains:
        d = [[gradient(x, a) for x in notches] for a in range(AXES)]
        for a in range(AXES):
            b = transverse(a)[0]
            parts[a] = parts[a] + pinion * hands.dot(d[a], d[b])
    return parts


def tensor_parts(parts: list[Any]) -> tuple[Any, list[Any]]:
    """A tensor's trace and its traceless diagonal parts: trace = SUM_a parts_a; traceless_a = 3 parts_a - trace (the stress's trace is the time gear's, the axis gears traceless)."""
    trace = sum(parts[:AXES])
    return trace, [AXES * part - trace for part in parts]


def net_flow(nows: list[Any], velocities: list[Any], axis: int) -> Any:
    """A hand's count flow on an axis at every clock (Y-S1, Y-S3): u.D_a N, the hand's own velocity against the centred gradient of its notches at the start through the axis's two meshes (the momentum density, the continuum's T_0a; summed over the great clock the lattice momentum, SUM_i F(i, i + a) with F_ij = u_i N_j - N_i u_j), odd under the axis's inversion (T_1u), one mesh's reach, no carry; the flow gears' source."""
    return hands.dot(velocities, [gradient(n, axis) for n in nows])


def rest_rate_of(clock: Clock, ratio: tuple[int, int]) -> int:
    """The hand's rest rate to the unit, K = omega_0 full_rate with cos omega_0 = pinion / rim (Y-S2, The clock train on the Ports): the count along the law's circuit at the step 1 / full_rate at which the circuit's cosine first falls to pinion / rim (hands.cosine_count, a search by comparisons and no root), found once per ratio and kept on the clock."""
    if ratio not in clock.rest_rates:
        clock.rest_rates[ratio] = hands.cosine_count(clock, ratio[0], ratio[1])
    return clock.rest_rates[ratio]
