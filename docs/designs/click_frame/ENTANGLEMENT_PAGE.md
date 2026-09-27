# Entanglement in the law, on one page: how a pair is built, how it is read, and what our records say

The canonical statement of this algebra is [docs/ALGEBRA.md](../../ALGEBRA.md), section 3.6; this file is kept as the record of 2026-09-22.

For a reader who knows physics and not this repository. Sources: the
registered Bell worlds (bell (`examples/events/bell/README.md`, deleted 2026-09-26),
amplitude (`examples/events/amplitude/README.md`, deleted 2026-09-26), `bell_0_8.json`
and its siblings with their `expectations.json`), [NATURE.md](../../NATURE.md)
row 1a, the paper's figure of S(N), and section 10 of the click frame's
[derivation](DERIVATION.md) (B1 to B4, the theorem, the table, the locality
sentence). Every number carries its kind: DETECTOR (a click), GAMEBOARD (a
diagnostic) or COMPUTATION (the algebra's). Bell's, CHSH's and Tsirelson's
forms are the things compared with, not inputs.

**1. The pair as it is built (B1).** A lamp releases one record with two
arms, one row per arm, carrying two joint labels, 00 and 11, each of
weight 1. In the lattice's algebra the record is psi = (00) + (11) in
Z^2 (x) Z^2 (the arms' label spaces), tensored with its phase in Z[Z_N],
N the phase grain (64 in the registered world). The pair is entangled by
construction: the coefficient matrix of psi is the identity, of rank 2,
and no integer vectors u, v give u (x) v = psi. In flight each arm's row
moves one Link per interval on its own line, its phase turned per Link; the
weights are carried unchanged, nothing of one arm is written on the other,
and no Node keeps anything beyond the events there.

**2. The settings (B2).** A detector's setting is an integer s, the
`phase_window` of its world file. At the detector the arm's label pair is
rotated by the integer matrix U_s = [[C'[s], S'[s]], [-S'[s], C'[s]]],
C' and S' the half-angle tables at 1/256 (the cosine and sine of theta_s =
pi s / N, rounded), with U_s^T U_s = n_s I exactly. Alice's arm reads
U_a, Bob's U_b, each at its own Node.

**3. The click of a pair (P6).** A record is read once. For a pair the
click is one gather of the one record from both settings at the
completion interval: the joint pointer J(o_A, o_B) = sum over the labels
l of U_a[o_A][l] U_b[o_B][l], the cell's weight R = J^2, and the birth
wheel's integer u selects one of the four cells through the rung, the
cumulative weights laid on a ladder of N steps. The rows are local (each at
its own Node with its six neighbours) and the read-out is not: the
non-locality sits in one object, a record of rank 2, read by one gather at
two clicks. No signal passes between the arms; there is one record with
two ends.

**4. What the algebra shows and what the run measures.** Shown, as
identities of the rotation's algebra (COMPUTATION): E(a, b) = cos(2 pi
(a - b) / N) before the tables' rounding and within 2/N + 0.0111 after it;
the marginals exactly 1/2 (Alice's for every setting pair, the rows of
U_b orthogonal on the integers; Bob's off a tie of the rung), so
no-signalling of the counts is an identity of the integers; and S = 2 sqrt 2 at the CHSH settings (0, N/4, N/8,
3N/8), four cosines of pi/4. Tsirelson's bound |S| <= 2 sqrt 2 is a
theorem of the operator algebra on the labels (Landau's identity for the
CHSH operator's square) and bounds the pre-rounding correlations, not the
lattice's rational: S(N) is the exact rational the rung gives, two-sided
about 2 sqrt 2, with S(16) = S(32) = 3 above the bound (COMPUTATION,
GAMEBOARD by kind: no run at 16 or 32), the plateau 181/64 = 2.828125 from
N = 512 to 8192, below 2 sqrt 2 by 3.02 x 10^-4, and 5793/2048 above it at
16384. Measured after a detector (DETECTOR): S = 176/64 = 2.75 at N = 64
(NATURE row 1a; the correlations 44, -44, 44, 44 in the unit 64; each
party's marginal 32/64 in every bin), and the closed form's values at the
six larger grains, seven in all (the paper's figure of S(N)). Against
nature: 2.75 lies 0.33 above Hensen et al. 2015's 2.42 +- 0.20 (1.65 of
its standard error), PASS (NATURE row 1a); beside it, the paper's own
check (its NUMBERS.md rows 53 and 152, `checks/s_of_n.txt`): the plateau
181/64 lies inside Poh et al. 2015's 2.82759 +- 0.00051 at 1.05 standard
errors. The law's numbers
match nature's within these errors; they are the law's, not nature's.

| What | Verdict | The line that decides | The register (kind) |
| --- | --- | --- | --- |
| E(a, b) = cos(2 pi (a - b) / N) within the two grains | SHOWN | J = U_a U_b^T, R = J^2, cos^2 - sin^2 | E x 1024 = 724, -724, 724, 724 at N = 1024 (DETECTOR) |
| the marginals exactly 1/2 (Alice's every pair; Bob's off a tie) | SHOWN, exact | the rows of U_b orthogonal | 32/64 in every bin at N = 64; N/2 on every plateau world (DETECTOR) |
| S = 2 sqrt 2 at the CHSH settings | SHOWN as an identity of the cosine | four cosines of pi/4 | 176/64 = 2.75 at N = 64; 181/64 at 512 to 8192 (DETECTOR) |
| Tsirelson's bound | SHOWN as mathematics; not a bound on S(N) | Landau's identity | S(16) = S(32) = 3 (COMPUTATION; no run) |
| the rise S(N) to the plateau | SHOWN at every N; MEASURED at seven | S(N) = 8 (c_1 + c_1') / N - 4 | 64, 512, 1024, 2048, 4096, 8192, 16384 (DETECTOR) |
| the loophole-free geometry | NEITHER | one gather at completion; the arms' order a declaration | `bell_16_24_far`: the same counts with Bob 116 Links farther, not a spacetime test |
| the order of the outcomes (the order-channel register, not section 10) | MEASURED, FAIL | the wheel a counter | 15/16 and -1/16 at lag 1, Bob's correlation over 192 births (COMPUTATION from DETECTOR clicks, row 1c) against nature's 0 |

**5. What neither shows, and what no experiment of ours tests.** The
loophole-free geometry: in nature the settings are chosen space-like
separated from each other and from the emission; here the click of a pair
is one gather at completion, the near party's outcome is written at the
far party's tick, and the arms' order is a declaration of the world file.
`bell_16_24_far` moves Bob's counters 116 Links farther and reads the same
counts: not a spacetime test. The window-form worlds of
`examples/events/bell` (each click a function of the arriving phase and
the local setting alone) read S = 2 exactly, the local bound (DETECTOR,
row 1b): the control that shows what a local read-out gives. The
choosers' world reads the correlation's bins with fifteen setting pairs
balanced over every u (DETECTOR); the order-channel run (its own register, `docs/designs/order_channel`)
reads the second party's outcome order, which carries the first party's
setting (15/16 and -1/16 at lag 1 over 192 births, COMPUTATION from
DETECTOR clicks, row 1c, FAIL): the counts are blind to the other
setting, the order is not.
Unequal weights and more than two labels are open.

**6. In one breath, the owner's question.** Does entanglement need a
small two-detector experiment to be explained? No: a run cannot prove
what the record assumes. The pair is entangled by construction, one
record of rank 2 with two arms; the run shows that the six verbs'
integers carry that record to two detectors' clicks under the one gather,
interval by interval on a lattice of 21 Nodes, and that the clicks' counts
are the closed form's at every grain built (seven, DETECTOR). The
correlation, the marginals of 1/2 and the value 2 sqrt 2 are the
algebra's, identities of the rotation on the record's two labels; the
bound is Tsirelson's theorem on the labels' operators; the lattice adds
its grain, the rung's rounding, two-sided about the bound. What a run
adds is that the engine reaches the algebra; what it cannot add is the
entanglement itself, the record's rank, put in at the lamp.
