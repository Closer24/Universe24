#!/bin/sh
# vf12: the cycle board of H-Births-Seed-On-Head-1 (ga2, 4-cube, cycle_m5_m0 at 5 quanta) to 450, back 10, under David's build e1209f752 with NO flag, and under the parent 99a9ee860 for contrast
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12/tools/derivations/open_items/H-Confirm-Build-12/cycle
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
env PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12/src:$D nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_vf12_450.json worlds/cycle_m5_m0.json back 10 > out/ga2_vf12_450.log 2>&1 &
env PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12/tools/derivations/open_items/H-Confirm-Build-12/parent/src:$D nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_parent_450.json worlds/cycle_m5_m0.json back 10 > out/ga2_parent_450.log 2>&1 &
wait
echo done > out/run_vf12.done
