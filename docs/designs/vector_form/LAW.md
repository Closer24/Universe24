# The law as one vector algebra: every rule in force as a vector operation, with its integer form beside it (read-only, the mathematician, 2026-09-21)

On the owner's word "everything moves to vectors and operations,
including c" (record 182) and the Boss's item B. This is the document
from which BEAM_LAW would be rewritten on the owner's word; nothing is
rewritten here. Its skeleton is the derivation's operator F
(`origin/claude/derivations-beam`, DERIVATIONS_BEAM.md section 0, at
e3d839e): one piecewise-linear map on the integer torus with a linear
block and a feedback block, the six operations (T) (B) (G) (P) (E) (D)
its only verbs; this document does not restate F, it fills its table
rule by rule and says in one line where it differs. File and line are
`main` at f1ee278 as merged into `claude/series-m-masses` at 2b17dca
(the derivation cites f89884f0; where a line moved, the current one is
given). The registered integer that checks each rule is the one the
register or a map of this branch holds.

## 1. The state: three vectors and nothing at a Node

| The vector | Its space | Its components | Where |
| --- | --- | --- | --- |
| **a row** (a message in flight) | `Z_X x Z_Y x Z_Z` (the Node; a periodic axis a circle, an open axis a segment with the face as its border) `x D x Z x Z_N x Z^+ x Z^+` | its Node, its direction (an index of the world's table D = F_P), its age, its phase (in the pair form a point of `Z_{N d}` whose whole part is the phase and whose residue the age holds), its number, its amount, its content; under a record its identity, branch (arm and label), multiplicity, birth phase u and hand | `nature_beam.py:195-240`, the store `1045-1280` |
| **a record** (one message of the apparatus, the unit the click reads) | `Z[Z_N]^{(end Node, label)}`, the group ring over the cells | one coefficient per phase per (end Node, label): the amounts of its rows that ended there at that phase; the rows in flight are its terms carried apart; the layer is its ledger, the memory no Node keeps | `amplitude.py:296-360`, TWO_SLITS.md section 1 |
| **a body** (a measured event) | `Z^F x Z^3 x Z_N x Z^+ x (Z / d Z)^n` | its held content per family, its momentum p, its phase, its clock age, and its counts table `acc` (one accumulator per count with its rate and wall: the drive per direction, the turn, the owed count, the release, the lamp, the push per column, the doppler flow while it exists) | `measured.py:205-353`; the table on the fraction-free branch (note 41) |

A Node is an index: it holds no register, no table, no remainder
(`nature_beam.py:2285-2291` is the host's index of which body is where,
read and not written). Everything below is a map on these three vectors.

## 2. The verbs: F's six, and the two non-linear places

The whole law is `s <- s + r; e <- [s >= d]; s <- s - e d` on every
component of the state at every interval, with the six verbs of the
derivation's section 1: **(T)** the translation, **(B)** the bilinear
form, **(G)** the group-ring addition, **(P)** a permutation of the joint
state, **(E)** the evaluation `Z[Z_N] -> Z[zeta_N]` and the norm, **(D)**
the Euclidean division with the remainder kept and the comparison. Two
places are not linear, and they are the only two:

1. **The Euclidean division with the remainder kept** (`by_drive`,
   `core/integer.py:77`): `Z -> Z/d x Z`, a bijection (nothing is lost;
   the whole part is delivered, the residue stays on the record). It is
   the carry of every count, the wall crossing that is an event. It is
   piecewise-linear: linear between walls, a jump at a wall.
2. **The click's threshold** (`amplitude.py:174-203`): the one comparison
   read out per record, `2 T u + T <= 2 N C_k`, where `C_k` is the norm
   `|ev(.)|^2` of the linear block's evaluation, the law's one quadratic
   step. It is a division whose quotient is 0 or 1 and whose remainder is
   not read: the one place the law throws information away by design
   (the click's discrete cost, the derivation's 6.2).

Everything else in the rows is linear (the flight, the phase, the age,
the merge, the split, the rotation, the gate, the evaluation), and
everything in the bodies is linear at a fixed content with bilinear
rates (the push, the drive, the turn, the owed count: F's feedback
block). Where this document differs from F's statement, in one line: F
lists a body's drive "per axis" (rate `p_a`, wall `Q S M + |p_a|`); under
the owner's yes to c in matter it is one drive on the momentum's
direction, the flight's own Manhattan accumulator at a fraction
(section 4, the drive), and the six deficit ladders of light and matter
are one.

## 3. c as the norm of the flight operator

The flight operator on a row is the translation of its Manhattan
accumulator at the rate `2 S_1 Q` against the wall `2 T_D`, `T_D = isqrt(3
|D|^2 Q^2)`, with the digital line's three deficit accumulators carrying
`S_1` from the largest. Its norm, the Euclidean displacement per interval
in the limit, is `Q |D| / T_D -> 1 / sqrt 3` on every direction: **c is
the operator norm of the flight**, the largest isotropic speed at which
the operator makes at most one Link per interval in every direction
(`S_1 Q <= T_D` is Cauchy-Schwarz, equality on the cube diagonals;
light_speed/FORM.md section 1, checked on 1 780 418 directions). Matter's
drive is the same operator at a fraction (section 4), so c bounds every
motion of the law with one constant; the constants beside it are the
widths of the samplings: N (the circle of phases), P (the sphere of
directions), Q (the pace's grain), W (the birth wheel), G (the fan's
grain), K (the clock), S (the world's width) and the declared roundings
of section 6.

## 4. The table: every rule in force, its vector form, its integer form, its place, its check

The operator of each rule acts on the vector named; the integer form is
the one in the code (or, for a rule decided and not yet built, the one in
the design named); the check is the registered integer. A rule marked
**decided** is the owner's yes not yet on main; a rule marked **design**
is proposed and waits for his word.

### 4.1 The linear block: the rows in flight

| Rule | Vector form | Integer form | File and line | The registered check |
| --- | --- | --- | --- | --- |
| The flight (the walk) | (T) on the Manhattan count along D, one Link per carry; the deficits (D) choose the axis | `m(tau) = (2 tau S_1 Q + T_D) // (2 T_D)`; the accumulator started at `T_D`, rate `2 S_1 Q`, wall `2 T_D`; the line by `abs(v_i)(j + 1) - S_1 abs(pos_i)` maximal, x before y before z | `nature_beam.py:559-563` (the count), `590-602` (the line), `605-660` (the table, an exact cache), `2389-2510` (the walk) | record 144's cone: 17 Links on the axis and 24 on the staircase at age 29; the derivation's 1.4 on seven directions over 600 intervals |
| The phase per Link | (T) on `Z_N` by `phase_per_link` per Link crossed | `phase = (phase + k x moved) mod N` | `nature_beam.py:2496, 2501` | L7's 51 and 8 mod 64 (record 144) |
| The phase per interval of age (the pair form) | (T) on `Z_{N d}` at the rate n per interval, the whole part read | `by_clock(age, n, d)` at every walk (the constant-rate identity: the age holds the residue) | `nature_beam.py:486-499, 2497-2499` | L7's 23 and 23; slits_low's 8 per interval (`two_slits_map.out`) |
| The exact phase at the click (**decided**) | (E) reads the row's two accumulators once: `phi = (n / d) x made x T_D / (S_1 Q)`, one floor on the table | the numerator `n x made x T_D` within 2^53, the denominator `d S_1 Q` | TWO_SLITS.md section 2 | slits_low's 64 clicks become wall 34, screen 16, faces 14; the cone's 41.75 and 42.00 |
| The age | (T) on `Z` at rate 1 (a rest row keeps it) | `age += 1` | `nature_beam.py:2500` | every world |
| The wrap, the face, the border `lifetime` | (T) on the circle `Z_extent`; the face a click (E); the border a comparison (D) of the age against a key | `ages_at_key(age, L)` | `nature_beam.py:2403-2405, 2413-2483, 519-527, 3993-4061` | the faces' 15 clicks of slits_low; the border's rows at age 3 in the deuteron (the derivation's 10.2) |
| The merge (the normal form) | (G): the addition in `Z[Z_N]` of identical rows at one Node, `[p + N/2] = -[p]` on a record's rows | the packed identity key, the lexsort, the sum; an antiphase pair leaves nothing | `nature_beam.py:1120-1129, 1163-1237` | `mz_balanced` 64 / 0 with D2's rows cancelled on the GameBoard (L1) |
| The collision | (P): the eight slots' single units permuted within the class `(crowd mask, n, S)`, the cyclic shift of the sorted members | the table of `3^8` codes, an exact cache of "sort, then shift"; 5440 classes | `nature_beam.py:674-705, 2345-2390` | `ladder.out` A (the classes reproduced from `class_key`); series C's rings |
| The split (a re-emission with weights) | a linear map with an integer matrix: `w -> w a_i`, `m -> m A`, `A = sum a_i^2`; (T) on `Z_N` by the turn `t_i` | the rows `(w a_i, m A, p + t_i)`; the multiplicity within 2^62 (the load ceiling `prod A`) | `nature_beam.py:3596-3695`, `world.py:2095-2137` | `mz_345` 63 / 1; the (20, 21) splitter's 1681 / 1682 |
| The fan by angle (**decided**: P as a width of the law) | the split whose matrix is the measure of each direction's Voronoi cell on the sphere, `F_P` the set | the plane: `a_D = floor(G (3 Q^2 / (T_D- T_D) + 3 Q^2 / (T_D T_D+)) / 2)`; space: the circumcentres at 2^24, the areas by Van Oosterom-Strackee at S = 2^14 and G = 2^5, the weights at 2^15 | TWO_SLITS.md sections 7 and 10; `fan_sphere_map.py` | slits_huygens: Pearson 0.895, visibility 0.954, every pin reproduced; the 290 fan's weights 483 to 2588 |
| The rotation of a label bit (a window) | a linear map with the half-angle tables' entries, applied on the lattice once per window | the amounts `w C'`, `w S'` of 2N at the scale 256, the multiplicity `x 65536` | `nature_beam.py:1848-1916`, `amplitude.py:125-140` | L3's S = 176 / 64; the marginals 32 / 64 |
| The label rotation per Link (**design**) | (T) on an angle index `Z_{2N}` per Link, the tables once at the click | `sigma += s mod 2N`; `U_{sigma + a}` at the click | label_rotation/FORM.md | the two-label counts (35, 29), (1, 63), (32, 32), (0, 64) at L = 5, 10, 16, 32 |
| The gate (CNOT) | (P): the joint labels permuted from the control's bit | the permutation of the product of the label sets | `nature_beam.py:1769-1845`, `amplitude.py:417-488` | the GHZ worlds' cells (L4) |
| The hand | a pseudoscalar bit on the row, `h -> det(g) h`; the hemisphere rule `sign(a . d) = -h` (B) and a comparison | one int8; `a . d` a lookup | `nature_beam.py:1966-1992, 3709-3719`, `world.py:1612-1620` | hand_map.out on 48 x 6 x 124 vectors; wu's counts |

### 4.2 The click: the evaluation, the norm and the wheel

| Rule | Vector form | Integer form | File and line | The registered check |
| --- | --- | --- | --- | --- |
| The offer (the record's ledger) | (E) term by term: `(X, Y) += 32 w (C[p], S[p])` per (Node, label), a ring homomorphism, so the sum of the images is the image of the sum | the tables C, S at the scale 256; the residual per channel through the rotation's entries | `amplitude.py:514-599` | `mz_equal`'s offers 1681 / 1682 and 1 / 1682 |
| The cells (the weights) | (E) and the norm `|z|^2`: the products of the residuals in `Z[i]`, summed over Node tuples (coherent within a Node, incoherent across) | Python integers, never refused | `amplitude.py:614-679` | slits_low's total 1.1364 and shares 0.528 / 0.244 / 0.228 (`two_slits_map.out` 4, reproduced) |
| The ladder and the cell of u | (D): the comparison `2 T u + T <= 2 N C_k`, the first k that holds | the rungs `b_k = (2 N C_k + T) // (2 T)`, the cell `u < b_k`; the Node within the cell by the same rungs | `amplitude.py:174-247, 681-776` | slits_low's 64 clicks (wall 11, 12, 11; screen 15; faces 8, 7) reproduced integer by integer |
| The birth wheel u | (T) on `Z_N` at rate 1 per birth | `u = (births - 1) mod N` | `nature_beam.py:3882` | the 64 births spanning the circle (L1) |
| The birth wheel at the golden rate (**decided in form**, the owner's word on the form pending) | (T) on `Z_W` at the rate r per birth, W = 4096, r = 2531 | `u_W = (ordinal x 2531) mod W`; the rungs `(2 W C_k + T) // (2 T)` | TWO_SLITS.md section 8, `wheel_map.py` | the screen's fan at 4096 births: bright 28 to 29, dark 0 to 3, Pearson 0.963, on both wheels |
| The wave reading and the returned phase | (E) applied before the click as a reading, then the nearest step | `argmin abs(X S_k - Y C_k)` among `X C_k + Y S_k > 0` | `nature_beam.py:937-999, 2767-2774` | series A's fringes 0.80 / 0.12 / 0.35 at 16 / 8 / 4 (the GameBoard's absorptions) |
| The window, the threshold, the parity filter | (D): comparisons on `Z_N`, on the amount, on a bit | `(d + w // 2) mod N < w`; the amount against the threshold; the hand against the entry's | `nature_beam.py:496-509, 2749-2757, 2792-2793, 2807-2808` | the which-path S = 88 / 64 (L3) |

### 4.3 The feedback block: the bodies

| Rule | Vector form | Integer form | File and line | The registered check |
| --- | --- | --- | --- | --- |
| The readings (the moments) | (B): `sum_rows w x u^(x)k`, k = 0, 1, 2, and the age moment, over the set; the traceless tensor a linear map | exact integers; the bound a refusal | `nature_beam.py:358-475, 319-327` | series E's `k_a r = 36.1` |
| The push (the coupling) | (B) then (T): `p += C a`, the reader's charges per column times the arriving label flow, one signed inner product per column | `epsilon_c sign(V E_c n_c) by_clock(age_A, abs(V E_c n_c), D_c d_c)`; the branch's `acc_push` per column and axis where `D_c d_c > 1` | `nature_beam.py:2180-2254, 3236-3252` | series C's nine ring readings; the deuteron's `310 967 280 640` per interval |
| The push by share (a record's row) | (D): `label x amount // m`, the residue on the giver's record (record 155 (3)) | `share_of`; today the rest on the books' `remainder` line | `nature_beam.py:855`, the record 155 order | the share world's 1536 and 1760 (record 136) |
| The drive (today) | (T)/(D) per axis: `drive += p_a`; a Link at `+-D_a`, `D_a = Q S M + abs(p_a)` | `by_drive(drive, p_a, D_a, at_most = 1)`, x before y before z, a coincident fire dropped | `core/integer.py:77`, `engine.py:95-126, 509-600`, `world.py:447-455` | the bar's speeds 0.30, 0.45, 0.75 exact; record 153's reader at v = 1 / 4 |
| The drive on the momentum's direction (**decided**: c in matter) | the flight operator at a fraction: (T) on the Manhattan count along the direction D nearest to p, the same deficits as light's | `by_drive(abs(p)_1 S_1 Q, Q S M S_1 Q + abs(p)_1 T_D, at_most = 1)` on the Bresenham line of D (form B); light the case `Q S M = 0` | light_speed/FORM.md section 3; `light_speed_map.py` D | the flight table's row and the drive at M = 0 at the same Node over 300 intervals on three directions; the k = 4 reader 84 for 100 Links |
| The contact and the give | (T): a refused step hands the axis component to the occupant (`measure`), the share over several by content (P); the give `held // h` with the remainder kept (D) | `apportion_whole`; `units = held // h` | `engine.py:685-838` | the deuteron's label 0 after each hand-over; the give's 27 / 24 (binding) |
| The turn (the clock's phase) | (T) on `Z_N` by the whole part of the accumulated rate content x n over d | main: `by_clock(clock_age, content x n, d)` (a-historical, drifts at a falling content); the branch: `acc_turn` | `engine.py:456-473`; note 41 (i) | a0_b0's 159 births for 160 (record 147); the cavity clicks 5 and 6 (PREDICTIONS 24) |
| The owed count (the clock's slowing by messages) | (T) on the accumulator at the rate k n over d, k the presence or the age moment; the clock's rate `1 / (1 + k n / d)` | main: `by_clock(clock_age, counted x n, d)`; the branch: `acc_owed` | `engine.py:119-131, 475-485`; note 41 | the deuteron's 69 waits for 80 (record 154); series E's `k_s r^2 = 41.5` |
| The release, the lamp's birth | (T): the free release `held x n / d` per direction, the lamp's count `rate_n / rate_d`, both accumulators on the branch; the cap and the stall a declared gate | `by_clock(age, held x n, d)`, `by_clock(age, rate_n, rate_d)` capped by `held // cost` | `nature_beam.py:3546-3566, 3746-3760, 3788-3799` | lamp_mirror_screen's 936 for 888 (record 147) |
| The apportioning of a row over directions or Nodes | (D) exact (the floors, the leftovers to the largest remainders) with a tie by comparison from `age mod n` (P) | `apportion_whole(total, weights, first)` | `core/integer.py:116-135`, `nature_beam.py:3727, 3866` | every fan world; the tie's break of the 48 (FORM.md section 3) |
| The recoil, the right-hand rule | (B) then (T): the momentum less the born rows' labels; `sign(A . u_d)` against the product's hand | exact integers | `nature_beam.py:3888-3921, 3709-3719` | the wu world's hemispheres |
| The transformation `become` | (D) comparisons (the age against `at`, the crowd against its key); (T) on the held vector | `ages_at_key`; the products pend to the next self-creation | `nature_beam.py:1413-1510, 3455-3457, 3528-3535` | j1's 522 .. 524 pinned; j3's 574 |
| The meeting (`meeting-v1`, under the key) | (B): the crowd's flow and the column sum; (P): the arc permutation toward the target by k steps read off the phase; (T)/(D) on `Z_N` with the carry | `t = sum kappa V`; `adv = (abs(t) + Q // 2) // Q`; `k = (phase + adv) // N`; the sectors by cross-multiplied angle keys | `meeting.py:161-241, 282-380` | series K's readings under the key (record 114's table) |
| The meeting's norm (**the one root at run time**) | not one of the six: `abs(t) = isqrt(t . t)` per interval, its fraction discarded | the derivation's 1.3 item 10; the exact form would count `t . t` against `(k Q)^2` by a comparison ladder | `meeting.py:351-358` | none registered beyond series K |
| The crossing rule (**decided**, record 158) | a body in motion meets a row once at the crossing of their world lines: (D) comparisons on the body's own last two Links and the row's last two steps | C1 the rows that crossed its Link the other way, C2 the rows resident at the destination moving against it, not C2', C3', C3'' | the design `crossing/DESIGN.md` (to be copied); `nature_beam.py:2741` today (the arrival) | 45, 58, 19, 38 reads on the experimenter's streams; 183 and 311 over 32 Links |
| The turn by momentum under `action` | (T) on `Z_N` by the whole part of `abs(p) N` over h per Link stepped (record 155: an accumulator; today a floor re-pricing the history) | `by_clock(k0, abs(p) N, h)` today; `acc_action += abs(p) N` per Link, the carry per h ordered | `engine.py:637-645` | Bohr's r = 8 and 12 closing under the step drive (H) |
| lorentz-v1 (**design**) | the clock rows' rates multiplied by `sqrt(1 - f_c^2)`, `f_c` the drive's rate over light's on its line: a rate with one root at a declared grain, a seventh verb | `f_hat = floor(G f_c)`, `gamma_inv = isqrt(G^2 - f_hat^2)`, G = 2^20; the turn's rate `(content x n x gamma_inv, d G)` | light_speed/FORM.md section 4 | the muon's pins: ticks 71 and 126 for 64 |
| The balance (the books) | (T) on the ledger: `released = in transit + absorbed + escaped (+ cancelled)` per family, exact at every tick; the momentum balance per paid message | the audit per tick | `engine.py:880-1025` | conserved at every tick on every registered run |

## 5. The two non-linear places, named once more, and the classical-quantum boundary

The derivation's section 0 puts it exactly and this document keeps it:
the law is piecewise-linear in every component of the rows and in every
count at a fixed content, with bilinear rates in the feedback block (the
push is the reader's content times the arriving flow); the one threshold
read out is the click's comparison against the norm of the linear
evaluation. So there are two non-linearities and no third: the carry of
the Euclidean division (a bijection, information kept) and the click's
threshold (information discarded by design). A record is in the linear
block while its rows fly (its state at the click a closed form of its
birth, the quantum case), and a body is in the feedback block because
its rates read the crowd (iterated, its history in its accumulators, the
classical case); the boundary is crossed once per record at the click.
The meeting's root (section 4.3) and lorentz-v1's root are the two
places a third verb would enter, both declared grains, neither derivable
from the six; the owner names them or leaves them.

## 6. Every declared rounding at load, as a constant of the law

| Constant | What it rounds | Where |
| --- | --- | --- |
| C, S (the tables of N) | `cos, sin(2 pi k / N)` to the nearest 1 / 256 | `core/phase.py:57-90` |
| C', S' (the half-angle tables of 2N) | the same at the half angle, for the rotations | `amplitude.py:125-140` |
| `u_d` | the unit vector `Q D / abs(D)` to the nearest integer vector (exact under the 48) | `nature_beam.py:567-587` |
| `T_D` | `sqrt 3 abs(D) Q` rounded down by isqrt (the flight's resolution; within 1 / T_D of the isotropic pace) | `nature_beam.py:605-660` |
| the fan's weights at G (**decided**) | the angle covered by each direction, at the grain G (2^18 in the plane; 2^24, 2^14, 2^5, 2^15 on the sphere) | TWO_SLITS.md sections 7 and 10 |
| the half circle `N // 2` | exact for every N of the law | `nature_beam.py:1125` |
| the parser's ceilings | the static budgets of the columns and the flight bound | `world.py:474, 1303-1304` |
| the rung at the click | `(2 N C_k + T) // (2 T)`, the nearest integer, once per record (the comparison form on the branch) | `amplitude.py:192, 215` |
| the returned phase of a `wave` set | the pointer's nearest step of N | `nature_beam.py:967-999` |

Everything else is exact: the widths N, P, Q, W, K, S are sizes, not
roundings; every table read at run time (`flight.steps`, `flight.lines`,
`collision.forward`, the arcs' cache) is an exact cache of a rule above
and can be replaced by the rule integer by integer.

## 7. What differs from the derivation's F, in one line each

1. The drive is one accumulator on the momentum's direction, the flight's
   own, not one per axis (section 4.3; the owner's yes to c in matter).
2. The fan is an operator with the angular measure as its matrix, not a
   per-world list (section 4.1; the owner's yes to P).
3. The birth wheel is `Z_W` at the golden rate, not `Z_N` at rate 1
   (section 4.2; the form on the owner's word).
4. The phase at the click is read from the row's accumulators at the exact
   time of its last Link, not at the whole age (section 4.1; the owner's
   yes).
5. lorentz-v1 and the meeting's norm are named as the two roots, a
   seventh verb if admitted (section 5); F lists the meeting's root among
   its exceptions and does not name the seventh verb.

Nothing else differs: the state, the six verbs, the two blocks, the
threshold and the tables are F's.
