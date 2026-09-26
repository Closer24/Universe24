"""Hypothesis B of ALGEBRA.md 9.103 (the model owner's reading of 2026-09-26, "a
base of three exits per Node"): the second-order rule's long-wave dispersion on
the Laves graph (the srs net, three exits per Node at 120 degrees, eight Nodes
per cubic cell, space group I4_1 32) against the cubic lattice with six Ports.

A host computation on the graphs' Bloch adjacency, no engine and no pin. For a
second-order rule the long-wave frequency squared is proportional to lambda(0)
- lambda(k), lambda the largest eigenvalue of the adjacency at the wave vector
k; the second-order tensor of that difference says whether light is isotropic,
and the fourth-order term is the lattice's own anisotropy, read on the cubic
lattice by the pace fans' diagnostic as the phase pace's difference between the
face diagonal and the axis, k^2 / 48 (reproduced here), and between the body
diagonal and the axis, k^2 / 36.

Read on 2026-09-26: the Laves graph's second-order tensor is isotropic (0.0625
times the identity in units of the cubic cell's edge); its fourth-order
anisotropy is -k^2 / 384 (face diagonal) and -k^2 / 288 (body diagonal), one
eighth of the cubic lattice's and of the opposite sign (the diagonals slower,
not faster); a mirror does not map the net to itself (the net is chiral).

Run: python docs/designs/laves_graph/laves_graph_check.py (about one second).
"""

import itertools

import numpy as np

# srs net: 8 Nodes in the cubic cell (units of the cell edge), Wyckoff 8a of I4_1 32
base = np.array([[1, 1, 1], [3, 7, 5], [7, 5, 3], [5, 3, 7]]) / 8.0
pos = np.vstack([base, (base + 0.5) % 1.0])
n = len(pos)
# links: each Node's three nearest neighbours across periodic images
links = []
for i in range(n):
    cands = []
    for j in range(n):
        for sh in itertools.product((-1, 0, 1), repeat=3):
            d = pos[j] + np.array(sh) - pos[i]
            r = np.linalg.norm(d)
            if r > 1e-9:
                cands.append((r, j, np.array(sh), d))
    cands.sort(key=lambda c: c[0])
    near = [c for c in cands if abs(c[0] - cands[0][0]) < 1e-9]
    assert len(near) == 3, (i, len(near))
    for _r, j, sh, d in near:
        links.append((i, j, sh, d))
    # the three exits at 120 degrees in one plane
    ds = [c[3] for c in near]
    angs = [
        np.degrees(np.arccos(np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)))
        for a, b in itertools.combinations(ds, 2)
    ]
    assert all(abs(a - 120) < 1e-6 for a in angs), angs
edge = links[0][3]
print(
    "srs: 8 Nodes per cubic cell, degree 3, exits at 120 degrees, edge length",
    round(np.linalg.norm(edge), 5),
)


def bloch_srs(k):
    H = np.zeros((n, n), dtype=complex)
    for i, j, _sh, d in links:
        H[i, j] += np.exp(1j * np.dot(k, d))
    return H


def lam_srs(k):
    return np.linalg.eigvalsh(bloch_srs(np.asarray(k, float))).max()


def lam_cubic(k):
    return 2 * np.cos(np.asarray(k, float)).sum()


# second-order tensor: lam(0) - lam(k) ~ Q(k); check isotropy and get the coefficient
for name, lam in (("cubic", lam_cubic), ("srs", lam_srs)):
    l0 = lam([0, 0, 0])
    eps = 1e-3
    Q = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            e = np.zeros(3)
            e[a] += eps
            f = np.zeros(3)
            f[b] += eps
            Q[a, b] = -(lam(e + f) - lam(e) - lam(f) + l0) / eps**2
    print(name, "lam(0) =", round(l0, 6), " second-order tensor (units of k^2):\n", np.round(Q / 2, 6))


# fourth order: the phase pace along the axis against the body diagonal, at small k
def fan(lam, k):
    l0 = lam([0, 0, 0])
    ax = np.array([k, 0, 0])
    dg = np.array([k, k, k]) / np.sqrt(3)
    fc = np.array([k, k, 0]) / np.sqrt(2)
    w_ax = np.sqrt(l0 - lam(ax))
    w_dg = np.sqrt(l0 - lam(dg))
    w_fc = np.sqrt(l0 - lam(fc))
    return (w_dg - w_ax) / w_ax, (w_fc - w_ax) / w_ax


for name, lam in (("cubic", lam_cubic), ("srs", lam_srs)):
    for k in (0.1, 0.2, 0.4):
        d, f = fan(lam, k)
        print(
            f"{name}: k = {k}: (diag - axis)/axis = {d:+.6f}  -> coefficient of k^2: {d / k**2:+.5f};  (face diag - axis)/axis = {f:+.6f} -> {f / k**2:+.5f}"
        )


# chirality: the mirror image of srs is not the same net (check: no improper operation maps the link set to itself)
def same_net(P):
    q = (pos @ P.T) % 1.0
    ok = True
    for i in range(n):
        if not any(
            np.allclose((q[i] - pos[j]) % 1.0 % 1.0, 0, atol=1e-9)
            or np.allclose(((q[i] - pos[j]) % 1.0), 1, atol=1e-9)
            for j in range(n)
        ):
            ok = False
    return ok


mirror = np.diag([-1, 1, 1])
rot4 = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
print(
    "srs invariant under a mirror x -> -x (positions mod 1)?",
    same_net(mirror),
    "; under a quarter turn about z?",
    same_net(rot4),
)
