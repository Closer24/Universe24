#!/bin/sh
# a484: every measurement, written out (no loop)
cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/a484/tools/derivations/open_items/H-48-In-The-Clicks-4
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/a484
A484_READ=1 nice -n 19 $PY dump_48_cb13.py src_a484 $W 60 out/dump48_3cube_60_flag.json > out/dump48_3cube_60_flag.log 2>&1 &
A484_READ=1 nice -n 19 $PY run_record_cb13.py src_a484 $W/tests/worlds/world_ga2.json 230 10 out/ga2_flag_230.json > out/ga2_flag_230.log 2>&1 &
nice -n 19 $PY run_record_cb13.py src_a484 $W/tests/worlds/world_hole.json 60 10 out/hole_60_unflagged.json > out/hole_60_unflagged.log 2>&1 &
A484_READ=1 nice -n 19 $PY run_record_cb13.py src_a484 $W/tests/worlds/world_hole.json 60 10 out/hole_60_flag.json > out/hole_60_flag.log 2>&1 &
A484_READ=1 nice -n 19 $PY dump_48_world.py src_a484 worlds/world_chiral_5_60.json 60 out/dump48_5cube_60_flag.json images 8 > out/dump48_5cube_60_flag.log 2>&1 &
wait
echo done > out/run_all.done
