# H-Children-Charge-Bug-1 (cc1): the charge of a birth's two children

Head: toys-5 3dc12e307 (GP-S1, EX-S1, CR-S1/S2, RW-S1, MG-S1 in the code), src/ and tests/ unedited; the worktree's src run by the engine's own runner (run.py) and by run_flag.py; the flagged copy /dev/shm/tmp/cc1/src_cc1 (make_flagged_copy_cc1.py); David's patch cc1.patch. Every number an integer from the engine's log. Clock: started 07:17 UTC, the box 60 minutes.

## Verdict

**BUG, the engine's, at src/event_universe/merger.py:242-243 (rise_of: `if now == before: return k, 0, 0`), with its consequence at merger.py:276-277 (light_children: `if d == 0: dp, exact_lay = child_at(node, s, where, sense), None`)**: at a merger (MG-S1) whose named line at one end has no direction, the light at that end is laid as the charged child's lay (re_now sense A, im_before B: the Wronskian sense A B = -T div 2), while the other end is laid as the exact take at -1 on one line (Wronskian 0); the merger's two children then carry -18000 + 0, not 0. On the chiral 60 this is 2 of 16 births (the sum over the births -36000); on the hole 60 0 of 16 (no merger); on ga2 450 0 of 146 (128 of 128 merger ends have a direction). The children's own charge is otherwise exact: sense A B at every child's lay, -18000 and 18000, summing to 0 at 16 of 16 (hole), 14 of 16 (chiral), 146 of 146 (ga2).

**Beside it, a READING matter (the Reader's), not a bug of the lay**: what the log calls `W_children` (close.py:190 and merger.py:285: `cross(re.now, im.now, re.before, im.before)` read from the board after the lay) is the record's Wronskian at the Node, W_stood + W_own + the cross term (sense A im_before_stood + B re_now_stood), not the children's own; the Reader (clicks.py:187 gate 17, gates.py:222 the conservations in the clicks, predicates.py:148 row 27) reads its sign as the child's sense. Where the standing level exceeds A = 125 the read sign flips (the chiral's two - children at 117216 and 153072 read +1), and at every exact lay the Reader reads the standing plane's sign (ga2: 128 of 128). So on the head gate 17 reads SHOWN on the hole (sense sum 0, 2 children on a residue counted by name), NOT SHOWN on the chiral (sense sum 2) and on ga2 (sense sum 128). The earlier "SUM W 3149" (One-Algebra-2, section 8) and "4 of 17 births not 0" (A11) are this sum of the record's W, not of the children's.

## 1. The numbers per record (the head, the engine's own log; q1_births.py over the run.py records)

Per birth: W_own = the children's own Wronskian as laid (sense A B for child_at's lay (sense A, 0, 0, B); 0 for a merger's exact lay, one line moved); W_stood = the plane's W at the end before the lay (the log's `stood`); W_after = the log's `W_children` (the record's W after the lay); cross = W_after - W_stood - W_own, checked against the letter of child_at, sense A im_before_stood + B re_now_stood (identity failures 0 on the three records). A = 125, B = 144, A B = 18000 = T div 2 (T 36000).

| record | births | merger ends (exact lays) | births with SUM W_own = 0 | SUM W_own | births with SUM W_after = 0 | SUM W_after | SUM W_stood | SUM cross (sense A im_b / B re_n) | Reader's sense sum, gate 17 | run back |
|---|---|---|---|---|---|---|---|---|---|---|
| hole 60 (world_hole.json) | 16 | 0 | 16 of 16 | 0 | 15 of 16 | +864 | 0 | 864 (0 / 864) | 0, SHOWN | 10 of 10 |
| chiral 60 (world_nature.json) | 16 | 2 | 14 of 16 | -36000 | 14 of 16 | +270288 | 0 | 306288 (0 / 306288) | 2, NOT SHOWN | 10 of 10 |
| ga2 450 (world_ga2.json at 450) | 146 | 128 | 146 of 146 | 0 | 82 of 146 | +5513088 | 4747008 | 766080 (766080 / 0) | 128, NOT SHOWN | 10 of 10 |

The births not 0, by name:
- hole, i 21, Node [3,4,1], ends [3,4,1] and [3,4,0]: stood [4,0,0,0] and [2,0,0,0]; W_own [-18000, 18000] (sum 0); W_after [-17424, 18288] (sum +864 = 144 x 4 + 144 x 2: the child's B on im_before crossed with the standing re_now). The children are exact; the record's W carries the cross term.
- chiral, i 10, Node [4,3,2], ends [4,3,2] and [4,3,3]: stood [939,1175,0,0] and [1329,1112,0,0]; exact_lay [None, [re, 8, 1975118186587907929149]]; W_own [-18000, 0] (sum -18000); W_after [117216, 0] (the - child reads +1: 144 x 939 - 18000).
- chiral, i 11, Node [3,4,1], ends [3,4,0] and [3,4,1]: stood [1188,1265,0,0] and [1447,1279,0,0]; exact_lay [None, [re, 7, 1863556190220929722087]]; W_own [-18000, 0]; W_after [153072, 0].
- ga2: 64 merger births, every end an exact lay (W_own 0 and 0); W_after the standing wave's W plus the cross sense A im_before_stood: 64 births not 0 in W_after, 0 in W_own.

Beside the births: EX-S1's identity taken + remainder_was - remainder = booked at every take carrying the fields (hole 1669 of 1669, chiral 3137 of 3137, ga2 484 of 484; the merger's whole takes carry no remainder); the board's total W (the readings' `W total`) is not conserved between the marks on any record (hole 0 to -919, steps of thousands between the births), so the charge the law conserves is the children's own at the click, not the board's bilinear sum.

## 2. The law's letter

docs/ALGEBRA.md, **The charge at the click** (line 267): "a plane quantum laid by the count at the quarter turn carries A^2 = T div 2 per plane and the Wronskian sense A^2 = sense T / 2 at an empty Node, and the born pair's equal and opposite charges are the imaginary part of the Gaussian product: ... so the senses are +1 and -1 and the charges +T / 2 and -T / 2, summing to the parents' 0". The head clause **The Node** (line 23): "a whole quantum from each end laying a child at each end at opposite senses and taking from the light at each end what the lay books". GP-S1 is not in docs/ALGEBRA.md or docs/HIGHLIGHTS.md on this head (grep 0); it stands in The-Gap-Zero-Parity_COMPARISON.md section 3: "the light's children are laid with the charge's sign (re_now = s A at each end, im_before = B)". MG-S1 (merger.py's own docstring): "the light is laid at each end as the exact take at -1, on the line the take names, by the least count of levels at which the share rises by the wall (`rise_of`), as the child's lay where the line has no direction (`light_children`)".

So the letter asks W = 0 of the children alone (sense T / 2 each, "at an empty Node"); of the record on a standing plane it says nothing, and the cross term is the bilinear's own (W is quadratic in the levels: a lay on a standing plane adds sense A im_before + B re_now beside its own sense A B). The Reader already counts the children laid on a residue by name for the magnitude (clicks.py: "children laid on a residue of their plane (W the Node's, not the lay's)"), not for the sign.

## 3. The cause by file and line

- take.py:42-43 (fall_of): the line named is the one with the largest now^2 - before^2, "the first line where equal". At the chiral's - end the re line stands at now 939, before 1175 (its gap negative) and the im line at 0, 0 (gap 0, the largest), so the named line is the empty im line.
- merger.py:242-243 (rise_of): `if now == before: return k, 0, 0`, the count 0 where the named line has no direction.
- merger.py:276-277 (light_children): `if d == 0: dp, exact_lay = child_at(node, s, where, sense), None`: the light laid as the child's lay with the sense, the charge sense A B = -18000, while the + end's light is the exact lay on the re line (count 8 and 7, Wronskian 0). The merger's children: -18000 + 0.

The integer reason is a slot (the line named), not a rounding: the fall's criterion chooses the empty line, and the fallback lays a charge. The children's own W at every child_at lay is sense A B exactly (the lay (sense A, 0, 0, B) has the cross re_now im_before - im_now re_before = sense A B), so the pair's lay itself is right; the cross term in the record's W is the law of the bilinear, and the field named W_children in the log carries that record's W (close.py:190, merger.py:285).

## 4. The fix (the engine's) and the Reader's predicate

The smallest change, one function, no new function, no number: strike rise_of's guard (merger.py:242-243). The letter's own `u = 1 if now > before else -1` resolves the tie now = before as -1, as fall_of's `t = 1 if before > now else -1` resolves it; the rise is then x (w d^2 - d pull) over the weight on the empty line, the least count by the same doubling and bisection (the predicate rise(d) < wall is monotone from rise(0) = 0 on a quadratic opening up). With the guard gone, light_children's `d == 0` branch is dead and goes with it (4 lines out, the sense unused in its loop): cc1.patch, 20 lines changed in merger.py alone (the one-function form is the guard alone).

The flagged copy (CC1_LIGHT_EXACT; /dev/shm/tmp/cc1/src_cc1, make_flagged_copy_cc1.py, 2 exact replacements in merger.py):
- the flag empty, bit for bit the head: the hole 60 hash 38c116e69728a8f4 = the head's 38c116e69728a8f4; the chiral 60 hash 5d9145eda42bb94b = the head's 5d9145eda42bb94b (run_flag.py, node.state_hash at 60; out/flag_*_head.json and out/flag_*_empty.json).
- the flag set, the hole 60: the hash 38c116e69728a8f4, the head's bit for bit (no merger on the hole: predicted and measured).
- the flag set, the chiral 60 (prediction written before the run: every merger end an exact lay, SUM W_own 0 at 16 of 16, the walls booked unchanged, the course after i 10 changed): hash ee08166ababf50ae; births 16 (the head's 16); credits 3202 (3119); merger ends exact 4 of 4 (2 of 4); births with SUM W_own = 0 16 of 16 (14 of 16); SUM W_own 0 (-36000); booked 56201602523063789404411 (equal to the head's); taken 57962070949389209950879 (57954846101029617925997); the run back 10 of 10; integers 99, bits 115 (the head's 99 and 115); EX-S1's identity at 3220 of 3220 takes (the head 3137 of 3137); the merger births under the fix: i 10 exact [[im, -191, 1999659581406482313139], [re, 8, 1975118186587907929149]], i 11 exact [[im, -191, 1651171189626099503380], [re, 7, 1863556190220929722087]], W_own 0 and 0 at both; the log's W_children there [224425, 0] and [241615, 0] (the cross -191 x -1175 and -191 x -1265: the record's W, the Reader's matter), so the present Reader still reads the sense sum 2 on the fixed chiral (predicted), until the predicate below is built.
- David's patch (the tree /dev/shm/tmp/cc1/src_patched, the flag struck): the one-Node test passes; the chiral 60 hash ee08166ababf50ae, the flagged copy's bit for bit (predicted), the same counts.
- ga2 450 under the flag: predicted bit for bit the head (128 of 128 merger ends have a direction at the head, the flagged path never entered); NOT RUN within the box: the 1-minute load stood above 3 from 07:27 (poll_load.py waiting); the head's ga2 450 took 30 s.

The one Node (test_children_charge_cc1.py, the 3-cube, 0.2 to 0.4 s): the chiral's birth at i 10 laid by hand at (1,1,1) and (1,1,2) (re 939/1175 and 1329/1112, im 0), walls_of then light_children: on the head exact [None, [re, 12, 1671250041200833425780]], W_own [-18000, 0], FAILS; on the flagged copy with the flag set and on the patched tree exact [[im, -191, 1659468532287537189327], [re, 12, 1671250041200833425780]] (both rises at or above the walls 1654009903854256729287), W_own [0, 0], PASSES; on the copy with the flag empty FAILS as the head. Command: `PYTHONPATH=<src> pytest -q -s -p no:cacheprovider -o pythonpath=<src> test_children_charge_cc1.py` (the -o because pyproject's pythonpath = ["src"] puts the worktree's src first otherwise).

The sentence for the owner (MG-S1's fallback struck): "The merger's light is the exact take at -1 on the line the fall names at both ends; where that line has no direction the count's sign is the tie's own (-1, as the fall resolves it); the light is never the child's lay, which carries the charge sense T div 2, and the merger's two children carry the Wronskian 0 and 0."

The Reader's predicate, for Animate (gate 17 and the conservations in the clicks): a child's own charge is sense x (T div 2) at a child's lay (the birth's `exact_lay` None at that end, or no `exact_lay` key) and 0 at an exact lay (the light); the gate: the children's own charges summed over the births 0, each pair birth's two opposite, each merger birth's two 0; the magnitude T div 2 at every child's lay (the present reading, kept). The record's W after the lay (the log's `W_children`) is W_stood + W_own + (sense A im_before_stood + B re_now_stood): read for the residue by name, never for the sign. The equivalent engine-side spelling, no state touched: close.py:190 and merger.py:285 log the lay's own Wronskian (the cross of the laid levels) under `W_children`, the record's W under its own name.

## 5. The test

tools/derivations/open_items/H-Children-Charge-Bug-1/test_children_charge_cc1.py: one Node, under 1 s; fails on the head (out/test_head.txt), passes on the fix (out/test_fix.txt, out/test_patched.txt), fails on the copy with the flag empty (out/test_copy_flag_empty.txt).

## 6. Laws with a number under the fix (the chiral 60)

The children's own charge 0 at 16 of 16 births; the run back 10 of 10; the fixed count 99 integers and 115 bits (unchanged); the walls booked unchanged (56201602523063789404411) and every end paid by the exact take (EX-S1 at 3220 of 3220); integers only (grep float: 0 in the scripts); one act (the move, CR-S1) on the light at every merger end alike, no name, no number (the tie's sign the letter's own u); the one-Link reach untouched (the lay at the two ends of one Link). Not shown: the 48 on the clicks under the fix; the bodies record; ga2 under the flag.

## 7. What was cut short, by name

ga2 450 under the flag (the load rule; predicted bit for bit); the 48 on the clicks under the fix; the bodies 300; gate 17 on the fixed chiral under the Reader's predicate of section 4 (predicted 0; the present Reader reads 2).

## Files

q1_births.py (the per-birth decomposition), run_records.sh (the three head records by run.py), run_flag.py, run_flag_all.sh and run_chiral_fix.sh (the flagged copy and the patch against the head), make_flagged_copy_cc1.py, test_children_charge_cc1.py, poll_load.py, cc1.patch; out/ (q1_*.jsonl, flag_*.json, patched_chiral.json, run_*.txt, test_*.txt). The records themselves (4 to 10 MB) under /dev/shm/tmp/cc1/.
