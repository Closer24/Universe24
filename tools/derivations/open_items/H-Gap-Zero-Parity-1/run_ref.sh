#!/bin/sh
# gp1: the head's own references on this base (the flags empty), the records' cache being 2ab32b518 without MG-S1
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
GP1_FORM= run ga2_off $PY ga2_course.py src_gp1 $W/tests/worlds/world_ga2.json 450 10 out/ga2_off.json 2,218,219,442 &
GP1_FORM= run chiral60_off $PY run_record.py src_gp1 $W/tests/worlds/world_chiral.json 60 10 out/chiral60_off.json &
wait
echo all > out/run_ref.done
