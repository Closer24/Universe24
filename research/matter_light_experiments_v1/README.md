# Matter and light experiments (curated, v1)

Each experiment here shows one result of the matter/light research program on the unchanged reference model. It
is **data**: init files in the official format or references to published blocks, declared detectors, and a card.
One generic verifier replays every run natively with the exact inverse, writes the official click log, and reads
every claim **only from the frozen click decoder's report** (`research/click_decoder_v1`). There is no
per-experiment code.

Names such as "light", "matter", "atom", "clock" and "charge" are **candidate names for click patterns** of this
model. No physical photons, mass, charge, spin-1/2, gravity or quantum behaviour is claimed. `C2` is not a selection
law and `Q` is not energy (AGENTS rules 10 and 12).

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
| [E16](E16_bigbang_backward_v5/CARD.md) | Big Bang candidate v5, built backwards: created light, two created ring clocks (36, 22), one gate decision, a matched α_in = 1 instrument pair and a radar echo, from a 14-cell seed | (−,+,+) | SIMULATION | 20 of 20 pass | r10h R10H-1..8 PARTLY (1, 3, 4, 7 CONFIRMED) | ~2 min |
| [E17](E17_exact_bounce_v6/CARD.md) | an exact bounce: one JR-fixed state s* whose contraction and expansion are mirror images in the clicks (0 of 49,830 records unpaired), on L and 2L | (−,+,+) | THEOREM + SIMULATION | 12 of 12 pass (7 decoder, 5 log_symmetry_v1) | remote FRESH4-A1..A3 CONFIRMED | ~2 min |

E01's twin runs reference the blocks appended to `research/matter_light_blocks_v1` in dff39dc. Like E01, E07b's run
a_A references a published block (`exact_front_111_box`).

Decoder pin: `click_decoder_v1` 1.0, frozen 2026-11-09T01:29:27Z (`research/click_decoder_v1/FROZEN.json`). E17
also pins the frozen layer log_symmetry_v1 (release 1.0.3). An
experiment is **ready** when every declared check passes on the decoder report and the referee's verdict is recorded.

## Commands

```sh
python -m research.matter_light_experiments_v1.verify E01_local_atom_twins E02_clicktime_chsh E03_exclusive_detection \
    E04_einstein_created E06_moving_clocks E07_sce_collapse_entanglement E07b_sce_superposition_interference \
    E09_einstein1911_clicks E10_prescribed_schwarzschild_lattice E16_bigbang_backward_v5 E17_exact_bounce_v6 \
                                                                                # every one "ready": true
python -m research.matter_light_experiments_v1.verify --all                     # every experiment folder present
python -m research.matter_light_experiments_v1.verify --fast                    # only the runs marked fast
python -m research.matter_light_experiments_v1.verify E04_einstein_created --keep runs/exp   # keep logs and reports
python -m unittest tests.test_matter_light_experiments_v1                       # fast test
```

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

* `coupling`: `{"kind": "reference", "signs": [..]}`; every run must have exactly this triple.
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
  `best_tau`, `period`, `c_image`, `record_diff`) and `beat_clock_v1` (`run_declared`). Each is frozen by
  `research/click_decoder_v1/FROZEN_<name>.json`, which names the layer's file and its SHA-256, and the manifest
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
* Detectors and windows are declared from the source researchers' pre-registered rules, before decoding.
* Controls are included; wherever birth, creation or locality is claimed the run is repeated on 2L.
* Wording: candidate names, "click-front speed", board-time versus click-time stated whenever click-time is used.

## Provenance

The manifests were built by the program's builder (`research/matter_light_v1/r01b/build_experiments.py`, program
record) from the researchers' init files and the published blocks; each run names its source file and SHA-256. The
verifier needs only `universe24`, `research.components`, `research.matter_light_blocks_v1` (blocks and registry) and
`research.click_decoder_v1`.

Manifests may carry four informational keys that the verifier ignores: `builder` (how the composition or init files
were made), `built_utc`, `composition_note` and `data_bytes`. A path under `research/matter_light_v1/` there, in this
README or in the package's test file names a file of the program's working folder, archived uncurated on branch
`backup/matter-light-working` at commit 2483837 unless the path names a later archive commit; nothing there is needed
to verify an experiment. The compositions of E07 and E07b are also produced
exactly by the registry builders `sce_e07_spec` and `sce_e07b_spec` in `research.matter_light_blocks_v1.registry`.
