"""rl1: one table from out/ (integers only): the records against the cache (the substance keys counts, log, nodes; the cache's rows differ in milliseconds and its run back ran 20), the 48 on the clicks, the torque's terms per form, the J balance per form, the horizon probe."""
import json
import os
import sys

sys.set_int_max_str_digits(0)
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "out")


def last_json(path):
    try:
        lines = [x for x in open(path).read().strip().splitlines() if x.startswith("{")]
        return json.loads(lines[-1]) if lines else None
    except FileNotFoundError:
        return None


print("## records against the cache 2ab32b518 (substance: counts, log, nodes equal)")
for name in sorted(os.listdir(out)):
    if not name.endswith(".stdout") or not any(name.startswith(p) for p in ("hole60", "chiral60", "universe400", "pair3", "plasma3", "ga2")):
        continue
    d = last_json(os.path.join(out, name))
    if not d or "counts" not in d:
        print(name, "no record (cut short or failed)")
        continue
    eq = d.get("against_cached", {}).get("keys_equal", {})
    sub = all(eq.get(k, False) for k in ("counts", "log", "nodes"))
    c = d["counts"]
    try:
        r = json.load(open(os.path.join(out, name.replace(".stdout", ".json"))))
        bits = max(int(x.get("max transient bits", 0)) for x in r["rows"])
        back = r.get("run_back")
    except Exception:
        bits, back = None, None
    fa = d.get("first_apart_log_entry")
    print(name[:-7], "substance equal" if sub else "CHANGED", "births", c["births"], "credits", c["body_clicks"], "turns", c["turns"], "laid_back", c["laid_back"], "transient bits", bits, "run back", back, "" if sub or fa is None else f"first apart at i {fa['found'].get('i')} ({fa['found'].get('event')})")

print("\n## the 48 on the clicks (run_48.py: rotations equal / conjugate / apart by det)")
for name in sorted(os.listdir(out)):
    if name.startswith("c48") and name.endswith(".stdout"):
        d = last_json(os.path.join(out, name))
        rows = [json.loads(x) for x in open(os.path.join(out, name)).read().strip().splitlines() if x.startswith("{") and "image" in x]
        if d and "counts" in d:
            print(name[:-7], "counts", d["counts"], "by det", d["by_det"], "base", d["base"]["births"], d["base"]["credits"], d["base"]["turns"], "first apart", d["first_apart_intervals"])
        else:
            byd = {}
            for r in rows:
                byd.setdefault(r["det"], {}).setdefault(r["verdict"], 0)
                byd[r["det"]][r["verdict"]] += 1
            print(name[:-7], "CUT SHORT at", len(rows), "of 48 images:", byd)

print("\n## the torque on the hole 60 (tq1's reader under the form): sum |term| over the record per component, the one-sided Link term against the Link's symmetric term and the step")
for f in ("off", "sum", "geo", "link"):
    p = os.path.join(out, f"tq_hole60_{f}.json")
    if not os.path.exists(p):
        print(f, "not finished")
        continue
    s = json.load(open(p))["summary"]
    terms = s["sum_abs_over_record"]
    def ints(v):
        found = []
        for x in v:
            x = str(x)
            found.append(int(x.split("/")[0]) // int(x.split("/")[1]) if "/" in x else int(x))
        return found
    print(f, "identity misses", s["identity_misses"], "line misses", s["line_misses"], "births", s["counts"]["births"])
    for t in ("link_asym", "link_sym", "ride", "turn", "rounding", "mass"):
        print("   ", t, ints(terms[t]))
    print("    step (int)", s["sum_abs_int"]["step"], "swap", s["sum_abs_int"]["swap"])

print("\n## J at the click on the hole 60 (aj1's reader)")
for f in ("off", "sum", "geo", "link"):
    p = os.path.join(out, f"aj1_hole60_{f}.json")
    if os.path.exists(p):
        d = json.load(open(p))
        c = d["counts"]
        print(f, "births", c["births"], "mergers", c["mergers"], "J conserved at the event", c["births: balance 0 about the centre (J conserved at the event)"], "about the Link's own axis 0", c["births: moment about the Link's own axis 0 (take and lay)"], "lay's moment 0", c["births: lay's moment about the Link's midpoint 0"], "W_children summing 0", c["births: W_children summing 0"], "credits", c["credits"])

print("\n## the chiral under FR-S1's two lines (rl1_probe.py, every 100 intervals)")
for f in ("sum", "link"):
    p = os.path.join(out, f"chiral3000_fr_{f}.stdout")
    rows = [json.loads(x) for x in open(p).read().strip().splitlines() if x.startswith("{")] if os.path.exists(p) else []
    print(f, "reached", rows[-1]["i"] if rows and "i" in rows[-1] else 0)
    for r in rows:
        if "i" in r:
            print("   ", r)
