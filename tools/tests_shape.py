"""The shape of tests/, held against the merge base (issue #1211; the model owner, 2026-09-27: the bulk must not come back).

Every count is compared with the same count at the merge base (CHECK_BASE, else origin/main),
read from git, so no baseline file is kept: a pull request may lower a count, never raise it.

(a) Size. tests/ holds no more lines than at the merge base: it only shrinks, and a pull
    request that adds tests offsets them by deletions (the model owner, 2026-09-27); a test
    file above 600 lines holds no more than at the merge base, and a new one stays under.
    A test the Boss gives room by name (ROOM: the test, its lines and the reason, recorded
    here and in ENGINE.md section 9) adds that room to the base's size while it stands with
    at most those lines; nothing else grows the budget. A file the Boss gives a budget (ROOM:
    the file alone, its lines and the reason; the owner's word of 2026-10-29, 02:5x UTC) takes
    room as a test does, grows within it with no new entry, and is refused above it.
(b) Copied setup. No test module imports another `test_*.py`: shared builders live in
    `tests/frame.py`. A function of 8 lines or more whose abstracted
    body appears twice across tests/ is refused beyond the merge base's groups.
(c) History. Across tests/, the docstring and comment lines that carry a history marker, and
    the docstrings beyond three lines, stay at or below the merge base's (a moved helper moves
    its count with it).
(d) Retired code. Across tests/, the module-wide skips and the skips that name cancelled or
    retired code stay at or below the merge base's; a public function of `src/` that
    nothing in `src/`, `tools/` or `examples/` names is refused unless the merge base has it.
"""

from __future__ import annotations

import ast
import hashlib
import io
import re
import subprocess
import sys
import tokenize
from pathlib import Path

import merge_base
from record_code_shape import Abstracted, docstring_of

ROOT = Path(__file__).resolve().parents[1]
FILE_LINES = 600
DUPLICATE_LINES = 8
DOCSTRING_LINES = 3
HISTORY = re.compile(r"\b(?:SINCE|HISTORY|BUILD\.md|[Ss]uperseded|[Pp]reviously|[Rr]ecords? \d{3,})\b")
RETIRED = re.compile(r"CANCELLED|[Rr]etired")
TENSOR24_FRAME = "Tensor24's frame, stage 0 of the build the owner approved at 16:0x UTC on 2026-10-28 (\"Approved, build it. You on the engine. Animate on the decoder.\"): the property tests of the plan's section 13 (locality in the stencil form, purity across two worlds and across fresh interpreters at other hash seeds, rename with an inert train, the 24's images with the translations, the formula against a naive model, the run back by a fresh engine and in a fresh interpreter that never stepped) for any engine, on a trivial engine at three seeds of Python integers whose every bit is drawn across 2**256 on a side of 5, each failing on every mutant it must catch.; on the trivial engine two tests, every mutant kept, on the owner's word of 2026-10-30, 09:2x UTC (\"what is generic, test only it, and then the whole\")."
TENSOR24_DECODER_BANGS = "Tensor24's decoder's third test file, Animate's, its budget on Animate's word under decision 26: row 46, each later bang shows more, on the owner's word to Animate of 06:3x UTC on 2026-10-29 (\"ever more complex clocks\"): the bangs read from the load at the load's bottoms, each bang's click kinds and the deepest clock its clicks lay against the deepest clock the ledger holds at its end, a bang that shows no more and a held clock that falls named, every frame the row cannot read named, nothing raised, each failing on its own mutant."
TENSOR24_DECODER_MEASURE = "Tensor24's decoder's fourth test file, Animate's, its budget on Animate's word under decision 26: the measurement's rules (the Boss's D6 to D8; decision 40's N5, records built in memory): the cone check by click, each take's and refusal's outcome binned by the frames of its lay's settings outside its past cone, proper time read twice through one beat, the twin reading, and a duration only as a clock's own count, every frame a rule cannot read named, nothing raised, each failing on its own mutant."
TENSOR24_FILES = "Tensor24's three files, stage 0 of the build the owner approved at 16:0x UTC on 2026-10-28: the examples hold under the files' checker (whole numbers alone, the integers and the sides at least 1, every reference whole, every integer within the width), each of its rules refuses its own broken file by name, and a file at a rule's edge holds, every key it requires absent and every key it lets a file leave out given as null (the fourteenth hostile review).; two tests, every case kept, on the owner's word of 2026-10-30, 09:2x UTC (\"what is generic, test only it, and then the whole\")."
TENSOR24_ROOM = "Tensor24's room by file (decision 26), the fourteenth hostile review's required change: the room a push may take is the head's budgets less the base's, so a test with no budget is refused beside budgets the base already holds."
TENSOR24_GENERIC = "Tensor24's generic node, G0 and G1 of decision 40 (the owner's words of 2026-10-29, 15:0x UTC: \"Start ... Finish a generic engine\"): the loaded board's rows geared by one formula of their own numbers, the clock's own gear among them and every row reading its teeth from it, no record that names a row apart, the file's order of its trains nothing to the run, and the loaded act alike under the 24 turns and the translations.; the time gear's one loaded round against the naive round that reads each square's 00 and ii slots by name folded in, the other clock tests read by the engine's parts, on the owner's word of 2026-10-30, 09:2x UTC (\"what is generic, test only it, and then the whole\")."
TENSOR24_RUN = "Tensor24's runner, stage 10 brought before stages 8 and 9 on the owner's word of 2026-10-29, 06:3x UTC (decision 27): the three files run to a record the decoder reads, the files verbatim with their digests, every Node-clock in every round with no rate line, the ledger beside it holding every train's counts at every Node-clock and round as the engine's rounds reach them, the end's digest the state the rounds reach and its run back read 0 where the run back misses, a departing file or a broken promise named with no record written, and the tool.; the record schema's leaves folded in, two tests, on the owner's word of 2026-10-30, 09:2x UTC (\"what is generic, test only it, and then the whole\")."
TENSOR24_ALGEBRA = "Tensor24's algebra, stage 1 of the build the owner approved at 16:0x UTC on 2026-10-28: Rule3's carry and the fine tooth's flip, each law failing on its own mutant, the tie rule's negated quotient and flipped tooth among them.; the Gaussian ring's laws (stage 5: the hand's product, conjugate, norm and pair, the twin hand's overlap, reverse and axis, Lagrange's identity, S . S = rho rho) folded in as the algebra's second test on the owner's word of 2026-10-30, 09:2x UTC (\"what is generic, test only it, and then the whole\")."
TENSOR24_KINDS = "Tensor24's kinds and tables, stage 6 of the build the owner approved at 16:0x UTC on 2026-10-28: the 24 a group of the Spokes' threefold power, each of the five kinds a representation, their characters Sofer's by his definitions at every turn and his table on every class, every table C equivariant and 0 exactly where David's products hold no channel, primitive, the dot, the cross and A2 x T1 -> T2 exactly, each law failing on its own mutant.; one test of the laws and every mutant, on the owner's word of 2026-10-30, 09:2x UTC (\"what is generic, test only it, and then the whole\")."
TENSOR24_LOAD = "Tensor24's load, stage 6 of the build the owner approved at 16:0x UTC on 2026-10-28: each refusal of the load naming its own broken file with its edge that loads, the four-vector's square found by its kinds' character alone in every order of them, the promise named where it fails and shown to be the run back's own condition, a gear laid on the first train's rows and at the last train's last component past 64 bits, no term of J where no file declares a coupling, and no raise on the files the checker holds nor on a board the machine's memory refuses.; two tests on the owner's word of 2026-10-30, 09:2x UTC (\"what is generic, test only it, and then the whole\")."
TENSOR24_ENGINE = "Tensor24's engine, stages 2 to 7a of the build the owner approved at 16:0x UTC on 2026-10-28, the four stages' tests merged into one on his word of 2026-10-29, 02:5x UTC (decision 26): every Node-clock in every round (G1b of decision 40), the board's neighbours and Meshes and the one-Mesh reach both ways, the one act at its coefficients against one naive model, the run back as the act on the mirrored state at every divisor of at least 2, the tie rule, the sources' images under the 24, the frame's properties on the act, a hand's charge moving by Rule3's torques and its kick alone, and the engine's records' fields pinned, each law failing on its own mutant.; one test per generic part on the owner's word of 2026-10-30, 09:2x UTC (\"what is generic, test only it, and then the whole\"): J by the vertex law against its potential alone (the spring's mutants, term 6's phenomena leaving the suite), the board and its Meshes, the act at its coefficients, the run back, and the whole node with the fresh interpreters once."
TENSOR24_DECODER = "Tensor24's decoder, Animate's, on the build the owner approved at 16:0x UTC on 2026-10-28 (\"Approved, build it. You on the engine. Animate on the decoder.\"): every reading of the click record against the plan and the schema, NOT READ with its cause where the record cannot support it, NOT SHOWN where it fails, the tool naming every cause it meets and raising on none, each test failing on its own mutant."
TENSOR24_DECODER_CASES = "Tensor24's decoder's second test file, Animate's, on the build the owner approved at 16:0x UTC on 2026-10-28, its budget on Animate's word under decision 26 (the Boss's 6487025699 on #2187: a second file for the new tests takes its own budget on your word): the twelfth hostile review's cases, each read as the plan, the schema and the decoder's own comments say and nothing raised (the values read where the line's record names them, the names in ASCII, the board by its sides, the books per train, the verdict's order with the gap named beside the open books, the ticks at count 0, the tool over clicks at two Node-clocks), each failing on the reader's mutant it was written for."
ROOM = {  # the room given by name: the test or the file, its lines and the reason (ENGINE.md, section 9)
    "tests/frame.py": (300, TENSOR24_FRAME),
    "tests/test_the_tensor24_engine.py": (575, TENSOR24_ENGINE),
    "tests/test_the_tensor24_algebra.py": (215, TENSOR24_ALGEBRA),
    "tests/test_the_tensor24_decoder.py": (600, TENSOR24_DECODER),
    "tests/test_the_tensor24_decoder_cases.py": (350, TENSOR24_DECODER_CASES),
    "tests/test_the_tensor24_decoder_bangs.py": (200, TENSOR24_DECODER_BANGS),
    "tests/test_the_tensor24_decoder_measure.py": (250, TENSOR24_DECODER_MEASURE),
    "tests/test_the_tensor24_files.py": (315, TENSOR24_FILES),
    "tests/test_the_tensor24_room.py": (50, TENSOR24_ROOM),
    "tests/test_the_tensor24_run.py": (160, TENSOR24_RUN),
    "tests/test_the_tensor24_generic.py": (205, TENSOR24_GENERIC),
    "tests/test_the_tensor24_frame.py": (240, TENSOR24_FRAME),
    "tests/test_the_tensor24_kinds.py": (325, TENSOR24_KINDS),
    "tests/test_the_tensor24_load.py": (185, TENSOR24_LOAD),
}
CALLERS = ("src/", "tools/", "examples/")

Snapshot = dict[str, str]


def working_tree(root: Path) -> Snapshot:
    """Every Python file of src/, tools/, examples/ and tests/ in the working tree."""
    found: Snapshot = {}
    for folder in ("src", "tools", "examples", "tests"):
        for path in sorted((root / folder).rglob("*.py")):
            found[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8")
    return found


def at_ref(root: Path, ref: str) -> Snapshot | None:
    """The same files at `ref`, or None where git cannot show it."""
    try:
        names = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", ref, "--", "src", "tools", "examples", "tests"],
            capture_output=True,
            text=True,
            cwd=root,
            check=True,
        ).stdout.split()
        names = [name for name in names if name.endswith(".py")]
        batch = subprocess.run(
            ["git", "cat-file", "--batch"],
            input="".join(f"{ref}:{name}\n" for name in names).encode(),
            capture_output=True,
            cwd=root,
            check=True,
        ).stdout
    except OSError, subprocess.CalledProcessError:
        return None
    found: Snapshot = {}
    offset = 0
    for name in names:
        header_end = batch.index(b"\n", offset)
        size = int(batch[offset:header_end].split()[2])
        found[name] = batch[header_end + 1 : header_end + 1 + size].decode("utf-8")
        offset = header_end + 1 + size + 1
    return found


def tests_of(snapshot: Snapshot) -> Snapshot:
    return {name: text for name, text in snapshot.items() if name.startswith("tests/")}


def lines_in(snapshot: Snapshot, folder: str) -> int:
    return sum(len(text.splitlines()) for name, text in snapshot.items() if name.startswith(folder))


def file_counts(text: str) -> dict[str, int]:
    """Per test file: its lines, history-marked lines, long docstrings and retirement skips."""
    tree = ast.parse(text)
    marked: set[int] = set()
    long_docstrings = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            doc = docstring_of(node)
            if doc is not None:
                end = doc.end_lineno or doc.lineno
                long_docstrings += end - doc.lineno + 1 > DOCSTRING_LINES
                source = text.splitlines()[doc.lineno - 1 : end]
                marked.update(doc.lineno + i for i, line in enumerate(source) if HISTORY.search(line))
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type == tokenize.COMMENT and HISTORY.search(token.string):
            marked.add(token.start[0])
    skip_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets
        ):
            if "skip" in ast.unparse(node.value):
                skip_lines.add(node.lineno)
        elif isinstance(node, ast.Call) and "skip" in ast.unparse(node.func):
            if RETIRED.search(ast.unparse(node)):
                skip_lines.add(node.lineno)
    skips = len(skip_lines)
    return {
        "lines": len(text.splitlines()),
        "history_lines": len(marked),
        "long_docstrings": long_docstrings,
        "retirement_skips": skips,
    }


def test_imports(snapshot: Snapshot) -> list[str]:
    """Every import of a `test_*.py` module by another test file."""
    found = []
    for name, text in tests_of(snapshot).items():
        for node in ast.walk(ast.parse(text)):
            module = node.module if isinstance(node, ast.ImportFrom) else None
            modules = [a.name for a in node.names] if isinstance(node, ast.Import) else [module or ""]
            for imported in modules:
                if imported.split(".")[-1].startswith("test_"):
                    found.append(f"{name} imports {imported}: move the helper to tests/frame.py")
    return found


def duplicate_groups(snapshot: Snapshot) -> dict[str, list[str]]:
    """Every abstracted body of a function of 8 lines or more that appears twice across tests/."""
    groups: dict[str, list[str]] = {}
    for name, text in tests_of(snapshot).items():
        for node in ast.walk(ast.parse(text)):
            if (
                isinstance(node, ast.FunctionDef)
                and (node.end_lineno or node.lineno) - node.lineno + 1 >= DUPLICATE_LINES
            ):
                copy = ast.parse(ast.unparse(node)).body[0]
                digest = hashlib.sha256(ast.dump(Abstracted().visit(copy)).encode()).hexdigest()[:16]
                groups.setdefault(digest, []).append(f"{name}:{node.name}")
    return {digest: sorted(names) for digest, names in groups.items() if len(names) > 1}


def uncalled(snapshot: Snapshot) -> set[str]:
    """The public top-level functions of src/ that nothing else names."""
    callers = "\n".join(text for name, text in snapshot.items() if name.startswith(CALLERS))
    found = set()
    for name, text in snapshot.items():
        if not name.startswith("src/"):
            continue
        for node in ast.parse(text).body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                if len(re.findall(rf"\b{node.name}\b", callers)) <= 1:
                    found.add(f"{name}:{node.name}")
    return found


def room_of(snapshot: Snapshot) -> int:
    """The room the named tests take in a snapshot: per ROOM entry whose test stands in its file, the fewer of its named lines and the test's own (the def through its last line), so a test keeps its room only while it holds it; 0 for a test that is gone. An entry that names a file alone is the file's budget, and the file takes the fewer of it and its own lines."""
    found = 0
    for name, (lines, _reason) in ROOM.items():
        path, _, function = name.partition("::")
        if path not in snapshot:
            continue
        if not function:
            found += min(lines, len(snapshot[path].splitlines()))
            continue
        for node in ast.walk(ast.parse(snapshot[path])):
            if isinstance(node, ast.FunctionDef) and node.name == function and node.end_lineno:
                found += min(lines, node.end_lineno - node.lineno + 1)
    return found


def over_budget(snapshot: Snapshot) -> list[str]:
    """Every file above the budget its ROOM entry gives it."""
    return [
        f"{name} has {len(snapshot[name].splitlines())} lines, above its budget of {lines}; raise the budget with its reason, or cut"
        for name, (lines, _reason) in ROOM.items()
        if "::" not in name and name in snapshot and len(snapshot[name].splitlines()) > lines
    ]


def violations(head: Snapshot, base: Snapshot | None) -> list[str]:
    """Every way the head departs from the shape, each one line; with no base, the head is its own base."""
    base = head if base is None else base
    found: list[str] = []
    # the room a push may take is what the head's budgets grant beyond what the base's already hold
    head_tests = lines_in(head, "tests/")
    base_tests = lines_in(base, "tests/") + room_of(head) - room_of(base)
    if head_tests > base_tests:
        found.append(
            f"tests/ grew from {base_tests} to {head_tests} lines; offset the new tests by deletions in the same pull request"
        )
    found.extend(over_budget(head))
    before = {name: file_counts(text) for name, text in tests_of(base).items()}
    after = {name: file_counts(text) for name, text in tests_of(head).items()}
    for name, counts in after.items():
        was = before.get(name, {"lines": 0})["lines"]
        if counts["lines"] > FILE_LINES and counts["lines"] > was:
            found.append(
                f"{name} has {counts['lines']} lines, above {FILE_LINES} and the merge base's {was}"
            )
    for key in ("history_lines", "long_docstrings", "retirement_skips"):
        total, was = sum(c[key] for c in after.values()), sum(c[key] for c in before.values())
        if total > was:
            found.append(f"tests/: {key.replace('_', ' ')} grew from {was} to {total}")
    found.extend(test_imports(head))
    base_groups = duplicate_groups(base)
    for digest, names in duplicate_groups(head).items():
        if len(names) > len(base_groups.get(digest, [])):
            found.append(f"copied setup: {', '.join(names)} share one body; keep one in tests/frame.py")
    for name in sorted(uncalled(head) - uncalled(base)):
        found.append(f"{name} is called nowhere in src/, tools/ or examples/: delete it with its tests")
    return found


def base_ref() -> str:
    return merge_base.base_ref()


def main() -> None:
    """Print every way tests/ has grown against the merge base and exit 1 where it has; nothing printed and exit 0 where the shape holds."""
    root = Path(__file__).resolve().parents[1]
    found = violations(working_tree(root), at_ref(root, base_ref()))
    print("\n".join(found) or "the shape of tests/ holds against the merge base")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
