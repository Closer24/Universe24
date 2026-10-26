"""H-Click-Beyond-Rule3-2: every click by kind on a record, with the three choices read at each (the twist's sign and the + end; the draw's digit and the plane born; the refusal's reading) and the one object's three readings (the sign of the Link's odd bilinear F h, the remainder's digit, the standing row's quotient against 0) compared with the head's choices. A reader: the engine run through run.record (no toy), close.meet and close.refuse wrapped to read what they read, nothing written. Integers only.

Usage: PYTHONPATH=<src> python cx2_clicks.py <world.json> <intervals> <out.json> [cube N] [image K] [back N] [src <path>]
  image K: the world run from its K-th image of the kit's 48 (the signed permutations about the origin), the readings carried back through the image.
"""

from __future__ import annotations

import itertools
import json
import sys
from typing import Any

import numpy as np


def arg_after(argv: list[str], key: str, default: str | None) -> str | None:
    return argv[argv.index(key) + 1] if key in argv else default


SRC = arg_after(sys.argv, "src", None)
if SRC:
    sys.path.insert(0, SRC)
sys.set_int_max_str_digits(0)

from event_universe import close, gram, run  # noqa: E402
from event_universe.core.ports import AXES, across, port_of  # noqa: E402
from event_universe.links import row_current, row_twist  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.rows import PLANE  # noqa: E402
from event_universe.take import neighbour  # noqa: E402

IMAGES = [
    np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
    for pi in itertools.permutations(range(3))
    for s in itertools.product((1, -1), repeat=3)
]


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def image(m: np.ndarray, node: Any, cube: int) -> tuple[int, ...]:
    return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))


def world_image(world: dict, m: np.ndarray, cube: int) -> dict:
    found = dict(world, shape=[cube] * 3, seed=[dict(lay) for lay in world["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, lay[key], cube))
    return found


MET: list[dict[str, Any]] = []
REFUSED: list[dict[str, Any]] = []
ORIGINAL_MEET = close.meet
ORIGINAL_REFUSE = close.refuse


def reading_meet(node: Any, rec: int, start: Any, sh: Any, rules: Any, frozen: Any) -> Any:
    """close.meet's reads, read again before the act: per Link met, the current F, the twist h, the two ends' charges, the rest case, the end the current flows into, and the one object's sign reading."""
    row, unit = node.records()[rec], node.units[rec]
    standing = np.vectorize(lambda v: int(v) >= unit, otypes=[bool])(sh) & ~frozen
    currents = [node.den * row_current(start, port_of(axis, 0)) for axis in range(AXES)]
    twists = [row_twist(start, axis) for axis in range(AXES)]
    charges = gram.charge(row.shape, start) if row is not node.emitter() else None
    for axis in range(AXES):
        both = standing & across(standing, port_of(axis, 0))
        for where in zip(*np.nonzero(both), strict=True):
            at = tuple(int(x) for x in where)
            j = neighbour(node, at, port_of(axis, 0))
            flow, h = int(currents[axis][at]), int(twists[axis][at])
            w = [0, 0] if charges is None else [int(charges[at]), int(charges[j])]
            rest = flow == 0 and w[0] * w[1] < 0
            odd = flow * h if not rest else w[1] - w[0]
            MET.append(
                {
                    "i": node.interval,
                    "rec": rec,
                    "at": at,
                    "j": j,
                    "axis": axis,
                    "flow": flow,
                    "h": h,
                    "w": w,
                    "rest": rest,
                    "odd": odd,
                    "plus_pred": j if odd > 0 else at,
                    "into": (j if flow > 0 else at) if not rest else (at if w[0] > 0 else j),
                }
            )
    born = ORIGINAL_MEET(node, rec, start, sh, rules, frozen)
    for b in born:
        key = (b.at, b.rec)
        drawn = node.drawn.get(key)
        for m in MET:
            if m["i"] == node.interval and m["rec"] == rec and {m["at"], m["j"]} == {b.minus, b.plus}:
                m["born"] = True
                m["plus_head"] = b.plus
                m["plane_head"] = b.line_pair
                m["room"] = b.room
                m["number"] = None if drawn is None else drawn[0]
                planes = [k for k, r in enumerate(node.records()) if r.shape == PLANE]
                m["plane_pred"] = (
                    close.list_of(node, rec, drawn[0]) if drawn is not None else close.list_of(node, rec, 0)
                )
                m["planes"] = len(planes)
    return born


def reading_refuse(node: Any, born: Any, owns: Any) -> Any:
    """close.refuse's reads: the standing row's share at each end, the refusal's quotient."""
    for b in born:
        s = b.line_pair
        REFUSED.append(
            {
                "i": node.interval,
                "at": b.at,
                "rec": b.rec,
                "plane": s,
                "minus": b.minus,
                "plus": b.plus,
                "owns": [int(owns[s][b.minus]), int(owns[s][b.plus])],
                "inverse": node.records()[s] is node.emitter() is not node.records()[b.rec],
            }
        )
    kept = ORIGINAL_REFUSE(node, born, owns)
    kept_keys = {(k.at, k.line_pair, k.minus, k.plus) for k in kept}
    for r in REFUSED:
        if r["i"] == node.interval:
            r["kept"] = (r["at"], r["plane"], r["minus"], r["plus"]) in kept_keys
    return kept


close.meet = reading_meet
close.refuse = reading_refuse


def main(argv: list[str]) -> None:
    world_path, intervals, out_path = argv[1], int(argv[2]), argv[3]
    universe, world = load_world(world_path)
    cube = int(arg_after(argv, "cube", str(world["shape"][0])))
    k = int(arg_after(argv, "image", "0"))
    back = int(arg_after(argv, "back", "0"))
    m = IMAGES[k]
    world = world_image(dict(world, intervals=intervals), m, cube)
    rec = run.record(universe, world, back, lambda line: None)
    log = rec["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    stops = [e for e in log if e["event"] == "refused" and e["cause"] == "stop"]
    lays = [e for e in log if e["event"] == "refused" and e["cause"] == "lay"]
    mi = m.T
    # (1) the births: the + end by the one object's sign, the plane by the digit, the refusal by the quotient
    met_born = [x for x in MET if x.get("born")]
    rows = []
    sign_ok = plane_ok = refuse_ok = 0
    light_taken = pair_taken = rest_births = 0
    for x in met_born:
        s_ok = x["plus_pred"] == x["plus_head"]
        p_ok = x["plane_pred"] == x["plane_head"]
        sign_ok += s_ok
        plane_ok += p_ok
        rows.append(
            {
                "i": x["i"],
                "rec": x["rec"],
                "link": [list(image(mi, x["at"], cube)), list(image(mi, x["j"], cube))],
                "axis": x["axis"],
                "flow_sign": sign(x["flow"]),
                "h_sign": sign(x["h"]),
                "odd_sign": sign(x["odd"]),
                "rest": x["rest"],
                "plus_head": list(image(mi, x["plus_head"], cube)),
                "plus_pred": list(image(mi, x["plus_pred"], cube)),
                "sign_ok": s_ok,
                "number": x["number"],
                "room": x["room"],
                "plane_head": x["plane_head"],
                "plane_pred": x["plane_pred"],
                "plane_ok": p_ok,
            }
        )
    crowded = 0
    for r in REFUSED:
        pred = r["inverse"] or max(r["owns"]) == 0
        if pred and not r.get("kept"):
            crowded += 1
        refuse_ok += pred == bool(r.get("kept"))
    # the kinds of click
    kinds = {
        "light_taken_births": sum(1 for e in births if "takes" not in e),
        "pair_taken_mergers": sum(1 for e in births if "takes" in e),
        "rest_births": sum(1 for x in met_born if x["rest"]),
        "credits": len(credits),
        "laid_back": sum(1 for e in credits if "laid_back" in e),
        "stops": len(stops),
        "lay_refusals": len(lays),
        "turns": int(rec["counts"]["turns"]),
    }
    # the credits' three readings from the log: the direction t, the line k, the bound (stop) and the lay-back
    cred = {
        "toward_before": sum(1 for e in credits if sign(e["taker"][1] - e["taker"][0]) * e["levels"] >= 0 and e["levels"] > 0),
        "levels_le_dist": sum(1 for e in credits if e["levels"] <= abs(e["taker"][1] - e["taker"][0])),
        "taken_line_0": sum(1 for e in credits if e["taken_line"] == 0),
        "taken_line_1": sum(1 for e in credits if e["taken_line"] == 1),
        "sense_plus": sum(1 for e in credits if e["sense"] > 0),
        "sense_minus": sum(1 for e in credits if e["sense"] < 0),
        "turned": sum(1 for e in credits if e["turned"]),
        "exact_take": sum(
            1 for e in credits if e["taken"] + e["remainder_was"] - e["remainder"] == e["booked"]
        ),
        "stops_fall_below_walls": sum(1 for e in stops if e.get("fall", 0) < e.get("walls", 0)),
    }
    birth_exact = sum(
        1 for e in births if "remainder_was" in e and e["taken"] + e["remainder_was"] - e["remainder"] == e["booked"]
    )
    summary = {
        "world": world_path,
        "cube": cube,
        "image": k,
        "intervals": intervals,
        "counts": rec["counts"],
        "run_back": rec["run_back"],
        "kinds": kinds,
        "births_read": len(met_born),
        "sign_from_odd_bilinear": [sign_ok, len(met_born)],
        "plane_from_digit": [plane_ok, len(met_born)],
        "refusal_from_quotient": [refuse_ok, len(REFUSED)],
        "refused_lay_by_share": sum(1 for r in REFUSED if max(r["owns"]) > 0),
        "refused_crowded": crowded,
        "refused_shares_at_emitter_row": sum(1 for r in REFUSED if max(r["owns"]) > 0 and r["plane"] == r["rec"]),
        "inverse_kept_with_standing": sum(1 for r in REFUSED if r["inverse"] and max(r["owns"]) > 0),
        "birth_exact_take": [birth_exact, len(births)],
        "credits": cred,
        "met_links": len(MET),
        "twist_sign_counts": {
            "h_pos": sum(1 for x in met_born if x["h"] > 0),
            "h_neg": sum(1 for x in met_born if x["h"] < 0),
            "odd_pos": sum(1 for x in met_born if x["odd"] > 0),
            "odd_neg": sum(1 for x in met_born if x["odd"] < 0),
        },
    }
    record_path = arg_after(argv, "record", None)
    if record_path:
        with open(record_path, "w", encoding="utf-8") as out:
            json.dump(rec, out)
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump({"summary": summary, "births": rows, "refusals": REFUSED and [
            dict(r, at=list(image(mi, r["at"], cube)), minus=list(image(mi, r["minus"], cube)), plus=list(image(mi, r["plus"], cube)))
            for r in REFUSED
        ]}, out, default=str)
    print(json.dumps(summary, default=str), flush=True)


if __name__ == "__main__":
    main(sys.argv)
