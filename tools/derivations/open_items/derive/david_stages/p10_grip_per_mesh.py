"""David's check for stage 7's grip, one per Mesh: which lattice coupling is general relativity's wave operator.

usage: python3 -I p10_grip_per_mesh.py
In coordinate time, a field on a static lapse N(x) obeys phi_tt = N d(N d phi) (a flat stretch; one axis suffices).
Three lattice forms, each read in coordinate time:
  the head's:   N_i^2 sum_j (phi_j - phi_i) / h^2                    (a grip per end, p_i^2)
  per Mesh, the clock at its own rate:  N_i sum_j N_ij (phi_j - phi_i) / h^2, N_ij = (N_i + N_j) / 2
      (the beat ticks N_i of the rounds and the end's own teeth carry N_i, the grip the even sum of the two rates)
  per Mesh, the clock at the full rate: sum_j N_ij^2 (phi_j - phi_i) / h^2
Each is compared with the continuum operator at h = 2 pi / n, n from 64 to 1,024; the error of a form that is the
operator falls as h^2. Floats, a continuum statement read on its lattice; no engine is run.
"""
import math


def lapse(x):
    return 1 + 0.3 * math.sin(x)


def dlapse(x):
    return 0.3 * math.cos(x)


def field(x):
    return math.cos(2 * x)


def gr(x):  # N (N phi')' = N (N' phi' + N phi'')
    return lapse(x) * (dlapse(x) * (-2 * math.sin(2 * x)) + lapse(x) * (-4 * math.cos(2 * x)))


for n in (64, 128, 256, 512, 1024):
    h = 2 * math.pi / n
    err = {"head": 0.0, "beat": 0.0, "full": 0.0}
    for i in range(n):
        x = i * h
        xs = [(x + h), (x - h)]
        ni = lapse(x)
        diffs = [(field(y) - field(x), (ni + lapse(y)) / 2) for y in xs]
        head = ni * ni * sum(d for d, _ in diffs) / h**2
        beat = ni * sum(m * d for d, m in diffs) / h**2
        full = sum(m * m * d for d, m in diffs) / h**2
        g = gr(x)
        for k, v in (("head", head), ("beat", beat), ("full", full)):
            err[k] = max(err[k], abs(v - g))
    print(f"n = {n:5d}: largest error, the head's {err['head']:.2e}, per Mesh at its own rate {err['beat']:.2e},"
          f" per Mesh at the full rate {err['full']:.2e}")
