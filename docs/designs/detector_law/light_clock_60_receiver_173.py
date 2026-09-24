"""The light clock's pin on the chain of 173 (SIZING.md: light_clock_60 shrunk from the chain of 673
to the builder's (ac) chain, A at [100, 112), the set the free Node 112, the mirror 172, the -x face
100 Links from A so that its half returns at 2 x 100 x sqrt 3 = 346, after the rung), by the same
map as `light_clock_60_receiver.py` (imported, nothing re-derived) under DECLARATIONS.md section 10
item 9's form: the set's one Node free for the grace and held at 0 after it, A's cells taking their
own record from the train's end (item 10). A COMPUTATION before the World Generator regenerates the
file; the .out beside is the pin's provenance on this chain.

    PYTHONPATH=src python docs/designs/detector_law/light_clock_60_receiver_173.py > docs/designs/detector_law/light_clock_60_receiver_173.out
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from light_clock_60_receiver import run  # noqa: E402

CHAIN = dict(n=173, lo=100, set_node=112)
STEPS = 460


def main() -> None:
    omega_b, norm, _cr, series, _closes, rows = run(steps=STEPS, **CHAIN)
    print(
        f"the chain 173, A at [100, 112), the set 112, the mirror 172: A's bare mode omega {omega_b:.5f},"
        f" period {2 * math.pi / omega_b:.2f}; the norm {norm:.4e}; the -x return {2 * 100 * math.sqrt(3):.0f}"
    )
    for W in (64, 256, 1024):
        _, _, c, s_, _, _ = run(W=W, steps=STEPS, **CHAIN)
        before = max((r for a, r in s_ if a < c.get(1.0, 10**9)), default=0.0)
        print(
            f"W = {W:4d}: FIRST RUNG at age {c.get(1.0)}; 1/4 at {c.get(0.25)}, 1/2 at {c.get(0.5)}, "
            f"3/2 at {c.get(1.5)}, 2 at {c.get(2.0)}; the largest reading before the rung {before:.3f} rung"
        )
    _, _, c0, _, _, _ = run(W=64, steps=STEPS, a_take=False, **CHAIN)
    print(f"beside, no take at A's cells (HISTORY's form): first rung {c0.get(1.0)} at W = 64")
    print("the rise at W = 64:", ", ".join(f"{a}:{r:.3f}" for a, r in series if 205 <= a <= 226))
    print("age | energy left | pointer | taken at A | share -x side | share beyond the set")
    for age, e, p, tk, left, cav in rows:
        print(f"{age:5d} | {e:.3e} | {p:.3e} | {tk:.3e} | {left:.3f} | {cav:.3f}")


if __name__ == "__main__":
    main()
