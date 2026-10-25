"""fd1's one-Node checks of the unifications and of what must not be unified, in integers: the identities on random integers with counts, the law's primitives from src (core/rule3, core/paces, features/phase).
Usage: python fd1_identities.py <universe_toy.json> <out.json>"""
import sys, os, json, random
sys.set_int_max_str_digits(0)
from event_universe.core import rule3, paces, ports
from event_universe.core.rule3 import carried_division, division_forward, rule_integers, wall_of, mass, largest_below
from event_universe.core.paces import rounded, odd_rounded, sine_den, clock_alone, frozen_content
from event_universe.features import phase

universe = json.load(open(sys.argv[1])); ints = universe['integers']
den, gamma, T, G = int(ints['den']), int(ints['node_clock']), int(ints['quantum_action']), int(ints['link_unit'])
rnd = random.Random(2026); N = 100000
def W(an, ab, bn, bb): return an * bb - bn * ab
out = {}
# (a) the one bilinear: antisymmetry, the current's F_ij + F_ji = 0, the form, the twist and the momentum's change as W
ok = {'W(b, a) = -W(a, b)': 0, 'F_ij + F_ji = 0': 0, 'form now^2 - next before = W((now, before), (next, now))': 0, 'twist = W((ub, uc)_k, (ub, uc)_k+a)': 0, 'dP = 2 num [W(d, down) - W(d, up)]': 0, 'J term re_i im_j - im_i re_j = W((re, im)_i, (re, im)_j)': 0}
for _ in range(N):
    v = [rnd.randint(-10**12, 10**12) for _ in range(12)]
    an, ab, bn, bb, nx, d_n, d_b, un, ub_, vn, vb, num = v
    ok['W(b, a) = -W(a, b)'] += (W(bn, bb, an, ab) == -W(an, ab, bn, bb))
    ok['F_ij + F_ji = 0'] += ((an * bb - ab * bn) + (bn * ab - bb * an) == 0)
    ok['form now^2 - next before = W((now, before), (next, now))'] += (an * an - nx * ab == W(an, ab, nx, an))
    ok['twist = W((ub, uc)_k, (ub, uc)_k+a)'] += (un * vb - vn * ub_ == W(un, ub_, vn, vb))
    ok['dP = 2 num [W(d, down) - W(d, up)]'] += (2 * num * (d_n * (ab - bb) + d_b * (bn - an)) == 2 * num * (W(d_n, d_b, an, ab) - W(d_n, d_b, bn, bb)))
    ok['J term re_i im_j - im_i re_j = W((re, im)_i, (re, im)_j)'] += (an * bb - ab * bn == W(an, ab, bn, bb))
out['(a) the one bilinear, of %d random cases' % N] = ok
# (b) rotate = shift o write: (w a + X) div w = a + X div w, the same remainder; and backward
w = wall_of(den, gamma, G); okb = {'forward (w a + X + r) div w = a + (X + r) div w, same remainder': 0, 'write as rotate: S = E, before 0, flux N': 0, 'rotate forward through write(t - w a) then shift': 0}
for _ in range(N):
    a, X, r = rnd.randint(-10**20, 10**20), rnd.randint(-10**30, 10**30), rnd.randint(0, w - 1)
    q1, r1 = carried_division(w * a + X, w, r, 1); q2, r2 = carried_division(X, w, r, 1)
    okb['forward (w a + X + r) div w = a + (X + r) div w, same remainder'] += (q1 == a + q2 and r1 == r2)
    E = rnd.choice([T, 54 * den * T * gamma ** 2, 2]); x, Nn, wr = rnd.randint(-10**15, 10**15), rnd.randint(-10**25, 10**25), rnd.randint(0, E - 1)
    qw, rw = carried_division(Nn, E, wr, 1)  # the write: x' = x + qw
    qr, rr = carried_division(E * x - E * 0 + Nn, E, wr, 1)  # the rotate with S = E, the before 0, the flux N: quotient = x'
    okb['write as rotate: S = E, before 0, flux N'] += (qr == x + qw and rr == rw)
    S, bfr, m = rnd.randint(-10**22, 10**22), rnd.randint(-10**15, 10**15), rnd.randint(-10**25, 10**25)
    t = S * a - w * bfr + m; q_rot, r_rot = carried_division(t, w, r, 1); q_wr, r_wr = carried_division(t - w * a, w, r, 1)
    okb['rotate forward through write(t - w a) then shift'] += (q_rot == a + q_wr and r_rot == r_wr)
out['(b) rotate and write share the one division, of %d random cases' % N] = okb
# (c) the phase line's act is Rule3's line with no Links: features/phase.act against the carried division of 2 K0 now - D before at the wall D
D = phase.D(gamma); K0 = phase.K0(gamma); X = phase.amplitude(phase.unit(gamma), 63)
pair = phase.seed(X, gamma); c, s = pair; eq = 0; acts = 3000
for _ in range(acts):
    c2, s2 = phase.act(c, gamma, 1), phase.act(s, gamma, 1)
    qc, rc = carried_division(2 * K0 * c[0] - D * c[1], D, c[2], 1); qs, rs = carried_division(2 * K0 * s[0] - D * s[1], D, s[2], 1)
    eq += (c2 == (qc, c[0], rc) and s2 == (qs, s[0], rs)); c, s = c2, s2
out['(c) the phase line act = rotate with S = 2 K0, wall D, no Links (acts equal of %d)' % acts] = eq
# (d) the carried clock (K-S4, toys-5's reach) is Rule3's line with no Links, the before term 0: rule3(flux 0, mass Gamma + 1, wall Gamma, now p, other 0, r)
fz = frozen_content(gamma); p, carry = gamma, division_forward(gamma, 2, 0)[0]; eqd = 0; differs_exact = 0; first_diff = None
for cnt in range(fz + 1):
    exact = clock_alone(gamma, cnt)
    if p != exact:
        differs_exact += 1
        if first_diff is None: first_diff = (cnt, p, exact)
    q1, r1 = division_forward(p * (gamma - 1), gamma, carry)
    q2, r2 = rule3.rule3(0, gamma + 1, gamma, p, 0, carry, 1)
    eqd += (q1 == q2 and r1 == r2); p, carry = int(q1), int(r1)
out['(d) the carried clock as Rule3 line (no Links, before 0, D = Gamma + 1, w = Gamma)'] = {'contents': fz + 1, 'equal': eqd, 'carried clock differs from the exact rounded power at contents': differs_exact, 'first difference (content, carried, exact)': first_diff, 'frozen content': fz}
# (e) the odd rounding against the half up: they part at the negative ties alone
ties_neg = 0; ties_pos = 0; differ = 0; span = range(-4 * gamma, 4 * gamma + 1)
for x in span:
    a1, a2 = int(rounded(x, gamma)), int(odd_rounded(x, gamma))
    differ += (a1 != a2)
    if (2 * x) % (2 * gamma) == gamma: ties_neg += (x < 0); ties_pos += (x > 0)
out['(e) odd_rounded against rounded over [-4 Gamma, 4 Gamma]'] = {'differ': differ, 'negative ties': ties_neg, 'positive ties': ties_pos, 'the difference at a negative tie (one unit)': int(odd_rounded(-(gamma // 2) if gamma % 2 == 0 else -gamma, gamma)) - int(rounded(-(gamma // 2) if gamma % 2 == 0 else -gamma, gamma))}
# (f) the complement at the wall against the half-wall origin, and the two's complement
oke = {'w - 1 - (w div 2) against w div 2': (w - 1 - w // 2) - (w // 2), 'ones complement commutes with the floor: of': 0, 'ones complement commutes': 0, 'twos complement fails where w | u: of': 0, 'twos complement fails': 0}
for _ in range(N):
    u = rnd.randint(-10**30, 10**30)
    if rnd.randint(0, 1) == 1: u = u - u % w  # a coin by integers, half the cases at a multiple of the wall
    oke['ones complement commutes with the floor: of'] += 1; oke['ones complement commutes'] += ((w - 1 - u) // w == -(u // w))
    if u % w == 0: oke['twos complement fails where w | u: of'] += 1; oke['twos complement fails'] += ((w - u) // w != -(u // w))
out['(f) the mirror of the carry'] = oke
# (g) the units: the massless unit is the unit of the pair (0, den), 3 T den sin(pi / 2)
lifts = [tuple(int(x) for x in r['pair']) for r in universe['rows'] if int(r['shape']) == 2 and int(r['pair'][0]) != int(r['pair'][1])]
out['(g) the units'] = {'sine_den(0, den) == den': sine_den(0, den) == den, '3 T sine_den(0, den) == 3 den T (W_c)': 3 * T * sine_den(0, den) == 3 * den * T, 'lifts: 3 T sine_den(num, den) == largest_below(9 T^2 (den^2 - num^2))': [3 * T * sine_den(nm, dn) == largest_below(9 * T * T * (dn * dn - nm * nm)) for nm, dn in lifts], 'lifts: den^2 - num^2 a square': [largest_below(dn * dn - nm * nm) ** 2 == dn * dn - nm * nm for nm, dn in lifts]}
# (h) the wall identity and the vacuum
okh = {'2 w = S + D + sum R at random paces': 0, 'S = 0 at the vacuum for every pair': 0, '6 R = 2 w for num = den at the vacuum': 0}
for _ in range(N // 10):
    nm = rnd.randint(0, den); p0 = rnd.randint(1, gamma); pc = rnd.randint(1, gamma); fac = tuple(rnd.randint(0, G * G) for _ in range(6))
    r = rule_integers(nm, den, gamma, p0, pc, fac, G)
    okh['2 w = S + D + sum R at random paces'] += (2 * r.wall == r.self_coefficient + r.mass + sum(r.reaches))
    rv = rule_integers(nm, den, gamma, gamma, gamma, None, G); okh['S = 0 at the vacuum for every pair'] += (rv.self_coefficient == 0)
rl = rule_integers(den, den, gamma, gamma, gamma, None, G); okh['6 R = 2 w for num = den at the vacuum'] = (sum(rl.reaches) == 2 * rl.wall and rl.mass == 0)
out['(h) the wall is the line coefficient sum, of %d random rules' % (N // 10)] = okh
# (i) the swap on a plane: W odd under T0 (the exchange), odd under C (the conjugation), even under C T0
oki = {'W(T0 z) = -W(z)': 0, 'W(C z) = -W(z)': 0, 'W(C T0 z) = W(z)': 0}
for _ in range(N):
    rn, rb, inw, ib = [rnd.randint(-10**12, 10**12) for _ in range(4)]
    w0 = W(rn, rb, inw, ib)
    oki['W(T0 z) = -W(z)'] += (W(rb, rn, ib, inw) == -w0); oki['W(C z) = -W(z)'] += (W(rn, rb, -inw, -ib) == -w0); oki['W(C T0 z) = W(z)'] += (W(rb, rn, -ib, -inw) == w0)
out['(i) the swap is C T0 on a plane, of %d random cases' % N] = oki
json.dump(out, open(sys.argv[2], 'w'), indent=1); print(json.dumps(out, indent=1))
