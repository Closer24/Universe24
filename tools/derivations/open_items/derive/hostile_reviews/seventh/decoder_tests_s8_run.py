"""Run the sketch decoder_tests_s8.py: part A and part B on the head, then part A with the decoder's own tests against
the new-text mutants of decoder_mutants_s8.py (the guard removals left out: the decoder's tests kill them already).

usage: python3 -I decoder_tests_s8_run.py <worktree> <scratch folder>   (PYTHONPATH unset)
"""

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import decoder_mutants_s8 as m  # noqa: E402

WT, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
m.WT, m.SCRATCH = WT, SCRATCH
SKETCH = "tests/decoder_tests_s8.py"


def tree_of(name, changes):
    tree = m.scratch(name, changes)
    shutil.copy(HERE / "decoder_tests_s8.py", tree / SKETCH)
    return tree


def pytest(tree, *args):
    got = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=tree,
                         capture_output=True, text=True)
    failed = [ln.split("::", 1)[-1] for ln in got.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))]
    return got.returncode, failed, (got.stdout.strip().splitlines() or [""])[-1]


head = tree_of("head", [])
code, failed, tail = pytest(head, SKETCH, "-k", "not required")
print(f"part A on the head: rc={code} {tail}")
code, failed, tail = pytest(head, SKETCH, "-k", "required")
print(f"part B on the head: rc={code} {tail}")
for f in failed:
    print(f"    fails on the head: {f.split(' - ')[0]}")
shutil.rmtree(head)

new_text = {k: v for k, v in m.MUTANTS.items() if not k.startswith("the guard ")}
survivors = []
for name, changes in new_text.items():
    tree = tree_of(name, changes)
    code, failed, tail = pytest(tree, m.TEST, SKETCH, "-k", "not required")
    print(f"{'SURVIVED' if code == 0 else 'killed  '} {name}" + (f"  <- {failed[0].split(' - ')[0]}" if failed else ""))
    survivors += [name] if code == 0 else []
    shutil.rmtree(tree)
print(f"{len(new_text)} new-text mutants against the decoder's tests and part A: {len(survivors)} survived")
