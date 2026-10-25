"""pa1: the branch's engine as written (src, no edit): the board's own births (both children at one Node, meeting_board.closed) on the bare 3-cube at den 1,021 from the sea plus one quantum at (1, 0, 0) and from its image under each of the cube's 48, the click records compared through the image (the birth lines: interval, family, children, senses, the Nodes, the take's integers; the credit lines: interval, identity, point, sense, beat): equal, the senses exchanged, or neither; the born dipole (0 at a one-Node birth) and the charge (the senses' sum). Reuses tests/test_the_board_is_the_cube_48.cube_48 and tests/laws_universe.sea_plus_one; integers only.
Usage: PYTHONPATH=<worktree>/src python tools/derivations/pa1/src_births48.py <intervals> <out.json>"""
import sys, json, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
for place in (str(ROOT), str(ROOT / 'src')):
    if place not in sys.path: sys.path.insert(0, place)

from event_universe import seed as seed_module, world_files  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import sea_plus_one, small_universe  # noqa: E402
from tests.test_the_board_is_the_cube_48 import cube_48  # noqa: E402

CUBE = 3


def det(m):
    m = m.tolist()
    return int(m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def image(m, node):
    return tuple(int(v) % CUBE for v in (m @ np.array(node, dtype=int)))


def board_at(folder: Path, at, intervals, lines):
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    small_universe(folder)
    (folder / 'w.json').write_text(json.dumps({'universe': 'u.json', 'shape': [CUBE] * 3, 'intervals': intervals}), encoding='utf-8')
    seed_module.uniform_seed = sea_plus_one(at)
    return Lattice(load_world(folder / 'w.json'), output=lines.append)


def records(lines):
    births = []; credits = []
    for x in lines:
        if x.get('event') == 'birth':
            nodes = [tuple(n) for n in x['nodes']]
            kids = frozenset((nodes[k % len(nodes)], x['children'][k], x['senses'][k]) for k in range(len(x['children'])))
            births.append((x['interval'], x['family'], kids, tuple(x.get(k) for k in ('taken', 'walls', 'levels', 'excess') if k in x)))
        elif x.get('event') == 'credit':
            credits.append((x['interval'], str(x.get('identity')), str(x.get('point')), x.get('sense'), str(x.get('beat')), str(x.get('family'))))
    return sorted(births, key=repr), sorted(credits, key=repr)


def mapped(births, m, exchange):
    found = []
    for i, fam, kids, take in births:
        found.append((i, fam, frozenset((image(m, n), ch, -s if exchange else s) for n, ch, s in kids), take))
    return sorted(found, key=repr)


if __name__ == '__main__':
    intervals, out = int(sys.argv[1]), sys.argv[2]
    t0 = time.monotonic_ns()
    at = (1, 0, 0)
    base_lines = []
    base = board_at(Path('/dev/shm/tmp/pa1_src/base'), at, intervals, base_lines)
    for _ in range(intervals): base.step()
    b_births, b_credits = records(base_lines)
    dipole = sum(1 for i, fam, kids, take in b_births if len({n for n, ch, s in kids}) > 1)
    result = {'engine': 'src at 8b1237234, meeting_board.closed (both children at one Node)', 'den': 1021, 'seed': 'sea plus one quantum at (1,0,0), the hole at the origin', 'intervals': intervals, 'births': len(b_births), 'credits': len(b_credits), 'births with the two children at different Nodes (the dipole)': dipole, 'charge: senses sum over births': sum(s for i, fam, kids, take in b_births for n, ch, s in kids), 'birth intervals': sorted({i for i, fam, kids, take in b_births})}
    equal = exchanged = neither = 0; per = []
    for k, m in enumerate(cube_48()):
        lines = []
        other = board_at(Path('/dev/shm/tmp/pa1_src/g%d' % k), image(m, at), intervals, lines)
        for _ in range(intervals): other.step()
        o_births, o_credits = records(lines)
        same = o_births == mapped(b_births, m, False)
        swapped = o_births == mapped(b_births, m, True)
        d = det(m)
        if same: equal += 1
        elif swapped: exchanged += 1
        else: neither += 1
        per.append({'element': m.tolist(), 'det': d, 'equal': same, 'exchanged': swapped, 'births': len(o_births)})
    result['the 48 on the birth records'] = {'equal': equal, 'exchanged (and not equal)': exchanged, 'neither': neither, 'note': 'with both children at one Node the exchange of the senses maps the pair to itself, so every equal element is also exchanged; the count above names the elements equal first'}
    result['the 48: equal and also exchanged (the pair at one Node is C-even)'] = sum(1 for p in per if p['equal'] and (mapped(b_births, np.array(p['element']), True) == mapped(b_births, np.array(p['element']), False)))
    result['per element'] = per
    result['milliseconds'] = (time.monotonic_ns() - t0) // 1000000
    json.dump(result, open(out, 'w'), indent=1)
    print(json.dumps({k: v for k, v in result.items() if k != 'per element'}))
