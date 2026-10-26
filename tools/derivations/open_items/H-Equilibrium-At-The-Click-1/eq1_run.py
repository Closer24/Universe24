"""eq1's runner over a copy of the engine (PYTHONPATH names it): a world run N intervals, every interval read from outside (the mean, least and largest X, every Node alike or not, the gap-0 line's velocity now - before at the origin, the credits and their levels), then `back` intervals run back by the state's hash; the bottoms and tops; the census (integers, bits); the state hash at the end (the flag off bit for bit David's). Integers only. Usage: eq1_run.py <world.json> <out prefix> [intervals N] [back N]. Writes <prefix>.json (compact) and prints the summary."""
import json, os, sys, time
import numpy as np

sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE


def ints(a):
    return [int(x) for x in np.asarray(a).reshape(-1)]


def main(argv):
    universe, world = load_world(argv[1])
    prefix = argv[2]
    intervals = int(argv[argv.index('intervals') + 1]) if 'intervals' in argv else int(world['intervals'])
    back = int(argv[argv.index('back') + 1]) if 'back' in argv else 0
    node = Node(universe, world)
    gamma = node.gamma
    origin = tuple(0 for _ in node.shape)
    rows = []
    hashes = []
    maxbits = 0
    seen = 0
    t0 = time.monotonic_ns()
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(node.state_hash())
        node.step()
        n_ints, bits = node.census()
        maxbits = max(maxbits, bits)
        x = ints(node.row(CARRIER).lines[0].now)
        gap0 = node.row(PLANE, gap=0).lines[0]  # the rows' Line objects are new at every interval: read the line now
        credits = [e for e in node.log[seen:] if e['event'] == 'credit']
        births = sum(1 for e in node.log[seen:] if e['event'] == 'birth')
        refused_arrival = sum(1 for e in node.log[seen:] if e['event'] == 'refused' and e.get('cause') == 'arrival')
        seen = len(node.log)
        rows.append({
            'i': node.interval,
            'X mean': sum(x) // len(x), 'X min': min(x), 'X max': max(x),
            'alike': int(min(x) == max(x)),
            'turned': int(node.turned.sum()),
            'v light at origin': int(gap0.now[origin]) - int(gap0.before[origin]),
            'light now at origin': int(gap0.now[origin]),
            'credits': len(credits),
            'credit levels': sorted(set(int(c['levels']) for c in credits)),
            'credit lines': sorted(set(int(c['line']) for c in credits)),
            'credit beats': sorted(set(int(c['beat']) for c in credits)),
            'laid back': sum(int(c.get('laid_back', 0)) for c in credits),
            'births': births,
            'refused arrival': refused_arrival,
            'laid': int(node.counts['laid']),
        })
    end_hash = node.state_hash()
    exact = 0
    for k in range(len(hashes)):
        node.step_back()
        exact += node.state_hash() == hashes[len(hashes) - 1 - k]
    means = [r['X mean'] for r in rows]
    n = len(means)
    bottoms = [(k + 1, means[k]) for k in range(1, n - 1) if means[k] <= means[k - 1] and means[k] < means[k + 1]]
    tops = [(r['i'], r['turned']) for r in rows if r['turned']]
    credits_all = [e for e in node.log if e['event'] == 'credit']
    per_node = {}
    for c in credits_all:
        per_node[tuple(c['node'])] = per_node.get(tuple(c['node']), 0) + int(c['levels'])
    summary = {
        'world': argv[1], 'flags': {k: v for k, v in os.environ.items() if k.startswith('EQ1_')},
        'intervals': intervals, 'alike': sum(r['alike'] for r in rows), 'tops': tops, 'bottoms': bottoms,
        'births': int(node.counts['births']), 'credits': len(credits_all),
        'credits by line': {str(k): sum(1 for c in credits_all if c['line'] == k) for k in sorted(set(c['line'] for c in credits_all))},
        'levels taken in all': sum(int(c['levels']) for c in credits_all),
        'laid back in all': sum(int(c.get('laid_back', 0)) for c in credits_all),
        'levels taken per Node (distinct sums)': sorted(set(per_node.values())),
        'refused arrival': int(node.counts.get('refused_arrival', 0)),
        'refused stop': int(node.counts['refused_stop']),
        'laid (the emission)': int(node.counts['laid']),
        'turns': int(node.counts['turns']),
        'integers': n_ints, 'max bits': maxbits,
        'run back': {'intervals': len(hashes), 'exact': exact},
        'state hash at the end': end_hash,
        'milliseconds': (time.monotonic_ns() - t0) // 1000000,
    }
    with open(prefix + '.json', 'w', encoding='utf-8') as out:
        json.dump({'summary': summary, 'rows': rows}, out)
    print(json.dumps(summary))


if __name__ == '__main__':
    main(sys.argv)
