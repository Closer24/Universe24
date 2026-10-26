# H-Read-Is-Write-Reversed-1: is every read of the law a write at -1?

Verdict: A FINDING. The acts that move the state are one function with the direction already, and the direction is the one rule's mirror: the carried division at -1 is the division at +1 conjugated by the remainder's mirror w - 1 - r (RW-T1, derived and measured exact), and Rule3's read at -1 is its read at +1 on the two-part record exchanged (RW-T2), so the swap's "exchanged and complemented" and the direction sigma are one object. Four spellings written twice at the head fold into one path bit for bit on ten worlds (the integers, the log, the Node lines, the counts, the turns), the run back exact, the 48 unchanged, the suite green. Three things are not a pair by the letter and are named: the click's draw and the swap's reading, whose inverses are the record (the log, the frame) and not a function at -1; the readings, which write nothing and have no inverse; the bodies' counters, which forget.

Hand rw1, blind, 2026-10-26, 05:4x to 06:2x UTC, on engine-5.0-test HEAD 7bddebe3e in the detached worktree $S/hands/rw1. English, ASCII, integers only. The copy of src under /dev/shm/tmp/rw1/src_rw1 (the flag RW1_FORM from the environment, empty the head bit for bit, "1" the fold), built by make_copy_rw1.py; the fold without the flag under /dev/shm/tmp/rw1/src_rw1_clean, built by make_fold_rw1.py, its diff against src the patch rw1.patch. Records above 200 KB under /dev/shm/tmp/rw1/out, never in the worktree.

## 0. The unification block (the owner's step 0)

What the letter holds twice. ALGEBRA.md writes the time reversal in two places with two names: **The direction** (sigma, u = sigma (SUM R arr + S x - w y) + rho, z = sigma (u div w)) and **The swap at the top** (every line's two levels exchanged and every remainder complemented at its wall, w - 1 - r, the one rule `mirrored`). The code holds them as two: `carried_division(..., direction)` (core/rule3.py:74) with sigma inside the division, and `exchange` (node.py:281) with the mirror outside it. Road (1), the algebra: one clause where two are written.

The one form, RW-T1 (the division). Let (q, r') = carried_division(t, w, r, +1), u = t + r, q = u div w, r' = u mod w. Then carried_division(t, w, r, -1) returns (q, r) from (t, w, r'): u" = -t + r' = -(u - r') + r' ... the head's spelling. Mirror the remainder instead: u' = t + (w - 1 - r') = (w - 1) - (u - 2t) ... the direct form: with v = -t + r', u' = w - 1 - v, so u' div w = -(v div w) and u' mod w = w - 1 - (v mod w) (for v = w k + s, 0 <= s < w: w - 1 - v = w (-k) + (w - 1 - s)). So the head's (direction * (v div w), v mod w) at -1 equals (u' div w, w - 1 - (u' mod w)): the act at -1 is the act at +1 on the mirrored remainder with the result's remainder mirrored back, the quotient as it falls. In one line: carried_division(t, w, r, -1) == (q, w - 1 - r'') where (q, r'') = carried_division(t, w, w - 1 - r, +1). Measured: 50,000 random (t, w, r) with |t| to 10^12, w to 10^6, the forward division then the backward on its remainder returning (q, r) exact, 50,000 of 50,000 (the division's inverse under the mirrored spelling; make_copy_rw1.py (a)).

RW-T2 (the rotate). ALGEBRA.md's proof under The direction takes (x, y) = (a_now, a_before) forward and (a_now, a_next) backward; the Line's two slots hold (now, before) forward and, after the forward act, (next, now): so the backward read of (x, y) is the forward read of the pair reversed, (a, y) = (now, before)[::direction], and the backward write is the forward write of the pair reversed, Line(*(q, a)[::direction]). The head's rotate (node.py:191 to 206) spells this as three branches (the slot at 191, the term w a_before dropped at 194 and taken off the quotient at 206, the Line at 202 to 206); the fold spells it as the pair reversed with the letter's total S a - w y + f + m in both directions, the same integers by the proof (the quotient shifted by a_next exactly, a multiple of the wall).

So the unification: the direction, the mirror and the swap are one object. A turned Node "ends the interval at its held pre-state, exchanged and complemented" (interval.py swap): that is the state read at -1 (RW-T2's exchange, RW-T1's complement). The swap at the top is the Node's own time reversal, the fifth act the direction's read at one Node and no second rule. Candidate sentence beside the item's own: **RW-U1**: the direction sigma = -1 is the one rule's mirror of every remainder and the exchange of every line's two slots; the carried division, Rule3's rotate and the swap are one act under it, the swap the direction read at one Node. The other roads: (2) the matrix, nothing twice found (the Link's record is read once per coupling, links_at); (3) the cube, no threshold twice in this neighbourhood (the 48 and the lattice's numbers stand untouched by the direction); (4) Rule3, the carried division with its remainder is the one step: the fold below removes four branches on the direction, no branch on a row's kind was found in the interval's acts (the walled row's rule by `r.wall is not None` in rule_of is a read of the row's state, not of a name).

## 1. The inventory: every act as a (forward, backward) pair

| act | forward | backward | one function at -1? | line (HEAD) |
| --- | --- | --- | --- | --- |
| the carried division | u = t + r, q = u div w | u = -t + r, sigma (u div w) | ONE already (one function, sigma inside); RW-T1: the same as the mirror conjugation | core/rule3.py:74 |
| Rule3's rotate | the now slot, S a - w before, Line(q, now) | the before slot, S a, Line(a, q - now) | ONE function, three branches on the direction (191, 194, 202); RW-T2 folds them to the pair reversed | node.py:181 |
| the write (the carried division at the write wall) | now + q | now - q | ONE already: `line.now + direction * q` | node.py:208 |
| the act (rotate then write) | two blocks: rotate, levels, write | write, levels, rotate, restore | TWO paths of one meaning; the fold: one path, the two acts in the direction's order, the levels read between | node.py:213 |
| the carrier's act | act(...) | act(...) | ONE already (calls act) | node.py:242 |
| the restore at the turned Nodes | none | the row set to kept | not an act: the exchange's inverse at a turned Node is no act (the Node ended at its pre-state) | node.py:254 |
| the exchange | exchange(top, held) | exchange(top, held) | ONE: an involution with its own inverse | node.py:281 |
| the swap's reading (which Nodes turn) | the weak maximum of (held before, held now, now after the lays) | the frame's mask `turned` popped from the stack | NOT a function at -1: the stepped now x2 is destroyed by the exchange, so the mask is kept as a record (the stack) | node.py:296, interval.py:38 |
| the readings at the start | at(line) = now | at(line) = before (now at a still Node) | ONE function, direction-covariant; a read writes nothing and has no inverse: it is placed first in both directions | interval.py:63, 79 |
| the proper count | + p0 | - p0 | ONE: `+ direction * ...` | interval.py:88 |
| the walled row's act with the flux inside | act(+1) | act(-1) | ONE (act) | interval.py:117 |
| the kick | p + X F | p - X F; the charge's division at -1 | ONE: `direction *`, carried_division(direction) | interval.py:165, 178, 183 |
| the riding line's division | Line(a + v, a) | Line(a, a - v) | ONE function, one branch (222); the fold: (a + direction v, a)[::direction] | interval.py:195 |
| the lays (the emission's write, the current's writes) | node.write(+1) after the divisions | node.write(-1) before the kick | ONE: write(direction); the order the reverse (run: lays first backward) | interval.py:239, 275 |
| the emission's size (laid_on) | counted | not undone | a reading of the run (counts), no inverse by design | interval.py:22, 246 |
| the swap | swap(held, frozen) | the exchange at the frame's mask | ONE exchange; the reading from the record (above) | interval.py:252, 45 |
| the close | click(+1): the meeting, the takes, the lays, the bodies | click(-1): unclick, the log read in reverse | one entry with the direction, TWO bodies: the click is the one act that is not a bijection (the draw), its inverse is the record | close.py:292, 323 |
| the lay (a record's levels at a Node) | lay(sign +1) | lay(sign -1) | ONE already: the count's sign | take.py:97 |
| the take's move and its undoing | lay(line=k, +levels) | lay(line=k, -levels) | ONE already (CR-S1, approved) | take.py:125, close.py:334 |
| the children laid and taken back | child_at(sign +1) | child_at(sign -1) (walls_of reads by laying and taking back) | ONE already: the sign; the merger's lay is the birth's lay at the sign, SL-S2 | close.py:225 |
| the birth and the merger (which ends are taken) | one take at one Node (the emitter) | two takes at two ends (a gapped row) | TWO functions of one meaning at the head (take_at summed, merger_take); CR-S2 approved folds them to one act at a list of ends; the list is a read of the row's gap, not a direction | close.py:119, 168 |
| the frame's read (the draw's digit) | read_number | none | NOT a pair: a read that writes nothing has no inverse | take.py:35 |
| the frame's write (the booking of the remainders) | the carried division's remainder | the same at -1 | ONE (the division) | core/rule3.py:74 |
| the emission's write and the absorption (the take of light) | node.write at the write wall with wr | lay with a count, no remainder | NOT a pair by the letter: two walls (CR-S1: the take is not the interval's write) | interval.py:245, take.py:125 |
| the bodies' counters (standing, crossed, beats) | where(standing, standing + 1, 0) | the frame's copy restored | NOT a function at -1: the reset to 0 forgets; the inverse is a record | bodies.py:20, close.py:339 |
| the counts of the run | += | never undone | readings of the run, no inverse by design | node.py COUNTS |
| the interval's count | += 1 at the making | -= 1 at the end | TWO places of one meaning; the fold: `+= direction` at the making | interval.py:34, 280 |
| the seed's lay | lay at the interval 0 | none | not a pair: the run back ends at the seed | seed.py:30 |

Direction branches at the head in the interval's path: node.py 5 (191, 194, 199, 202, 225), interval.py 11 (33, 45, 65, 222, 225, 229, 230, 235, 246, 275, 279), close.py 1 (300). Under the fold: node.py 1 (199, the transient's bit reading, forward alone), interval.py 10, close.py 1; the four struck are the four spellings written twice.

## 2. RW-S1, the one sentence (dated 2026-10-26; no sentence for approval: the owner's word)

**RW-S1**: every act of the Node that moves the state is one function with the direction, and the direction is the one rule's mirror: the carried division at -1 is the division at +1 with the remainder mirrored in and out (RW-T1); Rule3's rotate at -1 is the rotate at +1 on the line's two slots exchanged (RW-T2); the write, the lay and the take's move carry the count's sign; the readings are of the start's slot in either direction and, writing nothing, have no inverse, so they stand first in both directions; the run back is these acts in the reverse order, each at -1, with no second function. The click's draw and the swap's reading are reads of the board the board does not keep, and their inverse is the record (the log, the frame) and not a function at -1, by the letter "every act but the click a bijection".

What it folds in the code (the patch rw1.patch, 61 changed lines over three files): node.rotate's three branches to the pair reversed (one function, no branch on the slot); node.act's two blocks to one path (the two acts in the direction's order, the levels read between; the backward block struck); interval.division's Line branch; the interval counted at one place. Struck: 0 functions (no "un" function stood in the interval's acts); 4 branches on the direction; the module lines node.py 370 -> 370, interval.py 283 -> 280, core/rule3.py 212 -> 213 (the docstring carries the theorem); the engine 5,416 -> 5,414 lines, 358 -> 360 functions (the two inner acts of `act`, rotate and write, named inside it).

What it does not fold, by name: `unclick` (close.py:323) stays as the log's read in reverse, since the click's forward body is the draw and the meeting (read_number, meet) and its inverse by the letter is the record; the swap's mask stays on the stack; the bodies' counters stay in the frame. These three are the law's own arrow of time: the one place where the board does not carry its own past.

## 3. The symmetry's test: the run back under the fold

(filled from the measurements: section 4)

## 4. The measurements (RW1_FORM=1 on /dev/shm/tmp/rw1/src_rw1; the cache $S/records/2ab32b518/)

The ten worlds (run_record.py on the flagged copy, RW1_FORM=1; the flagged record against the cache for seven, against the flag-off record of the same copy for the three not in the cache; the rows' milliseconds struck, a clock reading; compare_rw1.py, compare_records.md):

| run | against | run back (intervals, exact) | births | credits | turns | log lines |
| --- | --- | --- | --- | --- | --- | --- |
| hole 60 (5-cube) | the cache: SAME in log, Node lines, counts, turns, rows | 20 of 20 | 16 | 777 | 546 | 16,420 |
| chiral 60 (5-cube) | the cache: SAME | 20 of 20 | 17 | 2,943 | 639 | 25,665 |
| bodies 300 (7-cube) | the cache: SAME | 10 of 10 | 0 | 1,973 | 4,229 | 15,782 |
| universe 400 (5-cube) | the cache: SAME | 10 of 10 | 0 | 1,875 | 250 | 19,752 |
| pair_3 400 (3-cube) | the cache: SAME | 10 of 10 | 0 | 297 | 54 | 3,646 |
| plasma_3 170 (3-cube) | the cache: SAME | 10 of 10 | 0 | 162 | 27 | 13,205 |
| ga2 450 (4-cube) | the cache: SAME | 10 of 10 | 64 | 1,408 | 128 | 70,401 |
| sea_3 240 (3-cube) | the flag off: SAME | 10 of 10 | 0 | 0 | 54 | 0 |
| universe_3 100 (3-cube; no cache, the count mine) | the flag off: SAME | 10 of 10 | 0 | 189 | 0 | 1,973 |
| plasma 170 (5-cube; no cache, the count mine) | the flag off: SAME | 10 of 10 | 0 | 750 | 125 | 61,127 |

Bit for bit on every world: the log (every birth, credit and refusal line with its integers), the Node lines at every interval, the counts, the turns, the reader's rows. The run back exact 10 of 10 on every world and 20 of 20 on the hole and the chiral (the state's hash with the interval at every returned interval). The smoke run (hole 6, back 6) flag on against flag off: every key equal but the clock reading.

RW-T1 on the head's own division (division_mirror_test.py, no flag): 50,000 random triples, the forward division then the backward on its remainder returning (q, r) exact 50,000 of 50,000; the act at -1 equal to the act at +1 under the mirror (the remainder mirrored in, the result's remainder mirrored out, the quotient as it falls) 50,000 of 50,000.

Run times under nice on four cores (the batch's wall clock): hole 52 s, chiral 71 s, ga2 99 s, universe 76 s, bodies 52 s, pair_3 29 s, plasma_3 18 s, sea_3 44 and 43 s, universe_3 27 and 26 s, plasma 19 and 18 s.

The 48 on the chiral 3-cube to 60 (H-48-In-The-Clicks-3's run_48.py on the flagged copy, the world copied to worlds/ with the head's universe file, since the runner's own universe_toy.json lacks the `trace` key the head reads; c48_3cube_60_on.jsonl and c48_3cube_60_off.jsonl): flag on 12 EQUAL, 0 CONJUGATE, 36 APART (det +1: 12 EQUAL, 12 APART; det -1: 24 APART), the base 4 births, 456 credits, 139 turns, the first apart intervals 4 and 6; flag off the same 48 lines image by image (the verdict, the births, the credits, the first apart interval of every image). Unchanged, as asked: the fold moves no record and the 48's standing is the head's own (H-48-In-The-Clicks-3's DOES NOT stands untouched by this item). 276 s and 283 s.

The code shape (before -> after, the flag-less fold src_rw1_clean): node.py 370 -> 370 lines, interval.py 283 -> 280, core/rule3.py 212 -> 213; the engine (src/event_universe, every .py) 5,416 -> 5,414 lines, 358 -> 360 functions (the two inner acts of `act` named inside it); direction branches on the interval's path 17 -> 12; "un" functions in the interval's acts 0 -> 0 (none stood; `unclick` stays, by the letter). The patch rw1.patch: 133 lines, 61 changed, three files.

## 3. The symmetry's test: the run back is the law's own proof

Under the fold the run back is exact on every world (10 of 10 on eight worlds, 20 of 20 on the hole and the chiral) with the four spellings struck, so the backward act of the division, the rotate, the act and the riding division is literally the forward function at -1 (the same code path: the pair reversed, the mirror conjugation inside the division, the two acts in the direction's order). What the run back still needs beside the forward functions: (i) the frame on the stack (the turned mask, the counters' copy, the log's length, the frozen mask), read at the Interval's making backward; (ii) `unclick`, the log read in reverse. Both are the record of a read the board does not keep (the draw, the swap's third level, the counters' reset), so by the letter the run back is "every act undone bit for bit" with no second function for the acts, and one record for the reads. Nothing more can be struck without a second carried integer per Node (the swap's x2 kept, the counters kept as counts and not resets), which is a change of the letter and goes to the owner by name (section 6).

## 4a. Every law with a number (the item's numbers)

RW-T1: 50,000 of 50,000 triples; the fold bit for bit on 10 worlds (3 cubes of 3, 1 of 4, 5 of 5, 1 of 7), 2,540 intervals forward, 120 back, 120 exact; the log 227,971 lines equal across the ten (16,420 + 25,665 + 15,782 + 19,752 + 3,646 + 13,205 + 70,401 + 0 + 1,973 + 61,127); the 48: 48 of 48 images equal to the head's own verdicts; the branches struck 4 of 17; the functions struck 0.

## 5. The ledger row

| item | verdict | sentence | what folds | what stays by name | measured |
| --- | --- | --- | --- | --- | --- |
| The read is the write at -1 (the owner's word of 2026-10-26, 07:0x UTC; hand rw1, blind) | A FINDING: the state's acts are one function with the direction already, and the direction is the one rule's mirror (RW-T1) and the exchange of the two slots (RW-T2); the swap is the direction read at one Node (RW-U1) | RW-S1 (dated; for the owner's word); RW-U1 the unification candidate | rotate's three branches, act's two paths, division's Line branch, the interval's two counts: rw1.patch, 61 lines, 3 files, 0 functions struck | unclick (the log), the frame's mask and counters (the stack), read_number (a read writes nothing), the emission's write against the take (two walls, CR-S1), the bodies' reset | 10 worlds bit for bit against the cache or the head; the run back 10 of 10 and 20 of 20; the 48 unchanged 48 of 48; RW-T1 50,000 of 50,000; the suite (section 7) |

## 6. Missing, by name

1. The swap's reading at -1 as a function and not a record: it needs the stepped now x2 at a turned Node, which the exchange destroys; a second carried level per Node would keep it (the "second carried integer" the law declined under **The integer budget of a derived row**). Named, not proposed.
2. The click's draw at -1: the law's own open item (what produces a click is not known; the log is its record); no function at -1 exists by the letter.
3. The bodies' counters as bijections: `standing = where(standing_now, standing + 1, 0)` forgets; a count that is never reset (the crossings counted, the reset read as a difference) would run back with no copy. A reading, no measurement made.
4. The birth and the merger as one act at a list of ends: CR-S2, approved, David's build; not re-derived here.
5. The emission's write and the take as one act: refused by the letter (two walls; CR-S1's own clause). Named.
6. run_record.py's summary reads the key "run back" where the record writes "run_back", so its one-line summary prints null for every run; the record's own `run_back` field is the measure read here. A runner's quirk, no law.
7. The run's `interval` counted at one place changes no integer of any record (measured), but the head's two places were counted as a spelling written twice and no more.
8. Cut short: nothing. Every run named above finished; universe_3 was run to 100 intervals and plasma to 170 (no count given, no cache), each compared flag on against flag off.

## 7. The suite on the copy

`pytest -q -o pythonpath=<copy>/src tests` on the flagged copy with RW1_FORM=1: 78 passed in 332 s (0 in stderr). The same suite on the flag-less fold /dev/shm/tmp/rw1/src_rw1_clean (the patch as David would land it): 78 passed in 269 s. `git apply --check` of rw1.patch against the worktree's src: clean (no file under src/ or tests/ edited; the check is a dry run).

## 8. The room each test needs (for David, with rw1.patch)

The ten worlds against the cache 2ab32b518 (run_record.py, the milliseconds struck): about 100 s each on one core under nice, 8 minutes in all on four cores; the run back 20 on the hole and the chiral, 10 elsewhere. The 48 on the chiral 3-cube to 60: about 280 s. The suite: about 300 s. RW-T1's script: 2 s. Everything of this item fits in 15 minutes on four cores.

Files: REPORT.md (this), make_copy_rw1.py (the flagged copy), make_fold_rw1.py (the flag-less fold), rw1.patch (the fold for David), run_all.sh (the batch), compare_rw1.py and compare_records.md (the ten worlds' comparison), division_mirror_test.py and division_mirror.txt (RW-T1), c48_3cube_60_on.jsonl and c48_3cube_60_off.jsonl (the 48 image by image), worlds/ (the 3-cube world with the head's universe file). The records (above 200 KB) under /dev/shm/tmp/rw1/out.
