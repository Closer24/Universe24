# Names review: codes that stand for things (the model owner's rule, record 1924)

Read-only review, 2026-09-25. Nothing in the repository was edited, committed
or pushed.

- Code: `origin/emitter-click` at `294a7c80` (`src/event_universe`, `tools`,
  `tests`, `examples/events`: 632 files).
- Living documents: `origin/main` at `676cfb87`; `docs/THE_EXPERIMENTS.md` on
  `origin/claude/new-boss-skills-file-4d1svd` at `b6aad2cf`.
- Skipped: `docs/LOG_*.md`, sections marked HISTORY (LAB_TOOLS.md parts 0 to
  12), ALGEBRA.md chapters 1 to 7, and the text of Markdown link targets (the
  record anchors are log headings, so they are records).
- Method: a regular-expression scan for each class of code (files and lines
  in the appendices), a Python AST scan of every assigned name, function,
  class and parameter, a scan of every JSON key, and a reading of each hit in
  its context.

**Allowed and left alone.** These stay as they are: math symbols inside
formulas that are named at first use (omega, K, W, T, u, k, v, gamma, e1 and
e2 in `meeting.py`, the L1 norm); record, PR, issue and commit numbers in
citations; section numbers in citations (for example "ALGEBRA.md 9.22 (8)" or
"(7a) (iii)") when the thing is also named; list markers (i), (ii), (v); and
established standard names (CHSH, Grover, the W boson, Deutsch-Jozsa).

**Rule for the rows below.** A citation such as "BUILD.md section 26 item 23"
or "DECLARATIONS.md section 15 M1-6" may stay only after the thing's name. It
is an offender when it is the only name, which is usual in refusal messages,
commit subjects, constants and test names.

---

## 0. Findings that make the renaming urgent: one code, several things

The same code names different things in different files. A reader cannot
resolve these without opening a table, and some of them resolve wrongly:

| Code | Meanings found in the active scope |
| --- | --- |
| M1 | (1) de Broglie's fringes (THE_EXPERIMENTS 9, ALGEBRA 9.22, LAB_TOOLS, RUN_LIST); (2) DECLARATIONS.md section 15 items `M1-1` to `M1-11` (world.py, detector_law.py, tests, SIMULATOR_DEFINITIONS 423, 429); (3) DERIVATIONS_BEAM 17.6 step M1, "the proper-time count" (engine.py 230, 747, 759, 869; covariant/*); (4) finding M1 of the physics-rule review of 408cf719 (tests/test_optical.py 69, 98, 741; optical/make_worlds.py `RUN_2026_09_21_M1`) |
| M2 | (1) the moving mass's energy; (2) DERIVATIONS_BEAM 17.6 step M2 (covariant/README.md 128 to 186, covariant/make_worlds.py, covariant/expectations.json 143, 145, 226) |
| R2 | (1) Sagnac; (2) the run-time overflow rule "R2" beside "R1" (world.py 4665 to 4667) |
| A1, A2, ... | (1) THE_EXPERIMENTS' six computed experiments A1 to A6; (2) the click theorem's two assumptions A1 and A2 (HIGHLIGHTS 262 to 333, 463, 586; POSTULATES 1923 to 1966; skills/paper-coordinator 86); (3) the old register codes of docs/EXPERIMENTS.md, A1 to A14, where A2 is the Bell test, A5 the electron repulsion, A6 light bending, A10 twice (the opening's width and the mass ladder) and A12 Malus (POSTULATES 424, 521, 567, 646, 660, 1156, 1369; HIGHLIGHTS 305, 465, 555, 592, 623; bell/, amplitude/, heisenberg/, tools/click_readings); (4) SCHEDULE.md rows "A", "A2", "B" (ALGEBRA 2934 to 2954, 5873; RUN_LIST 88), where A is now A3 and B is now A4 |
| D1 | (1) the Mach-Zehnder detector on +x (amplitude/*); (2) "the model owner's D1 of 2026-09-19", a decision, and "the D1 engine" (ENGINE.md 261; orbit/README.md 6, 85, 88) |
| series X | (1) Poisson after a detector (shell_clock/); (2) the directional drive (drive_b/, covariant/README.md 78, 98) |
| row 10 | (1) the moving mass's energy (THE_EXPERIMENTS 10); (2) the single-opening spread, "the paper's row 10" (NATURE.md 10; LAB_TOOLS 620; HIGHLIGHTS 506 to 508); (3) a fail_rows run (ENGINE.md 1223) |
| row 13 | (1) the light clock (THE_EXPERIMENTS 13, examples/events/pins.json); (2) light bending (NATURE.md 13; HIGHLIGHTS 339, 345, 351, 458, 499, 500; lamp_shell/README.md 1) |
| row 14 | (1) the receding index at k = 3 (THE_EXPERIMENTS 14, ALGEBRA 5846, LAB_TOOLS 638); (2) Newton's periods (NATURE.md 14; HIGHLIGHTS 428, 481) |
| 1b, 1d | (1) the Bell controls (ALGEBRA 5854, 5860); (2) two of "Bell's four settings 1a to 1d" (RUN_LIST 85; tools/click_readings/detector_law_bell.py 4); (3) "item 1b", the click's Gram form (HIGHLIGHTS 255, 692); (4) coupling world files `1b_m*.json`, the free-probe equivalence |
| ii-a, ii-b | (1) the box of side 20 and the box of side 28 (ALGEBRA 5886, 5887; RUN_LIST 81); (2) at rest and in motion (LAB_TOOLS 628; ALGEBRA 9.22 row 11, 5842) |
| F1 to F4 | (1) Nature24's engine packages F0 to F4 (origin/main's THE_EXPERIMENTS.md 34 to 81, still there until the Boss's branch lands); (2) audit and review finding labels F1 to F16 (record 567's audit, the physics-rule reviewer, the closing gate) in 18 code files (appendix A) |
| family `d` | (1) the down quark, declared inline in quarks/make_worlds.py 54, 55, 121; (2) the catalog's `detector_material_d` (entities/families.json 255) |
| verb letters | the six verbs are written as verb T, B, G, P, E and D (ALGEBRA 9, HIGHLIGHTS 493, 494, 507, 509, LAB_TOOLS 39, 113, 385, 386, 440, SIMULATOR_DEFINITIONS 200, detector_law.py). "verb G" (the merge) and "doppler-v1 and G deleted" (HIGHLIGHTS 597) also collide with the coupling G |
| "the eighteen" | The count moved from fifteen (RUN_LIST title and line 16, LAB_TOOLS part B's title) to sixteen, seventeen (ALGEBRA 9.22 (8) title, "THE SEVENTEEN") and eighteen, so each count word now names a different set |

**The written rule itself must change first (the Boss).** HIGHLIGHTS 5.4 line
512 (records 1813 and 1815) still says "a code (4a, R2, L-3, M1) only in
parentheses after it". skills/workflow.md lines 730 to 739 still allow "a code
... in parentheses as an index into a table". Record 1924 replaces both: no
code at all, even in parentheses. Both lines should say so before any
renaming starts, or the renaming has no rule to point to.

---

## 1. The canonical names (one English name per thing, used everywhere)

The slug is for file and folder names, JSON keys, test names and
identifiers. The name is for prose. The "Replaces" column lists every code
found for the thing in the active scope.

### 1.1 The eighteen measured experiments

| Now | Canonical name | Slug | Replaces |
| --- | --- | --- | --- |
| 1 | Bell's four settings | `bell_four_settings` | 1a to 1d, X13, "row 1", "the Bell run A2", A13 (old register), series L3, L5 and L6 (for the Bell worlds) |
| 1, control | Bell's no-signalling control | `bell_no_signalling_control` | 1d, "the control 1d" |
| 1, control | Bell's product-state control | `bell_product_state_control` | 1b as a control (ALGEBRA 5854), "the phase-form window" row 1b |
| 2 | Malus's four axes | `malus_four_axes` | 9, "row 9", X14, A12 (old register), "Malus's three settings" |
| 3 | The two slits | `two_slits` | 2a, X1, "row 3", A1 (old register) |
| 3, control | The two slits with one opening closed | `two_slits_one_opening` | 10, "the paper's row 10", "10 (a)", "10 (b)", "2a's CONTROL" |
| 4 | The pace fans | `pace_fans` | 5a, X2, "row 4", "the anisotropy of c" as a code |
| 5 | The muon's moving clock | `muon_moving_clock` | 4a, X3, "row 5", "the layer pin world", J4 (the older muon of covariant/) |
| 6 | The moving emitter's redshift | `moving_emitter_redshift` | 4b, X4, "row 6" (distinct from the cosmological series E below) |
| 7 | The round trip off a receding mirror | `receding_mirror_round_trip` | 4c, X5 ("transponder"), "row 7" |
| 8 | Sagnac's two-way light times | `sagnac_light_times` | R2, X6, "row 8" |
| 9 | De Broglie's fringes | `de_broglie_fringes` | M1, X7, "row 9" |
| 10 | The moving mass's energy | `moving_mass_energy` | M2, X8, "row 10" |
| 11 | The boxed clocks: the box of side 20 and the box of side 28 | `boxed_clock_side_20`, `boxed_clock_side_28` | ii, ii-a, ii-b, X9, "row 11" (which of ii-a and ii-b means "in motion" is inconsistent; see section 0) |
| 12 | The deep well's clock | `deep_well_clock` | X10, "row 12", "the cavity control" |
| 13 | The light clock | `light_clock` | LC, X11, "row 13", "five" in HIGHLIGHTS 509; the moving form LCm becomes "the moving light clock" (`moving_light_clock`, out by record 1895) |
| 14 | The receding index at one third of a Link per interval | `receding_index_speed_third` | v-m, X12, "row 14" |
| 14, control | The medium's index at rest | `medium_index_at_rest` | v, "the paper's row v", "14's CONTROL" |
| 15 | The receding index at one quarter of a Link per interval | `receding_index_speed_quarter` | X15, "row 15" |
| 16 | The two-qubit computer | `two_qubit_computer` | X16, "row 16", "the sixteenth row" |
| 17 | Mach-Zehnder | `mach_zehnder` | 2b, X17, "row 17" |
| 17, control | Mach-Zehnder with one arm blocked | `mach_zehnder_one_arm_blocked` | 17c, "17's CONTROL" |
| 18 | Sorkin's three openings | `sorkin_three_openings` | 2c, "row 18", "the eighteenth"; its seven worlds by the open openings: `sorkin_lower`, `sorkin_middle`, `sorkin_upper`, `sorkin_lower_middle`, `sorkin_lower_upper`, `sorkin_middle_upper`, `sorkin_all_three` in place of A, B, C, AB, AC, BC, ABC (N_A and the like stay as symbols in the formula) |

The two sets:

- "the measured experiments" replaces the eighteen, the seventeen, the sixteen
  and the fifteen;
- "the computed experiments" replaces the six.

The number stays in prose as a count ("the eighteen measured experiments"),
never as the name of the set.

### 1.2 The six computed experiments

| Now | Canonical name | Slug | Replaces |
| --- | --- | --- | --- |
| A1 | The atom's lines | `atom_lines` | A1; "7 (the atom's lines at the coupled modes)" in ALGEBRA 5871 |
| A2 | Light's dispersion by direction and wavelength | `light_dispersion` | A2 (THE_EXPERIMENTS and SCHEDULE.md) |
| A3 | The bound on the interval's length | `interval_length_bound` | A3, SCHEDULE.md "row A", "the bounds A" |
| A4 | The bound clock's second term | `bound_clock_second_term` | A4, SCHEDULE.md "row B", "B" in RUN_LIST 88 |
| A5 | Born's exponent and Tsirelson's limit | `born_exponent_and_tsirelson_limit` | A5; the paper's "2c" as a COMPUTATION of Born's exponent |
| A6 | Gravity's forms under a shell average | `shell_averaged_gravity` | A6 |

### 1.3 The engine parts still to be built (the owner's F0 to F4)

The Boss's branch already uses these names. Origin/main's
docs/THE_EXPERIMENTS.md lines 34 to 81 still carry the codes until that branch
lands.

| Code | Name | Slug |
| --- | --- | --- |
| F0 | the bodies with extents per axis | `bodies_with_extents` (already `tests/test_extents_and_face_slab.py`) |
| F1 | the travelling born profile | `travelling_born_profile` |
| F2 | the face slab | `face_slab` |
| F3 | the packets with momentum and the moving name | `moving_packet_and_name` |
| F4 | the polariser's axis and the crystal | `polariser_axis_and_crystal` |

### 1.4 The engine's six steps of an interval (BEAM_LAW section 3)

"step 1" to "step 6" are used as names about 230 times in the code (appendix
A) and 26 times in ENGINE.md. The engine's steps are:

1. step 1: the walk;
2. step 2: the readings;
3. step 3: the collision;
4. step 4: the detectors' step (the measured events and the click);
5. step 5: the self-creations;
6. step 6: the border and the merge.

Plan steps elsewhere reuse the same numbers:

- "every family under one wall, step 3";
- "stage (vii) step 4, the one click";
- "RUN_14.md step 6".

A comment should say "the collision" or "the detectors' step", not "step 3"
or "step 4". A plan step should use its name ("the one click", "the body's
drive under the one wall").

### 1.5 The six verbs

| Letter | Name |
| --- | --- |
| verb T | the translation (an accumulator by its rate) |
| verb B | the bilinear form |
| verb G | the group-ring sum (the merge) |
| verb P | the permutation |
| verb E | the evaluation |
| verb D | the division with the remainder kept |

### 1.6 Series letters (the register's world series)

These appear about 350 times in 95 code files and 22 times in HIGHLIGHTS 5.4
(the files are listed in appendix B). The folder name is already meaningful in
most cases, so the series should be called by its folder's plain name.

| Series | Name (and folder) |
| --- | --- |
| C | the coupling series (`coupling/`) |
| D | the orbit series (`orbit/`) |
| D3 | the orbit read by a lamp (`orbit_lamp/`) |
| E | the cosmological redshift series under the age reading (`redshift/`) |
| F | the physicist's Bohr design (`bohr/` notes) |
| G | the Hubble series (`hubble/`) |
| G2 | the Hubble series with stars (`hubble_stars/`) |
| H | the Bohr series (`bohr/`) |
| I | the nucleus series (`nucleus/`) |
| J | the weak-force series (`weak/`) |
| J1 | the neutron lattice trigger (`j1_lattice`, `j1_source`) |
| J2 | the phase window's readers (`j2_*`) |
| J3 | the bound neutron (`j3_*`) |
| J4 | the covariant muon (`covariant/j4_muon_*`) |
| K | the light beside a mass (`optical/`, the "box" and "beam of five lines") |
| L | the amplitude series (`amplitude/`) |
| L1 | the Mach-Zehnder split register |
| L2 | the click pages |
| L3 to L6 | the Bell worlds at N = 64, then at 1024 and 4096 |
| L7 | the cone worlds |
| N | the binding that costs content (`binding/`) |
| O | the moving detector (`moving_detector/`) |
| P | the hand (`tests/support/hand_worlds.py`) |
| Q | c measured behind a detector (`c_measured/`) |
| R | the quarks (`quarks/`) |
| S | the covariant readings (`covariant/`) |
| T | the clock's word (`clock_word/`) |
| U | the crowd clock's geometry (the retired `crowd_clock/`) |
| W | the optical series' matter declaration (optical/make_worlds.py 141) |
| X | Poisson after a detector (`shell_clock/`), and the directional drive (`drive_b/`): two meanings, so it must be split |

### 1.7 NATURE.md comparison rows cited by code in the scope

| Row | Name |
| --- | --- |
| 1a | the CHSH sum |
| 1b | the CHSH sum under the phase-form window |
| 1c | the order channel |
| 1d | the no-signalling check |
| 2a | the two-slit visibility |
| 2b | the Mach-Zehnder visibility |
| 2c | Born's exponent |
| 3 | the deceleration parameter |
| 4a | the muon's lifetime in flight |
| 4b | the moving lamp's redshift |
| 4c | the round-trip Doppler |
| 5a | the anisotropy of c by direction |
| 5b | the anisotropy between moving arms |
| 6 | Bohr's line ratio |
| 7a | the deuteron's binding fraction |
| 7b | the alpha-over-deuteron binding ratio |
| 8a | the neutron's decay-curve width |
| 8b | the neutrino's passage |
| 8c | the neutrino's mass |
| 9 | Malus at 45 degrees |
| 10 | the single-opening spread |
| 11a | the far lamp's brightness |
| 11b | the far lamp's stretch |
| 11c | Tolman's test |
| 12 | the clock's field at two distances |
| 13 | light bending |
| 14 | Newton's periods |

### 1.8 Roles written as numbers

The Boss should confirm the role names below.

| Now | Proposed |
| --- | --- |
| Reviewer 3 (1148 times on main; 51 in the scoped documents; 29 in code) | the gate reviewer |
| Reviewer 4 | the crystal's reviewer |
| Reviewer 2 | the earlier gate reviewer |
| Builder 2 | the reader builder |
| Builder 3 | name it by its task |

---

## 2. Owner: Nature24, the code on `emitter-click`

The items are ordered by how often each code is used. "Consumers" means the
other files that must change in the same commit.

### 2.1 The directional drive: `drive_b`, `drive-b-v1`, `DRIVE_B_RULE`, "form B" (289 uses in 40 files)

| Where | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| `src/event_universe/events/world.py` 459 to 461, 527, 1589 to 1591, 1699 to 1701, 1767 to 1796, 4168, 5736, 5742; `engine.py` (10); `run.py` (3); `measured.py` 359, 365, 380; `core/integer.py` (1) | world key `drive_b`, constant `DRIVE_B_RULE = "drive-b-v1"`, field `drive_b`, "form B" | world key `directional_drive`, `DIRECTIONAL_DRIVE_RULE = "directional-drive-v1"` (the code's own docstring calls it "the directional drive of a body") | yes: 15 optical `body_*` worlds, `drive_b/*.json`, `gate_set.json`, `tests/test_drive_b.py`, `test_optical_body.py`, `test_centred_step.py`, `test_record_trim.py`, `tools/check.py`, `tools/click_readings/drive_b.py` and README, ENGINE.md 273, 581, 590, 1066 to 1068, TERMINOLOGY 200, HIGHLIGHTS (see 4.1), docs/designs/drive_b/. The identity string is in registered fingerprints, so the migration note must map the old identity to the new one |
| folder `examples/events/drive_b/`, worlds `axis_b`, `plane_b`, `cube_b`, `axis_main`, `plane_main`, `cube_main` | "b" = form B, "main" = the per-axis drive | `examples/events/directional_drive/`, worlds `axis_directional`, `plane_directional`, `cube_directional` and `axis_per_axis`, `plane_per_axis`, `cube_per_axis` | same as above |
| `tests/test_drive_b.py`, `tools/click_readings/drive_b.py` | `drive_b` | `test_directional_drive.py`, `directional_drive.py` | `tools/check.py`, tools/click_readings/README.md |
| atoms/make_worlds.py 1, 8, 71, 118, 132, 267; atoms/README 1 to 67; orbit/README 155 to 239; orbit_lamp/* | "series under form B", `rays-atoms-hydrogen-r12-form-b-v1` | "under the directional drive", `...-directional-drive-v1` | atoms expectations, tools/click_readings/bohr.py |

### 2.2 The Mach-Zehnder detectors `D1`, `D2` (277 uses)

| Where | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| `examples/events/amplitude/make_worlds.py` 26 to 45, 212 to 216, 436, 437, 482 and more (93); amplitude/README.md (44); `tests/test_amplitude_layer.py` (19); `tests/test_amplitude_mz_345_n.py` (18); amplitude/expectations.json | `D1` (at (4, 3), fed along +x), `D2` (at (3, 4), fed along +y) | `detector_plus_x`, `detector_plus_y` (a name by place; "bright" and "dark" change from world to world) | yes: the detector names are world keys and expectation keys; every `mz_*` and `ev_*` world is regenerated |
| orbit/README.md 6, 85, 88; ENGINE.md 261 | "the model owner's D1 of 2026-09-19", "the D1 engine" | "the owner's push-width decision of 2026-09-19 (record N)", "the engine of that decision" | no |

### 2.3 Single-letter and coded family names (JSON; the most repeated keys in the repository)

| Family (entities/families.json) | Uses | Proposed | Consumers |
| --- | --- | --- | --- |
| `m` (`mass_m`) | 94216 table keys (flow_link, lamp_shell, lensing, newton_side, optical, orbit_lamp, redshift) and 15 declarations (coupling) | `central_mass` | every world of those folders (regenerated by their `make_worlds.py`), their expectations and readers |
| `nu`, `n`, `p`, `s`, `beta` | 11405, 10760, 10755, 10755, 4234 keys in weak/*.json | `neutrino`, `neutron`, `proton`, `fixed_source`, `beta_electron` | weak/*, `tests/test_weak_readings.py`, `tests/test_host_batches.py`, `tests/test_w_world.py`, `tools/click_readings/weak.py`; nucleus, binding, atoms and coupling for `p` and `n` |
| `e`, `mu`, `u`, `d`, `q`, `w`, `nubar` | catalog and quarks | `electron`, `muon`, `up_quark`, `down_quark`, `test_charge`, `w_boson`, `antineutrino` | quarks/*, `tools/click_readings/quarks*.py`, covariant/* |
| `d` (`detector_material_d`) | catalog line 255 | `plain_detector` (and fix the clash with the down quark) | worlds that use it |
| `neutron` (`neutron_star_material`) | catalog | `neutron_star` (it clashes with `neutron` above) | its worlds |
| `sa`, `sb` (`choosers`) | 233 and 234 keys (amplitude, bell) | `alice_chooser`, `bob_chooser` | bell/make_chooser_worlds.py, amplitude/*, tools/click_readings/bell_choosers.py |
| `px1` to `mz4` (24 families, `thrown_sources`) | 74 keys each (hubble/) | `star_plus_x_1` to `star_minus_z_4` | hubble/*, tools/click_readings/hubble.py (`at0`, `at1`) |
| `s_px1` to `s_mz4` (`hubble_stars`) | 168 keys each (hubble_stars, covariant) | `hubble_star_plus_x_1` and so on | hubble_stars/*, covariant/coasting_none_covariant.json, readers |

### 2.4 Experiment row codes inside the code (appendix A lists every line)

| Where | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| `examples/events/detector_law/make_worlds.py` 27, 51, 66, 182, 187, 392, 451, 666, 753, 787, 831, 870, 881; detector_law/README.md 46 to 50 | "Rows 2c", "row 2a", "row 5a", "Row 4b", "row 13", R2, M2, 4a | the canonical names in section 1.1 | no |
| same file, constants | `R2_CHAIN`, `R2_TICKS`, `R2_GRACE` | `SAGNAC_CHAIN`, `SAGNAC_TICKS`, `SAGNAC_GRACE` | no |
| same file, constants | `L3_K`, `L3_RELEASE`, `L3_LAMP_AMOUNT` ("the L3 series' K") | `BELL_N2048_LABEL_SCALE`, `BELL_N2048_RELEASE`, `BELL_N2048_STOCK` | no |
| `src/event_universe/events/detector_law.py` 135, 318, 326 | "rows 1a and 1d", "R2's blocks" | "Bell's settings and the no-signalling control", "the Sagnac blocks" | no |
| massive_record/make_worlds.py 26, 35, 42, 81, 299, 418, 458, 500; read_runs.py 22, 29, 61, 448, 512; pins.py 20, 22, 239, 271, 298; README 41 to 56 | 4a, 4b, ii-a, v-m | the canonical names | no |
| `examples/events/pins.json` | key `light_clock_60`, `"row": "13 the light clock: ..."`, detector `at_a` | key `light_clock`, drop the row number from `"row"` (or rename the key `experiment`), detector `at_well` | `tools/run_inputs.py`, `tests/test_run_inputs.py` |
| sagnac_*.json, light_clock_60.json, detector_law/make_worlds.py, tests/test_receiver_by_name.py | receivers `at_a`, `at_b`, wells "A" and "B" | `at_near_well`, `at_far_well` (Sagnac); `at_well` (the light clock) | yes: world files, readers, LAB_TOOLS, ALGEBRA 9.22 rows 8 and 13, RUN_LIST |
| tools/click_readings/detector_law_bell.py 4; README 24 | "rows 1a to 1d and Malus's row 9" | "Bell's four settings and Malus's four axes" | no |
| world.py 4665 to 4667 | run-time rules "R1", "R2" | "the per-push bound", "the column-sum bound" | no |
| covariant/*, engine.py 230, 747, 759, 869 | DERIVATIONS_BEAM 17.6 steps "M1", "M2", "M8", "N1" to "N3" | "the proper-time count", "the energy accumulator" and so on (name each step) | DERIVATIONS_BEAM 17.6 |
| tests/test_optical.py 69, 98, 741; optical/make_worlds.py `RUN_2026_09_21_M1` | "M1 of the physics-rule review" | "the review's residue finding"; constant `RUN_BEFORE_THE_RESIDUE_FIX` | no |

### 2.5 Sub-series and prefixes in weak, covariant and quarks

| Where | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| weak/make_worlds.py 157 to 163 and more: `J1_SIDE`, `J1_PITCH`, `J1_PER_AXIS`, `J1_SHELL`, `J1_SOURCE`, `J1_TICKS`, `J2_TICKS`, `J3_SIDE`, `J3_WIDTH`, `J3_SHELL`, `J3_TICKS`, `J3_FREE_TICKS`, `j1_world(s)`, `j2_world(s)`, `j3_world(s)`, `j2_expected`, `j2_expectations` | J1, J2, J3 | `TRIGGER_LATTICE_*`, `PHASE_READERS_*`, `BOUND_NEUTRON_*`; `trigger_lattice_worlds`, `phase_reader_worlds`, `bound_neutron_worlds` | tools/click_readings/weak.py (`j2_expectations`), tests/test_weak_readings.py, tools/check.py 74 |
| weak/ file names | `j1_lattice`, `j1_source`, `j2_default`, `j2_filter`, `j2_ladder`, `j2_stride2`, `j2_stride2_odd`, `j3_deuteron`, `j3_deuteron_crowd`, `j3_neutron_free`, `w_exchange` | `trigger_lattice`, `trigger_source`, `readers_default_width`, `readers_filter`, `readers_ladder`, `readers_stride_two`, `readers_stride_two_odd_centre`, `bound_neutron_deuteron`, `bound_neutron_crowd`, `free_neutron`, `w_boson_exchange` | weak/README, expectations, readers, tests |
| tests/test_weak_readings.py | `test_the_j2_register_is_derived_...`, `test_the_j1_and_j3_register_is_...` | `test_the_phase_readers_register_...`, `test_the_trigger_and_bound_neutron_register_...` | no |
| covariant/ | `j4_muon_rest`, `j4_muon_3640`, `j4_muon_12856`; `test_the_registered_j4_runs_replay_bit_exact` | `muon_at_rest`, `muon_momentum_3640`, `muon_momentum_12856`; `test_the_registered_muon_runs_replay_bit_exact` | covariant README, expectations, tools/click_readings/covariant.py |
| quarks/ | `q1_proton_line` to `q7_proton_dressed` | drop the prefix: `proton_line`, `neutron_line`, `proton_triangle`, `deuteron_rectangle`, `deuteron_line`, `proton_kick`, `proton_dressed` | quarks README ("q1 with the end u kicked"), expectations, readers |
| tests/support/hand_worlds.py 95, 110; weak/make_worlds.py 481 | `w_world`, `wu_world`, `w_families` | `w_boson_world`, `w_boson_up_quark_world` | tests/test_hand.py, tests/test_w_world.py |

### 2.6 Old register codes and series L1 to L7 (appendix A)

| Where | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| bell/README.md 1, 5, 129 to 220; bell/make_*.py; amplitude/make_worlds.py 107, 274, 838, 1160, 1193; tests/test_nature_beam_worlds.py 3, 26, 205; tools/click_readings/bell*.py, README 22, 23, 67 | "The Bell run A2" | "the Bell run with two detectors" | docs/EXPERIMENTS.md headings (records: link by name) |
| heisenberg/README.md 1, 6; heisenberg/make_worlds.py 1, 4; tools/click_readings/heisenberg.py 1, 23; lensing/README 9 | "The Heisenberg run A10" | "the opening's width and the spread behind it" | tools/click_readings/README 29, 73 |
| amplitude/README 507 to 591; amplitude/make_worlds.py 183 to 3141; tests/test_amplitude_malus.py 1 | "A12" | "Malus's law and the three-polariser chain" | no |
| amplitude/make_worlds.py, README, pages/build_pages.py, tests/test_amplitude_mz_345_n.py 6, 25, test_amplitude_pair.py, test_amplitude_gate.py, test_amplitude_cone.py, test_hand.py, test_algebra_visualizer.py 7, heisenberg/README 49, 50 | L1 to L7 | section 1.6 | no |

### 2.7 Reviewer numbers and finding codes

| Where | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| world.py 781, 887, 926, 1023, 2234, 5643; detector_law.py 649, 1537; diagnostics/massive_record_margin.py 2; detector_law/make_worlds.py 49 to 578; massive_record/make_worlds.py 622, 626; tests/test_massive_record.py 272 to 1591; tests/test_preflight_worlds.py 70; tools/preflight_worlds.py 13, 91, 114 | "Reviewer 3" | "the gate reviewer" (section 1.8) | no |
| clock_word/make_worlds.py 253, 258, expectations.json 117; tests/test_clock_word.py 177; test_coupling_readings.py 179; tools/click_readings/coupling.py 851, 997; covariant/README 25, 29; tests/test_covariant_readings.py 627, 630; weak/README 159, 161; tests/test_weak_readings.py 54, 56, 250, 271; tools/click_readings/weak.py 19, 107; bohr.py 428; nucleus.py 375, test_nucleus_readings 129; quarks.py 278, test_quarks_expectations 189; lensing.py 53 | "the audit of record 567, F1" and F3 to F16 | the finding's content, for example "record 567's finding that a crowd's k is a replay of the store", then the record number | no |
| tests/test_nature_beam_collision.py 26; test_nature_beam_detector.py 893; test_nature_beam_push.py 60 | "the reviewer's F1(c)", "the closing gate's finding F1", "the reviewer's F6" | name the finding ("rays meet at a Node only ...", "the wave pointer ...", "the fractional floor") | BEAM_LAW.md notes 18 and 19 use the same codes |
| detector_law/make_worlds.py 188 and more | "Reviewer 3's arithmetic", "MUST 3" | "the gate reviewer's third requirement: <its content>" | no |

### 2.8 Build items, engine lines and declaration items used as names

| Where | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| refusal messages in world.py and detector_law.py, for example `"(BUILD.md section 26 item 23)"`, item 15, item 24 | a build item as the only name of a rule | the rule's name first: "(the bodies with extents per axis; BUILD.md section 26 item 23)" | tests that match message text |
| detector_law.py 318, 1537; tests/test_massive_record.py 272, 1399, 1529; `detector-law-v1, line B` comments | "line B", "line 7", "Line 7", "line 8", "line 2" | "the block's grace for its emitted records", "a set bound to a block is a receiver", "the order channel's two keys", "the take's second line" | BUILD.md sections 14 and 15 |
| world.py 446, 922, 3471 to 3501, 5284, 5601, 5641, 5647; detector_law.py 318; diagnostics/massive_record_margin.py 449; tests/test_massive_record.py 531, 1060, 1399, 1631; detector_law/make_worlds.py 16 to 396 | "section 15 M1-4", "M1-6", "M1-10", "L-1", "L-3", "L-6" | the declaration's subject: "the barrier pair", "the massive worlds' bound 2^32", "the gap pair of the mirror" | DECLARATIONS.md section 15 |
| tests/test_massive_record.py 977 | "The series' two keys of step 5 (BUILD.md section 4 step 7 and section 5 (v-m))" | "the receding index's two keys" | no |
| `step N` comments (about 230; appendix A, class 1.4) | "step 4", "stage (vii) step 4", "every family under one wall, step 3", "RUN_14.md step 6" | section 1.4 | no |
| orbit_lamp/make_worlds.py 25 to 690; examples/events/README.md 420 to 447 | "Side A", "Side B" of Newton on the side | "the moving-detector side", "the lamp-on-the-probe side" | docs/designs/newton_clicks/ |
| orbit/README.md 152, 191, 211, 238; orbit/make_worlds.py 85 | "row 58 (Kepler's three laws)" | "Kepler's three laws" | no |
| lamp_shell/README 1, 7, 67, 112; make_worlds.py 1, 229; expectations.json 10422 | "row 13, STEP 2" | "the light bending's crowd stretch" | no |
| amplitude/README 557 to 639; make_worlds.py 350, 3144, 3159, 3316; expectations.json 4061, 4330; tests/test_amplitude_malus.py 9 | "the auditor's round 10 part 2", "row 4" | name the audit point | no |
| redshift/README 30; shell_clock/README 9, make_worlds.py 10 | "NATURE row 12" | "the clock's field at two distances" | no |
| verb letters: detector_law.py (verb B, D, G, T), tools/algebra_visualizer/panels.py (verb T) | verb T, B, G, D | section 1.5 | ALGEBRA 9 |

### 2.9 Opaque identifiers (from the AST scan)

| File: identifier | Proposed | Consumers |
| --- | --- | --- |
| `massive_record/make_worlds.py`: `MOMENTUM_K3`, `MOMENTUM_K4` | `MOMENTUM_SPEED_THIRD`, `MOMENTUM_SPEED_QUARTER` | no |
| `orbit_lamp/make_worlds.py`: `K17_SUFFIX`, `RUNG_K17`, `WIDTH_K17`, `MOMENTUM_FACTOR_K17`, `Y_D_K17`, `WORLDS_K17`, `pace_k17`, `k17` | `..._SPEED_SEVENTEENTH` (or `_SLOW_PROBE`) | orbit_lamp worlds `r12_k17*`, `r24_k17*` |
| `optical/make_worlds.py`: `CAPTURE_NEAR_G1`, `RUN_2026_09_21_M1` | `CAPTURE_NEAR_WITH_WALL`, `RUN_BEFORE_THE_RESIDUE_FIX` | no |
| `tools/click_readings/nucleus.py` 394: `LINE_P1_PUSH` | `LINE_END_PROTON_PUSH` | its test |
| `tools/click_readings/coupling.py` 1107: `pp`, `pp4` | `like_charges`, `like_charges_probe_4` | no |
| `tools/click_readings/orbit_lamp.py` 556: `t12`, `t24` | `period_near`, `period_far` | no |
| `tools/click_readings/hubble.py`: `at0`, `at1` | `age_before`, `age_after` (check use) | no |
| `tools/amplitude_probe.py`: `by_s1` | name by what S_1 is (the flight's step sum) | no |
| `amplitude/pages/build_pages.py`: `S64`, `lx0`, `ly0`, `lh` | `chsh_sum`, `ladder_left`, `ladder_top`, `ladder_height` | no |
| `bell/make_chooser_worlds.py` 309: `alice_a2`, `bob_b2` | `alice_second_axis`, `bob_second_axis` | no |
| `tests/test_massive_record.py` 710, 711: `r_m2`, `r_l2`, `x_n0`, `y_n0` | `matter_remainder_next`, `light_remainder_next`, `matter_row_start`, `light_row_start` | no |
| `tests/test_amplitude_mz_345_n.py`: `to_d2` | `share_to_plus_y_detector` | no |
| `tests/test_board_properties.py` 189: `the_48` | `signed_axis_permutations` | no |
| `src/event_universe/events/measured.py` 313: `grid` (a table of accumulators; "grid" is also a forbidden noun for the GameBoard) | `per_axis_accumulators` | callers |
| `src/event_universe/events/amplitude.py` 134: `cmul` | `complex_product` | callers |
| `src/event_universe/events/nature_beam.py`: `ZERO3`, `PAIR_I`, `PAIR_J` | `ZERO_VECTOR`, `MOMENT_ROW_AXIS`, `MOMENT_COLUMN_AXIS` | callers |
| `tools/click_readings/*_replay.py`: `tmp` | `scratch_directory` | no |

### 2.10 Test names

| Where | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| about 70 tests in 10 files: 29 in tests/test_massive_record.py, 8 in test_board_properties.py, 8 in test_initial_state.py (with `test_a_a_...`), 6 in test_body_conditions.py, 5 in test_extents_and_face_slab.py, 4 in test_receiver_by_name.py, 3 in test_emitter.py, 2 in test_flux_reading.py, and single ones in test_run_inputs.py and test_amplitude_bell_24_4.py (`test_s_...`) | an enumeration letter as a prefix: `test_b_...`, `test_aa_...`, `test_ah_...`, `test_z_...` | drop the prefix; the rest of each name is already meaningful | BUILD.md and commit messages cite "test (ac)", "test (h)", "test p"; test_massive_record.py docstrings "(i, k, u, ai, ak, ag ... removed)"; appendix A |
| tests/test_board_properties.py | `test_1_equivariance_under_the_48` to `test_8_the_same_input_gives_the_same_output` | `test_equivariance_under_the_cube_group`, `test_translation_on_the_torus`, ... (drop the numbers) | commit messages "test 8"; ALGEBRA 9.20 numbering |
| tests/test_drive_b.py 370, 399 | `test_the_reviewers_pin_1_...`, `_pin_2_...` | `test_the_wandering_direction_pin`, `test_the_hand_over_transient_pin` | no |
| tests/test_amplitude_bell_24_4.py (26 lines), test `test_s_over_the_quadruple_...` | named after DERIVATIONS_BEAM section 24.4 | `test_amplitude_bell_plateau_over_n.py`, `test_the_chsh_sum_over_the_four_settings_...` | tools/check.py mapping |
| tests/test_amplitude_mz_345_n.py | "mz", "345" | `test_mach_zehnder_split_3_4_5_by_n.py` | same |
| tests/test_paper_cut30.py (and the `cut30/` assembler it tests) | "cut30" | `test_thirty_page_manuscript_assembly.py` (`thirty_page_manuscript/`) | paper tooling |
| tests/test_w_world.py | "w world" | `test_w_boson_exchange_world.py` | no |
| tests/test_run_series.py | `test_the_series_7_read_records_replay_under_the_landed_form` | name series 7 by its content | no |

### 2.11 File and folder names with codes (examples/events)

| Folder | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| coupling/ | `1a_m1`, `1a_m4`, `1a_m16`, `1b_m1`, `1b_m4`, `1b_m16`, `2`, `3`, `3a`, `3b`, `4`, `5`, `5_long`, `5p`, `6`, `7_00`, `7_pp`, `7_pm`, `7_mp`, `7_mm`, `7_pp_m4` | `equivalence_fixed_probe_mass_1` (and 4, 16), `equivalence_free_probe_mass_1` (and 4, 16), `third_law_pair`, `superposition_both`, `superposition_heavy_alone`, `superposition_light_alone`, `retardation_probes`, `far_field`, `far_field_long`, `far_field_axis_pattern`, `probe_clock`, `electric_neutral`, `electric_plus_plus`, `electric_plus_minus`, `electric_minus_plus`, `electric_minus_minus`, `electric_plus_plus_probe_4` | coupling/README (table and prose "item-2 pair"), make_worlds.py, tools/click_readings/coupling.py (`runs["7_pp"]`), tests/test_coupling_readings.py, the register |
| amplitude/ | `ev_29`, `ev_169`, `mz_345`, `mz_345_n32`, `mz_345_n128`, `mz_equal`, `mz_half`, `mz_quarter`, `mz_balanced`, `mz_unequal_f0/f8/f16`, `malus_a`, `malus_b`, `malus_c`, `rotations_3` | `bomb_tester_hypotenuse_29`, `bomb_tester_hypotenuse_169`, `mach_zehnder_split_3_4_5` (and `_n32`, `_n128`), `mach_zehnder_equal`, and so on, `mach_zehnder_unequal_rate_0/8/16`, `malus_45_degrees`, `malus_crossed`, `malus_rotated_chain`, `three_rotations` | amplitude/README, make_worlds.py, expectations.json, the tests of amplitude/, pages/build_pages.py |
| heisenberg/ | `w1_wave` to `w27_beam` | `width_1_wave` to `width_27_beam` | README, make_worlds.py, identity strings `rays-heisenberg-w1-wave-v1`, tools/click_readings/heisenberg.py |
| orbit/ | `s1_r12` to `s32_r24_lamp` | `source_1_radius_12` to `source_32_radius_24_lamp` | README, reader |
| bohr/, atoms/, orbit_lamp/ | `r2` to `r16`, `hydrogen_r12`, `r12_k17`, `r24_4m` | `radius_2`, `hydrogen_radius_12`, `radius_12_slow_probe`, `radius_24_heavy_4` | readers, expectations, identity strings |
| flow_link/, optical/ | `ring_b6_g0`, `body_b10_g1`, `mass_g0`, `near_g1`, `matter2_g0` | `ring_impact_6_no_wall`, `body_impact_10_with_wall`, `mass_no_wall`, `near_with_wall` (g = the wall exponent gamma 0 or 1; b = the impact distance) | expectations keys `mass_g1`, `near_g1`, `shift_g1_over_g0`, `arrival_g1_over_g0`, readers, tests/test_optical*.py |
| moving_detector/ | `cart_k3`, `cart_k5`, `cart_k9`, `cart_k17`, `capability_k5` | `cart_speed_third`, `cart_speed_fifth`, `cart_speed_ninth`, `cart_speed_seventeenth`, `capability_speed_fifth` | identity strings `beam-moving-detector-cart-k3-v1` and others, README, tools/moving_detector_readings.py |
| massive_record/ | `layer_pin_k3_14`, `layer_pin_rest_14`, `redshift_k3`, `redshift_control`, `sagnac_k3`, `sagnac_rest`, `matter_waves_12`, `matter_front_12`, `moving_20`, `rest_20`, `deep_well_k3_40`, `light_clock_60`, `index_moving_long_k3_away` and so on, `EXPLORATORY_layer_k3_14/` | the slugs of section 1.1 with `_at_rest` or `_moving`, for example `muon_moving_clock_moving`, `sagnac_light_times_at_rest`, `boxed_clock_side_20_moving`, `receding_index_speed_third` | pins.json, read_runs.py, pins.py, RUN_LIST, LAB_TOOLS, tests/test_massive_record.py and test_body_conditions.py |
| bell/ | `a0_b8`, `written_a25_b29`, `order_a0_21_42_b0` | `alice_0_bob_8` and so on (the offsets are values; a and b are the parties) | README, readers |
| weak/, quarks/, covariant/ | see section 2.5 | | |

---

## 3. Owner: the mathematician

### 3.1 docs/ALGEBRA.md, chapters 8 and 9 (lines 2153 to 6653)

| Line(s) | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| 2349, 2351, 2910, 2912, 3355, 3528, 4188, 4200, 4212, 5043, 5123, 5494, 5600, 5613, 5837, 6016, 6265, 6396, 6521 | 4b, "row 4b" | the moving emitter's redshift | THE_EXPERIMENTS, LAB_TOOLS, RUN_LIST |
| 2788, 2904, 3648, 4991, 5017, 5120, 5590, 5612, 5794, 5820, 5836, 5885, 5892, 6259 | 4a, "row 4a" | the muon's moving clock | same |
| 2915, 5112, 5614, 5838, 6275 | 4c | the round trip off a receding mirror | same |
| 2916 | "row 5b, five's 1 and 1" | the anisotropy between moving arms | NATURE.md |
| 2919, 5615, 5839, 6279 | R2 | Sagnac's two-way light times | same |
| 4304, 4644, 4651, 5065, 5616, 5828, 5840, 6551, 6605, 6616, 6640 | M1 | de Broglie's fringes | same |
| 4308, 4644, 4919, 5112, 5617, 5841, 6187, 6257, 6607, 6618 | M2 | the moving mass's energy | same |
| 5618, 5842, 5886, 5887, 6259 | ii-a, ii-b | the box of side 20, the box of side 28 (and say "at rest" or "in motion" in words) | LAB_TOOLS 628 (conflicting use) |
| 5832, 5854, 5860 | 1b, 1d ("the controls 1b, 1d") | Bell's product-state control, Bell's no-signalling control | THE_EXPERIMENTS 1 |
| 3496 | "the lab tools' specification 1.1a" | name the clause | LAB_TOOLS |
| 5827 to 5870 (the table of (8)) | the "Row" column as "1 Bell, ...", "17c Mach-Zehnder, one arm blocked", "18 Sorkin's ..."; prose "row 3's layer", "as row 14", "rows 1, 2, 16, 17, 17c", "rows 3, 8, 9, 10, 13, 14, 15", "row 9's runs" | keep the column as an ordinal if wanted, but refer to rows by name in the cells and the prose: "the two slits' layer", "as the receding index at one third" | THE_EXPERIMENTS |
| 5860 to 5873 | "1b, 1d, v and 10 enter as the controls", "2c ... as an eighteenth", "7 (the atom's lines)", "LCm (the light clock in motion)", "the bounds A, A2 and B" | the canonical names in sections 1.1 and 1.2 | RUN_LIST 88; THE_EXPERIMENTS |
| 5818, 5821 (title of (8)) | "THE SEVENTEEN" | "the measured experiments" (the table already has eighteen rows) | THE_EXPERIMENTS 20 quotes this title |
| 2934, 2943, 2954 | "SCHEDULE.md row A", "row A", "row B" | the bound on the interval's length; the bound clock's second term | SCHEDULE.md |
| 2231, 2591, 2656, 2710, 3027, 3058, 3145, 3165, 3173, 3667, 3669; 4856, 5051 | Reviewer 3; Reviewer 4; "Reviewer 3's C11"; 9.10's title "Reviewer 3's forbidden branches" | the gate reviewer; the crystal's reviewer; name finding C11 by its content | section headings are linked from other files |
| 3312, 3498, 3719, 3746, 3768, 4158, 4507, 4571, 4880, 5672, 5678, 5984, 6082; 3442, 3684, 3854, 4087, 4264, 6234, 6245; 3487, 3534, 4085, 4896, 4965, 6378; 4085; 5984 | verb B, verb T, verb D, verb G, verb P | section 1.5 | LAB_TOOLS, SIMULATOR_DEFINITIONS, HIGHLIGHTS, detector_law.py |
| 2436, 2460, 2480, 2537, 3294, 3402, 4811, 4812, 5152, 5182, 5236, 6405 | "the 48" | the cube group (its 48 signed axis permutations) | HIGHLIGHTS, LAB_TOOLS, TERMINOLOGY 62, SIMULATOR_DEFINITIONS 208, code |
| 4936, 5812, 5862, 6012, 6047, 6293, 6326, 6603 | "the specification's part B", "part A" | "the placed experiments of LAB_TOOLS.md", "the tool cards of LAB_TOOLS.md" | LAB_TOOLS headings |
| 5331 to 5339, 5504 (the property test) | "(3a)", "(3b)", "(3c)", "(6b)", "(6c)" used alone ("residue-blindness (6c)") | the property's name first, the number after | test_board_properties.py |

### 3.2 docs/designs/lab_tools/LAB_TOOLS.md (lines 1 to 677; parts 0 to 12 are HISTORY)

| Line(s) | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| 542 (heading B) | "THE FIFTEEN EXPERIMENTS AS PLACED TOOLS" | "The measured experiments as placed tools" | THE_EXPERIMENTS 22, ALGEBRA links |
| 582, 626, 666 / 582, 627, 669 | M1, M2 ("M1 and M2 (matter waves)") | de Broglie's fringes; the moving mass's energy | ALGEBRA |
| 617 | "Bell, four settings (1a to 1d)" | drop the codes | no |
| 618 | "Malus, four settings (9)" | drop | no |
| 619, 620, 637 | "(2a)", "as row 2a", "2a's CONTROL, the paper's row 10", "as row 2a" | the two slits; the two slits with one opening closed | no |
| 621 | "(5a)" | drop | no |
| 622, 623, 624, 150, 293 | (4a), (4b), (4c) | drop | no |
| 625 | (R2) | drop | no |
| 628, 629 | "(ii-a, ii-b)", "ii-a: ... ii-b: ...", "as ii-b" | the box of side 20; in motion (the conflict with ALGEBRA 5886 must be resolved) | ALGEBRA |
| 631 | "(v-m)" | drop | no |
| 633, 636, 637, 638; 223, 250, 271 | "(16; ...)", "(17; ...)", "17's CONTROL", "(18, THE EIGHTEENTH ...; the paper's row 2c)", "(14's CONTROL, the paper's row v)", "as row 17", "Row 17" | the canonical names | no |
| 423, 660 | "THE SIXTEENTH ROW'S TOOLS"; "the specification's part B rows 16" | "the two-qubit computer's tools" | SIMULATOR_DEFINITIONS 243 |
| 39, 113, 385, 386, 440 | verb B, verb P, verb T | section 1.5 | ALGEBRA |
| 262, 420 | "the 48" | the cube group | as above |
| 33, 69, 423, 635 | "part A", "part B" as names | "the tool cards", "the placed experiments" | ALGEBRA, THE_EXPERIMENTS, SIMULATOR_DEFINITIONS |
| (the "A.1" to "A.14" card numbers after tool names, for example "the crystal (A.11)") | citations after a name | allowed; never write "A.14" alone (for example "a co-moving name (A.14)" is fine) | no |

### 3.3 SIMULATOR_DEFINITIONS.md

| Line(s) | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| 218, 244 | "(4a)" | a citation of 9.19 (4a); write "9.19 item (4a)" or name the item, since "4a" is also the muon's moving clock | no |
| 243 | "LAB_TOOLS.md part B rows 16" | "the two-qubit computer's placement" | LAB_TOOLS |
| 249, 252 | "the two_slits and M1 layers", "the fans, M2 and the cart" | de Broglie's fringes; the moving mass's energy | no |
| 263, 336, 354 | "Reviewer 3's preview", "Reviewer 3's line F" | the gate reviewer's preview; name the line's content ("a body with seed 0 ... exception") | no |
| 423, 429, 431 | "DECLARATIONS.md section 15 M1-11", "(M1-11)", "section 15 L-1" | the declaration's subject first | DECLARATIONS.md |
| 200 | verb T | the translation verb | no |
| 208 | "the 48" | the cube group | no |

### 3.4 POSTULATES.md

| Line(s) | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| 1923, 1924, 1928, 1966 | A1, A2 (the click theorem's assumptions) | "the one-Node-per-interval assumption", "the split-phase assumption" (they collide with the computed experiments A1 and A2) | click_frame/DERIVATION.md section 0, HIGHLIGHTS 262 to 586, skills/paper-coordinator 86 |
| 424, 521, 567, 646, 660, 1156, 1369 | "experiment A14", "A6", "A5", "A10", "A13" of docs/EXPERIMENTS.md | the experiment's name ("the light bending by direction", "the electron repulsion", "the mass ladder") | EXPERIMENTS.md |
| 317, 829, 869 | "chapter 6, row 1c" | "the order channel" | ALGEBRA 6 |
| 316, 867 | "series L and L6" | "the amplitude series and its Bell worlds at N = 1024 and 4096" | no |
| 621 | "4a and 4b" | the muon's moving clock and the moving emitter's redshift | no |
| 1153, 1373 | "feature 2b", "features 12, 8c, 2b and 8b" | the features' names (PHYSICAL_FEATURES.md) | PHYSICAL_FEATURES.md |
| 1247 | "rows 23a to 23l" | name the block of rows | POSTULATES_BY_ALGEBRA.md |
| 1901 | "6.2 row 2a" | the two-slit visibility | no |
| 265 | "Reviewer 3's PUSH_BALANCE.md 12.6 (c)" | the gate reviewer | no |
| 777 | "the 48" | the cube group | no |
| "hypothesis 11" and "experiment A13" (1156) | numbered hypothesis | its name | HYPOTHESES.md |

---

## 4. Owner: the Boss

### 4.1 docs/HIGHLIGHTS.md section 5.4 (lines 206 to 713)

| Line(s) | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| 512 | the rule "a code (4a, R2, L-3, M1) only in parentheses after it" | restate as record 1924: no code at all, in parentheses or not | skills/workflow.md 730 to 739 |
| 253, 255, 262, 274, 303, 404, 410, 457, 468, 572, 597, 652, 692; with drive-b / drive_b at 253, 255, 303, 410, 572, 652, 692 | "form B", "drive-b-v1", "form A" (572, amplitude-v1's alternative: a second meaning of "form B", which the line itself has to explain) | "the directional drive" (`directional-drive-v1`); "the all-local alternative" for amplitude's form B | the code (section 2.1) |
| 260, 262, 645; 260 | "Lorentz, A", "Lorentz, B", "route C" | "the law's falsifiable counter row", "the covariant readings", "the seventh-verb route" | TERMINOLOGY 640 |
| 262, 313, 321, 325, 327, 331, 333, 463, 586 | A1, A2 (click theorem) | section 3.4 | POSTULATES |
| 305, 465, 555, 592, 623 | "A14", "rows A10 and 1a", "A10" (old register) | the experiment's name | EXPERIMENTS.md |
| 493, 500, 506 to 511, 520, 564 | Reviewer 3, Reviewer 2 | section 1.8 | no |
| 262, 451, 457, 481, 512, 658 | 4a, 4b, "rows 4a and 4b", "NATURE 4b's FAIL" | the names of section 1.7 | NATURE.md |
| 307, 451, 481, 485 | 2a, "row 2a", "rows 2a"; 481 "(1a, 2b, 9; 5a ...)", "(1c, 6, 7b, 8a, 8b, 13)", "(3, 4a, 4b, 5b, 7a, 8c, 11a, 11c)" | list the observables by name | NATURE.md |
| 339, 345, 351, 458, 499, 500; 361, 369, 373; 268; 391; 392; 428; 506 to 508; 501; 509 | "row 13", "NATURE row 12", "NATURE rows 11a", "J1 and NATURE row 8a", "row 12", "row 14", "row 10", "row 8b", "row 1c" | section 1.7 names (row 13 is light bending here but the light clock in THE_EXPERIMENTS) | NATURE.md |
| 506, 512 | "R2", "M1", "L-3" | the canonical names | no |
| 509 | "Five must work out ... before five is computed"; "section 8b" | "The moving light clock must work out"; 8b stays as a citation after its name ("the binding through the Inside, section 8b") | no |
| 289, 292, 357, 359, 361, 369, 380, 468, 548, 555, 584, 588, 597, 679, 681; 276 | series C, E, T, X, D, D3, I, K, G2, H, W; 587, 591 L1, L7 | section 1.6 | examples/events |
| 253, 391, 584, 597 | "the muon of J4", "J1", "the J2 window" | the covariant muon; the neutron lattice trigger; the phase window's readers | weak/, covariant/ |
| 597 | "the verdicts of D and H", "I7 run as the bound clock's redshift", "doppler-v1 and G deleted" | "the orbit and Bohr verdicts", name I7, "the Doppler key and the crossing gate" | no |
| 493, 494, 507, 509 | "verb G", "verbs G", "verb E" | section 1.5 | ALGEBRA |
| 224, 446, 509, 527, 585 | "the 48" | the cube group | as above |
| 255, 692 | "item 1b" (the click's Gram form) | the click's Gram form | no |
| 279, 305, 416, 458, 581, 586, 627, 631, 700 | "stage 1, 2, 3", "step 2", "step 5", "item 10", "item 11" used as names | name the stage or item | no |

### 4.2 docs/THE_EXPERIMENTS.md (branch `claude/new-boss-skills-file-4d1svd`)

The branch version already names the engine parts. What remains:

| Line(s) | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| 41, 42, 43 | "de Broglie's fringes (M1)", "The moving mass's energy (M2)", "The boxes (ii-a, ii-b)" | drop the parentheses; "The boxed clocks, sides 20 and 28" | ALGEBRA 9.22 |
| 47 | "as row 14" (twice) | "as at one third" | no |
| 66 to 73 | "#" column A1 to A6 | the names of section 1.2 (A1, A2 collide with the click theorem and EXPERIMENTS.md) | ALGEBRA, LAB_TOOLS |
| 31 to 50 | "#" column 1 to 18 | an ordinal is fine as a column, but "row N" must never be written for it | no |
| 1, 20, 22 | "twenty-four", "The seventeen", "part B" | "the measured and computed experiments"; quote ALGEBRA's retitled heading; "the placed experiments of LAB_TOOLS.md" | ALGEBRA, LAB_TOOLS |
| origin/main's version, lines 34 to 81 | F0 to F4 | replaced by the branch; merge the branch | no |

### 4.3 docs/TERMINOLOGY.md

| Line(s) | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| 200, 264, 537, 576 | `drive_b`, "form B" | the directional drive | code |
| 640 | "Lorentz, B" | the covariant readings | HIGHLIGHTS |
| 611 | "series G" | the Hubble series | no |
| 62 | "the 48" | the cube group | no |
| 192, 210, 221, 230, 240, 249, 260, 570 to 572 | "COUPLINGS.md rows 2 and 19", "row 20", ..., "row 29"; 210 "record 494, S3" | citations after a defined name; allowed, but "S3" should be named by its content | no |
| 61, 105, 207, 273, 363, 583 to 590 | "step 1", "step 2", "step 5", "step 6", "item 9", "item 13" | the engine step names of section 1.4 | ENGINE.md |

### 4.4 skills/

| File: line | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| workflow.md 730 to 739 | the plain-name rule that still allows codes in parentheses ("a row number such as 4a or R2, a line label such as L-3, a family letter such as M1") | rewrite as record 1924: no code anywhere, with the example "the travelling born profile, not F1" | every role's skill; AGENTS.md |
| paper-coordinator/SKILL.md 86 | "(A1)" | the one-Node-per-interval assumption | no |
| physics-rule-validation/SKILL.md 171 | "Reviewer 3's read" | the gate reviewer's read | no |
| simulation-runner/SKILL.md 28 | "series L6" | the Bell worlds at N = 1024 and 4096 | no |
| boss-orchestrator/SKILL.md 280; paper-coordinator/SKILL.md 48 | "item 8" | name the item | no |

---

## 5. Owner: Nature24, ENGINE.md and RUN_LIST.md

### 5.1 docs/ENGINE.md

| Line(s) | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| 273, 581, 590, 1066 to 1068 | `drive_b`, `drive-b-v1` | the directional drive | code |
| 261 | "the model owner's D1 of 2026-09-19" | the owner's push-width decision (record N) | orbit/README |
| 37, 192, 209, 263, 396, 398, 429, 461, 464, 495, 508, 582, 619, 653, 836, 1152, 1207 | "step 1" to "step 5" of BEAM_LAW section 3; "stage (vii) step 2/3/4" | the engine step names (section 1.4); "the one click" for stage (vii) step 4 | no |
| 323, 1006, 1014, 1023, 1312 | "the owner's item 9", "section 11 item 7", "section 13 item 7" | the item's subject first | no |
| 580, 612, 1301 | series T, K, S; 611 "L1" | section 1.6 | no |
| 1223 | "a row 10 run of docs/designs/fail_rows at w = 9" | "a single-opening run ... at the opening's width 9" | no |
| 1287 | D1, D2 | the +x and +y detectors | amplitude/ |
| 1315 | "the audit of record 567, F6, F8 and F14" | name the three findings | code comments that cite the same |

### 5.2 docs/designs/detector_law/RUN_LIST.md

| Line(s) | Current | Proposed | Consumers |
| --- | --- | --- | --- |
| 1, 16, 27 to 31 | "the fifteen", "THE LIST IS CLOSED AT FIFTEEN"; "The fifteen: two_slits, the pace fans, 4a, 4b, 4c, R2, M1, M2, the boxes (ii-a) and (ii-b), ..." | the canonical names; the list is now superseded by ALGEBRA 9.22 (8), so mark it HISTORY or re-point it | THE_EXPERIMENTS |
| 21 to 26 | "2a at the 128-period train, 2c's seven ... worlds, 10 (a) and 10 (b), 2b Mach-Zehnder", "Rows 2c and 10", "rows 2b" | names | no |
| 73 to 88 (the "Row" column) | "2a, the two slits", "(5a)", "4a, ...", "4b, ...", "4c, ...", "(R2)", "M1, ...", "M2, ...", "(ii-a), (ii-b)", "(v-m)", "1a, 1b, 1c, 1d, Bell's four settings", "9 and Malus's three settings", "as (v-m)", "A, A2, B" | the names alone | no |
| 73, 74, 75 | "section 15 L-3", "(L-6, GAMEBOARD ...)", "M1-8" | the declarations' subjects | DECLARATIONS.md |
| 34, 62 | "the engine's line B", "loads under line B" | "the block's grace for its emitted records" | BUILD.md |
| 55 | "(Builder 2)" | the reader builder | no |
| 64, 74, 85 | Reviewer 3 | the gate reviewer | no |
| 75, 84, 92, 94 | "e2", "e3", "e4" | "the light clock's exploratory run", "the receding index's exploratory run", "the muon's exploratory pair" | EXPLORATION.md |
| 46 | `--output artifacts/<row>/<world>` | `artifacts/<experiment>/<world>` | tools/run_inputs.py |

---

## 6. Outside the listed scope, seen on the way

- docs/designs/paper_verification/NEW_ENGINE_AUDIT.md 278 to 294 uses X1 to
  X17 (215 times) as a second code system over the paper's codes.
- docs/EXPERIMENTS.md headings use A1 to A13 and "A5s". This is the source of
  the "A2", "A10" and "A12" codes in the code; two headings share the code
  A10.
- NATURE.md's comparison rows (1a to 14) are the source of the paper's codes.
  Its tables need a name column if the rows are to be cited by name.
- docs/designs/drive_b/, `cut30/`, RUN_14.md, BUILD.md section 26's numbered
  items and DECLARATIONS.md section 15's `L-` and `M1-` items are cited from
  the code. The renames above need their headings to carry names.
- The commit subjects on emitter-click name builds by number, for example
  "(BUILD.md section 26 item 23)". Later commits should put the name first:
  most subjects already do, so only the citation habit needs to change.

## 7. Suggested order

1. The Boss rewrites HIGHLIGHTS 5.4 line 512 and skills/workflow.md 730 to 739
   to record 1924, and adopts the canonical names of sections 1.1 to 1.8
   (one table, in TERMINOLOGY.md).
2. The mathematician renames ALGEBRA 9.22 (8), LAB_TOOLS part B and the verb
   letters, and resolves the conflict over ii-a and ii-b.
3. Nature24 renames the eighteen's input files as they are written (only the
   light clock's and a few older worlds exist now), then `drive_b`, `D1`/`D2`, the family letters and the
   coupling file names. Each rename lands with its consumers, its migration
   note and regenerated world files.
4. The series letters and the test prefixes follow as mechanical renames.

---

## Appendix A. Code occurrences on `emitter-click` (file: lines)

#### The directional drive (form B, drive_b, drive-b-v1)

| Code | File: lines |
| --- | --- |
| drive_b | `examples/events/README.md`: 545,546,548,549,550,553; `examples/events/covariant/README.md`: 76,97; `examples/events/drive_b/README.md`: 9,21,26,28,53,70,79,97; `examples/events/drive_b/axis_b.json`: 1; `examples/events/drive_b/cube_b.json`: 1; `examples/events/drive_b/make_worlds.py`: 3,7,31,108,130; `examples/events/drive_b/plane_b.json`: 1; `examples/events/gate_set.json`: 3,130,133; `examples/events/optical/README.md`: 430,441,463; `examples/events/optical/body_b10_g0.json`: 1; `examples/events/optical/body_b10_g1.json`: 1; `examples/events/optical/body_b12_g0.json`: 1; `examples/events/optical/body_b12_g1.json`: 1; `examples/events/optical/body_b14_g0.json`: 1; `examples/events/optical/body_b14_g1.json`: 1; `examples/events/optical/body_b16_g0.json`: 1; `examples/events/optical/body_b16_g1.json`: 1; `examples/events/optical/body_b18_g0.json`: 1; `examples/events/optical/body_b18_g1.json`: 1; `examples/events/optical/body_control_b10.json`: 1; `examples/events/optical/body_control_b12.json`: 1; `examples/events/optical/body_control_b14.json`: 1; `examples/events/optical/body_control_b16.json`: 1; `examples/events/optical/body_control_b18.json`: 1; `examples/events/optical/make_worlds.py`: 426,497; `src/event_universe/core/integer.py`: 167; `src/event_universe/events/engine.py`: 227,239,256,260,688,690,711,874,875,876; `src/event_universe/events/measured.py`: 357,366,370,377,385,390,398; `src/event_universe/events/run.py`: 187,189; `src/event_universe/events/world.py`: 461,518,521,522,560,591,1589,1591,1699,1701,1768,1796,4096,4106,4163,4168,5688,5690,5691,5692,5693,5722,5734,5742,5745,5771; `tests/test_centred_step.py`: 37,42,74,96,97,248,249; `tests/test_drive_b.py`: 2,4,14,15,18,53,87,138,170,223,237,246,319,356,502,503,504,505,510; `tests/test_optical_body.py`: 3,13,17,36,40,41,84,126,127,132,180,181,263,265,270,280,281,282,283,314; `tests/test_record_trim.py`: 96; `tools/check.py`: 54,55; `tools/click_readings/README.md`: 40,87; `tools/click_readings/drive_b.py`: 2,5,6,31 |
| drive-b | `examples/events/README.md`: 543,546; `examples/events/covariant/README.md`: 77,97; `examples/events/drive_b/README.md`: 1,27; `examples/events/drive_b/axis_b.json`: 1; `examples/events/drive_b/axis_main.json`: 1; `examples/events/drive_b/cube_b.json`: 1; `examples/events/drive_b/cube_main.json`: 1; `examples/events/drive_b/expectations.json`: 2,3,288,394,500; `examples/events/drive_b/make_worlds.py`: 1,68,88,128,275; `examples/events/drive_b/plane_b.json`: 1; `examples/events/drive_b/plane_main.json`: 1; `examples/events/gate_set.json`: 133; `examples/events/optical/README.md`: 430; `examples/events/optical/body_b10_g0.json`: 1; `examples/events/optical/body_b10_g1.json`: 1; `examples/events/optical/body_b12_g0.json`: 1; `examples/events/optical/body_b12_g1.json`: 1; `examples/events/optical/body_b14_g0.json`: 1; `examples/events/optical/body_b14_g1.json`: 1; `examples/events/optical/body_b16_g0.json`: 1; `examples/events/optical/body_b16_g1.json`: 1; `examples/events/optical/body_b18_g0.json`: 1; `examples/events/optical/body_b18_g1.json`: 1; `examples/events/optical/body_control_b10.json`: 1; `examples/events/optical/body_control_b12.json`: 1; `examples/events/optical/body_control_b14.json`: 1; `examples/events/optical/body_control_b16.json`: 1; `examples/events/optical/body_control_b18.json`: 1; `examples/events/optical/body_expectations.json`: 5,458,520,582,644,706,768,830,892,954,1016,1078,1140,1202,1264,1326; `examples/events/optical/make_worlds.py`: 487,555; `src/event_universe/core/integer.py`: 167; `src/event_universe/events/engine.py`: 239,260,875,900,907; `src/event_universe/events/measured.py`: 359; `src/event_universe/events/run.py`: 187; `src/event_universe/events/world.py`: 459,517,527,560,1589,1767,4107,4169,5688,5692; `tests/test_drive_b.py`: 1,116,507,515; `tests/test_optical_body.py`: 3; `tools/check.py`: 52; `tools/click_readings/README.md`: 40,87; `tools/click_readings/drive_b.py`: 1,2,8,32,248 |
| form B | `examples/events/README.md`: 265,267,273,364,547; `examples/events/atoms/README.md`: 1,9,14,34,67; `examples/events/atoms/make_worlds.py`: 1,8,71,118,132,267; `examples/events/covariant/README.md`: 77,95,96; `examples/events/drive_b/README.md`: 7,10; `examples/events/drive_b/expectations.json`: 276; `examples/events/drive_b/make_worlds.py`: 2,4,283; `examples/events/optical/make_worlds.py`: 424; `examples/events/orbit/README.md`: 155,218,220,239; `examples/events/orbit_lamp/README.md`: 74,204,206; `examples/events/orbit_lamp/make_worlds.py`: 25,218,308,513; `src/event_universe/core/integer.py`: 169; `src/event_universe/events/measured.py`: 359,365,380; `src/event_universe/events/world.py`: 520,4168,5736,5742; `tests/test_drive_b.py`: 1,3; `tests/test_optical_body.py`: 2,3 |

#### Mach-Zehnder detectors D1 and D2 (and the owner's decision D1)

| Code | File: lines |
| --- | --- |
| D2 | `examples/events/README.md`: 587; `examples/events/amplitude/README.md`: 43,45,46,51,52,53,54,55,56,57,58,59,60,74,75,79,120,126,135,144,145,148; `examples/events/amplitude/ev_169.json`: 1; `examples/events/amplitude/ev_29.json`: 1; `examples/events/amplitude/expectations.json`: 8,12,124,128,134,138,145,149,177,181,190,196,200,206,210,217,221,228,233,240,245,4072,4150,4164,4196,4210,4239,4253,4267,4289,4305,4331; `examples/events/amplitude/make_worlds.py`: 26,29,32,36,37,38,39,40,41,42,43,44,45,213,215,216,437,482,483,484,485,486,488,489,491,493,494,497,498,501,502,1913,2020,3242,3254,3260,3279,3285,3317; `examples/events/amplitude/mz_345.json`: 1; `examples/events/amplitude/mz_345_n128.json`: 1; `examples/events/amplitude/mz_345_n32.json`: 1; `examples/events/amplitude/mz_balanced.json`: 1; `examples/events/amplitude/mz_equal.json`: 1; `examples/events/amplitude/mz_half.json`: 1; `examples/events/amplitude/mz_quarter.json`: 1; `examples/events/amplitude/mz_unequal_f0.json`: 1; `examples/events/amplitude/mz_unequal_f16.json`: 1; `examples/events/amplitude/mz_unequal_f8.json`: 1; `tests/test_amplitude_layer.py`: 13,16,27,35,247,249,271,317; `tests/test_amplitude_mz_345_n.py`: 16,21,26,38,64,100,121,143,146,155,158,258; `tests/test_nature_beam_push.py`: 133 |
| D1 | `examples/events/README.md`: 587; `examples/events/amplitude/README.md`: 43,45,46,51,52,53,54,55,56,57,58,59,60,73,79,120,126,144,148; `examples/events/amplitude/ev_169.json`: 1; `examples/events/amplitude/ev_29.json`: 1; `examples/events/amplitude/expectations.json`: 7,11,100,123,127,133,137,144,148,176,180,190,195,199,205,209,216,220,227,232,239,244,4071,4140,4163,4186,4209,4252,4266,4288,4304,4331; `examples/events/amplitude/make_worlds.py`: 27,28,31,36,37,38,39,40,41,42,43,44,45,212,215,436,482,483,484,485,486,488,489,491,493,494,497,498,501,502,1999,2020,3254,3260,3279,3285,3317; `examples/events/amplitude/mz_345.json`: 1; `examples/events/amplitude/mz_345_n128.json`: 1; `examples/events/amplitude/mz_345_n32.json`: 1; `examples/events/amplitude/mz_balanced.json`: 1; `examples/events/amplitude/mz_equal.json`: 1; `examples/events/amplitude/mz_half.json`: 1; `examples/events/amplitude/mz_quarter.json`: 1; `examples/events/amplitude/mz_unequal_f0.json`: 1; `examples/events/amplitude/mz_unequal_f16.json`: 1; `examples/events/amplitude/mz_unequal_f8.json`: 1; `examples/events/orbit/README.md`: 6,85,88,279,315; `examples/events/orbit/make_worlds.py`: 42; `src/event_universe/events/engine.py`: 786; `src/event_universe/events/measured.py`: 691; `src/event_universe/events/nature_beam.py`: 5339; `src/event_universe/events/world.py`: 30; `tests/test_amplitude_layer.py`: 13,16,28,35,232,247,249,271,273,317,475; `tests/test_amplitude_mz_345_n.py`: 16,64,142,144,145,157; `tests/test_nature_beam_push.py`: 111; `tests/test_push_width.py`: 1 |

#### Experiment row codes

| Code | File: lines |
| --- | --- |
| M1 | `examples/events/covariant/README.md`: 57,66; `examples/events/covariant/expectations.json`: 142; `examples/events/covariant/make_worlds.py`: 11,322; `examples/events/detector_law/README.md`: 48; `examples/events/detector_law/make_worlds.py`: 55,642,672,870; `examples/events/massive_record/make_worlds.py`: 216; `examples/events/massive_record/read_runs.py`: 22; `examples/events/optical/README.md`: 127,202,277,351; `examples/events/optical/expectations.json`: 180,262; `examples/events/optical/make_worlds.py`: 282,841,848,901,911; `src/event_universe/events/engine.py`: 230,747,759,869; `src/event_universe/events/world.py`: 508; `tests/test_optical.py`: 69,98,741 |
| M2 | `examples/events/amplitude/pages/bell.html`: 101; `examples/events/covariant/README.md`: 128,157,170,180,186; `examples/events/covariant/expectations.json`: 143,145,226; `examples/events/covariant/make_worlds.py`: 27,50,111,325,339; `examples/events/detector_law/README.md`: 50; `examples/events/detector_law/make_worlds.py`: 75,870,881; `examples/events/massive_record/read_runs.py`: 22 |
| 4b | `examples/events/c_measured/README.md`: 25; `examples/events/covariant/make_worlds.py`: 50,69; `examples/events/detector_law/README.md`: 48; `examples/events/detector_law/make_worlds.py`: 65,660,753; `examples/events/hubble_stars/README.md`: 851; `examples/events/massive_record/README.md`: 79; `examples/events/massive_record/make_worlds.py`: 71,84,620,628; `examples/events/massive_record/read_runs.py`: 22; `examples/events/moving_detector/README.md`: 119 |
| R2 | `examples/events/detector_law/README.md`: 48; `examples/events/detector_law/make_worlds.py`: 51,66,666,787; `examples/events/massive_record/read_runs.py`: 22; `src/event_universe/events/detector_law.py`: 326; `src/event_universe/events/world.py`: 4667; `tests/test_massive_record.py`: 1529 |
| v-m | `examples/events/massive_record/README.md`: 43,56; `examples/events/massive_record/make_worlds.py`: 42,81,458,500; `examples/events/massive_record/pins.py`: 22,298; `examples/events/massive_record/read_runs.py`: 29,512; `tests/test_massive_record.py`: 977 |
| 4a | `examples/events/c_measured/README.md`: 25; `examples/events/covariant/make_worlds.py`: 17; `examples/events/detector_law/make_worlds.py`: 182; `examples/events/massive_record/expectations.json`: 241; `examples/events/massive_record/make_worlds.py`: 299; `examples/events/massive_record/pins.py`: 239; `examples/events/massive_record/read_runs.py`: 61,448 |
| 1b | `examples/events/coupling/1b_m1.json`: 3; `examples/events/coupling/1b_m16.json`: 3; `examples/events/coupling/1b_m4.json`: 3; `examples/events/coupling/README.md`: 13,256; `tools/click_readings/coupling.py`: 55 |
| 1a | `examples/events/coupling/1a_m1.json`: 3; `examples/events/coupling/1a_m16.json`: 3; `examples/events/coupling/1a_m4.json`: 3; `src/event_universe/events/detector_law.py`: 135; `tools/click_readings/README.md`: 24; `tools/click_readings/detector_law_bell.py`: 4 |
| 2a | `examples/events/amplitude/README.md`: 639; `examples/events/detector_law/README.md`: 46; `examples/events/detector_law/make_worlds.py`: 392; `examples/events/massive_record/read_runs.py`: 22 |
| 1d | `src/event_universe/events/detector_law.py`: 135; `tools/click_readings/README.md`: 24; `tools/click_readings/detector_law_bell.py`: 4 |
| 2c | `examples/events/detector_law/README.md`: 46; `examples/events/detector_law/make_worlds.py`: 27; `examples/events/massive_record/read_runs.py`: 22 |
| 5b | `examples/events/c_measured/README.md`: 25; `examples/events/optical/README.md`: 458 |
| 5a | `examples/events/detector_law/README.md`: 46; `examples/events/detector_law/make_worlds.py`: 451 |
| 2b | `examples/events/detector_law/README.md`: 47; `examples/events/detector_law/make_worlds.py`: 28 |
| ii-a | `examples/events/massive_record/README.md`: 52; `examples/events/massive_record/make_worlds.py`: 26 |
| ii-b | `examples/events/massive_record/README.md`: 52; `examples/events/massive_record/make_worlds.py`: 26 |

#### Weak and muon sub-series J1 to J4

| Code | File: lines |
| --- | --- |
| J1 | `examples/events/README.md`: 506; `examples/events/weak/README.md`: 11,102,118,146,179,182,186,212,273,308,338,381,398; `examples/events/weak/expectations.json`: 563,1617,2167; `examples/events/weak/make_worlds.py`: 4,11,45,100,145,156,303,345,590; `tests/test_w_world.py`: 14; `tests/test_weak_readings.py`: 25,71,80,426; `tools/check.py`: 74; `tools/click_readings/weak.py`: 4,20,65,446,648 |
| J3 | `examples/events/README.md`: 512; `examples/events/weak/README.md`: 11,102,137,146,179,182,212; `examples/events/weak/make_worlds.py`: 4,11,67,100,145,163,303,590; `tests/test_host_batches.py`: 9,27,65,98; `tests/test_w_world.py`: 14; `tests/test_weak_readings.py`: 71; `tools/check.py`: 74; `tools/click_readings/weak.py`: 4,20,71,446,648 |
| J2 | `examples/events/README.md`: 490; `examples/events/gate_set.json`: 3; `examples/events/weak/README.md`: 10,26,275; `examples/events/weak/make_worlds.py`: 3,11,24,135,214,276,594; `src/event_universe/events/world.py`: 203; `tests/support/hand_worlds.py`: 23,49; `tests/test_weak_readings.py`: 9,58; `tools/check.py`: 74; `tools/click_readings/weak.py`: 3,14,61,646 |
| J4 | `examples/events/README.md`: 532; `examples/events/covariant/README.md`: 56,121,138,153,203; `examples/events/covariant/make_worlds.py`: 17,104,215; `tests/test_covariant_readings.py`: 76; `tools/click_readings/covariant.py`: 12,225 |

#### Register codes of docs/EXPERIMENTS.md (A2, A9, A10, A12, ...)

| Code | File: lines |
| --- | --- |
| A2 | `examples/events/README.md`: 128,135,150,594; `examples/events/amplitude/README.md`: 299,345,359; `examples/events/amplitude/make_worlds.py`: 107,274,838,1160,1193; `examples/events/bell/README.md`: 1,5,129,150,152,167,219,220; `examples/events/bell/expectations.json`: 3; `examples/events/bell/make_chooser_worlds.py`: 2,5,76,81; `examples/events/bell/make_worlds.py`: 1,4; `tests/test_amplitude_pair.py`: 37; `tests/test_nature_beam_worlds.py`: 3,26; `tools/click_readings/README.md`: 22,23,67; `tools/click_readings/bell.py`: 1,8; `tools/click_readings/bell_choosers.py`: 2,456 |
| A10 | `examples/events/README.md`: 378,386; `examples/events/heisenberg/README.md`: 1,6; `examples/events/heisenberg/make_worlds.py`: 1,4; `examples/events/lensing/README.md`: 9; `tools/click_readings/README.md`: 29,73; `tools/click_readings/heisenberg.py`: 1,23 |
| A12 | `examples/events/amplitude/README.md`: 507,515,561,591; `examples/events/amplitude/make_worlds.py`: 183,329,1730,3119,3141; `tests/test_amplitude_malus.py`: 1 |
| A9 | `examples/events/amplitude/pages/bell.html`: 94 |
| A1 | `tests/test_nature_beam_worlds.py`: 205 |

#### Amplitude series L1 to L7

| Code | File: lines |
| --- | --- |
| L3 | `examples/events/README.md`: 594; `examples/events/amplitude/README.md`: 36,297,315; `examples/events/amplitude/make_worlds.py`: 105,127,274; `examples/events/amplitude/pages/bell.html`: 72,137; `examples/events/amplitude/pages/build_pages.py`: 1230,1261; `examples/events/detector_law/make_worlds.py`: 35,478,480,483; `tests/test_amplitude_pair.py`: 4; `tests/test_hand.py`: 92 |
| L1 | `examples/events/README.md`: 584; `examples/events/amplitude/README.md`: 23,92,129; `examples/events/amplitude/make_worlds.py`: 8,204,1918,3231; `examples/events/heisenberg/README.md`: 49,50; `tests/test_algebra_visualizer.py`: 7; `tests/test_amplitude_mz_345_n.py`: 6,25 |
| L2 | `examples/events/README.md`: 590; `examples/events/amplitude/README.md`: 164,196; `examples/events/amplitude/make_worlds.py`: 58,82,259,551,643; `examples/events/amplitude/pages/build_pages.py`: 1135,1148,1178; `examples/events/heisenberg/README.md`: 49,50 |
| L6 | `examples/events/README.md`: 597; `examples/events/amplitude/README.md`: 342,347,359; `examples/events/amplitude/make_worlds.py`: 155,294,303,2088; `examples/events/amplitude/pages/bell.html`: 138; `examples/events/amplitude/pages/build_pages.py`: 1262; `tests/test_amplitude_bell_24_4.py`: 7; `tests/test_amplitude_gate.py`: 4 |
| L4 | `examples/events/README.md`: 596; `examples/events/amplitude/README.md`: 317; `examples/events/amplitude/make_worlds.py`: 122,127,274; `tests/test_amplitude_pair.py`: 4 |
| L5 | `examples/events/README.md`: 596; `examples/events/amplitude/README.md`: 325,340; `examples/events/amplitude/make_worlds.py`: 138,294; `tests/test_amplitude_gate.py`: 4 |
| L7 | `examples/events/amplitude/README.md`: 488,498; `examples/events/amplitude/make_worlds.py`: 172,1236; `tests/test_amplitude_cone.py`: 1,2 |

#### Reviewer and builder numbers

| Code | File: lines |
| --- | --- |
| Reviewer 3 | `examples/events/detector_law/README.md`: 46,48; `examples/events/detector_law/make_worlds.py`: 49,188,195,354,494,578; `examples/events/massive_record/make_worlds.py`: 622,626; `src/event_universe/diagnostics/massive_record_margin.py`: 2; `src/event_universe/events/detector_law.py`: 649,1537; `src/event_universe/events/world.py`: 781,887,926,1023,2234,5643; `tests/test_massive_record.py`: 272,665,1052,1158,1293,1591; `tests/test_preflight_worlds.py`: 70; `tools/preflight_worlds.py`: 13,91,114 |
| Builder 2 | `examples/events/detector_law/make_worlds.py`: 330; `examples/events/massive_record/README.md`: 75 |

#### Finding codes F1 to F16

| Code | File: lines |
| --- | --- |
| F1 | `examples/events/clock_word/expectations.json`: 117; `examples/events/clock_word/make_worlds.py`: 253,258; `tests/test_clock_word.py`: 177; `tests/test_nature_beam_collision.py`: 26; `tests/test_nature_beam_detector.py`: 893 |
| F8 | `examples/events/weak/README.md`: 159; `tests/test_weak_readings.py`: 54,250; `tools/click_readings/weak.py`: 19 |
| F9 | `examples/events/weak/README.md`: 161; `tests/test_weak_readings.py`: 56,271; `tools/click_readings/weak.py`: 107 |
| F6 | `examples/events/covariant/README.md`: 25; `tests/test_covariant_readings.py`: 630; `tests/test_nature_beam_push.py`: 60 |
| F5 | `examples/events/covariant/README.md`: 29; `tests/test_covariant_readings.py`: 627 |
| F7 | `examples/events/covariant/README.md`: 29; `tests/test_covariant_readings.py`: 627 |
| F13 | `tests/test_quarks_expectations.py`: 189; `tools/click_readings/quarks.py`: 278 |
| F3 | `tests/test_coupling_readings.py`: 179; `tools/click_readings/coupling.py`: 851 |
| F4 | `tests/test_coupling_readings.py`: 179; `tools/click_readings/coupling.py`: 997 |
| F12 | `tests/test_nucleus_readings.py`: 129; `tools/click_readings/nucleus.py`: 375 |
| F16 | `tools/click_readings/lensing.py`: 53 |
| F10 | `tools/click_readings/bohr.py`: 428 |

#### Engine and build line codes

| Code | File: lines |
| --- | --- |
| line 2 | `examples/events/amplitude/README.md`: 585,611; `examples/events/massive_record/read_runs.py`: 28,310; `examples/events/optical/README.md`: 48,49; `src/event_universe/events/detector_law.py`: 1537; `tests/test_massive_record.py`: 272; `tests/test_nature_beam_label.py`: 64 |
| line 1 | `examples/events/orbit_lamp/run_flow.out`: 17,41; `examples/events/redshift/README.md`: 186,188; `tests/test_orbit_lamp_readings.py`: 369 |
| line B | `src/event_universe/events/detector_law.py`: 203; `src/event_universe/events/world.py`: 920,1268,5643 |
| line 7 | `src/event_universe/events/detector_law.py`: 318,475 |
| line 0 | `examples/events/binding/README.md`: 106; `tests/test_w_world.py`: 47 |
| Line 7 | `tests/test_massive_record.py`: 1440,1529 |
| line 8 | `examples/events/detector_law/README.md`: 47 |
| line 6 | `examples/events/detector_law/make_worlds.py`: 199 |
| line 3 | `tests/test_massive_record.py`: 152 |
| lines 2 | `tests/test_nature_beam_detector.py`: 125 |

#### Declaration item codes (DECLARATIONS.md section 15)

| Code | File: lines |
| --- | --- |
| M1-6 | `examples/events/detector_law/make_worlds.py`: 56,69,281,351,654,655,713,870; `src/event_universe/diagnostics/massive_record_margin.py`: 449; `src/event_universe/events/world.py`: 922,3471,3477,3485; `tests/test_massive_record.py`: 531 |
| M1-10 | `examples/events/detector_law/README.md`: 48; `examples/events/detector_law/make_worlds.py`: 68,217,653,739,880; `examples/events/massive_record/make_worlds.py`: 192; `src/event_universe/events/world.py`: 446,5601,5641,5647; `tests/test_massive_record.py`: 1060,1399 |
| L-1 | `examples/events/detector_law/README.md`: 26,46; `examples/events/detector_law/make_worlds.py`: 16,25,162,280,396; `src/event_universe/events/world.py`: 3501; `tests/test_massive_record.py`: 1631 |
| M1-1 | `examples/events/detector_law/README.md`: 48; `examples/events/detector_law/make_worlds.py`: 56,64,651,753,787; `examples/events/massive_record/make_worlds.py`: 600; `tests/test_massive_record.py`: 1399 |
| M1-4 | `examples/events/detector_law/make_worlds.py`: 65,698,787,794; `src/event_universe/events/detector_law.py`: 318; `src/event_universe/events/world.py`: 5284; `tests/test_massive_record.py`: 1399 |
| L-3 | `examples/events/detector_law/README.md`: 46; `examples/events/detector_law/make_worlds.py`: 17,163,381,392,402 |
| L-6 | `examples/events/detector_law/README.md`: 46; `examples/events/detector_law/make_worlds.py`: 16,21,163,421,451 |
| L-4 | `examples/events/detector_law/README.md`: 46; `examples/events/detector_law/make_worlds.py`: 28 |
| L-5 | `examples/events/detector_law/README.md`: 46; `examples/events/detector_law/make_worlds.py`: 28 |
| M1-3 | `examples/events/detector_law/make_worlds.py`: 65; `tests/test_massive_record.py`: 1399 |
| M1-2 | `examples/events/detector_law/make_worlds.py`: 64 |
| M1-5 | `examples/events/detector_law/make_worlds.py`: 753 |
| M1-7 | `examples/events/detector_law/make_worlds.py`: 793 |
| M1-11 | `examples/events/massive_record/README.md`: 21 |
| M1-8 | `examples/events/massive_record/make_worlds.py`: 551 |

#### Row numbers used as names

| Code | File: lines |
| --- | --- |
| row 4 | `examples/events/amplitude/README.md`: 557,559,605,614; `examples/events/amplitude/expectations.json`: 4061,4330; `examples/events/amplitude/make_worlds.py`: 350,3144,3159,3316; `tests/test_amplitude_malus.py`: 9 |
| row 13 | `examples/events/detector_law/make_worlds.py`: 831; `examples/events/lamp_shell/README.md`: 1,7,67,112; `examples/events/lamp_shell/expectations.json`: 10422; `examples/events/lamp_shell/make_worlds.py`: 1,229 |
| row 58 | `examples/events/orbit/README.md`: 152,191,238; `examples/events/orbit/make_worlds.py`: 85 |
| row 8a | `examples/events/weak/expectations.json`: 563,1617,2167; `tests/test_weak_readings.py`: 425 |
| rows 1a | `src/event_universe/events/detector_law.py`: 135; `tools/click_readings/README.md`: 24; `tools/click_readings/detector_law_bell.py`: 4 |
| NATURE row 12 | `examples/events/redshift/README.md`: 30; `examples/events/shell_clock/README.md`: 9; `examples/events/shell_clock/make_worlds.py`: 10 |
| row 2a | `examples/events/amplitude/README.md`: 639; `examples/events/detector_law/README.md`: 46; `examples/events/detector_law/make_worlds.py`: 392 |
| row 4a | `examples/events/massive_record/expectations.json`: 241; `examples/events/massive_record/pins.py`: 239; `examples/events/massive_record/read_runs.py`: 448 |
| rows 0 | `tests/test_massive_record.py`: 741; `tests/test_nature_beam_detector.py`: 152,950 |
| row 10 | `src/event_universe/trimmed_record.py`: 9; `tests/test_record_trim.py`: 7 |
| row 5a | `examples/events/detector_law/README.md`: 46; `examples/events/detector_law/make_worlds.py`: 451 |
| NATURE row 4b | `examples/events/covariant/make_worlds.py`: 50; `examples/events/moving_detector/README.md`: 119 |
| rows 3 | `examples/events/hubble_stars/README.md`: 851; `tests/test_amplitude_layer.py`: 43 |
| NATURE row 6 | `examples/events/atoms/README.md`: 81,98 |
| row 9 | `tools/click_readings/README.md`: 24; `tools/click_readings/detector_law_bell.py`: 5 |
| row 11 | `src/event_universe/events/nature_beam.py`: 743 |
| row 0 | `src/event_universe/events/nature_beam.py`: 3117 |
| Row 58 | `examples/events/orbit/README.md`: 211 |
| rows 10 | `examples/events/binding/README.md`: 98 |
| rows 7a | `examples/events/binding/README.md`: 140 |
| rows 2c | `examples/events/detector_law/README.md`: 46 |
| row 2b | `examples/events/detector_law/README.md`: 47 |
| Rows 2c | `examples/events/detector_law/make_worlds.py`: 27 |
| Row 4b | `examples/events/detector_law/make_worlds.py`: 753 |
| NATURE row 4a | `examples/events/covariant/make_worlds.py`: 17 |
| NATURE.md rows 4a | `examples/events/c_measured/README.md`: 25 |
| rows 2a | `examples/events/massive_record/read_runs.py`: 22 |
| NATURE row 8a | `examples/events/weak/README.md`: 375 |
| rows 8a | `examples/events/weak/README.md`: 405 |
| rows 2 | `tests/test_nature_beam_body.py`: 153 |
| row 12 | `tests/test_clock_word.py`: 53 |
| Row 13 | `tests/test_flow_link.py`: 176 |
| row 64 | `tests/test_w_world.py`: 30 |
| row 2 | `tests/test_nature_beam_detector.py`: 950 |

#### Side A / Side B, Lorentz A / B, route C

| Code | File: lines |
| --- | --- |
| Side A | `examples/events/README.md`: 420,423; `examples/events/newton_side/README.md`: 1,3; `examples/events/newton_side/make_worlds.py`: 1; `tests/test_newton_side_readings.py`: 1; `tools/check.py`: 39; `tools/newton_side_readings.py`: 1 |
| Side B | `examples/events/README.md`: 447; `examples/events/orbit_lamp/make_worlds.py`: 232,245,361,470,690; `tests/test_flow_link.py`: 187 |

#### Verb letters

| Code | File: lines |
| --- | --- |
| verb G | `src/event_universe/events/detector_law.py`: 15,51,1119,1658 |
| verb D | `src/event_universe/events/detector_law.py`: 138,962 |
| verb T | `src/event_universe/events/detector_law.py`: 625; `tools/algebra_visualizer/panels.py`: 1004 |
| verb B | `src/event_universe/events/detector_law.py`: 696,1243 |

#### Test letter references

| Code | File: lines |
| --- | --- |
| test (f) | `tests/test_contact.py`: 21,24; `tests/test_nucleus_readings.py`: 7 |
| test (z) | `tests/test_massive_record.py`: 326,1296 |
| test (m) | `examples/events/optical/README.md`: 421 |
| test (p) | `tests/test_massive_record.py`: 1263 |
| test (a) | `tests/test_columns.py`: 45 |
| tests (a) | `tests/test_hand.py`: 78 |
| test (n) | `tests/test_optical.py`: 767 |
| test (k) | `tests/test_nature_beam_detector.py`: 394 |
| test (i) | `tests/test_nature_beam_detector.py`: 902 |

#### "the 48" for the cube group

| Code | File: lines |
| --- | --- |
| the 48 | `examples/events/c_measured/README.md`: 119; `examples/events/flow_link/expectations.json`: 224,450,580,710,968,1226; `examples/events/flow_link/make_worlds.py`: 252; `examples/events/massive_record/README.md`: 52; `examples/events/quarks/make_worlds.py`: 29; `src/event_universe/events/nature_beam.py`: 861,887; `src/event_universe/events/world.py`: 674; `tests/test_board_properties.py`: 7,186; `tests/test_hand.py`: 77; `tests/test_nature_beam_collision.py`: 13; `tests/test_nature_beam_label.py`: 20; `tests/test_nature_beam_readings.py`: 23; `tools/algebra_visualizer/panels.py`: 950 |

## Appendix B. Series letters on `emitter-click` (file: lines)

| Series | File: lines |
| --- | --- |
| series K | `examples/events/README.md`: 429,440; `examples/events/flow_link/README.md`: 60,75,134,175; `examples/events/flow_link/make_worlds.py`: 9,13,16,23,60; `examples/events/gate_set.json`: 144; `examples/events/lamp_shell/README.md`: 24; `examples/events/lamp_shell/make_worlds.py`: 7; `examples/events/lensing/README.md`: 8; `examples/events/lensing/make_worlds.py`: 1; `examples/events/newton_side/README.md`: 15,37; `examples/events/newton_side/make_worlds.py`: 16,32,39,68; `examples/events/optical/README.md`: 8,9,13,77,130,358; `examples/events/optical/make_worlds.py`: 4,6,12,41,43,83,106,116,268,478,592; `tests/test_flow_link.py`: 28; `tests/test_lensing_readings.py`: 1; `tests/test_meeting.py`: 14,116; `tools/click_readings/lensing.py`: 1,863; `tools/newton_side_readings.py`: 125 |
| series E | `examples/events/README.md`: 176,196,198,397; `examples/events/c_measured/README.md`: 44; `examples/events/c_measured/make_world.py`: 12,90; `examples/events/clock_word/make_worlds.py`: 28; `examples/events/hubble/README.md`: 100,293; `examples/events/hubble/make_worlds.py`: 72; `examples/events/hubble_stars/README.md`: 116; `examples/events/hubble_stars/make_worlds.py`: 72; `examples/events/lensing/README.md`: 50,68,135,140; `examples/events/lensing/make_worlds.py`: 16,26,86,115; `examples/events/newton_side/README.md`: 36; `examples/events/newton_side/make_worlds.py`: 62; `examples/events/redshift/README.md`: 1; `examples/events/redshift/make_worlds.py`: 1; `examples/events/shell_clock/README.md`: 48,59,113; `examples/events/shell_clock/expectations.json`: 270; `examples/events/shell_clock/make_worlds.py`: 36,106,177,348; `tests/test_lensing_readings.py`: 28; `tests/test_redshift_readings.py`: 1; `tests/test_shell_clock.py`: 14,125; `tools/click_readings/lensing.py`: 51,797; `tools/click_readings/redshift.py`: 1 |
| series T | `examples/events/README.md`: 190,195,197,200; `examples/events/clock_word/make_worlds.py`: 1; `examples/events/lamp_shell/README.md`: 54; `examples/events/lamp_shell/make_worlds.py`: 28; `examples/events/lamp_shell/read_lamps.py`: 13; `examples/events/redshift/README.md`: 30; `examples/events/shell_clock/README.md`: 8,38,48,49,54,55,61,65,79,113,170; `examples/events/shell_clock/expectations.json`: 267,270; `examples/events/shell_clock/make_worlds.py`: 9,24,31,32,38,44,89,102,189,324,348; `tests/test_clock_age.py`: 30; `tests/test_clock_word.py`: 53,133; `tests/test_shell_clock.py`: 36; `tools/click_readings/clock_word.py`: 1,29; `tools/click_readings/shell_clock.py`: 13,40 |
| series D | `examples/events/README.md`: 332,373; `examples/events/orbit/README.md`: 1,153; `examples/events/orbit/make_worlds.py`: 1,86,101; `examples/events/orbit_lamp/README.md`: 11,60,62,72,76,100,210,223,233,290; `examples/events/orbit_lamp/expectations.json`: 4,7,8; `examples/events/orbit_lamp/expectations_flow.json`: 4,7,8; `examples/events/orbit_lamp/make_worlds.py`: 1,10,13,23,30,98,190,217,274,318,509,533; `tests/test_orbit_lamp_readings.py`: 105; `tools/click_readings/orbit.py`: 1; `tools/click_readings/orbit_lamp.py`: 1 |
| series I | `examples/events/README.md`: 298,316,513; `examples/events/atoms/make_worlds.py`: 5,16; `examples/events/binding/README.md`: 44,61,111; `examples/events/binding/make_worlds.py`: 4,12,20,22,72; `examples/events/nucleus/make_worlds.py`: 1; `examples/events/quarks/README.md`: 14,33; `examples/events/quarks/make_worlds.py`: 13,20; `examples/events/weak/README.md`: 137; `examples/events/weak/make_worlds.py`: 67,77,79,145,163; `tests/test_nature_beam_flight.py`: 48,404; `tests/test_w_world.py`: 21; `tools/click_readings/nucleus.py`: 1; `tools/click_readings/quarks.py`: 39 |
| series G | `examples/events/README.md`: 213; `examples/events/hubble/README.md`: 7; `examples/events/hubble/make_worlds.py`: 1,4; `examples/events/hubble_stars/README.md`: 23,151,159,164,237,290,420,782; `examples/events/hubble_stars/expectations.json`: 862; `examples/events/hubble_stars/make_worlds.py`: 589; `examples/events/hubble_stars/record/expectations.json`: 863; `tools/click_readings/hubble.py`: 1; `tools/click_readings/hubble_stars.py`: 28,33,57,71,111,293,296 |
| series C | `examples/events/README.md`: 157; `examples/events/coupling/README.md`: 1; `examples/events/coupling/make_worlds.py`: 1; `examples/events/hubble/README.md`: 73; `examples/events/hubble/make_worlds.py`: 49; `examples/events/hubble_stars/README.md`: 88; `examples/events/orbit/README.md`: 53,59; `examples/events/orbit/make_worlds.py`: 25,27,83; `examples/events/orbit_lamp/README.md`: 8,45; `examples/events/orbit_lamp/expectations_flow.json`: 19; `examples/events/orbit_lamp/make_worlds.py`: 252,582; `examples/events/redshift/README.md`: 50,94; `examples/events/redshift/make_worlds.py`: 33; `tools/click_readings/coupling.py`: 1 |
| series H | `examples/events/README.md`: 241,265,267; `examples/events/atoms/README.md`: 3,4,10,12,15,34; `examples/events/atoms/make_worlds.py`: 4,6,11,14,57,132,269; `examples/events/bohr/make_worlds.py`: 1; `tools/click_readings/bohr.py`: 1 |
| series L | `examples/events/README.md`: 579,638; `examples/events/amplitude/README.md`: 3; `examples/events/amplitude/make_worlds.py`: 1; `examples/events/massive_rows/README.md`: 21,138; `examples/events/massive_rows/expectations.json`: 53; `examples/events/massive_rows/make_worlds.py`: 5; `tests/test_amplitude_bell_24_4.py`: 5; `tests/test_amplitude_gram.py`: 14; `tests/test_amplitude_layer.py`: 6; `tests/test_amplitude_malus.py`: 4; `tests/test_amplitude_mz_345_n.py`: 4; `tests/test_amplitude_split.py`: 5 |
| series G2 | `examples/events/README.md`: 457,535; `examples/events/covariant/README.md`: 113; `examples/events/covariant/make_worlds.py`: 51; `examples/events/entities/make_definitions.py`: 131; `examples/events/hubble_stars/README.md`: 802; `examples/events/hubble_stars/make_worlds.py`: 1; `examples/events/moving_detector/make_worlds.py`: 12; `tests/test_hubble_stars_readings.py`: 1,268; `tests/test_step_drive.py`: 4; `tools/click_readings/hubble_stars.py`: 1,966,978 |
| series S | `examples/events/README.md`: 528; `examples/events/covariant/README.md`: 3; `examples/events/covariant/make_worlds.py`: 1; `examples/events/entities/make_definitions.py`: 45; `examples/events/moving_detector/make_worlds.py`: 10; `tools/click_readings/coupling.py`: 1021; `tools/click_readings/covariant.py`: 1,248,429 |
| series X | `examples/events/README.md`: 190,195,545; `examples/events/covariant/README.md`: 78,98; `examples/events/drive_b/README.md`: 3; `examples/events/shell_clock/make_worlds.py`: 1; `tools/click_readings/shell_clock.py`: 1 |
| series D3 | `examples/events/README.md`: 345,348; `examples/events/orbit_lamp/README.md`: 318; `examples/events/orbit_lamp/make_worlds.py`: 1; `tests/test_orbit_lamp_readings.py`: 1; `tools/click_readings/orbit_lamp.py`: 1 |
| series R | `examples/events/entities/make_definitions.py`: 69; `examples/events/quarks/make_worlds.py`: 1,8; `tools/click_readings/quarks.py`: 1,152; `tools/click_readings/quarks_replay.py`: 1 |
| series J2 | `examples/events/gate_set.json`: 3; `examples/events/weak/make_worlds.py`: 3,276; `tests/support/hand_worlds.py`: 49; `tests/test_weak_readings.py`: 58; `tools/click_readings/weak.py`: 3 |
| series U | `examples/events/clock_word/expectations.json`: 103; `examples/events/clock_word/make_worlds.py`: 18,23,28,203; `examples/events/shell_clock/make_worlds.py`: 89 |
| series J1 | `examples/events/weak/README.md`: 212; `examples/events/weak/make_worlds.py`: 4; `tests/test_w_world.py`: 14; `tests/test_weak_readings.py`: 71; `tools/click_readings/weak.py`: 4 |
| series L3 | `examples/events/amplitude/pages/bell.html`: 72; `examples/events/amplitude/pages/build_pages.py`: 1230; `tests/test_amplitude_pair.py`: 4; `tests/test_hand.py`: 92 |
| series O | `examples/events/README.md`: 76; `examples/events/moving_detector/README.md`: 18; `examples/events/moving_detector/make_worlds.py`: 10,144 |
| series J | `examples/events/README.md`: 489; `examples/events/weak/README.md`: 3; `examples/events/weak/make_worlds.py`: 1; `tools/click_readings/weak.py`: 1 |
| series Q | `examples/events/README.md`: 604; `examples/events/c_measured/make_world.py`: 1; `tests/test_algebra_visualizer.py`: 6; `tools/click_readings/c_measured.py`: 1 |
| series N | `examples/events/binding/README.md`: 115; `examples/events/binding/make_worlds.py`: 1; `examples/events/entities/make_definitions.py`: 64 |
| series F | `examples/events/bohr/README.md`: 35,72; `examples/events/bohr/make_worlds.py`: 9 |
| series P | `examples/events/entities/make_definitions.py`: 89; `tests/support/hand_worlds.py`: 1; `tests/test_hand.py`: 57 |
| series L6 | `examples/events/amplitude/pages/bell.html`: 138; `examples/events/amplitude/pages/build_pages.py`: 1262 |
| series L2 | `examples/events/amplitude/pages/build_pages.py`: 1135 |
| series W | `examples/events/optical/make_worlds.py`: 141 |
| series L5 | `tests/test_amplitude_gate.py`: 4 |
| series L1 | `tests/test_algebra_visualizer.py`: 7 |
| series L7 | `tests/test_amplitude_cone.py`: 1 |
