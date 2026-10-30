"""The split click's draw number on the node as built, read on the act's own digits (decision 29: d = (c + V) mod L)."""

# The world: one light train (A1, two parts) on a board of 6 by 6 by 6, the example universe's teeth W and grip, laid
# at random and run on the act (engine/step.py) for 450 rounds, read from round 50. V is the sum over a Node-clock and
# its six neighbours of the A1 rows' fine teeth in units of the row's pitch, the gcd of W and the grip. The node holds
# no round and no time (TENSOR24_NODE.md section 0), so it has no dial c: the draw reads V alone, d = V mod L. Beside
# it, the same sum read on the rows' now counts in place of their fine teeth.

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tests import frame  # noqa: E402

W = 90977140554674334000000  # the example universe's teeth at rest (Decoder4D2Clicks3D, the head)
GRIP = W // 6  # its grip, den Gamma^2: W = 6 grip
SHAPE = (6, 6, 6)
ROUNDS, FROM = 450, 50
SIZES = (2, 3, 10, 70, 97, 1000, 16384, 1048583)  # totals L of the parts' sizes


def main() -> None:
    nb = frame.board(SHAPE)
    n = nb.shape[1]
    y = frame.plain(
        nb,
        frame.meshes_of(nb),
        GRIP * np.ones((1, 3 * n), dtype=object),
        W * np.ones((2, 1), dtype=object),
    )
    rng = np.random.default_rng(7)
    a = np.array(rng.integers(-1000, 1000, (2, n)), dtype=object)
    s = State(
        a,
        a + np.array(rng.integers(-5, 6, (2, n)), dtype=object),
        np.full((2, n), W // 2, dtype=object),
        0 * a,
    )
    pitch = math.gcd(W, GRIP)
    seven = np.concatenate([np.arange(n)[None, :], nb]).T
    teeth, counts = [], []
    for t in range(ROUNDS):
        s = step.tick(y, s)
        if t >= FROM:
            digit = [int(s.r[0, i]) // pitch + int(s.r[1, i]) // pitch for i in range(n)]
            count = [int(s.a[0, i]) + int(s.a[1, i]) for i in range(n)]
            teeth.append([sum(digit[j] for j in seven[i]) for i in range(n)])
            counts.append([sum(count[j] for j in seven[i]) for i in range(n)])
    values = sorted({int(r) // pitch for r in s.r.reshape(-1)})
    print(
        f"W = {W}, the grip {GRIP}, the pitch gcd(W, grip) = the grip: a fine tooth takes {W // pitch} values"
    )
    print(f"the digits read at the last round: {values}")
    low, high = min(map(min, teeth)), max(map(max, teeth))
    print(f"V over the seven Node-clocks, fine teeth in pitch units: from {low} to {high}")
    print("\nd = V mod L on the fine teeth (the node with no dial):")
    for size in SIZES:
        reached = {v % size for row in teeth for v in row}
        print(f"  L = {size}: values of d reached {len(reached)} of {size}")
    print("\nd = V mod L on the now counts in place of the fine teeth:")
    for size in SIZES[2:]:
        d = np.array([[v % size for v in row] for row in counts], dtype=np.int64)
        tenths = np.bincount(((d * 10) // size).reshape(-1), minlength=10)
        chi = float((((tenths - tenths.sum() / 10) ** 2) / (tenths.sum() / 10)).sum())
        apart = float(np.mean((d * 2) // size == (d[:, nb[0]] * 2) // size))
        row = float(np.mean((d[1:] * 2) // size == (d[:-1] * 2) // size))
        print(
            f"  L = {size}: chi-square of the tenths on 9 {chi:.1f}; one Mesh apart in one half {apart:.3f}; "
            f"two rounds in a row in one half {row:.3f}"
        )
    print(f"\nthe counts' V spans {min(map(min, counts))} to {max(map(max, counts))}")
    print(
        "\nd = (c + V) mod L on the fine teeth, c a dial stepping one count a round (decision 29's c):"
    )
    v = np.array(teeth, dtype=np.int64)
    c = np.arange(v.shape[0])[:, None]
    for size in SIZES[2:6]:
        half = (((c + v) % size) * 2) // size
        row = float(np.mean(half[1:] == half[:-1]))
        apart = float(np.mean(half == half[:, nb[0]]))
        print(
            f"  L = {size}: two rounds in a row in one half {row:.3f}; one Mesh apart in one half {apart:.3f}"
        )


if __name__ == "__main__":
    main()
