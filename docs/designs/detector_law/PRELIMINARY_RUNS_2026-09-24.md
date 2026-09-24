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

bell_a1b0 and bell_a1b1: pending at this commit; appended when read.

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
  about 30 to 35 Links wide at one Link per interval, one to the other block
  and one to the open face, with about equal pointers at the two; a record
  completes 60 to 100 intervals after its face half is absorbed.
