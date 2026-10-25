#!/bin/sh
# pl2 batch B: the momentum-kick write (src_pl2b, PL2_WRITE=kick) on the 3-cube and 5-cube plasma to 400 back 10, the 3-cube through the top (90, back 10), the heavy pair and the conjugate pair 3-cube; then the records under n+kick-write
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pl2/tools/derivations/pl2
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pl2/tests/worlds
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp PYTHONPATH=$D/src_pl2b
cd $D
env CS7_EQ=n PL2_WRITE=kick nice -n 19 $PY retrace.py $W/world_plasma_3.json 400 10 out/p3_nkw_400.json > out/p3_nkw_400.log 2>&1 &
env CS7_EQ=n PL2_WRITE=kick nice -n 19 $PY retrace.py $W/world_plasma.json 400 10 out/p5_nkw_400.json > out/p5_nkw_400.log 2>&1 &
env CS7_EQ=n PL2_WRITE=kick nice -n 19 $PY retrace.py $W/world_plasma_3.json 90 10 out/p3_nkw_90_back.json > out/p3_nkw_90_back.log 2>&1 &
env CS7_EQ=n PL2_WRITE=kick nice -n 19 $PY retrace.py $W/world_universe.json 400 10 out/u5_nkw_400.json > out/u5_nkw_400.log 2>&1 &
wait
env CS7_EQ=n PL2_WRITE=kick nice -n 19 $PY -m event_universe.run $W/world_hole.json out/hole_nkw.json back 10 > out/hole_nkw.log 2>&1 &
env CS7_EQ=n PL2_WRITE=kick nice -n 19 $PY -m event_universe.run $W/world_chiral.json out/chiral_nkw.json back 10 > out/chiral_nkw.log 2>&1 &
env CS7_EQ=n PL2_WRITE=kick nice -n 19 $PY -m event_universe.run $W/world_bodies.json out/bodies_nkw.json back 10 > out/bodies_nkw.log 2>&1 &
env CS7_EQ=n PL2_WRITE=kick nice -n 19 $PY retrace.py $W/world_pair_3.json 400 10 out/c3_nkw_400.json > out/c3_nkw_400.log 2>&1 &
wait
nice -n 19 $PY -m event_universe.run $W/world_hole.json out/hole_head.json back 10 > out/hole_head.log 2>&1 &
nice -n 19 $PY -m event_universe.run $W/world_chiral.json out/chiral_head.json back 10 > out/chiral_head.log 2>&1 &
nice -n 19 $PY -m event_universe.run $W/world_bodies.json out/bodies_head.json back 10 > out/bodies_head.log 2>&1 &
wait
echo done > out/batch_b.done
