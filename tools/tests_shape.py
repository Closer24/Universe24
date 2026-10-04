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
    "tests/test_the_loader.py::test_a_massless_message_lays_no_uniform_mode_and_the_loader_refuses_one_that_does": (
        24,
        "the lay's uniform mode (the experimenter's bug report, #1827 comment 5975131359; the Boss's 5975430859): a massless "
        "packet's two levels each sum to 0 on the committed worlds, and the loader refuses a mode entry whose sums are not 0",
    ),
    "tests/test_the_meeting.py::test_the_taking_removes_the_photon_and_the_front_leaves_the_board_dark": (
        14,
        "the lay's uniform mode (#1827 comment 5975131359): the committed one-photon world's taking at 48, the share never "
        "above the lay's by more than the known transient, and 0 exactly once the front has swept both packets",
    ),
    "tests/test_documents.py::test_no_undated_history_clause_stands_in_the_law_or_the_engines_document": (
        10,
        "the documents' gates (the owner's word of 2026-10-04, a perfect algebra; #1793 comment 5974938542): no undated history "
        "clause in the law or the engine's document beyond tools/history_allowed.json, which only shrinks; the loader of the gates with it",
    ),
    "tests/test_documents.py::test_every_shared_number_stands_in_its_one_form": (
        4,
        "the documents' gates: every number of tools/numbers.json in its canonical form and in none of its forbidden forms",
    ),
    "tests/test_documents.py::test_every_derived_number_is_its_scripts_output": (
        4,
        "the documents' gates: every derived number of the table the output of its script under tools/derivations/",
    ),
    "tests/test_the_bound_body.py::test_the_committed_worlds_load_and_every_blind_is_its_builders_byte_for_byte": (
        25,
        "the count gate on the smallest shipped world of every builder whose load is seconds (the Boss's 5971346856, item 2, "
        "after #1788's lay defect in the committed worlds that the test without a board did not catch): one GameBoard per "
        "folder, no interval, the long-loading folders the runner's gate by name",
    ),
    "tests/test_pixel_mode.py::test_a_messages_mode_count_is_the_books_count_read_once_over_the_board": (
        16,
        "the generator's count as the books read it (mode-count, the mathematician's finding of 2026-10-03): the share "
        "summed over the board and read in quanta once, the shipped two slits and Zeno counts the books' own, the dilute wave",
    ),
    "tests/test_the_node_reader.py::test_a_count_is_one_quantum_of_the_invariant_in_the_familys_own_wall": (
        26,
        "count-unit (the two hands' word on #1793's R8): the taker's lay at 2 A^2 sin omega = T per quantum, the "
        "family's wall W_c sin omega_0 by one root, light's W_c, the [1, 1299] amplitude unchanged, a laid body's books",
    ),
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
    "tests/test_the_draw.py::test_the_born_lights_frequency_is_the_declared_resonance_and_a_node_reader_counts_in_its_own_quantum": (
        90,
        "the generic node_reader round (the Boss's brief at the owner's decision 234, item 7, 2026-10-03): the record's "
        "own unit W_rec read once at the books' origin, the transition key refused on a region, the one-Node "
        "refusal of a travelling wave, the dark's hazard per proper interval in the vacuum and in a well",
    ),
    "tests/test_the_giving.py::test_the_source_in_time_lays_no_uniform_mode_where_its_span_holds_a_period": (
        33,
        'the giving lays no uniform mode (the owner\'s "yes to everything" of 2026-10-04, #1793 comment 5975629873; the '
        "mathematician's 5975866852 and 5975925032): the source's increments corrected by the division act in time where the "
        "span holds a period, the period by the rotation act, a short span laid as built, the resonance world's sums and share",
    ),
    "tests/test_the_giving.py::test_the_open_boards_packet_lays_no_uniform_mode": (
        20,
        "the giving lays no uniform mode (2026-10-04): the open board's packet's two levels through the message lay's "
        "division act, each summing to 0 over the board after the lay, the quantum standing",
    ),
    "tests/test_the_giving.py::test_the_front_writes_to_zero_over_the_declared_shells_and_the_board_ends_dark": (
        38,
        "the front's taper (the owner's \"yes to everything\" of 2026-10-04, #1793 comment 5975629873): the world's "
        "`erasure` L, the ball behind the last L shells at (0, 0) exactly, the shells before the reach falling, the erasure "
        "line's take and unit, the board dark at 200 and the back-in-time gate MATCH across the tapered faces",
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
    "tests/test_the_meeting.py::test_a_given_plane_is_laid_on_every_plane_alike_with_the_tables_sense_and_writes_the_sign_row": (
        60,
        "the lay by the count with the sense (round F of the board, the Boss's brief at the owner's word of 2026-10-03, "
        "everything now and in parallel): the conversion table's sense per record out and its refusals, the given "
        "planes laid alike at the quarter turn on the committed neutron conversion world, the Wronskians and the shares "
        "at the Node, the twelve lay lines and the crossing, the sign rows' first write",
    ),
    "tests/test_the_bound_body.py::test_the_nucleons_fixed_point_in_its_own_nuclear_holders_well_stands_and_the_twin_without_it_spreads": (
        104,
        "the nucleon's dedicated test (the mathematician's 275 (b) with the advisor's second, the Boss's brief of "
        "2026-10-03, C.15): the fixed-point lay with the compact seed in its own nuclear holder's well at the four "
        "declared integers, the hold's first write returning the start's rest within one unit at every Node, the deviation from the exact line a GAMEBOARD reading, the count the record's share within "
        "the gate, the standing read over one period against the twin without the holder, the remainders at the "
        "half wall and the back-in-time gate across two periods",
    ),
    "tests/test_the_meeting.py::test_the_resonant_two_mode_act_turns_by_the_planes_size_once_per_window": (
        33,
        "the resonant two-mode act's dedicated test (the Boss, 2026-10-03): the scale derived from the file's "
        "numbers, the two reference records by the giving's recurrence, A W / 2 at every arrival phase, the "
        "detuned sinc, the root once per window on the shipped Zeno world, the window's turn as W sub-turns with the carry",
    ),
    "tests/test_integer_algebra.py::test_a_composed_product_of_literals_is_refused_outside_core_rule3": (
        11,
        "PR D's gate (the Boss's brief of 2026-10-03): no two integer literals multiplied, added or raised outside "
        "core/rule3.py, the composed number named from the Ports and the levels or taken from the files",
    ),
    "tests/test_the_features.py::test_the_engines_numbers_are_written_from_the_ports_and_the_levels_names": (
        51,
        "PR D, no number in the engine (the owner's word, the Boss's brief of 2026-10-03): the start's fine unit from "
        "the six reads twice, the tent against the discrete parabola's top on three chains, the miss bound from the "
        "six reads over the axis's two Ports on a chain, a slab and a cube, the rest's two powers by name and its "
        "keyword-only `intervals`, the radiated total against (2 / 3) T sin k at two T, one PORTS under src/",
    ),
    "tests/test_the_features.py::test_the_writes_room_under_a_negative_tension_is_the_larger_of_the_hills_and_the_tensions": (
        48,
        "the register's room under a negative tension (the mathematician's 268 with the advisor's second, two hands; the "
        "Boss's brief of 2026-10-03): the tension's room at the rule's universe's four pairs against the hill's, the four "
        "shipped universes' bound unmoved, a universe whose write binds the bound lowered by name",
    ),
    "tests/test_the_bound_body.py::test_two_charged_records_of_count_one_write_their_own_sign_rows_and_a_count_above_one_is_refused": (
        64,
        "the count-1 gate's dedicated test (the Boss, 2026-10-03; ALGEBRA.md, No record reads its own write of "
        "the sign, item 43 (1)): two charged records of count 1 on a chain, each its own record and its own row "
        "of the sign, each row sourced by its own Wronskian alone, the turn reading the other's row alone and the "
        "self-read 0 to the bit over three intervals, a count above 1 refused by name",
    ),
    "tests/test_the_meeting.py::test_the_pulsed_gates_window_is_bounded_by_the_probes_lays_and_closes_at_its_taking": (
        70,
        "the pulsed gate's dedicated test (the Boss's brief at the owner's word of 2026-10-03, about 80 lines): the "
        "window bounded by the probe's lays, the lay by the count at the declared tick, the probe's click and the "
        "drive's taking by the labels' squares, the body's clock and the window's index on the click line, the "
        "loader's five refusals, the back-in-time gate across the probe's lay on the shipped pulsed world",
    ),
    "tests/test_the_loader.py::test_the_loader_refuses_every_wrong_key_of_the_files_by_name": (
        172,
        "the loader's refusals by name on the loader's own functions with no world run (the owner's word of "
        "2026-10-03, every piece has a unit test; the architect's audit): the keys, the mode file, the lay and the "
        "budget's least T, the faces and the open faces' layer, the messages, the universe",
    ),
    "tests/test_the_node_reader.py::test_a_record_declared_a_reader_over_two_nodes_takes_gives_and_stays": (
        289,
        "the NodeReader round (the owner's word of 2026-10-03, a reader with Nodes alone is never on one Node; the "
        "Boss's brief): the ion's record declared over two adjacent Nodes in equal weights, the lay A_n^2 = A^2 / n, "
        "the share credited 1, the in-pieces and the count-on-a-Node refusals, the boundary cut with the inner Link open, the "
        "uniform mode's recurrence to the bit, the drive projected on the reader's normalised mode, one draw per click "
        "with the write's Node drawn after the outcome by the window's inflow booked per Node, the giving's Node by "
        "the record's share (the mathematician's 299 with the advisor's second, two hands)",
    ),
    "tests/test_the_node_reader.py::test_a_reader_with_its_own_record_stands_on_one_node": (
        46,
        "the relation seen from its two ends (the owner's decision of 2026-10-03, 16:30 UTC, on the mathematician's 323 "
        "with the advisor's yes): the shipped Zeno reader declared at one Node, its lay A_1 = A, the turn reading the "
        "drive's level exactly, its six Links cut, the uniform mode's recurrence, the click line naming no Node with "
        "the hole and the lay at the only Node, the back-in-time gate across the run, and a reader with Nodes alone "
        "at one Node still refused by name",
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
                    found.append(f"{name} imports {imported}: move the helper to tests/laws.py")
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
            found.append(f"copied setup: {', '.join(names)} share one body; keep one in tests/laws.py")
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
