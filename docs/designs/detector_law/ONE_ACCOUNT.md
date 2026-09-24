# One account in four layers: the five gaps the writer read between the engine and the paper, each re-read against the code, the law that decides it, and what changes where (the chief physicist, 2026-09-24, 05:20Z, on the Boss's order of 04:55Z on the model owner's word relayed by the writer; docs only, no run, no pin moved)

The model owner's word (through the writer, 04:46Z; the Boss's order of
04:55Z; the log's record and the Highlights 5.4 clause are the Boss's):
docs/ALGEBRA.md, docs/HIGHLIGHTS.md section 5.4, the engine
(`src/event_universe`) and the paper must agree EXACTLY, one account in
all four. The writer read five gaps between the engine on main (a5e80449
and 6b8ed356) and the paper (paper-48 at 47b3abd2) and changed nothing.
This page re-reads each gap against the code at the builder's head
af071b3f (PR 1068, detector-law-build-2, open) and at main 6b8ed356, and
against the paper's source `paper/general_formula/main.tex` at 47b3abd2,
with line numbers; names the account that is the law by the owner's
decision in Highlights 5.4 with its record, or writes QUESTION FOR THE
OWNER for the 09:00 page with the two accounts and a recommendation; and
says what changes where. No gap is settled by my own word and none by a
silent change of the code or the paper; Reviewer 3 reads this page
adversarially; the builder gets the code lines and the writer the paper's
sentences from the Boss as one order. Reviewer 3's own reading of the
five gaps at af071b3f reached me through the Boss at 05:05Z after the
first version of this page: (a), (b), (d) and (e) right as facts, (c)
stale (built at af071b3f). His read of 926bdd93 (through the Boss at
05:30Z) and of 9888b7e8 (through the Boss at 05:45Z, superseding the
first on rows (2) and (5)): the five facts stand, no gap settled by a
silent law change, no pin moves; rows (2) and (5) stay QUESTIONS FOR THE
OWNER, row (2) named as the name clash inside ALGEBRA.md and row (5) as
a question on the paper's sentence, not on the law; rows (3) and (4)
corrected on his lines; all folded here.

## The five gaps at a glance

| Gap | The fact, re-read | The law that decides it | What changes, where |
| --- | --- | --- | --- |
| (1) the cell chosen by u | the paper and the engine agree on the cell rule (u selects the cell through the rung) and on the stamp (the count and the birth stamp); the engine's gather line carries one more field, `u` | the wheel (record 180), the inputs (record 189), the click (record 1414), the six lines (records 1647 and 1648) | nothing in the code's cell rule and nothing in the paper; `u` on the gather line and on the `records` reading labelled HOST in ENGINE.md; the reader of record reads `chosen`, `birth`, `click` |
| (2) the pointer's form | the paper carries two forms: Definition 3 (251) and the read-out paragraph (683) say the receiver's own record's MOTION (the engine's, line 1211 for a set's Port and 872 for a block's response; ALGEBRA.md 8.6's); items (5) and 117, the caption and the panel label say the norm of the pair, ev(f)'s square, X^2 + Y^2; Definition 3's line 255, "the same form on the record's pair of levels", is the click's WEIGHT (the cell, Bell's J^2), not the pointer | QUESTION FOR THE OWNER, named as the NAME CLASH inside ALGEBRA.md (Reviewer 3's word): 2.5 calls (X, Y) = E f "the pointer" and its norm X^2 + Y^2 = f^T G f "the weight" for the ladder (the ray law's click frame, the source of the paper's 67, 117, 72 and the panel label), while 8.6 calls the motion-squared accumulator "the pointer" against the record's norm at the rung; the engine uses ONE currency for both (the ladder's weights are the pointers, `_click`, motion squared); recommendation (I), the pins' form | on his word: under (I) the paper's label and three phrases, a clause naming the weight against the pointer (the writer's), one clause in ALGEBRA.md 2.5 or 8.6 resolving the clash (mine); under (II) the pins re-derived before any run and the engine's two lines; nothing runs on either before his word |
| (3) the linear form S[k] | in the code at af071b3f (`_sine_table` 885, `read_pair` 1243, `_split` 1312); not on main because PR 1068 is open; `read_phase` (1622, `nearest_phase`) called by two tests and by nothing in the law's path | the groups' one account (record 1547), by the algebra (record 1421), section 14 on main (record 1545), the clock clause (record 1543) | PR 1068's merge (the Boss); `read_phase` kept, labelled the GAMEBOARD diagnostic its docstring names, or deleted with its two tests, on the owner's word; nothing in ALGEBRA.md or the paper |
| (4) the default path | `run.py` runs the old ray law unless `detector_law: true`; a block needs `massive_record: true`; the old law is 10000 lines, 332 example worlds and 95 test files | the owner's words of 2026-09-22, records 871 and 894 ("old code goes", "delete old code"), and of 04:53Z today ("throw out old code from the engine", relayed 04:56Z; the Boss's record to be written); Highlights item 10 amended by the Boss on it | the builder's removal PR, after the pin runs (my recommendation, Reviewer 3's too); dropping `detector_law` and `massive_record` as keys changes the world-file contract and every GO world carries `detector_law: true`, so that PR carries its worlds and the full gate (Reviewer 3's line); one Highlights clause (the Boss); nothing in the paper, which names one law; the 09:00 line on the old worlds and tests |
| (5) the block's click | the engine's two click lines: `_block_clock` (807 to 846) writes a `click` event per count, the body's self-click, and `_book_response` (861 to 881) stamps the foreign record's rung click with that count; the paper's Definition 3 (254) stamps the rung click with the body's count and does not merge the two; the writer read where the pointer is stored as whose it is | QUESTION FOR THE OWNER on the paper's sentence at Definition 3 (254), not on the law (Reviewer 3's word): (I) the count advancing at each click has no record and no map; (II) the body's count its own cycles and the click light's rung is the engine's, ALGEBRA.md 8.6's and Highlights item 7's (record 394); a body receiving no light has a clock under (II) and none under (I); recommendation (II) | under (II) nothing in the engine, ALGEBRA.md or Highlights; the paper's sentence at 254 and a clause naming both click lines (the writer's); under (I) every pin in a body's count is void |

## (1) The cell chosen by u

(a) THE FACT, re-read. The engine at af071b3f, `detector_law.py`:
`_click` chooses the cell by the record's residue, `chosen =
cell_of(weights, self.wheel, live.u)` (line 1423), the weights the
pointers per cell; the gather line it writes carries `chosen` (the
cell), `birth` (the record's birth interval, 1466), `click` (the chosen
cell's first rung, 1470 to 1473; `click_at` says "rung" or
"completion", 1479), `clock` and `clock_source` (the body's own count
where the cell is a block's or a set bound to one, 1483 to 1499), and
`u` (1446); the `records` reading carries `u` too (1781). The same on
main 6b8ed356 (1105, 1128, 1146, 1396). The paper at 47b3abd2:
Definition 3 (`main.tex` 249 to 266) says the click is "stamped with
that count and the record's birth stamp" (254) AND "the birth wheel's u
in Z_N, the lamp's phase at the birth, selects one cell through the rung
on the cumulative weights" with the rung's equation (259 to 263); item
(6) of the law's list (68): "What the clicks produce. A list of triples,
the Node, the detector's own count and the record's birth stamp".
CORRECTED: the paper and the engine agree on the cell rule and on the
stamp's content; the gap is one field, `u`, that the engine writes on the
gather line and on the `records` reading beside the stamp's fields.

(b) THE LAW. The birth wheel is the law's generic vector form (the
owner's yes, record 180) and W is among the inputs of kind 1 (record
189); the click is the evaluation at the declared wheel (the owner's
word, record 1414); the six lines of the order channel's solution (the
owner, 04:18Z, record 1648; the Boss, 04:14Z, record 1647) say the click
is stamped with the count and the birth interval, NEVER the residue, the
reader of record reads the click lists per set, and the gather line is
HOST. My word on the Boss's reading: it is mine. The cell chosen by the
record's residue u is the law as declared (u is Bell's lambda, born with
the record; the order channel hides only the ORDER of the births, item 8
of DECLARATIONS.md section 2); what the six lines forbid is u in the
STAMP and in any detector reading. So gap (1) resolves as a label, not a
change of the cell rule.

(c) WHAT CHANGES WHERE. ALGEBRA.md: nothing (8.6 already: the click line
carries the body's own count and the light record's birth stamp).
Highlights 5.4: nothing (the six lines' clause is the Boss's, record
1648). The engine: nothing in the cell rule; the builder's line is a
documentation line in ENGINE.md's "The detector's readings by type": the
gather line's `u` and the `records` reading's `u` are HOST (the diagnostic
E_N's input), never a field of a detector reading; and the reader of
record of the Bell rows reads `chosen`, `birth` and `click` and nothing
else (DECLARATIONS.md section 2 item 8). The paper: nothing; item (6) and
Definition 3 stand as written.

## (2) The pointer's form

(a) THE FACT, re-read. The paper's Definition 3 (251): "the detector's
pointer accumulates its own record's MOTION across its cells in the
units of the conserved form", and the click "W x (the pointer) >= (the
record's norm)" (253). The paper's item (5) of the law's list (67), the
paragraph "The detector and the click" (328) and Figure 1's caption (72)
say "the quadratic form of the record's VALUES in its cells crosses W",
"the record's quadratic form crossing the rung"; the label of the
figure's fourth panel reads X^2 + Y^2 (the writer's report of
`groups_figure.py`; I read the caption and the text, not the figure's
script). ALGEBRA.md 8.6 (2695 to 2720): "the block's pointer accumulates
its own record's motion across all its cells, in I's units (DESIGN.md
2.1, the Port's factor: the pointer books in the units of the conserved
form, the design's counting form)". DESIGN.md section 5 (394 to 403):
the static level is zero in the motion and a travelling train is not;
the build measured it on the chain, "with a^2 no completion"; "a Port
books the motion squared" (Reviewer 3's line). The engine at af071b3f: a
set's Port books `motion = ghost - live.ports[index]; offer += motion *
motion` (1205 to 1211; "a wave moves the receiver, a static level ...
does not"); a block's response books `value = sum over the block's mask
of (response.now - response.before)^2` (872). CORRECTED: the
paper's Definition 3, ALGEBRA.md 8.6 and the engine agree: the pointer
books the motion squared, the first difference squared, of the
receiver's own record (a block's response; a set's Port ghost), summed
across its cells and over the intervals; the gap is the figure's label
(X^2 + Y^2, the two levels' squares, a form that does not vanish on a
static level, which DESIGN.md section 5 measured as "no completion")
and the phrase "the record's values" in three places, which reads as
the levels and not their motion. The paper's theorem of section 5 (the
read-out a positive quadratic form on the lattice, 498 to 572) is not
touched: (Y - X)^2 is one.

(b) THE LAW: QUESTION FOR THE OWNER, named as Reviewer 3 names it (his
read of 9888b7e8, superseding his read of 926bdd93): a NAME CLASH inside
ALGEBRA.md, not two accounts of 8.6. ALGEBRA.md 2.5 calls (X, Y) = E f
"the pointer" and its norm X^2 + Y^2 = f^T G f "the weight" for the
ladder (the ray law's click frame; the source of the paper's item (5) at
67, of 117 "ev(f) with its norm |ev(f)|^2 at a detector, the one
read-out", of the caption at 72 and of the fourth panel's label), while
8.6 calls the motion-squared accumulator "the pointer" against the
record's norm at the rung (the engine as built: a set's Port 1211, a
block's response 872; DESIGN.md sections 2.1 and 5; the paper's
Definition 3 at 251 and the read-out paragraph at 683); the engine uses
ONE currency for both, the ladder's weights ARE the pointers (`_click`:
`weights = [(p, 1) for p in live.pointers]`), the motion squared. The
owner's words name the click (record 1414) and the algebra as the judge
(record 1421), not which of the two named forms the pointer of the rung
books. THE TWO FORMS: (I) THE MOTION SQUARED of one column, (a_now -
a_before)^2 of the receiver's own record per cell per interval, summed
across its cells and over the intervals, with which the light clock's
218 +- 2, R2's 108 / 247 / 72 and rows 4a's and 4b's readings in a
body's count were derived (`coupled_mode_pins.py`, the ledger's unit);
(II) THE PAIR'S NORM X^2 + Y^2 of 2.5 (the conserved form I on the two
levels, 8.2). A THIRD PLACE, the writer's to name: Definition 3's line
255, "the same form on the record's pair of levels", is the click's
WEIGHT (the cell's, Bell's J^2 of the joint pointer), not the pointer of
the rung. THE EXPECTATION, Reviewer 3's stated precisely and mine: each
form measured against ITS OWN norm crosses the rung at about the same
interval for a travelling character; the forms themselves differ by the
factor kappa^2 per interval (about 0.14 at 12 Links per period), which is
why a level booked into a motion ledger overbooks, and a standing
residual, zero in (I), is counted by (II). MY RECOMMENDATION (I), his
too: a static level (the rule's zero-frequency mode, which no receiver
takes) is zero in it, and DESIGN.md section 5 measured that with the
levels' squares a record on a board with a residual never completes
("with a^2 no completion"); (I) moves no pin; (I) is a positive
quadratic form on the pair, so the paper's read-out theorem (498 to
572) stands under it. If the owner chooses (II), the pins of the light
clock, R2, 4a and 4b are re-derived before any run (a derivation before
a run is not a pin moved) and the engine's two lines change; nothing
runs on either form before his word.

(c) WHAT CHANGES WHERE, after the owner's word. Under (I): ALGEBRA.md
one clause resolving the clash, mine (in 2.5 or 8.6: "the pointer of the
rung books the motion squared, (a_now - a_before)^2 per cell per
interval, in the same currency as the ladder's weights; the norm X^2 +
Y^2 of 2.5 is the click's weight of the ray law's frame; never the
levels' squares (DESIGN.md section 5: with a^2 no completion)");
Highlights 5.4 the owner's line, the Boss's clause; the engine nothing;
the paper (the writer, on the Boss's order): the fourth panel's label to
"(a_now - a_before)^2 across R: the record's motion", in item (5), in
117, in the caption and in the paragraph at 328 "the quadratic form of
the record's values" and "ev(f) with its norm" to "the quadratic form of
the record's motion, (a_now - a_before)^2 summed across its cells", at
Definition 3's line 255 one clause naming the pair's form as the click's
weight, the cell's, against the pointer of the rung; Definition 3's line
251 and 683 unchanged. Under (II): the engine's two lines (1211, 872) to
the pair's form, the pins re-derived, Definition 3 and 683 to the pair's
norm, ALGEBRA.md 8.6 and DESIGN.md sections 2.1 and 5 rewritten.

## (3) The linear form S[k]

(a) THE FACT, re-read. At af071b3f the linear form IS in the code:
`read_pair` (1243 to 1262; the sine table `_sine_table` at 885; the
splitter's `_split` at 1312: Reviewer 3's names) applies "the table's
action on a record's pair at a Node by the linear form of
DECLARATIONS.md section 14 item 1
... the level A cos(phi + t) = (a_now S[k + t] - a_before S[t]) / S[k] at
the turn t, S the sine table and k the interval's own whole step of the
record's clock (`by_clock`), one division", refusing a clock step whose
sine is 0 (1259 to 1262); the sine table `phase_sines` is imported (70)
beside the cosine table; the lamp's drive (`_phase` 1035, `_drive`
1040) inserts the character's real part by the cosine table, which is
the insertion and not a rotation, as ALGEBRA.md 1.7 has it; `read_phase`
(1622 to 1640, `nearest_phase`) has no caller in the law's path at
af071b3f; two tests call it (`tests/test_detector_law_tables.py` line
84, `nearest_phase` in its lines 62 to 101; `tests/test_massive_record.py`
line 1316): the nearest angle, the diagnostic that ALGEBRA.md 1.7 names
as GAMEBOARD (Reviewer 3's correction of my "dead code"). On main 6b8ed356 none of this exists (the writer's
fact is main's): PR 1068 (18 commits, 53 files) is open. The paper's
"One group, two representations" (164 to 170, the boxed identity, citing
ALGEBRA.md 1.7, DECLARATIONS.md section 14 and record 1543) and
ALGEBRA.md 1.7 (349 to 420) agree with af071b3f. CORRECTED: the gap is
main against the builder's branch, plus one dead function.

(b) THE LAW. The groups' one account in ALGEBRA.md and Highlights on the
owner's word (record 1547; ALGEBRA.md 1.7 "on the model owner's word");
by the algebra (record 1421); section 14, the linear form, on main since
PR 1069 (record 1545); the clock clause k such that S[k] is large (record
1543). No question for the owner.

(c) WHAT CHANGES WHERE. The engine: PR 1068's merge (the Boss, on
Reviewer 3's read and green CI), and one builder line on the
owner's word: keep `read_phase`, labelled the GAMEBOARD diagnostic its
docstring names, or delete it with its two tests. ALGEBRA.md: nothing. Highlights 5.4:
nothing. The paper: nothing; the writer's table of the code's state cites
af071b3f until the merge and the merge SHA after it.

## (4) The default path

(a) THE FACT, re-read. `run.py` at af071b3f (93 to 95, the same on
main): `DetectorLawSimulation(world, ...) if world.detector_law else
NatureBeamSimulation(...)`; `world.py`: `detector_law` "a boolean, false
by default" (WORLD_KEYS), `massive_record` "off by default", a block
admitted under it alone (419 to 429, 826, 844); `detector_law.py`'s own
head (1 to 6): "Selected by the world key `detector_law`, beside the ray
law as built, which stays the default." The old law's extent on main:
`nature_beam.py` 6734 lines, `engine.py`'s NatureBeamSimulation 1808,
`meeting.py` 419, what `measured.py` (1118) serves only them; fifteen
old identities' keys in `world.py` (amplitude-v1, drive-b-v1,
centred-step-v1, atom-level-v1, covariant-readings-v1, bohr-v1,
columns-v1, weak-v1, meeting-v1, optical-v1, flow-link-v1, hand-v1,
binding-v1, massive-rows-v1, become); 332 of 367 example worlds and 95
of 99 test files under it; `detector_law.py` imports nothing from
`nature_beam.py` (only `cell_of` and `rungs` from `amplitude.py`, the
core modules and `world.py`). The paper names one law with its
implementation (106). CONFIRMED.

(b) THE LAW. Highlights item 10 (the identities on main: the law
beam-v1, every hypothesis key absent or false by default) is the
standing rule that made `detector-law-v1` a key beside the ray law; the
owner's words of 2026-09-23 (DESIGN.md) made the detector law the law in
force; the owner's words of 2026-09-22 (records 871 and 894: "old code
goes", "delete old code") and of 04:53Z today, "throw out old code from
the engine" (relayed to the Boss at 04:56Z; the Boss's record of it to
be written, records 871 and 894 the citation until then), decide this
gap: one law in the engine, the old ray law out. For the 09:00
page (the Boss's decision line, standing): whether the old worlds and
tests go to a history directory or are deleted, and WHEN: my
recommendation, after the pin runs, as the first engine task, one PR,
the full gate, Reviewer 3's read; not between now and the GO, whose
preflight and pin runs need a frozen engine the gate has seen.

(c) WHAT CHANGES WHERE. The engine (the builder's PR, on the Boss's
order): `run.py` runs one simulation; `nature_beam.py`, the
NatureBeamSimulation of `engine.py`, `meeting.py` and what `measured.py`
serves only them removed; the fifteen identities' keys out of
`world.py`; `detector_law` and `massive_record` no longer keys (the
law's own; a block admitted by its `side`), which changes the world-file
contract, so that PR carries every GO world (each carries `detector_law:
true` today) and the full gate (Reviewer 3's line); `amplitude.py`'s `cell_of`,
`rungs` and what `detector_law.py` uses kept; the old worlds and tests
to a history directory or deleted on the owner's word. ALGEBRA.md:
nothing. Highlights 5.4: one clause by the Boss on the owner's word
(item 10 amended: the law is detector-law-v1 with massive-record-v1, one
law, no key). The paper: nothing; its implementation citation points at
the cleaned engine's SHA after the removal.

## (5) The block's click

(a) THE FACT, re-read. The engine at af071b3f, `_book_response` (861 to
881): "The click's pointer at a clock body: the response's motion across
the cells (the evaluation E of the object's record across R) added to
the light record's pointer for the block's cell, the first rung at 1 / W
of the record's norm stamped with the block's count": `motion =
response.now - response.before; value = sum over block.mask of motion^2;
light.pointers[cell] += value; light.absorbed += value; if
light.first_rung[cell] is None and light.pointers[cell] * wheel >=
light.norm: light.first_rung[cell] = self.tick; self.rung_counts[(light,
cell)] = block.count`. `_block_clock` (807 to 846): the block's total
record (its own and the responses light drives) summed across its cells,
one count per cycle at the sum's crossing from at most 0 to above 0
(verb D's comparison), a `click` line per count with its own count. The
gather line's `clock` is `rung_counts[(record, cell)]`, the block's count
at the first rung, with `clock_source` "measured:<n>" (1483 to 1499); a
receiver as built (a set bound to no block) stamps the interval. The
norm is the light record's, its insert's motion over the train
(`live.norm`, 843 to 848). ALGEBRA.md 8.6: the same two things, the
pointer the body's own record's motion across R against the record's
norm at the rung 1 / W "in the block's OWN clock", the click line the
block's own count (its mode's cycles, 8.3) and the birth stamp. The
paper's read-out paragraph (683: "the click is the evaluation (E) of a
body's own record on its cells at the declared rung W ... in the block's
own clock; the click line carries the block's own count and the light
record's birth stamp") and the paragraph at 328 say the pointer and the
rung as the engine has them. CORRECTED in part: the writer read where the pointer is STORED (one
integer per record per cell, on the record's `pointers` array) as WHOSE
motion it is (the body's response across R); that is no gap. The engine
has two click LINES: `_block_clock` (807 to 846) writes a `click` event
per count, the body's self-click, and `_book_response` (861 to 881)
stamps the foreign record's rung click with that count. The gap that
stands is on the PAPER'S SENTENCE (Reviewer 3's word on 9888b7e8): its
Definition 3 says at the click "the detector's count advancing, the
click stamped with that count" (254), which read literally makes the
count advance at the click.

(b) THE LAW: QUESTION FOR THE OWNER on the paper's sentence at
Definition 3 (254), not on the law (Reviewer 3's word). THE TWO
ACCOUNTS. (I) ONE MECHANISM: the body's count advances at each click
(the detector counts its clicks): Definition 3's "the detector's count
advancing" read literally; it has no record and no map. (II) TWO
MECHANISMS: the body's count is its own record's cycles across its cells
(the zero crossings of its sum, `_block_clock`), its clock, ticking with
or without light; the click is light's rung on the body's response
across its cells against the light record's norm, stamped with the
body's count at that interval (`_book_response`, `rung_counts`): the
engine's, ALGEBRA.md 8.6's ("the block's OWN clock ...; the click line
carries the block's own count (its mode's cycles, 8.3)") and Highlights
item 7's account (the detector's own count, record 394), with item 6
(the click, record 1414), and every pin in a body's count (the light
clock's 218 +- 2 in A's own cycles, R2's 108 / 247 / 72 in the blocks'
cycles, 4a's 42.364, 4b's per-record ratio). A body receiving no light
has a clock under (II) and none under (I). MY RECOMMENDATION (II), his
too: under (I) A's 218 would be a count of clicks, one per record,
which no map derived and item 7 excludes; under (II) nothing moves but
the paper's sentence.

(c) WHAT CHANGES WHERE, after the owner's word. Under (II): the engine
nothing; ALGEBRA.md nothing; Highlights 5.4 nothing (items 6 and 7 as
they stand); the paper (the writer, on the Boss's order): Definition 3's
"the detector's count advancing, the click stamped with that count" to
"the click stamped with the detector's own count, its own record's
cycles across its cells, which advance with or without light", and one
clause naming both click lines ("a body writes two click lines: its own
count's, one per cycle of its record across its cells, and the foreign
record's, at the first rung of that record's pointer on its cells,
stamped with the count then"); at 683 one gloss after "in the block's
own clock": "(its own record's cycles across its cells, not a count of
clicks)". Under (I): the engine's `_block_clock` replaced by a click
counter, every pin in a body's count re-derived before any run,
ALGEBRA.md 8.3 and 8.6 and Highlights item 7 rewritten on the owner's
word.

## For the 09:00 page

1. Gap (2), QUESTION FOR THE OWNER, the name clash inside ALGEBRA.md
   (2.5's "pointer" and "weight" of the ray law's click frame against
   8.6's "pointer" of the rung): the pointer of the rung books the motion
   squared of the receiver's own record (I, as built, the pins' form,
   the recommendation of Reviewer 3 and mine) or the pair's norm X^2 +
   Y^2 (II, the paper's items (5) and 117); on his word the writer's
   phrases, Definition 3's line 255 named as the click's weight, and my
   clause resolving the clash in ALGEBRA.md.
2. Gap (5), QUESTION FOR THE OWNER on the paper's sentence at Definition
   3 (254), not on the law: the count advancing at each click (I, no
   record, no map) or the body's count its own cycles and the click
   light's rung stamped with it (II, the engine's, ALGEBRA.md 8.6's and
   Highlights item 7's account; the recommendation of Reviewer 3 and
   mine); under (II) only the paper's sentence moves.
3. Gap (4): the old law's removal, its timing (after the pin runs, my
   recommendation, the Boss's and Reviewer 3's too) and the old worlds'
   and tests' fate (history directory or deletion): the owner's line,
   the Boss's decision line standing; the owner's words of 2026-09-22
   (records 871 and 894) and of 04:53Z already say "throw out"; that PR
   carries every GO world and the full gate.
4. Gaps (1) and (3): settled by the decisions cited; the changes are a
   HOST label, PR 1068's merge and the owner's word on `read_phase`
   (kept labelled, or deleted with its two tests); no physics moves and
   no pin moves.
5. THE LIGHT CLOCK'S BLOCKER (DECLARATIONS.md section 10 item 10): the
   emitter's ringing books the set's first rung at 141, the grace's end,
   on the builder's test (ac); declared: every emitter takes its own
   record's remnant after its train; the pin 218 +- 2 stands; the
   builder's line before the light clock's preliminary; Reviewer 3's
   read.
