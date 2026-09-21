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

The verdict of each section uses DERIVATIONS.md's words. **Reached**:
the known law follows from the rules in the stated limit, exactly or up to a
constant that is named. **Different law**: the rules give a definite law of
another form, stated, with the registered integer or the run that shows the
difference. **Not reached**: the rules as declared do not determine the
quantity, and what would is stated plainly. **New** marks a formula the
GameBoard gives that has no counterpart in known physics.

**Symbols** (the owner's rule, record 184). Every symbol is named in
English at its first use, and a Greek letter is written as a Latin word
with the quantity's name (gamma, the Lorentz factor), never as a letter
alone. The kind of a quantity is shown by its type in prose: a scalar
plain (c, M, N, gamma), a vector in bold lowercase (**p** the momentum
vector, **s** the state vector on the torus, **r** the rate vector), a
matrix, a tensor or an operator in bold uppercase (**F** the interval's
map, **C** the coupling matrix, **G** the click's Gram matrix), a
component plain with its index (`p_x`). Inside a formula (a code span or a
code block) every letter is plain, its kind being the one stated here or
at its first use. The recurring symbols:

| Symbol | Kind | Name |
| --- | --- | --- |
| **F** | operator | the interval's map, one piecewise-linear map of the state (section 0) |
| **s**, **r**, d | vector, vector, scalar per component | the state on the torus, its rate, its wall (the accumulator `s += r; e = [s >= d]; s -= e d`) |
| **C**, **a** | matrix, vector | the coupling matrix (the reader's charges per column) and the label flow vector of the arriving rows; the push `r = C a` |
| **G**, **P**, **E** | matrix, matrix, matrix | the click's Gram matrix (`G = E^T E` in 6.7), the rotation of the phase as a signed permutation (section 6.5), the `2 x N` matrix of the tables C and S; `U_s` the label rotation matrix of the half-angle tables |
| **p**, `p_x` | vector, component | a body's momentum and its component on an axis |
| **v**, v | vector, scalar | a body's velocity and its speed in Links per interval |
| **V** (the code's `V`) | vector | the label flow read at a Node, the vector moment of the arriving rows (written `V` in formulas as the code writes it) |
| **D**, `u_d`, `T_d`, `S_1` | vector, vector, scalar, scalar | a direction of the world's table, its unit vector at the scale Q, its period `isqrt(3 abs(D)^2 Q^2)`, its Manhattan length |
| c | scalar | the pace of a row, `Q / T_d` Links per interval on the axis (`32 / 55`) |
| Q, N, K, h | scalars | the direction table's scale (64), the circle of the phase, the world's content quantum, the world's action quantum |
| K (section 13 only), `K_clock` | scalars | the computation budget of one Node per interval; in section 13 the world's content quantum is written `K_clock` |
| M, k, q | scalars | a body's content (its mass); a crowd or a coupling count; a charge (in sections 2.5 and 5.5, q is the deceleration parameter of the Hubble fit, stated there) |
| n / d | rational | the declared phase rate per interval |
| u | scalar | the birth phase of a record, the wheel `ordinal mod N` |
| tau | scalar | the age of a row in intervals |
| gamma | scalar | the Lorentz factor `1 / sqrt(1 - v^2 / c^2)` |
| lambda | scalar | the wavelength |
| theta | scalar | an angle |
| pi | scalar | the ratio of the circle |
| phi | scalar | a body's phase |
| omega | scalar | the angular frequency |
| rho | scalar | the charge per unit of content, a family's declaration |
| alpha, `alpha_G`, k (section 16) | scalars | the fine-structure constant; the gravitational coupling `G m_p^2 / (hbar c)`; the electron's count in units of the minimal mass |
| kappa | scalar | the meeting's column sum per unit |
| zeta_N | scalar | the primitive N-th root of unity, `exp(2 pi i / N)` |
| sigma_j | map | the j-th Galois conjugate of the evaluation `ev` (section 6.5) |
| Lambda_c | scalar | a column's declared bound on the branch |
| f | element | a record's rows at a Node as an element of the group ring `Z[Z_N]` |
| beta, `R_ret`, `n_ret` | scalar, scalar, vector | the speed over the pace of a row `v / c`; the distance from a moving source's retarded position; the unit vector from it (section 12) |
| `c_1`, `k_p` | scalars | a direction's Manhattan pace `S_1 Q / T_d` in Links per interval (sections 2.4, 12c); the rest count of a partner's rows at a body (section 12c) |
| a, H | scalars | the growth factor of the flight's wall and its rate per interval, a declared constant of the world (section 15) |

The reference tree is `main` at `f89884f0` (the law as landed on 2026-09-20,
BEAM_LAW notes 1 to 40); where the fraction-free branch
(`origin/fraction-free` at `ddec5166`, note 41 there, record 154, its
physics review record 157) changes an operation, both are stated, the
branch's form named as the ordered one. The crossing rule (record 158) and
the `no-tables` items of record 155 are designed and not built; they are
cited as orders, not as code.

Section 0 states the law as one operator with its two blocks and places
every result under its block (the owner's second pass, record 167 as the
Boss relayed it); sections 9 and 10 answer records 166 and 162; section 11 answers record 190 (the GameBoard as one vector map between events); section 12 answers record 200 (Lorentz from the delay field) and 12b revisits it with the moving reader's count and the orbit as the bond; 12c answers record 230 (the mover's counter under the crossing count and the owed count, route C); section 13 answers record 209 (the one constant K, the computation per Node per interval); section 14 answers records 214 and 215 (entropy); section 15 answers records 215 and 218 (the growing wall); section 16 answers records 239 and 243 (the numbers of nature from the law's structure, the minimal mass). The
targets, in the Boss's order, one section each: 1 the inventory (the
owner's audit); 2 Doppler from the crossing rule; 3 Newton and Coulomb from
the bilinear coupling; 4 special relativity, the symmetry of the limit; 5
general relativity, the delay field; 6 the information cost and the
classical-quantum boundary; 7 Young's spacing and Bohr's levels.

## 0. The operator F: one piecewise-linear map on the integer torus, its two blocks, and where every result of this document sits

**The statement** (the owner's, accepted in record 167 as the Boss
relayed it; verified here against sections 1 to 7). The whole law is one
map **F** (the interval's map) applied at every Node at every interval to
the integer state vector **s**, per component with its own rate **r** and
wall d:

    s <- s + r;   e <- [s >= d];   s <- s - e d,

every wall crossing an event. The components of **s** and their (r, d): a
row's Manhattan count (rate `2 S_1 Q`, wall `2 T_d`, started at `T_d`;
section 1.4) and its three axis deficits (rate `abs(v_i)` per Manhattan
step, the carry `S_1` from the largest); a row's phase (rate
`phase_per_link` per Link, or `n` per interval of age with the wall d,
the whole part read mod N); a row's age (rate 1, no wall); a body's drive
per axis (rate `p_a`, wall `Q S M + abs(p_a)`); a body's counts, on the
branch the table `acc` (the turn: rate `content x n`, wall d; the owed
count: rate `counted x n`, wall d; the release and the lamp; the push per
column: rate `V E_c n_c`, wall `Lambda_c^2`, Lambda_c the column's declared bound); a record's birth wheel u
(rate 1 per birth, wall N); the click's ladder (the comparison `2 T u + T
<= 2 N C_k`, a wall read once). Everything in section 1.2 is **F** on one of
these components or a permutation of them (the collision, the meeting's
arc, the gate, the apportioning's tie), and the exceptions are section
1.3's list.

**The two blocks.** **F** is linear where its rates are constants of the
world, and it feeds back where a rate is a function of what arrives:

- **The linear block** (rows in flight): the translation at a constant
  rate (the flight, the phase per Link or per interval, the age); the
  group-ring addition at the merge (`Z[Z_N]`, with the cancel `[p + N/2]
  = -[p]`); the integer matrix of a split (`w -> w a_i`, `m -> m A`) or
  of a rotation (the half-angle tables) or of a gate (a permutation of
  labels); and the evaluation `ev: Z[Z_N] -> Z[zeta_N]` at the click
  (zeta_N the primitive N-th root of unity), linear over the group ring. Every component here has the closed form

      s(t) = floor(s_0 + r t)     (the accumulator's whole part at a constant rate; FORM.md section 1),

  so a row's state at any time is a formula of its birth and its age, and
  the limits of this document are limits of that formula.
- **The feedback block** (the rates as functions of the arrivals): the
  push `r = C a` (**C** the coupling matrix, the reader's charges per
  column; **a** the label flow vector of the arriving rows: the rate of a body's momentum is bilinear in the
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
| linear | the flight, `m(tau) = floor((2 tau S_1 Q + T_d) / (2 T_d))` (tau the age in intervals) and the deficit ladder | the digital line at `Q / T_d -> 1 / sqrt 3` Links per interval, isotropic | record 144's cone, 17 and 24 Links at age 29 | 1.4, 4.1 |
| linear | the phase, `floor((n / d) tau) mod N` along the line | `omega = c k` (omega the angular frequency, k here the wave number), dispersionless (the paper's check) | L7's path phases 23 and 23 (the pair form), 51 and 8 (the integer form) | 4.1, 7.1 |
| linear | the crossing count of a row's line with a body's, `n (c +- v) tau + O(1)` | the receiver's Doppler `1 +- v / c` | record 158's 45, 58, 19, 38, 183, 311; the bar's 96.9 .. 303.1 | 2.2 |
| linear | the merge, `Z[Z_N]` at one Node | the coherent sum within one Node | L1's `mz_equal` 41 of multiplicity 1682 | 6.3 |
| linear | the evaluation at `zeta_N` and the norm | `S(N, Q) -> 2 sqrt 2`; Born to `1 / (2 N)` | `176 / 64`, `2896 / 1024`, `11584 / 4096`; the dark port 0 of 64 | 6.2 |
| linear | two rows' phases at a pixel, `(n / d)(L_1 - L_2) / c` | Young's fringes at `L_1 - L_2 = +- j lambda` (lambda the wavelength; paraxially `lambda D / s`), from the fan's angular measure (record 160's Farey weights `3 Q^2 / (T_d T_d')` per direction) | L1's unequal arms 64/0, 32/32, 0/64; record 156's bands 23.5 apart against the exact 23.3 | 7.1 |
| linear | the split's norm `sum w_i^2 / m_i = w^2 / m` | the conservation of a record's norm | L1's (3, 4) split 63/1 | 6.1 |
| feedback | the push, `p_{t+1} = p_t + C a_t`, `a_t` the flow at the body's Node | `dp / dt = -M grad(A)`: Newton's and Coulomb's `1 / r^2` in the shell mean | series C's nine ring readings `r / N(r)`; item 7's `-1`, `-1 / 4` | 3.2 .. 3.4 |
| feedback | the drive, `x_{t+1} = x_t + [drive >= D]`, `v = p / (Q S M + p)` | the dispersion `v(p)`, saturating at 1 | the bar's speeds 0.30, 0.45, 0.75 exact | 4.4 |
| feedback | the owed count, `owed = by_clock(age, k n, d)` (the branch: `acc_owed`) | the clock at `1 / (1 + k n / d)`, the potential `M / r` under `age` | series E's `k_a r = 36.1`, `k_s r^2 = 41.5` | 5.1, 5.2 |
| feedback | the field of many bodies, the sum of their rows' moments | Poisson and the retarded wave equation, linear | series E; series K's 0.000 (no term on the rows) | 5.1, 5.4 |
| feedback | the turn under `action`, `phi += floor(k_1 abs(p) N / h) - floor(k_0 abs(p) N / h)` (phi the body's phase) | the action `2 pi p r = j h` (pi the ratio of the circle) | series H's re-reads (r = 12 the whole j) | 7.2 |

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

Read against main `f89884f0` and the fraction-free branch at `ddec5166`;
the fraction-free law landed on main at `cd6bb887` on 2026-09-21; the
items ordered on the branch are now on main; the re-read of the inventory
against main follows the no-tables and click pull requests, once.

**The claim audited** (the Boss's statement of the law to the owner, record
155, verified here against the documents and the code). The state is
integer vectors on tori and nothing at a Node. A row (a ray's record,
`NatureBeam`, `nature_beam.py:195-240`): its Node in `Z_X x Z_Y x Z_Z` (a
periodic axis a circle, an open axis a segment with the face as its
border), its direction an index of the world's table of direction vectors **D**, its age a whole
count, its phase in `Z_N` (and, in the pair form of `phase_per_link`, a
point of `Z_{N d}` whose whole part is the phase, note 37 (iii); the row
carries the age, from which that point is a function), its number, its
amount, its content, and under a record its identity, branch, multiplicity,
birth phase u and hand. A body (`Measured`, `measured.py:205-353`): its
held content per family in `Z^F`, its momentum vector **p** in `Z^3` (components `p_x`, `p_y`, `p_z`), its phase in
`Z_N`, its clock age, its drive per axis in `(-D, D)`, and on the
fraction-free branch its counts table, the point `acc` of `Z^n / d Z^n`.
One operator every interval at every Node. Six operations only:

- **(T) the translation**: `x -> x + r` on `Z^k` or on a torus; the counts'
  form `acc += r; e = [acc >= d]; acc -= e d`, every wall crossing an
  event, is the Euclidean division `Z = Z/d x Z` with the remainder kept
  (`core/integer.py:70-86`, `by_drive`), the one primitive of every count;
- **(B) the bilinear form**: a moment `sum_rows w x u^(x)k` of the
  neighbourhood's rows (k = 0, 1, 2 and the age), and the coupling `r = C
  a` (**C** the coupling matrix, **a** the flow vector), a signed inner
  product over declared columns times the moment;
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
| The Manhattan count `m(tau) = (2 tau S_1 Q + T_d) // (2 T_d)` | `nature_beam.py:549-554`, `632-643` (the step table) | (T)/(D): an accumulator started at `T_d` (the half), gaining `2 S_1 Q` per interval, carrying one Manhattan step at `2 T_d`; `2 S_1 Q <= 2 T_d`, so at most one Link per interval | as built a floor at run time (D) whose remainder is dropped; nothing is lost, because the dropped remainder is a function of the age alone (the accumulator started at `T_d`, gaining `2 S_1 Q`, carrying at `2 T_d`, equals `m(tau)` on seven directions over 600 intervals, section 1.4), so it is a torus operation with the age as the accumulator; the table `flight.steps[direction, age mod L_d]` at `2398` is its exact cache (FORM.md section 1); checked below |
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
| The meeting's norm `abs(t) = isqrt(t . t)`, then `norm //= denominator` over the columns' common denominator | `meeting.py:351-358` | an integer square root at run time, then a floor | **NOT** twice: a root whose fractional part no record owns, the one non-rational function evaluated on the lattice per interval; and the floor of the norm over the common denominator (exact only at denominator 1, every registered meeting world) |
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
| The apportioning of a row over the directions or over a body's Nodes: the floors, the units left to the largest remainders, ties from `age mod n` | `core/integer.py:100-116`, `nature_beam.py:3727`, `3866` | (D) exact (the shares sum to the total) with a tie by comparison; the tie's start a rotation (P) | a torus operation per birth; record 155 (3) orders the leftover onto the giver's record as an accumulator, which gives the same integers wherever the shares are equal weights (each direction takes the leftover once per n births either way) |
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
9. **A rounding per interval: the meeting's register, twice.** `meeting.py:232`,
   `adv = (abs(t) + Q // 2) // Q`: the crowd met is rounded to whole units
   of Q every interval and the rest dropped; and `meeting.py:357-358`,
   `norm //= denominator`: where the crowd's families have several column
   denominators the target is formed over their common denominator and
   its norm floored back per interval, a second discarded remainder
   (exact where the denominator is 1, every registered meeting world). The torus form: `acc += abs(t)`
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
axis") is NOT this form. Its one natural reading: axis i carries an
accumulator at the rate `abs(v_i) Q` with the wall `T_d`, so that the
Links made on axis i by the age tau are `floor(tau abs(v_i) Q / T_d)`. On
`(1, 1, 0)` the two axes then share the rate `64 / 156` and fire in the
same intervals (3, 5, 8, 10, ... under the plain floor; 2, 4, 7, 9, ...
under the half-rounded floor `(64 tau + 78) // 156`), two Links in one
interval either way, which the walk forbids; the total by age 29 is `2 x
floor(29 x 64 / 156) = 22` under the plain floor against `m(29) = 24`, and
24 under the half-rounded one, which agrees with `m(tau)` at 29 and not at
every age (at age 1: 0 against 1). The torus form of the flight is the one above: one count of Manhattan
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

### 1.5 Every integer division of the source, by class

Every `//` of `src/event_universe` outside docstrings and comments, on
`main` at `f89884f0`, with its class: **G** a guard (a bound tested by
division before a product is formed; no state changes), **A** an
addressing or an index division, exact by construction (the flat Node
index, the Port's axis, the arm of a way), **P** a period or a reduction
by a gcd or an lcm, exact, **R** a declared rounding (at load: the tables,
`u_d`, `T_d`, the half circle, the parser's ceilings; at the click: the
rungs), **E** an exact division whose remainder is kept or is zero
(`reduced`, the give, the apportioning's floors with the remainders
distributed in the same call, the carry of an accumulator), **C** a cap
or a comparison (a quotient read as a count of what can be paid, section
1.3 item 13), and **D** a discarded remainder at run time (the items of
section 1.3).

| Class | The lines |
| --- | --- |
| G | `measured.py:112`; `meeting.py:194, 336`; `nature_beam.py:838, 841, 868, 950, 964, 1808, 1871, 2056, 2118, 2140, 2213, 2216, 3634, 3645`, `2034` (the bound quoted in the guard's message); `world.py:1528, 1767, 2485, 2648, 2668, 2682`, `1698` (the parser's static budgets and the label bound at load, the last in its message) |
| A | `game_board.py:59` (the Port's axis); `nature_beam.py:1082, 1084` (the flat index's coordinates), `3784, 3828` (the ways per arm and the arm of a way, the parser refusing an uneven split); `world.py:1324` (the span's half, the span odd by the parser) |
| P | `nature_beam.py:610, 611, 612` (the flight's period `L_d`); `meeting.py:328, 333` (the columns' common denominator); `amplitude.py:153, 167, 184, 194, 650, 697` (lcm, gcd, the common denominator of two multiplicities, the reduced pair, the multiplicity over the arm's norm) |
| R at load | `core/integer.py:34, 36` (`integer_root`, Newton's iteration: the exact floor of a root, used at load for `T_d` and `u_d` and at run time by the meeting, item 10); `core/phase.py:28, 33, 34, 43, 48, 49, 63, 66, 83, 88` (the tables C and S from the fixed-point series, rounded to the nearest at the scale 256); `amplitude.py:132, 139` (the half-angle table's index, refused where it is not whole); `nature_beam.py:575` (`u_d`), `508` (the window's half width), `1125, 1221, 1883, 2599` and `world.py:1656` (the half circle `N // 2`, exact for every N of the law); `world.py:474, 1303, 1304` (ceilings of the budgets and the flight bound) |
| R at the click | `amplitude.py:192` (the rung `(2 N C_k + T) // (2 T)`, the nearest integer, once per record; the comparison form on the branch), `215` (the Node's rung within the cell) |
| E | `core/integer.py:45` (`reduced`, by the gcd), `108` (the apportioning's floors, the remainders given out in the same call, nothing left); `engine.py:800` (the give, `held // h` with `held mod h` kept on the giver); `meeting.py:233, 240` (the register's carry `total // N` with the residue kept as the phase, and its inverse); `nature_beam.py:553` (`m(tau)`, the Manhattan count: as built a floor whose dropped remainder is a function of the age, which holds it, section 1.4); `nature_beam.py:492` and `core/integer.py:67` where the rate is constant (the constant-rate identity, FORM.md section 1: the phase per interval of age, the lamp's rate, `ages_at_key`) |
| C | `nature_beam.py:3774, 3789, 3799` (the units a lamp can pay, `held // cost`, a comparison and the cap `min` of item 13) |
| D | `core/integer.py:67` and `nature_beam.py:492` where the rate changes (the turn, the owed count, the release, the columns: items 1 to 4; the branch's `by_drive` replaces them); `nature_beam.py:853` (`share_of`, item 12); `2057` (the speed's grain, item 5); `meeting.py:232, 239` (the crowd met to the nearest Q, item 9) and `358` (the norm over the common denominator, item 9); and `core/integer.py:67` again through `by_clock` (`58-67`, called at `engine.py:644`: the turn under `action`, item 6) |

Every line of the source with a `//` is in one row above; no division
is unclassified. The `%` of the wrap on a periodic axis
(`nature_beam.py:2404, 2373`) and of the phase (`2501`) are the torus's
own reductions, exact (T).

### 1.6 The verdict of target 1

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
at the Euclidean rate `n (abs(c) + v cos theta)` (theta the angle
between the row's direction and the reader's velocity). **Different law** on a
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
extent 1: there a row's y-step is a self-Link (the wrap `nature_beam.py:2403-2405`;
the adjacency's self-Link, its docstring `game_board.py:38-39` and the wrap `61-64`) that crosses no world
line and is no arrival, so the stream's Manhattan speed
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
s_px1 0.0573 reads 0.0611: every star within 0.004 in z of `v / c`
(the README's grain of the digital step is 0.003; s_mz2 and s_px1 are
0.0038 off, a grain and a third); and the crowd's registered free fit is
`q = -0.108` in the late window (-0.22, -0.08, -0.11 over the three
windows), `H (t_0 + T_0) = 1.026`, rms 0.0019 in z, inside the coasting
bracket `q = 0 +- 0.25` (the README's table, record 138). The tool's `q =
0.000`, `H = 1.000` is its validation of the exact Milne form at the
worlds' own taus, not the fit, and is not the check.

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
target 4; the answer here is what the count says: no factor of `gamma` (the Lorentz factor, `1 / sqrt(1 - v^2 / c^2)`)
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
3.3 at P = 16: the primitive vectors of the cube within 11.5 degrees of
the corner direction against those within 11.5 degrees of a face centre,
76 / 25 and 544 / 165, the arithmetic check), a cubic anisotropy of the DECLARATION, absent for a
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
(HYPOTHESES entry 21, the physicist's finding: "the engine's rate is one
at every speed, nature's gamma a limit stated so that it can fail").
The only slowing of the law is the owed count, `owed = by_clock(age, k n,
d)` with k the crowd the clock reads (the presence, or the age moment),
`engine.py:475-485`: a clock slows by what it reads, `1 / (1 + k n / d)`,
never by its speed. Nature's moving clock runs at `sqrt(1 - v^2 / c^2)`.
**Different law**: the moving clock's factor is 1. The registered check
is series G2's `coasting_none` (section 2.5): the star's light carries `1
+ z = (1 + k)(1 + v / c)` with `k = 0` (no crowd, no slowing); had the
lamp's clock carried nature's `gamma`, the fastest coasting star (s_mz2,
`v / c = 0.2674`, `gamma = 1.0378`) would read `z = 1.0378 x 1.2674 - 1 =
0.315`, and the register reads `0.2636`: 0.0038 below the classical
`0.2674` (a grain and a third of the README's 0.003) and 0.051 below the
relativistic value, 17 grains. The
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
alike) is the causal speed, and the rows' `1 / sqrt 3` is below it, so a
body of `p > 1.39 Q S M` (`v > 32 / 55`; 1.37 at `1 / sqrt 3`) outruns
its own family's rows (the bar's outrunning body at `v = 0.75`, section
2.2, registered). Nature's light is at
the causal bound; the lattice's is at `1 / sqrt 3` of it, the owner's
"phase velocity the wave on the mesh had" (BEAM_LAW section 3), so that
no direction crosses two Links in one interval.

### 4.5 What returns and what does not

| Formula | Verdict | The place |
| --- | --- | --- |
| The isotropic light cone, `omega = c k` | **reached** (the rows; the cone of record 144) | `c = 1 / sqrt 3` in the lattice's frame |
| Lorentz covariance of the free rows' limit | **reached** as the symmetry of the wave equation the rows converge to, not as a symmetry of the lattice (the cubic 48 and the translations only) | the ties of FORM.md section 3 break even the 48 |
| The invariance of c for a moving reader | **different law**: a moving reader counts `c -+ v` (Galilean); an isotropic crowd hides it two-way exactly, a one-way count shows it | the crossing count |
| The moving clock's `gamma` | **different law**: the rate is 1 at every v (HYPOTHESES 21); G2's fastest coasting star reads `z = 0.2636`, 0.0038 from the classical 0.2674 and 0.051 (17 grains) from `gamma`'s 0.315 | the clock's frame; the only slowing is the crowd's |
| The dispersion `v(p)` | **different law**: `p / (m + p)` in place of `p / sqrt(m^2 + p^2)`; the cap 1 above c | the step rule |
| Velocity addition, `E = m c^2`, the mass of a moving body | **not reached**: no operation carries a body's speed into its content or its clock; content is invariant, the momentum unbounded | the law has no energy of motion (target 6 for the release's E = h f) |
| A preferred frame | the lattice's, and inside a crowd the crowd's: measurable one-way, hidden two-way | 4.2, 4.3 |

## 5. General relativity: the equation of the delay field

**What "held content delays the flight" is in beam-v1.** Nothing in
flight is delayed: a row moves by the flight table at one speed, blind to
the crowd (BEAM_LAW section 3; series K, registered: the mean age 89.40
in every world, the difference 0.00). What a crowd delays is a CLOCK: a body
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

On `main` a row reads nothing of the crowd: a row is neither bent nor
delayed beside a mass, exactly (series K: the deflection 0.000 pixel in y
and z at `M = 2^12` and `2^13`, `b = 6` and 3, the mean age 89.40 in every
world, the count and the phase rate the control's, at a crowd where
nature would capture the beam). **Not reached**: the equivalence principle
holds for bodies (section 3.3) and not for rows; the delay field is a
metric for clocks and for the bodies' pushes, not for the flight. The
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
crowd met, `integral of abs(V) dt / Q`, which is `q / (4 b c)` phase
steps, `q / (4 N b c)` turns of the circle: a phase delay `~ M / b`. Nature's deflection is `4 G M / (b c^2)` and its
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
phase offset per pixel sharp (the README's words: "resultant 0.9 to
1.0 at the lit pixels of `mass` and `near`") and tens of steps apart from pixel to pixel: the crowd
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
the bodies' pushes, not on the flight); (iv) a cosmological term (here none:
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
| Einstein's equation | **not reached**: no tensor source, no self-gravitation, no metric for the rows, no cosmological term (`q > 0` registered) | the law's gravity is scalar and linear |

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
| Mach-Zehnder, the (20, 21) splitter | 2 | `2 x 41 = 82` (each mirror re-emits its unit whole, the splitter 41 per input unit; after the merge's cancel 42 remain, the registered rows of amount 41 toward D1 and 1 toward D2 of `mz_equal`, L1) | 2 | 1 | 82 |
| the pair | 4 | 4 | 4 | 2 | 2 |
| GHZ | 6 | 6 | 8 | 3 | 2 |
| the two slits (`slits_low`, the fans of 91) | 5 | `2 x 91 + 3 = 185` (two rows reach the openings and are re-emitted on 91 each; three end at the wall) | 80 sets | 6.3 | 29 |

The units at the ends are derived from the worlds' declarations by the
formula below; the registered integers that check the arithmetic are the
merged amounts `41` and `1` of `mz_equal` (L1: `20 + 21` in phase, `21 -
20` in antiphase) and `slits_low`'s 64 clicks, reproduced by record 156's
map row by row from the same five rows and two fans; the totals 82 and
185 are not registered as such.

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
imported law of physics, BEAM_LAW section 5; its form forced in 6.5),
so what the limit returns is the precision, not the rule.

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
`path_*` worlds, registered) where the unread pair reads `44, -44, 44, 44`
(`S = E(0, 8) - E(0, 24) + E(16, 8) + E(16, 24) = 176 / 64`); and a read on one arm at any tick before the counter
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
birth and stall once at tick 4 when their content falls below K (the
bell README: "paying 2 per birth, stalls once, at tick 4: 159 births in
160"; note 41 (vii), record 148: "a paid lamp's frequency falls at every birth, the cost
quantum x turn"); the L1 lamp of content 2^20 at K = 2^20 turns 1 per
self-creation and pays 1 per unit. What does not return: the frequency of
a row in flight is its family's `phase_per_link` or its pair form, a
declaration, while its content per unit is `h s` from its lamp: the two
are tied at the birth (the lamp's phase stamped on the row) and not
afterwards, so a row re-emitted at a re-emitter keeps its content and
takes the re-emitter's declared turn: no rule makes the content of a row
follow its frequency in flight.

### 6.5 The uniqueness of the click's square: a lattice Gleason

**The question** (record 170, the owner's, sent for a solution): the
click's square `X^2 + Y^2` (`amplitude.py:641`: a cell's weight is the sum
over the ends' Node tuples of `real^2 + imaginary^2` of the summed
pointers) is the one operation of the model beyond translate, threshold,
the declared matrix and the addition, and the place where the Born rule
is put in. Asked here: whether rows whose phases cancel, non-negative
counts, a total conserved at every declared split and invariance under
the phase rotation force the reading at a click to be a positive
quadratic form of the record's group-ring element, `|ev(f)|^2` up to a
constant, on the register's declared splits; or what weaker statement
holds, and what the register pins.

**The objects.** A record's rows at one Node and label are one element
`f = sum_p f_p x^p` of the group ring `Z[Z_N]` (`f_p` the amount at the
phase p, section 1.1); the pointer is `ev(f) = sum_p f_p zeta^p` (zeta
the primitive N-th root of unity) at the
tables' scale (`amplitude.py:562-565`: `weight x (C[p], S[p])`, summed
per `(Node, label)`); the merge's cancel (the design's 2.3: two rows of
one record at a phase difference of exactly `N/2` subtract) identifies
`x^{N/2}` with `-1`, so the rows after the cancel are an element of
`Z[x] / (x^{N/2} + 1)`. For N a power of two (64, 1024, 4096: every
registered N) `x^{N/2} + 1` is the cyclotomic polynomial of N, so this
quotient is the ring of cyclotomic integers `Z[zeta_N]` itself, a free
Z-module of rank `N/2` on the basis `1, x, ..., x^{N/2 - 1}`, and `ev` is
the identity on it: the GameBoard's cancel and the click's zero are one
relation, exactly. (For an N with an odd factor they are not: at N = 12
three rows at the phases 0, 4, 8 read 0 at the click and cancel nowhere
on the GameBoard; the register has no such N.) The reading is a function
`R: Z[zeta_N] -> R` of a cell's element; the ladder normalises by the
record's total (2.5), so R matters up to one factor per record, and the
multiplicity m is the split's bookkeeping of that factor.

**The hypotheses**, each an operation of section 1 and nothing else:

- (a) the phase rotation: `R(x f) = R(f)`. A rotation of the record's
  phase by one step changes no weight: the ladder (`rungs`,
  `amplitude.py:174-194`) takes no u, and L1's 64 births at 64 birth
  phases read one ladder up to the tables' rounding (6.2 (ii));
- (b) the balanced splitter conserves for every two inputs: the (1, 1)
  split with the quarter turn on the reflected row (`mz_balanced`; the
  table form `weights [[a, b], [b, a]]`, `turns [[16, 0], [0, 16]]` of
  `mz_345.json` with a = b = 1) sends the inputs f on arm 1 and g on arm
  2 to `x^{N/4} f + g` toward one port and `f + x^{N/4} g` toward the
  other, with the multiplicity factor `A_2`, and the total is conserved:
  `R(x^{N/4} f + g) + R(f + x^{N/4} g) = A_2 (R(f) + R(g))` for all f, g
  in `Z[zeta_N]`;
- (c) counts: `R(f) >= 0`.

Not assumed: continuity, a dimension, the form of R on one row, or
Theorem 2's `A = sum a_i^2`.

**Theorem (the lattice Gleason).** Under (a), (b), (c), with N a power
of two,

    A_2 = 2,   R(f) = sum over odd j, 1 <= j < N/2, of c_j |sigma_j(f)|^2,   c_j >= 0,
    sigma_j(f) = sum_p f_p exp(2 pi i j p / N)     (the j-th Galois conjugate of ev(f); sigma_1 = ev).

Every such R is a positive quadratic form on the lattice, homogeneous,
`R(a f) = a^2 R(f)`; it conserves the total at every declared split
`(a_1, ..., a_k; t_1, ..., t_k)` of one row or of two recombining inputs
exactly if and only if the multiplicity factor is `A = sum a_i^2`
(Theorem 2's rule, here a consequence), and at every label rotation
`U_s` with the factor `C'^2 + S'^2`. Two rows `a x^p` and `b x^{p + D}` (D
here the phase difference in steps) at one Node read

    R = C (a^2 + b^2) + 2 a b K(D),   C = sum c_j,   K(D) = sum c_j cos(2 pi j D / N),

with `K(0) = C`, `K(N/4) = 0`, `K(N/2) = -C` for every admissible R. The
Born form `|ev(f)|^2` is `c_1 = 1` and the other `c_j = 0`: `K(D) =
cos(2 pi D / N)`.

**Proof.** (i) g = 0 in (b) with (a): `R(x^{N/4} f) + R(f) = 2 R(f) =
A_2 R(f)`, so `A_2 = 2` (R not identically 0). (ii) Replace g by
`x^{-N/4} g` in (b) and use (a) on the first term, `x^{N/4} f +
x^{-N/4} g = x^{N/4} (f - g)` since `x^{-N/2} = -1`: `R(f - g) + R(f +
g) = 2 R(f) + 2 R(g)`, the parallelogram law on the abelian group
`Z[zeta_N]`. (iii) The parallelogram law alone makes R a quadratic form;
on a lattice Jordan and von Neumann's argument needs no continuity:
`R(0) = 0` (f = g = 0), `R(-f) = R(f)` (f = 0); for `B(f, g) = R(f + g)
- R(f) - R(g)`, symmetric, with `B(f, -g) = -B(f, g)` by the law, the
law at `(f + g, h)`, `(f + h, g)` and `(f, g - h)` gives `R(f + g + h) =
R(f + g) + R(f + h) + R(g) + R(h) - R(f) - R(g - h)`, whence `B(f + g, h)
- B(f, h) - B(g, h) = 2 R(g) + 2 R(h) - R(g + h) - R(g - h) = 0`: B is
Z-bilinear, `R(f) = B(f, f) / 2` (the law at (f, f)), so R is the
restriction to `Z^{N/2}` of the real quadratic form of the symmetric
matrix **G** `= (B(x^i, x^j))`, the click's Gram matrix, and `R(a f) = a^2
R(f)`. (iv) (a) transfers
to B by polarisation, `B(x f, x g) = B(f, g)`; multiplication by x is a
signed permutation of the basis, an orthogonal matrix **P**, so `P^T G P
= G` and **G** commutes with **P**. **P** has the `N/2` distinct
eigenvalues `zeta^j`,
j odd, with the eigen-functionals `sigma_j` (`sigma_j(x f) = zeta^j
sigma_j(f)`), so **G** is diagonal in that basis with real entries paired
under `j <-> -j`: `R(f) = sum_j c_j |sigma_j(f)|^2` over the `N/4`
conjugate pairs. (v) Were some `c_j < 0`, the real form would be
negative on an open cone of `R^{N/2}`, which contains lattice points,
against (c): every `c_j >= 0`. (vi) The conservation at a general split:
on one row `w x^p` the outputs `w a_i x^{p + t_i}` sum to `(sum a_i^2)
w^2 C` by homogeneity and (a), against `A w^2 C`: `A = sum a_i^2`. On
two recombining inputs, `a f + b x^{N/4} g` and `a g + b x^{N/4} f` (the
`(a, b)` splitter with the quarter turn), the cross terms `2 a b B(f,
x^{N/4} g)` and `2 a b B(g, x^{N/4} f) = 2 a b B(x^{N/4} g, x^{N/2} f) =
-2 a b B(f, x^{N/4} g)` cancel and the total is `(a^2 + b^2) (R(f) +
R(g))`; the label rotation's pair `(C' f + S' x^t g, -S' f + C' x^t g)`
cancels the same way with `C'^2 + S'^2`. (vii) Two rows: `|sigma_j(a +
b x^D)|^2 = a^2 + b^2 + 2 a b cos(2 pi j D / N)`, and at `D = 0, N/4,
N/2` the cosine is `1, 0, -1` for every odd j. (Each identity of (vi)
and (vii) was also checked numerically on random elements at N = 64.)

**What is reached and what is not.** Reached: the reading is a positive
quadratic form of the record's element, forced by the phase rotation,
the balanced splitter's conservation and the counts alone, with no
continuity and no dimension. (Gleason's own theorem needs dimension 3
and fails at 2; the lattice version does not, because (b) holds for
every two inputs and not only for orthogonal decompositions, which is
the parallelogram law, a stronger hypothesis, and the balanced splitter
accepts every pair of records.) The multiplicity rule `A = sum a_i^2` is
derived, not assumed; the square is the only power (`R(a f) = a^2
R(f)`: no `|w|^k` with `k != 2` conserves, the paper's "Theorem 2 admits
only k = 2"); and the cross term `2 a b K(D)`, the product between two
rows the GameBoard never forms (record 170: "the merge adds only
identical rows"), is forced to exist at the click by (b), because the
two outputs of a balanced splitter conserve the total only through
cross terms that cancel between them. Not reached by the algebra: the
constants `c_j`, the detector's response to the harmonics of the phase.
This is the lattice Gleason's weaker statement, and it is the exact
analogue of Gleason's: his theorem gives `<v, T v>` with T a free
positive operator (the state); here T is a free positive operator
commuting with the rotation, `diag(c_j)` on the Galois planes. Each
single harmonic alone is the Born form under the relabelling `p -> j p`
of the phase steps (an automorphism of `Z_N` for j odd): it reads the
declared rate `n / d` as `j n / d`, a change of the declaration, not of
the law. A mixture of harmonics is a different law: the flat mixture,
every `c_j` equal, is `R(f) = sum_p f_p^2` on the reduced basis
(Parseval over the odd j; checked), the reading that squares each
phase's amount after the GameBoard's merge and cancel and forms no
product across phases; it satisfies (a), (b), (c) exactly. The algebra
of the splits admits the phase-blind detector; what excludes it is the
register.

**Against the registered integers.**

- The power. The `(3, 4)` split's `63 / 1` (`mz_345`, L1): the elements
  at the ports are `7 x^{p + 16}` (4 and 3 in phase) and `1 x^{p + 32}`
  (the cancel's remainder of 4 and 3 in antiphase), single rows, so a
  power k reads `C 7^k` against `C 1`; the rung `b_1 = (2 x 64 x 49 +
  50) // 100 = 63` at k = 2, and `63 / 1` holds iff `7^k` lies in
  `[125 / 3, 127)`, k in `[1.917, 2.489)`: k = 1 gives `56 / 8`, k = 3
  gives `64 / 0`. The pair's cells `27, 5, 5, 27` (`bell_16_24_far`,
  `E x 64 = 44`): at the turn 0 (every registered pair world declares
  `phase_window` only) every entry of `U_s` is real and every pointer
  sits on one antipodal pair of phases, so a cell's element is the
  single row `(C'_a C'_b +- S'_a S'_b) x^p` and the reading tests only
  the power: the first cell is 27 iff k lies in `[1.784, 2.054)`; k = 1
  gives `23, 9, 9, 23` (`E x 64 = 28`), k = 3 gives `30, 2, 2, 30` (56).
  Both windows contain 2 and exclude 1 and 3. The (20, 21) split's `64 /
  0` needs only `k >= 1.304`; `mz_quarter`'s `32 / 32` and
  `mz_balanced`'s `64 / 0` are symmetric and test nothing.
- The harmonics. Every registered Mach-Zehnder world puts its two rows
  at a phase difference in `{0, 16, 32}` (the arm's turn; the two
  intervals at 8 or 16 steps), where K reads `C, 0, -C` for every
  admissible `c_j`: the MZ cells check the power and nothing about the
  harmonics, and the pair at the turn 0 likewise. Only the two slits
  test K: `slits_low`'s fans put rows of one record at a pixel at every
  phase difference, and record 156's map gives the bands at y = 35 ..
  38, 59 .. 61, 82 .. 85 with the cosine's Pearson 0.963 (7.1): the
  kernel `cos(2 pi D / 64)` of j = 1, 64 steps per 23.5 pixels. At the
  harmonic j the same rows read `cos(2 pi j D / 64)`, a fringe of period
  `23.5 / j` pixels (7.8 at j = 3, 2.6 at j = 9, below a pixel from j =
  31), and the flat mixture reads the comb `[D = 0] - [D = 32]`; the
  registered bands exclude both. So `c_j = 0` for `j != 1` is pinned by
  the two-slit register alone, and with it `R = c |ev(f)|^2`.
- The tables. The built click is this form to the tables' rounding: a
  record's total reads `65448 / 65536` to `65773 / 65536` over the 64
  birth phases (6.2 (ii)), the tables' violation of (a), a part in 276;
  the theorem's R is the exact form the design checks as the inverse
  (2.4), and the design's 2.5 (the ladder normalised by the record's
  total, not by T at birth) is the rule that keeps one click per record
  under that violation.

**The limit.** As `N = 2^k` grows the admissible readings are the same
family with `N / 4` constants; for two rows at the angle `theta = 2 pi D
/ N`, `K(theta) = sum over odd j of c_j cos(j theta)`, the closed cone
of the even positive-definite functions on the circle with odd harmonics
only (`K(theta + pi) = -K(theta)`, the cancel), whose extreme rays are
the single cosines; the Born kernel `cos theta` is the first of them,
the visibility is `V(theta) = K(theta) / K(0)`, and 6.3's `2 w_1 w_2 /
(w_1^2 + w_2^2)` is its amplitude. The limit adds nothing: no N and no
continuity forces `c_j = [j = 1]`; the fundamental is what the register
reads and what the phase means (one step of phase per declared `n / d`:
a detector at the harmonic j is a detector reading the wavelength
`lambda / j`).

**Verdict.** **Reached** for the form: on the lattice `Z[zeta_N]`, N a
power of two, the rotation, the balanced splitter's conservation for
every two inputs and the counts force a positive quadratic form, the
square as the only power and the multiplicity rule `sum a_i^2`; the
registered `63 / 1` and `27, 5, 5, 27` pin the power to 2 (the windows
`[1.917, 2.489)` and `[1.784, 2.054)`). **Not reached** from the
algebra: the harmonic constants `c_j` (Gleason's free state), pinned to
the fundamental by the two-slit bands of record 156 only; every
Mach-Zehnder and pair world of the register is blind to them.

### 6.6 The verdict of target 6

| Formula | Verdict | The place |
| --- | --- | --- |
| The cost per record, `k x prod (sum_i a_i)` units against `log2 (cells)` bits | **New** (a formula with no counterpart in known physics): 82, 4, 6, 185 units for 1, 2, 3, 6.3 bits; the cost the apparatus's product of weights, the information the Holevo bound | the split creates content on the released line; the norm `w^2 / m` is what is kept |
| The Holevo bound | **reached** as an identity (`log2 d` per click; GHZ's 2 bits of 3) | Definition 3 of the click |
| Born's rule | **reached as a limit** for the precision, `|P - W/T| <= 1 / (2 N)`; the form of the rule **reached** in 6.5 (a positive quadratic form, forced), its harmonic constants pinned by the register | the rung; the dark port 0 of 64 at `1 / 1682` |
| The click's square, its uniqueness (the lattice Gleason) | **reached** for the form: the rotation, the balanced splitter's conservation for every two inputs and the counts force a positive quadratic form, the power 2 (63 / 1 pins k to [1.917, 2.489); 27, 5, 5, 27 to [1.784, 2.054)) and `A = sum a_i^2`; **not reached** from the algebra: the harmonic constants `c_j`, Gleason's free state, pinned to the fundamental by record 156's bands alone | 6.5: the balanced splitter's conservation is the parallelogram law on `Z[zeta_N]`; the MZ and pair worlds are blind to the harmonics |
| The click without amplitudes | **reached**: the weight is `f^T G f`, `G = E^T E` the Gram matrix of the tables (rank 2, kills the antipodal pairs exactly, near-circulant to 237), bit-identical to `cells` for one arm and for the tensor form of several; the registered 64 / 0, the 64 clicks of `slits_low` and the pair's 27, 5, 5, 27 reproduced on the Gram weights; **corrected**: the ring convolution of several arms is the exact law, not bit-identical to the built `cmul` | 6.7; the amplitudes one factorisation of **G** |
| Tsirelson's bound | **reached as a limit**: `S(N, Q) -> 2 sqrt 2`, 2.75, 2.8125, 2.828125 registered at 64, 1024, 4096; two-sided at finite N | the rungs and the tables |
| The visibility | **reached** for two rows at a Node, `2 w_1 w_2 / (w_1^2 + w_2^2)`; **different law** for a partial read: a step `[reads = 0]`, S from 176/64 to 88/64 | the read factor selects a label whole |
| The classical-quantum boundary | **New**, a quantity of the law: two rows at one Node and no read before it | record 77's density of clicks = the density of reads |
| E = h f | **reached** as the release's identity, `E = h s = (h N) f` | Planck's constant `h N`; in flight the frequency and the content are untied |
| Landauer's heat | **not a formula of the law** (record 140) | |

### 6.7 The click without amplitudes: one bilinear form on the record's integer vector

**The question** (the owner's, 2026-09-21: "is there a vector operation
that replaces the amplitudes?"; the Boss's answer, proved and corrected
here). The map script beside this document,
[click_gram.py](designs/derivations_beam/click_gram.py) with its output
[click_gram.out](designs/derivations_beam/click_gram.out), makes every
check below on the engine's own tables, a host computation and no run.

**(1) One arm.** A record's rows at one end Node and label are the
integer vector **f** in `Z^N`, `f_p` the amount at the phase p (the
group-ring element of section 6.5 before the cancel, written as a
vector). The click's pointer is `(X, Y) = E f` with **E** the `2 x N`
integer matrix whose rows are the tables C and S (`core/phase.py`:
`cos, sin(2 pi p / N) x 256`, rounded to the nearest integer), the
amounts carrying the scale 32 (`amplitude.py:562-565`: `weight x (C[p],
S[p])` summed over the rows). The cell's weight is

    X^2 + Y^2 = (E f)^T (E f) = f^T G f,   G = E^T E,   G_jk = C_j C_k + S_j S_k,

**Theorem** (bit-identity): on integers, `(E f)^T (E f)` and `f^T (E^T
E) f` are the same sum of the same products in a different order
(associativity and distributivity in `Z`; no rounding after the tables),
so the weight `real^2 + imaginary^2` of `amplitude.py:641` equals `f^T G
f` exactly, for every f. Checked on 200 random vectors of `Z^64`, then on
the register: `mz_equal`'s ports (41 rows in phase toward D1 at `u +
16`, the cancel's 1 toward D2 at `u + 32`, multiplicity 1682) give the
same integer both ways at all 64 birth phases, the offers `1681 / 1682`
and `1 / 1682` exactly at every u (the two ports' phases differ by a
quarter turn, where `C^2 + S^2` repeats), the clicks 64 / 0; `slits_low`'s
126 sets (3 wall Nodes, 121 pixels, 2 faces; 80 with rows) give the same
integer both ways on every (set, Node, u), and the ladder on the Gram
weights returns the registered 64 clicks, wall 11, 12, 11, the fifteen
screen clicks on the fourteen registered pixels (two at 61), faces 8, 7.
The amplitudes are one factorisation of **G**, not a step of the law:
the law's step is the bilinear form, and `E` is its square root.

**What G is.** Symmetric, of rank 2 (two rows of **E**), non-negative
(`f^T G f = |E f|^2 >= 0`), and it kills every antipodal pair `e_p +
e_(p + N/2)` exactly, because the tables are exactly antisymmetric
(`C[p + N/2] = -C[p]`, `S[p + N/2] = -S[p]`: "opposite phases of equal
amounts exactly zero"), so the Gram form factors through the cancel of
section 6.5 exactly. It is near-circulant and not circulant: `G_jk`
deviates from `65536 cos(2 pi (j - k) / N)` by at most 237 (the tables'
rounding, section 6.2 (ii)), and `G_(j+1)(k+1) != G_jk` on 3696 of the
4096 entries at N = 64; its diagonal takes the eight values 65448, 65501,
65522, 65533, 65536, 65650, 65717, 65773 (the eight totals over the 64
births of L1), so `e_p^T G e_p` differs from 65536 at 60 of the 64 phases.
That is the built click's violation of the rotation invariance (a) of
6.5, a part in 276, and nothing else: **G** is the Gram matrix of the
lattice Gleason's form at `c_1 = 1` (the fundamental alone), on `Z^N`
before the cancel, to the tables' rounding.

**(2) Several arms** (the pair, GHZ). As built (`amplitude.py:614-679`):
each arm's rows at an end are evaluated to a pointer, the set's rotation
multiplies the pointer by its entry (a complex integer of the half-angle
tables: `cmul`), the arms' residuals are multiplied in `Z[i]` (`cmul`),
the labels' products are added, and the sum's square is the weight;
within one Node tuple coherent, across Node tuples added. The Boss's
statement "the product of the arms' complex residuals is the
multiplication in the group ring `Z[Z_N]`" is the exact algebra
(`ev(f * g) = ev(f) ev(g)` for the exact root of unity, the product of
two arms' elements the convolution, the label sum the ring addition) and
it is **not bit-identical** to the built click: on the rounded tables
**E** is not a ring homomorphism, `E(e_1)^2 = (64400, 12750)` against
`256 E(e_2) = (64256, 12800)`, so "convolve in the ring, then evaluate
once" and "evaluate each arm, then multiply in `Z[i]`" differ by the
rounding. On the pair's CHSH cells the difference is invisible to the
ladder, because at the turn 0 the two arms' pointers sit at one phase u
and the factor `|E e_u|^4` against `256^2 |E e_(2u)|^2` is common to the
four cells and cancels in the rungs: both forms return `27, 5, 5, 27` at
(0, 8), (16, 8), (16, 24) and `5, 27, 27, 5` at (0, 24), `E x 64 = 44,
-44, 44, 44`, `S = 176 / 64`, the registered integers, while the weights
themselves are bit-different at every u. The form that IS bit-identical
with several arms is one bilinear form on the tensor product: with the
record's block vector `F = (+)_labels (x)_arms f^arm_label` in
`Z^(N^arms)` per label, and `A` the `2 x N^arms` integer matrix "the
entries' scalars, then `E` on each arm, then the product map of `Z[i]`
(`(x_1, y_1, x_2, y_2) -> (x_1 x_2 - y_1 y_2, x_1 y_2 + y_1 x_2)`)", the
weight is `F^T (A^T A) F` exactly, again by associativity: checked on the
pair's four cells at u = 5, settings (16, 8). So the whole click is:
additions in the ring (the merge, the label sum), the arms' product
(a convolution exactly, a `Z[i]` product as built), then ONE bilinear
form with a block-diagonal Gram matrix (one block per Node tuple, the
incoherent sum), then the threshold `2 T u + T <= 2 N C_k` (`cell_of`,
the comparison of two products since `amplitude.py:208`). The Boss's
form stands with one correction: the ring convolution is the exact law,
the built law is its evaluation arm by arm.

**(3) The cost, and whether `Z[i]` can leave.** Per cell of k rows at one
Node the pointer costs 2k products and two squares; `f^T G f` costs `k^2`
products on the sparse **f** (`N^2 = 4096` dense at N = 64), the same
integers; the tensor form of two arms `N^2 x N^2` dense, `N^3` at three
(262144), on a vector of `2^arms` non-zero entries per label. For one arm
`Z[i]` can leave the code entirely: `f^T G f` is an integer bilinear form
and the pointer `(X, Y)` is a report. For several arms it can leave in
two ways, at a price each: the tensor Gram form (bit-identical, the size
`N^arms`), or the ring convolution then one form (exact arithmetic, not
bit-identical: the registered cells unchanged on the pair, the weights
changed at every u). The two places the rounding differs if **G** were
built from `cos(j - k)` instead of `E^T E`: (i) a product of two rounded
entries is not the rounding of the product (`C_j C_k + S_j S_k` against
`round(65536 cos)`: up to 237 apart); (ii) `E^T E` is not circulant (its
diagonal varies with the phase, 3696 entries move under `j, k -> j + 1, k
+ 1`), so a **G** built from `j - k` alone would restore the rotation
invariance the tables break and change the eight totals of L1 to one. The
build must use `E^T E` for bit-identity, and a **G** from the cosine is
the exact law's Gram matrix (section 6.5 at `c_1 = 1`), a change of the
law's integers by a part in 276 wherever a record's total is read.

**(4) The tie to 6.5.** `f^T G f` with `G = E^T E` is the quadratic form
of the lattice Gleason at the fundamental, `R(f) = |sigma_1(f)|^2`, to the
tables' rounding; its rank 2 is the one complex embedding; its kernel on
the antipodal pairs is the cancel; its failure of rotation invariance is
the rounding's and nothing of the law's. **Reached**, bit-identical for
one arm and for the tensor form of several; **corrected** for the ring
form of several arms, which is the exact law and not the built one.

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
/ c)`. The bright pixels are where `L_1 - L_2 = +- j lambda`, `lambda = c N d
/ n` Links (the wavelength: `N d / n` intervals at c Links per interval),
and only in the paraxial limit `s, y << D` does that become the spacing
`delta_y = lambda D / s` (delta_y the fringe spacing), Young's small-angle
law. On `slits_low` the
angle is not small (`y / D` is 0.5 at the first fringe): `lambda = 8
intervals x 32 / 55 = 4.654` Links, the paraxial spacing would be `4.654
x 44 / 10 = 20.5` pixels, and the exact condition `sqrt(D^2 + (y +
5)^2) - sqrt(D^2 + (y - 5)^2) = lambda` at `D = 44` puts the first bright
fringes at `abs(y) = 23.3` about the centre, the pixels 36.7 and 83.3.
Record 156 pins the bright bands at y = 35 .. 38, 59 .. 61, 82 .. 85 with
the screen's fan (Pearson 0.963 with the cosine, the visibility 0.96 over
4096 births): their centres 36.5, 60, 83.5, 23.5 apart, the exact law's
23.3 within the pixel; the paraxial 20.5 is three pixels off and is not
the check. **Reached in the limit of every direction**, with the exact
phase at the click, as the exact two-path law; Young's `lambda D / s` is
its paraxial form. The registered check of the two-path rule itself is L1's unequal
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
section: on the circle of the nearest lattice points to radius r, walked
by axis Links with a diagonal move counted as two, the tangent's
component on the stepped axis summed per Link reads `2.041, 2.011, 2.003,
2.000 x pi p r` at r = 8, 16, 64, 256; the digits depend on the circle
walked, the limit 2 does not). The phase closes on itself when

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
3.14; 12: 4.01; 15: 4.51; 16: 5.10): the one whole value falls at r = 12
(j = 4.01), the only registered radius with a whole j, not at r = 8
(3.14); r = 2 reads 1.49; in the step-drive
re-read r = 12 closed five times with every return within `r / 4` and r
= 8 four times. The registered fractions of the phase's turn beyond
whole circles at r = 8 (0.234 on the base over one pair of closings, 0.75
to 0.83 under the step drive, 0.969 under the signed drive) are read on
eccentric loops (r from 3 to 28) and check neither form: on a circle `j
= pi` would give 0.14, and no registered loop is a circle. The reading
that would decide is the r = 12 world's fraction under the step drive
(near 0 under `2 pi p r`, near 0.55 under `4 p r`), not taken here:
unchecked. (ii) The turn as built re-prices `k0 |p| N / h` at the current
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
| Young's fringes, `L_1 - L_2 = +- j lambda` (the paraxial `lambda D / s`) | **reached in the limit of every direction** with the exact phase at the click (record 156's bright bands 23.5 apart against the exact law's 23.3; L1's `64/0, 32/32, 0/64` the two-path rule registered) | the wheel, the fan's comb, the arrival's floor, the isqrt |
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
| 5 general relativity | Poisson and the retarded wave equation of the delay field; the redshift at first order; Newton's geodesics; the general flux | the redshift at second order, no horizon; the meeting's delay `~ M / b` | Einstein's equation; the rows' bending on `main`; the post-Newtonian terms |
| 6 the information cost | Holevo; Born and Tsirelson as limits; the click's square as a positive quadratic form with the power 2 and `sum a_i^2` derived (the lattice Gleason, 6.5); the click without amplitudes, `f^T G f` on the tables' Gram matrix, bit-identical (6.7); the visibility of two rows; `E = (h N) f`; **New**: the cost per record and the boundary as quantities | the partial read (a step) | Landauer; the click's harmonic constants `c_j` (Gleason's free state), register-pinned to the fundamental |
| 7 Young and Bohr | Young's fringes in the limit of every direction (the exact two-path law, `lambda D / s` its paraxial form); Bohr's `2 pi p r = j h` and `r_j ~ j^2` | the spectrum at the orbital frequency | the levels' energies and the Rydberg lines |

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
  at the interval's rate and its rows carry the clock's slowing only
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

## 10. Lorentz from a detector: the bond as a light clock, on paper

The owner (record 162, as the Boss relayed it): "Lorentz is derived from
a detector; a moving body is a detector moving over the Nodes". Target 4
is then operational, not a symmetry of the lattice: Lorentz emerges if
and only if a body's clock and its length are made of rays at c. A light
clock between two Nodes of the body slows by `gamma`; a length held by
exchanged rays contracts; a moving detector measuring c by round trips
reads c. Today the body's clock is a counter of intervals that does not
slow with motion (section 4.3). Binding-v1's bond (note 40) and the
strong exchange of series I are already a light clock: two bodies at one
Link exchanging rows every interval. This section derives that clock's
period at rest and in motion, on paper, from the flight table and the
crossing rule, against `gamma`; then the counter against the exchange,
and whether the rule "the body's clock is its own exchange" is one of
the six operations. Every integer below is derived; the ones the register
holds are named; the run is pinned for the experimenter after the
crossing rule lands.

### 10.1 The exchange at rest: the registered deuteron

The geometry of `deuteron_1` and `deuteron_1_kick` (`examples/events/
nucleus/make_worlds.py:158-161`; the README's base): the proton p at (10,
10, 10) and the neutron n at (11, 10, 10) in an open 21^3 cube, each
releasing one row of `nuclear` per direction of the 290-direction fan at
every self-creation (`release` [1, 1], `suspension` 0), the strong column
G = 10000 with the lifetime 3; the kick world adds opposite momenta
`-10^12` and `+10^12` on x. The exchange is the rows whose first Link is
on the axis toward the partner: 57 of the 290 directions (the README's
`U(1) = 3008`, the sum of their unit labels' x components; the arithmetic
check of this section reproduces 57 and 3008). A row released at the
self-creation of tick t makes its first Link at age 1 (`m(1) = 1` on
every direction of the fan) and is read by the partner at tick t + 1: the
transit is 1 interval, the round trip 2, and the partner reads 57 rows
per interval from tick 2 on. Registered: the push on p `310 967 280 640`
per interval toward n "from tick 2" (I1's expectation, met), 0 steps in
3000 intervals, the label 0 after each hand-over. So at rest the bond
exchanges at the rate 57 per interval each way, the round trip 2
intervals, `c_first = 1` Link per interval on the first Link (the
flight's first step is at age 1; the mean pace `32 / 55` shows only from
the second Link: ages 1, 3, 5, 7, 8, ...).

### 10.2 The exchange in motion: the pair thrown at v = 1 / k along the bond

Let both nucleons carry the same momentum on +x (not the register's
opposite kicks) so that each steps one Link per k self-creations, k = 4
and 8 (`abs(p) = Q S M / (k - 1)`; with `S = 2^28` and `M = 1837`, `Q S M
= 3.156 x 10^13`: `p = 1.052 x 10^13` at k = 4 and `4.51 x 10^12` at k =
8, above the register's kick of `10^12`). Two bodies at one Link cannot
step into each other: the rear body's step onto the front body's Node is
refused and hands its component over (`engine.py:661-766`), so a bound
pair moves front first, rear after. Take the front body B stepping at
tick 0 of each cycle and the rear body A one tick later (the case the
contact leaves when their drives fire one tick apart; a coincident fire
hands A's whole `p_x` to B and breaks the lock, a leapfrog the run will
show). The rows, per cycle of k ticks, with A at Node 0 and B at Node 1
at the cycle's start, B at 2 from the end of tick 0, A at 1 from the end
of tick 1, every release at the body's Node before its step:

- **A's rows toward B** (the forward exchange). Released at tick 0 at
  Node 0: at tick 1 at Node 1, B already at 2: missed; of the 57, the 17
  whose second Link is also +x (`U(2) = 1048` of 3008 in label units; 4 of
  them make it at age 2, 13 at age 3) reach Node 2 and are read at ticks 2
  and 3; the other 40 turn off the axis on their second step and never
  reach B (they end on the border at age 3). Released at tick 1 at Node 0:
  at tick 2 at Node 1, where A now is: they are A's own number, taken
  HOME and re-created at A's self-creation of tick 3 at Node 1 with age 0,
  so they reach B at tick 4: transit 3, none lost. Released at ticks 2 to
  k - 1 at Node 1: read at Node 2 one tick later, transit 1.
- **B's rows toward A** (the backward exchange). Released at tick 0 at
  Node 1: read at Node 0 at tick 1 (A still there); released at tick 1 and
  later at Node 2: read at Node 1 one tick later. Transit 1 always, none
  lost. The crossing rule adds nothing here (no row crosses A's Link the
  other way in A's step tick, none rests at its destination moving
  against it).

Per cycle B receives `17 + 57 + 57 (k - 2) = 57 (k - 1) + 17` of the
`57 k` rows sent to it and A receives `57 k`; the mean forward transit
over the rows received is `(4 x 2 + 13 x 3 + 57 x 3 + 57 (k - 2)) / (57
(k - 1) + 17)`; the backward transit is 1. The round trip and its ratio
to the rest value 2, against `gamma = 1 / sqrt(1 - v^2 / c^2)` with c the
exchange's mean pace `32 / 55` on the axis (the isotropic `1 / sqrt 3`
gives the same to three places):

| k | v | `v / c` | forward rows received per cycle | mean forward transit | round trip | ratio to rest | `gamma` | `gamma^2` (the ether light clock, no contraction) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 1/4 | 0.4297 | 188 of 228 | 1.766 | 2.766 | **1.383** | 1.107 | 1.226 |
| 8 | 1/8 | 0.2148 | 416 of 456 | 1.346 | 2.346 | **1.173** | 1.024 | 1.048 |

**The bond's length.** One Link for `k - 1` ticks of the cycle and two
Links for one tick (between B's step and A's): the mean `1 + 1 / k`, a
dilation by v, where nature contracts by `1 / gamma` (0.903 and 0.977).

**The transverse bond** (the pair side by side on y, both stepping +x in
the same tick; no contact, the steps coincide): the rows released in the
step tick miss the partner (it has moved one Link on x) except the 11 of
the 47 first-step-on-y directions whose second step is +x (10 at age 2, 1
at age 3); the rows of the other `k - 1` ticks transit in 1. Received per
way per cycle `47 (k - 1) + 11` of `47 k`; the mean transit 1.079 at k = 4
and 1.035 at k = 8; the rate of messages received `0.809` and `0.904` of
the rest rate. Against `gamma` (1.107, 1.024): the transverse period's
ratio 1.079 is near `gamma` at k = 4 by coincidence (the lost rows, not
a dilation) and 1.035 against 1.024 at k = 8.

**Verdict.** The bond clock slows in motion, and by more than `gamma`:
**different law**, `1 + 2 / k` at the leading order on the axis (the
whole-interval steps stretch the bond to two Links once per cycle, and
the second Link of a row takes 2 intervals where the first took 1),
against `gamma^2` for an ether light clock without contraction and
`gamma` for nature's; and the exchange is lossy in motion (40 of 228 rows
per cycle at k = 4 on the axis, 36 of 188 transverse), which no light
clock is. The bond's length dilates by `1 + 1 / k` and does not contract.
A moving detector made of this bond would not read c by round trips: it
would read a longer round trip forward than back (1.766 against 1 at k =
4), the lattice's frame visible one-way and two-way alike, because the
exchange's rows are on the flight table and the bodies step on whole
Links. The register's number this rests on is the rest exchange (the
push from tick 2, 0 steps, the label 0 after each hand-over); the moving
integers above are pinned and unchecked.

### 10.3 The counter against the exchange

The body's clock counts every interval in which nothing is owed
(`engine.py:444-451`): in the cycles above both bodies tick k times per
cycle at every v, while the bond exchanges `57 (k - 1) + 17` rows forward
and `57 k` back per cycle, with the round trip `2 + 4 / k` to the leading
order. A clock made of the exchange would run at the rest rate over the
round trip's ratio, `1 / 1.383` at k = 4 and `1 / 1.173` at k = 8, and the
counter runs at 1: the two clocks of one body disagree in motion, and
neither agrees with `gamma`. This is the operational content of section
4.3: the law's clock is the counter, and the register's stars (G2's
`coasting_none`, `z = v / c` per star within the grain) read the
counter's rate, not the exchange's.

### 10.4 The rule that would make the body's clock its own exchange

**As a torus operation.** "A body self-creates when it has received its
bond's round trip" is a count on the record with the rate the arrivals
of the bond family: `acc_bond += (bond rows received this interval)`; a
self-creation when `acc_bond >= d`, `acc_bond -= d`, with d the rows of
one exchange at rest (57 per interval per partner on the register's fan,
or the declared bond's rows). That is F's feedback block (section 0), one
row of the counts table with the rate a reading (like the owed count's
presence), local (the body's own arrivals), no register at a Node: **one
of the six operations**. Under it the body's clock slows exactly by the
exchange's loss and delay: to `0.809` of the rest rate transverse and to
the received fraction `(57 (k - 1) + 17) / (57 k)` forward-side at k = 4
(0.825), the two bodies of one pair disagreeing (A receives every row, B
does not): a clock that slows with motion, anisotropically, and not by
`gamma`.

**What Lorentz needs beyond it, and whether it is an operation.** The
light clock's `gamma` on the axis needs the bond to contract by `1 /
gamma = sqrt(1 - v^2 / c^2)` so that the longitudinal round trip equals
the transverse one; on the lattice the bond is whole Links held by the
contact rule (one Link, or two for a tick), and no operation of section 1
produces a square root at run time but the meeting's `isqrt` (section
1.3 item 10, a rounding whose remainder no record owns) and the load-time
`u_d`, `T_d`. A contraction of a one-Link bond is not representable; a
bond of L Links contracted to `floor(L / gamma)` would need `gamma` from
the body's own momentum, `1 / sqrt(1 - (p / (Q S M + p))^2 / c^2)`, a
root of a rational function of the state: **not one of the six
operations**, and not derivable from them (the six are translations,
bilinear forms, permutations, group-ring sums, the evaluation and the
division; none takes a root). So: the clock as the exchange is a torus
operation and gives a slowing that is not `gamma`; the contraction that
would make it `gamma` is not, and the honest statement is that Lorentz's
`gamma` is not reached by a rule of the six, whether the clock is the
counter or the exchange. What the exchange clock does reach is the
first-order fact that a moving bond's messages take longer forward than
back and are partly lost, a preferred frame read by the bond itself.

### 10.5 The run, pinned before it (for the experimenter, after the crossing rule lands)

The geometry of `deuteron_1_kick` with both kicks on +x at the momenta
above (k = 4 and k = 8), the crossing rule built, 200 intervals; the
readings from `events.jsonl`'s `read` lines per body per tick (the
`nuclear` rows) and the `step` and `contact` lines:

1. At rest (the register's `deuteron_1`): 57 `nuclear` rows read per body
   per tick from tick 2; the push `310 967 280 640` per interval; 0 steps
   (registered).
2. In motion, if the pair moves front-then-rear one tick apart: per cycle
   of k ticks the rear body reads 57 per tick; the front body reads 0, 4,
   70, 114 over the ticks after its step at k = 4 (0, 4, 70, 114, 57, 57,
   57, 57 at k = 8), `188` per cycle at k = 4 and `416` at k = 8 of the
   `57 k` sent; 40 rows per cycle of the rear body's fan end on the border
   `lifetime` at age 3 without a reader; the `read` line's push on the
   front body in the tick after its step 0, the strong part of the next
   tick `240 x (10^8 + 1837)` in label units (the 4 age-2 rows' x
   components, 240 of 3008).
3. If the drives fire in the same tick, the rear body's refused step hands
   its whole `p_x` to the front body (a `contact` line with `component`
   `10^13`-sized), the front body steps at its next fire with `2 p`, and
   the pair leapfrogs: the cycle above does not form, and the reading is
   the contact lines' sequence; pinned as the alternative, not as the
   expectation.
4. Transverse (the pair at (10, 10, 10) and (10, 11, 10), both kicked +x):
   47 rows per tick per body at rest from tick 2; in motion `47 (k - 1) +
   11` per cycle per body, the 36 lost rows per cycle on the border.
5. The bodies' clocks: k self-creations per cycle at every v (the counter),
   registered as the law's rule; a slowing of either body's clock in the
   run refutes section 4.3 and this section.

What refutes 10.2: a front body reading 57 in the tick after its step
(then the crossing rule reads the rows it was derived not to), or more
than `57 (k - 1) + 17` per cycle, or a round-trip ratio at k = 4 below
`gamma` = 1.107.

## 11. The GameBoard as one vector map between events: the event-driven form of the interval, its bit-identity, and its count

**The question** (the owner's, 2026-09-21, translated: "think also whether
the whole lattice can be moved to something vectorial, so that one need
not jump one by one; that the lattice itself, or the space, enters the
formula of the vectors"; the Boss's item, record 190). The answer here:
the interval stepping of `nature_beam.py` and `engine.py` is bit-identical
to an event-driven form in which the whole state is one vector **s** on
the product torus advancing linearly between events, and the lattice
enters through the flight's closed form; what the event form removes is
the idle intervals and the idle Nodes, and what it cannot remove is the
events and their order. The host script beside this document,
[event_count.py](designs/derivations_beam/event_count.py) with its output
[event_count.out](designs/derivations_beam/event_count.out), counts the
events against the intervals and the active Nodes on five registered
worlds (each run in-process for its own ticks, a reproduction of
registered integers, no engine change).

### 11.1 The linear block: the lattice as the translation group, the shift operator and the flight's closed form

The GameBoard is the torsor of its translation group `Z_X x Z_Y x Z_Z`
(a periodic axis a circle, an open axis a segment whose ends are the
faces): the group acts on the Nodes simply transitively, the Node chosen
as the origin is the identity, and the six Ports are the generators; the
collision table's two rest slots ("here a", "here b", BEAM_LAW section
4) represent the identity twice, a wording item for the physicist, not
changed here. A
direction **D** of the world's table gives the shift operator **S**_D: the
translation of a row's Node along its digital line by one Link. Its t-th
power on a row born at the Node **x**_0 is one lookup and no stepping:

    x(tau) = x_0 + line_D[m_D(tau)],   m_D(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D)),

`line_D` the Bresenham prefix of the direction (the deficit ladder of
section 1.4, `flight.lines`) and `m_D` the Manhattan count (the
accumulator started at `T_D`, rate `2 S_1 Q`, wall `2 T_D`), so the k-th
Link of the row falls at the age

    tau_k = ceil((2 k - 1) T_D / (2 S_1 Q)),   k = 1, 2, ...

the age at which the accumulator crosses its wall the k-th time. The
phase is a closed form too: `k m_D(tau)` under the integer form of
`phase_per_link`, `floor(tau n / d)` under the pair form (the sum of
`by_clock_rows` over the ages telescopes). A record's rows at a click are
therefore the sum of closed forms: at an end Node the element
`f = sum over the rows that reach it of amount x x^(phase_0 + floor(tau_row n / d))`,
`tau_row` the first age at which the row's line reaches the Node (the
inverse of the lookup), and the click's weight is `f^T G f` (6.7): the
two-slit click is computed at the click time, no interval stepped, which
is what record 156's map did for `slits_low` and what reproduced its 64
registered clicks (7.1, 6.7). In the evaluation at `zeta_N` the
translations become phases: `ev(x^(floor(tau n / d))) = zeta^(floor(tau n
/ d))`, the t-th power of the shift a phase factor, the plane wave of
target 7 with the lattice inside it (the L1 count `m_D`, the Euclidean
time `T_D`, the line's rounding). That is the sense in which "the lattice
itself enters the formula of the vectors": through `m_D(tau)` and
`line_D`, not through a step.

### 11.2 The whole board between two events: one vector on the product torus

**The state vector.** Every count of the law is an accumulator `(s, r, d)`
on a record and nothing at a Node (the fraction-free law, BEAM_LAW note
41; section 0). Per row: the Manhattan count (wall `2 T_D`), its three
axis deficits (the ladder), its age (rate 1, no wall), its phase (rate
`phase_per_link` per Link or `n / d` per interval, the wall d, the whole
part read mod N). Per body, the rows of its `CountTable`
(`measured.py:205-316`, one loop `advance`, one primitive `by_drive`,
`core/integer.py:77`): the turn (rate `content x n`, wall d), the count
owed (rate `k x n`, k the presence or the age moment, wall d; then the
countdown `owed -= 1` per interval, rate 1), the release per family (rate
`held x n`, wall d), the lamp (its rate `[n, d]`), the push per column
and axis (rate the column's lifted numerator of the arriving flow, wall
`Lambda_c^2`), the doppler weight per direction and axis (wall `G Q
|v_d|^2`), the drive per axis (rate `p_a`, wall `Q S M + |p_a|`, the cap
one per self-creation, signed). Per record: the birth wheel u (rate 1
per birth, wall N), the live count (rate 0, the ends subtract). So **s**
is one integer vector on the product of the components' tori, `prod_i
Z_(d_i)` on the walled components and `Z` on the ages, and the rate
vector **r** is a function of **s**.

**Between events.** A rate changes only at a carry, because every rule
that reads the state reads it at a carry (11.3 (ii)). So between two
events

    s(t) = s(t_0) + (t - t_0) r,   componentwise, exactly (integers, no rounding),

and the next event is the first carry of any component,

    t* = t_0 + min over i with r_i > 0 of ceil((d_i - s_i) / r_i)

(a component whose rate is 0 or of the wrong sign never carries; the
signed drive carries at `-D` on the negative side; a component with the
cap `at_most = 1` carries at every interval once `|r_i| >= d_i`, else by
the ceiling: its count by t is `min(t, floor((s_0 + t |p|) / D))`, exact
under the cap). The carries at `t*` are then taken in the interval's
order, and the rates re-read at the Nodes touched and their six
neighbours.

**The interval's order**, which the event form keeps as the total order
on the carries of one `t*` (every rate is per interval, so `t*` is an
integer and simultaneity is exact): (0) the frame, every body at once
(the turn's carry, the countdown of a wait; the content, the charges and
the momentum read once for the interval), before (1) the walk, every row
at once (its Link by the flight table at its age; the escapes click on
the faces in Port order), (2) the readings of the arrivals per Node, (3)
the collision per Node per class in (number, content) order, (4) the
tables: the measured events by number, then the declared detectors, the
faces, the border (the clicks, the re-emissions, the gates, the
rotations; the pushes on the bodies), (5) the self-creations by number
(the transformation's trigger, the lamp, the release), (6) the border
`lifetime`, then the merge (the normal form with the cancel); then, in
`engine.step`, the count owed by number and the drive by number with the
axes x before y before z, a coincident fire on a later axis lost (its
wall subtracted, no Link). Two bodies stepping toward one Node in one
interval: the lower number steps, the higher is refused and reads the
occupant's table (the contact): the number order is data of the law.

### 11.3 Theorem: the event-driven form is bit-identical to the interval stepping

**Statement.** Let the events be the carries of every component of **s**
listed in 11.2, taken at their integer times in the interval's order,
with the rates re-read after each event at the Nodes touched and their
six neighbours, and with the collision scheduled at every interval at a
Node whose single units form a moving state (below, (iii)). Then the
sequence of states at the events, and the state at every interval read
off the closed form between them, are the same integers as the interval
stepping's, on every world of `beam-v1`.

**Proof.** (i) Every component's rule is `by_drive` (a body's counts, the
drive) or a constant-rate count read off the age (a row's Manhattan
count and deficits, its phase, the age itself, the countdown of a wait):
between carries `by_drive` applied k times at a constant rate r with no
carry is one addition, `s + k r` (it adds r and subtracts nothing while
`|s| < d`), and the closed forms of 11.1 are exactly the same integers
(section 1.4: the accumulator equals `m(tau)` on seven directions over
600 intervals). So the state between events is the linear formula, bit
for bit. (ii) Every rule that reads the state reads it at a carry: the
tables and the detectors read the arrivals, the rows that crossed a Link
this interval (`arrival = where(moved, direction, NO_ARRIVAL)`,
`nature_beam.py:2464`; `read_arrivals`, `439-460`: "(0, 0, 0) for one
that did not step"); the readings' resident amounts (the presence k, the
age moment) are rates of the owed count, constant between a Link in and
a Link out, the age moment linear in t (its accumulator then gains a
linear rate, a quadratic closed form, its carry the first t where a
quadratic in integers crosses the wall: the one place the scheduler's
`t*` is a root, `isqrt`, and not a ceiling of a quotient; exact all the
same); the clicks act on arrivals; the merge (`4149`) fuses rows equal in
every identity field, which two rows become only by a Link or a birth;
the contact reads a body's Link; the border, the age bound and the
`become` trigger compare the age with a key, a wall on the age (rate 1);
the push changes the momentum, the drive's rate, at a reading of
arrivals; a release or a birth creates components at a carry of the
release's or the lamp's accumulator, and the lamp's discard (note 41
(iii): a self-creation of turn 0 or outside the window releases nothing
and loses the count) happens at a carry of the lamp's accumulator and
nowhere else (`3599-3606`). (iii) The one rule that acts on rows that made
no Link is the collision: `collide` (`2345-2390`) permutes every single
unit on a heading or a rest slot at a free Node, arrived this interval or
not (`eligible` is not filtered by `moved`), and on the table every
moving state lies on a cycle: 2132 of the 6561 slot states move, and none
of them reaches a fixed state under repeated application (checked on
`collision_table()`: 4429 fixed states, 2132 on cycles, 0 moving states
whose target occupies the same slots). So a moving group at one Node is
permuted again at every interval it stays co-located. In the event form
this is a count of rate 1 and wall 1 at that Node while its condition
holds: after each firing the next event at that Node is scheduled at
`t + 1`, no interval is skipped there, and the integers are the same; the
gain is nil at such Nodes (no acceptance world has a collision act, BEAM
LAW section 4; series C's rings do). (iv) Simultaneous carries: `t*` is
an integer, so the set of carries at `t*` is exactly the set the stepping
finds in that interval, and the interval's order of 11.2 is a total order
on them; the event form applies the same order. The three places where
the order changes the integers, each kept: the drive's coincident fire
(the first axis in x, y, z order makes the Link, a later axis's fire is
lost with its wall subtracted: an event without a Link, scheduled as
one, `engine.py:585-592`); two bodies toward one Node (the lower number
steps first, the higher meets the occupant: the contact); the collision's
class order (number, then content). (v) The rates re-read at every
interval today although the state did not change: the frame reads
content, charges and momentum every interval (constants between events);
the drive advances at every self-creation (linear, (i)); the readings
are recomputed at every Node with arrivals and are empty without; under
the meeting key the crowd's flow and its norm are read every interval,
a function of the resident rows, constant between a Link in and out; the
lamp's accumulator advances at every self-creation (linear, its carries
the births or the discards). A re-read of an unchanged state returns the
same rate, so the linear formula between events is the stepping's own
sequence of additions: nothing changes. (vi) What would break it: a rule
that changes the state at an interval with no carry anywhere. There is
none in the rows (the walk, the phase, the age, the merge, the clicks
are carries or linear); in the bodies the countdown of a wait and the
age are linear; the collision is (iii). The theorem holds. QED.

**What the theorem says and does not say.** It says the stepping is a
scheduler that visits every Node at every interval and finds nothing at
most of them; the event form visits the carries. It does not say the
events are fewer than the intervals: a lamp paying at every birth changes
its own rate at every birth (an event per interval), a body in a crowd
takes a push at every interval rows arrive (an event per interval), a
row in flight makes a Link every `T_D / (S_1 Q)` intervals on the
average (1.7 on a heading, 1.2 on a face diagonal, 1 on a cube diagonal:
an event per Link). The count below is that ratio on the register.

### 11.4 The count: events against intervals x active Nodes on five registered worlds

Each world run in-process for its own ticks by `event_count.py`; per
interval the host counts the carries it can read from the state: the
Links of rows (the flight table's step at their age, read before the
interval), the Links of bodies, the clicks (every end), the rows born,
the pushes taken (a body's momentum changed), and the Nodes active
(holding a row or a body) after the interval; the merges and the
collisions are not counted (the store reports neither; both happen at a
Link or a birth, so the events are undercounted by the merges alone).
The registered integer each run reproduces is named in the last column.

| World (the series) | Nodes; intervals run | Links of rows per interval | clicks per interval | rows born per interval | momentum changes per interval (pushes, recoils) | active Nodes per interval | events (Links + clicks + births) against intervals x active Nodes | against intervals x all Nodes | the registered integer reproduced |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `slits_low` (L2) | 7260; 230 | 9428.6 | 96.2 | 175.9 | 5.8 | 3426.6 | 2 231 147 against 788 126: **2.83** | 1.34 | the 64 clicks: wall 34, screen 15, faces 15 |
| `bell_16_24` (L3) | 21; 80 | 18.4 | 3.5 | 4.0 | 1.8 | 12.5 | 2068 against 1001: **2.07** | 1.23 | the cells 27, 5, 5, 27 |
| `cone_links` (L7) | 323; 96 | 34.1 | 1.4 | 2.0 | 3.4 | 36.9 | 3597 against 3544: **1.02** | 0.12 | every record clicks at the age 29 |
| `deuteron_1_kick` (I2b) | 9261; 2040 of 3000 (the script's seven-minute cap) | 12 076.6 | 1152.9 | 1160.0 | 2.0 | 4563.7 | 29 354 628 against 9 309 919: **3.15** | 1.55 | no Link of either body: the drive fired 113 and 106 times and the 219 fires were booked as the occupants' contacts, every fire refused |
| `coasting_none` (G2) | 27 270 901; 400 | 5924.3 | 38.7 | 79.6 | 24.9 | 692.7 | 2 418 536 against 277 090: **8.73** | 0.00022 | the 24 thrown stars' `|p(end)| / |p(0)|` 1.0000 to 1.0000 (the README's 1.000) |

Read: on every world the events outnumber the active Node-intervals
(the rows make a Link every 1.2 to 1.7 intervals and several rows share
a Node), so an event form gains nothing over the stepping where the
board is dense: the two slits, the pair, the cone and the deuteron are
dense (12 to 50 percent of the Nodes active), and there the ratio against
all the Nodes is above 1 too (0.12 on the cone: the one sparse case of
the four). It gains where the board is empty: G2's throw has 693 active
Nodes of 27 million, so the stepping visits 39 000 empty Nodes per event
(the ratio `2.2 x 10^-4`), and the event form visits the 8.7 events per
active Node-interval only. No interval of any of the five is idle (an
event in every interval: the lamps and the releases birth at every
interval, the rows make Links at every interval), so the event form
never jumps over an interval on the register; it jumps over Nodes. The
interactions (clicks, births, momentum changes) are 8 to 74 percent of
the active Node-intervals: the rest of the events are Links in free
space, the trivial carries of 11.5.

### 11.5 What cannot be removed: the order of events, and the feedback block's iteration

**Theorem (the order).** Two events at one `t*` commute exactly when the
Nodes they read and write are disjoint: an event reads and writes the
Node of its carry and, through the readings, the tables, the contact and
the merge, that Node's six neighbours and the set it belongs to
(LOCALITY-1: nothing farther). Events whose neighbourhoods meet do not
commute in general (a body's step refused by the other's; the collision's
class order; a merge of a born row with an arriving one), and the law
fixes their order by the interval's stage, then the number, then the
axis (11.2). So the order of events is part of the law, not of the
scheduler: the event form is local (the next event at a Node depends on
the accumulators there and on the rows in flight toward it), and its
scheduler is a queue of carry times per Node, the min over components,
which LOCALITY-1 allows and nothing else does.

**Theorem (the feedback block).** Across events the feedback block has no
closed form (record 181): the next event time is `t*_(k+1) = phi(s_k)`
with `phi` the min of ceilings of 11.2, a piecewise-linear function whose
pieces are chosen by the state, and `s_(k+1) = s_k + (t*_(k+1) - t*_k)
r(s_k) + (the carries)`; the sequence is a difference equation whose
exact solution is its iteration, and whose limit is the derivation's
differential equation (sections 3 to 5). The linear block's closed form
is the case of no event: a row whose Links meet no table, no body and no
row of its own class (or only spectators) has every Link a trivial carry
that changes no rate, so its state at any t is 11.1's formula and its
first interaction is the first `tau_k` whose destination Node is a set,
a body or an occupied Node, computable from the formula when those are
at rest (the two slits, the cone, the pair) and iterated when they move
(a body in a crowd, a crowd under a body). The event form removes the
idle intervals and the idle Nodes, never an event and never its place in
the order; its cost is the events plus the scheduling, against the
intervals times the active Nodes for the stepping: the table of 11.4.

**Verdict.** **Reached**: the event-driven form is bit-identical to the
interval stepping on every world of `beam-v1`, with the collision the
one rule scheduled at every interval of co-location and the age moment
the one carry whose time is a root; the lattice enters the vectors'
formula through the flight's closed form `x_0 + line_D[m_D(tau)]` and its
evaluation at `zeta_N`. **Not removable**: the events and their order
(LOCALITY-1), and the feedback block's iteration (record 181), the linear
block's closed form being the case of no event. The count on the
register is the table of 11.4.

## 12. Lorentz from the delay field, without a seventh verb

**The question** (the owner's, 2026-09-21, translated: "so how do we solve
Lorentz?"; the Boss's item, record 200). **The claim to prove or refute**:
gamma (the Lorentz factor) is not an operation of the law but the limit
of a quantity the GameBoard computes in the feedback block, from three
things already decided (c as the cap of every body's drive, record 186;
the push retarded at c, section 5; the pair in motion of section 10) and
one vector operation to add, the aberration of a moving body's fan. The
host script beside this document,
[lorentz_field.py](designs/derivations_beam/lorentz_field.py) with its
output [lorentz_field.out](designs/derivations_beam/lorentz_field.out),
makes every check below on the engine's own flight table (the register's
deuteron fan), a host computation and no run. Throughout, beta (the
speed over the pace of a row, `v / c`) is the body's speed as a fraction
of the rows' pace, `R_ret` the distance from the retarded position of
the source (where it was when the rows now arriving were released), and
`n_ret` the unit vector from that position.

### 12.1 The field of a moving source: the law's push in the continuum limit

**(1) c as the cap.** Under form B (record 186, light_speed/FORM.md
section 3) a body walks the digital line of its momentum's direction at
the Manhattan pace `|p|_1 S_1 Q / (Q S M S_1 Q + |p|_1 T_D)`, a fraction
of a row's pace on that line, never above it: `beta = |p|_1 T_D / (Q S M
S_1 Q + |p|_1 T_D)`, an exact rational of the state. A body moving at
`1 / k` Links per interval on a heading has `beta = (1 / k) / (32 / 55)`:
0.4297 at k = 4, 0.2148 at k = 8 (section 10.2's cases).

**(2) The retarded field of a moving source.** Let a source of the law
move uniformly at the velocity **v** and release q rows per interval on a
fan of every direction (the limit of section 3.2), each row flying at c
on its line and carrying its age. As built the fan is released
isotropically in the lattice's frame whatever the body's momentum (the
directions are the table's, `nature_beam.py:3628-3644`), and the release
rate is the same at every speed (the counter, HYPOTHESES 21, section
4.3). The rows released at the time `t'` from the position `v t'` are, at
the time t, on the sphere of radius `c (t - t')` about that position; the
shells of successive `t'` are not concentric, and at a point **x** their
spacing along the ray is `c (1 - n_ret . beta) dt'` (the derivative of
`c (t - t') - |x - v t'|` in `t'`), so the rows dwelling at **x** are

    P(x, t) = q dwell / (4 pi R_ret^2 (1 - n_ret . beta)),   R_ret = c (t - t_ret),   |x - v t_ret| = R_ret,

the presence of section 5.1 with the retardation factor of a moving
source, and the age they carry is `R_ret / c`, so the age moment is

    A(x, t) = P x R_ret / c = q dwell / (4 pi c (1 - n_ret . beta) R_ret).

That is the Lienard-Wiechert scalar potential of a uniformly moving point
source: the law's retarded potential of section 5.1 (the retarded
Green's function of the wave operator, `A` obeying `(1 / c^2) d^2 A /
dt^2 - Laplacian(A) = (dwell / c) q delta(x - v t)`) evaluated on a
moving source. With the classical identity, checked in the script on a
thousand random points and speeds to `10^-15`,

    (1 - n_ret . beta) R_ret = sqrt(x_par^2 + (1 - beta^2) x_perp^2)      (x from the PRESENT position, x_par along the motion),

the equal-age-moment surfaces are the ellipsoids `x_par^2 + (1 - beta^2)
x_perp^2 = const`, contracted along the motion by `sqrt(1 - beta^2)`:
Heaviside's ellipsoid, exactly, in the continuum limit of the law's own
readings. **Reached** for the potential: the delay field of a moving
source is the retarded field of the wave equation at c, and its
equipotentials are contracted by `1 / gamma`. The equal-PRESENCE surfaces
are not ellipsoids (`(1 - n_ret . beta) R_ret^2` is no quadric): the
question's "equal-presence surfaces" holds for the age moment, the
potential, and not for the presence, the flux.

**The push is not the classical force.** The flow a body reads is the
arriving rows' labels per interval, along `n_ret` (the rows come from
the retarded position) with the magnitude of the presence times the
encounter rate; a partner co-moving with the source meets the rows at
the rate `(1 - n_ret . beta)` times their density (under the `doppler`
key exactly, `flux_pair`, `nature_beam.py:2075-2103`; without the key
through the count of arrivals at its Node per interval), so it reads

    rows received per interval = q a^2 / (4 pi R_ret^2)   along n_ret,   a the Link,

the plain inverse square of the RETARDED distance. The classical field
of a uniformly moving charge is `E = q (n_ret - beta) / (4 pi eps (1 -
n_ret . beta)^3 R_ret^2)`, which points from the present position and
carries the magnetic term; the law's push has no `- beta` term and no
cube of the retardation factor: it points to the retarded position. For
a co-moving pair at the separation d along the motion the retarded
distances are `d / (1 - beta)` to the front body and `d / (1 + beta)` to
the rear one, so the two internal pushes are

    forward (on the front body)  (1 - beta)^2 x the rest rate,   backward (on the rear body)  (1 + beta)^2 x the rest rate:

0.325 and 2.044 at beta = 0.4297, 0.617 and 1.476 at 0.2148. An
attracting pair in motion pulls its rear body forward harder than its
front body back: a net push on the pair of `4 beta` times the rest push
along the motion, at first order in beta, and the field's momentum that
would balance it is not booked (a free release takes no recoil,
`nature_beam.py:3958-3962`: "a free release is the field and takes
none"), so the momentum of bodies and field is not conserved for a pair
in motion. Transverse, at the separation d across the motion, `R_ret =
gamma d` and the rate is `(1 - beta^2)` times the rest rate (0.815 and
0.954), the push along `n_ret`, tilted backward by the angle whose sine
is beta: a drag on a transverse pair of `beta` times the push, at first
order. The classical field gives the longitudinal force `(1 - beta^2)`
and the transverse `1 / gamma` (0.903 and 0.977), both along the present
separation, no net force and no drag. **Different law** for the force
between co-moving bodies: the retarded flux, first-order asymmetric and
dragging, where the classical field is symmetric.

**The bound pair's separation.** Every column of the law is an inverse
square with the one constant G (section 3.4: the ratio of two columns'
pushes is `-rho_A rho_B` at every r), so two bodies have no equilibrium
separation from their pushes: they attract or repel at every distance,
and a bound pair is held by the contact (one Link, the refused step,
section 10.2) or by a family's lifetime L (whole Links). There is no
force balance to contract: the question "does the equilibrium separation
contract by `1 / gamma`" has no object in the law. **Refuted** for the
contraction, by absence: the bond is a whole Link.

**Where the law differs from the classical field, named.** (i) The push
reads the retarded flux along `n_ret`, not the gradient of the retarded
potentials with the vector potential: no magnetic term, no `(n_ret -
beta)`. (ii) The fan is isotropic in the lattice's frame: the preferred
frame is the frame of emission. (iii) The flight is Manhattan on the
lattice, Euclidean to `T_D`'s 1.35 percent per direction, and the fan's
grain (290 directions on the register) sets the angular resolution of
`n_ret`. (iv) The counter's rate is one at every speed.

### 12.2 Aberration: the missing vector operation, its integer form, and what it costs

**The rule.** A moving body's released direction is the fan's direction
plus its velocity, brought to the table's nearest direction by the exact
comparison. With the row's velocity `(Q / T_D) D` on the direction **D**
(BEAM_LAW note 38) and the body's velocity **v** `= p S_1 Q / (Q S M S_1
Q + |p|_1 T_(D_p))` under form B (a rational vector: the numerator vector
`N_v = p S_1 Q`, the denominator `W`), the aberrated vector is the
integer vector

    w = Q W D + T_D N_v,        D' = the table's direction nearest to w: (w . D')^2 |D''|^2 >= (w . D'')^2 |D'|^2 for every D'', w . D' > 0,

no root (FORM.md section 3's choice of the drive's line, with w in place
of **p**; w shifted to components within `2^20` as that choice shifts
**p**, since `Q W` reaches `2^58` on the register's contents), a
translation (T) and a comparison (D): one of the six. At the register's
speeds `v = 1 / k` on a heading, `w = k Q D + T_D e_x`.

**In the continuum limit.** The map `n -> (n + beta e_x) / |n + beta
e_x|` (the Galilean aberration; the rows still fly at c on the new
direction) changes the fan's density per steradian by the Jacobian `J =
(1 + 2 beta cos theta + beta^2)^(3/2) / (1 + beta cos theta)` at the fan
angle theta that maps to the arrival direction: `(1 + beta)^2` forward,
`(1 - beta)^2` backward, `(1 + beta^2)^(3/2)` near the transverse. The
co-moving exchange rates become

    forward (1 + beta)^2 (1 - beta)^2 = (1 - beta^2)^2,   backward the same,   transverse J (1 - beta^2):

0.910, 0.910, 1.023 at beta = 0.2148 and 0.665, 0.665, 1.083 at 0.4297,
against the classical `(1 - beta^2)` = 0.954, 0.815 and `1 / gamma` =
0.977, 0.903. The first-order self-force of 12.1 vanishes (the two
internal pushes are equal); the transverse drag stays (the push is still
along `n_ret`); the longitudinal rate is the square of the classical
one, the transverse above one where the classical is below. **Lossless
in the limit** in the sense asked: every row aimed at the partner's
arrival point reaches it, the fall of the rate being the geometry of the
retarded distance, not a miss, and the fan's grain the only loss.

**On the lattice at one Link** (the register's bond), by the flight table
at k = 4 and 8, the exchange counted as in section 10.2 (the script
reproduces 10.2 first: 57 first-Link directions, 4 and 13 rows to Node 2
at ages 2 and 3, 188 and 416 forward per cycle, 152 and 340 transverse),
then with every direction replaced by its aberrated one:

| k | `v / c` | first-Link +x directions (rest 57) | rows to Node 2 at age 2 / 3 (rest 4 / 13) | forward received per cycle (rest 188, 416) | backward: first-Link -x directions (rest 57), received per cycle (rest 228, 456) | transverse: first-Link +y (rest 47), to (1, 1, 0) at age 2 / 3 (rest 10 / 1), received (rest 152, 340) |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 0.4297 | 93 | 8 / 17 | 304 | 29; 116 | 45; 22 / 0; 157 |
| 8 | 0.2148 | 73 | 8 / 17 | 536 | 41; 328 | 47; 18 / 0; 347 |

At one Link the aim is all-or-nothing on the first Link (the on-axis
partner is hit by the first Link alone), and the whole fan tilts forward:
the forward exchange gains (304 of the rest 228 sent per cycle at k = 4)
and the backward one is starved (116 of 228; 29 first-Link -x directions
of 57). The lattice's exchange under the rule is not lossless and not
symmetric: it is asymmetric the other way, by the first-Link rule, not
by the continuum's geometry. The rest counts stand on the register (the
push from tick 2, 0 steps); the aberrated ones are pinned in 12.4.

**The recoil.** A paid emitter takes as its recoil the momentum less
the born rows' labels (`nature_beam.py:3958-3966`); at rest the fan's
labels sum to 0, and the aberrated fan's sum to `5156` (k = 4) and
`2980` (k = 8) label units on +x per unit of amount on each direction
born (the continuum's `(2 / 3) K beta Q` = 5317 and 2658). So a lamp in
motion takes a recoil against its motion at every birth: momentum is
conserved between the lamp and its rows exactly, and the lamp is slowed
by its own light unless the content it pays per birth lowers its wall
`Q S M` in the same proportion, which happens only if `h s S c = 2 / 3`,
a coincidence of declared constants (the content and the momentum of a
body are untied, section 6.4: the law has no `E = m c^2`). A free
family's release takes no recoil, so an aberrated field carries net
momentum forward, created and unbooked, the first-order asymmetry of
12.1 replaced by an unbalanced field. The rule costs momentum
conservation between bodies and field in one form or the other; the
choice of which is the owner's, not derivable.

### 12.3 The bond clock under (1) to (3)

**The continuum.** The exchange's transits along the motion are `d / (c
- v)` forward and `d / (c + v)` back, the round trip `2 d c / (c^2 -
v^2) = gamma^2 x 2 d / c`; across the motion the retarded distance is
`gamma d` each way, the round trip `gamma x 2 d / c`: the ether light
clock, `gamma^2` along and `gamma` across, with or without the aberration
(the aberration changes which rows arrive, not when). Lorentz's own
argument makes the two equal by contracting the longitudinal arm by `1 /
gamma`, and 12.1 finds no object to contract: the bond is a whole Link.
So under (1) to (3) the bond clock slows anisotropically, `gamma^2`
along and `gamma` across, and the body's own counter does not slow at
all (section 4.3). At beta = 0.4297: 1.226 along, 1.107 across; at
0.2148: 1.048 and 1.024.

**On the lattice** (the script, k = 4 and 8): the round trip along the
motion is `1.375` and `1.175` times the rest value with the aberration
(1.383 and 1.173 as built, section 10.2), the transverse mean transit
`1.140` and `1.052` (1.079 and 1.035 as built): farther from `gamma` than
the continuum's ether clock, by the whole-Link steps and the first-Link
rule, as section 10.2 found; the aberration moves the transverse period
away from `gamma` (its rows arrive at age 2 in place of 1).

**The root.** `gamma` appears in the transverse period, `2 gamma d / c`,
and in the law it appears there without a seventh verb: the row aimed at
the transverse co-moving partner flies the direction `(beta, sqrt(1 -
beta^2))`, whose Euclidean length the flight table holds as `T_D =
isqrt(3 |D|^2 Q^2)`, the root taken once at load (section 1.5, class R
at load), and the digital line's Links realise it interval by interval.
The root is in the closed form of the transit and in the table's
constant, never an operation at run time: the point section 10.4 made
for the contraction holds here in the other direction, for a period. What
the board iterates the pair to is not a contracted equilibrium (there is
none) but the anisotropic ether clock.

**Section 10 reconciled.** The rigid-bond result stands: 1.383 at 0.43 c
as built, 1.375 with the aberration, against `gamma` 1.107 and `gamma^2`
1.226. The contraction is a root of the state in the exact sense that a
rule imposing it needs the seventh verb (lorentz-v1); the transverse
exchange shows `gamma` without the verb because the root sits in the
flight table; and no quantity of the feedback block converges to
`gamma` as an isotropic slowing of a body's own clock.

### 12.4 The pins for the run, written before it

The physicist's pair in motion (section 10.5) under form B and the
aberration rule of 12.2: the geometry of `deuteron_1_kick`, both
nucleons kicked +x, the crossing rule and form B built, the aberration
rule as stated, 200 intervals. Under form B the momentum that gives `v =
1 / k` on a heading is `|p| = Q S M x Q / (k Q - T_D)` with `T_D = 110`:
`1.383 x 10^13` at k = 4 and `5.03 x 10^12` at k = 8 (`Q S M = 3.156 x
10^13`); the counts below are integers of the flight table (no
tolerance), the continuum comparisons carry the flight's 1.35 percent
on c (`beta` 0.424 to 0.436 at k = 4, `gamma` 1.104 to 1.110, `gamma^2`
1.219 to 1.233).

| k | `v / c` | separation | ticks per cycle per body | forward received per cycle | backward received per cycle | transverse received per cycle | mean forward transit | round trip, x rest | lost per cycle on the border, forward |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 0.4297 | 1 Link for k - 1 ticks, 2 for one (mean 1.25) | 4 (the counter) | 304 (188 as built) | 116 (228) | 157 (152) | 1.750 (1.766) | 1.375 (1.383) | the 93 first-Link rows of tick 0 less the 25 that reach: 68 |
| 8 | 0.2148 | 1 Link for k - 1 ticks, 2 for one (mean 1.125) | 8 | 536 (416) | 328 (456) | 347 (340) | 1.351 (1.346) | 1.175 (1.173) | 73 - 25 = 48 |

What refutes 12.2 and 12.3: a forward count at k = 4 other than 304 (the
rule as stated and the pair moving front-then-rear as in 10.2; the
leapfrog of 10.5 (3) is the pinned alternative), a backward count other
than 116, a transverse count other than 157, or a body's tick count
other than 4 per cycle (which would refute section 4.3 first). What
refutes 12.1's continuum: a pair whose separation, held at two Links or
more by a lifetime, shows a net push along its motion other than `4
beta` times the rest push at first order (the doppler key off), or a
transverse pair with no drag.

**The muon of J4 as a bond clock.** The muon of HYPOTHESES 21 is one
body with no partner: no exchange, no bond clock; under (1) to (3) its
`become` at 64 turns fires at tick 64 at every speed (the counter), and
it reads `gamma` (ticks 71 and 126 at `f_c` 0.43 and 0.86) only under
lorentz-v1's seventh verb. Read as a bond clock it would need a partner
exchanging rows and would then slow by the exchange, `gamma^2` along
and `gamma` across in the limit (`1 + 2 / k` on the lattice at one
Link), anisotropically: nature's muon slows by `gamma` isotropically,
which is not a bond clock's slowing in this law.

### 12.5 The verdict of section 12

**Partial**, in these lines. (i) **Reached**: the age moment of a moving
source is the Lienard-Wiechert potential, the retarded field of the wave
equation at c whose equipotentials are Heaviside's ellipsoids contracted
by `1 / gamma`, from the law's own readings in the limit. (ii)
**Different law**: the push is the retarded flux to the retarded
position with no magnetic term, so the pushes between co-moving bodies
are `(1 -+ beta)^2` asymmetric as built (a self-force of `4 beta` on a
moving pair, the field's momentum unbooked) and `(1 - beta^2)^2`
symmetric with the aberration, never the classical `(1 - beta^2)` and
`1 / gamma`; a transverse pair is dragged. (iii) **Refuted** for the
contraction: no equilibrium separation exists to contract, the bond
being a whole Link of the contact or a lifetime. (iv) The aberration
rule is one of the six (a translation, then the comparison), lossless
in the limit; at one Link it starves the backward exchange (116 of 228
at k = 4) and gives a lamp a recoil of 5156 label units per unit born.
(v) The bond clock slows by `gamma^2` along and `gamma` across in the
limit and by 1.375 and 1.140 at k = 4 on the lattice; `gamma` enters the
transverse period through the flight table's root at load, in the
closed form and never as an operation. (vi) The seventh verb is not
needed for `gamma` to appear in a period; it is needed for `gamma` to
slow a body's own counter or to contract its bond (lorentz-v1), which
nothing of the six derives.

## 12b. Lorentz revisited: the moving reader's count as the magnetic term, and the orbit as the bond

**The two things section 12 did not have** (the Boss's item after
records 213 to 218): (1) the reader's velocity term, the crossing rule's
count of a MOVING reader (record 158: a body in motion meets a row once
at the crossing of their world lines, C1 the rows that crossed its Link
the other way, C2 the rows resident at the destination moving against
it), the candidate for the missing magnetic term, since in Maxwell's
theory the magnetic force is exactly the velocity dependence of the read
flux; (2) the orbit as the bond: a contact Link cannot contract, but
series D's orbit is a bound pair with a radius set by the push against
the drive, and the pair in motion is that orbit thrown. The host script
[orbit_thrown.py](designs/derivations_beam/orbit_thrown.py) with its
output [orbit_thrown.out](designs/derivations_beam/orbit_thrown.out)
integrates the law's continuum equations for (2) on the registered
`s32_r24` geometry; no run.

### 12b.1 The reader's velocity term

**What the crossing rule gives a moving reader.** Section 2 derived its
limit per direction: a reader moving at **v** through rows of the
direction **n** at the pace c counts `1 - n . v / c` times the rest
count on the headings and the diagonals (2.2: `1 + v / c` head-on, `1 -
v / c` co-moving, exactly 1 transverse, 2.3), and the Manhattan flux `1
+ v T_d / (Q S_1)` on a general fan direction (2.4, the lattice's
departure from the Euclidean `1 + v cos theta / c` by the factor `|D|^2
/ (a S_1)`); the `doppler` key's `flux_pair` (`nature_beam.py:2075-2103`,
`1 - v_body . c_d / |c_d|^2`) is that limit put on the flow as a factor.
In the continuum limit of every direction the moving reader's count is
therefore the rest density times `(1 - n . beta_reader)` per direction,
with `beta_reader` the reader's velocity over c.

**Section 12 already carried it.** The co-moving partner's rate of 12.1
was written as the bunched density `1 / ((1 - n_ret . beta) R_ret^2)`
times the encounter rate `(1 - n_ret . beta)`, the two factors
cancelling to `q a^2 / (4 pi R_ret^2)`: the second factor IS the
crossing rule's count for a reader moving with the source. So the
results of 12.1 and 12.2 stand with the reader's velocity term in them:
`(1 - beta)^2` and `(1 + beta)^2` on the axis without the aberration,
`(1 - beta^2)^2` both ways with it, `(1 - beta^2)` transverse, the
self-force of `4 beta` without the aberration and its vanishing with it,
the drag of `beta` on a transverse pair in both.

**Is it the magnetic term?** On the transverse co-moving pair, yes, in
the number and not in the direction. The rows that reach the transverse
partner fly along `n_ret = (beta, sqrt(1 - beta^2))`, so the reader's
factor is `1 - n_ret . beta = 1 - beta^2`, exactly Maxwell's reduction of
the transverse force on a co-moving charge by the magnetic term (`v x
B` with `B = v x E / c^2` gives `-beta^2 E` across the motion, 0 along
it); and on the longitudinal pair the factors are `1 -+ beta`, the
Doppler of the count, where Maxwell's magnetic term is 0. What the law
lacks is not the velocity dependence of the read flux but the FIELD it
multiplies: the law's is the flux `1 / R_ret^2` along `n_ret` (the
transverse partner at `R_ret = gamma d`: `1 / (gamma^2 d^2)`), Maxwell's
is the potential's gradient, `gamma / d^2` across the motion (the
Heaviside compression of the field lines, section 12.1's ellipsoid read
as a gradient). So with the reader's term the transverse push is `(1 -
beta^2) x rest = rest / gamma^2` against Maxwell's `rest / gamma`, the
longitudinal `(1 - beta^2)^2 x rest` with the aberration against
Maxwell's `(1 - beta^2) x rest`: each one factor of `1 / gamma` short,
and the direction along `n_ret` (a component `beta` along the motion on
the transverse pair, the drag) where Maxwell's is along the present
separation. **Different law**, as 12.1 said, now with the reason named:
the crossing rule is the magnetic term of the count, and the law's push
reads the retarded flux where Maxwell's force reads the retarded
potentials' gradient. The self-force of `4 beta` is gone with the
aberration and not without it; the drag is gone in neither.

### 12b.2 The orbit as the bond: the registered orbit thrown

**The bond that can contract.** Series D's `s32_r24` (the orbit README,
the register's D): a source of content `2^10` fixed at the centre of a
121 x 121 plane releasing 120 rays every 10 intervals on a fan of every
in-plane direction (q = 12 units per interval), the width S = 32, a probe
of content 1 at r = 24 with the tangential momentum 576 label units; the
plane's push `F = m q L C Q / (2 pi r)` label units per interval (a `1 /
r` force on the plane, a flat rotation curve), the circular orbit at `n v
= q L C / (2 pi)`, `n = p / (Q m) = 9`, `v = n / (S + n) = 0.2195` Links
per interval under today's drive, the derived period 687, the registered
closing 623 (the return `(-1, +1)`, the mean radius 23.63, the re-read
under the step drive). Here the radius is an equilibrium of the push
against the drive, an object the contact Link of section 12 was not.

**The equations integrated** (the law's continuum limit, one step per
interval as the engine steps): the drive under form B, **v** `= p / (Q S
m + |p| / c)` along **p** (the cap c; at rest `v = 576 / (2048 + 990) =
0.1896`, the period `2 pi r / v = 795`, longer than today's 687 because
form B prices the cap); the push per interval the retarded flux of the
source moving at `beta c` along x, `F_0 / (R_ret (1 - n_ret . beta))`
rows per Node on the plane (the 2D dilution `1 / R_ret`), met at the
crossing rule's rate `(1 - n_ret . beta_probe)` with the probe's own
velocity, each row's label Q along `n_ret`, and with the aberration the
fan's density multiplied by the plane's Jacobian at the emission angle;
the source unpushed (the register's `fixed`, its content `2^10`), the
probe's position taken relative to the source's present position. At
rest the integration gives the periods 743 and 718 (a slightly
precessing ellipse of extents 22.7 by 23.8) against the analytic 795 and
the register's 623: the continuum's orbit is not the register's polygon
(the burst field, the fan's grain), a 9 percent margin the pins below
carry.

**The registered geometry thrown** (both bodies at `v = 1 / 8` and `1 /
4` along +x, the probe's momentum the throw's `p_t = v Q S m / (1 - v /
c)` plus the orbital 576):

| `v` | `beta` | aberration | turns before the end | period over rest (Lorentz: gamma) | extents along / across (Lorentz: `1 / gamma`) | the relative centre's offset | the end |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1/8 | 0.2148 | no | 1 (857 intervals) | 1.153 (1.024) | 31.4 / 25.9, ratio 1.21 (0.977) | -7.4 along the motion | escapes, r = 200 at 2161 |
| 1/8 | 0.2148 | yes | 0 | - | 37.1 / 30.3 | -13.1, -7.5 | falls in, r = 0.9 at 1074 |
| 1/4 | 0.4297 | no | 0 | - | 93 / 94 | +43, +53 | escapes at 2353 |
| 1/4 | 0.4297 | yes | 0 | - | 59 / 139 | -32, +41 | escapes at 5204 |

The registered orbit does not survive the throw: at `0.21 c` it makes
one stretched turn (elongated ALONG the motion by 1.21, the period 1.15
times the rest) and unbinds, or falls in with the aberration; at `0.43
c` it is unbound both ways. The cause is not the field first but the
drive: `s32_r24`'s orbital speed is `0.33 c` under form B (0.1896 of
0.5818), and the law's dispersion `v = p / (Q S m + |p| / c)` composes
the throw and the orbit as momenta, not as velocities, so the probe's
speed relative to the source is `+0.126` Links per interval forward and
`-0.226` backward at `v = 1 / 8` where the rest orbit has `+-0.190`: the
composition of two motions is not a translation (no Galilean addition,
no Lorentz addition), the relative orbit is sheared, and the retarded
field's asymmetry (`(1 -+ beta)` on the plane) and the drag finish it.

**The Newtonian regime** (the width raised to S = 512 and 8192 with the
momentum of the register's derivation, `n v = q L C / (2 pi)`: the
orbital speed 0.098 c and 0.026 c; the rest periods 2557 and 9959,
circular to 0.1 Link):

| S | `v` | aberration | period over rest (gamma) | extents along / across, ratio (`1 / gamma`) | the centre's drift | the end |
| --- | --- | --- | --- | --- | --- | --- |
| 512 | 1/8 | no | 1.305 (1.024) | 27.6 / 30.0, 0.92 (0.977) | -3.6, -2.1 | decays to r = 12 by 12 141 |
| 512 | 1/8 | yes | 1.426 (1.024) | 30.4 / 31.7, 0.96 (0.977) | -6.4, -7.1 | escapes at 30 223 |
| 512 | 1/4 | no, yes | no turn | 104 / 164; 131 / 104 | | escapes |
| 8192 | 1/8 | no | 1.330 (1.024) | 26.2 / 30.1, 0.87 (0.977) | -2.2, -3.1 | decays to r = 14.5 by 40 963 |
| 8192 | 1/8 | yes | 1.433 (1.024) | 28.7 / 31.6, 0.91 (0.977) | -4.7, -7.9 | decays to r = 2.3 by 48 767 |
| 8192 | 1/4 | no, yes | no turn | 50 / 57; 56 / 68 | | falls in; escapes |

**By what else.** In the Newtonian regime at `0.21 c` the thrown orbit
does contract along the motion, by 0.87 to 0.96 against Lorentz's 0.977,
and its period does lengthen, by 1.31 to 1.43 against Lorentz's 1.024;
and it does not stay periodic: the relative centre drifts against the
motion and the radius decays or grows (the drag and the field's
asymmetry, a self-force on the pair in both forms), and at `0.43 c` no
orbit forms. The numbers have a reason in the law's dispersion: from `v
= p / (m + p / c)` the momentum's response along the motion is `dv / dp
= 1 / (m (1 + p / (m c))^2)`, a longitudinal mass `m (1 + v / (c -
v))^2`, and across it `m (1 + v / (c - v))`, against Lorentz's `gamma^3
m` and `gamma m`: at `v = 1 / 8` the law's masses are 1.62 and 1.27 times
m where Lorentz's are 1.07 and 1.02, so the orbit slows by more than
`gamma` and flattens along the motion by more than `1 / gamma`; the
decay and the drift are the retarded flux's (12.1). **Different law**:
the orbit thrown is neither the rest orbit nor its Lorentz transform;
the contraction and the slowing exist and are the dispersion's, larger
than Lorentz's and not isotropic, and the bond is not stable in motion.

**The pins for the run** (the physicist's, after form B, the crossing
rule and the aberration land): `s32_r24`'s base with the source made free
and both bodies given the throw along +x (the source `p_s = v Q S M_s /
(1 - v / c)` with `M_s = 2^10`: `1.86 x 10^5` label units at `v = 1 / 8`,
`3.68 x 10^5` at `1 / 4`; the probe `p_t = 460` and `898` plus the
tangential 576), 4000 intervals, the `step` records read as the orbit
README reads them (the angle about the source, the return, the mean
radius, the drift):

1. At rest under form B: the period `795 +- 15 %` (the cap's price on
   today's 623; the continuum's 743), the mean radius `24 +- 1`.
2. At `v = 1 / 8`, no aberration: one turn in `857 +- 15 %` intervals,
   the extents `31 +- 3` along the motion and `26 +- 3` across (elongated
   along it, ratio 1.2), the relative centre `7 +- 2` Links behind the
   source, then the probe unbound within 2200 intervals (through a
   face). With the aberration: no full turn, the probe reaching the
   source's Node within 1100 intervals (a contact).
3. At `v = 1 / 4`: no turn, the probe unbound within 2400 intervals in
   both forms.
4. What refutes 12b.2: a bound orbit at `1 / 4`; a contraction along the
   motion at `1 / 8` (the extents' ratio below 1) without the
   aberration; a period within `gamma` of the rest period.

### 12b.3 The seventh verb after (1) and (2)

Nothing of 12b needed it: the crossing rule's factor is a comparison of
world lines (D), the aberration a translation and a comparison (T, D),
the orbit's equations the push (B) and the drive (T) as declared; the
contraction and the slowing found are consequences of the six and are
not Lorentz's. The seventh verb is still needed for exactly what section
12.5 said: for `gamma` to slow a body's own counter or to contract its
bond by `1 / gamma` isotropically (lorentz-v1); the six give a
contraction and a slowing of their own, anisotropic, larger, and
unstable, and the crossing rule supplies the magnetic term's number
without the field it would need. **Verdict**: (1) reached for the
reader's velocity term as the magnetic term's count, the field short of
Maxwell's by `1 / gamma` and the direction along `n_ret`; (2) different
law for the orbit thrown: contraction 0.87 to 0.96 and slowing 1.31 to
1.43 at `0.21 c` in the Newtonian regime against 0.977 and 1.024, the
bond unstable, the registered geometry unbound at both speeds; the
seventh verb needed for Lorentz's `gamma` and for nothing of the six.

## 12c. The mover's counter under the crossing count and the owed count: route C

**The question** (record 230's three routes to Lorentz: A the six verbs
alone, B the seventh verb, C the reading budget; the Boss's order of
03:46Z). Route C: a body's counter is slowed by what it reads (the owed
count, `by_drive(acc_owed, k n, d)` after every self-creation, k the count
of the rows at its Node over every number but its own, `engine.py:496-509`;
section 13.2 (b) read it as the reading's cost over the budget K), and a
moving body reads by the crossing rule (record 158; sections 2 and 12b.1),
so its count differs from a rest body's. Does the difference slow the
mover's counter, by how much against gamma (the Lorentz factor), and at
what cost? The host script
[mover_counter.py](designs/derivations_beam/mover_counter.py) with its
output [mover_counter.out](designs/derivations_beam/mover_counter.out)
makes every number below on the derivation's own formulas and on the
registered fan and readings of series E; no run.

### 12c.1 The mover's count through an isotropic crowd at rest

**Four counts, one of them the rule's.** Let a crowd of rows at rest fill
the GameBoard isotropically: at every Node the rows of every direction
**n** arrive at the same rate (sources at rest everywhere, their fans
symmetric). A reader at the velocity **v** (its speed over a row's pace
`beta = v / c`) counts, per direction, one of four things:

| the count | per direction **n**, over the rest count | its mean over the sphere | what it is |
| --- | --- | --- | --- |
| the Euclidean sweep | `abs(n - beta)` (the relative speed) | `1 + beta^2 / 3` | a sphere reader sweeping point rows; the naive count |
| the Manhattan sweep | `sum_i abs(n_i - beta_i) / sum_i abs(n_i)` | `1 + beta^2 / 3` exactly, whatever the direction of **v** | a cube reader (a Node, six Ports) sweeping point rows |
| the Euclidean crossing | `1 - n . beta` (the fronts crossed) | 1 exactly | the receiver's Doppler per direction, section 2.2's limit |
| **the crossing rule** | `1 - sgn(n_e) beta / abs(n)_1` per step on the axis e | 1 exactly | record 158's count, section 2.4's Manhattan flux; `c_1 = c abs(n)_1` the direction's Manhattan pace |

The two sweeps have the same mean because the mean of `abs(n_x - beta)`
over the sphere is `(1 + beta^2) / 2` and the mean of `abs(n_x)` is `1 /
2` (the script, table (A): 1.0154, 1.0615, 1.2462 and 4/3 at `beta` =
0.2148, 0.4297, 0.8594 and 1, on x, on a face diagonal and on the cube
diagonal alike). The two crossing counts have the mean 1 by the
reflection `n_e -> -n_e`: the count is odd in the row's component along
the step, and an isotropic crowd has as many rows against the step as
with it. Named explicitly, the comparison is between two sphere means:
the mean of the crossing rule's per-direction factor `1 - n . beta`,
which is exactly 1, and the mean of the relative speed `abs(n - beta)`,
the distance from the point **beta** to the unit sphere, which is `1 +
beta^2 / 3` and is the sweep of point rows that the rule does not make. The sweep exceeds the rule exactly on the rows with `abs(n_e) <
beta`, the near-transverse ones, which the rule does not meet at a step
(record 158's C2: a resident row at the destination is met only if it
moves against the step, `u . e < 0`; a row moving across the step is
met at the rest rate, section 2.3's "transverse exactly 1", the
registered form of the difference); their share is `beta^2 / 3` of the
rest count. **Reached**: the crossing rule's count of a mover through an
isotropic crowd at rest is the rest count, at every speed to the cap, on
the sphere and on the lattice.

**On the registered fan** (series E's 290 directions with the integer
`T_d`, a body stepping on +x at `1 / 8` and `1 / 4` Link per
self-creation and at the cap `c = 32 / 55`, the script's table (B)): the
rule's mean over the fan is 1.000000 at the three speeds; the factor
runs from `1 - v T_d / (Q S_1)` on the co-moving heading (0.7852,
0.5703, 0 at the cap) to `1 + v T_d / (Q S_1)` head-on (1.2148, 1.4297,
2); the cube sweep's fan mean is 1.0253, 1.0820, 1.3674. The factor is
never negative under form B: a body's pace on any direction is at most
that direction's row pace, `c` on a heading, and the fan's Manhattan
paces `c_1 = S_1 Q / T_d` run from `c` (the headings) to 1 (the cube
diagonals), so `v <= c <= c_1` on every direction and no direction is
outrun. (Today's per-axis drive at one Link per interval, 1.72 c, can
outrun a heading; there the factor is `abs(1 - v / c_1)` and the mean
rises above 1: outside form B, not stated further.)

**What the mover does read.** Not a changed total but a dipole: over
the hemisphere of rows coming toward it, the rule's factor averages `1 +
0.674 beta` for a step on x (1.145, 1.290, 1.579 at the three speeds),
and the same below 1 behind. A mover reads the crowd's frame in the
direction of its rows and not in their number: the ether wind is in
the reading's first moment (the flow, the push of 12b.1) and absent
from its zeroth (the presence, the count the counter owes).

### 12c.2 The owed count and the counter: no slowing

**What is charged.** The owed count is charged once per self-creation,
`by_drive(acc_owed, k n, d)` with k the count of THAT interval
(`_suspend` after `_frame_all`); the body steps only in an interval in
which nothing is owed (`_move`), so a step's interval is a self-creating
interval and its crossing count is charged; the rows arriving during
the owed intervals are read and not charged. Over one Link at `v_free`
Links per self-creation (`1 / v_free` self-creations per Link), the
charged count is `(1 / v_free) x rest x (1 -+ v_free / c_1)` per
direction: the crossing rule's factor with the FREE pace, whatever the
owed intervals between the self-creations. A body in a crowd steps at
`v_free / (1 + k n / d)` Links per interval: route C slows a body's
motion by the same factor as its counter, isotropically, its momentum
untouched (a viscous crowd; section 9.2's wait).

**Through an isotropic crowd at rest.** The charged count's mean is the
rest count (12c.1), so the counter's rate is `1 / (1 + k n / d)` at
every speed to the cap: the mover's owed count does not grow and its
counter does not slow. Against Lorentz at small `beta`:

| the counter's rate over the rest rate | the coefficient of `beta^2` | near the cap |
| --- | --- | --- |
| the crossing rule (the law) | 0 | 1 in the mean, 0 to 2 by direction |
| the sweep (not the rule) | `-(k n / d) / (3 (1 + k n / d))`, at most 1/3 | `(1 + k n / d) / (1 + 4 k n / d / 3)`, at least 3/4 |
| nature, `1 / gamma` | `-1 / 2` | 0 |

**Different law**, in three structural ways before any number. (i) Any
slowing of route C is proportional to the crowd, `k n / d`: in an empty
world none (J4's bar, 12c.4), in series E's shells `k = 41.5 / r^2` at
rest; Lorentz's is the same in an empty world and in a crowd. (ii) It is
bounded: the largest count in any direction is `2 x rest` (head-on at
the cap), so the mover's rate over the rest rate is never below `(1 + k n
/ d) / (1 + 2 k n / d) > 1 / 2` whatever the crowd; gamma is unbounded
at the cap (29.3 for the CERN muon). (iii) Its sign follows the crowd's
frame: a body moving WITH the rows it reads counts fewer, owes less and
runs FASTER than a body at rest in the same crowd (record 158's
consequence for G2: "in `_scalar` and `_age` the clock's count now falls
by `v / c`"); only against the rows does it run slower, by `(1 + beta)`
at most. So route C gives no isotropic slowing, an anisotropic one in
the crowd's frame with the wrong sign for a body moving with its light,
and nothing a body carries into an empty world.

### 12c.3 The bond under route C: no contraction, a stretch or a speeding

The registered orbit worlds (series D, `s32_r24` and its five siblings)
have `suspension` 0: route C does nothing to 12b.2's orbit as
registered. In a world with a suspension, the pair's two counters read
each other's rows by section 12's exchange rates as counts (the script's
table (C)): without the aberration the leading body counts `(1 - beta)^2`
of the rest count of its partner's rows (0.617 at `beta` 0.2148, 0.325 at
0.4297) and the trailing body `(1 + beta)^2` (1.476, 2.044); with the
aberration both count `(1 - beta^2)^2` (0.910, 0.665); a transverse
partner `(1 - beta^2)` (0.954, 0.815). At the partner's rest count `k_p`
with `n / d = 1`:

| `beta` | `k_p` | rest rate | leading | trailing | both, aberrated | Lorentz `1 / gamma` |
| --- | --- | --- | --- | --- | --- | --- |
| 0.2148 | 1 | 0.500 | 0.619 (1.237 x rest) | 0.404 (0.808) | 0.524 (1.047) | 0.977 |
| 0.2148 | 0.1 | 0.909 | 0.942 (1.036) | 0.871 (0.959) | 0.917 (1.008) | 0.977 |
| 0.4297 | 1 | 0.500 | 0.755 (1.509) | 0.329 (0.657) | 0.601 (1.201) | 0.903 |
| 0.4297 | 0.1 | 0.909 | 0.969 (1.065) | 0.830 (0.913) | 0.938 (1.031) | 0.903 |

**Different law** in the direction. Without the aberration the two
counters of one pair split at first order in `beta` (the leading faster,
the trailing slower, `4 beta k_p / (1 + k_p)` of the rest rate apart): since a body steps
only when nothing is owed, the leading body also steps faster and the
trailing slower, so the pair STRETCHES along its motion at the rate of
that split (a self-force again, 12.2's `4 beta` in the counters instead
of the pushes) and no contraction is available. With the aberration
both counters run faster than at rest, `(1 - beta^2)^2` of the partner's
rows reaching them: fewer rows, less owed, a SPEEDING by about `2
beta^2 k_p / (1 + k_p)`, the sign opposite to Lorentz's slowing. The
isotropic crowd at rest around the pair adds a common factor to both
counters and both paces (12c.2) and changes neither the shape nor the
period's ratio to the rest. So route C neither contracts nor slows a
bond: it stretches an unaberrated pair and speeds an aberrated one, in
proportion to the partner's rows and to nothing in an empty world.

### 12c.4 The muon of J4 re-read under route C

HYPOTHESES 21's J4: muons of content 207 with `become` at 64, a key on
the body's own self-creation count (`ages_at_key`, the clock's trigger,
`nature_beam.py:1455-1460`), in an open bar with no crowd (`release` `[1,
2^20]`), one at rest and one thrown at `1 / 4` and `1 / 2` Link per
interval (0.43 c and 0.86 c). With no crowd `k = 0` at every Node: route
C charges nothing, the moving muon's 64th self-creation is at tick 64 as
at rest, its range `64 v` Links (16 and 32); the entry's prediction
stands unchanged. In a crowd at rest at `k n / d = 1` (the script's
table (D)): the rest muon fires at tick 128; the moving one at 128 in
the isotropic mean, at 100 (0.43 c) or 73 (0.86 c) moving with the
crowd's rows, at 156 or 183 against them. Nature: 2.197 microseconds at
rest, 64.4 in the CERN ring (gamma 29.3); lorentz-v1's comparison
(FORM.md section 4): ticks 71 and 126 at the two speeds (`64 gamma` =
70.9, 125.2). Route C's lifetime in flight lengthens at most by `(1 +
beta) < 2` over the rest lifetime in the same crowd, and only against
the crowd's rows; with them it shortens. **Different law** on the
number, the bound and the sign. A key on the Links moved in place of the
age (a range rule: the decay at a distance `L` whatever the pace) would
give a lifetime of `L / v` intervals, no decay at rest and no `gamma`
either: a range is not a clock, and nature's range `gamma beta c tau` is
a clock's range.

### 12c.5 What the mechanism needs, and the three tests

**What it needs.** (a) A crowd at rest everywhere at one presence, so
that every body has the same rest slowing `1 / (1 + k_0 n / d)`: a
declaration of a world, not a rule (the register's open worlds have the
crowd falling as `1 / r^2` from each source; a static periodic world
fills without bound and every counter slows toward zero, section 15.5's
Seeliger item and 14.3's third stream; under the growing wall the
presence settles, 0.000765 of `q dwell` per source at L = 301, and a
counter has a steady rest slowing). (b) A count that is not the crossing
rule: only the sweep of the near-transverse residents gives a `beta^2`
term at all, `beta^2 / 3`, and the sweep is refuted by the registered
transverse count of 1 (record 158's tests, section 2.3). (c) Even with
both, a slowing proportional to `k_0 n / d`, bounded above by 4/3 in the
factor, and read in the crowd's frame (the dipole of 12c.1: a preferred
frame, the crowd's, in the reading's first moment). Nothing of (a) to
(c) gives `1 / gamma`.

**The three tests.** Route C proposes no rule: the crossing rule (D on
the body's two last Links, record 158) and the owed count (one
`by_drive` on the body's record) are the law already, generic (no name),
vector (a comparison and a translation) and local (the body's own
record, the six Ports, nothing at a Node). What fails is the number, not
a test. The variant with a crowd everywhere passes the tests as a world
declaration; the sweep variant would change record 158's C2 and is
refuted by the register.

### 12c.6 The pins for a run under form B and the crossing rule

Series E's `scalar` world (`examples/events/redshift/scalar.json`:
the source of content 4096 at the centre on the 290-direction fan, one
row per direction per interval, `suspension` `[1, 1]`) with one probe
added, a free measured event of content 1 with the `pass` entry (no
push), on the +x axis, thrown along x under form B: `p = 10` label units
(`v_free` = 0.1232 Link per self-creation, the crossing factor `v T_d /
(Q S_1)` = 0.2117) and `p = 28` (0.2497, 0.4292), outward from r = 4 and
inward from r = 14, read over the 10 Links r = 4 .. 14 by the `step`
records and the owed counts. The rest reading of the axis probe is the
register's: 2.03 at r = 6 .. 12 and 1.00 at r = 4 and 14 (the heading's
dwell pattern), the mean over a path of Links `55 / 32` = 1.72; under the
rule a body at rest reads as built (record 158). The pins (the script's
table (E); the counts at the registered 2.03 first, at the path mean
second):

| throw | count over the rest count | the count | self-creations per 1000 intervals (rest 330; 368) | intervals for the 10 Links (rest 246; 221 at `p` 10, 121; 109 at `p` 28) |
| --- | --- | --- | --- | --- |
| `p` 10 outward | 0.788 | 1.60; 1.36 | 385; 425 | 211; 191 |
| `p` 10 inward | 1.212 | 2.46; 2.08 | 289; 324 | 281; 250 |
| `p` 28 outward | 0.571 | 1.16; 0.98 | 463; 505 | 86; 79 |
| `p` 28 inward | 1.429 | 2.90; 2.46 | 256; 289 | 156; 138 |

Tolerance: the boundary row per Link (section 2.2, at most one row
per Link) and the dwell pattern's sampling by the self-creating
intervals, about 5 % on the counts. The isotropic pin needs no new
world: the outward and inward counts average to the rest count within
the tolerance (an isotropic term `beta^2 / 3` would put the mean at
1.015 and 1.061 of the rest count); the transverse pin is registered
already (record 158's transverse 1; the doppler bar's tests). **What
refutes 12c**: a mean of the outward and inward counts above the rest
count by more than the tolerance at either momentum; a transverse count
other than 1; a counter of a moving probe in an empty world other than
the rest counter's.

### 12c.7 The verdict of section 12c

**Route C gives no slowing**: the crossing rule's count of a mover
through an isotropic crowd at rest is the rest count exactly, on the
sphere and on the registered fan, at every speed to the cap, so the
owed count's mean and the counter's rate are the rest ones. **The
number against Lorentz's**: the coefficient of `beta^2` is 0 where
Lorentz's is 1/2; the naive 1/3 is the sweep of point rows, not the
rule, and is refuted by the registered transverse count. **Its form**:
proportional to the crowd, bounded by 2 in the most anisotropic case,
in the crowd's frame, faster for a body moving with its rows; it
stretches or speeds a bond and never contracts one; the muon of J4
fires at 64 in its empty bar at every speed. **Its cost**: nothing new,
the crossing rule's comparisons and the owed count's one `by_drive` are
in the law and in section 13's count (26 per row read plus 5); a crowd
everywhere is a world's declaration. **The seventh verb** stands where
12b.3 left it: routes A and C give a slowing of their own (the bond's,
12b; none, 12c), neither Lorentz's; gamma enters the law's periods
through the flight table's root at load and a body's own counter
through nothing of the six.

## 13. The one constant K: the fixed computation per Node per interval, what it explains, what it bounds, what it leaves free

**The question** (the owner's, 2026-09-21, translated: "can one define
the total computation as a given that must be constant? then it could
explain many derived parameters"; the Boss's answer and order, record
209). In this section K is the computation budget of one Node per
interval, the number of integer operations a Node may do whatever is at
it; the world's content quantum, written K elsewhere in this document,
is written `K_clock` here. A constant TOTAL computation over a growing
GameBoard is the stepping form's reading of K (section 11.4: the
stepping visits every Node, the event form visits the events) and is
deferred to section 15 with the owner's addendum on the growing lattice.

### 13.1 What the law already fixes

Highlights 3.12 (local bounded processing): "each Node performs one
bounded local update per tick using fixed-capacity channels, bounded
payloads and identifiers, and six adjacent connections; per-Node work
and storage must not grow with world size or elapsed history". LOCALITY-1
(SIMULATOR_DEFINITIONS.md): "for fixed K and fixed-width integers, its
work and stored state must be O(1) with respect to world size, source
count, elapsed ticks and traveled distance". So the given is per Node: K
integer operations per interval and a fixed store, the same K at every
Node; a global constant is not admissible (no global quantity; the
world's total is the sum over the active Nodes, section 11.4). Two
precisions the code forces. (i) As built the work at a Node is
proportional to the rows at it (the walk, the reading and the click are
per row, `nature_beam.py:2441-2565`, `358-397`, `amplitude.py:562-565`),
and the rows at a Node are bounded only through the merge: rows of one
number, content, direction, age, phase and record fuse (`4149`), so a
free family has at most `P x L_D x N` distinct rows per Node per number
(the fan, the flight's period, the circle), a bound that is a function of
the widths; rows of different records never fuse, so under the amplitude
key the rows per Node grow with the open records (ENGINE.md: "the host's
work and memory per interval follow the open records"). K is therefore
a requirement the widths realise for the free families and a host cost
for the records, as 3.12 says of itself ("accepted requirements; their
encounter implementation still needs verification"). (ii) Two of the
interval's stages are host operations over every row, not per Node: the
store's sort before the merge (`NatureBeamStore.sort`, `1117`) and the
layer's ladder at a record's completion (`amplitude.py:681-776`); in the
event form of section 11 both are per Node and per record.

**The operations that count, per interval, from the code** (integer
operations; a lookup, an add, a multiply, a compare or a floor division
each one):

| Operation | Per | Count | Where |
| --- | --- | --- | --- |
| the walk: the flight table's step (a mod and a lookup), the three coordinates, the wrap or the face, the flat index, the phase per Link, the phase per age (`by_clock_rows`), the age | row | about 16 | `nature_beam.py:2441-2565` |
| the reading: the moment table's 13 columns (2 counts, 3 flow, 6 tensor, 2 age) and their sums per Node | arriving row | 26 | `358-397`, `439-486` |
| the collision: the class key, the 8-slot code, the table's lookup, the permutation | Node with two singles of one class | about 20 | `2345-2390` |
| the push: per column and axis one product and one `by_drive` (an add, a division, a compare, a subtraction) | body, per group of arrivals | 5 x 3 x columns (30 with gravity and charge) | `2180-2277` |
| the turn, the owed count, the release per family, the lamp: one `by_drive` each | body | 5 each | `engine.py:442-509`, `nature_beam.py:3599-3606` |
| the drive: one `by_drive` per axis (three today; one under form B) | body | 15 (5) | `engine.py:585-600` |
| a release: one row born per direction of the fan, the apportioning's share | releasing body | 12 P (P rows of 12 fields) | `3618-3644`, `3804` |
| the click: the pointer (2 products, 2 adds), the residual per channel (a `cmul`, 6) | ending row | 10 | `amplitude.py:562-599` |
| the merge: the identity key per row; the sort over the store (host, `R log R`) | row | about 10, plus the host's sort | `1117-1237` |

### 13.2 The four consequences, proved or bounded

**(a) c = 1 / sqrt 3, the flight's cap.** What K gives: one interval's
work on a row is one carry of its Manhattan accumulator at most (`2 S_1
Q <= 2 T_D`, the rate below the wall: at most one Link per interval, the
walk's causal bound, LOCALITY-1's "six causally available neighbour
records"), and the digital line of a direction **D** makes exactly `S_1 =
|D|_1` Links per period, the least number of Links any lattice path from
the Node to the Node at **D** can make (the L1 distance): the least
computation per Euclidean progress, one carry per Link. What K does not
give: the value `1 / sqrt 3`. One Link per interval on every direction
would let a heading row fly at 1 Link per interval and a cube-diagonal
row at `sqrt 3` per interval; the same Euclidean pace in every direction
(the flight table's isotropy, `T_D = isqrt(3 |D|^2 Q^2)`) is a second
axiom, and it fixes the pace at the diagonal's, `1 / sqrt 3`, the largest
isotropic pace that crosses at most one Link per interval on every line
(`S_1 Q <= T_D`, Cauchy-Schwarz with equality on the diagonals: c is the
operator norm of the flight, record 186). The flight table's sitting AT
that supremum, `1 / sqrt 3` and not below it, is a third statement of
the design beside locality and straightness, since a slower isotropic
pace obeys both (the paper's finding, round 7; the second axiom above
in the paper's words). **Partial**: K fixes the bound
(one carry per interval, the Manhattan count as the least computation),
isotropy fixes the number; the count against K is the walk's 16
operations per row per interval, and 1 carry per `T_D / (S_1 Q)`
intervals (1.72 on a heading, 1.22 on a face diagonal, 1 on a cube
diagonal).

**(b) The clock's slowing by the crowd as a computation budget.** A body
that self-creates reads the rows at its Node (the presence k, or the age
moment) and owes `by_drive(acc_owed, k n, d)` intervals before its next
self-creation (`engine.py:496-509`; section 9.2): the wait is
proportional to the crowd. The reading costs 26 operations per row
(13.1), so reading k rows costs `26 k` operations; if a Node's budget is
K per interval, the reading of k rows takes `26 k / K` intervals, and the
owed count is exactly that cost if and only if the world's suspension
pair is the reading's cost over the budget,

    [n, d] = [26, K]      (or [c_read, K] with c_read the reading's operations per row).

Then the gravitational slowing of a clock, `1 / (1 + k n / d)` (section
5.2, series E's `k_s r^2 = 41.5`), is the fraction of the body's
intervals its reading consumes: a body in a denser crowd self-creates
less often because its Node's budget is spent on reading. **Partial**,
and the register decides how far it holds: the suspension pair is a
declared key, `[1, 1]` in series E's `scalar` world and `[1, 2]` in its
`age` world (section 5.1), so under the budget reading those two worlds
have `K = 26` and `K = 52` operations per interval, two budgets and not
one; and the `age` world reads 13 columns where the `scalar` world needs
11 (no age moment), a ratio `11 / 13` and not `1 / 2`. So the owed count
is a computation budget in form (the wait proportional to the rows read,
one `by_drive` on the body's record) and the register's two suspensions
are not one K: what would make them one is a rule "the suspension of
every world is `[c_read, K]`", a declaration of K, which the law does not
have. The count against K: 26 per row read plus 5 for the owed count's
carry.

**(c) The click's one bit per record.** The click reads one comparison
per record, the cell of u on the ladder (`cell_of`, `amplitude.py:208`),
and deletes the record: at most `log2 (cells)` bits leave the rows
(section 6.1, the Holevo identity). Is the one read-out a consequence of
K? The ladder over `cells` cells costs `cells` comparisons and the lcm of
the multiplicities, once per record at its completion, on the host (the
layer, principle 5: the apparatus's one non-local operation): K bounds
its length, `cells <= K`, only if the ladder is counted as the Node's
work in the interval of the completion, and then the bits per record are
bounded by `log2 K`. The ONE read-out per record (one cell, not several)
is Definition 3 of the click, a design, not a consequence of K: a click
reading two cells would cost two comparisons and fit any K above 2.
**Bounded, not explained**: K bounds the bits per record by `log2 K`;
the one bit is the click's definition. The count: `cells` comparisons
per record, 10 operations per ending row.

**(d) The reading's rank-2 limit.** The moment table has 13 columns per
row (13.1): the counts, the flow (rank 1), the traceless tensor (rank 2,
six entries), the age. A rank-r moment adds the symmetric monomials of
degree r, `(r + 1)(r + 2) / 2` columns (10 at rank 3, 15 at rank 4), so
the reading's cost per row is `2 + sum over the ranks kept of (r + 1)(r
+ 2) / 2`, and for a Node reading k rows K bounds the rank: the largest r
with `k x cost(r) <= K`. That is a bound, and at the register's K it is
loose (13 columns against a budget of hundreds). What fixes rank 2 is
the vector test (record 202): every rate is at most bilinear in the
state, the push reads the flow (rank 1) times the reader's content and
nothing reads the tensor as a rate (it is reported, `reads: tensor`,
record 205: "the one rank-2 form and the contract's limit"), so a rank-3
moment would be computed and read by no rule; the contract's tensor
limit (ARCHITECTURE.md) is that statement as a bound of the code.
**Bounded by K, fixed by bilinearity**: the count is 26 per row at rank
2, 46 at rank 3, 76 at rank 4.

### 13.3 The grain from K: the budget equation and the register's widths

**The hypothesis.** If K is the one given, the widths N (the phase
circle), P (the fan), Q (the pace's grain), W (the birth wheel) and
`K_clock` (the clock's pair) are bounded or fixed by the cost of the
operations that use them. **The costs, from 13.1:**

- **P** enters the work directly: a release births P rows at one Node in
  one interval (`12 P` operations, the apportioning's P shares), and a
  re-emission at an opening births P per arriving row: `P <= K / 12` at
  every source Node. P also enters the store through the flight table,
  `P x (3 L_D + 3 S_1 + 3)` integers (the steps per period, the line,
  the label).
- **N** enters the store, not the work: the tables C and S are `2 N`
  integers and the half-angle tables `4 N` (`core/phase.py`,
  `amplitude.py:125-140`); the phase's operations per row (an add and a
  mod) cost the same at every N. N is bounded by the word width (a
  phase within 2^62; the tables' bound 65536, `MAX_PHASE_STEPS`) and by
  the store per Node if every Node holds the tables.
- **W** enters as one accumulator per record (`u = ordinal mod W`, or the
  golden rate on `Z_W`): one integer of `log2 W` bits and one operation
  per birth, whatever W.
- **Q** and **`K_clock`** enter the word width only: the flight's
  accumulator holds up to `2 T_D = 2 isqrt(3 |D|^2 Q^2)`, so `Q |D| <=
  2^61 / sqrt 3` (the fan's radius and the pace's grain bound each other
  through the word), the turn's product `content x n` must stay within
  `2^62` and below `K_clock x N / 2` (the frame's refusal at half the
  circle, `engine.py:475-489`), the push's `Lambda_c^2` within `2^62`.

**The budget equation the law implies**, per Node per interval, with r
the rows at the Node, a the arriving rows, b the bodies, e the ending
rows and one release of P rows:

    K >= 16 r + 26 a + 20 [collision] + b (30 + 15 + 20) + 12 P [release] + 10 e,
    store >= 12 r + 6 N + P (3 L_D + 3 S_1 + 3) + 6561 (the collision table) + the bodies' tables,
    word: Q |D|_max <= 2^61 / sqrt 3,  content x n < K_clock N / 2 <= 2^62,  Lambda_c^2 <= 2^62.

**The register's choices against it.** N = 64 (the amplitude worlds; a
store of 384 integers), P = 290 (the nucleus fan; 3480 operations at a
release) and 1423 (the two-slit fan by angle; 17 076), Q = 64 with `|D|`
up to 48 (`Q |D| = 3072` against `2^61 / sqrt 3`: fifty bits to spare), W
= 4096 (twelve bits), `K_clock = 2^20` with contents up to `2^30`
(thirty-two bits to spare). The largest per-interval cost on the register
is a source Node's release, `12 P`, of order `10^3` to `10^4`, and the
largest per-interval reading is the nucleons' (57 rows, 1482 operations)
and a two-slit opening's (91 re-emissions per arriving row); the
tables' costs are hundreds, the wheel's one operation, the word's bounds
untouched by fifty bits. **The widths sit at several budgets, not one:**
P at thousands of operations, N and W at hundreds of integers of store
and one operation, Q and `K_clock` at the word width with most of it
unused. Nothing in the register puts two widths at the same K, and no
width is at a bound.

**Are the widths free of K?** Yes, as the law stands: each width is a
resolution chosen below its bound (record 189, kind (1)), K bounds P
from above (`P <= K / 12`), bounds N and W through the store and the
word, and fixes none of them. PREDICTIONS 26 stands as written: the
widths are the sizes of finite samplings of compact groups, and what
they quantise is what lives on those groups. **What would fix them:** one
added principle, "every Node's budget is exhausted", that is, the widths
as large as K and the store allow (`P = K / 12` at a source, `N` and `W`
filling the store's remainder, `Q |D|` and `K_clock N` at the word
width): then the one number K, with the word width, would fix P and
bound the rest, and the law's grain would be the largest the budget
admits. That principle is not in the law, and the register does not sit
at it (fifty bits unused); it is stated here so that it can be chosen.

### 13.4 What K cannot explain

The family table: the contents M (a mass, on the non-compact scale,
free: PREDICTIONS 26), the cost h, the charge per unit of content rho,
the strong column, the lifetime L, the phase rate `n / d` and the hand
(record 189, kind (2)); the world's width S (the push per unit of content
per unit of flow, what physics calls Newton's constant); and the initial
state, the GameBoard's extents and the bodies' positions, momenta and
contents (kind (3)). K is a bound on the operations; these are the
operands. Nor does K alone give c: it gives the causal bound, and
isotropy gives the number (13.2 (a)).

### 13.5 The three tests on the statement "K is the one constant"

- **Generic**: passes. K is a bound with no family name, the same at
  every Node for every family; its special cases (a row, a body, a lamp)
  are counts of the same operations, not branches.
- **Vector**: passes vacuously. K is not one of the six verbs and changes
  no component of the state; it is a bound on how many verbs an interval
  may apply at a Node, a constraint on the law's form, not a rule of the
  state. Where it would enter the state (13.2 (b), the suspension as
  `[c_read, K]`) it enters through an existing verb, the owed count's
  `by_drive`.
- **Local**: passes in the per-Node form and fails in the global one. A
  budget per Node reads nothing beyond the Node; a constant total over
  the board is a global quantity (LOCALITY-1's "no global field solve"),
  admissible only as the sum the stepping form computes and not as a
  rule any Node can read.

### 13.6 The verdict of section 13

**Reached** (K explains): the causal bound of one Link per interval and
the Manhattan count as the least computation per Euclidean progress
(13.2 (a), the bound half of c); the wait as the reading's cost in form,
one `by_drive` on the body's record proportional to the rows read (13.2
(b)). **Partial** (K bounds): the value `c = 1 / sqrt 3` needs isotropy;
the bits per record are bounded by `log2 K` and fixed at one by the
click's definition; the reading's rank is bounded by K and fixed at 2 by
bilinearity; P is bounded by `K / 12` at a source, N and W by the store,
Q and `K_clock` by the word; the register's widths sit at several
budgets, none at a bound, so the widths are free of K and PREDICTIONS 26
stands. **Free** (K leaves): the family table, the width S, the initial
state, and the number `1 / sqrt 3` itself. The statement passes the
three tests in its per-Node form and fails the local test as a global
total.

## 14. Entropy on the GameBoard: the count of state vectors consistent with the click list, where it grows, and where the system goes

**The definition** (the owner's question of 2026-09-21, "how is entropy
defined in our system, vectorially, and where does such a system go";
records 214 and 215; the Boss's order). The state is one integer vector
**s** on the product torus (section 11.2), and what leaves the board is
the click list (the world is the list of clicks, BEAM_LAW; the click the
one read-out, section 0). The entropy of the world at a time is

    S = log2 of the number of state vectors s on the product torus consistent with the click list up to that time,

a count of points on the torus, no continuum measure. The host script
[entropy_clicks.py](designs/derivations_beam/entropy_clicks.py) with its
output [entropy_clicks.out](designs/derivations_beam/entropy_clicks.out)
evaluates it on the register's click counts; no run.

### 14.1 No production between events

Between two events the state advances linearly, `s(t) = s(t_0) + (t -
t_0) r` (section 11.3 (i)), a bijection of the torus onto itself, and
every rule of the linear block is one too: the walk (a translation), the
phase (a translation), the merge to the normal form (the multiset of rows
summed, invertible on the multiset), the split (the integer matrix whose
transpose is its inverse up to the normal form, the design's 2.4), the
rotation (`U_s^T U_s = (C'^2 + S'^2) I`), the gate (a permutation), the
evaluation (a ring homomorphism on the record, linear); the paper's
Theorem 1 says the same of the maps between clicks: injective given the
record. The Euclidean division keeps its remainder (the carry a
bijection `Z = Z / d x Z`, record 173). So the number of state vectors
consistent with the clicks does not change while no click, cancel or
discarded remainder happens: the flow on the torus preserves the count,
the lattice's Liouville theorem, and the linear block produces no
entropy at all.

### 14.2 Production at the click, the cancel and the discarded remainders

**The click.** A record's vector **f** (its amounts per phase per end
Node and label) is deleted at the completion and one cell is read (the
ladder, `amplitude.py:681-776`): the state vectors consistent with the
clicks multiply by the number of records that would have given that
cell. On the register's apparatus a record's vector is a function of its
birth phase u alone (the paths, the splits and the phases are the
world's; u is the one thing that differs from record to record, the
wheel `ordinal mod N`), so the freedom the click erases is u's, `log2 N`
bits per record, of which the click reports `H` bits, the Shannon
entropy of the cell distribution over the wheel, and erases the rest:

    bits read = H = - sum_k (w_k / N) log2 (w_k / N),   bits erased about u = log2 N - H = sum_k (w_k / N) log2 w_k,

`w_k = b_k - b_(k-1)` the cell's width in u (the rungs), so that **bits
read + bits erased = log2 N per record**, an identity of the ladder (the
cells partition the wheel). On the register (N = 64):

| World | the cells (the registered clicks over 64 births) | bits read H | bits erased about u | `log2 (cells)` (6.1's bound) | units at the ends (6.1's cost) |
| --- | --- | --- | --- | --- | --- |
| `mz_equal` (L1) | 64, 0 | 0 | 6 | 1 | 82 |
| `mz_quarter` (L1) | 32, 32 | 1 | 5 | 1 | 82 |
| `mz_345` (L1) | 63, 1 | 0.116 | 5.884 | 1 | 14 |
| the pair at (16, 24) (L3) | 27, 5, 5, 27 | 1.625 | 4.375 | 2 | 4 |
| the pair read at (16, 24) (L3) | 2, 14, 2, 14, 14, 2, 14, 2 | 2.544 | 3.456 | 3 | 4 |
| `slits_low` (L2) | 11, 12, 11; fourteen pixels of 1 and one of 2; 8, 7 | 3.425 | 2.575 | 4.25 | 185 |

The Boss's candidate formula, `log2 (prod (sum a_i)^k) - log2 (cells)`
(the units of 6.1 as bits), is the COST read as information, and on the
register it overcounts: `mz_equal`'s 82 units are one function of u, not
82 free amounts, and its click erases 6 bits, not `log2 (41^2) - 1 =
9.7`; `slits_low`'s 185 units erase 2.6 bits, not `log2 (91^2 x 5) - 4.25
= 11.1`. The units are what the apparatus pays per record (6.1, the cost
column); the entropy is what the click erases of the record's freedom,
and the record's freedom on a fixed apparatus is its wheel. Where the
record's rows carry more freedom (a lamp with several labels, records
that met other records at a gate), the erased bits are `log2` of the
number of joint states the cell admits, bounded by `log2 (N x the
labels' branches)`; the identity `read + erased = log2 (the record's
states)` holds by the same partition.

**The cancel.** Under the amplitude key two rows of one record at a
phase difference of exactly `N / 2` cancel at the merge and their units
leave to the ledger's `cancelled` lines (`nature_beam.py:4149-4170`): the
two amounts are erased (`log2` of their range per cancelled pair), the
ledger keeping their sum only. On `mz_balanced` D2's rows cancel entirely
(the register: "D2's rows cancel on the GameBoard").

**The discarded remainders of section 1.3** (on `main`; the fraction-free
law keeps every count's remainder): the meeting's `isqrt` and its floor
over the common denominator (items 9 and 10), the doppler floors (item
5), the lamp's discarded count at a stall (note 41 (iii)), the turn under
`action` (item 6): each a floor over a divisor d erases at most `log2 d`
bits per interval per count, bounded, the law's small leaks beside the
click's.

**The escape.** A row leaving through an open face clicks there and
leaves the board (its amount, content and label booked on the face's
lines): its position and phase are erased from the state, `log2 (extent
x N)` bits per row at most; a periodic world has no such term.

### 14.3 Where such a system goes

Three monotone streams, each a line of the books:

1. **The click list grows** and never shrinks: the world's entropy in the
   sense above is non-decreasing, by `log2 N - H` per record clicked (6 bits
   for `mz_equal`, whose click is certain and reports nothing of u; 2.6
   for `slits_low`, whose click reports 3.4 of u's 6 bits), by the cancels
   and by the leaks. The arrow of time is the click list (the paper's row
   8) and the ledger's `cancelled` and `escaped` lines.
2. **The paid content flows out.** A lamp pays `h s` per unit born and
   stalls once its content falls below `K_clock` (6.4: the Bell lamps at
   tick 4); the free field is born at content 0 and costs nothing. So the
   finite resource of a world is the paid families' content, which drains
   into `absorbed` and `escaped`; when every lamp has stalled no record
   is born and the click list stops growing.
3. **The free field accumulates or leaves.** In an open world the rows
   leave through the faces and the board empties. In a periodic world the
   rows of a family without a lifetime never leave: the presence k at
   every Node grows linearly with time and every clock owes more, its
   rate `1 / (1 + k n / d)` falling toward 0 (Seeliger's accumulation in
   integers, section 15.6); a family with a lifetime L bounds its crowd
   at the sources' rate times L and the periodic world is steady. The
   end state of a periodic world without lifetimes is not a uniform
   temperature but a board of stalled lamps and clocks that owe, full of
   rows nobody reads; of an open one, an empty board with the ledger
   holding what escaped.

**Verdict.** **New** (a quantity of the law with a counterpart's name):
the entropy as the log of the torus points consistent with the click
list, produced only at the click, the cancel and the leaks, with the
identity `bits read + bits erased = log2 N` per record checked on six
registered worlds; the Boss's units-as-bits formula corrected to the
wheel's bits; **reached** for the second law in the law's own terms (the
click list and the ledger's lines monotone, the linear block a bijection
that produces nothing); where the system goes stated as the three
streams, the periodic world's end the accumulation of section 15.6 unless
a lifetime or a growing wall bounds it.

## 15. The growing wall: the expansion as a wall of the flight that grows, its local form, and what it does to the register

**The question** (the owner's reading of the expansion, record 215,
translated: "what they see is that space itself grows: the computation c
does not grow, what grows is the number of Nodes between places"; and
his addendum, record 218: "the universe grows, neither closed nor open,
but keeps a constant total computation; then c must be tied to the size
of the universe"; the Boss's order (D)). The host script
[growing_wall.py](designs/derivations_beam/growing_wall.py) with its
output [growing_wall.out](designs/derivations_beam/growing_wall.out)
makes every check below on integer accumulators and the registered
stars; no run. The periodic universe (no faces) and the rule's entry
into the law are the owner's decisions, put to him with this section;
the rule is stated under a hypothesis identity of its own, absent by
default.

### 15.1 Two forms of "more Nodes between places"

(a) **Inserting Nodes**, `Z_X -> Z_(a X)`: a change of the translation
group, every index remade, the fan and the lines re-sorted. An
operation on the GameBoard, not on the state: not one of the six verbs,
and not stated further. (b) **The growing wall**: the flight of a row is
the Manhattan accumulator at the rate `2 S_1 Q` against the wall `2 T_D`
(section 1.4); let the wall grow, `2 T_D a`, with `a >= 1` a growth
factor that rises at the declared rate H per interval. Every coordinate
stays (nothing moves that was at rest), the rate stays (c in Links per
interval is untouched), and a Link takes `a` times as many intervals as
before: in the original Nodes per interval the pace is `c_0 / a`. The
owner's "c tied to the size" is this, with the invariant

    c(t) x a(t) = c_0      (the rate of the accumulator, unchanged; c the pace in original Nodes per interval),

a CONSEQUENCE of the wall's form beside c = the operator norm of the
flight (record 186; section 13.2 (a)): the operator's norm in Links per
interval is `1 / sqrt 3` at every a, and in original Nodes per interval
`1 / (sqrt 3 a)`.

### 15.2 The local form: three candidates on one stream, one of them the register's

The Boss's candidate: the wall grown with the row's own age, `2 T_D (1 +
H age)`, a Count row on the row's record reading the age, local by
construction. The script runs a stream of 400 rows released one per
interval on a heading (`T_D = 110`, H = 1 / 400 per interval) through
three walls, each as integers (the growth factor scaled by 400), and
reads `1 + z` as the arrival spacing at 100 and 300 Links:

| the wall grown with | `1 + z` at 100 Links | at 300 Links | the closed form |
| --- | --- | --- | --- |
| the row's age, `2 T_D (1 + H age)` | 1.000 | 1.000 | 1: every row makes the same flight shifted in time, the spacing is kept: **no redshift** |
| the row's birth tick, `2 T_D (1 + H t_birth)`, fixed at birth | 1.429 | 2.291 | `1 + H d / c_0` (1.430, 2.289): a redshift linear in d for ever, no Milne form |
| the tick, `2 T_D (1 + H t)` | 1.539 | 3.639 | `a(t_r) / a(t_e) = e^(H d / c_0)` (1.537, 3.629): `z = tau / (1 / H + t_r - tau)`, the Milne form |

So the age wall, the fully local candidate, gives no redshift: a rule
that reads only the row's own record makes every row's flight the same
function of its age, and a stream keeps its spacing. A redshift needs
the wall to differ between rows released at different times: the
birth-tick wall (read once, at the release) gives `z = H d / c_0`, right
at first order and wrong beyond it (15.5: refuted by the far stars); the
tick wall gives the cosmological `1 + z = a(t_r) / a(t_e)` and, with `a =
1 + H t`, exactly the Milne relation `z = tau / (T - tau)` with `T = 1 / H
+ t_r`, the form the register fits (15.5). **Corrected**: the local form
that works reads the tick, not the age.

**What the tick is.** The interval's index, which every Node has: the
GameBoard steps synchronously (section 11.2: `t*` is an integer, the
interval global by construction), every event record carries `tick`,
the frame and the wheel read it. The tick wall reads nothing beyond the
row's own accumulator and the interval it is in: no field solve, no
search, no map, no neighbour beyond the six. Whether a count shared by
every Node is "a global quantity" in LOCALITY-1's sense is the Boss's and
the owner's call, and the section gives both readings: if the tick is
admitted, the rule is

    the flight's wall  2 T_D x a,   a = H_den + H_num x tick   (integers; the rate 2 S_1 Q x H_den),

one row of the counts (the wall a function of the read state, F's
feedback block), H = `[H_num, H_den]` a declared constant of the world
under the identity `expansion-v1`, absent by default; if the tick is not
admitted, no local wall gives the register's redshift (the age wall
gives none, the birth wall the wrong second order), and the expansion
stays outside the law as a change of the board.

### 15.3 The condition for a redshift, and the two c

The redshift is a difference of rates: the flight slows in Nodes per
interval while the bodies' turns (the rate `content x n` over d, a row
of the body's own table, `measured.py:205-316`) keep their rate per
interval, so a lamp releasing one row per interval sends a stream whose
spacing at arrival is `a(t_r) / a(t_e)`. If every accumulator slowed
together (the flight's wall and the turn's wall both scaled by a), the
lamp would release once per `a` intervals and the spacing at arrival
would be 1 again: a common scaling of every wall is a relabelling of the
interval, unobservable. The law already keeps the two apart: the flight
is the board's table (`flight.steps`), the turn the body's counts table;
the growing wall touches the first and not the second. The two c: in
Links per interval unchanged, `1 / sqrt 3` (a ruler made of Links grows
with the board, every local measurement of c returns it); in original
Nodes per interval `c_0 / a(t)`; the invariant `c a = c_0`.

### 15.4 The Milne case and the register's 24 stars at rest

A board whose wall grows by one part in `1 / H` per interval, `a = 1 + H
t`, is the Milne universe: `q = 0`, no acceleration. G2's `coasting_none`
registers the crowd's fit `q = -0.108` inside the coasting bracket `+-
0.25`, `H (t_0 + T_0) = 1.026`, rms 0.0019 in z (section 2.5). Under the
tick wall the 24 thrown stars are AT REST at their places and their z is
the growth between the light's release and its reading:

    z = tau / (T - tau),   T = 1 / H + t_r,

with tau the light's age at the reading. Against the register's z per
star (the hubble_stars README's table, tau from 22.6 to 144.5 intervals,
z from 0.0611 to 0.4922): at `T = 440` (the README's own Milne column)
the rms is 0.0044 and the worst residual 0.0082 (`s_pz3`), the same
numbers as the README's column because the formula is the same; the
register's free fit (q free, H free) reaches 0.0019. **The map is an
identity, not a test**: a thrown coasting star has `z = v / c` and `tau =
v (T - tau) / c`, so `z = tau / (T - tau)` too: the coasting throw from a
point and the growing wall give the SAME `z(tau)` (Milne's equivalence of
the empty expanding space and the explosion in a static one). The
birth-tick wall's `z = H tau` at the same H fails the far stars (rms
0.08, worst 0.155): the second order decides between the local forms,
not between the two models.

**What separates the two models on the register.** (i) The centre: the
throw is isotropic from its point only (every other star sees the crowd
receding one way); the growing wall is isotropic from every Node. (ii)
The bound: the law's registered Doppler reads `z = v / c` (the README:
"the redshift the detector reads of a star's light is the Doppler of its
motion times its clock"), bounded by 1 at the cap; the growing wall's `z
= e^(H d / c_0) - 1` passes 1 at `d = (c_0 / H) ln 2`: a star with `z >
1` refutes the throw under the law's Doppler and not the wall. (iii) The
fields: a thrown star's field moves with it (section 12); a star at rest
under the wall has a static field, so series K's readings (a row neither
bent nor delayed) hold unchanged, and the push between two stars at rest
is the rest push at every a. (iv) The fan's grain does not dilute (15.5).

### 15.5 What the growing wall does to the fan, to the drive, and to Seeliger's accumulation

**The fan's grain.** The directions are the table's, `F_P`, and the
Bresenham lines are the same at every a: the angular grain of a source's
fan (section 3.2's shell density `N(r)`, the two slits' 91 or 1423
directions) is unchanged by the growth; only the pace along each line
falls. So the far field's discreteness does not dilute: a distant source
is read on the same lines with rows farther apart along them.

**The drive under form B.** The body's wall `Q S M S_1 Q + |p|_1 T_D`
carries `T_D`; the consistent rule scales it too, `T_D -> T_D a`: the
same primitive as the rows' (light the body of no content, record 186),
the cap `c_0 / a` in Nodes per interval, a body at rest at rest, a
moving body slowed in Nodes per interval exactly as a row is. One
change, "`T_D` grows to `T_D a` wherever it is a wall", covers the flight
and the drive; the turn's wall is untouched (15.3).

**Seeliger.** In a static periodic world an eternal source's field
accumulates (section 14.3): the light's reach `c_0 t` covers `(2 c_0 t /
L)^3` periodic images whose fluxes `1 / (4 pi d^2)` sum to about `4 pi
c_0 t / L^3` beyond the nearest, growing without bound, linearly in t
(the script, L = 301: 27 images at 1000 intervals, 30 307 at 10 000, the
presence rising past the nearest image's share after some `10^4`
intervals). Under the tick wall the reach saturates, `(c_0 / H) ln(1 + H
t)`, and every image's flux is cut off by `e^(-H d / c_0)` at the Hubble
length `c_0 / H` (233 Links at H = 1 / 400): 2, 19 and 81 images at
1000, 3000 and 10 000 intervals, the presence constant at 0.000765 of
`q dwell` from 1000 intervals on. **Cured**: a periodic world under the
growing wall does not fill, its clocks do not slow toward zero, and
section 14.3's third stream ends in a steady presence.

### 15.6 The three tests on the rule "the flight's wall is `2 T_D a`, a rising at H per interval"

- **Generic**: passes. One wall factor for every family and every
  direction, a declared H, no name; a body's drive the same primitive
  with the same factor.
- **Vector**: passes. A translation whose wall is a count (the growth
  factor an accumulator at the rate H, the wall its value times `2
  T_D`): F's feedback block with the interval as the read state, the
  rate untouched, no root, no float, the integers `H_den + H_num t`.
- **Local**: passes if the row's tick is a local reading (its own
  interval, which every record carries), and then reads only the row's
  own accumulator; fails if a count every Node shares is a global
  quantity. The age form passes the test and gives no redshift; the
  birth form passes and gives the wrong second order.

### 15.7 The verdict of section 15

**Reached** for the form: the expansion as a growing wall of the flight,
c in Links per interval unchanged, `c a = c_0` a consequence, the
redshift `1 + z = a(t_r) / a(t_e)` from the flight's slowing against the
turns' constant rate, the Milne case `q = 0` inside the register's
bracket, the 24 stars at rest reproduced by the same Milne relation the
throw obeys (rms 0.0044 at the README's T), Seeliger's accumulation
cured. **Corrected**: the local wall read off the row's age gives no
redshift; the wall must read the tick (or, at the wrong second order,
the birth tick); whether the tick is a local reading is the decision that
admits the rule. **Different from the throw** in the centre, the bound
(`z > 1`) and the fields, not in `z(tau)`. The constant total computation
of record 218 is the stepping form's reading of the one constant K over
a growing board (section 13) and adds nothing to the rule; the periodic
universe and the rule's entry are the owner's.

## 16. The numbers of nature from the law's structure: what is reached as c was, what is bound or related, what is input

**The question** (the owner, records 239 and 243, translated: "try all
the things, all the numbers they measured; try to derive them yourself
from the groups, like big G, and other numbers known in nature; try to
reach them yourself, as you reached c"; "so maybe mass is not a free
parameter: the minimal mass"; the Boss's order). The host script
[nature_numbers.py](designs/derivations_beam/nature_numbers.py) with its
output [nature_numbers.out](designs/derivations_beam/nature_numbers.out)
makes every number below; no run.

**The rule against numerology, stated first and applied throughout.** A
number of nature is reached only by a path from the law's structure
(16.3) that passes the three tests (generic, vector, local) and yields
the number as c was yielded: as the value of a defined quantity in the
law's own units, with no search. A match found by searching combinations
of the structure's integers is a coincidence, reported with the chance
of finding one at that tolerance in a set of that size, never a result.
"Not reachable from the structure" is a valid and expected answer for
most of the list, and no constant enters PREDICTIONS.md as derived
unless its path passes the three tests. 16.4 applies the rule to the
one near-match the search finds.

### 16.1 What c had, and what a constant must have to be reached the same way

c is a property of the lattice alone: the flight's Manhattan accumulator
(rate `2 S_1 Q`, wall `2 T_D`) crosses at most one Link per interval on
every line, and the largest isotropic pace with that property is the
cube diagonal's, `S_1 Q <= T_D` by Cauchy-Schwarz with equality on the
diagonals (section 13.2 (a); record 186). So c is DIMENSIONLESS in the
law's units, `1 / sqrt 3` Links per interval, fixed by locality and
straightness on the cube, and its SI value, 299 792 458 metres per
second, is a unit conversion: a ruler-and-clock reading between two
detectors (Highlights 5.7's dictionary, record 191). What c had: a
quantity defined by the law (the operator norm of the flight), a
structure that fixes it (the cube, the six Ports, one carry per
interval), and no declared number in it.

**The consequence for every constant that carries units.** In the law's
units a Link, an interval, a unit of content and a phase step are the
units, so every dimensional constant of nature is one of three things:
1 or a ratio of the grain (c; the age per Link `sqrt 3`; the dwell `55 /
32`), a declared column of the world (G is the width, `G = K (n / d) /
(4 pi S)`, section 3.3; h is the world's `action`; e is `rho M`, the
charge per unit of content times the content; the Coulomb constant is G
itself, section 3.4), or absent (k_B: the law has no temperature;
section 14's entropy is in bits, and Boltzmann's constant is the
conversion of bits to joules per kelvin, a unit). None of them can be
reached as c was, because none of them is dimensionless: G, h, e and c
in SI are the dictionary's four conversions, as physics itself says of
its units. What can be reached, in principle, are the DIMENSIONLESS
numbers of nature. The list, with one source each (CODATA 2022: Mohr,
Newell, Taylor and Tiesinga, Rev. Mod. Phys. 2025; PDG 2024: Navas et
al., Phys. Rev. D 110, 030001; Planck 2018: Aghanim et al., A&A 641, A6,
2020):

| the number | the measured value | source |
| --- | --- | --- |
| the fine-structure constant `alpha = e^2 / (4 pi epsilon_0 hbar c)` | `1 / 137.035999177(21)` | CODATA 2022 |
| `m_p / m_e` | 1836.152673426(32) | CODATA 2022 |
| `m_mu / m_e` | 206.7682827(46) | CODATA 2022 |
| `m_n / m_p` | 1.00137841946(40) | CODATA 2022 |
| `m_tau / m_e` | 3477.23(23) | PDG 2024 |
| the gravitational coupling `alpha_G = G m_p^2 / (hbar c)` | `5.906 x 10^-39` | from CODATA 2022's G, `m_p`, hbar, c |
| the strong coupling `alpha_s(M_Z)` | 0.1180(9) | PDG 2024 |
| the weak coupling: `G_F / (hbar c)^3` and the Weinberg angle `sin^2 theta_W` (MS-bar at `M_Z`) | `1.1663788(6) x 10^-5 GeV^-2`; 0.23122(4) | CODATA 2022; PDG 2024 |
| the electron's anomaly `a_e = (g - 2) / 2` | `1.15965218 x 10^-3` (the last digits at 1 part in 10^10) | CODATA 2022 |
| the deceleration `q_0 = Omega_m / 2 - Omega_Lambda` | -0.53 (from `Omega_m` = 0.315(7), `Omega_Lambda` = 0.685) | Planck 2018 |
| the density ratios `Omega_b`, `Omega_c`, `Omega_Lambda` | 0.049, 0.265, 0.685 | Planck 2018 |
| the photons per baryon `1 / eta` | `1.63 x 10^9` (`eta = 6.12 x 10^-10`) | Planck 2018 (PDG 2024's BBN review) |

### 16.2 The minimal mass: a theorem of the law, and what follows from it

**The theorem.** In the law a body's mass is its content M, and M is a
whole number of units: the amounts of the state vector are integers (a
row's amount, a body's `content`, `1 <= M`, the masses design's bound
`M <= K_clock (N / 2 - 1)`), and every place the mass acts reads that
integer linearly, the inertial mass in the drive's wall `Q S M` (form B:
`Q S M S_1 Q + |p|_1 T_D`), the passive gravitational mass in the push
`M_A (rho_A rho_B - 1) V` and the active one in the release, `content x
n / d` rows per direction per self-creation (the turn's rate). So the
smallest mass of the law is ONE UNIT, `M = 1`, and every mass is a whole
multiple of it: fixed by the integer form of the state, not declared,
as c is fixed by the lattice; a mass between 0 and 1 unit, or between 1
and 2, does not exist in the law. **Reached, with its scope stated**:
the theorem fixes the existence of a least mass and the integrality of
every mass ratio; it does not fix the unit's size against any body's
mass (the electron may be one unit or a million), because every map of
the law on the amounts is linear or homogeneous (PREDICTIONS 26: no
number of the law selects a mass), so the unit is the least count and
not a scale.

**(a) The ratios as rationals, and the electron's count.** If the
electron is k units, the proton is `k x 1836.152673426` units to the
measured precision, a whole number only for some k. The script's table
(A), at CODATA 2022's uncertainties:

| the ratios required whole | the smallest k (the electron's units) | the counts |
| --- | --- | --- |
| `m_p / m_e` alone | 4526 | the proton 8 310 427 |
| `m_mu / m_e` alone | 889 | the muon 183 817 |
| `m_p / m_e` and `m_mu / m_e` | 13 840 | the proton 25 412 353, the muon 2 861 673 (the masses design's k at CODATA 2018, unchanged) |
| with `m_n / m_e` | 45 129 | the proton 82 863 734, the neutron 82 977 955, the muon 9 331 246 |

At `k = 1` (the electron one unit, the catalog's 1836) the proton's
count is off by 0.152673 units, `8.3 x 10^-5` of the ratio and `4.8 x
10^6` standard deviations: **the electron is not the minimal mass**, or
the unit is finer than the electron by at least the factor 4526 (the
proton's ratio alone) and 13 840 (with the muon). But this is the
arithmetic of a fine grid, as the masses design said: any k above the
inverse precision fits, 989 567 of the k below 3 000 000 fit the proton
and the muon together, and the law fixes no k. So the theorem BOUNDS
the unit (`m_unit <= m_e / 4526`) and relates the ratios (all rational);
it derives none of them. **Bound and related, not reached.**

**(b) The second definition of mass, from the computation.** Section 13
counts the cost: a body's own accumulators cost 5 operations each per
interval whatever M (the drive, the turn, the owed count), so a body's
INERTIAL mass costs nothing per unit; what M costs is its RELEASE, `12
P` operations per row born times `content x n / d` births per direction
per self-creation, linear in M; and the wait it causes in every reader,
`26 k / K` intervals per self-creation for the k rows read (13.2 (b)),
reads that release count. So the computational definition of mass is
the rows a body puts on the GameBoard per interval over its rate `n /
d`, and it agrees with the first definition as an identity: it is the
same integer M read at the release instead of at the drive. The
agreement is the equivalence principle of section 3.3 (the source's
rows `content x n / d`, the reader's response `1 / (Q S M)`, `M_A`
cancelling) and adds no number: the unit of content costs `12 P n / d`
operations per interval to hold on the board and 26 to read, both
functions of the widths and not of nature's masses.

**(c) The unit in kilograms.** A conversion of the dictionary and
nothing the structure fixes: the law's mass unit is `m_e / k` with k the
electron's count, bounded below by (a) and otherwise free; the only
mass a structure could fix would be a combination of the law's
constants, and `sqrt(hbar c / G)` in the law's units is `sqrt(h (4 pi
S) / (sqrt 3 x 2 pi K (n / d)))`, two declared columns (the width S and
the action h) and the fan's count: declared, not structural. **Input**,
with the theorem's bound.

### 16.3 The law's structural numbers: what a derivation may use

The only things a derivation may use, each a count of the law's form
and not a declaration of a world:

| kind | the numbers | where |
| --- | --- | --- |
| the cube | 3 axes, 6 Ports, 2 hands; the group of the Ports of order `48 = 2^3 x 3!` (the signed permutations of the axes), its 24 rotations and 24 reflections (the determinant the hand) | record 226; `core.game_board` |
| the flight | `c = 1 / sqrt 3`; the age per Link `sqrt 3`; on the register's grain `T_d = 110, 156, 192` at `Q = 64` (the heading, the face and the cube diagonal), the dwell `55 / 32` | sections 1.4, 13.2 (a) |
| the collision table | `3^8 = 6561` slot states (8 slots: six headings and two rest slots, each empty, single or crowd), 5440 classes, 4429 fixed states, 2132 moving, the cycle lengths 1, 2, 3, 4, 6 (4429, 933, 52, 23, 3 classes) | `ladder.out` A; section 11.3 |
| the samplings, declared per world | N (the circle of phases, 64 on the register), W (the wheel, 4096), Q (the pace's grain, 64), P and the fan (5 and 290 directions; 16 and 1423; the Bohr shell 2616), `K_clock` (`2^20`, `2^22`), the width S | Highlights 5.7 (1); section 13.3 |
| the operations | the six verbs; the Gram form of rank 2 with its eight totals `65448 .. 65773 / 65536` (the rounding at 1 / 256); the one threshold; the wait `26 k / K`; the push's columns (gravity, charge, strong) with one constant `k_C = G` | sections 0, 6.5, 13.1, 3.4 |
| the limits they reach | `2 sqrt 2` (the Bell bound, 6.2); the Gleason power 2; `log2 N = 6` bits per record; `4 pi` (the shell); Milne's `q = 0` | sections 6, 14, 15 |

Everything else in a world file is an input: the family table (content,
the cost h, rho, sigma, the lifetime, the phase rate, the hand), the
width, the state and the apparatus (Highlights 5.7's three kinds).

### 16.4 Each number of nature against the structure

| the number | the path, if any | what it yields | verdict | what would have to be added, named as a hypothesis |
| --- | --- | --- | --- | --- |
| `alpha` | In the law `alpha_law = k_C q_e^2 / (hbar c)` with `k_C = G = K (n / d) / (4 pi S)`, `q_e = rho_e M_e`, `hbar = h / (2 pi)`, `c = 1 / sqrt 3`: `alpha_law = sqrt 3 K (n / d) (rho_e M_e)^2 / (2 S h)`; equivalently the electron's speed over c on Bohr's first orbit, `2 pi sqrt 3 M k / h` (7.2's closure), the width, the charges and the action all declared. The search over the structure (the script's (C): 3360 products and quotients of two structural numbers with the exponents 1 and 2): the nearest is `3^8 / 48 = 136.6875`, 0.25 % below `1 / alpha`; the set has 136 values within a factor `e^(1/2)` of 137, so 0.82 hits within 0.3 % are expected and 1 is found: a coincidence at the expected rate, reported and not a result | a ratio of three declarations | **input** | a rule tying `rho^2 S` to `h`: charge quantised in units of `sqrt(h c / G)` times a number the structure fixes (none is in sight; `charge-v1`, not built) |
| `m_p / m_e`, `m_mu / m_e`, `m_n / m_p`, `m_tau / m_e` | the family table's contents, rational by 16.2's theorem; the electron's count bounded below (4526; 13 840; 45 129); the search: nearest `5440 / 3 = 1813` (1.2 % off) and `24^2 / (2 sqrt 2) = 203.6` (1.5 %), 0 hits within 0.3 % where 0.7 are expected | rationals with a bound on the unit | **bound and related, not reached** | a nonlinear closure on amounts (a binding that costs content, issue #369; the masses design section 6's smallest rule) under its own identity |
| `alpha_G` | `alpha_G,law = G M_p^2 / (hbar c) = sqrt 3 K (n / d) M_p^2 / (2 S h)`: declared. With `alpha` it is RELATED by the one constant `k_C = G` (3.4): `alpha / alpha_G = (q_p / M_p)^2 = rho_p^2`, so nature's two couplings declare one number of the family table, `rho_p = sqrt(alpha / alpha_G) = 1.11 x 10^18` per unit of content (e in units of `sqrt G m_p`), and the neutrality of matter gives `rho_e = -rho_p m_p / m_e = -2.04 x 10^21`; the register's [1, 1] and -15 are a scale chosen for the runs (the masses design 4); the ratio of the electric to the gravitational force on the electron-proton pair is then `alpha m_p / (alpha_G m_e) = 2.27 x 10^39`, an identity of the form | one declared rho for two of nature's numbers | **related, not reached** | the same as alpha's: a rule fixing rho; nothing in the structure carries `10^18` (the largest structural number is 6561; W is 4096) |
| `alpha_s` | the strong column, `sigma = 10 000` with the sign -1 and the lifetime 3 on the register, a declared value per unit; the law's couplings do not run (every rule linear or homogeneous in the amounts, no scale in the coefficients): `alpha_s(M_Z)` = 0.118 against `alpha_s` about 1 at 1 GeV is a running the law has not | a declared column | **input**, the running absent | a coupling that depends on the momentum transfer: outside the six verbs as a rate at most bilinear in the state; a hypothesis named, not built |
| the weak coupling, `sin^2 theta_W` | the law's weak rule is `become` at a key on the age with a lifetime L (HYPOTHESES 21, series J): a transformation at a count, not a rate proportional to a coupling; no second gauge coupling and no mixing between two, so no angle | nothing | **absent** | two couplings and their mixing: a structure the law does not have |
| `a_e = (g - 2) / 2` | the law has no spin and no magnetic moment: a body's readings are the moments of the arriving rows (order 0, 1, 2 and the age), its hand a `Z_2` (the determinant of the cube's group) with no coupling; g is undefined | nothing | **absent** | a spin and a magnetic coupling, both outside the reading operator as it stands |
| `q_0` | section 15: the growing wall at a constant H gives Milne, `q = 0`, exactly; the register's throws `q = -0.108 +- 0.25`; nature's -0.53 +- 0.05 (Planck 2018) is outside both | 0, a bracket | **reached for the form (0), not for nature's number** | a rising H (a second rate on the wall under `expansion-v1`), giving `q < 0`: a hypothesis, the register cannot pin it (section 15.4's identity of the throw and the wall) |
| `Omega_b`, `Omega_c`, `Omega_Lambda` | the contents placed in the initial state (Highlights 5.7 (3)); no rule of the law fixes a ratio of contents (16.2's theorem: linear in the amounts) | nothing | **input** (the state) | none within the law: the initial state is the third kind of input |
| the photons per baryon | the law's counterpart is the rows per unit of held content on the GameBoard: `P x (n / d) x t` rows per unit released over t intervals from a free family's rate, unbounded in time (no absorption balances the release; a linear law has no equilibrium of rows and bodies, no temperature); section 6's units per bit (82, 2, 2, 29) are the apparatus's, section 14's `log2 N` bits per record the click's; none is `1.6 x 10^9` | a number of the world's age and rate | **absent** | an equilibrium between the release and the absorption (a thermal state), which needs a nonlinear rule |

### 16.5 What the search says, and the rule applied

The one near-match, `3^8 / 48 = 136.6875` against 137.036, is 0.25 %
off, and 0.82 hits at 0.3 % are expected from the set's own density:
its chance is of order one, and it has no path (no rule of the law
divides the collision table's slot states by the cube's group, and the
quotient would be a count of orbits, an integer, not a coupling).
Reported as a coincidence. The masses find no hit at 0.3 % where 0.7
are expected. The search confirms the rule's expectation: with about
twenty-five structural numbers and their pairwise products, a match at
a few parts in a thousand to any given target is expected about once,
and none of the matches has a path.

### 16.6 The verdict of section 16

**Reached as c was**: nothing on the list, and the reason is stated:
every constant with units is a conversion of the dictionary (G the
width, h the action, e the charge per unit of content times the
content, k_B absent), and the dimensionless numbers of nature are ratios
of those declarations or of the initial state, none a count of the
structure. **Bound or related**: the minimal mass, one unit, a theorem
of the integer form, with every mass ratio rational and the electron at
least 4526 units (13 840 with the muon) so that the unit is below the
electron's mass by that factor at least; `alpha` and `alpha_G` related
through the one constant `k_C = G` to one declared number, `rho_p =
sqrt(alpha / alpha_G) = 1.11 x 10^18` per unit of content, and the
neutrality of matter giving `rho_e` from it; `q = 0` reached for the
form and nature's -0.53 not. **Input**: `alpha` (three declarations),
the mass ratios (the family table), `alpha_G` (the width), `alpha_s`
(the strong column, no running), the density ratios (the state).
**Absent**: the weak coupling and the Weinberg angle (a key, not a
coupling; no mixing), `g - 2` (no spin), the photons per baryon (no
equilibrium). **What each would need**, named and not built: a rule
fixing rho against h and S (charge quantised in `sqrt(h c / G)`), a
nonlinear closure on the amounts for the masses, a running coupling
for the strong column, two couplings and a mixing for the weak, a spin
for `g`, a thermal balance for the photons, a rising H for `q`. **The
rule against numerology** held: one coincidence at the expected rate,
no path, no entry in PREDICTIONS.md.
