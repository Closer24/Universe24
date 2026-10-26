"""rl2 (a): Rule3's conserved form on a ring of Nodes with paces fixed in time, exact rationals, no remainder (the identity's algebra alone): the leapfrog a+ + a- = A a with A_ij = R_ij / w off the diagonal and A_ii = 2 - (D_i + SUM_j R_ij) / w; the form Q_D(t) = a^T D a + a-^T D a- - a^T D A a- is conserved exactly when D A is symmetric. Measured for the head's one-sided reach R_ij = 2 num p_i^2 Q_ij and for the symmetric forms (arith, geom, harm, link), with the weight D = diag(1 / p_i^2) (the law's, the carrier's unit X) and D = I. Prints the largest |Q(t) - Q(0)| over 40 steps as a fraction, 0 where exact."""
from fractions import Fraction as F
import random

random.seed(3)
n, num, den, gamma = 8, 7, 9, 1000
w = 6 * den * gamma * gamma
p = [random.choice([1, 2, 5, 40, 300, 1000]) for _ in range(n)]
Q = {}
for i in range(n):
    j = (i + 1) % n
    Q[(i, j)] = Q[(j, i)] = random.choice([250, 600, 1000, 0])
clock = [pp for pp in p]
D_mass = [12 * (den - num) * c * c for c in clock]
forms = {
    "head one-sided 2 num p_i^2 Q": lambda i, j: F(2 * num * p[i] ** 2 * Q[(i, j)]),
    "arith num (p_i^2+p_j^2) Q": lambda i, j: F(num * (p[i] ** 2 + p[j] ** 2) * Q[(i, j)]),
    "geom 2 num p_i p_j Q": lambda i, j: F(2 * num * p[i] * p[j] * Q[(i, j)]),
    "harm 4 num p_i^2 p_j^2 Q / (p_i^2+p_j^2)": lambda i, j: F(4 * num * p[i] ** 2 * p[j] ** 2 * Q[(i, j)], p[i] ** 2 + p[j] ** 2),
    "link 2 num p_ij^2 Q (p_ij the mean pace)": lambda i, j: F(2 * num * Q[(i, j)]) * F(p[i] + p[j], 2) ** 2,
}
weights = {"D = diag(1/p_i^2)": [F(1, pp * pp) for pp in p], "D = I": [F(1)] * n}


def matrix(R):
    A = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        for j in ((i + 1) % n, (i - 1) % n):
            A[i][j] += R(i, j) / w
        A[i][i] = 2 - F(D_mass[i] + sum(R(i, j) for j in ((i + 1) % n, (i - 1) % n)), w)
    return A


def mv(A, x):
    return [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]


for name, R in forms.items():
    A = matrix(R)
    before = [F(random.randint(-50, 50)) for _ in range(n)]
    now = [F(random.randint(-50, 50)) for _ in range(n)]
    for wname, D in weights.items():
        sym = all(D[i] * A[i][j] == D[j] * A[j][i] for i in range(n) for j in range(n))
        b, a = list(before), list(now)
        def q(a, b):
            Ab = mv(A, b)
            return sum(D[i] * (a[i] * a[i] + b[i] * b[i] - a[i] * Ab[i]) for i in range(n))
        q0, worst = q(a, b), F(0)
        for _ in range(40):
            nxt = [x - y for x, y in zip(mv(A, a), b)]
            b, a = a, nxt
            worst = max(worst, abs(q(a, b) - q0))
        print(f"{name:45s} {wname:18s} D A symmetric: {str(sym):5s}  max |Q(t)-Q(0)| over 40 steps: {worst}")
