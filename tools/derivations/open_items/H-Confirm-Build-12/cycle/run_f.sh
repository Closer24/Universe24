#!/bin/sh
# rg1 batch F (no loop): the flagged copy to 800 under the take by the fall's sign
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/rg1/tools/derivations/open_items/H-Births-Seed-On-Head-1
cd $D
export TMPDIR=/dev/shm/tmp PYTHONPATH=$D/src_rg1:$D CS4_TAKE_FARTHEST=1
nice -n 19 /home/user/Universe24/venv314/bin/python cs6_run.py worlds/empty4_ga2_800.json out/ga2_far_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_far_800.log 2>&1
echo done > out/run_f.done
