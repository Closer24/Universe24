# Findings, measured (every probe on the real act, engine/step.tick, through the blind hand's lab wiring of the
# real loader; whole numbers; the one division Rule3's carry; runaways read from outside at 10^9)

Files: q1_stress.out, q2_quantum.out, q3_generic.out, q4_frame.out, q4b_defects.out, q5_leak_{a..e}.out,
q6_flat.out (part i; part ii stalled on large integers and was killed; redone as q6b), q7_eisenstein.out, q8_00slot.out,
q9_zone.out, q10_room_gamma_{a,b}.out, q6b_board.out.

## F1. The held hand is an excited state above a massless ground state; no restoring force on |k|^2 (q1, q6 i)
- 2E = W (a-b)^2 + K a b, the act's conserved leapfrog form: E = W |k|^2 per Node-clock (q1 a, b: 2E/W = 2, 8, 18, 50
  at |k|^2 = 1, 4, 9, 25), E = 0 at k = 0. k = (0, 0) is a fixed point; matter beside it has no beat (q1 d: x stands
  at 4 for 2000 rounds, no crossing). The turn is exact at every magnitude tested, (1,0) to (1000,0), (3,4), (5,12),
  (20,21) (q6 i). So the law picks no |k|^2: "one quantum per Node-clock" is the seed's number.
- A matter quantum (D_x = 1, A = 22 at Gamma 1000) carries 2E_x/W between 0.97 and 1.92 (the floor's noise): about
  one half to one W. The held hand carries W |k|^2: one to two matter quanta per Node-clock, at every Node-clock.

## F2. Equation of state w >= 0, never -1 (q1 a)
Per round, both parts: 2E/W = 2.000; 2p/W = +2.000 (symmetric reading, w = +1) or 0.000 (now-slot reading, w = 0).
A vacuum needs w = -1. This is dust or stiff matter at rest in the lattice frame.

## F3. The zone-corner instability (q9): BLOCKING
Own spring 2W + the six Meshes' 2W on a checkerboard = 4W = the step's window's top.
- (a) k = (10,0) everywhere + a +-1 checkerboard on re, no matter: the checkerboard grows LINEARLY, |delta| = t + 1
  (1, 5, 9, 17, 33, 65, 129, 257 at rounds 0, 4, 8, ..., 256); |k|^2 from 100 to 61,009..71,289 at round 256.
- (c) k = (1,0) everywhere + a +-1 checkerboard on im (|k|^2 = 2 at every site), no matter: max|im| = t + 1;
  |k|^2 = 66,050 at round 256. The vev is one count, so this is the SMALLEST perturbation the board can hold.
- (b) (a) with a tied T1 hand at rest at A = 10 at every site: a runaway by round 16 (counts ~10^17).
- (b') the same matter without the checkerboard: bounded, |k|^2 wandering 25..136 over 256 rounds (the vev decays).
- (d) a wavelength-4 wave (+1,0,-1,0) on re: bounded to the bit (|k|^2 in 81..121 for 256 rounds).
The derivation's board layer ("laid alike everywhere the Meshes pull nothing on it") checked only the uniform mode.

## F4. Defects never heal (q4, q4b)
A single site at (0,1), (2,0) or (1,1) amid (1,0): the defect's |k|^2 cycles for 3000 rounds (1,5,5 / 4,1,2 / 2,1,4
every 100 rounds), last not-1 at round 2998-2999; its 26 neighbours stay at 1. A domain wall (4x4x4, x<2 at (1,0),
x>=2 at (0,1)) and a winding vacuum k(x) = i^x are exactly steady (64 of 64 sites at |k|^2 = 1 over 400 rounds): the
Meshes' pull of W/6 per differing neighbour is absorbed in the teeth. The vacuum's phase pattern is frozen as seeded;
nothing relaxes toward coherence; a point defect is a permanent mass anomaly of 4x to 5x at its site.

## F5. One matter quantum bends the vacuum (q2): BLOCKING for "where nature's matter sits"
Gamma 1000: exact to A = 15 (0.45 quantum at peak, g A^2 = 225); off at round 1 from A = 16 (0.51 quantum) through
A = 25 (1.25), |k|^2 in {0,1,2}; runaways from A = 28 (1.57 quanta). Gamma 4000: exact to A = 31 (0.48 quantum);
off at round 1 from A = 32 (0.51); runaways from A = 56 (1.57). The room at peak is half a quantum at every Gamma.
The beat at one quantum: 122-124 rounds at Gamma 1000 (A = 22, 23) against the claimed harmonic 140.5 (|k|^2 = 1):
13 per cent off, with |k|^2 wandering in {0,1,2}; at Gamma 4000, 241-246 against 281: 13 per cent.
Below the room the hand relaxes (P = Gamma/A + 4A: 126-130 at A = 12-15), and D_x = 1 is where the hand moves one
count a round at its peak. The mass formula is never the measured beat with |k|^2 held.

## F6. The room is not Gamma/4 (q5 d, e; q10 a)
Gamma 3200, A = 20 (g A^2 = 400 = Gamma/8): the fine tooth walks the full room [-500, +475] thousandths of W and the
turn bends at round 1281 and again near round 5000; A = 14 (Gamma/16) stays within [-140, 0] for 8000 rounds.
Gamma 1000, A = 10, 12, 14: the walk is a fixed path ([-200,0], [-336,0], [-448,0]), no leak over 80,000 rounds,
max|x| constant: inside the room the matter keeps its amplitude (SOUND).

## F7. The only generic plan ties light and the metric (q3)
Every train tied through its K x K -> A1 rows at g = 1: the T1 hand, light, the metric's 00 slot and ii slot all beat
at 266 rounds (A = 4). The 00 slot's spring 2 f |k|^2 / W = 2 / Gamma is the time gear's spring of the owner's law.
The held hand's self-tie (|k|^4, 4 f |k|^2 k_rho a round) is absorbed; |k|^2 stays 1.
The pair rule (K, A2 x K) from the tables: A2 x {A1, A2, E, T1, T2} -> {A2, A1, E, T2, T1}. The probes' trains
([A1]x2, [T1], [A1]x2) hold no pair; the example universe ([A1]x2, the metric) holds none; the text's pairs
(T1,T2), (A1,A2), (E,E) tie, and (A1,A2) is the held hand itself. A (T1,T2) train tied by the rule: both hands beat at
266: one beat per g.

## F8. The theorem of the turn presumes the Gaussian square (q7)
K = W: period 6, a^2 - ab + b^2 = 1 held exactly (a^2 + b^2 moves 1, 2); K = 2W: period 4, a^2 + b^2 held;
K = 3W: period 3, a^2 + ab + b^2 held. "The fastest steady beat the act holds exactly" (nu = 1/4) is false: period 3.

## F9. The 00 slot's tolerance (q8)
Fine tooth at rest/2 (the probes' lay): exact for -0.25 <= c/rest <= 0.49, off at -0.26. At W/2 (the deeper clock's
mid tooth): exact for -0.20 <= c/rest <= 0.33, off at -0.24 and 0.34. Not "+-rest/2". The matter's room did not
shrink for c/rest up to 0.3 (A = 8..15 all exact for 400 rounds): a deeper clock has more room (the teeth grow, the
push does not). My prior guess that gravity shrinks the room was wrong; retracted.

## F10. Probe hygiene in the text
p4b_a1a2.py uses np.linalg.det (float) and round(); lab.py uses //, % and divmod rather than the carry. Minor.

## F11. The text's own board worlds run away (q6b, q11 b): BLOCKING
p4's world (3x3x3, (A1)x2 held hand, T1 hand at rest within 1 count at every site, seed 99): |k|^2 = 1 at all 27
sites through round 200; at round 300 {0..10}, 9 sites at 1; at round 400 max 637, 1 site at 1; a count past 10^9 at
round 413. p4b's world ((A1, A2), seed 7): |k|^2 = 1 at every site through round 300 (the text's claim); at 400
max 26, 4 sites at 1; at 500 max 449, none at 1; runaway at round 510. The same one-count lay on 3x3x3, 4x4x4,
5x5x5, 6x6x6: runaways at rounds 436, 263, 282, 196 (1.4 to 3 beats of the tied hand). A one-count lay carries
about two thirds of a matter quantum per Node-clock in the Meshes alone (grip W/6, mean (dx)^2 = 4/3 over 3 Meshes
per site: W/3 against E_q ~ W/2), so there is no seed with matter on a board that keeps the vacuum.

## F12. The mechanism (q11 a, q9)
k = (10,0) + a +-1 pattern on re, no matter, 4x4x4: the (pi,0,0) and (pi,pi,0) patterns stay within 1 count for
256 rounds (K/W = 2 + 4/6 and 2 + 8/6); the (pi,pi,pi) pattern grows as t + 1 (K/W = 2 + 12/6 = 4, the window's
top). With matter the tie adds 2 g (x.x)/Gamma and the mode leaves the window: exponential (q9 b: runaway by
round 16). The held hand's own spring 2W leaves no margin at the zone corner.

## F13. Past the room at one Node-clock a stationary mixture (q10 b)
Gamma 1000, A = 20 and 24, 6000 rounds: |k|^2 at 0 / 1 / 2 for about 22 / 37 / 41 per cent of the rounds in every
500-round window; max |x| constant (20, 24). The single Node-clock is tame past the room; the board is not.

## F14. The room's resonance structure (q10 a)
Gamma 3200: A = 16 (Gamma/12) bends at round 3251, A = 20 (Gamma/8) at 1281, A = 28 (Gamma/4) at 85; A = 14, 18, 23,
25 not within 25,600 rounds. Gamma 12800: A = 40 (Gamma/8) at 4961, A = 56 (Gamma/4) at 170; A = 28..36, 46, 51 not
within 102,400. Gamma 1000: none to A = 15 within 8000. The room is not a threshold in g A^2.

## Notes on the files
- q6_flat.out holds part (i) and the first four checkpoints of part (ii); the run was stopped at round > 300 while
  grinding astronomically large integers (the runaway found by q6b). q6b_board.out and q11_board_life.out supersede it.
- q4b, q6b, q9, q11 were edited after their first run to take every remainder through the carry (g3p.rem) instead of
  %, and rerun; the first outputs are kept as *.out.run1 for comparison.
- Every probe's own divisions go through tensor24.algebra.carry.carry (g3p.quot, g3p.rem, g3p.half, g3p.thou); the
  remaining '/' in the folder are in strings and docstrings.

## F15. How little matter the board's vacuum bears (q12)
Mesh energy of the lay in matter quanta per Node-clock (E_q = W/2; grip W/6; the hand's rows summed), and the
runaway round, Gamma 1000, g 1:
- one T1 row at rest within 1 count at every site: 0.72 quanta (3x3x3) -> runaway at round 612; 0.84 (4x4x4) -> 418.
  The waves build to max|x| 13-19 first; |k|^2 then leaves 1 and runs away within ~100 rounds.
- the same at one site in five: 0.12 / 0.09 quanta -> no runaway in 3000 rounds, max|x| stays 0-1, |k|^2 = 1 at every site.
- one count at one site: 0.04 quanta -> no runaway in 3000 rounds (3x3x3).
- the text's p4 lay (three rows at one count): about 2 quanta per Node-clock -> 196-436 rounds (q11 b).
So on a board the vacuum bears about a tenth of a quantum per Node-clock, not "about one".
The reruns of q4b, q6b, q9, q11 with every remainder through the carry are identical to their first outputs.
