# FACE, the hostile physicist's report, 2026-10-31 (read 01:37 to 01:55 UTC)

(Written by the Boss from the reader's hand-back, the reader's harness having refused the write; the text is the
reader's, shortened in layout. Read: FACE.md in full (344 lines), face_lib, face_p1_gear, face_p2_act; face_p1_gear
rerun byte for byte. The reader's probe: fc_phys/fc_phys_p1.py with fc_phys_p1.txt, on the engine's lone gear
(step.gear) with FACE's own face_lib unchanged; whole numbers, Rule3's carry the one division, every window stated.)

VERDICT on FACE.md: NOT PASSED

## BLOCKING

B1. The face does not count a clock's proper time once the clock has more than one row (section 0; 1.1 and 1.2 "the
clock's own half beats"; 5.1).
- The face adds the zero crossings of each of the train's rows (C_h is a sum over rows), so its count per beat depends
  on how the clock is turned and polarized, not on its beat alone.
- MEASURED (fc_phys_p1 D3: spring 1,500,000, W = rest, rounds 1 to 40,000; lone gears summed as face_lib.crossed sums
  a train): one oscillation along one row 637; the same oscillation turned by the whole rotation (3, 4) / 5, |x|^2 =
  10^12 in both (any row-blind spring keeps it), 1,274; three rows alike 1,911; a second row laid 1, 3, 30 or 300
  counts from 0 adds 99, 288, 630 or 637.
- The 24 keep the face (T3) only because they are signed permutations. The click world's giver is a three-row hand
  laid at (20, -11, 7); its face counts 2 per beat for every row that crosses.
- A clock whose count changes under a rotation its own law keeps breaks special relativity's isotropy: "D6 twice" would
  fail between two clocks of one kind at one place laid in two orientations.
- Fix, one of: limit the face to one-row clocks (A1, A2) and say so in sections 0 and 5.1; or derive a crossing that is
  the same in every orientation, one count per half beat (a candidate: the sign of the train's dot product with a held
  copy of its lay, which crosses twice a beat in any orientation and polarization; owed). Either way, name the
  crossings per beat in the header.

B2. Sections 0 and 5.1 claim physics on a board reading alone, and the board refutes it ("Against the two theories, a
standing clock's D6 is its face", section 0; "The theories ask nothing more of it at one Node-clock", 5.1).
- Besides B1, near a notch the face depends on the clock's amplitude. MEASURED (fc_phys_p1 D1: spring 120,000, the
  giver's stride; W = rest; rounds 1 to 82,000): lays 10, 20, 40, 80, 160 give 158, 283, 400, 368, 363; far above a
  notch (lay 10^6) 369. Two clocks of one kind at one place can differ by up to 2.5 times.
- Fix: 5.1 states what the theories ask (the count does not depend on the clock's orientation, its amplitude or a
  neighbour's wave; two clocks of one kind at one place agree, read twice in the click world), then says the face
  meets this only for a one-row clock far above a notch, and only as MEASURED ON THE BOARD.

B3. Three sentences read a board wave as light (the owner's word of 01:4x: the board has no light).
- L1, section 0 lines 51-52: "light's two-way count is alike along the three axes by the 24 for a standing clock,
  elsewhere only in long waves".
- L2, 5.2 lines 281-284: "Light's two-way speed. A clock's echo count to a mirror a fixed number of Meshes away. For a
  standing clock it is alike along x, y and z by the 24 ... in long waves".
- L3, 5.4 lines 294-296: "The act as built gives every spring's beat and light's the same factor sqrt(rest / W) ...
  (one redshift for every clock, to the calibre)".
- L1 and L2 rest on the 24's equivariance of a board wave, which cannot fail; L2 also measures with "a fixed number of
  Meshes", a board length (the click world reads space only through the echo: the arms must be one mirror held by a
  clock and turned between directions). L3 calls a board dispersion "redshift", and is wrong as a board statement in a
  well: the engine reads the dial as W = rest + k0 c00 and the grip as grip_rest + ii (plans.py term 5; load.py line
  231), so a board wave's speed factor is (grip / W)^(1/2) and a beat's (spring / W)^(1/2); they agree only where
  ii = 0.
- The reader's measurement overturned the reader's derivation: on paper one shared factor gave half of general
  relativity's echo delay (gamma = 0); the engine's code carries the ii part, so that objection falls. Under the
  owner's word the echo is a click-world reading anyway.
- The light sentences at lines 50, 286-291, 314 and 323 are sound under the owner's word (light's links as click-world
  readings, owed).
- Fix: strike L1 and the light clause of L3; recast L2 as an owed click-world reading (echo counts between clocks, the
  arms one held mirror turned); name the board symmetry as the 24's equivariance of a board wave, without light.

B4. T6's "cannot" holds only at one value of a file integer, not for the law (section 0, T6 in bold; section 6 OPEN 1:
"no world of tonight's clicking law can be laid far above a notch").
- DERIVED from FACE's own scaling formulas (not measured): room |x|^2 at most about Gamma / (2 hold |k|); beat w^2 =
  2 hold |k|^2 / Gamma; so the stride is at most about sqrt|k|, and staying far below the cutoff needs
  |k| << (Gamma / 2 hold)^(1/2). Together a stride bound growing as (Gamma / 2 hold)^(1/4): about 8 counts a round at
  Gamma = 10^4, 80 at 10^8, 800 at 10^12.
- Gamma is the universe file's integer full_rate: 10,000 for the click world, 1,000 in examples/tensor24-well. A5 scaled
  the lay 25,000 times at a fixed Gamma (the push grows as the cube of the lay, so the world must leave the room); A5
  does not test Gamma.
- Fix: state T6 at Gamma = 10^4 with its Gamma^(1/4) law; probe the click world at a larger full_rate
  (rest = 6 den Gamma^2) before writing "cannot".

B5. The record line's header carries a sine formula in the design (the header names the rest beat as the pair [g, W]
"of 4 sin^2(w / 2) = g / W").
- 5.4 says two kinds' faces "compare only as a ratio of beats". The pair is whole numbers, but its stated meaning is an
  angle defined by a sine, and its one stated use (the ratio of two kinds' beats) needs arcsin((g1 / 4W)^(1/2)) /
  arcsin((g2 / 4W)^(1/2)) or, in long waves, the root (g1 / g2)^(1/2): a construction that finds a sine or a root (law
  line 102).
- Fix: name the beat as the act's own step ("[g, W]: the gear's step a+ + b = (2 - g / W) a, its trace deficit
  g / W", or the pair [2W - g, W] if a trace is wanted); two kinds' beats compare only by counting (two clocks of the
  two kinds at one place, between two common meetings, as SHADOW read N = sqrt(rest / W) by counting), never from the
  pairs.

## What T6 costs at tonight's Gamma (MEASURED ON THE BOARD, fc_phys_p1 D1, D2)

- The redshift test at the giver's stride (spring 120,000, rounds 1 to 82,000), faces at W, 4 W and 16 W: lay 40 gives
  400, 141, 39 (each fourfold dial a ratio 2.84, then 3.6; the continuum gives 2); lay 10 gives 158, 41, 10 (about 4:
  the face goes as 1 / W, the square of the dial, FACE 4(c)'s law for the release); lay 10^6 gives 369, 185, 92 (2.0).
  So a redshift read twice on tonight's law would measure the integers' lock, and that lock depends on the amplitude.
- The held hand at its spring of 2 rest, at 1, 4 and 16 rest: faces 200, 92, 45 (ratios 2.17 and 2.04: arccos(3/4)
  and arccos(15/16) against a quarter turn); its exact quarter turn, which the room rests on, holds only at W = rest;
  with the spring scaled as 2 W instead the faces are 200, 200, 200: it reads no depth. The click world's only steady
  face is the held hand's (face = round, A1): either it reads no depth or it loses its exact turn. So tonight's
  clicking world cannot be laid at a second depth as it stands.
- The click world's time in general: D6 reads the lock, not the clock; the twins need a bound pair that clicks
  steadily, and tonight's pair clicks in runs of 1 to 7 lines. The way out is B4's Gamma.

## Big Pic or FACE

- Big Pic is right in principle: in the click world a clock's own count between two meetings is the number of its own
  events between them. For a clock whose ticks are clicks (his bound pair; in physics a light clock) it is read from
  the click lines alone: count the lines that name it between the two meeting lines, no gear and no round. It is the
  only count that follows a moving clock (FACE's own 5.2 concedes it), and the only one the owner's arrangement
  (events only) lets physics use.
- FACE is right in fact for tonight's act: no steady clicking clock exists, beats are not clicks, nothing in the act
  counts them; so a standing gear's beats reach the lines only through a held count. But the face is a register of the
  board's rows (B1), so D6 on it is a clock fix, not yet a click-world clock.
- Relativity does not ask for the extra gear; it asks for a clock's count of its own events. The face is needed only
  because tonight's law has no steady clicking clock. Big Pic's road is the physics; the face can stay as a board clock
  fix for one-row standing clocks.

## Is the face nature's proper time?

- For a standing clock: only for a one-row gear far above a notch, in a pure mode, with no other wave of its train at
  its site; there it is proper time in half beats, to one half beat, MEASURED ON THE BOARD (637, 318, 159, an exact run
  back; D1's reference 369, 185, 92). Not for a train of several rows (B1), near a notch (B2, D1), or at a site where
  another wave of the same train passes (5.2's own carrier).
- For a moving clock, owed: a clicking clock that ticks steadily far above a notch (B4), set moving by the act, not
  laid (M2), named by its lay, its clicks counted between two meetings with a standing partner, read twice; agreement
  with special relativity only in long waves (M3).

## MINOR (one line each)

- M1 (5.3): the depth must come from a well (c00 sourced by a mass through term 5); a W laid by hand only re-reads G1's
  dispersion, so that reading cannot fail.
- M2 (5.2): a slowly moving clock cannot be laid in whole numbers (a whole carrier exists only at the crystallographic
  traces 2, 1, 0, -1, -2; a Pythagorean pair aimed at a small angle is a constructed cosine); the twin must be moved
  and turned by the act.
- M3 (5.2): "the pair's own E^2 = p^2 + m^2" holds for the lattice's dispersion only in long waves and depends on
  direction at order k^2 (no boost); write it as owed.
- M4: the face counts at a place (site, train), not on a clock; D6 needs one mode per (site, train) at both meetings
  (a hypothesis to state).
- M5 (G1, T5, Q4, 5.3): W, 4 W, 16 W are dials on the board; "depth" is a click-world word.
- M6 (section 0): "counting down ... like a time": the run back is the rewind; say D6 on the run back is positive
  ([-f+, -f]).
- M7 (Q4): "nature's hands have none" puts a board fact (no unit step off the five ratios) in a physics word.
- M8 (T6): "D6 on any record of this law reads the act's rhythm about a notch" predicts a click-world reading from a
  board scaling; label it a forecast (and see B4).
- M9 (OPEN 7): "along the Spokes and the diagonals" uses board directions for a click-world reading.
- M10 (outside FACE, for the Boss): the engine's own comments (load.py line 231, plans.py term 5) name a board wave as
  light ("GR's gamma = 1 for light").

## SOUND

- T1: the exact count of row crossings, 4 f + r = 2 V + v(lay) - v(last), at three dials.
- T2: the run back exact round by round, 0 of 4,000 at both strides; 40,000 unticks return exactly (rerun confirms).
- Q2: |s + t| + |t - s| = 2. T4: the face changes nothing in the act. Q4: a unit's step reads no depth (D2: 200, 200,
  200).
- 5.2's no is correct physics: a fixed Node-clock's face counts the lab's carrier at the rate w / pi; a moving clock's
  own count runs at (w - k v) / pi = m sqrt(1 - v^2) / pi, since E - p v = m / gamma; so no face at a site is a moving
  clock's count.

## DERIVED / MEASURED / OVERCLAIMED

- DERIVED and sound: T1, T2, T3 (for signed permutations), Q2, 5.2's no. DERIVED but scoped too wide: T6 (Gamma = 10^4
  only, B4).
- MEASURED ON THE BOARD and sound: G1 to G6, A1 to A4, the reader's D1 to D3.
- OVERCLAIMED: sections 0 and 5.1 (B1, B2); "the face counts the clock's own half beats" for trains of several rows
  (B1); 5.4's "one redshift for every clock" and "light's the same factor" (B3); L1 and L2 (B3); T6's "no world" (B4).

## Questions for the Boss

1. Is full_rate (Gamma) free in the universe file? If so, T6 is a no at 10^4 only, and a click world at full_rate 10^8
   to 10^12 is the first probe for a clicking clock far above a notch.
2. Is the face meant for one-row clocks only, or must it count one crossing per half beat for any train?
3. In a well (W = rest + k0 c00), does the held hand keep its exact quarter turn (K = 2 W)? D2 shows a spring of 2 rest
   at a dial of 4 rest is no unit step.
4. How is a moving clock set moving without a constructed cosine: by the act alone?

## Solution24

Not passed for physics. The face is a sound board register for a one-row standing clock far above a notch (637, 318,
159, an exact run back). It is not proper time for the click world's clocks of several rows, nor at their stride.
Three sentences read a board wave as light. T6's "cannot" holds only at full_rate 10^4, and the text's own scaling
lifts it as Gamma^(1/4). Big Pic's road, a clock's own clicks, is the physics; the face is a clock fix beside it.
