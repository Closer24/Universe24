"""Mutants of stage 7a's act (Animate), each against tests/test_the_tensor24_act.py: killed names the first failing test.

usage: python -I mutants_7a.py <worktree at the head> <scratch folder>   (run here at 9e5233d7f: mutants_7a.txt)
"""

import shutil
import subprocess
import sys
from pathlib import Path

WT, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
STEP, MESH = "src/tensor24/engine/step.py", "src/tensor24/engine/mesh.py"
TEST = "tests/test_the_tensor24_act.py"
MUTANTS = {
    "the drive's tooth written where the gear did not tick": [
        (
            STEP,
            "        choose(k, r1, r),\n        go,\n        choose(k, kept, rd),\n",
            "        choose(k, r1, r),\n        go,\n        kept,\n",
        )
    ],
    "the time written where the clock fired, not where it ticked": [
        (STEP, "        choose(k, count, tn),\n", "        choose(fire, count, tn),\n")
    ],
    "J read on the pull, not the force": [
        (
            STEP,
            "gradient, np.expand_dims(force, 0)))",
            "gradient, np.expand_dims(force + spring * a, 0)))",
        )
    ],
    "the drive run back from a home of 1": [
        (STEP, "back, kept = carry(rd - j, teeth, 0)", "back, kept = carry(rd - j, teeth, 1)")
    ],
    "the run back's sources read on the state after": [
        (
            STEP,
            "force, j = sources(layout, State(choose(k, b, a), b, r, go, rd, ph, count, tn))",
            "force, j = sources(layout, s)",
        )
    ],
    "the run back's sources read at the count after": [
        (
            STEP,
            "State(choose(k, b, a), b, r, go, rd, ph, count, tn)",
            "State(choose(k, b, a), b, r, go, rd, ph, c, tn)",
        )
    ],
    "the impulse read at W+": [
        (STEP, "    p = w * (a - b) + (r - home(w, go))\n", "    p = wp * (a - b) + (r - home(w, go))\n")
    ],
    "the carry's home at W": [
        (
            STEP,
            "q, kept = carry(p + push, wp, home(wp, go))",
            "q, kept = carry(p + push, wp, home(w, go))",
        )
    ],
    "the first train's grip for every train": [(MESH, "grip[:, meshes]", "grip[:1, meshes]")],
    "the drive's quotient turned in the push": [
        (
            STEP,
            "a1, b1, r1 = gear(a, b, r, go, w, wp, driven(gearing, force, q))",
            "a1, b1, r1 = gear(a, b, r, go, w, wp, driven(gearing, force, -q))",
        )
    ],
    "the spring read on the before slot": [
        (STEP, "force = pull(layout, s) - spring * a", "force = pull(layout, s) - spring * s.b")
    ],
    "the drive at one tooth more": [
        (STEP, "    return carry(j, teeth, rd)\n", "    return carry(j, teeth + 1, rd)\n")
    ],
    "the drive run back with J added": [
        (STEP, "back, kept = carry(rd - j, teeth, 0)", "back, kept = carry(rd + j, teeth, 0)")
    ],
    "the run back's drive read forward": [
        (STEP, "q, kept = undrive(j, teeth, rd)", "q, kept = drive(j, teeth, rd)")
    ],
    "the gradient's planes in the axes' reverse order": [
        (
            STEP,
            "gradient = np.moveaxis(ends[:, :, 0] - ends[:, :, 1], 1, 0)",
            "gradient = np.moveaxis(ends[:, ::-1, 0] - ends[:, ::-1, 1], 1, 0)",
        )
    ],
    "the force's plane before the gradient's": [
        (
            STEP,
            "(np.expand_dims(a, 0), gradient, np.expand_dims(force, 0))",
            "(np.expand_dims(a, 0), np.expand_dims(force, 0), gradient)",
        )
    ],
}


def run(name, changes):
    tree = SCRATCH / "".join(ch if ch.isalnum() else "_" for ch in name)[:80]
    shutil.rmtree(tree, ignore_errors=True)
    for part in ("src", "tests"):
        shutil.copytree(WT / part, tree / part, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(WT / "pyproject.toml", tree / "pyproject.toml")
    for rel, old, new in changes:
        path = tree / rel
        text = path.read_text()
        assert text.count(old) == 1, (name, old)
        path.write_text(text.replace(old, new))
    got = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-x", TEST],
        cwd=tree,
        capture_output=True,
        text=True,
    )
    failed = [
        ln.split("::", 1)[-1] for ln in got.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))
    ]
    shutil.rmtree(tree)
    return got.returncode, failed, (got.stdout.strip().splitlines() or [""])[-1]


code, failed, tail = run("unmutated", [])
print(f"unmutated: rc={code} {tail}")
assert code == 0, failed
survivors = []
for name, changes in MUTANTS.items():
    code, failed, tail = run(name, changes)
    print(
        f"{'SURVIVED' if code == 0 else 'killed  '} {name}"
        + (f"  <- {failed[0].split(' - ')[0]}" if failed else "")
    )
    survivors += [name] if code == 0 else []
print(f"{len(MUTANTS)} mutants, {len(survivors)} survived")
