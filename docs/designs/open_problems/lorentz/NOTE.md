# Special relativity from the six verbs: what gives gamma, what cannot, and where the bridge is declared (the open-problems physicist, read-only, 2026-09-21)

Problem (2) of the seven (record 393 of the log of 2026-09-20, on the
Boss's branch at the time of writing): "a moving clock is not slowed by
the six verbs; covariant-readings-v1 reproduces the muon's decay as a
reading under a key beside the law; form B's pace `1 / (1 + 0.72 v)` is
not the Lorentz factor; no derivation of gamma from the law's verbs
exists". The order: read record 230's routes A, B and C and DERIVATIONS
12, 12b, 12c, 17 and 18, and say whether any route gives gamma from the
verbs, with a derivation on the GameBoard or a proof that none can. Read
against `main` at be194aca (covariant-readings-v1 built on PR #582, open
at da367405, not merged; form B not on `main`). Every number is from
[lorentz_map.py](lorentz_map.py) beside this note (the flight rule
transcribed from BEAM_LAW section 3, integers, no engine import) and its
output [lorentz_map.out](lorentz_map.out); no run, nothing registered,
nothing decided. Notation as the workflow's rule: gamma the Lorentz
factor `1 / sqrt(1 - beta^2)`, beta the speed over the rows' pace, c the
rows' pace (`c^2 = 1 / 3` Links per interval squared, `c_h = 64 / 110` on
a heading), m = Q S M the mass, **p** the momentum vector, E the energy,
`E_0 = m c^2`; a scalar plain, a vector in bold lowercase.

## 0. The verdicts, stated at the top

| Route (record 230) | What it is | Verdict |
| --- | --- | --- |
| A, the six verbs alone, for a body's own counter (the muon) | the counter is the self-creation count; the rules that gate it are the frame's advance and the crowd's owed count | **NOT REACHABLE, proved** (section 2): the rate is exactly 1 in an empty world and speed-independent in the mean in any isotropic crowd at rest; no declared rule reads the momentum into a count |
| A, the six verbs alone, for a light clock (a row exchanged with a co-moving partner) | the transit of a row across the motion | **REACHED** (section 3): the transverse transit is `gamma` times the rest transit, exactly in the continuum and to the flight table's grain on the lattice, by Pythagoras in the table's integers; along the motion `gamma^2` (the ether clock): the anisotropy of NATURE row 5b, problem (3) |
| B, the seventh verb (lorentz-v1, a root at a declared grain) | `gamma` imposed on the counter by a run-time root | **NOT NEEDED**: the integer root by comparisons (DERIVATIONS 17.6 M3, reviewed) is within the six; route B is covariant-readings-v1 without the seventh verb; the owner replaced it (record 270) |
| C, the reading budget (the crowd's owed count under the crossing rule) | a mover's counter slowed by the rows it meets | **NOT ADMISSIBLE, proved** (12c, restated in section 2): the crossing count's mean through an isotropic crowd at rest is the rest count exactly; what slowing there is follows the crowd's frame with the wrong sign for a body moving with its rows, bounded, and nothing in an empty world |
| covariant-readings-v1 (the proper-time gate on the exact square) | after every self-creation the body owes `by_drive(acc_tau, E / c^2 - m, m)` intervals, `(E / c^2)^2 <= m^2 + 3 p . p < (E / c^2 + 1)^2` by comparisons | **ADMISSIBLE WITH CORRECTIONS** (as the two reviews found it): the FORM of the gate is forced by the cube's 48 once a body's counter reads its own momentum (section 4, a theorem of the six verbs); the COUPLING (that the counter reads **p** at all) is a declaration, and the contraction is not in it (17.6 M4, M5): rows 4a and 4b PASS under it, row 5b stays FAIL |

The answer to the order's question in one sentence: the six verbs give
`gamma` to the rows' clocks (a transverse exchange, section 3) and not to
a body's own counter (section 2); the bridge from the rows' `gamma` to the
body's counter is one declared coupling, the proper-time gate, whose form
the symmetry then forces (section 4); the isotropy of the whole (the
contraction, 5b) needs a second named identity, `source-velocity-v1`,
which nobody has designed.

## 1. The pins, before any number

- **Nature.** A moving clock runs at `1 / gamma`: the muon's lifetime
  2.197 microseconds at rest and 64.4 at `gamma = 29.3` (CERN; Bailey et
  al. 1977, to 2 x 10^-3), Ives and Stilwell's transverse Doppler, GPS.
  The isotropy of a moving laboratory's light clock: the resonator bounds
  at 10^-17 to 10^-18 (NATURE row 5b).
- **The register.** NATURE row 4a: the muon under the law fires its 64th
  turn at tick 64 at every speed (HYPOTHESES 21, series J4 pinned, FAIL by
  the factor 29.33); row 4b: `coasting_none`'s `s_mz2` reads `z = 0.2636`
  at `beta = 0.2674` against `gamma (1 + beta) - 1 = 0.315` (FAIL by
  0.051); row 5b: the frame's anisotropy `beta^2 / 2` (FAIL by eight to
  twelve orders). Under covariant-readings-v1 on PR #582 (measured, not
  merged): `become` at 64, 70 and 124 at rest, `p = 3640` and `12 856`
  (the pins 64, 70.9 +- 1, and 124 by the primitive's own count), the
  face clicks 392, 369, 345 (391, 367, 345 +- 2), `coasting_none` `z =
  0.3674` (0.369 +- 0.003).
- **What must not move.** The law's clock at rate 1 (4.3) as the law's
  registered prediction (record 249's route A, the FAIL row kept);
  every world without the key byte for byte.

## 2. Theorem 1: no rule of the six as declared slows a body's own counter

**On the GameBoard.** A body is a measured event at a Node with its
content M, its momentum **p** and its counts table on its record. Its
clock is the count of its self-creations. What gates a self-creation, by
the crowd audit ([BEAM_LAW note 47](../../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)),
is exactly two rows of that table: the frame's advance (one self-creation
per interval in which nothing is owed, whether or not the body steps:
`engine._frame_all`) and the owed count `by_drive(acc_owed, k n, d)`
with k the count of the OTHER numbers' rows at its Node (the presence,
or under the age word the age moment). The drive reads **p** into a
step; the turn reads the content; the release, the birth and `become`
read the body's own counts; none of them reads **p** into a count, and
the momentum sits on the record unread by every count.

**The proof.** (a) In an empty world k = 0 at every Node, the owed
accumulator never gains, and the self-creation count equals the
interval count at every speed: the rate is 1. This is the register's
J4 pin (64 at every v) and 4.3's statement, now as a consequence of the
audit's table and not of a run. (b) In an isotropic crowd at rest the
count a moving body is charged is the crossing rule's, per direction
**n** of the crowd `1 - sgn(n_e) beta / |n|_1` on the axis e of the
step (DERIVATIONS 2.4, 12c.1), which is odd about 1 under the reflection
`n_e -> -n_e`; an isotropic crowd has as many rows against the step as
with it, so the mean is exactly 1 and the owed count's rate is the
rest rate `1 / (1 + k n / d)` at every speed to the cap (12c.7, on the
sphere and on the registered fan of 290: 1.000000 at three speeds). The
only speed dependence is a dipole in the crowd's frame (faster with the
rows, slower against them, bounded by 2), proportional to the crowd and
absent in an empty world. (c) No other row of the counts table reads
the crowd or the momentum into the gate. So a body's own counter, under
every rule the law declares, runs at the rest rate in the isotropic
mean at every speed. Routes A and C for the muon are closed by this
theorem, not by a number.

**What the theorem does not forbid.** The momentum is on the record, and
a rule reading it into a count is within the six verbs (a bilinear form
on the state, a translation, a comparison); the law does not have such a
rule, and a rule that adds it is an identity beside the law. Whether that
rule is "derived" is section 4's question.

## 3. Theorem 2: the six verbs give `gamma` to a light clock, transversely, by Pythagoras in the flight table

**On the GameBoard** (the map's section A). Two bodies co-moving at v
Links per interval along x, b Links apart across the motion; one
releases a row toward the other. To arrive, the row must fly the
direction **D** = (a, b, 0) with `a / tau_D = v`, `tau_D` its transit;
the flight rule gives that transit as the direction's own age at its
Manhattan length, `tau_D = age_of(S_1)` with `T_D = isqrt(3 |D|^2 Q^2)`,
that is `|D| / c` up to the accumulator's whole interval. The same
partner at rest, b Links away on the heading (0, 1, 0), receives at
`age_of(b) = b / c`. The ratio is

    tau_D / tau_rest = |D| / b = 1 / sqrt(1 - (a / |D|)^2) = gamma(beta),   beta = a / |D| = v / c:

Pythagoras, the root sitting in `T_D` at load (DERIVATIONS 12.3's point,
made concrete direction by direction). On the lattice (the map's table):
(4, 7) 1.167 against `gamma` 1.151 at beta 0.495; (5, 11) 1.105 against
1.098; (3, 10) 1.059 against 1.044; (6, 7) 1.333 against 1.315 at beta
0.650; the short directions carry the accumulator's whole interval ((1,
2): 1.333 against 1.109, a transit of 4 intervals against 3). No rule of
the bodies, no key, no seventh verb: `gamma` is the geometry of the rows'
one pace.

**Along the motion** (section B): a partner d Links ahead is reached in
`d / (c_h - v)` intervals and the return takes `d / (c_h + v)`, the round
trip `gamma^2` times the rest one (1.2264 at v = 1 / 4, 1.0484 at 1 / 8)
where the transverse round trip is `gamma` (1.1074, 1.0239): Lorentz's
ether clock, which Lorentz closed by contracting the arm along the
motion by `1 / gamma`. No verb contracts a Link (12.1, 10.4); the two
arms differ by `gamma`, NATURE row 5b, problem (3).

**A detector reads it** (the map's section C, host arithmetic on the
flight rule, the arrivals only, the in-plane fan): a lamp and a detector
body both thrown at v = 1 / k on x, the detector d Links across, the
rows' ages at their arrivals at the detector's Node (the age moment the
click carries under `reads: age`): at k = 4 (beta 0.43) the mean age over
the rest transit is 1.125 to 1.150 against `gamma` 1.107; at k = 8, 1.04
to 1.06 against 1.024; at k = 16, 1.00 to 1.05 against 1.006. The trend
is `gamma`'s and the lattice reads above it by 0.02 to 0.04 (the rows
that reach a co-moving Node on the digital lines are not the
continuum's cone: the coincidence of the lines' whole Links with the
body's whole steps), so a run pins the map's number and not `gamma`;
the pin below.

**So route A does give `gamma`, for a clock made of rows.** What it does
not give is `gamma` for a clock made of a body's counter (Theorem 1),
nor the same `gamma` along and across (the contraction). The muon of
nature is a counter, not an exchange; DERIVATIONS 10.4's exchange clock
(a self-creation per bond round trip) slows anisotropically and by the
exchange's loss, not by `gamma`.

## 4. Theorem 3: once a counter reads its momentum, the cube forces the form; the coupling itself is the declaration

**On the GameBoard.** Suppose a rule of the six lets a body's counter
read its own **p**. A count is gated by an accumulator against a wall
(the translation and the Euclidean division); a rate at most bilinear in
the state is a bilinear form with a declared matrix, `p^T M p` (verb B);
a clock cannot know the sign of its motion, so the reading is even in
**p**; and a rule of the law commutes with the cube's group of 48 signed
axis permutations (FORM.md section 3, the law's only symmetry at finite
Q). The symmetric integer matrices fixed by all 48 are the multiples of
the identity (the map's section D: of the six-dimensional space of
symmetric matrices, the invariant ones with coefficients in -2 .. 2 are
exactly the five `c I`). So the only isotropic even reading of the
momentum within the six verbs is `c p . p`: the exact square `Xi = m^2 +
3 p . p` of covariant-readings-v1 (17.6 M3), with the 3 the declared
`c^2 = [1, 3]` that makes the pace `p c^2 / E` cap at the rows' `1 /
sqrt 3` (17.6 N2). The gate that follows, `E / c^2` the whole root of Xi
by comparisons and `by_drive(acc_tau, E / c^2 - m, m)` intervals owed
per self-creation, is `1 / gamma` with the relativistic dispersion, no
root at run time. **Derived**: the form. **Declared**: the coupling, that
a counter reads **p**; the six verbs neither give it (Theorem 1) nor
forbid it. The identity is therefore honestly named: a hypothesis whose
one free choice is a yes or no, not a number.

**Form B's pace beside it** (the map's section E): `1 / (1 + 0.72 v)` is
the ratio of form B's drive to today's per-axis drive, a dispersion `v =
p / (m + p / c)` that caps a body at the rows' pace and slows no clock;
`1 / gamma` is a clock's rate; the covariant pace `p c^2 / E` is the
relativistic dispersion (0.229 against 0.295 Links per interval at p /
m = 1 / 4). Three objects; the order's sentence is right and the three
are not to be compared.

**What the identity does not carry, named.** The contraction: the push
under it is `-grad(A)` alone (17.6 M4), which on a co-moving pair gives
the rest force along the motion and `gamma` times it across, not
Lorentz's pair; the magnetic part needs a row to carry its source's
momentum label (`source-velocity-v1`, named in 17.6 M4, not designed).
Until then 5b is the law's FAIL under the identity too, and a bound
system in motion is anisotropic (12b.2: the thrown orbit sheared and
unbound, the transverse and longitudinal masses `m (1 + v / (c - v))`
and its square in place of `gamma m` and `gamma^3 m`).

## 5. What each route gives for NATURE's rows, and what a run reads

| Row | The law (route A, the counter) | covariant-readings-v1 (PR #582, measured once) | a light clock of rows (route A, section 3) |
| --- | --- | --- | --- |
| 4a, the muon in flight | 64 at every speed, FAIL by 29.33 (the registered prediction) | 70 and 124 at `p = 3640` and `12 856` (`gamma` 1.107, 1.956), PASS to the primitive's integer | not a counter: no row |
| 4b, the moving lamp's z | 0.2636, FAIL by 0.051 | 0.3674 against 0.369 +- 0.003, PASS on the declared momentum | the lamp's phase per turn is the counter's: no row |
| 5b, the frame's anisotropy | `gamma` between the arms, FAIL | the same FAIL (no contraction) | `gamma^2` along, `gamma` across: the FAIL's mechanism, exact |
| new: a co-moving transverse detector's age | not a NATURE row today | the same reading (the flight is untouched by the key) | the transverse transit `gamma d / c` to the grain: a PASS of the six verbs on `gamma`, readable |

**The pin for a run that reads `gamma` from the six verbs alone** (no
key, no rule; for the Boss to order or not): a plane bar, a paid lamp of
one unit per interval on the in-plane fan of the 184 primitive
directions within Manhattan 12 and a detector body with a `measure`
entry reading `age`, both thrown at `v = 1 / 4` on x (k = 4, beta 0.43),
the detector 12 Links across; a control at rest. DETECTOR: the mean age
of the detector's clicks over a window after the transient, 22.5 +- 0.5
intervals against the control's 20 (the ratio 1.125; `gamma` 1.107; the
map's own number is the pin, the continuum's `gamma` the comparison,
the 0.02 the lattice's coincidence bias named before the run). At k = 8
and d = 12: 21.2 +- 0.5 against 20. What refutes the reading: a mean age
at the control's within the bracket in the thrown world. The crossing
rule's marks (a row on the body's Link against it) are not in the map's
arrivals-only count and may add rows of small age; the bracket is the
map's.

## 6. The owner's question on the conditional derivations, for this problem

- **Lorentz covariance of the rows**: derived, not conditional (4.1: the
  rows' limit is the wave equation at one c; its symmetry is Lorentz's;
  section 3 here shows `gamma` in the table's integers).
- **`gamma` for a body's clock**: conditional on covariant-readings-v1,
  and the condition is now sharp: one declared coupling, its form
  forced (Theorem 3). What a derivation would take: a mechanism by which
  a body's self-creation is timed by its own rows. The only such
  mechanism in the six is an exchange with a partner (10.4), whose
  period is `gamma` across and `gamma^2` along: it gives `gamma` to a
  transverse bound clock and not isotropically. So a derivation of the
  muon's `gamma` from the six as declared does not exist, and this note
  says why: the counter reads nothing of the motion, and the rows'
  `gamma` is anisotropic until something contracts.
- **The contraction and the isotropy of c**: conditional on
  `source-velocity-v1`, which is named and not designed; the paper
  carries 5b as a FAIL under the law and under the identity.
- **Can the paper stand with the conditional statement?** Yes: "the law's
  rows carry Lorentz's symmetry in the limit, exactly; a body's counter
  carries it under one declared coupling whose form the cube's symmetry
  forces (covariant-readings-v1, the muon at 70 and 124, z at 0.3674,
  measured once); the contraction is not reached, and a moving
  laboratory's light clock is anisotropic by `gamma`, a registered FAIL".
  A referee accepts the three statuses labelled so; what the referee
  would not accept is `gamma` presented as reached for the bodies.

## 7. Proposed lines for the documents I do not write

- **DERIVATIONS_BEAM 21.4, row E2** (the derivation mathematician), the
  column "what the six verbs give": add "the transverse light clock's
  `gamma` from the flight table's `T_D` (Pythagoras: `|D| / b`), the
  longitudinal `gamma^2`; a body's counter nothing (Theorem 1 of the
  open-problems note); the gate's form forced by the cube's 48 once the
  counter reads **p** (its Theorem 3)".
- **DERIVATIONS_BEAM 4.3** (the same): after "the moving clock's factor
  is 1": "a theorem of the counts table: the only gates of a
  self-creation are the frame's advance and the crowd's owed count,
  whose isotropic mean is speed-independent (12c)".
- **NATURE.md** (the physicist): a row 4c, "a co-moving transverse
  detector's age", with section 5's pin, NOT YET; rows 4a and 4b's
  "closed on paper by section 17" made "closed by one declared coupling,
  its form forced".
- **The paper** (the coordinator): the Lorentz section's open decision
  restated as section 6's sentence; the open problems' item (1) restated:
  "no derivation of `gamma` from the verbs exists" becomes "the six verbs
  give `gamma` to the rows' clocks and not to a body's counter, proved;
  the bridge is one declared coupling, its form forced".
- **HIGHLIGHTS 5.4**: nothing; no decision here.

## 8. Questions, through the Boss

1. **For the owner (substantive)**: none that the physics leaves open;
   the choice among A, B and C of record 230 was made (record 270), and
   this note finds B dissolved into the identity and C closed. If the
   paper's wording of covariant-readings-v1 should change from "a
   hypothesis" to "one declared coupling, its form forced by the law's
   symmetry", that is the coordinator's sentence and the owner's word.
2. **For the Boss**: the transverse-detector run of section 5 (two worlds
   of series K's size, seconds each, no key, no engine change) reads
   `gamma` from the six verbs through a detector for the first time; the
   Boss chooses the checks (record 396).

## 9. Links

[BEAM_LAW section 3](../../../BEAM_LAW.md#3-the-nodes-interval-nature_beam)
and [note 47](../../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[DERIVATIONS_BEAM 4](../../../DERIVATIONS_BEAM.md#4-special-relativity-the-symmetry-of-the-continuum-limit),
[12](../../../DERIVATIONS_BEAM.md#12-lorentz-from-the-delay-field-without-a-seventh-verb),
[12b](../../../DERIVATIONS_BEAM.md#12b-lorentz-revisited-the-moving-readers-count-as-the-magnetic-term-and-the-orbit-as-the-bond),
[12c](../../../DERIVATIONS_BEAM.md#12c-the-movers-counter-under-the-crossing-count-and-the-owed-count-route-c),
[17](../../../DERIVATIONS_BEAM.md#17-the-law-above-newton-and-einstein-the-theorem-of-covariant-readings-built-on-newton-and-tried-on-lorentz)
and [18.1](../../../DERIVATIONS_BEAM.md#181-the-clock-in-motion-rows-4a-4b-5b-closed-on-paper-by-section-17);
[the two reviews of covariant-readings-v1](../../derivations_beam/REVIEW_COVARIANT_READINGS.md)
([the second](../../derivations_beam/REVIEW_COVARIANT_READINGS_ROUND2.md));
[light_speed/FORM.md](../../light_speed/FORM.md) (form B and lorentz-v1);
[HYPOTHESES 21](../../../HYPOTHESES.md); [NATURE](../../../NATURE.md) rows 4a, 4b, 5b;
[the three tests](../../../../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202).
