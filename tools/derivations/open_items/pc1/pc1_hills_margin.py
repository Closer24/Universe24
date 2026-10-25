"""pc1: (a) the hills' side (c < 0) of every carried form against the letter (clock_alone) at Gamma 1,000 over c = -1 .. -300 (the records visit -65); (b) the least margin of the exact fraction from the half at Gamma 23,057 over every admitted content, read from the certified carried clock at 2^512 (the exact S p lies within (N - 1, N + 1): the margin is known to 2^-511).
Usage: python pc1_hills_margin.py <out.json>"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'toy_pc1'))
import pc1_paces
from event_universe.core import paces as engine_paces
sys.set_int_max_str_digits(0)
out = {}
gamma = 1000
for flag in ('plain', 'half', 'gamma', 'gamma2', 'scaled'):
    car = pc1_paces.Carried(flag)
    eq = off = 0; firsts = []
    for c in range(-1, -301, -1):
        letter = engine_paces.clock_alone(gamma, c); got = car.clock(gamma, c)
        if letter == got: eq += 1
        else:
            off += 1
            if len(firsts) < 8: firsts.append([c, got, letter])
    out['hills %s' % flag] = {'contents -1..-300 equal': eq, 'off': off, 'first off [c, form, letter]': firsts, 'memo bits': car.memo_bits(gamma), 'clock at -300 (form, letter)': [car.clock(gamma, -300), engine_paces.clock_alone(gamma, -300)]}
# the least margin at Gamma 23,057 from the certified clock at 2^512
g = 23057; edge = engine_paces.frozen_content(g); S = 1 << 512
N, r = g * S, g // 2
least = None
for c in range(edge + 1):
    frac = N % S  # S p = N + e with |e| < 1: the fraction's distance from the half, |2 frac - S| / (2 S), known within 2^-511
    d = abs(2 * frac - S)
    if least is None or d < least[0]:
        least = (d, c)
    N, r = divmod(N * (g - 1) + r, g)
d, c = least
out['Gamma 23057: least margin of the fraction from the half'] = {'at content': c, 'margin bits below the half': (S.bit_length() - d.bit_length()) if d else None, 'margin as 1 over': ((2 * S) // d) if d else None, 'edge': edge}
json.dump(out, open(sys.argv[1], 'w'), indent=1)
print(json.dumps(out))
