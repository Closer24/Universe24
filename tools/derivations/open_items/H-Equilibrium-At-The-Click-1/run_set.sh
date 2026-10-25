#!/bin/sh
# one configuration over the three uniform worlds: run_set.sh <tag> <PYTHONPATH> [ENV=VALUE ...]
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
W=$S/hands/eq1/tests/worlds
OUT=$S/hands/eq1/tools/derivations/eq1/out
P=/home/user/Universe24/venv314/bin/python
tag=$1; shift; export PYTHONPATH=$1; shift
export TMPDIR=/dev/shm/tmp
for kv in "$@"; do export "$kv"; done
nice -n 19 $P eq1_run.py $W/world_pair_3.json $OUT/pair3_$tag back 10 > $OUT/pair3_$tag.txt 2>&1
nice -n 19 $P eq1_run.py $W/world_universe.json $OUT/universe_$tag back 10 > $OUT/universe_$tag.txt 2>&1
nice -n 19 $P eq1_run.py $W/world_plasma.json $OUT/plasma_$tag back 10 > $OUT/plasma_$tag.txt 2>&1
