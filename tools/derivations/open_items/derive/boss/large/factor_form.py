"""kappa = F / (w^4 R^6), R = Y_last / Gamma, read from factor.txt's converged per-swing factors (no fit).

usage: python3 -I factor_form.py > factor_form.txt
"""

import math
import re
from pathlib import Path

rows = []
for line in open(Path(__file__).resolve().parent / "factor.txt"):
    m = re.search(
        r"Gamma\s+(\d+) \(R = Y_last/Gamma = ([\d.]+)\), w = ([\d.]+).*F per swing \[(.*?)\]", line
    )
    if m:
        g, R, w = int(m.group(1)), float(m.group(2)), float(m.group(3))
        F = float(m.group(4).split(",")[-1].strip(" '"))
        rows.append((g, R, w, F))
print("kappa = F / (w^4 R^6) from factor.txt's last factor per row (R = Y_last/Gamma ~ sqrt(2 Gamma)):")
for g, R, w, F in rows:
    print(
        f"  Gamma {g:4d}, w {w:.4f}, w R = {w * R:6.2f}: F = {F:.4e}, kappa = {F / (w**4 * R**6):.3f}, log F / log Gamma = {math.log(F) / math.log(g):.3f}"
    )
