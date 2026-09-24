# The status of the fifteen experiments: the engine features each needs, its world file, its test run without a pin (the Boss's file, the model owner's word of 2026-09-24, 13:10Z)

The model owner's word (in Hebrew, in substance, 2026-09-24, 13:10Z): "have
the right status for each of the fifteen we want: one, does it have the
features it needs and which features it uses; two, does it have the world
it wants; three, has it passed a test run, without a pin."

This is that file. The Boss keeps it and rewrites a cell only on a merged
record with its commit; it states the truth of the moment and nothing
else. The fifteen rows are the one list of
[RUN_LIST.md](RUN_LIST.md) (Nature24's branch `one-list`, the owner's
word of 12:36Z: fifteen, the seven others out). A "test run" is a
PRELIMINARY, EXPLORATORY run on current `main` without a pin: a
diagnostic by kind (HOST, GAMEBOARD, DETECTOR), never MET, PASS or FAIL,
never compared with a pin. The freeze is the one commit of `main` on which
every row reads "yes" in all three columns; the pin runs come after it, on
the owner's GO, and are not on this page.

## The three engine features (the bugs to fix, in Nature24's order of 12:40Z)

| Feature | What it is | Frees | Built by | State |
| --- | --- | --- | --- | --- |
| the receiver by name | the key `receiver` on every emitting block, the record's ladder that one cell, the gather line at the cell's first rung, the other sinks booked to `escaped`, the emitter's own cells taking on no pointer at every age | 4b, R2, the light clock | Nature24 (the owner's word of 13:03Z: one agent writes all the code) | on `main` at 9a11fcb2 (PR 1129, engine-features 3ce286dd), 2026-09-24 14:55Z; Reviewer 3's read of main pending |
| the joint gather | one gather of the pair record on the four joint cells, the polariser a table body of two cells with the offer split over the tables | Bell's four, Malus's four | Nature24 | on `main` at 9a11fcb2 (PR 1129), 14:55Z; Reviewer 3's read of main pending |
| the lamp's ladder | the declared sinks outside a lamp record's ladder, the cell chosen over the ladder's own sum, the screen's sets' own rung wheel | 2a, M1 | Nature24 | on `main` at 9a11fcb2 (PR 1129), 14:55Z; Reviewer 3's read of main pending |

Item 10 at T = 0 and the cell-index guard (PR 1115, merged at 328b560f) are
on `main` and are not counted as a feature owed.

## The fifteen

| Experiment | 1. Engine features (which; on `main`?) | 2. World file (on `main`?) | 3. Test run without a pin (clean?) |
| --- | --- | --- | --- |
| 2a, the two slits | the lamp's ladder; yes (PR 1129) | first draft on `main`; the second draft (L-3) owed after the lamp's ladder | ran on the first draft: 0 screen clicks, every record gathered behind the lamp (record 1798); not clean; re-run after the lamp's ladder on the second draft |
| 5a, the anisotropy of c (the pace fans) | none; yes | yes (pace_fan_12, _16, _24 at 88b3752) | ran on main 328b560f (PR 1130, section 11): loads, runs, reads; the probes' series NOT settled within L-6's window on any of the three (the criterion or the window to redeclare, Nature24); not clean yet |
| 4a, the muon's form (the layer pin world) | none; yes | yes (layer_pin_rest_14, layer_pin_k3_14) | ran (PR 1130, section 12): loads, runs, reads (DETECTOR the clicks' mean interval at rest and over the hold); the word clean against TEST_RUNS.md pending |
| 4b, the redshift of the moving lamp | the receiver by name; yes (PR 1129) | yes (redshift_k3, redshift_control; the `receiver` key added with the receiver by name) | not yet; after the receiver by name |
| 4c, the round trip off a receding transponder | none; yes | yes (cart_k3) | ran (PR 1130, section 13): loads, runs; the one command's record refused by the reader as trimmed, read with --keep-row-clicks (the reader of record's form to declare, Nature24); the word clean pending |
| R2, the Sagnac ratio | the receiver by name; yes (PR 1129) | yes (sagnac_k3, sagnac_rest; the `receiver` key added with the receiver by name) | not yet; after the receiver by name |
| M1, de Broglie's fringes | the lamp's ladder; yes (PR 1129) | on `main` (matter_waves_12); the sized form owed after the lamp's ladder | not yet; after the lamp's ladder |
| M2, the energy of a moving mass | none; yes | yes (matter_front_12) on `main`, but REFUSED at load (PR 1130, section 14: the matter lamp's take pair missing, a world line owed, Nature24) | not clean: no run |
| (ii-a), (ii-b), the bound clock's second term (the boxes) | none; yes | yes (moving_20, moving_28, rest_20, rest_28) | ran (PR 1130, section 15): loads, runs, reads; the word clean pending |
| the deep well in motion | none; yes | yes (deep_well_k3_40, deep_well_rest_40) | ran (PR 1130, section 16): loads, runs, reads; the word clean pending |
| the light clock of two bodies | the receiver by name; yes (PR 1129) | yes (light_clock_60; the `receiver` key added with the receiver by name) | not yet; after the receiver by name |
| (v-m), the receding index at k = 3 | none; yes | yes (index_moving_long_k3_away and its rest and reference worlds) | ran again (PR 1130, section 17): loads, runs, reads; the reader of record pairs the away world with the reference at omega, section 10 of the page paired it with omega' (the pairing to declare before any pin, Nature24); the word clean pending |
| Bell's four settings (1a to 1d) | the joint gather; yes (PR 1129) | yes (bell_a0b0, a0b1, a1b0, a1b1) | not yet; after the joint gather |
| Malus's four settings (9) | the joint gather; yes (PR 1129) | on `main` at 88b3752; the regeneration owed after the joint gather (the bar 8, no read body) | not yet; after the joint gather |
| the receding index at k = 4 | none; yes | yes (index_moving_long_k4_away and its rest and reference worlds) | ran last (PR 1130, section 18): loads, runs; its readings HELD off the page until the k = 4 pin (one-list) is on `main` |

Count at 14:55Z (main 2e1d5610): features on `main` for 15 of 15 (the
three merged in PR 1129; the owner's word of 14:00Z: the features are named,
never numbered; all three built by Nature24, one agent, on one branch);
world files on `main` for 15 of 15, three to be rewritten after their feature
(2a, M1, Malus) and one to receive its take pair (M2); test runs: eight rows
ran on main 328b560f (PR 1130), none yet carries the word "clean" against
TEST_RUNS.md (on `main` since PR 1131), and M2 refused at load; the seven
feature rows run on main 2e1d5610 now.
