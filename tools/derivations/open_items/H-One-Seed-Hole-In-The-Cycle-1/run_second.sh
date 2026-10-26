#!/bin/sh
# the four secondary candidates to 450, rerun after the first launch was cut short at 04:04 (the box's load); nice 19, TMPDIR=/dev/shm/tmp
H=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/os1
PY=/home/user/Universe24/venv314/bin/python
R=$H/tools/derivations/open_items/H-Lay-Rest-Mirror-2/run_record.py
W=$H/tools/derivations/open_items/H-One-Seed-Hole-In-The-Cycle-1/worlds
O=$H/tools/derivations/open_items/H-One-Seed-Hole-In-The-Cycle-1/out
export TMPDIR=/dev/shm/tmp PYTHONPATH=$H/src
cd $W
nice -n 19 $PY $R $H/src c1b_class2_4.json 450 10 $O/c1b_class2_4.json > $O/c1b_class2_4.summary 2>&1 &
nice -n 19 $PY $R $H/src c3_fixed_column_4.json 450 10 $O/c3_fixed_column_4.json > $O/c3_fixed_column_4.summary 2>&1 &
nice -n 19 $PY $R $H/src c5_hole_first_class0_4.json 450 10 $O/c5_hole_first_class0_4.json > $O/c5_hole_first_class0_4.summary 2>&1 &
nice -n 19 $PY $R $H/src c7_classes02_4.json 450 10 $O/c7_classes02_4.json > $O/c7_classes02_4.summary 2>&1 &
wait
