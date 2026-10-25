"""Hand D3: what the lattice conserves, read in the clicks from the credit and birth lines alone (THE_WAY.md, step 4; BRIEF_COMMON, Addition 5). Integers only.

The charge: the senses' sum on every birth line (0 at every birth) and the senses' sum over every credit. The momentum: the credits' running cosine per axis, [sign_a, num_a, den_a], how many credits read it, how many pairs lie within the circle (|num| <= den), and the signs' sum per axis (0 on a seed the 48 keeps). The energy: the beat on every credit (W_rec of the point read, 3 T den sin omega), light's at the births against the children's walls summed on the birth line (two quanta's beat against what the birth books, as integers), and a body's beat before and after its clicks along its own track. The count: on every line with a take, taken equals walls plus excess, and the excess below the last level's step; per close the credit lines against the walls (the unit per credit, one integer). The symmetry: the credit lines' multiset under each of the cube's 48 about the origin (the signed permutations on the torus), and the birth lines' likewise.

Usage: python tools/derivations/d3/d3_conserved_in_clicks.py --log <clicks.jsonl> --shape 3 3 3 --name course [--out tools/derivations/d3/out]
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve()


def elements():
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            yield permutation, signs


def carried_node(node, permutation, signs, shape):
    return tuple(int((signs[k] * node[permutation[k]]) % shape[k]) for k in range(3))


def carried_momentum(momentum, permutation, signs):
    if momentum is None:
        return None
    found = []
    for k in range(3):
        entry = momentum[permutation[k]]
        found.append(None if entry is None else [entry[0] * signs[k], entry[1], entry[2]])
    return found


def credit_key(line, permutation, signs, shape):
    support = carried_node(tuple(line["support"]), permutation, signs, shape)
    return (line["interval"], support, tuple(line["identity"]), json.dumps(line["point"]), line["kind"], line["sense"], line["beat"], line["proper"], line["windows"], json.dumps(carried_momentum(line["momentum"], permutation, signs)))


def birth_key(line, permutation, signs, shape):
    nodes = tuple(carried_node(tuple(n), permutation, signs, shape) for n in line["nodes"])
    return (line["interval"], nodes, tuple(line["children"]), tuple(line["senses"]), json.dumps(line.get("records")), json.dumps(line.get("points")), line.get("taken"), line.get("walls"), line.get("excess"), line.get("step"))


def invariant_count(lines, key, shape):
    plain = sorted(key(x, (0, 1, 2), (1, 1, 1), shape) for x in lines)
    return sum(1 for p, s in elements() if sorted(key(x, p, s, shape) for x in lines) == plain)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--shape", type=int, nargs=3, required=True)
    parser.add_argument("--name", default="course")
    parser.add_argument("--out", type=Path, default=HERE.parent / "out")
    args = parser.parse_args()
    shape = tuple(args.shape)
    lines = [json.loads(x) for x in args.log.read_text(encoding="utf-8").splitlines() if x.strip()]
    credits = [x for x in lines if x.get("event") == "credit"]
    births = [x for x in lines if x.get("event") == "birth"]
    born_at = {(x["interval"], tuple(n)) for x in births for n in x["nodes"]}
    light_credits = [x for x in credits if (x["interval"], tuple(x["support"])) in born_at]
    body_credits = [x for x in credits if (x["interval"], tuple(x["support"])) not in born_at]
    # the charge
    birth_sums = [sum(x["senses"]) for x in births]
    charge = {"births": len(births), "births_senses_sum_zero": birth_sums.count(0), "credits_senses_sum": sum(x["sense"] for x in credits), "body_credits_senses_sum": sum(x["sense"] for x in body_credits), "body_credits_sense_counts": dict(Counter(x["sense"] for x in body_credits))}
    # the momentum
    momentum = {}
    for axis in range(3):
        read = [x["momentum"][axis] for x in credits if x.get("momentum") is not None and x["momentum"][axis] is not None]
        single = [m for m in read if isinstance(m[1], int)]
        inside = [m for m in single if abs(m[1]) <= m[2]]
        momentum[f"axis_{axis}"] = {"credits_read": len(read), "one_pair": len(single), "pair_of_pairs_two_lines_differ": len(read) - len(single), "pairs_within_the_circle": len(inside), "signs_sum": sum(m[0] for m in read), "signs_counts": dict(Counter(m[0] for m in read))}
    momentum["credits_with_no_momentum"] = sum(1 for x in credits if x.get("momentum") is None)
    momentum["credits"] = len(credits)
    # the energy
    light_beats = [x["beat"] for x in light_credits]
    births_by = {(x["interval"], tuple(n)): x for x in births for n in x["nodes"]}
    against_walls = []
    for x in light_credits:
        b = births_by[(x["interval"], tuple(x["support"]))]
        if x["beat"] and b.get("walls") is not None:
            against_walls.append({"two_quanta_beat": 2 * x["beat"], "children_walls": b["walls"], "walls_over_two_beats_thousandths": [(1000 * b["walls"]) // (2 * x["beat"]), (1000 * b["walls"]) % (2 * x["beat"])]})
    tracks: dict[tuple, list] = {}
    for x in body_credits:
        tracks.setdefault((tuple(x["support"]), tuple(x["identity"])), []).append(x)
    before_after = []
    for key, found in sorted(tracks.items()):
        found.sort(key=lambda x: x["windows"])
        before_after.append({"place": list(key[0]), "body": list(key[1]), "beats_along_the_track": [x["beat"] for x in found], "proper_along_the_track": [x["proper"] for x in found]})
    energy = {"light_credits": len(light_credits), "light_beat_read": sum(1 for b in light_beats if b), "light_beat_none_or_zero": sum(1 for b in light_beats if not b), "light_beat_values": sorted(set(b for b in light_beats if b))[:8], "light_two_quanta_beat_against_children_walls_first_four": against_walls[:4], "body_credits": len(body_credits), "body_beat_none": sum(1 for x in body_credits if x["beat"] is None), "body_beat_zero": sum(1 for x in body_credits if x["beat"] == 0), "body_beat_read": sum(1 for x in body_credits if x["beat"]), "body_tracks_beat_before_after_first_four": before_after[:4], "body_point_pair_of_pairs": sum(1 for x in body_credits if isinstance(x["point"], list) and x["point"] and isinstance(x["point"][0], list))}
    # the count
    takes = [x for x in credits + births if x.get("taken") is not None]
    closes: dict[tuple, list] = {}
    for x in credits:
        closes.setdefault((x["interval"], tuple(x["support"])), []).append(x)
    units = Counter()
    unit_remainders = 0
    for (t, at), found in closes.items():
        walls = found[0].get("walls")
        if walls is None:
            continue
        n = sum(x["count"] for x in found)
        units[(found[0]["identity"][0] if (t, at) not in born_at else "birth", walls // n)] += 1
        unit_remainders += walls % n != 0
    count = {"lines_with_a_take": len(takes), "taken_equals_walls_plus_excess": sum(1 for x in takes if x["taken"] == x["walls"] + x["excess"]), "excess_below_the_step": sum(1 for x in takes if 0 <= x["excess"] < x["step"]), "excess_zero": sum(1 for x in takes if x["excess"] == 0), "credit_count_one_on_every_line": sum(1 for x in credits if x["count"] == 1), "closes": len(closes), "walls_per_credit_by_row_distinct": {str(k): v for k, v in sorted(units.items(), key=str)}, "walls_not_a_multiple_of_the_credits": unit_remainders}
    # the symmetry
    symmetry = {"credit_lines_invariant_under": invariant_count(credits, credit_key, shape), "birth_lines_invariant_under": invariant_count(births, birth_key, shape), "of": 48}
    found = {"log": str(args.log), "shape": list(shape), "credits": len(credits), "births": len(births), "charge": charge, "momentum": momentum, "energy": energy, "count": count, "symmetry_48": symmetry}
    (args.out / f"conserved_in_clicks_{args.name}.json").write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
