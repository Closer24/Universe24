# rw1_REPORT: H-Read-Is-Write-Reversed-1 (blind hand rw1, 2026-10-26, 05:4x to 06:0x UTC, HEAD 7bddebe3e)

Verdict: A FINDING. Every act that moves the Node's state is one function with the direction already, and the direction is the one rule's mirror: the carried division at -1 is the division at +1 with the remainder mirrored in and out (RW-T1, exact 50,000 of 50,000), and Rule3's read at -1 is its read at +1 on the line's two slots exchanged (RW-T2, the letter's own proof under The direction); so the swap's "exchanged and complemented" and sigma = -1 are one object (RW-U1, the unification candidate). Four spellings written twice fold into one path bit for bit on ten worlds; three reads are not a pair by the letter and are named: the click's draw (its inverse the log), the swap's reading (its inverse the frame's mask), the bodies' counters (a reset forgets; restored by copy); the readings write nothing and have no inverse.

Full derivation, inventory table, measurements and files: tools/derivations/open_items/H-Read-Is-Write-Reversed-1/REPORT.md in the worktree $S/hands/rw1 (absolute: /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/rw1/tools/derivations/open_items/H-Read-Is-Write-Reversed-1/REPORT.md). Records under /dev/shm/tmp/rw1/out.

## The unification block (step 0)

The letter holds the time reversal twice: **The direction** (sigma inside the division, core/rule3.py:74) and **The swap at the top** (the exchange and the complement w - 1 - r, node.py:281, `mirrored` core/rule3.py:128). RW-T1: carried_division(t, w, r, -1) == (q, w - 1 - r'') where (q, r'') = carried_division(t, w, w - 1 - r, +1); proof: with v = -t + r and u' = t + (w - 1 - r) = w - 1 - v, u' div w = -(v div w) and u' mod w = w - 1 - (v mod w). RW-T2: the backward read (a_now, a_next) of the two-part record is the forward read of the Line's pair reversed, (a, y) = (now, before)[::direction], the total S a - w y + f + m in both directions, the new line (q, a)[::direction]. **RW-U1** (candidate, beside the item's own): the direction -1 is the mirror of every remainder and the exchange of every line's two slots; the carried division, Rule3's rotate and the swap are one act under it, the swap the direction read at one Node. Roads (2) to (4): nothing twice found in the matrix or the cube; Rule3's carried division is the one step and no branch on a row's kind stands in the interval's acts.

## The inventory (a)

One function already: the carried division (rule3.py:74), the write (node.py:208, `+ direction * q`), the kick (interval.py:165), the riding division (interval.py:195), the lays (interval.py:239, write(direction)), the proper count (interval.py:88), the lay (take.py:97, the sign), the take's move and its undoing (take.py:125 and close.py:334, CR-S1), the children laid and taken back (close.py:225, the sign; SL-S2's merger lay), the exchange (node.py:281, an involution), the readings (interval.py:63, `at()` direction-covariant: a read writes nothing and has no inverse, so it stands first both ways). Two spellings of one meaning (the candidates, folded): node.rotate's three direction branches (node.py:191, 194, 202), node.act's two blocks (node.py:225), interval.division's Line branch (interval.py:222), the interval counted at two places (interval.py:34, 280). Two functions of one meaning not folded here: the birth's take and the merger's take (close.py:119, 168; CR-S2 approved, David's). Not a pair by the letter: click(+1) against unclick (close.py:292, 323: the click is the one act that is not a bijection, its inverse the record); the swap's reading (node.py:296) against the frame's mask (interval.py:38: x2 destroyed by the exchange); the bodies' counters (bodies.py:20, reset to 0; restored from the frame, close.py:339); read_number (take.py:35, a read that writes nothing); the emission's write against the absorption's take (interval.py:245, take.py:125: two walls, CR-S1); the counts of the run (readings); the seed's lay (no inverse needed).

## RW-S1 (b), dated 2026-10-26, no sentence for approval: the owner's word

Every act of the Node that moves the state is one function with the direction, and the direction is the one rule's mirror: the carried division at -1 is the division at +1 with the remainder mirrored in and out; Rule3's rotate at -1 is the rotate at +1 on the line's two slots exchanged; the write, the lay and the take's move carry the count's sign; the readings are of the start's slot in either direction and, writing nothing, have no inverse, so they stand first in both directions; the run back is these acts in the reverse order, each at -1, with no second function. The click's draw and the swap's reading are reads of the board the board does not keep, and their inverse is the record (the log, the frame) and not a function at -1, by the letter "every act but the click a bijection".

What it folds (rw1.patch, 133 lines, 61 changed, three files, `git apply --check` clean): rotate to the pair reversed; act to one path (the two acts in the direction's order, the levels read between); division's Line to (a + direction v, a)[::direction]; `node.interval += direction` at one place. Functions struck 0 (no "un" function stood in the interval's acts; unclick stays by the letter); direction branches on the interval's path 17 -> 12; node.py 370 -> 370, interval.py 283 -> 280, core/rule3.py 212 -> 213; the engine 5,416 -> 5,414 lines, 358 -> 360 functions.

## The symmetry's test (c) and the measurements (step 2)

| run | against | run back | births | credits | turns | log lines |
| --- | --- | --- | --- | --- | --- | --- |
| hole 60 | the cache: SAME (log, Node lines, counts, turns, rows) | 20 of 20 | 16 | 777 | 546 | 16,420 |
| chiral 60 | SAME | 20 of 20 | 17 | 2,943 | 639 | 25,665 |
| bodies 300 | SAME | 10 of 10 | 0 | 1,973 | 4,229 | 15,782 |
| universe 400 | SAME | 10 of 10 | 0 | 1,875 | 250 | 19,752 |
| pair_3 400 | SAME | 10 of 10 | 0 | 297 | 54 | 3,646 |
| plasma_3 170 | SAME | 10 of 10 | 0 | 162 | 27 | 13,205 |
| ga2 450 | SAME | 10 of 10 | 64 | 1,408 | 128 | 70,401 |
| sea_3 240 | the flag off: SAME | 10 of 10 | 0 | 0 | 54 | 0 |
| universe_3 100 (no cache; the count mine) | the flag off: SAME | 10 of 10 | 0 | 189 | 0 | 1,973 |
| plasma 170 (no cache; the count mine) | the flag off: SAME | 10 of 10 | 0 | 750 | 125 | 61,127 |

Bit for bit on every world with the four spellings struck; the run back exact 120 of 120 intervals over the ten worlds, with no separate "un" function for any act of the interval; what the run back still reads beside the forward functions is the record (the frame on the stack, the log in unclick), the law's own arrow of time. The 48 on the chiral 3-cube to 60: flag on and flag off the same 48 lines image by image (12 EQUAL, 36 APART; the base 4 births, 456 credits, 139 turns; first apart intervals 4 and 6): unchanged. The suite: 78 passed on the flagged copy (332 s) and 78 passed on the flag-less fold (269 s). RW-T1 on the head's own division: 50,000 of 50,000.

## Every law with a number (step 3)

RW-T1 50,000 of 50,000; ten worlds (3-cubes 3, a 4-cube, 5-cubes 5, a 7-cube), 2,540 intervals forward, 120 back, 120 exact; 227,971 log lines equal; 48 of 48 images at the head's verdicts; branches struck 4 of 17; functions struck 0; the suite 78 of 78 twice.

## The ledger row (step 5)

| item | verdict | sentence | folds | stays by name | measured |
| --- | --- | --- | --- | --- | --- |
| The read is the write at -1 (the owner's word, 2026-10-26 07:0x UTC; rw1, blind) | A FINDING: the state's acts one function with the direction already; the direction the one rule's mirror (RW-T1) and the exchange of the two slots (RW-T2); the swap the direction read at one Node (RW-U1) | RW-S1 dated; RW-U1 candidate | 4 branches, rw1.patch 61 lines, 3 files, 0 functions | unclick (the log), the frame's mask and counters, read_number, the emission's write against the take (CR-S1), the bodies' reset | 10 worlds bit for bit; run back 120 of 120; the 48 48 of 48; RW-T1 50,000; suite 78 twice |

## Missing, by name (step 6)

1. The swap's reading at -1 as a function needs the stepped now x2 at a turned Node, destroyed by the exchange: a second carried level per Node, which the law declined (The integer budget of a derived row). Named, not proposed.
2. The click's draw at -1: the law's open cause; the log is its record by the letter.
3. The bodies' counters as bijections (a count never reset): a reading, no measurement.
4. The birth and the merger as one act at a list of ends: CR-S2, approved, not re-derived.
5. The emission's write and the take as one act: refused by CR-S1's own clause (two walls).
6. run_record.py's summary reads "run back" where the record writes "run_back" (its one-line summary prints null); the record's field was read. No law.
7. Cut short: nothing; universe_3 run to 100 and plasma to 170 with no cache, each flag on against flag off.

No commit, no push, no edit under src/ or tests/. Files under /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/rw1/tools/derivations/open_items/H-Read-Is-Write-Reversed-1/; records under /dev/shm/tmp/rw1/out.
