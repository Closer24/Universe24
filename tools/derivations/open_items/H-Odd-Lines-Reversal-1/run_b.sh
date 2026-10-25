#!/bin/sh
# ol1's batch B (no loop): OL-S1 (OL1_ODD=exchkick) with PL-S1 on the beam (450; and 100 with the run back of 20 through the top), the three records, the zigzag z1m (head; PL-S1 + OL-S1) through ol1_run's pattern lay
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/ol1/tools/derivations/ol1
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/ol1/tests/worlds
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp PYTHONPATH=$D/src_ol1
cd $D
env OL1_PL=kick OL1_ODD=exchkick nice -n 19 $PY ol1_run.py worlds/beam4.json 450 10 out/beam_pl_ols1.json worlds/beam_wave.json > out/beam_pl_ols1.log 2>&1 &
env OL1_PL=kick OL1_ODD=exchkick nice -n 19 $PY ol1_run.py worlds/beam4.json 100 20 out/beam_pl_ols1_top.json worlds/beam_wave.json > out/beam_pl_ols1_top.log 2>&1 &
env OL1_PL=kick OL1_ODD=exchkick nice -n 19 $PY -m event_universe.run $W/world_hole.json out/hole_pl_ols1.json back 10 > out/hole_pl_ols1.log 2>&1 &
env OL1_PL=kick OL1_ODD=exchkick nice -n 19 $PY -m event_universe.run $W/world_chiral.json out/chiral_pl_ols1.json back 10 > out/chiral_pl_ols1.log 2>&1 &
wait
echo waveb1 > out/waveb1.done
env OL1_PL=kick OL1_ODD=exchkick nice -n 19 $PY -m event_universe.run $W/world_bodies.json out/bodies_pl_ols1.json back 10 > out/bodies_pl_ols1.log 2>&1 &
nice -n 19 $PY ol1_run.py worlds/zigzag4_400.json 400 10 out/z1m_head.json worlds/zigzag_m.json > out/z1m_head.log 2>&1 &
env OL1_PL=kick OL1_ODD=exchkick nice -n 19 $PY ol1_run.py worlds/zigzag4_400.json 400 10 out/z1m_pl_ols1.json worlds/zigzag_m.json > out/z1m_pl_ols1.log 2>&1 &
env OL1_PL=kick OL1_ODD=exchkick nice -n 19 $PY ol1_run.py worlds/empty4_450.json 450 10 out/ga2_pl_ols1.json worlds/cycle_m5_m0.json > out/ga2_pl_ols1.log 2>&1 &
wait
echo done > out/run_b.done
