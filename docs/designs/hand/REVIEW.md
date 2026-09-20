# Physics-rule review of hand-v1 (PR #385)

Read-only, 2026-09-20, the physics-rule reviewer, at 8e1c72e8 on `hand-v1`
over origin/main 9f6c3849. Both SHOULD-FIX items of section 6 were applied on
the branch before the merge (the parity filter on a label-hand family reads the
label, `nature_beam.read_hands`, note 39 of `BEAM_LAW.md` saying which; test
(d) of `tests/test_hand.py` runs the parity image over all 48 signed axis
permutations with the axes axial and the hands verbatim, and the three
"copied verbatim" statements are scoped to the x-mirror). The branch merged
main e0285bf4 at 8407d45c and landed on main at 4f94a86f (PR #385, record 142
of `LOG_2026-09-20.md`). The text below is the review as written.

---

# Physics-rule review of hand-v1 (8e1c72e8 on `hand-v1`, over origin/main 9f6c3849)

Read-only, 2026-09-20, the physics-rule reviewer. Worktree
`/home/user/Universe24/.claude/worktrees/hand`, clean, `git log -3` confirms
8e1c72e8 sits on 9f6c3849 (PR #384). Read against the physicist's design
(scratchpad `hand/DESIGN.md`), the mathematician's `docs/designs/hand/FORM.md`
and the owner's decisions (LOG_2026-09-20 records 120, 122, 128: the three
choices confirmed). Ran: `tests/test_hand.py` (10 passed, 1.8 s),
`tests/test_repository_language.py` (14 passed), and one probe of my own
(`scratchpad/hand_review/probe48b.py`, 12 s): the four series-P worlds under
ALL 48 signed axis permutations, three transforms each. No file of the
repository edited; no `tools/check.py`.

## The probe's result (evidence used below)

| World | FULL (hands x det, axes axial): unequal | PARITY-AXIAL (axes axial, hands verbatim): differs under improper / proper | PARITY-VERBATIM (the test's transform): differs under improper / proper, refused |
| --- | --- | --- | --- |
| `w_hand` | 0 of 48 | 24 / 0 | 4 / 4, 32 refused at load |
| `w_two_sides` | 0 of 48 | 0 / 0 | 0 / 0 |
| `wu` | 0 of 48 | 24 / 0 | 20 / 20 |
| `nu_hand` | 0 of 48 | 0 / 0 | 0 / 0 |

So the law as built is covariant under the whole group (FORM.md test (a)),
and the physical parity test (the mirrored apparatus, the axis an axial
vector, the catalog's hands unchanged) differs under exactly the 24 improper
elements and only where a birth has an axis and a handed product (FORM.md
test (b), the design's 1.3). The test's own transform ("hands and axes
verbatim") is correct only for the one element it runs (see finding 2.2).

## 1. The form: is the hand the owner's and the mathematician's exactly?

- **Pseudoscalar on the row, an identity field, carried unchanged.** Built.
  `nature_beam.py:736` (FIELDS) and `:754` (IDENTITY_FIELDS) add `hand`;
  the merge key's width is 0 where the column is constant
  (`merge_key`, `:1117-1137`). Every re-creation copies it: the home
  (`:3035`), the re-release (`:3218`), the split (`:3545`), the lamp
  (`:3720`, `:3744`), the free release (`:3441-3452`), the gate
  (`_replace`, `:1745+`), the rotation (`_replace`, `:1824+`); the collision
  permutes `store.direction` only (`:2238-2285`, the slot's single-ness
  counts rows of any hand, as the design says); the meeting does not touch
  the store's columns beyond direction and phase (`meeting.py`). Test (a)
  covers all of these and the non-merge and non-cancel of opposite hands
  (`test_hand.py:266-285`). Exactly FORM.md section 1 and the design 1.2.
- **The axis axial on the body.** `world.py:1567` (`_axis`: one of the six
  headings as a vector, refused otherwise), `MeasuredDefinition.axis`,
  `Measured.axis`; read in one place, the birth (`nature_beam.py:3596`).
  Fixed like `fixed`, no ledger. As decided.
- **The right-hand rule and its sign.** `nature_beam.py:3596-3605`: for a
  thrown row with a hand at a parent with an axis, admitted = the parent's
  directions with `axis_sign(A, u_d) == row.hand` (`world.py:1584`, one
  integer sign of one component). So a left-handed product leaves AGAINST
  the axis: `sign(A . u_d) = h`, the physicist's choice (i) that the owner
  confirmed (record 128), NOT FORM.md's `sign(a . d) = -h` (the assignment's
  phrasing of the rule uses FORM.md's convention; the owner's decision is
  the physicist's, and the code follows the owner). `wu.json` pins Wu's
  side (the beta on -x against +x). Correct.
- **The strict hemisphere; the equator.** For a HANDED product a direction
  with `A . u_d = 0` is not admitted (sign 0 != h): silently excluded, the
  set refused at load only when it is empty (`world.py:1594-1622`,
  `_handed_products`, naming rule, product and axis; test (b)
  `test_hand.py:391-395`). For an UNHANDED product at an axis parent every
  direction is admitted and the row is stamped `sign(A . u_d)`: 0 on the
  equator (`:3605`; test (b) `:372-388`, six headings +1/-1/0/0/0/0). Both
  are what the design 2.1 says ("+1 along, -1 against, 0 perpendicular";
  choice (ii) confirmed). Stated in BEAM_LAW note 39 (`docs/BEAM_LAW.md:2863-2866`)
  and TERMINOLOGY "Axis". Not a tie, not a refusal: declared behaviour.
- **The filter as the which-path factor, exact.** `nature_beam.py:2741-2742`:
  `inside &= (admits == 0) | (hand_at == admits)`, applied after the window
  and after the `sum`-set exemption, so a passed row goes on as a row
  outside a window does (the same `passing` path, `:2743`). Exact, the same
  code path, as FORM.md 4. Refused on `pass` (`world.py:2262`). Correct for
  rows whose hand is the COLUMN; see finding 1.1 for the label-hand case.
- **The products' hand from the family's home.** `transform`,
  `nature_beam.py:1469`: `hand=families[family].hand`; choice (iii). A
  handed product at a parent without an axis leaves on every direction with
  its hand (`:3596` guards on `entry.axis`), the unpolarised parent lawful,
  as decided. Test (b) `:398-403`.

**Finding 1.1 (SHOULD-FIX, docs or code).** The parity filter reads the
row's column only. On a branched family whose hands live in the labels
(`branches [[0,1,+1],[3,1,-1]]`, the row column 0 by the one-or-the-other
rule) a table entry with `hand` +1 or -1 admits nothing and passes every
row. FORM.md 4 says such a record "offers its two hands' rows to two sets",
and the design 4 pins "a `hand` filter alone on the same lamp is the
which-path click on the label: 32 of 64". Neither is built nor tested, and
FORM.md's "refused ... on a family whose rows carry no hand" is not built
either (a filter on a label-hand family loads silently). HYPOTHESES 23 lists
the composition of the label rotation with a label hand as open
(`docs/HYPOTHESES.md:1010-1016`) but not this. Fix: either make the filter
read the label's hand for a row of a record whose lamp names label hands
(the same lookup `row_hand` already makes, `nature_beam.py:1925`), or refuse
`hand` on an entry of a family that carries its hand in the labels, and in
both cases state it in note 39. No pinned integer moves.

**Finding 1.2 (NOTE).** The books' `left`/`right` count the column
(`nature_beam.py:3284-3290`), while the click line of a label-hand row
carries the label's hand (`:3338`, `row_hand`). On a Bell world with label
hands the books read left 0, right 0 under click lines of +1/-1. A report
inconsistency; say in note 39 that the books count the column.

## 2. Genericity, locality, the 48

- No branch on a family name anywhere in the change: the rule reads
  `families[family].hand` (an integer of the family), `entry.axis` (an
  integer of the body) and the direction table (`:3596-3605`); the filter
  reads `ev_hand[ev, family]` and the row's column (`:2741`). Grep of the
  diff: no family-name literal in `src/`.
- Locality: the birth reads the parent's own axis and its own declared
  directions at its Node; the filter reads the arriving row at the reader's
  Node against the reader's declaration; every re-creation copies a field of
  the row it holds. Fixed work per product per direction, one comparison per
  arrival. LOCALITY-1 kept. The one host read is `row_hand`
  (`nature_beam.py:1925-1937`): the click line's label hand is read from the
  EMITTER's lamp declaration by the record's identity; it is a world
  constant (as the family table is), it feeds nothing of the law, and note
  39 says so (`BEAM_LAW.md:2972-2974`). NOTE, acceptable.
- **Finding 2.1 (verified).** The 48-covariance claim holds on the engine:
  my probe finds the full transform (h -> det(g) h, a -> det(g) g a) equal
  under all 48 on all four worlds, and the axial parity test differs under
  exactly the 24 improper elements on `w_hand` and `wu`, never under a
  proper one, and never on `w_two_sides` or `nu_hand`. That is FORM.md
  tests (a) and (b) to the letter.
- **Finding 2.2 (SHOULD-FIX, test and docs).** Test (d) runs the parity
  test under `MIRROR_X` only and the full transform under `MIRROR_X` and one
  rotation (`test_hand.py:654`, `:679`). Its parity transform copies hands
  AND AXES verbatim (`:523-526`, `:542`). That equals the physical parity
  test only for elements that fix the axis line: under the y- or z-mirror
  (the axis in the mirror's plane, whose axial image is the OPPOSITE
  heading) the verbatim copy keeps the axis and reads "equal" on `wu`, where
  the mirrored apparatus differs; under a rotation moving x the verbatim
  world is a different world (refused at load on `w_hand`, 32 of 48;
  differs under 20 proper elements on `wu`). The doc statements
  "every `hand` and `axis` copied VERBATIM" (`BEAM_LAW.md:2938`,
  `TEST_EXPECTATIONS.md:2104`, `examples/events/hand/README.md:70`) are
  therefore right only with their stated scope (the x-mirror, where the two
  coincide, as note 39 itself remarks) and wrong as the general parity test.
  Fix: define the parity test as the design's 1.3 says (polar things by g,
  the axis by det(g) g, the hands verbatim: the law's data), run test (d)
  over the group's three generators and the inversion at least, or all 48
  (12 s for four worlds), asserting "differs iff det(g) = -1" on `w_hand`
  and `wu` and equal on the other two; every pinned integer of the x-mirror
  is unchanged. One rotation is not enough to claim "restricted to the 24
  proper rotations and not to fewer": the axial flip (axis in the mirror
  plane) is exercised by no element the test runs.

## 3. Integers, byte-identity, bounds, the books

- Byte-identity: the column defaults to 0 (`COLUMN_DEFAULTS`,
  `nature_beam.py:762`), no line writes `hand` unless `world.handed`
  (`world.py:1042`; every `if handed:` in `nature_beam.py`, `engine.py:768-806`,
  `run.py:136-176`); the gate set 15 of 15 byte-identical against 56a258f8
  (VALIDATION `docs/VALIDATION.md:14-53`); test (e) shows the packed key
  equal with and without the column (`test_hand.py:712-715`). `HAND_RULE`
  appended last (`world.py:1082-1083`), only when handed.
- The 16th gate world `hand/wu.json` (cap 23, the face click): appropriate,
  the first replayable world exercising the hand's lines; `test_doppler.py`
  updated for 16. NOTE: VALIDATION's digest table lists 15 worlds; add wu's
  two digests so the next replay has a base row (the replay compares trees,
  so nothing is blocked).
- Bell (g): S = 176/64, marginals 32/64, E x 64 = (44, -44, 44, 44), the
  row column 0, the click lines by the label bit (`test_hand.py:786-812`):
  the label bit named changes no integer. Verified by the test.
- Bounds: `A . u_d` one component within P; no product, division,
  remainder or draw; the merge key gains at most 2 bits where the hand
  varies; the row bound a factor 3 only where declared. Untouched elsewhere.
- Books: `left`/`right` are reports beside the measured line
  (`engine.py:801-806`, `measured.py:531-548`); `balanced` is unchanged and
  asserted at every tick of every run in `test_hand.py:136`. They close.

## 4. The four deviations

1. **The charge line 14688 (NOTE, correct).** `w_hand` has two protons of
   1836 at charge 4 per unit of content (`make_worlds.py:88-109`): 2 x 7344
   = 14688, conserved through the birth (3 x 7344 - 7344). The design's
   "[7344, 1] unchanged from `w_exchange`" forgot its own second proton.
   Reported honestly in EXPERIMENTS and the README, not moved.
2. **The control at measured 1 (NOTE, correct, the documented tie).**
   `nature_beam.py:3411`: `age = entry.clock_age`, "the age before the
   interval's self-creation, at which every rate of the law is read"
   (BEAM_LAW `:433-436`, note 33's unification (4)); the apportioning's
   leftover at `(clock age + k) mod n` (note 36, `BEAM_LAW.md:2318-2322`)
   is 7 mod 2 = 1 at the self-creation that takes the clock from 7 to 8:
   the second declared direction. This is the tie of record 105 / note 36
   as written, not a new one; the design read the clock age as 8. The
   control's verdict under the mirror (equal, the tie on the declared list
   order) does not depend on the side.
3. **No `pass` line for a `pass` rule (NOTE, existing form).**
   `nature_beam.py:2643`: rows at a `pass` entry are not "met", so no pass
   line has ever been written for them; pass lines are the rows a
   responding entry did not take. The design's 3.4 misread the record's
   form. The antineutrino's passage shows in the face click at tick 23 as
   pinned. Documented in note 39 and the README.
4. **A group line's hand None if mixed (NOTE, lawful; a report gap).**
   Groups are (event, number) (`nature_beam.py:2870-2876`), not the identity
   fields, so a source of one number emitting rows of both hands (an
   unhanded product at an axis parent, six headings: +1, -1 and 0 from one
   parent) lawfully gives a mixed group at a `read` or `rerelease` entry.
   The law admits it (each re-created row keeps its own hand, `:3218`); the
   design's premise "a group is of one hand" was wrong. Refusing or
   splitting is not warranted; a per-row list (as the click line already
   is) would be the better report. Not a defect.

The label hand read from the emitter's lamp (the fifth item the implementer
noted): NOTE, see section 2.

## 5. Docs

BEAM_LAW note 39 (`:2809-2984`), HYPOTHESES 23 (`:966-1019`), ENGINE
(`:412-427`, `:696-699`, `:766-771`), MIGRATION (`:9-51`), TEST_EXPECTATIONS
"The hand" (`:2045-2131`), TERMINOLOGY Hand/Axis (`:38-39`), ENTITY_CATALOG
(the neutrino, the W and Z, spin and polarization; `nubar` added to
`families.json` and `make_definitions.py`, 48 names), EXPERIMENTS P
(`:5347-5419`), VALIDATION (`:14-53`), the two READMEs: consistent with the
code line by line (the sign, the equator, the filter after the window, the
`sum`-set exemption, the record's keys, the books, the identity last), and
honest about the four deviations. English throughout (`test_repository_language.py`
14 passed). No HIGHLIGHTS edit (diff stat). No `board`, `lattice`, `grid` or
`Site` noun in any added line (grep). `hand-v1` last under `hypotheses`,
only when handed (`world.py:1082`, ENGINE `:696-699`). Two doc corrections
follow from findings 1.1 and 2.2 (the filter reads the column; the parity
test's axis is axial in general, verbatim coincides on the x-mirror only).

## 6. Verdict

MERGEABLE AFTER the listed SHOULD-FIX: (2.2) test (d) run with the axis
axial and the hands verbatim over the group's generators or all 48, and the
three "copied verbatim" statements scoped to the x-mirror; (1.1) the parity
filter on a label-hand family either read from the label or refused, and
note 39 saying which. The law as built is the owner's and the
mathematician's form exactly (pseudoscalar column, axial body, Wu's sign,
strict hemisphere, the family's home, the filter exact), covariant under all
48 and parity-breaking under exactly the 24 improper elements where a
birth has an axis and a handed product; the gate set and Bell's integers
are untouched; the four deviations are correct derivations, not defects.
