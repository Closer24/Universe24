# The cause of the widening at r = 12, read from the baseline's records by algebra, before the pins of atom-give-momentum-v1

The Atom Give Designer 2, 2026-09-22, on the model owner's word through
the Boss (record 935: the atom's baseline shows something to solve
first): one bounded section, ALGEBRA FIRST, no new run. The records read
are the Atom Baseline Runner's, on `main` at 384b15c6:
`docs/designs/atom_baseline/RUN.md` (sections 3 and 4) and
`docs/designs/atom_baseline/baseline_readings.out`; the run's events
(`artifacts/atom_baseline/events.jsonl`, 369 MB) are not in this
checkout, so every number below is the `.out`'s, by the runner's kind,
and every derived number is GAMEBOARD by formula. The algebra is
[ALGEBRA.md](../atom_algebra/ALGEBRA.md) sections 1 to 3 and
[PINS.md](../atoms/PINS.md) section 2; the flow's factor is the
reviewer's line of record 872 and the Flow Weight Designer's
[DESIGN.md](../flow_weight/DESIGN.md) (flow-link-v1, record 898, PR
#854). Bohr's and Kepler's forms appear only as the thing compared with
(record 817). Nothing here moves a pin, a rule or a world.

**The finding in one line.** The widening is not a shortfall of the
radial push: no push factor gives the crossings read (a conic from the
start has its far side at half a turn and comes home at the full turn,
against 13, 13, 17, 26 Links and no home); the loop's angular momentum
and its energy both RISE over the first three quarters of a turn (L by
30 percent, E by 45 percent of its bound value, GAMEBOARD by formula
from the crossings' momenta), which a central push cannot do: the push
the electron received had a tangential part along its motion of about
5 percent of its radial part. Candidates (i) to (iii) each change the
radial push's size or the pace and none makes a torque: NOT ACCOUNTED.
The torque's source is a rule of the push or the drive that the
algebra does not carry (iv), and the reading that names it is already
in the baseline's records (the electron's 305 `read` lines and its step
lines), a host reading and no run. Under flow-link-v1 the radial push
in the plane falls by 1.287 and the declared momentum is 13 percent
above the key's circle; the key does not touch the torque, so the loop
does not close under it either; the baseline the momentum give is read
against stays the register's as the law stands (section 3).

## 1. The loop's shape, and the push it implies

**The readings** (RUN.md section 4; the kinds the runner's): the
crossings +y at count 412 at 13.00 Links, -x at 851 at 13.00, -y at 1302
at 17.00, +x at 2191 at 26.00 (DETECTOR, the arrival Nodes); the
momentum's length at the crossings 283, 308, 273 and 182 million label
units, the start's 294 (GAMEBOARD, the step lines); the escape through
`face:+y` at 3407 at (29, 52) with the momentum (-172 906 816, 35 392
088, 0) (DETECTOR, the escape line); the dwell 20.0 counts per Link over
the twelve hops inside r = 17 (DETECTOR); the radius least 12.00,
greatest 27.86 (GAMEBOARD).

**The balance the algebra declared** (ALGEBRA.md section 2 (a); RUN.md
section 3, P2): on `main`'s drive the circle at r = 12 needs `p_c = 288
249 497` (the balance `p v / r = F` with `F = 16 M Q E_body(r) / 10`,
`E_body(12) = 6.588` entries per shell counted from the engine's own
flight lines through the electron's three Nodes, `v = p / (Q S M + p)`,
`Q S M = 5 301 780 480`); the declared momentum 293 783 192 is 1.0192 of
it (form B's circle, PINS.md section 2). In the inverse-square limit
this alone gives the loop's constant `E = p^2 / (2 m_i) - kappa / r` with
`kappa = p_c^2 r / m_i = 1.881 x 10^8`, `a = r / (2 - (p / p_c)^2) =
12.48` Links, the far side 12.97 at half a turn, home at 12 after one
turn, T = 1552.

**(a) A push factor fits no crossing.** Let the push the law delivered
be f times the balance at the start (the start's momentum tangential,
the push central). Then `E = v^2 (1 / 2 - f)` in the limit's units, the
loop is a conic with

    a = f r / (2 f - 1),   e = 1 / f - 1,   the far side r / (2 f - 1) at HALF a turn, home at r after ONE turn   (f < 1: the start is the near side; f > 1: the far side).

The far side read is 26 at the FULL turn: `r / (2 f - 1) = 26` needs `f
= 0.731` (the push 27 percent short), which puts the far side 26 at half
a turn and the electron home at 12 at 2191; read: 13 at half a turn, 26
at the full turn, no home, and the radius still growing to 27.86 after
it. At the dwell's f (section 2 (ii)) or the momentum's 0.963 the far
side is 13.3 or 13.0 and home at 12. No factor fits: the loop is not a
conic of any central push. GAMEBOARD by formula.

**(b) The energy and the angular momentum at the crossings.** With the
declared `kappa` (inverse square) and, beside it, the lattice's ring
flux `r^-1.83` (ALGEBRA.md section 2 (d), matched to the same push at r
= 12), the loop's constant at each crossing from `abs(p)` and r, in
units of `10^6` label units squared per `m_i`:

| The crossing | r | abs(p), million | T = p^2 / (2 m_i) | E, inverse square | E, r^-1.83 | L = r x abs(p), at most |
| --- | --- | --- | --- | --- | --- | --- |
| the start | 12 | 293.8 | 8.14 | -7.53 | -10.74 | 3.53 x 10^9 (exact: p tangential) |
| +y at 412 | 13 | 283 | 7.55 | -6.91 | -10.11 | 3.68 x 10^9 |
| -x at 851 | 13 | 308 | 8.95 | -5.52 | -8.72 | 4.00 x 10^9 |
| -y at 1302 | 17 | 273 | 7.03 | -4.03 | -7.11 | 4.64 x 10^9 |
| +x at 2191 | 26 | 182 | 3.12 | -4.11 | -6.81 | 4.73 x 10^9 |
| the escape at 3407 | 26.17 | 176.5 | 2.94 | -4.25 | -6.95 | 4.60 x 10^9 (exact: the vector is read) |

Under either force law the loop's constant rises from the start to the
third crossing (by 3.5 of 7.5 under the inverse square, by 3.6 of 10.7
under `r^-1.83`) and is then flat from r = 17 out (within 0.2, the
reading's grain). The angular momentum about the proton's Node, exact
at the two ends where the vector is known, rises from `12 x 293 783
192 = 3.525 x 10^9` to `3 x 35 392 088 + 26 x 172 906 816 = 4.602 x
10^9`: 1.305 of the start. The bounds at the crossings (r times
`abs(p)`, met when the momentum is tangential there) rise with it and
are consistent with a monotone rise through the first three quarters
and nothing after. A central push conserves L exactly and E up to the
kicks' grain (section 2 (iv)); neither is conserved here. The second
crossing is the plainest line: at the SAME radius 13 as the first, the
momentum's length is 308 against 283 million, 8.8 percent more, half a
turn later.

**(c) The push implied.** The tangential impulse is `Delta L / r`: with
r about 15 over the first three quarters, `1.08 x 10^9 / 15 = 7.2 x
10^7` label units along the motion. The radial impulse the law
delivered over the same three quarters, by the declared push: `F = 16 x
1836 x 64 x 6.588 / 10 = 1.24 x 10^6` per interval, `2.48 x 10^7` per
Link at the dwell 20, over about 61 Links of path (three quarters of a
ring of radius 13): `1.51 x 10^9`. The ratio: the push the electron
received had a component along its motion of about 4.7 percent of its
radial component, over the first three quarters of a turn, and none
after (the loop's constant flat from r = 17 out). The push it received
did not fall short of the balance in size by any factor that fits; it
was not central. GAMEBOARD by formula from the `.out`.

## 2. The candidates, each tested by algebra against the numbers

**(i) The fan's L1 factor.** As built a reader's push takes one label
`u_D` per arrival, and a line of direction D enters the arrival flow `S_1
/ abs(D)` times per Euclidean Link, so the push's shell mean carries the
fan's mean of `S_1 / abs(D)`: 1.4355 on the 290 directions, 1.421 by the
shells, 3 / 2 in the limit (record 872; record 898); on the plane the
factor is `F_plane = 1.2871` over the 120 in-plane directions, `4 / pi`
in the limit (record 898, D3's periods). Which flow did the atom's
algebra take? THE LATTICE'S AS BUILT: `E_body(r)` is the count of the
engine's own flight lines entering the electron's three Nodes per
shell (6.588 at r = 12; PINS.md section 2, "series H's derivation, the
engine's own flight lines"), each arrival one label of size Q, which is
the code's push arrival for arrival; the continuum's `q / (4 pi)` enters
only the shell mean's `E_0 / r^2` form of ALGEBRA.md section 2 (a),
never a number of the balance. So the declared momentum is the code's
balance at r = 12 within the fan's grain, and the L1 factor is not a
difference between the algebra and the code on this world. Where it
would act, it acts on the push's SIZE (a factor f, section 1 (a): a
conic, home at the full turn) and along the line's direction, never
across it: it moves the far side, not the angular momentum. Direction:
a push counted `1 / F` smaller than the balance widens the loop to the
far side `r / (2 / F - 1)`, 21.7 Links at `F_plane` (section 3), at
half a turn. Against the reading (13 at half a turn, 26 at the full
turn, L up 30 percent): does NOT account.

**(ii) The drive's wall.** The pace `v = p / (Q S M + abs(p_a))` per
axis gives `k = 1 + Q S M / abs(p_a) = 19.05` counts per Link at the
start's crossing (RUN.md P1); the dwell read 20.0 over the twelve hops
inside r = 17: the electron moved 4.8 percent slower per Link than the
wall says. A slower body at the same momentum needs LESS centripetal
push (`p v / r`), so the push delivered exceeds the need by the same
4.8 percent: `f = 1.048`, and with the momentum's 1.0192 the loop is a
conic with `a = 12.7`, the far side 13.3 at half a turn, home at 12:
TIGHTER by the wall's excess, not wider, and no torque (the pace is a
function of the momentum alone on each axis, a Hamiltonian flow up to
the kicks' grain, which conserves L exactly). The 4.8 percent itself
has a source the algebra names: on `main`'s per-axis drive a coincident
fire on a later axis is lost (BEAM_LAW note 30 (ii); `engine.py`, the
per-axis branch: only the first axis that fires steps), at the rate of
the coincidences, `v_x v_y` per interval, up to 2.6 percent of one
axis's steps where the two paces are equal, and the twelve hops read
are about the +y, -x and -y crossings where one pace is near zero; the
reading of 4.8 percent is above this and is left as read. Does NOT
account for the widening; accounts for nothing of the torque.

**(iii) The proton's reads per crossing.** Read 1, 1, 1, 1 against 0.63
in the mean (RUN.md P5, PASS within 0 to 2). The proton is `fixed`: the
push it takes moves nothing (RUN.md section 2), and its table's default
rule for the electron's free rows is `read`: the push taken, the row
goes on (no `rerelease`, no `measure`), so a read at the proton changes
neither the electron's momentum nor its rows. More reads there are more
kicks on a body that cannot move. Does NOT account, and cannot.

**(iv) A rule not in the algebra, or a defect.** (i) to (iii) cannot
account for the reading, because each is a size or a pace and the
reading is a torque: a tangential impulse along the motion of about 5
percent of the radial over the first three quarters of a turn, then
none. What the algebra says a central push on the fan cannot do, and
why: every kick is one label `u_D` of a line through the electron's
Node, and every such line starts at the proton's Node, so a kick is
along the line from the proton to within the digital line's offset (at
most half a Link over r, 0.04 rad at r = 12); the residues' sum around
a ring vanishes by the fan's mirror symmetry (a circulation is odd
under a mirror the fan is even under), and over each quarter of an
exact ring by the diagonal mirror; on a loop that is not a ring the
residues sum at random, about `sqrt(N) x 0.04` of one kick over N kicks,
one percent of the radial over 963 kicks per turn. Not 5 percent, and
not one-signed. So the torque is a rule of the push or of the drive
that the algebra of ALGEBRA.md sections 1 to 3 does not carry. Three
named, with what each would show in the records the run already wrote
(a host reading of `events.jsonl` on the runner's host; no run):

1. *The push's rule.* The electron's 305 `read` lines carry the push it
   took per bunch (one bunch per release of the proton, every 10
   intervals, `E_body` arrivals each). Sum them per quarter turn and
   resolve each against the electron's position: the algebra above
   says the tangential sum over a quarter is within one percent of the
   radial sum. A systematic 5 percent along the motion, quarter after
   quarter, is the push's rule and names where in the push it enters
   (the reader's velocity count `1 - n . beta` of DERIVATIONS_BEAM 12b.1
   is zero at first order on a circle, `n` radial and `beta` tangential,
   and cannot give it; the count of a bunch depending on the Node the
   electron entered or left in the same interval could).
2. *The drive's rule.* If the read lines' pushes are radial within the
   grain and L still rises, the torque is kinematic: `dL / dt = v x p +
   r x F`, and `v x p` is not zero on `main`'s per-axis drive, where v
   is not along p (the lost coincident fires slow the later axis by
   `abs(v_x)` of its steps; the per-axis walls differ by `abs(p_a)`).
   The algebra's estimate: `(v x p)_z = v_y abs(v_x) p_x` from the lost
   fires, about `2.5 x 10^5` per interval at the register's numbers,
   its sign alternating by quarter (negative in the first and third,
   positive in the second and fourth, where the electron spends 412,
   439, 451 and 889 intervals), a net of about `10^8` over the run
   against the `1.08 x 10^9` read: the right kind, one order too small
   and of the wrong symmetry on a symmetric loop. The reading that
   decides: the electron's step lines, `axis_steps` per axis against
   the momentum's integral per axis, the count of lost fires per
   quarter. Form B (`drive_b`, record 652) lifts the lost fires and the
   one-axis domain: the same world under `drive_b` is the algebra's
   test of this candidate, a run the owner has already approved as the
   atoms series' form (PINS.md), not a new one ordered here.
3. *A defect.* Only if 1 and 2 read zero: then the torque is in the
   engine's arithmetic and the reading that shows it is the books' one
   line, the transit momentum line against the bodies' momenta and the
   detectors' at every tick (the books balanced at every tick, RUN.md
   section 4, which bounds it: a defect that conserves the books moves
   momentum between the electron and the rows or the faces, and the
   faces' `momentum` on the `p` family's clicks, 328 045 and 325 073 per
   pair of faces, symmetric, say the proton's rows carried none of it
   out). What would show it: an asymmetry between the +y and -y faces'
   booked momentum of the `p` family of the order of `10^9`, which the
   clicks' equal counts make unlikely; then a minimal reproduction on a
   two-Node GameBoard by the engine's owner.

Verdict on the cause: NOT ACCOUNTED by (i), (ii) or (iii); the reading
is a torque; candidate (iv) 1 or 2 by the two host readings of the
existing records, in that order; the per-axis drive's lost fires are
the one mechanism the algebra finds of the right kind, an order too
small by its estimate. The algebra can go no further without the
records' lines; it orders no run.

## 3. Under flow-link-v1 (the key `flow_link`, PR #854, record 898): what the corrected flow does at r = 12

Under the key one flow label `f_D` per arrival, the integer vector
nearest `Q D / S_1`, so a line enters the push once per Euclidean Link
and the L1 factor is gone line by line (record 898 (1) to (3)). The
electron's three Nodes lie in and beside the plane z = 26, and the lines
through them are in-plane to within one part in twelve: the push's
factor is the plane's, `F_plane = 1.2871` (120 directions; `4 / pi` in
the limit; record 898, D3's periods 343 / 687 to 384 / 768). With the
declared momentum unchanged and the push central, the same algebra
gives `f = 1 / 1.2871 = 0.777` (times the momentum's 0.963: `f = 0.748`):

    a = 16.8 (17.6),   e = 0.287 (0.337),   the far side 21.7 (23.5) Links at half a turn, home at 12 after one turn,   T = 2430 (2600) by Kepler's `T ~ a^(3/2)` on the comparison side:

the loop does NOT close at the declared momentum under the key: it is a
conic wider than the circle by the key's own factor, and the generator
would re-pin the circle's momentum by `1 / sqrt(F_plane)`: `p_c' = 288
249 497 / 1.1345 = 254 075 280` on `main`'s drive, `258 952 912` for
form B's 293 783 192 (GAMEBOARD by formula; the wall's nonlinearity
moves it by a part in a thousand, the generator re-solves it exactly),
with `h = 16 p(8)` re-fixed by the series' rule and the closure `j =
4.001` at r = 12 re-read. And the key does not touch the torque of
section 1: `f_D` is along D as `u_D` is (the same direction, another
size per line), so whatever gives the push its tangential part gives it
under the key too, and a loop that leaves the board at the declared
momentum leaves it under the key at the re-pinned momentum unless the
torque's source is (iv) 2, the drive's, which the key does not touch
either. So the key does not select a new baseline: the atom's first run
under `flow_link` would read the corrected size of the push (the far
side 21.7 against 26 at the declared momentum, or a circle at the
re-pinned one if the torque is absent) and the torque at the same
time, two unknowns in one reading, and is not the baseline the momentum
give is read against until the torque is named. What remains: the
torque's source, by the two host readings of section 2 (iv); after it,
the same world under `drive_b` (the atoms series' own form) and, if the
owner admits the key, under `flow_link` with the re-pinned momentum,
each read against the register's as the law stands.

## 4. The consequence for the pins of atom-give-momentum-v1 (record 926)

Section 3 selects no baseline beyond the register's: the pins of
[DESIGN_MOMENTUM.md](DESIGN_MOMENTUM.md) section 6 stand as declared
against the baseline as the law stands (`hydrogen_r12_give` against the
runner's clicks, `hydrogen_r8_give` against the register's `r8`), the
two worlds under `drive_b` conditional on form B's loop returning, and
the give's own prediction is untouched by the cause: the momentum give
changes a loop's action and never its Nodes (DESIGN_MOMENTUM.md section
5 (b) and (g)), so it neither adds to nor takes from the torque, and a
torque that widens the loop widens it with the key on as without. One
line is added to the pins by this file: whatever names the torque
(section 2 (iv)) is read on the give's worlds too, since the give's rows
leave with the electron's momentum per unit of content and their
clicks on the faces carry it (the `light` rows' `momentum`, DESIGN_MOMENTUM.md
section 6), a second reading of the electron's momentum at each return
beside the step lines, DETECTOR.

## Links

[RUN.md](../atom_baseline/RUN.md) and [baseline_readings.out](../atom_baseline/baseline_readings.out)
(`main` at 384b15c6); [ALGEBRA.md](../atom_algebra/ALGEBRA.md) sections
1 to 3; [PINS.md](../atoms/PINS.md) section 2; [the flow weight design](../flow_weight/DESIGN.md)
(flow-link-v1); [DESIGN_MOMENTUM.md](DESIGN_MOMENTUM.md) sections 5 (g)
and 6; [BEAM_LAW note 30](../../BEAM_LAW.md); [DERIVATIONS_BEAM 12b.1](../../DERIVATIONS_BEAM.md);
records 652, 817, 872, 898, 926 and 935 of [the log](../../LOG_2026-09-20.md).
