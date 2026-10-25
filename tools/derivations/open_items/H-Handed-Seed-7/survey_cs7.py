"""cs7's survey of the second bang under EQ-S1's net reading (CS7_EQ=n; the flags far + no body), 400 intervals on the 4-cube with no sea, the cycle pattern at 5 quanta: every file named (K rows of one pair) at the mirrors and senses named; per run one line: the first alike close (64 births, crowd 0), the exact returns to Gamma at every Node, the births after the first bang (interval, count, rows, classes), the first interval not uniform, the tops with 64 turning, the credits laid back; the record kept (slimmed) where an exact return or a later alike close is found, else removed. No shell loop.
Usage: python survey_cs7.py <out dir> <workers> <mirrors: 0,1> <senses: p,m> <stem>... (stems with K: hh, ht at 2 to 8; ga, gl, gm, gb at 2 to 8)"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.set_int_max_str_digits(0)
here = os.path.dirname(os.path.abspath(__file__))
out, workers, mirrors, senses, stems = sys.argv[1], int(sys.argv[2]), [int(v) for v in sys.argv[3].split(",")], sys.argv[4].split(","), sys.argv[5:]
os.makedirs(out, exist_ok=True)
PY = "/home/user/Universe24/venv314/bin/python"
env = dict(os.environ, PYTHONPATH=f"{here}/src_cs7:{here}", TMPDIR="/dev/shm/tmp", CS4_TAKE_FARTHEST="1", CS4_LIGHT_NO_BODY="1", CS7_EQ=os.environ.get("CS7_EQ", "n"))
p1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
jobs = []
for stem in stems:
    for k in range(2, 9):
        world = f"{here}/worlds/empty4_{stem}{k}_400.json"
        if not os.path.exists(world):
            continue
        for sense in senses:
            for mirror in mirrors:
                tag = f"{stem}{k}_s{sense}_m{mirror}"
                pat = f"{out}/{tag}.pat.json"
                json.dump({"p1": p1, "cz": 1, "quanta": 5, "mirror": mirror, "sense": 1 if sense == "p" else -1}, open(pat, "w"))
                jobs.append((tag, world, pat))


def run(job):
    tag, world, pat = job
    rec = f"{out}/{tag}.json"
    with open(f"{out}/{tag}.log", "w") as log:
        subprocess.run(["nice", "-n", "19", PY, f"{here}/cs6_run.py", world, rec, pat], env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
    try:
        r = json.load(open(rec))
    except Exception as e:
        return f"{tag}: FAILED {e}"
    gamma = int(r["gamma"])
    cube = int(r["cube"])
    log = r["log"]
    lay = log[0]
    light = lay["line_pair"]
    phases = lay.get("phases")
    diag = [d for d in r["diag"] if d["i"] >= 1]
    births = {}
    for e in log:
        if e["event"] == "birth":
            births.setdefault(e["i"], []).append(e)
    landing = {e["i"]: e for e in log if e["event"] == "landing"}
    alike = [i for i, es in sorted(births.items()) if len(es) == 64 and landing[i]["nodes_crowded"] == 0]
    first = min(births) if births else None
    later = []
    for i, es in sorted(births.items()):
        if first is not None and i > first + 5:
            rows = {}
            classes = {}
            for e in es:
                rows[str(e["line_pair"])] = rows.get(str(e["line_pair"]), 0) + 1
                c = phases[(e["node"][0] * cube + e["node"][1]) * cube + e["node"][2]] if phases else None
                classes[str(c)] = classes.get(str(c), 0) + 1
            later.append((i, len(es), rows, classes, landing[i]["nodes_crowded"], landing[i]["nodes_with_light_child"], {c: sorted(v) for c, v in sorted(landing[i]["draws_per_class"].items())}))
    exact = [d["i"] for d in diag if d["X_min"] == gamma and d["X_max"] == gamma]
    split = next((d["i"] for d in diag if d["X_min"] != d["X_max"]), None)
    means = [d["X_mean"] for d in diag]
    tops = [(diag[k]["i"], means[k], diag[k + 1]["turned"]) for k in range(1, len(diag) - 1) if means[k] >= means[k - 1] and means[k] > means[k + 1]]
    bottoms = [(diag[k]["i"], means[k], diag[k]["X_min"], diag[k]["X_max"]) for k in range(1, len(diag) - 1) if means[k] <= means[k - 1] and means[k] < means[k + 1]]
    credits = [e for e in log if e["event"] == "credit"]
    laid = sum(1 for e in credits if "laid_back" in e)
    keep = bool(exact) or len(alike) > 1
    if keep:
        for k in ("rows", "nodes"):
            r.pop(k, None)
        counts = {}
        kept = []
        for e in r["log"]:
            if e["event"] == "refused":
                key = f"{e['i']}:{e['cause']}" + ("_crowd" if "children_at_one_node" in e else "_standing" if "standing" in e else "_control" if "control" in e else "")
                counts[key] = counts.get(key, 0) + 1
            else:
                kept.append(e)
        r["log"] = kept
        r["refused_counts"] = counts
        json.dump(r, open(rec, "w"))
    else:
        os.remove(rec)
    first_draw = json.dumps({c: sorted(v) for c, v in sorted(landing[first]["draws_per_class"].items())}, separators=(",", ":")) if first in landing else None
    return (f"{tag}: light {light} rows {len(r['planes'])} | first bang {first}: {len(births.get(first, []))} crowd {landing[first]['nodes_crowded'] if first in landing else None} draws {first_draw} | alike closes {alike} | exact returns {exact[:6]} ({len(exact)}) | split {split} | tops {tops[:3]} | bottoms {bottoms[:2]} | credits {len(credits)} laid back {laid} | later births " + json.dumps(later[:3], separators=(",", ":")) + f" | X end {diag[-1]['X_min']}..{diag[-1]['X_max']} e {diag[-1]['e_max']} | kept {keep}")


with ThreadPoolExecutor(max_workers=workers) as ex:
    for line in ex.map(run, jobs):
        print(line, flush=True)
