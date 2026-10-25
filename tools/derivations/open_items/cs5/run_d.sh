#!/bin/sh
# cs5: the alike bang's records (no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs5/tools/derivations/cs5
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
COPYC=$S/hands/cs5/tools/derivations/cs5/src_cs5c
CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs5_run.py worlds/empty4_lift7_400.json out/lift7_q5_far_400.json worlds/cycle_m5.json back 10 > out/lift7_q5_far_400.log 2>&1 &
CS5_BIRTHS_UNTIL=1 CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs5_run.py worlds/empty4_lift7_400.json out/lift7_q5_far_until1_400.json worlds/cycle_m5.json back 10 > out/lift7_q5_far_until1_400.log 2>&1 &
wait
CS5_BIRTHS_UNTIL=2 CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs5_run.py worlds/empty4_lift5_400.json out/lift5_q5_m0_far_until2_400.json worlds/cycle_m5_m0.json back 10 > out/lift5_q5_m0_far_until2_400.log 2>&1 &
CS5_BIRTHS_UNTIL=2 CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs5_run.py worlds/empty4_lift6_400.json out/lift6_q5_m0_far_until2_400.json worlds/cycle_m5_m0.json back 10 > out/lift6_q5_m0_far_until2_400.log 2>&1 &
wait
echo done > out/run_d.done
