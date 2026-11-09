# Matter and light experiments (curated, v1)

Each experiment here shows one result of the matter/light research program on the unchanged reference model (E19:
under an explicitly separate candidate variant, labelled as such). It is **data**: compositions of registered blocks,
init files in the official format (E19: the variant format) or references to published blocks, declared detectors,
and a card. One generic verifier replays every run natively with the exact inverse,
writes the official click log, and reads every claim **only from the frozen click decoder's report**
(`research/click_decoder_v1`). There is no per-experiment code.

Names such as "light", "matter", "atom", "clock", "charge", "spin", "quantum", "collapse", "entanglement",
"superposition", "redshift", "Shapiro delay", "Schwarzschild", "Big Bang", "bang", "universe" and "bounce" are
**candidate names for click patterns** of this model. No physical photons, mass, charge, spin-1/2, gravity,
cosmology or quantum behaviour is claimed. `C2` is not a selection law and `Q` is not energy (AGENTS rules 10 and 12).

## Index

| id | title | coupling | claim label | decoder checks | verdict | runtime |
|---|---|---|---|---|---|---:|
| [E01](E01_local_atom_twins/CARD.md) | locally created atom candidates (D1) and twin atom candidates in exact phase | (−,+,+) | SIMULATION | 16 of 16 pass | r10e R10E-52 CONFIRMED | ~1.5 min |
| [E02](E02_clicktime_chsh/CARD.md) | CHSH with light approvals: board-time S = 2, click-time S = 4 (a PR box, not quantum) | +++ | THEOREM + SIMULATION | 8 of 8 pass | r10e R10E-39 CONFIRMED | ~1 min |
| [E03](E03_exclusive_detection/CARD.md) | exclusive single-click detection: with one light approval exactly one of two detectors clicks | +++ | THEOREM + SIMULATION | 5 of 5 pass | r10e R10E-53 CONFIRMED | ~15 s |
| [E04](E04_einstein_created/CARD.md) | two-way Einstein synchronisation with created atom-clock candidates, t_B = (t1 + t2)/2 | (−,+,+) | SIMULATION | 10 of 10 pass | r10e R10E-40 CONFIRMED | ~1 min |
| [E06](E06_moving_clocks/CARD.md) | moving clocks: co-moving Einstein synchronisation gives δ = (3/8)(D + 24) | (−,+,+) | SIMULATION | 8 of 8 pass | r10e R10E-54 CONFIRMED | ~1.5 min |
| [E07](E07_sce_collapse_entanglement/CARD.md) | collapse and entanglement candidates in clicks: one approval gives one outbound copy (α = 0); a common-past Z4 Bell test, CHSH 2 | +++ | THEOREM + SIMULATION | 31 of 31 pass | r10e R10E-55 CONFIRMED (r10f R10F-9) | ~0.5 min |
| [E07b](E07b_sce_superposition_interference/CARD.md) | superposition and interference candidates in clicks: two exact C0 fronts, dark planes z = 0 and 3 | +++ | THEOREM + SIMULATION | 9 of 9 pass | r10e R10E-56 CONFIRMED (r10f R10F-10) | ~10 s |
| [E09](E09_einstein1911_clicks/CARD.md) | Einstein-1911 signatures in a prepared light-flux medium: Shapiro +4 per packet met, river, route switch, a received pattern that repeats every 24 instead of 16 (α = 1, γ = 0) | +++ | SIMULATION | 17 of 17 pass | r10f R10F-8 CONFIRMED | ~15 s |
| [E10](E10_prescribed_schwarzschild_lattice/CARD.md) | prescribed Schwarzschild relay lattice (PRESCRIBED geometry, not sourced gravity) | +++ | THEOREM + SIMULATION | 73 of 73 pass | r10f R10F-7 CONFIRMED | ~0.5 min |
| [E11](E11_light_clock_dilation/CARD.md) | moving light clocks: the beat of two exact diagonal light waves ticks at Ω = ω′√(1 − u²/c_s²), c_s = 1/√3, an identity of exact linear dispersion (free kinematics in the lattice frame) | +++ | THEOREM + SIMULATION | 10 of 10 pass (3 decoder, 7 beat_clock_v1) | r10g R10G-35 CONFIRMED (R10G-36) | ~10 s |
| [E12](E12_planar_forces/CARD.md) | contact forces in a planar universe: a decaying seed plane, an EM-like sign rule at + and − walls, confinement between opposite signs, and a clock pulled toward the seed without fall-off over D = 4 and 7 | +++ | SIMULATION | 20 of 20 pass (projection layer) | remote FRESH6-1 CONFIRMED | ~6 min |
| [E13](E13_exchange_contact_counts/CARD.md) | exchange contact counts on prescribed field lines: a fixed-area probe meets the prepared geometric count (192/r)² of lines, each delaying its probe quantum by 4 (prescribed flux) or 2 (created front) at every r: contact only, no fall-off per probe | +++ | THEOREM + SIMULATION | 19 of 19 pass | r10g R10G-46..50, 78..83 PARTLY (46, 47, 49, 78, 79 CONFIRMED) | ~4 min |
| [E14](E14_two_beam_interference/CARD.md) | exact two-beam interference of prepared board-filling plane light: zero clicks on dark planes spaced λ/(2 sin θ/2) at 109.47°, 70.53° and 180°, fewer clicks with both beams, and a click-silent update after each b = 0 moment of the standing wave | +++ | THEOREM + SIMULATION | 15 of 15 pass | remote FRESH6-2 CONFIRMED | ~3 min |
| [E15](E15_cyclic_bangs/CARD.md) | exactly periodic bang candidates: two time-symmetric moments per cycle (periods 48, 164, and 164 with a 720° ring) | (−,+,+) | THEOREM + SIMULATION | 29 of 29 pass (15 decoder, 14 log_symmetry_v1) | remote FRESH4-B1..B4, r10h R10H-29..31 CONFIRMED | ~20 s |
| [E15b](E15b_planar_cyclic_box/CARD.md) | a cyclic planar box: the seed plane between two + planes re-bangs exactly every 4d + 4 = 16 updates | +++ | THEOREM + SIMULATION | 4 of 4 pass (log_symmetry_v1) | remote FRESH6-1, r10g R10G-74..77 CONFIRMED | ~30 s |
| [E16](E16_bigbang_backward_v5/CARD.md) | Big Bang candidate v5, built backwards: created light, two created ring clocks (36, 22), one gate decision, a matched α_in = 1 instrument pair and a radar echo, from a 14-cell seed in a prepared network | (−,+,+) | SIMULATION | 20 of 20 pass | r10h R10H-1..8 PARTLY (1, 3, 4, 7 CONFIRMED) | ~2 min |
| [E17](E17_exact_bounce_v6/CARD.md) | an exact bounce: one JR-fixed state s* whose contraction and expansion are mirror images in the clicks (0 of 49,830 records unpaired), on L and 2L | (−,+,+) | THEOREM + SIMULATION | 12 of 12 pass (7 decoder, 5 log_symmetry_v1) | remote FRESH4-A1..A3 CONFIRMED | ~2 min |
| [E18](E18_cyclic_universe_c3c/CARD.md) | C3c, a cyclic universe candidate (period 320): created light, created matter at exact ∓1/3, a 720° spin ring, a ring clock at N = 3/5 and twin cavity atom candidates | (−,+,+) | THEOREM + SIMULATION | 15 of 15 pass (9 decoder, 6 log_symmetry_v1) | remote FRESH8 CONFIRMED (K6 PARTLY) | ~1 min |
| [E19](E19_cyclic_universe_c4_variant/CARD.md) | VARIANT C4: seven prepared, non-interacting sectors on one board, sharing one bang and turnaround schedule (period 320): light, matter at exact ∓1/3 and twin cavity atom candidates created by the decoder's positional rule inside prepared modules, a 720° spin ring, a ring clock at N = 3/5, and the weak-like (32 vs 56) and EM-like signatures | VARIANT chiral-011-mpp@190301d802c5 | THEOREM + SIMULATION | 15 of 15 pass (10 decoder, 5 log_symmetry_v1) | remote FRESH11-C4, r10g R10G-111..117, 119 CONFIRMED (R10G-120 PARTLY, wording) | ~1.5 min |
| [E20](E20_one_hardware_two_outcomes/CARD.md) | one hardware, two outcomes: two prepared initial states on identical hardware, differing only in escort B's starting end h, light only exit B and its clock (h = 0, exact cycle 90) or only exit C and its clock (h = 1, exact cycle 320); only one detector ever clicks in a cycle; for the detector-only observer the outcome is known only through the detector click, while the full official log shows h from update 1 | +++ | THEOREM + SIMULATION | 32 of 32 pass (13 decoder, 19 log_symmetry_v1) | r10r R10R-0..10, 12, 13 CONFIRMED (R10R-11 PARTLY, not claimed) | ~20 s |
| [E20b](E20b_one_hardware_in_c3c/CARD.md) | E20's member h = 1 placed in the refereed C3c cycle without interacting with it: period 320, integer moments 160ℤ, only exit C clicks, and the union's click log is C3c's refereed log plus the device's records | (−,+,+) | THEOREM + SIMULATION | 16 of 16 pass (6 decoder, 10 log_symmetry_v1) | r10r R10R-8..10 CONFIRMED | ~40 s |
| [E21](E21_gr_observer_clicks_only/CARD.md) | a clicks-only observer reads E09 and E10 at declared stations: exact clock periods, redshift from exact periods, Shapiro delays, routes, E10's lapse N, radial stretch H_r and α = 2 (E) or 1 (T), and a radar echo whose dwell is one device constant; E10's clicks hold no areal-radius measurement, so no spatial curvature is read | +++ | SIMULATION | 25 of 25 pass (gr_observer_v1) | r10zb R10ZB-1, 3, 4, 5, 7, 16, 17 CONFIRMED (R10ZB-6 PARTLY, fix-6 frame; R10ZB-19's profile wording applied); fresh machine 1 GRF2, GRF5 CONFIRMED | ~20 s |

E01's twin runs reference the blocks appended to `research/matter_light_blocks_v1` in dff39dc. Like E01, E07b's run
a_A references a published block (`exact_front_111_box`).

Decoder pin: `click_decoder_v1` 1.0, frozen 2026-11-09T01:29:27Z (`research/click_decoder_v1/FROZEN.json`). E15,
E15b, E17, E18, E19, E20 and E20b also pin the frozen layer log_symmetry_v1, E11 the frozen layer beat_clock_v1 (release
1.0.3) and E21 the frozen layer gr_observer_v1 (release 1.0.5). An experiment is **ready** when every run
replays exactly (initial-state, final-state and log hashes), every declared check passes and the referee's
verdict is recorded as CONFIRMED or PARTLY (E13 and E16: PARTLY, with their caveats on the cards).

## Commands

```sh
python -m research.matter_light_experiments_v1.verify E01_local_atom_twins E02_clicktime_chsh E03_exclusive_detection \
    E04_einstein_created E06_moving_clocks E07_sce_collapse_entanglement E07b_sce_superposition_interference \
    E09_einstein1911_clicks E10_prescribed_schwarzschild_lattice E11_light_clock_dilation E12_planar_forces \
    E13_exchange_contact_counts E14_two_beam_interference E15_cyclic_bangs E15b_planar_cyclic_box \
    E16_bigbang_backward_v5 E17_exact_bounce_v6 E18_cyclic_universe_c3c E19_cyclic_universe_c4_variant \
    E20_one_hardware_two_outcomes E20b_one_hardware_in_c3c E21_gr_observer_clicks_only \
                                                                                # every one "ready": true
python -m research.matter_light_experiments_v1.verify --all                     # every experiment folder present
python -m research.matter_light_experiments_v1.verify --fast                    # only the runs marked fast
python -m research.matter_light_experiments_v1.verify E04_einstein_created --keep runs/exp   # keep logs and reports
python -m unittest tests.test_matter_light_experiments_v1                       # fast test
```

`--fast` is a smoke test, not a verification: it replays only the runs marked `fast` and reports every check that
reads another run as "skipped (runs not selected)", so an experiment with slower runs ends with `"ok": true` and
`"ready": false`. Only E09, E10, E11, E15 and E21, whose runs are all marked fast, can be ready under `--fast`; E01,
E04, E06, E15b, E17 and E20b have no fast run. `--help` prints the usage, and an unknown flag stops with exit status 2.

```python
from research.matter_light_experiments_v1 import experiment
for run in experiment("E04_einstein_created"):      # engine, initial state and horizon; nothing evolves here
    print(run["name"], run["role"], run["steps"])
```

## What is in an experiment folder

`CARD.md` (at most 40 lines: "On the event board", "In the clicks", "Claim"), `experiment.json` (the manifest),
optionally `composition.json` (`u24-composition-v1` of registered blocks, regenerated by
`research.matter_light_blocks_v1.registry`) or, when the runs need more than one board, composition files under
`compositions/`, `init/*.json` (official init format) and `detectors.json`. Nothing else: no notes, logs, figures or
generated HTML. At most 1 MB of data per experiment.

## The manifest (`matter_light_experiments_v1-experiment-1`)

* `coupling`: `{"kind": "reference", "signs": [..]}`; every run must have exactly this triple. Or, for an explicitly
  separate candidate variant (AGENTS.md; E19), `{"kind": "variant", "label": "variant:<name>@<12 hex>",
  "fingerprint": "<64 hex>"}`, as in the blocks catalog; the card title then begins "VARIANT". Its init files and
  declared board files (`compositions`, no controls, `rewind` as below) are `universe24-variant-init-v1` files loaded
  only by `research.coupling_variants_v1`, whose table must be the declared one; every run is the variant runner's
  audited run (`python -m research.coupling_variants_v1 --audit`, in process), and its official click log is what the
  decoder and the layers read.
* `compositions` (optional): `{key: file}`, composition files inside the experiment folder, for runs on more than
  one board; `composition` (optional) is the default one.
* `runs`: each run names its initial data by `init` + `init_sha256`, or `block` + `block_file_sha256` (a published
  block of `research/matter_light_blocks_v1`, not copied), or `from_composition`: `{"composition": key, "control":
  name, "rewind": k}`, where a control is a mask of that composition (no key: the default `composition`; no control:
  the composition itself) and `rewind` (default 0) prepares the run's start by k exact inverse steps of the composed
  board, each checked, before t = 0 (a preparation, not a stage of the run). A run made only from a composition must
  record `initial_state_sha256`. Every run records `steps`, `initial_state_sha256`, `final_state_sha256`,
  `log_sha256` (the official click
  log) and optional `probes` (a declared detector and window). With `"decode_detectors": true` the run's report also
  carries the decoder's own correlations for `detectors.json["decode"]` (a decoder correlation spec). A run may
  declare a projection layer (decoder README, "Projection layers"): `"layer": {"name": label, "keep": {"y": 0,
  "z": 0}}` with `layer_sha256`. The run is then decoded on the records of its official log whose address has
  those coordinates (axes x, y, z), verbatim and in log order, and that projection's SHA-256 must equal
  `layer_sha256`. Decoder-layer checks (below) still read the full official log.
* `decoder`: name, version and the pinned code SHA-256 of every decoder file; they must equal the decoder's
  `FROZEN.json`, or the verifier stops with "decoder changed: re-validate all experiments".
* `checks`: a closed vocabulary. `pointer` (RFC 6901) into the decoder report, `pointers` (several pointers of one
  report) or `runs` (the same pointer in several runs); `op` in
  `eq ne lt le gt ge approx not_approx in len_eq len_ge same diff`
  (`diff`: two values, the second minus the first). A probe is one decoder `correlations` call over a declared detector
  and window; its entry is stored at `/probes/<name>` of the run's report. A claim the vocabulary cannot express is
  declared with `not_decodable` and its reason, and keeps the experiment from being "ready".
* `layers` (when a check names a decoder layer): `{name: SHA-256}` of each released layer the checks use.
* `verdict`: the referee, the verdict id and the result.
* informational keys, not checked: `composition_note`, `data_bytes`, `built_utc`, `builder` (provenance of the build).

## Decoder layers

Some click patterns need a reading that the decoder report does not hold, for example the time mirror of a log about
a moment or the rate of a beat clock. Such a check names a released, frozen layer of `click_decoder_v1`:
`{"layer": name, "call": function, "args": {...}, "run" | "runs", "pointer" | "pointers", "op", "value"}`, for
example `{"run": "bounce", "layer": "log_symmetry_v1", "call": "mirror", "args": {"tau": 240}, "pointer":
"/unpaired", "op": "eq", "value": 0}`.

* The layers are a closed list in `verify.py` (`LAYERS`, with the calls each allows): `log_symmetry_v1` (`mirror`,
  `best_tau`, `period`, `c_image`, `record_diff`), `beat_clock_v1` (`run_declared`) and `gr_observer_v1`
  (`run_declared`: r64's clicks-only GR observer, its declarations in the experiment's detectors.json). Each is
  frozen by `research/click_decoder_v1/FROZEN_<name>.json`, which names the layer's file and its SHA-256, and the manifest
  pins that SHA-256 under `layers`; any other file reports every check of that layer as "decoder layer changed:
  re-validate".
* A call reads the official click logs of the check's runs first. `record_diff` reads two, `"runs": [a, b]` in that
  order, and the pointer reads its one result. Every other call reads one log: the check's `run`, or each of its
  `runs` (the same pointer in each result, as in decoder checks).
* `args` are passed as they are, except that `{"detectors": pointer}` stands for a value of `detectors.json` (for
  example a beat-clock declaration). An argument that would write files is refused. `clock` may name the declared
  clock that a pointer reads (informational).
* The pointer reads the JSON form of the call's result (integer keys become strings) with the operators of the
  decoder checks (`not_approx`: abs(target − value) > tol). Layer checks count toward "ready" like decoder checks,
  and the report lists each layer's status.

## Derived quantities (`derive`): pure functions of decoder outputs, unit-tested

A station fires in a run if any of its declared probes (`detectors.json["stations"]`) has a fired bin; its outcome is
a = +1 if it fires, −1 if not. Settings are named by keys: **`chsh` uses `"xy"`** (for example `"01"`: x = 0, y = 1);
**the derives below use `"thA,thB"`** (for example `"0,1"`, the settings on Z_N).

| derive | formula | reference |
|---|---|---|
| `chsh` | E_xy = mean of a·b over the runs of a setting; S = max over the four relabellings of the decoder's `chsh` = E(a,b) − E(a,b′) + E(a′,b) + E(a′,b′); marginals P(a=+1), P(b=+1) | Clauser–Horne–Shimony–Holt; local bound 2, Tsirelson bound 2√2, PR box 4 |
| `alpha` | α = N·N_AB/(N_A·N_B) over a declared family of N runs | Grangier–Roger–Aspect anticorrelation parameter |
| `e_table` | E per setting pair and the marginals | — |
| `covariant_curve` | for a full N × N table: covariance E(θA, θB) = E(θA − θB); the curve E(Δ), its discrete Fourier coefficients and ℓ1 norm, P(a = b \| Δ) = (1 + E)/2, and the largest deviations from two **reference curves** cos(2πΔ/N) and 1 − 4\|Δ\|/N (cyclic distance) — reference curves, not claims | r12's covariant-table criterion (program record) |
| `best_chsh` | max over all N⁴ setting quadruples of \|E(a0,b0) + E(a0,b1) + E(a1,b0) − E(a1,b1)\|, and the TLM value there | CHSH |
| `tlm` | max over the four forms \|asin E00 + asin E01 + asin E10 + asin E11 − 2 asin E_xy\|; quantum-consistent iff ≤ π (unbiased marginals) | Tsirelson–Landau–Masanes arcsine criterion |
| `plane_spectrum` | discrete Fourier magnitudes of a list of probe counts, the smallest period dividing the list, the empty entries | — |

## Rules kept by every experiment

* Engine untouched; initial data and one of the eight sign triples only; nothing acts after t = 0.
* The complete state is used only for construction and integrity (inverse, hashes); physics is read from clicks.
* Detectors and windows are declared from the source researchers' pre-registered rules, before decoding. A window
  changed after registration is disclosed in `detectors.json`, on the card and in the check text (E16: the
  farther-mirror back windows, R10H-6).
* Controls are included; wherever birth, creation or locality is claimed the run is repeated on 2L.
* Wording: candidate names, "click-front speed", board-time versus click-time stated whenever click-time is used.

## Provenance

The manifests were built by the program's builder (`research/matter_light_v1/r01b/build_experiments.py`, program
record) from the researchers' init files and the published blocks; each run names its source file and SHA-256. E02,
E03, E04 and E06 shipped init files until e12a9c3; they are now compositions with every initial-state, final-state
and log hash unchanged. The verifier needs only `universe24`, `research.components`,
`research.matter_light_blocks_v1` (blocks and registry) and `research.click_decoder_v1`.

Manifests may carry four informational keys that the verifier ignores: `builder` (how the composition or init files
were made), `built_utc`, `composition_note` and `data_bytes`. A path under `research/matter_light_v1/` there, in this
README or in the package's test file names a file of the program's working folder, archived uncurated on branch
`backup/matter-light-working` at commit 2483837 unless the path names a later archive commit; nothing there is needed
to verify an experiment. The compositions of E07 and E07b are also produced
exactly by the registry builders `sce_e07_spec` and `sce_e07b_spec` in `research.matter_light_blocks_v1.registry`.

### Theorems cited

A THEOREM label on a card cites a proof in the program record, refereed there; the proof is not repeated here. The
paths below are relative to `research/matter_light_v1/` on branch `backup/matter-light-working`, at the commit named
in the last column (7aac8c5 is a later snapshot of the same folder).

| label on the cards | proof or review | commit |
|---|---|---|
| gate law [THEOREM, r08] (E02, E03) | `r08/REPORT.md` §R3, "Gate theorem"; stated in `chapters/CLOCKS.md` §1, where the 1-bit record after an absorption is [SIMULATION]; referee R08-2 and R08-3 in `r10/REVIEW.md` | 2483837 |
| r12 Theorem 7 (E07) | `r12/CLICKTIME_THEORY.md` §2.6 | 2483837 |
| r12 Theorems 12 and 13 (E07b); Theorem 10 (E07b; R10E-9 PARTLY: its clause (c) is false as stated) | `r12/CLICKTIME_THEORY.md` §7.2 and §6; `r10/r10e_REVIEW.md` | 2483837 |
| r13 G0, carry-free gates only (E07) | `r13/NOTES.md`, the entry "G0 [THEOREM, no run]"; its scope: R10E-2 | 2483837 |
| THEOREM FF (E10) | `r22/REPORT_WAVE2.md` §3 | 2483837 |
| r23 Lemma 2, s − 4 = R (E16) | `r23/NOTES.md`, the 02:20 theory record | 2483837 |
| time reversal F⁻¹ = JR∘F∘JR (E15, E15b, E17, E18, E19, E20, E20b) | `chapters/THEORY.md`, row S6; proved as Lemma 1 in `r36/REPORT_WAVE1.md` §1 | 2483837; 7aac8c5 |
| two moments make the history periodic (E15, E18, E19, E20, E20b) | `r36/REPORT_WAVE1.md` §1 | 7aac8c5 |
| the planar box period 4d + 4 (E15b) | `r18b/REPORT_WAVE1.md`, first section | 7aac8c5 |
| the exact bounce of a JR-fixed s* (E17) | `r27b/REPORT_WAVE3.md`, breakthrough 1 and §1 | 7aac8c5 |
| exact light on the body diagonals, the discrete d'Alembert law at c_s = 1/√3 [THEOREM, r03 L4; r25] (E11) | `r03/REPORT.md`, finding 2 (u a multiple of 3 on the planes n = x + y + z); `r25/REPORT_WAVE2.md` | 2483837; 9f9cc64 |
| r25 T8 (c_b = c_s is never exact) and V (no amplitude-scaling vertex) (E11) | `r25/REPORT_WAVE1.md`, T8 and V | 2483837 |
| r18 T1, T2 (interaction only at a carry), T4 and T7 (E12, E13) | `r18/REPORT_WAVE1.md`, T1, T2 and T4; `r18/NOTES.md`, the 02:57 entry (T7) | 2483837 |
| guide lemma (r04) (E13) | `r04/NOTES.md`, "Guide lemma" | 2483837 |
| the contact count (192/r)², by central projection (E13) | `r33/REPORT_WAVE1.md`, finding 1 | 9f9cc64 |
| r26 T1, T3, T4 and NB (E14) | `r26/REPORT_WAVE1.md`, T1, T3, T4 and NB; NB's scope: R10G-61 | 2483837 |
| b = 0 on every channel gives S_t+1 = JR(S_t), one empty update (E14) | `r26b/REPORT_WAVE1.md`, first item; referee R10G-87 | 9f9cc64 |
| referee ids R10E-n | `r10/r10e_REVIEW.md`, "Verdicts (R10E-\*)" | 2483837 |
| referee ids R10G-35, R10G-36 (E11) | `r10/REVIEW_R10G.md` | 9f9cc64 |
| R10G-46..61 (E13, E14) | `r10/REVIEW_R10G_W2.md` | 7aac8c5 |
| R10F-n; R10G-74..88; R10H-1..8; R10H-29..31 | `r10/REVIEW_R10F.md`; `r10/REVIEW_R10G_W3.md`; `r10/REVIEW_R10H.md`; `r10/REVIEW_R10H_W2.md` | 7aac8c5 |
| R10G-111..120 (E19) | `r10/REVIEW_R10G_W4.md`, §1 | bf2313b |
| remote referee reports FRESH4, FRESH6 and FRESH8 | `remote/FRESH_MACHINE_REPORT4.md`, `remote/FRESH_MACHINE_REPORT6.md`, `remote/FRESH_MACHINE_REPORT8.md` | 7aac8c5 |
| remote referee report FRESH11 (E19) | `remote/FRESH_MACHINE_REPORT11.md` | 678258e |
| R10R-0..13 (E20, E20b): builder D's report 5 and its files | `r10/r10r_REVIEW.md` (pre-registration `r10/r10r_NOTES.md`); `remote/BUILDER_D_REPORT5.md`, `remote/builderD_R5/` | 96b1c0f |
| remote referee report FRESH19 (E20: builder D's report 4, two different boards) | `remote/FRESH_MACHINE_REPORT19.md` | 96b1c0f |
| R10ZB-1..19 (E21): r64's observer and its E09 / E10 readouts | `r10/REVIEW_R10ZB.md`; r64's `r64/NOTES.md` (P1, P4, P17) and `r64/REPORT.md` | 13d4fa9 |
| remote referee report GRF2 (E21) | `remote/FRESH_MACHINE_REPORT_GRF2.md` | 13d4fa9 |
| remote referee report GRF5 (E21 reproduced) | `remote/FRESH_MACHINE_REPORT_GRF5.md` | 405aded |
