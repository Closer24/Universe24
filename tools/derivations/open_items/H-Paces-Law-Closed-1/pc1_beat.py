"""pc1, item 3: the beat against the proper clock, on a record's credit lines, in integers.

The law (The clock near matter; The paces compose): a record at rest at a Node of content c rotates by cos omega_c = 1 - (1 - num/den) (p_0(c)/Gamma)^2 per board interval, exact in the rationals: 2 cos omega_c = (2 den Gamma^2 - 2 (den - num) p_0^2) / (den Gamma^2). The beat the record carries is the count of board intervals between two upward zero crossings of its re line: predicted here by the law's own line, x_(n+1) = 2 cos omega_c x_n - x_(n-1) in exact rationals from the rest start (x_0 = 1, x_1 = cos omega_c), the intervals between upward crossings counted over 12 periods (the period's floor and ceiling and their counts: the beat a record carries is one of the two). Beside it the small-angle form, omega_c = omega_0 N (N = p_0 / Gamma), as a thousandths ratio: 2 sin(omega_c / 2) over 2 sin(omega_0 / 2) is exactly N (the clause of the same clock and the same ruler), and omega_c / omega_0 differs from N by the gap's term (the period measured in board intervals divided by the vacuum's period is omega_0 / omega_c, not 1 / N).
For every credit: the content, the measured beat, the predicted beats at that content (the exact line), the clock N in thousandths, the beat ratio vacuum/beat in thousandths; the counts of credits whose measured beat is one of the predicted two.
Usage: python pc1_beat.py <record.json> <out.json>
"""
import sys, os, json
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'toy_pc1'))
from event_universe.core import paces as engine_paces
from event_universe.core.rule3 import largest_below

sys.set_int_max_str_digits(0)


def periods(num, den, gamma, p0, periods_counted=12, step_cap=6000):
    """The intervals between upward zero crossings of the law's line at rest at the clock p0, exact in integers: x_n = y_n / q^n with q = den Gamma^2 and 2 cos omega = p / q, p = 2 den Gamma^2 - 2 (den - num) p0^2, so y_(n+1) = p y_n - q^2 y_(n-1), y_0 = 1, y_1 = p div 2 (p even), the signs of y the signs of x; returns the Counter of the spacings over the periods counted (or the step cap)."""
    q = den * gamma * gamma; p = 2 * den * gamma * gamma - 2 * (den - num) * p0 * p0
    y_prev, y = 1, p // 2
    last_up, spacings, n = None, Counter(), 1
    while sum(spacings.values()) < periods_counted and n < step_cap:
        y_next = p * y - q * q * y_prev
        if y < 0 <= y_next:
            if last_up is not None:
                spacings[n + 1 - last_up] += 1
            last_up = n + 1
        y_prev, y = y, y_next
        n += 1
    return spacings


def sine_den(num, den):
    return largest_below(den * den - num * num)


def main(record_path, out_path):
    R = json.load(open(record_path))
    gamma, den = R['gamma'], R['den']
    planes = [int(p) for p in R['planes']]
    credits = [e for e in R['log'] if e['event'] == 'credit']
    out = {'record': os.path.basename(record_path), 'gamma': gamma, 'den': den, 'credits': len(credits)}
    # the vacuum beats of every plane row
    vac = {}
    for k, num in enumerate(planes):
        if num == den:
            vac[k] = {'pair': 'massless', 'period': 'none: the drift is a double root, no crossing'}
            continue
        sp = periods(num, den, gamma, gamma)
        s = sine_den(num, den)
        vac[k] = {'num': num, 'g = (den - num)/den thousandths': (1000 * (den - num)) // den, 'den sin omega_0 (integer sine)': s, 'vacuum periods (spacing: count over 40)': dict(sp)}
    out['vacuum beats per plane'] = vac
    rows = []
    hit, miss = 0, 0
    by_content = {}
    for e in credits:
        k, c, beat = e['line'], e['content'], e['beat']
        num = planes[k]
        p0 = engine_paces.clock_alone(gamma, c)
        key = (k, c)
        if key not in by_content:
            by_content[key] = periods(num, den, gamma, p0)
        sp = by_content[key]
        predicted = sorted(sp)
        ok = beat in sp
        hit += ok; miss += (not ok)
        vac_period = sorted(periods(num, den, gamma, gamma))[0]
        rows.append({'i': e['i'], 'node': e['node'], 'line': k, 'content': c, 'p_0': p0, 'N thousandths': (1000 * p0) // gamma, 'beat measured': beat, 'beats predicted (spacing: count)': dict(sp), 'measured among predicted': ok, 'beat ratio vacuum period over measured beat (thousandths)': (1000 * vac_period) // beat if beat else None, 'proper': e['proper']})
    out['credits with the measured beat among the law line predicted spacings'] = hit
    out['credits with the measured beat outside them'] = miss
    out['beats measured (beat: count)'] = dict(Counter(e['beat'] for e in credits))
    out['contents at the credits (min, max)'] = [min(e['content'] for e in credits), max(e['content'] for e in credits)] if credits else None
    out['rows (first 40)'] = rows[:40]
    # the beat's dilation factor against the clock's at the credits' contents: omega_c / omega_0 against N, by the exact periods (integer counts)
    table = []
    for c in sorted({e['content'] for e in credits})[:: max(1, len({e['content'] for e in credits}) // 12)]:
        for k in sorted({e['line'] for e in credits}):
            num = planes[k]; p0 = engine_paces.clock_alone(gamma, c)
            sp = periods(num, den, gamma, p0, 12); mean_num = sum(s * n for s, n in sp.items()); mean_den = sum(sp.values())
            spv = periods(num, den, gamma, gamma, 12); vnum = sum(s * n for s, n in spv.items()); vden = sum(spv.values())
            table.append({'line': k, 'content': c, 'N thousandths': (1000 * p0) // gamma, 'mean period at c (thousandths of an interval)': (1000 * mean_num) // mean_den, 'mean vacuum period (thousandths)': (1000 * vnum) // vden, 'omega_c over omega_0 (thousandths) = vacuum period over period at c': (1000 * vnum * mean_den) // (vden * mean_num)})
    out['the beat factor against the clock factor at the credits contents'] = table
    json.dump(out, open(out_path, 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ('rows (first 40)',)}))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
