#!/bin/sh
# ol1's batch (no loop): every command written out; waves of four at nice 19
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/ol1/tools/derivations/ol1
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/ol1/tests/worlds
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp PYTHONPATH=$D/src_ol1
cd $D
# wave 1: the cycle board ga2 (head; PL-S1 + letter A) and the beam (head; PL-S1)
nice -n 19 $PY ol1_run.py worlds/empty4_450.json 450 10 out/ga2_head.json worlds/cycle_m5_m0.json > out/ga2_head.log 2>&1 &
env OL1_PL=kick OL1_ODD=exch nice -n 19 $PY ol1_run.py worlds/empty4_450.json 450 10 out/ga2_pl_ola.json worlds/cycle_m5_m0.json > out/ga2_pl_ola.log 2>&1 &
nice -n 19 $PY ol1_run.py worlds/beam4.json 450 10 out/beam_head.json worlds/beam_wave.json > out/beam_head.log 2>&1 &
env OL1_PL=kick nice -n 19 $PY ol1_run.py worlds/beam4.json 450 10 out/beam_pl.json worlds/beam_wave.json > out/beam_pl.log 2>&1 &
wait
# wave 2: the beam under PL-S1 + letter A, PL-S1 + letter B, letter A alone; the beam at rest under PL-S1 + letter A
env OL1_PL=kick OL1_ODD=exch nice -n 19 $PY ol1_run.py worlds/beam4.json 450 10 out/beam_pl_ola.json worlds/beam_wave.json > out/beam_pl_ola.log 2>&1 &
env OL1_PL=kick OL1_ODD=kick nice -n 19 $PY ol1_run.py worlds/beam4.json 450 10 out/beam_pl_olb.json worlds/beam_wave.json > out/beam_pl_olb.log 2>&1 &
env OL1_ODD=exch nice -n 19 $PY ol1_run.py worlds/beam4.json 450 10 out/beam_ola.json worlds/beam_wave.json > out/beam_ola.log 2>&1 &
env OL1_PL=kick OL1_ODD=exch nice -n 19 $PY ol1_run.py worlds/beam4.json 450 10 out/rest_pl_ola.json worlds/beam_rest.json > out/rest_pl_ola.log 2>&1 &
wait
echo wave2 > out/wave2.done
# wave 3: the plasma 3-cube and 5-cube under PL-S1 + letter A; the 3-cube under PL-S1 alone (the hash); the zigzag z1m head
env OL1_PL=kick OL1_ODD=exch nice -n 19 $PY ol1_run.py $W/world_plasma_3.json 400 10 out/p3_pl_ola.json > out/p3_pl_ola.log 2>&1 &
env OL1_PL=kick OL1_ODD=exch nice -n 19 $PY ol1_run.py $W/world_plasma.json 400 10 out/p5_pl_ola.json > out/p5_pl_ola.log 2>&1 &
env OL1_PL=kick nice -n 19 $PY ol1_run.py $W/world_plasma_3.json 400 10 out/p3_pl.json > out/p3_pl.log 2>&1 &
nice -n 19 $PY cs_run.py worlds/zigzag4_400.json out/z1m_head.json worlds/zigzag_m.json back 10 > out/z1m_head.log 2>&1 &
wait
echo wave3 > out/wave3.done
# wave 4: the zigzag under PL-S1 + letter A; the hole 60 under head, PL, PL + A
env OL1_PL=kick OL1_ODD=exch nice -n 19 $PY cs_run.py worlds/zigzag4_400.json out/z1m_pl_ola.json worlds/zigzag_m.json back 10 > out/z1m_pl_ola.log 2>&1 &
nice -n 19 $PY -m event_universe.run $W/world_hole.json out/hole_head.json back 10 > out/hole_head.log 2>&1 &
env OL1_PL=kick nice -n 19 $PY -m event_universe.run $W/world_hole.json out/hole_pl.json back 10 > out/hole_pl.log 2>&1 &
env OL1_PL=kick OL1_ODD=exch nice -n 19 $PY -m event_universe.run $W/world_hole.json out/hole_pl_ola.json back 10 > out/hole_pl_ola.log 2>&1 &
wait
echo wave4 > out/wave4.done
# wave 5: the hole under PL + B; the chiral 60 under head, PL, PL + A
env OL1_PL=kick OL1_ODD=kick nice -n 19 $PY -m event_universe.run $W/world_hole.json out/hole_pl_olb.json back 10 > out/hole_pl_olb.log 2>&1 &
nice -n 19 $PY -m event_universe.run $W/world_chiral.json out/chiral_head.json back 10 > out/chiral_head.log 2>&1 &
env OL1_PL=kick nice -n 19 $PY -m event_universe.run $W/world_chiral.json out/chiral_pl.json back 10 > out/chiral_pl.log 2>&1 &
env OL1_PL=kick OL1_ODD=exch nice -n 19 $PY -m event_universe.run $W/world_chiral.json out/chiral_pl_ola.json back 10 > out/chiral_pl_ola.log 2>&1 &
wait
echo wave5 > out/wave5.done
# wave 6: the chiral under PL + B; the bodies 300 under head, PL, PL + A
env OL1_PL=kick OL1_ODD=kick nice -n 19 $PY -m event_universe.run $W/world_chiral.json out/chiral_pl_olb.json back 10 > out/chiral_pl_olb.log 2>&1 &
nice -n 19 $PY -m event_universe.run $W/world_bodies.json out/bodies_head.json back 10 > out/bodies_head.log 2>&1 &
env OL1_PL=kick nice -n 19 $PY -m event_universe.run $W/world_bodies.json out/bodies_pl.json back 10 > out/bodies_pl.log 2>&1 &
env OL1_PL=kick OL1_ODD=exch nice -n 19 $PY -m event_universe.run $W/world_bodies.json out/bodies_pl_ola.json back 10 > out/bodies_pl_ola.log 2>&1 &
wait
echo wave6 > out/wave6.done
env OL1_PL=kick OL1_ODD=kick nice -n 19 $PY -m event_universe.run $W/world_bodies.json out/bodies_pl_olb.json back 10 > out/bodies_pl_olb.log 2>&1 &
wait
echo done > out/run_all.done
