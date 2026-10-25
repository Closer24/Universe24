#!/bin/sh
# rg1 batch B (no loop): the head with no flag over the quanta count and the lay's sense and mirror, 450 intervals, back 10
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/rg1/tools/derivations/open_items/H-Births-Seed-On-Head-1
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/rg1
cd $D
export TMPDIR=/dev/shm/tmp PYTHONPATH=$W/src:$D
PY=/home/user/Universe24/venv314/bin/python
nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_head_q6.json worlds/cycle_q6_m0.json back 10 > out/ga2_head_q6.log 2>&1 &
nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_head_q7.json worlds/cycle_q7_m0.json back 10 > out/ga2_head_q7.log 2>&1 &
nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_head_q8.json worlds/cycle_q8_m0.json back 10 > out/ga2_head_q8.log 2>&1 &
nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_head_q10.json worlds/cycle_q10_m0.json back 10 > out/ga2_head_q10.log 2>&1 &
nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_head_q12.json worlds/cycle_q12_m0.json back 10 > out/ga2_head_q12.log 2>&1 &
nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_head_q5_sm.json worlds/cycle_m5_m0_sm.json back 10 > out/ga2_head_q5_sm.log 2>&1 &
nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_head_q5_m1.json worlds/cycle_m5.json back 10 > out/ga2_head_q5_m1.log 2>&1 &
wait
echo done > out/run_b.done
