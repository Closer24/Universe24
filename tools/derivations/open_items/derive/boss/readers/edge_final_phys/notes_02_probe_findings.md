# Findings from my probes (all whole numbers, the engine's carry; outputs beside each .py)

## Reruns
All six of EDGE2's probes rerun byte for byte (rerun/*.txt, 0 diff lines each).

## probe_fp_root_board: the root dial on a board
- Per gear P+ - P = 4 q_F: 0 misses (the text's books hold per gear).
- Per row SUM F = 0 in 480 of 480 row-rounds (Meshes alike from both ends); SUM q_F != 0 in 230 of 480 (calibre grip, L = 3e11) and 235 of 480 (unit grip, L = 100); |SUM q_F| up to 4 and 5.
- The row's P drifts over 40 rounds by up to 36 (calibre) and 84 (toy) half-teeth units: 0 permille of a notch per site at the calibre, 1 to 7 permille at the toy.
=> Under the root dial the row's momentum (action-reaction) is not exact; the text says the force below half a root-count is lost and offers the second edge tooth, but does not say the board's books open. Immaterial in size at the calibre, not exact. MINOR.

## probe_fp_halfopen_table: section 3 under the owner's half-open convention
- Every number of the table is unchanged under half-open (v^2 W 3999 / 249 / 1000-1008; A/A0 1166 / 857 / 999; A^4 W 3433 / 1003 / 1957). Run back 0 misses of 30,000 on four courses.
- The root's "1000 to 1008" is the read of W at the step's far end: at the dial's own mean (D_in/2)^2 the invariant is 1000, 1000, 999(.75), 1000 to the permille. Presentation.
- T^2/W "988": the span of 9 beats on which T is read has mean W 33031 against the mark's 32500; at the mean W 997; at a standing clock 1000, 1000, 1001. The column measures the span, not the form. Presentation.

## probe_fp_other_route: "every grip and spring reading rest / W"
- Edge dial + push F rest / W: A/A0 1000, 1000, 1000 (nature's for a lapse); T/W 1000, 1002, 996 (T ~ W, not sqrt W); the free gear keeps W v.
- As built + scaled push: A/A0 1196, 1360 (A ~ W^(+1/2)); not nature's.
=> The route works with the edge dial, and it changes the clock's static rate law from N^2 = rest / W to N = rest / W (light's c^2 = grip rest / W^2): term 13's line and the second-order static field (beta) move with it. The text calls only the root a law change and this route "heavier". MINOR: name it.

## probe_fp_swing: where the physics sentences stop
- Hairspring beat 140 rounds at W0 = 99856, g = 201. The clock swings with period 70 (half the beat), 140, 1400 rounds, size 5 and 20 percent, 50 swings.
- Half the beat: as built x4.9 / x1280; edge x4.8 / x1419; root x1.000 / x1.000.
- The beat: all within 3.5 percent. Ten beats: all within 0.8 percent.
=> The CHOSEN edge form (and the act as built) pump a hand parametrically when the clock's swing is fast against the beat; nature's form for a lapse (the root) does not at any rate. EDGE2 says of term 9's uniform notch "under the edge every amplitude and velocity breathes within its beat": true on its adiabatic lay (ten beats), not at resonance. The law's term 9 swing is "about 140 ticks at Gamma 1,000" with its size OPEN, so the regime exists in the engine. Material to the owner's choice of the form. BLOCKING (one sentence and the probe fix it).

## probe_fp_wind: G5's line "the proper wind is D W / rest"
- Same amplitude at W and 4 W: the beat 2000 permille; SUM v^2 per beat 498 (W^-1/2); SUM W v^2 1995 (W^+1/2); SUM L v^2 997 (W^0); the phasor sum 499 (an (a, v) area again). D W / rest would be 16000.
=> Which momentum the area is read with decides whether a key counts the same quanta at two depths; the root's momentum does. No reading gives D W / rest. The line is not derived or probed. MINOR: derive or strike before G5.
