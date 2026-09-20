Read at e97bee54 (the branch binding-v1 on b8620d8f); the four should-fix applied at 3f4438d2 (the fact of the run, the momentum pin reported outside, the three readings stated, B2's key pending the one click).

# Physics-rule review of binding-v1 (branch `binding-v1` at e97bee54, three commits on b8620d8f)

Read-only, 2026-09-20. Worktree `/home/user/Universe24/.claude/worktrees/binding`
confirmed: `e97bee54` (docs), `f0282185` (worlds, runs, EXPERIMENTS, VALIDATION),
`1fb0ca52` (the rule and tests) on `b8620d8f`; 21 files, +1158/-25. Evidence
used: the diff, the design (`docs/designs/binding_v1/DESIGN.md`, `integers.txt`),
records 113/115/132/137, BEAM_LAW sections 2, 3, 5, notes 31 (vii)-(ix), 33, 40,
ARCHITECTURE's local integer operation contract, LOCALITY-1; `tests/test_binding.py`
run (4 passed) and `tests/test_repository_language.py` run (14 passed); my own
in-process replays of B1 (40 intervals), B3 (25) and B2 (30) from the shipped
worlds; a parse of all 159 shipped worlds for `binding`; `git merge-tree`
against the current `origin/main` (`4f94a86f`, PR #385 the hand merged). No
file of the repository edited, nothing committed, `tools/check.py` not run.
File paths below are relative to the worktree.

## 1. The rule as built against the design's candidate A

**Match, item by item (NOTE, pass).** One condition on one verb: `_contact`
gives once per contact, at the first hand-over whose rule is `measure`
(`src/event_universe/events/engine.py:710`, `:726-728`; a `rerelease` occupant
never triggers it). Every paid family the giver holds: the loop at `engine.py:776-779`
skips free families and the body's own. `held // h` units of content h as one
row: `engine.py:779` (`units`), `:781` (`content = units * quantum`), the row
appended with `amount = units`, `content = h`, `age = 0`, the body's phase and
number, no record (`engine.py:800-812`). Away from the occupant: `engine.py:774`.
The recoil on the giver: `engine.py:791-793` (minus the born label). `held mod h`
kept: `engine.py:794` lowers `held` by `units x h` only. The fates untouched: no
change to the tables, the walk, the border or the lamp (the diff touches only
`_contact`, `_give`, the heading table at `engine.py:145-153`, `world.py` and
`run.py`).

**"Opposite to the refused step" = "away from the occupant": proved.** The
drive fires `(axis, momentum, stepped)` with `stepped` the step's sign
(`engine.py:83-114`, `step_axis`); `_move` sets `port = 2*axis + (0 if sign > 0
else 1)` and `destination = adjacent_node(origin, port, ...)` (`engine.py:552-554`);
`PORT_HEADINGS` (`src/event_universe/core/game_board.py:20-27`) is `+x, -x, +y,
-y, +z, -z` in port order, so the destination is `origin + step x e_axis`. The
occupant is at the destination (`engine.py:609-613`: the occupants are read from
the moved set at the destination). The heading `headings[(axis, -step)]`
(`engine.py:774`) is the unit vector `-step x e_axis` (the table is built from
the six unit vectors of `world.directions`, `engine.py:149-153`, which always
holds them at indices 2..7, `world.py:1162-1164`). Hence the row's first Link
is `origin - step x e_axis`: the Node on the far side of the giver from the
occupant. QED.

**The momentum-sign form was a defect and the step-sign form is its
correction, not a new choice (NOTE).** The design says "opposite to the refused
step, away from the occupant" (DESIGN section 1, the boxed rule). Under the
signed drive (record 126) the step's sign follows the drive's signed history,
not the momentum's current sign; my B1 replay shows n at tick 16 with momentum
+270 720 after p's hand-over and its step -x (contact record `(16, 2, 1, axis 0,
component 270720, given 2, momentum [-128, 0, 0])`). The momentum's sign would
have sent n's row on -x into p. The first build's reading caught it; the
correction restores the design's letter. `_contact`'s own hand-over still uses
the momentum's sign (`engine.py:706`), the law as it was; only the give reads
the step. Correct.

**Three readings of the design the implementer had to make (NOTE, all
admissible, all now stated in note 40):**
- (i) "every paid family it holds" is built as "every paid family other than
  its own" (`engine.py:777`; `world.py:1035`). A measured event's own content
  sits in `held[own]` (`world.py:2129-2130`: `held[family] = amount`), so
  without the exclusion a lamp refused a step would give its whole stock. The
  design's F2 (a lamp's own content is released by its clock; a held paid
  family of another name is content carried) supports the exclusion; it is
  the design's intent, not a new law. Tested in (d) (`tests/test_binding.py`,
  the `h` body).
- (ii) `given` on the record is the content summed over the paid families
  (`engine.py:814-815`), where DESIGN section 3 says "the content given per
  family". With one paid family they coincide; with two the record loses the
  split (the books keep it per family). NOTE; say it in note 40 or make it
  per family before a world holds two.
- (iii) An occupant whose share is 0 is skipped before the give
  (`engine.py:720-721`), and a body on a set of Nodes gives its row at its
  centre `origin` only (`engine.py:800`), not apportioned over its Nodes as a
  lamp's release is (`nature_beam.py:3626-3641`). No shipped world reaches
  either; note 40 says "whole, on the one heading" without naming the centre.
  NOTE.

## 2. Genericity and locality

**Pass.** `_give` reads `definition.free` and `definition.quantum` (keys), the
giver's own `held`, `phase`, `number`, `momentum`, the refused step's axis and
sign, the giver's Node, and the static heading table; no family name, no
partner content, no shape, no memory of partners, no host total. Work is one
row per paid family held per contact, O(families) for fixed K. Nothing is
kept at a Node: the row goes to the family's store as a lamp's row does
(`engine.py:800-812`), the remainder stays on the body's own `held`. The row
is born at the giver's Node with age 0, in `_move` after the interval's
`nature_beam` (the walk, the reads, the releases, the border: `engine.py:358-381`),
exactly as a lamp's release is born at age 0 in step 5 after the walk
(`nature_beam.py:3643-3654`): first Link at the next interval, the border at
age 3 three intervals later. Give at 16, click at 19 in B1; give at 3, click
at 6 in test (a). Age 0 is right.

**SHOULD-FIX (the identity and the record key follow the load, the rule
follows the run).** The rule fires on the run-time `held` of any body; the
record's `given` key is written only when `world.binding` is true
(`engine.py:742-743`), and `run.json`'s `hypotheses` is computed at load
(`world.py:1028-1036`, `run.py:117`). A body of a free family that TAKES a paid
row under the keys' `measure` (the design's own fate (c), tested: the third body
holds `bond` 2 after the take) holds paid content from then on and gives it at
its next refused step, in a world whose `run.json` carries no `binding-v1` and
whose `contact` records carry no `given`. Physically consistent (the content
moves on, the books close), but the identity and the record would be silent.
My parse of all 159 shipped worlds: `binding` is true only for the three
series N worlds; the shipped layouts with a paid measured event beside a
mobile free body and a second free body are `catalog/sun_planet`, the four
`hubble/*` worlds and `weak/j3_deuteron*`, all in or beside the gate set and
15 of 15 byte-identical, so no registered record is affected today. Fix: let
the engine raise a flag at the first give and write `binding-v1` and `given`
from that fact (or write `given` whenever `given > 0`), and state the
run-time scope in note 40 and MIGRATION ("a body that takes paid content
gives it at its next contact").

## 3. Integers and the books

**Pass.** `held // h` and `held mod h` exact with h >= 1 (the parser's
`quantum`); the remainder's owner is the body's existing bounded `held`
(ARCHITECTURE: "declare the existing bounded remainder owner"): declared in
note 40. The label is formed by `momentum_labels` with `free=False`
(`engine.py:787-789`), the product `content x amount x |u_d|` checked before it
is formed (`nature_beam.py:826-866`); the recoil and the giver's momentum go
through `bounded` (`engine.py:791-793`). For the register's contents the
label is Q x held = 64 x 2 = 128, far inside; the general bound is the label's
2^62 refusal, loud, naming the Node. The check runs before `held` and the
ledger are touched (`engine.py:787` before `:794-799`), so a refused label
commits nothing of the give. NOTE: it runs after the hand-over of the same
occupant (`engine.py:717-719`); a refusal ends the run as every `bounded`
refusal does, the same practice as elsewhere in the engine.

The books: `spent`, `content_released`, `transit_released`, `transit_momentum`
booked exactly as a lamp's release books them (`engine.py:795-799` against
`nature_beam.py:3611-3614`, `:3641-3643`, `:3655`), the row's label on the
transit line until the border books `lifetime_content` and
`lifetime_momentum` (`nature_beam.py:3740-3750`); `books(recount=True)` counts
the store and closes at every tick in my replays of B1, B3 and B2 and in every
tick of the tests. The mass read 3673 = 3677 - 4 is the measured lines'
`current` summed (p 1834 + 0 + 1, n 0 + 1837 + 1): `Measured.content` is
`sum(held)` (`measured.py:336-337`), so the reader's gravity charge falls with
the give and the `read` lines show it (section 4). `given` records units x h
(content), the same unit as the record's `component`'s neighbour fields and
the books' `spent`; the click record's `content` is `amount x content per unit`
(`nature_beam.py:3782-3785`), so "amount 2, content 2" on the record is the
design's "amount 2, content 1 per unit": one convention, consistent.

**SHOULD-FIX (a design pin outside, unreported).** DESIGN section 2 pins
"momentum: measured + transit + escaped = 0" (DESIGN.md:195). In my B1 replay
the sum is +270 720 on x from tick 16 on (`measured` 270 720, `transit`
-23 645 864, `escaped` +23 645 864 at tick 40), and B3's sum is likewise
nonzero. The cause is not the give: before the give p reads n's rows (1838
free units) with its gravity charge 1837 while n reads p's rows (1835) with
1840, a gap of 6 x 3008 = 18 048 per interval over the 15 pushes from tick 2
to 16 = 270 720 exactly, the third-law gap of record 126 made visible by a held
paid family that counts in M_A (note 31 (viii)) but is never released; after
both gave the two pushes are equal (310 945 171 840 both) and the gap stops.
The README's pin table (`examples/events/binding/README.md`, "The
expectations") did not carry this design pin and EXPERIMENTS N says "every
reading inside its pin". Report it as a reading outside the design's pin with
its cause (a property of held paid content that predates the branch; the give
removes it), in the README, EXPERIMENTS N and note 40.

## 4. The readings against the design's pins (DESIGN sections 2 and 4)

My replays confirm the implementer's readings to the integer:
- B1 (40 intervals): first contact tick 16 for both bodies, p hands
  4 664 343 438 720, n hands 270 720, `given` 2 each, the recoils (+128, 0, 0)
  and (-128, 0, 0) on the tick-16 records, 0 on the tick-31 hand-overs; two
  `bond` clicks at tick 19 on the border `lifetime` at (8, 10, 10) number 1
  momentum (-128, 0, 0) and (13, 10, 10) number 2 momentum (+128, 0, 0),
  amount 2, content 2 each; `bond` books initial 4 = spent 4, released 4 =
  escaped 4; the push on p 310 956 229 248 at tick 10 (n rows 10 150 703 552 +
  nuclear 300 805 525 696) and 310 945 171 840 at tick 20; on n
  -310 956 211 200 and -310 945 171 840; no step; held p (1834, 0, 1, 0), n (0,
  1837, 1, 0), the mass read 3673. The escaped content 4 is the same under
  either content convention (2 clicks x 2 units x h 1).
- B3 (25 intervals): gives at 15 (p1, n2, n3) and 16 (p4), four clicks at 18
  ((8, 10, 10), (8, 11, 10), (13, 10, 10)) and 19 ((11, 13, 10)), escaped 8,
  mass read 7346 = 7354 - 8, the ratio 2.0 to B1's 4: the stated failure
  against nature's 12.72, nothing tuned (one declared width, `BOND_HELD = 2`,
  `make_worlds.py:47`).
- B2 (30 intervals): no contact, no `bond` row in the store, no `bond` click,
  held (1834, 0, 1, 2, 0, 0); the lamp clicks `light` only. The design's "the
  lamp is blind to the held content" holds by construction: the crowd counts
  the free rows, and the held `bond` is never released.
- The pp threshold prediction (7111 to 7112, DESIGN section 1) was not run and
  no pp world is in series N: it stays a prediction of the design, unread.
  Say so in EXPERIMENTS N (it is stated in note 40 and HYPOTHESES 23 as a
  prediction). NOTE.
- The design's "about tick 16" for the first contact is met exactly.

## 5. The register

- The gate set 15 of 15 byte-identical (VALIDATION, the branch's table) is
  consistent with the code: with `world.binding` false no record gains a key
  (`engine.py:742`), and `_give` appends nothing for a body whose paid `held`
  of another family is 0. The argument "no registered world holds a paid
  family other than its own" is confirmed by my parse of all 159 shipped
  worlds (only the three series N worlds). Its run-time hole is section 2's
  SHOULD-FIX, not observed in any registered record.
- `bond_family` in `entities/families.json` and `make_definitions.py`
  (NOTE, acceptable under record 113): one canonical definition per family,
  referenced by the worlds through the generator, the definition of a family
  alone admitted; the three worlds are generator-made and reference it. It is
  a new row in the shipped definitions with no measured event, changing no
  other world (the definitions are optional and merged by name).
- **SHOULD-FIX at the merge (B2's `amplitude: true`).** `make_worlds.py:110`
  sets the key and `proton_bond_lamp.json` carries it. Record 137 (1) deletes
  the key with the one click, and the parser refuses unknown top-level keys
  (`world.py:1098`, `WORLD_KEYS` at `:389`): once the one click lands, B2 is
  refused at load unless the one click keeps the key as accepted-and-ignored.
  The generator must drop the line, B2 be regenerated and re-run, and its lamp
  pin re-read: the lamp becomes a record lamp by default and record 135 says
  the seven lamp worlds' integers changed under the record form, so "2993
  gathers, 2961 x 8, 32 x 7" is I7's old-form integer and will move with
  I7's re-registration. B2's binding pins (no contact, no `bond` row or
  click, `held.bond` 2 at 3000) do not depend on the lamp's form and should
  survive; VALIDATION's B2 digests will not.

## 6. The documents

- English throughout the added lines (no non-Latin letters; the language
  gate passes); no `board`, `lattice`, `grid` or `Site` in any added line
  (the `lattice` in ENTITY_CATALOG's alpha row is pre-existing context, not
  this branch's). No HIGHLIGHTS or LOG edit on the branch: correct (the
  record of the run and any decision are the Boss's and the owner's to add).
- **SHOULD-FIX (note numbering and the merge).** Note 40 says "numbered 40
  because 39 is the one click's, landing in parallel" (`docs/BEAM_LAW.md:2811`).
  On `origin/main` note 39 is the hand's (`hand-v1`, PR #385 merged at
  `4f94a86f`); the one click has no number yet and will need 41. Fix the
  parenthesis at the merge; 40 itself is free. HYPOTHESES: the branch adds
  "## 23." (`docs/HYPOTHESES.md:966`) and main's 23 is the hand: renumber to
  24 (no added line cites the entry by number; only the heading and the
  commit message of `e97bee54` say 23). MIGRATION:
  both sides insert at the top (`docs/MIGRATION.md:9`); VALIDATION: both
  insert after the preamble (`docs/VALIDATION.md:14`); ENGINE and BEAM_LAW
  conflict at the same insertion points. `git merge-tree origin/main
  e97bee54` reports conflicts in BEAM_LAW, ENGINE, HYPOTHESES, MIGRATION and
  VALIDATION; `world.py` auto-merges (`BINDING_RULE` after `MEETING_RULE`,
  the hand's constants elsewhere). Textual, no physics in the conflicts.
- ENGINE (the contact's give, the record's `given`, the identity without a
  key), MIGRATION, HYPOTHESES 23, TEST_EXPECTATIONS ("The binding that costs
  content", the integers of (a) to (d) match the tests and my reading of
  them), ENTITY_CATALOG (the deuteron row and the `bond` name row),
  EXPERIMENTS N, `examples/events/README.md` and `binding/README.md`: consistent
  with the code as built, including the own-family exclusion and the step's
  sign. NOTE: DESIGN section 5 still says "BEAM_LAW note 38" (the design's
  guess, read-only; superseded by 40) and MIGRATION's first sentence says
  "`contact` records gain `given`" before qualifying it two sentences later;
  acceptable.

## 7. Verdict

MERGEABLE AFTER the listed SHOULD-FIX: (1) the identity and the `given` key
from the run-time fact (or the run-time scope stated), (2) the design's
momentum pin reported as outside with its cause, (3) B2's `amplitude` key
dropped and B2 re-run when the one click lands, (4) note 40's "39" sentence
and HYPOTHESES 23 -> 24 at the merge onto the hand. No BLOCKING finding: the
rule is candidate A to the letter, local, integer, books-exact, generic, and
my replays reproduce every pinned integer of B1, B2 and B3.
Merge order: rebase onto current `origin/main` (the hand landed: five doc
conflicts, textual) and resolve; then, if the one click lands first, expect
B2 refused at load (regenerate without the key, re-run, re-pin the lamp's
gathers against I7's re-registered form, redo B2's digests) and note 41 for
the click; if binding lands first, the one click's PR must regenerate B2 and
carry the lamp's new integers. Either way the B1 and B3 records and digests
should not move (no lamp, no `amplitude`), and the gate set should be
replayed once more against the merged tree.
