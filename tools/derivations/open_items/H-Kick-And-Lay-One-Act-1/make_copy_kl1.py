"""kl1's flagged copy of the engine (H-Kick-And-Lay-One-Act-1): src/event_universe copied whole to /dev/shm/tmp/kl1/src_kl1/event_universe with the kick's inverse behind the environment flag KL1_FORM (close.births, close.children, close.unclick). Unset or empty: the head bit for bit. "1": after one take's children are laid (MS-S1 kept: the take at the taker's Node pays the children's walls exactly as the head), the birth's momentum and its moment about the taker's Node are closed by moves of the taken line's now at the taker's six far ends (the kick's inverse: the same act as the take, the same line, one level count per far end, no row named, no typed number): the six integers solve the six equations (the three of P: the far ends' moves' momentum equal to minus the take's and the children's per-end momentum summed; the three of J: their moment about the taker's Node equal to minus the far child's moment) by the carried division of the exact rational solution toward zero, the remainder named; where the six columns do not span (the taken row smooth: the six gradients alike) the free columns are 0 and the equations' residual is the remainder; the far ends' moves' momentum booked by momentum_of exactly (a now-move's momentum reads the before field alone, so the six bookings are exact and independent); the taken row's share change by the six moves read (laid, read, taken back) and named as `made` against the walls booked (MS-S1's booking is the take's at the taker's Node alone; the inverse's share is booked by no take: named, not paid); the moves undone in the run back by each far end's now_was."""
import os
import shutil
import sys

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
root = sys.argv[1] if len(sys.argv) > 1 else "/dev/shm/tmp/kl1/src_kl1"
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


close = os.path.join(dst, "close.py")
replace(close, "import numpy as np\n", "import numpy as np\nimport os\nfrom fractions import Fraction\n\nKL1_FORM = os.environ.get(\"KL1_FORM\", \"\")  # kl1's flag: empty is the head bit for bit\n")
replace(close, "from event_universe.core.ports import AXES, across, port_of\n", "from event_universe.core.ports import AXES, PORTS, PORT_SIDES, across, port_of\n")
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
    """def solve_carried(m: list[list[int]], rhs: list[int]) -> tuple[list[int], list[int], int, int]:
    \"\"\"kl1: the carried division of a vector by a matrix (Rule3's road: one step, the remainder named): the exact rational solution of m x = rhs by elimination (free columns 0, inconsistent rows left to the remainder), each component carried toward zero to an integer; returns (x, the remainder rhs - m x, the rank, the count of components that were not integers).\"\"\"
    n, k = len(m), len(m[0])
    a = [[Fraction(v) for v in row] + [Fraction(r)] for row, r in zip(m, rhs, strict=True)]
    pivots: list[tuple[int, int]] = []
    r = 0
    for col in range(k):
        p = next((i for i in range(r, n) if a[i][col] != 0), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        pv = a[r][col]
        a[r] = [v / pv for v in a[r]]
        for i in range(n):
            if i != r and a[i][col] != 0:
                f = a[i][col]
                a[i] = [u - f * v for u, v in zip(a[i], a[r], strict=True)]
        pivots.append((r, col))
        r += 1
        if r == n:
            break
    x = [Fraction(0)] * k
    for row, col in pivots:
        x[col] = a[row][k]
    carried = []
    broken = 0
    for v in x:
        q = abs(v.numerator) // v.denominator
        q = q if v >= 0 else -q
        broken += v.denominator != 1
        carried.append(int(q))
    rem = [int(rv - sum(mv * xv for mv, xv in zip(row, carried, strict=True))) for row, rv in zip(m, rhs, strict=True)]
    return carried, rem, len(pivots), broken


def kick_inverse(
    node: Node, at: tuple[int, ...], rec: int, take: dict[str, Any], ends: list[tuple[tuple[int, ...], list[int]]], c: Any, factors: tuple[Any, ...]
) -> dict[str, Any]:
    \"\"\"kl1: the kick's inverse on the taken row at the taker's six far ends: the taken line's now moved at each far end by an integer so that the six far ends' momentum (each 2 num delta times the taken line's before gradient at the far end, momentum_of) closes the birth's momentum (the take's and the children's per-end lays') and their moment about the taker's Node closes the far child's; the six integers by the carried division (solve_carried), the remainder named; the share the moves add to the taken row read and named as `made` (booked by no take).\"\"\"
    row = node.records()[rec]
    assert row.pair is not None
    num, k = row.pair[0], int(take["taken_line"])
    z = row.lines[k]
    cube = node.cube

    def arm(where: tuple[int, ...]) -> list[int]:
        out = []
        for w_, a_ in zip(where, at, strict=True):
            d = (w_ - a_) % cube
            out.append(d - cube if d > cube // 2 else d)
        return out

    def crossv(u: list[int], v: list[int]) -> list[int]:
        return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]

    p_target = [-int(x) for x in take["dP_take"]]
    j_target = [0, 0, 0]
    for where, dpe in ends:
        p_target = [a - b for a, b in zip(p_target, dpe, strict=True)]
        j_target = [a - b for a, b in zip(j_target, crossv(arm(where), dpe), strict=True)]
    fars = [neighbour(node, at, p) for p in range(PORTS)]
    cols = []
    for far in fars:
        g = momentum_of(node, z.now, z.before, far, d_now=1, num=num)
        cols.append(g + crossv(arm(far), g))
    m = [[cols[p][i] for p in range(PORTS)] for i in range(2 * AXES)]
    deltas, rem, rank, broken = solve_carried(m, p_target + j_target)
    rule = node.rule(row.pair, c, factors)

    def total() -> int:
        return int(sum(int(x) for x in node.share(row.lines, rule).reshape(-1)))

    share0 = total()
    moves = []
    for p, (far, delta) in enumerate(zip(fars, deltas, strict=True)):
        if delta == 0:
            continue
        dp = momentum_of(node, z.now, z.before, far, d_now=delta, num=num)
        now_was = int(z.now[far])
        lay(node, rec, far, delta, line=k)
        moves.append({"node": list(far), "port": p, "delta": delta, "dP": dp, "now_was": now_was, "before": int(z.before[far])})
    made = total() - share0
    node.counts["kick_inverse_moves"] = node.counts.get("kick_inverse_moves", 0) + len(moves)
    node.counts["kick_inverse_exact"] = node.counts.get("kick_inverse_exact", 0) + (rem == [0] * (2 * AXES))
    node.counts["kick_inverse_rank_short"] = node.counts.get("kick_inverse_rank_short", 0) + (rank < 2 * AXES)
    summed = [sum(x["dP"][a] for x in moves) for a in range(AXES)]
    return {
        "taken_line": k,
        "target_P": p_target,
        "target_J_about_taker": j_target,
        "columns": cols,
        "deltas": deltas,
        "rank": rank,
        "broken": broken,
        "remainder": rem,
        "moves": moves,
        "dP_moves": summed,
        "made": made,
        "booked": int(take["booked"]),
        "levels_abs": sum(abs(d) for d in deltas),
    }


def children(
    node: Node, at: tuple[int, ...], kids: list[Kid], take: dict[str, Any], rec: int, c: Any = None, factors: tuple[Any, ...] = ()
) -> set[tuple[int, ...]]:
""",
)
replace(
    close,
    """    touched = {at}
    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
        touched |= {minus, plus}
""",
    """    touched = {at}
    ends_all: list[tuple[tuple[int, ...], list[int]]] = []
    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
        touched |= {minus, plus}
        ends_all += list(zip((minus, plus), node.dp_lay_ends, strict=True))
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
                **({"dP_lay_ends": node.dp_lay_ends} if KL1_FORM else {}),
            }
        )
    if KL1_FORM and "takes" not in take:
        inverse = kick_inverse(node, at, rec, take, ends_all, c, factors)
        node.log[-1]["kick_inverse"] = inverse
        touched |= {tuple(x["node"]) for x in inverse["moves"]}
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
    """        if entry["event"] == "birth" and "kick_inverse" in entry:  # kl1: the far ends' moves undone first
            row = entry.get("taken_row", rec0)
            k = entry["kick_inverse"]["taken_line"]
            line = node.records()[row].lines[k]
            for one in reversed(entry["kick_inverse"]["moves"]):
                far = tuple(one["node"])
                lay(node, row, far, one["now_was"] - int(line.now[far]), line=k)
        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]
""",
)
replace(
    close,
    """    node.counts["refused_" + cause] += 1
""",
    """    node.counts["refused_" + cause] = node.counts.get("refused_" + cause, 0) + 1  # kl1: new causes counted
""",
)
print("copy written:", dst)
