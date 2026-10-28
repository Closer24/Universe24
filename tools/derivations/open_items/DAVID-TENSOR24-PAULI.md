# Pauli at the click: Tensor24's law 7, derived from the kind's own pairing and the phase reversal

David, 2026-10-28, 11:4x UTC, for the Boss (Sofer and Animate copied). This page answers three of the owner's words:
- through the Boss (6467107471, 10:4x UTC): "Pauli is derived from a very important law. It is about the clicks, note. On the board it is the phase reversal. It must be derived from a big law. Think clocks, think tensors and Rule3."
- through Sofer (6467182879): "Pauli never as a postulate. It is derived from the phase reversal of a family on the board; in a click this gives Pauli; check it."
- to David, 11:0x UTC: "Did you get the solution for Pauli?" Yes, through both lines.

It also answers Sofer's four open items (SOFER-PAULI-PHASE-REVERSAL-1.md, scribe-5 f767a4e08) and the reviews' P1 to P4 and M1 to M4. It is TENSOR24.md section 19's law 7 (Pauli's act), at the protocol's steps 1 to 5, and it derives law 7 as the plan words it at engine-5.0-test 943a40df7. It is read on that head, whose src is 8b657aa57's; toys-5's src is the same. The second hand has confirmed it (below); Sofer's check follows, then my sign-off. Each claim is marked PROVED, CHECKED or OPEN; the probes and their outputs are in DAVID-TENSOR24-PAULI_CHECKS.txt. No src is pushed.

## The big law: a family pairs as its kind pairs

1. **The kind's own pairing.** Two copies of one kind are compared by a bilinear form B that every turn of the 24 keeps.
   - On the 24's kinds the condition is M^T B M = B.
   - On the twins it is M^T B M = det(M) B, since their turns hold up to a scale.
   - The form is computed, not chosen. The probe solves these equations exactly under the half turns, the quarter turn about z and the third turn about the diagonal.
   - **Each kind keeps exactly one form (Schur).** CHECKED on all eight kinds of the double cover.
   - **It is symmetric on the 24's five kinds,** A1, A2, E, T1 and T2: the force carriers' kinds.
   - **It is antisymmetric on the three spinor kinds,** E1/2, E5/2 and G3/2: matter. On the twins it is the determinant, B(phi, chi) = phi1 chi2 - phi2 chi1. CHECKED.
   - **Its sign** is the kind's Frobenius-Schur indicator and the full turn's sign on the kind.
   - **The half turns alone already exclude a symmetric form on the twins,** since they anticommute there (XY = -YX). CHECKED.
   - **The same holds with the rotations about the twins' axis written exactly on the gears,** as Gaussian units up to a phase (the quarter turn about z as diag(1, i)). This is my readings helper's correction of DAVID-TENSOR24-THE-CLICK.md's check 10, which said the quarter turn doubles the reading; that page takes the correction at its next edit. CHECKED.
2. **The phase reversal is that pairing with every phase reversed.** T phi = conj(B^T phi), so that <T phi, chi> = B(phi, chi).
   - On the twins this gives T(z1, z2) = (-conj z2, conj z1), which is Sofer's T. On the force carriers it gives T z = conj z.
   - **T T is the pairing's own sign:** -1 on matter, +1 on the force carriers. PROVED: T T = (B conj B)^T, and here eps eps = -1 and 1 1 = 1. CHECKED.
   - **Kramers:** <T phi, phi> = B(phi, phi) = 0 on matter. A quantum of matter is orthogonal to its own phase reversal. CHECKED.
3. **The law of the pair, one sentence for every family alike:** a family's two quanta exchange as its kind pairs. The family's exchange sign is the sign of its kind's own pairing.
   - **Read in the click:** two quanta at one node-clock are one whole of the family. The one whole of two copies of a kind that the 24 keep is its pairing.
   - CHECKED in the pair space directly. The vectors of phi (x) chi that every turn keeps form one line on each kind. The exchange acts on that line by -1 on the twins (the singlet u d - d u) and by +1 on A1 and T1.
   - **It names no family and no sign.** The signs come from the 24: matter is antisymmetric and the force carriers are symmetric. This is what the owner's word of 2026-10-27 asked for: Pauli from the families' symmetries, not put in by force.
   - **This is the spin-statistics connection,** since the indicator is (-1)^(2s). The law is put in once, for every family; Pauli itself is not put in.
   - **OPEN:** deriving the law itself from the hops, through the pawl's turns around a loop (the Boss's draft E candidates).

## The click: a quantum laid where its family stands (Sofer's open 1)

1. **The pair's size.** A newcomer chi laid at a node-clock where an occupant phi of its family stands writes the pair phi (x) chi + e chi (x) phi, where e is the family's sign.
   - Its size, half the norm of that product, is N(phi) N(chi) + e N(<phi, chi>).
   - The share is that size over the room N(phi) N(chi). PROVED.
2. **On matter, with e = -1 in two dimensions,** Lagrange gives N(phi) N(chi) - N(<phi, chi>) = N(det(phi, chi)) = N(<T phi, chi>).
   - **Free:** the newcomer's part along the occupant's phase reversal.
   - **Blocked:** its part along the occupant, N(<phi, chi>).
   - **For the occupant's own state** the free size is exactly 0, so the draw never lays it. PROVED; CHECKED.
3. **It is law 6's split, read on the board.** Read on the gears, the free share is the split share of the newcomer against the occupant's phase reversal as the detector.
   - The newcomer is laid where c (W_c + W_c) W_o < room (W_c W_o - S_c . S_o). Here (W_c, S_c) is the newcomer's reading and (W_o, S_o) the occupant's, reversed to (W_o, -S_o).
   - So the click of a whole and the click of a split are one carry: a quantum is written, and whether it is written is the draw by sizes, free against blocked. It is cut 1's draw: one product against another, Rule3's sign test.
   - CHECKED on 3,170 turning pairs, exactly.
   - **Mutant:** with the occupant itself as the detector, not reversed, the same state is laid whole. It is caught.
4. **The general occupation.** Let (rho, S) be the occupation and u one quantum's wind. Then the free share is (2u - rho) rho_d - S . m over 2u rho_d, which is Sofer's cap.
   - It is the one contraction of the newcomer with the free reading (2u - rho, -S): the capacity's identity less what stands.
   - With one quantum standing, the free reading is the occupant's phase reversal.
   - On the filled orbital it is 0, so a third quantum has no state. CHECKED.
5. **On the force carriers, with e = +1,** the pair's size is the room or more. The newcomer is always laid and nothing is blocked. CHECKED on A1 and T1.
   - Its excess over the room, the overlap's share, is the stimulated weight. Its use in the rates is OPEN.
   - **Beyond two dimensions, the pairing's own size is not the lay's size.** On a vector kind, a . a = 0 for the circular (1, i, 0), which would block a boson. The lay's size is the pair's norm. On the twins the two agree, by Lagrange. CHECKED.

## The phase reversal on the board, and what the lay writes (Sofer's open 2)

1. **On a twin pair's gears, the phase reversal is three exact acts with no division:**
   - the now and the before exchanged (the rewind);
   - every phase conjugated (the twelve gear's sign);
   - the two twins exchanged with one sign.

   So the up twin's now becomes -conj(down's before), the down twin's now becomes conj(up's before), and the befores move the same way.
   - **It maps the pair's reading (W, S) to (W, -S) for any gears,** not only for a turning pair. Applied twice, it is -1 on every gear. PROVED: the new doubled density is eps^T D^T eps, and sigma_y sigma_k^T sigma_y = -sigma_k. CHECKED.
   - **On the head's real twin gears it is exact** at all 11,625 pair readings of the twin world over 30 ticks, with 5 births. CHECKED.
   - **The rewind is part of it:** with the now and the before left in place, the wind changes sign (the antiparticle). The mutant is caught on 1,981 of 2,000.
   - **On a single hand (a force carrier)** it is the now and the before exchanged, each conjugated. It keeps the sweep, and applied twice it is the identity. CHECKED.
2. **The free outcome writes the occupant's phase reversal.**
   - It is one quantum, since the reversal keeps the wind.
   - It is orthogonal to the occupant, so the board's wind gains exactly one quantum, with no cross term.
   - The occupation goes from (u, S) to (2u, 0), and the books gain one quantum.
   - The blocked outcome writes nothing and takes nothing.
3. **The pair must stand as two hands.** On one field the reading can never be (2u, 0), nor the open reading (W, 0).
   - **On one field, det D <= 0.** The field's doubled density is a rank-one matrix plus its adjoint, and W^2 - S . S = 4 det D. So one field reads pure (|S| = W) or worse (|S| > |W|), never mixed. PROVED; CHECKED on 12,000 random gears.
   - **Exactly, det D = -N(det[now, before]).** It is 0 only where the now and the before are parallel, which is draft D's verifier's form. CHECKED on 6,000.
   - **The same holds on the head's twin world:** det D > 0 at 0 of 11,625 readings. Of these, 499 are pure, 3,034 worse and 8,092 empty. CHECKED.
   - **Written as two hands,** the occupant and its reversal read (2u, 0) for any gears, and every third newcomer's free size is 0. CHECKED.
   - **Summed on one field,** the two do not read (2u, 0). The third newcomer's free size falls below 0 for 6,631 of 13,283 newcomers and is above 0 for 6,652. So one field cannot carry the cap. CHECKED; it is the same finding as Sofer's 57,600 of 60,000.
4. **On the head, a twin family is one field.** Its up and down hands hold every quantum's wind on the same gears: unwind.advance adds onto what stands (my helper's code facts at 8b657aa57).
   - So on one field the derived rule leaves no partner: a standing quantum of matter leaves no free state that the field can hold.
   - **The double occupancy needs the field's phase reversal beside it.** This is the partner at one node-clock, an atom's filled orbital: "on the board it is the phase reversal". The alternative is to give each quantum of matter its own hand.
   - **The same reading is Draft D's open axis.** A child born open reads (W, 0): the field and its reversal at half a quantum each. One answer serves both, as Sofer said.

## The bound between clicks (Sofer's open 3)

1. **The step does not keep the cap.** It is linear, so two equal waves superpose, and one field gathers the wind of many quanta at one node-clock: 11.8 quanta at one node-clock on the head (DAVID-PAULI-DYNAMICS.md). A field holds the symmetric algebra, the force carriers': any number in one state.
2. **Quanta held as orthogonal hands keep the cap exactly.** The local occupation is then the node-clock's block of a projector, so 1 - O(x) is positive at every node-clock, whatever the hands. PROVED: a projector's diagonal block is at most 1. CHECKED on 1,500 node-clocks of random orthogonal sets.
   - A step that keeps the hands' overlaps keeps the cap.
   - The engine's carries keep the overlaps only up to their remainders. OPEN.
3. **So the cap is met at the click.** Between clicks it is kept only by the antisymmetric algebra on the board: the quanta of matter as hands, read through the determinant at the click. Which representation the plan takes is the owner's word (below).

## Locality (Sofer's open 4)

The lay reads only the occupant's gears at its node-clock and the newcomer's. The phase reversal acts on one node-clock's gears. PROVED, by the formulas' arguments. Two quanta at different node-clocks are not constrained by the click.

## What it replaces

1. **The lay jam** (click.jam's "lay"). It refuses a fitting wherever the landing hand holds any positive wind at that end at the tick's start, including a tail from a neighbour. My helper measured it on the head:
   - the twin world: 1,012 jams against 5 births in 60 ticks;
   - nature as written: 1,183 jams against 3 births.

   It is replaced as follows:
   - **On the force carriers and on every one-hand row,** no exclusion is derived: a one-hand row is the scalar kind A1, so the files' one-hand matter rows are bosons by their kind. The jam there is a fake and goes. The light alone took 199 and 300 of those jams.
   - **On the twins,** the jam becomes the lay's draw against the occupation, at a whole quantum, not at any wind.
   - **The crowded jam** (two children on one hand at one node-clock in one click) becomes the second child's draw against the first. Its order-free form is OPEN.
2. **The setting's refusal by name** ("Pauli at the setting": a twin hand sweeping two quanta at a clock) goes. A setting lays its quanta by the same rule.
3. **The children's twins at a birth:** the minus child goes on the vernier's hand s and the plus child on its twin, and the log writes the literal senses [-1, 1] (run.py:68). These are the pair's pairing on the twins, and they go with Draft D's open axis. OPEN; one cut.

## The reviews' points on Pauli (TENSOR24.md section 30)

1. **P1 and M3: an exchange is a half-braid, and a full orbit is the exchange squared.** This derivation uses no orbit and no belt. The sign is the kind's pairing, computed. It equals the full turn's sign on the kind, which is what the owner's fourth step points at, but it is not obtained from a path.
2. **P2 and M4: without Lorentz invariance and microcausality, the sign is a postulate.**
   - The law of the pair is declared once, for every family alike. Every sign is derived from it: the calibre's exchange key and ALGEBRA.md's declared exchange go.
   - So M4 holds for the one law and not for any family's sign.
   - Deriving the law itself from the lattice's locality is OPEN.
3. **P3 and M1: psi + (-psi) is one-quantum interference, while the antisymmetry lives in the two-quantum product.** The law acts on the pair, phi (x) chi + e chi (x) phi, never on one field's sum.
4. **P4: commuting spinors are bosons, law 5 counts two or more quanta at a site, and degeneracy pressure cannot follow.**
   - **On one field this holds,** and it is PROVED here: one field's reading is never mixed, and it gathers wind.
   - **At the click it does not.** Law 5's count at a node-clock goes through law 7: on matter the click books the whole quanta there one at a time, each by the lay's draw against what it has booked. So it books at most the kind's dimension, 2.
   - **Between clicks,** degeneracy follows only from matter's quanta standing as orthogonal hands. That keeps the cap (PROVED), and which representation the plan takes is the owner's word.
5. **M2: zeroing the field destroys wind.** Nothing is zeroed. The free outcome adds one orthogonal quantum, and the blocked outcome writes nothing and takes nothing. The wind that cannot click stays on the board as the remainder.

## The second hand (protocol step 5)

1. **CONFIRMED.** A second helper wrote its own exact probe from the claims alone, without opening mine. It re-solved every claim:
   - the invariant forms, by exact elimination over Q(i) and again by the characters of the 48 (the Frobenius-Schur indicator -1 on the three spinor kinds and +1 on the other five);
   - the phase reversal, the board's reading, the lay's share, the two hands against one field, the cap between clicks and the force carriers;
   - the head's twin gears.

   It found no failure in 1,464,812 cases (1,382,662 in the algebra, 82,150 on the head), and it caught all 24 of its mutants. With T's minus sign dropped, both of its probes exit 1. I reran both, and the outputs are identical.
2. **Its three notes:**
   - **On G3/2 the scale is the twins' factor's det,** the square root of the 4x4's det. My probe used it, and the characters agree.
   - **The share cannot see the rewind.** A detector read as (-W, S) instead of (W, -S) gives the same share, since the share is a ratio. The rewind shows only in the wind's sign, which the written partner needs. So the rewind serves the write, not the share.
   - **On one field the summed wind is exactly 2W.** What breaks the filled orbital is S, with S . S >= 4 W^2.
3. **Its finding on the head, for the plan:**
   - **All 499 pure twin readings sit where one twin hand is empty.** Wherever both hands hold wind, det D < 0. In 1,788 of the 3,005 such readings with W not 0, S . S >= 2 W^2.
   - **So no head twin pair is ever a spinor turning with both components.** There its reading has |S| > |W|, outside the bound |S| <= rho of Sofer's open item 3.
   - **The cause has two parts** (my count). Of the 2,584 readings where both twins sweep, 1,395 have opposite signs: the birth lays the minus child on one twin and the plus child on the other, so a negative and a positive wind meet at one node-clock. In the other 1,189 the twins turn apart, and det[now, before] is not 0. Both are cut (e)'s, with draft D.

## For the Boss: law 7 and its cuts

1. **Law 7 as the plan words it at 943a40df7 stands, and this page derives it:**
   - the sign e from the kind's own pairing, computed under the 24;
   - the two ways' sizes, sigma_ab = N(M_a1 M_b2 + e M_b1 M_a2). Summed over the parts they are twice the pair's size, N(phi) N(chi) + e N(<phi, chi>) (CHECKED on 8,000 cases). On matter one part for both has size 0, and on light it has four times its size (CHECKED);
   - on the board, the phase reversal as the rewind, with every phase conjugated and the twins exchanged with one sign.
2. **The cuts:**
   - (a) the lay's draw, one contraction, in the click's gate (cut 5);
   - (b) the jam on the force carriers out;
   - (c) the setting's refusal out;
   - (d) the representation of matter: either the phase-reversed field beside each matter family, or each quantum its own hand. The owner's word decides; only the second keeps the cap between clicks;
   - (e) the birth's twins, with Draft D's open axis.
3. **OPEN, by name:**
   - the law of the pair, derived from the hops;
   - the use of the stimulated weight;
   - the carries against the hands' overlaps;
   - the partial occupation: a spread quantum's wind at the node-clock below u.
