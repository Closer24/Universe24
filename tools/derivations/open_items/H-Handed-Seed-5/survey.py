"""cs5: the draw survey: every named universe file at the named quanta run for a few intervals under the flags (the light no body, the take by the fall's sign), the landing census read: per close the draws per class, the births, the crowd and standing refusals. Three workers, no shell loop.
Usage: python survey.py <out_dir> <intervals> <quanta,...> <stem,...>"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

here = os.path.dirname(os.path.abspath(__file__))
py = "/home/user/Universe24/venv314/bin/python"
out_dir, n, quanta, stems = sys.argv[1], int(sys.argv[2]), [int(q) for q in sys.argv[3].split(",")], sys.argv[4].split(",")
env = dict(os.environ, PYTHONPATH=os.path.join(here, "src_cs5"), TMPDIR="/dev/shm/tmp", CS4_TAKE_FARTHEST="1", CS4_LIGHT_NO_BODY="1")


def one(job):
    stem, q = job
    out = os.path.join(out_dir, f"sv_{stem}_q{q}_{n}.json")
    log = out.replace(".json", ".log")
    with open(log, "w") as f:
        subprocess.run(["nice", "-n", "19", py, os.path.join(here, "cs5_run.py"), os.path.join(here, "worlds", f"empty4_{stem}_{n}.json"), out, os.path.join(here, "worlds", f"cycle_m{q}.json")], env=env, stdout=f, stderr=subprocess.STDOUT, cwd=here)
    rec = json.load(open(out))
    lines = []
    for e in rec["log"]:
        if e["event"] == "landing":
            i = e["i"]
            births = sum(1 for b in rec["log"] if b["event"] == "birth" and b["i"] == i)
            causes = {}
            for r in rec["log"]:
                if r["event"] == "refused" and r["i"] == i:
                    k = r["cause"] + ("_crowd" if "children_at_one_node" in r else "_standing" if "standing" in r else "")
                    causes[k] = causes.get(k, 0) + 1
            lines.append(f"  i {i} draws {json.dumps(e['draws_per_class'], sort_keys=True)} births {births} refused {json.dumps(causes, sort_keys=True)}")
    diag = rec["diag"]
    xs = [(d["i"], d["X_min"], d["X_max"]) for d in diag]
    os.remove(out)
    return f"{stem} q{q}: A {rec['log'][0]['amplitude']} planes {len(rec['planes'])} births {rec['counts']['births']} X {xs[-1]}\n" + "\n".join(lines)


jobs = [(s, q) for s in stems for q in quanta]
with ThreadPoolExecutor(3) as pool:
    for line in pool.map(one, jobs):
        print(line, flush=True)
