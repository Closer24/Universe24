#!/bin/sh
E=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/eq2/tools/derivations/eq2
export PYTHONPATH=$E/src_eq2
export TMPDIR=/dev/shm/tmp
export EQ2_CROSS=up
P=/home/user/Universe24/venv314/bin/python
cd $E
nice -n 19 $P -m event_universe.run worlds/world_pair_3.json out/up_pair_3.json back 10 > out/up_pair_3.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_universe.json out/up_universe.json back 10 > out/up_universe.log 2>&1 &
nice -n 19 $P -m event_universe.run worlds/world_plasma.json out/up_plasma.json back 10 > out/up_plasma.log 2>&1 &
wait
echo UP_DONE
