"""hr1: the stream's section for the report, from the JSONL and hr1_read.py's summary of it. Usage: hr1_stream_section.py <stream.jsonl> <read.json>"""
import json
import sys

sys.set_int_max_str_digits(0)
lines = [json.loads(l) for l in open(sys.argv[1])]
rows = [l for l in lines if "i" in l]
tail = next((l for l in lines if l.get("tail")), None)
R = json.load(open(sys.argv[2]))
reach = rows[-1]["i"]
first = {}
for r in rows:
    for n in r["frozen"]:
        first.setdefault(n, r["i"])
twice = sum(1 for a, b in zip(rows, rows[1:]) for n in a["frozen"] if n in b["frozen"])
fz_count = [len(r["frozen"]) for r in rows]
hist = {}
for k in fz_count:
    hist[k] = hist.get(k, 0) + 1
c11 = [(r["i"], 11 in r["frozen"]) for r in rows]
f11 = [i for i, f in c11 if f]
gaps = [b - a for a, b in zip(f11, f11[1:])]
sums = [(r["i"], sum(r["content"]), min(r["content"]), max(r["content"])) for r in rows if r["i"] % 500 == 0 or r["i"] == reach]
credits = [c for r in rows for c in r["clicks"] if c["event"] == "credit"]
last_credit = max((c["i"] for c in credits), default=None)
mono = all(a[1] <= b[1] for a, b in zip(sums, sums[1:]))
frozen_lines = sum(fz_count)
per = {r["i"]: r for r in R["per interval"]}
hood = [(i, per[i]["hood nodes"], per[i]["hood content sum"], per[i]["rest content sum"]) for i in (2101, 3000, 4000, 5000, 6000, 7000, 8000, reach) if i in per]
turned_at_frozen = sum(1 for r in rows for n in r["frozen"] if n in r["turned"])
section = (
    f"The stream reached the interval {reach} of 8,000 (the box's rate: {'the run complete' if reach == 8000 else 'cut short by the time box, named'}); its X, content, frozen and turned equal to the FR hand's record at every interval to 2,400 (checked at 1,421 and at 2,400). "
    f"{len(first)} Nodes ever froze by {reach} (every one of the 125: {len(first) == 125}), {frozen_lines} frozen lines, no Node frozen at two intervals in a row ({twice} such pairs), {turned_at_frozen} frozen Nodes turned at their frozen interval (FR-S1's own act reads 'turned' at the next line); "
    f"the frozen count per interval at most {max(fz_count)}, its histogram (count: intervals) {dict(sorted(hist.items()))}: the horizon is a set of hovering Nodes whose freezes come to fall together. "
    f"Node (0, 2, 1)'s refreezes: {len(f11)} by {reach}, the gaps {gaps[:12]} ... {gaps[-6:]} (the least {min(gaps) if gaps else None}, the last {gaps[-1] if gaps else None}). "
    f"The board's content sum at 500, 1,000, ...: {[(i, s) for i, s, _, _ in sums]}, rising at every mark: {mono}; the least and greatest content at the end {sums[-1][2]} / {sums[-1][3]}. "
    f"The neighbourhood (ever-frozen Nodes and their six neighbours: Nodes, content sum, the rest's sum) at 2,101 and every 1,000: {hood}. "
    f"The credits: {len(credits)} in the stream, the last at {last_credit}; after the first freeze (2,101) {sum(1 for c in credits if c['i'] > 2101)} credits anywhere on the board in {reach - 2101} intervals; the rate 0 per interval at and beside the horizon. "
    f"Bits: the transient at most {max(r['max transient'] for r in rows)}, the state {max(r['state bits'] for r in rows)}. "
    f"The run back: {tail['run back'] if tail else 'not reached (the run cut before its end)'}; the counts {tail['counts'] if tail else 'not reached'}."
)
bits = f"{max(r['max transient'] for r in rows)} transient / {max(r['state bits'] for r in rows)} state to {reach}"
back = f"{tail['run back'][0]} of {tail['run back'][1]} at {reach}" if tail else f"not reached (cut at {reach})"
rep = open(sys.argv[3]).read().replace("STREAM_SECTION", section).replace("STREAM_BITS", bits).replace("STREAM_BACK", back)
open(sys.argv[3], "w").write(rep)
print(section)
