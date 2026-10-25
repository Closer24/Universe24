"""pc1 (2026-10-25), item 1: the carried clock against the law's letter, in integers.

Measures, at each Gamma named: the frozen content (the loader's edge); the exact clock (the oracle: the engine's clock_alone, the running fraction rounded once) over every content to the edge; each carried form's clock and Link pace against it (the count equal, the count off by one unit and where); the ties of the clock and of the Link's pace; the least margin of the exact fraction from the half (the certificate a scaled carried form needs); the width of each form's state and transient; the non-injectivity of the unit-scale recurrence (the collisions). At a Gamma whose edge is far (23,057) the oracle is the certified scaled form at 2^512 (the exact value lies within (N - 1, N + 1) at the scale, a theorem of the carried division; a content whose rounding the certificate cannot decide is counted).
Usage: python pc1_clock.py <out.json> [gammas...]
"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'toy_pc1'))
import pc1_paces
from event_universe.core import paces as engine_paces

sys.set_int_max_str_digits(0)


def exact_margins(gamma, edge):
    """The exact clock by the running fraction (the engine's letter) and, per content, the margin of the fraction from the half in units of 1 / (2 wall): the least margin and the ties."""
    numerator, wall = gamma, 1
    clocks, links, least, ties_clock, ties_link = [], [], None, 0, 0
    frac_bits = 0
    for c in range(edge + 1):
        twice = 2 * numerator
        q, rem = divmod(twice + wall, 2 * wall)  # rounded half up
        clocks.append(q)
        d = abs(2 * (numerator % wall) - wall)  # the distance of twice the fraction from the wall, in 1 / wall units; 0 at a tie
        if d == 0:
            ties_clock += 1
        if 2 * (q * q % gamma) == gamma:
            ties_link += 1
        links.append((2 * q * q + gamma) // (2 * gamma))
        # the margin as a fraction d / (2 wall): keep the least as a pair, compared by cross multiplication
        if least is None or d * least[1] < least[0] * (2 * wall):
            least = (d, 2 * wall, c)
        frac_bits = max(frac_bits, numerator.bit_length(), wall.bit_length())
        numerator, wall = numerator * (gamma - 1), wall * gamma
    return clocks, links, least, ties_clock, ties_link, frac_bits


def certified(gamma, edge, scale_bits):
    """The scaled carried clock with its certificate: at the scale S the exact S p lies in (N - 1, N + 1); the rounding to the unit is certain where (N - 1) / S and (N + 1) / S round alike. Returns the clocks, the count of undecided contents (and the first), the transient's bits."""
    S = 1 << scale_bits
    N, r = gamma * S, gamma // 2
    clocks, undecided, first, bits = [], 0, None, 0
    for c in range(edge + 1):
        lo, hi = pc1_paces.rounded_int(N - 1, S), pc1_paces.rounded_int(N + 1, S)
        clocks.append(pc1_paces.rounded_int(N, S))
        if lo != hi:
            undecided += 1
            first = c if first is None else first
        total = N * (gamma - 1) + r
        bits = max(bits, total.bit_length())
        N, r = divmod(total, gamma)
    return clocks, undecided, first, bits


def compare(oracle_clocks, oracle_links, clocks, links):
    """The counts: contents equal, off by one unit (and the first ten of them), off by more; the same for the Link's pace."""
    eq = sum(1 for a, b in zip(oracle_clocks, clocks) if a == b)
    off1 = [c for c, (a, b) in enumerate(zip(oracle_clocks, clocks)) if abs(a - b) == 1]
    offmore = [c for c, (a, b) in enumerate(zip(oracle_clocks, clocks)) if abs(a - b) > 1]
    above = sum(1 for a, b in zip(oracle_clocks, clocks) if b > a)
    below = sum(1 for a, b in zip(oracle_clocks, clocks) if b < a)
    leq = sum(1 for a, b in zip(oracle_links, links) if a == b)
    loff = [c for c, (a, b) in enumerate(zip(oracle_links, links)) if a != b]
    return {'contents': len(clocks), 'clock equal': eq, 'clock off by one': len(off1), 'clock above the letter': above, 'clock below the letter': below, 'clock off by more': len(offmore),
            'first off contents': off1[:10], 'last off content': off1[-1] if off1 else None, 'link pace equal': leq, 'link pace off': len(loff), 'link pace first off': loff[:10]}


def expected_plain_off(gamma, edge):
    """The derivation's count for the plain form, the floor of the exact plus a bias rising as (1 - lambda^c) / 2: the mismatch rate e^(-c / Gamma) / 2 summed, in integers: Gamma (1 - (1 - 1/Gamma)^edge) div 2, by the running fraction."""
    numerator, wall = (gamma - 1) ** edge, gamma ** edge
    return (gamma * (wall - numerator)) // (2 * wall)


def collisions(gamma):
    """The unit-scale recurrence T -> T - T div Gamma on the totals T in [0, Gamma^2): the count of pairs of totals with one image (the map is no bijection: a decaying clock loses states)."""
    seen, found = {}, 0
    for T in range(gamma * gamma):
        img = T - T // gamma
        if img in seen:
            found += 1
        seen[img] = T
    return found


def run(gamma, oracle_cap=4000):
    out = {'gamma': gamma}
    t0 = time.time()
    edge = engine_paces.frozen_content(gamma)
    out['frozen content (the loader edge)'] = edge
    forms = {}
    if edge <= oracle_cap:
        clocks, links, least, ties_c, ties_l, frac_bits = exact_margins(gamma, edge)
        out['oracle'] = 'the running fraction rounded once (the engine letter)'
        out['exact fraction bits at the edge'] = frac_bits
        out['clock ties (2 Gamma (Gamma-1)^c = odd Gamma^c)'] = ties_c
        out['link pace ties (2 p_0^2 = odd Gamma)'] = ties_l
        d, twowall, at = least
        out['least margin of the fraction from the half'] = {'at content': at, 'margin as 1 over': (twowall // d) if d else None, 'margin bits (below the half)': (twowall.bit_length() - d.bit_length()) if d else None}
        # cross-check the oracle against the engine's clock_alone at a few contents
        out['oracle equals engine clock_alone at 0, 1, 2, 100, edge'] = all(clocks[c] == engine_paces.clock_alone(gamma, c) for c in (0, 1, 2, min(100, edge), edge))
    else:
        clocks, undecided, first, bits = certified(gamma, edge, 512)
        links = [(2 * q * q + gamma) // (2 * gamma) for q in clocks]
        out['oracle'] = 'the certified scaled carried clock at 2^512'
        out['oracle undecided contents'] = undecided
        out['oracle first undecided'] = first
        out['oracle transient bits'] = bits
        out['oracle equals engine clock_alone at 0, 1, 2, 100'] = all(clocks[c] == engine_paces.clock_alone(gamma, c) for c in (0, 1, 2, 100))
    out['clock at the edge (oracle)'] = clocks[edge]
    out['link pace at the edge (oracle)'] = links[edge]
    for flag in ('plain', 'half', 'gamma', 'gamma2', 'scaled'):
        car = pc1_paces.Carried(flag)
        side = car.side_of(gamma, edge)
        fc, fl = side.clocks[: edge + 1], side.links[: edge + 1]
        forms[flag] = compare(clocks, links, fc, fl)
        forms[flag]['memo transient bits'] = side.max_bits
        forms[flag]['state bits (N at c = 0)'] = (gamma * car.scale_of(gamma)).bit_length()
        forms[flag]['clock at the edge'] = fc[edge]
        forms[flag]['frozen first at content (link pace 0)'] = next((c for c, v in enumerate(fl) if v == 0), None)
    out['forms'] = forms
    out['plain form: derived count off (Gamma (1 - lambda^edge) div 2)'] = expected_plain_off(gamma, edge)
    # the certificate at the derived scales: which scale decides every content
    for bits in (10, 20, 30, 40, 63):
        _c, und, first, tbits = certified(gamma, edge, bits)
        out['certified at 2^%d: undecided contents' % bits] = und
        out['certified at 2^%d: transient bits' % bits] = tbits
    # the plain recurrence with no remainder (the rounding alone) freezes
    p, c = gamma, 0
    while c < edge and pc1_paces.rounded_int(p * (gamma - 1), gamma) != p:
        p = pc1_paces.rounded_int(p * (gamma - 1), gamma); c += 1
    out['plain rounding without remainder: freezes at pace / content'] = [p, c]
    out['seconds'] = int(time.time() - t0)
    return out


if __name__ == '__main__':
    gammas = [int(g) for g in sys.argv[2:]] or [1000, 1001, 1021, 23057]
    found = {}
    for g in gammas:
        found[str(g)] = run(g)
        print(json.dumps({str(g): found[str(g)]}), flush=True)
    found['collisions at Gamma 1000 on [0, Gamma^2)'] = collisions(1000)
    found['collisions at Gamma 7 on [0, 49)'] = collisions(7)
    print(json.dumps({'collisions': [found['collisions at Gamma 1000 on [0, Gamma^2)'], found['collisions at Gamma 7 on [0, 49)']]}))
    json.dump(found, open(sys.argv[1], 'w'), indent=1)
