"""Row 1c, the order channel of the Bell rows, computed before the run (COMPUTATION; the
issue triage reader's line of 2026-09-24, record 762; DECLARATIONS.md section 2 item 7).

The declared ladder of section 1 item 3: the four cells in the order ++, +-, -+, -- with the
weights (1 + E) / 4, (1 - E) / 4, (1 - E) / 4, (1 + E) / 4 of the total (the settings pair
(0, 3N/8) reversed, as bell_plateau.py declares; E_1 = 46565 / 65773 and E_2 = 46452 / 65773 the
tables' exact correlations), the rungs b_k = (2 N C_k + T) // (2 T) on the wheel [1, N] (u the
birth's ordinal mod N), the cell of u the first k with u < b_k (amplitude.rungs and cell_of). The
COUNTS are the theorem's (the marginals N / 2, S = 181 / 64 at N = 2048); THE ORDER is the
sequence of outcomes over u, and this prints how many births' outcome at one party flips when
the other party's setting changes: the order channel's width. Under any deterministic wheel it
cannot be 0 at every setting while S exceeds 2, since a sequence over u that depended on the
party's own setting alone would be a local deterministic assignment, which Bell's theorem bounds
by 2: the channel is open by the theorem, the counts' no-signalling exact beside it.

    PYTHONPATH=src python docs/designs/detector_law/order_channel_pins.py
"""

from fractions import Fraction as Fr

E1 = Fr(46565, 65773)
E2 = Fr(46452, 65773)


def rungs(n, weights):
    cumulative, out = Fr(0), []
    for w in weights:
        cumulative += w
        out.append(int((2 * n * cumulative + 1) // 2))
    return out


def weights_of(e, reverse):
    same, diff = (1 + e) / 4, (1 - e) / 4
    return [diff, same, same, diff] if reverse else [same, diff, diff, same]


def cells(n, e, reverse):
    b = rungs(n, weights_of(e, reverse))
    out = []
    for u in range(n):
        for k, bk in enumerate(b):
            if u < bk:
                out.append(k)
                break
    return out


# the four settings pairs: (a, b) = (0, N/8): E1; (0, 3N/8): E1 reversed; (N/4, N/8): E2; (N/4, 3N/8): E2
def table(n):
    return {
        (0, 1): cells(n, E1, False),
        (0, 3): cells(n, E1, True),
        (1, 1): cells(n, E2, False),
        (1, 3): cells(n, E2, False),
    }


def o_a(k):
    return +1 if k in (0, 1) else -1


def o_b(k):
    return +1 if k in (0, 2) else -1


for n in (64, 256, 2048):
    t = table(n)
    # A's sequence at a = 0: does it depend on b?  compare (0, N/8) vs (0, 3N/8)
    flip_a0 = sum(o_a(x) != o_a(y) for x, y in zip(t[(0, 1)], t[(0, 3)], strict=True))
    flip_a1 = sum(o_a(x) != o_a(y) for x, y in zip(t[(1, 1)], t[(1, 3)], strict=True))
    # B's sequence at b = N/8: compare a = 0 vs a = N/4; at b = 3N/8 likewise
    flip_b1 = sum(o_b(x) != o_b(y) for x, y in zip(t[(0, 1)], t[(1, 1)], strict=True))
    flip_b3 = sum(o_b(x) != o_b(y) for x, y in zip(t[(0, 3)], t[(1, 3)], strict=True))
    marg = {k: (sum(o_a(c) > 0 for c in v), sum(o_b(c) > 0 for c in v)) for k, v in t.items()}
    corr = {k: Fr(sum(o_a(c) * o_b(c) for c in v), n) for k, v in t.items()}
    s = corr[(0, 1)] - corr[(0, 3)] + corr[(1, 1)] + corr[(1, 3)]
    print(
        f"N = {n}: the marginals (+ counts of A, B) per settings pair {marg}; S = {s} = {float(s):.6f}"
    )
    print(
        f"   THE ORDER CHANNEL: A's outcome flips with B's setting on {flip_a0} of {n} births at a = 0 and {flip_a1} at a = N/4;"
        f" B's flips with A's setting on {flip_b1} of {n} at b = N/8 and {flip_b3} at b = 3N/8"
        f" ({flip_a0 / n:.4f}, {flip_a1 / n:.4f}, {flip_b1 / n:.4f}, {flip_b3 / n:.4f} of the births)"
    )
