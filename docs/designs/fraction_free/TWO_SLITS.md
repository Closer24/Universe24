# The two slits under the record click: the generic form of the click, the exact phase, the birth wheel, and the pinned prediction (read-only, the mathematician, 2026-09-20)

On the owner's word of the evening ("shouldn't a mathematician check and
give us a generic solution for this? With us there is a transition from
ray to wave, as if, at the click") and the Boss's four questions, on the
paper session's statement (the record's state in `Z[Z_N]`, the two breaks
of resolution, both the shape of the fraction-free accumulator). Every
integer here is from `two_slits_map.py` beside this file (`two_slits_map.out`,
2 s, the engine's own tables C and S and its `by_clock` imported, nothing
else of the engine). The map first RECONSTRUCTS the registered `slits_low`
world row by row (the lamp's five rows, the two fans of 91, the walk by
the flight table, the pair form of `phase_per_link`, the offers per set,
the ladder of N = 64) and reproduces the register's 64 clicks exactly
(wall 34 as 11, 12, 11; screen 15 at y = 11, 29, 36, 43, 50, 56, 59, 60,
70, 77, 82, 90, 107 and two at 61; faces 15 as 8, 7; the total 1.1364 of
the birth norm and the shares 0.528 / 0.244 / 0.228: `two_slits_map.out`
section 4, `reproduced: True`), so every number below is the click's. No
run; nothing built; nothing registered.

## 1. Is the click as the evaluation of `Z[Z_N]` at zeta_N the generic form?

Yes, and it is the form the layer already has; the generic statement is
this. A record's state at its completion is one element of the group ring
`Z[Z_N]` per (end Node, label): the coefficient of `[p]` is the amount of
the record's rows that ended there at phase p (the rows are the terms; the
GameBoard carries them apart, one term per row, and adds them exactly only
where two rows of one record meet at one Node in flight, which is the
merge's normal form, the group-ring addition restricted to the lattice,
with `[p + N/2] = -[p]` its cancel). The click is the composition of two
maps: the ring homomorphism `ev: Z[Z_N] -> Z[zeta_N]`, `[p] -> zeta_N^p`
(the tables C, S are zeta_N at the scale 256, so `ev` is taken in
`Z[i]` at that scale with one rounding per term), and the norm
`z -> |z|^2` into the real cyclotomic ring; the ladder is the sampling of
the norms by the birth wheel. "Ray to wave" is exactly `ev`: a term of the
group ring is a ray (a count at a phase), its image is a pointer, and a
sum of pointers is a wave; nothing before `ev` is a wave and nothing after
it is a ray. That is generic: the same two maps for every record, every
set, every apparatus, with no parameter but N.

Can the GameBoard carry what the click needs without the apparatus's
layer, within "a Node keeps nothing"? No, and the map shows why with one
number: on the screen's pixels the two paths of one record arrive at ages
that differ by up to 18 intervals (the path difference of a fringe is up
to 2.2 wavelengths of 8 intervals), so no Node ever holds both rows at
once; a coherent sum across arrival times is a memory by definition, and
the only owner of that memory that keeps the Node empty is the record
itself. The layer IS the record's ledger of its ended rows, one group-ring
element per (end Node, label), read once at the completion: the minimum
memory and the right owner. The one sum the GameBoard does hold without
memory is the sum over rows PRESENT at one Node in one interval, which is
the `wave` reading (the crowd's pointer per interval: rows of different
records born at different ticks); with a lamp that births every record at
the same phase it reads the classical field's interference (the register's
0.80 / 0.12 / 0.35 at 16 / 8 / 4), which is a property of the lamp's phase
lock, not of the record: DESIGN section 0 rejected it as the click and the
rejection stands. So the answer to question 1 is: `Z[Z_N]` on the record,
`ev` and the norm at the click, the ladder on the wheel; the layer stays
and is generic.

On the torus form of record 150 (every count one point translated by its
rate, every crossing of a wall an event): the group-ring element is a
point of `Z^N`, not of a torus; but every ROW of it in flight is a point on
one circle, `Z_{N d}` for the pair form `[n, d]` (the phase accumulator:
the whole part is the index in `Z_N`, the residue below d the position
within the step), translated by n at every interval of age, and the click
reads its whole part. So yes: the phase of a row in flight is one more
component of the counts' torus, a row of the counts table with the rate
`[n, d]` and the cap none, the residue carried on the row, and the click
is the event at which that component is read. Section 2 says what the
exact reading of that component is.

## 2. Does the accumulator give an exact phase at the click, and what does it do to the pins?

Two roundings, and only one of them is a floor of the phase. (i) The phase
per interval of age: `by_clock(age, n, d)` at the world's rate
8591334592 / 2^30 = 8.0000000596 steps per interval is exactly 8 at every
age below 2^24 (`two_slits_map.out`, the first lines: the values over 300
intervals are {8}); the accumulator on the row gives the same whole part
with the residue kept: bit-identical here, exact in general, and nothing
of the two-slit failure is in it. (ii) The arrival: a row moves by the
flight table at whole intervals, `m(tau) = (2 tau S_1 Q + T_d) // (2 T_d)`
Links by age tau, so the phase read at the click is the phase at a whole
age, while the exact time of the row's last Link is `made x T_d / (S_1 Q)`
intervals, a rational. On the screen of `slits_low` the exact phase
exceeds the built one by 0.45 to 9.19 steps of 64 per row (mean 4.76; one
interval is 8 steps, 45 degrees), and between the two paths of a pixel by
up to 6 steps (34 degrees): the "sum of floors along the path" is this
one floor per row, taken at the arrival, not a floor per interval.

**The exact form**, one rational and one floor at the click: the fraction-free
row carries the phase accumulator `(n, d)` and the step accumulator of the
drive (`by_drive` with `S_1 Q` over `T_d`, whose residue at the arrival is
the overshoot of the whole interval over the exact step); the phase of the
row at its last Link is

    phi = (n / d) x (made x T_d) / (S_1 Q)      (mod N)

a fraction with the denominator `d S_1 Q` (2^30 x 12 x 64 = 2^40 on the
fan of `slits_low`, 2^43 on the screen's fan of section 4) and the
numerator `n x made x T_d` (below 2^53 on every path of either world),
within the ceiling; the click takes ONE floor, `floor(phi x N' / N)` on
the table of N' steps it evaluates on (N' = N = 64 today; a finer table
is one declaration), and adds u exactly. No new field: the two
accumulators are the fraction-free record's own; the click reads them
once. Its limit is the flight table's: `T_d = isqrt(3 |D|^2 Q^2)` is
rounded once per direction, within 1 / T_d of the isotropic pace (within
0.00018 of 1 on the screen's fan, section 6), and the exact phase exposes
that rounding where the built one hid it under the whole interval: on
record 144's cone (17 Links on the axis, 24 on the staircase of (1, 1, 0),
both arriving at age 29 and reading 40 today) the exact phases are 41.75
and 42.00, one step apart on the table of 64, the anisotropy of isqrt
(156 against 110 sqrt 2 = 155.56) made visible at one step in 234.

**What it does to the pins.** The Mach-Zehnder worlds with equal arms on
headings and the Bell and GHZ worlds do not move (equal paths have equal
overshoots, and the label click reads u and the label, not the path
phase). `slits_low` re-registers: under the exact phase and the ladder as
built the 64 clicks become wall 34, screen 16 on 15 pixels, faces 14
(section 5). `mz_unequal_f8` and `f16` (arm 2 two intervals longer) and
the cone test of record 144 are to be re-read, since their two paths'
overshoots differ; the map does not pin them (its geometry is the two
slits). And on the two-slit weights the exact phase changes LITTLE: the
Pearson of the screen's weights with the Euclidean two-source cosine goes
from 0.390 to 0.407 over the 75 pixels with rows and from 0.645 to 0.669
over the 27 two-path pixels (section 3; the register's 0.368 is the
reading tool's own cosine, this map's is 0.390 at the heading pace 64/110
and 0.389 at the isotropic pace). The arrival's rounding is real and the
exact form removes it, but it is not what hides the fringes; section 4
says what does.

## 3. Is u as the lamp clock's exact fraction lawful, and does it remove the empty cells?

Three findings. (i) The exact fraction of the lamp's clock is not the
form: `slits_low`'s lamp runs at the rate [1, 1] and its turn is
`by_clock(age, K, K)` = 1, so both accumulators are 0 at every birth; an
exact-fraction u is identically 0 and every record would click in the
first cell. The proposal degenerates on the very world it is meant for,
and on every lamp whose rate is whole. (ii) The built u is already a
lawful clock: u = (births - 1) mod N is the accumulator of a count of rate
1 / N per birth on the lamp's own record, written on the row at birth and
read once at the click; it satisfies "no register at the detector" (#359
step B) as it stands. (iii) The empty cells are not a shortage of births
but a PERIOD: the ladder's rung is 1 / 2N = 0.0078 of the total and only
3 of the 75 screen cells of `slits_low` are above it (the largest, y = 60,
is 0.0264); the 15 screen landings are the cumulative rounding's, not the
cells' own; and since every record of the world has the same offers and
u repeats with the period 64, the 19 distinct cells landed by the first
64 births (3 wall, 14 screen, 2 faces) are the cells of every birth after
them: 230 births read the same 19 cells, and so would 2^30. No count of
births removes an empty cell under u = ordinal mod 64.

**The generic form: the birth wheel W with the bit-reversed ordinal.** Let
W = 2^k be a constant of the click beside N (the map uses W = 4096, the
grain of doppler-v1), and let the lamp write on the record

    u_W = bitreverse_k(ordinal mod W),     the click's rungs  b_j = (2 W C_j + T) // (2 T),  the cell the first j with u_W < b_j

(the van der Corput sequence in base 2: the ordinal's k bits read
backwards). It is a count on the lamp (12 bits of the ordinal, a fixed
permutation of them), no draw, no register at the detector, one field on
the record as today; its first 64 births are exactly the 64 positions of
today's wheel in another order (the multiples of 64 on W = 4096), and
every further block of 2^j births halves the grain, so that after W births
every cell of weight above 1 / 2W has clicked and every count is within
one of W times its weight, in EVERY prefix of the run. The same wheel at
the ordinal itself (u = ordinal mod W without the reversal) is not it: it
sweeps the ladder in cell order, the first 2048 births of `slits_low` all
at the wall. N stays the phase circle (the tables, the merge's cancel);
W is the click's own grain, as G is the doppler weight's.

What it does: under the bit-reversed wheel the screen of `slits_low`
receives 62 clicks on 43 pixels by 256 births and 1001 on 75 pixels by
4096 (section 5: every single-path pixel 7 or 8, the two-path pixels 4 to
108 under the built phase, 0 to 115 under the exact one); the empty cells
are gone. But what appears is not Young's pattern: the Pearson of the
two-path pixels' counts with the Euclidean cosine is 0.645 (built) and
0.668 (exact), the same as the weights', because 48 of the 75 pixels
receive one path only (a flat 1 / 455 each), because the pixel a fan
direction lands on is the digital line's, so that rows of ONE opening on
neighbouring directions meet at one pixel and interfere with each other
(y = 59, 60, 61 take 68, 115, 68 of the 1001), and because the 91
directions are the fan's comb and not the screen's. That is "the
geometry's own 0.381": the fan of the opening, not the law.

## 4. The prediction, pinned before any run

Under 2 and 3 on `slits_low` AS REGISTERED (the fan of 91), 4096 births:
wall 2168, screen 1001 on 74 pixels, faces 927; the 27 two-path pixels
(y = 22, 29, 30, 36, 39, 43, 46, 48, 49, 50, 51, 55, 59, 60, 61, 65, 69,
70, 71, 72, 74, 77, 81, 84, 90, 91, 98) read 7, 16, 19, 32, 31, 21, 5, 1,
1, 28, 15, 8, 68, 115, 68, 8, 15, 29, 0, 1, 5, 22, 31, 32, 19, 16, 7 and
every single-path pixel 7 or 8: a comb with the visibility 1.000 across
the two-path pixels and the Pearson 0.668 with the Euclidean two-source
cosine. **No fringes of the slits on this world under any form of the
click**, because its fan is not the screen's.

Under 2 and 3 with **the screen's fan** (the openings' `directions` the
121 vectors (44, y - opening), one per pixel of the screen, components
within the direction bound 64, the multiplicity 5 x 121 = 605 equal on
both paths of every pixel, the same law and the same click; 174 of the
242 directions land on their own pixel and the others one Node short,
115 pixels receive two rows, 2 none), 4096 births: **Young's fringes**,
the Pearson of the counts with the Euclidean cosine 0.963, the bright
pixels (y = 35 to 38, 59 to 61, 82 to 85, the spacing 20.5 pixels =
wavelength 4.654 Links x 44 / 10) at 28 to 29 clicks and the dark ones
(y = 13 to 20, 48 to 50, 70 to 72, 100 to 107) at 0 to 3: the visibility
(bright mean 28.7, dark mean 0.55) 0.96, the profile the cosine's
(section 6, the rows `exact` and `cos`, the counts y = 40 .. 80). Under 3
alone (the built phase, the wheel) the same world gives the Pearson 0.904,
the bright 24 to 29 and the dark 0 to 4, the visibility 0.93, and the
profile a STAIRCASE of 45 degrees (the weights take the five values 0,
0.6, 2.0, 3.4, 4.0 x 1 / 605: the cosine sampled at the arrival's whole
interval); under neither (the click as built) the screen's fan gives 23
clicks on 23 pixels by 64 births, the Pearson 0.36, and the same 23 cells
forever. So the order of what hides the fringes is: the wheel (3) first,
the fan second, the phase (2) last, and the exact phase is what turns the
staircase into the cosine. Refutation: a run of the screen's fan under
the wheel and the exact phase whose bright pixels are not 28 to 29 or
whose dark pixels exceed 3 of 4096 births, or a Pearson below 0.95.

## 5. The four answers in one line each, and what is the owner's

1. The click is `ev: Z[Z_N] -> Z[zeta_N]` and the norm, the ladder on the
   wheel, on the record's group-ring element per (end Node, label): generic,
   and the layer is that element's ledger, the memory no Node may keep; the
   phase in flight is a component of the counts' torus, read at the click.
2. The exact phase is `(n / d) x made x T_d / (S_1 Q)` from the row's two
   accumulators, one floor at the click, within 2^53; it moves `slits_low`
   (34 / 16 / 14) and the unequal-arm and cone pins, not MZ-equal, Bell or
   GHZ, and it lifts the two-slit cosine's Pearson by 0.02 only.
3. The exact fraction of the lamp's clock is 0 at rate [1, 1] and not the
   form; today's u is a lawful clock whose period 64 repeats 19 cells
   forever; the generic form is the bit-reversed ordinal on a wheel W = 2^k,
   which fills every cell above 1 / 2W in every prefix, a count on the lamp.
4. `slits_low` as registered shows no fringes under any click (its fan is a
   comb); with the screen's fan, the wheel and the exact phase: fringes at
   the Euclidean spacing, bright 28 to 29, dark 0 to 3 of 4096, Pearson
   0.963, visibility 0.96; with the wheel alone a staircase at 0.904.

For the owner: W as a constant of the click (2^12) with the bit reversal;
the exact phase at the click as the reading of the fraction-free row's two
accumulators; the screen's fan as the two-slit world's declaration (a
world, not a law); the pins that move, once, in one batch with the
fraction-free re-registration. Nothing here is built or registered.

## 7. The fan by angle: the integer form, and the run of `slits_huygens` on main

**The rule (Huygens on the lattice).** A re-emitter's fan is the full
primitive fan within a width P of the law, every (a, b, c) with a >= 1
and |a| + |b| + |c| <= P coprime (in the plane, a + |b| <= P), and each
direction carries as its split weight THE ANGLE IT COVERS: half the gap
to each of its two neighbours in the fan's angular order. In the plane
consecutive directions of that order are Farey neighbours, `|a b' - a' b|
= 1` (checked on all 1422 consecutive pairs at P = 48), so the angle
between them is exactly `sin^-1 (1 / (|D| |D'|))`, and in the flight
table's own integers, with `T_D = isqrt(3 |D|^2 Q^2)` the law's resolution
of |D|,

    gap(D, D') = 3 Q^2 / (T_D T_D'),      a_D = floor(G x (gap(D^-, D) + gap(D, D^+)) / 2)

with G the weights' grain (the exact 1 / (|D| |D'|) within 1 / T_D, below
0.8 percent on a heading and less elsewhere); a fan's edge direction
takes its one gap twice. The rows re-emitted are `(w a_D, m A, p)` by the
split as built, `A = sum a_D^2`. Equal weights per direction are not
this rule and give a comb: the number of Farey directions landing on a
pixel is arithmetic, not uniform (section 5 of `TWO_SLITS.md`'s follow-up
map: Pearson 0.65 with the cosine at P = 64 with equal weights, 0.90
with the angle weights). Bounds at P = 48: 1423 directions in the
plane, within the direction table's 4096 and its components within 64;
at G = 2^18 the weights run 123 to 5619, A = 714 364 777 (2^29.4), the
multiplicity 5 A within 2^32; the load-time ceiling multiplies every
re-emitter's A on the world (two openings: A^2), so G = 2^18 is the
largest power of two that keeps A^2 within 2^62; the rounding of the
smallest weight at that grain is below 0.5 percent. The registered
fan of 91 is this rule's P = 12 without the weights.

**The world** `examples/events/amplitude/slits_huygens.json` (written by
`make_worlds.py`, `two_slits_huygens`): `slits_low`'s geometry, lamp and
frequency, each opening's fan the Farey fan of width 48 restricted to
|b| <= 13 a by the freed band of 6 (the 96 steeper directions would walk
into the wall at x = 8 or through the other opening: 1327 directions,
3.5 percent of the angle lost at the edges), the integer angle weights
at G = 2^18 as the split's `weights`, 420 intervals; no src change. The
expectation was pinned in the series' README before the run from
`two_slits_map.py`'s walk with these weights (the built phase, the click
as built).

**The run** (2026-09-20, main f89884f9 merged into `claude/series-m-masses`,
the outputs in the session's scratchpad; 420 intervals in 76.3 s, 0.18 s
per interval, 2659 rows per record, completed and conserved at every
tick; 271 records gathered, 149 open at the end; the page
<https://claude.ai/artifact/6pyy8C62muHshZ7iMDCUx9>). Every pinned
number reproduced:

| reading | pinned | measured |
| --- | --- | --- |
| the first record's total of the birth norm; shares wall / screen / faces | 2.677; 0.224 / 0.410 / 0.366 | 2.6771; 0.224 / 0.410 / 0.366 |
| the screen WEIGHTS: Pearson with the Euclidean cosine; visibility (bright y = 35 to 38, 59 to 61, 82 to 85 against dark 13 to 20, 48 to 50, 70 to 72, 100 to 107) | 0.895; 0.954 | 0.895; 0.954 |
| the peak pixel and its share of the total (the rung 1 / 2N = 0.0078) | y = 59, 0.012 | y = 59, 0.01204 |
| the CLICKS of the first 64 births: wall, screen on pixels, faces | 14, 27 on 27, 23 | 14, 27 on the pinned 27, 23 |
| clicks at the dark pixels | none | none in 271 |
| distinct cells | 32 over 64 births, the same after | 32 in the first 64, 32 in all 271; every u clicked its one cell at every birth |
| the click histogram's Pearson with the cosine | 0.499 at 64 births | 0.493 at 271 (the bright pixels 4 0 4 0 4 4 4 0 4 0 4) |

So the GameBoard's reading separates the two: **the fringes are in the
record's weights** (Young's pattern at the Euclidean spacing, visibility
0.95, from the fan by angle alone, under the built phase and no src
change), **and the clicks cannot show them** (27 screen cells of 121,
fixed for the whole run, because u repeats with the period 64; the
cumulative rungs do fall where the weights are, none at a dark pixel).
Refutation line: none of its four conditions occurred. The wheel of
section 3 (or section 8's golden rate) is what turns the weights into
counts.

## 8. The birth wheel under "one mechanism": the golden rate against the bit reversal

On the Boss's item B (2026-09-20, after the owner's rule of the day, "no
registers at Nodes, no tables", one mechanism for every count): the bit
reversal of section 3 is a permutation of the ordinal's bits, a rule of
its own beside the counts' mechanism `acc += r; e = [acc >= d]; acc -= e d`.
The alternative that IS the mechanism: `u_W = (ordinal x r) mod W`, a
count on the lamp's record at the rate r / W with r / W near the golden
ratio's conjugate (W = 4096, r = 2531 = the nearest odd integer to 0.618 W,
coprime to W), the Weyl sequence, whose every prefix is equidistributed
by the three-distance theorem; the rungs `(2 W C_j + T) // (2 T)` as in
section 3, the rows' birth phase the lamp's clock (ordinal mod 64) on
both wheels. Every integer is from `wheel_map.py` beside this file
(`wheel_map.out`; the three cases of section 4 at 256 and 4096 births).

| case, wheel | 256 births: screen on pixels, bright, dark | 4096 births: bright, dark, Pearson, visibility | empty cells (with weight) at 64 / 256 / 1024 / 4096 | worst prefix discrepancy at 4096 |
| --- | --- | --- | --- | --- |
| the registered fan, bit-reversed | 62 on 43; 0 2 0 1 4 7 5 0 0 2 0; at most 2 | 0 32 0 8 71 109 71 8 0 32 0; 0 to 27; 0.367; 0.693 | 60 / 32 / 0 / 0 | 1.08 |
| the registered fan, golden | 62 on 45; 0 2 0 1 5 6 4 1 0 1 0; at most 1 | 0 32 0 8 72 108 71 8 0 32 0; 0 to 27; 0.368; 0.695 | 61 / 30 / 0 / 0 | 1.14 |
| the screen's fan, the wheel alone, bit-reversed | 91 on 71; 1 to 2; at most 1 | 24 to 29; 0 to 4; 0.905; 0.924 | 77 / 28 / 0 / 0 | 0.76 |
| the screen's fan, the wheel alone, golden | 91 on 69; 1 to 3; at most 1 | 25 to 29; 0 to 4; 0.904; 0.924 | 76 / 30 / 1 / 0 | 0.76 |
| the screen's fan, the wheel and the exact phase, bit-reversed | 90 on 70; 1 to 2; at most 1 | 28 to 29; 0 to 3; 0.963; 0.954 | 97 / 49 / 22 / 12 | 0.94 |
| the screen's fan, the wheel and the exact phase, golden | 90 on 68; 1 to 3; at most 1 | 28 to 29; 0 to 3; 0.963; 0.954 | 96 / 51 / 22 / 12 | 0.94 |

(The 12 cells still empty at 4096 births under the exact phase are the
cells of weight below 1 / 2W, the dark pixels' own; the same 12 on both
wheels.) At 4096 births the two wheels give the same counts on every
pixel within one click, the same Pearson and visibility to three places,
and a worst prefix discrepancy within 1.14 clicks of B x weight / total
on both; at 256 births the golden wheel is slightly less even (bright
pixels 1 to 3 against 1 to 2), the Weyl sequence's discrepancy being
larger by a constant than van der Corput's at small prefixes, and it
fills the cells at the same prefixes (the registered fan: 30 empty at
256 against 32, 0 at 1024 on both).

**Verdict, one line:** the golden rate is the generic wheel, since it is
the counts' one mechanism with the accumulator itself as u (one row of
the counts table, rate 2531 / 4096, no cap, nothing else), and it loses
nothing the bit reversal has that a run can read: the same counts at
4096, the same cells filled by 1024, a prefix discrepancy within one
click; the bit reversal's one advantage, an exactly stratified prefix at
every power of two, is a property no click reads. The words for the
owner: u is the lamp's count on the wheel W at the golden rate.
