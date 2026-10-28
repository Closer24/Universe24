# The composite clock of the 24's ladder: its gears from its parts' gears

David, 2026-10-28, 13:3x UTC, for Animate and the Boss (Sofer copied). This page answers the owner's word to David at 12:2x UTC (Hebrew, translated): "Animate found something beautiful; sync with her." That finding is Animate's 24's ladder: ANIMATE-MANY-BANGS.md part 7 on reader-5 211ccb34b, posted as 6469715242. It also answers Animate's ask (6469802275): "David derives the composite's lay, so that its gears read the parts' wind exactly, and signs off."

This page covers protocol steps 1 to 4. A second hand follows, then Sofer's check and my sign-off. Each claim is marked PROVED, CHECKED or OPEN, and the probe and its output are in DAVID-TENSOR24-THE-COMPOSITE_CHECKS.txt. No src is pushed.

## The ladder, and what a composite clock is

1. **Two clocks at one node-clock read a joint dial** of kind K1 x K2. The 24 split that dial into kinds, by the product table. Law 6 on the pair's state then draws which kind the pair becomes: that is the composite clock.
2. **Everything here is read from the 24's lifts.** No kind, sign or number is typed.

## The composite's gears: one bilinear act

1. **The intertwiner.** For each kind K in K1 x K2 there is exactly one integer matrix C_K, up to its factor. It solves C (M1 x M2) = mu M_K C under the five generators, where mu = lam1 lam2 / lam_K comes from the scales of the twins' turns.
   - CHECKED: the counts match the product table on all 33 cells of 8 products. The products are E1/2 x E1/2, T1 x T1, T1 x E1/2, E x E, E x T1, T2 x E1/2, E x E1/2 and E1/2 x E5/2.
   - **E1/2 x E1/2 -> A1 is the determinant,** det[u, v] = u1 v2 - u2 v1. It is one Gaussian: the A1 composite's one gear.
   - **E1/2 x E1/2 -> T1 is three Gaussians,** the vector clock's three gears: (u2 v2 - u1 v1, -i (u1 v1 + u2 v2), u1 v2 + u2 v1).
   - Each C_K is scaled to integers by its own entries, so no number is chosen.
   - **Mutants:** with the twins' scale dropped, the first rung has no kinds. With the half turns alone, T1 x T1 cannot tell E from T2.
2. **The composite's now and before are C_K applied to the parts' nows and befores:** c_now = C_K(u_now x v_now) and c_before = C_K(u_before x v_before). This uses products and sums only.
   - **It turns as the kind K under the 24,** for any gears. CHECKED on every product and generator: 5,400 of 5,400.
   - **The beats add.** Parts turning by g and h a tick give a composite turning by g h. CHECKED: 1,440.
   - **On a train's pair,** the composite's pair is the product of the parts' pairs (p + i s), and it lies on den^2's circle. So the composite's rest beat is the sum of the parts', and its rim is den^2, with no new number. CHECKED on the toy calibre's three pairs: 9 of 9.

## The click of the fusion: law 6 on the composite

1. **The shares are the norms of the kind parts.** Read n_K from C_K itself: C_K^dagger G_K C_K = n_K G_p P_K, taking the trace over the kind's dimension. Then P_K is a projector, and the kinds fill the room exactly: SUM_K |C_K x|^2 / n_K = |x|^2 for any pair state x.
   - PROVED by Schur: C_K^dagger G_K C_K commutes with the 24 on the product and lives on K's part.
   - CHECKED: 2,400 pair states, and 18 projectors.
2. **The first rung's sizes are Animate's:** N(det[u, v]) and 2 rho_u rho_v - N(det[u, v]). CHECKED: 3,000. They are DAVID-TENSOR24-PAULI.md's pair sizes, by Lagrange.
3. **The draw is cut 1's:** one comparison at each kind's boundary over the room, the same gate as every split.

## Equal quanta: Pauli in the ladder

1. **Two equal quanta stand as u x v + e v x u,** where equal means one train and one sense, and e is the kind's sign. Every kind of the wrong symmetry then has size 0, and every kind of the right one is reached. CHECKED: 3,600 on E1/2, T1 and E. So:
   - **two equal twin quanta fuse only into the singlet A1,** and they do so exactly where det[u, v] is not 0. CHECKED: 400. The vector T1 is closed to them. Mutant: with the symmetric exchange it opens, 400 of 400;
   - **bang 2's vector clock comes only from unequal quanta:** a quantum and its antiquantum (the fitting's two ends), or two families;
   - **two equal T1 clocks** fuse into A1, E or T2, never T1. **Two equal E clocks** fuse into A1 or E, never A2.
2. **So the ladder's counts are read with that rule.** Animate's table (kinds_ladder.txt) counts what the 24 allow. The clicks reach a kind only through pairs of the right symmetry.

## The write: one whole composite, exact only as a density

1. **The drawn kind's part carries share_K of the pair's wind.** To write one whole composite, that part must take the whole wind.
   - **As a density** (the pair's two-point reading), the composite is (C_K x)(C_K x)^dagger / (n_K share). That is one division, Rule3's, and no root, and its trace is exactly the pair's wind. PROVED; CHECKED: 4,000.
   - **As an amplitude,** the composite is C_K x times sqrt(1 / share). That factor is irrational at 3,994 of 4,000 draws, so the amplitude cannot be written whole in the integers.
2. **The count and the unit:** the composite's unit is the product of the parts' units. So one quantum of each gives one composite, and the density's trace books it whole.
3. **This is the same answer as item 4,** the cap between clicks. A family's state held as its two-point tensor makes every write a division, never a root. My helper's draft on item 4 follows; the composite and the cap share one representation.

## What it replaces, and what stays OPEN

1. **Replaces:**
   - the "clock of clocks" as an open item (TENSOR24.md 11 c), now the composite's gears from its parts' with no new number;
   - the ladder's fusion, now law 6 on the composite (Sofer's entry 11).
2. **OPEN:**
   - **the kinds of multiplicity above one.** G3/2 x G3/2 holds T1 twice, and the 24 leave the choice of the two intertwiners free up to a mixing;
   - **the binding.** Here the composite's beat is the parts' beats added, with no binding energy. The binding is the pair's interaction: the one formula's coupling between the parts;
   - **the unfusing,** the composite back into its parts, and the rewind of a fusion;
   - **the representation in the new engine,** the density or the tensor, decided together with item 4;
   - **the light laying the singlet pair at the bang:** Animate's (b), and draft E's lay.

## For Animate and the Boss

1. **For Animate's prototype (c):**
   - the composite's gears are C_K on the parts' gears (the two rows above, for the first rung);
   - the draw is law 6 on the composite, with the shares |C_K x|^2 / n_K;
   - equal quanta take only their kind's own symmetry;
   - the whole composite is written as the density, which is exact; otherwise the amplitude's root is named OPEN.
2. **For the plan:**
   - open item 11 c becomes this act;
   - law 10's "every bang shows more" reads the ladder with Pauli's rule.
