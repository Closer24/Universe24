"""Usage: python3 -I t5_trace.py

Term 5's source in whole numbers: with T the outer product of the four-vector v (stride, gradients) and V the
spring's part, the full stress is S = v v - eta (v.v / 2 + V); taken whole, 2S = 2 v v - eta (v.v + 2 V), and its
trace-reversal 2 (2S) - eta tr (2S) equals 4 v v + 4 eta V, twice 2 v v + 2 eta V (Sofer's whole form, #2187
6517919800, item 3). The vectors and springs come from a carry sequence, no draw. The page's form, 2T - eta tr T with
T = v v, differs: on a uniform swing with no spring it gives the 00 slot stride^2 and each ii slot stride^2, where
rho + 3p = 2 stride^2 and rho - p = 0."""

eta = [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # its own inverse


def carry(n, d, r):
    """Rule3: n + r = q d + r' with 0 <= r' < d."""
    u = n + r
    return u // d, u % d


def outer(v):
    return [[v[i] * v[j] for j in range(4)] for i in range(4)]


def dot(v):
    return sum(eta[i][i] * v[i] * v[i] for i in range(4))


def trace(t):
    return sum(eta[i][i] * t[i][i] for i in range(4))


def reverse(t):
    tr = trace(t)
    return [[2 * t[i][j] - eta[i][j] * tr for j in range(4)] for i in range(4)]


state = 24


def next_count():
    """A carry sequence: the state's next value is the kept part of 1103515245 state + 12345 over 2^31; each count
    in -50..50 is the kept part of the state over 101, less 50."""
    global state
    _, state = carry(1103515245 * state + 12345, 2**31, 0)
    _, count = carry(state, 101, 0)
    return count - 50


ok = True
for _ in range(2000):
    v = [next_count() for _ in range(4)]
    V = next_count()
    twice = [[2 * outer(v)[i][j] - eta[i][j] * (dot(v) + 2 * V) for j in range(4)] for i in range(4)]
    want = [[4 * outer(v)[i][j] + 4 * eta[i][j] * V for j in range(4)] for i in range(4)]
    ok = ok and reverse(twice) == want
print("2 (2S) - eta tr (2S) = 4 v v + 4 eta V on 2000 whole four-vectors and springs from a carry sequence:", ok)
s = 7
v = [s, 0, 0, 0]
page = reverse(outer(v))
right = [[2 * outer(v)[i][j] for j in range(4)] for i in range(4)]
print(f"uniform swing, stride {s}, no spring: the page's form gives 00 = {page[0][0]}, each ii = {page[1][1]};"
      f" the full stress gives 00 = {right[0][0]} (rho + 3p), each ii = {right[1][1]} (rho - p)")
