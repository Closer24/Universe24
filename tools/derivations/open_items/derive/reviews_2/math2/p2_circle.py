# Probe 2: law 10 against laws 3 and 4.  A reversible integer board (law 2's form, one odd teeth count W,
# the flip r -> W-1-r so that T S T = S^-1 holds exactly), a time gear X that rises and falls, and the
# turnover at X's weak top (symmetric under the exchange of X's two notches).  Two readings of law 4:
#   G1: at a top the turnover replaces the step;  G2: at a top the step is taken and then turned over.
# The probe counts the distinct states the board holds at each return of X to its lowest value (a "bang").
import random
W = 7
def mid(W): return W // 2
N = 6  # matter gears on a ring, plus the time gear X at index N
def force(n):
    # integer linear pull, symmetric; X couples weakly to the ring by a product term (nonlinear, odd in nothing special)
    f = [0] * (N + 1)
    for i in range(N):
        f[i] = (n[(i - 1) % N] + n[(i + 1) % N] - 2 * n[i]) - n[i] // 1 * 0 + ((n[N] * n[i]) // 64)
    f[N] = -n[N] // 4 * 0 - n[N] + sum(n[i] * n[i] for i in range(N)) // 256
    return f
def S(state):
    b, n, r = state
    f = force(n)
    nb, nn, nr = list(n), [], []
    for i in range(N + 1):
        p = W * (n[i] - b[i]) + (r[i] - mid(W))
        q, rr = divmod(p + f[i] + mid(W), W)
        nn.append(n[i] + q); nr.append(rr)
    return (tuple(nb), tuple(nn), tuple(nr))
def T(state):
    b, n, r = state
    return (n, b, tuple(W - 1 - x for x in r))
def top(state, nxt):
    x0, x1, x2 = state[0][N], state[1][N], nxt[1][N]
    return x0 <= x1 >= x2 and (x0 < x1 or x1 > x2)
def run(G, x0, steps):
    x = x0; bangs = []; turns = 0; seen = {}
    lowX = None
    hist = []
    for t in range(steps):
        y = S(x)
        if top(x, y):
            turns += 1
            x = T(x) if G == 1 else T(y)
        else:
            x = y
        hist.append(x)
        if x == x0 or x == T(x0):
            bangs.append(t + 1)
    return turns, bangs[:8], hist
rng = random.Random(3)
# seed 1: at rest (a = a-, r = mid): T-symmetric at odd W
n0 = tuple([rng.randint(-30, 30) for _ in range(N)] + [-400])
rest = (n0, n0, tuple([mid(W)] * (N + 1)))
# seed 2: moving (not T-symmetric)
b0 = tuple(v - rng.randint(-3, 3) for v in n0)
moving = (b0, n0, tuple(rng.randint(0, W - 1) for _ in range(N + 1)))
for name, x0 in (("rest seed", rest), ("moving seed", moving)):
    for G in (1, 2):
        turns, bangs, hist = run(G, x0, 4000)
        # period: first return to x0
        per = next((t + 1 for t, h in enumerate(hist) if h == x0), None)
        distinct = len(set(hist))
        print(name, "G%d" % G, "turnovers", turns, "first returns to x0 or T x0 at", bangs, "period", per, "distinct states", distinct)
# sanity: T S T = S^-1 on random states
bad = 0
for _ in range(2000):
    st = (tuple(rng.randint(-50, 50) for _ in range(N + 1)), tuple(rng.randint(-50, 50) for _ in range(N + 1)), tuple(rng.randint(0, W - 1) for _ in range(N + 1)))
    if T(S(T(S(st)))) != st: bad += 1
print("T S T S = id failures", bad, "of 2000")
