"""Hand g3: the toy's runs, four at a time (no shell loop): each a body_toy.py configuration named below, its output under
tools/derivations/open_items/H-Gap-Of-The-Middle-3/out/<name>.jsonl and its log <name>.log. Run from the worktree root with PYTHONPATH=<worktree>/src."""
import os, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
PY = "/home/user/Universe24/venv314/bin/python"
BEST, CTRL, SMALL = "1655909141", "15162856759112389", "193253"
RUNS = {
    "A1_wide_well_best": ["--den", BEST, "--cube", "9", "--g-target", "650", "--lay", "wide", "--sigma", "20", "--hold", "rising", "--well-depth", "300", "--well-offset", "3", "--intervals", "200", "--run-back"],
    "A2_wide_well_ctrl": ["--den", CTRL, "--cube", "9", "--g-target", "838", "--lay", "wide", "--sigma", "20", "--hold", "rising", "--well-depth", "300", "--well-offset", "3", "--intervals", "200", "--run-back"],
    "A3_point_well_best": ["--den", BEST, "--cube", "9", "--g-target", "650", "--lay", "point", "--hold", "rising", "--well-depth", "300", "--well-offset", "3", "--intervals", "200", "--run-back"],
    "A4_point_well_ctrl": ["--den", CTRL, "--cube", "9", "--g-target", "838", "--lay", "point", "--hold", "rising", "--well-depth", "300", "--well-offset", "3", "--intervals", "200", "--run-back"],
    "B1_wide_flat0_best": ["--den", BEST, "--cube", "9", "--g-target", "650", "--lay", "wide", "--sigma", "20", "--hold", "rising", "--content", "0", "--intervals", "200", "--run-back"],
    "B2_wide_flat300_best": ["--den", BEST, "--cube", "9", "--g-target", "650", "--lay", "wide", "--sigma", "20", "--hold", "rising", "--content", "300", "--intervals", "200", "--run-back"],
    "B3_wide_flat0_ctrl": ["--den", CTRL, "--cube", "9", "--g-target", "838", "--lay", "wide", "--sigma", "20", "--hold", "rising", "--content", "0", "--intervals", "200"],
    "B4_wide_flat300_ctrl": ["--den", CTRL, "--cube", "9", "--g-target", "838", "--lay", "wide", "--sigma", "20", "--hold", "rising", "--content", "300", "--intervals", "200"],
    "C1_pair_point_letter_best": ["--den", BEST, "--cube", "7", "--g-target", "650", "--lay", "point", "--hold", "none", "--pair", "3", "--intervals", "300", "--run-back"],
    "C2_wide_well_once_best": ["--den", BEST, "--cube", "9", "--g-target", "650", "--lay", "wide", "--sigma", "20", "--hold", "none", "--well-depth", "300", "--well-offset", "3", "--intervals", "200", "--run-back"],
    "D1_wide4q_well_best": ["--den", BEST, "--cube", "9", "--g-target", "650", "--lay", "wide", "--sigma", "20", "--quanta", "4", "--hold", "rising", "--well-depth", "300", "--well-offset", "3", "--intervals", "200", "--run-back"],
    "D2_wide_well_small": ["--den", SMALL, "--cube", "9", "--g-target", "650", "--lay", "wide", "--sigma", "20", "--hold", "rising", "--well-depth", "300", "--well-offset", "3", "--intervals", "200", "--run-back"],
}
names = sys.argv[1:] or list(RUNS)
env = dict(os.environ, PYTHONPATH=str(HERE.parents[2] / "src"), TMPDIR="/dev/shm/tmp")
running = []
queue = list(names)
t0 = time.time()
while queue or running:
    while queue and len(running) < 4:
        name = queue.pop(0)
        log = open(OUT / f"{name}.log", "w")
        proc = subprocess.Popen([PY, str(HERE / "body_toy.py"), *RUNS[name], "--out", str(OUT / f"{name}.jsonl")], stdout=log, stderr=subprocess.STDOUT, env=env, cwd=str(HERE.parents[2]))
        running.append((name, proc, log))
    time.sleep(2)
    still = []
    for name, proc, log in running:
        if proc.poll() is None:
            still.append((name, proc, log))
        else:
            log.close()
            print(f"{name} exit {proc.returncode} at {time.time() - t0:.0f} s", flush=True)
    running = still
print("done", round(time.time() - t0), "s")
