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
    "tests/test_the_clicks_reader.py::test_the_committed_records_credits_give_the_counts_floor_and_the_torus_wide_where_and_name_the_lacking_keys": (
        26,
        "the reader of the clicks log alone on the committed record (2026-10-24, the owner's word that every measurement goes to the clicks): "
        "125 credits in one window, the count's floor 1, the where 5 Links on every axis, the momentum and the clock unreadable with their keys named",
    ),
    "tests/test_the_clicks_reader.py::test_a_log_with_the_click_views_keys_gives_velocity_verdict_dilation_rest_and_product_by_hand": (
        89,
        "the same reader on a log with the click's view's keys, the momentum the frame's running cosine with the Link current's sign (2026-10-24): "
        "the velocity in Links per board and per proper interval, the bound and the free verdicts, p in T's unit, the rest point from the four pairs "
        "(1 for the massless record, None at a one-Node lay), the dilation ratio and the Delta x Delta p product in Links x T against the floor T / 2, each number computed by hand",
    ),
    "tests/test_the_loader.py::test_dens_circle_is_read_from_its_integers_alone": (
        30,
        "the one test that factors the PeV den (2026-10-24, the Boss's rule that one test alone pays the factoring, 23 s cold): the shipped file's rows, "
        "the least leg and the proton's point, their legs and the massless wall over the proton's, the lightest point and the pages' captions at that den, "
        "moved here from the rows test, the heaviest pair's, the lightest point's, the one world's and the captions' tests",
    ),
    "tests/test_the_click_readings.py::test_the_point_is_the_reduced_pair_of_the_cosine_read_from_three_levels": (
        7,
        "the click's view (2026-10-24, the owner's frame, the builder's six readings): the point the reduced pair of the cosine read from three levels",
    ),
    "tests/test_the_click_readings.py::test_the_readings_at_a_node_are_the_boards_own_at_the_intervals_start": (
        41,
        "the click's view: the six readings at a Node equal to the board's own levels at the interval's start and the level the step left",
    ),
    "tests/test_the_click_readings.py::test_every_credit_of_the_first_meeting_carries_the_eight_readings_and_every_birth_its_childrens_records_and_points": (
        36,
        "the click's view on the uniform cube's first meeting: every credit's six keys as the board reads them, every birth's children's records and points",
    ),
    "tests/test_the_click_readings.py::test_the_hole_seeds_credits_read_their_own_clocks_and_differ_where_the_volume_differs": (
        27,
        "the click's view on the sea with a hole: every credit's proper the floor of its Node's clock summed to its interval, its windows the Node's closes, two propers differing where the clocks differ",
    ),
    "tests/test_the_click_readings.py::test_the_momentum_is_the_frames_running_cosine_with_the_link_currents_sign_and_a_second_credit_reads_no_point": (
        49,
        "the click's view, the momentum as the frame's running cosine with the Link current's sign at the interval's start (2026-10-24, the blind measured, the Boss's ruling): the plane wave at k = "
        "2 pi / 3 reads [1, -1, 2] on x and [0, 1, 1] across; on the hole seed under the hole the Node's own level before, the drift stopped (the Boss's ruling of 2026-10-24), the hole's Node alone re-lit at every close, "
        "its first credit [0, 5, 6] on every axis and every later credit a point with the momentum alike on the three axes at the sign 0, the beat None beyond the band",
    ),
    "tests/test_the_click_readings.py::clock_of": (
        7,
        "the helper: the Node's composed clock at every Node from the seed's read, the time count's term summed by the tests apart from the engine",
    ),
    "tests/test_the_click_readings.py::bare_board": (
        7,
        "the helper of the three tests above: the one universe file on the bare 3-cube, every output line kept",
    ),
    "tests/test_the_readings_are_made_once_per_interval.py::test_the_rule_and_the_pairs_of_the_digits_read_are_made_once_per_close": (
        22,
        "the digits' read made once per record per interval (the branch record-speed, 2026-10-24): digits.ruled and flux.pairs_of asked at "
        "every Node's frame of a close give the same integers memoized and not, and node.rule_of is called once per record over every frame",
    ),
    "tests/test_the_readings_are_made_once_per_interval.py::test_the_turned_room_is_computed_once_per_pair_at_load": (
        14,
        "plane.turned_room under functools.cache at load (the branch record-speed, 2026-10-24): the same room cold and warm per turned pair, "
        "every warm call a hit, the amplitude bound the world's",
    ),
    "tests/test_the_birth_is_a_list_of_records.py::test_the_lists_two_light_quanta_make_are_the_conjugate_pairs_and_the_general_enumeration_a_function": (
        16,
        "Matter's birth from light, N records one per child (2026-10-24, the owner's word, several can be born): the law as written "
        "selects among the conjugate pairs, birth_of gives those, exact, kept, lightest first; lists_of the general enumeration with the test's bound",
    ),
    "tests/test_the_birth_is_a_list_of_records.py::test_a_list_of_four_children_lays_four_records_through_the_same_path": (
        20,
        "the same sentence's path for N: a four-child list handed to born_items lays two records of each family at the list's senses, "
        "each record's Wronskian its child's sense, the holder's four reader rows written after one interval",
    ),
    "tests/test_the_birth_is_a_list_of_records.py::test_the_uniform_cube_births_the_list_one_record_per_child_each_at_its_sense": (
        30,
        "the same sentence on the uniform 3-cube's first meeting: the records laid number the list's children, each born record's "
        "Wronskian its child's sense, opposite children opposite, the books one per child, the holder's row of every charged record written",
    ),
    "tests/test_the_birth_is_a_list_of_records.py::test_the_holes_board_runs_back_exact_through_its_births": (
        16,
        "the same sentence's run back: the sea with a hole 20 intervals through its births and back, MATCH, the N records' lays undone",
    ),
    "tests/test_the_birth_is_a_list_of_records.py::bare_board": (
        8,
        "the helper of the three tests above: the one universe file on the bare 3-cube with the births kept",
    ),
    "tests/test_the_pages_carry_the_legend_of_kinds.py::test_the_captions_name_the_three_prime_lifts_by_rising_sine_at_every_den": (
        26,
        "the pages' captions a look and no law (the owner's word of 2026-10-24, the branch born-amplitude): den's three prime lifts by "
        "rising sine the electron, the proton and the neutron's candidate, at den 1,021, the top tier and the PeV den; the former rule kept by name",
    ),
    "tests/test_the_birth_is_a_list_of_records.py::born_here": (
        12,
        "the birth's own path at one Node of a fresh board (the branch born-amplitude, 2026-10-24): the seed's record at the Node to "
        "the state of a Node with no level through the one lay act, the hole, then the list laid by the one click act",
    ),
    "tests/test_the_birth_is_a_list_of_records.py::test_a_born_child_carries_the_two_light_quantas_energy_and_the_charge_t_div_2": (
        34,
        "the lay of a born child is the law's at every den (the owner's ruling of 2026-10-24 on the hand's measurement): 6 den A^2 = "
        "0.99756 W_c per child, W = +-A^2, the charge one per child, the Lorentz factor in the child's own unit, at den 1,021 and the file's den",
    ),
    "tests/test_the_charge_per_quantum.py::test_equal_wronskians_of_two_families_write_equal_charge": (
        16,
        "the charge written is the Wronskian over T div 2 for every reader (the law's sentence of 2026-10-24, the owner's word): "
        "one quantum of the proton and one of the electron in the birth's own form write the same level into the holder of the sign",
    ),
    "tests/test_the_charge_per_quantum.py::test_the_holes_board_runs_25_intervals_with_the_sign_holder_bounded": (
        22,
        "the same sentence on the sea with a hole over 25 intervals: electron pairs born by the draw and the holder of the sign "
        "below the former factor's one-electron write of two intervals, no exponential (the runaway hand's finding of 2026-10-24)",
    ),
    "tests/test_the_share.py::test_under_the_rotation_the_share_reads_the_level_pair_as_the_step_reads_it": (
        88,
        "the share under the rotation (the mathematician's line, #1793 comment 5981866600 K3; the advisor's breaker): the level "
        "pair read as the step reads it, the step's identity exact at every Node with its three walk terms, the turned read "
        "standing within the integer walk on the ring where the plain read drifts by percent, the plain read bit for bit where no family turns",
    ),
    "tests/test_the_stress_is_the_links.py::test_the_board_sums_of_the_former_and_the_new_reading_are_equal_to_the_bit_on_a_wrapped_board": (
        16,
        "the stress is the Links' (the builder's M21, 2026-10-23): the former reading's board sum over its wall and the new "
        "reading's over the doubled wall equal to the bit on a wrapped board, a plane wave, a one-Node record and random levels",
    ),
    "tests/test_the_stress_is_the_links.py::test_the_reading_is_invariant_under_the_shift_and_even_under_the_inversion_and_reads_a_one_node_record_at_its_neighbours": (
        26,
        "the stress is the Links': the reading invariant under the shift of every level by one number where the former gains "
        "m Delta_a a, even under the axis's inversion, a one-Node record's parts at its two neighbours",
    ),
    "tests/test_integer_algebra.py::test_the_conventions_tables_identities_hold_on_small_integers": (
        93,
        "the conventions table's identities asserted where the engine computes them (fill 17 part 3, the Boss's brief of "
        "2026-10-04): the momentum identity with the carried remainders, the tension's Node part and the Link's mean, the "
        "two forms' walks under the rounding and the weighted coefficients' symmetry, on small integers",
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
    "tests/test_the_features.py::test_a_frozen_row_stands_outside_the_energy_line_and_two_moving_planes_still_share_their_pair": (
        12,
        "the atom round's dedicated test (the Boss, 2026-10-03): the frozen row [0, den] loads beside a moving plane "
        "under the rotation holder, one plane or three, and two moving planes of different num / den are still refused",
    ),
    "tests/test_integer_algebra.py::test_a_composed_product_of_literals_is_refused_outside_core_rule3": (
        11,
        "PR D's gate (the Boss's brief of 2026-10-03): no two integer literals multiplied, added or raised outside "
        "core/rule3.py, the composed number named from the Ports and the levels or taken from the files",
    ),
    "tests/test_the_loader.py::test_the_loader_refuses_every_wrong_key_of_the_files_by_name": (
        172,
        "the loader's refusals by name on the loader's own functions with no world run (the owner's word of "
        "2026-10-03, every piece has a unit test; the architect's audit): the keys, the mode file, the lay and the "
        "budget's least T, the faces and the open faces' layer, the packets, the universe",
    ),
    "tests/test_proofs_check_the_law.py::test_every_row_of_the_proofs_inventory_returns_its_verdict_and_the_unchecked_only_fall": (
        77,
        "the proofs' gate (the owner's order of 2026-10-04, 07:50 UTC, that all the proofs be checked by machine; the "
        "advisor's design lines, #1793 comment 5977935062): every row of tools/derivations/proofs_inventory.json with a "
        "check runs to its verdict, every check_ function of the proofs_ modules is a row's, the rows of the kinds A, B "
        "and C without a machine check are a ratchet that only falls, and no proofs_ module imports the engine or names "
        "a run's file; the imports stand inside the test so the file is the test alone",
    ),
    "tests/test_the_sign_holders_link_turn.py::test_the_wronskian_is_conserved_on_the_bare_torus_under_the_folded_link_turn": (
        50,
        "the Wronskian conserved on the bare torus under the sign's Link phase in the fold form, the electron reading the charge holder",
    ),
    "tests/test_the_interval.py::test_the_volume_of_a_level_and_the_level_of_a_volume_are_one_division_and_one_search_each_the_others_inverse": (
        46,
        "the directive's build (the reader's line on the volume form M12a, 2026-10-22, T3): the volume of a level one "
        "division and the level of a volume one search, the staircase's inverse bit for bit, the clock's zero, the "
        "refusals by name, the start's two functions",
    ),
    "tests/test_the_eras_log.py::test_the_eras_log_holds_the_boards_readings_per_interval_and_the_page_draws_them": (
        74,
        "the directive's build (the Boss's brief of 2026-10-22, DESIGN section 4 (g)): the eras' log and its page, the two "
        "host tools of the test of the law's course read on the 3-cube light cube under the hypotheses' keys",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_the_holed_nodes_own_quanta_pay_and_nothing_is_made_at_the_links_on_the_3_cube": (
        17,
        "the board's own hole the Node's own level before, the drift stopped (the Boss's ruling of 2026-10-24 on the bound-click hand's measurement): conservation at the click on the 3-cube, nothing made at the Links, at most one hole per close, the light never spent",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_the_5_cube_keeps_its_light_above_zero_under_the_holes": (
        10,
        "the same hole on the 5-cube: the light above zero through 20 intervals where the write to (0, 0) spent it by 8, no close holing every Node, no light made",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_a_hole_on_the_uniform_sea_is_the_seeds_own_origin": (
        17,
        "the hole's form is the seed's: stopped_at at the seed's origin (0, 0), on the uniform sea the level before twice, the seed's kink exactly",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_the_first_draw_by_the_digits_falls_at_a_share_between_one_and_two_quanta_and_writes_its_credit": (
        30,
        "the Born side on the hole seed: the first meeting met by the draw at one whole quantum with a remainder, the weights the remainder against the unit, the credit and birth lines at that Node",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_the_run_back_is_exact_through_the_closes_that_hole": (
        14,
        "the hole's lay logged and undone by the run back, eight intervals forward through the births and eight back bit for bit",
    ),
    "tests/test_the_board_is_the_cube_48.py::test_two_signed_permutations_generate_the_48_and_every_element_is_one": (
        6,
        "the Boss's covariance test of 2026-10-24 (the board is the cube's 48): the 48 generated from two signed permutations by the closure, no table",
    ),
    "tests/test_the_board_is_the_cube_48.py::test_a_seed_invariant_under_the_48_runs_invariant_under_the_48": (
        17,
        "the covariance test (a): a seed invariant under the 48 runs invariant under every element at every interval, every level, remainder, write remainder and phase line; fails by name on the ordered read at the first whether draw on a non-trivial orbit (the sea plus one at the origin at 4, the hole-seed 5-cube at 4)",
    ),
    "tests/test_the_board_is_the_cube_48.py::test_a_seed_transformed_before_the_run_gives_the_transformed_run": (
        20,
        "the covariance test (b): the sea plus one at (1, 0, 0) carried by a rotation and by a reflection before the run gives the carried run, bit for bit; fails by name on the ordered read at 4",
    ),
    "tests/test_the_click_reads_one_link.py::test_the_link_lattice_is_the_neighbours_own_coarsened_and_no_port_order_enters_the_number": (
        34,
        "the one-Link read's unit test (2026-10-24, the builder's sentence): at the first draw of the hole-seed 3-cube each Link lattice F_ij a multiple of the neighbour's own F_j with the coarse index the floor of the fine one over the ratio, the frame's neighbours reversed and rolled reading the same number, a Node beyond no Port refused by name",
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
