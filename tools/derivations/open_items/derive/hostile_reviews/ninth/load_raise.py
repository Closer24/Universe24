"""Probe: checker-held files on which the load raises rather than naming (the claim of 91226e796).

A. The plan's scatter, np.zeros((rows, terms)), sits outside any guard: one train of N T1 kinds on a hand (rows 6N) and
   M cross rows T1 x T1 -> T1 (6 terms each) ask rows x terms x 8 bytes, quadratic in a file of a few hundred KB.
B. The lay guards its first three arrays, but not the going (0 * a) built after them: under an address-space limit that
   holds three of the arrays and not four, the load raises.
The address space is capped (RLIMIT_AS) so no allocation can touch memory the machine lacks: case A's cap, 20 GB, is
above this machine's 15 GB of RAM, so it constrains nothing real; case B's cap is set to hold 3.75 of its arrays.
usage: python -I load_raise.py <worktree> <A|B|C> <out dir>"""

import inspect
import json
import resource
import subprocess
import sys
import time
import traceback
from pathlib import Path

WT, CASE, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path[:0] = [str(WT / "src")]
import numpy as np  # noqa: E402

from tensor24.engine.contract import Plan, contract  # noqa: E402
from tensor24.main import made  # noqa: E402
from tensor24.runner.files import departures, sites_of  # noqa: E402
from tensor24.runner.load import load  # noqa: E402


def vm():
    return int(next(l for l in open("/proc/self/status") if l.startswith("VmSize")).split()[1]) * 1024


def files(n_kinds, m_rows, shape, gears=()):
    u = {"version": 1, "integers": {"den": 5, "full_rate": 1000, "key": 36000, "trace": 6, "width": 128},
         "trains": [{"name": "big", "kinds": ["T1"] * n_kinds, "part": 2, "pinion": 3, "sine": 4}],
         "couplings": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]] * m_rows}
    p = {"version": 1, "shape": list(shape)}
    s = {"version": 1, "ticks": 1, "gears": [list(g) for g in gears]}
    OUT.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, doc in (("universe", u), ("piece", p), ("setting", s)):
        (OUT / f"{name}.json").write_text(json.dumps(doc), encoding="utf-8")
        paths.append(OUT / f"{name}.json")
    return u, p, s, paths


def run(u, p, s, paths):
    found = departures(*paths)
    print(f"files: {', '.join(f'{x.name} {x.stat().st_size} bytes' for x in paths)}; the checker: {found[:3] or 'holds'}")
    if found:
        return
    t = time.time()
    try:
        held, named = load(u, s, sites_of(p["shape"]), *made(tuple(p["shape"])))
        print(f"the load: named {named[:2]}, loaded {held is not None} in {time.time() - t:.1f}s")
        return held
    except BaseException as error:  # noqa: BLE001
        print(f"the load RAISED {type(error).__name__}: {str(error)[:160]}")
        print("  " + " | ".join(line.strip() for line in traceback.format_exc().splitlines()[-6:-1]))


if CASE == "A":
    resource.setrlimit(resource.RLIMIT_AS, (20 << 30, 20 << 30))
    n = m = 10_000
    print(f"A: one T1 train of {n} kinds on a hand (rows {6 * n}), {m} cross rows ({6 * m} terms); "
          f"a dense scatter of them asks {6 * n * 6 * m * 8 / 2**30:.1f} GiB")
    u, p, s, paths = files(n, m, (2, 2, 2))
    run(u, p, s, paths)
    env = {"PYTHONPATH": str(WT / "src"), "PATH": "/usr/bin:/bin", "TMPDIR": "/dev/shm/tmp"}
    tool = subprocess.run(["/bin/sh", "-c", f"ulimit -v {20 << 20}; exec /home/user/Universe24/venv314/bin/python "
                           f"{WT}/tools/tensor24_files.py {' '.join(map(str, paths))}"],
                          env=env, capture_output=True, text=True, timeout=600)
    print(f"tools/tensor24_files.py on them: exit {tool.returncode} (1 is also its exit for a named departure); "
          f"stderr's last line: {(tool.stderr.strip().splitlines() or ['-'])[-1][:160]}")
elif CASE == "B":
    rows, sites = 2, 40_000_000  # the hand's two rows (one A1 kind), one array 640 MB
    u, p, s, paths = files(0, 0, (sites, 1, 1))
    u["trains"][0]["kinds"] = ["A1"]
    (OUT / "universe.json").write_text(json.dumps(u), encoding="utf-8")
    made((sites, 1, 1))
    base = vm()
    cap = base + int(3.75 * rows * sites * 8)
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    print(f"B: a board of {sites} sites, two rows: one array {rows * sites * 8 / 2**20:.0f} MiB; the cap holds 3.75 of them (three, and the clocks of half of one)")
    run(u, p, s, paths)
elif CASE == "C":
    for n in (100, 200, 400):
        u, p, s, paths = files(n, n, (8, 1, 1))
        held = run(u, p, s, paths)
        rows, terms = 6 * n, len(held.plan[0])
        readings = np.ones((7 * rows, 8), dtype=object)
        t = time.time()
        gears = [held.state[0]][: len(inspect.signature(contract).parameters) - 2]  # the gears' shape where contract takes it (after the ninth's changes)
        contract(Plan(*held.plan), readings, *gears)
        print(f"C: rows {rows}, terms {terms}, rows x terms {rows * terms}: one contraction {time.time() - t:.4f}s")
