# The criteria of Table 3, row by row: what is measured, what the number is, what would refute it, and what each row needs

The criteria runner's table of 2026-09-22, on the model owner's referee
point 6 of the paper ("ask that what is needed be re-run; handle
everything", the Boss's order of about 10:15Z). Written from the current
checkout, `origin/main` at `4028b020b95512e796485d8b3e98522d39f82093`,
and the paper on `claude/paper-owner-review-five` at
`735ee8c81b8615a5a73de45f82cd4724ccf4657c` (its Table 3, `tab:nature`,
carries fifteen rows at this head and at `f7ac7856` alike: 1a, 1b, 2a,
2b, 2c, 3, 4b, 5a, 7a, 7b, 8a, 8b, 8c, 9 and 12; rows 11a to 11c are
named in its text as pinned without a run; the brief's "fourteen" is
read as these fifteen). The sources: the confrontation register
[NATURE.md](../../NATURE.md) (the base `88d843ef`), the experiments
register [EXPERIMENTS.md](../../EXPERIMENTS.md), the worlds' READMEs and
`expectations.json` under `examples/events/`,
[REPLICATIONS.md](../../REPLICATIONS.md), the paper's `NUMBERS.md`,
`RECORD.md` and `checks/`, the readings by type of
[ENGINE.md](../../ENGINE.md), and records 156, 160, 408, 865 and 868 of
[the day's log](../../LOG_2026-09-20.md) (record 883, the order's record,
is not yet on `origin/main`, whose log ends at record 877; the order's
text is taken as given).

The rules this table follows: a detector's click is a measurement and
the only kind compared with nature; a GameBoard reading is a labelled
diagnostic, never pinned or compared; every pin is declared here before
its run; the engine is deterministic, so a click count over B births is
exact (no sampling width: the same u on the same ladders gives the same
cells), and the only width a count carries is the ladder's own grain
(a cell's count within 2 of W x its weight over the total, the rungs'
rounding; BEAM_LAW note 46). Nothing in this table moves a pin, a rule
or a world; a re-run reproduces or refutes, and a number that moved is
recorded beside the old one with the SHA, never in its place. ASCII
throughout; every number labelled DETECTOR (a click, a record line) or
GAMEBOARD (the host's view) or COMPUTATION (the algebra's).

## The counts

| Count | Rows |
| --- | --- |
| Rows complete as they stand (nothing needed) | 7: 1a, 1b, 2b, 2c, 5a, 8c, 9 |
| Rows needing a re-run at head | 6: 3 and 4b (one run serves both), 7a and 7b (one batch), 8a and 8b (one batch); plus 2a after its pin |
| Rows needing more clicks | 0 (8a and 8b: the criterion does not need more clicks; see the rows) |
| Rows needing a pin derived for this world | 1: 2a (derived in this commit, before the run: [slits_huygens_pin.py](slits_huygens_pin.py), [its output](slits_huygens_pin.out)) |
| Rows marked and left to another writer | 1: 12 (series T, being redeclared in the weak field by the chief physicist) |
| Readings NOT MADE | 3 rows of the far lamp (11a, 11b, 11c: an engine key not built) and 4 readings the paper names: the two-way c after a detector; the inverse square's decisive reading (form B, a closed orbit's period at two radii); the moving detector's one-way ratio and the velocity's quantum (the cart build in flight); and the detector reading behind row 8a's width (a lamp at the shell counted between the clicks) |

The cost of everything this table orders: five worlds of seconds each
(rows 3 and 4b: 2 worlds of 400 intervals on 301^3, about 50 s each;
rows 7a and 7b: 3 worlds of 3000 intervals, 13 to 53 s each), three of
minutes (rows 8a and 8b: `j1_lattice` and `j1_source` at the cap 1024,
about 2.5 minutes each; `j2_filter` 5 s) and one of about 22 minutes
(row 2a: `slits_huygens`, 4300 intervals at 0.31 s per interval on the
register's host); about 35 minutes of host time in all, under 30 minutes
per run, so none waits for the Boss's word.

## The rows

### Row 1a. The CHSH sum of a pair, S = 2.75 at N = 64

- **(a) What is measured.** Series L3, `examples/events/amplitude/bell_0_8`,
  `bell_0_24`, `bell_16_8`, `bell_16_24`: one record born at the lamp with
  two arms, each arm read at its party's `sum` set (Alice's and Bob's
  counters at the CHSH labels (0, 8), (0, 24), (16, 8), (16, 24) on the
  circle of N = 64); the click is the gather's chosen cell (oA, oB) per
  record, counted over 64 births (u = 0 .. 63 on the wheel [1, 64]): the
  cells 27, 5, 5, 27 (E x 64 = 44), 5, 27, 27, 5 (-44), 27, 5, 5, 27 and
  27, 5, 5, 27; S = 176 / 64 = 2.75, every marginal 32 of 64. The tool:
  `tools/amplitude_path.py --check` (the gathers' list, DETECTOR);
  `tests/test_amplitude_pair.py` replays the four worlds and sums the
  correlations at every check.
- **(b) Ideal or instrument.** The law's ideal at the registered grain:
  the rungs on the wheel over the cells' weights, a deterministic count
  with no apparatus model; the closed form S(N) = 8 (c_1 + c_1') / N - 4
  (the paper's `checks/s_powers_of_two.txt`), 11 / 4 at N = 64, 181 / 64
  from 512 through 8192.
- **(c) The criterion.** PASS where the reading meets nature's value within
  the stated uncertainty (the register's rule (e), two standard errors):
  |2.75 - 2.42| <= 2 x 0.20 against Hensen et al. 2015 (1.65 standard
  errors above); against the quantum bound 2 sqrt 2 the reading is 0.078
  below. What would refute the row: a count in any cell off its rung
  (the width 1 click at W = 64; none in the replay). The paper's own
  refutation line for the plateau: a CHSH measurement at an uncertainty
  below 1e-4 reading a deficit below 2e-4 or above 4e-4 from 2 sqrt 2; at
  N = 64 the paper says N = 64 and 256 are excluded by Poh et al. 2015
  (2.82759 +- 0.00051; the paper's `checks/s_of_n.txt`, -152 standard
  deviations), so the row's PASS is against Hensen 2015's uncertainty and
  not against Poh 2015's. No statistical width: the 64 births are the
  64 u once each.
- **(d) The number in the paper.** S = 2.75, DETECTOR; the source
  fingerprint `ff5c382d672f` (series L, stage (v), 2026-09-20); replicated
  bit-exact by the Replicator (round 1, the tree `10a9ac6`); at head:
  `tests/test_amplitude_pair.py` runs the four worlds in-process and
  asserts the cells and S at every check that touches the engine (green
  at the engine's last change, PR #813, `e0761893`).
- **(e) What the criterion needs.** Nothing. Cost 0.

### Row 1b. The same sum in the phase-form window, S = 2 exactly

- **(a) What is measured.** The ten A2 worlds of `examples/events/bell/`
  (`a0_b0` .. `a16_b24`, `read`, `fixed`): the counters' clicks under
  each party's phase window (a row's own phase against the counter's
  setting; the bar of 21 with the lamp at x = 10); `chsh_sum` = 2 and
  `primed_sum` = 2 by `tools/bell_chsh.py`; DETECTOR (the counters'
  clicks).
- **(b) Ideal or instrument.** An identity of the window's form: a local
  deterministic response gives the local bound exactly, at any count.
- **(c) The criterion.** FAIL: S = 2 is 2.1 standard errors below Hensen
  2015's 2.42. Nothing refutes a FAIL of this kind: the value is exact
  and count-free; what would move the row is another form of the click,
  which is row 1a.
- **(d) The number in the paper.** S = 2, DETECTOR (registered 2026-09-19
  under the law of events and re-read under the one click, 2026-09-20);
  at head: `bell/a0_b0` and `bell/fixed` are in the gate set
  (`examples/events/gate_set.json`), their digests asserted by
  `tests/test_amplitude_click.py` at every engine change.
- **(e) What the criterion needs.** Nothing. Cost 0.

### Row 2a. The two-slit visibility of one quantum at a time, 0.966 in the clicks

- **(a) What is measured.** `examples/events/amplitude/slits_huygens`:
  the lamp at (2, 60) on five directions, the two openings at (8, 55)
  and (8, 65) re-emitting on the Farey fan of width 48 (1327 directions
  each, the angle weights 123 .. 5619 at the grain 2^18), the screen the
  121 one-Node `sum` sets `screen_0` .. `screen_120` at x = 52; the
  click is the gather's chosen cell per record over the 4096 births of
  the golden wheel [2531, 4096] under the exact phase at the click (4300
  intervals); counted per pixel: wall 882, screen 1711 on 107 pixels,
  faces 1503; the criterion's number is the clicks' visibility (mean of
  the bright pixels - mean of the dark) / (mean bright + mean dark) over
  the two-source cosine's bright pixels y = 35 .. 38, 59 .. 61, 82 .. 85
  and its dark pixels y = 13 .. 20, 48 .. 50, 70 .. 72, 100 .. 107. The
  tool: `tools/amplitude_path.py --check` (the gathers, DETECTOR); the
  counts per pixel from the gathers' `chosen`.
- **(b) Ideal or instrument.** A reading for THIS instrument: the fan's
  width 48 with its weights, the grain 2^18, N = 64, the screen at 44
  Links, 4096 births. The law's ideal for two equal paths is 1 (the rows
  of a pixel at Delta = N / 2 cancel to no row); the fan's discreteness
  (the digital lines' landings: the bright pixels at y = 36 and 84 read
  19 and 20 where their neighbours read 41 and 42) is what the reading
  carries below the ideal. **The pin for this world's fan, derived
  before the run** (this commit, [slits_huygens_pin.py](slits_huygens_pin.py):
  the register's own algebra, `two_slits_map.py`'s walk by the flight
  table's closed form on the world's declared fan and weights, the phase
  of every row by BEAM_LAW note 45, u = ordinal x 2531 mod 4096 with the
  birth phase u mod 64 by note 46, the cells' weights by the click's
  bilinear form on the tables, the cell of u by the engine's own
  `rungs` and `cell_of`; the output in [slits_huygens_pin.out](slits_huygens_pin.out)):
  the counts per cell bit for bit (the screen's 121 counts printed
  there; wall 294, 295, 293; the faces 751, 752), the bright pixels 41,
  19, 42, 38, 51, 49, 51, 39, 42, 20, 40 and the dark 3, 1, 0, 0, 0, 0,
  0, 0, 3, 0, 1, 1, 0, 3, 0, 0, 0, 0, 0, 1, 0, 2, the Pearson with the
  cosine 0.891, and **the visibility 0.9659** (COMPUTATION). The same
  computation reproduces the registered run of 2026-09-21 on every one
  of these numbers, so the pin is the algebra's and the registered
  0.966 is its confirmation; the record's screen weights under the exact
  phase read the same 0.966 (the paper's "0.954 in the record's weights"
  is the 2026-09-20 pin under the built phase, before note 45, and
  belongs to history: under the law as it stands the weights' visibility
  is 0.966 too, the counts being the weights within 2 clicks).
- **(c) The criterion.** The paper's caption: PASS where the model's
  visibility lies above the apparatus-limited measurement, 0.98 (Grangier,
  Roger and Aspect 1986), the ideal 1. Under the pin: FAIL by 0.014
  below the measured and 0.034 below the ideal, by the algebra itself
  and confirmed by the run. What would refute the pin at head: any cell's
  count off the derived count by more than the rungs' own width (2
  clicks: the rungs are per record, the tables' eight totals at u mod 64,
  a part in 276); what would move the verdict: nothing at this fan and
  grain; a wider fan or a finer grain is another world (the scratch map
  of record 160: 0.94 at P = 32, 0.97 at P = 48, 0.96 at P = 64 in the
  weights), not registered. No statistical width: the ladder is
  deterministic.
- **(d) The number in the paper.** 0.966, DETECTOR (the run of 2026-09-21
  on the branch `click`, 4300 intervals in 1334 s, source sha256
  `aa52ecb3168d4353`, initialization `b75b611959ec3dfe`; the 0.954 of
  the weights is the built-phase pin of 2026-09-20 on main `f89884f9`).
  Replicated (round 2 part 1, the tree `5fbd0c7`, L2b REPLICATED; the
  48 images not run). NOT at head: no test replays `slits_huygens`, it
  is not in the gate set, and the engine changed after `5fbd0c7`
  (clock-age-v1, drive-b; neither touches a lamp world without a crowd
  by its own statement, which the re-run confirms or refutes).
- **(e) What the criterion needs.** A pin derived for this world's fan
  (done, above) and a re-run at head `4028b020` against it. Cost: 1
  world, 4300 intervals, about 22 minutes on one core (0.31 s per
  interval on the register's host), the record about 4300 gathers.

### Row 2b. The Mach-Zehnder visibility, 64 / 0

- **(a) What is measured.** `examples/events/amplitude/mz_equal`: the
  (20, 21) splitter, the two arms, the mirrors, the second splitter, the
  ports D1 and D2 (`sum` sets); the click is the gather's chosen port
  per record over 64 births (u = 0 .. 63): D1 64, D2 0; the visibility
  of the clicks (64 - 0) / 64 = 1.000. DETECTOR. The offers 1681 / 1682
  and 1 / 1682 are the record's ledger (`mach_zehnder.mz_equal.offers`),
  a diagnostic of the apparatus layer beside the verdict. The tool:
  `tools/amplitude_path.py --check`; `tests/test_amplitude_layer.py`
  and `tests/test_amplitude_split.py` run the world at every check.
- **(b) Ideal or instrument.** The law's ideal at the registered table:
  the offers exact by the bilinear form at every u (DERIVATIONS_BEAM
  6.7), the clicks by the rungs (2 x 64 x 1681 / 1682 + 1) // 2 = 64,
  so every u lands in D1; the 1 / 1682 is the (20, 21) split's declared
  imbalance, not a fit.
- **(c) The criterion.** PASS as a bound met: the clicks' visibility
  1.000 above 0.98 (Grangier 1986). What would refute: one click at D2
  in 64 births (a rung off by one). More births change nothing of the
  verdict: on a wheel of 4096 the dark port's rung would be 4096 x
  1 / 1682 = 2 clicks, the visibility 0.9988, still above 0.98. No
  statistical width.
- **(d) The number in the paper.** 64 / 0, DETECTOR, `ff5c382d672f`;
  replicated bit-exact (round 1); at head: replayed in-process by the
  two tests above at every engine change (PR #813 green).
- **(e) What the criterion needs.** Nothing. Cost 0.

### Row 2c. The power of the click's form, the window [1.917, 2.012)

- **(a) What is measured.** `mz_345` (63 / 1 at N = 64, `ff5c382d672f`),
  `mz_345_n32` (31 / 1) and `mz_345_n128` (125 / 3; both 2026-09-21,
  main `c8edd50f`, source `5d254c8544aadc88`), and the pair's cells 27,
  5, 5, 27 (row 1a): the gathers over 64 births, DETECTOR; the window of
  the power k is read back from them (a computation on the clicks).
- **(b) Ideal or instrument.** A read-back of the built click, which
  carries the square: an implementation gate, not a prediction about
  nature.
- **(c) The criterion.** NOT COMPARED: Sorkin's kappa (0.0064 +- 0.0119,
  Sinha et al. 2010) is not computed; no three-opening world is
  registered. What would make it a comparison: a three-opening world
  reading kappa after a detector (a reading NOT MADE, not in the paper's
  list and not ordered here).
- **(d) The number in the paper.** The window, from DETECTOR clicks;
  replicated (round 2 part 1, `mz_345_n`); at head:
  `tests/test_amplitude_mz_345_n.py` derives the pins and replays the
  worlds bit-exact at every check.
- **(e) What the criterion needs.** Nothing for the row as it stands.

### Row 3. The deceleration parameter, q = -0.108 coasting

- **(a) What is measured.** `examples/events/hubble_stars/record/coasting_none`
  (the record click; the base world `coasting_none` reads the same
  clicks: "the coasting clicks identical in the second and third runs"):
  an open cube of 301^3 Nodes, the detector `centre` at (150, 150, 150)
  reading `wave` with `reads: "age"` for each of the 24 thrown stars'
  families; per star the redshift z from the rate at which the pointer
  of the detector's `record` lines turns over the window (1 + z = rho
  over the phase slope), the light-travel time tau from the click
  records' age moments; q the second-order coefficient of z(tau) with H
  free (the power-law family) over the registered window [300, 400),
  in the detector's own clock (r = 1.0000 here, no crowd). DETECTOR
  (the record lines and the click ages). The tool:
  `tools/hubble_stars_readings.py` on `tools/run_series.py`'s output,
  the pins `record/expectations.json`.
- **(b) Ideal or instrument.** A reading for this instrument (24 stars at
  the declared fractions of c on the six axes, K 4 198 400, the window);
  the law's ideal in the coasting crowd is the exact Milne form, q = 0
  (1 + z = 1 + v / c, DERIVATIONS_BEAM 2.2), whose pin is the bracket
  [-0.25, +0.25] on q and [0.90, 1.10] on H (t_0 + T_0).
- **(c) The criterion.** The paper's caption: PASS within the stated
  uncertainty, nature's q_0 = -0.53 +- 0.01 (Planck 2018 with a flat
  universe, -0.527 +- 0.011): PASS if |q - (-0.527)| <= 0.011 + the
  reading's own grain; the reading is 0.42 away: FAIL, the law having no
  term with q < 0. The reading's own grain: 0.004 between the engines of
  2026-09-20 and 2026-09-21 (-0.108 to -0.104), 0.03 between the three
  windows (-0.236 / -0.076 / -0.104 at head). What would refute the FAIL:
  a coasting reading below -0.50 at head. No statistical width (the
  clicks are deterministic; the fit's residual rms 0.0019 in z).
- **(d) The number in the paper.** -0.108, DETECTOR, the registered run of
  2026-09-20 (main `f3a41f28`, fingerprint `acf789fe`); "-0.104 at head,
  record 408" beside it. **The register's number now:** -0.104 (the
  Replicator at `6b707a5`, 2026-09-21, record 408: NOT equal to the
  registered digits, the crossing rule moved them; and the register's
  own replay of 2026-09-22 on main's engine in the detector's clock,
  `8cdba4fb`: q = -0.104, H (t_0 + T_0) = 1.0232, r = 1.0000, "no number
  of this series re-registered, the line dated"). So the register carries
  -0.108 as the registered run and -0.104 as the head's dated replay;
  the paper's row already says both; the verdict FAIL under either. Not
  at head `4028b020`: the last replay (`8cdba4fb`) precedes PR #813
  (`e0761893`, the body drive under a key off by default).
- **(e) What the criterion needs.** A re-run at head `4028b020` (the
  writer's list): `record/coasting_none` and the base `coasting_none`,
  400 intervals each, about 50 s each and 323 MB, the tool 15 s. The
  pins: q in [-0.25, +0.25] (the register's), H (t_0 + T_0) in [0.90,
  1.10]; the paper's criterion FAIL unless q <= -0.516; the expected
  reading -0.104 (the head's replay) within the grain 0.01, DETECTOR.
- **(f) The reading at head (2026-09-22, the criteria runner; `origin/main` `4028b020`, the source sha256 `d537d4435b921895`; `tools/run_series.py --jobs 1`, `record/coasting_none` 400 intervals in 62.6 s, 326 MB, completed and conserved, the initialization `22bc71da034c1f64`, the digests state `3993941601dc`, audit `33cf0ac763ce`, events `0fa8cfa523de`; read by `tools/hubble_stars_readings.py` with `record/expectations.json`).** DETECTOR, the window [300, 400) in the detector's own clock (r = 1.0000): q = -0.104, H (t_0 + T_0) = 1.0232, rms 0.0019 in z; the reading's formula 72 of 72 within 2 percent, the luminosity 72 of 72 within 5 percent; 0 record checks failed, 150 readings inside, 0 outside. The pin met (-0.104 within 0.01; the register's brackets [-0.25, +0.25] and [0.90, 1.10] met); equal to the register's dated replay of 2026-09-22 and to the Replicator's reading at `6b707a5`, so PR #813 moved nothing here. **Verdict under the criterion: FAIL** (q = -0.104 against -0.527 +- 0.011; not below -0.516). The base `coasting_none` was run beside it (60.4 s, the digests state `1a385429c948`, audit `33cf0ac763ce`, events `f75ca18274d2`, equal to series S's OFF replay of 2026-09-21): NOT READABLE under the acoustic rule, as the register states; the reading of these worlds is the record world's.

### Row 4b. A moving lamp's redshift with the clock's factor, z = 0.2636

- **(a) What is measured.** The same world and tool as row 3: the star
  `s_mz2` (rank 2 on -z, beta = v / c = 0.2674, momentum 51 901 289 008
  505), its z from the centre's pointer over the late window [300, 400).
  DETECTOR.
- **(b) Ideal or instrument.** The law's ideal for a lamp at rate 1
  thrown at beta is the classical Doppler 1 + beta (z = 0.2674); the
  reading 0.2636 is that ideal within the star's grain (0.0038, a grain
  and a third of the README's 0.003); nature's 1 + z = gamma (1 + beta),
  z = 0.315.
- **(c) The criterion.** PASS if |z - 0.315| <= 0.003 (the reading's grain;
  Botermann et al. 2014 confirm gamma to 2.3e-9 at beta = 0.338): FAIL
  by 0.051, 17 grains. What would refute the FAIL: z >= 0.312 at head.
  Under covariant-readings-v1 (series S, `coasting_none_covariant`, the
  head `24e0c1ba`, replayed at the cap 60 by
  `tests/test_covariant_readings.py`) the same star reads 0.3674 for
  the pinned 0.369 +- 0.003, the hypothesis's row, not the law's.
- **(d) The number in the paper.** 0.2636, DETECTOR (the registered run,
  as row 3); at head 0.2647 (the Replicator at `6b707a5`, record 408;
  the 2026-09-22 replay at r = 1.0000 leaves it), FAIL unchanged.
- **(e) What the criterion needs.** The same re-run as row 3 (one run
  serves both). The pin: z of `s_mz2` = 0.2647 within the grain 0.003
  (the head's replay), DETECTOR; the criterion FAIL unless z >= 0.312.
- **(f) The reading at head (the same run as row 3).** DETECTOR: `s_mz2`'s z = 0.2647 in the window [300, 400) (the record's k 0.0000, v / c 0.2659, the ratio 0.9990 inside; the luminosity 0.9865 inside), the pin 0.2647 within 0.003 met. **Verdict under the criterion: FAIL** (0.050 below nature's 0.315; not at or above 0.312).

### Row 5a. The anisotropy of c by direction, a BOUND on the grain

- **(a) What is measured.** A COMPUTATION: the flight table's pace per
  direction Q |D| / T_D, 0.5774 to 0.5818 at Q = 64 (the paper's
  `checks/light_speed.txt`; DERIVATIONS_BEAM 3.5). The detector reading
  behind it: series Q, `examples/events/c_measured/c_measured`, 290 of
  290 face clicks at the derived tick, Node and face (DETECTOR, the pace
  0.5718 to 0.5893 at finite ages; fingerprint `acf789fe`, 100 intervals,
  0.39 s; replicated at `6b707a5`; `tests/test_c_measured.py` at head).
- **(b) Ideal or instrument.** The law's ideal: the table's rounding on
  the heading, bounded by 1 / (sqrt 3 Q).
- **(c) The criterion.** BOUND: below 1e-18 (Nagel et al. 2015) needs
  Q >= 5.8e17. Nothing to refute: the row bounds a free parameter.
- **(d) The number in the paper.** A computation; the clicks DETECTOR.
- **(e) What the criterion needs.** Nothing (a re-run of `c_measured`
  costs 0.4 s and changes no number of the row). Cost 0.

### Rows 7a and 7b. The deuteron's binding fraction (a BOUND) and the alpha's ratio (FAIL by 6.4)

- **(a) What is measured.** Series N, `examples/events/binding/deuteron_bond`
  (B1) and `alpha_square_bond` (B3), 3000 intervals on an open 21^3
  GameBoard: the border `lifetime` clicks of the paid family `bond` two
  Links from the give (each of content 2; B1 two clicks at tick 19, the
  escaped content 4 of the declared 3677, 0.109 percent, the mass a
  detector reads 3673; B3 four clicks, the escaped 8 of 7354), DETECTOR
  (the border's `click` lines and the books' `escaped`, the bodies'
  `contact` records with `given`); the ratio B3 / B1 = 2.0. No shipped
  readings tool: the README's table reads `events.jsonl`, `run.json` and
  `state.json`.
- **(b) Ideal or instrument.** The law as declared: the give per nucleon
  (2 units of `bond`) is an input, so the escaped content is the
  declaration's; the ratio 2.0 is the rule's linearity (a give once per
  body), an ideal of the rule at any count.
- **(c) The criterion.** 7a: BOUND on the input: nature's E_B / (m_p +
  m_n) = 0.1185 percent (AME2020) is 4.35 units of 3677, which no whole
  give reaches (4 give 0.109, 5 give 0.136); the reading to confirm at
  head: the escaped 4 and the mass 3673 exactly. 7b: PASS if the ratio
  meets 28.296 / 2.2246 = 12.72 within AME2020's precision (better than
  0.01): FAIL by the factor 6.4; what would refute the FAIL: a ratio near
  12.7 (a give that grows with the bonds a body makes, not the rule as
  built). No statistical width: the clicks are the rule's integers.
- **(d) The number in the paper.** 0.109 percent and 2.0, DETECTOR, the
  run of 2026-09-20 (main `b8620d8f`, the sources' fingerprint
  `22935341b7400e13`, the runner's `4a1db891`); re-read under the
  fraction-free law the same day; NOT replicated; NOT re-read since:
  three engine changes that move bodies landed after it (the crossing
  rule, 2026-09-21; clock-age-v1, PR #646; the body drive, PR #813), so
  the numbers are not at head.
- **(e) What the criterion needs.** A re-run at head `4028b020` of the
  three binding worlds (`proton_bond_lamp` beside them as the control).
  Cost: 3 worlds, 3000 intervals, 13 to 53 s each. The pins: B1 the
  first contact about tick 16 with `given` 2 each and 0 after, two
  `bond` clicks of content 2, the escaped 4, the mass 3673; B3 four
  clicks, the escaped 8, the ratio 2.0; the criterion's verdicts BOUND
  and FAIL unless the escaped contents move.
- **(f) The reading at head (2026-09-22, the criteria runner; `origin/main` `4028b020`, the source sha256 `d537d4435b921895`; `tools/run_series.py --jobs 2`, 3000 intervals each, completed and conserved: `deuteron_bond` 98.0 s (the initialization `3de4370135634ee0`, the digests state `36d43a04f9ac`, audit `3243dd29965b`, events `46cd2ba58723`), `alpha_square_bond` 21.6 s (`2458489ca2a8494e`; `647f45e71e86` / `ba6e81715af5` / `c18da506c68e`), `proton_bond_lamp` 59.9 s (`1755092cf58eb185`; `5ac833225257` / `e994ab4c63af` / `a6df0ee9feb4`); read off `events.jsonl`, `run.json` and `state.json`, no rule replayed).** B1, DETECTOR: two `bond` clicks on the border `lifetime` at tick 19 at (8, 10, 10) and (13, 10, 10), each amount 2 and content 2, no other to 3000; the first contact of each body with `given` 2 and 0 on all 346 later hand-overs; the bodies' content 1835 and 1838, `held` (1834, 0, 1, 0) and (0, 1837, 1, 0), the mass read 3673 of 3677; the books' `bond` escaped 4 (GAMEBOARD, the books), 0.109 percent. B3, DETECTOR: four `bond` clicks at ticks 18, 18, 18, 19 at (8, 10, 10), (8, 11, 10), (13, 10, 10) and (11, 13, 10), each amount 2 and content 2; the escaped 8 (the books), 0.109 percent of 7354; the ratio to B1 2.0. The control `proton_bond_lamp`: no contact, no `bond` click, `held.bond` 2 (DETECTOR); its lamp's 2993 gathers read 2958 of content 8 and 35 of content 7 against the registered 2961 and 32 (DETECTOR; the control's reading moved by three gathers at head, no criterion of these rows). What moved in the lattice's clock (GAMEBOARD, the tick of a line): the first contacts at tick 17 (B1; registered 16, the pin "about tick 16" met) and the gives at 16, 16, 16, 17 (B3; registered 15, 15, 15, 16), the alpha's first step at 82 (registered 81), 62 step lines. Every pin of the rows met, nothing moved. **Verdicts under the criteria: 7a BOUND** (the give 4 of 3677, nature's 4.35 unreachable by a whole give), **7b FAIL** (2.0 against 12.72, the factor 6.4).

### Row 8a. The neutron's decay curve, 0.036 against 3.17

- **(a) What is measured.** Series J1, `examples/events/weak/j1_lattice`
  (and `j1_source`): 64 neutrons `n` (content 1839, fixed) on a lattice
  of pitch 4 about the centre of an open 41^3 GameBoard, each with
  `become` at 512 into `p` with the products `beta` (1, 3) and `nu` (1,
  0); a shell of the paid family `d` at r = 18 (4170 Nodes) as one `beam`
  set measuring `beta` with `reads: "age"`. Two detector readings: every
  neutron's own `become` line (its clock's count at the trigger, the key
  512 exactly: a step of width 0 in the neutrons' own clocks) and the
  shell's 64 beta clicks (their count 64, every content 3, their ages).
  The curve the paper cites, the 10th-to-90th-percentile width of the
  click ticks over their median (0.036), is since 2026-09-22 [GAMEBOARD,
  the lattice's clock] in the register (the reviewer's correction on PR
  #777; the entry's re-read of that day): printed and counted in no
  criterion, the detector reading behind it (a lamp at the shell counted
  between the clicks) not yet made. The tool: `tools/weak_readings.py`.
- **(b) Ideal or instrument.** The law's ideal: a delta at the key in
  each neutron's own clock (the width 0); the spread in the lattice's
  clock is this instrument's crowd (the line-mates' rows at 4, 8 and 12
  Links: the counts 154 476 to 338 172 at the trigger at head).
- **(c) The criterion.** Nature's memoryless decay gives the width over
  the median ln 9 / ln 2 = 3.17 (an identity of the exponential form).
  The register's step pin: below 0.1. FAIL where the width is below about
  3; what would refute the FAIL: a width near 3 (an exponential), which
  the law's `become` at a clock count cannot give. **Does the criterion
  need more than 64 clicks?** No: the percentiles at 64 clicks are the
  7th and 58th clicks, so the width's resolution is one click's tick
  (about 1 in 549, 0.002 of the median), and the count sets no verdict:
  more neutrons at one clock fire at the same key, a step at any count.
  The widths at the present count: 0.036 (the registered run, 650
  intervals), 0.0787 in the click ticks and 0.1111 in the betas' births
  at the cap 1024 on the head's replay (the triggers moved to 602 .. 671
  under the age word), so the factor against 3.17 is 88 in the paper and
  28 to 40 at head, FAIL either way.
- **(d) The number in the paper.** 0.036 "a step (series J1, 64 clicks)":
  the registered run of 2026-09-20 (the transformation's fingerprint
  `071197bc5d0f`), re-pinned 2026-09-21, replicated bit-exact at
  `6b707a5` (0.0364). Its kind: the 64 clicks and their contents
  DETECTOR; the width over the median GAMEBOARD (the lattice's clock)
  under the register's re-read of 2026-09-22 (`b220ce9f`, `68b060ed`),
  which the paper's row does not yet say. At head: the replay of
  2026-09-22 read, at the declared 650 intervals, 56 of 64 fired and the
  shell's 20 clicks (the triggers at 602 .. 671 under clock-age-v1), and
  at the cap 1024, 64 of 64 fired at their keys, the 64 clicks, the width
  0.0787 / 0.1111; that replay precedes PR #813, so the numbers are not
  at `4028b020`.
- **(e) What the criterion needs.** A re-run at head `4028b020` at the
  cap 1024 (both J1 worlds), reported by kind: the `become` lines'
  counts (DETECTOR, within the pinned ranges of `expectations.json`), the
  64 clicks of content 3 (DETECTOR), the width in the lattice's clock
  (GAMEBOARD, printed). Cost: 2 worlds of 1024 intervals, about 2.5
  minutes each (the records 180 to 208 MB). The detector reading behind
  the curve (a lamp at the shell) is NOT MADE: a world-file design of the
  physicist's, tier (c), not ordered here.
- **(f) The reading at head (2026-09-22, the criteria runner; `origin/main` `4028b020`, the source sha256 `d537d4435b921895`; `tools/run_series.py --jobs 2 --ticks 1024`, the cap 1024: `j1_lattice` 206.5 s, 189 MB (the initialization `70afd0ac7cf56037`, the digests state `c6f9e3542a09`, audit `9a8126568046`, events `75b7e5372a87`), `j1_source` 224.6 s, 204 MB (`b1bdb15150e0` / `446427636161` / `2008b437cdb5`), completed and conserved; read by `tools/weak_readings.py`).** `j1_lattice`, DETECTOR: 64 of 64 neutrons transformed, every `become` line at its key on its own clock with the count read at the trigger 154476 .. 338172 within its pinned range (inside); the shell's 64 beta clicks, every content 3, the ages 17 .. 41 (inside); [GAMEBOARD, the lattice's clock, not counted]: the trigger ticks 602 .. 671, the width over the median 0.1111 in the betas' births and 0.0787 in the click ticks. `j1_source`, DETECTOR: 64 of 64, the counts 171027 .. 367454, one or more outside the pinned range of counts (as the register's replay of 2026-09-22 read it: the count at the trigger under the fan's dwells is not the dwell period's range), the 64 clicks of content 3 inside; GAMEBOARD the widths 0.1279 and 0.1147. The tool: 0 record checks failed, 5 readings inside, 1 outside, 6 lattice-clock lines not counted; every number equal to the register's replay of 2026-09-22, so PR #813 moved nothing here. **Verdict under the criterion: FAIL** (a step: every neutron at its key, the width 0 in its own clock; in the lattice's clock 0.08 to 0.13 of the median, the factor 25 to 40 below nature's 3.17 at the cap, 88 in the paper's registered run); the count of clicks changes nothing of it.

### Row 8b. The neutrino's passage through a second detector, 16 of 1024 with 0 behind

- **(a) What is measured.** `examples/events/weak/j2_filter`: a bar of
  200 x 1 x 1, a fixed source of `nu` at x = 0 releasing one row per
  self-creation on +x with the stride 1 over the circle; 128 fixed
  readers of `d` at x = 8 .. 135, each measuring `nu` in the window of
  centre 0 and width 1; a far detector at x = 190 without a window. The
  first reader's clicks 16 of its 1024 arrivals, the 127 behind it 0,
  the far detector 699 of 711: each reader's own record (`events`,
  `pass` lines), DETECTOR. The tool: `tools/weak_readings.py`, the pins
  `expectations.json` (`j2`), derived from the flight table and the
  window's rule and checked by `tests/test_weak_readings.py` (d).
- **(b) Ideal or instrument.** The law's ideal: a window admits w / N of
  a stride coprime to N (1 / 64 exactly; BEAM_LAW note 36), and an
  identical reader behind reads the same residue, which the first has
  taken: 0, a filter and not an attenuation. A closed form at any count.
- **(c) The criterion.** Nature: two identical detectors in line read the
  same MeV-neutrino rate to a part in 1e16 per metre (Formaggio and
  Zeller 2012), the ratio 1. The law's ratio 0 / 16: FAIL. What would
  refute: any click at the second reader. **Does the criterion need more
  clicks?** No: the ratio is exact (the residue class behind the first
  reader is empty by the window's rule); 1024 arrivals resolve the
  admitted fraction to 1 / 1024 and the count behind stays 0 at any
  length of the run.
- **(d) The number in the paper.** 16 of 1024 with 0 behind, DETECTOR
  (2026-09-20; re-pinned 2026-09-21; replicated bit-exact at `6b707a5`;
  the 2026-09-22 replay unchanged); at head: `weak/j2_ladder` (the same
  rule) is in the gate set, its digests asserted at every engine
  change; `j2_filter` itself last replayed before PR #813.
- **(e) What the criterion needs.** Nothing for the verdict; a re-run of
  `j2_filter` at head costs 5 s and rides with row 8a's batch as the
  head's confirmation. The pin: 16 of 1024, 0 behind, the far detector
  699 of 711, DETECTOR.
- **(f) The reading at head (2026-09-22, the same batch: `j2_filter` 1037 intervals in 6.2 s, 62 MB, the digests state `ddec44874294`, audit `38ae53006d7b`, events `1c92c9c38177`; `tools/weak_readings.py`).** DETECTOR: the first reader 16 clicks of 1024 arrivals (1 / 64 exactly), the 127 readers behind it 0, the far detector 699 (711 reach it: GAMEBOARD, the flight rule); 3 readings inside, 0 outside; the pin met bit for bit. **Verdict under the criterion: FAIL** (0 against nature's 1).

### Row 8c. The heaviest neutrino mass state, a declared input refuted

- **(a) What is measured.** Nothing: the `nu` family's content 0 is an
  input of the family table.
- **(b) Ideal or instrument.** An input.
- **(c) The criterion.** Nature's splittings need a state above 9.8e-8 of
  the electron's mass; a content 0 cannot carry them: the input is
  refuted; a content above 0 is an input the register does not declare.
- **(d) The number in the paper.** An input, no kind of reading.
- **(e) What the criterion needs.** Nothing. Cost 0.

### Row 9. Malus's law, 128 of 256 at 45 degrees; 219 of 256 at 22.5

- **(a) What is measured.** A12, `examples/events/amplitude/malus_a`,
  `malus_b`, `malus_c`, `malus_22_5`, `malus_67_5`, `malus_chain_22_5`:
  the `sum` set's pass cells over the records 1 .. 256 (u = ordinal x
  159 mod 256), the fraction transmitted the pass cells' count over the
  births: 128 / 128, 0 / 256, 64 / 64 / 64 / 64; 219 / 37, 37 / 219, 187
  / 32 / 5 / 32. DETECTOR (the gathers). The tool:
  `tools/amplitude_path.py --check`; `tests/test_amplitude_malus.py`
  derives the pins from the worlds and the tables and replays the
  worlds bit-exact at every check.
- **(b) Ideal or instrument.** The law's ideal at the tables' grain: exact
  at 45 and 90 degrees (181 = 181; 0 and 256), the tables' rounding at
  22.5 (219 / 256 = 0.8555 against cos^2 22.5 = 0.8536, +0.0019).
- **(c) The criterion.** PASS where the fractions meet cos^2 within the
  tables' resolution 1 / 256: exact at 45 and 90 degrees, +0.0019 at 22.5
  (below 1 / 256 = 0.0039). What would refute: a cell off its rung by
  more than one click. No statistical width.
- **(d) The number in the paper.** DETECTOR; the re-run under the click
  PR #513 at `0323bd5e` (2026-09-21), the 22.5-degree extension at
  `71e15626`; replicated bit-exact (round 1); at head by the test.
- **(e) What the criterion needs.** Nothing. Cost 0.

### Row 12. The clock's field at two distances, 1.907 (series T): marked and left

- **(a) What is measured.** `examples/events/clock_word/age_3`, `age_6`,
  `presence_3`, `presence_6`: the lamp `s_px1` at rest inside a crowd at
  3 and at 6 Links, its light read at the detector's record (1 + z from
  the pointer's turn, in two windows); the ratio of the two k under the
  age word 1.907 (the pin 1.909 +- 0.05), the presence word 1.000.
  DETECTOR. The tool: `examples/events/clock_word/read_runs.py`.
- **(b) Ideal or instrument.** A lattice-exact reading at the dwelling
  ages 5, 6 and 10, 11 (the continuum's 2.000 outside the pin).
- **(c) The criterion.** The potential's form 2.00 (the GPS term); PASS
  under the age word within the pin, 4.6 percent from the continuum;
  FAIL under the presence word.
- **(d) The number in the paper.** 1.907, DETECTOR (the tree `afb533a`;
  replicated bit-exact, round 2 part 1, `5fbd0c7`). Not readable under
  the law as it stands since 2026-09-22 (record 865: the generic entry
  of the bending traps the light in a crowd at a pair with n > 0), and
  being redeclared in the weak field (the pair [1, 16384], the crowd's
  age moment at most 1024 per Node on the light's path) by the chief
  physicist on the owner's word (record 868).
- **(e) What the criterion needs.** Not this runner's: the redeclared
  worlds, their pins from `clock_age_map.py` and their run are the
  physicist's in flight; the paper takes the new numbers on his SHA.
  Marked, left.

### Rows 11a, 11b, 11c. The far lamp through a detector: pinned, the run NOT MADE

- **(a) What would be measured.** [BRIGHTNESS.md](../far_lamp/BRIGHTNESS.md):
  a lamp at rest releasing one row per interval, a detector at rest at
  100 and at 300 Links on a periodic board under `expansion-v1` at H =
  1 / 400 (the wall 2 T_D a, a = H_den + H_num x tick, T_D = 110, S_1 Q
  = 64); the reading DETECTOR: the clicks per interval at each detector
  (the stream's rate, 0.650 and 0.275 for 1 + z = 1.539 and 3.639) and
  the content per click (unchanged in flight: one factor of 1 / (1 + z)
  in the flux where the expanding form has two).
- **(b) Ideal or instrument.** An ideal prediction of the rule 15.2 on its
  own integers (`far_lamp_map.out`): q_eff = +1 (11a), the stretch 1 + z
  exactly (11b), the surface brightness (1 + z)^-1 (11c).
- **(c) The criterion.** 11a FAIL pinned (q_eff = +1 against -0.53; the
  shape residual 0.339 mag rms against flat Lambda-CDM); 11b PASS pinned
  (Blondin et al. 2008's (1 + z)^(0.97 +- 0.10)); 11c FAIL pinned (one
  power of 1 + z against four, Lubin and Sandage 2001). What would refute
  the pins: clicks per interval off 1 / (1 + z) by more than the
  stream's grain, or a content per click that follows the frequency.
- **(d) The number in the paper.** Pins, no reading; the register's rows
  11a to 11c at `01bb782a`; the Replicator's 11b INCONCLUSIVE (a pin
  without a run).
- **(e) What the criterion needs, and the cost.** NOT MADE because
  `expansion-v1` is not built ("no run: expansion-v1 is not built",
  BRIGHTNESS.md): the cost is an engine key (a tick wall on the flight,
  an implementer's build under the physics-rule reviewer's ADMISSIBLE,
  an hour or two of build and review; not this runner's: no engine line),
  then two worlds on a periodic board of about 320 Links (the lamp, two
  detectors), 400 intervals, minutes each, and their pins re-derived from
  the map before the run. Left with the Boss.

## The readings the paper names NOT MADE (marked, left)

| Reading | Where the paper names it | What it needs | Cost |
| --- | --- | --- | --- |
| The two-way c after a detector (a pulse and its return at one detector) | the Lorentz section; [light_outside/DERIVATION.md](../light_outside/DERIVATION.md) "NOT MADE: the two-way c after a detector" | a world of a lamp-detector and a mirror with the pin c_D = Q \|D\| / T_D from the flight table (the physicist's design, a pin per direction) | a world of seconds once designed; the design not this runner's |
| The inverse square's decisive reading, form B: a closed orbit's period at two radii | the Newton paragraph, the claims table row 21 ("the shell mean; the inverse square's decisive reading NOT MADE"); [orbit_lamp/README.md](../../../examples/events/orbit_lamp/README.md) (the pins written at form B's pace 0.2033, which main's drive did not run; D3's 1.997 under main's drive is not decisive, a 1 / r force being scale-invariant) | since PR #813 (`e0761893`) the directional drive is on main under the key `drive_b`, off by default: the orbit-lamp worlds redeclared under the key with note 49's pins, the physicist's order, the reviewer's ADMISSIBLE | two worlds of minutes once declared; not ordered here |
| The moving detector's one-way ratio and the velocity's quantum | the frame paragraph (Table 3 row 4b's clause, the claims table row 27) | the cart build in flight (`moving-detector-build`, step 3 pushed at `5aa64b3e6`, step 4 running; record 868) | the physicist's; marked, left |
| The detector reading behind row 8a's curve: a lamp at the shell counted between the clicks | the register's J entry (2026-09-22, tier (c)) | a world-file change (a lamp on the shell's Nodes, the clicks read against its count) and its pin | minutes once declared; not ordered here |

## The runs this table orders (step 2), in the order of need and cost

1. Rows 3 and 4b: `hubble_stars/record/coasting_none` and
   `hubble_stars/coasting_none` at head, read by
   `tools/hubble_stars_readings.py`; the pins in the rows above.
2. Rows 7a and 7b: `binding/deuteron_bond`, `alpha_square_bond`,
   `proton_bond_lamp` at head; the pins in the row above (the README's
   table).
3. Rows 8a and 8b: `weak/j1_lattice` and `j1_source` at the cap 1024 and
   `weak/j2_filter` at head, read by `tools/weak_readings.py`; the pins
   in the rows above.
4. Row 2a: `amplitude/slits_huygens` at head, 4300 intervals, read by
   `tools/amplitude_path.py --check` and the counts per cell against
   [slits_huygens_pin.out](slits_huygens_pin.out).

Each run headless through the shipped runner (`python -m event_universe
--init <world> --output <dir>` or `tools/run_series.py`), Python 3.14, no
render, no frames, the outputs under the runner's convention in the
session's scratchpad; the readings recorded in the rows below as they
land, PASS or FAIL under the declared criterion, the register's entries
given a dated line, no pin edited after a run, no prior reading deleted.

## The readings at head (step 2)

Recorded in each row's bullet (f) as the runs landed: rows 3 and 4b, 7a and 7b, 8a and 8b at 09:40Z to 09:44Z; row 2a below it when its run lands. Every number by kind; no pin edited after a run; the register's entries given a dated line (EXPERIMENTS.md, series G2, N and J and the L2b entry; the worlds' READMEs).
