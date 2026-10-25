#!/bin/sh
# the head's src, unflagged: the three uniform worlds to 400, back 10
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
W=$S/hands/eq1/tests/worlds
export PYTHONPATH=${PYTHONPATH:-$S/hands/eq1/src} TMPDIR=/dev/shm/tmp
P=/home/user/Universe24/venv314/bin/python
OUT=$S/hands/eq1/tools/derivations/eq1/out
tag=${1:-base}
nice -n 19 $P -m event_universe.run $W/world_pair_3.json $OUT/pair3_$tag.json back 10 > $OUT/pair3_$tag.txt 2>&1
nice -n 19 $P -m event_universe.run $W/world_universe.json $OUT/universe_$tag.json back 10 > $OUT/universe_$tag.txt 2>&1
nice -n 19 $P -m event_universe.run $W/world_plasma.json $OUT/plasma_$tag.json back 10 > $OUT/plasma_$tag.txt 2>&1
