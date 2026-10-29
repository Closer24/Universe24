"""Probe 3: source mutants of stage 6 that neither eighth/source_mutants.py nor ninth/new_mutants.py tried, aimed first at
the changed code (contract, plan, lay). Each runs in a scratch copy under /dev/shm/tmp/s11mut/<n> (src/ and tests/ whole,
the examples, the two tools, pyproject.toml) against every tests/test_the_tensor24_*.py (pytest -x) and
tools/tensor24_files.py on the examples; "control" applies no edit and must survive. SURVIVED: every test passes and the
tool exits 0. For a survivor, Sofer's gate (scribe_scan.scan) is run on the mutated file: "gate: +N" are its new hits.
usage: python3 -I mutants_s11.py <worktree>"""

import concurrent.futures as cf
import shutil
import subprocess
import sys
from pathlib import Path

WT = Path(sys.argv[1])
PY = "/home/user/Universe24/venv314/bin/python"
SCRATCH = Path("/dev/shm/tmp/s11mut")
K, M, L, C, F = (f"src/tensor24/{p}" for p in ("engine/kinds.py", "main.py", "runner/load.py", "engine/contract.py", "runner/files.py"))
ADD = "    np.add.at(source, target, factor[:, None] * readings[first] * readings[second])\n"
LAY = '        a, b, r, go = (np.zeros((rows, sites), dtype=object) for _ in ("a", "b", "r", "go"))\n'
MUTANTS = {
    "control (no edit)": [],
    # contract.py
    "S1 J added onto the gears (source = gears + 0)": [(C, "source = 0 * gears", "source = gears + 0")],
    "S2 J written into the caller's gears (source = gears)": [(C, "source = 0 * gears", "source = gears")],
    "S3 the source of int64": [(C, "source = 0 * gears", "source = np.zeros(gears.shape, dtype=np.int64)")],
    "S4 a buffered add (repeated landings collapse)": [(C, ADD, "    source[target] += factor[:, None] * readings[first] * readings[second]\n")],
    "S5 a plain write (the last term of a row wins)": [(C, ADD, "    source[target] = factor[:, None] * readings[first] * readings[second]\n")],
    "S6 the factor squared": [(C, "factor[:, None] * readings[first]", "factor[:, None] * factor[:, None] * readings[first]")],
    "S7 the second reading twice": [(C, "readings[first] * readings[second]", "readings[second] * readings[second]")],
    "S8 the landings reversed": [(C, "np.add.at(source, target, ", "np.add.at(source, target[::-1], ")],
    # load.py: the plan
    "S9 the landing column of object integers": [(L, "first_, second_, landing_ = (np.array(column, dtype=np.intp) for column in (first, second, landing))",
                                                  "first_, second_ = (np.array(column, dtype=np.intp) for column in (first, second))\n    landing_ = np.array(landing, dtype=object)")],
    "S10 the plan's factor of int64": [(L, "np.array(factor, dtype=object)", "np.array(factor, dtype=np.int64)")],
    "S11 the plan's two reading columns swapped": [(L, "return (first_, second_, np.array(factor", "return (second_, first_, np.array(factor")],
    "S12 the landing at the first side's part": [(L, "row(target_kind, x, target_part))", "row(target_kind, x, part))")],
    "S13 the landing at the first side's kind": [(L, "landing.append(trains[target].row(target_kind, x,", "landing.append(trains[target].row(kind, x,")],
    "S14 the table of the target train's first kind": [(L, "landed = trains[target].kinds[target_kind]", "landed = trains[target].kinds[0]")],
    "S15 the gradient's three axes on one plane": [(L, "(gradient + axis) * rows", "(gradient + 0 * axis) * rows")],
    "S16 the gradient reads its A1 at the axis's component": [(L, "train.row(kind, 0, part) for axis", "train.row(kind, axis, part) for axis")],
    "S17 the strides' refusal falls through (equivalent at the load)": [(L, "with the trains that step between an impulse and its carry\"\n            )\n            continue\n",
                                                                         "with the trains that step between an impulse and its carry\"\n            )\n")],
    # load.py: the lay
    "S18 the lay's five arrays of int64": [(L, LAY, LAY.replace("dtype=object", "dtype=np.int64")),
                                           (L, "clocks = np.zeros((1, sites), dtype=object)", "clocks = np.zeros((1, sites), dtype=np.int64)")],
    "S19 the going alone of int64": [(L, LAY, '        a, b, r = (np.zeros((rows, sites), dtype=object) for _ in ("a", "b", "r"))\n'
                                              "        go = np.zeros((rows, sites), dtype=np.int64)\n")],
    "S20 the clocks of int64": [(L, "clocks = np.zeros((1, sites), dtype=object)", "clocks = np.zeros((1, sites), dtype=np.int64)")],
    "S21 the lay's before at every site of its row": [(L, "a[row, site], b[row, site], r[row, site] = now, before, tooth", "a[row, site], b[row], r[row, site] = now, before, tooth")],
    "S22 the lay's bound read on the first train": [(L, "if component >= trains[train].rows():", "if component >= trains[0].rows():")],
    "S23 the three clocks one array (aliased) and the going a's": [(L, "return (a, b, r, go, clocks, clocks, clocks)", "return (a, b, r, go, clocks, clocks, clocks[:, :])")],
    # kinds.py
    "S24 det's first cofactor's minus turned": [(K, "a0 * (b1 * c2 - b2 * c1)", "a0 * (b1 * c2 + b2 * c1)")],
    "S25 the Spokes without their opposites": [(K, "spokes = np.concatenate((unit, -unit))", "spokes = np.concatenate((unit, unit))")],
    "S26 the tables' shape in the order (m, k, i)": [(L, "for n in (m, i, k))", "for n in (m, k, i))")],
    # files.py, the checker
    "S27 the sites the sum of the sides": [(F, "sites = sites * side", "sites = sites + side")],
    "S28 a gear's train one past": [(F, "0 <= train < trains and 0 <= site < sites", "0 <= train <= trains and 0 <= site < sites")],
    "S29 a gear's site from 1": [(F, "0 <= train < trains and 0 <= site < sites", "0 <= train < trains and 0 < site < sites")],
    "S30 a component below 0 passes": [(F, "if not (component >= 0 and tooth >= 0):", "if not (tooth >= 0):")],
    "S31 an empty trains list passes": [(F, "if found or not (isinstance(trains, list) and trains):", "if found or not isinstance(trains, list):")],
    "S32 a nesting too deep not caught": [(F, "except (OSError, ValueError, RecursionError) as error:", "except (OSError, ValueError) as error:")],
    "S33 the width unchecked inside lists": [(F, 'left += [(f"{where}[{at}]", item) for at, item in enumerate(value)]', "left += []")],
    "S34 a doubled key passes": [(F, "if len(held) < len(pairs):", "if len(held) < len(pairs) - 1:")],
}


def gate_delta(root, path):
    """The gate's new hits on the mutated file against the worktree's own."""
    code = ("import sys; sys.path[:0] = [sys.argv[1]]; import scribe_scan; from pathlib import Path; "
            "rel = sys.argv[3]; a = scribe_scan.scan(rel, Path(sys.argv[2]).read_text()); b = scribe_scan.scan(rel, Path(sys.argv[4]).read_text()); "
            "print(len(b) - len(a), sorted({(h.rule, h.detail) for h in b} - {(h.rule, h.detail) for h in a}))")
    out = subprocess.run([PY, "-I", "-c", code, str(WT / "tools/derivations/open_items"), str(WT / path), path.removeprefix("src/"), str(root / path)],
                         capture_output=True, text=True, timeout=120)
    return (out.stdout.strip() or out.stderr.strip().splitlines()[-1])[:150]


def run(item):
    n, (name, edits) = item
    root = SCRATCH / f"m{n:02d}"
    shutil.rmtree(root, ignore_errors=True)
    ignore = shutil.ignore_patterns("__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache")
    shutil.copytree(WT / "src", root / "src", ignore=ignore)
    shutil.copytree(WT / "tests", root / "tests", ignore=ignore)
    shutil.copytree(WT / "examples/tensor24", root / "examples/tensor24")
    (root / "tools").mkdir()
    for tool in ("tensor24_files.py", "tensor24_decode.py"):
        shutil.copy(WT / "tools" / tool, root / "tools" / tool)
    shutil.copy(WT / "pyproject.toml", root / "pyproject.toml")
    for path, old, new in edits:
        text = (root / path).read_text()
        if text.count(old) != 1:
            shutil.rmtree(root, ignore_errors=True)
            return name, f"NOT APPLIED ({text.count(old)} matches of {old!r})"
        (root / path).write_text(text.replace(old, new))
    env = {"PYTHONPATH": str(root / "src"), "TMPDIR": "/dev/shm/tmp", "PATH": "/usr/bin:/bin", "HOME": "/dev/shm/tmp"}
    tests = sorted(str(p.relative_to(root)) for p in (root / "tests").glob("test_the_tensor24_*.py"))
    t = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *tests], cwd=root, env=env,
                       capture_output=True, text=True, timeout=900)
    tool = subprocess.run([PY, "tools/tensor24_files.py"], cwd=root, env=env, capture_output=True, text=True, timeout=300)
    lines = [x for x in t.stdout.splitlines() if x.strip()]
    first_fail = next((x for x in lines if x.startswith("FAILED") or x.startswith("ERROR")), "")
    killed = t.returncode != 0 or tool.returncode != 0
    gate = "" if killed or not edits else "; gate: +" + "; ".join(gate_delta(root, p) for p in sorted({e[0] for e in edits}))
    shutil.rmtree(root, ignore_errors=True)
    return name, f"{'killed  ' if killed else 'SURVIVED'} tests: {(lines[-1:] or ['?'])[0][:48]}; tool exit {tool.returncode}; {first_fail[:100]}{gate}"


with cf.ThreadPoolExecutor(max_workers=4) as pool:
    results = dict(pool.map(run, enumerate(MUTANTS.items())))
for name in MUTANTS:
    print(f"{name:<62} {results[name]}")
print("survived (the control aside):", sum("SURVIVED" in results[n] for n in MUTANTS if n != "control (no edit)"), "of", len(MUTANTS) - 1)
