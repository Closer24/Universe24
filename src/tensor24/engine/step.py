"""The Node-clock's step: every gear's impulse, drive and carry, the time gear first, and the rate dial's beat, each run back."""

import numpy as np

from tensor24.algebra.carry import Z, carry, choose, home, nonneg, uncarry
from tensor24.engine.contract import contract
from tensor24.engine.mesh import due, pull, seen
from tensor24.engine.state import Gearing, Layout, Out, Ruler, State


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
    nb, _, _, gearing, plan, _, _, _ = layout
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


def reading(count: Z, last: Z) -> Z:
    """A count read on the ruler: below 0 at 0, no clock running faster than the full rate (the owner's word of 2026-10-27, 18:5x UTC), past the last count at the last, the clock's last rate; each end one whether."""
    held = count * nonneg(count)
    return choose(nonneg(last - held), held, last)


def at(table: Z, count: Z, last: Z) -> Z:
    """The ruler's entry at every Node-clock's count: a gather, the count read on the ruler."""
    return table[reading(count, last).astype(np.intp)]


def ruled(gearing: Gearing, ruler: Ruler, b: Z, a: Z, after: Z) -> Gearing:
    """The round's gearing at the time gear's before, now and after counts: a reading row's W = Z_b + Z_n, its W+ = Z_n + Z_+ and its spring its factor times Y_n^2, so each tick's W is the last tick's W+; every other row's as laid."""
    w, wp, stretch, spring, kick, drive = gearing
    row, last, teeth, square, reads, factor = ruler
    now = at(teeth, a[row], last)
    return Gearing(
        choose(reads, at(teeth, b[row], last) + now, w),
        choose(reads, now + at(teeth, after[row], last), wp),
        stretch,
        choose(reads, factor * at(square, a[row], last), spring),
        kick,
        drive,
    )


def tick(layout: Layout, s: State, allowed: Z) -> tuple[State, Out]:
    """One round where the runner allows: the due beat turns the dial; where it ticks, each gear steps on its sources, the time gear first, then every gear whose W+ its count after reads."""
    nb, meshes, grip, gearing, plan, rate, gamma, ruler = layout
    a, b, r, go, rd, ph, c, tn = s
    fire = due(c, nb) * allowed
    k, dial = beat(ph, rate, gamma, fire)
    laid = ruled(gearing, ruler, b, a, a)
    w, wp, _, _, _, teeth = laid
    force, j = sources(Layout(nb, meshes, grip, laid, plan, rate, gamma, ruler), s)
    q, kept = drive(j, teeth, rd)
    push = driven(laid, force, q)
    first, _, _ = gear(a, b, r, go, w, wp, push)
    w, wp, _, _, _, _ = ruled(gearing, ruler, b, a, first)
    a1, b1, r1 = gear(a, b, r, go, w, wp, push)
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
    """The round run back from its out: the sources as they were read, the drive, the time gear, then the gears that read its counts, the count, the dial, the time."""
    nb, meshes, grip, gearing, plan, rate, gamma, ruler = layout
    a, b, r, go, rd, ph, c, tn = s
    fire, k, before = o
    count = c - fire
    start = choose(k, b, a)
    laid = ruled(gearing, ruler, start, start, a)
    w, wp, _, _, _, teeth = laid
    force, j = sources(
        Layout(nb, meshes, grip, laid, plan, rate, gamma, ruler),
        State(start, b, r, go, rd, ph, count, tn),
    )
    q, kept = undrive(j, teeth, rd)
    push = driven(laid, force, q)
    _, first, _ = ungear(a, b, r, go, w, wp, push)
    w, wp, _, _, _, _ = ruled(gearing, ruler, first, start, a)
    a0, b0, r0 = ungear(a, b, r, go, w, wp, push)
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
