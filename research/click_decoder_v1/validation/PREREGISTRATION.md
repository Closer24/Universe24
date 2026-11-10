# Pre-registration and freeze record of click_decoder_v1 v1.0

Copied verbatim from the researcher's notes (r17), where the full development log is kept.
Times are UTC, 2026-11-09.

## 01:00 — PRE-REGISTRATION (written before any decoder code exists and before any validation log is decoded)

### Rule being implemented (UPDATE 8, binding)
Physics is read only from click logs. The decoder reads the official
`python -m universe24 --events` JSONL (or a read-only observer log in the same
record form). From each record it keeps only `step`, `address`, `kind`,
`quotient`; the state fields `before`/`after` are discarded at load time. The
only other inputs are the board side and the horizon, declared by the experiment
(command-line or API arguments); nothing is read from init files or states.

### Development set (logs I may look at while writing the decoder)
Seen before this note, only as raw click listings (no decoder output exists):
`I6_impulse`, `D5_dimer`, `mover_v2of6_sp_guide02`, `fiber_x_packet`,
`atom_trap_d6`, `ring16`, `lamp_pmm_bg4_core10`, `bigbang_C3_seed_pmm_bg4`,
`crystal_light_matter_L8`, `crystal_light_and_matter`, `diag_sheet` (timing only),
plus synthetic logs written by the unit tests. These blocks stay in validation set A;
their scores are also reported separately as "dev (seen)".
I have read r08's wave-6/7 reports, so set B is not blind for me: its outcomes
under r08's analysers are known. I will not run my decoder on any set-B or set-C
log before the freeze.

### Validation set A — catalog blocks (declared truth from `research/matter_light_blocks_v1/catalog.json`)
Catalog SHA-256 `465c080634253134cd027018560430eca4c2211f6699d68795abdb319a508263`
(format `matter_light_blocks_v1-catalog-1`, built 2026-11-09T00:35:40Z).

* **Selection rule:** every entry with `heavy = false` whose signature declares at
  least one of `period`, `translation`, `silent`, or that has `box_checks`.
  Count at registration: **194 blocks** (P 129, P+silent 36, P+T 11, T 10, box 5, silent 3).
* **Logs:** official CLI, `python -m universe24 --config BLOCK --steps H --events LOG`,
  written under `runs/click_decoder_v1/` (gitignored); the SHA-256 of every log is stored.
* **Horizon rule H (fixed now):**
  box checks: `H = steps`; silent with a period: `H = max(steps, 24)`; silent without a
  period: `H = steps`; period P: `H = min(max(steps, 4P, 24), 480)`;
  translation (T, shift) without period: `H = max(steps, 4T, 24)`.
  A declared state period P stays exact for all later times, and so does a declared
  translation, so extending the horizon keeps the truth valid.
* **Decoder inputs:** `--side` = the catalog side, `--horizon` = H. Nothing else.
* **Truth at click level (logical consequences of the declared state signature):**
  - period P ⇒ the click log is exactly P-periodic from update 1. Any exact minimal
    period the decoder reports on a long enough window must divide P.
  - The **reference click period** p_ref = the smallest divisor d of P such that the
    whole log is d-periodic on [1, H] (a brute-force definitional check in `score.py`,
    not decoder code). p_ref < P happens when part of the state is dark or the
    states differ invisibly.
  - translation (T, shift) ⇒ the log at t+T equals the log at t shifted by `shift`
    (mod L). Truth velocity = shift/T (exact rational vector).
  - silent ⇒ zero clicks ⇒ the decoder must report zero objects.
  - clicks_per_period / kinds_per_period ⇒ totals over one period P.
  - box `periodic` (P, from, to, sites) ⇒ clicks at those sites are P-periodic on the
    window: an atom candidate. box `c_image` (lap T) ⇒ after one lap the clicks equal
    the original with channels relabelled g → 14·g: site pattern repeats after T,
    channel pattern only after 2T.
* **Metrics (set A):**
  - **A-P recall:** blocks with a declared period, not silent, and identifiable
    (H ≥ 3P): fraction where lcm(periods of the decoder's sources) == p_ref (exact).
    Also reported: == P, and p_ref == P (how often clicks show the full state period).
    Non-identifiable blocks (H < 3P) are listed and counted separately as misses.
  - **A-P precision:** over all sources the decoder reports in identifiable period
    blocks: fraction whose period divides P (a non-divisor is provably wrong).
  - **A-P coverage:** fraction of events owned by sources in those blocks (expected 1.0).
  - **A-T recall:** translation blocks: fraction where some decoder track (free track or
    motion inside a source) has exact velocity == shift/T.
  - **A-T precision:** over all decoder tracks with an exact velocity in translation
    blocks: fraction equal to shift/T.
  - **A-LM:** translation blocks: light/matter class correct (L1 speed 1 → light
    candidate, < 1 → matter candidate).
  - **A-S:** silent blocks with zero decoder objects.
  - **A-K:** blocks with clicks_per_period / kinds_per_period: the decoder's sources,
    scaled to the declared period, reproduce the declared totals.
  - **A-B:** box `periodic`: a decoder source with period == box P within Chebyshev 4
    of the box-site centroid, flagged `created`; box `c_image`: a decoder source within
    Chebyshev 4 of the ring whose channel period == 2 × site period.
  - Composites, lamps and emissions on set A: descriptive only (the catalog has no
    object-level truth for them).

### Validation set B — r08's wave-6 test set (object-level truth)
* Logs: r08's official CLI logs in `runs/matter_light_v1/r08/clicklogs/`
  (`chamber_L26`, `trap_d6`, `pair45`, `HL22_dimer_monomer`, `HL22_like_pair`,
  `C3_lamp_L81`, `flagship_v2`, `dark_M4_far`, `crystal_g17`; extra: `crystal_g17_36`),
  SHA-256 stored. Side and horizon from r08's CLI summary files (`side`,
  `completed_steps`; nothing else is read from them).
* Truth: r08's post-hoc reference truth (`r08/clicks_truth.py: reference()` with its
  dark rule), snapshotted once into `validation/r08_reference.json` with r08's file hashes.
* Matching: r08's declared criterion: same family, time overlap ≥ 50 % of the shorter
  life, Chebyshev ≤ 4 at the middle common update; one-to-one, visible objects first,
  nearest pairs first.
* Families: light (free track, L1 speed ≥ light threshold or front), matter (other free
  movers), source (decoder sources), bound (sources flagged composite), created
  (objects flagged created).
* Metrics: per family TP/FP/FN, precision, recall (all), recall (visible), periods of
  matched sources vs truth periods; compared with r08 v1/v2 (W6 tables).

### Validation set C — the dark layer (declared observer log)
* Logs: r08's wave-7 change-observer logs `runs/matter_light_v1/r08/observers/<case>.C.jsonl`
  and native logs `<case>.N.jsonl`. The ℓ = 0 layer is the click-log difference
  C minus N on (step, address) (exact by r08's theorem O_N = O_L ∩ O_C).
* Truth: the set-B reference objects at rest that are dark in the native log.
* Metrics: recall of dark objects at rest by decoder sources in the ℓ = 0 layer
  (same matching rule, family "source"); precision of ℓ = 0 sources against all
  reference objects at rest.

### Correlations
No catalog truth exists. Validated only by unit tests on synthetic logs with exact
expected joint counts.

### Freeze protocol
* v1.0 is frozen **no later than 03:45 UTC**, before any set A/B/C log is decoded for
  scoring. At freeze the SHA-256 of every decoder source file and of `config_v1.json`
  is written to `FROZEN.json`.
* Scores are computed only with the frozen version. Any later change is v1.x, must
  be re-run on all of sets A, B, C, and both result files are kept.

## 01:29:27 — v1.0 FROZEN
`FROZEN.json` holds the SHA-256 of `decoder.py`, `correlate.py`, `config_v1.json`.
Scoring starts now with this version; the scorer refuses to run if the files differ.

## 01:31 — catalog changed under me (no effect on the truth)
The first scoring attempt (01:29, PID 5855) stopped at the input check: `catalog.json` now has
SHA-256 `c9039cd9…`, from commit 17c7588 (architect tidy, 01:26). Field-by-field comparison
with the registered version (8301320, `465c0806…`): the only difference is the `what` text of
`band_bigbang_W3A` (heavy, not in set A). name, group, file, file_sha256, side, steps, heavy,
signature, box_checks and final_state_sha256 are identical for all 338 entries. The scorer
now accepts exactly these two hashes. The decoder is unchanged (still the frozen v1.0).
The same commit notes 21 entries in 10 groups of repeated preparations; I add a labelled
post-hoc view over distinct logs next to the registered metrics (which stay as registered).

## 01:40 — PRE-REGISTRATION of held-out set D (before any decoder run on it)
r08's three trap-atom logs, never decoded by me and not in sets A–C:
`runs/matter_light_v1/r08/clicklogs/spectro_d{6,10,14}_atom_alone.jsonl`
(SHA-256 8ec29c6c…, dba3e1d5…, dcc43ca7…; side 420; horizons 163, 195, 227 from the CLI
summaries). Truth (r08 W6/W7, r04 trap theory): one atom candidate per log, a packet
between two dark cores with level period 2d + 4 = 16, 24, 32.
Metric: the decoder reports a source with period exactly 2d + 4 that is flagged composite;
reported for v1.0 and for any v1.1. Also listed: other objects reported.



---

# Decoder v1.1 (copied verbatim from the researcher's notes)

# WAVE 2 — decoder v1.1

## 01:53 — PRE-REGISTRATION v1.1 (written before any v1.1 code; v1.0 files untouched)

### Layout
v1.0 stays byte-identical (`decoder.py`, `correlate.py`, `config_v1.json`, `FROZEN.json`).
v1.1 = `decoder_v11.py` (imports v1.0's unchanged primitives) + `layers.py` (click-log -> click-log
transforms: `diff`, `peak`) + `config_v1.1.json` + `FROZEN_v1.1.json`. CLI: `--version 1.0|1.1`
(default 1.0, so every claim made with v1.0 reproduces with the same command).

### Change list
(i) C-image lap test. Fixed table C: g -> z.g, z = 14 (48 entries, in the config; a test checks it
    against universe24.core.group_2o; only the test imports universe24). For a source with
    channel-free period p0 < period p, test rec(t + p0) == C(rec(t)) on its channel-resolved record;
    report lap, laps verified (>= 3 lap-to-lap relations to accept), window, 720-degree return.
    Sites that are not fully periodic but satisfy the C relation for >= 3 laps also enter sources
    (period 2 x lap, basis "c_image").
(g) Track splitting at velocity changes: a track born by a split from a parent gets back the
    parent's earlier sites that lie on its own back-extrapolated path (nearer to it than to the
    parent's path), down to the real split; it is born there, from the parent.
(h) (h1) the arm walk stops at feeding cycles (circulation is never an arm; v1.0 could walk round a
    ring and delete it); (h2) a site that is not periodic gets a second test with the clicks of
    passing movers (net displacement >= 6) removed; sites periodic in the first test are untouched.
(j) `layers.peak`: r14's peak_arrival_click_v1 exactly as specified (w = 8), as a layer transform;
    an `arrival_map` in every report (first click per site: radial and plane-wave fits, directional
    speeds along axis / face / body diagonals); class "c-light" when the caller declares c
    (`--c`): Euclidean speed within `c_light_rel_tol` = 1 % of c; consistency across directions
    reported.
(a) site period = the period whose exact run explains the most updates, ties to the smallest p.
(b) "translating" only if the internal translation holds for >= one full source period.
(c) co-moving merge only for tracks born within `link_gap` updates of each other.
(d) space-time connected free tracks whose union is an exact co-mover over >= 80 % of its span
    become one track.
(e) exact-motion cap 4000 -> 60000 events per update; candidate shifts include every v with
    |v|_1 <= T for T <= 4 (sheet co-movers: a board-wide sheet has no meaningful centroid), with a
    sampled pre-check (architect P1).
(f) empty-log summary with the same keys as a non-empty one.
(P2) reports record the log's file name and SHA-256, not its path.
(P6) the two inline constants of v1.0 go to the config: prediction window 6 observations,
    velocity search box +-1 site.
Not in v1.1 (proposed for later): r14's Einstein-protocol module; a k-detector coincidence-class
histogram. For r01b's "alpha" I prefer a pure function of the decoder's pair counts,
alpha = (n10 + n01) / (n11 + n10 + n01), documented and tested in r01b's package.

### Acceptance rules (v1.1 versus v1.0, sets A-D as registered at 01:00/01:40)
* Floors: A period identity >= 123/135; A source-period precision >= 0.89; A velocity precision
  18/18 (all exact velocities correct); A silent 39/39; A created-atom boxes 5/5.
* No other regression on A-D, except these declared tolerances: set-B light precision may fall from
  1.00 to >= 0.90 and matter precision to >= 0.80 (more tracks are reported); set-C one-to-one dark
  recall must stay >= 8/34.
* Expected improvements (predictions, not floors): A period identity, A velocity recall (3/7, 1/2,
  5/11, 5/13, the planar glider), set-B light recall (rays no longer merged), set-D composites 3/3.
* If a rule fails, v1.1 is still frozen and reported, labelled as failing that rule, and v1.0 stays
  the reference.

### New held-out targets (declared before any look at the logs; truth from the owners' reports)
H1 r06b flagship v3 (`runs/matter_light_v1/r06b/logs/`, side and horizon from the init files):
   skeleton_main_L160/256/320/512 (T = 240; sha 9361148c, a74b05bc, d51aa3cb, 288274a1),
   twins_far_main_L256/512 (T = 300; a547d10a, 1f2a7384), control skeleton_no_ring_L160 (dd152caa).
   Q1 (glider split): on each skeleton board, two matter tracks with exact velocity (0, +1/3, 0)
   and (0, -1/3, 0), both born at t <= 45 within Chebyshev 4 of (13, 0, 3); the +y member is not
   part of a light track. Q2 (spin ring): a source with a verified C-image lap of 18 (>= 3 laps)
   within Chebyshev 6 of (15.5, -20 mod L, 5) on all four skeleton boards and both twins_far
   boards; laps verified reported (truth: laps from t = 96: 6 on L = 160, 7 on 320, 8 on 256/512).
   Control: no C-image source near the ring site in skeleton_no_ring_L160.
H2 r15 D2J (`runs/matter_light_v1/r15/d2j/`, 5 logs; side 200; horizons t_q + 64): with r15's
   declared detector spec (r15's `d2j.det_spec`, written once to JSON) the decoder's correlation
   counts equal r15's recorded counts in every window (approval, quantum, afterpulse): the
   selected arm has exactly 2 clicks (C1 + C2), afterpulse 0. Turning back (app1_lam0): a light
   track with exact velocity (-1, 0, 0) born within 3 sites of (90, 100, 99) at t in [45, 49],
   origin emitted, and a light track with exact velocity (0, -1, 0) born near y = 120 at
   t in [89, 93]. D2 (34 logs): descriptive only.
H3 r14 peak-arrival light (`runs/matter_light_v1/r14/`): (a) `layers.peak` on each
   w2_v2_chain_{100,110,111}_amp1e+06_staircase.clicks.jsonl equals r14's
   *.peak_arrival_v1.jsonl record for record; (b) decoding each staircase peak layer with
   c = 1/sqrt(3): the main track (most clicks) is class c-light, Euclidean speed within 1 % of c,
   in 3/3 directions, consistent across them (truth: 0.57602, 0.57669, 0.57735);
   (c) the chain line logs decoded the same way give 0.576, 0.8156, 1.000 sites/update (line
   placement compresses (110), (111) by the plane spacing), within 1 %; V1 native line logs:
   descriptive.
H4 set A's identifiable c-image box: d1_skeleton_atom_spin_clocks_L160 (lap 18, 7 laps from 97,
   ring box centroid (15.5, 140, 5)): a source within Chebyshev 4 with a verified C-image lap 18.
H5 planar Big Bang (architect P1): research/matter_light_blocks_v1/blocks/seeds_big_bang/
   planar_bigbang_L16.json (sha 51f879a2), CLI logs at the declared 14 updates and at r16's 18.
   Truth: two board-wide sheets born at t = 4 next to the seed plane x = 8, moving with exact
   velocities (-1/2, 0, 0) and (+1/2, 0, 0) (planar profile in the catalog). Pass: two tracks with
   these exact velocities, class matter (on h18 the sheets meet across the torus after t = 14).

## 01:59 — PRE-REGISTRATION ADDENDUM v1.1 (before any v1.1 run on any log)
Additions to the change list (from the coordinator's later messages; generic rules only):
(g+) besides the registered backdating, a track whose path has pieces of different constant velocity
     (each >= 6 observations, velocities differing by >= 0.15, each piece fitting within 0.75 site
     RMS) is split into one track per piece, the later piece born from the earlier one (the
     coordinator's item 1: a glider merged into a light track).
(k) lamp rule: an emitted track counts for a lamp only if it ends >= 8 sites (Chebyshev) from every
     core site (it leaves); a trap atom's packet legs are not emissions.
(l) passages: for each declared detector region, every free track's first and last click inside it
     (generic; any calibration such as r14's +6 offset stays with the experiment).
(m) the difference layer (main minus a declared control run, on (step, address)) is layers.diff.
(c-light) class "c-light" for a declared c (already in (j)); r14's Einstein module: later.
Additional held-out targets (truth from the manifests in research/matter_light_experiments_v1/;
logs from the official CLI at the manifest horizons, checked against the manifests' log_sha256):
H6 E01: the manifest's decoder checks E01-1..15 (incl. E01-13: two period-20 sources whose births
   differ by 12 updates), evaluated on v1.0 and v1.1 reports.
H7 E05: E05-1 two exact sheet movers +-1/2 from t = 4 (planar_bigbang_L16, 14 updates); E05-2 the
   planar glider alone, exact 1/2 (planar_glider_100, 24 updates); E05-3 kinds C2 only.
H8 E06: E06-4 exact speeds include 1 and 1/2 (v1of2 run, 220 updates); same with 1 and 1/3 for the
   v1of3 run (308 updates, declared v = 1/3); E06-5 the no-glider control is silent. E06-1/2 (round
   trips) need rung detectors that the manifest does not declare: descriptive only.

## 02:01 — PRE-REGISTRATION ADDENDUM 2 v1.1 (r24's request; before any v1.1 run)
(n) quotient field (r24's quotient_field_v1, research/matter_light_v1/r24/observer.py): for a declared
    window [t0, t1], per site the signed sum of quotients; Qbar = sum / (48 (t1 - t0 + 1)); with a
    declared centre, the shell profile (Euclidean shells rounded to integers, empty sites counted in
    each shell's population) and a least-squares fit a/r + c over the declared r range. Written as
    a field file by `layers.quotient_field` and summarised in the report when a window is declared.
    Projection layers (r24's g0/box/ray): documented input convention, no code.
H9 r24: (Qa) for every log in runs/matter_light_v1/r24/events/ (centre (L//2, L//2, L//2), window
    [1, last step]), v1.1's per-site sums and shell profile equal r24's quotient_field() exactly.
    (Qb) the a/r + c fit is reported descriptively (no truth value for these small boards).

## 02:02 — v1.1 development note (before freezing; no held-out log decoded yet)
A synthetic unit test (a track at Euclidean speed 0.577, one site per update) was labelled
"exact speed 1": `_exact_motion` (v1.0 and draft v1.1) accepts any exact sub-run of 3 periods.
Fix in v1.1 (same principle as (a)): the exact run must also cover >= 80 % of the track's click
updates (`exact_min_coverage` 0.8). v1.0 keeps this flaw; it is documented as a v1.0 limit.

## 02:00–02:07 — v1.1 development on seen logs only (dev logs, non-held-out set-A logs)
* (d) as first coded linked only sequential fragments; the guided 3/7, 1/2, 5/11, 5/13 movers have
  fragments that overlap in time, so overlapping fragments close at a common update (<= 6 sites) are
  linked too ("space-time connected", as registered). Result on those seen logs: exact 3/7, 1/2,
  5/11, 5/13 (v1.0: none).
* NEW, added before the freeze (not in the 01:53 text): exact-run segmentation (g++). A mover without
  an exact velocity over 80 % of its clicks but with an exact run of >= 6 updates is cut at the ends
  of that run; each exact segment is its own track, born from the previous piece. Found on the dev
  block junction_emission_d1, where the coverage rule had removed v1.0's exact packet speeds.
* Seen-log effects: HL22 single period-22 composite; trap d10 composite kept; (111) front box period 6;
  spinor_ring_r09 and spin720_ring C-image laps 24 and 14; fiber_light_creates_glider: incoming light
  +1, reflected light -1 and glider 1/3 as three tracks (v1.0: the two lights fused);
  fiber_glider_becomes_light: glider -1/3 then light -1 (v1.0: one light track).
  Torus-wrapped dev lamps get extra slow tracks after their wrap bound (flagged after_wrap_bound).
* Smoke run over 189 set-A logs (held-out blocks excluded): no crash, 92 s, peak RSS 0.35 GB.
* Unit tests: tests/test_click_decoder_v11.py 12/12, tests/test_click_decoder_v1.py 12/12.

## 02:07:53 — v1.1 FROZEN (`research/click_decoder_v1/FROZEN_v1.1.json`)
Hashes of decoder.py (v1.0's file, unchanged), decoder_v11.py, layers.py, correlate.py,
config_v1.1.json. v1.0's three hashes re-checked equal to FROZEN.json. Scoring starts now.


## 02:22 — PRE-REGISTRATION ADDENDUM 3: quotient-sign layer (r20), outside the frozen v1.1 core
v1.1 is frozen; its files are not touched. A separate declared observer layer `sign_split_v1` (r20's
definition, research/matter_light_v1/r20/phase_element.py) goes into a new file
`research/click_decoder_v1/sign_layer.py` (CLI `sign`), frozen on its own (`FROZEN_sign_split_v1.json`)
before it is run on r20's logs. Rule: layer P = the records with quotient > 0, layer M = quotient < 0,
each record kept verbatim; a layer is decoded on its own.
H10 r20 cos^2 element (runs/matter_light_v1/r20/phase_element/ and phase_element_cli/; truth: r20's
phase_element.json, 34 settings, every count exact, plus the CLI log's 280 / 0 / 3): (a) my P and M
layers equal r20's .P/.M files byte for byte; (b) decoding each layer with v1.1 and r20's saved
detector declaration (one detector per comparator, window [1, 1]) gives r20's counts (+, -, 0, both)
in 34/34 settings and 280 / 0 / 3 on the CLI log.

