"""The metric's sources and the flux lines' fold, Y-S1 to Y-S3 (H-Six-Metric-Lines-3, 2026-10-26, the Boss's order under the owner's delegation): the stress tensor's diagonal parts and their trace (the tensions, the time line's write), its off-diagonal parts (the shears, T_2g) and the records' count flux on each axis (the momentum density, T_1u: the record's own velocities in and out against the centred gradient of its levels at the start, one Link's reach, the same integers in either direction), the nine axis lines' sources by the position of their reading; the read, the planes with a gap turned at each Link by the flux lines' odd part at the record's rest rotation K = omega_0 Gamma (`rotation_of`) as a second tangent triple multiplied into the odd line's (links.folded, the former fold_links kept by name), the row at the gap 0 turned by nothing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from event_universe import gram
from event_universe.core.ports import AXES, transverse
from event_universe.links import gradient
from event_universe.rows import zeros

if TYPE_CHECKING:
    from event_universe.node import Node

Sources = list[tuple[list[Any], int]]


def stress_parts(rows: Sources, shape: tuple[int, ...]) -> list[Any]:
    """The stress tensor's three diagonal parts from the records' levels, one act on every record alike: SUM over records of num x d.d with d the gradient of the lines along the axis (the sum of the lines' squared gradients); `rows` holds (levels, num) pairs."""
    parts = [zeros(shape) for _ in range(AXES)]
    for levels, num in rows:
        for a in range(AXES):
            d = [gradient(x, a) for x in levels]
            parts[a] = parts[a] + num * gram.dot(d, d)
    return parts


def shear_parts(rows: Sources, shape: tuple[int, ...]) -> list[Any]:
    """The stress tensor's three off-diagonal parts on the axis pairs (a, a + 1): xy, yz, zx, the shears' source (Y-S1): SUM over records of num x d_a.d_b, the Node's product of its two centred gradients, T_2g under the cube's 48 (the sign the product of the two axes' signs), one Link's reach, the same act on every record as the diagonal parts; 0 at a Node where one body stands alone, the two-body tidal term between two."""
    parts = [zeros(shape) for _ in range(AXES)]
    for levels, num in rows:
        d = [[gradient(x, a) for x in levels] for a in range(AXES)]
        for a in range(AXES):
            b = transverse(a)[0]
            parts[a] = parts[a] + num * gram.dot(d[a], d[b])
    return parts


def tensor_parts(parts: list[Any]) -> tuple[Any, list[Any]]:
    """A tensor's trace and its traceless diagonal parts: trace = SUM_a parts_a; traceless_a = 3 parts_a - trace (the stress's trace is the time line's, the axis lines traceless)."""
    trace = sum(parts[:AXES])
    return trace, [AXES * part - trace for part in parts]


def net_flux(nows: list[Any], velocities: list[Any], axis: int) -> Any:
    """A record's count flux on an axis at every Node (Y-S1, Y-S3): u.D_a N, the record's own velocity against the centred gradient of its levels at the start through the axis's two Links (the momentum density, the continuum's T_0a; summed over the board the lattice momentum, SUM_i F(i, i + a) with F_ij = u_i N_j - N_i u_j), odd under the axis's inversion (T_1u), one Link's reach, no division; the flux lines' source."""
    return gram.dot(velocities, [gradient(n, axis) for n in nows])


def rotation_of(node: Node, pair: tuple[int, int]) -> int:
    """The record's rest rotation to the unit, K = omega_0 Gamma with cos omega_0 = num / den (Y-S2, The clock family on the Ports): the count along the law's orbit at the step 1 / Gamma at which the orbit's cosine first falls to num / den (gram.cosine_count, a search by comparisons and no root), found once per pair and kept on the Node."""
    if pair not in node.rotations:
        node.rotations[pair] = gram.cosine_count(node, pair[0], pair[1])
    return node.rotations[pair]
