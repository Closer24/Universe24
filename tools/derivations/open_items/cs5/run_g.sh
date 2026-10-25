#!/bin/sh
# cs5: the key records re-run and slimmed for the Boss's reading (no loop)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
cd $S/hands/cs5/tools/derivations/cs5
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
COPYC=$S/hands/cs5/tools/derivations/cs5/src_cs5c
CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs5_run.py worlds/empty4_hh3_800.json out/hh3_q5_m0_far_800.json worlds/cycle_m5_m0.json back 10 > out/hh3_q5_m0_far_800.log 2>&1 &
CS5_BIRTHS_UNTIL=2 CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs5_run.py worlds/empty4_hh3_800.json out/hh3_q5_m0_far_until2_800.json worlds/cycle_m5_m0.json back 10 > out/hh3_q5_m0_far_until2_800.log 2>&1 &
CS5_BIRTHS_UNTIL=1 CS4_TAKE_FARTHEST=1 CS4_LIGHT_NO_BODY=1 PYTHONPATH=$COPYC nice -n 19 $PY cs5_run.py worlds/empty4_ht6_400.json out/ht6_q5_far_until1_400.json worlds/cycle_m5.json back 10 > out/ht6_q5_far_until1_400.log 2>&1 &
wait
$PY shrink2.py out/hh3_q5_m0_far_800.json out/hh3_q5_m0_far_until2_800.json out/ht6_q5_far_until1_400.json > out/shrink2.txt 2>&1
echo done > out/run_g.done
