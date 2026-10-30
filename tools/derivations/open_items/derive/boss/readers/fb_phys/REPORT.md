# The hostile physicist on the escapement (FWDBACK.md)

The report as the reader gave it, 2026-10-30, filed by the Boss (the reader's harness refused the file). Probes
probe_p1_onesite .. probe_p6_step with their .txt; notes_01_derivation.md, notes_02_measured.md, notes_03_runaway.md.

VERDICT on FWDBACK: NOT PASSED

The harness refused to write REPORT.md, so the full report is this message. Everything else is in /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/fb_phys/: phys_lib.py, probes probe_p1_onesite, p2_phase, p2b_phase_check, p3_gradient, p4_lever, p5_unstable, p5b_caseH, p5c_textact and p6_step (each .py with its .txt), rerun_text/, rerun_live/, and notes_01_derivation.md, notes_02_measured.md, notes_03_runaway.md.

How it was run: t24b/.venv/bin/python -I -B; whole numbers; tensor24.algebra.carry.carry the one division; no float, root or true division. Every number of mine is on t24b (9067de20d). The text's five probes rerun byte-identical there. Under node-live (939fa65a7) probe_fb1 is identical; the board probes stop at load (KeyError 'chosen').

In short: on ONE Node-clock, or wherever every Node-clock releases on the same rounds, the escapement is nature's for a uniform lapse at every velocity, the count level included. Where neighbours release on different rounds, the act runs away exponentially, on the text's own code, inside its promise. The text read the first 400 rounds of that runaway as "the lapse gradient's force, nature's".

ITEMS

1. BLOCKING. Where neighbours release on different rounds, the act runs away exponentially.
   - Place: s.4 ("a stepping site reads its neighbours' now slots whether they step or stand"; "-249,248 grips ... the lapse gradient's force, nature's"); s.0 ("non-uniform clocks"); s.7 steps 6 and 7 ("none found").
   - The text's own act with nothing held from outside (P5c A: fb_lib.tick_board, example universe, 1 x 1 x 16):
     - The clock is UNIFORM and standing at L = 2 L_0. The escapement's teeth are lawful but staggered: tau = 0 on half the line, and the promise holds at every round.
     - The light row's oscillation goes from 6 to 306 bits and its proper energy from 91 to 687 bits in 20,000 rounds (e-fold about 100 rounds).
     - With the teeth alike (the text's own lay) it stays at 6..8 and 91..92 bits.
   - The text's case H is this runaway (P5b):
     - The light row's largest |a| goes 1000 -> 136,755 in 400 rounds; SUM P reaches -249,248 grips.
     - With both clocks equal (both 0, or both 12 grips) it stays at <= 1160 with SUM P exactly 0.
   - On a standing clock, in the ring model (the text's act on one row; 0 misses in 60 rounds against tick_board on a moving non-uniform clock, P3 A), with the deep half at L_0 (1 + e), the energy grows (P5 B):
     - e = 1: x2^59 in 2e4 rounds; e = 1/2: x2^42 in 2e4.
     - e = 1/10: x2^26 in 4e4; e = 1/100: x2^12 in 2e5; e = 1/1000: x1.86 in 4e5.
     - A smooth 10 % well: x2^389 in 4e4.
     - Equal clocks with staggered teeth: x2^146 in 2e4 (P5 C).
     - The aligned controls stay flat: 978..1081 permille.
   - On the same sharpest lay, the act as built and nature's divergence form hold at 19 bits throughout (P5 D).
   - The rate is about 6..8 bits of energy per 1000 rounds in which a Mesh's two ends release apart.
   - The clock itself runs away too (P5c B, P5 A):
     - With the 00 laid at L = 3 L_0 +- 1 grip, the 00 row's SUM P falls in only 39 of 4000 rounds.
     - The mean clock goes from 36 to 7,747 grips in 4000 rounds, and to about 3700 L_0 by 20,000 rounds.
     - Each site then makes 156..159 releases, against 6667 on the uniform control: the board's time freezes.
     - On paper: d_t SUM P_00 = grip L_0 SUM_links (dc)^2 / L^2 >= 0.
   - Why (derived):
     - A Mesh's pull reaches each end only at that end's own release.
     - When the ends release apart, one end is kicked from the other's held count, and the reaction lands on another round.
     - A kick of one end alone is no symplectic map. The act stays volume-kept and reversible (its run back is exact), so its multipliers leave the circle in pairs.
     - The continuum limit (masses N^-2) is stable. The event structure is at fault, not the equation.
     - My notes_01 predicted a bounded average book; my own measurement overturned it.
   - The text's probes never ran a non-uniform clock past 40 rounds, except case H.
   - Fix: a Mesh's impulse must land on both of its ends at one event (for instance each Mesh released by its own escapement at the link's clock, its impulse given to both ends). Show that bounded by windows over >= 10^4 rounds on the lays above: the uniform clock with staggered teeth, a contrast sweep, a smooth well. The Mesh-tooth text now being written must pass exactly these. Strike "nature's" from s.4 and step 6.

2. BLOCKING. Even before the runaway grows, the board's equation where clocks differ is the act as built's, not nature's. The "force" is wrong in size and in kind. Big Pic's finding, which you asked me to measure here, belongs to this item.
   - Place: s.4; s.7 step 6 ("nature's where the clocks differ"); "which the act as built does not have".
   - Nature (derived): a massless field on a static lapse with flat slices (the covariant scalar, and Maxwell with eps = mu = 1/N alike) obeys d_t(N^-1 d_t phi) = div(N grad phi). So SUM pi is EXACT (pi = N^-1 d_t phi, which is the escapement's P / rest). The impedance is 1, so nothing reflects at a lapse step.
   - The escapement (derived):
     - Its pull per proper step at the standing grip gives d_t(N^-1 d_t phi) = N kappa Lap phi, which is nature's minus kappa grad N . grad phi.
     - On a standing clock that is N^-2 d_t^2 phi = kappa Lap phi: the act as built's static equation. The act as built keeps that equation's book exactly; the escapement's does not stay.
     - Nature's 0 is thus replaced by -grip SUM_links dN da.
   - Structural (derived): nature's pull per proper step of x weighs each Mesh by N_xy / N_x = 2 L_x / (L_x + L_y). That is a division at a dial moving with the clocks, so Theorem 1's hypothesis (H) returns for the Mesh's part. The escapement removes (H) only where the clock is uniform across every Mesh.
   - Measured, the Boss's case, a step N 1 -> 4/5 (P6; pulse widths 40 and 80 give the same figures):

     | act | reflected (permille) | transmitted (permille) |
     |---|---|---|
     | escapement | -90 | 901 |
     | act as built | -112 (continuum -111) | 879 |
     | nature | -1 | 989 |

     Big Pic's 98 permille is this same effect. His mend, a tooth on each Mesh, belongs to the second text and was not measured here.
   - Measured at N 1 -> 1/2 (P6, P3 C): escapement -284 / 710, act as built -335 / 659, nature -4 / 989.
   - Derived (WKB): a packet entering a well keeps its proper energy, so its quanta fall as N; nature keeps them.
   - Fix: write the non-uniform board's physics as the act as built's (the lapse in the inertia only). Name the Mesh weight 2 L_x / (L_x + L_y) OPEN, with its remainder (the Mesh tooth is the candidate). Strike "nature's" and "which the act as built does not have".

3. BLOCKING. The lapse's own equation is chosen, not read; tg_phys item 2 applies here unchanged.
   - Place: s.5 "the 00 row needs no law of its own beyond riding the escapement"; s.7 step 3 "CHOSEN nowhere"; step 10 "the 00 row's own law ... retire".
   - Measured (P1 C): the free 00 gear from u = 1 count a proper step keeps L c', which is sqrt(W_eff) c'.
     - L^2 / (L_0^2 + 2 L_0 t) = 999..1000 permille from t = 10^3 to 10^6 rounds (W_eff x101). This is k = 1/2, TIMEGEAR's own choice.
     - Against it at 10^6 rounds: k = 0 gives 197, k = 1/4 gives 175 (in L^3), k = 1 gives 6722 permille.
     - The text's own fb1 A (c00 = 20,000 at round 30,000) is the same course.
   - On paper: the covariant action of a lapse-sourcing field keeps sqrt(L) c' (k = 1/4), and GR gives a uniform lapse no equation. "The clock's field ticks with its site" is an argument for a choice, not a reading of nature. On a non-uniform clock it also adds the one-signed drive of item 1.
   - Fix: write CHOSEN with that argument; put k = 0, 1/4, 1/2, 1 to the owner on their consequences; strike "CHOSEN nowhere" and "retire".

4. MINOR. The half-step phase is bounded on a monotone course but secular under a swing.
   - Place: s.6 item 4 ("no secular rate; a swing moves it back and forth").
   - Monotone courses (P2, P2b):
     - I read the releases as n + tau/D (the escapement's own continuous phase) against SUM L_0 / L(now).
     - The offset moves +95, -100 and +701 milli-steps at L x2, L /2 and L x10.05. All three sit within the text's (1/2) ln bound of 347, 347 and 1151.
     - The exact identity, 1/2 + S' - SUM tau dL / (2 L L), holds term by term.
   - Swinging courses, with the 00 gear on its own spring (swings of 363, 115 and 14 proper steps):
     - The offset drifts -2.6, +1.6, +4.9 and +8.6 milli-steps a swing.
     - The rates are steady over 2.4e6 rounds: 5e-6 .. 6e-4 of the clock's rate.
   - Against the clock's own course in proper steps (the trapezoid of D) the phase is bounded by construction.
   - My own paper sum was corrected by this measurement (it lacked the tooth's term).
   - Fix: state the reference, and say "a swing drifts it at second order in the clock's change per step".

5. MINOR. Light crossing a well gets the lapse-only delay.
   - Measured (P3 D): through 200 sites at N = 4/5, all three acts give 123 rounds (delay^2 15129 against the paper's 15000). The redshift between two depths is exact (the release rate L_0 / L).
   - This is gamma = 0: half of GR's Shapiro delay and bending at weak field. The spatial part belongs to the ii slots (G2).
   - Fix: say "lapse only" where s.5 says "one cone" and s.0 says "nature's".

6. MINOR. The domain and the lever.
   - The domain c >= 0 loses every clock faster than the rest: a void or hill against the reference, a 00 wave about a mean at rest, a clock that speeds up. For example, a free clock falling at 1 count a step from c = 20,000 leaves the domain at round 30,000 (P1).
   - The lever is sound as arithmetic only with the push 4 rest m (so the text's "2 rest m" must be per slot) and L_0 = 2 rest m^2 (P4):
     - At rest it releases at rate 1/m: 6000 and 4000 of 12,000 rounds at m = 2 and 3.
     - At c = -2 rest m (m - 1) it releases every round.
     - The run back is exact into c < 0: 0 misses over 15,001 and 40,001 rounds, rewound.
     - Beyond the edge the escapement turns 2.
   - Its cost: at rest every gear stands m - 1 rounds of m, light per round falls to 1/m, and neighbours whose clocks differ by one count release apart everywhere, which spreads item 1 everywhere.
   - Fix: name the push per slot, and name that cost.

7. MINOR. Two clocks at one site (s.5 table "2012 .. 2016") is a window artefact: periods of ten-period spans of different lengths on a rising clock.
   - In releases the periods are 62..63 and 31..32 on every course, with amplitudes identical across courses.
   - In rounds, 317 against 634 beats over one window (P1 D).
   - Fix: count in releases.

8. MINOR. Case H is mislabelled. The clocks went from 12 and 24 grips to 770 and 838 grips under the 00 row's own pull (P3 F), so the run was not "two sites at c = 0 and 12 grips". Fix: report the clocks; see item 1.

THE LAW AS I READ IT (docs/ALGEBRA.md on origin/main)
- Line 35: "every whether a quotient and no if".
- Postulate 5: "a dial whose whole turn leaves as an event", and no mask or branch in any act.
- Line 106: a mask is "an indicator that zeroes a term above a bound is a bound spelt as a quotient".
- My reading: q_tau is the escapement's own whole turn, with tau kept. While q_tau is 0 or 1 it is a whether, not a mask. But x + q_tau (y - x) selects the stepped state, and at q_tau = 2 it is not two steps. So it is a whether only inside the promise.
- Locality: a neighbour of a Node-clock that stood reads its held now slot. That is lawful and local, and it is the cause of item 1.

SOUND, with numbers
- One Node-clock, or a uniform clock: the release-sampled states equal the standing act's, with 0 misses in 15 courses (rising, falling and swinging; with v_p = 1, a sub-notch momentum, g = 1 at a0 = 3, g = 100 at a0 = 10, and push 1). Nature's test for a uniform lapse holds at every velocity, the count level included.
- No lock-in of its own:
  - In rounds the velocity passes below one count a round while L v / L_0 stays at 999..1000 permille.
  - The free 00 gear follows its own class's course for 10^6 rounds, where the time gear locked at one count a round.
  - The sub-notch freeze is the standing act's own; as built is the same.
- No pump at any uniform swing: this follows from the identity, and the text measured 1000 permille at swings of 72..1614 rounds.
- Two clocks at one site keep every ratio exactly.
- On a uniform clock: one cone, and light's beat scales as W_eff (the text's 1000 and 2250..30257 permille).
- Every push is kept and the kick of 1 is alive (the text's fb5 A-C).
- The run back is exact in every case I ran, the lever's included.

DERIVED / MEASURED / OVERCLAIMED
- DERIVED and standing:
  - the proper-time identity for one Node-clock or a uniform clock;
  - L v kept by a free clock;
  - the lever's arithmetic;
  - the physics side of Theorem 2.
- MEASURED and standing: the text's numbers byte for byte, and its one-site physics table.
- OVERCLAIMED:
  - "nature's" for the board where clocks differ, the books "nature's where the clocks differ", and "none found" (items 1 and 2);
  - "CHOSEN nowhere" and the 00 row's law "retires" (item 3);
  - "no secular rate" (item 4);
  - "nothing is pumped at any swing", which holds for uniform swings only;
  - "two clocks at one site ... 2012 .. 2016" as a measurement (item 7);
  - "Postulate 6 at first post-Newtonian order either way": L linear gives ln N = -c/L_0 + (1/2)(c/L_0)^2 and W linear gives -c/L_0 + (c/L_0)^2, so they differ at 1PN.

QUESTIONS FOR THE BOSS
1. Does the Mesh-tooth text make a Mesh's impulse reach both of its ends at one event? It must be measured on P5c A's lay (uniform clock, staggered teeth) and on P5 B's sweep, for >= 10^4 rounds rather than 40.
2. The lapse's own law (k = 0, 1/4, 1/2, 1) is the owner's to choose. Is the escapement's one-signed deepening of a non-uniform clock to be read as physics or as a defect?
3. Postulate 6's product of slowdowns at 1PN: with the 00 row on a Laplacian, c superposes, so neither L linear nor W linear keeps the product. Which does the law intend, and with which term 5?
4. Is the rest the fastest clock of every world (voids, 00 waves)? If not, the lever costs a staircase m deep everywhere.

SOLUTION24: step 7 ("both ways, by windows") must include a long run, with energy by windows over >= 10^4 rounds, on a non-uniform clock and on a uniform clock with dephased escapements. Forty rounds, plus one 400-round case read as "nature's force", is how a runaway passed.
