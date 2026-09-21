# exact-circle-v1: the click computed in the ring of the circle

The derivation mathematician, 2026-09-21, read-only on the tree; the
identity `exact-circle-v1`, beside the law until the owner's word. The
decision (the model owner, record 327, translated: "go with the beautiful
solution"): the exact circle, no rounding anywhere, the regular N-gon kept
exactly, the tables at 1/256 to leave; the click computed in the ring of
the circle, the group ring `Z[Z_N]` evaluated at the N-th roots of unity.
A rule change of the click under the three tests, by the method: the pins
before the run. The host map
[exact_circle_map.py](exact_circle_map.py) with its output
[exact_circle_map.out](exact_circle_map.out) prints every number below
from integers and fractions; its real embedding (`decimal` at 60 digits)
is used only to CHECK the integer identities, never for a number of the
design. Nothing is built, nothing is run.

**Notation, once.** N the circle's steps (64 and 4096 on the register); a
= 2 pi / N the step's angle; zeta the primitive N-th root of unity; theta
= 2 cos a; **f** the phase-count vector of a record's rows at one Node and
label, `f_j = 32 x amount` at the phase j in `Z_N` (amplitude.py's offer;
BEAM_LAW note 37 (xii)); A = sum_j f_j the summed amplitude; **c** the
autocorrelation of **f**; **e** the coefficient vector of a weight on the
ring's basis; **E** the 2 x N matrix of the tables C and S at the scale
256 (`core/phase.py`, `PHASE_COSINE_SCALE`); **G** = **E**^T **E** the
Gram matrix; W the birth wheel and u the record's birth coordinate on
`Z_W`; C_k the cumulative weight of the cells 1 .. k and T the total;
P a precision in bits.

## 1. The state and the weight

**Today.** The click's weight of a cell is the bilinear form `w = f^T G f`
with `G_jk = C_j C_k + S_j S_k` over the rounded tables (`core/phase.py`
`phase_gram`, record 188; `events/amplitude.py` `gram_form`, one arm; the
rank-2 factorisation `evaluate` and `cmul` for several arms, record 192).
Each table entry is `256 cos(d a)` or `256 sin(d a)` rounded to the
nearest integer, so it errs by at most 1/2 (the map's section 4: the
largest error 0.4868 at N = 64); `C_d^2 + S_d^2` runs from 65448 to 65773
against 65536, the eight totals of L1 (`65448 / 65536` to `65773 /
65536`, note 37 (xii)), a part in 276 on the norm; a Gram entry errs by at
most `2 x (256 x 1/2 + 256 x 1/2 + 1/4) = 512.5` on 65536, a part in 128
(the crude bound). The rounded evaluation is not a ring homomorphism, so
the several-arm click needs the tensor form (record 192).

**The exact form.** The weight is the square of the evaluation at zeta:

    w = |sum_j f_j zeta^j|^2 = sum over d in Z_N of c_d cos(d a),
    c_d = sum_j f_j f_(j+d)      (the autocorrelation; c_d = c_(N-d); integers).

The autocorrelation is the bilinear form B on **f** against its own
shifts (the vector verb), and every cos(d a) reduces to a basis by the
circle's symmetries alone, `cos((N/2 - d) a) = -cos(d a)`, `cos((N/4) a)
= 0`, `cos((N - d) a) = cos(d a)`:

    w = e_0 + sum over d = 1 .. N/4 - 1 of e_d cos(d a),
    e_0 = c_0 - c_(N/2),   e_d = 2 (c_d - c_(N/2 - d)).

So `2 w` is an element of the real subring `Z[theta]` of the cyclotomic
integers, written on the integer basis `1, 2 cos(a), 2 cos(2 a), ...,
2 cos((N/4 - 1) a)`: a vector **e** of N/4 integers (16 at N = 64, 1024
at N = 4096). It is a basis: `2 cos(d a) = P_d(theta)` with P_d the
Dickson polynomial (`P_0 = 2`, `P_1 = t`, `P_(d+1) = t P_d - P_(d-1)`),
monic of degree d, so the change to the power basis is unitriangular,
and `Z[theta]` has degree `phi(N) / 2 = N / 4` with the minimal
polynomial `Psi_N = P_(N/4)` (at N = 64: degree 16, the coefficients
`[2, 0, -64, 0, 336, 0, -672, 0, 660, 0, -352, 0, 104, 0, -16, 0, 1]`,
checked `Psi_64(theta) = 3 x 10^-55` at 60 digits; at N = 4096 degree
1024, its largest coefficient 707 bits, not needed by the build: the
basis is the cosines, not the powers). The sizes: `|e_d| <= 2 sum_j f_j^2
<= 2 A^2`. Two weights are equal exactly if and only if their vectors
are equal. The map checks the identity `e . cos = X^2 + Y^2` on random
vectors to `3.4 x 10^-53` at N = 64 and `3.7 x 10^-49` at N = 4096.

What this is on the law's own terms: the click of 6.5's lattice Gleason
at `c_1 = 1` exactly (the Born form `|ev(f)|^2`), with the rounded **G**
replaced by the ring itself; the exact evaluation IS a ring homomorphism
of `Z[Z_N]` onto `Z[zeta_N]` (for N a power of two `Z[Z_N] / (x^(N/2) +
1) = Z[zeta_N]`, 6.5), so the several-arm click is the ring product of
the arms' elements (`ring_product`, the convolution, already the exact
law's statement in note 37 (xii)) followed by one autocorrelation: the
tensor form and the complex pair `Z[i]` leave the code with the tables.
The detector's own record under `wave` (BEAM_LAW section 5, `X^2 + Y^2`
per interval, cumulative per detector and family) is the same element: a
vector of N/4 integers per detector, added per interval (the verb G), and
its threshold "the nearest integer to `(X^2 + Y^2) / 2^26`" a comparison
of the element with `(2 m + 1) 2^25`, the sign test of section 2.

## 2. The ladder made exact

**Today.** `b_k = (2 W C_k + T) // (2 T)`, integers over a common
denominator (`amplitude.py` `rungs`, `cell_of`, `node_choice`); the
click the cell k with `b_(k-1) <= u < b_k`.

**The exact test.** With `C_k` and `T` elements of the ring (their vectors
the sums of the cells' vectors, the verb G), the rung's comparison is one
sign: since `b_k = floor((2 W C_k + T) / (2 T))` and `T > 0`,

    u < b_k   if and only if   x_k = 2 W C_k - (2 u + 1) T  >=  0,

and `x_k` is formed exactly (integer scalings and additions of the
vectors: T and G). Its sign in bounded work: `2 x_k` is an algebraic
integer of `Z[theta]`; it is 0 exactly if and only if its vector is the
zero vector (the basis), so the tie needs no rule (the floor's own `>=`
decides it, as today); otherwise the norm over the N/4 conjugates `2
cos(d j a)`, j odd, is a nonzero integer, each conjugate is at most `2
sum_d |coefficient_d|` in size, hence

    |2 x_k| >= (2 sum_d |coefficient_d|)^-(N/4 - 1),

and a precision of `P = (N/4 - 1) log2(2 sum_d |coefficient_d|) + 2` bits
of the real embedding decides the sign with certainty (the map's section
2: at N = 64 and A = 2^20, 647 bits; A = 2^25, 797 bits; at N = 4096 and
A = 2^20, 43 991 bits). The embedding `cos(d a)` to P bits is law data at
load: `theta` by the nested square roots `2 cos(2 pi / 2^(k+1)) = sqrt(2 +
2 cos(2 pi / 2^k))` with the integer square root at the scale `2^P` (the
class of `T_D`'s load-time rounding, the three tests allow it), then the
Dickson recurrence in integers with `log2 N` guard bits; no rounded value
enters a weight, a rung or a record, only the one sign. The build first
tries 128 bits and refines to P only when the margin is below the error
bound; the worst case is P, fixed for fixed N and A. So the honest
statement is both: the work of one comparison grows as the two numbers
approach each other, AND it is bounded by P, a function of N and the
register's width, fixed local work for fixed N and A. The Node choice
within a cell (`node_choice`) is the same test with the Node's cumulative
weight and the cell's.

**The three tests.** Generic: one primitive (the autocorrelation, the
sums, the sign), no family name, no kind. Vector: B for **c**, G and T for
the vectors and the rungs, D for the sign on P-bit integers (the
comparison verb at a declared width P; no root at run time, the one
`isqrt` at load). Local: the click reads its own record and the
detector's set, as today; nothing at a Node. The one declaration the law
gains is P, derived from N and A at load, not chosen.

**The choice for the owner.** (a) The exact sign with P at load, as
above: no rounding anywhere, the comparison's cost bounded and rarely
above 128 bits. (b) A declared cutoff `P_0 < P` with a tie rule (a margin
below `2^-P_0` sends u to the lower cell): a rounding again, at `2^-P_0`
in place of 1/256. The design recommends (a); (b) is named so that the
choice is the owner's.

## 3. The pins before any run, from the exact form

Every number here is derived from the register's declared integers and
the bound of section 1; nothing is run. What can move is a click (a cell
chosen by u) and the norm; what cannot move is any phase, flight, count or
push (section 5).

- **Bell, `S(N, Q)` (22.3, 6.2).** The CHSH cells at N = 64 give `176 /
  64 = 2.75` unchanged: the design's own check `bell.txt` (line 6) already
  computed the cells "with the exact cosine's cells" at N = 256 (`720 /
  256` on both), and 6.2 records `S(N, Q)` unchanged by the tables' scale
  from 256 to `2^20` at N = 64, 256, 1024 and 4096, the rungs deciding;
  the exact circle is that limit. The marginals `32 / 64` stay exact. The
  bound's second term `16 arcsin(sqrt 2 / (2 Q))` vanishes: `S(N) -> 2
  sqrt 2` within `8 / N` alone. Readings that move: none of `176 / 64`,
  `2896 / 1024`, `11584 / 4096`.
- **The Mach-Zehnder arms (L1, `amplitude/expectations.json`).** Every
  phase of the ten worlds is a multiple of `N / 4` (the splitter's quarter
  turn, `phase_per_link` 0 or `[16, 1]`) or, on `mz_unequal_f8`, of `N /
  8`, where the two ports' weights are equal by symmetry; the tables are
  exact at the multiples of N/4 (`C = 256, 0, -256, 0`, the map), so the
  offers `1681 / 1682`, `1 / 1682`, `49 / 50`, `1 / 50`, `441 / 1682`,
  `200 / 841` are the exact form's already and the clicks `64 / 0`, `0 /
  64`, `32 / 32`, `63 / 1`, `17 / 15 / 32`, `16 / 16 / 32` do not move.
  The one reading that moves: the record's `total`, from the eight values
  `65448 / 65536` to `65773 / 65536` at u mod 64 to exactly `65536 /
  65536 = 1` at every u (the exact evaluation conserves the total at every
  declared split with `A = sum a_i^2`, 6.5's theorem, now exactly), so the
  design's bound "1 within 0.0019", pinned as failing
  (`tests/test_amplitude_layer.py`), passes.
- **Young's fringes and the cone (L2 `slits_low`, `tests/test_amplitude_cone.py`).**
  The measured cells' weights `32761 / 163840`, `1 / 5`, `32761 / 163840`
  carry the 45-degree entry `181` (`32761 = 181^2`) whose exact value is
  `128 sqrt 2` (`32768`): the three become `1 / 5` each, exactly (the
  map). A cell's weight moves by at most `256 A_k |ev(f_k)| + A_k^2 / 4`
  in the tables' unit (`|E_table - 256 E| <= 1/2` per entry), a part in
  256 of the largest weight; at W = 64 a rung therefore moves by at most
  one (the map: `64 x 237 / 65536 = 0.231 < 1`), and a click moves only
  where its rung lies within 0.231 of a half-integer. That is NOT rare a
  priori (a band of width 0.46 in the rung's fractional part), so this
  design does not claim the 64 clicks `34 / 15 / 15` unchanged: the pin
  is the replay of the registered records' weights under the exact form
  (`tools/amplitude_path.py --check` with the exact evaluation), written
  before the run; the same for the cone's clicks. The record's screen
  weights (Pearson 0.744 with the incoherent sum, 0.368 with the cosine)
  move by less than a part in 256: Pearson `0.744 +- 0.005`, `0.368 +-
  0.005`.
- **A10 (22.2).** The pin `w x FWHM / lambda = 0.92 +- 0.03` at `w27` and
  `0.886 +- 0.03` at `w9` stands: a part in 276 on the norm moves a full
  width at half maximum by less than 0.4 percent, inside the tolerance.
- **`slits_huygens` at 4096 births (W = 4096).** Registered: bright 19 to
  51 (the mean 39.3), dark 0 to 3 (the mean 0.68), the counts' Pearson
  0.891 with the cosine (the weights' 0.895), the visibility 0.966, every
  count within 2 of its width against the FIRST record's rungs (the
  tables' eight totals at u mod 64 made the rungs per record). Under the
  exact form the rungs are one ladder for every u, so the wheel's own
  statement tightens to "every cell within 1 of `4096 x` its weight over
  the total"; a cell's count moves by at most `W (A_k / A)^2 / 256 + W
  (w_k / T) / 256 + 1`, which at the brightest cell (51 of 4096, `w_k / T
  = 0.0125`) is below 2: **the pin**: every cell within 2 of its
  registered count, dark 0 to 3, bright 19 to 51 within 2 per cell,
  Pearson `0.891 +- 0.01`, visibility `0.966 +- 0.01`, and the histogram
  within 1 of the ladder for all 4096 births.
- **The case where the rounded and the exact click choose a different
  cell, and how rare.** A rung moves if and only if `W C_k / T` lies
  within `W x epsilon_k` of a half-integer, `epsilon_k` the tables' error
  on the ratio `C_k / T`, at most a part in 276 on the register (the
  norm's error) and a part in 128 by the crude bound: at W = 64 at most
  one rung step (the integer bound `ceil(64 x 237 / 65536) = 1`), at W =
  4096 at most 15 steps per rung but at most 2 per cell width (the
  difference of two adjacent rungs' errors is the one cell's). The
  fraction of rungs that move is not bounded a priori (up to 46 percent
  at W = 64); on the register it is 0 for Bell (`bell.txt`) and 0 for L1
  (exact phases), and for L2 and `slits_huygens` it is what the replay
  counts before the run.

## 4. The widths

- **The register bounds.** `|e_d| <= 2 A^2` with `A = 32 x` the record's
  summed amount: on the registered amplitude worlds (K = 2^20) `A <=
  2^25`, so `|e_d| <= 2^51`, within `2^62 - 1` as a Python integer of the
  host (the record is a report of the host, never refused, BEAM_LAW
  section 5); a weight is N/4 such integers (16 at N = 64, 1024 at N =
  4096). The sign test's precision: 647 bits at N = 64 and A = 2^20 (797
  at A = 2^25), 43 991 bits at N = 4096 (54 221 at 2^25) in the worst
  case; 128 bits first.
- **The host cost against today.** The Gram matrix has `N^2` entries
  (4096 at N = 64; 16 777 216 at N = 4096, stored through N = 512 and
  formed beyond); the exact form stores no matrix: N/4 integers per
  weight and per cumulative rung, the autocorrelation `s^2` products for
  a vector with s nonzero phases (at most N; the sparse vectors of the
  register have s of order the rows per Node), one P-bit inner product
  over N/4 terms per sign at the worst precision, one 128-bit one
  typically. The `decimal` check of the map (60 digits) took the bulk of
  its time at N = 4096; the build's integers do not.
- **N and W.** N stays a width of the law: the circle `Z_N` is the group
  itself, the rows' phase its element, and the exact form removes the
  tables' scale 256 (a width of the computation), not N. W stays the
  ladder's resolution (`u` on `Z_W`, the birth wheel of note 46); `W = N`
  under the default rate `[1, N]` is a coincidence of the default and not
  an identity, and the exact form does not make them one thing: the
  phases live on `Z_N`, the clicks' coordinate on `Z_W`, and the rungs
  compare `W C_k` with `(2 u + 1) T` in the ring. The one width the exact
  form adds is P, derived from N and A at load, not declared.

## 5. What the build touches, and what it must not

**Touches.** `core/phase.py`: `phase_cosines`, `phase_sines`, `phase_gram`,
`PhaseCircle.vector` and `PHASE_COSINE_SCALE` leave; in their place the
ring's representation (the vector of N/4 integers, the reduction of
section 1) and the load-time P-bit embedding for the sign test.
`events/amplitude.py`: `evaluate`, `gram_entry`, `gram_form`, `Complex`
and `cmul` (the `Z[i]` path) leave; `ring_product` becomes the
several-arm click; `rungs`, `cell_of`, `node_choice` take ring elements
and the sign test. `events/nature_beam.py`: `coherent_pointer`,
`pointer_units`, `pointer_phases` (the set's phase after a click, the
nearest step to the pointer, becomes a sign test of `Im(ev(f)
zeta^-k)`), `moment_table`, `reading_fits`, `read_groups` (the detector's
record and threshold, BEAM_LAW section 5). The tools that replay a
register: `tools/amplitude_path.py`, `bell_chsh.py`, `bell_choosers.py`,
`buildup_readings.py`, `bohr_readings.py`, `heisenberg_readings.py`. The
tests: `test_amplitude_gram.py`, `test_amplitude_layer.py` (the total's
bound now passing), `test_amplitude_gate.py`, `test_group_structure.py`,
`test_nature_beam_detector.py` and the detector tests that pin a
`record` integer. ENGINE.md's readings by type (the record a vector of
the ring). The runs re-registered once on the owner's word, with the pins
of section 3 written first.

**Must not touch.** The six verbs; the rows' phase as a step of `Z_N`
(note 45's exact phase at the click stays an integer step of the circle:
the exactness here is the weight's, not the phase's); the flight (`T_D`,
the Manhattan accumulator, the deficits); the crossing rule (note 48);
the meeting; form B (the directional drive); the fan and its angle
weights (integers at `2^18`, record 163); the birth wheel W and u (note
46); the family table; every count of the fraction-free law.

## 6. The verdict of the design

The exact circle is one bilinear form on the record's own vector, whose
value lives in a ring of integers of degree N/4, with equality exact by
the vector and every strict comparison decided in bounded work by the
separation bound of the ring; it removes the tables, the Gram matrix, the
complex pair and the tensor form of record 192 at once, and it makes the
click's unitarity exact (the total 1 at every u). It passes the three
tests with one declared width, P, derived at load. What it costs is the
worst-case precision of a comparison at large N, bounded and stated. What
it moves on the register: the `total` of L1 to exactly 1, the two-slit
measured cells to `1 / 5` each, and some clicks of L2 and `slits_huygens`
by one cell where a rung sits within the tables' error of a half-integer,
to be counted by replay before the run; Bell, the arms, A10 and the
4096-birth fringes keep their pins. The physics-rule review follows, then
the build, then the runs once on the owner's word.
