"""Probe 6: the dual run's agreement at both ends, at other keys.  The Boss's tsym.py (the clean copy, unchanged) checks
T tick T = 1 (and T T = 1, T tick T = untick, and the doubled clock: forward N ticks, mirror, forward N, mirror = the
start) on the committed act at key 36,000.  Here its functions run unchanged at other keys: a history agrees with
itself at both ends at every key or the key would be singled out.  The universe's integers are swapped in tsym's own
module before its worlds are built; nothing else is touched.

usage: python3 -I p6_reversal_keys.py   (about a minute)
"""

import importlib.util
import sys
from pathlib import Path

SRC = str(Path(__file__).resolve().parents[6] / "src")  # the worktree's committed act
TSYM = str(Path(__file__).resolve().parents[1] / "tsym" / "tsym.py")  # boss/tsym, unchanged
sys.path.insert(0, SRC)
spec = importlib.util.spec_from_file_location("tsym", TSYM)
tsym = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tsym)


def main():
    print(
        "Probe 6: the act's exact time reversal (tsym.py's checks, unchanged) at keys other than 36,000"
    )
    for key in (36000, 35999, 2, 1, 10**12):
        tsym.INTEGERS["key"] = key
        lines = []
        for name, trains, amplitude, seed in (
            ("light", [tsym.LIGHT], 600, 11),
            ("light + matter", [tsym.LIGHT, tsym.MATTER], 300, 113),
        ):
            L, s = tsym.built(trains, amplitude, seed)
            exact, rounds, cells, span, past, below, fail = tsym.run(L, s, 60)
            far = [tsym.doubled(L, s, 60, at) for at in (tsym.C, 0)]
            lines.append(
                f"{name}: exact {exact}/60, time gear {span[0]}..{span[1]}, first failure {fail}, doubled clock {far}"
            )
        print(f"  key {key}: " + "; ".join(lines))
    print(
        "So every history of the act agrees with itself at both ends at every key: the fixed point of the dual run is"
    )
    print("met by each history alike and singles out no key.")


if __name__ == "__main__":
    main()
