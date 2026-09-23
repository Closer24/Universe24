"""COMPUTATION on the algebra (no engine run): the pace c of the six-neighbour
rule from its characters, and the three inputs that fix it (MASSIVE_RECORD.md
section 1.1: locality with the 48, the zero mode, the absent self term).

    PYTHONPATH=src python docs/designs/detector_law/massive_c_derivation.py

The general 48-invariant rule of range 1, second order in time, solved for
a_next:  a_next + a_before = w * SUM6 + s * a_now   (w the neighbour weight,
s the self weight).  Characters exp(i(k.x - omega t)) give
    2 cos omega = 2 w SUM_i cos k_i + s.
"""

import itertools

import numpy as np

# (1) the 48's only invariant rank-2 tensor on the six neighbours is a multiple of I
E = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]])
M2 = sum(np.outer(e, e) for e in E)
print(
    "second moment of the six neighbours SUM e e^T =\n",
    M2,
    " -> (1/3) of it is (2/3) I:",
    np.allclose(M2 / 3, (2 / 3) * np.eye(3)),
)


def omega(k, w, s):
    """cos omega from the characters; complex when |2 cos omega| > 2 (unstable)."""
    c = (2 * w * np.sum(np.cos(k), axis=-1) + s) / 2
    return np.arccos(c.astype(complex))


# (2) masslessness: the uniform record is a solution iff omega(0) = 0 iff s = 2 - 6 w
for w in (0.2, 1 / 3, 0.4):
    s = 2 - 6 * w
    print(f"w={w:.4f} s={s:+.4f}: omega(k=0) = {omega(np.zeros(3), w, s).real:.3e}")

# (3) c^2 = w: the pace near k = 0 in every direction, for the massless family
for w in (0.2, 1 / 3):
    s = 2 - 6 * w
    paces = []
    for d in ([1, 0, 0], [1, 1, 0], [1, 1, 1], [2, 1, 0], [3, 1, 1]):
        d = np.array(d, float)
        d /= np.linalg.norm(d)
        eps = 1e-3
        om = omega(eps * d, w, s).real
        paces.append(om / eps)
    print(
        f"w={w:.4f}: phase pace at k->0 by direction {np.round(paces, 5)}  (sqrt w = {np.sqrt(w):.5f})"
    )

# (4) stability: the checkerboard corner (pi,pi,pi): 2 cos omega = 2 - 12 w; real omega iff w <= 1/3
for w in (0.3, 1 / 3, 0.34):
    s = 2 - 6 * w
    val = 2 - 12 * w
    print(
        f"w={w:.4f}: 2 cos omega at the corner = {val:+.3f} -> {'real (stable)' if val >= -2 else 'complex (grows)'}"
        f"{' ; double root at -2: the checkerboard secular mode' if abs(val + 2) < 1e-12 else ''}"
    )

# (5) the same c for the massive kind: 3 q (a_next + a_before) + 3 p a_now = q SUM6
#     -> w = 1/3, s = -p/q ; omega0 from cos omega0 = 1 - p/(2 q); omega^2 - omega0^2 ~ k^2/3 near 0
c = 1 / np.sqrt(3)
for p, q in ((1, 50), (1, 8), (1, 1), (2, 1)):
    w, s = 1 / 3, -p / q
    om0 = omega(np.zeros(3), w, s).real
    print(
        f"[p,q]=[{p},{q}]: omega0 = {om0:.5f} (arccos(1 - p/2q) = {np.arccos(1 - p / (2 * q)):.5f})",
        end="",
    )
    eps = 1e-2
    om = omega(eps * np.array([1, 0, 0.0]), w, s).real
    print(
        f"; (omega^2 - omega0^2)/k^2 at k=0.01 = {(om**2 - om0**2) / eps**2:.5f} (c^2 = 1/3 = 0.33333)",
        end="",
    )
    # the group pace |grad omega| over the whole zone: never above c
    ks = np.linspace(-np.pi, np.pi, 61)
    K = np.array(list(itertools.product(ks, ks, ks)))
    h = 1e-5
    grads = []
    for ax in range(3):
        dk = np.zeros(3)
        dk[ax] = h
        grads.append((omega(K + dk, w, s).real - omega(K - dk, w, s).real) / (2 * h))
    g = np.linalg.norm(np.array(grads), axis=0)
    print(f"; max group pace over the zone {g.max():.5f} < c = {c:.5f}: {g.max() < c + 1e-9}")

# light itself: the group pace over the zone, its maximum and where
w, s = 1 / 3, 0.0
ks = np.linspace(-np.pi, np.pi, 61)
K = np.array(list(itertools.product(ks, ks, ks)))
h = 1e-5
grads = []
for ax in range(3):
    dk = np.zeros(3)
    dk[ax] = h
    grads.append((omega(K + dk, w, s).real - omega(K - dk, w, s).real) / (2 * h))
g = np.linalg.norm(np.array(grads), axis=0)
i = np.argmax(g)
print(
    f"light [0,1]: max group pace over the zone {g.max():.6f} (c = {c:.6f}) at k = {np.round(K[i], 3)}; along the body diagonal exactly c: {np.allclose(g[np.all(np.isclose(K, K[:, [0]]), axis=1)], c, atol=1e-6)}"
)

# (6) the index: the coefficient form 3 den a_next = num SUM6 + 6(den - num) a_now - 3 den a_before
for num, den in ((1, 1), (2, 3), (1, 2)):
    w, s = num / (3 * den), 2 * (den - num) / den
    eps = 1e-3
    om = omega(eps * np.array([1, 0, 0.0]), w, s).real
    print(
        f"[num,den]=[{num},{den}]: pace {om / eps:.5f} = c/n with n^2 = den/num = {den / num:.4f} -> n = {c / (om / eps):.5f} vs sqrt = {np.sqrt(den / num):.5f}"
    )

# (7) the Beam Law's road in d axes: one Link per interval Manhattan, the slowest line 1/sqrt d;
#     the wave's road: c^2 = 2/(2d) = 1/d. The same number for every d.
for d in (1, 2, 3, 4):
    print(
        f"d={d}: Manhattan-bound isotropic pace 1/sqrt d = {1 / np.sqrt(d):.5f}; wave rule c = sqrt(2/(2d)) = {np.sqrt(1 / d):.5f}"
    )
