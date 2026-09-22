# The atoms series: hydrogen at r = 12 and helium under form B

Two worlds of series H's base, written by `make_worlds.py` (which imports
series H's fan, flux count and orbit arithmetic from
[bohr/make_worlds.py](../bohr/make_worlds.py)), on the model owner's word
of 2026-09-21 (record 333, "it is important to show one atom or two, to
close all the corners"). The pins before the runs, every number labelled by
its kind, are in [docs/designs/atoms/PINS.md](../../../docs/designs/atoms/PINS.md),
printed by its host map; the runs come after form B lands, by an
experimenter, registered as rows of series H. Since 2026-09-22 form B's
drive is the law's drive of a body, the line drive (the model owner's
record 972; [the design](../../../docs/designs/drive_b/DEFAULT.md)), so
the two worlds run under the drive their momenta were derived for with
nothing declared; series H's generator now derives the same integers
(`bohr/expectations.json`: p(12) = 293783192, h = 5536242544).

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

## The three worlds under the law's line drive (2026-09-22, measured against the pins of PINS.md and CENTRED_STEP.md section 4, nothing moved)

The flip of 2026-09-22 (the model owner's word, record 972; [the
design](../../../docs/designs/drive_b/DEFAULT.md), step 2, series H's
re-pin): the three worlds as registered, byte for byte (their momenta
were derived for this drive on 2026-09-21; the generator's output is
unchanged), run once each on the checkout of `drive-default` at `543d202`
(source fingerprint `e67f6b9a5469d75d`, package 0.3.1), Python 3.14.0rc2,
numpy 2.5.3, headless, `tools/run_series.py --jobs 3`; every run completed
with the books balanced at every tick, `run.json` carrying `"drive":
"line"`; the digests (state, audit, events): `80425f1adcab`,
`92077bd37aa5`, `e0ee793f1653` (`hydrogen_r12`, 126.2 s), `ac10ba004826`,
`acedae509e82`, `6bd33ee057e2` (`hydrogen_r12_centred`, 135.1 s),
`cb93a6bbed5c`, `5714d91bea4e`, `1a169e20d306` (`helium_r12`, 236.3 s).
The baseline of the section above and the centred run of
[RUN_CENTRED.md](../../../docs/designs/atom_give/RUN_CENTRED.md) stand as
registered, read under the per-axis drive; these are new rows beside them.

**`hydrogen_r12`** ([baseline_readings.py](../../../docs/designs/atom_baseline/baseline_readings.py)
against the pins P1 to P6 of RUN.md section 3, declared for the per-axis
drive on 2026-09-22 and kept as declared; the world's integers are now
series H's `r12` exactly, and the run reads as that run does): the
electron widens every quarter turn (the crossings at 12, 13, 19, 18, 16
and 23 Links from the proton's Node, the arrival Nodes of its rows on the
side faces, DETECTOR; the baseline's 13, 13, 17, 26 and out) and leaves
through `face:-y` at count 4125 (DETECTOR; the baseline's `face:+y` at
3407); one return to the +x axis at 2182, 6 Links from the start, no
second return, so no period and no closure are read; the dwell 22.00
counts per Link over 24 hops (P1 PASS within 17 to 22.5; the baseline
23.06 over 16, FAIL); the proton reads one row per crossing on four of
the six (P5 PASS: 0, 1, 1, 1, 1, 0); the side faces 418, 408, 419, 403
clicks of the electron's rows (P6 FAIL as declared: 750 less the rows in
flight); P2, P2b FAIL (one return at 6 Links), P3 and P3b NOT READ. 2
PASS, 3 FAIL, 2 NOT READ of 7 pins; nothing moved. GAMEBOARD, a
diagnostic: the radius from the step lines 11.70 to 34.71, one closing
of the angle at 2201, the per-axis action to it x 137.98, y 167.02
quotients of h (4.77 circles), the electron's phase at the closing 48.
The loop under the line drive stays longer than the baseline's (4125
against 3407) and is no more a closed one.

**`hydrogen_r12_centred`** ([centred_readings.py](../../../docs/designs/atom_give/centred_readings.py)
against C1 to C5, declared on 2026-09-22 from the map's cases T and U
under the per-axis drive and kept as declared; the world reads the line
drive started at the half wall, DEFAULT.md section (e)): THE LOOP STAYS,
C1 PASS (no escape in 7500 intervals; 19 quarter crossings, the registered
run's 23); the crossings' radii 12, 10, 11, 12, 11, 10, 12, 11, 9, 11, 14,
10, 9, 14, 11, 7, 9, 23, 12 Links (C2 FAIL as declared: one at 7 in the
fourth turn and one at 23 in the fifth; the registered run's four at 7);
four returns to the +x axis at 1401, 2822, 4232, 5542, the periods 1421,
1410, 1310 (C3 FAIL as declared: the third below 1400; the registered
run's 1431, 1500, 1150, 1040 fell to 1040), against the circle's 1490;
C5, reported and not pinned: the circles per return from the rows'
phases 4.031, 4.016, 4.094 (the closed circle's j = 4.001; the registered
run did not read it whole); C4, a GAMEBOARD diagnostic: the momentum's
length at the crossings 160 to 478 million label units (the pin 200 to
350); the proton reads 13 rows, the electron 1082; the side faces 756,
737, 752, 735 clicks. 1 PASS, 2 FAIL of the three counted pins; nothing
moved. What the run adds beside RUN_CENTRED.md, read and not claimed:
under the line drive the centred loop holds its radius for four turns
(the periods 1421, 1410, 1310 against the per-axis 1431 to 1040) and
its rows' phases sum to a whole number of circles per return within
0.1, the reading CENTRED_STEP.md section 4 named as not expected of a
wandering loop; the fifth turn widens to 23 Links and the loop is still
on the GameBoard at 7500.

**`helium_r12`** (read on the electrons' `step` lines, GAMEBOARD, and the
detectors' clicks, DETECTOR, by a host script of the campaign against
PINS.md section 3): the pinned reading was the DECAY, each electron's
momentum at the first closing of the angle 0.34 to 0.66 of the start and
the pair spiralling in or scattered within two turns. Read: the electron
at (40, 28, 27) falls from r = 12.5 to 1.6 Links of the square's centre,
is slung past the nucleus (one `contact` line at 516, GAMEBOARD: the
electron onto the nucleon `p` at (28, 28, 27), whose `measure` entry for
`e` takes the axis component p_x = -6 453 058 968, the contact rule of
2026-09-20) with its momentum 5.69 x the start at its one closing of the
angle (the tick 510; OUTSIDE 0.34 to 0.66 on the other side: the momentum
grows at the close pass instead of decaying) and leaves through `face:+y`
at 617 with 4.24 x the start; the electron at (15, 27, 27) turns 0.64 of
the angle without closing, from r = 11.5 to 32.9, and leaves through
`face:+y` at 700 with 1.30 x the start. The pair is scattered apart
within one turn, as the pin's second clause allows, but by the close pass
of one electron and not by the drag: the drag's first-order estimate is
not read on these loops. DETECTOR: `at_nucleus` clicks 0 for `e` (read,
not measured, as hydrogen's `at_proton`); the side faces 9082, 8193,
9255, 8310 clicks of the electrons' rows (the band of 2616 directions
and the four headings per release); the record check passed (completed,
the books balanced at every tick over 3700 intervals). Nothing moved;
nothing compared with nature; NATURE row 6 stays NOT YET.
