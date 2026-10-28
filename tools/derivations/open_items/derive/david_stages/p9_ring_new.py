"""David's probe of the ring's three new laws at 81521e0f4 (the fourth hostile reviewer's R1), on algebra/ring.py.

usage: python3 -I p9_ring_new.py <worktree>/src
  the joint dial: <T phi, psi> = phi_up psi_down - phi_down psi_up (a determinant, so <T phi, phi> = 0: Kramers);
  the split's share in the readings: 2 N<phi, psi> = rho rho' + S . S' and 2 N<T phi, psi> = rho rho' - S . S';
  S's orientation: S = (2 Re conj(up) down, 2 Im conj(up) down, N(up) - N(down)), so up alone reads +z,
  (1, 1) reads +x and (1, i) reads +y; the plan's T = (-conj down, conj up) turns S to -S, and so does its
  negative (i sigma_y) K, the sign of the older pages: only the joint dial sees which of the two is used.
20,000 draws at 120 bits.
"""
import random
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.ring import axis, conj, mul, norm, overlap, reverse  # noqa: E402

rng = random.Random(81521)
B = 1 << 120
bad = dict.fromkeys(("joint", "share", "orient", "signs"), 0)
N = 20000
for _ in range(N):
    phi = ((rng.randint(-B, B), rng.randint(-B, B)), (rng.randint(-B, B), rng.randint(-B, B)))
    psi = ((rng.randint(-B, B), rng.randint(-B, B)), (rng.randint(-B, B), rng.randint(-B, B)))
    (pu, pd), (qu, qd) = phi, psi
    det = (mul(pu, qd)[0] - mul(pd, qu)[0], mul(pu, qd)[1] - mul(pd, qu)[1])
    bad["joint"] += overlap(reverse(phi), psi) != det
    r1, s1 = axis(phi)
    r2, s2 = axis(psi)
    dot = sum(x * y for x, y in zip(s1, s2))
    bad["share"] += 2 * norm(overlap(phi, psi)) != r1 * r2 + dot or 2 * norm(overlap(reverse(phi), psi)) != r1 * r2 - dot
    # (i sigma_y) K psi = (conj down, -conj up), the negative of the plan's T: it turns S over too, and its
    # joint dial is the plan's negated
    other = (conj(qd), (-qu[0], qu[1]))
    flipped = axis(other)[1] == tuple(-x for x in s2) and other == tuple((-z[0], -z[1]) for z in reverse(psi))
    bad["signs"] += not flipped
one, zero = (1, 0), (0, 0)
bad["orient"] = int(axis((one, zero))[1] != (0, 0, 1) or axis((one, one))[1] != (2, 0, 0) or axis((one, (0, 1)))[1] != (0, 2, 0))
for k, v in bad.items():
    print(f"{k}: failures {v}" + ("" if k == "orient" else f" of {N}"))
