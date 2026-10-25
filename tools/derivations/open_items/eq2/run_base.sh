#!/bin/sh
# the head's src (the flag absent), every world with back 10
E=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/eq2/tools/derivations/eq2
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/eq2/src
export TMPDIR=/dev/shm/tmp
P=/home/user/Universe24/venv314/bin/python
cd $E
nice -n 19 $P -m event_universe.run worlds/world_pair_3.json out/base_pair_3.json back 10 > out/base_pair_3.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_universe.json out/base_universe.json back 10 > out/base_universe.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_plasma.json out/base_plasma.json back 10 > out/base_plasma.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_hole.json out/base_hole_60.json back 10 > out/base_hole_60.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_chiral.json out/base_chiral_60.json back 10 > out/base_chiral_60.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_bodies.json out/base_bodies_300.json back 10 > out/base_bodies_300.log 2>&1 &
wait
echo BASE_DONE
