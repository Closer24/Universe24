"""lc2: one line per course record (course_*.json): the laws' numbers and the course's marks. Usage: python summarize.py course_a.json [course_b.json ...] [--rows A B] (the rows A..B printed for the first file)."""
import json
import sys

MARKS = (10, 30, 60, 120, 200, 220, 300, 400)


def line(path):
    d = json.load(open(path))
    s, rows = d["summary"], d["rows"]
    by = {r["i"]: r for r in rows}
    marks = {i: (by[i]["mean"], by[i]["max"], by[i]["e_rms"]) for i in MARKS if i in by}
    cred = sum(r["credits"] for r in rows)
    cred220 = sum(r["credits"] for r in rows if r["i"] <= 220)
    births = sum(r["births"] for r in rows)
    wmax = s["links_weighted_abs_max_num_den"]
    print(json.dumps({
        "file": path, "form": s["form"], "back": s["run_back"], "bits": s["max_bits"], "ints": s["integers"],
        "births": births, "credits": cred, "credits_by_220": cred220, "turns": s["counts"]["turns"],
        "first_turn": s.get("first_turn_readings"), "tops": s["tops"][:8], "returns": s["returns_to_seed"][:6],
        "min_after_top": s["mean_min_after_first_top"], "links_plain_sign(+,-,0)": s["links_plain_sign"],
        "links_plain_abs_max": s["links_plain_abs_max"], "links_weighted_abs_max": wmax[0] // wmax[1],
        "marks(i:(mean,max,e_rms))": marks,
    }))


args = [a for a in sys.argv[1:] if a.endswith(".json")]
for p in args:
    line(p)
if "--rows" in sys.argv:
    k = sys.argv.index("--rows")
    a, b = int(sys.argv[k + 1]), int(sys.argv[k + 2])
    d = json.load(open(args[0]))
    w = d["rows"][0]["wall"]
    for r in d["rows"]:
        if a <= r["i"] <= b:
            write_plus = r["xpp_sum_unturned"] - (r["links_plain"] - r["mass_sum"]) // w
            print(r["i"], "mean", r["mean"], "min", r["min"], "max", r["max"], "e", r["e_rms"], "turned", r["turned"], r["turned_nodes"][:4],
                  "links", r["links_plain"], "links/w", r["links_plain"] // w, "mass/w", r["mass_sum"] // w, "xpp", r["xpp_sum_unturned"], "write+round", write_plus,
                  "births", r["births"], "credits", r["credits"], "W", r["W_total"], "frozen", r["frozen"], "reach_min/max", r["reach_min"], r["reach_max"], "Lmax@", r["links_abs_max"], r["links_abs_max_node"])
