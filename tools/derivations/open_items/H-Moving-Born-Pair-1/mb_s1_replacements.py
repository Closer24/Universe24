"""Writes mb_s1_replacements.json: qc1's 17 replacements (HQ_S1, the quartet admitted as a born child) followed by this hand's (MB_S1, the born child laid at a phase pair along the born Link from the take's recoil and the child's wall: k from v = P / (2 E) and the band; the levels logged and the undo from the log)."""
import json, sys

qc1 = json.load(open("/dev/shm/tmp/qc1/hq_s1_replacements.json"))
M = "event_universe/merger.py"
C = "event_universe/close.py"
mine = [
    {"file": M,
     "old": "from event_universe.core.rule3 import least_at, quotient, share_weight\n",
     "new": "from event_universe.core.paces import sine_den\nfrom event_universe.core.rule3 import least_at, quotient, share_weight, signed_quotient\nfrom event_universe.seed import circle_point\n"},
    {"file": M,
     "old": "def child_levels(node: Node, s: int, vector: list[int], sense: int) -> tuple[int, ...]:\n",
     "new": '''def born_phase(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], dp: list[int], booked: int
) -> list[tuple[int, int]]:
    """The born pair's phase pair per end (MB_S1): the recoil P the take books along the born Link (LT-S1), each child's wall E the booked half, the velocity v = P / (2 E) (MV-S2), the wave number by the band's rotation at the row's own sine, sin k = AXES v sin omega / cos omega, the half-angle sine h = den sin(k / 2) to the unit (one carried division per step, every integer within 128 bits), capped at the band's edge; the point of den's circle at h (seed.circle_point), the + end at +h in the slot's direction and the - end at -h (the children moving apart); (den, 0) at h = 0, the rest lay bit for bit."""
    row = node.records()[s]
    assert row.pair is not None
    num = row.pair[0]
    for port in range(PORTS):
        if neighbour(node, minus, port) == plus:
            axis, side = PORT_SIDES[port]
            break
    else:
        raise ValueError("the born Link's ends are not one Link apart")
    p, e = abs(int(dp[axis])), quotient(booked, PLANE)
    h = 0
    if e > 0:
        h = quotient(AXES * sine_den(num, node.den) * quotient(node.den * p, num), (e + e) + (e + e))
        h = min(h, node.den)
    c, sn = circle_point(node.den, h)
    return [(c, -side * sn), (c, side * sn)]


def child_levels(
    node: Node, s: int, vector: list[int], sense: int, phase: tuple[int, int] | None = None
) -> tuple[int, ...]:
'''},
    {"file": M,
     "old": "    for v, j in zip(vector, turned, strict=True):\n        found += [sense * node.A * v, node.B * j]\n    return tuple(found)\n",
     "new": '''    for v, j in zip(vector, turned, strict=True):
        if phase is None:
            found += [sense * node.A * v, node.B * j]
        else:
            c, sn = phase
            found += [
                signed_quotient(sense * node.A * (c * v + sn * j), node.den),
                signed_quotient(node.B * (c * j - sn * v), node.den),
            ]
    return tuple(found)
'''},
    {"file": M,
     "old": "    sign: int = 1,\n    vector: list[int] | None = None,\n) -> list[int]:\n",
     "new": "    sign: int = 1,\n    vector: list[int] | None = None,\n    phase: tuple[int, int] | None = None,\n) -> list[int]:\n"},
    {"file": M,
     "old": "    if vector is not None:\n        levels = child_levels(node, s, vector, sense)\n",
     "new": "    if vector is not None or phase is not None:\n        levels = child_levels(node, s, [1, 0] if vector is None else vector, sense, phase)\n"},
    {"file": C,
     "old": "from __future__ import annotations\n",
     "new": "from __future__ import annotations\n\nimport os\n"},
    {"file": C,
     "old": "from event_universe.merger import (\n    child_at,\n    child_levels,\n    child_vector,\n",
     "new": "from event_universe.merger import (\n    born_phase,\n    child_at,\n    child_levels,\n    child_vector,\n    levels_at,\n"},
    {"file": C,
     "old": "    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...]\n) -> tuple[list[int], list[int], list[list[int]], list[list[int]]]:\n",
     "new": "    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], take: dict[str, Any] | None = None\n) -> tuple[list[int], list[int], list[list[int]], list[list[int]]]:\n"},
    {"file": C,
     "old": "    ends = [\n        child_at(node, s, where, sense, 1, child_vector(node, s, minus, plus, sense))\n        for where, sense in ((minus, -1), (plus, 1))\n    ]\n",
     "new": '''    phases: list[tuple[int, int] | None] = [None, None]
    if take is not None and os.environ.get("MB_S1", ""):
        phases = list(born_phase(node, s, minus, plus, take["dP_take"], take["booked"]))
    ends = [
        child_at(node, s, where, sense, 1, child_vector(node, s, minus, plus, sense), phase)
        for (where, sense), phase in zip(((minus, -1), (plus, 1)), phases, strict=True)
    ]
'''},
    {"file": C,
     "old": "        exact: list[list[int] | None] = []\n",
     "new": "        exact: list[list[int] | None] = []\n        laid: list[list[int]] | None = None\n"},
    {"file": C,
     "old": "            dp_lay, w_children, stood, ends = child_laid(node, s, minus, plus)\n",
     "new": '''            dp_lay, w_children, stood, ends = child_laid(node, s, minus, plus, take)
            if os.environ.get("MB_S1", ""):
                row = node.records()[s]
                laid = [
                    [int(x) - int(y) for x, y in zip(levels_at(row, where), st, strict=True)]
                    for where, st in ((minus, stood[0]), (plus, stood[1]))
                ]
'''},
    {"file": C,
     "old": "                **({\"takes\": take[\"takes\"], \"exact_lay\": exact} if \"takes\" in take else {}),\n",
     "new": "                **({\"takes\": take[\"takes\"], \"exact_lay\": exact} if \"takes\" in take else {}),\n                **({\"laid_levels\": laid} if laid is not None else {}),\n"},
    {"file": C,
     "old": "                    if laid is None:\n                        vector = child_vector(node, s, tuple(entry[\"minus\"]), tuple(entry[\"plus\"]), sense)\n",
     "new": "                    if laid is None and \"laid_levels\" in entry:\n                        lay(node, s, tuple(where), tuple(entry[\"laid_levels\"][int(sense > 0)]), -1)\n                    elif laid is None:\n                        vector = child_vector(node, s, tuple(entry[\"minus\"]), tuple(entry[\"plus\"]), sense)\n"},
]
out = sys.argv[1]
json.dump(qc1 + mine, open(out, "w"), indent=1)
print(len(qc1), "+", len(mine), "->", out)
