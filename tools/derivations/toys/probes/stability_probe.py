"""The engine's own course on the tests' small universe at a given den, the hole seed on a cube: per interval the light's velocity (max |now - before|), the tension lines' range, the content's range, the births and the turns, to set beside the toy's rows on the same universe.
Usage: python stability_probe.py <den> <cube> <intervals>"""
import sys, os, json
from pathlib import Path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'src')); sys.path.insert(0, ROOT)
import numpy as np
from tests.laws_universe import bare_torus, SMALL
from event_universe import world_files
from event_universe.world_files import load_world
from event_universe.lattice import Lattice
den, cube, intervals = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
folder = Path(os.environ.get('TMPDIR', '/tmp')) / ('stability_%d_%d' % (den % 100000, cube))
folder.mkdir(parents=True, exist_ok=True); world_files.REPOSITORY_ROOT = folder
path = bare_torus(folder, cube, intervals)
(folder / 'u.json').write_text(json.dumps({'integers': {**SMALL['integers'], 'den': den}}), 'utf-8')
world = load_world(path)
board = Lattice(world)
names = [f.name for f in board.families]
vol = [i for i in board.held if not board.families[i].wronskian][0]
light = world.seed
def rng(a): a = np.asarray(a, dtype=object).reshape(-1); return [min(int(x) for x in a), max(int(x) for x in a)]
marks = {1, 5, 10, 25, 50, 75, 100, 150, 200, 300, 400, 600}
print({'families': names, 'volume row': vol, 'light row': light, 'width': world.width.bit_length() if hasattr(world, 'width') else None})
for t in range(intervals):
    board.step()
    if board.interval in marks or board.interval == intervals:
        st = board.states[vol].lines; lt = board.states[light].lines[0]
        tens = [rng(st[k].now) for k in range(1, 4)]
        v = max(abs(int(a) - int(b)) for a, b in zip(np.asarray(lt.now, dtype=object).reshape(-1), np.asarray(lt.before, dtype=object).reshape(-1)))
        content = board.read(vol, 1, 0)[0] if hasattr(board, 'read') else None
        print(json.dumps({'i': board.interval, 'light velocity max': v, 'tensions min/max per axis': tens, 'volume time line min/max': rng(st[0].now), 'turns': int(board.turned.sum()) if hasattr(board, 'turned') else None, 'swaps so far': len(getattr(board, 'swaps', []))}), flush=True)
