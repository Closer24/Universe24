#!/bin/sh
# rg1 batch G (no loop): the three records under the head and under the flag alone
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/rg1/tools/derivations/open_items/H-Births-Seed-On-Head-1
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/rg1
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
mkdir -p out/three
env PYTHONPATH=$W/src nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/hole_head.json back 10 > out/three/hole_head.log 2>&1 &
env PYTHONPATH=$D/src_rg1 CS4_TAKE_FARTHEST=1 nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/hole_far.json back 10 > out/three/hole_far.log 2>&1 &
env PYTHONPATH=$W/src nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/chiral_head.json back 10 > out/three/chiral_head.log 2>&1 &
env PYTHONPATH=$D/src_rg1 CS4_TAKE_FARTHEST=1 nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/chiral_far.json back 10 > out/three/chiral_far.log 2>&1 &
env PYTHONPATH=$W/src nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_bodies.json out/three/bodies_head.json back 10 > out/three/bodies_head.log 2>&1 &
env PYTHONPATH=$D/src_rg1 CS4_TAKE_FARTHEST=1 nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_bodies.json out/three/bodies_far.json back 10 > out/three/bodies_far.log 2>&1 &
wait
echo done > out/run_g.done
