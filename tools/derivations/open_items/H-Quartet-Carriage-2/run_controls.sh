#!/bin/sh
# H-Quartet-Carriage-2: the control worlds, one run at a time (each about 5 to 10 s on the 3-cube).
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/qe2
F=$W/tools/derivations/open_items/H-Quartet-Carriage-2
P=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=/dev/shm/tmp/qe2/src_qe2 HQ_S1=1 TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/qe2
run() { nice -n 19 $P -m event_universe.run $F/worlds/world_$1.json /dev/shm/tmp/qe2/$1.json back 20 > /dev/shm/tmp/qe2/$1.out 2>&1; }
run one3_60_lift3
run one3_60_mid
run one3_60_p3
run one3_60_lift1
run pairrest3_60_lift3
run pairrest3_60_mid
run pairwave3_60_lift3
run pairwave3_60_mid
run pairrest3_60_p3
run pairrest3_60_lift1
run pairwave3_60_p3
run pairwave3_60_lift1
echo CHAIN2 DONE > /dev/shm/tmp/qe2/chain2.done
