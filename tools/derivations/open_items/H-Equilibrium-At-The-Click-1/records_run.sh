#!/bin/sh
# the three records under one configuration through the writer and the gates reader: records_run.sh <tag> <PYTHONPATH> [ENV=VALUE ...]; the record files deleted after the read (above 1.5 MB), the gates and the counts kept
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
W=$S/hands/eq1/tests/worlds
OUT=$S/hands/eq1/tools/derivations/eq1/out
P=/home/user/Universe24/venv314/bin/python
tag=$1; shift; export PYTHONPATH=$1; shift
export TMPDIR=/dev/shm/tmp
for kv in "$@"; do export "$kv"; done
for w in hole chiral bodies; do
  nice -n 19 $P -m event_universe.run $W/world_$w.json /dev/shm/tmp/${w}_$tag.json back 10 > $OUT/rec_${w}_$tag.txt 2>&1
  nice -n 19 $P -m event_universe.gates /dev/shm/tmp/${w}_$tag.json > $OUT/gates_${w}_$tag.txt 2>&1
  nice -n 19 $P -I $S/hands/eq1/tools/derivations/eq1/credits_read.py /dev/shm/tmp/${w}_$tag.json > $OUT/credits_${w}_$tag.txt 2>&1
  rm -f /dev/shm/tmp/${w}_$tag.json
done
