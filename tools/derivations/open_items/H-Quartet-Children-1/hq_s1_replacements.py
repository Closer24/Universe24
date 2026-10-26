"""The flag HQ_S1's replacements for the kit's make_flagged_copy.py (H-Quartet-Children-1): with the flag empty every path is the head's bit for bit; with the flag set the draw names the quartet among the children's rows (rows.BORN), a child's lay is the one form now = sense A v, before = B (J v) with v the lay's vector (the plane's (1, 0) by name, the quartet's the eigenvector of the born Link's axis matrix at the sense's sign in the Link's direction), the lay's momentum per line, and the click at -1 the same lay removed."""

import json
import sys

R = []


def rep(file, old, new):
    R.append({"file": "event_universe/" + file, "old": old, "new": new})


rep("rows.py", "from typing import Any\n\nimport numpy as np\n", "import os\nfrom typing import Any\n\nimport numpy as np\n")
rep(
    "rows.py",
    "QUARTET = 8\n",
    "QUARTET = 8\nBORN = (PLANE, QUARTET) if os.environ.get(\"HQ_S1\", \"\") else (PLANE,)  # the shapes the draw names for a birth's children (HQ_S1: the quartet admitted; empty: the planes alone, the head)\n",
)
rep("draw.py", "from event_universe.rows import PLANE, Line\n", "from event_universe.rows import BORN, Line\n")
rep(
    "draw.py",
    "modulus = unit * sum(1 for r in node.records() if r.shape == PLANE)",
    "modulus = unit * sum(1 for r in node.records() if r.shape in BORN)",
)
rep("close.py", "from event_universe.rows import PLANE, Line\n", "from event_universe.rows import BORN, PLANE, Line\n")
rep(
    "close.py",
    "    planes = [k for k, r in enumerate(records) if r.shape == PLANE]\n",
    "    planes = [k for k, r in enumerate(records) if r.shape in BORN]\n",
)
rep(
    "close.py",
    "from event_universe.merger import (\n    child_at,\n",
    "from event_universe.merger import (\n    child_at,\n    child_levels,\n    child_vector,\n",
)
rep(
    "close.py",
    """    re, im = node.records()[s].lines
    stood = [[int(a[w_]) for a in (re.now, re.before, im.now, im.before)] for w_ in (minus, plus)]
    ends = [child_at(node, s, where, sense) for where, sense in ((minus, -1), (plus, 1))]
    dp_lay = [a + b for a, b in zip(*ends, strict=True)]
    senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
""",
    """    row = node.records()[s]
    stood = [[int(a[w_]) for line in row.lines for a in (line.now, line.before)] for w_ in (minus, plus)]
    ends = [
        child_at(node, s, where, sense, 1, child_vector(node, s, minus, plus, sense))
        for where, sense in ((minus, -1), (plus, 1))
    ]
    dp_lay = [a + b for a, b in zip(*ends, strict=True)]
    if row.shape == PLANE:
        re, im = row.lines
        senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
    else:
        senses = [int(gram.charge(row.shape, row.lines)[w_]) for w_ in (minus, plus)]
""",
)
rep(
    "close.py",
    """                    if laid is None:
                        lay(node, s, tuple(where), (sense * a, 0, 0, b), -1)
""",
    """                    if laid is None:
                        vector = child_vector(node, s, tuple(entry["minus"]), tuple(entry["plus"]), sense)
                        if vector is None:
                            lay(node, s, tuple(where), (sense * a, 0, 0, b), -1)
                        else:
                            lay(node, s, tuple(where), child_levels(node, s, vector, sense), -1)
""",
)
rep("merger.py", "from event_universe.core.ports import AXES\n", "from event_universe.core.ports import AXES, PORTS, PORT_SIDES\n")
rep("merger.py", "from event_universe.rows import Line, zeros\n", "from event_universe.rows import PLANE, Line, zeros\n")
rep(
    "merger.py",
    """def child_at(node: Node, s: int, where: tuple[int, ...], sense: int, sign: int = 1) -> list[int]:""",
    """def child_vector(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], sense: int
) -> list[int] | None:
    \"\"\"The lay's vector of a child by its row's shape (HQ_S1): none for a plane (the lay (A, 0 | 0, B) by name, the vector (1, 0)); for a row with axis matrices the integer eigenvector of the born Link's axis matrix at the eigenvalue of the sense's sign in the Link's direction from the - end to the + end (the two children's axes opposite).\"\"\"
    row = node.records()[s]
    if row.shape == PLANE:
        return None
    for port in range(PORTS):
        if neighbour(node, minus, port) == plus:
            axis, side = PORT_SIDES[port]
            return gram.spin_vector(row.shape, axis, sense * side)
    raise ValueError("the born Link's ends are not one Link apart")


def child_levels(node: Node, s: int, vector: list[int], sense: int) -> tuple[int, ...]:
    \"\"\"A child's levels (now, before per line) along the lay's vector v at the charge T div 2 (HQ_S1, GP-S1's one form for every shape): now = sense A v, before = B (J v); the plane's (sense A, 0 | 0, B) at v = (1, 0).\"\"\"
    shape = node.records()[s].shape
    turned = gram.matvec(gram.rotation(shape), list(vector))
    found: list[int] = []
    for v, j in zip(vector, turned, strict=True):
        found += [sense * node.A * v, node.B * j]
    return tuple(found)


def child_at(
    node: Node,
    s: int,
    where: tuple[int, ...],
    sense: int,
    sign: int = 1,
    vector: list[int] | None = None,
) -> list[int]:""",
)
rep(
    "merger.py",
    """    row = node.records()[s]
    re, im = row.lines
    assert row.pair is not None
    num = row.pair[0]
    dp = momentum_of(node, re.now, re.before, where, d_now=sign * sense * node.A, num=num)
""",
    """    row = node.records()[s]
    assert row.pair is not None
    num = row.pair[0]
    if vector is not None:
        levels = child_levels(node, s, vector, sense)
        dp_all = [0] * AXES
        for k, line in enumerate(row.lines):
            dk = momentum_of(
                node,
                line.now,
                line.before,
                where,
                d_now=sign * levels[PLANE * k],
                d_before=sign * levels[PLANE * k + 1],
                num=num,
            )
            dp_all = [a + b for a, b in zip(dp_all, dk, strict=True)]
        lay(node, s, where, levels, sign)
        return dp_all
    re, im = row.lines
    dp = momentum_of(node, re.now, re.before, where, d_now=sign * sense * node.A, num=num)
""",
)
rep(
    "merger.py",
    """    for where, sense in ((minus, -1), (plus, 1)):
        if (s, sense, where) not in cache:
            row.lines = [
                Line(zeros(node.shape), zeros(node.shape), line.rem, line.wall) for line in held
            ]
            child_at(node, s, where, sense)
            cache[(s, sense, where)] = sum(
                share_at(node, row.lines, rule, at) for at in set(frame_nodes(node, where))
            )
        found.append(cache[(s, sense, where)])
""",
    """    for where, sense in ((minus, -1), (plus, 1)):
        vector = child_vector(node, s, minus, plus, sense)
        key: Any = (s, sense, where) if vector is None else (s, sense, where, tuple(vector))
        if key not in cache:
            row.lines = [
                Line(zeros(node.shape), zeros(node.shape), line.rem, line.wall) for line in held
            ]
            child_at(node, s, where, sense, 1, vector)
            cache[key] = sum(
                share_at(node, row.lines, rule, at) for at in set(frame_nodes(node, where))
            )
        found.append(cache[key])
""",
)
rep(
    "gram.py",
    "from event_universe.quartet import quartet\n",
    "from event_universe.quartet import kernel_vector, quartet\n",
)
rep(
    "gram.py",
    """def scale(shape: int, gamma: Any) -> Any:""",
    """def spin_vector(shape: int, axis: int, sign: int) -> list[int]:
    \"\"\"The row's lay vector along the axis at the sign (HQ_S1): the integer eigenvector of the axis matrix Gamma_a at the eigenvalue +1 (the quartet's up along z the case axis 2), and at -1 that vector turned by the next axis's matrix, Gamma_(a+1) v, an eigenvector at -1 of the same G-norm (Gamma_b anticommutes with Gamma_a and keeps G), so the two children's charges are opposite and sum to 0.\"\"\"
    g = axes(shape)[axis]
    up = kernel_vector([[g[r][c] - int(r == c) for c in range(len(g))] for r in range(len(g))])
    return up if sign > 0 else matvec(axes(shape)[wrap(axis + 1, AXES)], up)


def scale(shape: int, gamma: Any) -> Any:""",
)

rep(
    "merger.py",
    """            (re, im), (re_now, re_before, im_now, im_before) = row.lines, levels
            dp = momentum_of(node, re.now, re.before, where, -re_now, -re_before, row.pair[0])
            dp_im = momentum_of(node, im.now, im.before, where, -im_now, -im_before, row.pair[0])
            lay(node, rec, where, levels, -1)
            node.closes[where] -= 1
            size, moment = sum(abs(x) for x in levels), [a + b for a, b in zip(dp, dp_im, strict=True)]
""",
    """            moment = [0] * AXES
            for j, line in enumerate(row.lines):
                dj = momentum_of(
                    node,
                    line.now,
                    line.before,
                    where,
                    -levels[PLANE * j],
                    -levels[PLANE * j + 1],
                    row.pair[0],
                )
                moment = [a + b for a, b in zip(moment, dj, strict=True)]
            lay(node, rec, where, levels, -1)
            node.closes[where] -= 1
            size = sum(abs(x) for x in levels)
""",
)

json.dump(R, open(sys.argv[1], "w"), indent=1)
print(len(R), "replacements")
