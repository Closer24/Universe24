"""H_verify v3: draft H's engine probe rerun on short cases, with one more count: the A1 sum S of a clock's six
Mesh factors against the vacuum's C = 6 G^2 (S < C, S = C, S > C, S = 0 where F-H5 needs its guard).

Run: /home/user/Universe24/venv314/bin/python -I v3_engine.py <variant> <world> <ticks>
Imports the draft's h_engine.py read-only; the head's code is only monkeypatched at run time.
"""

import sys

S = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad"
sys.path[:0] = [S + "/derive/H", S + "/t24/src", S + "/t24"]

import numpy as np  # noqa: E402

import h_engine as E  # noqa: E402

ORIG = E.gearing


def gearing(pinion, rim, full_rate, rate, mesh_rate, factors=None, mesh_unit=1):
    if factors is not None:
        total = np.asarray(sum(np.asarray(f, dtype=object) for f in factors), dtype=object)
        cap = 6 * mesh_unit * mesh_unit
        E.bump("A1: S == 0 (F-H5's guard)", E.n(total == 0))
        E.bump("A1: S < C", E.n(total < cap))
        E.bump("A1: S == C", E.n(total == cap))
        E.bump("A1: S > C", E.n(total > cap))
        E.bump("A1: 2 S <= C (half the vacuum's or less)", E.n(total + total <= cap))
    return ORIG(pinion, rim, full_rate, rate, mesh_rate, factors, mesh_unit)


E.gearing = gearing

if __name__ == "__main__":
    E.main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
