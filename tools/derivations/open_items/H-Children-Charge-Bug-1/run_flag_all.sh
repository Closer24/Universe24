#!/bin/bash
# The flagged copy against the head: the flag empty (bit for bit) and set, on the hole 60, the chiral 60 and ga2 450; one at a time, nice 19.
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cc1
F=$W/tools/derivations/open_items/H-Children-Charge-Bug-1
P=/home/user/Universe24/venv314/bin/python; export TMPDIR=/dev/shm/tmp; cd $F
C=/dev/shm/tmp/cc1/src_cc1
$P make_flagged_copy_cc1.py
date -u
nice -n 19 $P run_flag.py $W/src $W/tests/worlds/world_hole.json 60 10 > out/flag_hole_head.json
nice -n 19 $P run_flag.py $C $W/tests/worlds/world_hole.json 60 10 > out/flag_hole_empty.json
CC1_LIGHT_EXACT=1 nice -n 19 $P run_flag.py $C $W/tests/worlds/world_hole.json 60 10 > out/flag_hole_set.json
nice -n 19 $P run_flag.py $W/src $W/tests/worlds/world_nature.json 60 10 > out/flag_chiral_head.json
nice -n 19 $P run_flag.py $C $W/tests/worlds/world_nature.json 60 10 > out/flag_chiral_empty.json
CC1_LIGHT_EXACT=1 nice -n 19 $P run_flag.py $C $W/tests/worlds/world_nature.json 60 10 > out/flag_chiral_set.json
date -u
$P poll_load.py
nice -n 19 $P run_flag.py $W/src /dev/shm/tmp/cc1/world_ga2_450.json 450 10 > out/flag_ga2_head.json
CC1_LIGHT_EXACT=1 nice -n 19 $P run_flag.py $C /dev/shm/tmp/cc1/world_ga2_450.json 450 10 > out/flag_ga2_set.json
date -u; echo done flags
