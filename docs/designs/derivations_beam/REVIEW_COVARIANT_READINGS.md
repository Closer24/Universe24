# Physics-rule review: covariant-readings-v1 as a hypothesis beside the law

The physics-rule reviewer of beam-v1, 2026-09-21. Read-only review of `origin/main`
at `a9acbd67` (a detached worktree; nothing edited, no run, no fit, no new
physics). The object reviewed: DERIVATIONS_BEAM.md section 17 (the four
covariant readings), 18.1 (the pins), 19.5 (the derived condition), 21.2
(rows 37 to 39, 44), against AGENTS.md (the change boundaries, the three
tests, the measurement rule of record 281), skills/workflow.md (the three
tests, the notation), skills/physics-rule-validation/SKILL.md (the
physics-rule-reviewer skill of this repository), SIMULATOR_DEFINITIONS.md
(LOCALITY-1), BEAM_LAW.md (notes 43 to 48), HIGHLIGHTS 5.4 ("Lorentz, B
replaced", record 270), LOG_2026-09-20.md records 230, 270, 281, and the
engine on `main` (`events/engine.py`, `events/nature_beam.py`,
`events/world.py`, `core/integer.py`).

Premise: the owner decided (record 270) that covariant-readings-v1 is built
beside the law under its own identity in place of lorentz-v1, after a
physics-rule review of the four rules, run against the pins of 18 (a). The
Boss's direction of 2026-09-21 07:15Z ("derive all of Einstein, not only
E = m c^2", record 291) is quoted from the assignment: record 291 is not on
`main` at `a9acbd67` (the log ends at record 289); nothing below depends on
its text.

Notation (record 184): c the pace of a row (1 / sqrt 3 Links per interval in
the limit; Q S_1 / T_D on a direction of the flight table); beta the speed
over c; gamma the Lorentz factor 1 / sqrt(1 - beta^2); Q the label's scale
(64); S the world's width; M a body's content; **p** the momentum vector
(label units), p its magnitude, p_a a component; **dp** the push of one
interval (a vector); E the energy accumulator (a scalar), E_0 its rest value;
A the age moment (a scalar; the scalar potential phi in the limit); **A** the
vector potential; **u**_d the unit vector of a direction; **n**_ret the unit
vector from a source's retarded position; **e** the heading of a body's last
Link; n / d a clock's rate pair; N the circle's steps; h the quantum; T_D and
S_1 a direction's resolution and Manhattan length; `by_drive` the count
primitive (an accumulator gains a rate, the whole part in units of a wall is
taken, the remainder kept on the record).

## VERDICT: ADMISSIBLE WITH MUST-FIXES

Admissible as a hypothesis under its own identity beside the law: none of the
four readings needs the seventh verb at run time; each is generic (no family
name), local in form (its own record, the six neighbours) and one of the six
verbs (comparisons, one `by_drive` with a wall that is a function of the read
state, the form section 15.2 admitted for the flight's wall). The build may
not start on section 17 as it stands: nine must-fixes below, each a design
sentence that is wrong, absent or unreachable on the engine of `main`. The
first two decide whether the pins of 18 (a) can be met at all (the counter
the identity gates; the declared momenta of the pinned worlds). None of the
nine changes the law of the six verbs.

The three verdicts per reading, one line each (record 202):

| Reading | Generic | Vector | Local |
| --- | --- | --- | --- |
| (i) the count per turn | pass: the crossing rule's comparisons, no name | pass: comparisons (D) and one `by_drive` (T) charged per proper-time unit | pass: the body's two last Links, the rows' two last steps, its own E (note 48) |
| (ii) the gradient push | pass in form: one linear combination of moments, no name | pass in form: bilinear (content x moments) and a translation; its integer form is NOT written (M4) | pass for the six neighbours' age moments (LOCALITY-1's six records; a new read, M4); FAIL for the vector potential as named (the source's velocity is no local reading, M4) |
| (iii) E as an accumulator, the drive **v** = **p** c^2 / E | pass: one accumulator per body, E_0 = Q S M c^2 forced | pass with two conditions: the rate **p** . **dp** read as the push integer (bilinear), the wall E a state (15.2's form); a root only at load for a declared momentum, to be declared (M3) | pass: its own record |
| (iv) the turn per proper time E_0 / E | pass | pass: one `by_drive`, rate content x n x E_0, wall d x E, no root; the widths overflow the register on the pinned world (M3) | pass: its own record |
| 19.5 the release reads E | pass in form | pass in form; the units are wrong as written (M6) | pass for its own E; FAIL for "the set's E" beyond one Link (M6) |

## 1. The four readings against the three tests

**(i) The count per turn** (17.3 (i)). The crossing rule (note 48) counts the
rows a moving body meets, one per crossing of world lines, by comparisons on
the body's own two last Links and the rows' own two last steps: generic,
vector, local, in force on `main` (the C1 to C3'' table). The identity
changes only the cadence at which the count is charged: per unit of the
proper-time accumulator instead of per interval. As a verb it adds nothing;
as a design it has an ambiguity of object: "the count per TURN of the body
(its self-creations under (iv) below)" says self-creations, while (iv) as
written scales the phase turn per self-creation and not the self-creation
itself (M1). A consequence to state: a moving body in a crowd is charged
gamma times the rest count per self-creation under (i), so its owed count
grows with speed (12c.2 found no such growth under the law); the design
must own it and pin it on 12c.6's probe (S5).

**(ii) The push as the gradient of the age moment** (17.3 (ii)). Section 12.1
proved that the age moment of a moving source is the Lienard-Wiechert scalar
potential in the limit, and its gradient across the six Ports is a finite
difference of six neighbour readings, a bilinear rate (the reader's content
times a linear combination of moments), local by LOCALITY-1's six records.
Three findings:

1. The sentence "with the flow's age-weighted moment as the vector potential
   (**A** = **beta** phi for a moving source)" names a reading that is not the
   vector potential. Counterexample: a source at rest releases isotropically;
   at a reader the age-weighted flow moment, sum of amount x age x **u**_d
   over the arriving rows, is the age moment times the radial unit vector,
   nonzero and radial, while the vector potential of a source at rest is
   zero. For a moving source the arriving rows fly along **n**_ret (from the
   retarded position, 12.1) and carry no label of the source's velocity
   vector, so the moment is A **n**_ret and not **beta** A. The induction term
   `-d**A**/dt = **beta** (d phi / dt)` needs **beta** of the source, which no
   reading of the rows at a Node or its six neighbours gives (a row carries
   its direction, age, phase, amount, content, hand; no source velocity). The
   claim "Maxwell's field of a moving charge exactly in the limit" is
   therefore not established for the reading named.
2. What -grad(A) alone gives on a co-moving pair (the classical computation
   on the potential of 12.1, `phi = q / (4 pi sqrt(x_par^2 + (1 - beta^2)
   x_perp^2))`): along the motion the REST force (Maxwell's total is
   `(1 - beta^2)` times the rest), across the motion `gamma` times the rest
   (Maxwell's total with the magnetic term is `1 / gamma`). Lorentz's 1904
   argument (the contraction by `1 / gamma`, the period `gamma`) needs the
   full force; -grad(A) alone gives neither, so the 5b pin is not derived
   from (ii) as stated.
3. The reading of the six neighbouring Nodes' resident rows is a NEW reading
   set: on `main` `read_arrivals` (nature_beam.py:452) reads the arrivals at
   the body's set and the swap rows (note 48), never a neighbour's residents.
   The extension is allowed by LOCALITY-1 (six causally available neighbour
   records) and is fixed work only if the reading bound (`reading_fits`,
   `first_reading_overflow`) is applied per neighbour; it must be keyed, or a
   registered world with a large crowd at a neighbour is refused by the
   larger group (bit-exactness, section 4).

Generic and local pass in form; the vector test passes in form and cannot be
checked until the integer form exists (the moments read, the coefficient
integers, the wall, the previous interval's reading kept on the body's own
record as a declared component). M4.

**(iii) E as an accumulator of the work; the drive v = p c^2 / E** (17.3
(iii)). The form is the law's: `by_drive(acc_E, rate, wall)` with the rate
the bilinear form **p** . **dp** (the identity matrix, declared) and the
wall E, a function of the read state (the form 15.2 admitted for the
flight's growing wall; here the state is the body's own accumulator, so
"local" holds without the tick question of 15.2). E_0 = Q S M c^2 is forced
by the Newtonian limit (17.3's argument is correct). Findings:

1. The rate as "**p** . **dp**" with **dp** = -M_A **V** expanded is trilinear
   in the state (content x flow x momentum); as the product of two integers
   of the record this interval (**p** and the push `pushed`) it is bilinear.
   State the second (S1).
2. c^2 in the law's units is 1 / 3 in the limit and `(Q S_1 / T_D)^2` on a
   direction of the flight table (0.3385 on a heading, 1.5 percent above
   1 / 3): the design must declare which enters the accumulator (a pair of
   integers of the identity) because the pins' gamma is `E / E_0`, read from
   the declared momentum through c^2. E_0 = Q S M / 3 is not an integer on
   the register (Q S M = 64 x 2^20 x 4 198 400 for G2's stars); the whole
   form is E' = 3 E with E'_0 = Q S M and the invariant `E'^2 - 3 p^2 =
   E'_0^2`, the drive `v = p / E'` Links per interval (the cap `1 / sqrt 3`
   as p grows). M3.
3. The initial E of a body declared with a momentum. The world file declares
   **p**, not E (`MEASURED_KEYS`, world.py:511); without a rule E = E_0 and a
   thrown body's clock does not slow at all (the muon of J4 is born thrown).
   Either the world declares E (an integer the parser checks against the
   invariant within a declared grain) or E is `isqrt(E_0^2 + c^2 p^2)` at
   load, a declared load-time rounding of the same class as T_D and **u**_d
   (the three tests allow "the ones declared at load"). Not a run-time root.
   M3.
4. The invariant is not kept exactly by any accumulator form. The midpoint
   step `E <- E + p_mid . dp / (3 E)` adds `Delta^2 = (p_mid . dp / (3 E))^2`
   to `E^2 - p^2 / 3` at every push, always positive; the script's 5 x 10^-12
   is the float's, at pushes of 10^-5 of E. On the nucleus (p about 1.4 x
   10^13, the push 3.1 x 10^11 per interval) the relative drift per interval
   is of order (v dp / (c E))^2, about 10^-4, and 3000 intervals give a
   drift of order 0.3 in E^2. "Whether the remainder closes it exactly is
   the implementer's" is not a design: state the scheme and its drift bound
   for the pinned runs, or keep the exact quantity `W = E^2 = E_0^2 + c^2
   p^2` as the state (bilinear in **p**, exact, no drift) and state how the
   drive reads its wall from W without a root at run time (a comparison of
   squares is one candidate; not designed here). M3.
5. The register widths. `MOMENTUM_BOUND = 2^62 - 1` (4.6 x 10^18,
   world.py:337). The rate **p** . **dp** on the nucleus is about 4 x 10^24;
   (iv)'s wall d x E on `coasting_none` is 4 198 400 x 9.4 x 10^13 = 3.9 x
   10^20, and its rate content x n x E_0 the same order. As written the
   identity refuses (or wraps) on the very world the z pin names. The design
   must give the scaling (the ratio E_0 / E as one Euclidean division at a
   declared grain, its remainder on the record; the rate in units of a
   declared divisor) and the bound test by division before the product is
   formed, as `push_form` does (nature_beam.py:2147). M3.
6. E on a change of content. 17.3 (iii) claims "a body that pays content
   h s for a row loses the row's energy from its accumulator E" as an
   identity; no rate is given. A click (`held += content`), a release (the
   cost `h s`), a give (binding-v1), a `become` change M and so E_0 = Q S M
   c^2; the rate given (the work) does not touch E, so E is stale after the
   first click and the invariant is broken. State: on every change of held
   content by dM, E gains Q S c^2 dM (the identity), E_0 read as Q S M c^2 at
   the frame, and whether the exchange's rows carry their energy out of E
   (the mass defect of the deuteron, 17.3's claim) or not. M7.

**(iv) The turn per proper time** (17.3 (iv)). One `by_drive` with the rate
content x n x E_0 and the wall d x E: no root, its own record, no family
name; the ratio E_0 / E of two accumulators of the record. Two findings:

1. The object. On `main` a body's clock is its self-creation count (`age`,
   advanced in `_frame_all` at every interval in which nothing is owed,
   engine.py:460); the turn is the phase steps per self-creation
   (`acc_turn`); the `become` trigger reads the AGE against `at`
   (`ages_at_key(entry.age, clock_trigger.at)`, nature_beam.py:3649). (iv)
   as written scales the phase turn per self-creation and leaves the
   self-creation cadence at one per unowed interval, so the muon's 64th
   self-creation is at tick 64 at every speed, exactly as HYPOTHESES 21 says
   of the law; the 71 / 125 pin is unreachable by (iv) as written, and (i)'s
   "per turn (its self-creations under (iv))" has no object. The design
   must say which counter the proper-time accumulator gates. (a) The phase
   turn only: then z = 0.315 follows (the pointer's turn per row falls by
   1 / gamma, the arrival spacing stays 1 + beta) and the muon does not
   slow. (b) The self-creation itself: one self-creation when the
   accumulator gains a whole unit at the rate E_0 over the wall E; then the
   age, the turn, the owed count, the release, the lamp's count and
   `become` follow proper time, the muon's pin follows, and the drive must
   be decoupled from the self-creation (`_move` runs only at a
   self-creation: `if entry.fixed or not entry.creating: return`,
   engine.py:522; under (b) the body would move at `v / gamma` in lattice
   time, a second slowing the design does not want). M1.
2. The identity `h (n / d) = Q S c^2` (21.33 at Q = 64, S = 1) is stated as
   a constraint on the inputs, derived, not a rule: correct as stated; say
   whether the engine checks it (refuse, warn or nothing) (S10).

**19.5's derived condition** (the release reads E). "One rule, the same
`by_drive` with E in place of `content`: generic, vector, local." Two
findings: the units (E is Q S c^2 times a content: E in place of content
multiplies every free body's release rate by Q S / 3, 21 at S = 1 and 2.2 x
10^7 at S = 2^20) and the owner of "the set's E" (a set of three, the
nucleon chain of 19.3, has its ends two Links apart; a body reads its own
record and its six neighbours, so its release can read its own E and at
most a contact partner's, never "the set's"). M6.

## 2. LOCALITY-1: the origin of every input, end-to-end

| Input | Owner | Delivery | Fixed work and storage | Verdict |
| --- | --- | --- | --- | --- |
| a moving reader's clock: E_0 (its content at the frame), E (its accumulator) | the body's record | none needed | one `by_drive` per self-creation, one integer kept | local |
| the crowd it reads (the count): its two last Links, the rows' two last steps off the flight rule, the Link's traffic, the entered Node's residents | the body's record; the rows' records; the walk's own fact | note 48's C1 to C3'' | fixed per row read (note 48) | local (in force) |
| the count's cadence (per proper-time unit) | the body's E | none | one comparison | local |
| the push (ii): the age moments at the six neighbouring Nodes | the rows resident at the six neighbours | a read of six neighbour records | fixed only with the reading bound per neighbour | local by LOCALITY-1's allowance; a new read to key and bound (M4) |
| the push (ii): the previous interval's reading (the time difference) | the body's record (one integer kept from the interval before, as `last_step_port` is) | none | one integer | local |
| the push (ii): the source's velocity vector for **A** = **beta** phi | NO OWNER at the reader: a row carries no source velocity | none exists | - | NOT LOCAL as named: not derivable from any local reading (M4) |
| the work (iii): **p** and **dp** | the body's record (this interval's push) | none | one bilinear form | local |
| the initial E of a thrown body | the world file (the host at load) | none | one root at load, declared (M3) | local (a declaration) |
| the release's E (19.5) | its own record | none | one `by_drive` | local for its own E; "the set's E" is not (M6) |
| the pins' reference c^2 | the identity's declared pair | none | - | a declaration (M3) |

No global estimator, no replay, no per-source map enters; the one input that
has no local origin is the source's velocity that (ii)'s vector-potential
sentence assumes. A local subtraction or a linear combination of local
moments cannot manufacture it.

## 3. The measurement rule (record 281): which reading is a detector's

The four readings are RULES of the feedback block, none is a reading in the
sense of record 281; what they change is read after a detector or on the
GameBoard as follows.

| Pin of 18 (a) | As written | Its kind on the engine | What the design must say |
| --- | --- | --- | --- |
| (a) "the muon's 64th turn at 71 and 125 (the tolerance one tick)" | the tick of the `become` line | GameBoard reading (HYPOTHESES 21: "the `become` lines the GAMEBOARD reading; the products' face clicks the DETECTOR reading") | the detector's: the products' face clicks (the tick and the Node of each click), the decay's tick derived by the flight table, named as derived; the J4 world file does not exist (NATURE 4a: "no world file") and is written with its face detectors before the run (M9) |
| (b) "the pair in motion of 12.4 with the same round trip along and across (the ratio 1 within the grain)" | counts on the `read` lines per body per tick and their ages (12.4's table) | detector kind (ENGINE.md's table: the age of a row, "read whole only by a measured event"; the `read` line of a measured event); the `step` and `contact` lines GameBoard | name the line and the derivation of "round trip" from the ages; and the geometry (M5) |
| (c) "`coasting_none`'s `s_mz2` at z = 0.315 +- 0.003" | the detector's z | detector reading (the README: `1 + z = Delta t / Delta Phi` of the arrivals' pointer at the centre) | the star's declared momentum under (iii) (M2) |

The new state E and the six-Port gradient reading enter `state.json` and
ENGINE.md's "readings by type" with their kind (the clock of a measured
event is listed as detector there) (S6). NATURE.md rows 4a, 4b and 5b are
re-read under both identities, as record 270 orders; 4a and 5b are NOT YET
(no run) and stay so until the worlds exist.

## 4. Bit-exactness of the law when the identity is OFF

The identity is a world key, absent by default (as `action`, `meeting`,
`hand`, `binding` are; `WORLD_KEYS`, world.py:381; an unknown key is refused
at world.py:1172). With the key absent the engine must compute nothing of
the four: no E on any record, no neighbour read, no change to
`read_arrivals`' group or bound, no new field in `run.json` or `state.json`
that a registered comparison reads, no change to the `become` trigger's
input. The risks on the engine of `main`, each to be closed by the design:

1. The reading set of (ii): if `read_arrivals` is extended for every body,
   the larger group can trip `first_reading_overflow` on a registered world
   with the key absent. Key the extension.
2. The base is form B (record 186), "decided and in build" (HIGHLIGHTS 5.4),
   NOT on `main`: `step_axis` is the per-axis drive `by_drive(drive, p_a,
   Q S M + |p_a|, at_most = 1)` (engine.py:85-127). The covariant drive has
   one |**p**| and one direction; on the per-axis drive it has neither. The
   identity's OFF baseline is the register AFTER form B lands and
   re-registers its 47 moving-body worlds (FORM.md section 5). M8.
3. The proof: the identity's pull request runs the full register with the
   key absent and shows the VALIDATION table (the 66 rows of the crossing's
   table) unchanged to the byte; a dedicated test loads every registered
   world and asserts no E is carried and no neighbour read is made (S8).

## 5. What the world file must declare and what the engine must refuse

Declare (the identity key, one object, absent by default; a suggested shape,
the name the design's): the identity `covariant-readings-v1`; `c2` the pair
of integers of c^2 (1 / 3, or the flight table's per direction); the grain
of the ratio E_0 / E where a division is used; per measured event either `E`
(an integer) or the rule "E at load is `isqrt(E_0^2 + c^2 p^2)`" stated once
for the identity; the coefficient integers of (ii)'s linear combination and
the components it reads; the cadence choice of M1 is the identity's, not the
world's. Families: none named (generic); every measured event of every
family carries E; a row is the body of no content and carries none.

Refuse (the engine, naming the key): the key without form B's drive; a
measured event with a declared momentum and no E where no load rule is
declared; a declared E below E_0 or off the invariant by more than the
declared grain; the key with `action` until the design states how the turn
by momentum (per Link stepped) and the turn per proper time compose on one
phase (S4); any product (**p** . **dp**, content x n x E_0, d x E) above
`MOMENTUM_BOUND`, tested by division before it is formed; a world that
declares the deleted `doppler` key (already refused). Not a refusal but a
test: under (iii) no body reaches c (`v = p c^2 / E < c` for every finite p)
and `fast_steps` (note 48) is 0.

## MUST-FIXES (before the build), numbered

1. **The counter the identity gates** (17.3 (iv), the sentence "the covariant
   reading: the turn per proper time, dtau = dt E_0 / E, one `by_drive`
   whose rate is content x n x E_0 and whose wall is d x E"; 17.3 (i), "the
   count per TURN of the body (its self-creations under (iv) below)"). State
   whether the proper-time accumulator gates the phase turn only or the
   self-creation itself, and for each of the body's six counts (the turn,
   the owed count, the release, the lamp, `become`, the drive) the cadence
   under the identity (lattice interval or proper-time unit). As written,
   `become` reads the age (nature_beam.py:3649) and the muon fires at 64 at
   every speed; if the self-creation is gated, the step must advance in
   lattice time (engine.py:522 steps only at a self-creation).
2. **The pins' declared momenta** (18.1, "What a run must show"; record 270's
   "the muon within one tick of 71 and 125 ... z = 0.315 +- 0.003"). The
   pins are stated in beta; a world declares **p**; (iii) changes the map
   from **p** to beta. FORM.md section 4's momenta 5815 and 47 349 (form B's
   0.43 c and 0.86 c) give under `v = p c^2 / E` beta 0.605 and 0.987, the
   64th turn at 80 and 401; `coasting_none`'s `s_mz2` (p_z = -51 901 289 008
   505 at Q S M = 2^48) gives beta 0.304 and z = 0.369, outside the pin by
   18 grains. Name the declared integers: the muon at p = 3640 and 12 856
   label units for 70.9 and 125.2 (c^2 = 1 / 3; 3668 and 12 955 with the
   heading's (64 / 110)^2), `s_mz2` at p = 45 097 270 682 765 for beta
   0.2674 and z = 0.3153, or re-declare the worlds and say so.
3. **The integers of E** (17.3 (iii), "E_0 = Q S M c^2 = Q S M / 3 in the
   law's units, with no freedom" and "one `by_drive` with the remainder
   kept"). Declare c^2 as a pair; scale so that every integer is whole
   (E' = 3 E, E'_0 = Q S M, `E'^2 - 3 p^2 = E'_0^2`, `v = p / E'`); declare
   the initial E of a thrown body (in the world file, or the root at load
   as a declared rounding of T_D's class); state the accumulator scheme and
   its drift bound (the midpoint form adds `(p . dp / (3 E))^2` per push,
   always positive: it cannot close exactly; or carry `W = E^2` exactly and
   state the drive's wall from W without a run-time root); give the
   register widths for the pinned worlds: `coasting_none`'s wall d x E = 3.9
   x 10^20 and the nucleus's rate **p** . **dp** about 4 x 10^24 exceed
   `MOMENTUM_BOUND` = 2^62 - 1, so the identity as written refuses on the
   world the z pin names.
4. **The push's vector potential** (17.3 (ii), "with the flow's age-weighted
   moment as the vector potential (**A** = **beta** phi for a moving source)
   and its time difference as the induction term. A linear combination of
   the readings (B), local, no name: Maxwell's field of a moving charge
   exactly in the limit"). The age-weighted flow moment is A **n**_ret (for a
   source at rest: nonzero and radial, while **A** = 0): it is not the vector
   potential, and the induction term needs the source's velocity, which no
   local reading gives. Either derive a local reading that gives **A** (with
   its proof in the limit) or restate (ii) as -grad(A) alone with its
   co-moving forces (the rest force along the motion, gamma x rest across;
   not Lorentz's 1904 pair). In both cases write (ii)'s integer form: the
   six neighbours' age moments as rates, the coefficient integers, the
   wall, the previous interval's reading as a declared component of the
   record, the new reading set's bound per neighbour, and the key that
   confines it.
5. **The 5b pin's geometry** (18.1, "the pair in motion of 12.4 with the same
   round trip along and across (the ratio 1 within the grain, against 1.375
   / 1.140)"). 12.4's pair is `deuteron_1_kick`, bound by the contact at one
   Link ("1 Link for k - 1 ticks, 2 for one"); 12.1: "the bond is a whole
   Link ... no equilibrium separation exists to contract". No push contracts
   a one-Link contact by 1 / gamma; the pin is unreachable on that geometry
   under any reading. Pin a pair whose separation is an equilibrium of the
   push against the drive (12b.2's thrown orbit `s32_r24` in the Newtonian
   regime at S = 512 or 8192, the extents along over across at 1 / gamma =
   0.977 at beta 0.2148: 0.6 Link on a 26-Link radius, the grain stated) or
   a pair held at eight Links or more by a lifetime; define "within the
   grain" in Links and intervals.
6. **The release's E: units and owner** (19.5, "a bound body's release must
   read the set's energy accumulator E, not its held content (one rule, the
   same `by_drive` with E in place of `content`: generic, vector, local)").
   E is Q S c^2 times a content; "E in place of content" multiplies every
   free body's release by Q S / 3 (21 at S = 1, 2.2 x 10^7 at S = 2^20).
   State the release's rate as the content-equivalent, E over Q S c^2, one
   Euclidean division with the remainder kept, whole integers; and state
   that each body's release reads its OWN E (a set's ends are two Links
   apart on the chain of 19.3; "the set's E" fails the local test), with
   how the exchange's energy enters a body's E (M7). Name the world and the
   detector reading that pins the equivalence principle (the active mass
   read by a probe's push against the inertial mass read by the drive),
   since Nordtvedt's 10^-4 is nature's number and not a reading of the law.
7. **E on a change of content** (17.3 (iii), "a body that pays content h s
   for a row loses the row's energy from its accumulator E, so its inertia
   E / c^2 falls by that energy over c^2 (Einstein's 1905 conclusion as an
   identity of the accumulator)"). Give the rate: on every change of held
   content by dM (a click, a release, a give, a `become`) E gains Q S c^2
   dM; E_0 read as Q S M c^2 at the frame; whether the exchange's rows carry
   energy out of E (the deuteron's mass defect, 17.3's claim) and by which
   integer.
8. **The base and the order** (17.3 (iii), "`v = p / (Q S M + abs(p) / c)`:
   a rational function declared in the lattice's frame"). That drive is
   form B, decided (record 186) and not on `main` (`step_axis`, engine.py:85,
   is the per-axis drive). State that the identity is built on form B, that
   form B lands and re-registers its worlds first, and that the identity's
   OFF baseline is that register; on the per-axis drive the covariant drive
   has no |**p**| and no direction.
9. **The pins as detector readings** (18.1, "the muon's 64th turn at 71 and
   125 (the tolerance one tick)"; record 281, AGENTS.md's bullet). As written
   the pin is the `become` line's tick, a GameBoard reading. State it as the
   products' face clicks (the tick and the Node of the click, the decay's
   tick derived by the flight table and named as derived) on a J4 world file
   that is written with its face detectors before the run (none exists,
   NATURE 4a); state pin (b) as the `read` lines' ages with the derivation
   of "round trip"; add E and the gradient reading to ENGINE.md's readings by
   type with their kind.

## SHOULD-FIXES

- S1. 17.3 (iii): write the rate as **p** . **dp** with **dp** the push
  integer of the record this interval (bilinear), not as **p** . (M **V**)
  (trilinear); the three tests say "at most bilinear".
- S2. Notation (record 184) in 17.3: `n . beta`, `A = beta phi`, `p . dp`
  appear as plain letters; the vectors in bold, gamma and beta named once at
  the section's first use.
- S3. The identity key's name and shape, added to `WORLD_KEYS` beside
  `action` and `meeting`; the parser refuses unknown keys already
  (world.py:1172), so nothing else guards it.
- S4. The composition with `action` (bohr-v1, the turn by momentum per Link
  stepped, engine.py `_move`): state it or refuse the pair.
- S5. The consequence of (i) for the owed count (a moving body in a crowd is
  charged gamma times the rest count per self-creation): state it and pin it
  on 12c.6's probe (series E's `scalar` world, p = 10 and 28) under the
  identity, beside 12c.6's law pins.
- S6. ENGINE.md "The detector's readings by type": add E (a scalar of the
  measured event's state) and the six-Port gradient (a vector), each with
  its kind; `state.json` and the `step` line carry E as they carry `drive`.
- S7. 21.2 rows 38, 39 and 44: after the fixes, the "closed form" column
  carries the integer forms (the rate and the wall of each `by_drive`) and
  the "run" column the world files by name.
- S8. The design's own tests, with inputs, an expected result and an edge
  case: (1) a body at rest under the key, E = E_0 exact, every registered
  integer of that world unchanged; (2) a thrown free body in an empty bar,
  E constant, the 64th self-creation (or turn, per M1) at the declared p's
  gamma within one tick; (3) the invariant under pushes within the stated
  drift bound; (4) the edge p = 0 with a push (E rises from E_0 at second
  order, the remainder kept); (5) the OFF test of section 4.
- S9. Record 291 is not on `main` at `a9acbd67`; when it lands, cite it in
  the design's premise line in place of the Boss's paraphrase.
- S10. `h (n / d) = Q S c^2` (17.3 (iv)): say whether the engine checks the
  identity at load (a refusal, a warning or nothing) and on which worlds it
  holds (21.33 at Q = 64, S = 1: none of the register's lamps as declared).
- S11. 17.3 (i)'s numbers (head-on 1.583 and 3.637 at 0.43 c and 0.86 c,
  across 1.108 and 1.956) are the continuum's; the lattice's crossing count
  on a fan direction is the Manhattan flux (2.4, 12c.1), so a pin on a
  moving reader's count per turn is stated per direction of the flight
  table, not as the continuum's gamma (1 - **n** . **beta**).

## THE PINS THE BUILD MUST MEET

Quoted from DERIVATIONS_BEAM.md section 18.1 (the Boss's "18 (a)"), the
sentence "What a run must show": "the muon's 64th turn at 71 and 125 (the
tolerance one tick); the pair in motion of 12.4 with the same round trip
along and across (the ratio 1 within the grain, against 1.375 / 1.140);
`coasting_none`'s `s_mz2` at `z = 0.315 +- 0.003`."

Quoted from record 270 (the decision): "run against the pins of 18 (a) (the
muon within one tick of 71 and 125, the pair's round trips equal within the
grain, z = 0.315 +- 0.003), NATURE.md rows 4a, 4b and 5b re-read under both".

Quoted from 18.1 on what stays: "route C stays closed (12c: the crossing count
through an isotropic crowd is the rest count exactly, so nothing of the
clock's slowing comes from the crowd), and the cube's 48 carry no boost
(record 231 ...), so the symmetry is the LIMIT's, the wave equation's, and c
enters the bodies through the drive `v = p c^2 / E` and nowhere else."

Quoted from 19.5 (the derived condition, 21.2 row 44 "H (a pin)"): "a bound
body's release must read the set's energy accumulator E, not its held
content ... or the equivalence principle fails for every bound body by the
binding fraction, 99 % for a nucleon against nature's `10^-4`."

The OFF pin (this review, section 4): with the key absent, every registered
integer of the register after form B is unchanged to the byte.

With M2 the three pins of 18.1 are restated on the declared integers (the
muon at p = 3640 and 12 856 label units, or the design's own with its c^2;
`s_mz2` at p = 45 097 270 682 765 or a re-declared world); with M5 the second
pin moves to a multi-Link bound pair; with M9 the first is read at the
products' face detector. The tolerance of the first pin (one tick) is met
only if c^2 is declared once (M3): the same p under 1 / 3 and under (64 /
110)^2 differs by 0.7 tick at beta 0.86.

## What this review does not do

No run, no fit, no new physics: the counterexample of M4 is the classical
computation on the potential section 12.1 already proved, the numbers of M2
and M3 are the register's declared integers put through the design's own
formulas, and the alternatives named (W = E^2 as the state; -grad(A) alone)
are stated as what the design must decide, not as rules. Nothing here
changes beam-v1; the law's FAIL rows 4a, 4b and 5b stand as the law's
prediction (route A) beside the identity, as record 270 decided.

> The scripts of this folder (`amended_pins.py`, `bell_plateau.py`, `click_gram.py`, `covariant_readings.py`, `crowd_decay.py`, `decay_click.py`, `entropy_clicks.py`, `event_count.py`, `growing_wall.py`, `kepler_compton.py`, `lamp_orbits_map.py`, `lattice_gas.py`, `lorentz_field.py`, `masses_chain.py`, `massive_rows.py`, `mover_counter.py`, `nature_numbers.py`, `orbit_thrown.py`, `periodic_images.py`, `rest_of_masses.py`, `smallest_mass.py`, `uncertainty_lattice.py`, `units_from_g.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/derivations_beam/<script>`).
