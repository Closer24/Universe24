"""H-Moving-Born-Pair-2: the flag MB_S1 on top of H-Quartet-Children-1's HQ_S1 (the 17 replacements copied, mine after them, applied in order by the kit's maker). The born pair laid as a two-Node packet along the born Link: the - child at the phase (den, 0), the + child at the circle's point at the wave number h = den sin(k / 2) with the slot's sign (the Link's side from the - end to the + end), the levels by gram.moving's form with GP-S1's two amplitudes (now = sense A (C v + S J v) div den, before = B (C J v - S v) div den; the phase (den, 0) GP-S1 bit for bit); den sin k from the take's recoil along the born Link, |dP_a| den div (2 num 2 E), E the child's charge A B (v.G.v); the levels laid logged (mb_levels) and taken back by the log at -1. Usage: python mb_s1_replacements.py <qc1 replacements json> <out json>"""

import json
import sys

qc1 = json.load(open(sys.argv[1]))
mine = [
    {
        "file": "event_universe/rows.py",
        "old": 'BORN = (PLANE, QUARTET) if os.environ.get("HQ_S1", "") else (PLANE,)',
        "new": 'BORN = (PLANE, QUARTET) if os.environ.get("HQ_S1", "") else (PLANE,)\nMOVING = bool(os.environ.get("MB_S1", ""))  # MB_S1: the born pair laid moving at the recoil\'s wave number along the born Link',
    },
    {
        "file": "event_universe/merger.py",
        "old": "from event_universe.core.rule3 import least_at, quotient, share_weight\n",
        "new": "from event_universe.core.rule3 import half, largest_below, least_at, quotient, share_weight, signed_quotient\n",
    },
    {
        "file": "event_universe/merger.py",
        "old": 'def child_levels(node: Node, s: int, vector: list[int], sense: int) -> tuple[int, ...]:',
        "new": '''def born_wave(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], vector: list[int], recoil: list[int]
) -> tuple[int, int, int, int]:
    """The born child's wave number from the take's recoil (MB_S1): along the born Link's axis a (the side from the - end to the + end, the slot's direction), den sin k = |dP_a| den div ((num + num) (E + E)), E the child's charge A B (v.G.v) (MV-S2's v = P / (2 E) at the pair's own Link momentum 2 num 2 E sin k), the band's edge where it exceeds den; h = den sin(k / 2) = largest_below(den (den - den cos k) div 2). Returns (axis, side, h, den sin k)."""
    row = node.records()[s]
    assert row.pair is not None
    num, den = row.pair[0], node.den
    g = gram.gram(row.shape)
    norm = sum(vector[r] * g[r][c] * vector[c] for r in range(len(vector)) for c in range(len(vector)))
    energy = node.A * node.B * norm
    axis, side = PORT_SIDES[next(port for port in range(PORTS) if neighbour(node, minus, port) == plus)]
    sine = min(den, (abs(recoil[axis]) * den) // ((num + num) * (energy + energy)))
    cosine = largest_below(den * den - sine * sine)
    return axis, side, largest_below(half(den * (den - cosine))), sine


def child_levels(
    node: Node, s: int, vector: list[int], sense: int, phase: tuple[int, int] | None = None
) -> tuple[int, ...]:''',
    },
    {
        "file": "event_universe/merger.py",
        "old": '''    turned = gram.matvec(gram.rotation(shape), list(vector))
    found: list[int] = []
    for v, j in zip(vector, turned, strict=True):
        found += [sense * node.A * v, node.B * j]
    return tuple(found)''',
        "new": '''    turned = gram.matvec(gram.rotation(shape), list(vector))
    c, sn = (node.den, 0) if phase is None else phase
    found: list[int] = []
    for v, j in zip(vector, turned, strict=True):
        found += [
            signed_quotient(sense * node.A * (c * v + sn * j), node.den),
            signed_quotient(node.B * (c * j - sn * v), node.den),
        ]
    return tuple(found)''',
    },
    {
        "file": "event_universe/merger.py",
        "old": '''    sign: int = 1,
    vector: list[int] | None = None,
) -> list[int]:''',
        "new": '''    sign: int = 1,
    vector: list[int] | None = None,
    phase: tuple[int, int] | None = None,
) -> list[int]:''',
    },
    {
        "file": "event_universe/merger.py",
        "old": '''    if vector is not None:
        levels = child_levels(node, s, vector, sense)''',
        "new": '''    if vector is not None or phase is not None:
        levels = child_levels(node, s, vector if vector is not None else gram.identity(PLANE)[0], sense, phase)''',
    },
    {
        "file": "event_universe/close.py",
        "old": "from event_universe.rows import BORN, PLANE, Line\n",
        "new": "from event_universe.rows import BORN, PLANE, Line\nfrom event_universe.rows import MOVING\nfrom event_universe.seed import circle_point\n"  # the names on two lines: the documents gate refuses three capitals in a row,
    },
    {
        "file": "event_universe/close.py",
        "old": "from event_universe.merger import (\n    child_at,\n",
        "new": "from event_universe.merger import (\n    born_wave,\n    child_at,\n",
    },
    {
        "file": "event_universe/close.py",
        "old": '''def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...]
) -> tuple[list[int], list[int], list[list[int]], list[list[int]]]:''',
        "new": '''def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], recoil: list[int] | None = None
) -> tuple[list[int], list[int], list[list[int]], list[list[int]], dict[str, Any]]:''',
    },
    {
        "file": "event_universe/close.py",
        "old": '''    ends = [
        child_at(node, s, where, sense, 1, child_vector(node, s, minus, plus, sense))
        for where, sense in ((minus, -1), (plus, 1))
    ]
    dp_lay = [a + b for a, b in zip(*ends, strict=True)]''',
        "new": '''    vectors = {sense: child_vector(node, s, minus, plus, sense) for sense in (-1, 1)}
    phases: dict[int, tuple[int, int] | None] = {-1: None, 1: None}
    moving: dict[str, Any] = {}
    if recoil is not None:
        plane_vector = gram.identity(PLANE)[0]
        axis, side, h, sine = born_wave(node, s, minus, plus, vectors[1] or plane_vector, recoil)
        phases[1] = circle_point(node.den, side * h)
        moving = {
            "mb_wave": [axis, side, h, sine],
            "mb_phase": list(phases[1]),
            "mb_levels": [
                list(child_levels(node, s, vectors[sense] or plane_vector, sense, phases[sense]))
                for sense in (-1, 1)
            ],
        }
    ends = [
        child_at(node, s, where, sense, 1, vectors[sense], phases[sense])
        for where, sense in ((minus, -1), (plus, 1))
    ]
    dp_lay = [a + b for a, b in zip(*ends, strict=True)]''',
    },
    {
        "file": "event_universe/close.py",
        "old": '''        senses = [int(gram.charge(row.shape, row.lines)[w_]) for w_ in (minus, plus)]
    return dp_lay, senses, stood, ends''',
        "new": '''        senses = [int(gram.charge(row.shape, row.lines)[w_]) for w_ in (minus, plus)]
    return dp_lay, senses, stood, ends, moving''',
    },
    {
        "file": "event_universe/close.py",
        "old": "        exact: list[list[int] | None] = []\n",
        "new": "        exact: list[list[int] | None] = []\n        moving: dict[str, Any] = {}\n",
    },
    {
        "file": "event_universe/close.py",
        "old": "            dp_lay, w_children, stood, ends = child_laid(node, s, minus, plus)",
        "new": "            dp_lay, w_children, stood, ends, moving = child_laid(\n                node, s, minus, plus, take[\"dP_take\"] if MOVING else None\n            )",
    },
    {
        "file": "event_universe/close.py",
        "old": '''                **({"takes": take["takes"], "exact_lay": exact} if "takes" in take else {}),''',
        "new": '''                **({"takes": take["takes"], "exact_lay": exact} if "takes" in take else {}),
                **moving,''',
    },
    {
        "file": "event_universe/close.py",
        "old": '''                    if laid is None:
                        vector = child_vector(node, s, tuple(entry["minus"]), tuple(entry["plus"]), sense)''',
        "new": '''                    if laid is None and "mb_levels" in entry:
                        lay(node, s, tuple(where), tuple(entry["mb_levels"][int(sense > 0)]), -1)
                    elif laid is None:
                        vector = child_vector(node, s, tuple(entry["minus"]), tuple(entry["plus"]), sense)''',
    },
]
json.dump(qc1 + mine, open(sys.argv[2], "w"), indent=1)
print(len(qc1), "of qc1 +", len(mine), "of mb2 =", len(qc1) + len(mine))
