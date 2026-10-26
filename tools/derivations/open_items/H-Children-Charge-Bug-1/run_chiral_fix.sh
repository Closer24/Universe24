#!/bin/bash
# The chiral 60 under the flag set and under David's patch (the tree /dev/shm/tmp/cc1/src_patched), one after the other, nice 19.
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cc1
F=$W/tools/derivations/open_items/H-Children-Charge-Bug-1
P=/home/user/Universe24/venv314/bin/python; export TMPDIR=/dev/shm/tmp; cd $F
CC1_LIGHT_EXACT=1 nice -n 19 $P run_flag.py /dev/shm/tmp/cc1/src_cc1 $W/tests/worlds/world_nature.json 60 10 > out/flag_chiral_set.json 2>&1
nice -n 19 $P run_flag.py /dev/shm/tmp/cc1/src_patched $W/tests/worlds/world_nature.json 60 10 > out/patched_chiral.json 2>&1
nice -n 19 $P run_flag.py $W/src $W/tests/worlds/world_nature.json 60 10 > out/flag_chiral_head.json 2>&1
echo chiral fix runs done >> /dev/shm/tmp/cc1/run_flags.log
