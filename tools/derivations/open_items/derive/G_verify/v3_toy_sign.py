"""V3 (verifier of G): a replicate of g2 part 2 (the K pair under half up) with a new random seed and more
seeds, to test whether the tie's net charge has a sign bias. g2's own functions are loaded from its file with
its three top-level calls left out. Integers only. argv: trials rng_seed."""
import random
import sys
from collections import Counter
src = open('/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/G/g2_toy.py', encoding='ascii').read()
src = src.replace('\npart1()\npart2()\npart3()\n', '\n')
ns = {}
exec(compile(src, 'g2_toy.py', 'exec'), ns)
trials, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
pool = Counter()
for w in (8, 12, 16, 20):
    sf, sl, ss = Counter(), Counter(), Counter()
    flips = 0
    for _ in range(trials):
        K = rng.randint(1, w - 1)
        amp = rng.randint(3, 40)
        n3, n12, b3, b12 = (rng.randint(-amp, amp) for _ in range(4))
        m = ns['mid_of'](w)
        A = ((b3, n3, m), (b12, n12, m))
        B = ns['conj'](A, w)
        a, bb, a2, bb2 = A, B, A, B
        up, down = [], []
        for _t in range(400):
            a, bb = ns['hand_step']('up', a, w, K), ns['hand_step']('up', bb, w, K)
            a2, bb2 = ns['hand_step']('down', a2, w, K), ns['hand_step']('down', bb2, w, K)
            up.append(ns['charge'](a) + ns['charge'](bb))
            down.append(ns['charge'](a2) + ns['charge'](bb2))
        flips += all(x == -y for x, y in zip(up, down))
        first = next((x for x in up if x), 0)
        sgn = lambda x: (x > 0) - (x < 0)
        sf[sgn(first)] += 1
        sl[sgn(up[-1])] += 1
        ss[sgn(sum(up))] += 1
    for k in (-1, 1):
        pool[('first', k)] += sf[k]; pool[('last', k)] += sl[k]; pool[('sum', k)] += ss[k]
    print(f'w {w}: first {dict(sorted(sf.items()))}; last {dict(sorted(sl.items()))}; run sum {dict(sorted(ss.items()))}; down = -up on {flips} of {trials}')
for stat in ('first', 'last', 'sum'):
    neg, pos = pool[(stat, -1)], pool[(stat, 1)]
    print(f'pooled {stat}: - {neg}, + {pos}, excess {pos - neg}, (excess)^2 * 100 / (n) = {(pos - neg) ** 2 * 100 // (pos + neg)} (z^2 in hundredths; 384 is the two-sided 5% line)')
