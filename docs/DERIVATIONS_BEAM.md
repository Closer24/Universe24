# Derivations of the known laws from the Beam Law (round 9 onward)

The model owner's direction of 2026-09-20 ([record 159](LOG_2026-09-20.md#159-the-owner-proposes-a-derivation-mathematician-2335z-the-owners-words-translated-a-formula-mathematician-whose-whole-role-is-to-derive-formulas-without-runs-will-work-on-a-strong-machine-of-his-own-the-role-to-reach-the-known-formulas-only-from-our-vector-scalar-and-tensor-activity-which-is-in-fact-an-infinite-activity-on-the-gameboard-to-look-at-everything-and-verify-that-everything-is-only-in-such-activity-the-bosss-answer-yes-as-round-9-onward-of-derivationsmd-on-the-beam-law-rounds-1-to-8-derived-the-earlier-laws-beam-v1-has-no-derivation-round-yet-a-standing-read-only-session-with-the-register-as-its-test-data-one-formula-per-note-checked-against-a-registered-integer-and-the-audit-of-every-rule-as-an-operation-on-the-integer-torus-opened-on-the-owners-word),
his words translated): "to reach the known formulas only from our vector,
scalar and tensor activity, which is in fact an infinite activity on the
GameBoard; to look at everything and verify that everything is only in such
activity"; "if you take the computation on our Nodes to infinity you should
derive Einstein's formulas, all of them"; "information is discrete, the
computation is discrete, what does it cost us? The cost is discrete too".
This document answers it on paper for the Beam Law, `beam-v1`
([BEAM_LAW.md](BEAM_LAW.md)), as [DERIVATIONS.md](DERIVATIONS.md) answered
it for the laws before it (rounds 1 to 8, the same method, section 0 there):
one interval of the engine written as an operator on the GameBoard, its exact
identities, its limit over many intervals, many Nodes and large N, Q and K,
and the place where the integers depart from the known formula. No engine
run is made for it; the register ([EXPERIMENTS.md](EXPERIMENTS.md), the
world READMEs, [VALIDATION.md](VALIDATION.md)) is its test data: every
derived formula is checked against an integer already registered, never by a
new run. The small arithmetic checks are made in Python on the formulas of
this document alone, seconds each; they are not engine runs and establish
nothing about the engine. Nothing here is tuned: a formula that does not
return is a result, stated with the place it fails.

The verdict of each section uses DERIVATIONS.md's three words. **Reached**:
the known law follows from the rules in the stated limit, exactly or up to a
constant that is named. **Different law**: the rules give a definite law of
another form, stated, with the registered integer or the run that shows the
difference. **Not reached**: the rules as declared do not determine the
quantity, and what would is stated plainly.

The reference tree is `main` at `f89884f0` (the law as landed on 2026-09-20,
BEAM_LAW notes 1 to 40); where the fraction-free branch
(`origin/fraction-free` at `ddec5166`, note 41 there, record 154, its
physics review record 157) changes an operation, both are stated, the
branch's form named as the ordered one. The crossing rule (record 158) and
the `no-tables` items of record 155 are designed and not built; they are
cited as orders, not as code.

Section 0 states the law as one operator with its two blocks and places
every result under its block (the owner's second pass, record 167 as the
Boss relayed it); sections 9 and 10 answer records 166 and 162. The
targets, in the Boss's order, one section each: 1 the inventory (the
owner's audit); 2 Doppler from the crossing rule; 3 Newton and Coulomb from
the bilinear coupling; 4 special relativity, the symmetry of the limit; 5
general relativity, the delay field; 6 the information cost and the
classical-quantum boundary; 7 Young's spacing and Bohr's levels.

## 0. The operator F: one piecewise-linear map on the integer torus, its two blocks, and where every result of this document sits

**The statement** (the owner's, accepted in record 167 as the Boss
relayed it; verified here against sections 1 to 7). The whole law is one
map F applied at every Node at every interval to the integer state s, per
component with its own rate r and wall d:

    s <- s + r;   e <- [s >= d];   s <- s - e d,

every wall crossing an event. The components of s and their (r, d): a
row's Manhattan count (rate `2 S_1 Q`, wall `2 T_d`, started at `T_d`;
section 1.4) and its three axis deficits (rate `abs(v_i)` per Manhattan
step, the carry `S_1` from the largest); a row's phase (rate
`phase_per_link` per Link, or `n` per interval of age with the wall d,
the whole part read mod N); a row's age (rate 1, no wall); a body's drive
per axis (rate `p_a`, wall `Q S M + abs(p_a)`); a body's counts, on the
branch the table `acc` (the turn: rate `content x n`, wall d; the owed
count: rate `counted x n`, wall d; the release and the lamp; the push per
column: rate `V E_c n_c`, wall `Lambda_c^2`); a record's birth wheel u
(rate 1 per birth, wall N); the click's ladder (the comparison `2 T u + T
<= 2 N C_k`, a wall read once). Everything in section 1.2 is F on one of
these components or a permutation of them (the collision, the meeting's
arc, the gate, the apportioning's tie), and the exceptions are section
1.3's list.

**The two blocks.** F is linear where its rates are constants of the
world, and it feeds back where a rate is a function of what arrives:

- **The linear block** (rows in flight): the translation at a constant
  rate (the flight, the phase per Link or per interval, the age); the
  group-ring addition at the merge (`Z[Z_N]`, with the cancel `[p + N/2]
  = -[p]`); the integer matrix of a split (`w -> w a_i`, `m -> m A`) or
  of a rotation (the half-angle tables) or of a gate (a permutation of
  labels); and the evaluation `ev: Z[Z_N] -> Z[zeta_N]` at the click,
  linear over the group ring. Every component here has the closed form

      s(t) = floor(s_0 + r t)     (the accumulator's whole part at a constant rate; FORM.md section 1),

  so a row's state at any time is a formula of its birth and its age, and
  the limits of this document are limits of that formula.
- **The feedback block** (the rates as functions of the arrivals): the
  push `r = C a` (C the reader's charges per column, a the label flow of
  the arriving rows: the rate of a body's momentum is bilinear in the
  state, the reader's content times the flow); the owed count (the rate
  the presence, or the age moment); the turn and the release (the rate
  the content, which the clicks change); the drive (the rate the momentum,
  which the push changes); the meeting's turn (the rate the crowd's flow).
  These have no closed form; they are iterated, and their continuum limit
  is the differential equation `ds / dt = r(s)`.

**The readout.** The click reads one comparison, the ladder's cell `2 T u
+ T <= 2 N C_k`, and nothing else leaves the rows (section 6.1); the `C_k`
it compares against are the norms `|ev(.)|^2` of the linear block's
evaluations, the one quadratic step of the law.

**Every result of this document under its block**, with its closed form
or its difference equation, its limit, and the registered integer it is
checked against:

| Block | Component and its closed form | The limit | The registered check | Section |
| --- | --- | --- | --- | --- |
| linear | the flight, `m(tau) = floor((2 tau S_1 Q + T_d) / (2 T_d))` and the deficit ladder | the digital line at `Q / T_d -> 1 / sqrt 3` Links per interval, isotropic | record 144's cone, 17 and 24 Links at age 29 | 1.4, 4.1 |
| linear | the phase, `floor((n / d) tau) mod N` along the line | `omega = c k`, dispersionless (the paper's check) | L7's path phases 23 and 23 (the pair form), 51 and 8 (the integer form) | 4.1, 7.1 |
| linear | the crossing count of a row's line with a body's, `n (c +- v) tau + O(1)` | the receiver's Doppler `1 +- v / c` | record 158's 45, 58, 19, 38, 183, 311; the bar's 96.9 .. 303.1 | 2.2 |
| linear | the merge, `Z[Z_N]` at one Node | the coherent sum within one Node | L1's `mz_equal` 41 of multiplicity 1682 | 6.3 |
| linear | the evaluation at `zeta_N` and the norm | `S(N, Q) -> 2 sqrt 2`; Born to `1 / (2 N)` | `176 / 64`, `2896 / 1024`, `11584 / 4096`; the dark port 0 of 64 | 6.2 |
| linear | two rows' phases at a pixel, `(n / d)(L_1 - L_2) / c` | Young's `lambda D / s`, from the fan's angular measure (record 160's Farey weights `3 Q^2 / (T_d T_d')` per direction) | L1's unequal arms 64/0, 32/32, 0/64; record 156's spacing 20.5 | 7.1 |
| linear | the split's norm `sum w_i^2 / m_i = w^2 / m` | the conservation of a record's norm | L1's (3, 4) split 63/1 | 6.1 |
| feedback | the push, `p_{t+1} = p_t + C a_t`, `a_t` the flow at the body's Node | `dp / dt = -M grad(A)`: Newton's and Coulomb's `1 / r^2` in the shell mean | series C's nine ring readings `r / N(r)`; item 7's `-1`, `-1 / 4` | 3.2 .. 3.4 |
| feedback | the drive, `x_{t+1} = x_t + [drive >= D]`, `v = p / (Q S M + p)` | the dispersion `v(p)`, saturating at 1 | the bar's speeds 0.30, 0.45, 0.75 exact | 4.4 |
| feedback | the owed count, `owed = by_clock(age, k n, d)` (the branch: `acc_owed`) | the clock at `1 / (1 + k n / d)`, the potential `M / r` under `age` | series E's `k_a r = 36.1`, `k_s r^2 = 41.5` | 5.1, 5.2 |
| feedback | the field of many bodies, the sum of their rows' moments | Poisson and the retarded wave equation, linear | series E; series K's 0.000 (no term on the rows) | 5.1, 5.4 |
| feedback | the turn under `action`, `phi += floor(k_1 abs(p) N / h) - floor(k_0 abs(p) N / h)` | the action `2 pi p r = j h` | series H's re-reads (r = 12 the whole j) | 7.2 |

**The feedback block per world class**, its difference equation and its
continuum limit `ds / dt = r(s)`, against the register:

| Class | The difference equation, per interval | The limit | Registered |
| --- | --- | --- | --- |
| D, the orbit (a body about a fixed source, gravity) | `p += -M_A V(x)`, `V(x)` the flow at x (`q Q / N(r)` in the shell mean, radial); `x` by the drive | `d^2 x / dt^2 = -G M x / abs(x)^3`, a Kepler orbit with the retarded field | no orbit closed by D's criterion; the flat-curve period ratio 3.73 against 4 (record 131): the six-heading shells of section 3.2, not the limit's ellipse |
| H, Bohr (the electric column against the proton's fan, the turn) | the same with `C = M_A (rho_A rho_B - 1)` and `phi` by the turn | the same orbit; the closure `2 pi p r = j h` | the mean inward push 40 600 against the derived 39 660 (1.02); r = 8 and 12 closing under the step drive | 7.2 |
| G2, the stars (bodies thrown from one point in a crowd) | `p_i += -M_i sum_j V_j(x_i)` and the clock's owed count from the crowd | the deceleration of a matter-only expansion, `q > 0`, retarded | `q = +0.922` (the source rule), `+0.345` (under the key), `-0.108` coasting; nothing gives `q < 0` (records 124, 138) |
| I, the nucleus (two bodies at one Link, three columns) | `p += (Q_A Q_B - G_A G_B - M_A M_B) U(1)` per interval toward the partner; a refused step hands `p_x` over | a fixed point `p = 0` on both after each contact: a bound pair | the deuteron's `310 967 280 640` per interval, 0 steps in 3000, the label 0 after each hand-over; the branch's 69 waits of 700 |
| J, the weak (a clock in a crowd against a key) | `owed = by_clock(age, c n, d)` at the crowd c; the trigger at `at` | `t_trigger = at (1 + c n / d)`, the telescoped count | j1's 522 .. 524 pinned from 12 to 14 rows (525 at 15), j3's 574 pinned and 577 read (the crowd not one number) |

**The classical-quantum boundary as the property of the rate.** A
component whose rate is a constant of the world has the closed form
`floor(s_0 + r t)`: its state at the click is a formula of its birth,
exact whatever happened in between, and two such components of one record
meeting at one Node are compared exactly by the evaluation: that is the
quantum case, and the interference is the closed form's. A component
whose rate is a function of the state is iterated, its history matters,
and its limit is a differential equation: the classical case, a body's
momentum under the push. A record is quantum while its rows are in the
linear block and no read has selected a label (section 6.3: the
visibility `[reads = 0] x 2 w_1 w_2 / (w_1^2 + w_2^2)`, the which-path S
from `176 / 64` to `88 / 64`), and a body is classical because its rate
reads the crowd. The boundary is crossed once per record, at the click,
which is the one place the linear block's closed form is compared against
a wall.

**The paper's sentence.** "The model is one piecewise-linear map on an
integer torus; the measurement is the one threshold that is read out."
This document supports it with two precisions, without which it is not
exact: (i) the map is piecewise-linear in every component of the rows
(the flight, the phase, the age, the merge, the split, the evaluation)
and in every count at a fixed content, but the feedback block's rates
are bilinear in the state (the push is the reader's content times the
arriving flow, `nature_beam.py:2147-2221`), so the exact word for the
whole map is "piecewise-linear with bilinear rates" (or "piecewise-linear
in the rows"); (ii) the threshold read out is one comparison per record
(`2 T u + T <= 2 N C_k`, `amplitude.cell_of` on the branch, `rungs` and
`choose` on main, `amplitude.py:174-203`), and the quantity it compares
against is the norm of the linear evaluation, the law's one quadratic
step; the sentence is exact if "the one threshold" is read as that
comparison and the norm is understood as what it compares. With those
two readings the document supports the sentence; with "piecewise-linear"
taken to cover the push and the click's weight, it does not.

## 1. The inventory: every rule of beam-v1 as an operation on the integer torus, and what is not one

**The claim audited** (the Boss's statement of the law to the owner, record
155, verified here against the documents and the code). The state is
integer vectors on tori and nothing at a Node. A row (a ray's record,
`NatureBeam`, `nature_beam.py:195-240`): its Node in `Z_X x Z_Y x Z_Z` (a
periodic axis a circle, an open axis a segment with the face as its
border), its direction an index of the world's table D, its age a whole
count, its phase in `Z_N` (and, in the pair form of `phase_per_link`, a
point of `Z_{N d}` whose whole part is the phase, note 37 (iii); the row
carries the age, from which that point is a function), its number, its
amount, its content, and under a record its identity, branch, multiplicity,
birth phase u and hand. A body (`Measured`, `measured.py:205-353`): its
held content per family in `Z^F`, its momentum p in `Z^3`, its phase in
`Z_N`, its clock age, its drive per axis in `(-D, D)`, and on the
fraction-free branch its counts table, the point `acc` of `Z^n / d Z^n`.
One operator every interval at every Node. Six operations only:

- **(T) the translation**: `x -> x + r` on `Z^k` or on a torus; the counts'
  form `acc += r; e = [acc >= d]; acc -= e d`, every wall crossing an
  event, is the Euclidean division `Z = Z/d x Z` with the remainder kept
  (`core/integer.py:70-86`, `by_drive`), the one primitive of every count;
- **(B) the bilinear form**: a moment `sum_rows w x u^(x)k` of the
  neighbourhood's rows (k = 0, 1, 2 and the age), and the coupling `r = C
  a`, a signed inner product over declared columns times the moment;
- **(G) the group-ring addition** in `Z[Z_N]`: the merge of identical rows,
  with `[p + N/2] = -[p]` on a record's rows (the cancel);
- **(P) a permutation of the joint state**: the collision, the meeting's
  turn, the gate, the apportioning's tie;
- **(E) the evaluation** `ev: Z[Z_N] -> Z[zeta_N]` through the tables C, S
  and the norm `|z|^2` (the click), then the ladder on the wheel;
- **(D) the Euclidean division with the remainder kept** (the same as (T)'s
  carry) and **the comparison** (the ladder's cell `2 T u + T <= 2 N C_k`,
  an age against a key, a phase against a window, a threshold), itself a
  division whose quotient is 0 or 1 and whose remainder is not read.

Everything else is what the owner asked to be listed: a floor whose
remainder no record owns, a table looked up at run time that is not a cache
of one of the six, a branch on a declared name, an event dropped.

### 1.1 The state, verified

The Node holds nothing (`NatureBeamStore`, `nature_beam.py:1045-1280`: the
store is a structure of arrays over rows, sorted by Node; a Node is an
index, not a record; `nature_beam.py:2285-2291`, `node_event`, is the host's
index of which body is where, rebuilt from the bodies' sets every interval
and read, not written, by the law). What a body holds beyond the vectors
above is host bookkeeping (tallies, pending rows waiting for the next
self-creation, the frame's copies `frame_content`, `frame_charges`,
`frame_momentum`; `measured.py:277-352`), and the apparatus's layer
(`amplitude.py:296-752`) is the record's own ledger, the memory no Node may
keep (record 156, TWO_SLITS.md section 1). The claim of the state holds.
One correction to the Boss's statement: the phase of a row in flight is
`Z_N` on the record; the point of `Z_{N d}` exists only where the family
declares the pair form, and even there the row carries the age, not the
accumulator, so the residue is recomputed from the age (a constant rate:
the identity case of FORM.md section 1, exact).

### 1.2 The inventory, rule by rule

The six operations are named by their letters. A rule marked **NOT** is
listed again in section 1.3 with what replaces it. Every line is `main` at
`f89884f0` unless it says the branch.

**Step 1, the walk (`nature_beam.py:2389-2510`).**

| Rule | Where | Operation | Verdict |
| --- | --- | --- | --- |
| The Manhattan count `m(tau) = (2 tau S_1 Q + T_d) // (2 T_d)` | `nature_beam.py:549-554`, `632-643` (the step table) | (T)/(D): an accumulator started at `T_d` (the half), gaining `2 S_1 Q` per interval, carrying one Manhattan step at `2 T_d`; `2 S_1 Q <= 2 T_d`, so at most one Link per interval | a torus operation; the table `flight.steps[direction, age mod L_d]` at `2398` is its exact cache, since the rate is constant and the age is the accumulator (FORM.md section 1); checked below |
| The digital line (Bresenham): at Manhattan step j the axis maximising `abs(v_i) (j + 1) - S_1 abs(pos_i)`, the lowest axis on a tie | `nature_beam.py:580-592` | (T)+(D): three deficit accumulators, each gaining `abs(v_i)` per Manhattan step, the carry `S_1` taken from the largest (a comparison, the axis furthest behind); ties by axis order | a torus operation with a declared tie (x before y before z); the table `lines` its cache |
| The wrap on a periodic axis | `nature_beam.py:2403-2405` | (T) on the circle `Z_extent` | a torus operation |
| The open face: the escape | `nature_beam.py:2407, 2413-2483` | the border; the escaped rows' pointer (E) and labels (B) booked | the one-way border (a click), not an operation on the state |
| The phase per Link `phase += phase_per_link x moved` | `nature_beam.py:2496, 2501` | (T) on `Z_N` by the Links stepped | a torus operation |
| The phase per interval of age, the pair form `by_clock_rows(age, n, d)` | `nature_beam.py:2497-2499`, `481-493` | (T) on `Z_{N d}`, the whole part read; the residue `(age n) mod d` a function of the age | a torus operation (the constant-rate identity; nothing discarded, the age holds the residue) |
| The age `age += 1` (a rest row keeps it) | `nature_beam.py:2500` | (T) on `Z` | a torus operation |
| The direction table's unit vectors `u_d`, the nearest integer vector to `Q D / abs(D)`, and `T_d = isqrt(3 abs(D)^2 Q^2)` | `nature_beam.py:557-577`, `608` | an integer square root, once per direction at load | a declared rounding of the world's table, like C and S (record 156: its anisotropy `156` against `110 sqrt 2 = 155.56`, one step in 234 on the cone); not a run-time operation |

**Step 2, the readings (`nature_beam.py:264-475`).**

| Rule | Where | Operation | Verdict |
| --- | --- | --- | --- |
| The moments of order 0, 1, 2 and the age moment, `sum amount x u^(x)k` over a set, split outside and here | `nature_beam.py:353-377` (`moment_table`), `434-475` (`read_arrivals`), `412-431` (per group) | (B) | a torus operation (exact integers; the bound a refusal, not a rounding) |
| The traceless tensor `3 M_2 - tr(M_2) I` | `nature_beam.py:319-327` | (B) (a linear map of the second moment) | a torus operation |
| The label flow `sum content x amount x u_d` (paid) or `sum amount x u_d` (free) | `nature_beam.py:857-916`, `2973-2978` | (B) | a torus operation |
| The presence and what the clock counts (the presence or the age moment by the entry's `reads`) | `nature_beam.py:2920-2922, 3065-3070`; `measured.py:129-140` | (B); the selection by a declared key | a torus operation; the key is a world declaration, not a branch on a name |

**Step 3, the collision and the meeting.**

| Rule | Where | Operation | Verdict |
| --- | --- | --- | --- |
| The collision: per (Node, number, content) class the single units in the eight slots permuted; the class `(crowd mask, n, S)`, its members sorted as 8-tuples, the forward map the cyclic shift | `nature_beam.py:2293-2335` (`collide`), `677-705` (the table generated from its rule) | (P): a permutation of the joint state, fixed on the class invariants (amount and the labels' sum conserved) | a torus operation; the table of `3^8` codes at `2321` is the cache of the rule "sort, then shift"; its tie (the sorted order is Port order) is the one undeclared breaking of the 48 (BEAM_LAW section 4, FORM.md section 3): a stated limit, not a discard |
| The meeting (`meeting-v1`, under the key): the crowd's flow (B), `kappa` the column sum (B, a rational), the target `t = sum kappa V` | `meeting.py:244-279, 214-226, 325-342` | (B) | a torus operation |
| The meeting's norm `abs(t) = isqrt(t . t)` | `meeting.py:351-358` | an integer square root at run time | **NOT**: a rounding whose remainder (the fractional part of the root) no record owns; the one non-rational function evaluated on the lattice per interval |
| The meeting's register `adv = (abs(t) + Q/2) // Q`, `total = phase + adv`, `k = total // N`, `phase' = total mod N` | `meeting.py:229-241`, `364-367` | (T)/(D) on `Z_N` with the carry k into the turn: a torus operation in `phase`; but `adv` rounds `abs(t) / Q` to the nearest each interval | **NOT** in `adv`: the crowd met below `Q / 2` in an interval is dropped and above it rounded up, nothing accumulated (the exact form: `acc += abs(t)` on `Z_{N Q}`, the carry per Q, no rounding) |
| The arc permutation `pi_t^k` (the sectors about t, sorted by the exact angle, shifted by k) | `meeting.py:161-211`, `369-380` | (P) built by comparisons (cross-multiplied angle keys; ties by index) | a torus operation; the permutation per target is cached (`132-144`), a cache of a rule, not a table of the law |

**Step 4, the tables and the detectors (`nature_beam.py:2528-3505`).**

| Rule | Where | Operation | Verdict |
| --- | --- | --- | --- |
| The threshold: the amount over the set against the declared threshold | `nature_beam.py:2749-2757` | (D) a comparison | a torus operation |
| The window: `(d + w // 2) mod N < w` | `nature_beam.py:496-509`, `2792-2793` | (D) a comparison on `Z_N` (one floor of the width, exact) | a torus operation |
| The set's phase for the window under `wave`: the pointer of the arrivals (E) and its nearest step | `nature_beam.py:2767-2774`, `927-959`, `967-999` | (E) then a comparison (`argmin abs(X S_k - Y C_k)` among `X C_k + Y S_k > 0`) | (E) is the click's own map applied before the click as a reading; the nearest step discards the pointer's angle within one step of N: a declared rounding of the click's kind (the phase returned, note 24), stated |
| The parity filter (the hand): the row's hand against the entry's | `nature_beam.py:2807-2808`, `1966-1992` | (D) a comparison of two declared bits | a torus operation |
| The `beam` reading's pairing: the rays that would click paired by opposite phase, greedily in row order, a paired couple passing on | `nature_beam.py:2837-2890` | a greedy matching in the store's row order, `min(left_i, left_j)` per pair | **NOT** one of the six: an order-dependent matching (a declared option, absent by default since record 02; under `wave` and `sum` unused); listed, not ordered away |
| The push, ONE signed inner product over the columns, per column `epsilon_c sign(V E_c n_c) by_clock(age_A, abs(V E_c n_c), D_c d_c)` | `nature_beam.py:2147-2221` (`push_form`), `3236-3252` | (B) the product; then per column a floor off the clock | (B) a torus operation; the floor **NOT** where `D_c d_c > 1` (`2219`): the remainder `(age x V E n) mod (D d)` is recomputed from the age at a numerator that changes every interval, so the discarded parts drift (FORM.md section 2: +38.7 label units off the exact 12 239.3 over 5000 intervals); the branch's `acc_push` per column and axis is the torus form (note 41 (iv)). On the register the divisor is 1 on gravity and on every whole charge, so the floor is exact and identical everywhere but the series 7 pair |
| The push by share: a record row's push `label x amount // m`, the rest to the books' `remainder` line | `nature_beam.py:845-854` (`share_of`), `2983-2996`, `3136-3143`, `3299-3306`, `3897-3910` | a division whose remainder is booked on a ledger line of the host | **NOT**: the remainder's owner is the books, not a record (record 155 (3) orders it onto the giver's record) |
| The reading's weight at the relative speed (`doppler-v1`, under the key): the speed `w_a = G abs(p_a) // D_a`, the flux pair, the weighted flow `by_clock(age, abs(V_d) num_d, G Q abs(v)^2)` per direction | `nature_beam.py:2038-2058`, `2061-2087`, `2090-2144` | (B) for the pair; two floors | **NOT** twice: `(G abs(p_a)) mod D_a` is discarded every interval (`2057`, a declared grain), and the per-direction floor at `2142` discards as the push's does (the branch's `acc_flow`, note 41 (iv), owns the second); the whole rule leaves the code under the crossing rule (record 158), where the reader's Doppler is an encounter count with no weight |
| The click: `held += content`, `clicks += amount`, the momentum `+= push` | `nature_beam.py:3245-3252`, `3384-3388` | (T) on `Z^F` and `Z^3` | a torus operation |
| The home: the own number's rows taken to be created again; a paid row's labels join the momentum | `nature_beam.py:2664-2727`, `3109-3158` | (T) (a transfer between two lines of one record) | a torus operation |
| The detector's record `X^2 + Y^2` of the clicked rows; the set's phase returned to its events | `nature_beam.py:3035-3053`, `3467-3500` | (E) and the norm; the nearest step as above | the click: (E) at the border; the returned phase's rounding declared (note 24) |
| The transformation `become`: at a click of the entry or at the age against the key `at` (`ages_at_key`), gated by `crowd` (a comparison), the family changes and the products pend | `nature_beam.py:1413-1510`, `3528-3535`, `3455-3457` | (D) comparisons; (T) on the held vector | a torus operation; the trigger and the products are world declarations |
| The rule per (body, family): `read`, `measure`, `rerelease`, `pass`, `become` | `nature_beam.py:1402-1407` (the codes), `3104`, `3262`, `3308`, `3456`; the defaults `world.py:743-755` from the quantum | a branch on a declared verb | **NOT** (a branch on a name): the verbs are declared per entry; record 155 (5) orders them derived from the families' keys (today `default_rule` derives the default from `free`, a declared entry overrides it) |
| The contact: a refused step hands the axis component to the occupant (`measure`), returns it doubled (`rerelease`), or nothing; the share over several occupants by content | `engine.py:661-766` | (T) a transfer of momentum between two records; `apportion_whole` (P); a branch on the verb | (T) a torus operation; the verb a branch on a name (the same item); the refused step's drive, see step 5 |
| The give (`binding-v1`): `units = held // h`, `held mod h` kept | `engine.py:768-838` | (D) with the remainder kept on the giver's `held` | a torus operation |
| The gather: the layer's ladder at a record's completion | `amplitude.py:590-752`, `nature_beam.py:4120-4181` | (E): the products of residuals in `Z[i]`, the norm summed over Node tuples; the rungs `b_k = (2 N C_k + T) // (2 T)`; the cell `u < b_k` (D) | the click: (E) and a comparison; the rung's rounding to the nearest declared once per record (note 41 (v): the cell is the comparison `2 T u + T <= 2 N C_k`, the same integers) |

**Step 5, the self-creations (`engine.py:418-473`, `nature_beam.py:3507-3977`).**

| Rule | Where | Operation | Verdict |
| --- | --- | --- | --- |
| The turn `s = by_clock(clock_age, content x n, d)`; the phase `+= s mod N` | `engine.py:456-473`, `world.py:1019-1026` | (T) on `Z_N` by s; s a floor off the clock | **NOT** on `main` where the content changes (every registered lamp pays per birth: the drift +1 in 160, +9 in 20 000, +1089 in 200 000 births on `a0_b0`, record 148); the branch's `acc_turn` is the torus form (note 41 (i), (ii)) |
| The owed count `by_clock(clock_age, counted x n, d)`, paid one per interval | `engine.py:119-131`, `475-485`, `444-447` | a floor off the clock; the payment (T) | **NOT** on `main` where the crowd changes (the deuteron: 80 waits for the exact 69, record 154); the branch's `acc_owed` is the torus form |
| The free release `by_clock(age, held x n, d)` per direction | `nature_beam.py:3546-3566` | a floor off the clock | **NOT** on `main` where `held` changes (a click joined it); the branch's `acc_release` |
| The lamp's count `by_clock(age, rate_n, rate_d)`, capped by what the lamp can pay; nothing at a stalled self-creation or outside the window | `nature_beam.py:3746-3760`, `3788-3799` | a floor at a constant rate (the identity case); a `min` | the count is a torus operation; the cap and the stall **drop** the count gained there (note 41 (iii), "the one discarded count", a declared gate on the branch): listed |
| The birth phase `u = (births - 1) mod N`; the record's identity `number x 2^32 + ordinal` | `nature_beam.py:3801-3806`, `1525-1535` | (T) on `Z_N` at rate 1 per birth; an encoding | a torus operation (record 156: a lawful count; the wheel W with the bit-reversed ordinal, a fixed permutation (P) of its bits, the ordered generic form) |
| The split: `(w a_i, m A, p + t_i)` per direction, `A = sum a_i^2` | `nature_beam.py:3596-3695` | a linear map over Z with an integer matrix; (T) on `Z_N` by `t_i`; the multiplicity times the norm | a torus operation (the isometry of the paper's Theorem 1) |
| The rotation of a label bit: the amounts `w C'`, `w S'` of the half-angle tables of 2N, the multiplicity `x 65536` | `nature_beam.py:1848-1916`, `amplitude.py:125-140` | a linear map whose entries are the tables' rounded cosines | a declared rounding (the same tables as the click) applied ON the lattice, the one place besides the meeting's root where a rounded constant multiplies a row in flight: stated, lawful under record 155 (6) |
| The gate (CNOT): the joint labels permuted from the control's bit | `nature_beam.py:1769-1845`, `amplitude.py:393-488` | (P) | a torus operation |
| The apportioning of a row over the directions or over a body's Nodes: the floors, the units left to the largest remainders, ties from `age mod n` | `core/integer.py:88-113`, `nature_beam.py:3727`, `3866` | (D) exact (the shares sum to the total) with a tie by comparison; the tie's start a rotation (P) | a torus operation per birth; record 155 (3) orders the leftover onto the giver's record as an accumulator, which gives the same integers wherever the shares are equal weights (each direction takes the leftover once per n births either way) |
| The recoil: the momentum less the born rows' labels (their shares under a record) | `nature_beam.py:3888-3921` | (B) then (T) | a torus operation; the share's remainder as above |
| The right-hand rule: `sign(A . u_d)` against the product's hand | `world.py:1612-1620`, `nature_beam.py:3709-3719` | (B) and a comparison | a torus operation |

**The engine's frame, the step and the turn by momentum (`engine.py`).**

| Rule | Where | Operation | Verdict |
| --- | --- | --- | --- |
| The drive: `drive += p_a`; a Link at `+-D`, `D = Q S M + abs(p_a)`, `D` subtracted | `core/integer.py:70-86`, `engine.py:85-116`, `558-567` | (T)/(D): the paradigm of every count | a torus operation |
| The first axis whose rule fires steps; a later axis's coincident fire is lost, "its D subtracted, nothing carried" | `engine.py:552-568` | a carry taken from the drive with no Link crossed | **NOT** (an event dropped): the wall crossing on the second axis is counted (`axis_steps`) and paid (`drive -= D`) and the position does not move; the distance driven is lost, once per coincidence (every body with two nonzero components: the orbits of series D and H, the diagonal stars of G2). Not fixed on the branch. Stated in 1.3 |
| The refused step (a contact): the drive was paid and the body stays; under `read` or `pass` the labels stay too | `engine.py:630-634`, `661-766` | the carry paid, the Link refused | **NOT** (an event dropped) under `read` and `pass`: the drive loses D per attempt and nothing is handed; under `measure` the component is handed over (T), which is the torus form. Stated in 1.3 |
| The turn by momentum under `action`: `by_clock(k0, abs(p) N, h)` at the Link stepped, `k0 = axis_steps - 1` | `engine.py:637-645` | a floor off a count | **NOT**: re-prices the whole history at today's `abs(p)` (record 157: Bohr's electron's p turns every interval) and, since `k0` counts the lost and refused steps, the floor's increment at a skipped k is never added; ordered to join the counts (record 155) |
| The body's escape through a face | `engine.py:585-629` | the border | a click |
| The frame's copies `frame_content`, `frame_charges`, `frame_momentum` | `engine.py:441-443` | a read of the record once per interval | bookkeeping (D1, note 27), not an operation |

**Step 6, the border and the merge.**

| Rule | Where | Operation | Verdict |
| --- | --- | --- | --- |
| The border `lifetime`: `ages_at_key(age, L)`, `by_clock(age - 1, 1, L) = 1` | `nature_beam.py:512-522`, `3993-4061` | (D) a comparison of the age against a key (no rate) | a torus operation; the click there (E) |
| The age bound `ages_at_key(age, age_bound + 1)` | `nature_beam.py:4110-4114` | a comparison; a refusal | a guard of the host |
| The merge: identical rows summed; under a record the phase modulo `N / 2` with the sign, an equal pair leaving nothing | `nature_beam.py:1110-1129` (`identity_columns`), `1153-1237` (`merge`) | (G): the addition in `Z[Z_N]` with `[p + N/2] = -[p]` | a torus operation (a bijection); the packed key and the lexsort are the host's ordering |

**The apparatus's layer (`amplitude.py`, host state per live record).**

| Rule | Where | Operation | Verdict |
| --- | --- | --- | --- |
| The offer: `(X, Y) += 32 w (C[p], S[p])` per (Node, label); the residual per channel through the rotation's entries | `amplitude.py:490-575` | (E), term by term (ev is a ring homomorphism, so the sum of the images is the image of the sum, the tables' rounding linear) | the click's map, the record's ledger |
| The cells: products of residuals in `Z[i]`, `abs(z)^2` summed over Node tuples (coherent within one Node, incoherent across Nodes) | `amplitude.py:590-655` | (E) and the norm | the click |
| The rungs and the cell of u; the Node tuple within the cell | `amplitude.py:174-217`, `657-752` | (D) comparisons; one rounding to the nearest per record | the click; the rounding declared (note 41 (v)) |
| The common denominator of two multiplicities (a square test by `isqrt`) | `amplitude.py:156-171` | an exact test (the root squared back) | bookkeeping, no rounding |
| The live count, the completion, the aliases of a gate | `amplitude.py:335-392`, `657-752` | counters | the record's memory (record 156): host, not a Node |

**The tables of the law, computed once from N and Q at load.** C and S
(`core/phase.py:62-90`): the cosine and sine of `2 pi k / N` in 256ths from
a fixed-point series, rounded to the nearest; the half-angle tables of 2N
(`amplitude.py:125-140`); `u_d` and `T_d` (above). These are the declared
roundings of record 155 (6), confirmed by record 156: the click does not ask
for the integer circle. Every other table read at run time (`flight.steps`,
`flight.lines`, `collision.forward`, `arcs.cache`) is an exact cache of a
rule in the alphabet, stated above, and the rule can replace it integer by
integer.

### 1.3 What is NOT such an operation, for the implementer

Listed with the file and line on `main` at `f89884f0`, the class of the
departure, the record that already orders its replacement where one does,
and the exact torus form where none does. Items 1 to 6 are ordered already;
7 to 10 are this inventory's findings; 11 to 14 are declared roundings and
options, stated so that the list is complete.

1. **A remainder discarded: the turn.** `engine.py:456-473`,
   `world.py:1019-1026`, `by_clock(clock_age, content x n, d)`. Replaced
   by `acc_turn` on the branch (note 41 (i)); record 148.
2. **A remainder discarded: the owed count.** `engine.py:119-131`.
   Replaced by `acc_owed` on the branch; the deuteron's 80 waits become
   the exact 69 (record 154).
3. **A remainder discarded: the free release.** `nature_beam.py:3550`.
   Replaced by `acc_release` on the branch.
4. **A remainder discarded: the push's column floor** where `D_c d_c > 1`.
   `nature_beam.py:2219`. Replaced by `acc_push` (note 41 (iv)); on the
   register only the series 7 pair has such a divisor.
5. **A remainder discarded twice: the reading's weight at the relative
   speed.** `nature_beam.py:2057` (the grain, `(G abs(p_a)) mod D_a` per
   interval) and `2142` (the per-direction floor). The rule leaves the code
   with the crossing rule (record 158); until then `acc_flow` owns the
   second on the branch and the first is a declared grain.
6. **A history re-priced: the turn by momentum under `action`.**
   `engine.py:644`. Ordered to join the counts (record 155, record 157).
   Its torus form: `acc_action += abs(p_a) N` at every Link stepped on the
   axis, the carry per h into the phase; and since a lost or refused step
   crosses no Link, it adds nothing (today `k0` counts it and the floor's
   increment at that k is skipped for ever: a second discard inside the
   first).
7. **An event dropped: the coincident fire on a later axis.**
   `engine.py:552-568`. Two drives reaching their walls in one
   self-creation make one Link; the second's D is subtracted and its Link
   never crossed. The torus form keeps one Link per interval and loses
   nothing: a later axis whose drive is at or beyond its wall in an
   interval that already stepped is NOT advanced past the wall (its
   `by_drive` is not called, or its D is added back), so it fires at the
   next self-creation. What moves: only bodies whose momentum has two
   nonzero components with coincident fires (series D, H, the diagonal
   stars of G2, the kicked deuteron); every body on an axis is
   byte-identical. To be pinned before any run.
8. **An event dropped: the refused step under `read` and `pass`.**
   `engine.py:630-634`, `_contact` `735-740`. The drive paid its D and the
   body did not move; nothing was handed. Under `measure` (the keys' own
   rule) the component is handed over and the drive's residual stays, the
   torus form; under `read` or `pass` the Link's distance is lost per
   attempt. The torus form: add D back to the drive on a refused step
   whose rule hands nothing (the body keeps pressing, as its momentum
   does). Registered worlds under `read`/`pass` contacts: the pushed-body
   worlds where a contact is declared `read` on a paid family (none on the
   gate set by the default; to be listed by the implementer from the
   worlds' `contact` keys).
9. **A rounding per interval: the meeting's register.** `meeting.py:232`,
   `adv = (abs(t) + Q // 2) // Q`. The crowd met is rounded to whole units
   of Q every interval and the rest dropped. The torus form: `acc += abs(t)`
   on `Z_{N Q}` (the phase in units of `1 / Q`), the carry k per `N Q`; the
   same phase to within one grain at every interval and exact in the sum.
   Under the key only (`meeting-v1`, off by default; series K under the
   meeting is the registered world).
10. **A root at run time: the meeting's `abs(t) = isqrt(t . t)`.**
    `meeting.py:354-358`. The one non-rational function evaluated on the
    lattice per interval; its fractional part is discarded. It is a
    declared rounding of the same kind as `u_d` and `T_d` but taken per
    interval on a varying t, so its discards do not telescope. No torus
    form removes it while the phase counts `abs(t)`; if the phase counted
    `t . t` (a bilinear form) against the wall `(k Q)^2` by a comparison
    ladder, the root would leave: a change of the meeting's law, for the
    owner, not ordered here.
11. **A branch on a name: the table's verbs and the contact's.**
    `nature_beam.py:3104, 3262, 3308, 3456`; `engine.py:735-739`;
    `world.py:743-755` (the default from the quantum). Record 155 (5)
    orders the verbs derived from the families' keys. As built the default
    is already derived (`free` gives `read`, paid gives `measure`) and a
    declared entry overrides it: the branch is on a declared word, a
    world declaration; what (5) removes is the word, not the operation.
12. **A remainder on the host's books: the push by share.**
    `nature_beam.py:853` and the `remainder` lines. Record 155 (3) orders
    the leftover onto the giver's record. The torus form: per (record,
    axis) `acc_share += label x amount`, the carry per m the push, the
    residue on the row's record (it travels with the record, as u does).
13. **A count dropped by a gate: the lamp's stalled or windowed
    self-creation.** `nature_beam.py:3746-3760`, `3799`. Declared on the
    branch (note 41 (iii)): a window is a gate on the clock's phase, not a
    queue. Listed; the owner's declaration stands.
14. **Declared roundings, once, at the click or at load, and one option:**
    the nearest step of a pointer (`nature_beam.py:967-999`, the phase
    returned); the rung at the nearest integer (`amplitude.py:192`, the
    comparison form on the branch); C, S, the half-angle tables, `u_d`,
    `T_d` (at load); the `beam` reading's greedy pairing
    (`nature_beam.py:2846-2880`, a declared option). And **a floor at an
    arrival**: the click reads a row's phase at the whole age of its last
    Link (`nature_beam.py:2634`, `3043`), while the exact time of that Link
    is `made x T_d / (S_1 Q)` intervals, a rational the Manhattan
    accumulator's residue holds (section 1.2, step 1); the exact phase at
    the click, one floor of `(n / d) x made x T_d / (S_1 Q)` on the table,
    is TWO_SLITS.md section 2 (record 156), and it is a reading of the
    row's own accumulators, no new field.

### 1.4 The check against the register

The flight's accumulator form (one Manhattan accumulator started at `T_d`,
gaining `2 S_1 Q`, carrying at `2 T_d`; three deficit accumulators carrying
`S_1` from the largest) reproduces `m(tau)` and the Bresenham line integer
by integer on `(1,0,0)`, `(1,1,0)`, `(1,1,1)`, `(3,1,0)`, `(2,1,0)`,
`(5,-3,2)` and `(44,7,0)` over 600 intervals (the arithmetic check of this
section, on the formulas alone), and record 144's cone: at age 29, `m = 17`
Links on the axis (`T = 110`) and `24` on the plane diagonal (`T = 156`),
the registered arrival of both rows at age 29. The per-axis accumulator that
record 155 (2) names ("the flight table as the position's accumulator per
axis") is NOT this form: on `(1,1,0)` two independent axis accumulators at
the rate `64 / 156` fire at the same intervals (2, 4, 7, 9, ...), two Links
in one interval, and the sum of the per-axis floors at age 29 is 22, not
24. The torus form of the flight is the one above: one count of Manhattan
steps and the line's deficits, which the age holds whole. The implementer
retiring the table keeps the age and computes the step from it, or carries
the two accumulators; either is bit-identical, the per-axis form is not.

The rest of the inventory is checked by what the register already shows:
every rule marked a torus operation replays byte-identical on the register
(notes 33 (1) to (4): the four unifications changed no integer); every rule
marked **NOT** as a discarded remainder is exactly the set the fraction-free
branch moved (record 154: 103 worlds moved, every lamp world and every crowd
on a fan; 82 identical, the constant-rate worlds), which is FORM.md section
1's theorem read off the register: the counts whose rate never changed are
identical under the two forms, the others are not. Items 7 and 8 have no
registered integer of their own yet; their pins are the orbit worlds (D, H)
and the diagonal stars (G2), to be re-read once when the fix lands.

### 1.5 The verdict of target 1

**Reached** for the audit: every rule of `beam-v1` on `main` is one of the
six operations, or a declared rounding at load or at the click, except the
fourteen items of section 1.3, of which six are ordered (1 to 6, the
fraction-free branch and records 155, 157, 158), four are this inventory's
findings for the implementer (7 to 10: two dropped events at the step, the
meeting's per-interval rounding and its root), one is a declared word (11),
one a remainder on the wrong owner already ordered (12), one a declared gate
(13), and one the list of the declared roundings with the floor at the
arrival (14). The one correction to the Boss's statement of the law: the
phase of a row in flight is a point of `Z_N` on the record and of `Z_{N d}`
only through the age (nothing is discarded, since the rate is constant);
and the flight is not a per-axis accumulator but one Manhattan accumulator
with a comparison ladder on the axes' deficits.

## 2. Doppler from the crossing rule: 1 + v/c and 1 - v/c on the axis, exactly 1 on the transverse, and the Manhattan flux on a fan direction

**The rule derived from** (record 158, the physicist's design, not yet
built; until it lands the statement of the record is the rule): a row and
a body meet ONCE, at the crossing of their world lines. A body at rest
meets a row when the row arrives at its Node (the law as built,
`nature_beam.py:2741`); a body stepping from O into X along the signed
axis unit e meets, in the interval of the step, the rows that crossed its
own Link the other way (C1) and the rows resident at X moving against it
(C2, `u . e < 0`), and does not meet the rows moving with it, the rows
behind it on its Link, or one interval later the rows it met at O. The
operations: the walk of the rows (T, section 1.2 step 1), the body's
step by the drive (T/D), and the meeting as a comparison of two records'
last Links (D). The count is an integer per interval; nothing is weighted.

**What main does** (record 153, the engine as built, `engine.py:378-401`:
the reading before the step, the arrivals only): a reader stepping one
Link per k intervals toward a lamp at rest reads k rows per k intervals,
and k away; the reader's Doppler is absent. That is the registered
state; the derivation below is of the rule of record 158, and its check
is the record's own encounter counts and the doppler bar's registered
rates, whose limit the count reproduces.

### 2.1 The stream and the speed of light on the axis

A lamp at rest releases one row per interval on the heading `(1, 0, 0)`.
The row of age tau is at `m(tau) = (2 tau Q + T) // (2 T)` Links with
`T = T_d = isqrt(3 Q^2) = 110`, so the rows advance `c = Q / T = 32 / 55`
Links per interval (0.5818; `1 / sqrt 3` = 0.5774, the isqrt's rounding
of 110.85 to 110, within 0.8 %) and stand `c` Links apart: the stream's
density is `n = T / Q = 55 / 32` rows per Link (record 153's 1.72), and a
reader at rest meets `n c = 1` row per interval, the lamp's rate. As Q
grows, `Q / T_d -> 1 / sqrt 3` for every direction (the flight table's
limit, BEAM_LAW section 3: within 1.35 % at Q = 64 on every direction of
the table); the speed of light of the limit is `1 / sqrt 3` Links per
interval in the lattice's frame, isotropic.

A body of content M with the momentum p on the axis steps one Link per
`D / abs(p)` self-creations, `D = Q S M + abs(p)` (`engine.py:85-116`), so
its speed is `v = abs(p) / (Q S M + abs(p))` Links per interval, a
rational below 1; record 153's reader has `M = 21 x 2^16`, `abs(p) = 7 x
2^22`, `Q S M = 21 x 2^22`, `D = 28 x 2^22`, `v = 1 / 4` exactly, and `v /
c = 55 / 128 = 0.4297`.

### 2.2 The encounter count and its limit: the receiver's Doppler

The rows' world lines are the staircases `x_j(t) = x_0 - m(t - j)`, one
per released row j; the body's is the staircase `x_b(t) = x_b0 + s
floor(t / k)`, s = +1 toward the lamp. The rule counts every crossing of a
row's staircase with the body's once. Over an interval of length tau the
body sweeps `v tau` Links and the stream advances `c tau` Links, so the
rows whose lines cross the body's are those within `(c + s v) tau` Links
of it: the count is

    E(tau) = n (c + s v) tau + O(1) = (1 + s v / c) tau + O(1),

the O(1) the boundary row (a row exactly at a wall of the swept
interval), never more than one. Over a whole number of Links of the
body's path the count is exact: in `L k` intervals the body sweeps L Links
and the count is `L k + n L` exactly when `n L` is whole. The rate per
interval in the limit of many intervals is

    1 + v / c   toward the lamp,      1 - v / c   away from it,

the receiver's Doppler of a source at rest in the lattice's frame, with c
the table's speed on the axis. **Reached**, exactly (the rounding never
exceeds one row, and vanishes over whole Links).

**The registered checks** (record 158's proof of the rule on the
experimenter's streams of record 153, the rows' and the body's positions
as the engine made them, the count by the rule):

| Stream, body | The formula | The count of record 158 | Difference |
| --- | --- | --- | --- |
| toward, k = 4, 32 intervals | `32 (1 + 55 / 128) = 183 / 4 = 45.75` | 45 | the boundary row |
| toward, k = 8, 48 intervals | `48 (1 + 55 / 256) = 933 / 16 = 58.31` | 58 | the boundary row |
| away, k = 4, 32 intervals | `32 (1 - 55 / 128) = 73 / 4 = 18.25` | 19 | the boundary row |
| away, k = 8, 48 intervals | `48 (1 - 55 / 256) = 603 / 16 = 37.69` | 38 | the boundary row |
| toward, k = 4, 32 Links (128 intervals) | `128 + 55 = 183` | 183 | exact |
| toward, k = 8, 32 Links (256 intervals) | `256 + 55 = 311` | 311 | exact |
| at rest, 48 intervals | 48 | 48 | exact |

The weight that doppler-v1 supplied in place of the missing count (record
153: the flux pair `374784 / 262144` at k = 4) is `1 + 55 / 128 = 183 /
128` exactly, `262144 x 183 / 128 = 374784`: the key was the limit of the
count, put on the flow as a factor. The doppler bar of `tests/test_doppler.py`
(b), FORM.md's map, registers the same limit at five speeds: over 200
intervals the receding body at `v = 0.30` reads the weighted rate `200 (1
- 0.30 x 55 / 32) = 96.875` (the register's 96.9; 6204 / 64 = 96.94 with
the speed's grain), at 0.45 `45.31` (45.3), the approaching body at 0.30
`303.125` (303.1), the co-moving body at `v = c` 0 (0), the outrunning
body at 0.75 `200 (0.75 x 55 / 32 - 1) = 57.81` (57.8): every one is
`abs(1 - v / c)` times the rest rate, the encounter count's limit, and
under the crossing rule these become counts of 97, 45, 303, 0 and 58 rows
within one (record 158's tests (a) to (e), pinned there).

### 2.3 The transverse motion

A body stepping on y through a stream on x meets, at its step, no row of
the destination: the rows' `u . e_y` is 0, neither against nor with, and
the rule counts only arrivals (C2 needs `u . e < 0`). Its count is the
rest rate, exactly 1 per interval at every v (record 158: "transverse
exactly 1"). In the continuum this is the classical transverse Doppler, 1:
the rows a point meets per unit time do not change when it moves along
the fronts. Nature's transverse Doppler is `1 / sqrt(1 - v^2 / c^2)` (Ives
and Stilwell 1938): at `v = 0.30 c` the factor 1.048, at the G2 stars'
`v / c = 0.057 .. 0.27` from 1.002 to 1.038. **Different law** at order
`v^2 / c^2`: the lattice's transverse count is 1, and nothing in the six
operations carries a body's speed into its clock or its reading (target
4).

### 2.4 The fan direction: the Manhattan flux against the Euclidean one

Let the stream be on a direction `D = (a, b, c_z)` of the table, released
one row per interval, and let the body move on x at v. A row of D
advances `S_1 Q / T_d` Manhattan steps per interval, `a / S_1` of them on
x: its velocity is `(Q / T_d) D` per axis (GRAIN.md section 2). In a world
of full extent the rows of a plane stream occupy the Nodes at a density
`n` per Node, and a Node at rest is entered by rows through its Ports at
the rate `n x (S_1 Q / T_d)` per interval (each Manhattan step of a row is
an arrival at some Node; each Node receives its share); the body stepping
into X meets the n rows resident there (all against it, `u_x < 0`) once
per step, `n v` per interval more, and the rule's C1 and C3 clauses make
no row count twice or drop. In the limit the ratio of the moving count to
the rest count is

    1 + v x T_d / (Q S_1)   (the crossing rule: the Manhattan flux)

against the continuum flux of a plane wave whose wave vector is along D
(GRAIN.md section 2, the flux `1 - v . c_d / abs(c_d)^2`):

    1 + v x a T_d / (Q abs(D)^2)   (the Euclidean flux).

The two Doppler terms differ by the factor `abs(D)^2 / (a S_1)`: 1 on
every heading and on every direction whose nonzero components are all
+-1 (`abs(D)^2 = S_1` and `a = 1`: the face and the space diagonals, for a
body on any of their axes), and not 1 elsewhere: 5/6 on `(2, 1, 0)` and
`(3, 1, 0)` for a body on x (the count under-reads the Euclidean Doppler
by 17 %), 5/3 on `(1, 2, 0)` and 5/2 on `(1, 3, 0)` for a body on x (the
count over-reads it), 1985/2244 on the screen's `(44, 7, 0)`. The reason
is the Node: a lattice reader is a cube whose faces are its six Ports, so
the rows it meets per interval are the Manhattan flux `n (abs(c_x) +
abs(c_y) + abs(c_z))` at rest and `n (abs(c_x) + v + abs(c_y) + abs(c_z))`
in motion, while a continuum point reader in a plane wave meets the fronts
at the Euclidean rate `n (abs(c) + v cos theta)`. **Different law** on a
general fan direction, stated: the emergent Doppler on the lattice is `1 +
v / c_1` with `c_1 = S_1 Q / T_d` the direction's Manhattan speed (0.82 on
the face diagonal), not `1 + v cos theta / abs(c)`; equal to it on the
headings and the diagonals. As Q grows the ratio `abs(D)^2 / (a S_1)`
does not change: this is a limit of the lattice, not of the resolution
(a fan of every direction, target 7, averages it over the fan's
directions, where `sum_D (a S_1) / abs(D)^2` decides the mean).

**Record 158's two numbers.** The design names `1 + 2.44 / k` head-on on
a face diagonal against `1 + 1.22 / k`. Both are rationals of the table:
`2.44 = T_d / Q = 156 / 64` and `1.22 = T_d / (Q S_1) = 156 / 128` on
`(1, 1, 0)`. The second is the formula above in a world of full extent
(the Manhattan and the Euclidean flux coincide on the face diagonal, the
ratio 1). The first is the same count on a world whose y axis has the
extent 1: there a row's y-step is a self-Link (`game_board.py:48-49`) that
crosses no world line and is no arrival, so the stream's Manhattan speed
on the real axes is `S_1' Q / T_d` with `S_1' = 1`, `c_1 = 64 / 156 =
0.41` on x, the rows stand `2.44` per Link and the count reads `1 + v x
156 / 64`: the correct Doppler of a stream that moves at 0.41 along the
bar, which is what a diagonal direction is on that bar. So the deviation
of record 158 is the bar's geometry, not a departure of the count; on the
plane the count and the flux agree there. One fact of the engine for the
implementer, found on the way: on `main` a self-Link step marks an
arrival (`nature_beam.py:2399, 2412`: `moved` is true and the Node is the
same), so a body at rest on a periodic axis of extent 1 reads a row with a
component on that axis again at every such step; the crossing rule's
"once" removes it (a self-Link crosses no line), and the rule's tests on
the bar should pin the rest rate at 1 per interval, not `S_1 / S_1'`.

### 2.5 The source's Doppler: a moving lamp

A lamp of content M thrown at v releases one row per self-creation, and
its clock ticks at every interval whether or not it steps (`engine.py:
418-451`; HYPOTHESES entry 21: the rate is one at every speed). Between
two releases the lamp moves v Links on average and the row moves c, so
the rows stand `c - v` Links apart ahead of the lamp and `c + v` behind
it; a reader at rest meets them at the rate `c / (c - v) = 1 / (1 - v / c)`
ahead and `1 / (1 + v / c)` behind: the classical source Doppler, `1 + z =
1 + v / c` for a receding lamp, exactly in the limit (the staircase of the
lamp's steps is a jitter of at most one Link in the spacing, one row in
the count over a period). **Reached.** The registered check: series G2's
`coasting_none` (the stars thrown from one point, gravity off; the
hubble_stars README's per-star table), where the detector's z per star is
`1 + z = (1 + k)(1 + v / c)` with k = 0: s_my1 declared `v / c = 0.1146`
reads z = 0.1146, s_pz2 0.2483 reads 0.2478, s_mz2 0.2674 reads 0.2636,
s_px1 0.0573 reads 0.0611, every star within the grain of the digital
step (0.003 in z, the README's), and the crowd fits the Milne form with
`q = 0.000`, `H (t_0 + T_0) = 1.000` (record 138 and the README).

### 2.6 The two Doppler formulas and nature's one

The lattice gives the receiver's `1 + v / c` (2.2) and the source's `1 /
(1 - v / c)` (2.5) as two different laws, as the classical ether did;
they agree to first order in `v / c` and differ at second: at `v / c =
0.5156` (the bar's approaching body) 1.516 against 2.065. Nature has one
formula for both, `sqrt((1 + v / c) / (1 - v / c))` (1.769 at that speed),
which lies between them, because in nature only the relative velocity
exists. **Different law** at order `v^2 / c^2`, the lattice's frame
preferred: the flight table's c is isotropic in the lattice's frame and
in no other, and the crossing rule counts in that frame. Whether the
limit has any Lorentz-like symmetry, and what a moving clock reads, is
target 4; the answer here is what the count says: no factor of `gamma`
enters any of the six operations, so none appears in the limit.

### 2.7 The verdict of target 2

| Formula | Verdict | The place |
| --- | --- | --- |
| The receiver's Doppler `1 +- v / c` on the axis | **reached** under the crossing rule (record 158), exact over whole Links and within one row otherwise; on `main` **not reached** (k per k, record 153) | `c = Q / T_d`, the table's rational; the boundary row |
| The transverse Doppler | **different law**: exactly 1 (the classical value); nature's `gamma` absent at order `v^2 / c^2` | no operation carries a speed into a reading |
| A fan direction | **different law**: the Manhattan flux `1 + v T_d / (Q S_1)` in place of the Euclidean `1 + v a T_d / (Q abs(D)^2)`; equal on the headings and the diagonals, off by `abs(D)^2 / (a S_1)` elsewhere; record 158's 2.44 and 1.22 are `156 / 64` (a bar of extent 1) and `156 / 128` (the plane) | the Node is a cube with six Ports |
| The source's Doppler `1 / (1 -+ v / c)` | **reached** (the classical law; G2 `coasting_none`, z = v / c per star within the grain) | the lamp's clock at rate 1 |
| The relativistic Doppler | **different law** at `v^2 / c^2`: two formulas, receiver's and source's, in place of nature's one | the lattice's frame |

## 3. Newton and Coulomb from the bilinear coupling and the flow's moments

**The operations.** The free release (T): a body of content M_B holding a
free family releases `by_clock(age, M_B n, d)` units on EVERY declared
direction at each self-creation (`nature_beam.py:3546-3566`: the count
is per direction, so a fan of K directions releases `K M_B n / d` per
interval, the flux q); the walk (T, section 1.2); the reading (B): the
label flow `V = sum amount x u_d` of the rows arriving at the reader's
Node, `abs(u_d) = Q` within 1.35 % on every direction; the coupling (B):
per axis `push_A = M_A (rho_A rho_B - 1) V` (`push_form`,
`nature_beam.py:2147-2221`; the gravity column `-M_A V`, the charge column
`+rho_A rho_B M_A V`, every column a signed value per unit of content
declared per family, BEAM_LAW note 31); the momentum (T) `p_A += push`;
the step (D) one Link per `D / abs(p)` self-creations, `D = Q S M_A +
abs(p)`. The register: series C (`examples/events/coupling/`, the
plane 121 x 121 x 1, the source of content 2^24 on the six headings at
`release` [1, 128], `q = 6 x 2^17 = 786432` per interval in four in-plane
beams of `3 x 2^16`; EXPERIMENTS "C, the couplings under the Beam Law")
and its item 7, series 7 (two free families with the charges [1, 2] and
[2, 1] per unit of content).

### 3.1 Gauss's law, exact

The walk is a translation: a row released inside a closed surface crosses
it once and never returns (no collision acts on a fan or on lone beams,
BEAM_LAW section 4), so after the front has passed, the amount crossing
any closed surface per interval equals the release inside it, exactly:

    sum over the surface's Ports of the amount crossed = q.

**Reached exactly.** Registered: series C item 5, the flux through the
square of half-width h over q is `1.0000` at h = 4, 8, 12, 20, 40 and
the escape through the faces `1.0000 q` (the tool sums the Links crossed,
`per_port`, the walk's own diagnostic).

### 3.2 The far field: a beam does not dilute, a shell does

On a beam the flow per Node is `amount x u_d`, the same at every Node of
the digital line: the field along a beam is `1 / r^0`, and off every beam
it is 0 (item 5P, registered: the axial count `q / 4` per interval
constant with r; item 3: a probe off both axes reads nothing). The
inverse square is the density of beams over a shell. A shell at the
distance r holds `N(r)` Nodes (on the plane the ring `abs(dist - r) <
1/2`; in space the shell), and the K beams cross it at K of them, so the
shell mean of the flow is `q Q / N(r)` per Node, and the mean over the
shell of what a body reads is

    <V>(r) = q Q / N(r) -> q Q / (2 pi r)  on the plane,  q Q / (4 pi r^2)  in space,

as `N(r) -> 2 pi r` and `4 pi r^2`. The departure at finite r is the
lattice's count of Nodes on a shell, Gauss's circle problem: `N(r) = 2 pi
r + O(r^theta)` with `theta <= 131 / 208` (Huxley), so the shell mean's
relative ripple vanishes as `r^(theta - 1)`. **Reached in the shell
mean**, with the ripple named.

**The registered check** (series C item 5, world 5, the nine radii; the
tool's ring is `abs(dist - r) < 0.5`, `engine.py:1120-1143`): the
register's `count x r / q` and `flow x 2 pi r / q` are `r / N(r)` and `2
pi r / N(r)` to every printed digit, N(r) counted on the lattice
(the arithmetic check of this section):

| r | N(r) | `r / N(r)` | registered `count x r / q` | `2 pi r / N(r)` | registered `flow x 2 pi r / q` |
| --- | --- | --- | --- | --- | --- |
| 4 | 32 | 0.125 | 0.125 | 0.785 | 0.785 |
| 6 | 40 | 0.150 | 0.150 | 0.942 | 0.942 |
| 8 | 48 | 0.167 | 0.167 | 1.047 | 1.047 |
| 12 | 68 | 0.176 | 0.176 | 1.109 | 1.109 |
| 16 | 112 | 0.143 | 0.143 | 0.898 | 0.898 |
| 20 | 112 | 0.179 | 0.179 | 1.122 | 1.122 |
| 24 | 144 | 0.167 | 0.167 | 1.047 | 1.047 |
| 30 | 200 | 0.150 | 0.150 | 0.942 | 0.942 |
| 40 | 264 | 0.152 | 0.152 | 0.952 | 0.952 |

The registered slope `-0.944` of the count against r over the nine radii
is the log-log slope of `1 / N(r)` over them (`r / N(r)` fits `+0.056`);
the design's `+-10 %` was missed at r = 12, 16, 20 because `N(16) = N(20)
= 112`: the ring's Node count, not the law. In the limit `<count x r /
q> -> 1 / (2 pi) = 0.159`, which the nine readings straddle (0.125 to
0.179). The verdict of series C ("the far-field readings follow the
GameBoard ring's Node count and not r") is this identity read off the
register.

**Per Node, not in the mean.** A single body at r reads a beam or nothing
(item 6: "a Node reads one ray or none"), so the inverse square on ONE
Node exists only in the limit of every direction, K -> infinity at fixed
r, when every Node of the shell lies on about `K / N(r)` digital lines
and reads their sum: `q Q / (4 pi r^2)` again (the Huygens fan of target
7). With a fan declared as a cube of directions (every primitive vector
with components in -P .. P) that limit is not isotropic: the density of
directions per solid angle is the cube's, `3^(3/2) = 5.2` times larger
toward a corner than toward a face centre in the limit (3.0 at P = 8 and
3.5 at P = 16 within 11.5 degrees of the corner against the face, the
arithmetic check), a cubic anisotropy of the DECLARATION, absent for a
fan declared within a ball `abs(D) <= P`. The lattice's own anisotropy is
`abs(u_d)` within 1.35 % of Q (the isqrt of `unit_label`), vanishing as
Q grows.

### 3.3 Newton's law and G's place

A body A of content M_A at the mean flow `<V>` takes per interval `push =
-M_A <V>` (label units) and its speed is `v = p / (Q S M_A + p)`; for `p
<< Q S M_A` the acceleration is `a = push / (Q S M_A)` Links per
interval^2, so

    a = - G M_B / r^2,     G = K (n / d) / (4 pi S)     (space; on the plane a = -G' M_B / r, G' = K (n / d) / (2 pi S)),

in Links^3 per unit of content per interval^2: G is the source's release
rate per unit of content per direction `n / d`, times the number of
directions K, over `4 pi` and the world's width S. Nothing of A enters: the
equivalence principle is exact (item 1 registered: `push_m = m x push_1`
record by record for m = 1, 4, 16, and the step rule divides by M_A). The
third law at rest is exact to the apportioning's grain (item 2: the two
sources' momenta `9612145197056` and `-9612088573952`, the ratio 1.0000).
**Reached in the shell mean, G named**; per Node in the limit of every
direction. Two departures from Newton's law as written, both stated: the
field is retarded at c = Q / T_d (item 4: the front at r arrives at the
tick `1 + m^-1(r)`: 8, 11, 14, 21, 28, 35, 42, 52, 69 at r = 4 .. 40),
so the limit is the retarded inverse square and not action at a
distance; and the speed the push builds saturates at `v = p / (Q S M +
p) < 1` Link per interval, above the flight's `c = 0.58`: a body can
outrun its own field's rows (the bar of section 2.2, 0.75 registered), a
limit of the law (target 4).

### 3.4 Coulomb's law and the one constant

The charge column adds `+rho_A rho_B M_A V` per axis. With `q_A = rho_A
M_A` and `q_B = rho_B M_B` the charges (rho the declared charge per unit of
content), and `<V>` proportional to M_B as above, the electric push in the
shell mean is

    push_e = q_A q_B x K (n / d) Q / (4 pi r^2),    a_e = (q_A q_B / M_A) x G / r^2,

Coulomb's inverse square with the SAME constant as gravity, `k_C = G` in
the law's units (charge in units of content), repulsive for like signs
(V points away from the source; `+V` pushes A outward, `-V` inward). The
ratio of the two forces on one body is `-rho_A rho_B = -q_A q_B / (M_A
M_B)` at every r. **Reached**, exactly in form. Registered: item 7's
electric / gravity `-1` and `-1 / 4` exactly (the probes of charge [2, 1]
on content 1 and [1, 2] on content 4 against the source's [1, 2] on
2^24), and series 7's coefficients `M_A (rho_A rho_B - 1)` read integer
by integer on the `read` records: 0 in `7_pp` and `7_mm` (like charges of
`rho_A rho_B = 1`: the electric push cancels the gravity exactly),
`-2^25` and `-2` in `7_mp` and `7_pm` (the source of 2^24 and the probe of
1 at `rho_A rho_B = -1`), `-12582912 = -(3/4) 2^24` and `-3` in `7_pp_m4`
(`rho_A rho_B = 1/4`), `-2^24` and `-1` in `7_00`. Nature's ratio for two
protons, `e^2 / (4 pi eps_0 G m_p^2) = 1.24 x 10^36`, is `rho_p^2` here:
`rho_p = 1.1 x 10^18` units of charge per unit of content (the electron
`2.0 x 10^21`); the hierarchy is the declared rho, not a formula of the
law (record 106: the masses and charges are the initialisation).

### 3.5 What departs, and where

1. The field along a beam does not fall: `1 / r^0` on a digital line, 0
   off it; the inverse square is a shell mean, or the limit of every
   direction (3.2).
2. The shell's Node count `N(r)` against `2 pi r` and `4 pi r^2`: the
   Gauss circle problem, `O(r^theta)`, the registered nine ring readings
   exactly (3.2).
3. A cube fan's `3^(3/2)` corner-to-face density: the declaration's, not
   the law's (3.2).
4. `abs(u_d)` within 1.35 % of Q: the isqrt at load, vanishing as Q grows.
5. The field retarded at `c = Q / T_d`, and the body's speed capped at 1
   above c (3.3).
6. The clock's count reads the presence, which on a beam does not fall
   with r (item 6: the clock on the axis owed the beam's presence at
   every r); the potential's `1 / r` is the age moment's reading (BEAM_LAW
   note 25, series E), target 5.
7. The charge column's floor per interval where `rho_A rho_B` is not whole
   (section 1.3 item 4): on gravity the divisor is 1 and Newton's push is
   exact in integers at every interval; Coulomb's with a fractional rho
   is exact in the sum over a period only under the accumulator (the
   branch).

### 3.6 The verdict of target 3

| Formula | Verdict | The constant or the place |
| --- | --- | --- |
| Gauss's law | **reached** exactly (the walk a translation; the flux 1.0000 at every h) | none |
| The inverse square | **reached** in the shell mean, `<V> = q Q / N(r)`, `N(r) -> 4 pi r^2`; per Node only in the limit of every direction; the nine ring readings of series C are `r / N(r)` and `2 pi r / N(r)` exactly | the Gauss circle problem's ripple `r^(theta - 1)`; a cube fan's `3^(3/2)` |
| Newton's `a = -G M / r^2` | **reached** in the shell mean with the equivalence principle exact and the third law exact at rest; retarded at c; the speed capped at 1 | `G = K (n / d) / (4 pi S)` |
| Coulomb's `F = k q_A q_B / r^2` | **reached** in form, `k_C = G`, the ratio `-rho_A rho_B` exact (item 7, series 7) | the hierarchy `rho_p^2 = 1.24 x 10^36` a declaration |

## 4. Special relativity: the symmetry of the continuum limit

**The question.** The flight table's c is isotropic in the lattice's frame
(section 2.1: `Q / T_d -> 1 / sqrt 3` on every direction). What does a
moving body read, what is a moving clock's rate, and does the limit have
a Lorentz-like group or a preferred frame? The operations that answer
it: the walk (T) for the rows, the crossing count (D) for what a moving
body reads (section 2), the step (T/D) for a body's speed, the clock's
frame (`engine.py:418-451`: the age advances at every interval in which
nothing is owed, whether or not the body steps) and the owed count (D)
for its rate.

### 4.1 The rows alone: the wave equation's symmetry returns

A family's rows on a fan of every direction, each advancing `Q / T_d ->
1 / sqrt 3` Links per interval on its line with the phase `k x - omega t`
along it (`phase_per_link` per Link, or the pair form per interval:
`omega = c k` for every rate, the paper's second limit), are in the limit
the plane waves of the massless wave equation with one speed c. That
equation's symmetry group is the Lorentz group with that c: for the free
rows the limit is Lorentz-covariant, a property of the equation the
lattice converges to, not a rule of the lattice. What the lattice adds
at finite Q: the isqrt's rounding of `T_d` per direction (within 1.35 %,
one step in 234 on the cone, record 156), the digital line's staircase
(the arrival at a whole interval), and the cubic group: the operator
commutes with the 48 signed axis permutations up to the ties named in
FORM.md section 3 (the collision's Port order, the apportioning's, the
axes' order x, y, z), and with the lattice's translations and the
interval's; no boost is among its symmetries. Registered: the cone
(record 144), both rows at age 29 on the axis (17 Links, `T = 110`) and on
the plane diagonal (24 Links, `T = 156`) at the same Euclidean distance
within one percent, the isotropic front. **Reached** for the rows: `omega
= c k`, the isotropic light cone, and with them the Lorentz symmetry of
the free wave's limit.

### 4.2 A moving body: what it reads

A body moving at v through a stream reads, under the crossing rule, the
encounter count of section 2: `1 + v / c` head-on, `1 - v / c` co-moving,
1 transverse. The rows' speed relative to a moving reader is therefore `c
-+ v`, not c: the reader's count is Galilean. In an ISOTROPIC crowd (rows
of every direction at equal density, the ether of the six-heading or the
fan release) the two senses cancel exactly for `v` below the rows' speed
on the body's axis: a direction against the motion gives `n (c_1 + v)`,
the same direction with it gives `n (c_1 - v)` (the rows overtake the body
from behind), the sum `2 n c_1` at every v below `c_1`. So a body moving
through an isotropic crowd reads the rest count exactly, to every order in
v below `c_1`: no two-way measurement inside the crowd detects the
motion (the lattice's Michelson-Morley null, exact), while a one-way
count of one stream detects it at first order (section 2). The preferred
frame is measurable by a one-way count and by nothing two-way.

### 4.3 A moving clock: the rate is one at every speed

A body's clock is the count of its self-creations; `_frame_all` advances
it at every interval in which nothing is owed, and `_move` steps the body
after it, so a body thrown at any v ticks at the rate of one at rest
(HYPOTHESES entry 21, the physicist's finding; TERMINOLOGY corrected).
The only slowing of the law is the owed count, `owed = by_clock(age, k n,
d)` with k the crowd the clock reads (the presence, or the age moment),
`engine.py:475-485`: a clock slows by what it reads, `1 / (1 + k n / d)`,
never by its speed. Nature's moving clock runs at `sqrt(1 - v^2 / c^2)`.
**Different law**: the moving clock's factor is 1. The registered check
is series G2's `coasting_none` (section 2.5): the star's light carries `1
+ z = (1 + k)(1 + v / c)` with `k = 0` (no crowd, no slowing); had the
lamp's clock carried nature's `gamma`, the fastest coasting star (s_mz2,
`v / c = 0.2674`, `gamma = 1.0378`) would read `z = 1.0378 x 1.2674 - 1 =
0.315`, and the register reads `0.2636` against the classical `0.2674`,
within the grain 0.003 and fifty grains from the relativistic value. The
absence of `gamma` is registered, not only derived. Under the crossing
rule a moving clock inside a crowd reads a count that depends on its
direction of motion relative to the crowd (record 158: in the `_scalar`
and `_age` worlds the count falls by `v / c` for a star moving with its
light), an anisotropic slowing by the crowd's frame: a preferred frame
again, the crowd's.

### 4.4 A body's speed: the step rule's dispersion

The step rule gives `v = p / (Q S M + p)` (label units; `engine.py:85-116`,
`world.py:447-456`): the speed is a rational function of the momentum
that saturates at 1 Link per interval. Relativity's is `v = p c /
sqrt(m^2 c^2 + p^2)`, saturating at c. With `m = Q S M` as the mass and
the unit of speed the Link per interval:

| `p / m` | the lattice `p / (m + p)` | relativity `p / sqrt(m^2 + p^2)` |
| --- | --- | --- |
| 1 / 4 | 0.200 | 0.243 |
| 1 | 0.500 | 0.707 |
| 3 | 0.750 | 0.949 |
| 9 | 0.900 | 0.994 |

**Different law**: the lattice's dispersion is `v = p / (m + p)`, not
`p / sqrt(m^2 + p^2)`; both are `p / m` at small p (Newton, section 3.3)
and both saturate, the lattice's at the Link speed 1 and not at the
flight's `c = 1 / sqrt 3`. Two invariant speeds cannot share a Lorentz
group: the walk's bound 1 (one Link per interval for rows and bodies
alike) is the causal speed, and light's `1 / sqrt 3` is below it, so a
body of `p > 0.73 Q S M` outruns its own family's rows (the bar's
outrunning body at 0.75, section 2.2, registered). Nature's light is at
the causal bound; the lattice's is at `1 / sqrt 3` of it, the owner's
"phase velocity the wave on the mesh had" (BEAM_LAW section 3), so that
no direction crosses two Links in one interval.

### 4.5 What returns and what does not

| Formula | Verdict | The place |
| --- | --- | --- |
| The isotropic light cone, `omega = c k` | **reached** (the rows; the cone of record 144) | `c = 1 / sqrt 3` in the lattice's frame |
| Lorentz covariance of the free rows' limit | **reached** as the symmetry of the wave equation the rows converge to, not as a symmetry of the lattice (the cubic 48 and the translations only) | the ties of FORM.md section 3 break even the 48 |
| The invariance of c for a moving reader | **different law**: a moving reader counts `c -+ v` (Galilean); an isotropic crowd hides it two-way exactly, a one-way count shows it | the crossing count |
| The moving clock's `gamma` | **different law**: the rate is 1 at every v (HYPOTHESES 21); G2's fastest coasting star reads `z = 0.2636` where `gamma` would give 0.315 | the clock's frame; the only slowing is the crowd's |
| The dispersion `v(p)` | **different law**: `p / (m + p)` in place of `p / sqrt(m^2 + p^2)`; the cap 1 above c | the step rule |
| Velocity addition, `E = m c^2`, the mass of a moving body | **not reached**: no operation carries a body's speed into its content or its clock; content is invariant, the momentum unbounded | the law has no energy of motion (target 6 for the release's E = h f) |
| A preferred frame | the lattice's, and inside a crowd the crowd's: measurable one-way, hidden two-way | 4.2, 4.3 |

## 5. General relativity: the equation of the delay field

**What "held content delays the flight" is in beam-v1.** Nothing in
flight is delayed: a row moves by the flight table at one speed, blind to
the crowd (BEAM_LAW section 3; series K, registered: the mean age 89.40
in every world, the delta 0.00). What a crowd delays is a CLOCK: a body
reads at its Node the presence of every row of another number (or, on an
entry that reads `age`, the age moment) and owes `by_clock(age, k n, d)`
intervals before its next self-creation (`engine.py:475-485`; on the
branch the accumulator `acc_owed`), so its rate is `1 / (1 + k n / d)`.
Its push reads the flow of the same rows. The operations: the release
(T), the walk (T), the reading (B: the zeroth moment, the age moment, the
first moment), the owed count (D), the coupling (B). The register: series
E (`examples/events/redshift/`: an open 31^3 cube, a fixed source of
content 2^12 on the 290-direction fan, `q = 290` per interval, probes on
the shells r = 4 .. 14; the `scalar` world at `suspension` [1, 1], the
`age` world at [1, 2]), series K and K under the meeting
(`examples/events/lensing/`), series G2 (the deceleration q).

### 5.1 The two fields of one stream, and the equation they obey

Let a source release `q(t)` rows per interval on a fan of every direction
(the limit of section 3.2), each row moving at c and carrying its age.
The presence at the distance r at the time t is the rows dwelling there,

    P(x, t) = q(t - r / c) x dwell / (4 pi r^2)            (dwell = T_d / Q intervals per Link, 1.72 on a heading),

and the age moment is the presence times the age the rows carry, `r / c`
(each row's age at r is the light-travel time):

    A(x, t) = q(t - r / c) x dwell / (4 pi c r).

The presence is the retarded flux of a conserved stream, the age moment
is the retarded potential of the source: `f(t - r / c) / (4 pi r)` is the
retarded Green's function of the wave operator, so A obeys the
inhomogeneous scalar wave equation with the release as its source,

    (1 / c^2) d^2 A / dt^2 - Laplacian(A) = (dwell / c) q(t) delta(x),

and in the static limit Poisson's equation, `Laplacian(A) = -(dwell / c) q
delta(x)`, `A = (dwell q / (4 pi c)) / r`. The moments are sums over rows,
so the field of many sources is the sum of their fields (additive, note
25): the theory is linear. The flow the push reads is the stream's flux
vector, `V = (q Q / (4 pi r^2)) r_hat`, which is `-(Q c / dwell)
grad(A)` in the static case: the acceleration of a body is minus the
gradient of the age moment's field. **Reached**: the delay field obeys
Poisson's equation and, dynamically, the retarded scalar wave equation;
the push is its gradient. The registered check is series E: `k_s x r^2 =
41.5` (39.0 to 44.8 over r = 6 .. 14; the design's `q dwell / (4 pi) =
290 x 1.72 / 12.57 = 39.7`) and `k_a x r = 36.1` (33.1 to 39.2), their
ratio 0.870 against `sqrt 3 / 2 = 0.866` (the age at r is `r sqrt 3`
intervals, the `age` world's `[1, 2]` halving it): the presence M / r^2
and the age moment M / r from the same rays, "Einstein's pair from two
readings" (note 25), the ripple the shell's Node count as in section 3.2.

### 5.2 The clock: the gravitational redshift

A clock at the age moment `k_a = C M / r` (C the constant above times
`n / d`) runs at `1 / (1 + k_a)`. General relativity's clock at the
potential runs at `sqrt(1 - 2 G M / (r c^2)) = 1 - G M / (r c^2) - (1 /
2)(G M / (r c^2))^2 ...`. With `k_a = G M / (r c^2)` the two agree at
first order: the gravitational redshift between two clocks, `rate(r_1) /
rate(r_2) = 1 - k(r_1) + k(r_2)` at first order, is the `1 / r` law.
**Reached at first order.** At second order the lattice reads `1 - k +
k^2` against `1 - k - k^2 / 2`, and its rate never reaches 0 at a finite
k: **different law** in the strong field, no horizon (the crowd only
slows; nothing stops a clock). Registered: series E's rate ratios `rate(r)
/ rate(14) = 0.3453, 0.5015, 0.5701, 0.7227, 0.8215` at r = 4 .. 12
against the 1 / r law's `0.3627, 0.5162, 0.6548, 0.7805, 0.8951`: the
form is the law's (the nearer clock slower, the shift `1 / r - 1 / 14`),
inside at r = 6 and outside at 8, 10, 12 by the ripple of the shell mean
entering `(1 + k_14) / (1 + k_r)` whole, at a strong field (k = 2 .. 9),
where the first-order line fails as expected; the weak-field
confrontation (k << 1) is the follow-up the register names. The bound
clock's reading of record 123 (the lamp beside the nucleus, a deficit of
0.100 % in the count alone) is the same law at a small k.

### 5.3 Bodies: Newton's geodesics, retarded

A body's push reads the flow, `-M_A V`, and its speed the step rule: the
acceleration `-G M_B / r^2` of section 3.3 with the field retarded at c.
In the limit the body follows the geodesics of the Newtonian potential
`A`, not of a metric: no term of order `v^2 / c^2` or `(G M / r c^2)^2`
enters the push (the coupling is bilinear in the flow and the content,
nothing else), so the perihelion advance of general relativity (three
halves of the Newtonian potential's square in the orbit equation) has no
source here. **Reached** for Newton's motion; **not reached** for the
post-Newtonian terms. What the register shows of orbits (series D, record
131: the flat-curve period ratio 3.73 against 4, no orbit closed by D's
criterion) is the six-heading shell structure of section 3.2, not a
precession, and is not read here as either.

### 5.4 Light: no optical metric on main; the meeting's turn as a key

On `main` a row reads nothing of the crowd: light is neither bent nor
delayed beside a mass, exactly (series K: the deflection 0.000 pixel in y
and z at `M = 2^12` and `2^13`, `b = 6` and 3, the mean age 89.40 in every
world, the count and the phase rate the control's, at a crowd where
nature would capture the beam). **Not reached**: the equivalence principle
holds for bodies (section 3.3) and not for light; the delay field is a
metric for clocks and for matter's pushes, not for the flight. The
paper's statement ("an optical metric and its geodesics") describes a
rule the law does not have.

Under the world key `meeting` (`meeting-v1`, note 35, off by default) a
paid row turns toward the crowd's `-V` by one step of the direction table
per N crowd units met, the count on its phase (section 1.2 step 3). In
the continuum limit of a fine fan (the step `delta_theta -> 0` with the
grain `N delta_theta` fixed) a row passing a mass at the impact distance
b turns by

    theta = integral of (abs(V) / (Q N)) delta_theta dt = (q / (4 pi N)) delta_theta x (pi / (b c)) = q delta_theta / (4 N b c),

the form `M / b` of Newton's and Einstein's deflection with the sign
toward the mass, the constant a grain of the fan; and its phase gains the
crowd met, `integral of abs(V) dt / Q`, which is `q / (4 N b c)` too: a
phase delay `~ M / b`. Nature's deflection is `4 G M / (b c^2)` and its
Shapiro delay `(2 G M / c^3) ln(4 r_1 r_2 / b^2)`: the delay reads the
POTENTIAL along the path (M / r integrated, a logarithm), the meeting's
phase reads the FLOW (M / r^2 integrated, `1 / b`). **Different law** for
the delay under the key, **reached in form** for the bending with a grain
constant; and no delay in time under either (the flight table is one
speed). Registered (K under the meeting): the centroid toward the mass in
every world (-1.79, -4.36, -2.30 pixels at (2^12, 6), (2^13, 6), (2^12,
3); the offline flight's -3.0, -4.3, -2.6, the first outside because 122
of the most turned rays clicked on the mass itself), the mean age moved
only by the bent path's extra Links (+0.50, +1.24, +0.31 intervals), the
phase offset per pixel sharp (the resultant 0.92 to 0.98 at the lit
pixels of `mass`) and tens of steps apart from pixel to pixel: the crowd
met is per path, an interferometer of two paths reads their difference.
The smallest step of K's table is 2.4 degrees, `10^4` times nature's 1.75
arcseconds: the value is out of reach by the grain and is not claimed
(the register's own words).

### 5.5 The general flux, and what Einstein's equation has that this does not

The owner names "the general flux". The exact statement the lattice has
is Gauss's law of the stream at every instant (section 3.1): the amount
crossing any closed surface per interval is the release inside it, after
the front; in the continuum `div(g) = -4 pi G rho` with `g = -grad(A)`
the field of 5.1, and dynamically the continuity equation of the rows
(the paper's fourth limit: the books hold the content exactly, `d rho / dt
+ div(j) = 0`). This is the flux form of the field equation, exact on the
lattice and linear in the sources. Einstein's equation `G_mu_nu = 8 pi G
T_mu_nu` reduces to it in the weak static limit and has beyond it: (i) a
tensor source (pressure and momentum flux gravitate: here only the
content's release does); (ii) the field's own energy as a source, the
nonlinearity (here the rows carry content 0, are read by no row, and the
fields of two sources add exactly: gravity does not gravitate); (iii) the
metric acting on light and on clocks alike (here on clocks and on
matter's pushes, not on the flight); (iv) a cosmological term (here none:
series G2's deceleration `q = +0.345` under the key and `+0.922` under
the source rule with gravity on, `-0.108` coasting, the law having no term
that gives `q < 0`, records 124 and 138). **Not reached** for Einstein's
equation; **reached** for its weak-field flux form and its retardation.

### 5.6 The verdict of target 5

| Formula | Verdict | The place |
| --- | --- | --- |
| Poisson's equation for the delay field | **reached**: the age moment is the retarded potential `q(t - r/c) dwell / (4 pi c r)`, the presence its flux; series E's `k_a r = 36.1`, `k_s r^2 = 41.5`, the ratio `sqrt 3 / 2` | linear, additive over sources |
| The retarded wave equation of the field | **reached** (a scalar field propagating at c, sourced by the release) | no self-source |
| The gravitational redshift | **reached at first order** (`1 / (1 + k)`, the 1 / r form of series E); **different law** at second order, no horizon | the strong field k = 2 .. 9 registered |
| Newton's geodesics | **reached**, retarded; the post-Newtonian terms **not reached** | the coupling bilinear |
| The bending of light | **not reached** on `main` (0.000 registered); under `meeting-v1` **reached in form** `~ M / b` toward the mass, the constant a grain | the flight blind to the crowd |
| The Shapiro delay | **not reached** on `main` (0.00); under the key **different law**: a phase `~ M / b` from the flow, not `M ln(4 r_1 r_2 / b^2)` from the potential, and no delay in time | the meeting reads the flow |
| The general flux | **reached**: Gauss's law of the field exact at every instant, the continuity equation | the weak-field flux form of the field equation |
| Einstein's equation | **not reached**: no tensor source, no self-gravitation, no metric for light, no cosmological term (`q > 0` registered) | the law's gravity is scalar and linear |

## 6. The information cost: units created per record against bits out, the click's discrete cost, and the classical-quantum boundary as a quantity

**The operations.** The birth (T: a lamp of quantum h at the turn s pays
`cost = h s` per unit born, `nature_beam.py:3762, 3844-3847`), the split
(a linear map: a row `(w, m, p)` becomes `(w a_i, m A, p + t_i)` on the
directions, `A = sum a_i^2`, `nature_beam.py:3596-3695`), the rotation
(the half-angle tables, `1848-1916`), the gate (P, `1769-1845`), the merge
with the cancel (G, `1153-1237`), the click (E: the offers' pointers, the
cells' norms, the rungs, the cell of u; `amplitude.py:490-752`). The
register: series L (`examples/events/amplitude/`: L1 the Mach-Zehnder, L2
the two slits, L3 the pair and the which-path worlds, L4 GHZ, L5 the
gate, L6 the pair at N = 1024 and 4096), the paper's checks
(`paper/click_model/checks/`, on the branch `claude/paper-click-model`:
formulas evaluated from the rules, not runs).

### 6.1 What a record costs and what it pays back

A record is born as k rows of one unit (one per direction, one per label:
the Mach-Zehnder 2, the pair `2 arms x 2 labels = 4`, GHZ `3 x 2 = 6`,
the two slits' lamp 5), each unit costing the lamp `h s` of content. A
split multiplies units: `w -> w sum_i a_i` (the (20, 21) splitter makes 41
of 1, the fan of 91 makes 91 of 1), and the content per unit is kept, so
the content in transit grows at every split and is booked as released
(`nature_beam.py:3665`: `content_released += w a_i x content`; note 37
(ii): "the units a split creates enter `released` as every re-creation
does"). The books balance because the created content is on the released
line; what is conserved through the split is not the content but the
norm `sum w_i^2 / m_i = w^2 / m` (the paper's Theorem 2, the isometry). At
the completion every offer's rows have already clicked at their sets
(`held += content` at each `measure`, `3384-3388`), the ladder chooses one
cell, and the record with its other offers is deleted from the layer
(`amplitude.py:749`). The units a record carries to its ends are therefore
its cost in content per record, against the bits the one click reports,
`log2 (cells)` at most (the paper's row 5):

| World | units born | units at the ends (the record's rows) | cells | bits out per click | units per bit |
| --- | --- | --- | --- | --- | --- |
| Mach-Zehnder, the (20, 21) splitter | 2 | `2 + 2 + 2 x 41 = 86` (the two mirrors re-emit 1 each, the splitter 41 per input unit) | 2 | 1 | 86 |
| the pair | 4 | 4 | 4 | 2 | 2 |
| GHZ | 6 | 6 | 8 | 3 | 2 |
| GHZ by one gate of three parties | (the Boss's tally of the register: 729; not re-derived here) | 729 | 8 | 3 | 243 |
| the two slits (`slits_low`, the fans of 91) | 5 | `5 + 2 x 91 = 187` | 80 sets | 6.3 | 30 |

The cost is discrete and grows with the apparatus, not with the
information: a splitter of weights `(a, b)` costs `a + b` units per unit
for one bit, and every rotation of a label bit costs `C' + S'` units per
unit (362 at a quarter turn on the tables of 128) with the multiplicity
`x 65536`, so a chain of rotations reaches the register's ceiling at the
fourth (L5: `rotations_4` refused at load). What the record pays back at
the click is the deletion of every combination but one (`gather`'s
`before` and `after`: `labels x channels` combinations to 1, record 80:
"the one operation that changes the possibilities") and the content of
the chosen offer joined to the world's list; the content of the unchosen
offers stayed where their rows clicked. **The formula**: per record,

    cost (units of content h s) = sum over the ends of the rows' amounts = k x product over the path's splits of (sum_i a_i),
    information out <= log2 (cells)  bits,

the first a product of the declared weights along the paths (the host's
`2^n`, principle 9 of record 74), the second the Holevo bound of a
d-level system read once (`log2 d`), an identity of the model with
quantum mechanics (the paper's row 5: GHZ XXX's 4 of 8 triples, 2 bits,
the third bit the law's). **Reached** for Holevo, as an identity; the cost
per bit is the apparatus's and has no counterpart formula in nature (the
units are amplitudes in integers, and nature's amplitudes cost nothing to
carry). Landauer's heat per click (record 140: "Landauer out") is not a
formula of the law.

### 6.2 The click's discrete cost: the rung, the tables and the wheel

Three roundings, each declared once, are the whole cost of the click's
discreteness (sections 1.2 and 1.3): the rung `b_k = (2 N C_k + T) // (2
T)` at the nearest integer, the tables C, S at the scale 256, and the
birth wheel `u = ordinal mod N`. What they cost: (i) the probability of a
cell is `b_k / N`, a multiple of `1 / N`, within `1 / (2 N)` of the Born
weight `W_k / T` (the paper's row 3, proved from the rung), so a cell of
weight below `1 / (2 N)` never clicks: the Mach-Zehnder's dark port at
the offers `1 / 1682 = 0.0006` reads 0 of 64 (Born's 0.04), and `mz_345`
reads 63 / 1 where the rung moved one u into D2 (L1, registered); (ii) the
tables' rounding puts a record's total at `65448 / 65536` to `65773 /
65536` (eight values over the 64 births of L1, within `237 / 65536` of
1, registered): the norm is kept to a part in 276, the unitarity of the
click's map to that precision, and `S(N, Q)`'s second term `16 arcsin(sqrt
2 / (2 Q))` is its trace (0.044 at Q = 256); (iii) the wheel's period N
repeats the same cells for ever (record 156: `slits_low`'s 19 cells for
2^30 births), so a run of B births resolves the Born weights to `1 / N`
and not to `1 / B`; the bit-reversed wheel W of record 156 resolves every
prefix to `1 / 2W`.

**Born as a limit.** `|P(o) - W_o / T| <= 1 / (2 N)` with `T = sum W_k`:
as N grows the click's probabilities converge to the squared sums, at the
rate `1 / N` (the paper's check: within `7.8 x 10^-3` at N = 64, `4.9 x
10^-4` at 1024, `7.6 x 10^-6` at 65536). **Reached as a limit**, the
squared sum itself the click's definition (E and the norm, the one
imported law of physics, BEAM_LAW section 5), so what the limit returns
is the precision, not the rule.

**Tsirelson as a limit.** The pair's `S(N, Q)` at the CHSH labels, from
the rungs and the tables: 2.75 at N = 64 (the registered `176 / 64`),
2.8125 at 256, 2.828125 at 1024 and 4096 (the registered `2896 / 1024`
and `11584 / 4096`, both `181 / 64`), unchanged by Q from 256 to 2^20 at
these N (the rungs decide), and `S(N, Q) -> 2 sqrt 2` with the bound `8 /
N + 16 arcsin(sqrt 2 / (2 Q)) -> 0` (the paper's check, `limits.txt`
section 1); not monotone in N (record 102: 252 of 512 values above `2
sqrt 2`, the powers of two from 512 exactly `181 / 64`), two-sided within
the bound. **Reached as a limit**: the finite-N departures are the terms
of it, a no-signalling box of the Popescu-Rohrlich kind at finite N, with
the marginals exact (`32 / 64` in all 4096 setting pairs, record 105).

### 6.3 The boundary between classical and quantum, as a quantity

Record 77: "classical and quantum are the same GameBoard at a different
density of clicks". The quantity the law gives is per record: its rows
at one Node and its reads before its merge.

**Rows per record.** A record of one row (a lamp of one direction and one
label, a free release, a row of no record) is a classical particle: its
ladder has one cell wherever it ends, the click lands where the row is,
u chooses nothing. A record of two or more rows that meet at one Node is
the quantum case: the cell's weight there is `|w_1 e^(i p_1) + w_2
e^(i p_2)|^2` (coherent within one Node, record 96), so the weight of that
Node oscillates with the phase difference with the visibility

    V = 2 w_1 w_2 / (w_1^2 + w_2^2)      (1 for equal rows; the classical formula of two amplitudes),

and across Nodes the weights add (incoherent: rows at different Nodes
never meet, `amplitude.py:625-643`). Registered: the Mach-Zehnder's 64/0,
0/64, 32/32 at the phase 0, a half turn, a quarter turn (L1); the `(3,
4)` split's 63/1.

**Reads per record.** A `read` at a `sum` set puts a which-path factor on
the record: one residual per label present, the identity entry
(`amplitude.py:524-527`), so every cell of the ladder is one label's and
the cross terms between labels vanish from every weight. For the pair the
correlation goes from the interference form to the product form,

    E(a, b) = cos 2a cos 2b   in place of   cos 2(a - b),

so at the CHSH labels `E x 64 = 44, -44, 0, 0` and `S = 88 / 64` (L3's
`path_*` worlds, registered) where the unread pair reads `44, 44, 44, 44`
and `S = 176 / 64`; and a read on one arm at any tick before the counter
gives the same (`path_16_24_far`, Bob 116 Links farther: `E x 64 = 0`).
The law has no partial read: a read factor selects a label whole, so the
visibility of an interference between two labels is a step,

    V(reads) = [reads = 0] x 2 w_1 w_2 / (w_1^2 + w_2^2),

not the continuous trade-off `V^2 + D^2 <= 1` of a partial which-path
measurement (Englert); a filter on a hand or a label is a full read
(hand-v1: the filter the label's which-path factor). **Different law** for
the partial case, **reached** for the two ends of it (V = 1 unread, V = 0
read; S = 176 / 64 and 88 / 64 registered). The boundary as a quantity:
a record is quantum where it has at least two rows at one Node and no
read on its labels before that Node; it is classical otherwise; the
density of clicks of record 77 is the density of reads along the rows'
paths.

### 6.4 E = h f from the release

A lamp of quantum h whose clock turns s phase steps per self-creation
(`s = by_clock(age, content x n, d)` at `K = [n, d]`, note 33 (2): the
turn is the release at the rate [1, K], "E = h f as a rate") pays `h s`
per unit born (`cost = definition.quantum * turn`, `nature_beam.py:3762`).
Its frequency is `f = s / N` cycles per self-creation, so the content of
one unit of light is

    E = h s = (h N) f,

Planck's constant the declared quantum times the circle, `h N`, and the
frequency the lamp's own turn: a unit carries the content its lamp's
frequency says, exactly, at every birth. **Reached**, as an identity of
the release. Registered: the Bell lamps of content `K + 2` pay 2 per
birth and stall once at tick 4 when their content falls below K (note 41
(vii), record 148: "a paid lamp's frequency falls at every birth, the cost
quantum x turn"); the L1 lamp of content 2^20 at K = 2^20 turns 1 per
self-creation and pays 1 per unit. What does not return: the frequency of
a row in flight is its family's `phase_per_link` or its pair form, a
declaration, while its content per unit is `h s` from its lamp: the two
are tied at the birth (the lamp's phase stamped on the row) and not
afterwards, so a row re-emitted at a re-emitter keeps its content and
takes the re-emitter's declared turn: no rule makes the content of a row
follow its frequency in flight.

### 6.5 The verdict of target 6

| Formula | Verdict | The place |
| --- | --- | --- |
| The cost per record, `k x prod (sum_i a_i)` units against `log2 (cells)` bits | **stated**: 86, 4, 6, 187 units for 1, 2, 3, 6.3 bits; the cost the apparatus's product of weights, the information the Holevo bound | the split creates content on the released line; the norm `w^2 / m` is what is kept |
| The Holevo bound | **reached** as an identity (`log2 d` per click; GHZ's 2 bits of 3) | Definition 3 of the click |
| Born's rule | **reached as a limit**: `|P - W/T| <= 1 / (2 N)`; the rule itself the click's definition (imported) | the rung; the dark port 0 of 64 at `1 / 1682` |
| Tsirelson's bound | **reached as a limit**: `S(N, Q) -> 2 sqrt 2`, 2.75, 2.8125, 2.828125 registered at 64, 1024, 4096; two-sided at finite N | the rungs and the tables |
| The visibility | **reached** for two rows at a Node, `2 w_1 w_2 / (w_1^2 + w_2^2)`; **different law** for a partial read: a step `[reads = 0]`, S from 176/64 to 88/64 | the read factor selects a label whole |
| The classical-quantum boundary | **stated as a quantity**: two rows at one Node and no read before it | record 77's density of clicks = the density of reads |
| E = h f | **reached** as the release's identity, `E = h s = (h N) f` | Planck's constant `h N`; in flight the frequency and the content are untied |
| Landauer's heat | **not a formula of the law** (record 140) | |

## 7. Young's spacing from the click in the limit of every direction, and Bohr's levels from the turn under `action`

### 7.1 Young's fringes

**The operations.** The re-emission on a fan (the split with equal
weights: one row per direction, the multiplicity K), the walk (T), the
phase per interval of age (T on `Z_{N d}`, the pair form), the merge (G)
where two rows of one record meet at one Node, the click (E and the norm)
at the record's completion; the record: the two-slit world `slits_low`
(L2: the lamp's rate [1, 1], the pair form `[8591334592, 2^30]` = 8.00
steps per interval, the fans of 91 per opening, `s = 10` between the
openings, the screen at `D = 44`, N = 64), record 156's map
(`two_slits_map.py`: the register's 64 clicks reproduced exactly, then
the prediction under the screen's fan, the wheel and the exact phase),
the paper's `limits.txt` (the fan's discreteness and the flight's
rounding), L1's unequal arms.

**The derivation.** A pixel at the height y of the screen receives one
row from each opening at `y = +-s / 2` when the fans hold the directions
`(D, y -+ s / 2)` (the limit of every direction, Huygens'). Each row's
age at the click is its Euclidean path over c, `tau_i = L_i / c` with `L_i
= sqrt(D^2 + (y -+ s / 2)^2)` (section 4.1: the cone is Euclidean), and
its path phase is `(n / d) tau_i` steps; the cell's weight at the pixel
is `|e^(i phi_1) + e^(i phi_2)|^2 = 2 + 2 cos(2 pi (n / (d N)) (L_1 - L_2)
/ c)`. With `L_1 - L_2 = y s / D` to first order in `s / D` and `y / D`
the weight is periodic in y with the spacing

    delta_y = lambda D / s,   lambda = c N d / n Links   (the wavelength: N d / n intervals at c Links per interval),

Young's law. On `slits_low`: `lambda = 8 intervals x 0.5818 = 4.654
Links`, `delta_y = 4.654 x 44 / 10 = 20.5` pixels, the spacing record 156
pins with the screen's fan (bright at y = 35 .. 38, 59 .. 61, 82 .. 85,
Pearson 0.963 with the cosine, the visibility 0.96 over 4096 births).
**Reached in the limit of every direction**, with the exact phase at the
click. The registered check of the two-path rule itself is L1's unequal
arms: arm 2 longer by two intervals at the pair form 0, `[8, 1]` and
`[16, 1]` reads D1/D2 `64/0`, `32/32`, `0/64`: the phase difference `(n /
d) delta_tau = 0, 16, 32` steps of 64 gives `cos^2` of 0, a quarter turn,
a half turn, integer by integer (the register's L1).

**Where the lattice departs, in order of size** (record 156's order: the
wheel, the fan, the phase):
1. The birth wheel of period N (section 6.2): `slits_low` as registered
   lands 15 screen clicks on 14 pixels for ever (64 clicks: wall 34,
   screen 15, faces 15), whatever the run's length; the bit-reversed wheel
   W resolves every prefix.
2. The fan's discreteness: an opening's fan of K directions reaches a
   pixel from one opening only where its digital line lands there and the
   other's does not; with K = 91 only 27 of 75 pixels see both openings
   (the register), and the correlation with the cosine grows with K: 0.45
   at 91, 0.84 at 361, 0.90 from 721 on (the paper's check, every pixel
   seeing both from K = 721); the registered fan of 91 is the opening's
   comb (68, 115, 68 at y = 59, 60, 61 where rows of ONE opening on
   neighbouring directions meet), no fringes under any click.
3. The arrival at a whole interval: the phase is read at the whole age of
   the last Link while the exact time is `made x T_d / (S_1 Q)`, an
   error of up to one interval, an eighth of the wavelength at `lambda =
   8 intervals` (the correlation 0.93 with the exact pattern at lambda 8,
   0.995 at 32, the paper's check: vanishing as `lambda / interval`
   grows); the exact phase from the row's two accumulators (record 156,
   section 1.3 item 14) removes it, and turns the wheel-alone staircase
   (Pearson 0.904) into the cosine (0.963).
4. The isqrt of `T_d` per direction (1.35 % in c, one step in 234 on the
   cone), vanishing as Q grows; and the envelope of the fan's density
   (section 3.2), a declaration.

### 7.2 Bohr's levels

**The operations.** The push (B, section 3.4: the electric column
against the proton's crowd), the step (D) and the turn by momentum
(`engine.py:637-645`: at the Link stepped on an axis the phase turns by
`by_clock(k0, |p_axis| N, h)`, the world's `action` h), the release of
the electron's rays with its phase, the faces' `wave` records (E). The
register: series H (`examples/events/bohr/`: the proton of content 1836
on the 2616-direction shell, the electron of content 1836 and charge
-15 on a set of three Nodes, `width` 45120, r = 2 .. 16), its re-reads
under the step drive and the signed drive.

**The closure.** Over one orbit the phase turns by `(N / h) x sum over the
Links stepped of |p_axis|`, the floors telescoping at a constant `|p|`.
For a circle of radius r stepped on the lattice with p tangent and
constant, the sum over the x-Links of `|p_x|` is `integral of p |sin
theta| x r |sin theta| d theta = pi p r` and the y-Links give the same:

    sum over the Links of |p_axis| = 2 pi p r = the action  integral of p . dl,

exactly in the limit of small Links (the arithmetic check of this
section on lattice circles: `2.010, 2.003, 2.0004, 2.0001 x pi r` at r =
8, 16, 64, 256). The phase closes on itself when

    2 pi p r = j h,   j whole:   Bohr's quantization of the action, exactly, with h the world's `action`.

With the push `p^2 / (Q S M r) = M k / r^2` of section 3.4 (a circular
orbit under the inverse square, `p ~ 1 / sqrt r`) the closing radii are

    r_j = j^2 h^2 / (4 pi^2 Q S M x (M k)),   r_j ~ j^2:

Bohr's ladder of radii, **reached in form**, the constants the world's
(`action`, `width`, the charges' product). Two corrections to the
register's design on the way: (i) the Bohr README derives the closure as
`4 p r = j h` ("the Manhattan weighting of the path, 4 r against the
circle's 2 pi r"); the sum over the Links of the component on the
stepped axis is the action `2 pi p r` and not `4 p r`, so with `h = 16
p(8)` the design's `j = 2.000` at r = 8 is `j = pi = 3.14`, and the
table's j are `pi / 2` times larger (r = 2: 1.49; 4: 2.30; 6: 2.71; 8:
3.14; 12: 4.01; 15: 4.51; 16: 5.10): the whole values fall at r = 12 (j
= 4) and near r = 2 (j = 1.5, between), not at r = 8; in the step-drive
re-read r = 12 closed five times with every return within `r / 4` and r
= 8 four times, and the phase's turn per orbit at r = 8 read 0.75 to 0.83
of a circle beyond whole circles, which is what `j = 3.14` on an
eccentric loop gives sooner than the design's 0; the r = 12 world's
fraction is the reading to take (the register's re-read tables, not read
here). (ii) The turn as built re-prices `k0 |p| N / h` at the current
`|p|` (section 1.3 item 6), and on an orbit `|p_axis|` changes at every
interval, so the closure is exact only under the accumulator form
ordered by record 155.

**The levels and the lines.** Bohr's energies `E_j ~ -1 / j^2` and the
Rydberg lines `1 / j^2 - 1 / k^2` need an energy of the orbit and a
transition between orbits; the law has neither: no energy is defined for
a body, and nothing makes the electron leave one closed orbit for
another (no rule of the GameBoard reads a closure). What a detector reads
of a closed orbit is the phase of the electron's rays, turning per
interval by `(N / h) p v` on the average, the orbital frequency `nu_j =
p_j v_j / h ~ 1 / j^3`: the classical radiation frequency of the orbit
(Bohr's correspondence limit), not the difference of two levels.
**Not reached** for the levels and the lines; **reached in form** for the
quantization condition and the ladder of radii. Registered: no orbit
closed by the series' criterion on the base (the whole kicks: 84 lumps of
4.3 degrees per orbit at r = 8 from the fan of 2616 directions every 10
intervals, and the close pass), the mean inward push 40 600 against the
derived 39 660 (1.02: the mean flux is the derived one, the orbit is
broken by the lumps); under the step drive r = 8 and r = 12 closed four
and five times and the coherence `C(4) = 1.01` against 2.0; under the
signed drive r = 8 twice, r = 12 none. The limit that closes the orbit is
the one of section 3.2: every direction and a smooth push (the ring flux
`r^-1.83` of the 2616-direction fan against `r^-2`); Bohr's lines then
still need what the law lacks, an energy and a transition.

### 7.3 The verdict of target 7

| Formula | Verdict | The place |
| --- | --- | --- |
| Young's spacing `lambda D / s` | **reached in the limit of every direction** with the exact phase at the click (record 156's 20.5 pixels; L1's `64/0, 32/32, 0/64` the two-path rule registered) | the wheel, the fan's comb, the arrival's floor, the isqrt |
| Bohr's condition `2 pi p r = j h` | **reached** exactly in the limit of small Links (the sum of `|p_axis|` over the Links is the action) | the design's `4 p r` corrected; the accumulator form for a changing p |
| Bohr's radii `r_j ~ j^2` | **reached in form** under the inverse square | no closed orbit registered on the base; r = 12 (j = 4.01) the closing radius under the true sum |
| Bohr's energies and the Rydberg lines | **not reached**: no energy, no transition; the detector reads the orbital frequency `~ 1 / j^3` | a different law of the spectrum |

## 8. The verdicts of round 9 in one table

| Target | Reached | Different law | Not reached |
| --- | --- | --- | --- |
| 1 the inventory | every rule one of six operations or a declared rounding; the flight one Manhattan accumulator with a deficit ladder | | fourteen items for the implementer, four new (two dropped events at the step, the meeting's rounding and its root) |
| 2 Doppler | `1 +- v / c` on the axis under the crossing rule; the source's `1 / (1 -+ v / c)` | the transverse 1; the Manhattan flux on a fan direction; two formulas at `v^2` | on `main`, the reader's Doppler (k per k) |
| 3 Newton and Coulomb | Gauss exactly; the inverse square in the shell mean; `G = K (n / d) / (4 pi S)`; `k_C = G`, the ratio `-rho_A rho_B` | | per Node without the limit of every direction |
| 4 special relativity | the light cone and `omega = c k`; the Lorentz symmetry of the rows' limit | the moving reader's `c -+ v`; the clock at 1; `v = p / (m + p)`; the cap 1 above c | velocity addition, `E = m c^2`, the moving mass |
| 5 general relativity | Poisson and the retarded wave equation of the delay field; the redshift at first order; Newton's geodesics; the general flux | the redshift at second order, no horizon; the meeting's delay `~ M / b` | Einstein's equation; light on `main`; the post-Newtonian terms |
| 6 the information cost | Holevo; Born and Tsirelson as limits; the visibility of two rows; `E = (h N) f` | the partial read (a step) | Landauer |
| 7 Young and Bohr | Young's spacing in the limit of every direction; Bohr's `2 pi p r = j h` and `r_j ~ j^2` | the spectrum at the orbital frequency | the levels' energies and the Rydberg lines |

## 9. The law of information on the GameBoard: the inventory restated as one law, and its cases derived

The owner's request (record 166, through the G2 session, as the Boss
relayed it): "a generic information law in the system", not a rule per
case. Section 1's inventory restated as that law; then the wait, the
moving detector and the crossing rule derived from it as its cases, and
what it forbids.

### 9.1 The law, in five statements

- **(I1) A message is a row.** It is created at exactly one event, a
  self-creation of a body (a release, a lamp's birth, a re-emission, a
  give; `nature_beam.py:3507-3955`, `engine.py:768-838`), and it ends at
  exactly one event: a read that absorbs it (a click at a body's table, a
  home, a re-emission's take), an escape through a face, or the border
  `lifetime`; or it has not ended yet. Between the two it is in transit,
  a row of the store, and nothing else exists: no Node holds a message
  that is not in transit (section 1.1). What it carries is its record:
  direction, age, phase, number, amount, content, and under a record its
  identity, label, multiplicity, birth phase and hand.
- **(I2) A Node transmits per interval the rows that step out of it**,
  each through one Port, one Link, at the flight table's pace (section
  1.2 step 1); it holds nothing back, delays nothing, copies nothing (the
  merge adds identical rows, the split creates units on the released
  line: section 6.1). A Node's whole activity in an interval is the
  translation of the rows on it and, in free space, their permutation
  (the collision, the meeting).
- **(I3) A body receives the rows of other numbers that reach it, and
  emits only at its self-creations.** At rest a row reaches it when it
  arrives at its Node (`nature_beam.py:2741`); in motion, under the
  crossing rule (record 158), when their world lines cross, once. It
  emits its release, its lamp's birth and its re-emissions at its
  self-creation and at no other interval (`entry.creating`,
  `nature_beam.py:3514`); its own rows that return are taken home and
  re-emitted at the next self-creation.
- **(I4) A clock's rate is the reciprocal of one plus what it reads.**
  A body's clock counts its self-creations; after each it owes `by_clock(age,
  k n, d)` intervals, k the messages present at its Node in that interval
  (the presence) or their age-weighted sum (the age moment), n / d the
  world's width: the rate `1 / (1 + k n / d)`. A clock is slowed by
  messages and by nothing else (sections 4.3 and 5.2).
- **(I5) The balance.** Every message released is on exactly one line of
  the books at every interval: `released = in transit + absorbed +
  escaped (+ cancelled)` per family, in amount and in content, exact at
  every tick (`engine.py:880-1025`); this is the message balance, the
  conservation of information as a count. The momentum balance is a
  statement about messages: a PAID message carries its label out of its
  emitter at birth (the recoil, `nature_beam.py:3888-3921`) and into its
  reader at its end (the click's push, the label), so for paid messages
  `sum of momenta on bodies + in transit + escaped` is conserved exactly
  and the third law holds message by message. A FREE message (a free
  family's row, the field) carries no recoil at birth (section 3.3: a
  free release costs nothing) and pushes its reader by its label times the
  reader's content: for free messages the third law is not a balance per
  message but a symmetry between two readers, `M_A V_B = M_B V_A`, exact
  only while both read the same number of each other's messages (series
  C item 2: 1.0000 at rest).

### 9.2 The wait, derived

Record 139's open question: in an interval in which a body's clock owes,
messages arrive at its Node. Three readings of I3: (a) the body is absent
in both directions (rule (a), record 128: neither emits nor reads); (b)
it is a receiver only (`main`: it reads and takes pushes, releases
nothing); (c) the wait is a matter of the count alone (the clock's phase
stops, the messages continue both ways).

What I5 says of each, for a pair A, B of free readers with A waiting one
interval at t (B's messages take one interval to A, A's to B):

- Under (b), A takes B's push at t and sends nothing at t; B misses A's
  push at t + 1. The pair gains one net push per wait, on A's side
  (record 126: "one push net per wait"). I5's symmetry is broken by
  exactly the message A did not send.
- Under (a), A misses B's push at t and B misses A's at t + 1: one each,
  balanced per single wait. The imbalance record 139 measured (`-12 P`
  in 500 intervals on the register's deuteron, two steps) is the pair's
  waits falling in the same interval or one apart at every cycle: the
  two clocks read each other's releases and lock, and when B's wait falls
  at t + 1 it removes an empty read (nothing arrived) and one real
  release. So under (a) the balance fails not by the rule but by the
  locked clocks; I5 says why no rule at the waiting body alone closes it:
  a free message has no recoil, so a missed read is a lost push with no
  partner, and only the symmetry of the two readers' counts balances the
  pair. The form that closes every case is the one record 132's section
  7 names, a recoil at the free release, which makes I5's paid-message
  balance hold for the field too; it is a change of the law for the
  owner, not derived here.
- Under (c), messages neither stop nor are missed; I5's symmetry is
  untouched by a wait and the third law holds as at rest. What changes:
  the release no longer stops with the clock, so a lamp in a crowd emits
  at the interval's rate and its light carries the clock's slowing only
  in its phase, not in its count; the register's luminosity reading of
  series G and G2 (the click rate `1 / (1 + k)` times the Doppler, the
  hubble_stars README) would move by `(1 + k)`. A different law with a
  registered consequence, stated so that it can be chosen.

The two sub-questions. (i) Does a body count the messages it did not
read while waiting? Under I4 the count is read at the self-creation from
the messages present at that interval (`engine.py:475-485`,
`Measured.counted` set by the law's step 4 in that interval): the rows
that passed during the wait are not counted, and the rows resting at the
Node at the next self-creation are (record 139's "the probe of k = 8
counts 16 and owes 4"), a bounded feedback and not a register. The
owner's principle "a message enters only at a self-creation" is I3 and
I4 together: it is read and counted at the self-creation and neither at
any other interval. (ii) Does its own returning message enter it while
it waits? On `main` the home rows are taken whatever the clock owes
(`nature_beam.py:2664-2727`, record 139's note). I1 and I3 leave two
lawful readings: the home rows are taken (a body's own message is not a
message from another, so I3's "receives" does not govern it), or they are
not taken and walk on as rows of the body's own number (leaving with
their content, an emission during a wait, which I3 forbids). What is NOT
lawful is the third: the rows held at the Node until the body creates
(section 9.4). The first reading is the one the law has, and the one
I3 permits.

### 9.3 The moving detector and the crossing rule, as cases

**The moving detector** is I3's second clause with I1: a message ends at
exactly one event, so a body and a row meet at most once, and they meet
when their world lines cross. On `main` the reading is at the Node after
the walk and before the step (`engine.py:378-401`), which misses the rows
resident at the destination when the body enters (never read: 1.72 per
step toward the lamp, record 153) and reads again the rows it left
behind that catch it up (the leapfrog): two violations of I1, one a lost
message and one a message read twice, which cancel in the count (k per k
in both senses) and not in the physics. **The crossing rule** (record
158) is I1 applied to a stepping body: it meets the rows that crossed its
own Link the other way and the rows resident at its destination moving
against it, and not the rows moving with it, behind it, or already met.
Its count is section 2's `1 +- v / c` on the axis, the Manhattan flux on
a fan direction, exactly 1 transverse: every one a consequence of "once"
and of the flight table, with no weight and no key. The reading's weight
of doppler-v1 was a factor standing in for the missing crossings (section
2.2: the key's `374784 / 262144` is `1 + 55 / 128`); under I1 it is
redundant, as record 151 said.

### 9.4 What the law forbids

- **A message waiting for a closed body.** A row held at a Node until the
  body there self-creates is a register at the Node (a Node holds nothing
  but the rows in transit, I2), so under a wait a row is read at the
  crossing or it goes on; it is never queued.
- **A message read twice or by two bodies.** I1: one end. The leapfrog
  re-read of `main` and the self-Link re-arrival (section 2.4) are the
  two places the engine does it today; the crossing rule removes both.
- **A message without a sender**, and content created outside a
  self-creation: the split's units are booked on the released line at
  the re-emitter's self-creation (I5), a lamp's birth costs its content;
  nothing else creates a row (the give is a self-creation's act at the
  contact).
- **A weight on a message**: a body counts messages; it does not scale
  them by its own state (I3, I4). The one weight the law had, the flux of
  doppler-v1, is deleted with the crossing rule.
- **A rate that reads what is not at the Node**: I4's k is the messages
  present, never a field, a total or a history (LOCALITY-1).

What the law does not decide, and says so: the third law of free
messages is a symmetry and not a balance (I5), so a bound pair whose
clocks lock can drift under any rule at the waiting body; the balance
per message needs a recoil at the free release, the owner's question of
record 132's section 7.
