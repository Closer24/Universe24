# The moving laboratory's anisotropy without a contraction: what the six verbs give, what would remove it, and the grain of any contraction (the G2 experimenter, read-only, 2026-09-21)

Problem (3) of the seven (record 393 of the log of 2026-09-20, on the
Boss's branch at the time of writing; the Boss's order of 15:00Z under
record 396's rules): NATURE row 5b, "the anisotropy of c between a
laboratory's two arms when the laboratory moves through the lattice's
frame", registered FAIL by eight to nine orders (DERIVATIONS 12.3: the
round trip `gamma^2` along the motion and `gamma` across, no
contraction). The question: is there, within the six verbs as declared,
a reading of a moving laboratory that is isotropic without a contraction
of the arm along the motion; if not, what exactly would remove the
anisotropy, and what does the lattice's grain do to it. Read against
`main` at b7ddf93 (form B and covariant-readings-v1 not on `main`;
`source-velocity-v1` named in DERIVATIONS 17.6 M4 and not designed).
Every number is from [moving_laboratory_map.py](moving_laboratory_map.py)
beside this note (the engine's flight rule, `direction_flight`, the one
import; the Manhattan accumulator of BEAM_LAW section 3 step 1
transcribed; no run, no fit) and its output
[moving_laboratory_map.out](moving_laboratory_map.out); nothing here is
registered, built or decided. Notation: `beta = v / c_h` with `c_h = 32 /
55` Links per interval the heading's pace, `gamma = 1 / sqrt(1 -
beta^2)`, d the arm in Links, k the bodies' step (one Link per k
intervals, `v = 1 / k`), s the factor by which the arm along the motion
is shorter in motion than at rest (`s = 1` no contraction, `s = 1 /
gamma` Lorentz's); the Robertson-Mansouri-Sexl coefficients `alpha`
(the clock), `beta_L` (the arm along), `delta` (the arm across).

## 0. The verdicts, stated at the top

| Candidate | What it is | Verdict |
| --- | --- | --- |
| (A) the law as built: the rows at one pace in the lattice's frame, the bond a whole Link, the counter unslowed | the classical ether at rest in the lattice | **NOT REACHED, exact** (sections 2 and 3): two arms of one length differ by `gamma` in their round trips; the Michelson-Morley coefficient is the ether's full `1 / 2`, Kennedy-Thorndike's 1, Ives-Stilwell's `1 / 2`; no verb of the six reads the laboratory's velocity into a row's pace or a Link's length; the FAIL of row 5b stands as the law's own prediction, `gamma - 1 = 5 x 10^-9` at the Earth's `beta = 10^-4` against `10^-17` |
| (A') the same under covariant-readings-v1 (the counter at `1 / gamma`) | the clock half of the owner's form (record 162), without the length half | **NOT REACHED** for row 5b: the Michelson-Morley coefficient stays `1 / 2` (a common clock does not move a fringe), Kennedy-Thorndike's halves to `1 / 2`, Ives-Stilwell's closes to 0 (rows 4a, 4b PASS as the two reviews found); 17.6 M4 and M5 withdrew the 5b pin from this identity, and the map agrees |
| (B) the arm as the law's own bond under the six (DERIVATIONS 12b.2: a pair held by exchanged rows and the retarded push, thrown) | the owner's form's length half, tried on the verbs as declared | **NOT ADMISSIBLE** as the null (section 4): the six give a contraction of the wrong size (the dispersion's 0.87 to 0.96 where `1 / gamma` is 0.977 at `beta = 0.215`) or an elongation (1.2 by the retarded flux without the aberration), unstable (the bond unbound within 2200 intervals); the residual anisotropy `s gamma - 1` is -0.11 to +0.23 where nature reads 0 |
| (C) `source-velocity-v1` (named in 17.6 M4, not designed): a row carrying its source's momentum label, the push's magnetic part `q v x B` from it | Lorentz's 1904 argument on Heaviside's field: a bond of the law contracted by `1 / gamma` exactly in the continuum | **REACHABLE IN FORM, conditional on the design, and bounded by the grain** (sections 4 to 6): the Michelson-Morley coefficient 0 for a laboratory made of the law's bonds, Kennedy-Thorndike's 0 with the counter at `1 / gamma`; the identity passes the three tests in form; the lattice's whole Link then bounds the null: an arm of d Links contracts to whole Links, the residual anisotropy is at most `gamma / (2 d)`, and a null at `10^-17` needs an arm of `5 x 10^16` Links, the order of row 5a's bound on Q |

The answer to the order's question in one sentence: without a
contraction the anisotropy of a moving laboratory is exact and equal to
`gamma - 1`, nothing in the six verbs as declared removes it (the
aberration changes which rows arrive and not when, the crossing count
stretches or speeds a pair and contracts nothing, the bond under the
retarded push contracts by the wrong amount and comes apart), the one
thing that removes it is the magnetic part of the push, which needs a row
to carry its source's velocity, one named identity that nobody has
designed; and even under it the lattice contracts an arm by whole Links,
so the null at nature's `10^-17` is a statement about the laboratory's
size in Links, `5 x 10^16` at least, the same order as the grain bound of
row 5a. The owner's form of Lorentz (record 162, "a body's clock and
length made of rays at c") is two halves: the clock half is reached for
the rows' clocks (the lorentz note's Theorem 2, `gamma` by Pythagoras in
the flight table) and declared for a body's counter (its Theorem 3); the
length half is this problem, and it is not reached by the six.

## 1. The pins, before any number

Nature's (the map's section A):

| Pin | Nature | Source |
| --- | --- | --- |
| The Michelson-Morley shift on a 90-degree rotation | expected `2 d beta^2 / lambda = 0.40` fringe at the Earth's `beta = 10^-4` with the 11 m arm; observed below 0.01 ("less than one twentieth, probably less than one fortieth, of the expected") | Michelson and Morley 1887, Am. J. Sci. 34, 333 |
| The resonators' anisotropy of c between two arms | `delta c / c` below about `10^-17`; `9.2 +- 10.7 x 10^-19` | Herrmann et al. 2009, Phys. Rev. D 80, 105011; Nagel et al. 2015, Nature Communications 6, 8174 |
| The Robertson-Mansouri-Sexl coefficients | a moving laboratory's clock `1 + alpha beta^2`, its arm along `1 + beta_L beta^2`, across `1 + delta beta^2`; Michelson-Morley reads `beta_L - delta + 1 / 2`, Kennedy-Thorndike `alpha - beta_L + 1`, Ives-Stilwell `alpha + 1 / 2`; relativity `-1 / 2, -1 / 2, 0`, all three coefficients 0; the ether at rest `0, 0, 0`, the coefficients `1 / 2, 1, 1 / 2` | Robertson 1949; Mansouri and Sexl 1977; Kennedy and Thorndike 1932; Ives and Stilwell 1938; Botermann et al. 2014 (`2.3 x 10^-9` on the clock's) |

The model's (the register and the derivations): NATURE row 5b, FAIL by
`beta^2 / 2 = 5 x 10^-9` against `10^-17`, pinned by
[DERIVATIONS 12.3](../../../DERIVATIONS_BEAM.md#123-the-bond-clock-under-1-to-3)
(the round trip `gamma^2` along and `gamma` across; on the flight table
1.375 and 1.140 at `beta = 0.4297` for a one-Link pair); the pair in
motion of 12.4 not run; 17.6 M4 ("Lorentz's 1904 pair is NOT derived
from `-grad(A)`") and M5 (the 5b pin withdrawn from covariant-readings-v1);
21.4 row E3 (the contraction NOT in covariant-readings-v1; the geometry
when `source-velocity-v1` comes: 12b.2's thrown orbit, the extents' ratio
0.903 at `beta = 0.43`); the paper's row 6 ("REFUTED on `main` by nine
orders; the contraction not derived under covariant-readings-v1 either").
What must not move: every world without a key byte for byte; the law's
prediction of row 5b as a FAIL kept on the register.

## 2. The GameBoard first: the law's laboratory and its two round trips

A laboratory of the law is bodies: a lamp (a paid family releasing one
row per interval on a fan), a mirror d Links ahead on the heading +x and
a mirror d Links across on +y (bodies with a `measure` entry that
re-emit what they click, BEAM_LAW section 5), a detector at the lamp,
all given the same momentum so that each steps one Link every k
intervals (`v = 1 / k`). A row flies at the flight table's pace on its
digital line in the lattice's frame whatever its source does (BEAM_LAW
section 3 step 1; the aberration rule of 12.2, were it built, moves
the released direction, not the pace). The along arm: the forward leg
chases a mirror stepping away, the backward leg meets a lamp stepping
toward it. The across arm: the only rows that reach the co-moving mirror
are the ones aimed at `(a, d)` with a the mirror's advance during the
transit; their transit is the direction's own age at `a + d`, Pythagoras
in the flight table's `T_D` (the lorentz note's Theorem 2). The map's
section C, in whole intervals of the flight rule:

| d | k | `beta` | rest round trip | along: forward, back, round trip | along / rest against `gamma^2` | across: the direction the mirror meets, round trip | across / rest against `gamma` | along / across against `gamma` | the difference, intervals | the fringe shift on a 90-degree rotation (the turn 8: twice the difference over 8) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 12 | 4 | 0.4297 | 40 | 34, 14, 48 | 1.200 (1.226) | (5, 12), 44 | 1.100 (1.107) | 1.091 (1.107) | +4 | 1.0 |
| 12 | 8 | 0.2148 | 40 | 25, 17, 42 | 1.050 (1.048) | (2, 12), 42 | 1.050 (1.024) | 1.000 (1.024) | 0 | 0 |
| 12 | 16 | 0.1074 | 40 | 22, 19, 41 | 1.025 (1.012) | (1, 12), 42 | 1.050 (1.006) | 0.976 (1.006) | -1 | -0.25 |
| 24 | 4 | 0.4297 | 82 | 70, 29, 99 | 1.207 (1.226) | (11, 24), 92 | 1.122 (1.107) | 1.076 (1.107) | +7 | 1.75 |
| 24 | 8 | 0.2148 | 82 | 51, 34, 85 | 1.037 (1.048) | (5, 24), 84 | 1.024 (1.024) | 1.012 (1.024) | +1 | 0.25 |
| 48 | 4 | 0.4297 | 164 | 142, 58, 200 | 1.220 (1.226) | (22, 48), 182 | 1.110 (1.107) | 1.099 (1.107) | +18 | 4.5 |
| 48 | 8 | 0.2148 | 164 | 103, 67, 170 | 1.037 (1.048) | (10, 48), 170 | 1.037 (1.024) | 1.000 (1.024) | 0 | 0 |
| 48 | 16 | 0.1074 | 164 | 91, 74, 165 | 1.006 (1.012) | (5, 48), 166 | 1.012 (1.006) | 0.994 (1.006) | -1 | -0.25 |

(The arm of 6 Links and the rest of the table are in the output.) Three
things the lattice says:

- **The continuum's ether clock is what the lattice approaches.** At
  `beta = 0.43` the along arm reads 1.200 to 1.220 of the rest round
  trip against `gamma^2 = 1.226`, the across arm 1.100 to 1.122 against
  `gamma = 1.107`, and the two arms differ by 1.076 to 1.099 against
  `gamma`: the anisotropy is there, whole intervals of it (4 to 18 on
  arms of 12 to 48 Links), a shift of 1 to 4.5 fringes of the register's
  lamp on a rotation.
- **Below `beta = 0.22` and arms of 48 Links the grain hides it.** The
  accumulator's whole interval per leg and the bodies' whole steps put
  each round trip one or two intervals off its closed form, and the two
  arms' difference (`gamma (gamma - 1) x 2 d / c_h`, 4 intervals at
  `k = 8`, `d = 48`) falls inside that: the lattice reads 0, +1 or -1
  intervals, of either sign. A run at the register's usual `k = 8` would
  read a fringe shift within the grain and prove nothing; the signature
  is at `k = 4`.
- **The fringe is the wheel's.** The two arms' rows that arrive together
  were re-emitted at the beam splitter that many intervals apart, and
  the phase a row carries is its wheel's at the re-emission (BEAM_LAW
  section 5: the set's phase returned to the event, "what it emits
  afterwards carries the phase it received"); the detector's pointer
  reads the difference as a phase, one fringe per 8 intervals for the
  register's lamp. A common slowing of every clock in the laboratory
  (candidate A') changes both phases alike and moves no fringe.

## 3. Why no verb of the six removes it

The two round trips are fixed by two things only: the rows' pace on
their digital lines, which is the flight table's and the same in the
lattice's frame for every source (12.1 (1), BEAM_LAW note 38), and the
mirrors' positions, which are the drive's whole Links. What could read
the laboratory's velocity into either, rule by rule:

- **The flight** reads nothing of the crowd or of its source (BEAM_LAW
  note 47, the walk's row: "nothing"). The clock's word (the age moment
  or the presence) is the clock's, not the flight's; optical-v1 makes a
  row's pace read the crowd's age moment, a field of the masses about
  the laboratory and not of its motion, and a laboratory in an empty
  region reads none. The bending note (#602) says the same from the
  other side: the space part has no verb.
- **The aberration** (12.2, one of the six: a translation and a
  comparison) moves a moving body's released direction and changes
  which rows arrive, not when: the round trips of 12.3 are the same with
  it (12.3, "the aberration changes which rows arrive, not when").
- **The crossing count** (route C, 12c) charges a mover for the rows it
  meets; on a co-moving pair it stretches an unaberrated pair and speeds
  an aberrated one (12c.3), and in an empty world it does nothing: no
  contraction.
- **The push as declared** (the retarded flux, 12.1) and **`-grad(A)`
  alone** (covariant-readings-v1 (ii), 17.6 M4) give a co-moving pair
  the rest force along the motion and `gamma` times it across, Maxwell's
  are `1 - beta^2` and `1 / gamma`: the pair does not settle at Lorentz's
  separation; 12b.2's orbit thrown contracts by the dispersion's factor
  and comes apart (candidate B).
- **A body's counter** (Theorem 1 of the lorentz note) reads nothing of
  its motion; a slowed counter would in any case be common to both arms.

So the anisotropy is a theorem of the six as declared: `along / across =
gamma` in the continuum, exact, and the lattice's whole intervals about
it. This is not a number to run for; it is the register's row 5b as
stated, now with its mechanism written on the GameBoard.

## 4. The candidates against the three coefficients

The map's section E1, with the factor s of the arm along the motion
written as `1 + beta_L beta^2` at `beta = 0.2148` (12b.2's speed, where
`1 / gamma = 0.977`):

| Candidate | `alpha` | `beta_L` | `delta` | Michelson-Morley | Kennedy-Thorndike | Ives-Stilwell |
| --- | --- | --- | --- | --- | --- | --- |
| (A) the law as built | 0 | 0 | 0 | +0.500 | +1.000 | +0.500 |
| (A') covariant-readings-v1 | -0.5 | 0 | 0 | +0.500 | +0.500 | 0 |
| (B) the bond under the six, `s = 0.87` (the dispersion) | -0.5 | -2.82 | 0 | -2.32 | +3.32 | 0 |
| (B) `s = 0.96` | -0.5 | -0.87 | 0 | -0.37 | +1.37 | 0 |
| (B) `s = 1.2` (the retarded flux, no aberration; the pins of 12b.2) | -0.5 | +4.33 | 0 | +4.83 | -3.83 | 0 |
| (C) `source-velocity-v1`, Lorentz's 1904 pair | -0.5 | -0.5 | 0 | 0 | +1.000 with the counter unslowed; 0 with it at `1 / gamma` | 0 |

The residual anisotropy `s gamma - 1` of the along arm (E2): at `beta =
0.43`, +0.107 with no contraction, -0.037 at `s = 0.87`, +0.063 at
`0.96`, +0.329 at `1.2`, 0 at `1 / gamma`. Candidate (B) is the
owner's form's length half tried on the six: a length held by exchanged
rows does change in motion, by the law's dispersion (the longitudinal
mass `m (1 + v / (c - v))^2` against Lorentz's `gamma^3 m`) and by the
retarded flux's self-force, not by `1 / gamma`; and the bond is not
stable in motion. Candidate (C) is Lorentz's own 1904 argument: with the
magnetic part of the push the field of a moving source is Heaviside's
ellipsoid (the age moment already is the Lienard-Wiechert potential,
12.5 (i), reached), a bound pair settles at the contracted separation,
and a laboratory made of such bonds reads c isotropically by round trips.
What the law lacks for it is exactly one thing, named in 17.6 M4: no
row carries its source's velocity and no reading of a Node or its six
neighbours gives it, so `-grad(A)` is the electric part alone.

## 5. The grain of any contraction

The map's section E3. Under candidate (C) an arm of d Links contracts to
the nearest whole number of Links `d' = round(d / gamma)`, and the
residual anisotropy is `d' gamma / d - 1`:

| d | k | `beta` | `d / gamma` | `d'` | residual | without the contraction |
| --- | --- | --- | --- | --- | --- | --- |
| 12 | 4 | 0.4297 | 10.84 | 11 | +0.015 | +0.107 |
| 24 | 8 | 0.2148 | 23.44 | 23 | -0.019 | +0.024 |
| 48 | 4 | 0.4297 | 43.34 | 43 | -0.008 | +0.107 |
| 48 | 8 | 0.2148 | 46.88 | 47 | +0.003 | +0.024 |
| 48 | 16 | 0.1074 | 47.72 | 48 | +0.006 | +0.006 |

The residual is at most `gamma / (2 d)`. A null at `10^-17` with a
contraction quantised to one Link needs an arm of at least `5 x 10^16`
Links (55.5 bits); at the Earth's `beta = 10^-4` an arm of `10^8` Links
would contract by half a Link, that is not at all, and read the full
`gamma - 1 = 5 x 10^-9`. This is the same order as NATURE row 5a's bound
on the grain Q (`5.8 x 10^16` for the one-way anisotropy below `10^-17`):
the two anisotropy rows of NATURE put the same number on the lattice
from two sides, the pace's grain and the length's. Whether the bound is
a laboratory's size in Links or, for a laboratory of many bonds each
below a Link of contraction, a statement that such a laboratory does
not contract at all, is a question of what a bond of one Link does
under the magnetic push (M5: "a contraction of a one-Link bond is not
representable"); the map states the bound for one arm.

## 6. The three tests for `source-velocity-v1` as named, one line each

The identity does not exist as a design; the tests here are on M4's
naming of it ("a row carrying its source's momentum label at release,
one more declared component of the row's record, from which the vector
potential is a bilinear reading at the Node"), in form only:

- **Generic:** one more declared integer component on the row's record
  (the source's momentum label at release, three integers), read as
  `sum amount x age x p_s` at the Node like the age moment is read; no
  family name, no branch on a kind. Pass in form.
- **Vector:** the reading is bilinear in the state (amount x age, then
  the label); the magnetic part of the push is the body's momentum
  crossed with the difference of that reading across the six Ports (a
  curl by central differences, as `-grad(A)` is a gradient by them), a
  bilinear form applied by one `by_drive` with its remainder; no root,
  no float. Pass in form; the integer bound of the product (amount x
  age x label at the register's contents) is the design's to state.
- **Local:** the row carries the label; the Node reads its own rows and
  its six neighbours' (M4's reading set); fixed work per row for fixed
  K; the cost three more columns of the moment table per row, a host
  cost to be measured. Pass in form.

The tests admit the form; they do not decide the size of the contraction
on the lattice (section 5) or the stability of the bond in motion
(12b.2's pins: unbound within 2200 intervals without the magnetic part;
with it, unknown until designed and run).

## 7. The owner's question on the conditional derivations, for this problem

**Derived on the GameBoard from the six verbs:**

- the rows' one pace in the lattice's frame and the wave equation's
  Lorentz symmetry in the limit (4.1);
- the transverse light clock's `gamma` by Pythagoras in the flight
  table's `T_D` (the lorentz note's Theorem 2), and the longitudinal
  `gamma^2` (12.3, the map's section C): the ether clock;
- the anisotropy `gamma - 1` of a moving laboratory without a
  contraction, exact (section 3): the law's prediction of row 5b as a
  FAIL is a theorem, not a reading;
- the field of a moving source as the Lienard-Wiechert potential, whose
  equipotentials are Heaviside's ellipsoids contracted by `1 / gamma`
  (12.5 (i)): the FIELD's contraction is derived.

**Conditional (a declaration, not a derivation):**

- **the magnetic part of the push**, hence the bond's contraction by
  `1 / gamma` and the Michelson-Morley null: conditional on
  `source-velocity-v1`, a row carrying its source's velocity. M4 proves
  no reading of a Node and its six neighbours gives the source's
  velocity from the rows as they are; the label must be on the row. This
  is the one declaration between the law and the null.
- **the isotropy of the whole** (the contraction and the clock's `gamma`
  together, Kennedy-Thorndike's 0): conditional on both
  covariant-readings-v1 (one declared coupling, its form forced) and
  `source-velocity-v1`.
- **the lattice's grain**: not a declaration but a bound (section 5); a
  null at `10^-17` is a statement about the laboratory's size in Links.

Enough, or derive? The anisotropy without a contraction is derived, and
so is what removes it in form. The identity that removes it is bounded
and nameable: one record component at release, the push's magnetic part
by central differences, the reading set of M4. If the owner wants the
null reached, that design is the task, with 12b.2's thrown orbit as its
pin geometry (E3, M5) and this note's `k = 4, d = 48` laboratory as the
reading; nothing in this note derives it from the six as they are, and I
know no route that does.

## 8. Proposed lines for the documents I do not write

- **NATURE row 5b** (the physicist), the verdict cell: after "pinned by
  12.3": "the law's laboratory on the lattice (the moving-laboratory
  note): the anisotropy 1.08 to 1.10 against `gamma` 1.107 at `beta =
  0.43` on arms of 12 to 48 Links, hidden inside the whole-interval
  grain at `beta <= 0.21` and arms up to 48; under any contraction
  quantised to one Link the null at `10^-17` needs an arm of `5 x 10^16`
  Links".
- **DERIVATIONS 12.3** (the derivation mathematician): the one-Link
  pair's 1.375 and 1.140 supplemented by the arms of 12 to 48 Links
  (section 2's table): the lattice approaches the closed forms as the
  arm grows.
- **DERIVATIONS 21.4 row E3**: "the geometry when it comes" gains the
  reading: a laboratory of two arms at `k = 4`, `d = 48`, the difference
  18 intervals, 4.5 fringes on a rotation, to be 0 within the grain
  (`+-1` interval) under the identity.
- **The paper's row 6**: "REFUTED on `main` by nine orders" stands;
  after "the contraction not derived under covariant-readings-v1
  either": "removed in form by `source-velocity-v1` (Lorentz 1904), and
  then bounded by the lattice's whole Link: `5 x 10^16` Links per arm for
  `10^-17`".
- **HIGHLIGHTS 5.4**: nothing; no decision here.

## 9. Questions, through the Boss

1. **For the owner (substantive):** is `source-velocity-v1` to be
   designed? It is the one declaration between the law and the
   Michelson-Morley null, bounded (one record component, the push's
   magnetic part), and it is also what Faraday, Ampere-Maxwell and the
   Lorentz force wait on (21.5 rows 49 and 50). Without it row 5b stays a
   FAIL by theorem, and the paper says so.
2. **For the owner (substantive):** the grain bound of section 5. Is "a
   laboratory of `5 x 10^16` Links per arm" an acceptable statement of
   the paper beside row 5a's "Q of `5.8 x 10^16`", or does the owner read
   the lattice's Link as far below any laboratory's size so that both
   bounds are met, in which case the note should say so and stop
   counting?
3. **For the Boss:** the two-arm laboratory at `k = 4`, `d = 48` (a lamp,
   two re-emitting mirrors, a detector, all thrown; two worlds of series
   K's size, no key, no engine change) reads the law's anisotropy through
   a detector for the first time: 18 intervals, 4.5 fringes on a
   rotation, against the grain's `+-1`; the Boss chooses whether it is
   run (record 396).

## 10. Links

[NATURE](../../../NATURE.md) rows 5a and 5b;
[DERIVATIONS_BEAM 12](../../../DERIVATIONS_BEAM.md#12-lorentz-from-the-delay-field-without-a-seventh-verb)
(12.1 to 12.5),
[12b.2](../../../DERIVATIONS_BEAM.md#12b2-the-orbit-as-the-bond-the-registered-orbit-thrown),
[12c.3](../../../DERIVATIONS_BEAM.md#12c3-the-bond-under-route-c-no-contraction-a-stretch-or-a-speeding),
[17.6](../../../DERIVATIONS_BEAM.md#176-amended-per-the-physics-rule-review-of-covariant-readings-v1-record-297-the-nine-must-fixes-the-integer-forms-the-should-fixes)
(M4, M5) and
[18.1](../../../DERIVATIONS_BEAM.md#181-the-clock-in-motion-rows-4a-4b-5b-closed-on-paper-by-section-17);
[BEAM_LAW section 3](../../../BEAM_LAW.md#3-the-nodes-interval-nature_beam)
(step 1, notes 38 and 47) and
[section 5](../../../BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors);
[the owner's form of Lorentz, record 162](../../../LOG_2026-09-20.md);
[problem (2), special relativity from the six verbs](../lorentz/NOTE.md)
(Theorems 1 to 3); problem (1), the bending of light (PR #602, the space
part has no verb);
[the three tests](../../../../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202).
