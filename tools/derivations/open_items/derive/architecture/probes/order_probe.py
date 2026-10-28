# Probe for RULING item 4: the arrivals rule, the count, the stopped clock, the slot read.
# Toy: a ring of N Node-clocks, one integer leapfrog gear with Rule3's carry, a rate dial per site.
# Not engine code: a runner-side model with ifs, for the ruling only.
import random
N, W, GAM, T = 10, 7, 5, 30
def run(rates, sched, mode, seed):
    rng = random.Random(seed)
    a = [(3*x*x+1) % 11 - 5 for x in range(N)]; b = [(5*x+2) % 7 - 3 for x in range(N)]
    r = [x % W for x in range(N)]; c = [0]*N; tb = [-1]*N; tn = [0]*N; ph = [x % GAM for x in range(N)]
    for sweep in range(40*T):
        A, B, R, C, TB, TN, PH = a[:], b[:], r[:], c[:], tb[:], tn[:], ph[:]
        for x in range(N):
            nbs = ((x-1) % N, (x+1) % N)
            due = all(C[y] >= C[x] for y in nbs) and C[x] < T
            allowed = 1 if sched == 'sync' else rng.randint(0, 1)
            if not (due and allowed): continue
            k, php = divmod(PH[x] + rates[x], GAM)
            if mode == 'as_written' and k == 0:
                ph[x] = php; continue          # no tick: the count does not advance (Sofer read literally)
            if k:
                t = C[x]
                if mode == 'by_difference':
                    vals = [A[y] if C[y] == t else B[y] for y in nbs]
                else:
                    vals = [A[y] if TN[y] <= t else B[y] for y in nbs]
                q, rp = divmod(sum(vals) - 2*A[x] + R[x], W)
                a[x], b[x], r[x] = 2*A[x] - B[x] + q, A[x], rp
                tb[x], tn[x] = TN[x], t + 1
            ph[x] = php; c[x] = C[x] + 1
        if min(c) == T: break
    return (min(c), max(c)), (a, b, r, tb, tn, ph)
full = [GAM]*N
slow = [GAM, 3, GAM, 2, GAM, GAM, 4, GAM, 1, GAM]
stop = slow[:]; stop[5] = 0
for name, rates in (('full rate', full), ('rates part', slow), ('one stopped (rate 0)', stop)):
    for mode in ('as_written', 'by_difference', 'ruled'):
        ref = run(rates, 'sync', mode, 0)
        same = sum(run(rates, 'async', mode, s)[1] == ref[1] for s in range(1, 41))
        print(f'{name:22s} {mode:14s} sync counts(min,max)={ref[0]}  async runs equal to sync at count T: {same}/40')
