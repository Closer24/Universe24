"""kl2's flagged copy of the engine: src/event_universe copied whole to /dev/shm/tmp/kl2/src_kl2/event_universe with the kick's inverse behind the environment flag KL2_FORM (close.births and close.unclick; the solver kl2_inverse.py beside). Unset or empty: the head bit for bit. "1": after one take's children are laid (MS-S1, the head's take and lay untouched), the taken row's own levels at the taker's six far ends (the Node beyond each Port) are moved by the integers that balance the birth's momentum (3) and its moment about the taker's Node (3): the kick's inverse on the taken row, the same lay act (`lay`) on the same record the take moved, every move's momentum booked at its Node by `momentum_of`; the levels solved exactly over the integers where the far ends' standing gradients hold the target, the remainder named where not (nothing laid: refused by name `inverse_remainder`); the lays' exact share change read (laid, read, taken back) and named as the energy remainder, no second take (one act); the lays undone in the run back. "2": as "1" with a seventh equation, the lays' share change 0 to the linear order (each column's share coefficient read as the symmetric difference of one level laid and taken back), the exact share change named as the quadratic remainder."""
import os
import shutil
import sys

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
root = sys.argv[1] if len(sys.argv) > 1 else "/dev/shm/tmp/kl2/src_kl2"
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
shutil.copy(os.path.join(here, "kl2_inverse.py"), os.path.join(dst, "kl2_inverse.py"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


close = os.path.join(dst, "close.py")
replace(close, "import numpy as np\n", "import numpy as np\nimport os\n\nKL2_FORM = os.environ.get(\"KL2_FORM\", \"\")  # kl2's flag: empty is the head bit for bit\n")
replace(
    close,
    """    for at, rec, kids, take in taken:
        touched |= children(node, at, kids, take, rec)
        node.counts["taken"] += take["taken"]
        node.counts["booked"] += take["booked"]
    return touched
""",
    """    for at, rec, kids, take in taken:
        touched |= children(node, at, kids, take, rec)
        node.counts["taken"] += take["taken"]
        node.counts["booked"] += take["booked"]
        if KL2_FORM and "takes" not in take:
            touched |= inverse_kick(node, at, rec, take, kids, c, factors)
    return touched


def inverse_kick(
    node: Node, at: tuple[int, ...], rec: int, take: dict[str, Any], kids: list[Kid], c: Any, factors: tuple[Any, ...]
) -> set[tuple[int, ...]]:
    \"\"\"kl2: the kick's inverse on the taken row at the taker's six far ends (kl2_inverse): per far end j = at + e and per line of the taken row the two integers (d_now, d_before), each a column of momentum_of at j (the standing gradient) and of its moment 2 e x that; the six equations the birth's momentum balance (the take, the children per end, the lays) and its moment balance about the taker's Node; solved over the integers, size-reduced; laid by the one lay act where exact, refused by name `inverse_remainder` where the lattice does not hold the target (the remainder logged); the lays' exact share change read and logged as the energy remainder (no second take: one act).\"\"\"
    from event_universe.kl2_inverse import cross3, size_reduce, solve_integer

    row = node.records()[rec]
    assert row.pair is not None
    num = row.pair[0]
    ends = node.kl2_ends
    b_p = [-int(x) for x in take["dP_take"]]
    b_j = [0, 0, 0]
    for where, dpe in ends:
        for a in range(AXES):
            b_p[a] -= dpe[a]
        arm = [0, 0, 0]
        for a in range(AXES):
            if where[a] != at[a]:
                d = (where[a] - at[a]) % node.cube
                arm[a] = 2 * (d - node.cube if d > node.cube // 2 else d)
        for a, v in enumerate(cross3(arm, dpe)):
            b_j[a] -= v
    cols, where_of = [], []
    for port in range(PORTS):
        far = neighbour(node, at, port)
        axis, side = PORT_SIDES[port]
        arm = [0, 0, 0]
        arm[axis] = 2 * side
        for k, z in enumerate(row.lines):
            for kind in (0, 1):
                v = momentum_of(node, z.now, z.before, far, d_now=1 - kind, d_before=kind, num=num)
                cols.append(v + cross3(arm, v))
                where_of.append((far, k, kind))
    A = [[cols[k][i] for k in range(len(cols))] for i in range(2 * AXES)]
    b = b_p + b_j
    rule = node.rule(row.pair, c, factors)

    def total() -> int:
        return int(sum(int(v) for v in node.share(row.lines, rule).reshape(-1)))

    if KL2_FORM == "2":  # the share's linear part as the seventh equation: the lays' share 0 to the linear order (the standing level's own gradient of the share)
        unit = [0] * (PLANE * len(row.lines))
        share_row = []
        for far, k, kind in where_of:
            lv = list(unit)
            lv[PLANE * k + kind] = 1
            lay(node, rec, far, tuple(lv))
            up = total()
            lay(node, rec, far, tuple(lv), -1)
            lv[PLANE * k + kind] = -1
            lay(node, rec, far, tuple(lv))
            down = total()
            lay(node, rec, far, tuple(lv), -1)
            share_row.append(up - down)
        A.append(share_row)
        b.append(0)
    x, rem, kernel = solve_integer(A, b)
    entry: dict[str, Any] = {"event": "inverse", "i": node.interval, "node": list(at), "taken_row": rec, "target_P": b_p, "target_J2": b_j, "remainder": rem, "form": KL2_FORM}
    if any(rem):
        node.counts["inverse_remainder"] = node.counts.get("inverse_remainder", 0) + 1
        node.log.append(entry | {"laid": False})
        return set()
    x = size_reduce(x, kernel)
    assert all(sum(A[i][k] * x[k] for k in range(len(x))) == b[i] for i in range(len(b)))
    levels: dict[tuple[int, ...], list[int]] = {}
    for (far, k, kind), v in zip(where_of, x, strict=True):
        levels.setdefault(far, [0] * (PLANE * len(row.lines)))[PLANE * k + kind] += v
    before = total()
    for far, lv in levels.items():
        lay(node, rec, far, tuple(lv))
    d_share = total() - before
    for far, lv in levels.items():
        lay(node, rec, far, tuple(lv), -1)
    laid = []
    for far, lv in levels.items():
        dp = [0, 0, 0]
        for k, z in enumerate(row.lines):
            for a, v in enumerate(momentum_of(node, z.now, z.before, far, d_now=lv[PLANE * k], d_before=lv[PLANE * k + 1], num=num)):
                dp[a] += v
        lay(node, rec, far, tuple(lv))
        laid.append({"node": list(far), "levels": lv, "dP": dp})
    node.counts["inverse_laid"] = node.counts.get("inverse_laid", 0) + 1
    node.log.append(entry | {"laid": True, "lays": laid, "d_share": d_share, "booked": take["booked"], "max_level": max(abs(v) for v in x)})
    return set(levels)
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
    for where, sense in ((minus, -1), (plus, 1)):
        end = child_at(node, s, where, sense)
        if KL2_FORM:
            node.kl2_ends.append((where, [int(v) for v in end]))
        for a, d in enumerate(end):
            dp_lay[a] += d
""",
)
replace(
    close,
    """    touched = {at}
    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
""",
    """    touched = {at}
    node.kl2_ends = []
    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
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
                **({"dP_lay_ends": [e[1] for e in node.kl2_ends]} if KL2_FORM else {}),
            }
        )
    return touched
""",
)
replace(
    close,
    """        at = tuple(entry["node"])
        if entry["event"] == "birth":
""",
    """        at = tuple(entry["node"])
        if entry["event"] == "inverse" and entry["laid"]:  # kl2: the inverse's lays undone (logged after its births, so undone before them)
            for one in reversed(entry["lays"]):
                lay(node, entry["taken_row"], tuple(one["node"]), tuple(one["levels"]), -1)
            continue
        if entry["event"] == "inverse":
            continue
        if entry["event"] == "birth":
""",
)
replace(close, "from event_universe.core.ports import AXES, across, port_of\n", "from event_universe.core.ports import AXES, PORT_SIDES, PORTS, across, port_of\n")
print("copy written:", dst)
