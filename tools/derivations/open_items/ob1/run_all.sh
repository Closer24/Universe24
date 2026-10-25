#!/bin/sh
# Hand ob1: the eight runs of ob1_run.py, launched together, each writing out/<name>.json and out/<name>.log
cd "$(dirname "$0")"
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/ob1/src TMPDIR=/dev/shm/tmp
P=/home/user/Universe24/venv314/bin/python
$P ob1_run.py toy/world_bodies.json 120 20 out/bodies_two.json > out/bodies_two.log 2>&1 &
$P ob1_run.py worlds/one_body.json 120 20 out/bodies_one.json > out/bodies_one.log 2>&1 &
$P ob1_run.py worlds/two_lifts.json 120 20 out/two_lifts.json > out/two_lifts.log 2>&1 &
$P ob1_run.py worlds/sea5.json 100 10 out/coulomb_like.json single 1 2,2,1 2 125 1 single 1 2,2,3 2 125 1 > out/coulomb_like.log 2>&1 &
$P ob1_run.py worlds/sea5.json 100 10 out/coulomb_unlike.json single 1 2,2,1 2 125 1 single 1 2,2,3 2 125 -1 > out/coulomb_unlike.log 2>&1 &
$P ob1_run.py worlds/sea5.json 100 10 out/coulomb_alone.json single 1 2,2,1 2 125 1 > out/coulomb_alone.log 2>&1 &
$P ob1_run.py worlds/empty5.json 100 10 out/coulomb_like_empty.json single 1 2,2,1 2 125 1 single 1 2,2,3 2 125 1 > out/coulomb_like_empty.log 2>&1 &
$P ob1_run.py worlds/empty5.json 100 10 out/coulomb_unlike_empty.json single 1 2,2,1 2 125 1 single 1 2,2,3 2 125 -1 > out/coulomb_unlike_empty.log 2>&1 &
wait
echo ALL DONE
