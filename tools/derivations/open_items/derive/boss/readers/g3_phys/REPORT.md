# Report to the Boss: term 6 at G3, the coupling family, whole-speed part (G3.md, scratchpad/g3_blind)

Hostile physicist, new to the project. Probes and outputs in scratchpad/g3_phys (g3p.py the bench; q1..q11 .py/.out;
00_read_log.md, 01_analysis_before_probes.md, 02_findings_measured.md). All on the real act (engine/step.tick) through
the real loader; whole numbers; the one division Rule3's carry; runaways read from outside at 10^9.

## VERDICT on the coupling family (whole-speed part): NOT PASSED

Probe files: g3p.py (bench), q1_stress, q2_quantum, q3_generic, q4_frame, q4b_defects, q5_leak (a-e), q6_flat (part i),
q6b_board, q7_eisenstein, q8_00slot, q9_zone, q10_room_gamma (a, b), q11_board_life, q12_sparse, each .py with its .out.

## Items

1. BLOCKING. The vacuum does not survive on a board with Meshes. G3.md section 3 ("bounded over 300 rounds"), section 8
   ("stands as written"). Measured (q6b, q11 b, 3x3x3 to 6x6x6, Gamma 1000, g 1, the text's own p4/p4b worlds and lay:
   a T1 hand at rest within ONE COUNT at every site): p4's world |k|^2 = 1 everywhere to round 200, max 637 at round 400,
   runaway (a count past 10^9) at round 413; p4b's world (A1, A2) |k|^2 = 1 everywhere to round 300 as the text says,
   max 449 at round 500, runaway at 510; the same lay on 3^3, 4^3, 5^3, 6^3: runaways at rounds 436, 263, 282, 196
   (1.4 to 3 beats of the tied hand). Mechanism (q9, q11 a): the held hand's own spring 2W plus the six Meshes' pull
   (grip W/6, 2W on a checkerboard) is 4W at the zone corner, the step's window's top: a +-1 checkerboard on k = (10,0)
   or on k = (1,0) grows as t + 1 with NO matter (|k|^2 from 1 to 66,050 in 256 rounds); the (pi,0,0) and (pi,pi,0)
   patterns stay bounded to the bit; with a tied hand at A = 10 at every site the checkerboard runs away by round 16.
   The text's lay (three rows at one count) carries about two matter quanta per Node-clock in the Meshes (grip W/6,
   E_q = W/2); one row at one count at every site (0.7-0.8 quantum per Node-clock) dies at rounds 612 (3^3) and 418
   (4^3) after the waves build to |x| 13-19; a lay at one site in five (about 0.1 quantum per Node-clock) and one
   count at one site hold 3000 rounds with |x| never above 1 (q12). The board bears about a tenth of a quantum per
   Node-clock, not "about one". Fix: the stability must be checked at every wavevector with the
   Meshes, not the uniform mode; a held hand whose own spring is 2W has no margin; either a smaller own spring with a
   norm the tables hold (K = W holds a^2 - ab + b^2, q7; the tie would then be through that row) or a different
   coupling; and every board claim run past ten beats.

2. BLOCKING. There is no vacuum: |k|^2 = 1 is an excited state, not a minimum. Section 1 ("held not by standing but by
   turning"), section 2.1, Open 3. Measured (q1, q6 i): the act's conserved form 2E = W (a-b)^2 + K a b gives E = W|k|^2
   per Node-clock (2E/W = 2, 8, 18, 50 at |k|^2 = 1, 4, 9, 25) and E = 0 at k = 0, a fixed point where tied matter has
   no beat (x stands 2000 rounds); the turn is exact at (1,0) ... (1000,0), (3,4), (5,12), (20,21): no law picks |k|^2.
   The radial direction is flat (no restoring force), the phase turns at omega = pi/2: the reverse of nature's Higgs
   (massive radial mode, phase eaten). Decision 40 (g) "from the law" is not met; the seed sets the vev. Fix: name it
   OPEN; "Higgs-like" is overclaimed; a minimum needs a potential the law does not have.

3. BLOCKING. The vacuum has a rest frame and w >= 0. G5's physicist's objection confirmed and quantified (q1 a): per
   round and on average, 2E/W = 2.000, 2p/W = +2.000 (symmetric leapfrog reading, w = +1) or 0.000 (now-slot reading,
   w = 0); never w = -1. It is stiff or dust-like matter at rest in the lattice frame, with E = W per Node-clock, one to
   two matter quanta (a quantum at D_x = 1 reads 2E_x/W in 0.97..1.92), in every Node-clock. Under decision 40 (a)
   (gravity gravitates by every train's rho + 3p) it sources the lapse everywhere. The text's section 4 ("gravity's
   slots are untied") does not answer this. Fix: none for a turning hand; say so.

4. BLOCKING. Not generic: which hands tie is laid by hand, and the only generic plan ties light and the metric.
   Sections 2.2, 2.6, Open 1. Measured (q3 a): every train tied through its K x K -> A1 rows at g = 1: the T1 hand,
   light, the metric's 00 slot and ii slot all beat at 266 rounds (A = 4); the 00 slot's spring is 2f/W = 2/Gamma,
   the time gear's spring of the owner's law (a unification the text could claim, but light comes with it). The pair
   rule (K with A2 x K) read from the tables (A2 x {A1,A2,E,T1,T2} -> {A2,A1,E,T2,T1}) ties NOTHING in the probes'
   universe ([A1]x2, [T1], [A1]x2) nor in the example universe, and ties the held hand (A1, A2) to itself (|k|^4,
   omitted in the text; absorbed, q3 a). The probes' tied train is one T1 kind: not a pair. Probes 1-6 use (A1)x2,
   light's kinds exactly. Fix: either derive light's exemption from a structure the act realizes (the norm tells no
   kind, so not from this tie), or write "declared by the plan's list".

5. BLOCKING. One mass for everything tied. Sections 2.4, 4. Measured (q3 c, p6 ii-iii): T1, T2, light, both hands of a
   (T1, T2) pair: 266 rounds at A = 4, g = 1. A spectrum needs g per train, a declared number (decision 35), or a vev
   of many quanta, which puts every mass at the window's top (masses go as |k|^2, the window 2 g |k|^2/Gamma < 4).
   Nature's Yukawas span 10^6 with one vev. Fix: name "one beat per tied train" as what it is: not nature's coupling.

6. BLOCKING. The quantum and the room do not overlap; the mass formula is never the measured beat. Sections 2.4, 2.5,
   4. Measured (q2): Gamma 1000: exact to A = 15 (g A^2 = 225, 0.45 quantum at peak), off from round 1 at A = 16
   (0.51) through 25 (1.25) with |k|^2 in {0,1,2}, runaways from A = 28 (1.57 quanta); Gamma 4000: exact to A = 31
   (0.48), off at 32 (0.51), runaways from 56. The room at peak is half a quantum at every Gamma ("about one matter
   quantum" used the mean x.x). D_x = 1 is where the hand moves one count a round at its peak, so below the room the
   hand relaxes (P = Gamma/A + 4A; 126-130 rounds) and at one quantum the beat is 122-124 rounds against the claimed
   140.5 (13 per cent; Gamma 4000: 241-246 against 281) with the vev bent. The room is also not Gamma/4 (q10 a, q5 d):
   Gamma 3200 bends at A = 16 (Gamma/12, round 3251), 20 (Gamma/8, 1281), 28 (85), yet not at 18, 23, 25 within
   25,600 rounds; Gamma 12800 at 40 (4961) and 56 (170): a resonance structure, not a threshold. Fix: state the room
   per Gamma as measured over many lays; state the mass at one quantum as a 13 per cent-off mixture over |k|^2.

7. MINOR. "A chirality of the seed" (section 2.2). The A2 character is -1 on 12 PROPER rotations (p0: the 24 are the
   det +1 signed permutations; A2 is the sign of the axes' permutation). A sense flipped by a 90-degree turn is a cubic
   anisotropy (l = 3 in the continuum), not a chirality; the vacuum breaks O to T. Invisible to the norm tie, visible
   to the named half-speed tie through k_im. Fix: rename, and name the anisotropy for the half-speed part.

8. MINOR. Defects never heal (q4, q4b, 3000 rounds): a site at (0,1), (2,0) or (1,1) amid (1,0) cycles |k|^2 through
   1,5,5 / 4,1,2 / 2,1,4 forever (its neighbours stay 1): a permanent 4-5x mass anomaly; a domain wall and a winding
   vacuum k(x) = i^x are exactly steady (64 of 64 sites, 400 rounds): the phase pattern is frozen as seeded. Fix: name
   it; the act has no dissipation.

9. MINOR. The theorem of the turn (section 2.1) presumes the Gaussian square. q7: K = W holds a^2 - ab + b^2 (period
   6), K = 3W holds a^2 + ab + b^2 (period 3), each to the bit; the text measured re^2 + im^2 for them. "Only W" is
   "only the Gaussian norm": the factor 2 is the ring, CHOSEN. "The fastest steady beat" (nu = 1/4) is false: period 3.

10. MINOR. The 00 slot's tolerance (section 3, "exact for |00 slot| below rest/2"). q8: exact for -rest/4 <= c <
    rest/2 at the probes' lay (tooth at rest/2); -rest/5 <= c < rest/3 at the deeper clock's mid tooth. (The matter's
    room did not shrink with c up to 0.3 rest; a deeper clock has more room.)

11. MINOR. The click layer is a prediction about an unbuilt part (G5 OPEN): "the held hand never clicks", "a mass per
    quantum", "E = n h nu" are not measurable on main. Fix: mark n/a, not results.

12. MINOR. Probe hygiene: p4b_a1a2.py uses np.linalg.det (float) and round(); lab.py uses //, %, divmod, not the carry.

## What is SOUND
- The quarter turn at K = 2W: |k|^2 and D held to the bit (p1; my q1, q6 i, q7), at den up to 1.5 x 10^16.
- Inside the room at Gamma 1000 (g A^2 <= 196): no leak and no drain over 80,000 rounds; the fine tooth's walk is a
  fixed path ([-200,0], [-336,0], [-448,0] thousandths of W at A = 10, 12, 14) and max|x| constant (q5 a-c).
- The relaxation period P = Gamma/(gA) + 4A to a round for A <= 15 (p2; q2: 130, 126, 126 at A = 12, 14, 15).
- The step's window [0, 4] (p3); the run back exact wherever bounded (every probe).
- The 24 commute with the plan's J, A2 row signed (p4, p4b).
- Past the room at one Node-clock a stationary mixture: |k|^2 at 0/1/2 for 22/37/41 per cent of rounds, the matter's
  envelope constant over 6000 rounds (q10 b).
- The generic plan reproduces the time gear's spring D/W = 2/Gamma on the 00 slot (q3 a): one monomial form for the
  own spring, the tie and the time gear's spring (the text's step 10), at the price of item 4.

## Solution24, one line
Add to step 6/8: a held train's stability is checked at every wavevector with the Meshes (the zone corner), and every
board claim is run past ten beats with a runaway read from outside.
