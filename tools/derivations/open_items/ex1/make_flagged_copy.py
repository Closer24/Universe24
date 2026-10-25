"""ex1: the flagged copy of the engine (src/event_universe) under tools/derivations/ex1/engine, written by exact text
replacements, each named; the flag is the toy's control key "take": "remainder" (with "take_origin": "zero" or "half");
the flag absent, every replaced line is inert and the record is David's bit for bit (checked by compare_records.py).
Usage: make_flagged_copy.py <worktree>"""
import os
import shutil
import sys

REPLACEMENTS = {
    "node.py": [
        (
            "R1 the take's remainder array born with the state (one array of the board's shape)",
            "        self.last_dp = [0, 0, 0]\n",
            "        self.last_dp = [0, 0, 0]\n        self.take_rem = zeros(shape)  # ex1 R1: the take's remainder at the Node\n        self.take_log: dict[tuple[int, ...], dict[str, int]] = {}  # ex1 R1: each Node's last take's remainder numbers for the log\n",
        ),
        (
            "R2 the census counts the remainder under the flag alone",
            "        arrays += self.standing + self.crossed + self.beats + [self.proper, self.closes]\n",
            "        arrays += self.standing + self.crossed + self.beats + [self.proper, self.closes]\n        arrays += take.remainder_arrays(self)  # ex1 R2\n",
        ),
        (
            "R3 the state's bytes carry the remainder under the flag alone (the run back's comparison)",
            '        return " ".join(str(int(v)) for a in arrays for v in a.reshape(-1)).encode()\n',
            '        arrays += take.remainder_arrays(self)  # ex1 R3\n        return " ".join(str(int(v)) for a in arrays for v in a.reshape(-1)).encode()\n',
        ),
        (
            "R4 the remainder born after the seed (the half wall under take_origin half, 0 under zero)",
            "        self.ride_walls()\n",
            "        self.ride_walls()\n        take.born_remainder(self)  # ex1 R4\n",
        ),
    ],
    "take.py": [
        (
            "R5 the helpers: the flag, the remainder arrays, the one-level step, the birth of the remainder",
            "def take_at(\n",
            '''def take_flag(node: Node) -> str:
    """ex1 R5: the flag read from the toy's control key `take` ("" when absent: David's path)."""
    return str(getattr(node, "control", {}).get("take", ""))


def remainder_arrays(node: Node) -> list[Any]:
    """ex1 R5: the take's remainder as one more state array under the flag, none without it."""
    return [node.take_rem] if take_flag(node) == "remainder" else []


def step_of(node: Node, at: tuple[int, ...], r: rule3.Rule, line: Line) -> int:
    """ex1 R5: the one-level fall toward before at the Node (fall(1) of `fall_of`), 0 where now equals before."""
    now, before = int(line.now[at]), int(line.before[at])
    if now == before:
        return 0
    t = 1 if before > now else -1
    own, w = int(np.asarray(r.self_coefficient)[at]), int(r.wall)
    reached = 0
    for port, reach in enumerate(r.reaches):
        reached += int(np.asarray(reach)[at]) * int(line.before[neighbour(node, at, port)])
    pace = int(np.asarray(paces.link_pace_of(node.gamma, node.start_content), dtype=object)[at])
    weight = 2 * pace * pace * node.G * node.G + (1 if pace == 0 else 0)
    return int(quotient(w * (now * now - (now + t) ** 2) - t * (own * before + reached), weight))


def born_remainder(node: Node) -> None:
    """ex1 R5: the take's remainder born at the half of its wall, the one-level step at the Node after the seed (take_origin half), or at 0 (take_origin zero)."""
    if take_flag(node) != "remainder" or str(node.control.get("take_origin", "zero")) != "half":
        return
    gap0 = node.row(PLANE, gap=0)
    c = node.content()
    r = node.rule_of(gap0, c, node.link_factors())
    node.start_content = c
    for at in np.ndindex(*node.shape):
        node.take_rem[at] = half(max(0, step_of(node, at, r, gap0.lines[0])))


def take_at(
''',
        ),
        (
            "R6 the take under the flag: the walls less the standing remainder owed, the fall's excess carried as the remainder",
            '''    gap0 = node.row(PLANE, gap=0)
    z = gap0.lines[0]
    levels, fall = fall_of(node, at, walls, r_gap0, z)
    if levels is None:
''',
            '''    gap0 = node.row(PLANE, gap=0)
    z = gap0.lines[0]
    flagged = take_flag(node) == "remainder"  # ex1 R6
    rem_was = int(node.take_rem[at]) if flagged else 0
    owed = walls - rem_was
    if flagged and owed <= 0:
        levels, fall = 0, 0
    else:
        levels, fall = fall_of(node, at, owed, r_gap0, z)
    if levels is None:
''',
        ),
        (
            "R7 the remainder written at the Node after the take and kept for the log",
            '''    lay(node, node.records().index(gap0), at, (toward * levels, 0, 0, 0))
    node.closes[at] += 1
''',
            '''    lay(node, node.records().index(gap0), at, (toward * levels, 0, 0, 0))
    node.closes[at] += 1
    if flagged:  # ex1 R7
        node.take_rem[at] = fall - owed
        node.take_log[at] = {"remainder_was": rem_was, "remainder": fall - owed, "owed": owed, "booked": walls}
''',
        ),
    ],
    "close.py": [
        (
            "R8 the birth line carries the remainder under the flag",
            '''                "dP_take": dp_take,
                "dP_lay": dp_lay,
            }
        )
''',
            '''                "dP_take": dp_take,
                "dP_lay": dp_lay,
                **(node.take_log.get(at, {}) if take_flag(node) == "remainder" else {}),
            }
        )
''',
        ),
        (
            "R9 the credit line carries the remainder and the booked unit under the flag",
            '''        "sign_level": int(node.row(POTENTIAL).lines[0].now[at]),
        "turned": bool(node.turned[at]),
    }
''',
            '''        "sign_level": int(node.row(POTENTIAL).lines[0].now[at]),
        "turned": bool(node.turned[at]),
        **(node.take_log.get(at, {}) if take_flag(node) == "remainder" else {}),
    }
''',
        ),
        (
            "R10 the unclick restores the remainder",
            '''            lay(node, rec0, at, (entry["taken_now_was"] - int(gap0.lines[0].now[at]), 0, 0, 0))
            node.closes[at] -= 1
''',
            '''            lay(node, rec0, at, (entry["taken_now_was"] - int(gap0.lines[0].now[at]), 0, 0, 0))
            node.closes[at] -= 1
            if "remainder_was" in entry:  # ex1 R10
                node.take_rem[at] = entry["remainder_was"]
''',
        ),
        (
            "R11 the import of the flag",
            "    read_number,\n    take_at,\n)\n",
            "    read_number,\n    take_at,\n    take_flag,\n)\n",
        ),
    ],
}


def main(worktree):
    src = os.path.join(worktree, "src", "event_universe")
    dst = os.path.join(worktree, "tools", "derivations", "ex1", "engine", "event_universe")
    if os.path.exists(os.path.dirname(dst)):
        shutil.rmtree(os.path.dirname(dst))
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
    for name, reps in REPLACEMENTS.items():
        path = os.path.join(dst, name)
        text = open(path, encoding="utf-8").read()
        for label, old, new in reps:
            n = text.count(old)
            if n != 1:
                raise SystemExit(f"{name}: {label}: the old text occurs {n} times, 1 expected")
            text = text.replace(old, new)
            print(f"{name}: {label}: replaced")
        open(path, "w", encoding="utf-8").write(text)
    toy = os.path.join(worktree, "tools", "derivations", "toys", "lean", "toy.py")
    shutil.copy(toy, os.path.join(worktree, "tools", "derivations", "ex1", "toy_ex1.py"))
    print("toy.py copied to toy_ex1.py unchanged")


if __name__ == "__main__":
    main(sys.argv[1])
