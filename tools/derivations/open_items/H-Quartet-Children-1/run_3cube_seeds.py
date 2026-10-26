"""Several seeds on the 3-cube under the flag HQ_S1 (each run under 20 s): the chiral seed's three packets at other centres (b to e) and the hole seed; the records under /dev/shm/tmp/qc1, the readings under out/, the Bell cells pooled over every 3-cube record (the pairs of all the seeds in one count)."""
import json, os, subprocess, sys
from collections import Counter
P = "/home/user/Universe24/venv314/bin/python"
W = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/qc1"
H = W + "/tools/derivations/open_items/H-Quartet-Children-1"
D = H + "/worlds"
env = dict(os.environ, TMPDIR="/dev/shm/tmp", PYTHONPATH="/dev/shm/tmp/qc1/src_qc1", HQ_S1="1")
seeds = {
    "chiral3b_60": [[1, 1, 0], [0, 2, 2], [2, 0, 1]],
    "chiral3c_60": [[2, 0, 0], [1, 2, 1], [0, 1, 2]],
    "chiral3d_60": [[0, 1, 0], [2, 2, 1], [1, 0, 2]],
    "chiral3e_60": [[1, 0, 1], [0, 2, 0], [2, 1, 2]],
}
names = []
for name, centres in seeds.items():
    w = {"universe": "universe_quartet_toy.json", "shape": [3, 3, 3], "intervals": 60, "seed": [{"lay": "sea", "row": 0}, {"lay": "hole", "at": [0, 0, 0]}] + [{"lay": "at", "row": 0, "centre": c, "quanta": 1} for c in centres]}
    json.dump(w, open(D + "/world_" + name + ".json", "w"))
    names.append(name)
if os.path.exists(D + "/world_hole3_60.hold"):
    os.rename(D + "/world_hole3_60.hold", D + "/world_hole3_60.json")
names.append("hole3_60")
if len(sys.argv) > 1:
    names = [n for n in sys.argv[1:] if n != "pool"]
for name in names:
    out = open("/dev/shm/tmp/qc1/" + name + ".out", "w")
    subprocess.run(["nice", "-n", "19", P, "-m", "event_universe.run", D + "/world_" + name + ".json", "/dev/shm/tmp/qc1/" + name + ".json", "back", "10"], env=env, stdout=out, stderr=subprocess.STDOUT, cwd="/dev/shm/tmp/qc1")
    subprocess.run(["nice", "-n", "19", P, H + "/hq_reader.py", "/dev/shm/tmp/qc1/" + name + ".json", "/dev/shm/tmp/qc1/src_qc1", H + "/out/" + name + "_reading.json"], env=env, stdout=open("/dev/shm/tmp/qc1/" + name + ".reading.txt", "w"), stderr=subprocess.STDOUT)
    if not os.path.exists(H + "/out/" + name + "_reading.json"):
        print(name, "no record (the run ended early)", flush=True)
        continue
    r = json.load(open(H + "/out/" + name + "_reading.json"))
    print(name, "births", r["births"], "by shape", r["births by the children's shape"], "run back", r["run_back"], "quartet pairs clicked", r["quartet pairs clicked at both ends"], "axis kept", r["axis sign kept, summed"], "dominant", r["dominant axis kept, summed"], "axes sum 0", r["pairs' axes summed to 0"], "W sum 0", r["pairs' W summed to 0"], flush=True)
# the pool over every 3-cube reading
pool = {}
total = Counter()
for f in sorted(os.listdir(H + "/out")):
    if not f.endswith("_reading.json") or "3" not in f.split("_")[0]:
        continue
    r = json.load(open(H + "/out/" + f))
    total["records"] += 1
    total["births"] += r["births"]
    total["quartet pairs clicked"] += r["quartet pairs clicked at both ends"]
    total["plane pairs clicked"] += r["plane pairs clicked at both ends"]
    total["axis kept"] += r["axis sign kept, summed"][0]
    total["credits on tracks"] += r["axis sign kept, summed"][1]
    total["dominant kept"] += r["dominant axis kept, summed"][0]
    for k, v in r["bell on the quartet pairs"].items():
        cells = pool.setdefault(k, {})
        for cell, (same_minus_opp, n) in v["E (same - opposite, n)"].items():
            c = cells.setdefault(cell, [0, 0])
            c[0] += same_minus_opp
            c[1] += n
sys.path.insert(0, "/dev/shm/tmp/qc1/src_qc1")
sys.path.insert(0, H)
from hq_reader import s_of  # noqa: E402
pooled = {}
for k, cells in pool.items():
    cc = {}
    for cell, (d, n) in cells.items():
        a, b = (int(x) for x in cell.split(","))
        cc[(a, b)] = Counter({1: (n + d) // 2, -1: (n - d) // 2})
    pooled[k] = s_of(cc)
json.dump({"total": dict(total), "pooled bell": pooled}, open(H + "/out/bell_pooled_3cube.json", "w"), indent=1)
print(json.dumps(dict(total)))
for k, v in pooled.items():
    print(k, "S", v.get("S"), v.get("band", v.get("why")), "E", v["E (same - opposite, n)"])
