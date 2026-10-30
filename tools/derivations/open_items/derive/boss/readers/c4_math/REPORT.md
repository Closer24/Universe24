# Term 11's count, the fourth text (COUNT4.md): the fourth reader's report (the hostile mathematician, final pair)

2026-10-30, 17:5x UTC. Read fresh: COUNT4.md whole; probe_canon, probe_flux, probe_x, probe_xring with their outputs
(all four rerun byte for byte, rerun_*.txt here, empty .err); the engine (carry, step, contract, mesh, state, kinds,
load); the harnesses (t11lib, probe2, click.py, w.py, probe_g, probe_h); the earlier reports for reference only.
My own probes (this folder, whole numbers, the engine's carry the one division, no float, root, round or random):
c4_canon_mesh.py, c4_pairing.py, c4_sameact.py, c4_torus.py, c4_keys.py, c4_td.py, c4_planck_w.py, each with its .txt.

## VERDICT on term 11's count: NOT PASSED

## Items

1. BLOCKING. The run back of the click tooth is not the same act on the mirrored state; no act with the text's X is.
   Place: Clock ("the run back is exact by the act alone (M2)"), Algebra "The lemma for an odd increment", law lines 1
   ("the mirror negates X and keeps the click tooth ... the run back is exact") and 4, Method step 6.
   Measurement (c4_sameact.txt, Animate's world, 6,000 rounds, the tooth kept, the run back mirror-act-mirror by ONE act):
   act B (the tooth carried on the state the round reads, X(S)): the gears return 6,000 of 6,000, the TEETH 0;
   act I (carried on the state the round produces, X(S+), the pairing probe_x's forward run uses): teeth 0 of 6,000;
   act S (carried on X(S) + X(S+), the two-round form): teeth 6,000 of 6,000, quotients negated 6,000, forward
   books 0 misses, the taker 0..7. Why: the forward round reads S = (a, b) and produces S+ = (a+, a); the backward
   round reads mirror(S+) = (a, a+), whose passing is -X(S+), and produces mirror(S), whose passing is -X(S). The lemma
   -X + k+ = -q key + k inverts only if the backward increment is minus the forward one; of the increments linear in X
   only X(S) + X(S+) is odd across that swap. probe_x's "6,000 returned" (c4_pairing.txt reproduces it) carries
   forward on the produced state and backward on the read state: two acts, which Postulate 2 ("the same acts in the
   reverse order") and ARCHITECTURE ("the run back is the same act on the mirrored state") do not allow. The lemma is
   exact; "by the act alone" is not.
   Fix: carry the two-round passing X(S) + X(S+) (the physicist's form the text already calls "one form" with X):
   three contractions a round (J(b), J(a), J(a+)) or last round's J kept; the key doubles and is EVEN, so the pair's
   births are K - 1 and K (the parity trade the text lists: the hands told apart, or EDGE's centred split); strike
   "with no next" and "the odd key CHOSEN" or declare the asymmetric act and say Postulate 2 is bent for the record.

2. BLOCKING. The canonical identity and "the exchange is energy" are stated for every board and hold on one.
   Place: The Mesh flux "The canonical reading (N5)" ("per gear ... exactly", "the exact whole-number form of W dD = X
   to Rule3's turn: a hand's X_h is its own energy change"); Clicks "The exchange is energy" (unscoped); "What it
   means" ("two beating hands ... there each hand's X_h is its own energy change").
   Measurement (c4_canon_mesh.txt): on the text's own sea of bobs (light with Meshes, the value vertex) 2 dE_i = X_i +
   v-(r- - r+) misses on light's row at 18,694 of 19,152 gear-rounds (the bobs' row 0); the gap is exactly v-(F(a) +
   F(b)), the pull's work (0 misses); the pull's Wronskian a F(b) - b F(a) is up to 134 times X on light's row and sums
   to 0 over the ring 400 of 400 (a flux: it is the text's own Psi with the grip for G, div Psi_pull). On a moving
   clock (a clock row rising 1 a round read into the teeth, the plan rebuilt) 11,996 misses of 35,988.
   Derived and measured exact (0 misses on both boards): 2 dE' = X + (a F(b) - b F(a)) + v-(r- - r+) + (W_t - W_t-1) v-^2
   with 2 E' = W v+ v- - a (J + F). So a hand's X_h is its own energy change only where it holds no Mesh (the bobs),
   at a standing clock, at s = T_k = T_d = 1; per Node-clock a travelling hand's energy change is X plus the pull's
   flux; the two-beating-hands sentence is false as written on the very world it names (both rows carry grips).
   Fix: scope the identity to that case and give the general form above; in Clicks say "summed over a closed region,
   or at a Node-clock without Meshes"; rewrite the OPEN sentence as "each hand's X_h plus the pull's flux through its
   Meshes is its own energy change".

3. MINOR. T_d above 1: X on J is off in SCALE, not "by the floor's remainder", and the OPEN has a measured road.
   Place: Board "The push, not J alone (M6)"; Open.
   Measurement (c4_td.txt, Animate's world): at (s, T_k, T_d) = (1, 1, 5) SUM X^J / SUM X^kick = 5.000 and the taker
   on X^J runs 0..35 (five keys per real key), on the kick's X 0..7; at (1, 1, 7) 7.000 and 0..49 against 0..7; at
   the cube's (3, 2, 7) 1.166. The kick's X = a kick(t-1) - b kick(t), with last round's kick recovered from the
   state by the drive's own run back (carry(J(b), T_d, T_d - 1 - rd), 0 misses), gives 2 dE = X^kick + v-(r- - r+)
   exactly at every gearing (0 of 71,988; X^J 23,996 misses), its antisymmetry off only by the floor: |X^kick_L +
   X^kick_M| up to 1.5 x 10^7 against a key of 6.6 x 10^28, books 0 misses. Fix: write "T_d / (s T_k) times the wind
   passed" and offer the kick's X as the road.

4. MINOR. Locality allows one Mesh leg per monomial; "a term with several Mesh legs sums theirs" overreaches.
   Place: The Mesh flux, "Every Mesh leg of a term contributes a flux ... a term with several Mesh legs sums theirs".
   Derived: a monomial with two Mesh legs (gradient x gradient, gradient x force, force x force) has a reaction at s
   reading s +- 2, which no Node-clock reads; only value x gradient and value x force are layable as one potential.
   Measured (c4_torus.txt): several AXES of one gradient leg do sum: on a torus 12 x 8 with the engine's own gradient
   reading, X_L + X_M = div_x Phi_x + div_y Phi_y at 19,200 of 19,200 (the x flux alone 64), booked 618/618 with 0 off;
   and a force-leg CROSS vertex g M F_L with its reaction has its flux Xi(s, s+1) = -g G [a_M b_L+ - b_M a_L+ + a_L
   b_M+ - b_L a_M+], 14,400 of 14,400. Fix: "one Mesh leg beside value legs; its flux is summed over the axes it reads".

5. MINOR. Planck's key names W: one key per train is Planck's at the rest teeth alone.
   Place: Clicks "Planck's relation"; law line 3; Open ("the key's value per train ... checked at load").
   Measurement (c4_planck_w.txt): the same action 7 K_a on a circle at teeth W, 2W, 4W counts 0..7, 0..5, 0..4 at the
   card's key and 0..7 at every teeth count with the key cut at those teeth (707 and 500 thousandths of the card's).
   Where the 00 slot differs the relation names another key. Fix: "at the rest teeth" or OPEN with G2 beside the
   moving clock; and the "files' checker verifies the squares" needs its rule (no exact square exists in general:
   state the half-step tolerance by two carries); load.py today has no key, no card and no checker.

6. MINOR. "Under the 24 on a moving clock" is measured under the half-tooth act, not the engine's.
   Place: Board "Under the 24"; Measured 11. probe_xring (c) runs H.forward_h; the engine's act as built fails the
   24 on a rising clock from round 1 (NOTES: built [24, 3, 3, 3]). Disclosed in parentheses; say it in the claim.

7. MINOR. "Two contractions a round, read from now and before alone, with no next" (Board; Algebra) describes X as
   a function of a state, not the round's carry: under item 1's fix the round reads three slots (b, a, a+) or keeps J;
   N6's before-slot read across the Mesh gains the new now's read. Fold into item 1.

## Sound, with numbers
- X_L + X_M = 0 for a quadratic one-potential vertex with its legs at the Node-clock: exact (symmetric K against the
  antisymmetric a_i b_j - b_i a_j); probe_x 0 misses on every lay, rerun byte for byte.
- The Mesh flux: Phi's eight products and Psi re-derived by hand, exact; extended here to two axes (19,200 of 19,200)
  and to the force-leg cross vertex (14,400 of 14,400); the booking a declaration, as the text says.
- The pair's invariant: q_L + q_M = 0 for ANY key once k_L + k_M = key - 1 (floor(u/key) + floor((key-1-u)/key) = 0),
  and key - 1 is the only closing sum (c4_keys: keys 2..13, every C, every increment); the even key with births
  key/2 - 1 and key/2: 0 misses of 6,000 on the text's increments; three hands within [-1, 1] by the teeth's sum
  (6,000 of 6,000). No parity enters the pair's books; the odd key is a choice, rightly marked CHOSEN.
- The lemma -X + k+ = -q key + k: exact; the tooth kept (item 1 is about the act, not the lemma).
- The kick's energy form 2 dE = X^kick + v-(r- - r+): 0 of 71,988 at four gearings (item 3's road).
- The general energy form with the pull's flux and the moving clock's term: 0 misses on the ring (19,152 x 2) and
  on the rising clock (35,988).
- Planck's relation in whole numbers at the rest teeth: the taker 0..7 at W with the card's key (and at 2W, 4W with
  the local key).

## Solution24
A new dial's run back is checked as the same act on the mirrored state, and an identity measured on one world is
scoped to that world's push until the act's general form is written.
