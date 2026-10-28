"""V6c (verifier A): the fitted pair (+e at x = 3, -e at y = 4) with one more hand of the same train standing two
Meshes away (at 6), stepped exactly (no carry, uniform rates, no pawl wall), so SUM W is kept exactly.  The pair's
own book W_x + W_y, which F5's gate requires to be 0, is read each tick.  python3 -I"""
from fractions import Fraction as Fr
N, A, B = 10, 125, 144
w, g = Fr(10 ** 6), Fr(2 * 10 ** 4)
a = [(Fr(0), Fr(0))] * N
b = [(Fr(0), Fr(0))] * N
a[3], b[3] = (Fr(A), Fr(0)), (Fr(0), Fr(B))
a[4], b[4] = (Fr(-A), Fr(0)), (Fr(0), Fr(B))
a[6], b[6] = (Fr(90), Fr(40)), (Fr(85), Fr(47))     # a hand of the same train, standing apart
P = [((a[x][0] - b[x][0]) * w, (a[x][1] - b[x][1]) * w) for x in range(N)]
W = lambda n, p: n[0] * p[1] - n[1] * p[0]
total0 = sum(W(a[x], b[x]) for x in range(N))
for t in range(1, 7):
    newP = []
    for x in range(N):
        pull = [sum(g * (a[y][k] - a[x][k]) for y in ((x + 1) % N, (x - 1) % N)) for k in range(2)]
        newP.append((P[x][0] + pull[0], P[x][1] + pull[1]))
    na = [(a[x][0] + newP[x][0] / w, a[x][1] + newP[x][1] / w) for x in range(N)]
    b, a, P = a, na, newP
    Ws = [W(a[x], b[x]) for x in range(N)]
    print(f"tick {t}: SUM W - SUM W at the start = {sum(Ws) - total0} (kept exactly); the pair's book W_x + W_y = {float(Ws[3] + Ws[4]):.4g}"
          f" (F5's gate {'open' if Ws[3] + Ws[4] == 0 else 'closed'})")
