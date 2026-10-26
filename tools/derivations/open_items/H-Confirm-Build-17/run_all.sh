#!/bin/sh
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf17/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf17/tests/worlds; O=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/records/16711fe5e; L=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf17/tools/derivations/open_items/H-Confirm-Build-17/logs
cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf17
run() { ( s0=$(date +%s); nice -n 19 $PY -m event_universe.run $1 $O/$2.json back $3 > $L/$2.out 2>&1; echo "exit $? seconds $(( $(date +%s) - s0 ))" >> $L/$2.out ) & }
run $W/world_hole.json world_hole_60 20
run $W/world_chiral.json world_chiral_60 20
run $W/world_pair_3.json world_pair_3_400 10
run /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf17/tools/derivations/open_items/H-Confirm-Build-17/worlds/world_plasma_3_170.json world_plasma_3_170 10
run $W/world_bodies.json world_bodies_300 20
run $W/world_universe.json world_universe_400 10
run /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf17/tools/derivations/open_items/H-Confirm-Build-17/worlds/world_ga2_450.json world_ga2_450 10
wait
echo ALL DONE > $L/ALL_DONE
