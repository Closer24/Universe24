# Draft D1: energy at a click (item 3, question 4), with notes for David on question 1

For the Boss. Revised on the change of scope of #2187 6488418223: question 4 (David's item 7) is the derivation, and
question 1 is notes and probes for David, who derives his items 5 and 6 himself.

How it was made:
- **Where:** on my own worktree at origin/tensor24-review, first 298bec5d8 and then a64a60444. src/tensor24 is identical
  at both, with zero changed lines. The worktree is removed.
- **What the probes run:** the engine's own functions, in exact integers: step.tick, step.sources, step.drive,
  step.driven, load.plan, load.trains_of and main.made.
- **Where they are:** probes/ beside this file, each script with its output .txt beside it; from the repository's
  root, `PYTHONPATH=src:<this folder>/probes python <probe>`, on the engine at a64a60444 (7a's Layout of seven fields).
- **Status:** a draft, verified by the Boss (VERIFY.md).

Scope: the 7a act, with the synchronous round at the full rate (every clock beats every round) and W = W+. That
includes the 7b gearing at rest, W = W+ = 2T with s = 2.

---

## Question 4: energy at a click

### The answer in plain words

1. **What the act keeps exactly: the wholes.**
   - The gear's carry keeps the stride with its fine tooth, M = W (a - b) + r. At W = W+, M+ = M + push, bit for bit.
     This confirms the 7b table's identity; the other drafter checked it too.
   - The drive's carry keeps the source: T_d q + r_d+ = J + r_d, bit for bit.
   - Both held at 8,077 of 8,077 round-ticks on random worlds (P1).
2. **The energy is the wind**, E = SUM W (a - b)^2 + s a . K b, with K b = D b - pull(b). This is section 27's rational
   leapfrog form: products of the gears now and before over the clock and its six neighbours.
   - The act does not keep it. It moves it by an exact, local amount:

         E(a+, a) - E(a, b) = SUM (a+ - b) (s T_k q - (r+ - r))

     That is the click's work, plus the fine teeth's defect. It held bit for bit at 8,077 of 8,077 round-ticks (P1),
     and at the 7b gearing at 1,609 of 1,609 (P7).
   - At each Node-clock, the same law holds with an antisymmetric flux through its six Meshes. The wind at a clock moves
     by exactly its own click's work, its own fine tooth's defect, and what its Meshes carry, with
     Phi(i -> j) = -Phi(j -> i). That held at every row and site of 1,250 of 1,250 round-ticks, with J and the drive (P8).
3. **The free gear: no exact invariant exists, so I give a bound.**
   - For W >= 2 with s K invertible mod W, the only polynomials in (a, b, r), of any degree, that the free act keeps
     are the constants (the theorem below).
   - P2 (the exact rational nullspace on the engine's tick) found only constants in 5 of 5 such worlds. Its controls
     keep what the theorem says they should: the wind at W = 1, the momentum SUM M with no spring, and the wind where
     s K is a multiple of W (the fine teeth then never move).
   - **The 7b gearing** (W = 2T, s = 2) fails the hypothesis, since s and W share the factor 2. As the Boss's note says,
     it is the act at (T, 1) by a common factor: the fine tooth is r = 2 r' + e, and the parity bit e is kept for ever.
     P7 checked this bit for bit at 1,609 of 1,609 round-ticks, with J and the drive. The theorem applies to the reduced
     act. At (4, 2) and (6, 2) the kept space is the constants and the parity bit (dimension 2), and the wind is not
     kept (P7).
   - This extends David's item 7 ("no quadratic charge of one state escapes the torque") to every degree and to the
     energy.
4. **The invariant that holds the remainders, in the only form there is.** The wind with its defect booked is kept
   exactly:

       E_n + SUM over past ticks of SUM (a_(k+1) - a_(k-1)) (r_(k+1) - r_k) - (the clicks' work) = E_0.

   The defect is a product of each gear's own readings (its two strides and its fine tooth's change), so the clock
   where it happens can book it, as it books a remainder.
5. **The proved bound on the drift.** Where the wind is positive definite (the board's stability, fixed by springs and
   grips alone):
   - **Free gear:** |sqrt E+ - sqrt E| <= sqrt(SUM (r+ - r)^2 / W) < sqrt(SUM W) at every tick. So the root of the wind
     drifts at most linearly in time. It held at 44,366 of 44,366 ticks (P5).
   - **With J and the drive:** |sqrt E+ - sqrt E| <= sqrt(SUM (s T_k q - (r+ - r))^2 / W). It held at 2,445 of 2,445
     round-ticks (P9).
   - Both checks are exact rationals, with no root taken.
   - **What the wind actually did** (free, small worlds, 4,000 ticks): it wandered between 0.42 and 1.99 of its start.
     That is far inside the bound, but not "within one quantum" on those worlds. One orbit came back exactly to its
     start after 366 ticks; the step is a bijection, so a bounded orbit is periodic (Postulate 4, seen).
6. **What a click does to the energy.**
   - The drive's carry adds exactly s T_k (a+ - b) q to the wind at its own Node-clock: the work of its q quanta over the
     two strides. The rest of J stays in r_d, so over a run the carried source is the total source to within one tooth.
   - "Energy checked in the clicks through the beat before and after" is therefore a reading that can fail. At the click's
     Node-clock, the wind after less the wind before must equal the work, plus the defect, less the Meshes' flux, exactly
     (P8's law).
   - A click keeps no energy by itself. With a cubic coupling no exact energy exists, since the step is a leapfrog with
     a non-linear force. What a click with its take keeps exactly is the sweep pairs; see the notes for David below.

### The derivation

1. **The step as an equation.** At W = W+, synchronous:
   - u = W (a - b) + r + push, and (a+ - a, r+) = (u div W, u mod W). The home cancels.
   - So M+ = W (a+ - a) + r+ = u = M + push, and

         W (a+ - 2a + b) = -s K a + s T_k q - (r+ - r),   F = pull - D a = -K a.

   - K is symmetric because each Mesh has one grip, read alike from both ends (board.py pairs a Spoke's two ends).
2. **The wind's change.** With E(a, b) = (a - b)^T W (a - b) + s a^T K b, which is symmetric in a and b:

       E(a+, a) - E(a, b) = (a+ - b) . [W (a+ - 2a + b) + s K a] = (a+ - b) . (s T_k q - (r+ - r)).

3. **The local law.** Split each Mesh's term half and half between its two ends:

       e_i = W (a_i - b_i)^2 + s D a_i b_i + (s/2) SUM over the Spokes of g (a_i - a_j)(b_i - b_j),   SUM_i e_i = E.

   Then:
   - the clock's own part is (a+_i - b_i) [W (a+ - 2a + b)_i + s D a_i];
   - the Mesh halves give (s/2) SUM g (a_i - a_j) [(a+_i - b_i) - (a+_j - b_j)].

   Substituting step 1:

       de_i = (a+_i - b_i)(s T_k q_i - (r+ - r)_i) - SUM over the Spokes of Phi(i -> j),
       Phi(i -> j) = (s/2) g (a_i - a_j) [(a+_i - b_i) + (a+_j - b_j)].

   The bracket is symmetric in i and j, and (a_i - a_j) is antisymmetric, so Phi(i -> j) = -Phi(j -> i). This is the
   method's F_ij = -F_ji for energy.
4. **No polynomial invariant** (the free act). Suppose Q(a, b, r) is kept. Write Q_r for each value of the fine teeth.
   - Where the residue of u is j, the step is affine: (a+, a) = M (a, b) + ((r - j)/W, 0), with
     M (a, b) = ((2 - kappa) a - b, a) and kappa = s K / W.
   - If s K is invertible mod W, every residue j is reached from every r, on lattice cosets that are dense for
     polynomials. Matching the pieces gives Q_r(a, b) = P(a + r/W, b) for one polynomial P.
   - P must satisfy P o M = P. It must also be invariant under the translations (r/W)(e, e), because
     M^-1 (u, 0) = (0, -u). So P depends on a - b alone.
   - Then P(u) = P(u - kappa a) for all a. With kappa invertible, P is constant.
   - With no spring, K has the constants in its kernel, and P may depend on SUM (a - b + r/W) = SUM M / W.
   - Where s and W share a factor c, write W = c W' and s = c s'. Then u = c u' + e with e = r mod c, so
     (u div W, u mod W) = (u' div W', c (u' mod W') + e). The act is (W', s') with the bits e kept, and the theorem
     applies to (W', s' K). For 7b, c = 2 and (W', s') = (T, 1).
5. **The bound.** The step is z+ = M z + (e, 0), with e = (s T_k q - (r+ - r)) / W, and E(M z) = E(z). Where E is
   positive definite, sqrt E is a norm, so

       |sqrt E(z+) - sqrt E(z)| <= sqrt E((e, 0)) = sqrt(SUM (s T_k q - (r+ - r))^2 / W).

   With q = 0 this is below sqrt(SUM W), because |r+ - r| < W.
6. **The click.** The work term of steps 2 and 3 is the click's. Summing the drive's identity gives
   T_d SUM q = SUM J + r_d(0) - r_d(n).

### The probes

All are in probes/, each with its .txt output.

- **p1_wind_identity.py**, 1,600 random worlds (boards 1..3 per side, 3 rows, with W, s, D, T_k, T_d, the grips and J
  random). M+ = M + push and T_d q = J + r_d - r_d+ held at 8,077 of 8,077 round-ticks.

  | Case | The wind's identity | E kept exactly | The mutant (no remainder term) |
  | --- | --- | --- | --- |
  | W = 1, no J | 2,400 of 2,400 | 2,400 | the same (r = 0) |
  | W 1..9, no J | 2,400 of 2,400 | 8 | 8 |
  | W = 1, with J | 1,556 of 1,556 | 120 | the same (r = 0) |
  | W 1..9, with J | 1,721 of 1,721 | 0 | 11 |

- **p2_no_invariant.py:** the exact rational nullspace of Q(tick(state)) - Q(state) over monomials up to degree 4 (one
  gear) or 2 (two gears), times every function of r.

  | World | Dimension kept | What is kept |
  | --- | --- | --- |
  | One gear, W = 1 | 3 | E |
  | One gear, W = 2, D = 1 | 1 | constants only |
  | One gear, W = 3, D = 1 | 1 | constants only |
  | One gear, W = 3, D = 2 | 1 | constants only |
  | One gear, W = 2, D = 2 (s K = 0 mod W) | 6 | r and E |
  | Two gears, W = 1, D = 0 | 4 | E and Pi |
  | Two gears, W = 2, D = 0 | 7 | Pi, not E |
  | Two gears, W = 2, D = 1 | 1 | constants only |
  | Two gears, W = 3, D = 1 | 1 | constants only |

- **p5_drift_bound.py:** 12 free worlds with E positive definite (Sylvester's criterion by exact Bareiss minors), 4,000
  ticks each.
  - The free bound held at 44,366 of 44,366 ticks.
  - E ranged from 421 to 1,986 per mille of its start.
  - One orbit came back to its start after 366 ticks.
- **p7_gearing_7b.py:** the 7b gearing (2T, 2) against (T, 1), 300 worlds, half with J.
  - The trajectories and r = 2 r' + e agree at 1,609 of 1,609 round-ticks.
  - The parity bit is kept at 1,609 of 1,609.
  - The wind's identity holds at 1,609 of 1,609.
  - One free gear at (4, 2) and at (6, 2) keeps a space of dimension 2 (the constants and the parity), and the wind is
    not kept.
- **p8_local_wind.py:** 300 worlds with J and the drive, 1,250 round-ticks, 1,177 of them with a drive quantum.
  - The local law holds at every row and site at 1,250 of 1,250.
  - The flux is antisymmetric at 1,250 of 1,250.
  - The densities sum to E at 1,250 of 1,250.
  - The mutant with no flux holds at 62 of 1,250.
- **p9_drive_bound.py:** 400 worlds with E positive definite, J random. The bound with the drive held at 2,445 of
  2,445 round-ticks.

### What stays open

- **The asynchronous beat** (rate < Gamma, the runner's masks). The laws above are for the synchronous round. With reads
  "as seen", a clock's wind mixes counts. Not derived.
- **W != W+** (the riding gear). The teeth change and home(W+) - home(W) add a term. Not derived.
- **A bound uniform in time,** better than linear in sqrt E. Not proved. For one gear this is a round-off rotation of the
  plane, whose boundedness I did not settle.
- **A modified energy kept to a bounded drift under a cubic coupling.** Not derived.
- **The scale question.** Whether the wobble stays within one winding w_c (David's item 7, "within one quantum") on the
  head's trains is not shown. It needs the trains' real amplitudes against W.

**Method: addressed.**
- **(a) Which clock or gear produces each term.**
  - The wind is a contraction of the gear now and before over its clock and six neighbours. W, s and D are the gear's
    teeth, stretch and spring; the grips are the Meshes'.
  - The defect -(a+ - b) . (r+ - r) comes from the gear's fine-tooth notch.
  - The click's work comes from the drive's quotient.
  - The flux is the Mesh's grip read alike from both ends.
  - The order of reads enters only as the synchronous round.
  - All of it follows from the one tensor act, and no term is added.
  - At the 7b gearing the common factor 2 adds one kept bit per fine tooth, and nothing else.
- **(b) What the clicks show, the books first.**
  - The gear's and the drive's carries keep their wholes exactly.
  - The wind at a click's Node-clock changes by exactly its work, its defect and its Meshes' flux, so the beat before
    and after is a reading that can fail.
  - No energy is kept exactly for W >= 2, but the wind with its booked defect is.
- **(c) What does not follow, asked of the clicks.** Each is to be read in the clicks as the wind before and after over
  every train, against the work, the defect and the flux.
  - an exact energy (none exists, by the theorem);
  - a bound uniform in time;
  - the asynchronous wind;
  - the energy books of a cubic coupling.

---

## Question 1: notes and probes for David (input to his items 5 and 6, not a competing derivation)

What the 7a act shows about the take and the books. I spent no more time to settle it.

1. **Where a click's quanta land.** The drive's quotient q = (J + r_d) div T_d of a target row enters only that row,
   through the push s T_k q: the train, kind component and part that the coupling row and the table's non-zero entries
   name, with no list. It is exact by the drive's and the gear's carries (P1).
2. **The take as mirror terms.** A coupling of value operands is the derivative of one A1 invariant
   U = strength x SUM C[c, a, b] z_c x_a y_b. Its take is the derivative of U with respect to the two sources, landing
   on the triples the row already names.
   - On A1, A2, T1 and T2, both mirrors are the engine's own tables, with sign +1 and the operands cycled: (y, z -> x)
     and (z, x -> y). That holds for 24 of the 24 non-zero tables without E.
   - The 19 tables that touch E are not proportional to their permuted forms (E's basis is not orthogonal), so E's take
     needs E's pairing (P4).
3. **The books close in the sweep, not in the count of q.**
   - On hands, the invariant Re(strength conj(Z) (X o Y)) is unchanged by the phase pairs (X, Z) and (Y, Z). The exact
     Noether identity is Im(conj(X) J_X) + Im(conj(Z) J_Z) = 0 at every site.
   - With S_t = SUM Im(conj(a) M):

         T_d d(S_X + S_Z) = T_d (tau_X + tau_Z) + s T_k SUM over X and Z of Im(conj(a) (r_d - r_d+)),

     where tau = SUM Im(conj(a+ - a) r+) is Rule3's torque.
   - So the pairs close bit for bit at W = T_d = 1, and up to the two booked torques otherwise. This is Manley and
     Rowe's relation: one Z for one X and one Y.

   P3 (150 worlds per case):

   | Case | (c2) pairs, with torques | (c3) bit for bit | (c5) q balances |
   | --- | --- | --- | --- |
   | A1, W = T_d = 1, with the take | 616 of 616 | 616 of 616 | 0 of 616 |
   | A1, W 1..6, T_d 2..5, with the take | 806 of 806 | 0 | 0 |
   | T1 cross product, W = T_d = 1, with the take | 603 of 603 | 603 | 0 |
   | T1, W 1..6, T_d 2..5, with the take | 765 of 765 | 0 | 1 |
   | Every case, the lay alone (mutant) | at most 1 | 0 | at most 3 |

   q is negative at nearly every tick.
4. **What this means for item 5.**
   - The take needs no root, no search and no if. A due at or below 0 is just a negative J.
   - It moves action through the dynamics, not one quantum per click: the counts of q do not balance while the action
     does. It does not give "one hand whole". Item 6's slots would have to keep these pairs.
5. **Single gears (part 1)** have no phase pair, so the only books left are the energy's, which no integer step keeps
   exactly (question 4).
6. **Gradient or force operands.**
   - The exact take is a divergence of a product. It reads the other source two Meshes away: P6, offsets -2, 0, +2 for
     Y and -1, +1 for Z.
   - So no coupling row gives it. The coupling would have to be held on the Mesh (a difference across one Mesh, read
     alike from both ends) for the take to stay within one Mesh.
7. **A conversion** is the same act. The table's non-zero entries fix the kinds and components laid. The phase pairs fix
   the counts. The windings balance only at resonance, with the remainders holding the rest.
8. **Conflicts with the record.**
   - The ruling says a whole click has q of at least 1, but the drive's q is signed.
   - The decoder's part_closes adds windings and kept over the part. A conversion from one family to two gives
     -dN_Z there, not 0; its books are per Noether pair.
9. **Draft A against the 7a act.**
   - F3's ladder (refused) is not needed: the take is the mirror rows' own drive carry.
   - A_verify's "Q* kept up to Rule3's torque" agrees with the sweep step above, in its one-sided form.
   - F5's Rule3 quotient at each end carries over as the drive's carry. Its two-end lay waits on the coupling held on the
     Mesh.
   - F1 was not tested.
10. **Probes for question 1:** p3_mirror_books.py, p4_tables_mirror.py and p6_gradient_take.py, with their .txt outputs.
