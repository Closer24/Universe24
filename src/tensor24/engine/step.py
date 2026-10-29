"""The Node-clock's step: every gear's impulse, drive and carry, and the rate dial's beat, each with its run back."""

import numpy as np

from tensor24.algebra.carry import Z, carry, choose, home, uncarry
from tensor24.engine.contract import contract
from tensor24.engine.mesh import due, pull, seen
from tensor24.engine.state import Gearing, Layout, Out, State


def gear(a: Z, b: Z, r: Z, go: Z, w: Z, wp: Z, push: Z) -> tuple[Z, Z, Z]:
    """A gear's tick: p = W (a - b) + (r - home), and a+ = a + q with (q, r+) the carry of p + push at W+."""
    p = w * (a - b) + (r - home(w, go))
    q, kept = carry(p + push, wp, home(wp, go))
    return a + q, a, kept


def ungear(a: Z, b: Z, r: Z, go: Z, w: Z, wp: Z, push: Z) -> tuple[Z, Z, Z]:
    """The gear's tick run back from its now (a, b, r): the stride read at W+, then carried at W."""
    q, kept = carry(wp * (a - b) + (r - home(wp, go)) - push, w, home(w, go))
    return b, b - q, kept


def drive(j: Z, teeth: Z, rd: Z) -> tuple[Z, Z]:
    """The drive: (q, r_d+), the carry of the source J at the drive's teeth T_d; on the force's path, T_d = 1, q is J."""
    return carry(j, teeth, rd)


def undrive(j: Z, teeth: Z, rd: Z) -> tuple[Z, Z]:
    """The drive run back from r_d+: (q, r_d) with J + r_d = q T_d + r_d+, r_d the remainder of r_d+ - J at T_d."""
    back, kept = carry(rd - j, teeth, 0)
    return -back, kept


def sources(layout: Layout, s: State) -> tuple[Z, Z]:
    """Every gear's force, its pull less its spring D a, and its source J: the plan on the value, the differences, the force."""
    nb, _, _, gearing, plan, _, _ = layout
    _, _, _, spring, _, _ = gearing
    a, _, _, _, _, _, _, _ = s
    force = pull(layout, s) - spring * a
    near = seen(s, nb)
    rows, _, sites = near.shape
    ends = near.reshape(rows, -1, 1 + 1, sites)
    gradient = np.moveaxis(ends[:, :, 0] - ends[:, :, 1], 1, 0)
    readings = np.concatenate((np.expand_dims(a, 0), gradient, np.expand_dims(force, 0)))
    return force, contract(plan, readings.reshape(-1, sites), a)


def driven(gearing: Gearing, force: Z, q: Z) -> Z:
    """The push on every gear, s F + K with the kick K = T_k s q: the force, and every source through the drive."""
    _, _, stretch, _, kick, _ = gearing
    return stretch * (force + kick * q)


def beat(ph: Z, rate: Z, gamma: Z, fire: Z) -> tuple[Z, Z]:
    """The rate dial's beat where fire is 1: (k, ph') = carry(ph, Gamma, rate), k = 0 being no tick this tick."""
    k, turned = carry(ph, gamma, rate)
    return fire * k, choose(fire, turned, ph)


def unbeat(k: Z, ph: Z, rate: Z, gamma: Z, fire: Z) -> Z:
    """The beat run back: k Gamma + ph' - rate where it fired, ph' where it did not."""
    return choose(fire, uncarry(k, gamma, ph) - rate, ph)


def tick(layout: Layout, s: State, allowed: Z) -> tuple[State, Out]:
    """One round where the runner allows: the due beat turns the dial; where it ticks, each gear steps on its sources."""
    nb, _, _, gearing, _, rate, gamma = layout
    w, wp, _, _, _, teeth = gearing
    a, b, r, go, rd, ph, c, tn = s
    fire = due(c, nb) * allowed
    k, dial = beat(ph, rate, gamma, fire)
    force, j = sources(layout, s)
    q, kept = drive(j, teeth, rd)
    a1, b1, r1 = gear(a, b, r, go, w, wp, driven(gearing, force, q))
    count = c + fire
    now = State(
        choose(k, a1, a),
        choose(k, b1, b),
        choose(k, r1, r),
        go,
        choose(k, kept, rd),
        dial,
        count,
        choose(k, count, tn),
    )
    return now, Out(fire, k, tn)


def untick(layout: Layout, s: State, o: Out) -> State:
    """The round run back from its out: the sources as they were read, the drive, the gears, the count, the dial, the time."""
    _, _, _, gearing, _, rate, gamma = layout
    w, wp, _, _, _, teeth = gearing
    a, b, r, go, rd, ph, c, tn = s
    fire, k, before = o
    count = c - fire
    force, j = sources(layout, State(choose(k, b, a), b, r, go, rd, ph, count, tn))
    q, kept = undrive(j, teeth, rd)
    a0, b0, r0 = ungear(a, b, r, go, w, wp, driven(gearing, force, q))
    dial = unbeat(k, ph, rate, gamma, fire)
    return State(
        choose(k, a0, a),
        choose(k, b0, b),
        choose(k, r0, r),
        go,
        choose(k, kept, rd),
        dial,
        count,
        before,
    )
