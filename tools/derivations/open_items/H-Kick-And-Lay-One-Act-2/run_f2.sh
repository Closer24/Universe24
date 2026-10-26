#!/bin/sh
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
SRC=/dev/shm/tmp/kl2/src_kl2
W=../../../..
R=../../../../../../records/2ab32b518
O=/dev/shm/tmp/kl2/out
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
( KL2_FORM=2 run hole60_f2 $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_f2.json $R/world_hole_60.json ) &
( KL2_FORM=2 run chiral60_f2 $PY run_record.py $SRC $W/tests/worlds/world_chiral.json 60 10 $O/chiral60_f2.json $R/world_chiral_60.json ) &
wait
echo all > out/run_f2.done
