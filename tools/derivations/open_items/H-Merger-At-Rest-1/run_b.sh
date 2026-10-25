#!/bin/sh
# mg1 batch B (no loop): the three records under the stack (the merger at rest, the own wall, the whole take) and the controls (every flag absent), the gates reader on the ga2 records
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mg1/tools/derivations/mg1
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mg1
cd $D
export TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=$D/src_mg1:$D
F="CS4_TAKE_FARTHEST=1 CS8_REST=1 CS8_MERGER_LAY=1 MG1_WALL=own MG1_TAKE=whole MG1_LOG_WALLS=1"
mkdir -p out/three
(env $F nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/whole_hole.json back 10 > out/three/whole_hole.log 2>&1; env $F nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/whole_chiral.json back 10 > out/three/whole_chiral.log 2>&1) &
(nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_hole.json out/three/abs_hole.json back 10 > out/three/abs_hole.log 2>&1; nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_chiral.json out/three/abs_chiral.json back 10 > out/three/abs_chiral.log 2>&1) &
env $F nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_bodies.json out/three/whole_bodies.json back 10 > out/three/whole_bodies.log 2>&1 &
nice -n 19 $PY -m event_universe.run $W/tests/worlds/world_bodies.json out/three/abs_bodies.json back 10 > out/three/abs_bodies.log 2>&1 &
wait
nice -n 19 $PY -m event_universe.gates out/ga2_whole_450.json > out/ga2_whole_450_gates.jsonl 2>&1
nice -n 19 $PY -m event_universe.gates out/ga2_ctrl_450.json > out/ga2_ctrl_450_gates.jsonl 2>&1
echo done > out/run_b.done
