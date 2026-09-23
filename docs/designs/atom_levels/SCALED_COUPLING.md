# scaled-coupling-v1: a declared scale of the electron's coupling to the proton, off by default, for the side track of the levels (the owner's word of 2026-09-22, record 997)

The Atom Levels Mathematician, 2026-09-22, docs only: no build, no run, no
PR. The paper takes the atom's levels by the algebraic formula alone
([LEVELS.md](LEVELS.md) sections 1 and 3); the runs of the three level
worlds are the side track's record ([RUN.md](RUN.md)). This note declares
the one knob the owner named for that side track, what it changes and what
it leaves, the pins before any run and the estimate. Every number below is
a COMPUTATION from the atoms generator's own arithmetic
(`examples/events/atoms/make_worlds.py`: series H's fan, flux count and
orbit; the map [scaled_coupling_map.py](scaled_coupling_map.py) and its
output [scaled_coupling_map.out](scaled_coupling_map.out) beside this
note); nothing was run. Bohr's and Balmer's forms stand on the comparison
side only.

In six lines:

1. **The knob.** One world key `coupling: [n_k, d_k]` (two integers, `n_k`
   and `d_k` from 1, one rational scale k = n_k / d_k), absent by default;
   present, it declares the identity `scaled-coupling-v1` in the record's
   `hypotheses`. Every registered world stays byte-identical.
2. **What it changes: the push's constant.** At the frame, the charge of a
   moving body in every column, read for the push as the pair (E_c, D_c),
   becomes (E_c x n_k, D_c x d_k): the electric and the gravity column
   alike, so the pull of the proton's rays on the electron, kappa = 16 M_e
   per unit of label flow today, becomes 16 M_e x k. Not the flux (the fan
   is the proton's declaration, shared by the count and the Planck
   identity) and not the action h (the closure's wall, which sets every
   level's scale).
3. **What the ladder does under it.** At the same h the rungs move: a_j
   proportional to j^2 / k, p_j to k / j, T_j to j^3 / k^2, E_j to k^2 /
   j^2. The ratio of two lines is k-free (LEVELS.md section 3): the knob is
   a control of the ladder's form, never a fit of it.
4. **What it does NOT change.** The fan's grain is the count's geometry per
   radius, not the push's: the flux the three Nodes receive departs from
   the inverse square by -17 percent at r = 3, -18 at r = 5, -10 at r = 6,
   +21 at r = 16, -16 at r = 24 and r = 27, +38 at r = 40, and stands
   within 5 percent at r = 4, 7, 12, 14, 19 and 48 (section 3). The pulse
   at r = 3 (one shell per 10 intervals, 21 shells and 17 degrees per shell
   per loop) is r's and the speed's; a stronger push there makes it
   coarser (23 degrees per shell at k = 2).
5. **Which r the knob makes usable.** k = 1/2 brings rung 2 from r = 3 (the
   loop that escaped) to r = 6 and rung 3 to r = 14, both within 10 percent
   of the inverse square, on boards of 41^3 and 57^3; rung 4 lands at r =
   24 where the fan is 16 percent short (its closure 3.585 for 4), so
   Balmer's triple (2, 3, 4) is not reachable within the grain at any of
   the five scales mapped. The best triple needs no knob: rungs 3, 4, 5 at
   r = 7, 12, 19 (closures 3.017, 4.001, 4.981), the r = 19 world on 67^3,
   about 5 minutes alone; its ratio is Paschen's, 2304 / 1575 = 1.463 in
   the limit, on the comparison side.
6. **The pins and the estimate.** The k = 1/2 pair of worlds at r = 6 and r
   = 14 (section 5): the loop stays five turns, the level on the body's
   own record within 10 percent of 39.4 and 19.8 steps at [512, 1], the
   same rung at two scales in the ratio k^2 (rung 3: 19.8 at k = 1/2
   against the r = 7 run's 71.7 at k = 1, the ratio 3.62 for 4; the k-free
   control), the Planck identity on two faces; about 4 minutes alone,
   boards to 57^3; the r = 24 world (77^3, 17 minutes) only on the owner's
   word (record 997: no large lattices).

Notation as in LEVELS.md: N = 64 phase steps per circle, Q = 64 the
lattice's period constant, M_e = 1836 the electron's content, h the
action (5 536 242 544 = 16 p_B(8)), kappa the push's constant (the
momentum a moving body gains per unit of label flow of the proton's rays,
a scalar), k = n_k / d_k the declared scale (a rational), j the whole
closure (a rung), a_j the rung's radius in Links, p_j its momentum (a
scalar, the magnitude of the momentum vector **p**), T_j its period in
intervals, E_j its level, r the world's radius, T the loop's period as the
generator gives it, L the level in phase steps at the pair [n_l, d_l] =
[512, 1] (LEVELS.md section 2 (b)). Bold lowercase is a vector, plain a
scalar.

## 1. The knob and where it enters

**(a) The declaration.** One world key, off by default:

    "coupling": [n_k, d_k]

`n_k` and `d_k` are integers from 1 through the declared bound of a charge
(`MAX_VALUE` in `world.py`); the pair is reduced at load. `[1, 1]` under
the key is refused (a declared scale that scales nothing is a mistake, and
the registered worlds carry no key). A denominator of 0, a negative part
or a part that is not an integer is refused naming the key. With the key
present the world's `hypotheses` carry `scaled-coupling-v1` after
`atom-level-v1`; the run's record names it as it names every identity
(docs/ENGINE.md, the record).

**(b) Where it enters: the reader's side of the push, at the frame.** The
push a moving body takes from one group of arriving rays is one signed
inner product over the columns (`nature_beam.push_form`): per column c and
axis,

    X = V x E_c x n_c x (Lambda_c / D_c) x (Lambda_c / d_c)

counted by the drive against the wall Lambda_c^2, the remainder kept on
the body's own record. (E_c, D_c) is the reader's charge in the column as
the frame read it once per interval (`Measured.charges(for_push=True)`
into `frame_charges`); (n_c, d_c) the arriving family's value per unit of
content; Lambda_c the column's common denominator. Under the key the frame
forms, for every body that is not fixed and in every column alike,

    (E_c, D_c) -> (E_c x n_k, D_c x d_k)

after the gravity column's replacement under `drive_b` (the body's weight
(w, Q S), `world.body_weight`), so that the weight scales as the charge
does. The column's common denominator carries d_k (Lambda_c -> Lambda_c
x d_k at load, `world.column_scales`); the count the drive makes per
interval is then the same integer as today's times k, up to the one unit
per column, axis and interval the drive's remainder already grants
(light_speed/FORM.md section 2). Refused at load when Lambda_c x d_k or
E_c x n_k for any held content within the declared bounds would exceed
the drive's bound (the same refusal the columns make today, naming the
key).

**(c) Why the push's constant, and not the flux or the action.**

- The flux is the proton's declaration: its fan (1016 directions on the
  count), its shell of 10 intervals and its label flow. The level counts
  the same rays' phase (the faces' count, the Planck identity of LEVELS.md
  section 2 (d)); a scaled flux would move the count and the identity
  with it, and the grain is the fan's geometry, which no scale of its
  amount removes.
- The action h is the closure's wall: every level is E_j = -j h / (2
  T_j), and the rise released at a return is a Euclidean division by 2 h
  d_l (LEVELS.md section 2 (b)). A re-fixed h moves the scale of every
  level and every line with it; the paper's h is series H's, 16 p_B(8),
  and stays.
- The push's constant is what the electron alone reads: its own charges at
  the frame against the arriving labels. One pair on the reader's side
  scales kappa, leaves the proton, the fan, the count, h and the pair
  untouched, and leaves the ratio of two lines as it was.

**(d) The same arithmetic without the key, and why the key.** The
electron's `charge` is already a pair in the world file ([-15, 1]);
declaring [-15, 2] scales the electric column alone. That is a different
physics: it moves the ratio of the electric to the gravity column (15 : 1
to 15 : 2), it moves the charge line of the books (a DETECTOR line of
every run, docs/ENGINE.md), and it names no identity. The key scales both
columns alike, keeps the family's charge as declared and stands in the
record under its own name.

## 2. The three tests

- **Generic.** One primitive: a pair (n_k, d_k) on the reader's charges in
  every column, for every body that is not fixed, whatever its family;
  no family name, no kind, no branch on a name. A world of one moving body
  and a world of ten read the same rule.
- **Vector.** The push is verb 2 (the bilinear form over the columns) and
  verb 6 (the drive's Euclidean division against Lambda_c^2 with the
  remainder kept); the key multiplies two declared integers of the form's
  coefficients at the frame. No root, no float, no new verb.
- **Local.** The frame reads what the body holds (its own record) and the
  rays arriving from its six neighbours; the scaled pair is formed from
  the body's own charges and two declared integers. Nothing new is kept at
  a Node: the accumulator and the remainder are the body's own already
  (BEAM_LAW note 41). Fixed local work for fixed K: one multiplication per
  column per frame, on the host.

Under the key absent the frame forms the same integers as today, byte for
byte: every registered world stays byte-identical (the gate set
`examples/events/gate_set.json`), the test the identity must pass before
any world is registered under it.

## 3. What the knob does NOT change: the fan's grain and the pulse

The flux the electron's three Nodes receive per shell against the inverse
square anchored at r = 12 (the map's table; the fan of 1016 directions,
the count exact per Node): a COMPUTATION of the geometry, the same under
every k.

| r | flux per shell | inverse square | departure |
| --- | --- | --- | --- |
| 3 | 87.5 | 105.4 | -17 percent |
| 4 | 56.3 | 59.3 | -5 percent |
| 5 | 31.1 | 37.9 | -18 percent |
| 6 | 23.6 | 26.4 | -10 percent |
| 7 | 18.4 | 19.4 | -5 percent |
| 8 | 13.5 | 14.8 | -9 percent |
| 10 | 8.4 | 9.5 | -11 percent |
| 12 | 6.59 | 6.59 | 0 |
| 14 | 5.09 | 4.84 | +5 percent |
| 16 | 4.50 | 3.71 | +21 percent |
| 19 | 2.62 | 2.63 | 0 |
| 24 | 1.39 | 1.65 | -16 percent |
| 27 | 1.10 | 1.30 | -16 percent |
| 32 | 0.81 | 0.93 | -13 percent |
| 40 | 0.82 | 0.59 | +38 percent |
| 48 | 0.40 | 0.41 | -4 percent |

The grain is not a small-r effect alone: it is the lattice ring's count
of a fan of whole directions, and it comes and goes with r (within 5
percent at r = 4, 7, 12, 14, 19, 48; 16 percent short at 24 and 27; 38
percent over at 40). What the knob does is move the rungs among these
radii (a_j proportional to 1 / k); it leaves the table. After the
coupling is scaled the grain leaves, at each radius, the closure the
world reads instead of the whole j: at k = 1/2 the rung-4 world at r = 24
reads 3.585, the rung-2 world at r = 6 reads 1.889, the rung-3 world at r
= 14 reads 3.087 (section 5).

The pulse at r = 3: the proton emits one shell per 10 intervals, the loop
of 212 intervals sees 21 shells, 17 degrees of the loop per shell (RUN.md,
the r = 3 finding: the electron leaves the board at tick 733). The pulse's
grain is T / SHELL; at a fixed r a stronger push shortens T (k = 2: T =
155, 23 degrees per shell; k = 4: T = 115, 31 degrees) and a weaker one
lengthens it (k = 1/2: about 300, 12 degrees), but r = 3 is then no rung
(rung 2 sits at a_2 = 6 under k = 1/2). No scale of the five makes r = 3 a
rung with a fine pulse: the pulse is r's, the rung's radius is k's, and
r = 3 as a rung needs k = 1 (rung 2) or k = 4 (rung 4, 12 shells per loop,
31 degrees per shell, coarser than today's).

## 4. What the ladder does under the knob (COMPUTATION, the limit's form)

From the closure's congruence at the same h (LEVELS.md section 1): with
kappa -> kappa x k,

    a_j = a_j(1) / k,    p_j = p_j(1) x k,    T_j = T_j(1) / k^2,    E_j = E_j(1) x k^2

and the level in steps at [512, 1], L_j = 512 x 64 x j / (2 T_j),
scales by k^2 (the map: rung 2 reads 146.1 steps at k = 1 and 39.4 at k =
1/2, the ratio 3.71 for 4 with the read closures 1.892 and 1.889 and the
two worlds' own T). The ratio of two lines, nu(j to i) / nu(j' to i), is
k-free, as it is free of E_1, m_i, h, N and the pair (LEVELS.md section
3): the knob cannot bring a ratio nearer Balmer's or farther from it. Its
use is the control: two worlds that differ by the key alone must read
levels in the ratio k^2 within their bands, or the rule is not the
ladder's.

## 5. Which r the knob makes usable, by scale (COMPUTATION)

The map's rows, rung by rung: the rung's radius a_j at the same h, the
world at the nearest whole r, its side (2 (r + 14) + 1), the flux's
departure, the closure the world reads, the period T, the pulse's grain,
the level L at [512, 1] and the ticks of five turns.

| k | rung | a_j | r (side) | flux off | closure | T | degrees per shell | L | five turns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 4 | 3.00 | 3 (35) | -17 | 4.108 | 115 | 31.2 | 584.2 | 3000 |
| 4 | 5 | 4.69 | 5 (39) | -18 | 5.079 | 240 | 15.0 | 346.6 | 3000 |
| 4 | 6 | 6.75 | 7 (43) | -5 | 6.393 | 365 | 9.9 | 286.7 | 3000 |
| 2 | 3 | 3.38 | 3 (35) | -17 | 2.769 | 155 | 23.2 | 292.1 | 3000 |
| 2 | 4 | 6.00 | 6 (41) | -10 | 3.943 | 410 | 8.8 | 157.6 | 3000 |
| 2 | 5 | 9.38 | 9 (47) | -13 | 4.692 | 750 | 4.8 | 102.5 | 3800 |
| 2 | 6 | 13.50 | 14 (57) | +5 | 6.366 | 1315 | 2.7 | 79.3 | 6600 |
| 1 | 2 | 3.00 | 3 (35) | -17 | 1.892 | 212 | 17.0 | 146.1 | 3000 |
| 1 | 3 | 6.75 | 7 (43) | -5 | 3.017 | 690 | 5.2 | 71.7 | 3500 |
| 1 | 4 | 12.00 | 12 (53) | 0 | 4.001 | 1490 | 2.4 | 44.0 | 7500 |
| 1 | 5 | 18.75 | 19 (67) | 0 | 4.981 | 2945 | 1.2 | 27.7 | 14800 |
| 1 | 6 | 27.00 | 27 (83) | -15 | 5.421 | 5375 | 0.7 | 16.5 | 26900 |
| 1/2 | 2 | 6.00 | 6 (41) | -10 | 1.889 | 785 | 4.6 | 39.4 | 4000 |
| 1/2 | 3 | 13.50 | 14 (57) | +5 | 3.087 | 2551 | 1.4 | 19.8 | 12800 |
| 1/2 | 4 | 24.00 | 24 (77) | -16 | 3.585 | 6334 | 0.6 | 9.3 | 31700 |
| 1/2 | 5 | 37.50 | 38 (105) | +37 | 5.761 | 9886 | 0.4 | 9.5 | 49500 |
| 1/4 | 2 | 12.00 | 12 (53) | 0 | 1.956 | 2914 | 1.2 | 11.0 | 14600 |
| 1/4 | 3 | 27.00 | 27 (83) | -15 | 2.673 | 10602 | 0.3 | 4.1 | 53100 |
| 1/4 | 4 | 48.00 | 48 (125) | -4 | 3.785 | 23531 | 0.2 | 2.6 | 117700 |

Read plainly:

- **Strengthening (k = 2, 4) moves the rungs inward** onto the coarse
  radii (3, 5) and shortens every period: the pulse's grain grows. It
  buys nothing.
- **Weakening by 1/2 makes r = 6 and r = 14 usable**: rung 2 at r = 6
  (the flux 10 percent short, 79 shells per loop, 4.6 degrees per shell,
  the closure 1.889) in place of the r = 3 loop that escaped, and rung 3
  at r = 14 (5 percent over, the closure 3.087). Rung 4 falls at r = 24,
  where the fan is 16 percent short and the world reads 3.585 for 4, on
  77^3 for 31 700 ticks: Balmer's triple (2, 3, 4) is not reachable within
  the grain at k = 1/2, and not at k = 1/4 either (rung 3 at r = 27, 15
  percent short; rung 4 on 125^3, 264 minutes, the large lattice the
  owner forbade).
- **The best triple needs no knob**: rungs 3, 4, 5 at r = 7, 12, 19
  (within 5 percent of the inverse square; the closures 3.017, 4.001,
  4.981, within 2 percent of whole). Two of the three worlds exist and ran
  (RUN.md); the third is r = 19 on 67^3, 14 800 ticks, about 5 minutes
  alone. Its ratio on the comparison side is Paschen's, nu(5 to 3) / nu(4
  to 3) = (1/9 - 1/25) / (1/9 - 1/16) = 2304 / 1575 = 1.463 in the limit;
  from the generator's levels 71.7, 44.0, 27.7 the computation reads
  (71.7 - 27.7) / (71.7 - 44.0) = 1.588, the departure the read closures
  and each world's own T carry (LEVELS.md section 5, the same band).
- **The knob's own use is the k-free control** (section 4): the same
  rung at two scales reads levels in the ratio k^2. Rung 3 at r = 14
  under k = 1/2 (19.8 steps) against the r = 7 run under k = 1 (71.7 by
  the generator; 70 read, RUN.md): the ratio 3.62 for 4, with the read
  closures 3.087 and 3.017. Rung 2 at r = 6 under k = 1/2 (39.4) against
  r = 12 under k = 1/4 (11.0): 3.58 for 4, with the closures 1.889 and
  1.956. Both on boards of 57^3 or less.

## 6. The pins before any run (GAMEBOARD by formula; a reading is compared with these only)

For the k = 1/2 worlds at r = 6 and r = 14 (`coupling: [1, 2]`, the level
declaration of the r = 12 world, the family `light`, the pair [512, 1],
the return at the +x crossing), each on its own side and ticks as
section 5 gives them; the bands are LEVELS.md's (10 percent per level,
the lattice's own):

- **P1 (stays).** The loop returns five times and the electron stays on
  the board: at r = 6, 785 intervals per return within 10 percent; at r
  = 14, 2551. R1's form (RUN.md). An escape is a finding, as r = 3's was.
- **P2 (the level, GAMEBOARD).** The body's own record at the first
  return: 39.4 steps at r = 6, 19.8 at r = 14, within 10 percent. R3's
  form.
- **P3 (the level, DETECTOR).** The same from the faces' two counts
  (`level_readings.py`, the loop between +x returns), within one step of
  P2. R2's form.
- **P4 (the k-free control, COMPUTATION of two readings).** L(r = 7, k =
  1) / L(r = 14, k = 1/2) = 3.62 within the two bands combined (about 20
  percent), against 4 of the limit, the r = 7 reading the registered
  run's (RUN.md, level 70); and, if the r = 12 world at k = 1/4 runs (53^3,
  14 600 ticks), L(r = 6, k = 1/2) / L(r = 12, k = 1/4) = 3.58 for 4.
  Passing does not make the ladder nature's; failing outside the band
  refutes the k^2 form of section 4.
- **P5 (the Planck identity).** A released row's `turn` equals its
  content in steps on two faces, as R5 read it at r = 12.
- **P6 (the control).** The same worlds without the key are the k = 1
  worlds at r = 6 and r = 14 (no rung there): their records differ from
  the keyed ones from the first frame, and the keyed r = 12 world differs
  from the registered `hydrogen_r12_level.json` from the first frame,
  while every registered world stays byte-identical.

No pin claims a match with nature: NATURE row 6 stays NOT YET on the side
track; the paper's claim is the algebra's (record 997).

## 7. The estimate (host, scaled from the r = 12 run: 77 s alone for 7500 ticks on 53^3)

| world | side | ticks | alone |
| --- | --- | --- | --- |
| r = 6, k = 1/2 | 41 | 4000 | about 20 s |
| r = 14, k = 1/2 | 57 | 12800 | about 3 min |
| r = 12, k = 1/4 | 53 | 14600 | about 2.5 min |
| r = 19, k = 1 (no knob; the Paschen triple's third) | 67 | 14800 | about 5 min |
| r = 24, k = 1/2 (rung 4; only on the owner's word) | 77 | 31700 | about 17 min |

The build, if the owner orders it: the key in `WORLD_KEYS` and the parser
(`world.py`, beside `atom_level`), the identity in `hypotheses`, the
scaled pair at the frame (`engine.py`, where `frame_charges` is formed)
and the column scales at load; a test of the identity (the key absent:
byte identity of the gate set; the key present: the frame's charges
scaled, the refusals, the k^2 of two worlds' levels by the generator);
the generator's worlds under the key; the index rows. About two hours of
build and the runs of section 7 after it. None of it is authorized by
this note.
