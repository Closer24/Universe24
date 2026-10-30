"""David's probe: can lin's one rounding per read keep the reversal, with the tie rule's going as its home?

usage: python3 -I p7_lin_tie.py   (no worktree needed)
The read between a neighbour's before b (at tb) and now a (at tn), at u = c - tb in [0, L], L = tn - tb >= 1:
  m = b + carry((a - b) u, L, home(L, go))[0], home(L, go) = (L - go) div 2.
Under T the read must turn as the gear does: on a T-even gear (b, a) -> (a, b) and the going advanced, m' = m;
on a T-odd gear (b, a) -> (-a, -b) and the going kept, m' = -m; the moment u -> L - u.
Counted over every L from 1 to 12, every u, a - b from -40 to 40, both goings.
"""
def home(L, go):
    return (L - go) // 2


def read(b, a, u, L, go):
    return b + ((a - b) * u + home(L, go)) // L


bad = {"even": [0, 0], "odd": [0, 0]}
for L in range(1, 13):
    for u in range(0, L + 1):
        for d in range(-40, 41):
            for go in (0, 1):
                b, a = 7, 7 + d
                m = read(b, a, u, L, go)
                me = read(a, b, L - u, L, 1 - go)       # T-even: slots exchanged, going advanced
                mo = read(-a, -b, L - u, L, go)         # T-odd: exchanged and negated, going kept
                par = L % 2
                bad["even"][par] += me != m
                bad["odd"][par] += mo != -m
print("T-even, going advanced: the read turns wrong at", bad["even"][0], "cases with L even and", bad["even"][1], "with L odd")
print("T-odd, going kept:      the read turns wrong at", bad["odd"][0], "cases with L even and", bad["odd"][1], "with L odd")
