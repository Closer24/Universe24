"""A packet falling by the rule alone (ALGEBRA.md 9.98 (7); the model owner's
question of 2026-09-26, "does the rule move a body by itself?").

A host check, not a pin. The rule 9.57 (1) (9.91 (2) at equal paces) runs
exactly in 64-bit integers on a chain of N Nodes with the pair [num, den]
at every Node and the Node clock Gamma (the pace p = Gamma - c, c the
content at the Node). The content rises by g per Node along the chain, c =
1000 + g x, so a packet started at x_0 sits in a content gradient. The
prediction of 9.98 (7): the packet's acceleration is a = (num / den) g / (6
Gamma) Nodes per interval squared, from the rule's long-wave form alone,
with no motion rule.

The reading: the packet's centroid over the square of its level (a
GameBoard reading of the host, printed every 250 intervals), and the
acceleration from second differences of the centroid over windows of 500
intervals; the first window carries the start's transient (a packet born
with the local phase relaxes for about 1000 intervals). The control row g =
0 must not move. The "uniform phase" row starts the packet with one phase
pace for every Node instead of the local one, to show that the start's
phase does not make the motion. Floats appear only in the start's envelope
and in the readings; every step of the rule is an integer step.

Run: python docs/designs/fall_from_rule/fall_from_rule_check.py (about one
second on a host). Read at 7dba902b on 2026-09-26: the ratios of the read
acceleration to the prediction 0.85, 1.16, 1.06 at t = 1500, 2000, 2500
with the local phase, the same three with the uniform phase, and 0.00 for
the control.
"""

import numpy as np

GAMMA = 10_000  # the Node clock
NUM, DEN = 800, 809  # the pair at every Node
N = 2600  # the chain's Nodes
A = 1 << 16  # the packet's amplitude
X_0 = 600.0  # the packet's start
SIGMA = 40.0  # the packet's width in Nodes
x = np.arange(N)


def run(g: int, intervals: int = 3000, uniform_phase: bool = False, every: int = 250) -> dict:
    """The rule on the chain with the content c = 1000 + g x; the centroid every
    `every` intervals (a GameBoard reading)."""
    c = 1000 + g * x
    p = (GAMMA - c).astype(np.int64)
    # the mode's phase pace at each Node (the rule's dispersion at k = 0)
    cos_omega = 1 - (1 - NUM / DEN) * (1 + (p / GAMMA) ** 2) / 2
    if uniform_phase:
        cos_omega = np.full(N, cos_omega[int(X_0)])
    envelope = A * np.exp(-((x - X_0) ** 2) / (2 * SIGMA**2))
    a_now = np.rint(envelope).astype(np.int64)
    a_before = np.rint(envelope * cos_omega).astype(np.int64)
    remainder = np.zeros(N, dtype=np.int64)
    wall = 6 * DEN * GAMMA * GAMMA
    read = 2 * NUM * p**2
    own = 12 * DEN * GAMMA * GAMMA - 6 * (p**2 + GAMMA * GAMMA) * (DEN - NUM) - 12 * NUM * p**2
    centroids = {}
    for t in range(intervals + 1):
        if t % every == 0:
            density = a_now.astype(np.float64) ** 2
            centroids[t] = float((density * x).sum() / density.sum())
        six = np.roll(a_now, 1) + np.roll(a_now, -1) + 4 * a_now
        total = read * six + own * a_now - wall * a_before + remainder
        a_next = total // wall
        remainder = total - wall * a_next
        a_before, a_now = a_now, a_next
    return centroids


def main() -> None:
    predicted = (NUM / DEN) / (6 * GAMMA)
    print("predicted a (g = 1) =", predicted)
    rows = (
        ("control g = 0", 0, False),
        ("g = 1, local phase", 1, False),
        ("g = 1, uniform phase", 1, True),
    )
    for label, g, uniform in rows:
        centroids = run(g, uniform_phase=uniform)
        print("==", label)
        print(
            "  centroid at t = 0, 1000, 2000, 3000:",
            [round(centroids[t], 2) for t in (0, 1000, 2000, 3000)],
        )
        for t in (1000, 1500, 2000, 2500):
            acc = (centroids[t + 500] - 2 * centroids[t] + centroids[t - 500]) / 500**2
            print(
                f"  a from second differences at t = {t}: {acc:.3e}  ratio to the prediction {acc / predicted:+.3f}"
            )


if __name__ == "__main__":
    main()
