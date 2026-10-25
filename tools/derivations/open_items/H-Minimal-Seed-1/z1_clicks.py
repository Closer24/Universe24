"""Hand z1: the decoder's conservations read from the credit lines alone (ALGEBRA.md, The Node, The way to a solution,
step 4): the charge (the senses' sum over every birth), the count (taken = walls + excess on every birth and body credit,
the excess 0 or above), the momentum (the credits' running cosine per axis: the signs' sum per axis over the credits),
the energy (the beat per proper interval before and after a click: the beats carried, None counted), and the cube's 48
in the clicks (the multiset of (interval, the support carried by the element about the origin, kind, sense, beat, the
identity's family) the same under the element; the count of the 48 under which it is), with the births' points and the
species the decoder names from the pairs (the lifts by their legs, the lightest the electron's, the next the proton's);
integers only. The folder holds `<tag>.clicks.jsonl`, `<tag>.eras.jsonl`, `<tag>.nodes.jsonl`; the folder is also read
by tools/record_gates.py.

    PYTHONPATH=src python tools/derivations/open_items/H-Minimal-Seed-1/z1_clicks.py tools/derivations/open_items/H-Minimal-Seed-1/out/hole --shape 5 5 5
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from z1lib import ROOT  # noqa: E402

sys.path.insert(0, str(ROOT))
from tests.test_the_board_is_the_cube_48 import axis_map, cube_48  # noqa: E402


def read(folder: Path) -> list[dict]:
    (clicks,) = sorted(folder.glob("*.clicks.jsonl"))
    return [json.loads(line) for line in clicks.read_text().splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    parser.add_argument("--shape", nargs=3, type=int, required=True)
    args = parser.parse_args()
    lines = read(args.folder)
    shape = tuple(args.shape)
    credits = [l for l in lines if l["event"] == "credit"]
    births = [l for l in lines if l["event"] == "birth"]
    lays = [l for l in lines if l["event"] == "lay"]
    header = json.loads(sorted(args.folder.glob("*.eras.jsonl"))[0].read_text().splitlines()[0])
    light = header["seed"]
    light_credits = [c for c in credits if c["family"] == light and c["identity"][0] == header["families"].index(light)]
    body_credits = [c for c in credits if c not in light_credits]
    found: dict = {"folder": args.folder.name, "credits": len(credits), "births": len(births), "lays": len(lays), "light_credits": len(light_credits), "body_credits": len(body_credits)}
    # the charge: the senses' sum over every birth; the senses per close over the body credits
    sums = [sum(b["senses"]) for b in births]
    per_close: dict = Counter()
    for c in body_credits:
        per_close[c["interval"]] += c["sense"]
    found["charge"] = {"births": len(sums), "births_summing_to_zero": sums.count(0), "births_not_zero": [s for s in sums if s != 0][:5], "body_closes": len(per_close), "body_closes_senses_zero": sum(1 for v in per_close.values() if v == 0)}
    # the count: taken = walls + excess on every line that carries a take
    rows = [r for r in [*births, *credits] if r.get("taken") is not None]
    found["count"] = {"take_lines": len(rows), "identity_holds": sum(1 for r in rows if r["taken"] == r["walls"] + r["excess"]), "excess_zero": sum(1 for r in rows if r["excess"] == 0), "excess_below_step": sum(1 for r in rows if r["step"] == 0 or r["excess"] < r["step"]), "excess_over_taken_milli_max": max(((1000 * r["excess"]) // r["taken"] for r in rows if r["taken"]), default=None)}
    # the momentum: the credits' running cosine per axis, the signs' sums
    signs = [[0, 0, 0] for _ in range(3)]
    read_momenta = 0
    for c in credits:
        m = c.get("momentum")
        if not isinstance(m, list):
            continue
        read_momenta += 1
        for a, term in enumerate(m):
            if isinstance(term, list) and term and isinstance(term[0], int):
                signs[a][term[0] + 1] += 1
    found["momentum"] = {"credits_with_momentum": read_momenta, "sign_counts_per_axis_minus_zero_plus": signs, "sign_sum_per_axis": [s[2] - s[0] for s in signs]}
    # the energy: the beat per proper interval, the beats carried
    beats = [c["beat"] for c in credits]
    found["energy"] = {"credits_with_beat": sum(1 for b in beats if b), "credits_beat_none": sum(1 for b in beats if b is None), "credits_beat_zero": sum(1 for b in beats if b == 0), "light_beats": sorted(Counter(c["beat"] for c in light_credits).items(), key=str)[:6], "body_beats": sorted(Counter(c["beat"] for c in body_credits).items(), key=str)[:6], "proper_spacing_body": sorted(Counter(b["proper"] - a["proper"] for a, b in zip(body_credits, body_credits[1:], strict=False) if a["node_detector"] == b["node_detector"] and a["identity"] == b["identity"]).items(), key=str)[:8]}
    # the births' points and the species the decoder names
    points = Counter()
    for b in births:
        for child, point in zip(b["children"], b["points"], strict=True):
            points[(child, tuple(point))] += 1
    found["species"] = {f"{child} {list(point)}": n for (child, point), n in points.items()}
    found["births_per_interval"] = sorted(Counter(b["interval"] for b in births).items())[:40]
    found["birth_intervals_first_last"] = [min((b["interval"] for b in births), default=None), max((b["interval"] for b in births), default=None)]
    found["credits_per_interval_first_last"] = [min((c["interval"] for c in credits), default=None), max((c["interval"] for c in credits), default=None)]
    # the 48 in the clicks: the multiset of the credits and the births carried about the origin
    def carried(node: list[int], m: np.ndarray) -> tuple[int, ...]:
        return tuple(int(v) for v in np.mod(m @ np.array(node), np.array(shape)))

    def multiset(m: np.ndarray) -> Counter:
        rows = Counter()
        for c in credits:
            rows[("credit", c["interval"], carried(c["support"], m), c["kind"], c["sense"], c["beat"], c["identity"][0])] += 1
        for b in births:
            rows[("birth", b["interval"], carried(b["nodes"][0], m), tuple(sorted(b["children"])), tuple(sorted(b["senses"])))] += 1
        return rows

    plain = multiset(np.eye(3, dtype=int))
    kept, mirrors_kept, mirrors = 0, 0, 0
    for m in cube_48():
        is_mirror = axis_map(m)[0] == [0, 1, 2]
        mirrors += is_mirror
        if multiset(m) == plain:
            kept += 1
            mirrors_kept += is_mirror
    found["cube_48_in_the_clicks"] = {"kept": kept, "of": 48, "mirrors_kept": mirrors_kept, "mirrors": mirrors}
    # the one-place view: one Node's credits in its own proper order
    by_node: dict = {}
    for c in credits:
        by_node.setdefault(c["node_detector"], []).append((c["proper"], c["interval"], c["identity"][0], c["beat"]))
    busiest = max(by_node.items(), key=lambda kv: len(kv[1]), default=(None, []))
    found["one_place"] = {"nodes_credited": len(by_node), "busiest_node": busiest[0], "busiest_credits": len(busiest[1]), "busiest_proper_first_last": [busiest[1][0][0], busiest[1][-1][0]] if busiest[1] else None, "proper_monotone": all(a[0] <= b[0] for a, b in zip(busiest[1], busiest[1][1:], strict=False))}
    (args.folder / "clicks_conservations.json").write_text(json.dumps(found, indent=1, default=str) + "\n")
    print(json.dumps(found, default=str))


if __name__ == "__main__":
    main()
