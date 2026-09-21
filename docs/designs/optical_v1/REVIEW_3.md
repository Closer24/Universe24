# Physics-rule review of `optical-v1` in its generic form, before the build (third round)

The open-problems physicist acting as the physics-rule reviewer,
2026-09-21, on the Boss's bounded order of 16:01Z under the owner's
decision of 16:4xZ ("Clearly, in the generic form"; record 309 item 4: the
review before the build). Read-only, docs only, no run, nothing edited on
any branch. The object is not one file: the generic `optical-v1` is
assembled from (a) the light-bending note's section 6 (the six
corrections to `optical-v1`, main), (b) the one-wall design note as
corrected (docs/designs/one_wall/NOTE.md on branch claude/one-wall-design,
PR #618, head 114248b3: the three verbs in integers, the pins from the
lattice's lines, the refusals, the host price) and (c) the chief
physicist's re-read (docs/designs/one_wall/PHYSICIST.md on branch
claude/one-wall-physicist, PR #619, head 9af20d50: `one-wall-v1` withdrawn;
what survives is one wall function over a declared set with a coefficient
each, the clock 1, the flight 1 + gamma, the phase per age 0, and one
vector verb for the turn with the weight (E^2 + 3 gamma **p** . **p**) / E,
under the key `optical`, gamma the world's input), against the two earlier
reviews of `optical-v1` ([the first](../gr_rows/REVIEW.md), ADMISSIBLE
WITH MUST-FIXES; [the second](../gr_rows/REVIEW_ROUND2.md), BUILDABLE) and
[the amended design](../gr_rows/DESIGN.md). Read first: HIGHLIGHTS 5.4 on
main (the three tests, record 202; one motion primitive for a body as for
a row, record 183; the age word, record 394; the covariant readings,
record 270; optical-v1's go, record 303), BEAM_LAW section 3, DERIVATIONS
5.1 and 17.6, the covariant readings as merged (PR #582, the energy E' by
comparisons and its one-axis domain), issue #605 (closed on PR #619's
verdict).

Notation, once (record 369): **p** the momentum vector in label units and
p its magnitude; **u**_D the unit label of the direction D at the scale
Q = 64 (|**u**_D| = Q within 1.35 percent); T_D = isqrt(3 |D|^2 Q^2) the
direction's resolution (110 on a heading, |D| times that on a fan
direction); e_D = isqrt(3 **u**_D . **u**_D), 110 or 111 on every
direction; c = 1 / sqrt 3 Links per interval, c_h = 64 / 110 on a heading;
S the width, M a body's content, m = Q S M its rest energy in mass units,
E = isqrt(m^2 + 3 **p** . **p**) its energy in the same units (the covariant
readings' E', 17.6 M3; for a row m = 0 and E = content x e_D), gamma_L =
E / m the Lorentz factor, beta the speed over c; A the age moment of the
other numbers' rows at a Node and **V** their flow (the one reading set,
BEAM_LAW note 47), [n, d] the world's suspension pair, k = n A / d the
clock's count; gamma (without a subscript) the post-Newtonian parameter,
the world's declared input, f = 1 + gamma the flight's coefficient;
`by_drive(acc, rate, wall)` the one count primitive; a DETECTOR reading a
detector's record, a GAMEBOARD reading the host's view (record 281).

## VERDICT: ADMISSIBLE WITH CORRECTIONS

The generic form is the amended `optical-v1` with two changes that make it
better, not different: the turn's weight is the row's or body's energy in
the law's value form with gamma declared once (so a row of light and a
body are one rule under the key, and the turn's coefficient stops
depending on the row's direction, section 1), and the wall function's set
is stated with its coefficients (the clock 1 by the law, the flight
1 + gamma by the key, the phase per age 0, never stretched). Every rule
passes the three tests (section 1), every input is local (section 2), the
pins are detector readings with their derivations (sections 3 and 5), the
key gates every path (section 4). Four corrections to the design text
must be made before the build, because as assembled the text (1) writes
the turn's rate with the direction's T_D where the physics has the
direction-independent e_D, a factor 12 on series K's own beam directions;
(2) gives a moving body's weight E, which on `main` exists only under the
covariant readings' key and its one-axis domain, so the series D pin
cannot be run on `main` and the design must say what runs now and what
waits on form B; (3) leaves the body's drive out of the declared set
without saying so, although under form B the drive is the flight
primitive; (4) declares gamma, the pair, the 3 of the weight and the
refusals in three places with three wordings. Five should-fixes follow.
The build (Far 2, after clock-age-v1) may start on the text once the four
are in it; the verdict on the physics is unchanged from the earlier rounds:
a hypothesis beside the law, nothing of it in the law, PPN gamma an input.

## 1. The three tests, one line each per rule

1. **The wall function over the declared set** (verb 1: `by_drive(acc,
   rate x d, wall x (d + c_i n A))` for each accumulator i in the set,
   c_i its coefficient: the clock 1, the flight 1 + gamma, the phase per
   age 0). Generic: PASS, one primitive, the coefficients values of the
   identity and not branches, no family name (a row is the value m = 0).
   Vector: PASS, a translation whose wall is linear in the read state (the
   growing wall's form, 15.2 and 15.6, admitted twice before); the
   flight's accumulator becomes a field of the row's record with its
   residue (the second round's must-fix 4, closed) and the click's exact
   phase reads it. Local: PASS, the row's own record and the moments of
   its own Node, recomputed per interval, nothing kept at a Node. The
   clock's coefficient 1 is not the key's: it is clock-age-v1, the law's
   default (record 394), on with or without `optical`; the key adds the
   flight at 1 + gamma. The phase per age at 0 is right physics (a static
   crowd conserves a row's frequency in transit; the redshift is the
   emitter's clock against the receiver's, DERIVATIONS 5.2) and PHYSICIST's
   correction of #605 stands.
2. **The turn with the energy as the weight** (verb 2: the row's momentum
   accumulator **w** translated per interval by the transverse flow at the
   rate n x weight x (Q^2 **V** - (**V** . **u**) **u**) with weight =
   (E^2 + 3 gamma **p** . **p**) / E, the comparison against the fan's
   grain, the permutation to the neighbouring direction with the remainder
   kept, as the amended design's verb 2). Generic: PASS, one primitive for
   a row and a body, the weight a value (for a row E = content x e_D and
   the weight is (1 + gamma) content x e_D; for a body at rest E = m and
   the weight is m, today's push integer). Vector: PASS, the weight is
   one bilinear form (the exact square with the declared gamma) over one
   Euclidean division by E with the remainder kept, E itself by
   comparisons (17.6 M3), no root at run time (e_D a table at load, as
   T_D); the rate is bilinear in the state within the test. Local: PASS,
   the flow of the row's own Node. What the weight fixes, and the design
   must write (must-fix 1): the amended `optical-v1` writes the rate as
   `f n_s T_D G (Q^2 V - (V . u) u)` with T_D the row's direction's
   resolution, and the first review's re-derivation of the angle per
   interval, `f (n_s / d_s)(T_D / Q^2) |V_perp|`, used `c = Q / T_D` and
   `dwell = T_D / Q`, which hold on a heading only; on a direction D the
   pace is |D| Q / T_D and the dwell per Euclidean Link T_D / (|D| Q), so
   the correct coefficient is T_D / |D| = 110.8 for every D, which is e_D
   (110 or 111 on every direction of the table; recomputed: on series K's
   beam directions (12, +-1, 0) and (12, 0, +-1) T_D = 1334 while T_D /
   |D| = 110.8 and e_D = 111). As written the off-heading rows of the
   beam would turn twelve times faster than the heading row; with the
   weight content x e_D they turn alike. The generic form is right; the
   text must carry e_D and drop T_D from verb 2 (T_D stays in verb 1's
   wall, where it is right).
3. **The second-order term on the clock** (the amended design's section 5,
   `owed = by_drive(acc_owed, 2 k n d + 3 k^2 n^2, 2 d^2)` under the same
   key): unchanged by the generic form, its three tests as the earlier
   rounds found them (a bilinear rate, its own record); the design must
   say in one line that it stays under `optical` as it was, or that it is
   dropped (should-fix S1).
4. **The declarations and the refusals** (the key with `suspension` 0,
   with `meeting`, with a wall or rate beyond the register, with a
   direction without its neighbour table, gamma not a non-negative integer
   or pair): read at load from the world's own data; PASS on all three.

## 2. LOCALITY-1

Every input has a local owner: A and **V** are the moments of the rows
present at the row's own Node, read once before step 1 from the rows' own
records (their ages and amounts, their `arrival` marks of the interval
before), one interval retarded as a body's push is (the second round's
must-fix 5, closed); the weight reads the row's own label and content (a
row) or the body's own E (a body, the covariant readings' record); the
neighbour table, e_D and THETA_G are tables at load. The Node holds
nothing; the store per row is four integers (the flight accumulator with
its residue, the three of **w**); fixed work per row per interval for
fixed K (section 6). No event relays information across more than one
Link per interval by this key. Holds.

## 3. The measurement rule

The pins are DETECTOR readings: the click's centroid on the screen (the
pixel), the click's mean age (the delay), the count ratio and the phase
rate at the screen, and, for the factor, the ratio of the centroid's
shift at f = 2 over f = 1 (two worlds); k(b), the deflection in radians,
the lamp's clock rate and the beam's back-reaction are GAMEBOARD and so
labelled in the design's tables and the light-bending note's. Series D's
pin (section 5) reads the orbit's period and extents, GAMEBOARD readings
of a probe's positions, which the register has always labelled so; the
design must label them (should-fix S2). The pinning before the numbers
holds: every number in section 5 is a closed form of the rule's integers
or the light-bending map's offline flight, written before any run.

## 4. Bit-exactness with the key off

A property of the design and a test of the build, as the second round put
it, and unchanged by the generic form: with the key absent no field is
added to the store, no reading is taken before step 1, `Flight`'s wall is
today's 2 T_D, the push's weight is today's content (the covariant key is
another identity, absent by default, PR #582's OFF replay byte for byte),
the clock's count is clock-age-v1's whatever `optical` says. The build's
gate: the 85-world set and `gate_set.json`'s digests byte for byte,
`state.json` and `events.jsonl`, with the key absent. Series K's four
registered worlds declare `suspension` 0, so the key is refused there and
they cannot move: "series K byte for byte" holds by refusal, not by a
run (the pin world is a new world, section 5).

## 5. The world-file declarations and the pins with their derivations

**The declarations** (must-fix 4 asks for them in one place, one
wording): the key `optical` with gamma the world's input (a non-negative
integer, or a pair [n_g, d_g] if the owner wants a PPN gamma off an
integer), f = 1 + gamma derived once and written into the flight's wall
and the turn's weight as the same number (the earlier rounds' must-fix 3
kept); the suspension pair [n, d] the clock's, shared (no second pair);
the 3 of the weight the covariant readings' pair c^2 = [1, d_c] declared
once (17.6 M3), not a literal; the set's members the identity's (the
clock, the flight; the phase per age excluded), not a world list (a world
that could put the phase in the set would need a refusal by name, which
the generic test forbids: should-fix S3); the lamp's `reads: age` no
longer declared (record 394's default; the light-bending note's item 5);
the refusals of section 1 item 4.

**The pin world** (the light-bending note's section 5, the design's
section 4 re-scaled): series K's `mass` and `near` (`heavy` optional) at
the pair [1, 16384], the mass x 16, the key at f = 1 and f = 2, two worlds
each. The derivations, each a closed form recomputed by me on the host at
the note's writing: k(b) from the lattice's lines (the age moment A at the
beam's Node per interval of dwell, `k = A n / d`); the deflection along
the path `2 f k(b)` in the continuum, on the lattice the sum over the
row's dwell of the transverse flow's turn (the map's flow route with the
exact dwell per Node); the centroid's shift the deflection times 26 Links
to the screen; the delay `(f / c) integral of k dl`, on the lattice the
sum of `f n A / d` over the dwell. The pins (DETECTOR if run; the bracket
0.5 pixel and 1 interval): `mass` (2^16, b = 6) the shift -1.93 / -3.86
pixels and the delay 2.68 / 5.36 intervals at f = 1 / f = 2; `heavy`
(2^17, 6) -3.86 / -7.72 and 5.36 / 10.7; `near` (2^16, 3) -2.42 / -4.83
and 2.17 / 4.34; the ratio of the two shifts 2.00 within the bracket, the
number the run reads; the lamp's clock rate under the age word 0.918,
0.849, 1.000 (GAMEBOARD). Under the generic form these pins are unchanged
because for a row the weight (1 + gamma) content x e_D is f times the
heading's constant, which is what the map used (must-fix 1 makes the
design agree with the map on the off-heading rows). What the run cannot
read at P = 6: the 1 / b form (the plane's comb; the light-bending note's
section 4), a second pin at a denser fan.

**Series D's orbit under the key** (PHYSICIST's prediction "by 1 + gamma
beta^2"): must-fix 2 and 3. The weight on a body's push is (E^2 + 3 gamma
**p** . **p**) / E = E (1 + gamma beta^2) since 3 **p** . **p** = E^2 beta^2,
so the push on the body's LABEL is gamma_L (1 + gamma beta^2) times
today's m-weighted push: at gamma = 0 (f = 1) it is gamma_L alone (1.08 at
the physicist's 0.38 c), at gamma = 1 gamma_L (1 + beta^2). The orbit's
response goes through the drive's rule, which on `main` is `step_axis`
(the pace p / (Q S M + |p|) per axis) and under form B the directional
drive; "the orbit moves by 1 + gamma beta^2" is not that number and is
not a derivation. And on `main` a body's E exists only under the
covariant readings' key, whose domain refuses a momentum on more than one
axis (17.6 as built: the per-axis base until form B lands): an orbit is
refused at load. So: the body's weight is a stated form whose pin waits on
form B (or on the covariant domain lifted); the design must say which
worlds run on `main` under the key (rows beside a mass: the pin world) and
which do not yet (a moving body under the energy weight: series D), and
derive series D's pin from the integer forms before its run, not from the
continuum's factor. Until then the design may key the body's weight off
(the push on a body today's m, the row's weight (1 + gamma) content x
e_D), which is the amended `optical-v1` exactly and runs on `main`.

**The body's drive and the set** (must-fix 3). Under form B a body's drive
is the flight primitive on its momentum's direction (record 183), so if
"the flight" is in the set at 1 + gamma the body's drive inherits it and a
moving body's pace in Nodes per interval falls by 1 / (1 + f k) in the
potential (the amended design's section 7, "at the cap term"), while
nature's slow body has no such first-order slowing of its coordinate pace
(the post-Newtonian equation's velocity terms are (2 + 2 gamma) (**v** .
grad U) **v**, momentum-dependent, not a scaling of the pace). The set
must name the body's drive with its coefficient (0, or the flight's with
the reason), and series D's pin must carry the choice.

**Series K byte for byte**: by refusal (section 4).

**The Sun** (GAMEBOARD, the formula's): f = 1 gives 0.876 arcsec and half
Shapiro's coefficient; f = 2 gives 1.751 arcsec and Shapiro's coefficient;
nature reads f = 2.000 +- 0.0002 (VLBI, Cassini). The paper's rows state
that gamma is an input, as HIGHLIGHTS 5.4's line of record 303 and the
light-bending note's item 1 say.

## 6. The host price

Per row per interval beyond today's walk of 16: the wall 2 (a multiply and
an add on A), the turn's rate 10 (a dot product, a scale, three multiplies
and three adds; the weight for a row one table product, for a body one
bilinear form, one comparison walk of E and one division), the comparison
against the fan's neighbours 2 per neighbour (4 to 6), a step 3: about 30,
as the amended design's section 6 counts, and the five columns' reading at
every Node with a row, shared by every row and body there (the main cost;
on series K's `mass` about 3.2 times the walk's count by the one-wall
note's section 7, linear in the rows, nothing that grows with the
GameBoard or the families). The host's segmented sums (the meeting's 4.6
ms per interval on `mass`, note 35 (vii)) are reported apart from the
count. The pin world at the mass x 16: at most sixteen times series K's
rows, an upper bound (the second round's should-fix H).

## 7. Must-fixes (numbered), on the design text before the build

1. **Verb 2's coefficient is e_D, not the direction's T_D.** The amended
   design's `f n_s T_D G (...)` and the first review's derivation are right
   on a heading and wrong by |D| on every other direction; the generic
   weight content x e_D (e_D = isqrt(3 **u**_D . **u**_D), 110 or 111 for
   every D, a table at load listed with T_D and **u**_D) is the coefficient
   for every direction. One sentence in the design's verb 2 and one row in
   its map; the pins of the light-bending note stand (its map used the
   heading's constant).
2. **What runs on `main` and what waits on form B.** A body's E exists on
   `main` only under `covariant_readings` with its one-axis domain; an
   orbit is refused there. The design states the body's weight as the
   form (E^2 + 3 gamma **p** . **p**) / E with its pin deferred to form B
   (or to the domain lifted), and keys it off until then, so that the pin
   world of the rows runs now; series D's pin is derived from the drive's
   integer form (the push on the label gamma_L (1 + gamma beta^2) times
   today's, the pace by the drive's rule) before its run, never stated as
   "1 + gamma beta^2".
3. **The body's drive in the set.** The set names every accumulator of the
   law with its coefficient: the clock 1 (the law's), the flight 1 + gamma
   (the key's), the phase per age 0, the body's drive (under form B the
   flight primitive) with a declared coefficient and the reason; the
   release and the lamp's count 0 (per self-creation, gated by the clock
   already). One table in the design.
4. **One declaration, one wording.** The key `optical` carries gamma (an
   integer or a pair) and nothing else; f = 1 + gamma derived once; the
   pair [n, d] the clock's; the 3 of the weight the covariant pair's d_c;
   the set the identity's; the refusals listed once (with `suspension` 0,
   with `meeting`, beyond the register, a direction without its neighbour
   table, gamma out of range; the key without `covariant_readings` when a
   body moves under the energy weight, until must-fix 2's choice). The
   three texts (the light-bending note's section 6, the one-wall note's
   section 2, the physicist's section 4) say these in three ways; the
   build needs one.

## 8. Should-fixes

- **S1.** The second-order term on the clock (the amended design's
  section 5): kept under `optical` as it was, or dropped; one line.
- **S2.** Series D's readings labelled GAMEBOARD in the pin (the probe's
  positions), the screen's readings of the pin world DETECTOR, as the
  register's convention.
- **S3.** The set fixed by the identity, not declared per world: a world
  list would need a refusal by the accumulator's name (the phase), which
  the generic test forbids; the world declares gamma only.
- **S4.** The wheel's dither correlation between the turn and the click in
  a `sum` set world (the amended design's verb 2, "to be named and tested
  at the build"): the pin world's screen is `wave`, where it is absent;
  the build's test names it.
- **S5.** The one-wall note's pin table at [1, 256] (the push captures the
  beam, the wall stalls it) is the strong-field regime the light-bending
  note left; the design keeps [1, 16384] as the pin and cites [1, 256] as
  the bracket's far end, not as a pin.

## 9. What stands, in one paragraph for the Boss

The owner's "clearly, in the generic form" is the amended `optical-v1`
with the turn's weight the energy in the law's value form and gamma
declared once: one wall function over the identity's set (the clock 1 by
the law, the flight 1 + gamma by the key, the phase never), one vector
verb for the turn, a row and a body one rule. It passes the three tests
and LOCALITY-1, its pins are detector readings with derivations, the key
gates every path, and its numbers at the Sun are the earlier rounds'
(0.876 arcsec at f = 1, 1.751 at f = 2, gamma an input). The four
corrections are text: the turn's coefficient e_D (a factor 12 on series
K's own beam directions if T_D were built), what runs on `main` now (the
rows' pin world) and what waits on form B (a moving body's weight, series
D), the body's drive's place in the set, and one declaration. With them
in the text the build may start; the verdict is ADMISSIBLE WITH
CORRECTIONS, nothing of it in the law.
