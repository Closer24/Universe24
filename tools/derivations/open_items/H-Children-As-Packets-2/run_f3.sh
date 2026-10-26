#!/bin/sh
# cp2: the bodies and the Compton world on the second copy
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
SRC=/dev/shm/tmp/cp2/src_cp2
O=/dev/shm/tmp/cp2/out
W=../../../..
R=../../../../../../records/2ab32b518
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
CP2_FORM=1 run bodies300_f2 $PY run_record.py $SRC $W/tests/worlds/world_bodies.json 300 10 $O/bodies300_f2.json $R/world_bodies_300.json &
CP2_FORM=1 run compton60_f2 $PY run_record.py $SRC worlds/world_compton.json 60 10 $O/compton60_f2.json &
wait
echo all > out/run_f3.done
