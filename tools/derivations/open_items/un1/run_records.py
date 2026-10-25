"""un1: the three records (hole 60, chiral 300, bodies 120) run three ways each, in parallel processes: the engine's src (David's),
the copy with the flag off (must be bit for bit David's), the copy with UN1_FREE=1 (predicted bit for bit David's: the branch-free
forms are the law's letter, not a new law). Prints the nine summaries and the comparison (state hash, log digest, rows digest,
Node-lines digest, counts, run back). Usage: run_records.py [back]"""

from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PY = "/home/user/Universe24/venv314/bin/python"
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
back = sys.argv[1] if len(sys.argv) > 1 else "10"
WORLDS = ["world_hole60.json", "world_chiral300.json", "world_bodies120.json"]
WAYS = {
    "src": (os.path.join(ROOT, "src"), ""),
    "copy_off": (os.path.join(HERE, "src_un1"), ""),
    "copy_free": (os.path.join(HERE, "src_un1"), "1"),
}

procs = []
for world in WORLDS:
    for way, (path, flag) in WAYS.items():
        env = dict(os.environ, PYTHONPATH=path, TMPDIR="/dev/shm/tmp")
        if flag:
            env["UN1_FREE"] = flag
        else:
            env.pop("UN1_FREE", None)
        out = os.path.join(OUT, f"{world[:-5]}_{way}.json")
        log = open(os.path.join(OUT, f"{world[:-5]}_{way}.log"), "w")
        procs.append(
            (
                world,
                way,
                out,
                subprocess.Popen(
                    [PY, os.path.join(HERE, "runner.py"), os.path.join(HERE, "worlds", world), out, back],
                    env=env,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                ),
            )
        )
found: dict[str, dict[str, dict]] = {}
for world, way, out, p in procs:
    p.wait()
    if p.returncode != 0:
        print(world, way, "FAILED, exit", p.returncode, open(out[:-5] + ".log").read()[-2000:])
        continue
    found.setdefault(world, {})[way] = json.load(open(out))

KEYS = ["state_hash", "log_digest", "rows_digest", "nodes_digest", "counts", "run_back", "census", "max_transient", "turns_total"]
for world, ways in found.items():
    print("==", world)
    for way, s in ways.items():
        print(
            way,
            "flag", repr(s["flag"]), "FREE", s["free_in_module"], "state", s["state_hash"], "log", s["log_digest"],
            s["log_lines"], "rows", s["rows_digest"], "nodes", s["nodes_digest"], "births", s["births"], "credits",
            s["credits"], "turns", s["turns_total"], "run back", s["run_back"], "census", s["census"], "transient",
            s["max_transient"], "charge", s["charge_at_births"], "zero senses", s["zero_senses"], "taken>=booked",
            s["taken_ge_booked"], "of", s["births"],
        )
    base = ways.get("src")
    for way in ("copy_off", "copy_free"):
        if base and way in ways:
            same = [k for k in KEYS if ways[way][k] == base[k]]
            apart = [k for k in KEYS if ways[way][k] != base[k]]
            print(f"  {way} against src: equal {same}; apart {apart}")
