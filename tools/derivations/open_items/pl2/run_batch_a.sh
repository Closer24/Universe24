#!/bin/sh
# pl2 batch A: the 5-cube plasma under n and n+kick (retrace, back 10), the 3-cube through the top (intervals 90, back 10), letters (a) and (ends) on the 3-cube; then the records under n and n+kick
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pl2/tools/derivations/pl2
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pl2/tests/worlds
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp PYTHONPATH=$D/src_pl2
cd $D
env CS7_EQ=n nice -n 19 $PY retrace.py $W/world_plasma.json 400 10 out/p5_n_400.json > out/p5_n_400.log 2>&1 &
env CS7_EQ=n PL2_CHARGE=kick nice -n 19 $PY retrace.py $W/world_plasma.json 400 10 out/p5_nkick_400.json > out/p5_nkick_400.log 2>&1 &
env CS7_EQ=n PL2_CHARGE=kick nice -n 19 $PY retrace.py $W/world_plasma_3.json 90 10 out/p3_nkick_90_back.json > out/p3_nkick_90_back.log 2>&1 &
env CS7_EQ=n PL2_SIGN_ODD=1 nice -n 19 $PY retrace.py $W/world_plasma_3.json 400 10 out/p3_nodd_400.json > out/p3_nodd_400.log 2>&1 &
wait
env CS7_EQ=n PL2_CHARGE=ends nice -n 19 $PY retrace.py $W/world_plasma_3.json 90 10 out/p3_nends_90_back.json > out/p3_nends_90_back.log 2>&1 &
env CS7_EQ=n PL2_CHARGE=ends nice -n 19 $PY retrace.py $W/world_plasma_3.json 400 10 out/p3_nends_400.json > out/p3_nends_400.log 2>&1 &
env CS7_EQ=n nice -n 19 $PY -m event_universe.run $W/world_hole.json out/hole_n.json back 10 > out/hole_n.log 2>&1 &
env CS7_EQ=n PL2_CHARGE=kick nice -n 19 $PY -m event_universe.run $W/world_hole.json out/hole_nkick.json back 10 > out/hole_nkick.log 2>&1 &
wait
env CS7_EQ=n nice -n 19 $PY -m event_universe.run $W/world_chiral.json out/chiral_n.json back 10 > out/chiral_n.log 2>&1 &
env CS7_EQ=n PL2_CHARGE=kick nice -n 19 $PY -m event_universe.run $W/world_chiral.json out/chiral_nkick.json back 10 > out/chiral_nkick.log 2>&1 &
env CS7_EQ=n nice -n 19 $PY -m event_universe.run $W/world_bodies.json out/bodies_n.json back 10 > out/bodies_n.log 2>&1 &
env CS7_EQ=n PL2_CHARGE=kick nice -n 19 $PY -m event_universe.run $W/world_bodies.json out/bodies_nkick.json back 10 > out/bodies_nkick.log 2>&1 &
wait
echo done > out/batch_a.done
