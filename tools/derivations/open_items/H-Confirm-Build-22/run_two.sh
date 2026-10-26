#!/bin/sh
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad; W=$S/hands/cb22; H=$W/tools/derivations/open_items/H-Confirm-Build-22; L=$H/logs; R=$S/records/8b1dbb781; O=/dev/shm/tmp/cb22/records
PY=/home/user/Universe24/venv314/bin/python; export TMPDIR=/dev/shm/tmp PYTHONPATH=$W/src; cd $W
run() { start=$(date +%s); nice -n 19 $PY -m event_universe.run $1 $O/$2.json back $3 > $L/run_$2.out 2>&1; echo "exit $? seconds $(($(date +%s)-start))" >> $L/run_$2.out; }
run /dev/shm/tmp/cb22/world_ga2_450.json world_ga2_450 10 &
run /dev/shm/tmp/cb22/world_plasma_3_170.json world_plasma_3_170 10 &
wait
for n in world_plasma_3_170 world_ga2_450; do echo "$n (second run, the universe file beside the world): $($PY $H/compare.py $O/$n.json $R/$n.json 2>&1 | tail -1 | cut -c1-600)" >> $H/compare_worlds.txt; done
echo TWO_DONE > $L/run_two.done
