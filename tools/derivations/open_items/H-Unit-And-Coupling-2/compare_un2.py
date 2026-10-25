"""un2: run one world under David's src (base), under the copy with the flag absent (off) and with UN2_GENERIC=1 (on), each in its own
process (`python -m event_universe.run <world> <out> back 10`), then compare the records bit for bit with the timing field alone
stripped (the reader's milliseconds). Usage: python compare_un2.py <world.json> <name> [modes...]  (modes default: base off on).
Prints one line per mode (seconds, counts, run back) and one line per comparison (EQUAL or the first differing key)."""

import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PY = "/home/user/Universe24/venv314/bin/python"
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
os.makedirs("/dev/shm/tmp", exist_ok=True)

SRCS = {
    "base": os.path.join(ROOT, "src"),
    "off": os.path.join(HERE, "src_un2"),
    "on": os.path.join(HERE, "src_un2"),
}


def run(world: str, name: str, mode: str) -> str:
    out = os.path.join(OUT, f"{name}_{mode}.json")
    env = dict(os.environ, PYTHONPATH=SRCS[mode], TMPDIR="/dev/shm/tmp")
    env.pop("UN2_GENERIC", None)
    if mode == "on":
        env["UN2_GENERIC"] = "1"
    t0 = time.monotonic_ns()
    done = subprocess.run(
        [PY, "-m", "event_universe.run", world, out, "back", "10"],
        env=env,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    seconds = (time.monotonic_ns() - t0) // 1000000000
    if done.returncode != 0:
        print(mode, "FAILED", done.stderr[-2000:])
        sys.exit(1)
    lines = [json.loads(line) for line in done.stdout.splitlines() if line.startswith("{")]
    counts = next(x["counts"] for x in lines if "counts" in x)
    back = next((x["run back"] for x in lines if "run back" in x), None)
    kept = {k: counts[k] for k in ("births", "body_clicks", "turns", "refused_lay", "refused_orientation", "refused_twist", "refused_stop", "taken", "booked", "laid")}
    print(mode, name, "seconds", seconds, "run back", back, "counts", json.dumps(kept))
    return out


def stripped(path: str):
    rec = json.load(open(path, encoding="utf-8"))
    for row in rec["rows"]:
        row.pop("milliseconds", None)
    return rec


def first_difference(a, b, path=""):
    if type(a) is not type(b):
        return path + " type"
    if isinstance(a, dict):
        if sorted(a) != sorted(b):
            return path + " keys " + str(sorted(set(a) ^ set(b)))
        for k in a:
            d = first_difference(a[k], b[k], path + "/" + str(k))
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return path + f" length {len(a)} against {len(b)}"
        for i, (x, y) in enumerate(zip(a, b, strict=True)):
            d = first_difference(x, y, path + f"[{i}]")
            if d:
                return d
        return None
    return None if a == b else path + f" {str(a)[:60]} against {str(b)[:60]}"


def main(argv):
    world, name = argv[1], argv[2]
    modes = argv[3:] or ["base", "off", "on"]
    outs = {m: run(world, name, m) for m in modes}
    base = stripped(outs[modes[0]])
    for m in modes[1:]:
        d = first_difference(base, stripped(outs[m]))
        print("compare", name, modes[0], "against", m, "EQUAL" if d is None else "DIFFERS at " + d)


if __name__ == "__main__":
    main(sys.argv)
