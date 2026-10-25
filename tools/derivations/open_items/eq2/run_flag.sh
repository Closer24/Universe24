#!/bin/sh
# the flagged copy under EQ2_CLICK=$1, every world with back 10, in parallel
E=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/eq2/tools/derivations/eq2
export PYTHONPATH=$E/src_eq2
export TMPDIR=/dev/shm/tmp
export EQ2_CLICK=$1
P=/home/user/Universe24/venv314/bin/python
cd $E
nice -n 19 $P -m event_universe.run worlds/world_pair_3.json out/$1_pair_3.json back 10 > out/$1_pair_3.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_universe.json out/$1_universe.json back 10 > out/$1_universe.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_plasma.json out/$1_plasma.json back 10 > out/$1_plasma.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_hole.json out/$1_hole_60.json back 10 > out/$1_hole_60.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_chiral.json out/$1_chiral_60.json back 10 > out/$1_chiral_60.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_bodies.json out/$1_bodies_300.json back 10 > out/$1_bodies_300.log 2>&1 &
wait
echo FLAG_$1_DONE
