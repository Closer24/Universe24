set -e
P=/home/user/Universe24/venv314/bin/python
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cm2
export PYTHONPATH=/dev/shm/tmp/cm2/src_cm2 TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/cm2
ENDS_REVERSED=1 nice -n 19 $P -m event_universe.run $W/tests/worlds/world_nature.json /dev/shm/tmp/cm2/rev_nature.json back 20 > /dev/shm/tmp/cm2/rev_nature.txt
ONE_MOMENT=1 nice -n 19 $P -m event_universe.run $W/tests/worlds/world_nature.json /dev/shm/tmp/cm2/one_nature.json back 20 > /dev/shm/tmp/cm2/one_nature.txt
ONE_MOMENT=1 ENDS_REVERSED=1 nice -n 19 $P -m event_universe.run $W/tests/worlds/world_nature.json /dev/shm/tmp/cm2/onerev_nature.json back 20 > /dev/shm/tmp/cm2/onerev_nature.txt
ONE_MOMENT=1 nice -n 19 $P -m event_universe.run $W/tests/worlds/world_hole.json /dev/shm/tmp/cm2/one_hole.json back 20 > /dev/shm/tmp/cm2/one_hole.txt
echo DONE
