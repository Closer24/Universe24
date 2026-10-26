# H-Moving-Born-Pair-1 (mb1), the report (2026-10-26; the engine head b779335e1; the box 11:06 to 12:21 UTC)

The item: the carriage hands' candidate, the birth's lay as MV-S1's moving lay at the recoil's wave number, derived on the law's integers and measured behind the flag MB_S1 on top of qc1's HQ_S1. The derivation is DERIVATION.md; this report is the ledger of what was run, with the commands.

## The verdict line

Does not work (as a unification and as a lay), measured so: k per shape: on the massive plane rows h = 229,053,828,622 (the first lift) and about 2.6 x 10^15 (the heavy legs), on the quartet row about 2.6 x 10^15, on the gap-0 row 0; k rounds to 0 on no massive row, so no plane record is bit for bit (the hole 60 parts at the interval 8, the chiral 60 at 3, each at its first birth, as predicted before the runs); the born quartet pair survives the next close at 0 of 18 under the flag (2 of 2, 9 of 9, 7 of 7 taken back at the delay 1) against 0 of 18 at rest, by the theorem that a pair whose charges sum to 0 carries no current across its Link for any phase; the axis along the track 0 of 0 credits (no child credited); Bell's cells empty on the six settings, S undefined; the laws checked: the run back 20 of 20 on every flagged record, the flag empty bit for bit on both worlds, the one-Link reach by the form, integers only (floats 0), no name in src, the 128 bits reached (128 on two records, the product 3 s q), the 48 and the kit's conservation in section 3 of DERIVATION.md; the laws unmet under the flag: the children's charge unit (W per child 17,680 to 17,937 against 18,000; 70,932 to 71,780 against 72,000) and the births' charge summed to 0 on the quartet (5 of 18), both by the rounding toward zero of the phase's quotients, and MS-S1's booking (the wall the rest lay's share, the lay's share the moving lay's).

## The commands

    P=/home/user/Universe24/venv314/bin/python; W=<worktree>; F=$W/tools/derivations/open_items/H-Moving-Born-Pair-1; K=$W/tools/derivations/open_items/H-Kit-48-Re-Cut-1
    $P $F/mb_s1_replacements.py $F/mb_s1_replacements.json
    cd /dev/shm/tmp/mb1; nice -n 19 $P $K/make_flagged_copy.py mb1 MB_S1 $F/mb_s1_replacements.json src $W/src python $P   (out/flag_check.out: EQUAL, EQUAL)
    $P $F/predict_k.py /dev/shm/tmp/mb1/head_world_hole.json   (out/predict_hole60.json; the chiral alike)
    $P $F/chain.py   (the runs in order under nice 19, /dev/shm/tmp/mb1/chain.log; each record <name>.json beside it)
    $P $F/mb_reader.py <record> <out> [head <control>]   (out/read_*.json)
    $P <H-Quartet-Children-1>/hq_reader.py <record> /dev/shm/tmp/mb1/src_mb1 <out>   (out/hq_*.json)

## The runs and their numbers

See DERIVATION.md sections 1.5 (the predictions), 3.1 (the quartet pairs), 3.2 (the plane records), 3.3 (the laws), 3.4 (the measurement world, the bodies, the 48).

## Bugs by file and line

See DERIVATION.md section 7.

## What was cut short

The chiral 5-cube at 120 under the flag (the box); nothing else: every run of the brief but it landed, no chain still running.
