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

The targets, in the Boss's order, one section each: 1 the inventory (the
owner's audit); 2 Doppler from the crossing rule; 3 Newton and Coulomb from
the bilinear coupling; 4 special relativity, the symmetry of the limit; 5
general relativity, the delay field; 6 the information cost and the
classical-quantum boundary; 7 Young's spacing and Bohr's levels.

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
