# Registered blocks and compositions

Parametric **data generators** for the matter/light building blocks, and the composer that turns a
composition (`u24-composition-v1`, designed by the program registrar r21) into one initial state.
They let an experiment ship a short composition instead of large init files, and let anyone
regenerate those files from tracked code. Nothing here evolves a state or acts after t = 0.

```python
from research.matter_light_blocks_v1.registry import compose, d1_main_spec, init_data

prepared, assertions = compose(d1_main_spec(100))     # the published block d1_local_atom_L100
data = init_data(prepared, steps=140)                 # the official init format
```

## Registered generators

| id | prepares | checks before writing |
| --- | --- | --- |
| `matter_line@1` | a straight class-0 fibre of one self-ported label at rest, with optional seed sockets | the label is self-ported along the axis |
| `light_line@1` | a gauged straight light fibre: r = 0 / 4 alternating with a gauge phase | chain weight −1; even length on a closed loop |
| `slot_clock@1` | one silent period-4 channel in a slot of a light-line node | the state is one of the 8 silent slot states |
| `slow_glider@1` | an r06 SLOW or SLOW_LEFT glider seed (window + history halo), filling a matter-line socket | chain sign; vacuum (0,0,2) |
| `spin_ring_z@1` | r04's 28-cell holonomy-z light ring at a matter-line node ([`data/spin_ring_z.json`](data/spin_ring_z.json)) | signs (−,+,+) |
| `guide_net@1` | gauged guide paths (straight, staircase, branches = degree 3–6 junctions, closed rings), with in-flight packets (forward, inward `~path`, or halo-only `keep: "halo"`); a port of r04's guide algebra ([`guides.py`](guides.py)) | packet admissibility (unit transmission); guide paths must agree |
| `pulse_train@1` | a straight fibre with unit pulses given by arrivals (m, t) or a stream; σ = −1 on channel 14 gives the K-image fibre | the label is self-ported along x; separate pulses need period ≥ 4 |
| `phase_gate@2` | an all-48 dark clock two sites from a fibre node, orbit phase 0..3 of (−1,−1,0), with the history halo for phases 1 and 3 | the offset is two sites along one transverse axis |
| `all48_site@1` | all 48 channels of one site at one triple (monomers, rotors, breathers, the A1 core) | exactly one of triple / phase |
| `single_channel@1` | one prepared channel (stars, trap cores) | — |
| `k_core@1` | the T6 k-cores through the tracked `research.components` factories | +++ (as those factories) |
| `light_line@2` (alias key `light_line_s@1`) | `light_line@1` with a socket window that a `fibre-packet` or `glider-seed` filler must fill; no sockets = `light_line@1` exactly | as `light_line@1` |
| `fibre_packet@1` | an in-flight r04 packet (shape (1,−1) by default) on a gauged light line, in socket form | the front sits on a class-0 node |
| `literal_patch@1` | literal initial data `[[x,y,z,g,a,b,r], ...]` (seeds found by rewind, e.g. [`data/bb27_point.json`](data/bb27_point.json)) | no duplicate address |
| `all48_planes@1` | consecutive whole planes, every site holding all 48 channels in one triple (planar gliders, mark planes) | — |
| `matter_line@2` | `matter_line@1` with a periodic r06 catalog medium; medium (0,) = `matter_line@1` exactly | medium classes in {0, 1, 2} |
| `slow_glider@2` | `slow_glider@1` plus explicit r06 catalog species profiles (`compositions.R06_CATALOG`); 'SLOW' / 'SLOW_LEFT' = `slow_glider@1` exactly | window arrays of length W; vacuum (0,0,2) |
| `matter_line@3` | `matter_line@2` plus sparse rest-class marks `[[node, class], ...]` (class-2 marks are r06 phase advancers); no marks = `matter_line@2` exactly | classes in {0, 1, 2}; a mark is not a socket |
| `fused_mover@1` | r29's fused mover β_n (β_1 = r06's SLOW family) on a class-0 chain, front activated at t = −phase, as the cumulative-hand embedding of its free translator ([`bform.py`](bform.py)); fills a matter-line socket of exactly `fused_mover_window(n, front, direction, phase)` | chain weight −1; vacuum (0,0,2); no shared vacuum partner |
| `field_line_bundle@1` | r33's field-line bundle: the (2ρ)² open gauged staircases from a source point toward (2ρ, 2j+1, 2k+1) as guide paths, with parametric packets — `flux` (outward heads on every line), `probe` (one inward packet on each line crossing the plane x = r inside \|y\|, \|z\| ≤ half), explicit `packets` and `root_sources` (one single channel in the −x halo slot of every root) | r04's halo condition over the whole bundle (no shortcut, no shared halo channel) |
| `plane_light@1` | exact A1 plane light on the whole board: beams `{sigma, profile, shift}` along the eight body diagonals, a = Σ f(σ·x + 1 + k), b = Σ f(σ·x + k), r = 2 on all 48 channels (one beam (1,1,1) with a delta profile is the published `diag_sheet`) | σ a body diagonal; the profile period divides L; +++ and the vacuum (0,0,2) |

The lineage of every generator is recorded in `generators.LINEAGE`. A changed generator gets a new
version (`@2`); a composition names the versions it uses.

## Compositions

A composition holds:
* one board: `side`, `background`, and `coupling.signs`. `coupling.variant` must be `null`
  in this version;
* placements: `name`, `block`, `params`, `at`, proper 2O `orientation` and explicit `wrap`;
* declared `assertions` on the initial data (junction classes, silent slot clocks);
* informational `timing` and `steps`;
* `controls`, which are masks of the same composition (`apply_control`: remove placements,
  override parameters, unfill sockets).

The strict assembler of `research.components` rejects overlaps, additions, wrong socket fillers,
and mixed tensors or backgrounds.

`compositions.py` writes r11's D1 module this way. `tests/test_matter_light_blocks_registry.py`
checks that four published blocks regenerate exactly: `d1_local_atom_L100`, `d1_local_atom_L200`,
`d1_control_no_seed_L100` and `d1_skeleton_atom_spin_clocks_L160`. Before publication, the port
was also checked against the program's own code:
* it gives the same specification, state and init JSON as the registrar's composer on all seven
  D1 files;
* the glider generator equals r06's `glider_delta` on 768 label, sign and start cases.

## Gauge transport, includes and assertions (r21, WAVE 2)

* **One tensor per board.** A placement whose block needs another triple is refused, unless it carries
  `gauge` (`{"character": bool, "staggered": bool}` or `"auto"`) and `native_signs`. The block is then
  generated for its own triple and moved into the board's triple as data ([`symmetry.py`](symmetry.py);
  THEORY S7: `research/matter_light_v1/chapters/THEORY.md`, program record). This is allowed only inside one
  gauge class (B = {+++, +−−, −++, −−−}, F = the other four), with a J-fixed background, and on even L when
  staggered. The click addresses are unchanged; C1↔C2 and q → −q on the flipped channels. Coupling patches
  between different triples are impossible (r16,
  [`research/coupling_variants_v1`](../../coupling_variants_v1/README.md)).
* **Includes.** A placement `{"include": spec, "at": [...], "gauge": ..., "prefix": "..."}` inlines a
  sub-composition (`expand`), carrying its assertions.
* **Assertions.** `junction_classes`, `slot_clocks_silent`, `beside_fibre` (a gate clock two sites from a
  node of a named guide), `clearance` (minimum Manhattan distance between placement groups) and, from
  WAVE 4, `guide_halo_clear` (every halo channel of a named guide port is vacuum except listed junction
  channels: r04's insertion rule for rings beside a line).
* **Controls.** `apply_control` on a spec without `assertions` adds none (WAVE 4, r12's report).

## Metadata

* [`data/registry.json`](data/registry.json) (`u24-registry-v1`): every registered block (id@version,
  kind, registration new / update-of / republication-of, generator, coupling, evidence status, parts,
  lineage), the experiments and their cards (`experiment_cards`), the read-only `observers`, the
  `aliases`, the registrar's decisions on proposed cards, the verified points (init files regenerated
  exactly, recipes and builder equalities, with SHA-256 prefixes; 507 after WAVE 17, all exact), and the
  role of each of the 348 published names (the 338 of 8301320, the 8 appended in dff39dc and the 2 appended with the
  candidate-coupling framework (the variant block and its reference companion): canonical, variant, control, alias,
  J-image, experiment instance).
* `variant_couplings` in [`data/registry.json`](data/registry.json): the five explicitly separate candidate tables
  that r16 reviewed (program record), each with its label, construction, review and files. They are records only:
  the composer composes reference boards, so a variant block is a variant init file of
  [`research/coupling_variants_v1`](../../coupling_variants_v1/README.md) (`interaction.chiral_two_sector_board@1`,
  published as `chiral_two_sector_board_L192` beside its reference companion).
  `tests/test_matter_light_blocks_registry_variants.py` rebuilds the five tables from their constructions.
* [`data/cards.json`](data/cards.json): one card per block. Card format: (a) use = purpose, interface, timing,
  coupling and composability; (b) algebra = the law with its evidence label; (c) clocks = gears and click signature.
  From WAVE 6 a block's card text is kept here only (its `registry.json` entry carries no second copy).

Both files are compact JSON. Paths and modules under `research/matter_light_v1/` that the registry's code or data
name are files of the program's working folder, archived uncurated on branch `backup/matter-light-working` at commit
2483837, except five WAVE 5 source files (`r27b/cards_r27b.json` and the four `r27b/preparations/bb27v4_ringclock_*`
files) and r30's `proposal_chiral_both_forces.json` (WAVE 9, the variant block), which are first archived at commit
9f9cc64, the WAVE 6 sources at commit 39ca35f, the WAVE 7 and 8 sources at commit 7aac8c5, the WAVE 10 sources
(builder D's `remote/builderD_R5/` and `remote/BUILDER_D_REPORT5.md`, r10r's `r10/r10r_REVIEW.md`) at commit 96b1c0f
and the WAVE 11 sources (builder D's `remote/builderD_QMA_interim/`, `remote/builderD_QMA_final/` and their
reports, fresh machine 2's `remote/FRESH_MACHINE_REPORT_QMF4.md`) at commit 6c0798c, r10g's
`r10/REVIEW_R10G_W9.md` at commit 01790e6, and the WAVE 12 sources (builder B's `remote/builderB_QMB3/qmb/`,
`remote/builderB_QMB5/qmb8/` and the QM-B8 section of `remote/BUILDER_B_REPORT_QMB_FULL.md`, r10zc's
`r10/r10zc_REVIEW.md`, fresh machine 2's `remote/FRESH_MACHINE_REPORT_QMF5.md`) at commit 3ca4977, and the WAVE 13
sources (r70's `r70/flrw.py`, `r70/kit70.py`, `r70/results/`, r10zf's `r10/REVIEW_R10ZF.md`, the fresh-machine
reports `remote/FRESH_MACHINE_REPORT_GRF8.md` and `GRF10.md`) at commit 3ee08d7, and the WAVE 14 sources
(builder B's `remote/builderB_QMSHOW/qmshow/`, `remote/builderB_QMSHOW5/qmb/grid.py`, r10zh's `r10/REVIEW_R10ZH.md`,
fresh machine 2's `remote/FRESH_MACHINE_REPORT_QMF15.md`) at commit fd49c09, and the WAVE 15 sources (builder F's
`remote/builderF_FINAL/`, `remote/BUILDER_F_REPORT_SWL.md`, r10zi's `r10/REVIEW_R10ZI.md`, fresh machine 2's
`remote/FRESH_MACHINE_REPORT_GRF12.md`) at commit c2b4258, and the WAVE 16 sources (r71's `r71/tensor_board.py`,
`r71/time_board.py`, `r71/stations_*.json`, r10zg's `r10/REVIEW_R10ZG.md`, fresh machine 2's
`remote/FRESH_MACHINE_REPORT_GRF9.md`) at commit c2b4258, and the WAVE 17 sources (builder C's
`remote/builderC_GRS/grs/`, `remote/BUILDER_C_REPORT_GRS.md`, r10zj's `r10/REVIEW_R10ZJ.md`, fresh machine 1's
`remote/FRESH_MACHINE_REPORT_GRF11.md`) at commit c2b4258.
Nothing there is needed to regenerate or verify a block or a composition; `runs/` paths are local.

`compositions.py` also holds the WAVE 2 compositions: the published guide instances
(`published_guide_specs`), r08's W9 devices, r03's Q1c selector, r12's approval router, r13's beam-splitter
device, r11's twin atoms, r20's SR2, r15's D2 / D2J / CHSH stations, r24's A1 core, and the integrator
specs `flagship_v3_spec` (r06b), `bell_router_spec` (r12) and the `target_*` specs (r27).
`tests/test_matter_light_blocks_registry_wave2.py` regenerates eight published blocks exactly from
`guide_net@1` and checks the gauge transport natively.

WAVE 3 added r27's backward Big Bang (`bb27_target_spec`, `bb27_dark_spec`, `bb27_seed_spec`, data in
`data/compositions/` and `data/bb27_point.json`). WAVE 4 added r06b's flagship v3 / v4
(`r06b_flagship_spec` with r06b's controls; `h1_ring_placement`, `r06b_link_y_placement`,
`r20_bridge_placement`), r23's slow clocks and long links (`r23_cases`), the r08 clock-rate and
spectroscopy instances (`r08_clockrates_cases`, `r08_spectro_cases`), r15's seeded selector
(`r15_w3_selector_spec`), r19's shared-record gate and angle pair (`r19_cases`), r18's planar sector and
Wu seed (`r18_planar_spec`, `r18_wu_seed_spec`), r14's co-moving Einstein modules (`r14_e2_sync_spec`,
`r14_w3_created_spec`), r27's entangled-pair universes (`bb27v2_target_spec`, `bb27v2_seedstar_spec`; data
`data/compositions/bb27v2_base_target_T12_L160.composition.json`) and r12's SCE compositions
(`sce_e07_spec`, `sce_e07b_spec`). `tests/test_matter_light_blocks_registry_wave4.py` regenerates the three
published clock-rate blocks and the eight appended published blocks (`published_appended_specs`) exactly,
and checks the WAVE 4 generators and composer additions.

WAVE 5 added the assemblies `gate.split_pair_reader@1` (`split_pair_reader_placement`; r28's isolated boards
`r28_reg9b_spec` and the created module's readers `r28_module_readers`), `parity.wu_half_cross@1`
(`wu_half_cross_spec`), `detect.race_comparator@1` and `detect.heralded_projection_z6@1` (`r19_race_spec`,
`r19_heralded_z6_spec`; a declared post-selection) and `clock.diagonal_light_clock@1` (`e11_main_diagonal_spec`,
with `e11_control_generic_spec`); the builders of the curated experiments E09 (`r23_e09_cases`), E10
(`e10_spec_all`, ported from r22's builder, and `e10_lamp_spec`) and E11 (`E11_light_clock_dilation`: main board
`e11_main_plane_light_spec` of WAVE 8, control board `r25_e11_cases`); and r27b's cards
`clock.ring_emitter@2` (`ring_tap_placement`), `clock.ring_clock_h1@1` (`ring_clock_h1_placement`) and
`medium.mirror_bridge@1` (`mirror_bridge_placement`). No generator changed.
`tests/test_matter_light_blocks_registry_wave5.py` regenerates the three published planar blocks from
`all48_planes@1` and checks the WAVE 5 builders against their assertions and recorded initial-state hashes.

WAVE 6 added [`bform.py`](bform.py) (initial data from cumulative hands B(−1), B(0), r29's Theorem B0) and the
generators `fused_mover@1`, `matter_line@3` and `field_line_bundle@1`; the cyclic universes of r36 — `seed.cyclic_point@1`
(`CYCLIC_POINT`, `cyclic_point_placement`), `spin.holonomy_ring@2` (`holonomy_ring_counterpair_placement`),
`cyclic_light_spec` (C1), `cyclic_matter_spec` (C2) and `cyclic_spin_spec` (C3a, whose seed is prepared by an exact
recipe: form `'outgoing'` with 11 exact rewinds, or r36's form `'incoming'` with 11 updates; the two agree because
the seed is JR-fixed) — r36b's gravity inside the cycle (`cyclic_gravity_spec`: G1 and C3b as ONE composition each,
the dark parts plus one moment patch per part, `R36B_MOMENTS` = `seed.cyclic_point@2`; parts `counter_ring_placement`
= `clock.counter_ring@1`, `clock.counter_lamp@1`, `spin.box_loop_z@1`; `r36b_part_spec`) and r27b's exact bounce
`bigbang_bounce_v6_spec`; r33's field-line bundle as the generator `field_line_bundle@1`
(`field_line_bundle_placement`; `e13_spec` and `e13b_spec` regenerate every board of the curated experiment
`E13_exchange_contact_counts`, whose `created_flux` composition is E13b); r29's fused movers and rail pairs
(`fused_mover_line_spec`, `towed_pair_spec`, `leapfrog_pair_spec`); and split guide paths for vacuum gap nodes
shared by two fibres (`split_guide_path`, `path_through`, `gapped_guide_placement`): r20's `gate.x_gate@1`
(`x_gate_spec`), `store.x_cavity@1` (`x_cavity_spec`) and `select.escorted_junction@1` (`escorted_junction_spec`),
and r15b's `select.escort_pair_router@1` (`escort_pair_router_spec`), `store.set_entrance@1`,
`router.conserving@1` (`conserving_router_spec`) and `router.conserving_pair@1` (`conserving_pair_router_spec`),
whose halo-core registers are `slot_clock@1` cores at an orbit phase (`CORE_ORBIT`; at phases 2 and 3 the nodes they
share sit at r = 2, the vacuum value, so they are gap nodes). Existing generators are unchanged.
`tests/test_matter_light_blocks_registry_wave6.py` checks these builders against recorded initial-state hashes,
the seeds' JR symmetry, both C3a recipes natively and the bundle generator against the explicit guide form.

WAVE 7 added the atoms inside the cycles and the bounces, every seed as ONE composition of existing generators (no
generator changed): r36b's C3c (`cyclic_universe_c3c_spec`: C3b plus `atom.twin_cavity_module@1`,
`twin_cavity_atoms_placements` / `twin_cavity_atoms_spec` with its controls `no_escorts` and `right_inarm_plus1`;
the escort sources are `seed.cyclic_point@2` patches, `ESCORT_WALL_MINUS_Y`), r36's C3a without a recipe
(`cyclic_spin_moment_spec`: the ring's moment patch `C3A_RING_MOMENT`), r27c's twin-atom module
`atom.twin_xcavity@1` (`MOD82`, `twin_xcavity_module_placements`, `twin_xcavity_module_spec`), U82 = C3a + MOD82
(`cyclic_spin_atoms_spec`) and the exact bounce with atoms s\*_c (`bigbang_bounce_atoms_spec`, controls
`no_escorts` and `up_escort_late`), and r26b's half-integer bang (`half_integer_bang_spec`, design PG: b = 0 on every
channel). `tests/test_matter_light_blocks_registry_wave7.py` checks them against recorded initial-state hashes, the
seeds' JR symmetry and the moment patches natively.

WAVE 8 added the generator `plane_light@1` (`light.plane_light@1`, an update of `light.front_111@1`: sums of exact
plane waves along the body diagonals; `plane_light_placement`). It writes r26b's E14 (`e14_two_beam_spec`, one placement
with the seven runs as beam masks), r25's E11 main board (`e11_main_plane_light_spec`, the same state as
`e11_main_diagonal_spec`) and the published `diag_sheet`. `tests/test_matter_light_blocks_registry_wave8.py` checks
them against the recorded initial-state hashes and the published block.

WAVE 9 added the registry records of the explicitly separate candidate couplings, as data only (no generator or
composition changed; the composer still composes reference boards only): `variant_couplings`, the five reviewed
tables, and the block record `interaction.chiral_two_sector_board@1` of the published variant block
`chiral_two_sector_board_L192`, a `universe24-variant-init-v1` file of
[`research/coupling_variants_v1`](../../coupling_variants_v1/README.md) (generator none) with two prepared,
non-interacting sectors on one board (R10G-44, R10G-73), beside its reference companion
`chiral_two_sector_board_L192_control_reference` ((−,+,+)). The block's catalog entry declares its table as
`{"kind": "variant", "label", "fingerprint"}`; its record and card name the same label.
`tests/test_matter_light_blocks_registry_variants.py` rebuilds the five tables from their constructions with the
framework and checks that the variant block carries exactly its table.

WAVE 10 (r67) added builder D's device CC7-M (R5, refereed by r10r: R10R-0..13) as the assembly
`select.escort_end_junction@1`, a variant-of `select.escorted_junction@1` with a bare-ended input line, bare-ended
exits behind the doors and escort lines bent away 4 nodes from them (`CC7M`, `cc7m_router_placement`: pieces of
`guide_net@1` through `gapped_guide_placement`, every path running outward from the junction or a door). Its members
`cc7m_spec(h, L)` differ only in escort B's starting end h, a datum of the prepared state, not of the hardware
(controls `no_quantum` and `no_escorts`, packet masks); the member h = 1 at its integer moment t = 9 is
`cc7m_moment_placements` (the hardware without packets plus three `seed.cyclic_point@2` patches, `CC7M_H1_MOMENT`), and
`cc7m_in_c3c_spec(L)` places it beside r36b's C3c seed with the class-B gauge into (−,+,+) (controls `c3c_alone` and
`device_alone`). No generator changed. They write the curated experiments `E20_one_hardware_two_outcomes` and
`E20b_one_hardware_in_c3c`. `tests/test_matter_light_blocks_registry_wave10.py` checks that the members and the union
write builder D's init files byte for byte, that both members have the same hardware and differ in 14 cells on escort
B's line or its face neighbours, that the moment form is the member advanced 9 updates natively (JR-fixed), and that
the union is C3c's seed plus the device, with disjoint supports.

WAVE 11 (r67) added builder D's device CC8 (QM-3; refereed by r10g, R10G-276..286, and reproduced by fresh machine 2,
QM-F4) as the assembly `select.escort_lattice_router@1`, a variant-of `select.escort_end_junction@1`: CC7-M's
hardware with a 60-node input line and both escort lines trapped below their doors (`CC8`, `cc8_router_placement`),
so that one elementary quantum and two escorts, all in flight at t = 0, meet only on an 8-update lattice. Its members
differ only in two packets: the quantum's hidden phase τ (`CC8_QUANTUM`, 14 values) and escort C's device phase D′
(`CC8_ESCORT_C`, 13 values); `cc8_spec(runs, L)` is one composition with one control `tau{τ}_D{D′}` per member
(packet masks), and `cc8_prediction(τ, D′)` is builder D's coincidence arithmetic. No generator changed. They write
the curated experiment `E22_one_quantum_one_exit`. `tests/test_matter_light_blocks_registry_wave11.py` checks that
the representative members write builder D's init files byte for byte, that all 182 members have the same hardware
and differ only in the quantum's and escort C's packets, that the prediction gives N_B = 1, 2, 3, 5, 6, 7, 8, 9, 10,
11, 11, 12, 13 for D′ = 1, 2, 3, 6–12, 14–16 (no ties), and that two short native runs click first at the predicted
exit, 2 updates after the coincidence, with all three prepared packets lit at update 1.

WAVE 12 (r67) added builder B's triple gate (QM-B3 / QM-B8; refereed by r10zc, R10ZC-7..9, and reproduced by fresh
machine 2, QM-F5) as the assembly `gate.triple_x_gate@1`, a variant-of `gate.x_gate@1`: an x-, a y- and a z-fibre
through one vacuum gap node, (−,+,+), one unit (1,−1) packet per line (`TRIPLE_GATE_PATHS`, `triple_gate_params`: one
`gapped_guide_placement` of `guide_net@1` paths; a J-flipped line is the same path with the opposite gauge sign; the
gate gear g = 3, 4 one `literal_patch@1` cell). `triple_gate_spec(members, L)` is one composition with one control
per member (Dy, Dz, sy, sz, g) (for g = 2 the gear placement is removed). No generator changed. They write the
curated experiment `E25_two_time_counting_rule`, whose mirrored runs are init files JR(x_T) written from each run 1's
complete final state. `tests/test_matter_light_blocks_registry_wave12.py` checks builder B's two init files byte for
byte, the members' controls, that two mirrored runs (second forward runs) end at JR(x0) with run 1's records mirrored
and the statistic k̄ = k, E25's init-file hashes, and the ε-twin (gears 2 and 3: identical clicks (t, x, k, q),
finals differing only in the gate r).

WAVE 13 (r67) added r70's rung-E9 boards (refereed by r10zf, R10ZF-1..11; reproduced by fresh machines 1 and 2, GR-F8
and GR-F10) as the assembly `light.flrw_relay_lattice@1`: a static, comoving relay lattice of fibre light whose
standard clocks are tapes, trains of A-pulses passing each station's tick node at prescribed updates, so that a(η) is
written into the packet positions (prescribed, not caused by matter). `flrw_params(version, schedule)` gives one
`guide_net@1` placement (tapes; the radar and emission branches as degree-3 fan-out junctions; closed 16-node rings;
for v3 closed 600-node tape rings) with the data `FLRW` and `FLRW_TICKS` (r70's tick schedules), and `flrw_spec(runs,
L, version)` one composition per hardware version and board side, the hardware without packets and one control per
schedule. No generator changed. The composed EdS, EdS_2L, RAD, DARK, EdS2, RAD2, STATIC2 and CYC boards equal r70's
init files byte for byte. They write the curated experiment `E23_flrw_in_clicks` (withdrawn from the curated experiments on 2026-11-09; the block stays).
`tests/test_matter_light_blocks_registry_wave13.py` checks the DARK board against r70's init file byte for byte,
r70's tick schedules, the tapes' packets for every schedule and the U-path, lane and ring geometry.

WAVE 14 (r67) added builder B's QM-SHOW router (refereed by r10zh, R10ZH-27..33; reproduced by fresh machine 2,
QM-F15) as the assembly `gate.x_gate_pair_router@1`, a variant-of `gate.triple_x_gate@1`: the triple gate's x- and
y-lines through one vacuum gap node with two separately prepared (1,−1) packets, Q 12 nodes and K 12 + D nodes before
the gate (`x_gate_pair_params`, `x_gate_pair_key`; `x_gate_pair_spec(entries, L)`: one composition, one control per
member and packet mask); for D = 8 (2 of the 34 members) the y-line begins at K's lead, so only K's leading cell (0,
∓1) is placed: there K is a truncated packet, not a full (1,−1) quantum. No generator changed. All 136 composed
boards (34 members × 4 masks) equal builder B's, and his two CLI init files are reproduced byte for byte. They write
the curated experiment `E26_one_gate_two_quanta`. `tests/test_matter_light_blocks_registry_wave14.py` checks the two
init files, the packet masks, and for all 8 of E26's mirror runs the init-file hashes, the return to JR(x0) and the
mirrored records, with the exact union of the branch logs where the gate stays silent.

WAVE 15 (r67) added builder F's prescribed Schwarzschild-lapse ladder (g00 only; refereed by r10zi, R10ZI-1..20;
reproduced by fresh machine 2, GR-F12) as the assembly `clock.lapse_ring_ladder@1`: five closed rectangle rings of
node counts 120/N with static taps and three side taps (`LADDER`, `ladder_params`, `lapse_ladder_spec(L)`; equal to
builder F's init file byte for byte), and his SHAPIRO-RADIAL chain (`SHAPIRO`, `shapiro_params`,
`shapiro_chain_spec(L)`, controls curved and flat). No generator changed. They write the curated experiment
`E27_lapse_ladder_g00` (withdrawn from the curated experiments on 2026-11-09; the block stays), read by the frozen layer gr_observer_v1. `tests/test_matter_light_blocks_registry_wave15.py`
checks the init file, the node counts 120/N, the taps and the two chains.

WAVE 16 (r67) added r71's radar tensor station (refereed by r10zg, R10ZG-1..12; reproduced by fresh machine 2, GR-F9)
as the assembly `light.radar_tensor_station@1`: a standard 16-node ring clock and 26 staircase radar arms of fibre
light, one per lattice line and its negative, arm n assigned the coordinate B n by the designer with the node count
round(B √(nᵀgn)) (`TENSOR`, `TENSOR_G_ANISO`, `tensor_length`, `tensor_arms`, `tensor_station_spec(name, g, B)`; the
Manhattan control with g = 'manhattan'), and the two-station time board (`tensor_time_spec()`, r71's v2). No
generator changed. The aniso, manhattan and time_v2 boards equal r71's init files byte for byte. They write the
curated experiment `E24_metric_tensor_declared_chart` (withdrawn from the curated experiments on 2026-11-09; the block stays). `tests/test_matter_light_blocks_registry_wave16.py` checks the
time board against r71's init file, the design lengths of aniso and manhattan, and the arm geometry.

WAVE 17 (r67) added builder C's GS-2b (refereed by r10zj, R10ZJ-1..20; reproduced by fresh machine 1, GR-F11) as the
assembly `light.radial_relay_tree@1`: one connected relay tree of fibre light whose node counts were prescribed from
Schwarzschild's formulas (M = 64), a spoke with six junctions and at each an open spiral branch fibre whose A→B node
count is C_i = round(2πr_i/N_i) (prescribed; it does not close and encircles nothing), and seven ring clocks (`GS2B`,
`GS2B_MEMBERS`, `gs2b_design`, `gs2b_params`, `gs2b_spec(member)` for S, T, F, D and S2L). No generator changed.
GS2b_S equals builder C's init file byte for byte. It writes the curated experiment
`E28_schwarzschild_radial_profile` (withdrawn from the curated experiments on 2026-11-09; the block stays). `tests/test_matter_light_blocks_registry_wave17.py` checks GS2b_S against builder
C's init file and the design integers.

## Limits

These are generators for the prepared media of the program; a successful composition is a valid
preparation, not a proof that the parts keep their behaviour together (that needs a native run). This
version composes boards with one of the eight reference sign triples only.
