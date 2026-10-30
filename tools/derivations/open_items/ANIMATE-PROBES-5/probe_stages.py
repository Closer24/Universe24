"""Animate's bench probes on tensor24-review at 4b39f234b (integers only): python3.14 -I probe_stages.py <a worktree of the branch>.

1. Stage 5, the ring, on random twin hands of 130-bit coefficients: T T = -1, Lagrange's N<phi, psi> + N<T phi, psi> =
   rho_phi rho_psi, S . S = rho rho, and the turnover reverses the reading: axis(T psi) = (rho, -S).
2. Stages 2 and 3, the decoder's count of ticks from the rate lines: random masks on the stage 3 engine (rates parted,
   one clock stopped); the rate lines written per Node-clock at its first beat and at each beat whose k differs from its
   last beat's, with the beat's count; the ticks to every count read back from the lines against the k actually put out.
   Also the lines written per round instead (k as fire times k), to count what that wording would cost.
"""

import sys

import numpy as np

sys.path[:0] = [sys.argv[1] + "/src", sys.argv[1]]

from tensor24.algebra import ring  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tests.test_the_tensor24_mesh import T, parted  # noqa: E402


def twin(rng, bits):
    def one():
        return int(rng.integers(0, 1 << 62)) * (1 << (bits - 62)) + int(
            rng.integers(-(1 << 62), 1 << 62)
        )

    return ((one(), one()), (one(), one()))


def ring_laws(seed, cases, bits):
    rng = np.random.default_rng(seed)
    held = {"T T = -1": 0, "Lagrange": 0, "S . S = rho rho": 0, "axis(T psi) = (rho, -S)": 0}
    for _ in range(cases):
        phi, psi = twin(rng, bits), twin(rng, bits)
        tt = ring.reverse(ring.reverse(psi))
        held["T T = -1"] += tt == ((-psi[0][0], -psi[0][1]), (-psi[1][0], -psi[1][1]))
        rho_phi, _ = ring.axis(phi)
        rho_psi, spin = ring.axis(psi)
        lagrange = ring.norm(ring.overlap(phi, psi)) + ring.norm(ring.overlap(ring.reverse(phi), psi))
        held["Lagrange"] += lagrange == rho_phi * rho_psi
        held["S . S = rho rho"] += sum(s * s for s in spin) == rho_psi * rho_psi
        rho_t, spin_t = ring.axis(ring.reverse(psi))
        held["axis(T psi) = (rho, -S)"] += rho_t == rho_psi and spin_t == tuple(-s for s in spin)
    return held


def rate_lines(seed):
    layout, s, rng = parted(seed)
    n = s.c.shape[1]
    by_beat, by_round = [[] for _ in range(n)], [[] for _ in range(n)]
    last_beat, last_round = [None] * n, [None] * n
    truth = [[] for _ in range(n)]  # (count after the beat, k) for every beat
    rounds = 0
    while (s.c < T).any() and rounds < 60 * T:
        allowed = rng.integers(0, 2, size=s.c.shape).astype(object)
        s, out = step.tick(layout, s, allowed)
        rounds += 1
        for i in range(n):
            fire, k, count = int(out.fire[0, i]), int(out.k[0, i]), int(s.c[0, i])
            if fire:
                truth[i].append((count, k))
                if last_beat[i] != k:
                    by_beat[i].append((count, k))
                    last_beat[i] = k
            if last_round[i] != k:
                by_round[i].append((rounds, k))
                last_round[i] = k
    held, asked = 0, 0
    for i in range(n):
        ticks = 0
        for count, k in truth[i]:
            ticks += k
            # the decoder's reading: the k in force at this beat is the last line's at or before its count
            lines = [kk for cc, kk in by_beat[i] if cc <= count]
            stretch = []
            for cc, kk in by_beat[i]:
                stretch.append((cc, kk))
            read = 0
            for j, (cc, kk) in enumerate(stretch):
                end = stretch[j + 1][0] - 1 if j + 1 < len(stretch) else count
                end = min(end, count)
                if cc <= count:
                    read += kk * (end - cc + 1)
            asked += 1
            held += read == ticks and bool(lines)
    beats = sum(len(t) for t in truth)
    return {
        "beats": beats,
        "ticks read back right at every beat": f"{held} of {asked}",
        "rate lines, written by the beat": sum(len(b) for b in by_beat),
        "rate lines, written by the round (k as fire times k)": sum(len(b) for b in by_round),
        "rounds": rounds,
    }


def main():
    for seed in (0, 1, 2):
        print(f"seed {seed}: ring, 2,000 pairs at 130 bits: {ring_laws(seed, 2000, 130)}")
    for seed in (0, 1, 2):
        print(f"seed {seed}: rate lines on the stage 3 engine, random masks: {rate_lines(seed)}")


if __name__ == "__main__":
    main()
