"""Source mutants of src/tensor24/decoder/{records,books,clocks}.py against tests/test_the_tensor24_decoder.py (pytest).

usage: python -I decoder_mutants.py <worktree> [test file in place of the committed one]
Each mutant is one or more textual changes in a scratch copy of src/tensor24 and the decoder's test under
/dev/shm/tmp/s6/decmut/<name>; SURVIVED means all 15 tests pass with it. Sofer's G1 to G3 are not re-reported:
the mutants here are of the readings' arithmetic, the verdict, the rate lines' reading and the causes named.
"""

import shutil
import subprocess
import sys
from pathlib import Path

PY = "/home/user/Universe24/venv314/bin/python"
SCRATCH = Path("/dev/shm/tmp/s6/decmut")
REC, BOOKS, CLOCKS = "src/tensor24/decoder/records.py", "src/tensor24/decoder/books.py", "src/tensor24/decoder/clocks.py"
CLOSES = 'return all(gained(p.get("taken", [])) + gained(p.get("laid", [])) == 0 for p in parts(click))'

MUTANTS = {
    # the first reading
    "the books close at any end, not every end": [(BOOKS, CLOSES, CLOSES.replace("return all(", "return any("))],
    "the books close over the two ends together, not at each": [
        (BOOKS, CLOSES, 'return sum(gained(p.get("taken", [])) + gained(p.get("laid", [])) for p in parts(click)) == 0')
    ],
    # the second reading
    "the windings moved read at the click alone, never at its ends": [
        (BOOKS, '    into: dict[int, int] = {}\n    for p in parts(click):', '    into: dict[int, int] = {}\n    for p in [click]:')
    ],
    "the round's clicks summed over every round (the round dropped)": [
        (BOOKS, 'into[(c["round"], train)] = into.get((c["round"], train), 0) + windings',
         'into[(0, train)] = into.get((0, train), 0) + windings'),
        (BOOKS, "agree += after - before == into.get((r, t), 0)", "agree += after - before == into.get((0, t), 0)"),
    ],
    "the ledger agreeing where its change is at least the clicks'": [
        (BOOKS, "agree += after - before == into.get((r, t), 0)", "agree += after - before >= into.get((r, t), 0)")
    ],
    # the verdict
    "SHOWN wherever the ledger agrees, the books open or not": [
        (BOOKS, 'kind = "SHOWN" if every and agree else "NOT SHOWN"', 'kind = "SHOWN" if agree else "NOT SHOWN"')
    ],
    "SHOWN wherever the record reads": [(BOOKS, 'kind = "SHOWN" if every and agree else "NOT SHOWN"', 'kind = "SHOWN"')],
    "the ledger absent read as an empty ledger": [
        (BOOKS, "    if ledger is None:\n", "    if ledger is None:\n        ledger = []\n    if ledger is None:\n")
    ],
    # the ticks
    "the rate lines read by the round (the schema's former line), not by the beat's count": [
        (CLOCKS, 'append((line["count"], line["k"]))', 'append((line["round"], line["k"]))')
    ],
    "the rate lines of every Node-clock read as one": [
        (CLOCKS, 'by_site.setdefault(line["site"], [])', 'by_site.setdefault(0, [])')
    ],
    # the causes named
    "the broken line named one line on": [(REC, "start=1) if line is None]", "start=1 + 1) if line is None]")],
    "the unplaced event named one line back": [(REC, "enumerate(events, start=1 + 1)", "enumerate(events, start=1)")],
    "the two causes of the major swapped": [
        (REC, 'return "the header holds no major version"', 'return f"the major version {major} is unknown"')
    ],
    "the order read by round and kind alone": [(REC, "return round_, KINDS.index(e[\"kind\"]), site, train", "return round_, KINDS.index(e[\"kind\"]), 0, 0")],
    "the kinds' order within a round changed (rate before turnover)": [
        (REC, 'KINDS = ("whole", "split", "turnover", "rate", "books")', 'KINDS = ("whole", "split", "rate", "turnover", "books")')
    ],
    "a line with no kind let through the first guard": [
        (REC, 'return line if isinstance(line, dict) and isinstance(line.get("kind"), str) else None',
         "return line if isinstance(line, dict) else None")
    ],
}


def run(name, changes):
    tree = SCRATCH / "".join(ch if ch.isalnum() else "_" for ch in name)[:80]
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(WT / "src" / "tensor24", tree / "src" / "tensor24", ignore=shutil.ignore_patterns("__pycache__"))
    (tree / "tests").mkdir()
    shutil.copy(WT / "tests" / "__init__.py", tree / "tests" / "__init__.py")
    shutil.copy(TEST, tree / "tests" / "test_the_tensor24_decoder.py")
    (tree / "pytest.ini").write_text("[pytest]\naddopts = --import-mode=importlib\npythonpath = src\n")
    for rel, old, new in changes:
        path = tree / rel
        text = path.read_text()
        assert text.count(old) == 1, (name, old)
        path.write_text(text.replace(old, new))
    got = subprocess.run(
        [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_the_tensor24_decoder.py"],
        cwd=tree, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin", "TMPDIR": "/dev/shm/tmp"},
    )
    failed = [ln.split("::", 1)[1] for ln in got.stdout.splitlines() if ln.startswith("FAILED")]
    shutil.rmtree(tree)
    return got.returncode, failed, (got.stdout.strip().splitlines() or [""])[-1]


if __name__ == "__main__":
    WT = Path(sys.argv[1]).resolve()
    TEST = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else WT / "tests" / "test_the_tensor24_decoder.py"
    code, failed, tail = run("unmutated", [])
    print(f"unmutated: rc={code} {tail}")
    assert code == 0, failed
    survivors = []
    for name, changes in MUTANTS.items():
        code, failed, tail = run(name, changes)
        print(f"{'SURVIVED' if code == 0 else 'killed  '} {name}" + (f"  <- {'; '.join(f.split(' - ')[0] for f in failed)[:300]}" if code else ""))
        survivors += [name] if code == 0 else []
    print(f"{len(MUTANTS)} mutants, {len(survivors)} survived")
