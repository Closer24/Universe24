#!/bin/sh
# H-Quartet-Carriage-2: the 5-cube controls (one quartet quantum over the envelope of width 2, at rest and moving), then the measurement 7-cube at lift3 and the 48 on the chiral 3-cube at lift3; one run at a time, the kit's wait_load before the runs above a minute.
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/qe2
F=$W/tools/derivations/open_items/H-Quartet-Carriage-2
K=$W/tools/derivations/open_items/H-Kit-48-Re-Cut-1
P=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=/dev/shm/tmp/qe2/src_qe2 HQ_S1=1 TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/qe2
run() { date -u >> /dev/shm/tmp/qe2/chain4.log; echo $1 >> /dev/shm/tmp/qe2/chain4.log; nice -n 19 $P -m event_universe.run $F/worlds/world_$1.json /dev/shm/tmp/qe2/$1.json back 20 > /dev/shm/tmp/qe2/$1.out 2>&1; }
run one5q100_60_lift3
run one5q100_60_mid
run one5q100_60_lift1
run one5q100_60_p3
run one5waveq100_60_lift3
run one5waveq100_60_mid
run one5waveq100_60_lift1
echo CONTROLS DONE >> /dev/shm/tmp/qe2/chain4.log
nice -n 19 $P $K/wait_load.py 3 >> /dev/shm/tmp/qe2/chain4.log 2>&1
run measure7_60_lift3
echo MEASURE DONE >> /dev/shm/tmp/qe2/chain4.log
nice -n 19 $P $K/wait_load.py 3 >> /dev/shm/tmp/qe2/chain4.log 2>&1
date -u >> /dev/shm/tmp/qe2/chain4.log
nice -n 19 $P $K/clicks_48.py $F/worlds/world_chiral3_60_lift3.json 60 /dev/shm/tmp/qe2/clicks48_chiral3_lift3.json cube 3 > /dev/shm/tmp/qe2/clicks48_chiral3_lift3.out 2>&1
echo CHAIN3 DONE >> /dev/shm/tmp/qe2/chain4.log
date -u >> /dev/shm/tmp/qe2/chain4.log
