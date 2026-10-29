"""Probe 6: source mutants of kinds.py, main.py, load.py, contract.py and the checker (files.py), the eighth review's (its M1 updated for kinds(matrix), L17 and C1 for the ninth's changes), each in a
scratch copy under /dev/shm/tmp/s9mut/<n>, run against tests/test_the_tensor24_{kinds,load,files}.py (pytest -x) and
tools/tensor24_files.py on the examples. SURVIVED: every test passes and the tool exits 0 with the mutant in place.
usage: python3 -I source_mutants.py <worktree>"""
import concurrent.futures as cf, shutil, subprocess, sys
from pathlib import Path

WT = Path(sys.argv[1]); PY = "/home/user/Universe24/venv314/bin/python"; SCRATCH = Path("/dev/shm/tmp/s9mut")
K, M, L, C, F = (f"src/tensor24/{p}" for p in ("engine/kinds.py", "main.py", "runner/load.py", "engine/contract.py", "runner/files.py"))
T1_CYCLED = ("    cyc = np.stack((e2, e3, e1))\n    t1 = np.einsum(\"ij,gjk,lk->gil\", cyc, matrix, cyc)\n"
             "    return Kinds(0 * sign + 1, sign, e, t1, sign * t1)")
MUTANTS = {
    "K1 E's reading (e1, e2)": [(K, "reading = np.stack((e1, e1 + e2))", "reading = np.stack((e1, e2))")],
    "K2 E's plane (e1 - e2, e1 - e3)": [(K, "np.stack((e1 - e2, e2 - e3), axis=1)", "np.stack((e1 - e2, e1 - e3), axis=1)")],
    "K3 T1 (and T2) conjugated by the 3-cycle of the axes": [(K, "    return Kinds(0 * sign + 1, sign, e, matrix, sign * matrix)", T1_CYCLED)],
    "K4 A2 the turn's own determinant": [(K, "sign = det(permutation)[:, None, None]", "sign = det(matrix)[:, None, None]")],
    "K5 projector reads the inverse kinds transposed": [(K, '"g,gxy,gpa,gqb->xabypq"', '"g,gxy,gap,gbq->xabypq"')],
    "K6 kinds.inverse the turn itself": [(K, "return np.swapaxes(matrix, 1, 1 + 1)", "return matrix + 0")],
    "K7 the 48 weighed in": [(K, "weight, _ = carry(turn + turn * turn, 1 + 1, 0)", "weight = turn * turn")],
    "K8 E in the other equivalent basis (an E basis choice)": [
        (K, "np.stack((e1 - e2, e2 - e3), axis=1)", "np.stack((e2 - e3, e1 - e2), axis=1)"),
        (K, "reading = np.stack((e1, e1 + e2))", "reading = np.stack((e1 + e2, e1))")],
    "M1 main.made passes the turns as their own inverses": [(M, "kinds.kinds(kinds.inverse(matrix))", "kinds.kinds(matrix)")],
    "L1 the last seed not 0 (equivalent since the sign is fixed)": [(L, "for seed in seeds if seed.any()", "for seed in seeds[::-1] if seed.any()")],
    "L2 the sign by the last entry": [(L, "next(x for x in q if x) > 0", "next(x for x in q[::-1] if x) > 0")],
    "L3 the gcd without abs": [(L, "a, b = abs(value), g", "a, b = value, g")],
    "L4 Train.row with the part slowest": [(L, "return self.first + (sum(self.dims[:kind]) + component) * self.part + part",
                                            "return self.first + part * sum(self.dims) + sum(self.dims[:kind]) + component")],
    "L5 lay ignores the train's first row": [(L, "row = trains[train].first + component", "row = component")],
    "L6 lay's bound one past": [(L, "if component >= trains[train].rows():", "if component > trains[train].rows():")],
    "L7 the pull's plane one on": [(L, "else operand + d - 1", "else operand + d")],
    "L8 the gradient read at part 0": [(L, "rows + train.row(kind, 0, part) for axis", "rows + train.row(kind, 0, 0) for axis")],
    "L9 the gradient's A1 rule on the first side alone": [(L, "for t, k, _, o in sides)", "for t, k, _, o in sides[:1])")],
    "L10 the strides on the first side alone": [(L, "{OPERANDS[operand], OPERANDS[with_operand]} & {", "{OPERANDS[operand]} & {")],
    "L11 a forbidden channel not named": [(L, "        if not table.any():", "        if table.size < 0:")],
    "L12 the landing at part 0": [(L, "row(target_kind, x, target_part)", "row(target_kind, x, 0)")],
    "L13 the table's sign dropped from the factor": [(L, "strength * table[x, y, z]", "strength * abs(table[x, y, z])")],
    "L14 a part of 3 loads": [(L, 'not in (1, 1 + 1):', 'not in (1, 1 + 1, 1 + 1 + 1):')],
    "L15 E loads": [(L, 'elif label == "E":', 'elif label == "E?":')],
    "L16 lay swaps before and the tooth": [(L, "= now, before, tooth", "= now, tooth, before")],
    "L17 lay's going at 1, not 0": [(L, "return (a, b, r, go, clocks", "return (a, b, r, go + 1, clocks")],
    "L18 promises' tooth bound one past": [(L, "(r < 0) | (r >= w)", "(r < 0) | (r > w)")],
    "L19 promises' rate bound one past the full rate": [(L, "(rate < 0) | (rate > gamma)", "(rate < 0) | (rate > gamma + 1)")],
    "L20 promises' rate floor one below": [(L, "(rate < 0) | (rate > gamma)", "(rate < 0 - 1) | (rate > gamma)")],
    "C1 the factor dropped": [(C, "factor[:, None] * readings[first]", "readings[first]")],
    "C2 the second reading as the first": [(C, "readings[first] * readings[second]", "readings[first] * readings[first]")],
    "F1 a pinion below den only": [(F, "whole(pinion) and 0 <= pinion <= den", "whole(pinion) and 0 <= pinion < den")],
    "F2 a pinion above 0 only": [(F, "whole(pinion) and 0 <= pinion <= den", "whole(pinion) and 0 < pinion <= den")],
    "F3 a hand from part 3": [(F, 'train["part"] > 1)', 'train["part"] > 1 + 1)')],
    "F4 a sine below den only": [(F, "whole(other) and 0 <= other <= den", "whole(other) and 0 <= other < den")],
    "F5 a sine above 0 only": [(F, "whole(other) and 0 <= other <= den", "whole(other) and 0 < other <= den")],
    "F6 the norm at most den den": [(F, "if norm == den * den", "if norm <= den * den")],
    "F7 a kind one past": [(F, '0 <= kind < len(trains[train]["kinds"])', '0 <= kind <= len(trains[train]["kinds"])')],
    "F8 a kind from 1 (the floor moved by one)": [(F, '0 <= kind < len(trains[train]["kinds"])', '0 < kind < len(trains[train]["kinds"])')],
    "F9 a part one past": [(F, '0 <= part < trains[train]["part"]', '0 <= part <= trains[train]["part"]')],
    "F10 an operand one past": [(F, "0 <= operand < len(OPERANDS)", "0 <= operand <= len(OPERANDS)")],
    "F11 the second side's kind read as the first's": [(F, "(with_train, with_kind, with_part, with_operand),", "(with_train, kind, with_part, with_operand),")],
    "F12 the target's kind read as the first's": [(F, "(target, target_kind, target_part, 0),", "(target, kind, target_part, 0),")],
    "F13 the target's part read as the first's": [(F, "(target, target_kind, target_part, 0),", "(target, target_kind, part, 0),")],
    "F14 a train one past": [(F, "0 <= train < len(trains) for train, _, _, _ in sides", "0 <= train <= len(trains) for train, _, _, _ in sides")],
    "F15 the norm's sine not squared": [(F, "norm = pinion * pinion + other * other", "norm = pinion * pinion + other")],
    "F16 a sine allowed on one gear": [(F, '[] if other is None else [f"{where}.{second}: none on a train of one gear, not {other!r}"]', "[]")],
    "F17 the second operand unchecked": [(F, "for _, _, _, operand in sides)", "for _, _, _, operand in sides[::2])")],
}
TESTS = ["tests/test_the_tensor24_kinds.py", "tests/test_the_tensor24_load.py", "tests/test_the_tensor24_files.py"]

def run(item):
    n, (name, edits) = item
    root = SCRATCH / f"m{n:02d}"
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(WT / "src/tensor24", root / "src/tensor24", ignore=shutil.ignore_patterns("__pycache__"))
    (root / "tests").mkdir(parents=True)
    for t in ["tests/__init__.py", "tests/frame.py", *TESTS]:
        shutil.copy(WT / t, root / t)
    shutil.copy(WT / "pyproject.toml", root / "pyproject.toml")
    shutil.copytree(WT / "examples/tensor24", root / "examples/tensor24")
    (root / "tools").mkdir()
    shutil.copy(WT / "tools/tensor24_files.py", root / "tools/tensor24_files.py")
    for path, old, new in edits:
        text = (root / path).read_text()
        if text.count(old) != 1:
            return name, f"NOT APPLIED ({text.count(old)} matches of {old!r})"
        (root / path).write_text(text.replace(old, new))
    env = {"PYTHONPATH": str(root / "src"), "TMPDIR": "/dev/shm/tmp", "PATH": "/usr/bin:/bin"}
    t = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *TESTS], cwd=root, env=env,
                       capture_output=True, text=True, timeout=600)
    tool = subprocess.run([PY, "tools/tensor24_files.py"], cwd=root, env=env, capture_output=True, text=True, timeout=300)
    last = [l for l in t.stdout.splitlines() if l.strip()][-1:] or ["?"]
    killed = t.returncode != 0 or tool.returncode != 0
    shutil.rmtree(root, ignore_errors=True)
    return name, f"{'killed  ' if killed else 'SURVIVED'} tests: {last[0][:90]}; tool exit {tool.returncode}"

with cf.ThreadPoolExecutor(max_workers=8) as pool:
    results = dict(pool.map(run, enumerate(MUTANTS.items())))
for name in MUTANTS:
    print(f"{results[name]:<130} {name}")
print("survived:", sum("SURVIVED" in v for v in results.values()), "of", len(MUTANTS))
