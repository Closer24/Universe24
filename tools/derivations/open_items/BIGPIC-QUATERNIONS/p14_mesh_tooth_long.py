"""p14: the escapement with the Mesh's own tooth on the escapement readers' lays (Big Pic, 2026-10-30; the Boss's
6532753216 item 5 and 6532927029 item 1).

Both readers refused the escapement for a runaway wherever neighbouring Node-clocks release on different rounds: a
Mesh's pull reaches each end only at that end's own release, a one-ended kick. The mend asked: a Mesh's impulse lands on
both its ends at one event. Here each Mesh has its own tooth at the dial L(i) + L(i+1), pushed by L0 + L0, whose release
pays the Mesh's pull into both ends at once; each Node-clock's own tooth releases its step (the momentum split at the
rest dial). Every event is a shear: a step at one Node-clock, or a Mesh's kick into both its ends from the counts as
they stand. On a ring of 64 for 20,000 rounds, read by the bit length of the largest count (30 at the lay), the books
(the sum of the momenta) at every round, and the run back of all 20,000 rounds:
  (a) a uniform clock with the teeth born at scattered phases, at N = 4/5 and at N = 10/11, beside aligned births and
      beside the escapement without the Mesh's tooth;
  (b) the contrast sweep: half the ring at L0 (1 + e), e = 1, 1/10, 1/100;
  (c) a smooth well 10 per cent deep;
  (d) the lever for clocks faster than the rest: the rest releasing every other round, a region at 2/3.
The finding: the tooth keeps the books and the run back on every lay and closes the one-ended kick, but the releases'
rhythm still pumps the waves wherever neighbouring teeth release apart at a slow rhythm. Whole numbers only; every
division is Rule3's carry.
"""

from qlib import ONE, TWO, carry, report

lines = []
SITES = 64
ROUNDS = 20000
WINDOW = 1000
A1, B1 = 32000000, 2000000  # the rest dial and grip: a quarter Mesh a round at full release
HEIGHT = 1000000000


def ring(i):
    return carry(i, SITES, 0)[1]


def pascal(m):
    row = [ONE]
    for _ in range(m):
        row = [a + b for a, b in zip([0] + row, row + [0], strict=True)]
    return row


ROW = pascal(24)
LAY = [0] * SITES
for k, v in enumerate(ROW):
    LAY[ring(20 + k)] = carry(HEIGHT * v, ROW[12], 0)[0]


def tooth_run(counts, push, births, rounds, mesh_tooth=True, back=False):
    """counts: each Node-clock's L (still); push: L0 + L0; births: (tau, mu) at their phases. With mesh_tooth the
    Mesh's own tooth releases its pull into both ends; without it each end takes the pull at its own release."""
    d = TWO * A1
    a = list(LAY)
    mom = [0] * SITES
    tau, mu = list(births[0]), list(births[ONE])
    start = (list(a), list(mom), list(tau), list(mu))
    books, first, last = set(), 0, 0
    for t in range(rounds):
        pulls = [TWO * TWO * B1 * (a[ring(i + ONE)] - a[i]) for i in range(SITES)]
        if mesh_tooth:
            for i in range(SITES):
                go, mu[i] = carry(push, counts[i] + counts[ring(i + ONE)], mu[i])
                mom[i] += go * pulls[i]
                mom[ring(i + ONE)] -= go * pulls[i]
            for i in range(SITES):
                go, tau[i] = carry(push, counts[i] + counts[i], tau[i])
                v, _ = carry(mom[i] + d, TWO * d, 0)
                a[i] += go * v
        else:
            steps = []
            for i in range(SITES):
                go, tau[i] = carry(push, counts[i] + counts[i], tau[i])
                steps.append(go)
            for i in range(SITES):
                mom[i] += steps[i] * (pulls[i] - pulls[ring(i - ONE)])
            for i in range(SITES):
                v, _ = carry(mom[i] + d, TWO * d, 0)
                a[i] += steps[i] * v
        books.add(sum(mom))
        top = max(abs(x) for x in a)
        if t < WINDOW:
            first = max(first, top)
        if t >= rounds - WINDOW:
            last = max(last, top)
    if not back:
        return books, first, last, None
    for _ in range(rounds):
        for i in range(SITES):
            dial = counts[i] + counts[i]
            go, flipped = carry(push, dial, dial - ONE - tau[i])
            tau[i] = dial - ONE - flipped
            v, _ = carry(mom[i] + d, TWO * d, 0)
            a[i] -= go * v
        pulls = [TWO * TWO * B1 * (a[ring(i + ONE)] - a[i]) for i in range(SITES)]
        for i in range(SITES):
            dial = counts[i] + counts[ring(i + ONE)]
            go, flipped = carry(push, dial, dial - ONE - mu[i])
            mu[i] = dial - ONE - flipped
            mom[i] -= go * pulls[i]
            mom[ring(i + ONE)] += go * pulls[i]
    return books, first, last, (a, mom, tau, mu) == start


def births_scattered(counts):
    taus = [carry(7 * i + 3, counts[i] + counts[i], 0)[1] for i in range(SITES)]
    mus = [carry(3 * i + 1, counts[i] + counts[ring(i + ONE)], 0)[1] for i in range(SITES)]
    return taus, mus


def bits(first, last):
    return first.bit_length(), last.bit_length()


def stands(books, home):
    return len(books) == ONE and home


# (a) a uniform clock, teeth born scattered
deep = [5] * SITES
books, first, last, home = tooth_run(deep, 8, births_scattered(deep), ROUNDS, back=True)
_, plain_first, plain_last, _ = tooth_run(deep, 8, births_scattered(deep), ROUNDS, mesh_tooth=False)
b_tooth, b_plain = bits(first, last), bits(plain_first, plain_last)
report(
    lines,
    f"(a) a uniform clock at N = 4/5, the teeth born at scattered phases: with the Mesh's tooth the largest count holds "
    f"at {b_tooth[0]} to {b_tooth[1]} bits over {ROUNDS} rounds, the books stand and the run back is exact; without it, "
    f"on the same lay, {b_plain[0]} to {b_plain[1]} bits",
    stands(books, home) and b_tooth[1] <= b_tooth[0] + ONE and b_plain[1] > b_plain[0] + 100,
)
fast = [110] * SITES
books, first, last, home = tooth_run(fast, 200, births_scattered(fast), ROUNDS, back=True)
_, al_first, al_last, _ = tooth_run(fast, 200, ([110] * SITES, [110] * SITES), ROUNDS)
b_sc, b_al = bits(first, last), bits(al_first, al_last)
report(
    lines,
    f"(a) a uniform clock at N = 10/11 with the Mesh's tooth: the teeth born scattered, {b_sc[0]} to {b_sc[1]} bits "
    f"(a runaway; the books stand and the run back is exact); the teeth born aligned, {b_al[0]} to {b_al[1]} bits",
    stands(books, home) and b_sc[1] > b_sc[0] + 100 and b_al[1] <= b_al[0] + ONE,
)

# (b) the contrast sweep
for num, den, grows in ((ONE, ONE, False), (ONE, 10, True), (ONE, 100, True)):
    l0 = 100
    deep_l = l0 + carry(l0 * num, den, 0)[0]
    counts = [l0] * 32 + [deep_l] * 32
    books, first, last, home = tooth_run(counts, l0 + l0, births_scattered(counts), ROUNDS, back=True)
    b = bits(first, last)
    report(
        lines,
        f"(b) half the ring at L0 (1 + {num}/{den}) (L {l0} and {deep_l}) with the Mesh's tooth: {b[0]} to {b[1]} bits "
        f"({'a runaway' if grows else 'held'}), the books stand, the run back exact",
        stands(books, home) and ((b[1] > b[0] + 5) if grows else (b[1] <= b[0] + ONE)),
    )

# (c) a smooth well 10 per cent deep
well = [1000] * SITES
for k, v in enumerate(pascal(40)):
    well[ring(12 + k)] += carry(100 * v, pascal(40)[20], 0)[0]
books, first, last, home = tooth_run(well, 2000, births_scattered(well), ROUNDS, back=True)
b = bits(first, last)
report(
    lines,
    f"(c) a smooth well 10 per cent deep (L 1000 to {max(well)}) with the Mesh's tooth: {b[0]} to {b[1]} bits (a "
    "runaway), the books stand, the run back exact",
    stands(books, home) and b[1] > b[0] + 5,
)

# (d) the lever: the rest releases every other round, so a clock may run faster than the rest
lever = [8] * 32 + [6] * 32  # L0 = 4: the rest at N = 1/2, the region at N = 2/3
books, first, last, home = tooth_run(lever, 8, births_scattered(lever), ROUNDS, back=True)
b = bits(first, last)
report(
    lines,
    "(d) the lever: L0 = 4 with the rest clock at L = 8 (one release in two) and half the ring faster than the rest "
    f"(L = 6, N = 2/3): {b[0]} to {b[1]} bits over {ROUNDS} rounds, the books stand, the run back exact",
    stands(books, home),
)
lines.append(
    "   so the Mesh's tooth closes the one-ended kick and keeps the books and the run back on every lay, but where"
)
lines.append(
    "   neighbouring teeth release apart at a slow rhythm (rates near 1) the releases switch the couplings in that"
)
lines.append(
    "   rhythm and pump the waves; aligned releases, and rhythms faster than twice the band's top, hold"
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")
