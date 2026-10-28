# Draft E: Pauli from the phase reversal, read in the click of two equal quanta

For the Boss's Tensor24 (TENSOR24.md law 7 and section 19's owed list, "Pauli's exclusion: the act that writes the exchange sign, with the law's exact count of quanta kept where the board would hold 0 and the books booked two"; section 16's Pauli row; section 22; section 24 item 1; section 30's objections). Drafted under derive/PROTOCOL.md on 2026-10-28, its steps 1 to 4. Steps 5 (a second hand) and 6 (Sofer's law check, David's sign-off) are not this draft's.

**The owner's words this draft answers** (translated):
- 10:4x UTC: "Pauli is derived from a very important law. It is about the clicks, note. On the board it is the phase reversal. It must be derived from a big law. Think clocks, think tensors, and Rule3."
- To Sofer, 10:4x UTC: "Pauli never as a postulate. It is derived from the phase reversal of a family on the board; in a click this gives Pauli; check it."
- 11:1x UTC, the spine of this draft: (1) add amplitudes, not probabilities: two identical quanta and two detectors give two ways, whose amplitudes are added and then squared; (2) the exchange keeps the size and twice returns the system, so one exchange is 0 or 180 degrees; (3) with both detectors alike, the antisymmetric total is A - A = 0; (4) the exchange equals a 360 degree turn of one quantum, which flips a spin one half's sign. "From here understand what to do on the board so that a click will be Pauli."
- Through David, 07:0x UTC: "Pauli should be derived from matter being something not symmetric, and from the trains that carry force, which are symmetric."

**Read on:** the t24 worktree (S/t24, the head's src: hands.py, meshes.py, clock.py, click.py, phase.py, assembly/setting.py, trains.py, core/acts.py); TENSOR24.md lines 453 to 712 and 1261 to 1342; draft D (S/derive/D/DERIVATION.md); Sofer's SOFER-PAULI-PHASE-REVERSAL-1.md with its probe and checks (scribe-5, tools/derivations/open_items/, read through the GitHub API at the remote's head, with no local git write); David's DAVID-PAULI-DYNAMICS.md (toys-5); scribe-5's docs/ALGEBRA.md at 7c23a98aa. The probes and their outputs are in this folder (part 8). Every claim is marked **PROVED** (with its proof), **CHECKED** (with the probe's count) or **OPEN**.

## 0. The answer in one page

1. **The big law: the phase reversal law of the 24's double cover.** On every kind of the 48 (the eight irreducible kinds of 2O), three signs are one sign:
   - the full turn z on the kind, the phase reversal on the board (+1 on A1, A2, E, T1, T2; -1 on E1/2, E5/2, G3/2);
   - the square of the kind's phase reversal T, the one antiunitary act that commutes with all 48 (Kramers);
   - the exchange symmetry of the kind's one A1 pairing, the clock of two equal quanta (the Frobenius-Schur indicator).

   PROVED (part 7, P1 to P4). CHECKED exactly on the 48, with all eight kinds built from the group (e1: 8 of 8). It is the cube's: on the 12 turns of the tetrahedron it fails on 4 of 7 kinds, and with commuting lifts on 5 of 5 (e1, the mutants).
2. **Pauli from it, in the click** (the owner's four steps as one act). The joint click of two equal quanta reads their two-quantum amplitude, sigma_ab = N(M_a1 M_b2 + eps_T M_b1 M_a2) with M_aj = <phi_a, psi_j>, and eps_T is the big law's sign, read on the board as the train's own half turn applied twice. On the twin hands eps = -1:
   - sigma_aa = 0: two equal twin quanta never click in one state;
   - at one Node-clock they click only as the singlet, of size rho(phi)^2 N(det[psi1, psi2]) in every frame;
   - a third has no state;
   - law 5's q per state is at most 1, because the sum of the signs of the q! orders is 0.

   On the force carriers eps = +1: sigma_aa = 4 N(M_a1 M_a2), so they bunch, and a balanced splitter at a Mesh gives no coincidence (Hong, Ou and Mandel). The books close: over a complete set of parts, SUM sigma = 2 lam^2 (rho1 rho2 + eps N(<psi1, psi2>)) (Cauchy-Binet; Lagrange at two parts). PROVED; CHECKED (e2: 20,000 of 20,000 and more, every mutant failing).
3. **Sofer's occupant frame is the same act**, at the occupied state: free = N(<T phi, chi>), blocked = N(<phi, chi>), room = rho(phi) rho(chi). PROVED; CHECKED (e2: 3,744 of 3,744). One correction: his bound |S| <= rho <= 2u does not keep the sizes positive. The bound that does is S . S <= (2u - rho)^2 (e2: 22,384 occupations inside his bound and outside this one give a negative free size).
4. **What the board must hold, so that a click is Pauli: one hand per quantum.**
   - One twin pair per train and Node-clock (the head's board) cannot hold two quanta: their sum is one pure spinor, and it lets a third in (e4: 29,488 of 29,952).
   - The occupation (rho, S) is a reading of the quanta's hands, not a state: equal occupations step apart (e4: 20 of 20).
   - The one formula keeps the quanta's mutual two-slot form exactly (e4: 24 of 24 ticks).
   - On that board the free partner of an occupant is the occupant's own turnover image, the phase reversal with the slots exchanged. It is exactly orthogonal to the occupant and an equal quantum (e4: 20,000 of 20,000). "On the board it is the phase reversal."
5. **The turnover on the twin hands must be T = i sigma_y K**, which commutes with all 48 lifts (e3: 48 of 48). The head's K commutes with 8, and as built the head applies K: S goes to (Sx, -Sy, Sz) at 375 of 375 Node-clocks (e5, bit for bit on the head). T T = -1 is Kramers' phase reversal, so two turnovers reverse a twin hand's sign: the carry of the ratchet's two teeth (e3).
6. **What stays OPEN** (part 12):
   - The board's own bound (degeneracy pressure). The step keeps the two-slot form, in which one quantum's occupation is not positive (e4, draft D's P2). The one-slot occupation is positive but not kept (e4).
   - Exact statistics for several occupants spread over many Node-clocks, which need their Gram matrix, a sum over the board.
   - Step 4's topological form (Finkelstein and Rubinstein; Balachandran et al.) is no theorem on the engine, which holds no configuration space of quanta. Its algebraic form, the big law, carries the derivation.
   - The Bell pair's singlet across a Mesh is no product of two hands (the side question, part 13).

| objection | verdict |
| --- | --- |
| P1 (half-braid, belt trick, no configuration space) | STANDS against the topological route; REFUTED as a bar, since the algebraic route needs no configuration space |
| P2 (needs Lorentz and microcausality) | STANDS in general; REFUTED on the engine under named premises (part 11) |
| P3 (psi + (-psi) = 0 is interference) | STANDS against the old law 7; REFUTED for this act, whose interference is between two quanta's two ways, opposite for bosons |
| P4 (commuting spinors are bosons; q >= 2; no pressure) | STANDS for the head's board; REFUTED in the clicks (q per state <= 1 by the arithmetic); degeneracy pressure OPEN |
| M1 (antisymmetry in the two-quantum product) | REFUTED: the act is that product |
| M2 (zeroing destroys wind) | STANDS against the old law 7; REFUTED here, since nothing is zeroed |
| M3 (an orbit is the exchange squared) | STANDS against the plan's sentence, which is replaced; the exchange is a full turn of one quantum about its own frame |
| M4 (the sign is a postulate) | REFUTED: the sign is the kind's full turn; the click's form is a law for every train alike |
| Sofer's two checks | answered (part 6) |
| David's 11.8 quanta | STANDS for the head's board; answered by one hand per quantum; his carry not needed (part 10) |

## 1. The words

**The clock words** (docs/CLOCK_WORDS.md) used here:
- the Node-clock, the Mesh and its two ends, the Spoke, the tick, the great clock;
- the train, the hand (a Gaussian integer z = three + i twelve), the twin hands (a twin pair psi = (psi1, psi2), two hands), the gear (its notch, fine tooth and teeth count), the carry;
- the wind, the winding, the click of a whole (law 5), the click of a split (law 6), the draw (law 9), the books (law 8), the remainder;
- the turnover (law 4), the ratchet and its pawl;
- the fitting (a pair from light at a Mesh's two ends), the unspringing (a pair into light), the bob.

**Named here:**
- **The 48.** In this draft, as in the brief, the 48 is 2O, the double cover of the 24: the 24 turns of the cube, each with its two signs. The plan's section 19 uses "the 48" for the 24 turns with their mirrors (O_h); this draft never uses that group.
- **A quantum's hand.** Each quantum of a train holds its own hand at every Node-clock (now, before, fine teeth, teeth counts). A matter train's state is the list of its quanta's hands. A fitting appends two hands; an unspringing removes two (part 4).
- **The parts of a click.** These are the places one quantum can be found: a detector's two senses (phi, T phi); an occupant's frame (phi, T phi); or a Mesh's two ends.
- **The overlap.** M_aj = <phi_a, psi_j> = SUM over the train's own components of conj(phi_a) psi_j, a Gaussian contraction.
- **The two-quantum amplitude** A_ab = M_a1 M_b2 + eps_T M_b1 M_a2, and **the joint size** sigma_ab = N(A_ab).
- **The phase reversal of a train T_T.** On a hand, z -> conj(z) (the head's K). On the twin hands, T(z1, z2) = (-conj z2, conj z1). This is i sigma_y K up to a unit, and it equals draft D's phi_perp.
- **The half turns' lifts on the twin hands**, exact integer acts:
  - H_x(psi) = (-i psi2, -i psi1);
  - H_y(psi) = (-psi2, psi1);
  - H_z(psi) = (-i psi1, i psi2).
- **The full turn of a train**, eps_T = the train's half turn applied twice: H(H(psi)) = eps_T psi.
- **The occupation** at a Node-clock: n = SUM_k psi_k psi_k^dagger over the quanta's hands there, read as (rho, S) with n = (rho + S . sigma) / 2.
- **Arithmetic.** N(x + i y) = x x + y y; <u, v> = conj(u1) v1 + conj(u2) v2; det[u, v] = u1 v2 - u2 v1; rho = N(psi1) + N(psi2); S = (2 Re conj(psi1) psi2, 2 Im conj(psi1) psi2, N(psi1) - N(psi2)).

**Equal quanta** are quanta of one train and one sense of the sweep. A quantum and its antiquantum, the two ends of a fitting, are told apart by their sweeps, a reading of the state, so they carry no exchange term. This answers the law's open question: "The one question that decides the build, named and not answered: whether the same state at a Node-clock is the same train (David's default) or the same train and the same sense (the antiparticle admitted)" (scribe-5 docs/ALGEBRA.md line 1562; line 1558 in the copy the plan cites).

## 2. The big law, named: the phase reversal law of the 24's double cover

**Statement.** Let V be any of the eight kinds of 2O, z the full turn and chi_V its character. Then:

    chi_V(z) / dim V  =  nu(V) = (1/48) SUM_g chi_V(g g)  =  T_V T_V

Here nu(V) is the Frobenius-Schur indicator, and T_V is any antiunitary act on V that commutes with all 48. All three are +1 on the five kinds of the 24 and -1 on the three spinor kinds.

**Its three faces:**
1. **On the board, the phase reversal.** A full turn reverses a twin hand: H(H(psi)) = -psi for every half turn's lift, and every lift of a half turn has order 4. Its value on one hand is +1. PROVED (P1); CHECKED (e1: 18 of 18 lifts; e2: 5,000 of 5,000 per axis).
2. **In the tensors, the clock of two equal quanta.** V x V holds A1 exactly once. It sits in the symmetric square on the 24's kinds and in the antisymmetric square on the spinor kinds, where it is det, the singlet. PROVED (P2, P3); CHECKED (e1: the A1 counts of Sym^2 and Alt^2 for all eight kinds).
3. **In time, Kramers.** Every 24-covariant phase reversal of the twin hands is lam (-i sigma_y) K, with square -N(lam), which is below 0. Every one of a hand squares to +1. PROVED (P4); CHECKED (e3: the generators of the tetrahedral 24 already force X = lam (-i sigma_y) in X conj(U) = U X; X conj(X) is a negative multiple of 1; and T commutes with all 48, 48 of 48).

**Why it is the cube's 24 and not less.** The half turns about two face axes commute as turns of the cube, but their lifts anticommute (ij = -ji). This is what makes every lift of a half turn of order 4, and every spinor kind quaternionic. CHECKED (e1, e2).
- On the 12 turns of the tetrahedron (2T), the two complex spinor kinds have nu = 0 while z = -1, and the two complex one-dimensional kinds have nu = 0 while z = +1. The law fails on 4 of its 7 kinds (e1, mutant M1).
- On a double with commuting lifts (O x Z2), every odd kind has nu = +1 while z = -1 (5 of 5; e1, mutant M2).

So the owner's choice of the 24 (the cube's turns, no mirrors) is the group whose double cover holds the law. A smaller group of turns, the tetrahedron's 12, would not.

## 3. Pauli from the big law, step by step (the owner's four steps)

Two equal quanta psi1, psi2 of a train T, and parts phi_a.

**Step 1, the amplitudes of two ways are added.** The pair is found at the parts (a, b) in two ways: quantum 1 at a and 2 at b, or the reverse. The click reads A_ab = M_a1 M_b2 + eps M_b1 M_a2 and takes its norm. This is the law's own joint credit: "the sign under exchange is a train's declaration that the click alone reads, the lists' factor and the joint credit's determinant or permanent" (ALGEBRA.md line 821; 817 in the cited copy). Only the declaration goes; the joint credit stays. What the draft adds is that eps comes from the kind.

**Step 2, the exchange is 0 or 180 degrees.**
- Exchanging the quanta keeps every size: N(eps) = 1.
- Twice it returns the pair: eps eps = 1, the double swap being trivial in three dimensions (M3).
- Among the Gaussian units (1, -1, i, -i) this leaves +1 and -1 alone. PROVED; CHECKED (e2, part 1).

**Step 3, Pauli by destructive interference.** At one part, A_aa = (1 + eps) M_a1 M_a2. With eps = -1 it is A - A = 0. PROVED; CHECKED (e2: 20,000 of 20,000).

**Step 4, the sign is the full turn (the big law).** eps_T = z_T, read on the board as the train's half turn applied twice.
- On the twin hands, (i sigma_z)^2 = -1. On the 24's kinds every half turn squared is the identity, and a hand is A1. PROVED (P1); CHECKED (e2, part 2).
- It has two forms:
  - **Topological.** The exchange of two framed quanta, with pair creation, is homotopic to a 2 pi turn of one quantum about its own frame (Finkelstein and Rubinstein 1968; Balachandran, Daughton, Gu, Marmo, Sorkin and Srivastava 1993). It is not an orbit of one quantum about the other. That orbit is the exchange squared, the trivial loop of step 2.
  - **Algebraic, a theorem on the engine.** eps_T is the one sign for which two equal quanta at one Node-clock can be wound into the clock (A1). For the twin hands Sym^2 E1/2 = T1 holds no A1, so only eps = -1 lets them form a clock, the singlet. For the 24's kinds Alt^2 holds no A1, so only eps = +1 does (e1, part 3).
- The topological form needs a configuration space of quanta, which the engine lacks (P1, part 10). The algebraic form needs none, and the derivation stands on it.

**What follows** (PROVED in part 7, CHECKED in e2):
- **At one Node-clock** the parts are its two senses (phi, T phi), for any frame phi. Then sigma_++ = sigma_-- = 0 and sigma_+- = sigma_-+ = rho(phi)^2 N(det[psi1, psi2]). The singlet's size is the same in every frame: it is the A1. CHECKED: 10,000 pairs x 5 frames.
- **A third twin quantum has no state.** The three-quantum amplitude over two senses has two equal rows in every assignment: 0 in all 8. CHECKED: 3,000 of 3,000; with eps = +1 never all 0.
- **Law 5's q per state.** q equal quanta in one part have amplitude PROD_j M_aj times SUM over the q! orders of eps^inversions. With eps = -1 that sum is 0 for q >= 2. CHECKED: q = 2 to 7.
- **The force carriers.** sigma_aa = 4 N(M_a1 M_a2), twice the value with the probabilities added. A balanced Gaussian splitter at a Mesh, psi1 = (1, i) and psi2 = (i, 1) at the ends x and y, gives sigma_xy = 0. The probabilities added give 2, and eps = -1 gives 4. For every Gaussian splitter, the coincidences order as bosons <= distinguishable <= fermions, and the bosons' are 0 exactly where N(a) = N(b) (e2: 20,000 of 20,000 splitters). This is a prediction that can fail on the engine.
- **The books.** For any parts with SUM_a phi_a phi_a^dagger = lam I: SUM over ordered (a, b) of sigma_ab = 2 lam^2 (rho1 rho2 + eps N(<psi1, psi2>)). For any parts at all: 2 [(psi1 G psi1)(psi2 G psi2) + eps N(psi1 G psi2)], with G = SUM_a phi_a phi_a^dagger. With eps = -1 this is 2 x the Gram determinant (Cauchy-Binet). CHECKED: 10,000 of 10,000 in each of four sets of parts.

**What the candidates of the brief became:**
- (a) the double cover as the phase reversal: face 1 of the big law.
- (b) Frobenius-Schur: face 2, and the theorem the algebraic step 4 stands on.
- (c) the exterior power in the click: steps 1 to 3 for k quanta. The k-quantum amplitude with eps = -1 is the coordinates of psi1 ^ ... ^ psik, so Alt^2 C^2 is the singlet and Alt^3 C^2 = 0. What forces the exterior product is eps_T = z_T, not a choice.
- (d) spin-statistics without relativity: step 4's topological form; its premises are in part 10, P1.
- (e) the lattice statistics of the hops: no route (part 10, P1 and P2; e6).
- (f) time reversal: face 3. It bears on the exchange sign through the theorem T T = nu. On its own, on the board, it is kinematics: Kramers' degeneracy.

## 4. The act in the new engine, with its expected lines

The act is written once, for every train alike, in the three operations: products, sums and Rule3. Every number is a gear's, a train's integer from the calibre, or a unit the hands' own arithmetic holds (i, and -1 = i i).

1. **The full turn of the train, eps_T, read once from the kind's table.** Apply the train's half-turn act twice to its unit gear and read the first coefficient: -1 on the twin hands (H_z(H_z(1, 0)) = (-1, 0)), +1 on a hand and on every train of the 24's kinds. 2 lines; the half turn's act is a row of the kind's table, the signed permutation with unit factors the 24 already carry.
2. **The phase reversal of the train at the turnover, T_T, a row of the kind's table.** It is a signed permutation of the train's own gears with conjugation flags: [three, -twelve] on a hand (the head's K), and (u3, u12, d3, d12) -> (-d3, d12, u3, -u12) on the twin hands (e3, part 6). The turnover writes now' = T(before) and before' = T(now), each fine tooth mirrored as the head mirrors it, gear by gear. Its rewind uses T^-1 = -T on the twin hands. 4 lines.
3. **The transport of the twin hands across a Mesh reads the ratchet's notch parity.** The neighbour's twin pair is read through T^delta, with delta the two ends' turnover counts' difference modulo 4: the pawls give delta modulo 2, and the parity of the ratchet's notch (the carries of its two teeth) gives the rest. 4 lines. The one-hand trains keep the pawl alone.
4. **The quanta's hands.** A matter train's state is the list of its quanta's hands. The fitting appends the two fitted hands (each the head's fitted notches, sense A now and i sense B before, at its end); the unspringing removes its two; the one formula steps every hand alike. About 10 lines in the state and the chart. This is the board's change (part 5).
5. **The joint size of equal quanta at the click's parts.** M_aj = <phi_a, psi_j(x)>, then sigma_ab = N(M_a1 M_b2 + eps_T M_b1 M_a2). For quanta of opposite sweep there is no exchange term: sigma_ab = N(M_a1 M_b2). The sweep's sign of a quantum is its hand's own, set by its fitting's end and kept by the step, which keeps W(u, u) (part 7, P11). 4 lines.
6. **The draw, law 6's Rule3.** c SUM sigma = t room + r_t; the pair of parts where t falls takes the two quanta, each comparison the quotient [x >= 0] = 1 + x div (x x + 1). The existing draw.
7. **The lay of a newcomer chi into an occupant phi at a Node-clock**, act 5 at the occupied state (part 6). Its parts are the occupant's frame: free N(<T phi, chi>), blocked N(<phi, chi>), room rho(phi) rho(chi) (Lagrange). Then c (rho(phi) rho(chi)) = t room + r_t. If blocked takes, there is no click. If free takes, the newcomer's hand is written at the Node-clock as the occupant's turnover image, (T phi_before, T phi_now). That image is orthogonal to the occupant however the occupant is spread (P11). It holds exactly one quantum where the occupant's hand holds its whole quantum at the Node-clock: a bob, a quantum that has clicked there. For an occupant spread over several Node-clocks, the image at one Node-clock holds only the occupant's share there, and scaling it to one whole quantum is no integer act (OPEN). 6 lines.
8. **The occupation reading** (rho, S) = SUM_k (rho(psi_k(x)), S(psi_k(x))), for the frame and the books. 2 lines.

**Expected lines.** About 32 added (the eight items above). About 85 removed: click.jam's standing and crowding tests with their logs (about 45); phase.crowded and claimed for the hands' writes (about 35); the setting's refusal (5); the loader key `exchange` on toys-5. The order-free sum of the light's takes at one Node-clock stays.

**What the act never does:**
- It writes no sign on the board and never forms psi + eps psi.
- It types no capacity, clamp or train's name: the zeros come from (1 + eps) = 0 and from repeated rows.
- It reads beyond one Mesh only where a joint click's parts lie at two Node-clocks, which it does not do: its parts are one Node-clock's senses, or a Mesh's two ends.

## 5. What the board must hold, and what the click books

**The board: one hand per quantum.** The owner's step 1 needs each quantum's own amplitude at the parts.
- A train holding one field per Node-clock holds only their sum. Its product at two parts adds the "same quantum at both" terms M_a1 M_b1 + M_a2 M_b2 that no pair of quanta has.
- For two quanta in one state, the two-quantum amplitude is 0 at every pair of parts, while the summed field's product is not (e4: 5,000 of 5,000 each).
- The filled orbital, read as one spinor phi + T phi, is a pure spinor with S . S = rho^2 (624 of 624). Against it a third newcomer finds a free size above 0 in 29,488 of 29,952 cases (e4). This is Sofer's 57,600 of 60,000, reproduced on another box.

PROVED (S . S = rho rho for every twin pair, draft D's P1; the product of a sum expanded); CHECKED.

**What the occupation (rho, S) is:**
- It is the reading n = SUM_k psi_k psi_k^dagger at a Node-clock. It lives nowhere as state, and is read at the click from the quanta's hands there (local: the Node-clock's own gears).
- It cannot be the state. Two boards with the same occupation at every Node-clock, differing by a phase i^(x + 2y) at each Node-clock, step to different occupations (e4: 20 of 20). The one formula steps amplitudes, and the occupation's own step needs the coherences between Node-clocks.

PROVED (P11); CHECKED.

**What the click books:**
- **Two equal twin quanta at one Node-clock.** In opposite senses they are booked as the singlet, of joint size rho(phi)^2 N(det). In one sense the joint size is 0, so they are never booked as two, and the wind of both stays in their own two hands.
- **Three:** never; the amplitude is 0 in every assignment. At most two per Node-clock per twin train, one per sense.
- **The force carriers:** any number at one Node-clock. Two at one part have joint size 4 N(M_a1 M_a2), and bunch.
- **The click of a whole (law 5)** on one quantum's hand books at most that quantum, wherever the hand's local wind does not exceed its whole. The wind's local density can be negative elsewhere (section 30, the mathematician), so this is OPEN for the engine's wind. Over several quanta at one Node-clock, q per state is at most 1 by the arithmetic of step 3. On the head's board, one field per train, law 5 can count q >= 2 at one Node-clock (David's 11.8); on the board of one hand per quantum that count is never formed.

## 6. Sofer's two checks: the act that writes the sign, and where the wind that cannot click is kept

1. **"The act that writes the exchange sign."** No act writes it on the board. The click's joint size reads eps_T, and eps_T is read once from the kind's half turn. The board never forms psi + eps psi.
2. **"The law's exact count of quanta kept where the board would hold 0 and the books booked two."** Two equal twin quanta in one state:
   - Their two-quantum amplitude is 0 at every pair of parts: the pair's "board" holds 0.
   - So the books book 0, not two.
   - The count kept is exactly the two quanta, each in its own hand, with their wind untouched.
   - No remainder is written, nothing is destroyed, and SUM over the Node-clocks of (wind + remainder) is unchanged by the act.
   - The old law 7, psi + (-psi) = 0, takes the two windings to 0 while booking two. It fails the books in 624 of 624 hands (e4; Sofer's 168 of 168).
3. **The partial cases.**
   - In the joint click of two given quanta, the deficit against the distinguishable whole, 2 lam^2 N(<psi1, psi2>), is exactly the part that cannot click together. It stays in the two hands.
   - In the lay, the blocked part is no click: nothing is taken from the light, and the newcomer's wind stays where it stood.

   PROVED (P6, P7); CHECKED (e2, parts 4 and 9).

## 7. The proofs (protocol step 2)

- **P1, the full turn and the half turns.**
  - In 2O, z = -1 is central.
  - A half turn h of the cube (h h = 1) lifts to g with g g in {1, z}. In the unit quaternions a lift of a turn by pi has real part cos(pi/2) = 0, so g g = -1 = z.
  - On a train of the 24's kinds, g acts through its turn h, so g g acts as h h = 1. A hand is A1, so its half turn is 1.
  - The face lifts i, j, k satisfy ij = -ji, while the turns diag(1,-1,-1) and diag(-1,1,-1) commute.

  PROVED. CHECKED (e1: 18 of 18 lifts square to z; 24 ordered pairs of face lifts anticommute; e2: H H = -1 on 5,000 twin pairs per axis).
- **P2, the A1 of V x V is one, and lies in Sym^2 or Alt^2.**
  - Each kind of 2O has a real character, so V is self-dual and V x V = Hom(V*, V) holds A1 once (Schur).
  - The A1's in Sym^2 and Alt^2 number (1/48) SUM (chi(g)^2 +- chi(g g)) / 2, whose sum is 1 and whose difference is nu.

  PROVED. CHECKED (e1, part 3, for all eight kinds).
- **P3, nu = chi(z)/dim on 2O.**
  - The five kinds of the 24 are real (the 24 signed permutation matrices, and their permutation parts on the axes), so nu = +1 = chi(z)/dim.
  - On E1/2, det[M u, M v] = det(M) det[u, v] = det[u, v] for M in SU(2), so the A1 is det, antisymmetric: nu = -1 = chi(z)/dim.
  - E5/2 = E1/2 x A2 and G3/2 = E1/2 x E carry the product of an antisymmetric and a symmetric form, antisymmetric: nu = -1, and z = -1 on both.
  - On 2T, chi of the kinds 1', 1'', 2', 2'' is complex, so nu = 0.

  PROVED. CHECKED (e1, 8 of 8; the mutants 4 of 7 and 5 of 5).
- **P4, T T = nu (Kramers).**
  - An antiunitary J = X K commutes with the 48 iff X conj(U) = U X for every lift.
  - Two such X differ by an element of the commutant of an irreducible kind, a scalar (Schur). So X = lam X0, and J J = X conj(X) = N(lam) X0 conj(X0).
  - On the twin hands X0 = -i sigma_y, with X0 conj(X0) = -1.
  - B(u, v) = <J u, v> is then the A1 pairing, and B(v, u) = (J J) B(u, v), so J J = nu.
  - On a hand J = K, J J = 1.

  PROVED. CHECKED (e3: the solution space of X conj(U) = U X over Q is spanned by -i sigma_y and its i multiple; X conj(X) is a negative multiple of 1 for every solution tried; det[phi, chi] = <T phi, chi> at 56,160 of 56,160; <T phi, phi> = 0 at 624 of 624; <K z, z> = z z, never 0, at 80 of 80).
- **P5, the turnover with T.**
  - T commutes with all 48 lifts: sigma_y conj(U) sigma_y = U on SU(2). K commutes only with the real lifts, the 8 turns about the y axis, or 16 of 48 up to a sign.
  - On the reading, T is S -> -S, which commutes with all 24 turns. K is S -> (Sx, -Sy, Sz), which commutes with 8.
  - T keeps rho, reverses S, exchanges the two twins' sweeps (keeping their sum), and squares to -1. So the turnover is no involution on the twin hands, and its rewind is T^-1 = -T.
  - T^n = (-1)^(n div 2) T^(n mod 2): the sign is the carry of the ratchet's two teeth.

  PROVED. CHECKED (e3: 48 of 48, 8 of 48, 16 of 48, 24 of 24, 8 of 24; 20,000 of 20,000 in each line; n = 0 to 16 on 500 pairs). On the head: e5, 375 of 375 Node-clocks with K's image, and 69 of 69 nonzero readings off T's.
- **P6, steps 2 and 3.**
  - N(eps) = 1 and eps eps = 1 leave eps = +-1 among the units.
  - A_aa = (1 + eps) M_a1 M_a2.
  - The q-quantum amplitude in one part is PROD M times SUM_pi eps^inversions(pi), and with eps = -1 this sum is 0 for q >= 2. Composing with one transposition pairs the orders and changes the parity.

  PROVED. CHECKED (e2, parts 1, 3 and 7).
- **P7, the books (Cauchy-Binet).**
  - SUM_(a,b) N(A_ab) = 2 (SUM_a N(M_a1))(SUM_b N(M_b2)) + 2 eps Re[(SUM_a M_a1 conj M_a2)(SUM_b M_b2 conj M_b1)] = 2 [(psi1 G psi1)(psi2 G psi2) + eps N(psi1 G psi2)].
  - With G = lam I this is 2 lam^2 (rho1 rho2 + eps N(<psi1, psi2>)).
  - With eps = -1 it is 2 det(M^dagger M) = 2 SUM_(a<b) N(minor_ab).

  PROVED. CHECKED (e2, part 4: 10,000 of 10,000 in each of four sets of parts, both signs).
- **P8, one Node-clock, the singlet.**
  - With the parts (phi, T phi) the overlap matrix is Phi^dagger [psi1, psi2], with Phi = [phi, T phi] and det Phi = rho(phi).
  - So A_+- = det(Phi^dagger) det[psi1, psi2] = rho(phi) det[psi1, psi2], and A_++ = A_-- = 0. The size is independent of phi up to rho(phi)^2.
  - Three quanta over two parts repeat a row: 0.

  PROVED. CHECKED (e2, parts 5 and 6).
- **P9, Sofer's occupant frame is the same act.** Put psi1 = phi (the occupant) and psi2 = chi (the newcomer), with the parts (phi, T phi):
  - M_+1 = rho(phi), M_-1 = <T phi, phi> = 0 (Kramers), M_+2 = <phi, chi>, M_-2 = <T phi, chi> = det[phi, chi].
  - So sigma_+- + sigma_-+ = 2 rho(phi)^2 N(<T phi, chi>) (the free part), sigma_++ + sigma_-- = 0, and the distinguishable whole less the two-quantum total is 2 rho(phi)^2 N(<phi, chi>) (the blocked part).
  - Lagrange gives free + blocked = rho(phi) rho(chi), Sofer's room.

  PROVED. CHECKED (e2, part 9: 3,744 of 3,744). Also: with n = (rho + S . sigma)/2, chi^dagger n chi = (rho rho(chi) + S . m)/2, so Sofer's free (2u - rho) rho(chi) - S . m = 2 chi^dagger (u - n) chi, the hole projector (e2, part 10: 20,000 of 20,000; one quantum there 389,376 of 389,376; the filled orbital 389,376 of 389,376).
- **P10, the bound.**
  - free >= 0 for every newcomer iff the larger eigenvalue (rho + |S|)/2 of n is at most u, that is S . S <= (2u - rho)^2 with rho <= 2u.
  - blocked >= 0 for every newcomer iff S . S <= rho^2.

  PROVED (the extremes of chi^dagger (u - n) chi over a newcomer are the eigenvalues). CHECKED (e2, part 11: 0 negative sizes inside; 22,384 of the 22,560 occupations inside Sofer's |S| <= rho <= 2u but outside this bound give a negative free size in the box, for example (2u, (0, 0, 2u)), two quanta in one sense).
- **P11, the board.**
  - The one formula's linear step a+ = 2a - a- + g SUM_j (a_j - a) - d a, alike on every hand (L real and symmetric), keeps W(u, v) = SUM_x <u_now, v_before> - <u_before, v_now>, since W+ - W = SUM [<L u, v> - <u, L v>] = 0.
  - It does not keep SUM_x <u_now, v_now>.
  - The occupant's turnover image v = (T u_before, T u_now) has W(u, v) = <u_now, T u_now> - <u_before, T u_before> = 0 and W(v, v) = W(u, u): an equal quantum, orthogonal to the occupant.
  - A child set at one Node-clock meets a spread hand there alone.
  - The occupation is not closed under the step.

  PROVED. CHECKED (e4, parts 3 to 5: 24 of 24 ticks with 3 x 3 entries; the one-slot form moved at 24 of 24; 20,000 of 20,000; 200 of 200; 20 of 20).
- **P12, the half-turn transport (candidate e).**
  - With U_a = H_a: U_a U_b U_a^-1 U_b^-1 = -1, a flux pi in every plaquette, and H_x H_y H_z = -H_z H_y H_x.
  - The covariant step's A = -SUM_a H_a (S_a - S_a^-1) has A A = SUM_a (2 - S_a^2 - S_a^-2), since the cross terms cancel by the anticommutation. So M = 6 + A has the eigenvalues 6 +- 2 (SUM sin^2 k_a)^(1/2).
  - The uniform field has M psi = 6 psi, with no zero mode at k = 0, and the extremes 6 +- 2 r3 sit at the eight k = (+-pi/2)^3.
  - The pawls f_ij = s_i s_j are a pure gauge.

  PROVED. CHECKED (e6; on the 4^3 torus A^2 (A^2 - 4)(A^2 - 8)(A^2 - 12) = 0 on 4 of 4 random fields, and the lower product is not 0 on 4 of 4; e5: the head's pawl signs have plaquette product +1 at 15,000 of 15,000).
- **P13, the side question.** The states of E1/2 x E1/2 fixed by a group H of lifts number (1/|H|) SUM chi(h)^2:
  - 1 for the 48, the singlet;
  - 1 for the 16 lifts of the Mesh's axis taken as a line;
  - 2 for the 8 lifts of the quarter turns about the Mesh: the singlet and the triplet's component along the Mesh, (0, 1, 1, 0), which the 8 end-exchanging half-turn lifts reverse.

  PROVED. CHECKED (e7).

## 8. The probes and their counts (protocol step 3)

Run with python3 -I in this folder; e5 with /home/user/Universe24/venv314/bin/python -I e5_head.py S/t24/src (sys.path set to that src explicitly). Each probe's mutations run with the argument `mutants` and must fail; every output is kept beside its probe.

| probe | what it checks | the claims | the mutants (each must fail) |
| --- | --- | --- | --- |
| e1_law48.py (.txt, _mutants.txt) | the 48 built exactly; the eight kinds from the group; nu against chi(z)/dim; A1 in Sym^2 and Alt^2; the half turns' lifts | 0 failures; 8 of 8 kinds | 2T fails on 4 of 7; commuting lifts fail on 5 of 5; the sign flipped fails on 8 of 8 |
| e2_click.py | steps 1 to 4; Pauli; the books; one Node-clock; the third; q per state; bunching; Sofer's frame; the occupation; the bound | 0 failures | eps = +1 on twin hands: 1,996 of 2,000 pairs with sigma_aa > 0; probabilities added: 1,998 of 2,000; the exchange term conjugated: 1,998 Pauli and 2,000 books failures of 2,000; the parts unexchanged: books fail 1,998 of 2,000; K's partner: 576 of 624 own states free; capacity u: 1,791 of 3,744 negative; capacity 3u: a third free 3,744 of 3,744 |
| e3_reversal.py | T against K: the 48, the 24, Kramers, uniqueness, the ratchet's carry, the turnover's gear table | 0 failures | K: 32 of 48 lifts break the reading, 576 of 624 non-Kramers, eps read as K K +1 on 624 of 624; T without its sign: 40 of 48 break, 624 of 624 square +1; the exchange without conjugation: 496 of 624 non-Kramers |
| e4_board.py | the head's board cannot hold two quanta; one hand per quantum; Bessel on the one-slot form; the step's two-slot form; the partner; the occupation is no state; the two-slot occupation of one quantum not positive | 0 failures | 8 of 8 equal pairs exceed one quantum in one sense at their Node-clock; K's image not orthogonal 5,000 of 5,000; T without the slot exchange 5,000 of 5,000; unequal steps move W 6 of 6 |
| e5_head.py (.txt) | the head's turnover on twin hands (bit for bit), the head's pawls, the head's lay jam on its own twin world | 0 failures: K at 375 of 375; T's -S differs at 69 of 69; pawl plaquettes +1 at 15,000 of 15,000; Lagrange at 1,440 of 1,440 ends | (a harness on the head: it reads, it mutates nothing) |
| e6_hops.py | the half-turn transport: flux, T-junction, the 4^3 spectrum; the pawls | 0 failures | commuting transports: flux 3 of 3 and T-junction 1 of 1 fail; a non-product link sign: 16 of 16 plaquettes -1; the plain transport: 1 of 1 |
| e7_pair.py | the side question's fixed states | 0 failures | the triplet along the Mesh moved by 40 of 48; the 8's count 2, not 1 |

One requested mutation is no mutation. "The sign on the wrong term", eps M_a1 M_b2 + M_b1 M_a2, keeps every size, since N(eps x + y) = N(x + eps y) for eps = +-1 (e2, N1: 2,000 of 2,000 unchanged). The mutations that do fail are the exchange term conjugated and the parts left unexchanged (M3 and M4 of e2).

**Where the head holds no fake, the probe is the head's own code** (e5):
- `Clock.reverse` with `hands.signs` is K on every twin hand.
- `meshes.pawls` is a pure gauge.
- On the head's own twin world (tests/worlds/world_nature.json with every sprung train as four gears, as the head's test test_a_train_of_four_gears_at_a_spring_is_twin_hands_and_keeps_the_spin builds it, 20 ticks), `click.jam`'s standing test refuses 303 twin fittings:
  - 51 of them have an occupied end whose free size is 0, so this draft's act refuses them too;
  - 252 leave a free size above 0 at every occupied end, so the act would draw them, 57 with certainty;
  - the head keeps 155, none with a blocked part.

  This is the head's one-field board read with the act's sizes. It is indicative only, since that board holds the twins' sum (part 5).

## 9. What it replaces, and the rows it moves (protocol step 4)

- **The calibre key `exchange`** (toys-5, the measurement branch's loader key; the law's "declared word", ALGEBRA.md lines 821 and 1047). It goes: eps_T is read from the kind. The law's lines on the exchange stand until Sofer's sentence and the owner's word (TENSOR24.md section 24, "For the law").
- **click.jam** (the standing test, "where any of the fitted hand's hand already stands at its clock", and the crowding test) goes, replaced by the lay of act 7 at each end. A fitted hand is laid into its end's occupant by the occupant's frame. Two fitted hands of one train landing at one Node-clock in one click are read by their joint size: the same sense gives size 0, the opposite gives the singlet. The unspringing's light children pass by the arithmetic (eps = +1), not by a coupling comparison.
- **phase.crowded and phase.claimed** for the hands' writes go. With one hand per quantum, two fitted hands are two hands and share no gear, so no order can choose between their writes, and the jam's one remaining role, Pauli's, is the joint size. The order-free sum of the light's takes at one Node-clock stays.
- **The setting's refusal by name** ("Pauli at the setting: a twin hand sweeps two quanta at a clock, refused by name", assembly/setting.py, E16) goes from the engine. The setting is data. Two quanta of one twin train set in one state have joint size 0 at every frame (Gram 0), and the files' checker outside the engine reports such a setting by that same arithmetic (TENSOR24.md section 21: "the exclusion's refusal among them goes with Pauli's derivation").
- **Section 16's Pauli row and law 7** change text. "An exchange is a full turn of one quantum about the other" becomes "the exchange of two equal quanta has the sign of the full turn of one quantum about its own frame (the big law); the click reads the two-quantum amplitude with that sign". "psi + (-psi) = 0" is struck (M2, P3).
- **Section 22's first row** (the exclusion's refusals) is replaced by the click's joint size.
- **Section 24 item 1** stands, with its derivation: "derived from the kind under the click's law". The hostile physicist's "an axiom" becomes, for the clicks, the law of the click's joint credit (named, the same for every train). For the board, the bound stays OPEN (part 12).
- **The turnover (law 4)** on the twin hands becomes T in place of K. This moves every twin chart at a turnover: S reversed, the twins' sweeps exchanged. Law 4's "an involution" holds on the 24's trains and becomes "of period four" on the twin hands.

**The rows:**
- **Row 43 (exclusion).** It now counts the lay jam itself (predicates.py:185-191) and becomes two independent readings: the clicks per sense per Node-clock per tick (never two of one sense of one twin train), against the kind's eps.
- **A bunching row, new:** a Mesh whose two ends see a balanced splitter's two light quanta (each its own hand): coincidences 0 for the light, every click for a twin train.
- **Every twin fitting** that the head's standing test refuses with a free size at both ends (e5: 252 of 303 on the twin world) is now drawn.
- **Rows 17, 65 and 70** (the typed senses) are untouched by this draft.

**Contradictions with nature it leaves:** part 12.

## 10. The objections, one by one

- **P1, "An exchange is a half-braid. The belt trick links it to a 2pi turn only for framed particles, in a two-particle configuration space the engine lacks."**
  - STANDS against the topological route.
  - The engine meets some of the premises:
    - twin quanta are framed by their own phase: a twin pair up to its sign is a quaternion, and so a frame; psi and -psi give one turn, z the full one (e1: q and -q give the same turn, 48 of 48);
    - it has pair creation and annihilation, the fitting and the unspringing;
    - it has three dimensions.
  - It lacks the configuration space of quanta and the continuity of an amplitude on it. The theorems are about loops in that space (Finkelstein and Rubinstein: "the observed relation between spin and (exchange) statistics follows from continuity alone"; Balachandran et al.: the proofs "assume certain continuity conditions involving the existence of antiparticles"). One hand per quantum holds the product configuration but no path.
  - REFUTED as a bar to the derivation: the algebraic face of the big law (P2 to P4) is a theorem on the 48 and needs no configuration space.
- **P2, "Spin-statistics needs Lorentz invariance and microcausality. Without them, spin and statistics are independent."**
  - STANDS in general. Spin one half bosons are consistent lattice models, and so are spinless fermions.
  - REFUTED on the engine, under the premises of part 11.
- **P3, "psi + (-psi) = 0 is interference, which bosons show too."**
  - STANDS against the old law 7, which is struck.
  - REFUTED for this act. Its interference is between the two ways of two quanta, the two-quantum amplitude, never within one quantum's field. Bosons show it with the opposite sign: bunching, sigma_aa = 4 N(M_a1 M_a2), and no coincidence at a balanced splitter. Fermions antibunch (e2, part 8).
- **P4, "Commuting spinors are bosons, and law 5 counts q >= 2 per site. Degeneracy pressure cannot follow."**
  - The first clause STANDS for the head's board. One commuting field per train is a bosonic mean field: its sum lets a third quantum in (e4), and David's 11.8 quanta gather on it.
  - The second clause is REFUTED in the clicks. q per state is at most 1 by SUM_pi sgn(pi) = 0. The commutativity of the integers is exactly what makes det[psi, psi] = 0: the product of two equal hands cancels in the antisymmetric amplitude.
  - The third clause, degeneracy pressure on the board, is OPEN (part 12).
- **M1, "psi+(-psi)=0 adds one-quantum amplitudes, but antisymmetry lives in the two-quantum product."** REFUTED for this draft: its act is that product, M_a1 M_b2 - M_b1 M_a2.
- **M2, "Zeroing the field destroys wind, against the books."**
  - STANDS against the old law 7 (e4: 624 of 624).
  - REFUTED here: no field is zeroed; the pair that cannot click keeps its wind in its two hands (part 6).
- **M3, "A full orbit of one quantum about another is the exchange squared, which is trivial in 3D."**
  - STANDS against the plan's sentence, which is wrong and is replaced (part 9).
  - The orbit is the double swap of step 2, the source of eps eps = 1. The exchange equals the full turn of one quantum about its own frame.
- **M4, "Without relativistic locality the sign is a postulate: mark it declared."** REFUTED with its premise named.
  - No sign is declared. It is the kind's full turn, read from the train's own half turn, an integer act, and equal by theorem to T T and to the A1's symmetry.
  - What the derivation takes is the click's form: the joint credit is the two-quantum amplitude, and its sizes are the clock's. That is one law for every train, the law's own joint credit (line 821), not a sign.
  - Mark: derived from the kind under the click's law.
- **Sofer's two checks:** answered in part 6.
- **Sofer's note of 2026-10-28, reproduced with independent code:**
  - his points 1 to 5 (e3, e2 and e4 counts above);
  - his point 6, that the single spinor cannot be the filled orbital (e4: 29,488 of 29,952);
  - his law 7 count (e4: 624 of 624);
  - one correction: his bound is not enough (P10).
- **Sofer's open points, with this draft's answers:**
  1. The sizes of a lay are law 6's overlaps with the occupant as the detector. PROVED (P9): the occupant's frame (phi, T phi) is draft D's (phi, phi_perp), and the click of a whole (one quantum arrives, its winding whole) and the click of a split (where it lays) are one carry, c (rho(phi) rho(chi)) = t room + r_t.
  2. The written state at every occupation.
     - One occupant: write the newcomer at the Node-clock as the occupant's partner. In the one-slot reading this is T phi, orthogonal by Kramers. In the two-slot reading it is the turnover image (T phi_before, T phi_now), orthogonal and an equal quantum (P11; e4).
     - Orthogonality holds however the occupant is spread. One whole quantum is written exactly only where the occupant is held at the Node-clock (a bob); otherwise the scale is OPEN.
     - Several occupants spread over many Node-clocks: exactly orthogonal writes need their Gram matrix, a sum over the board. OPEN.
  3. The bound between clicks. It is not kept by the step in the one-slot form (e4: the one-slot form moved at 24 of 24 ticks). In the two-slot form, which the step keeps, one quantum's occupation is not positive. So the bound is met only at the next click. There the two-quantum form's sizes are norms and never go below 0, while the occupation form's free size can (P10). OPEN for the board itself.
  4. Locality. The lay reads the Node-clock's own quanta's hands and the newcomer. The joint click reads one Node-clock's senses or one Mesh's two ends. PROVED (P11, a child at one Node-clock).
- **David's measurement** (DAVID-PAULI-DYNAMICS.md: on the head, twin wind gathers to 11.8 quanta at one Node-clock, and "nothing in Rule3 holds a twin to one quantum there").
  - STANDS for the head's board: one field per train sums the twins' winds.
  - With one hand per quantum no hand holds more than its own quantum, the clicks book at most one per sense per Node-clock, and the books keep what is not booked.
  - His proposal, "the write beyond one quantum carried to its twin", is neither needed nor taken. The second quantum at a Node-clock is its own hand, laid into the occupant's partner by the click. Nothing is carried between twins, and where the partner too is taken, a third has no state and no write.
  - If the board keeps one field per train, his carry is the only board-level exclusion. It would be a nonlinear write, its form his and OPEN.

## 11. The answer to P2: what stands in for Lorentz invariance and microcausality

In relativistic field theory the sign comes from two places. The first is the Lorentz group: the strong reflection lies in the identity component of its complexification and lifts to (-1)^(2j) on spin j. The second is locality: the field must hold both the quantum's annihilation and its antiquantum's creation, tied by the invariant pairing C, with C^T = (-1)^(2j) C. On the engine the stand-ins are:

1. **The 24's double cover** (the 48, with its anticommuting half-turn lifts) stands in for the complexified Lorentz group as the source of the sign. Every half turn's lift squares to z, and nu = chi(z)/dim on all eight kinds (P1, P3). It would not stand with the tetrahedron's 12, or with commuting lifts (e1).
2. **The click's law** stands in for the field's covariance and its pairing C. The joint credit is the two-quantum amplitude, the clock (A1) of two equal quanta is its sizes' kind, and the phase reversal T commutes with the 24. The A1 pairing is C, and its symmetry is the sign (P2, P4).
3. **The cone of one Mesh a tick** stands in for microcausality only as locality of the act. The joint click reads one Node-clock's senses or one Mesh's ends; it fixes no sign.
4. **Pair creation (the fitting)** stands in for the field's particle-antiparticle content only with an A1 spin write. That write gives the pair the singlet (P13). It is needed for Bell (draft D), not for the exchange sign.
5. **Framing** is met (a twin pair up to sign is a frame) but used only by the topological form.
6. **Reversibility (the rewind)** is not used for the sign. The rewind of the turnover with T is exact, with T^-1 = -T.

## 12. What it leaves (OPEN), and the contradictions with nature

1. **The board's change.**
   - One hand per quantum changes the state's shape: a matter train's hands grow with its quanta.
   - Without it the click's Pauli cannot be read, because the sum loses the two ways (e4).
   - The light, a coherent field of many quanta, keeps one field. Its clicks show a coherent field's statistics, not a single photon's bunching, except where single light quanta are given their own hands.

   OPEN for the build. The decision is the owner's.
2. **Degeneracy pressure and the field's gathering.**
   - In the one-slot form, Bessel's bound holds for orthogonal quanta (e4: 255 of 255 sets, and the filled band rho = 2u, S = 0), but the step does not keep that form.
   - In the two-slot form, which the step keeps exactly, one quantum's occupation has S . S - W W = 4 N(det[now, before]) >= 0 and so a negative eigenvalue (e4: 19,998 of 20,000).
   - So no bound on the board follows from the step as written. The step's carries also move the two-slot form by their rounding.
   - Nature's bound comes from the fermion field's anticommuting algebra, which a commuting integer field lacks.

   OPEN (David's, with the step's carries).
3. **Several spread occupants.** The exact lay size of a newcomer into k occupants is the Gram determinant's ratio. It reduces to the local hole projector chi^dagger (u - n(x)) chi only for orthonormal occupants. Keeping them orthonormal after a lay needs their Gram matrix, a sum over the board. OPEN: the locality limit of exact fermion statistics on a local board of commuting integers.
4. **Exchange forces** (the Fock term) are absent. The interactions read the occupation's direct part (section 18 item 19 stands).
5. **The topological step 4** is no theorem on the engine (P1). The algebraic form carries the derivation.
6. **The turnover with T** has period four on the twin hands. Law 4's "involution" and the twin transport's read of the ratchet's notch parity are text changes for Sofer's sentence (part 4, act 3).
7. **Coincidences at detectors more than one Mesh apart** would need a joint click that reads two Node-clocks beyond one Mesh. The act reads one Node-clock or one Mesh. A splitter's bunching at distant detectors needs the joint click where the quanta overlap. OPEN, as draft D's Bell closure is.
8. **The lattice hop by the half turn's lift** (candidate e) would put a flux pi through every plaquette and take the twin hands' zero mode from k = 0 to the eight points (+-pi/2)^3. It is rejected as the twin transport (e6).
9. **Levin and Wen's criterion** does not apply. It asks hopping operators t_ij |j, i_1, ...> ~ |i, i_1, ...> acting on many-particle states, "the state |i,j,...> which contains particles at sites i,j and other particles far away", with hops on distinct sites commuting (Phys. Rev. B 67, 245316, eqs. 2 to 4). The engine's step moves fields, and the pawls carry no flux (e5, e6). The paper's conclusion that "fermions never appear alone - they always come with some kind of gauge field" names what an engine of fields would need for fermions on the board itself: a Z2 gauge field with flux, as in exact bosonization (Chen, Kapustin and Radicevic, Ann. Phys. 393, 234 (2018), a bosonization map "preserving the locality of the Hamiltonian"). The pawls are a pure gauge.
10. **Contradictions with nature.** None is new from the sign: matter is antisymmetric and the clicking force carriers symmetric, as in nature. Left: no degeneracy pressure on the board (item 2); no exchange forces (item 4); the light's clicks a coherent field's (item 1).

## 13. The side question: does an A1 source give the fitting's pair the singlet?

- If the fitting conserves the kind in the sense that its spin write commutes with all 48 acting on the pair's spins, Schur gives one fixed state: the singlet. PROVED (P13); CHECKED (e7: 1 for the 48). So draft D's premise ("the pair's split reads the A1 part of its two fitted hands") is this draft's law of the click: the click's spin write is the clock's kind.
- The head's fitting orients the pair by the light's lead along the Mesh and its twist, a vector along the Mesh and a pseudoscalar. A spin write that reads that axis is fixed only by the 8 quarter-turn lifts about the Mesh, which leave two states: the singlet and the triplet's component along the Mesh (e7: 2 for the 8). The 8 end-exchanging half turns reverse that component (8 of 8), but they reverse the lead too. So an A1 light alone gives the singlet, and a lead-reading fitting needs the axis-blind spin write as a premise. CHECKED.
- A singlet across a Mesh's two ends is no product of two hands. One hand per quantum holds products and one Slater determinant. At one Node-clock the singlet of two equal quanta is one Slater determinant, phi ^ T phi = rho(phi) det. The fitted pair's singlet needs the pair's joint amplitude held with the pair. OPEN (draft D's carriage).

## 14. Where this draft and David's helper would differ

The helper's brief, as named to this draft, is "the lay's book read on the board with the train's exchange sign". If it reads the wind of the board's sum of the occupant and the child with the sign, it differs from this draft in five places:
1. **The quantity read.** This draft reads the two-quantum amplitude, a product of two overlaps, never the wind of a sum.
2. **Two quanta in one state.** The board-level book holds (1 + eps) psi, and its wind is 0 for eps = -1: two windings gone while two are booked (M2). This draft books nothing and keeps both.
3. **The board.** This draft needs one hand per quantum. The board-level book keeps one field per train.
4. **A third quantum.** The board's sum phi + T phi is a pure spinor, and it lets a third in (e4: 29,488 of 29,952). This draft's third has no state.
5. **Two parts for the force carriers.** A summed field's book gives a coherent field's coincidences. This draft gives no coincidence at a balanced splitter.

**Where they agree:** at one part with eps = +1 the factor 4, and in the opposite senses at one Node-clock, where the sum has no cross term.

## 15. Status of every claim

| claim | status |
| --- | --- |
| the big law on all eight kinds of 2O (nu = chi(z)/dim = T T) | PROVED (P1 to P4); CHECKED (e1, e3) |
| it fails on 2T and with commuting lifts | CHECKED (e1 mutants) |
| eps = +-1 (steps 1, 2); sigma_aa = 0 for eps = -1 (step 3) | PROVED (P6); CHECKED (e2) |
| eps_T = the half turn squared = z_T (step 4, algebraic) | PROVED (P1, P3); CHECKED (e1, e2) |
| step 4, topological, on the engine | OPEN: no configuration space (P1) |
| one Node-clock: the singlet alone, the frame-free size; a third has no state; q per state <= 1 | PROVED (P6, P8); CHECKED (e2) |
| bunching and no coincidence at a balanced splitter for the force carriers | PROVED; CHECKED (e2); on the engine's own step OPEN |
| the books (Cauchy-Binet) | PROVED (P7); CHECKED (e2) |
| Sofer's occupant frame = this act at the occupied state | PROVED (P9); CHECKED (e2) |
| Sofer's bound corrected to S . S <= (2u - rho)^2 | PROVED (P10); CHECKED (e2) |
| T forced on the twin hands; the head applies K | PROVED (P4, P5); CHECKED (e3; e5 bit for bit on the head) |
| one hand per quantum needed; the occupation a reading, no state | PROVED (P11); CHECKED (e4) |
| the step keeps the two-slot form; the partner is the turnover image | PROVED (P11); CHECKED (e4) |
| the lay is local | PROVED (P11); CHECKED (e4) |
| the head's lay jam over-refuses against the act | CHECKED (e5: 252 of 303), indicative |
| degeneracy pressure on the board | OPEN (part 12, item 2) |
| several spread occupants exact and local | OPEN (part 12, item 3) |
| the half-turn transport rejected (flux pi, eight minima) | PROVED (P12); CHECKED (e6) |
| the singlet from an A1, axis-blind spin write | PROVED (P13); CHECKED (e7) |
| the fitted pair's singlet held on the board | OPEN (part 13) |

## 16. Literature relied on (quoted as read)

- **A. P. Balachandran, A. Daughton, Z.-C. Gu, G. Marmo, R. D. Sorkin, A. M. Srivastava**, "Spin-statistics theorems without relativity or field theory", Int. J. Mod. Phys. A 8, 2993-3044 (1993), DOI 10.1142/S0217751X93001223 (INSPIRE record). The abstract opens "Conventional proofs of the spin-statistics theorem either use relativistic quantum field theory". Per the record, the proofs assume certain continuity conditions involving the existence of antiparticles, and non-Abelian statistics (parastatistics, braid statistics of order 2 or more) are excluded in the paper's framework.
- **D. Finkelstein, J. Rubinstein**, "Connection between spin, statistics, and kinks", J. Math. Phys. 9, 1762-1779 (1968) (INSPIRE record). "Sufficiently nonlinear classical fields admit modes called kinks"; "a rotating kink can have half-odd angular momentum, if double-valued state functionals are admitted"; "the observed relation between spin and (exchange) statistics follows from continuity alone".
- **M. Levin, X.-G. Wen**, "Fermions, strings, and gauge fields in lattice spin models", Phys. Rev. B 67, 245316 (2003), section III, eq. 4: the statistics are e^{i theta} where t_il t_ki t_ij = e^{i theta} t_ij t_ki t_il, for hops t_ij |j, i_1, ...> ~ |i, i_1, ...> (eq. 2) that commute on distinct sites (eq. 3), read on "the state |i,j,...> which contains particles at sites i,j and other particles far away". Section IV: "fermions never appear alone - they always come with some kind of gauge field."
- **Y.-A. Chen, A. Kapustin, D. Radicevic**, "Exact bosonization in two spatial dimensions and a new class of lattice gauge theories", Ann. Phys. 393, 234-253 (2018). The map takes "an arbitrary fermionic system on a 2d lattice to a lattice gauge theory while preserving the locality of the Hamiltonian".
- **M. V. Berry, J. M. Robbins**, Proc. R. Soc. Lond. A 453, 1771-1790 (1997). Not read in the original. Secondary sources (Harrison and Robbins, arXiv math-ph/0302037; Anastopoulos, quant-ph/0110169) describe the construction as a spin basis transported with the particles through Schwinger's representation, giving the physical sign, with its single-valuedness condition disputed by one author (Reyes, Mainz 2006). It is not used here.
- **The group theory** (Frobenius-Schur, Schur's lemma, Wigner's three types) is computed in e1 and e3, not quoted.
