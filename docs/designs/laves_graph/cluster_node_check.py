"""Hypothesis B's second form (the Boss's record 2143 on the model owner's question,
"can our Node of today be built from sub-Nodes of three exits?"): one Node of six
Ports as ten sub-Nodes of three exits each, six face sub-Nodes (one outer Link to
the neighbour's opposite face, two Links to the hubs on the face) and four hubs on
alternate corners of the cube. A host computation on the Bloch adjacency of the
cubic lattice of clusters, no engine, no pin; it reproduces the Boss's numbers and
adds the point group and the internal modes' content.

Read on 2026-09-26: every sub-Node has three exits; the long wave is isotropic (0.04
times the identity per Node spacing); the anisotropy is +0.0111 k^2 on the body
diagonal and +0.0083 k^2 on the face diagonal, 2.5 times smaller than the cubic
lattice's +0.0278 and +0.0208; the adjacency at k = 0 has the values 3 (the long
wave), 1 five-fold and -2 four-fold; the cluster's point group is T_d (the hubs'
tetrahedron; no handedness, but the cube's quarter turn is gone); the five-fold
level is E + T_2 and the four-fold level A_1 + T_2 under T_d; away from k = 0 the
internal levels disperse into bands (along an axis the -2 level spreads to -2.5 to
-1 and the 1 level to -0.3 to 2), so they propagate as high branches and are not
local states.

Run: python docs/designs/laves_graph/cluster_node_check.py (about one second).
"""

import itertools

import numpy as np

faces = [np.array(v) for v in ([1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1])]
hubs = [np.array(v) for v in ([1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1])]


# sub-Node index: faces 0..5, hubs 6..9
def bloch(k):
    H = np.zeros((10, 10), dtype=complex)
    for f, v in enumerate(faces):
        # hub links: the hubs on this face
        for h, c in enumerate(hubs):
            if np.dot(c, v) == 1:
                H[f, 6 + h] += 1
                H[6 + h, f] += 1
        # the outer Link: to the opposite face sub-Node of the neighbour at +v
        g = next(i for i, u in enumerate(faces) if np.array_equal(u, -v))
        H[f, g] += np.exp(1j * np.dot(k, v))  # the neighbour cluster at +v, its face -v
    return H


degrees = np.abs(bloch(np.zeros(3))).sum(axis=1)
print("degrees:", degrees.astype(int))


def lam(k):
    return np.linalg.eigvalsh(bloch(np.asarray(k, float))).max()


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
print("lam(0) =", round(l0, 6), "second-order tensor per Node spacing:\n", np.round(Q / 2, 6))


def fan(k):
    ax = np.array([k, 0, 0])
    dg = np.array([k, k, k]) / np.sqrt(3)
    fc = np.array([k, k, 0]) / np.sqrt(2)

    def w(q):
        return np.sqrt(l0 - lam(q))

    return (w(dg) - w(ax)) / w(ax) / k**2, (w(fc) - w(ax)) / w(ax) / k**2


for k in (0.1, 0.2):
    d, f = fan(k)
    print(
        f"k={k}: anisotropy coefficient body diag {d:+.5f}, face diag {f:+.5f}  (cubic: +0.02778, +0.02083)"
    )
vals = np.linalg.eigvalsh(bloch(np.zeros(3)))
print("adjacency at k = 0:", np.round(vals, 6))
# band flatness of the internal modes: eigenvalues along k from 0 to the zone edge
for kx in (0.0, 0.5, 1.0, 2.0, np.pi):
    v = np.linalg.eigvalsh(bloch(np.array([kx, 0, 0])))
    print(f"  k = ({kx:.2f},0,0): eigenvalues", np.round(v, 3))


# the point group T_d: signed permutations preserving the hub tetrahedron; decompose the k = 0 eigenspaces
def elements():
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            if np.prod(signs) == 1:
                M = np.zeros((3, 3))
                for i in range(3):
                    M[i, perm[i]] = signs[i]
                yield M


def perm_matrix(M):
    P = np.zeros((10, 10))
    pts = faces + hubs
    for i, p in enumerate(pts):
        q = M @ p
        j = next(jj for jj, r in enumerate(pts) if np.array_equal(r, q))
        P[j, i] = 1
    return P


H0 = bloch(np.zeros(3)).real
w, V = np.linalg.eigh(H0)
groups = {}
for val, vec in zip(np.round(w, 6), V.T, strict=True):
    groups.setdefault(val, []).append(vec)
# T_d classes by (det, trace): E: (1,3); 8C3: (1,0); 3C2: (1,-1); 6S4: (-1,-1); 6 sigma_d: (-1,1)
table = {  # T_d character table, classes in the order E, 8C3, 3C2, 6S4, 6sd
    "A1": [1, 1, 1, 1, 1],
    "A2": [1, 1, 1, -1, -1],
    "E": [2, -1, 2, 0, 0],
    "T1": [3, 0, -1, 1, -1],
    "T2": [3, 0, -1, -1, 1],
}
sizes = [1, 8, 3, 6, 6]


def cls(M):
    d = round(np.linalg.det(M))
    tr = round(np.trace(M))
    return {(1, 3): 0, (1, 0): 1, (1, -1): 2, (-1, -1): 3, (-1, 1): 4}[(d, tr)]


els = list(elements())
assert len(els) == 24
for val, vecs in groups.items():
    B = np.array(vecs).T  # 10 x m
    Pproj = B @ B.T
    chi = np.zeros(5)
    for M in els:
        chi[cls(M)] += np.trace(Pproj @ perm_matrix(M))
    chi = chi / np.array(sizes)
    dec = {
        name: round(sum(s * c * x for s, c, x in zip(sizes, chi, ch, strict=True)) / 24, 3)
        for name, ch in table.items()
    }
    print(
        f"eigenvalue {val}: multiplicity {len(vecs)}: T_d content",
        {k_: v_ for k_, v_ in dec.items() if abs(v_) > 1e-6},
    )
