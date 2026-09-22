# Series O: two stars moving toward each other, each the detector of the other

The model owner's request (2026-09-21, in conversation, translated):
"document an experiment of two stars moving toward each other; they are
creatures from outside". The design with the expectation pinned before any
run is [docs/designs/two_stars/DESIGN.md](../../../docs/designs/two_stars/DESIGN.md);
this folder holds the three worlds it declares, written by `make_worlds.py`,
and `expectations.json`, the generator's derivation. The first run and its
readings are the design's section 7 (2026-09-21); nothing is registered.

Since 2026-09-22 the law's drive of a body is the line drive (the model
owner, record 972; [DEFAULT.md](../../../docs/designs/drive_b/DEFAULT.md)):
the generator's momenta are the line rule's (p = Q S M v / (1 - v T_D / Q):
41 021 779 276 297 at 0.2 c, 109 391 411 403 460 at 0.4 c; the per-axis
drive of history's 37 139 059 427 100 and 85 543 046 832 089, the first
run's, reproducible by `worlds(AXIS_DRIVE)`), its derivation moves a star
by (1 - v T_D / Q)^2 a / S per row (the per-axis (1 - v)^2 a / S), and
`expectations.json` names the drive. The first run of 2026-09-21 (the
design's section 7) stands as read under the per-axis drive; the re-read
under the law is the last section of this page.

## The worlds

Two of the register's stars (series G2's kind: one measured event of a paid
family holding `mass` 2^22, a lamp of one unit per self-creation) on the x
axis of a bar of 201 x 3 x 3 Nodes, sixty Links apart, thrown toward each
other at 0.2 c each (or one at 0.4 c toward the other at rest), each
measuring the other's light with `reads: "age"` and lit both ways so that a
fixed lab detector behind each star reads its outward light too; the mass
rows on the axis give the gravity of the line between them (`read`) or pass
(the control); no suspension.

| World | star A `s_px1` at x = 70 | star B `s_mx1` at x = 130 | mass | model id |
| --- | --- | --- | --- | --- |
| `symmetric.json` | +0.2 c | -0.2 c | `read` | `rays-two-stars-symmetric-v1` |
| `rest_frame.json` | +0.4 c | 0 | `read` | `rays-two-stars-rest-frame-v1` |
| `symmetric_pass.json` | +0.2 c | -0.2 c | `pass` | `rays-two-stars-symmetric-pass-v1` |

## The expectation, pinned (the design's section 3)

Under the law as built a reader at v_r toward a lamp at v_s toward it reads
1 + z = (1 - v_s / c) / (1 + v_r / c); the lab at rest reads a receding
star at 1 + v_s / c. In the symmetric frame both stars read 2 / 3 exactly
(gravity off), nature's value too; in the rest frame the mover reads 0.697
and the star at rest reads 0.581 where nature reads 0.637 for both; the
labs read 1.200 and 1.409 where nature reads 1.225 and 1.543. Under gravity
the approach speeds up (by 15 % under the per-axis drive of history, 12 %
under the line drive), the mutual 1 + z falls between the windows (from
0.650 to 0.633 per axis; from 0.653 to 0.639 under the line drive, whose
push factor is smaller), and the first contact comes at tick 237 (236 in
the rest frame) per axis, 240 (238) under the line drive, against 254 in
the control under either; at the contact the stepping star hands its
momentum to the other. The brackets, the refutation lines and what the
run cannot decide are the design's sections 3 to 5.

## Run and read

```bash
PYTHONPATH=src python examples/events/two_stars/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 3 --out artifacts/two_stars examples/events/two_stars/symmetric.json examples/events/two_stars/rest_frame.json examples/events/two_stars/symmetric_pass.json
```

The readings tool (the stars' and the labs' `click` lines, the `contact`
lines) is to be written before the run, as the design's section 6 says.
`tests/test_two_stars.py` pins the shipped worlds to the generator, the
derivation's algebra and the pinned contact ticks.

## The register entry, drafted (not registered until the model owner says so)

- **Confronts.** The owner's form of Lorentz ([record 162](../../../docs/LOG_2026-09-20.md)):
  a moving body is a detector moving over the Nodes. Two stars thrown
  toward each other, each measuring the other's light, two fixed lab
  detectors behind them; the closing speed 0.4 c in a frame where both move
  alike and in the lattice's frame where one is at rest.
- **Model prediction, pinned before the run** (the design's section 3):
  the symmetric frame reads alike, 2 / 3 exactly without gravity (nature's
  value too); the rest frame tells the two outsiders apart (0.697 against
  0.581, nature 0.637 for both); the labs read 1 + v_s / c without gamma
  (1.200, 1.409 against nature's 1.225, 1.543); gravity deepens the
  blueshift and brings the contact from tick 254 to 237; the contact is the
  hand-over.
- **The clock of the reading (the clock audit of 2026-09-22; record 678).** Each 1 + z is read
  against the reader's own clock (a star reading `age`, or a fixed lab detector
  at `suspension` 0 whose tick is its own clock, record 569); the contact tick
  and the speeds at the contact are host and step numbers, named so and not
  compared with nature.
- **Run.** 2026-09-21 on main 5cc43ae, the first run (the design's
  section 7): 17 of 24 readings of 1 + z inside and 7 outside, the three
  contacts outside (the derivation's two omissions, the mass rows' flight
  time and the drive's first Link); the symmetric frame reads 2 / 3 to
  the third digit; the rest frame reads 0.71 against 0.60 where nature
  reads 0.637 for both; the labs read without gamma; a measuring star
  gives the light it took at the contact (binding-v1), not foreseen.
  The page https://claude.ai/artifact/Sr8fRHoQyMNEPkXqbFP4Ta.

## Re-read under the law's line drive (2026-09-22, measured against the pins of expectations.json committed at a5de093 before the run)

The flip of 2026-09-22 (the model owner's word, record 972; [the
design](../../../docs/designs/drive_b/DEFAULT.md), step 2): the three
worlds rewritten by the generator with the line rule's momenta (the same
0.2 c and 0.4 c; the pins re-derived with the line drive's push factor,
committed before the run), run once each on the checkout of
`drive-default` at `a5de093` (source fingerprint `c71927e33dea0e12`,
package 0.3.1), Python 3.14.0rc2, numpy 2.5.3, headless,
`tools/run_series.py --jobs 3`, 5.0 to 5.2 s per world; every run
completed at 500 intervals with the books balanced at every tick,
`run.json` carrying `"drive": "line"`; the digests (state, audit,
events) `373f7a41c6ef`, `94477a45e5d8`, `6c9afc2bdfa0` (`symmetric_pass`),
`a7749a2f8e1c`, `92b85b75ee58`, `288fa98e038a` (`symmetric`),
`f1e814903c6e`, `78650c0597fa`, `1385b2c51177` (`rest_frame`). Read as
the first run was (the design's section 7: 1 + z from the slope of the
birth ordinal of the record's identity against the tick of the click,
the lamp's rate one birth per interval; the `contact` and `step` lines),
a reading inside within ten grains (0.03) of its pin, a contact within
the design's bracket: 19 readings inside, 8 outside (the first run: 17
and 10), nothing moved. The first run's numbers in parentheses.

| World | window | A reads B | pinned | B reads A | pinned | the left lab reads A | pinned | the right lab reads B | pinned |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `symmetric_pass` | [50, 150) | 0.6666 inside (0.6666) | 0.6667 | 0.6661 inside (0.6661) | 0.6667 | 1.2502 outside (1.2502) | 1.2000 | 1.2351 outside (1.2351) | 1.2000 |
| `symmetric_pass` | [150, 250) | 0.6672 inside (0.6672) | 0.6667 | 0.6670 inside (0.6670) | 0.6667 | 1.2046 inside (1.2046) | 1.2000 | 1.1998 inside (1.1998) | 1.2000 |
| `symmetric` | [50, 150) | 0.6648 inside (0.6648) | 0.6528 | 0.6643 inside (0.6643) | 0.6528 | 1.2502 outside (1.2502) | 1.2100 | 1.2351 inside (1.2351) | 1.2100 |
| `symmetric` | [150, 250) | 0.6546 inside (0.6517) | 0.6393 | 0.6542 inside (0.6515) | 0.6393 | 1.2046 inside (1.2046) | 1.2201 | 1.1998 inside (1.1998) | 1.2201 |
| `rest_frame` | [50, 150) | 0.7118 inside (0.7118) | 0.6992 | 0.6014 inside (0.6014) | 0.5845 | 1.4591 outside (1.4591) | 1.4053 | 1.0045 inside (1.0045) | 1.0174 |
| `rest_frame` | [150, 250) | 0.7116 inside (0.7090) | 0.6843 | 0.5962 inside (0.5929) | 0.5696 | 1.4015 inside (1.4015) | 1.4106 | 1.0000 outside (1.0000) | 1.0347 |

The first contacts (GAMEBOARD, the tick of a line): `symmetric_pass` 258
(258; pinned 254 +- 3, outside by one as before), `symmetric` 252 (251;
pinned 240 +- 5, outside), `rest_frame` 255 (254; pinned 238 +- 5,
outside), 0 of 3 inside as before: the derivation's two omissions of
section 7 (the mass rows' flight time and the drive's first Link) stand
under either drive. The control reads byte for byte what it read (the
speed 0.2 c is the design's under either drive and the control's stars
are pushed by nothing); under gravity the second window's mutual 1 + z
falls less than derived (0.665 to 0.655 read against 0.653 to 0.639
derived; the first run 0.665 to 0.652 against 0.650 to 0.633), the line
drive's smaller push factor half of the difference; `rest_frame`'s right
lab reads B at 1.0000 in the second window, outside as before. The
contact is the hand-over: in `symmetric` B (number 4) steps onto A at
252 and gives 231 units of the light it took (binding-v1, as found on
2026-09-21), the pair meeting again at 426; in `rest_frame` at 255 and
256 (223 and 253 given). Every reading of the symmetric frame alike, the
rest frame telling the outsiders apart (0.71 against 0.60), the labs
without gamma: the design's readings stand as read; nothing is
registered (the register entry above stays drafted).
