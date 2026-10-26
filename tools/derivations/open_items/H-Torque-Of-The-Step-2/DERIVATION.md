# H-Torque-Of-The-Step-2: where in the step's letter the torque is born (2026-10-26, 03:0x to 03:4x UTC; the head 38655ef18)

Project NatureFirst, item A1, the owner's words of 02:45 and 02:49 UTC (generic laws first, the angular momentum first of them if it is missing; derive what is needed, unify). The board hands (The-Angular-Momentum_COMPARISON.md) and the click hands (The-Angular-Momentum-In-The-Clicks_COMPARISON.md) left one term unlocated: the step's torque. This hand locates it in the step's letter, act by act, as an exact identity, and asks whether a local form conserves the moment. A blind hand works the same question; no file of it was read.

## 1. The algebra

**The reading.** MV-S1's density on the Link i -> i + b of a record with the pair (num, den): p_b(i) = 2 num SUM over the record's lines l of (a_l(i + b) a'_l(i) - a_l(i) a'_l(i + b)), a the level now, a' the level before. L_c = SUM_i [X_a(i) p_b(i) - X_b(i) p_a(i)] with (c, a, b) cyclic and X the doubled arm 2 r - (cube - 1) about the cube's centre (the board hands' L2). In one line: L_c = 2 num a'^T B_c a with B_c = G_c - G_c^T, G_c = X_a Sh_b - X_b Sh_a (Sh_b the shift by one Link along b): the moment is an antisymmetric bilinear form of the two levels.

**The step as built** (interval.kick, interval.division; node.py, rule3.py). A riding line's level after the division is a_next = a + v with v = (P + half(ws)) div ws, P = W (a - a') + r - half(W) + X F: W the mean wall at the kick (the row's scale times (w div 2)(X_before + X_now) of the carrier as the rows hold it), ws the mean wall at the division (the same after the carrier's act), X = X_now the carrier's time level, r the line's remainder at the start, F the force the engine reads: F(i) = SUM_j R_ij U_ij a(i + j) - (D_i + SUM_j R_ij) a(i) + C(i), the arrivals turned by the Links (U_ij the Link's turn, the identity at the coupling 0), the Node's own weight, and the curl's term C of the planes with a coupling (gram.term). Writing delta = a_next - 2 a + a' (an integer at every Node and line), the division's own identity is exact:

    ws(i) delta(i) = X(i) F(i) + (W(i) - ws(i)) (a(i) - a'(i)) + rho(i),   rho = r - half(W) + half(ws) - r_end,

rho the dropped remainder, |rho| < (W + ws) div 2 + 1 (less than one wall). Since the new before is the old now, the density's change on the Link i -> i + b is

    dp_b(i) = 2 num SUM_l [delta_l(i + b) a_l(i) - delta_l(i) a_l(i + b)]:

the change of a Link's current is the second difference at one end times the level at the other, antisymmetrised. Each part of delta gives one term of the moment's change, exactly, as a quotient of integers (the denominators the two ends' walls): with e_ij = R_ij X(i) / ws(i) the Link's effective reach as read from the end i,

| term | the part of ws delta | the act it names |
|---|---|---|
| LINKS_SYM | SUM_j (e_ij + e_ji) / 2 a(i + j) | the arrivals at the Link's reach read alike from both ends |
| LINKS_ASYM | SUM_j (e_ij - e_ji) / 2 a(i + j) | the one-end read: the clock is the Node's, R_ij = 2 num p_i^2 Q_ij, and X / ws is the Node's own |
| TURN | the turned arrivals less the plain | the Links' turn of the arrivals (the records' coupling to the potential) |
| OWN | -(D_i + SUM_j R_ij) a(i) X / ws | the Node's own weight, its gradient across the Link |
| CURL | C(i) X / ws | the curl's term of the coupled planes |
| RIDE | (W - ws)(a - a') | the carrier's mean wall moving between the kick and the division |
| ROUND | rho | the dropped remainders of the step's divisions |
| REST | what the identity leaves | 0 by the letter but at a frozen Node, whose lines are restored (BH-S1) |

and across one interval, L2(S4) - L2(S0) = [the eight terms of the table, summed] (the step, S0 -> S1) + the write's change (the lays, S1 -> S2) + the swap's change (S2 -> S3) + the clicks' change (S3 -> S4, the clicks' moment of AJ-S1, exact).

**Which vanish by the letter.** Write dL_c(step) = (2 num) a^T B_c M_eff a with M_eff the matrix of the effective step (the diagonal -(D + SUM R) X / ws, the off-diagonal e_ij U_ij, plus the ride and the rounding as vectors). For a symmetric M the quadratic form is a^T [B_c, M] a / 2, the commutator of the arm's rotation with the step's operator; for the antisymmetric part it is the anticommutator, a^T {B_c, M_a} a / 2, which no symmetry kills.

- *Uniform paces, no turn, the carrier at rest*: M is the plain Laplacian with uniform coefficients. The Links along the axis of the arm's own shift telescope on the torus (the arm is constant along the shifted axis); the two transverse plaquette terms a_i a_(i+a+b) - a_(i+b) a_(i+a), one from each of X_a Sh_b and X_b Sh_a, carry the arm's difference across one Link (2 in the doubled arm) and cancel each other exactly; the third axis telescopes. So the bulk of [B_c, M] is 0 identically, and what remains is the seam of the torus's cut where the arm jumps by 2 (cube - 1): a term of the reading (the cut arm), not of the step (am1's finding, 6 of 6). On every uniform board every term is 0 to the bit (the current 0 on every Link).
- *A Link's current along its own axis*: a change of p_b(i) is a change along e_b; its moment about any centre is X_a(i) e_c - X_b(i) ... (the arm across the Link times the change), 0 about the Link's own line alone. So a term of the step is torque-free only where its change of the current on the Link i -> i + b is balanced by the opposite change on a Link the arm reads alike: the telescoping and the plaquette cancellation above are the only two such balances in the six-Link stencil, and both need the coefficient the same at both ends of every Link of the plaquette. Every act that moves momentum ACROSS axes with a coefficient that differs between two Nodes is where the torque is born: the gradient of the own weight across a Link (OWN), the reach read at one end alone (LINKS_ASYM), the symmetric reach varying across a plaquette (LINKS_SYM's bulk), the carrier's wall moving unequally at two Nodes (RIDE), the dropped remainders, which differ at every Node (ROUND), and the Links' turn (TURN) where the records couple.
- *The swap*: at a Node both of whose ends are turned the density reverses, p -> -p (the exchange of now and before under the conjugation K with K^2 = 1 negates the antisymmetric form); at a Link with one end turned the density goes to 2 num (a(i + b) a(i) - a'(i) a'(i + b)), no sign rule. Time's reversal at a Node reverses the Node's share of the moment by its letter: the swap's term is the act's own and no form of it that keeps the act conserves the moment.
- *The clicks*: AJ-S1, exact (the click hands): a one-Node take's moment equals the board's change.
- *The write* (the lays: the emitter's W-S1 lay and the shape-4 row's current): one Node's level moved by the lay's quotient: a change of the two Links of each axis at that Node, exactly as a take, with the moment (r - c) x dP_lay.

**The bound of the rounding in units of the wall.** |rho(i)| < (W(i) + ws(i)) div 2 + 1 at every Node and line, so the rounding's part of delta is below one unit of the level, and its term on the moment is below 2 num SUM over the Links (|X_a(i)| + |X_b(i)|)(|a(i)| + |a(i + b)|) summed over the lines: a walk of remainders at the scale of the levels times the arm, two decades below the paces' terms on the hole (the measurement below).

## 2. The measurement (tq2_torque.py, integers and exact quotients of integers; about the doubled cube centre)

The identity closes on every interval of every record: REST 0 on 60 of 60 (the hole), 60 of 60 (the chiral), 300 of 300 (the bodies), 450 of 450 (ga2), and the terms' sum is the measured step change to the integer (the fractions sum to an integer at every interval). The reader reproduces the board hands' L2 at the end of the hole 60 to the bit, [-429523890798423826416, 23815323951483308120, -23815323951483308120].

The bodies 300 and ga2 450: every term 0 on every interval, every phase 0 (the seeds' symmetry; ga2's 64 births at the interval 2, P_z 88727700428746492867072 unreturned along z as the click hands read it).

The hole 60 (16 births, 546 turns, 777 clicks), the y component (L_y = -L_z at every interval, the transposition's pseudovector; L_x's terms in the json), the integer parts of the exact sums over the 60 intervals:

| phase or term | sum over 60 intervals (y) | sum of absolute values (y) | largest one interval |
|---|---|---|---|
| the step | 17862396336423982013668 | | |
| the write | 0 | 0 | 0 |
| the swap | -16987156279734819838420 | | |
| the clicks | -851424732737678867128 | | |
| LINKS_SYM | -126736312115809148499613 | 316034143880501981873833 | 42747987098296660151183 at 13 |
| LINKS_ASYM | 40408275544082829985292 | 179941151440212770646934 | 22267116369422912804028 at 15 |
| TURN | -113778885473600787962 | 3265774769976124408622 | 1367299190868882844559 at 23 |
| OWN | 92417427985897605899659 | 369617238394045771685519 | 59145405890532276039206 at 15 |
| CURL | 0 | 0 | 0 |
| RIDE | 12199830344779630967038 | 52622804166699929152141 | 9107909222930351049710 at 9 |
| ROUND | -313046537053335550745 | 2037741720251186493126 | 145552520371371836155 at 7 |

The well's symmetric torque LINKS_SYM + OWN sums to -34318884129911542599954, the one-end read's to 40408275544082829985292, the ride's to 12199830344779630967038, the rounding's to -313046537053335550745, the turn's to -113778885473600787962: the step's 17862396336423982013668 (the integer parts' sum differs from it by 1, the parts' rounding). The torque is born in three acts of comparable size, the well's gradient read across a Link (OWN against LINKS_SYM, each 10^23 and cancelling to 10^22), the one-end pace (LINKS_ASYM, 10^22, present on 60 of 60 intervals), the carrier's moving wall (RIDE, 10^22), and the rounding's walk two decades below (10^20, the bound above). The swap is the largest single mover and undoes most of the step (-1.70 x 10^22 against +1.79 x 10^22 on y): the turned Node ends at its pre-state exchanged, which takes back the step's torque there and reverses its share.

The chiral 60 (17 births, 639 turns, 2943 clicks): the step [-19852052908394301378788, -19910893117643987426872, 17065526420877150245300], the write [-57922112819809325980, 74358649546687155656, -77027312336290936120] on 6 of 60 intervals (the emitter's lay), the swap [22057883571347686828128, 18848483455569386174132, -16677941328881061442632], the clicks [-2548682205121551609916, 532590783696417292212, 1326953399347397122428]; the terms' sums LINKS_SYM [7327108437973374611529, -92539006054195905031953, -171958702938519739797805], LINKS_ASYM [168641244630186754673855, 21884699200496424937808, -106031369442105058876324], TURN [3149183008570861225680, -6389788638821644487641, -3588930939505753527650], OWN [-151895728277973707269418, 71513265550281334145953, 232389827675524434723790], RIDE [-47069739336858916410217, -14671808645977458590900, 66390189967111395150036], ROUND [-4121370292668210218, 291745470573261599861, -135487901628127426745], CURL 0, REST 0 on 60 of 60. The same three acts, the one-end read the largest on x.

## 3. A local form within the law

The one term a local form removes is LINKS_ASYM: the reach read alike from both ends, R_ij = 2 num p_i p_j Q_ij (the neighbour's pace read through the Link, one Link; an integer within the same bits; the same for every row; its own inverse by the same reaches from the same start level, so the run back holds; the 48 kept since the two ends enter alike), built flagged as the measured form TQ2_FORM=1 on a copy of src (make_copy_tq2.py; off, the head bit for bit: the hole 60's state hash the same, the run back 10 of 10). Its measurement is in the report (what it removes and what it leaves). It does not reach conservation, and it is not proposed as the law: it changes the conserved form's weighting (D M symmetric with D = diag(1 / p_i^2) is the law's line; a symmetric M changes which bilinear form is exact) and so crosses **Rule3 is not changed** (the conserved form fixed), and the first-order gradient term it adds to the wave equation is the two-end pace's divergence form the law refused for the periapsis (beta_K).

The terms no local form removes, by name:

1. **The well's torque, OWN + LINKS_SYM**: the commutator of the arm's rotation with the well. The arm 2 r - (cube - 1) is the centre's, read by no Node (a Node has no position in its state: **The Node**); a local act can conserve a moment only where its change of the density is a divergence of a local flux, and the six-Link stencil has exactly two such balances (the telescoping along the arm's shift and the plaquette's cancellation), both needing the coefficient the same at both ends of the plaquette's Links. A well is a coefficient that varies; its torque about the centre is nature's own where the well is off the centre (nature conserves L about the force's centre alone), and the cube's anisotropy where the well is central (the 48 is the lattice's rotation group and has no continuous generator). The term cannot be made local because the quantity it fails to conserve is not local: it is the centre's.
2. **The swap**: time's reversal at a Node reverses the Node's share of the density by the letter (p -> -p where both ends turn); a decided act, the fifth.
3. **The rounding**: the carried division's own remainder, bounded below one wall per Node and line per interval; the carried remainder makes the level exact over time and the bilinear density not, since the level multiplying it varies.
4. **The ride**: the carrier's wall moving between the kick and the division is the clock's own tick; where X_before = X_now at both ends it is 0.

Verdict: A FINDING. The torque of the step is located to its acts with the integers; no local form of the step reaches the conservation of the moment about a centre; the conservation of angular momentum stays missing by name, in the form nature would need (a continuous rotation the six Links do not have).

## 4. The laws with a number

The one-Link reach: every term reads one Node and its six Links (the reach's two ends, the neighbour's pace through the Link); the arm is the reading's, not an act's. Integers: every level, remainder, reach and wall an integer; the terms exact quotients of integers (fractions.Fraction), no float; the largest bit length on the hole 60 run 115 bits (run_hash.py census) under 128. The fixed count: the reader adds no row; the measured form adds no integer to the state. The run back: the head 10 of 10 on the hole 60 and to the start (run_hash.py); the measured form's in the report. Nothing under src/ or tests/ is changed; the copy is flagged and off bit for bit.

## 5. TQ-S1, the sentence for ALGEBRA.md (dated 2026-10-26; a reading's clause and a finding; for the Boss's cold read, no sentence for approval)

**TQ-S1** (2026-10-26, the torque of the step; the hands H-Torque-Of-The-Step-1 and -2): the step changes the moment of the lattice momentum density about a centre by an exact identity Node by Node, ws delta = X F + (W - ws)(a - a') + rho, the change of a Link's current the second difference at one end times the level at the other; the torque is born where the step moves momentum across axes with a coefficient that differs at the two ends of a Link: the well's gradient read across the Link (the own weight against the arrivals), the one-end pace (the clock is the Node's), the carrier's moving wall, and the dropped remainders below one wall per Node and line, with the Links' turn where the records couple; at uniform paces with the carrier at rest the bulk vanishes identically and the seam of the cut arm alone remains; the swap reverses a turned Node's share; the clicks' part is AJ-S1's; no local form of the step conserves the moment about a centre, since the arm is the centre's and no Node reads it, and the lattice's rotation group is the 48 without a continuous generator; what the law conserves is the lattice momentum and the 48 (AM-S1), the moment a reading.

The row for the gates of the phenomena, "the conservation of angular momentum": NOT SHOWN, the law missing by name; the step's torque located to its acts (TQ-S1) and 0 to the bit where the seed has the symmetry (the bodies 300 of 300, ga2 450 of 450, the uniform boards); the reader tq2_torque.py and its test test_tq2_torque.py.

## 6. The ledger row and what remains missing

| item | derived | one-Node test | toy | gates | spec | missing by name |
|---|---|---|---|---|---|---|
| the torque of the step (tq2) | an exact identity of the step's torque by act: the well's gradient, the one-end pace, the ride, the rounding, the turn, the swap, the clicks; no local form reaches conservation, the arm the centre's | test_tq2_torque.py: the identity closes on the hole 3 intervals, the one-end term present, the turn and curl 0 | the hole 60 and the chiral 60 (REST 0 on 120 of 120), the bodies 300 and ga2 450 (every term 0) | the row NOT SHOWN with the torque located | TQ-S1 | the conservation of angular momentum in nature's continuous form; the seam's term as its own reading (the cut moved); the swap's reversal's balance; the turn's term's letter (a gauge-covariant density) |
