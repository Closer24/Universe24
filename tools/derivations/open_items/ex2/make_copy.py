"""The flagged copy of the engine (hand ex2, 2026-10-25): src/event_universe copied to engine/event_universe beside this
script, with exact text replacements, each matched once; the flag is the environment variable EX2_CARRY=1 (the take's
remainder carried at the Node, EX-S1); with the flag absent every replaced line reduces to the former path (carry 0,
no state array, no log key), so the record is bit for bit the engine's.

Usage: python make_copy.py   (prints the count of replacements, each matched once, or raises)."""

from __future__ import annotations

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[2] / "src" / "event_universe"
DST = HERE / "engine" / "event_universe"

REPLACEMENTS: list[tuple[str, str, str]] = [
    # take.py: the flag
    (
        "take.py",
        "from typing import TYPE_CHECKING, Any\n\nimport numpy as np\n",
        "import os\nfrom typing import TYPE_CHECKING, Any\n\nimport numpy as np\n\n"
        "CARRY = os.environ.get(\"EX2_CARRY\", \"\") == \"1\"  # ex2: the take's remainder carried (EX-S1)\n",
    ),
    # take.py: fall_of takes the carry
    (
        "take.py",
        "    node: Node, at: tuple[int, ...], walls: int, r: rule3.Rule, line: Line\n) -> tuple[int | None, int]:",
        "    node: Node, at: tuple[int, ...], walls: int, r: rule3.Rule, line: Line, carry: int = 0\n"
        ") -> tuple[int | None, int]:",
    ),
    (
        "take.py",
        "    now, before = int(line.now[at]), int(line.before[at])\n    if now == before:\n        return None, 0\n",
        "    if carry >= walls:\n        return 0, 0\n"
        "    now, before = int(line.now[at]), int(line.before[at])\n    if now == before:\n        return None, 0\n",
    ),
    (
        "take.py",
        "    full = fall(dist)\n    if full < walls:\n        return None, full\n",
        "    full = fall(dist)\n    if full + carry < walls:\n        return None, full\n    walls = walls - carry\n",
    ),
    # take.py: take_at reads the carry, writes the remainder, books the counts
    (
        "take.py",
        "    levels, fall = fall_of(node, at, walls, r_gap0, z)\n    if levels is None:",
        "    rec0 = node.records().index(gap0)\n"
        "    carry = int(node.taken_rem[rec0][at]) if CARRY else 0\n"
        "    levels, fall = fall_of(node, at, walls, r_gap0, z, carry)\n    if levels is None:",
    ),
    (
        "take.py",
        "                \"fall\": fall,\n                \"walls\": walls,\n            }\n        )\n        return None\n",
        "                \"fall\": fall,\n                \"walls\": walls,\n"
        "                **({\"carry\": carry} if CARRY else {}),\n            }\n        )\n        return None\n",
    ),
    (
        "take.py",
        "    node.last_dp = momentum_of(node, z.now, z.before, at, d_now=toward * levels, num=gap0.pair[0])\n"
        "    return levels, fall, now, before\n",
        "    node.last_dp = momentum_of(node, z.now, z.before, at, d_now=toward * levels, num=gap0.pair[0])\n"
        "    if CARRY:\n"
        "        node.taken_rem[rec0][at] = carry + fall - walls\n"
        "        node.last_rem = [carry, carry + fall - walls, walls]\n"
        "        node.rem_at[at] = node.last_rem\n"
        "        node.counts[\"taken_all\"] = node.counts.get(\"taken_all\", 0) + fall\n"
        "        node.counts[\"booked_all\"] = node.counts.get(\"booked_all\", 0) + walls\n"
        "        node.counts[\"take_rem_held\"] = node.counts.get(\"take_rem_held\", 0) + fall - walls\n"
        "        node.counts[\"takes_from_carry\"] = node.counts.get(\"takes_from_carry\", 0) + (1 if levels == 0 else 0)\n"
        "    return levels, fall, now, before\n",
    ),
    # node.py: the state array per record, in the census and the state bytes
    (
        "node.py",
        "        self.stepped: list[list[Line]] = []\n",
        "        self.stepped: list[list[Line]] = []\n"
        "        self.taken_rem: list[Any] = [zeros(shape) for _ in range(nr)] if take.CARRY else []\n"
        "        self.last_rem = [0, 0, 0]\n        self.rem_at: dict[tuple[int, ...], list[int]] = {}\n",
    ),
    (
        "node.py",
        "        arrays += self.standing + self.crossed + self.beats + [self.proper, self.closes]\n"
        "        return len(arrays), max(bits_of(a) for a in arrays)\n",
        "        arrays += self.standing + self.crossed + self.beats + [self.proper, self.closes]\n"
        "        arrays += self.taken_rem\n"
        "        return len(arrays), max(bits_of(a) for a in arrays)\n",
    ),
    (
        "node.py",
        "        arrays += [line.wr for line in lines if line.wr is not None]\n"
        "        return \" \".join(str(int(v)) for a in arrays for v in a.reshape(-1)).encode()\n",
        "        arrays += [line.wr for line in lines if line.wr is not None]\n"
        "        arrays += self.taken_rem\n"
        "        return \" \".join(str(int(v)) for a in arrays for v in a.reshape(-1)).encode()\n",
    ),
    # close.py: the birth and credit lines carry the remainder, the undo restores it
    (
        "close.py",
        "from event_universe.take import (\n    frame_nodes,",
        "from event_universe.take import (\n    CARRY,\n    frame_nodes,",
    ),
    (
        "close.py",
        "                \"dP_take\": dp_take,\n                \"dP_lay\": dp_lay,\n            }\n        )\n    return touched\n",
        "                \"dP_take\": dp_take,\n                \"dP_lay\": dp_lay,\n"
        "                **({\"take_rem\": list(node.rem_at[at])} if CARRY else {}),\n            }\n        )\n    return touched\n",
    ),
    (
        "close.py",
        "        \"sign_level\": int(node.row(POTENTIAL).lines[0].now[at]),\n        \"turned\": bool(node.turned[at]),\n    }\n",
        "        \"sign_level\": int(node.row(POTENTIAL).lines[0].now[at]),\n        \"turned\": bool(node.turned[at]),\n"
        "        **({\"take_rem\": list(node.rem_at[at]), \"booked\": node.units[rec]} if CARRY else {}),\n    }\n",
    ),
    (
        "close.py",
        "            lay(node, rec0, at, (entry[\"taken_now_was\"] - int(gap0.lines[0].now[at]), 0, 0, 0))\n"
        "            node.closes[at] -= 1\n",
        "            lay(node, rec0, at, (entry[\"taken_now_was\"] - int(gap0.lines[0].now[at]), 0, 0, 0))\n"
        "            node.closes[at] -= 1\n"
        "            if CARRY:\n                node.taken_rem[rec0][at] = entry[\"take_rem\"][0]\n",
    ),
]


def main() -> None:
    if DST.parent.exists():
        shutil.rmtree(DST.parent)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))
    done = 0
    for name, old, new in REPLACEMENTS:
        path = DST / name
        text = path.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise SystemExit(f"{name}: the text to replace is matched {text.count(old)} times, not once:\n{old}")
        path.write_text(text.replace(old, new), encoding="utf-8")
        done += 1
    print(f"{done} replacements, each matched once; the copy at {DST}")


if __name__ == "__main__":
    main()
