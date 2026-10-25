"""ex1: the one-Node test of the exact take. The 3-cube world (world_node.json) is loaded; at the Node (1,0,0) the gap-0
line is fed FEED levels above its before; then K takes of walls = 2 x unit_gap0 are made at that Node by take_at alone
(no interval runs). Without the flag: the excess fall - walls at every take (all above 0 expected). With the flag: the
owed, the fall, the remainder's course, the identity fall + remainder_was - remainder == walls at every take (K of K
expected), the remainder below the one-level step at every take. Then the K takes are undone in reverse by the inverse
the unclick uses (the lay back of the levels and the remainder restored) and the state's hash compared: MATCH expected.
Usage: one_node_take.py <engine dir with event_universe> <world_node.json> <flag: none|zero|half> [K] [FEED]"""
import json
import sys


def main(argv):
    sys.set_int_max_str_digits(0)
    sys.path.insert(0, argv[1])
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    import toy_ex1
    from event_universe.rows import PLANE
    from event_universe import take as take_mod

    flag = argv[3]
    K = int(argv[4]) if len(argv) > 4 else 20
    feed = int(argv[5]) if len(argv) > 5 else 800
    universe, world = toy_ex1.load_toy_world(argv[2])
    if flag != "none":
        world["control"] = {"take": "remainder", "take_origin": flag}
    node = toy_ex1.Toy(universe, world)
    at = node.node_of([1, 0, 0])
    gap0 = node.row(PLANE, gap=0)
    z = gap0.lines[0]
    z.now[at] = int(z.before[at]) + feed
    c = node.content()
    node.start_content = c
    r = node.rule_of(gap0, c, node.link_factors())
    walls = 2 * node.unit_gap0
    h0 = take_mod.step_of(node, at, r, z)
    before_hash = node.state_hash()
    rem0 = int(node.take_rem[at])
    rows = []
    undo = []
    for k in range(K):
        rem_was = int(node.take_rem[at])
        now_was = int(z.now[at])
        step = take_mod.step_of(node, at, r, z)
        got = take_mod.take_at(node, at, walls, r, 1)
        if got is None:
            rows.append({"k": k, "refused": "stop"})
            break
        levels, fall, now, before = got
        rem = int(node.take_rem[at])
        rows.append(
            {
                "k": k,
                "now_was": now_was,
                "levels": levels,
                "fall": fall,
                "walls": walls,
                "excess": fall - walls,
                "owed": walls - rem_was,
                "remainder_was": rem_was,
                "remainder": rem,
                "paid": fall + rem_was - rem,
                "paid_eq_walls": fall + rem_was - rem == walls,
                "step_at_take": step,
                "remainder_below_step": rem < step if step > 0 else rem == 0,
            }
        )
        undo.append((now_was, rem_was))
    for now_was, rem_was in reversed(undo):
        take_mod.lay(node, node.records().index(gap0), at, (now_was - int(z.now[at]), 0, 0, 0))
        node.closes[at] -= 1
        node.take_rem[at] = rem_was
    after_hash = node.state_hash()
    out = {
        "flag": flag,
        "feed": feed,
        "walls": walls,
        "unit_gap0": node.unit_gap0,
        "step_h0_at_feed": h0,
        "remainder_born": rem0,
        "takes": len(undo),
        "excess_above_0_count": sum(1 for r_ in rows if "excess" in r_ and r_["excess"] > 0),
        "paid_eq_walls_count": sum(1 for r_ in rows if r_.get("paid_eq_walls")),
        "remainder_below_step_count": sum(1 for r_ in rows if r_.get("remainder_below_step")),
        "sum_fall": sum(r_["fall"] for r_ in rows if "fall" in r_),
        "sum_walls": sum(r_["walls"] for r_ in rows if "walls" in r_),
        "sum_excess_tenthousandths": [sum(r_["excess"] for r_ in rows if "excess" in r_) * 10000 // (walls * max(1, len(undo))), sum(r_["excess"] for r_ in rows if "excess" in r_) * 10000 % (walls * max(1, len(undo)))],
        "sum_excess_hundredths": [
            sum(r_["excess"] for r_ in rows if "excess" in r_) * 100 // (walls * max(1, len(undo))),
            sum(r_["excess"] for r_ in rows if "excess" in r_) * 100 % (walls * max(1, len(undo))),
        ],
        "remainder_course": [r_.get("remainder") for r_ in rows],
        "levels_course": [r_.get("levels") for r_ in rows],
        "excess_course": [r_.get("excess") for r_ in rows],
        "run_back_match": before_hash == after_hash,
        "integers_bits": node.census(),
        "remainder_bits_max": max((r_.get("remainder", 0) or 0).bit_length() for r_ in rows),
    }
    print(json.dumps(out, default=str))


if __name__ == "__main__":
    main(sys.argv)
