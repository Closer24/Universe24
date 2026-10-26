#!/bin/sh
# H-Confirm-Build-21: the seven records at 8b1dbb781, launched together under nice 19.
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad; H=$S/hands/cb21/tools/derivations/open_items/H-Confirm-Build-21; R=$S/records/8b1dbb781
export PYTHONPATH=$S/hands/cb21/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
cd $S/hands/cb21
run() { ( start=$(date +%s); nice -n 19 $PY -m event_universe.run $1 $R/$2.json back $3 > $H/logs/run_$2.out 2>&1; echo "exit $? seconds $(($(date +%s)-start))" >> $H/logs/run_$2.out ) & }
run tests/worlds/world_universe.json world_universe_400 10
run tests/worlds/world_pair_3.json world_pair_3_400 10
run $H/worlds/world_plasma_3_170.json world_plasma_3_170 10
run $H/worlds/world_ga2_450.json world_ga2_450 10
run tests/worlds/world_hole.json world_hole_60 20
run tests/worlds/world_nature.json world_chiral_60 20
run tests/worlds/world_bodies.json world_bodies_300 20
wait
echo ALL_DONE > $H/logs/run_all.done
