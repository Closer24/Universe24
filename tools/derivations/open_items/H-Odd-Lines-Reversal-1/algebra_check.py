"""ol1's one-Node algebra check (integers only, the engine's own gram): on a 4-cube of random plane levels and velocities,
(1) the sign's current J_a = dN_a.GJ.N (gram.current) at the levels K N is -J_a at the levels N at every Node: the current is odd
under the conjugation, so the fall (whose start levels are the rise's start levels conjugated) writes -J where the rise wrote J;
(2) the kick form dN_a.GJ.U + dU_a.GJ.N summed over in and out is the same integer at (K N, -K U_out, -K U_in) as at (N, U_in, U_out):
its own mirror; (3) the velocity-form charge of PL-S1 likewise; (4) under the exchange with the frames preserved (a whole board
turning) the Link's odd part n_ij = side (n_i + n_j) of a negated odd line is negated, and the tangent turn of a conjugated pair by
(tc, -ts) is the conjugate of the turn by (tc, ts): the arrivals of the fall are the conjugate of the rise's."""
import random, sys
sys.set_int_max_str_digits(0)
import numpy as np
from event_universe import gram
from event_universe.core.ports import AXES, across
from event_universe.links import turn_pair
from event_universe.rows import zeros
random.seed(24)
shape = (4, 4, 4)
def rand(scale):
    a = zeros(shape)
    for at in np.ndindex(*shape):
        a[at] = random.randint(-scale, scale)
    return a
N = [rand(200), rand(200)]
U_in, U_out = [rand(50), rand(50)], [rand(50), rand(50)]
frames = [zeros(shape) + 1 for _ in range(6)]
K = gram.conjugation(2)
KN = gram.matvec(K, N)
J = gram.current(2, N, frames)
J_K = gram.current(2, KN, frames)
odd = all(bool(np.all(a + b == 0)) for a, b in zip(J, J_K))
gj = gram.matmul(gram.gram(2), gram.rotation(2))
def kick_form(levels, pair_of_velocities):
    found = [zeros(shape) for _ in range(AXES)]
    for u in pair_of_velocities:
        for a in range(AXES):
            dn = [across(n, 2 * a) - across(n, 2 * a + 1) for n in levels]
            du = [across(x, 2 * a) - across(x, 2 * a + 1) for x in u]
            found[a] = found[a] + gram.form(gj, dn, u) + gram.form(gj, du, levels)
    return found
A = kick_form(N, (U_in, U_out))
B = kick_form(KN, ([-x for x in gram.matvec(K, U_out)], [-x for x in gram.matvec(K, U_in)]))
even = all(bool(np.all(a == b)) for a, b in zip(A, B))
def charge_form(levels, pair_of_velocities):
    found = zeros(shape)
    for u in pair_of_velocities:
        found = found - (levels[0] * u[1] - levels[1] * u[0])
    return found
C = charge_form(N, (U_in, U_out))
D = charge_form(KN, ([-x for x in gram.matvec(K, U_out)], [-x for x in gram.matvec(K, U_in)]))
charge_even = bool(np.all(C == D))
# (4) the tangent turn: turn_pair(K z, tc, -ts) = K turn_pair(z, tc, ts) at an exact odd rounding (the rounding is odd)
wl, n = 4000, 137
tc, ts, tw = wl * wl - n * n, 2 * wl * n, wl * wl + n * n
re, im = N
t_re, t_im = turn_pair(re, im, tc, ts, tw)
k_re, k_im = turn_pair(re, -im, tc, -ts, tw)
turn_conj = bool(np.all(t_re == k_re)) and bool(np.all(t_im == -k_im))
print({"J(K N) = -J(N) at every Node and axis": odd, "kick form its own mirror": even, "PL-S1 charge form its own mirror": charge_even, "turn by (tc, -ts) of K z = K (turn of z)": turn_conj, "J at the origin": [int(j[0, 0, 0]) for j in J], "kick form at the origin": [int(a[0, 0, 0]) for a in A]})
assert odd and even and charge_even and turn_conj
print("PASS")
