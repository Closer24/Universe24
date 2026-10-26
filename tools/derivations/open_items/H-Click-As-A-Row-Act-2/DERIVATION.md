# H-Click-As-A-Row-Act-2: is the click one of the Node's acts on the rows?

Hand H-Click-As-A-Row-Act-2 (blind derivation), 2026-10-26, on the head 62d8ce8f1 (a detached worktree; nothing under src or tests of the head touched; the fold built on a copy, src_cr2, and handed as cr2.patch). The owner's words of 04:1x and 03:3x, the four criteria (the 48, simplicity, Rule3 the one step, the generic form) and the four roads of 05:1x.

Verdict: A FINDING. The click's take is the write act's form at one Node (one carried division at the line's own wall of an exact numerator, the quotient `levels`, the remainder unmoved) and the three letters of the take are one act at a list of ends, measured bit for bit on the ten worlds (the log, the Node lines, the counts, the turns; the run back 10 of 10; 115 bits); it is not the write act of the interval (the taken line holds no write wall in the letter: 1,472 of 1,472 takes on ga2 fall on a line with none) and not Rule3's step (the step moves the before slot, the take does not), and the lay-back clause of EQ-S1 does not cover the birth's take without a course change (64 of 64 births on ga2 stand at a Node whose gap-0 current sums 0). The interval's list of acts does not fold by one; the close's list folds by two functions and 14 lines.

## Step 0. The unification candidates, in order of size, by the four roads

The neighbourhood searched: the close's take and lay (take.py, close.py, bodies.py) against the Node's acts on a line (node.rotate, node.write, rule3.carried_division) and the seed's lays (seed.py through node.lay).

What the letter holds twice, by name:
- The take's move on a line, spelled twice: `take.lay(..., line=k)` building a tuple of zeros with one count, and the write's `line.now = line.now + direction * q` (node.write); the same move spelled a third time in bodies' lay-back and a fourth in unclick's restore (both through lay's `line` branch).
- The take at ends, spelled three times: the birth's one take at one Node (`take_at` in births), the merger's take per end (`merger_take`, reading both ends before writing either), the body's take (`take_at` in bodies); the merger's refusal spelled once more (`refused` beside take_at's own `stop` entry, the same keys in the same order).
- The take's log fields, spelled twice: `take_line` for one end and `merger_take`'s summed form for two.

The candidates:

CR-C1 (the largest; road 4, Rule3): the click's take is the Node's write act, one carried division at the line's own wall; the interval's list of acts folds by one (the close's take is "the write at the taken line of the numerator levels times the wall"). Derived below; refused by the letter's state for `node.write` (no write wall on the taken line in two of the three letters) and held for the write's form at the line's rotation wall (CR-S1).

CR-C2 (road 1, the algebra; road 4, the generic act): the three letters of the take are one act at a list of ends, (Node, walls) pairs, every end read before any is written, refused by name at the first end that cannot pay: the birth's list one end of the children's walls summed, the merger's two ends, the body's one end of its unit. Built, bit for bit (CR-S2).

CR-C3 (road 1): one lay-back clause (EQ-S1) for every take alike, the birth's take laid back where the gap-0 current sums 0 as a credit's is (the Bell hands' candidate, The-Bell-In-The-Click_COMPARISON.md 1.5). Measured: a course change on ga2 (64 of 64 kept births at a Node with the net current 0), none on the hole and the chiral (0 of 24, 0 of 26). Not built; the change named for the owner.

CR-C4 (road 4): the birth's lay (re_now += A, im_before -+ B at the two ends) and the seed's four forms are one lay act with one form, a tuple of counts per line slot at a Node or over the board (`take.lay`); the take is no longer a spelling of it (its `line` branch struck). Built, bit for bit, inside CR-C2.

Road 2 (the matrix): the take acts on one line of one record at one Node by a count; the gram enters it only through fall_of's share, which is a reading and not an act; no second coefficient stands beside the first. Nothing found to fold by this road, said by name.

Road 3 (the cube): the take's move is one integer added to one slot, covariant under every image of the 48 as the slot is; the choice of line (CS4-S2, the largest now^2 - before^2) is the one threshold and stands. The 48 on the clicks measured below. Nothing found to fold by this road, said by name.

## Step 1. The algebra

What the acts do to a line (now, before, rem, wall; and where the row writes, wr, wwall):

- Rule3's step (node.rotate, forward): q, rem' = carried_division(total, w, rem); (now, before, rem) -> (q, now, rem'). Both levels move: the now slot to the quotient, the before slot to the old now.
- The write (node.write): q, wr' = carried_division(n, T, wr); (now, before, wr) -> (now + q, before, wr'). The now slot alone moves, by the quotient; the before slot stands.
- The take (take_at, the head): (now, before, rem) -> (now + t levels, before, rem) at the one Node, t the sign toward the before. The now slot alone moves, by the count; nothing else.

So the take has the write's shape and not the step's: one slot moved by an added integer, the before slot standing. The take is the write with the numerator an exact multiple of the wall: carried_division(levels * w, w, r) = (levels, r) for every r in [0, w), since (levels * w + r) div w = levels and the remainder is r. The exactness of the take (CS4-S2, nothing made) is the remainder's not moving: the numerator a multiple of the wall. The take is therefore the write act at the quotient `levels` at any wall, and "the exact take is the exact lay": one act (CR-S1).

Which wall is the line's own? The write act's wall is the line's write wall T, held by the lines that write: the carrier's ten, the shape-4 row's four, the emitter's re line (rows.write_walls: `[action, None]` for the plane at (den, den); `[None] * shape` for a plane with a gap). The take moves the emitter's re line or its im line (CS4-S2's choice) and, in the merger's letter, a gapped record's line: the im line and every gapped line hold no write wall. So the take cannot be `node.write` without a course change to the Node's state (a write remainder on every line: 98 integers per Node would grow). Every line holds its rotation wall w and its rotation remainder rem; the take as the carried division at the rotation wall of levels * w leaves rem unmoved bit for bit. This is the form built: `take.move(line, at, count)`: `q, rem[at] = carried_division(count * w, w, rem[at])`, `now[at] += q`. It is the write's form at the line's own wall, with the division's primitive and its remainder in the letter, and not a new act; it is not the interval's write act by name, because that act's wall is another.

The three letters of the take: on the head, `take_at(node, at, walls, rule, cause, rec)` is one function called from the birth (one end, the walls summed over the children), from the merger (`merger_take`: both ends read by fall_of, then take_at at each) and from the body (one end, its unit). The one form: `takes(node, ends, rule, cause, rec)`: fall_of at every end, the refusal at the first that cannot pay (the count `refused_stop += cause`, the log entry with fall, walls, row; the birth's cause the children's count at the Node, the merger's and the body's 1), then at each end the move, the Node's close counted, the momentum booked, the end's fields returned. For one end this is take_at's own order (fall_of read twice, deterministic; the second read after no write); for two ends it is merger_take's order (the first end's move changes now at the - end, the + end's fall_of reads its own now and the neighbours' before, so the second read is the first). Bit for bit by construction and measured.

The log's two shapes of the take (one end flat, two ends summed with `takes`) stay as `summed`: one function in place of take_line and the merger's summing. A branch on the ends' count remains in the log's shape (the records' letter) and not in the act. The generic form (every take logging `takes` as a list) is a named change to the log of every birth and credit; not built.

The lay-back clause (EQ-S1) covers the body's take alone on the head. The Bell candidate (lay the birth's take back where the gap-0 current sums 0) is one clause for every take; its course: on the ten worlds the births kept at a Node with the net current 0 are 64 of 64 on ga2 (the 4-cube, every birth), 0 of 24 on the hole, 0 of 26 on the chiral, none elsewhere. Under the clause ga2's 64 births would stand with their takes laid back, the children made from nothing against MS-S1 (what is taken is what the lay books and nothing made). A course change on one world of ten, named; not built.

The lay act: `take.lay(node, rec, where, levels, sign)` adds a tuple of counts (now, before per line) at a Node or over the board (Ellipsis). The seed's four forms (seed.lay_world through node.lay), the children (child_at: (A, 0, 0, sense B)), the unclick of a birth and the uniform lay (arrays as counts) are this one act. The take's spelling through `line=k` is struck: the take is the write's form (`move`), the lay the lay. One form for the lay, said by name: a tuple of counts per slot.

## Step 2. The measurements (the copy src_cr2 off the head bit for bit, cr2.patch; Python venv314, nice 19, TMPDIR=/dev/shm/tmp)

The ten worlds against the cache records/2ab32b518 (seven) and against the head's own run (sea_3, universe_3, plasma): compare.py on the content keys after one JSON round trip (the cache carries the integers as strings): the log, the Node lines, the counts, the turns, the rows without the milliseconds, gapped, planes, T, G, gamma.

| world | intervals | log entries | births | credits | laid back | bit for bit | run back | max bits |
|---|---|---|---|---|---|---|---|---|
| hole | 60 | 16,420 | 16 | 777 | 0 | yes | 10 of 10 | 115 |
| chiral | 60 | 25,665 | 17 | 2,943 | 3 | yes | 10 of 10 | 115 |
| bodies | 300 | 15,782 | 0 | 1,973 | 0 | yes | 10 of 10 | 92 |
| universe | 400 | 19,752 | 0 | 1,875 | 1,875 | yes | 10 of 10 | 115 |
| pair_3 | 400 | 3,646 | 0 | 297 | 297 | yes | 10 of 10 | 115 |
| plasma_3 | 170 | 13,205 | 0 | 162 | 162 | yes | 10 of 10 | 115 |
| ga2 | 450 | 70,401 | 64 | 1,408 | 1,408 | yes | 10 of 10 | 115 |
| sea_3 (head) | 240 | 0 | 0 | 0 | 0 | yes | 10 of 10 | 115 |
| universe_3 (head) | 400 | 4,268 | 0 | 405 | 405 | yes | 10 of 10 | 115 |
| plasma (head) | 400 | 138,377 | 0 | 1,875 | 1,875 | yes | 10 of 10 | 115 |

The cache's run back on the hole, the chiral and the bodies was 20 of 20; this hand ran 10 of 10 on every world (the one key not equal, by the count of intervals run back and not by a hash).

The tallies (run_cr2.py's wrap of fall_of and births; fall_of is read twice per take under the one act, the counts halved):
- takes: hole 793, chiral 2,960, bodies 1,973, universe 1,875, pair_3 297, plasma_3 162, ga2 1,472, sea_3 0, universe_3 405, plasma 1,875; 11,812 in all.
- takes on a line with no write wall (the emitter's im line): ga2 1,472 of 1,472; every other world 0. 1,472 of 11,812. The refutation of CR-C1 as `node.write`.
- births kept at a Node whose gap-0 current sums 0 (the Bell clause's course): ga2 64 of 64, hole 0 of 24, chiral 0 of 26 (the kept births before the take's refusal; the births counted 16 and 17 after it).
- the merger's takes (a gapped record taken, SL-S2): 0 on every world. The merger's letter is folded by construction and not exercised by the ten worlds.

The 48 on the clicks (H-48-In-The-Clicks-3's run_48.py, the chiral 3-cube to 60; the world file carried into this folder with the tests' universe_toy.json, the a483 folder's universe lacking `trace`): the copy and the head the same totals and the same 48 lines image for image: EQUAL 12, CONJUGATE 0, APART 36 (the 24 rotations 12 EQUAL and 12 APART, the 24 reflections 24 APART, the first apart intervals 4 and 6; the base births 4, credits 456, turns 139); the 48 unchanged by the fold (the head's own reading at this sha differs from a483's 24 EQUAL of 2026-10-25, the law having moved since by GP-S1 and the rest; not this hand's item)

The suite on the copy (pytest tests -q -o pythonpath=src_cr2): 78 passed, 0 failed, in 318 seconds (the head's suite the same 78 tests)

The code's shape (take.py, close.py, bodies.py): 643 lines and 27 functions on the head; 629 lines and 27 functions on the copy (take_at, take_line and merger_take struck; move, takes and summed added). The interval's list of acts (interval.run): unchanged, five acts. tools/record_code_shape.py's gate reads the merge base from git and was not run on the copy; the view given is its line count.

The 5-cube chiral 48 to 60 was launched on the copy by this hand's first form and cut short at 8 of 48 images (one image in about 3 minutes under the load); the 3-cube is the measure, as for a483.

## Step 3. Every law with a number

- The take's move is the carried division of an exact numerator: (levels * w + r) div w = levels and the remainder r for r in [0, w): 11,812 takes on ten worlds, the records bit for bit.
- The taken line holds a write wall in one of its three cases: 1,472 of 1,472 takes on ga2 on the emitter's im line (none); 0 of 10,340 elsewhere.
- One take act at a list of ends: the birth's one end 97 (16 + 17 + 64), the body's one end 11,715, the merger's two ends 0; refusals by name 5,775 (the sum of refused_stop over the ten worlds: 434 + 2,221 + 825 + 250 + 27 + 81 + 1,408 + 0 + 54 + 375), every entry equal to the head's.
- The lay-back clause for every take: 64 of 64 births on ga2 would be laid back; 0 of 50 on the hole and the chiral.
- The code: 643 to 629 lines, 27 to 27 functions.

## Step 4. The sentences for ALGEBRA.md (proposed; the owner's word decides) and the patch

CR-S1 (2026-10-26, H-Click-As-A-Row-Act-2): "The take's move is the write's form at one Node: one carried division at the line's own wall of the exact numerator levels times the wall, the quotient levels added to the level now and the remainder unmoved; the take forward, its lay-back and its undoing are this one act with the count's sign; the take is not the interval's write act, whose wall is the line's write wall, which the taken line does not hold." Changes no record (bit for bit, ten worlds).

CR-S2 (2026-10-26): "The close's take is one act at a list of ends, each end a Node and the walls booked there, every end read before any is written and refused by name at the first that cannot pay: the birth's list one end of the children's walls summed, the merger's the two ends, the body's one end of its unit; the former three spellings kept by name." Changes no record.

CR-S3 (a finding, no sentence to approve): the lay-back clause of EQ-S1 does not cover the birth's take without a course change: 64 of 64 births on ga2 stand at a Node whose gap-0 current sums 0; under one clause for every take those children would be made from nothing, against MS-S1. The one clause for every take is refused by the letter at this head.

The patch: cr2.patch (diff -ru src/event_universe src_cr2/event_universe, 263 lines), for David. The room each test needs: none; the suite's count stands (78 of 78 passed); every record bit for bit.

## Step 5. The ledger row

| 2026-10-26 | H-Click-As-A-Row-Act-2 | The click as a row act: the take is the write's form at the line's own wall (CR-S1) and one act at a list of ends (CR-S2); not the interval's write (no write wall on 1,472 of 1,472 takes on ga2), not Rule3's step (the before slot stands), the one lay-back clause a course change (64 of 64 births on ga2 at net 0) | A FINDING | ten worlds bit for bit, run back 10 of 10, 115 bits, 643 to 629 lines | cr2.patch |

## Step 6. Missing by name

- The merger's take (SL-S2) at two ends is folded by construction and exercised by none of the ten worlds (0 takes of a gapped record): a world where a gapped pair meets and pays is owed for the measure.
- The 5-cube chiral 48 to 60: cut short at 8 of 48 images (the load; a483 cut it short alike).
- tools/record_code_shape.py's own view on the copy (it reads the merge base from git): the line count given in its place.
- The take as `node.write` by name needs a write wall on every line (a course change to the Node's integer count) or the write act's wall made the line's rotation wall where it holds none: the owner's word.
- The generic log form (every take under `takes`): a named change to every birth's and credit's record, not built.
