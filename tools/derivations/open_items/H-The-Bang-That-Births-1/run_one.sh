#!/bin/sh
set -e
P=/home/user/Universe24/venv314/bin/python
D="$1"; W="$2"; B="$3"; BACK="$4"
export PYTHONPATH="$W/src" TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/bb1
nice -n 19 $P -m event_universe.run "$D/worlds/$B.json" "/dev/shm/tmp/bb1/$B.json" back "$BACK" > "/dev/shm/tmp/bb1/$B.out" 2>&1
nice -n 19 $P "$D/read_record.py" "/dev/shm/tmp/bb1/$B.json" "$D/out/$B.tsv" 1
