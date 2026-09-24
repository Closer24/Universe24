# The one list: the fifteen experiments the paper stands on, each with its world file, its reader of record, its pin by kind, its build, its state and its host time (the chief physicist, 2026-09-24, 12:30Z and 12:45Z, the model owner's words of 11:29Z, 11:31Z and 12:40Z; docs only, no run)

THE OWNER'S WORD (2026-09-24, 11:29Z and 11:31Z, verbatim in sense): there
is no "GO tonight" and no such list; there is ONE list of all the
experiments we want. We are not in the freeze yet; until the freeze
everything that needs building is built, everyone runs their experiments
aside to see that they contribute, and no pin runs; when the engine is
stable we run everything in one go. THE FREEZE is every world of this list
reading clean on ONE commit of main, announced by the Boss; after it the
engine is not touched; then the GO, every pin on that commit. The paper
is submitted only when everything is stable (his word of 11:10Z). The
launch list of 2026-09-23, 23:20Z, with its four groups, its "GO tonight"
and its "NOT IN THE GO" split, is HISTORY; its run command, readers and
preflight sequence are kept below.

THE LIST IS CLOSED AT FIFTEEN (the owner's word of 2026-09-24, 12:40Z, record
1812, written by the Boss;
verbatim in sense: "we are closed, these are the experiments we go on;
there is no 'after the paper', we finish the paper and that is it"): the
seven rows of the 12:30Z draft that were not the paper's runs are OUT,
not deferred: 2a at the 128-period train, 2c's seven three-opening
worlds, 10 (a) and 10 (b) the single opening, 2b Mach-Zehnder, the atom's
lines and the 3-D controls. Rows 2c and 10 stay in the paper as
COMPUTATION checks of the rule (PINS.md; the theorem of the click's
exponent, DESIGN.md 6.1's sums), as they are marked, with no engine run;
rows 2b, the atom's lines and the 3-D controls leave the paper's
schedule. The fifteen: two_slits, the pace fans, 4a, 4b, 4c, R2, M1, M2,
the boxes (ii-a) and (ii-b), the deep well, the light clock, the index at
k = 3 and at k = 4, Bell's four settings, Malus's four settings. The
freeze is every world of these fifteen rows reading clean on one commit
of main.

THE STATE COLUMN: "loads on main" means the world file is on origin/main
and loads under the engine's line B; "file owed" names the writer (the
World Generator from the declaration line named, once the owner orders
it; the owner's word of 11:45Z through the Boss: no world is built ahead of
its need); "build owed" names the engine line the row waits on; "pin
owed, blind" names a pin not yet computed, to be computed from the
declaration before any reading of that world. Every preliminary run of a
world is EXPLORATORY: a diagnostic on current main, by kind, never MET,
PASS or FAIL, never compared with the pin (the owner's rule of 03:29Z).

The run command of every world is the engine's one line from the
repository root:

    python -m event_universe --init <world.json> --output artifacts/<row>/<world>

and the reader of record of every massive world is

    PYTHONPATH=src python examples/events/massive_record/read_runs.py

(the clicks at W on the block's own record, the mean interval over the
hold, DETECTOR; the spectral peak GAMEBOARD beside), with `screen_clicks`
and `light_clicks` in `read_runs.py` for the count rows and the redshift
(Builder 2). The layer declaration of every row is DECLARATIONS.md section
7; the ramp rule is section 8; the sizes are SIZING.md, on world-sizing (PR
1124) until its merge (each shrink a new
declaration, re-derived blind, regenerated on the owner's order only).

THE SEQUENCE AT THE GO (the owner's rule of 04:18Z, record 1648, kept):
(a) the full gate `python tools/check.py --full` green on the frozen
commit, its SHA named; (b) every world of this list loads under line B on
it, one line per world; (c) every world's preliminary once more on the
frozen commit, EXPLORATORY; (d) Reviewer 3's word per world, "the world
works" or the named defect; (e) only then the pin runs, one run each, no
pin moved. Nothing runs before the GO except the preliminaries as
diagnostics.

## The list

SINCE BUILD.md SECTION 26 (2026-09-24, the emitter as a clicking body):
every world below that carried a lamp is regenerated onto an emitter body
of the kind [7, 8] with the well [8, 7] seeded on its mode (the light
clock's, the Sagnac's and the redshift's bodies keep their own kind), the
lamp being refused under the detector law; the four Bell worlds are held
in `docs/designs/detector_law/held_worlds/` until the crystal; every
DETECTOR reading below pinned on the lamp's train stands as written and
is re-derived blind on the emitter before its run (the Boss's order of
23:30Z), the one-cell birth's character (section 26 item 9) and the
line's per-Link pair being the mathematician's gate. The rows' file and
build columns describe the lamp's worlds as they were; the files on this
head are the emitter's.

| Row | World file | Reader of record | The pin (kind) | Build | State | HOST |
| --- | --- | --- | --- | --- | --- | --- |
| 2a, the two slits | `examples/events/detector_law/two_slits.json`, THE SECOND DRAFT of DECLARATIONS.md section 15 L-3 through the World Generator (world-files, 2026-09-24: 160 x 256, x and y open, d = 26, L = 113, the openings of width 3, the lamp's wheel [1, 1024] at one per 4, the lamp's `receiver` the 201 screen sets so that the faces and the mirror line are sinks, the sets with the rung wheel 2^20, ticks 5500; loads and constructs); the first draft on main before it (128 x 128, y periodic, width-1 openings; its own map reads 0.81 and 0.39, SIZING.md) HISTORY | `screen_clicks`: the counts per Node; the counts' visibility, the mean count per pixel over the two-source cosine's bright and dark pixels of the window y in [40, 216] (DETECTOR; `two_slits_1024.out` lists the pixels) | 0.96 +- 0.02 (K, COMPUTATION on the world's own map, `two_slits_1024.py` on world-sizing, PR 1124, until its merge; the falsifier 0.93) | the lamp's ladder (the lamp record's ladder of screen sets only, the sinks outside it, the cell of u over the ladder's own sum; engine-features) | file owed; build owed | 94 minutes |
| The anisotropy of c, the pace fans (5a) | `examples/events/detector_law/pace_fan_{12,16,24}.json` (the lamp with no heading since the no-heading regeneration of 2026-09-24, Reviewer 3's second reading: the six headings by the loader's default, one record; the four declared headings HISTORY; the rule's numbers do not move; the probes at 40 and 36 Links, no rings, ticks 1000 / 1400 / 1900) | the two probes' phase difference per ray, printed per period, the reading of record the SETTLED value or the last period's with its change beside (L-6, GAMEBOARD by declaration) | the axis's k above the diagonal's by k^2 / 48 at fixed omega, the phase pace below by 0.57, 0.28, 0.14 percent at 12, 16, 24 Links (K, COMPUTATION, section 7; a GAMEBOARD reading of the probes, a check of the rule against the engine's board, not a measurement; the World Generator's re-read of pace_fan_12 a diagnostic, section 7 row 5a) | none | loads on main | seconds |
| 4a, the muon's form, the layer pin world | `examples/events/massive_record/layer_pin_rest_14.json` and `layer_pin_k3_14.json` (the ramp 12000 and ticks 20500 since body-check, DECLARATIONS.md section 8 and M1-8: ten relaxation times by the margin module's own number, the engine's check at load; the hold 1000 with ticks 13100 the sized form, SIZING.md, on the owner's order; ramp 10000 and ticks 18500 HISTORY) | `read_runs.py`: the clicks' mean interval over the hold at k = 3 over the rest world's | f / f_0 = 0.8116 at c_eff, the band 0.3 percent (K; 0.8108 and 0.8132 the CONTROLS beside) | none | loads on main; the exploratory run of the regenerated pair (e4) owed before the pin | 4 minutes each (2.8 sized) |
| 4b, the redshift of the moving lamp | `examples/events/massive_record/redshift_k3.json` and `redshift_control.json` on main (88b3752: the chain 4096, the hold 3000, ticks 9600, the light detector at 1100 Links; the sized form 1420 / 1000 / 4000 owed on the owner's order, section 4 rewritten to one form then) | `light_clicks`: f_B per record from the light detector's clicks, the receding world's over the control's (DETECTOR); the ladder's share per cell beside (GAMEBOARD) | 1 + z = 1.9889, the band 0.3 percent (K; 1.9339 with 1.9350 and 1.9319 the CONTROLS beside) | the receiver by name (engine-features) | loads on main; build owed | a minute each |
| 4c, the round trip off a receding transponder | `examples/events/moving_detector/cart_k3.json` on main | the cart's clicks (the README's reader); the received line over the sent | (1 + beta_c) / (1 - beta_c) = 3.732 at k = 3 (K) | none | loads on main; a new exploratory run under the rule owed | seconds |
| The Sagnac ratio (R2) | `examples/events/massive_record/sagnac_k3.json` and `sagnac_rest.json` on main (the world reads the one-way light times between two co-moving bodies, the ratio's linear form, not a rotating ring) (the chain 2200 then 3000, ticks 6400 / 8450; the sized form 800 / 300 with ticks 1050 / 560 owed on the owner's order) | the receiver's FIRST RUNG per hold record from the emitter's birth stamp per direction (DETECTOR, the click line at the rung); the ratio (t_+ - t_-) / (t_+ + t_-) a COMPUTATION beside | 108 (rest), 247 and 72 (k = 3), each +- 2 at W = 256 (K, the rule's own map, COMPUTATION; its provenance DERIVED_BLIND, section 13); the ratio 0.5774 +- 0.01 | the receiver by name (A at_b, B at_a; engine-features); the hop take's fix at every age, on main since PR 1115 | loads on main; build owed | a minute each |
| M1, de Broglie's fringes | `examples/events/massive_record/matter_waves_12.json` in THE SIZED FORM of section 12 and SIZING.md through the World Generator (world-files, 2026-09-24: the take key [-19, 86], the lamp's wheel [1, 2048] at one per 2, its `receiver` the 121 screen sets so that the take lines are sinks, the sets with the rung wheel 65536, ticks 4700, the lamp's `own_grace` the hold; `matter_waves_16.json` the same form on its own clock and take; loads and constructs) | `screen_clicks`: the counts per Node, the side lobe's count centroid over y in [64 + 14, 64 + 40] (DETECTOR) | y = 64 + 27.4, the band one Node (K, COMPUTATION on the lattice map of the layer itself, `matter_waves_2048.py` on world-sizing, PR 1124, until its merge; the formula's 27.79 beside) | the lamp's ladder, as 2a (engine-features) | loads on main; sized form owed; build owed | 30 minutes |
| M2, the energy of a moving mass | `examples/events/massive_record/matter_front_12.json` on main | the first click's interval from the lamp's birth stamp (DETECTOR) | 169 +- 2 at W = 64 (K, `matter_wave_pins.py`; the group transit 167.1 beside) | none | loads on main | seconds |
| (ii-a), (ii-b), the bound clock's second term | `examples/events/massive_record/moving_20.json`, `moving_28.json`, `rest_20.json`, `rest_28.json` on main (the hold 1000 with ticks 2600 / 1200 the sized form, on the owner's order) | `read_runs.py`: the clicks' mean interval at k = 3 over the rest world's | 0.7814 and 0.8032 at c_eff, the band 0.3 percent (P; the controls beside) | none | loads on main; a new exploratory run under amplitude_bound owed | 50 minutes each (30 sized) |
| the deep well in motion (the cavity control) | `examples/events/massive_record/deep_well_k3_40.json` and `deep_well_rest_40.json` on main (ticks 9500; the hold 1000 the sized form) | `read_runs.py` | 0.7531 at c_eff (CONTROL, `massive_layer_pins.py`), the band 0.3 percent | none | loads on main; the exploratory run owed | 3 minutes each (1.2 sized) |
| the light clock of two bodies | `examples/events/massive_record/light_clock_60.json` on main (the chain 673, A at [600, 612), the set the free Node 612, the mirror 672, ticks 2600; the 173 chain with ticks 460 the sized form, its map `light_clock_60_receiver_173.out` on world-sizing, PR 1124, on the owner's order) | the first cycle's record's first rung at the set from its birth (DETECTOR, the click line at the rung); the later cycles beside | 213 +- 1 at W = 64 (K, the rule's own map, COMPUTATION; its provenance DERIVED_BLIND; section 10 item 9, `light_clock_60_receiver.out`; 218 +- 2 HISTORY; 2 L / c = 207.85 beside as the K form) | the receiver by name (A at_a, its own bound set; engine-features); item 10's take at T = 0, on main since PR 1115 | loads on main; build owed | seconds |
| (v-m), the receding index at k = 3 | `examples/events/massive_record/index_moving_long_k3_away.json` with `index_moving_long_rest_k3_away.json` and `index_moving_long_reference_k3_away.json` on main (the clock [3565, 10000] on N = 64 = omega 0.035 per interval, section 11) | the probe's phase over the window [3800, 5400] against the reference and its drift rate (GAMEBOARD: a prediction of the engine's board, not a measurement) | the lab phase +1.0144 rad, +- 0.04, and the drift 1.2 x 10^-3 rad per interval, +- 10 percent (P, `massive_moving_index.py`, `receding_declared`; a GAMEBOARD reading of the probe, a check of the rule against the engine's board, not a measurement) | none | loads on main; the Runner's exploratory readings recorded, his series asked for (section 11); e3's gap explained on it before the pin | 2 minutes each |
| 1a, 1b, 1c, 1d, Bell's four settings | `examples/events/detector_law/bell_{a0b0,a0b1,a1b0,a1b1}.json` on main (N = 2048, the wheel [1, 2048], the train 128 periods) | the joint cells' counts (++, +-, -+, --) per setting, the pair record gathered ONCE on the four joint cells with the weights R = J^2 (DETECTOR); the marginals per side | S = 181 / 64 = 2.828125 EXACTLY at N = 2048 (K, DETECTOR, the counts' own rational on the engine's tables and rung: 874, 150, 150, 874 per settings pair on the wheel [1, 2048], section 1 item 4; NO band, a differing count an engine defect to name; the tables' limit form 46565 / 65773 beside, COMPUTATION); the marginals 1 / 2 within the binomial band (P); THE GUARD: no Bell run before ORDER_CHANNEL_ATTACKS.md is on main under Reviewer 3's read with none open | the joint gather (the pair's one gather on the joint cells, the polariser a table body of two cells; engine-features) | loads on main; build owed | 19 minutes each |
| 9 and Malus's three settings | HELD in `docs/designs/detector_law/held_worlds/malus_{45,11.25,28.125,33.75}.json` (BUILD.md section 26 item 14: under the cumulative ladder of ALGEBRA.md 9.19 (3) (b) as written the table body's two cells at one Node give no distribution; the polariser returns as a body with an axis and two receivers named, the mathematician's step 3, and the counts are re-derived on it); before the hold, regenerated from section 5's two lines through the World Generator (world-files, 2026-09-24: the bar of 8, the read body at x = 4 and its set `first` dropped, the polariser's set alone on its entry Node at x = 6 with the exit cell at x = 7; load and construct); the bar of 7 of main 88b3752 HISTORY | the + and - cells' counts over the 256 records (DETECTOR) | 128, 246, 199, 177 of 256 at s = 64, 16, 40, 48 (K, the tables, exact; the wheel [159, 256] a permutation) | the joint gather's table body of two cells (engine-features) | files owed (the regeneration); build owed | seconds each |
| the receding index at k = 4 | `examples/events/massive_record/index_moving_long_k4_away.json` with its rest and reference worlds on main | as (v-m) | the lab phase +0.6103 rad, +- 0.04, and the drift 4.3 x 10^-4 rad per interval, +- 10 percent (P, `massive_moving_index_k4.py`, written blind 12:50Z, section 11; the rest n 1.2577 beside; a GAMEBOARD reading of the probe, a check of the rule against the engine's board, not a measurement) | none | loads on main; the Runner's k = 4 readings held unrelayed until this pin is on main | 2 minutes each |
| A, A2, B | no world | no run | BOUNDS (SCHEDULE.md rows A, A2, B) | none | no run | none |

## The exploratory runs that precede the pins

e2 is the light clock's world run once as EXPLORATORY; e3 is the receding
index's world run once as EXPLORATORY (the script's number in
DECLARATIONS.md section 11 beside); e4 is 4a's regenerated pair run once
as EXPLORATORY (the clicks must read the mode at rest within 0.1 percent
and the one formula at k = 3 within the band before the pinned run of the
same files). Every exploratory reading is written beside its number on
EXPLORATION.md or the preliminary page and never in the table.
