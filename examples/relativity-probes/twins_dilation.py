"""Kinematic twin clocks: does a tight computation budget produce velocity-dependent dilation?

The traveller's transport costs route/send operations that the stay-at-home twin does
not pay. With an unlimited budget both clocks tick once per interval (no dilation, as
verified before). With a budget below the moving cycle cost the traveller needs more
than one interval per cycle. Compare the resulting clock ratio with sqrt(1 - v^2/c^2).
"""

import math
import subprocess
import sys

for budget in (1_000_000, 24, 20):
    print(f"\n=== normal_budget {budget} ===")
    for rate in (30, 60, 90, 120):
        out = (
            subprocess.run(
                [sys.executable, "examples/relativity-probes/observer_twins.py", str(budget), str(rate)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            .stdout.strip()
            .splitlines()
        )
        v = rate / 120
        lorentz = math.sqrt(1 - v * v)
        ratio = next(
            (line.split("ratio traveller/home = ")[1].split(";")[0] for line in out if "ratio" in line),
            "n/a",
        )
        print(
            f"  v = {v:.2f} c: ratio traveller/home = {ratio:>6}   sqrt(1-v^2) = {lorentz:.3f}   {out[0]}"
        )
