"""tw3's table: every summary under out/<tag>.out with its gates' table out/<tag>.gates.json laid as record x weight x gate
(the SHOWN set with its count, the gates gained and lost against the weight 54 of the same record, the named gates' numbers:
4 the era of matter, 45 the bodies' binding, 8 the families, 26 the lifts, 22 Coulomb's sign, 14 and 34 the horizon, 1 and 46 the
exact returns, the births, credits, laid back, turns, the run back, the integers and the bits); the clicks' 48 from out/clicks48_*.json.
Usage: tabulate_tw3.py  (prints Markdown)."""

import glob
import json
import os
import re
import sys

sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__))
NAMED = {1: "1 recurring bangs", 4: "4 an era of matter", 8: "8 families forming (whole view)", 14: "14 the horizon", 22: "22 Coulomb's sign",
         26: "26 the three lifts born and their beats' ratios", 34: "34 the horizon and the stopped clock", 45: "45 the bodies' well, binding and collapse",
         46: "46 the bangs recurring with the same gates"}
NAMES = {int(k): v for k, v in json.load(open(os.path.join(HERE, "out", "gate_names.json"))).items()}
runs = {}
for path in sorted(glob.glob(os.path.join(HERE, "out", "world_*.out"))):
    text = open(path).read().strip().splitlines()
    line = next((ln for ln in reversed(text) if ln.startswith("{")), None)
    tag = os.path.basename(path)[:-4]
    if line is None:
        runs[tag] = {"tag": tag, "failed": text[-3:] if text else ["(empty: cut short or running)"]}
        continue
    s = json.loads(line)
    gpath = os.path.join(HERE, "out", tag + ".gates.json")
    s["gates"] = json.load(open(gpath)) if os.path.exists(gpath) else {}
    runs[tag] = s

def rec_of(tag: str) -> tuple[str, str]:
    m = re.match(r"(world_\w+?_\d+)_K(\d+)(_revA48)?$", tag)
    return (m.group(1) + (m.group(3) or ""), m.group(2)) if m else (tag, "?")

by_record: dict[str, dict[str, dict]] = {}
for tag, s in runs.items():
    rec, w = rec_of(tag)
    by_record.setdefault(rec, {})[w] = s

print("## The table: record x weight x gate (every run on the flagged copy src_tw3, back 10, nice 19; the command of each run is the queue's line in queue_tw3.sh)\n")
print("| record | K | SHOWN count | SHOWN set | gained vs 54 | lost vs 54 | births | credits | laid back | turns | run back | integers | bits | seconds |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for rec in sorted(by_record):
    base = by_record[rec].get("54", {}).get("gates SHOWN")
    for w in sorted(by_record[rec], key=lambda x: -int(x) if x.isdigit() else 0):
        s = by_record[rec][w]
        if "failed" in s:
            print(f"| {rec} | {w} | not finished | {' / '.join(s['failed'])[:120]} | | | | | | | | | | |")
            continue
        shown = s["gates SHOWN"]
        gained = [NAMES[n] for n in sorted(set(shown) - set(base))] if base is not None else "-"
        lost = [NAMES[n] for n in sorted(set(base) - set(shown))] if base is not None else "-"
        rb = s["run back"]
        print(f"| {rec} | {w} | {len(shown)} | {shown} | {gained} | {lost} | {s['births']} | {s['credits']} | {s['laid back']} | {s['turns']} | {rb['exact']} of {rb['intervals']} | {s['integers']} | {s['max bits']} | {s['seconds']} |")

print("\n## The named gates, every number from the engine's reader (event_universe.gates on the record)\n")
for rec in sorted(by_record):
    for w in sorted(by_record[rec], key=lambda x: -int(x) if x.isdigit() else 0):
        s = by_record[rec][w]
        if "failed" in s:
            continue
        g = s["gates"]
        print(f"### {rec} at K {w} (hash {s['hash']}, returns {s['returns'][:6]} count {s['returns count']}, W total {s['W total at the end']})")
        for n, key in NAMED.items():
            v = g.get(key, {})
            nums = {k: val for k, val in v.items() if k != "verdict"}
            print(f"- gate {n}: {v.get('verdict', 'absent')}; " + json.dumps(nums, default=str)[:400])
        kinds = s["kinds"]
        print("- kinds: " + ", ".join(f"{n} {k}" for n, k in kinds.items()))
        print()

print("## The clicks' 48 on the hole 60 (clicks_48_tw3.py, ag1's script unchanged, 49 runs each)\n")
for path in sorted(glob.glob(os.path.join(HERE, "out", "clicks48_*.json"))):
    c = json.load(open(path))
    print(f"- {os.path.basename(path)}: births {c['births']}, credits {c['credits']}, clicks through the image {json.dumps(c['clicks through the image'])}, end state equal of {json.dumps(c['end state (X, gap-0 re) equal through the image, of'])}, apart (first) {json.dumps(c['apart (first three)'][:1], default=str)[:300]}, {c['seconds']} s")
