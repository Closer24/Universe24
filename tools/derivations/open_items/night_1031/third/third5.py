"""THIRD5's test act: THIRD4's act (third4.act4, frozen) with WHO read from the takers' present squares by the right
triangle, a_i^2 / SUM a^2: takers 1 .. n - 1 carry delta s_i at the dial L = SUM_j s_j with a tooth of their own kept,
the last takes the rest. Everything else is third4.act4's. The mirror flips the share teeth at the dial read where the
mirrored round will read it (the now slot of the mirrored state, the before slot of the state mirrored). With "chosen"
the share is THIRD4's CHOSEN form, so the two stand side by side. Whole numbers; Rule3's carry; paths by joinpath."""
import sys
from pathlib import Path
from typing import Any
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("c5", "src")))
import numpy as np  # noqa: E402
from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import contract  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from third4 import Third  # noqa: E402

TRIANGLE_DIAL = [0]  # the triangle's fixed share dial, CHOSEN in world/third.json ("chosen5"), set by the probe at load


def act5(layout: Any, roles: Any, cfg: Third, s: State, x: Any, who: str = "squares", variant: str = "") -> Any:
    _, _, _, _, gearing, plan, clock, _, click, _, _ = layout
    a, b, tooth, rd, k = s
    r3, rw = x
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
    delta, r31 = carry(cfg.strength * a[roles.giver], cfg.dial, r3)
    held = a[roles.takers]
    sizes = (held * held).sum(axis=1)  # (n, sites): the takers' present squares, the legs squared
    total = sizes.sum(axis=0)  # (sites,): the whole squared, the dial L
    if who == "draw":
        # a measurement form, not lawful (THIRD5 1.7): the triangle's sources picked by G5's draw from the state, the draw
        # entering each taker's carry as its remainder, no tooth kept; the pointer the norm of the Node-clock's own teeth in
        # and out, its digits at the dial one per taker
        cin, cout = senses * tooth + 1, senses * s0 + 1
        pointer = (cin * cin + cout * cout).sum(axis=0)
        digits = []
        for _ in range(roles.takers.shape[0]):
            pointer, d = carry(pointer, TRIANGLE_DIAL[0], 0)
            digits.append(d)
        draw = np.stack(digits)[:, None, :]
        lam, _ = carry(cfg.strength * a[roles.giver][None] * sizes[:, None, :], TRIANGLE_DIAL[0], draw)
        rw1 = rw
        delta, r31 = lam.sum(axis=0), r3
        outside = 0
    elif who == "triangle":
        # the right triangle in the drive's form: every taker's tooth carries the giver's count times its own present
        # square at the fixed dial, its tooth kept; the giver gives what the takers carried (no rest, no taker special)
        lam, rw1 = carry(cfg.strength * a[roles.giver][None] * sizes[:, None, :], TRIANGLE_DIAL[0], rw)
        delta, r31 = lam.sum(axis=0), r3
        outside = int(np.any((rw < 0) | (rw >= TRIANGLE_DIAL[0])))
    elif who == "squares":
        lam_head, rw1 = carry(delta[None] * sizes[:-1, None, :], total[None, None, :], rw)
        outside = int(np.any((rw < 0) | (rw >= total[None, None, :])))  # a kept tooth outside this round's dial
    else:
        w = np.array(cfg.weights, dtype=object)[:, None, None]
        lam_head, rw1 = carry(delta[None] * w, cfg.share_dial, rw)
        outside = int(np.any((rw < 0) | (rw >= cfg.share_dial)))
    if who not in ("triangle", "draw"):
        lam = np.concatenate((lam_head, (delta - lam_head.sum(axis=0))[None]))
    give = {"no_give": 0}.get(variant, 1)
    take = {"no_take": 0, "double": 2}.get(variant, 1)
    impulse = 0 * push
    np.add.at(impulse, roles.giver, give * -delta * wa[roles.giver])
    np.add.at(impulse, roles.takers.reshape(-1), (take * lam * wa[roles.takers]).reshape(-1, a.shape[-1]))
    pushed, before = push + impulse, b
    if variant == "shear":  # the push written into the stored before slot before the passing reads it
        dq, _ = carry(impulse, wa, 0)
        pushed, before = push, b - dq
    if variant == "gear_lost":
        gonly = 0 * impulse
        np.add.at(gonly, roles.giver, impulse[roles.giver])
        pushed = push + gonly
    if variant == "unapplied":
        pushed = push
    a1, b1, s1 = step.gear(a, before, tooth, wa + wb, d_out, pushed, senses)
    jb, ja, ja1 = (contract(plan, step.valued(before), before), contract(plan, step.valued(a), a), contract(plan, step.valued(a1), a1))
    moved = step.passing(click, a, before, ja, jb) + step.passing(click, a1, a, ja1, ja)
    clicks, k1 = carry(moved, key, k)
    return State(a1, b1, s1, kept, k1), (r31, rw1), clicks, {"delta": delta, "lam": lam, "a0": a0, "sizes": sizes, "outside": outside}


def mirror5(layout: Any, roles: Any, cfg: Third, s: State, x: Any, who: str = "squares") -> Any:
    r3, rw = x
    if who == "squares":
        held = s.b[roles.takers]  # the mirrored state's now slot is this state's before slot
        dial = (held * held).sum(axis=1).sum(axis=0)[None, None, :]
    elif who in ("triangle", "draw"):
        dial = TRIANGLE_DIAL[0]
    else:
        dial = cfg.share_dial
    return step.mirror(layout, s), (flip(r3, cfg.dial), flip(rw, dial))


def untick5(layout: Any, roles: Any, cfg: Third, s: State, x: Any, who: str = "squares", variant: str = "") -> Any:
    m, mx = mirror5(layout, roles, cfg, s, x, who)
    out, ox, clicks, reads = act5(layout, roles, cfg, m, mx, who, variant)
    back, bx = mirror5(layout, roles, cfg, out, ox, who)
    return back, bx, clicks, reads
