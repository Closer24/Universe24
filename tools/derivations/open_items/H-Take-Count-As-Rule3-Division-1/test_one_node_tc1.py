"""The one-Node test (tc1): on the 3-cube world's first takes the fall is the count times a price linear in the count, f(s) = s X (|L| - w s) over the weight with L = 2 w now + pull (Rule3's backward numerator read at the now slot), exactly to the division's remainder; the carried division of the walls by the price at the start, s_div, is at most the share's root s and pays less than the walls by the moved levels' own square X w s_div^2 over the weight (to the remainder) exactly where s_div is below s, and the root is the quotient or the next count: the count as one carried division with the exact guard, no root. Under 15 s."""
import os, sys
sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, os.path.join(W, "src")); sys.path.insert(0, os.path.join(W, "tests"))
from event_universe import merger, take as take_mod
from event_universe.core import rule3
from event_universe.core.rule3 import quotient
from laws import node_of


def test_take_count_is_a_root_not_a_division():
    node = node_of("world_hole.json", intervals=12)
    orig, seen = merger.fall_of, []

    def wrapped(node_, at, walls, r, row):
        got = orig(node_, at, walls, r, row)
        if sys._getframe(1).f_code.co_name == "read_ends" and got[0]:
            s, fall_s, k = got
            line = row.lines[k]
            now, before = int(line.now[at]), int(line.before[at])
            w, own, reached = int(r.wall), take_mod.at_node(r.self_coefficient, at), 0
            for port, reach in enumerate(r.reaches):
                reached += take_mod.at_node(reach, at) * int(line.before[take_mod.neighbour(node_, at, port)])
            pull = own * before + reached
            t = 1 if before > now else -1
            x, weight = int(node_.start_x[at]), rule3.share_weight(node_.gamma, node_.G)
            price = -t * ((w + w) * now + pull) * x
            seen.append((now, before, t, w, pull, x, weight, walls, s, price))
        return got

    merger.fall_of = wrapped
    for _ in range(12):
        node.step()
    merger.fall_of = orig
    assert seen, "no take on the 3-cube in 12 intervals"
    product_form = division_below = short_by_square = 0
    for now, before, t, w, pull, x, weight, walls, s, price in seen:
        moved = now + t * s
        numerator = x * (w * (now * now - moved * moved) - t * s * pull)
        assert numerator == s * (price - x * w * s), "the fall is the count times the price less the count's own square"
        product_form += 1
        assert price > 0
        s_div = -quotient(-walls * weight, price)
        assert s_div <= s
        division_below += s_div < s
        fall_div = quotient(s_div * (price - x * w * s_div), weight)
        short_by_square += fall_div < walls
    assert product_form == len(seen)
    assert division_below == short_by_square, "the division sits below the root exactly where its quotient's fall is short of the walls (the moved levels' own square)"
    assert all(s - (-quotient(-walls * weight, price)) <= 1 for now, before, t, w, pull, x, weight, walls, s, price in seen), "the root is the quotient or the next count"
    print("takes", len(seen), "product form", product_form, "division below the root", division_below, "division short of the walls", short_by_square)
