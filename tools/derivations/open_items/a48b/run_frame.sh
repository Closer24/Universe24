#!/bin/sh
# a48b: the frame fold on the 3-cube at 30, the 5-cube at 24, and the three records
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=src_a48b TMPDIR=/dev/shm/tmp A48B_FOLD=frame
$PY a48b_48.py worlds/world_chiral_3_30.json 30 out/c48_chiral3_30_frame.json notrack > out/c48_chiral3_30_frame.stdout 2>&1
cd worlds
export PYTHONPATH=../src_a48b
$PY -m event_universe.run world_hole_60.json ../out/rec_hole60_frame.json back 10 > ../out/rec_hole60_frame.stdout 2>&1
$PY -m event_universe.run world_chiral_300.json ../out/rec_chiral300_frame.json back 10 > ../out/rec_chiral300_frame.stdout 2>&1
$PY -m event_universe.run world_bodies_120.json ../out/rec_bodies120_frame.json back 10 > ../out/rec_bodies120_frame.stdout 2>&1
cd ..
export PYTHONPATH=src_a48b
$PY a48b_48.py worlds/world_chiral_5_24.json 24 out/c48_chiral5_24_frame.json notrack > out/c48_chiral5_24_frame.stdout 2>&1
echo done > out/run_frame.done
