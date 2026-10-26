#!/bin/sh
# H-Confirm-Build-21: the three uniform boards at e708e778c (GP-S1 alone), nice 19.
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad; H=$S/hands/cb21/tools/derivations/open_items/H-Confirm-Build-21; R=$S/records/e708e778c
export PYTHONPATH=$S/hands/cb21gp/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
cd $S/hands/cb21gp
run() { ( start=$(date +%s); nice -n 19 $PY -m event_universe.run $1 $R/$2.json back $3 > $H/logs/gp_run_$2.out 2>&1; echo "exit $? seconds $(($(date +%s)-start))" >> $H/logs/gp_run_$2.out ) & }
run $H/worlds/world_plasma_3_170.json world_plasma_3_170 10
run tests/worlds/world_pair_3.json world_pair_3_400 10
run tests/worlds/world_universe.json world_universe_400 10
wait
echo ALL_DONE > $H/logs/run_gp.done
