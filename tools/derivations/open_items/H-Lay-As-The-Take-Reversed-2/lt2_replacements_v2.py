"""Writes lt2_replacements_v2.json: the lay as the take reversed on the Link's record, the mended form (one carried division per far Node per close, every numerator summed before any write, CR-S2), behind LT2_LAY_REVERSED, in close.py alone (H-Lay-As-The-Take-Reversed-2)."""
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
    node: Node,
    s: int,
    at: tuple[int, ...],
    sense: int,
    take: dict[str, Any],
    rec: int,
    totals: dict[tuple[int, tuple[int, ...]], int],
) -> list[list[Any]]:
    """The lay as the take reversed on the Link's record, the reads (H-Lay-As-The-Take-Reversed-2, behind the flag LT2_LAY_REVERSED): at each of the six neighbours j of the take's Node the taken line's Link record the take removed, R_j = d before_j (the count d of quanta the take moved times the taken line's level before at j), to be returned on the children's re line's before at j, whose now at the take's Node is the child's sense A; the numerator -sense R_j times the quotient of that line's wall at j by A is summed into `totals` per record and Node, so that one carried division per Node is written after every birth of the close is read (CR-S2); returns the Link records read."""
    re = node.records()[s].lines[0]
    z = node.records()[rec].lines[take["taken_line"]]
    now_was, before_at, count = take["taker"]
    d = count if before_at > now_was else -count
    found: list[list[Any]] = []
    for port in range(PORTS):
        j = neighbour(node, at, port)
        record = d * int(z.before[j])
        total = -sense * record * quotient(at_node(re.wall, j), node.A)
        totals[(s, j)] = totals.get((s, j), 0) + total
        found.append([list(j), record, total])
    return found


def far_flush(
    node: Node, totals: dict[tuple[int, tuple[int, ...]], int]
) -> tuple[list[list[Any]], list[int]]:
    """The lay as the take reversed, the writes: per record and Node one carried division of the summed numerator at the children's re line's own wall at that Node in the direction -1, the quotient laid on the line's before, the remainder kept in the line's own remainder (exact where A divides the wall), the momentum of each write booked at its Node; returns the writes and the momentum summed."""
    found: list[list[Any]] = []
    dp = [0] * AXES
    for s, j in sorted(totals):
        row = node.records()[s]
        assert row.pair is not None
        re = row.lines[0]
        wall, rem_was = at_node(re.wall, j), int(re.rem[j])
        q, rest = rule3.carried_division(totals[(s, j)], wall, rem_was, -1)
        moved = momentum_of(node, re.now, re.before, j, d_before=q, num=row.pair[0])
        dp = [a + b for a, b in zip(dp, moved, strict=True)]
        re.before[j] = re.before[j] + q
        re.rem[j] = rest
        found.append([s, list(j), totals[(s, j)], q, rem_was, rest])
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
        at, take, rec, totals = reversed_at
        which = (minus, plus).index(at)
        far = lay_reversed(node, s, at, which + which - 1, take, rec, totals)
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
                node,
                s,
                minus,
                plus,
                (at, take, rec, totals) if take.get("taken_line") is not None else None,
            )
'''})
R.append({"file": "event_universe/close.py",
    "old": "                **({\"takes\": take[\"takes\"], \"exact_lay\": exact} if \"takes\" in take else {}),\n",
    "new": "                **({\"takes\": take[\"takes\"], \"exact_lay\": exact} if \"takes\" in take else {}),\n                **({\"far_records\": far} if far else {}),\n"})
R.append({"file": "event_universe/close.py",
    "old": "    rec: int,\n    c: Any,\n    factors: tuple[Any, ...],\n) -> set[tuple[int, ...]]:\n",
    "new": "    rec: int,\n    c: Any,\n    factors: tuple[Any, ...],\n    totals: dict[tuple[int, tuple[int, ...]], int] | None = None,\n) -> set[tuple[int, ...]]:\n"})
R.append({"file": "event_universe/close.py",
    "old": "    touched: set[tuple[int, ...]] = set()\n    for at, rec, kids, take in taken:\n        touched |= children(node, at, kids, take, rec, c, factors)\n        node.counts[\"taken\"] += take[\"taken\"]\n        node.counts[\"booked\"] += take[\"booked\"]\n    return touched\n",
    "new": '''    touched: set[tuple[int, ...]] = set()
    totals: dict[tuple[int, tuple[int, ...]], int] = {}
    for at, rec, kids, take in taken:
        touched |= children(node, at, kids, take, rec, c, factors, totals)
        node.counts["taken"] += take["taken"]
        node.counts["booked"] += take["booked"]
    if totals:
        far, dp_far = far_flush(node, totals)
        node.log[-1]["lay_far"] = far
        node.log[-1]["dP_far"] = dp_far
    return touched
'''})
R.append({"file": "event_universe/close.py",
    "old": "                exact = entry.get(\"exact_lay\", [None, None])\n",
    "new": '''                exact = entry.get("exact_lay", [None, None])
                for s_far, where, _total, q, rem_was, _rest in reversed(entry.get("lay_far", [])):
                    far_line = node.records()[s_far].lines[0]
                    far_line.before[tuple(where)] = far_line.before[tuple(where)] - q
                    far_line.rem[tuple(where)] = rem_was
'''})
json.dump(R, open(sys.argv[1], "w"), indent=1)
print(len(R), "replacements")
