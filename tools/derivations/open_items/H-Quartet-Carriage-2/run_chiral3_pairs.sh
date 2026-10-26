#!/bin/sh
# H-Quartet-Carriage-2: the chiral seed on the 3-cube at 60 under HQ_S1, one run at a time, per candidate pair.
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/qe2
F=$W/tools/derivations/open_items/H-Quartet-Carriage-2
P=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=/dev/shm/tmp/qe2/src_qe2 HQ_S1=1 TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/qe2
nice -n 19 $P -m event_universe.run $F/worlds/world_chiral3_60_p3.json /dev/shm/tmp/qe2/chiral3_60_p3.json back 20 > /dev/shm/tmp/qe2/chiral3_60_p3.out 2>&1
nice -n 19 $P -m event_universe.run $F/worlds/world_chiral3_60_mid.json /dev/shm/tmp/qe2/chiral3_60_mid.json back 20 > /dev/shm/tmp/qe2/chiral3_60_mid.out 2>&1
nice -n 19 $P -m event_universe.run $F/worlds/world_chiral3_60_lift1.json /dev/shm/tmp/qe2/chiral3_60_lift1.json back 20 > /dev/shm/tmp/qe2/chiral3_60_lift1.out 2>&1
echo CHAIN1 DONE > /dev/shm/tmp/qe2/chain1.done
