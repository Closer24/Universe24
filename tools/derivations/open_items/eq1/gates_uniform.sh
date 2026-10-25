#!/bin/sh
# the uniform boards through the writer and the gates reader under one configuration: gates_uniform.sh <tag> <PYTHONPATH> [ENV=VALUE ...]; the records deleted after the read
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
W=$S/hands/eq1/tests/worlds
OUT=$S/hands/eq1/tools/derivations/eq1/out
P=/home/user/Universe24/venv314/bin/python
tag=$1; shift; export PYTHONPATH=$1; shift
export TMPDIR=/dev/shm/tmp
for kv in "$@"; do export "$kv"; done
for w in pair_3 universe plasma; do
  nice -n 19 $P -m event_universe.run $W/world_$w.json /dev/shm/tmp/u_${w}_$tag.json back 10 > /dev/null 2>&1
  nice -n 19 $P -m event_universe.gates /dev/shm/tmp/u_${w}_$tag.json > $OUT/gates_u_${w}_$tag.txt 2>&1
  rm -f /dev/shm/tmp/u_${w}_$tag.json
done
