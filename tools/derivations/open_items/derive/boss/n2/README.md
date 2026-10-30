# N2: the metric's push reads the matter's rate, and the round still runs back

A draft for David's reading (term 5, G2), on the owner's word of 2026-10-30, 08:4x UTC: what is missing is derived as a
solution, by the clock, the algebra and the physics. Whole numbers only: Python integers in numpy object arrays,
addition, multiplication and Rule3's carry; the varied lays from an integer carry sequence, no random.

Run: `uv run python -I n2_probe.py <src of tensor24-review at ed745f7cc>` and the same for `n2_probe_extra.py`; their
outputs are `n2_results.txt` and `n2_results_extra.txt`, each equal on a rerun.

## The question

The node's term 5 pushes each slot of the metric family by its component of 2T + 2 eta V, T built from each family's
four-vector (the stride a - b and the gradient). A push that reads the stride breaks the act's run back as built: the
mirrored tick reads a - a+ where the forward tick read a - b. The node's page (4.1) asked for the first-order form, each
rate in its own slot, with the run back exact while the clock moves.

## 1. In clocks

- A gear's rate is the stride between its slots. Around the now there are two strides: the one in (a - b) and the one
  out (a+ - a), taken this round.
- Running back swaps in and out and turns their sign. The now, and its gradient through the Meshes, is the pivot.
- A push that reads only the stride in sees another number when mirrored. A push that reads both alike sees the same
  number either way: both slots are needed.
- No message and no queue: at one Node-clock the matter's gear carries first, reading the now slot alone, and the
  metric's gear beside it reads that carry's quotient. No neighbour's stride out is read, so the reach stays one Mesh.
- A gear that read its own stride out would be pushed by the motion it is deciding: the metric's self-push of its own
  rate stays out.

## 2. In algebra: the first-order form

The rate gets its own slot, p = W (a - b) + r, the act's own dividend. The state is (a, p, r_d), and W = the rest + the
clock's read of a, as built.

- **Pass 1:** J1 = the plan on the now slot (a, its gradient, the pull F); q1 = the quotient of carry(J1, T_d, r_d);
  sigma_b = p div W, the stride in; sigma_a = (p + s (F + T_k q1)) div W, the stride out.
- **Pass 2:** J = J1 + the plan on the matter's strides (sigma_b, sigma_a, the gradient); q_d, r_d+ = carry(J, T_d,
  r_d); p+ = p + s (F + T_k q_d); a+ = a + p+ div W.
- **Term 5:** S + 2 eta V, with S the sum through C[K x K -> A1] of v_b (x) v_b + v_a (x) v_a, v_b = (sigma_b, the
  gradient) and v_a = (sigma_a, the gradient): the 00 slot the sum of sigma_b^2 + sigma_a^2, each 0i slot the sum of
  (sigma_b + sigma_a) times the gradient along i, each ij slot twice the sum of the two gradients' product. The plan on
  the strides reads the matter's strides alone.
- **The mirror, R = R_P after the drift undone:** the 00 row's teeth at rest, so the 00 row comes back first, then W,
  then every row. R_P maps an even row's (p, r_d) to (W - 1 - p, T_d - 1 - r_d) and an odd row's a to -a. The parity is
  the reversal's: it turns the four-vector's stride and not its differences, so the 0i slots are odd and the rest even.
  The run back is R, then the tick, then R.

**Proof sketch.**

1. The tick is a drift D after a shear K: K is triangular in p and D triangular in a (W reads the 00 row alone). So R,
   then the tick, then R, is R_P, then K, then R_P, after D undone.
2. R_P leaves an even row's push as it is and negates an odd row's. On an even row, (W - 1 - p) + push = W - 1 - (p -
   push), and the drive's flipped tooth gives the same quotient.
3. As (W - 1 - p) div W = -(p div W), the strides map (sigma_b, sigma_a) to (-sigma_a, -sigma_b), and S to its turned
   self.
4. So R_P, K, R_P is K's inverse at any W of at least 1, rising or falling, and no tooth is read at another round's
   teeth.

**Verdicts.**

- (ii), T even in the stride read at the now slot, **fails**: (a - b)^2 departs at the first round back. Evenness
  cancels the sign, not the swap of in and out.
- (i), a staged round in the act's present form with a parity mirror, is exact at a standing clock and needs no
  palindrome, since the matter reads the now slot alone; it keeps G1's limit, and term 5 moves the clock.
- (iii), the first-order form, equals (i) bit for bit at a standing clock and stays exact while the clock moves. It also
  restores the term G1 drops, (d_t W)(d_t a): d_t (W d_t a) = F.
- **The self-push of the metric's rate stays out:** its stride in is (ii), and its stride out is implicit. The 00 row
  reading itself as teeth is no bijection: at rest 3000 with p = 15000, counts 0 and 1 both drift to 5.
- **What stays in, exact:** the metric's own gradient (D g D g onto the ii and jk slots), the grips, and other slots'
  teeth reading the 00 slot.
- **The cost to Postulate 6:** none for sources at rest, where the metric's rate is 0; what is lost is the metric's own
  swing as a source.

## 3. In physics

- T is the mean of the two half-rounds around the now; the 2 of 2T is the two slots.
- rho is at or above 0 at every round: at a turning point (+1, then -1) the 00 slot gets 2, where the product form
  would give -2.
- The 0i slots are the momentum's density, odd under the mirror as the shift is.
- With 4 rho = J00 + 3 Jii and 4 p = J00 - Jii, a uniform swing at stride 7 with no spring gives the 00 slot 98 and each
  diagonal slot 0, for an A1 gear and a T1 gear alike: rho = p = 49 / 2, as N3 says.

## The probes (n2_results.txt, n2_results_extra.txt)

The 3 x 4 x 5 board, T1, E and A1 matter beside the metric family's ten slots; lays from an integer carry sequence.

| Check | Result |
|---|---|
| The probe's harness against the head's step.tick | equal |
| S under the 24 turns | covariant on all 24 |
| (i) at a standing clock | exact, 300 rounds at each of 4 lays |
| The uniform mirror, with no parity | departs on the 0i rows |
| (iii) with the clock moving | exact over 300 rounds at 4 lays and 800 rounds at 1 (23,856 site-rounds rising, 23,798 falling) |
| The head's form, and the head's own act with no term 5, the clock moving | departs at once |
| Locality | one Mesh |

## What stays OPEN

- The strengths per slot (D reads twice the difference, and c^2 = the grip over W).
- The 00 row's teeth at rest changes the loader.
- The matter's parity: the click's swept area is odd (G5).
- Postulate 6's cross-term form.
- A second-order W at the half round.
- In code: the second slot becomes p, and the promise becomes W at least 1.
