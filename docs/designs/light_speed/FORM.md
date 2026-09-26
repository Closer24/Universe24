# c in the vector law: the statement completed, the drive on the rows' flight table, and lorentz-v1 (read-only, the mathematician, 2026-09-21)

On the Boss's item A after the owner's word "everything moves to vectors
and operations, including c" (record 182) and his yes to (i) the c
statement completed, (ii) the drive on the momentum's direction in
the rows' flight table, (iii) lorentz-v1 as a hypothesis. Every integer is from
`light_speed_map.py` beside this file (`light_speed_map.out`, 32 s: the
engine's `by_drive` and its world loader imported, nothing else). Nothing
built, nothing run, nothing registered; the pins are the map's.

Amended on 2026-09-21 after the physics-rule review of the build (section 3.1: M1 and the correction; the map `drive_residue_map.py` beside `light_speed_map.py`).

Notation (the owner's rule, record 184): every symbol is named in English at its first use and a Greek letter is written as a word (gamma, tau, phi, zeta); a scalar is plain (c, M, N, Q, gamma), a vector is bold lowercase (**p** the momentum vector, **s** the state vector on the torus, **r** the rate vector, **e** the step's unit vector), a matrix or an operator is bold uppercase (**F** the interval's map, **C** the coupling matrix), and a component is plain with its index (p_a); the direction vector keeps its uppercase letter D as in BEAM_LAW, where T_D is its resolution, the one exception, and inside code spans and code blocks every symbol is plain.

## 1. The statement of c, completed

**c = 1 / sqrt 3 Links per interval is the meeting of the lattice's L1
walk with the Euclidean flight.** A row makes at most one Link per
interval (the walk is Manhattan: `m(tau + 1) - m(tau)` is 0 or 1, tau the
age and m the Manhattan count), and it
flies straight (its Euclidean displacement after a period is the
direction vector D, with S_1 its Manhattan length and T_D its
resolution). The Manhattan pace on D is `S_1 Q / T_D` with `T_D =
isqrt(3 |D|^2 Q^2)`, and `3 |D|^2 >= S_1^2` (Cauchy-Schwarz) is exactly
the statement `S_1 Q <= T_D`: at most one Link per interval on every
direction, with equality on the cube diagonals, where three Manhattan
steps make one Euclidean sqrt 3. So `1 / sqrt 3` is the largest isotropic
Euclidean speed at which no primitive direction crosses two Links in one
interval (`1 / sqrt n` in n dimensions; the plane world uses space's
table, BEAM_LAW section 3). Checked on the map over the 1 780 418
primitive directions with components within 64: `S_1 Q <= T_D` on every
one, equality on the 2072 with |a| = |b| = |c| (T = 192 = 3 x 64), the
Euclidean pace `Q |D| / T_D` from 0.5774 to 0.5818 (isqrt's rounding; 64
/ 110 on a heading), and record 144's cone is its run-time check (17
Links on the axis and 24 on the staircase at age 29). The rows are fine;
the statement that was missing is the bodies' half.

## 2. The bodies' half: today's step rule outruns the rows

The step rule is per axis: a body of content M (a scalar) and momentum
vector **p** with the component p_a on the axis steps one Link on that axis per `D_a / |p_a|` self-creations, `D_a =
Q S M + |p_a|` (`engine.py:85-116`, `world.py:447-455`), so its axis speed
is `v_a = |p_a| / (Q S M + |p_a|)` Links per interval. Its shape is the
relativistic `v = p / sqrt(m^2 + p^2)` (v the speed, p the momentum's
magnitude, m the mass, scalars) written with the lattice's L1 norm
(`m + |p|` in place of `sqrt(m^2 + p^2)`), and its cap is therefore the
Manhattan cap, one Link per interval = 1.72 c, not c: a body outruns its
own family's rows above `|p| = 1.39 Q S M` (the derivation's 4.4). The
dispersion, in units of c on a heading (`light_speed_map.out` B):

| p / m | today, `p / (m + p)` | form A, `c p / (m + p)` | form B, `p / (m + p / c)` | relativity, `p / sqrt(m^2 c^2 + p^2)` |
| --- | --- | --- | --- | --- |
| 1/16 | 0.101 | 0.059 | 0.097 | 0.107 |
| 1/4 | 0.344 | 0.200 | 0.301 | 0.395 |
| 1 | 0.859 | 0.500 | 0.632 | 0.864 |
| 3 | 1.289 | 0.750 | 0.838 | 0.982 |
| 9 | 1.547 | 0.900 | 0.939 | 0.998 |

**Which registered worlds outrun the rows.** At the declared momenta (the
map's scan of the 47 world files with a moving body, content = amount +
held): the orbit series D at width S = 1, `orbit/s1_r12` and `s1_r24` (a
body of content 1 with momentum 192: v = 192 / (64 + 192) = 0.75 Links
per interval = 1.29 c), above c from the first interval; the others
below it: `orbit/s8_*` at 0.385 (0.66 c), the hubble throws at 0.349
(0.60 c), G2's stars at 0.033 declared and 0.289 (0.50 c) at their
run-time momentum of 1.14 x 10^14 (GRAIN.md), the fastest coasting star
reading z = 0.2636 (the derivation's 4.5), bohr's electron at 0.054 and
the nucleus pairs at 0.005. The doppler bar's "outrunning at 0.75"
(push_relative_speed/FORM.md, `tests/test_doppler.py` (b)) is a test
fixture, not a world file. So the register has one series above c (D at
S = 1) and several between c / 2 and c.

## 3. The vector form that inserts c into the bodies: one flight primitive for rows and bodies

**The rule.** A body walks the DIGITAL LINE OF ITS MOMENTUM'S DIRECTION
at the pace its momentum earns on that line, with the rows' pace as the
cap. In the counts' one mechanism (record 150, the translation of **F**,
the interval's map, on one component with a wall; **p** the momentum
vector, D its direction, S_1 and T_D the direction's Manhattan length and
resolution; plain in the block):

    D     = the direction of the world's table nearest to p (the primitive p / gcd(p) itself when within the table's bound),
            chosen by the exact comparison (p' . D)^2 |D'|^2 >= (p' . D')^2 |D|^2 with p' . D > 0, p' = p shifted to components within 2^20
    rate  = |p|_1 x S_1 Q,   wall = Q S M x S_1 Q + |p|_1 x T_D       (form B; |p|_1 = sum |p_a|, the lattice's own norm of p)
    step  = by_drive(drive, rate, wall, at_most = 1) on the Bresenham line of D   (one Manhattan accumulator, the line's deficits as a row's)

so that the body's Manhattan pace is `v_M = |p|_1 S_1 Q / (Q S M S_1 Q +
|p|_1 T_D)` Links per interval: at a small momentum it is `|p|_1 / (Q S M)` on the
line, whose Euclidean speed is `|p|_2 / (Q S M)` on every direction
(`|p|_1 = k S_1`, `|p|_2 = k |D|` for p = k D: Newton's limit, isotropic,
today's momentum unit kept), and as the momentum grows it bends to the
rows' pace
`S_1 Q / T_D` on that line, never above it. The map's check (B, form B at
p / m = 1 on (1, 0, 0), (1, 1, 0), (1, 1, 1), (3, 1, 0)): the Euclidean
speed over 600 intervals 0.3667, 0.3182, 0.2887, 0.3336 against the
formula's 0.3678, 0.3187, 0.2887, 0.3340, the direction's own T_D the only
anisotropy (the L1 norm in the fraction and isqrt's rounding), within
the flight table's own 1.35 percent. Form A (the fraction `|p| / (Q S M +
|p|)` of the rows' pace, `v = c p / (m + p)`) is the same primitive with
the wall `Q S M x T_D + |p|_1 x T_D`; it rescales every registered speed
by c (Newton's limit becomes `v = c p / m`, the momentum unit changes),
so form B is the recommendation: the same Newtonian regime as today, c as
the cap, the momentum unit untouched.

**One flight primitive.** The derivation's section 1.3 gives a row's
flight as one Manhattan accumulator (rate `2 S_1 Q`, wall `2 T_D`, started
at the half) with three deficit accumulators carrying `S_1` from the
largest (the line). A body's drive above is THAT accumulator with its
rate multiplied by the momentum's fraction: `by_drive(|p|_1 S_1 Q, Q S M
S_1 Q + |p|_1 T_D)` is `by_drive(S_1 Q, T_D)` when `Q S M = 0` or `|p|_1
-> infinity`, and the deficits are the same three. Checked on the map (D):
on (1, 0, 0), (1, 1, 0) and (5, -3, 2) the flight table's row and the
directional drive at M = 0 are at the same Node after every one of 300
intervals. So rows and bodies share one flight primitive, a row being
the body of no content (the fraction 1), and the difference between a
row and a body in flight is one number, the wall's second term `Q S M x
S_1 Q`. When the push changes **p**, the rates change (the feedback block
of **F**,
the direction and the fraction re-read from the record) and the
accumulators keep their residues: nothing is discarded, the line
re-targets from where the body stands. The sizes: `|p|_1 T_D` within
`2^62`: for `|p|_1` up to 2^47 at T_D up to 8300 (2^13) the wall stays
within 2^60; larger momenta are refused at the push as today's bound is.

**Its effect on the registered pushed worlds (bit-exact, the expected
direction).** No world with a moving body is byte-identical: on an axis
the speed becomes `v / (1 + v (T / Q - 1))` of today's `v = |p| / (Q S M +
|p|)`, that is `1 / (1 + 0.72 v)`; the first interval at which the Links
part is the first step for a fast body and later for a slow one. From the
map (D) and section 2: the k = 4 reader of record 153 makes 84 Links in
400 intervals in place of 100 (0.84; the drives part at interval 4), the
k = 8 reader 45 for 50 (0.90; interval 8), G2's fastest star 95 for 115
(0.83; the z readings of series G2 fall by the same factor, since z reads
v / c), the orbit body of D at S = 1 from 1.29 c to 0.84 c (0.65 of
today; the orbits of D and H re-close or not at new radii, since the
push per interval is unchanged and the speed is lower: the closure moves
toward larger radii at the same momentum), bohr's electron 0.96 of today
(its closure condition moves by 4 percent), the nucleus and binding pairs
at 0.005 within one step over 700 intervals (a step's tick may shift by
one), sun_planet and the hubble throws by 0.7 to 0.8. The 87 worlds with
no moving body are byte-identical. A diagonal momentum now walks the
diagonal's digital line (one Link per interval at most, the line's
order) in place of the per-axis staircase with the coincident fire
dropped (the derivation's 1.3 item 7 is closed by construction: one
accumulator, one Link, nothing dropped).

**The meeting and the crossing rule under it.** The meeting reads at
co-location per interval and is untouched. The crossing rule (record 158)
reads a body's step by its own Link, the signed axis unit vector **e** of
the step:
under the directional drive the step is the line's next step, still one
Link on one axis per interval, so C1, C2 and the leapfrog exclusions
apply as written with **e** the line's step; the rule's proof covers at most
one Link per two intervals (`v_M <= 1 / 2`), which under the cap is every
body below 0.86 of the rows' pace on a heading; above that the rule is
local and generic as record 158 says and unproved, to be extended to one
Link per interval. The contact (a refused step onto an occupant) is the
line's step refused, as today.

### 3.1 Amended after the physics-rule review of the build (M1): the residue across lines, and the correction

**The finding (M1, the reviewer's, on PR #526 at fe911492; reproduced
here).** Under form B as built the accumulator's unit is the line's: the
rate and the wall both carry `S_1` (and `T_D`), so a residue r means
`r / wall` Links on that line; at a change of D at a constant `|p|_1`
the residue is kept and read against the new wall, and the distance it
holds multiplies by `wall_old / wall_new`, between `1 / (3 P)` and `3 P`
at the bound P (192 at P = 64); a residue of a long line discharges as
consecutive Links on a short one, one per interval, above the pace the
momentum earns. Reproduced on the same integers
(drive_residue_map.py (`docs/designs/light_speed/drive_residue_map.py`, deleted 2026-09-26) (A), its output
[drive_residue_map.out](drive_residue_map.out)): at `|p|_1 = 6000`, M =
64, S = 1, the residue 0.585 Link of the (3, 1, 2) line's wall (4056864)
is 2.575 Links of the heading's (922144): four Links in the first four
intervals on the heading where the pace earned is 0.416. Over 1000
intervals at a constant `|p|_1` with the direction cycling through five
lines (part (B)) the build makes 348 Links for a driven distance of
512.6, off by 165 Links at some n. So the build breaks its own contract
(the count the whole part of the distance driven; nothing discarded;
never above c) and record 301's condition is not met, as the reviewer
says. **M1b, a second place, found here.** The deficits are in the line's
unit too (each gains `|D_a|` per Manhattan step and the stepped one loses
`S_1`); carried across lines they order the Links by the old line: from
(1, 64, 0) at its x deficit 30 to the momentum (0, 6500, 0), purely along
+y, the body makes 30 Links on -x before its first y Link (the sign rule
gives -1 on an axis D lacks; part (A)). A correction must close both; a
re-read of the drive alone leaves M1b.

**Why no accumulator with a line-independent unit carries form B's
pace.** The intervals per Manhattan Link on D are `Q S M / |p|_1 + T_D /
(S_1 Q)`, and the second term is the rows' own Manhattan pace on the
line, which differs per line (110 / 64 on a heading, 156 / 128 on (1, 1,
0), 1 on the cube diagonal); an accumulator of Manhattan distance with
form B's cap therefore carries the line's constant in its wall, and the
lattice has no exact Euclidean unit (`T_D` is already an isqrt). So an
exact form with form B's Euclidean-isotropic cap and one line-independent
unit does not exist; the correction changes the cap off the headings.

**The three forms the Boss named, each under the three tests, the pace,
the cap and the reviewer's pin.**

(a) *A rate and a wall without `S_1`*: `rate = |p|_1 Q`, `wall = Q^2 S M
+ |p|_1 T_h` with `T_h = isqrt(3 Q^2) = 110` the heading's resolution,
one accumulator on the line of D with the line's deficits. The drive's
unit is then line-independent and M1 closes, but the deficits keep M1b
(their exact re-read is a rational with the old `S_1` in the
denominator, their reset makes a body that changes line every interval
step on its largest component alone). Not sufficient alone.

(b) *The residue re-read at a change of line*, `r -> r x wall_new /
wall_old`: exact only as a pair (the numerator `r x wall_new` over the
denominator `wall_old`), whose denominator compounds at every change
(`wall_old x wall_old' x ...`): unbounded storage on the record, against
LOCALITY-1's fixed storage; with a floor, a declared rounding below one
unit of the new wall per change, below `1 / (Q^2 S M)` Link, accumulating
to `n / (Q^2 S M)` Links over n changes (a pushed body changes line at
every self-creation): the owner's word, and the deficits would need the
same re-read with their own rounding (below `1 / S_1'` of a step per
axis per change). Stated for his decision; not recommended.

(c) *The residue owned per axis*, RECOMMENDED: three signed accumulators
`drive_a` on the body's record, the rate `p_a Q` on each, the ONE wall

    W = Q^2 S M + |p|_1 T_h,   T_h = isqrt(3 Q^2) = 110,

every accumulator advancing at every self-creation, one Link per
interval at most: the axis furthest over the wall steps (the lowest axis
on a tie), its accumulator loses W with the Link's sign (the
accumulator's), the others keep their overflow for the following
intervals; a reversal cancels first (the signed accumulator, record
126); `p = 0` never steps. No direction read, no bound P, no deficits:
the per-axis rule of note 17 with one wall in place of three, and the
Link deferred in place of dropped. The three tests: generic (the
integers `p_a`, M, S and the constants Q, `T_h`; no family name, no
kind), vector (T on three accumulators against one wall, a comparison
for the order; no root, no float), local (the body's own record, fixed
work). The pace: per axis `|p_a| Q / W`, Manhattan `|p|_1 Q / W`, that
is `Q S M / |p|_1 + T_h / Q = Q S M / |p|_1 + 1.72` intervals per
Manhattan Link on every direction; on a heading `|p| Q / (Q^2 S M + 110
|p|)` is form B's `|p| x 64 / (Q S M x 64 + 110 |p|)` exactly, so
`1 / (1 + 0.72 v)` survives on a heading and on an axis unchanged, and
the axial registered worlds read as under form B; off the headings the
pace is below form B's (part (C): at `p = Q S M`, 0.632 of the rows'
heading pace under both forms on a heading, 0.501 against 0.631 on (1,
1, 0), 0.432 against 0.629 on (1, 1, 1)). The cap: the Euclidean pace
`|p|_2 Q / W <= Q / T_h = 64 / 110`, the rows' pace on a heading, on
every direction, and on the line of D at most `|D| Q / (S_1 T_h)`
against the rows' `|D| Q / T_D` there, the ratio at most 1 over the 4034
primitive directions within 8 with equality on the six headings and
0.577 on the cube diagonal (part (C)): "never above c" becomes true and
a body never outruns its family's rows on any line (record 301's
condition), at the price that the cap is the Manhattan-isotropic 64 /
110, a fast body on a diagonal slower than its rows by up to `1 / sqrt
3` (the Euclidean-isotropic cap of form B is not reachable exactly,
above). Newton's limit `|p|_2 / (Q S M)`, isotropic on every direction,
unchanged. The reviewer's pins for the re-run, on the map (B): (1) at a
constant `|p|_1` with a wandering direction the wall is constant, each
axis's count is exactly `floor(sum_t p_a(t) Q / W)` at every n (the
signed sum; `by_drive` with a constant wall), and the Links crossed lag
the count by the deferral only, within 2 at any n (112, 112, 83 Links
against the whole parts 111, 111, 83 after 1000 intervals of five lines;
the build 348 against 512.6); (2) a one-interval hand-over transient
cancelled within the tick leaves at most `|delta_a| Q / W` Link as a
residue on its own axis and fires nothing (-0.086 Link on y, no Link in
the 100 intervals after; the build's two re-reads change the distance
held by +0.60 Link). What changes for the register: the axial movers
read as under form B; the diagonal and orbit worlds (series D and its
lamp worlds, sun_planet, bohr, the off-axis hubble throws) move again
and are re-pinned by the implementer from (c)'s pace (row 58's pins
under form B carry the heading's pace and stand); a body's path is the
per-axis staircase within one Link of the digital line (the order by
overflow), and DERIVATIONS 1.3 item 7 stays closed (nothing dropped, the
coincident fire deferred). (c) needs no declared rounding: the
implementer builds it on this PR's SHA; only (b) would need the owner's
word.

**S1, S2 and S7 of the review.** Under (c) the direction read leaves the
rule (no shift, no bound P, no read's grain) and 24.1's ledger gains no
row: the three are closed by removal. Should the owner keep the line ((a)
or (b)), they are FORM.md's: S1, section 3 declared the shift to
components within `2^20` and the build reads within `2^k`, `k = 29 - 2
bits(P) = 15` at P = 64 (note 49): the built value is the one the 64-bit
comparison admits (`(p' . D)^2 |D'|^2` within `2^63` needs p' within
`2^15` at |D| up to 3 P), and section 3's `2^20` is amended here to
`2^15`, a precision `2^-15` against the table's half step `2^-7`; S2, at
a larger bound the shift shrinks with `k = 29 - 2 bits(P)` while the
candidates' angular spacing shrinks as `1 / P^2`, so the read tells
neighbouring candidates apart only while `2^-k <= 1 / (2 P^2)`, that is
`bits(P) <= 7`, P below 128: the bound stays at 64 unless the comparison
is widened beyond 64 bits; S7, the read's grain (P and k) is an input of
the law and would take a row of 24.1's ledger, "the direction read's
grain, INPUT", to be added there only if the line is kept.

## 4. lorentz-v1, stated so that it can fail

**The rule.** The rate of a body's clock, its turn and its owed count,
is multiplied by gamma (the Lorentz factor), read from the body's own
drive (f_c the speed in units of c, G the grain, scalars; plain in the
block):

    f_c      = |p|_1 T_D / (Q S M S_1 Q + |p|_1 T_D)          (the drive's rate over a row's rate on the same line: the speed in units of c, exact rational)
    f_hat    = floor(G f_c),   gamma_inv = isqrt(G^2 - f_hat^2),   G = 2^20
    the turn's rate (content x n, d)  ->  (content x n x gamma_inv, d x G);   the owed count's rate likewise

one row of the counts table each, their rates carrying one integer
square root per interval at a declared grain. Is it one of the six
operations? The accumulator is (the whole part of an accumulated rate on
the record, the feedback block of **F**, the rate a function of the state as the
push's is); the root is not: none of the six verbs takes a root, and the
derivation's 10.4 says so for the contraction. The honest statement:
lorentz-v1 is a torus operation only if a seventh verb is admitted, the
root at a declared grain, the same class as the meeting's `isqrt` at run
time (the derivation's 1.3 item 10) and as `T_D` and `u_d` at load; the
grain's discard is bounded (2^-20 in the rate) and does not accumulate
(the accumulator holds the residue exactly). The owner's decision is
whether that verb exists; if not, gamma stays a limit of the law
(HYPOTHESES 21) and this section is its integer form for the record.

**The test: the muon of series J4, the integers pinned** (M = 207, S = 1,
`Q S M = 13248`, the clock at rate [1, 1], `become` at 64 turns; the map's
E). HYPOTHESES 21's momenta 69 and 207 were written before the Q factor of
the divisor: with Q = 64 they give v = 0.005 and 0.015 Links per interval,
not 1 / 4 and 1 / 2, to be corrected there. Under form B the two speeds
of the test are the fractions `f_c` = 0.43 and 0.86 of c:

| `f_c` | p (label units) | v under form B, Links per interval | gamma | the 64th turn (today: tick 64 at every speed) | the range (today 16 and 32 Links) |
| --- | --- | --- | --- | --- | --- |
| 0.43 | 5815 | 0.2502 | 1.108 | tick 71 | 17 Links |
| 0.86 | 47349 | 0.5004 | 1.960 | tick 126 | 63 Links |

Refutation of lorentz-v1 in a run: a trigger tick other than 71 and 126
(within one), or a rate depending on the direction of motion beyond the
flight table's 1.35 percent. Refutation of today's law (HYPOTHESES 21):
any tick other than 64.

**The derivation's section 10, reconciled.** The derivation finds that the
bond as a light clock (relativity's term) slows in motion by MORE than gamma (the round trip
1.383 x rest at v / c = 0.43 against gamma 1.107; 1.173 against 1.024 at
0.21) and is lossy, and that the contraction gamma would need is a root
of the state, not one of the six. Both stand with this section: (i) no
six-verb rule gives gamma, agreed; lorentz-v1 imposes it as a rate with
the seventh verb, it does not derive it; (ii) the exchange clock of 10.4
(a body self-creating on its bond's round trip) and lorentz-v1 are two
different clocks and cannot both be the body's: a body with both would
slow by the product 1.383 x 1.108 at 0.43 c. The runs decide: 10.5's
pair in motion reads the exchange clock (a slowing larger than gamma,
anisotropic, lossy, no contraction), J4 reads lorentz-v1 (gamma, one
number, isotropic); nature's muon is the second. If the owner takes
lorentz-v1, section 10's bond clock becomes a second, emergent slowing
that the register must not also count, and the physicist decides which
one a bound body's clock is; if he does not, HYPOTHESES 21 stands and the
bond clock is the law's only slowing in motion, at 1 + 2 / k on the axis.

## 5. The three lines for the owner

1. c is complete when the bodies' half is written: one flight table for
   rows and bodies, a row the body of no content, c the cap of every
   drive (section 3, form B), which makes every moving body's registered
   speed `1 / (1 + 0.72 v)` of today's and re-registers the 47 worlds with
   a moving body once, the orbit series D at S = 1 (1.29 c today) first.
   Amended (3.1): the build's residue across lines (M1, and M1b in the
   deficits) is closed by form (c), three accumulators with one wall
   `Q^2 S M + |p|_1 T_h`; the pace on a heading unchanged, the cap 64 / 110
   on every direction, no direction read.
2. The drive on the momentum's direction is the same accumulator as the
   flight's, one row of the counts table; nothing new in the six verbs.
3. lorentz-v1 needs a seventh verb (a root at a grain); with it the muon's
   pins are ticks 71 and 126; without it gamma stays HYPOTHESES 21's
   limit; and it and the derivation's exchange clock are two clocks, of
   which a body can have one.

> The scripts of this folder (`drive_residue_map.py`, `light_speed_map.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/light_speed/<script>`).
