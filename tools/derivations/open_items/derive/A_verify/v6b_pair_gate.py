"""V6b (verifier A): a fitted pair (+e at x, -e at y) on an otherwise empty ring, stepped exactly (no carry, uniform
rates, no pawl wall: the step keeps SUM W exactly).  Does the pair's own book W_x + W_y = 0 stay?  python3 -I"""
from fractions import Fraction as Fr
N, A, B = 10, 125, 144
w, g = Fr(10 ** 6), Fr(2 * 10 ** 4)   # teeth and one grip per Mesh, uniform
a = [(Fr(0), Fr(0))] * N
b = [(Fr(0), Fr(0))] * N
a[3], b[3] = (Fr(A), Fr(0)), (Fr(0), Fr(B))       # (+A, i B): W = +A B
a[4], b[4] = (Fr(-A), Fr(0)), (Fr(0), Fr(B))      # (-A, i B): W = -A B
P = [((a[x][0] - b[x][0]) * w, (a[x][1] - b[x][1]) * w) for x in range(N)]
W = lambda n, p: n[0] * p[1] - n[1] * p[0]
for t in range(1, 6):
    newP = []
    for x in range(N):
        pull = [sum(g * (a[y][k] - a[x][k]) for y in ((x + 1) % N, (x - 1) % N)) for k in range(2)]
        newP.append((P[x][0] + pull[0], P[x][1] + pull[1]))
    na = [(a[x][0] + newP[x][0] / w, a[x][1] + newP[x][1] / w) for x in range(N)]
    b, a, P = a, na, newP
    Ws = [W(a[x], b[x]) for x in range(N)]
    print(f"tick {t}: SUM W = {float(sum(Ws)):.6g} (kept exactly: {sum(Ws) == 0}); the pair's own W_x + W_y = {float(Ws[3] + Ws[4]):.6g};"
          f" W at x, y: {float(Ws[3]):.6g}, {float(Ws[4]):.6g}")
