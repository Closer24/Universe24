"""The Node-clock's step: a gear's tick and its rate dial's beat, each with its run back."""

from tensor24.algebra.carry import Z, carry, choose, home, uncarry
from tensor24.engine.mesh import due, pull
from tensor24.engine.state import Layout, Out, State


def gear(a: Z, b: Z, r: Z, go: Z, w: Z, wp: Z, push: Z) -> tuple[Z, Z, Z]:
    """A gear's tick: p = W (a - b) + (r - home), and a+ = a + q with (q, r+) the carry of p + push at W+."""
    p = w * (a - b) + (r - home(w, go))
    q, kept = carry(p + push, wp, home(wp, go))
    return a + q, a, kept


def ungear(a: Z, b: Z, r: Z, go: Z, w: Z, wp: Z, push: Z) -> tuple[Z, Z, Z]:
    """The gear's tick run back from its now (a, b, r): the stride read at W+, then carried at W."""
    q, kept = carry(wp * (a - b) + (r - home(wp, go)) - push, w, home(w, go))
    return b, b - q, kept


def beat(ph: Z, rate: Z, gamma: Z, fire: Z) -> tuple[Z, Z]:
    """The rate dial's beat where fire is 1: (k, ph') = carry(ph, Gamma, rate), k = 0 being no tick this tick."""
    k, turned = carry(ph, gamma, rate)
    return fire * k, choose(fire, turned, ph)


def unbeat(k: Z, ph: Z, rate: Z, gamma: Z, fire: Z) -> Z:
    """The beat run back: k Gamma + ph' - rate where it fired, ph' where it did not."""
    return choose(fire, uncarry(k, gamma, ph) - rate, ph)


def times(k: Z, c: Z, tb: Z, tn: Z) -> tuple[Z, Z]:
    """The slots' local times after a tick of k at the count c: the before slot takes the now's, the now c."""
    return choose(k, tn, tb), choose(k, c, tn)


def tick(layout: Layout, s: State, allowed: Z) -> tuple[State, Out]:
    """One round where the runner allows: the due beat turns the dial, and where it ticks the gears step."""
    nb, _, w, rate, gamma = layout
    a, b, r, go, ph, c, tb, tn = s
    fire = due(c, nb) * allowed
    k, dial = beat(ph, rate, gamma, fire)
    a1, b1, r1 = gear(a, b, r, go, w, w, pull(layout, s))
    count = c + fire
    tb1, tn1 = times(k, count, tb, tn)
    now = State(choose(k, a1, a), choose(k, b1, b), choose(k, r1, r), go, dial, count, tb1, tn1)
    return now, Out(fire, k, tb)


def untick(layout: Layout, s: State, o: Out) -> State:
    """The round run back from its out: the pull as it was read, the gears, the times, the count and the dial."""
    _, _, w, rate, gamma = layout
    a, b, r, go, ph, c, tb, tn = s
    fire, k, before = o
    count = c - fire
    read = pull(layout, State(choose(k, b, a), b, r, go, ph, count, tb, tn))
    a0, b0, r0 = ungear(a, b, r, go, w, w, read)
    dial = unbeat(k, ph, rate, gamma, fire)
    return State(
        choose(k, a0, a),
        choose(k, b0, b),
        choose(k, r0, r),
        go,
        dial,
        count,
        choose(k, before, tb),
        choose(k, tb, tn),
    )
