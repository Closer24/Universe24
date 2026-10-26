"""The algebra's check in exact rationals (integers' quotients, no float): Rule3's uniform step on a torus, next = (S now - w before + R SUM_ports now_j) / w, one line, and the change of L_c = SUM_i eps_cab x_a(i) p_b(i) with p_b(i) = now_(i+b) before_i - now_i before_(i+b).
(1) a field vanishing on a shell of the cut planes (x_a in {0, c-1} for every a): Delta L = 0 exactly; (2) a field across the cut: Delta L a multiple of c (the wrap's term), Delta P = 0 in both."""
import random
from fractions import Fraction
from itertools import product
random.seed(7)
c = 7
S, R, w = Fraction(1000), Fraction(37), Fraction(1200)
nodes = list(product(range(c), repeat=3))
def shift(i, b, s):
    j = list(i); j[b] = (j[b] + s) % c; return tuple(j)
def step(now, before):
    nxt = {}
    for i in nodes:
        arr = sum(now[shift(i, b, s)] for b in range(3) for s in (1, -1))
        nxt[i] = (S * now[i] - w * before[i] + R * arr) / w
    return nxt
def PL(now, before):
    p = {b: {i: now[shift(i, b, 1)] * before[i] - now[i] * before[shift(i, b, 1)] for i in nodes} for b in range(3)}
    P = [sum(p[b].values()) for b in range(3)]
    L = []
    for cc in range(3):
        a, b = {0: (1, 2), 1: (2, 0), 2: (0, 1)}[cc]
        L.append(sum(i[a] * p[b][i] - i[b] * p[a][i] for i in nodes))
    return P, L
def field(inner):
    now, before = {}, {}
    for i in nodes:
        ok = all(1 <= x <= c - 2 for x in i) if inner else True
        now[i] = Fraction(random.randint(-50, 50)) if ok else Fraction(0)
        before[i] = Fraction(random.randint(-50, 50)) if ok else Fraction(0)
    return now, before
for inner in (True, False):
    now, before = field(inner)
    P0, L0 = PL(now, before)
    nxt = step(now, before)
    P1, L1 = PL(nxt, now)
    dL = [x - y for x, y in zip(L1, L0)]
    print({"field": "inside the cut's shell" if inner else "across the cut", "dP": [str(x - y) for x, y in zip(P1, P0)],
           "dL": [str(x) for x in dL], "dL / c": [str(x / c) for x in dL], "dL multiple of c": all((x / c).denominator == 1 for x in dL)})
