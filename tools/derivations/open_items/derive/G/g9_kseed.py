"""G9 (drafter G): which shipped seeds are their own antiworld: after the setting, before the first tick, every
hand's twelve gear at the notch 0 (now and before) with its fine tooth at mid at every clock, so that K (the
twelve gear negated, the fine tooth reflected about mid) leaves the state unchanged; and the offset train at
rest (all notches 0). Builds each world's clock (no tick). argv: none."""
import sys
from pathlib import Path

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src', S + '/t24']
sys.set_int_max_str_digits(0)
import numpy as np  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe import clock as CL  # noqa: E402
from event_universe.core import acts  # noqa: E402
from event_universe.trains import OFFSET  # noqa: E402

worlds = sorted(p.name for p in Path(S + '/t24/tests/worlds').glob('world_*.json'))
for name in worlds:
    calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + name))
    clock = CL.Clock(calibre, piece)
    per_hand = []
    for r in clock.hands():
        g = r.gears[1]
        zero = not np.any(np.asarray(g.now, dtype=object) != 0) and not np.any(np.asarray(g.before, dtype=object) != 0)
        at_mid = bool(np.all(np.asarray(g.fine, dtype=object) == np.asarray(acts.mid(g.teeth), dtype=object)))
        per_hand.append('K-fixed' if zero and at_mid else 'moved by K')
    off = clock.train(OFFSET)
    rest = all(not np.any(np.asarray(a, dtype=object) != 0) for g in off.gears for a in (g.now, g.before))
    verdict = 'its own antiworld' if all(h == 'K-fixed' for h in per_hand) and rest else 'not K-fixed'
    print(f'{name}: {verdict}; the hands (acts order) {per_hand}; the offset at rest {rest}')
