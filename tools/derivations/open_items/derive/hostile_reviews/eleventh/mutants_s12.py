"""Source mutants of stage 7a's engine (step, mesh, state, contract) and of load's side(), run against every Tensor24 test.

Usage: python -I mutants_s12.py <base copy> <work dir> [names...]
Each mutant is one exact replacement in one file of a fresh copy of <base copy>; the Tensor24 tests run on the copy
with -x; a mutant survives when every test passes.
"""

import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

STEP = "src/tensor24/engine/step.py"
MESH = "src/tensor24/engine/mesh.py"
STATE = "src/tensor24/engine/state.py"
CONTRACT = "src/tensor24/engine/contract.py"
LOAD = "src/tensor24/runner/load.py"

M = {
    # the gear's carry
    "g1 stride read at W+": (STEP, "    p = w * (a - b) + (r - home(w, go))", "    p = wp * (a - b) + (r - home(w, go))"),
    "g2 impulse home at W+": (STEP, "    p = w * (a - b) + (r - home(w, go))", "    p = w * (a - b) + (r - home(wp, go))"),
    "g3 carry home at W": (STEP, "carry(p + push, wp, home(wp, go))", "carry(p + push, wp, home(w, go))"),
    "g4 ungear home at W": (STEP, "(r - home(wp, go)) - push, w, home(w, go))", "(r - home(w, go)) - push, w, home(w, go))"),
    "g5 ungear carry home at W+": (STEP, "(r - home(wp, go)) - push, w, home(w, go))", "(r - home(wp, go)) - push, w, home(wp, go))"),
    # the drive
    "d1 drive carries j+rd at 0 (equivalent)": (STEP, "    return carry(j, teeth, rd)", "    return carry(j + rd, teeth, 0)"),
    "d2 undrive keeps rd in": (STEP, "back, kept = carry(rd - j, teeth, 0)", "back, kept = carry(rd - j, teeth, rd)"),
    "d3 undrive reads -j": (STEP, "back, kept = carry(rd - j, teeth, 0)", "back, kept = carry(rd + j, teeth, 0)"),
    "d4 untick pushes j not q": (STEP, "ungear(a, b, r, go, w, wp, driven(gearing, force, q))", "ungear(a, b, r, go, w, wp, driven(gearing, force, j))"),
    "d5 tick pushes j not q": (STEP, "a1, b1, r1 = gear(a, b, r, go, w, wp, driven(gearing, force, q))", "a1, b1, r1 = gear(a, b, r, go, w, wp, driven(gearing, force, j))"),
    "d6 tick keeps rd where no tick too": (STEP, "        choose(k, kept, rd),\n        dial,\n        count,\n        choose(k, count, tn),", "        kept,\n        dial,\n        count,\n        choose(k, count, tn),"),
    "d7 tick keeps rd where fired": (STEP, "        choose(k, kept, rd),\n        dial,\n        count,\n        choose(k, count, tn),", "        choose(fire, kept, rd),\n        dial,\n        count,\n        choose(k, count, tn),"),
    "d8 untick rd unchosen": (STEP, "        choose(k, kept, rd),\n        dial,\n        count,\n        before,", "        kept,\n        dial,\n        count,\n        before,"),
    "d9 untick drive by drive": (STEP, "    q, kept = undrive(j, teeth, rd)", "    q, kept = drive(j, teeth, rd)"),
    # the push
    "p1 push without stretch on force": (STEP, "    return stretch * (force + kick * q)", "    return force + stretch * kick * q"),
    "p2 push kick squared": (STEP, "    return stretch * (force + kick * q)", "    return stretch * (force + kick * kick * q)"),
    "p3 push without force": (STEP, "    return stretch * (force + kick * q)", "    return stretch * kick * q"),
    # the sources
    "s1 J value plane zero": (STEP, "readings = np.concatenate((np.expand_dims(a, 0), gradient", "readings = np.concatenate((np.expand_dims(0 * a, 0), gradient"),
    "s2 J pull operand without spring": (STEP, "gradient, np.expand_dims(force, 0)))", "gradient, np.expand_dims(force + spring * a, 0)))"),
    "s3 J value and pull planes swapped": (STEP, "np.concatenate((np.expand_dims(a, 0), gradient, np.expand_dims(force, 0)))", "np.concatenate((np.expand_dims(force, 0), gradient, np.expand_dims(a, 0)))"),
    "s4 J readings gear-major": (STEP, "contract(plan, readings.reshape(-1, sites), a)", "contract(plan, np.swapaxes(readings, 0, 1).reshape(-1, sites), a)"),
    "s5 gradient from now slots whatever their time": (STEP, "    near = seen(s, nb)", "    near = s[0][:, nb]"),
    "s6 gradient from before slots": (STEP, "    near = seen(s, nb)", "    near = s[1][:, nb]"),
    "s7 gradient forward one-sided": (STEP, "gradient = np.moveaxis(ends[:, :, 0] - ends[:, :, 1], 1, 0)", "gradient = np.moveaxis(ends[:, :, 0] - a[:, None, :], 1, 0)"),
    "s8 gradient axes z y x": (STEP, "gradient = np.moveaxis(ends[:, :, 0] - ends[:, :, 1], 1, 0)", "gradient = np.moveaxis((ends[:, :, 0] - ends[:, :, 1])[:, ::-1], 1, 0)"),
    "s9 gradient sign turned": (STEP, "gradient = np.moveaxis(ends[:, :, 0] - ends[:, :, 1], 1, 0)", "gradient = np.moveaxis(ends[:, :, 1] - ends[:, :, 0], 1, 0)"),
    "s10 gradient halved by carry": (STEP, "gradient = np.moveaxis(ends[:, :, 0] - ends[:, :, 1], 1, 0)", "gradient = np.moveaxis(carry(ends[:, :, 0] - ends[:, :, 1], 1 + 1, 0)[0], 1, 0)"),
    "s11 spring on b": (STEP, "    force = pull(layout, s) - spring * a", "    force = pull(layout, s) - spring * s[1]"),
    "s12 J landing on 0*a gears from b": (STEP, "contract(plan, readings.reshape(-1, sites), a)", "contract(plan, readings.reshape(-1, sites), s[1])"),
    # the run back's reading
    "u1 untick sources at after a": (STEP, "sources(layout, State(choose(k, b, a), b, r, go, rd, ph, count, tn))", "sources(layout, State(a, b, r, go, rd, ph, count, tn))"),
    "u2 untick sources at after count": (STEP, "sources(layout, State(choose(k, b, a), b, r, go, rd, ph, count, tn))", "sources(layout, State(choose(k, b, a), b, r, go, rd, ph, c, tn))"),
    "u3 untick sources at before tn (equivalent?)": (STEP, "sources(layout, State(choose(k, b, a), b, r, go, rd, ph, count, tn))", "sources(layout, State(choose(k, b, a), b, r, go, rd, ph, count, before))"),
    "u4 untick sources with b at choose": (STEP, "sources(layout, State(choose(k, b, a), b, r, go, rd, ph, count, tn))", "sources(layout, State(choose(k, b, a), choose(k, b, a), r, go, rd, ph, count, tn))"),
    "u5 untick ungear W W": (STEP, "    a0, b0, r0 = ungear(a, b, r, go, w, wp,", "    a0, b0, r0 = ungear(a, b, r, go, w, w,"),
    # the mesh
    "m1 pull first row's grips for every row": (MESH, "* grip[:, meshes]).sum(axis=1)", "* grip[:1, meshes]).sum(axis=1)"),
    "m2 pull grips of the far end's Mesh": (MESH, "* grip[:, meshes]).sum(axis=1)", "* grip[:, meshes[[1, 0, 3, 2, 5, 4]]]).sum(axis=1)"),
    "m3 seen strict": (MESH, "nonneg(c[:, None, :] - tn[:, nb])", "nonneg(c[:, None, :] - tn[:, nb] - 1)"),
    "m4 seen slots swapped": (MESH, "a[:, nb], b[:, nb])", "b[:, nb], a[:, nb])"),
    "m5 due one early": (MESH, "nonneg(c[:, nb] - c[:, None, :])", "nonneg(c[:, nb] - c[:, None, :] + 1)"),
    # the records
    "r1 Gearing kick and drive names swapped": (STATE, "    kick: Z  # T_k, the kick's teeth: 1 on the force's path\n    drive: Z", "    drive: Z  # T_k, the kick's teeth: 1 on the force's path\n    kick: Z"),
    "r2 Gearing w and wp names swapped": (STATE, "    w: Z  # W, the teeth the impulse reads the stride at\n    wp: Z", "    wp: Z  # W, the teeth the impulse reads the stride at\n    w: Z"),
    "r3 Gearing stretch and spring names swapped": (STATE, "    stretch: Z  # s, the impulse's factor on the force and the kick: 1 on a gear's own teeth\n    spring: Z", "    spring: Z  # s\n    stretch: Z"),
    "r4 State rd and go names swapped": (STATE, "    go: Z\n    rd: Z", "    rd: Z\n    go: Z"),
    "r5 Plan first and second names swapped": (STATE, "    first: Z  # (terms,): the row of the readings that enters first\n    second: Z", "    second: Z  # (terms,): the row of the readings that enters first\n    first: Z"),
    # the contraction
    "c1 contract no accumulation": (CONTRACT, "    np.add.at(source, target, factor[:, None] * readings[first] * readings[second])", "    source[target] = factor[:, None] * readings[first] * readings[second]"),
    "c2 contract first twice": (CONTRACT, "readings[first] * readings[second])", "readings[first] * readings[first])"),
    # the load's indexing of the readings
    "l1 load pull at the z gradient's plane": (LOAD, "    plane = operand if operand < gradient else operand + d - 1\n", "    plane = operand if operand < gradient else operand + d - 1 - 1\n"),
    "l2 load gradient axes reversed": (LOAD, "(gradient + axis) * rows + train.row(kind, 0, part) for axis in range(d)", "(gradient + d - 1 - axis) * rows + train.row(kind, 0, part) for axis in range(d)"),
    "l3 load gradient reads component of part 0": (LOAD, "(gradient + axis) * rows + train.row(kind, 0, part) for axis in range(d)", "(gradient + axis) * rows + train.row(kind, 0, 0) for axis in range(d)"),
    "l4 load value and pull planes swapped": (LOAD, "    plane = operand if operand < gradient else operand + d - 1\n", "    plane = {0: d + 1, 2: 0}.get(operand, operand + d - 1)\n"),
    "l5 load pull plane one past (before's)": (LOAD, "    plane = operand if operand < gradient else operand + d - 1\n", "    plane = operand if operand < gradient else operand + d\n"),
}


def run(name, base, work):
    path, old, new = M[name]
    where = os.path.join(work, "".join(ch if ch.isalnum() else "_" for ch in name))
    shutil.rmtree(where, ignore_errors=True)
    shutil.copytree(base, where)
    target = os.path.join(where, path)
    text = open(target, encoding="utf-8").read()
    if text.count(old) != 1:
        return name, f"NOT APPLIED (found {text.count(old)})", ""
    open(target, "w", encoding="utf-8").write(text.replace(old, new))
    env = {**os.environ, "PYTHONPATH": os.path.join(where, "src"), "TMPDIR": "/dev/shm/tmp"}
    tests = sorted(
        os.path.join("tests", f)
        for f in os.listdir(os.path.join(where, "tests"))
        if f.startswith("test_the_tensor24_") and f.endswith(".py") and "decoder" not in f
    )
    done = subprocess.run(
        [sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *tests],
        cwd=where,
        env=env,
        capture_output=True,
        text=True,
    )
    shutil.rmtree(where, ignore_errors=True)
    lines = [x for x in done.stdout.splitlines() if x.startswith("FAILED") or "passed" in x or "failed" in x or "error" in x.lower()]
    return name, ("SURVIVES" if done.returncode == 0 else "killed"), " | ".join(lines[-2:])[:300]


def main():
    base, work, *names = sys.argv[1:]
    names = names or list(M)
    with ThreadPoolExecutor(4) as pool:
        for name, verdict, detail in pool.map(lambda n: run(n, base, work), names):
            print(f"{verdict:10} {name}: {detail}", flush=True)


main()
