"""Toy: the local tick as the light cone's carry (Animate; the owner's word of 2026-10-28, 15:2x UTC: "understand at the
level of the clocks where the problem is in each, whether it is one law or several, solve it in the clocks, then in the
algebra, and do a small simulation").

A ring of clocks, each a hand of two slots (before, now) at its own times (tau - d, tau), d its own tick, stepped by the
one formula
    now+ = 2 now - before + c d^2 (left + right - 2 now),
c the Mesh's coupling (the rate squared, in the full rate's units), exact in rationals. One full-rate tick (d = 1)
crosses one Mesh at c = 1, the light cone. A compressed patch asks for c = 27/25 there.

Every clock reads its neighbours where they stand at its own reading moment (David's correction of line 557): the
neighbour's now if it stands at that time, its before if it is one of its ticks ahead, the point between its two slots if
the moment falls inside its tick. The events run in the order of their start times, so the reads are the same in any
order of the clocks at one time. Each event is a bijection of its own two slots given its neighbours' reads, so the
events undone in the reverse order return the start exactly.

Four runs of one pulse moving right:
  global    one tick for all, c = 27/25 in the patch (F2's lower side struck);
  clamped   one tick for all, c read at 1 in the patch (F2's lower side, the clamp);
  local     the patch's clocks tick at d = 1/2, twice per great tick, the others at d = 1 (a clock's time is the carry
            of its own dial: its dial advances by its rate, and each whole turn is a tick);
  fine      every clock at d = 1/2 (the reference).
Read: the largest |now| over the run (bounded, or grown past 10^6), the tick at which the front passes a clock beyond
the patch, and the rewind.
"""

from fractions import Fraction as F

N, PATCH, STEPS = 60, range(20, 40), 120
C_PATCH, PROBE = F(27, 25), 47


class Clock:
    __slots__ = ("before", "now", "tau", "d", "c")

    def __init__(self, before, now, d, c):
        self.before, self.now, self.tau, self.d, self.c = F(before), F(now), F(0), F(d), F(c)

    def at(self, s):
        """The clock's reading at the moment s, between its two slots (s in [tau - d, tau])."""
        if s == self.tau:
            return self.now
        lo = self.tau - self.d
        assert lo <= s <= self.tau, (s, lo, self.tau)
        return self.before + (self.now - self.before) * (s - lo) / self.d


def board(mode):
    before = {5: 1, 6: 2, 7: 1}
    now = {6: 1, 7: 2, 8: 1}
    clocks = []
    for i in range(N):
        inside = i in PATCH
        c = (C_PATCH if mode == "global" else F(1)) if inside else F(1)
        if mode == "local" and inside or mode == "fine":
            c = C_PATCH if inside else F(1)
            d = F(1, 2)
        else:
            d = F(1)
        clocks.append(Clock(before.get(i, 0), now.get(i, 0), d, c))
    if any(k.d != 1 for k in clocks):
        # a clock of tick 1/2 starts with its before at -1/2: the pulse read between its slots at -1 and 0
        for i, k in enumerate(clocks):
            if k.d != 1:
                k.before = (F(before.get(i, 0)) + F(now.get(i, 0))) / 2
    return clocks


def event(clocks, i, going):
    k = clocks[i]
    if going == 1:
        s = k.tau
        lap = clocks[(i - 1) % N].at(s) + clocks[(i + 1) % N].at(s) - 2 * k.now
        k.before, k.now, k.tau = k.now, 2 * k.now - k.before + k.c * k.d * k.d * lap, k.tau + k.d
    else:
        s = k.tau - k.d
        lap = clocks[(i - 1) % N].at(s) + clocks[(i + 1) % N].at(s) - 2 * k.before
        k.now, k.before, k.tau = k.before, 2 * k.before - k.now + k.c * k.d * k.d * lap, k.tau - k.d


def run(mode):
    clocks = board(mode)
    start = [(k.before, k.now, k.tau) for k in clocks]
    log, largest, arrival, last = [], F(0), None, 0
    for t in range(1, STEPS + 1):
        # every event whose start time is below t, in the order of its start time, then of its clock
        while True:
            due = [(k.tau, i) for i, k in enumerate(clocks) if k.tau < t]
            if not due:
                break
            _s, i = min(due)
            event(clocks, i, 1)
            log.append(i)
        last = t
        largest = max(largest, max(abs(k.now) for k in clocks))
        if arrival is None and abs(clocks[PROBE].now) >= F(1, 2):
            arrival = t
        if largest > 10**6:
            break
    rewound = None
    if largest <= 10**6:
        for i in reversed(log):
            event(clocks, i, -1)
        rewound = [(k.before, k.now, k.tau) for k in clocks] == start
    return largest, arrival, last, rewound, len(log)


def main():
    print(
        f"a ring of {N} clocks, the patch {PATCH.start}..{PATCH.stop - 1} at c = {C_PATCH} (outside c = 1), "
        f"{STEPS} great ticks; the probe clock {PROBE}"
    )
    for mode in ("global", "clamped", "local", "fine"):
        largest, arrival, last, rewound, n = run(mode)
        grown = "grows past 10^6" if largest > 10**6 else f"largest |now| {float(largest):.4f}"
        print(
            f"  {mode:8s}: {grown} (to tick {last}); the front at the probe at tick {arrival}; "
            f"{n} events; the rewind exact: {rewound}"
        )


if __name__ == "__main__":
    main()
