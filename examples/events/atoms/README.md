# The atoms series: hydrogen at r = 12 and helium under form B

Two worlds of series H's base, written by `make_worlds.py` (which imports
series H's fan, flux count and orbit arithmetic from
[bohr/make_worlds.py](../bohr/make_worlds.py)), on the model owner's word
of 2026-09-21 (record 333, "it is important to show one atom or two, to
close all the corners"). The pins before the runs, every number labelled by
its kind, are in [docs/designs/atoms/PINS.md](../../../docs/designs/atoms/PINS.md),
printed by its host map; the runs come after form B lands, by an
experimenter, registered as rows of series H.

- `hydrogen_r12.json` (`rays-atoms-hydrogen-r12-form-b-v1`): series H's
  `r12` with the electron's momentum derived for the circular orbit under
  form B's drive (293783192 in place of 288249497), the action re-fixed
  by series H's rule under the same drive (h = 16 p(8) = 5536242544), a
  `wave` detector `at_proton` on the proton's Node, 7500 intervals.
- `hydrogen_r12_centred.json` (`rays-atoms-hydrogen-r12-centred-step-v1`):
  `hydrogen_r12.json` as registered plus the world key `centred_step`
  (centred-step-v1, off by default: the body's step fires when its
  accumulated motion reaches half the wall, the whole wall subtracted,
  so the electron's Node is the nearest to its accumulated motion) and
  nothing else; the pins before its run are
  [atom_give/CENTRED_STEP.md](../../../docs/designs/atom_give/CENTRED_STEP.md)
  section 4 (the loop stays five turns, the crossings within 9 to 20
  Links, three to four returns, the period 1400 to 2000; an escape face
  click FAIL), the cause it answers
  [atom_give/CAUSE.md](../../../docs/designs/atom_give/CAUSE.md).
- `hydrogen_r3_level.json`, `hydrogen_r7_level.json`, `hydrogen_r12_level.json`
  (`rays-atoms-hydrogen-r{3,7,12}-level-v1`): hydrogen's construction at the
  three radii where the shell mean's closure `4 sqrt(r / 12)` is nearest 2, 3
  and 4 (the generator's own closures 1.892, 3.017, 4.001 under the SAME
  action h = 16 p_B(8)), each `hydrogen_r12_centred.json`'s construction at
  its radius (the flux the electron's three Nodes receive on the ring, the
  orbit under form B's rule, the side of series H's rule, five turns of
  ticks, `centred_step`) plus the world key `atom_level` (atom-level-v1, off
  by default: the release at a closure of the difference of two closures'
  levels, the virial form) with the family `light` (the photon's, quantum 1)
  and the electron's `level` declaration (`{"family": "light", "pair":
  [512, 1], "return": [0, -1]}`); the pins before their runs are
  [atom_levels/LEVELS.md](../../../docs/designs/atom_levels/LEVELS.md)
  section 5 (the loop stays and returns; the level of the loop between the
  first and the second returns off the faces' two counts, 146, 71 and 43
  steps within 10 percent; the ratio of two lines a reported computation
  with its band; the releases and the Planck identity read from two faces;
  the control). The r = 12 world is the centred world plus the key, the
  declaration and the photon's family, integer for integer
  (`tests/test_atom_level.py`).
- `helium_r12.json` (`rays-atoms-helium-r12-form-b-v1`): binding-v1's
  square ([binding/alpha_square_bond.json](../binding/alpha_square_bond.json):
  `p` of charge 4 and `n`, each with its held `nuclear` and `bond`) fixed
  at the four Nodes about the centre, two electrons of the register's
  electron point-symmetric about it at r = 12.51 with opposite tangential
  momenta, each releasing on the fan's band |c| <= 2 and the four in-plane
  headings so that the partner's rays push it, a `wave` detector
  `at_nucleus` on the four nucleons' Nodes, 3700 intervals.

```bash
python examples/events/atoms/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/atoms examples/events/atoms/*.json
PYTHONPATH=src python tools/bohr_readings.py artifacts/atoms
```

## The baseline run of hydrogen at r = 12 as the law stands (2026-09-22)

One run, on the owner's word (record 886 on record 884 (2)), of
`hydrogen_r12.json` as registered (no new rule, no engine line, no world
file changed; the drive on `main`, form B's key not declared), the pins
declared before it and the clicks after it in
[docs/designs/atom_baseline/RUN.md](../../../docs/designs/atom_baseline/RUN.md).
A LABELLED BASELINE, not a re-registration of the pins above: the electron
widens every quarter turn (the crossings at 13, 13, 17 and 26 Links from
the proton's Node, read as the arrival Nodes of its rows on the faces,
DETECTOR) and leaves through `face:+y` at count 3407 (DETECTOR); no
return, no period and no closure are read; the dwell about the three
crossings inside r = 17 reads 20.0 counts per Link (the formula's 19.05 at
r = 12; 23.06 over all 16 hops read, FAIL as declared), the proton reads
one row per crossing (its `read` lines at 30, 442, 882, 1329, 2254; under
`read` the `at_proton` set clicks 0), the four side faces 342, 337, 342 and
339 clicks of the electron's rows; four pins FAIL, two NOT READ, one PASSES, nothing
moved; the radius from the step lines 12.00 to 27.86 (GAMEBOARD, a
diagnostic). Helium is not run. NATURE row 6 stays NOT YET.

## The three runs of the level worlds (2026-09-22)

One run each of `hydrogen_r3_level.json`, `hydrogen_r7_level.json` and
`hydrogen_r12_level.json` on the Boss's word after the physics-rule
reviewer's AGREED on the pins as written, read by kind in
[docs/designs/atom_levels/RUN.md](../../../docs/designs/atom_levels/RUN.md)
(the reader `level_readings.py` beside it, its printout, the run blocks in
[expectations.json](expectations.json)); no pin moved after the runs. The
r = 3 electron LEFT the board through `face:+x` at tick 733 (R1 FAIL: the
fan's grain at small r, a finding); the r = 7 loop stays four returns
(the first at 612 against the generator's 690, R1 FAIL by the band; the
level of its first loop 70 against 71, R3 PASS); the r = 12 loop stays five
returns (R1 and R3 PASS at the bands' edges, 1341 and 47) and releases once,
four `light` rows of content 4 at its fourth return, the Planck identity
read on the +x and +y faces (R5). Two levels give one line and no ratio:
R4 NOT READ, NATURE row 6 stays NOT YET. By the model owner's word
(record 997) these runs are the side track's record beside the paper: the
paper does not cite them as a reading of the levels.
