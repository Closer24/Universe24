"""em2's runner (no shell loops): every record under the default src, the flagged copy with the flag absent, and the flagged copy under EM2_EMISSION=quantum, in parallel subprocesses; the counts and the run back printed per record. Usage: python run_records.py <tag> <world file name> <intervals or 0 for the file's> [more tag/world/intervals triples]"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PY = "/home/user/Universe24/venv314/bin/python"
OUT = os.path.join(HERE, "out")
WORLDS = os.path.join(HERE, "worlds")
os.makedirs(OUT, exist_ok=True)


def world_file(name, intervals):
    """The world's file, its intervals replaced where asked; written beside the worlds."""
    if not intervals:
        return os.path.join(WORLDS, name)
    w = json.load(open(os.path.join(WORLDS, name)))
    w["intervals"] = intervals
    path = os.path.join(WORLDS, name.replace(".json", f"_{intervals}.json"))
    json.dump(w, open(path, "w"))
    return path


def launch(tag, world, src, env_flag):
    env = dict(os.environ, PYTHONPATH=src, TMPDIR="/dev/shm/tmp")
    if env_flag:
        env["EM2_EMISSION"] = "quantum"
    else:
        env.pop("EM2_EMISSION", None)
    out_json = os.path.join(OUT, f"{tag}.json")
    log = open(os.path.join(OUT, f"{tag}.txt"), "w")
    return subprocess.Popen([PY, "-m", "event_universe.run", world, out_json, "back", "10"], stdout=log, stderr=subprocess.STDOUT, env=env, cwd=HERE)


args = sys.argv[1:]
jobs = []
for k in range(0, len(args), 3):
    tag, name, intervals = args[k], args[k + 1], int(args[k + 2])
    world = world_file(name, intervals)
    jobs.append((f"{tag}_default", launch(f"{tag}_default", world, os.path.join(ROOT, "src"), False)))
    jobs.append((f"{tag}_off", launch(f"{tag}_off", world, os.path.join(HERE, "src_em2"), False)))
    jobs.append((f"{tag}_flag", launch(f"{tag}_flag", world, os.path.join(HERE, "src_em2"), True)))
for tag, p in jobs:
    p.wait()
    lines = open(os.path.join(OUT, f"{tag}.txt")).read().strip().split("\n")
    print(tag, "exit", p.returncode, *lines[-2:], sep="\n  ")
