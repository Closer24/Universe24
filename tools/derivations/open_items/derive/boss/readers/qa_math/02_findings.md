# Findings on ONE_ALGEBRA.md (running; numbers from qa2..qa6 .txt and rerun/)

## Reruns of the text's probes (rerun/)
- probe, probe_units, probe_time, probe_square, probe_ring, probe_books, probe_carry, probe_carry_big: byte-identical.
- probe_double.py: CRASHES (TypeError: turned_edge() missing 'wd'): edge/edge_lib.py was rewritten at 16:33:19, after
  probe_double.txt (16:29). With the one-argument patch (rerun/probe_double_fixed.py) the output is byte-identical to
  the stored one. MINOR (hygiene): the measurement stands, the probe as filed does not run.

## Item A (BLOCKING): the "iff gcd(W, 6) = 1" holds only for a remainder set that is one fundamental domain for
## every quotient; the text says that is "what makes the act bijective and the run back a mirror", which is false.
- The theorem's framework: "r in a set D of coset representatives of L / W L (a fundamental domain)". Within it the
  proof is right (qa3: fixed cosets exactly where 2 | W or 3 | W, on H by brute force W = 1..13 and Smith up to
  1002, on Lambda by brute force at W = 2, 3 and Smith elsewhere; indices 16, 9, 4, 1 and 256, 81, 16, 1, 4).
- Outside it: the orbit-canonical quotient Q(u) = conj(g) [centred box quotient of g u], g u the least of the 24
  images (free action on H \ 0, so g is unique): Q(g u) = g Q(u) (0 misses of 1440 at each of W = 2, 3, 5, 6, 7, 9),
  Q(-u) = -Q(u), bounded remainder. States valid iff Q(W (a - b) + r) = a - b (the tooth is its own remainder, as
  the edge form's |s| = D only at an even velocity). Then the state map is a bijection on valid states, the mirror
  (b, a, -r) inverts it, and every lift commutes. ON THE ACT (worlds/spin4, a lone Node-clock, J = -2 psi): 480 of
  480 lifts x starts and the run back 20 of 20 at W = 2, 3, 5, 6, 7, 9 alike (centred rule; the tooth moves in 18-20 of 20
  runs; the act as built 40 of 480, 53 at W = 2); on Lambda (worlds/spin8) 240 of 240 and 5 of 5 at W = 2, 9.
  Remainders: 4 N(r) at most 12, 12, 56, 116, 116, 224 over the cell of 0 against 4 N(W) = 16, 36, 100, 144, 196, 324;
  the cell of 0 at W = 2 holds 73 dividends and the 15 fixed cosets carry two or more remainders each.
- The project's own edge form is of this kind in rank 1: edge_lib.split at dial 2D has cells of sizes 2D - 1,
  2D + 1 by the quotient's parity (D = 3: sizes 3, 5, 7 seen; D = 4: 4, 7, 9) and the class D mod 2D, fixed by -1,
  carries two remainders +-D. So the framework the theorem needs excludes the Boss's own draft.
- What survives: "no fundamental domain (one dial of W^4 teeth, the same at every velocity) turns with the lifts at
  gcd(W, 6) > 1" (DERIVED, right); "no per-gear carry in any basis" (right, fam_math); (c) a formula free of a table
  or comparison: OPEN at EVERY W (the canonical rule compares 24 images; the orbit domain is a table).
- Fix: state the hypothesis in the theorem and in Answer 1 and the Clock layer ("a dial of W teeth per gear ... the
  same dial at every count of the velocity"); strike "that is what makes the act bijective"; add that
  quotient-dependent remainder sets (the edge's kind) give an equivariant bijective mirrored carry at every W, by a
  table or a comparison; retire the "wall at the load's teeth" sentences in Answer 1, Board and Clicks, or restate
  them for fixed dials.

## Item B (MINOR, a false reason): "the group ring escapes the wall (it has fixed vectors, the orbit sums)".
- qa5: L(-1) = -I and R(-1) = -I on the 24-gear train; SUM_g L(g) = 0; a common fixed vector is 0. No fixed
  vectors, no orbit sums. |det(L(g) - I)| = 256 for the order-6 lifts (not 1): the H^1 = 0 argument does not run;
  the flip twist c_g = (W - 1)[negated rows] is a cocycle (0 misses of 576) and a coboundary iff W odd (48 a = -192
  at W = 9 whole; -216 at W = 10 not). The train rides the per-gear carry because its lifts are monomial (the
  carry's lemma). Fix: replace the parenthesis by "its lifts are signed permutations there, and the flip twist is a
  cocycle the H^1 argument does not kill (g - 1 is no unit on the train)".

## Item C (MINOR, scope): "the slot quaternion's unit step is the lone clock's or the uniform hand's".
- qa4: a cube of side 3, the light hand an eigen-hand of the pull (patterns (2, -1, -1), (0, 1, -1) along x), the
  spring k = 2 W - 3 grip = 3 W / 2: F != 0 and q+ = q j at all 27 sites for 12 rounds, N(q) kept, teeth still; the
  same hand at k = 2 W fails. Even boards (sides 2 and 4), the checkerboard hand, NO spring: q+ = q j 12 rounds at
  every site. Fix: "q+ = q j wherever the round's push is -2 W now: k + s lambda grip = 2 W for an eigen-hand of
  the pull of eigenvalue -lambda; the lone clock and the uniform hand are the case lambda = 0".

## Item D (MINOR, overclaim of weight): "the double Node-clock IS Hamilton's quaternion of the slots".
- Every identity (i q, (i q i^-1) j, q (1 - j)) holds at every mode; the phase commutes with the act as built with
  the flip at k = W, 2 W, 3 W alike (12 of 12 each, qa4). What is the quarter mode's is only S_0 = right
  multiplication by j and N(q) kept; and at every exact mode the carry is inert (q exact, r still), so the quaternion
  reading touches none of the act's one non-trivial operation. Strengthening the text: for t = +-1 the step is a unit
  quaternion's right multiplication in NO whole basis of the slots (the rational invariant form has Gram determinant
  3/4; 0 of 1184 small GL_2(Z[i]) bases, against 32 at t = 0). Answer 0 says "the velocity" for the j slot of
  q (1 - j); it is before - now, the velocity negated (the body says so).

## Item E (MINOR, numbers that are not invariants): -48, -16, -128.
- qa6: the ten forms' determinant is -48 with Im(h h) = 2 a v and -6 with a v; the invariant content is rank 5
  (Smith diagonal [1,1,1,1,1,1,2,2,2,6]). The -128 is an index (Smith [1,1,1,1,2,2,2,2,2,4]): the inverse needs
  denominators dividing 4, "halves and quarters" right.

## Item F (MINOR, wording): "bijective division with remainder" (the state map is the bijection; (n, r) -> (q, r')
## is |D| to 1); "a determinant W'/W" of a non-linear map; the theorem's implicit hypothesis that the tooth turns
## by a map of the tooth alone.

## SOUND (my numbers)
- Finding 3: from the quaternion side, 24 Hurwitz units + 24 norm-2 Lipschitz give exactly the engine's 24, two to a
  turn (g, -g), every sandwich / N(g) whole, det 1, N(g) = 1 iff A2 = +1 on 24 of 24; the kinds 1 + 3 + 8 and 6 + 6.
- Finding 2: tables entry by entry: C[T1 T1 -> A1] = delta, C[T1 T1 -> T1] = the Levi-Civita symbol (eps[0,1,2] = 1),
  A1 channels 1; e_a e_b = -delta + sum eps e_x on 9 of 9 pairs; -> E and -> T2 outside (6 entries each).
- Finding 1 within its framework: fixed cosets as above; orbit domains at W = 5 and 7 (625 and 2401 reps, invariant,
  symmetric, (W^4 - 1)/24 = 26 and 100 orbits); conflicts 97 and 64 at W = 6 and 9.
- Finding 5: time plane orders 6, 4, 3 at t = 1, 0, -1 and the kept form; metric ranks; O_48's double farthest point
  256 against 256 and the half 128 (two quotients recomputed in halves); Hurwitz's two quotients at n = 1, W = 2.
- The 24-gear train: SUM tr^2 = 1152, SUM tr(L L) = -384, pi of rank 8 (det pi pi^T = 104976), onto O_48.
- The identities W (a+ - 2 a + b) = push + r - r+ and W p' = W' (p + push + r - r+) (0 misses, W rising 60 -> 66).
- The lone clock at k = 2 W, W, 3 W and 2 W + 2 on the act as built: as the text says (qa4).
