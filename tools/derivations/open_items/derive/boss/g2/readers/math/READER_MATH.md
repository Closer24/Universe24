# The hostile mathematician on G2's two texts: N2's second text (term 5) and term 13 blind

The report as the reader gave it, 2026-10-30, filed by the Boss. Checks in whole numbers, on the engine's act via
n2b_lib unchanged, beside this file: probe_theorem.py, probe_term13.py, probe_phys.py, probe_small.py, their .txt
outputs, findings.txt; repro/ holds the three probes rerun, and all three result files reproduce bit for bit.

VERDICT on term 5: NOT PASSED
VERDICT on term 13: NOT PASSED

## TERM 5 (N2's second text), most serious first

1. BLOCKING. Section 4, hypothesis (b) and proof step (2). The parity rule is not sufficient: R_P maps (sigma_b,
   sigma_a) to (-sigma_a, -sigma_b), so a lone stride monomial maps to its partner, not to +-itself; the theorem needs
   pass 2's plan invariant under the swap of the two stride planes, which the statement never asks and the probes
   never break (rate_part always lays both). Measured: sigma_b(A1)^2 alone onto 00, sigma_a(A1)^2 alone, sigma_b(T1x)
   sigma_a(T1y) alone, and sigma_b(A1) D_x(A1) alone onto 0x all pass rule (b) and all depart at round back 1; their
   swap-symmetric pairs hold 60 rounds. Fix: add hypothesis (e), the pass-2 plan symmetric under the stride swap;
   measure sigma_b^2 alone as its broken case; repair step (2).
2. MINOR. Hypothesis (c) says the reads "land" on even rows. M5's own lay lands the 00 read on the odd 0i rows and
   holds (exact); the odd 0y row read into the even A1 row departs at 1. Fix: "reading even rows only".
3. MINOR. Proof step (3): on an even row the drive with J kept and tooth flipped gives the same quotient with remainder
   T_d - 1 - r_d (9718 of 9718 cases); the negated quotient is the odd row's (J negated, tooth kept). The gear's
   flipped dividend does the negating.
4. MINOR. Conservation. "Each row's momentum kept exactly on the torus under a moving W" (section 2, the condition
   paragraph, Solution24 item 6) is the identity p+ = p + F with sum F = 0 and J = 0, no W in it; under term 5 the 00
   row's sum of p grows 0 -> 241,517 (TERM13 probe 2) and the spring breaks the matter's. The owner's word puts
   conservation in the clicks; both texts say "Clicks: n/a". Fix: name the identity, restrict it, and owe the clicks'
   check at G5.
5. MINOR. gamma. Term 5 as written pushes the ii slots up under every source laid (held count J_ii = +25, the lump's xx
   slot -> +250, the swing 0); gamma = 1 needs the ii strength negative against the 00's. "The sign lowers the grips
   where matter is" is not the plan's sign; -1/12 is honestly CHOSEN but carries a sign flip (the ii slot stands for
   the inverse spatial metric). Fix: say so.
6. MINOR. P4: "23.1 against 24, the lattice's dispersion" stated without a number. Measured at half widths 8, 16, 32,
   64: Szz/S00 = 23.13, 23.77, 23.94, 23.98; -S0z/S00 = 4.79, 4.87, 4.89, 4.90. The attribution is right; add the
   widths.
7. MINOR. M3's third case "a held gradient" is not held (the pull moves 36 of 60 sites) and J_xx = J_yy = 1080 are the
   potential's; the gradient alone gives J00 = J_xx = J_yy = 0 (+72 from the pass-1 motion), J_zz = 7776, as the
   continuum. "rho = pr = 98/4" is the identity 4 rho = J00 + sum J_ii applied, not a measure.
8. MINOR. P5 "the clock-rate wave runs at light's speed" is measured at rest only, where both rows obey one equation.
   In a well the 00 wave keeps 302 rounds (teeth at rest) while light takes 428 and 607 at W = 2, 4 rest: speed^2
   ratio 2008, 4039 permille. A superluminal 00 wave in a well: name it.

## TERM 13

1. BLOCKING. "4K - 2V averages to the swing's energy ... the act carries it into W." By 500-round windows of probe 2,
   push / 2E = 1006, 942, 1095, 1477, 1480, 1076 permille; from round 1000 on 69-85% of the 00 push comes from rounds
   with -W < p < 0, where p div W = -1 and the stride's square contributes 2W; 2E plateaus (59k, 52k, 53k, 47k, 53k
   against the adiabatic 100k -> 43k) and p00's gain per 500 rounds does not slow (28k, 28k, 40k, 35k, 29k). W does
   grow without bound, but after round 500 by Rule3's floor on a slow hand, not by the energy. Fix: state the claim
   for the stride-many-notches regime (rounds 0-500, 1006 permille) and name the floor's pump with its share, or
   source the 00 slot by p^2 / W rather than W (p div W)^2.
2. BLOCKING. "The well of a lump settles to a bounded depth" (Poisson). Sampled every 25 rounds, the well swings with
   width 43, 93, 160 over successive 500-round windows, growing, never settling; "bounded" is asserted, not shown, and
   the OPEN clause's answer ("nowhere at a Node-clock") rests on it. Fix: claim what is measured (the well's swing is
   1/600 of the mean at round 1500) and leave "bounded" OPEN or derive it.
3. MINOR. "N^2 = rest / W exactly." The measured 4008, 8027, 16068 permille are the discrete law's own second order,
   (12W - g)/(12 rest - g) = 4017, 8041, 16088, within one round's resolution (9, 12, 17). Exact to first order in
   g / W only.
4. MINOR. "Both edges are reached by the act alone." Light's edge is laid by hand (probe 4); the act's only run with the
   ii slots moving (probe 3) raises them, away from the edge.
5. MINOR. "Two clocks on one board keep their ratio": by the text's own numbers W_far / W_lump goes 995 -> 1000
   permille from round 500 to 1500; the redshift fades with the mean.
6. MINOR. Item 6 "the row sums kept in the p-form": the 00 row's sum is what the whole text shows growing; the books
   are the clicks'.
7. MINOR. Probe 5's held count carries V with the spring's g in the source while no spring acts on the hand: plans
   mixed; legal as a vacuum energy, say so.

## SOUND, with numbers

The theorem's mechanism is right once the swap symmetry is added, and it holds at the edge the text never visited:
W = 1 at 1668-2208 matter site-rounds over 33-40 rounds (rest 3-4, grip 0), exact; (W - 1 - p) div W = -(p div W):
0 misses for W in 1..7 over p in [-50, 50], 67-101 misses for W < 0; M1's broken cases and M2's narrowing (the ii and
jk strides as sources, 300 rounds exact) stand; the 3000-round run back under W 3000 -> 143066; the 24's condition
measured in both forms (24, 3, 3, ...) and the mend honestly deferred, with the p-form's removal of the falling-clock
cost correctly observed; P3's virial 1.000809 and 1.000838 and the g / 2W shortfall agree with the exact discrete
invariant (a+ - a)^2 + k a a+; the rho and pr identities; J = 2T - eta T matches S + 2 eta V for a scalar field;
light's edge arithmetic (grip = rest/6 - c00/6 = 0 at c00 = rest) on the chosen ratio.

## For Solution24

Add to step 6 that a theorem's hypotheses are measured by cases built to pass the stated rule and still break (not
only cases that break the rule), and to step 7 that a claimed mean is read by windows over the run and a "bounded" or
"settles" names its width over time, never from one sum or seven samples.
