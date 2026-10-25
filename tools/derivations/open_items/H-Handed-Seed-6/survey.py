"""cs6's count survey (cs5's survey4 rebuilt on cs6_run.py, no shell loop): every file of the stems named, K rows of one pair, at the sense 1 / -1 and the mirror 0 / 1, 4 intervals under the flags far + no body; the finding per run: the first close of 64 births with crowd 0 (the alike bang) and the draws per class at every landing. Usage: python survey.py <out dir> <workers> <stem> ... (the stems ga, gb, gc, gl, gm; K 2 to 8)"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.set_int_max_str_digits(0)
here = os.path.dirname(os.path.abspath(__file__))
out, workers, stems = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
os.makedirs(out, exist_ok=True)
PY = "/home/user/Universe24/venv314/bin/python"
env = dict(os.environ, PYTHONPATH=f"{here}/src_cs6:{here}", TMPDIR="/dev/shm/tmp", CS4_TAKE_FARTHEST="1", CS4_LIGHT_NO_BODY="1")
p1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
jobs = []
for stem in stems:
    for k in range(2, 9):
        for sense in (1, -1):
            for mirror in (0, 1):
                tag = f"{stem}{k}_s{'p' if sense == 1 else 'm'}_m{mirror}"
                pat = f"{out}/{tag}.pat.json"
                json.dump({"p1": p1, "cz": 1, "quanta": 5, "mirror": mirror, "sense": sense}, open(pat, "w"))
                jobs.append((tag, f"{here}/worlds/empty4_{stem}{k}_4.json", pat))
def run(job):
    tag, world, pat = job
    rec = f"{out}/{tag}.json"
    with open(f"{out}/{tag}.log", "w") as log:
        subprocess.run(["nice", "-n", "19", PY, f"{here}/cs6_run.py", world, rec, pat], env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
    try:
        r = json.load(open(rec))
    except Exception as e:
        return f"{tag}: FAILED {e}"
    light = r["log"][0]["line_pair"]
    found = []
    for e in r["log"]:
        if e["event"] == "landing":
            i = e["i"]
            births = sum(1 for b in r["log"] if b["event"] == "birth" and b["i"] == i)
            found.append((i, births, e["nodes_crowded"], {c: sorted(v) for c, v in sorted(e["draws_per_class"].items())}))
    alike = [i for i, b, c, d in found if b == 64 and c == 0]
    os.remove(rec)
    return f"{tag}: alike at {alike} light {light}; " + " ".join(f"i{i}:b{b}:c{c}:{json.dumps(d, separators=(',', ':'))}" for i, b, c, d in found[:4])
with ThreadPoolExecutor(max_workers=workers) as ex:
    for line in ex.map(run, jobs):
        print(line, flush=True)
