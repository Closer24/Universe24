"""THIRD4's act: the third click with no indicator and no selection, a copy of step.act with one term added to its push.

Clock: at every Node-clock alike, every round, the direction is the drive's law on the giver's own count, row by row,
(delta, r3+) = carry(k a_giver, D3, r3), its tooth kept: the third click fires where that tooth carries, so "when" is read
from the giver's own count (the fallback trigger; it does not dilate). The quantum delta is shared among the n takers in
their own order by the drive's law again: takers 1 to n - 1 each carry delta w_i at the dial D_w with a tooth of their
own kept, (lam_i, r_i+) = carry(delta w_i, D_w, r_i), and the last takes the rest, lam_n = delta - SUM lam_i, so the
shares sum to delta at every round. The act's own push carries -delta W(a) on the giver and +lam_i W(a) on each taker.
Algebra: whole numbers, sums, products and Rule3's carry, each carry a linear source at a fixed dial with its remainder
kept (the drive's form), none a bound, a sign or a selection; the 24 act on r3 and the r_i as on the edge's tooth (a
negated row's tooth flipped), the mirror flips them in their dials.
Board: the engine's step functions of main b1a50bb33; with k 0 the act is step.act.
"""

import sys
from pathlib import Path
from typing import Any, NamedTuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("c5", "src")))

import numpy as np  # noqa: E402

from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import contract  # noqa: E402
from tensor24.engine.state import State  # noqa: E402

Z = Any


class Third(NamedTuple):
    """The CHOSEN integers, read from world/third.json's "chosen4": the direction's strength k and dial D3, the takers' weights w_1 .. w_(n-1) at the share dial D_w."""

    strength: int
    dial: int
    weights: tuple[int, ...]
    share_dial: int


def act4(layout: Any, roles: Any, cfg: Third, s: State, x: tuple[Z, Z]) -> tuple[State, tuple[Z, Z], Z, dict[str, Z]]:
    """One round with the third click, the true act alone (W2; the trigger the direction's own carry)."""
    _, _, _, _, gearing, plan, clock, _, click, _, _ = layout
    a, b, tooth, rd, k = s
    r3, rw = x  # the direction's teeth (giver rows, sites); the takers' share teeth (n - 1, giver rows, sites)
    force, j1 = step.sources(layout, a)
    _, _, _, teeth, _ = gearing
    _, _, _, _, key = click
    first, _ = step.drive(j1, teeth, rd)
    j = j1 + step.stress(layout, s, step.driven(gearing, force, step.kick(gearing, first)))
    q, kept = step.drive(j, teeth, rd)
    kicks = step.kick(gearing, q)
    senses, push = step.halves(layout), step.driven(gearing, force, kicks)
    wa, wb = step.dials(layout, s)
    first, _, _ = step.gear(a, b, tooth, wa + wb, wa + wb, push, senses)
    d_out = wa + step.weight(gearing, clock, first)
    a0, _, s0 = step.gear(a, b, tooth, wa + wb, d_out, push, senses)
    # WHEN and how much: the drive's law on the giver's own count
    delta, r31 = carry(cfg.strength * a[roles.giver], cfg.dial, r3)
    # WHO: takers 1 .. n - 1 by their own teeth, the last the rest
    w = np.array(cfg.weights, dtype=object)[:, None, None]
    lam_head, rw1 = carry(delta[None] * w, cfg.share_dial, rw)
    lam = np.concatenate((lam_head, (delta - lam_head.sum(axis=0))[None]))  # (n, giver rows, sites): the last the rest
    impulse = 0 * push
    np.add.at(impulse, roles.giver, -delta * wa[roles.giver])
    np.add.at(impulse, roles.takers.reshape(-1), (lam * wa[roles.takers]).reshape(-1, a.shape[-1]))
    a1, b1, s1 = step.gear(a, b, tooth, wa + wb, d_out, push + impulse, senses)
    jb, ja, ja1 = (contract(plan, step.valued(b), b), contract(plan, step.valued(a), a), contract(plan, step.valued(a1), a1))
    moved = step.passing(click, a, b, ja, jb) + step.passing(click, a1, a, ja1, ja)
    clicks, k1 = carry(moved, key, k)
    reads = {"delta": delta, "lam": lam, "a0": a0, "s0": s0, "impulse": impulse}
    return State(a1, b1, s1, kept, k1), (r31, rw1), clicks, reads


def mirror4(layout: Any, cfg: Third, s: State, x: tuple[Z, Z]) -> tuple[State, tuple[Z, Z]]:
    """The state mirrored as built; the third click's teeth flipped in their dials (the drive's law, even rows)."""
    r3, rw = x
    return step.mirror(layout, s), (flip(r3, cfg.dial), flip(rw, cfg.share_dial))


def untick4(layout: Any, roles: Any, cfg: Third, s: State, x: tuple[Z, Z]) -> tuple[State, tuple[Z, Z], Z, dict[str, Z]]:
    """The round run back: the same act on the mirrored state, mirrored."""
    m, mx = mirror4(layout, cfg, s, x)
    out, ox, clicks, reads = act4(layout, roles, cfg, m, mx)
    back, bx = mirror4(layout, cfg, out, ox)
    return back, bx, clicks, reads
