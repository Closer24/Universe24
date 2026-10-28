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
TENSOR24_FRAME = "Tensor24's frame, stage 0 of the build the owner approved at 16:0x UTC on 2026-10-28 (\"Approved, build it. You on the engine. Animate on the decoder.\"): the property tests of the plan's section 13 (locality, purity, rename, the 24's images, the formula against a naive model, bijectivity both ways) on a trivial engine, Fredkin's second-order form, each failing on its own mutant; the Boss's room by name."
ROOM = {  # the room given by name: the test, its lines and the reason (ENGINE.md, section 9)
    "tests/test_the_tensor24_frame.py::board": (
        5,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::trivial": (
        3,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::untrivial": (
        3,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::mutants": (
        12,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::local": (
        6,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::pure": (
        5,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::renamed": (
        5,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::turns": (
        9,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::turned": (
        10,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::naive": (
        6,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::formula": (
        3,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::bijective": (
        4,
        TENSOR24_FRAME,
    ),
    "tests/test_the_tensor24_frame.py::test_each_property_holds_on_the_trivial_engine_and_fails_on_its_mutant": (
        7,
        TENSOR24_FRAME,
    ),
    "tests/test_the_record.py::test_one_big_bang_recurs_within_its_integers_and_spreads_its_matter_alike": (
        26,
        "The one big bang on the great clock (the owner's word of 2026-10-27, 18:5x UTC: the whole system one great clock that runs the small clocks, priority to what makes the one big bang; his rule of 14:5x UTC that a push's test sees what it was pushed for): 20 bangs in 100 ticks within 128 bits under the three bounds, the held field in its universe, and under the order-free click and the one mirror its seed's symmetry standing through the run, every family born chiming one mesh apart at the board's own share exactly (the heavy family bound above it before them, the order's reading); the Boss's room by name.",
    ),
    "tests/test_the_record.py::test_the_books_close_at_every_click_mergers_and_lays_alike": (
        26,
        "The close's books at every click (the owner's yes of 2026-10-27, 15:5x UTC to the unspringing carrying its excess in the signed remainder; the temperature builder's finding, 68 of 70 clicks with a merger off; his rule of 14:5x UTC that a push's test sees what it was pushed for): on the hole's first 30 ticks (the bang's merging nothing under the order-free click) the board's wind lost is the chimes' booked plus the remainder's rise at every click, mergers among them; the Boss's room by name.",
    ),
    "tests/test_the_record.py::test_the_hole_falls_through_its_bottom_and_runs_on_and_back": (
        17,
        "The great clock whole through the bottom (the owner's word of 2026-10-27, 18:5x UTC: a whole engine that runs one big bang; the Boss's finding of 2026-10-28, 00:5x UTC): the bang's seed at 40 times its quanta stopped at tick 23 with a division by 0, a clock's stretch carried through its bottom within the tick and the end's mean teeth at or below 0 there; the start's teeth read at such a clock (Tick.end_teeth), the bang runs on and back exactly; under the one mirror and the order-free click the hole falls through its bottom at its ticks 12 and 18 to 22 and the bang no more, so the hole runs it; the Boss's room by name.",
    ),
    "tests/test_the_record.py::test_the_bang_without_the_held_field_chimes_every_family_it_bears_and_a_weightless_field_is_refused": (
        14,
        "The control of the nuclear binding (the owner's rule of 2026-10-27, 14:5x UTC that a push's test sees what it was pushed for): the same bang with no held field chimes on every family it bears under the order-free click (the near-light family alone before it, the order's; the two heavy families under the fair draw), and a weight on a hand and a held field with no weight are refused by name; the Boss's room by name.",
    ),
    "tests/test_the_record.py::test_the_light_is_polarized_along_its_sources_current_at_the_detectors_chimes": (
        38,
        "The polarization of light seen at the chimes (the owner's words of 2026-10-27, 14:32 and 14:5x UTC, the four phenomena on the board after the chimes, and his rule of 14:5x UTC that a push's test sees what it was pushed for; David's DAVID-FOUR-PHENOMENA.md section 1, toys-5 96caee2d8): the offset's transverse odd gears at a neutral bob's chimes follow the current of a charged source two clocks away, along x and, turned a quarter about the line of sight, along y, and stand equal at rest; the run along y the exact image of the run along x under the swap of x and y at every tick, every train's gears at every clock and every chime's clock (a mirror of the cube, the merger's cross term booked at the fitting's own clock, David's DAVID-THE-ONE-MIRROR.md, the owner's word of 2026-10-27, 18:5x UTC: the rule violations the Scribe found fixed where possible); the world as written runs back exactly; the Boss's room by name, widened from 21 to 38 lines for the swap's images.",
    ),
    "tests/test_the_record.py::test_the_beat_is_the_hands_own_and_a_quarter_turn_of_the_hand_moves_no_chime": (
        16,
        "The beat read free of the phase (the owner's word of 2026-10-27, 15:5x UTC, through the Boss's recommendation; David's DAVID-OWN-BEAT.md, toys-5 ce1d65fce; the owner's rule of 14:5x UTC that a push's test sees what it was pushed for): a quarter turn of the chiming hand at the setting moves no chime on the plasma, the pair and the two hands of the 3-cube, the pair turned onto its twelve gear chiming as on its three gear, the rewind exact with the beats' references in the state; the Boss's room by name.",
    ),
    "tests/test_the_record.py::test_spin_one_half_reads_minus_one_after_one_turn_and_comes_home_after_two": (
        32,
        "Spin one half seen on the great clock (the owner's rule of 2026-10-27, 14:5x UTC: a push's test sees what it was pushed for; David's DAVID-SPIN-IN-CLOCKS full turn, toys-5 e22420aee): the twins' overlap with the free run below -1/2 after one turn of the spin and above +1/2 after two, S_z home after one; the twin-hands test above it given 7 lines more for Pauli by the sweep (one fitted quantum's sweep per hand per clock at every tick); the Boss's room by name.",
    ),
    "tests/test_the_record.py::test_a_train_of_four_gears_at_a_spring_is_twin_hands_and_keeps_the_spin": (
        31,
        "Spin one half on two hands (David's DAVID-SPIN-SOLVED.md, toys-5 67f2ff192, on the owner's words of 2026-10-27, 12:02 UTC, built by the Boss on the clock engine): a train of four gears at a spring read as twin hands, every fitting's two children in twin hands, every unspringing across them, the rewind exact over 20 ticks of the node world (a fitting group of two children at one clock undone by its one take once); a law of the engine never roomed before, the Boss's room by name.",
    ),
    "tests/test_the_phase_line.py::test_the_standard_length_is_the_rims_and_the_engine_refuses_a_scale_below_the_floor_from_gamma": (
        20,
        "The standard's length derived from the rim, X = Gamma rim, and the declared amplitude refused by name (David's DAVID-AMPLITUDES.md section 4, toys-5 6415deeb0, on the owner's word of 2026-10-27, 12:4x UTC, and his rule of 11:3x UTC, no declarations; the former test of the amplitude declared from outside, 19 lines, re-cut): the floor 23 Gamma derived from Gamma alone, the refusal below it by name and never nature's; the Boss's room by name",
    ),
    "tests/test_rule3.py::test_a_hands_wind_is_a_gaussian_norm_and_its_quanta_are_its_sweep": (
        21,
        "The amplitudes as the hand's norms (David's DAVID-AMPLITUDES.md sections 1 and 5, on the owner's word of 2026-10-27, 12:4x UTC, and his rule of 14:5x UTC that a push's test sees what it was pushed for): every sprung hand's even rest wind is the Gaussian form exactly and SPOKES s |W| plus the lay's two remainders, its quanta its sweep in e, the winding 3 T s; the Boss's room by name",
    ),
    "tests/test_the_phase_line.py::test_the_reversal_is_bit_exact_over_ten_thousand_acts": (
        18,
        "The phase act's reversal bit exact over ten thousand acts (the law's own time reversal on the phase line, CA-S1's direction as the slot; a test of the law never roomed, standing since the phase line entered): the Boss's room by name at the merge of toys-5 e48273be8 (2026-10-27), the test as the merged tree holds it",
    ),
    "tests/test_the_record.py::test_the_exact_return_is_the_seeds_first_state_and_the_horizon_standing": (
        26,
        "The exact return read as the seed's own first pair of states, with a released horizon standing while frozen (2026-10-26, the owner's words of 19:4x and 21:3x UTC through the Boss, the Reader's reading on reader-5 daecb7deb): the returns numbered on the bang records and the horizon's silence read from the Node lines; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_record.py::test_the_momentum_booked_on_the_link_is_an_identity_on_every_booking": (
        17,
        "LT-S1 read on a whole record rather than at one Node (2026-10-26, the Boss's road for the Reader): the booking on the carrier's flux line an identity per axis at every booking of the record; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_record.py::test_the_horizon_is_read_from_the_node_lines_not_the_rows": (
        16,
        "The first of the two reader bugs that hid a horizon (2026-10-26, The-Horizon-On-The-Returning-Board_COMPARISON.md section 2): the content's maximum read from the Node lines and never from the reader's rows, so a horizon shorter than a twelfth of the run is seen; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_record.py::test_the_page_of_the_bangs_is_one_html_from_the_records_and_the_readings": (
        15,
        "The one page of the bangs (2026-10-26, the owner's words of 19:4x and 21:3x UTC through the Boss): the three bangs played side by side with their numbers, what each brings and lacks, and every numbered row by family, written from the records and the readings alone; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_board.py::laid": (
        22,
        "A helper of the board tests, the lay read back from a world (2026-10-26, the Reader's merge of the folds): one lay built and read in one place for the tests that need it, in place of a copy per test; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/laws.py::wronskian": (
        3,
        "A helper of the law's tests (2026-10-26, the Reader's merge of the folds): the phase line's two solutions read for their constant, named once in tests/laws.py so no test carries its own copy; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_board.py::centroid": (
        7,
        "A helper of the board tests (2026-10-26, the Reader's merge of the folds): the share's centroid read in thousandths of a Link, named once for the moving lay's tests; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_node.py::exchanged": (
        15,
        "A helper of the Node's tests (2026-10-26, the Reader's merge of the folds): the slot exchange of a state read in one place, the law's own time reversal, for the tests that compare the two ends; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_rule3.py::test_every_move_of_the_close_books_its_momentum_on_the_flux_line_as_an_identity_lt_s1": (
        39,
        "LT-S1 (2026-10-26, the owner's word of 08:4x UTC, 'approve', the Boss's order 6411867383: the hand's one-Node test under its room; H-Lay-As-The-Take-Reversed-1): every move of the close books its momentum on the carrier's flux line by the Node's write act, the identity per axis at every booking on the hole seed's 14 intervals, the run back exact; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_node.py::test_the_turn_at_the_horizon_runs_back_exact": (
        11,
        "FR-S1's second test (2026-10-26, the owner's word of 07:3x UTC 'enter now', the frozen Node released by the turn of its time; the Boss's room at the merge of reader-5 a77fde969 carrying toys-5 3d7729581): the turn at the horizon run back exactly",
    ),
    "tests/laws.py::level_at": (
        7,
        "the level of a volume as one shared builder of tests/laws.py (2026-10-26, David's move of the helper out of a test at 3d7729581; the Boss's room at the merge of reader-5 a77fde969): read by the tests of the volumes and the metric lines",
    ),
    "tests/test_rule3.py::wrapped": (
        14,
        "TC-S1's helper (2026-10-26, the owner's word of 08:3x UTC; the Boss's room at the merge of reader-5 a77fde969 carrying toys-5 3d7729581): the hole seed's walls wrapped for the take count's one-Node test",
    ),
    "tests/test_rule3.py::test_the_take_count_is_one_carried_division_of_the_walls_by_the_price_tc_s1": (
        42,
        "TC-S1 (2026-10-26, the owner's word of 08:3x UTC, 'approved', the Boss's order 6411031946 under the owner's delegation: the hand's one-Node test under its room; H-Take-Count-As-Rule3-Division-1): the take's count one carried division of the walls by the price of one level, iterated from below, no root, on the hole seed's 47 first takes at the trace 6; widened at the merge of reader-5 a77fde969 carrying toys-5 3d7729581 (2026-10-26, the Boss's room by name): the test as it stands on the merged tree",
    ),
    "tests/test_the_node.py::test_the_take_keeps_its_remainder_at_the_node_and_pays_exactly_ex_s1": (
        40,
        "EX-S1 (2026-10-26, the Boss's order of 03:3x UTC under the owner's delegation, 6407630119 and 6405916579: the room 40 named; H-Exact-Take-Remainder-1's one-Node test): the take's remainder at the Node, the identity fall + remainder before - remainder after = booked at twenty takes, the undo to the hash",
    ),
    "tests/test_the_board.py::test_the_six_metric_lines_are_written_read_and_run_back_exactly_through_a_top_y_s3": (
        60,
        "Y-S3 (2026-10-26, the Boss's order of 03:3x UTC under the owner's delegation, 6407630119; H-Six-Metric-Lines-3's test with its room): the six metric lines written from the Node's own flux and shears, read by the fold at the rest rotation, run back exactly through a top; the hole at 20, the sea's return, the one-Link reach; widened at the merge of reader-5 a77fde969 carrying toys-5 3d7729581 (2026-10-26, the Boss's room by name): the test as it stands on the merged tree",
    ),
    "tests/test_the_board.py::test_the_pair_at_rest_merges_into_light_by_its_own_quantum_taken_whole_mg_s1": (
        45,
        "MG-S1 (2026-10-26, the Boss's order of 01:03 UTC under the owner's delegation, 6405916579 and 6404745207: the room 45 named; H-Merger-At-Rest-1's REPORT.md): the child's own quantum as the wall, the pair at rest met by its charges, the whole take at -1 and the stop, on the cycle board at 6 and the bare 5-cube's pairs",
    ),
    "tests/test_the_node.py::test_the_files_are_refused_by_name": (
        46,
        "The loader's refusals by name (2026-10-26, the Boss's room at the merge of toys-5 50c73c972: the fifth form wave admitted by CS5-S2 and the former refusal of the word wave struck, so the test names one more refusal, "
        "the cycle form at its quanta; with it the six module-level lines the finders' rename and CS5-S2's imports added to tests/test_the_board.py and tests/test_the_node.py)",
    ),
    "tests/test_the_board.py::test_one_pair_in_several_rows_births_the_conjugate_pair_at_every_node_cs5_s2": (
        51,
        "CS5-S2 with the fifth form wave (2026-10-25, the owner's word of 22:50 UTC, The-Handed-Seed-And-Births_COMPARISON.md; the Boss's room named in 6404974647 and 6405218245): one pair in several rows admitted, the file's cycle form laid, the loader's refusals by name, the board's course on the head",
    ),
    "tests/test_the_node.py::test_the_unit_the_emitter_and_the_identity_turn_are_values_of_the_pair_un": (
        30,
        "The gap-0 finders (2026-10-26, the owner's word of 23:40 UTC, The-Unit-And-The-Coupling_COMPARISON.md section 4; the Boss's room named in 6405000794 and 6405218245): the twelve branches on the gap folded to the pair's values (the unit, the emitter, the coupling and its identity turn) shown on the three records bit for bit and the loader's refusals by name",
    ),
    "tests/test_the_node.py::test_the_take_moves_the_line_farthest_from_its_before_and_logs_it_per_take_cs4_s2": (
        56,
        "CS4-S2 (2026-10-25, the owner's word of 22:50 UTC, The-Handed-Seed-And-Births_COMPARISON.md; the Boss's room of 40 named in 6404974647 for the cycle board at 6 intervals; this test's 56 asked in David's line: the pair beside its quarter-turned image, the 81 credits equal take for take, and SL-S2's merger board with every take's line re-derived by hand), the one take rule",
    ),
    "tests/test_the_board.py::test_the_plasma_retraces_bit_for_bit_and_returns_to_gamma_exactly_pl_s1": (
        37,
        "PL-S1 (2026-10-25, the owner's word of 22:50 UTC, The-Plasma-Charge-At-The-Kick_COMPARISON.md; the Boss's room named in 6404974647 at the merge of toys-5 99a9ee860): nature's plasma on the 3-cube returning to Gamma exactly "
        "at 166 and 167 with every credit laid back, the retrace the engine's own exchange at every k, the run back exact through the top",
    ),
    "tests/test_rule3.py::test_the_composed_paces_are_the_laws_carried_division_at_gamma_squared_bit_for_bit_the_power": (
        29,
        "the composed paces (2026-10-25, PC-S1 in pc1's form, the owner's word K-S4 through the Boss; the room given at the merge of toys-5 84009e333): the clock the exact power rounded half up once by the carried division "
        "at the resolution Gamma squared, bit for bit at every content to the edge, the Link's pace the clock twice",
    ),
    "tests/test_the_node.py::test_the_horizon_holds_the_links_at_the_wall_and_the_node_births_nothing": (
        18,
        "the horizon (2026-10-25, BH-S1's second test, the Boss's room at the merge of toys-5 84009e333): the frozen Node's Links held at the wall and no birth at it; widened at the merge of reader-5 a77fde969 carrying toys-5 3d7729581 (2026-10-26, the Boss's room by name): the test as it stands on the merged tree",
    ),
    "tests/test_the_record.py::test_the_record_carries_a_node_line_per_interval_and_the_reading_its_events": (
        30,
        "the record's Node lines and the reading's event lines (2026-10-25, the owner's word through the Reader, every gate its event line; the Boss's room at the merge of toys-5 84009e333, 20; widened by 3 at the merge of reader-5 becc47f4d, 2026-10-26, the events read per record of the reader folder): "
        "one Node line per interval and the events the page labels"
        ". Widened to 30 at the merge of reader-5 f1e5d5b68 (2026-10-26, the Boss): the events of rows 62 to 67.",
    ),
    "tests/test_the_record.py::test_the_page_is_one_html_from_the_record_and_the_reading_with_nothing_typed": (
        14,
        "the page (2026-10-25, the third tool of the standard, the owner's word through the Boss; the Boss's room at the merge of toys-5 84009e333): one HTML from the record and the reading with nothing of a universe typed",
    ),
    "tests/test_the_record.py::test_the_gates_of_the_phenomena_are_one_table_written_from_the_readings": (
        24,
        "the table of the phenomena (2026-10-26, the fourth tool of the standard, tools/phenomena.py, the owner's word through the Boss; the Boss's room at the merge of reader-5 becc47f4d): "
        "every row of the gates in one table written from the readings, the SHOWN count on the head and the document's section rewritten from it"
        ". Widened to 24 at the merge of reader-5 f1e5d5b68 (2026-10-26, the Boss): the rows' count read from the readings, the one shape for every row.",
    ),
    "tests/test_the_record.py::test_the_committed_record_shows_the_gates_by_name": (
        11,
        "the rows 62 to 67 and the SHOWN sets per record (2026-10-26, the owner's words of 07:04 and 07:24 UTC through the Reader; the Boss's room at the merge of reader-5 f1e5d5b68): the arrow of time, the uniformity in the clicks, dark matter in kind, the lepton number, the energy in the clicks, CPT as one row, each a function of the reading",
    ),
    "tests/test_the_record.py::test_the_conservations_hold_on_the_record": (
        18,
        "gate 47 on the births of a pair with EX-S1's identity and the charge read from the children's own senses (2026-10-26, the Reader's strokes 3 and 4 and the readers' charge bug, H-Children-Charge-Bug-1; the Boss's room at the merge of reader-5 f1e5d5b68)",
    ),
    "tests/test_the_board.py::test_the_body_at_rest_lays_back_what_it_takes_and_the_light_stays_whole_eq_s1": (
        26,
        "EQ-S1, the body at rest lays back what it takes (David's test of 2026-10-25, never given a room by name; the Boss's room at the merge of reader-5 f1e5d5b68 carrying toys-5 3dc12e307)",
    ),
    "tests/test_rule3.py::test_no_integer_beyond_the_laws_own_enters_the_engine_or_the_tools": (
        56,
        "the integer gate's own test, grown with symmetries.py's three refusals (2026-10-26, the Reader's rows 63 to 67; the Boss's room at the merge of reader-5 f1e5d5b68): no integer beyond the law's own in the engine or the tools",
    ),
    "tests/test_the_record.py::test_the_committed_reading_is_the_decoders_own_whole": (
        3,
        "the whole reading (2026-10-26, the Reader's one check of every key, number, verdict, field and event; the Boss's room at the merge of reader-5 becc47f4d): the committed reading beside the record equal to a fresh read line for line",
    ),
    "tests/test_the_node.py::test_the_born_pair_meets_at_the_next_close_with_no_current_and_is_refused_by_the_orientation_sl_s1": (
        27,
        "SL-S1 (2026-10-25, the Boss's 6399718139, The-Merger-As-The-Birth-Reversed_COMPARISON.md section 4: the generic close's one-Node test under 15 s): the chiral seed on the 3-cube at 30 intervals, "
        "every born pair's Link meeting at the next close with no current and refused by the orientation (5 of 5), the meetings counted, the run back exact; widened at the merge of reader-5 a77fde969 carrying toys-5 3d7729581 (2026-10-26, the Boss's room by name): the test as it stands on the merged tree; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_node.py::test_the_merger_takes_one_light_quantum_at_each_end_of_the_pair_and_lays_the_light_sl_s2": (
        46,
        "SL-S2 (2026-10-25, the Boss's ledger item 10, The-Merger-As-The-Birth-Reversed_COMPARISON.md: the test under 15 s): the heaviest record's conjugate pair fed at two adjacent Nodes of the bare 5-cube at 20 intervals, "
        "one merger (the taken row the heaviest record, the children the gap-0 row), each child's wall one light quantum to the rounding paid by one exact take at its own end, the gap-0 row whole at each end, the charge 0, the stop by name, the run back exact; widened at the merge of reader-5 a77fde969 carrying toys-5 3d7729581 (2026-10-26, the Boss's room by name): the test as it stands on the merged tree",
    ),
    "tests/test_the_node.py::test_the_bodies_closing_clicks_on_the_zero_crossing_in_either_direction_ck_s1": (
        44,
        "CK-S1 (2026-10-25, the owner's word of 17:57 through the Boss, 6401141446; ck1's REPORT.md section 4: the test under 15 s): the crossing read in either direction, even under the negation of the line, "
        "at one Node fed a plane's re line at rest over the period 6 and its negation (the counters equal step for step, the beat 3, the half period), and the chiral 5-cube at 20 intervals with every plane credit's beat the count between the two latest zero crossings of its re line read by hand, credits on a downward crossing among them, the run back exact; widened at the merge of reader-5 a77fde969 carrying toys-5 3d7729581 (2026-10-26, the Boss's room by name): the test as it stands on the merged tree",
    ),
    "tests/test_the_node.py::test_the_charge_is_one_e_for_every_row_at_the_lay_ms_s1": (
        17,
        "MS-S1 (2026-10-25, the owner's word through the Boss, 6399410929, The-Masses-From-The-Clicks_COMPARISON.md section 5: the test under 15 s beside the sentence): the lay's pair (A, B) with A B = T div 2 from T alone, "
        "the chiral 5-cube at 12 intervals with every child's Wronskian +-(T div 2) where its plane stood at nothing, the senses opposite and summing to 0, taken at or above booked, the run back exact",
    ),
    "tests/test_the_node.py::test_the_swap_keeps_the_charge_of_every_plane_at_every_turned_node_ws": (
        35,
        "WS (2026-10-25, the Boss's 6400357538, The-Swap-Keeps-The-Charge_VERDICT.md section 4: the test under 15 s): the reading Node within the test (its click reads W of the held pre-state against W after the swap at every turned Node and every plane before it lays), the Boss's 3-cube to 60 and the chiral 5-cube at 20, kept = sites, negated 0, changed 0, the nonzero sites counted; widened at the merge of reader-5 a77fde969 carrying toys-5 3d7729581 (2026-10-26, the Boss's room by name): the test as it stands on the merged tree",
    ),
    "tests/test_the_board.py::test_the_uniform_pair_at_every_node_returns_with_the_whole_board_turning_at_once_ma": (
        27,
        "MA-S1 (2026-10-25, the Boss's 6400767119 (4), Matter-And-Antimatter-At-Every-Node_COMPARISON.md section 4: the test under 15 s): the pair at every Node of the 3-cube by the file's `at` lays to 400, every Node alike, the whole board turning at once at the top, births 0, the bottom named against Gamma, the run back exact",
    ),
    "tests/test_the_board.py::test_the_bare_sea_returns_exactly_with_the_whole_board_turning_at_once_bb": (
        22,
        "BB-S1 and MA-S1 (2026-10-25, the Boss's 6400540638 and 6400767119 (2), The-Uniform-Board-Returns_COMPARISON.md section 4: gate 1 from the Node lines, the test under 15 s): the sea on the 3-cube to 240, the exact returns at 115 and 230, the whole board turning at 58 and 173, the bangs numbered, no birth between",
    ),
    "tests/test_the_board.py::test_the_moving_lay_runs_at_its_momentum_over_twice_its_share_mv": (
        64,
        "MV-S1 to MV-S3 (2026-10-25, the Boss's ledger item 7, The-Moving-Lay-With-A-Wave-Number_COMPARISON.md section for David: the test under 15 s): the heavy row's pair of 3 quanta laid with a wave number under the sea on the 9-cube, "
        "W 0 at every Node, the share centroid's step at each of the first four closes against (1000 P) div (2 E) within 40 milli by cross multiplication, the top's value above, wave 0 hash-equal to no wave, the four refusals by name, the run back exact through 10; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_board.py::test_the_moving_lay_is_carried_by_the_48_with_its_centre_and_wave_mv": (
        57,
        "MV-S1 (2026-10-25, vf5's item (a) through the Boss, 6401916517; The-Moving-Lay-With-A-Wave-Number_COMPARISON.md's spec: the 48 with the centre and the wave transformed, under 15 s): the moving lay on the 5-cube at two intervals against its 48 images carried back, 24 and 24, 0 apart",
    ),
    "tests/test_the_node.py::shares_of": (
        11,
        "PM-S1 (2026-10-25, the owner's word through the Boss, 6399410929, The-Count-In-The-Carriers-Unit_COMPARISON.md section 5: the tests under 15 s beside the sentence): the helper, the gap-0 line's share in the carrier's unit and by hand at the frame's and the vacuum's weights",
    ),
    "tests/test_the_node.py::test_every_count_is_read_in_the_carriers_unit_pm_s1": (
        35,
        "PM-S1 (2026-10-25, the owner's word through the Boss, 6399410929, The-Count-In-The-Carriers-Unit_COMPARISON.md section 5: the tests under 15 s beside the sentence): the identity Gamma^2 div p_i^2 = X div Gamma, the 3-cube hole's shares at 1 and at 20 against the frame's and the vacuum's, the chiral 5-cube at 60 by pm2's numbers; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_quartet.py::toy_of": (
        9,
        "the shape-8 row (2026-10-25, the Boss's order 6398593790 (3) and The-Spinor-Row_COMPARISON.md's spec: the five tests under 15 s beside the row): the helper, the toy on the middle universe with the shape-8 row, one packet along a vector with the controls",
    ),
    "tests/test_the_quartet.py::lines_of": (
        3,
        "the shape-8 row (2026-10-25, the Boss's order 6398593790 (3) and The-Spinor-Row_COMPARISON.md's spec: the five tests under 15 s beside the row): the helper, the row's lines",
    ),
    "tests/test_the_quartet.py::test_the_zeeman_doublet_is_the_derived_shift_with_the_two_spins_opposite_sr_s3": (
        19,
        "the shape-8 row (2026-10-25, the Boss's order 6398593790 (3) and The-Spinor-Row_COMPARISON.md's spec: the five tests under 15 s beside the row): the Zeeman doublet, the one-interval shifts of the two spins opposite and within one level of the derived num B0 x_now div (3 den Gamma)",
    ),
    "tests/test_the_quartet.py::test_the_negated_vector_lays_the_lay_negated_with_the_charge_the_share_and_the_credits_equal_sr_s2": (
        23,
        "the shape-8 row (2026-10-25, the Boss's order 6398593790 (3) and The-Spinor-Row_COMPARISON.md's spec: the five tests under 15 s beside the row): the double cover's -I, the negated vector's lay the lay negated with the share, the charge and the credits equal line for line, the run back exact",
    ),
    "tests/test_the_quartet.py::test_the_quartet_sees_one_link_sr": (
        11,
        "the shape-8 row (2026-10-25, the Boss's order 6398593790 (3) and The-Spinor-Row_COMPARISON.md's spec: the five tests under 15 s beside the row): the reach, an odd line changed two Links away leaves the row's eight lines bit for bit",
    ),
    "tests/test_the_quartet.py::test_the_exclusion_at_the_lay_reads_the_full_state_and_the_pile_is_gone_sr_s4": (
        24,
        "the shape-8 row (2026-10-25, the Boss's order 6398593790 (3) and The-Spinor-Row_COMPARISON.md's spec: the five tests under 15 s beside the row): the exclusion at the lay per full state, the pile 1x refused like, 2x opposite spins, 4x by hand, the neutral pair, the refusals by name",
    ),
    "tests/test_the_quartet.py::test_stern_gerlach_reads_the_credits_centroids_per_spin_sign_along_the_gradient_sr": (
        21,
        "the shape-8 row (2026-10-25, the Boss's order 6398593790 (3) and The-Spinor-Row_COMPARISON.md's spec: the five tests under 15 s beside the row): the Stern-Gerlach gate read from the toy's committed records of the 9-cube at 60 intervals, the verdict asserted by name",
    ),
    "tests/test_the_node.py::test_the_frozen_node_rests_and_its_links_stand_at_the_wall_bh_s1": (
        28,
        "BH-S1 (2026-10-25, the owner's word through the Boss, 6398593790: the test under 15 s beside the frozen Node's): the 3-cube centre fed to the frozen content for 100 intervals, "
        "its lines and proper count unchanged, the twelve factors 0, no click, the frozen count 1, the width held, the run back exact 100 of 100; widened at the merge of reader-5 a77fde969 carrying toys-5 3d7729581 (2026-10-26, the Boss's room by name): the test as it stands on the merged tree; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_the_board.py::test_the_merger_lays_light_of_no_charge_at_both_ends_cc1": (
        20,
        "H-Children-Charge-Bug-1 (2026-10-26, the Boss's 6410696786: the one-Node test under 1 s, three pins): the chiral's merger of the interval 10 fed on the 3-cube, "
        "the light the exact take at -1 at both ends, the children's own charge 0; widened at the merge of reader-5 a77fde969 carrying toys-5 3d7729581 (2026-10-26, the Boss's room by name): the test as it stands on the merged tree",
    ),
    "tests/test_the_board.py::test_a_frozen_node_is_released_by_the_turn_of_its_time": (
        24,
        "FR-S1 (2026-10-26, the owner's words of 03:41 and 07:3x UTC through the Boss, 6407706168 and 6410516303: the test under 3 s beside BH-S1's): the 3-cube centre fed to the frozen content with its before below it, "
        "frozen and turned at the first interval, released with its clock running at the second, no Node frozen twice in a row, the width held, the run back exact 20 of 20; widened at the merge of reader-5 a77fde969 carrying toys-5 3d7729581 (2026-10-26, the Boss's room by name): the test as it stands on the merged tree; the Boss's room by name at the merge of reader-5 f0c47f489 carrying toys-5 9c2198f34 (2026-10-26): the test as the merged tree holds it",
    ),
    "tests/test_rule3.py::test_the_one_rule_of_the_remainder_is_one_primitive_and_every_rounding_odd": (
        19,
        "the one rule of the remainder (2026-10-25, the owner's word through the Boss, 6398455072: the identities as a test under 15 s): the mirror once per reversal and the identity for an even count, "
        "the coefficient's rounding the carried division from the half wall with the carry mirrored, odd at every integer, the turn's and the kicks' roundings a fold, the origin pair",
    ),
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
    "tests/test_the_features.py::test_the_two_signed_roundings_are_odd_half_away_from_zero_at_a_tie": (
        46,
        "the odd rounding of the two signed coefficients (2026-10-25, the owner's word on two blind hands' derivation): paces.odd_rounded equal bit for bit to sign(x) rounded(|x|, wall) and to "
        "phase.signed_rounded over a sweep of walls and kinds, odd at every integer; the turn's factor odd at the tie 2 L p_0 = Gamma mod 2 Gamma derived in the test and across a sweep "
        "where the half-up rounding is not; the write's fixed-wall ratio odd at a tie through records.write_sources at the vacuum's paces",
    ),
    "tests/test_the_node_holds_the_same_count_of_integers.py::test_every_node_holds_the_same_count_of_integers_and_the_count_grows_by_a_point_at_a_birth": (
        41,
        "the generic Node's gate (2026-10-25, the plan's stage 0): the integers one Node holds read by tools/node_integers.py loaded by its path on the bare 3-cube at den 1,021 and at the top tier's den, "
        "never the shipped file; the rows' 35 derived and read at every Node before the first birth, every array of the board's shape, the growth at the first birth by 52 per record born, "
        "the three lifts' growth at the top tier's den by the interval 8, the largest bit length within 128 at both dens and the shipped den's half wall above it, the two deviations kept by name",
    ),
    "tests/test_the_generic_node_toy.py::test_the_node_fed_the_boards_own_shells_is_the_boards_centre_bit_for_bit_and_runs_back_exact": (
        52,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the calibration, the centre fed the board's own shells is the board's centre bit for bit through the first birth and runs back exact",
    ),
    "tests/test_the_generic_node_toy.py::test_rule3_at_the_node_is_the_six_fed_arrivals_division_on_each_line_and_its_inverse": (
        52,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): Rule3 on each line from six fed arrivals by hand and its inverse",
    ),
    "tests/test_the_generic_node_toy.py::test_the_clock_is_the_nodes_and_the_tension_is_the_links_read_the_same_from_both_ends": (
        40,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the clock the Node's and the tension the Link's, the same from both ends",
    ),
    "tests/test_the_generic_node_toy.py::test_the_node_sees_one_link_a_change_at_the_edge_and_corner_nodes_leaves_its_interval": (
        23,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the one-Link reach at the Node, the edge and corner Nodes' change leaving the centre, a face neighbour's the positive control",
    ),
    "tests/test_the_generic_node_toy.py::test_the_held_write_at_the_node_is_the_form_and_the_stresses_over_the_fixed_wall_once_and_its_inverse": (
        51,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the volume's write from the by-hand form and the stresses, the remainder within its wall, the inverse",
    ),
    "tests/test_the_generic_node_toy.py::test_the_signs_row_is_the_wronskian_and_no_record_reads_its_own_row": (
        76,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the sign's row from the Wronskian and the record's read excluding its own row",
    ),
    "tests/test_the_generic_node_toy.py::test_the_phase_act_at_the_node_is_the_clocked_potential_and_the_counts_along_the_orbit": (
        68,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the phase act, Phi_next = 2 Phi_now - Phi_before + the turn factor, the counts with the frame sign across a Link, the pair on the orbit",
    ),
    "tests/test_the_generic_node_toy.py::test_the_swap_at_a_fed_weak_maximum_and_at_the_floor_turns_the_node_alone_on_the_trigger": (
        86,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the swap at a fed weak maximum and at the floor, the complements at every wall, nothing off the trigger, the inverse",
    ),
    "tests/test_the_generic_node_toy.py::test_the_frozen_clock_has_no_share_and_is_read_by_no_meeting": (
        29,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the frozen clock",
    ),
    "tests/test_the_generic_node_toys_close_and_constants.py::test_the_clicks_read_at_the_node_is_one_number_of_the_fed_remainders_with_its_three_refusals_and_the_48": (
        99,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the click's read as one number by hand, its invariance under the 48 on the fed neighbours, the three refusals by name",
    ),
    "tests/test_the_generic_node_toys_close_and_constants.py::test_the_take_at_two_fed_quanta_pays_the_walls_lays_the_pair_and_refuses_stop_and_lay_by_name": (
        84,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the take and the lay at two fed quanta, the refusals stop and lay",
    ),
    "tests/test_the_generic_node_toys_close_and_constants.py::test_the_bodys_closing_at_the_node_reads_the_beat_and_writes_the_credit_or_refuses_stop": (
        90,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the body's closing, the beat by hand, the click at the period's close, the credit's readings",
    ),
    "tests/test_the_generic_node_toys_close_and_constants.py::test_constant_1_the_count_of_integers_at_the_node_is_the_rows_35_and_grows_by_52_per_record_born": (
        29,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): constant 1, the 35 derived from the rows and the 52 per record born named as the deviation",
    ),
    "tests/test_the_generic_node_toys_close_and_constants.py::test_constant_2_the_list_of_acts_is_the_same_for_a_feed_that_births_and_one_that_does_not": (
        51,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): constant 2, the trace of the acts the same for a feed that births and one that does not, the close's branches named",
    ),
    "tests/test_the_generic_node_toys_close_and_constants.py::test_constant_3_the_state_stands_within_128_bits_at_the_fed_extremes_and_the_transients_beyond_are_named": (
        100,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): constant 3, the state within 128 bits at the fed extremes, the transients beyond measured and named",
    ),
    "tests/test_the_generic_node_toys_close_and_constants.py::test_the_fold_on_the_one_node_torus_sums_the_links_to_zero_and_turns_at_the_pinned_rest": (
        45,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the fold on the 1x1x1, the Links' sum 0, a swap every interval",
    ),
    "tests/test_the_generic_node_toys_close_and_constants.py::test_the_48_at_the_node_carry_the_fed_shell_and_the_centres_outputs_alike": (
        29,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the 48 at the Node, the centre's outputs alike under the signed permutations of the fed shell",
    ),
    "tests/laws_universe.py::node_toy": (
        11,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the helper, the toy's board with the meetings restricted to the centre",
    ),
    "tests/laws_universe.py::node_arrays": (
        16,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the helper, every array of the state keyed",
    ),
    "tests/laws_universe.py::impose": (
        28,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the helper, the fed shell written at the 26 Nodes through new Records",
    ),
    "tests/laws_universe.py::fed_interval": (
        7,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the helper, the two-call interval with the shell imposed before the acts and before the close",
    ),
    "tests/laws_universe.py::at_centre": (
        3,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the helper, the arrays read at the centre",
    ),
    "tests/laws_universe.py::course": (
        18,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the helper, the plain board's own shells recorded per interval under a translation",
    ),
    "tests/laws_universe.py::shaken": (
        14,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the helper, a random fed shell on the light line and the volume",
    ),
    "tests/laws_universe.py::carried": (
        20,
        "the generic Node's toy (2026-10-25, the owner's word through the adviser: every property tested on one Node fed through its six Links): the helper, a fed shell under one of the cube's 48",
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
    "tests/test_the_properties_hold_on_a_run.py::test_the_links_lengthen_on_the_running_board": (
        20,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the Links lengthen on the running board: the hole seed's summed X never falls and ends above the seed's, every Node's X above Gamma at the end, the clock at or below Gamma where X is at or above it and below where X reads the first level, the clock non-increasing in X across the Nodes, the eras tool's length non-decreasing in X",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_the_lengthening_is_read_in_the_clicks": (
        13,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the lengthening in the clicks: at the Node credited most often the proper never outruns the interval and the last pair's pace delta proper over delta interval is at or below the first pair's and below 1",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_the_clock_reverses_at_a_nodes_own_top_on_the_course": (
        40,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the reversed clock on the course: at the first turned Node whose light moves, the fifth act's triple read by a spy fires where the board reads turned, the light's and the volume's levels the kept pair exchanged, the velocity negated, an unturned neighbour's level now not the kept before, one step back exact",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_the_uniform_sea_turns_at_every_node_at_once_and_runs_its_rise_back": (
        27,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the returns of the volume on the uniform sea: every Node turned in one interval, the state at t* + k the state at t* - 1 - k under the act's image until the mirror meets an act, the summed X largest at the top and falling after it; about 7 s",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_gravitys_sign_on_two_boards": (
        17,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "gravity's sign on two boards: the lone pair laid at the hole by the birth's own path, X there above the bare board's after the first interval and at the end, the proper count at or below the bare board's at every interval and below at the end, the run back exact",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_the_dilations_sign_by_hand": (
        15,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the dilation's sign by hand: the light emptied and the volume line at the cube's centre at the volume of the level Gamma div 10, the clock there below Gamma and Gamma elsewhere at the start, the proper count there below every other Node's after the cube's side of intervals",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_the_horizon_is_forced_at_the_wall": (
        51,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the horizon forced at the wall: the x axis line along the hole's ring at Gamma, Gamma and -Gamma puts one Link's tension at Gamma, its factor 0 and G^2 on every other Port by hand and by the engine, horizon_links names it alone, the +x neighbour steps as Rule3 by hand with that Port's reach 0 and not as the plain rule, the run back exact, half the wall re-couples",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_the_frozen_clock_holds_and_births_nothing": (
        26,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the frozen clock: the volume line at one Node at volume_of(Gamma, frozen_content(Gamma)), that Node alone frozen under the seed's read with its axis paces 0 and its X unchanged, no credit and no birth there at the first crediting close while its six neighbours are credited, the run back exact",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_the_whole_interval_reaches_one_link": (
        17,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the one-Link reach of the whole interval on the 3-cube and the 5-cube: the light raised by one level at one Node, after one interval the boards differ at the Node and its six neighbours alone, after the step back at the Node alone",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_the_uniform_sea_is_a_fixed_point_of_the_remainders": (
        32,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the uniform sea a fixed point of the remainders: to its first births the light's remainder at the half wall at every Node, every line alike at every Node, digits.at_origin at every frame, no credit; at the birth interval a birth at every Node alike",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_only_a_bound_body_clicks": (
        20,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "only a bound body clicks: every credit of the light at a birth at its Node, every other credit a charged plane record's with the kind its width, the massless pair no body",
    ),
    "tests/test_the_properties_hold_on_a_run.py::test_the_signs_write_travels_one_link_per_interval": (
        20,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the sign's write travels one Link per interval: the lone pair laid at the cube's centre, the holder's rows 0 before the first interval, non-zero at the Node alone after one and at the Node and its six neighbours alone after two",
    ),
    "tests/test_the_properties_hold_on_a_run.py::hole_run": (
        14,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the fixture: the hole seed stepped once for the module, the clocks and the volumes per interval and the output lines",
    ),
    "tests/test_the_properties_hold_on_a_run.py::hole_board": (
        8,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the helper: the hole seed on the bare torus in a folder with every output line kept",
    ),
    "tests/test_the_properties_hold_on_a_run.py::levels": (
        4,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the helper: a family's first line's two levels as Python's integers",
    ),
    "tests/test_the_properties_hold_on_a_run.py::pair_laid": (
        6,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the helper: the lone pair laid at one Node by the birth's own path",
    ),
    "tests/test_the_properties_hold_on_a_run.py::apart": (
        10,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the helper: the Nodes at which two states differ",
    ),
    "tests/test_the_properties_hold_on_a_run.py::mirrored": (
        17,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): "
        "the helper: the fifth act's image between two states, the levels exchanged and the plain remainders complemented",
    ),
    "tests/laws_universe.py::light_emptied": (
        7,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): the shared setup by hand, the light emptied so that nothing sources the held rows (the turn at the top and at the floor, the dilation's sign)",
    ),
    "tests/laws_universe.py::time_line_set": (
        10,
        "the properties hold on a run (2026-10-25, the owner's word: every property with a small test): the shared setup by hand, the first held row's time line set at every Node (the turn at the top and at the floor, the dilation's sign, the frozen clock)",
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
    return merge_base.base_ref()


def main() -> None:
    """Print every way tests/ has grown against the merge base and exit 1 where it has; nothing printed and exit 0 where the shape holds."""
    root = Path(__file__).resolve().parents[1]
    found = violations(working_tree(root), at_ref(root, base_ref()))
    print("\n".join(found) or "the shape of tests/ holds against the merge base")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
