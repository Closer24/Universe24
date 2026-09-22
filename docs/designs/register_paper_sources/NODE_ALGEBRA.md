# Every operation at a Node against the six verbs: the audit, and what is outside them (the Register Architect, 2026-09-22)

The model owner's word (2026-09-22, in Hebrew, to this session, translated):
"Make sure that all the algebraic operations at a Node are by the rules of
modern algebra, the clicks too; it should be really clear and simple in the
code." The law's verbs are the six of Highlights 5.4 ("The six operations",
the owner's records 181 and 202): (T) the translation of an accumulator by
its rate, (B) the bilinear form with a declared matrix, (G) the group-ring
addition in Z[Z_N], (P) the permutation, (E) the evaluation of the tables at
zeta_N (the primitive N-th root of unity), (D) the Euclidean division with the
remainder kept and the comparison. Two places are not linear and there is
no third: the carry and the click's threshold. A root is the seventh verb,
outside the law by the owner's decision (record 249: the law stays the six
verbs; a root enters only under its own identity beside the law).

This audit reads main at 8b414806 (merged into `register-paper-sources` at
9426899f) and the mathematician's table
[docs/designs/vector_form/LAW.md](../vector_form/LAW.md) section 4, place by
place. No code is changed here: `nature_beam.py`, `engine.py`, `world.py`,
`measured.py` and `meeting.py` are the files of the branches in flight
(`generic-bending`, `moving-detector-build`), and the ordering proposed in
section 4 is done after their merge SHAs, as
[PLAN.md](PLAN.md) section D orders every edit of those files.

## 1. The interval, step by step: the verb each step is in the code

`nature_beam()` (`nature_beam.py:3299`) runs one Node's interval at every
Node; `engine.py:576` frames it (the clocks' frame, the bodies' steps, the
law, the turn and the count).

| Step | Code | Verbs in the code | Verdict |
| --- | --- | --- | --- |
| 1. The walk | `_walk` (:3966), `by_drive_rows` (:586), `by_clock_rows` (:569) | (T) the Manhattan accumulator gains `2 S_1 Q` against the wall `2 T_D`, (D) the carry is the Link and the deficits choose the axis; the phase (T) on Z_N per Link; the age (T) at rate 1; the face a click (E); the exact phase at the click (E) once on the table | in the six |
| 2. The readings | `read_arrivals` (:522), `Moments` (:365), `CrowdMoments` (:3069) | (B) the moments `sum w u^k`, exact integers, the bound a refusal | in the six |
| 3. The collision | `_collide` (:3360), `collision_table` (:1203) | (P) the eight slots' single units permuted within their class, an exact cache of "sort, then shift" | in the six |
| 3b. The meeting (the key `meeting`, off by default; K under the meeting) | `meeting.py:329-365` | (B) the crowd's flow and the column sum, (P) the arc permutation, (T)/(D) on Z_N with the carry; and one root: `norm = integer_root(t . t)` per row per interval (:359) | ONE ROOT at run time, the known seventh verb (LAW.md 4.3 names it; the exact form is the comparison ladder of `t . t` against `(k Q)^2`) |
| 3c. Under the key `optical` (off by default) | `optical_turn` (:3730), `optical_walk_step` (:3634), `momentum_pair` (:3494) | (T) the turn's accumulator by the crowd's flow, (D) the stretched rate against the stretched wall; and one root: `resolution = math.isqrt((R^2 + 3 abs(P)^2) Q^2)` per pushed row in every interval its momentum changes (:3549) | ONE ROOT at run time, not named as a seventh verb anywhere; the 32 crowd worlds refuse exactly there (record 866: "the wall's square ... exceeds the working bound before the root"); `generic-bending` keeps it (its `momentum_pair` at :3531, the root at :3586) |
| 4. The measured events' tables and the detectors (the click) | `_family_plan` (:4317, 587 lines), `FamilyPlan` (:2557), `_apply_plan` (:4915, 458 lines), `_measure` (:5423) | (D) the window `(d + w // 2) mod N < w`, the threshold on the amount, the parity filter on the hand; (B) the push `p += C a` per column through `push_form` (:2932) and `signed_inner`; (D) the share `label x amount // m`; (P) the gate; the record lines | in the six, but spread over about 1,500 lines of bulk numpy, the verbs not named |
| 4b. The click's ledger and the read-out | `amplitude.py`: `Layer.evaluate` (:766), `gram_form` (:788), `cells` (:817), `rungs` and `cell_of` (:241, :275), `node_choice` (:299) | (E) the offer `(X, Y) += 32 w (C[p], S[p])`, a ring homomorphism; (B) the Gram form; the norm `abs(z)^2` of the evaluation; (D) the one comparison `2 T u + T <= 2 W C_k` and the rungs, no division at run time; the wheel (T) on Z_W | in the six: the click is the clearest part of the code |
| 4c. The join of two multiplicities at an offer | `common_denominator` (`amplitude.py:223`) | `math.isqrt` used as the test "is the ratio a perfect square" (refused when not); an exact predicate, no rounded number enters a reading | a comparison in effect, written as a root: to be written as the predicate it is |
| 5. The self-creations | `_release` (:5960), `_release_family` (:5494), `born_recoil` (:1620), `apportion_whole` (`core/integer.py:233`) | (T) the release and the lamp's count by `by_clock` / `by_drive`; (D) the apportioning, exact, the tie by comparison; (B) the recoil `p -= sum labels`; the right-hand rule (B) then a comparison | in the six |
| 6. The border and the merge | `_border` (:6076), `_merge` (:6215), `_merge_rows` (:1377) | (D) the comparison of the age against the lifetime key; (G) the addition in Z[Z_N] of identical rows, `[p + N/2] = -[p]` the cancel | in the six |
| The frame around the law | `engine.py:_frame_all`, `_move`, `step` | (T) the turn, the owed count, the drive by `by_drive` with the remainder kept; (D) the carry the event; the crossing rule's comparisons | in the six |
| The covariant readings (the key `covariant_readings`, series S) | `engine.py:336-366` at load, comparisons in the frame | the root `integer_root(square)` ONCE AT LOAD (E' the declared rounding of DERIVATIONS_BEAM 17.6 M3), then comparisons only | a declared load-time rounding, in the six at run time |
| The load-time constants | `world.py:470, 545, 610, 1621, 3059`; `nature_beam.py:842, 860, 874, 1051, 1148` | `T_D = isqrt(3 abs(D)^2 Q^2)`, `T_HEADING`, the label rounding `k(abs(a))`, `E'_D` of optical's triples, `E'_0` | declared roundings at load (LAW.md section 6); the section 6 list lacks `E'_D`, `E'` at load and `T_HEADING` |

The numeric audit of the gates (`diagnostics/numeric_audit.py`, run by
`tests/test_architecture.py`) refuses floats, true division and `sqrt` in
`events/`, and ALLOWS `math.isqrt` and `integer_root` there: the gate does not
enforce the six verbs at run time, only the integers.

## 2. The verdict, in the owner's terms

1. **In the six, verified place by place**: the walk, the readings, the
   collision, the click (the window, the threshold, the push, the share, the
   gate, the ledger's evaluation, the Gram form, the rungs), the
   self-creations, the border, the merge, the frame's counts. The two
   non-linear places are the two the law names (the carry, the click's
   threshold) and there is no third among them.
2. **Outside the six at run time, two places, both under keys off by
   default**: the meeting's norm (`meeting.py:359`) and the pushed row's wall
   under `optical` (`nature_beam.py:3549`). The first is named as the seventh
   verb in LAW.md; the second is named nowhere as such. Under the generic
   entry of the bending (`generic-bending`) the second stays and stops being
   under a key: it becomes a root inside the law's interval. This is the one
   finding that needs the physicist's and the owner's word before that
   branch merges: either the pushed row's wall is a declared constant (the
   flight table's `T_D` on the primitive direction nearest **P**, a table
   read, in the six) or a comparison ladder (`(R^2 + 3 abs(P)^2) Q^2` against
   `T^2` for the candidate T, the exact form LAW.md gives the meeting), or it
   is admitted as the seventh verb under its own identity (record 249's B).
3. **A root written where a comparison is meant**: `common_denominator`'s
   perfect-square test. No number is rounded, but the code says root.
4. **Clarity**: the click's ledger (`amplitude.py`) is clear; the Node's
   interval (`nature_beam.py`, 6,455 lines, 104 definitions) is not: the six
   verbs exist as named primitives only for (D) (`by_drive`, `by_clock`,
   `apportion_whole`) and, in part, (B) (`signed_inner`); the walk's (T), the
   collision's (P), the merge's (G) and the tables' (E) are bulk numpy with
   the verb in a comment, and the click's plan (`_family_plan`, `_apply_plan`)
   interleaves five verbs over a thousand lines.

## 3. What is not changed by this audit

No formula, no pin, no register; the local integer operation contract and
LOCALITY-1 as they are. A finding here is a statement about the code's
form, not a physics change; the one physical question (item 2) is put to
the owner and the physicist, not decided.

## 4. The ordering proposed (after the merge SHAs of the branches in flight)

One line each, to be done as step 4 of [PLAN.md](PLAN.md) on the same rules
(byte-identical readings for every paper-cited world, the register's
`expectations.json` and the gate set's digests unchanged, no rename of a
rule's identity):

1. `core/integer.py` becomes the one place of the six verbs, each a named
   primitive with its docstring naming the verb: `translate` (T; today the
   accumulator lines of `by_drive`, `by_clock`), `bilinear` (B; today
   `signed_inner` and the moments' sums), `ring_add` (G; the merge's sum in
   Z[Z_N] with the cancel), `permute` (P; the collision table's application,
   the gate), `evaluate` (E; the tables' read at the phase), `divide` (D;
   `by_drive` itself, the comparison ladder). Their bulk (numpy) forms are the
   same names in `events/` with the same docstrings; no arithmetic changes,
   only its name and place.
2. Each of the six step functions of `nature_beam()` names its verbs in its
   docstring's first line and calls them by name; the click's plan is split
   into its verbs (the window and the threshold, one function each (D); the
   push (B); the share (D); the gate (P); the record lines apart from the
   arithmetic), the bulk numpy kept, the order of the records kept.
3. `common_denominator` is written as the predicate "the ratio is a perfect
   square" with no root in its name.
4. The load-time roundings are listed once, completely (LAW.md section 6
   plus `E'_D`, `E'` at load and `T_HEADING`), and the numeric audit gains a
   rule: `isqrt` and `integer_root` are allowed only in the functions of that
   list (a load-time rounding) and in a module that carries a hypothesis
   identity naming the seventh verb (the meeting; lorentz-v1 if built); a
   root anywhere else in `events/` fails the gate.
5. The pushed row's wall under the generic bending: the owner's and the
   physicist's word (section 2, item 2) before the gate of item 4 is turned
   on, since the branch as it stands would fail it.

The cost, as a host estimate: items 1 to 3 about a day of the architect's
work after the merges, no run needed, every registered digest the proof;
item 4 an hour; item 5 the physicist's, one bounded change under the
branch's own review.
