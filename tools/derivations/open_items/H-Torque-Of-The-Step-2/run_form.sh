#!/bin/sh
# the measured form TQ2_FORM=1 on the flagged copy (/dev/shm/tmp/tq2copy/src) against the head's src, under nice
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../../tests/worlds
HEAD=../../../../src
COPY=/dev/shm/tmp/tq2copy/src
A48=../H-48-In-The-Clicks-3
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
# wave 1
TQ2_FORM=1 PYTHONPATH=$COPY run form_hole_60 $PY tq2_torque.py $W/world_hole.json out/form_hole_60.json 60 &
TQ2_FORM=1 PYTHONPATH=$COPY run form_chiral_60 $PY tq2_torque.py $W/world_chiral.json out/form_chiral_60.json 60 &
PYTHONPATH=$COPY run off_hole_60 $PY run_hash.py $W/world_hole.json 60 10 &
PYTHONPATH=$HEAD run head_hole_60 $PY run_hash.py $W/world_hole.json 60 10 &
wait
# wave 2
TQ2_FORM=1 PYTHONPATH=$COPY run form_hash_hole_60 $PY run_hash.py $W/world_hole.json 60 10 &
TQ2_FORM=1 run form_48_3cube_60 $PY $A48/run_48.py $COPY $A48/worlds/world_chiral_3_30.json 60 out/form_48_3cube_60.json &
TQ2_FORM=1 run form_ga2_450 $PY $A48/ga2_course.py $COPY $W/world_ga2.json 450 10 out/form_ga2_450.json 2,218,442 &
PYTHONPATH=$COPY run off_chiral_60 $PY run_hash.py $W/world_chiral.json 60 10 &
wait
# wave 3: the uniform boards, the form against the head
TQ2_FORM=1 PYTHONPATH=$COPY run form_pair_3_400 $PY run_hash.py $W/world_pair_3.json 400 &
PYTHONPATH=$HEAD run head_pair_3_400 $PY run_hash.py $W/world_pair_3.json 400 &
TQ2_FORM=1 PYTHONPATH=$COPY run form_plasma_3_170 $PY run_hash.py $W/world_plasma_3.json 170 &
PYTHONPATH=$HEAD run head_plasma_3_170 $PY run_hash.py $W/world_plasma_3.json 170 &
wait
TQ2_FORM=1 PYTHONPATH=$COPY run form_universe_400 $PY run_hash.py $W/world_universe.json 400 &
PYTHONPATH=$HEAD run head_universe_400 $PY run_hash.py $W/world_universe.json 400 &
PYTHONPATH=$HEAD run head_chiral_60 $PY run_hash.py $W/world_chiral.json 60 10 &
wait
echo all > out/run_form.done
