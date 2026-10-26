"""sl1's flagged copy of the engine: src/event_universe copied whole to /dev/shm/tmp/sl1/src_sl1/event_universe with the birth's six-Link lay behind the environment flag SL1_FORM (close.children and close.unclick). Unset or empty: the head bit for bit. "1": after the children are laid (MS-S1), the recoil's two transverse components are laid as the light's own lay on the other two axes' Links of the taker's Node: on each transverse axis b the far end is the Node beyond the Port the recoil points to (the sign of dP_take_b), the level laid is re_before beta with beta the carried division of -dP_take_b by the lay's own momentum per level (2 num times the plane's now gradient at the far end along b, -sign A onto nothing), the remainder named; the lays' share read as the children's (laid, read, taken back) and booked by one exact take at the taker's Node from the taken row (cause 1), the lays refused by name where that take stops, the second take's own momentum named as the remainder's; every lay's momentum booked per Node (the children's per end, the recoil lays' per far end); the lays undone in the run back. "2": as "1" with the along-axis component laid the same way at the far end of the Node's other Link of the birth's axis (the three axes alike)."""
import os
import shutil
import sys

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
root = sys.argv[1] if len(sys.argv) > 1 else "/dev/shm/tmp/sl1/src_sl1"
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


close = os.path.join(dst, "close.py")
replace(close, "import numpy as np\n", "import numpy as np\nimport os\n\nSL1_FORM = os.environ.get(\"SL1_FORM\", \"\")  # sl1's flag: empty is the head bit for bit\n")
replace(
    close,
    """    for at, rec, kids, take in taken:
        touched |= children(node, at, kids, take, rec)
""",
    """    for at, rec, kids, take in taken:
        touched |= children(node, at, kids, take, rec, c, factors)
""",
)
replace(
    close,
    """def children(
    node: Node, at: tuple[int, ...], kids: list[Kid], take: dict[str, Any], rec: int
) -> set[tuple[int, ...]]:
""",
    """def recoil_lays(
    node: Node, at: tuple[int, ...], s: int, rec: int, dp_take: list[int], minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...]
) -> dict[str, Any] | None:
    \"\"\"sl1: the recoil laid on the taker's Node's other Links as the light's own lay (the same lay act, the same record s): per axis the far end (a transverse axis: beyond the Port the recoil points to; the birth's axis under SL1_FORM 2: the end of the Node's other Link of that axis), the level re_before beta = the carried division of -dP_take_b by 2 num g_b (g_b the plane's re_now gradient at the far end along b, -sign A onto nothing), the lay's momentum booked by momentum_of exactly; the lays' share read by laying and taking back and booked by one exact take at the taker's Node from the taken row (cause 1); refused by name `recoil_gradient` (g_b = 0), `recoil_level` (beta 0), `recoil_stop` (the take cannot pay); the remainder named: -dP_take less the lays' momentum, and the second take's own momentum.\"\"\"
    row = node.records()[s]
    re, _im = row.lines
    assert row.pair is not None
    num = row.pair[0]
    link_axis = [a for a in range(AXES) if minus[a] != plus[a]][0]
    other = minus if plus == at else plus
    lays: list[tuple[tuple[int, ...], int, int]] = []
    for b in range(AXES):
        if b == link_axis:
            if SL1_FORM != "2":
                continue
            far = neighbour(node, at, port_of(b, 1 if neighbour(node, at, port_of(b, 0)) == other else 0))
        else:
            if dp_take[b] == 0:
                continue
            far = neighbour(node, at, port_of(b, 0 if dp_take[b] > 0 else 1))
        g = int(re.now[neighbour(node, far, port_of(b, 0))]) - int(re.now[neighbour(node, far, port_of(b, 1))])
        if g == 0:
            refused(node, at, "recoil_gradient", axis=b, row=rec)
            continue
        beta = int(quotient(-dp_take[b], (num + num) * g))
        if beta == 0:
            refused(node, at, "recoil_level", axis=b, row=rec)
            continue
        lays.append((far, b, beta))
    if not lays:
        return None
    rule_s = node.rule(row.pair, c, factors)

    def total() -> int:
        return int(sum(int(x) for x in node.share(row.lines, rule_s).reshape(-1)))

    before = total()
    for far, _b, beta in lays:
        lay(node, s, far, (0, beta, 0, 0))
    wall = total() - before
    for far, _b, beta in reversed(lays):
        lay(node, s, far, (0, beta, 0, 0), -1)
    taken_row = node.records()[rec]
    assert taken_row.pair is not None
    second: dict[str, Any] = {"node": list(at), "dP_take": [0, 0, 0], "booked": wall}
    if wall > 0:
        got = take_at(node, at, wall, node.rule(taken_row.pair, c, factors), 1, rec)
        if got is None:
            node.counts["recoil_stop"] = node.counts.get("recoil_stop", 0) + 1
            return None
        levels, fall, now, before_, k = got
        node.closes[at] -= 1
        second = {"node": list(at), **take_line(fall, wall, levels, now, before_, node.last_dp, k)}
    laid = []
    standing = 0
    for far, b, beta in lays:
        standing += any(int(x[far]) != 0 for x in (re.now, re.before, _im.now, _im.before))
        dp = momentum_of(node, re.now, re.before, far, d_before=beta, num=num)
        lay(node, s, far, (0, beta, 0, 0))
        laid.append({"node": list(far), "axis": b, "beta": beta, "dP": dp})
    node.counts["recoil_lays"] = node.counts.get("recoil_lays", 0) + len(laid)
    node.counts["recoil_onto_standing"] = node.counts.get("recoil_onto_standing", 0) + standing
    summed = [sum(x["dP"][a] for x in laid) for a in range(AXES)]
    return {
        "lays": laid,
        "take": second,
        "dP_laid": summed,
        "remainder": [-dp_take[a] - summed[a] for a in range(AXES)],
        "onto_standing": standing,
    }


def children(
    node: Node, at: tuple[int, ...], kids: list[Kid], take: dict[str, Any], rec: int, c: Any = None, factors: tuple[Any, ...] = ()
) -> set[tuple[int, ...]]:
""",
)
replace(
    close,
    """    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
        touched |= {minus, plus}
""",
    """    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
        touched |= {minus, plus}
        recoil = None
        if SL1_FORM and "takes" not in take:
            recoil = recoil_lays(node, at, s, rec, [int(x) for x in take["dP_take"]], minus, plus, c, factors)
            if recoil is not None:
                touched |= {tuple(x["node"]) for x in recoil["lays"]}
""",
)
replace(
    close,
    """                **({"takes": take["takes"]} if "takes" in take else {}),
            }
        )
    return touched
""",
    """                **({"takes": take["takes"]} if "takes" in take else {}),
                **({"dP_lay_ends": node.dp_lay_ends} if SL1_FORM else {}),
                **({"recoil": recoil} if recoil is not None else {}),
            }
        )
    return touched
""",
)
replace(
    close,
    """    dp_lay = [0, 0, 0]
    for where, sense in ((minus, -1), (plus, 1)):
        for a, d in enumerate(child_at(node, s, where, sense)):
            dp_lay[a] += d
""",
    """    dp_lay = [0, 0, 0]
    node.dp_lay_ends = []
    for where, sense in ((minus, -1), (plus, 1)):
        end = child_at(node, s, where, sense)
        node.dp_lay_ends.append([int(x) for x in end])
        for a, d in enumerate(end):
            dp_lay[a] += d
""",
)
replace(
    close,
    """        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]
""",
    """        if entry["event"] == "birth" and "recoil" in entry:  # sl1: the recoil lays and their take undone first
            s = entry["line_pair"]
            for one in reversed(entry["recoil"]["lays"]):
                lay(node, s, tuple(one["node"]), (0, one["beta"], 0, 0), -1)
            second = entry["recoil"]["take"]
            if "taken_line" in second:
                row = entry.get("taken_row", rec0)
                line = node.records()[row].lines[second["taken_line"]]
                lay(node, row, at, second["taken_now_was"] - int(line.now[at]), line=second["taken_line"])
        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]
""",
)
replace(
    close,
    """    node.counts["refused_" + cause] += 1
""",
    """    node.counts["refused_" + cause] = node.counts.get("refused_" + cause, 0) + 1  # sl1: the new causes counted
""",
)
print("copy written:", dst)
