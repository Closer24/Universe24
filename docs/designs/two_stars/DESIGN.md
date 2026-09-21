# Series O, two stars moving toward each other, each the detector of the other: the design, with the expectation pinned before any run

The G2 experimenter, 2026-09-21, on the model owner's request in
conversation (translated): "document an experiment of two stars moving
toward each other; they are creatures from outside". Read as: each star is an
observer external to the other, and both are external to the lattice; the
experiment asks what two outside observers read of each other, whether they
read each other alike, and whether their readings show the lattice's own
frame. It is the owner's form of Lorentz made into a run
([record 162](../../LOG_2026-09-20.md): "a moving body is a detector moving
over the Nodes"), on the register's own star (series G2, the catalog's kind)
and on the law as it stands on main after the crossing rule
([note 48](../../BEAM_LAW.md)). Nothing is run here; the worlds and the
expectation are pinned so that the run, when the Boss orders it, is made
once. Nothing is registered.

## 1. The board, as an exchange of messages

Two stars on one axis of a bar of 201 x 3 x 3 Nodes, sixty Links apart,
thrown toward each other. Each star is the register's star: one measured
event of a paid family of its own (`s_px1` for star A at x = 70, `s_mx1` for
star B at x = 130; the two families of series G2's inner x stars, defined in
`entities/families.json`) holding a mass of 2^22 (the free family `mass`)
and a lamp of one unit per self-creation on BOTH headings of the axis: the
inward light reaches the other star, the outward light a fixed lab detector
behind it (`detector`, at x = 5 and x = 195). Each star's table entry for
the other's light is `{"rule": "measure", "reads": "age"}`: the star clicks
the other's light and its click line carries the row's phase and its age,
the flight time. **The star is the detector.** The lab detectors read the
outward light the same way: they are the lattice's frame, at rest. The mass
rows (64 units per direction per self-creation, series G2's gravity crowd)
go both ways on the axis; each star reads the other's (`read`, the default:
the push toward the emitter, the gravity between them) and the lab detectors
read them for nothing (fixed bodies take no push). No suspension: no clock
slows, k = 0, so what the stars read is the motion's alone.

In the board's own terms: a star sends one message per self-creation each
way, at its clock's rate (one self-creation per interval: a body's clock
runs at one at every speed, [DERIVATIONS_BEAM 4.3](../../DERIVATIONS_BEAM.md));
a message flies at c = 32 / 55 Links per interval on a heading; a reader
meets the messages it crosses (the crossing rule), so a reader moving toward
the messages meets them at 1 + v_r / c of the rate they come in at, and a
lamp moving toward its reader spaces its messages c - v_s apart so the
reader at rest meets them at c / (c - v_s). What each star reads of the
other is the count of the other's messages against its own clock.

## 2. The three worlds

| World | star A (`s_px1`, x = 70) | star B (`s_mx1`, x = 130) | the mass entry at a star | the question |
| --- | --- | --- | --- | --- |
| `symmetric` | +0.2 c toward B | -0.2 c toward A | `read` (gravity on) | the two outsiders in the frame where both move alike |
| `rest_frame` | +0.4 c toward B | at rest | `read` | the same closing speed, one star in the lattice's own frame |
| `symmetric_pass` | +0.2 c | -0.2 c | `pass` (gravity off) | the control: the motion's reading without the push |

c = 32 / 55 Links per interval (the flight table's pace on a heading); 0.2 c
= 0.11636 Links per interval; the momentum from the speed by the drive's
rule v = p / (Q S M + p), the content M = 2^22 + 2^13 (the mass and the
light), the width S = 2^20 (series G2's); 500 intervals; the windows
[50, 150) and [150, 250) before the contact. The worlds are written by
`examples/events/two_stars/make_worlds.py` with `expectations.json`; the
generator's numbers are this document's.

## 3. What each star reads, pinned before the run

The law as built ([DERIVATIONS_BEAM 2.2, 2.5, 2.6](../../DERIVATIONS_BEAM.md)):
a reader moving at v_r toward a lamp moving at v_s toward it reads

    1 + z = (1 - v_s / c) / (1 + v_r / c)          (the source's factor times the reader's count)

and nature reads one formula for both, sqrt((1 - beta) / (1 + beta)) with
beta the relative speed (the relativistic sum of the two). The lab detector
at rest behind a receding star reads 1 + z = 1 + v_s / c (the source's
Doppler alone), where nature reads (1 + v_s / c) x gamma.

**The identity of the symmetric frame.** With v_s = v_r = 0.2 c the law
reads (0.8 / 1.2) = 2 / 3 exactly, and nature's formula at the
relativistic sum beta = 0.4 / 1.04 reads the same 2 / 3: in the frame
where both stars move alike, the lattice and nature agree on what the two
outsiders read of each other, to every order. The two are told apart only
where one star is in the lattice's frame.

| World | window | v_A / c | v_B / c | gap (Links) | A reads B, 1 + z | B reads A | the left lab reads A (receding) | the right lab reads B | nature: A and B alike | nature: the lab |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `symmetric_pass` | [50, 150) | +0.200 | -0.200 | 36.7 | 0.6667 | 0.6667 | 1.2000 | 1.2000 | 0.6667 | 1.2247 |
| `symmetric_pass` | [150, 250) | +0.200 | -0.200 | 13.5 | 0.6667 | 0.6667 | 1.2000 | 1.2000 | 0.6667 | 1.2247 |
| `symmetric` | [50, 150) | +0.212 | -0.212 | 36.0 | 0.6497 | 0.6497 | 1.2123 | 1.2123 | 0.6497 | 1.2406 |
| `symmetric` | [150, 250) | +0.225 | -0.225 | 10.6 | 0.6329 | 0.6329 | 1.2248 | 1.2248 | 0.6329 | 1.2570 |
| `rest_frame` | [50, 150) | +0.409 | -0.018 | 36.0 | 0.6974 | 0.5811 | 1.4087 | 1.0176 | 0.6366 | 1.5435 |
| `rest_frame` | [150, 250) | +0.418 | -0.035 | 10.4 | 0.6805 | 0.5626 | 1.4175 | 1.0354 | 0.6188 | 1.5599 |

The speeds under gravity are the continuum derivation of the generator
(each star reads the other's 64 units per self-creation at the rate
(1 + v_r / c) / (1 - v_s / c), each unit moving the reader's speed by
(1 - |v|)^2 / S toward the emitter, [note 31](../../BEAM_LAW.md)): the
approach speeds up by 15 % before the contact under gravity and not at all
in the control. The grain of a reading of z over a window of one hundred
intervals is 0.003 (series G2's, the digital step); the brackets below are
ten grains.

**Pinned, inside or outside:**

1. **The symmetric frame reads alike.** In `symmetric` and `symmetric_pass`,
   |z_AB - z_BA| < 0.01 in every window (the law: 0 exactly; the tie of the
   frame, the lower number stepping first, moves nothing before the
   contact).
2. **The rest frame tells the two outsiders apart.** In `rest_frame` A (the
   mover) reads B at 1 + z within 0.03 of 0.697 and B (at rest) reads A
   within 0.03 of 0.581 in [50, 150): a difference of 0.116, forty grains,
   where nature reads 0.637 for both. This is the reading that shows the
   lattice's frame to two observers who, in nature, could not tell which of
   them moves.
3. **The labs read the source's Doppler without gamma.** Each lab reads its
   receding star at 1 + z within 0.03 of 1 + v_s / c (1.200 in the control;
   1.409 for the mover of `rest_frame`), where nature reads 1.225 and
   1.543: the absence of the Lorentz factor in a lamp's clock, registered
   already on G2's coasting stars (DERIVATIONS_BEAM 4.3), here at 0.4 c
   where it is 0.135 in z, forty-five grains.
4. **Gravity makes the approach faster and the blueshift deeper.** In
   `symmetric` the mutual 1 + z falls from 0.650 to 0.633 between the two
   windows (within 0.01 of each), against 0.6667 flat in the control, and
   the first contact comes at tick 237 +- 5 (236 +- 5 in `rest_frame`)
   against 254 +- 3 in the control (sixty Links closing at 0.4 c to one
   Link: 59 / 0.2327 = 253.5).
5. **The contact is the hand-over.** At the first refused step the stepping
   star (A, the lower number, steps first) hands its x component to the
   occupant ([note 31 (ix)](../../BEAM_LAW.md)): in `symmetric` both
   momenta go to 0 (+p and -p summed on B, then B's step onto A hands 0
   back: the pair stands at one Link, a `contact` record per attempt, no
   Link made after the contact, the pair held by the gravity of the line as
   the register's deuteron is by its column); in `rest_frame` A stops and
   B leaves at A's speed (the momentum transferred whole: 0.42 c, the
   speed at the contact), so after the contact B recedes from A and both
   labs and A read B as a receding lamp. The stars carry no paid content
   but their own light, so binding-v1's give ([note 40](../../BEAM_LAW.md))
   gives nothing: the contact is the hand-over alone.
6. **The reading's formula and the luminosity**, as in series G2: on every
   click line 1 + z from the phase's slope against the tick equals the
   rate of the rows against the emitter's within 2 %; the click rate is
   1 / (1 + z) of the lamp's rate within 5 % (a blueshifted star is seen
   brighter by the count, no distance enters).

## 4. What would refute the reading

- If `rest_frame`'s two stars read each other alike (|z_AB - z_BA| < 0.03),
  the law has a symmetry the derivation says it has not; then either the
  crossing rule does not count as pinned or the lamp's clock slows with its
  motion, and DERIVATIONS_BEAM 2.6 and 4.3 are wrong.
- If the symmetric stars read each other unlike (> 0.03), the frame's tie
  (the number order of the steps) or the fan's discreteness moves a reading
  before the contact: a defect of the experiment's symmetry, to be found on
  the GameBoard before any physics is read.
- If a lab reads its receding star nearer to nature's 1.225 than to the
  law's 1.200 (by more than a grain), a factor entered a lamp's rate that
  none of the six operations of the law carries (record 197); the run is
  then evidence for a clock in motion that the derivation excludes.
- If the control's contact falls outside 254 +- 3, the drive's speed is not
  p / (Q S M + p) on this world (the one motion primitive of record 183, if
  it has landed by then, changes the pace of a body on a heading by nothing
  and this pin stands).

## 5. What the run cannot decide, and what it is for

It cannot decide whether Lorentz holds in nature; it decides what this law
gives two moving detectors and whether the lattice's frame is visible to
them: by the derivation it is, in one-way readings (the mutual and the
lab's), at first order in v / c, and the symmetric frame hides it exactly.
The same two stars are the world for lorentz-v1 when it is built (record
183, 197: a body's counts slowed by isqrt(D^2 - p^2) / D as a hypothesis
with its own identity): under it the labs would read 1.225 and 1.543 and
`rest_frame`'s two stars would move toward 0.637 from both sides; the
expectation for that run is to be pinned from its FORM.md before it is
made, not from this table. The design's numbers are the law's as built on
main at 5cc43ae (the crossing rule, the fraction-free counts, no key).

## 6. The run, when ordered

    PYTHONPATH=src python examples/events/two_stars/make_worlds.py
    PYTHONPATH=src python tools/run_series.py --jobs 3 --out artifacts/two_stars examples/events/two_stars/symmetric.json examples/events/two_stars/rest_frame.json examples/events/two_stars/symmetric_pass.json

The readings tool is to be written before the run and to read the engine's
own record only: the stars' `click` lines (`measured` the reading star,
`family` the other star's light, `phase`, `reading` the age moment, `tick`),
the labs' `click` lines the same way, the `contact` lines (the tick, the
component handed) and the `step` lines for the speed on the GameBoard as a
labelled control; z per reader per window from the least-squares slope of
the unwrapped phase against the tick with the lamp's rate rho = 1 step of N
per self-creation, exactly as `tools/hubble_stars_readings.py` reads the
detector's lines; the criteria of section 3 inside or outside; an HTML page
published as an artifact. Every number above is a detector reading except
the speeds and the gap, which are the GameBoard's.
