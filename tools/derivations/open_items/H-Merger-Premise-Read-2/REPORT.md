# pr2 report: when the merger premise is read (H-Merger-Premise-Read-2, 2026-10-26)

The derivation, the flag, the measures and the sentence stand in DERIVATION.md beside this file; this report is its copy for the Boss (the brief: the verdict line first, then (1) to (7)).

Hand pr2, blind to pr1. Worktree <W> = /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pr2 (the engine head 0aa0b8ff4, detached). Nothing under src/ or tests/ of the worktree touched; the flagged copy under /dev/shm/tmp/pr2/src_pr2. Python /home/user/Universe24/venv314/bin/python, TMPDIR=/dev/shm/tmp. The predictions stand in out/PREDICTIONS.txt, written before every run.

## Verdict line

The letter requires reading (a), the pair's own state as the birth laid it, AND the engine on this head already reads it so: there is no Rule3 step between the birth's lay and the premise's read. The two readings are NOT one in the algebra (the stepped current is nonzero at 30 of 32 born pairs met at their next close, exactly den A (q_minus + q_plus)), but they are one in the engine's order of acts, which reads the close at the interval's start. Records: the hole 60 and the chiral 60 and the quartet leg's chiral 3-cube at 60 hold the SAME board under both readings (nodes equal, the births, the takes and the credits equal to the integer), and part only in the refusals' names (the hole at the interval 9, the chiral at 5, the leg at 5). The rest premise as laid 16 of 17 (hole), 14 of 15 (chiral), 6 of 6 (the leg); stepped 2 of 17, 0 of 15, 1 of 6. Laws checked under reading (b): the flag empty bit for bit 2 of 2 worlds, the run back 20 of 20 and 10 of 10, the kit's conservation 11 of 12 in full (the one missed law the head's own, measured on the head's record as the control), integers 0 floats, one Link, the count and the bits unchanged. The one unmet: gate 15's pre-EX-S1 inequality taken >= booked per birth (14 of 17), unmet on the head alike.

## Step 0: the unification above the item (the brief's unification block)

**The close reads ONE board, and that board is the interval's start.** By the four roads:

(1) The algebra: the close's every reading is taken from `plane_starts`, the records' lines at the interval's start (close.py:300-313): the standing share (`owns` = gram.share of plane_starts), the rules (`node.read_lines(held, plane_starts, ...)`), the meeting's current and twist and the charges (close.meet), the bodies' closing. One moment, one array, one form.

(2) The doubling the letter holds: `bodies.credit`'s frame reads a SECOND moment at the same close, the stepped levels (bodies.py:85-96, `node.stepped[rec]`, the keys `re_stepped` and `im_stepped`), and the decoder reads them (decoder.py:240). So the close as written reads the board at two moments: the start for the meeting, the refusal and the share, and the step's end for the credit's frame. The brief's three (close.meet, close.refuse, bodies.credit) read the SAME number only if the second moment goes.

(3) The one form, named: **the Link's own bilinear of the row, F_ij = SUM over the row's lines of (now_i before_j - before_i now_j) (links.cross, the one bilinear of the law), read once per Link per record at the interval's start, and nowhere else in the close.** The current, the twist (the cross of the summed transverse currents, itself two F's), the charge (the Wronskian, the same cross at one Node) and the credit's frame are four readings of that one bilinear at one moment.

(4) The candidate sentence of the unification (PR-S1 below): the close is one reading of the board at the interval's start; `node.stepped` leaves the close, and with it one array per record per interval and one of the two moments. Cost: the credit's frame loses `re_stepped`/`im_stepped`; the decoder's zx reads the start levels and the next interval's start instead (the stepped levels plus the close's own lays are exactly the next interval's start, so nothing is lost that the next frame does not carry).

## 1. The algebra (one page)

**The lay (GP-S1, merger.child_at).** One child at each end of the born Link at the quarter turn: the four slots (re_now, re_before, im_now, im_before) = (sense A, 0, 0, B), sense -1 at the minus end and +1 at the plus end, A B = T div 2, the same two integers for every row. So the pair is even under the Link's mirror (the exchange of the ends with the re line's sign) while the current is odd.

**The premise at the lay.** F_ij = SUM lines (now_i before_j - before_i now_j): the re line gives (sense_i A)(0) - (0)(sense_j A) = 0, the im line (0)(B) - (B)(0) = 0. **F = 0 exactly, with no rounding, on both lines.** The charge W = re_now im_before - im_now re_before = sense A B, so W_minus W_plus = -(A B)^2 < 0: MG-S1's premise (both ends whole, the charges opposite, no current) holds at the lay for every row alike. This is the theorem of the moving pair's rest case and the theorem of SL-S1.

**The premise one step on (reading (b)).** Rule3 shifts the slots: after one step re.before = the laid re.now = sense A and re.now = the step's quotient q. Then:
- the im line contributes 0 at every pair: its before slot after the step is the laid im.now = 0 at BOTH ends, so F_im = p_i 0 - 0 p_j = 0. **One line, the re line, carries the whole stepped current.**
- the re line: F_re = q_minus (A) - (-A) q_plus = A (q_minus + q_plus).
So the stepped current in the close's own unit is **flow = den A (q_minus + q_plus)**, an integer multiple of den A.

**The step's own form at each end.** Rule3's line: w a_next + r' = w (2 a_now - a_before) - D a_now + SUM_j R_ij (m_ij - a_now) + r, one rule for every line of a row at a Node, the remainder r kept in [0, w) per line per Node, w = 6 den Gamma^2 G^2, D = 12 (den - num) p_0^2 G^2, R_ij = 2 num p_i^2 Q_ij G^2. At the two ends of the born Link, with the record standing at nothing about the pair, every term is the mirror's negative: w(2(-A) - 0) = -w(2A - 0); -D(-A) = +DA; the born Link's own term R(m - a_now) with m the neighbour's level turned by the Link's record, the turn's rounding odd (paces.odd_rounded), so m_at_minus = -m_at_plus exactly and R(m + A) = -R(-m - A); the five other Links' terms R(0 + A) = -R(0 - A). **So the two ends' totals are exactly M and -M.**

**The cross term's two parts and why the sum is not 0.** The quotient is the floor of the carried division, which is NOT odd: with one remainder r at both ends, q_minus + q_plus = (2 r - s_minus - s_plus) div w with s the two new remainders in [0, w), so q_minus + q_plus is 0 where s_minus + s_plus = 2 r and -1 or +1 where it is 2 r -+ w; where the two ends' remainders and their environments differ (the other records, the carrier's levels, the Link factors and phases, the gap-0 row), the totals are no longer exact mirrors and the sum is any small integer. **The pair's charge law (the charges summing to 0, the amplitudes equal) does NOT force the stepped current to 0: it forces only that the im line carries none of it and that the whole of it is A times the floor's own residue of the two ends.** Measured below: the residues -9, -1, +7, +37, 0 at the hole 60's pairs; flow exactly den A times them.

**The condition on the row under which the stepped current is 0:** the wall w divides the end's own total, D A + SUM_j R_ij (m_ij + A) congruent to the remainders' shift mod w. It is a divisibility and not an inequality: the carriage pair's inequality (the row's mass above its reaches, den > 2 num, 6 (den - num) >= num) bounds the hop and leaves the divisibility untouched, so a carrying leg's born pair has a nonzero stepped current exactly as a plane leg's.

**The prediction before the runs** (out/PREDICTIONS.txt, B6): every born pair of the hole 60, the chiral 60 and the bodies 120 reads flow 0 at its next close under reading (a) and a nonzero stepped current under (b) wherever the wall does not divide the end's total; the quartet row's births on a carrying leg the same.

**Step 0's unification carried into the item:** close.meet, close.refuse and bodies.credit read the one bilinear F at one moment, the interval's start. One reading serves the three, and it is reading (a).

## 2. The order of the acts: why reading (a) is already the engine's (the finding)

The interval's five acts (interval.py): (1) the readings at the start, (2) the kick, (3) the division (Rule3's step), (4) the swap, (5) the close. In act (3), interval.py:229-233:

    start = self.rows[k] if self.direction == 1 else new
    after = new if self.direction == 1 else self.held[k]
    self.plane_starts.append(list(start))
    self.stepped.append([line.copy() for line in after])

`self.rows[k]` is the row as the interval began, BEFORE this interval's step; `new` is the stepped row. The close is handed `plane_starts` (close.py:271, node.click), so **the close of interval n reads the board at the start of interval n and writes its lays onto the stepped board of interval n.** A birth's children are therefore laid after the step of n, and the close of interval n + 1 reads the start of n + 1, which is that same stepped board with the children on it: **no Rule3 step acts on the children between their lay and the read of the premise.** The brief's premise ("the engine reads that meeting one step after the birth") and the moving pair's reading of the delay as "the step's transient" are both a misreading of the order of the acts: what gave the moving pair its current at the next close was its own phase in the lay, read as laid, not a step.

So reading (a) is the head's own reading, and reading (b) is the change: the premise read at `node.stepped`, the pair one Rule3 step after its lay.

## 3. Which reading the letter requires

1. **The letter's words.** SL-S1: "a meeting where both ends hold a whole quantum of the record at the interval's start" (the letter's own words); the sentence (1) of 19:0x UTC: "the current F_ij = num (now_i before_j - before_i now_j) read at the interval's start keeps the draw and the take at the end it flows into"; links.link_current's own letter: "read at the interval's start". The premise's three numbers (whole, opposite, no current and no twist) are one clause of MG-S1 and are read at one moment, and the letter names that moment: the interval's start. Reading (b) reads the current at a moment the letter names nowhere.
2. **One act on every row alike** (the owner's word of 09:2x UTC, "it acts on every row the same"). Reading (b) can only be spelt for a record with a gap (the gap-0 row has no second end's charge and no merger), so it reads the gapped rows' current one step later than the gap-0 row's: a branch on the row's kind, which THE_WAY names as never a solution.
3. **The close as one reading** (step 0): reading (b) adds the second moment to the close instead of taking it out; reading (a) with the unification takes the second moment out altogether.
4. **SL-S1's own theorem is kept in its number and corrected in its derivation.** SL-S1 asserts the stepped current is "exactly 0 at the next close (the re line q A - A q)" by the mirror. The measure refutes the assertion (the floor is not odd: 15 of 17 pairs on the hole 60 and 15 of 15 on the chiral 60 have a nonzero stepped current) and confirms its conclusion (the current at the next close is 0 at 16 of 17 and 14 of 15), because the close reads the pair as laid. The letter's conclusion stands; its reason is the order of the acts, not the step's mirror.
5. What reading (b) would make false: MG-S1's premise at a born pair (30 of 32 measured pairs lose it), SL-S1's theorem as written, and the quartet's 42 of 42 taken back. What reading (a) leaves false: nothing of the letter measured here.

## 4. The flag

The kit's maker: `make_flagged_copy.py pr2 PREMISE_STEPPED replacements_pr2.json src <W>/src python <P>`. Three replacements in event_universe/close.py (replacements_pr2.json), no other file: the import of `environ`; in `meet`, the premise read as `node.stepped[rec]` in place of `start` for the currents, the twists and the charges where the row has a gap and the flag stands (reading (b)), and the alternative read computed for the log; and one log line per meeting of a gapped record under the second flag `PREMISE_LOG` carrying both readings' flow, twist and charges. With both flags empty the path is the head's: **the kit's check EQUAL on the hole 60 (c7060288e55c497b24f74111e1fd559df2434d7874cfc783fa48fece371f3c1f) and the chiral 60 (4e5b63f9ac2f2fa7cc686ad902a42bd5ce567854c81618a3a6fff46ae6496374), 2 of 2 worlds, the same two hashes the carriage and the click pairs report.** The copy: /dev/shm/tmp/pr2/src_pr2. No number enters a src line; no name of a family; nothing beyond one Link; no act of the law changed under the flag empty.

## 5. The measure

The runs (every one `nice -n 19`, PYTHONPATH=/dev/shm/tmp/pr2/src_pr2, back 20 or 10; the records under /dev/shm/tmp/pr2/):

| record | reading | births | credits | refused stop / orientation / twist / sense | run back | board |
|---|---|---|---|---|---|---|
| hole 60 | (a) as laid | 17 | 2,288 | 9,146 / 248 / 229 / 9,274 | 20 of 20 | - |
| hole 60 | (b) stepped | 17 | 2,288 | 9,314 / 96 / 164 / 9,323 | 20 of 20 | equal to (a) |
| chiral 60 | (a) | 17 | 2,903 | 9,371 / 110 / 42 / 10,393 | 20 of 20 | - |
| chiral 60 | (b) | 17 | 2,903 | 9,586 / 69 / 7 / 10,254 | 20 of 20 | equal to (a) |
| chiral 3-cube at 60, the leg p3 | (a) | 7 | 928 | 2,106 / 65 / 14 / 2,086 | 10 of 10 | - |
| chiral 3-cube at 60, the leg p3 | (b) | 7 | 928 | 2,171 / 24 / 2 / 2,074 | 10 of 10 | equal to (a) |

The births, the takes (taken and booked to the integer: 91,524,260,120,888,090,397,359 and 89,041,969,164,090,056,764,412 on the hole 60 under both), the credits, the turns, the refused lays, the met and the Node lines are EQUAL under the two readings on every record; the refusals' total is equal too (the hole 18,897 under both, the chiral 19,916 under both). **The two readings part in the NAME of the refusal and in nothing else on these records**, because no merger is paid inside 60 intervals under either (MG-S1's record: the merger at rest is refused by the stop at the pair's first close and lands at the cycle's bottom, 217 on ga2). The first parting line of the log: the hole at the interval 9, the chiral at 5, the leg at 5 (hash_pr2.py; the records APART, `nodes_equal` true, the log of equal length).

The premise at the born pair's next close (premise_read.py on the log alone, out/premise_*.json):

| record | births | met at the next close | flow 0 as laid | the rest premise as laid | flow 0 stepped | the rest premise stepped | the fates under (b) |
|---|---|---|---|---|---|---|---|
| hole 60 | 17 | 17 | 16 | 16 | 2 | 2 | twist 10, stop 7 |
| chiral 60 | 17 | 15 | 14 | 14 | 0 | 0 | stop 10, twist 5 |
| leg p3, 3-cube 60 | 7 | 6 | 6 | 6 | 1 | 1 | stop 5, twist 1 |

Totals: **the rest premise holds at 30 of 32 born pairs met at their next close as laid, and at 2 of 32 one step on.** The charges at the next close as laid are -+18,000 = -+(T div 2) at every clean pair (A 125, B 144) and the two the exceptions are the pairs laid where the record already held levels (the lay's refusal reads the share at the start and lays onto the stepped board: the residue, hole interval 11, flow 52,402,832,959,492,416,384 and the charges -+17,136).

**The algebra confirmed to the integer**: every stepped flow measured is den A times a small integer: -17,058,213,854,001,437,625 = -den x 125 x 9, -1,895,357,094,889,048,625 = -den x 125 x 1, -15,162,856,759,112,389,000 = -den x 125 x 8, 13,267,499,664,223,340,375 = +den x 125 x 7, 70,128,212,510,894,799,125 = +den x 125 x 37. The form flow = den A (q_minus + q_plus) of section 1 holds at every pair measured, the residue between -9 and +37 and 0 at 2 of 32.

All the meetings of a gapped record, not the born pairs alone (the log's premise lines): the hole 60, 18,568 meetings, the rest premise 33 as laid against 18 stepped; the chiral 60, 19,764 meetings, 50 against 32; the leg, 4,231 meetings, 8 against 2. **Reading (b) cuts the merger's premise about in half over the whole record and to one sixteenth at the born pairs.**

The kit's conservation check in full on one record: the hole 60 under reading (b) (the flag set for the check's own board re-run too) **11 of 12 laws in full**; the control, the head's own hole 60 record, **11 of 12**, the same law missed (the count's "taken >= booked per birth", 14 of 17, gate 15's pre-EX-S1 inequality, while EX-S1's exact identity holds at 2,305 of 2,305 clicks under reading (b)); the run back 20 of 20, the current's antisymmetry 60 of 60, the Node lines' current against the board's 60 of 60, the Wronskian at the marks 14 of 14, the births' charge of opposite sign 17 of 17, floats 0. Run without the flag in the check's environment the law of the form reads 102 of 40,267 log lines, which is the re-run reading (a) against a record written under (b): the check's board re-run takes no flag, named as a reading of the tool.

The pins the engine's tests hold that move under reading (b): every test that pins a refusal's count or name at a born pair's close, and SL-S1's own test of the born pair refused at its next close (tests of the close's counts); no test of the births, the takes, the credits, the run back, the 48's rows or the conservation moves, since the board does not. Named, not run (the suite is the Boss's full check).

## 6. What each reading costs and buys

**Reading (a), as laid (the head's).** Makes true: MG-S1's premise at every born pair (16 of 17, 14 of 15, 6 of 6); SL-S1's refusal of the undoing and its number; the exact take (EX-S1 2,305 of 2,305); the charge law (the charges -+T div 2 at every clean pair, the births' W of opposite sign 17 of 17); the count of integers 99 and 112 bits unchanged. Costs: the born pair is a merger's premise at its next close always, so no born pair survives on any leg (the quartet's 42 of 42 taken back), which is the carriage's open item; and the premise is read on a state the board has already left by one step (the close reads one board and writes on another), which is the residue the lay's refusal does not see.

**Reading (b), stepped.** Buys: the born pair survives its next close at 30 of 32 measured pairs, which is exactly what the carriage pair sought and the moving lay failed to buy, and at no price in the charge (nothing is rounded: the lay is untouched). Costs: MG-S1's premise is read where the letter names no moment; a branch on the row's kind (no gap-0 row has it); the merger's premise over the whole record cut about in half (33 to 18 on the hole 60, 50 to 32 on the chiral 60), so gate 24 (the merger at rest seen at the cycle's bottom, 64 mergers at 64 of 64 Nodes at 217 on ga2) is at risk by the same factor and is the one gate that must be re-read before any word; SL-S1's theorem as written is made false; and the records' refusals change name with no change on the board, which buys nothing in the clicks: no credit, no birth, no Bell cell and no 48 count moves inside 60 intervals.

**Which reading nature's records favour.** The gates the Reader's rows read: the merger as a row (gate 24) favours (a) outright, it is the clause (b) weakens; the pair into light is the same under both on these records (the births and the takes equal to the integer); Bell's cells are empty under both here (no pair clicked at both ends on these records, as the carriage and the click pairs both read). So **nature's records as they stand favour (a), and (b) buys only on a record where a merger is paid at the delay 1 (the quartet legs), which is cut short below.**

## 7. The sentence

**PR-S1 (the premise of the merger is read at the interval's start, 2026-10-26), as it would stand in ALGEBRA.md under The click; MG-S1, SL-S1, SL-S2, GP-S1, CA-S1, LT-S1 and the sentence (1) of 19:0x UTC kept by name:**

"The close is one reading of the board at the interval's start, and every number of it is read there: each record's standing share, each row's rule, the Link's own bilinear F_ij = SUM over the row's lines of (now_i before_j - before_i now_j) with the twist and the charge as its cross at the Link's two ends, and the credit's frame alike; the state the step left is read nowhere in the close, being the next close's own start with the close's lays upon it. So the premise of MG-S1's merger (a record with a gap whose two ends hold a whole quantum each of opposite charge with no current and no twist) is the pair's own state as the one lay act laid it, and every born pair is that premise at its next close, by the lay's evenness under the Link's mirror against the current's oddness, with no step between the lay and the read. The former reading kept by name: the stepped premise, the pair read one Rule3 step after its lay, whose current is den A (q_minus + q_plus), A the child's amplitude and q the two ends' stepped levels, nonzero at 30 of 32 born pairs of the records and a reading of the floor's own residue and not of the pair."

A reading needs no word of the owner unless it changes a course. **PR-S1's first half (the close's one moment, the unification) changes one course and must go to the owner through the Boss: `node.stepped` leaves the close, so bodies.credit's frame loses the keys `re_stepped` and `im_stepped` and the decoder's zx (decoder.py:240) reads the start levels instead; the credit lines of every record change in those two fields and in nothing else (no birth, no take, no level, no count: the board is untouched). PR-S1's second half changes no course at all on this head (it is the head's own reading, bit for bit).** The course the refused reading (b) would change, with its numbers, for the owner's book: the refusals' names on every record (the hole 60 stop 9,146 to 9,314, orientation 248 to 96, twist 229 to 164, sense 9,274 to 9,323; the chiral 60 stop 9,371 to 9,586, orientation 110 to 69, twist 42 to 7, sense 10,393 to 10,254), the merger's premise over the record (33 to 18 and 50 to 32), the born pair's survival (2 of 32 to 30 of 32), and, by the quartet comparison's 42 of 42 taken back at the delay 1, the whole of the quartet legs' mergers.

## 8. Bugs, by file and line

- interval.py:229-233 with close.py:271 and 300-313: the close reads `plane_starts`, the board at the interval's start, and lays onto the stepped board. The lay's refusal (close.py:115, `owns` read at the start) therefore lays a child onto levels it never read: the residue, measured at 2 of 32 born pairs (the hole's interval 11 pair with the charges -+17,136 for -+18,000 and a current 5.24 x 10^19 at its next close). One moment for the close's reads and its writes is the item; under PR-S1 the moment is the start and the lay's refusal is to be read on the board the lay lands on.
- bodies.py:85-96 and decoder.py:240: the second moment in the close (`node.stepped`, the keys `re_stepped` and `im_stepped`), the doubling step 0 names; one array per record per interval carried for it (interval.py:67, 232-233, node.py:102).
- close.py:134-190 (the kit's standing note) reads the walls before the takes; merger.child_at lays after write_ends.
- readings.py:41-46: the orbit's table on a heavy quartet row (the standing memory bug; no 7-cube run here).
- The record's Node lines hold the carrier's lines alone, so a born pair's levels are readable only through the log: every number of this hand came from the log (premise_read.py imports nothing of the engine).

## 9. What was cut short, by name

- **The quartet's shape-4 row behind qc1's HQ_S1** (tools/derivations/open_items/H-Quartet-Children-1/hq_s1_replacements.json, 9,463 bytes, the copy /dev/shm/tmp/qc1/src_qc1 present): the two readings on a quartet row at the third lift (2580388913625285 over den), the axis along the track at N of M credits, Bell's cells by hq_reader.py's settings and the measurement clicks. The plane legs' chiral 3-cube at 60 on the carriage's own leg world (H-Quartet-Carriage-1/worlds/w_chiral3_p3.json with u_p3.json) was run under both readings and is in section 5; the quartet row itself was not reached inside the box. The number that matters and is owed: the quartet comparison's 42 of 42 pairs taken back at the delay 1 under (a) against the survival (b) predicts from 30 of 32.
- **The 48 under each reading** (clicks_48.py on the chiral 3-cube at 60, about 4 minutes a reading): not run. The head's count (3 equal, 45 apart) stands from The-Click-Beyond-Rule3_COMPARISON.md; the prediction (both readings 3 and 45, both premises bilinears of the Link read at both ends) is unmeasured.
- **The bodies 120**: not run (the two 60-interval records and the leg were run under both readings instead).
- No chain of this hand is still running.

## 10. The ledger row

item | derived | one-Node test | toy (records, numbers) | gates touched | Universe | spec | missing by name
---|---|---|---|---|---|---|---
The premise of the merger read (PR-S1) | the close's one moment and the stepped current's form den A (q_minus + q_plus), reading (a) required by the letter's words, by one act on every row alike and by the close's one reading | the premise read from the log at every born pair's next close (premise_read.py), 32 pairs on three records | the hole 60, the chiral 60, the chiral 3-cube at the leg p3 under both readings: the board equal, the refusals' names apart at the intervals 9, 5, 5; the rest premise 30 of 32 as laid against 2 of 32 stepped; the conservation 11 of 12 under (b) and 11 of 12 on the head; the run back 20 of 20 and 10 of 10 | gate 24 (the merger at rest) kept by (a) and halved by (b); gate 15's inequality unmet on the head alike | the record's length: the merger lands at the cycle's bottom (217 on ga2), where the two readings part on the board and not only in the names; the width: den A within 112 bits at every pair measured | PR-S1 above, the keys and the lines named in section 7 and 8; no new act, no number, no name | the quartet's shape-4 row, the 48 under each reading, the bodies 120, ga2 at 217 under (b) for gate 24
