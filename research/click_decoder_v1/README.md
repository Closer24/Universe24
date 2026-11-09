# Generic click decoder v1

One decoder, frozen and versioned, that reads **only click logs** and reports what can be
seen in them: tracks with speeds, periodic sources (clocks, lamps), bound or periodic
composites, emission and creation events, spectra, kind statistics and joint statistics
of declared detectors. Under the owner's rule (BRIEF UPDATE 8) every physics claim must
come from this decoder's output, run unchanged on the experiment's click log, with the
decoder version recorded. The board itself is not read.

Standard library only. Nothing here runs or changes a board; the decoder never imports
`universe24`. Names such as "light", "matter", "lamp" and "atom" are candidate names for
click patterns, not claims about physical photons, mass or atoms.

## Quick use

```sh
python -m universe24 --config research/matter_light_blocks_v1/blocks/atoms/atom_trap_d6.json \
    --steps 64 --events runs/trap.jsonl
python -m research.click_decoder_v1 decode runs/trap.jsonl --side 96 --horizon 64 --out runs/trap.report.json
python -m research.click_decoder_v1 diff C.jsonl N.jsonl --out L0.jsonl     # change-observer l = 0 layer
python -m research.click_decoder_v1 decode L0.jsonl --side 96 --horizon 64 --layer change_l0
```

```python
from research.click_decoder_v1 import read_log, decode, chsh
events, info = read_log("runs/trap.jsonl")              # keeps step, address, kind, quotient only
report = decode(events, side=96, horizon=64, log_info=info, detectors=None)
print(report["summary"], report["sources"][0]["period"])  # 16, a composite with a zig-zag
```

`--side` and `--horizon` are declared by the experiment (the board side and the number
of updates run). Without `--side` the decoder uses 1 + the largest clicked coordinate
and says so in the report (a lower bound); without `--horizon` it uses the last click
update. `--detectors FILE` adds correlations (format in `correlate.py`).

## Input contract

* The official `python -m universe24 --events` JSONL, or a read-only observer log in the
  same record form (for example r08's change observer, or its l = 0 layer made with
  `diff`). Each layer is decoded separately; layers are never merged.
* From each record only `step`, `address` = (x, y, z, g), `kind` and `quotient` are kept.
  `before`/`after` are state values; they are dropped while loading and listed in the
  report under `fields_ignored`.
* The report records the decoder version, the SHA-256 of every decoder file and of the
  config, and the SHA-256 of the input log.

## Click-only rules (thresholds: `config_v1.json`)

Distances are Chebyshev on the torus unless called L1. "Exact" always means equality of
click records, never a fit.

1. **Clusters.** Per update, connected sets of clicked sites (gap `cluster_gap` = 2).
2. **Tracks.** Clusters are linked over updates: a cluster may continue a track whose
   last cluster was `dt` <= `link_gap` updates earlier and lies within `dt + link_slack`;
   ties go to the cluster nearest the track's predicted (constant-velocity) position. An
   established slow track (>= 6 observations, speed < 0.1) may stay silent up to
   `rest_link_gap` updates and does not jump more than 2 sites from its prediction.
   A cluster that a track wanted but lost starts a new track with that track as parent.
3. **Periodic sites.** A site is periodic with period p if its click record (channel,
   kind, quotient per update) is exactly p-periodic on a run covering at least
   `period_min_reps` = 3 periods (silent updates count; the run is the longest one).
   The smallest such p (<= `period_max`) is used.
4. **Sources.** Periodic sites within `region_gap` whose runs overlap by >= 3 periods form
   a region. **Arms** are removed: a site is *fed* if its channel-free record equals a
   neighbour's record delayed by tau (L1 offset <= tau < period); a feeding chain whose
   end touches clicked non-periodic sites is a train leaving the region (a lamp's rays)
   and is removed back to its first unfed site. Chains that close inside the region
   (circulation on a ring) stay. Each connected remainder is a **source**: period =
   lcm of its sites' periods, checked exactly on the joint record; window, clicks and
   kinds per period, phases, and the period with channel indices ignored. A ratio
   `period / period_channels_ignored` = 2 is the click signature of a pattern whose
   360-degree image differs only by channel relabelling (720-degree return).
5. **Composites.** A source is a **bound/periodic composite** if (a) it has >= 2 parts
   (site groups `centre_gap` apart) with different phase sets, or (b) its per-update
   click centroid oscillates inside one period (range >= 2 sites, >= 2 reversals of
   >= 1 site): the trap atom's zig-zag, a packet pair circulating on a ring. A mover that
   translates through its whole periodic region (a glider wrapping the torus) is
   reported as `translating`, not as a composite.
6. **Free tracks.** Tracks not inside a source. Co-moving tracks (velocity difference
   <= 0.15, overlap >= 80 %, distance <= 6 at every common update) merge into one object
   (for example the head and tail of a packet). Velocity: the smallest exact co-moving
   symmetry (T, v), |v|_1 <= T, with the record at t+T equal to the record at t shifted
   by v over >= 3 periods (channel indices ignored, because guides relabel channels along
   a path); otherwise a least-squares fit, marked `exact: false`. Classes: **front**
   (footprint spread grows by >= 0.7 site/update), **light** (mover with L1 speed >=
   0.85; the causal bound is L1 speed 1), **matter** (slower mover), **local**
   (stationary, >= 12 updates, not periodic), **transient**. A mover has net
   displacement >= 3 and >= 4 observations.
7. **Births, emission, creation.** The seed is the first `seed_steps` = 3 updates with
   clicks and its footprint the sites clicked then. Each object's birth is its first
   click (for a source, the first click inside its periodic run). Origin: `seed`;
   `emitted` (split from a linked track, or an earlier click of another object within
   `emit_radius + dt` sites in the `emit_lookback` = 3 updates before); `isolated` (no
   earlier click in that causal neighbourhood: a birth with no visible cause).
   **Created** (UPDATE 6, positional): born after the seed updates and more than
   `create_radius` = 4 sites from the seed footprint. `after_wrap_bound` marks births at
   or after first click + L/2, when click signals may have met themselves across the
   torus. A **lamp** is a source with >= 2 movers born within 4 sites of its core after
   its birth.
8. **Spectra and kinds.** Source periods, the histogram of inter-click intervals of every
   site, the exact period of the whole record, C0/C1/C2 per object and per period.
9. **Correlations** (only with a declared detector file): per detector, clicks, bins fired
   and kinds; per pair n11/n10/n01/n00, E = <ab> with a, b = +-1, covariance, Pearson r,
   coincidences by lag; per two-sided set-up the +-1 outcome E; `chsh()` combines four
   runs. Which time is used (board updates, or bins of them) is stated in the output.

## Report (main keys)

`decoder` (name, version, code hashes), `input` (layer, log hash, side, horizon),
`summary`, `sources[]` (period, window, sites, parts, composite, internal_motion, lamp,
emitted_tracks, birth), `tracks[]` (class, motion with exact rational velocity, direction,
path, kinds, birth), `events[]` (emission, creation), `spectra`, `kinds`, `correlations`.
The report is deterministic: the same log and arguments give the same bytes.

## Validation: one score table, v1.0 against v1.1

Pre-registrations (v1.0 at 01:00 UTC, before any decoder code; v1.1 at 01:53 with addenda 01:59 and 02:03,
before v1.1 existed) and freeze records: `validation/PREREGISTRATION.md`. Scores: `validation/results_v1.0.json`,
`results_v1.0_extra.json`, `results_v1.1.json`, `results_v1.1_extra.json`, `heldout_v1.1.json`,
`heldout_sign_split_v1.json`.

| set | target / metric | v1.0 | v1.1 |
|---|---|---|---|
| A (194 catalog blocks) | period: lcm of source periods == reference click period (identifiable) | 123/135 | 135/135 |
| A | source periods that divide the declared P (precision) | 152/171 = 0.89 | 143/143 |
| A | exact rational velocity == declared shift/T; precision | 16/21; 18/18 | 21/21; 21/21 |
| A | light/matter class of the mover | 16/21 | 21/21 |
| A | silent blocks with zero objects | 39/39 | 39/39 |
| A | clicks / kinds per period reproduced | 35/38; 16/16 | 38/38; 16/16 |
| A | created atom boxes: period 20, flagged created | 5/5 | 5/5 |
| A | 720-degree boxes | 0/2 | 0/2 |
| B (r08 test set) | light: precision / recall | 1.00 / 0.455 | **0.875 (FAILS rule >= 0.90)** / 0.891 |
| B | matter: precision / recall | 1.00 / 0.70 | 0.80 / 0.80 |
| B | sources at rest: precision; recall of visible objects | 0.75; 6/6 | 1.00; 6/6 |
| B | bound: precision / recall | 1.00 / 0.50 | 1.00 / 0.50 |
| B | created: precision / recall | 0.75 / 0.82 | **0.52 (FAILS rule: no regression)** / 1.00 |
| C (l = 0 layer) | native-dark objects at rest matched one-to-one; covered (post hoc) | 8/34; 33/34 | 8/34; 33/34 |
| D (held out) | trap atoms d = 6, 10, 14: period 2d + 4 exact; flagged composite | 3/3; 1/3 | 3/3; 3/3 |
| held out | r06b flagship v3: created glider pair as two exact +-1/3 tracks (4 boards) | 0/4 | 4/4 |
| held out | r06b flagship v3: spin ring as a C-image source, lap 18 (6 boards) | 0/6 | 0/6 |
| held out | set A 720-degree box (d1 skeleton) | fail | fail |
| held out | r15 D2J: detector counts in 3 windows (5 logs x 3); unselected copy turning back | 15/15; pass | 15/15; fail |
| held out | r14: peak layer equal to r14's (3 logs); c-light on staircase layers; line speeds within 1 % | -; 0/3; 3/3 | 3/3; 3/3; 3/3 |
| held out | r24: quotient field equal to r24's observer (7 logs) | - | 7/7 |
| held out | r20: sign layers byte-identical, counts exact (34 settings; CLI log 280 / 0 / 3) | - | 34/34; yes |
| held out | planar Big Bang: two exact sheets +-1/2 (14 and 18 updates) | 0/2 | 1/2 |
| held out | E05 / E01 / E06 checks (as registered) | 1/3; 15/15; 2/3 | 3/3; 15/15; 2/3 |

v1.0's scores are blind. v1.1's scores on sets A-C are post hoc (v1.0's failures there motivated v1.1); set D and
the held-out targets were blind for v1.1. **v1.1 fails two of its pre-registered acceptance rules** (bold above):
its new velocity-change pieces (light continuing or reflected at a junction) count as extra light tracks, and as
"created" because they are born mid-flight away from the seed. All five floors pass (period identity >= 123/135,
source precision >= 0.89, velocity precision 18/18 or better, silent 39/39, created-atom boxes 5/5). v1.0 therefore
stays the reference and the default; use v1.1 where its gains matter (periods, exact speeds, composites, c-light,
layers) and read its `created` flags together with `origin` and `parent`. The spin ring is in the clicks site by
site (13 of its 14 sites obey lap(n+1) = C(lap n) with lap 18; the junction site does not), but v1.1 tests the C
relation jointly over a source and its arm rule removes ring sites, so it misses it.

**Reruns.** Only set A can be rerun from tracked data: its logs are regenerated from the published init files with
the official CLI. In a clean checkout:

```sh
nice -n 10 python -m research.click_decoder_v1.validation.run logs --sets A                 # set-A logs (official CLI)
nice -n 10 python -m research.click_decoder_v1.validation.run score --sets A                # score set A with v1.0
nice -n 10 python -m research.click_decoder_v1.validation.run score --sets A --version 1.1  # the same with v1.1
```

These commands write only under `runs/click_decoder_v1/` (logs, per-case reports and
`v<version>/results_setA.json`). `score` compares each set with the recorded `validation/results_v<version>.json`
(timing ignored), reports per set whether it is `equal` and whether it `reproduces_recorded` (every recorded value
reproduced; the scorer gained one set-A metric after v1.0's results were recorded), and stops with an error if a
recorded value is not reproduced. Sets B, C and D and every held-out target need the program's local logs
(`runs/matter_light_v1/`, not in the repository); their SHA-256 are recorded in `validation/r08_reference.json` and in
the results files.
Paths under `research/matter_light_v1/` named in this package (provenance, held-out inputs) are files of the
program's working folder, archived uncurated on branch `backup/matter-light-working` at commit 2483837; logs
under `runs/` are local and recorded here by SHA-256 only.

Reproduce all sets (needs those local logs) with

```sh
nice -n 10 python -m research.click_decoder_v1.validation.run logs    # official CLI logs (set A), l = 0 layers (set C)
nice -n 10 python -m research.click_decoder_v1.validation.run score   # sets A, B, C; compared with results_v1.0.json
nice -n 10 python -m research.click_decoder_v1.validation.run extra   # set D, set-C coverage; vs results_v1.0_extra.json
nice -n 10 python -m research.click_decoder_v1.validation.run score --version 1.1   # the same with v1.1 (also extra)
nice -n 10 python -m research.click_decoder_v1.validation.heldout       # v1.1 held-out targets (needs the owners' logs)
nice -n 10 python -m research.click_decoder_v1.validation.heldout_sign  # r20's sign-layer counts
python -m research.click_decoder_v1.validation.table                  # print the tables
python -m unittest tests.test_click_decoder_v1 tests.test_click_decoder_v11
```

`run` writes its scores under `runs/click_decoder_v1/v<version>/`, never into the package. `heldout` and
`heldout_sign` still rewrite their recorded files `validation/heldout_v1.1.json` and
`validation/heldout_sign_split_v1.json`.

Set A uses the declared signatures of `research/matter_light_blocks_v1/catalog.json`
(period, translation, silence, clicks and kinds per period, box checks), pinned through a
fingerprint of exactly those fields. Set B is r08's wave-6 test set with r08's reference
truth (snapshot `validation/r08_reference.json`). Set C is the change observer's l = 0
layer of r08's wave-7 logs. Set D is r08's three trap-atom logs.

## Limits

* **Dark objects are not in the data.** An object that never clicks in a layer cannot be
  found in that layer; this is the point of the rule. 34 of r08's 40 reference objects
  at rest are native-dark. The change observer's l = 0 layer is a separate read-only
  observer; decode it when the experiment declares it. By r08's media theorem the static
  remainder landscape (fibres, crystals, network lines) is invisible to every per-channel
  event observer that is silent in uniform vacua; laws read from clicks are conditional on
  such unseen media.
* **Exactness needs time.** A period p is reported only after 3 exact repetitions
  (horizon >= 3p plus any start-up); a co-moving velocity needs 3 periods T as well.
* **No 360-degree images in v1.0.** v1.0 reports only the ratio of the full period to the period
  with channel indices ignored; it does not test whether one lap is the C image (g -> 14 g) of the
  previous lap.
* **Two constants are inline in v1.0** (not in `config_v1.json`): the predicted position of a track
  uses its last 6 observations, and the exact-velocity search tries every shift within +-1 site of
  the rounded fitted displacement (`round(v_fit T)` +- 1 on each axis).
* **Known v1.0 flaws (found in validation).**
  (1) The smallest period with any 3-repetition run wins, even when a longer period
  explains the whole record: short local runs (three equal updates count as "period 1")
  give spurious periods that need not divide the true one. (2) One leg of a zig-zag that
  moves exactly for 3 updates marks the source "translating", so trap atoms d >= 10 lose
  the composite flag (their period is right). (3) Intermittent movers are cut into
  fragments (exact speeds 3/7, 1/2, 5/11, 5/13 missed). (4) Successive rays of a train
  within 6 sites are merged into one track. (5) Sheets above 4000 events per update get
  no exact velocity. (6) Adjacent clocks within 2 sites form one source.
* **Click periods can be shorter than state periods**: a dark part, or states that differ
  invisibly, shorten the click period. The decoder reports the click period.
* **Torus.** After the wrap bound, signals may meet themselves; such births are flagged,
  and a lamp whose rays wrap becomes one periodic region.
* **Segmentation is heuristic** where objects touch: crossing tracks, junction traffic,
  merged movers, a site passed by two trains (not "fed"), fragments of one mover. Binding
  ("bound composite") is recognised from click structure only; that the binding is caused
  by the interaction needs a declared control run, decoded separately.
* **"Created" is positional** (UPDATE 6). It also fires for fragments re-born mid-flight
  and for torus self-encounters; read `origin`, `parent` and `after_wrap_bound` with it.

## Version 1.1 (`decoder_v11.py`, `config_v1.1.json`, `FROZEN_v1.1.json`)

v1.0 stays byte-identical and remains the default, so every command used for a v1.0 claim reproduces
unchanged. Select v1.1 with `--version 1.1` (CLI) or `decode_v11` (API). v1.1 imports v1.0's unchanged
primitives (geometry, clusters, exact runs, kinematics) and changes these rules (all thresholds in
`config_v1.1.json`):

* **C-image laps (spin).** C: g -> z g with z = 14 is a fixed 48-entry table in the config (a test checks
  it against `universe24.core.group_2o`). A source whose record satisfies rec(t + T) = C(rec(t)) for at
  least 3 consecutive laps gets `c_image` = {lap T, laps verified, window, return after 2T}. Sites that
  are not yet fully periodic but obey the C relation for 3 laps enter sources with period 2T
  (`period_basis: "c_image"`).
* **Tracks split at velocity changes.** A path with pieces of different constant velocity becomes one track
  per piece; a split-born track takes back its share of the shared clusters down to the real split; a
  mover with an exact run of >= 6 updates that does not explain 80 % of its clicks is cut at the run's
  ends. Each later piece is born from the earlier one.
* **Traffic.** Arm walks stop at feeding cycles (circulation is never an arm). A site that is not periodic
  gets a second test with the clicks of passing movers (net displacement >= 6) removed
  (`traffic_clicks_removed`).
* **Periods** are the ones whose exact run explains the most click updates (no more "3 equal updates =
  period 1"); exact velocities must cover 80 % of a track's clicks; "translating" needs a full period.
* **Fragments** that touch in space-time and form an exact co-mover become one track (guided 3/7, 5/11 ...);
  a co-moving merge needs tracks born together (successive rays stay separate); sheets: every shift
  |v|_1 <= T for T <= 4 is tried (a board-wide sheet has no meaningful centroid), cap 60000 events/update.
* **Lamps** count only emitted movers that leave the core (end >= 8 sites away): a trap's bouncing packet
  is not an emission.
* **Light.** `--c C` declares a light speed: tracks within 1 % of C (Euclidean) get class `c-light`, and
  `summary.c_light` checks the speeds across directions (tracks and the arrival map). Every report has an
  `arrival_map` (first click per site: radial and plane-wave fits, speeds along axes and diagonals).
* **Declared detectors** also give `passages`: each free track's first and last click in each region.
* **Reports** carry the log's file name and SHA-256, not its path, and one summary schema.

Layer commands (click log in, derived layer or field out; decode each layer on its own):

```sh
python -m research.click_decoder_v1 peak LOG.jsonl --out PEAK.jsonl          # r14's peak_arrival_click_v1
python -m research.click_decoder_v1 decode PEAK.jsonl --side L --version 1.1 --c 0.57735 --layer peak
python -m research.click_decoder_v1 diff MAIN.jsonl CONTROL.jsonl --out D.jsonl   # difference layer
python -m research.click_decoder_v1 field LOG.jsonl --side L --window 1 72 --centre 80 80 80 --out F.json
python -m research.click_decoder_v1 decode LOG.jsonl --side L --version 1.1 --field-window 1 72 --centre 80 80 80
```

`field` is r24's `quotient_field_v1`: per-site signed quotient sums over the declared window,
Qbar = sum / (48 T), shell profile about a declared centre and an a/r + c fit.

**Quotient-sign layers** (`sign_layer.py`, frozen separately in `FROZEN_sign_split_v1.json`, outside both
decoder cores): r20's `sign_split_v1` writes `PREFIX.P.jsonl` (records with q > 0) and `PREFIX.M.jsonl`
(q < 0), each record verbatim; decode each layer on its own (for example with one detector per gate):

```sh
python -m research.click_decoder_v1 sign LOG.jsonl --out-prefix runs/x/LOG
python -m research.click_decoder_v1 decode runs/x/LOG.P.jsonl --side L --horizon 1 --version 1.1 --detectors DET.json --layer sign_split_v1:P
```

**Projection layers** (input convention): a declared subset of an official log in the same record form,
for example channel 0 only (`g0`), or the sites inside declared boxes. Name it with `--layer`. On a
projection, channel-dependent results (C-image laps, channel periods) are meaningful only if every channel
of the object is kept; box projections cut every object at the box boundary, and nothing outside is visible.

## Versions

v1.0 frozen 2026-11-09 01:29:27 UTC (`FROZEN.json`); v1.1 frozen 02:07:53 UTC (`FROZEN_v1.1.json`, which also
re-records v1.0's hashes). Any v1.x is re-run on all earlier validation cases; the results of every version
are kept (`validation/results_v<version>.json`, `validation/heldout_v1.1.json`).
