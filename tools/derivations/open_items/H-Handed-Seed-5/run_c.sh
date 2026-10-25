#!/bin/sh
# cs5: the one-bang controls at 6 and 8 quanta (no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs5/tools/derivations/cs5
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
COPYC=$S/hands/cs5/tools/derivations/cs5/src_cs5c
CS5_BIRTHS_UNTIL=1 CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs5_run.py worlds/empty4_l4_400.json out/l4_q6_far_until1_400.json worlds/cycle_m6.json back 10 > out/l4_q6_far_until1_400.log 2>&1 &
CS5_BIRTHS_UNTIL=1 CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs5_run.py worlds/empty4_l4_400.json out/l4_q8_far_until1_400.json worlds/cycle_m8.json back 10 > out/l4_q8_far_until1_400.log 2>&1 &
wait
echo done > out/run_c.done
