"""bh2: the one-Node test of the frozen Node (ALGEBRA.md The frozen Node has no share; Locality is never broken; the brief's (1) and (2)): the 3-cube of world_node.json with its centre fed to a content at or past the frozen content (the carrier's time line at X(c), before = now, the light at the centre four times the sea's), run N intervals under the engine's default (the law) and under the flagged form `hold`; per interval at the centre: the content, X and its bits, X's second difference (the write and the mass term), each row's first line's level and velocity, the proper count's increment (the clock), the clicks at the centre, the neighbours' reaches toward the centre (the valve), the largest neighbour content; the max transient; then the run back of N compared by the state's hash. Integers only. Usage: python bh2_one_node.py <content> <intervals> <out.json>"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np

from bh2_flagged import Flagged, load_flagged_world
from event_universe.core import paces
from event_universe.features import volume
from event_universe.rows import CARRIER, PLANE

sys.set_int_max_str_digits(0)
WORLD = sys.argv[4] if len(sys.argv) > 4 else "world_node.json"
CUBE = json.load(open(os.path.join(HERE, "worlds", WORLD)))["shape"][0]
CENTRE = (CUBE // 2,) * 3
NEIGHBOURS = [tuple((CENTRE[a] + (s if a == ax else 0)) % CUBE for a in range(3)) for ax in range(3) for s in (1, -1)]


def level_at(node, content):
    return int(np.asarray(volume.volume_of(node.gamma, np.array([content], dtype=object)), dtype=object).reshape(-1)[0])


def fed(form, content):
    universe, world = load_flagged_world(os.path.join(HERE, "worlds", WORLD))
    world = dict(world, control={'frozen': form})
    node = Flagged(universe, world)
    carrier = node.row(CARRIER).lines[0]
    carrier.now[CENTRE] = level_at(node, content)
    carrier.before[CENTRE] = carrier.now[CENTRE]
    node.ride_walls()
    light = node.row(PLANE, gap=0).lines[0]
    light.now[CENTRE] = 4 * int(light.now[CENTRE])
    return node


def bits(x):
    return abs(int(x)).bit_length()


def course(node, n):
    rows = []
    x_hist = []
    for k in range(n):
        c = node.content()
        X = node.row(CARRIER).lines[0]
        x_hist.append(int(X.now[CENTRE]))
        p_before = int(node.proper[CENTRE])
        factors = node.link_factors()
        # the neighbours' reaches toward the centre: each neighbour's rule at its own content, the Port that faces the centre
        reach_in = []
        for port, nb in enumerate(NEIGHBOURS):
            back_port = port ^ 1  # the Port from the neighbour toward the centre
            r = node.rule_of(node.row(PLANE, gap=0), c, factors)
            reach_in.append(bits(np.asarray(r.reaches[back_port])[nb]))
        node.step()
        row = {
            'i': node.interval,
            'content': int(c[CENTRE]),
            'X bits': bits(X.now[CENTRE]) if False else bits(x_hist[-1]),
            'X velocity (now - before) bits, sign': [bits(int(X.now[CENTRE]) - int(X.before[CENTRE])), int(np.sign(int(X.now[CENTRE]) - int(X.before[CENTRE])))],
            'lines at the centre (level bits, velocity bits) per row first line': [[bits(r_.lines[0].now[CENTRE]), bits(int(r_.lines[0].now[CENTRE]) - int(r_.lines[0].before[CENTRE]))] for r_ in node.rows_],
            'proper increment at the centre (the clock)': int(node.proper[CENTRE]) - p_before,
            'frozen Nodes': int((np.asarray(paces.link_pace_of(node.gamma, c), dtype=object) == 0).sum()),
            'neighbour reach toward the centre bits (gap-0 row)': reach_in,
            'largest neighbour content': max(int(c[nb]) for nb in NEIGHBOURS),
            'clicks at the centre so far': sum(1 for e in node.log if tuple(e['node']) == CENTRE and e['event'] in ('birth', 'credit')),
            'births, body clicks, turns': [node.counts['births'], node.counts['body_clicks'], node.counts['turns']],
            'max transient bits': node.max_transient,
            'max state bits': node.census()[1],
        }
        rows.append(row)
    # X's second differences at the centre: the write plus the mass term, from the history
    second = [x_hist[k + 1] - 2 * x_hist[k] + x_hist[k - 1] for k in range(1, len(x_hist) - 1)]
    return rows, x_hist, second


def run_back(node, n):
    hashes = []
    for _ in range(n):
        hashes.append(node.state_hash())
        node.step()
    exact = 0
    for k in range(n):
        node.step_back()
        exact += node.state_hash() == hashes[n - 1 - k]
    return exact


def main(argv):
    content, n = int(argv[1]), int(argv[2])
    out = {}
    for form in (argv[5].split(',') if len(argv) > 5 else ('law', 'hold')):
        node = fed(form, content)
        start = copy.deepcopy(node)
        rows, x_hist, second = course(node, n)
        picks = [0, 1, 2, 4, 9, 19, 49, n - 1]
        out[form] = {
            'fed content, X at the start (value, bits)': [content, x_hist[0], bits(x_hist[0])],
            'course at intervals 1, 2, 3, 5, 10, 20, 50, N': [rows[k] for k in picks if k < n],
            'X at the end (bits), content at the end': [bits(x_hist[-1]), rows[-1]['content']],
            'X second difference bits per interval (first 5, last 3)': [[bits(s), int(np.sign(s))] for s in second[:5]] + [[bits(s), int(np.sign(s))] for s in second[-3:]],
            'X velocity at the end (bits, sign)': rows[-1]['X velocity (now - before) bits, sign'],
            'proper count at the centre: start, end': [0, int(node.proper[CENTRE])],
            'clicks at the centre': rows[-1]['clicks at the centre so far'],
            'clicks on the board (births, body clicks)': rows[-1]['births, body clicks, turns'][:2],
            'max transient bits over the run': max(r['max transient bits'] for r in rows),
            'max state bits over the run': max(r['max state bits'] for r in rows),
            'run back exact of N': run_back(start, n),
            'frozen Node-intervals': sum(r['frozen Nodes'] for r in rows),
        }
    json.dump(out, open(argv[3], 'w'), indent=1)
    for form, v in out.items():
        print('==', form)
        for k, val in v.items():
            if k.startswith('course'):
                for r in val:
                    print('  ', json.dumps(r))
            else:
                print(' ', k, ':', val)


if __name__ == '__main__':
    main(sys.argv)
