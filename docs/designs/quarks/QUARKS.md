# The quarks as families of the family table (the physicist, read-only, 2026-09-21)

The model owner's direction of 2026-09-21 (the log of 2026-09-20, record
249, translated): "try to add the quarks too: model them and bring them
in, so that we try to give their masses and their properties as well;
bring them into our groups; everything enters the groups, as a group or a
set or a vector, within our generic laws; bring the quarks in with all
their families, and check how it converges." Refined the same hour
(record 251): "the quarks get the same binding we have, the ordinary
binding; they just need to be another family, since quarks compose the
proton and the neutron, so they are the base underneath; the quarks have
some specific binding of their own, it is not hard to model it and put it
in our tables; ... I would go down to the smallest, which is the quark;
check whether in the mathematics a group underneath also works out, as
the last group there is from below." And (record 256): "maybe several
masses must be derived: the electron the smallest of its kind, the quark
the smallest of its kind, the quark composing the protons and neutrons;
try to reach the smallest mass by kind from our conditions."

Base: `origin/main` at `5f7fc813` (the records 243 to 256 are in the
Boss's pull request and are cited by number; on this base
[the log](../../LOG_2026-09-20.md) ends at record 228). Nothing under
`src/` is edited and no law changes: a read-only design. Its evidence is
beside it: `quark_numbers.py` (every integer below, recomputed from the
engine's own flight table and the law's push form; its printed output
`quark_numbers.out`), `make_worlds.py` (the seven world files under
`worlds/`, for the run on the owner's go), and a smoke test of the seven
worlds for 24 intervals each (section 4.6), which is the only run made.
Read: [BEAM_LAW](../../BEAM_LAW.md) sections 2 to 5 and its notes 31, 36,
39, 40 and 41; [ENTITY_CATALOG](../../ENTITY_CATALOG.md) (the rows on the
six quarks, the proton, the neutron, the deuteron, the alpha, the gluon,
and [the gap list](../../ENTITY_CATALOG.md#the-gap-list));
[HYPOTHESES 13](../../HYPOTHESES.md#13-confinement-from-the-quarks-field-rays-binding-to-each-other);
[EXPERIMENTS](../../EXPERIMENTS.md) series
[I](../../EXPERIMENTS.md#i-the-nucleus-2026-09-20) and
[J](../../EXPERIMENTS.md#j-the-weak-force-2026-09-20) with their pages
([the nucleus](../../../examples/events/nucleus/README.md),
[the weak force](../../../examples/events/weak/README.md),
[the binding](../../../examples/events/binding/README.md));
[PREDICTIONS 26](../../PREDICTIONS.md#26-the-law-quantises-exactly-what-lives-on-a-compact-group-and-leaves-free-what-lives-on-a-scale-charge-phase-and-direction-have-numbers-mass-has-none);
[DERIVATIONS_BEAM](../../DERIVATIONS_BEAM.md) section 13 (the wait as
the reading's cost, and 13.4, what K leaves free: the family table);
the strong design of 2026-09-20 (`scratchpad/strong/DESIGN.md`, whose
appendix A first placed a quark row) and
[the binding design](../binding_v1/DESIGN.md) (record 115);
[the click's square](../amplitude-v1/CLICK_SQUARE.md) (the law has no
product between rows); [the shared workflow](../../../skills/workflow.md)
(the three tests, the notation, "a formula gives, a run proves").

Notation (record 184): a scalar plain, a vector in bold lowercase, a
matrix in bold uppercase; every symbol named at its first use. Rows and
bodies, not light and matter. One source per number: nature's numbers
are PDG 2024 (S. Navas et al., Phys. Rev. D 110, 030001 (2024)), the
register's are series I and J as recorded, the design's are
`quark_numbers.out` (the section is cited as "numbers N").

**What this design finds, in three lines.** The quarks enter the family
table as they are, six rows with the keys the table already has, and the
strong column that binds the register's nucleons (a held unit of a strong
family, its value sigma per unit of content, its lifetime L as the range)
binds three quark bodies into a line that holds; nothing new is needed
for that, and the engine's first pushes equal the formula's integers to
the unit. What the law does not give: the proton's mass (the bound set
reads the exact sum of its parts, 20 units against nature's 1836), any
growth of the bond with distance (a kicked quark leaves as a free
fractional charge), and a colour with three values (a label is
admissible, a colour force is a seventh verb). The masses are inputs, as
the law says of every mass (PREDICTIONS 26); no condition of the law
selects the quark's count of units, and the two candidates for "the
smallest mass by kind" are confronted and fail against PDG (section 1.5).

## 1. The quarks as families of the family table

### 1.1 The charge unit the register uses

The law's `charge` is rho, the charge per unit of content of a family, a
rational pair `[n, d]` (BEAM_LAW section 2; note 28); a body's charge is
rho times its content, a report, and the push reads the product of two
bodies' charges through the pairs, so no body's charge needs to be whole.
The register uses two scales: the atom's (series H: the proton's rho
`[1, 1]` on 1836 units, the electron's -15 on 1836 units, a declared
asymmetry for the orbit) and the nucleus' (series I and J: the proton's
rho 4 on 1836 units, the whole charge 7344, and the beta's whole charge
-7344 under D-1, so that the electron's charge is minus the proton's).
This design uses the nucleus' scale: **e = 7344** label-charge units is
one elementary charge, and every quark charge below is a third of it.

### 1.2 The six rows

One unit of content is the electron's (record 243: the unit is the
smallest mass; the register's grain is one electron, series N). The
content of a quark row is PDG's mass over the electron's, the nearest
whole count; the whole charge is nature's thirds of e; rho is the
quotient, a reduced pair (numbers 1).

| Row | Mass, PDG 2024 (MeV) | Mass / m_e | Content M (units) | Whole charge (thirds of e = 7344) | rho per unit of content `[n, d]` | Key kind |
| --- | --- | --- | --- | --- | --- | --- |
| `u` | 2.16 | 4.2270 | 4 | +2/3: 4896 | `[1224, 1]` | M INPUT; charge INPUT; rho DERIVED |
| `d` | 4.70 | 9.1977 | 9 | -1/3: -2448 | `[-272, 1]` | the same |
| `s` | 93.5 | 182.9749 | 183 | -1/3: -2448 | `[-816, 61]` | the same |
| `c` | 1273 | 2491.1989 | 2491 | +2/3: 4896 | `[4896, 2491]` | the same |
| `b` | 4183 | 8185.9268 | 8186 | -1/3: -2448 | `[-1224, 4093]` | the same |
| `t` | 172 570 | 337 711.0657 | 337 711 | +2/3: 4896 | `[4896, 337711]` | the same |

The light quarks are PDG's MS-bar masses at 2 GeV, the charm and bottom
at their own scale, the top from the direct measurements; the register's
proton and neutron rows are 1836 and 1839 units (m_p / m_e = 1836.153,
m_n / m_e = 1838.684, their difference 2.531). The sum of a proton's
quark masses is 9.02 MeV, 0.96 % of the proton; of a neutron's 11.56
MeV, 1.23 %.

The other keys of a quark row, each named as the table names it:

| Key | Value on a quark row | Kind | Why |
| --- | --- | --- | --- |
| `quantum` | 0 | INPUT (fixed by kind) | a quark is a body of a free family: its rays carry no content and are read for gravity and electricity (the catalog's principle); a paid family carries no column (the binding design's F1) |
| `phase` | false in the run's worlds | INPUT | as the register's nucleons; a phase circle changes nothing of the binding |
| `charge` | the pair above | DERIVED from two inputs | rho = (thirds of e) / M |
| `columns.strong` on the quark family | none | | the strong column rides on a held unit of a strong family (next row), as the register's nucleon holds one unit of `nuclear`: a `lifetime` on the quark family itself would cut its electric rays at L, and the electric rays live forever |
| `held` on the quark's measured event | `{"glue": 1}` | INPUT | one unit of the strong family `glue`, `columns {"strong": {"value": sigma, "sign": -1}}`, `lifetime` L; sigma is the quark's "specific binding of its own" (record 251), a family key; the run's first case takes the register's sigma 10000 and L 3, "the same binding we have" |
| `lifetime` (of `glue`) | 3 | INPUT | the range: the six neighbours at the age 1, the face diagonals at 2, the cube diagonals and the second Link of a heading at 3 (note 31 (vii)) |
| `become` (the weak force) | per flavour change, below | `into` and the products INPUT; the content R the W carries DERIVED; `at` INPUT through the dictionary | note 36 (iii) |
| `hand` on the products | the W and the neutrino `hand` -1, the antineutrino +1; the parent's `axis` for a polarised quark | INPUT | hand-v1 (note 39): a left-handed product leaves against the parent's axis |
| the decay's `at` | the top alone: nature's width 1.42 GeV, a lifetime of 5 x 10^-25 s (PDG 2024) before any binding; the others decay only bound | INPUT, in intervals through the dictionary (record 210), not fixed here | no quark but the top has a free lifetime |

**The transformations, with the content the W carries** (numbers 1). A
`become` is a measured event's one change of family, its products paid
from what it holds, the charge exact (note 36 (iii)): rho_into x (M - R)
+ c_W = rho_from x M, where c_W is the W's whole charge and R the content
of the products. With the whole charges above this gives **R = M_from -
M_into**, the W carries the difference of the two rows' contents, exactly
as the register's neutron gives its beta the content 3 = 1839 - 1836:

| Change | R (units) | The W's whole charge | State |
| --- | --- | --- | --- |
| d -> u + W- | 9 - 4 = 5 | -7344 | payable |
| s -> u + W- | 183 - 4 = 179 | -7344 | payable |
| c -> s + W+ | 2491 - 183 = 2308 | +7344 | payable |
| b -> c + W- | 8186 - 2491 = 5695 | -7344 | payable |
| t -> b + W+ | 337 711 - 8186 = 329 525 | +7344 | payable |
| u -> d + W+ | 4 - 9 = -5 | +7344 | REFUSED: the body would gain content, which no `become` does |

So the law's free u does not decay to d (as nature's free proton does
not decay), and the neutron's beta decay at the quark level is `d`'s
row: `"become": {"at": A, "into": "u", "products": [["beta", 1, 5],
["nu", 1, 0]]}` with the beta's whole charge -7344 under D-1, or through
a W of `lifetime` 1 as in `weak/w_exchange.json`. The generations are a
chain ordered by content (t -> b -> c -> s -> u, d -> u); nature's mixing
matrix has no key (`into` is one declared family), stated as a limit.

The rows in the world file's form (the run's `u`, `d` and `glue`; the
generator `make_worlds.py`):

```json
"families": [
  {"name": "u", "quantum": 0, "charge": 1224, "phase": false},
  {"name": "d", "quantum": 0, "charge": -272, "phase": false},
  {"name": "glue", "quantum": 0, "columns": {"strong": {"value": 10000, "sign": -1}},
   "lifetime": 3, "phase": false}
],
"measured": [
  {"position": [9, 10, 10], "family": "u", "amount": 4, "held": {"glue": 1}, "fixed": false},
  {"position": [10, 10, 10], "family": "d", "amount": 9, "held": {"glue": 1}, "fixed": false},
  {"position": [11, 10, 10], "family": "u", "amount": 4, "held": {"glue": 1}, "fixed": false}
]
```

### 1.3 What the parser refuses, and one limit found

- **The six flavours in one world are refused** by the fraction-free
  law's column scale (note 41 (iv)): Lambda, the least common multiple of
  the rho denominators of a column's families, must stay within 2^31 -
  1. With the counts above (numbers 1): u + d Lambda 1; with s 61; with c
  151 951; with b 621 935 443 (admitted); with t 2.1 x 10^14, REFUSED at
  load. The five lightest share a world; the top's world is its own (t,
  b, the W). This is a property of the register's grain (one electron)
  and of the counts, not of the law's form: another grain gives other
  denominators.
- `u -> d + W+` is refused (the table above), a statement the law makes
  by itself.
- A `lifetime` on `u` or `d` would cut the charge's rays: refused by the
  design, not by the parser (it is lawful and wrong).

### 1.4 Every key, INPUT or DERIVED

INPUT: the six contents in units (PDG over m_e), the six whole charges
(nature's thirds), the strong value sigma of `glue` and its lifetime L,
the held glue per body, `at` of every decay, the hand and the axis, the
world's width S. DERIVED: rho per unit as the quotient, R of every
transformation as the difference of contents, the binding condition and
every push of section 4 from the coupling formula, the set's charges as
the rational sums (section 3), the group on the three events from the
48 (section 3), the step regime from the drive rule. Nothing of the
engine is added: the rows use `name`, `quantum`, `charge`, `columns`,
`lifetime`, `phase`, `held`, `become`, `hand` and `axis` as
`world.py` accepts them today (the family keys `FAMILY_KEYS`, the
measured keys `MEASURED_KEYS`, `BECOME_KEYS`), and the engine branches on
no name.

### 1.5 The smallest mass by kind (records 243 and 256), confronted

The owner asks whether the electron and the quark are each the smallest
of their kind and whether the law's conditions reach their masses. The
Boss's candidate (record 256): a body's charge is rho x content, so the
smallest content carrying a whole charge is rho's denominator; the
electron with `[1, 1]` one unit, a u quark with `[2, 3]` three units, a
d quark with `[-1, 3]` three units, the proton u u d nine units. Checked
in the law's own charge units:

- **The arithmetic.** `[2, 3]` is a charge PER UNIT OF CONTENT. A u body
  of three units at rho `[2, 3]` carries the whole charge 2 e, not 2/3 e;
  its set u u d would carry 2 + 2 - 1 = 3 e, three times the proton's.
  For the u to carry 2/3 e its rho is `[2, 3 M_u]`, and the denominator
  rule then reads M_u = 3 M_u: it fixes nothing. The candidate holds only
  if "the whole charge" is read at the grain of a third (e/3 the charge
  unit, the u carrying 2 grains, the d 1, the electron 3): then "a whole
  charge per unit of content" (rho in whole grains) gives M_d | 1, M_u |
  2, M_e | 3, that is **M_d = 1, M_u in {1, 2}, M_e in {1, 3}**: the d
  quark the unit of content and the electron heavier than the d. Against
  PDG the d is 9.2 electrons and the u 4.2: FAILS by a factor 9 and
  reverses the order. The other reading, M as the smallest content whose
  charge is whole in e (the denominator of rho written with the whole
  charge over the content), gives **M_e = 1, M_u = 3, M_d = 3**, so m_u =
  m_d = 3 m_e and the proton 9 units: against PDG's 4.2, 9.2 and 1836 it
  FAILS (the u by 1.4, the d by 3, m_u = m_d contradicting the
  neutron-proton difference, the proton by 200).
- **What the law says.** No condition of the law selects a content
  (PREDICTIONS 26; record 106): rho and M are two free keys and the
  charge line reads their product as a pair. The charge's grain (e/3, a
  winding) is quantised and the content's scale is not; the candidates
  above are conditions ADDED to the law that tie the two, and both are
  refuted by the measured ratios. What the law does fix: the minimal
  mass is one unit (record 243), so the smallest body by kind is any
  family of content 1, and at the register's grain that is the electron,
  not the quark (the u is four units, the d nine).
- **The read mass of the bound triple of nine units under binding-v1**
  (the Boss's question): the sum, 9, exactly; binding-v1's give at the
  contact (note 40) moves paid content OUT of a body at its first
  contact, so a triple that holds a paid family reads LESS than 9 by
  what it gave (as the register's deuteron reads 3673 of 3677), and
  nothing reads more. The proton's 1836 is not reachable from 9 (nor
  from the design's 20) by any rule of the law (section 4.3).
- The derivation mathematician writes the same question as section 16
  (2) of DERIVATIONS_BEAM.md (the trigger of record 239 with the minimal
  mass as the first candidate); the integers above (4, 9, 183, 2491,
  8186, 337 711 units; the two candidates' 1, 2, 3 and 1, 3, 3) are the
  ones that section must reproduce or refute, and this file cites it
  once it lands.

### 1.6 The rows and the paper

The family table's quark rows (1.2 with their `become` entries) may go
into the paper at the paper-writer's decision (record 251: "the tables
can also go into the paper"); the paper states them as inputs, with
section 4's pins as what the run decides.

## 2. What the law lacks for confinement and what it has

### 2.1 What it has: the strong column, the contact and the lifetime hold three events in a line

The push between two bodies within the reach is the law's one coupling
(BEAM_LAW step 4; note 31): per axis, `(Q_A Q_B - G_A G_B - M_A M_B) x
U(r)` per unit per direction, with Q the whole electric charge of a body
(rho x M), G its whole strong charge (sigma x the glue held), M its
content, and U(r) the delivery, the sum of the unit labels of the fan's
lines that arrive at the Node r within the lifetime (the register's 290
fan: U(1) = 3008 on the x axis, 57 lines). The quark bodies of the run's
worlds (numbers 2): u with M 5 (4 + 1 glue), Q 4896, G 10000; d with M
10, Q -2448, G 10000. **The pair table at one Link** (the push on the
reader per interval, a negative x toward the emitter):

| Pair | Electric and gravity alone (sigma 0) | With sigma 10000 | Of which the glue rows |
| --- | --- | --- | --- |
| u u | +72 104 139 328 (repulsion) | -228 695 860 672 | -300 800 015 040 |
| u d | -36 052 257 664 (attraction) | -336 852 257 664 | -300 800 015 040 |
| d d | +18 025 752 832 (repulsion) | -282 774 247 168 | -300 800 030 080 |

At two Links on the axis (U 1048 at L = 3): u u -79 678 611 032, u d
-117 360 759 984, d d -98 519 751 008; at three Links, beyond the reach,
the electric and gravity alone: u u +7 574 771 536, u d -3 787 403 148,
d d +1 893 666 024. **The binding condition of a pair at one Link is
G_A G_B + M_A M_B > Q_A Q_B** (the sign of the push): u d binds
electrically already (any sigma); u u needs sigma above 4895 (the least
whole value 4896 = |Q_u|, the gravity 25 negligible), d d above 2447
(2448). The register's 10000 binds every pair, G^2 / Q_u^2 = 4.17 (the
nucleons' 1.85).

**The shapes** (numbers 3; at L = 3, sigma 10000, the width S = 2^37 of
section 4.1). A nucleon is three bodies at adjacent Nodes; on the cubic
lattice three Nodes are never mutually adjacent, so the shapes are the
line (the odd quark in the middle or at an end), the corner (the three
bonds 1, 1, sqrt 2, all within L = 3), and the equilateral triangle of
the face-diagonal sublattice ({(1, 1, 0), (0, 1, 1), (1, 0, 1)}, mutual
sqrt 2, the shape whose stabiliser in the 48 is S_3, section 3.2). The
push on every body and the strong design's toy (the fan's steady
delivery at the current separations, the step drive per axis, the
contact through the table under `measure`, 3000 intervals):

| Shape | The push per body per interval | Inward on every body | The toy over 3000 intervals |
| --- | --- | --- | --- |
| proton line u d u | the ends +-416 530 868 696 on x (electric alone +-10 930 868 696), the middle 0 | yes (electric alone: yes) | holds: no step, 412 hand-overs, the largest 6 664 493 899 136, the label 0 after each |
| proton line u u d | u0 +346 056 620 656 (electric alone -59 543 379 344, outward), u1 +108 156 396 992, d2 -454 213 017 648 | no (the middle u is pushed toward d) | holds: no step, 419 hand-overs (the middle's push handed to d and returned by d's pull) |
| proton corner u d u (d at the corner) | inward on both axes | yes (electric alone: no) | disperses: the first step at tick 34 (u0), 659 steps, the spread 439 Links |
| proton corner d u u | inward on both axes | yes (electric alone: no) | disperses: the first step at tick 30, the spread 547 |
| proton triangle u u d | inward on all three axes | yes (electric alone: no) | disperses: the first step at tick 25 (u1), 608 steps, the spread 317 |
| neutron line d u d | the ends +-435 372 008 672 (electric alone +-29 772 008 672) | yes (electric alone: yes) | holds: no step, 319 hand-overs, the largest 9 142 812 182 112 |
| neutron line d d u | d0 +400 135 007 152, d1 +54 078 010 496, u2 -454 213 017 648 | no | holds: no step, 364 hand-overs |
| neutron corner, neutron triangle | inward | yes | disperse: the first steps at ticks 43 and 25 |

Why the line and not the corner: a set holds under the contact rule when
every inward step of every body lands on an occupied Node; in a line the
ends' pushes point at the middle and the middle's net push is 0 (or is
handed over), while in a corner or a triangle a body pulled diagonally
steps on one axis onto an EMPTY Node and the shape shears, exactly as
series I's alpha square sheared and its line held (the register: "the
model's alpha is the line, not the square"). **So the law's nucleon of
three quark bodies is a line, two Links end to end; the strong column
alone holds it, and even the electric column alone holds the symmetric
lines u d u and d u d.** The engine's smoke test reads the designed
pushes exactly (section 4.6).

One more thing the law has: an isospin-like asymmetry for nothing. Per
unit of charge squared u u repels by 4/9, u d attracts by 2/9, d d
repels by 1/9, so the u d u line binds more tightly at its ends than a
neutral pair would; the neutron's d u d ends read 435 372 008 672 against
the proton's 416 530 868 696 (numbers 3).

### 2.2 What it lacks: growth with distance, and any bar to a free quark

- **The bond is a square well, not a string.** Within the reach the push
  falls as the delivery U(r) (3008, 1048, 0 at one, two and three Links on
  the axis; a 1 / r^2 with a cut), and beyond L the strong rays have
  clicked on the border `lifetime` and nothing remains but the electric
  residual. HYPOTHESES 13's growth with distance (the content held
  between two quarks rising with their separation) has no counterpart:
  no rule lets a ray in transit read another ray (two paid units at one
  Node "read the same V and never each other", step 3), and the merge
  adds rows of one record, it never multiplies two rows (the click's
  square, CLICK_SQUARE: "the law has no product between rows").
- **A kicked quark leaves as a free fractional charge** (numbers 3, the
  kicked line; the world `q6_proton_kick`): the end u of the line kicked
  outward by 10^12 label units is turned back within three intervals (the
  ends' pushes are 4 x 10^11 per interval), and kicked by 10^13 it steps
  at tick 7 in the toy (tick 6 on the engine), then every seven
  intervals, is beyond the reach at three Links where only the electric
  residual -3.8 x 10^9 reads, and is beyond nine Links (series I's face)
  at tick 78 of the toy: a body of charge +2/3 e alone on the GameBoard,
  which nature never shows. The law does not confine; it binds.
- **Confinement in the detector's world** (the catalog's row): a set
  covering the three reads the exact rational sum of their charges, 2/3
  + 2/3 - 1/3 = 1 and 2/3 - 1/3 - 1/3 = 0 (section 3.1), and the far
  field of the triple is the field of one body of the summed charge (the
  fans add); a detector of width 1 at a quark's Node resolves the quark
  (its own rho, its own fan). Whether a quark is "seen" is a statement of
  the detector's width, not of the law: the law forbids nothing.
- **The flight table's tie.** A direction's first step is along the axis
  furthest behind, ties in axis order (x first), so the six neighbours
  are not equivalent at one Link: U(1) is 3008 on x (57 lines), 2598 on
  y (47) and 2336 on z (41) (numbers 2). A line along x is the tightest
  orientation; the run's worlds lie on x and the spread over the 48
  orientations is a known limit of the register (the catalog: "no spread
  across the 48 orientations").

### 2.3 Colour: what it would be in the law, and the three tests

**Colour as a label.** Three values that sum to nothing is the group
Z_3 (the cyclic group of three), and the law carries such a thing
already: a phase circle of N steps on a family, the group ring Z[Z_N]
on a record, and the click's evaluation at the character (the two-slit
design: the click is the evaluation of the record's group-ring element
at zeta_N, the N-th root of unity). A colour would be **a second circle
per family with N_c = 3**, the family key `colour` in {0, 1, 2}, a
colour-neutral set the one whose three colours evaluate to 1 + omega +
omega^2 = 0 at the non-trivial character (omega the cube root of unity).
It cannot sit on the world's circle: N = 64 is not divisible by 3. The
three tests on the label: generic PASS (one circle with declared
integers, the same for every family, 0 for a family without colour, no
branch on a name); vector PASS (the group-ring addition over the set and
the evaluation at the click, two of the six verbs); local PASS as a
reading of a detector set (a set is one record; a nucleon's three Nodes
are within one reader's six neighbours only for a line's middle). So a
colour label is admissible today as a key and a reading; **it does
nothing**: a reading reads, and no rule of the law acts on a reading.

**Colour as a force: the candidate rule, in vector form.** HYPOTHESES
13's mechanism is the glue rays binding to each other. Its generic
vector form: at every Node, for every pair of glue rows in transit
(their label vectors **v** and **v'**, integer 3-vectors at the label's
scale), a bilinear form **v**^T **C** **v'** with a declared integer
matrix **C** per family turns each row toward the other by its phase
register (the meeting's verb on a paid unit reading the free crowd, note
35, applied between two rows), so that the field between two quarks
closes into a string instead of spreading, and a string's content held
between them grows with their separation. The three tests:

1. **Generic**: PASS. One matrix with declared integers per family, no
   name or kind; a family without it has **C** = 0.
2. **Vector**: FAIL. The six verbs act on one row's accumulator or add
   rows of one record; a product between two rows in transit is a
   seventh verb, the one the click's square refused on 2026-09-21
   (CLICK_SQUARE: "the merge adds only identical rows, the law has no
   product between rows").
3. **Local**: FAIL for the string. Two rows at one Node read each other
   locally, but a string is content held on a path of Nodes between two
   bodies, "nothing kept at a Node" (record 202's third test; the
   engine keeps nothing at a Node beyond the events there).

**The verdict of section 2.** No colour is NEEDED for the convergence:
the strong column sigma with the contact rule and the lifetime holds
three events at adjacent Nodes in a line (2.1). A colour label is
admissible and idle; a colour force fails two of the three tests and is
stated as the hypothesis **colour-v1** under its own identity, not
built: the label `colour` in Z_3 and the row-to-row matrix **C**, its
pins the string's content against the separation, the range of a second
triple, and a lone quark's count (HYPOTHESES 13's three outcomes). Its
statistics is a further gap: the law's line carries Z_2 on its three
events (section 3.2), not the S_3 a colour singlet is antisymmetric
under; only the triangle carries S_3, and the triangle disperses under
sigma alone.

## 3. The group

### 3.1 Which structure of the law the quarks are

The owner asks that the quarks enter "as a group or a set or a vector".
Each word is one structure the law has, and the quarks use all three at
their own level:

- **A family's rows on the group ring.** A quark's FIELD is the rows of
  its family, born at its self-creations on the fan, one row per
  direction of amount M (its content) for `u`, `d`, and one of amount 1
  for `glue`: a free family's rows, read for gravity, electricity and
  the strong column, carrying no content. A row's record is the state
  vector **s** on the torus (the vector-form document); for the run's
  phase-less rows it is the amounts alone.
- **A measured event, a set of Nodes with one record.** A quark's BODY is
  a measured event on one Node (`span` `[1, 1, 1]`), the external thing
  of the catalog; its record holds its content, its charges per column
  as pairs, its momentum vector **p**, its drive and its counts.
- **A bound set of measured events.** A NUCLEON is three bodies at
  adjacent Nodes, three records, bound by the strong column with the
  contact rule; a detector whose set covers the three reads it as one
  record (a click says "here, in one of these"). Its state vector per
  column is the exact rational sum over its members, **q**(S) = sum over
  i in S of **q**(i) with **q** = (content, charge, strong) (numbers 6):
  the proton u u d (20, 7344/1, 30000/1), the neutron u d d (25, 0/1,
  30000/1); the register's rows are (1837, 7344/1, 10000/1) and (1840,
  0/1, 10000/1). **The charge composes exactly** (the fans add: an
  electron at r = 8 reads the integer charge's push); the content and the
  strong charge compose to the declared sums, not to the register's
  rows, unless the glue is declared to make them (section 4.3).
- **The transformation's group action.** `become` maps the family index
  of a body (d -> u with the W's charge and the content R = M_d - M_u):
  the weak force acts on the flavour label as a transposition within the
  pair (u, d) of a generation, and across the generations as the chain
  t -> b -> c -> s -> u ordered by content (1.2). It is the one rule that
  changes a row's index; the charge line is its invariant.

**The tower.** The law composes bound sets in a tower: quark bodies into
a nucleon (this design), nucleons into a nucleus (series I), nuclei and
electrons into an atom (series H), bodies into a star (the catalog's
neutron star). At every level the structure is the same triple: (i) a
set of events at Nodes within the reach of the level's binding column
(the strong column with L for the nucleon and the nucleus, the electric
column for the atom, gravity for the star); (ii) the set's state as the
group-ring sum of its members per column, the map **q** a homomorphism
from the free abelian monoid on the family rows to the rationals per
column, associative and commutative, so that a set of sets is a set and
the level is not a property of the algebra; (iii) the contact rule
between the level's members and the detector's set that reads the level
as one record. This is the owner's "a group underneath also works out":
the algebra is level-free, and the run of the tower's next level (the
deuteron of two triples, section 4.5) is the check that the strong
residual between two lines binds them as series I's nucleons bind.

**What is not level-free is the mass.** The set's content is the sum of
its members' at every level, and nature's is not at the nucleon: the
proton's 1836 units are 1 % its quarks' and 99 % the binding. The law's
tower reproduces the charges up and the contents up as sums; the
nucleon's content of the register (1837) is then not the sum of its
quark rows (20) but a declared row, unless the difference is declared as
glue held (4.3). The two ways to say it: the nucleon is a family (the
register today, the owner's decision of 2026-09-20) or a set of three
quark families with 1819 units of glue declared among them; the law does
not choose, since no rule of it adds content to a bound set.

### 3.2 Which group the three colours would be, and who carries it

If colour is admitted, its group is **Z_3** as a label (the cyclic
relabelling of the three values, the circle of section 2.3) and **S_3**
as the permutations of the three events (the Weyl group of nature's
SU(3), which permutes the three colour weights; a colour singlet is the
sign representation of S_3, antisymmetric). Who carries it on the
GameBoard (numbers 6, by enumeration of the 48 signed axis
permutations):

| Carrier | What it acts on | Does it carry S_3 on three events? |
| --- | --- | --- |
| the cube's group of 48 on a line (the stabiliser 16 of 48) | the shape | no: the induced permutations of the three events are the identity and the swap of the ends, **Z_2** (the middle is fixed) |
| the 48 on a corner (the stabiliser 4 of 48) | the shape | no: **Z_2** |
| the 48 on the equilateral triangle {(1, 1, 0), (0, 1, 1), (1, 0, 1)} (the stabiliser 6 of 48: the three-fold turn about the body diagonal and the three reflections that swap two axes) | the shape | **yes, S_3**, all six permutations |
| the collision table's classes (the cyclic shift on the slot states) | rays in the eight slots at a Node | no: it acts on rays, never on bodies (a measured event is outside the table) |
| the world's phase circle Z_N | a row's phase | a Z_3 only if 3 divides N; N = 64: no |
| a colour circle N_c = 3 (a new key) | a family's label | Z_3 as a label, S_3 as the permutations of the set's members |

So the geometric carrier of a colour action is the triangle of the
face-diagonal sublattice, reached at L >= 2 (the face diagonals arrive
at the age 2), and it is the one shape of three that disperses under
sigma alone (2.1): a colour force would have to hold what the strong
column does not. The 48 carry the shape's symmetry, never an internal
label; the label needs its circle.

### 3.3 The bottom of the tower: is a level below the quark possible?

The law's floor is the unit of content: a body's `amount` is an integer
from 1, and the minimal mass is one unit (record 243). Two orders answer
the owner's "the last group from below":

- **By composition** the quark is the last group from below in the
  register's tower (nothing composes it), and the law neither forbids
  nor selects a level beneath: a u of four units is, in the algebra, the
  sum of four bodies of one unit, but a set holds only by a column, and
  no column is declared that binds four one-unit bodies into a u and
  nine into a d. Such a level would be a family of content 1 with its
  own column and range, one more row of the same table; the algebra of
  3.1 works at that level as at every other. The law does not decide
  whether it exists (PREDICTIONS 26), and no reading of the register
  bears on it.
- **By mass** the bottom is the electron, not the quark: at the
  register's grain the electron is one unit and the quarks are four and
  nine (PDG: m_u / m_e = 4.23, m_d / m_e = 9.20). The quark cannot be
  the family of content one unless the electron is a fraction of a
  unit, which the law refuses (a content is a whole number of units).
  The finer-unit reading of record 243 (the unit below the electron, so
  that 1836.15267 and 4.2270 are both whole counts) is section 16 (2)'s
  question, and the answer changes every row's count and none of this
  design's forms.

## 4. Convergence: the expectation pinned before any run

### 4.1 The formulas the pins come from

- **The push** (BEAM_LAW step 4, note 31; `nature_beam.push_form`): per
  axis and per column, epsilon_c x sign(V E_c n_c) x by_clock(age_A,
  |V E_c n_c|, D_c d_c), the gravity exact; for two bodies at rest
  within the reach with `release` [1, 1] this is `(Q_A Q_B - G_A G_B -
  M_A M_B) x U(r)` (2.1). The engine counts it on the fraction-free
  accumulator `acc_push` (note 41 (iv)) and differs from the floor by at
  most one label unit per column, axis and interval where a charge is
  not whole (the dressed world's d, whose G is the pair 3 035 000 / 303).
- **The binding condition** of a pair at one Link: G_A G_B + M_A M_B >
  Q_A Q_B (2.1).
- **The delivery** U(r) from the flight table with the lifetime's cut
  (`quark_numbers.py`, the class `Fan`, the same table the engine walks).
- **The step regime** (BEAM_LAW step 5, the drive): a body of content M
  steps one Link when its drive reaches W = 64 S M + |p| (64 the label's
  scale, S the world's width, p the momentum's component); under a
  constant push F per interval the drive is F t (t + 1) / 2, so the
  first attempt is at about sqrt(2 W / F) intervals. The quark worlds
  take **S = 2^37** so that W on a u body (M 5) is 4.4 x 10^13, the
  register's regime (series I: 64 x 2^28 x 1837 = 3.2 x 10^13 on a
  nucleon): the first attempt at 16.2 intervals for u, 22.9 for d
  (numbers 6); the dressed world S = 2^30 (M 610: 4.2 x 10^13, 15.8).
- **The contact** (note 31 (ix)): the refused step hands the momentum
  component to the occupant, the body's 0 after, the sum unchanged, each
  label bounded by one inter-attempt accumulation (about F x 16^2 / 2 ~
  5 x 10^13 at most; the toy's largest 6.7 x 10^12 on the proton line).
- **The border** (note 31 (vii)): every glue row clicks on `lifetime` at
  the age 3, 290 rows per glue unit per body per interval from tick 4.
- **The read mass**: the content a detector reads of a bound set is the
  exact sum of its members' (step 4: a `read` moves no content; a free
  row carries none), lowered only by binding-v1's give (note 40).
- **The parser's budget** (note 31 (iii)): every |E n| x 64 x Nodes x
  release within 2^62 - 1 (numbers 6: 7.7 x 10^8 for the charges, 6.4 x
  10^9 for the strong column: within).

### 4.2 From series I's deuteron and alpha to the quark triple

Series I registered the deuteron at one Link holding by the push
310 967 280 640 per interval on each nucleon (the `n` rows 1837 x 1839 x
3008 and the `nuclear` rows (10^8 + 1837) x 3008), no step in 3000
intervals, the labels handed over and 0 after each; the pair at three
Links free (the square well's edge); the alpha square shearing and its
line holding. The same formula on the quark rows gives the u d pair at
one Link 336 852 257 664 (the glue rows 300 800 015 040, the electric
36 052 242 624 attractive, the gravity 15 040), the line's ends
416 530 868 696 (the middle d at one Link 336 852 257 664 inward plus
the far u at two Links 79 678 611 032 inward, the strong pull
outweighing the u u repulsion; numbers 3), and the same verdict by the
same mechanism: the line holds, the non-collinear shapes shear (2.1).
The three quark bodies converge to a bound set as the two nucleons did,
and to the same shape class as the four nucleons did.

### 4.3 The read mass against the sum of the parts

- The law's proton u u d with one glue unit each reads **20 units** (4 +
  4 + 9 + 3), the neutron u d d **25**; nature's 1836.15 and 1838.68: the
  ratio 91.8 (numbers 5). The law's ratio of the read mass to the sum of
  the parts' units is **1 exactly**, from the formula of 4.1 (the read
  mass); nature's proton is 0.96 % quark rest masses and the rest the
  binding (record 248). binding-v1 (record 115) lowers a bound set's
  mass by the paid content given at the contact and never raises it: the
  register's deuteron reads 3673 of 3677. **No rule of the law raises the
  mass of a bound set above its parts**, so the proton's 99 % is not in
  the law: registered as a plain disagreement, not tuned.
- The neutron-proton difference: the law's rows give **5 units** (M_d -
  M_u; the register's nucleon rows 3; nature 2.531 m_e). The
  electromagnetic self-energy nature subtracts has no counterpart (a
  bound set's field costs nothing); a falsifiable row of the paper.
- **The dressed quark** (the world `q7_proton_dressed`; numbers 5): the
  input moved, not derived. Each quark holds the glue that makes the
  set's sum the register's proton: 606, 607, 606 units (the neutron's
  605, 606, 606 sum to 1839 - 22 = 1817), the glue's value declared as
  the pair `[10000, 606]` so that 606 units carry the strong charge
  10000 as one unit at 10000 does (the d's 607 give 10 016.5, the pair
  3 035 000 / 303). The line's ends then read 418 547 308 612 (the
  gravity of 610 units added; the engine's accumulator 418 547 308 613,
  the one unit of 4.1), the toy holds it (437 hand-overs, no step), and
  a detector reads 1836: the glue's share 99.07 % of the mass, declared,
  nature's 99.0 %. This row says only that the binding's share can be
  written as held content; nothing selects 606.

### 4.4 The size of the set in Links

The line is two Links end to end (the ends at 2, each at 1 from the
middle); the reach of the glue at L = 3 covers 1, sqrt 2, sqrt 3 and 2
Links, so every pair of the line is within the reach and a fourth body
at three Links is beyond it. A corner or a triangle is 1, 1, sqrt 2 (all
within the reach at L >= 2) and does not hold.

### 4.5 The deuteron of two triples: the tower's check

Two lines at adjacent Nodes (`q4_deuteron_rectangle`: u d u at y = 10
over d u d at y = 11, the 2 x 3 rectangle; numbers 4): every body's push
is inward (the proton's ends (514 900 489 024, 384 064 524 729), its
middle (0, 486 661 618 356); the neutron's (550 101 777 180,
-402 779 816 516) and (0, -449 231 033 022)); the three pairs across at
one Link on y read 290 938 219 884 each (U_y = 2598, the flight table's
tie); the sum over the proton's three toward the neutron line is
1 254 790 667 814 per interval, 4.0 times series I's 310 967 280 640
between two nucleons (three strong pairs across and the diagonals), and
the neutron's sum differs by 1760 (the third-law gap of the fans on
bodies of unequal content, record 126). The toy DISPERSES the rectangle:
the first step at tick 161 (n_u1), 105 hand-overs before it, the spread
686 Links; the inward diagonal pulls step onto empty Nodes as the alpha
square's did. The collinear deuteron (`q5_deuteron_line`: u d u d u d on
x, the two triples end to end) holds in the toy: no step in 3000
intervals, 954 hand-overs, the largest 13 452 697 595 604; its pushes
419 551 209 892, 101 923 625 280, 3 787 403 148, -3 787 401 568,
-81 931 883 236, -439 542 951 616 on x, the sum over the first triple
toward the second 525 262 238 320 per interval (1.7 times series I's
deuteron). Two lines three Links apart (beyond the reach) read the
electric and gravity residual alone, the proton's three summing to
-12 284 928 740 on y, a weak repulsion. **So the tower composes: the
strong residual between two triples binds them at adjacent Nodes as
series I's nucleons bind, in the collinear shape; a deuteron of two
lines side by side does not hold under sigma alone.** Which of the two
is the model's deuteron of triples is the run's finding; the pins say
the line.

### 4.6 The worlds and the smoke test

The seven worlds (`make_worlds.py`, under `worlds/`; series I's base: an
open cube of 21^3, K 2^20, N 64, `release` [1, 1], `suspension` 0, the
290 fan, 3000 intervals; the model ids `beam-quarks-<name>-space-v1`;
not registered, waiting for the owner's go):

| World | What |
| --- | --- |
| `q1_proton_line` | u d u on x |
| `q2_neutron_line` | d u d on x |
| `q3_proton_triangle` | u u d on the face-diagonal triangle |
| `q4_deuteron_rectangle` | u d u over d u d at one Link |
| `q5_deuteron_line` | u d u d u d on x |
| `q6_proton_kick` | q1 with the end u kicked -x by 10^13 |
| `q7_proton_dressed` | q1 with the glue 606, 607, 606 at `[10000, 606]`, S = 2^30 |

**The smoke test** (the only run made; `tools/run_series.py --ticks 24`
on this worktree at `5f7fc813` with the project's environment, the seven
worlds completed in 1 to 8 s each, the books conserved at every tick,
`hypotheses` `columns-v1`): at tick 20, when every line of the fan
within the reach has arrived and no body has stepped (the register's
reference tick), **the engine's push per interval on every body equals
the script's integer exactly** in q1 to q6 (q1 +-416 530 868 696; q2
+-435 372 008 672; q3 (-46 833 992 744, -55 544 787 168, 126 813 807 239)
on its first body; q4 (514 900 489 024, 384 064 524 729) and the others
of 4.5; q5 the six of 4.5) and to one label unit in q7 (418 547 308 613
against 418 547 308 612); the first hand-overs at ticks 16 to 22 (the
drive's 16.2 and 22.9); no step in q1 to q5 and q7 in 24 intervals; the
border `lifetime` clicking 870 rows per interval from tick 4 for three
bodies (290 x 3) and 1740 for six; in q6 the kicked u steps -x at ticks 6,
13 and 20 (the toy's 7 and every seven) and reads -767 061 952 at tick
24, the residual beyond the reach, its momentum -7.3 x 10^12 outward.
The smoke test confirms the formula's integers and the worlds' parse; it
decides nothing about the shapes (3000 intervals decide).

### 4.7 The pins, before the run

Every reading is a DETECTOR reading (the bodies' `read` and `contact`
records, the border's clicks, a face's record) or a GAMEBOARD reading
(the bodies' steps and separations: the host's view). A reading outside
its pin is reported with its numbers and never moved.

| World | Reading | Expected | Refutes the design if |
| --- | --- | --- | --- |
| q1 | the push per interval at tick 20 on each end, on the middle (DETECTOR) | +-416 530 868 696 on x; 0 | any other integer |
| q1 | steps in 3000 intervals (GAMEBOARD); hand-overs (DETECTOR) | no step; hand-overs from tick 17 every 14 to 20 intervals, about 400 in all, the label 0 after each, the largest about 6.7 x 10^12 | a step of any body; a label growing without bound |
| q1 | the border `lifetime` (DETECTOR) | 870 `glue` rows per interval from tick 4, no `u` or `d` row on the border | any `u` or `d` click on the border |
| q1 | the read mass (the detector's content over the three; DETECTOR) | 20 units, the sum, at every tick | anything but 20 |
| q2 | the push on each end; steps; hand-overs | +-435 372 008 672; no step; hand-overs from tick 22 | a step |
| q3 | the push on each body at tick 20 (DETECTOR) | (-46 833 992 744, -55 544 787 168, 126 813 807 239), (148 740 759 524, -116 576 861 778, -66 677 616 293), (-101 906 766 780, 172 121 648 946, -60 136 190 946) | any other integer |
| q3 | the shape (GAMEBOARD) | disperses: the first step by tick 25 to 60 (the toy's 25 with the steady delivery; the engine's fan arrives over the first ticks), the three beyond three Links of each other within a few hundred intervals, out through the faces | the triangle holding 3000 intervals (then the flight's delay is the named cause and the triangle is registered as held, as series I's rule) |
| q4 | the push per body at tick 20; the sum over each triple | as 4.5; 1 254 790 667 814 and -1 254 790 666 054 on y | any other integer |
| q4 | the shape (GAMEBOARD) | disperses: the first step at about tick 160 (the toy's 161), later than every three-body shape; the two lines separate | the rectangle holding 3000 intervals |
| q5 | the six pushes; the sum over a triple; steps | as 4.5; +-525 262 238 320; no step in 3000 intervals, about 950 hand-overs | a step |
| q6 | the kicked u's steps (GAMEBOARD); its push (DETECTOR); the face (DETECTOR) | steps -x at tick 6 and every seven intervals; its push falling to the electric residual (-3.8 x 10^9 at three Links, below 10^9 beyond); it leaves through `face:-x` at about tick 70 to 90 (the toy's 78 at nine Links) with its momentum and its charge 2/3 e; the other two stay a pair (d u at one Link, bound electrically and by the glue) | the kicked u returning; the pair d u separating |
| q7 | the push on each end at tick 20; the read mass | 418 547 308 612 or 613 (the accumulator's unit); 1836 at every tick | a read mass other than 1836; a step |
| all | the books | initial = current + spent + escaped per family at every tick; the momentum line closed through every hand-over | any imbalance |

**What refutes the design as a whole:** a line that does not hold (then
the contact rule's bound or the delivery is wrong and the strong design's
verdict on the alpha line is in question too); a triangle that holds
(then the toy's shear is an artefact of the steady delivery and the
colour carrier is a live shape); a read mass that differs from the sum
(then a rule moves content that the law text does not name).

## 5. What converges and what does not: the verdict

1. **Carried as they are by the generic law:** the six quarks as rows
   with the keys the table has (`charge` as a rational pair per unit of
   content, the content in units, a held unit of a strong family with
   its sigma and its lifetime, `become` with the hand for the flavour
   changes), the engine branching on no name; the rows u, d, s, c, b in
   one world, the top in its own (the fraction-free scale).
2. **Converges (pinned):** three quark bodies at adjacent Nodes under
   the strong column sigma alone, the contact rule and the lifetime, in
   a LINE that holds (u d u, d u d), the engine's first pushes equal to
   the formula's integers; the tower's next level, two triples end to
   end, holds too; the corner, the triangle and the side-by-side
   rectangle shear and disperse.
3. **Does not converge and cannot in this law:** the proton's mass. The
   bound set reads the exact sum of its parts (20 units against 1836,
   the ratio 91.8), no rule raises a bound set's content; the 99 %
   binding of nature is writable only as glue held by declaration (606
   units per quark), an input moved, not derived; the neutron-proton
   difference 5 units against nature's 2.53.
4. **Needs a rule the law lacks, named as a hypothesis:** confinement
   (the growth with distance, no free quark): **colour-v1**, a Z_3 label
   with a row-to-row matrix **C**, which fails the vector test (a
   product between rows, a seventh verb) and the local test (a string is
   content kept between Nodes); a colour label alone passes the three
   tests and does nothing. The law binds and does not confine: a kicked
   quark leaves as a free fractional charge.
5. **Inputs:** the masses in units (PDG over m_e: 4, 9, 183, 2491, 8186,
   337 711) and the whole charges (nature's thirds), sigma and L, the
   glue held, `at` of the top's decay; the smallest mass by kind is not
   reachable from the law's conditions (the two candidates of record
   256 fail against PDG), the minimal mass is one unit and at the
   register's grain the electron is the bottom, the quark the last group
   from below by composition only.
6. **What the run would decide:** whether the line holds 3000 intervals
   on the engine as in the toy (the design stands), whether the triangle
   holds (the colour carrier is a live shape), which deuteron of triples
   the model has (the line of six or the rectangle), the free quark's
   exit, and the dressed row's identity with q1's binding; never the
   mass, which is the sum by theorem.

### The formulas of this design, for CODE_TO_FORMULAS.md's section 6 (what, when, how)

| What | When | How reached | Where it lives |
| --- | --- | --- | --- |
| rho_q = (thirds of e) / M_q as a reduced pair: the quark's charge per unit of content (1.2) | 2026-09-21, this design | from the law's definition of rho (BEAM_LAW section 2, note 28) and PDG's counts at the register's grain | numbers 1; the rows of `make_worlds.py` |
| R = M_from - M_into: the content a W or a beta carries at a flavour change (1.2) | 2026-09-21 | from the charge balance of `become` (note 36 (iii)), the whole charges being the rows' | numbers 1; the register's neutron (3 = 1839 - 1836) as the check |
| Lambda = lcm of the rho denominators within 2^31 - 1: which flavours share a world (1.3) | 2026-09-21 | from the fraction-free column scale (note 41 (iv), `world.column_scales`) | numbers 1 |
| G_A G_B + M_A M_B > Q_A Q_B: a pair binds at one Link (2.1); the least sigma 4896 (u u), 2448 (d d), 0 (u d) | the form 2026-09-20 (the strong design 3.2); the quark values 2026-09-21 | the sign of the one coupling on two bodies at rest within the reach | numbers 2 |
| the push of a shape per body: `(Q_A Q_B - G_A G_B - M_A M_B) x U(r)` summed over the members, U from the flight table with the cut (2.1, 4.5) | 2026-09-21 | BEAM_LAW step 4 with the lifetime; verified on the engine at tick 20 to the unit | numbers 3 and 4; the smoke test |
| "a set holds when every inward step lands on an occupied Node": the line holds, the corner and the triangle shear (2.1) | the mechanism 2026-09-20 (series I's square and line); the statement 2026-09-21 | the step drive per axis with the contact rule, in the toy | numbers 3 |
| the read mass of a bound set M(S) = sum of M_i, the ratio to the parts 1 (4.3) | 2026-09-21 | step 4 (a `read` moves no content) and note 40 (the give lowers only) | numbers 5 |
| the first attempt at a step at about sqrt(2 x 64 S M / F) intervals (4.1) | the arithmetic 2026-09-20 (the binding design's "about tick 16"); the form 2026-09-21 | the drive rule (step 5) under a constant push | numbers 6; the smoke test's ticks 16 to 22 |
| **q**(S) = sum over the members of **q**(i): the set's charges as the exact rational sum, a homomorphism level by level (3.1) | 2026-09-21 | note 31 (i)'s `rational_sum` over the held families, extended to a set of events | numbers 6 |
| the stabiliser of a shape in the 48 and the group it induces on three events: Z_2 for a line and a corner, S_3 for the face-diagonal triangle (3.2) | 2026-09-21 | enumeration of the 48 signed axis permutations | numbers 6 |
| the colour label as a circle N_c = 3 with the neutral reading 1 + omega + omega^2 = 0; the colour force as **v**^T **C** **v'** between rows, a seventh verb (2.3) | 2026-09-21 | the group-ring form of the click (the two-slit design) and the three tests | this file; colour-v1 not built |

Not checked on the engine: the 3000-interval fates (the toy stands in);
the kicked quark's exit tick; the dressed world's hand-over count; any
orientation but x for a line and y for the stacked pair.
