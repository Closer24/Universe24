"""V4 (verifier of G): the exact ties of the odd (sign-magnitude) roundings the draft's site table leaves out:
rates.rounded outside the impulse's u (tick.py:115 the clocked offset, tick.py:301 the release) and
meshes.offset_pair's rounded (meshes.py:49, every turn through a mesh, the skew's included). A tie: 2 n = T
(mod 2 T). Counting wrappers only; the head's integers unchanged. argv: world ticks."""
import sys
from collections import Counter
from pathlib import Path
S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src', S + '/t24']
sys.set_int_max_str_digits(0)
import numpy as np
from event_universe.assembly.piece import read_piece
from event_universe import clock as CL, meshes as M, tick as T
from event_universe.core import rates
C = Counter()
orig = rates.rounded
def obj(x):
    return np.asarray(x, dtype=object)
def wrap(numerator, teeth):
    out = orig(numerator, teeth)
    f = sys._getframe(1)
    site = f'{f.f_code.co_filename.split("/")[-1]}:{f.f_lineno} {f.f_code.co_name}'
    n, t = obj(numerator), obj(teeth)
    tie = ((n + n) % (t + t)) == t
    C[site + ' calls'] += int(np.size(n))
    C[site + ' ties'] += int(np.count_nonzero(tie.astype(bool)))
    return out
rates.rounded = wrap
M.rounded = wrap
world, ticks = sys.argv[1], int(sys.argv[2])
calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + world))
clock = CL.Clock(calibre, piece)
C.clear()  # the setting's roundings left out; the ticks alone
for _ in range(ticks):
    clock.tick()
print(f'{world} {ticks} ticks')
for k in sorted(C):
    print(f'  {k}: {C[k]}')
