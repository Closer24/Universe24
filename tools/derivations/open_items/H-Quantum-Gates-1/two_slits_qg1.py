"""The two slits on the engine of engine-5.0-test (the hand qg1): two coherent light sources (two `at` lays of the gap-0 row with one `wave`, the slits in Huygens's form) on an empty board, read at a far plane of Nodes.

The law's letter used: Rule3's line is linear in the levels to the carried remainder (The line; The conserved form), so the record of the two sources is the sum of the two single records to the remainders' width (the superposition); the clicks are the meetings (The click is the meeting; the births of close.meet) where both ends of a Link stand at a whole quantum of the gap-0 row, so the clicks sample the intensity above one quantum; the interference term at a Node is the cross term of the conserved form, 2 a b, read as the sum over the intervals of now_AB^2 - now_A^2 - now_B^2 (the same levels, four runs: empty, A, B, AB).

Integers only: every reading a level, a square of levels, a count or a quotient with its remainder; the predicted minima by the integer comparison (s1 - s2 - q)^2 >= 4 q s2 with s1, s2 the squared paths and q the squared half wavelength's scaled form.

Usage: python two_slits_qg1.py [cube] [intervals] [quanta per source] (defaults 11, 30 and 60); writes out/two_slits_qg1.json and prints the table.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from event_universe.core.rule3 import largest_below, quotient
from event_universe.loader.world import read_world
from event_universe.node import Node
from event_universe.rows import PLANE

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
UNIVERSE = HERE.parents[2] / "tests" / "worlds" / "universe_toy.json"


def wave_third(den: int) -> int:
    """h = den sin(pi / 3) to the integer: the wave number k = 2 pi / 3, the wavelength 3 Links, the band's rotation omega = pi / 3 exactly (den cos omega = (den cos k + 2 den) div 3 = den div 2), the group velocity one third of a Link per interval."""
    return largest_below(quotient(3 * den * den, 4))


def world_of(cube: int, intervals: int, sources: list[tuple[int, int, int]], h: int, quanta: int, sea: bool = False) -> dict:
    """The world file: the gap-0 row's packets at the sources' centres, moving along +x at the wave h, the half width 2 (three Nodes across) and the top 3 (five Nodes along x)."""
    return {
        "universe": "universe_toy.json",
        "shape": [cube, cube, cube],
        "intervals": intervals,
        "seed": ([{"lay": "sea", "row": 0}] if sea else []) + [
            {
                "lay": "at",
                "row": 0,
                "centre": list(c),
                "width": 2,
                "quanta": quanta,
                "wave": [h, 0, 0],
                "top": 3,
            }
            for c in sources
        ],
    }


def run_world(universe: dict, world: dict, x_far: int) -> tuple[list[list[list[int]]], dict, dict]:
    """The Node run in process for the world's intervals: the gap-0 line's level now at the plane x = x_far after every interval (intervals x cube x cube), the births' take Nodes and the meetings per Node on that plane."""
    node = Node(universe, dict(world, seed=list(world["seed"])))
    gap0 = node.row(PLANE, gap=0)
    rec0 = node.records().index(gap0)
    planes = []
    for _ in range(int(world["intervals"])):
        node.step()
        now = gap0.lines[0].now
        planes.append([[int(now[x_far, y, z]) for z in range(node.cube)] for y in range(node.cube)])
    births: dict = {}
    met: dict = {}
    for e in node.log:
        if e["event"] == "birth":
            at = tuple(e["node"])
            births[at] = births.get(at, 0) + 1
        if (e["event"] == "birth" and int(e["taken_row"]) == rec0) or (
            e["event"] == "refused" and e["cause"] in ("orientation", "twist", "lay") and int(e["row"]) == rec0
        ):
            at = tuple(e["node"])
            met[at] = met.get(at, 0) + 1
    counts = dict(node.counts)
    return planes, {"births": births, "met": met, "counts": counts}, {"state": node.state_hash()}


def predicted_rows(cube: int, length: int, y_a: int, y_b: int, lam_num: int, lam_den: int) -> dict:
    """The near field's rows at the far plane, integers only: for each row y the squared paths s1 = L^2 + (y - y_a)^2 and s2 = L^2 + (y - y_b)^2 (the torus distance), and whether the paths' difference is at or above half a wavelength: sqrt(s1) - sqrt(s2) >= lam / 2 with lam = lam_num / lam_den, by (4 lam_den^2 (s1 - s2) - lam_num^2)^2 >= 16 lam_den^2 lam_num^2 s2 where the left factor is at or above 0 (s1 >= s2 taken by the swap); the rows from the midline outward where the difference first reaches the half wavelength are the predicted minima."""

    def tdist(a: int, b: int) -> int:
        d = abs(a - b)
        return min(d, cube - d)

    rows = {}
    for y in range(cube):
        s1 = length * length + tdist(y, y_a) ** 2
        s2 = length * length + tdist(y, y_b) ** 2
        if s1 < s2:
            s1, s2 = s2, s1
        left = 4 * lam_den * lam_den * (s1 - s2) - lam_num * lam_num
        half_reached = left >= 0 and left * left >= 16 * lam_den * lam_den * lam_num * lam_num * s2
        # the whole wavelength: sqrt(s1) - sqrt(s2) >= lam
        left_whole = lam_den * lam_den * (s1 - s2) - lam_num * lam_num
        whole_reached = left_whole >= 0 and left_whole * left_whole >= 4 * lam_den * lam_den * lam_num * lam_num * s2
        rows[y] = {"s1": s1, "s2": s2, "half_reached": bool(half_reached), "whole_reached": bool(whole_reached)}
    return rows


def main() -> None:
    cube = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    intervals = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    quanta = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    sea = len(sys.argv) > 4 and sys.argv[4] == "sea"
    universe = json.loads(UNIVERSE.read_text())
    den = int(universe["integers"]["den"])
    h = wave_third(den)
    mid = quotient(cube, 2)
    x_s, length, d_half = 3, 5, 2
    x_far = x_s + length
    y_a, y_b = mid - d_half, mid + d_half
    a = (x_s, y_a, mid)
    b = (x_s, y_b, mid)
    worlds = {
        "empty": world_of(cube, intervals, [], h, quanta, sea),
        "A": world_of(cube, intervals, [a], h, quanta, sea),
        "B": world_of(cube, intervals, [b], h, quanta, sea),
        "AB": world_of(cube, intervals, [a, b], h, quanta, sea),
    }
    OUT.mkdir(exist_ok=True)
    for name, w in worlds.items():
        path = OUT / f"world_two_slits_{name}_{quanta}{'_sea' if sea else ''}.json"
        path.write_text(json.dumps(dict(w, universe="../../../../tests/worlds/universe_toy.json")))
    read_world(worlds["AB"], universe)
    # the prediction, written before the runs
    prediction = {
        "wave h (den sin(pi/3))": h,
        "wavelength (Links)": 3,
        "group velocity (Links per interval, num/den)": [1, 3],
        "sources": [a, b],
        "far plane x": x_far,
        "midline row": mid,
        "rows": predicted_rows(cube, length, y_a, y_b, 3, 1),
        "expected": "the interference term summed over z and the intervals is largest at the midline row and at or below 0 at the first rows where the paths differ by half a wavelength; the births' count per row for AB above A + B at the midline and at or below A + B at those rows; the superposition now_AB - now_A - now_B within a few levels per Node",
    }
    print(json.dumps({"prediction": prediction}, default=str))
    results = {}
    planes = {}
    for name, w in worlds.items():
        t0 = time.time()
        p, clicks, state = run_world(universe, w, x_far)
        planes[name] = p
        results[name] = {
            "seconds": int(time.time() - t0),
            "counts": clicks["counts"],
            "state": state["state"],
            "births_on_far_plane_by_row": [
                sum(v for k, v in clicks["births"].items() if k[0] == x_far and k[1] == y) for y in range(cube)
            ],
            "met_on_far_plane_by_row": [
                sum(v for k, v in clicks["met"].items() if k[0] == x_far and k[1] == y) for y in range(cube)
            ],
            "births_total": sum(clicks["births"].values()),
            "turns": clicks["counts"]["turns"],
            "births_by_x_plane": [sum(v for k, v in clicks["births"].items() if k[0] == x) for x in range(cube)],
            "gap-0 meetings by x plane": [sum(v for k, v in clicks["met"].items() if k[0] == x) for x in range(cube)],
            "met_total": sum(clicks["met"].values()),
        }
        print(json.dumps({name: {k: v for k, v in results[name].items() if k != "state"}}, default=str))
    # the superposition and the interference term on the far plane
    sup_max = 0
    sup_sum_abs = 0
    cells = 0
    inter_by_row = [0] * cube
    single_by_row = [0] * cube
    both_by_row = [0] * cube
    amp_max = 0
    for t in range(intervals):
        for y in range(cube):
            for z in range(cube):
                e0 = planes["empty"][t][y][z]
                na = planes["A"][t][y][z] - e0
                nb = planes["B"][t][y][z] - e0
                nab = planes["AB"][t][y][z] - e0
                dev = abs(nab - na - nb)
                sup_max = max(sup_max, dev)
                sup_sum_abs += dev
                cells += 1
                amp_max = max(amp_max, abs(na), abs(nb), abs(nab))
                inter_by_row[y] += nab * nab - na * na - nb * nb
                single_by_row[y] += na * na + nb * nb
                both_by_row[y] += nab * nab
    half_rows = [y for y in range(cube) if prediction["rows"][y]["half_reached"]]
    inner_half = sorted(half_rows, key=lambda y: min(abs(y - mid), cube - abs(y - mid)))[:2]
    verdict_board = (
        all(inter_by_row[mid] >= inter_by_row[y] for y in range(cube))
        and all(inter_by_row[y] <= 0 for y in inner_half)
    )
    ab = results["AB"]["births_on_far_plane_by_row"]
    sa = results["A"]["births_on_far_plane_by_row"]
    sb = results["B"]["births_on_far_plane_by_row"]
    verdict_clicks = ab[mid] > sa[mid] + sb[mid] and all(ab[y] <= sa[y] + sb[y] for y in inner_half)
    summary = {
        "superposition: max |now_AB - now_A - now_B| (levels)": sup_max,
        "superposition: mean deviation in thousandths of a level": quotient(1000 * sup_sum_abs, cells),
        "largest |level| on the far plane": amp_max,
        "interference term by row (sum over z and intervals of now_AB^2 - now_A^2 - now_B^2)": inter_by_row,
        "single sources' squares by row": single_by_row,
        "both sources' squares by row": both_by_row,
        "visibility per row in thousandths: (both - singles) / singles": [
            quotient(1000 * (both_by_row[y] - single_by_row[y]), single_by_row[y]) if single_by_row[y] else None
            for y in range(cube)
        ],
        "predicted first half-wavelength rows": inner_half,
        "board verdict (midline the largest, the half-wavelength rows at or below 0)": "SHOWN" if verdict_board else "NOT SHOWN",
        "clicks verdict (births AB above A + B at the midline, at or below at the half rows)": "SHOWN" if verdict_clicks else "NOT SHOWN",
    }
    print(json.dumps({"summary": summary}, default=str))
    (OUT / f"two_slits_qg1_{cube}_{intervals}_{quanta}{'_sea' if sea else ''}.json").write_text(
        json.dumps({"prediction": prediction, "results": results, "summary": summary}, default=str, indent=1)
    )


if __name__ == "__main__":
    main()
