"""mv2's measurement driver on the flagged copy (lean_mv2.py): the world run N intervals, per interval the readings of every plane record
(the share-weighted position along each axis, unwrapped on the torus from the peak; the peak Node and its share; the lattice momentum
P_a = 2 num SUM_i SUM_lines (now_(i+a) before_i - now_i before_(i+a)) over the board; the Wronskian's board sum), the content at the peak,
the counts, the census (integers, bits), then the run back of every interval compared bit for bit by the state's hash; the lay lines, the
births and the credits of the log kept with their momentum readings. Integers only (every position in milli-Links, a quotient).
Usage: python measure.py <world.json> <out.json> [intervals] [noback]"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from lean_mv2 import Lean, load_world, wronskian

sys.set_int_max_str_digits(0)


def momentum(b, lines, num):
    """P_a over the board for a record's lines: 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) summed over the lines (The lattice momentum), a reading, no division."""
    found = []
    for a in range(3):
        total = 0
        for l in lines:
            up_now = np.roll(l.now, -1, axis=a); up_before = np.roll(l.before, -1, axis=a)
            total += int(sum(int(x) for x in (up_now * l.before - l.now * up_before).reshape(-1)))
        found.append(2 * num * total)
    return found


def positions(b, rec):
    """The record's share at the vacuum's weight at every Node (re + im), its peak Node, and its position per axis as the peak plus the share-weighted mean of the offsets within the half torus about the peak, in milli-Links (a quotient)."""
    r_ = b.records()[rec]; c = b.content(); factors = b.link_factors(); r = b.rule_of(r_, c, factors)
    re, im = r_.lines
    sh = b.share(re, r, vacuum=True) + b.share(im, r, vacuum=True)
    flat = [int(x) for x in sh.reshape(-1)]
    total = sum(flat)
    if total <= 0: return sh, None, [None, None, None], 0
    peak = tuple(int(x) for x in np.unravel_index(int(np.argmax(np.array(flat, dtype=object))), b.shape))
    pos = []
    half = b.cube // 2
    for a in range(3):
        moment = 0
        for node in np.ndindex(*b.shape):
            d = (node[a] - peak[a] + half) % b.cube - half
            moment += d * int(sh[node])
        pos.append(1000 * peak[a] + (1000 * moment) // total)
    return sh, peak, pos, total


def unwrap(prev, now, cube):
    """The position carried across the torus's seam: the step from the previous reading taken within the half torus."""
    if prev is None or now is None: return now
    step = ((now - prev) + 500 * cube) % (1000 * cube) - 500 * cube
    return prev + step


def main():
    universe, world = load_world(sys.argv[1]); out = sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != 'noback' else int(world['intervals'])
    back = 'noback' not in sys.argv
    t0 = time.monotonic_ns()
    b = Lean(universe, world)
    recs = [k for k, r in enumerate(b.records()) if any(int(x) != 0 for l in r.lines for x in l.now.reshape(-1))]
    rows = []
    unwrapped = {rec: [None, None, None] for rec in recs}
    hashes = []

    def reading(i):
        row = {'i': i, 'content max': int(max(int(x) for x in b.content().reshape(-1))), 'records': {}}
        for rec in recs:
            r_ = b.records()[rec]; num = r_.pair[0]
            sh, peak, pos, total = positions(b, rec)
            for a in range(3): unwrapped[rec][a] = unwrap(unwrapped[rec][a], pos[a], b.cube)
            W = int(sum(int(x) for x in wronskian(*r_.lines).reshape(-1)))
            row['records'][rec] = {'peak': peak, 'peak share': None if peak is None else int(sh[peak]), 'share total': total, 'quanta (share div unit)': total // b.units[rec], 'position milli': list(pos), 'unwrapped milli': list(unwrapped[rec]),
                                   'P': momentum(b, r_.lines, num), 'W total': W, 'content at peak': None if peak is None else int(b.content()[peak])}
        row['counts'] = dict(b.counts)
        row['census (integers, bits)'] = list(b.census())
        row['max transient bits'] = b.max_transient
        return row

    rows.append(reading(0))
    for t in range(n):
        if back: hashes.append(b.state_hash())
        b.step()
        rows.append(reading(b.interval))
        if b.interval % 10 == 0: print('interval', b.interval, 'ms', (time.monotonic_ns() - t0) // 1000000, flush=True)
    log = list(b.log)
    run_back = None
    if back:
        exact = 0; first_bad = None
        for k in range(n):
            b.step_back()
            if b.state_hash() == hashes[n - 1 - k]: exact += 1
            elif first_bad is None: first_bad = n - 1 - k
        run_back = {'intervals': n, 'exact': exact, 'first mismatch': first_bad}
    result = {'world': world, 'den': b.den, 'cube': b.cube, 'intervals': n, 'units': {k: b.units[k] for k in recs}, 'pairs': {k: list(b.records()[k].pair) for k in recs}, 'rows': rows, 'run_back': run_back,
              'lays': [e for e in log if e['event'] == 'lay'], 'births': [e for e in log if e['event'] == 'birth'], 'credits': [e for e in log if e['event'] == 'credit'],
              'refused': {cause: sum(1 for e in log if e['event'] == 'refused' and e['cause'] == cause) for cause in ('stop', 'origin', 'lay', 'orientation', 'twist')},
              'milliseconds': (time.monotonic_ns() - t0) // 1000000}
    json.dump(result, open(out, 'w'))
    first, last = rows[0], rows[-1]
    for rec in recs:
        p0, p1 = first['records'][rec]['unwrapped milli'], last['records'][rec]['unwrapped milli']
        v = [None if (a0 is None or a1 is None) else ((a1 - a0) // n) for a0, a1 in zip(p0, p1)]
        print(json.dumps({'record': rec, 'position milli at 0': p0, 'at n': p1, 'velocity milli per interval (quotient)': v, 'P at 0': first['records'][rec]['P'], 'P at n': last['records'][rec]['P'], 'W at 0': first['records'][rec]['W total'], 'W at n': last['records'][rec]['W total'], 'quanta at 0': first['records'][rec]['quanta (share div unit)'], 'quanta at n': last['records'][rec]['quanta (share div unit)']}))
    print(json.dumps({'run back': run_back, 'counts': b.counts, 'census': last['census (integers, bits)'], 'transient bits': last['max transient bits'], 'lays': [{k: e[k] for k in e if k != 'event'} for e in result['lays']], 'births': len(result['births']), 'credits': len(result['credits']), 'refused': result['refused'], 'ms': result['milliseconds']}))


if __name__ == '__main__':
    main()
