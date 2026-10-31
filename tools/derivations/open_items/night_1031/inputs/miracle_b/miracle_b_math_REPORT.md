# MIRACLE_B, read by the hostile mathematician (2026-10-31)

(Written by the Boss from the reader's hand-back at 08:4x UTC, the reader's harness refusing the write; the text below
is the reader's, word for word.)

My harness refuses report files from me, as before, so the whole report is here. The text is S/miracle_b_frozen/MIRACLE_B.md (628 lines, sha256 0e034a761f86d016...); all 81 sums in FROZEN.sha256 check. I reran from my copy at S/miracle_b_math/copy, with S/live/.venv/bin/python -I, nice -n 19, one process at a time. Every run was gated on load below 8; the start loads were 6.82 to 7.95 (chain.log).

## VERDICT on MIRACLE_B: PASSED

There is no BLOCKING item. As board clock facts, B-edge has:
- an exact, time-symmetric step with the gears as they are and no new state;
- acyclic reads, with each edge's dial its own;
- the run back by the engine's mirror;
- the 24 alike.

Three more results hold:
- The energy identity is exact. I derived it independently, and it holds in every round rerun.
- The lemma's proof is sound.
- HAT4's unqualified claim is refuted by counterexample.

The energy is not kept in whole numbers, and the text says so. Its books are checks by construction and must be named that way (MINOR 1, a condition before they are cited).

## MINOR

**1. The identity and the books are checks by construction on B-edge.** They must be named so under the Boss's 08:1x books ruling. Places: 4.4's last paragraph ("The reading that can fail is the first column"); 4.1 and 4.3 ("MEASURED to the unit in every round"); the verdict's energy bullets.
- Derivation (mine, by hand). Each row's split, 2 d_out (a+ - a) + s+ = 2 d_in (a - b) + 4 push + s, gives the held equation 4W (h+ - 2h + h-) + 2 g_out (h+ + h) + 2 g_in (h + h-) = s - s+.
  - Hence 4p - 4p' = s - s+, with p = W (h+ - h) + g_out (h + h+)/2 and p' = W (h - h-) - g_in (h- + h)/2.
  - E_H = p^2/(2W) + g h^2 at one end and p'^2/(2W) + g h'^2 at the other.
  - So 32W dE_H = (s - s+)(4W (h+ - h-) + 2 g_out (h + h+) - 2 g_in (h- + h)) + 32W (g_out - g_in) h^2.
  - The last term cancels the tied rows' work, -f k_n^2 o_n (o+ - o-), because T reads the held now slot.
  - The hands' tie gives (f/4)(C(b, a) + C(a, a+)) to each leg.
  - So both the identity and "each clock's change = booked + teeth's share" hold on every state, by algebra.
- "0 misses" therefore checks the code against the derivation, which is itself worth having: it would catch a moving W or a monomial of another kind. But it cannot fail on a correct build.
- The share is read, not fitted: predicted() (b_edge.py:171-176) is a fixed formula in (s, s+) and the counts, compared at :329 with E32 (:154), which is computed from the state alone.
- The identity books the change and bounds nothing.
  - Pair world: E32 runs from 3.75 10^14 to 2.58 10^16, against 4.94 10^14 at the lay.
  - Click world: from 1.18 10^20 to 6.81 10^22. One Node-clock reaches 2.52 10^21, from 4.38 10^18 (my rerun).
- Fix: name both checks by construction. Give the ruled reading that can fail, each clock's stored share of the coupling's energy within its teeth, or name it OWED.

**2. MIRACLE_A's Theorem A, step (3), names "road B's edge dial" among its dials** (MIRACLE_A.md 3.2). So section 4.2's OPEN, the coupled round's written proof, is that theorem's claim under (D) and (H).
- Fix: cite it as the candidate, with nothing leaning on it until its pair reads it (the Boss, 08:1x).
- The two agree: no energy is kept exactly in whole numbers. B-edge's heating is what Theorem A predicts.

**3. 4.2's coverage overreaches.** "A tied row at the lay is one [a slow gear alone] ... no polynomial of degree below about 70 is kept" is not supported.
- The lemma is for one uncoupled gear, n = 2D (a - b) + s - 4 kappa a, with a polynomial in that gear's (a, b, s).
- A tied row is coupled: to the other tied row through the hands' tie, to the held hand through the tie, and to its neighbours. Its "2 c |k|^2 + tie" mixes a self-curvature with a cross coupling.
- Fix: the tied row is the coupled case, OPEN (or Theorem A's).

**4. The probe classifies by the as-laid factor, which is case (c), ruled not lawful at 08:1x.**
- Places: b_edge.py:58-60 (`if int(f) == 0: continue`) and :95-97 (GPLAN from `int(f) != 0`).
- The act's function is unchanged, since a factor-0 monomial adds 0 to g and to J_g.
- But the kinds' assertions then cover only the files' chosen strengths. A build must read the structure, with every chosen strength at 1.
- At those strengths the click world turns on the push and the gradient vertex, which section 7 already names OPEN.
- Fix: say so for the writer.

**5. W's constancy is an unnamed hypothesis of 3.4 and 4.1.**
- E32's derivation takes one W for every row and both slots, that is, the clocks' read landing nothing.
- b_edge.py asserts the teeth at rest at the lay alone (:280). The identity's check would catch a move later.
- On these worlds the 00 row stays at rest (push, notch and mesh 0).
- Fix: name it among section 7's limits.

**6. The no-selection (uniform) form is MEASURED on the pair world alone** (rec/pair_uniform.txt).
- The click world's 5,000 rounds, the square-2 lay and the late probe ran the selecting probe form, bedge(), which masks: a1[H], s1[H] = h1[H], hs[H].
- The two forms are one function by the plan (g = 0 and J_g = 0 off the held rows), DERIVED.
- Fix: say which form each run used.

**7. The family split is a structural rule, and that should be said in 3.1.** The rule is: the Mesh-less train's rows take their own square's coefficient in the dial. It is not "every row held twice", since the tie also holds each tied row twice. A world with two coupled Mesh-less trains would need its own reading.

## SOUND

**The algebra:**
- My derivations of 3.4 and 4.1 agree with the text: the held equation; E_H's two readings; the cancellation of the tie's work between the families; the leapfrog's polarized energy for the hands' tie and the Meshes. E32 is whole.

**The lemma (4.2), checked step by step:**
- The strip reading is right: q(M) = a - b for s in [-D, D).
- (1): the grid holds more than m by more than m points, since D/(4 kappa) >= 2(m + 1).
- (2): M - 4 kappa a lies within [2Dj + D, 2Dj + 11D/4), inside strip j + 1.
- (3): this gives invariance along (1, 0, -2D) on all of Z^3, so E = G(b, M).
- (4): G(a - j, M) = G(a, M - 4 kappa a) for every j, so G is constant.
- It is sound as stated, for one gear.

**The HAT4 refutation:**
- HAT4.md:28-30 is unqualified: "three properties cannot all be had at once for two coupled families".
- B-edge has all three: exact run back by the same act, edge-own dials, acyclic reads. Its uniform form is byte for byte the selecting form on the pair world.
- So the claim is refuted. The text names the true condition: both families' dials carrying the curvature.

**The other texts:**
- ALG1 (3.4) is consistent. On the engine's step the four-leg tie's residual cannot telescope (d >= 3); only a change of the push can make it an exact difference. B-edge is that change, and 4.4's exchanges are exact.
- MIRACLE_A is consistent (MINOR 2).

**The act's kind:**
- The uniform form has no if, mask, loop, bound or book.
- Rule3's carry is the one division.
- No number is typed: the push's two terms are the monomial's two held legs, and senses comes from the star.
- It is local.
- It is acyclic: T reads the held now slot only, and H reads T's before, now and next counts, which are already given.
- Each dial is the edge's own: g is symmetric per monomial (asserted), and round n's out-dial is round n+1's in-dial.
- The stagger's algebra holds: M_s = M after P is an involution and conjugates QP to its inverse.

**Reruns:**
- Pair world, with the text's own command: byte-identical to rec/pair_1.txt.
  - The identity holds in 1,260 of 1,260 rounds, and the run back is exact.
  - The 24 are alike in 24 of 24 turns over 100 rounds, and the twin's board is alike.
  - Clicks are [523, 3879, 3838].
- Uniform form: byte-identical to rec/pair_uniform.txt and to pair_1.
- Pair books: the same lines as rec/pair_books_1.txt (0 of 3,780 clock-rounds missed; 225 keys).
- Click1, 5,000 rounds with books: every key line identical to rec/click1_1.txt.
  - The identity holds in 5,000 of 5,000 rounds, the books miss 0 of 25,000 clock-rounds, and the run back is exact.
  - Clicks are [0, 0, 133537, 242112, 281280], 27 times the click world's figures exactly.
  - The smallest held dial is 1,299,940,000 (541 per mille of 4W) at round 1405.
- The late pair trace: at round 1903 the out-dial is -2,852,000, the held count jumps to 502, and the tied curvature reaches 3.0 10^9 against 4W = 2.4 10^7, as recorded.
- I did not rerun the full 27-site click world (38 minutes). It is DERIVED from click1 by the lay's homogeneity and recorded twice alike.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED, sound:**
  - the edge's rule and the centering lemma;
  - B-edge acyclic, with edge-own dials, the run back and the 24;
  - E32 kept when nothing rounds;
  - the whole-number identity;
  - the lemma for one gear;
  - each monomial's exchange exact.
- **MEASURED, reproduced by me:** pair (identity, run back, 24, twin, books); the uniform form; click1 (identity, books, run back, dial); the fall at round 1903.
- **OVERCLAIMED:**
  - 4.4's "the reading that can fail" (MINOR 1);
  - "MEASURED to the unit" presented without "by construction" (MINOR 1);
  - the lemma applied to a coupled tied row (MINOR 3).

## Questions for the Boss

1. On B-edge, are the identity and the per-clock books named checks by construction, with each clock's stored share within its teeth OWED before the books are cited?
2. Does road B close the owner's question D as "an exact, time-symmetric step that keeps the gears as they are, with exact books and no exactly kept energy in whole numbers", pending MIRACLE_A's pair?

## Solution24

Road B gives Solution24 the coupled families' step in the gears as they are: exact run back, acyclic reads, edge-own dials and no new state. It survives both shipped worlds where the engine falls. It books the energy exactly but keeps none in whole numbers, as the lemma and Theorem A say no such step can.

## Files

Everything is in S/miracle_b_math:
- chain.sh and chain.log;
- pair_r.txt, pair_uniform_r.txt and pair_books_r.txt;
- click1_r.txt and click1_dial_r.txt;
- trace_r.txt;
- copy/.
