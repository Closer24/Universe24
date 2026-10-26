"""cm1's flagged copy of the engine: src/event_universe copied whole to /dev/shm/tmp/cm1/src/event_universe with one act behind one environment flag, empty for the head bit for bit.
CM1_FORM "1": the children laid moving (the one lay act, every row alike): each child is laid (re_now A, re_before sense Q, im_now 0, im_before sense B), the one integer Q the carried quotient of the recoil's projection on the pair's own lay momentum line (the lay's momentum is linear in Q: c = dP_lay(1) - dP_lay(0), read by laying and taking back; Q = odd_rounded(-(dP_take + dP_lay(0)) . c, c . c), one rounding), so the pair's lattice momentum cancels the take's along the line the pair can carry and the rest is the remainder, logged; the walls read exactly by laying the moving children (walls_of unchanged in form), the take and the children's Q found together as a fixed point of the search by comparisons (at most 8 rounds), the exact lay kept; the charge W = A B sense kept to the bit (im_now 0); the run back from the log's own Q."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
root = "/dev/shm/tmp/cm1/src"
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


close = os.path.join(dst, "close.py")
replace(close, "import numpy as np\n", "import numpy as np\nimport os\n\nCM1_FORM = os.environ.get(\"CM1_FORM\", \"\")  # cm1's flag: empty is the head bit for bit\nCM1_ROUNDS = 8\n")
replace(close, "from event_universe.core.rule3 import quotient, remainder\n", "from event_universe.core.paces import odd_rounded\nfrom event_universe.core.rule3 import quotient, remainder\n")
# child_at: the moving child, re_before sense Q
replace(
    close,
    """    num = row.pair[0]
    dp = momentum_of(node, re.now, re.before, where, d_now=sign * node.A, num=num)
    dp_im = momentum_of(node, im.now, im.before, where, d_before=sign * sense * node.B, num=num)
    lay(node, s, where, (node.A, 0, 0, sense * node.B), sign)
    return [a + b for a, b in zip(dp, dp_im, strict=True)]
""",
    """    num = row.pair[0]
    q = getattr(node, "cm1_q", {}).get((s, where), 0) if CM1_FORM == "1" else 0
    dp = momentum_of(node, re.now, re.before, where, d_now=sign * node.A, d_before=sign * sense * q, num=num)
    dp_im = momentum_of(node, im.now, im.before, where, d_before=sign * sense * node.B, num=num)
    lay(node, s, where, (node.A, sense * q, 0, sense * node.B), sign)
    return [a + b for a, b in zip(dp, dp_im, strict=True)]


def pair_momentum(node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...]) -> list[int]:
    \"\"\"cm1: the two children's lay momentum read by laying them (the - child, then the +) and taking both back; linear in the children's Q.\"\"\"
    found = [0, 0, 0]
    for where, sense in ((minus, -1), (plus, 1)):
        for a, d in enumerate(child_at(node, s, where, sense)):
            found[a] += d
    child_at(node, s, plus, 1, -1)
    child_at(node, s, minus, -1, -1)
    return found


def moving_q(node: Node, kids: list[Kid], dp_take: list[int]) -> dict[tuple[int, tuple[int, ...]], int]:
    \"\"\"cm1: the children's Q per take from the take's recoil: the lay's momentum is linear in Q (c = dP_lay(1) - dP_lay(0)), Q the carried quotient of the recoil's projection on c (one odd rounding), the same for every row; 0 where the pair's lay carries nothing (c = 0).\"\"\"
    found: dict[tuple[int, tuple[int, ...]], int] = {}
    node.cm1_q = {}
    for s, minus, plus, _room in kids:
        at0 = pair_momentum(node, s, minus, plus)
        node.cm1_q = {(s, minus): 1, (s, plus): 1}
        at1 = pair_momentum(node, s, minus, plus)
        node.cm1_q = {}
        c = [b - a for a, b in zip(at0, at1, strict=True)]
        cc = sum(x * x for x in c)
        target = [-(t + a) for t, a in zip(dp_take, at0, strict=True)]
        q = 0 if cc == 0 else int(odd_rounded(sum(t * x for t, x in zip(target, c, strict=True)), cc))
        found[(s, minus)] = q
        found[(s, plus)] = q
    return found
""",
)
# births: the fixed point of the take and the children's Q at the gap 0
replace(
    close,
    """        booked = sum(sum(walls[Birth(at, *kid, rec)]) for kid in kids)
        one = take_at(node, at, booked, rule, len(kids), rec)
""",
    """        booked = sum(sum(walls[Birth(at, *kid, rec)]) for kid in kids)
        fixed = None
        if CM1_FORM == "1":
            qs: dict[tuple[int, tuple[int, ...]], int] = {}
            fixed = False
            for _round in range(CM1_ROUNDS):
                levels0, _fall0, k0 = fall_of(node, at, booked, rule, row)
                if levels0 is None:
                    break
                z0 = row.lines[k0]
                toward0 = 1 if int(z0.before[at]) > int(z0.now[at]) else -1
                dp0 = momentum_of(node, z0.now, z0.before, at, d_now=toward0 * levels0, num=row.pair[0])
                new_qs = moving_q(node, kids, dp0)
                node.cm1_q = new_qs
                for kid in kids:
                    walls[Birth(at, *kid, rec)] = walls_of(node, kid.line_pair, kid.minus, kid.plus, c, factors)
                booked = sum(sum(walls[Birth(at, *kid, rec)]) for kid in kids)
                if new_qs == qs:
                    fixed = True
                    break
                qs = new_qs
            node.cm1_q = qs
        one = take_at(node, at, booked, rule, len(kids), rec)
        if fixed is not None:
            node.cm1_fixed = fixed
""",
)
replace(
    close,
    """        take = take_line(fall, booked, levels, now, before, node.last_dp, k)
        taken.append((at, rec, kids, take))
""",
    """        take = take_line(fall, booked, levels, now, before, node.last_dp, k)
        if CM1_FORM == "1":
            take["cm1_q"] = dict(node.cm1_q)
            take["cm1_fixed"] = node.cm1_fixed
        taken.append((at, rec, kids, take))
""",
)
# children: the Q laid from the take's own, logged
replace(
    close,
    """    touched = {at}
    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
""",
    """    touched = {at}
    for s, minus, plus, room in kids:
        if CM1_FORM == "1":
            node.cm1_q = take.get("cm1_q", {})
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
        moving = (
            {"cm1_q": [node.cm1_q.get((s, minus), 0), node.cm1_q.get((s, plus), 0)], "cm1_fixed": take.get("cm1_fixed")}
            if CM1_FORM == "1"
            else {}
        )
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
                **moving,
            }
        )
    return touched
""",
)
# unclick: the lay removed with its Q
replace(
    close,
    """            s, (a, b) = entry["line_pair"], entry["amplitude"]
            lay(node, s, tuple(entry["minus"]), (a, 0, 0, -b), -1)
            lay(node, s, tuple(entry["plus"]), (a, 0, 0, b), -1)
""",
    """            s, (a, b) = entry["line_pair"], entry["amplitude"]
            qm, qp = entry.get("cm1_q", [0, 0])
            lay(node, s, tuple(entry["minus"]), (a, -qm, 0, -b), -1)
            lay(node, s, tuple(entry["plus"]), (a, qp, 0, b), -1)
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
    node.cm1_ends = []
    for where, sense in ((minus, -1), (plus, 1)):
        end = child_at(node, s, where, sense)
        node.cm1_ends.append(list(end))
        for a, d in enumerate(end):
            dp_lay[a] += d
""",
)
replace(
    close,
    """            {"cm1_q": [node.cm1_q.get((s, minus), 0), node.cm1_q.get((s, plus), 0)], "cm1_fixed": take.get("cm1_fixed")}""",
    """            {"cm1_q": [node.cm1_q.get((s, minus), 0), node.cm1_q.get((s, plus), 0)], "cm1_fixed": take.get("cm1_fixed"), "dP_lay_ends": node.cm1_ends}""",
)
print("src built at", root)
