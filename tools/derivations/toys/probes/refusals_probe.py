"""Why 4.0 births stop: per interval, the meetings (Nodes with a whole quantum of light), the origin refusals, the reads' refusals by cause, the births; on the small bare torus with the hole seed."""
import sys, json, time
from pathlib import Path
from collections import Counter
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))  # tools/derivations/toys/probes -> the repository
sys.path.insert(0, os.path.join(ROOT, 'src')); sys.path.insert(0, ROOT)
from tests.laws_universe import bare_torus, SMALL
from event_universe import world_files, meeting_board, digits
from event_universe.features.click import Refused
from event_universe.world_files import load_world
from event_universe.lattice import Lattice
if sys.argv[1].endswith('.json'):  # a world file given whole (the record's), the repository the root
    path = Path(sys.argv[1]); world_files.REPOSITORY_ROOT = Path(__file__).resolve().parents[4]; intervals = int(sys.argv[3])
else:
    folder, cube, intervals = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    folder.mkdir(parents=True, exist_ok=True); world_files.REPOSITORY_ROOT = folder
    path = bare_torus(folder, cube, intervals)
    if len(sys.argv) > 4: (folder / 'u.json').write_text(json.dumps({'integers': {**SMALL['integers'], 'den': int(sys.argv[4])}}), 'utf-8')
world = load_world(path)
C = Counter()
_meetings = meeting_board.meetings
def meetings(board, index, shares, frozen):
    found = _meetings(board, index, shares, frozen); C['meetings'] += len(found); C['meetings whole>=2'] += sum(1 for _a, w, _r in found if w >= 2); C['meetings whole==1 rest>0'] += sum(1 for _a, w, r in found if w == 1 and r > 0); return found
meeting_board.meetings = meetings
_at_origin = meeting_board.at_origin
def at_origin(board, reads):
    r = _at_origin(board, reads); C['at_origin ' + str(r)] += 1; return r
meeting_board.at_origin = at_origin
_read_of = meeting_board.read_of
def read_of(board, reads, label):
    try: r = _read_of(board, reads, label); C['read ok'] += 1; return r
    except Refused as named: C['read refused ' + str(named.cause)] += 1; raise
meeting_board.read_of = read_of
_affordable = meeting_board.affordable
def affordable(*a):
    t = _affordable(*a); C['tables ' + str(len(t))] += 1; return t
meeting_board.affordable = affordable
_refused_by = meeting_board.refused_by
SAMPLE = []
def refused_by(board, at, table, found):
    r = _refused_by(board, at, table, found)
    if r is None: C['BIRTH'] += 1
    else:
        C['refused ' + str(r[0])] += 1
        if len(SAMPLE) < 3 or C['refused ' + str(r[0])] % 500 == 0: SAMPLE.append((board.interval, at, r, getattr(found, 'taken', None), getattr(found, 'walls', None), getattr(found, 'levels', None)))
    return r
meeting_board.refused_by = refused_by
board = Lattice(world)
t0 = time.time(); last = Counter()
for i in range(intervals):
    board.step()
    if board.interval in (1, 2, 3, 5, 8, 12, 13, 14, 15, 17, 20, 25, 30, 40, 50, 60, 80, 100, 150, 200, 300):
        d = {k: C[k] - last[k] for k in sorted(C)}; last = C.copy()
        q = board.quanta(world.seed)[0]
        print(json.dumps({'i': board.interval, 'since last': d, 'light quanta board': int(q.sum()), 'max per node': int(q.max()), 'births total': int(getattr(board.credit, 'counts', [0]*9)[world.seed]) if False else None, 'seconds': int(time.time() - t0), 'sample': [str(x) for x in SAMPLE[-2:]]}), flush=True)
