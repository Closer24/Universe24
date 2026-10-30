"""Usage: python3 -I t5_trace.py

Term 5's source in whole numbers: with T the outer product of the four-vector v (stride, gradients) and V the
spring's part, the full stress is S = v v - eta (v.v / 2 + V), and its trace-reversal 2S - eta tr S equals 2 v v + 2 eta V.
The page's form, 2T - eta tr T with T = v v, differs: on a uniform swing with no spring it gives the 00 slot stride^2
and each ii slot stride^2, where rho + 3p = 2 stride^2 and rho - p = 0."""
from fractions import Fraction as F
import itertools
import random

eta = [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
inv = eta  # eta is its own inverse


def outer(v):
    return [[F(v[i] * v[j]) for j in range(4)] for i in range(4)]


def dot(v):
    return sum(inv[i][i] * v[i] * v[i] for i in range(4))


def trace(t):
    return sum(inv[i][i] * t[i][i] for i in range(4))


def reverse(t):
    tr = trace(t)
    return [[2 * t[i][j] - eta[i][j] * tr for j in range(4)] for i in range(4)]


rng = random.Random(24)
ok = True
for _ in range(2000):
    v = [rng.randrange(-50, 51) for _ in range(4)]
    V = rng.randrange(-50, 51)
    full = [[outer(v)[i][j] - eta[i][j] * (F(dot(v), 2) + V) for j in range(4)] for i in range(4)]
    want = [[2 * outer(v)[i][j] + 2 * eta[i][j] * V for j in range(4)] for i in range(4)]
    ok = ok and reverse(full) == want
print("2S - eta tr S = 2 v v + 2 eta V on 2000 whole four-vectors and springs:", ok)
s = 7
v = [s, 0, 0, 0]
page = reverse(outer(v))
right = [[2 * outer(v)[i][j] for j in range(4)] for i in range(4)]
print(f"uniform swing, stride {s}, no spring: the page's form gives 00 = {page[0][0]}, each ii = {page[1][1]};"
      f" the full stress gives 00 = {right[0][0]} (rho + 3p), each ii = {right[1][1]} (rho - p)")
