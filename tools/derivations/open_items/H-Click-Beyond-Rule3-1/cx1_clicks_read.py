"""H-Click-Beyond-Rule3-1: the three choices of the click read beside the one object at every click, on the engine's own close (no toy, no import of node or interval: run.record through a wrapped close).

The one object at a Link (i, j) of the taken row: the pair of Rule3's carried divisions at the two ends, read three ways: (i) the antisymmetric part, the determinant D = F_a (u_b u'_c - u_c u'_b) of the Link's current and the two ends' transverse net currents (the hand: the + child at j where D > 0; at rest, F = 0, D = w_j - w_i, the charges' difference); (ii) the remainder part, every line's remainder at the Node and its six neighbours on its lattice, the digit r div F_lat (the draw: the plane born); (iii) the symmetric part, the standing share at the child's end (the refusal: the lay refused where it is above 0).

Usage: python cx1_clicks_read.py <world.json or record.json> <intervals> <out.json> [back N]
Prints one JSON summary; integers only."""

from __future__ import annotations

import json
import sys
from typing import Any

sys.set_int_max_str_digits(0)

from event_universe import close, draw, run  # noqa: E402
from event_universe.core.ports import AXES, port_of  # noqa: E402
from event_universe.core.rule3 import quotient, remainder  # noqa: E402
from event_universe.loader.world import read_world  # noqa: E402
from event_universe.rows import PLANE  # noqa: E402
from event_universe.take import at_node, frame_nodes, neighbour  # noqa: E402


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def cross(a: int, b: int, c: int, d: int) -> int:
    return a * d - b * c


COUNTS: dict[str, int] = {}
ROWS: list[dict[str, Any]] = []
DRAWS: dict[str, int] = {}


def bump(key: str, n: int = 1) -> None:
    COUNTS[key] = COUNTS.get(key, 0) + n


def level(line: Any, slot: str, at: tuple[int, ...]) -> int:
    return int(getattr(line, slot)[at])


def link_current_at(node: Any, lines: list[Any], i: tuple[int, ...], j: tuple[int, ...]) -> int:
    """F_ij = SUM_lines (now_i before_j - before_i now_j), the law's one bilinear read from the levels."""
    return sum(
        cross(level(z, "now", i), level(z, "before", i), level(z, "now", j), level(z, "before", j))
        for z in lines
    )


def net_current_at(node: Any, lines: list[Any], at: tuple[int, ...], axis: int) -> int:
    """u_b(k) = F(k, k - b) - F(k, k + b)."""
    down, up = neighbour(node, at, port_of(axis, 1)), neighbour(node, at, port_of(axis, 0))
    return link_current_at(node, lines, at, down) - link_current_at(node, lines, at, up)


def one_object(node: Any, lines: list[Any], charges: Any, i: tuple[int, ...], j: tuple[int, ...], axis: int) -> dict[str, int]:
    """The determinant D at the Link (i, j = i + e_axis): F_a times the twist of the transverse net currents; at F = 0 the charges' difference w_j - w_i."""
    b, c = (axis + 1) % AXES, (axis - 1) % AXES
    f = link_current_at(node, lines, i, j)
    ub, uc = net_current_at(node, lines, i, b), net_current_at(node, lines, i, c)
    vb, vc = net_current_at(node, lines, j, b), net_current_at(node, lines, j, c)
    h = cross(ub, uc, vb, vc)
    wi = 0 if charges is None else int(charges[i])
    wj = 0 if charges is None else int(charges[j])
    d = f * h if f != 0 else wj - wi
    return {"F": f, "h": h, "D": d, "w_i": wi, "w_j": wj}


ORIG_MEET, ORIG_REFUSE, ORIG_READ = close.meet, close.refuse, close.read_number


def meet_wrapped(node: Any, rec: int, start: list[Any], sh: Any, rules: Any, frozen: Any) -> list[Any]:
    born = ORIG_MEET(node, rec, start, sh, rules, frozen)
    row = node.records()[rec]
    from event_universe import gram  # noqa: PLC0415

    charges = gram.charge(row.shape, start) if row is not node.emitter() else None
    planes = [k for k, r in enumerate(node.records()) if r.shape == PLANE]
    kind = "light_taken" if row is node.emitter() else "pair_taken"
    for birth in born:
        at, s, minus, plus, room, rec_ = birth
        axis = [a for a in range(AXES) if minus[a] != plus[a]][0]
        # i is the end from which the + axis Port leads to the other end
        i, j = (minus, plus) if neighbour(node, minus, port_of(axis, 0)) == plus else (plus, minus)
        obj = one_object(node, start, charges, i, j, axis)
        rest = obj["F"] == 0
        plus_at_j = plus == j
        hand_given = (obj["D"] > 0) == plus_at_j and obj["D"] != 0
        bump(kind + "_births")
        bump(kind + "_rest" if rest else kind + "_moving")
        bump(kind + "_hand_given_by_D", hand_given)
        drawn = node.drawn.get((at, rec_))
        digit_given = None
        if row is not node.emitter():
            bump(kind + "_plane_is_emitter_by_law", s == node.records().index(node.emitter()))
        elif not rest and drawn is not None:
            number, _room = drawn
            digit_given = planes[int(remainder(quotient(number, node.units[rec_]), len(planes)))] == s
            bump(kind + "_draw_read")
            bump(kind + "_digit_gives_plane", bool(digit_given))
        ROWS.append(
            {
                "i": node.interval,
                "kind": kind,
                "rec": rec_,
                "axis": axis,
                "i_end": list(i),
                "j_end": list(j),
                "plus": list(plus),
                **obj,
                "rest": rest,
                "hand_given": hand_given,
                "drawn": None if drawn is None else [int(drawn[0]), int(drawn[1])],
                "plane": s,
                "digit_gives_plane": digit_given,
            }
        )
    return born


def refuse_wrapped(node: Any, born: list[Any], owns: list[Any]) -> list[Any]:
    before = len(node.log)
    kept = ORIG_REFUSE(node, born, owns)
    for entry in node.log[before:]:
        if entry.get("cause") == "lay":
            bump("refused_lay_by_state" if "standing" in entry else "refused_lay_crowded")
    # the symmetric part: every kept birth's two ends below the unit, every refused-by-state birth one end at or above it
    for k in kept:
        if int(owns[k.line_pair][k.minus]) <= 0 and int(owns[k.line_pair][k.plus]) <= 0:
            bump("kept_share_zero_both_ends")
        else:
            bump("kept_share_above_zero")
    bump("born_in", len(born))
    bump("kept_out", len(kept))
    return kept


def read_wrapped(node: Any, at: tuple[int, ...], rules: Any, unit: int) -> Any:
    got = ORIG_READ(node, at, rules, unit)
    modulus = unit * sum(1 for r in node.records() if r.shape == PLANE)
    nodes = frame_nodes(node, at)
    digits, mirrored, w = [], [], int(node.w)
    for line, r in rules:
        for k, n in enumerate(nodes):
            key = (id(r), k, n)
            if key not in node.lattices:
                continue
            f, wl = int(node.lattices[key]), at_node(line.wall, n)
            rem = int(line.rem[n])
            base = int(quotient(wl, f)) + 1
            d, dm = int(quotient(rem, f)), int(quotient(wl - 1 - rem, f))
            digits.append((d, base))
            mirrored.append((dm, base))
            bump("digit_reads")
            bump("digit_mirror_covariant", dm == base - 1 - d)
            bump("digit_lattice_divides_wall", remainder(wl, f) == 0)
            bump("digit_lattice_one", f == 1)
    if got is None:
        bump("draw_refused")
        return got
    planes = sum(1 for r in node.records() if r.shape == PLANE)

    def compose(ds: list[tuple[int, int]]) -> int:
        carry = 0
        for d, b in sorted(ds):
            carry = remainder(carry * b + d, modulus)
        return int(carry)

    same_plane = remainder(quotient(compose(digits), unit), planes) == remainder(
        quotient(compose(mirrored), unit), planes
    )
    bump("draws")
    bump("draw_recomposed_equal", compose(digits) == int(got[0]))
    bump("draw_mirror_same_plane", bool(same_plane))
    return got


def main(argv: list[str]) -> None:
    path, intervals, out = argv[1], int(argv[2]), argv[3]
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 10
    raw = json.loads(open(path, encoding="utf-8").read())
    if "world" in raw and "universe" in raw and "log" in raw:
        universe, world = read_world(raw["world"], raw["universe"])
    else:
        from event_universe.loader.world import load_world  # noqa: PLC0415

        universe, world = load_world(path)
    world = dict(world, intervals=intervals)
    close.meet, close.refuse, close.read_number = meet_wrapped, refuse_wrapped, read_wrapped
    draw.read_number = ORIG_READ
    rec = run.record(universe, world, back=back, out=lambda s: None)
    log = rec["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    mergers = [e for e in births if "takes" in e]
    bump("log_births", len(births))
    bump("log_mergers", len(mergers))
    bump("log_credits", len(credits))
    bump("log_credits_laid_back", sum(1 for e in credits if "laid_back" in e))
    bump("log_credits_sense_plus", sum(1 for e in credits if e["sense"] > 0))
    bump("log_credits_sense_minus", sum(1 for e in credits if e["sense"] < 0))
    # the merger as the birth reversed: a pair taken whole at two ends of opposite charge, light laid at both
    conj = 0
    for e in mergers:
        ws = []
        for t in e["takes"]:
            rn, rb, im_n, im_b = t["taken_levels"]
            ws.append(cross(rn, im_n, rb, im_b))
        conj += int(len(ws) == 2 and ws[0] * ws[1] < 0)
    bump("mergers_conjugate_pair_taken", conj)
    bump("mergers_light_laid_both_ends", sum(1 for e in mergers if all(x is not None for x in e.get("exact_lay", []))))
    bump("births_children_W_opposite", sum(1 for e in births if e["W_children"][0] * e["W_children"][1] < 0))
    bump("births_W_sum_zero", sum(1 for e in births if e["W_children"][0] + e["W_children"][1] == 0))
    summary = {
        "world": path,
        "intervals": intervals,
        "counts": COUNTS,
        "engine_counts": rec["counts"],
        "run_back": rec["run_back"],
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "rows": ROWS}, f)
    print(json.dumps(summary))


if __name__ == "__main__":
    main(sys.argv)
