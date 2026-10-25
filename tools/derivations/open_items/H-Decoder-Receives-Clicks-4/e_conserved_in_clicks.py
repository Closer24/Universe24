"""(e, Addition 5) What the lattice conserves, read in the credit and birth lines alone (hole_N.lines.jsonl): the charge, the senses summed over each birth and over all births; the count, taken against walls on every birth and body credit (excess = taken - walls below step, integer) and the credits per close against the births' children; windows derivable from the record (each credit's `windows` against the running count of the Node's own credits and births in the output); the energy as the beat per proper interval before and after a body's click (the same body's `beat` on consecutive credits); the momentum, the credits' running cosine per axis and the sum of the sign terms over each close; the 48, the credits' multiset under each cube element about the origin (support and momentum mapped) against itself. Integer readings only.
Command: cd <worktree> && PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Decoder-Receives-Clicks-4/e_conserved_in_clicks.py 120"""

from __future__ import annotations

import json
import sys
from itertools import permutations, product

from d4lib import HERE, dump

N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
L = 3
lines = [json.loads(x) for x in (HERE / f"hole_{N}.lines.jsonl").read_text(encoding="utf-8").splitlines()]
credits = [l for l in lines if l["event"] == "credit"]
births = [l for l in lines if l["event"] == "birth"]
# charge: the senses' sum per birth and over all
per_birth = [sum(b["senses"]) for b in births]
charge = {"births": len(births), "births_with_senses_summing_to_0": sum(1 for s in per_birth if s == 0), "total_sense_sum": sum(per_birth)}
# the credits' senses per close (the body credits' Wronskian signs at the Node): sums per interval
sense_per_close = {}
for c in credits:
    if c.get("taken") is not None:
        sense_per_close[c["interval"]] = sense_per_close.get(c["interval"], 0) + c["sense"]
charge["body_credit_sense_sum_per_close"] = sense_per_close
# count: the exact take on every line carrying it
take_lines = [l for l in lines if l.get("taken") is not None]
count = {
    "lines_with_a_take": len(take_lines),
    "taken_at_or_above_walls": sum(1 for l in take_lines if l["taken"] >= l["walls"]),
    "excess_equals_taken_minus_walls": sum(1 for l in take_lines if l["excess"] == l["taken"] - l["walls"]),
    "excess_below_step": sum(1 for l in take_lines if l["excess"] < l["step"]),
    "credits_count_1": sum(1 for c in credits if c["count"] == 1),
    "birth_children_total": sum(len(b["children"]) for b in births),
    "light_credits_total": sum(1 for c in credits if c.get("taken") is None),
}
# windows derivable from the record: the running count of a Node's own credits and births written so far, against the credit's `windows`
running: dict[str, int] = {}
derivable = 0
checked = 0
by_close: dict[int, list] = {}
for l in lines:
    if l["event"] in ("credit", "birth"):
        by_close.setdefault(l["interval"], []).append(l)
for t in sorted(by_close):
    per_node_this_close: dict[str, int] = {}
    for l in by_close[t]:
        if l["event"] == "birth":
            for n in l["nodes"]:
                per_node_this_close[json.dumps(n)] = per_node_this_close.get(json.dumps(n), 0) + 1
    body_counts: dict[str, int] = {}
    for l in by_close[t]:
        if l["event"] == "credit" and l.get("taken") is not None:
            body_counts[json.dumps(l["support"])] = body_counts.get(json.dumps(l["support"]), 0) + 1
    for l in by_close[t]:
        if l["event"] == "credit":
            key = json.dumps(l["support"])
            checked += 1
            # the engine counts the births' closes first, then each body credit one by one in the x-major, family, record order
            if l.get("taken") is None:
                expected = running.get(key, 0) + per_node_this_close.get(key, 0)
            else:
                expected = None
            if expected is not None and expected == l["windows"]:
                derivable += 1
    # update running counts after the close
    for key, n in per_node_this_close.items():
        running[key] = running.get(key, 0) + n
    for key, n in body_counts.items():
        running[key] = running.get(key, 0) + n
# body credits: windows against the running count including the body's own increments in order
running2: dict[str, int] = {}
body_checked = body_ok = 0
for t in sorted(by_close):
    for l in by_close[t]:
        if l["event"] == "birth":
            for n in l["nodes"]:
                running2[json.dumps(n)] = running2.get(json.dumps(n), 0) + 1
    for l in sorted((x for x in by_close[t] if x["event"] == "credit" and x.get("taken") is not None), key=lambda x: (x["support"], x["identity"])):
        key = json.dumps(l["support"])
        running2[key] = running2.get(key, 0) + 1
        body_checked += 1
        body_ok += int(running2[key] == l["windows"])
windows = {"light_credits_checked": checked - body_checked, "light_credits_windows_derivable": derivable, "body_credits_checked": body_checked, "body_credits_windows_derivable": body_ok}
# energy: the beat per proper interval before and after a body's click, the same body at the same Node
bodies: dict[str, list] = {}
for c in credits:
    if c.get("taken") is not None:
        bodies.setdefault(json.dumps([c["identity"], c["support"]]), []).append(c)
pairs = same_beat = same_point = 0
beat_over_spacing = []
for key, cs in bodies.items():
    cs.sort(key=lambda c: (c["proper"], c["windows"]))
    for a, b in zip(cs, cs[1:], strict=False):
        pairs += 1
        same_beat += int(a["beat"] == b["beat"])
        same_point += int(a["point"] == b["point"])
        dp = b["proper"] - a["proper"]
        if isinstance(b["beat"], int) and dp > 0:
            beat_over_spacing.append([b["beat"] // dp, b["beat"] % dp, dp])
energy = {"consecutive_body_credit_pairs": pairs, "same_beat_after_as_before": same_beat, "same_point_after_as_before": same_point, "beat_div_proper_spacing_[q, r, dp]_first_8": beat_over_spacing[:8]}
# momentum: the running cosine per axis; the sign terms summed per close (the directions cancel on a symmetric close)
mom = {"credits_with_momentum": 0, "credits_momentum_None": 0, "axis_pairs_within_circle_|num|<=den": 0, "axis_pairs_outside": 0, "sign_sum_per_close": {}}
for c in credits:
    m = c["momentum"]
    if m is None:
        mom["credits_momentum_None"] += 1
        continue
    mom["credits_with_momentum"] += 1
    for axis in m:
        if axis is None or not all(isinstance(v, int) for v in axis):
            continue
        s, num, den = axis
        mom["sign_sum_per_close"][c["interval"]] = mom["sign_sum_per_close"].get(c["interval"], 0) + s
        if abs(num) <= den:
            mom["axis_pairs_within_circle_|num|<=den"] += 1
        else:
            mom["axis_pairs_outside"] += 1
# the 48: image of a credit under (perm, signs) about the origin on the torus
def image_node(n, perm, signs):
    return [(signs[i] * n[perm[i]]) % L for i in range(3)]
def image_momentum(m, perm, signs):
    if m is None:
        return None
    out = []
    for i in range(3):
        axis = m[perm[i]]
        if axis is None or not isinstance(axis[0], int):
            out.append(axis)
        else:  # [sign_a, num_a, den_a], or [sign_a, [pair], [pair]] on a record of two lines
            out.append([signs[i] * axis[0], *axis[1:]])
    return out
def signature(c, perm, signs, with_sense):
    return json.dumps([c["interval"], c["identity"][0], c["point"], c["kind"], c["sense"] if with_sense else 0, c["beat"], c["proper"], c["windows"], image_node(c["support"], perm, signs), image_momentum(c["momentum"], perm, signs)], sort_keys=True)
def multiset(perm, signs, with_sense):
    found = {}
    for c in credits:
        s = signature(c, perm, signs, with_sense)
        found[s] = found.get(s, 0) + 1
    return found
base = multiset((0, 1, 2), (1, 1, 1), True)
base_ns = multiset((0, 1, 2), (1, 1, 1), False)
elements = [(p, s) for p in permutations(range(3)) for s in product((1, -1), repeat=3)]
invariant = sum(1 for p, s in elements if multiset(p, s, True) == base)
invariant_ns = sum(1 for p, s in elements if multiset(p, s, False) == base_ns)
# the births' images too
def birth_sig(b, perm, signs):
    return json.dumps([b["interval"], sorted(b["senses"]), sorted(b["children"]), [image_node(n, perm, signs) for n in b["nodes"]], b["taken"], b["walls"], b["excess"], b["step"]], sort_keys=True)
def birth_multiset(perm, signs):
    found = {}
    for b in births:
        s = birth_sig(b, perm, signs)
        found[s] = found.get(s, 0) + 1
    return found
bbase = birth_multiset((0, 1, 2), (1, 1, 1))
binv = sum(1 for p, s in elements if birth_multiset(p, s) == bbase)
result = {
    "intervals": N,
    "charge": charge,
    "count": count,
    "windows_derivable_from_the_record": windows,
    "energy": energy,
    "momentum": mom,
    "the_48": {"elements": len(elements), "credit_multiset_invariant_with_sense": invariant, "credit_multiset_invariant_sense_dropped": invariant_ns, "birth_multiset_invariant": binv},
}
dump(HERE / f"e_conserved_in_clicks_{N}.json", result)
print(json.dumps(result, indent=1)[:6000])
