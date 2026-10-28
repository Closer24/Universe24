"""The cube's 24 turns on the kinds: characters of V, Sym2 V, Lambda2 V, xyz and the trace, against the five irreducible kinds of the rotation group O."""
import itertools
import numpy as np
mats = []
for perm in itertools.permutations(range(3)):
    for signs in itertools.product((1, -1), repeat=3):
        m = np.zeros((3, 3), dtype=np.int64)
        for i, (j, s) in enumerate(zip(perm, signs)):
            m[i, j] = s
        if round(np.linalg.det(m)) == 1:
            mats.append(m)
assert len(mats) == 24
def sym2(m):  # action on the 6 components (xx, yy, zz, yz, zx, xy)
    idx = [(0, 0), (1, 1), (2, 2), (1, 2), (2, 0), (0, 1)]
    out = np.zeros((6, 6), dtype=np.int64)
    for c, (a, b) in enumerate(idx):
        t = np.outer(m[:, a], m[:, b]); t = t + t.T
        for r, (i, j) in enumerate(idx):
            out[r, c] = t[i, j] // (2 if i == j else 1) if i == j else t[i, j]
    return out
chars = {
    "V (vector, 3)": [int(np.trace(m)) for m in mats],
    "Sym2 V (6)": [int(np.trace(sym2(m))) for m in mats],
    "Lambda2 V (axial, 3)": [int((np.trace(m) ** 2 - np.trace(m @ m)) // 2) for m in mats],
    "xyz (1)": [int(np.prod([m[i, np.nonzero(m[i])[0][0]] for i in range(3)])) for m in mats],
}
# classes of O by (trace, order)
def order(m):
    p, k = m.copy(), 1
    while not (p == np.eye(3, dtype=np.int64)).all():
        p, k = p @ m, k + 1
    return k
cls = [(int(np.trace(m)), order(m)) for m in mats]
classes = sorted(set(cls))
irreps = {  # characters of O on the classes keyed (trace, order): E(3,1), C2 axis(-1,2), C3(0,3), C4(1,4), C2' edge(-1,2)
}
print("classes (trace, order) and sizes:", [(c, cls.count(c)) for c in classes])
for name, ch in chars.items():
    by = {c: ch[cls.index(c)] for c in classes}
    print(name, by)
# Decompose with the character table of O (orders: identity, 8 C3, 6 C4, 3 C2 (= C4^2), 6 C2')
# C2 axis and C2' both have trace -1 and order 2: split them by whether m^2 of a C4 ... use the fixed axis: C2 about a cube axis is diagonal.
def kind(m):
    t, o = int(np.trace(m)), order(m)
    if o == 1: return "E"
    if o == 3: return "C3"
    if o == 4: return "C4"
    return "C2" if (np.abs(m) == np.eye(3, dtype=np.int64)).all() else "C2'"
size = {"E": 1, "C3": 8, "C4": 6, "C2": 3, "C2'": 6}
table = {"A1": {"E": 1, "C3": 1, "C4": 1, "C2": 1, "C2'": 1}, "A2": {"E": 1, "C3": 1, "C4": -1, "C2": 1, "C2'": -1},
         "E": {"E": 2, "C3": -1, "C4": 0, "C2": 2, "C2'": 0}, "T1": {"E": 3, "C3": 0, "C4": 1, "C2": -1, "C2'": -1},
         "T2": {"E": 3, "C3": 0, "C4": -1, "C2": -1, "C2'": 1}}
for name, ch in chars.items():
    by = {}
    for m, x in zip(mats, ch):
        by[kind(m)] = x
    mult = {ir: sum(size[c] * by[c] * table[ir][c] for c in size) // 24 for ir in table}
    print(f"{name:22s} =", " + ".join(f"{n} {ir}" if n > 1 else ir for ir, n in mult.items() if n))
print("sum of squares of the five kinds' dimensions:", 1 + 1 + 4 + 9 + 9)
# spinors: the quarter turn about z in SU(2) is diag(e^{-i pi/4}, e^{i pi/4}); its entries' squared modulus 1/2 per component of (1 - i)/sqrt 2: no integer (or rational) 2x2 matrix
q = np.array([[1 - 1j, 0], [0, 1 + 1j]]) / np.sqrt(2)
print("spinor quarter turn squared (half turn) =", np.round(q @ q, 12).tolist(), "; its entries need sqrt 2:", np.round(q[0, 0], 6))
