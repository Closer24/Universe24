#!/bin/sh
# cs7 batch B (no loop): the survey of the second bang under CS7_EQ=n (3 workers), and beside it the three records (hole 60, chiral 60, bodies 300) under the flag absent, n and c
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs7/tools/derivations/cs7
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs7
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
mkdir -p out/survey out/three
CS7_EQ=n nice -n 19 $PY survey_cs7.py out/survey 3 0,1 p,m hh ht > out/survey_n.txt 2>&1 &
export PYTHONPATH=$D/src_cs7
nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/abs_hole.json back 10 > out/three/abs_hole.log 2>&1
CS7_EQ=n nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/n_hole.json back 10 > out/three/n_hole.log 2>&1
CS7_EQ=c nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/c_hole.json back 10 > out/three/c_hole.log 2>&1
nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/abs_chiral.json back 10 > out/three/abs_chiral.log 2>&1
CS7_EQ=n nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/n_chiral.json back 10 > out/three/n_chiral.log 2>&1
CS7_EQ=c nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/c_chiral.json back 10 > out/three/c_chiral.log 2>&1
nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_bodies.json out/three/abs_bodies.json back 10 > out/three/abs_bodies.log 2>&1
CS7_EQ=n nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_bodies.json out/three/n_bodies.json back 10 > out/three/n_bodies.log 2>&1
CS7_EQ=c nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_bodies.json out/three/c_bodies.json back 10 > out/three/c_bodies.log 2>&1
echo done > out/three/done
wait
echo done > out/run_b.done
