"""mv1 (2): the band omega(k) of every row of universe_middle at the vacuum's paces, in integers: the orbit's pair (c_n, s_n) over X at the count n (the toy's own, features/phase at Gamma: one count = arccos(1 - 1 / (2 Gamma^2)) radians, 1 / Gamma to the first order), cos omega_k = num (c_n + 2 X) / (3 den X) along an axis (2 w cos omega = S + SUM_ports R cos k, S = 0 at the vacuum), sin omega_k = largest_below(D^2 - C^2) / D, the group velocity v_g = (num / (3 den)) sin k / sin omega_k in milli-Links per interval as the quotient (1000 num s_n D) div (3 den X S_w) (p = Gamma), the fastest count per row by the scan, light's long-wavelength speed isqrt(10^6 / 3) = 577 milli, and the relativistic check omega^2 against 2 g + k^2 / 3."""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src'))
sys.set_int_max_str_digits(0)
from event_universe.core import rule3
from event_universe.features import phase
HERE = os.path.dirname(os.path.abspath(__file__))
uni = json.load(open(os.path.join(HERE, 'toy', 'universe_middle.json')))
den, gamma, T = int(uni['integers']['den']), int(uni['integers']['node_clock']), int(uni['integers']['quantum_action'])
X = phase.amplitude(phase.unit(gamma), 128 // 2 - 1)
cosine, sine = phase.seed(X, gamma)
orbit = [(int(cosine[0]), int(sine[0]))]
def pair(n):
    while len(orbit) <= n:
        global cosine, sine
        cosine, sine = phase.act(cosine, gamma, 1), phase.act(sine, gamma, 1)
        orbit.append((int(cosine[0]), int(sine[0])))
    return orbit[n]
# the edge: the last count whose sine is at or above 0
n = 1
while pair(n)[1] >= 0: n += 1
n_edge = n - 1
rows = [(k, tuple(int(x) for x in r['pair'])) for k, r in enumerate(uni['rows']) if int(r['shape']) == 2]
out = {'X': X, 'n_edge': n_edge, 'theta_0 milli-radians x 1000 (1000000 x arccos(1 - 1/(2 Gamma^2)) at Gamma 1000, derived by the orbit: n_edge against pi)': None, 'light long-wavelength speed milli-Links per interval isqrt(10^6/3)': math.isqrt(10 ** 6 // 3), 'rows': {}}
def band(num, n):
    c_n, s_n = pair(n)
    C = num * (c_n + 2 * X); D = 3 * den * X; S_w = rule3.largest_below(D * D - C * C)
    v_milli = (1000 * num * s_n * D) // (3 * den * X * S_w) if S_w > 0 else None
    return C, D, S_w, v_milli
for idx, (num, dn) in rows:
    g = den - num
    table = {}
    best = (0, 0)
    for n in (0, 100, 300, 500, 785, 1000, 1257, 1571, 2000, 2356, 2800, 3141):
        C, D, S_w, v = band(num, n)
        table[n] = {'cos omega_k x 10^6': (10 ** 6 * C) // D, 'sin omega_k x 10^6': (10 ** 6 * S_w) // D, 'v_g milli-Links/interval': v, 'v/c thousandths (c = 577)': None if v is None else (1000 * v) // 577}
    for n in range(1, n_edge + 1):
        v = band(num, n)[3]
        if v is not None and v > best[1]: best = (n, v)
    # the relativistic check at n = 785: 10^6 (1 - cos omega_k) against 10^6 (g/den + (num/den)(1 - cos k)/3) (exact by construction) and the small-angle form 10^6 (omega^2/2) ~ 10^6 (g/den + k^2/6)
    C, D, S_w, v = band(num, 785); c785 = pair(785)[0]
    out['rows'][str(idx)] = {'pair': [num, den], 'gap den - num': g, 'g x 10^9': (10 ** 9 * g) // den, 'rest cos omega_0 x 10^9': (10 ** 9 * num) // den, 'band': table, 'fastest count n and v_g milli': best,
                             'one minus cos omega at n 785, x 10^9': (10 ** 9 * (D - C)) // D, 'g/den + (num/den)(1 - cos k)/3 at n 785, x 10^9 (the band exact)': (10 ** 9 * (g * 3 * X + num * (X - c785))) // (3 * den * X), 'small-angle 2g/den + k^2/3 over 2 at n 785, x 10^9': (10 ** 9 * (2 * g * gamma * gamma * 3 + den * 785 * 785)) // (6 * den * gamma * gamma)}
json.dump(out, open(os.path.join(HERE, 'out', 'band.json'), 'w'))
print(json.dumps(out))
