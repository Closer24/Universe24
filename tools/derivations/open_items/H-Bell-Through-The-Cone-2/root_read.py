"""Bell read through the root (hand bc2): the board run forward from the seed with the state's hash kept at every interval, then run back from the last interval to the first (the run back, every act its own inverse), each interval compared bit for bit; for every born pair the two children's clicks (the first credit of the children's record at each end after the birth), the intervals from each click back to the birth (the backward run's length), the Link distance from each click's Node to the birth's Link (the cone: one Link per interval backward), the root's integers from the birth line (what both children share), the outcomes at the clicks under four settings (the frame's axis p re_now + q im_now, and the sense), the outcomes read at the root (the lay's levels with the sense), the per-pair identity A(a) B(b) - A(a) B(b') + A(a') B(b) + A(a') B(b') and S over the pairs as one rational, by the clicks and by the root. Integers only; no act touched.

Usage: python root_read.py <world.json> <out.json>"""
import json
import sys
import time
from collections import defaultdict

from event_universe.node import Node
from event_universe.run import load_world

SETTINGS_A = ((1, 0), (1, 1))
SETTINGS_B = ((12, 5), (5, 12))
SETTINGS = SETTINGS_A + SETTINGS_B


def sign(x):
    return (x > 0) - (x < 0)


def outcome(frame, setting):
    p, q = setting
    return sign(p * frame["re_now"] + q * frame["im_now"])


def torus_distance(a, b, cube):
    return sum(min(abs(x - y), cube - abs(x - y)) for x, y in zip(a, b))


def pairs_of(log):
    """Every birth with its two ends' first credits (the children's record at the end's Node after the birth's interval)."""
    credits = defaultdict(list)
    for e in log:
        if e["event"] == "credit":
            credits[(tuple(e["node"]), e["line"])].append(e)
    found = []
    for b in log:
        if b["event"] != "birth":
            continue
        ends = []
        for where in (b["minus"], b["plus"]):
            later = [c for c in credits[(tuple(where), b["line_pair"])] if c["i"] > b["i"]]
            ends.append(min(later, key=lambda c: c["i"]) if later else None)
        found.append((b, ends[0], ends[1]))
    return found


def root_of(b):
    """The integers at the birth's Link that both children share: the children's record, the senses, the Wronskians, the lay's levels (a, 0, 0, -+b), the taken row and line, the taker's levels at the take, the room and the proper count."""
    return {
        "i": b["i"],
        "node": b["node"],
        "minus": b["minus"],
        "plus": b["plus"],
        "line_pair": b["line_pair"],
        "senses": b["senses"],
        "W_children": b["W_children"],
        "amplitude": b["amplitude"],
        "taken_row": b.get("taken_row"),
        "taken_line": b.get("taken_line"),
        "taken_now_was": b.get("taken_now_was"),
        "taker": b.get("taker"),
        "room": str(b.get("room")),
        "proper": b.get("proper"),
    }


def root_outcome(root, end, setting):
    """The outcome read at the root: the child's levels at the lay, (a, 0, 0, -+b): re_now = a, im_now = 0 at both ends (the lay's tuple (re_now, re_before, im_now, im_before)); the frame's axis reads sign(p a) at both ends alike; the sense reads -1 at the minus end and +1 at the plus end."""
    a, _b = root["amplitude"]
    p, q = setting
    return sign(p * a + q * 0)


def identity(a_out, b_out):
    """A(a) B(b) - A(a) B(b') + A(a') B(b) + A(a') B(b') from the four outcomes of one pair; 0 where an outcome is 0 enters as 0."""
    a0, a1 = a_out
    b0, b1 = b_out
    return a0 * b0 - a0 * b1 + a1 * b0 + a1 * b1


def chsh(rows):
    """S = SUM over the pairs of the identity, over the pairs' count: one rational (num, den)."""
    return sum(rows), len(rows)


def main(argv):
    sys.set_int_max_str_digits(0)
    world_path, out_path = argv[1], argv[2]
    universe, world = load_world(world_path)
    node = Node(universe, world)
    intervals = int(world["intervals"])
    t0 = time.monotonic_ns()
    hashes = [node.state_hash()]
    for _ in range(intervals):
        node.step()
        hashes.append(node.state_hash())
    forward_ms = (time.monotonic_ns() - t0) // 1000000
    log = list(node.log)
    cube = node.cube
    pairs = pairs_of(log)
    both = [p for p in pairs if p[1] is not None and p[2] is not None]
    # the run back from the last interval to the first, each interval compared bit for bit
    t1 = time.monotonic_ns()
    exact_at = {}
    for k in range(intervals, 0, -1):
        node.step_back()
        exact_at[k - 1] = node.state_hash() == hashes[k - 1]
    back_ms = (time.monotonic_ns() - t1) // 1000000
    per_pair = []
    ids_click_frame, ids_click_sense, ids_root_frame, ids_root_sense = [], [], [], []
    for b, m, p in both:
        root = root_of(b)
        d_m, d_p = m["i"] - b["i"], p["i"] - b["i"]
        a_click = [outcome(m["frame"], s) for s in SETTINGS_A]
        b_click = [outcome(p["frame"], s) for s in SETTINGS_B]
        a_sense = [m["sense"]] * 2
        b_sense = [p["sense"]] * 2
        a_root = [root_outcome(root, 0, s) for s in SETTINGS_A]
        b_root = [root_outcome(root, 1, s) for s in SETTINGS_B]
        a_root_sense = [root["senses"][0]] * 2
        b_root_sense = [root["senses"][1]] * 2
        # the backward run from each click to the birth: every interval between them exact
        back_exact = all(exact_at[i] for i in range(b["i"], max(m["i"], p["i"])))
        row = {
            "birth i": b["i"],
            "clicks i": [m["i"], p["i"]],
            "intervals back to the birth": [d_m, d_p],
            "Link distance click to the birth's Link": [
                min(torus_distance(m["node"], b["minus"], cube), torus_distance(m["node"], b["plus"], cube)),
                min(torus_distance(p["node"], b["minus"], cube), torus_distance(p["node"], b["plus"], cube)),
            ],
            "within the cone (distance <= intervals back)": True,
            "run back exact from the clicks to the birth": back_exact,
            "root": root,
            "outcomes at the clicks, the frame (A at a, a'; B at b, b')": [a_click, b_click],
            "outcomes at the clicks, the sense": [m["sense"], p["sense"]],
            "outcomes at the root, the frame": [a_root, b_root],
            "outcomes at the root, the sense": root["senses"],
            "identity at the clicks, the frame": identity(a_click, b_click),
            "identity at the clicks, the sense": identity(a_sense, b_sense),
            "identity at the root, the frame": identity(a_root, b_root),
            "identity at the root, the sense": identity(a_root_sense, b_root_sense),
        }
        row["within the cone (distance <= intervals back)"] = all(
            dist <= d for dist, d in zip(row["Link distance click to the birth's Link"], row["intervals back to the birth"])
        )
        per_pair.append(row)
        ids_click_frame.append(row["identity at the clicks, the frame"])
        ids_click_sense.append(row["identity at the clicks, the sense"])
        ids_root_frame.append(row["identity at the root, the frame"])
        ids_root_sense.append(row["identity at the root, the sense"])

    def summary(ids):
        num, den = chsh(ids)
        return {
            "S as a rational": [num, den],
            "S in hundredths": (num * 100) // den if den else None,
            "S^2 > 8 (nature)": num * num > 8 * den * den if den else None,
            "|S| <= 2": abs(num) <= 2 * den if den else None,
            "identity per pair": {str(k): ids.count(k) for k in sorted(set(ids))},
        }

    out = {
        "world": world_path,
        "cube": cube,
        "intervals": intervals,
        "forward ms": forward_ms,
        "run back ms": back_ms,
        "run back exact, intervals": sum(exact_at.values()),
        "run back intervals": intervals,
        "births": sum(1 for e in log if e["event"] == "birth"),
        "pairs clicked at both ends": len(both),
        "pairs with one end clicked": sum(1 for p in pairs if (p[1] is None) != (p[2] is None)),
        "every pair's clicks within the cone": all(r["within the cone (distance <= intervals back)"] for r in per_pair),
        "every pair's run back exact to its birth": all(r["run back exact from the clicks to the birth"] for r in per_pair),
        "intervals back to the birth, max": max((max(r["intervals back to the birth"]) for r in per_pair), default=0),
        "S at the clicks by the frame": summary(ids_click_frame),
        "S at the clicks by the sense": summary(ids_click_sense),
        "S through the root by the frame (the lay's levels)": summary(ids_root_frame),
        "S through the root by the sense": summary(ids_root_sense),
        "root integers equal under the four settings": True,
        "pairs": per_pair,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f)
    brief = {k: v for k, v in out.items() if k != "pairs"}
    print(json.dumps(brief))


if __name__ == "__main__":
    main(sys.argv)
