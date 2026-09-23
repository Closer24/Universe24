# The register's sources are the paper's: the table before the deletion (the Register Architect, 2026-09-22)

The order: the model owner, 2026-09-22, about 08:57Z, record 871 of
[the log](../../LOG_2026-09-20.md): "It turns out we do not need the 32
crowd worlds at all. They are not in the paper. Start an architect to remove
worlds or experiments that are not in the paper. Order the new code of the
clicks. Old code goes." The Boss's frame (the order to this session): the
paper is the one course (record 606); its cited sources are the truth for
what stays; the table first, in one commit, then the deletions in order,
each green under `python tools/check.py --base origin/main`, nothing
deleted from Highlights or the logs, no physical behavior changed, and the
files of the branches in flight untouched until the Boss sends their merge
SHAs.

**The base commit:** `59c6b8112a76cb81370d032d5e4e02eebcba24cc` (origin/main,
PR #828 merged, 2026-09-22). **The branch:** `register-paper-sources`.

**The paper read:** branch `claude/paper-owner-review-five` (PR #802) at
`0406382f3700469b5459b9494ce8396e568f8b20` (2026-09-22, 08:50Z; the writer's
head after 678bb103), the files `paper/general_formula/main.tex`,
`NUMBERS.md`, `RECORD.md`, `checks/*.py`, `figures.py` and
`summarize_runs.py`. The head is read again before the deletion commits.

**The rule of reach**, applied to every path below. A world, a design, a
tool or a code path is reached by the paper when (i) main.tex, NUMBERS.md,
RECORD.md, a check script, figures.py or summarize_runs.py names it, its
series or a reading made in it; or (ii) a test or a generator those files
name reads it (the paper names `tests/test_amplitude_malus.py`,
`tests/test_amplitude_mz_345_n.py`, `tests/test_crossing.py`,
`tests/test_nature_beam_world_parsing.py`, `tools/amplitude_path.py`,
`tools/run_series.py`, `tools/check.py`, `examples/events/amplitude/make_worlds.py`
and, through NUMBERS.md, `tools/bell_choosers.py` and
`docs/designs/paper_families/family_table.py`); or (iii) it is the code the
reached worlds execute (the engine, the families, the keys and rules they
declare, the readings tools their numbers come from). Everything else is
not reached. Nothing here is a physics change: a deletion and a move leave
every kept world's record byte for byte as it was, and the local integer
operation contract and LOCALITY-1 are untouched.

## The counts

| What | Total | Kept | Deleted now | Deleted after the merge SHAs | Moved (step 3) |
| --- | --- | --- | --- | --- | --- |
| World files (`examples/events/**/*.json` that are worlds, the four root worlds included) | 306 | 243 | 21 (two_stars 3, masses 2, buildup 3; on the owner's strike of record 894: gallery 5, hand 4, catalog 4) | 41 (the 21 crowd worlds of the 22 that remain after gallery's `clock_6`, shell_clock's six ruled KEEP by the Boss, record 891; optical's 20 `body_*` worlds) | 0 |
| World directories | 34 (+ 4 root worlds) | 24 | 6 (two_stars, masses, buildup; gallery, hand, catalog on record 894) | 3 (crowd_clock, cluster_clock, reader_clock); optical partly | 0 |
| Design directories under `docs/designs/` | 43 | 33 | 5 (two_stars, masses, doppler_v1, push_relative_speed; hand on record 894) | 5 (crowd_clock, cluster_clock, reader_clock, optical_v1; one_wall in part) | 0 |
| Code modules in `src/event_universe/` (`.py`) | 25 | 24 | 1 (`ui.py`, with `ui_assets/`; the owner's word, record 894) | 0 | 0 |
| Tools in `tools/` (files) | 26 + the package `generic_vector_lab/` (9 files) | 3 as they are (`check.py`, `run_series.py`, `amplitude_path.py`, cited by the paper at its path) | 5 files + the package (`derivations_round7.py`, `derivations_round8.py`, `buildup_readings.py`, `gallery_pages.py` on record 894, `optical_readings.py`, `generic_vector_lab/`) | 0 | 21 into `tools/click_readings/` (18 first, then lensing, drive_b and shell_clock's reader), 2 more after the SHAs (`clock_word/read_runs.py` on generic-bending, the cart's `moving_detector_readings.py` on its branch) |
| Tests (`tests/test_*.py`) | 95 | 91 | 4 (`test_two_stars.py`, `test_buildup_readings.py`, `test_gallery_pages.py`, `test_entity_catalog.py`; `test_register_map.py` re-pointed, not deleted; `test_entity_loading_consumers.py` loses its UI cases; `test_hand.py` builds its worlds from `tests/support/hand_worlds.py`) | 0 (`test_optical_body.py` after optical's SHA) | the readings tests re-pointed to the package |

Of the 32 crowd worlds at n > 0 (record 865: clock_word 4, cluster_clock 2,
crowd_clock 8, gallery 1, hubble_stars 6, reader_clock 5, shell_clock 6):
series T's four (clock_word) are the paper's (the clock's field at two
distances, the ratio 1.907, NATURE row 12; the physicist's relevance check,
record 868) and stay; the 28 others are the physicist's list. Of those 28,
this table flags one thing the check of record 868 did not: **shell_clock's
six** (age_2, age_4, age_12, presence_2, presence_4, presence_12) are the
worlds of series X, Poisson after a detector, whose readings main.tex names
six times (k(2) / k(4) = 1.0029 for the pin 1.0039; k = 0.9089 at r = 4;
Section "The delay field" and the conversion table). By the rule of reach
they stay; the Boss decides whether they are the 28's or the paper's. The
remaining 22 (crowd_clock 8, cluster_clock 2, reader_clock 5, gallery's
clock_6, hubble_stars' gravity_* and double_* 6) the paper names nowhere in
main.tex; NUMBERS.md rows 130 to 134 name the crowd, cluster and reader
readings as "measured once, the entry drafted and not registered", numbers
main.tex no longer carries (record 868). They are deleted after the Boss
sends the merge SHA of `generic-bending`, whose refusal list names them.

## A. What the paper reaches (kept)

### A.1 Worlds, by the paper's series letter

| Directory | Series | Where the paper reaches it | Transitive code and readings |
| --- | --- | --- | --- |
| `amplitude/` (72 worlds) | L, L1 to L7, L2b, A12 (Malus) | main.tex throughout (Mach-Zehnder, the pair, GHZ, the gates, the cone, the two slits, Malus); NUMBERS.md; `figures.py` reads `amplitude/expectations.json`; `summarize_runs.py` reads its runs; `tests/test_amplitude_malus.py`, `tests/test_amplitude_mz_345_n.py` | `events/amplitude.py` (the layer, the one click), `tools/amplitude_path.py`, `tools/bell_choosers.py`, `examples/events/amplitude/make_worlds.py` (reads the root `two_slits.json`, `one_slit.json`) |
| `bell/` (17) | A2, A2 with the choosers | NUMBERS.md ("Paper 1's local candidates and the choosers' run: S = 2 exactly; the registry 2.83", the "before"); the gate set (`bell/a0_b0`, `bell/fixed`) | `tools/bell_chsh.py`, `tools/bell_choosers.py`, `tests/test_nature_beam_worlds.py`, `tests/test_bell_choosers.py` |
| `c_measured/` (1) | Q | main.tex (290 of 290 face clicks; Table 1's c row; the reproduction appendix) | `tools/c_measured_readings.py`, `tests/test_c_measured.py` |
| `clock_word/` (4) | T | main.tex (the clock's field at two distances, 1.907; NATURE row 12; the status word of record 868) | `clock_word/read_runs.py`, `tests/test_clock_word.py`, `tests/test_clock_age.py`; the key `reads: age` (clock-age-v1) |
| `covariant/` (4) | S | main.tex ten times (the muon's 64th self-creation, the face clicks 369 and 345, z = 0.3674) | the key `covariant_readings` (`covariant-readings-v1`, HYPOTHESES 25), `tools/covariant_readings.py`, `tests/test_covariant_readings.py` |
| `massive_rows/` (3) | W | main.tex (the massive rows, series W's first-click ages 815 and 876) | the key `massive_rows` (HYPOTHESES 26), `massive_rows/read_run.py`, `massive_rows/replay_register.py`, `tests/test_massive_rows.py` |
| `weak/` (11) | J1, J2 | main.tex (the neutron's decay clicks, the neutrino's window 16 of 1024; rows 8a, 8b); the gate set (`j3_deuteron`, `j2_ladder`, `j3_deuteron_crowd`) | the rule `become` (weak-v1), the hand on the family (`entities/families.json`), `tools/weak_readings.py`, `tests/test_weak_readings.py`, `tests/test_host_batches.py` |
| `binding/` (3) | N | main.tex (the deuteron's held bond, the alpha's 2.0; rows 7a, 7b) | binding-v1 (the give at the contact), `tests/test_binding.py` |
| `lensing/` (9) | K, K under the meeting | main.tex (0.000 pixel, 0.00 interval; row 13); NUMBERS.md (the meeting: `mass`, `heavy`, `near`); the gate set (`heavy_meeting`) | `events/meeting.py` (the key `meeting`, HYPOTHESES 20), `tools/lensing_readings.py`, `tests/test_lensing_readings.py`, `tests/test_meeting.py` |
| `hubble_stars/` (18, `record/` included) | G2 | main.tex (z = 0.2636 on `coasting_none`, row 4b; q_0 = -0.108); NATURE row 3 cites `record/coasting_none.json`; REPLICATIONS round 1 | the step drive, the suspension pair, `tools/hubble_stars_readings.py`, `tests/test_hubble_stars_readings.py`, `tests/test_step_drive.py`; its six crowd worlds are the 28's (below) |
| `hubble/` (4) | G | main.tex ("the hubble worlds' q_0 = -0.108 (row 3)"; series G's accelerating shape); the gate set (`pushing_age`) | `tools/hubble_readings.py`, `tests/test_hubble_readings.py` |
| `shell_clock/` (9) | X (Poisson after a detector) | main.tex six times (k(2) / k(4) = 1.0029, k = 0.9089 at r = 4) | `shell_clock/read_runs.py`, `tests/test_shell_clock.py`; flagged above: six of its worlds are in the count of 28 |
| `orbit_lamp/` (5) | D3 | main.tex (138 of 139 births, T(24) / T(12) = 1.997; the Newton row) | `tools/orbit_lamp_readings.py`, `tests/test_orbit_lamp_readings.py` |
| `orbit/` (8) | D | NUMBERS.md (Table 1's register list; "series D read 1.16 to 1.39"; `docs/designs/orbit_read/NOTE.md`) | `tools/orbit_readings.py`, `tests/test_orbit_readings.py`; `orbit_lamp/make_worlds.py` imports it |
| `coupling/` (21) | C | NUMBERS.md (Table 1's register list; the appendix's pin columns: the flux within 2 percent, the ring mean, the slopes); the gate set (`1b_m16`) | `tools/coupling_readings.py`, `diagnostics/shell_readings.py`, `tests/test_coupling_readings.py`, `tests/test_columns.py` |
| `redshift/` (2) | E | main.tex ("series E reads probes on the GameBoard, diagnostics this paper does not cite"); NUMBERS.md (Table 1's register list) | `tools/redshift_readings.py`, `tests/test_redshift_readings.py` |
| `bohr/` (7) | H | main.tex (Bohr's ratio, row 6, not run; "M = 1836 (atoms, bohr)"); NUMBERS.md (Table 1's register list); the gate set (`r2`) | the turn by momentum (`action`, `phase_by_momentum`, bohr-v1), `tools/bohr_readings.py`, `tests/test_bohr_readings.py` |
| `heisenberg/` (8) | A10 | main.tex Section 22 (the uncertainty relation: the far field 0.886, the exact sum at w27 0.916, the pin 0.92 at w = 27); NATURE row 10 cites `heisenberg/w27_wave.json`; the gate set (`w27_beam`, `w1_beam`) | `tools/heisenberg_readings.py`, `tests/test_heisenberg_readings.py` |
| `quarks/` (7) | R | main.tex Appendix D ("no detector reading registered (the quarks worlds)"); NUMBERS.md ("Series R (the masses row's check)") | `tools/quarks_readings.py`, `quarks/replay_register.py`, `tests/test_quarks_expectations.py` |
| `nucleus/` (8) | I | main.tex Appendix D ("7000 on one nucleus world"); the gate set (`alpha_square`) | `tools/nucleus_readings.py`, `tests/test_nucleus_readings.py`, `tests/test_step_drive.py` |
| `atoms/` (2) | the atoms series (no register entry, NATURE row 6 NOT YET) | main.tex Appendix D ("M = 1836 (atoms, bohr)"; "rho = 4 on the atoms and binding worlds"): named as the declaration the family table reads, no reading | `atoms/make_worlds.py` imports bohr's; `docs/designs/atoms/PINS.md`. Thin reach: named only as a declaration; the owner may strike it, and then Appendix D's two cells are the writer's |
| `gallery/` (5) | the visual gallery's worlds | main.tex Appendix D ("M = 1 (gallery)"): named as a declaration only | STRUCK by the owner (record 894, "delete old code"): deleted in the fourth commit with `tools/gallery_pages.py`, `docs/pages/gallery/` and `tests/test_gallery_pages.py`; `clock_6` (one of the 28) went with it |
| `hand/` (4) | P | main.tex Appendix D names the rule `hand-v1` (its reading series J2's); the worlds were the rule's own | STRUCK by the owner (record 894): deleted in the fourth commit with `docs/designs/hand/` and the gate set's row `wu`; the rule stays in the law, and `tests/test_hand.py` builds its four worlds from `tests/support/hand_worlds.py` (the generator moved, not a world file by hand) |
| `catalog/` (4) | the entity catalog's placements | main.tex Appendix D cites "the catalog, records 30 and 113", the document, not the worlds | STRUCK by the owner (record 894): deleted in the fourth commit with `tests/test_entity_catalog.py` and the gate set's two rows; `docs/ENTITY_CATALOG.md` stays as the catalog's document |
| `detector/` (4 + `entities/detectors.json`) | the apparatus definitions | the gate set (`grouped_12_nodes`: entity definitions, in_transit, a detector set with a threshold); the fixture of some thirty rule tests | `world_loading.py`, `tests/test_entity_catalog.py`, the rule tests |
| `entities/` (`families.json`, `apparatus.json`) | the one canonical definition per family | NUMBERS.md (the families: `families.json` audited by `docs/designs/paper_families/family_table.py`); every world's `entity_definitions` | `world_loading.py`, `entities/make_definitions.py` |
| `drive_b/` (6) | X (the directional drive, `drive-b-v1`) | not named by the paper (main.tex still says "form B, not built"); kept on the owner's approval of form B (record 652, 2026-09-22) and the Kepler row the paper's NUMBERS names as its future reading; the gate set (`plane_b`) | the key `drive_b` (HYPOTHESES 28, off by default), `tools/drive_b_readings.py`, `tests/test_drive_b.py`. Its composition with the one wall (`optical/body_*`, `tests/test_optical_body.py`, `one_wall/BODY_DRIVE.md`) is the superseded part, below |
| the root `one_content.json`, `two_contents.json`, `two_slits.json`, `one_slit.json`, `expectations.json`, `gate_set.json` | the four world files of the one engine; the gate set | `amplitude/make_worlds.py` reads `two_slits.json` and `one_slit.json` (NUMBERS.md: "`slits_one` is read by the generator"); the others are the loader's and `run_series.py`'s fixtures in eleven tests | `tests/test_nature_beam_worlds.py`, `tests/test_run_series.py`, `tools/run_series.py --list` |

### A.2 Designs the paper cites (kept), and the designs of kept worlds or rules (kept)

Cited by main.tex or NUMBERS.md: `algebra_transition`, `amplitude-v1`,
`click_frame`, `clock_age`, `einstein_outside`, `far_lamp`, `fraction_free`,
`gr_rows`, `light_outside`, `light_speed`, `malus`, `new_formulas`,
`notation`, `open_problems/born`, `orbit_read`, `paper_families`,
`vector_form`; `derivations_beam` holds the host scripts of
DERIVATIONS_BEAM.md (`amended_pins.py`, `kepler_compton.py`,
`mover_counter.py` and the rest) that NUMBERS.md names in a dozen rows;
`clock_loop` is cited by `click_frame`; `label_rotation` by `malus`;
`moving_detector` is the cart's design (the click code, section C).

Designs of kept worlds or of rules in force, not cited but not deleted
(a document, not a world or an experiment): `atoms` (the atoms worlds),
`binding_v1` (series N), `covariant_readings` (series S), `crossing` (the
crossing rule, BEAM_LAW note 48, which NUMBERS.md names), `drive_b`
(drive-b-v1), `hand` (hand-v1), `hubble_stars` (series G2's rule reviews),
`massive_rows` (series W), `quarks` (series R), `architecture`,
`architecture_2026-09-20`, `clock_audit`, `highlights_prune` (reports on the
owner's orders), `open_problems/*` (the seven problems' notes; born cited).

### A.3 Code paths the paper's worlds execute (kept)

`src/event_universe/`: `events/world.py` (the world file), `events/nature_beam.py`
(the Beam Law and the click), `events/engine.py`, `events/measured.py`,
`events/amplitude.py`, `events/meeting.py` (K under the meeting),
`events/run.py`, `core/integer.py`, `core/game_board.py`, `core/phase.py`
(read by the paper's checks: `event_universe.core.phase`), `runner.py`,
`world_loading.py`, `json_documents.py`, `configuration_validation.py`
(the preflight of ENGINE.md), `snapshot_writer.py`, `retention.py` (the
runner's and `check.py`'s output ownership), `register_map.py`,
`diagnostics/numeric_audit.py` (the integer gate), `diagnostics/shell_readings.py`
(series C). Tools: `check.py`, `run_series.py`, the readings tools of A.1.

## B. Everything else: the table

Columns: the path; what it is; why the paper does not reach it (not cited /
superseded / a hypothesis off by default the paper never reads); the
proposed action with its one reason; the tests that touch it.

### B.1 Worlds and experiments

| Path | What it is | Why not reached | Action | Tests |
| --- | --- | --- | --- | --- |
| `examples/events/two_stars/` (3 worlds, `expectations.json`, `make_worlds.py`, README) | Series O, two stars moving toward each other (2026-09-21) | not cited: named nowhere in the paper's files | DELETE now: not in the paper | `tests/test_two_stars.py` (deleted); `tests/test_register_map.py` part (e) re-pointed to `clock_word/make_worlds.py` |
| `examples/events/masses/` (2 cavity worlds, README) | the cavity of the masses design (series M, 2026-09-20), written by hand | not cited: the paper's masses row rests on DERIVATIONS_BEAM 19.2 and 19.4, not on this design | DELETE now: not in the paper | none |
| `examples/events/buildup/` (3 worlds, `make_worlds.py`, README) | A10 at a low rate, the single-click build-up before the one click (2026-09-20) | superseded: the one click of amplitude-v1 is the build-up now; RECORD.md names the old result only as a limit set aside | DELETE now: superseded and not in the paper | `tests/test_buildup_readings.py` (deleted; it reads `tools/buildup_readings.py`) |
| `examples/events/crowd_clock/` (8 worlds) | series U, a lamp inside a crowd | not cited in main.tex (record 868); NUMBERS.md row 130 names the design's reading, a number main.tex no longer carries | DELETE after the merge SHA of `generic-bending` (its refusal list names them) | `tests/test_crowd_clock.py` (deleted then); `tools/gallery_pages.py` reads `crowd_clock` for the clock page (re-pointed then) |
| `examples/events/cluster_clock/` (2 worlds) | series V, a cluster of crowds | not cited in main.tex; NUMBERS.md row 133 | DELETE after the SHA of `generic-bending` | `tests/test_cluster_clock.py` (deleted then) |
| `examples/events/reader_clock/` (5 worlds) | series S (the letter reused), a reader inside a crowd | not cited in main.tex; NUMBERS.md row 134 | DELETE after the SHA of `generic-bending` | `tests/test_reader_clock.py` (deleted then) |
| `examples/events/gallery/clock_6.json` | series U's `still_3` as a gallery world | one of the 28 | DELETE after the SHA of `generic-bending`; the gallery's clock page then draws no crowd world | `tests/test_gallery_pages.py` |
| `examples/events/hubble_stars/{gravity,double}_{age,none,scalar}.json` and `record/` copies | G2's six crowd worlds (gravity on, doubled mass) | the 28's; the paper's G2 rows rest on `coasting_none` (gravity off) and on record 408's re-read, which the register keeps as history | DELETE after the SHA of `generic-bending`; the register blocks kept as history in `expectations.json` (record 865) | `tests/test_hubble_stars_readings.py` |
| `examples/events/shell_clock/{age,presence}_{2,4,12}.json` | series X's six shell worlds | counted among the 28 by record 868, but main.tex names their readings six times (series X) | KEEP by the rule of reach; the Boss decides (flagged at the top) | `tests/test_shell_clock.py` |
| `examples/events/optical/body_*.json` (20 worlds), `body_expectations.json` | the one-wall course's step 3: the body's drive under the wall (optical-body-drive, records 745 to 780) | superseded (record 816: "there is no wall any more"; marked, not deleted, then; the owner's "old code goes" now) | DELETE after the SHA of `generic-bending` (the branch asserts its 28 unchanged worlds byte identical; which they are is the physicist's list) | `tests/test_optical_body.py` (deleted then); `tools/drive_b_readings.py` loses its optical part |
| `examples/events/optical/` the 13 pin worlds under the key `optical` (`mass`, `near`, `far`, `fast`, `control`, `matter`, `matter2` at gamma 0 and 1), `expectations.json` | optical-v1's pin worlds, light beside a mass under the key | the paper names the key's form as NOT COMPARED (design gr_rows); the key is being removed by `generic-bending` (the coupling inserted into the law at c_f = 1 + gamma, the 20 moving worlds re-pinned) | the physicist's, in flight: no action here; after his SHA the worlds either carry the generic declaration or go with the key | `tests/test_optical.py` (the physicist's) |

### B.2 Designs

| Path | What it is | Why not reached | Action | Tests |
| --- | --- | --- | --- | --- |
| `docs/designs/two_stars/DESIGN.md` | the design of series O | not cited | DELETE now, with its world; the links in `docs/designs/moving_detector/DESIGN.md` and `docs/README.md` become plain text | none |
| `docs/designs/masses/` (DESIGN.md, `ladder.py`, `cavity_read.py`, `cavity_click_read.py`, their outputs, `worlds/cavity_*_click.json`) | the masses design (series M) and its scratch maps | not cited (the paper's masses row rests on DERIVATIONS_BEAM 19) | DELETE now, with its worlds; the links in `docs/FULL_PICTURE.md`, `docs/PREDICTIONS.md`, `docs/README.md`, `docs/designs/open_problems/masses/NOTE.md` become plain text | none |
| `docs/designs/doppler_v1/` (REVIEW_1.md, REVIEW_2.md) | the reviews of doppler-v1, the reading's weight at the relative speed | the key `doppler` was deleted on 2026-09-20 (the crossing rule gives the Doppler, BEAM_LAW note 48); these review deleted code | DELETE now: the record of deleted code, its verdict already in the log | none |
| `docs/designs/push_relative_speed/` (FORM.md, GRAIN.md, two maps) | change 2 (the push at the relative speed, not admissible) and doppler-v1's grain form | the same deleted key; the verdict of change 2 is in Highlights 5.4 | DELETE now | none |
| `docs/designs/crowd_clock/DESIGN.md`, `cluster_clock/DESIGN.md`, `reader_clock/DESIGN.md` | the designs of series U, V and the reader | their worlds are the 28's; NUMBERS.md rows 130 to 134 cite them for numbers main.tex no longer carries | DELETE after the SHA of `generic-bending`, with their worlds, unless the writer keeps rows 130 to 134 (then they stay as the rows' source); the links in `docs/designs/clock_age/NOTE.md` (cited by the paper) and `docs/designs/moving_detector/DESIGN.md` become plain text | none |
| `docs/designs/one_wall/BODY_DRIVE.md`, `PHYSICIST.md`, `MATHEMATICIAN.md`, `one_wall_check.py`, `one_wall_map.py` and outputs | the one-wall course (one-wall-v1 withdrawn; the body's drive under the wall, step 3) | superseded (record 816) | DELETE after the SHA of `generic-bending`; `NOTE.md` (optical-v1's generic form) and `EVERY_FAMILY.md` (the physicist's step 2 of the generic bending) with `every_family_map.py` are the physicist's and stay or go on his word | none |
| `docs/designs/optical_v1/` (REVIEW_3.md, REVIEW_408CF719.md) | the reviews of optical-v1's generic form | the key is being removed by `generic-bending` | DELETE after its SHA, with the key, unless the physicist keeps them as the coupling's review record | none |

### B.3 Register maps, readings and tools

| Path | What it is | Why not reached | Action | Tests |
| --- | --- | --- | --- | --- |
| `tools/derivations_round7.py`, `tools/derivations_round8.py` (1,121 lines) | scratch computations for DERIVATIONS.md rounds 7 and 8 (the law of the shadow, 2026-09-18) | not cited: the paper cites DERIVATIONS_BEAM.md, never DERIVATIONS.md | DELETE now: old code; DERIVATIONS.md's and MIGRATION.md's mentions become plain text | none |
| `tools/buildup_readings.py` | the readings of the build-up worlds | with `buildup/` | DELETE now | `tests/test_buildup_readings.py` |
| `tools/generic_vector_lab/` (9 files, about 4,490 lines) | the opt-in vector lab, an externally supplied prototype beside the engine (README, ARCHITECTURE.md) | not reached by any world, test of the law or paper file; not the click code | DELETE now: old code beside the engine; `README.md`, `docs/ARCHITECTURE.md` and `docs/MIGRATION.md` updated. The owner asked for this lab once (ARCHITECTURE.md, "user-requested"); his "old code goes" covers it, and the deletion is one commit to revert if he wants it back | `tools/generic_vector_lab/test_lab.py`, `test_node_rules.py` (inside the package) |
| `tools/optical_readings.py` | a GAMEBOARD diagnostic of optical-v1's pin worlds (record 483), never a detector reading | the key is in flight | DELETE after the SHA of `generic-bending` | none |
| `src/event_universe/ui.py`, `src/event_universe/ui_assets/` (3 files), `docs/WORKSPACE.md`, the script `event-universe-ui` | the local configuration workspace of the law of events (a browser UI over the parser and runner) | not reached: a host convenience of 2026-09-1x; no test of the law, no world, no paper file uses it | DELETE now: old code; `pyproject.toml`, `MANIFEST.in`, `README.md`, `docs/README.md`, `docs/ARCHITECTURE.md`, `docs/MIGRATION.md` updated | `tests/test_entity_loading_consumers.py` (its UI cases removed) |
| `examples/events/*/expectations.json` register blocks of deleted worlds | the register rows | with their worlds | deleted with the worlds now (two_stars); kept as history for the 28 (record 865) | `tests/test_register_map.py` |
| `docs/EXPERIMENTS.md` entries and `docs/TEST_EXPECTATIONS.md` sections of deleted worlds; `docs/README.md` and `examples/events/README.md` index rows | the register's prose | with their worlds | the entry's one line moves to EXPERIMENTS.md section D ("What is deleted") with the commit; the sections and rows go; VALIDATION.md's dated lines stay as history with their links made plain | `tests/test_repository_navigation.py` |

### B.4 Keys, hypotheses and rules the paper never reads

| Key or rule | Where | Read by a paper world? | Action |
| --- | --- | --- | --- |
| `drive_b` (drive-b-v1, HYPOTHESES 28) | `world.py`, `nature_beam.py` | no (the paper: "form B, not built") | KEEP on the owner's approval of form B (record 652); the flag stays off by default. Its one-wall composition goes with `optical/body_*` |
| `optical` (optical-v1, the age wall's set) | `world.py`, `nature_beam.py`, `measured.py` | named as NOT COMPARED only | the physicist's: `generic-bending` removes the key and inserts the coupling; no action here |
| `clock_stamp` | the cart's build (moving-detector-build) | the click code (new) | no action until its merge; then ordered under section C |
| `covariant_readings` (HYPOTHESES 25), `massive_rows` (26), `meeting` (20), `action` and `phase_by_momentum` (bohr-v1), `become` (weak-v1), the hand, binding-v1, `reads: age` (clock-age-v1) | the engine | yes (series S, W, K under the meeting, H, J, N, T) | KEEP: reached |
| `OLD_KEYS` (23 refused keys), the refusals of `law: events` and the old law value | `world.py` | the loader's refusals, not physics | KEEP: they name what was deleted and refuse it |

## C. The click code: the new, the old it supersedes, and the order

### C.1 The new click code

| Path | Responsibility | State |
| --- | --- | --- |
| `docs/designs/click_frame/DERIVATION.md` | Lorentz from the clicks: Bondi's two factors on the GameBoard, the missing direction k_AB | on main (PR #769 at 70e9781a); cited by the paper |
| `docs/designs/moving_detector/DESIGN.md` | the cart with a click: a body carrying a detector, its clicks on its own record, the pins before any run, the code path (section 7) | on main (PR #807 at 4fc273ee) |
| the cart's build, branch `moving-detector-build` at `5aa64b3edae793ab4de0c59555a79835faab4199` | the world key `clock_stamp` (`world.py`: the parse and the field; `nature_beam.py`: the `clock` field on every line a measured event writes, in `_apply_plan` and `_release`; `engine.py`: the face click's line; `run.py`: the record key); `examples/events/moving_detector/` (`cart_k3`, `cart_k5`, `cart_k9`, `cart_k17`, `cart_quantum`, `capability_k5`, `expectations.json`, `make_worlds.py`, README); `tools/moving_detector_readings.py` (422 lines: k_AB, the least step, the round trip, the radar velocity, k_BA from the post's record; `--capability`); `tests/test_moving_detector.py`; the three families in `entities/families.json` | in flight: not touched here |
| the readings of a click from a run's record | `tools/amplitude_path.py`, `bell_chsh.py`, `bell_choosers.py`, `bohr_readings.py`, `c_measured_readings.py`, `coupling_readings.py`, `covariant_readings.py`, `drive_b_readings.py`, `heisenberg_readings.py`, `hubble_readings.py`, `hubble_stars_readings.py`, `lensing_readings.py`, `nucleus_readings.py`, `orbit_lamp_readings.py`, `orbit_readings.py`, `quarks_readings.py`, `redshift_readings.py`, `weak_readings.py`; `examples/events/clock_word/read_runs.py`, `shell_clock/read_runs.py`, `massive_rows/read_run.py`, `massive_rows/replay_register.py`, `quarks/replay_register.py` | on main, one file per series, each with its own `find_runs` (14 copies) and `read_run` (15 copies) of the record's access |
| the engine's click | `events/nature_beam.py` (`_apply_plan`: the click, read and rerelease lines; the face click in `engine.py`), `events/amplitude.py` (the layer: the one click, the rungs), `events/measured.py` (the record) | on main; the law |

### C.2 The old code the new supersedes or that nothing in the paper reaches

| Old code | Consumers today | Superseded by or unreached | Action |
| --- | --- | --- | --- |
| the one-wall course: `optical/body_*` (20 worlds), `body_expectations.json`, `tests/test_optical_body.py`, the optical part of `tools/drive_b_readings.py`, `one_wall/BODY_DRIVE.md`, `PHYSICIST.md`, `MATHEMATICIAN.md`, `one_wall_check.py`, `one_wall_map.py` | `examples/events/optical/README.md`, `EXPERIMENTS.md` ("X, the directional drive" and the optical entry), `NATURE.md` row 13's note | the cart with a click (record 816: no wall) | DELETE after the SHA of `generic-bending` |
| `tools/optical_readings.py` (a GAMEBOARD diagnostic) | `optical/README.md`, `make_worlds.py` | the key is leaving | DELETE after the SHA |
| `tools/buildup_readings.py`, `examples/events/buildup/` | `tests/test_buildup_readings.py`, VALIDATION.md | the one click | DELETE now |
| `tools/derivations_round7.py`, `derivations_round8.py` | DERIVATIONS.md (history) | DERIVATIONS_BEAM.md | DELETE now |
| `src/event_universe/ui.py`, `ui_assets/`, `docs/WORKSPACE.md` | `tests/test_entity_loading_consumers.py`, `pyproject.toml` | nothing: the runner and `run_series.py` are the only paths a world takes | DELETE now |
| `tools/generic_vector_lab/` | README.md, ARCHITECTURE.md | nothing in the law | DELETE now |
| `docs/designs/doppler_v1/`, `push_relative_speed/` | docs/README.md | the crossing rule | DELETE now |
| `examples/events/two_stars/`, `masses/` and their designs | the tests named above | not in the paper | DELETE now |
| the 28 crowd worlds (22 of them here, shell_clock's six flagged) and the designs of series U, V and the reader | `tests/test_crowd_clock.py`, `test_cluster_clock.py`, `test_reader_clock.py`, `tools/gallery_pages.py` | the generic entry of the bending (records 847, 865, 868) | DELETE after the SHA of `generic-bending` |

### C.3 The order (step 3): one boundary for the readings of a click

What moves where, one line each:

1. A package `tools/click_readings/` is created: the readings of the register's series from a run's record, the clicks alone labelled DETECTOR and the GameBoard's lines labelled GAMEBOARD; its `README.md` names the boundary (nothing here runs a rule; nothing here reads a Node; every number printed carries its kind).
2. No shared `record.py`: read at the move, the tools' `find_runs` and `read_run` bodies all differ but for four trivial pairs (nucleus and weak's `find_runs`, hubble_stars and weak's `load_expectations`, bell and bell_choosers' `load`, hubble and hubble_stars' `fmt`), so a shared module would hold nothing worth a second boundary; each tool keeps its own helpers and arithmetic where they are, byte for byte.
3. Each readings tool moves under the package with the name of its series' subject and without the suffix `_readings`, its docstring, usage line and arithmetic unchanged (`tools/amplitude_path.py` stays where it is: the paper's RECORD.md cites it at that path, as it cites `tools/run_series.py` and `tools/check.py`): `bell_chsh.py` -> `bell.py`; `bell_choosers.py` -> `bell_choosers.py`; `bohr_readings.py` -> `bohr.py`; `c_measured_readings.py` -> `c_measured.py`; `coupling_readings.py` -> `coupling.py`; `covariant_readings.py` -> `covariant.py`; `heisenberg_readings.py` -> `heisenberg.py`; `hubble_readings.py` -> `hubble.py`; `hubble_stars_readings.py` -> `hubble_stars.py`; `nucleus_readings.py` -> `nucleus.py`; `orbit_lamp_readings.py` -> `orbit_lamp.py`; `orbit_readings.py` -> `orbit.py`; `quarks_readings.py` -> `quarks.py` (with `quarks/replay_register.py` -> `quarks_replay.py`); `redshift_readings.py` -> `redshift.py`; `weak_readings.py` -> `weak.py`; `massive_rows/read_run.py` and `replay_register.py` -> `massive_rows.py` and `massive_rows_replay.py`.
4. After the SHAs of `generic-bending` and `moving-detector-build`: `lensing_readings.py` -> `lensing.py`; `drive_b_readings.py` -> `drive_b.py` (its optical part gone); `clock_word/read_runs.py` -> `clock_word.py`; `shell_clock/read_runs.py` -> `shell_clock.py`; `tools/moving_detector_readings.py` -> `moving_detector.py`. The cart's readings then sit beside every other click reading under the one boundary, and the moving detector's world key, lines and record stay in the engine where the build put them (the engine writes the click; the package reads it).
5. Consumers updated in the same commit: the tests that load a tool by path, `tools/check.py`'s dependency map, the usage lines in `examples/events/*/README.md`, `docs/EXPERIMENTS.md`, `docs/TEST_EXPECTATIONS.md`, `README.md`'s project map, `docs/ARCHITECTURE.md`; the paper's PLAN.md is not touched (it is the writer's).
6. What is deleted in this step: nothing but the duplicated `find_runs` and `read_run` bodies, replaced by the one in `record.py` where the bodies are identical; a body that differs stays in its tool.
7. The proof: `python tools/check.py --base origin/main` green at every commit and `--full` once at the end; every `expectations.json` of a kept world byte identical to the base (`git diff --stat 59c6b811 -- 'examples/events/**/expectations.json'` empty for the kept worlds); the paper's pinning tests (`tests/test_amplitude_malus.py`, `tests/test_amplitude_mz_345_n.py`) green; the gate set replayed with its digests (`tests/test_amplitude_click.py` part (d)).

## D. Conflicts with the branches in flight (deleted only after the Boss sends the merge SHAs)

| Branch | Its files | What waits on it |
| --- | --- | --- |
| `generic-bending` (the physicist's step 5: the generic bending law and the 46-world digest; not yet on the remote at this reading) | `world.py`, `nature_beam.py`, the optical, lensing and clock worlds' registers and tests, EVERY_FAMILY.md | the 22 crowd worlds and their three designs; `optical/body_*` and the one-wall files; `optical_readings.py`; `optical_v1/`; the key `optical`; the moves of `lensing_readings.py`, `drive_b_readings.py`, `clock_word/read_runs.py`, `shell_clock/read_runs.py` |
| `moving-detector-build` at `8f5b42fbbcf6240d096052832db21c4e330d2ec2` (the cart's steps 3 and 4; PR #834, HELD indefinitely by the owner's scope word, record 920; the Boss, record 932: do not wait on it) | `engine.py`, `nature_beam.py`, `run.py`, `world.py`, `ENGINE.md`, `ENTITY_CATALOG.md`, `TEST_EXPECTATIONS.md`, `entities/families.json`, `make_definitions.py`, the moving_detector worlds, tool and test | only the move of `tools/moving_detector_readings.py` under the package is deferred on the cart (a file of that branch); every other deferred item depends on `generic-bending` alone |
| `claude/paper-owner-review-five` at `0406382f3700469b5459b9494ce8396e568f8b20` (the paper) | `paper/general_formula/*` | nothing here touches `paper/` |
| `light-bending-algebra` (PR #821) at `a7615254bb8fd5de4806980c5e7739f12a880b95`; `atom-algebra` (PR #823) at `c7ae2269b0a4e2763979519f7f25f063951f1e44` | `docs/README.md` (one index row each), their design directories | `docs/README.md` is edited here (index rows removed); the merge of either branch adds a row, no overlap in lines |

## D2. Step 4: the six verbs named in the code (the owner's word, records 920 and 940; after PR #855 and PR #854 merge)

The owner's word (2026-09-22, record 940, to this session): every algebraic
operation at a Node by the rules of modern algebra, the clicks too, clear
and simple in the code; the Boss's order (about 12:50Z): the plan written
here now, the work after the merge SHAs of `generic-bending` (PR #855) and
the flow-link ring (PR #854), about a day, no run, every registered digest
the proof. The audit it rests on is [NODE_ALGEBRA.md](NODE_ALGEBRA.md).

**The rule of the step.** No arithmetic changes: every integer the engine
computes is computed by the same operations in the same order, so every
registered digest (the gate set's `digests`, every `expectations.json`, the
paper's pinning tests) is byte for byte the proof; the local integer
operation contract and LOCALITY-1 untouched; no rule's identity renamed; a
verb gets a name, a place and a docstring, nothing else.

**D2.1 The six verbs as named primitives** (`core/integer.py`, the one place;
their bulk numpy forms beside them in `events/verbs.py`, the same names,
the same docstrings, one file):

| Verb | The primitive today | Its name after | The bulk form today |
| --- | --- | --- | --- |
| (T) the translation of an accumulator by its rate | the `s + r` inside `by_drive` and `by_clock` | `translate(state, rate)` | `by_drive_rows`, `by_clock_rows` (`nature_beam.py:569-620`), the phase and age lines of `_walk` |
| (D) the Euclidean division with the remainder kept, and the comparison | `by_drive`, `by_clock`, `apportion_whole`, the rungs `cell_of` | `divide(state, wall, at_most)` (the carry is the event), `compare(...)` for the ladders | the same bulk rows; `rungs`, `cell_of`, `node_choice` in `amplitude.py` |
| (B) the bilinear form with a declared matrix | `signed_inner`, the moments' sums, `push_form` (`nature_beam.py:2932`), `Layer.gram_form` | `bilinear(matrix, vector)` | `read_arrivals`, `Moments`, `CrowdMoments`, `born_recoil` |
| (G) the group-ring addition in Z[Z_N] | the merge's sum with the cancel (`_merge_rows`, `nature_beam.py:1377-1560`) | `ring_add(rows)` | the same |
| (P) the permutation | the collision table's application (`_collide`), the gate (`apply_gate`), the arc permutation of the meeting, the apportioning's tie | `permute(table, state)` | the same |
| (E) the evaluation of the tables at zeta_N and the norm | `circle_vectors`, `coherent_pointer`, `Layer.evaluate`, the face click's reading | `evaluate(phase)` and `norm(...)` (the one quadratic step) | `pointer_phases`, `Layer.cells` |

**D2.2 Each step of the interval names its verbs.** The six step functions of
`nature_beam()` (`_walk`, `_collide`, `_measure`, `_release`, `_border`,
`_merge`) and the frame (`engine.py: _frame_all`, `_move`, `step`) get a
first docstring line of the form "(T) then (D): ..." and call the named
forms; the comment that names a verb today becomes the call.

**D2.3 The click's plan split by verb.** `_family_plan` (587 lines) and
`_apply_plan` (458 lines) become one function per verb, the bulk numpy kept
and the order of the record lines kept: the window and the threshold (D,
one function each), the parity filter on the hand (D), the push (B, through
`push_form`), the share (D, `share_of`), the gate (P), the record lines apart
from the arithmetic; `FamilyPlan` stays the plan's record. The ledger in
`amplitude.py` is already by verb (`evaluate`, `gram_form`, `cells`, `rungs`,
`cell_of`) and only gains the names.

**D2.4 The predicate written as one.** `amplitude.common_denominator`'s
perfect-square test becomes `is_square(n)` in `core/integer.py` (the root
squared back and compared, as today), so no root stands in the click's
path by name; `world._same_class` the same.

**D2.5 The load-time roundings listed once, and the gate rule.** LAW.md
section 6's list completed (`E'_D` of the flight triple, `E'` at load under
`covariant_readings`, `T_HEADING`); the algebra gate's list of roots
(`tests/test_integer_algebra.py`, ALLOWED_ROOTS) reduced to those functions
plus the modules that carry a seventh-verb identity (`meeting.py` under its
key; lorentz-v1 if built), so that a root anywhere else in `events/` fails.

**D2.6 The pushed row's wall under the generic bending.** Not this step's:
the physicist chooses in his fold of PR #855 between the table read (the
flight table's `T_D` on the primitive direction nearest **P**) and the
comparison ladder (`(R^2 + 3 |P|^2) Q^2` against `T^2` for the candidate T),
the owner's word of record 920 (no root in a rule) and the Boss's routing
(record 940); D2.5's gate rule is turned on after his fold lands, since the
branch as it stands would fail it.

**The order and the proof.** D2.1 and D2.4 first (the primitives and the
predicate, `core/integer.py` and `events/verbs.py`, every consumer
re-pointed; `check.py --base origin/main`, the gate set's digests), then
D2.2 (docstrings and calls), then D2.3 (the click's plan, the largest
diff, `tests/test_amplitude_click.py` part (d) and the paper's pinning
tests the proof), then D2.5. One commit each, the six lines after each.
The host estimate: about a day after the SHAs; no run; the danger: none
to the physics (no arithmetic moves), the risk a wrong re-pointing, which
the digests catch at the first check.

## E. What is deleted now, in order (step 2)

1. Worlds and experiments: `two_stars/` (with `tests/test_two_stars.py`, `docs/designs/two_stars/`, the TEST_EXPECTATIONS section, the index rows, `test_register_map.py` re-pointed); `masses/` (with `docs/designs/masses/`); `buildup/` (with `tools/buildup_readings.py`, `tests/test_buildup_readings.py`); the EXPERIMENTS.md entry of A10 at a low rate moved to section D in one line; VALIDATION.md's links made plain.
2. Old code nothing left reaches: `tools/derivations_round7.py`, `tools/derivations_round8.py`, `tools/generic_vector_lab/`, `src/event_universe/ui.py` with `ui_assets/` and `docs/WORKSPACE.md`, `docs/designs/doppler_v1/`, `docs/designs/push_relative_speed/`; TERMINOLOGY.md, HYPOTHESES.md, ENGINE.md, ARCHITECTURE.md, MIGRATION.md and the register maps updated in the same commit; nothing in Highlights or the logs.
3. The click code ordered as C.3 says, the moves of item 3 now, item 4 after the SHAs.

## Done

(One line per deletion commit, appended as the commits land: what was deleted, the commit's SHA, the check that was green.)

1. Step 2 (1): `examples/events/two_stars/`, `masses/`, `buildup/` with `docs/designs/two_stars/`, `docs/designs/masses/`, `tests/test_two_stars.py`, `tests/test_buildup_readings.py`, `tools/buildup_readings.py` and DERIVATIONS_BEAM 18.6's host script `series_o_identity.py`; the register entry of A10 at a low rate moved to EXPERIMENTS.md section D (its heading kept for the validation log's links), the TEST_EXPECTATIONS section and the index rows removed, `tests/test_register_map.py` part (e) re-pointed to `orbit_lamp/make_worlds.py`, the links of VALIDATION.md, PREDICTIONS.md, FULL_PICTURE.md, DERIVATIONS_BEAM.md, `moving_detector/DESIGN.md` and `crowd_clock/DESIGN.md` made plain, one MIGRATION.md entry. Commit: 215c6db02e7c5886b75735ad957ecc836e6bd6c3. Check: `python tools/check.py --base origin/main`: 35 test files selected, 694 passed, 1 xfailed (pre-existing), after the last link was made plain; the three gates green.
2. Step 2 (2): `tools/derivations_round7.py`, `tools/derivations_round8.py`, `tools/generic_vector_lab/` (9 files), `src/event_universe/ui.py` with `ui_assets/` (3 files), `docs/WORKSPACE.md`, the script `event-universe-ui` and the package data in `pyproject.toml` and `MANIFEST.in`, `docs/designs/doppler_v1/`, `docs/designs/push_relative_speed/`; the UI cases of `tests/test_entity_loading_consumers.py` removed; README.md's UI and vector-lab sections and project-map row, ARCHITECTURE.md's vector-lab section and workspace clauses, ENGINE.md's, PROJECT_STATUS.md's, RETENTION.md's and VALIDATION.md's workspace sentences, DERIVATIONS.md's two mentions, `tools/check.py`'s `ui_assets` prefix and four docs/README.md index rows updated; one MIGRATION.md paragraph. `skills/regression-check/SKILL.md` line 108 still names `ui_assets` (the Boss's document, reported, not edited). Commit: 3b262ec539c7c291625e8c0415a35af856b92a29. Check: `python tools/check.py --base origin/main`, the whole suite (pyproject.toml changed): 1455 passed, 1 skipped, 1 xfailed (pre-existing); ruff and mypy clean.
3. Step 3, item 3 of C.3: the package `tools/click_readings/` with its README; 18 modules moved with `git mv` (bell, bell_choosers, bohr, c_measured, coupling, covariant, heisenberg, hubble, hubble_stars, massive_rows, massive_rows_replay, nucleus, orbit, orbit_lamp, quarks, quarks_replay, redshift, weak), their root paths corrected (`parents[2]`; the per-world readers' `WORLDS`), nothing else in them changed; the tests' load paths, `tools/check.py`'s map, the worlds' READMEs, EXPERIMENTS.md, TEST_EXPECTATIONS.md, BEAM_LAW.md, ENGINE.md, README.md's project map and ARCHITECTURE.md's tools row updated; the JSON registers, the generators and the dated evidence untouched (every `expectations.json` byte identical to the base). Commit: 93aff8f2d257259d1cefd83c3c12c4965937971f. Check: `python tools/check.py --base origin/main`, the whole suite (tools/check.py changed): 1455 passed, 1 skipped, 1 xfailed (pre-existing).
4. Main merged into the branch at 9426899f (no conflict; docs/README.md's rows both kept). The owner's strike of record 894, read from main's records 891 and 894: `examples/events/gallery/` with `tools/gallery_pages.py`, `docs/pages/gallery/` and `tests/test_gallery_pages.py`; `examples/events/hand/` with `docs/designs/hand/` (the generator moved to `tests/support/hand_worlds.py`, `tests/test_hand.py` re-pointed; the rule hand-v1 untouched); `examples/events/catalog/` with `tests/test_entity_catalog.py` (ENTITY_CATALOG.md stays, its world links plain); the gate set's three rows removed (fourteen worlds, the coverage named in its description), `tests/test_amplitude_layer.py`'s list of the design's test 7 loses the two catalog rows (fifteen); the register entries of series P and the gallery one line each under EXPERIMENTS.md section D with their headings kept; TEST_EXPECTATIONS, the worlds index, docs/README.md (three rows), HYPOTHESES, FULL_PICTURE, BEAM_LAW, ENTITY_DEFINITIONS, VALIDATION and MIGRATION links made plain; one MIGRATION.md paragraph. The UI workspace's deletion of commit 2 stands under the same word. The four families only those worlds declared (`apparatus`, `neutron`, `nubar`, `screen`) stay defined in `entities/families.json` (the paper's family table audits the file and the cart's build touches it); `tests/test_entity_definitions.py` names them as the families of deleted worlds. Commit: 7034008b8157ab8064249e64a58b01ceeec6ab42. Check: `python tools/check.py --base origin/main`, the whole suite (tools/check.py changed): 1414 passed, 1 xfailed.
5. The owner's word to this session and the Boss's order on record 920: [NODE_ALGEBRA.md](NODE_ALGEBRA.md), the audit of every operation at a Node against the six verbs (commit 959589573539faac0a8e5374225812d38cb18539); then the algebra gate `tests/test_integer_algebra.py` (the token and syntax-tree test on the nine physical modules; every root listed by function with its reason, the list the inventory; `tools/check.py` selects it on any `src/` change) and the clicks' certificate (the table in `tools/click_readings/README.md`, one row per readings tool the paper reaches: what it reads, what it writes back, what its floats are, what it derives outside the engine). Commit: f15abe5e608e74dfe810b7c1330c69c0ccb4dbae. Check: `python tools/check.py --base origin/main`, the whole suite (tools/check.py changed): 1437 passed, 1 xfailed.
6. The moves no branch in flight touches (the Boss, record 932): `tools/lensing_readings.py` -> `tools/click_readings/lensing.py`, `tools/drive_b_readings.py` -> `drive_b.py`, `examples/events/shell_clock/read_runs.py` -> `shell_clock.py` (its `WORLDS`), their tests and mentions re-pointed; `tools/optical_readings.py` deleted (its mentions in optical's README and the register made plain; the strings of `optical/make_worlds.py` that the register carries untouched); `skills/workflow.md`'s Visualiser line corrected on the Boss's order. Left deferred: `clock_word/read_runs.py` (generic-bending's test) and the cart's tool. Commit: dcacdbe0bd865938ccc36e7756ba4a1415997fba. Check: `python tools/check.py --base origin/main`: 1437 passed, 1 xfailed.
7. Section D2 (step 4's plan) at 70681736dae17191240dc486c9296416d9dd945a (docs only; the same check). Then the reviewer's three lines on PR #860 folded: the gate's four holes closed with self-tests (aliases of `math`, `isqrt` and `integer_root` refused and resolved; allocations without a dtype and `np.array` of a non-integer literal; the builtin `float`, the methods `.mean`, `.std`, `.var`, `.astype` on an unlisted name; the chains `np.linalg.*`, `np.linspace`, `np.random.*`, `np.fft.*`), the certificate's rows for orbit_lamp, weak, hubble and hubble_stars corrected, docs/README.md and VALIDATION.md's old tool paths renamed; the should-fixes: two docstrings, the optical and bell registers' strings bracketed so they read true (the generator's strings alike, the worlds byte identical), NODE_ALGEBRA's frame row naming `by_line`; the `astype(dtype)` of `moment_table` left for the main-merge commit (nature_beam.py is generic-bending's file). Commit: b12dd253 (b12dd253fabc69e92c359732fbc56911b880a33b in the branch's log). Check: see the commit message.
8. Main merged into the branch at 536edefb (one merge commit, no rebase; the owner's pace order, record 961). The textual conflicts resolved on this side: `docs/TEST_EXPECTATIONS.md` (main's rows for the quarks, the redshift, the weak force, `become`, the four reading tools, hubble_stars, orbit_lamp, the moving detector and c_measured kept with the paths of `tools/click_readings/`; the rows of `test_gallery_pages.py` and `test_two_stars.py`, deleted worlds, not taken), `examples/events/README.md` (main's flow-link section taken). The gate's root list: `momentum_pair` leaves (PR #855 made the optical wall the comparison ladder `split_ladder`; no root there), the reason texts say so; the bare name `dtype` no longer passes `astype` (a self-test). The should-fix of `moment_table`: the dtype named in each branch (`object` under `exact`, `np.int64` otherwise; the ages' column cast the same way), no behaviour change. NODE_ALGEBRA.md row 3c and section 2 carry the resolution. Local check: `ruff` and `pytest tests/test_integer_algebra.py` (38 passed); the CI run on PR #860 is the gate. Open after this commit: `tools/flow_link_readings.py` and `tests/test_flow_link.py` (new on main with PR #855) sit outside the package `tools/click_readings/`, a move of its own commit.
9. The first deferred row, after the merge SHA of `generic-bending` (PR #855, main at 536edefb): `examples/events/crowd_clock/` (series U, 8 worlds), `examples/events/cluster_clock/` (series V, 2), `examples/events/reader_clock/` (the reader, 5) with their generators, registers and READMEs, the designs `docs/designs/crowd_clock/`, `cluster_clock/`, `reader_clock/` and `tests/test_crowd_clock.py`, `test_cluster_clock.py`, `test_reader_clock.py` (30 files). Series T's generator `clock_word/make_worlds.py` carried series U's constants (the wheel, the lamp's reservoir and rate, the release and suspension pairs, the width, `beam_speed`) in place of the import of the deleted generator: its four worlds byte identical to the shipped files, its register output identical to the old generator's (the shipped `expectations.json` carries one hand-written block beside the generator's, `read_under_the_split_ladder_89f43572`, as before). The links in `docs/README.md` (three index rows), `docs/MIGRATION.md`, `docs/designs/clock_age/NOTE.md` and one link in `docs/designs/moving_detector/DESIGN.md` (the cart's file, PR #834 held: the one link into a deleted design turned to plain text so the navigation gate stays green, nothing else of it touched) made plain text; TEST_EXPECTATIONS' three rows and three sections removed; EXPERIMENTS.md carries the dated deletion section. Two leftovers of the main merge (Done 8) found by the navigation gate and fixed here: the hand series' section of `examples/events/README.md` (deleted with the hand worlds, record 894) had come back beside main's flow-link section and is removed again; the three links of main's new `docs/GROUP_STRUCTURE.md` into `docs/designs/hand/FORM.md` made plain text naming the deletion. Local: ruff and the tests the deletion touches (clock_word, navigation, register_map, check_scope, entity_definitions: 107 passed once the two leftovers were fixed); the CI run on PR #860 is the gate. Commit: the next line's SHA.

