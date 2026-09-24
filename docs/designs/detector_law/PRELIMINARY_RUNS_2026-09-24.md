# EXPLORATORY: the preliminary runs of the GO worlds on 2026-09-24 (the Preliminary Runner, 08:05Z to 09:30Z)

Every run on this page is EXPLORATORY: a dry run of a world on an engine as it
stands, never a pin run. No pin is compared and no MET, PASS or FAIL is written.
Every number is labelled by kind: a detector's click (its interval and its cell)
is a MEASUREMENT; a store, book, presence, pointer, profile or phase read from
the board is a GAMEBOARD reading; a ratio or a derived number is a COMPUTATION;
the host's time and memory are HOST. The runs were ordered by the Boss on the
model owner's order of 07:48Z (RUN_LIST.md, the PRELIMINARY column and PREFLIGHT
(c)) and extended by the Boss's orders of 08:50Z, 08:58Z, 09:10Z and 09:25Z.
Item 10's emitter take (T = 0) is not on main 5fe266c9; ENGINE C below carries it.

## 1. The engines, the files and the host

- ENGINE A: the checkout of `detector-law-worlds` at c4284f7a, whose merge
  brought main 02f7388b (the PR 1111 merge), NOT main 5fe266c9 (the PR 1068
  merge): `git merge-base --is-ancestor 5fe266c9 c4284f7a` is false, and the
  builder's GO keys (`residue_order`, `amplitude_bound`, the world key `wheel`)
  are absent from its `src/`. Closed by the World Generator's head d1822c66,
  which contains 5fe266c9.
- ENGINE B: a scratchpad worktree of origin/main 5fe266c9 (the detector law's
  second build, no emitter take).
- ENGINE C: a scratchpad worktree of `detector-law-build-3` at 540456da (item
  10's take at T = 0; PR 1115 against main 6f437c01).
- The world files: the `held_worlds` copies at c4284f7a for the ENGINE A and B
  runs (the Malus four, the Bell four at ticks 5000, the redshift pair at
  ticks 14686 with the world key `wheel` 64); the shipped files at
  `detector-law-worlds` 0fd1156 for the ENGINE C runs (sagnac_k3 at ticks 6400
  with `wheel` 256, the Bell four at ticks 5500, light_clock_60 at ticks 2000).
- HOST: the container had Python 3.10 to 3.13 and no numpy; the project
  requires Python 3.14 and numpy 2.5.3. CPython 3.14.0rc2 was installed with uv
  into the scratchpad with numpy 2.5.3. Four cores, 16 GB; up to six engine
  processes ran at once, so the wall times below are shared-core times.
- The runner path: `python -m event_universe --init <world> --output <dir>`,
  headless, the default record. The ENGINE C readings ran in-process
  (`DetectorLawSimulation` stepped with the events collected and the live
  records read from their own books at the end), verified on malus_45 to
  reproduce the runner's gathers exactly.

## 2. The Malus four (ENGINE A and ENGINE B, identical on both)

Files malus_11.25, malus_28.125, malus_33.75, malus_45 (sha256 prefixes
172471078fce, 0113de076d4f, 0f15dabafd61, e4740df19564): a chain of 7, N 256,
ticks 1200, the lamp's stock 256 at wheel [159, 256] and train 32, the `read`
table at x = 4 (set "first"), the polariser table at x = 6 (set "second").

- HOST: status completed, 1200 of 1200 ticks, the books balanced; wall seconds
  11.6 to 13.4 per world, peak RSS about 54 MB.
- MEASUREMENT: 256 clicks of 256 records, all 256 at the cell "first" (the
  `read` table at x = 4), 0 at "second", in all four settings on both engines;
  the first clicks (interval, cell) (11, first), (12, first), ..., (18, first).
- COMPUTATION: the click interval minus the birth stamp is 10 on every record.
- GAMEBOARD: every gather's ladder lists one cell only, [["first", 0, "0"]]
  with weight 256; no cell of the polariser is on the ladder; the counter at
  x = 4 holds [256, 1] at the end, the one at x = 6 holds [0, 1].
- Reviewer 3's word (08:52Z, through the Boss): a named defect of the world
  files (the `read` counter at x = 4 absorbs every record before the polariser
  sees it) and of the engine (the polariser's two channels are not cells as
  built), not of the run.

## 3. The Bell four (ENGINE B; refused on ENGINE A)

On ENGINE A all four refuse at load: `Run failed: beam-v1: measured[0].lamp
has unknown keys: residue_order, residue_seed`. On ENGINE B (files at ticks
5000, sha256 prefixes 408184a91443, 5e1c87dcaa8e, 073ac190ce37, 83f8961362f3)
the four worlds read identically in every count:

- HOST: wall seconds 1032, 1016, 1036, 1021; peak RSS 100 MB; completed.
- GAMEBOARD: 2048 births, one per interval, each a pair record with two arm
  records; the train 3200 intervals; 252 births have no gather within 5000 (a
  record completes 3204 to 3211 intervals after its birth).
- MEASUREMENT: 3585 gathers, 1796 at Alice's one cell "0" and 1789 at Bob's
  one cell "0"; Alice's click 7 intervals after the birth stamp, Bob's 15.
- GAMEBOARD: every ladder lists one cell only, the arm's own table's cell "0";
  no joint cell and no cell of the other table is ever on the ladder.
- HOST (the gather's `u`): the seed order is read by the loader; both arms of a
  birth carry the same `u`; the 1796 gathered births carry 1796 distinct values.

## 4. The redshift pair (ENGINE B; refused on ENGINE A)

On ENGINE A both refuse: `beam-v1: the world has unknown keys: amplitude_bound,
wheel`. On ENGINE B (the c4284f7a files, ticks 14686, `wheel` 64):

- HOST: wall seconds 3097 (k3) and 2891 (control), peak RSS 172 MB, completed.
- GAMEBOARD: the control 238 births (the last at 14676); k3 129 births, the
  last at 9739: A's block steps off the -x face of the 4096 chain (its corner
  at x = 0 at tick 9722, its sum 0 from 9756, the last block line at corner
  -1655 with 4649 steps).
- MEASUREMENT: the control 108 gathers, k3 52, all at light_detector, no face
  gather; the first rung's transit 1888 to 1890 (control) and 2294 to 6110
  (k3); 130 and 77 records open at the end.
- COMPUTATION (the per-record reading of DECLARATIONS.md section 4 item 5,
  read, not compared): f_B = 107 / 6605 = 0.016200 (control) and 85 / 10428 =
  0.008151 (k3) cycles per interval; the ratio 1115796 / 561425 = 1.98744.
- GAMEBOARD: the ladder carries light_detector then face:-x; the set's rungs
  22 to 35 of 64 (control, mean 31.76) and 9 to 19 of 64 (k3, mean 10.15);
  every gather's `u` is 0, so the first cell on the ladder is chosen whatever
  its share.

## 5. sagnac_k3 on ENGINE C (the chain of 3000, wheel 256, ticks 6400)

- HOST: in-process, 294 seconds (the first pass), 232 (the probe pass), 230
  (the readings pass); deterministic (the same 36 gathers on every pass).
- GAMEBOARD: 140 births (70 per block, the first at tick 54); 106 records live
  at 6400 (A's 69, B's 35, and the two blocks' own massive records).
- MEASUREMENT: 36 gathers, 35 of B's records at at_a and 1 of A's at at_b; no
  face click; the completion ages 1709 to 5969 (COMPUTATION, the gather tick
  minus the birth tick); B's click stamps 70 to 97 intervals after the birth.
- GAMEBOARD (the close probe): the first age at which energy x 64 < absorbed
  is met by 27 of A's 70 records (1830 to 3880) and 53 of B's 70 (1542 to
  5734); the 256 crossing coincides with the completion as built; no record
  met either before its train ended.
- GAMEBOARD (the remainder's place, five records at 5000, 5100, 6300, 6400):
  A's old records' energy is spread over the segment behind the blocks with
  the peak inside the gap between the blocks and travelling with them (A born
  1: peak 2163, 2201, 2575, 2607; the gap's share 0.18 to 0.22); B's records'
  energy lies ahead of the blocks with the peak drifting toward the +x face
  (B born 1: 2489, 2614, 2962, 2995); the birth place holds 0 to 9.5 percent.
- GAMEBOARD (the chosen cell): at the 64 crossing the ladder with u = 0 chooses
  at_b on all of A's and at_a on all of B's; the same as the built cell on
  every completed record. With u = 0 the chosen cell is the first in the
  ladder's order holding at least 1 / (2 W) of the absorbed (0.195 percent at
  W = 256), not the first with a nonzero pointer: at_a is nonzero on A's
  records and is skipped because it holds 0.14 percent at most (Reviewer 3's
  correction through the Boss, 09:46Z).
- GAMEBOARD (the hop take): the emitter's own set books its own record first at
  age train + own_grace + 0 to 2 on 38 of A's and 29 of B's records; its share
  of the absorbed at 6400 is 0.0014 or less.

## 6. light_clock_60 on ENGINE C (the closed chain of 673, wheel 64, ticks 2000)

- HOST: 7.2 seconds; 28 births, 0 gathers, 29 live at the end.
- GAMEBOARD (the close probe): neither energy x 64 < absorbed nor energy x 256
  < absorbed holds on any record within 2000; the set's first rung at 214 then
  216 to 217 after the birth; energy x 64 / absorbed 17 to 27 on the settled
  records, not falling with age.

## 7. The Bell four on ENGINE C with the close probe (ticks 5500)

The four files at 0fd1156 (ticks 5500), in-process with the close probe, one
after another. bell_a0b0 (sha256 prefix 1ccd60ef85a0):

- HOST: 1122 seconds; 2048 births, 4096 gathers, 0 live at the end.
- MEASUREMENT: 2048 clicks at Alice's one cell "0" and 2048 at Bob's; no
  escape; Alice's click 7 intervals after the birth stamp, Bob's 15.
- COMPUTATION: every arm completes at the train's end: Alice's arms at age
  3201 and Bob's at 3205 (the train 3200), against 3204 to 3211 on ENGINE B.
- GAMEBOARD (the close probe): energy x 64 < absorbed first holds at age 70
  (Alice) and 380 (Bob) and energy x 256 < absorbed at 267 and 1481, all within
  the train, on every arm; the first interval after the train at which each
  holds is 3200 on every arm; the completion as built follows at 3201 and 3205.
- GAMEBOARD: every ladder lists one cell only, the arm's own table's cell "0";
  the seed order is read (`u` 1465, 864, 1062, ... distinct over the 2048).

bell_a0b1 (sha256 prefix 796d3d582c6b; residue_seed 7815816498507250857):

- HOST: 1147 seconds, one core, 66 MB resident; 2048 births, 4096 gathers,
  0 live at the end; the books balanced.
- MEASUREMENT: 2048 clicks at Alice's one cell "0" and 2048 at Bob's; no
  escape; Alice's first rung 7 intervals after the birth stamp, Bob's 15.
- COMPUTATION: every Alice arm completes at age 3201 and every Bob arm at
  3205, as in bell_a0b0.
- GAMEBOARD (the close probe): energy x 64 < absorbed first holds at age 70
  (Alice) and 380 (Bob), energy x 256 < absorbed at 267 and 1481, all within
  the train, on every arm; after the train each first holds at 3200 on every
  arm; the completion as built follows at 3201 and 3205.
- GAMEBOARD: one cell per ladder, the arm's own table's cell "0"; the seed
  order is read (`u` 1419, 1811, 1930, ... distinct over the 2048). The two
  files differ in the seed order and in nothing this run reads.

bell_a1b0 (sha256 prefix f43e7e96915a; residue_seed 5111944488953294737) and
bell_a1b1 (65d41223674f; residue_seed 14513186461269123306), run in parallel
on two cores:

- HOST: 1159 and 1162 seconds, 66 MB resident each; 2048 births, 4096 gathers,
  0 live at the end, the books balanced, on both.
- MEASUREMENT: 2048 clicks at Alice's one cell "0" and 2048 at Bob's on both;
  no escape; Alice's first rung 7 intervals after the birth stamp, Bob's 15.
- COMPUTATION: every Alice arm completes at age 3201 and every Bob arm at
  3205 on both.
- GAMEBOARD (the close probe): the 64 form first holds at age 70 (Alice) and
  380 (Bob), the 256 form at 267 and 1481, within the train, on every arm of
  both; after the train each first holds at 3200 on every arm.
- GAMEBOARD: one cell per ladder on both; the seed order is read (`u` 308,
  1212, 1455, ... on bell_a1b0 and 1599, 806, 1725, ... on bell_a1b1, distinct
  over the 2048 on each).

The Bell four on ENGINE C read the same in every number but `u`: the setting
changes no count this run reads, as on ENGINE B.

## 8. sagnac_rest on ENGINE C (the open chain of 3000, both blocks at rest, ticks 8450)

The World Generator's file at 90c687a4 (the same content as at 0fd1156, sha256
prefix 53f1f254df2f): A fixed at [700, 712) and B at [772, 784), own_grace
3000, wheel 256, the x faces open. Read in-process with the blocks' corners at
every interval and the x-profile of the squared steps of every open light
record at 4000, 6000, 8000 and 8450 (the Boss's reading (5) of 09:46Z).

- HOST: 258 seconds, one core; 240 births (120 per block), 147 gathers, 240
  click lines, 93 light records open at the end; the books balanced.
- GAMEBOARD (the blocks): A's corner 700 and B's corner 772 at every one of the
  8450 intervals, 0 hops; neither resting block hops under the other's light.
  The emitter's own set books no rung on any of the 240 light records; the two
  blocks' own massive records hold absorbed 0 and no pointer at 8450.
- MEASUREMENT: at_b 100 clicks (all of A's completed records) and at_a 47 (all
  of B's); no click at a face or a measured cell; `u` 0 on every gather.
- COMPUTATION (the completion as built): A's records complete at ages 1309 to
  1336 on 97 of 100 (the three earliest at 8116, 2936 and 1487); B's at 3996 to
  5054, the first at tick 4402, 4007 to 4060 on the births up to about 2500 and
  rising after (5054 on B born 3362). The chosen cell at the first 64 crossing
  with u = 0 equals the built cell on all 147.
- GAMEBOARD (the late B records): B born 3433 at 8000 (age 4567, completed at
  4888): energy 1.51e11 against absorbed 2.363e13, 99.8 percent ahead of B,
  0.2 percent in the gap, none behind A or on a block's cells; the 90 percent
  range 1464 to 2922, the peak 2841; the pointers at_a 1.192e13 and face:+x
  1.171e13. B born 3574 at 8450 (age 4876, open): energy 1.047e11 against
  2.377e13 (energy x 256 / absorbed 1.13), 99.6 percent ahead of B, 0.4 in the
  gap, the range 2130 to 2982, the peak 2928; at 6000 the same record was a
  packet 35 Links wide (2140 to 2175) with energy 6.84e12.
- GAMEBOARD (the gap's share on the oldest records): A born 54: 0.011, 0.027,
  0.013, 0.010 at the four samples, the rest behind A; B born 54: 0.007, 0.011,
  0.004, 0.003, the rest ahead of B. At most 0.045 on any record read (A born
  3785 at age 215, its +x half crossing the gap).
- COMPUTATION (read, not compared): each record's light leaves as two packets
  about 30 to 35 Links wide, one to the other block and one to the open face,
  with about equal pointers at the two; the packets travel at about 0.57 Links
  per interval (c = 1 / sqrt 3; B born 3574's +x half at 2140 to 2175 at age
  2426 from 784; Reviewer 3's line through the Boss, 10:09Z), so A's records
  complete about 1310 after the birth for the 700 Links to the -x face and
  B's about 4000 for the 2216 Links to the +x face.

## 9. two_slits on ENGINE C (the board 128 x 128 x 1, ticks 17300)

The World Generator's file examples/events/detector_law/two_slits.json at
248235b (sha256 prefix eec84865be63): the lamp at [20, 64, 0] with rate 1/16,
the wall of 252 blocks at x = 40 and 41 with the gaps at y = 48 and y = 80,
121 screen sets at x = 104, wheel 64. Read in-process (the Boss's order of
10:09Z); the preliminary reading of record for this file on 540456da, the
World Generator's later run of the same file being its regression check.

- HOST: 1609 seconds wall on one core, 645 intervals per minute cumulative,
  the live records at a plateau of 49 to 50, resident 357 MB at tick 2000 and
  931 MB at tick 8000; 4359600 block lines counted and dropped.
- GAMEBOARD: 1024 births (one every 16 intervals from tick 16 to 16384, one
  arm each, `u` the birth's index modulo 64), 1024 gathers, 0 click lines, 0
  live at 17300; the books balanced: transit released 1024, absorbed 0,
  escaped 1024.
- MEASUREMENT: 0 clicks at every one of the 121 screen sets and at every wall
  cell; every gather chooses the cell face:-x "0" (the open face behind the
  lamp), 1024 of 1024, click_at rung, clock_source interval.
- GAMEBOARD (the completion as built): age 791 on every record, 1024 of 1024,
  the first gather at tick 807 and the last at 17175.
- COMPUTATION (read, not compared): on this file and this engine bit no record
  reaches the screen within its life; each record's light is booked at the -x
  face and the gather closes it there at the same age.

## 10. The receding index's three worlds on ENGINE C (the chain of 4000, ticks 6000)

The three files of main ecebf895 named by RUN_LIST.md's index row, unchanged:
index_moving_long_k3_away.json (sha256 prefix f151bb27f71b),
index_moving_long_rest_k3_away.json (87f5b98ea570) and
index_moving_long_reference_k3_away.json (f81bc35bfe59); the source at 800,
the probe at 2400, the block of side 24 from 1500 (away) or at 2100 (rest).
The probe's phase is a GAMEBOARD reading (DECLARATIONS.md section 11: the row
is a prediction of the engine's board, not a measurement); the declared
numbers are read beside, not compared (the Boss's order of 11:07Z).

- HOST: 4.2, 3.0 and 1.2 seconds wall (away, rest, reference), 37 MB peak
  each, one light record live throughout, 6000 probe lines each.
- GAMEBOARD (the board): the away block hops from 1500 at tick 3002 one Link
  every 3 intervals to 2500 at 5999 (its cells reach the probe after the
  window); the rest block stays at 2100; the probe first reads nonzero at
  2745 (2748 on the rest run); the amplitude ratio world / reference in the
  window [3800, 5400] is 0.981 (rest) and 1.052 (away).
- GAMEBOARD (the probe's phase, the script's projection form over the window
  and its halves, reference minus world): at the series' own frequency,
  0.0180 rad per interval (the projection amplitude's peak on the reference),
  the rest world reads +0.1976 rad (halves +0.1982, +0.1964; n 1.2641 by
  n = 1 + d / ((omega / c) s)) and the away world +1.9071 rad (halves
  +2.4494, +0.9506; the drift -1.87e-3 rad per interval). At the script's
  omega 0.035 (3.7 percent of the series' projection amplitude): rest +0.4297
  rad (n 1.2953), away +1.6522 rad (halves +1.9703, +1.1671; the drift
  -1.00e-3 rad per interval).
- Read beside (declared, not compared): the script's +1.0144 rad with the
  halves +0.5539 and +1.5234 (the drift +1.2e-3 rad per interval) and the
  rest n 1.2519; this reading's halves come in the opposite order and the
  source's frequency on the board reads 0.018 where the script declares
  0.035.

## 11. EXPLORATORY: the second round, the one list's eight rows on main 328b560f (the Preliminary Runner, 12:30Z to 13:30Z)

The Boss's order of 12:30Z on the owner's rule of records 1805, 1806, 1809 and
1810: every run below is EXPLORATORY, a diagnostic by kind on current main, no
pin compared, no MET, PASS or FAIL. The rows are the eight of RUN_LIST.md
(one-list 10eaa3f9, the list closed at fifteen rows at 5f91aecf) that Nature24
names as running on main today with no engine line: 5a, 4a, 4c, M2, the boxes
(ii-a) and (ii-b), the deep well in motion, the receding index at k = 3 and at
k = 4. The Boss's precision of 12:45Z: the k = 4 index worlds ran LAST and
their readings are HELD off this page (`artifacts/index_k4/HELD.md` on the
Runner's container) until the Boss says their pin has landed on main.

- ENGINE: origin/main 328b560f (the PR 1115 merge, item 10's take at T = 0
  and the cell-index guard), installed with uv in a Python 3.14.0rc2 venv
  with numpy 2.5.3; the engine's source fingerprint in every `run.json`
  `f1d93923b43f`. No `src/` file was touched.
- THE RUN: the one list's one command from the repository root,
  `python -m event_universe --init <world.json> --output artifacts/<row>/<world>`,
  headless, the default record; the load line first,
  `python -m event_universe.configuration_validation <world.json>`.
- THE READERS: the reader of record's own functions
  (`examples/events/massive_record/read_runs.py`: `clock`, `pump`,
  `index_reading`, the clicks' mean interval by `click_mean_interval`) called
  on `artifacts/<row>/<world>` with no pin read (its `main` reads
  `expectations.json` and prints a ratio over the pin, so it was not run);
  the cart's reader `tools/moving_detector_readings.py --capability` (the
  design's read / not read mode); the fans' reader written for this round in
  the Runner's scratchpad from the L-6 reading form (section 12 below).
- HOST: four cores, 15 GB; four engine processes at once, so the wall times
  are shared-core times; the peak resident size is the process's.

The load line on the nineteen files (every world of the eight rows and the
receding index's shared reference at omega): eighteen VALID; ONE refusal,
`matter_front_12.json` (section 15).

## 12. EXPLORATORY: row 5a, the pace fans (pace_fan_12, _16, _24 at 88b3752)

The files at their blobs f17bf031 (12), and the 16 and 24 files of the same
generator commit: the layer 128 x 128 x 1, x and y open, the lamp at [64, 64]
with one record on the four headings, the train 32 periods, wheel [1, 64], two
probes per ray at 40 and 36 Links on the axes (39.6 and 35.4 on the diagonals),
no detector set. The clocks [77, 25], [30, 13], [77, 50] on N = 64 give omega
= 2 pi p / (q N) = 0.30238, 0.22656 and 0.15119 rad per interval (the periods
20.78, 27.73 and 41.56 intervals; the trains 665, 887 and 1330 intervals).

THE READER (GAMEBOARD by declaration, L-6): per ray, the phase of each probe's
series by the projection form of `read_runs.probe_phase` at the lamp's own
omega over one period's window, the difference outer minus inner (negative:
the outer probe lags), its magnitude over the gap (4 Links on the axes, 4.243
on the diagonals) the phase advance k in rad per Link; printed per period from
two periods after the front's first nonzero value at the outer probe to one
period before the train's end passes the inner probe (28 periods per ray on
every world); the reading of record the last period's with its change from
the period before, the spread over the window beside as the reader's
precision.

- HOST: wall 9.6, 12.6 and 16.9 s; peak resident 57, 60 and 62 MB; status
  completed at 1000, 1400 and 1900 ticks; the books balanced at every tick.
- GAMEBOARD: one birth (tick 1, one arm, train 665 / 887 / 1330), 1000 / 1400
  / 1900 probe lines, one gather (at 772, 1042 and 1417, the cell face:-x, the
  open face; the record escaped, `escaped` light 1); no click line (no set).
  The front's first nonzero value at the outer probes at 59 / 60 / 60 (the
  axes) and 64 (the diagonals), at the inner 53 / 53 / 54 and 57.
- GAMEBOARD (k in rad per Link, the last period; the spread over the window
  as low to high, its width in percent of the window's mean):

| World | +x | -x | +y | -y | +x+y | -x-y | +x-y | -x+y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pace_fan_12, last period | 0.5382 | 0.5350 | 0.5382 | 0.5350 | 0.5185 | 0.5085 | 0.5159 | 0.5159 |
| pace_fan_12, change from the period before | -0.0031 | -0.0034 | -0.0031 | -0.0034 | -0.0048 | -0.0055 | -0.0052 | -0.0052 |
| pace_fan_12, spread | 0.5128 to 0.5419 (5.5) | 0.5166 to 0.5409 (4.6) | 0.5128 to 0.5419 (5.5) | 0.5166 to 0.5409 (4.6) | 0.5178 to 0.5310 (2.5) | 0.5083 to 0.5297 (4.1) | 0.5156 to 0.5297 (2.7) | 0.5156 to 0.5297 (2.7) |
| pace_fan_16, last period | 0.3898 | 0.3980 | 0.3898 | 0.3980 | 0.4005 | 0.3999 | 0.4021 | 0.4021 |
| pace_fan_16, change | -0.0006 | -0.0006 | -0.0006 | -0.0006 | +0.0008 | +0.0008 | +0.0009 | +0.0009 |
| pace_fan_16, spread | 0.3887 to 0.4047 (4.1) | 0.3912 to 0.4127 (5.4) | 0.3887 to 0.4047 (4.1) | 0.3912 to 0.4127 (5.4) | 0.3918 to 0.4043 (3.1) | 0.3919 to 0.4047 (3.2) | 0.3919 to 0.4056 (3.4) | 0.3919 to 0.4056 (3.4) |
| pace_fan_24, last period | 0.2666 | 0.2654 | 0.2666 | 0.2654 | 0.2517 | 0.2583 | 0.2555 | 0.2555 |
| pace_fan_24, change | +0.0096 | +0.0095 | +0.0096 | +0.0095 | -0.0037 | -0.0035 | -0.0035 | -0.0035 |
| pace_fan_24, spread | 0.2567 to 0.2710 (5.5) | 0.2556 to 0.2725 (6.5) | 0.2567 to 0.2710 (5.5) | 0.2556 to 0.2725 (6.5) | 0.2516 to 0.2595 (3.1) | 0.2582 to 0.2658 (2.9) | 0.2554 to 0.2625 (2.8) | 0.2554 to 0.2625 (2.8) |

- COMPUTATION (read, not compared): the last period's mean of the four axes
  over the four diagonals is 1.0425 at 12 Links, 0.9819 at 16 and 1.0421 at
  24 (the axis above the diagonal in k by 4.2 percent, below by 1.8 percent,
  above by 4.2 percent); 2 pi over the wavelength is 0.5236, 0.3927 and 0.2618
  rad per Link. The series does NOT settle within the window on any world: on
  every ray the per-period value moves by up to 2 to 3 percent between
  neighbouring periods with a recurrence of about five periods (12 Links) or
  four periods (16 and 24 Links), so the last period's value is read with its
  change and the spread, as L-6's settling criterion asks. On the 16-Link
  world the +x and -x rays differ from the first period (0.3912 against
  0.3928 at the window's start, 0.3898 against 0.3980 at its end), where on
  the 12- and 24-Link worlds the opposite axes read alike to four places;
  which of the reader's fit (one period's window of non-integer length on
  integer ticks) and the board this is, is unread here.

## 13. EXPLORATORY: row 4a, the layer pin worlds (layer_pin_rest_14 at 7e9b0002, layer_pin_k3_14 at aee58cd3)

The periodic 200 x 200 x 1 layer, the kind [3200, 3236], the block s = 14 at
the well [3200, 3227], the seed the bound mode's integer profile, `margin`
"pin" (the margin module's omega_b 0.14844, the extent 35.97 Links, on both
files); at rest 3500 intervals; at k = 3 the ramp 10000 and the hold 8000,
18500 intervals, `mode_axis` x. The reader of record's windows: [200, 3000]
at rest, [10200, 18200] in motion (`read_runs.LAYER_HOLD`).

- HOST: layer_pin_rest_14 wall 147.5 s (the engine's own 85.0), peak resident
  95 MB; layer_pin_k3_14 wall 522.0 s (the engine's 497.2), 193 MB; both
  completed at every requested tick, the books balanced; no escape.
- DETECTOR (the block's clicks, its own record): at rest 82 clicks in 3500,
  the first at 32, 74, 116, 159, 201, the last at 3460; over [200, 3000] 67
  clicks, their mean interval 42.3333 intervals (2 pi over it 0.14842 rad per
  interval). At k = 3: 387 clicks in 18500, the first at 32, 74, 116, 159,
  201, the last at 18477; over the ramp [200, 10000] 218 clicks, their mean
  interval 45.0323; over the hold [10200, 18200] 154 clicks, their mean
  interval 51.8170 intervals (2 pi over it 0.12126).
- GAMEBOARD: the rest block's corner [93, 93, 0] throughout, 0 steps; the k =
  3 block from [93, 93, 0] to [167, 93, 0] with 4474 steps in 18500 (1640 by
  10000, 4374 by 18200: one Link per 3 intervals over the hold); the summed
  record's spectral peak 0.14826 at rest over [200, 3000] and 0.12035 over
  the hold, the centre cell's the same; the rate by count 0.023929 and
  0.019250 per interval; the pump 0 identically (no light family content:
  `light_form` 0, the mode content 0).
- COMPUTATION (read, not compared): the rest clicks' mean interval over the
  hold clicks' mean interval 0.81698 (DETECTOR over DETECTOR); the rate ratio
  0.80448 and the spectral peak ratio 0.81172 (GAMEBOARD).

## 14. EXPLORATORY: row 4c, the cart with a click (cart_k3 at 07c96fb7)

The bar 240 x 3 x 3, open; the post R fixed at x = 1 (the transponder), the
lamp A at x = 3, the cart D from x = 20 at one Link per 3 counts; `clock_stamp`
true; 600 intervals; the model beam-moving-detector-cart-k3-v1.

- HOST: the one command, wall 4.0 s, 66 MB, completed at 600, the books
  balanced; the record's `escaped` lists the family `mass` with content
  35328 and 0 for post, source and cart (GAMEBOARD, the ledger as written).
- THE READER'S REFUSAL on the one command's record: `tools/moving_detector_readings.py`
  refuses a trimmed record (`omit_row_clicks` true, the runner's default:
  the events file holds 552 click lines, none the per-row click of a measured
  event) and names the way: run again with `--keep-row-clicks`. So the world
  ran a second time with that flag (`artifacts/4c_row_clicks/cart_k3`, the
  same initialization fingerprint 85a203a3, 3.8 s, 900 click lines), and the
  reader read that run in `--capability` mode, the design's read / not read
  form (every number below is printed as read; the pins the reader prints
  beside its lines are not copied here).
- DETECTOR (the cart's own record, its count, its Node, the ordinal read):
  the first clicks of the lamp's rows at the counts 68, 71, 74, 77, 80, 82,
  83, 86, 89, 91, 92 at the Nodes x = 42, 43, 44, 45, 46, 47, 47, 48, 49,
  50, 50, the ordinals 1 to 11; 227 clicks of the lamp's rows in all; the
  Node's change between consecutive clicks {0: 49, 1: 177}, at most one per
  count; the pace over the window 1 / 3 Nodes per count exactly.
- DETECTOR (the ratios of counts): k_AB, the cart's counts apart over the
  lamp's ordinals apart from the cart's count 60, 2.34956 over 531 counts;
  k_BA, the post's counts apart over the cart's ordinals apart from its count
  60, 1.57143 over 539 counts (360 re-release lines); the round trip, the
  cart's counts apart between two returns over its ordinals apart from its
  count 153, 3.66387 over 436 counts (121 returns); the radar velocity of the
  post, delta x_D over delta t_D, +0.33232 Nodes per count over 436 counts;
  the ratio k_BA / k_AB 0.66882 (COMPUTATION of two detectors' counts).
- GAMEBOARD: 200 step lines, the intervals between hops {3: 199}; the cart's
  final age 600 against 600 intervals.

## 15. EXPLORATORY: row M2, the energy of a moving mass (matter_front_12 at 43311da1): REFUSED AT LOAD

The load line refuses the file on main 328b560f, and the one command refuses
it the same way (`Run failed`, exit 1, no run directory):

    beam-v1: measured[0]: a lamp of the massive kind 'matter' needs the kind's take pair (the family key `take` [n, d], the Ports' follow at its own remnant take; DECLARATIONS.md section 10 item 10)

The file's matter family declares `pair` [800, 809] and `phase_per_link`
[1089, 320] and no `take`; its lamp at [20, 0, 0] has rate [1, 8], wheel
[1, 64], train 8; the detector set `front` at [104, 0, 0]. The refusal is the
loader's line of PR 1115 (item 10's take at T = 0); the file predates it
(31f9b6b). Not a defect of the engine's run: a world line owed, reported to
the Boss with the refusal line. No reading.

## 16. EXPLORATORY: the deep well in motion (deep_well_rest_40 at f1e94f5c, deep_well_k3_40 at 42ffca6f)

The periodic 128 x 128 x 1 layer, the kind [800, 809], the block s = 40 at
full depth [800, 800], the flat seed 2^20, the block at (44, 44); at rest 3500
intervals; at k = 3 the ramp 1500 and the hold 8000, 9500 intervals,
`mode_axis` x; `margin` "control" (omega_b 0.05357, the extent 4.13 Links,
both files). The windows [200, 3000] at rest and [1500, 9500] in motion
(`read_runs.HOLD`).

- HOST: deep_well_rest_40 wall 44.9 s (the engine's 43.4), 84 MB;
  deep_well_k3_40 wall 142.9 s (the engine's 139.9), 129 MB; both completed,
  the books balanced; no escape.
- DETECTOR (the block's clicks): at rest 30 clicks in 3500, the first at 89,
  204, 320, 440, 559, the last at 3488; over [200, 3000] 24 clicks, their
  mean interval 117.3043 intervals (2 pi over it 0.05356). At k = 3: 63
  clicks in 9500, the first at 89, 205, 322, 442, 564, the last at 9421; over
  the ramp [200, 1500] 11 clicks, their mean interval 128.7000; over the hold
  51 clicks, their mean interval 155.4600 intervals (2 pi over it 0.04042).
- GAMEBOARD: the rest block's corner [44, 44, 0] throughout; the k = 3 block
  from [44, 44, 0] to [12, 44, 0] with 2912 steps in 9500 (246 by 1500; the
  periodic layer crossed); the summed record's spectral peak 0.05370 at rest
  and 0.04044 over the hold (the centre cell's the same); the rate by count
  0.008571 and 0.006375 per interval; the pump 0 identically.
- COMPUTATION (read, not compared): the rest clicks' mean interval over the
  hold clicks' mean interval 0.75456 (DETECTOR over DETECTOR); the rate ratio
  0.74375 and the spectral peak ratio 0.75302 (GAMEBOARD).

## 17. EXPLORATORY: the boxes (ii-a) and (ii-b) (rest_20 at 97e12136, rest_28 at 20f5bf72, moving_20 at 70cd3b21, moving_28 at 4a78b736)

The rest worlds on the periodic 48^3 board, 3000 intervals (s = 20 at full
depth [800, 800] on the kind [800, 809]; s = 28 at half depth [1600, 1609] on
[1600, 1618]); the moving worlds the same blocks on 64^3 pushed to k = 3 over
the ramp 1500 and the hold 8000, 9500 intervals, `mode_axis` x. `margin`
"control": omega_b 0.11046 (the extent 5.73 Links) and 0.13053 (7.94) on the
rest files. The windows [200, 3000] and [1500, 9500].

- HOST (the rest worlds): rest_20 wall 319.6 s (the engine's 318.7), 114 MB;
  rest_28 wall 317.3 s (315.7), 115 MB; both completed, the books balanced,
  no escape.
- DETECTOR (the rest blocks' clicks): rest_20 52 clicks in 3000, the first at
  42, 100, 157, 213, 270, the last at 2944; over [200, 3000] 49 clicks, their
  mean interval 56.8958 intervals (2 pi over it 0.11043). rest_28 62 clicks,
  the first at 35, 84, 132, 181, 229, the last at 2973; over the window 58
  clicks, their mean interval 48.1404 (2 pi over it 0.13052).
- GAMEBOARD (the rest worlds): the corners [14, 14, 14] and [10, 10, 10]
  throughout, 0 steps; the summed record's spectral peaks 0.11023 and
  0.13034, the centre cells' the same; the rates by count 0.017500 and
  0.020714 per interval; the pump 0.

## 18. EXPLORATORY: the receding index at k = 3 (index_moving_long_k3_away at 653a5456, index_moving_long_rest_k3_away at a23edda0, index_moving_long_reference_k3_away at eb4b0f52, index_moving_long_reference_omega at 4ecbd591)

The chain of 4000, x open for light; the source at 800 (a train of 200
periods), the probe at 2400; the block of side 24 (the well [314, 315] on the
kind [156, 157], g [1, 200], G [1, 1]) from x = 1500 stepping away from
interval 3000 at k = 3 (the away world, light at omega = 2 pi 3565 / (10000 x
64) = 0.034999 rad per interval), or at rest at x = 2100 with light at the
block-frame frequency omega' = 2 pi 1846 / (10000 x 64) = 0.018123 (the rest
world); the references the same chains without the block, at omega
(`index_moving_long_reference_omega`, the reader of record's reference of the
away world) and at omega' (`index_moving_long_reference_k3_away`, the rest
world's). 6000 intervals each. The reader of record (`read_runs.index_reading`
over `LONG_WINDOW` [3800, 5400] and its halves): the probe's phase by the
projection form at the light family's own omega, the delay the reference's
phase less the world's. Section 10 above paired the away world with the
reference AT OMEGA' (the same file as the rest world's reference); this round
pairs it as `read_runs.py` does, with the reference at omega, so its numbers
are not those of section 10 by the pairing alone.

- HOST: wall 28.9, 26.4, 14.3 and 13.7 s (away, rest, the reference at
  omega', the reference at omega); 87 to 88 MB each; all four completed at
  6000, the books balanced; no escape.
- GAMEBOARD (the board): the away block hops from [1500, 0, 0] to [2500, 0, 0],
  1000 steps in 6000 (one Link per 3 intervals from 3000); the rest block at
  [2100, 0, 0] throughout; the probe's first nonzero value at 2745 (away) and
  2748 (rest); 6000 probe lines each.
- GAMEBOARD (the away world against the reference at omega, the projection
  form at omega over [3800, 5400]; a prediction of the engine's board, not a
  measurement): the delay +0.9590 rad (n = 1 + delay / (k s) 1.6592 as the
  reader forms it), the amplitude ratio 1.0429; the halves +0.4336 and
  +1.5350 rad, the drift between them +1.377 x 10^-3 rad per interval. At
  the reference series' own frequency over the window (the projection
  amplitude's peak, 0.0350) the same to three places: +0.9586, the halves
  +0.4334 and +1.5356.
- GAMEBOARD (the rest world at omega' against its reference): the delay
  +0.1988 rad, n 1.2638, the amplitude ratio 0.9807; the halves +0.1976 and
  +0.1966 (the drift -1.1 x 10^-6 rad per interval); at the series' own
  frequency 0.0181: +0.1982, the halves +0.1976 and +0.1967.
- GAMEBOARD (the pump over the window, the away world): light's `form` from
  1.076 x 10^13 to 1.459 x 10^13, the drift 2.39 x 10^9 per interval in the
  mean, the largest 6.61 x 10^10; the mode k = 2 pi / 3 content 1.94 x 10^11
  in the mean, 4.80 x 10^11 at the largest. The rest world: `form` 5.56 x
  10^12 to 7.50 x 10^12, the drift 1.21 x 10^9 in the mean, no mode line.
- HOST (the moving worlds): moving_20 wall 2871.1 s (the engine's 2866.0),
  peak resident 216 MB; moving_28 wall 2673.5 s (2668.3), 217 MB; both
  completed at 9500, the books balanced, no escape; the margin module's
  omega_b on the 64^3 files 0.11065 (the extent 5.74) and 0.13170 (8.18), so
  the two boxes' rest modes differ by 1.0017 and 1.0090 (COMPUTATION of the
  margin lines, the periodic image).
- DETECTOR (the moving blocks' clicks): moving_20 135 clicks in 9500, the
  first at 42, 99, 157, 213, 270, the last at 9495; over the ramp [200, 1500]
  21 clicks, their mean interval 61.3000; over the hold [1500, 9500] 111
  clicks, their mean interval 72.5818 intervals (2 pi over it 0.08657).
  moving_28 165 clicks, the first at 35, 82, 132, 179, 227, the last at 9468;
  over the ramp 25 clicks, their mean interval 51.0833; over the hold 136
  clicks, their mean interval 58.9185 intervals (2 pi over it 0.10664).
- GAMEBOARD (the moving worlds): the corners from [22, 22, 22] to [54, 22, 22]
  and from [18, 18, 18] to [50, 18, 18], 2912 steps each in 9500 (246 by 1500,
  one Link per 3 intervals over the hold; the periodic box crossed); the
  summed record's spectral peaks over the hold 0.08649 and 0.10593, the
  centre cells' the same; the rates by count 0.013875 and 0.017000 per
  interval; the pump 0 identically on both (no light declared).
- COMPUTATION (read, not compared; the 48^3 rest box against the 64^3 moving
  box, the boxes' ratio above not applied): the rest clicks' mean interval
  over the hold clicks' mean interval 0.78389 (s = 20) and 0.81707 (s = 28)
  (DETECTOR over DETECTOR); the rate ratios 0.79286 and 0.82069, the spectral
  peak ratios 0.78463 and 0.81274 (GAMEBOARD).

## 19. EXPLORATORY: the receding index at k = 4: RUN LAST, THE READINGS HELD

index_moving_long_k4_away (28d38c4e), index_moving_long_rest_k4_away
(cbf52785) and index_moving_long_reference_k4_away (271db477) loaded VALID and
ran after every other world (HOST: wall 27.5, 25.0 and 13.9 s, 87 to 88 MB,
all completed at 6000, the books balanced). Their readings are HELD in
`artifacts/index_k4/HELD.md` on the Runner's container and are not on this
page, on the Boss's precision of 12:45Z (the pin at k = 4 computed blind by
Nature24 first), until the Boss says the pin has landed on main.

## 20. The one list's preliminary column, and the test-run lines (the Boss's order of 13:22Z)

Whether each world "works" in the sense of RUN_LIST.md's preliminary column
(it loads, the emitter emits, the clicks arrive at the declared detector
within the declared count, the reader reads), one line per world; and the
line against Nature24's TEST_RUNS.md, which is not on one-list (2bcadd7) at
this writing, so every world reads "readings recorded, no test-run line yet".

| Row | World | Loads | Emits | The clicks at the declared set | The reader reads | Against TEST_RUNS.md |
| --- | --- | --- | --- | --- | --- | --- |
| 5a | pace_fan_12, _16, _24 | VALID | one record on four headings, the train 665 / 887 / 1330 | no set declared (L-6): no click; the record's one gather at the open face | the probes' phase per ray per period, 28 periods, the spread 2.5 to 6.5 percent; the series does not settle in the window | readings recorded, no test-run line yet |
| 4a | layer_pin_rest_14, layer_pin_k3_14 | VALID | the block's own record | 82 and 387 clicks on the block's own record, 67 over the rest window and 154 over the hold | `clock` reads both | readings recorded, no test-run line yet |
| 4c | cart_k3 | VALID | the lamp's rows and the cart's pulses | 227 clicks of the lamp's rows and 121 returns on the cart's own record | the one command's record is refused as trimmed (`omit_row_clicks`); read on the run with `--keep-row-clicks` in `--capability` mode | readings recorded, no test-run line yet |
| M2 | matter_front_12 | REFUSED: the matter lamp needs the kind's take pair (section 15) | no run | no run | no run | readings recorded, no test-run line yet |
| the boxes | rest_20, rest_28, moving_20, moving_28 | VALID | the block's own record | 52, 62, 135 and 165 clicks | `clock` reads all four | readings recorded, no test-run line yet |
| the deep well | deep_well_rest_40, deep_well_k3_40 | VALID | the block's own record | 30 and 63 clicks | `clock` reads both | readings recorded, no test-run line yet |
| (v-m) k = 3 | index_moving_long_k3_away, _rest_k3_away, _reference_k3_away, _reference_omega | VALID | the source's train of 200 periods, the probe nonzero from 2745 / 2748 | no set declared: the probe's phase, GAMEBOARD by declaration | `index_reading` reads the away world against the reference at omega and the rest world against its reference at omega' | readings recorded, no test-run line yet |
| k = 4 | index_moving_long_k4_away and its rest and reference | VALID | as k = 3 | as k = 3 | held (section 19) | held |
