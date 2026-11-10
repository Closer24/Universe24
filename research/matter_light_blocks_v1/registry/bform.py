"""Initial data in cumulative-hand form (r29 Theorem B0); data only, nothing here evolves a state.

With B the running sum of the hand b, Rule3 on a set of active channels -- every input partner of an active channel
is active, or a private vacuum partner fed by that channel alone -- reads, while |B| <= 1,

    B_v(t+1) + B_v(t-1) = floor((c_v + sum_w A_vw B_w(t)) / 3)        (c_v = rest class of v, A = signed coupling).

So B(-1), B(0) and the rest classes fix the complete state at t = 0:

    a = B(0) - B(-1),   b = B(1) - B(0),   theta = (c + A B(0)) mod 3,   r = 2 theta,

with B(1) from the relation above, and a private vacuum partner (weight w) of a channel with B(0) = S rests at class
1 + w S (the history halo).  ``beta_field`` is the free fused mover beta_n of a class-0 chain of weight -1 (r29
Theorem C: an exact translator by one node per 3 updates; beta_1 is r06's SLOW glider).
"""
from __future__ import annotations

from universe24.core.group_2o import DIRECTIONS


def bform_cells(coupling, nodes, classes, Bm1, B0):
    """{(x, y, z, g): (a, b, r)} for the active ``nodes`` (local, unwrapped addresses) with rest ``classes`` and the
    cumulative hands ``Bm1`` = B(-1), ``B0`` = B(0); the history halo goes on private vacuum partners.  A vacuum
    channel fed by two active channels is refused (it would be a hidden coincidence node)."""
    index = {tuple(a): i for i, a in enumerate(nodes)}
    n = len(index)
    if n != len(nodes) or not len(classes) == len(Bm1) == len(B0) == n:
        raise ValueError("nodes, classes and hands must be distinct and of one length")
    U, halo = [int(c) for c in classes], {}
    for i, (x, y, z, g) in enumerate(index):
        for d in range(6):
            rec = (x + DIRECTIONS[d][0], y + DIRECTIONS[d][1], z + DIRECTIONS[d][2], coupling.ports[d][g])
            w = coupling.weights[d][g]
            j = index.get(rec)
            if j is not None:
                U[j] += w * int(B0[i])
            elif rec in halo:
                raise ValueError(f"vacuum channel {rec} is fed by two active channels")
            else:
                halo[rec] = (i, w)
    cells = {}
    for i, k in enumerate(index):
        B1 = U[i] // 3 - int(Bm1[i])
        cells[k] = (int(B0[i]) - int(Bm1[i]), B1 - int(B0[i]), 2 * (U[i] % 3))
    for rec, (i, w) in halo.items():
        if B0[i]:
            cls = 1 + w * int(B0[i])
            if not 0 <= cls <= 2:
                raise ValueError("history halo outside the window |B| <= 1")
            cells[rec] = (0, 0, 2 * cls)
    return cells


def beta_field(n, offsets, t):
    """B at time t of the free fused mover beta_n on chain nodes at signed offsets dy behind (< 0) or ahead (> 0) of
    its front, the front node being activated at t = 0: B = psi_k at k = t - 3 dy (k >= 0 even, k / 2 <= 2n), with
    psi = -1, +1, -1, ... (2n + 1 values); 0 elsewhere."""
    psi = [(-1 if i % 2 == 0 else 1) for i in range(2 * n + 1)]
    out = []
    for dy in offsets:
        k = t - 3 * dy
        out.append(psi[k // 2] if k >= 0 and k % 2 == 0 and k // 2 < len(psi) else 0)
    return out
