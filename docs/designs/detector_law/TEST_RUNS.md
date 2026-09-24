# What a test run must show, one section per experiment of the fifteen, written before that experiment's preliminary run and never moved after it (the chief physicist, 2026-09-24, 13:40Z, the model owner's word of 13:18Z through the Boss; docs only, no run)

THE RULE (the owner, 13:18Z, in substance): whoever writes the world also
writes, for each one, what a test run must show. Each section below says
(1) the world file(s) by path and the engine commit they load on, or the
feature they wait on (the receiver by name, the joint gather, the lamp's
ladder; the four building blocks and the features are
defined in [SIMULATOR_DEFINITIONS.md](../../../SIMULATOR_DEFINITIONS.md)); (2)
what a CLEAN run must show, in words and counts, with no pin and no target
number: the load line VALID, the emitter emitting (which record, from which
interval), the clicks arriving at the declared detector (which set, at
least how many, within how many intervals), what the reader of record
prints (which reader, which fields) and the HOST budget; (3) what makes a
run NOT CLEAN, each a bug for the code; (4) nothing is compared with the
pin: every number a preliminary reads is a diagnostic by kind (DETECTOR a
click, GAMEBOARD a reading of the board, HOST a cost), never MET, PASS or
FAIL. The Preliminary Runner checks each run against its section and names
what broke; the Boss's ENGINE_STATUS.md carries the state.

The run command of every world is the engine's one line from the
repository root, `python -m event_universe --init <world.json> --output
artifacts/<row>/<world>`; the run writes `run.json` (the state, the
`detectors` entries, the `audit`), `events.jsonl` (the `birth`, `block`,
`click`, `gather`, `probe` and `mode` lines) and `state.json`. The readers
of record: `examples/events/massive_record/read_runs.py` (`clock` for a
body's clicks over a window, `light_clicks` for a light detector's train,
`screen_clicks` for a screen's counts per Node, `index_reading` for a
probe's phase); the fans' reader of DECLARATIONS.md section 15 L-6; the
Bell and Malus reader `tools/click_readings/detector_law_bell.py`; the
cart's `tools/moving_detector_readings.py`. HOST budgets are SIZING.md's,
one core.

COMMON TO EVERY SECTION. Clean: the loader prints VALID and the run starts
(a refusal names its key; a refusal of a world of the fifteen is a bug of
the code or of the world file, never of the declaration); `balanced` true
on every `audit` line of `run.json`; the run reaches its declared `ticks`
with no overflow (no `amplitude_bound` refusal, no `RuntimeError` naming
an interval); the reader of record reads the run folder without an error
and prints every field named below; the peak memory below 2 GB. Not clean:
any of these missing. The numbers below (intervals, counts) are the
declarations' geometry (the transit at c = 0.577 Links per interval, the
train's length, the hold), not pins.

## 1. The pace fans, row 5a (three worlds, on main)

1. `examples/events/detector_law/pace_fan_12.json`, `pace_fan_16.json`,
   `pace_fan_24.json` on main af4c3b03 (loaded on 328b560f by the World
   Generator's re-read); no feature waited on.
2. Clean: one `birth` line at tick 1 (the lamp at [64, 64], `amount` 1, one
   record, the train 32 periods: 665, 943 and 1330 intervals); no detector
   set exists, so exactly ONE `gather` line per run at the record's close
   naming a face (the sponge) and no other; the 16 `probe` values per
   interval, the probes at 40 and 36 Links on the eight rays reading 0
   until the front (about 62 to 70 intervals after the birth at 40 Links)
   and nonzero after it; the run reaching 1000, 1400 and 1900 ticks (past
   the train's end by at least 300). The reader (L-6, 14:50Z): per ray the
   phase difference of its two probes printed per period from the second
   period after the front to the train's end, and the reading of record
   the MEAN of that series over the window with its spread beside (the
   settling criterion HISTORY: the series settled on none of the three
   worlds, the spread 2.5 to 6.5 percent per ray, the Runner's 13:40Z);
   both GAMEBOARD; a spread above 0.57 percent leaves the row unresolved,
   named, not a defect. HOST: seconds each, under 100 MB.
3. Not clean: a `click` line or a `gather` line naming a set (there is
   none); a probe at 40 Links reading nonzero before 55 intervals or
   still 0 at 120; a second `gather` line; the run ending inside the
   train; a reader that cannot fit one period at a probe.

## 2. The muon's form, row 4a (two worlds, on main)

1. `examples/events/massive_record/layer_pin_rest_14.json` (3500 ticks) and
   `layer_pin_k3_14.json` (18500 ticks, `ramp` 10000) on main af4c3b03; no
   feature waited on (a body's own clock; no light, no set).
2. Clean: the block of side 14 at [93, 93] on the 200 x 200 periodic layer
   with its seeded profile; a `block` line every interval with the record's
   sum across its cells; the body's `click` lines at its own clock (one per
   cycle of its record; the rest world's cycle about 49 intervals, so about
   55 to 60 clicks over the hold [200, 3000]); in the k = 3 world the drive
   ramping over 10000 intervals, then one Link every 3 intervals along x
   (the `step` lines; the block wrapping on the periodic axis, never off
   the board), and at least 100 clicks over the hold [10200, 18200], their
   intervals longer than the rest world's. The reader: `read_runs.clock`
   on each (the count, the rate per interval, the mean interval between
   clicks, the spectral peak; DETECTOR the clicks, GAMEBOARD the peak).
   HOST: 4 minutes each, under 300 MB.
3. Not clean: no `click` line in the hold; the block stepping off the
   board (a refusal naming the interval); the click intervals of the
   moving world not steady within the hold (the ramp not over); the books
   unbalanced at a hop.

## 3. The round trip off a receding transponder, row 4c (on main)

1. `examples/events/moving_detector/cart_k3.json` on main af4c3b03 (the
   cart world as built under the ray law, `beam-moving-detector-cart-k3-v1`;
   re-declared under the rule by its README; no feature waited on).
2. Clean: the world loads and runs its 600 ticks on the 240 x 3 x 3 board;
   THE RUN KEEPS THE ROW CLICKS (the runner's flag `--keep-row-clicks`; the
   runner's default omits them and the reader then refuses the record as
   trimmed, the Preliminary Runner's finding of 13:40Z): the lamp's births
   and the cart's clicks as its README declares (the sent line and the
   received line); the reader `tools/moving_detector_readings.py` on the run
   folder printing the received line's period over the sent line's
   (DETECTOR). HOST: seconds.
3. Not clean: no click on the cart within the run; the reader unable to
   form a period from fewer than three clicks.

## 4. The energy of a moving mass, row M2 (on main)

1. `examples/events/massive_record/matter_front_12.json` regenerated on
   runner-lines with the matter family's `take` [-19, 86] (the loader's
   requirement on a matter lamp since PR 1115; the file on main af4c3b03 is
   refused without it, the Preliminary Runner's finding of 13:40Z): the
   chain of 200, x open, the matter lamp at x = 20 with `rate` [1, 8],
   `wheel` [1, 64], `train` 8 periods, the set `front` on the body at x =
   104 with W = 64, 600 ticks; no feature waited on.
2. Clean: `birth` lines from tick 8 at one per 8 intervals (the lamp's
   stock); the first record's `gather` line with `chosen` "front" and
   `click_at` "rung", its `click` between 120 and 260 intervals after its
   `birth` (the group transit of 84 Links at about half a Link per interval,
   with the rise); the later records likewise or at the faces after the
   stock (the lamp's own take from age > train, `taken_by_emitter` on the
   books). The reader: `read_runs.light_clicks` on `front` (the first
   click's interval from the birth stamp, the mean interval; DETECTOR).
   HOST: seconds.
3. Not clean: the first record's line at a face and not at `front`; a
   `click_at` "completion" on the first record; a `gather` line before 100
   intervals after its birth.

## 5. The bound clock's second term, rows (ii-a) and (ii-b) (four worlds, on main)

1. `examples/events/massive_record/moving_20.json`, `moving_28.json` (the
   64^3 periodic box, 9500 ticks, `ramp` 1500) and `rest_20.json`,
   `rest_28.json` (the 48^3 box, 3000 ticks) on main af4c3b03; no feature
   waited on.
2. Clean: as row 4a in a box: the `block` line every interval, the body's
   `click` lines (the rest worlds about 40 to 60 over [200, 3000]; the
   moving worlds one Link every 3 intervals along x after the ramp and at
   least 100 clicks over the hold [1500, 9500]). The reader:
   `read_runs.clock` (the hold's rate over the rest's, the peak beside;
   DETECTOR the clicks) and `read_runs.pump` (the light family's energy
   drift and the mode k = 2 pi / 3, GAMEBOARD). HOST: about 50 minutes each
   moving world, under 1 GB; the rest worlds minutes.
3. Not clean: as row 4a; a `mode` line missing (the world key `mode_axis`).

## 6. The deep well in motion, the cavity control (two worlds, on main)

1. `examples/events/massive_record/deep_well_k3_40.json` (9500 ticks,
   `ramp` 1500) and `deep_well_rest_40.json` (3500 ticks) on main
   af4c3b03; no feature waited on.
2. Clean: the block of side 40 at [44, 44] on the 128 x 128 periodic
   layer, the flat seed; the `block` lines; the body's `click` lines (the
   rest world at least 30 over [200, 3500]; the moving world at least 80
   over [1500, 9500], one Link every 3 intervals). The reader:
   `read_runs.clock` (DETECTOR the clicks, GAMEBOARD the peak). HOST: 3
   minutes each.
3. Not clean: as row 4a.

## 7. The receding index at k = 3, row (v-m) (three worlds, on main)

1. `examples/events/massive_record/index_moving_long_k3_away.json`,
   `index_moving_long_rest_k3_away.json`,
   `index_moving_long_reference_k3_away.json` on main af4c3b03 (the chain
   of 4000, x open; the light lamp at 800 with `train` 200 periods, so the
   source runs the whole 6000 ticks; the probe at 2400; the block of side
   24 from 1500 stepping away from interval 3000, or at rest at 2100, or
   absent); no feature waited on.
2. Clean: one `birth` at tick 1; the `probe` line every interval, reading
   0 until about 2740 (1600 Links at c) and nonzero after; the away
   block's `step` lines from about 3002, one Link every 3 intervals, its
   cells short of the probe at 6000; no set, no `click`; the run to 6000.
   The reader: `read_runs.index_reading` over the window [3800, 5400]
   (the phase by projection at the declared omega 0.035 per interval, the
   window's halves, the rest n; GAMEBOARD), EACH WORLD PAIRED WITH THE
   REFERENCE AT ITS OWN SOURCE CLOCK (section 11, 14:50Z): the away world
   against `index_moving_long_reference_omega.json`, the rest world against
   `index_moving_long_reference_k3_away.json`. The Runner's earlier peak at
   0.018 (PRELIMINARY_RUNS_2026-09-24.md section 10) is read again with
   the series printed, so that its origin is named. HOST: about 4 seconds
   each, 40 MB.
3. Not clean: the probe nonzero before 2600; a `gather` line before 6000
   (the record closing early); the block reaching the probe.

## 8. The receding index at k = 4 (three worlds, on main)

1. `index_moving_long_k4_away.json`, `index_moving_long_rest_k4_away.json`,
   `index_moving_long_reference_k4_away.json` on main af4c3b03; no feature
   waited on. THE ORDER: run last, its readings held unrelayed until the
   k = 4 pin (one-list 2bcadd7f, section 11) is on main.
2. Clean: as row 7 with the block stepping one Link every 4 intervals (its
   cells reaching about 2250 at 6000). The reader the same, at the
   block-frame clock of the rest world ([2243, 10000] on N = 64).
3. Not clean: as row 7.

## 9. The light clock of two bodies (waits on the receiver by name)

1. `examples/events/massive_record/light_clock_60.json` keyed with
   `receiver` "at_a" on engine-features b487b0b9 (the chain of 673 closed
   at both ends, A at [600, 612), the set `at_a` the free Node 612, W = 64,
   `own_grace` 70, 2600 ticks); the receiver by name.
2. Clean: A's own record seeded, its clock's `click` lines; A's first light
   record born at A's first cycle (a `birth` line naming measured 0 with
   `cycle`); its ONE `gather` line with `chosen` "at_a", `click_at` "rung",
   `clock_source` "measured:0", its `click` after the grace (train + 70)
   and before 400 intervals from its birth; no `gather` at a face for that
   record; the later cycles' records likewise or closing with no line
   (`closed_after_click` and the escaped row on the books, HOST). The
   reader: `read_runs.light_clicks` on `at_a` from A's birth stamp
   (DETECTOR). HOST: seconds.
3. Not clean: a rung at `at_a` before the return's transit (208 intervals
   from the record's birth) on the first record; two `gather` lines for one
   record; a line with `click_at` "completion".

## 10. The Sagnac ratio, row R2 (two worlds, wait on the receiver by name)

1. `examples/events/massive_record/sagnac_rest.json` and `sagnac_k3.json`
   keyed (block 0 `receiver` "at_b", block 1 "at_a") on engine-features
   b487b0b9 (the chain of 3000, the blocks at 700 and 772 with their faces
   60 Links apart, W = 256, `own_grace` 3000; 8450 and 6400 ticks); the receiver by name.
2. Clean: both blocks' own clocks clicking; each block's light records
   born per cycle; every record of A that completes within the ticks with
   ONE `gather` line at `at_b` (`click_at` "rung", `clock_source`
   "measured:1") and every record of B at `at_a`, the `click` more than 60
   intervals after the birth and under 400; at least 5 such lines per
   direction over the hold; no line at a face; in the k = 3 world the two
   blocks stepping together one Link every 3 intervals. The reader:
   `read_runs.light_clicks` per set from the emitter's birth stamp (the
   first-rung interval per record, DETECTOR; the ratio of the two
   directions a COMPUTATION beside). HOST: about a minute each, under 200
   MB.
3. Not clean: a record of A lined at `at_a` (its own set) or at a face; a
   record with two lines; the blocks stepping off the board; the k = 3
   world's lines not arriving on both directions.

## 11. The redshift of the moving lamp, row 4b (two worlds, wait on the receiver by name)

1. `examples/events/massive_record/redshift_k3.json` and
   `redshift_control.json` keyed (A `receiver` "light_detector") on
   engine-features b487b0b9 (the chain of 4096, A at 2994 pushed on -x
   from `start`, the light body at 4094 with the set `light_detector`, W =
   64, `own_grace` 3000, 9600 ticks); the receiver by name.
2. Clean: A's records born per cycle; each record's ONE `gather` line at
   `light_detector` (`click_at` "rung"), the first arriving about 1900
   intervals after its birth (1100 Links at c) and the later ones
   likewise, at least 10 lines in the hold before A leaves the board (9732
   is beyond the ticks); in the k = 3 world A stepping one Link every 3
   intervals on -x after the ramp. The reader: `read_runs.light_clicks` on
   `light_detector` (the per-record ratio f_B = the birth ordinals'
   difference over the set's count difference between consecutive lines,
   DETECTOR; the ladder's share per cell beside, GAMEBOARD). HOST: about a
   minute each.
3. Not clean: a line at the -x face; fewer than 10 lines; the block off
   the board before the ticks' end (a refusal).

## 12. Malus, row 9 and the three settings (four worlds, wait on the joint gather and the regeneration)

1. `examples/events/detector_law/malus_45.json`, `malus_11.25.json`,
   `malus_28.125.json`, `malus_33.75.json`: on main at 88b3752 they carry
   the bar of 7 and the read body at x = 4, which the joint gather's loader refuses (the
   exit cell off the board); FILES OWED by regeneration from section 5's
   two lines (the bar 8, no read body, the set on the polariser's Node);
   the joint gather on engine-features b487b0b9.
2. Clean: 256 `birth` lines at one per interval (the wheel [159, 256], u
   every residue once); 256 `gather` lines, each with `chosen` naming the
   polariser's set with the channel 0 or 1 (the + or - cell), `click_at`
   "rung", the `click` within 60 intervals of the birth (the transit of 6
   Links and the offer's rise); the two channels' counts summing to 256;
   the run to 1200. The reader: `tools/click_readings/detector_law_bell.py`
   on the four folders (the + share per world, DETECTOR). HOST: seconds
   each.
3. Not clean: a `gather` line at a face or naming no channel; fewer than
   256 lines; a `click_at` "completion"; the loader refusing the
   regenerated file.

## 13. Bell's four settings, rows 1a to 1d (four worlds, wait on the joint gather)

1. `examples/events/detector_law/bell_a0b0.json`, `bell_a0b1.json`,
   `bell_a1b0.json`, `bell_a1b1.json` on engine-features b487b0b9 (the bar
   of 21, the pair lamp at the centre with two arms, the polarisers alice
   at x = 7 and bob at x = 17 as table bodies of two cells, N = 2048, the
   wheel [1, 2048], the train 128 periods, 5500 ticks); the joint gather. THE GUARD
   (section 2 item 8): no Bell run before ORDER_CHANNEL_ATTACKS.md is on
   main under Reviewer 3's read with none open; a preliminary is a run.
2. Clean: 2048 births (two arm records per birth stamp, `arm_records` on
   the `birth` line); every pair gathering ONCE: one `gather` line per
   birth with `arm_records` of two and `chosen` of TWO triples (alice's
   channel, bob's channel), `click_at` "rung", the `click` within 200
   intervals of the birth; the four joint cells all counted over the 2048
   lines; the arms' marginals near one half each (read, not compared); the
   quantum landing on the body of arm 0 (`held` on the books). The reader:
   `detector_law_bell.py` on the four folders (the four cells' counts per
   setting, the correlations and S as fractions, DETECTOR). HOST: about 19
   minutes each, under 500 MB.
3. Not clean: a `gather` line with one triple (an arm clicking alone); two
   lines for one birth; a line at a face; fewer than 2048 lines within
   5500 ticks.

## 14. The two slits, row 2a (waits on the lamp's ladder and the second-draft file)

1. `examples/events/detector_law/two_slits.json` on main is the first draft
   (128 x 128, y periodic, width-1 openings, the screen's 121 sets without
   `receiver`); FILE OWED: the second draft of section 15 L-3 (160 x 256,
   x and y open, d = 26, L = 113, the openings of width 3, the lamp with
   `receiver` naming the 201 screen sets, each set with `wheel` 2^20, the
   lamp's `wheel` [1, 1024], `rate` [1, 4], `train` 32, 5500 ticks); the lamp's ladder on
   engine-features b487b0b9.
2. Clean: 1024 `birth` lines at one per 4 intervals; 1024 `gather` lines,
   EVERY one with `chosen` naming a screen set (`screen_<y>`), `ladder` the
   201 names and `sunk` below `T`; the `click` of each between 150 and 700
   intervals after its birth (the transit 133 Links at c, the offer's
   rise); no line at a face; the run to 5500. The reader:
   `read_runs.screen_clicks` on the screen's sets (the counts per Node, the
   maxima's positions, the visibility over the declared bright and dark
   pixels as an exact fraction, DETECTOR). HOST: about 94 minutes, under
   1.5 GB.
3. Not clean: any `gather` line at a face (the first draft's whole
   finding); `chosen` None on a record whose `T` is nonzero; fewer than
   1024 lines; a count centroid outside the screen.

## 15. De Broglie's fringes, row M1 (waits on the lamp's ladder and the sized form)

1. `examples/events/massive_record/matter_waves_12.json` on main (the
   first form: 128 x 128 y periodic, the screen's 121 sets, the take key
   [-19, 86]); FILE OWED: the sized form of section 12 and SIZING.md (the
   lamp's `wheel` [1, 2048], `rate` [1, 2], `receiver` naming the 121
   screen sets, each with `wheel` 65536, the take lines as sinks, 4700
   ticks); the lamp's ladder on engine-features b487b0b9.
2. Clean: 2048 `birth` lines at one per 2 intervals; 2048 `gather` lines,
   every one with `chosen` a screen set, `ladder` the 121 names, `sunk`
   below `T`; the `click` between 120 and 500 intervals after the birth
   (the group transit of 84 Links at about half a Link per interval); no
   line at a take line or a face; the run to 4700. The reader:
   `read_runs.screen_clicks` (the counts per Node and the side lobe's
   count centroid over y in [64 + 14, 64 + 40], DETECTOR). HOST: about 30
   minutes, under 1 GB.
3. Not clean: as row 14; the matter lamp refused for a missing `take`.
