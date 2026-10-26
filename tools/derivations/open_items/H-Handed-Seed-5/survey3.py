"""cs5: the count survey: the lift's pair listed K times (K 2 to 8) with the sense (1, -1) and the mirror (0, 1), 3 intervals under the flags; per run the draws per class at i 1 to 3, the births and the crowd; a close with 64 births marked.
Usage: python survey3.py <out_dir>"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

here = os.path.dirname(os.path.abspath(__file__))
py = "/home/user/Universe24/venv314/bin/python"
out_dir = sys.argv[1]
env = dict(os.environ, PYTHONPATH=os.path.join(here, "src_cs5b"), TMPDIR="/dev/shm/tmp", CS4_TAKE_FARTHEST="1", CS4_LIGHT_NO_BODY="1")
p1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
jobs = [(k, sense, mirror) for k in range(2, 9) for sense in (1, -1) for mirror in (0, 1)]


def one(job):
    k, sense, mirror = job
    tag = f"lift{k}_s{sense}_m{mirror}"
    pat = os.path.join(out_dir, f"pat_{tag}.json")
    json.dump({"p1": p1, "cz": 1, "quanta": 5, "mirror": mirror, "sense": sense}, open(pat, "w"))
    out = os.path.join(out_dir, f"sv3_{tag}.json")
    with open(out.replace(".json", ".log"), "w") as f:
        subprocess.run(["nice", "-n", "19", py, os.path.join(here, "cs5_run.py"), os.path.join(here, "worlds", f"empty4_lift{k}_6.json"), out, pat], env=env, stdout=f, stderr=subprocess.STDOUT, cwd=here)
    rec = json.load(open(out))
    os.remove(out)
    lines = []
    best = 0
    for e in rec["log"]:
        if e["event"] == "landing" and e["i"] <= 3:
            i = e["i"]
            births = sum(1 for b in rec["log"] if b["event"] == "birth" and b["i"] == i)
            best = max(best, births)
            crowd = sum(1 for r in rec["log"] if r["event"] == "refused" and r["i"] == i and "children_at_one_node" in r)
            lines.append(f"  i {i} draws {json.dumps(e['draws_per_class'], sort_keys=True)} births {births} crowd {crowd}")
    return f"{tag}: planes {len(rec['planes'])} best close {best}{' <== 64' if best == 64 else ''}\n" + "\n".join(lines)


with ThreadPoolExecutor(2) as pool:
    for line in pool.map(one, jobs):
        print(line, flush=True)
