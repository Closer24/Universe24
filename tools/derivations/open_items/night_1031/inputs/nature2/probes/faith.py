"""NATURE2's faithfulness probe: writer E's guard (decoder/sides.paired, in records.read) and books (shadow.books) on
node-all 9d75a4904, on a record and on forged copies of it. A forged copy is written beside the probe, read by
records.read (the guard), and read again with every guard but the sides' guard, so the books' own verdict on it is
seen. Whole numbers only; no division; paths by joinpath.

Usage: python3 -I faith.py <tree> <record .jsonl> <label> <out folder>
"""

import copy
import json
import sys
from pathlib import Path

TREE = Path(sys.argv[1])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

from tensor24.decoder import records, shadow, sides  # noqa: E402

RECORD = Path(sys.argv[2])
LABEL = sys.argv[3]
OUT = Path(sys.argv[4])
UNGUARDED = tuple(g for g in records.GUARDS if g is not sides.paired)


def rows():
    return [json.loads(t) for t in RECORD.read_text(encoding="utf-8").splitlines() if t.strip()]


def write(name, lines):
    path = OUT.joinpath(f"{LABEL}_{name}.jsonl")
    path.write_text("".join(json.dumps(e) + "\n" for e in lines), encoding="utf-8")
    return path


def read_both(path):
    held, cause = records.read(str(path))
    guarded = "admitted" if held is not None else f"refused: {cause[:150]}"
    loose, why = records.read(str(path), UNGUARDED)
    if loose is None:
        return guarded, f"not read without the guard either: {why[:120]}"
    verdict = shadow.books(loose)
    return guarded, f"{verdict['kind']}: {verdict['cause'][:170]}"


def middle(items):
    """The item at the middle of a list, found by counting, with no division."""
    n, k = len(items), 0
    while 2 * k < n:
        k += 1
    return items[k - 1] if items else None


def main():
    base = rows()
    print(f"== {LABEL}: {len(base)} lines")
    held, cause = records.read(str(RECORD))
    print(f"the record: {'admitted by the guard' if held is not None else 'refused: ' + cause}")
    if held is not None:
        v = shadow.books(held)
        print(f"E's books: {v['kind']}: {v['cause'][:220]}")
    clicks = [n for n, e in enumerate(base) if e.get("kind") == "click"]
    if not clicks:
        print("no click line: no forgery read")
        return
    forged = {}
    # f1: one line's q +1, its sides unchanged
    f = copy.deepcopy(base)
    n = middle(clicks)
    f[n]["q"] += 1
    forged["f1_line_q_plus1"] = f
    # f5: an in-site side +1, its line's q moved with it
    with_side = [n for n in clicks if any(s[1] != 0 for s in base[n].get("sides", []))]
    if with_side:
        f = copy.deepcopy(base)
        n = middle(with_side)
        k = [i for i, s in enumerate(f[n]["sides"]) if s[1] != 0][0]
        f[n]["sides"][k][1] += 1
        f[n]["q"] += 1
        forged["f5_insite_side_plus1_line_moved"] = f
        # f6: an in-site side dropped from one end, its line's q moved
        f = copy.deepcopy(base)
        dropped = f[n]["sides"].pop(k)
        f[n]["q"] -= dropped[1]
        forged["f6_insite_side_dropped_line_moved"] = f
    with_across = [n for n in clicks if base[n].get("across")]
    if with_across:
        # f2: an across side +1, its line's q moved
        f = copy.deepcopy(base)
        n = middle(with_across)
        f[n]["across"][0][2] += 1
        f[n]["q"] += 1
        forged["f2_across_side_plus1_line_moved"] = f
        # f4: an across side dropped from one end, its line's q moved
        f = copy.deepcopy(base)
        dropped = f[n]["across"].pop(0)
        f[n]["q"] -= dropped[2]
        forged["f4_across_side_dropped_line_moved"] = f
        # f3, the swap: at one place, one across side of one train's line exchanged with one of another train's line,
        # each line's q moved so each line is still its sides' sum: every quantum booked at the right place, at the
        # wrong clock
        at = {}
        for n2 in with_across:
            at.setdefault((base[n2]["round"], base[n2]["site"]), []).append(n2)
        two = [v for v in at.values() if len(v) >= 2]
        if two:
            a, b = middle(two)[0], middle(two)[1]
            f = copy.deepcopy(base)
            sa, sb = f[a]["across"][0], f[b]["across"][0]
            f[a]["across"][0], f[b]["across"][0] = sb, sa
            f[a]["q"] += sb[2] - sa[2]
            f[b]["q"] += sa[2] - sb[2]
            forged["f3_swap_across_between_two_clocks"] = f
    for name, lines in forged.items():
        guard, book = read_both(write(name, lines))
        print(f"{name}: the guard {guard}; the books without the guard: {book}")


main()
