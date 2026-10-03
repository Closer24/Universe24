"""The shape of tests/, held against the merge base (issue #1211; the model owner, 2026-09-27: the bulk must not come back).

Every count is compared with the same count at the merge base (CHECK_BASE, else origin/main),
read from git, so no baseline file is kept: a pull request may lower a count, never raise it.

(a) Size. tests/ holds no more lines than at the merge base: it only shrinks, and a pull
    request that adds tests offsets them by deletions (the model owner, 2026-09-27); a test
    file above 600 lines holds no more than at the merge base, and a new one stays under.
    A test the Boss gives room by name (ROOM: the test, its lines and the reason, recorded
    here and in ENGINE.md section 9) adds that room to the base's size while it stands with
    at most those lines; nothing else grows the budget.
(b) Copied setup. No test module imports another `test_*.py`: shared builders live in
    `tests/laws.py`. A function of 8 lines or more whose abstracted
    body appears twice across tests/ is refused beyond the merge base's groups.
(c) History. Across tests/, the docstring and comment lines that carry a history marker, and
    the docstrings beyond three lines, stay at or below the merge base's (a moved helper moves
    its count with it).
(d) Retired code. Across tests/, the module-wide skips and the skips that name cancelled or
    retired code stay at or below the merge base's; a public function of `src/` outside `features/` that
    nothing in `src/`, `tools/` or `examples/` names is refused unless the merge base has it.
"""

from __future__ import annotations

import ast
import hashlib
import io
import os
import re
import subprocess
import sys
import tokenize
from pathlib import Path

from record_code_shape import Abstracted, docstring_of

ROOT = Path(__file__).resolve().parents[1]
FILE_LINES = 600
DUPLICATE_LINES = 8
DOCSTRING_LINES = 3
HISTORY = re.compile(r"\b(?:SINCE|HISTORY|BUILD\.md|[Ss]uperseded|[Pp]reviously|[Rr]ecords? \d{3,})\b")
RETIRED = re.compile(r"CANCELLED|[Rr]etired")
ROOM = {  # the room given by name: the test, its lines and the reason (ENGINE.md, section 9)
    "tests/test_the_draw.py::test_the_open_boards_giving_is_a_packet_along_a_drawn_axis_with_the_carry": (
        79,
        "the open board's packet lay's dedicated test (the Boss, 2026-10-03): the exact root and the envelope, "
        "the band's line with the transverse mode, the loader's three refusals, the lay on an open board with the "
        "carrier's phase at Omega, the blind",
    ),
    "tests/test_the_meeting.py::test_the_hole_of_a_dense_record_removes_one_quantums_share_and_the_phase_stands": (
        36,
        "the partial hole's round (the owner's decision 234, item 7; the Boss's brief of 2026-10-03): the hole of a "
        "dense record, the face's target the scaled level where the share at the Node exceeds the record's own quantum, "
        "the phase and the sense standing, the back-in-time gate across a dense taking",
    ),
    "tests/test_the_meeting.py::test_the_two_faces_remove_exactly_one_quantum_from_a_dense_record": (
        40,
        "the partial hole's second pass (the Boss's brief of 2026-10-03 at the mathematician's 244): the quadratic "
        "factor on the Node's own form at the first face and the exact rest at the second, one quantum leaving the "
        "record within Rule3's floors on the shipped Zeno world",
    ),
    "tests/test_the_draw.py::test_the_source_in_time_lays_the_form_it_radiates": (
        30,
        "the partial hole's second pass (the mathematician's 245 with the advisor's second): the source in time's "
        "total (2 / 3) T sin k in the law's integers at [2, 3], [4, 5] and [9, 10], the root on the large number",
    ),
    "tests/test_the_draw.py::test_a_record_empty_at_the_origin_takes_its_unit_from_its_first_lay": (
        24,
        "the partial hole's round (the owner's decision 234, item 7; the Boss's brief of 2026-10-03): the unit of a "
        "record empty at the books' origin set at its first lay to the giving's own W_c sin Omega, a born quantum "
        "below the half-top energy credited 1 and not 0",
    ),
    "tests/test_the_draw.py::test_the_born_lights_frequency_is_the_declared_resonance_and_a_detector_counts_in_its_own_quantum": (
        90,
        "the generic detector round (the Boss's brief at the owner's decision 234, item 7, 2026-10-03): the record's "
        "own unit W_rec read once at the books' origin, the transition key refused on a region, the one-Node "
        "refusal of a travelling wave, the dark's hazard per proper interval in the vacuum and in a well",
    ),
    "tests/test_the_meeting.py::test_a_record_converted_whole_at_its_node_lays_the_table_at_the_rate": (
        36,
        "the conversion's dedicated test (the Boss, 2026-10-03): the committed neutron conversion world's lays by "
        "the invariant and by the count, the back-in-time crossing from the lay lines, the six loader refusals",
    ),
    "tests/test_the_share.py::test_the_steps_shortened_reads_equal_the_full_reads_bit_for_bit": (
        35,
        "the step's speed's dedicated test (the owner's word of 2026-10-03, 15:12 Israel, let them do it): every "
        "shortened read of the step, the share at the Nodes with a level, the write factor in the hardware's "
        "integers inside the width and the Port's fill on the face layer, equals the full read bit for bit",
    ),
    "tests/test_the_features.py::test_a_frozen_row_stands_outside_the_energy_line_and_two_moving_planes_still_share_their_pair": (
        12,
        "the atom round's dedicated test (the Boss, 2026-10-03): the frozen row [0, den] loads beside a moving plane "
        "under the rotation holder, one plane or three, and two moving planes of different num / den are still refused",
    ),
    "tests/test_the_meeting.py::test_the_resonant_two_mode_act_turns_by_the_planes_size_once_per_window": (
        33,
        "the resonant two-mode act's dedicated test (the Boss, 2026-10-03): the scale derived from the file's "
        "numbers, the two reference records by the giving's recurrence, A W / 2 at every arrival phase, the "
        "detuned sinc, the root once per window on the shipped Zeno world, the window's turn as W sub-turns with the carry",
    ),
    "tests/test_the_features.py::test_the_writes_room_under_a_negative_tension_is_the_larger_of_the_hills_and_the_tensions": (
        48,
        "the register's room under a negative tension (the mathematician's 268 with the advisor's second, two hands; the "
        "Boss's brief of 2026-10-03): the tension's room at the rule's universe's four pairs against the hill's, the four "
        "shipped universes' bound unmoved, a universe whose write binds the bound lowered by name",
    ),
    "tests/test_the_meeting.py::test_the_pulsed_gates_window_is_bounded_by_the_probes_lays_and_closes_at_its_taking": (
        70,
        "the pulsed gate's dedicated test (the Boss's brief at the owner's word of 2026-10-03, about 80 lines): the "
        "window bounded by the probe's lays, the lay by the count at the declared tick, the probe's click and the "
        "drive's taking by the labels' squares, the body's clock and the window's index on the click line, the "
        "loader's five refusals, the back-in-time gate across the probe's lay on the shipped pulsed world",
    ),
    "tests/test_the_node_reader.py::test_a_record_declared_a_reader_over_two_nodes_takes_gives_and_stays": (
        213,
        "the NodeReader round (the owner's word of 2026-10-03, a detector is never on one Node; the Boss's brief): the "
        "ion's record declared over two adjacent Nodes in equal counts, the lay A_n^2 = A^2 / n, the share credited 1, "
        "the one-Node and the in-pieces refusals, the boundary cut with the inner Link open, the uniform mode's "
        "recurrence to the bit, the taking's and the giving's Nodes drawn by the shares",
    ),
}
CALLERS = ("src/", "tools/", "examples/")
FEATURES = "src/event_universe/features/"

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
                    found.append(
                        f"{name} imports {imported}: move the helper to tests/worlds.py or tests/running.py"
                    )
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
    """The public top-level functions of src/ outside features/ that nothing else names."""
    callers = "\n".join(text for name, text in snapshot.items() if name.startswith(CALLERS))
    found = set()
    for name, text in snapshot.items():
        if not name.startswith("src/") or name.startswith(FEATURES):
            continue
        for node in ast.parse(text).body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                if len(re.findall(rf"\b{node.name}\b", callers)) <= 1:
                    found.add(f"{name}:{node.name}")
    return found


def room_of(snapshot: Snapshot) -> int:
    """The room the named tests take in a snapshot: per ROOM entry whose test stands in its file, the fewer of its named lines and the test's own (the def through its last line), so a test keeps its room only while it holds it; 0 for a test that is gone."""
    found = 0
    for name, (lines, _reason) in ROOM.items():
        path, function = name.split("::")
        if path not in snapshot:
            continue
        for node in ast.walk(ast.parse(snapshot[path])):
            if isinstance(node, ast.FunctionDef) and node.name == function and node.end_lineno:
                found += min(lines, node.end_lineno - node.lineno + 1)
    return found


def violations(head: Snapshot, base: Snapshot | None) -> list[str]:
    """Every way the head departs from the shape, each one line; with no base, the head is its own base."""
    base = head if base is None else base
    found: list[str] = []
    head_tests, base_tests = lines_in(head, "tests/"), lines_in(base, "tests/") + room_of(head)
    if head_tests > base_tests:
        found.append(
            f"tests/ grew from {base_tests} to {head_tests} lines; offset the new tests by deletions in the same pull request"
        )
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
            found.append(
                f"copied setup: {', '.join(names)} share one body; keep one in tests/worlds.py or tests/running.py"
            )
    for name in sorted(uncalled(head) - uncalled(base)):
        found.append(f"{name} is called nowhere in src/, tools/ or examples/: delete it with its tests")
    return found


def base_ref() -> str:
    return os.environ.get("CHECK_BASE") or "origin/main"


def main() -> None:
    """Print every way tests/ has grown against the merge base and exit 1 where it has; nothing printed and exit 0 where the shape holds."""
    root = Path(__file__).resolve().parents[1]
    found = violations(working_tree(root), at_ref(root, base_ref()))
    print("\n".join(found) or "the shape of tests/ holds against the merge base")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
