#!/bin/sh
# The v2 chain of H-Lay-As-The-Take-Reversed-2 (one carried division per far Node per close), one record at a time, wait_load before the long ones: the hole 60 and the chiral 60 with the kit's check, the 48 on the chiral 3-cube to 60, ga2 450 under the flag and under the head.
P=/home/user/Universe24/venv314/bin/python
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/lt2
K=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit
F=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/lt2/tools/derivations/open_items/H-Lay-As-The-Take-Reversed-2
O=/dev/shm/tmp/lt2
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=/dev/shm/tmp/lt2b/src_lt2b LT2_LAY_REVERSED=1
date -u > $O/v2.log
nice -n 19 $P -m event_universe.run $W/tests/worlds/world_hole.json $O/v2_hole60.json back 20 2>&1 | tail -2 >> $O/v2.log
nice -n 19 $P -m event_universe.run $W/tests/worlds/world_nature.json $O/v2_chiral60.json back 20 2>&1 | tail -2 >> $O/v2.log
nice -n 19 $P $K/conservation_check.py $O/v2_hole60.json out $O/cons_v2_hole60.json 2>&1 | grep -v "^{" >> $O/v2.log
nice -n 19 $P $K/conservation_check.py $O/v2_chiral60.json out $O/cons_v2_chiral60.json 2>&1 | grep -v "^{" >> $O/v2.log
date -u >> $O/v2.log
$P $K/wait_load.py 3 >> $O/v2.log
nice -n 19 $P $K/clicks_48.py $W/tests/worlds/world_nature.json 60 $O/c48_v2.json cube 3 2>&1 | tail -1 >> $O/v2.log
date -u >> $O/v2.log
$P $K/wait_load.py 3 >> $O/v2.log
nice -n 19 $P -m event_universe.run $F/worlds/world_ga2_450.json $O/v2_ga2_450.json back 10 2>&1 | tail -2 >> $O/v2.log
date -u >> $O/v2.log
export PYTHONPATH=$W/src LT2_LAY_REVERSED=
$P $K/wait_load.py 3 >> $O/v2.log
nice -n 19 $P -m event_universe.run $F/worlds/world_ga2_450.json $O/head_ga2_450_true.json back 10 2>&1 | tail -2 >> $O/v2.log
date -u >> $O/v2.log
echo DONE >> $O/v2.log
