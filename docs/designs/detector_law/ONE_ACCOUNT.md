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
sentences from the Boss as one order.

## The five gaps at a glance

| Gap | The fact, re-read | The law that decides it | What changes, where |
| --- | --- | --- | --- |
| (1) the cell chosen by u | the paper and the engine agree on the cell rule (u selects the cell through the rung) and on the stamp (the count and the birth stamp); the engine's gather line carries one more field, `u` | the wheel (record 180), the inputs (record 189), the click (record 1414), the six lines (records 1647 and 1648) | nothing in the code's cell rule and nothing in the paper; `u` on the gather line and on the `records` reading labelled HOST in ENGINE.md; the reader of record reads `chosen`, `birth`, `click` |
| (2) the pointer's form | the paper's Definition 3, ALGEBRA.md 8.6 and the engine agree: the pointer books the motion squared of the receiver's own record; the paper's figure label and three phrases say "the record's values" and X^2 + Y^2 | the click (record 1414), by the algebra (record 1421), ALGEBRA.md 8.6 carried; the unit DESIGN.md sections 2.1 and 5 | one clause in ALGEBRA.md 8.6 (mine); the paper's label and three phrases (the writer's); nothing in the engine; a one-line confirmation for the 09:00 page |
| (3) the linear form S[k] | in the code at af071b3f (the table's action, `_table_action`; the sine table imported); not on main because PR 1068 is open; one dead diagnostic function, `read_phase` | the groups' one account (record 1547), by the algebra (record 1421), section 14 on main (record 1545), the clock clause (record 1543) | PR 1068's merge (the Boss); `read_phase` and `nearest_phase` deleted or labelled a diagnostic with no caller (the builder); nothing in ALGEBRA.md or the paper |
| (4) the default path | `run.py` runs the old ray law unless `detector_law: true`; a block needs `massive_record: true`; the old law is 10000 lines, 332 example worlds and 95 test files | the owner's word of 04:53Z ("throw out old code from the engine"; relayed 04:56Z, the Boss's record); Highlights item 10 amended by the Boss on it | the builder's removal PR, after the pin runs (my recommendation); one Highlights clause (the Boss); nothing in the paper, which names one law; the 09:00 line on the old worlds and tests |
| (5) the block's click | the paper's Definition 3, ALGEBRA.md 8.6 and the engine agree: the rung test on the body's response's motion across its cells against the record's norm, stamped with the body's own count of cycles; the writer read where the pointer is stored as whose it is | the click (record 1414), the detector's own count (Highlights item 7, record 394), by the algebra (record 1421) | nothing in the engine, ALGEBRA.md or Highlights; one clause of clarity in the paper's Definition 3 (the writer's, optional) |

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
of (response.now - response.before)^2` (1870 to 1872). CORRECTED: the
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

(b) THE LAW. The click is the evaluation of the body's own record on its
cells at the declared wheel (the owner's word, record 1414); the
postulates and the paper go by the algebra (the owner's word, record
1421); ALGEBRA.md 8.6 carries the unit from DESIGN.md sections 2.1 and 5
(the conserved form's units, the motion squared; Reviewer 3's Port
factor; the build's measurement). No decision of the owner names the
unit by itself; it enters under records 1414 and 1421 through 8.6. For
the 09:00 page, one line, not a question unless the Boss reads 1421
otherwise: THE POINTER BOOKS THE MOTION SQUARED, (a_now - a_before)^2 of
the receiver's own record per cell per interval, never the levels'
squares; a static level moves no receiver. My recommendation: the motion
squared, as built, as 8.6 has it and as the paper's Definition 3 has it.

(c) WHAT CHANGES WHERE. ALGEBRA.md 8.6: one clause, mine, on the next
commit that touches the file: "the motion squared, (a_now - a_before)^2
per cell per interval, never the levels' squares a^2 (DESIGN.md section
5: with a^2 no completion)". Highlights 5.4: nothing. The engine:
nothing. The paper (the writer, on the Boss's order): the fourth
panel's label to "(a_now - a_before)^2 across R: the record's motion";
in item (5), in the caption and in the paragraph at 328, "the quadratic
form of the record's values" to "the quadratic form of the record's
motion, (a_now - a_before)^2 summed across its cells"; Definition 3
unchanged.

## (3) The linear form S[k]

(a) THE FACT, re-read. At af071b3f the linear form IS in the code:
`_table_action` (1244 to 1262) applies "the table's action on a record's
pair at a Node by the linear form of DECLARATIONS.md section 14 item 1
... the level A cos(phi + t) = (a_now S[k + t] - a_before S[t]) / S[k] at
the turn t, S the sine table and k the interval's own whole step of the
record's clock (`by_clock`), one division", refusing a clock step whose
sine is 0 (1259 to 1262); the sine table `phase_sines` is imported (70)
beside the cosine table; the lamp's drive (`_phase` 1035, `_drive`
1040) inserts the character's real part by the cosine table, which is
the insertion and not a rotation, as ALGEBRA.md 1.7 has it; `read_phase`
(1622 to 1640, `nearest_phase`) is defined and has NO caller at
af071b3f (the nearest angle, the diagnostic that ALGEBRA.md 1.7 names as
GAMEBOARD; dead code). On main 6b8ed356 none of this exists (the writer's
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
Reviewer 3's read and green CI), and one builder line: delete
`read_phase` and `core.phase.nearest_phase` (the owner's word of 04:53Z,
old code out) or, if kept for a diagnostic, name it so in ENGINE.md with
no caller in the law's path. ALGEBRA.md: nothing. Highlights 5.4:
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
force; the owner's word of 04:53Z today, "throw out old code from the
engine" (relayed to the Boss at 04:56Z; the record the Boss's), decides
this gap: one law in the engine, the old ray law out. For the 09:00
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
law's own; a block admitted by its `side`); `amplitude.py`'s `cell_of`,
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
paper's Definition 3 (251 to 254) and the paragraph at 328 ("the
evaluation (E) of the record on the detector's cells in the detector's
own clock; a body is a detector of itself, across its own cells"): the
same. CORRECTED: no gap in substance. The writer read where the pointer
is STORED (one integer per record per cell, on the record's `pointers`
array) as WHOSE motion it is (the body's response across R), and read
the body's cycle count as "a separate mechanism": it is the body's own
clock (Highlights item 7, the detector's own count), the stamp; the rung
test is the click (Highlights item 6). Two items, one account.

(b) THE LAW. The click (record 1414: the evaluation E of the record's
time series on the foreign object's cells at the declared wheel W); the
detector's own count (Highlights item 7, record 394); by the algebra
(record 1421). No question for the owner.

(c) WHAT CHANGES WHERE. The engine: nothing. ALGEBRA.md: nothing.
Highlights 5.4: nothing. The paper (the writer, optional, one clause in
Definition 3 for a reader of the code): "the pointer is kept per record
and per cell; its value is the body's response's motion across its
cells; the body's count is its own record's cycles, the zero crossings
of its sum across its cells, and the click is stamped with that count".

## For the 09:00 page

1. Gap (4): the old law's removal, its timing (after the pin runs, my
   recommendation) and the old worlds' and tests' fate (history
   directory or deletion): the owner's line, the Boss's decision line
   standing.
2. Gap (2): one confirmation line, the pointer's unit the motion squared
   under records 1414 and 1421 through ALGEBRA.md 8.6; a question only
   if the Boss reads those records as not covering it.
3. Gaps (1), (3) and (5): settled by the decisions cited; the changes
   are labels, a merge, a deletion of dead code and the writer's
   phrases; no physics moves and no pin moves.
