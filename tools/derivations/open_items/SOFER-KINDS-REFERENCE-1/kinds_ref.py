"""Sofer's independent reference for the 24 (the cube's rotations) and its five kinds, in integers only.

The group: the 24 signed permutation matrices of three axes with determinant +1. Classes by (order, trace).
Kinds: A1 = 1, A2 = sign of the permutation of the four body diagonals, T1 = the trace, T2 = T1 A2,
E = (the faces' permutation character) - A1 - T1. No float; every value a whole number."""

from itertools import permutations, product


def rotations():
    out = []
    for p in permutations(range(3)):
        for s in product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for i in range(3):
                m[i][p[i]] = s[i]
            det = (
                m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
            )
            if det == 1:
                out.append(tuple(map(tuple, m)))
    return out


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def apply(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


def order(m):
    ident = tuple(tuple(int(i == j) for j in range(3)) for i in range(3))
    x, n = m, 1
    while x != ident:
        x, n = mul(x, m), n + 1
    return n


def trace(m):
    return m[0][0] + m[1][1] + m[2][2]


def diagonals():
    return [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]  # the four lines, one vector each


def line_of(v):
    return v if v in diagonals() else tuple(-x for x in v)


def sign_of_perm(images):
    seen, parity = set(), 0
    for i in range(len(images)):
        if i in seen:
            continue
        j, length = i, 0
        while j not in seen:
            seen.add(j)
            j = images[j]
            length += 1
        parity += length - 1
    return 1 - 2 * (parity % 2)


def characters():
    group = rotations()
    assert len(group) == 24
    lines = diagonals()
    faces = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    table = {}
    for g in group:
        a2 = sign_of_perm([lines.index(line_of(apply(g, v))) for v in lines])
        fixed = sum(apply(g, f) == f for f in faces)
        t1 = trace(g)
        table[g] = {
            "A1": 1,
            "A2": a2,
            "T1": t1,
            "T2": t1 * a2,
            "E": fixed - 1 - t1,
            "order": order(g),
            "fixed": fixed,
        }
    return group, table


def check():
    group, table = characters()
    names = ["A1", "A2", "E", "T1", "T2"]
    identity = next(g for g in group if table[g]["order"] == 1)
    dims = {n: table[identity][n] for n in names}
    assert dims == {"A1": 1, "A2": 1, "E": 2, "T1": 3, "T2": 3}, dims
    for i in names:
        for j in names:
            s = sum(table[g][i] * table[g][j] for g in group)
            assert s == (24 if i == j else 0), (i, j, s)
    classes = {}
    for g in group:
        classes.setdefault((table[g]["order"], trace(g), table[g]["fixed"]), []).append(g)
    assert sorted(len(v) for v in classes.values()) == [1, 3, 6, 6, 8], sorted(
        len(v) for v in classes.values()
    )
    return group, table, classes


if __name__ == "__main__":
    group, table, classes = check()
    print("24 rotations; 5 classes by (order, trace, fixed faces):")
    for key, members in sorted(classes.items()):
        t = table[members[0]]
        print(key, len(members), {n: t[n] for n in ["A1", "A2", "E", "T1", "T2"]})
    print("orthonormal: yes (25 sums of 24 g)")
