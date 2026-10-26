#!/bin/sh
# The long chain of H-Lay-As-The-Take-Reversed-2 under the flag, one record at a time, wait_load before each: the 48 on the chiral 3-cube to 60, ga2 450, the bodies 300 (the head's ga2 450 for the return beside it).
P=/home/user/Universe24/venv314/bin/python
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/lt2
K=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit
O=/dev/shm/tmp/lt2
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$O/src_lt2 LT2_LAY_REVERSED=1
date -u > $O/long.log
$P $K/wait_load.py 3 >> $O/long.log
nice -n 19 $P $K/clicks_48.py $W/tests/worlds/world_nature.json 60 $O/c48_flag.json cube 3 >> $O/long.log 2>&1
date -u >> $O/long.log
$P $K/wait_load.py 3 >> $O/long.log
nice -n 19 $P -m event_universe.run $W/tests/worlds/world_ga2.json $O/flag_ga2_450.json back 10 2>&1 | tail -3 >> $O/long.log
date -u >> $O/long.log
$P $K/wait_load.py 3 >> $O/long.log
nice -n 19 $P -m event_universe.run $W/tests/worlds/world_bodies.json $O/flag_bodies_300.json back 10 2>&1 | tail -3 >> $O/long.log
date -u >> $O/long.log
export PYTHONPATH=$W/src LT2_LAY_REVERSED=
$P $K/wait_load.py 3 >> $O/long.log
nice -n 19 $P -m event_universe.run $W/tests/worlds/world_ga2.json $O/head_ga2_450.json back 10 2>&1 | tail -3 >> $O/long.log
date -u >> $O/long.log
echo DONE >> $O/long.log
