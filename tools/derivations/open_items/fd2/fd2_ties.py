"""The ties of the turn's rounding on a record (fd2, section 3): David's toy rounds a turned arrival half up, (2 a + X) div (2 X), the
engine's phase.fold rounds half away from zero (odd_rounded); the two differ where 2 a = X mod 2 X with a < 0 (a negative tie).
This script runs David's Node with `turned_arrival` instrumented (a reading, the state untouched) and counts, over the run, the
roundings taken, the ties met and the negative ties (where the two roundings would part the record).
Usage: python fd2_ties.py <world.json> <intervals>"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'toy_david'))
import numpy as np
from lean_full import Lean, load_world, link, AXES

sys.set_int_max_str_digits(0)


class Counted(Lean):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.ties = {'roundings': 0, 'ties': 0, 'negative ties': 0, 'nonzero numerators': 0}

    def turned_arrival(self, arrivals, port, turn):
        if turn is None or len(arrivals) == 1: return arrivals
        phases, odd, frames = turn; axis, side = AXES[port]
        re_j, im_j = arrivals; im_j = frames[port] * im_j; c, s = phases[port]
        _e, (n,), _f = link(port, odd=[odd[axis]])
        Wl = 4 * self.gamma; tc, ts, tw = Wl * Wl - n * n, 2 * Wl * n, Wl * Wl + n * n
        a_re = (c * re_j - s * im_j); a_im = (s * re_j + c * im_j)
        for num, wall in ((a_re, self.X), (a_im, self.X)):
            self.count(num, wall)
        a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)
        b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)
        for num, wall in ((b_re, tw), (b_im, tw)):
            self.count(num, wall)
        return [(2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)]

    def count(self, num, wall):
        num = np.asarray(num, dtype=object).reshape(-1); wall = np.asarray(wall, dtype=object).reshape(-1)
        if wall.size == 1: wall = np.repeat(wall, num.size)
        for x, w in zip(num.tolist(), wall.tolist()):
            x, w = int(x), int(w); self.ties['roundings'] += 1; self.ties['nonzero numerators'] += (x != 0)
            if (2 * x) % (2 * w) == w:
                self.ties['ties'] += 1; self.ties['negative ties'] += (x < 0)


universe, world = load_world(sys.argv[1]); n = int(sys.argv[2])
b = Counted(universe, world)
for _ in range(n): b.step()
print(json.dumps({'world': os.path.basename(sys.argv[1]), 'intervals': n, 'X': b.X, 'counts': {k: str(v) for k, v in b.counts.items()}, 'turn roundings': b.ties}))
