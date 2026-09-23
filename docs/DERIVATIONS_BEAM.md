# Derivations of the known laws from the Beam Law (round 9 onward)

The canonical statement of this algebra is [docs/ALGEBRA.md](ALGEBRA.md), section 2 (the operations), 4 (the identities) and 5 (the map's rows); this file is kept as the record of 2026-09-22.

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
| psi, **k** | scalar field, vector | the wave function of the continuum limit (section 23; a field of the limit, never a state of the lattice) and its wave vector `k = 2 pi p / h` |
| d, `d_p`, eta, **q** (section 25) | scalars, vector | the six-heading gas's density per heading slot and per rest pair at rest, and the Fermi-Dirac parameters of its invariant measure |
| g, `c_s`, `nu_L`, Gamma, **D**, **A** (section 25) | scalars, tensor, operator | the Galilean factor, the sound speed, the longitudinal viscosity, a sound wave's damping rate, the diffusion tensor of the tagged unit, the linearized collision operator |
| Theta, r (section 25) | scalars | the temperature reading `(1 / n) sum p_a^2 / (Q S M)` per axis, and a lamp's cooling rate `h b n / d` per self-creation |
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
| E, `E_0` (section 17) | scalars | a body's energy as an accumulator of the work; its rest value `Q S M c^2` |
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
Boss relayed it); sections 9 and 10 answer records 166 and 162; section 11 answers record 190 (the GameBoard as one vector map between events); section 12 answers record 200 (Lorentz from the delay field) and 12b revisits it with the moving reader's count and the orbit as the bond; 12c answers record 230 (the mover's counter under the crossing count and the owed count, route C); section 13 answers record 209 (the one constant K, the computation per Node per interval); section 14 answers records 214 and 215 (entropy); section 15 answers records 215 and 218 (the growing wall); section 16 answers records 239 and 243 (the numbers of nature from the law's structure, the minimal mass); section 17 answers the owner's direction of 2026-09-21 (the law above Newton and Einstein: the theorem of covariant readings); section 18 answers records 264 and 265 (the three structural failures of the register under one logic); section 19 answers the owner's direction of 2026-09-21 on the masses (a bound set's mass as its total content, the nucleon as a chain of three on the bipartite lattice); section 20 answers record 270 (the periodic universe against the measured numbers); section 21 is the derivation map for the paper (every formula with its premises, script, run, the pin before the run, the order of the expansion, the error term and status; 21.4 the Einstein map; 21.5 the standard of record 300 and the new rows); section 22 answers records 291 and 292 (the uncertainty relation from the six verbs, and Bell); section 23 answers record 331 (Schrodinger's equation and the massive row, massive-rows-v1, reached only in part); section 24 answers record 337 (the inputs ledger, the bilinear rate forced, the Delta P table and the one prediction, S = 181 / 64); section 25 answers record 343 (the big formulas of the continuum: flow, heat, temperature, the inventory of round 1 and the derivations of round 2); section 26 answers the paper coordinator's list under record 352 (the ten formulas the paper wants and the derivation lacks, each with its standing, the identity or program and the pin). The
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

    s <- s + r;   e <- sign(s) x min(floor(abs(s) / d), at_most);   s <- s - e d,       (1)

every wall crossing an event, `at_most` the cap of that component (the
count primitive `core.integer.by_drive`, and `by_drive_rows` on the rows'
arrays, `nature_beam.py:519`): the accumulator gains the signed rate, the
count is the whole part it then holds in units of the wall, capped at
`at_most` where a cap is declared and the whole part otherwise
(`at_most = 0`), that much is subtracted and the remainder stays, the
sign of a reversed rate first cancelling what was accumulated the other
way (record 126). Which counts carry the cap: the drive alone, `at_most =
1` (`engine.py:126`, `step_axis`; form B's directional drive the same,
one Link per interval on the Bresenham line, 24.3's step cap), the rest
of a larger count kept and fired one per following self-creation. Every
other count takes the whole part, `at_most = 0`, and can fire several
events in one interval: the turn (a lamp at the rate `content x n` over d
turns s steps per self-creation, 6.4), the owed count, the release, the
lamp, the push per column, the counts table of `measured.py:232`; the
owner's high-rate series 0, 2, 5, 7, 10 (record 340: a rate of 5 against
a wall of 2) is this form and not the 0 / 1 form. The 0 / 1 form `e <-
[s >= d]` holds exactly where the rate never exceeds the wall: the
flight (`2 S_1 Q <= 2 T_D`, at most one Link per interval, 1.2 step 1),
the drive (by its cap), the birth wheel (rate 1, wall W), a clock whose
rate is below its wall; the paper's Eq. (1) follows this one. The components of **s** and their (r, d): a
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

      s(t) = floor(s_0 + r t)     (the accumulator's cumulative count at a constant rate, r the rate as a fraction of the wall: the carries made by t; the residual on the torus is `(s_0 + r t) mod 1`; FORM.md section 1),

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
`floor(s_0 + r t)` for its count of carries (the residual its fractional
part; the external reviewer's F13): its state at the click is a formula
of its birth,
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
  form `acc += r; e = [acc >= d]; acc -= e d`, every wall crossing an event, is the division with the remainder kept,
signed and truncating (Eq. (1): the count `sign(s) floor(abs(s) / d)`,
the remainder with the accumulator's sign in `(-d, d)`, so an
accumulator at -1 against the wall 2 counts 0 and keeps -1, where the
Euclidean division would count -1 and keep 1; Euclidean for a
non-negative accumulator, the case of every unsigned count; the external
reviewer's F13), the bijection `Z = Z/d x Z` on the pair (`core/integer.py:70-86`,
`by_drive`), the one primitive of every count;
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
- **(D) the signed truncating division with the remainder kept** (the same as (T)'s carry; Euclidean on a non-negative accumulator) and **the comparison** (the ladder's cell `2 T u + T <= 2 N C_k`,
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
| The digital line (Bresenham): at Manhattan step j the axis maximising `abs(v_i) (j + 1) - S_1 abs(pos_i)`, the lowest axis on a tie | `nature_beam.py:580-592` | (T)+(D): three deficit accumulators, each gaining `abs(v_i)` per Manhattan step, the carry `S_1` taken from the largest (a comparison, the axis furthest behind); ties by axis order | a torus operation with a declared tie (x before y before z), the second declared breaking of the 48 beside the collision's Port-order tie (the auditor's round 2, on a fan world of five directions): covariant on the six headings and on every direction without a tie; for a tied direction ((1, 1, 0), (3, 1, 2), (0, 1, -3); not (2, 1, 0) or (1, -2, 0)) the 40 axis permutations move the Nodes crossed and the exit face, not the label `u_d`, the momentum or the hand; the table `lines` its cache |
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
| The receiver's Doppler `1 +- v / c` on the axis | **reached under the crossing rule, built** (the model owner's record 158 of 2026-09-20; BEAM_LAW note 48; on `main` since PR #468 at 562fb736, 2026-09-21): a reader moving one Link per k intervals meets `k + 55 / 32` rows per k intervals toward the source and `k - 55 / 32` away, `c = 32 / 55` on an axis; exact over whole Links and within one row otherwise; the counts pinned in `tests/test_crossing.py`: 45 rows in 32 intervals toward at k = 4 and 58 in 48 at k = 8, 19 in 32 and 38 in 48 away, 48 in 48 at rest; over 32 Links 183 = 128 + 55 and 311 = 256 + 55 toward, 74 and 202 away, `1 +- v / c` with `c = 32 / 55`; the note's caveat (a reader faster than one Link per two intervals is counted, not proved); the G2 run under the rule not yet made, its expectations to be pinned first; record 153's earlier finding (k rows per k intervals, the Doppler not reached) was the engine before the rule and is history | `c = Q / T_d`, the table's rational; the boundary row |
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

**Reached exactly.** Registered as a GAMEBOARD reading of the probes (the
host's view of the state, a diagnostic, never a measurement): series C
item 5, the flux through the square of half-width h over q is `1.0000`
at h = 4, 8, 12, 20, 40 and the escape through the faces `1.0000 q` (the
tool sums the Links crossed, `per_port`, the walk's own diagnostic). The
detector reading of Gauss's law is not made.

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

**The registered check, a GAMEBOARD reading** (series C item 5, world 5,
the nine radii; the probes' view of the state, a diagnostic; the tool's
ring is `abs(dist - r) < 0.5`, `engine.py:1120-1143`): the register's `count x r / q` and `flow x 2 pi r / q` are `r / N(r)` and `2
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
register's GAMEBOARD readings; the detector reading of the inverse square
(Newton after a detector) is not made.

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
equivalence principle is exact (item 1 registered as a GAMEBOARD reading of
the probes' momenta, a diagnostic: `push_m = m x push_1` record by record
for m = 1, 4, 16, and the step rule divides by M_A). The third law at rest
is exact to the apportioning's grain (item 2, GAMEBOARD: the two sources'
momenta `9612145197056` and `-9612088573952`, the ratio 1.0000). Every
series C number of this section is the host's view of the state; the
detector reading of Newton's law (Newton after a detector) is not made,
and only it would be a measurement. **Reached in the shell mean, G named**; per Node in the limit of every
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
| The inverse square | **reached** in the shell mean, `<V> = q Q / N(r)`, `N(r) -> 4 pi r^2`; per Node only in the limit of every direction; the nine ring readings of series C (GAMEBOARD, the probes' reading) are `r / N(r)` and `2 pi r / N(r)` exactly | the Gauss circle problem's ripple `r^(theta - 1)`; a cube fan's `3^(3/2)` |
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
v below `c_1`: no two-way COUNT inside the crowd detects the motion
(`n (c_1 + v) + n (c_1 - v) = 2 n c_1`, the null of the count, exact),
while a one-way count of one stream detects it at first order (section
2). The round-trip TIME is another quantity and is not null: a signal
sent along the motion and back takes `2 L c / (c^2 - v^2)`, `gamma^2`
times the rest along the motion and `gamma` across (section 12.3, the
ether light clock; NATURE.md row 5b, the registered FAIL at `beta^2 /
2`), second order in v. The preferred frame is measurable by a one-way
count and by a two-way time, and by no two-way count.

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

    P(x, t) = q(t - r / c) x dwell / (4 pi r^2)            (dwell = T_d / (abs(D) Q) intervals per Euclidean Link along the direction, 1 / c on every direction within the table's grain, 1.72 on a heading),

(the external reviewer's F05, 2026-09-21: per Node on its line a row
dwells `T_d / (S_1 Q)` intervals, one per Link on the cube diagonal
where `T_d = 192`, and a line has `S_1 / abs(D)` Nodes per Euclidean
Link, so the rows' presence per Euclidean length is the isotropic `T_d /
(abs(D) Q)`; the earlier `T_d / Q` was the heading's case alone) and the
age moment is the presence times the age the rows carry, `r / c` (each
row's age at r is the light-travel time):

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
the push is its gradient. The registered check is series E, a GAMEBOARD
reading of the probes' clocks and presences (the host's view of the state,
a diagnostic; the detector reading of Poisson's source term after a
detector is not made): `k_s x r^2 =
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
slows; nothing stops a clock). Registered as a GAMEBOARD reading of the
probe clocks (a diagnostic; the one detector reading of the field's outside
form is series T, NATURE row 12): series E's rate ratios `rate(r)
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
| Poisson's equation for the delay field | **reached**: the age moment is the retarded potential `q(t - r/c) dwell / (4 pi c r)`, the presence its flux; series E's (GAMEBOARD, the probes' reading) `k_a r = 36.1`, `k_s r^2 = 41.5`, the ratio `sqrt 3 / 2` | linear, additive over sources |
| The retarded wave equation of the field | **reached** (a scalar field propagating at c, sourced by the release) | no self-source |
| The gravitational redshift | **reached at first order** (`1 / (1 + k)`, the 1 / r form of series E (GAMEBOARD, the probes' reading)); **different law** at second order, no horizon | the strong field k = 2 .. 9 registered |
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
birth wheel `u = ordinal mod N`. What they cost: (i) the CUMULATIVE probability up to a cell is `b_k / N`, a multiple
of `1 / N`, within `1 / (2 N)` of the cumulative Born weight `C_k / T`
(the paper's row 3, proved from the rung); a single cell's count `b_k -
b_(k-1)` is therefore within one of `N W_k / T` and its probability
within `1 / N` of the Born weight `W_k / T`, and a cell of weight below
`1 / (2 N)` clicks at most once per wheel, not never (the external
reviewer's F02, 2026-09-21: at N = 64 the weights 49, 2 and 6349 of
6400 give the rungs 0, 1 and 64 and the counts 0, 1, 63, the middle
cell of weight `2 / 6400` clicking once): the Mach-Zehnder's dark port
at the offers `1 / 1682 = 0.0006` reads 0 of 64 because its rung rounds
to 64 (Born's 0.04), and `mz_345` reads 63 / 1 where the rung moved one
u into D2 (L1, registered); (ii) the
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
sqrt 2`, the powers of two from 512 to 8192 exactly `181 / 64`, the
plateau, 24.4; above it S oscillates about the tables' `186034 / 65773`
within `2 x 10^-4`, the external reviewer's F01), two-sided within the
bound. **Reached as a limit**: the finite-N departures are the terms
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

**The dictionary of h (the external reviewer's F08, issue #553, closed
here by one calibration).** The law has two keys that nature writes as
one constant: the family's `quantum`, `h_q`, paid per phase step (this
section), and the world's `action`, `h_A`, that turns the phase by
`abs(p) N / h_A` steps per Link (7.2, 23.1). Planck's constant read from
the release is `h_q N` (content x interval per cycle: `E = h_q s = (h_q
N) f`); read from the wavelength it is `h_A` (the momentum label p is the
physical momentum in the units the drive fixes, `v = p / (Q S M)` Links
per interval, 3.3, so `lambda = h_A / p` Links and `p lambda = h_A`,
content x interval per cycle, the same unit). One Planck constant is the
calibration

    h_A = h_q N,    h = h_q N = h_A,    hbar = h / (2 pi),    E = h f,    lambda = h / p,    k = 2 pi p / h,

a constraint on the inputs beside 17.6's `3 h_q n = Q S d` (the click's
`E = h f` and the drive's `E_0 = Q S M c^2` one energy at rest), not a
rule: with both, the family's quantum, the world's action, the pair `[n,
d]` and the width S describe one energy and one action. The check the
register already holds: a photon of turn rate `n / d` (`f = n / (d N)`
cycles per interval) has `E = h_q n / d` and `p = E / c`, so `lambda =
h_A / p = (h_A / h_q) c d / n`, which is the wave's `c / f = c N d / n`
if and only if `h_A = h_q N` (23.3's `256 / 55` Links from `h / p` and
from `c N d / n`, the point of that pin). The limit `N -> infinity` of
section 22 is taken at fixed h (the physical action): `h_q = h / N -> 0`
with the phase step `2 pi / N`, the Link and the interval fixed, the
momentum a label whose turn per Link, `p / h_q` steps, is `2 pi p / h`
radians; so `hbar = h N_phi / (2 pi)` in the paper's letters (h there the
quantum) and `hbar = h_A / (2 pi)` (h the action) are one number. CLOSED
as a calibration (24.1 row 25); what stays INPUT is the value of h.

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
- (c) counts: `R(f) >= 0`;
- (d) the empty reads zero: `R(0) = 0` on the zero count vector (the
  owner's condition, record 340);
- (e) some input reads: R is not identically zero (record 340).

Not assumed: continuity, a dimension, the form of R on one row, or
Theorem 2's `A = sum a_i^2`.

**Theorem (the lattice Gleason).** Under (a) to (e), with N a power of
two and `N >= 4` (N = 2 has no quarter turn; the register's N run from
32 to 4096),

    A_2 = 2,   R(f) = sum over odd j, 1 <= j < N/2, of c_j |sigma_j(f)|^2,   c_j >= 0,
    sigma_j(f) = sum_p f_p exp(2 pi i j p / N)     (the j-th Galois conjugate of ev(f); sigma_1 = ev).

The exact classification behind it (the auditor's round 1, a host check
on the integers for N = 4 to 1024): under (a) to (c) either R is constant
with `A_2 = 1`, or `R(0) = 0` with R not identically zero and then `A_2 =
2` and the sum form; the zero function satisfies (a) to (c) with every
`A_2`. Every such R is a positive quadratic form on the lattice, homogeneous,
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

**Proof.** (i) g = 0 in (b) with (a) and (d): `R(x^{N/4} f) + R(f) = 2
R(f) = A_2 (R(f) + R(0)) = A_2 R(f)`, so `A_2 = 2` at any f with `R(f) !=
0`, which (e) supplies. (ii) Replace g by
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
`(a, b)` splitter with the quarter turn), the cross terms `a b B(f,
x^{N/4} g)` and `a b B(g, x^{N/4} f) = a b B(x^{N/4} g, x^{N/2} f) =
-a b B(f, x^{N/4} g)` (B as (iii) defines it, `R(f + g) - R(f) - R(g)`)
cancel and the total is `(a^2 + b^2) (R(f) +
R(g))`; the label rotation's pair `(C' f + S' x^t g, -S' f + C' x^t g)`
cancels the same way with `C'^2 + S'^2`. (vii) Two rows: `|sigma_j(a +
b x^D)|^2 = a^2 + b^2 + 2 a b cos(2 pi j D / N)`, and at `D = 0, N/4,
N/2` the cosine is `1, 0, -1` for every odd j. (Each identity of (vi) and (vii) was also checked numerically on random
elements at N = 64.)

**The two conditions added (the owner, record 340: "the conditions
stated for the theorem allow a detector that always returns 1, so by
themselves they do not force a quadratic weight").** Without (d) and
(e) the constant function `R = 1` satisfies (a), (b) and (c) with `A_2 =
1` (both sides of (b) read 2 at every f, g), so the old statement admitted
it and its proof used `R(0) = 0` silently at step (i). With (d) and (e):
step (i) forces `A_2 = 2`, and the constant fails (b) (2 against 4); the
other function the old conditions admitted, `R = c > 0` on every nonzero
vector and `R(0) = 0`, passes (i) but fails (b) at `f = -x^{N/4} g`
(`R(2 g) + R(0) = c` against `A_2 (R(f) + R(g)) = 4 c`); and steps (ii)
to (vii) run as written, (iii)'s `R(0) = 0` now a hypothesis and not a
consequence. Why the code satisfies both, in one line: a cell with no
rows has the zero count vector and the weight `f^T G f = 0` (the click's
zero on the empty; `amplitude.py`'s `gram_form` over no phases), the
GameBoard's cancel and the click's zero are one relation (above), and
one row of amount w alone reads `(32 w)^2 x 256^2 > 0` (BEAM_LAW section
5), so R is not identically zero.

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
  total, not by T at birth) is the rule that keeps one click per record under that violation (one
click per record, `b_K = N`, every u in exactly one cell, rests on `T >
0`, which the isometry theorem supplies for a record born with a
nonzero row whose every end is an offer; at `T = 0` the engine's guard
gathers nowhere, the auditor's round 4b).

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
`[1.917, 2.489)` and `[1.784, 2.054)`); with the (3, 4) split registered
at N = 32 and 128 as well (`mz_345_n32` reading `31 / 1`, `mz_345_n128`
reading `125 / 3`, both met exactly, PR #563 at 34f505ec; the register's
`mz_345_n.power_windows` and `mz_345_n.intersection`) the windows
`[1.548, 2.129)`, `[1.917, 2.489)` and `[1.835, 2.012)` intersect in
`[1.917, 2.012)`, the lower bound N = 64's and the upper N = 128's,
containing 2 and excluding 1 and 3 (the auditor's round 4). **Not reached** from the
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
no Link is the collision: `_collide` permutes every single
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
give: the value `1 / sqrt 3`. One Link per interval on every line is
anisotropic: a heading row advances 1 Link per interval, while a
cube-diagonal row needs three Links for the displacement `sqrt 3` and
advances `1 / sqrt 3` per interval (a row stepping on all three axes in
one interval would advance `sqrt 3`, and K forbids it: one carry per
interval). An isotropic pace is therefore bounded by the slowest line,
the cube diagonal's: `c <= 1 / sqrt 3` (`S_1 Q <= T_D`, Cauchy-Schwarz
with equality on the diagonals: c is the operator norm of the flight,
record 186). The same Euclidean pace in every direction (the flight
table's isotropy, `T_D = isqrt(3 |D|^2 Q^2)`) is a second axiom, and it
gives the inequality, not the value; the equality, the flight table's
sitting AT that supremum and not below it, is a third statement of the
design beside locality and straightness, since a slower isotropic pace
obeys both (the owner's finding, record 262; the paper's, record 253).
In the owner's terms: what is derived is the largest uniform pace the
GameBoard allows under locality and straightness; that the rows realise
it (the third statement) and what a detector in motion reads of it
(section 4.2, the one-way count `c -+ v`) are stated, not derived.
**Partial**: K fixes the bound
(one carry per interval, the Manhattan count as the least computation),
isotropy bounds the number and the third statement fixes it; the count against K is the walk's 16
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
record. The division keeps its remainder (signed and truncating, 1.2
(T); the carry a bijection `Z = Z / d x Z`, record 173). So the number of state vectors
consistent with the clicks does not change while no click, cancel or
discarded remainder happens: the flow on the torus preserves the count,
the lattice's Liouville theorem, and the linear block produces no
entropy at all.

### 14.2 Production at the click, the cancel and the discarded remainders

**The observation map, stated once** (issue #586, the owner's testing
agent, 2026-09-21; the paper's 2096 to 2097 and 2542 to 2547). Two
records exist at a click. The run's record (the `gather` line of
`amplitude.py` and the click line's fields `record`, `u`, `born`, `share`,
`age`, `exact`, `remainder`, `window`) is the host's diagnostic record
(record 281: a GameBoard reading): it keeps the record's identity and its
birth coordinate u, and nothing below deletes them. The observable
output is the click's OUTCOME: the cell the click fell in (the pixel,
the port, a setting's outcome) and its tick, what a detector in nature
reads; the outcome list K is what section 14 counts against. The count
of this section is the number of birth coordinates consistent with the
outcome list, and its identity

    H(K) + H(U | K) = H(U) = log2 N     (U uniform over the wheel, K = f(U) the cells' partition of it)

is Shannon's chain rule for a uniform source and a deterministic
partition, an identity about that coarse graining of the record: `H(U |
K)` is the freedom of u the outcome does not report, not a deletion of
u from the run's record, where `H(U | C) = 0` for the complete record C
that carries u. It is not an H-theorem and not a thermodynamic second
law: nothing in it supplies a temperature or a heat (16.4, 25.8), and
14.3's monotone streams are counts that only grow. The one list of what
leaves the STATE (the GameBoard's state vector, not the run's record),
with its bits: (1) the click, the record's vector deleted, `log2 N - H`
bits of u not reported by the outcome; (2) the cancel under the amplitude
key, two amounts, `log2` of their range; (3) the escape at a face, a
row's position and phase, at most `log2 (extent x N)`; (4) the discarded
remainders on `main`, at most `log2 d` each. "Only the click deletes"
(14.1, 25.1's F3) means that among the law's steps between events the
click is the one non-bijective step on the state; the cancel and the
escape stand beside it in this list, each at its own rule.

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
   sense above (the count against the outcome list, 14.2's observation
   map; a count, not a thermodynamic law) is non-decreasing, by `log2 N -
   H` per record clicked (6 bits
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
law's units, `1 / sqrt 3` Links per interval, fixed by the three
statements of 13.2 (a) (the cube diagonal's bound from locality, the
isotropy as a second axiom giving the inequality `c <= 1 / sqrt 3`, and
the flight table's sitting at the supremum as a third statement;
records 253, 262), and its SI value, 299 792 458 metres per
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

**(d) The smallest mass per kind** (the owner, record 256, translated:
"maybe several masses must be derived: the electron may be the
smallest and the quark the smallest, and the quark composes the
protons and neutrons; try to reach the smallest mass by kind from our
conditions"; the host script
[smallest_mass.py](designs/derivations_beam/smallest_mass.py) with its
output [smallest_mass.out](designs/derivations_beam/smallest_mass.out)).
The law's own condition that fixes a floor is the charge line: a
family's charge per unit of content is a reduced pair `rho = [n, d]`
and a body's charge is `rho x M`, so `rho x M` is a whole number if and
only if d divides M. **Theorem**: the smallest content of a family
whose bodies carry a whole charge is its reduced denominator d. The
law does not impose the whole charge (the masses design, section 4:
nothing forbids `rho = 1 / 7`); nature does (every free body's charge
a multiple of e), so the theorem is conditional on that fact and
exact under it. The floors on the register and the quark design: the
electron `[-15, 1]` and the proton `[1, 1]` one unit, the up quark
`[2, 3]` and the down quark `[-1, 3]` (records 249, 251) three units
each, a family declared at `[-5, 69]` sixty-nine. The quarks design
(QUARKS.md, PR #454) puts the up quark on 4 units and the down on 9
with the elementary charge declared as `e = 7344` label units, so that
every quark charge is a whole number and rho a pair with denominator 1:
the design fixes the charge per unit by choosing e, and its counts are
multiples of the floors (the floors 1 and 3 are the smallest counts
under nature's whole charge in units of e / 3, the design's counts the
nearest whole numbers to PDG's masses), not the floors. Confronted:

- **(a) with the electron's bound.** The theorem gives the electron's
  floor as 1 unit and 16.2 (a) gives its count as at least 4526 by the
  proton's ratio: no contradiction, the count is a multiple of the
  floor (any multiple of 1); the theorem fixes floors, the ratios fix
  multiples, and neither fixes the other. The smallest counts that
  meet CODATA 2022 stay 4526 (the proton alone) and 13 840 (with the
  muon).
- **(b) with the quarks as the base.** At the floors the proton `u u
  d` is 9 units of charge `2 / 3 + 2 / 3 - 1 / 3 = 1` and the neutron
  `u d d` 9 units of charge 0: `m_n / m_p = 1` exactly against nature's
  1.00138, and `m_p / m_e = 9` at the electron's floor against 1836.15:
  the floors are not the masses, refuted at once, so the counts are
  multiples of the floors. If the binding carries no held content
  (today's law: a free family's rows carry none), a nucleon's count is
  a sum of quark counts and hence a multiple of 3: the smallest
  electron count with the proton's count a multiple of 3 within CODATA
  is 4657 (the proton 8 550 963), with the neutron's too 32 206 (the
  proton 59 135 133, the neutron 59 216 646), with the muon 74 512; at
  16.2 (a)'s 4526 the proton's count is `8 310 427 = 1 mod 3`, not a sum
  of quark floors. Under binding-v1 (record 115, candidate (b): the
  strong family's rows paid, the exchange as content in flight, the
  read mass the held part) the constraint lapses and the read mass is
  the parts' sum LESS the content in flight: a bound set lighter than
  its parts, the sign of the deuteron's defect; nature's nucleon is
  HEAVIER than its quarks by a hundredfold (the current masses 2.2,
  2.2, 4.7 MeV against 938.3), so a tower whose quark contents are
  nature's current masses gives the wrong sign, and the tower's quark
  contents would have to be the constituent masses (about a third of
  the nucleon each): a statement for the quarks physicist's design, not
  a derivation.
- **(c) the kinds of the law and the smallest member of each.** Rows
  of a free family: content 0, no floor to fix. Rows of a paid family:
  `quantum x s` at the turn s, the smallest the family's h at `s = 1`,
  fixed by the declaration h and by nothing structural. Bodies with a
  charge: the floor d of the theorem, conditional on the whole charge.
  Bodies with sigma only (the strong family, no charge line): the floor
  1 of 16.2's theorem, no further condition (the strong column is a
  value per unit with no denominator that must divide). Passed families
  with a phase window (`pass` with `phase_window`): their content enters
  no rule that divides, the floor 1. So the conditions of the law fix
  exactly one floor beyond the unit, the charged body's d, and fix no
  count: the electron's, the quarks' and the nucleons' masses stay
  inputs with the floors 1, 3, 3 and the multiples of (b).

**(e) G, the width, and what a rule fixing it would have to be.** In
the law's units `G = K (n / d) / (4 pi S)` (section 3.3: the release
rate per unit of content per direction, times the fan's count, over
`4 pi` and the width), and with the one constant `k_C = G` (3.4)
`alpha_G = alpha / rho_p^2` (16.4). A rule fixing S from the structure
would have to make S a count of the structure times declared columns,
and two candidates can be stated so that they can be chosen: `S = K
(n / d) / (4 pi)`, which is "G = 1 in Links per unit of content per
interval squared" (Newton's constant one, the natural-units choice:
generic, a constant at load, local), and `S = sqrt 3 K (n / d) / (2
h)`, which is "the unit of content is the Planck mass" (`sqrt(hbar c /
G)` = 1 unit, 16.2 (c)). The second is refuted at once: `alpha_G = (m_p
/ m_Planck)^2` would then be `M_p^2 >= 1` against `5.9 x 10^-39`, so
the unit must lie below the proton by at least `1 / sqrt(alpha_G) =
1.3 x 10^19`. The first moves the number instead of deriving it: with
`G = 1`, `alpha_G = 2 pi sqrt 3 M_p^2 / h` puts `10^38 M_p^2` into the
action h. Either way the hierarchy `alpha / alpha_G = rho_p^2 = 1.2 x
10^36` must be carried by a declaration, and no count of the structure
(the largest 6561, the wheel 4096) carries it: **none in sight**; the
choice of S is a choice of units, and `alpha_G` stays the width's
input.

**(f) The Link, the interval, the unit and the computation, from c, G
and hbar** (the owner's three questions in conversation, record 266,
translated: "extract the lattice's length from G, and then you could
know the size of the universe"; "bring the computation into S and G and
try to give these numbers"; "maybe G is the one that varies"; the host
script [units_from_g.py](designs/derivations_beam/units_from_g.py) with
its output [units_from_g.out](designs/derivations_beam/units_from_g.out)).
Three paragraphs, each with its assumptions named.

*The three units from the three conversions.* c, G and hbar are the
dictionary's three conversions (16.1) and they fix exactly the law's
three units, the Link L, the interval T and the unit of content M in
SI, given the law's two declared dimensionless numbers `G_law = K_fan
(n / d) / (4 pi S)` (`K_fan` the fan's direction count) and `hbar_law =
h / (2 pi)`: from `c = L / (sqrt 3 T)`, `G = G_law L^3 / (M T^2)` and
`hbar = hbar_law M L^2 / T`,

    L = l_Planck / sqrt(3 sqrt 3 G_law hbar_law),   T = L / (sqrt 3 c),   M = m_Planck sqrt(sqrt 3 G_law / hbar_law),

equivalently the Link is the gravitational radius of one unit, `G M /
c^2`, over `3 G_law`; the universe's size in Links is its diameter over
L and its age in intervals its age over T. **Not derived**, because S
and h are inputs (16.2 (c), 16.4); what the structure gives is the
relation and one bound: 16.2 (a)'s `m_unit <= m_e / 4526` forces
`G_law / hbar_law <= 4.9 x 10^-53`. The cases (the script's (A)): both
numbers 1, the Planck choice, gives `L = 7 x 10^-36` m, `T = 1.4 x
10^-44` s, the universe `1.2 x 10^62` Links across and `3 x 10^61`
intervals old, and is refuted by the mass bound (the unit `3 x 10^22
m_e`); the bound saturated with `hbar_law = 1` gives `L = 1` nm and `9 x
10^35` Links; with `hbar_law = 10^6`, `L = 10^-12` m and `9 x 10^38`
Links. The size in Links is fixed only when the action h and the width
are: one more number of nature, which the structure does not carry.

*The computation in G.* Two things must be kept apart: the width S (the
inertia per unit of content) and the GameBoard's extent X (Nodes per
side); the total computation per interval is `K_budget X^3` (section
13). The computation enters G through the clock: the redshift's constant
of 5.2 is `G_clock = K_fan (n_r / d_r) (n_s / d_s) / (4 pi)` (the age
moment times the suspension pair; `dwell x c = 1`) and the push's of 3.3
is `G_push = K_fan (n_r / d_r) / (4 pi S)`; nature has one G for the
redshift and the orbit, so the two are one if and only if `n_s / d_s =
1 / S`, and with 13.2 (b)'s reading of the suspension as the reading's
cost over the budget, `[n_s, d_s] = [26, K_budget]`,

    S = K_budget / 26,      G = 26 K_fan (n_r / d_r) / (4 pi K_budget):

the width is the budget over the reading's cost, and gravity's strength
is the inverse of the computation per Node per interval. **Derived**
from 3.3, 5.2 and 13.2 (b) under two assumptions named: one G (nature's)
and the budget reading (13.2 (b), partial); series E has `S = 1` and
`[1, 1]`, the two G one trivially. With the mass bound, `K_budget >= 26
K_fan (n / d) hbar_law / (4 pi x 4.9 x 10^-53)`, of order `10^51` to
`10^55` operations per Node per interval (the script's (B): `K_fan =
290`, `n / d` from `1 / 4096` to 1, `hbar_law = 1`): gravity is weak
because the reading of one row costs 26 of a budget of `10^52`; the
budget is not fixed without `hbar_law`, the same missing number as the
Link's.

*What varies: not G.* A constant TOTAL computation over a growing board
(`K_budget X^3` constant with `X ~ a`) gives `K_budget ~ 1 / a^3` and
hence `G ~ a^3`; under Milne, `a ~ t`, that is `Gdot / G = 3 H = 2 x
10^-10` per year, against lunar laser ranging's bound of order `10^-13`
per year (Hofmann and Muller 2018): refuted by three orders, so the
computation per Node is constant to a part in `10^3` of H, as section 13
assumed, and a varying G is excluded (Dirac's `G ~ 1 / t`, `-H`, with
it). The reconciliation is section 15.1 (b): under the growing wall no
Node is inserted, `X^3` and K are fixed, the total `K X^3` is constant,
G is constant, and the varying quantity is the pace in the original
Nodes, `c_0 / a` (the invariant `c a = c_0`), which is the redshift; the
conflict arises only under 15.1 (a), inserting Nodes. A local
measurement of G (the Moon's orbit) reads `G_SI` in local units, which
the wall does not change; a comparison between two places or two
epochs is made by rows and is the redshift, not G. **Answered**: not G;
the computation per Node, the width and G are constants of the law, the
pace in the original Nodes is what the expansion changes, and the three
numbers above are the two inputs' (h and S), not the structure's.

**(g) Whether any rule selects a bound set's counts** (the owner, record
271, translated: "there is only one quantum of mass because a click
cannot measure mass; the other masses need to be derived from it, but
we do not know how to derive mass at a click"). The owner's reading is
the law's: a click measures `E = h f`, the content of a paid unit, never
a mass; a mass is read by the push (the dictionary, Highlights 5.7),
and the one quantum of mass is the unit of 16.2's theorem. Whether the
other masses derive from it is the question whether any rule of the
six selects the count of held rows of a bound set, so that some counts
are stable under the dynamics and the rest are rejected. Read against
every rule that touches a bound set: binding-v1's read mass is the
exact sum of the held parts (the quarks design: 20 units against
1836, record 115); the strong column's push is linear in the contents
(`M_A (rho_A rho_B - 1) V`, homogeneous); the contact rule hands over
momentum, not content; the lifetime L ends a row and the escape click
releases its content whatever the set's count; the give is `held // h`
with the remainder kept, so a body whose held content falls below h
gives nothing, a FLOOR of h per bound body and not a count; the steady
state `F = H (n / d) tau` holds for every H. **No rule of the six reads
a content back into its own survival**: every map of the law on the
amounts is linear or homogeneous (PREDICTIONS 26), so every count is
stable and none is selected, and the only selections the law makes are
floors (the unit, a charged family's d, the give's h). A selection
would need a nonlinear closure on the amounts (the masses design's
section 6: a window set by the reader's own phase, which gives a
harmonic ladder nature does not show), stated under its own identity,
outside the law. So the paper states the masses as inputs with this
reason: the law fixes the quantum and the floors, and a linear law
cannot fix a count.

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

## 17. The law above Newton and Einstein: the theorem of covariant readings, built on Newton and tried on Lorentz

**The owner's direction** (2026-09-21, in conversation, translated: "I
want to show that our formulas are above: that whoever accepts our
formulas, our linearity, and what you wrote, can obtain from them E =
m c^2 and all the formulas Einstein reached"; then: "build it correctly
on Newton too, and try on Lorentz"). No new rule is proposed here. The
section states what "above" means as a theorem, proves it for the
linear block, builds it on Newton (where the law already stands) and
tries it on Lorentz (where the law does not), naming for each rule of a
body the reading that would inherit the symmetry, within the six verbs,
as a candidate and not a build. The host script
[covariant_readings.py](designs/derivations_beam/covariant_readings.py)
with its output
[covariant_readings.out](designs/derivations_beam/covariant_readings.out)
makes the numbers; no run. The script is a floating-point consistency
check of the proposal, not the exact discrete proof: its parts (A) and
(D) use `gamma(beta)` with a square root, and its part (C) integrates
`dE = c^2 p . dp / E` by the midpoint rule to about `10^-8`; "without a
root" below names the PROPOSED form (the accumulator with the remainder
kept), and the exact discrete form, integers and remainders with the
invariant closed to the grain, is what covariant-readings-v1 must prove
before it is built.

### 17.1 The theorem, and what "above" means

**The two blocks** (section 0). The linear block is the rows: the
flight at the pace c on the digital lines, the merge in `Z[Z_N]`, the
evaluation at `zeta_N`; its continuum limit is the retarded scalar wave
equation at c (section 5.1: the age moment is the Lienard-Wiechert
potential, the presence its flux, both sourced by the release), and the
symmetry of that limit is the Poincare group, Lorentz's boosts with the
translations (section 4.1: "reached as the symmetry of the wave
equation the rows converge to, not as a symmetry of the lattice"). The
feedback block is the bodies: a body is its content M, its momentum
vector **p** and its counts table, and it acts on the linear block
through four READINGS, each a rule declared in the lattice's frame: the
drive (**p** into a pace, the wall `Q S M`), the turn (the content into
phase steps per self-creation, `content x n / d`), the push (the first
moment of the arriving rows into a change of **p**) and the count (the
rows met, by the crossing rule, into the owed count).

**The theorem.** Every quantity defined by covariant operations on the
linear block's limit (the retarded potential and its derivatives, the
crossings of world lines, the proper time along a world line, the sums
of the rows' energy-momentum vectors) transforms as the block does; so
a body ALL of whose rules are such readings inherits the block's
symmetry, and for it Einstein's kinematics and dynamics follow by the
standard argument (a Lorentz-covariant dynamics with a conserved
energy-momentum vector gives the Lorentz transformations of its
clocks and rods, `E^2 = p^2 c^2 + m^2 c^4`, `E_0 = m c^2`, the
relativistic Doppler and the velocity addition). Conversely, every
rule that reads the block in the lattice's frame (per interval, per
Link, along the lattice's axes) breaks the symmetry at the order at
which the frame enters. So "our formulas are above Einstein's" is
TRUE of the linear block and of everything built from it alone, and,
for the bodies, exactly as true as their four readings are covariant.
The content of this section is therefore the checklist: for each of
the four readings, whether it is covariant as declared, and if not
what its covariant form within the six verbs would be. **Reached** as a
theorem for the linear block (the wave equation's symmetry, section
4.1, is the whole proof); the rest is the checklist.

### 17.2 Built on Newton: what the readings give at v << c, and where the law leaves Newton

Newton's laws are the readings' limit at small momentum, and every one
is registered:

| Newton's | the reading | the limit | the registered check |
| --- | --- | --- | --- |
| the first law (inertia) | the drive: **p** an accumulator translated by nothing between pushes (T) | a body with no rows arriving keeps **p** exactly | G2's 24 thrown stars, `abs(p(end)) / abs(p(0))` = 1.0000 (section 11.4) |
| the second law `F = m a` | the push `-M_A <V>` (B), the drive `v = p / (Q S M + p / c)` | `a = push / (Q S M)` for `p << Q S M c`: `F = m a` with `m = Q S M` | series 7's `push_m = m x push_1` for m = 1, 4, 16 (section 3.3, item 1) |
| the third law | the apportioning of the rows' momentum at the release (the free family's release takes no recoil, section 12.4) | the two sources' momenta equal and opposite to the grain | `9612145197056` against `-9612088573952` at rest (section 3.3, item 2) |
| gravitation `G M / r^2` | the shell mean of the flux, `G = K (n / d) / (4 pi S)` (3.3); the age moment obeying Poisson's equation (5.1) | the inverse square, retarded at c; the equivalence principle exact (`M_A` cancels) | series E's (GAMEBOARD, the probes' reading) `k_s r^2 = 41.5`, `k_a r = 36.1`; series D's orbit |
| Galilean composition | the momenta add (the drive reads `p`) | velocities add where `v` is linear in `p` | 12b.2's shear at `0.21 c` is the departure |

**Where the law leaves Newton, and in what order.** Under form B the
drive is `v = p / (m + p / c)`, so `p = m v / (1 - v / c)`: the law's
momentum departs from Newton's `m v` at FIRST order in `v / c` (the
script's table (B): 5.3 %, 11 % and 25 % at `v / c` = 0.05, 0.1 and
0.2), where nature's `p = gamma m v` departs at second order (0.13 %,
0.5 %, 2.1 %). The register's throws use the first-order form
(HYPOTHESES 21's `p = S M v / (1 - v)`, the hubble stars at 0.6 c, G2's
at 0.5 c). So "built on Newton" is exact at `v << c` and the law's own
correction is one order too early: a body at a twentieth of c carries 5
% more momentum per unit speed than Newton's, a registered fact of the
drive and not of nature. The covariant drive of 17.3 (iii) has the
right order. The same check on the other three readings: the turn per
interval, the push as the flux and the count per interval are all
Newton's at rest and at `v << c`, with no correction at first order in
the isotropic case (12c: the count's dipole averages to 0), so Newton
stands on all four; only the drive's cap enters at first order.

### 17.3 Tried on Lorentz: the four readings against the checklist

**Einstein's 1905 argument as the test of the count.** A body at rest
emits two pulses of energy `L / 2` forward and back; in a frame moving
at `beta` their energies are `(L / 2) gamma (1 -+ beta)`, the sum `gamma
L`, so the moving body's kinetic energy fell by `(gamma - 1) L`, the
inertia lost `L / c^2`: `E = m c^2`. The law's reader counts the rows
by the crossing rule, `(1 -+ beta)` without the `1 / gamma` (12b.1: the
number one factor short), so the two pulses sum to `(L / 2)(1 - beta) +
(L / 2)(1 + beta) = L` exactly (the script's (A)), the difference is 0
and no inertia is lost: `Delta m = 0`. The missing `1 / gamma` of the
count IS the missing `E = m c^2`: the reading that breaks Einstein's
first derivation is the count per interval, and nothing else in it.

**(i) The count.** A crossing of two world lines is an event, and the
number of crossings along a segment of the body's line is a Lorentz
invariant: the crossing rule's NUMBER is covariant (12b.1: it is
Maxwell's magnetic term's number), and 12c showed it exact. What is
not covariant is its RATE: the count is divided by the lattice's
interval and not by the body's proper time. The covariant reading:
the count per TURN of the body (its self-creations under (iv)
below), which is `gamma (1 - n . beta)` times the rest count, the
relativistic Doppler exactly (the script's (D): head-on 1.583 and
3.637 at `0.43 c` and `0.86 c` against today's 1.430 and 1.859; across
`gamma` = 1.108 and 1.956 against today's 1, Ives and Stilwell's
transverse Doppler). No new verb: the same comparisons (D), charged per
turn instead of per interval.

**(ii) The push.** The law reads the retarded FLUX along `n_ret`
(section 12.1: `q / (4 pi R_ret^2)` on the co-moving pair, `(1 -+
beta)^2` and `(1 - beta^2)`, one factor of `1 / gamma` short of
Maxwell's and along `n_ret` where Maxwell's is along the present
separation). Section 12.1 proved that the age moment IS the
Lienard-Wiechert scalar potential, whose equipotentials are
Heaviside's ellipsoids; the covariant reading of the force is
therefore the GRADIENT of the age moment across the six Ports (the
finite difference of the neighbouring Nodes' age moments: the body
reads its six neighbours, LOCALITY-1's allowance, nothing kept at a
Node), with the flow's age-weighted moment as the vector potential
(`A = beta phi` for a moving source) and its time difference as the
induction term. A linear combination of the readings (B), local, no
name: Maxwell's field of a moving charge exactly in the limit, the
Heaviside compression `gamma / d^2` across the motion, the `1 /
gamma` the flux lacked. Under it a bound pair in motion is Lorentz's
pair of 1904: contracted by `1 / gamma` along the motion, its period
`gamma` times the rest, no self-force (12.2's `4 beta` was the flux
form's).

**(iii) The drive.** `v = p / (Q S M + abs(p) / c)`: a rational
function declared in the lattice's frame, first order off Newton
(17.2) and never Lorentz's. The covariant dispersion is `v = p c^2 /
E` with `E^2 = p^2 c^2 + E_0^2`, which as a closed form needs the root
(the seventh verb, records 186 and 197). It does not need it as an
OPERATION: carry E as an accumulator of the body's record whose rate is
the work, `dE = c^2 (p . dp) / E` (the bilinear form `p . dp` over the
state's own wall E: one `by_drive` with the remainder kept, the same
verb as the flight against `T_D` and section 15's wall as a function
of the read state), and the drive `v = p c^2 / E`: a translation at a
rate, no root anywhere. The script's (C) integrates it from rest under
pushes: `E^2 - c^2 p^2` stays `E_0^2` to `5 x 10^-12` after 40 000
steps (the invariant kept by the accumulator's form; whether the
remainder closes it exactly is the implementer's), `E / E_0` = 1.2166 =
`gamma` at `v = 0.57 c`. **And then E = m c^2 is forced**: the
accumulator's rest value `E_0` is fixed by the Newtonian limit, since
`v = p c^2 / E_0` at small p must be Newton's `p / (Q S M)`, so `E_0 =
Q S M c^2 = Q S M / 3` in the law's units, with no freedom; the
inertia of energy follows: a body that pays content `h s` for a row
loses the row's energy from its accumulator E, so its inertia `E / c^2`
falls by that energy over `c^2` (Einstein's 1905 conclusion as an
identity of the accumulator), and a bound pair's `E` is the sum
of its parts' less the exchange's, a mass defect (the deuteron's 0.119
% of the masses design becomes a quantity the exchange sets, not an
absence). The first-order departure of 17.2 becomes nature's
second-order one (the script's (B): 0.13 % at `0.05 c`).

**(iv) The clock.** The turn `content x n / d` per self-creation and
one self-creation per interval owed nothing: the rate 1 at every speed
(section 4.3, HYPOTHESES 21). The covariant reading: the turn per
proper time, `dtau = dt E_0 / E`, one `by_drive` whose rate is `content
x n x E_0` and whose wall is `d x E` (the wall a function of the read
state, section 15.2's form): the clock at `1 / gamma` exactly, no root
(`E_0 / E` is a ratio of two accumulators). The muon of J4 fires its
64th turn at 70.9 and 125.2 (the script's (D); lorentz-v1's 71 and 126
by the root at `2^20`): the same numbers, from the accumulator instead
of the seventh verb. And the two readings of E become one: the click
reads `E = h f` with f the turn rate, the drive reads `E_0 = Q S M
c^2`; at rest one E requires `h (n / d) = Q S c^2 = Q S / 3` (21.33 at
Q = 64, S = 1), the identity of 12.4's "coincidence of declared
constants" turned into the condition that the family table's h and
`n / d` and the world's width describe one energy: a constraint on the
inputs, derived, and not a new rule.

### 17.4 What follows for whoever accepts the readings, formula by formula

| Einstein's formula | from which reading | status as declared | status under the covariant readings |
| --- | --- | --- | --- |
| the Lorentz transformation of the rows' field, `omega = c k`, the light cone | the linear block alone | **reached** (4.1) | the same |
| `E = p c` for a row | the row's content and momentum (`quantum x s` both) | **reached**, declared per unit (16.1) | the same |
| the Doppler `gamma (1 -+ beta)`, the transverse `gamma` | (i) the count per turn | different law, `1 -+ beta` and 1 | reached |
| the field of a moving charge (Heaviside), the magnetic term | (ii) the gradient of the age moment | different law, the flux along `n_ret` | reached in the limit |
| `E = m c^2`, the inertia of energy, the mass defect | (iii) the energy accumulator with the Newtonian limit | not reached (4.5) | reached, `E_0 = Q S M c^2` forced |
| `E^2 = p^2 c^2 + m^2 c^4`, `v = p c^2 / E`, the velocity addition | (iii) | different law, `p / (m + p / c)` | reached (the invariant kept to `10^-12`) |
| the time dilation `gamma`, the muon's lifetime | (iv) the turn per proper time | different law, 1 (HYPOTHESES 21) | reached, 70.9 and 125.2 |
| the contraction `1 / gamma`, the bond's period `gamma` | (ii) with (iii) and (iv) | different law (12b.2: 0.87 to 0.96, 1.31 to 1.43) | reached (Lorentz's 1904 argument on Heaviside's field) |
| the general formulas: the redshift at first order, Poisson's equation | section 5 | reached at first order | the same |
| the bending of light, the Shapiro delay, the second-order redshift | the rows reading the crowd | not reached on `main` (5.6): the flight is blind to the crowd | unchanged: these need a rule on the LINEAR block (a row's pace read off the field), outside this theorem, which reads only the bodies |

### 17.5 The verdict of section 17

**Above, as a theorem**: the linear block's limit carries Lorentz's
symmetry, so every formula of Einstein's special theory holds for
whatever is built from it alone, and for a body exactly as far as its
four readings are covariant. **Built on Newton**: all four readings
give Newton's laws at `v << c`, registered (inertia 1.0000, `F = m a`,
the third law to the grain, `G M / r^2` with one G); the law's own
correction to Newton is the drive's, first order in `v / c` where
nature's is second. **Tried on Lorentz**: as declared, three of the
four readings are in the lattice's frame and Einstein's 1905
derivation gives `Delta m = 0` with the law's Doppler; the covariant
form of each exists within the six verbs, the count per turn, the
gradient of the age moment across the six Ports, the energy as an
accumulator of the work with the drive `p c^2 / E`, the turn per proper
time `E_0 / E`, no root anywhere; and then `E = m c^2` is forced by the
Newtonian limit, the invariant `E^2 - p^2 c^2` is kept by the
accumulator, the muon fires at 70.9 and 125.2, and the identity `h (n /
d) = Q S c^2` ties the inputs. **What stays outside**: the general
formulas beyond first order, which need the rows to read the crowd,
not the bodies. **For the owner and the Boss**: the four covariant
readings are named as one hypothesis, `covariant-readings-v1`, four
rules that pass the three tests on paper and change every moving
body's register; not built here; the seventh verb is not needed for
any of them. The owner decided (record 270) that covariant-readings-v1
is built beside the law in place of lorentz-v1.

### 17.6 Amended per the physics-rule review of covariant-readings-v1 (record 297): the nine must-fixes, the integer forms, the should-fixes

The review (docs/designs/derivations_beam/REVIEW_COVARIANT_READINGS.md,
the physics-rule reviewer, 2026-09-21; ADMISSIBLE WITH MUST-FIXES) found
nine design sentences of 17.3 wrong, absent or unreachable on the engine
of `main`. Nothing above is rewritten; each fix below replaces the
sentence it names, marked M1 to M9, with the integers from the host
script [amended_pins.py](designs/derivations_beam/amended_pins.py) and
its output [amended_pins.out](designs/derivations_beam/amended_pins.out).
Notation, once (S2, and the Boss's decision under record 362 on
2026-09-21, applied here at this pass): **p** the momentum vector and p
its magnitude, **dp** the push of one interval (the integer `pushed` of
the record), **n** a row's unit direction, beta the speed over c, gamma
the Lorentz factor; the energy in physics' letters, E the energy, `E_0 =
m c^2` the rest energy, `m = Q S M` the mass (the paper's `N_l N_w M`),
`c^2 = 1 / 3`, the pace `v = p c^2 / E`; the exact square `Xi = m^2 + 3 p
. p`, an integer kept by comparisons and never rooted (the code's
`energy_square`; `Xi` is `(E / c^2)^2` to within the root's remainder),
and `E / c^2` its whole root, the energy in mass units, the largest
integer whose square is at most `Xi`. Where this subsection wrote `E'`,
`E'_0` and `W` before the decision, read `E / c^2`, m and `Xi`.

**M1, the counter the identity gates: the self-creation itself, by an
owed count.** The proper-time accumulator gates the SELF-CREATION, not
the phase turn: after every self-creation the body owes
`by_drive(acc_tau, E / c^2 - m, m)` further intervals (a second owed
count on the record, beside the crowd's; at rest 0), so self-creations
come one per `E / (m c^2) = gamma` intervals and everything counted per
self-creation follows proper time at once: the age (and so `become`,
which reads the age, nature_beam.py:3649), the turn (the phase per
self-creation, unchanged), the crowd's owed count, the release, the
lamp's count, and the crossing count of (i), which is charged per
self-creation as `_suspend` charges it today and is therefore `gamma (1
- n . beta)` per self-creation with no separate rule (N1 below: by a
declared sum over the owed intervals): (i) is the cadence of (iv). The
drive is NOT decoupled and does not need to be: `_move`
keeps stepping at self-creations (engine.py:522), and its rate per
self-creation is Newton's, `p / (Q S M)` on the momentum's direction
(form B's directional accumulator `by_drive(drive, abs(p)_1 S_1 Q, Q S M
S_1 Q)` WITHOUT its cap term `abs(p)_1 T_D`), so the pace per lattice
interval is the product of the two gates, `(p / (Q S M)) x (m c^2 / E)
= p c^2 / E` Links per interval, which is the covariant `v = p c^2 / E`
exactly (in the mean, with two bounded remainders, as form B's own pace
is), with the cap `1 / sqrt 3` as p grows (N2 below: on the domain
`abs(p)_1 <= Q S M`): the second slowing the
review feared is the covariant pace itself. The six counts and their
cadence under the identity: the turn, the owed count, the lamp,
`become`, the drive's gain: all per self-creation (proper time); the
release: per lattice interval (N4 below);
the reading of arrivals and the crossing count: per interval, charged
per self-creation. A consequence to own (S5): a moving body in a crowd
is charged `gamma` times the rest count per self-creation, so its
crowd's owed count grows with speed; pinned below on 12c.6's probe.

**M2, the pins on declared momenta.** With `c^2` declared as the pair
`[1, 3]` (M3): the muon of J4 (`Q S M = 13248`) at `p = 3640` and `12
856` label units has `E / c^2` at load 14 671 and 25 910, `gamma = E / (m c^2)
= 1.1074` and `1.9558`, beta read back 0.4297 and 0.8594, the 64th self-creation at 70.9 and
125.2 in the continuum and at the integers 70 and 124 by the primitive's
own count, `64 + floor(63 (E / c^2 - m) / m)` (18.1 (a) as restated;
the build reads 70 and 124) (FORM.md section 4's 5815 and 47 349,
form B's momenta, give 0.605 and 0.987 under the identity, the 64th at
80 and 401: not the pinned speeds). `coasting_none`'s `s_mz2` at its
declared `p_z = 51 901 289 008 505` (`Q S M = 2^48`) has beta 0.3042 and
`z = gamma (1 + beta) - 1 = 0.3691`; the momentum that keeps beta 0.2674
is 45 097 270 682 765 (z = 0.3153). The pin is on the REGISTERED world:
`z = 0.369 +- 0.003`; a re-declared world would pin 0.315.

**M3, the integers of E.** `c^2 = [1, 3]` declared by the identity (the
flight table's per-direction `(Q S_1 / T_D)^2`, 0.3385 on a heading, is
the alternative and shifts the muon's 64th by 0.7 tick at 0.86 c; one
pair, declared once). The energy in whole units: `E / c^2 = 3 E`, `m = Q S
M` (whole on every register), the invariant `(E / c^2)^2 - 3 p . p = m^2`,
the pace `p c^2 / E`. The state carried is NOT an accumulator of the work
but the exact square, `Xi = m^2 + 3 p . p` (bilinear in **p**, the
identity matrix declared, no drift), and `E / c^2` is kept as the largest
integer with `(E / c^2)^2 <= Xi` by comparisons only: at every interval `E / c^2`
rises by one while `(E / c^2 + 1)^2 <= Xi` and falls by one while `(E / c^2)^2 > Xi`
(the comparison verb, at most `ceil(sqrt 3 abs(dp)) + 1` comparisons
per interval for a push of `abs(dp)` label units, since `d(E / c^2) / dp <
sqrt 3`; N3 below: the push per interval is bounded by the grain, so the
count is fixed); the script's (C): 40 000 unit pushes from rest, the
invariant
`(E / c^2)^2 <= Xi < (E / c^2 + 1)^2` at every step, at most 3 comparisons per step,
`E / c^2` equal to `isqrt(Xi)` at the end. The initial `E / c^2` of a thrown body:
`isqrt(m^2 + 3 p . p)` at load, a declared load-time rounding of
`T_D`'s class (the three tests allow it), stated once for the identity;
a world may declare `E / c^2` instead, refused if below `m` or off the
invariant by more than 1. The widths: the identity declares a grain `g`
(a power of two) and carries `m / g`, `p / g` and `Xi / g^2` (the
momentum's bits below g do not enter E; the drive keeps the full **p**),
tested by division before the product is formed as `push_form` does;
on `coasting_none` `g = 2^18` puts `Xi / g^2 = 1.27 x 10^18` within
`MOMENTUM_BOUND` (`2^16` does not), `(E / c^2) / g = 1 127 172 967`; on J4 `g =
1`. The proper-time owed count's rate `E / c^2 - m` and wall `m` are of
the order of `m / g`: no product, no overflow (the earlier form
"rate content x n x E_0, wall d x E" is withdrawn with M1).

**M4, the push's vector potential: withdrawn; (ii) restated as the
gradient alone, and its integer form.** The sentence "the flow's
age-weighted moment as the vector potential" is wrong (the review's
counterexample: for a source at rest that moment is the age moment
times the radial unit vector, nonzero, while the vector potential is
0; for a moving source it is `A n_ret`, not `beta A`), and the
induction term needs the source's velocity, which no row carries and no
reading of a Node or its six neighbours gives. (ii) is restated as
`-grad(A)` alone: the push per axis is the difference of the age
moments at the two neighbouring Nodes of that axis, `pushed_a = C x
(A_(-a) - A_(+a))` with C the column's coupling as a declared pair
applied by one `by_drive` with its remainder (the factor 2 of the
central difference into the pair), the six neighbours' age moments read
as their records' presence-and-age line (a NEW reading set, keyed by the
identity, with the reading bound `reading_fits` applied per neighbour),
no previous-interval component (with no vector potential there is no
time difference to take). What `-grad(A)` alone gives on a co-moving
pair, from 12.1's potential: the rest force along the motion, `gamma`
times the rest across (Maxwell's are `1 - beta^2` and `1 / gamma`):
**Lorentz's 1904 pair is NOT derived from (ii)**, and rows E3 and E7 of
21.4 and the 5b pin of 18.1 are withdrawn from this identity. What a
local reading of the vector potential would need is stated so that it
can be designed: a row carrying its source's momentum label at release
(one more declared component of the row's record, local to the row,
generic), from which `A = beta A` is a bilinear reading at the Node;
named `source-velocity-v1`, not designed here.

**M5, the 5b pin's geometry.** 12.4's pair is a one-Link contact pair
and no push contracts it; the pin is unreachable on that geometry
under any reading. With M4 the contraction is not derived from this
identity at all, so the pin is withdrawn from 18.1 rather than moved;
when `source-velocity-v1` supplies the magnetic term, the pin's
geometry is 12b.2's thrown orbit in the Newtonian regime (S = 512 or
8192), where the extents along over across at `1 / gamma` is 0.977 at
beta 0.2148, 0.6 Link on a 26-Link radius, BELOW the grain (one Link),
so the pin needs beta at or above 0.43 (0.903, 2.5 Links on 26, "within
the grain" meaning within one Link of the 26-Link extent and within 2
percent of the rest period in intervals).

**M6, the release's E: units and owner.** 19.5's "E in place of
content" is restated: the release's rate reads the content-equivalent
of the body's OWN energy, `E / c^2 / (Q S)` in place of M, as one
`by_drive(acc_release, E / c^2 x n, Q S x d)` with the remainder kept, whole
integers; each body reads its own `E / c^2` and never "the set's" (the chain
of 19.3 has its ends two Links apart; the local test allows the record
and its six neighbours). The energy in flight between the bodies of a
bound set is in rows, not in any body's `E / c^2`, so this identity makes a
body's field its own energy's (rest plus kinetic) and leaves the
binding fraction to `field-source-v1` (21.4, E16). The world and the
detector reading that pin it: a free body thrown in an empty bar with a
probe of content 1 at rest beside its path reading the push (the active
mass from the probe's `pushed` line) against the body's drive under a
declared kick (the inertial mass from its `step` lines): the ratio 1
at rest and `gamma` in motion under the identity, both to the grain (N4
below: the release runs per lattice interval, so the pin stands);
Nordtvedt's `10^-4` is nature's number and stays in 19.5 as such.
**The per-family release as built** (PR #582, `covariant_release`; the
physics-rule review's S7): per free family f the release row of the
body's counts table gains `held_f x (E / c^2) x n` against the wall `m
x d` at every lattice interval, the owed intervals included, the
remainder kept, `by_drive(acc_release_f, held_f (E / c^2) n, m d)`: at
rest `E / c^2 = m` and the count is the law's `held_f n / d` rows per
interval exactly, in motion `E / (m c^2) = gamma` times it, the
content-equivalent of the body's own energy in place of its content,
family by family; a body of no content (m = 0) holds nothing and releases
as the law does; every product tested by division before it is formed;
no root, no family name, the body's own record.

**M7, E on a change of content.** On every change of the held content
by dM (a click's `held += content`, a release's cost `h s`, a give, a
`become`): `m` is read as `Q S M` at the frame (no state), and `Xi`
gains `Q S (2 m + Q S dM) dM` (the identity `(m + Q S dM)^2 -
m^2`, bilinear, exact), so the kinetic part `E / c^2 - m` is kept and
the rest part follows the content. The exchange's rows carry their
energy as rows (their momentum `h s` along their direction, their energy
`3 h s c = 96 h s / 55` in `E / c^2` units, a declared pair on the row), out
of the emitter's `Xi` by the same identity at the release and into the
absorber's at the click: the books balance only if `3 h n = Q S d` for
every paid family (17.3 (iv)'s identity), which the engine CHECKS AT
LOAD and refuses otherwise under the identity key (S10; none of the
register's lamps as declared satisfies it at Q = 64, S = 1: 21.33) (N5
below: the balance is withdrawn until derived, and the check is a
diagnostic line at load, a refusal only where the world declares the
exchange's accounting). The
deuteron's mass defect is then the escaped rows' energy, 17.3's claim
made exact.

**M8, the base and the order.** The identity is built on form B (record
186, decided, not on `main`): its drive is form B's directional
accumulator without the cap term (M1), and on the per-axis `step_axis`
of `main` it has no magnitude and no direction. Form B lands and
re-registers its 47 moving-body worlds first; the identity's OFF
baseline is that register, and its pull request shows the crossing
rule's validation table unchanged to the byte with the key absent (S8's
test 5). Until form B lands the identity is built on `main`'s per-axis
drive with its cap term keyed off, on the domain of a momentum on one
axis (refused otherwise), where the count equals form B's; the OFF
baseline is `main`'s register; form B's landing re-registers the
identity's worlds with the domain lifted (REVIEW_3's must-fix 1,
2026-09-21: the build under record 348, form B BLOCKED).

**M9, the pins as detector readings.** The muon's pin is restated as the
products' face clicks on a J4 world file, to be written before the run
(none exists, NATURE 4a). It declares: an open bar `[201, 1, 1]` (the +x
face at x = 200; N6), the
identity key with `c2 = [1, 3]` and `grain = 1`, the muon family
(content 207, no charge line beyond the catalog's, `become` at 64 into
the electron family with the products of the catalog and the charges
balanced), one muon at x = 10 with `momentum = [3640, 0, 0]` (a second
world at 12 856, a third at rest), `width` 1, and the two faces as
detectors reading the products' clicks. The reading: the electron
product's click on the +x face at tick 367 for `p = 3640` (the decay at
70.9 at x = 27.6, the flight 172.4 Links at 55 / 32 intervals per
Link), 345 for 12 856 (125.2, x = 72.1) and 391 at rest (64, x = 10); the
decay tick is derived back from the click by the flight table and named
as derived; the tolerance one tick on the decay, two on the click
(N6 below: re-derived 390.6, 368.2 and 345.2 with the drive's whole
steps).
Pin (b) is withdrawn (M5). Pin (c) is `coasting_none`'s detector `z`,
the pointer's `Delta t / Delta Phi` at the centre, `0.369 +- 0.003` on
the declared momentum. E and the six-Port gradient reading enter
ENGINE.md's readings by type with their kind at the build (S6): `E / c^2` a
scalar of the measured event's state (the `step` line carries it as it
carries `drive`), the gradient a vector.

**The should-fixes.** S1 done above (the rate is `3 p . dp` with **dp**
the record's push integer, bilinear; with Xi exact no rate is
accumulated at all). S2 the notation line above. S3 the key
`covariant_readings` in `WORLD_KEYS` beside `action` and `meeting`, one
object: `c2`, `grain`, and per measured event an optional `E`. S4 the
key with `action` is refused until the composition of the turn by
momentum per Link with the proper-time cadence is designed. S5 pinned
in 18.1's amendment. S6 in M9. S7 rows 38, 39 and 44 of 21.2 restated
below with their integer forms and world files. S8 the design's tests:
(1) a body at rest under the key, `E / c^2 = m`, every registered integer
of the world unchanged; (2) a thrown free body in an empty bar, `Xi`
constant, the 64th self-creation at the declared momentum's `gamma`
within one tick (J4's world above); (3) `(E / c^2)^2 <= Xi < (E / c^2 + 1)^2` at
every interval under pushes, with the count of comparisons; (4) the
edge `p = 0` with one push (`E / c^2` rises from `m` only when `3 dp^2 >=
2 m + 1`, the remainder in Xi); (5) the OFF test of M8. S9 record 291
is on `main` now and is cited above in place of the paraphrase. S10 the
load-time check refuses. S11 the counts per self-creation are per
direction of the flight table: `gamma (1 - v T_d / (Q S_1))` on a
heading, the Manhattan factor of 2.4 on a fan direction, not the
continuum's `gamma (1 - n . beta)`; 17.3 (i)'s numbers are the
continuum's limit.

**Buildable, in this reading**: yes for (iii) and (iv) as amended (one
exact square, one comparison loop, one owed count, the drive's rate
without its cap term, the load-time root and the load-time identity
check), with the J4 world and `coasting_none` as the two pinned runs;
NOT for (ii) beyond `-grad(A)`, whose magnetic part waits for
`source-velocity-v1`; the special theory's clock, Doppler and energy
close under the amended identity, its contraction does not.

**Amended per the second round of the physics-rule review (record 314;
the file docs/designs/derivations_beam/REVIEW_COVARIANT_READINGS_ROUND2.md;
BUILDABLE WITH MUST-FIXES: M2, M4, M5, M8 closed; M1, M3, M6, M7, M9
partly; none open).** Six sentences of this subsection are fixed here,
N1 to N6, each marked above at the sentence it replaces; N2 and N3 are
declarations the build carries. Nothing enters the law by them; the
identity stays `covariant-readings-v1`, a hypothesis.

- **N1, the crossing count's gamma (M1).** `counted` is one interval's
  reading and the owed intervals' readings are dropped by `_suspend` as
  it charges today, so the factor gamma was a claim. The fix: the record
  carries one more integer, the SUM of `counted` over the intervals
  since its last self-creation (the accumulator verb T, added each
  interval, reset at the self-creation; bounded by the reading bound
  times the owed count, at most two intervals' readings on the domain of
  N2), and `_suspend` charges `by_drive(acc_owed, sum x n, d)` at the
  self-creation with that sum. Then the count charged per self-creation
  is `gamma (1 - v T_d / (Q S_1))` per direction (S11) as written, and
  18.1 (d)'s pins on 12c.6's probe (0.763 / 1.300 at p = 10, 0.498 /
  2.002 at p = 28) stand. Generic, vector (a sum), local (its own
  record). The composition of the two owed counts, the crowd's and the
  proper time's, is additive in intervals (a body waits for both; on
  `coasting_none` `suspension` is 0, so only the proper-time count runs).
- **N2, the domain of the pace (M1).** The pace `p c^2 / E` holds while
  `abs(p)_1 <= Q S M`; above it the drive's `at_most = 1` with the step
  only at a self-creation gives one Link per self-creation, `1 / gamma`
  Links per interval, a pace that falls with p. The identity declares
  its domain `abs(p)_1 <= Q S M` (gamma at most 2 on a heading, beta at
  most 0.866): refused at load, and a push under the key that would
  carry `abs(p)_1` beyond it stops the run with a diagnostic line naming
  the record. Both pinned worlds are inside: the muon at 12 856 is at
  0.970 of 13 248, `s_mz2` at 0.184 of `2^48`. The script's (C) at p = 40
  000 (beta 0.98) lies outside the domain and is a check of the
  comparison loop alone, not of the pace.
- **N3, the fixed count of comparisons (M3).** Three comparisons hold
  for a push of one unit of the grain; the general bound grows with the
  push (171 for a push of 100 at p = 40 000). The identity declares the
  push ceiling per interval at the grain, `abs(dp)_1 <= g`, refused at
  run time with a diagnostic line: then `(E / c^2) / g` moves by less than
  `sqrt 3` per interval, the floor by at most 2, and the count is at
  most 3 comparisons per interval, fixed work for fixed K. On the two
  pinned worlds the push is 0 at every interval (J4's bar is empty;
  `coasting_none`'s registered record carries no `pushed` line), so the
  count there is the two failing comparisons. A form with fixed work for
  larger pushes, one Euclidean division `by_drive(Xi - (E / c^2)^2, 2 E / c^2)` as
  Newton's first step before the bounded comparisons, is named as the
  option and not designed.
- **N4, the release's cadence (M6).** The release per self-creation
  times the cadence `m c^2 / E` gives `M n / d` rows per lattice
  interval at every speed, so the pin "1 at rest and gamma in motion"
  did not follow from M1 as written. The design chooses the release per
  lattice interval: `by_drive(acc_release, E / c^2 x n, Q S x d)` advances on
  the owed intervals too, and M1's list is amended for the release
  alone (the turn, the lamp, `become` and the drive's gain stay per
  self-creation, so a moving lamp emits per proper time and 17.3 (i)'s
  Doppler with gamma stands). The field of a body is then its own energy
  per lattice interval, which is M6's purpose (E15), and the pin of M6,
  19.5, row 44 and E15 stands: the probe reads 1 at rest and `gamma` in
  motion. The alternative, the release per self-creation with the pin 1
  at every speed, is rejected because it makes the identity add
  nothing to the equivalence principle beyond the law's; the run decides
  the hypothesis, not this choice.
- **N5, the load-time identity `3 h n = Q S d` (M7, S10).** The refusal
  refuses `coasting_none` (paid stars of quantum 1 at `Q S = 2^26`,
  which no turn rate the engine accepts satisfies), so pin (c) could not
  be run. The fix: under the key the check is a DIAGNOSTIC, one line at
  load naming each paid family off the identity and its gap; the refusal
  holds only where the world declares the exchange's accounting (a
  `books` entry under the key, E5's lamp world). "The books balance" is
  WITHDRAWN from M7 and from E5's pin until derived: the row's energy
  `96 h s / 55` is on the heading's c while Xi is on the pair `[1, 3]`
  (under the pair a row's energy in `E / c^2` units is `sqrt 3 h s`, not an
  integer), and at rest the emitter's `E / c^2` falls by about `Q S h s` per
  unit paid while the row carries `1.75 h s`, a gap no (h, n, d) closes.
  What stands of M7 is the content identity, `Xi` gaining `Q S (2 m +
  Q S dM) dM` on a change of content dM, exact. Pin (c) runs on the
  registered `coasting_none` under the diagnostic: `z = 0.369 +- 0.003`,
  whose centre by S11's own formula on the heading, `gamma (1 + v T_D /
  (Q S_1)) - 1`, is 0.3667, inside the interval by 0.0006 (the continuum's
  beta gives 0.3691; both are inside).
- **N6, the J4 world's shape (M9).** The ticks 391, 367 and 345 were
  derived for a face at x = 200 while the bar was declared `[220, 1,
  1]` (a face at 220 gives 425, 403 and 380). The shape is `[201, 1, 1]`
  with the +x face at x = 200, fixed above; the ticks stand, re-derived
  with the drive's whole steps (the decay at x = 27 and 72, not 27.6 and
  72.1): 390.6, 368.2 and 345.2, inside the two-tick tolerance. The world
  file also declares the muon's `directions` line, `[[1, 0, 0]]` alone,
  so that the electron product leaves toward the +x face at rest too,
  and its family table in full (the muon's content, quantum, charge and
  `become` products; the electron's; the catalog has no muon).

The should-fixes carried: the identity's drive is form B's ONE primitive
with the wall's second term `abs(p)_1 T_D` keyed off, not a second copy
(M8); the pace is exact in the mean with two bounded remainders (M1,
above); and the build's obligation (S8's test 5 stated in full): a
dedicated test loads every registered world with the key absent and
asserts that no record carries `E / c^2`, `Xi`, the grain, `acc_tau`, the sum
of N1 or a second owed count, that `state.json`, `run.json` and the
`step` line have no new field, that `read_arrivals` reads no neighbour,
and that the drive's wall carries form B's cap term; the OFF baseline is
form B's register of its 47 moving-body worlds, not `main`'s. Rows 38 and
44 of 21.2 and E5 of 21.4 carry the amendment.


### 17.7 The proper-time gate without a root: two counters compared, against the whole root (the owner's word, 2026-09-22, records 642 and 647)

**The question.** covariant-readings-v1 gates a body's self-creations by
the whole root `E' = isqrt(W)` of its exact square `W = m^2 + 3` **p**
`.` **p** (17.6 M3; m = Q S M the rest energy in the identity's units,
**p** the momentum label, `c^2 = 1 / 3`), and the physics-rule reviewer's
vector verdict is that a whole root of the state's quadratic form at run
time is not a form at most bilinear in the state (record 202). The owner
names a gate with no root: two counters since a reset, t the intervals
and n the self-creations, and the n-th self-creation allowed when `t^2
m^2 >= n^2 W`, a comparison of two integer products (verbs 1, 2 and 6),
the physics the same, `t / n >= sqrt(W) / m = gamma`. This section
derives what the counters give against the whole-root gate, exactly, on
the domain `abs(p)_1 <= m` (`gamma <= 2`), with the enumeration
[root_free_gate.py](designs/covariant_readings/root_free_gate.py) (its
output [root_free_gate.out](designs/covariant_readings/root_free_gate.out);
integers only, no root and no float anywhere; a check, not a run).

**The whole-root gate's closed form.** From an empty proper-time
accumulator and the first self-creation at tick 1, the body owes
`by_drive(acc_tau, E' - m, m)` intervals after every self-creation with
the remainder kept (17.6 M1), so the n-th self-creation falls at

    T_n = n + floor((n - 1) (E' - m) / m) = 1 + floor((n - 1) E' / m),

the form 18.1 (a) uses (`T_64 = 70` and `124` for the muon). Equivalently
`T_n = min {t : t m > (n - 1) E'}`.

**Two root-free gates on the counters.** (A) The owner's, as stated: the
n-th self-creation at the first tick t (the first interval after the
reset is t = 1) with `t^2 m^2 >= n^2 W`, i.e. `T'_n = ceil(n sqrt(W) /
m)`. (B) The same comparison at the whole-root gate's origin, strict:
the n-th at the first t with `t^2 m^2 > (n - 1)^2 W`, i.e. `T''_n = 1 +
floor((n - 1) sqrt(W) / m)`. Both are comparisons of integers; `sqrt(W)`
is never formed, it only names the value the comparison decides.

**(1) Exactness.** For (B): `T''_n = T_n` unless a multiple of m lies in
the half-open interval `((n - 1) E', (n - 1) sqrt(W)]`, whose length
`(n - 1) (sqrt(W) - E')` is below `n - 1`; so for `n <= m + 1` the
interval holds at most one multiple of m and `T''_n - T_n` is 0 or 1,
never negative (`E' <= sqrt(W)`); in general `0 <= T''_n - T_n <= ceil((n
- 1) / m)`. Equality for every n when W is a perfect square (**p** = 0;
`gamma = 2` exactly, `W = 4 m^2`, where both give `T_n = 2 n - 1`), and
for every n with `(n - 1) (sqrt(W) - E') < m - ((n - 1) E' mod m)`. For
(A): `T'_n - T_n = ceil(n gamma) - 1 - floor((n - 1) E' / m)`, which is 0
at **p** = 0, exactly 1 at `gamma = 2`, never negative, and at most 3 on
the domain (the enumeration: 3 is attained, at m = 16, 64, 100 and 128
alike, for n near m); (A) is later than the whole root at almost every
W (identical for 1 value of W in 2359 at m = 64, the rest case) because
its first self-creation waits `ceil(gamma)` intervals where the
whole-root gate fires at tick 1 and owes afterwards. The bound, as an
integer: (B) 1 for `n <= m + 1`; (A) 3 on the domain. An exact root-free
form exists with one division: `T_n = min {t : c^2 > W, c = ceil(t m /
(n - 1))}` for `n >= 2` (`t m > (n - 1) E'` if and only if `ceil(t m / (n -
1)) > sqrt(W)`, E' being the largest integer below `sqrt(W)`), verbs 6, 2
and 6, no root; it reproduces every tick of the whole-root gate, but it
keeps t and n growing like (B).

**(2) The counters' bound and the reset.** The structural fact first,
the section's theorem: every accumulator of the law is bounded because
its slope is a rational of declared integers, a rate over a wall, and
its residue lives below the wall; a slope that is irrational, here
`sqrt(W) / m`, has no bounded exact accumulator, so a bounded state
costs a declared rounding of the slope, and two are on offer: the whole
root `E' / m` (the identity's M3, the comparison walk, the state
bounded, the period reset below for `m <= 2^15`) or a rational grain
`m / g` small enough for the run, which coarsens the gate's resolution.
The counters of (A) and (B) grow with the
run: `t^2 m^2 <= 2^63 - 1` holds up to `t = floor(sqrt(2^63 - 1) / m)`,
i.e. 229 242 intervals for the muon's `m = 13 248`, 47 453 132 for `m =
64`, 2 896 for `m = 2^20` and 181 for `m = 2^24`; and `n^2 W <= 2^63 - 1`
at `gamma = 2` up to `n = 114 621`, 23 726 566, 1 448 and 90
self-creations respectively. The registered covariant worlds run 420
ticks (`j4_muon_3640`, `j4_muon_12856`), so the muon's products stay
below `2^49` with no reset; a general body at `m = 2^24` overflows the
working bound within 181 intervals and needs one. A reset of (t, n) to
(0, 0) at a self-creation with nothing carried moves the ticks: the next
self-creation would fall at `floor(gamma) + 1 = 2` intervals for every `1
< gamma < 2`, a rate 1 / 2 in place of `1 / gamma`; and the residue `t^2
m^2 - n^2 W` is not a state that can be carried, since after the reset
the comparison needs the old counters themselves (the cross terms `2 T
t' m^2 - 2 n n' W`) and the residue grows like `2 t m^2`. The reset that
moves no tick is the sequence's own period: the whole-root gate is
periodic in n with period m and shift E', `T_(n + m) = T_n + E'` (the
floor's identity; checked on the muon for every `n <= m + 1` at both
momenta), so after m self-creations the counters may drop by (E', m)
with E' read as the elapsed ticks, no root computed; that reset comes
after `m gamma` intervals, within the working bound for `m <= 2^15`
(`4 m^4 <= 2^63`) and not beyond. Gate (B) has no exact period (its
shift per m self-creations is `sqrt(W)`, not an integer), so it has no
tick-preserving reset at all: its exactness within 1 holds only while
the counters run unreset, `n <= m + 1`.

**(3) Series S under the root-free gates**, from the tables, no run
(`m = 13 248`, `c^2 = [1, 3]`; the whole-root values are 18.1 (a)'s, the
register's pins, the beta product's flight to the +x face as run: 328,
299 and 221 intervals): at `p = 3640` (`W = 215 258 304`, `E' = 14 671`)
the 64th self-creation is 70 under the whole root and under (B), 71 under
(A); the beta click 369 (the run's 369, the pin 367 +- 2) under (B), about
370 under (A) (the muon gains under one Link in the extra interval), outside
the pin. At `p = 12 856` (`W = 671 339 712`, `E' = 25 910`): 124 under the
whole root and (B), 126 under (A); the click 345 (the run's 345, the pin
345 +- 2) under (B), 346 to 347 under (A), inside the pin by its bracket.
At rest all three give 64 and the click 392. So (B) reproduces both of
series S's decay ticks and both clicks exactly; (A) misses the integer
pins 70 and 124 by 1 and 2. Note 18.1 (a)'s continuum values `64 gamma
= 70.9` and `125.2`: (A) is the gate that rounds them up (71, 126), the
whole root and (B) the gate that starts at tick 1 (70, 124); the
register's pins are the latter's.

**(4) The three tests**, for the gate as a rule of the law. Generic: one
primitive for every body, the record's own integers m and W (the
identity's M3), no family name, the counters two more integers of the
record. Vector: with the two products kept as accumulators, `A <- A + (2
t + 1) m^2` per interval and `B <- B + (2 n - 1) W` per self-creation,
the rates are bilinear in the state (`t` with `m^2`, `n` with `W`), the
gate one comparison `A > B` (verbs 1, 2 and 6), no root and no float:
the physics-rule reviewer's PASS (2026-09-22) on the condition that
`m^2` and `W` are record integers formed by verb 2, the rates then
bilinear and the gate one comparison;
stated as `t^2 m^2` against `n^2 W` the products are degree four in the
record's integers, the same admission as the comparisons of 17.6 M3 and
M7 and the frame's `(p . D)^2 abs(D')^2`, which the reviewer must rule
on once for all three. Local: the record's own four integers, nothing at
a Node, the fixed work one multiplication, one addition and one
comparison per interval and one multiplication per self-creation; the
storage bounded only on the declared domain of (2), since gate (B) has
no exact period and no tick-preserving reset.

**The word.** For the owner's gate as stated (A): NOT the same ticks,
EQUIVALENT WITHIN 3 on the domain, later and never earlier, and outside
series S's decay pins (71 and 126 for 70 and 124). For the same
comparison at the whole-root gate's origin and strict (B): EQUIVALENT
WITHIN 1 for `n <= m + 1`, exact on both of series S's worlds and
whenever W is a perfect square, with no tick-preserving reset. EXACT
only with the division form `ceil(t m / (n - 1))^2 > W`, or with the
whole root itself; the difference between (B) and the whole root is the
root's own rounding (`E' = floor(sqrt W)`), which (B) removes: (B) is the
gate nearer to `gamma`, the whole root the one the register pinned.
The physics-rule reviewer's recommendation to the owner (his, recorded
here, not this section's): the whole-root gate with its rounding
declared per frame fits the law's shape; (B) stands as the proof that
the root's rounding is the only price, exact within 1 and on series S
exact.

## 18. The three structural failures of the register under one logic

**The question** (the owner, records 264 and 265, translated: "explain
whether there is a generic solution to this from the vector groups, or
maybe c enters here; you said you have problems with the masses and
with the self clock; see that it closes too with the same logic"; "do
all three settle things generically and truly to our structure?"). The
failures are NATURE.md's rows 4a, 4b and 5b (the clock in motion), 8a
and 8b (the weak forms) and 7b (the strong ratio), with the masses
beside them. The logic is one: every rule of a body is a reading of the
linear block, and a failure closes when a covariant reading exists
within the six verbs, passes the three tests, and the register's number
follows from it; it stays open when the reading needs what the six do
not have. The host script
[decay_click.py](designs/derivations_beam/decay_click.py) with its
output [decay_click.out](designs/derivations_beam/decay_click.out)
makes the numbers of 18.2; no run.

### 18.1 The clock in motion (rows 4a, 4b, 5b): closed on paper by section 17

Section 17.3 named the four covariant readings within the six verbs:
the count per turn, the push as the gradient of the age moment across
the six Ports, the energy as an accumulator of the work with the drive
`v = p c^2 / E`, and the turn per proper time `E_0 / E`; no root, no
family name, the record and its six neighbours. Under them the three
rows close: 4a, the muon of J4 fires its 64th turn at 70.9 and 125.2 at
0.43 c and 0.86 c (nature's `gamma`, lorentz-v1's 71 and 126 by the
root; the law as declared 64); 4b, `s_mz2` at `beta = 0.2674` reads `1 +
z = gamma (1 + beta)`, `z = 0.315` (the register's 0.2636 as declared,
the count per interval); 5b, the two arms of a moving laboratory read
the same round trip, since under the gradient push the bond contracts
by `1 / gamma` along the motion (Lorentz's 1904 argument on Heaviside's
field) and the clock slows by `gamma` both ways, where the flux push
gives `gamma^2` along and `gamma` across (12.3: 1.375 and 1.140 at
0.4297 on the register's table; `beta^2 / 2 = 5 x 10^-9` at the Earth's
orbital speed). **What a run must show**: the muon's 64th turn at 71 and
125 (the tolerance one tick); the pair in motion of 12.4 with the same
round trip along and across (the ratio 1 within the grain, against
1.375 / 1.140); `coasting_none`'s `s_mz2` at `z = 0.315 +- 0.003`. Two
things stay as they were and belong to the same logic: route C stays
closed (12c: the crossing count through an isotropic crowd is the rest
count exactly, so nothing of the clock's slowing comes from the crowd),
and the cube's 48 carry no boost (record 231: a boost mixes a space
step with a time step and is not among the signed permutations of the
axes), so the symmetry is the LIMIT's, the wave equation's, and c enters
the bodies through the drive `v = p c^2 / E` and nowhere else. **Closed
on paper**, as `covariant-readings-v1`, which the owner decided (record
270) is built beside the law in place of lorentz-v1; the run decides.

**Amended per the review (record 297; 17.6).** The pins of this
subsection are restated on the declared integers and as detector
readings: (a) the muon of J4 on the world file 17.6's M9 declares, `p =
3640` and `12 856` label units at `c^2 = [1, 3]`: the decay (`become` at
64 turns) at the interval the primitive gives, from an empty
proper-time accumulator and the body's first self-creation at tick 1
(M1: after every self-creation the body owes `by_drive(acc_tau, E /
c^2 - m, m)` intervals, so the k-th self-creation falls at the interval
`k + floor((k - 1) (E / c^2 - m) / m)`),

    t_64 = 64 + floor(63 (E / c^2 - m) / m):   64 at rest,   70 at p = 3640 (E / c^2 = 14 671, 63 x 1423 / 13 248 = 6.77),   124 at p = 12 856 (E / c^2 = 25 910, 63 x 12 662 / 13 248 = 60.21),

the integers the register row carries (the build of PR #582 reads 70
and 124; the continuum's `64 gamma = 70.9` and `125.2` lie one `(gamma -
1)` above the count from an empty accumulator, the physics-rule
review's S1); the electron product's click on the +x face at tick 391,
367 and 345 within two ticks (the run read 392, 369 and 345), the
decay's tick no longer a real-valued pin; (b) the pair's round trips: WITHDRAWN from this identity
(M4: the magnetic part of the push is not a local reading; M5: 12.4's
one-Link pair cannot contract), so 5b stays the law's FAIL beside the
identity until `source-velocity-v1`; (c) `coasting_none`'s `s_mz2` at its
declared momentum: `z = 0.369 +- 0.003` (0.315 only on a re-declared
momentum, 45 097 270 682 765); (d) S5's consequence, 12c.6's probe under
the identity (`m = 64`): at `p = 10` the pace `p c^2 / E = 0.1515` Link
per interval (the law's form B 0.1232), gamma 1.031, the counts per
self-creation outward 0.763 and inward 1.300 of the rest count (the
law's 0.788 and 1.212); at `p = 28` the pace 0.350 (0.250), gamma 1.250,
outward 0.498 and inward 2.002 (0.571 and 1.429). "Closed on paper"
above now reads: the clock, the Doppler and the energy close under the
amended identity; the contraction does not.

### 18.2 The weak forms (rows 8a, 8b): what the click can and cannot give

**The failures.** J1's decay at a fixed lifetime L gives every neutron
the same tick, a step: the 10th-to-90th width over the median 0.036
against the memoryless 3.17. J2's passage by a phase window gives a
filter: the rows in the window are absorbed by the first reader (16 of
1024), the rest pass every reader, and the 127 readers behind read 0
where nature's second detector reads the first's count. Both come from
deterministic rules read once: a lifetime, a residue.

**The click as the mechanism.** The one non-bijective read of the law is
the click: one threshold `[u < b_k]` of the record's wheel u against a
rung of the crowd's cumulative weights (6.2, 6.5). Read as the decay's
mechanism at a rate, it is "at every self-creation compare the body's u
with the rung b of the rate `p = b / W`, and `become` at the first
success"; read as the passage per Node of depth, "at every Node compare
the row's u with the rung of the absorption". As rules both pass the
three tests by construction: no family name (one rung, one comparison),
one verb (D, the comparison; T for the wheel), local (the record and
its Node). The question is the number: whether the survival is
memoryless. The answer splits on WHAT u is compared with.

**(i) Against the body's own record: bounded, never memoryless.** If the
rung is fixed and u advances on the record (the golden wheel `u_n = u_0
+ n r mod W`, record 155, or the bit-reversed wheel of record 156), the
decay time is the first passage of a rotation into an interval of
length p, and by the three-distance theorem a rotation's return times
into an interval of length p are bounded by about `1 / p`: every body
decays before a hard maximum, and the survival is a ramp, not an
exponential. The script (B), over all 4096 birth phases at `p = 1 / 64`:
the 10th, 50th and 90th percentiles 7, 33, 77 with the maximum 89, the
width over the median 2.12 against the geometric law's 7, 45, 147 and
3.11 (3.17 in the limit of small p); at `p = 1 / 1024` the ratio is 1.60
against 3.17; the bit-reversed wheel 1.55 (C). The same holds for the
passage: with u advanced per Link the count behind n Nodes falls as
0.984, 0.844, 0.000 at n = 1, 10, 100 against `(1 - p)^n` = 0.984,
0.854, 0.207 (D), a ramp to zero at the depth `1 / p`; with u fixed per
row it is J2's filter, all or nothing. **The theorem behind it**: every
count on the body's own record is a deterministic sequence of bounded
discrepancy (a rotation, a bit reversal, a counter), so its first
passage into any interval is bounded, and a memoryless survival, whose
maximum is unbounded and whose width over the median is 3.17, cannot
come from the record alone, at any W and any rate. **Refuted** for the
record.

**(ii) Against the crowd: memoryless if and only if the crowd mixes.**
If the rung is the crowd's, the cumulative Gram weight of the rows
arriving at the body's Node in that interval (6.5's ladder, read per
interval), the comparison is fresh at every interval exactly as fresh as
the crowd's phases are: the survival is memoryless in the limit where
the arriving rows' weights decorrelate from one interval to the next,
which is a property of the WORLD (many sources, many directions, the
ages mixing on the circle `Z_N`), not of the rule, and cannot be proved
on paper for a given world; it can be pinned. Then the decay's rate is
`p = b / T` with T the crowd's total weight, the survival `(1 - p)^n`,
the width over the median 3.17 in the limit, and the passage per Node
`(1 - p)^n` with p the reader's absorption, nature's "about 1" for a
small p (0.984 at `p = 1 / 64` behind one reader, 15.75 of 16). The
price, stated: in an empty world there is no crowd, no weight and no
click, so a body in J4's bar would never decay (or, with the lifetime L
kept as the wall, decay at L exactly as today): the memoryless decay of
this reading needs a background crowd everywhere, the same need as
route C's (12c.5) and section 15.5's steady presence under the growing
wall, and the decay's rate then reads the background (a decay slower
where the crowd is thinner: a prediction, and a departure from nature's
constancy of the lifetime unless the background is the same
everywhere). **Named**, as one hypothesis, `decay-by-crowd-v1`: the
`become` trigger as the click of the body's u against the crowd's rung
at the rate, and the absorption of a row at a reader as the click of its
u against the reader's rung; passes the three tests; not built.

**Addendum: the background crowd named, and the beam-and-bottle pin**
(the owner, record 271, translated: "what do you mean that a
background crowd is needed? maybe that solves everything; what is this
background crowd you need?"; the host script
[crowd_decay.py](designs/derivations_beam/crowd_decay.py) with its
output [crowd_decay.out](designs/derivations_beam/crowd_decay.out)).

*What the crowd is.* Nothing new: the field rows every body already
emits under the coupling, the free family's rows of sections 3 and 5
whose presence and flow the push reads, plus light and any passed
family's rows, reaching every Node within the horizon. Its density at a
Node is the sum over the sources of `M / r^2` (3.2's shell mean, `q
dwell / (4 pi r^2)` per source), so the nearest large mass dominates:
in the law's universe the crowd at a body on the Earth is the Earth's
rows (`M / r^2 = 1.5 x 10^11` kg per m^2 in the units of the script's
(A)), the Sun's `6 x 10^-4` of that, a laboratory's own matter `7 x
10^-9`, and the cosmic background, the sum over every source to the
Hubble length under the growing wall (15.5: `4 pi rho R_H`, saturating
at the Hubble length), `10^-10`. So the crowd is uniform on a
detector's scale (the Earth's rows change by `2 h / R` over a height h,
`3 x 10^-7` per metre) and never absent inside a galaxy; it is absent
only in the law's empty worlds. Does it mix? A sum of many sources
with ages differing by more than the circle's period `N` intervals
brings phases from every residue of `Z_N`, and the arriving rows' Gram
weight at a Node changes from interval to interval by the rows that
arrive and leave: the Earth's rows alone come from `10^51` units on
`290` directions at every age, so the mixing condition of (ii) is met
wherever a crowd is; it is the empty world that fails it.

*The prediction the hypothesis cannot avoid, and its pin.* As written
in (ii), with the rung the crowd's total weight T, the decay rate is `p
= b / T` and FOLLOWS the local crowd: a lifetime measured where the
crowd differs differs, in proportion. Nature's neutron lifetime in a
beam is `887.7 +- 2.2` s (Yue et al. 2013, Phys. Rev. Lett. 111, 222501)
and in a bottle `877.75 +- 0.36` s (UCNtau, Gonzalez et al. 2021, Phys.
Rev. Lett. 127, 162501), a difference of 10.0 s, 1.13 % of the
lifetime, 4.5 standard deviations (a ratio, rule (b)). To reproduce it
the hypothesis needs the beam's crowd 1.12 % thinner than the bottle's;
the two apparatus differ by their own matter, `7 x 10^-9` of the
Earth's crowd: the hypothesis CANNOT reproduce the beam-and-bottle
difference (it predicts the two equal to a part in `10^8`), and it is
not refuted by it either, since the Earth's crowd is the same for
both. What refutes the rate-from-the-crowd reading is the lifetime OFF
the Earth (the script's (C)): the rate in proportion to `M / r^2` gives
a neutron's lifetime 6 times the Earth's on the Moon, 1.3 times at 500
km above Venus against MESSENGER's `780 +- 60 +- 70` s there (Wilson et
al. 2020, Phys. Rev. Research 2, 023316, within 15 % of the Earth's
value), 1700 times in interplanetary space at 1 au, and `4 x 10^7`
times at Voyager 1, whose plutonium-238 has decayed at its 87.7-year
half-life for 45 years (the RTGs' output, NASA JPL's Voyager mission
status): **refuted** for the rate as the crowd's weight. **The
correction of (ii)**: the crowd may supply only the FRESHNESS of the
comparison, not the rate: the body's wheel u advanced each interval by
the arriving rows' phase sum (a reading of the crowd, T on the record
with a rate read from the rows, bilinear, local), and the rung the
family's own `b / W` (the declared rate, as J1's L is declared today).
Then the rate is constant wherever any crowd mixes (the Sun's rows
suffice at Voyager, `3 x 10^3` kg per m^2), the survival is memoryless
as far as the phase sum mixes, the beam-and-bottle difference is not
predicted (it stays nature's open anomaly, as it is in the standard
model), and the hypothesis fails only in an empty world. `decay-by-
crowd-v1` is restated in that form; the pins below hold with (4) read
accordingly.

**The pins a run would have to meet** (before any run): (1) J1's neutrons
in a crowd world (the source's fan on, the crowd mixing): the 64 beta
clicks' width over the median within 0.5 of 3.17, the maximum decay
time beyond `3 / p`, no two clicks at one tick more often than the
geometric law's; (2) the same world with the crowd off: every click at
L (today's register, 0.036); (3) J2 with the readers reading the
crowd's rung at `p = 1 / 64`: the second reader's count `16 x 63 / 64
= 15.75` (16 or 15 in integers) and the n-th `16 (1 - p)^(n - 1)`, 12.9
at the 15th; (4) what refutes the hypothesis: a bounded maximum in (1),
a ramp in (3), or a rate that follows the crowd's weight (the addendum: the rate is the family's, the crowd supplies the freshness).

### 18.3 The strong ratio (row 7b): the give per contact pair, in form and in number

**The failure.** The give of binding-v1 is once per body (`units = held
// h`, the remainder kept, section 1.3's table), so the escaped content
of a bound set is linear in its bodies: the alpha's four `bond` clicks
release 8 against the deuteron's 4, the ratio 2.0 where nature's binding
energies give `28.296 / 2.2246 = 12.72`.

**The give per contact pair.** The set's geometry on the six Ports: the
cubic lattice is bipartite (a Link joins Nodes of opposite parity), so it
has no triangle and no tetrahedron; four bodies at adjacent Nodes form
at most a square (a 4-cycle, 4 contact Links), a line or an L (3), never
6 mutual contacts. A give per contact Link (a count over the Ports, the
comparison verb, local, no family name: it passes the three tests)
gives the deuteron 1, the three-body line or L 2, the alpha's square 4:
the ratio 4.0 against 12.72, and for the tritium and helium-3 2.0
against nature's 3.81 and 3.47. Counting the square's two diagonals as
second-neighbour contacts at the same give raises the alpha to 6.0;
at a weaker give, between 4 and 6. **Reached in form, short in number**:
the pair count gives 1 : 2 : 4 (or 6) where nature gives 1 : 3.8 : 12.7,
and the remainder, a factor of 2 to 3 on the alpha, is not a count of
contacts on any lattice geometry: it needs the quark substructure (the
nucleon as a bound set of three, the quarks design, record 251), where
the alpha's give counts contacts between quarks across nucleons. The
pins: the alpha on the square 4 clicks of the pair give, the ratio 4.0;
the alpha on a line 3 and 3.0; the tritium 2.0.

### 18.4 The masses

The honest sentence of 16.2 (d): the law fixes floors and no counts. One
unit is the least mass (the integer form), a charged family's floor is
the reduced denominator of its charge per unit of content (1 for the
electron and the proton, 3 for the up and down quarks), and every mass
ratio is a rational number of the family table; the counts (the
electron at least 4526 units, the nucleons multiples of 3 if the binding
holds no content) are inputs, and no logic of the six verbs selects
them (PREDICTIONS 26: a linear law is scale-free in its coefficients).
**Open**, and stated as open: the same logic closes nothing here, and
what would close it is a nonlinear closure on the amounts (binding-v1's
content in flight, the quarks design), named and not built.

### 18.5 The verdict per failure

| the failure | the logic | the verdict |
| --- | --- | --- |
| the clock in motion (4a, 4b, 5b) | the four covariant readings of section 17, one hypothesis `covariant-readings-v1` | **closes on paper**: 70.9 and 125.2, `z = 0.315`, the arms equal; route C closed, the 48 carry no boost, c enters through `v = p c^2 / E` |
| the weak forms (8a, 8b) | the click as the decay and the passage | **half**: against the body's own record it is refuted (bounded first passage, the width over the median 2.1 and 1.6 against 3.17, a ramp against the exponential); against the crowd's rung it is memoryless exactly as far as the crowd mixes, named `decay-by-crowd-v1`, needing a background crowd everywhere, pinned |
| the strong ratio (7b) | the give per contact pair on the six Ports | **in form, not in number**: 4.0 (6.0 with the diagonals) against 12.72; the rest the quarks' |
| the masses | none within the six | **open**: the floors 1 and 3 fixed, the counts inputs |

So: one closes under a logic already in the law, one splits (the
record cannot, the crowd can), one closes in form and stays short by a
factor the lattice's geometry cannot supply, and one stays open; nothing
claimed beyond that, and every closure is a hypothesis with its pins,
not a build.

### 18.6 Series O, two stars each the detector of the other, under covariant-readings-v1: the expected readings pinned before any run

**The order** (the owner through the G2 session, record 344: "pass it
to the Boss with a request for lorentz-v1 on this experiment"; record
270 builds `covariant-readings-v1` in place of lorentz-v1, so the test
is under that identity). The worlds are series O's
(`examples/events/two_stars`, PR #517; the design
`docs/designs/two_stars/DESIGN.md`): a bar of 201 x 3 x 3, star A
(`s_px1`) at x = 70 and star B (`s_mx1`) at x = 130, each a mass `2^22`
with a lamp of one unit per self-creation on both headings, each
measuring the other's light with `reads: age`, two fixed lab detectors
at x = 5 and x = 195 reading the outward light; `symmetric` (the stars
at `+-0.2 c_h` under the law's drive, gravity on), `rest_frame` (A at
`+0.4 c_h` onto B at rest), `symmetric_pass` (gravity off), 500
intervals, the windows [50, 150) and [150, 250); the momenta declared
for the law's drive `v = p / (Q S M + p)`, `Q S M = 2^48.003` (M = `2^22
+ 2^13`). The identity's rules used are 17.6's as amended: M1 (a body's
self-creations one per `gamma = E / (m c^2)` intervals; the drive's rate
per self-creation Newton's, so the pace per interval `p c^2 / E`), N1
(the crossing count read per interval and charged per self-creation),
N2 (the domain `abs(p)_1 <= Q S M`: both momenta inside, at 0.13 and
0.30 of it), N4 (the lamp's count per self-creation: a moving lamp
emits per proper time), M3 (`c^2 = [1, 3]`; the rows on a heading at
`c_h = 32 / 55`). The host script
[series_o_identity.py](designs/derivations_beam/series_o_identity.py)
with its output
[series_o_identity.out](designs/derivations_beam/series_o_identity.out)
makes every number below from the world files, exact rationals; no run.

**(a) The pace of the declared momenta changes under the identity.**
`p c^2 / E` against the law's `p / (Q S M + p)`: the symmetric stars at
0.1284 Links per interval (0.2207 `c_h`, `gamma = 1.02568`) in place of
0.1164 (0.2 `c_h`); the mover of `rest_frame` at 0.2685 (0.4615 `c_h`,
`gamma = 1.1296`) in place of 0.2327 (0.4 `c_h`). The pins below are on
the registered momenta (M2's rule); the momenta that would keep 0.2 and
0.4 `c_h` under the identity are 33 504 989 557 488 and 71 719 693 608
158 (`p = Q S M v / sqrt(1 - 3 v^2)`), for a re-declared world.

**(b) The clock question, in the form's own words.** The click's tick
belongs to the lattice interval: the click is read per interval (N1)
and its record carries the engine's tick. The reader's own clock is its
age, which advances once per self-creation, one per `gamma_r` intervals
(M1). The record's reading tool (DESIGN section 6: `1 + z` from the
slope of the birth ordinal against the click's tick, the lamp's rate
one birth per interval) therefore reads in lattice time and assumes the
declared rate; with `v_s` the source's speed toward the reader (negative
when receding) and `v_r` the reader's toward the source, a moving lamp's
units are `(c_h - v_s) gamma_s` Links apart (one per `gamma_s`
intervals, N4) and the reader meets `(c_h + v_r) / ((c_h - v_s)
gamma_s)` of them per interval, so

    the tool reads   1 + z = (c_h - v_s) gamma_s / (c_h + v_r),          the lamp's proper emission shows, the reader's proper time does not;
    per the reader's own clock   1 + z = (c_h - v_s) gamma_s / ((c_h + v_r) gamma_r),   the slope against the reader's AGE in place of the tick,

the second being the identity's Doppler (17.3 (i)), nature's `sqrt((1 -
beta) / (1 + beta))` up to the grain between `c_h` and `1 / sqrt 3` (0.8
percent in v; 0.606 against 0.608 below). Both are pinned; the tool as
written returns the first, and the second needs the reader's age from
its own record beside the click line.

**(c) The table**, at the declared momenta and the identity's pace,
constant speeds (the control's; the gravity worlds at their start), the
law as built beside (DESIGN section 3 at the declared momenta; measured
in section 7, the second window, in brackets):

| World | the reading | the identity, the tool | the identity, the reader's own clock | nature at the identity's speeds | the law as built (measured) |
| --- | --- | --- | --- | --- | --- |
| `symmetric_pass` | A reads B | 0.6548 | 0.6384 | 0.6384 | 0.6667 (0.6672) |
| | B reads A | 0.6548 | 0.6384 | 0.6384 | 0.6667 (0.6670) |
| | the left lab reads A (receding) | 1.2520 | 1.2520 | 1.2515 | 1.2000 (1.2046) |
| | the right lab reads B (receding) | 1.2520 | 1.2520 | 1.2515 | 1.2000 (1.1998) |
| `rest_frame` | A, the mover, reads B | 0.6842 | 0.6057 | 0.6070 | 0.7143 (0.7090) |
| | B, at rest, reads A | 0.6083 | 0.6083 | 0.6070 | 0.6000 (0.5929) |
| | the left lab reads A (receding) | 1.6509 | 1.6509 | 1.6475 | 1.4000 (1.4015) |
| | the right lab reads B (at rest) | 1.0000 | 1.0000 | 1.0000 | 1.0000 (1.0000) |
| `symmetric` | as the control at the start | 0.6548 | 0.6384 | 0.6384 | 0.6497, 0.6329 (0.6517) |

In the symmetric frame the readings per the stars' own clocks are `(c_h
- v) / (c_h + v)` exactly, the law's own form at the identity's speeds:
the frame hides the identity in the proper readings (DESIGN section 3's
identity again) and shows it in the tool's by the lamp's `gamma_s`,
0.655 against 0.638. In the rest frame the two outsiders read alike per
their own clocks (0.606 and 0.608, nature's 0.607) where the law reads
0.714 against 0.600: the lattice's frame is no longer visible in the
mutual readings; the tool still tells them apart (0.684 against 0.608)
because it reads the mover in lattice time. The labs carry the lamp's
`gamma` (1.252 and 1.651 against the law's 1.200 and 1.400). Under
gravity (`symmetric`, `rest_frame`) the identity's push is `-grad(A)`
(M4), whose effect on an approaching pair is not derived here; the law's
own gravity moved the mutual reading by 2 percent between the windows
(0.665 to 0.652, section 7), the size of the correction to expect.

**(d) The first contacts** (no gravity; the first interval t with
`floor(t v_A) + floor(t v_B) >= 60`, the pace in the mean with the two
remainders of M1): `symmetric_pass` at 234 +- 2 under the identity (the
law's 258, measured 258); `rest_frame` at 224 +- 2 without gravity (the
law's 258 without it, measured 254 with it); `symmetric` at 234 less
the gravity's lead, which the law's run put at 7 intervals (258 to 251).

**(e) What refutes the identity on this run** (the grain of z 0.003 per
window; the brackets ten grains): (1) the control's mutual reading by
the tool outside 0.655 +- 0.01 (0.667 is the law's, four grains away);
(2) a lab's reading in the control outside 1.252 +- 0.01 (1.200 the
law's: the lamp's `gamma`, N4); (3) the control's contact outside 234 +-
2 (258 the law's: the pace `p c^2 / E`, M1); (4) in `rest_frame`, the two
stars' readings per their own clocks unlike by more than 0.01 (the
identity 0.606 and 0.608; the law 0.714 and 0.600), or the tool's
reading of the mover outside 0.684 +- 0.01. What refutes the law as
built is any of the identity's values read where the law's are pinned
(DESIGN section 4).

**(f) The G2 session's 0.7794 for the mover, corrected.** It is the
law's mover reading at the declared pace, 0.7143, times `gamma(0.4 c_h)
= 1.0911`: the factor on the wrong side. Under the identity the reader's
self-creations are fewer (one per `gamma_r` intervals), so its count per
self-creation is larger and `1 + z` per its own clock is the law's
reading OVER `gamma`: 0.6547 at the law's pace, and at the identity's own
pace of the declared momentum 0.606 (the tool 0.684). A mover reading
0.78 would refute the law and the identity both.

**(g) The law's expected readings, restated beside.** DESIGN section 3
at the declared momenta, no `gamma` anywhere: the mutual `(1 - v_s /
c_h) / (1 + v_r / c_h)`, 2 / 3 in the symmetric worlds, 0.714 and 0.600
in `rest_frame`; the labs `1 + v_s / c_h`, 1.200 and 1.400; the control's
contact 258. Section 7 measured 0.667 / 0.667, 0.709 / 0.593, 1.205 /
1.200 and 1.402 / 1.000 in the second windows and the contacts 258, 251,
254. Nothing enters the law; the identity stays a hypothesis, and this
run is its third pinned world beside J4's muon and `coasting_none`.

## 19. The masses generically: a bound set's mass as its total content, the nucleon as a chain of three on the bipartite lattice, from the electron to the quarks

**The owner's direction** (2026-09-21, in conversation, translated:
"solve the masses generically too: you reached the electron, and from
the electron perhaps the proton, and from the proton the quarks, and
close the whole family; and understand how the quarks bind, the
binding law, generically"). What the structure gives is stated as
derived, what it does not as input, with the numbers against nature
(PDG 2024, CODATA 2022) from the host script
[masses_chain.py](designs/derivations_beam/masses_chain.py) with its
output [masses_chain.out](designs/derivations_beam/masses_chain.out);
no run. The quarks' design (records 249, 251) is the physicist's and
is not on `main`; this section states what any design must satisfy
and what it may not expect.

### 19.1 The generic statement: the mass of a bound set is its total content

Under binding-v1's generic form ("the field is content in flight,
every family paid", its design's section 7) and section 17's energy
accumulator, the mass a detector reads of a bound set is the set's
TOTAL content: what its bodies hold plus what is in flight between
them, less what has escaped (the escape click's content, the released
binding). Three consequences, each a form and not a number:

- **The current and the constituent mass.** A body's held content at
  the moment of a reading is its current mass; its share of the
  content in flight is the rest of its constituent mass; the set's mass
  is the sum of both, and neither part is a rung of any ladder
  (PREDICTIONS 26 stands: nothing selects the held counts).
- **The bond's content in flight is blind to charge and to the held
  content.** The strong column reads `sigma` per unit with one sign for
  every family that carries it, never the charge line (3.4: the charge
  column is a separate column) and never the family's name; so in a
  steady exchange between three bodies the content in flight F is a
  property of the bond (the rate, the contacts, the round trip), the
  same for `u u d` and `u d d`.
- **The steady state.** With H the held content, `n / d` the strong
  family's release rate per unit per self-creation and tau the rows'
  round trip in intervals, the content in flight is `F = H (n / d) tau`
  (each unit released stays in flight tau intervals), so the fraction in
  flight is `(n / d) tau / (1 + (n / d) tau)`, a number of the family
  table and the geometry.

### 19.2 From the electron to the proton to the quarks: what closes and what stays input

**The electron to the proton.** Nothing generic: the electron's count k
is at least 4526 units (16.2 (a)) and the proton's `1836.15 k` is the
family table's (16.2 (d)); the sentence stands.

**The proton from the quarks: the bond's number.** With nature's
current masses (`m_u = 2.16`, `m_d = 4.70` MeV) the proton's held part
is `2 m_u + m_d = 9.02` MeV and its bond's content in flight `F = 938.27
- 9.02 = 929.25` MeV, 0.990 of the mass: the proton is one percent held
content and ninety-nine percent content in flight, exactly the
distribution record 248 named, and F is a number the family table's
`(n / d) tau = F / H = 103` must give (30 per self-creation at one
Link's round trip, `tau = 2 x 55 / 32`): **an input**, one number for
the whole bond.

**The neutron from the proton: a prediction with its number.** Since F
is the same for `u d d`, the neutron's mass is `m_u + 2 m_d + F` and
the difference is the held difference alone:

    m_n - m_p = m_d - m_u = 2.54 +- 0.41 MeV      (measured 1.293 MeV).

**Different by the electric part**: lattice QCD splits the measured
difference into 2.52 MeV from the quark masses and -1.00 MeV from the
proton's electric self-energy (Borsanyi et al., Science 347, 1452,
2015); the law's electric rows are free rows that carry no content
(section 3.4's column, 16.4), so the law as declared predicts the QCD
part alone, 2.54 against 1.29, and the electric part is exactly the
content in flight of a PAID electric family (binding-v1's "every
family paid"): a uniform sphere of the proton's charge radius holds `(3
/ 5) alpha hbar c / r_p = 1.03` MeV, and `2.54 - 1.03 = 1.51` against
1.29 (lattice QCD's 1.51 +- 0.28). So the neutron-proton difference
closes in form under two readings the law already names (the bond's
content in flight blind to charge; the electric column paid), with the
number at the quark masses' uncertainty; **reached in form, the number
within the inputs' uncertainty**, and it is a prediction: a design in
which the strong exchange read the charge would break it.

**The quarks' held counts** at `k = 4526`: `u` 19 131 +- 3543, `d` 41
629 +- 620 units, the bond `8.2 x 10^6` per nucleon; both compatible
with the floor 3 within the uncertainties, and nothing selects them.

### 19.3 How the quarks bind, generically: the chain on the bipartite lattice

**The binding law is the one the nucleons have.** Record 251: no new
force unless the mathematics forces it; the quarks bind through the
strong column `sigma` with their own value as the family key, one give
per contact Link (18.3), the lifetime L as the range. The mathematics
forces one thing, and it is geometry: the cubic lattice is BIPARTITE
(a Link joins a Node of even coordinate sum to one of odd), so it has no
triangle, and three bodies at adjacent Nodes cannot all touch: three
quarks form a CHAIN, a line or an L, with one quark at the centre bound
to both ends and the ends not bound to each other. Two consequences,
one of them a number:

- **Which quark sits at the centre is fixed by the charge radius.** The
  mean square charge radius of a chain of three at one Link about its
  charge centroid (the script's (B)): `u d u` (the d at the centre)
  `+4 / 3 L^2`, `u u d` (the d at an end) `-2 / 3 L^2`; the proton's is
  measured positive (`r_p^2 = 0.707` fm^2), so the proton is `u d u`,
  the odd quark at the centre. Then the neutron, by the same rule, is
  `d u d`, and its mean square charge radius is `-2 / 3 L^2`: NEGATIVE,
  as nature's is (`r_n^2 = -0.1155` fm^2, the neutron's charge
  distribution positive at the centre and negative outside). **The sign
  is a parameter-free consequence of the bipartite chain**; the
  magnitude is not: with L from the proton, `L = r_p sqrt(3 / 4) = 0.73`
  fm, the chain gives `-0.35` fm^2, three times nature's, the point
  charges at the chain's ends against nature's spread (the content in
  flight carries the charge along the rows, which a chain of point
  bodies does not read). **Reached in sign, short in magnitude by 3.**
- **The quarks design's three shapes** (QUARKS.md, "the shapes": the
  range L = 3 admits bonds up to three Links, so beside the line there
  are the corner, bonds 1, 1 and `sqrt 2`, and the equilateral triangle
  of the face-diagonal sublattice, mutual `sqrt 2`, whose stabiliser in
  the 48 is `S_3`). The charge radius decides between them (the script
  `periodic_images.py`, (C)): the line gives `+4 / 3` and `-2 / 3 L^2`
  for the proton and the neutron with the odd quark at the centre, the
  corner `+4 / 9` and `-2 / 9` (the same signs, the same ratio -1 / 2),
  the triangle 0 and 0 (a charged equilateral triangle has no second
  moment about its charge centroid). Nature's negative `r_n^2` therefore
  excludes the triangle and admits the line and the corner, both with
  the odd quark at the centre: a pin for the design.
- **The colour of the law is the parity.** The lattice's two classes of
  Nodes are the only "colour" a bond on the six Ports knows: a contact
  is always between the two classes, and a set of three has two of one
  class and one of the other, the centre. A third class does not exist
  on the lattice; a design that needs three colours needs a hypothesis
  outside the six Ports (record 251's "colour only as a stated
  hypothesis if sigma alone cannot hold three events at adjacent
  Nodes": on the cubic lattice sigma alone cannot hold three at
  MUTUALLY adjacent Nodes, since there are none, and holds them as a
  chain).
- **Confinement is not in the law.** The lifetime L gives the strong
  rows a range and the escape click releases their content; a quark
  moved beyond L Links from its partner loses the exchange and is a
  free body of its held content: the law has a range, not a
  confinement, and a free quark is admissible in it. **Absent**, stated.

### 19.4 The three tests and the verdict of section 19

The readings used pass the three tests as they stand: the bound set's
mass as its total content (a sum over the record and the rows, B and
T, no name), the strong column blind to charge (one primitive per
column), the chain (the six Ports, local). **Derived**: the mass of a
bound set as held plus in flight less escaped (form); the
neutron-proton difference as the held difference with the electric
part named (`2.54`, `1.51` with the paid electric column, against
1.29); the nucleon as a chain with the odd quark at the centre and the
neutron's negative charge radius squared (sign). **Input**: the
electron's count, the held counts of the quarks (the current masses),
the bond's content in flight (`(n / d) tau = 103`). **Absent**:
confinement; a third colour. **For the quarks physicist's design**,
the pins before any run: three bodies at adjacent Nodes bind as a
chain and never as a triangle; the read mass of the set is the held
sum plus the content in flight, the same F for `u u d` and `u d d`
within the grain; `m_n - m_p` equal to the held difference; the escape
click's content the released binding; and, if the electric family is
paid, the proton heavier than the strong reading by about one part in
a thousand of its mass (1.0 MeV of 938).

### 19.5 The rest of the masses, as readings after a detector

**The owner's direction** (2026-09-21, in conversation, translated:
"try to understand the rest of the masses and reach on your own the
masses measured in nature, which are of course measured after
detectors"). The host script
[rest_of_masses.py](designs/derivations_beam/rest_of_masses.py) with its
output [rest_of_masses.out](designs/derivations_beam/rest_of_masses.out)
makes the numbers (PDG 2024); no run.

**How a detector reads a mass in the law, and the one condition it
imposes.** A mass is never clicked; it is read four ways, and every
measured mass of nature is one of them: (a) the push a body's rows
exert on a reader, the source's release `content x n / d` rows per
direction (3.3: the active gravitational mass); (b) the momentum a
body needs per Link, the drive's wall `Q S M` or, under section 17,
`E / c^2` (the inertial mass); (c) the turn rate a click reads as `E =
h f` (the rest energy); (d) for a bound set, the total content, held
plus in flight less escaped (19.1). Nature's equivalence principle says
(a) and (b) agree for bound bodies too: the binding energy gravitates
(the Nordtvedt test by lunar laser ranging, `eta = (-3.0 +- 5.0) x
10^-4`, Hofmann and Muller 2018, Class. Quantum Grav. 35, 035015), so
the proton's field is its 938 MeV's, not its held 9. In the law as
declared the release reads the HELD content (a body releases; rows in
flight release nothing), so a bound set's (a) is one percent of its
(b) under section 17's drive: **the condition**, derived and pinned for
covariant-readings-v1 with binding-v1: a bound body's release must
read the set's energy accumulator E, not its held content (one rule,
the same `by_drive` with E in place of `content`: generic, vector,
local), or the equivalence principle fails for every bound body by the
binding fraction, 99 % for a nucleon against nature's `10^-4`.

**Amended per the review (record 297; 17.6's M6 and M7).** "E in place
of content" is restated with its units and its owner: the release's
rate reads the content-equivalent of the body's OWN energy, `E' / (Q
S)`, as one `by_drive(acc_release, E' x n, Q S x d)` with the remainder
kept; a body reads its own `E'` and never the set's (the chain's ends
are two Links apart), so this identity gives a bound body a field equal
to its own rest and kinetic energy and leaves the binding fraction, the
energy in flight between the bodies, to `field-source-v1` (21.4, E16):
the 99 percent of a nucleon is E16's number, not this identity's. The
pin is a reading of the law, not Nordtvedt's: a free body thrown in an
empty bar beside a probe of content 1 at rest, the probe's `pushed` line
(the active mass) against the body's `step` lines under a declared kick
(the inertial mass), the ratio 1 at rest and `gamma` in motion to the
grain.

**The hadrons.** Under "one content in flight per contact" (19.1, 18.3)
the pion, a pair with one contact, holds 6.86 MeV and carries 132.7 in
flight; the nucleon on the chain holds 9.02 and carries 929.2 over two
contacts, 464.6 per contact (309.8 on the triangle): the pion's F per
contact is 0.29 of the nucleon's, and a nucleon at the pion's F would
weigh 274 MeV against 938; under the steady-state form with one `(n /
d) tau` the pion would weigh 714 against 139.6; and the rho, the same
pair at the same contact, weighs 775 (an excited state the law has no
second value for). **Not reached**: the content in flight is not one
number per contact nor one rate for all bonds; nature's lightness of
the pion (the Goldstone boson of chiral symmetry) and the hadrons'
excitations are dynamics the six verbs do not have, and every F is an
input per bond.

**The leptons.** Free families, no bond, no reading but the declared
content: `m_mu / m_e = 206.768`, `m_tau / m_e = 3477.4` are inputs (16.2,
16.4). Koide's relation, `(m_e + m_mu + m_tau) / (sqrt m_e + sqrt m_mu +
sqrt m_tau)^2 = 2 / 3` to `3 x 10^-6`, is on record as a coincidence of
that precision with no path from the structure (the rule of section
16: the law has no square root of a content and no rule on three
families).

**The neutrino.** The law's `nu` is a free family with the content 0
on the register; nature's oscillations give squared mass differences
`7.4 x 10^-5` and `2.5 x 10^-3` eV^2 (PDG 2024), so at least one neutrino
has a mass above 0.05 eV and below 0.8 eV (KATRIN 2022, Nature Physics
18, 160): **a massless neutrino is refuted**, a content above 0 is an
input, at least `10^-7` of the electron's, and the oscillation itself
(a family turning into another with the flight) is `become` at a phase,
outside this section.

**The carriers.** The `w` family (charge `-7344`, lifetime 1) and any
Z or Higgs are paid carriers whose content is declared; no reading of
the law fixes them.

**Reached, bound, input**, for the whole family of masses: reached in
form, a bound set's mass as its total content and the condition that
its release read E; reached in sign, the neutron's charge radius (19.3);
reached within the inputs' uncertainty, `m_n - m_p`; bound, the floors
(1, 3, h) and the electron's count; input, every count and every F per
bond; refuted as declared, the massless neutrino. The masses that
nature measures after its detectors are, in the law, the counts and the
bonds' contents in flight, and the law's structure fixes the readings,
the floors and the relations between them, not the numbers.

## 20. The periodic universe against the measured numbers

**The owner's decision** (record 270, translated: "a periodic universe
is a possibility but it needs a proof, or leave it open: the
mathematician, according to the numbers that are measured"; the Boss's
order). Two boards, what each predicts for a detector at rest under the
growing wall of section 15, the measured numbers that decide, the
verdict in the owner's terms, and expansion-v1's rule stated once so
that it can be chosen. The host script
[periodic_images.py](designs/derivations_beam/periodic_images.py) with
its output
[periodic_images.out](designs/derivations_beam/periodic_images.out)
makes the numbers; no run.

### 20.1 The two boards under the growing wall, and what each predicts

The periodic GameBoard is the torus `Z_X x Z_Y x Z_Z` with no faces (a
row leaving one side enters the other; records 218, 234); the open
board is the segment whose ends are faces (an open face is a detector,
an escape a click, the content lost outward). Both under 15.1 (b): the
flight's wall `2 T_D a` with `a = 1 + H t`, no Node inserted, the
coordinates fixed, c in Links per interval unchanged and `c_0 / a` in
the original Nodes per interval. For a detector at rest:

| the reading | the periodic board | the open board |
| --- | --- | --- |
| the Hubble diagram, z against the flight time | `1 + z = a(t_r) / a(t_e)`, Milne's `z = tau / (T - tau)`, `q = 0` (15.2, 15.4): the wall is local, the board's topology does not enter inside the first winding | the same, exactly |
| the far stars' images | a lamp's rows return along every winding: images of one lamp at the winding distances `n L` (L the box's side) along the axes and the diagonals, `z_n = e^(H n L / c_0) - 1` under the tick wall, their count within the causal reach `(c_0 / H) ln(1 + H t)` (the script's (A), section 15's world, L = 301, H = 1 / 400: no image before t = 1000, 18 at t = 3000, 80 at 10 000, 304 at 100 000; `z_1 = 2.68`, `z_2 = 12.6`, `z_3 = 48.9`; the reach saturates at 1807 Links by `10^6` intervals, 3402 by `10^9`, so the count is finite for ever) | none: a row that reaches a face is a click, nothing returns |
| the largest angular scales | no mode longer than the box: the power of the oldest rows (the crowd's first shell) is missing beyond L, and the sky of a detector repeats: the same rows arrive from two directions at once when the reach exceeds `L / 2` (the matched circles of a torus) | no cut, no repeat |
| the isotropy of the count | isotropic from every Node (15.4 (i)); the images anisotropic, aligned with the axes and the diagonals of the box (the fan's grain, 15.5) | isotropic from every Node; no images |
| Seeliger's accumulation | fills without bound in a static board (14.3, 15.5: linear in t); cured by the wall, the presence steady from about 1000 intervals (0.000765 of `q dwell` per source at L = 301) | never fills: the rows leave through the faces; cured trivially, at the price of the content lost |

So the two boards differ in nothing a detector reads inside the first
winding, and in three things beyond it: the images, the cut at the
largest scales with the repeated sky, and the anisotropy of the images.

### 20.2 The measured numbers that decide

Per number: its value with one source, what the law's boards say, and
whether the register can compare it (NATURE.md's rule (b): a
dimensionless comparison the register makes; a size in metres needs
the dictionary).

| the number | measured | the boards | the comparison |
| --- | --- | --- | --- |
| the deceleration `q_0` | -0.53 (from `Omega_m` = 0.315(7), `Omega_Lambda` = 0.685, Planck 2018, Aghanim et al., A&A 641, A6, 2020) | Milne's 0 on BOTH boards (15.4): the wall gives it, the topology does not | dimensionless, the register's (16.4: not reached; nature's -0.53 outside the coasting bracket); decides nothing between the boards |
| the matched circles | none found: the fundamental domain of a flat torus larger than the last-scattering surface, `R_i > 0.97 chi_rec` for the inscribed radius (Planck 2015 results XVIII, A&A 594, A18, 2016; Planck 2013 XXVI: 0.92), so the box's side `L > 1.94 chi_rec = 27.2` Gpc, 0.97 of the surface's diameter (Cornish, Spergel, Starkman and Komatsu 2004, Phys. Rev. Lett. 92, 201302: beyond 24 Gpc) | a periodic board whose box is smaller than the reach shows the repeated sky; the bound says the box is at least 0.97 of the diameter of the oldest shell, so the first image lies at or beyond the last-scattering surface | a ratio, `L / (2 chi_rec)`, dimensionless: the register compares its box to its reach the same way; the measured value is a bound, `> 0.97` |
| the ghost images | none in the catalogues (cosmic crystallography, Lehoucq, Lachieze-Rey and Luminet 1996, A&A 313, 339; Roukema 1996): no pair of images of one source at a winding distance within the catalogues' depth of a few Gpc | the periodic board predicts them at `n L` with `z_n` above; their absence bounds L below the catalogue depth only | a count, dimensionless; weaker than the circles |
| the largest-scale anomalies | the low quadrupole and the lack of large-angle correlation, at 2 to 3 standard deviations (Planck 2018 results VII, isotropy and statistics, A&A 641, A7, 2020) | compatible with a box of about one diameter (the missing power beyond L) and with chance; not a proof | a ratio (the correlation statistic), dimensionless; the register has no oldest shell registered yet |

### 20.3 The verdict, in the owner's terms

**Open, neither proven nor refuted.** Every reading inside the first
winding is the same on both boards, and the only measurements that
reach the whole sky put the period beyond 0.97 of the last-scattering
surface's diameter: a periodic universe smaller than the surface is
REFUTED (no matched circles), one larger than the surface is
indistinguishable from an open one by any measurement to date, because
no signal has yet crossed a winding. **The one number that decides**:
the box's side in last-scattering diameters, `L / (2 chi_rec)`. Measured
`> 0.97`; a matched pair of circles found would fix it below 1 and
prove the torus; nothing can push it above 1 by observation, since the
image that would show it lies beyond the oldest light. What the law's
registers would have to show for the periodic board to be more than a
convention: a lamp's second image at the winding distance with the
redshift `e^(H L / c_0) - 1` (2.68 in section 15's world), the repeated
sky when the reach passes `L / 2`, and the steady presence of 15.5, all
on a run under the growing wall, which the open board cannot show. So
today the law's choice of board is a CONVENTION, and it is stated as
such: the periodic board is the one that closes Seeliger under the wall
without losing content through faces (15.5) and keeps the total
computation constant (16.2 (f)), the open board the one every registered
world uses; neither is required by a measured number, and the owner may
leave it open.

### 20.4 expansion-v1, stated once so that it can be chosen

The rule: the flight's wall is `2 T_D x a` with `a = H_den + H_num x
tick`, H = `[H_num, H_den]` a declared constant of the world, the rate
`2 S_1 Q x H_den` untouched, the tick the interval's index read by the
row at its carry (a local reading, the interval every record carries;
15.2); the body's drive under form B scales its `T_D` the same way
(15.5), the turn's wall does not (15.3); the board periodic or open as
the world's one boolean (the existing `boundary` key), with no other
change. The three tests (15.6): generic, one wall factor for every
family and direction, no name; vector, a translation whose wall is a
count, F's feedback block, no root, no float; local, if the tick is a
local reading, and then it reads only the row's own accumulator. What
it gives: `1 + z = a(t_r) / a(t_e)`, Milne's `q = 0`, `c a = c_0`,
Seeliger cured on the periodic board; what it does not: nature's `q_0
= -0.53` (a rising H would be a second declared rate, a hypothesis
beside this one), and any decision between the boards. Absent by
default; the identity `expansion-v1`.

## 21. The derivation map: how every formula of this document was reached, from the six verbs to the number, with its script and its run

**The owner's direction** (2026-09-21, in conversation, translated:
"show them how you reached all these things, logically,
schematically, with formulas and links to the simulator's runs; we
need it for the paper, so that we have the big explanation of how one
reaches our general formula"). This section is the map: one schema
from the six verbs to every formula, and one table per formula with
its premises, its closed form, the host script that checks the
arithmetic, the registered run that checks the number, and the verdict.
The chronology of how the work went from runs to formulas is
[CODE_TO_FORMULAS.md](CODE_TO_FORMULAS.md); the register's own
derivation entries are in each world's README under
`examples/events/`; the paper cites this map by section number.

### 21.1 The schema

    THE GIVEN (Highlights 5.7): the integer torus, the six Ports, one carry per Node per interval (K),
    the six verbs T B G P E D, the widths N Q P W K_clock, the family table, the width S, the state.
        |
        v
    THE OPERATOR F (section 0) = the linear block  +  the feedback block
        |                              |                       |
        |        rows in flight: T on the Manhattan       bodies: the four readings of the block
        |        accumulator against the wall 2 T_D;      (the count D, the push B, the drive T,
        |        the merge G in Z[Z_N]; the click E, D     the turn T), each one by_drive
        |                              |                       |
        v                              v                       v
    the flight's norm             the wave equation at c     Newton (3), the delay field (5),
    c = 1 / sqrt 3 (13.2 a)       (5.1), Lorentz its         the crossing count (2, 12b, 12c),
    the third statement (262)     symmetry (4.1)             the owed count (5.2, 13.2 b)
        |                              |                       |
        v                              v                       v
    the dictionary (5.7):          the click as the Gram     THE THEOREM (17.1): Einstein's formulas
    G, h, e units; only            form and one threshold    hold for whatever is built from the
    dimensionless numbers          (6.5 Gleason, 6.2 Born,   linear block, and for a body as far as
    reachable (16.1)               Tsirelson, 7.1 Young)     its four readings are covariant
        |                              |                       |
        v                              v                       v
    the minimal mass (16.2),       the information law (9),  covariant-readings-v1 (17.3): E as an
    the floors (16.2 d),           entropy (14), the         accumulator, v = p c^2 / E, the turn
    the units from c, G, hbar      classical-quantum         per proper time, the gradient push,
    (16.2 f), G from K (16.2 f)    boundary (6.3)            the count per turn: E = m c^2 forced
        |                                                         |
        v                                                         v
    the bound set's mass = its total content (19.1),          the three failures (18): the clock
    the chain on the bipartite lattice (19.3),                closes, the weak forms split, the
    the growing wall and the periodic board (15, 20)          strong ratio 4 against 12.7, masses open

### 21.2 The table: one row per formula

Status: **R** reached (the formula follows and the register's number
checks it), **F** reached in form (the shape follows, the number is an
input), **B** bound or related, **D** different law (the law gives
another formula, stated), **I** input, **X** refuted as declared, **H**
a hypothesis named with pins, not built. "Run" names the registered
world whose README carries the number; "script" the host arithmetic in
`docs/designs/derivations_beam/`.
"The pin before the run" (record 316) names the number the register
held before that run and its source: an expectation paragraph of
EXPERIMENTS.md, a series' `expectations.json`, or a design's pin;
"no pin; a host reading" where the number is a script's reading of the
register after the run; "no pin; the run's own reading" where a run
was registered without a written expectation, with the run and its
date; "pinned, not run" where the pin exists and no run has been made;
"no run" where the row has no run at all. No number moves by the
column.

| # | the formula | from (the verbs, the premises) | the closed form | section | script | run (the registered check) | the pin before the run | the order of the expansion | the error term | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | c, the pace of light | T on the flight's accumulator, one carry per interval (K), isotropy, the third statement | `c = 1 / sqrt 3` Links per interval (`32 / 55` on a heading at Q = 64) | 13.2 (a), 1.4 | (record 186's light_speed map) | every flight table; `T_D = isqrt(3 abs(D)^2 Q^2)` | pinned: the pace per direction 0.5718 to 0.5893 (the mean 0.5810), the asymptotic 0.5774 to 0.5818 (series Q, `c_measured/expectations.json`, written from the closed form before the run) | exact: an inequality with equality on the diagonals | the load-time rounding of `T_D` (isqrt), one step in 234 on a heading | R (the bound and the value; the realisation stated, record 262) |
| 2 | the flight's line and period | T, the Bresenham deficits | `m(tau) = (2 tau S_1 Q + T_D) // (2 T_D)`, `tau_k = ceil((2k - 1) T_D / (2 S_1 Q))` | 1.4 | `event_count.py` | `cone_links`, the 24 stars' Links | pinned: the flight table's own rows as the closed form's check (`tests/test_amplitude_cone.py`, derive-and-compare); the 24 stars' Links no pin; a host reading (`event_count.py`) | exact in integers | the deficit below one Link | R |
| 3 | the plane wave, `omega = c k`, the light cone | E on the phase, the flight | the rows' limit is the retarded wave equation at c | 4.1, 5.1 | `lorentz_field.py` | series K: the mean age 89.40 in every world | pinned: the mean age of the arrivals the control's within 1 interval, the flight table's 89 and 90 (series K) | second order in the Link | not stated; the flight table's per-direction pace (1.5 percent above `1 / sqrt 3` on a heading) would state it (row 48) | R |
| 4 | Doppler on the axis | D, the crossing rule (record 158; BEAM_LAW note 48; built, PR #468 at 562fb736) | `1 +- v / c` head-on and behind, exactly 1 across | 2.2, 2.3, 2.7 | (record 158's crossing_sim) | `tests/test_crossing.py`: 45 / 58 toward, 19 / 38 away, 48 at rest; 183 / 311 and 74 / 202 over 32 Links; the doppler bar's 97, 45, 303, 0, 58 (the deleted key's limit) | pinned: 45 / 58 toward, 19 / 38 away, 48 at rest, the sums 183 / 311 / 74 / 202 (TEST_EXPECTATIONS.md, "The crossing rule", written before the first run; the plane's pins from `crossing_2d.py`); the doppler bar's five numbers are the deleted key's registered readings, no pin claimed | exact over whole Links | one boundary row per Link | R, built |
| 5 | the fan direction's count | D on the Manhattan flux | `1 + v T_d / (Q S_1)`, off the Euclidean by `abs(D)^2 / (a S_1)` | 2.4 | `mover_counter.py` | record 158's `1 + 2.44 / k` on the bar | no pin; a design reading (`crossing_sim.py` of record 158, the physicist's scratch map, not a registered run) | exact | none: another formula, stated | D (stated) |
| 6 | Newton's inverse square, G | B (the push), the shell mean of the flux | `a = -G M / r^2`, `G = K_fan (n / d) / (4 pi S)` | 3.3 |  | series 7 (`push_m = m push_1`), series D's orbit | pinned: item 1 the identity `push_m = m x push_1` record by record, item 6 the count `~ 1 / r` in the mean over a ring (series C (GAMEBOARD, the probes' reading) under the Beam Law); series D's orbit closed within r / 4, T within 15 % | the leading term of the shell mean | the fan's grain: the ring flux `r^-1.83` against `r^-2` (7.2), the shell's Node-count ripple (3.2) | R |
| 7 | Coulomb with one constant | B, the charge column | `k_C = G`, the ratio `-rho_A rho_B` | 3.4 |  | item 7's `-1` and `-1 / 4` exactly | pinned: item 7 `-Qq / (M m)` exactly (series C (GAMEBOARD, the probes' reading)) | exact in form | the apportioning's grain | R |
| 8 | the third law | the apportioning at the release | the sources' momenta equal and opposite to the grain | 3.3 |  | `9612145197056` against `-9612088573952` | pinned: item 2 the third law 1.00 exactly, the cumulative ratio 1.0000 at four decimals (series C (GAMEBOARD, the probes' reading)); the two integers are the run's reading of that pin | exact to the grain | 6 parts in `10^6` (the two sources' momenta) | R (at rest) |
| 9 | Poisson and the retarded wave equation of the field | B (the age moment), the release | `A = q dwell / (4 pi c r)`, the source `(dwell / c) q delta` | 5.1 |  | series E (GAMEBOARD, the probes' reading): `k_a r = 36.1`, `k_s r^2 = 41.5`, ratio `sqrt 3 / 2` | pinned: `k_s r^2` constant (40 with the heading's dwell) within +- 15 % over r >= 6, `k_a r` constant within +- 15 %, the ratio `sqrt 3 / 2` (series E); 36.1 and 41.5 are the measured means inside those pins | the leading term | the dwell's direction dependence (1.72 on a heading, 1 on the diagonal), the shell means 39.0 to 44.8 | R |
| 10 | the gravitational redshift | D (the owed count) on the age moment | `1 / (1 + k_a)`, `k_a = G M / (r c^2)` at first order | 5.2 |  | series E's (GAMEBOARD, the probes' reading) shells r = 4 .. 14 | pinned: the age clocks' ratio against the 1 / r law fitted at r = 14 within 15 % of the law's shift, the first-order line expected to fail (series E) | first order in k | the second order: `k^2` against nature's `k^2 / 2` | R at first order, D beyond |
| 11 | the bending of light, Shapiro | the rows blind to the crowd | none on `main`; `~ M / b` under the meeting key | 5.4 |  | series K: 0.000 registered | pinned: the centroid's deflection 0 within 0.5 pixel at every M and b (series K) | none | none: a different law | D |
| 12 | Born's rule | E, the norm, the rung | `abs(P - W / T) <= 1 / (2 N)` | 6.2 | `click_gram.py` | `mz_equal` 64 / 0, `mz_345` 63 / 1 | pinned: `mz_equal` 64 / 0 and `mz_345` 63 / 1 from the offers 1681 / 1682 and 49 / 50 (`amplitude/expectations.json`, series L1) | the rung, `1 / (2 N)` | `1 / (2 N)` = 0.0078 at N = 64, the tables' rounding a part in 276 | R as a limit |
| 13 | Gleason on the lattice (the form of the click forced) | rotation, the balanced splitter, non-negativity | `R = sum c_j abs(sigma_j f)^2`, the power 2 pinned to [1.917, 2.489) | 6.5 | `click_gram.py` | `mz_345`'s 63 / 1, the first cell 27 | pinned: `mz_345` 63 / 1 (series L1); the window `[1.917, 2.489)` and the first cell 27 no pin; a host reading (`click_gram.py` after the run) | exact in form | the rung's window on the power: [1.917, 2.489); with N = 32 and 128 registered (34f505ec) the intersection [1.917, 2.012) | R |
| 14 | Tsirelson's bound | E on the pair | `S(N, Q) -> 2 sqrt 2` | 6.2 |  | `176 / 64`, `2896 / 1024`, `11584 / 4096` | pinned: S = 2 exactly, S' = 3 / 2, the offsets 14 and 16 (A2 under the Beam Law, `bell/expectations.json`); `176 / 64` and the sequence are the closed form's values, no run | the limit N, Q to infinity | `8 / N + 16 arcsin(sqrt 2 / (2 Q))` | R as a limit |
| 15 | Young's spacing | the fan's angular measure, the click | the fringes at the wavelength times the distance over the opening | 7.1 | (record 160's two_slits map) | `slits_low`'s 64 clicks reproduced row by row | pinned: the weights per pixel and the clicks 34 / 15 / 15 over the 64 births (`amplitude/expectations.json` under `two_slits`, the generator's reading before the run, series L2) | paraxial, `s, y << D` | the fan's grain (91 directions) and the tables' rounding (a rung by parts in `10^3`) | R in the limit of every direction |
| 16 | Bohr's quantisation | the turn under `action`, the push | `2 pi p r = j h`, `r_j ~ j^2` | 7.2 |  | series H, r = 12 closing (j = 4.01) | pinned: the closure `4 p r = j h` with j = 2 at r = 8 and 2.555 at r = 12, the orbit closed within r / 4, T within 15 % (series H); j = 4.01 at r = 12 no pin; the run's own reading (7.2's true sum re-derived on the registered orbit, 2026-09-20) | the limit of small Links | the digital circle: 2.041, 2.011, 2.003, 2.000 at r = 8, 16, 64, 256 | F (the levels and lines not reached) |
| 17 | the information law, the click's cost | the one non-bijective read | units per record against bits out; `log2 (cells)` per click at most | 6.1, 9 | `click_gram.py` | the four worlds' units per bit 82, 2, 2, 29 | no pin; a host reading (`click_gram.py` on the four registered worlds) | exact | none | R |
| 18 | the moving clock's rate | the frame (T) | 1 at every speed; only the crowd slows a clock | 4.3 |  | `coasting_none`: `s_mz2` at `z = 0.2636` | pinned: `1 + z = 1 + v / c` within 2 %, `s_mz2` at v / c = 0.2674 (`hubble_stars/expectations.json`, the coasting form); the register reads 0.2636, inside | exact | none: the rate is 1 | D (the register's) |
| 19 | the dispersion | T (the drive), form B | `v = p / (m + p / c)`, first order off Newton | 4.4, 17.2 | `covariant_readings.py` | the hubble throws at 0.6 c, G2 at 0.5 c | pinned: the stars' speeds declared, the momenta from them by `v = p / (Q S M + p)` (`hubble_stars/expectations.json`; the hubble throws by the same rule) | first order in `v / c` | 5.3 percent at `0.05 c` (nature's second order 0.13 percent) | D |
| 20 | the event-driven interval | the scheduler to the next carry | bit-identical to stepping; 2.83 .. 8.73 events per active Node | 11 | `event_count.py` | the five worlds in-process | pinned: bit-identity with stepping on the five worlds (the test's assertion before its run); the events per active Node no pin; a host reading (`event_count.py`) | exact (bit-identical) | none | R |
| 21 | the Lienard-Wiechert potential | B (the age moment) of a moving source | Heaviside's ellipsoids, exact in the limit | 12.1 | `lorentz_field.py` | the deuteron's fan at k = 4, 8 | no pin; a host reading (`lorentz_field.py` on 12.1's potential, no registered run) | the limit of every direction | the fan's grain (the nearest direction by comparison); the check to `10^-15` | R |
| 22 | the co-moving push | the flux along `n_ret` | `(1 -+ beta)^2`, `(1 - beta^2)^2` aberrated, `1 - beta^2` across; one `1 / gamma` short | 12.1, 12b.1 | `lorentz_field.py` | pins for the pair in motion (12.4), not run | pinned, not run: `(1 -+ beta)^2` along and `1 - beta^2` across on 12.4's pair (12.1, 12b.1) | the continuum limit | at one Link the aberration starves the exchange: 304 / 116 / 157 against 188 / 228 / 152 | D |
| 23 | the aberration rule | T then D on the fan's direction | `w = Q W D + T_D N_v`, the nearest by comparison | 12.2 | `lorentz_field.py` | pins 304 / 116 / 157 per cycle | pinned, not run: 304 / 116 / 157 per cycle at k = 4 (12.2) | exact in integers | the fan's grain | H |
| 24 | the thrown orbit | B and T integrated | contraction 0.87 .. 0.96, slowing 1.31 .. 1.43 at 0.21 c | 12b.2 | `orbit_thrown.py` | pins on `s32_r24` | pinned, not run: the contraction 0.87 .. 0.96, the slowing 1.31 .. 1.43 on `s32_r24` (12b.2); series D's own pins on that world (closed, T 687) are the register's | the continuum integration | not stated; the lattice's Bresenham orbit (a run) would state it | D |
| 25 | route C, the mover's counter | D (the crossing count), D (the owed count) | the isotropic mean exactly 1; no slowing | 12c | `mover_counter.py` | pins on series E's axis probe (p = 10, 28) | pinned, not run: 0.7883 / 1.2117 at p = 10 and 0.5708 / 1.4292 at p = 28 on series E's axis probe (12c.6) | exact on a symmetric fan | one boundary row per Link | R (no slowing), D against gamma |
| 26 | the one constant K | LOCALITY-1's budget | the causal bound, the wait `26 k / K`, the bits `log2 K`, the widths free | 13 |  | the budget equation against the register's widths | no run: a bound on the register's declared widths, no number to pin | bounds, not an expansion | none | B |
| 27 | entropy | the count of torus points consistent with the click list | bits read + bits erased = `log2 N` per record | 14 | `entropy_clicks.py` | `mz_equal` 0 / 6, `slits_low` 3.425 / 2.575 | no pin; a host reading (`entropy_clicks.py` on the registered click lists) | exact identity | none | R |
| 28 | the growing wall, the redshift | T with a growing wall (F's feedback block) | `1 + z = a(t_r) / a(t_e)`, Milne `z = tau / (T - tau)`, `c a = c_0` | 15 | `growing_wall.py` | the 24 stars, rms 0.0044 at T = 440 | no pin; a host reading (`growing_wall.py` on the 24 stars' declared speeds); the registered G2 run pinned the coasting form and Milne's `H t_0 = 1` within 10 %, not the wall | first order in H per interval for the closed forms | the accumulator's integer, one part in 400; the second order `(H d / c_0)^2 / 2` (row 55) | R for the form; the tick's locality the owner's |
| 29 | Seeliger cured | the wall's cutoff at the Hubble length | the presence steady from 1000 intervals | 15.5, 20.1 | `growing_wall.py`, `periodic_images.py` | (a periodic world under the wall, not run) | pinned, not run: the presence steady from 1000 intervals on a periodic world under the wall (15.5, 20.1) | the image sum | the cutoff's tail beyond the Hubble length | R on paper |
| 30 | the constants of nature | the dictionary | G, h, e, k_B units; only dimensionless numbers reachable; none reached | 16.1, 16.4 | `nature_numbers.py` |  | no run: the dictionary's identities on nature's constants | none | none: units | I (with the reason) |
| 31 | the minimal mass | the integer form | one unit; every ratio rational; the electron at least 4526 units | 16.2 | `nature_numbers.py`, `smallest_mass.py` |  | no run: a theorem on the integer form; the 4526 units from nature's ratios | none | none: a bound | B |
| 32 | the floors per kind | the charge line `rho = [n, d]` | the floor d under a whole charge: 1, 1, 3, 3 | 16.2 (d) | `smallest_mass.py` | QUARKS.md's counts (multiples) | pinned: the read masses 20, 25, 20, 45, 45, 20, 1836 and the pushes per body (`quarks/expectations.json`, committed at eba635dd before the run, series R); the floors 1, 1, 3, 3 are the design's counts | none | none: floors | B |
| 33 | `alpha` and `alpha_G` related | `k_C = G` | `rho_p = sqrt(alpha / alpha_G) = 1.1 x 10^18` | 16.4 | `nature_numbers.py` |  | no run: a relation between two of nature's numbers | none | none: an identity of the form | B |
| 34 | the Link, the interval, the unit | the three conversions | `L = l_Planck / sqrt(3 sqrt 3 G_law hbar_law)`, T, M | 16.2 (f) | `units_from_g.py` |  | no run: the conversions on nature's constants | none | none: a relation | I (the relation derived, the number needs h and S) |
| 35 | G from the computation | one G for the clock and the push, the budget reading | `S = K_budget / 26`, `G = 26 K_fan (n / d) / (4 pi K_budget)` | 16.2 (f) | `units_from_g.py` | series E's S = 1 and [1, 1] | no pin; the world file's declarations (series E's S = 1, the rate [1, 1]); no run reads them | none | none: two assumptions named | B (two named assumptions) |
| 36 | not G but the pace varies | lunar laser ranging | `Gdot / G = 3 H` refuted; under the wall G and K constant | 16.2 (f) | `units_from_g.py` |  | no run: lunar laser ranging is nature's number | none | none: a bound of nature's | R |
| 37 | the theorem of covariant readings | the wave equation's symmetry | Einstein's formulas for whatever is built from the linear block | 17.1 | `covariant_readings.py` |  | no run: a theorem; `covariant_readings.py` a floating-point check of its own formulas | exact: a symmetry | none | R |
| 38 | E = m c^2 | the exact square `W = E'_0^2 + 3 p . p` on the record (B), `E'` the largest integer with `E'^2 <= W` by comparisons (D), the proper-time owed count `by_drive(acc_tau, E' - E'_0, E'_0)` (T), the drive `p / (Q S M)` per self-creation without the cap term; the Newtonian limit | `E'_0 = Q S M` forced (`E_0 = Q S M c^2`); the pace `p / E'` Links per interval; the invariant exact | 17.3 (iii), 17.6 M1, M3, M7 | `covariant_readings.py` (a floating-point check), `amended_pins.py` (the integers) | the J4 world of 17.6's M9 (to be written): the products' face clicks at 367 and 345, the rest 391 | pinned, not run: the face clicks 367 / 345 / 391 on the J4 world (17.6 M9, N6) | exact in the amended form (W carried) | none: `E'^2 <= W < (E' + 1)^2` at every step | H (covariant-readings-v1, decided built, record 270; amended per records 297 and 314) |
| 39 | the time dilation, the Doppler with gamma, the contraction | the self-creation gated by the proper-time owed count (17.6 M1), the crossing count charged per self-creation, `-grad(A)` across the six Ports | the 64th self-creation at `64 E' / E'_0`; the count per self-creation `gamma (1 - v T_d / (Q S_1))` per direction; the contraction NOT derived (`-grad(A)` alone: the rest force along, `gamma` across) | 17.3, 17.6 M1, M4, M5 | `amended_pins.py` | J4 at p = 3640 and 12 856 (70.9, 125.2); `coasting_none` at the declared momentum, z = 0.369; the contraction unpinned | pinned, not run: the 64th self-creation at 70.9 and 125.2; `z = 0.369 +- 0.003` on the registered `coasting_none` (17.6 M2, N5) | exact per self-creation | one tick (the owed count's integer) | H for the dilation and the Doppler; the contraction open until `source-velocity-v1` |
| 40 | the weak forms | the click against the record: bounded; against the crowd: memoryless as far as it mixes | the width over the median 2.1 against 3.17; the rate the family's | 18.2 | `decay_click.py`, `crowd_decay.py` | pins on J1, J2; Voyager and MESSENGER as nature's | pinned: J2's five worlds 16, 0, 512, 32, 0 of 1024 and the far detector 699, 0, 352, 688, 711 (`weak/expectations.json`, series J); J1's `become` counts no pin; the run's own reading (the range over a warm run of 120 intervals, the file says "measured", 2026-09-20); Voyager and MESSENGER nature's | exact by enumeration | none | H (decay-by-crowd-v1, restated) |
| 41 | the strong ratio | the give per contact pair on the bipartite lattice | 4.0 (6.0) against 12.72 | 18.3 |  | `alpha_square_bond`'s 2.0 | pinned: `alpha_square_bond`'s ratio 2.0 to the deuteron against nature's 12.72, stated before the run as the law's failure (series N) | counts | none | F |
| 42 | a bound set's mass | held + in flight - escaped | the proton 1 % held, 99 % in flight; `m_n - m_p = m_d - m_u = 2.54`, 1.51 with the electric part | 19.1, 19.2 | `masses_chain.py` | pins for the quarks design | pinned, not run: the quarks design's masses (`masses_chain.py`); series R's registered pins are the pushes and the read masses, not these | exact in form | the quark masses' uncertainty, 0.41 MeV | F (the number within the inputs' uncertainty) |
| 43 | the nucleon's chain, the neutron's charge radius | the lattice bipartite, one bond per contact | `+4 / 3 L^2`, `-2 / 3 L^2` (the sign) | 19.3 | `masses_chain.py`, `periodic_images.py` | pins for the quarks design | pinned, not run: the radii `+4 / 3 L^2` and `-2 / 3 L^2` (19.3) | exact in sign | the point charges: the magnitude by 3 | R in sign, D by 3 in magnitude |
| 44 | the equivalence principle for a bound body | the release reads the body's own `E' / (Q S)` (17.6 M6), per lattice interval (17.6 N4); the energy in flight is the rows' | `by_drive(acc_release, E' x n, Q S x d)`; the field of a body equal to its own rest plus kinetic energy; the binding fraction E16's | 19.5, 17.6 M6 | `rest_of_masses.py` | a thrown body beside a probe of content 1: the probe's push against the body's drive, 1 at rest and `gamma` in motion | pinned, not run: the probe's push 1 at rest and `gamma` in motion (17.6 M6, N4) | none | none: a condition | H for the body's own energy; the binding part `field-source-v1` (E16) |
| 45 | the hadrons, the leptons, the neutrino | no rule selects a count | inputs; Koide a coincidence; the massless neutrino refuted | 19.5, 16.2 (g) | `rest_of_masses.py` |  | no run: nature's masses as inputs | none | none: inputs | I, X |
| 46 | the periodic universe | the two boards under the wall against the measured bounds | open; `L / (2 chi_rec) > 0.97` | 20 | `periodic_images.py` | pins for a periodic world under the wall | pinned, not run: the two boards' image counts against the catalogues (20) | none | none: a bound of nature's | B (a convention today) |
| 47 | Gauss's law and the continuity of the field | the release, the flight, the presence (T, B), the books | `div(g) = -4 pi G rho`, `d rho / dt + div(j) = 0` | 5.5, 21.5 |  | series E's (GAMEBOARD, the probes' reading) `k_s r^2 = 41.5` | pinned: `k_s r^2` constant, 40 within +- 15 % (series E); 41.5 the measured mean, inside | exact at every instant; the shell mean's leading term | the fan's grain (`r^-1.83`), the shell ripple | R |
| 48 | the wave equation of the field | the flight at c, the age moment (T, B) | the retarded scalar wave equation at c | 5.1, 21.5 | `lorentz_field.py` | series K's ages 89.40; the potential to `10^-15` | pinned: the mean age 89 and 90 within 1 interval (series K); the potential to `10^-15` no pin; a host reading (`lorentz_field.py`) | second order in the Link | the cube's anisotropic term at `(k Link)^2`, the pace 1.5 percent off on a heading | R |
| 49 | Faraday and Ampere-Maxwell, the moving charge's field with the magnetic term | the age moment as the scalar potential; the vector potential from a carried source velocity (`source-velocity-v1`) | Jefimenko's retarded fields from both potentials | 12.1, 17.6 M4, 21.5 | `lorentz_field.py` | the potential to `10^-15`; the pair's transverse push `1 / gamma` when **A** exists | no pin; a host reading (`lorentz_field.py`); the transverse push under **A** pinned, not run (17.6 M4) | the potentials' order | the age's integer, the fan's grain | H (`source-velocity-v1`) |
| 50 | the Lorentz force and Biot-Savart | `-grad(A)` across the six Ports; `q v x B` and the magnetostatic **A** | `q (E + v x B)`; `B = (mu_0 / 4 pi) integral of J x r / r^3` | 17.6 M4, 21.5 |  | the deuteron fan at k = 4: `1 / gamma` across, `1 - beta^2` along under **A** | pinned, not run: `1 / gamma` across and `1 - beta^2` along on the deuteron's fan at k = 4 under **A** (17.6 M4); the fan's numbers a host reading | first order in the Link | the central difference's `Link^2` term | H (the electric part covariant-readings-v1, the magnetic `source-velocity-v1`) |
| 51 | Planck, `E = h f` | the release pays `h s` per unit at a turn of s steps | `E = h s = (h N) f` | 6.4, 21.5 |  | the Bell lamps' 2 per birth, the stall at tick 4 | pinned: L1's 64 births with none at tick 2 (`amplitude/expectations.json`, the birth rows); the Bell lamps' stall at tick 4 (159 births in 160) no pin; the run's own reading (A2 under the Beam Law, 2026-09-19, the bell README) | exact | none | R |
| 52 | de Broglie, `lambda = h / p` | the turn by momentum under `action`, `abs(p) N / h` per Link | a circle every `h / abs(p)` Links | 7.2, 21.5 |  | series H's closure on the digital circle, 2.041 .. 2.000 | pinned: j = 2 at r = 8 by the closure `4 p r = j h` (series H); the digital circle's 2.041 .. 2.000 no pin; a host reading (7.2) | exact to the floor | one step per Link, `1 / N` | R (an identity under the declared key) |
| 53 | Boltzmann, `S = k log W` | the count of torus points consistent with the click list | `S = log2 W` bits, `k_B` the conversion | 14, 16.1, 21.5 | `entropy_clicks.py` | `mz_equal` 0 / 6, `slits_low` 3.425 / 2.575 | no pin; a host reading (`entropy_clicks.py`) | exact | none | R |
| 54 | Shannon, and Landauer | the bits read per click and the bits erased per record; the click's deletion | `H = -sum (w / N) log2 (w / N)`, read + erased = `log2 N`; the bound `k T ln 2` | 14, 6.1, 21.5 | `entropy_clicks.py` | `slits_low` 3.425 / 2.575 | no pin; a host reading (`entropy_clicks.py`) | exact | none | Shannon R; Landauer D (no temperature, record 140) |
| 55 | Hubble's law, `z = H d / c` | the growing wall `2 T_D a`, the tick wall | `z = H d / c_0` at first order, `1 + z = e^(H d / c_0)` in full | 15.2, 20.4, 21.5 | `growing_wall.py` | the 24 stars, rms 0.0044 at T = 440 | no pin; a host reading (`growing_wall.py`); the registered G2 run's pin is the coasting form and Milne's `H t_0 = 1` within 10 %, first order | first order in `H d / c_0` | `(H d / c_0)^2 / 2`; the accumulator's part in 400 | R for the form under `expansion-v1`, H an input |
| 56 | the aberration of light | the aberration rule `w = Q W D + T_D N_v`, the nearest direction by comparison | Bradley's `tan theta' = sin theta / (cos theta + beta)` | 12.2, 21.5 | `lorentz_field.py` | the pins 304 / 116 / 157 at k = 4 (not run) | pinned, not run: 304 / 116 / 157 at k = 4 (12.2) | first order in beta | `beta^2 / 2` against nature's `gamma`; the fan's grain `1 / P` | R at first order, D at second |
| 57 | Schrodinger for a free particle | the pair (flight, phase) of the linear block; a body's phase per Link | none: the rows' dispersion is `omega = c k`, a body is one record | 21.5 |  | none | no run | not applicable | not applicable | not reached (D); `dispersion-v1` named; section 23 checks the route as `massive-rows-v1` (row 60) |
| 58 | Kepler's three laws | the push `p += -M_A V(x)` in the shell mean (B), the drive on the momentum's direction, form B (T) | the ellipse, equal areas, `T = 2 pi r^(3/2) sqrt(4 pi S / q)` with `G M_B = q / (4 pi S)`; on the plane `T = 2 pi r (Q S m + abs(p) / c) / abs(p)`, `T ~ r` | 3.3, 12b.2, 21.5 | `kepler_compton.py` | series D's `s32_r24` (the plane); `s32_r24_lamp` and `s32_r12_lamp` to be written | pinned, not run, on the lamp worlds `s32_r24_lamp` and `s32_r12_lamp` under form B's pace (decided and in build; the physicist's `lamp_orbits_map.py`, the circular momenta re-derived under the directional drive, n = 10 at S = 32, 640 label units per unit of content): T 784 (714 to 855) at r = 24 and 392 (357 to 428) at r = 12, the mean radius `24.8 +- 1` and `12.4 +- 1`, the age's minimum advancing `-81 +- 15` degrees per radial period at both radii (the closed form `psi = pi / sqrt(1 + e)`, `e = d ln v / d ln p = 0.651` at n = 10: 140.1 degrees, `-79.8`; `kepler_compton.py` (D)), `T(24) / T(12) = 2.00 +- 0.15`; the earlier `-105 +- 15` the Newtonian pace's (e = 1) and the earlier 795 form B's period at the kept momentum 576, both kept as the record (21.5 row 58) | first order in `Link / r` and in `v / c` | form B's first-order slowing `1 / (1 - v / c)`; the fan's grain (`r^-1.83` on the 2616 shell); the lattice's own precession not derived | R in the limit (space); the plane's exponent 1 (F); the lattice's precession D |
| 59 | Compton, `lambda' - lambda = (h / (M c)) (1 - cos theta)` | the exact square (B) and the momentum's conservation at a `measure` then a `rerelease` (17.6 M7, N5), the released turn `floor(k' / h)` (T) | `1 / k' - 1 / k = sqrt 3 (1 - cos theta) / (Q S M)`, `lambda = h / k` Links, `c = 1 / sqrt 3` | 17.6 M7, N5, 21.5 | `kepler_compton.py` | the `compton` world (to be written), after covariant-readings-v1 is built | pinned, not run: the faces' turns 16 (+x), 11 (+-y, +-z), 8 (-x), 14 and 9 on the face diagonals, from k = 16 at `Q S M = 64` (21.5 row 59) | exact on the pair `c^2 = [1, 3]`; first order in `(k - k') / k` at the heading's c | the residual `(gamma^2 - 3) (k - k')^2 / (2 E'_0 gamma)`, `gamma^2 - 3 = 141 / 3025`; the floor of `k' / h` (one step); the fan's grain | H under covariant-readings-v1 with the exchange's accounting (`books`, N5); D on `main` |
| 60 | Schrodinger for a free particle, `massive-rows-v1` | the massive row: the flight's wall `E' = isqrt(E'_0^2 + 3 p . p)` (the photon its `E'_0 = 0` case, `T_D`), the turn `abs(p_a) N / h` per axis Link (7.2), no turn per interval | the phase `(N / h) p . x` on the Nodes; the Helmholtz equation `Laplacian(psi) + k^2 psi = 0`, `k = 2 pi p / h`: the time-independent Klein-Gordon form exactly, Schrodinger's at small p; the time-dependent form not reached | 23 | `massive_rows.py` | the `slits_matter` world (to be written) | pinned, not run: the bright bands at the pixels 36.5, 60, 83.5 within one, Pearson `0.96 +- 0.02`, the centre's first click at 941 within 2 (23.3, the lamp's flight to the opening counted) | exact on the Nodes for the phase; the dispersion within a part in `E'`; Schrodinger's at second order in `p / E'_0` | the fan's grain, the floor of `E'` (a part in 4113), the temporal phase dropped (a global factor per record) | reached only in part (the time-independent form); H, `massive-rows-v1` named, not built |

### 21.3 How to read the map for the paper

Every row is reached the same way: a rule of the law is written as its
verb on the state (section 1's inventory), its closed form is taken in
the limit the paper names (every direction, small momentum, many rows,
large N), the host script checks the arithmetic of the closed form on
its own, and the registered run's integer (the world's README, pinned
in a test) checks the number; where the two agree the row is R, where
the form follows and the number is a declared input F, where the law
gives another formula D with the formula stated, where a reading within
the six verbs would reach nature's formula H with its pins, where
nothing in the structure carries the number I. The general formula of
the paper is the operator F of section 0 with its two blocks; the rows
of this map are its limits, and the map is the proof that each limit
was taken from F and from nothing else.

### 21.4 The Einstein map: every result of the special and the general theory, its status today, what the six give, what must be added, the pin

The owner's direction (record 291): "derive all of Einstein, not only
`E = m c^2`". One row per result. "Today" is the law on `main` (the
crossing rule landed, BEAM_LAW note 48; form B decided); "the six give"
is what follows from the verbs as declared; "to add" names the reading
or the rule needed, under its identity (covariant-readings-v1 is the
decided one, record 270, its physics-rule review the gate of its build;
the others are named, not decided); "the pin" is the number a run must
meet, written before it.

| # | Einstein's result | status today | what the six verbs give | what must be added, under which identity | the pin a run would meet |
| --- | --- | --- | --- | --- | --- |
| E1 | Lorentz's symmetry of light, `omega = c k`, the light cone | R | the rows' limit is the wave equation at c (4.1, 5.1) | nothing | series K's ages, 89.40 in every world (registered) |
| E2 | `gamma`, the time dilation of a moving clock | D (the rate 1, 4.3; NATURE 4a) | no operation carries a body's speed into its clock | the self-creation gated by the proper-time owed count `by_drive(acc_tau, E' - E'_0, E'_0)` (17.6 M1), covariant-readings-v1 | J4's world of 17.6's M9: the products' face clicks at 367 and 345 (the decay at 70.9 and 125.2 derived), 391 at rest, one tick's tolerance on the decay |
| E3 | the contraction `1 / gamma` | D (12b.2: 0.87 .. 0.96 by the dispersion, unstable) | the retarded flux push (12.1); `-grad(A)` alone gives the rest force along and `gamma` across (17.6 M4) | the magnetic part of the push, which needs the source's velocity: `source-velocity-v1` (a row carrying its source's momentum label), named, not designed; NOT in covariant-readings-v1 | none until then; the geometry when it comes: 12b.2's thrown orbit at beta 0.43 or above, the extents' ratio 0.903 within one Link on 26 (17.6 M5) |
| E4 | Doppler with `gamma`, `1 + z = gamma (1 + beta)` | D (the count `1 + beta`, 2.2; NATURE 4b) | the crossing count per interval, exact | the count charged per self-creation, the cadence of 17.6's M1 (no separate rule), covariant-readings-v1 | `coasting_none`'s `s_mz2` at its declared momentum: `z = 0.369 +- 0.003` (0.315 on a re-declared momentum, 17.6 M2) |
| E5 | `E = m c^2`, the inertia of energy | not reached (4.5, 12.4) | `E = h f` for a row; the content and the momentum of a body untied | `E'_0 = Q S M` forced by the Newtonian limit, `W` gaining `Q S (2 E'_0 + Q S dM) dM` on a change of content, the load-time identity `3 h n = Q S d` (17.6 M3, M7), covariant-readings-v1 | a lamp emitting two opposite units keeps its pace, its `W` falling by the content identity's `Q S (2 E'_0 - Q S h s) h s` per unit paid (whether that equals the rows' energy on one c is the exchange's accounting, withdrawn until derived, 17.6 N5); the identity check a diagnostic line at load, a refusal only where the world declares the accounting |
| E6 | the invariant `E^2 - p^2 c^2 = E_0^2`, `v = p c^2 / E`, the velocity addition | D (`v = p / (m + p / c)`, 4.4) | the drive's rational form, first order off Newton | `W = E'_0^2 + 3 p . p` exact and `E'` by comparisons (17.6 M3): the discrete form is exact by construction, the open item of 17.1's note closed; the pace `p / E'`; form B's directional accumulator without the cap term (M8) | `E'^2 <= W < (E' + 1)^2` at every interval of a pinned run; the composition of two throws by momenta within the grain |
| E7 | the field of a moving charge (Heaviside), the magnetic term | D (12.1, 12b.1: the flux along `n_ret`; the count's number right, the field short) | the age moment is the Lienard-Wiechert potential exactly (12.1); its gradient across the six Ports gives `-grad(A)` only (17.6 M4) | the magnetic part: `source-velocity-v1`, named, not designed; NOT in covariant-readings-v1 | none until then; under `-grad(A)` alone the co-moving pair's pushes are the rest force along and `gamma` times the rest across, pinned as such |
| E8 | Poisson's equation, the field of a source | R (5.1) | the age moment, sourced by the release | nothing | series E (GAMEBOARD, the probes' reading): `k_a r = 36.1`, `k_s r^2 = 41.5` |
| E9 | the gravitational redshift at first order | R (5.2) | the owed count on the age moment, `1 / (1 + k_a)` | nothing | series E's (GAMEBOARD, the probes' reading) shells |
| E10 | Newton's geodesics (the retarded inverse square, the orbit) | R (3.3, 5.3) | the push and the drive | nothing | series D's orbit; `push_m = m push_1` |
| E11 | the second-order redshift, `sqrt(1 - 2 G M / (r c^2))` | D (5.2: `1 / (1 + k)` at second order, no horizon) | a clock slowed by what it reads, linear in the crowd | the field's self-source: the rows in flight as sources of rows (the content in flight gravitates), `field-source-v1`, not decided | the strong-field probes k = 2 .. 9 of series E re-read: the rate `1 - k + k^2 / 2 - ...` against `1 - k + k^2 - ...` |
| E12 | the perihelion advance, `6 pi G M / (c^2 a (1 - e^2))` | not reached (5.6: post-Newtonian terms) | the retarded push gives the drift and the decay of 12b.2, not a precession | one sixth from the velocity terms of covariant-readings-v1 (the special-relativistic advance), five sixths from the field's nonlinearity, `field-source-v1` | the thrown orbit's apsidal drift per turn in the Newtonian regime: `pi beta_orbit^2` per turn from the readings alone (one sixth of Einstein's), the rest after the self-source |
| E13 | the bending of light, `4 G M / (c^2 b)` | D (5.4, NATURE: series K's 0.000; the meeting key `~ M / b`) | the flight blind to the crowd | a rule on the LINEAR block: the row's wall reading the age moment (`optical-v1`), giving the delay's half, `2 G M / (c^2 b)`; the space half needs the second-order field | series K's beam at b = 6: a deflection of `2 G M / (c^2 b)` under the wall alone, `4 G M / (c^2 b)` with the field's second order |
| E14 | the Shapiro delay | D (5.4) | no delay in time on `main` | the same `optical-v1` | the lensing world's round trip lengthened by `(2 G M / c^3) ln(4 r_1 r_2 / b^2)` |
| E15 | the equivalence principle for a bound body | D (19.5: the release reads the held content) | the source's rows from the held content, `M_A` cancelling for a free body (3.3, exact) | the release reading the body's OWN `E' / (Q S)` (17.6 M6), inside covariant-readings-v1; the energy in flight `field-source-v1` | a thrown body beside a probe of content 1: the probe's push against the body's drive, 1 at rest and `gamma` in motion; the binding fraction E16's |
| E16 | the self-gravitation of the field's content | not reached | the rows carry no source | `field-source-v1` (rows in flight releasing, or the wall reading the presence) | E11's and E12's numbers |
| E17 | the tensor source (the stress as a source) | D (record 196: the order-2 moment is read, the push uses the flow) | the reading **R** returns the traceless second moment | the push reading the order-2 moment as well, a column of the coupling (`tensor-source-v1`) | a moving crowd's push on a probe differing from a static crowd's by the stress term |
| E18 | the cosmological term, `q_0 = -0.53` | D (15.4: Milne's 0) | the growing wall at a constant H | a rising H, a second declared rate under `expansion-v1` | the 24 stars' `z(tau)` with `q < 0` against the register's bracket |
| E19 | the relativistic dispersion of a massive quantum, `E^2 = m^2 c^4 + p^2 c^2` as a wave (Klein-Gordon) | not reached on `main` (every row flies at c, 4.1's `omega = c k`) | the rows' massless wave equation (4.1, 5.1) | `massive-rows-v1` (section 23): the row's wall `E' = isqrt(E'_0^2 + 3 p . p)`, the time-independent form exact, the temporal phase not carried | `slits_matter`'s bands at 36.5, 60, 83.5 and the centre's first click at `1 + 828` (23.3) |

**Read across**: the special theory is one hypothesis away
(covariant-readings-v1, rows E2 to E7 and E15), the exact discrete
proof of its invariant the one open mathematical item; the general
theory's first order is reached (E8 to E10) and its second order needs
the field to be its own source (E11, E12, E16) and the rows to read the
field (E13, E14), two named readings on the two blocks, neither
decided; the tensor source and the cosmological term are separate
declarations. Nothing enters the law by this table.

### 21.5 The standard, and the new rows under it

**The standard** (record 300; the owner: "see how other papers do these
things so that it becomes a standard"). The papers that derive a
continuum law from one lattice rule state six things per formula, and
each has its place in this document: (1) the rule, the verb on the
state and its premises (section 1's inventory; the Chapman-Enskog
derivation of Navier-Stokes from the lattice gas starts from the
collision and the streaming rule, Frisch, Hasslacher and Pomeau 1986,
Phys. Rev. Lett. 56, 1505); (2) the limit taken (the Link to zero, many
rows, large N, small momentum: the continuum limit of a lattice field
theory, Wilson 1974, Phys. Rev. D 10, 2445); (3) the order of the
expansion; (4) the symmetry the result needs (the square lattice fails
the isotropy Navier-Stokes needs and the hexagonal passes, Frisch,
Hasslacher and Pomeau's finding; here the cube's 48, the fan and the
circle, records 225 and 226); (5) the error term, what the next order
gives with the grain (the lattice Boltzmann method's stated truncation,
Qian, d'Humieres and Lallemand 1992, Europhys. Lett. 17, 479); (6) the
numerical check against a value pinned before the run (this
document's rule, record 205). 21.2 now carries (3) and (5) as two
new columns for every row, and (6) as the column "the pin before the
run" (record 316: for every formula, how it was reached, by the pin
method first; the column states the number the register held before
the run with its source, "no pin; a host reading" where a script read
the register after the run, and "no pin; the run's own reading" where a
run was registered without a written expectation) ("not stated" with a note where the section
does not state them; no new derivation for the old rows); the rows
below are new, each under the six points, the three tests and the pin.
Nothing enters the law by them; a row that needs more than the six
verbs is named under its own identity.

**47. Gauss's law and the continuity of the field.** (1) The rule: the
release (T) and the flight (T), the presence read as the zeroth moment
(B), the books' exact accounting of every unit. (2) The limit: the fan
of every direction, many rows, the shell mean. (3) The order: exact at
every instant on the lattice (the amount crossing a closed surface per
interval is the release inside it, 5.5); the continuum form `div(g) =
-4 pi G rho` at the leading order of the shell mean. (4) The symmetry:
the fan's 48 for the shell mean, none for the flux count. (5) The error:
the fan's grain, the ring flux `r^-1.83` on the 2616-direction fan
against `r^-2` (7.2) and the shell's Node-count ripple (3.2). (6) The
check: series E's `k_s r^2 = 41.5` (39.0 to 44.8 over r = 6 .. 14), a
GAMEBOARD reading of the probes. The
three tests: pass (the law's own reading). **R.**

**48. The wave equation of the field.** (1) The flight at c and the age
moment (T, B). (2) The Link to zero at fixed c, many rows. (3) Second
order in the Link (the lattice's second difference). (4) The cube's 48
for the second-order isotropy; the fourth-order term is the cube's,
anisotropic (the same finding as the lattice gas's on the square
lattice, here at the next order and not at the leading one). (5) The
error: the anisotropic term of order `(k x Link)^2` in the dispersion,
not stated in 4.1 or 5.1; the flight table's per-direction pace `Q S_1
/ T_D` (1.5 percent above `1 / sqrt 3` on a heading) states it. (6)
Series K's ages 89.40 in every world; 12.1's retarded potential to
`10^-15`. **R**, with the error term named for the paper.

**49. Faraday's and Ampere-Maxwell's equations, the field of a moving
charge with its magnetic term.** (1) The scalar potential is the age
moment (12.1, exact in the limit); the vector potential needs the
source's velocity, which no row carries (17.6 M4). (2) The limit: every
direction, the retarded time. (3) With both retarded potentials in the
Lorenz gauge, the four equations follow identically (Jefimenko's form of
the retarded solution): the order is the potentials'. (4) Lorentz's
symmetry, the limit's. (5) The error: the age's integer (the retarded
time to one interval) and the fan's grain. (6) 12.1's potential to
`10^-15`; the pair's transverse push `1 / gamma` when **A** exists. The
three tests: pass for the age moment; the vector potential is not a
local reading of the rows as they are. **H**, `source-velocity-v1` (a row
carrying its source's momentum label at release, one declared
component, local to the row, generic): Gauss and the wave equation are
the law's, Faraday and Ampere-Maxwell wait for **A**.

**50. The Lorentz force `q (E + v x B)` and Biot-Savart.** (1) The push as
`-grad(A)` across the six Ports (17.6 M4, the electric part without the
induction term), `q v x B` from **B** = curl **A**. (2) Every direction,
small Link. (3) First order in the Link for the six-Port difference. (4)
The cube's 48 for the gradient's isotropy. (5) The error: the central
difference's `Link^2` term. (6) The pin: on the deuteron's fan at k = 4
the transverse push `1 / gamma` of the rest and the longitudinal `1 -
beta^2` under **A**; without it the rest force along and `gamma` across
(17.6 M4). Biot-Savart is the magnetostatic limit of the same **A**
(`B = (mu_0 / 4 pi) integral of J x r / r^3`), the steady current a crowd
of rows carrying one velocity label. **H** for both, the same identity
as 49; the electric part under covariant-readings-v1.

**51. Planck, `E = h f`.** (1) The release: a lamp pays `h s` per unit at
a turn of s steps (6.4). (2) None: an identity at every birth. (3) Exact.
(4) None. (5) None. (6) The Bell lamps paying 2 per birth and stalling
once at tick 4 (159 births in 160); L1's lamp at `2^20` paying 1. **R**,
an identity of the release.

**52. De Broglie, `lambda = h / p`.** (1) The turn by momentum under
`action`: at every Link stepped the phase turns `abs(p) N / h` steps
(7.2), so a whole circle of N steps closes every `h / abs(p)` Links. (2)
None: an identity of the declared turn. (3) Exact, to the floor. (4)
None. (5) The floor's one step per Link (`1 / N` of a circle). (6) Series
H's closure `2 pi p r = j h` on the digital circle, 2.041, 2.011, 2.003,
2.000 times `pi p r` at r = 8, 16, 64, 256. **R** as an identity under
the `action` key (bohr-v1, declared); the wavelength of a body is its
phase per Link, not a wave on the lattice (row 57).

**53. Boltzmann, `S = k log W`.** (1) Section 14's definition: the
entropy of a record is the logarithm of the torus points consistent
with the click list. (2) None: a count. (3) Exact. (4) None. (5) None;
`k_B` is the conversion of bits to joules per kelvin (16.1). (6) The
registered `mz_equal` 0 / 6, `mz_quarter` 1 / 5, `mz_345` 0.116 / 5.884,
`slits_low` 3.425 / 2.575. **R**, a theorem of the count.

**54. Shannon, and Landauer.** (1) Shannon: bits read `H = -sum_k (w_k /
N) log2 (w_k / N)` per click, bits read plus bits erased `= log2 N` per
record (14). Landauer: the click's erasure of `log2 N - H` bits against
the bound `k T ln 2` per bit. (2) None. (3) Exact (Shannon). (4) None.
(5) None. (6) `slits_low` 3.425 read and 2.575 erased. Shannon **R**;
Landauer **D**: the law has no temperature, the click erases at no
energy (record 140: "Landauer out"), and the bound is not a formula of
the law until a temperature is (a thermal balance, 16.4's last row).

**55. Hubble's law, `z = H d / c`.** (1) The growing wall of the flight,
`2 T_D a` with `a = H_den + H_num x tick` (15.2, the tick wall). (2) The
first order in `H d / c_0`. (3) First; the full form `1 + z = e^(H d /
c_0)` (Milne) with the second order `(H d / c_0)^2 / 2`. (4) None (the
wall is isotropic by construction); the tick as a count every Node
shares (15.2's local question). (5) The error: the second order, and the
accumulator's integer (one part in 400 at H = 1 / 400). (6) The 24 stars
at rest under the wall: rms 0.0044 at T = 440 (15.4); the birth-tick
wall's linear form fails the far stars (rms 0.08). **R** for the form
under `expansion-v1` (the identity, 20.4), the value of H an input.

**56. The aberration of light.** (1) The aberration rule of 12.2: the
released direction is the fan's plus the body's velocity, `w = Q W D +
T_D N_v`, brought to the nearest direction by the comparison (T, D). (2)
Every direction, small beta. (3) First order in beta: Bradley's `tan
theta' = sin theta / (cos theta + beta)`, the angle beta at the
transverse (20.5 arcseconds at the Earth's `10^-4`); the relativistic
form has `gamma` in the denominator, a difference at order `beta^2`. (4)
The fan's grain: the nearest direction by comparison. (5) The error:
`beta^2 / 2` against nature's form, and the fan's grain `1 / P`. (6) The
pins of 12.2: the counts 304 / 116 / 157 per cycle at k = 4 (not run).
**R** at first order, **D** at the second; the rule is a hypothesis of
12.2 (the aberration rule, decided with form B).

**57. Schrodinger's equation for a free particle.** (1) The pair (flight,
phase) of the linear block: a row's phase advances per interval by its
family's rate and per Link by its declared turn; a body's phase turns
`abs(p) N / h` per Link stepped (row 52). (2) The Link to zero, many
rows. (3) The rows' limit is the wave equation with `omega = c k`
(massless, row 48); a body's phase along its path is de Broglie's, but
the body is ONE record on one line, not a field on the lattice: there is
no `psi` whose second difference the law takes. (4) Would need the
cube's 48 for the Laplacian's isotropy. (5) Not applicable. (6) None.
**Not reached** (D): `i hbar d psi / dt = -(hbar^2 / 2 m) Laplacian(psi)`
needs a massive dispersion `omega = hbar k^2 / (2 m)` of rows, which the
flight table does not have (every row flies at c); what would state it
is a family of rows whose pace reads their phase per Link (a dispersion
in the flight's wall, `dispersion-v1`), named, not designed; the caveat
stands: the law has no wave on the lattice, it has rows and one click.
Section 23 checks the named family on paper (`massive-rows-v1`, row 60):
the time-independent form reached, the time-dependent not.

**58. Kepler's three laws.** (1) The rule: the push `p += -M_A V(x)`
with **V** the flow in the shell mean (`q Q / N(r)`, radial; B, 3.3) and
the drive on the momentum's direction, form B (T; FORM.md section 3):
`v = abs(p) / (Q S M)` at small momentum, the cap c as the momentum
grows. (2) The limit: the Link to zero, small momentum (`v << c`), every
direction (the shell mean). (3) The order: the leading order in `Link /
r` and in `v / c`; the force exact in the shell mean (Gauss, 5.5). (4)
The symmetry: the cube's 48 and the shell mean's isotropy (the fan's
grain its ripple, 3.2). (5) The error term, three parts: (i) the fan's
grain, `r^-1.83` against `r^-2` on the 2616-direction shell (7.2), the
shell's ripple `+- 7` percent (3.2); (ii) form B's cap, `p = Q S M v /
(1 - v / c)`: an inertia growing at FIRST order in `v / c`, so a circular
orbit's period is the Newtonian `2 pi r / v` times `1 / (1 - v / c)`
(`s32_r24`: 795 against today's 687, the host check), and an eccentric
orbit's apsides advance at that order, not derived here; (iii) the
retarded field of a FIXED source is static and gives no precession; a
moving source's retarded push gives the drift and the decay of 12b.2,
not a precession (E12). Kepler's three laws in the limit, in space: the
ellipse (the apsidal angle `pi` of the `1 / r^2` force: closed), equal
areas (the force central: the fan's lines radial within 0.8 degrees),
`T^2 ~ a^3` with `T = 2 pi r^(3/2) sqrt(4 pi S / q)` and `G M_B = q /
(4 pi S)` (the host check: at S = 512 with series E's fan of 290
directions, T(12) = 1230 and T(24) = 3480, the ratio 2.8284 = `2^(3/2)`,
the exponent 1.5000). On the plane, where the register's orbits are
(series D), the force is `1 / r`: `T ~ r` (the ratio 2, the squares 4),
and the orbit is a rosette with the apsidal angle `pi / sqrt 2 = 127.28`
degrees, the perihelion moving by `-105.44` degrees per radial period, the
plane's own law and not the lattice's. (6) The pin, on ONE declared world:
series D's registered `s32_r24` (S = 32, r = 24, p = 576 label units, the
fixed source of content `2^10` on the plane's fan of 120 directions, q =
12 rows per interval, 4000 intervals) with ONE change so that a detector
reads it: the probe's family releases one row per direction of the same
fan every 10 intervals (the source's `release` `[1, 2^10 x 10]`; the
register's probe releases at the age 10240, beyond the run) and the
source is a detector of one Node with `measure` on the probe's family;
named `s32_r24_lamp`, to be written, `s32_r12_lamp` beside it. The
DETECTOR reading is the source's click list of the probe's rows, whose
arrival directions turn with the probe. Under form B: the period T, the
recurrence of the arrival direction's angle, 795 (the analytic `2 pi r /
v` with `v = 288 / 1519 = 0.1896` on a heading and 0.1893 on the
diagonal, the host check) within the continuum's own margin, 700 to 830
(12b.2's integrated at-rest periods 743 and 718 against the analytic 795,
the 9 percent the burst field and the fan's grain owe); the mean radius
from the clicks' ages, `r = age x c` per direction, `23.6 +- 1` (the
register's 23.63 under the step drive; the continuum's extents 22.7 by
23.8); the precession: the direction of the age's minimum moving by
`-105 +- 15` degrees per radial period (the polygon's kicks, 6.4 degrees
per ray); the exponent: `T(24) / T(12) = 2.00 +- 0.15` with
`s32_r12_lamp` (analytic 397.7 and 795.3), the exponent 1 on the plane,
`3 / 2` being space's. **Amended for the lamp worlds as written** (the
physicist, the branch `claude/series-m-masses`, `lamp_orbits_map.py`):
the circular momenta re-derived under the directional drive, n = 10 at S
= 32 (640 label units per unit of content; the kept 576 was today's
rule's), so T = 784 (714 to 855) at r = 24 and 392 (357 to 428) at r =
12, the mean radius `24.8 +- 1` and `12.4 +- 1`, the precession `-81 +-
15` degrees per radial period at both radii, `T(24) / T(12) = 2.00 +-
0.15`. The precession is checked here by the closed form of a
near-circular orbit under a dispersion: with the push on the momentum
and the pace v(p) along it, the radial frequency is `(v_0 / r_0) sqrt(1
+ e)` against the angular `v_0 / r_0`, `e = d ln v / d ln p` at the
circle, so the apsidal angle is `psi = pi / sqrt(1 + e)`: e = 1 gives
the plane's `pi / sqrt 2` and `-105.4`; form B's pace on a heading at n =
10 gives e = 0.651, 140.1 degrees and `-79.8` per radial period (the
physicist's integrator `-80.6` at the rosette's amplitude, within 0.4
degrees; today's per-axis pace at n = 9 gives e = 0.780, 134.9 and
`-90.2`, the integrator's `-90.5`): `-81` is right under form B's pace and
`-105` was the Newtonian pace's ([kepler_compton.py](designs/derivations_beam/kepler_compton.py)
(D)). Under FORM.md 3.1's form (c), if adopted, the pace on the plane's
diagonal at n = 10 is 13 percent below the heading's and the lamp worlds
are re-pinned. Record 131's "no closed orbit by D's criterion"
restated: the law predicts eccentric loops precessing at the `1 / r`
force's apsidal angle, bound for the run (four turns of 701 to 880
registered under the signed drive, the mean radius 26 to 36), and the
run must show the clicks' direction turning through `2 pi` with the
period above and the age's minimum advancing by the apsidal angle; the
criterion "returns within one Link" is a circle's and not this force's.
For `3 / 2` itself a world in space is named and not pinned here: the
probe on series H's 2616-direction shell (the one fan the register
resolves at r = 12 to 24), whose ring flux `r^-1.83` reads the exponent
`(1 + 1.83) / 2 = 1.42` on that fan and `3 / 2` in the limit of every
direction. The three tests: pass (the law's own push and drive). **R** in
the limit (Kepler's third law with G named, 3.3); the plane's register
**F** for the exponent (1); the lattice's own precession **D**, not
derived.

**59. Compton, `lambda' - lambda = (h / (M c)) (1 - cos theta)`.** (1) The
rule: a row of momentum k (label units; `k = h s` for a lamp's unit at
the turn s, 17.6 M7) absorbed at the body's Node (`measure`: the content
and the momentum join, the content identity of 17.6 M7 on W), then a row
released on one direction of the re-emitter's declared fan at the angle
theta to the incoming one, with the books balanced for that one row (the
exchange's accounting, 17.6 N5, declared under `books`): the released
momentum k' fixed by the exact square (B) and the momentum's conservation
(the body's recoil `p = k - k'` as vectors), the released turn `s' =
floor(k' / h)` (T, the remainder kept). From `W = E'_0^2 + 3 p . p` with
the row's energy `sqrt 3 k` in `E'` units on the pair `c^2 = [1, 3]`:
`(E'_0 + sqrt 3 k - sqrt 3 k')^2 = E'_0^2 + 3 abs(k - k')^2`, whence

    1 / k' - 1 / k = sqrt 3 (1 - cos theta) / (Q S M),   lambda = h / k Links:   lambda' - lambda = (h / (Q S M c)) (1 - cos theta),

Compton's formula with the rest `Q S M` and `c = 1 / sqrt 3`, exactly (the
host check). (2) The limit: none for the momenta (an identity of the
exact square); every direction for the angle. (3) The order: exact on
the pair; at the heading's own `c = 32 / 55` (the row's energy `(96 / 55)
k`, M7) first order in `(k - k') / k`, with the residual `(gamma^2 - 3)
(k - k')^2 / (2 E'_0 gamma)`, `gamma = 96 / 55`, `gamma^2 - 3 = 141 /
3025` (at 90 degrees `k' = 11.195` against 11.165 on the pair). (4) The
symmetry: the fan's 48 (the headings and the face diagonals). (5) The
error: the fan's grain (theta at the declared directions only, `cos theta
= +- 1 / sqrt 2` on the face diagonals), the floor of `s'` (one step), the
identity's domain `abs(p)_1 <= Q S M` (N2). (6) The pin, the declared
world `compton`, to be written: an open cube of 41 Nodes a side, S = 1,
N = 64, the key `covariant_readings` with `c2 = [1, 3]`, `grain = 1` and
`books`; a lamp of the paid family `light` (quantum h = 1) at (2, 20, 20)
releasing one unit per interval on +x at the turn s = 16 steps per
self-creation (`k = h s = 16` label units, `E = h s`); a free body of
content M = 1 (`Q S M = 64`) at the centre with `measure` on `light` and
`rerelease` on the six headings and the twelve face diagonals; the six
faces as detectors reading `light` with `reads: "age"`, the DETECTOR
reading the phase rate of the rows at each face (the `record` lines'
phase slope, `hubble_readings`' method), that is the released turn per
direction: 16 at the +x face (theta = 0, no shift), 11 at the +-y and +-z
faces (90 degrees, `k' = 11.165`), 8 at the -x face (180 degrees, `k' =
8.574`), 14 on the forward face diagonals (45 degrees, 14.199) and 9 on
the backward ones (135 degrees, 9.200), each to one step; the body's
recoil `abs(p) = 19.5` label units at 90 degrees (0.305 of `Q S M`,
inside N2's domain) a GameBoard diagnostic of its `step` lines, not the
pin. What refutes: a face reading a turn off by more than one step from
these, or the same turn at every face (the law on `main`: the released
row takes the re-emitter's declared turn, 6.4, no shift). The three
tests: generic (no name), vector (B, T, D), local (the body's record and
its Node). **H** under covariant-readings-v1 as amended, with the
exchange's accounting of N5 (Compton is exactly the books' balance for
one row in and one row out); **D** on `main`. The run after
covariant-readings-v1 is built.

## 22. The uncertainty relation from the six verbs, and Bell beside it

**The owner's direction** (records 291 and 292, translated: "let them
derive all of Einstein"; "confirm all of them, and also Heisenberg and
the uncertainty principle, and Bell"). The host script
[uncertainty_lattice.py](designs/derivations_beam/uncertainty_lattice.py)
with its output
[uncertainty_lattice.out](designs/derivations_beam/uncertainty_lattice.out)
makes the numbers; no run.

### 22.1 The conjugate pair on the torus, and what the six verbs give exactly

**The pair.** A record is the vector **f** of `Z[Z_N]` of the amounts
that ended at each phase (section 0; 6.7); its position is the Node its
rows ended at (a cell of the ladder, the click's one read-out), its
momentum the label with the phase per Link `abs(p) N / h` (the turn by
momentum, 7.2: the wavelength `lambda = h / abs(p)` Links, de Broglie's
relation as the declared turn) and, for a row, the direction of the fan.
The click evaluates **f** at the N-th roots of unity (E) and weighs the
result by the Gram form (B, 6.5): the evaluation is the discrete Fourier
transform on the circle `Z_N`, and the position and the phase are the
two sides of one transform.

**What is exact, from the transform alone (R).** (i) The support
bound: a record whose rows end on s phases has an evaluation supported
on at least `N / s` of the N roots, `abs(supp f) x abs(supp f_hat) >= N`
(Donoho and Stark 1989, SIAM J. Appl. Math. 49, 906, for any finite
cyclic group), checked by enumeration at N = 64 on the register's records
(the script's (A)): one phase gives all 64 roots, the antiphase pair 32,
a comb of every eighth phase 8 (the product 64 exactly, the equality
case), a run of 8 phases 57. No hypothesis: it is the Fourier
transform's, and the law's click is that transform (E and the norm, the
one imported law, BEAM_LAW section 5). (ii) The Weyl relation: the shift
by one phase U and the multiplication by `omega^y` V on `Z_N` satisfy `V
U = omega U V` with `omega` the primitive N-th root (the script's (B),
exact to `10^-15`): the finite commutator of position and momentum on
the torus, the algebra from which the continuum's `[x, p] = i hbar`
follows as `N -> infinity` with `hbar = h N / (2 pi)` per 6.4's `E = h
s = (h N) f`. Both pass the three tests trivially: no name, the
evaluation verb and the group ring, the record's own vector.

**What is a limit (R as a limit).** The variance form `Delta x Delta p
>= hbar / 2` (Kennard 1927; Robertson 1929 for any pair) follows from
(ii) by Cauchy-Schwarz on the Gram form of 6.5 (a positive quadratic
form on the record vector, so the Robertson argument runs verbatim
with the finite commutator) in the limit `N -> infinity` of a record
spread over many phases; at finite N the bound is the finite group's
(the entropic form of Hirschman and of Maassen and Uffink: the sum of
the two Shannon entropies at least `log2 N`, which is section 14's
identity "bits read plus bits erased = `log2 N` per record" read for
the conjugate pair), and the Gaussian equality case does not exist on
`Z_N`. **So**: reached exactly in the support and entropic forms, as a
limit in the variance form, with `hbar` the world's action times the
circle over `2 pi`; nothing is added to the law, and no hypothesis is
named.

**What makes it an uncertainty and not a spread.** The click reads ONE
cell of one record (Definition 3, 6.1): a record read at a Node gives
its position and erases its phase vector (14.2: `log2 N - H` bits
erased), and a record read on the fan's angle (the far screen) gives
its momentum's direction and not the Node it came from. The two are not
jointly readable because there is one read-out, the same reason the
law has no hidden joint distribution for Bell (below); the reading, not
the GameBoard, is what is uncertain (Highlights 5.4, A10's premise).

### 22.2 The pin for A10 under the one click (NATURE row 10), before any run

The single opening of width w Nodes, one emitter per Node re-emitting
on a fan, read on a screen L Links behind: the record's weight in `s =
sin theta` is the array factor `[sin(pi w s / lambda) / (w sin(pi s /
lambda))]^2` (the transform of a run of w phases, 22.1 (i)) times the
fan's angular density (3.2's `N(theta)`, the grain). Its full width at
half maximum is `0.886 lambda / w` for `w >= lambda` (the Fraunhofer
constant), so the dimensionless product is

    w x FWHM(sin theta) / lambda = 0.886      (the far field, the fan of every direction).

At the registered geometry (`w27`: w = 27, L = 108, `lambda = 8 c` with
`c = 32 / 55` on `main`, 4.655 Links; the Fresnel number `w^2 / (lambda
L) = 1.45`) the exact sum over the 27 emitters at L = 108 on the 161
pixels gives 0.916 (the script's (C)): the near field at Fresnel number
1.45 widens the lobe by 3.4 % over Fraunhofer's, which is the whole
correction the geometry owes; the crowd form read 1.08 (NATURE row 10,
kept as history), whose 22 % the sparse fan explains (47 directions,
spacing 0.083 in s, half the FWHM: a lobe of two directions). **The
pin**: under the one click on `w27` with the fan of every direction
(the screen's fan by angle, record 155's 1423 directions, spacing
0.0026 in s), the record's clicks over the 161 pixels give `w x FWHM /
lambda = 0.92 +- 0.03` (0.916 by the exact sum; 0.886 in the far-field
limit `L -> infinity`), the count of plain clicks per pixel the fan's
profile at every w (the control, unchanged), and at w = 9 (Fresnel
number 0.16) the product `0.886 +- 0.03`; what refutes 22: a product
below 0.85 at any width at or above `lambda`, or one that does not fall
toward 0.886 as L grows.

### 22.3 Bell, beside it

Bell's inequality is not derived here because it is already registered
and derived: 6.2's `S(N, Q)` at the CHSH labels from the rungs and the
tables, `176 / 64 = 2.75` at N = 64 (NATURE row 1a, PASS at 1.65 standard
errors), `181 / 64 = 2.828` from N = 512 to 8192 (the plateau, 24.4), `S -> 2 sqrt 2` with the bound
`8 / N + 16 arcsin(sqrt 2 / (2 Q))`, Tsirelson's bound reached as a
limit, the marginals exact (`32 / 64` in all 4096 setting pairs, no
signalling), and the reason it is not a hidden-variable value: the one
read-out per record of 22.1, a record of two rows read at two detectors
with one Gram weight over both. What is proven: (1) on the tree, the
pair's weight at the settings (a, b) is ONE Gram form of the record's
evaluation (E, then B; 6.2, 6.5), quadratic in the record vector **f**
with cross terms between its cells, where a mixture over the cells is
linear in **f** with weights that do not depend on the settings
jointly; (2) in mathematics, a joint probability distribution over the
four outcomes of two settings a side exists if and only if the CHSH
inequalities hold (Fine 1982, Phys. Rev. Lett. 48, 291), so the
registered `176 / 64 = 2.75` has no such distribution. What is NOT
proven on the tree: that the quadratic form's excess over 2 is "the
same Fourier fact as the support bound" of 22.1 (i); that phrase is
withdrawn. The support bound is Donoho and Stark's on one vector's
transform; the Bell excess is a statement about a quadratic form of two
evaluations against every mixture, and no derivation of the one from
the other is written here. **R** for `S(N, Q)` and its limit, as
registered; the relation between the two facts not proven on the
tree.

### 22.4 The verdict of section 22

The uncertainty relation is reached from the six verbs: exactly in its
support and entropic forms on the circle `Z_N` (the evaluation verb is
the Fourier transform), exactly in its algebra (the Weyl relation, the
finite commutator), and as the limit `N -> infinity` in Kennard's
variance form with `hbar = h N / (2 pi)`; the one read-out per record is
what makes it an uncertainty; A10's pin under the one click is `0.92 +-
0.03` at the registered geometry and `0.886` in the far field; Bell is
registered at `176 / 64` and derived as a limit at `2 sqrt 2`. No
hypothesis; the three tests pass.

## 23. Schrodinger's equation: the massive row, and what its linear block reaches

**The owner's question** through the paper coordinator (record 331,
translated: "can Schrodinger's equation be reached?"). The coordinator's
route is checked here on paper under the identity `massive-rows-v1`,
named and not built: a family of massive rows carrying a momentum label
**p** and a content M, flying at the covariant pace `p / E'` with `E'^2
= E'_0^2 + 3 p . p` (17.6 M3) in place of c, and turning de Broglie's
`abs(p) N / h` per Link (7.2): row 57's "family of rows whose pace reads
their phase per Link". The host check
[massive_rows.py](designs/derivations_beam/massive_rows.py) with its
output [massive_rows.out](designs/derivations_beam/massive_rows.out)
makes the numbers; no run. Nothing enters the law.

**Notation, once.** **p** the row's momentum label (label units) and p
its magnitude; M the row's content (units); `E'_0 = Q S M` its rest
energy in the identity's units and `W = E'_0^2 + 3 p . p` the exact
square, `E'` the largest integer with `E'^2 <= W` (17.6 M3); h the
world's action (the `action` key, 7.2); N the circle; **x** a Node's
position (integers); **k** the wave vector of the continuum limit, `k =
2 pi p / h`, and lambda `= h / p` the wavelength in Links; psi the wave
function of the continuum limit (a field of the limit, never a state of
the lattice); m the mass and `hbar = h / (2 pi)` with h the action (`h =
h_q N`, the quantum times the circle, 6.4's dictionary and 24.1 row 25;
the constants of 16.1); L a path's length in Links; V a potential.

### 23.1 The massive row, and the three tests

**The row.** Today's row (BEAM_LAW section 2: a direction **D** of the
fan, one Manhattan accumulator against the wall `2 T_D`, a phase that is
a step of `Z_N` turned by the family's rate) with three more declared
integers on its record, **p**, M and, at its birth, `E'` (by `isqrt` at
the birth, the class of `T_D`'s load-time rounding, exactly as 17.6 M3's
initial `E'`), and two changes of rate:

- (a) the flight: the accumulator's rate `abs(p)_1` and its wall `E'`
  (integers; the deficits of the digital line as today), so the
  Manhattan pace is `abs(p)_1 / E'` and, with **p** `= k D` along the
  row's own line, the Euclidean pace is `k abs(D) / E' = p / E'` on every
  direction, exact in the mean, isotropic without `T_D`; the cap is the
  square's own: `E'^2 >= 3 p . p` gives `p / E' <= 1 / sqrt 3` for every
  **p**. The photon is the case `E'_0 = 0`: then `E' = isqrt(3 p . p)`,
  and at `p = Q D` this is `isqrt(3 Q^2 abs(D)^2) = T_D`, today's flight
  table to the integer: ONE primitive for every row, massless or massive,
  the wall `E' = isqrt(E'_0^2 + 3 p . p)`, today's `T_D` its `E'_0 = 0`
  member (the map's (A): `E' = 4113` at `E'_0 = 4096`, `p = 220`).
- (b) the phase: at every Link stepped on the axis a the phase turns by
  `by_drive(acc_turn, abs(p_a) N, h)` steps (7.2's turn by momentum, the
  body's rule of `engine.py:637`, on the row), and by NOTHING per interval
  of age: the massive row carries no frequency in flight (the design's
  choice; why, in 23.2; its price in 23.5). On a monotone digital line
  the sum over the Links stepped of `abs(p_a)` is `p . (x - x_0)` exactly
  (each axis Link adds `abs(p_a)` and the line never turns back), so the
  phase at the Node **x** is

      phi(x) = phi_0 + (N / h) p . (x - x_0)      (the floor's remainder kept on the accumulator),

  the plane wave `exp(i k . x)` on the lattice's Nodes with `k = 2 pi p /
  h`, the wavelength `h / p` along **p**: de Broglie's, exact on the
  Nodes to the accumulator's remainder.

**The three tests.** Generic: one primitive per rate (the accumulator with
declared integers **p**, M, h), no family name and no kind, the massless
row the same primitive at `E'_0 = 0`. Vector: T (the flight's
accumulator and the turn's), B (the square `W`), D (`E'` by comparisons
at the birth); no root at run time (the one `isqrt` at the birth, the
class of `T_D`). Local: the row's own record; a free row reads nothing
of any Node. Pass.

### 23.2 The continuum limit of the massive linear block, under the six-point standard

(1) The rule: 23.1. (2) The limit: the Link to zero, many rows, the fan
of every direction; for Schrodinger also `p << E'_0`. (3) The order, (4)
the symmetry and (5) the error term below; (6) the check is 23.3's pin.

**The derivation.** A record's rows born at the Node **x**_0 at one
phase `phi_0` (the lamp's wheel) with one magnitude p on the fan's
directions: the row of direction **D** reaches the Nodes **x** with `x -
x_0` along **D** at the phase `phi_0 + (N / h) p abs(x - x_0)`, so over
the Nodes reached the phases form the spherical wave `exp(i k abs(x -
x_0))` of wave number k, its amplitude the fan's angular density (3.2's
`N(theta)`, the grain); two openings give 7.1's two-path law with
`lambda = h / p` in place of `c N d / n`. Every row's phase is a plane
wave `exp(i k . x)` along its line, and the linear block adds rows
without reading them, so in the limit of small Links the field of the
rows present obeys

    Laplacian(psi) + k^2 psi = 0,   k = 2 pi p / h        (Helmholtz),

which is (i) the time-independent Klein-Gordon equation at the energy E:
with `E = E' / 3`, `m c^2 = E'_0 / 3`, `c^2 = 1 / 3`, `p = hbar k`, the
relation `E^2 - m^2 c^4 = p^2 c^2` is `E'^2 - E'_0^2 = 3 p . p`, the
exact square itself: the dispersion is exact, not a limit; and (ii) at
small p the time-independent Schrodinger equation of a free particle,
`-(hbar^2 / 2 m) Laplacian(psi) = E_kin psi`, with `m = E'_0` in label
units (17.2: `p = m v` at small p) and `E_kin = (E' - E'_0) / 3 = p^2 /
(2 m) - ...` (the map's (A): `E' - E'_0 = 17` against `3 p^2 / (2 E'_0) =
17.72`, the next term `-9 p^4 / (8 E'_0^3) = -0.04`). **The click's
Gram form as `abs(psi)^2`**: at the click the cell's weight is `f^T G f =
abs(sum over the rows of amount x exp(i phi))^2` (6.7), the square of
the summed plane waves at the click's Node up to the tables' rounding,
and the ladder normalises it by the record's total (6.2): Born's
`abs(psi)^2` holds AT THE CLICK as the cell's probability to within `1 /
(2 N)`, and nowhere between clicks, where there is no psi on the
GameBoard, only rows.

**What is NOT reached, and why the row carries no frequency.** The
time-dependent equation `i hbar d psi / dt = -(hbar^2 / 2 m)
Laplacian(psi)` has the temporal phase `exp(-i E t / hbar)` and the
spreading of a packet. Neither is in the block: (i) a record's rows have
ONE p, so no packet disperses (the fan's other directions spread the
record in angle, not in momentum); (ii) the row turns per Link and not
per interval of age. The second is forced by the click: two rows of one
record reach a pixel at different times (their paths differ), and the
click compares the phases stamped at each row's own arrival (note 45).
If the row also turned per interval by Planck's `E' N / (3 h)`, the two
stamps would differ by `(E'^2 / (3 p)) (N / h) (L_1 - L_2)`, the PHASE
velocity's `E / p` in place of de Broglie's wave number: the fringes at
`3 h p / E'^2` Links, 0.040 Links on the declared world of 23.3, below
the Link, no fringes. So the temporal phase is not carried, which is
exactly the global factor `exp(-i m c^2 t / hbar)` that the reduction
from Klein-Gordon to Schrodinger drops, here dropped for the whole
energy: the row's frequency stays the lamp's cost at the birth (6.4, `E
= h s`, tied at the birth and not afterwards), as for the photon.

**(3) The order.** The pace exact in the mean (the accumulator's
remainder); the dispersion within a part in `E'` (`E'^2 <= W < (E' +
1)^2`: a part in 4113 on the declared world); the phase exact on the
Nodes (`p . x` an integer) to the floor's one step at the click;
Schrodinger's form at second order in `p / E'_0`. **(4) The symmetry.**
The cube's 48 (the fan, the shell mean, 3.2) and the isotropy of the
massive pace in the mean (`p / E'` on every direction, no `T_D`); the
limit equation's own group (Lorentz for Klein-Gordon, Galilei for
Schrodinger) is the equation's and not the lattice's, as in 4.1. **(5)
The error term.** The fan's grain and the wheel (7.1's list), the
digital line's staircase, the floor of `E'` (a part in `E'`), and the
temporal phase dropped, a global factor for a record born together.

### 23.3 The pin before any run

**The declared world** `slits_matter`, to be written: `slits_low`'s
plane and apparatus as `slits_huygens` runs them (the openings at y = 55
and 65, `s = 10`; the screen at `D = 44`; the screen's fan by angle; the
wheel `[2531, 4096]`; 4096 births), with the family `matter` of massive
rows in place of the photon's: M = 64 units per row and S = 1 (`E'_0 =
Q S M = 4096`), the action `h = 1024`, the birth momentum `p = 220`
label units along each fan direction, so that `E' = isqrt(16 922 416) =
4113` at the birth (`gamma = 4113 / 4096 = 1.0042`), the turn per Link
`by_drive(acc, 14 080, 1024)` (`55 / 4` steps), the wavelength `lambda =
h / p = 256 / 55 = 4.6545` Links (the photon world's `4.654`, which is
the point: the same fringes from de Broglie's `h / p` in place of `c N d
/ n`), the pace `p / E' = 220 / 4113 = 0.05349` Links per interval
(`0.0926 c`; the photon's 0.5818); 5250 intervals (the last birth's
arrivals by `4096 + 112 + 978 = 5186`: the lamp at x = 2 shoots 6 Links
to the openings at x = 8, 112 intervals at this pace, then the
opening's re-release; the count corrected by the physicist's design,
PR #539, and verified here, 5100 before it).

**The DETECTOR reading, pinned** (the screen's clicks per pixel over
the 4096 births): the bright bands centred at the pixels 36.5, 60 and
83.5 (7.1's exact two-path law at `lambda = 4.6545`: the first bright
fringe at `abs(y) = 23.3`, the pixels 36.7 and 83.3, the map's (B); the
paraxial `lambda D / s = 20.5` is not the check), within one pixel;
Pearson with the two-source cosine `0.96 +- 0.02` and the visibility
`0.95 +- 0.03` over the 4096 births on the screen's fan (record 156's
0.963 and 0.96 for the photon at the same lambda; `slits_huygens`
registered 0.891 and 0.966 on its Farey fan), dark pixels 0 to 3; the
group pace: the first click at the centre pixel at the tick `1 + 112 +
828 = 941` within 2 (the lamp's 6 Links to the opening, then the path
44.28 Links, both over `220 / 4113`; the photon's `1 + 10 + 76`), the
first-fringe pixels' first clicks between 1004 and 1091 (the map's (C)
plus the 112 of the lamp's flight).
What refutes: a band off by more than one pixel (the wavelength not `h /
p`), the centre's first click off by more than 5 intervals of 941 (the pace
not `p / E'`), or no fringes (the phase not `p . x`).

**The confrontation** (dimensionless, the form and not the units):
Jonsson 1961 (Z. Phys. 161, 454 to 474: 50 keV electrons, the slits 0.3
micrometres wide and 1 micrometre apart, 50 micrometres long) at `lambda
= 5.355` pm by the relativistic de Broglie formula (the map's (D)),
`lambda / s = 5.4 x 10^-6`, the small-angle case of the same two-path
law whose large-angle case the world above runs at `lambda / s =
0.465`; Tonomura, Endo, Matsuda, Kawasaki and Ezawa 1989 (Am. J. Phys.
57, 117 to 120: 50 kV electrons through an electron biprism, the
pattern built one electron at a time), the law's wheel building the
same bands one click per birth (`slits_huygens`, 4096 births). Both
checked against the standard sources on 2026-09-21 (the journals'
pages, the abstracts); the comparison is the fringe positions in units
of `lambda D / s` and the build-up one click at a time, never a number
in metres.

### 23.4 The potential V: what the rows must read

optical-v1's rule with the massive pace (docs/designs/gr_rows/DESIGN.md
section 3): a row at its Node reads the crowd of LOCALITY-1 (the rows
present less its own number, one interval retarded, the same set the
bodies' clock and push read) for its age moment A, and the potential
enters the exact square as the energy's shift: with `V' = kappa_c A`
(kappa_c the column's coupling, a declared rational, the sign the
column's) the local momentum **p'** on the row's direction has

    (E' - 3 V')^2 = E'_0^2 + 3 p' . p',

`E'` conserved (the row's energy the constant, as a body's in a static
field), `abs(p')` the largest integer with `3 p'^2 <= (E' - 3 V')^2 -
E'_0^2` (D, by comparisons as `E'` is, 17.6 M3 and N3), the pace `abs(p')
/ (E' - 3 V')` and the turn per Link `abs(p'_a) N / h`: the eikonal of
the Klein-Gordon equation in a scalar potential; at small p and V, `p'^2
= 2 m (E_kin - V)`, the time-independent Schrodinger equation with V.
Bohr's closure `2 pi p r = j h` of 7.2 would be its standing-wave
condition on a closed line of rows, which is not designed: the rows do
not bend (their direction is the fan's), and a bound state of rows needs
the fan re-read at every Node, optical-v1's second verb, the turn toward
the target. The free particle comes first: 23.3's pin reads no crowd; V
is named under the same identity and not pinned.

### 23.5 The price, stated plainly for the owner

A massive quantum IN FLIGHT is a RECORD of rows (born on the fan with its
content and momentum apportioned over the rows as a photon's amount is,
one click at its completion), and MATTER is a BODY after the click (the
record's content joins the measured event at the click's Node,
`measure`): a new distinction in the law, two representations of one
particle chosen by whether it is in flight or bound and clicked, with the
click as the only bridge. What it changes for the register's electron:
nothing on the register. Series H's electron is a body (content 1836 on
a set of three Nodes, pushed by the proton's crowd, stepping, its phase
turned by the action per Link) and stays one; a free electron between a
source and a screen would be a record of massive rows; the two pictures
meet at the click and nowhere else. The owner's decision, when it comes:
whether a bound electron is (a) the body of series H, on which Bohr's
levels are reached in form (7.2), or (b) a standing record of rows under
V (23.4), not designed and not pinned. Until then the law has both, and
this section names the seam.

**The owner's yes, and two words defined** (record 332, translated:
"with the electron this is the right thing to do; it works exactly by
the system's tools; a free quantum, when it is free, does not
replicate"). What "a free quantum replicates" means in the law's words:
at its birth it is a record of rows over the fan, as a lamp's birth is
(one release at the lamp's self-creation, the content and the momentum
apportioned over the rows, the birth phase stamped by the wheel); in
flight it does NOT replicate: a record's rows are born once and fly on
their lines, no row re-emits, no self-creation and no release per
interval happen to a record (a body releases its rows at every
self-creation; a record is the rows themselves), and the click gathers
it into one body. What a bound electron is under the hypothesis: a body,
as series H has it (content 1836 on a set of Nodes, pushed, stepping,
releasing per self-creation), until a design says otherwise; 23.4's
standing record of rows is that design's name and not its content.

### 23.6 The verdict of section 23

**Reached only in part.** The time-independent free Schrodinger equation
is reached in form: the massive linear block's stationary limit is the
Helmholtz equation with de Broglie's wave number, its dispersion the
exact square (the time-independent Klein-Gordon form exactly, not as a
limit), Schrodinger's at second order in `p / E'_0`, and Born's
`abs(psi)^2` the click's Gram form at the click. The time-dependent
equation is not reached: the row carries no frequency in flight (forced
by the click, 23.2), and a record has one momentum, so no packet
spreads. The potential's form is the eikonal of 23.4, named and not
derived further. The three tests pass on the massive row, with the
photon its `E'_0 = 0` case. The identity `massive-rows-v1` is named and
not built; its pin is 23.3, before any run; nothing enters the law.

## 24. The inputs ledger, the Delta P table and the one prediction the paper can carry

**The owner's order** (record 337, 2026-09-21: "check how the paper can
indeed be strengthened as a theory"). The referee's question on which
the paper stands or falls: does the physics come from **F**, or hide in
the rates **r**, the walls d, the family tables, the bilinear forms, the
matrices and the click rule; in particular "its rates are constant for a
message in transit and bilinear in the state for a body reading what
arrives": who fixed the bilinear rate; and the strongest test is a
prediction `P_U24 = P_QM + Delta P` computed in advance and measurable.
This section answers on the law as built at `main` 5cc43ae7, under the
six-point standard (21.5): every entry a fact of a section, a note or a
registered number; no run; nothing enters the law. Three labels for an
input: **DERIVED** from **F** (with the argument that forces it),
**POSTULATE** (a grain or a rule stated in one line, with what breaks
without it), **INPUT** (a declared number, with the smallest postulate
that would replace it, or "none in sight"). Three verdicts for a
difference: **refuted**, **open**, **below reach**.

### 24.1 The inputs ledger: every place physics enters the law

| # | The input | Where it enters | Label | The argument, or what breaks, or the smallest replacing postulate |
| --- | --- | --- | --- | --- |
| 1 | the GameBoard: the cubic lattice, six Ports, one carry per Node per interval (K) | AGENTS.md, section 0 | POSTULATE | the stage; without it nothing is computed; K the one constant (13) |
| 2 | the six verbs T, B, G, P, E, D and nothing else | section 1, the three tests | POSTULATE | the grammar; what breaks without it: the inventory's "NOT" list (1.3) enters the law |
| 3 | LOCALITY-1: a reader's own record and its six neighbours, fixed work for fixed K | AGENTS.md, note 47 | POSTULATE | without it the crowd is global (the deleted Q-ORACLE-1); with it every rate is a function of the arrivals |
| 4 | the bijection: every step invertible but the click (the one non-bijective read) | 6.1, 9, 14 | POSTULATE | forces the information law (9) and the entropy identity (14); without it records could be copied |
| 5 | the integer contract: bounded integers, every count an accumulator with its remainder kept | 1.2, FORM.md | POSTULATE (a grain) | a body's content is a count of units and a row's amount a count: the additivity of 24.2 (ii) |
| 6 | the cube's 48 signed axis permutations | 4.1, FORM.md section 3 | DERIVED | the symmetry group of input 1; the law commutes with it up to the declared ties |
| 7 | the constant rate in transit: a row reads nothing of the crowd (the flight blind) | note 47 (the walk reads nothing), B7 | POSTULATE on `main`, a choice among few | the alternative is optical-v1 (the wall reads the age moment; BUILDABLE, record 323); what it forces: the superposition of rows (5.1's linearity), the retarded field, `omega = c k` (4.1) |
| 8 | the bilinear rate of a body's reading: `r = C a`, the reader's columns against the first moment of the arrivals | note 47 (the one reading, the moments of order 0, 1, 2 and the age), 3.3, 0 | DERIVED from 5 and 7 | forced by two additivities, proved in 24.2; the choice among few is WHICH moment (order 0, 1, 2 or the age) and the columns' values (row 18) |
| 9 | `c = 1 / sqrt 3` Links per interval, the cap of every pace | 13.2 (a), record 186, 23.1 | DERIVED | the operator norm of the flight: `S_1 Q <= T_D` is Cauchy-Schwarz on the Manhattan accumulator, equality on the body diagonals; the cap of a massive row the exact square's own |
| 10 | `32 / 55` on an axis (the crossing rule's count) | 2.7, note 48 | DERIVED given Q | `T_D = isqrt(3 Q^2)` at Q = 64: c rounded by the grain Q (input 14) |
| 11 | the factor 3 in the dispersion `E'^2 = E'_0^2 + 3 p . p` | 17.6 M3, 23.2 | DERIVED | `c^2 = 1 / 3` from input 9, declared as the pair `[1, 3]` |
| 12 | the click's form: the square of the evaluation, `f^T G f` | 6.5, 6.7 | DERIVED up to the Galois coefficients `c_j >= 0`; `c_1 = 1` a POSTULATE | 6.5's theorem: rotation invariance, the balanced splitter's conservation and non-negativity force a positive quadratic form `sum c_j abs(sigma_j f)^2`; Born's member `c_1 = 1` is the one imported law; Malus bounds the others (24.3 row 4) |
| 13 | the tables C, S at the scale 256 (the click's rounding) | core/phase.py, record 328 | POSTULATE (a grain) | an input of the law beside Q, S, N by the owner's word; what it costs: the norm a part in 276 (6.2), the 22.5-degree chain (24.3) |
| 14 | Q, the label's scale (64) | 2.1, 13.3 | POSTULATE (a grain) | sets c's rounding per direction (24.3 row 5); the limit `Q -> infinity` isotropic |
| 15 | N, the circle of phases (64, 4096) | 6.2 | POSTULATE (a grain) | Born within `1 / (2 N)`, `S(N)` within `8 / N`; the limits are the formulas |
| 16 | W, the birth wheel, and the coordinate u | 6.2, note 46 | POSTULATE | the click's coordinate on the ladder; without it no click chooses; its form (the bit-reversed ordinal, the golden rate) a design among few |
| 17 | P, the fan's grain, and the angle weights | record 160, 163 | POSTULATE (a grain) | Huygens' weights derived from P (`3 Q^2 / (T_d T_d')`); the shell ripple and `r^-1.83` are its cost |
| 18 | the family table: the content M, the quantum h, the charge rho, the strong column sigma, the lifetime L, the phase rate n / d, the hand | families.json, record 189 | INPUT | M: none in sight (a count on Z, 16.2 (g)); h: the family's quantum `h_q` and the world's action `h_A` one constant by the calibration `h_A = h_q N` (row 25, 6.4), its value none in sight; rho: the floors per kind constrain it (16.2 (d)); sigma, L, n / d: none in sight; the hand's structure the 48's pseudoscalar (DERIVED), its value INPUT |
| 19 | S, the width (what carries G) | 3.3, 16.2 (e), S_AND_A0.md | INPUT | none in sight: every candidate refuted or a relabelling |
| 20 | the drive, form B (the flight's accumulator at the momentum's fraction) | FORM.md section 3, 17.2 | POSTULATE among few | form A or B (record 186); Newton's limit fixes the small-p form, input 9 the cap; the first-order departure from `p = m v` is its cost (24.3 row 8); covariant-readings-v1 replaces it by the exact square (H) |
| 21 | the collision table (a permutation per class) | 1.2 step 3 | POSTULATE among few | conservation forces a bijection of the slots; the cyclic shift is the design's choice |
| 22 | the crossing rule (a row and a body meet once) | note 48 | DERIVED given 7 and 20 | the count of crossings of two digital lines (record 158); the receiver's Doppler its consequence (2.7) |
| 23 | the detector's declarations: the threshold, the window, `measure`, `pass`, `read`, `rerelease` | BEAM_LAW section 5 | POSTULATE (the apparatus) | the reading is the apparatus's, never the GameBoard's (Highlights 5.4); a branch on a declared verb, not on a name |
| 24 | the exact phase at the click (note 45) | 11.1 | DERIVED | a function of the row's age and direction at a constant rate |
| 25 | the dictionary of h: the family's quantum `h_q` (paid per phase step) and the world's action `h_A` (the turn per momentum per Link) | 6.4, 7.2, 23.1; issue #553 (the external reviewer's F08) | DERIVED as a constraint on the inputs (a calibration) | one Planck constant `h = h_q N = h_A`, `hbar = h / (2 pi)`, `E = h f`, `lambda = h / p`, `k = 2 pi p / h`; the photon's `lambda = h_A / (E / c)` equals its wave's `c N d / n` if and only if `h_A = h_q N` (23.3's `256 / 55`); with 17.6's `3 h_q n = Q S d` one energy and one action; the limit `N -> infinity` at fixed h, `h_q = h / N`; CLOSED as a calibration, the value of h INPUT (row 18) |

So the physics that is NOT in **F** is short: seven grains (1, 5, 13,
14, 15, 16, 17), three rules chosen among few (7, 20, 21), one
imported member of a derived family (12's `c_1 = 1`), the apparatus (23),
and the two inputs no postulate replaces (18, 19). Everything else in the
referee's list (the bilinear form, the matrices, c, the factor 3, the
crossing count, the click's square) is derived from those.

### 24.2 The referee's question: is "bilinear in the state" forced?

**The claim.** The rate of a body's momentum is bilinear in the state:
the reader's content (its columns) against the first moment of the
arriving rows (0; 3.3; note 47). **It is forced**, over the integers, by
two additivities that are themselves postulates 5 and 7:

- (i) additivity over the arrivals: the rows do not read each other
  (input 7), so the reading of a set of arriving rows is the sum of the
  readings of its rows, `r(m, A + B) = r(m, A) + r(m, B)`, and a row of
  amount w is w rows of amount 1 (the apportioning; input 5);
- (ii) additivity over the reader's units: a body of content m is m
  units, each reading alone (input 5; the equivalence principle as a
  rule, the registered item 1 of series C, `push_m = m x push_1` record by
  record), so `r(m_1 + m_2, A) = r(m_1, A) + r(m_2, A)`.

**Proof** (two lines). Over Z, a map additive in one argument is linear
in it: `r(m, A) = m r(1, A)` by induction on m, and `r(1, A) = sum over
the rows of A of w x r(1, one unit of that row)`. The one unit's reading
is a function of the row's declared numbers alone (its direction **D**,
its family's columns, its age), so `r = m x sum over the rows of w x
g(D, family, age)`: the content times a moment of the arrivals, a
bilinear form. With `g = C u_D` (the columns times the direction's unit
vector) it is the flow (the moment of order 1); with `g = C` the
presence (order 0); with g quadratic in `u_D` the second moment; with g
the age the age moment: note 47's four readings and no other. That is
the whole freedom: bilinear is forced, the ORDER of the moment and the
columns' values are the choice among few (the columns INPUT, row 18).
Nothing non-linear in the state can enter a body's rate without
breaking (i) (a row's effect depending on the other rows) or (ii) (a unit
of content reading differently in company), and the lattice Gleason of
6.5 shows the one quadratic step of the law, the click, is forced the
same way on the record's vector. **Answer**: forced by symmetry of the
count (additivity in both arguments), not chosen; what is chosen is the
moment's order per rate, and the register pins it (the push the flow,
the clock the presence or the age moment).

### 24.3 The Delta P table: every computable difference from quantum mechanics or relativity, as the law is declared

Each row: the difference, the law's number, nature's or the theory's,
the size, the experiment that bounds it today (the source as NATURE.md's
rows carry it, or named here), the verdict; rows 21 and 22 are the two
the owner's report of record 340 measured on `main` 5cc43ae7. Where
covariant-readings-v1 (17.6, buildable) or optical-v1 (record 323)
changes the row, the row says so; the verdict is `main`'s.

| # | The difference | The law | Quantum mechanics or relativity | Delta P | The experiment that bounds it | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Tsirelson's bound reached as a limit only: the CHSH sum at the registered Bell world, N = 256 | `S = 720 / 256 = 2.8125` (bell.txt line 6, the exact cells, unchanged by the tables' scale from 256 to `2^20`) | `2 sqrt 2 = 2.828427` | `-0.0159` (0.56 percent) | Poh, Joshi, Cere, Cabello and Kurtsiefer 2015, Phys. Rev. Lett. 115, 180408: `S = 2.82759 +- 0.00051` (the deficit `0.00084 +- 0.00051`) | REFUTED at N = 256 (30 standard errors: the measured `2.82759` less the law's `2.8125` is `0.0151`, `29.6` times `0.00051`; the `0.0159` of the difference column is the law's deficit from `2 sqrt 2` itself, `31.2` errors, not the distance from the measurement); N = 64's `2.75` likewise |
| 2 | the same at N = 512, 1024, 2048, 4096 and 8192, the plateau | `S = 181 / 64 = 2.828125` exactly (the registered `1448 / 512`, `2896 / 1024`, `11584 / 4096`; the closed form of 24.4 on the tables' exact correlations, `bell_plateau.py`; record 102's "every power of two from 512" was wrong above 8192, the external reviewer's F01) | `2.828427` | `-3.02 x 10^-4` | the same measurement: the law's deficit is `1.1` standard errors from the measured deficit | OPEN, within reach (24.4) |
| 3 | the same at N not a power of two, or a power of two outside the plateau | above `2 sqrt 2` for 252 of the 512 values of N (record 102), at the powers of two N = 16, 32 and 128 (S = 3, 3 and `23 / 8`; the engine reads `23 / 8 = 2.875` at N = 128, the auditor's round 6 at d17af9b9) and at N = 16384 and 32768 (`5793 / 2048 = 2.828613`, `+1.9 x 10^-4` above the bound: the rungs of both settings round up together and the plateau ends); N = 65536 gives `11585 / 4096 = 2.828369`, N = 131072 `46341 / 16384 = 2.828430`, `2^20` `370727 / 131072 = 2.828423`, and the limit is the tables' own `186034 / 65773 = 2.828425`, `2.1 x 10^-6` below the bound (24.4's closed form; `bell_plateau.py`): a no-signalling box wherever S is above the bound | at most `2 sqrt 2` | up to `+8 / N` (N = 16, 32, 128: 3, 3, `23 / 8`; 16384 and 32768: `+1.9 x 10^-4`; from 65536 within `6 x 10^-5` of the bound) | the same measurement bounds an excess above `0.001` at two standard errors | REFUTED for N = 16, 32, 128 and the non-powers above the bound by more than `0.001`; N = 16384 and 32768 at `2.0` standard errors from the measurement (the edge, `+0.00102`); the powers from 65536 inside (1.5 to 1.6 errors); the law's N is the plateau's (row 2) or 65536 and above |
| 4 | the click's rounding to the scale 256: one polariser at 22.5 degrees and the 22.5-degree chain (Malus) | the pass `219 / 256 = 0.85547` and the chain `187 / 256 = 0.73047` at N = W = 256 (malus_map.out, sections 2 and 4) | `cos^2 = 0.85355`, `cos^4 = 0.72855` | `+0.0019` both (0.22 and 0.26 percent) | Malus's law at a polariser, NATURE row 9; RUN in the law (EXPERIMENTS A12, extended at 22.5 degrees, 2026-09-21, record 395): the gathers' chosen cells over the records 1 .. 256, a DETECTOR reading, `219 / 37` of 256 at the polariser and `187 / 32 / 5 / 32` on the chain, the pinned counts exactly (the difference zero), the same `+0.0019` against nature; a precision Malus test at `10^-3` decides | OPEN at the tables' scale; REFUTED by any test at `10^-3` unless the scale is raised (the cost of input 13 by the owner's word, record 328); the exact form removes it (24.1 row 13) |
| 5 | the anisotropy of c: the one-way pace per direction at Q = 64 | `32 / 55` on an axis, `64 sqrt 2 / 156` on a face diagonal, `1 / sqrt 3` on the body diagonal: `+0.78`, `+0.49`, `0` percent | isotropic | `7.6 x 10^-3` | Herrmann et al. 2009, Phys. Rev. D 80, 105011 (`10^-17`); Nagel et al. 2015, Nature Communications 6, 8174 (`9.2 +- 10.7 x 10^-19`); NATURE row 5a | REFUTED at Q = 64 by fifteen orders; OPEN only as a bound on the grain, `Q >= 5.8 x 10^17` (NATURE 5a) |
| 6 | the two arms of a moving laboratory (no contraction on `main`) | the round trip `gamma^2` along and `gamma` across (12.3) | equal (Michelson and Morley) | `beta^2 / 2 = 5 x 10^-9` at the Earth's `10^-4` | the same sources; NATURE row 5b | REFUTED on `main` by nine orders; the contraction not derived under covariant-readings-v1 either (17.6 M4) |
| 7 | the moving clock: the rate 1 at every speed | the muon's `become` at tick 64 at every speed (4.3, J4) | `gamma = 29.33` | a factor 29.33 | Bailey et al. 1977, Nature 268, 301; NATURE row 4a | REFUTED on `main`; under covariant-readings-v1 the 64th at `64 gamma` (17.6 M2), the pin J4's 367 / 345 / 391 |
| 8 | the Doppler without gamma | `1 + z = 1 + beta` (`s_mz2`: 0.2636 at beta 0.2674) | `gamma (1 + beta)`: 0.315 | `0.051` in z | Botermann et al. 2014, Phys. Rev. Lett. 113, 120405 (`2.3 x 10^-9` at beta 0.338); NATURE row 4b | REFUTED on `main`; under covariant-readings-v1 `z = 0.369 +- 0.003` on the registered world (17.6 N5) |
| 9 | the drive's first-order departure from `p = m v` (form B) | `p = m v / (1 - v / c)`: 5.3 percent more momentum per unit speed at `0.05 c` (17.2) | `gamma m v`: 0.13 percent | `v / c` at first order | the momentum of fast electrons, Bucherer 1909, Ann. Phys. 333, 513, and every accelerator since (`10^-6`) | REFUTED on `main`; the exact square of covariant-readings-v1 has relativity's form (E5, E6) |
| 10 | the dispersion `E'^2 = E'_0^2 + 3 p . p` under covariant-readings-v1 | the same form as relativity's; the grain: `E'` within a part in `E'` (`E'^2 <= W < (E' + 1)^2`) | `E^2 = m^2 c^4 + p^2 c^2` | `1 / E'_0` (a part in 4096 to a part in `2^48` on the register) | the same tests as row 9 (`10^-6`) | BELOW REACH at `E'_0 >= 2^20`; REFUTED at J4's `E'_0 = 13248` (`7.5 x 10^-5`) if J4's grain were nature's; a bound on the grain |
| 11 | the matter wavelength per axis Link (section 23): the fringe spacing's dependence on the apparatus's orientation to the axes | none: the phase at a Node is `(N / h) p . x` exactly (23.1), the wavelength `h / p` on every direction; the flight's staircase one Link | none | `0` in the phase; one Link in the arrival | spatial anisotropy of matter (Hughes-Drever type), Kostelecky and Russell, Rev. Mod. Phys. 83, 11 (2011) data tables (`10^-22` and below) | OPEN at 0 (no difference to test at the phase's level); the massive row not built |
| 12 | the gravitational redshift at second order (5.2) | `1 - k + ...`, the second order the lattice's, no horizon | `(1 + 2 Phi / c^2)^(1/2)` | `(G M / r c^2)^2 = 5 x 10^-19` at the Earth | the first order to `2.5 x 10^-5` (Galileo satellites, Delva et al. 2018, Phys. Rev. Lett. 121, 231101); Gravity Probe A, Vessot et al. 1980, Phys. Rev. Lett. 45, 2081 | BELOW REACH |
| 13 | the perihelion advance (E12) | 0: the bilinear push has no post-Newtonian term (5.3) | `43` arcseconds per century for Mercury | `43` arcseconds per century | Clemence 1947, Rev. Mod. Phys. 19, 361; the modern ephemerides | REFUTED on `main` |
| 14 | the bending of light (E13) | 0 on `main` (series K's 0.000) | `1.75` arcseconds at the Sun's limb | `1.75` arcseconds | Dyson, Eddington and Davidson 1920, Phil. Trans. R. Soc. A 220, 291; VLBI to `10^-4` (Shapiro et al. 2004, Phys. Rev. Lett. 92, 121101) | REFUTED on `main`; optical-v1 gives `~ M / b` toward the mass, the constant a grain (BUILDABLE, record 323) |
| 15 | the deceleration parameter (E18, 15.4) | `q = 0` (Milne) under the wall; `+0.35` to `+0.92` with gravity | `-0.53 +- 0.01` | `0.53` to `1.45` | Planck 2018, Aghanim et al. 2020, A&A 641, A6; Riess et al. 1998; Perlmutter et al. 1999; NATURE rows 3 and 11a | REFUTED |
| 16 | the neutrino's mass (18, 19.5) | 0: a free row of a family without content | at least `1 x 10^-7` of the electron's | the mass itself | the oscillations and KATRIN; NATURE row 8c | REFUTED |
| 17 | the weak force's two forms (18.2) | the decay curve's width over its median bounded by the record; the passage through an identical detector a filter | memoryless: `ln 9 / ln 2 = 3.17`; the passage about 1 | the form | NATURE rows 8a and 8b | REFUTED as declared (18.2's addendum names the crowd's supply) |
| 18 | the strong ratio (18.3) | the alpha's binding over the deuteron's 2.0 (series N) | 12.72 | a factor 6.4 | AME2020; NATURE row 7b | REFUTED |
| 19 | the growing wall's brightness (11a) and Tolman (11c) | `q_eff = +1`; three powers of `1 + z` short | `-0.53`; `(1 + z)^-4` | as NATURE 11a, 11c | Pantheon+; Lubin and Sandage 2001 | REFUTED |
| 20 | Born's rule to the rung `1 / (2 N)` (6.2) | the cell's probability a multiple of `1 / N` | the squared amplitude | `0.0078` at N = 64, `1.2 x 10^-4` at N = 4096 | Sinha et al. 2010, Science 329, 418 (the Sorkin parameter `0.0064 +- 0.0119`, a different observable); NATURE row 2c | OPEN at N = 4096 (below the tests' `10^-2`); the rounding is not the Sorkin term |
| 21 | the axis preference of the drive as declared on `main` (the per-axis step, `step_axis`: every axis's drive advances at every self-creation and the FIRST axis whose rule fires makes the step, x before y before z, a coincident fire of a later axis lost, `engine._move` on `main`; with equal components the same axis fires every time, with unequal components the smaller axis steps where the larger does not fire) | equal momentum on two axes: the body advanced 26 Nodes in x and none in y (the owner's report, eight runs on `main` 5cc43ae7, record 340) | isotropic motion: 45 degrees | the direction of motion off by 45 degrees; the speed per axis `n / (S + n)` | any measurement of a free body's track (the orbit README's "x before y"; series D's polygon) | REFUTED on `main` as declared; the fix form B's directional drive, in build (record 186, 301): one accumulator on the momentum's line, the Euclidean pace `abs(p) / (Q S M)` on every direction |
| 22 | a body's pace not bounded by c on `main` | a fast body at 0.925 Nodes per interval against the rows' 0.582 on an axis (the same report, record 340); the per-axis drive caps at one Link per interval in all (one axis steps per interval, the first whose rule fires), `sqrt 3 c = 1.73 c` on a heading (FORM.md section 2's `1.72 c = T_d / Q`; the register's series D at S = 1 at `1.29 c`, record 186 (2)) | nothing outruns light | one Link per interval, `1.72 c` on a heading; never `sqrt 3` Nodes per interval | every bound on superluminal matter (the Cohen-Glashow bound from the absence of vacuum Cherenkov radiation, Phys. Rev. Lett. 107, 181803 (2011)) | REFUTED on `main` as declared; closed under form B (the cap `S_1 Q / T_D` on the line) and the covariant readings (`p / E' <= 1 / sqrt 3` by the exact square, 17.6 M3, 23.1) |

### 24.4 The one prediction the paper can carry

**The candidate.** Of the open rows within reach, the smallest is row 2:
for N on the plateau, N = 512, 1024, 2048, 4096 or 8192, the law's CHSH
sum on the maximally entangled pair at the CHSH settings is

    S_U24 = 181 / 64 = 2.828125 exactly,   Delta S = S_U24 - 2 sqrt 2 = -3.02 x 10^-4,

with the marginals exactly `1 / 2` (no signalling, 6.2), unchanged by the
tables' scale from 256 to `2^20` and by N from 512 to 8192 (the
registered `1448 / 512`, `2896 / 1024` and `11584 / 4096`, all `181 /
64`). This is `P_U24 = P_QM + Delta P` computed in advance: the sum of
the four correlations' deficits is `-3.02 x 10^-4`, their split among
the settings changing with N (at 1024 and 2048 the four are `181 / 256`
each, at 512 `91 / 128` twice and `45 / 64` twice, at 4096 and 8192 `725 /
1024` twice and `723 / 1024` twice; the table below).

**The closed form, and the plateau's true domain** (the external
reviewer's F01, 2026-09-21, verified here with exact integers, the host
script [bell_plateau.py](designs/derivations_beam/bell_plateau.py) with
its output [bell_plateau.out](designs/derivations_beam/bell_plateau.out);
no run). The tables at the scale 256 give the exact correlations `E_1 =
46565 / 65773` at the settings `(0, N / 8)` and `(0, 3 N / 8)` and `E_2 =
46452 / 65773` at `(N / 4, N / 8)` and `(N / 4, 3 N / 8)`, independent of
N; a settings pair's four cells weigh `(1 + E) / 4`, `(1 - E) / 4`, `(1 -
E) / 4`, `(1 + E) / 4` of the total; the rungs `b_k = floor(N C_k / T + 1
/ 2)` (6.2) give the counts over the N births, the middle rung exactly
`N / 2`, and each pair's correlation is `E_N = 4 b_1 / N - 1`, so

    S(N) = 8 [round(N (1 + E_1) / 4) + round(N (1 + E_2) / 4)] / N - 4,   S(N) -> 2 (E_1 + E_2) = 186034 / 65773 = 2.828425 as N -> infinity (the tables' own, 2.1 x 10^-6 below 2 sqrt 2).

`S = 181 / 64` holds exactly when the two roundings sum to `437 N /
512`, which they do for N = 512 to 8192 (the fractional parts of `N (1
+ E_1) / 4` and `N (1 + E_2) / 4` rounding one up and one down) and not
at 16384, where both round up (0.83 and 0.79) and the sum exceeds by one:

| N | S(N) exact | decimal | `S - 2 sqrt 2` | the four `E_N` | `(S - 2.82759) / 0.00051` |
| --- | --- | --- | --- | --- | --- |
| 512 | `181 / 64` | 2.828125 | `-3.0 x 10^-4` | `91 / 128`, `-91 / 128`, `45 / 64`, `45 / 64` | +1.05 |
| 1024 | `181 / 64` | 2.828125 | `-3.0 x 10^-4` | `181 / 256` four times (one negative) | +1.05 |
| 2048 | `181 / 64` | 2.828125 | `-3.0 x 10^-4` | `181 / 256` four times | +1.05 |
| 4096 | `181 / 64` | 2.828125 | `-3.0 x 10^-4` | `725 / 1024`, `-725 / 1024`, `723 / 1024`, `723 / 1024` | +1.05 |
| 8192 | `181 / 64` | 2.828125 | `-3.0 x 10^-4` | the same as 4096 | +1.05 |
| 16384 | `5793 / 2048` | 2.828613 | `+1.9 x 10^-4` | `725 / 1024`, `-725 / 1024`, `2893 / 4096`, `2893 / 4096` | +2.01 |
| 32768 | `5793 / 2048` | 2.828613 | `+1.9 x 10^-4` | the same as 16384 | +2.01 |
| 65536 | `11585 / 4096` | 2.828369 | `-5.8 x 10^-5` | `11599 / 16384`, `-11599 / 16384`, `11571 / 16384`, `11571 / 16384` | +1.53 |
| 131072 | `46341 / 16384` | 2.828430 | `+3.1 x 10^-6` | `23199 / 32768`, `-23199 / 32768`, `11571 / 16384`, `11571 / 16384` | +1.65 |
| `2^20` | `370727 / 131072` | 2.828423 | `-4.6 x 10^-6` | | +1.63 |

So the headline "`181 / 64` at every power of two from 512" (record
102; the paper's statement) is FALSE as stated: the plateau is 512 to
8192, above it S(N) oscillates about the tables' limit within `2 x
10^-4`, above `2 sqrt 2` at 16384, 32768 and 131072 (a no-signalling
box at those N, `+1.9 x 10^-4` at most) and below at 65536 and `2^20`.
The prediction the paper can carry is the plateau's `181 / 64`, five
values of N, of which the register runs two (512 and 4096; 1024 by the
design's map).

**What bounds it today.** Poh et al. 2015 measured `S = 2.82759 +-
0.00051`, a deficit `0.00084 +- 0.00051` from `2 sqrt 2`: the law's
deficit `0.00030` is inside at 1.1 standard errors, and the measurement
excludes the law's N = 256 (`2.82759 - 2.8125 = 0.0151`, 30 standard
errors, `29.6`; the law's deficit from `2 sqrt 2`, `0.0159`, is `31.2`
errors and is not the distance from the measurement) and every N
that is not a power of two (an excess above `0.001`). **What refutes**: a
CHSH measurement on a maximally entangled pair with an uncertainty below
`1 x 10^-4` reading a deficit below `2 x 10^-4` (S above 2.8282), or any
deficit above `4 x 10^-4` outside its error; three times Poh's
precision decides. **The pin's run, made** (PR #528, merged at 84d7e5b7; until it the
values above were the design's host map, bell.txt, at N = 64, 256 and
1024 and 6.2's statement for the rest). The pin before the run: `11584
/ 4096` at every quadruple of the CHSH settings, the marginals `2048 /
4096`, the counts over `W` births within one of `W x` their rungs. The
run: the registered Bell worlds at N = 512 and 4096 under the one click
and the wheel `[r, W]` on the registered geometry read `S = 1448 / 512`
and `11584 / 4096`, both exactly `181 / 64`, the marginals `256 / 256`
and `2048 / 2048`, every count equal to its pinned count (N = 512: 219 /
37 / 37 / 219, 37 / 219 / 219 / 37, 218 / 38 / 38 / 218 twice; N = 4096:
1749 / 299 / 299 / 1749, 299 / 1749 / 1749 / 299, 1747 / 301 / 301 /
1747 twice), PASS on all eight worlds; the register's block
`bell_24_4` and the test `tests/test_amplitude_bell_24_4.py`. No number
moved.

**Why this one.** Rows 5 to 9 and 13 to 19 are refuted on `main` or
below reach; row 4 is a grain the owner has declared an input (the
tables' scale, record 328) and falls with it, not with the law; row 11 is
zero; row 20 is a rounding. Row 2 is a number of the law's own structure
(the rungs of the ladder at a power-of-two N on the tables'
correlations), fixed for the five N of the plateau, which the register
uses, and one experiment already sits at its edge. It is the prediction the paper can carry: a CHSH sum three parts
in ten thousand below Tsirelson's bound, exactly `181 / 64`.

### 24.5 The verdict of section 24

**The conditional derivations of this document** (record 398's CONDITIONAL list, with the passages the paper's cut removed) are each a declared hypothesis outside the law, [HYPOTHESES 27](HYPOTHESES.md), with the condition, what closes it and what refutes it; no line of this document claims them as the law's (the owner's GO of 2026-09-21, about 23:28Z, its record to follow).

The physics of the law lives in seven grains, two rules chosen among
few, one imported member of a derived family, the apparatus's
declarations and two inputs no postulate replaces (24.1); the bilinear
rate the referee asked about is forced by additivity in both its
arguments over the integers (24.2), the choice being the moment's
order. Of twenty-two computable differences from quantum mechanics and
relativity (24.3), fourteen are refuted on `main` as declared (five of
them closed by covariant-readings-v1 or optical-v1 in form, to be run,
and two, the axis preference and the unbounded pace, by form B in
build),
three are below reach, four are open, and one is a prediction within
reach: `S = 181 / 64`, three parts in ten thousand below Tsirelson's
bound (24.4). No run; nothing enters the law.

## 25. The big formulas of the continuum: flow, heat, temperature and the rest, what the GameBoard has of each

**The owner's order** (record 343, 2026-09-21, translated: "check whether
it is possible to reach also the formulas of flow, the formulas of
temperature if there are any, and more big formulas that people brought
with them"). Two rounds under the six-point standard (21.5): round 1,
this inventory, every formula with what it is on the GameBoard (the
reading that shows it, DETECTOR or GAMEBOARD, record 281), its standing
(reached exactly, in the limit, in form, or not reached with what is
missing named as an identity if a rule is needed), its pin (the derived
integer or closed form and the world that would read it) and its verdict;
round 2, the derivations of what round 1 finds reachable now, one formula
per subsection with its error term, the host map
[lattice_gas.py](designs/derivations_beam/lattice_gas.py) with its output
[lattice_gas.out](designs/derivations_beam/lattice_gas.out) (the collision
table imported as law data, exact rationals, decimal only for checks)
making round 2's numbers. Nothing enters the law; no run (a
pin that needs one is the experimenter's, on the Boss's order). The
three tests apply to any rule a formula would need beyond the law:
generic, vector, local (skills/workflow.md, record 202).

**Notation, once.** rho the density of rows or bodies per Node; **j** the
flux (rows crossing a face per interval); **u** a mean velocity in Links
per interval; P the pressure (the momentum crossing a face per interval
per Node of the face, label units); Theta the temperature reading defined
in 25.1 row 8 (label units squared per unit of content); nu the kinematic
viscosity and D_diff the diffusion coefficient (Links squared per
interval); kappa the thermal conductivity; H Boltzmann's H (bits, section
14); the other symbols as in the sections cited.

### 25.1 The inventory

**Three facts of the law that decide most rows, stated once.** (F1) Rows
in flight are ballistic on their lines (input 7 of 24.1: the flight blind
to the crowd) and collide only on the six-heading gas of ONE number and
content (BEAM_LAW section 4: eight slots, the six headings and two rest
slots; a fan direction is a spectator; the table permutes the single
units of one (number, content) class, conserving amount and momentum;
the head-on pair parks and cycles through the three axes); rows of two
emitters never collide. (F2) Bodies interact only at the contact (a step
refused by an occupant, `engine.py` `_contact`): under `measure` the axis
component of the momentum is handed to the occupant (momentum
conserved, the pair's kinetic energy not: inelastic), under `rerelease`
it is returned doubled (an elastic wall, the occupant unmoved), under
`pass` nothing; there is no rule by which two free bodies exchange their
momenta elastically. (F3) The click is the one non-bijective step among the law's steps
between events (14.1, 14.2; the cancel and the escape beside it in
14.2's one list): between clicks the count of states is constant (the
lattice's Liouville theorem), at a click `log2 N - H` bits of the birth
coordinate are not reported by the outcome (the run's record keeps u,
14.2's observation map).

| # | The formula | On the GameBoard: the reading that shows it (kind) | Standing | The pin (the closed form or integer; the world that would read it) | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1 | the continuity equation `d rho / dt + div(j) = 0` | the books: every unit born, absorbed, escaped or in transit is on a ledger line at every tick (BEAM_LAW section 5; `measured + transit + escaped` constant); the flux through a face the face's escaped line (GAMEBOARD) and its clicks (DETECTOR) | reached EXACTLY at every instant on the lattice (5.5, row 47): the amount crossing a closed surface per interval is the release inside it | series E's `k_s r^2 = 41.5` (the flux through the square within 2 percent of q, series C item 5); round 2 derives the equation from the ledger's identity | reached exactly |
| 2 | Euler's equation `rho (d u / dt + u . grad u) = -grad P` | the six-heading gas of one number under the collision table (F1): the mean flux per Node over a coarse cell (GAMEBOARD) | the classical lattice-gas route (Frisch, Hasslacher and Pomeau 1986; Wolfram 1986): the collision conserves mass and momentum and the Chapman-Enskog expansion gives Euler's form at first order in the gradient; but on the cubic six-Link lattice with two rest slots the momentum flux tensor is not isotropic at fourth rank (the HPP obstacle: the square and cubic lattices carry `sum_i c_i c_i c_i c_i` off the isotropic form; FHP's hexagon cures it in two dimensions, the FCHC projection in three) and the Galilean factor `g(rho) != 1` multiplies the convective term | the collision table's `g(rho)` and the stress tensor's anisotropy computed from the table's 20 orbits (round 2, an integer host map), the pin a shear flow on the six-heading gas reading the momentum flux per face | reached IN FORM with the known obstacle: Euler's form with an anisotropic momentum flux and `g(rho)`; the isotropic Euler NOT reached on the six-Link lattice (a fan-wide collision would be an identity, `fan-collision-v1`, not designed) |
| 3 | Navier-Stokes, `+ nu Laplacian(u)` | the same gas; the viscous stress from the collision's relaxation of the momentum flux (GAMEBOARD) | the same route at second order: a viscosity from the table's relaxation, with the same anisotropy of the fourth-rank tensor; the six-heading gas of one number only (F1), so a fluid of many emitters' rows does not mix by collision at all | `nu` from the table by the Chapman-Enskog integer map (round 2); the pin the decay of a shear wave on the gas | reached IN FORM on a single-number gas with the obstacle; NOT reached as the isotropic Navier-Stokes |
| 4 | Bernoulli, `P + rho u^2 / 2 = const` along a streamline | follows from Euler on a steady flow | as Euler's: in form with the `g(rho)` factor (`P + g rho u^2 / 2`) | the same shear world's pressure against its mean flux | reached in form as Euler's corollary; the constant's factor the table's |
| 5 | the diffusion equation `d rho / dt = D_diff Laplacian(rho)` and Fick's law `j = -D_diff grad(rho)` | a tagged row of the six-heading gas scattered by the collision (F1): its displacement's second moment per interval (GAMEBOARD); a row on a fan direction is ballistic and never diffuses | the lattice-gas route: the tagged unit's walk is a Markov chain on the six headings with the table's scattering probabilities at the local density, so its second moment grows linearly and the density obeys the diffusion equation at second order in the gradient; the second-rank tensor IS isotropic on the cube (the only isotropic rank-2 tensor on the 48 is the identity), so the diffusion equation is isotropic where Navier-Stokes is not | `D_diff = c^2 tau_c / 3` with `tau_c` the mean intervals between collisions from the table at the density (round 2's integer map); the pin a pulse of rows on the six headings in a periodic cube, its second moment per interval | reached IN FORM for the six-heading gas of one number; a fan-direction row does not diffuse (ballistic, F1) |
| 6 | the heat equation `d T / dt = (kappa / rho c_v) Laplacian(T)` and Fourier's law `q = -kappa grad(T)` | the content carried by the diffusing rows (each row's content `h s`, 6.4) as the energy that diffuses (GAMEBOARD); a detector's content per click (DETECTOR) | Fourier's law is Fick's law on the content current where the rows diffuse (row 5), with `kappa = D_diff x rho x (content per row)`; a temperature enters only through row 8's definition | the same pulse world with two families' contents; the content current per face against the content's gradient | reached IN FORM as Fick's law on content; the coefficient the table's |
| 7 | temperature | no rule of its own on the GameBoard (no rate reads a temperature; 16.4's last row); TWO readings: GAMEBOARD, the mean squared momentum per unit of content over a set's bodies per axis, `Theta_a = (1 / n) sum over the set of p_a^2 / (Q S M)`, in label units squared per unit of content; DETECTOR, a detector's histogram of the content per click against its energy ladder `E = h s` (the click record's `content`), a temperature only if the histogram is exponential (Boltzmann's factor), which nothing in the law makes it (F2: no thermalisation) | a reading exists (GAMEBOARD) and a measurement exists (DETECTOR); a temperature as an equilibrium's parameter does not: no rule brings a set of bodies to one Theta (F2), and the entropy's count (section 14) gives `1 / T = dS / dE` only when the count is a function of the energy alone (row 12) | the definition, with `k_B` the conversion of 16.1; the pin the reading on series G2's 24 stars (`Theta_x` from their declared momenta, an identity of the declaration) | reached as a READING (a definition, not a law); not reached as an equilibrium's parameter |
| 8 | the ideal gas law `P V = N k T` | the pressure as the books' momentum flux through a face: the face's escaped momentum per interval (`face_momentum`, `engine.py`, GAMEBOARD) or the momentum the face's clicks carry (DETECTOR) per Node of the face; N the bodies of the set; T row 7's Theta | the kinetic identity `P_a = n <p_a v_a> = n Theta_a` per axis for free bodies with elastic face reflections (`rerelease` at a face: the component returned doubled, F2) holds as an identity of the readings, exact in the mean, needing no equilibrium; `P V = N Theta` per axis | a periodic-in-two-axes bar of n free bodies at declared momenta with `rerelease` faces: the face's momentum per interval against `n Theta_x` (an integer identity of the declared momenta and the flight's whole steps; round 2) | reached IN FORM as an identity of two readings (`P V = N k Theta` per axis); the equation of state of a real gas (the interactions) not reached |
| 9 | equipartition, `<E_a> = k T / 2` per degree of freedom | the mean of `p_a^2 / (2 Q S M)` over a set per axis (GAMEBOARD) | an identity per axis by row 7's definition; the CONTENT of equipartition, that the three axes share one Theta and every body the same, needs elastic exchange between bodies, which the law lacks (F2): an identity `elastic-contact-v1` (the one-dimensional elastic exchange of the axis components between two bodies of contents `m_1`, `m_2` at a refused step, `p_1' = ((m_1 - m_2) p_1 + 2 m_1 p_2) / (m_1 + m_2)` as one `by_drive` with its remainder, momentum exact, the energy to the remainder) is named, not designed; its three tests: generic (no name), vector (T, B), local (the two records) pass on paper | none until the identity | NOT reached (the equality of the axes' Theta); the identity named |
| 10 | the Maxwell-Boltzmann distribution | the histogram of a set's `p_a` (GAMEBOARD) | needs the same exchange (row 9) and many contacts; under `measure` contacts (inelastic) the momenta drain to zero, under `rerelease` they are reflected off unmoved occupants: no relaxation to a distribution on `main` | none until `elastic-contact-v1`; then the pin the histogram of n bodies in a periodic box after `10^4` contacts against `exp(-p^2 / (2 m Theta))` to the rung | NOT reached; the identity named |
| 11 | Boltzmann's entropy `S = k log W` | section 14's count of state vectors consistent with the click list (a host reading of the register's click counts; `mz_equal` 0 / 6, `slits_low` 3.425 / 2.575) | reached EXACTLY as the count (row 53) | the registered counts | reached exactly |
| 12 | the H-theorem, `d S / dt >= 0` | 14.1 and 14.2 under the bijection (F3): the count is constant between clicks (Liouville on the lattice) and drops by `log2 N - H` bits erased at each click, so the world's entropy in 14's sense changes only at clicks, and the click list only grows | reached in the law's own terms (14.3's verdict): the second law located at the click; Boltzmann's kinetic H (a coarse-grained count over the gas's cells) would decrease under the collision table's mixing on the six-heading gas as in every lattice gas, a GAMEBOARD reading not made | the click-count identity of section 14; for the kinetic H a coarse-grained count on the pulse world of row 5 | reached in form (at the click, exactly; the kinetic form a reading not made) |
| 13 | temperature from entropy, `1 / T = dS / dE` | the count of 14 as a function of the set's energy (the content per click, the bodies' `E'`) | the derivative exists only where the count depends on the energy alone; the law's count depends on the click list, not on an energy: a temperature from entropy needs an ensemble of worlds at one energy, which the law does not have (one world, one click list) | none in sight | NOT reached (no ensemble) |
| 14 | Planck's law, Wien, Stefan-Boltzmann | the release `E = h s` per unit at the lamp's turn (6.4, row 51, exact); a detector's histogram of the content per click (DETECTOR) | the spectrum of a crowd is the lamps' declared rates; a black body needs lamps at every rate weighted by `1 / (e^(h f / k T) - 1)`, which no rule produces (rows 7, 10): the shape is an input | none: a world declaring Planck's weights would read them back (an identity of the declaration, not a law) | NOT reached; the spectrum an INPUT (24.1 row 18's `n / d`) |
| 15 | Maxwell's equations | 21.5's rows 47 to 50 by reference: Gauss exact, the wave equation reached, Faraday and Ampere-Maxwell under `source-velocity-v1` | as there | as there | as 21.5 |
| 16 | the wave equation (the linear block) | 4.1, 5.1, row 48 | reached (second order in the Link, the anisotropic term named) | series K's 89.40 | reached |
| 17 | Dirac's equation | the hand is a pseudoscalar bit on the row (hand-v1, the 48's action); a massive row's dispersion is the exact square (23) | the spinor structure (two components mixed by the momentum, the first-order form) is not in the law: the hand is a bit, not a spinor, and the massive row's block is scalar (23.2); an identity would carry a two-component label turned by the direction (`spinor-rows-v1`), not designed; the three tests on paper: generic, vector (P on a two-state label), local | none | NOT reached; the identity named |
| 18 | Hooke's law `F = -k x` | binding-v1's bond (the give at the contact, a bound pair a fixed point `p = 0` at one Link, 0's class I) | the bound pair is a hard bond: the force is the columns' `1 / r^2` in flight and the contact's hand-over at one Link, no term linear in a displacement; a Hooke oscillator would need a restoring push proportional to the separation, which no column gives (the columns are bilinear in the flow, 24.2) | none | NOT reached: the law's bonds are hard (a fixed point), not springs; a chain of hard bonds has no small-oscillation mode |
| 19 | Ohm's law `j = sigma E` | a charged body pushed by a field's flow through a crowd of other bodies: its momentum accumulates the push per interval and nothing drains it (F2: contacts hand over or reflect, no drag) | a steady drift needs a drag; the law's crowd slows a body's CLOCK (the owed count, 5.2), not its momentum; on `main` a pushed body accelerates without bound (row 22 of 24.3) | none until a drag: `elastic-contact-v1` (row 9) gives a mean free path and a drift at `sigma = n q^2 tau_c / m`, the Drude form, if built | NOT reached; the identity named (Drude's form follows from it in form) |
| 20 | Newton's cooling `d Q / dt = -h (T - T_env)` | a body's held content released at its rate `M n / d` per self-creation (the release, 3.3) and absorbed from the crowd's rows (the click) | the release alone is an exponential decay of the held content, `M(t) = M_0 (1 - n / d)^t` (an identity of the accumulator); the "environment's temperature" is the crowd's arriving content, so the balance `dM / dt = -(n / d) M + (absorbed per interval)` is linear and relaxes exponentially to the crowd's supply: Newton's form with the content in place of the temperature | series J's lamps (the paid content falling at every birth, 6.4) and any free body's release accumulator: an identity of the declared rate | reached IN FORM for the content (the "temperature" the content's, row 7) |
| 21 | Stokes' drag and the mean free path | a body through the six-heading gas: rows arriving push it (the flow), none scatter off it | no drag on `main` (row 19) | none until `elastic-contact-v1` | NOT reached |
| 22 | the sound speed `c_s^2 = dP / d rho` | the six-heading gas: a density pulse's pace (GAMEBOARD) | the lattice gas's `c_s = c / sqrt 3`-type constant from the table (HPP: `1 / sqrt 2` on the square; the cubic value the round-2 map's) | the pulse's front per interval on the gas | reached in form (the table's constant) |
| 23 | the second law and Landauer | 14; Landauer out (record 140): the click erases at no energy | as 22.1 and row 54 | | reached (the entropy identity); Landauer D |

**Amended per round 2** (25.10): rows 2, 3, 5 and 22 carry their round-2
results there (the Galilean factor's closed form, the shear viscosity
exactly zero with the per-line invariants, the diffusion tensor not
isotropic, the sound speed's closed form); the rows above stand as the
record of round 1.

### 25.2 What round 2 derives, and what it does not

Reachable now, one subsection each in round 2 with its error term: (i)
the continuity equation from the ledger's identity (row 1, exact); (ii)
the lattice-gas limit of the six-heading collision (rows 2, 3, 22): the
Chapman-Enskog expansion on the table's 20 orbits as an integer host map,
the Galilean factor `g(rho)`, the momentum flux tensor and its
anisotropy on the cube, the viscosity and the sound speed, with the
obstacle stated as the finding; (iii) the diffusion equation from the
tagged unit's scattering (row 5) and Fourier's law on the content (row
6); (iv) temperature as a reading with the ideal gas law and
equipartition as identities of the readings (rows 7, 8, 9's identity
part); (v) temperature from entropy: why the count of 14 gives no `d S /
d E` without an ensemble (row 13), in one page; (vi) Newton's cooling as
the release's exponential (row 20). Not derivable without a rule: the
isotropic Navier-Stokes (a fan-wide collision), the Maxwell-Boltzmann
distribution, equipartition's equality of the axes, Ohm's and Stokes'
drag (all through `elastic-contact-v1`, one identity named for four
rows), Planck's spectrum (an input), Dirac (`spinor-rows-v1`), Hooke (the
bonds are hard).

### 25.3 The verdict of round 1

Of twenty-three formulas: reached exactly, three (the continuity
equation, Boltzmann's count, the second law at the click); reached in
form on the six-heading gas of one number, six (Euler and Navier-Stokes
with the HPP obstacle and the Galilean factor, Bernoulli, diffusion and
Fick, Fourier, the sound speed); reached as identities of readings,
three (temperature as a reading, the ideal gas law per axis, Newton's
cooling of the content); by reference, two (Maxwell's, the wave
equation); not reached, nine (the isotropic Navier-Stokes,
equipartition's equality, Maxwell-Boltzmann, temperature from entropy,
Planck's spectrum, Dirac, Hooke, Ohm, Stokes), of which four fall to one
identity, `elastic-contact-v1` (equipartition's equality,
Maxwell-Boltzmann, Ohm, Stokes; the isotropic Navier-Stokes to
`fan-collision-v1`), whose three tests pass on paper and whose
design is not this section's. Nothing enters the law.

### 25.4 The continuity equation from the books (row 1)

**(1) The rule.** The flight (T on the position: a unit crosses one Link
at the ages its direction's accumulator fires, 2.1, never two in one
interval), the collision (P on the directions at a free Node: the count
at the Node unchanged), the merge and the split (the amount conserved),
the release (the births at a lamp or a holder), the click, the face and
the cancel (the sinks), and the books that hold every unit on a ledger
line at every interval (BEAM_LAW section 5: units are moved, not copied;
per family, in amount, initial + released = current + escaped +
absorbed, exact at every tick). **(2) The limit.** A coarse cell of L^3
Nodes and tau intervals, many rows. **(3) The order.** The lattice
identity is exact; the continuum form is second order in the Link over
the cell. **(4) The symmetry.** None is needed: a first-rank identity
(the divergence of an integer flux). **(5) and (6)** below.

**The derivation.** Let `n(x, t)` be the amount of one family at Node
**x** at the end of interval t and `J_a(x, t)` the signed amount that
crossed the Link from **x** to **x + e_a** during interval t (the units
that crossed toward +a less those that crossed toward -a); `b(x, t)` the
amount born at **x** in the interval (the release, the re-emission, what
came home) and `q(x, t)` the amount absorbed there (the click, the
cancel; an escape is the crossing of a face Link with no Node beyond).
Every unit at **x** at the end of the interval was at **x** or at a
neighbour at its start, or was born, and every unit that was at **x** is
at **x** or at a neighbour or absorbed: so, at every Node and interval,

    n(x, t + 1) - n(x, t) = - sum_a [J_a(x, t) - J_a(x - e_a, t)] + b(x, t) - q(x, t),

the discrete continuity equation, an identity of the ledger in integers
with no remainder. Summed over a region it is the books' line for that
region, and over the GameBoard the books themselves (the transit line);
in a steady state summed over a region it is 5.5's statement that the
amount crossing a closed surface per interval is the release inside it.
With `rho` the amount per Node and `j_a` the crossing per face per
interval, both averaged over the cell, and the flux placed at the face
(the half Link), the centred differences give

    d rho / dt + div(j) = b - q + epsilon,   epsilon = (1 / 24) [d^3 rho / dt^3 + sum_a d^3 j_a / dx_a^3] + ...

in Link and interval units: **(5) the error term** is second order in the
Link over a feature's width (a feature of width `ell` Links carries a
relative error of order `(1 / ell)^2`), and the flux of rows of one
direction is `j = rho x (Q / T_d) v` exactly in the mean with the
staircase's remainder below one Link per unit at any time (2.1), which
the cell divides by L. On a fan the same identity holds direction by
direction (the rows ballistic, F1). **(6) The pin.** Series E's flux
through the square, `k_s r^2 = 41.5`, within 2 percent of the release q
(series C item 5), and every registered run's books "conserved at every
tick" (the c_measured record, EXPERIMENTS.md), which is this identity
summed over the GameBoard. **Reached exactly.**

### 25.5 The lattice-gas limit of the six-heading collision: Euler's form, the sound speed, the longitudinal viscosity and the frozen shear (rows 2, 3, 4, 22)

**(1) The rule.** The collision (P: the permutation of the single units
within a class at every free Node and interval, the class conserving the
number n of units and the vector sum **S** of their headings, BEAM_LAW
section 4) and the flight on the headings (T). The gas is of rows of one
number and content and amount 1 (the crowd of two units of one class on
one heading at one Node is a wall the table does not enter: the
lattice gas's exclusion is not a rule here but the low-density regime,
the crowd fraction per slot of order d). The unit's assignment when a
state moves, read from the implementation (`collide`,
nature_beam.py:2456-2497, not stated in BEAM_LAW section 4): the k-th
single in slot order goes to the k-th occupied slot of the image; so on
the head-on pair's cycle `+x -x -> ha hb -> +z -z -> +y -y -> +x -x` the
unit that came on +x leaves on +z two intervals later, the one on -x on
-z: a head-on meeting turns the pair's axis `x -> z -> y -> x`, a
three-fold rotation about the cube's diagonal, always the same way (the
tie by Port order, section 4's "one undeclared breaking"). Three
premises, stated because each carries an error term: (a) the flight's
staircase is replaced by its mean, c = 32 / 55 Links per interval on a
heading (2.1; the remainder below one Link per unit); the table acts at
every interval a unit spends at a free Node, so the lattice gas's time
step is the interval and its unit speed is c; (b) the Boltzmann level:
the state at a Node is drawn from the product measure of its slots'
densities, the classical lattice gas's closure (Frisch, d'Humieres,
Hasslacher, Lallemand, Pomeau and Rivet 1987, Complex Systems 1, 649),
whose error is the correlation the propagation builds, not bounded here;
(c) the law's own sector: the parity of the rest count is conserved by
every class (checked on the 256 binary states, [lattice_gas.py](designs/derivations_beam/lattice_gas.py)
(A)), so a gas born on the headings holds its rest units in pairs at
every Node and never one alone; the rest pair is one slot of two units
with its own density, not two independent slots (the classical closure
with independent rest slots is carried beside it for comparison).
**(2) The limit.** Small velocity **u** (Links per interval, below
c), long waves (the wavenumber k in 1 / Link small), the Chapman-Enskog
order. **(3) The order.** Second order in u for the flux, second order
in k for the modes. **(4) The symmetry.** The cube's: `sum_i c_ia c_ib =
2 delta_ab` (a second-rank tensor is isotropic) but `sum_i c_ia c_ib
c_ic c_id = 2 delta_abcd`, nonzero only when all four indices are equal
(the fourth-rank tensor of the cubic lattice is not isotropic: the HPP
obstacle, which the hexagon cures in two dimensions and the FCHC
projection in three; here it is not an approximate anisotropy but the
absence of every off-diagonal term); and beyond it the table's own
breaking of the 48 by Port order.

**(a) The invariant measure, exact.** Let `w(s) = exp(-eta n(s) - q .
S(s))` be a weight on the slot states with eta a scalar and **q** a
vector (four parameters). It is constant on every class, and the
collision permutes the class; so the product measure with

    f_i = 1 / (1 + exp(eta + q . c_i))   on the six headings,   f_p = 1 / (1 + exp(2 eta))   for the rest pair,

**c**_i the unit vector of heading i, is unchanged by the collision at
every Node, for every (eta, **q**), and unchanged by the streaming when
uniform: the Fermi-Dirac family of every lattice gas with semi-detailed
balance, here with the balance trivial (a permutation). At rest (**q** =
0) the heading's density is `d = 1 / (1 + exp(eta))` and the pair's `d_p
= d^2 / (d^2 + (1 - d)^2)` (a pair weighs two units), the density per
Node `rho = 6 d + 2 d_p`.

**(b) The momentum flux to second order in u.** With `F(x) = 1 / (1 +
exp(x))`, `F' = -d (1 - d)`, `F'' = d (1 - d) (1 - 2 d)` at eta, the
expansion of `f_i = F(eta + q . c_i)` summed with the cube's tensors gives

    rho = 6 d + 2 d_p + F'' q^2,   rho u_a = 2 F' q_a,   Pi_ab = sum_i c_ia c_ib f_i = delta_ab (2 d + F'' q_a^2),   all + O(q^4);

eliminating **q**,

    Pi_ab = delta_ab [2 d + g(d) rho u_a^2] + O(u^4),   g(d) = rho (1 - 2 d) / (4 d (1 - d)),

at a fixed eta, and in terms of the local density `Pi_ab = delta_ab
[P(rho) + g rho (u_a^2 - c_s^2 u^2)]` with `P(rho) = 2 d(rho)` the rest
pressure at that density and `c_s^2 = dP / d rho` below. Off the
diagonal `Pi_ab = 0` for every distribution whatever, since every
heading is axis-aligned (`c_ia c_ib = 0` for `a != b`): there is no shear
stress on the six headings at any order. Checked at d = 1 / 4 (script
part (C)): the residual of the diagonal is `1.9 x 10^-11` at `|u| =
0.0027` and falls sixteen-fold when u halves (the `O(u^4)` term), the
off-diagonal 0; `g(1 / 4) = 17 / 15`.

**(c) Euler's form (row 2) and Bernoulli (row 4).** The momentum's
ledger identity (25.4's with the labels: **S** conserved at the Node, the
momentum crossing a face per interval `Pi` per Node of the face) gives,
to second order in u,

    d (rho u_a) / dt + d/dx_a [P(rho) + g(d) rho (u_a^2 - c_s^2 u^2)] = 0,   P(rho) = 2 d,   rho = 6 d + 2 d_p(d),

against Euler's `d (rho u_a) / dt + sum_b d/dx_b (P delta_ab + rho u_a
u_b) = 0`. Three differences, each the cube's or the table's: (i) the
convective term `d/dx_b (rho u_a u_b)` keeps only its diagonal `d/dx_a
(rho u_a^2)`, the cross terms absent (the fourth-rank tensor); (ii) it
carries the Galilean factor g(d), `17 / 15` at d = 1 / 4 and `3 / 2` as d
-> 0, not 1 (the same `(1 - 2 d) / (1 - d)` factor the hexagonal gas
carries, with the cube's own prefactor: Galilean invariance broken, as
in every lattice gas); (iii) the pressure carries the isotropic
correction `-g rho c_s^2 u^2`. Bernoulli along a steady flow on one
axis, `u = u_a e_a`: `P + g (1 - c_s^2) rho u_a^2 = const`, the classical
`rho u^2 / 2` replaced by `g (1 - c_s^2) rho u_a^2` (about `rho u^2` at
low density, twice Bernoulli's). **Reached in form** with the two
factors named; the isotropic Euler not reached (round 1's verdict
stands).

**(d) The sound speed (row 22).** From the rest equation of state,

    c_s^2 = dP / d rho = 2 d (1 - d) / (6 d (1 - d) + 4 d_p (1 - d_p))   (lattice units),   c_s -> c / sqrt 3 as d -> 0,   c / sqrt 5 at d = 1 / 2;

in Links per interval `c_s = 0.3278` at d = 1 / 16, `0.3175` at 1 / 8,
`0.2924` at 1 / 4, `0.2602` at 1 / 2 (`c_s^2 = 12769 / 40227`, `625 /
2099`, `25 / 99`, `1 / 5` lattice units; the classical closure with
independent rest slots gives `1 / 4` at every density, `c / 2`). Isotropic
in the direction of the wave (the second-rank tensor is), density
dependent through the pair: at low density the rest pair is rare and the
gas is the six-heading gas whose `c_s = c / sqrt 3`, the sound speed of
radiation.

**(e) The viscosity (row 3): the linearized table and the plane wave.**
Let **A** be the linearized collision operator, `A_ij = d Delta_i / d
f_j` at the rest equilibrium (part (D): a 7 x 7 matrix of rationals at
every rational d, from the 128 states of the sector). **A** annihilates
the tangents of the equilibrium family on the right and the conserved
functionals (the mass, the momentum) on the left, and acts on the three
relaxing modes (the two differences of the axis pairs, `e_1 = (x pair) -
(y pair)`, `e_2 = (x, y pairs) - 2 (z pair)`; the exchange between the
headings and the pair, r) with the eigenvalues, at d = 1 / 16, 1 / 8,
1 / 4, 1 / 2: the pair `-0.198`, `-0.412`, `-0.834`, `-1.13` and
`-1.27` (degenerate up to d = 1 / 4 to the decimal shown, split at 1 / 2
by the Port-order tie), the exchange `-1.00`, `-1.01`, `-1.08`, `-1.47`:
the stress relaxes in one to five intervals. For a plane wave `exp(i k
x)` along x the one-step map is `L(k) = diag(exp(-i k c_ix)) (I + A)`;
reduced to the conserved modes to second order in k with the spectral
projector **P** on them and **Q** = I - **P**,

    M(k) = P + k P L_1 P + k^2 [P L_2 P + P L_1 Q (I - L_0)^-1 Q L_1 P],   L_1 = -i C (I + A),   L_2 = -(1 / 2) C^2 (I + A),   C = diag(c_ix),

which in the coordinates `delta rho`, `delta j_x` reads

    delta rho' = delta rho - i k delta j_x + k^2 m_aa delta rho,   delta j_x' = delta j_x - i k c_s^2 delta rho + k^2 m_bb delta j_x,

with `m_aa = -c_s^2 / 2` exactly and `m_bb` the table's (the cross terms
vanish). The modes are `ln lambda = -+ i c_s k - Gamma k^2` with `Gamma =
-(m_aa + m_bb) / 2 - c_s^2 / 2`, so the wave obeys, to second order,

    d j_x / dt + c_s^2 d rho / dx = nu_L d^2 j_x / dx^2,   nu_L = 2 Gamma,

the one-axis Navier-Stokes with the longitudinal viscosity, a rational
function of d from the table:

| d | `c_s^2` (lattice) | `Gamma` (lattice) | `nu_L` (lattice) | `nu_L` (Links^2 per interval, `x c^2`) | a 64-Link sound wave falls to 1 / e in |
| --- | --- | --- | --- | --- | --- |
| 1 / 16 | 12769 / 40227 | 1.2488 | 2.4975 | 0.8455 | 245 intervals |
| 1 / 8 | 625 / 2099 | 0.5833 | 1.1665 | 0.3949 | 525 |
| 1 / 4 | 25 / 99 | 0.2596 | 0.5191 | 0.1757 | 1181 |
| 1 / 2 | 1 / 5 | 0.1436 | 0.2872 | 0.0972 | 2134 |

(the exact rationals in [lattice_gas.out](designs/derivations_beam/lattice_gas.out)
(E); the classical closure gives 0.50 Links^2 per interval at d = 1 / 8
against the sector's 0.39: the pairing matters at the ten-percent
level). **(6) The check.** The eigenvalues of the full `L(k)` at `k =
0.01` and `0.005` (decimal) agree with `-+ i c_s k - Gamma k^2` to four
figures at every d, and two eigenvalues are exactly 1 at every k: the
transverse modes. **The shear is frozen, exactly.** `C c_y = 0` and `(I
+ A) c_y = c_y`, so `L(k) c_y = c_y` for every k: a shear wave `u_y(x)`
neither propagates nor decays at the Boltzmann level; and in the law
itself, without any closure, the sum of `S_y` over every line of Nodes
along y is conserved (part (A): `S_a` is conserved at every Node and a
unit with `p_a != 0` moves along its own line), so the profile `u_y(x)`
is an exact invariant. The shear viscosity is not small; it is zero, and
the per-line sums are an extensive family of conserved quantities beyond
mass and momentum (the spurious invariants of the square gas, HPP's,
here in three dimensions, not removed by the rest pair). **Reached in
form** as the one-axis longitudinal equation with `nu_L(d)` and
`c_s(d)`; the isotropic Navier-Stokes **not reached**, and the obstacle
is exact. **(5) The error terms.** `O(u^4)` in the flux and `O(k^3)` in
the modes; the crowd fraction of order d per slot; the staircase's one
Link per unit; the Boltzmann closure (unbounded here); the per-line
invariants, which make every line its own conserved system. **(6) The
pin, before any run.** On a periodic bar of one number's rows at density
d = 1 / 8 per heading: a density pulse's front at `0.3175` Links per
interval (the grain `1 / 55`); a sound wave of 64 Links falling to `1 /
e` in 525 intervals (the closure's error unbounded: a reading within a
factor 2 would confirm the form, not the number); a shear profile
`u_y(x)` unchanged after any number of intervals (an integer identity:
zero decay, exactly).

### 25.6 Diffusion and Fick's law from the tagged unit, Fourier's law on the content (rows 5, 6)

**(1) The rule.** The same table with the same unit assignment, followed
for one tagged unit. **(2) The limit.** Many intervals; the
displacement's second moment. **(3) The order.** Second order in the
gradient (the diffusion equation); the Markov chain of the tagged unit
is summed exactly (all its memory), at the Boltzmann level. **(4) The
symmetry.** The chain's velocities are axis-aligned, but the table is not
equivariant under the 48 (the tie by Port order, BEAM_LAW section 4), so
the cube's isotropy of a second-rank tensor is not available to the
diffusion tensor: round 1's row 5 assumed an equivariant table and is
corrected here.

**The derivation.** The tagged unit's slot i is a Markov chain on the
eight slots: from a heading, the other five headings are each held with
probability d and the rest pair with `d_p`; from a rest slot, the partner
is present with certainty (the pair, premise (c)) and the headings at d;
the image state and the assignment give the new slot. The transition
matrix `T_ij(d)` is a polynomial in d (part (F)); the equilibrium
occupation (d per heading, `d_p` per rest slot) is its stationary law
(checked exactly at every d: the consistency of the chain with the
sector's measure). With `e_a(t)` the unit's velocity component (lattice
units) and `C_k^ab = <e_a(0) e_b(k)>` under the stationary law, the
displacement's covariance over T intervals is `T [C_0^ab + sum_{k >= 1}
(C_k^ab + C_k^ba)] + O(1)`, so

    D_ab = c^2 [C_0^ab / 2 + (1 / 2) sum_{k >= 1} (C_k^ab + C_k^ba)],   sum_{k >= 1} T^k e_a = T (I - T)^-1 e_a on the mean-zero subspace,

an exact rational at every rational d, and the density of tagged units
obeys `d rho / dt = sum_ab D_ab d^2 rho / dx_a dx_b` with Fick's `j_a = -
sum_b D_ab d rho / dx_b`. The values (Links^2 per interval, `c^2 = 1024 /
3025`):

| d | `d_p` | turning probability per interval on +x, +y, +z | **D** diagonal xx, yy, zz | **D** off-diagonal xy, xz, yz | principal values | the memoryless `c^2 / (3 p_turn)` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 / 16 | 1 / 226 | 0.062, 0.070, 0.071 | 2.651, 2.567, 2.574 | 1.690, 1.594, 1.716 | 0.835, 1.026, 5.931 | 1.820 |
| 1 / 8 | 1 / 50 | 0.121, 0.150, 0.158 | 0.948, 0.813, 0.813 | 0.413, 0.323, 0.407 | 0.389, 0.562, 1.624 | 0.932 |
| 1 / 4 | 1 / 10 | 0.217, 0.316, 0.360 | 0.433, 0.286, 0.274 | 0.115, 0.042, 0.092 | 0.176, 0.294, 0.524 | 0.520 |
| 1 / 2 | 1 / 2 | 0.234, 0.422, 0.531 | 0.359, 0.179, 0.157 | 0.075, 0.001, 0.035 | 0.122, 0.187, 0.387 | 0.481 |

**The finding.** The diffusion tensor is symmetric and positive but far
from isotropic, and its anisotropy is not the cube's: at low density the
only two-unit collision is the head-on pair (every other pair of headings
is a fixed class), and the pair leaves on the next axis of the cycle `x
-> z -> y -> x` with the sign kept (+x to +z), so a unit's velocity
correlates positively with its later velocity on the next axis; the
off-diagonal `D_ab` are as large as the diagonal at d = 1 / 16 and the
largest principal axis is the cube's diagonal (1, 1, 1) with a value
seven times the two others. The `d rho / dt = D Laplacian(rho)` of row 5
is reached only as the tensor form; the scalar D would be the mean `tr(D)
/ 3` (2.60, 0.86, 0.33, 0.23 Links^2 per interval at the four
densities), and the naive `c ell / 3` with `ell = c / p_turn`
underestimates it at low density and overestimates it at high (the
parking and the cycle are memory the chain keeps). **(5) The error
terms.** The Boltzmann closure; the staircase; the crowd fraction; the
density is that of one number and content (rows of two emitters never
collide, F1). **(6) The pin, before any run.** A pulse of one number's
rows on the eight slots at d = 1 / 8 in a periodic cube: the covariance
of the tagged units' displacements grows per interval by `2 D_ab` with
the tensor of the table's row above (0.948, 0.813, 0.813 on the diagonal;
0.413, 0.323, 0.407 off it); the ratio of the largest principal growth to
the smallest `4.18`. **Fourier's law (row 6).** Every row of one number
and content carries the content `h s` its lamp paid (6.4), fixed in
flight; the content current is the unit current times `h s`, so
Fourier's `q = - kappa grad(T)` is Fick's law on the content, `q_a = - h s
sum_b D_ab d rho / dx_b`, with the same tensor and the same error terms;
the heat equation is the diffusion equation of the content. A
temperature enters only by 25.7's definition. **Reached in form** (Fick
and Fourier as one tensor law); the isotropic diffusion equation **not
reached**.

### 25.7 Temperature as a reading, the ideal gas law and equipartition's identity (rows 7, 8, 9)

**(1) The rule.** The drive (`by_drive` on the body's accumulator: a
Link at `+-D`, `D = Q S M + abs(p_a)`, so `v_a = abs(p_a) / (Q S M +
abs(p_a))` Links per interval, 4.4) and the contact under `rerelease`
(the axis component returned doubled to a fixed occupant, `_contact`,
engine.py; the occupant's momentum label accumulates the impulse).
**(2) No limit**: identities of readings, exact in the mean over T
intervals. **(3) The order.** The ratio `1 - v_a` per body, exact.
**(4) No symmetry.**

**The temperature reading (row 7).** `Theta_a = (1 / n) sum over the set
of p_a^2 / (Q S M)`, in label units squared per unit of content; `k_B`
is the conversion of 16.1 (the law has no temperature of its own; 16.4).
On series G2's 24 stars (the declared momenta of `coasting_none.json`; Q
S M = 2^48), an identity of the declaration, part (G): `Theta_x / (Q S M)
= 0.013166`, `Theta_y / (Q S M) = 0.017468`, `Theta_z / (Q S M) =
0.022764` (the mean of `(p_a / Q S M)^2`, the mean squared pace at first
order; the exact rationals in the output). The three differ by the
throw's design and no rule of the law brings them together (F2): a
reading exists, an equilibrium's parameter does not.

**The ideal gas law as an identity (row 8).** One free body of content M
and momentum `p_x` on a bar of L Links along x, periodic on y and z,
between two fixed occupants that declare `rerelease` for the body's
family: at each wall the step is refused, the body's component reversed
and the occupant's label raised by `2 abs(p_x)` (the impulse). The body
crosses a Link every `D / abs(p_x)` intervals, so a round trip of 2 L
Links takes `2 L D / abs(p_x)` intervals and the mean force on one wall
is `2 abs(p_x) x abs(p_x) / (2 L D) = p_x v_x / L`; with P the force per
Node of the wall and V = L per Node of the cross-section,

    P_x V = p_x v_x = p_x^2 / (Q S M + abs(p_x)),   and over n bodies on their own lines   P_x V = sum_i p_ix v_ix = n <p_x v_x>,

the kinetic identity of a gas of free bodies with elastic walls, exact in
the mean, needing no equilibrium (relativity's `P V = N <p v>`). Against
the temperature reading, `p_x v_x = (p_x^2 / (Q S M)) (1 - v_x)`:

    P_x V = n Theta_x - n <p_x^2 v_x / (Q S M)>,

the ideal gas law per axis with **(5) the error term** `-v_x` per body
(the drive's saturation, the lattice's `p / (m + p)` for relativity's
`p c^2 / E`, 4.4), plus the remainder of one bounce per body in the
wall's label (`2 abs(p_x)`, the reading's O(1)) and the drive's
hesitation at a reversal (the signed accumulator must be driven from its
remainder to `-D`: below `D / abs(p_x)` intervals per bounce, one Link's
time, a relative `1 / L`). **(6) The pin** (part (H)): at Q S M = 4096
(the slits_matter units), `p = 220`: `p v = 12100 / 1079 = 11.214`
against `Theta = 3025 / 256 = 11.816`, the ratio `1024 / 1079`; `p =
1024`: `204.8` against 256, the ratio `4 / 5`; `p = 4096`: 2048 against
4096, the ratio `1 / 2`. On G2's stars the kinetic mean is `0.793`,
`0.775`, `0.756` of `Theta_a` on the three axes (the paces up to 0.29).
**Reached as an identity** of two readings, with its error term.

**Equipartition's identity part (row 9).** The exact square (17.6 M3),
`E'^2 = E'_0^2 + 3 p . p` with `E'_0 = Q S M` and `E' = E / c^2` in the
identity's units, gives the kinetic part `c^2 (E' - E'_0) = p . p / (2 Q
S M) - 3 (p . p)^2 / (8 (Q S M)^3) + ...`, so per axis

    <K_a> = Theta_a / 2 + O(Theta_a^2 / (Q S M)),

"k T / 2 per degree of freedom" with `k T = Theta_a` by the definition:
an identity, the error term the relativistic correction. The content of
equipartition (one `Theta` for the three axes and for every body) needs
the elastic exchange the law lacks (F2): `elastic-contact-v1` of round
1, named, not designed. **Reached as an identity; not reached as a law.**

### 25.8 Temperature from entropy: why the count of section 14 gives no `dS / dE` (row 13)

`S = log2 W` with W the number of state vectors consistent with the
click list (14.1, 14.2) is exact and registered (`mz_equal` 0 / 6,
`slits_low` 3.425 / 2.575 bits read / erased). A temperature from it,
`1 / T = dS / dE`, needs W as a function of an energy E that can vary
while everything else is held: the microcanonical count of a subsystem
at the energy its contact with a reservoir gives it. The law has three
reasons that no such function exists. (i) One world, one click list: W
is a function of the click list, which is a function of the world's
history; there is no ensemble of worlds over which an energy varies,
and in a closed world the content's total is a constant of the books
(the content line, BEAM_LAW section 5), not a variable. (ii) Within a
world, the freedom the click erases is the birth phase u (14.2), and
every record of one lamp carries the same content `h s` (6.4): along the
one variable W counts, the energy does not change; W(E) is supported on
one value of E and has no derivative. (iii) No subsystem exchanges
content reversibly with another: the exchanges are the click (F3, not a
bijection, no reverse step) and the hand-over at a contact (F2,
inelastic), so no part of the world has a count that is a function of
its own energy alone, which is what a reservoir gives. What would supply
it is the same identity as row 9's, `elastic-contact-v1`, with many
contacts; its three tests pass on paper (generic, vector, local) and its
design is not this section's. The one ratio the law does have is the
click's: `log2 N - H` bits erased per record of content `h s`, a bits-
per-content number of the detector (6 bits per record of content 1 on
`mz_equal`), which is not `dS / dE` (nothing is held fixed against a
varying E) and is not called a temperature here. **Not reached; the
identity named; nothing enters the law.**

### 25.9 Newton's cooling as the release's exponential (row 20)

**(1) The rule.** The turn accumulator (T on the lamp's record: it gains
`M(t) x n` at every self-creation, M(t) the content the frame reads
before the birth pays, the clock's rate `K = [n, d]`; the turn `s_t` is
the whole part in units of d and the remainder stays: `by_drive`,
`_frame_all`, engine.py; BEAM_LAW note 41) and the cost `h s_t` per unit
born, b units per self-creation (the directions times the rate's count;
`cost = quantum x turn`, nature_beam.py). **(2) No limit**: an identity
of the accumulator. **(3) The order.** Exact recurrence; the smooth
solution's error bounded. **(4) No symmetry.**

**The derivation.** `M(t + 1) = M(t) - h b s_t`, and because the
accumulator keeps its remainder the turns sum to a whole part exactly:
`sum_{tau < t} s_tau = floor(Phi(t))` with `Phi(t) = sum_{tau < t} M(tau)
n / d`. So `M(t) = M_0 - h b Phi(t) + h b theta_t` with `theta_t` in `[0,
1)`. Let `r = h b n / d` and `u(t) = M_0 - h b Phi(t)`; then `u(t + 1) =
u(t) - r M(t) = (1 - r) u(t) - r h b theta_t`, whence `u(t) = M_0 (1 -
r)^t - r h b sum_{tau < t} (1 - r)^(t - 1 - tau) theta_tau`, the sum in
`[0, 1 / r)`. Therefore

    M(t) = M_0 (1 - r)^t + epsilon_t,   abs(epsilon_t) < h b,   r = h b n / d,

the exponential decay of the lamp's content at the rate r per
self-creation, **(5) the error term** below one birth's cost at every t,
for every M_0 and every rate. The lamp's frequency is its turn, `f = s /
N` (6.4), so the frequency falls with the content (record 148, "a paid
lamp's frequency falls at every birth"): `f(t) = f_0 (1 - r)^t` to the
same error over N. With an environment, the content the lamp's Node
absorbs from arriving paid rows (the measured line's clicks, `A_t` per
interval), `M(t + 1) = M(t) - h b s_t + A_t`, a linear balance that
relaxes to `M* = A / r` at the rate r: Newton's `dM / dt = -r (M - A /
r)`, with the content in place of the temperature and the crowd's supply
in place of the environment's, the error the same `h b`. **(6) The
pin** (part (I)): the Bell lamp, `M_0 = K + 2` at `K = 2^20`, h = 1, b =
2: the recurrence stalls once, at tick 4, and makes 159 births in 160
(the registered facts, the bell README), its content after 160 ticks `K
+ 2 - 318 = 1048260`, and `abs(M(t) - M_0 (1 - r)^t)` stays below
`1.99999 < h b = 2` over the run. **Reached in form** for the content
(row 7's reading; the "temperature" is the content's).

### 25.10 The verdict of round 2, and the amendments to round 1

| Formula | Derived in round 2 | The error term | The pin (before any run) |
| --- | --- | --- | --- |
| the continuity equation (row 1) | exact on the lattice from the ledger; the continuum form at second order in the Link | `(1 / 24) (d^3 rho / dt^3 + sum d^3 j / dx^3)`; the staircase's one Link per unit | series E's 41.5; the books conserved at every tick |
| Euler's form (row 2), Bernoulli (row 4) | `d (rho u_a) / dt + d/dx_a [P + g rho (u_a^2 - c_s^2 u^2)] = 0`, the convective term diagonal only, `g = rho (1 - 2 d) / (4 d (1 - d))` | `O(u^4)`; the crowd fraction; the Boltzmann closure | a periodic bar of one number's rows |
| the sound speed (row 22) | `c_s^2 = 2 d (1 - d) / (6 d (1 - d) + 4 d_p (1 - d_p))`, `c / sqrt 3` at low density, `c / sqrt 5` at d = 1 / 2 | the same | a density pulse's front at 0.3175 Links per interval at d = 1 / 8 |
| Navier-Stokes (row 3) | the one-axis longitudinal equation with `nu_L(d)` from the table (0.39 Links^2 per interval at d = 1 / 8); the shear viscosity zero exactly; the per-line sums of `S_a` conserved | `O(k^3)`; the closure, unbounded | a 64-Link sound wave to 1 / e in 525 intervals; a shear profile unchanged, exactly |
| diffusion and Fick (row 5), Fourier (row 6) | the tensor form with **D** from the tagged chain, anisotropic along the cube's diagonal by the head-on cycle `x -> z -> y`; Fourier as Fick on the content `h s` | the closure; the staircase | the covariance's growth `2 D_ab` per interval at d = 1 / 8 |
| temperature (row 7), the ideal gas law (row 8), equipartition (row 9) | `Theta_a` a reading; `P_a V = n <p_a v_a> = n Theta_a (1 - v)` an identity; `<K_a> = Theta_a / 2` an identity | `-v_a` per body; one bounce; the relativistic `O(Theta^2)` | G2's `Theta_a / (Q S M)` = 0.0132, 0.0175, 0.0228; `p = 220`: 11.214 against 11.816 |
| temperature from entropy (row 13) | not reached: no ensemble, no reversible exchange; the identity named | | none |
| Newton's cooling (row 20) | `M(t) = M_0 (1 - r)^t + epsilon`, `abs(epsilon) < h b`, `r = h b n / d` | below one birth's cost | the Bell lamp's stall at tick 4, 159 births in 160 |

**The amendments to round 1's rows** (25.1; the rows stand as the
record): row 2's pin (a shear flow) is replaced by the pulse and the
frozen shear, and the Galilean factor is now the closed form; row 3's
"viscosity from the table" is the longitudinal `nu_L(d)` alone, the shear
viscosity being exactly zero and the per-line invariants exact (the
obstacle is exact, not approximate); row 5's "the second-rank tensor IS
isotropic on the cube" is withdrawn: the table is not equivariant under
the 48 (BEAM_LAW section 4) and the diffusion tensor's largest axis is
the cube's diagonal, seven times the others at d = 1 / 16; row 22's
"`c / sqrt 3`-type constant" is the closed form above, `c / sqrt 3` at
low density only. Two facts of the implementation entered the
derivations and are stated in BEAM_LAW section 4 nowhere: the unit's
assignment by rank at a moving state (the cycle's chirality) and the
parity of the rest count (the pairing); both are read from `collide` and
the table, and a change of either would change 25.5's `nu_L` and 25.6's
**D**, not the exact results (25.4, the invariant measure, the frozen
shear, 25.7, 25.9). Of round 2's six items: two exact (the continuity
equation; Newton's cooling within one birth's cost), three in form with
their coefficients from the table (Euler's, the sound speed, the one-axis
Navier-Stokes; diffusion, Fick and Fourier as one tensor law), two
identities of readings (the ideal gas law, equipartition's half), one not
reached (temperature from entropy). Nothing enters the law; no run.

## 26. What the paper wants and the derivation lacks: the ten, each with its standing, the identity or program that would reach it, and the pin

**The order** (the owner's rule of record 352, through the Boss: a
formula the paper wants and the derivation lacks is listed to the Boss,
who orders it; the paper coordinator's list of 2026-09-21). Ten items,
in section 25's form: EXACT, IN FORM, IDENTITY OF READINGS or NOT
REACHED with the identity that would reach it named under its three
tests; the pin before any number and the reading that would test it; a
derivation written where it is one page, a program named and stopped
where it is one. No experiment for nothing. Nothing enters the law.

| # | The formula | Standing today | What would reach it | The pin before any number | The reading that tests it |
| --- | --- | --- | --- | --- | --- |
| 1 | the time-dependent Schrodinger equation | NOT REACHED (23.6): the stationary form is reached (Helmholtz with de Broglie's k, the exact square's dispersion, Born at the click); in flight a row carries no frequency and a record has one momentum, so nothing spreads | `packet-rows-v1`, a program (26.1) | the two-momentum record of 26.1: the centre pixel's first clicks at 863 +- 2 and 1033 +- 2 | the click ticks per pixel, bimodal (DETECTOR) |
| 2 | the Lorentz contraction; the books' balance under the identity | NOT REACHED: the contraction needs the magnetic part of the push (17.6 M4, 21.4 E3), the balance was withdrawn (N5: a row's energy `sqrt 3 h s` is no integer on the pair, a gap no (h, n, d) closes) | `source-velocity-v1` (a row carrying its source's momentum label at release; named in M4, not designed); the balance a program (26.2) | 12b.2's thrown orbit at beta 0.43: the extents' ratio 0.903 along over across, 2.5 Links on 26 (M5) | the orbit's extents from the step lines (GAMEBOARD) and the source's click list (DETECTOR) |
| 3 | Kepler's precession on the GameBoard | IN FORM on the plane: the 1 / r force's apsidal angle under the pace's exponent, `psi = pi / sqrt(1 + e)` (21.5 row 58 as amended): `-105.4` degrees per radial period at the Newtonian pace, `-79.8` under form B's; NOT REACHED beyond the continuum: the lattice's own precession (the fan's kicks, the polygon) is a GameBoard reading no closed form gives (12b.2's 9 percent margin); in space the continuum's precession is 0 and the relativistic advance needs item 8 | the lamp worlds' run (row 58), a run already ordered; the lattice's own part a reading, not a formula | `-81 +- 15` degrees per radial period on `s32_r24_lamp` and `s32_r12_lamp`, T 784 and 392 | the source's click list: the age's minimum advancing per radial period (DETECTOR) |
| 4 | the isotropic Navier-Stokes | NOT REACHED (25.5): the six-heading gas has no shear stress and conserves the momentum on every line; the longitudinal equation reached | `fan-collision-v1`, a program (26.3) | a shear wave `u_y(x)` of 64 Links on the fan gas decaying at a rate to be derived from the fan's table; on the six headings zero, exactly | the momentum per face over a coarse cell (GAMEBOARD) |
| 5 | Planck's spectrum | NOT REACHED (25.1 row 14): the spectrum is the lamps' declared rates, an input (24.1 row 18) | `elastic-contact-v1` (25.1 row 9) with rerelease walls, a program (26.4) | none until the identity; then a detector's content histogram against `E / (exp(E / Theta) - 1)` at 25.7's Theta | the content per click (DETECTOR) |
| 6 | Dirac's equation | NOT REACHED (25.1 row 17): the hand is a pseudoscalar bit, the massive row's block scalar | `spinor-rows-v1`, a two-component label turned by the direction; the three tests on paper (generic, P on a two-state label, local); not designed | none until the identity; the first pin would be the doublet's split under a field on one row | the click's label per pixel (DETECTOR) |
| 7 | Bohr's levels | IN FORM for the condition and the radii (7.2: `2 pi p r = j h` exact in the limit, `r_j ~ j^2` under the inverse square); the ENERGY reached here as an IDENTITY OF READINGS (26.5): `E_j = K + q A` with A the age moment at the body's Node, `E_j ~ -1 / j^2` in form; the TRANSITION NOT REACHED: no rule releases the difference of two levels | `level-release-v1`, named in 26.5, not designed | the ratio of the energy readings on the closed orbits at r = 12 and r = 3 of series H's geometry, 1 / 16 within the radii's grain | the body's step line (its K) and its pushed line (its A) at the closure (GAMEBOARD); the transition's photon would be a click (DETECTOR) |
| 8 | Einstein's field equation | NOT REACHED (5.5): the weak-field flux form and its retardation reached; the field's self-gravitation (E16) and the tensor source (E17) missing | `field-source-v1` and `tensor-source-v1` (21.4), named, not designed; a program of two identities | E11's and E12's numbers (the deflection and the delay of light past a mass) under the first; a moving crowd's push under the second | the rows' arrival directions past a mass (DETECTOR); the push per interval (GAMEBOARD) |
| 9 | the strong ratio's remainder | IN FORM, SHORT IN NUMBER (18.3): 4.0 (6.0 with the diagonals) against 12.72; the remainder a factor 2 to 3 that no count of the lattice's geometry gives | none within the six: the give per contact pair as a declared coupling (`sigma_s`, 19.1) makes the ratio an input; stated as such | none: an input has no pin | the escaped content per contact pair (GAMEBOARD, the books) |
| 10 | the weak forms' memorylessness | HALF (18.2): against the body's own record refuted (a bounded first passage, a ramp against the exponential); against the crowd's rung memoryless exactly as far as the crowd mixes | `decay-by-crowd-v1` (18.2), named, its three tests passing, not built; its pin the beam-and-bottle of 18.2's addendum | 18.2's addendum: the beam and the bottle reading one lifetime under the background crowd, two without it | the `become` clicks' ticks (DETECTOR) |

### 26.1 The packet, a program (item 1)

The time-dependent equation's content is the spreading of a packet, a
sum over momenta of `exp(i (p . x - E t / hbar))`. Under
`massive-rows-v1` a record has ONE momentum p on every row (the design,
PR #539: the label `p_D` the unit vector of D at the scale p), so the
record is a monochromatic wave and its temporal phase a global factor
that the click cannot see (23.2). The program: a lamp declaring a list
of momenta with weights, the record born with one row per (direction,
momentum), each row flying at its own `p / E'_D` with its own turn per
Link (the design's columns unchanged) and, the one addition, turning
per interval by its own energy, `E'_D N / h_t` with a declared temporal
quantum `h_t` (one `by_drive` on the row's `acc_turn` at every
interval; generic, vector, local: the three tests on paper); the rows
of different momenta then arrive at different ticks and their phases
differ by `(E'_1 - E'_2) t N / h_t`, which the click reads. The pin
before any number, on `slits_matter`'s geometry with the two momenta
200 and 240 in one record (the design's `E'` 4110 and 4117, the paces
0.04866 and 0.05829, the wavelengths 5.120 and 4.267 Links): the centre
pixel's first clicks at `1 + 112 + 920 = 1033 +- 2` and `1 + 112 + 750
= 863 +- 2` (the paths 50.28 Links), the bright bands of each momentum
at `23.3 x lambda / 4.6545` from the centre, and, with the temporal
turn, a beat of the two momenta of wavelength `h / (p_1 - p_2) = 25.6`
Links across the screen. What refutes the program: one arrival time for
both momenta (the pace not `p / E'`). Stopped here: the program is the
physicist's design to extend, the derivation the same as 23.2 with a
sum over momenta.

### 26.2 The books' balance under the identity, a program (item 2)

N5 withdrew the balance because a row's energy on the pair `c^2 = [1,
3]` is `sqrt 3 h s` in the identity's units, no integer, while the
emitter's exact square is an integer. The program that closes it without
a root: the exact-square bookkeeping. A row carries the square of its
energy, `3 (h s)^2`, and its momentum `h s` along its direction; at a
release the emitter's square W falls by the cross term and the row's
square, `W' = W - 2 E' sqrt 3 h s + 3 (h s)^2`, whose middle term is
irrational unless the identity declares the rounding of `sqrt 3 h s` to
the pair (`h s x 26 / 15`, the pair `[26, 15]` within `2 x 10^-4`, or a
finer pair), a declared rounding that needs the owner's word (the same
class as `T_D` at load). With it the books close to the pair's error per
unit, `2 x 10^-4 h s`, bounded and not accumulating beyond the count of
units. Stopped here: the choice of the pair is the owner's, the check
the implementer's, the pin then E5's lamp world (21.4).

### 26.3 The fan collision, a program (item 4)

The isotropic Navier-Stokes needs a collision whose fourth-rank tensor
`sum_i c_ia c_ib c_ic c_id` is isotropic, which the six headings' is not
(the cube's `delta_abcd`, 25.5) and which the fan's is in the limit of
many directions (the fan within the bound P covers the sphere within its
grain; the tensor's anisotropic part falls with the grain). The program:
a table over the fan's directions as slots (their count grows with P,
fixed for a fixed P: the local test passes), a permutation within each
class of (crowd mask, n, **S**) as the six-heading table is, generated
lazily per class (the members of a class over hundreds of slots cannot
be enumerated as the 3^8 states are: a program of its own), the class
conserving amount and momentum by construction; then the per-line
invariants of 25.5 break (a fan direction crosses lines) and a shear
stress exists. The three tests: generic, vector (P on the slots), local.
The pin before any number: the shear wave `u_y(x)` of 64 Links on the
fan gas at density d per slot decays at `nu_shear k^2` with `nu_shear`
from the fan table's linearized operator by 25.5's reduction, a number
the map gives once the table exists; on the six headings it is zero,
exactly (25.5). Stopped here.

### 26.4 Planck's spectrum, a program (item 5)

A black body's spectrum needs a crowd in equilibrium with its walls: the
rows' contents exchanged at contacts until the histogram is Boltzmann's,
then the cavity's modes counted. The law has neither exchange (F2) nor a
thermal wall (a `rerelease` wall returns the row's content unchanged).
The program: `elastic-contact-v1` (25.1 row 9) extended to rows, a wall
that at a click re-releases a unit whose content is drawn from its own
held content by the turn accumulator (25.9's release with the wall's
content as the temperature's proxy), and the reading of 25.7. The pin
comes only after the identity: a cavity of such walls at one Theta reads
a content histogram per click against `E / (exp(E / Theta) - 1)` within
the rung. Stopped here; the spectrum is an input until then (24.1 row
18).

### 26.5 Bohr's energy as an identity of readings, and the transition not reached (item 7)

Two readings a bound body has on the GameBoard: its kinetic energy from
its momentum, `K = p . p / (2 Q S M)` at first order (25.7, the exact
square's kinetic part), and the potential of the crowd at its Node, the
age moment A (12.1: the Lienard-Wiechert scalar potential exactly) times
its coupling q. Their sum on a closed orbit is the level's energy as an
identity of readings, `E_j = K + q A`, and under the inverse square on a
circle the virial gives `K = -q A / 2`, so `E_j = -K = -q A / 2 ~ -1 /
r_j`, and with 7.2's `r_j ~ j^2` the Rydberg form `E_j ~ -1 / j^2` IN
FORM. The derivation is 7.2's condition (the action per orbit `j h`)
with the circular condition `p v = q A / r` (12b.2's), one page in 7.2
already; what is new is only that the energy is read, not that a rule
gives it. The pin before any number: on series H's geometry (the
electron of content 1836 on the proton's crowd), the ratio of `K + q A`
on the closed orbits at r = 12 (j = 4.01, 7.2) and at the radius of j =
1 is `1 / 16` within the radii's grain (one Link on 12: 17 percent),
read from the body's step line (p) and its pushed line (A at its Node)
at the closure. The transition, a body leaving one level for another and
a unit of content `h f = E_j - E_k` released, is NOT REACHED: no rule
changes a body's orbit but the push, and the lamp's release is the
clock's (a rate, not a difference of levels). The identity that would
reach it, named and not designed: `level-release-v1`, a bound body
releasing at a `become`-like trigger one unit whose content is the
difference of its own energy readings before and after a push, its
three tests on paper (generic: a difference of two readings of its own
record; vector: T on the release count; local). Its first pin would be
the Rydberg ratio of two such units' contents, `1 / 4 : 1 / 9`, read as
clicks on a detector (DETECTOR); none until the identity.

### 26.6 The verdict of section 26

Of the ten: none exact; two in form (Kepler's precession on the plane,
Bohr's condition and radii) with one reading added (the level's energy
as an identity); one half (the weak forms, against the crowd); one short
in number and stated as an input (the strong ratio); six not reached,
each with its identity or program named and its pin stated where the
identity fixes a number (the packet's 863 and 1033; the contraction's
0.903; the fan gas's zero on the headings; Bohr's 1 / 16) or deferred
where it does not (Planck, Dirac, Einstein's equation). Four programs
are stopped at their statement (the packet, the books, the fan
collision, the cavity), each the physicist's or the implementer's after
the owner's word. Nothing enters the law; no run.

## 27. The constancy of c: do the six verbs with locality force a phase-blind flight? (the owner's word through the paper's writer, 2026-09-22: "go for the proof of c")

**The question.** The flight of the law moves a row along its digital
line by one accumulator, `by_drive(acc, N_l abs(D)_1, T_D)`: N_l the
label's scale (64), **D** the direction (an integer vector), `abs(D)_1`
its Manhattan length, `T_D = isqrt(3 abs(D)_2^2 N_l^2)` the direction's
wall, a carry a Link crossed; the row's phase f (an integer on the
circle of N steps) is a second accumulator, advanced per Link by the
family's declared turn (the paper's def:rules, F). The flight reads
neither f nor the family's phase rate, so the pace `N_l abs(D)_2 / T_D`
is the same at every phase and every frequency: no dispersion
(rem:nodispersion, a fact of the definitions, rung 1). The question put
here is whether that blindness is FORCED: whether any flight whose pace
depends on the row's phase accumulator f, or on the family's declared
phase rate n / d, must fail at least one of five requirements: (R1) the
three tests as written (record 202: generic, vector, local); (R2) the
books' exactness at every operation; (R3) th:isometry (the split an
isometry inverted by its conjugate transpose) and th:bijection (the
interval injective on the rows' weights, multiplicities and phases);
(R4) the isotropy within `1 / T_D` of prop:pace; (R5) the generic
requirement that the flight's declared integers are the direction's
alone, a row being a body of no content, so no family column in the
flight. The outcome must be one of three: DERIVED (the constancy of c a
theorem of the six verbs, rung 1), A HYPOTHESIS (one more requirement
named), or REFUTED (a dispersive flight passes all five, and the
constancy of c stands as the declared postulate P9 of the paper, "a
row's rate in transit constant and its wall the direction's T_D").

**Two kinds of dispersion, kept apart.** (i) Frequency dispersion: the
pace a function of the family's declared phase rate `n / d` (nature's
`omega(k)` non-linear). (ii) Phase dispersion: the pace a function of
the row's phase accumulator f, a state integer of the record, not a
declared column. The assignment names both; they fall differently.

**(i) fails (R5) by the letter and by nothing else.** A wall `T_D d /
(d + n)` or a rate `N_l abs(D)_1 (d + n) / d` reads the family's column
`[n, d]`: (R5) forbids a family column in the flight, so (i) is excluded
by requirement. It is excluded by no theorem: such a flight passes (R1)
(one primitive with declared integers, the family's pair read as an
integer, no branch on a name), (R2) (a pace moves no amount), (R3) (the
split and the interval read no pace; the injectivity argument of
th:bijection is per row and per family), and (R4) if the family factor
multiplies the whole rate (the same factor for every direction). So the
requirement (R5) is the postulate for frequency dispersion, restated: it
derives nothing.

**(ii) passes all five: the counterexample.** Take the flight

    rate = N_l abs(D)_1 (N - f),    wall = T_D N,    (the carry a Link, the phase f then advanced by the family's turn as before),

N the circle's own integer, no new declared integer; at f = 0 the pace
is the law's, at f = N - 1 it is `1 / N` of it; a row's pace changes
with its phase along its line. Against each requirement, each claim
exact on the GameBoard (rung 1):

- (R1) generic: one primitive, `by_drive`, with the declared integers
  N_l, T_D and N and the record's own f; no family name or kind; the
  same rule for every family; a row of no content is its value case.
  Vector: a translation of an accumulator at a rate that is a product of
  the declared `N_l abs(D)_1` and the state integer `N - f`, at most
  bilinear in the state (the push's rate is the same kind, a content
  times a flow); the wall declared; no root, no float, no rounding
  beyond the load's. Local: the row's own record; fixed work (one
  multiplication more per interval) and fixed storage; nothing kept at a
  Node.
- (R2) the books: the rule moves positions, never amounts; every ledger
  line (measured, transit, escaped) is unchanged at every operation.
- (R3) th:isometry reads the arriving row's weight and phase and
  re-emits by the tables at age 0: no pace enters its statement or its
  proof. th:bijection: the interval's three maps stay injective on
  weights, multiplicities and phases, and the state the injectivity
  rests on under a state-dependent stride is the row's AGE, a function
  of the event history the record keeps (the current tick less the tick
  of the row's last event), which def:rules and th:bijection's
  statement carry: the paper's Theorem 3 is stated on the quotient that
  forgets the age for a fixed event history, and 14.1's "injective given
  the record" is the same conditioning. On (Node,
  phase) alone the phase-dependent stride CAN bring two rows of one
  record together (the physics-rule reviewer's check, 2026-09-22: at N =
  64, r = 32 on one heading, two rows born at different split events on
  one line with flight residues `s_A = s_B + T_D N - N_l abs(D)_1 r`,
  both below the wall, A crossing its Link and B staying, land at the
  same Node with the same phase and the same residue after the interval:
  a collision the law's flight, with its constant stride, cannot make).
  What separates them is the age: rows of one line that reach one (Node,
  phase) by different strides were born at different ticks and so differ
  in age, and the age is the history's function, so the history the
  state keeps separates them; rows of equal age and
  equal birth phase share the whole history of the stride and never
  collide; rows of equal age and different birth phases `f_0 != f'_0`
  never meet in (Node, phase), since the same Node from the same age
  means the same count k of Links crossed and then the phases are `f_0 +
  k r` and `f'_0 + k r` (r the family's turn per Link), distinct; rows of
  different families or records are distinct terms already. So the
  theorem holds under the counterexample, on the state as the theorem
  states it; the argument of the first draft (one birth event) was one
  case short.
- (R4) the pace is `(N - f) / N` times the law's `N_l abs(D)_2 / T_D`,
  the factor the same for every direction, so at every f the pace over
  the directions differs by at most `(N - f) / N` of prop:pace's `1 /
  T_D`: isotropic within `1 / T_D`. (A phase term added to the rate
  rather than multiplied, `N_l abs(D)_1 + f`, would break isotropy, since
  the base rate scales with `abs(D)_1` and the term does not; the
  counterexample multiplies.)
- (R5) the declared integers of the rule are N_l and T_D (the direction's)
  and N (the circle's, a grain of the law, no family's); no family
  column is read; f is the record's state, not a declared integer. N is
  the circle's grain and not a column: f itself is defined on the circle
  of N steps, and no rule reads f without N, so a flight that reads f
  reads N with it; and (R5) is read here as its own justification states
  it, "no family column in the flight", so the refutation does not hang
  on a reading of the word "declared".

The merge's cancel and the click's interference do not constrain it
either, for the reason the paper's writer gives and one more: the click
reads a record's phase-count vector when the record completes, after
every one of its rows has ended, so two arms of a Mach-Zehnder whose rows
arrive at different ticks under this rule still cancel in the
evaluation `ev(f)` at the dark port (opposite phases, equal amounts,
whenever they arrive); the fringes and the 64 / 0 are timing-blind, and
so is Born's form. The phase along a path counts Links, not intervals,
so the arrival phases are those of the law; only the arrival times move.

**The counterexample disperses frequencies too, with no family column.**
Over one turn of its phase the row's mean rate factor is the mean of
`(N - f) / N` over the orbit of f under steps of r, `{s + j g : j = 0 ..
N / g - 1}` with `g = gcd(r, N)` and `s = f_0 mod g` the birth phase's
residue: the mean factor is `(N - s - (N - g) / 2) / N`. For r coprime to
N (g = 1) every family has the same mean pace, `(N + 1) / (2 N)` of the
law's, whatever its birth phase; for `g > 1` the mean pace depends on the
family's turn through g and on the birth phase through s (at N = 64 and
r = 32 the orbit is `{s, s + 32}` and the factor `(48 - s) / 64`, s from 0
to 31). So a flight reading only the record's own phase, no family
column, gives a mean pace that depends on the family's declared rate:
frequency dispersion in the mean arises from (ii) without touching (R5).
Rung 1 (an exact mean over a finite orbit).

**What would force the blindness, named.** (a) The requirement the law
already states and the paper numbers P9: the flight's rate and wall are
declared constants of the direction, the flight table indexed by (**D**,
tau) alone, the flight in the linear block (the paper's "two blocks": the
block is linear where its rates are constant); this excludes (ii) by
forbidding a state integer in the flight's rate, and it is the constancy
of c itself, not a premise from which it follows. (b) Its method form,
record 165 and 176: a constant-rate component has a closed form
(`floor(s_0 + r t)`), the exact phase at the click is a function of the
row's age and direction (24.1 row 24), and a run only confirms; the
counterexample is of the feedback class (a state-dependent rate, no
closed form) and would move the click's exact phase off its closed form
only in TIME, the arrival tick, never in the phase's value, which counts
Links (the Mach-Zehnder paragraph above: the fringes, the 64 / 0 and the
paper's Born form are untouched); the method's rule excludes it, again as
a choice. (c) The physical
candidates the writer named do not force it: the retarded field of a
source with several families (5.1) stays linear and additive under (i)
and (ii), family by family, and its static Poisson equation holds with a
coefficient per family; what is lost is one retarded wave operator with
one c for the sum, a requirement on the DYNAMIC field that the six verbs
do not state (a hypothesis, if the owner wants it: "the age moment of a
source of several families is one retarded potential with one c"); and
the identity's load-time constraint `3 h n = Q S d` (17.6 M7, N5) ties a
family's phase rate to its quantum, the width and the pair, and says
nothing of the pace, so it cannot force the pace to ignore the rate. (d)
Meyer's theorem (the paper's rem:nodispersion, second half) says no local
linear wave scheme is both isotropic within `1 / T_D` and free of
dispersion; it shows why a ballistic walker with a passenger phase is the
form that has both, not that the law must choose it: the counterexample
is a ballistic walker too, with a phase-dependent stride.

**The outcome: REFUTED.** A dispersive flight, the rule above, passes
(R1) to (R5), the books, both theorems, the isotropy and the generic
requirement as written, and it disperses both phases and, in the mean,
frequencies. The constancy of c is therefore not a theorem of the six
verbs with locality; it is the declared postulate P9 of the paper (the
flight's rate constant and its wall the direction's `T_D`, one of the
"four rules chosen among few"), and 24.1's row 7 keeps its word
POSTULATE; the ledger's line on dispersion reads "none, by P9", not
"none, in truth". What the six verbs do force, exactly (rung 1), is
narrower and already stated: GIVEN a flight whose rate and wall are the
direction's declared integers, the pace is `N_l abs(D)_2 / T_D` at every
phase and every rate up to the alias bound (rem:nodispersion), isotropic
within `1 / T_D` (prop:pace), with `c = 1 / sqrt 3` its limit (13.2
(a)); and the requirement (R5) closes frequency dispersion by the letter.
The one addition that would make the blindness a theorem is the linear
block's constancy itself, so the honest word is the paper's: an
assumption, not a derivation. No reading is pinned by this section; it
names no run.
