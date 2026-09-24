"""The sequential statistic of B's outcomes under per-trial settings (COMPUTATION, no run,
no pin moved; the chief physicist, 2026-09-24, on Reviewer 3's line of 06:50Z on the Opus
referee's finding 4; ORDER_CHANNEL_ATTACKS.md item 21).

At a fixed setting b, B's outcome at a birth of residue u is [u in S_a], the set S_a of
size W / 2 depending on A's setting a. With the residues in a uniformly random order (the
seed-set permutation of item 8, without replacement), two consecutive births carry two
DISTINCT residues, so at a held setting a the probability that B's consecutive outcomes
agree is (W / 2 - 1) / (W - 1), below 1 / 2; when A switches a to a' between the two births
it is (W / 2 - 2 m / W) / (W - 1) with m = |S_a and S_a'|, so the difference is E / (W - 1),
E = (W - 2 m) / W the flip fraction of the pair (a, a') at that b (the finite-N correlation,
order_channel_pins.py). B's sequential statistic therefore carries A's SWITCHING pattern
(not a's value) at order 1 / W: the model's own prediction, falsifiable, absent in nature's
quantum mechanics. The marginal (B's count) is blind to a: no-signalling in distribution
(hypergeometric with mean n / 2 for every a). A Monte Carlo over seeds checks the formula."""

from order_channel_hidden_pins import b_lists, permutation


def sets(n):
    lists = b_lists(n)
    return {a: {u for u, o in enumerate(lists[a]) if o > 0} for a in (0, 1)}


def exact(n):
    s = sets(n)
    m = len(s[0] & s[1])
    flips = n - 2 * m
    e = flips / n
    p_fixed = (n / 2 - 1) / (n - 1)
    p_switch = (n / 2 - 2 * m / n) / (n - 1)
    return m, flips, e, p_fixed, p_switch, p_switch - p_fixed


def monte_carlo(n, seeds, switch_every):
    """B's consecutive-pair agreement over `seeds` permutations, A's setting held for
    `switch_every` births then switched (0, 1, 0, ...), the held pairs and the switched
    pairs counted apart."""
    s = sets(n)
    held = [0, 0]
    switched = [0, 0]
    for seed in range(1, seeds + 1):
        order = permutation(n, seed * 0x9E3779B97F4A7C15 + 17)
        a_of = [(t // switch_every) % 2 for t in range(n)]
        for t in range(n - 1):
            b0 = order[t] in s[a_of[t]]
            b1 = order[t + 1] in s[a_of[t + 1]]
            bucket = held if a_of[t] == a_of[t + 1] else switched
            bucket[0] += b0 == b1
            bucket[1] += 1
    return held[0] / held[1], switched[0] / switched[1], held[1], switched[1]


if __name__ == "__main__":
    print("(a) EXACT, b = 3 N / 8, the pair (a, a') = (0, N / 4): m = |S_a and S_a'|, the flips,")
    print("    E, P(B_t = B_t+1) held, switched, the difference E / (W - 1), pairs for one sigma")
    for n in (64, 256, 2048):
        m, flips, e, pf, ps, d = exact(n)
        print(
            f"    W = {n:5d}: m = {m:4d}, flips = {flips:4d}, E = {e:.4f}, held {pf:.6f}, "
            f"switched {ps:.6f}, difference {d:.3e} = E / (W - 1), pairs 1 / (4 d^2) = {1 / (4 * d * d):.2e}"
        )
    print("(b) MONTE CARLO at W = 64 over 400 seeds, A switching every 8 births:")
    pf, ps, nh, ns = monte_carlo(64, 400, 8)
    m, flips, e, ef, es, d = exact(64)
    print(
        f"    held {pf:.5f} over {nh} pairs (exact {ef:.5f}); switched {ps:.5f} over {ns} pairs (exact {es:.5f})"
    )
    print("(c) at b = N / 8 the pair has no flips (E = 0): no difference, no signature.")
