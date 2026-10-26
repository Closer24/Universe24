"""Bell read through the root (hand bc1): the world run forward with the state's hash kept at every interval; every birth's two children (the - child at `minus`, the + child at `plus`, their record `line_pair`) and each child's first credit at its own Node and line after the birth (the click of that end); the cone of each click (the torus distance from the click's Node to its own birth end against the intervals since the birth); then the run back from the last interval to the earliest birth, one interval per step, every kept hash compared bit for bit, so that the state at every birth's interval (the shared root of its pair) is recovered from after the clicks by the law's own inverse; the children's integers at the two ends at the birth captured forward and read again after the run back. The reading: the outcome at a setting (p, q) the sign of p re_now + q im_now of the click's frame, the four settings of the former Bell worlds, the per-pair identity A(a) B(b) - A(a) B(b') + A(a') B(b) + A(a') B(b'), E and S by the frame, by the senses, and through the root (the same outcomes conditioned on the root's recovered state, which is one and the same for the four settings), and the one-setting form where each end's setting is drawn by a digit of its own click (the turned bit of the credit). Integers only; no act of the engine touched.

Usage: python bell_root_bc1.py <world.json> <out.json>"""
import json
import sys
from collections import defaultdict

from event_universe.loader.world import load_world
from event_universe.node import Node

SETTINGS_A = ((1, 0), (1, 1))
SETTINGS_B = ((12, 5), (5, 12))
THOUSAND = 1000


def sign(x):
    return (x > 0) - (x < 0)


def outcome(credit, setting):
    p, q = setting
    f = credit["frame"]
    return sign(p * f["re_now"] + q * f["im_now"])


def torus_distance(a, b, cube):
    return sum(min(abs(x - y), cube - abs(x - y)) for x, y in zip(a, b))


def ints_at(node, s, where):
    """The children's row's integers at one Node: every line's now, before and remainder (and the write remainder where the row writes), as plain integers; [] where the row's lines are not reachable by name."""
    try:
        row = node.records()[s]
        idx = tuple(int(x) for x in where)
        out = []
        for line in row.lines:
            out.append([int(line.now[idx]), int(line.before[idx]), int(line.rem[idx])])
            if line.wr is not None:
                out[-1].append(int(line.wr[idx]))
        return out
    except Exception as e:  # the capture is a reading beside the hash, never the measurement
        return [str(type(e).__name__)]


def pairs_of(log):
    credits = defaultdict(list)
    for e in log:
        if e["event"] == "credit":
            credits[(tuple(e["node"]), e["line"])].append(e)
    births = [e for e in log if e["event"] == "birth"]
    found = []
    for b in births:
        s = b["line_pair"]
        ends = []
        for where in (b["minus"], b["plus"]):
            later = [c for c in credits[(tuple(where), s)] if c["i"] > b["i"]]
            ends.append(min(later, key=lambda c: c["i"]) if later else None)
        found.append((b, ends[0], ends[1]))
    return births, found


def correlation(pairs, a, b, key):
    same = opposite = 0
    for birth, minus, plus in pairs:
        x, y = key(minus, a, birth), key(plus, b, birth)
        if x == 0 or y == 0:
            continue
        if x == y:
            same += 1
        else:
            opposite += 1
    return same - opposite, same + opposite


def chsh(pairs, key):
    es = {}
    for ia, a in enumerate(SETTINGS_A):
        for ib, b in enumerate(SETTINGS_B):
            es[(ia, ib)] = correlation(pairs, a, b, key)
    terms = [(1, es[(0, 0)]), (-1, es[(0, 1)]), (1, es[(1, 0)]), (1, es[(1, 1)])]
    num, den = 0, 1
    for sgn, (n, d) in terms:
        if d == 0:
            return es, None
        num, den = num * d + sgn * n * den, den * d
    return es, (num, den)


def identity(minus, plus):
    """The per-pair identity on the four outcomes read from the two credit lines."""
    a0, a1 = outcome(minus, SETTINGS_A[0]), outcome(minus, SETTINGS_A[1])
    b0, b1 = outcome(plus, SETTINGS_B[0]), outcome(plus, SETTINGS_B[1])
    return a0 * b0 - a0 * b1 + a1 * b0 + a1 * b1


def one_setting(pairs, draw):
    """The one-setting form: each end's setting drawn by a digit of its own click; the four E's over four disjoint subsamples; S as a rational where every subsample is filled."""
    es = {}
    for ia, a in enumerate(SETTINGS_A):
        for ib, b in enumerate(SETTINGS_B):
            sub = [p for p in pairs if draw(p[1]) == ia and draw(p[2]) == ib]
            es[(ia, ib)] = correlation(sub, a, b, lambda c, s, _b: outcome(c, s))
    terms = [(1, es[(0, 0)]), (-1, es[(0, 1)]), (1, es[(1, 0)]), (1, es[(1, 1)])]
    num, den = 0, 1
    for sgn, (n, d) in terms:
        if d == 0:
            return es, None
        num, den = num * d + sgn * n * den, den * d
    return es, (num, den)


def rational_text(r):
    return None if r is None else f"{r[0]} / {r[1]}"


def thousandths(r):
    return None if r is None or r[1] == 0 else (r[0] * THOUSAND) // r[1]


def main(world_path, out_path):
    universe, world = load_world(world_path)
    node = Node(universe, world)
    intervals = int(world["intervals"])
    hashes = {node.interval: node.state_hash()}
    roots_forward = {}
    seen = 0
    for _t in range(intervals):
        node.step()
        hashes[node.interval] = node.state_hash()
        for e in node.log[seen:]:
            if e["event"] == "birth":
                key = (e["i"], tuple(e["minus"]), tuple(e["plus"]), e["line_pair"])
                roots_forward[key] = {
                    "interval": node.interval,
                    "minus": ints_at(node, e["line_pair"], e["minus"]),
                    "plus": ints_at(node, e["line_pair"], e["plus"]),
                }
        seen = len(node.log)
    log = list(node.log)
    births, pairs = pairs_of(log)
    both = [p for p in pairs if p[1] is not None and p[2] is not None]
    cube = int(node.cube)

    # the cone of every click: the click's Node against its own birth end, the intervals since the birth
    cone = []
    for b, m, p in both:
        for end, c in (("minus", m), ("plus", p)):
            d = torus_distance(c["node"], b[end], cube)
            back = c["i"] - b["i"]
            cone.append({"birth_i": b["i"], "end": end, "click_i": c["i"], "intervals_back": back, "links_to_birth_end": d, "within_cone": d <= back})

    # the run back: from the last interval to the earliest birth, every kept hash compared
    earliest = min((b["i"] for b in births), default=node.interval)
    last = node.interval
    steps_back = 0
    exact = 0
    compared = []
    roots_back = {}
    birth_intervals = {b["i"] for b in births}
    click_intervals = {c["i"] for _b, m, p in both for c in (m, p)}
    while node.interval > earliest:
        node.step_back()
        steps_back += 1
        same = node.state_hash() == hashes.get(node.interval)
        exact += same
        if node.interval in birth_intervals or node.interval in click_intervals:
            compared.append({"interval": node.interval, "exact": same, "birth": node.interval in birth_intervals, "click": node.interval in click_intervals})
        for key, cap in roots_forward.items():
            if cap["interval"] == node.interval:
                roots_back[key] = {
                    "minus": ints_at(node, key[3], key[1]),
                    "plus": ints_at(node, key[3], key[2]),
                }
    roots_equal = sum(1 for k in roots_forward if k in roots_back and roots_back[k]["minus"] == roots_forward[k]["minus"] and roots_back[k]["plus"] == roots_forward[k]["plus"])

    # the readings
    frame_key = lambda c, s, _b: outcome(c, s)
    sense_key = lambda c, s, _b: c["sense"]
    es_f, s_f = chsh(both, frame_key)
    es_s, s_s = chsh(both, sense_key)
    # through the root: the outcome conditioned on the root's recovered state; the root's hash is the same object for the four settings, so the key reads the same outcome
    root_hash = {b["i"]: hashes.get(b["i"]) for b in births}
    root_key = lambda c, s, b: outcome(c, s) if root_hash.get(b["i"]) is not None else 0
    es_r, s_r = chsh(both, root_key)
    idents = defaultdict(int)
    for _b, m, p in both:
        idents[identity(m, p)] += 1
    draw = lambda c: 1 if c.get("turned") else 0
    es_one, s_one = one_setting(both, draw)
    subsamples = {f"a{ia} b{ib}": d for (ia, ib), (n, d) in es_one.items()}
    draw_parity = lambda c: c["i"] % 2
    es_par, s_par = one_setting(both, draw_parity)
    subsamples_par = {f"a{ia} b{ib}": d for (ia, ib), (n, d) in es_par.items()}

    first = births[0] if births else None
    out = {
        "world": world_path,
        "cube": cube,
        "intervals": intervals,
        "births": len(births),
        "pairs_both_clicked": len(both),
        "root_carried_by_the_birth_line (the first birth)": None if first is None else {k: first[k] for k in ("i", "line_pair", "senses", "W_children", "amplitude", "taken_row", "taken_line", "levels", "taker", "proper", "content", "children_at_node") if k in first},
        "amplitude the same at every birth": len({tuple(b["amplitude"]) for b in births}) <= 1,
        "W_children the same at every birth": len({tuple(b["W_children"]) for b in births}) <= 1,
        "children integers at the two ends at the birth (forward, the first birth)": None if not roots_forward else next(iter(roots_forward.values())),
        "cone": {"clicks": len(cone), "within_cone": sum(1 for c in cone if c["within_cone"]), "links_to_birth_end_max": max((c["links_to_birth_end"] for c in cone), default=0), "intervals_back_min_max": [min((c["intervals_back"] for c in cone), default=0), max((c["intervals_back"] for c in cone), default=0)]},
        "run_back": {"from_interval": last, "to_interval": earliest, "steps": steps_back, "exact": exact, "birth_and_click_intervals_compared": compared, "roots_captured": len(roots_forward), "roots_recovered_equal_every_integer": roots_equal},
        "root_hash_one_per_birth_independent_of_setting": all(v is not None for v in root_hash.values()),
        "E by the frame (same - opposite, pairs)": {f"a{ia} b{ib}": v for (ia, ib), v in es_f.items()},
        "S by the frame": rational_text(s_f),
        "S by the frame (thousandths)": thousandths(s_f),
        "E by the senses": {f"a{ia} b{ib}": v for (ia, ib), v in es_s.items()},
        "S by the senses": rational_text(s_s),
        "E through the root": {f"a{ia} b{ib}": v for (ia, ib), v in es_r.items()},
        "S through the root": rational_text(s_r),
        "S through the root equals S by the frame": s_r == s_f,
        "per-pair identity": dict(sorted(idents.items())),
        "S^2 > 8 through the root": None if s_r is None else s_r[0] * s_r[0] > 8 * s_r[1] * s_r[1],
        "|S| <= 2 through the root": None if s_r is None else abs(s_r[0]) <= 2 * s_r[1],
        "one-setting form (the setting drawn by the click's turned bit): subsample sizes": subsamples,
        "one-setting form: E": {f"a{ia} b{ib}": v for (ia, ib), v in es_one.items()},
        "one-setting form: S": rational_text(s_one),
        "one-setting form: S (thousandths)": thousandths(s_one),
        "one-setting form: S^2 > 8": None if s_one is None else s_one[0] * s_one[0] > 8 * s_one[1] * s_one[1],
        "one-setting form by the click's interval parity: subsample sizes": subsamples_par,
        "one-setting form by the click's interval parity: E": {f"a{ia} b{ib}": v for (ia, ib), v in es_par.items()},
        "one-setting form by the click's interval parity: S": rational_text(s_par),
        "one-setting form by the click's interval parity: S (thousandths)": thousandths(s_par),
        "counts": {k: str(v) for k, v in node.counts.items()},
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out))
    return out


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    main(sys.argv[1], sys.argv[2])
