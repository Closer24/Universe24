#!/bin/bash
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad; H=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf14/tools/derivations/open_items/H-Confirm-Build-14; PY=/home/user/Universe24/venv314/bin/python; export TMPDIR=/dev/shm/tmp
cd $S/hands/vf14
run() { nice -n 19 $PY -I $H/run_record.py $S/hands/vf14/src tests/worlds/$1.json $2 $3 $S/records/a796f299c/$1_$2.json > $H/logs/$1_$2.log 2>&1; echo "$1 $2 exit $?" >> $H/logs/done.txt; }
run world_hole 60 20 &
run world_chiral 60 20 &
run world_bodies 300 20 &
run world_pair_3 400 10 &
run world_universe 400 10 &
run world_plasma_3 170 10 &
wait
echo ALL >> $H/logs/done.txt
