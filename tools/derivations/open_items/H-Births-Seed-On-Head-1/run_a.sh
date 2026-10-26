#!/bin/sh
# rg1 batch A (no loop): ga2 to 450 on the head (no flag), on src_rg1 under CS4_TAKE_FARTHEST=1, on src_rg1 with the flag absent; the head to 800; the flag-absent check
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/rg1/tools/derivations/open_items/H-Births-Seed-On-Head-1
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/rg1
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
env PYTHONPATH=$W/src:$D nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_head_450.json worlds/cycle_m5_m0.json back 10 > out/ga2_head_450.log 2>&1 &
env PYTHONPATH=$D/src_rg1:$D CS4_TAKE_FARTHEST=1 nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_far_450.json worlds/cycle_m5_m0.json back 10 > out/ga2_far_450.log 2>&1 &
env PYTHONPATH=$D/src_rg1:$D nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_copy_450.json worlds/cycle_m5_m0.json back 10 > out/ga2_copy_450.log 2>&1 &
env PYTHONPATH=$W/src:$D nice -n 19 $PY cs6_run.py worlds/empty4_ga2_800.json out/ga2_head_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_head_800.log 2>&1 &
nice -n 19 $PY check_flag_absent.py > out/check_flag_absent.txt 2>&1 &
wait
echo done > out/run_a.done
