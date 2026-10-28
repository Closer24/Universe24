"""V1 (verifier of G): at the setting, for every shipped world: rim's parity, Gamma, G, and every hand gear's
teeth as a multiple of rim and of t = clock.teeth (no tick). Integers only."""
import sys
from pathlib import Path
S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src', S + '/t24']
sys.set_int_max_str_digits(0)
import numpy as np
from event_universe.assembly.piece import read_piece
from event_universe import clock as CL
for p in sorted(Path(S + '/t24/tests/worlds').glob('world_*.json')):
    calibre, piece = read_piece(p)
    c = CL.Clock(calibre, piece)
    rim, t, gam, G = int(c.rim), int(c.teeth), int(c.full_rate), int(c.G)
    ws = set()
    for r in c.hands():
        for g in r.gears:
            for w in np.asarray(g.teeth, dtype=object).flat:
                ws.add(int(w))
    xs = sorted(set(w // t for w in ws))
    ok = all(w % rim == 0 and (w // rim) % 2 == 0 for w in ws)
    print(f'{p.name}: rim odd {rim % 2 == 1}; Gamma {gam}; G {G}; t even {t % 2 == 0}; hand teeth / t {xs} exact {all(w % t == 0 for w in ws)}; rim | w and w/rim even {ok}')
