# The continuum limit: what a scaling theory would have to state, which pieces exist, which are missing, and whether the paper can stand on the conditional statements (the open-problems physicist, read-only, 2026-09-21)

Problem (7) of the seven (record 393 of the log of 2026-09-20, on the
Boss's branch at the time of writing): "the continuum limit (the wave
equation, Lorentz covariance, hydrodynamics) is unproved; a scaling
theory nobody has". And the owner's question of 14:23Z (record 396,
translated): "Conditional, not derived: the wave limit and Lorentz, the
field equation beyond the static case, `1 / r^2`. Do we need to derive
them, or is what we have enough?" Read against `main` at be194aca:
DERIVATIONS 2 (c and the Doppler), 3.2 (the shell mean), 4.1 (the rows'
wave equation), 5.1 (the retarded field equation), 6.2 (Born as a
limit), 21.5 (the six-point standard), 25.4 and 25.5 (the continuity
equation and the lattice gas), 25.10 and 26 (the verdicts and the
programs), and the general-formula paper's "Continuum limits: what
returns and what does not". Every number is from
continuum_map.py (`docs/designs/open_problems/continuum/continuum_map.py`, deleted 2026-09-26) beside this note (the flight rule
transcribed, integers, no engine import) and its output
[continuum_map.out](continuum_map.out); no run, nothing registered,
nothing decided. Notation: Q the label's scale, N the circle, P the
fan's bound, q the fan's size, r the distance in Links.

## 0. The verdicts, stated at the top

A scaling theory of the law is a statement, per formula, of four things:
the grain it is a limit in, the order at which the formula holds, the
error term with the grain, and the number pinned before the run (21.5's
six points, (2), (3), (5), (6)). The law has FOUR grains with a limit
each and one more condition that is not a grain:

| The limit | The formula it carries | The rate, measured here or in the tree | Status |
| --- | --- | --- | --- |
| Q -> infinity (the label's scale) | the isotropy of c, `Q abs(D) / T_D -> 1 / sqrt 3` on every direction | the largest departure 7.7e-3 at Q = 64, 9.1e-4 at 256, 6.8e-5 at 4096, 6.0e-6 at 65536: `1 / Q`, one-sided (section A) | **DERIVED**, the rate stated (2.1, 3.5 item 4, NATURE 5a) |
| N -> infinity (the circle) | Born's rule to `1 / (2 N)`, Tsirelson's `2 sqrt 2 - 8 / N`, the uncertainty relation's variance form | the registered S 2.75, 2.8125, 2.828125 (section B); Born's rung within `1 / (2 N)` | **DERIVED**, the rate stated (6.2, the paper's theorem); the tables' `1 / 256` a floor |
| P -> infinity (the fan) | the crowd as a FIELD: the shell means `1 / r^2` and `1 / r` (Poisson, the retarded potential), the push's `G M / r^2`, the gradient across the Ports | a shell is covered while `r < P / 2` and is a comb beyond it: at P = 6, 63 percent of the Nodes at r = 6 lie on a line, 20 percent at r = 12; at P = 12, 100 percent to r = 8, 87 percent at 12 (section C); the shell means' ripple 12 to 20 percent at every P (section D) | **DERIVED as shell means** (3.2, 5.1, series E); **NOT a field at any registered fan** beyond r = 4: the dense-fan condition `P >> r` is stated, its rate (the coverage) measured here for the first time |
| the small-rate, long-wave limit (Chapman-Enskog) | Euler's form on the six-heading gas, the sound speed, the longitudinal viscosity; the continuity equation exact | 25.4 exact; 25.5 second order in u and k with the cube's fourth-rank tensor anisotropic (the HPP obstacle: no shear stress on the headings) | **DERIVED in form** for the longitudinal equations, with the error term; the isotropic Navier-Stokes **NOT REACHED** (needs `fan-collision-v1`, 26.3) |
| not a grain: the many-rows superposition in TRANSIT | the wave equation of the ROWS as a field on the GameBoard | none: a row is never summed with another in flight (record 170; the general-formula paper's "no wave on the GameBoard"); the rows' wave equation is the limit's symmetry (4.1) and the click's reading (7.1, Young), not a field on the Nodes | **CONDITIONAL and stays so**: the wave is at the click; the field equation of the AGE MOMENT is exact (5.1, the retarded wave equation, sourced by the release, linear) |

So the answer to the owner's question, problem by problem: the wave
limit is derived where it lives (the click reads the rows' interference
exactly, 7.1; the age moment obeys the retarded wave equation exactly,
5.1) and conditional where the paper phrases it as a wave on the
GameBoard, which the law does not have and should not claim; Lorentz
covariance is derived for the rows' limit (4.1, the Lorentz note's
section 3) and conditional for the bodies (one declared coupling,
covariant-readings-v1); the field equation beyond the static case IS
derived (5.1: the retarded scalar wave equation, not only Poisson; what
is not reached is Einstein's nonlinearity, 5.5); `1 / r^2` is derived as
a shell mean (3.2) with its ripple, and is a field only where the fan is
dense, a condition the paper should state with its number. **The paper
can stand with the conditional statements, and it stands better with
each conditional row carrying its grain, order and error term** (21.5's
columns (3) and (5), "not stated" on many old rows): that filling is a
task for the derivation mathematician and not a derivation gap; what
nobody has is not a scaling theory but its table, and the table's rows
are in the tree.

## 1. The pins, before any number

- **The standard** (21.5): the six points per formula, the lattice
  gas's precedent (Frisch, Hasslacher and Pomeau 1986: the square
  lattice's fourth-rank tensor is not isotropic, the hexagon's is), the
  lattice field theory's (Wilson 1974: the continuum limit as the
  spacing to zero at fixed physics).
- **The register's rates.** c's anisotropy 7.6e-3 at Q = 64 (NATURE 5a);
  Born within `7.8e-3` at N = 64, `4.9e-4` at 1024 (6.2); series E's
  shell means `k_s r^2 = 41.5` (39.0 to 44.8), `k_a r = 36.1` (33.1 to
  39.2) at P = 6 (5.1); the cone at age 29, 17 Links on the axis and 24
  on the diagonal (record 144).
- **What must not move.** Those integers; the six-point standard.

## 2. The limits on the GameBoard, one at a time

**Q, the pace's grain** (the map's section A). A row on **D** advances
`Q abs(D) / T_D` Links per interval with `T_D = isqrt(3 abs(D)^2 Q^2)`;
isqrt rounds down, so the pace exceeds `1 / sqrt 3` by less than `1 /
T_D` of itself and never falls below it. The largest departure over the
290 directions: 7.7e-3, 9.1e-4, 3.5e-4, 6.8e-5, 6.0e-6 at Q = 64, 256,
1024, 4096, 65536, under the bound `1 / (sqrt 3 Q - 1)` at every Q: the
isotropy of c is a limit in Q at the rate `1 / Q`, one-sided, exact. The
error term of every formula that reads c enters at this order (the
Doppler's `1 -+ v / c`, the transverse light clock's `gamma`, the cone).

**N, the circle** (section B). The rung `b_k = (2 N C_k + T) // (2 T)`
puts every cumulative probability within `1 / (2 N)` of the Born weight;
the CHSH sum's deficit is bounded by `8 / N` plus the tables' term; the
registered 2.75, 2.8125, 2.828125 at 64, 256, 1024 follow. The tables at
`1 / 256` are a second grain with a floor of their own (`2.1e-6` in S).
The uncertainty relation's variance form is a limit in N likewise
(22.1). Born, Tsirelson and Kennard are limits in N at the rate `1 / N`.

**P, the fan** (sections C and D). One source releasing one unit per
direction per interval on the fan of every primitive direction within
Manhattan P: a Node holds a row only if some line passes it. The fraction
of a shell's Nodes on some line: at P = 6 (the register's fan in space),
100 percent at r = 4, 63 at 6, 42 at 8, 20 at 12, 9 at 20; at P = 12,
100 percent to r = 8, 87 at 12, 50 at 20. The crowd is a FIELD (every
Node reads the shell's mean to the ripple) while `r` is below about
`P / 2`, and a COMB beyond it (a Node reads a line or nothing). The
shell MEANS carry the `1 / r^2` and `1 / r` forms at every P within a
ripple of 12 to 20 percent (section D: 0.98 to 0.99 of the continuum's
constant in the mean, 0.81 to 1.14 shell by shell at P = 4, 0.92 to 1.08
at P = 12), which is series E's registered pair. So `1 / r^2` is derived
as a shell mean at every P and as a field only where `P >> r`; every
single-Node reading in the register (a clock on a line, series T; a
beam in the mass's plane, the light-bending note; the orbit's inward
legs, the orbit note) reads the comb, not the field, and the derivations
that read the gradient across the six Ports (covariant-readings-v1's
(ii), optical-v1's identity `V = -(Q / 3) grad A`) hold in the field
regime alone. The dense-fan condition is the one scaling condition of
the law that is not a grain of a table but of the WORLD (the declared
`direction_bound`), and its cost is the fan's size (98, 290, 674, 2114
directions at P = 4, 6, 8, 12).

**The small-rate limit** (25.4, 25.5). The continuity equation is exact
on the books; the six-heading gas's Chapman-Enskog expansion gives
Euler's form to second order in u with the cube's fourth-rank tensor
non-isotropic (no shear stress on the headings, `Pi_ab = 0` off the
diagonal for every distribution), the sound speed and the longitudinal
viscosity closed; the isotropic Navier-Stokes needs a collision on a
fan (`fan-collision-v1`), a program. The error terms are stated there
(`O(u^4)`, `O(k^2)`): the one section of the tree that carries the six
points in full.

**The wave of the rows.** A row in transit is never summed with another
(the merge adds identical rows only; the collision permutes; the flight
is a bijection): there is no field of rows on the Nodes whose
superposition obeys a wave equation. What obeys the wave equation
exactly is the AGE MOMENT (5.1: the retarded Green's function of the
wave operator, sourced by the release, additive over sources), a
reading of the crowd, and what carries the interference is the click
(the record's phase-count vector evaluated at the click, 7.1: Young's
spacing to the Fresnel correction). The rows' "wave equation" of 4.1 is
therefore the symmetry of the limit of the rows' flight (the light cone,
`omega = c k`), and the general-formula paper's own remark says it
plainly: no wave on the GameBoard, and no dispersion in any direction
for that reason. That is not a gap to derive; it is the law's statement,
and the paper's phrasing must not promise a wave on the Nodes.

## 3. What a scaling theory would have to state, in one table

| Formula | The grain(s) | The order | The error term | The pin | In the tree |
| --- | --- | --- | --- | --- | --- |
| c isotropic, the light cone | Q | exact in the limit | `1 / (sqrt 3 Q - 1)`, one-sided | the cone at age 29 (record 144) | 2.1, 3.5, NATURE 5a: stated |
| Lorentz symmetry of the rows' limit | Q (the cone), the fan's angle grain for a body's transverse clock | the symmetry of the limit's equation | the cube's 48 at finite Q; the transverse clock's `gamma` to the accumulator's whole interval (the Lorentz note) | the transverse detector's mean age (the Lorentz note's pin) | 4.1: stated without the error term; the Lorentz note adds it |
| Born, Tsirelson, Kennard | N, the tables' scale | `1 / N` | `1 / (2 N)`, `8 / N`, the tables' `1 / 256` | 176 / 64 etc. | 6.2, 22.1, the paper's theorem: stated |
| Poisson and the retarded field equation | P (the fan), the many-rows mean | exact for the shell means; the field where `P >> r` | the ripple (12 to 20 percent at r = 4 .. 14), the coverage (section C) | series E's 41.5 and 36.1 | 3.2, 5.1: the means stated; the coverage and its rate first measured here |
| `G M / r^2`, the push, the orbit | P, the width S | the shell mean; the fan's Manhattan factor 1.287 on a single body (the orbit note) | the ripple; the factor | series D's period | 3.3, the orbit note: stated in part |
| Euler, the sound speed, the longitudinal viscosity | the rate u, the wave number k | second order in u and k | `O(u^4)`, `O(k^2)`, the cube's tensor | the pulse's front | 25.5: stated in full |
| the isotropic Navier-Stokes, Maxwell-Boltzmann, equipartition | a collision on the fan; elastic contacts | not reached | | | 25.10, 26: programs named |
| Lorentz covariance of the bodies | one declared coupling | exact under covariant-readings-v1 to the grain | `E / c^2` within one unit of the root | the muon's 70 and 124 | 17.6: stated; conditional on the identity |
| the second-order redshift, the perihelion, the bending's space part | the field's self-source; a declared factor | not reached | | | 5.5, 21.4, the light-bending note: named |

Nobody has "a scaling theory" as one document because the rows of this
table sit in nine sections; what the paper needs is the table with its
error column, which 21.2 already has as two columns marked "not stated"
for the old rows. Filling them is bounded work for the derivation
mathematician (the numbers above are most of it), not a derivation
nobody can do.

## 4. The owner's question, answered row by row

- **The wave limit.** Derived where it lives: the age moment's retarded
  wave equation (exact), the click's interference (exact, Young to the
  Fresnel correction), the rows' light cone (exact in the limit, the rate
  `1 / Q`). Conditional only if the paper says "a wave on the GameBoard";
  the paper's own remark says there is none. Enough, with the phrasing
  right.
- **Lorentz.** Derived for the rows' limit; conditional for the bodies
  on one declared coupling (the Lorentz note); the contraction on a
  second (the anisotropy note). Enough as three labelled statuses; not
  derivable further as the law stands, and this note's predecessors say
  why.
- **The field equation beyond the static case.** Derived: 5.1 is the
  retarded scalar wave equation, sourced, linear, exact in the shell
  mean; the static case is its special case, not the other way round.
  What is beyond it is Einstein's nonlinearity and tensor source (5.5),
  which the law does not have and the paper says it does not. Enough.
- **`1 / r^2`.** Derived as the shell mean of the flux at every fan
  (Gauss exact, 3.1); a field where `P >> r`, a comb beyond, with the
  coverage measured (section 2). Enough, with the condition and its
  number stated; the register's single-Node readings are combs and the
  paper should say so where it cites them.

So: nothing on this list needs a derivation the tree lacks; two need a
sentence the tree has and the paper must carry (no wave on the Nodes;
the dense-fan condition with its coverage), and one (the bodies'
Lorentz) needs the labelled identity. The referee's standard is the
conditional theorem labelled so; the law meets it.

## 5. Proposed lines for the documents I do not write

- **DERIVATIONS_BEAM 3.2** (the mathematician): the coverage table of
  section 2 (the fraction of a shell's Nodes on a line at P = 4, 6, 8,
  12) as the statement of the dense-fan condition, `r < P / 2`, with the
  ripple per P; 21.2's columns (3) and (5) for the rows of section 3
  above filled from the numbers here.
- **DERIVATIONS_BEAM 4.1** (the same): the rate `1 / Q` of the cone's
  isotropy as the error term; the transverse light clock's `gamma` to the
  accumulator's whole interval as the finite-Q statement of the symmetry.
- **The paper** (the coordinator): the open problems' item (7) restated:
  "the continuum limit is four limits with a rate each (Q, N, P, the
  rate u) and one statement (no wave on the Nodes); its table is
  DERIVATIONS 21.2's error column; the isotropic hydrodynamics and the
  bodies' Lorentz covariance are the two rows that need an identity"; and
  wherever the paper cites a single-Node reading beside a mass, "at the
  registered fan the crowd is a comb beyond r = 4".
- **HIGHLIGHTS 5.4**: nothing.

## 6. Questions, through the Boss

1. **For the owner (substantive)**: none; the answer to his question is
   section 4, and it costs no run. The one choice is the paper's: to
   carry the conditional rows with their error column, which this note
   recommends.
2. **For the Boss**: the filling of 21.2's error column for the old rows
   is bounded work for the derivation mathematician; the numbers of
   sections A to D are on the table.

## 7. Links

[DERIVATIONS_BEAM 2.1](../../../DERIVATIONS_BEAM.md#21-the-stream-and-the-speed-of-light-on-the-axis),
[3.2](../../../DERIVATIONS_BEAM.md#32-the-far-field-a-beam-does-not-dilute-a-shell-does),
[4.1](../../../DERIVATIONS_BEAM.md#41-the-rows-alone-the-wave-equations-symmetry-returns),
[5.1](../../../DERIVATIONS_BEAM.md#51-the-two-fields-of-one-stream-and-the-equation-they-obey),
[6.2](../../../DERIVATIONS_BEAM.md#62-the-clicks-discrete-cost-the-rung-the-tables-and-the-wheel),
[21.5](../../../DERIVATIONS_BEAM.md#215-the-standard-and-the-new-rows-under-it),
[25.5](../../../DERIVATIONS_BEAM.md#255-the-lattice-gas-limit-of-the-six-heading-collision-eulers-form-the-sound-speed-the-longitudinal-viscosity-and-the-frozen-shear-rows-2-3-4-22),
[26](../../../DERIVATIONS_BEAM.md#26-what-the-paper-wants-and-the-derivation-lacks-the-ten-each-with-its-standing-the-identity-or-program-that-would-reach-it-and-the-pin);
[NATURE](../../../NATURE.md) rows 5a and 2c;
the five notes before this one under docs/designs/open_problems/ (on their branches, PRs #602, #603, #606, #608 and the Born note's);
[the three tests](../../../../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202).

> The scripts of this folder (`continuum_map.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/open_problems/continuum/<script>`).
