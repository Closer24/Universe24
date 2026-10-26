"""Writes lt2_replacements.json: the lay as the take reversed on the Link's record, behind LT2_LAY_REVERSED, in close.py alone (H-Lay-As-The-Take-Reversed-2)."""
import json
import sys

R = []
R.append({"file": "event_universe/close.py",
    "old": "from event_universe.core.ports import AXES, across, port_of\n",
    "new": "from os import environ\n\nfrom event_universe.core.ports import AXES, PORTS, across, port_of\n"})
R.append({"file": "event_universe/close.py",
    "old": "from event_universe.take import lay, move, neighbour\n",
    "new": "from event_universe.take import at_node, lay, momentum_of, move, neighbour\n\nLAY_REVERSED = environ.get(\"LT2_LAY_REVERSED\", \"\")\n"})
R.append({"file": "event_universe/close.py",
    "old": "def child_laid(\n    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...]\n) -> tuple[list[int], list[int], list[list[int]], list[list[int]]]:\n",
    "new": '''def lay_reversed(
    node: Node, s: int, at: tuple[int, ...], sense: int, take: dict[str, Any], rec: int
) -> tuple[list[list[Any]], list[int]]:
    """The lay as the take reversed on the Link's record (H-Lay-As-The-Take-Reversed-2, behind the flag LT2_LAY_REVERSED): at each of the six neighbours j of the take's Node the taken line's Link record the take removed, R_j = d before_j (the count d of quanta the take moved times the taken line's level before at j), returned on the children's re line's before at j by one carried division at that line's own wall at j in the direction -1 (the numerator -sense R_j times the wall's quotient by A, so the quotient is the division of -sense R_j by A and the remainder stays in the line's own remainder at j, exact where A divides the wall), the momentum of each write booked at j; the child's re now at the take's Node is sense A, so the children's record on the Link (at, j) changes by sense A q_j against the taken row's R_j."""
    row = node.records()[s]
    assert row.pair is not None
    re = row.lines[0]
    z = node.records()[rec].lines[take["taken_line"]]
    now_was, before_at, count = take["taker"]
    d = count if before_at > now_was else -count
    found: list[list[Any]] = []
    dp = [0] * AXES
    for port in range(PORTS):
        j = neighbour(node, at, port)
        wall, record, rem_was = at_node(re.wall, j), d * int(z.before[j]), int(re.rem[j])
        q, rest = rule3.carried_division(-sense * record * quotient(wall, node.A), wall, rem_was, -1)
        moved = momentum_of(node, re.now, re.before, j, d_before=q, num=row.pair[0])
        dp = [a + b for a, b in zip(dp, moved, strict=True)]
        re.before[j] = re.before[j] + q
        re.rem[j] = rest
        found.append([list(j), record, q, rem_was, rest])
    return found, dp


def child_laid(
    node: Node,
    s: int,
    minus: tuple[int, ...],
    plus: tuple[int, ...],
    reversed_at: tuple[Any, ...] | None = None,
) -> tuple[list[int], list[int], list[list[int]], list[list[int]], list[list[Any]]]:
'''})
R.append({"file": "event_universe/close.py",
    "old": "    ends = [child_at(node, s, where, sense) for where, sense in ((minus, -1), (plus, 1))]\n    dp_lay = [a + b for a, b in zip(*ends, strict=True)]\n",
    "new": '''    ends = [child_at(node, s, where, sense) for where, sense in ((minus, -1), (plus, 1))]
    far: list[list[Any]] = []
    if LAY_REVERSED and reversed_at is not None:
        at, take, rec = reversed_at
        which = (minus, plus).index(at)
        far, dp = lay_reversed(node, s, at, which + which - 1, take, rec)
        ends[which] = [a + b for a, b in zip(ends[which], dp, strict=True)]
    dp_lay = [a + b for a, b in zip(*ends, strict=True)]
'''})
R.append({"file": "event_universe/close.py",
    "old": "    return dp_lay, senses, stood, ends\n",
    "new": "    return dp_lay, senses, stood, ends, far\n"})
R.append({"file": "event_universe/close.py",
    "old": "        exact: list[list[int] | None] = []\n",
    "new": "        exact: list[list[int] | None] = []\n        far: list[list[Any]] = []\n"})
R.append({"file": "event_universe/close.py",
    "old": "            dp_lay, w_children, stood, ends = child_laid(node, s, minus, plus)\n",
    "new": '''            dp_lay, w_children, stood, ends, far = child_laid(
                node, s, minus, plus, (at, take, rec) if take.get("taken_line") is not None else None
            )
'''})
R.append({"file": "event_universe/close.py",
    "old": "                **({\"takes\": take[\"takes\"], \"exact_lay\": exact} if \"takes\" in take else {}),\n",
    "new": "                **({\"takes\": take[\"takes\"], \"exact_lay\": exact} if \"takes\" in take else {}),\n                **({\"lay_far\": far} if far else {}),\n"})
R.append({"file": "event_universe/close.py",
    "old": "                exact = entry.get(\"exact_lay\", [None, None])\n",
    "new": '''                exact = entry.get("exact_lay", [None, None])
                for where, _record, q, rem_was, _rest in reversed(entry.get("lay_far", [])):
                    far_line = node.records()[s].lines[0]
                    far_line.before[tuple(where)] = far_line.before[tuple(where)] - q
                    far_line.rem[tuple(where)] = rem_was
'''})
json.dump(R, open(sys.argv[1], "w"), indent=1)
print(len(R), "replacements")
