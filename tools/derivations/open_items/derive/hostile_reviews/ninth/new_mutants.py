"""Probe: source mutants of stage 6 the eighth reader did not write (kinds.py, contract.py, load.py, files.py, main.py).

Each runs in a scratch copy under /dev/shm/tmp/s10mut/<n> (src/ and tests/ whole, the examples, the two tools, pyproject.toml)
against every tests/test_the_tensor24_*.py (pytest -x) and tools/tensor24_files.py on the examples. "control" applies no
edit and must survive, so a copy that cannot run never counts as a kill. SURVIVED: every test passes, the tool exits 0.
usage: python3 -I new_mutants.py <worktree>"""

import concurrent.futures as cf
import shutil
import subprocess
import sys
from pathlib import Path

WT = Path(sys.argv[1])
PY = "/home/user/Universe24/venv314/bin/python"
SCRATCH = Path("/dev/shm/tmp/s10mut")
K, M, L, C, F = (f"src/tensor24/{p}" for p in ("engine/kinds.py", "main.py", "runner/load.py", "engine/contract.py", "runner/files.py"))
MUTANTS = {
    "control (no edit)": [],
    # load.py
    "N1 the lay drops the fine tooth (r stays 0)": [(L, "a[row, site], b[row, site], r[row, site] = now, before, tooth", "a[row, site], b[row, site] = now, before")],
    "N2 the clocks of one site": [(L, "clocks = np.zeros((1, sites), dtype=object)", "clocks = np.zeros((1, 1), dtype=object)")],
    "N3 the gradient read at its train's first kind": [(L, "rows + train.row(kind, 0, part) for axis", "rows + train.row(0, 0, part) for axis")],
    "N4 the gradient's A1 rule reads its train's first kind": [(L, 'labels[trains[t].kinds[k]] != "A1"', 'labels[trains[t].kinds[0]] != "A1"')],
    "N5 a train's first row after the earlier trains' kinds, the part ignored": [(L, "held[-1].first + held[-1].rows() if held", "held[-1].first + sum(held[-1].dims) if held")],
    "N6 the lay's guard without MemoryError": [(L, "except (ValueError, MemoryError) as error:", "except ValueError as error:")],
    "N7 the couplings by key (91226e796 undone)": [(L, 'universe.get("couplings", [])', 'universe["couplings"]')],
    "N8 the gears by key (91226e796 undone)": [(L, 'setting.get("gears", [])', 'setting["gears"]')],
    "N9 the two sides' readings swapped": [(L, "(a, ones), (b, twos) = (side(", "(b, twos), (a, ones) = (side(")],
    "N10 the table's entry read with its two inputs transposed": [(L, "strength * table[x, y, z]", "strength * table[x, z, y] if table.shape[1] == table.shape[2] else strength * table[x, y, z]")],
    # kinds.py and main.py
    "K9 the axes of int64, not Python integers": [(K, "return np.eye(d, dtype=object)", "return np.eye(d, dtype=np.int64)")],
    "K10 the projector's two read slots swapped in C": [(K, '"g,gxy,gpa,gqb->xabypq"', '"g,gxy,gpa,gqb->xbaypq"')],
    "K11 det's middle cofactor's sign turned": [(K, "- a1 * (b0 * c2 - b2 * c0)", "+ a1 * (b0 * c2 - b2 * c0)")],
    "M2 main.made returns the inverse's kinds": [(M, "    return held, load.tables(", "    return kinds.kinds(kinds.inverse(matrix)), load.tables(")],
    # files.py, the checker
    "F18 a row of more fields than the format's": [(F, "len(row) == len(fields)", "len(row) >= len(fields)")],
    "F19 a truth value read as whole": [(F, "return isinstance(value, int) and not isinstance(value, bool)", "return isinstance(value, int)")],
    "F20 ticks from 1": [(F, 'setting["ticks"] >= 0', 'setting["ticks"] >= 1')],
    "F21 a gear given twice passes": [(F, "given[(train, component, site)] > 1:", "given[(train, component, site)] > 1 + 1:")],
    "F22 a site one past": [(F, "0 <= site < sites", "0 <= site <= sites")],
    "F23 a side of 0": [(F, "all(whole(s) and s >= 1 for s in shape)", "all(whole(s) and s >= 0 for s in shape)")],
    "F24 an integer of 0": [(F, "whole(integers.get(name)) and integers.get(name) >= 1", "whole(integers.get(name)) and integers.get(name) >= 0")],
    "F25 the width one bit short": [(F, "if n.bit_length() > width", "if n.bit_length() >= width")],
    "F26 a part of 0": [(F, "whole(part) and part >= 1", "whole(part) and part >= 0")],
    "F27 a label doubled passes": [(F, "if count > 1", "if count > 1 + 1")],
    "F28 a later version passes": [(F, "whole(version) and version == VERSION", "whole(version) and version >= VERSION")],
    "F29 a fine tooth below 0 passes": [(F, "component >= 0 and tooth >= 0", "component >= 0")],
    "F30 an empty name passes": [(F, "isinstance(name, str) and name)", "isinstance(name, str))")],
    "F31 an empty kinds list passes": [(F, "isinstance(kinds, list) and kinds and all(", "isinstance(kinds, list) and all(")],
    "F32 a weight not whole passes": [(F, 'if "weight" in train and not whole(train["weight"]):', 'if "weight" in train and not isinstance(train["weight"], (int, float)):')],
}


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
    shutil.rmtree(root, ignore_errors=True)
    return name, f"{'killed  ' if killed else 'SURVIVED'} tests: {(lines[-1:] or ['?'])[0][:60]}; tool exit {tool.returncode}; {first_fail[:110]}"


with cf.ThreadPoolExecutor(max_workers=4) as pool:
    results = dict(pool.map(run, enumerate(MUTANTS.items())))
for name in MUTANTS:
    print(f"{results[name]:<200} {name}")
print("survived (the control aside):", sum("SURVIVED" in results[n] for n in MUTANTS if n != "control (no edit)"), "of", len(MUTANTS) - 1)
