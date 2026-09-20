# Physics-rule review: `doppler-v1`, commit e916e115 on `doppler-v1` (base origin/main f3a41f28)

Read-only. Read: the diff (10 files, +986/-23), `world.py`, `nature_beam.py`,
`engine.py`, `measured.py`, `run.py`, `tests/test_doppler.py`, BEAM_LAW note 38,
ENGINE, MIGRATION, TEST_EXPECTATIONS; the contracts (physics-rule-validation
SKILL, the local integer operation contract, LOCALITY-1); the design (FORM.md
section 6 on `claude/series-m-masses`; record 119 on
`claude/universe24-new-3ytqde`). Run from the scratchpad, nothing written
in the worktree: `tests/test_doppler.py` (11 passed, 10 s); an arithmetic
probe of the G2 world `hubble_stars/gravity_scalar.json` (from
`claude/series-g2-stars`) through the branch's own `parse_nature_beam_world`,
`step_divisor`, `relative_speed_bound`.

## Verdict

**Mergeable as `doppler-v1`** (a world key off by default, its own identity,
every shipped world byte-identical by construction: the weight enters only
behind `world.doppler and free and not entry.fixed`), **on one condition**:
B1 below, a documentation line, because the record as written promises a run
the build refuses. The rule as built equals FORM.md section 6 (the pair, the
arrivals only, per (direction, column) floors off the reader's clock, R1 and
R2 met on the products, local, generic, the pace read from the table); the
sign at v > c and the "floors only where p_a is nonzero" rule are choices the
record must own (S2, S4), not defects.

## Blocking

**B1. The record says the moving-body worlds are re-run under the key by the
G2 session; as built they cannot be.** `_doppler_load_checks` budgets only the
pair's numerator, (N + T) x D <= 2^62 - 1. Every G2 star world passes it
(`gravity_scalar.json` parses under `doppler: true`, D = 2^48.05 .. 2^48.49,
87 D fits) and refuses at the first weighted push: one mass row (amount 64,
V = 2^12) read by a star (E = M_A = 2^22 + 4096, n = 1) against a heading
gives |V E n| x |32 D - 55 s p| = 2^87.1 .. 2^88.1 against 2^62, 26 bits out,
by the same R1 refusal the implementer met on the bar with rows of 64
(2^32 x 155 x 2^26). It is not the width: at S = 1 and amount 1 the same
star's product is 2^61.0, so no G2 world fits at any S; the content enters
twice (E and D). The grain form of FORM.md section 1 (|num| <= N Q + T Q =
5568 on a heading) fits with room (2^46.4). Condition: note 38, MIGRATION and
ENGINE state that the load check is a budget of the pair only, that the
registered moving-body worlds (G2's stars; the deuteron by FORM.md section 1)
refuse at the first weighted push under the key, and that the second G2 run
(record 119 (6)) needs either the grain form as an owner-declared width or a
world re-scaled to content about 2^20, rows of amount 1 and a small S. The
refusal itself is loud and named (body, Node, column, direction, product):
that part passes.

## Should-fix

**S1. The load check reads a smaller content than the push.** The check sums
`held` over free families only; the run's D uses `Measured.content =
sum(held)`, paid families included (`_move`, `frame_content`,
`doppler_terms`). A paid body holding free content (a G2 star: 4096 of light
beside 2^22 of mass) is budgeted at load 0.1 % below the D it reads at the
push; a world at the edge passes load and refuses at its first push. Read the
same content in both (the note claims "the same bound at load").

**S2. The sign at v > c is a physical choice the owner has not made.** The
build takes FORM.md section 6 literally ("the sign of the push flipped where
N_d D_a - T_d s p_a is negative") and pins -57 on the bar's "outrunning at
0.75" (0.75 Links per interval, 1.29 c). The map's own table (section 4)
lists 58 unsigned, and the owner's frame (record 119: a body TAKES a message
at the rate at which it and the message meet) is a count, nonnegative
(|c - v| / c). Physically the flip makes the gravity column repel: a body
outrunning its source's rows is pushed away from the source, while the
message it takes still points from the source and its momentum in the lab
frame is unchanged; a classical absorber faster than its stream sweeps rows
from behind at the rate |v - c| and still gains their momentum with the same
sign. My reading: |.| (+57) is right in the owner's frame; the flip is the
mathematician's signed-flux reading. Either way: one line of the owner in
note 38 before any world at v > c is run; if |.|, the -57 line and
`column_term`'s use of the numerator's sign change together.

**S3. R1 on the new denominator product.** `column_term` forms `divisor *=
den` (D_c d_c x N_d D_a) untested by division; only N_d D_a is budgeted (by
`relative_speed_bound`). The old law's `denominator * d` was also untested,
and FORM.md section 1 admits Python integers inside `by_clock`'s step; state
that exception for this product in note 38 or test it by division.

**S4. "Per-direction floors only on an axis where p_a is nonzero" is a new
rule, exact, and should be named as the implementer's.** FORM.md section 6
says per (direction, column) floors, and claims bit-identity at p = 0 in
general; that claim is true on headings and wherever the column's divisor is
1, and false on a fan with a column denominator > 1 (a sum of floors is not
the floor of the sum). The implementer's rule keeps the claim true: on an
axis with p_a = 0 the plain branch runs the same operations as before
(`column_term` with weight (1, 1) is the old inline code line for line), so
a free body at rest is bit-identical on a fan. Its price is a discontinuity
at p_a -> 0 of at most (directions present - 1) units per column per
interval, and a body's push at p_a = 1 differs from p_a = 0 by more than the
weight. Per-direction floors always would not move series C's fixed probes
(a fixed body never enters the branch) but would move a free body at rest on
a fan with d_c > 1 under the key (the deuteron's nucleons before their first
step, Bohr's electron), which the owner's "bit-identical for every fixed
body" does not cover and the mathematician's claim assumed away. Keep the
rule; add to note 38 that it departs from section 6 and why; test it on a
fan with a column of denominator > 1 at p = 0 (bit-identical under and
without the key) and at p = 1 (the split).

**S5. Test gaps.** Missing: a body on a set (`span`) under the key (the sum
over its Nodes with one p); a body moving on two axes at once; a moving
reader with a column of denominator > 1 (the fan test is gravity alone; the
bar's probe has one direction); the `frame_momentum` snapshot with two
groups in one interval after the first has changed the momentum; the free
body at rest identity is tested as 0 = 0 (probe off): a direct `push_form`
call with `DopplerTerms(moving=(False, False, False), ...)` against `None`
on a nonzero push would test the claim. Covered and right: the six bar lines
(the map's 97 and 58 are 96.875 and 57.8 at the engine's clock ages from 0;
the floor's grain, not a defect), the refusal at the first weighted push
naming the column and the direction, the third law (both fixed: it tests the
guard only), the parse refusals, the pace table, a moving reader on a fan
(one floor per direction, the y axis at rest read as today), the fixed
reader on the same fan, `run.json`, the gate set's parse.

**S6.** `column_term` with a numerator of 0 divides by zero
(`MOMENTUM_BOUND // 0`); the caller skips such a term, so no run reaches it;
guard or state it.

## Notes

N1. Locality (LOCALITY-1) confirmed: the inputs are p_a and M from the
reader's own record as the frame read them, the row's direction from its own
record (`t_arrival` is `store.direction` where the row moved this interval;
the fan test's diagonal at index 8 confirms it is a table index, not a face),
the pace a table constant per direction; no history, nothing at a Node;
work per group bounded by directions present x 3 x columns.

N2. Genericity confirmed: no branch on a family or column name (names appear
only in refusal text); the weight is one factor for every column and family;
32/55 is computed by `axis_pace` from Q and the vector (110 = isqrt(3 Q^2),
156 on (1, 1, 0), 247 on (2, 1, 0)) and appears as a literal only in tests
and docs.

N3. Where the weight enters and does not: the push of a free family's group
on a free, non-fixed reader only. Not in the clock's count, the size and
threshold readings, the meeting, the emitter, a paid ray's click, the
contact's hand-over (`engine._contact` moves a body's momentum through the
occupant's table; no `push_form` call, the weight cannot enter), the step
rule. A `read` entry's push on a moving body is weighted (the bar). A body on
a set gets one `DopplerTerms` per Node group with the same p: the sum over
its Nodes, as the design says and nothing more.

N4. The per-axis weight on an oblique direction is the design's, 1 -
v_a / c_{d,a}, not a flux's scalar 1 - v . c_d / |c_d|^2 applied to every
component: on the fan test's diagonal 0.1875 against 0.594. The owner
accepted the per-axis form (record 119); a question for the mathematician
on fans, not a defect of the build.

N5. A paid family's click pushes by its label unweighted: FORM.md's scope
(the arrivals' flow). The owner's verb TAKE would cover a click too (nature's
absorber takes h f Doppler-shifted); out of scope here, worth one line.

N6. The fixed body's weight 1 whatever its booked momentum is the owner's
requirement (record 119, "bit-identical for every fixed body"), not a new
rule; physically right (a fixed body's momentum is a book, not a speed).

N7. R2 met: `bounded` after every (direction, column) term. R1 met on
|V| x |E n| and on its product with |num| (tested by division before each is
formed); the pair's numerator budgeted before it is formed; see S3 for the
denominator.

## The six questions, one line each

1. Equals the admissible form: the pair, `frame_momentum`, `FlightTable.pace`
   from `axis_pace`, arrivals only, per (direction, column) floors, never
   summed before the floor; the clock, size, threshold, meeting and emitter
   untouched; see N3 and N4.
2. Bit-identity exact for a fixed body (the guard) and a free body at rest
   (the same operations); the "only where p_a is nonzero" rule is new and
   exact (S4); per-direction floors always would not move the fixed probes.
3. The refusal is loud and named and is the design's bound (FORM.md section 1,
   D_a < 2^62 / 87, the exact pair, the grain not taken); the G2 worlds pass
   the load check and refuse at the first weighted push by 26 bits; the
   second G2 run needs the grain form or a re-scaled world (B1, S1).
4. The six lines hold to the floor's grain; the -57 is FORM.md section 6's
   text, but |.| is the owner's frame and the flip repels under gravity at
   v > c (S2); the refusals, third law, parse and record are tested; missing:
   a set body, two axes, d_c > 1 on a moving fan reader (S5).
5. Generic: no name branch, one factor per column, the pace from the table.
6. Mergeable as `doppler-v1` on B1; S1 to S6 before any registered run.

## Not checked

No G2 world was run (the arithmetic above through the branch's functions
only); the gate set's fifteen worlds were not replayed by me (the tests' (e)
parses them; byte-identity rests on the guard, which is structural); the
set-body path was not exercised; `python tools/check.py` was not run; the
inverse interval was not considered (no measured events there); the
mathematician's bit-identity claim for record 35's 11 945 pushes was taken
from the guard, not replayed.
