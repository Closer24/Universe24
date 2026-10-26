"""tc1's reader of every gap-0 take on the head (take.fall_of wrapped, no src edited): at every take the taken line's integers (now, before,
t, pull, w, X, weight, walls) and the head's count s; beside it the three candidate counts of the item: s_div the carried division of the
walls (in the share's unit) by the price of one level X |2 w now + pull| (Rule3's backward numerator at the now slot, the ceiling), s_link
the Link's record divided by the wall (the largest |now_i before_j - before_i now_j| over the six Links, div w), s_own the taken line's own
move at -1, |a_minus2 - now| (Rule3's own division on the taken line). Counted: s == each candidate; s_div below s; the fall at s_div
against the walls (the deficit, the moved levels' own square X w s^2 over the weight); the root's second difference in the walls
(s at m walls for m = 1..4) against the division's. Usage: tc1_takes.py <world name> <n> <out.json>. Integers only."""
import json, os, sys
sys.set_int_max_str_digits(0)
sys.path.insert(0, os.environ["PYTHONPATH"]); sys.path.insert(0, os.path.join(os.environ["PYTHONPATH"], "..", "tests"))
from event_universe import merger, take as take_mod
from event_universe.core import rule3
from event_universe.core.rule3 import quotient
from laws import node_of, state_of

world, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
node = node_of(world)
orig = merger.fall_of
takes, paid_by_remainder, refused = [], [], []


def wrapped(node, at, walls, r, row):
    got = orig(node, at, walls, r, row)
    if sys._getframe(1).f_code.co_name != "read_ends":
        return got
    if walls <= 0:
        paid_by_remainder.append(walls); return got
    if got[0] is None:
        refused.append(walls); return got
    s, fall_s, k = got
    line = row.lines[k]
    now, before, rem = int(line.now[at]), int(line.before[at]), int(line.rem[at])
    w, own, mass = int(r.wall), take_mod.at_node(r.self_coefficient, at), take_mod.at_node(r.mass, at)
    reached, flux, links = 0, 0, []
    for port, reach in enumerate(r.reaches):
        j = take_mod.neighbour(node, at, port)
        rj, bj, nj = take_mod.at_node(reach, at), int(line.before[j]), int(line.now[j])
        reached += rj * bj; flux += rj * (bj - before); links.append(abs(now * bj - before * nj))
    pull = own * before + reached
    t = 1 if before > now else -1
    x, weight = int(node.start_x[at]), rule3.share_weight(node.gamma, node.G)

    def fall(c):
        moved = now + t * c
        return int(quotient(x * (w * (now * now - moved * moved) - t * c * pull), weight))

    dist = abs(now - before)
    price = -t * ((w + w) * now + pull) * x
    s_div = -quotient(-walls * weight, price) if price > 0 else None
    a_m2, _r = rule3.rule3(flux, mass, w, before, now, rem, -1)
    s_own = abs(a_m2 - now)
    s_link = quotient(max(links), w)

    def root(target):
        full = fall(dist)
        if full < target:
            return None
        return next(c for c in range(1, dist + 1) if fall(c) >= target) if dist <= 4000 else s
    roots = [root(m * walls) for m in range(1, 5)]
    steps, c_ = 0, s_div
    while c_ is not None and c_ <= dist and fall(c_) < walls and price - x * w * (c_ + c_) > 0:
        c_ += -quotient(-(walls * weight - c_ * (price - x * w * c_)), price - x * w * (c_ + c_)); steps += 1
    takes.append(dict(i=node.interval, iterated=c_, iterated_steps=steps, at=list(at), k=k, now=now, before=before, t=t, pull=pull, w=w, x=x, weight=weight, walls=walls, s=s, dist=dist,
                      s_div=s_div, fall_div=None if s_div is None else fall(s_div), deficit=None if s_div is None else walls - fall(s_div),
                      square=None if s_div is None else quotient(x * w * s_div * s_div, weight), s_own=s_own, s_link=s_link, roots=roots,
                      price=price))
    return got


merger.fall_of = wrapped
for _ in range(n):
    node.step()
c = dict(takes=len(takes), iterated_eq_s=sum(e['iterated'] == e['s'] for e in takes), iterated_steps_max=max((e['iterated_steps'] for e in takes), default=0), iterated_steps_sum=sum(e['iterated_steps'] for e in takes), paid_by_remainder=len(paid_by_remainder), refused_stop=len(refused), s_eq_div=0, s_above_div=0, s_below_div=0, div_none=0, div_pays=0, div_short=0, deficit_sum=0, deficit_is_square=0, deficit_within_one_of_square=0,
         s_eq_own=0, s_eq_link=0, root_convex=0, root_defined4=0, div_second_difference_abs_at_most_one=0, s_minus_div_max=0, s_div_over_dist=0)
for e in takes:
    if e["s_div"] is None:
        c["div_none"] += 1; continue
    c["s_eq_div"] += e["s"] == e["s_div"]; c["s_above_div"] += e["s"] > e["s_div"]; c["s_below_div"] += e["s"] < e["s_div"]
    c["s_minus_div_max"] = max(c["s_minus_div_max"], e["s"] - e["s_div"])
    c["div_pays"] += e["fall_div"] >= e["walls"]; c["div_short"] += e["fall_div"] < e["walls"]; c["deficit_sum"] += max(0, e["deficit"])
    c["deficit_is_square"] += e["deficit"] == e["square"] - (e["s_div"] * e["price"] - e["walls"] * e["weight"]) // e["weight"]
    c["deficit_within_one_of_square"] += abs(e["deficit"] - (e["square"] - quotient(e["s_div"] * e["price"] - e["walls"] * e["weight"], e["weight"]))) <= 1
    c["s_eq_own"] += e["s"] == e["s_own"]; c["s_eq_link"] += e["s"] == e["s_link"]; c["s_div_over_dist"] += e["s_div"] > e["dist"]
    r = e["roots"]
    if all(v is not None for v in r):
        c["root_defined4"] += 1
        c["root_convex"] += (r[2] - 2 * r[1] + r[0] >= 0) and (r[3] - 2 * r[2] + r[1] >= 0) and (r[3] - 2 * r[2] + r[1] + r[2] - 2 * r[1] + r[0] > 0)
        d = [-quotient(-m * e["walls"] * e["weight"], e["price"]) for m in range(1, 5)]
        c["div_second_difference_abs_at_most_one"] += abs(d[2] - 2 * d[1] + d[0]) <= 1 and abs(d[3] - 2 * d[2] + d[1]) <= 1
json.dump(dict(world=world, n=n, counts=c, takes=takes[:40]), open(out, "w"))
print(json.dumps(dict(world=world, n=n, counts=c)))
