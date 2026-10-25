"""ma2's reader of a record written by ma_run.py: the X course (the tops with the count of Nodes turning, the exact returns to Gamma at every Node), the first interval where the board is not uniform, the spread's course, the turns that were not the whole board's, the charge, the light's current pattern, the births and the refusals, the mergers' premises summed, the 48 about the Node (0, 0, 0) on X and on the light's current (from the node lines), the run back, the bits. Integers only.

Usage: python read_diag.py <out.json> [marks i1 i2 ...]"""

from __future__ import annotations

import json
import sys
from itertools import permutations, product
from typing import Any

import numpy as np


def cube48() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """The 48 signed permutations of the three axes."""
    found = []
    for perm in permutations(range(3)):
        for signs in product((1, -1), repeat=3):
            found.append((perm, signs))
    return found


def image(a: Any, perm: tuple[int, ...], signs: tuple[int, ...]) -> Any:
    """A board array's image under a signed permutation about the Node (0, 0, 0), x_a -> signs_a x_perm(a)."""
    b = np.transpose(a, perm)
    for axis in range(3):
        if signs[axis] == -1:
            n = b.shape[axis]
            idx = [(-k) % n for k in range(n)]
            b = np.take(b, idx, axis=axis)
    return b


def forty_eight(x: Any) -> int:
    """The count of the 48 under which the scalar board array is invariant."""
    return sum(1 for perm, signs in cube48() if (image(x, perm, signs) == x).all())


def forty_eight_vector(cur: list[Any]) -> int:
    """The count of the 48 under which the Links' current (a vector along each axis, read from the Node toward +a) is invariant: the image of the component along axis a is signs_a times the component along perm(a), read from the image Node and, where the sign is -1, from the Node one Link back along the axis with the sign reversed (the current is odd under the exchange of the ends)."""
    kept = 0
    for perm, signs in cube48():
        ok = True
        for axis in range(3):
            src = cur[perm[axis]]
            img = image(src, perm, signs)
            if signs[axis] == -1:
                n = img.shape[axis]
                idx = [(k - 1) % n for k in range(n)]
                img = -np.take(img, idx, axis=axis)
            if not (img == cur[axis]).all():
                ok = False
                break
        kept += ok
    return kept


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    with open(argv[1], encoding="utf-8") as f:
        d = json.load(f)
    gamma = int(d["gamma"])
    shape = tuple(int(x) for x in d["world"]["shape"])
    n_nodes = shape[0] ** 3
    diag = d["diag"]
    nodes = d["nodes"]
    print("record", argv[1], "shape", shape, "intervals", d["intervals"], "lays_fourth", d.get("lays_fourth"))
    for e in d["log"]:
        if e["event"] == "lay_fourth":
            print("lay", e)
    print("counts", d["counts"], "run back", d["run_back"])
    print("bits max", max(e["bits"] for e in diag), "integers", d["rows"][-1]["integers"], "transient", d["rows"][-1]["max transient bits"])
    # the X course
    means = [e["X_mean"] for e in diag]
    tops = []
    for k in range(1, len(means) - 1):
        if means[k - 1] <= means[k] >= means[k + 1] and (means[k - 1] < means[k] or means[k] > means[k + 1]):
            tops.append((diag[k]["i"], means[k], diag[k]["turned"], diag[k + 1]["turned"]))
    print("tops of the mean (i, mean, turned at i, turned at i+1), first 12:", tops[:12])
    returns = [(e["i"], e["X_mean"]) for e in diag if e["X_min"] == gamma and e["X_max"] == gamma and e["i"] > 20]
    print("exact returns (every Node at Gamma, i > 20):", returns[:12], "count", len(returns))
    bottoms = []
    for k in range(1, len(means) - 1):
        if means[k - 1] >= means[k] <= means[k + 1] and (means[k - 1] > means[k] or means[k] < means[k + 1]):
            bottoms.append((diag[k]["i"], means[k], diag[k]["X_min"], diag[k]["X_max"]))
    print("bottoms of the mean (i, mean, min, max), first 8:", bottoms[:8])
    first_split = next((e["i"] for e in diag if e["X_min"] != e["X_max"]), None)
    print("first interval with X not uniform:", first_split)
    marks = [int(x) for x in argv[argv.index("marks") + 1 :]] if "marks" in argv else [5, 10, 20, 40, 60, 100, 150, 200, 300, 400]
    for i in marks:
        if i <= len(diag):
            e = diag[i - 1]
            print(
                f"i {i}: X mean {e['X_mean']} min {e['X_min']} max {e['X_max']} even {e['X_even_mean']} odd {e['X_odd_mean']} e {e['e_max']} "
                f"W even {e['W_even']} odd {e['W_odd']} total {e['W_total']} Wodd-fail {e['W_odd_under_translation_fail']} "
                f"F max {e['F_abs_max']} zero/even/odd {e['F_links_zero']}/{e['F_links_from_even']}/{e['F_links_from_odd']} twist!=0 {e['twist_links_nonzero']} "
                f"light share {e['light_share_min_max_hundredths']} births {e['births']} ref o/t/l/s {e['refused_orientation']}/{e['refused_twist']}/{e['refused_lay']}/{e['refused_stop']}"
            )
            for rec, m in e["mergers"].items():
                print("   mergers rec", rec, m)
    turns_partial = [(e["i"], e["turned"]) for e in diag if 0 < e["turned"] < n_nodes]
    turns_whole = [e["i"] for e in diag if e["turned"] == n_nodes]
    print("turns of the whole board at:", turns_whole[:12], "count", len(turns_whole))
    print("partial turns (i, Nodes), first 12:", turns_partial[:12], "count", len(turns_partial), "sum", sum(t for _i, t in turns_partial))
    print("W_total nonzero intervals:", sum(1 for e in diag if e["W_total"] != 0), "of", len(diag), "; W odd under translation fails at intervals:", sum(1 for e in diag if e["W_odd_under_translation_fail"]))
    print("F pattern: intervals with every Link from even:", sum(1 for e in diag if e["F_links_from_even"] == 3 * n_nodes), "from odd:", sum(1 for e in diag if e["F_links_from_odd"] == 3 * n_nodes), "all zero:", sum(1 for e in diag if e["F_links_zero"] == 3 * n_nodes), "mixed:", sum(1 for e in diag if 0 < e["F_links_from_even"] < 3 * n_nodes))
    print("twist nonzero Links summed over intervals:", sum(e["twist_links_nonzero"] for e in diag))
    # the mergers summed
    for rec in diag[-1]["mergers"]:
        keys = ["met", "opposite", "orientation_0", "twist_0", "lay_former", "lay_s3", "stop_checked", "stop_one_2u0", "stop_each_u0_ends"]
        sums = {k: sum(e["mergers"][rec][k] for e in diag) for k in keys}
        print("mergers rec", rec, "summed over intervals:", sums)
        print("   share of the record (hundredths) at 1 / 100 / 400:", diag[0]["mergers"][rec]["share_min_max_hundredths"], diag[min(99, len(diag) - 1)]["mergers"][rec]["share_min_max_hundredths"], diag[-1]["mergers"][rec]["share_min_max_hundredths"])
    # the 48 about the Node (0, 0, 0) on X and on the light's current
    for i in [1, 10, 50, 100, 200, 400]:
        if i <= len(nodes):
            line = nodes[i - 1]
            x = np.array(line["X"], dtype=object).reshape(shape)
            cur = [np.array(c, dtype=object).reshape(shape) for c in line["current"]]
            print(f"the 48 about (0,0,0) at i {i}: X {forty_eight(x)} of 48; the light's current {forty_eight_vector(cur)} of 48; turned {len(line['turned'])}")


if __name__ == "__main__":
    main(sys.argv)
