#!/bin/sh
cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/am2
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/am2/src TMPDIR=/dev/shm/tmp
for w in hole chiral bodies pair_3 universe packet; do
  nice -n 19 /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Angular-Momentum-2/am2_angular.py tests/worlds/world_$w.json tools/derivations/open_items/H-Angular-Momentum-2/out/world_$w.L.json > tools/derivations/open_items/H-Angular-Momentum-2/out/world_$w.log 2>&1 &
done
wait
echo ALLDONE
