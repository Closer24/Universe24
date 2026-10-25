#!/bin/sh
# lc2: the official records (python -m event_universe.run ... back 10) and the gates, per flag; one line per run
cd "$(dirname "$0")/out"
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=../src_lc2
rec() { echo "== $1 $2"; LC2_REACH=$2 nice -n 19 $PY -m event_universe.run $1 rec_$3_$2.json back 10 > log_$3_$2.txt 2>&1; LC2_REACH=$2 nice -n 19 $PY -m event_universe.gates rec_$3_$2.json > gates_$3_$2.txt 2>&1; }
unset LC2_REACH
echo "== chiral300 default"; nice -n 19 $PY -m event_universe.run world_chiral_300.json rec_chiral300_default.json back 10 > log_chiral300_default.txt 2>&1; nice -n 19 $PY -m event_universe.gates rec_chiral300_default.json > gates_chiral300_default.txt 2>&1
rec world_chiral_300.json harmonic chiral300
rec world_chiral_300.json product chiral300
rec world_sea3_400.json harmonic sea3
rec world_q1_3_400.json harmonic q1
rec world_hole3_400.json harmonic hole3
rec world_hole.json harmonic hole60
echo "== hole60 default"; nice -n 19 $PY -m event_universe.run world_hole.json rec_hole60_default.json back 10 > log_hole60_default.txt 2>&1; nice -n 19 $PY -m event_universe.gates rec_hole60_default.json > gates_hole60_default.txt 2>&1
rec world_bodies_120.json harmonic bodies120
echo "== bodies120 default"; nice -n 19 $PY -m event_universe.run world_bodies_120.json rec_bodies120_default.json back 10 > log_bodies120_default.txt 2>&1; nice -n 19 $PY -m event_universe.gates rec_bodies120_default.json > gates_bodies120_default.txt 2>&1
echo "== done"
