# Series O: two stars moving toward each other, each the detector of the other

The model owner's request (2026-09-21, in conversation, translated):
"document an experiment of two stars moving toward each other; they are
creatures from outside". The design with the expectation pinned before any
run is [docs/designs/two_stars/DESIGN.md](../../../docs/designs/two_stars/DESIGN.md);
this folder holds the three worlds it declares, written by `make_worlds.py`,
and `expectations.json`, the generator's derivation. The first run and its
readings are the design's section 7 (2026-09-21); nothing is registered.

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
the approach speeds up by 15 %, the mutual 1 + z falls from 0.650 to 0.633
between the windows, and the first contact comes at tick 237 (236 in the
rest frame) against 254 in the control; at the contact the stepping star
hands its momentum to the other. The brackets, the refutation lines and
what the run cannot decide are the design's sections 3 to 5.

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
