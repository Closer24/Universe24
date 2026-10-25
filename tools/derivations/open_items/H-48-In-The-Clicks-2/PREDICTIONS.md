# a48b: the predictions, written before each run (the measurement under each after it)

## Run 1: chiral 3-cube at 30 (world_chiral_3_30.json, the seed of fd1's 3-cube wrapped: [2,1,3] -> [2,1,0]), the default engine, 48 images
Predicted: criterion A (pm2's tuple): 24 rotations equal / 0 exchanged / 24 apart, because a birth's tuple holds (minus Node, plus Node) in place and the conjugate swaps them, so "exchanged" is unreachable on any birth under A.
Criterion B and C: 24 equal (det +1) / 24 senses exchanged (det -1) / 0 apart, PROVIDED the odd lines stay at 0 through the run (no current written from gapped children).
The state through the image: scalars 0 mismatches at every interval; odd levels 0 (signed); the ones' complement carry fails from interval 1 (the lay's gauge: the remainder w/2 is not its own ones' complement); the two's complement carry fails from the first turn (a turned Node's remainder w/2 - 1 is not its own two's complement); the turn-parity carry 0 mismatches through the whole run.

Measured (run 1, out/c48_chiral3_30_default.json, 78 s): A 12 equal / 0 / 36 apart (rotations 12 / 0 / 12, reflections 0 / 0 / 24); B and C the same 12 / 0 / 36. The base births 5, credits 1, turns 122; the odd lines moved (max level 2), gapped levels 64: the proviso of the prediction failed (gapped children were born and the odd lines moved), so B and C part on the images that negate an axis whose odd line moved and on every reflection. The ones' carry fails at interval 1 (54 and 81 odd remainders), the two's carry at interval 1 at the turned Nodes (2 and 3), the parity carry 0 on the odd lines through the run; its first mismatch is a plane's im line (interval 2 / 6), the conjugation the comparison did not carry: the reflected world is the conjugate (im negated, the senses exchanged), so the im lines and the shape-4 row's time line are odd under det -1 and the odd lines axial (det s_a). The first parting draw: image 46 at interval 4 (one digit differs: a plane's im line, slot +X), image 47 at interval 6 (two digits: the odd lines x and z at the -Z neighbour).

## Run 2: the flag off against src, bit for bit
Predicted: the record of world_chiral_3_30 (log, counts, turns, run back) sha256-equal between PYTHONPATH=src and PYTHONPATH=src_a48b with A48B_FOLD unset.

## Run 3: chiral 3-cube at 30, the comparison with the conjugation carried, default (flag off), 48 images
Predicted: every logged digit's remainder sits on its lattice at the residue 0 or F - 1 (100 percent; the residue the Node's turn parity); under the parity carry with the conjugation 0 mismatches at every interval before the first parting draw, on every image; the first parting draw's folded multisets: "ones" (fd1's) NOT equal, "lattice" equal, on every parting image.

## Run 4: chiral 3-cube at 30 with A48B_FOLD=lattice
Predicted: B and C 24 equal / 24 senses exchanged / 0 apart; A 24 / 0 / 24 (A cannot see an exchange); the base's births change from the default's 5 (the draw's numbers change at every draw).

## Run 5: chiral 3-cube at 30 with A48B_FOLD=ones (fd1's fold)
Predicted: reflections apart (24), rotations partly apart (those negating an axis whose odd line or im digits are read): fd1's pattern, not a mend.

## Run 6: chiral 5-cube at 24: default, lattice, ones
Predicted: default 24 rotations equal / reflections apart in B where a conjugation-odd digit was read before the end (pm2 measured A 24 / 0 / 24); lattice 24 / 24 / 0; ones: reflections apart.

## Run 7: the records under the flag off and lattice (hole 60, chiral 300, bodies 120), back 10
Predicted: the flag off equals the engine's own record (the hash as run 2); under lattice the run back 10 of 10 on every record, the charge 0 at every birth (every pair at opposite W), taken at or above booked; the counts change where a draw changed the plane drawn (births, credits, turns differ from the default's; the hole 60 seed has a mirror plane and births nothing under the twist in both: 0 births, bit for bit).

## Run 8: the one-Node test (test_a48b_one_node.py)
Predicted: every identity 20,000 of 20,000 (the ties apart); the lattice fold equal at r and its carry 20,000 of 20,000; fd1's ones' fold equal in fewer than half.

Measured (run 3 residues, a48b_residues.py on the chiral 3-cube at 30, 120 draws): the residues of the remainders on their lattices are NOT confined to {0, F - 1}: on the shape-4 row's odd lines 180 of 720 neighbour slots "other", on the planes' im lines up to 402 of 720; the wall moves with X each interval and the residue drifts. So the lattice fold (delta = ceil(r / F)) is exact only on the residues 0 and F - 1 and off by one elsewhere; the exact fold needs the turn parity, which the state holds as the walled row's remainder at the wall 2 (the frame bit, complemented at every swap, unchanged by its own act since its flux 2 cphi is even).

## Run 9: the "frame" fold: rho = mirrored(r, W, 1 - b), b the walled row's remainder at the slot's Node at the start; the digit min(rho, (W - rho) mod W) div F, base (W div F) div 2 + 1
Predicted: chiral 3-cube at 30: B and C 24 equal / 24 senses exchanged / 0 apart (exact, no residue condition; the ties of the riding division and of the odd rounding the only exceptions, none expected in 30 intervals); A 24 / 0 / 24. The chiral 5-cube at 24 the same. The records: run back 10 of 10, the charge 0 at every birth, taken at or above booked; the counts differ from the default's where a draw changed.

Measured (runs 4, 5, 9): lattice 3-cube at 30: rotations 24 equal / reflections 24 apart (B, C); 5-cube at 24 the same; ones (fd1's): rotations 24 / reflections 24 apart; frame: rotations 24 / reflections 24 apart. Every fold mends the rotations (24 of 24 from the default's 12) and none the reflections. The cause read from the state comparison (run 3, out/c48_chiral3_30_off.json, state_first_mismatch under the parity carry): an im line's remainder at a turned Node is NOT carried by the parity rule: the exchange mirrors an im line's rotation remainder twice per turn (the identity: node.exchange, "an im line's rotation remainder is left"), so an im line's carry under the conjugation is the two's complement at every Node, while the shape-4 row's time line and odd lines (mirrored once per turn) carry by the turn parity. The frame fold mirrored every line once per turn and so broke the im lines at the turned Nodes (off by 2).

## Run 10: "frame2": rho = mirrored(r, W, (1 - b) x (1 + [the line is an im line])), the exchange's own count of reversals; digit min(rho, (W - rho) mod W) div F, base (W div F) div 2 + 1
Predicted: chiral 3-cube at 30 and 5-cube at 24: B and C 24 equal / 24 senses exchanged / 0 apart; the records: run back 10 of 10, the charge 0, taken at or above booked.
