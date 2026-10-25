"""The engine's held writes on the record's world: per line the write's quotient (numerator div wall) over the board at a few intervals, and the walls, to read the law's scales for the toy."""
import sys, json
from pathlib import Path
ROOT = str(Path(__file__).resolve().parents[4]); sys.path.insert(0, ROOT + '/src'); sys.path.insert(0, ROOT)
import numpy as np
from event_universe import world_files, records
from event_universe.world_files import load_world
from event_universe.lattice import Lattice
world_files.REPOSITORY_ROOT = Path(ROOT)
world = load_world(Path(ROOT) / 'examples/events/universe24/universe24.json')
LAST = {}
_ws = records.write_sources
def ws(held, families, bookings, stresses, write, rulers, gamma, sourcing, motion=None, direction=1, fixed=None):
    found, walls, terms = _ws(held, families, bookings, stresses, write, rulers, gamma, sourcing, motion, direction, fixed)
    rows = []
    for f, w in zip(found, walls):
        fa = np.asarray(f, dtype=object).reshape(-1); wa = np.asarray(w, dtype=object).reshape(-1)
        n = max((abs(int(x)) for x in fa), default=0); ww = int(wa[0]) if wa.size else int(w)
        rows.append((n, ww))
    LAST[held] = rows
    return found, walls, terms
records.write_sources = ws
board = Lattice(world)
names = [f.name for f in board.families]
print('held rows', [(i, names[i], board.families[i].pair[0] == board.families[i].pair[1]) for i in board.held])
for i in board.held:
    print(names[i], 'write walls bits', [int(w).bit_length() if np.ndim(w) == 0 else 'array' for w in board.write_walls[i]])
for t in range(40):
    board.step()
    if board.interval in (1, 5, 13, 20, 30, 40):
        out = {}
        for held, lines in LAST.items():
            out[names[held]] = [(n.bit_length(), w.bit_length(), 'q~%d' % (n // w if w else -1)) for n, w in lines]
        q = board.quanta(world.seed)[0]
        print(json.dumps({'i': board.interval, 'per line (max |numerator| bits, wall bits, q = numerator div wall)': out}))
