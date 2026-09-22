"""The comb against the fan's density (COMB_NOTE.md): the crowd of a one-Node
mass on the lattice (the step algebra map's Crowd, host algebra, no run) at the
fan bounds 6 (series K's 290), 8, 10, 12 and 16: (a) the push's path sum along the heading at impact b against the
continuum's (STEP_ALGEBRA section 8), (b) the flow's shell mean against q / (4 pi)
(F_L1), (c) the age moment's shell mean A(r) x r / q (Newton's 1 / r is a constant),
the fraction of a shell's Nodes any line crosses, and the spread of A over the shell. Run from the repository root:

    PYTHONPATH=src python docs/designs/light_bending/comb_map.py > docs/designs/light_bending/comb_map.out
"""

import contextlib
import importlib.util
import io
import math
import statistics
import sys

sys.path.insert(0, "src")
spec = importlib.util.spec_from_file_location("sam", "docs/designs/light_bending/step_algebra_map.py")
m = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(m)
Q = m.Q
heading_s1, heading_t = 1, math.isqrt(3 * Q * Q)
L = 26


def path_sum(crowd, b):
    total = 0
    node_x = -L
    for made in range(0, 2 * L):
        dwell = m.age_of(made + 1, heading_s1, heading_t) - m.age_of(made, heading_s1, heading_t)
        total += dwell * crowd.flow.get((node_x + made, b, 0), [0, 0, 0])[1]
    return total


def shell_nodes(r, half=15):
    return [
        (x, y, z)
        for x in range(-half, half + 1)
        for y in range(-half, half + 1)
        for z in range(-half, half + 1)
        if abs(math.sqrt(x * x + y * y + z * z) - r) < 0.5
    ]


print(
    "bound | q | b=3 | b=6 | b=8 | b=10 | b=14 (the path sum / continuum) | F_L1 | A r / q at r=4,8,12,14 | crossed fraction r=6,12 | CV of A on shell r=6,12"
)
for bound in (6, 8, 10, 12, 16):
    fan = m.primitive_fan(bound)
    q = len(fan)
    crowd = m.Crowd(fan, 1)
    ratios = []
    for b in (3, 6, 8, 10, 14):
        total = path_sum(crowd, b)
        cont = 2 * q * Q * L / (4 * math.pi * b * math.sqrt(L * L + b * b)) * math.sqrt(3)
        ratios.append(total / cont)
    shells = []
    for r in range(4, 15):
        nodes = shell_nodes(r)
        total = sum(math.sqrt(sum(a * a for a in crowd.flow.get(n, [0, 0, 0]))) for n in nodes)
        shells.append(total / len(nodes) * r * r / Q)
    f_l1 = (sum(shells) / len(shells)) / (q / (4 * math.pi))
    a_r = []
    for r in (4, 8, 12, 14):
        nodes = shell_nodes(r)
        a_r.append(sum(crowd.age_moment.get(n, 0) for n in nodes) / len(nodes) * r / q)
    crossed = []
    cv = []
    for r in (6, 12):
        nodes = shell_nodes(r)
        vals = [crowd.age_moment.get(n, 0) for n in nodes]
        crossed.append(sum(1 for v in vals if v) / len(vals))
        cv.append(statistics.pstdev(vals) / statistics.mean(vals))
    print(
        f"{bound:5d} | {q:5d} | "
        + " | ".join(f"{x:.2f}" for x in ratios)
        + f" | {f_l1:.3f} | "
        + ", ".join(f"{x:.3f}" for x in a_r)
        + " | "
        + ", ".join(f"{x:.2f}" for x in crossed)
        + " | "
        + ", ".join(f"{x:.2f}" for x in cv)
    )
