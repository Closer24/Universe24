#!/bin/sh
# cs8 batch B (no loop): R1 (the merger at rest at every interval) and R2 (the pair's click) on ga2 to 800; the three records under R1
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs8/tools/derivations/cs8
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs8
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=$D/src_cs8:$D
F="CS4_TAKE_FARTHEST=1 CS7_EQ=n CS8_MERGER_LAY=1"
env $F CS8_REST=1 nice -n 19 $PY cs6_run.py worlds/empty4_ga2_800.json out/ga2_r1_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_r1_800.log 2>&1 &
env $F CS8_REST=2 nice -n 19 $PY cs6_run.py worlds/empty4_ga2_800.json out/ga2_r2_800.json worlds/cycle_m5_m0.json back 10 > out/ga2_r2_800.log 2>&1 &
mkdir -p out/three
(env $F CS8_REST=1 nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/r1_hole.json back 10 > out/three/r1_hole.log 2>&1; env $F CS8_REST=1 nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/r1_chiral.json back 10 > out/three/r1_chiral.log 2>&1; env $F CS8_REST=2 nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/r2_hole.json back 10 > out/three/r2_hole.log 2>&1; env $F CS8_REST=2 nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/r2_chiral.json back 10 > out/three/r2_chiral.log 2>&1) &
wait
env $F CS8_REST=1 nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_bodies.json out/three/r1_bodies.json back 10 > out/three/r1_bodies.log 2>&1 &
env $F CS8_REST=2 nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_bodies.json out/three/r2_bodies.json back 10 > out/three/r2_bodies.log 2>&1 &
wait
echo done > out/run_b.done
