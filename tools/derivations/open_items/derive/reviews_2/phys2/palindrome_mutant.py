# Toy for laws 3, 4 and 10: a reversible second-order integer map S
# with T S T = S^-1 (T exchanges now and before, law 4's a <-> a-),
# and a whole-board turnover T at every weak maximum of a reading X
# (the time gear). Claim: after the first turnover the board only
# retraces the segment between two tops, so the bangs repeat with a
# period of two swings and nothing new is ever shown.
import random, sys
N, M = 9, 1000003
def F(x):
    return [(x[(i-1) % N] + x[(i+1) % N] + (x[i]*x[i]) % 7) % M for i in range(N)]
def S(st):
    a, b = st; fa = F(a)
    return ([(fa[i] - b[i]) % M for i in range(N)], a)
def T(st):
    a, b = st; return (b, a)
def X(st):
    return st[0][0]            # one gear read as the time gear
for _ in range(2000):          # T S T = S^-1 exactly
    st = ([random.randrange(M) for _ in range(N)], [random.randrange(M) for _ in range(N)])
    a, b = st; fb = F(b)
    assert T(S(T(st))) == (b, [(fb[i] - a[i]) % M for i in range(N)])
print("T S T = S^-1 on 2000 random states: ok")
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
for trial in range(6):
    st = ([random.randrange(M) for _ in range(N)], [random.randrange(M) for _ in range(N)])
    prev = X(T(st)); seen = set(); tops = []
    for t in range(20000):
        seen.add((tuple(st[0]), tuple(st[1])))
        nxt = S(st)
        x0, x1, x2 = prev, X(st), X(nxt)
        if x0 <= x1 >= x2 and (x0 < x1 or x1 > x2):
            tops.append((tuple(st[0]), tuple(st[1])))
            st = T(st); st = (st[0], [(st[1][0] + 1) % M] + st[1][1:])  # MUTANT: turnover not the exact reversal
            nxt = S(st)
        prev = X(st); st = nxt
    print("seed", trial, "ticks 20000, turnovers", len(tops),
          "distinct turnover states", len(set(tops)), "distinct states visited", len(seen))
