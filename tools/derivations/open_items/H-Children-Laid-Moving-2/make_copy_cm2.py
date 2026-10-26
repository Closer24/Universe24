"""cm2's flagged copy of the engine: src/event_universe copied whole to /dev/shm/tmp/cm2/src_cm2/event_universe with one act behind one environment flag, empty for the head bit for bit.
CM2_FORM "1": the children laid moving (the one-Link form the letter allows): at a birth from the gap-0 row each child keeps MS-S1's re_now = A and im_before = -+B (its charge -+T div 2 exact) and carries one integer more, re_before = -+a, the antisymmetric part of the pair's before along the Link (the symmetric part carries no momentum: the Link's bilinear is odd under the exchange of the ends), a the carried division (toward zero) of the predicted recoil's along-Link component by the pair's gain per unit a (read by one trial lay, the bilinear exact), the walls re-read with the moving children (the exact lay: what is taken is what the lay books), the take then paid from the taken line; each end's lay momentum booked at its own Node (dP_lay_ends) and the children's integers logged (moving), the run back undoing them."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
root = os.environ.get("CM2_COPY", "/dev/shm/tmp/cm2/src_cm2")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:70])
    open(path, "w").write(text.replace(old, new))


close = os.path.join(dst, "close.py")
replace(close, "import numpy as np\n", "import numpy as np\nimport os\n\nCM2_FORM = os.environ.get(\"CM2_FORM\", \"\")  # cm2's flag: empty is the head bit for bit\n")
replace(
    close,
    "def child_at(node: Node, s: int, where: tuple[int, ...], sense: int, sign: int = 1) -> list[int]:",
    "def child_at(node: Node, s: int, where: tuple[int, ...], sense: int, sign: int = 1, moving: int = 0) -> list[int]:",
)
replace(
    close,
    "    dp = momentum_of(node, re.now, re.before, where, d_now=sign * node.A, num=num)\n",
    "    dp = momentum_of(node, re.now, re.before, where, d_now=sign * node.A, d_before=sign * moving, num=num)\n",
)
replace(close, "    lay(node, s, where, (node.A, 0, 0, sense * node.B), sign)\n", "    lay(node, s, where, (node.A, moving, 0, sense * node.B), sign)\n")
replace(
    close,
    "    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...]\n) -> tuple[int, int]:",
    "    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...], moving: tuple[int, int] = (0, 0)\n) -> tuple[int, int]:",
)
replace(
    close,
    """    before = total()
    child_at(node, s, minus, -1)
    middle = total()
    child_at(node, s, plus, 1)
    after = total()
    child_at(node, s, plus, 1, -1)
    child_at(node, s, minus, -1, -1)
""",
    """    before = total()
    child_at(node, s, minus, -1, moving=moving[0])
    middle = total()
    child_at(node, s, plus, 1, moving=moving[1])
    after = total()
    child_at(node, s, plus, 1, -1, moving=moving[1])
    child_at(node, s, minus, -1, -1, moving=moving[0])
""",
)
replace(
    close,
    """def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...]
) -> tuple[list[int], list[int], list[list[int]]]:""",
    """def pair_gain(node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...]) -> tuple[list[int], list[int]]:
    \"\"\"cm2: the pair's lay momentum at rest (dp0) and its gain per unit of the moving integer a (re_before -a at the - child, +a at the + child), read by two trial lays taken back; the bilinear is exactly linear in a.\"\"\"
    found = []
    for a in (0, 1):
        dp = [0, 0, 0]
        for where, sense, m in ((minus, -1, -a), (plus, 1, a)):
            for k, d in enumerate(child_at(node, s, where, sense, moving=m)):
                dp[k] += d
        for where, sense, m in ((plus, 1, a), (minus, -1, -a)):
            child_at(node, s, where, sense, -1, moving=m)
        found.append(dp)
    return found[0], [g - z for g, z in zip(found[1], found[0], strict=True)]


def moving_of(
    node: Node, at: tuple[int, ...], kids: list[Kid], walls: dict[Any, tuple[int, int]], rule: rule3.Rule, rec: int, c: Any, factors: tuple[Any, ...]
) -> dict[Kid, tuple[int, int]]:
    \"\"\"cm2: the children's moving integer per kid from the predicted recoil of the take of the resting walls (fall_of read, nothing written; momentum_of of the predicted levels on the taken line), the recoil's along-Link component divided (toward zero) by the pair's gain along its Link, kid after kid on the residual; the walls then re-read with the moving children (MS-S1: the lay books what the take pays).\"\"\"
    row = node.records()[rec]
    assert row.pair is not None
    found = {kid: (0, 0) for kid in kids}
    gains = {kid: pair_gain(node, kid.line_pair, kid.minus, kid.plus) for kid in kids}
    for _pass in range(2 * AXES):  # the division carried to its fixed point: the walls move with a, the levels with the walls, a with the levels
        booked = sum(sum(walls[Birth(at, *kid, rec)]) for kid in kids)
        levels, _fall, k = fall_of(node, at, booked, rule, row)
        if levels is None:
            return found
        z = row.lines[k]
        toward = 1 if int(z.before[at]) > int(z.now[at]) else -1
        residual = momentum_of(node, z.now, z.before, at, d_now=toward * levels, num=row.pair[0])
        before = dict(found)
        for kid in kids:
            dp0, gain = gains[kid]
            residual = [r + d for r, d in zip(residual, dp0, strict=True)]
            axis = max(range(AXES), key=lambda b: abs(gain[b]))
            a = 0 if gain[axis] == 0 else int(rule3.signed_quotient(-residual[axis], gain[axis]))
            residual = [r + a * g for r, g in zip(residual, gain, strict=True)]
            found[kid] = (-a, a)
            walls[Birth(at, *kid, rec)] = walls_of(node, kid.line_pair, kid.minus, kid.plus, c, factors, found[kid])
        if found == before:
            break
    return found


def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], moving: tuple[int, int] = (0, 0)
) -> tuple[list[int], list[int], list[list[int]], list[list[int]]]:""",
)
replace(
    close,
    """    dp_lay = [0, 0, 0]
    for where, sense in ((minus, -1), (plus, 1)):
        for a, d in enumerate(child_at(node, s, where, sense)):
            dp_lay[a] += d
    senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
    return dp_lay, senses, stood
""",
    """    dp_lay, ends = [0, 0, 0], []
    for where, sense, m in ((minus, -1, moving[0]), (plus, 1, moving[1])):
        end = child_at(node, s, where, sense, moving=m)
        ends.append(end)
        for a, d in enumerate(end):
            dp_lay[a] += d
    senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
    return dp_lay, senses, stood, ends
""",
)
replace(
    close,
    """        booked = sum(sum(walls[Birth(at, *kid, rec)]) for kid in kids)
        one = take_at(node, at, booked, rule, len(kids), rec)
        if one is None:
            continue
        levels, fall, now, before, k = one
        node.closes[at] -= 1
        take = take_line(fall, booked, levels, now, before, node.last_dp, k)
        taken.append((at, rec, kids, take))
    touched: set[tuple[int, ...]] = set()
    for at, rec, kids, take in taken:
        touched |= children(node, at, kids, take, rec)
""",
    """        moving = moving_of(node, at, kids, walls, rule, rec, c, factors) if CM2_FORM == "1" else {}
        booked = sum(sum(walls[Birth(at, *kid, rec)]) for kid in kids)
        one = take_at(node, at, booked, rule, len(kids), rec)
        if one is None:
            continue
        levels, fall, now, before, k = one
        node.closes[at] -= 1
        take = take_line(fall, booked, levels, now, before, node.last_dp, k)
        take["moving"] = moving
        taken.append((at, rec, kids, take))
    touched: set[tuple[int, ...]] = set()
    for at, rec, kids, take in taken:
        touched |= children(node, at, kids, take, rec)
""",
)
replace(
    close,
    """    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
""",
    """    for s, minus, plus, room in kids:
        moving = take.get("moving", {}).get(Kid(s, minus, plus, room), (0, 0))
        dp_lay, w_children, stood, ends = child_laid(node, s, minus, plus, moving)
""",
)
replace(
    close,
    """                "dP_lay": dp_lay,
                **({"takes": take["takes"]} if "takes" in take else {}),
""",
    """                "dP_lay": dp_lay,
                **({"takes": take["takes"]} if "takes" in take else {}),
                **({"moving": list(moving), "dP_lay_ends": ends} if CM2_FORM == "1" else {}),
""",
)
replace(
    close,
    """            lay(node, s, tuple(entry["minus"]), (a, 0, 0, -b), -1)
            lay(node, s, tuple(entry["plus"]), (a, 0, 0, b), -1)
""",
    """            m_minus, m_plus = entry.get("moving", [0, 0])
            lay(node, s, tuple(entry["minus"]), (a, m_minus, 0, -b), -1)
            lay(node, s, tuple(entry["plus"]), (a, m_plus, 0, b), -1)
""",
)
print("copied to", root)
