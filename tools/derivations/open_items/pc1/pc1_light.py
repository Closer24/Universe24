"""pc1, item 2: light's click in the record, measured on the flagged toy copy (the clock's form from PC1_CLOCK; the question is independent of it).

(a) On a world run in-process: per interval, the massless plane's share per Node at the vacuum's weight in units of its quantum W_c = 3 den T (the share div W_c and the remainder's thousandths), the largest over the board, the count of Nodes at or above one whole quantum, the count of Nodes whose massless re line crosses zero upward (the one condition the law's close needs beside the whole quantum: a period of upward crossings); the births' takes in light's quanta (the fall div W_c) and the bodies' closes' takes; every credit line's kind counted.
(b) The one-place reading of gate 10: a world of two bodies of one lift at different counts (different wells) with a detector at each body's centre and one far off, the light credits at the detectors (the toy's reading of light's whole quanta rising at the Node) with their proper counts; the spacing of each detector's credits in its own proper count against the clocks' ratio p_0(c_A) / p_0(c_B) at the credits' contents.
Usage: python pc1_light.py <world.json> <intervals> <out.json>
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'toy_pc1'))
import numpy as np
import lean_full
from lean_full import Lean, load_world

sys.set_int_max_str_digits(0)


def thousandths(a, b):
    return (1000 * a) // b


def run(path, intervals):
    universe, world = load_world(path)
    b = Lean(universe, world)
    massless = b.row(2, gap=0)
    unit = b.unit_gap0
    out = {'world': os.path.basename(path), 'intervals': intervals, 'W_c (3 den T)': unit, 'drift per Node': b.drift, 'flag': lean_full.paces.flag}
    per_interval = []
    max_share_units, max_share_thousandths, nodes_whole_total, upward_total, upward_whole_total = 0, 0, 0, 0, 0
    for t in range(intervals):
        c = b.content(); factors = b.link_factors(); rule = b.rule_of(massless, c, factors); b.start_content = c
        pace = lean_full.paces.link_pace_of(b.gamma, c)
        re, im = massless.lines
        share = b.share(re, rule, pace, vacuum=True) + b.share(im, rule, pace, vacuum=True)
        flat = [int(x) for x in share.reshape(-1)]
        top = max(flat)
        whole = sum(1 for x in flat if x >= unit)
        up = np.vectorize(lambda bb, n: 1 if (int(bb) < 0 <= int(n)) else 0, otypes=[object])(re.before, re.now)
        up_n = int(sum(int(x) for x in up.reshape(-1)))
        up_whole = int(sum(1 for x, u in zip(flat, up.reshape(-1)) if int(u) == 1 and x >= unit))
        if top // unit > max_share_units or (top // unit == max_share_units and thousandths(top % unit, unit) > max_share_thousandths):
            max_share_units, max_share_thousandths = top // unit, thousandths(top % unit, unit)
        nodes_whole_total += whole; upward_total += up_n; upward_whole_total += up_whole
        if t < 3 or (t + 1) % max(1, intervals // 12) == 0:
            per_interval.append({'i': t + 1, 'max share units': top // unit, 'max share remainder thousandths': thousandths(top % unit, unit), 'nodes at or above one quantum': whole, 'nodes with an upward crossing of the massless re line': up_n, 'light re min/max': [min(int(x) for x in re.now.reshape(-1)), max(int(x) for x in re.now.reshape(-1))], 'light im abs max': max(abs(int(x)) for x in im.now.reshape(-1))})
        b.step()
    out['max massless share over the run (units, remainder thousandths)'] = [max_share_units, max_share_thousandths]
    out['node-intervals at or above one quantum'] = nodes_whole_total
    out['node-intervals with an upward crossing of the massless re line'] = upward_total
    out['node-intervals with both (the close condition for light)'] = upward_whole_total
    out['per interval'] = per_interval
    births = [e for e in b.log if e['event'] == 'birth']
    credits = [e for e in b.log if e['event'] == 'credit']
    detectors = [e for e in b.log if e['event'] == 'detector']
    out['counts'] = {k: str(v) for k, v in b.counts.items()}
    out['births'] = len(births)
    out['births: light taken in quanta of W_c (fall div W_c, remainder thousandths) per birth, first 16'] = [[e['taken'] // unit, thousandths(e['taken'] % unit, unit), e['booked'] // unit, thousandths(e['booked'] % unit, unit)] for e in births[:16]]
    out['births: light taken total in quanta'] = [sum(e['taken'] for e in births) // unit, thousandths(sum(e['taken'] for e in births) % unit, unit)] if births else None
    out['body credits'] = len(credits)
    out['body credits: light taken per close in thousandths of W_c (min, max)'] = [min(thousandths(e['taken'], unit) for e in credits), max(thousandths(e['taken'], unit) for e in credits)] if credits else None
    out['body credits: light taken total in quanta'] = [sum(e['taken'] for e in credits) // unit, thousandths(sum(e['taken'] for e in credits) % unit, unit)] if credits else None
    out['body credits on the massless plane (line index of light)'] = sum(1 for e in credits if e['line'] == b.records().index(massless))
    out['light credits (detector lines)'] = len(detectors)
    # (b) the one-place dilation through the detectors
    if b.detectors:
        rows = {}
        for det in b.detectors:
            mine = [e for e in detectors if tuple(e['node']) == det]
            props = [e['proper'] for e in mine]
            gaps = [q - p for p, q in zip(props, props[1:])]
            contents = [e['content'] for e in mine]
            rows[str(det)] = {'light credits': len(mine), 'quanta': sum(e['quanta'] for e in mine), 'proper at the credits': props[:12], 'spacings in proper': gaps[:12], 'contents at the credits': contents[:12], 'clock p_0 at the credits': [int(lean_full.paces.clock_of(b.gamma, c_)) for c_ in contents[:12]], 'content at the end': int(b.content()[det]), 'proper at the end': int(b.proper[det])}
        out['detectors'] = rows
        # the clocks' ratio against the spacings' ratio, for every pair of detectors with two or more credits
        pairs = {}
        dets = list(rows)
        for i in range(len(dets)):
            for j in range(i + 1, len(dets)):
                A, B = rows[dets[i]], rows[dets[j]]
                if A['spacings in proper'] and B['spacings in proper']:
                    sa, sb = sorted(A['spacings in proper'])[len(A['spacings in proper']) // 2], sorted(B['spacings in proper'])[len(B['spacings in proper']) // 2]
                    ca, cb = A['clock p_0 at the credits'][0], B['clock p_0 at the credits'][0]
                    pairs['%s / %s' % (dets[i], dets[j])] = {'middle spacing A, B': [sa, sb], 'spacing ratio B over A (thousandths)': thousandths(sb, sa), 'clock ratio p_0(A) over p_0(B) (thousandths)': thousandths(ca, cb)}
        out['one-place dilation pairs'] = pairs
    return out


if __name__ == '__main__':
    found = run(sys.argv[1], int(sys.argv[2]))
    json.dump(found, open(sys.argv[3], 'w'), indent=1)
    print(json.dumps({k: v for k, v in found.items() if k != 'per interval'}))
    for row in found['per interval']:
        print(json.dumps(row))
