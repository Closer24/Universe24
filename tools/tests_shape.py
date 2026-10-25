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
    "tests/test_the_record_gates.py::test_the_committed_record_shows_the_agreed_gates_by_name": (
        27,
        "the record's gates (2026-10-25, the two blind hands' table agreed cold on PR #2187): the nineteen gates of tools/record_gates.py loaded by its path on the committed logs of examples/events/universe24, "
        "the thirteen verdicts shown and the ten not shown asserted by name so that a lost or a gained verdict fails by name, the board's view at five gates, the lack named where a verdict is not shown, "
        "the existence counts: returns above one, black holes above zero, the bodies' credits above light's",
    ),
    "tests/test_the_record_gates.py::test_three_predicates_on_a_record_by_hand": (
        36,
        "three predicates of the record's gates on a record of a few lines by hand: the recurring bangs shown with a birth after the return and not shown without it, "
        "the dilation with the births as matter, the conservation exact",
    ),
    "tests/test_the_record_gates.py::hand_record": (
        86,
        "the helper of the gates' hand test: the volume's top and return, two births at the Node A, a body's credits at A and B with their propers, every take exact, one Node turned",
    ),
    "tests/test_the_node_holds_the_same_count_of_integers.py::test_every_node_holds_the_same_count_of_integers_and_the_count_grows_by_a_point_at_a_birth": (
        41,
        "the generic Node's gate (2026-10-25, the plan's stage 0): the integers one Node holds read by tools/node_integers.py loaded by its path on the bare 3-cube at den 1,021 and at the top tier's den, "
        "never the shipped file; the rows' 35 derived and read at every Node before the first birth, every array of the board's shape, the growth at the first birth by 52 per record born, "
        "the three lifts' growth at the top tier's den by the interval 8, the largest bit length within 128 at both dens and the shipped den's half wall above it, the two deviations kept by name",
    ),
    "tests/test_the_point_rows_are_born_at_the_first_birth.py::test_the_lean_board_equals_the_board_with_every_point_standing_through_the_births": (
        70,
        "the point rows born at the first birth (2026-10-24, the field view (c)): the lean board against its twin with every point standing from the start, "
        "equal bit for bit on every shared label and every output line over 24 intervals of the hole seed through its births, the step back through the first birth",
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
    "tests/test_the_birth_is_a_list_of_records.py::bare_board": (
        8,
        "the helper of the three tests above: the one universe file on the bare 3-cube with the births kept",
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
    "tests/test_the_share.py::test_under_the_rotation_the_share_reads_the_level_pair_as_the_step_reads_it": (
        88,
        "the share under the rotation (the mathematician's line, #1793 comment 5981866600 K3; the advisor's breaker): the level "
        "pair read as the step reads it, the step's identity exact at every Node with its three walk terms, the turned read "
        "standing within the integer walk on the ring where the plain read drifts by percent, the plain read bit for bit where no family turns",
    ),
    "tests/test_the_loader.py::test_the_loader_refuses_every_wrong_key_of_the_files_by_name": (
        172,
        "the loader's refusals by name on the loader's own functions with no world run (the owner's word of "
        "2026-10-03, every piece has a unit test; the architect's audit): the keys, the mode file, the lay and the "
        "budget's least T, the faces and the open faces' layer, the packets, the universe",
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
    "tests/test_the_board_runs_in_slabs.py::test_the_5_cube_under_the_gapped_holder_runs_the_same_by_five_one_layer_slabs": (
        9,
        "the slabs' gate under the gapped holder (2026-10-24, the gravity-top hand's finding, the re-imposed halo): the 5-cube hole seed with the volume's pair gapped through loader/universe.volume_pair, 12 intervals, one process against five one-layer slabs, every array, line and swap count equal",
    ),
    "tests/test_the_board_runs_in_slabs.py::test_the_5_cube_hole_seed_runs_the_same_by_two_and_by_five_slabs": (
        7,
        "the slabs' gate (slabs.py, the board stepped in slabs by processes with one-Link halos, 2026-10-24): the 5-cube hole seed "
        "12 intervals through its births by two and by five slabs, every array, every line in its order and the swaps equal to the single process bit for bit",
    ),
    "tests/test_the_board_runs_in_slabs.py::test_a_tube_cut_across_z_runs_the_same_by_three_slabs": (
        5,
        "the slabs' gate on a [3, 3, 9] tube by three slabs across z: the three slabs' lines interleaved into the board's x-major order",
    ),
    "tests/test_the_board_runs_in_slabs.py::test_the_run_back_from_the_board_the_slabs_stepped_is_exact": (
        13,
        "the slabs' gate on the run back: the 3-cube through three slabs and back by the board's own inverse, every snapshot met again",
    ),
    "tests/test_the_board_runs_in_slabs.py::test_the_slabs_count_is_the_machines_and_the_boards_and_no_files": (
        12,
        "the slabs' count the machine's cores and the board's longest axis, no key of any file: slabs_of by hand, the world file's three keys",
    ),
    "tests/test_the_board_runs_in_slabs.py::board_of": (
        8,
        "the helper of the slabs' gate: the small universe on a bare torus with every output line kept",
    ),
    "tests/test_the_board_runs_in_slabs.py::run": (
        12,
        "the helper of the slabs' gate: a run by so many slabs with every array after every interval, the lines and the swaps",
    ),
    "tests/test_the_board_runs_in_slabs.py::parting": (
        12,
        "the helper of the slabs' gate: the first parting from the single process named by interval and arrays, by line or by the swaps",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_the_hole_takes_what_the_birth_books_and_makes_nothing_on_the_3_cube": (
        20,
        "the hole's clause of 2026-10-24 (the exact take, the builder's derivation): nothing made at any close of the 3-cube, the fall the births' taken where the born Nodes stand apart, each the walls plus an excess below the last level's step, a refused close leaving the light standing",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_the_5_cube_keeps_its_light_above_zero_and_makes_nothing_under_the_takes": (
        11,
        "the exact take on the 5-cube: the light above zero, nothing made at any close, births at several closes, no close holing every Node",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_a_full_stop_that_cannot_pay_refuses_by_name_and_the_light_stands": (
        16,
        "the refusal by name where the full stop would take less than the children's walls, on the chain of three Nodes at den 1,021: the cause, the two numbers, nothing born, the light standing",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_every_take_is_read_before_any_hole_is_written": (
        20,
        "every face before any write: within every close the frame's shares are read before the first hole is written",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_nothing_is_booked_without_its_lay_and_the_first_births_charge_is_the_books": (
        15,
        "the Boss's default of 2026-10-24, a close whose children's lay would be refused births nothing: no deficit, the books the children laid, the first birth's charge the books, the lay refusals naming a share above the unit",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_the_first_draw_by_the_digits_falls_at_a_share_between_one_and_two_quanta_and_writes_its_credit": (
        33,
        "the first draw by the digits met and not refused: one whole quantum and a rest, the weights the rest against the unit less it, the credit and the birth lines at that Node",
    ),
    "tests/test_the_hole_stops_the_drift.py::test_the_run_back_is_exact_through_the_closes_that_hole": (
        14,
        "the run back through the closes that hole, every state the forward run's bit for bit",
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
    "tests/test_the_reads_refusal_is_a_logged_line.py::test_a_refused_read_at_the_board_is_a_logged_line_and_the_run_goes_on": (
        20,
        "a refusal by name is a logged line, never a crash (2026-10-24, the gravity-top hand's finding): the 3-cube hole seed under the gapped holder of the volume through loader/universe.volume_pair runs 20 intervals with the read's vacuum refusal logged at the origin and births elsewhere",
    ),
    "tests/test_a_click_does_what_it_should.py::test_a_bound_bodys_click_writes_the_take_at_its_node_and_nothing_elsewhere": (
        44,
        "the owner's standing test extended to the bound body's click (2026-10-24, his sentence of 16:45 UTC): the lone pair's two records clicking together at their Node, the Node moved by the two takes' levels and its before kept, every other Node unchanged, the credits with the records' identities, nothing born, the run back exact",
    ),
    "tests/test_a_bound_body_clicks.py::test_the_lone_pairs_two_records_click_at_their_node_with_their_identities": (
        42,
        "the bound body's click (2026-10-24, the owner's sentence of 16:45 UTC): the lone pair's two records click together at the birth Node with their identities and the eight keys, the light falling by at least the two units, the quantum into the record booked by the beam's rule, the period of the beat 9 for the heavier point of den 1,021 and 0 for the massless pair",
    ),
    "tests/test_a_bound_body_clicks.py::test_the_lone_pairs_clicks_run_the_same_by_three_slabs": (
        30,
        "the slabs' gate through a bound body's click: the lone pair on the 3-cube by three one-layer slabs through its first clicks, every array, line and swap count equal",
    ),
    "tests/test_a_click_does_what_it_should.py::test_one_close_at_one_node_writes_the_take_there_and_nothing_elsewhere": (
        80,
        "the owner's standing test of the click (2026-10-24, 16:4x UTC, his word: a click does what it is supposed to, to the Nodes and to the Node): one close at one Node on the chain of three and on the 3-cube, the Node changed by exactly the take, every other Node unchanged, the children at the two senses with their Wronskians summing to 0, the log's take keys and the credit's support and windows, the draw from the Node and its six neighbours alone divided by the unit once, the run back exact; it stays whatever the tests hand prunes",
    ),
    "tests/test_the_click_reads_one_link.py::test_the_link_lattice_is_the_neighbours_own_coarsened_and_no_port_order_enters_the_number": (
        34,
        "the one-Link read's unit test (2026-10-24, the builder's sentence): at the first draw of the hole-seed 3-cube each Link lattice F_ij a multiple of the neighbour's own F_j with the coarse index the floor of the fine one over the ratio, the frame's neighbours reversed and rolled reading the same number, a Node beyond no Port refused by name",
    ),
    "tests/test_the_readers_tables.py::test_the_density_the_ledger_and_the_births_read_the_epochs_the_erasure_and_the_senses_by_hand": (
        148,
        "the reader's seven tables (2026-10-24, the owner's word that all the epochs, the second bang, the attraction, relativity and the Links' lengthening show in the clicks; the architect's list): on a log of a few lines by hand with the eras lines beside it by hand, "
        "the clicks per interval and the epochs bang, rise, top, fall, return with the eras log's bounds and the density's own runs, the first rise alone, the ledger's two cycles with the holder's quantum erased across the return and the tracks that cross it, the births per cycle per point per sense, the senses summing to 0, the lists equal to the legend's counts",
    ),
    "tests/test_the_readers_tables.py::test_the_tracks_the_distance_the_dilation_and_the_spacing_read_the_bodies_and_light_by_hand": (
        97,
        "the same tables on the bodies and light: the tracks per identity with the where per close, the distance A to B falling from 2 to 1 Links at the slope -1 / 8 Links per interval and B to C standing at 1 Link across the torus's edge by name, "
        "the dilation at every where against the nodes log's pace within one interval at seven wheres and off by three at one, light's spacing against e^U longer where e^U is smaller on both sides of the return",
    ),
    "tests/test_the_readers_tables.py::test_the_back_in_time_window_runs_forward_to_k_with_no_snapshot_then_the_window_forward_and_back": (
        14,
        "the window of tools/back_in_time.py (--from K, 2026-10-24): the bare 3-cube forward to 4 with no snapshot, then 4 forward and 4 back, MATCH at the window's first interval with the report's `from`, the plain run's report as before",
    ),
    "tests/test_the_readers_tables.py::test_the_seven_tables_read_the_committed_record_through_the_command_line": (
        25,
        "the smoke check: the reader's command line with the eras and nodes logs beside the committed record, 26 epochs over 7 cycles, the ledger's 7 rows with nothing erased, 125 proton lists, the tracks and the clock tables unreadable with their keys named",
    ),
    "tests/test_the_readers_tables.py::hand_log": (
        39,
        "the helper of the tables' tests: the hand log written to a file, light's credits at eight closes over four Nodes, the body A moving one Link toward the bound body B, the body C bound a Link from B across the torus's edge, three births and two lays",
    ),
    "tests/test_the_readers_tables.py::era": (
        19,
        "the helper: one eras line by hand, the volume rising to 180 at 8, falling to 110 at 15 and rising again, one fire at the top, the quanta per family stepping at the births, the holder's one quantum spent at the return",
    ),
    "tests/test_the_readers_tables.py::birth": (
        11,
        "the helper: one birth line by hand with its children's records and points",
    ),
    "tests/test_the_readers_tables.py::credit": (
        7,
        "the helper: one credit line by hand with the click's view's eight keys, the board's own for light and `body n` for a body",
    ),
    "tests/test_the_readers_tables.py::node_line": (
        6,
        "the helper: one nodes line by hand, the Link's length 1 everywhere but at three Nodes",
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
