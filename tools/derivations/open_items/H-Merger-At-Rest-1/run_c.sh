#!/bin/sh
# mg1 batch C (no loop): the whole take with the light laid as the exact take at -1, ga2 to 450; the three records under it
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mg1/tools/derivations/mg1
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mg1
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=$D/src_mg1:$D
F="CS4_TAKE_FARTHEST=1 CS8_REST=1 CS8_MERGER_LAY=1 MG1_WALL=own MG1_TAKE=whole MG1_LAY=exact"
env $F nice -n 19 $PY cs6_run.py worlds/empty4_ga2_450.json out/ga2_exact_450.json worlds/cycle_m5_m0.json back 10 > out/ga2_exact_450.log 2>&1 &
(env $F nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/exact_hole.json back 10 > out/three/exact_hole.log 2>&1; env $F nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/exact_chiral.json back 10 > out/three/exact_chiral.log 2>&1) &
env $F nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_bodies.json out/three/exact_bodies.json back 10 > out/three/exact_bodies.log 2>&1 &
wait
echo done > out/run_c.done
