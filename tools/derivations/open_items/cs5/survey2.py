"""cs5: the pattern search for the draw alike by parity: the cycle pattern varied by the sense (1, -1), the mirror (0, 1), the digits' shift (+0 to +3) and cz (1, 3), on the files named, 2 intervals under the flags; printed per run: the draws per class at i 1 and i 2, the births, the crowd; the runs whose births reach 64 at one close marked.
Usage: python survey2.py <out_dir> <quanta> <stem,...>"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

here = os.path.dirname(os.path.abspath(__file__))
py = "/home/user/Universe24/venv314/bin/python"
out_dir, q, stems = sys.argv[1], int(sys.argv[2]), sys.argv[3].split(",")
env = dict(os.environ, PYTHONPATH=os.path.join(here, "src_cs5"), TMPDIR="/dev/shm/tmp", CS4_TAKE_FARTHEST="1", CS4_LIGHT_NO_BODY="1")
p1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
jobs = []
for stem in stems:
    for sense in (1, -1):
        for mirror in (0, 1):
            for shift in range(4):
                for cz in (1, 3):
                    jobs.append((stem, sense, mirror, shift, cz))


def one(job):
    stem, sense, mirror, shift, cz = job
    tag = f"{stem}_q{q}_s{sense}_m{mirror}_sh{shift}_cz{cz}"
    pat = os.path.join(out_dir, f"pat_{tag}.json")
    json.dump({"p1": [(v + shift) % 4 for v in p1], "cz": cz, "quanta": q, "mirror": mirror, "sense": sense}, open(pat, "w"))
    out = os.path.join(out_dir, f"sv2_{tag}.json")
    with open(out.replace(".json", ".log"), "w") as f:
        subprocess.run(["nice", "-n", "19", py, os.path.join(here, "cs5_run.py"), os.path.join(here, "worlds", f"empty4_{stem}_6.json"), out, pat], env=env, stdout=f, stderr=subprocess.STDOUT, cwd=here)
    rec = json.load(open(out))
    os.remove(out)
    lines = []
    best = 0
    for e in rec["log"]:
        if e["event"] == "landing" and e["i"] <= 2:
            i = e["i"]
            births = sum(1 for b in rec["log"] if b["event"] == "birth" and b["i"] == i)
            best = max(best, births)
            crowd = sum(1 for r in rec["log"] if r["event"] == "refused" and r["i"] == i and "children_at_one_node" in r)
            lines.append(f"  i {i} draws {json.dumps(e['draws_per_class'], sort_keys=True)} births {births} crowd {crowd}")
    return f"{tag}: A {rec['log'][0]['amplitude']} best close {best}{' <== 64' if best == 64 else ''}\n" + "\n".join(lines)


with ThreadPoolExecutor(3) as pool:
    for line in pool.map(one, jobs):
        print(line, flush=True)
