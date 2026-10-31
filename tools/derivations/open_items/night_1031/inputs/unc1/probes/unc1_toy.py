"""UNC1's toy check of the derivations, exhaustive on small odd dials: the carry's coding of a passing sequence.

Usage: python -I unc1_toy.py <tree>

For each dial K in (3, 5, 7) and N = 4 rounds, every passing sequence P in [-2K, 2K]^N is carried from the birth
(K - 1) div 2 by Rule3's carry (the tree's carry), giving the q-word and the tooth path. Checked, each by count:
  T1  the q-word and the tooth path determine the passing sequence (the carry is a bijection n <-> (q, r') given r);
      and, among the q-words with every |q| <= 1 (inside the enumeration's reach), every tooth path in [0, K)^N stands
      over each: the fiber of a q-word is K^N, so the q-word carries no bit of the tooth (U2).
  T2  over those q-words, the passing sums S_W consistent with one q-word on a window [m, n): exactly the 2K - 1
      values K Q_W - (K - 1) .. K Q_W + (K - 1) for m >= 1, and exactly the K values K Q_W - half .. K Q_W + half
      for m = 0 (U1, attained).
  T3  from the birth, 2 |K Q_n - S_n| <= K - 1 at every round: the count is the passing's nearest whole number of
      quanta, never a tie (K odd).
  T4  two births b, b' (every pair) under one passing sequence: |Q_W - Q'_W| <= 1 on every window (U1e).
Then the CHSH enumeration: the 16 local deterministic strategies (A0, A1, B0, B1 in {-1, 1}),
S = A0 B0 + A0 B1 + A1 B0 - A1 B1, the set of S printed.
Whole numbers only.
"""

import itertools
import sys
from pathlib import Path

TREE = Path(sys.argv[1])
sys.path.insert(0, str(TREE.joinpath("src")))

from tensor24.algebra.carry import carry  # noqa: E402


def coded(ps: tuple[int, ...], k: int, dial: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """The q-word and the tooth path (k_1 .. k_N) of a passing sequence carried from the tooth k at the dial."""
    qs, ks = [], []
    for p in ps:
        q, k = carry(p, dial, k)
        qs.append(q)
        ks.append(k)
    return tuple(qs), tuple(ks)


N = 4
for K in (3, 5, 7):
    half, _ = carry(K - 1, 2, 0)
    span = range(-2 * K, 2 * K + 1)
    seen: dict[tuple[tuple[int, ...], tuple[int, ...]], tuple[int, ...]] = {}
    fiber: dict[tuple[int, ...], set[tuple[int, ...]]] = {}
    sums: dict[tuple[tuple[int, ...], int, int], set[int]] = {}
    clash = nearest_bad = 0
    for ps in itertools.product(span, repeat=N):
        qs, ks = coded(ps, half, K)
        clash += int((qs, ks) in seen and seen[(qs, ks)] != ps)
        seen[(qs, ks)] = ps
        pre = [0]
        for p in ps:
            pre.append(pre[-1] + p)
        cq = [0]
        for q in qs:
            cq.append(cq[-1] + q)
        nearest_bad += sum(1 for n in range(N + 1) if 2 * abs(K * cq[n] - pre[n]) > K - 1)
        if all(abs(q) <= 1 for q in qs):
            fiber.setdefault(qs, set()).add(ks)
            for m in range(N):
                for n in range(m + 1, N + 1):
                    sums.setdefault((qs, m, n), set()).add(pre[n] - pre[m])
    full = sum(1 for paths in fiber.values() if len(paths) == K**N)
    exact_late = exact_birth = windows_late = windows_birth = 0
    for (qs, m, n), ss in sums.items():
        cq = sum(qs[m:n])
        if m:
            windows_late += 1
            exact_late += int(ss == set(range(K * cq - (K - 1), K * cq + K)))
        else:
            windows_birth += 1
            exact_birth += int(ss == set(range(K * cq - half, K * cq + half + 1)))
    print(f"K {K}, N {N}, passings in [-{2 * K}, {2 * K}]: sequences {len(seen)}, two sequences on one (q-word, tooth "
          f"path): {clash}")
    print(f"  T1 q-words with every |q| <= 1: {len(fiber)}; each over all {K**N} tooth paths: {full} of {len(fiber)}")
    print(f"  T2 windows from round 1 on: {windows_late}, sums exactly the 2K - 1 = {2 * K - 1} values: {exact_late}; "
          f"windows from the birth: {windows_birth}, sums exactly the K = {K} values: {exact_birth}")
    print(f"  T3 rounds where 2 |K Q_n - S_n| > K - 1: {nearest_bad}")
    # T4: every pair of births under every passing sequence, every window
    worst = pairs = 0
    for ps in itertools.product(range(-K, K + 1), repeat=N):
        counts = []
        for b in range(K):
            qs, _ = coded(ps, b, K)
            pre = [0]
            for q in qs:
                pre.append(pre[-1] + q)
            counts.append(pre)
        for c1 in counts:
            for c2 in counts:
                pairs += 1
                # every window [m, n) at once: Q_W - Q'_W = d_n - d_m, so the largest |.| is max d - min d
                d = [x - y for x, y in zip(c1, c2, strict=True)]
                worst = max(worst, max(d) - min(d))
    print(f"  T4 births paired under passings in [-{K}, {K}]^{N}: {pairs} pairs; largest |Q_W - Q'_W| = {worst}")

values = set()
for a0, a1, b0, b1 in itertools.product((-1, 1), repeat=4):
    values.add(a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1)
print(f"CHSH: the 16 local deterministic strategies give S in {sorted(values)}")
