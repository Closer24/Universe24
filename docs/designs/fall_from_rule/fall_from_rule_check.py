"""A packet falling by the rule alone (ALGEBRA.md 9.98 (7), corrected by the
Boss's record 2132 fix 2; the model owner's question of 2026-09-26, "does the
rule move a body by itself?").

A host check, not a pin. The rule 9.57 (1) (9.91 (2) at equal paces) runs
exactly in 64-bit integers on a chain of N Nodes with the pair [num, den]
at every Node and the Node clock Gamma (the pace p = Gamma - c, c the
content at the Node). The content rises by g per Node along the chain, c =
1000 + g x, so a packet started at x_0 sits in a content gradient with the
potential U = c / (2 Gamma) at its centre.

The prediction (9.98 (7)): the packet's acceleration is a = (num / den) g /
(6 Gamma) times 2 (1 - 2 U)^3 / (1 + (1 - 2 U)^2) Nodes per interval
squared, from the rule's own clock rate and light speed (9.97 (4)); at U =
0 the factor is 1 (Newton's a = c_l^2 dU / dx), at the packet's U = 0.08 it
is 0.695.

The reading: the packet's centroid over its amplitude envelope, (now^2 - 2
now before cos omega + before^2) / sin^2 omega with the local omega (a
GameBoard reading of the host, printed every 250 intervals; the centroid of
now^2 at one instant is biased by the phase gradient across the packet and
is not used), and the acceleration from second differences of the centroid
over windows of 500 intervals. The control row g = 0 must not move. Two
widths show the width's effect: a wider packet reads closer to the line.
Floats appear only in the start's envelope and in the readings; every step
of the rule is an integer step.

Run: python docs/designs/fall_from_rule/fall_from_rule_check.py (about two
seconds on a host). Read on 2026-09-26: the ratios of the read acceleration
to the prediction 0.96 to 0.94 from t = 500 to 2500 at the width 40, 0.99
to 0.97 at the width 80, and 0.00 for the control; the rms width grows from
28 to 93 Nodes (width 40) and from 57 to 71 (width 80) in 3000 intervals.
"""

import numpy as np

GAMMA = 10_000  # the Node clock
NUM, DEN = 800, 809  # the pair at every Node
N = 2600  # the chain's Nodes
A = 1 << 16  # the packet's amplitude
X_0 = 600.0  # the packet's start
x = np.arange(N)


def run(g: int, sigma: float, intervals: int = 3000, every: int = 250) -> tuple[dict, dict]:
    """The rule on the chain with the content c = 1000 + g x; the envelope's
    centroid and rms width every `every` intervals (GameBoard readings)."""
    c = 1000 + g * x
    p = (GAMMA - c).astype(np.int64)
    # the mode's phase pace at each Node (the rule's dispersion at k = 0)
    cos_omega = 1 - (1 - NUM / DEN) * (1 + (p / GAMMA) ** 2) / 2
    sin_omega_squared = 1 - cos_omega**2
    envelope = A * np.exp(-((x - X_0) ** 2) / (2 * sigma**2))
    a_now = np.rint(envelope).astype(np.int64)
    a_before = np.rint(envelope * cos_omega).astype(np.int64)
    remainder = np.zeros(N, dtype=np.int64)
    wall = 6 * DEN * GAMMA * GAMMA
    read = 2 * NUM * p**2
    own = 12 * DEN * GAMMA * GAMMA - 6 * (p**2 + GAMMA * GAMMA) * (DEN - NUM) - 12 * NUM * p**2
    centroids: dict = {}
    widths: dict = {}
    for t in range(intervals + 1):
        if t % every == 0:
            now = a_now.astype(np.float64)
            before = a_before.astype(np.float64)
            density = (now * now - 2 * now * before * cos_omega + before * before) / sin_omega_squared
            centre = float((density * x).sum() / density.sum())
            centroids[t] = centre
            widths[t] = float(np.sqrt((density * (x - centre) ** 2).sum() / density.sum()))
        six = np.roll(a_now, 1) + np.roll(a_now, -1) + 4 * a_now
        total = read * six + own * a_now - wall * a_before + remainder
        a_next = total // wall
        remainder = total - wall * a_next
        a_before, a_now = a_now, a_next
    return centroids, widths


def main() -> None:
    newton = (NUM / DEN) / (6 * GAMMA)
    potential = (1000 + X_0) / (2 * GAMMA)
    factor = 2 * (1 - 2 * potential) ** 3 / (1 + (1 - 2 * potential) ** 2)
    predicted = newton * factor
    print(f"U at the packet {potential:.3f}, factor {factor:.4f}, predicted a (g = 1) {predicted:.4e}")
    rows = (("control g = 0", 0, 40.0), ("g = 1, width 40", 1, 40.0), ("g = 1, width 80", 1, 80.0))
    for label, g, sigma in rows:
        centroids, widths = run(g, sigma)
        print("==", label)
        print(
            "  centroid at t = 0, 1000, 2000, 3000:",
            [round(centroids[t], 2) for t in (0, 1000, 2000, 3000)],
        )
        print(f"  rms width {widths[0]:.1f} -> {widths[3000]:.1f} Nodes")
        for t in (500, 1000, 1500, 2000, 2500):
            acc = (centroids[t + 500] - 2 * centroids[t] + centroids[t - 500]) / 500**2
            print(
                f"  a from second differences at t = {t}: {acc:.3e}  ratio to the prediction {acc / predicted:+.3f}"
            )


if __name__ == "__main__":
    main()
