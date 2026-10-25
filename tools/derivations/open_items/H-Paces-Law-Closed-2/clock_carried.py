"""pc2, item 1: the carried clock against the engine's memo, bit for bit, at Gamma 1,000 over every content to the clock's zero and on the hills to -Gamma; the three forms (K1's 2^K-scaled value, K2's carried remainder, the plain iterated rounding); the ties; the collisions of the forward act (r = Gamma - 1); the width; the group law; the one-Node test of the chain (forward of the inverse is the identity on every hill content); at the larger Gammas over the contents the records visit.
Usage: PYTHONPATH=src python tools/derivations/open_items/H-Paces-Law-Closed-2/clock_carried.py > tools/derivations/open_items/H-Paces-Law-Closed-2/out/clock_carried.txt. Integers only."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)
import pc2_paces as P
from event_universe.core import paces as E
from event_universe.core.rule3 import division_forward

out = {}


def exact_clock(gamma, c):
    return E.clock_alone(gamma, c)


def compare(gamma, contents, label):
    """The carried clock and its Link pace against the engine's memo over the contents: equal, off by one up, off by one down, off by more; where."""
    eq = up = down = more = 0; firsts = []; link_eq = link_off = 0; link_offs = []
    E.clear_memo(); P.clear_memo()
    for c in contents:
        pm = E.clock(gamma, c); pc = P.carried_clock(gamma, c)
        d = pc - pm
        if d == 0: eq += 1
        elif d == 1: up += 1
        elif d == -1: down += 1
        else: more += 1
        if d != 0 and len(firsts) < 12: firsts.append((c, pm, pc))
        lm = E.link_pace(gamma, c); lc = P.carried_link_pace(gamma, c)
        if lm == lc: link_eq += 1
        else:
            link_off += 1
            if len(link_offs) < 8: link_offs.append((c, lm, lc))
    return {'label': label, 'contents': len(contents), 'clock equal': eq, 'clock carried one above memo': up, 'clock carried one below memo': down, 'clock off by more than one': more, 'first differences (content, memo, carried)': firsts, 'link pace equal': link_eq, 'link pace off': link_off, 'first link pace differences': link_offs}


t0 = time.monotonic_ns()
gamma = 1000
zero = P.clock_zero(gamma)  # on the carried clock
E.clear_memo()
zero_memo = 0
while E.clock(gamma, zero_memo) > 0: zero_memo += 1
out['clock zero (carried, memo)'] = [zero, zero_memo]
frozen_c = P.frozen_content(gamma) if P.CARRIED else None
P.CARRIED = True; frozen_c = P.frozen_content(gamma); P.CARRIED = False
out['frozen content: the Link pace 0 first (carried, memo)'] = [frozen_c, E.frozen_content(gamma)]
out['clock at the frozen content (carried, memo)'] = [P.carried_clock(gamma, frozen_c), E.clock(gamma, E.frozen_content(gamma))]

# the hollows to the clock's zero, half-wall start
hollows = list(range(0, max(zero, zero_memo) + 1))
out['hollows 0..zero, r(0) = Gamma div 2'] = compare(gamma, hollows, 'Gamma 1000 hollows')
# the records' range (the chiral 300 run visits contents to 5,988; the 60-interval run far less)
out['hollows 0..6000'] = compare(gamma, list(range(0, 6001)), 'Gamma 1000 hollows to 6000')
# the hills to -Gamma (the floor's content)
out['hills -1..-Gamma'] = compare(gamma, list(range(-1, -gamma - 1, -1)), 'Gamma 1000 hills')

# r(0) = 0 start, for the record (K2's count)
def carried_chain(gamma, r0, n):
    p, r = gamma, r0; found = [(p, r)]
    for _ in range(n):
        p, r = P.carried_forward(gamma, p, r); found.append((p, r))
    return found
E.clear_memo()
ch0 = carried_chain(gamma, 0, 3800); diff0 = sum(1 for c in range(3794) if ch0[c][0] != E.clock(gamma, c)); first0 = next((c for c in range(3794) if ch0[c][0] != E.clock(gamma, c)), None)
chh = carried_chain(gamma, gamma // 2, 3800); diffh = sum(1 for c in range(3794) if chh[c][0] != E.clock(gamma, c)); firsth = next((c for c in range(3794) if chh[c][0] != E.clock(gamma, c)), None)
out['r(0) = 0 against the memo over 0..3793: differing, first'] = [diff0, first0]
out['r(0) = Gamma div 2 against the memo over 0..3793: differing, first'] = [diffh, firsth]

# K1's 2^K-scaled form
def scaled_chain(gamma, K, n):
    Pv, R = gamma << K, 0; found = []
    for c in range(n + 1):
        found.append(int(division_forward(Pv + Pv, 1 << (K + 1), 1 << K)[0]))
        total = (gamma - 1) * Pv + R; Pv, R = total // gamma, total % gamma
    return found
for K in (16, 32, 64):
    sc = scaled_chain(gamma, K, 7600)
    diffs = [c for c in range(7600) if sc[c] != E.clock(gamma, c)]
    out['K1 scaled form K=%d over 0..7599: differing count, first 5' % K] = [len(diffs), diffs[:5], 'bits of the scaled transient', ((gamma - 1) * (gamma << K) + gamma).bit_length()]
# the plain iterated rounding
p = gamma; plain = [p]
for c in range(4000):
    p = int(E.rounded((gamma - 1) * p, gamma)); plain.append(p)
out['plain iterated rounding: value at 500, 1000, 3793; first content where it stops falling'] = [plain[500], plain[1000], plain[3793], next((c for c in range(1, 4000) if plain[c] == plain[c - 1]), None)]

# the ties of the Link pace: 2 p^2 = Gamma mod 2 Gamma over the hollows' chain (memo and carried), and the clock values at which they fall
ties_memo = [c for c in hollows if (2 * E.clock(gamma, c) ** 2) % (2 * gamma) == gamma]
ties_carried = [c for c in hollows if (2 * P.carried_clock(gamma, c) ** 2) % (2 * gamma) == gamma]
out['Link pace ties on the chain (memo count, carried count, the clock values at the memo ties)'] = [len(ties_memo), len(ties_carried), sorted(set(E.clock(gamma, c) for c in ties_memo))]
# the carried clock has no tie: its act is a floor with the remainder; count the remainders at the half wall and the collisions r = Gamma - 1 (where the inverse act would not return the chain's state)
rems = [P.carried_pair(gamma, c)[1] for c in hollows]
collisions = [c for c in hollows if rems[c] == gamma - 1]
out['hollows: contents with r = Gamma - 1 (the forward act not injective there), count and list'] = [len(collisions), collisions]
# the one-Node test of the chain: forward(inverse(x)) = x on every hill content, inverse(forward(x)) = x on every hollow content except the collisions
fi = sum(1 for c in range(0, -gamma, -1) if P.carried_forward(gamma, *P.carried_pair(gamma, c - 1)) == P.carried_pair(gamma, c))
if_ok = [c for c in hollows[:-1] if P.carried_back(gamma, *P.carried_pair(gamma, c + 1)) == P.carried_pair(gamma, c)]
out['chain: forward of the hill inverse returns the content, count of Gamma hills'] = [fi, gamma]
out['chain: inverse of the forward returns the hollow content, count, of'] = [len(if_ok), len(hollows) - 1, 'the misses', [c for c in hollows[:-1] if c not in set(if_ok)]]
# the width: the transient's bits (Gamma - 1) p + r on the hollows and Gamma p + r on the hills; the Link pace's p^2
out['width at Gamma 1000: max bits of the carried transient (hollows, hills to -Gamma), of p^2, the memo fraction bits at 3793 and at 5988'] = [max(((gamma - 1) * P.carried_pair(gamma, c)[0] + P.carried_pair(gamma, c)[1]).bit_length() for c in hollows), max((gamma * P.carried_pair(gamma, c)[0] + P.carried_pair(gamma, c)[1]).bit_length() for c in range(0, -gamma - 1, -1)), max((P.carried_clock(gamma, c) ** 2).bit_length() for c in range(-gamma, zero + 1)), [(gamma * (gamma - 1) ** 3793).bit_length(), (gamma ** 3793).bit_length()], [(gamma * (gamma - 1) ** 5988).bit_length(), (gamma ** 5988).bit_length()]]
# the group law p(c1 + c2) against rounded(p(c1) p(c2), Gamma): the largest deviation in units, memo and carried, on a grid
dev_m = 0; dev_c = 0
for c1 in range(0, 3000, 37):
    for c2 in range(0, 3000 - c1, 53):
        dev_m = max(dev_m, abs(E.clock(gamma, c1 + c2) - int(E.rounded(E.clock(gamma, c1) * E.clock(gamma, c2), gamma))))
        dev_c = max(dev_c, abs(P.carried_clock(gamma, c1 + c2) - int(E.rounded(P.carried_clock(gamma, c1) * P.carried_clock(gamma, c2), gamma))))
out['group law deviation in units on a grid of pairs (memo, carried)'] = [dev_m, dev_c]
out['milliseconds so far'] = (time.monotonic_ns() - t0) // 1000000
# the larger Gammas over the contents the records visit (0..6000): the two Gammas K found largest within the width at the two dens, and the toy's 1,021 companion
for g in (1021, 9902, 23057):
    t1 = time.monotonic_ns()
    found = compare(g, list(range(0, 6001)), 'Gamma %d hollows to 6000' % g)
    found['hills to -Gamma'] = compare(g, list(range(-1, -g - 1, -1)), 'hills')['clock equal']
    found['carried transient bits (hollows to 6000, hills to -Gamma)'] = [max(((g - 1) * P.carried_pair(g, c)[0] + P.carried_pair(g, c)[1]).bit_length() for c in range(6001)), max((g * P.carried_pair(g, c)[0] + P.carried_pair(g, c)[1]).bit_length() for c in range(0, -g - 1, -1))]
    found['memo fraction bits at 6000'] = [(g * (g - 1) ** 6000).bit_length(), (g ** 6000).bit_length()]
    found['milliseconds'] = (time.monotonic_ns() - t1) // 1000000
    out['Gamma %d' % g] = found
for k, v in out.items(): print(json.dumps({k: v}))
