# Hand R5: the fifth act at a single-Node top under the ride, locally (2026-10-25, blind derivation on engine-5.0-test at 7dc781bc2)

Worktree: scratchpad/hands/r5 (branch hand-r5). The flagged engine I started from is R4's tools/derivations/open_items/r4/variant_src.diff (450 lines, against R3's 526). It applied clean on 7dc781bc2 with `git apply` and keeps its values U24_RIDES=1 and 2. My mend sits behind the same flag at the value 3: R4's value 2 (form A, the two mends, the strict reverse order) plus the fifth act's backward trigger read from the forward act on the swapped state. Off, the branch's path is bit for bit (3.6). Scripts are under tools/derivations/r5/ with their outputs beside them. Nothing pushed. Of other hands I read only the landed files under tools/derivations/open_items (R_COMPARISON.md, r3/REPORT.md, r4/REPORT.md and the two diffs). Every number below is an integer reading of a script; no script uses a float.

## 1. The derivation, from the law's clauses by name

**1.1 When the fifth act is a bijection (The swap at the top; The Node: "every one a bijection", "backward the same acts in the reverse order"; The direction).**

Notation:
- S is the pre-state, F the interval's acts before the fifth, tau the swap with every remainder complemented at its wall.
- A is the set of states where the trigger fires. The interval's map is Phi = tau on A and F off A.

Since tau and F are bijections, Phi is a bijection iff tau(A) and F(A^c) partition the states, that is, iff F(A^c) = tau(A^c). That holds iff the trigger set is invariant under M = tau o F:

  T(S) = T(tau F S) for every S.

Under the branch, Rule3's identity on the carried division gives G = tau F tau (G the inverse; the ones' complement commutes with the floor, The cube's symmetry (1)). So M is an involution and F(tau F S) = tau S. The triple's trigger reads (X0, X1, X2) at S and (X2, X1, X0) at M S. It is symmetric in its outer two, hence M-invariant, and the fifth act is a bijection.

Measured as a reversal error delta = X2' - X0, with X2' the volume's step of the swapped post-state (the candidate's own step):
- delta = 0 at 1,985 of 1,985 non-turned Node-intervals on the open standing board;
- delta = 0 at 1,419 of 1,419 on the closed standing board (tools/derivations/r5/twin.py, flag 0, the control).

**1.2 Under the ride, M is no involution, and the interval has twins (The line rides the volume in form A; The conserved form).**

Two terms break G = tau F tau.

(i) The riding remainder's directional wall. A remainder is born in [0, w X_k) and read back in [0, w X_{k-1}). Solving the riding line at the swapped state leaves the velocity terms w (X1 - X2) v_out + w (X1 - X0) v_in in the remainder's equation. These vanish only where X0 = X1 = X2. The mean-wall complement makes the swap an involution, but it does not make M one.

(ii) Form A's remainder term. w F = w^2 D - w next (r' - r) is not even under next <-> before. So the write's source at the swapped state differs from the forward's even at a resting volume, by about (next - before)(r' - r) / w units of D.

So T(M S) != T(S) wherever the reversal error delta (or its backward twin epsilon) exceeds the volume's own step. Two kinds of twin follow, each two legitimate pre-states with one post-state:

- **The false top.** The truth is unturned with X0 > X1 >= X2, and the swapped candidate's step reads X2' <= X1. The integer condition is delta <= -(X0 - X1) < 0 with X2 <= X1: a slow fall of the volume, by no more than |delta| levels, followed by a fall. Both the true pre-state G(Z) and the candidate tau Z step to Z.
- **The missed top.** The truth is turned (X0 <= X1 >= X2), and the engine's inverse of the swapped state reads Y.before > X1. The integer condition is epsilon > X1 - X2. Both the true pre-state and the unturned twin G(Z) step to Z.

A twin is a non-injectivity of the forward interval. The two pre-states differ at one Node, in its levels before and its remainders only. Every neighbour reads that Node's level now, which is the same in both (The interval's dependency radius is one Link). So no reading of the post-state, local or not, can return both. **The run back exact fails at a twin by a theorem, under any trigger reading.**

Measured (twin.py):
- At each of the 4 mismatches met under the two readings, the wrong pre-state stepped forward gives the true post-state bit for bit (0 unequal entries).
- The open board under the local trigger: interval 4, the centre, X0 1,027, X1 1,026, X2 1,000, X2' 1,025.
- The open board under the former reading: interval 18, the centre, X0 972, X1 1,184 (R4's 62 of 80).
- The closed standing board under the local trigger: intervals 4 and 12 (at 12, X0 1,081, X1 1,079, X2 947, X2' 1,079).

**1.3 The local mend, part (a) (R4's first option).**

The backward trigger is the forward act on the swapped state. The candidate pre-state at every Node is tau Z: the post-state swapped and complemented, with its phase rows by the swap's inverse image and the phase act back. The board's own forward acts run on a scratch copy up to the fifth act, and a Node turns back where that forward act turns it, that is, where the forward act reproduces the post-state there.

- **Exact at every turned Node.** There tau Z is the true pre-state, and the candidate's neighbours' levels now are the post-state's levels before, which equal the true pre-state's levels now for a turned and an unturned neighbour alike. So the candidate's step is the true discarded step. Measured: 0 misses over 608 turned Node-intervals on the four boards.
- **Wrong exactly at the false tops** (1.2), which the former reading got right. The former reading is wrong exactly at the missed tops, which this mend gets right. Neither is exact; each fails on one side of the twins.
- **Frequency, from the integers.** A false top needs delta < 0 with 0 < X0 - X1 <= -delta and X2 <= X1. Measured, delta < 0 at: 35 of 1,985 Node-intervals (open), 17 of 1,369 (closed standing), 6 of 1,497 (hole), 27 of 2,133 (sea). The full condition is met at 1, 2, 0 and 0 of them, exactly the false tops found.
- **Size of delta.** It is the ride's asymmetry times the write's gain at the Node. Measured |delta| at most 133 (open), 10 (closed standing), 54 (hole), 1 (sea). It is large where the standing wave's antinode writes the volume by tens to hundreds of levels per interval.
- **Locality**, shown both ways:
  - On the code: the mask at a Node is the forward trigger on its own candidate, which reads that candidate and its six neighbours' levels now (the post-state's levels before).
  - By measurement (locality.py): changing the post-state by +1 on the light's and the volume's two levels at a Node two Links from the centre changed the centre's inverse at 0 of 80 intervals; the centre was turned back at 13 of them. The one-Link control changed it at 67 of 80.

**1.4 A wall symmetric in the Node's two levels, part (b).**

*The theorem.* For the swap's identity by construction, a remainder's range must be the same forward and back. The output's wall at S must equal the input's wall at tau F S, so it must be a function of (X_k, X_{k+1}) read the same from both ends. The light's step at interval k then needs X_{k+1}. While the volume's write reads the light's levels after the division (the branch's D, form A), the volume can step only after the light's division forward, or the light's inverse only after the volume's backward: a cycle in one direction. The candidates the brief names fail as follows:
- the mean wall used for the remainder itself: needs X_{k+1} (the cycle);
- the geometric form: no integer;
- the remainder as a fraction of its own wall: a rescale, not a bijection (R3, R4: 4,894 of 20,000 wrong).

*The form that exists (derived; not in the engine).* The write must not read the light's level after the division. It can read the division's **numerator**, which is known before the wall is needed:

- The light's momentum lives on the half interval with the wall W = (w div 2)(X_before + X_now): R3's mean wall made the remainder's own wall. Its centred value is P_c = W (a_now - a_before) + r - W div 2.
- The kick is P_c_out = P_c_in + X_now [SUM_j R_ij (m_j - a_now) - D a_now], with no division.
- The volume's write is sourced by u_in u_out + [a_now SUM_j R_ij (a_now - m_j)] div w, the potential's part from the levels now. Here u = round(Q / (2 w X_now)) with Q = 2 P_c + 1. Q is odd and 2 w X_now even, so the quotient is never a half and the rounding to the nearest is exactly odd: the odd rounding derived as the carry's mirror, not declared.
- The volume then steps by its one division.
- The light divides once at W_out = (w div 2)(X_now + X_next), the remainder kept in [0, W_out).
- Backward, the same in the reverse order: the numerator from the post-state at W_out, the kick back, the same source, the volume back (X_before returns), then the division at W_in.

Neither direction has a cycle, and every line keeps one carried division. Under tau, Q_in -> -Q_out and Q_out -> -Q_in, so the product u_in u_out is invariant. Written out, F(tau F S) = tau S at every Node, so M is an involution and the triple's trigger is M-invariant: no false top and no missed top, by construction.

Measured on the ring toy (symmetric_ride.py, 12 Nodes, w = 24,504, E = 65,536):
- The step's bijection: 1,666 of 1,666 random boards, in both forms.
- M an involution: 1,666 of 1,666 boards in the symmetric form, 0 of 1,666 in R4's form.
- Runs of 300 intervals with the fifth act: in the symmetric form, 0 misses and 0 false tops in every one of 8 runs (gains 1 and 30, amplitudes 300 to 1,200), per step 300 of 300 under both readings. In R4's form: 0 to 4 misses under the former reading (2, 4, 0, 0 at gain 1 and amplitudes 600, 750, 900, 1,200; 2 and 2 at gain 30), and 4 to 20 false tops under the local trigger (4, 20, 12, 13; 5, 9; per step 289 to 297 of 300), in the runs where the toy's volume runs away. At gain 1 and amplitude 300 or 450 (volume within 523 to 1,616) R4's form met no twin in 300 intervals; the symmetric form at gain 1 and amplitude 300 (volume within 647 to 1,640) met none either.

Named:
- The toy's volume coupling is not the engine's. At the larger amplitudes the toy's volume runs away under both forms, to 122 and 1,055 bits in the symmetric form at amplitudes 450 and 900. The 128 bits are not held by the toy there.
- At the engine's integers: P about w X v is 76 bits (w 41 bits, X 25, v 10), W about 66 bits, u_in u_out about 20 bits.
- The form changes the interval's order (the lines' numerators, the held write, the volume's step, then the lines' divisions) and the write's source (from form A's levels to the momenta). That is the owner's word, and the form is not built in the engine.

**1.5 The standing wave's count at the top, and the seed under the ride (part (c), with the Boss's note "the seed must birth").**

A pair is born where two whole quanta stand at one Node (The board reads itself). So a seed births iff some Node holds two whole quanta at the vacuum's weight, or gathers them. The standing wave's share at a Node scales as A^2. Under U24_RIDES=3, measured (the forward acts are U24_RIDES=2's, the mend acting on the run back alone):

| seed | quanta at the centre at the seed (engine; vacuum's weight) | quanta on the board at the seed | births (intervals) | charge's sum | count at the top (X largest, interval) | MATCH per step / chained | false tops |
| --- | --- | --- | --- | --- | --- | --- | --- |
| standing wave A 576, the close | 10; 10 | 22 (23 at the vacuum's weight) | 9 lines (8, 17) | 0 | 7 on the board (10,925, 60) | 58 / 48 of 60 | 2 |
| standing wave A 320, the close | 3; 3 | 9 | 2 (28, 58) | 0 | 2 (3,415, 60) | 60 / 60 | 0 |
| standing wave A 260, the close | 2; 2 | 2 | 1 (5) | 0 | 1 (1,014, 38) | 60 / 60 | 0 |
| standing wave A 200, the close | 1; 1 | 1 | 1 (59) | 0 | 2 (1,016, 56) | 60 / 60 | 0 |
| the law's hole seed, the close | 1; 0 | 26 (25) | 6 (4) | 0 | 6 (7,852, 60) | 60 / 60 | 0 |
| standing wave A 576, no close (open) | 10; 10 | 22 (23) | 0 | 0 | 22, the centre 2, 1 at the vacuum's weight (19,517, 80) | 79 / 76 of 80 | 1 |
| the uniform sea, no close | 1; 0 | 27 (26) | 0 | 0 | 27, 8 at the vacuum's weight (1,732, 48) | 80 / 80 | 0 |

Which seeds birth, under the ride:
- The law's hole seed: at 4, with the take exact (142,567,961 against the walls 142,560,000, excess 7,961).
- A standing wave whose antinode holds two whole quanta: A 260 and above; the first births at 5 (A 260) and 8 (A 576).
- A wave with one quantum at the centre gathers a second and births late (A 200: at 59).
- The uniform drift as laid births nothing by itself: its count is 1 or 0 per Node, the count not kept (R3, R4).

The Boss's "one quantum per mode plus one" lies below A 200: at most one quantum at any Node and nothing born. So the seed the ride admits, and that births, is the standing wave of 2 whole quanta at its antinode or more: A at least 260 on the 3-cube at den 1,021, its count about 2 on the board at the seed. Alternatively the law's hole seed.

The count at the top is not 1 per Node. On the open board the centre goes 10 -> 2 and the vacuum's weight 23 -> 1, at e^U 2.04 at the centre. The scattering is the write's own and the fifth act's:
- The volume the wave writes is inhomogeneous: X 17,210 at the centre against 19,517 at the largest Node by 80, moving up to about 200 levels per interval at the centre.
- The single-Node turns reverse the light at their Node: 26 to 28 turn intervals in 80.

It is not the ride's: with the volume set by hand, the ride keeps A^2 sin omega X within 4.2 and 5.7 percent (R3, R4). The law's seed under the ride is therefore the owner's word: the hole seed, or a standing wave of 2 quanta at the antinode, with the count read in the books; one quantum per mode is not kept at the top.

**1.6 The flux form's L clause under the ride, part (d).**

With the half wall's move, the centred momentum P_c = w X_before (now - before) + r - (w X_before) div 2 moves by exactly X_now [SUM_j R_ij (m_j - a_now) - D a_now]. The out-momentum of one interval is the in-momentum of the next (X_before' = X_now). Summed over the board, the Link terms pair as (a_j - a_i)(X_i R_ij - X_j R_ji). In the reals:

  X_i R_ij = Gamma (Gamma / p_0)^4 x 2 num (p_0^2 / Gamma)^2 q_ij^2 G^2 / Gamma^2 = 2 num Gamma q_ij^2 G^2,

the same from both ends at every content profile, static or not. So for light (D = 0), L_ride = SUM P_c is conserved between turns:
- exactly on a uniform board: measured 0 at every interval without a turn on the sea;
- elsewhere up to the volume's reading, the time line's X against the volume of its content's level (up to 4 X / Gamma per level). Measured changes of order 10^16 per interval on the standing and hole boards, against w X v of order 10^18 at one Node.
- A turn reverses P_c at its Node.

## 2. What is derivable and what needs the owner's word

Derived and measured:
- the bijection criterion (M-invariance of the trigger);
- the twins under form A with the fifth act (4 met, each verified as two pre-states with one post-state);
- the local mend exact at every turned Node and wrong at the false tops, with the integer condition and its counts;
- the symmetric form, with M an involution (toy);
- the L clause;
- the seeds that birth.

Sentences as they would stand in ALGEBRA.md:

- **The fifth act's bijection** (under The swap at the top, dated 2026-10-25): "The fifth act is a bijection of the interval iff its trigger is invariant under the step followed by the swap, T(S) = T(swap(step(S))); under Rule3 with the form now^2 - next x before the step followed by the swap is an involution and the triple's trigger is invariant; a form of the line or of the write that is not time-symmetric leaves pairs of pre-states with one post-state, the twins, where no reading of the post-state can run back."
- **The line rides the volume, the symmetric form** (replacing form A's order, the former kept by name; the owner's word): "At every Node a line's momentum lives on the half interval with the wall W = (w div 2)(X_before + X_now), P_c = W (a_now - a_before) + r - W div 2; the interval moves it by X_now (SUM over the six Ports of R_ij (m_ij - a_now) - D_i a_now) with no division; the held write of the volume reads the lines' momenta in and out, u_in u_out with u the nearest integer to (2 P_c + 1) / (2 w X_now), and the levels now; the volume steps; then each line divides once at (w div 2)(X_now + X_next), its remainder kept in [0, (w div 2)(X_now + X_next)); backward the same acts in the reverse order; the swap complements a line's remainder at its own wall; the step followed by the swap is an involution and the fifth act a bijection by construction."
- **The backward trigger** (if the owner keeps form A): "Backward the fifth act fires where the forward act on the swapped post-state fires (the one-Link reach kept); the twins of form A are named and the run back is exact except at them." This keeps the law unmet by name.
- **The flux form's L under the ride**: "Under The line rides the volume, the linear sum of a massless line is the sum of the centred momenta, L = SUM over the Nodes of [w X_before (now - before) + r - (w X_before) div 2], conserved between the turns where X_i R_ij = X_j R_ji on every Link, exactly in the reals at every profile (X R = 2 num Gamma q^2 G^2) and in the integers to the volume's reading; the former L = SUM [w (now - before) + r] kept by name for Rule3's line."
- **The seed under the ride**: "The law's seed is the hole seed, or the standing wave about the centre with at least two whole quanta at its antinode; one quantum per Node and one quantum per mode are not kept at the top under the ride."

## 3. Every number, with its script and command

Python /home/user/Universe24/venv314/bin/python, from the worktree's root, with PYTHONPATH=$PWD/src and TMPDIR=/dev/shm/tmp. The tests' small universe: den 1,021, Gamma 1,000, T 36,000, G 16, on the bare 3-cube.

3.1 MATCH, misses and false tops (top_local.py FLAG BOARD; run_all.py runs the twelve). Output: top_local_<flag>_<board>.json/.log.
- "per step" = one step back from every true post-state.
- "chained" = the run back from the end.
- miss = turned forward, not turned back. false = turned back, not turned forward.

| board | flag 3 (local trigger): per step, chained, misses, false tops | flag 2 (R4): per step, chained, misses, false tops | flag 0 (branch): per step, chained |
| --- | --- | --- | --- |
| open standing (80, no close) | 79, 76 (first miss at 4), 0, 1 | 79, 62 (first at 18), 1, 0 | 80, 80 |
| hole seed (60, close) | 60, 60, 0, 0 | 60, 60, 0, 0 | 60, 60 |
| uniform sea (80, no close, top at 48) | 80, 80, 0, 0 | 80, 80, 0, 0 | 80, 80 |
| closed standing (60, close) | 58, 48 (first at 12), 0, 2 | 60, 60, 0, 0 | 60, 60 |

Turned Node-intervals forward, flag 3: 208, 122, 27, 251. Under flag 3 the former reading beside it (board.bijection_turned): misses 1, 0, 0, 0 and false tops 0, 0, 0, 0.

3.2 The twins and the reversal error (twin.py BOARD FLAG; run_twins.py). Output: twin_<flag>_<board>.json/.log.

| flag, board | twins | delta histogram (non-turned Node-intervals) | false-top conditions met |
| --- | --- | --- | --- |
| 3, open | 2: interval 4 (local trigger), 18 (former reading), each verified | 0 at 1,784; nonzero at 201, -5 to 133 | 1 |
| 3, closed standing | 2: intervals 4 and 12 (local trigger), each verified | 0 at 1,176; nonzero at 193, -10 to 7 | 2 |
| 3, hole | none | 0 at 1,371; nonzero at 126, -4 to 54 | 0 |
| 3, sea | none | 0 at 2,052; -1 at 27; 1 at 54 | 0 |
| 0, open | none | 0 at 1,985 | 0 |
| 0, closed standing | none | 0 at 1,419 | 0 |

"Verified" means the wrong pre-state stepped forward gives the post-state with 0 unequal entries.

3.3 The 48 (top_local.py):
- The backward masks are invariant under all 48 at every backward step: 3,840 element-steps of 3,840 (open), 2,880 of 2,880 (closed standing), 3,840 of 3,840 (sea), under flags 2 and 3.
- The first single-Node turn (interval 7, the centre, X0 1,042 < X1 1,044): 48 of 48 elements keep every level.
- At the end: the open board 48 of 48; the closed boards 1 of 48 (the draws, the law's named exception); the hole seed is not a symmetric lay.

3.4 Locality (locality.py, open board, flag 3; locality.json): a two-Links change altered the centre's inverse at 0 of 80 intervals; the one-Link control at 67 of 80; the centre was turned back at 13 intervals.

3.5 The toy (symmetric_ride.py GAIN [AMPLITUDES]; run_symmetric.py). Output: symmetric_ride_g1.json, symmetric_ride_g30.json, symmetric_ride_g1_A450_600_750_900.json. The numbers are in 1.4.

3.6 Off path bit for bit (offpath.py; offpath.json). The flag unset on the patched src against git archive of 7dc781bc2's src, with the sha256 of every forward array:

| board | sha256, patched and pristine alike | MATCH |
| --- | --- | --- |
| open | 48fde39f90679d0bcf779e8970d07158a2cfc36b0ec9a185ebe15c88198eedbb | 80 / 80 |
| hole | b2c3b1904dbc8616dc6438176314cd704ce27c420717c335fe0eeee65fe80fd6 | 60 / 60 |
| sea | ff01fa320c7417501a3bd0d228427a97675a6a9ef1ae87989507e66bd3a952f7 | 80 / 80 |

3.7 The width: the widest state integer is 60 bits (open), 76 (closed boards), 59 (sea). No integer is added per Node: the scratch copy is a transient of the act, not state.

3.8 The src lines (git diff against 7dc781bc2): R4's diff unchanged (bookings.py, digits.py, emission.py, lattice.py; flux.py and swap.py as R4 left them), plus mine:
- flux.py: `RIDES` takes "3"; `MENDED` is true at "2" and "3"; `LOCAL_TOP = (U24_RIDES == "3")` added.
- swap.py, `acted`: under `direction == -1 and flux.LOCAL_TOP`, `board.bijection_turned = mask` (a reading) and `mask = forward_turned(board, held)`.
- swap.py: the function `forward_turned(board, held)` added (the scratch copy, the swap and the phases at -1 over every Node, the phase act back, `advanced_to_the_close`, its `turned`).

Not measured, named: the conserved form at fixed reads under flag 3 (the forward acts are flag 2's; R4's equality to the unit stands for them); the momentum and the energy in the clicks before and after a click; the 5-cube.

## 4. The toy for David

- **The lay.** The ring of 12 Nodes; per Node one light line (now, before, r) and one volume time line (X, X_before, rho). w = 24 x 1,021 = 24,504; R = w / 3 = 8,168; S = 2 w - 2 R. The volume's line: E = 65,536 with E (X_next - 2 X + X_before) + rho' - rho = GAIN x source - (E div 40)(X - 1,000), GAIN 1. The light laid at A = 300 at the Nodes 0 mod 4 (2 A at Node 0), -A at 2 mod 4, 0 elsewhere; before 0. X = X_before = 1,000; rho = E div 2; r at half its wall.
- **The forms.** R4's (the riding line at w X_now, the remainder born at w X_before, form A's source after the division) and the symmetric form of 1.4. The fifth act at the weak maximum of X, the swap complementing at (w div 2)(X_before + X_now) and rho at E.
- **The intervals.** 300 forward. Then from every true post-state one step back by the former reading (the triple of the engine's inverse) and by the forward act on the swapped state. Then the chained run back.
- **What to read.** Random boards with the step's G(F(S)) = S and with M(M(S)) = S. Per run: the per-step matches, the misses and the false tops, and the widest integer.
- **The pass predicate.**
  - The symmetric form: M(M(S)) = S on every random board; per step 300 of 300 under both readings; 0 misses; 0 false tops; the chained run back 300 of 300; every integer within 128 bits.
  - R4's form as the control: M(M(S)) = S on no random board.
- **The deviation from the law's letter.** The volume's write is the toy's (a restoring term and a gain) and not the engine's E_s T write; one light line, no paces.

## 5. Verdict

The local mend (a) DOES NOT WORK. Laws checked:
- locality: 0 of 80 for a two-Links change, 67 of 80 for one Link;
- the 48: every backward mask 48 of 48, the first single-Node turn 48 of 48;
- the fixed count and the 128 bits: 0 integers added, 76 bits;
- integers only;
- the exact take and the charge: 142,567,961 against the walls 142,560,000; the senses' sum 0 at every birth;
- off path: the branch bit for bit, the digests equal.

The one law unmet is the run back exact. The interval under form A with the fifth act has twins (two pre-states, one post-state, 4 verified). The local trigger is exact at every turned Node (0 misses over 608 turned Node-intervals) but falls on the false tops: 3 met, open 76 of 80, closed standing 48 of 60. The former reading falls on the missed top: open 62 of 80. The mend within the laws is the symmetric ride of 1.4, the momentum at the half interval's mean wall with the write read from the numerators; it WORKS WITH THE SENTENCE on the toy (M an involution, 1,666 of 1,666; 0 twins in 8 runs) and is not built in the engine.
