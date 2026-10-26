"""pc1, the ONE-NODE test of the carried clock (2026-10-25): a Node fed a content, its paces read from the carried memo forward and back.

(i) The memo is a pure function of the content: the clock and the Link's pace at every content from 0 to the edge read twice in two orders (upward, then downward) are the same integers (the run back through a content's change reads the same paces, so Rule3's inverse recomputes the same coefficients).
(ii) The step at one Node: the toy's 3-cube (world_node.json) with the centre's content fed to c (the volume's level set), 20 intervals forward and 20 back, the state compared bit for bit, under the flag (the carried clock) and off it (David's memo); the paces at the fed content listed with the letter's value.
(iii) The width: the memo's largest integer at the edge under each form.
Usage: PYTHONPATH=<worktree>/src python one_node_test_pc1.py <out.json>
"""
import sys, os, json, copy, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'toy_pc1'))
import numpy as np
import pc1_paces
from event_universe.core import paces as engine_paces
from event_universe.features import volume as volform

sys.set_int_max_str_digits(0)


def pure_function(gamma, edge, flag):
    car = pc1_paces.Carried(flag)
    up = [(car.clock(gamma, c), car.link(gamma, c)) for c in range(edge + 1)]
    car2 = pc1_paces.Carried(flag)
    down = [(car2.clock(gamma, c), car2.link(gamma, c)) for c in range(edge, -1, -1)][::-1]
    hills_up = [(car.clock(gamma, -c), car.link(gamma, -c)) for c in range(1, 101)]
    hills_down = [(car2.clock(gamma, -c), car2.link(gamma, -c)) for c in range(100, 0, -1)][::-1]
    return {'contents': edge + 1, 'equal in both orders': sum(1 for a, b in zip(up, down) if a == b), 'hills equal (100)': sum(1 for a, b in zip(hills_up, hills_down) if a == b), 'memo bits': car.memo_bits(gamma)}


def step_at_content(flag, content, intervals):
    os.environ['PC1_CLOCK'] = flag
    for m in [k for k in sys.modules if k in ('lean_full',)]:
        del sys.modules[m]
    import lean_full
    lean_full.paces = pc1_paces.shim(engine_paces, flag)
    universe, world = lean_full.load_world(os.path.join(HERE, 'toy_pc1', 'world_node.json'))
    b = lean_full.Lean(universe, world)
    p = tuple(x // 2 for x in world['shape'])
    m = b.row(10).lines[0]
    level = int(np.asarray(volform.volume_of(b.gamma, np.array([content], dtype=object)), dtype=object).reshape(-1)[0])
    m.now[p] = level; m.before[p] = level
    def h(): return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()
    kept = [h()]
    read = []
    for _ in range(intervals):
        b.step(); kept.append(h()); read.append(int(np.asarray(b.start_content)[p]))
    exact = 0
    for k in range(intervals):
        b.step_back(); exact += (h() == kept[intervals - 1 - k])
    c_read = read[0]
    return {'flag': flag, 'content fed': content, 'content read at the Node at interval 1': c_read, 'contents read at the Node over the run': sorted(set(read)),
            'clock at the fed content (form)': int(lean_full.paces.clock_of(b.gamma, c_read)), 'clock letter (engine clock_alone)': engine_paces.clock_alone(b.gamma, c_read),
            'link pace (form)': int(lean_full.paces.link_pace_of(b.gamma, c_read)), 'link pace letter': int(engine_paces.rounded(engine_paces.clock_alone(b.gamma, c_read) ** 2, b.gamma)),
            'run back exact': exact, 'intervals': intervals, 'births': b.counts['births'], 'body credits': b.counts['body_clicks'], 'turns': b.counts['turns'], 'max transient bits (toy)': b.max_transient, 'memo bits': lean_full.paces.memo_bits(b.gamma)}


if __name__ == '__main__':
    out = {}
    gamma = 1000
    edge = engine_paces.frozen_content(gamma)
    for flag in ('plain', 'half', 'gamma', 'gamma2', 'scaled'):
        out['(i) pure function %s' % flag] = pure_function(gamma, edge, flag)
    for flag in ('memo', 'scaled', 'plain'):
        for content in (0, 300, 1000, 3000):
            out['(ii) %s at content %d' % (flag, content)] = step_at_content(flag, content, 20)
            print(json.dumps({'(ii)': out['(ii) %s at content %d' % (flag, content)]}), flush=True)
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k.startswith('(i)')}))
