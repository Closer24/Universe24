"""V8 (verifier A): the turnover's act on one hand (acts.reverse with hands.signs [1, -1]: now' = K before, before' = K now,
K the twelve gear negated) keeps the stored sweep W = n3 b12 - n12 b3, and flips the pawl bit; so in the pawl frame
(Z = z where the bit is 0, conj z where 1) the turned clock's charge eps W changes sign.  Random integers.  python3 -I"""
import random
rng = random.Random(9)
keep = flip = n = 0
for _ in range(100000):
    n3, n12, b3, b12 = (rng.randint(-10 ** 12, 10 ** 12) for _ in range(4))
    bit = rng.randint(0, 1)
    W = n3 * b12 - n12 * b3
    N3, N12, B3, B12 = b3, -b12, n3, -n12          # the turnover: exchanged through K
    W2 = N3 * B12 - N12 * B3
    eps, eps2 = 1 - 2 * bit, 1 - 2 * (1 - bit)     # the pawl stepped once modulo its two teeth
    n += 1
    keep += W2 == W
    flip += eps2 * W2 == -(eps * W)
print(f"the stored sweep kept by the turnover: {keep} of {n}; the framed charge eps W reversed: {flip} of {n}")
