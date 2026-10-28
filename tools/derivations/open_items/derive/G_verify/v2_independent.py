"""V2 (verifier of G): independent re-derivations in integers only (python -I); no engine but the head's
rates.rounded. Each part prints its count and a mutant that must fail.
A  Lemma 2: rounded(2p+1, 2tX) = (p + tX/2) div tX at even tX (exhaustive); mutant odd tX.
B  Lemma 4, S7: G^2 m^2 = Gamma^2/2 (mod Gamma^2) never, any even Gamma, any G; mutant 2 m^2.
C  Lemma 4, S5: -c N = rim c/2 (mod rim c) never at odd rim, even c; mutant even rim.
D  Toy with a NONLINEAR odd force F(n) = -(3 n + n^3): C_c commutes, T_c involution, T_c S T_c = S^-1,
   Theorem 3 (S_down C0 = C0 S_up), the carried mirror's involution failures; mutant: an even force."""
import sys
S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src']
from event_universe.core import rates

# A
cases = bad = 0
for tX in range(2, 66, 2):
    for p in range(-4 * tX, 4 * tX + 1):
        cases += 1
        bad += int(rates.rounded(2 * p + 1, 2 * tX)) != (p + tX // 2) // tX
mbad = sum(int(rates.rounded(2 * p + 1, 2 * tX)) != (p + tX // 2) // tX
           for tX in range(3, 65, 2) for p in range(-4 * tX, 4 * tX + 1))
print(f'A: {cases} cases at even tX, {bad} failures; mutant odd tX: {mbad} failures')

# B
ties = cases = 0
for gam in range(2, 130, 2):
    w = gam * gam
    for G in range(1, 9):
        for m in range(-2 * gam, 2 * gam + 1):
            cases += 1
            ties += (G * G * m * m) % w == w // 2
mt = sum((2 * m * m) % (g * g) == (g * g) // 2 for g in range(2, 130, 2) for m in range(0, 2 * g))
print(f'B: {cases} cases, {ties} ties; mutant 2 m^2: {mt} ties')

# C
ties = cases = 0
for rim in range(1, 61, 2):
    for c in range(2, 42, 2):
        w = rim * c
        for N in range(-300, 301):
            cases += 1
            ties += (-c * N) % w == w // 2
mt = sum((-c * N) % (rim * c) == (rim * c) // 2 for rim in range(2, 62, 2) for c in range(2, 42, 2) for N in range(-300, 301))
print(f'C: {cases} cases, {ties} ties; mutant even rim: {mt} ties')

# D
def q(rule, p, w):
    m = w // 2
    q0, s = divmod(p + m, w)
    tie = w % 2 == 0 and s == 0
    if tie and rule == 'down':
        return q0 - 1
    if tie and rule == 'even' and q0 % 2:
        return q0 - 1
    return q0

def step(rule, x, w, F):
    b, n, r = x
    p = w * (n - b) + r - w // 2 + F(n)
    v = q(rule, p, w)
    return (n, n + v, p - w * v + w // 2)

def states(rule, w, R):
    out = []
    for b in range(-R, R + 1):
        for n in range(-R, R + 1):
            v = n - b
            rr = {'up': range(0, w), 'down': range(1, w + 1), 'even': range(0, w + 1)}[rule]
            for r in rr:
                if rule == 'even' and r in (0, w) and (w % 2 or v % 2):
                    continue
                if rule == 'even' and w % 2 and r == w:
                    continue
                out.append((b, n, r))
    return out

def back(rule, x, w, F):
    b, n, r = x
    P = w * (n - b) + r - w // 2
    Pm = P - F(b)
    v = q(rule, Pm, w)
    return (b - v, b, Pm - w * v + w // 2)

R = 6
odd_F = lambda n: -(3 * n + n ** 3)
even_F = lambda n: -(n * n)
for F, tag in ((odd_F, 'odd force'), (even_F, 'mutant even force')):
    for w in (6, 8, 10, 12, 9):
        line = []
        for rule, two_c in (('up', -1), ('even', 0), ('down', 1)):
            Cc = lambda x: (-x[0], -x[1], w + two_c - x[2])
            Tc = lambda x: (x[1], x[0], w + two_c - x[2])
            st = states(rule, w, R)
            fc = sum(Cc(step(rule, x, w, F)) != step(rule, Cc(x), w, F) for x in st)
            fi = sum(Tc(Tc(x)) != x for x in st)
            ft = sum(Tc(step(rule, Tc(x), w, F)) != back(rule, x, w, F) for x in st)
            fb = sum(step(rule, back(rule, x, w, F), w, F) != x for x in st)
            line.append(f'{rule}: C {fc} inv {fi} TST {ft} S(S^-1) {fb} of {len(st)}')
        C0 = lambda x: (-x[0], -x[1], w - x[2])
        th3 = sum(step('down', C0(x), w, F) != C0(step('up', x, w, F)) for x in states('up', w, R))
        def carried(rule, x):
            b, n, r = x
            P = w * (n - b) + r - w // 2
            v = q(rule, -P, w)
            return (b - v, b, -P - w * v + w // 2)
        cu = sum(carried('up', carried('up', x)) != x for x in states('up', w, R))
        r0 = sum(x[2] == 0 for x in states('up', w, R)) if w % 2 == 0 else 0
        ce = sum(carried('even', carried('even', x)) != x for x in states('even', w, R))
        print(f'D {tag} w {w}: ' + '; '.join(line) + f'; Thm3 failures {th3}; carried mirror up: not involutive at {cu} (states at r = 0: {r0}); even: {ce}')
