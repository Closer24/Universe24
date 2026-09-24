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
| F1, the receiver by name | the key `receiver` on every emitting block, the record's ladder that one cell, the gather line at the cell's first rung, the other sinks booked to `escaped`, the emitter's own cells taking on no pointer at every age | 4b, R2, the light clock | Nature24 (the owner's word of 13:03Z: one agent writes all the code) | not yet on `main` |
| F2, the joint gather and Malus's two cells | one gather of the pair record on the four joint cells, the polariser a table body of two cells with the offer split over the tables | Bell's four, Malus's four | Nature24 | not yet on `main` |
| F3, the lamp's ladder by name | the declared sinks outside a lamp record's ladder, the cell chosen over the ladder's own sum, the screen's sets' own rung wheel | 2a, M1 | Nature24 | not yet on `main` |

Item 10 at T = 0 and the cell-index guard (PR 1115, merged at 328b560f) are
on `main` and are not counted as a feature owed.

## The fifteen

| Experiment | 1. Engine features (which; on `main`?) | 2. World file (on `main`?) | 3. Test run without a pin (clean?) |
| --- | --- | --- | --- |
| 2a, the two slits | F3; not yet | first draft on `main`; the second draft (L-3) owed after F3 | ran on the first draft: 0 screen clicks, every record gathered behind the lamp (record 1798); not clean; re-run after F3 on the second draft |
| 5a, the anisotropy of c (the pace fans) | none; yes | yes (pace_fan_12, _16, _24 at 88b3752) | not yet (the Preliminary Runner, 12:35Z) |
| 4a, the muon's form (the layer pin world) | none; yes | yes (layer_pin_rest_14, layer_pin_k3_14) | not yet (the Preliminary Runner) |
| 4b, the redshift of the moving lamp | F1; not yet | yes (redshift_k3, redshift_control; the `receiver` key added with F1) | not yet; after F1 |
| 4c, the round trip off a receding transponder | none; yes | yes (cart_k3) | not yet (the Preliminary Runner) |
| R2, the Sagnac ratio | F1; not yet | yes (sagnac_k3, sagnac_rest; the `receiver` key added with F1) | not yet; after F1 |
| M1, de Broglie's fringes | F3; not yet | on `main` (matter_waves_12); the sized form owed after F3 | not yet; after F3 |
| M2, the energy of a moving mass | none; yes | yes (matter_front_12) | not yet (the Preliminary Runner) |
| (ii-a), (ii-b), the bound clock's second term (the boxes) | none; yes | yes (moving_20, moving_28, rest_20, rest_28) | not yet (the Preliminary Runner) |
| the deep well in motion | none; yes | yes (deep_well_k3_40, deep_well_rest_40) | not yet (the Preliminary Runner) |
| the light clock of two bodies | F1; not yet | yes (light_clock_60; the `receiver` key added with F1) | not yet; after F1 |
| (v-m), the receding index at k = 3 | none; yes | yes (index_moving_long_k3_away and its rest and reference worlds) | ran (PR 1123, section 10): readings recorded, the gap to the declared phase to be explained before any pin; re-run by the Preliminary Runner |
| Bell's four settings (1a to 1d) | F2; not yet | yes (bell_a0b0, a0b1, a1b0, a1b1) | not yet; after F2 |
| Malus's four settings (9) | F2; not yet | on `main` at 88b3752; the regeneration owed after F2 (the bar 8, no read body) | not yet; after F2 |
| the receding index at k = 4 | none; yes | yes (index_moving_long_k4_away and its rest and reference worlds) | not yet (the Preliminary Runner, last; its readings held until the k = 4 pin of one-list 2bcadd7f is on `main`) |

Count at this writing: features on `main` for 8 of 15; world files on
`main` for 15 of 15 (three to be rewritten after their feature: 2a, M1,
Malus); a clean test run for 0 of 15.
